import os
from agents import Agent,RunConfig,Runner,OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
load_dotenv()

api_key = os.getenv("OPEN_ROUTER_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

#step n1: initialize the provider
provider = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)
#step n2:initialize the model
model=OpenAIChatCompletionsModel(
    model=model,
    openai_client=provider,
)
#step n3:Define config at run level
run_config=RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)
#step n4:Initialize the agent
agent=Agent(
    name="Chatbot",
    instructions="You are a helpful assistant",
    
)
#step n5:Initialize the runner
result=Runner.run_sync(
    starting_agent=agent,
    input="What is the capital of France",
    run_config=run_config,
    )
print(result.final_output)





