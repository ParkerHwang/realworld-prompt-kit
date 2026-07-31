#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
const artifactToolModule =
  globalThis.process?.env?.RWPK_ARTIFACT_TOOL_MODULE ?? "@oai/artifact-tool";
const {
  Presentation,
  PresentationFile,
  SpreadsheetFile,
  Workbook,
} = await import(artifactToolModule);

const runtimeArgs = globalThis.process?.argv ?? [];
const repoRoot = path.resolve(runtimeArgs[2] ?? ".");
const qaRoot = path.resolve(
  runtimeArgs[3] ?? path.join(repoRoot, "tmp", "v0.2-office-qa"),
);
const dataRoot = path.join(repoRoot, "data", "v0.2");

const COLORS = {
  navy: "#17324D",
  blue: "#2F6B8A",
  cyan: "#57C7D4",
  ink: "#182230",
  muted: "#5D6B79",
  pale: "#EDF4F7",
  white: "#FFFFFF",
  green: "#2E7D65",
  amber: "#B7791F",
  red: "#B94A48",
  grid: "#D7E1E7",
};

async function ensureParent(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

async function writeBlob(filePath, blob) {
  await ensureParent(filePath);
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

async function removeInspectSidecar(filePath) {
  await fs.rm(`${filePath}.inspect.ndjson`, { force: true });
}

function addText(slide, name, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: style.fontSize ?? 26,
    color: style.color ?? COLORS.ink,
    bold: style.bold ?? false,
    alignment: style.alignment ?? "left",
    verticalAlignment: style.verticalAlignment ?? "middle",
  };
  return shape;
}

function addRule(slide, top, color = COLORS.cyan) {
  return slide.shapes.add({
    geometry: "rect",
    name: `rule-${top}`,
    position: { left: 72, top, width: 136, height: 7 },
    fill: color,
    line: { style: "solid", fill: color, width: 0 },
  });
}

function addFooter(slide, text, page) {
  addText(
    slide,
    `footer-${page}`,
    `${text}  |  ${page}`,
    { left: 72, top: 668, width: 1136, height: 22 },
    { fontSize: 15, color: COLORS.muted, alignment: "right" },
  );
}

function addDeckTitleSlide(presentation, spec) {
  const slide = presentation.slides.add();
  slide.background.fill = COLORS.navy;
  slide.shapes.add({
    geometry: "rect",
    name: "accent-band",
    position: { left: 0, top: 0, width: 26, height: 720 },
    fill: COLORS.cyan,
    line: { style: "solid", fill: COLORS.cyan, width: 0 },
  });
  addText(
    slide,
    "kicker",
    spec.kicker.toUpperCase(),
    { left: 88, top: 86, width: 720, height: 34 },
    { fontSize: 20, color: COLORS.cyan, bold: true },
  );
  addText(
    slide,
    "deck-title",
    spec.title,
    { left: 88, top: 166, width: 1010, height: 170 },
    { fontSize: 68, color: COLORS.white, bold: true },
  );
  addText(
    slide,
    "deck-subtitle",
    spec.subtitle,
    { left: 90, top: 368, width: 950, height: 104 },
    { fontSize: 29, color: "#D8E6ED" },
  );
  addText(
    slide,
    "deck-period",
    spec.period,
    { left: 90, top: 568, width: 500, height: 32 },
    { fontSize: 20, color: COLORS.white, bold: true },
  );
  addFooter(slide, "RWPK v0.2 synthetic fixture", 1);
}

function addMetricSlide(presentation, spec) {
  const slide = presentation.slides.add();
  slide.background.fill = COLORS.white;
  addText(
    slide,
    "slide-title",
    spec.metricTitle,
    { left: 72, top: 52, width: 1136, height: 68 },
    { fontSize: 48, color: COLORS.navy, bold: true },
  );
  addRule(slide, 132);

  addText(
    slide,
    "metric-value",
    spec.metricValue,
    { left: 76, top: 184, width: 350, height: 112 },
    { fontSize: 66, color: spec.metricColor ?? COLORS.green, bold: true },
  );
  addText(
    slide,
    "metric-label",
    spec.metricLabel,
    { left: 78, top: 304, width: 360, height: 84 },
    { fontSize: 25, color: COLORS.muted },
  );
  addText(
    slide,
    "metric-interpretation",
    spec.metricInterpretation,
    { left: 78, top: 430, width: 370, height: 132 },
    { fontSize: 24, color: COLORS.ink },
  );

  slide.shapes.add({
    geometry: "roundRect",
    name: "chart-frame",
    position: { left: 492, top: 176, width: 716, height: 408 },
    fill: COLORS.pale,
    line: { style: "solid", fill: COLORS.grid, width: 1 },
    borderRadius: "rounded-xl",
  });
  slide.charts.add("bar", {
    position: { left: 540, top: 218, width: 620, height: 318 },
    categories: spec.chartCategories,
    series: [
      {
        name: spec.chartSeriesName,
        values: spec.chartValues,
        fill: COLORS.blue,
      },
    ],
    hasLegend: false,
    dataLabels: { showValue: true, position: "outEnd" },
    xAxis: {
      majorGridlines: { style: "solid", fill: COLORS.grid, width: 1 },
    },
  });
  addFooter(slide, "RWPK v0.2 synthetic fixture", 2);
}

function addActionSlide(presentation, spec) {
  const slide = presentation.slides.add();
  slide.background.fill = COLORS.pale;
  addText(
    slide,
    "slide-title",
    spec.actionTitle,
    { left: 72, top: 52, width: 1136, height: 70 },
    { fontSize: 48, color: COLORS.navy, bold: true },
  );
  addRule(slide, 132, COLORS.blue);

  const rows = spec.actions.slice(0, 3);
  rows.forEach((action, index) => {
    const top = 188 + index * 144;
    addText(
      slide,
      `action-number-${index + 1}`,
      String(index + 1).padStart(2, "0"),
      { left: 76, top, width: 90, height: 76 },
      { fontSize: 38, color: COLORS.cyan, bold: true },
    );
    addText(
      slide,
      `action-title-${index + 1}`,
      action.title,
      { left: 176, top, width: 430, height: 52 },
      { fontSize: 28, color: COLORS.navy, bold: true },
    );
    addText(
      slide,
      `action-detail-${index + 1}`,
      action.detail,
      { left: 622, top: top - 2, width: 560, height: 92 },
      { fontSize: 22, color: COLORS.ink },
    );
  });
  addFooter(slide, "RWPK v0.2 synthetic fixture", 3);
}

async function buildDeck(relativePath, spec) {
  const presentation = Presentation.create({
    slideSize: { width: 1280, height: 720 },
  });
  addDeckTitleSlide(presentation, spec);
  addMetricSlide(presentation, spec);
  addActionSlide(presentation, spec);

  const outputPath = path.join(dataRoot, relativePath);
  await ensureParent(outputPath);
  const deck = await PresentationFile.exportPptx(presentation);
  await deck.save(outputPath);
  await removeInspectSidecar(outputPath);

  const qaDir = path.join(
    qaRoot,
    "presentations",
    path.basename(relativePath, ".pptx"),
  );
  await fs.mkdir(qaDir, { recursive: true });
  for (const [index, slide] of presentation.slides.items.entries()) {
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await writeBlob(
      path.join(qaDir, `slide-${String(index + 1).padStart(2, "0")}.png`),
      png,
    );
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(
      path.join(qaDir, `slide-${String(index + 1).padStart(2, "0")}.layout.json`),
      await layout.text(),
    );
  }
  const montage = await presentation.export({
    format: "webp",
    montage: true,
    scale: 1,
  });
  await writeBlob(path.join(qaDir, "montage.webp"), montage);
}

function styleTitle(sheet, range) {
  range.format = {
    fill: COLORS.navy,
    font: { bold: true, color: COLORS.white, size: 18 },
    verticalAlignment: "center",
  };
  range.format.rowHeight = 34;
}

function styleHeader(range) {
  range.format = {
    fill: COLORS.blue,
    font: { bold: true, color: COLORS.white },
    borders: { preset: "outside", style: "thin", color: COLORS.blue },
    verticalAlignment: "center",
    wrapText: true,
  };
  range.format.rowHeight = 28;
}

function styleBody(range) {
  range.format = {
    borders: {
      insideHorizontal: { style: "thin", color: COLORS.grid },
      bottom: { style: "thin", color: COLORS.grid },
    },
    verticalAlignment: "center",
  };
}

async function renderWorkbook(workbook, relativePath, sheetNames) {
  const qaDir = path.join(
    qaRoot,
    "workbooks",
    path.basename(relativePath, ".xlsx"),
  );
  await fs.mkdir(qaDir, { recursive: true });
  for (const sheetName of sheetNames) {
    const preview = await workbook.render({
      sheetName,
      autoCrop: "all",
      scale: 1,
      format: "png",
    });
    await writeBlob(
      path.join(qaDir, `${sheetName.replaceAll(" ", "-")}.png`),
      preview,
    );
  }
}

async function saveWorkbook(workbook, relativePath, sheetNames) {
  const outputPath = path.join(dataRoot, relativePath);
  await ensureParent(outputPath);
  await renderWorkbook(workbook, relativePath, sheetNames);
  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);
  await removeInspectSidecar(outputPath);
}

