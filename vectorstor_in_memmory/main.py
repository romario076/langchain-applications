import os

os.environ["OPENAI_API_KEY"] = '***'
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


print("hi")
pdf_path = "./2210.03629.pdf"
loader = PyPDFLoader(file_path=pdf_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
docs = text_splitter.split_documents(documents=documents)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index_react")

new_vectorstore = FAISS.load_local("faiss_index_react", embeddings, allow_dangerous_deserialization=True)
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=new_vectorstore.as_retriever())
res = qa.run("Give me the gist of ReAct in 3 sentences")
print(res)


from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
user_template = HumanMessagePromptTemplate.from_template("{user_prompt}")
template = ChatPromptTemplate.from_messages([user_template])
user_prompt = "Give me the gist of LLM ReAct in 3 sentences"

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
chain = LLMChain(llm=llm, prompt=template)
result = chain.run({"user_prompt": user_prompt})

print(result)