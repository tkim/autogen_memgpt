import autogen
import os
import openai
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": os.getenv("model"),
        "api_base": "http://localhost:5001/v1",
        "api_key": os.getenv("api_key")
    },
]

openai.api_key = os.getenv("api_key")

llm_config = {
    "config_list": config_list,
    "seed": int(os.getenv("seed")),
    "request_timeout": int(os.getenv("request_timeout"))
}

# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_mmessage="A human admin.",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "agenets-workspace",
        "use_docker": False,
        
    }
)