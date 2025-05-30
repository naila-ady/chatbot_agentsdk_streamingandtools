import os                      # For environment variables
import chainlit as cl          # Chainlit framework for chatbot UI
# Agent framework components
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig  
from openai import AsyncOpenAI # Async OpenAI client
from dotenv import load_dotenv # To load .env config

load_dotenv()                 # Load environment variables from .env file
print("🚀 Starting Chainlit App...")  # Simple startup log

# Step 1: Get API key, base URL, and model name from environment variables
api_key = os.getenv("OPEN_ROUTER_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL")

# Step 2: Initialize the OpenAI async client with API key and base URL
client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

# Step 3: Initialize the OpenAI chat completion model with the client and model name
model = OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=client
)

# Step 4: Configure the run settings including model, provider, and disable tracing
run_config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# Step 5: Create an Agent with a name and instructions for how it should behave
agent = Agent(
    name="Smart ChatBot",
    instructions="you are a helpful assisstant"
)

# When chat starts, send a welcome message to the user
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hello! I'm ready to chat!").send()

# When a message is received from the user, run the agent and send back the reply
@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        starting_agent=agent,
        input=message.content,
        run_config=run_config
    )
    await cl.Message(content=result.final_output).send()
