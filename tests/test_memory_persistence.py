# -*- coding: utf-8 -*-
"""二期记忆与持久化单测：偏好 Store / 会话状态 round-trip。"""
import pytest

from agentscope.message import AssistantMsg, UserMsg
from agentscope.state import AgentState

from app.domain.buyer.preference import BuyerPreference
from app.infrastructure.persistence.json_file_stores import (
    JsonFilePreferenceStore,
    JsonFileSessionStore,
)


class TestPreferenceStore:
    async def test_append_and_list(self, tmp_path):
        store = JsonFilePreferenceStore(tmp_path)
        await store.append(BuyerPreference(buyer_id="b1", kind="dislike", statement="不要塑料材质"))
        await store.append(BuyerPreference(buyer_id="b1", kind="like", statement="喜欢小众设计"))

        preferences = await store.list_by_buyer("b1")
        assert len(preferences) == 2
        assert preferences[0].statement == "不要塑料材质"

    async def test_dedupe_same_statement(self, tmp_path):
        store = JsonFilePreferenceStore(tmp_path)
        for _ in range(3):
            await store.append(BuyerPreference(buyer_id="b1", kind="dislike", statement="不要塑料材质"))
        assert len(await store.list_by_buyer("b1")) == 1

    async def test_buyers_are_isolated(self, tmp_path):
        store = JsonFilePreferenceStore(tmp_path)
        await store.append(BuyerPreference(buyer_id="b1", kind="like", statement="喜欢小众设计"))
        assert await store.list_by_buyer("b2") == []

    async def test_survives_reinstantiation(self, tmp_path):
        store = JsonFilePreferenceStore(tmp_path)
        await store.append(BuyerPreference(buyer_id="b1", kind="dislike", statement="不要塑料材质"))
        # 重新实例化（模拟服务重启）后仍可读
        reopened = JsonFilePreferenceStore(tmp_path)
        preferences = await reopened.list_by_buyer("b1")
        assert preferences[0].statement == "不要塑料材质"

    def test_invalid_kind_rejected(self):
        with pytest.raises(ValueError, match="kind"):
            BuyerPreference(buyer_id="b1", kind="hate", statement="x")


class TestSessionPersistence:
    async def test_agent_state_roundtrip_via_store(self, tmp_path):
        store = JsonFileSessionStore(tmp_path)
        state = AgentState(session_id="s1")
        state.context.append(UserMsg("buyer-001", "我想买露营灯"))
        state.context.append(AssistantMsg("concierge", "好的，已为你检索"))

        await store.save("s1", state.model_dump_json())
        restored = AgentState.model_validate_json(await store.load("s1"))
        assert len(restored.context) == 2
        assert restored.context[0].get_text_content() == "我想买露营灯"

    async def test_load_missing_session_returns_none(self, tmp_path):
        store = JsonFileSessionStore(tmp_path)
        assert await store.load("nonexistent") is None

    async def test_session_id_sanitized(self, tmp_path):
        store = JsonFileSessionStore(tmp_path)
        await store.save("../evil", "{}")
        # 路径穿越字符被清洗，文件落在 sessions/ 目录内
        files = list((tmp_path / "sessions").iterdir())
        assert len(files) == 1
        assert files[0].parent == tmp_path / "sessions"
