import logging
import asyncio
from typing import Any

from .product_management_agent import SemanticKernelProductManagementAgent

logger = logging.getLogger(__name__)

# Simple data structures to replace A2A types


class TaskState:
    working = "working"
    completed = "completed"
    failed = "failed"
    input_required = "input_required"


class TaskStatus:
    def __init__(self, state, message=None):
        self.state = state
        self.message = message


class TaskStatusUpdateEvent:
    def __init__(self, status, final=False, contextId=None, taskId=None):
        self.status = status
        self.final = final
        self.contextId = contextId
        self.taskId = taskId


class TaskArtifactUpdateEvent:
    def __init__(self, artifact, final=True, contextId=None, taskId=None):
        self.artifact = artifact
        self.final = final
        self.contextId = contextId
        self.taskId = taskId


class TextArtifact:
    def __init__(self, description, text):
        self.description = description
        self.text = text


class AgentTextMessage:
    def __init__(self, text, contextId, taskId):
        self.text = text
        self.contextId = contextId
        self.taskId = taskId


def new_agent_text_message(text, contextId, taskId):
    return AgentTextMessage(text, contextId, taskId)


def new_text_artifact(description, text):
    return TextArtifact(description, text)


class SemanticKernelProductManagementExecutor:
    """SemanticKernelProductManagement Executor for A2A Protocol"""

    def __init__(self):
        self.agent = SemanticKernelProductManagementAgent()

    async def execute(
        self,
        context: Any,
        task: Any,
        event_queue: Any,
    ) -> None:
        """Execute agent request with A2A protocol support

        Args:
            context: Request context containing user input and task info
            event_queue: Event queue for publishing task updates
        """
        query = task.input

        async for partial in self.agent.stream(query, task.contextId):
            require_input = partial['require_user_input']
            is_done = partial['is_task_complete']
            text_content = partial['content']

            if require_input:
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.input_required,
                            message=new_agent_text_message(
                                text_content,
                                task.contextId,
                                task.id,
                            ),
                        ),
                        final=True,
                        contextId=task.contextId,
                        taskId=task.id,
                    )
                )
            elif is_done:
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        append=False,
                        contextId=task.contextId,
                        taskId=task.id,
                        lastChunk=True,
                        artifact=new_text_artifact(
                            name='current_result',
                            description='Result of request to agent.',
                            text=text_content,
                        ),
                    )
                )
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(state=TaskState.completed),
                        final=True,
                        contextId=task.contextId,
                        taskId=task.id,
                    )
                )
            else:
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.working,
                            message=new_agent_text_message(
                                text_content,
                                task.contextId,
                                task.id,
                            ),
                        ),
                        final=False,
                        contextId=task.contextId,
                        taskId=task.id,
                    )
                )

    async def cancel(
        self, context: Any, event_queue: Any
    ) -> None:
        """Cancel the current task execution"""
        logger.warning("Task cancellation requested but not implemented")
        raise Exception('cancel not supported')
