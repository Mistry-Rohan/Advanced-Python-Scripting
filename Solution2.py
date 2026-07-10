import json
from pathlib import Path

import requests


BASE_URL = "https://openlibrary.org/search.json"
TIMEOUT = 10
LIMIT = 10
FIELDS = "title,author_name,first_publish_year,ratings_average"
MAX_PAGES = 5
OFFLINE_FILE = (
    Path(__file__).resolve().parent.parent
    / "python_advance_assignment_assets"
    / "data"
    / "starter"
    / "offline_books.json"
)


def clean_book(book):
    """Return only the fields needed for this assignment."""
    authors = book.get("author_name") or []
    if isinstance(authors, list):
        author = ", ".join(authors)
    else:
        author = authors

    return {
        "title": book.get("title"),
        "author": author,
        "first_publish_year": book.get("first_publish_year"),
        "rating": book.get("ratings_average"),
    }


def load_offline_books():
    """Load the local sample used when the API is unavailable."""
    with open(OFFLINE_FILE, "r", encoding="utf-8") as file:
        books = json.load(file)
    return [clean_book(book) for book in books]


def get_books(subject, page):
    """Fetch one page of books from Open Library."""
    params = {
        "q": subject,
        "page": page,
        "limit": LIMIT,
        "fields": FIELDS,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return [clean_book(book) for book in data.get("docs", [])]
    except (requests.RequestException, ValueError) as error:
        print(f"Error fetching page {page}: {error}")
        if page == 1:
            print("Using offline sample for the first page.")
            return load_offline_books()
        return []


def full_load_books(subject, max_pages=MAX_PAGES):
    """Fetch books page by page until an empty page or page cap is reached."""
    all_books = []

    for page in range(1, max_pages + 1):
        books = get_books(subject, page)

        if not books:
            print(f"Stopping at page {page}: no books returned.")
            break

        print(f"Page {page}: fetched {len(books)} books")
        all_books.extend(books)

    return all_books


def get_watermark(books):
    """Find the newest publish year from the full load."""
    publish_years = [
        book["first_publish_year"]
        for book in books
        if book.get("first_publish_year") is not None
    ]

    if not publish_years:
        return None

    return max(publish_years)


def get_incremental_books(subject, watermark, max_pages=MAX_PAGES):
    """Fetch books again and keep only books newer than the watermark."""
    if watermark is None:
        return full_load_books(subject, max_pages)

    incremental_books = []

    for page in range(1, max_pages + 1):
        books = get_books(subject, page)

        if not books:
            print(f"Stopping incremental load at page {page}: no books returned.")
            break

        new_books = [
            book
            for book in books
            if book.get("first_publish_year") is not None
            and book["first_publish_year"] > watermark
        ]
        incremental_books.extend(new_books)

    return incremental_books


def print_sample(books, count=5):
    for book in books[:count]:
        print(book)


def main():
    subject = "python"

    print(f"Full load for subject: {subject}")
    full_load = full_load_books(subject)
    watermark = get_watermark(full_load)

    print(f"\nFull-load count: {len(full_load)}")
    print(f"Watermark newest publish year: {watermark}")
    print("\nSample full-load books:")
    print_sample(full_load)

    print("\nIncremental load using watermark")
    incremental_load = get_incremental_books(subject, watermark)
    print(f"Incremental count: {len(incremental_load)}")
    print("\nSample incremental books:")
    print_sample(incremental_load)


if __name__ == "__main__":
    main()
