"""
Demo script for ji-async-utils aiohttp helpers.

Shows two flows against the public JSONPlaceholder API using iter_responses:
- Range-like fetch: posts 1..5 and print titles
- Custom transformer (on_result): parse JSON and print titles

Run:
    python demo.py
"""

from __future__ import annotations

import asyncio
from typing import Any
import aiohttp
from ji_async_http_utils.aiohttp import iter_responses

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


async def demo_range_like_iter_responses() -> None:
    print("\n=== iter_responses (range-like: posts 1..5) ===")
    async for post_id, data in iter_responses(
        base_url=BASE_URL,
        items=range(1, 6),
        max_concurrency=5,
        pbar="Range",
        raise_on_error=True,
    ):
        title = str(data.get("title", "(no title)"))
        print(f"[{post_id}] {title}")


async def to_json(_: int, resp: aiohttp.ClientResponse) -> dict[str, Any]:
    async with resp:
        return await resp.json()


async def demo_iter_responses() -> None:
    print("\n=== iter_responses (items=[1..5], on_result JSON) ===")
    async for post_id, data in iter_responses(
        base_url=BASE_URL,
        items=list(range(1, 6)),
        max_concurrency=5,
        pbar="iter_responses",
        on_result=to_json,
        raise_on_error=True,
    ):
        title = str(data.get("title", "(no title)"))
        print(f"[{post_id}] {title}")


async def main() -> None:
    await demo_range_like_iter_responses()
    await demo_iter_responses()


if __name__ == "__main__":
    asyncio.run(main())
