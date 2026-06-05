#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 辅助产品预演自动化 - 需求澄清工具
通过交互式问答，将模糊想法转化为清晰的产品目标
"""

import json
from pathlib import Path

class ProductGoalClarifier:
    """
    产品目标澄清器
    通过"杠精"式追问，澄清用户真实意图
    """
    
    def __init__(self):
        self.questions = self.load_questions()
        self.answers = {}
    
    def load_questions(self):
        """加载追问清单"""
        return {
            "target_users": [
                "你的目标用户是谁？（年龄、职业、痛点）",
                "他们目前如何解决这个痛点？",
                "为什么现有方案不够好？"
            ],
            "core_features": [
                "你心目中的产品核心功能有哪些？",
                "这些功能中，哪些是必须有的（P0），哪些是可以没有的（P1/P2）？",
                "你能举一个用户使用产品的具体场景吗？"
            ],
            "technical_constraints": [
                "你的预算是多少？（如果预算为0，告诉我）",
                "你有多少时间开发？",
                "你有技术背景吗？熟悉哪些技术栈？"
            ],
            "success_criteria": [
                "如何衡量产品成功？（定量指标，如 DAU、留存率）",
                "你希望用户使用产品后有什么感受？（定性反馈）",
                "如果产品失败了，可能的原因是什么？"
            ]
        }
    
    def start_clarification(self):
        """开始澄清流程"""
        print("=" * 60)
        print("AI 辅助产品预演 - 需求澄清工具")
        print("=" * 60)
        print("\n欢迎！我是你的 AI 产品助手。")
        print("我会像'杠精'一样追问，直到你的目标完全清晰。")
        print("请认真对待每个问题，你的回答将直接影响最终产品。\n")
        
        # 逐个维度澄清
        for dimension, question_list in self.questions.items():
            print("\n" + "=" * 60)
            print(f"维度: {self.get_dimension_name(dimension)}")
            print("=" * 60)
            
            self.answers[dimension] = []
            
            for i, question in enumerate(question_list, 1):
                print(f"\n问题 {i}: {question}")
                answer = input("你的回答: ").strip()
                self.answers[dimension].append({
                    "question": question,
                    "answer": answer
                })
        
        # 生成澄清报告
        self.generate_clarification_report()
    
    def get_dimension_name(self, key):
        """获取维度中文名"""
        names = {
            "target_users": "目标用户",
            "core_features": "核心功能",
            "technical_constraints": "技术约束",
            "success_criteria": "成功标准"
        }
        return names.get(key, key)
    
    def generate_clarification_report(self):
        """生成澄清报告"""
        print("\n" + "=" * 60)
        print("[OK] 澄清完成！正在生成报告...")
        print("=" * 60)
        
        report = f"""# 产品目标澄清报告

**生成时间**: {self.get_current_time()}

---

## 1. 目标用户

"""
        
        # 目标用户
        for qa in self.answers["target_users"]:
            report += f"**Q: {qa['question']}**\n\n"
            report += f"A: {qa['answer']}\n\n"
        
        report += """---

## 2. 核心功能

"""
        
        # 核心功能
        for qa in self.answers["core_features"]:
            report += f"**Q: {qa['question']}**\n\n"
            report += f"A: {qa['answer']}\n\n"
        
        report += """---

## 3. 技术约束

"""
        
        # 技术约束
        for qa in self.answers["technical_constraints"]:
            report += f"**Q: {qa['question']}**\n\n"
            report += f"A: {qa['answer']}\n\n"
        
        report += """---

## 4. 成功标准

"""
        
        # 成功标准
        for qa in self.answers["success_criteria"]:
            report += f"**Q: {qa['question']}**\n\n"
            report += f"A: {qa['answer']}\n\n"
        
        report += """---

## 5. 产品目标总结 (AI 生成)

基于以上澄清，你的产品目标可以总结为：

**产品定位**: [待 AI 生成]

**核心用户**: [待 AI 生成]

**MVP 功能**: [待 AI 生成]

**技术路线**: [待 AI 生成]

**下一步**: 将此报告发送给 AI 工具，生成完整需求规格文档。

---

**报告结束**

下一步：将此报告作为输入，让 AI 工具生成需求规格文档。
"""
        
        # 保存报告
        output_file = Path("./product_goal_clarification.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[OK] 报告已生成: {output_file}")
        print(f"\n下一步:")
        print(f"  1. 查看报告: {output_file}")
        print(f"  2. 补充/修改报告（如有需要）")
        print(f"  3. 将报告作为输入，让 AI 生成需求规格")
        print("=" * 60)
    
    def get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """主函数"""
    clarifier = ProductGoalClarifier()
    clarifier.start_clarification()

if __name__ == '__main__':
    main()
