"""
visualizer.py
=============
Concept covered: 47
4 合 1 子图仪表板模块

涵盖:
  - plt.subplots 多子图布局
  - 价格 / 收益率 / 财富指数 / 回撤 四视图
  - tight_layout 自动间距
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from returns import plot_returns
from wealth_drawdown import plot_drawdowns


def plot_dashboard(
    prices: pd.DataFrame,
    returns: pd.DataFrame,
    wealth_index: pd.DataFrame,
    drawdowns: pd.DataFrame,
    figsize: tuple = (16, 11),
    suptitle: str = "Quantitative Finance Dashboard",
) -> plt.Figure:
    """
    Concept 47 - Subplots：将 4 个核心视图整合到一张仪表板。

    Layout（2×2 网格）:
      ┌────────────────┬────────────────┐
      │  价格序列       │  收益率序列     │
      ├────────────────┼────────────────┤
      │  财富指数       │  回撤          │
      └────────────────┴────────────────┘
    """
    # ── 全局样式 ───────────────────────────────
    plt.style.use("seaborn-v0_8-darkgrid")
    colors = ["#2E86AB", "#E84855", "#3BB273", "#F4A261"]

    # ── 创建 2×2 子图 ──────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold", y=0.98)

    # ── 左上：价格序列 ─────────────────────────
    ax = axes[0, 0]
    for i, col in enumerate(prices.columns):
        prices[col].plot(ax=ax, label=col, color=colors[i % len(colors)], linewidth=2)
    ax.set_title(" Price Series", fontsize=12, fontweight="bold")
    ax.set_ylabel("Price ($)")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── 右上：收益率序列 ───────────────────────
    ax = axes[0, 1]
    plot_returns(returns, ax=ax)
    ax.set_title(" Return Series", fontsize=12, fontweight="bold")
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda y, _: f"{y:.1%}")
    )

    # ── 左下：财富指数 ─────────────────────────
    ax = axes[1, 0]
    for i, col in enumerate(wealth_index.columns):
        wealth_index[col].plot(
            ax=ax, label=col, color=colors[i % len(colors)], linewidth=2
        )
    ax.set_title(" Wealth Index (Growth of $1)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.2f}"))

    # ── 右下：回撤 ─────────────────────────────
    ax = axes[1, 1]
    plot_drawdowns(drawdowns, ax=ax)
    ax.set_title(" Drawdowns", fontsize=12, fontweight="bold")

    # ── 统一美化 ───────────────────────────────
    for row in axes:
        for a in row:
            a.set_xlabel("")
            a.tick_params(axis="x", rotation=30, labelsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


def save_dashboard(fig: plt.Figure, path: str = "dashboard.png") -> str:
    """保存图表到文件并返回路径。"""
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f" Dashboard saved → {path}")
    return path
