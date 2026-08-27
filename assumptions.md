# Assumptions

This file records the assumptions used during the Tailwyndz "Empty On The Map" project and the potential impact if those assumptions are incorrect.

## Current Assumptions

### 1. Raw datasets remain unchanged

**Assumption:** Raw datasets are treated as immutable source data throughout the project.

**Why:** This preserves traceability and allows all preprocessing decisions to be reproduced.

**What breaks if wrong:** If raw data is overwritten, it becomes difficult to reproduce or audit preprocessing decisions.

---

### 2. Cleaning is performed on working copies

**Assumption:** Data cleaning, normalization, and transformation are performed on working representations rather than modifying raw files.

**Why:** Phase 1 is an audit of the raw data; cleaning belongs to the preprocessing phase.

**What breaks if wrong:** Raw-data lineage and reproducibility would be compromised.

---

### 3. District identifiers can be normalized safely

**Assumption:** Different district-ID representations refer to the same underlying districts when their normalized identifiers match.

**Evidence:** Original representations include formats such as `DST_0001`, `DST-0001`, and numeric IDs. After controlled normalization, the datasets align to 340 districts.

**What breaks if wrong:** Incorrect normalization could create false joins or combine different districts, which would distort district-level analysis.

---

### 4. District-month is the primary analytical grain

**Assumption:** District-month is an appropriate common grain for combining the major analytical datasets.

**Evidence:** The relationship audit identified 8,160 aligned district-month combinations across the analytical datasets.

**What breaks if wrong:** Incorrect temporal or geographic aggregation could create duplicated observations or misleading district-level metrics.

---

### 5. Date fields require controlled parsing and validation

**Assumption:** Mixed date representations can be converted into a common datetime representation during preprocessing.

**Evidence:** Approximately 92% of records successfully parsed across the audited date fields, while a material proportion contained unparseable values. The Retail Panel also contains future-dated records extending to 2031-11-28.

**What breaks if wrong:** Invalid or future dates could distort monthly aggregation, trends, and historical comparisons.

---

### 6. Panel data represents a sample, not a complete market census

**Assumption:** Observed panel sales should not automatically be treated as the complete district market.

**Evidence:** 6,314 of 8,160 district-month observations (77.4%) have panel coverage below 60%. At the district level, 257 of 340 districts have mean panel coverage below 60%.

**What breaks if wrong:** Treating low panel sales as zero demand could incorrectly classify districts as whitespace opportunities.

---

### 7. Low panel coverage represents uncertainty, not zero demand

**Assumption:** Districts below the required panel-coverage threshold should not be interpreted as having zero demand.

**Why:** Poor panel coverage can make actual sales appear artificially low.

**What breaks if wrong:** The WCI ranking could prioritize data gaps instead of genuine commercial opportunities.

---

### 8. Exact duplicate rows require investigation before removal

**Assumption:** Exact duplicate rows are not automatically treated as errors during Phase 1.

**Evidence:** Exact duplicates were identified in several datasets, including 27,746 in the Retail Panel, 7,645 in Audience, 979 in Kestrel Sales, and 816 in Competitor.

**What breaks if wrong:** Automatically deleting duplicates could remove legitimate repeated observations or distort volume-based measures.

---

### 9. Kestrel sales are excluded from the independent demand signal

**Assumption:** The demand signal should represent category demand independently of Kestrel's own sales.

**Why:** Including Kestrel sales would make the demand signal circular and could make Kestrel's existing presence appear as evidence of external demand.

**What breaks if wrong:** The WCI could overstate opportunity in districts where Kestrel already has meaningful sales.

---

### 10. New assumptions will be documented

Any additional assumptions introduced during preprocessing, WCI construction, or opportunity sizing will be added to this file together with their potential impact.

---

### 11. Near-duplicate records require stronger evidence before removal

**Assumption:** Repeated business keys alone are not sufficient evidence that records are duplicates.

**Evidence:** A timestamp-proximity audit was performed using business identity keys and a 10-second threshold. No confirmed true near-duplicate pairs were found.

**What breaks if wrong:** Removing legitimate repeated events could distort event counts, sales measures, or engagement measures.

---

### 12. Invalid numeric values are handled explicitly

**Assumption:** Values that violate known business/data constraints are treated as invalid and handled during preprocessing.

**Evidence:** Negative Retail Panel unit prices and impossible Audience ages (<5 or >110) were converted to missing values. No invalid negative prices or invalid ages remained after validation.

**What breaks if wrong:** Impossible values could distort averages, ratios, distributions, and downstream WCI components.

