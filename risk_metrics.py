"""
risk_metrics.py
===============
Concepts covered: 33-37
风险与收益指标计算模块

涵盖:
  - 标准差（波动率）
  - 年化收益率
  - 年化波动率
  - 原始夏普比率
  - 无风险利率说明
"""

import numpy as np
import pandas as pd


# ──────────────────────────────────────────────
# Concept 33 - Standard Deviation (Volatility)
# ──────────────────────────────────────────────
def calc_volatility(returns: pd.DataFrame) -> pd.Series:
    """
    计算各资产的月度波动率（标准差）。

    σ = √Variance
    """
    return returns.std()


# ──────────────────────────────────────────────
# Concept 34 - Annualized Return
# ──────────────────────────────────────────────
def annualize_return(
    returns: pd.DataFrame,
    periods_per_year: int = 12,
) -> pd.Series:
    """
    将月度收益率序列年化。

    公式：compound_growth ^ (periods_per_year / n_periods) - 1

    原理：已知全量复合增长，反推等效年化率。
    """
    compound_growth = (1 + returns).prod()
    n_periods = returns.shape[0]
    return compound_growth ** (periods_per_year / n_periods) - 1


# ──────────────────────────────────────────────
# Concept 35 - Annualized Volatility
# ──────────────────────────────────────────────
def annualize_vol(
    returns: pd.DataFrame,
    periods_per_year: int = 12,
) -> pd.Series:
    """
    将月度波动率年化。

    公式：σ_monthly × √periods_per_year

    原理：方差与时间成线性比例，标准差因此与 √time 成比例。
    """
    return returns.std() * np.sqrt(periods_per_year)


# ──────────────────────────────────────────────
# Concept 36 - Raw Sharpe Ratio
# ──────────────────────────────────────────────
def raw_sharpe(
    returns: pd.DataFrame,
    periods_per_year: int = 12,
) -> pd.Series:
    """
    原始夏普比率（不扣除无风险利率）：
        Sharpe_raw = 年化收益率 / 年化波动率

    评级参考：
      < 0.5   → 偏弱
      0.5-1.0 → 股票均值水平
      > 1.0   → 强劲
      > 2.0   → 顶级水平
    """
    ann_ret = annualize_return(returns, periods_per_year)
    ann_vol = annualize_vol(returns, periods_per_year)
    return ann_ret / ann_vol


# ──────────────────────────────────────────────
# Concept 37 - Risk-Free Rate (placeholder)
# ──────────────────────────────────────────────
def adjusted_sharpe(
    returns: pd.DataFrame,
    rf_rate: float = 0.05,
    periods_per_year: int = 12,
) -> pd.Series:
    """
    真实夏普比率，扣除年化无风险利率（如当前美联储基准利率）：
        Sharpe = (R_portfolio - R_f) / σ_portfolio

    Parameters
    ----------
    rf_rate : 年化无风险利率，默认 5%（对应近期 T-Bill 水平）
    """
    ann_ret = annualize_return(returns, periods_per_year)
    ann_vol = annualize_vol(returns, periods_per_year)
    return (ann_ret - rf_rate) / ann_vol


# ──────────────────────────────────────────────
# Consolidated Summary
# ──────────────────────────────────────────────
def risk_return_summary(
    returns: pd.DataFrame,
    periods_per_year: int = 12,
    rf_rate: float = 0.05,
) -> pd.DataFrame:
    """
    输出一份完整的风险收益汇总 DataFrame，包含：
      - 年化收益率
      - 年化波动率
      - 原始夏普
      - 调整后夏普
    """
    summary = pd.DataFrame({
        "Ann. Return (%)":    (annualize_return(returns, periods_per_year) * 100).round(2),
        "Ann. Volatility (%)": (annualize_vol(returns, periods_per_year) * 100).round(2),
        "Raw Sharpe":         raw_sharpe(returns, periods_per_year).round(3),
        f"Sharpe (rf={rf_rate:.0%})": adjusted_sharpe(returns, rf_rate, periods_per_year).round(3),
    })
    return summary


def print_risk_summary(returns: pd.DataFrame, rf_rate: float = 0.05) -> None:
    """打印格式化的风险指标汇总。"""
    summary = risk_return_summary(returns, rf_rate=rf_rate)
    print("\n" + "=" * 60)
    print("  RISK & RETURN METRICS")
    print("=" * 60)
    print(summary.to_string())
    print("\n夏普比率解读:")
    print("  < 0.5  = 偏弱  |  0.5-1.0 = 均值  |  >1.0 = 强劲  |  >2.0 = 顶级")
    print("=" * 60)
