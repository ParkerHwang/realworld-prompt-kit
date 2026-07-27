#!/usr/bin/env python3
"""Dependency-free validation and quality lint for the v0.1 broad core."""

from __future__ import annotations

import difflib
import itertools
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "v0.1" / "manifest.json"
EXPECTED_SCHEMA = "realworld-prompt-kit.scenario/0.1.0"
EXPECTED_MANIFEST_SCHEMA = "realworld-prompt-kit.manifest/0.1.0"
EXPECTED_CATALOG_SCHEMA = "realworld-prompt-kit.catalog/0.1.0"

REGULATED_DOMAINS = {
    "health_care",
    "legal_compliance",
    "finance_accounting_tax",
    "hr_people_labor",
    "privacy_security",
    "government_public_policy",
    "safety_emergency",
}

GENERAL_OFFICE_BUSINESS_EDUCATION_PERSONAL = {
    "general_knowledge",
    "office_admin",
    "communication_meetings",
    "project_product_management",
    "strategy_business_operations",
    "sales_marketing",
    "customer_support_success",
    "education_research",
    "personal_everyday",
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bLOREM\s+IPSUM\b", re.IGNORECASE),
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"<\s*(?:FILL|INSERT|TODO|PLACEHOLDER)[^>]*>", re.IGNORECASE),
)
PLACEHOLDER_WORD_PATTERN = re.compile(r"\bPLACEHOLDERS?\b", re.IGNORECASE)
VALID_PLACEHOLDER_CONTEXT_PATTERN = re.compile(
    r"\b(?:time|date|field|value|name|address|amount|missing|fixed|identical)\s+"
    r"placeholders?\b|\bplaceholder names?\b|\bplaceholders?\s+for\b|"
    r"\bmachine-readable\b",
    re.IGNORECASE,
)

KO_GRAMMAR_DEFECT_PATTERNS = (
    re.compile(
        r"안로|제안로|활동를|했다야|보고했다야|발상를|계획는|재개 안로|"
        r"섞임는|항목는|의식는|요약는|투명성는|기준는|버전는|게시물는|"
        r"결정는|양식는|입력는|시작라고|제공라고|불명확라고|가능라고|"
        r"완료라고(?!\s*표시하지)|"
        r"없음라고|보고함라고|평가라고|요청라고|인분 요청라고|。"
    ),
)
EN_GRAMMAR_DEFECT_PATTERNS = (
    re.compile(r"\.\."),
    re.compile(r"。"),
    re.compile(r"(?<=[.!?])\s+[a-z]"),
    re.compile(r"\bbehind\s+are\s+The\b"),
    re.compile(r"\bThe\s+option\s+[a-z]\s+entry\b"),
    re.compile(r"\bp\.m;"),
    re.compile(r"\b([A-Za-z]{2,}(?:\s+[A-Za-z]{2,})?)\s+\1\b", re.IGNORECASE),
)

# A repeated retrieval tail is not harmless boilerplate when it introduces a
# transport evidence fixture into a non-transport scenario. Keep the signal
# narrow enough to allow ordinary uses of "date" or "official source" while
# catching the known city/route/service-day and stop/route variants.
TRANSPORT_RETRIEVAL_TAIL_PATTERN = re.compile(
    r"(?:도시\s*[·,/、]\s*노선\s*[·,/、]\s*(?:운행일|날짜)|"
    r"city\s*[,/]\s*route\s*[,/]\s*(?:service\s+day|date)|"
    r"(?:정류장|stop)\s*(?:이나|또는|or)?\s*(?:경로|route)\s*"
    r"(?:가|는|is|are)?\s*(?:없|missing|absent)|"
    r"(?:stop|route)\s+(?:details?\s+)?(?:are\s+)?(?:missing|absent))",
    re.IGNORECASE,
)
TRANSPORT_CONTEXT_PATTERN = re.compile(
    r"버스|교통|시간표|정류장|노선|운행일|환승|기차|열차|항공|"
    r"transit|timetable|\bbus\b|\bstop\b|\broute\b|"
    r"service\s+day|\btrain\b|\bflight\b|commut",
    re.IGNORECASE,
)
NUMERIC_LITERAL_PATTERN = re.compile(r"(?<![\w])\d[\d,]*(?:\.\d+)?")
EN_POSSESSIVE_PATTERN = re.compile(r"\b([A-Za-z][A-Za-z-]{1,})'s\b")

RESPONSE_MODES = {
    "answer_directly",
    "infer_and_answer",
    "state_assumptions_and_answer",
    "ask_one_clarifying_question",
    "clarification_dialogue",
    "hold",
    "refuse_or_escalate",
}


