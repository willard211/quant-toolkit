"""
wealth_drawdown.py
==================
Concepts covered: 38-46
财富指数与回撤分析模块

涵盖:
  - 财富指数（累积乘积）
  - DateOffset 插入起始点
  - pd.concat 拼接
  - 前高（cummax）
  - 回撤公式
  - 最大回撤 + 发生日期
  - Matplotlib 标注箭头
  - arrowprops 格式化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# ──────────────────────────────────────────────
# Concept 38 - Wealth Index (.cumprod)
# ──────────────────────────────────────────────
def build_wealth_index(returns: pd.DataFrame) -> pd.DataFrame:
    """
    将收益率序列转化为财富指数（$1 增长曲线）：
        wealth = (1 + returns).cumprod()
    """
    return (1 + returns).cumprod()


# ──────────────────────────────────────────────
# Concepts 39-40 - DateOffset + pd.concat
# ──────────────────────────────────────────────
def prepend_base(wealth_index: pd.DataFrame) -> pd.DataFrame:
    """
    在财富指数最前方插入 $1 基准点，使所有资产从同一起点出发。

    - 用 DateOffset 往前推一个月（Concept 39）
    - 用 pd.concat 拼接（Concept 40）
    """
    # pandas 3.0 中 Period 不支持 DateOffset 减法，
    # 改用 Period 频率算术：直接对 Period 整数减 1
    min_period = wealth_index.index.min()
    start = min_period - 1  # Period 直接支持整数加减（-1 = 往前一期）
    base = pd.DataFrame(
        {col: [1.0] for col in wealth_index.columns},
        index=pd.PeriodIndex([start], freq="M"),
    )
    return pd.concat([base, wealth_index])



# ──────────────────────────────────────────────
# Concept 41 - Previous Peaks (.cummax)
# ──────────────────────────────────────────────
def previous_peaks(wealth_index: pd.DataFrame) -> pd.DataFrame:
    """
    计算运行历史最高点（前高）。
    cummax：每个时刻对应其本身及此前所有点中的最大值。
    """
    return wealth_index.cummax()


# ──────────────────────────────────────────────
# Concept 42 - Drawdown Series
# ──────────────────────────────────────────────
def calc_drawdowns(wealth_index: pd.DataFrame) -> pd.DataFrame:
    """
    回撤序列：
        drawdown = (wealth - peak) / peak

    始终为零或负数，表示从前高的百分比下跌幅度。
    """
    peaks = previous_peaks(wealth_index)
    return (wealth_index - peaks) / peaks


# ──────────────────────────────────────────────
# Concept 43 - Maximum Drawdown
# ──────────────────────────────────────────────
def max_drawdown(drawdowns: pd.DataFrame) -> pd.Series:
    """
    最大回撤：回撤序列中的最小值（最大负数）。
    """
    return drawdowns.min()


# ──────────────────────────────────────────────
# Concept 44 - Date of Max Drawdown
# ──────────────────────────────────────────────
def max_drawdown_date(drawdowns: pd.DataFrame) -> pd.Series:
    """
    最大回撤发生日期：使用 .idxmin()。
    """
    return drawdowns.idxmin()


# ──────────────────────────────────────────────
# Concepts 45-46 - Matplotlib Annotation + arrowprops
# ──────────────────────────────────────────────
def plot_drawdowns(drawdowns: pd.DataFrame, ax=None) -> None:
    """
    绘制回撤面积图，并为每个资产标注最大回撤点。

    箭头样式通过 arrowprops 字典控制（Concept 46）。
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(12, 5))

    # 面积图
    drawdowns.plot.area(ax=ax, alpha=0.35, title="Drawdowns")
    ax.set_ylabel("Drawdown (%)")
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.0%}")
    )

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    mdd = max_drawdown(drawdowns)
    mdd_dates = max_drawdown_date(drawdowns)

    for i, col in enumerate(drawdowns.columns):
        mdd_val = mdd[col]
        mdd_date = mdd_dates[col]

        # Concept 45 - plt.annotate
        ax.annotate(
            f"{col} Max DD: {mdd_val:.2%}",
            xy=(mdd_date.to_timestamp(), mdd_val),
            xytext=(mdd_date.to_timestamp(), mdd_val + 0.06),
            # Concept 46 - arrowprops formatting
            arrowprops=dict(
                arrowstyle="->",
                color=colors[i % len(colors)],
                lw=1.5,
            ),
            fontsize=8,
            color=colors[i % len(colors)],
        )

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")

    if standalone:
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────
# Concept 48 - Why Drawdowns > Volatility
# ──────────────────────────────────────────────
def drawdown_vs_vol_insight(returns: pd.DataFrame) -> None:
    """
    打印回撤与波动率的关键区别说明。
    回撤只衡量下行风险（你真正感受到的损失），
    而波动率对涨跌一视同仁。
    """
    from risk_metrics import annualize_vol, annualize_return
    wealth = build_wealth_index(returns)
    dd = calc_drawdowns(wealth)
    mdd = max_drawdown(dd)
    ann_vol = annualize_vol(returns)
    ann_ret = annualize_return(returns)

    print("\n" + "=" * 55)
    print("  DRAWDOWN vs VOLATILITY INSIGHT (Concept 48)")
    print("=" * 55)
    for col in returns.columns:
        print(f"\n  [{col}]")
        print(f"    年化收益:   {ann_ret[col]:.2%}")
        print(f"    年化波动率: {ann_vol[col]:.2%}  ← 涨跌等权")
        print(f"    最大回撤:   {mdd[col]:.2%}      ← 只反映亏损体验")
    print("\n   相同夏普可以对应截然不同的最大回撤体验！")
    print("=" * 55)


def drawdown_summary(returns: pd.DataFrame) -> pd.DataFrame:
    """输出回撤汇总 DataFrame。"""
    wealth = prepend_base(build_wealth_index(returns))
    dd = calc_drawdowns(wealth)
    return pd.DataFrame({
        "Max Drawdown (%)": (max_drawdown(dd) * 100).round(2),
        "Max DD Date":      max_drawdown_date(dd).astype(str),
    })
