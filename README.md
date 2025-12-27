---
title: PromptTune
emoji: 🐠
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 5.48.0
app_file: app/gradio_interface.py # <--- FIXED LINE
pinned: false
license: mit
short_description: MLOps for Prompt Engineering and Continuous Improvement.
---

# 🚀 Intelligent Prompt Optimizer (IPO-Meta)

This project demonstrates a zero-GPU MLOps pipeline using LLM orchestration 
to automatically improve the system prompt based on continuous user feedback.


check out the live preview at https://prompt-tune-web.vercel.app/
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
# 🎵 PromptTune

**MLOps Toolkit for Interactive Prompt Engineering and Optimization**

---

## 📖 Introduction

**promptTune** is a modular MLOps toolkit designed for experimenting with, optimizing, and managing LLM prompts. It provides a streamlined interface for rewriting prompts, collecting feedback, and iteratively improving prompt performance—all while maintaining robust, auditable records of prompt changes and user interactions.

---
## 🚀 Features

**🤖 LLM Orchestration & Rewriting:** Dynamically leverages a **Meta-LLM** via the OpenRouter API to transform vague user inputs into highly structured, actionable system prompts, ensuring high-quality responses from the final **Task-LLM**.

**♻️ Continuous Prompt Learning:** Implements a zero-GPU, feedback-driven loop where sufficient **negative user ratings (Rating: 0)** automatically trigger the optimization workflow.

**⚙️ MLOps Deployment Pipeline:** Uses scheduled **GitHub Actions** to execute the core Python script, automatically versioning, committing, and deploying the newly refined system prompt configuration back to the main branch.

**💾 Versioned Configuration Management:** Maintains a single source of truth for the active system prompt (`master_prompt.json`), ensuring **reproducibility** and enabling future rollbacks.

**💻 Gradio Interface & Data Collection:** Provides a simple, Python-native web interface for user interaction and securely logs all raw feedback to inform the next nightly deployment cycle.

**📊 Observability Log:** Includes a dedicated status file (`status_log.txt`) that tracks the exact date and time of the last successful prompt deployment, offering a clear audit trail.

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/promptTune.git
   cd promptTune
   ```

2. **Set up a Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Create a `.env` file in the project root and add your OpenAI or compatible API key:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```

---

## ⚡ Usage

### 1. **Run the Gradio Web App**
   ```bash
   python -m app.gradio_interface
   ```
   - **Interact:** Enter prompts, view responses, and provide feedback via the web UI.

### 2. **Optimize Prompts via Script**
   ```bash
   python scripts/optimize_prompt.py
   ```
   - This script reviews feedback logs and updates the master prompt for improved results.

### 3. **Project Structure**
   ```
   promptTune/
   ├── app/
   │   ├── __init__.py
   │   ├── core_logic.py
   │   └── gradio_interface.py
   ├── data/
   │   ├── feedback_log.json
   │   └── master_prompt.json
   └── scripts/
       └── optimize_prompt.py
   ```

---

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a branch for your feature or fix (`git checkout -b feature-name`).
3. Commit your changes.
4. Submit a pull request with a clear description.

**Please ensure all code is well-documented and tested.**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> **Maintained by [Manisankarrr](https://github.com/Manisankarrr)**
```

🔗 GitHub Repo: https://github.com/Manisankarrr/promptTune