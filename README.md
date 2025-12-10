# AI Council

An autonomous multi-agent discussion platform where AI models deliberate on complex topics. A "Council Head" manages the discussion, synthesizes arguments from various "Council Members," and delivers a final, well-reasoned decision.

## 🚀 Features

- **Multi-Agent Deliberation**: Different LLMs (e.g., Llama 3, Gemini, Qwen) debate topics in real-time.
- **Council Orchestration**: A dedicated "Council Head" agent manages rounds and makes the final decision.
- **Interactive UI**: Clean Streamlit interface to configure members and watch the debate unfold.
- **Collapsible Responses**: Organized view of member arguments with expandable details settings.
- **Real-time Updates**: Watch the discussion progress round-by-round.
- **Flexible Configuration**: Choose your council members and head from a variety of OpenRouter/Ollama models.

## 📸 Screenshots

[![Clean-Shot-2025-12-10-at-10-57-24-2x.png](https://i.postimg.cc/7hfqT381/Clean-Shot-2025-12-10-at-10-57-24-2x.png)](https://postimg.cc/9w566qfz)

[![Clean-Shot-2025-12-10-at-10-57-30-2x.png](https://i.postimg.cc/XYc6qHGg/Clean-Shot-2025-12-10-at-10-57-30-2x.png)](https://postimg.cc/k24phyyV)

[![Clean-Shot-2025-12-10-at-10-57-36-2x.png](https://i.postimg.cc/nhcfsK4h/Clean-Shot-2025-12-10-at-10-57-36-2x.png)](https://postimg.cc/GHN5VygW)

## 🛠️ Tech Stack

### Core
- **Python**: Primary programming language.
- **Streamlit**: Interactive web interface.
- **Orchestrator Pattern**: Custom logic for managing multi-agent state and rounds.
- **Concurrent.futures**: Parallel execution of model responses.

### Integrations
- **OpenRouter API**: Access to diverse LLMs (DeepSeek, Gemini, Llama, etc.).
- **Ollama**: Support for local model inference.

## 📋 Prerequisites

Before installation, ensure you have the following:

- [Python 3.8+](https://www.python.org/)
- [OpenRouter API Key](https://openrouter.ai/)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-council
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 🚀 Running the App

### Start Web UI

```bash
streamlit run app.py
```
Accessible at [http://localhost:8501](http://localhost:8501)

### Start CLI Mode

```bash
python main.py
```