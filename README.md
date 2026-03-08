# Quant Toolkit — 50 Hedge Fund Concepts in Python

基于 phosphenq 在 X 上发布的《50个对冲基金量化概念》文章，将所有概念整合为一个**模块化、可执行的 Python 量化分析工具包**。

## 项目结构

```
quant_toolkit/
├── data_loader.py       # 概念 1-13, 23-32  数据获取与探索
├── returns.py           # 概念 14-22        收益率计算
├── risk_metrics.py      # 概念 33-37        风险指标
├── wealth_drawdown.py   # 概念 38-46, 48    财富指数与回撤
├── visualizer.py        # 概念 47           4合1仪表板
├── main.py              # 概念 49           完整流水线
└── requirements.txt     # 依赖
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行默认分析 (SPY + AGG)
python main.py

# 3. 自定义股票池
python main.py --tickers SPY QQQ GLD BTC-USD

# 4. 指定无风险利率并保存图表
python main.py --tickers SPY AGG --rf 0.045 --save --out my_dashboard.png
```

## 50个概念覆盖一览

| 模块 | 概念编号 | 核心内容 |
|------|---------|---------|
| `data_loader.py` | 1-13, 23-32 | NumPy/Pandas/Matplotlib/yfinance, 价格序列, 数据探索 |
| `returns.py` | 14-22 | 收益率公式, 1+R格式, 几何复合, **方差拖曳** |
| `risk_metrics.py` | 33-37 | 标准差, 年化收益/波动率, 夏普比率, 无风险利率 |
| `wealth_drawdown.py` | 38-46, 48 | 财富指数, DateOffset, 前高, 回撤, 最大回撤, 标注 |
| `visualizer.py` | 47 | 2×2 子图仪表板 |
| `main.py` | 49-50 | 完整端到端流水线 |

## 核心概念深度解析

### ⚠️ 方差拖曳 (Concept 17) — 最重要的一个

均值为 0% 但实际损失 9%：
- +30% → $130
- -30% → $91（-30% 作用在更大的基数上）

**理论拖曳 ≈ σ²/2**，在高波动资产（如杠杆 ETF）中极为显著。

### 📐 年化转换

- **收益率**：`compound_growth ^ (12/n) - 1`（逆推等效年化）
- **波动率**：`σ_monthly × √12`（方差线性累积，标准差 √ 缩放）

### 📊 夏普比率评级

| 值域 | 评级 |
|------|------|
| < 0.5 | 偏弱 |
| 0.5 – 1.0 | 股票均值 |
| > 1.0 | 强劲 |
| > 2.0 | 顶级 |

### 💡 回撤 vs 波动率 (Concept 48)

- 波动率：涨跌一视同仁（+5% 和 -5% 贡献相同）
- 回撤：**只衡量你实际亏损体验的幅度**
- 相同夏普的两个策略，-20% 和 -60% 最大回撤的持有体验天壤之别
