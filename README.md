# Invoice Matching and Fraud Detection

A small educational Streamlit prototype that compares invoice amounts with purchase-order amounts and highlights records needing review. It uses sample data and simple rules; a flag means investigate, not confirmed fraud.

## Run on Windows

1. Install Python 3.10 or newer.
2. Open PowerShell in this folder.
3. Run:

   py -m pip install -r requirements.txt
   py -m streamlit run app.py

4. Open the local address Streamlit prints (usually http://localhost:8501).

Upload a CSV with columns `invoice_id`, `vendor`, `po_id`, `invoice_amount`, and `po_amount`, or use the included sample data.

This app is not publicly deployed. See `LIVE_LINK.txt`.
