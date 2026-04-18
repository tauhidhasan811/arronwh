# import asyncio
# import httpx

# async def main():
#     async with httpx.AsyncClient(timeout=None) as client:
#         async with client.stream("GET", "http://127.0.0.1:8000/api/get") as response:
#             async for line in response.aiter_lines():
#                 print(line, flush=True)

# asyncio.run(main())

import asyncio
import httpx

async def main():
    payload = {
        "previous_chat": [
            {
                "user_query": "string",
                "ai_response": "string"
            }
        ],
        "user_query": "give the price"
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            "http://127.0.0.1:8000/api/ai/chatbot",
            json=payload
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    print(line, flush=True)

asyncio.run(main())