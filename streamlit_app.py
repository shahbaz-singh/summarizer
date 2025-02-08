import streamlit as st
import base64
from phi.agent import Agent
from phi.model.openai import OpenAIChat
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Document & Text Summarizer",
    page_icon="✨",
    layout="wide"
)

# Initialize session state
if 'summary' not in st.session_state:
    st.session_state.summary = None

def get_prompt_for_usecase(text, usecase='general'):
    prompts = {
        'general': f"""Please analyze this text and provide a summary with:
            
            🎯 MAIN POINTS:
            - Key takeaways
            
            💡 KEY DETAILS:
            - Supporting information""",
            
        'legal': f"""Please analyze this legal document and provide a detailed legal summary with:
            
            ⚖️ DOCUMENT INFO:
            - Document type
            - Date of document
            - Parties involved
            - Court/Jurisdiction
            
            📜 KEY PROVISIONS:
            - Main legal points
            - Core obligations
            
            ⏰ DATES & DEADLINES:
            - Important dates
            - Filing deadlines
            - Response requirements
            
            📋 OBLIGATIONS:
            - Required actions
            - Compliance requirements
            
            ⚠️ LIABILITY & CONSEQUENCES:
            - Risk factors
            - Legal implications""",
    }
    return prompts.get(usecase, prompts['general'])

def summarize_document(document, usecase='general'):
    try:
        # Convert document to base64
        base64_data = base64.b64encode(document).decode('utf-8')
        
        # Create the agent
        agent = Agent(
            name="Document Vision Agent",
            model=OpenAIChat(
                id="gpt-4o",
                max_tokens=4000,
                temperature=0.7,
                vision=True,
                api_key=os.getenv('OPENAI_API_KEY')
            ),
            instructions=[
                "Analyze the provided document image.",
                "Create a structured summary using the sections provided.",
                "Use bullet points for clarity and keep each point concise.",
                "Maintain appropriate terminology for the specific use case."
            ],
            show_tool_calls=False,
            markdown=True,
        )

        # Create the message with image
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": get_prompt_for_usecase("", usecase)},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_data}"
                    }
                }
            ]
        }

        response = agent.run(message)
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        st.error(f"Error in summarize_document: {str(e)}")
        raise

# Streamlit UI
st.title("✨ AI Document & Text Summarizer")
st.markdown("Transform documents and text into concise, structured summaries")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    # Use case selector
    use_case = st.selectbox(
        "Select Use Case",
        ["general", "legal", "technical", "medical", "academic", "research"],
        format_func=lambda x: x.title()
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a document (PDF or Image)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    # Text input
    text_input = st.text_area(
        "Or enter text here",
        height=200,
        placeholder="Paste your text here..."
    )

    # Process button
    if st.button("✨ Generate Summary", type="primary"):
        if uploaded_file and text_input:
            st.error("Please either upload a file OR enter text, not both.")
        elif not uploaded_file and not text_input:
            st.error("Please upload a file or enter text to summarize.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    if uploaded_file:
                        # Process file
                        bytes_data = uploaded_file.getvalue()
                        st.session_state.summary = summarize_document(bytes_data, use_case)
                    else:
                        # Process text
                        agent = Agent(
                            name="Text Summary Agent",
                            model=OpenAIChat(
                                id="gpt-4o",
                                max_tokens=4000,
                                temperature=0.7,
                                api_key=os.getenv('OPENAI_API_KEY')
                            )
                        )
                        prompt = get_prompt_for_usecase(text_input, use_case)
                        response = agent.run(prompt + "\n\nText to summarize:\n" + text_input)
                        st.session_state.summary = response.content if hasattr(response, 'content') else str(response)
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")

with col2:
    # Display summary
    if st.session_state.summary:
        st.markdown("### Generated Summary")
        st.markdown(st.session_state.summary) 