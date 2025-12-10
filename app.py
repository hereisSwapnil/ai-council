import streamlit as st
import time
import os
from dotenv import load_dotenv
from typing import List

# Import our backend components
from provider.open_router import OpenRouter
from provider.model import Model
from orchestrator import Orchestrator
from constants.constants import Model as ModelEnum

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AI Council",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better looking chat
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-user {
        background-color: #2b313e;
    }
    .chat-assistant {
        background-color: #f0f2f6;
        color: black;
    }
    .council-member {
        border-left: 4px solid #4e8cff;
        padding-left: 1rem;
        margin-top: 0.5rem;
        background-color: #262730;
    }
    .head-decision {
        border: 2px solid #ff4b4b;
        background-color: #3d2626;
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "is_running" not in st.session_state:
        st.session_state.is_running = False

def get_council_members(models_selection: List[str]):
    members = []
    names = []
    for model_name in models_selection:
        members.append(Model(model_name, OpenRouter))
        names.append(model_name.split("/")[-1]) # Simplified name
    return members, names

def main():
    initialize_session_state()
    
    st.title("🤖 AI Council Orchestrator")
    st.markdown("Autonomous multi-agent deliberation system")

    # Sidebar Configuration
    with st.sidebar:
        st.header("Council Configuration")
        
        # Available models from our enum
        available_models = [m.value for m in ModelEnum]
        
        selected_models = st.multiselect(
            "Select Council Members",
            options=available_models,
            default=[
                ModelEnum.OPEN_ROUTER_GPT_OSS_20B.value,
                ModelEnum.OPEN_ROUTER_GROK_4_1_FAST.value,
                ModelEnum.OPEN_ROUTER_DEEPSEEK_R1T2_CHIMERA.value
            ],
            format_func=lambda x: x.split("/")[-1]
        )
        
        head_model = st.selectbox(
            "Select Council Head",
            options=available_models,
            index=5,
            format_func=lambda x: x.split("/")[-1]
        )
        
        num_rounds = st.slider("Max Discussion Rounds", 1, 3, 3)
        
        if not os.getenv("OPENROUTER_API_KEY"):
            st.error("⚠️ OPENROUTER_API_KEY not found in environment variables!")

    # Main Chat Interface
    query = st.chat_input("Enter your discussion topic...", disabled=st.session_state.is_running)
    
    # Display message history
    for msg in st.session_state.messages:
        if msg["type"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        
        elif msg["type"] == "round_start":
            st.markdown(f"### 🔄 Round {msg['round_number']}")
            st.divider()
            
        elif msg["type"] == "member_response":
            # Using expander as requested
            with st.expander(f"{msg['name']} Response", expanded=True):
                if msg.get("error"):
                    st.error(f"Error: {msg['error']}")
                else:
                    st.markdown(msg["content"])
                
        elif msg["type"] == "head_decision":
            st.markdown("---")
            with st.container():
                st.markdown("### 🎯 Council Head Final Decision")
                st.info(msg["content"])

    if query and not st.session_state.is_running:
        st.session_state.is_running = True
        
        # Add user message
        st.session_state.messages.append({"type": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)
            
        # Initialize Backend
        try:
            head = Model(head_model, OpenRouter)
            members, names = get_council_members(selected_models)
            
            orchestrator = Orchestrator(
                council_head=head,
                council_members=members,
                num_rounds=num_rounds,
                member_names=names
            )
            
            # Progress Callback
            def on_progress(event):
                if event["type"] == "round_start":
                    st.session_state.messages.append({
                        "type": "round_start", 
                        "round_number": event["round_number"]
                    })
                    st.markdown(f"### 🔄 Round {event['round_number']}")
                    st.divider()
                    
                elif event["type"] == "member_response":
                    content = event.get("content", "")
                    error = event.get("error")
                    
                    st.session_state.messages.append({
                        "type": "member_response",
                        "name": event["name"],
                        "content": content,
                        "error": error
                    })
                    
                    with st.expander(f"{event['name']} Response", expanded=True):
                        if error:
                            st.error(f"Error: {error}")
                        else:
                            st.markdown(content)
                        
                elif event["type"] == "head_decision_complete":
                    st.session_state.messages.append({
                        "type": "head_decision",
                        "content": event["content"]
                    })
                    st.markdown("---")
                    with st.container():
                        st.markdown("### 🎯 Council Head Final Decision")
                        st.info(event["content"])
            
            # Run Discussion
            with st.spinner("Council is deliberating..."):
                orchestrator.run_discussion(query, on_progress=on_progress)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            st.session_state.is_running = False
            st.rerun()

if __name__ == "__main__":
    main()
