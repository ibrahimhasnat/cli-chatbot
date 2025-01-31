import os
import json
import anthropic
from datetime import datetime
from dotenv import load_dotenv
import argparse

class ChatbotApp:
    def __init__(self, model="claude-3-opus-20240229", max_tokens=1024):
        # Load environment variables
        load_dotenv()
        
        # Initialize Anthropic client
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Conversation management
        self.messages = []
        self.model = model
        self.max_tokens = max_tokens
        self.conversation_dir = "conversations"
        
        # Create conversations directory if it doesn't exist
        os.makedirs(self.conversation_dir, exist_ok=True)

    def save_conversation(self, filename=None):
        """Save current conversation to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.conversation_dir}/conversation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=2)
        
        print(f"\n💾 Conversation saved to {filename}")

    def load_conversation(self, filename):
        """Load a previous conversation from a JSON file."""
        try:
            with open(filename, 'r') as f:
                self.messages = json.load(f)
            print(f"\n📂 Conversation loaded from {filename}")
        except FileNotFoundError:
            print(f"\n❌ File {filename} not found.")

    def clear_conversation(self):
        """Clear conversation history."""
        self.messages = []
        print("\n🧹 Conversation history cleared.")

    def count_tokens(self, text):
        """Estimate token count for a given text."""
        return len(text.split())  # Rough estimate

    def chat(self, system_prompt=None):
        """Interactive chat loop."""
        system_prompt = system_prompt or "You are a helpful and friendly AI assistant. Keep your responses concise and clear."
        
        print("🤖 CLI Chatbot")
        print("Commands: /save, /load [filename], /clear, /quit, /tokens")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle special commands
                if user_input.startswith('/'):
                    command = user_input.split()[0].lower()
                    
                    if command == '/quit':
                        print("\n👋 Goodbye!")
                        break
                    elif command == '/save':
                        self.save_conversation()
                    elif command == '/load':
                        if len(user_input.split()) > 1:
                            self.load_conversation(user_input.split()[1])
                        else:
                            print("Please specify a filename.")
                    elif command == '/clear':
                        self.clear_conversation()
                    elif command == '/tokens':
                        tokens = sum(self.count_tokens(msg.get('content', '')) for msg in self.messages)
                        print(f"\n🧮 Estimated token count: {tokens}")
                    continue
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Add user message
                self.messages.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Get AI response
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=self.messages,
                    system=system_prompt
                )
                
                # Extract and print response
                assistant_message = response.content[0].text
                print("\nAssistant:", assistant_message)
                
                # Add assistant message
                self.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser(description="CLI Chatbot with Anthropic API")
    parser.add_argument('--model', default='claude-3-opus-20240229', 
                        help='Anthropic model to use')
    parser.add_argument('--max-tokens', type=int, default=1024, 
                        help='Maximum tokens in response')
    args = parser.parse_args()

    # Initialize and run chatbot
    chatbot = ChatbotApp(model=args.model, max_tokens=args.max_tokens)
    chatbot.chat()

if __name__ == "__main__":
    main()