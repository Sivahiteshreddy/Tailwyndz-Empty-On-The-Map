# Approach Tried

This document records analytical approaches considered during the Tailwyndz "Empty On The Map" project and explains why the final approach was selected.

---

## 1. Rank districts using raw Kestrel sales

**Approach considered:** Rank districts directly using observed Kestrel sales.

**Why rejected:** Observed sales are affected by uneven panel coverage. The panel-coverage analysis found 6,314 of 8,160 district-month observations (77.4%) below the 60% coverage threshold. Low observed sales therefore cannot automatically be interpreted as weak demand.

**Decision:** Rejected. Kestrel sales are used for commercial context and opportunity sizing, but not as the independent demand signal.

---

## 2. Treat low panel coverage as zero demand

**Approach considered:** Interpret districts with low panel coverage as low- or zero-demand markets.

**Why rejected:** A weak panel can make observed activity appear artificially low. The assessment requires districts below 60% panel coverage to be classified as UNKNOWN.

**Decision:** Rejected. Low coverage represents insufficient evidence, not zero demand.

---

## 3. Join datasets using original district identifiers

**Approach considered:** Join datasets using district IDs exactly as supplied.

**Why rejected:** District identifiers were represented inconsistently, including formats such as `DST_0001`, `DST-0001`, and numeric representations.

**Decision:** Rejected. District identifiers were normalized to a canonical representation before cross-dataset joins.

---

## 4. Use Kestrel sales in the independent Demand Signal

**Approach considered:** Include Kestrel sales as an input to the demand score.

**Why rejected:** The assessment requires an independent demand signal. Including Kestrel's own sales would introduce circularity because existing Kestrel performance would become evidence of external demand.

**Decision:** Rejected. The Demand Signal is based on independent category/audience/event evidence.

---

## 5. Rank districts by absolute category volume

**Approach considered:** Rank districts using absolute category volume.

**Why rejected:** Large districts naturally generate larger absolute volumes. This would favor market size rather than identifying genuine relative whitespace.

**Decision:** Rejected. Market-size normalization is required so the ranking reflects whitespace rather than simply the largest markets.

---

## 6. Treat missing discounts as zero

**Approach considered:** Convert missing discount values to 0%.

**Why rejected:** A missing value does not prove that no discount existed.

**Decision:** Rejected. Missing discounts remain missing unless a later analysis provides a justified treatment.

---

## 7. Impute missing projection weights immediately

**Approach considered:** Fill missing projection weights before analysis.

**Why rejected:** An appropriate weighting methodology had not been established. Arbitrary imputation could distort projected audience or demand measures.

**Decision:** Rejected. Missing weights are retained for explicit handling where required.

---

## 8. Remove every repeated business key

**Approach considered:** Remove all repeated District/SKU/Month or District/User/Event combinations.

**Why rejected:** Repeated business keys can represent legitimate repeated observations. Business-key repetition alone is insufficient evidence of duplication.

**Decision:** Rejected. Exact duplicates and near-duplicates were investigated separately.

---

## 9. Calculate WCI before validating coverage and joins

**Approach considered:** Begin WCI calculations immediately after basic preprocessing.

**Why rejected:** WCI depends on correctly aligned district/month data and reliable panel evidence.

**Decision:** Rejected. District/month joins and panel coverage were validated before WCI construction.

---

# Final Approach

The final approach follows this sequence:

1. Audit the raw datasets without modifying them.
2. Create controlled working copies for preprocessing.
3. Standardize dates, categorical fields, and district identifiers.
4. Validate district and district-month relationships.
5. Save validated processed datasets separately from the raw data.
6. Quantify 24-month panel coverage.
7. Classify districts below 60% panel coverage as UNKNOWN.
8. Construct an independent Demand Signal without Kestrel sales.
9. Calculate Distribution Gap from Kestrel versus category stocking.
10. Calculate Competitive Intensity from the top two competitors.
11. Apply the assessment-specified WCI formula:
   
   `WCI = 0.45 × Demand Signal + 0.35 × Distribution Gap + 0.20 × (1 − Competitive Intensity)`
   
12. Rank all 340 districts.
13. Apply the assessment recommendation conditions:
   
   - WCI ≥ 0.70
   - Distribution Gap ≥ 0.40
   - Panel Coverage ≥ 60%
   
14. Keep UNKNOWN districts separate from recommended expansion targets.
15. Size the top five recommended opportunities in ₹.
16. Classify each top opportunity as requiring Distribution, Marketing, or Both.
17. Explicitly identify pale districts that should not receive expansion priority.