import os
import anthropic
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the Anthropic client
    # Make sure to set ANTHROPIC_API_KEY in your .env file
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Initialize conversation history
    messages = []
    
    print("Welcome to the CLI Chatbot! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for quit command
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break
        
        # Skip empty inputs
        if not user_input:
            continue
            
        try:
            # Add user message to history
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Send message to Claude
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=messages,
                system="You are a helpful and friendly AI assistant. Keep your responses concise and clear."
            )
            
            # Extract and print assistant's response
            assistant_message = response.content[0].text
            print("\nAssistant:", assistant_message)
            
            # Add assistant's response to history
            messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()