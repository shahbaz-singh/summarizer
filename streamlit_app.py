import streamlit as st
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
        base64_data = base64.b64encode(document).decode('utf-8')
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates structured summaries while maintaining key details."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": get_prompt_for_usecase("", usecase)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_data}"
                        }
                    }
                ]
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error in summarize_document: {str(e)}")
        raise

def summarize_text(text, usecase='general'):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates structured summaries while maintaining key details."
            },
            {
                "role": "user",
                "content": get_prompt_for_usecase(text, usecase) + "\n\nText to summarize:\n" + text
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error in summarize_text: {str(e)}")
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
                        bytes_data = uploaded_file.getvalue()
                        st.session_state.summary = summarize_document(bytes_data, use_case)
                    else:
                        st.session_state.summary = summarize_text(text_input, use_case)
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")

with col2:
    # Display summary
    if st.session_state.summary:
        st.markdown("### Generated Summary")
        st.markdown(st.session_state.summary) 