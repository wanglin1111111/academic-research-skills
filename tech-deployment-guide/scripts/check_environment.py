#!/usr/bin/env python3
"""
Tech Deployment Guide - Check Environment Script
技术部署环境检查脚本示例
"""

import subprocess
import sys
import json
from typing import Dict, Optional


def check_command(cmd: str) -> Optional[str]:
    """
    检查命令是否可用
    
    Args:
        cmd: 命令名称
    
    Returns:
        版本信息或None
    """
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip() or result.stderr.strip()
        return None
    except Exception as e:
        return None


def check_environment() -> Dict:
    """
    检查系统环境
    
    Returns:
        环境检查结果
    """
    checks = {
        "node": "node --version",
        "npm": "npm --version",
        "python": "python --version",
        "python3": "python3 --version",
        "git": "git --version",
        "docker": "docker --version"
    }
    
    results = {}
    for name, cmd in checks.items():
        version = check_command(cmd)
        results[name] = {
            "installed": version is not None,
            "version": version
        }
    
    return results


def generate_report(results: Dict) -> str:
    """
    生成环境检查报告
    
    Args:
        results: 检查结果
    
    Returns:
        格式化报告
    """
    report = "# 环境检查报告\n\n"
    report += "## 检查结果\n\n"
    report += "| 工具 | 状态 | 版本 |\n"
    report += "|------|------|------|\n"
    
    for tool, info in results.items():
        status = "✅ 已安装" if info["installed"] else "❌ 未安装"
        version = info["version"] or "N/A"
        report += f"| {tool} | {status} | {version} |\n"
    
    return report


def main():
    """主函数"""
    print("正在检查系统环境...\n")
    
    results = check_environment()
    
    # JSON格式输出
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    # 生成报告
    print("\n" + "="*50)
    print(generate_report(results))


if __name__ == "__main__":
    main()
