import sys
import base64
import json
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv(override=True)  # Add override=True to ensure .env takes precedence

# Get API key from environment
API_KEY = os.environ.get('OPENAI_API_KEY')  # Use os.environ.get instead of os.getenv
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Set OpenAI API key
openai.api_key = API_KEY

print(f"API key loaded from env: {API_KEY[:8]}...", file=sys.stderr)

def get_prompt_for_usecase(text, usecase='general'):
    prompts = {
        'general': """Please analyze this document and provide a summary with:

            🎯 MAIN POINTS:
            - Key takeaways
            
            💡 KEY DETAILS:
            - Supporting information""",
            
        'legal': """Please analyze this legal document and provide a detailed legal summary with:
            
            ⚖️ DOCUMENT INFO:
            - Document type
            - Date of document
            - Parties involved
            - Court/Jurisdiction (if applicable)
            
            📜 KEY PROVISIONS:
            - Main legal points and requirements
            - Core legal obligations
            
            ⏰ DATES & DEADLINES:
            - Important dates
            - Filing deadlines
            - Court appearances
            - Response requirements
            
            📋 OBLIGATIONS:
            - Required actions
            - Compliance requirements
            - Specific responsibilities
            
            ⚠️ LIABILITY & CONSEQUENCES:
            - Risk factors
            - Potential consequences
            - Legal implications
            
            🤝 NEXT STEPS:
            - Immediate actions needed
            - Required responses
            - Follow-up requirements""",
            
        'medical': """Please analyze this medical document and provide a detailed medical summary with:
            
            🏥 DIAGNOSIS:
            - Primary conditions
            - Secondary conditions
            - Key symptoms
            
            💊 TREATMENT PLAN:
            - Prescribed medications
            - Treatment procedures
            - Therapy recommendations
            
            📋 KEY FINDINGS:
            - Test results
            - Important observations
            - Vital measurements
            
            🔍 FOLLOW-UP:
            - Next steps
            - Future appointments
            - Monitoring requirements""",
            
        'technical': """Please analyze this technical document and provide a detailed technical summary with:
            
            🔧 SYSTEM OVERVIEW:
            - Core functionality
            - System architecture
            - Key components
            
            💻 SPECIFICATIONS:
            - Technical requirements
            - Performance metrics
            - System constraints
            
            🛠️ IMPLEMENTATION:
            - Development approach
            - Key technologies
            - Integration points
            
            📈 PERFORMANCE:
            - Benchmarks
            - Optimization details
            - Scalability considerations""",
    }
    return prompts.get(usecase, prompts['general'])

def summarize_document(document, usecase='general'):
    try:
        print(f"Received document size: {len(document)} bytes", file=sys.stderr)
        
        if len(document) == 0:
            raise ValueError("Empty document received")

        # Convert document to base64
        base64_data = base64.b64encode(document).decode('utf-8')
        print(f"Base64 data size: {len(base64_data)}", file=sys.stderr)
        
        # Create the agent with API key from env
        agent = Agent(
            name="Document Vision Agent",
            model=OpenAIChat(
                id="gpt-4o",
                max_tokens=4000,
                temperature=0.7,
                vision=True,
                api_key=API_KEY,
                openai_api_key=API_KEY
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

        # Create the message with image using correct format
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": get_prompt_for_usecase("", usecase)},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_data}"  # Using JPEG as default
                    }
                }
            ]
        }

        print("Sending to OpenAI...", file=sys.stderr)
        response = agent.run(message)
        print("Received response from OpenAI", file=sys.stderr)
        
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        print(f"Error in summarize_document: {str(e)}", file=sys.stderr)
        print(f"Error type: {type(e)}", file=sys.stderr)
        raise

def main():
    try:
        if sys.stdin.buffer.readable():
            # Read the first line as metadata using readline() instead of reading byte by byte
            metadata_line = sys.stdin.buffer.readline().decode('utf-8')
            
            # Parse metadata
            metadata = json.loads(metadata_line)
            usecase = metadata.get('useCase', 'general')
            
            if metadata.get('isText'):
                # For text input, read the text from metadata
                text = metadata.get('text', '')
                print(f"Processing text input with use case: {usecase}", file=sys.stderr)
                summary = summarize_text(text, usecase)
                print(summary)
            else:
                # For file input, read binary data
                expected_size = metadata.get('fileSize', 0)
                document = sys.stdin.buffer.read(expected_size)
                if len(document) != expected_size:
                    raise ValueError(f"Expected {expected_size} bytes but got {len(document)}")
                summary = summarize_document(document, usecase)
                print(summary)
        else:
            print("No input provided")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON metadata: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error in main: {str(e)}", file=sys.stderr)
        sys.exit(1)

def summarize_text(text, usecase='general'):
    try:
        print(f"Creating summary for text of length: {len(text)}", file=sys.stderr)
        
        # Create the agent
        agent = Agent(
            name="Text Summary Agent",
            model=OpenAIChat(
                id="gpt-4o",
                max_tokens=4000,
                temperature=0.7
            ),
            instructions=[
                "Create a structured summary using the sections provided.",
                "Use bullet points for clarity and keep each point concise.",
                "Maintain appropriate terminology for the specific use case."
            ],
            show_tool_calls=False,
            markdown=True,
        )

        # Create the message with the prompt and text
        prompt = get_prompt_for_usecase(text, usecase)
        message = {
            "role": "user",
            "content": prompt + "\n\nText to summarize:\n" + text
        }

        print("Sending to OpenAI...", file=sys.stderr)
        response = agent.run(message)
        print("Received response from OpenAI", file=sys.stderr)
        
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        print(f"Error in summarize_text: {str(e)}", file=sys.stderr)
        print(f"Error type: {type(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main() 