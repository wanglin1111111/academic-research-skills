#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将量化策略框架写入个人知识库
使用 Markdown 格式保存到 workspace/memory/ 目录
"""

import os
from datetime import datetime

def save_to_knowledge_base(content, filename):
    """保存内容到知识库"""
    # 知识库路径
    kb_path = os.path.expanduser("~/.qclaw/workspace/memory")
    os.makedirs(kb_path, exist_ok=True)
    
    # 完整文件路径
    filepath = os.path.join(kb_path, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] 已保存到知识库: {filepath}")
    return filepath

def create_strategy_summary():
    """创建策略摘要文档"""
    content = """# 量化交易策略框架 - 知识库摘要

**创建时间**: 2026-06-05  
**来源**: 用户提供的10大类量化策略清单  
**用途**: 个人知识库参考资料

---

## 策略分类速查表

### 一、趋势跟踪策略
- 动态ATR通道突破
- 多周期MACD共振
- 海龟交易法则改良
- 波动率调整持仓
- 日内趋势平仓算法

### 二、均值回归策略
- 布林带收缩统计套利
- RSI极端值回归
- 跨品种价差协整
- 订单簿失衡回归
- VIX均值回归

### 三、套利策略
- 跨交易所三角套利
- ETF折溢价套利
- 期货跨期套利
- 可转债delta对冲
- 外汇三币套利

### 四、事件驱动策略
- 财报option波动率
- 指数调整抢跑
- 央行利率决议
- 大宗交易因子
- 社交媒体情绪

### 五、市场环境应对
- Gamma Scalping
- 反向价差交易
- 波动率曲面交易
- 熔断机制应对
- 尾部风险对冲

### 六、组合优化
- 动态风险平价
- 相关性矩阵
- 最大回撤约束
- 流动性分层
- 保证金监控

### 七、数据处理
- Tick数据清洗
- 多频数据对齐
- 因子衰减测定
- 新闻情感分析
- 另类数据降噪

### 八、风险管理
- 动态VaR模型
- 策略拥挤度监测
- 杠杆率自适应
- Monte Carlo模拟
- 敞口可视化

### 九、交易执行
- TWAP算法优化
- 冰山订单预测
- 订单流毒性检测
- 智能路由算法
- 冲击成本模型

### 十、回测验证
- 幸存者偏差修正
- 滑点敏感性分析
- 过拟合识别
- Regime切换测试
- 实盘差异归因

---

## 使用建议

### 1. 快速查找策略
根据市场环境选择策略类型：
- 趋势市场 → 趋势跟踪
- 震荡市场 → 均值回归
- 价格差异 → 套利
- 特殊事件 → 事件驱动

### 2. 代码实现请求模板
```
请用Python展示 [策略名称] 的实现框架，包括：
1. 数据获取
2. 信号生成
3. 风险控制
4. 回测验证
```

### 3. 参数优化请求模板
```
请针对 [具体市场] 优化 [策略名称] 的参数：
- 市场特点：[描述]
- 约束条件：[描述]
- 优化目标：[描述]
```

### 4. 分步实现请求模板
```
请分步骤实现 [复杂策略]：
Step 1: [子任务1]
Step 2: [子任务2]
...
```

---

## 核心思想总结

### 1. 策略设计原则
- **简单有效**: 复杂的策略容易过拟合
- **风险第一**: 永远把风险控制放在第一位
- **适应性强**: 策略要能适应不同市场环境

### 2. 实施要点
- **数据质量**: 高质量数据是成功的基础
- **回测验证**: 充分验证后再实盘
- **成本控制**: 手续费、滑点、冲击成本

### 3. 持续优化
- **监控**: 实时监控策略表现
- **调整**: 市场变了，策略也要调整
- **学习**: 从失败中总结经验

---

## 相关文件

- 完整框架: `academic-research-skills/skills/quantitative-strategy-framework/SKILL.md`
- 股票分析: `academic-research-skills/skills/stock-analysis/SKILL.md`
- 量化金融: `academic-research-skills/skills/quantitative-finance/SKILL.md`
- AI构建系统: `academic-research-skills/skills/ai-quantitative-system-builder/SKILL.md`

---

**标签**: #量化交易 #策略框架 #知识库 #参考手册
**最后更新**: 2026-06-05
"""
    
    return content

def create_implementation_examples():
    """创建策略实现示例"""
    
    # 示例1: 动态ATR通道突破策略
    example1 = """
# 示例1: 动态ATR通道突破策略

## 策略逻辑
使用ATR构建动态通道，价格突破上轨买入，突破下轨卖出。

## Python实现框架

