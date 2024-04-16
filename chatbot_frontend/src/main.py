import os

import requests
import streamlit as st

CHATBOT_URL = os.getenv(
    "CHATBOT_URL", "http://localhost:8000/course-rag-agent"
)

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a Langchain
        agent designed to answer questions about the courses details, 
        student credentials and alumni guidance 1-to-1 guidance program
        through synthetic course data.
        The agent uses  retrieval-augment generation (RAG) over both
        structured and unstructured data that has been synthetically generated.
        """
    )

    st.header("Example Questions")
    st.markdown("- How many placed students took courses having rating 5?")
    st.markdown(
        """- What is the name of alumni who guided student with student id 56?"""
    )
    st.markdown(
        """- Is the courses suitable for beginner or advanced users ?"""
    )
    st.markdown(
        "- How many students applied for the financial aid?"
    )
    st.markdown(
        """- Who are the instructors for the course - Modern American Poetry?"""
    )
    st.markdown(
        "- What type of schedule is followed in the course - Concept Art for Video Games?"
    )
    st.markdown("- How many students have been placed uptill now?")

    st.markdown("- What is the salary of alumni who guided student with student id as 1?")
    st.markdown(
        """- Which courses provided maximum placed students?"""
    )
    


st.title("GFG Chatbot")
st.info(
    """Ask me questions about enrolled students, provided courses and our alumni!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
