# Keg Metrics 

Estimate keg usage, waste, and profitability for my mum (her pub).  
Models fixed waste from **line clears/cleans** and probabilistic waste from **foam/spillage** (Monte Carlo).  
Shows expected margin and **probability a keg makes money**.

## Quickstart
```bash
pip install -r requirements.txt
python -m src.kegmetrics.cli
streamlit run app.py
