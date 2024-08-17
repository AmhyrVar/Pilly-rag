import streamlit as st
from utils.llm_chains import generate_response_cypher
from utils.page_init import page_init  # noqa



def handle_submit(call):
    

    # handle the response
    with st.spinner("Thinking..."):
        response = generate_response_cypher(call)
        
        with st.chat_message("assistant"):
            formatted_text = response.replace("\n", "<br>")
            st.markdown(formatted_text, unsafe_allow_html=True)


  


def main():
    with st.chat_message("assistant"):
        st.markdown("Je suis votre LLM Médical comment puis-je vous aider ?")

        
    # display messages in Session State
    questions = [
        "Selectionnez une question",
        "Quel est le traitement de la brucellose ?",
        "Quels est la physiopathologie de la tuberculose ?",
        
    ]

    # handle any user input from the selectbox
    selected_question = st.selectbox("Select a question", questions)
    if selected_question != "Selectionnez une question":
        # display user message in chat message container
        with st.chat_message("user"):
            st.markdown(selected_question)

        # generate a response
        handle_submit(selected_question)


if __name__ == "__main__":
    page_title = "Chat Pilly"

    # initialise streamlit
    page_init(page_title=page_title)

    
    main()
