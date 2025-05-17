import os
from dotenv import load_dotenv
from llm_setup import setup_llm

def main():
    """Main function."""
    load_dotenv()
    
    # Setup LLM
    llm = setup_llm()
    
    # Your agent code will go here
    print("Agent initialized successfully!")

if __name__ == "__main__":
    main()
