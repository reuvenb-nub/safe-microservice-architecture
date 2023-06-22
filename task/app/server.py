import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'auth_user'
app.config["MYSQL_PASSWORD"] = 'Auth123'
app.config["MYSQL_DB"] = 'svc'

mysql = MySQL(app)

@app.route('/create', methods=['POST'])
def create_task():
    # Get task details from the request body
    title = request.json.get('title')
    description = request.json.get('description')
    due_date = request.json.get('due_date')
    user_id = request.json.get('user_id')

    # Insert the task into the database
    cursor = mysql.connection.cursor()
    query = "INSERT INTO tasks (user_id, title, description, due_date) VALUES (%s, %s, %s, %s)"
    values = (user_id, title, description, due_date)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/get', methods=['GET'])
def get_tasks():
    # Get user_id from query parameters or request headers (authentication token)
    user_id = request.args.get('user_id')
    print(user_id)

    # Retrieve tasks for the user from the database
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM tasks WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    cursor.close()

    response = requests.get(
        f"http://127.0.0.1:1234/"
    )
    print(response.text)

    # Convert task data into a JSON response
    task_list = []
    for task in tasks:
        task_data = {
            'id': task[0],
            'title': task[2],
            'description': task[3],
            'due_date': task[4]
        }
        task_list.append(task_data)

    return jsonify({'tasks': task_list})

@app.route('/remove/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete the task from the database
    cursor = mysql.connection.cursor()
    user_id = request.args.get('user_id')

    # Check if the task exists
    query = "SELECT id FROM tasks WHERE id = %s AND user_id = %s"
    cursor.execute(query, (task_id, user_id,))
    task = cursor.fetchone()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Delete the task
    delete_query = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
    cursor.execute(delete_query, (task_id, user_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)

