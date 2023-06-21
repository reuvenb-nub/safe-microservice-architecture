import os, requests, json


def create(request, user_id):
    # Get task details from the request body
    title = request.json.get('title')
    description = request.json.get('description')
    due_date = request.json.get('due_date')

    task_data = {
        'user_id': user_id,
        'title': title,
        'description': description,
        'due_date': due_date
    }

    # Convert the task data to JSON
    payload = json.dumps(task_data)

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
    f"http://127.0.0.1:6000/create", data=payload, headers=headers
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def get(request, user_id):
    response = requests.get(
    f"http://127.0.0.1:6000/get?user_id={user_id}"
    )
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, (response.json(), response.status_code)

def remove(request, user_id, task_id):
    response = requests.delete(
    f"http://127.0.0.1:6000/remove/{task_id}?user_id={user_id}"
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)