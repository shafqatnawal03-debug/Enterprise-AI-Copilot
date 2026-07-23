import streamlit as st
import datetime
from copilot_core.chatbot import EnterpriseCopilot
from copilot_core.prompts import get_task_template
from copilot_core.security import check_prompt_security

# ==========================================
# 1. PAGE CONFIGURATION & UI STYLING
# ==========================================
st.set_page_config(
    page_title="Enterprise AI Copilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #2563EB, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR (SETTINGS MENU)
# ==========================================
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Configure your AI Copilot here.")
    
    # API Key Configuration
    api_key_input = st.text_input("🔑 Gemini API Key", type="password", help="Required to connect to Google's AI.")
    if not api_key_input:
        st.warning("Please enter your API key to start chatting.")
    
    st.divider()
    
    # Dynamic Prompt Selection
    st.subheader("💡 Task Template")
    task_type = st.selectbox(
        "How should the AI handle your message?", 
        ["Standard Chat", "Explain Topic", "Summarize", "Translate", "Improve Writing", "Generate Ideas"],
        help="Select a template and the AI will automatically format your request."
    )
    
    st.divider()
    
    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        if 'copilot' in st.session_state:
            del st.session_state['copilot']
        st.success("Memory cleared!")
        st.rerun()

    # Export Feature (Bonus)
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        chat_text = "Enterprise AI Copilot - Chat Export\n" + "="*40 + "\n\n"
        for msg in st.session_state.messages:
            role_name = "You" if msg['role'] == 'user' else "AI Copilot"
            time = msg.get('timestamp', '')
            chat_text += f"[{time}] {role_name}:\n{msg['content']}\n\n"
            
        st.download_button(
            label="💾 Export Chat (TXT)",
            data=chat_text,
            file_name="copilot_chat.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()
    st.write("**Enterprise AI Copilot v2.0**")
    st.caption("Powered by Google Gemini & Streamlit")

# ==========================================
# 3. MAIN UI APP INIT
# ==========================================
st.markdown("<h1 class='main-title'>Enterprise AI Copilot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your secure, intelligent, and professional AI assistant.</p>", unsafe_allow_html=True)

# Initialize Session Memory
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming initial AI message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I am your Enterprise AI Copilot. I can calculate math, convert units, check the time, or assist you with any task. How can I help you today?",
        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
    })

# Render Chat History
for message in st.session_state.messages:
    # Use different avatars for User and AI
    avatar = "👤" if message["role"] == "user" else "💼"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        # Bonus: Display timestamp
        if "timestamp" in message:
            st.caption(message["timestamp"])

# ==========================================
# 4. CHAT INPUT & PROCESSING
# ==========================================
if prompt := st.chat_input("Type your message here..."):
    
    # Validation 1: Empty message is automatically handled by Streamlit chat_input
    
    # Validation 2: Missing API Key
    if not api_key_input:
        st.error("❌ Action Blocked: No API Key found. Please add it in the sidebar settings.")
        st.stop()
        
    # Validation 3: Security Prompt Injection Check
    is_safe, warning = check_prompt_security(prompt)
    if not is_safe:
        st.error(warning)
        st.stop()
        
    # Initialize the backend AI if it doesn't exist in memory yet
    if 'copilot' not in st.session_state:
        try:
            st.session_state.copilot = EnterpriseCopilot(api_key=api_key_input)
        except Exception as e:
            st.error(f"❌ Failed to initialize AI. Please check your API Key. Error: {e}")
            st.stop()

    # Step A: Display user's message immediately
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": current_time})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        st.caption(current_time)

    # Step B: Route the prompt through our dynamic templates
    final_prompt = get_task_template(task_type, prompt)

    # Step C: Show Loading Animation and Get Response
    with st.chat_message("assistant", avatar="💼"):
        with st.spinner("Analyzing request and running tools..."):
            # Send message to backend
            response_text = st.session_state.copilot.send_message(final_prompt)
            
            # Display response
            st.markdown(response_text)
            
            # Save to memory
            resp_time = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({"role": "assistant", "content": response_text, "timestamp": resp_time})
            st.caption(resp_time)
