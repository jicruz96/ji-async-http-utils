"""
Demo script for ji-async-utils aiohttp helpers.

Shows two flows against the public JSONPlaceholder API using iter_requests:
- Range-like fetch: posts 1..5 and print titles
- Custom transformer (on_result): parse JSON and print titles

Run:
    python demo.py
"""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from ji_async_http_utils.aiohttp import iter_requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


async def demo_range_like_iter_requests() -> None:
    print("\n=== iter_requests (range-like: posts 1..5) ===")
    async for post_id, data in iter_requests(
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


async def demo_iter_requests() -> None:
    print("\n=== iter_requests (items=[1..5], on_result JSON) ===")
    async for post_id, data in iter_requests(
        base_url=BASE_URL,
        items=list(range(1, 6)),
        max_concurrency=5,
        pbar="iter_requests",
        on_result=to_json,
        raise_on_error=True,
    ):
        title = str(data.get("title", "(no title)"))
        print(f"[{post_id}] {title}")


async def main() -> None:
    await demo_range_like_iter_requests()
    await demo_iter_requests()


if __name__ == "__main__":
    asyncio.run(main())
