# Agentic Data Analysis Assistant

An autonomous AI agent that allows users to explore, query, and transform datasets (CSV/Excel) using natural language. Built with FastAPI, Pydantic AI, and DuckDB.

## 🚀 Features
- **Natural Language to SQL**: Query your data without writing a single line of SQL.
- **Autonomous Transformations**: Delete columns, update values, or clean data via chat.
- **DuckDB Integration**: High-performance analytical engine for local file processing.
- **Stateful File Management**: Modified data is saved back to disk and available for instant download.


## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Agent Orchestration**: Pydantic AI
- **LLM**: Google Gemini (3.1 Flash Lite)
- **Database Engine**: DuckDB
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5, Marked.js)

## 📋 Prerequisites
- Python 3.9+
- A Google Gemini API Key

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/project-name.git
   cd project-name
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API Key:**
   Create a `.env` file in the root directory:
   ```bash
   GOOGLE_API_KEY='your_api_key_here'
   ```

## 🏃 Running the Application

1. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the UI:**
   Open your browser and navigate to `http://127.0.0.1:8000`

## 📂 Project Structure
- `main.py`: FastAPI backend and file handling logic.
- `agent.py`: Pydantic AI agent definition and DuckDB tools.
- `index.html`: Dark-mode frontend interface.
- `uploads/`: Directory where processed datasets are stored.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
Distributed under the MIT License.