import requests

BASE_URL = "https://openlibrary.org/search.json"
TIMEOUT = 10  # seconds
FIELDS = "title,author_name,first_publish_year,ratings_average"
LIMIT = 10  # maximum number of results to return

def print_books(books):
    '''Prints the list of books one by one as a dictionary. If the list is empty, it prints "No books found." If the list has 5 or fewer books, it prints all of them. If the list has more than 5 books, it prints only the first 5.'''
    num = len(books)
    if num ==0:
        print("No books found.")
    elif num <= 5:
        for book in books:
            print(book)
    else:
        for i in range(0, 5):
            print(books[i])

def get_books(subject, page):
    params = {
        "q": subject,
        "page": page,
        "limit": LIMIT,
        "fields": FIELDS
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        print_books(data['docs'])
        # return [book for book in data.get("docs", []) if all(field in book for field in FIELDS)]
    except requests.RequestException as e:
        print(f"Error fetching books: {e}")
        return []

get_books("love and laughter", 1)


