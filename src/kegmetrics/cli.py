from __future__ import annotations
import argparse
import pandas as pd
from .io import load_config_csv
from .model import compute_table

def main():
    parser = argparse.ArgumentParser(description="Keg metrics CLI")
    parser.add_argument("--config", default="data/sample_config.csv", help="Path to CSV config")
    parser.add_argument("--sims", type=int, default=5000, help="Monte Carlo draws")
    args = parser.parse_args()

    df = load_config_csv(args.config)
    out = compute_table(df, n_sim=args.sims)
    with pd.option_context('display.max_columns', None):
        print(out.round(2).to_string(index=False))

if __name__ == "__main__":
    main()
