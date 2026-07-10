# Booknest Session 5 Solutions

Run all commands from this folder:

```bash
cd "Solution_Week3_Session5"
```

## Setup

Install the required libraries if they are not already installed:

```bash
pip install requests pandas pytest
```

If using WSL with the existing virtual environment:

```bash
source .venv/bin/activate
```

## Solution 1: API Request

Fetch and print a few books from the Open Library API:

```bash
python Solution1.py
```

In WSL:

```bash
python3 Solution1.py
```

## Solution 2: Pagination and Incremental Load

Run a full load across pages, calculate the newest publish year watermark, and show an incremental load:

```bash
python Solution2.py
```

In WSL:

```bash
python3 Solution2.py
```

## Solution 3: Sync Versus Async

Compare fetching result counts one at a time with fetching them concurrently using `asyncio.gather` and `asyncio.to_thread`:

```bash
python Solution3.py
```

In WSL:

```bash
python3 Solution3.py
```

## Solution 4: Serial Versus Parallel

Run a CPU-heavy genre scoring job serially and with `ProcessPoolExecutor`:

```bash
python Solution4.py
```

In WSL:

```bash
python3 Solution4.py
```

This script expects `sales.csv` to be in the same folder as `Solution4.py`.

## Solution 5: File Streaming and Memory

Stream `sales.csv` in chunks, total revenue by genre, and compare memory usage before and after dtype optimization on one chunk:

```bash
python Solution5.py
```

In WSL:

```bash
python3 Solution5.py
```

This script expects `sales.csv` to be in the same folder as `Solution5.py`.

## Solution 6: Pytest Tests

Run the pricing tests from the test folder:

```bash
cd question6_tests
pytest
```

In WSL:

```bash
cd question6_tests
python3 -m pytest
```

To return to the solutions folder:

```bash
cd ..
```