async function buildExpenseExtractionWorkbook() {
  const workbook = Workbook.create();
  const data = workbook.worksheets.add("Extracted Expenses");
  const checks = workbook.worksheets.add("Checks");
  data.showGridLines = false;
  checks.showGridLines = false;

  data.getRange("A1:F1").merge();
  data.getRange("A1").values = [["Expense table extraction"]];
  styleTitle(data, data.getRange("A1:F1"));
  data.getRange("A3:F3").values = [[
    "Date",
    "Department",
    "Category",
    "Vendor",
    "Amount",
    "Receipt ID",
  ]];
  styleHeader(data.getRange("A3:F3"));
  data.getRange("A4:F9").values = [
    [new Date("2026-04-03"), "Operations", "Shipping", "Cobalt Freight", 1280, "R-1041"],
    [new Date("2026-04-06"), "People", "Training", "Northline Learning", 860, "R-1042"],
    [new Date("2026-04-09"), "Sales", "Travel", "Harbor Rail", 420, "R-1043"],
    [new Date("2026-04-13"), "Operations", "Supplies", "Beacon Office", 315, "R-1044"],
    [new Date("2026-04-18"), "Marketing", "Events", "Civic Hall", 2100, "R-1045"],
    [new Date("2026-04-24"), "People", "Recruiting", "Evergreen Jobs", 740, "R-1046"],
  ];
  data.getRange("A4:A9").format.numberFormat = "yyyy-mm-dd";
  data.getRange("E4:E9").format.numberFormat = "$#,##0";
  styleBody(data.getRange("A4:F9"));
  data.getRange("A3:F9").format.autofitColumns();
  data.getRange("B:F").format.columnWidth = 18;
  data.freezePanes.freezeRows(3);

  checks.getRange("A1:D1").merge();
  checks.getRange("A1").values = [["Extraction checks"]];
  styleTitle(checks, checks.getRange("A1:D1"));
  checks.getRange("A3:B6").values = [
    ["Check", "Result"],
    ["Row count", null],
    ["Amount total", null],
    ["Duplicate receipt IDs", null],
  ];
  checks.getRange("B4").formulas = [["=COUNTA('Extracted Expenses'!$A$4:$A$9)"]];
  checks.getRange("B5").formulas = [["=SUM('Extracted Expenses'!$E$4:$E$9)"]];
  checks.getRange("B6").formulas = [["=COUNTA('Extracted Expenses'!$F$4:$F$9)-COUNTA(UNIQUE('Extracted Expenses'!$F$4:$F$9))"]];
  styleHeader(checks.getRange("A3:B3"));
  styleBody(checks.getRange("A4:B6"));
  checks.getRange("B5").format.numberFormat = "$#,##0";
  checks.getRange("A:B").format.columnWidth = 24;

  await saveWorkbook(
    workbook,
    "public-calibration/rwpk.extraction_parsing.scanned_expense_table.0002/expense-table-extracted.xlsx",
    ["Extracted Expenses", "Checks"],
  );
}

