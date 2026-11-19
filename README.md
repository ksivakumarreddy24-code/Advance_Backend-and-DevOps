# Todo List API

A small FastAPI service for a todo list, stored in a local SQLite database.
You can create todos, list them all, update them and delete them.

## Project structure

```text
todo-list/
├── main.py            # FastAPI app, request/response models and routes
├── functions.py       # SQLite connection, Todo table and the CRUD functions
└── requirements.txt
```

The database file `todo.db` is created automatically next to `main.py` the first time the app starts.

## Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/malnadhudga/todo-list.git
cd todo-list
```

### 2. Create and activate a virtual environment

Create the venv:

```bash
python -m venv venv
```

Activate it (pick your terminal):

**Windows – PowerShell**
```powershell
venv\Scripts\Activate.ps1
```
> If PowerShell says running scripts is disabled, run this once, then activate again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

**Windows – Command Prompt (cmd)**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
source venv/bin/activate
```

When it's active you'll see `(venv)` at the start of your terminal prompt. To leave it later, run `deactivate`.

### 3. Install the requirements

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the server

```bash
python -m uvicorn main:app --reload
```

Open the interactive docs at http://127.0.0.1:8000/docs

## Endpoints

| # | Action | Method | Endpoint | Success |
|---|---|---|---|---|
| 1 | Create a todo | `POST` | `/todos` | 201 |
| 2 | Read all todos | `GET` | `/todos` | 200 |
| 3 | Update a todo (partial) | `PATCH` | `/todos/{todo_id}` | 200 |
| 4 | Delete a todo | `DELETE` | `/todos/{todo_id}` | 200 |

### `POST /todos` — Create a todo

| Field | Type | Rules | Meaning |
|---|---|---|---|
| `title` | string | required, 1 – 200 chars | What needs doing |
| `description` | string | optional, max 1000 chars | Extra detail |
| `completed` | boolean | optional, default `false` | Whether it's done |

```json
// request
{"title": "Buy milk", "description": "2 litres"}

// response (201)
{"id": 1, "title": "Buy milk", "description": "2 litres", "completed": false}
```

### `GET /todos` — Read all todos

Returns every todo, ordered by `id`.

```json
// response (200)
[
  {"id": 1, "title": "Buy milk", "description": "2 litres", "completed": false},
  {"id": 2, "title": "Gym", "description": null, "completed": true}
]
```

### `PATCH /todos/{todo_id}` — Update a todo

Send only the fields you want to change (`title`, `description`, `completed`).

```json
// request  PATCH /todos/1
{"completed": true}

// response (200)
{"id": 1, "title": "Buy milk", "description": "2 litres", "completed": true}
```

- **404** if the todo doesn't exist
- **422** if the body is empty (`"Nothing to update"`) or a field is invalid

### `DELETE /todos/{todo_id}` — Delete a todo

```json
// response (200)
{"message": "Todo deleted"}
```

- **404** if the todo doesn't exist

Invalid input (for example an empty `title`) is rejected with HTTP **422** and a message naming the bad field.

## Run with Docker

```bash
docker build -t todo-list .
docker run -p 8000:8000 todo-list
```

The SQLite file lives inside the container, so todos are lost when the container is removed.
