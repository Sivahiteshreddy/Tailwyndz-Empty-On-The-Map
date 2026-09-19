# Kestrel — Empty On The Map Dashboard V4

This is the Streamlit dashboard companion for the Kestrel market-expansion assessment.

## V4 additions
- India Opportunity Map using state-level visual anchors with district decision details on hover.
- Opportunity Shortlist page with all recommended districts.
- Sortable/filterable-style decision table for WCI, demand, distribution gap and panel coverage.
- “Why this district?” panel for explaining one selected target.
- Evidence-gate table for decision review.
- Commercial sizing shown separately from WCI.
- Existing Executive Overview, District Explorer, Decision Logic and Audit & Evidence retained.

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

Upload the project's full `wci_complete_analysis.csv` from the sidebar to use the complete 340-district analysis.

### Map note
The map intentionally uses state-level visual anchors rather than potentially mismatched district polygons. The 340-district decision remains district-level.
