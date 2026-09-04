# Assumptions

This document records the assumptions used in the Tailwyndz "Empty On The Map" analysis and what could happen if each assumption is incorrect.

---

## 1. Raw datasets are immutable

**Assumption:** Raw source datasets remain unchanged throughout the project.

**Why:** This preserves traceability and reproducibility.

**What breaks if wrong:** Preprocessing decisions cannot be reliably audited or reproduced.

---

## 2. Cleaning is performed on working copies

**Assumption:** Cleaning and transformations are applied to working/processed datasets rather than raw files.

**Why:** Raw-data audit and analytical preparation need to remain separate.

**What breaks if wrong:** Data lineage and reproducibility become difficult to establish.

---

## 3. District identifiers can be safely normalized

**Assumption:** Different representations such as `DST_0001`, `DST-0001`, and numeric IDs can be mapped to the same canonical district when their normalized identifiers agree.

**Evidence:** After normalization, the analytical datasets align to the same 340 District Master districts.

**What breaks if wrong:** Incorrect normalization could create false joins or combine different districts.

---

## 4. District-month is the common analytical grain

**Assumption:** District-month is an appropriate common grain for combining the major analytical datasets.

**Evidence:** The datasets align to 340 districts × 24 months = 8,160 district-month combinations.

**What breaks if wrong:** Incorrect aggregation could create duplication or misleading district-level metrics.

---

## 5. Panel data is a sample rather than a complete census

**Assumption:** Panel observations should not automatically be treated as the complete retail market.

**Evidence:** 6,314 of 8,160 district-month observations (77.4%) are below the 60% panel-coverage threshold.

**What breaks if wrong:** Low observed sales could be incorrectly interpreted as weak market demand.

---

## 6. Panel coverage below 60% means UNKNOWN

**Assumption:** Districts below 60% panel coverage have insufficient evidence for reliable whitespace interpretation.

**Treatment:** These districts are classified as UNKNOWN rather than zero-demand or rejected markets.

**Evidence:** 257 of 340 districts have mean panel coverage below 60%.

**What breaks if wrong:** The analysis could mistake data blindness for genuine whitespace.

---

## 7. Dates can be standardized during preprocessing

**Assumption:** Mixed source date representations can be converted into a common datetime representation.

**Treatment:** Date fields are parsed and validated during preprocessing.

**What breaks if wrong:** Incorrect dates could distort monthly aggregation and time-based analysis.

---

## 8. Exact duplicates require investigation

**Assumption:** Exact duplicate rows should be investigated before removal rather than automatically assumed to be errors.

**Why:** Some repeated records can represent legitimate observations.

**What breaks if wrong:** Removing legitimate records could distort volume, revenue, or engagement measures.

---

## 9. Near-duplicate business keys are not automatically errors

**Assumption:** Repeated business keys alone do not prove that observations are duplicates.

**Treatment:** Near-duplicate logic requires additional evidence such as timestamp proximity and business identity.

**What breaks if wrong:** Legitimate repeated events or transactions could be removed.

---

## 10. Invalid numeric values require explicit handling

**Assumption:** Values that violate known business constraints are treated as invalid during preprocessing.

**Examples:** Negative retail unit prices and impossible audience ages.

**What breaks if wrong:** Invalid values could distort averages, ratios, and downstream scores.

---

## 11. Missing discounts do not equal zero

**Assumption:** A missing discount value does not prove that no discount existed.

**Treatment:** Missing discount values are retained as missing unless a justified analytical treatment is established.

**What breaks if wrong:** Treating all missing discounts as zero could bias pricing analysis.

---

## 12. Missing projection weights are not arbitrarily imputed

**Assumption:** Missing projection weights should not be filled with arbitrary values.

**Why:** The correct weighting methodology must be justified before imputation.

**What breaks if wrong:** Audience or demand estimates could be systematically distorted.

---

## 13. District Master is the geographic reference

**Assumption:** District Master provides the canonical district identifier and standardized district name/state information.

**Why:** It provides a consistent geographic reference for joins and reporting.

**What breaks if wrong:** Sales, demand, competition, or coverage information could be assigned to the wrong district.

---

## 14. Joins must be validated before WCI construction

**Assumption:** Analytical joins are valid only after district and district-month key validation.

**Evidence:** After normalization, the relevant district and district-month relationships were validated across the analytical datasets.

**What breaks if wrong:** Incorrect joins could duplicate observations or assign information to the wrong market.

---

## 15. Kestrel sales are excluded from the independent Demand Signal

