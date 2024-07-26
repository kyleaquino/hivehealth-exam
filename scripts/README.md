### `scripts/bgg_compare_users.py`

This script compares the top 100 games of two Board Game Geek users and calculates a similarity score based on their collections.

```python
import argparse
from services.bgg_service import BGGCollectionItem

def get_top_games(username, own=1, rated=1):
    try:
        collection_items = BGGCollectionItem.fetch_collection(
            username, own=own, rated=rated
        )

        return {item.name for item in collection_items[:100]}

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

def calculate_similarity_score(games1: set, games2: set):
    if not games1 or not games2:
        return 0

    common_games = games1.intersection(games2)
    total_games = games1.union(games2)

    return len(common_games) / len(total_games)

def main(user1, user2):
    similarity_score = calculate_similarity_score(
        get_top_games(user1),
        get_top_games(user2),
    )
    print(f"Similarity Score between {user1} and {user2}: {similarity_score:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two BGG users' game tastes.")
    parser.add_argument("user1", type=str, help="BGG username of the first user.")
    parser.add_argument("user2", type=str, help="BGG username of the second user.")

    args = parser.parse_args()
    main(args.user1, args.user2)
```

### Running the Script

To run the script from the command line, use the following command:

```bash
python -m scripts.bgg_compare_users <username_1> <username_2>
```

### Explanation

1. **Imports**:
   - `argparse` for command-line argument parsing.
   - `BGGCollectionItem` from `services.bgg_service` to fetch user collections.

2. **Functions**:
   - `get_top_games(username, own=1, rated=1)`: Fetches the top 100 games from a user's collection and returns them as a set.
   - `calculate_similarity_score(games1: set, games2: set)`: Calculates the similarity score between two sets of games based on the intersection and union of the sets.
   - `main(user1, user2)`: Main function to calculate and print the similarity score between two users.

3. **Command-Line Interface**:
   - Uses `argparse` to parse the usernames of the two users from the command line.
   - Calls `main` with the parsed usernames.
