# -*- coding: utf-8 -*-
"""task_dispatch 工具

SubAgent as Tool 的调度工具——MainAgent 调它意味着"派一个专家子 Agent 去执行这段 demands"。
2.0 库级没有 subagent 原语，用 FunctionTool 包装子 Agent 实现同等语义。

子 Agent 每次调度新建实例（独立 AgentState = 上下文隔离），只把最终结论回传给 MainAgent，
中间的工具调用过程由业务工具自身通过 EventBus 直接上报前端。

真并行：本工具注册为 is_concurrency_safe，主 Agent 同一轮发起的多个 task_dispatch
会被 2.0 批量 asyncio.gather 并发执行；agent.dispatch 事件带 started_at，
完成时另发 tool.result 带 finished_at/elapsed_ms，可从事件流直接判定时间重叠。

注意：本模块不能用 `from __future__ import annotations`（AgentScope schema 生成依赖运行时注解）。
"""
import time
from datetime import datetime, timezone
from typing import Literal

from agentscope.message import TextBlock, ToolResultState, UserMsg
from agentscope.tool import ToolChunk

from app.application.agents.search_agent import SearchAgentFactory
from app.application.agents.trade_agent import TradeAgentFactory
from app.infrastructure.context import ShoppingContext
from app.infrastructure.eventbus import TradeEventBus


def build_task_dispatch_tool(
    search_factory: SearchAgentFactory,
    trade_factory: TradeAgentFactory,
    bus: TradeEventBus,
):
    async def task_dispatch(
        subagent_type: Literal["search_agent", "trade_agent"],
        demands: str,
    ) -> ToolChunk:
        """调度专家子代理执行子任务，返回子代理的结论（JSON 字符串）。

        仅当子任务满足"可并行 / 需要上下文隔离 / 内部调用链较深"任一条件时使用；
        简单的单步工具调用应自己直接调业务工具完成。
        多个彼此独立的子任务请在同一轮一次性发起多个本工具调用，系统会并发执行。

        Args:
            subagent_type (`str`):
                子代理类型："search_agent"（跨境商品检索专家）或 "trade_agent"（下单交易专家）。
            demands (`str`):
                自包含的自然语言指令，必须包含子代理完成任务所需的全部上下文
                （买家偏好、预算、product_id/sku_id、收货地址等），子代理看不到主对话历史。
        """
        session_id = ShoppingContext.current_session_id()
        started_at = datetime.now(timezone.utc).isoformat()
        started_monotonic = time.monotonic()
        bus.publish(
            session_id,
            "agent.dispatch",
            {"agent": subagent_type, "demands": demands, "started_at": started_at},
        )

        if subagent_type == "search_agent":
            worker = search_factory.build()
        elif subagent_type == "trade_agent":
            worker = trade_factory.build()
        else:
            return ToolChunk(
                content=[TextBlock(type="text", text=f"[error] 未知 subagent_type：{subagent_type}")],
                state=ToolResultState.ERROR,
            )

        reply = await worker.reply(UserMsg("commerce_concierge", demands))
        output = reply.get_text_content() or ""
        bus.publish(
            session_id,
            "tool.result",
            {
                "tool": "task_dispatch",
                "agent": subagent_type,
                "started_at": started_at,
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "elapsed_ms": round((time.monotonic() - started_monotonic) * 1000),
            },
        )
        return ToolChunk(
            content=[TextBlock(type="text", text=output)],
            state=ToolResultState.SUCCESS,
        )

    return task_dispatch
