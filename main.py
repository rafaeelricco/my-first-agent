from agno.agent import Agent
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from agno.tools.telegram import TelegramTools
from agno.models.google import Gemini

from config import settings

mcp_tools = MCPTools(command="npx @playwright/mcp@latest")

telegram_tools = TelegramTools(
    token=settings.telegram_token,
    chat_id=settings.telegram_chat_id,
)

agent = Agent(
    id="playwright-scraper",
    name="Playwright Scraper Agent",
    model=Gemini(id=settings.model_id, api_key=settings.api_key),
    tools=[mcp_tools, telegram_tools],
    instructions=["After completing any scraping task, always send the results summary to Telegram."],
    markdown=True,
)

agent_os = AgentOS(
    description="Car rental pricing extraction agent with Telegram notifications",
    agents=[agent],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app")
