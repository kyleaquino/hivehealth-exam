import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.bgg_service import BGGCollectionItem, BGGException

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    filename="logs/app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class Usernames(BaseModel):
    username1: str
    username2: str


def get_top_games(username, own=1, rated=1):
    try:
        collection_items = BGGCollectionItem.fetch_collection(
            username, own=own, rated=rated
        )

        return {item.name for item in collection_items[:100]}

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()


@app.post("/calculate-similarity-score")
async def calculate_similarity_score_endpoint(usernames: Usernames):
    try:
        games1 = get_top_games(usernames.username1)
        games2 = get_top_games(usernames.username2)

        if not games1 or not games2:
            return {"similarity_score": 0}

        common_games = games1.intersection(games2)
        total_games = games1.union(games2)

        logger.info(f"Common Games: {len(common_games)} out of {len(total_games)}")
        similarity_score = len(common_games) / len(total_games)
        return {"similarity_score": f"{round(similarity_score, 2)}"}

    except BGGException as e:
        raise HTTPException(400, str(e)) from e
    except Exception as e:
        raise HTTPException(500, f"Internal Server Error: {str(e)}") from e
