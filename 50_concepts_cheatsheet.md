# 50 量化代码速查表 (50 Quant Concepts Cheatsheet)

这份速查表汇总了你在本项目中学习和使用到的 50 个核心量化编程概念与代码指令片段。

## 1. 基础依赖导入 (Data Source)
1. **NumPy**：处理矩阵与数组的数学库
   ```python
   import numpy as np
   ```
2. **Pandas**：金融数据分析最核心的库
   ```python
   import pandas as pd
   ```
3. **Matplotlib**：数据可视化画图库
   ```python
   import matplotlib.pyplot as plt
   ```
4. **read_csv**：从本地或网址加载外部数据
   ```python
   df = pd.read_csv("path/to/data.csv")
   ```
5. **yfinance**：雅虎财经的 Python 接口库
   ```python
   import yfinance as yf
   ```
6. **yf.download**：下载历史各周期数据
   ```python
   prices = yf.download("SPY", period="max", interval="1mo")
   ```
7. **Adjusted Close (复权收盘价)**：包含分红和拆股的真实价格
   ```python
   prices = yf.download(["SPY", "AGG"], period="max")["Adj Close"]
   ```

## 2. 数据信息与清洗 (Information Preparation)
8. **Series (序列)**：单只股票的一维数据结构
   ```python
   spy = prices["SPY"]
   ```
9. **DataFrame (数据框)**：多只股票的二维表格矩阵
   ```python
   type(prices) # pandas.core.frame.DataFrame
   ```
10. **dropna 和 inplace**：清洗缺失数据（替换原有数据）
    ```python
    prices.dropna(inplace=True)
    ```
11. **Price Series (价格序列)**：连续时间步长上的资产价格。
12. **Index (时间索引整理)**：将精确时间戳格式化为按月度周期
    ```python
    prices.index = prices.index.to_period("M")
    ```
13. **Plotting Prices (价格可视化)**：基础折线图
    ```python
    prices.plot(title="Price Series")
    plt.show()
    ```

## 3. 收益率法则 (Returns)
14. **标准单期收益率**：(期末 - 期初) / 期初
    ```python
    ret = (p_final - p_initial) / p_initial
    ```
15. **1+R 格式**：期末 / 期初（便于复利乘法）
    ```python
    one_plus_r = p_final / p_initial
    ```
16. **Multi-Period Return (多期复合收益)**
    ```python
    compound = (1 + r1) * (1 + r2) * (1 + r3) - 1
    ```
17. **Variance Drag (方差拖曳)**：由于波动率导致的算术平均大于几何平均的隐形损耗。
18. **pct_change (百分比变化)**：Pandas 将价格一键转收益率的捷径
    ```python
    returns = prices.pct_change()
    ```
19. **首日数据丢失 (First Data Point Loss)**：价格转成收益率第一天必然是空值
    ```python
    returns.dropna(inplace=True)
    ```
20. **Plotting Returns (收益率可视化)**
    ```python
    returns.plot(title="Return Series")
    ```
21. **.prod() (序列复利)**：一行代码计算二十年的总收益
    ```python
    total_return = (1 + returns).prod() - 1
    ```
22. **Formatting Output (打印格式化)**
    ```python
    print((total_return * 100).round(2).astype(str) + "%")
    ```

## 4. 数据框常用查询 (DataFrame Methods)
23. **head()**：获取前 5 行数据
24. **tail()**：获取最后 5 行数据
25. **size**：数据元素总数量
26. **shape**：矩阵的行列数量 `(rows, columns)`
27. **index**：数据的行索引（在这里是日期）
28. **columns**：数据的列索引（在这里是股票代码）
29. **单括号索引**：提取 Series `prices["SPY"]`
30. **双括号索引**：提取子 DataFrame `prices[["SPY", "AGG"]]`
31. **loc**：按名字/日期索引行 `prices.loc["2025-01"]`
32. **iloc**：按数字行号索引 `prices.iloc[0:12]`

## 5. 风险与夏普指标 (Measures of Risk)
33. **Standard Deviation (标准差/波动率)**：价格偏离均值的幅度
    ```python
    vol = returns.std()
    ```
34. **Annualized Return (年化收益)**：逆推复利至每年
    ```python
    ann_ret = ((1 + returns).prod()) ** (12 / len(returns)) - 1
    ```
35. **Annualized Volatility (年化波动)**：按时间平方根放大
    ```python
    ann_vol = returns.std() * np.sqrt(12)
    ```
36. **Raw Sharpe Ratio (原始夏普)**：单位风险对应的收益
    ```python
    sharpe = ann_ret / ann_vol
    ```
37. **Risk-Free Rate (无风险利率调整)**：真实夏普要先减掉国债无风险利率

## 6. 财富指数与最大回撤 (Wealth Index & Drawdowns)
38. **.cumprod() (财富指数)**：模拟投入 $1 每时间节点的资产价值
    ```python
    wealth_index = (1 + returns).cumprod()
    ```
39. **DateOffset (日期偏移)**：把时间往前移一格加入起点
    ```python
    start = returns.index.min() - pd.DateOffset(months=1)
    ```
40. **pd.concat (数据拼接)**：把最开始的 $1 基点合并到曲线前头
41. **.cummax() (前期高点/历史极值)**：走到这一步人生见过的最大值
    ```python
    previous_peaks = wealth_index.cummax()
    ```
42. **Drawdown Formula (回撤公式)**：由于高点跌下来的亏损幅度
    ```python
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    ```
43. **Maximum Drawdown (最大回撤幅度)**：寻找这一生跌得最惨的那个谷底点
    ```python
    max_dd = drawdowns.min()
    ```
44. **Date of Maximum Drawdown (最大回撤发生日)**
    ```python
    max_dd_date = drawdowns.idxmin()
    ```
45. **Matplotlib Annotation (图表标注)**：给最大跌幅处画个标记
    ```python
    plt.annotate(f"Max DD: {max_dd:.2%}", xy=(max_dd_date, max_dd))
    ```
46. **arrowprops (箭头参数)**：配置刚刚标记使用的指针样式

## 7. 仪表板与理论总结
47. **Subplots (多子图)**：2行2列画出四大核心资产图 
    ```python
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ```
48. **为什么 回撤 > 波动率？**：波动率认为暴涨 5% 和暴跌 5% 风险一样大，但人类其实只能感受到“回撤”带来的下行痛苦。
49. **The Full Pipeline (完整流水线)**：全貌端到端实现（见 `main.py`）。
50. **What Comes Next**：以上 49 条是理解**期权定价、蒙特卡洛模拟、量化多因子回归**的绝对基石。