def _naturalistic_feature_errors(
    document: dict[str, Any],
    path: Path,
    manifest: dict[str, Any] | None = None,
) -> list[str]:
    """Check objective naturalistic-profile evidence without guessing about style.

    Many profiles are pragmatic authoring labels (for example, an implicit goal
    or a polite request) and cannot be decided reliably with a language-neutral
    regular expression.  The release gate therefore enforces only cues that are
    objectively observable: message count, emoji, paste/format-noise markers,
    explicit correction/change/resumption language, and a minimum for a truly
    rambling stream.  The remaining profiles are still carried into the review
    report and must be inspected by a human; they are not silently treated as
    proven by generic boilerplate.

    A cue may be localized differently, so the hard checks use the pair of
    naturalistic realizations as the evidence scope.  ``message_burst`` is the
    exception: both localized prompts must contain the burst.
    """
    features = set(document.get("coverage", {}).get("naturalistic_features", []))
    naturalistic = [
        item
        for item in document.get("realizations", [])
        if isinstance(item, dict) and item.get("form") == "naturalistic"
    ]
    if not naturalistic:
        return []

    localized = [
        (realization_text(item), item.get("locale"), item.get("messages", []))
        for item in naturalistic
    ]
    all_text = "\n".join(text for text, _, _ in localized)
    profile_rules = (
        (manifest or {}).get("quality_gates", {}).get("profile_realism", {})
    )
    burst_min_messages = int(profile_rules.get("message_burst_min_messages_per_locale", 2))
    rambling_min_characters = int(
        profile_rules.get("rambling_stream_min_characters_per_locale", 180)
    )
    terse_max_tokens = int(
        profile_rules.get("terse_fragment_max_tokens_per_locale", 32)
    )
    terse_short_token_cutoff = int(
        profile_rules.get("terse_fragment_short_token_cutoff", 8)
    )
    terse_short_char_limit = int(
        profile_rules.get("terse_fragment_max_characters_when_under_8_tokens", 160)
    )

    cue_patterns: dict[str, re.Pattern[str]] = {
        "emoji_shorthand": re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"),
        "untrusted_embedded_instruction": re.compile(
            r"<\s*pasted|ignore all constraints|instruction inside|붙인 메모|복붙 문구|"
            r"지시(?:로|를).{0,12}(?:섞|따르|무시)",
            re.IGNORECASE,
        ),
        "interleaved_instruction_and_paste": re.compile(
            r"pasted|paste|copied|copy|reference material|source text|복붙|붙인|"
            r"붙여넣|참고 자료",
            re.IGNORECASE,
        ),
        "self_correction_scope_shift": re.compile(
            r"\b(?:actually|wait|correction|rather|narrow|changed|I meant|to be precise)\b|"
            r"그러니까|수정|정정|좁히|바꿔|다시 말|범위를",
            re.IGNORECASE,
        ),
        "mid_task_change": re.compile(
            r"\b(?:changed|change|changing|shifted|instead|new target|new direction|"
            r"move beyond|switch|pivot)\b|잠깐|초점을|방향을 바|바뀌|수정|다시|"
            r"조건을 바|전환",
            re.IGNORECASE,
        ),
        "resume_after_interruption": re.compile(
            r"\b(?:resume|resumed|resuming|resumption|interruption|earlier|previous|paused|"
            r"pick up|reconnect)\b|앞서|앞선|다시 잇|다시 여|멈췄|연결|중단|재개|이어|돌아|계속",
            re.IGNORECASE,
        ),
        "ocr_copy_format_noise": re.compile(
            r"ocr|pasted|copied|broken|damaged|garbled|column|line break|formatting|"
            r"복붙|깨졌|깨진|손상|줄바꿈|사진|표|오탈자|붙여",
            re.IGNORECASE,
        ),
        "typo_spacing_punctuation": re.compile(
            r"\.\.|[!?]{2,}|typo|spacing|ocr|joined words|attached punctuation|"
            r"\[copy\]|\[raw\]|messy paste|scan note|"
            r"오탈자|띄어쓰기|붙여쓰기|붙어 있는|문장부호|줄바꿈 섞임|복사본|스캔 텍스트|"
            r"안로|했다야|제안로|재개 안로|복붙한내용",
            re.IGNORECASE,
        ),
        "code_switching_jargon": re.compile(
            r"\b(?:API|CSV|KPI|SOP|OAuth|JSON|IT|URL|SDK|HTTP|SQL|CRM|ERP|"
            r"OCR|task ID|dashboard|workflow|connector|rollback|cache|payload|"
            r"schema|endpoint|webhook|ETL|SLA|OKR|ROI|A/B|UI|UX|regex|CLI|MVP|"
            r"DNS|status|owner|policy|review|prompt|token|timezone|checklist|caption|"
            r"budget|travel time|task|owner_role|due_date|dependency)(?:\b|(?=[가-힣]))",
            re.IGNORECASE,
        ),
    }

    errors: list[str] = []
    if "message_burst" in features and any(
        not isinstance(messages, list) or len(messages) < burst_min_messages
        for _, _, messages in localized
    ):
        errors.append(
            f"{path}: naturalistic feature 'message_burst' requires at least "
            f"{burst_min_messages} messages in each locale"
        )
    if "rambling_stream" in features and any(
        len(text) < rambling_min_characters
        for text, _, _messages in localized
    ):
        errors.append(
            f"{path}: naturalistic feature 'rambling_stream' requires at least "
            f"{rambling_min_characters} characters in each locale"
        )

    if "terse_fragment" in features and profile_rules.get("field_template_is_not_terse", True) and any(
        len(_word_tokens(text)) > terse_max_tokens
        for text, _, _messages in localized
    ):
        errors.append(
            f"{path}: naturalistic feature 'terse_fragment' exceeds the "
            f"{terse_max_tokens}-token per-locale limit"
        )

    if "terse_fragment" in features and any(
        len(_word_tokens(text)) <= terse_short_token_cutoff
        and len(text) > terse_short_char_limit
        for text, _, _messages in localized
    ):
        errors.append(
            f"{path}: naturalistic feature 'terse_fragment' is an overlong "
            f"serialized message ({terse_short_char_limit}-character limit when "
            f"under {terse_short_token_cutoff} whitespace tokens)"
        )

    if "terse_fragment" in features and any(
        text.count(";") >= 2
        and re.search(
            r"\b(?:known|result|context|deliver|gaps|topic)\b|주제|아는 내용|결과|산출물|빈칸",
            text,
            re.IGNORECASE,
        )
        for text, _, _ in localized
    ):
        errors.append(
            f"{path}: naturalistic feature 'terse_fragment' is realized as a field-template sentence, not a terse fragment"
        )
    if "terse_fragment" in features and any(
        re.search(
            r"(?:\b(?:topic|context|goal|known|result|output|deliverable|gap|request)\b|"
            r"주제|맥락|목표|아는 내용|결과|산출물|빈칸|요청)\s*[:=]\s*[^|;\n]+"
            r"(?:\s*[|;]\s*[^|;\n]+){1,}",
            text,
            re.IGNORECASE,
        )
        for text, _, _ in localized
    ):
        errors.append(
            f"{path}: naturalistic feature 'terse_fragment' is a serialized field list, not a user fragment"
        )

    hard_features = set(cue_patterns) - {"code_switching_jargon"}
    for feature in sorted(features & hard_features):
        if not cue_patterns[feature].search(all_text):
            errors.append(
                f"{path}: naturalistic feature {feature!r} is declared but has no observable cue"
            )
    if "code_switching_jargon" in features:
        # The ordinary English vocabulary in the English realization must not
        # satisfy this check.  A technical token in either localized prompt is
        # sufficient evidence of the profile.  Require the token in the
        # Korean realization so ordinary English prose cannot self-satisfy the
        # code-switching profile.
        korean_text = "\n".join(
            text for text, locale, _messages in localized if locale == "ko-KR"
        )
        if not cue_patterns["code_switching_jargon"].search(korean_text):
            errors.append(
                f"{path}: naturalistic feature 'code_switching_jargon' is declared but has no observable jargon cue"
            )
    return errors


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^\w]+", " ", value, flags=re.UNICODE).strip()


def realization_text(realization: dict[str, Any]) -> str:
    return "\n".join(
        str(message.get("content", ""))
        for message in realization.get("messages", [])
    ).strip()


def _transport_tail_context_errors(document: dict[str, Any], path: Path) -> list[str]:
    """Reject transport-specific retrieval boilerplate in unrelated tasks."""
    rendered = "\n".join(
        realization_text(item)
        for item in document.get("realizations", [])
        if isinstance(item, dict)
    )
    matches = list(TRANSPORT_RETRIEVAL_TAIL_PATTERN.finditer(rendered))
    if not matches:
        return []

    title = document.get("title", {})
    task = document.get("task", {})
    user_goal = task.get("user_goal", {}) if isinstance(task, dict) else {}
    semantic_context = " ".join(
        str(value)
        for value in (
            title.get("ko", "") if isinstance(title, dict) else "",
            title.get("en", "") if isinstance(title, dict) else "",
            user_goal.get("ko", "") if isinstance(user_goal, dict) else "",
            user_goal.get("en", "") if isinstance(user_goal, dict) else "",
            task.get("expected_artifact", "") if isinstance(task, dict) else "",
        )
    )
    if TRANSPORT_CONTEXT_PATTERN.search(semantic_context):
        return []
    examples = ", ".join(repr(match.group(0)) for match in matches[:2])
    return [
        f"{path}: transport-specific retrieval tail appears in a non-transport scenario ({examples})"
    ]


