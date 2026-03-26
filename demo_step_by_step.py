#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

# 导入刚才重构的极简通用引擎
from meta_skill_engine import WorkflowEngine

# ==========================================
# 第一步：定义数据契约 (Data Contracts)
# 这就是他们交流的“标准普通话”
# ==========================================
@dataclass
class TopicRequest:
    """初始输入：告诉系统要搜什么"""
    keyword: str

@dataclass
class NewsItem:
    """一条新闻的结构"""
    title: str
    heat_score: int  # 热度分数

@dataclass
class SavedRecord:
    """技能 A (Storage) 保存成功后的记录"""
    record_id: str
    saved_title: str
    heat_score: int

@dataclass
class TrendChart:
    """技能 C (Chart) 生成的图表结果"""
    chart_url: str


# ==========================================
# 第二步：编写独立的技能 (Skills)
# 它们互相完全不知道对方的存在！
# ==========================================

class SkillB_SpotNews:
    """技能 B：搜集热点新闻"""
    name = "Spot News Collector"
    
    # 【核心】：声明我吃什么，拉什么
    input_signature = TopicRequest
    output_signature = List[NewsItem] # 注意这里，输出的是一个列表

    def run(self, data: TopicRequest) -> List[NewsItem]:
        print(f"  [Skill B] 正在全网搜集 '{data.keyword}' 的热点新闻...")
        # 模拟搜到了两条新闻
        return [
            NewsItem(title="AI Agent 爆发", heat_score=95),
            NewsItem(title="Python 3.14 发布", heat_score=88)
        ]

class SkillA_Storage:
    """技能 A：保存数据到数据库"""
    name = "Database Storage"
    
    # 【核心】：声明我吃什么，拉什么
    input_signature = NewsItem
    output_signature = SavedRecord

    def run(self, data: NewsItem) -> SavedRecord:
        print(f"  [Skill A] 正在将 '{data.title}' (热度:{data.heat_score}) 存入数据库...")
        # 模拟保存动作
        record_id = f"db_id_{data.heat_score}"
        return SavedRecord(record_id=record_id, saved_title=data.title, heat_score=data.heat_score)

class SkillC_TrendChart:
    """技能 C：生成趋势图表"""
    name = "Trend Chart Generator"
    
    # 【核心】：它接收“保存记录的列表”来画图
    # 注意：引擎在处理完 Skill A 后，会把多个 SavedRecord 收集成一个 List[SavedRecord]
    input_signature = List[SavedRecord]
    output_signature = TrendChart

    def run(self, data: List[SavedRecord]) -> TrendChart:
        print(f"  [Skill C] 收到 {len(data)} 条数据，正在生成趋势分析图表...")
        # 模拟画图
        url = "/var/www/html/charts/trend_latest.png"
        print(f"  [Skill C] 图表生成完毕！访问地址: {url}")
        return TrendChart(chart_url=url)


# ==========================================
# 第三步：如何连接它们？ (The Glue)
# ==========================================
if __name__ == "__main__":
    print("========================================")
    print("场景 1：只有 B (搜集) 和 A (保存)")
    print("========================================")
    engine_v1 = WorkflowEngine()
    
    # 把技能注册进引擎（顺序无所谓）
    engine_v1.register(SkillA_Storage())
    engine_v1.register(SkillB_SpotNews())
    
    # 丢给它初始指令，引擎会自动计算路径：TopicRequest -> (Skill B) -> List[NewsItem] -> (引擎自动解包并循环) -> (Skill A) -> List[SavedRecord] -> 结束
    engine_v1.execute(TopicRequest(keyword="Tech"))
    
    print("\n\n========================================")
    print("场景 2：新需求来了！在保存后，加上 C (画图表)")
    print("========================================")
    engine_v2 = WorkflowEngine()
    
    # 原来的 A 和 B 原封不动，直接加进来
    engine_v2.register(SkillA_Storage())
    engine_v2.register(SkillB_SpotNews())
    # 唯一的变化：把新买的技能 C 也注册进来
    engine_v2.register(SkillC_TrendChart())
    
    # 再次丢给它初始指令，引擎会自动计算出新路径：
    # TopicRequest -> (Skill B) -> List[NewsItem] -> (引擎解包) -> (Skill A) -> List[SavedRecord] -> (Skill C 发现自己能吃这个列表) -> (Skill C) -> TrendChart -> 结束
    final_result = engine_v2.execute(TopicRequest(keyword="AI"))
    
    print("\n🎉 最终拿到的对象:", type(final_result).__name__)
