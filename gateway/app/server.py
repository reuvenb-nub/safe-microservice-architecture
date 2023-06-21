import os, json
from flask import Flask, request, jsonify
from auth import auth
from task import task
from flask_mysqldb import MySQL
import hashlib

server = Flask(__name__)

# config
server.config["MYSQL_HOST"] = 'localhost'
server.config["MYSQL_USER"] = 'auth_user'
server.config["MYSQL_PASSWORD"] = 'Auth123'
server.config["MYSQL_DB"] = 'gateway'


mysql = MySQL(server)
@server.route('/')
def hello():
    return 'hello'

@server.route("/register", methods=["POST"])
def register():
    res, err = auth.register(request)
    if not err:
        return res
    else:
        return err

@server.route("/login", methods=["POST"])
def login():
    token, err = auth.login(request)
    if not err:
        sha = hashlib.sha3_256()
        sha.update(bytes(token, "utf-8"))
        opaque = sha.hexdigest()

        #insert into database
        cur = mysql.connection.cursor()
        res = cur.execute(
            "INSERT INTO opaque (auth_key, opaque_key) VALUES (%s, %s)", (token, opaque,)
        )
        mysql.connection.commit()
        return opaque
    else:
        return err


@server.route("/create", methods=["POST"])
def create():
    opaque = request.headers["Authorization"]
    cursor = mysql.connection.cursor()
    # Check if the task exists
    query = "SELECT auth_key FROM opaque WHERE opaque_key = %s "
    cursor.execute(query, (opaque,))
    token = cursor.fetchone()
    token = token[0]

    access, err = auth.token(request, token)
    if err:
        if err[1] == 401:
            query = "DELETE FROM opaque WHERE opaque_key = %s "
            cursor.execute(query, (opaque,))
            mysql.connection.commit()
            cursor.close()
        return err

    access = json.loads(access)

    if access["admin"]:
        task.create(request, access["id"])

        return "success!", 200
    else:
        return "not authorized", 401
    
@server.route("/delete/<int:task_id>", methods=["DELETE"])
def delete(task_id):
    opaque = request.headers["Authorization"]
    cursor = mysql.connection.cursor()
    # Check if the task exists
    query = "SELECT auth_key FROM opaque WHERE opaque_key = %s "
    cursor.execute(query, (opaque,))
    token = cursor.fetchone()
    token = token[0]

    access, err = auth.token(request, token)
    if err:
        if err[1] == 401:
            query = "DELETE FROM opaque WHERE opaque_key = %s "
            cursor.execute(query, (opaque,))
            mysql.connection.commit()
            cursor.close()
        return err

    access = json.loads(access)

    if access["admin"]:
        task.remove(request, access["id"], task_id)

        return "success!", 200
    else:
        return "not authorized", 401

@server.route("/retrival", methods=["GET"])
def retrieval():
    opaque = request.headers["Authorization"]
    cursor = mysql.connection.cursor()
    # Check if the task exists
    query = "SELECT auth_key FROM opaque WHERE opaque_key = %s "
    cursor.execute(query, (opaque,))
    token = cursor.fetchone()
    token = token[0]

    access, err = auth.token(request, token)
    if err:
        if err[1] == 401:
            query = "DELETE FROM opaque WHERE opaque_key = %s "
            cursor.execute(query, (opaque,))
            mysql.connection.commit()
            cursor.close()
        return err

    access = json.loads(access)

    if access["admin"]:
        data = task.get(request, access["id"])
        print(data)
        return jsonify(data), 200
    else:
        return "not authorized", 401


@server.route("/logout", methods=["GET"])
def logout():
    opaque = request.headers["Authorization"]
    cursor = mysql.connection.cursor()
    # Check if the task exists
    query = "SELECT auth_key FROM opaque WHERE opaque_key = %s "
    cursor.execute(query, (opaque,))
    token = cursor.fetchone()
    token = token[0]

    access, err = auth.token(request, token)
    if err:
        if err[1] == 401:
            query = "DELETE FROM opaque WHERE opaque_key = %s "
            cursor.execute(query, (opaque,))
            mysql.connection.commit()
            cursor.close()
        return err

    access = json.loads(access)

    if access["admin"]:
        query = "DELETE FROM opaque WHERE opaque_key = %s "
        cursor.execute(query, (opaque,))
        mysql.connection.commit()
        cursor.close()
        return "Success for deleting", 200
    return "failure", 500

context = ('./certificate.crt', './ec-private-key.pem')

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)