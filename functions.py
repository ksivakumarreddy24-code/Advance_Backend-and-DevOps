from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import Session, declarative_base

# ---------- Database connection ----------

DB_URL = "sqlite:///todo.db"
engine = create_engine(DB_URL)

# ---------- Tables / Models ----------

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False, nullable=False)


# Create the table if it doesn't exist.
Base.metadata.create_all(engine)


def todo_to_dict(todo):
    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    }


# ---------- CREATE ----------

def create_todo(title, description=None, completed=False):
    with Session(engine) as session:
        todo = Todo(title=title, description=description, completed=completed)

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return todo_to_dict(todo)


# ---------- READ ALL ----------

def get_todos():
    with Session(engine) as session:
        todos = session.query(Todo).order_by(Todo.id).all()
        return [todo_to_dict(todo) for todo in todos]


# ---------- UPDATE (partial) ----------

def update_todo(todo_id, changes):
    """changes = dict with only the fields to update. Returns None if the todo doesn't exist."""
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if todo is None:
            return None

        for field, value in changes.items():
            setattr(todo, field, value)

        session.commit()
        return todo_to_dict(todo)


# ---------- DELETE ----------

def delete_todo(todo_id):
    """Returns False if the todo doesn't exist."""
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if todo is None:
            return False

        session.delete(todo)
        session.commit()
        return True
