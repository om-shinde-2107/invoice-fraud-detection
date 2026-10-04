import pandas as pd
import streamlit as st

st.set_page_config(page_title="Invoice Matching & Fraud Review", layout="wide")
st.title("Invoice Matching and Fraud Detection")
st.caption("Educational prototype: flags indicate records for review, not confirmed fraud.")

required = ["invoice_id", "vendor", "po_id", "invoice_amount", "po_amount"]
upload = st.file_uploader("Upload invoice/PO comparison CSV", type="csv")
if upload:
    df = pd.read_csv(upload)
else:
    df = pd.read_csv("data/sample_invoices.csv")

missing = [c for c in required if c not in df.columns]
if missing:
    st.error("CSV is missing required columns: " + ", ".join(missing))
    st.stop()

for c in ["invoice_amount", "po_amount"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
tolerance = st.number_input("Amount tolerance", min_value=0.0, value=1.0, step=1.0)
df["difference"] = (df["invoice_amount"] - df["po_amount"]).round(2)
def assess(row):
    flags = []
    if not str(row["po_id"]).strip() or row["po_amount"] == 0:
        flags.append("Missing PO")
    if abs(row["difference"]) > tolerance:
        flags.append("Amount mismatch")
    if not str(row["vendor"]).strip():
        flags.append("Missing vendor")
    return "; ".join(flags) if flags else "Matched"
df["result"] = df.apply(assess, axis=1)
df["status"] = df["result"].map(lambda x: "REVIEW" if x != "Matched" else "MATCHED")
a, b, c = st.columns(3)
a.metric("Invoices", len(df))
b.metric("Matched", int((df.status == "MATCHED").sum()))
c.metric("Needs review", int((df.status == "REVIEW").sum()))
st.dataframe(df, use_container_width=True)
st.download_button("Download results CSV", df.to_csv(index=False).encode("utf-8"), "invoice_review_results.csv", "text/csv")
st.info("A review flag is only a prompt for human checking; it does not prove fraud.")
