from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parent / "sales.csv"
CHUNK_SIZE = 50_000


def stream_revenue_by_genre():
    """Read sales.csv in chunks and total revenue by genre."""
    revenue_by_genre = {}
    total_rows = 0

    for chunk_number, chunk in enumerate(
        pd.read_csv(DATA_FILE, chunksize=CHUNK_SIZE),
        start=1,
    ):
        total_rows += len(chunk)
        chunk["revenue"] = chunk["price"] * chunk["quantity"]
        chunk_revenue = chunk.groupby("genre")["revenue"].sum()

        for genre, revenue in chunk_revenue.items():
            revenue_by_genre[genre] = revenue_by_genre.get(genre, 0) + revenue

        print(f"Processed chunk {chunk_number}: {len(chunk)} rows")

    return revenue_by_genre, total_rows


def optimize_chunk_memory(chunk):
    """Shrink one DataFrame chunk by using smaller and categorical dtypes."""
    optimized = chunk.copy()

    optimized["price"] = optimized["price"].astype("float32")
    optimized["rating"] = optimized["rating"].astype("float32")
    optimized["genre"] = optimized["genre"].astype("category")
    optimized["city"] = optimized["city"].astype("category")
    optimized["payment_type"] = optimized["payment_type"].astype("category")

    return optimized


def memory_in_mb(dataframe):
    """Return deep memory usage in MB."""
    return dataframe.memory_usage(deep=True).sum() / (1024 * 1024)


def print_revenue_by_genre(revenue_by_genre):
    print("\nTotal revenue by genre")
    for genre, revenue in sorted(revenue_by_genre.items()):
        print(f"{genre}: {revenue:,.2f}")


def main():
    print(f"Streaming file: {DATA_FILE.name}")
    print(f"Chunk size: {CHUNK_SIZE:,} rows")

    revenue_by_genre, total_rows = stream_revenue_by_genre()
    print(f"\nTotal rows processed: {total_rows:,}")
    print_revenue_by_genre(revenue_by_genre)

    first_chunk = next(pd.read_csv(DATA_FILE, chunksize=CHUNK_SIZE))
    before_memory = memory_in_mb(first_chunk)
    optimized_chunk = optimize_chunk_memory(first_chunk)
    after_memory = memory_in_mb(optimized_chunk)
    reduction = before_memory - after_memory
    reduction_percent = (reduction / before_memory) * 100

    print("\nMemory optimization on one chunk")
    print(f"Before: {before_memory:.2f} MB")
    print(f"After: {after_memory:.2f} MB")
    print(f"Reduction: {reduction:.2f} MB ({reduction_percent:.2f}%)")


if __name__ == "__main__":
    main()
