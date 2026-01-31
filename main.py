from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

from config import settings

mcp_tools = MCPTools(command="npx @playwright/mcp@latest")

agent = Agent(
    id="playwright-scraper",
    name="Playwright Scraper Agent",
    model=OpenAILike(
        id=settings.model_id,
        base_url="https://api.z.ai/api/coding/paas/v4",
        api_key=settings.api_key,
    ),
    tools=[mcp_tools],
    markdown=True,
)

agent_os = AgentOS(
    description="Car rental pricing extraction agent",
    agents=[agent],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app")
