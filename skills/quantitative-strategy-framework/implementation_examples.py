#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化策略实现示例集合
包含3个核心策略的完整实现框架
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class QuantitativeStrategyExamples:
    """
    量化策略示例集合
    包含趋势跟踪、均值回归、套利三大类策略
    """
    
    @staticmethod
    def example1_dynamic_atr_channel():
        """
        示例1: 动态ATR通道突破策略
        
        适用市场: 高波动市场
        核心思想: 使用ATR构建动态通道，适应波动率变化
        """
        print("\n" + "=" * 60)
        print("示例1: 动态ATR通道突破策略")
        print("=" * 60)
        
        # 1. 数据获取（示例数据）
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
        data = pd.DataFrame({
            'close': prices,
            'high': prices * (1 + abs(np.random.randn(len(dates)) * 0.01)),
            'low': prices * (1 - abs(np.random.randn(len(dates)) * 0.01))
        }, index=dates)
        
        # 2. 计算ATR
        def calculate_atr(high, low, close, period=14):
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(period).mean()
            return atr
        
        data['atr'] = calculate_atr(data['high'], data['low'], data['close'])
        
        # 3. 计算动态通道
        channel_multiplier = 2.0
        data['upper_channel'] = data['close'] + channel_multiplier * data['atr']
        data['lower_channel'] = data['close'] - channel_multiplier * data['atr']
        
        # 4. 生成信号
        data['signal'] = 0
        data.loc[data['close'] > data['upper_channel'], 'signal'] = 1   # 买入
        data.loc[data['close'] < data['lower_channel'], 'signal'] = -1  # 卖出
        
        # 5. 可视化
        plt.figure(figsize=(15, 8))
        plt.plot(data.index, data['close'], label='Close Price', linewidth=2)
        plt.plot(data.index, data['upper_channel'], label='Upper Channel', 
                 linestyle='--', alpha=0.7)
        plt.plot(data.index, data['lower_channel'], label='Lower Channel', 
                 linestyle='--', alpha=0.7)
        
        # 标记买卖点
        buy_signals = data[data['signal'] == 1]
        sell_signals = data[data['signal'] == -1]
        plt.scatter(buy_signals.index, buy_signals['close'], 
                   marker='^', color='green', s=100, label='Buy', zorder=5)
        plt.scatter(sell_signals.index, sell_signals['close'], 
                   marker='v', color='red', s=100, label='Sell', zorder=5)
        
        plt.title('Dynamic ATR Channel Breakout Strategy', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('./atr_channel_example.png', dpi=150)
        print("[OK] 图表已保存: atr_channel_example.png")
        
        return data
    
    @staticmethod
    def example2_mean_reversion_rsi():
        """
        示例2: RSI极端值回归策略（波动率加权）
        
        适用市场: 震荡市场
        核心思想: RSI进入极端区域后，价格会回归均值
        """
        print("\n" + "=" * 60)
        print("示例2: RSI极端值回归策略（波动率加权）")
        print("=" * 60)
        
        # 1. 数据获取（示例数据）
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 1)  # 低波动
        data = pd.DataFrame({'close': prices}, index=dates)
        
        # 2. 计算RSI
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        
        data['rsi'] = calculate_rsi(data['close'])
        
        # 3. 计算波动率
        data['volatility'] = data['close'].pct_change().rolling(20).std()
        data['volatility_percentile'] = data['volatility'].rolling(252).apply(
            lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
        )
        
        # 4. 生成信号（波动率加权）
        data['position_size'] = 1.0  # 基础仓位
        data.loc[data['volatility_percentile'] > 0.8, 'position_size'] = 0.5  # 高波动减仓
        data.loc[data['volatility_percentile'] < 0.2, 'position_size'] = 1.5  # 低波动加仓
        
        data['signal'] = 0
        data.loc[data['rsi'] < 30, 'signal'] = 1 * data['position_size']   # 买入（加权）
        data.loc[data['rsi'] > 70, 'signal'] = -1 * data['position_size']  # 卖出（加权）
        
        print(f"[OK] RSI策略信号生成完成")
        print(f"  平均仓位: {data['position_size'].mean():.2f}")
        print(f"  买入信号数: {(data['signal'] > 0).sum()}")
        print(f"  卖出信号数: {(data['signal'] < 0).sum()}")
        
        return data
    
    @staticmethod
    def example3_pairs_trading_cointegration():
        """
        示例3: 跨品种价差协整回归策略
        
        适用市场: 相关性高的品种
        核心思想: 两个协整关系的品种，价差偏离后会回归
        """
        print("\n" + "=" * 60)
        print("示例3: 跨品种价差协整回归策略")
        print("=" * 60)
        
        # 1. 生成示例数据（两个协整关系的品种）
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        np.random.seed(42)
        base_price = 100 + np.cumsum(np.random.randn(len(dates)) * 1)
        noise = np.random.randn(len(dates)) * 5
        stock_a = base_price + noise
        stock_b = 0.8 * base_price + noise * 0.5 + 20
        
        data = pd.DataFrame({
            'stock_a': stock_a,
            'stock_b': stock_b
        }, index=dates)
        
        # 2. 计算协整关系（简化版，实际应使用Engle-Granger检验）
        data['spread'] = data['stock_a'] - 0.8 * data['stock_b']
        spread_mean = data['spread'].mean()
        spread_std = data['spread'].std()
        
        print(f"[OK] 协整关系计算完成")
        print(f"  价差均值: {spread_mean:.2f}")
        print(f"  价差标准差: {spread_std:.2f}")
        
        # 3. 生成交易信号
        data['z_score'] = (data['spread'] - spread_mean) / spread_std
        
        data['signal'] = 0
        # 价差偏高，做空价差（卖出A，买入B）
        data.loc[data['z_score'] > 2, 'signal'] = -1
        # 价差偏低，做多价差（买入A，卖出B）
        data.loc[data['z_score'] < -2, 'signal'] = 1
        # 价差回归，平仓
        data.loc[abs(data['z_score']) < 0.5, 'signal'] = 0
        
        # 4. 可视化
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # 子图1: 价格走势
        axes[0].plot(data.index, data['stock_a'], label='Stock A', linewidth=2)
        axes[0].plot(data.index, data['stock_b'], label='Stock B', linewidth=2)
        axes[0].set_title('Stock Prices', fontsize=14)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 子图2: 价差和Z得分
        axes[1].plot(data.index, data['spread'], label='Spread', linewidth=2)
        axes[1].axhline(y=spread_mean + 2*spread_std, color='red', 
                      linestyle='--', label='+2 STD')
        axes[1].axhline(y=spread_mean - 2*spread_std, color='green', 
                      linestyle='--', label='-2 STD')
        axes[1].axhline(y=spread_mean, color='black', linestyle='-', 
                      alpha=0.5, label='Mean')
        axes[1].set_title('Spread with Trading Bands', fontsize=14)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('./pairs_trading_example.png', dpi=150)
        print("[OK] 图表已保存: pairs_trading_example.png")
        
        return data
    
    @staticmethod
    def run_all_examples():
        """运行所有示例"""
        print("\n" + "=" * 60)
        print("量化策略实现示例集合")
        print("=" * 60)
        
        # 示例1: 动态ATR通道
        result1 = QuantitativeStrategyExamples.example1_dynamic_atr_channel()
        
        # 示例2: RSI均值回归
        result2 = QuantitativeStrategyExamples.example2_mean_reversion_rsi()
        
        # 示例3: 配对交易
        result3 = QuantitativeStrategyExamples.example3_pairs_trading_cointegration()
        
        print("\n" + "=" * 60)
        print("[OK] 所有示例运行完成！")
        print("=" * 60)
        print("\n生成的文件:")
        print("  - atr_channel_example.png")
        print("  - pairs_trading_example.png")
        print("\n下一步:")
        print("  1. 查看图表和信号")
        print("  2. 在历史数据上回测")
        print("  3. 优化参数")
        print("  4. 实盘验证")

def main():
    """主函数"""
    examples = QuantitativeStrategyExamples()
    examples.run_all_examples()

if __name__ == '__main__':
    main()
