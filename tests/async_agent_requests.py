import asyncio
import time

import httpx

CHATBOT_URL = "http://localhost:8000/course-rag-agent"


async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response


async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    outputs = [r.json()["output"] for r in responses]
    return outputs


questions = [
    "Suitable for beginner or advanced users ?",
    "Can I learn at my own pace?",
    "What type of assignment do you give ?",
    "What are the pre-requirement for this course ?",
    "How long does this course take to complete ?",
    "How much does the course cost ?",
    "How is the doubt support ?",
    "Does this course offer placement opportunities also ?",
    "How is the course different from other platform courses ?",
    "Is there any money back guarantee if I did not like the course ?",
    "Is this course relevant in todays market ?",
    "Is good DSA a prerequisite for this course ?",
    "How much I can make after completing this course ?",
    "Can I pay in EMI for this course ?",
    "Does this course offer financial aid for under-previleged people ?",
    "Does this course offer any certificate ?",
    "Where can I get testimonials for this course ?",
    "Who is the mentor for this course ?",
    "Is it an online or offline course ?",
]

request_bodies = [{"text": q} for q in questions]

start_time = time.perf_counter()
outputs = asyncio.run(make_bulk_requests(CHATBOT_URL, request_bodies))
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")
