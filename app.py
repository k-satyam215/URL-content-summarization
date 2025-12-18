import validators
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader, WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
import time
import re

# Streamlit App
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")


# URL input
generic_url = st.text_input("Enter URL", placeholder="https://youtube.com/watch?v=... or https://example.com", label_visibility="collapsed")

# Sidebar for API key
with st.sidebar:
    st.markdown("### 🔑 Groq API Key")
    groq_api_key = st.text_input("Groq API Key", value="", type="password")
    st.markdown("---")
    st.markdown("**✅ Tested URLs:**")
    st.markdown(generic_url)




# ChatPromptTemplate for summarization
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert summarizer. Provide clear, concise, and accurate summaries in 2000 words or less. Focus on key points, main ideas, and important details. Structure your summary with bullet points for clarity."),
    ("human", "Summarize this content:\n\n{text}")
])

def load_content_safely(url):
    """Try multiple loaders until one works"""
    loaders = [
        lambda: UnstructuredURLLoader(urls=[url], headers={"User-Agent": "Mozilla/5.0"}),
        lambda: WebBaseLoader(url),
    ]
    
    for i, loader_func in enumerate(loaders):
        try:
            loader = loader_func()
            docs = loader.load()
            total_chars = sum(len(doc.page_content.strip()) for doc in docs)
            if total_chars > 50:  # Minimum meaningful content
                return docs
        except:
            continue
    
    raise ValueError("All loaders failed - no readable content found")

# Button click
if st.button("🚀 Summarize the Content", type="primary"):
    if not groq_api_key.strip():
        st.error("⚠️ Please enter your Groq API key")
    elif not generic_url.strip():
        st.error("⚠️ Please enter a URL")
    elif not validators.url(generic_url):
        st.error("⚠️ Please enter a valid URL")
    else:
        try:
            # Create LLM
            with st.spinner("🔄 Initializing Groq..."):
                llm = ChatGroq(
                    model="llama-3.1-8b-instant",
                    api_key=groq_api_key,
                    temperature=0.1
                )

            with st.spinner("📥 Loading content..."):
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    st.info("📺 Processing YouTube...")
                    try:
                        # Try YouTube specific loader first (without language_code)
                        loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                        docs = loader.load()
                        st.success("✅ YouTube transcript loaded!")
                    except:
                        st.warning("⚠️ YouTube transcript unavailable, using page content...")
                        docs = load_content_safely(generic_url)
                else:
                    st.info("🌐 Loading website...")
                    docs = load_content_safely(generic_url)

                # Final content validation
                total_chars = sum(len(doc.page_content.strip()) for doc in docs)
                if total_chars < 50:
                    raise ValueError(f"No meaningful content (only {total_chars} chars). Try a text-heavy page.")

            with st.spinner("✨ Generating summary..."):
                if len(docs) == 1 and total_chars < 8000:
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=chat_prompt)
                else:
                    chain = load_summarize_chain(
                        llm, chain_type="map_reduce", 
                        map_prompt=chat_prompt, combine_prompt=chat_prompt
                    )
                summary = chain.run(docs)

            # Results
            st.success("✅ Summary ready!")
            st.markdown("### 📄 Summary")
            st.markdown(summary)
            
            st.markdown("### 📊 Content Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documents", len(docs))
            with col2:
                st.metric("Characters", f"{total_chars:,}")

        except Exception as e:
            st.error(f"❌ {str(e)}")
            st.info("**🔧 Quick Fixes:**")
            st.markdown("- Use simple blog posts")
            st.markdown("- Avoid login-walled sites")
            st.markdown("- Try: https://groq.com")

