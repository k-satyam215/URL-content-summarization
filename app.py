import validators
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# Streamlit App
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")

# Sidebar for API key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# URL input
generic_url = st.text_input("URL", label_visibility="collapsed")

# Summarization prompt
prompt_template = """
Provide a summary of the following content in 800 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Button click
if st.button("Summarize the Content from YT or Website"):

    # Validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It may be a YouTube video URL or website URL")
    else:
        try:

            # Create LLM AFTER the user enters the API key
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                api_key=groq_api_key
            )

            with st.spinner("Loading and summarizing..."):

                # Load website or YouTube content
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        add_video_info=True
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1)"
                        }
                    )

                docs = loader.load()

                # Summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                # Show result
                st.success(output_summary)

        except Exception as e:
            st.exception(f"Exception: {e}")