**Assumption:** Kestrel's own sales are not used to construct Demand Signal.

**Why:** The assessment requires independent demand evidence.

**What breaks if wrong:** The WCI could become circular and overstate opportunity where Kestrel already performs well.

---

## 16. Demand Signal represents independent demand evidence

**Assumption:** Demand Signal uses independent category/audience/event evidence rather than Kestrel's own sales.

**Why:** This separates underlying market demand from Kestrel's existing commercial performance.

**What breaks if wrong:** Existing Kestrel presence could be mistaken for external market demand.

---

## 17. Distribution Gap measures relative whitespace

**Assumption:** Distribution Gap is interpreted as the gap between Kestrel distribution and category distribution.

**Formula:**

`Distribution Gap = 1 − (Kestrel stocking outlets / Category stocking outlets)`

**What breaks if wrong:** Distribution opportunity could be overstated or understated.

---

## 18. Competitive Intensity reflects the top two rivals

**Assumption:** Competitive Intensity represents the share of category volume held by the top two competitors.

**Why:** This follows the assessment definition.

**What breaks if wrong:** Markets with strong competitive lockout could be incorrectly interpreted as open whitespace.

---

## 19. WCI weights and recommendation thresholds follow the assessment

**Assumption:** The prescribed WCI formula and recommendation thresholds are used without changing them.

**Formula:**

`WCI = 0.45 × Demand Signal + 0.35 × Distribution Gap + 0.20 × (1 − Competitive Intensity)`

**Recommended Target conditions:**

- WCI ≥ 0.70
- Distribution Gap ≥ 0.40
- Panel Coverage ≥ 60%

**What breaks if wrong:** Changing the weights or thresholds would make the analysis inconsistent with the assessment.

---

## 20. Market-size normalization is necessary

**Assumption:** Demand/opportunity interpretation must account for market size rather than relying only on absolute volume.

**Why:** Large districts naturally generate larger absolute activity.

**What breaks if wrong:** The shortlist could become dominated by the largest districts rather than genuine whitespace.

---

## 21. Kestrel revenue is used for commercial sizing, not independent demand

**Assumption:** Kestrel revenue may be used separately for commercial opportunity sizing and context, while remaining excluded from Demand Signal.

**Why:** Existing Kestrel performance is useful for quantifying commercial scale but should not contaminate the independent demand measure.

**What breaks if wrong:** Mixing these purposes could introduce circularity into the WCI.

---

## 22. Top-five ₹ sizing is a commercial estimate

**Assumption:** The top-five ₹ figure is presented as a commercial sizing/baseline and not as a guaranteed incremental revenue forecast unless an explicit uplift methodology is justified.

**Why:** The assessment requires ₹ sizing but does not prescribe a single incremental-revenue formula.

**What breaks if wrong:** Presenting baseline revenue as guaranteed incremental opportunity would overstate the business case.

---

## 23. Intervention recommendations are diagnostic

**Assumption:** Distribution, Marketing, or Both recommendations are based on the observed Demand Signal and Distribution Gap.

**Interpretation:**
- Strong demand + large distribution gap → Both
- Large distribution gap without strong demand → Distribution
- Strong demand without large distribution gap → Marketing

**What breaks if wrong:** The intervention could address the wrong commercial constraint.

---

## 24. Pale districts are not automatically rejected because of low sales alone

**Assumption:** A pale district should be rejected only when the available evidence indicates insufficient whitespace opportunity, rather than simply because its Kestrel sales are low.

**Why:** Low sales can result from weak demand, poor distribution, competition, or insufficient evidence.

**What breaks if wrong:** Genuine whitespace could be incorrectly rejected.

---

## 25. UNKNOWN districts are not rejection markets

**Assumption:** Districts below 60% panel coverage remain UNKNOWN rather than being labelled poor or rejected.

**Why:** Insufficient evidence is different from evidence of weak opportunity.

**What breaks if wrong:** Data gaps could be mistaken for weak commercial potential.

---

## 26. Processed datasets and analytical outputs remain separate

**Assumption:** Processed datasets provide the stable analytical input layer, while WCI and recommendation outputs are generated separately.

**Why:** This preserves reproducibility and makes the analytical pipeline easier to audit.

**What breaks if wrong:** Analytical transformations could overwrite the validated input layer.

---

## 27. Additional assumptions must be documented

Any new assumption introduced during opportunity sizing, recommendation classification, memo preparation, or presentation development will be added here with its potential impact.