async function buildStatusWorkbook() {
  const workbook = Workbook.create();
  const raw = workbook.worksheets.add("Source Data");
  const summary = workbook.worksheets.add("Status Summary");
  const assumptions = workbook.worksheets.add("Assumptions");
  for (const sheet of [raw, summary, assumptions]) sheet.showGridLines = false;

  raw.getRange("A1:F1").values = [[
    "Project",
    "Owner",
    "Status",
    "Budget",
    "Budget Used",
    "Target Date",
  ]];
  raw.getRange("A2:F7").values = [
    ["Atlas migration", "Operations", "On Track", 42000, 27400, new Date("2026-08-15")],
    ["Beacon onboarding", "Customer Success", "At Risk", 28000, 24100, new Date("2026-07-31")],
    ["Cobalt launch", "Marketing", "On Track", 35000, 18200, new Date("2026-09-10")],
    ["Delta controls", "Finance", "Blocked", 18000, 9600, new Date("2026-08-01")],
    ["Evergreen renewal", "Sales", "At Risk", 22000, 19600, new Date("2026-08-20")],
    ["Harbor training", "People", "On Track", 12000, 5400, new Date("2026-09-01")],
  ];
  styleHeader(raw.getRange("A1:F1"));
  styleBody(raw.getRange("A2:F7"));
  raw.getRange("D2:E7").format.numberFormat = "$#,##0";
  raw.getRange("F2:F7").format.numberFormat = "yyyy-mm-dd";
  raw.getRange("A:F").format.columnWidth = 20;
  raw.freezePanes.freezeRows(1);

  summary.getRange("A1:D1").merge();
  summary.getRange("A1").values = [["Project portfolio status"]];
  styleTitle(summary, summary.getRange("A1:D1"));
  summary.getRange("A3:D3").values = [["Status", "Projects", "Budget", "Budget Used"]];
  summary.getRange("A4:A6").values = [["On Track"], ["At Risk"], ["Blocked"]];
  summary.getRange("B4").formulas = [["=COUNTIF('Source Data'!$C$2:$C$7,A4)"]];
  summary.getRange("B4:B6").fillDown();
  summary.getRange("C4").formulas = [["=SUMIF('Source Data'!$C$2:$C$7,A4,'Source Data'!$D$2:$D$7)"]];
  summary.getRange("C4:C6").fillDown();
  summary.getRange("D4").formulas = [["=SUMIF('Source Data'!$C$2:$C$7,A4,'Source Data'!$E$2:$E$7)"]];
  summary.getRange("D4:D6").fillDown();
  styleHeader(summary.getRange("A3:D3"));
  styleBody(summary.getRange("A4:D6"));
  summary.getRange("C4:D6").format.numberFormat = "$#,##0";
  summary.getRange("A:D").format.columnWidth = 19;
  const chart = summary.charts.add("bar", summary.getRange("A3:B6"));
  chart.title = "Projects by status";
  chart.hasLegend = false;
  chart.setPosition("F2", "M17");

  assumptions.getRange("A1:C1").merge();
  assumptions.getRange("A1").values = [["Assumptions and checks"]];
  styleTitle(assumptions, assumptions.getRange("A1:C1"));
  assumptions.getRange("A3:B6").values = [
    ["Item", "Definition"],
    ["Status", "Source values are treated as authoritative labels."],
    ["Currency", "All budget figures are synthetic US dollars."],
    ["Refresh", "Summary formulas update when source rows change within rows 2-7."],
  ];
  styleHeader(assumptions.getRange("A3:B3"));
  styleBody(assumptions.getRange("A4:B6"));
  assumptions.getRange("A:A").format.columnWidth = 18;
  assumptions.getRange("B:B").format.columnWidth = 58;
  assumptions.getRange("B4:B6").format.wrapText = true;

  await saveWorkbook(
    workbook,
    "public-calibration/rwpk.quantitative_formal_analysis.project_status_workbook.0007/project-status-summary.xlsx",
    ["Source Data", "Status Summary", "Assumptions"],
  );
}