```python
import pandas as pd
import numpy as np

def calculate_atr(high, low, close, period=14):
    \"\"\"计算ATR\"\"\"
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr

def dynamic_atr_channel_strategy(data, atr_period=14, channel_multiplier=2):
    \"\"\"
    动态ATR通道突破策略
    
    Parameters:
    - data: DataFrame with columns [open, high, low, close]
    - atr_period: ATR计算周期
    - channel_multiplier: 通道倍数
    
    Returns:
    - signals: 交易信号 (1:买入, -1:卖出, 0:持有)
    \"\"\"
    # 计算ATR
    data['atr'] = calculate_atr(data['high'], data['low'], data['close'], atr_period)
    
    # 计算动态通道
    data['upper_channel'] = data['close'] + channel_multiplier * data['atr']
    data['lower_channel'] = data['close'] - channel_multiplier * data['atr']
    
    # 生成信号
    data['signal'] = 0
    data.loc[data['close'] > data['upper_channel'], 'signal'] = 1   # 买入
    data.loc[data['close'] < data['lower_channel'], 'signal'] = -1  # 卖出
    
    return data['signal']

# 使用示例
if __name__ == '__main__':
    # 假设已有数据
    # data = pd.read_csv('stock_data.csv')
    # signals = dynamic_atr_channel_strategy(data)
    pass
```
"""
    
    # 示例2: 海龟交易法则改良
    example2 = """
# 示例2: 海龟交易法则的现代改良（考虑流动性衰减）

## 改进点
1. 根据成交量调整仓位（流动性衰减时减仓）
2. 动态止损：考虑流动性因子
3. 分批建仓：避免冲击成本

## Python实现框架

```python
def improved_turtle_strategy(data, atr_period=20, breakout_period=20):
    \"\"\"
    改良版海龟交易策略
    
    Improvements:
    - Consider liquidity decay
    - Dynamic position sizing
    - Batch entry to reduce impact cost
    \"\"\"
    # 计算ATR
    data['atr'] = calculate_atr(data['high'], data['low'], data['close'], atr_period)
    
    # 计算突破通道
    data['upper_channel'] = data['high'].rolling(breakout_period).max()
    data['lower_channel'] = data['low'].rolling(breakout_period).min()
    
    # 计算流动性因子 (基于成交量)
    data['volume_ma'] = data['volume'].rolling(20).mean()
    data['liquidity_factor'] = data['volume'] / data['volume_ma']
    data['liquidity_factor'] = data['liquidity_factor'].clip(upper=2.0)  # 上限2.0
    
    # 动态仓位计算
    account_risk = 0.02  # 账户风险2%
    data['position_size'] = (account_risk * data['close']) / (data['atr'] * 2 * data['liquidity_factor'])
    
    # 动态止损
    data['stop_loss'] = data['close'] - 2 * data['atr'] * data['liquidity_factor']
    
    # 生成信号
    data['signal'] = 0
    data.loc[data['close'] > data['upper_channel'], 'signal'] = 1
    data.loc[data['close'] < data['lower_channel'], 'signal'] = -1
    
    return data[['signal', 'position_size', 'stop_loss']]
```
"""
    
    return example1 + "\\n" + example2

def main():
    """主函数"""
    print("=" * 60)
    print("将量化策略框架写入个人知识库")
    print("=" * 60)
    
    # 1. 创建策略摘要
    print("\\n[1/3] 创建策略摘要文档...")
    summary = create_strategy_summary()
    save_to_knowledge_base(summary, f"quant_strategy_summary_{datetime.now().strftime('%Y%m%d')}.md")
    
    # 2. 创建实现示例
    print("\\n[2/3] 创建策略实现示例...")
    examples = create_implementation_examples()
    save_to_knowledge_base(examples, f"quant_strategy_examples_{datetime.now().strftime('%Y%m%d')}.md")
    
    # 3. 创建速查表
    print("\\n[3/3] 创建策略速查表...")
    cheat_sheet = """# 量化策略速查表

## 趋势跟踪
- ATR通道: 高波动市场
- MACD共振: 趋势确认
- 海龟改良: 流动性考量

## 均值回归
- 布林带: 收缩后突破
- RSI: 极端值回归
- 协整: 价差回归

## 套利
- 三角套利: 延迟补偿
- ETF套利: 折溢价风控
- 跨期套利: 展期成本

## 事件驱动
- 财报: option波动率
- 指数调整: 抢跑策略
- 央行决议: 分钟级捕捉

## 风险管理
- VaR: 压力测试
- 拥挤度: 监测指标
- 杠杆: 波动率自适应

**快速参考**: 看完整文档 `quantitative-strategy-framework/SKILL.md`
"""
    save_to_knowledge_base(cheat_sheet, f"quant_strategy_cheatsheet_{datetime.now().strftime('%Y%m%d')}.md")
    
    print("\\n" + "=" * 60)
    print("[OK] 完成！所有文档已保存到知识库")
    print("=" * 60)

if __name__ == '__main__':
    main()
