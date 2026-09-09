# ProcureAI — AI-Powered Procurement Assistant

ProcureAI is a conversational AI prototype for analyzing procurement data using natural language.

The application allows users to ask procurement-related questions without writing database queries manually. It interprets the user's question, generates a structured analytical query plan using a Large Language Model (LLM), converts that plan into a MongoDB query or aggregation pipeline, executes it against the procurement database, and returns a clear natural-language answer.

The project uses the State of California procurement dataset as its primary data source.

---

## Features

- Natural-language procurement questions
- AI-assisted query planning
- Automatic MongoDB query and aggregation generation
- MongoDB-based procurement data retrieval
- Support for filtering, grouping, aggregation, sorting, and limiting
- Query validation before database execution
- Natural-language answer generation from database results
- Conversational React interface
- Markdown-formatted assistant responses
- Loading and error handling
- Separate frontend and backend architecture

Example questions include:

- What are the top 5 departments by total spending?
- Which suppliers received the most spending?
- What is the total spending by acquisition type?
- How many purchase orders were created in January 2014?

---

## System Architecture

ProcureAI separates the user interface, API, AI agent, and database responsibilities.

```text
User
  │
  ▼
React Frontend
  │
  │ POST /chat
  ▼
FastAPI Backend
  │
  ▼
LangGraph Agent
  │
  ├── Query Generation
  │       │
  │       ▼
  │   LLM Query Plan
  │       │
  │       ▼
  ├── Query Compiler
  │       │
  │       ▼
  ├── Query Validator
  │       │
  │       ▼
  ├── MongoDB Executor
  │       │
  │       ▼
  └── Answer Generator
          │
          ▼
    Natural-Language Answer
          │
          ▼
     React Frontend
```

Rather than allowing the LLM to directly produce unrestricted MongoDB code, the system uses a structured intermediate query plan. The plan is compiled into a MongoDB query or aggregation pipeline and validated before execution.

This approach improves reliability and provides greater control over database operations.

---

## Agent Workflow

A user request passes through the following workflow:

1. **Natural-language input**  
   The user asks a procurement-related question through the React interface.

2. **Query generation**  
   The LLM interprets the question and produces a structured analytical query plan.

3. **Compilation**  
   The query compiler translates the structured plan into the required MongoDB filter or aggregation pipeline.

4. **Validation**  
   The generated database operation is checked before execution. The validator restricts the pipeline to supported operations and prevents unsupported or unsafe stages.

5. **Execution**  
   The validated query is executed against the MongoDB procurement collection.

6. **Answer generation**  
   The database results are provided to the LLM to generate a concise, user-friendly response based on the retrieved data.

7. **Response display**  
   The final answer is returned through the FastAPI API and rendered in the React conversational interface.

---

## Technology Stack

### Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Google Gemini
- MongoDB
- PyMongo
- Pydantic

### Frontend

- React
- Vite
- JavaScript
- CSS
- React Markdown

### Data

- State of California procurement dataset
- MongoDB database

---

## Project Structure

```text
procurement-ai-assistant/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── answer_generator.py
│   │   │   ├── compiler.py
│   │   │   ├── executor.py
│   │   │   ├── graph.py
│   │   │   ├── prompts.py
│   │   │   ├── query_generator.py
│   │   │   ├── query_models.py
│   │   │   ├── schema.py
│   │   │   ├── state.py
│   │   │   └── validator.py
│   │   │
│   │   ├── models/
│   │   │   └── chat.py
│   │   │
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── data/
│   │   └── .gitkeep
│   │
│   ├── scripts/
│   │   ├── explore_data.py
│   │   ├── import_to_mongodb.py
│   │   ├── prepare_data.py
│   │   ├── test_connection.py
│   │   ├── test_executor.py
│   │   ├── test_full_flow.py
│   │   ├── test_graph_validation.py
│   │   ├── test_graph.py
│   │   └── test_query_generator.py
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

> The procurement CSV files and local environment files are intentionally excluded from version control.

---

## Data Preparation

The original procurement CSV dataset is prepared before being imported into MongoDB.

The data preparation scripts are located in:

```text
backend/scripts/
```

The main preparation workflow includes:

- Exploring the original dataset
- Cleaning and preparing the procurement records
- Importing the processed dataset into MongoDB
- Testing the MongoDB connection

The procurement data is then accessed by the AI assistant through the backend database layer.

The original and cleaned CSV files are excluded from Git because they are local dataset files and are not required to expose application source code.

---

## Query Safety and Validation

ProcureAI does not directly execute arbitrary database code produced by the LLM.

Instead, the LLM generates a structured analytical plan. The application then compiles the plan into MongoDB operations and validates the generated pipeline before execution.

The validator restricts aggregation operations to supported stages such as:

- `$match`
- `$group`
- `$sort`
- `$limit`
- `$project`
- `$count`
- `$unwind`

Potentially destructive stages such as `$out` and `$merge` are rejected.

This design separates natural-language interpretation from database execution and reduces the risk of executing unsupported LLM-generated operations.

---

## API Endpoints

The FastAPI backend provides the following endpoints:

### `GET /`

Returns basic API information.

### `GET /health`

Checks the MongoDB connection and returns the number of available procurement records.

### `GET /stats`

Returns basic dataset statistics, including the number of records, departments, and suppliers.

### `POST /chat`

Accepts a natural-language procurement question and runs the complete AI workflow.

Example request:

```json
{
  "question": "What are the top 5 departments by total spending?"
}
```

Example response structure:

```json
{
  "answer": "..."
}
```

---

# Local Setup

## Prerequisites

Ensure the following are installed:

- Python 3
- Node.js and npm
- Access to MongoDB
- A Google Gemini API key

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd procurement-ai-assistant
```

