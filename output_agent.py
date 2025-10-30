import os
import json
from datetime import datetime
from typing import Dict, Any
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core.memory import ListMemory
from autogen_core.tools import FunctionTool


def save_report(
        chart_data: str = "",
        analysis_content: str = "",
        stock_data: str = "",
        output_format: str = "html"
) -> str:
    """
    将图表和分析内容保存到文件的工具函数

    Args:
        chart_data: 图表数据或图表文件路径
        analysis_content: 分析评论内容
        stock_data: 股票数据
        output_format: 输出格式 (markdown/html)

    Returns:
        str: 保存的文件路径
    """

    # 创建输出目录
    output_dir = "./output/reports"
    os.makedirs(output_dir, exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stock_analysis_report_{timestamp}"

    if output_format == "html":
        filename += ".html"
        filepath = os.path.join(output_dir, filename)

        # 生成HTML报告
        html_content = generate_html_report(stock_data, chart_data, analysis_content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

    else:  # markdown格式
        filename += ".md"
        filepath = os.path.join(output_dir, filename)

        # 生成Markdown报告
        md_content = generate_markdown_report(stock_data, chart_data, analysis_content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

    print(f"报告已保存到: {filepath}")
    return filepath


def generate_markdown_report(stock_data: str, chart_data: str, analysis: str) -> str:
    """生成Markdown格式的报告"""

    # 解析数据（在实际应用中，这些数据会是结构化的）
    stock_info = extract_stock_info(stock_data)
    chart_info = extract_chart_info(chart_data)
    analysis_info = extract_analysis_info(analysis)

    report = f"""# 股票分析报告

## 股票信息
- **股票代码**: {stock_info.get('symbol', 'AAPL')}
- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **数据周期**: {stock_info.get('period', '2024年1月')}

## 价格数据
{stock_info.get('data_summary', '')}

## 图表信息
{chart_info.get('description', '')}

**图表文件**: `{chart_info.get('path', '')}`

## 专业分析
### 走势分析
{analysis_info.get('analysis', '')}

### 投资建议
{analysis_info.get('recommendation', '')}

## 总结
本报告由多智能体系统自动生成，包含股票数据收集、图表制作和专业分析三个主要环节。

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return report


def generate_html_report(stock_data: str, chart_data: str, analysis: str) -> str:
    """生成HTML格式的报告"""

    stock_info = extract_stock_info(stock_data)
    chart_info = extract_chart_info(chart_data)
    analysis_info = extract_analysis_info(analysis)

    html_report = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票分析报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #2c3e50; border-left: 4px solid #3498db; padding-left: 10px; }}
        .info-item {{ margin: 10px 0; }}
        .analysis {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
        .recommendation {{ background: #e8f5e8; padding: 15px; border-radius: 5px; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>股票分析报告</h1>
        <p>自动生成的专业股票分析报告</p>
    </div>

    <div class="section">
        <h2>股票信息</h2>
        <div class="info-item"><strong>股票代码:</strong> {stock_info.get('symbol', 'AAPL')}</div>
        <div class="info-item"><strong>分析时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        <div class="info-item"><strong>数据周期:</strong> {stock_info.get('period', '2024年1月')}</div>
    </div>

    <div class="section">
        <h2>价格数据</h2>
        <pre>{stock_info.get('data_summary', '')}</pre>
    </div>

    <div class="section">
        <h2>图表信息</h2>
        <p>{chart_info.get('description', '')}</p>
        <p><strong>图表文件:</strong> <code>{chart_info.get('path', '')}</code></p>
    </div>

    <div class="section">
        <h2>专业分析</h2>
        <div class="analysis">
            <h3>走势分析</h3>
            <p>{analysis_info.get('analysis', '')}</p>
        </div>
        <div class="recommendation">
            <h3>投资建议</h3>
            <p>{analysis_info.get('recommendation', '')}</p>
        </div>
    </div>

    <div class="footer">
        <p>本报告由多智能体系统自动生成</p>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>"""
    return html_report


def extract_stock_info(stock_data: str) -> Dict[str, Any]:
    """从股票数据中提取信息"""
    try:
        if isinstance(stock_data, str) and stock_data.strip():
            # 尝试解析JSON格式的股票数据
            if stock_data.startswith('{'):
                data = json.loads(stock_data)
                return {
                    'symbol': data.get('stock', 'AAPL'),
                    'period': '自定义周期',
                    'data_summary': f"包含{data.get('prices', 5)}个价格数据点"
                }
    except:
        pass

    return {
        'symbol': 'AAPL',
        'period': '2024年1月',
        'data_summary': '模拟股票价格数据'
    }


def extract_chart_info(chart_data: str) -> Dict[str, Any]:
    """从图表数据中提取信息"""
    if isinstance(chart_data, str) and chart_data.strip():
        if chart_data.startswith('{'):
            try:
                data = json.loads(chart_data)
                return {
                    'path': data.get('chart_path', 'output/chart.png'),
                    'description': data.get('chart_description', '股票价格走势图')
                }
            except:
                pass

    return {
        'path': 'output/stock_chart.png',
        'description': 'AAPL股票价格走势折线图'
    }


def extract_analysis_info(analysis: str) -> Dict[str, Any]:
    """从分析内容中提取信息"""
    if isinstance(analysis, str) and analysis.strip():
        if analysis.startswith('{'):
            try:
                data = json.loads(analysis)
                return {
                    'analysis': data.get('analysis', '专业的股票走势分析'),
                    'recommendation': data.get('recommendation', '投资建议')
                }
            except:
                pass

    return {
        'analysis': analysis if analysis else '基于价格数据的专业分析',
        'recommendation': '请根据个人风险承受能力做出投资决策'
    }


def create_output_agent(llm_model: OpenAIChatCompletionClient, memory: ListMemory) -> AssistantAgent:
    """
    创建输出智能体

    Args:
        llm_model: 语言模型实例
        memory: 团队使用的记忆实例

    Returns:
        OutputAgent实例
    """
    # 工具函数映射（用于AutoGen注册）
    save_report_tool = FunctionTool(save_report, description="根据已有的分析结果，输出分析内容到文件中。")

    output_agent = AssistantAgent(
        name="OutputAgent",
        system_message="""你是一个专业的报告输出智能体。你的职责是：

        1. 收集整理所有智能体的输出结果
        2. 调用save_report工具将内容保存到文件
        3. 确保报告的完整性和格式正确
        4. 支持多种输出格式（markdown/html）

        当收到其他智能体的完整输出后，你应该：
        - 确认所有必要信息都已收集（股票数据、图表信息、分析内容）
        - 调用save_report工具
        - 返回生成的文件路径

        重要：确保在调用工具时提供以JSON格式组织的，清晰的结构化信息，基于以下标准：
        1.股票信息中至少包含股票代码（标记为stock）、数据时间区间（标记为period）、制图使用到的股价数据点个数（标记为prices），以及其他必要信息。
        2.图表信息中至少包含图表的路径（标记为chart_path）。
        3.分析信息中包含之前智能体输出的股票分析结果。
        """,
        model_client=llm_model,
        tools=[save_report_tool],
        memory=[memory]
    )

    return output_agent
