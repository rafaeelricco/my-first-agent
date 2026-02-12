import asyncio

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from agno.tools.telegram import TelegramTools
from apscheduler import Scheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from config import Settings, settings
from prompts import unidas_extract_expected_output, unidas_extract_prompt


def create_trigger(cfg: Settings) -> IntervalTrigger | CronTrigger:
    """Factory function to create appropriate trigger based on config."""
    if cfg.schedule_cron is not None:
        return CronTrigger.from_crontab(cfg.schedule_cron)
    return IntervalTrigger(minutes=cfg.schedule_interval_minutes)


def create_agent(cfg: Settings) -> Agent:
    """Factory function to create the agent with configured tools."""
    mcp_tools = MCPTools(
        command="npx -y @playwright/mcp@latest",
        transport="stdio",
        timeout_seconds=120,
        tool_name_prefix="playwright",
    )

    telegram_tools = TelegramTools(
        token=cfg.telegram_token,
        chat_id=cfg.telegram_chat_id,
    )

    return Agent(
        model=Gemini(id=cfg.model_id, api_key=cfg.api_key),
        tools=[mcp_tools, telegram_tools],
        instructions=[
            "After completing any scraping task, always send the results summary to Telegram."
        ],
        expected_output=unidas_extract_expected_output,
        markdown=True,
    )


async def agent_task() -> None:
    """Execute the agent with the configured prompt."""
    agent = create_agent(settings)
    await agent.aprint_response(unidas_extract_prompt)


def run_agent_task():
    asyncio.run(agent_task())


def main() -> None:
    """Main entry point with scheduler loop."""
    trigger = create_trigger(settings)

    with Scheduler() as scheduler:
        scheduler.add_schedule(
            run_agent_task,
            trigger,
            id="agent-scheduled-task",
        )
        scheduler.run_until_stopped()


if __name__ == "__main__":
    main()
