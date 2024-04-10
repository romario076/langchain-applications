from dotenv import load_dotenv, find_dotenv
load_dotenv('D:/Udemy/LangChain/documentation-helper/.env')

import os
from typing import Any, List, Dict

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.pinecone import Pinecone as PineconeLangChain
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
import pinecone


INDEX_NAME = "langchain-doc-index"


pinecone = pinecone.Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeLangChain.from_existing_index(embedding=embeddings,index_name=INDEX_NAME)
    chat = ChatOpenAI(verbose=True,temperature=0,)

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True
    )
    return qa.invoke({"question": query, "chat_history": chat_history})

#if __name__ == "__main__":
#    print(run_llm(query="What is LangChain?"))
