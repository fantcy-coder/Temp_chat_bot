import os

from langchain.chains import RetrievalQA
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain_cohere import ChatCohere,CohereEmbeddings

COURSE_QA_MODEL = os.getenv("COURSE_QA_MODEL")

neo4j_vector_index = Neo4jVector.from_existing_graph(
    embedding=CohereEmbeddings(request_timeout=200),
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="Objectives",
    node_label="Courses",
    text_node_properties=[
        "Objectives",
        "Skill gain",
        "Modules",
        "Level",
        "Keyword"
    ],
    embedding_node_property="Rating",
)

objective_template = """Your job is to use course
objectives to answer questions about the learnings one will gain after
completion of the course. Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer,
say you don't know.
{context}
"""

objective_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=objective_template
    )
)

objective_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [objective_system_prompt, objective_human_prompt]

objective_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

objectives_vector_chain = RetrievalQA.from_chain_type(
    llm=ChatCohere(model=COURSE_QA_MODEL, temperature=0),
    chain_type="stuff",
    retriever=neo4j_vector_index.as_retriever(k=12),
)
objectives_vector_chain.combine_documents_chain.llm_chain.prompt = objective_prompt
