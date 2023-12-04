import os
import autogen
import memgpt.autogen.memgpt_agent as memgpt_autogen
import memgpt.autogen.interface as autogen_interface
import memgpt.agent as agent
import memgpt.system as system
import memgpt.utils as utils
import memgpt.presets as presets
import memgpt.constants as constants
import memgpt.personas.personas as personas
import memgpt.humans.humans as humans
from memgpt.persistence_manager import InMemoryStateManager, InMemoryStateManagerWithPreloadedArchivalMemory, InMemoryStateManagerWithFaiss
import openai
openai.api_key = ''

""" config_list = [
    {
        "model": os.getenv("model"),
        "api_base": "http://localhost:5001/v1",
        "api_key": os.getenv("api_key")
    },
] 
"""

config_list = [
    {
        'model': 'gpt-4'
    },
]

llm_config = {
    "config_list": config_list,
    "seed": 42
    #"request_timeout": int(os.getenv("request_timeout"))
}

inteface = autogen_interface.AutoGenInterface() # MemGPT talk to AutoGen
persistence_manager = InMemoryStateManager()
persona = "I\'m a 10x engineer at a tech company."
human = "I\'m a team manager at a tech company"
memgpt_agent     = presets.use_preset(presets.DEFAULT, 'gpt-4', persona, human, interface, persistence_manager)

#MemGPT coder
coder = memgpt_autogen.MemGPTAgent(
    name="MemGPT_coder",
    agent=memgpt_agent,
)

# non-MemGPT PM
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="First send the message 'Let's go Mario!'")

'''
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
'''
