from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from config import settings

agent = Agent(model=OpenAIResponses(id=settings.model_id))
