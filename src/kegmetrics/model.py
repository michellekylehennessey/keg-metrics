from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass

UK_PINT_LITERS = 0.568

@dataclass
class KegResult:
    beer: str
    expected_pints_sold: float
    expected_revenue: float
    expected_waste_liters: float
    expected_draw_liters: float
    expected_margin_gbp: float
    prob_profit: float
    break_even_pints: float

def _trunc_norm(mean: float, sd: float, low: float = 0.0, high: float = 0.8, size: int = 1, rng=None):
    rng = rng or np.random.default_rng()
    x = rng.normal(mean, sd, size=size)
    return np.clip(x, low, high)

def compute_one_row(row: pd.Series, n_sim: int = 5000, rng=None) -> KegResult:
    rng = rng or np.random.default_rng()
    beer = row["beer"]
    keg_size = float(row["keg_size_liters"])
    cost = float(row["cost_per_keg_gbp"])
    price = float(row["price_per_pint_gbp"])
    avg_pints_sold = float(row["avg_pints_sold_per_keg"])
    line_clear_loss = float(row["line_clear_loss_liters"])
    line_clean_loss = float(row["line_clean_loss_liters"]) * float(row["line_cleans_per_keg"])
    foam_mean = float(row["foam_loss_pct_mean"])
    foam_sd = float(row["foam_loss_pct_sd"])

    sold_volume = avg_pints_sold * UK_PINT_LITERS  # liters sold to customers

    foam_draw_fracs = _trunc_norm(foam_mean, foam_sd, 0.0, 0.8, size=n_sim, rng=rng)
    draw_no_fixed = sold_volume / (1.0 - foam_draw_fracs)
    total_draw = draw_no_fixed + line_clear_loss + line_clean_loss

    # Cap at keg size and proportionally reduce sold if capped
    capped_draw = np.minimum(total_draw, keg_size)
    scale = capped_draw / total_draw
    sold_liters_sim = sold_volume * scale
    pints_sold_sim = sold_liters_sim / UK_PINT_LITERS
    revenue_sim = pints_sold_sim * price
    margin_sim = revenue_sim - cost
    prob_profit = float((margin_sim > 0).mean())

    expected_pints_sold = float(pints_sold_sim.mean())
    expected_revenue = float(revenue_sim.mean())
    expected_margin = float(margin_sim.mean())
    expected_draw = float(capped_draw.mean())
    expected_waste = float(expected_draw - (expected_pints_sold * UK_PINT_LITERS))
    break_even_pints = cost / price  # ignores waste; quick yardstick

    return KegResult(
        beer=beer,
        expected_pints_sold=expected_pints_sold,
        expected_revenue=expected_revenue,
        expected_waste_liters=expected_waste,
        expected_draw_liters=expected_draw,
        expected_margin_gbp=expected_margin,
        prob_profit=prob_profit,
        break_even_pints=break_even_pints,
    )

def compute_table(df: pd.DataFrame, n_sim: int = 5000, seed: int | None = 123) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    results = [compute_one_row(row, n_sim=n_sim, rng=rng) for _, row in df.iterrows()]
    out = pd.DataFrame([r.__dict__ for r in results])
    return out.sort_values("expected_margin_gbp", ascending=True).reset_index(drop=True)