async function buildBudgetWorkbooks() {
  const source = Workbook.create();
  const sourceSheet = source.worksheets.add("Budget");
  sourceSheet.showGridLines = false;
  sourceSheet.getRange("A1:D1").merge();
  sourceSheet.getRange("A1").values = [["Quarterly budget - repair required"]];
  styleTitle(sourceSheet, sourceSheet.getRange("A1:D1"));
  sourceSheet.getRange("A3:D3").values = [["Department", "Plan", "Actual", "Variance"]];
  sourceSheet.getRange("A4:C7").values = [
    ["Operations", 42000, 44600],
    ["Marketing", 36000, 33100],
    ["People", 28000, 29100],
    ["Technology", 51000, 49800],
  ];
  sourceSheet.getRange("D4").formulas = [["=B4-C4"]];
  sourceSheet.getRange("D4:D7").fillDown();
  sourceSheet.getRange("A8:C8").values = [["Total", null, null]];
  sourceSheet.getRange("B8").formulas = [["=SUM(B4:B6)"]];
  sourceSheet.getRange("C8").formulas = [["=SUM(C4:C7)"]];
  sourceSheet.getRange("D8").formulas = [["=B8-C8"]];
  styleHeader(sourceSheet.getRange("A3:D3"));
  styleBody(sourceSheet.getRange("A4:D8"));
  sourceSheet.getRange("B4:D8").format.numberFormat = "$#,##0;[Red]-$#,##0";
  sourceSheet.getRange("A:D").format.columnWidth = 20;
  await saveWorkbook(
    source,
    "assets/rwpk.diagnosis_root_cause.budget_workbook_repair.0008/budget-with-range-error.xlsx",
    ["Budget"],
  );

  const repaired = Workbook.create();
  const budget = repaired.worksheets.add("Budget");
  const checks = repaired.worksheets.add("Checks");
  budget.showGridLines = false;
  checks.showGridLines = false;
  budget.getRange("A1:D1").merge();
  budget.getRange("A1").values = [["Quarterly budget - repaired"]];
  styleTitle(budget, budget.getRange("A1:D1"));
  budget.getRange("A3:D3").values = [["Department", "Plan", "Actual", "Variance"]];
  budget.getRange("A4:C7").values = [
    ["Operations", 42000, 44600],
    ["Marketing", 36000, 33100],
    ["People", 28000, 29100],
    ["Technology", 51000, 49800],
  ];
  budget.getRange("D4").formulas = [["=B4-C4"]];
  budget.getRange("D4:D7").fillDown();
  budget.getRange("A8").values = [["Total"]];
  budget.getRange("B8").formulas = [["=SUM(B4:B7)"]];
  budget.getRange("C8").formulas = [["=SUM(C4:C7)"]];
  budget.getRange("D8").formulas = [["=B8-C8"]];
  styleHeader(budget.getRange("A3:D3"));
  styleBody(budget.getRange("A4:D8"));
  budget.getRange("A8:D8").format.font = { bold: true };
  budget.getRange("B4:D8").format.numberFormat = "$#,##0;[Red]-$#,##0";
  budget.getRange("A:D").format.columnWidth = 20;

  checks.getRange("A1:D1").merge();
  checks.getRange("A1").values = [["Repair checks"]];
  styleTitle(checks, checks.getRange("A1:D1"));
  checks.getRange("A3:B5").values = [
    ["Check", "Result"],
    ["Plan total", null],
    ["Variance reconciliation", null],
  ];
  checks.getRange("B4").formulas = [["='Budget'!B8"]];
  checks.getRange("B5").formulas = [["='Budget'!B8-'Budget'!C8-'Budget'!D8"]];
  styleHeader(checks.getRange("A3:B3"));
  styleBody(checks.getRange("A4:B5"));
  checks.getRange("B4").format.numberFormat = "$#,##0";
  checks.getRange("A:B").format.columnWidth = 26;

  await saveWorkbook(
    repaired,
    "public-calibration/rwpk.diagnosis_root_cause.budget_workbook_repair.0008/budget-repaired.xlsx",
    ["Budget", "Checks"],
  );
}

