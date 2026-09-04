# -*- coding: utf-8 -*-
"""OpenAIEmbeddingClient

OpenAI 兼容 /v1/embeddings 客户端（httpx 直连，不引入 openai SDK 的 embedding 封装，
便于对接任意兼容网关）。模型默认 text-embedding-v4。
"""
from __future__ import annotations

import httpx

from app.domain.catalog.ports.retrieval_ports import EmbeddingClient
from app.infrastructure.settings import Settings


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(self, settings: Settings, timeout_seconds: float = 15.0) -> None:
        self._base_url = settings.embedding_base_url.rstrip("/")
        self._api_key = settings.embedding_api_key
        self._model = settings.embedding_model
        self._timeout = timeout_seconds

    async def embed(self, text: str) -> list[float]:
        return (await self.embed_batch([text]))[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/embeddings",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"model": self._model, "input": texts},
            )
            response.raise_for_status()
            body = response.json()
        if "data" not in body:
            raise RuntimeError(f"embedding 响应异常：{str(body)[:200]}")
        # 按 index 回位，避免网关乱序
        ordered = sorted(body["data"], key=lambda item: item["index"])
        return [item["embedding"] for item in ordered]
