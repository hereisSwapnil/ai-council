# AI Council

A sophisticated multi-agent AI discussion system that orchestrates autonomous deliberations between multiple AI models to reach well-reasoned conclusions. The system enables different AI models to debate, challenge each other's arguments, and collaboratively arrive at comprehensive answers through structured multi-round discussions.

## 🚀 Features

- **Multi-Round Discussions**: Autonomous deliberations with up to 3 rounds of structured debate.
- **Parallel Execution**: Council members respond concurrently for faster deliberations.
- **Intelligent Orchestration**: Sophisticated discussion flow with early stop mechanisms when consensus is reached.
- **Provider-Agnostic**: Flexible architecture supporting multiple AI providers (OpenRouter, Ollama).
- **Rich Logging System**: Comprehensive logging for debugging and observability.
- **Error Resilience**: Robust error handling ensures partial failures don't halt the entire discussion.
- **Council Head Decision**: Final decision synthesis by a designated council head based on all debate rounds.

## 🎯 How It Works

1. **Initial Round**: Each council member provides their initial position, key arguments, and potential concerns on the query.
2. **Debate Rounds**: Members review others' responses, challenge disagreements, support agreements, and refine their positions.
3. **Early Stop Protocol**: Members can signal consensus with `READY_FOR_DECISION` or `STOP_DISCUSSION` keywords.
4. **Final Decision**: The council head synthesizes all arguments and provides a definitive answer with rationale.

## 🛠️ Tech Stack

### Core Technologies
- **Python**: Core programming language for orchestration and logic.
- **OpenRouter API**: Access to multiple free AI models (Gemma, Grok, DeepSeek).
- **Ollama**: Optional local AI model provider support.
- **Threading**: Concurrent execution using ThreadPoolExecutor for parallel responses.

### Key Libraries
- **requests**: HTTP client for API communication.
- **python-dotenv**: Environment variable management.
- **logging**: Comprehensive logging system for debugging and monitoring.

## 📋 Prerequisites

Before running the application, ensure you have the following installed:
- [Python](https://www.python.org/) (v3.8 or higher)
- [pip](https://pip.pypa.io/) (Python Package Manager)
- An API key from [OpenRouter](https://openrouter.ai/) (optional: free tier available)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-council
   ```

2. **Install dependencies**
   ```bash
   pip install requests python-dotenv
   ```

## ⚙️ Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Getting Your API Key
1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Navigate to your API keys section
3. Generate a new API key
4. Copy the key to your `.env` file

## 🚀 Running the App

1. **Run a Discussion**
   ```bash
   python main.py
   ```
   
   The system will:
   - Initialize the council with multiple AI models
   - Run autonomous deliberation on the configured query
   - Display each round's responses in real-time
   - Present the council head's final decision
   - Show summary statistics (rounds executed, early stop status)

2. **Customize the Query**
   
   Edit `main.py` to change the discussion topic:
   ```python
   query = "Your question here"
   ```

3. **Configure Council Members**
   
   Modify the council composition in `main.py`:
   ```python
   member1 = Model(ModelEnum.OPEN_ROUTER_GEMMA_3_27B_IT.value, OpenRouter)
   member2 = Model(ModelEnum.OPEN_ROUTER_GROK_4_1_FAST.value, OpenRouter)
   # Add more members as needed
   ```

## 📁 Project Structure

```
ai-council/
├── constants/
│   └── constants.py       # Model enumerations and constants
├── provider/
│   ├── base.py           # Base provider abstract class
│   ├── model.py          # Model wrapper class
│   ├── open_router.py    # OpenRouter API integration
│   └── ollama.py         # Ollama local model integration
├── prompts/
│   └── prompts.py        # Discussion prompts for each round
├── utils/
│   └── logger.py         # Logging configuration
├── orchestrator.py       # Core discussion orchestration logic
├── main.py              # Entry point for running discussions
├── .env.sample          # Example environment variables
└── README.md            # Project documentation
```

## 🎨 Customization

### Adding New AI Providers

1. Create a new provider class in `provider/`:
   ```python
   from provider.base import BaseProvider
   
   class YourProvider(BaseProvider):
       def generate(self, messages: list[dict[str, str]]):
           # Your implementation
           pass
   ```

2. Add model constants in `constants/constants.py`:
   ```python
   YOUR_PROVIDER_MODEL_NAME = "model-identifier"
   ```

3. Use in `main.py`:
   ```python
   member = Model(ModelEnum.YOUR_PROVIDER_MODEL_NAME.value, YourProvider)
   ```

### Adjusting Discussion Rounds

Modify the `num_rounds` parameter (maximum 3):
```python
orchestrator = Orchestrator(
    council_head=head,
    council_members=[member1, member2, member3],
    num_rounds=2,  # 1-3 rounds
    member_names=["Gemma", "Grok", "Deepseek"]
)
```

### Customizing Prompts

Edit prompts in `prompts/prompts.py`:
- `DISCUSSION_ROUND_1_PROMPT`: Initial round instructions
- `DISCUSSION_ROUND_N_PROMPT`: Subsequent debate rounds
- `COUNCIL_HEAD_DISCUSSION_PROMPT`: Final decision prompt

## 📊 Output Example

```
================================================================================
QUERY: What is the capital of France?
================================================================================

Starting discussion with up to 3 rounds and 3 members...

================================================================================
ROUND 1
================================================================================
────────────────────────────────────────────────────────────────────────────────
Gemma:
────────────────────────────────────────────────────────────────────────────────
**Initial Position:** Paris is the capital of France.
**Key Arguments:** Historical records, government location, international recognition.
**Potential Concerns:** None significant.

[... More member responses ...]

================================================================================
🎯 COUNCIL HEAD FINAL DECISION
================================================================================

**Final Answer:** Paris is the capital of France.

**Decision Rationale:** All council members reached unanimous consensus based on 
historical, governmental, and geographical evidence.

[... Full decision ...]

================================================================================
DISCUSSION COMPLETE
================================================================================
Total rounds requested: 3
Total rounds executed: 1
Stopped early: True
Final decision available: True
```


## 🙏 Acknowledgments

- **OpenRouter**: For providing unified access to multiple AI models
- **Ollama**: For local model deployment capabilities
- The open-source AI community for making advanced models accessible

---

**Made with ❤️ for better AI collaboration**
