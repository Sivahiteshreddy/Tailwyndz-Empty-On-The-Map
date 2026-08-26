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