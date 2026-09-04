# -*- coding: utf-8 -*-
"""BuyerPreference 值对象 + PreferenceStore 端口

买家长期偏好（"上次说不要塑料"）跨会话持久化的领域建模：
    - kind=like     正向偏好（如"喜欢小众设计"）
    - kind=dislike  负向偏好 / 黑名单（如"不要塑料材质"）
Infrastructure 提供 JSON 文件实现，生产可换 OpenSearch / PG。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone

VALID_KINDS = ("like", "dislike")


@dataclass(frozen=True)
class BuyerPreference:
    buyer_id: str
    kind: str  # like / dislike
    statement: str  # 一句话偏好陈述，如"不要塑料材质"
    created_at: str = ""

    def __post_init__(self) -> None:
        if self.kind not in VALID_KINDS:
            raise ValueError(f"BuyerPreference.kind 必须是 {VALID_KINDS}：{self.kind}")
        if not self.statement or not self.statement.strip():
            raise ValueError("BuyerPreference.statement required")
        if not self.created_at:
            object.__setattr__(self, "created_at", datetime.now(timezone.utc).isoformat())


class PreferenceStore(ABC):
    @abstractmethod
    async def append(self, preference: BuyerPreference) -> None:
        """追加偏好；同 buyer 同 statement 幂等去重。"""

    @abstractmethod
    async def list_by_buyer(self, buyer_id: str) -> list[BuyerPreference]:
        ...
