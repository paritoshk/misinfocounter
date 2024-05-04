import asyncio
import os

from anyio import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    mongo_uri: str
    root_path: str


async def set_config():
    file_path = await Path(__file__).parent.parent.absolute()
    return Config(
        root_path=str(file_path),
        mongo_uri=os.environ["MONGODB_KEY"]
    )

CONFIG = asyncio.run(set_config())
