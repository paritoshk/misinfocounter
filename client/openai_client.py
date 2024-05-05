import json
import os
from typing import Any
from anyio import Path

from openai import AsyncOpenAI

from config import CONFIG

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def get_topic_for_article(article_json: dict[str, Any]) -> dict[str, Any]:
    """

    :param article_json:
    :return:
    """

    system_prompt_path = Path(CONFIG.root_path).joinpath("prompts/system_prompts/topic_extraction.prompt")
    system_prompt = await system_prompt_path.read_text()
    user_prompt_path = Path(CONFIG.root_path).joinpath("prompts/user_prompts/topic_extraction.prompt")
    user_prompt = await user_prompt_path.read_text()

    combined_prompt = f"{user_prompt}\n{json.dumps(article_json, indent=2)}"

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": combined_prompt,
            }
        ],
        model="gpt-3.5-turbo-0125",
    )
    print(chat_completion.json())

    try:
        chat_completion = str(chat_completion.choices[0].message.content)
        stripped_completion = chat_completion.replace("```json", "")
        stripped_completion = stripped_completion.replace("```", "")
        return json.loads(stripped_completion)
    except Exception as e:
        return {}
