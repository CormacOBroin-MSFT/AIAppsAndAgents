from dotenv import load_dotenv
from tools.discountLogic import calculate_discount
from typing import Callable, Set, Any
from azure.ai.agents.models import FunctionTool, ToolSet
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from tools.aiSearchTools import product_data_ai_search
load_dotenv()

CL_PROMPT_TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'prompts', 'CustomerLoyaltyAgentPrompt.txt')
with open(CL_PROMPT_TARGET, 'r', encoding='utf-8') as file:
    CL_PROMPT = file.read()
