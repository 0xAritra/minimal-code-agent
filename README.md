# Code Agent

Gemini-powered AI coding agent for file operations and Python execution in a sandbox directory (`./calculator`).

## Features
- List files/directories
- Read/write file contents
- Execute Python files with optional arguments
- Conversational tool-calling loop via Gemini API

## Installation
```bash
uv sync  # Recommended, or pip install -e .
```

## Setup
1. Create `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
2. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage
```bash
python main.py "List files and read main.py" [--verbose]
```
- `--verbose`: Show detailed logs and token usage.
- Provide any coding task as the prompt; the agent will plan and execute tool calls.
- All operations are relative to `./calculator` for security.

## Project Structure
```
.
├── main.py              # Agent core (Gemini integration + tool loop)
├── functions/           # Tool implementations + schemas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/          # Sandbox working directory
├── pyproject.toml      # Dependencies (google-genai, python-dotenv)
├── config.py           # Config
├── tests.py            # Root tests (if any)
└── README.md
```

## Available Tools
| Function            | Description                          |
|---------------------|--------------------------------------|
| `get_files_info`    | List files and directories           |
| `get_file_content`  | Read file contents                   |
| `write_file`        | Write or overwrite file              |
| `run_python_file`   | Execute Python file with args        |

## Example
```bash
python main.py "Create hello.py with print('Hello from agent!')" --verbose
```

