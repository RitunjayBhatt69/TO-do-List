To-Do List REST API

A RESTful API built with Python (Flask) and SQLite to manage tasks with CRUD operations, task prioritization, and basic analytics. Deployed on Heroku for live access.

Features





CRUD Operations: Create, read, update, and delete tasks.



Task Prioritization: Assign Low, Medium, or High priority to tasks.



Analytics: View counts of completed/pending tasks and priority distribution.



Tested: Validated endpoints using Postman.



Deployed: Live demo on Heroku.

API Endpoints





POST /tasks: Create a task (e.g., {"title": "Study", "description": "Revise chapters", "priority": "High"}).



GET /tasks: Retrieve all tasks.



PUT /tasks/: Update a task (e.g., {"completed": true}).



DELETE /tasks/: Delete a task.



GET /analytics: Get task statistics (completed, pending, priority distribution).

Setup





Clone the repository:

git clone <your-repo-url>
cd todo-api



Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Run the app:
python main.py

Test APIs using Postman at http://127.0.0.1:5000.

Live Demo

Heroku Link

Technologies Used
Python, Flask, SQLite
Postman for testing
Heroku for deployment


Future Improvements
Add user authentication with API keys.
Implement task categories (e.g., Work, Personal).
Add filtering for tasks (e.g., by priority or completion status).