async function buildOpsWorkbook() {
  const workbook = Workbook.create();
  const data = workbook.worksheets.add("Monthly Data");
  const summary = workbook.worksheets.add("Management Summary");
  data.showGridLines = false;
  summary.showGridLines = false;
  data.getRange("A1:E1").values = [["Month", "Orders", "On-time %", "Backlog", "Support cases"]];
  data.getRange("A2:E7").values = [
    ["Jan", 1180, 0.91, 84, 126],
    ["Feb", 1240, 0.92, 79, 118],
    ["Mar", 1310, 0.9, 96, 134],
    ["Apr", 1390, 0.93, 71, 112],
    ["May", 1460, 0.94, 63, 105],
    ["Jun", 1525, 0.95, 54, 99],
  ];
  styleHeader(data.getRange("A1:E1"));
  styleBody(data.getRange("A2:E7"));
  data.getRange("C2:C7").format.numberFormat = "0.0%";
  data.getRange("A:E").format.columnWidth = 18;
  data.freezePanes.freezeRows(1);

  summary.getRange("A1:D1").merge();
  summary.getRange("A1").values = [["Monthly operations summary"]];
  styleTitle(summary, summary.getRange("A1:D1"));
  summary.getRange("A3:B6").values = [
    ["KPI", "Latest"],
    ["Orders", null],
    ["On-time delivery", null],
    ["Backlog", null],
  ];
  summary.getRange("B4").formulas = [["='Monthly Data'!B7"]];
  summary.getRange("B5").formulas = [["='Monthly Data'!C7"]];
  summary.getRange("B6").formulas = [["='Monthly Data'!D7"]];
  styleHeader(summary.getRange("A3:B3"));
  styleBody(summary.getRange("A4:B6"));
  summary.getRange("B5").format.numberFormat = "0.0%";
  summary.getRange("A:B").format.columnWidth = 24;
  // Keep measures with incompatible scales out of one plot. On-time delivery
  // remains visible as a formatted KPI while the chart shows order volume.
  const chart = summary.charts.add("line", data.getRange("A1:B7"));
  chart.title = "Order volume trend";
  chart.hasLegend = false;
  chart.setPosition("D3", "L18");

  await saveWorkbook(
    workbook,
    "public-calibration/rwpk.operations_monitoring_improvement.monthly_ops_package.0009/monthly-ops-workbook.xlsx",
    ["Monthly Data", "Management Summary"],
  );
}

