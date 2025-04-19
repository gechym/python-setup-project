import logging

from agents import (
    set_default_openai_api,
    set_default_openai_client,
)
from openai import AsyncOpenAI


def setup(
    mongodb_config: dict[str, str],
    external_config: dict[str, str],
) -> None:
    logging.info(f"Setting up MongoDB with config: {mongodb_config}")
    if external_config["llm_provider"] != "openai":
        logging.info(f"Using {external_config['llm_provider']} API")
        client = AsyncOpenAI(base_url=external_config["base_url"], api_key=external_config["provider_api_key"])
        use_for_tracing = external_config.get("USE_TRACE", False) and bool(external_config.get("OPEN_API_KEY"))
        set_default_openai_client(client=client, use_for_tracing=use_for_tracing)
        set_default_openai_api("chat_completions")
    else:
        logging.info("Using OpenAI API")
