# python -m scripts.bgg_compare_users <username_1> <username_2>
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
    # https://realpython.com/command-line-interfaces-python-argparse/#creating-a-cli-with-argparse
    parser = argparse.ArgumentParser(description="Compare two BGG users' game tastes.")
    parser.add_argument("user1", type=str, help="BGG username of the first user.")
    parser.add_argument("user2", type=str, help="BGG username of the second user.")

    args = parser.parse_args()
    main(args.user1, args.user2)