async function buildCampaignSourceWorkbook() {
  const workbook = Workbook.create();
  const results = workbook.worksheets.add("Campaign Results");
  results.showGridLines = false;
  results.getRange("A1:F1").values = [[
    "Channel",
    "Spend",
    "Leads",
    "Qualified",
    "Pipeline",
    "Cost per qualified lead",
  ]];
  results.getRange("A2:E5").values = [
    ["Search", 24000, 720, 198, 310000],
    ["Events", 18000, 260, 104, 220000],
    ["Partner", 12000, 180, 92, 205000],
    ["Email", 6000, 420, 84, 98000],
  ];
  results.getRange("F2").formulas = [["=B2/D2"]];
  results.getRange("F2:F5").fillDown();
  styleHeader(results.getRange("A1:F1"));
  styleBody(results.getRange("A2:F5"));
  results.getRange("B2:B5").format.numberFormat = "$#,##0";
  results.getRange("E2:E5").format.numberFormat = "$#,##0";
  results.getRange("F2:F5").format.numberFormat = "$#,##0";
  results.getRange("A:F").format.columnWidth = 20;
  await saveWorkbook(
    workbook,
    "assets/rwpk.evaluation_review_audit.campaign_readout_package.0010/campaign-results.xlsx",
    ["Campaign Results"],
  );
}