Replace `<repository-url>` with the URL of this GitHub repository.

---

## 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory.

Use `.env.example` as a reference:

```env
MONGODB_URI=your_mongodb_connection_string_here
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Replace the placeholder values in your local `.env` file with your own MongoDB connection string and Google Gemini API key.

The real `.env` file is intentionally excluded from Git and must not be committed because it contains private credentials.

---

## 3. Prepare and Import the Data

The procurement CSV files are intentionally excluded from version control.

Place the required procurement dataset inside:

```text
backend/data/
```

The scripts inside:

```text
backend/scripts/
```

can then be used to explore, prepare, and import the procurement data into MongoDB.

The project includes separate scripts for:

- Data exploration
- Data preparation and cleaning
- MongoDB import
- Database connection testing
- Query and agent testing

---

## 4. Run the Backend

From the `backend` directory, start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

The health endpoint can be used to verify the API and MongoDB connection:

```text
http://127.0.0.1:8000/health
```

---

## 5. Frontend Setup

Open another terminal.

From the project root, navigate to the frontend:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Open the local address displayed by Vite in the browser.

The default Vite development address is typically:

```text
http://localhost:5173
```

---

## Example Use Cases

ProcureAI can answer procurement questions involving:

- Spending analysis
- Department comparisons
- Supplier analysis
- Acquisition types
- Purchase-order counts
- Date-based filtering
- Ranked procurement results
- Aggregated procurement metrics

The assistant is designed to make procurement data accessible to users who may not know MongoDB or database query languages.

---

## Design Decisions

### Structured Query Planning

An early approach of generating database pipelines more directly from the LLM could produce structurally inconsistent queries.

ProcureAI instead separates natural-language interpretation from deterministic database compilation:

```text
Natural Language
      ↓
Structured Query Plan
      ↓
Deterministic Compiler
      ↓
Validated MongoDB Query
```

This gives the application more control over how database operations are constructed and prevents the LLM from directly executing unrestricted MongoDB operations.

### Separate Frontend and Backend

The React frontend is responsible for user interaction and presentation, while FastAPI manages the AI workflow, database communication, and API logic.

This separation keeps the architecture modular and easier to maintain.

### Grounded Answer Generation

The final response is generated from the retrieved database results. The answer-generation stage is instructed to base its response on those results rather than introduce unrelated external information.

---

## Limitations

This project is a prototype and currently has several limitations:

- It is designed specifically around the provided procurement dataset and its schema.
- Query capabilities are limited to the analytical operations supported by the query plan and compiler.
- LLM requests are subject to the availability and rate limits of the configured model provider.
- The application is intended for analytical, read-only interaction with procurement data.
- The current implementation runs locally and is not configured as a production deployment.
- The procurement dataset itself is not included in the repository.

---

## Future Improvements

Possible future improvements include:

- Conversation-aware follow-up questions
- Additional procurement analytics
- More advanced multi-step query planning
- Visual charts and dashboards
- Automated evaluation of generated queries
- Support for additional procurement datasets
- Production deployment and authentication

---

## Purpose

This project was developed as an AI engineering assessment to demonstrate the feasibility of combining an LLM-powered agent with MongoDB to provide a natural-language interface for procurement analytics.