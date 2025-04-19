import asyncio

from agents import RawResponsesStreamEvent, Runner, TResponseInputItem, trace
from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from _setting import setup
from mutil_agents.agents import create_event_agent, create_manager_agent, create_payment_support_agent


async def main() -> None:
    setup()
    manager_agent = create_manager_agent("gpt-4.1")
    event_agent = create_event_agent("gpt-4.1")
    payment_support_agent = create_payment_support_agent("gpt-4.1")

    manager_agent.handoffs.append(event_agent)
    manager_agent.handoffs.append(payment_support_agent)

    event_agent.handoffs.append(manager_agent)
    event_agent.handoffs.append(payment_support_agent)

    payment_support_agent.handoffs.append(manager_agent)
    payment_support_agent.handoffs.append(event_agent)

    agent = manager_agent
    msg = input("Hi!\n")
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    with trace("Test Flow Agent"):
        while True:
            result = Runner.run_streamed(
                agent,
                input=inputs,
            )
            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print("\n")

            inputs = result.to_input_list()

            user_input = input("Enter a message: ")
            inputs.append({"content": user_input, "role": "user"})
            agent = result.current_agent


if __name__ == "__main__":
    asyncio.run(main())
