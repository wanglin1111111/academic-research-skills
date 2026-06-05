#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据获取脚本 - 使用 AKShare
支持多周期、多市场数据获取
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import argparse
import sys

def fetch_a_stock_data(stock_code, start_date, end_date, frequency='daily'):
    """
    获取A股历史数据
    
    参数:
        stock_code: 股票代码（如：000001、600000）
        start_date: 开始日期（YYYYMMDD）
        end_date: 结束日期（YYYYMMDD）
        frequency: 数据频率（daily/weekly/monthly）
    
    返回:
        DataFrame: 包含日期、开盘价、最高价、最低价、收盘价、成交量等
    """
    try:
        # 根据频率选择不同的函数
        if frequency == 'daily':
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", 
                                     start_date=start_date, end_date=end_date, adjust="qfq")
        elif frequency == 'weekly':
            df = ak.stock_zh_a_hist(symbol=stock_code, period="weekly",
                                     start_date=start_date, end_date=end_date, adjust="qfq")
        elif frequency == 'monthly':
            df = ak.stock_zh_a_hist(symbol=stock_code, period="monthly",
                                     start_date=start_date, end_date=end_date, adjust="qfq")
        else:
            raise ValueError(f"不支持的频率: {frequency}")
        
        print(f"✓ 成功获取 {stock_code} 的{frequency}数据，共 {len(df)} 条记录")
        return df
    
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        return None

def fetch_hk_stock_data(stock_code, start_date, end_date):
    """
    获取港股历史数据
    
    参数:
        stock_code: 港股代码（如：00700、09988）
        start_date: 开始日期（YYYYMMDD）
        end_date: 结束日期（YYYYMMDD）
    """
    try:
        df = ak.stock_hk_hist(symbol=stock_code, period="daily",
                               start_date=start_date, end_date=end_date, adjust="qfq")
        print(f"✓ 成功获取港股 {stock_code} 的数据，共 {len(df)} 条记录")
        return df
    except Exception as e:
        print(f"✗ 获取港股数据失败: {e}")
        return None

def fetch_us_stock_data(symbol, start_date, end_date):
    """
    获取美股历史数据
    
    参数:
        symbol: 美股代码（如：AAPL、TSLA）
        start_date: 开始日期（YYYYMMDD）
        end_date: 结束日期（YYYYMMDD）
    """
    try:
        df = ak.stock_us_hist(symbol=symbol, period="daily",
                               start_date=start_date, end_date=end_date, adjust="qfq")
        print(f"✓ 成功获取美股 {symbol} 的数据，共 {len(df)} 条记录")
        return df
    except Exception as e:
        print(f"✗ 获取美股数据失败: {e}")
        return None

def capture_chart_screenshot(stock_code, output_path='./charts'):
    """
    捕获股票图表截图（用于缠论分析）
    
    参数:
        stock_code: 股票代码
        output_path: 截图保存路径
    """
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def capture():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # 打开腾讯财经页面
                url = f"https://gu.qq.com/{stock_code}"
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # 截图
                screenshot_path = f"{output_path}/{stock_code}_chart.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                
                await browser.close()
                print(f"✓ 图表截图已保存: {screenshot_path}")
        
        asyncio.run(capture())
    
    except Exception as e:
        print(f"✗ 截图失败: {e}")
        print("提示: 请确保已安装 playwright: pip install playwright && playwright install")

def main():
    parser = argparse.ArgumentParser(description='股票数据获取工具')
    parser.add_argument('--code', type=str, required=True, help='股票代码')
    parser.add_argument('--market', type=str, default='a-stock', 
                        choices=['a-stock', 'hk', 'us'], help='市场类型')
    parser.add_argument('--start', type=str, required=True, help='开始日期 (YYYYMMDD)')
    parser.add_argument('--end', type=str, required=True, help='结束日期 (YYYYMMDD)')
    parser.add_argument('--frequency', type=str, default='daily',
                        choices=['daily', 'weekly', 'monthly'], help='数据频率')
    parser.add_argument('--output', type=str, default='./data', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建输出目录
    import os
    os.makedirs(args.output, exist_ok=True)
    
    # 获取数据
    if args.market == 'a-stock':
        df = fetch_a_stock_data(args.code, args.start, args.end, args.frequency)
    elif args.market == 'hk':
        df = fetch_hk_stock_data(args.code, args.start, args.end)
    elif args.market == 'us':
        df = fetch_us_stock_data(args.code, args.start, args.end)
    
    # 保存数据
    if df is not None:
        output_file = f"{args.output}/{args.code}_{args.start}_{args.end}_{args.frequency}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✓ 数据已保存: {output_file}")

if __name__ == '__main__':
    # 检查依赖
    try:
        import akshare
    except ImportError:
        print("✗ 未安装 AKShare，请运行: pip install akshare")
        sys.exit(1)
    
    main()
