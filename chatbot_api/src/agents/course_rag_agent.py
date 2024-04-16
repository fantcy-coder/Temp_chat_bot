import os

from chatbot_api.src.chains.course_cypher_chain import course_cypher_chain
from chatbot_api.src.chains.course_objectives_chain import objectives_vector_chain as ovc
from langchain import hub
from langchain.agents import AgentExecutor, Tool
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_cohere import ChatCohere

COURSE_AGENT_MODEL = os.getenv("COURSE_AGENT_MODEL")
course_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    # tool for getting quantitative details of students, alumni and courses
    Tool(
        name="Graph",
        func=course_cypher_chain.invoke,
        description="""Useful for answering questions about students credentials
        such as whether placed or not, alumni who guided, variation in courses statistics. 
        This is mainly used for providing objective questions.
        Use the entire prompt as input to the tool. For instance, if the prompt is "How many alumni
        that have guided?", the input should be "How many alumni that have guided?".
        Example: Which schools alumni guided the maximum students?
        """,
    ),
    tool for getting subjective details of courses
    Tool(
        name="Objectives",
        func=ovc.invoke,
        description="""Useful when you need to answer questions
        about course, modules, skill gains or levels 
        question that could be answered about a course using semantic
        search. Useful for answering subjective questions that do not involve
        maximum, minmum, counting, percentages, aggregations, or listing facts. Use the
        entire prompt as input to the tool. For instance, if the prompt is
        "Will i learn art in this course?", the input should be
        "Will i learn art in this course?".
        Example : What are the skill gain in fashion and design courses? 
        """,
    ),
    
]

chat_model = ChatCohere(
    model=COURSE_AGENT_MODEL,
    temperature=0,
)

course_rag_agent = create_cohere_react_agent(
    llm=chat_model,
    prompt=course_agent_prompt,
    tools=tools,
)

course_rag_agent_executor = AgentExecutor(
    agent=course_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
