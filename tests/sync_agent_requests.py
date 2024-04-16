import time

import requests

CHATBOT_URL = "http://localhost:8000/course-rag-agent"

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
outputs = [requests.post(CHATBOT_URL, json=data) for data in request_bodies]
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")
