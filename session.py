from typing import List

from pydantic import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
# from langchain_core.runnables.utils import ConfigurableFieldSpec


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


def get_history_factory_config():
    return None


def get_invoke_config():
    return {"configurable": {"session_id": "foo"}}


# def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
#     if (user_id, conversation_id) not in store:
#         store[(user_id, conversation_id)] = InMemoryHistory()
#     return store[(user_id, conversation_id)]
#
# def get_history_factory_config():
#     return [
#         ConfigurableFieldSpec(
#             id="user_id",
#             annotation=str,
#             name="User ID",
#             description="Unique identifier for the user.",
#             default="",
#             is_shared=True,
#         ),
#         ConfigurableFieldSpec(
#             id="conversation_id",
#             annotation=str,
#             name="Conversation ID",
#             description="Unique identifier for the conversation.",
#             default="",
#             is_shared=True,
#         ),
#     ]
#
# def get_invoke_config():
#     return {"configurable": {"user_id": "123", "conversation_id": "1"}}
