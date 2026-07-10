import asyncio
import time

import requests


BASE_URL = "https://openlibrary.org/search.json"
TIMEOUT = 15
ASYNC_GROUP_TIMEOUT = TIMEOUT + 5
SUBJECTS = [
    "python",
    "data engineering",
    "machine learning",
    "love and laughter",
    "science fiction",
    "history",
]


def fetch_result_count(subject):
    """Fetch the Open Library result count for one subject."""
    params = {
        "q": subject,
        "limit": 1,
        "fields": "key",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data.get("numFound", 0)
    except (requests.RequestException, ValueError) as error:
        print(f"Error fetching count for '{subject}': {error}")
        return 0


def fetch_counts_sync(subjects):
    """Fetch subject counts one at a time."""
    results = {}
    total_subjects = len(subjects)

    for index, subject in enumerate(subjects, start=1):
        print(f"[sync {index}/{total_subjects}] Starting '{subject}'")
        results[subject] = fetch_result_count(subject)

    return results


async def fetch_counts_async(subjects):
    """Fetch subject counts concurrently using threads for blocking requests."""
    print(f"[async] Starting {len(subjects)} requests together")
    tasks = [asyncio.to_thread(fetch_result_count, subject) for subject in subjects]
    counts = await asyncio.wait_for(
        asyncio.gather(*tasks),
        timeout=ASYNC_GROUP_TIMEOUT,
    )
    return dict(zip(subjects, counts))


def print_counts(title, counts):
    print(f"\n{title}")
    for subject, count in counts.items():
        print(f"{subject}: {count}")


def main():
    subject_count = len(SUBJECTS)
    print(f"Fetching result counts for {subject_count} subjects...")
    print(f"This is a fixed list, so each version runs exactly {subject_count} requests.")
    print(f"Each request has a {TIMEOUT}-second timeout.")

    sync_start = time.perf_counter()
    sync_counts = fetch_counts_sync(SUBJECTS)
    sync_time = time.perf_counter() - sync_start

    async_start = time.perf_counter()
    try:
        async_counts = asyncio.run(fetch_counts_async(SUBJECTS))
    except asyncio.TimeoutError:
        print(f"Async group stopped after {ASYNC_GROUP_TIMEOUT} seconds.")
        async_counts = {}
    async_time = time.perf_counter() - async_start

    print_counts("Sync counts", sync_counts)
    print_counts("Async counts", async_counts)

    print("\nTimings")
    print(f"Sync time: {sync_time:.2f} seconds")
    print(f"Async time: {async_time:.2f} seconds")

    if async_time < sync_time:
        speedup = sync_time / async_time
        print(f"Async was {speedup:.2f}x faster.")
    else:
        print("Async was not faster in this run.")


if __name__ == "__main__":
    main()
