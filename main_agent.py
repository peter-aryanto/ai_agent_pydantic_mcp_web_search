import os
import datetime
from dotenv import load_dotenv
from llm_setup import setup_llm

from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
import asyncio
from contextlib import AsyncExitStack

load_dotenv()

bright_data_server = MCPServerStdio(
    'npx', ["@brightdata/mcp"],
    env={
        "API_TOKEN": os.getenv("BRIGHT_DATA_API_KEY"),
    },
)

llm = setup_llm()
bright_data_agent = Agent(
    llm,
    system_prompt="""You are a web scraping and data collection specialist using Bright Data's tools.
    You can help users extract data from websites, navigate complex web pages, and collect information
    from various online sources. You have access to Bright Data's powerful web scraping capabilities
    and can assist with data extraction tasks. Unless user request specify a particular point of time,
    provide the answer based on the current date time from your tool.""",
    mcp_servers=[bright_data_server],
)
print("Main agent initialized successfully!")

@bright_data_agent.tool_plain
async def get_todays_date() -> str:
    """Get today's date."""
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # print(f"Now: {formatted_date_time}")
    return formatted_date_time

async def main():
    """Main function: run the Bright Data agent with user queries."""
    print("Running main code...")

    # async with bright_data_agent.run_mcp_servers():  # [Learning from mistake] The usage of AsyncExitStack below is tidier for cleaning resources such as MCP servers at the closing of the app.
    async with AsyncExitStack() as stack:
        print("Starting MCP servers...")
        await stack.enter_async_context(bright_data_agent.run_mcp_servers())
        print("Bright Data MCP servers started successfully!")

        console = Console()
        messages = []

        print("Enter 'exit' to quit the app.")
        while True:
            user_input = input("\n[You] ")
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                print("Goodbye!")
                break
            
            try:
                # print("\n[Assistant] ")  # [Learning from mistake] This will cause the response from AI always starts on a new line, the approach using a constant like below is tidier for console output.
                START_OF_ASSISTANT = "\n[Assistant] "
                print(START_OF_ASSISTANT, end="")
                with Live('', console=console, vertical_overflow='visible') as live:
                    # curr_message = ""
                    curr_message = START_OF_ASSISTANT

                    async with bright_data_agent.run_stream(
                        user_input, message_history=messages
                    ) as result:
                        # curr_message = ""  # [Learn from mistake] This will cause duplication on output!
                        async for message in result.stream_text(delta=True):
                            curr_message += message
                            live.update(Markdown(curr_message))
                            
                    messages.extend(result.all_messages())

            except Exception as e:
                print(f"\n[Error] {str(e)}")

        print("The app has stopped.")
        # print(messages)

if __name__ == "__main__":
    asyncio.run(main())
