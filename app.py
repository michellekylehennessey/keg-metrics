import streamlit as st
from src.kegmetrics.io import load_config_csv, REQUIRED_COLS
from src.kegmetrics.model import compute_table

st.set_page_config(page_title="Keg Metrics", layout="wide")
st.title("🍺 Keg Metrics: usage, waste & profitability")

st.markdown("""Upload a CSV in the required format (see sidebar for template).  
Then view expected margin, waste, and probability of profit per keg.
""")

with st.sidebar:
    st.header("Data template")
    st.code(",".join(REQUIRED_COLS), language="text")
    st.markdown("You can start from `data/sample_config.csv`.")

uploaded = st.file_uploader("Upload beer config CSV", type=["csv"])

if uploaded is None:
    st.info("Using bundled sample data…")
    df = load_config_csv("data/sample_config.csv")
else:
    df = load_config_csv(uploaded)

sims = st.slider("Monte Carlo simulations", 1000, 20000, 5000, step=1000)
out = compute_table(df, n_sim=sims)
st.subheader("Per-beer results")
st.dataframe(out.round(3))

st.subheader("Notes")
st.markdown("""
- A UK pint is taken as 0.568L.  
- Foam loss is modeled as a truncated normal on [0, 0.8].  
- Break-even pints ignores waste (fast sanity check).  
- If draw exceeds the keg size, sold pints are scaled down proportionally.
""")
