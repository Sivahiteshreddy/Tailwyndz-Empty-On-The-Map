# Approach Tried

This file records approaches considered or tested during the Tailwyndz "Empty On The Map" project and why they were not used in the final analysis.

## Approach 1 – Rank districts using raw sales

I initially considered ranking districts directly using observed Kestrel sales from the raw data.

**Why I did not use it:** This would treat observed panel sales as directly comparable across districts even though panel coverage is highly uneven. The panel-coverage audit found that 6,314 of 8,160 district-month observations (77.4%) are below the 60% coverage threshold. Therefore, a low observed sales value may reflect limited panel coverage rather than weak demand.

**Decision:** Dropped. Sales must be interpreted together with panel coverage and market-size information.

---

## Approach 2 – Use raw date values for monthly analysis

I initially considered using the original date fields directly to create monthly analysis.

**Why I did not use it:** The date audit identified mixed and partially unparseable date values. Approximately 92% of records successfully parsed across the audited date fields, leaving a material proportion requiring controlled handling. The Retail Panel also contains future-dated records extending to 2031-11-28.

**Decision:** Dropped. Dates must be parsed and validated during preprocessing before monthly aggregation.

---

## Approach 3 – Join datasets using original district identifiers/names

I initially considered joining datasets using the original district identifiers and names without normalization.

**Why I did not use it:** District identifiers were represented in different formats, including values such as `DST_0001`, `DST-0001`, and numeric representations. Exact matching therefore produced apparent mismatches. After non-destructive normalization, the datasets aligned to the same 340 districts.

**Decision:** Dropped. District identifiers must be standardized in a controlled working representation before cross-dataset joins.

---

## Final Approach

The final analysis will use controlled preprocessing and normalized join keys while preserving the raw datasets. Panel coverage will be evaluated before interpreting sales, and market size and other demand/distribution signals will be incorporated before identifying whitespace opportunities.