import logging
import httpx
from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import asyncio
from datetime import datetime

from .agent_executor import SemanticKernelProductManagementExecutor

logger = logging.getLogger(__name__)

# Simple data models for A2A protocol


class AgentSkill(BaseModel):
    id: str
    name: str
    description: str
    tags: List[str]
    examples: List[str]


class AgentCapabilities(BaseModel):
    streaming: bool = True


class AgentCard(BaseModel):
    name: str
    description: str
    url: str
    version: str
    defaultInputModes: List[str]
    defaultOutputModes: List[str]
    capabilities: AgentCapabilities
    skills: List[AgentSkill]


class TaskRequest(BaseModel):
    id: str
    input: str
    contextId: Optional[str] = None


class TaskResponse(BaseModel):
    id: str
    output: str
    status: str = "completed"


class A2AServer:
    """A2A Server wrapper for the Zava Product Helper"""

    def __init__(self, httpx_client: httpx.AsyncClient, host: str = "localhost", port: int = 8001):
        self.httpx_client = httpx_client
        self.host = host
        self.port = port
        self.executor = SemanticKernelProductManagementExecutor()
        self._setup_server()

    def _setup_server(self):
        """Setup the A2A server with the product helper"""
        # Create simple Starlette application with A2A endpoints
        routes = [
            Route("/agent-card", self.get_agent_card_endpoint,
                  methods=["GET"]),
            Route("/task", self.execute_task_endpoint, methods=["POST"]),
            Route("/health", self.health_endpoint, methods=["GET"]),
        ]

        self.a2a_app = Starlette(routes=routes)
        logger.info(f"A2A server configured for {self.host}:{self.port}")

    async def get_agent_card_endpoint(self, request):
        """Endpoint to get the agent card"""
        agent_card = self._get_agent_card()
        return JSONResponse(agent_card.dict())

    async def execute_task_endpoint(self, request):
        """Endpoint to execute a task"""
        try:
            body = await request.json()
            task_request = TaskRequest(**body)

            # Mock context and event queue for the executor
            class MockContext:
                def __init__(self):
                    self.request_id = task_request.id

            class MockEventQueue:
                def __init__(self):
                    self.events = []

                async def enqueue_event(self, event):
                    self.events.append(event)

            class MockTask:
                def __init__(self, task_id, input_text, context_id=None):
                    self.id = task_id
                    self.input = input_text
                    self.contextId = context_id or str(uuid.uuid4())

            context = MockContext()
            event_queue = MockEventQueue()
            task = MockTask(task_request.id, task_request.input,
                            task_request.contextId)

            # Execute the task
            await self.executor.execute(context, task, event_queue)

            # Extract the response from events
            output = "Task completed"
            for event in event_queue.events:
                if hasattr(event, 'status') and hasattr(event.status, 'message'):
                    if hasattr(event.status.message, 'text'):
                        output = event.status.message.text
                        break

            response = TaskResponse(
                id=task_request.id,
                output=output,
                status="completed"
            )

            return JSONResponse(response.dict())

        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return JSONResponse({"error": str(e)}, status_code=500)

    async def health_endpoint(self, request):
        """Health check endpoint"""
        return JSONResponse({"status": "healthy", "timestamp": datetime.now().isoformat()})

    def _get_agent_card(self) -> AgentCard:
        """Returns the Agent Card for the Zava Product Helper."""
        capabilities = AgentCapabilities(streaming=True)

        skill_product_helper = AgentSkill(
            id='product_helper_sk',
            name='Zava Product Helper',
            description=(
                'Handles customer inquiries about Zava products, including features, pricing, and ranking products based on customer needs.'
            ),
            tags=['product', 'catalog', 'customer-support', 'semantic-kernel'],
            examples=[
                'Which paint roller is best for smooth surfaces?',
                'Sell me on the benefits of the Zava paint sprayer.',
                'How many different types of paint brushes do you offer?',
                'What are the three most popular colors of paint?',
            ],
        )

        agent_card = AgentCard(
            name='Zava Product Helper',
            description=(
                'Zava Product Helper providing comprehensive product information and recommendations.'
            ),
            url=f'http://{self.host}:{self.port}/',
            version='1.0.0',
            defaultInputModes=['text'],
            defaultOutputModes=['text'],
            capabilities=capabilities,
            skills=[skill_product_helper],
        )

        return agent_card

    def get_starlette_app(self):
        """Get the Starlette app for mounting in FastAPI"""
        return self.a2a_app