async function buildDeliveryTracker() {
  const workbook = Workbook.create();
  const tracker = workbook.worksheets.add("Delivery Tracker");
  tracker.showGridLines = false;
  tracker.getRange("A1:F1").merge();
  tracker.getRange("A1").values = [["Quarterly delivery tracker"]];
  styleTitle(tracker, tracker.getRange("A1:F1"));
  tracker.getRange("A3:F3").values = [[
    "Deliverable",
    "Owner role",
    "Status",
    "Due date",
    "Dependency",
    "Check",
  ]];
  tracker.getRange("A4:E7").values = [
    ["Executive recap", "Program lead", "Complete", new Date("2026-07-31"), "Approved metrics"],
    ["Action tracker", "Operations", "Complete", new Date("2026-07-31"), "Owner confirmation"],
    ["Handoff note", "Program lead", "Complete", new Date("2026-07-31"), "Package manifest"],
    ["Archive copy", "Operations", "Ready", new Date("2026-08-03"), "Final sign-off"],
  ];
  tracker.getRange("F4").formulas = [["=IF(C4=\"Complete\",\"OK\",\"OPEN\")"]];
  tracker.getRange("F4:F7").fillDown();
  styleHeader(tracker.getRange("A3:F3"));
  styleBody(tracker.getRange("A4:F7"));
  tracker.getRange("D4:D7").format.numberFormat = "yyyy-mm-dd";
  tracker.getRange("A:F").format.columnWidth = 20;
  tracker.getRange("E:E").format.columnWidth = 28;
  tracker.freezePanes.freezeRows(3);
  await saveWorkbook(
    workbook,
    "public-calibration/rwpk.one_off_tool_execution.delivery_package.0012/delivery-tracker.xlsx",
    ["Delivery Tracker"],
  );
}

