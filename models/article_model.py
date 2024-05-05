from pydantic import BaseModel


class Article(BaseModel):
    """

    """
    source: str
    title: str
    content: str
    sentiment: int
    sentiment_by_topic: list[list[str, int]]
