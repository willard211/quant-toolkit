"""
returns.py
==========
Concepts covered: 14-22
收益率计算模块

涵盖:
  - 标准收益率公式
  - 1+R 格式
  - 多期复合收益（几何链接）
  - 方差拖曳 (Variance Drag) 演示
  - pct_change / dropna
  - 收益率序列图
  - .prod() 全量复合
  - 格式化输出
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ──────────────────────────────────────────────
# Concept 14 - Standard Return Formula
# ──────────────────────────────────────────────
def single_period_return(p_initial: float, p_final: float) -> float:
    """
    标准单期收益率：(P_final - P_initial) / P_initial
    """
    return (p_final - p_initial) / p_initial


# ──────────────────────────────────────────────
# Concept 15 - 1+R Format
# ──────────────────────────────────────────────
def one_plus_r(p_initial: float, p_final: float) -> float:
    """
    1+R 格式：p_final / p_initial  （减 1 即得收益率）
    """
    return p_final / p_initial - 1


# ──────────────────────────────────────────────
# Concept 16 - Multi-Period Compound Return
# ──────────────────────────────────────────────
def compound_return(period_returns: list[float]) -> float:
    """
    多期几何复合收益率：∏(1+r) - 1
    """
    result = 1.0
    for r in period_returns:
        result *= (1 + r)
    return result - 1


# ──────────────────────────────────────────────
# Concept 17 - Variance Drag Demonstration
# ──────────────────────────────────────────────
def demonstrate_variance_drag(
    initial: float = 100.0,
    gain: float = 0.30,
    loss: float = 0.30,
    print_result: bool = True,
) -> dict:
    """
    演示方差拖曳现象：均值为 0% 但实际回报为负。

    方差拖曳近似 = σ/2
    """
    after_gain = initial * (1 + gain)
    after_loss = after_gain * (1 - loss)
    arithmetic_avg = (gain + (-loss)) / 2
    actual_return = (after_loss / initial) - 1
    # 理论拖曳量 ≈ σ/2，这里 σ 用两期收益率的标准差近似
    sigma = np.std([gain, -loss])
    theoretical_drag = -(sigma ** 2) / 2

    result = {
        "initial": initial,
        "after_gain": after_gain,
        "after_loss": after_loss,
        "arithmetic_avg": arithmetic_avg,
        "actual_return": actual_return,
        "theoretical_drag_approx": theoretical_drag,
    }

    if print_result:
        print("─" * 45)
        print("   VARIANCE DRAG DEMONSTRATION")
        print("─" * 45)
        print(f"  初始资金:       ${initial:,.2f}")
        print(f"  +{gain:.0%} 后:       ${after_gain:,.2f}")
        print(f"  -{loss:.0%} 后:       ${after_loss:,.2f}")
        print(f"  算术平均:        {arithmetic_avg:.2%}   ← 看起来 = 0%")
        print(f"  实际复合收益:    {actual_return:.2%}   ← 真实亏损!")
        print(f"  理论拖曳 ≈ σ/2: {theoretical_drag:.2%}")
        print("─" * 45)

    return result


# ──────────────────────────────────────────────
# Concept 18-19 - pct_change + dropna
# ──────────────────────────────────────────────
def prices_to_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    将价格序列转换为收益率序列。
    - 使用 pct_change()（Concept 18）
    - dropna 移除第一行 NaN（Concept 19）
    """
    returns = prices.pct_change()
    returns.dropna(inplace=True)
    return returns


# ──────────────────────────────────────────────
# Concept 20 - Plotting Returns
# ──────────────────────────────────────────────
def plot_returns(returns: pd.DataFrame, ax=None) -> None:
    """绘制收益率时间序列。"""
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(12, 4))
    returns.plot(ax=ax, title="Return Series", alpha=0.8)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Monthly Return")
    ax.set_xlabel("")
    if standalone:
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────
# Concept 21 - Compound the Series (.prod)
# ──────────────────────────────────────────────
def total_compound_return(returns: pd.DataFrame) -> pd.Series:
    """
    全量复合收益率：(1+returns).prod() - 1
    """
    return (1 + returns).prod() - 1


# ──────────────────────────────────────────────
# Concept 22 - Formatted Output
# ──────────────────────────────────────────────
def format_returns(series: pd.Series, decimals: int = 2) -> pd.Series:
    """
    将收益率序列格式化为百分比字符串，便于展示。
    """
    return (series * 100).round(decimals).astype(str) + "%"


def print_return_summary(returns: pd.DataFrame) -> None:
    """打印简洁的收益率汇总报告。"""
    total = total_compound_return(returns)
    formatted = format_returns(total)

    print("\n" + "=" * 45)
    print("  COMPOUND RETURN SUMMARY")
    print("=" * 45)
    for ticker, val in formatted.items():
        print(f"  {ticker:<10}: {val}")
    print("=" * 45)
