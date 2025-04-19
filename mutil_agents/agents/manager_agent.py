from agents import Agent, function_tool


def create_manager_agent(model_name: str) -> Agent[any]:
    @function_tool
    def get_weather(city: str) -> str:
        print(f"[debug] getting weather for {city}")
        return f"The weather in {city} is sunny."

    manager_agent = Agent(
        name="Assistant",
        instructions="Bạn là trợ lý ảo, hãy giúp tôi tìm kiếm thông tin. về thời tiết",
        model=model_name,
        tools=[get_weather],
    )
    return manager_agent
