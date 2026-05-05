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
                "user_query": "give me price",
                "ai_response": "Thank you for your query. Could you please specify which product you are interested in—boilers, controllers, or any specific model or accessory? This will help me provide you with the accurate price information."
            }
        ],
        "user_query": "controllers"
        }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            # "http://127.0.0.1:8000/api/ai/chatbot",
            "https://arronwh.onrender.com/api/ai/chatbot",
            json=payload
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    print(line, flush=True)

asyncio.run(main())