import os
from dotenv import load_dotenv
from llm_setup import setup_llm

from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
import asyncio

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
    and can assist with data extraction tasks.""",
    mcp_servers=[bright_data_server],
)
print("Main agent initialized successfully!")

async def main():
    """Main function: run the Bright Data agent with user queries."""
    # Your main code will go here
    print("Running main code...")
    print("Enter 'exit' to quit the app.")

    async with bright_data_agent.run_mcp_servers():
        print("Bright Data MCP servers started successfully!")

        console = Console()
        messages = []

        while True:
            user_input = console.input("\n[You] ")
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                print("Goodbye!")
                break
            
            try:
                print("\n[Assistant] ")
                with Live('', console=console, vertical_overflow='visible') as live:
                    async with bright_data_agent.run_stream(
                        user_input, message_history=messages
                    ) as result:
                        curr_message = ""
                        async for message in result.stream_text(delta=True):
                            curr_message += message
                            live.update(Markdown(curr_message))
                            # messages.append(message)
                            
                    messages.extend(result.all_messages())

            except Exception as e:
                print(f"\n[Error] {str(e)}")

if __name__ == "__main__":
    # main()
    asyncio.run(main())
