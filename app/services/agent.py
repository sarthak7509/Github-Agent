from langchain import agents
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.redis import RedisSaver
from redis import Redis
from mcp_server.server import mcp
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
API_KEY = os.getenv("OPENAI_API_KEY")
redis_client = Redis.from_url(url=REDIS_URL)
#checkpointer = RedisSaver.from_conn_string(REDIS_URL)
checkpointer = RedisSaver(redis_client=redis_client)
#get the tools
client = MultiServerMCPClient({
    "github":{
        "transport": "stdio",
        "command": "python",
        "args": ["mcp_server/server.py"]
    }
})

async def get_tool():
    return await client.get_tools()

# get the model

async def create_github_agent():
    chatgpt = ChatOpenAI(model="gpt-4o", api_key=API_KEY)
    tools = await get_tool()

    agent = create_agent(
        model = chatgpt,
        tools=tools,
        checkpointer=checkpointer,
        system_prompt=(
            "You are an elite GitHub Assistant. Use your tools to search repositories, "
            "analyze code, and answer user questions. Always check history for context."
        )
    )
    return agent

async def ask_agent(user_input: str, thread_id: str, agent):
    #get thred
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {"message": [("user", user_input)]}

    #trigger the chat infrence
    result = agent.invoke(
        input_state,
        config=config
    )
    return result["messages"][-1].content