def _critical_fact_errors(document: dict[str, Any], path: Path) -> list[str]:
    """Check conservative literal preservation in canonical/naturalistic pairs."""
    by_pair = {
        (item.get("locale"), item.get("form")): realization_text(item)
        for item in document.get("realizations", [])
        if isinstance(item, dict)
    }
    errors: list[str] = []
    for locale in ("ko-KR", "en-US"):
        canonical = by_pair.get((locale, "canonical"), "")
        naturalistic = by_pair.get((locale, "naturalistic"), "")
        canonical_numbers = {
            token.replace(",", "") for token in NUMERIC_LITERAL_PATTERN.findall(canonical)
        }
        naturalistic_numbers = {
            token.replace(",", "") for token in NUMERIC_LITERAL_PATTERN.findall(naturalistic)
        }
        missing_numbers = sorted(canonical_numbers - naturalistic_numbers)
        if missing_numbers:
            errors.append(
                f"{path}: {locale} naturalistic realization drops canonical numeric "
                f"fact literal(s): {missing_numbers}"
            )
        if locale == "en-US":
            for base in EN_POSSESSIVE_PATTERN.findall(canonical):
                possessive = re.compile(rf"\b{re.escape(base)}'s\b", re.IGNORECASE)
                plural = re.compile(rf"\b{re.escape(base)}s\b", re.IGNORECASE)
                if not possessive.search(naturalistic) and plural.search(naturalistic):
                    errors.append(
                        f"{path}: en-US naturalistic realization turns canonical "
                        f"possessive {base!r}s into a bare plural"
                    )
    return errors


def _word_tokens(text: str) -> list[str]:
    """Return language-neutral word tokens for corpus phrase lint."""
    return normalize_text(text).split()


def scenario_paths(manifest: dict[str, Any], root: Path = ROOT) -> list[Path]:
    return sorted(root.glob(manifest["scenario_glob"]))


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _required_object(document: dict[str, Any], field_name: str, path: Path, errors: list[str]) -> dict[str, Any] | None:
    value = document.get(field_name)
    if not isinstance(value, dict):
        errors.append(f"{path}: {field_name} must be an object")
        return None
    return value


