# Approach Tried

This file records the methods I considered during the Tailwyndz "Empty On The Map" project and why I did not use them.

## Approach 1 – Rank districts using raw data

I first thought of ranking districts directly from the raw datasets.

**Why I did not use it:** The raw data had different district names, mixed date formats, and panel coverage issues. The ranking would not be reliable.

## Approach 2 – Use raw dates for monthly analysis

I tried using the original date values for monthly analysis.

**Why I did not use it:** The datasets had different date formats, so the monthly comparison was not consistent.

## Approach 3 – Join datasets using original district names

I tried joining the datasets using the original district names.

**Why I did not use it:** Different spellings of district names caused failed joins, so I standardized the district names before merging the datasets.
