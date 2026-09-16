import asyncio
import httpx
import time
import random

URL = "http://localhost:8000/api/v1/predict"

HEADERS = {
    "X-API-Key": "mysecretkey"
}


# 🔥 Generate random input every request
def generate_random_data():
    return {
        "sepal_length": random.uniform(4.0, 7.0),
        "sepal_width": random.uniform(2.0, 4.5),
        "petal_length": random.uniform(1.0, 6.0),
        "petal_width": random.uniform(0.1, 2.5)
    }


async def send_request(client):
    try:
        data = generate_random_data()  # 👈 RANDOM DATA HERE

        response = await client.post(
            URL,
            json=data,
            headers=HEADERS
        )
        return response.status_code

    except Exception as e:
        print("Error:", e)
        return 500


async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:

        # 🔥 100 concurrent requests
        tasks = [send_request(client) for _ in range(100)]

        start = time.time()

        results = await asyncio.gather(*tasks)

        end = time.time()

        print("\n⏱ Time taken:", round(end - start, 2), "seconds")
        print("✅ Success:", results.count(200))
        print("❌ Failed:", len(results) - results.count(200))


if __name__ == "__main__":
    asyncio.run(main())