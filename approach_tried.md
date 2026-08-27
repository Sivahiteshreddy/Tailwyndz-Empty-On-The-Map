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

## Approach 4 – Treat missing discount as zero

I considered treating missing discount values as 0%.

**Why I did not use it:** A missing discount does not prove that no discount existed. The missing values are therefore retained as missing.

## Approach 5 – Impute missing projection weights immediately

I considered filling missing projection weights before analysis.

**Why I did not use it:** The appropriate weighting methodology had not yet been established, so arbitrary imputation could distort the analysis.

## Approach 6 – Remove all near-duplicate business keys

I considered removing every repeated District/SKU/Month or District/User/Event combination.

**Why I did not use it:** Repeated business keys can represent legitimate repeated observations. Timestamp proximity was therefore investigated separately, and no confirmed true near-duplicate pairs were found.

## Approach 7 – Join datasets using original district IDs

I considered joining datasets using the IDs exactly as originally stored.

**Why I did not use it:** District identifiers were represented inconsistently across datasets. IDs were normalized before joining.

## Approach 8 – Treat unmatched Kestrel keys as missing sales

I considered treating Kestrel combinations that do not match Retail Panel as zero or missing sales.

**Why I did not use it:** The unmatched Kestrel combinations represent a join-coverage issue, not proof of zero sales. The 82.41% match rate is therefore retained as a documented limitation.

## Approach 9 – Use Kestrel sales as part of the demand signal

I considered using Kestrel's own sales history as an indicator of demand.

**Why I did not use it:** The assessment explicitly requires the demand signal to be independent of Kestrel's own sales.

## Approach 10 – Rank districts by absolute sales/volume

I considered ranking districts directly by absolute volume.

**Why I did not use it:** This would favor large markets and would not distinguish market size from genuine whitespace opportunity. The assessment requires normalization for market size.

## Approach 11 – Treat low panel coverage as zero demand

I considered treating districts with weak panel coverage as having weak or zero demand.

**Why I did not use it:** Panel gaps can look like zero demand. Districts below 60% panel coverage must therefore be reported as UNKNOWN.

## Approach 12 – Calculate WCI before validating joins and panel coverage

I considered beginning WCI calculations immediately after basic cleaning.

**Why I did not use it:** WCI depends on correctly aligned district/month data and reliable panel coverage. Join-key validation and panel-coverage validation were completed first.