const decks = [
  {
    relativePath:
      "assets/rwpk.transformation_rewriting.deck_feedback_revision.0006/existing-status-deck.pptx",
    spec: {
      kicker: "Existing draft",
      title: "Service readiness update",
      subtitle: "A synthetic draft deck before reviewer feedback is applied.",
      period: "Q2 2026",
      metricTitle: "Readiness is improving, but handoff risk remains",
      metricValue: "82%",
      metricLabel: "workstreams marked ready",
      metricInterpretation: "The draft does not yet separate confirmed readiness from owner-reported confidence.",
      chartCategories: ["Data", "Training", "Support", "Handoff"],
      chartValues: [92, 88, 81, 67],
      chartSeriesName: "Readiness",
      actionTitle: "Draft actions",
      actions: [
        { title: "Close data checks", detail: "Confirm the last migration sample before the next review." },
        { title: "Finish training", detail: "Publish the role-based quick reference." },
        { title: "Prepare handoff", detail: "Assign the support owner and escalation window." },
      ],
    },
  },
  {
    relativePath:
      "public-calibration/rwpk.summarization_synthesis.executive_update_deck.0005/executive-update-deck.pptx",
    spec: {
      kicker: "Executive update",
      title: "Portfolio delivery is stabilizing",
      subtitle: "Progress, risk, and decisions distilled from the source report and metrics.",
      period: "June 2026",
      metricTitle: "Three workstreams are on plan; one needs a decision",
      metricValue: "3 / 4",
      metricLabel: "workstreams on plan",
      metricInterpretation: "The capacity decision for Enablement is the only unresolved executive dependency.",
      chartCategories: ["Platform", "Data", "Enablement", "Support"],
      chartValues: [94, 91, 68, 87],
      chartSeriesName: "Completion %",
      actionTitle: "Decisions that keep July on track",
      actions: [
        { title: "Approve capacity", detail: "Add one facilitator to Enablement through July 18." },
        { title: "Protect scope", detail: "Keep the Platform change freeze through migration validation." },
        { title: "Confirm ownership", detail: "Name the post-launch Support escalation owner." },
      ],
    },
  },
  {
    relativePath:
      "public-calibration/rwpk.transformation_rewriting.deck_feedback_revision.0006/revised-status-deck.pptx",
    spec: {
      kicker: "Revised update",
      title: "Handoff ownership is the remaining readiness gap",
      subtitle: "Reviewer feedback applied without changing the underlying source figures.",
      period: "Q2 2026",
      metricTitle: "Confirmed readiness is 76%, below the reported 82%",
      metricValue: "76%",
      metricLabel: "readiness after evidence checks",
      metricInterpretation: "The revision distinguishes verified completion from owner confidence and keeps all figures source-grounded.",
      chartCategories: ["Data", "Training", "Support", "Handoff"],
      chartValues: [92, 84, 78, 52],
      chartSeriesName: "Verified readiness",
      actionTitle: "Three actions resolve the gap",
      actions: [
        { title: "Assign handoff owner", detail: "Name one accountable role by July 8." },
        { title: "Verify training", detail: "Use completion records rather than self-reported confidence." },
        { title: "Publish escalation path", detail: "Document the first-response and executive escalation windows." },
      ],
    },
  },
  {
    relativePath:
      "public-calibration/rwpk.operations_monitoring_improvement.monthly_ops_package.0009/monthly-ops-deck.pptx",
    spec: {
      kicker: "Operations review",
      title: "Throughput rose as backlog fell",
      subtitle: "A six-month management view of orders, delivery reliability, and workload.",
      period: "January-June 2026",
      metricTitle: "June closed with the strongest service balance",
      metricValue: "95%",
      metricLabel: "on-time delivery in June",
      metricInterpretation: "Orders reached 1,525 while backlog declined to 54 items.",
      chartCategories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      chartValues: [1180, 1240, 1310, 1390, 1460, 1525],
      chartSeriesName: "Orders",
      actionTitle: "Protect the gains in the next cycle",
      actions: [
        { title: "Hold service floor", detail: "Escalate if on-time delivery falls below 93%." },
        { title: "Watch backlog", detail: "Review the queue if open items exceed 70." },
        { title: "Share capacity", detail: "Move one support block to peak order days." },
      ],
    },
  },
  {
    relativePath:
      "public-calibration/rwpk.evaluation_review_audit.campaign_readout_package.0010/campaign-recap-deck.pptx",
    spec: {
      kicker: "Campaign readout",
      title: "Partners produced the most efficient qualified demand",
      subtitle: "A decision-ready recap grounded in the campaign workbook and brand brief.",
      period: "Spring 2026",
      metricTitle: "Partner spend generated the lowest cost per qualified lead",
      metricValue: "$130",
      metricLabel: "cost per qualified lead",
      metricInterpretation: "Search created more total pipeline, while Partner delivered stronger efficiency.",
      chartCategories: ["Search", "Events", "Partner", "Email"],
      chartValues: [121, 173, 130, 71],
      chartSeriesName: "Cost / qualified lead",
      actionTitle: "Shift the next test toward efficient scale",
      actions: [
        { title: "Expand Partner", detail: "Increase the next-cycle test while preserving qualification criteria." },
        { title: "Refine Search", detail: "Separate high-intent terms before raising spend." },
        { title: "Keep Email lean", detail: "Use the channel for nurture rather than broad acquisition." },
      ],
    },
  },
  {
    relativePath:
      "public-calibration/rwpk.one_off_tool_execution.delivery_package.0012/delivery-recap-deck.pptx",
    spec: {
      kicker: "Delivery package",
      title: "The quarterly handoff is ready",
      subtitle: "A concise recap aligned with the handoff note, tracker, and package manifest.",
      period: "July 31, 2026",
      metricTitle: "All required handoff artifacts are present",
      metricValue: "4 / 4",
      metricLabel: "required package files",
      metricInterpretation: "The archive step remains scheduled for August 3 after final sign-off.",
      chartCategories: ["Recap", "Tracker", "Note", "Manifest"],
      chartValues: [100, 100, 100, 100],
      chartSeriesName: "Completion %",
      actionTitle: "Complete the controlled handoff",
      actions: [
        { title: "Confirm sign-off", detail: "Record the final approver role in the tracker." },
        { title: "Archive package", detail: "Store the four-file bundle after confirmation." },
        { title: "Preserve sources", detail: "Keep the supplied brief and data unchanged." },
      ],
    },
  },
];

for (const deck of decks) {
  await buildDeck(deck.relativePath, deck.spec);
}

await buildExpenseExtractionWorkbook();
await buildStatusWorkbook();
await buildBudgetWorkbooks();
await buildOpsWorkbook();
await buildCampaignSourceWorkbook();
await buildDeliveryTracker();

console.log(`built office assets under ${dataRoot}`);
console.log(`wrote visual QA previews under ${qaRoot}`);
