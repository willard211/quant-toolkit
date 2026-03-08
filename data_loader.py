"""
data_loader.py
==============
Concepts covered: 1-13
数据获取、清洗与基础数据结构处理模块

涵盖:
  - NumPy / Pandas / Matplotlib / yfinance 导入
  - pd.read_csv (备用路径)
  - yf.download + Adjusted Close
  - Series vs DataFrame
  - dropna / index.to_period
  - head / tail / size / shape / index / columns
  - 单双括号索引 / .loc / .iloc
"""

import numpy as np                      # Concept 1 - NumPy
import pandas as pd                     # Concept 2 - Pandas
import matplotlib.pyplot as plt         # Concept 3 - Matplotlib
import yfinance as yf                   # Concept 5 - yfinance

# ──────────────────────────────────────────────
# Concept 4 - read_csv (备用本地/远程 CSV 加载)
# ──────────────────────────────────────────────
def load_from_csv(path: str) -> pd.DataFrame:
    """从本地文件或 URL 加载价格数据。"""
    return pd.read_csv(path, index_col=0, parse_dates=True)


# ──────────────────────────────────────────────
# Concepts 6-7 - yf.download + Adjusted Close
# ──────────────────────────────────────────────
def download_prices(
    tickers: list,
    period: str = "max",
    interval: str = "1mo",
) -> pd.DataFrame:
    """
    通过 yfinance 下载多支股票的月度复权收盘价。

    Parameters
    ----------
    tickers  : 股票代码列表，例如 ["SPY", "AGG"]
    period   : 时间范围，"max" 代表全部历史
    interval : 数据粒度，"1mo" = 月线

    Returns
    -------
    pd.DataFrame  —  复权收盘价 (Adjusted Close)，已做索引周期化
    """
    # Concept 6 - yf.download
    # yfinance 1.2.0: auto_adjust=True → 列名为 "Close"
    #                 multi_level_index=True (默认) → MultiIndex 列
    raw = yf.download(
        tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    # Concept 7 - Adjusted Close
    # 处理 MultiIndex 和 单层 Index 两种情况
    if isinstance(raw.columns, pd.MultiIndex):
        # 多股票: ("Close", "SPY"), ("Close", "AGG") ...
        if "Close" in raw.columns.get_level_values(0):
            prices = raw["Close"]
        else:
            prices = raw.xs("Close", axis=1, level=0)
        # 保证列名与传入的 tickers 顺序一致
        prices = prices[[t for t in tickers if t in prices.columns]]
    else:
        # 单股票 或 multi_level_index=False 情况
        if "Close" in raw.columns:
            prices = raw[["Close"]].rename(columns={"Close": tickers[0]})
        else:
            prices = raw.iloc[:, :1].copy()
            prices.columns = tickers[:1]

    # Concept 10 - dropna.inplace：移除因上市日期不同产生的 NaN
    prices.dropna(inplace=True)

    # Concept 12 - index.to_period：将日期索引转为月度周期
    prices.index = prices.index.to_period("M")

    return prices


# ──────────────────────────────────────────────
# Concepts 8-9 - Series vs DataFrame inspection
# ──────────────────────────────────────────────
def inspect_data(prices: pd.DataFrame, verbose: bool = True) -> dict:
    """
    打印并返回 DataFrame 的基本信息。

    Demonstrates:
      Series (single column), DataFrame (multi-column),
      head/tail, size, shape, index, columns,
      single/double bracket indexing, loc, iloc
    """
    info = {}

    # Concept 8 - Series（单股）
    first_ticker = prices.columns[0]
    single = prices[first_ticker]                       # → Series
    info["series_type"] = type(single).__name__

    # Concept 9 - DataFrame（多股）
    info["dataframe_type"] = type(prices).__name__

    if verbose:
        print("=" * 55)
        print("  DATA INSPECTION")
        print("=" * 55)
        # Concept 23 - head()
        print("\n Head (first 5 rows):")
        print(prices.head())

        # Concept 24 - tail()
        print("\n Tail (last 3 rows):")
        print(prices.tail(3))

        # Concept 25 - size
        print(f"\n Size (total elements): {prices.size}")

        # Concept 26 - shape
        print(f" Shape (rows, cols):    {prices.shape}")

        # Concept 27 - index
        print(f" Index (dates):         {prices.index[:3]} ...")

        # Concept 28 - columns
        print(f" Columns (tickers):     {list(prices.columns)}")

        # Concept 29 - single bracket → Series
        print(f"\n Single bracket [{first_ticker!r}]  → {type(single).__name__}")

        # Concept 30 - double bracket → DataFrame
        multi = prices[list(prices.columns)]
        print(f" Double bracket [all]   → {type(multi).__name__}")

        # Concept 31 - loc
        first_label = prices.index[0]
        print(f"\n .loc[{first_label}]:")
        print(prices.loc[first_label])

        # Concept 32 - iloc
        print(f"\n .iloc[0:2]:")
        print(prices.iloc[0:2])

    info.update({
        "size": prices.size,
        "shape": prices.shape,
        "tickers": list(prices.columns),
        "start": str(prices.index.min()),
        "end": str(prices.index.max()),
    })
    return info