def _load_contract(manifest_path: Path, root: Path, report: ValidationReport) -> tuple[dict[str, Any], dict[str, Any]] | None:
    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report.errors.append(f"{manifest_path}: {exc}")
        return None
    if manifest.get("schema") != EXPECTED_MANIFEST_SCHEMA:
        report.errors.append(
            f"{manifest_path}: unsupported release manifest schema {manifest.get('schema')!r}"
        )
    catalog_path = root / manifest.get("catalog_path", "data/v0.1/catalog.json")
    try:
        catalog = load_json(catalog_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report.errors.append(f"{catalog_path}: {exc}")
        return manifest, {}
    if catalog.get("schema") != EXPECTED_CATALOG_SCHEMA:
        report.errors.append(
            f"{catalog_path}: unsupported release catalog schema {catalog.get('schema')!r}"
        )
    return manifest, catalog


def _intent_contract(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in catalog.get("task_intents", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _block_contract(catalog: dict[str, Any]) -> dict[str, set[str]]:
    return {
        intent_id: {
            f"{intent_id}.{block}.cb8" for block in item.get("blocks", [])
        }
        for intent_id, item in _intent_contract(catalog).items()
    }


def _validate_scenario(
    document: dict[str, Any],
    path: Path,
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    required = {
        "schema",
        "scenario_id",
        "revision",
        "status",
        "semantic_group_id",
        "title",
        "task",
        "coverage",
        "realizations",
        "evaluation",
        "provenance",
    }
    missing = sorted(required - document.keys())
    if missing:
        return [f"{path}: missing top-level fields: {', '.join(missing)}"]
    if document.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"{path}: unsupported scenario schema {document.get('schema')!r}")
    if not re.fullmatch(r"rwpk\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.[0-9]{4}", str(document.get("scenario_id", ""))):
        errors.append(f"{path}: invalid scenario_id")
    if not re.fullmatch(r"rwpg\.[a-z0-9_.]+", str(document.get("semantic_group_id", ""))):
        errors.append(f"{path}: invalid semantic_group_id")
    if not isinstance(document.get("revision"), int) or document["revision"] < 1:
        errors.append(f"{path}: revision must be a positive integer")
    if document.get("status") not in {"draft", "reviewed", "frozen", "retired"}:
        errors.append(f"{path}: invalid status")
    if manifest.get("status") == "released" and document.get("status") == "draft":
        errors.append(f"{path}: release-candidate scenarios must be reviewed or frozen, not draft")

    title = _required_object(document, "title", path, errors)
    if title is not None and (not str(title.get("ko", "")).strip() or not str(title.get("en", "")).strip()):
        errors.append(f"{path}: title must contain non-empty ko and en text")

    task = _required_object(document, "task", path, errors)
    coverage = _required_object(document, "coverage", path, errors)
    evaluation = _required_object(document, "evaluation", path, errors)
    provenance = _required_object(document, "provenance", path, errors)
    if task is None or coverage is None or evaluation is None or provenance is None:
        return errors

    intent_contract = _intent_contract(catalog)
    allowed_intents = set(intent_contract)
    primary_intent = task.get("primary_intent")
    if primary_intent not in allowed_intents:
        errors.append(f"{path}: unauthorized primary_intent {primary_intent!r}")
    secondary = task.get("secondary_intents", [])
    if not isinstance(secondary, list) or not all(isinstance(item, str) for item in secondary):
        errors.append(f"{path}: secondary_intents must be a list of strings")

    allowed_domains = set(catalog.get("authorized_domain_ids", []))
    primary_domain = task.get("primary_domain")
    if primary_domain not in allowed_domains:
        errors.append(f"{path}: unauthorized primary_domain {primary_domain!r}")
    domain_tags = task.get("domain_tags", [])
    if not isinstance(domain_tags, list) or any(tag not in allowed_domains for tag in domain_tags):
        errors.append(f"{path}: domain_tags contain an unauthorized domain id")
    user_goal = task.get("user_goal")
    if not isinstance(user_goal, dict) or not str(user_goal.get("ko", "")).strip() or not str(user_goal.get("en", "")).strip():
        errors.append(f"{path}: task.user_goal must contain non-empty ko and en text")
    if not str(task.get("expected_artifact", "")).strip():
        errors.append(f"{path}: task.expected_artifact must not be empty")

    block_id = coverage.get("block_id")
    blocks = _block_contract(catalog)
    if primary_intent in blocks and block_id not in blocks[primary_intent]:
        errors.append(f"{path}: block {block_id!r} is not declared for {primary_intent!r}")
    if isinstance(block_id, str):
        block_parts = block_id.split(".")
        if len(block_parts) != 3 or block_parts[-1] != "cb8" or block_parts[0] != primary_intent:
            errors.append(f"{path}: block_id must be <primary_intent>.<block>.cb8")
    row = coverage.get("row")
    if row not in range(1, 9):
        errors.append(f"{path}: coverage.row must be 1..8")
    facets = coverage.get("facets")
    levels = manifest.get("coverage_facets", {})
    if not isinstance(facets, dict):
        errors.append(f"{path}: coverage.facets must be an object")
    else:
        extra_facets = sorted(set(facets) - set(levels))
        if extra_facets:
            errors.append(f"{path}: coverage.facets contain unexpected factors {extra_facets}")
        for factor, expected_levels in levels.items():
            if facets.get(factor) not in expected_levels:
                errors.append(f"{path}: invalid {factor} facet {facets.get(factor)!r}")
    allowed_profiles = set(catalog.get("authorized_naturalistic_profile_ids", []))
    coverage_profiles = coverage.get("naturalistic_features", [])
    if not isinstance(coverage_profiles, list) or not coverage_profiles:
        errors.append(f"{path}: coverage.naturalistic_features must not be empty")
    elif any(profile not in allowed_profiles for profile in coverage_profiles):
        errors.append(f"{path}: coverage contains an unauthorized naturalistic profile")
    elif len(coverage_profiles) != len(set(coverage_profiles)):
        errors.append(f"{path}: coverage.naturalistic_features must not contain duplicates")

    realizations = document.get("realizations")
    if not isinstance(realizations, list):
        errors.append(f"{path}: realizations must be a list")
        realizations = []
    expected_pairs = {
        ("ko-KR", "canonical"),
        ("ko-KR", "naturalistic"),
        ("en-US", "canonical"),
        ("en-US", "naturalistic"),
    }
    actual_pairs = {(item.get("locale"), item.get("form")) for item in realizations if isinstance(item, dict)}
    if actual_pairs != expected_pairs:
        errors.append(f"{path}: realization pairs differ from required ko/en canonical/naturalistic set")
    if len(realizations) != int(manifest.get("realizations_per_scenario", 4)):
        errors.append(f"{path}: expected exactly four realizations, got {len(realizations)}")
    min_chars = int(manifest.get("quality_gates", {}).get("minimum_prompt_characters", 40))
    for item in realizations:
        if not isinstance(item, dict):
            errors.append(f"{path}: realization must be an object")
            continue
        prompt_id = item.get("prompt_id", "<missing>")
        locale = item.get("locale")
        form = item.get("form")
        if not isinstance(prompt_id, str) or not prompt_id.startswith(f"{document.get('scenario_id')}."):
            errors.append(f"{path}: {prompt_id} prompt_id is not rooted at scenario_id")
        if locale not in {"ko-KR", "en-US"} or form not in {"canonical", "naturalistic"}:
            errors.append(f"{path}: {prompt_id} has invalid locale/form")
        elif prompt_id != f"{document.get('scenario_id')}.{locale}.{form}":
            errors.append(f"{path}: {prompt_id} must end with its exact locale/form pair")
        features = item.get("features", [])
        if not isinstance(features, list) or any(profile not in allowed_profiles for profile in features):
            errors.append(f"{path}: {prompt_id} contains an unauthorized profile feature")
        elif len(features) != len(set(features)):
            errors.append(f"{path}: {prompt_id} contains duplicate profile features")
        if form == "canonical":
            if item.get("origin") != "controlled_canonical":
                errors.append(f"{path}: canonical {prompt_id} has wrong origin")
            if features:
                errors.append(f"{path}: canonical {prompt_id} must not claim naturalistic profiles")
        elif form == "naturalistic":
            if item.get("origin") != "synthetic_naturalistic":
                errors.append(f"{path}: naturalistic {prompt_id} must be synthetic")
            if not features:
                errors.append(f"{path}: naturalistic {prompt_id} needs at least one profile")
            elif set(features) != set(coverage_profiles):
                errors.append(
                    f"{path}: naturalistic {prompt_id} features must match coverage.naturalistic_features"
                )
        messages = item.get("messages", [])
        if not isinstance(messages, list) or not messages:
            errors.append(f"{path}: {prompt_id} must contain at least one message")
            continue
        text = realization_text(item)
        if len(text) < min_chars:
            errors.append(f"{path}: {prompt_id} is below minimum prompt substance ({len(text)} < {min_chars} chars)")
        if locale == "ko-KR" and not re.search(r"[가-힣]", text):
            errors.append(f"{path}: {prompt_id} lacks Korean language presence")
        if locale == "en-US" and not re.search(r"[A-Za-z]", text):
            errors.append(f"{path}: {prompt_id} lacks English language presence")
        if locale == "ko-KR":
            for pattern in KO_GRAMMAR_DEFECT_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{path}: {prompt_id} contains a known Korean grammar defect")
                    break
        if locale == "en-US":
            for pattern in EN_GRAMMAR_DEFECT_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{path}: {prompt_id} contains a known English capitalization or punctuation defect")
                    break
        if any(pattern.search(text) for pattern in PLACEHOLDER_PATTERNS) or (
            PLACEHOLDER_WORD_PATTERN.search(text)
            and not VALID_PLACEHOLDER_CONTEXT_PATTERN.search(text)
        ):
            errors.append(f"{path}: {prompt_id} contains placeholder leakage")

    evaluation_modes = evaluation.get("response_mode")
    if not isinstance(evaluation_modes, dict) or not evaluation_modes.get("canonical") or not evaluation_modes.get("naturalistic"):
        errors.append(f"{path}: evaluation.response_mode must define canonical and naturalistic")
    elif any(mode not in RESPONSE_MODES for mode in evaluation_modes.values()):
        errors.append(f"{path}: evaluation.response_mode contains an unsupported behavior mode")
    if isinstance(evaluation_modes, dict) and evaluation_modes.get("naturalistic") == "refuse_or_escalate":
        behavior_text = " ".join(
            str(value)
            for field_name in ("title", "task", "evaluation")
            for value in ([document.get(field_name)] if isinstance(document.get(field_name), str) else [])
        )
        behavior_text = " ".join(
            [
                str(title.get("ko", "")) if isinstance(title, dict) else "",
                str(title.get("en", "")) if isinstance(title, dict) else "",
                str(task.get("user_goal", {}).get("ko", "")) if isinstance(task.get("user_goal"), dict) else "",
                str(task.get("user_goal", {}).get("en", "")) if isinstance(task.get("user_goal"), dict) else "",
                str(task.get("expected_artifact", "")),
            ]
        ).casefold()
        risk_markers = r"self[- ]?harm|suicid|immediate danger|abuse|harass|panic|emergency|crisis|diagnos|prescri|medical appointment|safety concern|긴급|위험|자해|자살|학대|괴롭힘|공황|응급|진단|처방|안전 우려"
        if primary_intent == "coaching_conversational_support" and not re.search(risk_markers, behavior_text):
            errors.append(
                f"{path}: benign coaching/support request must not use naturalistic response_mode=refuse_or_escalate"
            )
    for field_name in ("invariants", "rubric_dimensions", "failure_signals"):
        value = evaluation.get(field_name)
        if not isinstance(value, list) or not value or not all(str(item).strip() for item in value):
            errors.append(f"{path}: evaluation.{field_name} must not be empty")
    if primary_domain in REGULATED_DOMAINS:
        evaluation_text = " ".join(
            str(item)
            for field_name in ("invariants", "failure_signals")
            for item in evaluation.get(field_name, [])
        ).casefold()
        if not re.search(r"uncertain|assumption|official|professional|escalat|review|verify|source", evaluation_text):
            errors.append(f"{path}: regulated domain lacks an uncertainty or escalation boundary")

    if provenance.get("origin") != "synthetic":
        errors.append(f"{path}: public release scenarios must declare origin=synthetic")
    if provenance.get("contains_personal_data") is not False:
        errors.append(f"{path}: public scenarios must declare contains_personal_data=false")
    if provenance.get("rights_basis") != "original_project_authorship":
        errors.append(f"{path}: unsupported rights_basis")
    if provenance.get("license") != "MIT":
        errors.append(f"{path}: provenance license must be MIT")
    errors.extend(_naturalistic_feature_errors(document, path, manifest))
    errors.extend(_transport_tail_context_errors(document, path))
    errors.extend(_critical_fact_errors(document, path))
    return errors


def _pairwise_errors(
    scenarios_by_block: dict[str, list[dict[str, Any]]],
    manifest: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    factor_levels: dict[str, list[str]] = manifest.get("coverage_facets", {})
    for block_id, scenarios in sorted(scenarios_by_block.items()):
        if len(scenarios) != 8:
            errors.append(f"coverage: {block_id} expected 8 scenarios, found {len(scenarios)}")
            continue
        rows = [scenario.get("coverage", {}).get("facets", {}) for scenario in scenarios]
        observed_rows = {scenario.get("coverage", {}).get("row") for scenario in scenarios}
        if observed_rows != set(range(1, 9)):
            errors.append(f"coverage: {block_id} rows must be exactly 1..8")
        for factor, levels in factor_levels.items():
            observed = {row.get(factor) for row in rows}
            if observed != set(levels):
                errors.append(f"coverage: {block_id} {factor} expected levels {levels}, observed {sorted(observed)}")
        for left, right in itertools.combinations(factor_levels, 2):
            expected = set(itertools.product(factor_levels[left], factor_levels[right]))
            observed = {(row.get(left), row.get(right)) for row in rows}
            if observed != expected:
                missing = sorted(expected - observed)
                errors.append(f"coverage: {block_id} pair {left} × {right} missing {missing}")
    return errors


def _quality_lint(
    scenarios: Iterable[dict[str, Any]],
    manifest: dict[str, Any],
    root: Path,
) -> tuple[list[str], list[str], dict[str, Any]]:
    scenarios = list(scenarios)
    errors: list[str] = []
    warnings: list[str] = []
    exact_texts: defaultdict[str, list[str]] = defaultdict(list)
    normalized_texts: defaultdict[str, list[str]] = defaultdict(list)
    similarity_pairs: list[dict[str, Any]] = []
    semantic_title_keys: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
    semantic_goal_keys: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
    canonical_by_intent: defaultdict[str, list[tuple[str, str, str, str]]] = defaultdict(list)
    phrase_counts: defaultdict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    phrase_examples: defaultdict[tuple[str, str, str], list[str]] = defaultdict(list)
    warning_threshold = float(manifest.get("quality_gates", {}).get("similarity_warning_threshold", 0.75))
    failure_threshold = float(manifest.get("quality_gates", {}).get("similarity_failure_threshold", 0.85))
    phrase_config = manifest.get("quality_gates", {}).get("phrase_concentration", {})
    phrase_size = int(phrase_config.get("ngram_size", 6))
    # The release contract is deliberately strict even when a caller supplies
    # a partial manifest: more than five percent of the scenarios in a
    # locale/form is an error.  The manifest repeats this value explicitly,
    # but the validator must not silently fall back to the former 10% draft
    # threshold.
    phrase_max_fraction = float(phrase_config.get("max_scenario_fraction", 0.05))
    phrase_review_fraction = float(phrase_config.get("review_fraction", 0.05))
    phrase_whitelist = {
        normalize_text(str(value))
        for value in phrase_config.get("whitelist", [])
        if str(value).strip()
    }
    for scenario in scenarios:
        scenario_id = str(scenario.get("scenario_id"))
        task = scenario.get("task", {})
        coverage = scenario.get("coverage", {})
        intent = str(task.get("primary_intent", ""))
        block_id = str(coverage.get("block_id", ""))
        title = scenario.get("title", {})

        def semantic_base(value: Any) -> str:
            text = str(value or "")
            text = re.split(r"\s*(?:·|—|–|\|)\s*", text, maxsplit=1)[0]
            text = re.sub(r"\s*\([^)]*\)\s*$", "", text)
            text = re.sub(r"\s*\[[^]]*\]\s*$", "", text)
            return normalize_text(text)

        title_base = semantic_base(title.get("en") or title.get("ko"))
        goal = task.get("user_goal", {})
        goal_base_en = semantic_base(goal.get("en"))
        goal_base_ko = semantic_base(goal.get("ko"))
        if title_base:
            semantic_title_keys[f"{intent}|{title_base}"].append((scenario_id, block_id))
        if goal_base_en or goal_base_ko:
            semantic_goal_keys[f"{intent}|{goal_base_en}|{goal_base_ko}"].append((scenario_id, block_id))
        by_pair = {
            (item.get("locale"), item.get("form")): item
            for item in scenario.get("realizations", [])
            if isinstance(item, dict)
        }
        for realization in scenario.get("realizations", []):
            if not isinstance(realization, dict):
                continue
            prompt_id = str(realization.get("prompt_id", "<missing>"))
            text = realization_text(realization)
            exact_texts[text].append(prompt_id)
            normalized_texts[normalize_text(text)].append(prompt_id)
            if phrase_size > 0:
                locale = str(realization.get("locale", ""))
                form = str(realization.get("form", ""))
                tokens = _word_tokens(text)
                ngrams = {
                    " ".join(tokens[index:index + phrase_size])
                    for index in range(len(tokens) - phrase_size + 1)
                }
                for ngram in ngrams:
                    phrase_counts[(locale, form)][ngram] += 1
                    phrase_examples[(locale, form, ngram)].append(scenario_id)
            if realization.get("form") == "canonical":
                canonical_by_intent[intent].append(
                    (block_id, str(realization.get("locale", "")), scenario_id, normalize_text(text))
                )
        for locale in ("ko-KR", "en-US"):
            canonical = by_pair.get((locale, "canonical"))
            naturalistic = by_pair.get((locale, "naturalistic"))
            if not canonical or not naturalistic:
                continue
            canonical_text = realization_text(canonical)
            naturalistic_text = realization_text(naturalistic)
            normalized_canonical = normalize_text(canonical_text)
            normalized_naturalistic = normalize_text(naturalistic_text)
            if normalized_canonical == normalized_naturalistic:
                errors.append(f"{scenario_id}: {locale} canonical and naturalistic prompts are identical after normalization")
                continue
            similarity = difflib.SequenceMatcher(
                None, normalized_canonical, normalized_naturalistic
            ).ratio()
            if similarity >= warning_threshold:
                entry = {
                    "scenario_id": scenario_id,
                    "locale": locale,
                    "similarity": round(similarity, 4),
                    "canonical_prompt_id": canonical.get("prompt_id"),
                    "naturalistic_prompt_id": naturalistic.get("prompt_id"),
                }
                similarity_pairs.append(entry)
                if similarity >= failure_threshold:
                    errors.append(
                        f"{scenario_id}: {locale} canonical/naturalistic similarity {similarity:.3f} >= {failure_threshold:.2f}"
                    )
    duplicate_groups = {
        "exact": [values for values in exact_texts.values() if len(values) > 1],
        "normalized": [values for values in normalized_texts.values() if len(values) > 1],
    }
    for scope, groups in duplicate_groups.items():
        if groups:
            preview = "; ".join(", ".join(group[:4]) for group in groups[:3])
            errors.append(f"quality: {scope} duplicate prompt text groups={len(groups)} ({preview})")
    semantic_title_duplicates = [
        values for values in semantic_title_keys.values()
        if len({block_id for _, block_id in values}) > 1
    ]
    semantic_goal_duplicates = [
        values for values in semantic_goal_keys.values()
        if len({block_id for _, block_id in values}) > 1
    ]
    if semantic_title_duplicates:
        preview = "; ".join(
            ", ".join(f"{scenario_id}@{block_id}" for scenario_id, block_id in values[:4])
            for values in semantic_title_duplicates[:3]
        )
        errors.append(
            f"semantic: duplicate normalized title bases across blocks={len(semantic_title_duplicates)} ({preview})"
        )
    if semantic_goal_duplicates:
        preview = "; ".join(
            ", ".join(f"{scenario_id}@{block_id}" for scenario_id, block_id in values[:4])
            for values in semantic_goal_duplicates[:3]
        )
        errors.append(
            f"semantic: duplicate normalized goals across blocks={len(semantic_goal_duplicates)} ({preview})"
        )
    high_similarity_cross_block: list[dict[str, Any]] = []
    for intent, entries in canonical_by_intent.items():
        for left, right in itertools.combinations(entries, 2):
            left_block, left_locale, left_id, left_text = left
            right_block, right_locale, right_id, right_text = right
            if left_block == right_block or left_locale != right_locale:
                continue
            similarity = difflib.SequenceMatcher(None, left_text, right_text).ratio()
            if similarity >= 0.90:
                high_similarity_cross_block.append(
                    {
                        "intent": intent,
                        "locale": left_locale,
                        "left_scenario_id": left_id,
                        "right_scenario_id": right_id,
                        "left_block": left_block,
                        "right_block": right_block,
                        "similarity": round(similarity, 4),
                    }
                )
    if high_similarity_cross_block:
        preview = "; ".join(
            f"{item['left_scenario_id']}↔{item['right_scenario_id']}={item['similarity']:.3f}"
            for item in high_similarity_cross_block[:5]
        )
        errors.append(
            f"semantic: high canonical similarity across blocks={len(high_similarity_cross_block)} ({preview})"
        )
    warning_fraction = len(similarity_pairs) / max(1, sum(1 for _ in scenarios) * 2)
    failure_count = sum(1 for item in similarity_pairs if item["similarity"] >= failure_threshold)
    failure_fraction = failure_count / max(1, sum(1 for _ in scenarios) * 2)
    max_warning_fraction = float(manifest.get("quality_gates", {}).get("max_warning_fraction_without_documented_exception", 0.10))
    max_failure_fraction = float(manifest.get("quality_gates", {}).get("max_failure_fraction_without_documented_exception", 0.02))
    if warning_fraction > max_warning_fraction:
        errors.append(
            f"quality: {warning_fraction:.1%} of locale pairs exceed similarity warning threshold; maximum is {max_warning_fraction:.1%}"
        )
    if failure_fraction > max_failure_fraction:
        errors.append(
            f"quality: {failure_fraction:.1%} of locale pairs exceed similarity failure threshold; maximum is {max_failure_fraction:.1%}"
        )
    if similarity_pairs:
        warnings.append(
            f"quality: {len(similarity_pairs)} locale pairs exceed similarity warning threshold {warning_threshold:.2f}"
        )
    phrase_concentration_violations: list[dict[str, Any]] = []
    phrase_concentration_reviews: list[dict[str, Any]] = []
    scenario_denominator = max(1, len(scenarios))
    for (locale, form), counts in sorted(phrase_counts.items()):
        for ngram, count in counts.most_common():
            normalized_ngram = normalize_text(ngram)
            if normalized_ngram in phrase_whitelist:
                continue
            fraction = count / scenario_denominator
            item = {
                "locale": locale,
                "form": form,
                "ngram": ngram,
                "scenario_count": count,
                "fraction": round(fraction, 6),
                "examples": phrase_examples[(locale, form, ngram)][:8],
            }
            if fraction > phrase_max_fraction:
                phrase_concentration_violations.append(item)
            elif fraction > phrase_review_fraction:
                phrase_concentration_reviews.append(item)
    if phrase_concentration_violations:
        preview = "; ".join(
            f"{item['locale']}/{item['form']} {item['scenario_count']} ({item['fraction']:.1%}): {item['ngram']}"
            for item in phrase_concentration_violations[:5]
        )
        errors.append(
            "quality: phrase concentration exceeds the configured corpus fraction "
            f"{phrase_max_fraction:.1%} ({preview})"
        )
    if phrase_concentration_reviews:
        warnings.append(
            "quality: phrase-concentration review candidates="
            f"{len(phrase_concentration_reviews)} above {phrase_review_fraction:.1%}"
        )
    return errors, warnings, {
        "phrase_scenario_denominator": len(scenarios),
        "phrase_locale_form_scope": "locale_and_form",
        "phrase_whitelist": sorted(phrase_whitelist),
        "phrase_max_scenario_fraction": phrase_max_fraction,
        "phrase_review_fraction": phrase_review_fraction,
        "similarity_warning_pairs": len(similarity_pairs),
        "similarity_failure_pairs": failure_count,
        "similarity_warning_fraction": round(warning_fraction, 6),
        "similarity_failure_fraction": round(failure_fraction, 6),
        "similarity_pairs": similarity_pairs,
        "exact_duplicate_groups": len(duplicate_groups["exact"]),
        "normalized_duplicate_groups": len(duplicate_groups["normalized"]),
        "semantic_title_duplicate_groups": len(semantic_title_duplicates),
        "semantic_goal_duplicate_groups": len(semantic_goal_duplicates),
        "high_similarity_cross_block_pairs": len(high_similarity_cross_block),
        "high_similarity_cross_block_examples": high_similarity_cross_block[:25],
        "phrase_concentration_violation_count": len(phrase_concentration_violations),
        "phrase_concentration_review_count": len(phrase_concentration_reviews),
        "phrase_concentration_violations": phrase_concentration_violations[:100],
        "phrase_concentration_reviews": phrase_concentration_reviews[:100],
    }


def validate_repository(
    manifest_path: Path = DEFAULT_MANIFEST,
    root: Path = ROOT,
) -> ValidationReport:
    report = ValidationReport()
    contract = _load_contract(manifest_path, root, report)
    if contract is None:
        return report
    manifest, catalog = contract
    paths = scenario_paths(manifest, root) if manifest.get("scenario_glob") else []
    loaded: list[tuple[Path, dict[str, Any]]] = []
    scenarios: list[dict[str, Any]] = []
    scenario_validation_error_count = 0
    transport_tail_error_count = 0
    critical_fact_error_count = 0
    for path in paths:
        try:
            document = load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            report.errors.append(f"{_relative(path, root)}: {exc}")
            continue
        loaded.append((path, document))
        scenarios.append(document)
        scenario_errors = _validate_scenario(
            document, _relative(path, root), manifest, catalog
        )
        report.errors.extend(scenario_errors)
        scenario_validation_error_count += len(scenario_errors)
        transport_tail_error_count += sum(
            "transport-specific retrieval tail" in error for error in scenario_errors
        )
        critical_fact_error_count += sum(
            "drops canonical numeric fact" in error or "bare plural" in error
            for error in scenario_errors
        )

    scenario_ids: defaultdict[str, list[str]] = defaultdict(list)
    group_ids: defaultdict[str, list[str]] = defaultdict(list)
    prompt_ids: defaultdict[str, list[str]] = defaultdict(list)
    scenarios_by_block: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    domain_counts: Counter[str] = Counter()
    profile_counts: Counter[str] = Counter()
    intent_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    for scenario in scenarios:
        path_label = str(scenario.get("scenario_id", "<unknown>"))
        scenario_ids[str(scenario.get("scenario_id"))].append(path_label)
        group_ids[str(scenario.get("semantic_group_id"))].append(path_label)
        coverage = scenario.get("coverage", {})
        block_id = coverage.get("block_id")
        scenarios_by_block[str(block_id)].append(scenario)
        intent = scenario.get("task", {}).get("primary_intent")
        intent_counts[str(intent)] += 1
        status_counts[str(scenario.get("status"))] += 1
        domain_counts[str(scenario.get("task", {}).get("primary_domain"))] += 1
        for profile in coverage.get("naturalistic_features", []):
            profile_counts[str(profile)] += 1
        for realization in scenario.get("realizations", []):
            if isinstance(realization, dict):
                prompt_ids[str(realization.get("prompt_id"))].append(path_label)

    for label, values in (("scenario_id", scenario_ids), ("semantic_group_id", group_ids), ("prompt_id", prompt_ids)):
        for identifier, occurrences in values.items():
            if len(occurrences) > 1:
                report.errors.append(f"identity: duplicate {label} {identifier!r} ({len(occurrences)} occurrences)")

    expected_scenarios = int(manifest.get("expected_scenarios", 0))
    expected_blocks = int(manifest.get("expected_blocks", 0))
    expected_realizations = int(manifest.get("expected_realizations", 0))
    realization_count = sum(len(scenario.get("realizations", [])) for scenario in scenarios)
    if len(scenarios) != expected_scenarios:
        report.errors.append(f"manifest: expected {expected_scenarios} scenarios, found {len(scenarios)}")
    if len(scenarios_by_block) != expected_blocks:
        report.errors.append(f"manifest: expected {expected_blocks} CB8 blocks, found {len(scenarios_by_block)}")
    if realization_count != expected_realizations:
        report.errors.append(f"manifest: expected {expected_realizations} prompt realizations, found {realization_count}")
    report.errors.extend(_pairwise_errors(dict(scenarios_by_block), manifest))

    partition_quality: dict[str, Any] = {}
    partition_paths_seen: set[Path] = set()
    intent_order = [
        item.get("id")
        for item in catalog.get("task_intents", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    for partition in manifest.get("partitions", []):
        if not isinstance(partition, dict):
            continue
        partition_id = str(partition.get("id", "<unnamed>"))
        intent_range = partition.get("intent_range", [])
        try:
            start, end = int(intent_range[0]), int(intent_range[1])
        except (IndexError, TypeError, ValueError):
            report.errors.append(f"partition {partition_id}: invalid intent_range")
            continue
        partition_intents = set(intent_order[max(0, start - 1):end])
        partition_glob = partition.get("scenario_glob")
        if not isinstance(partition_glob, str) or not partition_glob.strip():
            report.errors.append(f"partition {partition_id}: scenario_glob is required")
            partition_paths = {
                path
                for path, scenario in loaded
                if scenario.get("task", {}).get("primary_intent") in partition_intents
            }
        else:
            partition_paths = set(root.glob(partition_glob))
            if not partition_paths:
                report.errors.append(
                    f"partition {partition_id}: scenario_glob matched no scenario files"
                )
        overlap = sorted(partition_paths & partition_paths_seen)
        if overlap:
            report.errors.append(
                f"partition {partition_id}: scenario_glob overlaps earlier partition files "
                f"({', '.join(_relative(path, root) for path in overlap[:4])})"
            )
        partition_paths_seen.update(partition_paths)
        partition_scenarios = [
            scenario
            for path, scenario in loaded
            if path in partition_paths
        ]
        unexpected_intents = sorted(
            {
                str(scenario.get("task", {}).get("primary_intent"))
                for scenario in partition_scenarios
                if scenario.get("task", {}).get("primary_intent") not in partition_intents
            }
        )
        if unexpected_intents:
            report.errors.append(
                f"partition {partition_id}: scenario_glob includes intents outside its range "
                f"{unexpected_intents}"
            )
        expected_partition_scenarios = partition.get("expected_scenarios")
        if isinstance(expected_partition_scenarios, int) and len(partition_scenarios) != expected_partition_scenarios:
            report.errors.append(
                f"partition {partition_id}: expected {expected_partition_scenarios} scenarios, "
                f"found {len(partition_scenarios)}"
            )
        expected_partition_blocks = partition.get("expected_blocks")
        observed_partition_blocks = {
            str(scenario.get("coverage", {}).get("block_id"))
            for scenario in partition_scenarios
        }
        if isinstance(expected_partition_blocks, int) and len(observed_partition_blocks) != expected_partition_blocks:
            report.errors.append(
                f"partition {partition_id}: expected {expected_partition_blocks} blocks, "
                f"found {len(observed_partition_blocks)}"
            )
        partition_errors, partition_warnings, partition_stats = _quality_lint(
            partition_scenarios, manifest, root
        )
        report.errors.extend(
            f"partition {partition_id}: {error}" for error in partition_errors
        )
        report.warnings.extend(
            f"partition {partition_id}: {warning}" for warning in partition_warnings
        )
        partition_quality[partition_id] = {
            "intent_range": [start, end],
            "scenario_glob": partition_glob,
            "scenario_count": len(partition_scenarios),
            "cb8_block_count": len(observed_partition_blocks),
            "prompt_realization_count": sum(
                len(scenario.get("realizations", [])) for scenario in partition_scenarios
            ),
            "quality_errors": len(partition_errors),
            "quality_warnings": len(partition_warnings),
            "phrase_ngram_size": int(
                manifest.get("quality_gates", {})
                .get("phrase_concentration", {})
                .get("ngram_size", 6)
            ),
            "phrase_max_scenario_fraction": partition_stats.get(
                "phrase_max_scenario_fraction", 0.05
            ),
            "phrase_review_fraction": partition_stats.get(
                "phrase_review_fraction", 0.05
            ),
            "phrase_scenario_denominator": partition_stats.get(
                "phrase_scenario_denominator", len(partition_scenarios)
            ),
            "phrase_locale_form_scope": partition_stats.get(
                "phrase_locale_form_scope", "locale_and_form"
            ),
            "phrase_concentration_violation_count": partition_stats.get(
                "phrase_concentration_violation_count", 0
            ),
            "phrase_concentration_review_count": partition_stats.get(
                "phrase_concentration_review_count", 0
            ),
            "similarity_warning_pairs": partition_stats.get(
                "similarity_warning_pairs", 0
            ),
            "similarity_failure_pairs": partition_stats.get(
                "similarity_failure_pairs", 0
            ),
            "semantic_goal_duplicate_groups": partition_stats.get(
                "semantic_goal_duplicate_groups", 0
            ),
            "high_similarity_cross_block_pairs": partition_stats.get(
                "high_similarity_cross_block_pairs", 0
            ),
        }

    loaded_paths = {path for path, _scenario in loaded}
    unassigned_paths = sorted(loaded_paths - partition_paths_seen)
    if unassigned_paths:
        report.errors.append(
            "partitions: scenario files are outside every declared partition "
            f"({', '.join(_relative(path, root) for path in unassigned_paths[:6])})"
        )

    intent_contract = _intent_contract(catalog)
    expected_intents = set(intent_contract)
    if len(expected_intents) != int(manifest.get("expected_intents", 0)):
        report.errors.append("catalog: expected_intents does not match catalog task_intents")
    if set(intent_counts) != expected_intents:
        report.errors.append(f"catalog: observed intents differ from catalog ({sorted(set(intent_counts) ^ expected_intents)})")
    expected_blocks_by_intent = _block_contract(catalog)
    for intent_id, block_ids in expected_blocks_by_intent.items():
        observed_blocks = {block_id for block_id in scenarios_by_block if block_id.startswith(f"{intent_id}.")}
        if observed_blocks != block_ids:
            report.errors.append(f"quota: {intent_id} block set differs from catalog")
        expected_count = int(intent_contract[intent_id].get("expected_scenarios", len(block_ids) * 8))
        if intent_counts.get(intent_id, 0) != expected_count:
            report.errors.append(f"quota: {intent_id} expected {expected_count} scenarios, found {intent_counts.get(intent_id, 0)}")

    authorized_domains = set(catalog.get("authorized_domain_ids", []))
    minimum_domain_count = int(catalog.get("domain_quota_overlays", {}).get("minimum_scenarios_per_domain", 1))
    missing_domains = sorted(domain for domain in authorized_domains if domain_counts.get(domain, 0) < minimum_domain_count)
    if missing_domains:
        report.errors.append(f"quota: domains below minimum presence: {', '.join(missing_domains)}")
    if set(domain_counts) - authorized_domains:
        report.errors.append(f"quota: unauthorized primary domains: {sorted(set(domain_counts) - authorized_domains)}")
    denominator = max(1, len(scenarios))
    broad_ratio = sum(domain_counts[domain] for domain in GENERAL_OFFICE_BUSINESS_EDUCATION_PERSONAL) / denominator
    software_ratio = (domain_counts["software_it"] + domain_counts["data_analytics"]) / denominator
    guardrails = manifest.get("composition_guardrails", {})
    if broad_ratio < float(guardrails.get("general_office_business_education_personal_min_ratio", 0.60)):
        report.errors.append(f"quota: broad general/office/business/education/personal ratio {broad_ratio:.1%} is below gate")
    if software_ratio > float(guardrails.get("software_it_plus_data_analytics_max_ratio", 0.20)):
        report.errors.append(f"quota: software_it+data_analytics ratio {software_ratio:.1%} exceeds gate")

    authorized_profiles = set(catalog.get("authorized_naturalistic_profile_ids", []))
    minimum_profile_count = int(catalog.get("profile_quota_overlays", {}).get("minimum_scenarios_per_profile", 1))
    missing_profiles = sorted(profile for profile in authorized_profiles if profile_counts.get(profile, 0) < minimum_profile_count)
    if missing_profiles:
        report.errors.append(f"quota: profiles below minimum presence: {', '.join(missing_profiles)}")
    if set(profile_counts) - authorized_profiles:
        report.errors.append(f"quota: unauthorized naturalistic profiles: {sorted(set(profile_counts) - authorized_profiles)}")

    quality_errors, quality_warnings, quality_stats = _quality_lint(scenarios, manifest, root)
    report.errors.extend(quality_errors)
    report.warnings.extend(quality_warnings)
    report.stats.update(quality_stats)
    report.stats.update(
        {
            "semantic_scenarios": len(scenarios),
            "cb8_blocks": len(scenarios_by_block),
            "prompt_realizations": realization_count,
            "scenario_validation_error_count": scenario_validation_error_count,
            "transport_tail_error_count": transport_tail_error_count,
            "critical_fact_error_count": critical_fact_error_count,
            "manifest_status": manifest.get("status"),
            "suite_status": manifest.get("suite_status", {}),
            "task_intents": len(intent_counts),
            "domain_counts": dict(sorted(domain_counts.items())),
            "profile_counts": dict(sorted(profile_counts.items())),
            "intent_counts": dict(sorted(intent_counts.items())),
            "status_counts": dict(sorted(status_counts.items())),
            "broad_ratio": round(broad_ratio, 6),
            "software_data_ratio": round(software_ratio, 6),
            "phrase_ngram_size": int(
                manifest.get("quality_gates", {})
                .get("phrase_concentration", {})
                .get("ngram_size", 6)
            ),
            "phrase_max_scenario_fraction": quality_stats.get(
                "phrase_max_scenario_fraction", 0.05
            ),
            "phrase_review_fraction": quality_stats.get(
                "phrase_review_fraction", 0.05
            ),
            "phrase_scenario_denominator": quality_stats.get(
                "phrase_scenario_denominator", len(scenarios)
            ),
            "phrase_locale_form_scope": quality_stats.get(
                "phrase_locale_form_scope", "locale_and_form"
            ),
            "phrase_concentration_metric": manifest.get("quality_gates", {})
            .get("phrase_concentration", {})
            .get("metric"),
            "partition_quality": partition_quality,
            "blocks": {
                block_id: {
                    "scenario_ids": sorted(scenario.get("scenario_id", "") for scenario in block_scenarios),
                    "sample_scenario_id": min(
                        (str(scenario.get("scenario_id", "")) for scenario in block_scenarios),
                        default="",
                    ),
                }
                for block_id, block_scenarios in sorted(scenarios_by_block.items())
            },
        }
    )
    return report
