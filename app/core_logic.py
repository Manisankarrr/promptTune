import os
import json
import datetime
# Import Path for robust file handling
from pathlib import Path 
from openai import OpenAI
from dotenv import load_dotenv

# --- Configuration & Initialization ---
# Load environment variables from .env file
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# --- CORRECTED PATH HANDLING ---
# The root of the project is two levels up from 'app/core_logic.py'
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Use Path objects for reliable access
MASTER_PROMPT_PATH = PROJECT_ROOT / "data" / "master_prompt.json"
FEEDBACK_LOG_PATH = PROJECT_ROOT / "data" / "feedback_log.json"

# --- CORRECTED LLM Model IDs ---
# Swapping to a confirmed free model ID on OpenRouter
TASK_LLM_MODEL = "z-ai/glm-4.5-air:free" 
# Keeping the Meta-LLM for later use
META_LLM_MODEL = "z-ai/glm-4.5-air:free" 


def load_master_prompt():
    """Loads the current system message from the master configuration file."""
    try:
        #  Using Path.read_text() is clean and safe
        return json.loads(MASTER_PROMPT_PATH.read_text())
    except FileNotFoundError:
        # Create the file with initial data if it doesn't exist
        initial_data = {
            "system_message": "Error: Master prompt file not found.",
            "model_name": TASK_LLM_MODEL,
            "version": "0.0.0",
            "last_updated": datetime.datetime.now().isoformat()
        }
        with open(MASTER_PROMPT_PATH, 'w') as f:
             json.dump(initial_data, f, indent=4)
        return initial_data
    except Exception as e:
        print(f"Error loading master prompt: {e}")
        return {"system_message": f"CRITICAL ERROR: {e}"}


def rewrite_and_generate(user_input: str) -> tuple[str, str]:
    """
    1. Loads the system prompt.
    2. Sends the combined prompt to the Task-LLM via OpenRouter.
    3. Returns the rewritten prompt (for user visibility) and the final response.
    """
    if not user_input:
        return "Please enter a question.", "---"

    config = load_master_prompt()
    system_message = config.get("system_message", "")
    
    # The Meta-Prompt for the LLM to structure its own output
    rewrite_instruction = (
        "TASK: First, rewrite the following VAGUE_INPUT into a highly specific and professional instruction (the 'OPTIMIZED PROMPT'). "
        "The optimized prompt MUST include a clear Persona, the desired Output Format, and clear Constraints. "
        "Second, provide the final answer based on the OPTIMIZED PROMPT. "
        "Format your output strictly as: \n\n<OPTIMIZED_PROMPT>\n\n<FINAL_RESPONSE>"
    )

    full_prompt = f"VAGUE_INPUT: {user_input}"

    messages = [
        {"role": "system", "content": system_message + " " + rewrite_instruction},
        {"role": "user", "content": full_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=TASK_LLM_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
        )
        
        raw_output = response.choices[0].message.content.strip()
        
        if "\n\n" in raw_output:
            # We use .split("\n\n", 1) to ensure we only split on the first occurrence
            optimized_prompt, final_response = raw_output.split("\n\n", 1)
        else:
            optimized_prompt = "--- (Parsing Error: Could not separate prompt and response. The LLM output might not follow the required format.)"
            final_response = raw_output

        return optimized_prompt.strip(), final_response.strip()

    except Exception as e:
        return (
            f"ERROR: Failed to connect to OpenRouter API. Check key/internet. Details: {e}",
            "---"
        )


def log_feedback(
    original_prompt: str,
    optimized_prompt: str,
    final_response: str,
    rating: int
):
    """Logs the interaction data and user feedback to the JSON log file."""
    
    new_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "original_prompt": original_prompt,
        "optimized_prompt": optimized_prompt,
        "final_response": final_response,
        "rating": rating
    }

    try:
        # 1. Load existing data
        if FEEDBACK_LOG_PATH.exists():
            with open(FEEDBACK_LOG_PATH, 'r') as f:
                # Handle case where file is empty (e.g., just '[]')
                content = f.read().strip()
                data = json.loads(content) if content else []
        else:
            data = []
        
        # 2. Append new entry and write back
        data.append(new_entry)
        
        with open(FEEDBACK_LOG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        
        return "Feedback Logged successfully! Thank you."
    
    except Exception as e:
        return f"ERROR: Could not log feedback to JSON file. Details: {e}"

# If you run this file directly, it runs a quick test:
if __name__ == "__main__":
    print("--- Testing Core Logic ---")
    
    # Check loading
    config = load_master_prompt()
    print(f"Current System Message: {config.get('system_message', 'N/A')}")
    
    # Test generation
    opt_prompt, response = rewrite_and_generate("Tell me about the biggest planet in our solar system.")
    print("\n[Optimized Prompt]:\n", opt_prompt)
    print("\n[Final Response]:\n", response)

    # Test logging
    log_status = log_feedback("Vague Test", opt_prompt, response, 1)
    print("\n[Log Status]:", log_status)