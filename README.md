# 🧠 Data Intelligence Assistant

A natural language interface for longitudinal, cohort-based health data analysis. This assistant enables researchers to query complex health study data using simple English questions, providing safe, reproducible, and interpretable results.

## 🚀 Features

- **Natural Language Queries**: Ask questions like "What is the BMI change for participant p002?" or "Show me blood pressure by smoking status"
- **Deterministic Intent Mapping**: Fast, rule-based parsing with Groq Llama 3.1 8B fallback for complex queries
- **Longitudinal Analysis**: Designed for cohort studies with baseline and follow-up visits
- **Data Integrity**: Immutable data model prioritizing correctness and reproducibility
- **Explainable Results**: Groq-powered natural language explanations of query results and insights

## 📊 Data Model

The system uses a carefully designed relational model to support longitudinal analysis:

- **Participants**: Static attributes (sex, date of birth)
- **Visits**: Timepoints (baseline, follow-up) linked to participants
- **Measurements**: Visit-linked data (vitals, surveys)
- **Derived Insights**: Computed results never overwrite source data

## 🏗️ Architecture

```
core/
├── assistant.py          # Main entry point and query processing
├── intents.py            # Intent registry and definitions
├── intent_executor.py    # Query execution engine
├── nl_intent_mapper.py   # Natural language to intent mapping
├── query_runner.py       # SQL execution utilities
└── load.py              # Data loading and processing

genai/
├── llm_intent_helper.py  # Groq-powered intent recognition
└── explainer.py          # Groq-powered result explanation

queries/
├── analysis/             # SQL queries for different intents
└── qc/                   # Quality control queries

schemas/
└── schema.sql            # Database schema definition
```

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Grewal-Pam/data-intelligence-assistant.git
   cd data-intelligence-assistant
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Groq API Key**:
   ```bash
   export GROQ_API_KEY="your-groq-api-key-here"
   ```

4. **Initialize the database**:
   ```bash
   python -c "from core.load import load_data; load_data()"
   ```

## 💡 Usage

### Interactive Mode
```bash
python -m core.assistant
```

Example interaction with real output:
```
🧠 Data Intelligence Assistant (type 'exit' to quit)

You: bmi change participant p002

Assistant:
{
  'status': 'ok',
  'intent': 'bmi_change_by_participant',
  'rows': 1,
  'explanation': "Based on the query result, we can see the BMI (Body Mass Index) change for participant P002.\n\nHere's a breakdown of the result:\n\n- **Participant ID:** P002\n- **BMI at Baseline:** 28.409091 (This is the participant's BMI at the beginning of the study)\n- **BMI at Follow-up:** 20.077335 (This is the participant's BMI at the end of the study)\n- **BMI Change:** -8.331756 (This is the difference between the participant's BMI at baseline and follow-up)\n\nIn simple terms, the participant's BMI decreased from 28.409091 to 20.077335, which means they lost approximately 8.33 units of BMI.",
  'data':     participant_id  bmi_baseline  bmi_followup  bmi_change
              0           P002     28.409091     20.077335   -8.331756
}
----------------------------------------
```

### Programmatic Usage
```python
from core.assistant import ask

result = ask("BMI change for participant p002")
print(result)
```

## 📋 Available Intents

| Intent | Description | Parameters |
|--------|-------------|------------|
| `bmi_change` | BMI change between baseline and follow-up | None |
| `bp_by_smoking` | Average blood pressure by smoking status | `smoking_status` |
| `sleep_by_education` | Average sleep duration by education level | None |
| `bmi_change_by_participant` | BMI change for specific participant | `participant_id` |

## 🔍 Query Examples

- "What's the BMI change between visits?"
- "Show me blood pressure for smokers"
- "How much sleep do people with higher education get?"
- "BMI change for participant p002"
- "Average systolic BP by smoking status"

## 🗃️ Database Schema

The system uses SQLite with four main tables:

- `participants`: Static participant information
- `survey_measurements`: Survey responses (smoking, alcohol, education, sleep)
- `visits`: Visit timepoints and types
- `vital_measurements`: Clinical measurements (BP, BMI, height, weight)

## 🤖 Groq AI Integration

The assistant leverages Groq's fast inference platform for two key capabilities:

### Intent Recognition (`genai/llm_intent_helper.py`)
- **Primary**: Rule-based deterministic mapping for speed and reliability
- **Fallback**: Groq Llama 3.1 8B model for complex or ambiguous queries
- **Purpose**: Convert natural language questions to structured intents and parameters

### Result Explanation (`genai/explainer.py`)
- **Model**: Groq Llama 3.1 8B Instant
- **Purpose**: Generate clear, cautious explanations of query results
- **Features**: Avoids speculation, handles missing data explicitly, provides medical context

Both components require `GROQ_API_KEY` environment variable to be set.

## 🔄 Code Flow

Here's how a natural language query flows through the system:

### 1. **Input Processing** (`core/assistant.py`)
```
User Input: "bmi change participant p002"
     ↓
   ask(question)
```

### 2. **Intent Mapping** (`core/nl_intent_mapper.py` → `genai/llm_intent_helper.py`)
```
try:
    mapped = map_nl_to_intent(question)  # Fast rule-based parsing
except ValueError:
    llm_guess = llm.suggest_intent(question)  # Groq fallback
```

### 3. **Query Execution** (`core/intent_executor.py` → `core/query_runner.py`)
```
intent = "bmi_change_by_participant"
params = {"participant_id": "P002"}
     ↓
df = execute_intent(intent, params)  # Runs SQL query
```

### 4. **Result Explanation** (`genai/explainer.py`)
```
explanation = explainer.explain(question, df)  # Groq generates explanation
```

### 5. **Final Response**
```
{
  "status": "ok",
  "intent": "bmi_change_by_participant",
  "rows": 1,
  "explanation": "Based on the query result, we can see the BMI change for participant P002...",
  "data": DataFrame
}
```

### **Fallback Handling**
- If parameters are missing → Returns `{"status": "needs_clarification", "required": ["participant_id"]}`
- If query fails → Returns `{"status": "error", "message": "error details"}`

## 📈 Quality Control

Built-in QC queries available in `queries/qc/`:
- Missing data analysis
- Visit counts per participant
- Data completeness checks

## 🔒 Design Principles

- **Data Immutability**: Source data is never modified
- **Explicit Time Modeling**: All temporal information through Visit entity
- **Safe Longitudinal Analysis**: Prevents accidental time-based errors
- **Reproducible Results**: All analyses fully reproducible from source data

## 📚 Documentation

- [`docs/data_model.md`](docs/data_model.md) - Detailed data model documentation
- [`queries/readme.md`](queries/readme.md) - Query documentation
- [`schemas/INTENT.md`](schemas/INTENT.md) - Intent specification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for longitudinal health data analysis
- Powered by Groq's fast and efficient AI inference
- Designed with data integrity and researcher usability in mind
- Inspired by modern data science and natural language processing practices
