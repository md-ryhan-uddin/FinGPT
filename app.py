"""
FinGPT - Multi-Agent Financial Intelligence Platform
A Streamlit application showcasing advanced LangGraph multi-agent orchestration.
"""

import streamlit as st
from src.graph.workflow import graph, get_config
import config
import re
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="FinGPT - Multi-Agent Financial Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .research-badge { background-color: #e3f2fd; color: #1976d2; }
    .quant-badge { background-color: #f3e5f5; color: #7b1fa2; }
    .viz-badge { background-color: #e8f5e9; color: #388e3c; }
    .supervisor-badge { background-color: #fff3e0; color: #f57c00; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"
if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0
if "processing" not in st.session_state:
    st.session_state.processing = False

# Sidebar
with st.sidebar:
    st.markdown("### 📊 FinGPT")
    st.markdown("Multi-Agent Financial Intelligence Platform")

    st.markdown("---")

    st.markdown("### 🤖 Agent Team")
    st.markdown("""
    <div class="agent-badge supervisor-badge">📋 Portfolio Manager</div>
    <div class="agent-badge research-badge">🔍 Research Analyst</div>
    <div class="agent-badge quant-badge">📐 Quant Analyst</div>
    <div class="agent-badge viz-badge">📊 Viz Specialist</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📈 Available Stocks")
    for ticker in config.AVAILABLE_TICKERS:
        st.markdown(f"- **{ticker}**")

    st.markdown("---")

    st.markdown("### 💡 Example Queries")
    example_queries = [
        "Who is Apple's CEO?",
        "Analyze Tesla's stock performance over the last month",
        "Compare Apple vs Microsoft returns",
        "Show me a chart of Meta's stock price over 90 days",
        "Calculate volatility for Netflix over the past month",
        "Which tech stock has better returns: AAPL or MSFT?"
    ]

    for i, query in enumerate(example_queries):
        if st.button(query, key=f"example_{i}", use_container_width=True):
            # Check if this message already exists to avoid duplicates
            if not st.session_state.messages or st.session_state.messages[-1].get("content") != query:
                st.session_state.messages.append({"role": "user", "content": query})
                st.session_state.processing = True
            st.rerun()

    st.markdown("---")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(int(st.session_state.thread_id) + 1)
        st.rerun()

    st.markdown("---")

    with st.expander("ℹ️ About FinGPT"):
        st.markdown("""
        **FinGPT** is a production-quality multi-agent system built with:

        - **LangChain** & **LangGraph** for agent orchestration
        - **OpenAI GPT-4o-mini** for intelligence
        - **Supervisor Pattern** for task delegation
        - **Streamlit** for interactive UI

        This project demonstrates advanced agentic AI capabilities including:
        - Multi-agent coordination
        - Tool creation & integration
        - State management
        - Real-world financial analysis

        **Tech Stack:** Python, LangChain, LangGraph, Streamlit, Pandas, Matplotlib
        """)

# Main content
st.markdown('<div class="main-header">📈 FinGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Agent Financial Intelligence Platform</div>', unsafe_allow_html=True)

# Check if we need to process the last message (from example button)
should_process_last = (st.session_state.processing and 
                       st.session_state.messages and 
                       st.session_state.messages[-1]["role"] == "user")

# Display chat messages (except the one we're about to process)
messages_to_display = st.session_state.messages[:-1] if should_process_last else st.session_state.messages
for message in messages_to_display:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input - always visible
prompt = st.chat_input(
    "Ask me anything about stocks... (e.g., 'Who is Tesla's CEO?')",
    key=f"chat_input_{st.session_state.chat_input_key}"
)

# Determine what to process
if should_process_last:
    # Process the last message from example button
    prompt = st.session_state.messages[-1]["content"]
    st.session_state.processing = False
    with st.chat_message("user"):
        st.markdown(prompt)
elif prompt:
    # Process new input from chat box
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
else:
    # Nothing to process
    prompt = None

# Only continue if we have something to process
if prompt:

    # Get response from supervisor graph
    with st.chat_message("assistant"):
        response_container = st.empty()
        display_text = ""

        with st.spinner("🤖 Agents are working..."):
            try:
                full_response = ""
                agent_outputs = []
                seen_contents = set()  # Track seen messages to avoid duplicates
                
                # Use a unique thread_id for each query to avoid conversation history replay
                query_thread_id = f"{st.session_state.thread_id}_{len(st.session_state.messages)}"
                config_dict = get_config(thread_id=query_thread_id)

                # Stream through all chunks
                for chunk in graph.stream(
                    {"messages": [{"role": "user", "content": prompt}]},
                    config_dict
                ):
                    # Check all possible node names in the chunk
                    for node_name in ["researcher", "quant_analyst", "viz_specialist", "supervisor"]:
                        if node_name in chunk:
                            node_data = chunk[node_name]

                            # Extract messages
                            if "messages" in node_data:
                                messages = node_data["messages"]
                                if messages:
                                    for msg in messages:
                                        if hasattr(msg, "content") and msg.content:
                                            content = str(msg.content).strip()
                                            # Skip empty, very short, or duplicate responses
                                            content_hash = hash(content)
                                            if content and len(content) > 5 and content_hash not in seen_contents:
                                                # Skip supervisor routing messages and user input
                                                if (content.lower() not in ['researcher', 'quant_analyst', 'viz_specialist', 'finish'] and
                                                    content != prompt):
                                                    agent_outputs.append(content)
                                                    seen_contents.add(content_hash)
                                                    # Show incremental progress so the user sees updates live
                                                    response_container.markdown("\n\n".join(agent_outputs))

                # Combine all agent outputs
                if agent_outputs:
                    full_response = "\n\n".join(agent_outputs)

                    # Check for image references in the response
                    image_pattern = r'!\[Chart\]\((output/chart_[a-f0-9]+\.png)\)'
                    images = re.findall(image_pattern, full_response)

                    # Remove image markdown from text response for readability
                    clean_response = re.sub(image_pattern, '', full_response)
                    clean_response = re.sub(r'\*\*Charts created:\*\*\s*', '', clean_response)

                    # Build combined response that retains image markdown for history
                    combined_response = clean_response.strip()
                    if images:
                        charts_md = "\n\n**Charts created:**\n" + "\n".join([f"![Chart]({img})" for img in images])
                        combined_response = (combined_response + "\n\n" + charts_md).strip()

                    # Display text (and inline images via markdown)
                    display_text = combined_response if combined_response else full_response
                    response_container.markdown(display_text)

                    # Display images if any were created (ensures visibility during the current run)
                    if images:
                        st.markdown("### 📊 Generated Charts")
                        for img_path in images:
                            if os.path.exists(img_path):
                                image = Image.open(img_path)
                                st.image(image, width="stretch")
                else:
                    full_response = "I've processed your request, but no detailed response was generated. Please try again."
                    display_text = full_response
                    response_container.markdown(display_text)

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}\n\nPlease check your .env file and ensure AI_API_KEY is set correctly."
                st.error(error_msg)
                full_response = error_msg
                display_text = full_response

        # Ensure the final assistant message remains visible after the spinner ends
        if display_text:
            response_container.markdown(display_text)

        # Add assistant response to chat history (including any image markdown so charts persist)
        if display_text:
            st.session_state.messages.append({"role": "assistant", "content": display_text})
        
        # Increment chat input key to reset the input field
        st.session_state.chat_input_key += 1