---

### 13. Missing discount values are not automatically interpreted as zero

**Assumption:** A missing discount value does not prove that no discount existed.

**Treatment:** Missing discount values are retained as missing unless a later analysis requires an explicitly justified treatment.

**What breaks if wrong:** Converting missing discounts to 0% could bias price and discount analysis.

---

### 14. Missing projection weights are not arbitrarily imputed

**Assumption:** Missing projection weights should not be filled with arbitrary values before the appropriate weighting methodology is established.

**Treatment:** Missing weights are retained for explicit handling in the relevant analysis.

**What breaks if wrong:** Arbitrary imputation could distort projected audience or demand estimates.

---

### 15. District Master is the reference for district standardization

**Assumption:** District IDs and district names are standardized against the District Master before cross-dataset joins.

**Evidence:** Retail Panel, Competitor, Audience, and Kestrel each resolve to 340 normalized districts with standardized district names.

**What breaks if wrong:** Incorrect district mapping could transfer sales, demand, competition, or coverage information between districts.

---

### 16. Join keys must be validated before WCI construction

**Assumption:** WCI calculations should only begin after the relevant district, month, and analytical join keys have been validated.

**Evidence:** Audience ↔ Retail Panel, Competitor ↔ Retail Panel, Kestrel ↔ Competitor, and Panel Coverage ↔ Retail Panel achieved 100% district-month match rates after normalization.

**What breaks if wrong:** Misaligned joins could duplicate observations or assign information to the wrong district/month.

---

### 17. Kestrel District × SKU × Month coverage is not assumed to be complete

**Assumption:** Unmatched Kestrel District × SKU × Month combinations are treated as a documented join-coverage issue rather than automatically interpreted as zero sales or deleted.

**Evidence:** 40,348 of 48,960 unique Kestrel District × SKU × Month keys matched Retail Panel, giving an 82.41% match rate.

**What breaks if wrong:** Treating unmatched combinations as zero could create artificial distribution gaps or distort Kestrel-related analysis.

---

### 18. Kestrel sales are excluded from the independent demand signal

**Assumption:** Kestrel's own sales are not used to construct the WCI demand signal.

**Why:** Including Kestrel sales would make the demand signal circular and could make existing Kestrel presence appear as evidence of external demand.

**What breaks if wrong:** The WCI could overstate opportunity in districts where Kestrel already has meaningful sales.

---

### 19. Demand signal uses independent demand evidence

**Assumption:** The WCI demand signal uses the assessment-defined independent sources: category velocity, content/social engagement, and event registrations.

**What breaks if wrong:** Using Kestrel sales or another non-independent signal could introduce circularity into the opportunity score.

---

### 20. Low panel coverage is treated as uncertainty

**Assumption:** Districts with panel coverage below 60% are treated as UNKNOWN rather than as confirmed whitespace opportunities.

**Why:** Low panel coverage can make observed activity appear artificially weak.

**What breaks if wrong:** WCI could prioritize data gaps instead of genuine commercial opportunities.

---

### 21. WCI formula and thresholds follow the assessment

**Assumption:** The prescribed WCI weights and recommendation thresholds are used without changing them.

**Treatment:** Recommended targets require WCI ≥ 0.70, Distribution Gap ≥ 0.40, and Panel Coverage ≥ 60%.

**What breaks if wrong:** Changing the weights or thresholds would make the analysis inconsistent with the assessment specification.

---

### 22. Market-size normalization is required

**Assumption:** Opportunity measures are normalized for market size rather than relying only on absolute volume.

**Why:** Larger districts naturally generate more absolute activity; normalization helps identify genuine whitespace rather than simply the largest markets.

**What breaks if wrong:** The shortlist could be dominated by large districts even when their relative whitespace is weak.

---

### 23. Distribution quality issues are explicitly flagged

**Assumption:** Impossible distribution values are identified and documented before WCI interpretation.

**Evidence:** The Distribution audit identified 159 rows with at least one impossible condition, while the percentage consistency checks showed zero calculation mismatches.

**Treatment:** These issues remain explicitly documented for WCI analysis rather than being silently treated as valid business observations.

**What breaks if wrong:** Invalid outlet counts could distort distribution-gap calculations.

---

### 24. Processed datasets are separate from WCI outputs

**Assumption:** Validated processed datasets form a stable preprocessing layer, while WCI calculations and opportunity outputs are created separately.

**Why:** This preserves a clear boundary between data preparation and analytical results.

**What breaks if wrong:** Analytical transformations could overwrite the validated input layer and make the analysis difficult to reproduce.