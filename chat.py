from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever

from langchain_ollama import ChatOllama

import config
from loader import get_retriever
from session import get_session_history, get_history_factory_config, get_invoke_config


llm = ChatOllama(model=config.model, disable_streaming=True)
retriever = get_retriever()

### Contextualize question ###
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", config.contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

### Answer question ###
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", config.qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

chain_with_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    output_messages_key="answer",
    history_messages_key="chat_history",
    history_factory_config=get_history_factory_config(),
)


def chat(query):
    res = chain_with_history.invoke(
        {"input": query},
        config=get_invoke_config(),
    )
    print(res)
    return res["answer"]
