# Kestrel — Empty On The Map

## Business Problem

Kestrel Beverages' growth team has identified pale districts on its sales map and wants to know whether those areas represent genuine whitespace opportunities.

Low Kestrel sales do not necessarily mean low market demand. A district may be pale because:

- demand for the category is weak,
- Kestrel distribution is weak,
- or panel coverage is insufficient.

The objective is therefore to distinguish genuine expansion opportunities from markets where marketing alone is unlikely to solve the problem.

## Objective

Identify districts that have:

1. Strong independent evidence of category demand.
2. Significant Kestrel distribution whitespace.
3. Manageable competitive intensity.
4. Sufficient panel coverage to support a reliable decision.

The final output provides a ranked WCI shortlist, separately reports UNKNOWN districts, sizes the top five opportunities in ₹, and identifies the appropriate commercial intervention.

## Analytical Approach

The analysis follows this sequence:

Raw Data
→ Data Audit
→ Data Preparation
→ Panel Coverage
→ Independent Demand Signal
→ Distribution Gap
→ Competitive Intensity
→ WCI
→ Target Classification
→ Opportunity Sizing

### Data Audit

The raw datasets were inspected for:

- Missing values
- Exact duplicates
- Potential near-duplicates
- Invalid numeric values
- Date issues
- Inconsistent district identifiers
- Relationship and join issues

Raw datasets were not modified.

### Data Preparation

Working copies were created for preprocessing.

The preparation included:

- Standardising dates
- Normalising district identifiers
- Standardising analytical fields
- Handling invalid numeric values
- Preserving missing values where their meaning could not be safely inferred
- Validating district and district-month relationships

The common analytical grain is district-month.

There are 340 districts and 24 months, giving 8,160 district-month observations.

## Panel Coverage

Panel coverage was evaluated before interpreting retail activity.

The assessment-defined rule is:

**Panel Coverage < 60% → UNKNOWN**

UNKNOWN does not mean zero demand and does not mean rejection.

The analysis found:

- 8,160 district-month observations
- 6,314 observations below 60% coverage
- 77.4% of district-month observations below the threshold
- 257 of 340 districts with mean coverage below 60%

These districts are reported separately.

## Independent Demand Signal

Kestrel's own sales are not used to construct Demand Signal.

Independent demand evidence comes from:

- Category velocity in the retail panel
- Content/social engagement
- Event registrations

This avoids circularity between Kestrel's existing sales and the assessment of market demand.

## WCI Framework

The assessment-defined Whitespace Confidence Index is:

WCI =
0.45 × Demand Signal
+ 0.35 × Distribution Gap
+ 0.20 × (1 − Competitive Intensity)

Where:

**Distribution Gap**

1 − (Outlets Stocking Kestrel / Outlets Stocking Category)

**Competitive Intensity**

Share of category volume held by the top two rivals.

### Recommended Target Conditions

A district is a recommended target only when all three conditions are satisfied:

- WCI ≥ 0.70
- Distribution Gap ≥ 0.40
- Panel Coverage ≥ 60%

## Market-Size Normalisation

Absolute category volume was not used as the sole ranking measure because large districts naturally generate larger volumes.

Market-size normalisation is therefore used so that the ranking reflects relative whitespace rather than simply market size.

## Key Results

The final WCI analysis identifies:

- **25 recommended target districts**
- **257 districts classified as UNKNOWN**
- **7 reliable pale districts explicitly rejected**

The five highest-ranked opportunities are:

1. Dharwad, Karnataka
2. Paschim Bardhaman, West Bengal
3. Warangal, Telangana
4. Ujjain, Madhya Pradesh
5. Vizag, Andhra Pradesh

The top five have high WCI scores and large distribution gaps. The recommended intervention for each is **Both Distribution and Marketing**.

## Opportunity Sizing

The top five opportunities are sized using Kestrel revenue as a commercial baseline.

The annualised top-five baseline is approximately:

**₹52.11M**

This is a sizing baseline and should not be interpreted as guaranteed incremental revenue.

## UNKNOWN vs Rejected

The project deliberately separates:

**UNKNOWN**

Insufficient panel evidence. These districts should not be rejected.

**REJECTED**

Reliable evidence indicates that the whitespace opportunity is not strong enough to prioritise.

This distinction prevents data gaps from being mistaken for weak markets.

## Project Structure

```text
Tail_project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── Notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_preparation.ipynb
│   └── 03_wci_analysis.ipynb
│
├── approach_tried.md
├── assumptions.md
├── README.md
├── requirements.txt
├── memo.pdf
└── presentation.pptx