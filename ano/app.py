from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def get_random_joke():
    url = "https://api.chucknorris.io/jokes/random"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify({'joke': data["value"]})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1234)