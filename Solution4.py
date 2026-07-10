import csv
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent
    / "sales.csv"
)
SCORE_ITERATIONS = 5_000_000


def load_genres():
    """Read the unique genres from Booknest sales data."""
    genres = set()

    with open(DATA_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            genres.add(row["genre"])

    return sorted(genres)


def score_genre(genre):
    """Run a deterministic CPU-heavy scoring job for one genre."""
    genre_seed = sum((index + 1) * ord(char) for index, char in enumerate(genre))
    score = 0

    for number in range(1, SCORE_ITERATIONS + 1):
        score += ((number * genre_seed) % 97) * ((number + genre_seed) % 89)

    return genre, score


def score_genres_serial(genres):
    """Run the CPU-heavy scoring job one genre at a time."""
    return [score_genre(genre) for genre in genres]


def score_genres_parallel(genres):
    """Run the CPU-heavy scoring job across CPU cores."""
    with ProcessPoolExecutor() as pool:
        return list(pool.map(score_genre, genres))


def print_results(results):
    for genre, score in results:
        print(f"{genre}: {score}")


def main():
    genres = load_genres()
    core_count = os.cpu_count() or 1

    print(f"Machine core count: {core_count}")
    print(f"Genres to score: {len(genres)}")
    print(f"Score iterations per genre: {SCORE_ITERATIONS:,}")
    print(f"Genres: {', '.join(genres)}")

    serial_start = time.perf_counter()
    serial_results = score_genres_serial(genres)
    serial_time = time.perf_counter() - serial_start

    parallel_start = time.perf_counter()
    parallel_results = score_genres_parallel(genres)
    parallel_time = time.perf_counter() - parallel_start

    results_match = serial_results == parallel_results

    print("\nSerial results")
    print_results(serial_results)

    print("\nParallel results")
    print_results(parallel_results)

    print("\nTimings")
    print(f"Serial time: {serial_time:.2f} seconds")
    print(f"Parallel time: {parallel_time:.2f} seconds")
    print(f"Results match: {results_match}")

    if parallel_time < serial_time:
        speedup = serial_time / parallel_time
        print(f"Parallel was {speedup:.2f}x faster.")
    else:
        print("Parallel was not faster in this run.")


if __name__ == "__main__":
    main()
