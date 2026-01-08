#!/usr/bin/env python3
"""
Todo List Manager - A simple command-line todo list application.
"""

import json
import os
from datetime import datetime
from pathlib import Path


TODO_FILE = "todos.json"


class TodoManager:
    def __init__(self, filename=TODO_FILE):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Load todos from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_todos(self):
        """Save todos to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.todos, f, indent=2)
            return True
        except IOError:
            print(f"Error: Could not save to {self.filename}")
            return False
    
    def add_todo(self, task):
        """Add a new todo item."""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"✓ Added: {task}")
    
    def list_todos(self, show_completed=True):
        """List all todos."""
        if not self.todos:
            print("No todos found. Add one with 'add <task>'")
            return
        
        print("\n" + "=" * 50)
        print("TODO LIST")
        print("=" * 50)
        
        for todo in self.todos:
            if not show_completed and todo["completed"]:
                continue
            
            status = "✓" if todo["completed"] else "○"
            task = todo["task"]
            created = todo.get("created_at", "Unknown")
            
            print(f"{todo['id']}. [{status}] {task}")
            print(f"   Created: {created}")
        
        print("=" * 50)
        print()
    
    def complete_todo(self, todo_id):
        """Mark a todo as completed."""
        try:
            todo_id = int(todo_id)
            for todo in self.todos:
                if todo["id"] == todo_id:
                    todo["completed"] = True
                    self.save_todos()
                    print(f"✓ Completed: {todo['task']}")
                    return
            print(f"Error: Todo #{todo_id} not found")
        except ValueError:
            print("Error: Please provide a valid todo ID")
    
    def delete_todo(self, todo_id):
        """Delete a todo item."""
        try:
            todo_id = int(todo_id)
            for i, todo in enumerate(self.todos):
                if todo["id"] == todo_id:
                    task = todo["task"]
                    del self.todos[i]
                    # Reassign IDs
                    for j, t in enumerate(self.todos):
                        t["id"] = j + 1
                    self.save_todos()
                    print(f"✓ Deleted: {task}")
                    return
            print(f"Error: Todo #{todo_id} not found")
        except ValueError:
            print("Error: Please provide a valid todo ID")
    
    def get_stats(self):
        """Get statistics about todos."""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo["completed"])
        pending = total - completed
        
        print(f"\nStatistics:")
        print(f"  Total: {total}")
        print(f"  Completed: {completed}")
        print(f"  Pending: {pending}")
        print()


def print_help():
    """Print help message."""
    help_text = """
Todo Manager - Commands:
  add <task>        - Add a new todo
  list              - List all todos
  complete <id>     - Mark todo as completed
  delete <id>      - Delete a todo
  stats             - Show statistics
  help              - Show this help message
  quit/exit         - Exit the program
"""
    print(help_text)


def main():
    """Main function."""
    print("=" * 50)
    print("Welcome to Todo Manager!")
    print("=" * 50)
    print("Type 'help' for commands or 'quit' to exit\n")
    
    manager = TodoManager()
    
    while True:
        try:
            command = input("todo> ").strip()
            
            if not command:
                continue
            
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None
            
            if cmd in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif cmd == 'help' or cmd == 'h':
                print_help()
            elif cmd == 'add' and arg:
                manager.add_todo(arg)
            elif cmd == 'list' or cmd == 'ls':
                manager.list_todos()
            elif cmd == 'complete' and arg:
                manager.complete_todo(arg)
            elif cmd == 'delete' and arg:
                manager.delete_todo(arg)
            elif cmd == 'stats':
                manager.get_stats()
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
