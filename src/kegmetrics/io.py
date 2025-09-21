from __future__ import annotations
import pandas as pd

REQUIRED_COLS = [
    "beer",
    "keg_size_liters",
    "cost_per_keg_gbp",
    "price_per_pint_gbp",
    "avg_pints_sold_per_keg",
    "line_clear_loss_liters",
    "line_clean_loss_liters",
    "line_cleans_per_keg",
    "foam_loss_pct_mean",
    "foam_loss_pct_sd",
]

def load_config_csv(path_or_buffer) -> pd.DataFrame:
    df = pd.read_csv(path_or_buffer)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df
