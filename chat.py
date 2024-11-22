# from operator import itemgetter
from typing import List

from langchain_core.chat_history import BaseChatMessageHistory

# from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
# from langchain_core.runnables import (
#     RunnableLambda,
#     ConfigurableFieldSpec,
#     RunnablePassthrough,
# )
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

from langchain_community.chat_models import ChatOllama
# from langchain_ollama import ChatOllama


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


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


prompt = ChatPromptTemplate.from_messages(
    [
        # ("system", "You're an assistant who's good at {ability}"),
        (
            "system",
            "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# chain = prompt | ChatOllama(model="qwen2:0.5b")
chain = prompt | ChatOllama(model="qwen2:0.5b") | StrOutputParser()

chain_with_history = RunnableWithMessageHistory(
    chain,
    # Uses the get_by_session_id function defined in the example
    # above.
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)

# def get_session_history(
#     user_id: str, conversation_id: str
# ) -> BaseChatMessageHistory:
#     if (user_id, conversation_id) not in store:
#         store[(user_id, conversation_id)] = InMemoryHistory()
#     return store[(user_id, conversation_id)]
#
# with_message_history = RunnableWithMessageHistory(
#     chain,
#     get_session_history=get_session_history,
#     input_messages_key="question",
#     history_messages_key="history",
#     history_factory_config=[
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
#     ],
# )


def chat(query):
    # sess = get_session()
    # res = sess.run(query)
    res = chain_with_history.invoke(
        # {"ability": "math", "question": "What's its inverse"},
        # {"ability": "math", "question": query},
        {"question": query},
        config={"configurable": {"session_id": "foo"}},
        # config={"configurable": {"user_id": "123", "conversation_id": "1"}}
    )
    print(res)
    return res
