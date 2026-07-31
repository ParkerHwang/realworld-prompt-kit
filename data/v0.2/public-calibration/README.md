
# Public calibration references

This directory contains 18 synthetic reference artifacts for the 12 v0.2 work
episodes. They demonstrate one valid way to satisfy each artifact contract and
are used to verify that the deterministic grader can recognize a conforming
package.

They are not byte-for-byte gold answers. Submissions may differ in structure,
wording, formulas, or visual design when the declared task properties, source
facts, filenames, editability requirements, and hard gates still pass.

## Human calibration status

Status: `not_run`

No practitioner score, model ranking, locale-parity conclusion, or leaderboard
claim is attached to these files. Before an episode can move from
`calibration_ready` to `reviewed`, record:

1. at least two blind workplace-practitioner reviews of materially different
   system outputs;
2. agreement and adjudication results for every human or model-judge item;
3. separate Korean and English calibration evidence;
4. any repaired or removed ambiguous rubric items;
5. reviewer roles, review date, protocol version, and immutable evidence path;
6. an independent run of the package without author assistance.

The scenario schema blocks `reviewed` and `frozen` status unless human
calibration is marked completed. Automated reference conformance alone cannot
promote an episode.
