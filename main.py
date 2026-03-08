"""
main.py
=======
Concept 49 - The Full Pipeline
量化金融分析完整流水线

将所有模块整合为一个端到端的分析程序：
  1. 下载数据
  2. 计算收益率
  3. 风险指标
  4. 财富指数 + 回撤
  5. 4 合 1 仪表板可视化
  6. 方差拖曳演示

用法:
  python main.py                           # 默认 SPY + AGG
  python main.py --tickers SPY QQQ BTC-USD # 自定义股票池
  python main.py --rf 0.045               # 指定无风险利率 4.5%
  python main.py --save                   # 将图表保存为 PNG
"""

import argparse
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data_loader import download_prices, inspect_data
from returns import (
    prices_to_returns,
    total_compound_return,
    format_returns,
    print_return_summary,
    demonstrate_variance_drag,
)
from risk_metrics import print_risk_summary, risk_return_summary
from wealth_drawdown import (
    build_wealth_index,
    prepend_base,
    calc_drawdowns,
    drawdown_summary,
    drawdown_vs_vol_insight,
)
from visualizer import plot_dashboard, save_dashboard


# ─────────────────────────────────────────────────────────
# 主流水线函数
# ─────────────────────────────────────────────────────────
def run_pipeline(
    tickers: list[str],
    rf_rate: float = 0.05,
    save_chart: bool = False,
    chart_path: str = "dashboard.png",
) -> dict:
    """
    Concept 49 - 完整量化分析流水线。

    Returns 包含所有中间结果的字典，方便进一步分析。
    """

    print("\n" + "█" * 60)
    print("█  QUANT TOOLKIT — 50 Hedge Fund Concepts in Python   █")
    print("█" * 60)
    print(f"\n 分析标的: {', '.join(tickers)}")
    print(f" 当前时间: 2026-03-08")
    print(f" 无风险利率: {rf_rate:.2%}\n")

    # ── STEP 1: 下载数据 ──────────────────────────────────
    print("  下载历史月度数据...")
    prices = download_prices(tickers)
    inspect_data(prices)

    # ── STEP 2: 收益率计算 ────────────────────────────────
    print("\n 计算收益率序列...")
    returns = prices_to_returns(prices)
    print_return_summary(returns)

    # ── STEP 3: 方差拖曳演示 ──────────────────────────────
    print("\n")
    demonstrate_variance_drag(initial=100, gain=0.30, loss=0.30)

    # ── STEP 4: 风险指标 ──────────────────────────────────
    print_risk_summary(returns, rf_rate=rf_rate)

    # ── STEP 5: 财富指数 + 回撤 ───────────────────────────
    print("\n 构建财富指数与回撤序列...")
    wealth = prepend_base(build_wealth_index(returns))
    drawdowns = calc_drawdowns(wealth)

    print("\n" + "=" * 55)
    print("  DRAWDOWN SUMMARY")
    print("=" * 55)
    print(drawdown_summary(returns).to_string())
    print("=" * 55)

    # ── STEP 6: 回撤 vs 波动率洞察 ───────────────────────
    drawdown_vs_vol_insight(returns)

    # ── STEP 7: 4 合 1 仪表板 ─────────────────────────────
    print("\n  生成可视化仪表板...")
    fig = plot_dashboard(
        prices=prices,
        returns=returns,
        wealth_index=wealth,
        drawdowns=drawdowns,
        suptitle=f"Quant Dashboard — {' & '.join(tickers)}",
    )

    if save_chart:
        save_dashboard(fig, chart_path)

    plt.show()

    print("\n" + "█" * 60)
    print("█  分析完成！Concept 50: 这些工具构成了所有高级量化  █")
    print("█  策略的基础：期权定价、蒙特卡洛模拟、因子模型...  █")
    print("█" * 60)
    print(" 提示: 如果你看不懂上面表格里的专有名词，请运行:")
    print("   python main.py --explain")
    print("█" * 60 + "\n")

    return {
        "prices": prices,
        "returns": returns,
        "wealth": wealth,
        "drawdowns": drawdowns,
        "risk_summary": risk_return_summary(returns, rf_rate=rf_rate),
        "dd_summary": drawdown_summary(returns),
    }


# ─────────────────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="Quant Toolkit — 50 Hedge Fund Concepts in Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py
  python main.py --tickers SPY QQQ GLD
  python main.py --tickers BTC-USD ETH-USD --rf 0.04
  python main.py --save --out my_chart.png
        """,
    )
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=["SPY", "AGG"],
        metavar="TICKER",
        help="股票/ETF 代码列表（默认: SPY AGG）",
    )
    parser.add_argument(
        "--rf",
        type=float,
        default=0.05,
        dest="rf_rate",
        help="年化无风险利率（默认: 0.05 = 5%%）",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="将仪表板保存为 PNG 文件",
    )
    parser.add_argument(
        "--out",
        default="dashboard.png",
        dest="chart_path",
        help="图表输出路径（默认: dashboard.png）",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="打印量化金融指标的通俗白话文解释",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.explain:
        import explainer
        explainer.print_explanations()
    else:
        results = run_pipeline(
            tickers=args.tickers,
            rf_rate=args.rf_rate,
            save_chart=args.save,
            chart_path=args.chart_path,
        )
