from flask import Flask, request, jsonify
from database import create_connection, create_table
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

   # Initialize database
create_table()

   # Create a task
@app.route('/tasks', methods=['POST'])
def add_task():
       data = request.get_json()
       title = data.get('title')
       description = data.get('description', '')
       priority = data.get('priority', 'Medium')
       
       valid_priorities = ['Low', 'Medium', 'High']
       if not title:
           return jsonify({"error": "Title is required"}), 400
       if priority not in valid_priorities:
           return jsonify({"error": "Priority must be Low, Medium, or High"}), 400
       
       conn = create_connection()
       try:
           cursor = conn.cursor()
           cursor.execute('''
               INSERT INTO tasks (title, description, priority)
               VALUES (?, ?, ?)
           ''', (title, description, priority))
           conn.commit()
           task_id = cursor.lastrowid
           return jsonify({"id": task_id, "title": title, "description": description, "priority": priority, "completed": False}), 201
       except Error as e:
           return jsonify({"error": str(e)}), 500
       finally:
           conn.close()

   # Read all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
       conn = create_connection()
       try:
           cursor = conn.cursor()
           cursor.execute('SELECT id, title, description, priority, completed, created_at FROM tasks')
           tasks = cursor.fetchall()
           return jsonify([{
               "id": task[0],
               "title": task[1],
               "description": task[2],
               "priority": task[3],
               "completed": bool(task[4]),
               "created_at": task[5]
           } for task in tasks]), 200
       except Error as e:
           return jsonify({"error": str(e)}), 500
       finally:
           conn.close()

   # Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
       data = request.get_json()
       title = data.get('title')
       description = data.get('description')
       priority = data.get('priority')
       completed = data.get('completed')
       
       valid_priorities = ['Low', 'Medium', 'High']
       if priority and priority not in valid_priorities:
           return jsonify({"error": "Priority must be Low, Medium, or High"}), 400
       
       conn = create_connection()
       try:
           cursor = conn.cursor()
           cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
           task = cursor.fetchone()
           if not task:
               return jsonify({"error": "Task not found"}), 404
           
           updates = []
           params = []
           if title:
               updates.append("title = ?")
               params.append(title)
           if description is not None:
               updates.append("description = ?")
               params.append(description)
           if priority:
               updates.append("priority = ?")
               params.append(priority)
           if completed is not None:
               updates.append("completed = ?")
               params.append(completed)
           
           if updates:
               params.append(id)
               cursor.execute(f'UPDATE tasks SET {", ".join(updates)} WHERE id = ?', params)
               conn.commit()
           
           cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
           updated_task = cursor.fetchone()
           return jsonify({
               "id": updated_task[0],
               "title": updated_task[1],
               "description": updated_task[2],
               "priority": updated_task[3],
               "completed": bool(updated_task[4]),
               "created_at": updated_task[5]
           }), 200
       except Error as e:
           return jsonify({"error": str(e)}), 500
       finally:
           conn.close()

   # Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
       conn = create_connection()
       try:
           cursor = conn.cursor()
           cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
           task = cursor.fetchone()
           if not task:
               return jsonify({"error": "Task not found"}), 404
           
           cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
           conn.commit()
           return jsonify({"message": "Task deleted"}), 200
       except Error as e:
           return jsonify({"error": str(e)}), 500
       finally:
           conn.close()

   # Analytics endpoint
@app.route('/analytics', methods=['GET'])
def get_analytics():
       conn = create_connection()
       try:
           cursor = conn.cursor()
           cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = 1')
           completed = cursor.fetchone()[0]
           cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = 0')
           pending = cursor.fetchone()[0]
           cursor.execute('SELECT priority, COUNT(*) FROM tasks GROUP BY priority')
           priority_counts = cursor.fetchall()
           return jsonify({
               "completed_tasks": completed,
               "pending_tasks": pending,
               "priority_distribution": {row[0]: row[1] for row in priority_counts}
           }), 200
       except Error as e:
           return jsonify({"error": str(e)}), 500
       finally:
           conn.close()

if __name__ == '__main__':
       app.run(debug=True)