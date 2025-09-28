import gradio as gr
from app.core_logic import rewrite_and_generate, log_feedback

# --- State Variables ---
# Gradio needs a way to temporarily store the original prompt and response 
# to be used by the separate feedback button.

# These will hold the current interaction data
current_original_prompt = gr.State("")
current_optimized_prompt = gr.State("")
current_final_response = gr.State("")


# --- Helper Functions for Gradio UI ---

def process_submission(user_input):
    """Handles the full workflow: calling the LLM and storing results."""
    
    # 1. Call the core logic function
    optimized_prompt, final_response = rewrite_and_generate(user_input)
    
    # 2. Return new UI values and update internal state variables
    # The return order must match the output components in the 'Submit' button click event.
    return (
        optimized_prompt, 
        final_response, 
        user_input,          # New state for original_prompt
        optimized_prompt,    # New state for optimized_prompt
        final_response       # New state for final_response
    )

def handle_feedback(rating_value, orig_prompt, opt_prompt, final_resp):
    """Handles the user clicking the feedback button."""
    if not orig_prompt:
        return "Error: Please run a query first before providing feedback."
    
    # 1. Map the string rating to an integer (1 for thumbs up, 0 for thumbs down)
    rating_int = 1 if rating_value == "👍 Excellent" else 0
    
    # 2. Call the core logic function to log data
    log_message = log_feedback(orig_prompt, opt_prompt, final_resp, rating_int)
    
    # 3. Clear the state variables after successful logging
    return log_message, "", "", ""


# --- Gradio Interface Layout ---

with gr.Blocks(title="IPO-Meta: Prompt Optimizer") as demo:
    gr.Markdown("# ✨ IPO-Meta: Intelligent Prompt Optimizer")
    gr.Markdown(
        "Enter a question, and our system will automatically rewrite it into a **high-quality, structured prompt** (powered by LLMs) "
        "before generating the final answer. Provide feedback to improve the system's core instruction over time! (The MLOps loop)"
    )

    # --- INPUT SECTION ---
    with gr.Row():
        user_input = gr.Textbox(
            label="1. Your Vague Question/Input:",
            placeholder="e.g., Tell me about quantum computing.",
            lines=3
        )
        
    # --- SUBMIT BUTTON ---
    submit_btn = gr.Button("🚀 Optimize Prompt & Generate Response")

    # --- OUTPUT SECTION ---
    with gr.Row():
        optimized_output = gr.Textbox(
            label="2. Optimized Prompt (The System's Suggestion):",
            lines=4,
            interactive=False,
            elem_id="optimized_prompt"
        )
    
    final_response_output = gr.Markdown(
        "**3. Final AI Response:**\n\n---",
        elem_id="final_response_area"
    )

    # --- FEEDBACK SECTION ---
    gr.Markdown("---")
    gr.Markdown("### 4. Continuous Improvement Feedback (The MLOps Data)")
    
    with gr.Row():
        feedback_status = gr.Textbox(
            label="Feedback Status", 
            value="Waiting for feedback...", 
            interactive=False,
            scale=2
        )
        
        # Radio buttons for clear feedback
        feedback_radio = gr.Radio(
            ["👍 Excellent", "👎 Needs Work"],
            label="Did the Optimized Prompt result in a good response?",
            value=None, # No default selection
            scale=1
        )
        
        feedback_btn = gr.Button("💾 Log Feedback")

    # --- STATE MANAGEMENT (Hidden) ---
    # These hidden components store the data needed by the feedback handler
    current_original_prompt.render()
    current_optimized_prompt.render()
    current_final_response.render()

    # --- Event Handling ---
    
    # When 'Submit' is clicked:
    submit_btn.click(
        fn=process_submission,
        inputs=[user_input],
        outputs=[
            optimized_output,
            final_response_output,
            current_original_prompt,
            current_optimized_prompt,
            current_final_response
        ]
    )
    
    # When 'Log Feedback' is clicked:
    feedback_btn.click(
        fn=handle_feedback,
        inputs=[
            feedback_radio,
            current_original_prompt,
            current_optimized_prompt,
            current_final_response
        ],
        outputs=[
            feedback_status, 
            current_original_prompt, # Clear state on successful log
            current_optimized_prompt, # Clear state on successful log
            current_final_response # Clear state on successful log
        ]
    )
    
# Launch the Gradio app
if __name__ == "__main__":
    # Note: To run locally, your OpenRouter API key must be set in the .env file.
    demo.launch()