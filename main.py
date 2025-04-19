import asyncio

from agents import Runner, trace

from _setting import setup
from mutil_agents.agents.manager_agent import create_manager_agent


async def main() -> None:
    setup()
    manager_agent = create_manager_agent("gemini-2.0-flash")

    input_data = []
    with trace("Demo chatbot agent"):
        while True:
            user_input = input("Enter a message: ")
            input_data.append({
                "role": "user",
                "content": user_input,
            })
            result = await Runner.run(manager_agent, user_input)
            print(result.final_output)
            input_data = result.to_input_list()


if __name__ == "__main__":
    asyncio.run(main())
