import os, requests, json, datetime
import hashlib

def token(request, token):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://127.0.0.1:5000/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        access = json.loads(response.text)
        exp = access["exp"]
        time = datetime.datetime.now()
        cur_time = int(time.strftime("%Y%m%d%H%M%S"))
        if exp < cur_time:
            return None, ("Token Expired", 401)
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    sha = hashlib.sha3_256()
    sha.update(bytes(auth.password, "utf-8"))
    hash_pass = sha.hexdigest()

    basicAuth = (auth.username, hash_pass)

    response = requests.post(
        f"http://127.0.0.1:5000/login", auth=basicAuth
    )

    

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
def register(request):
    auth = request.authorization
    if not auth:
        return None, ("missing information", 401)

    sha = hashlib.sha3_256()
    sha.update(bytes(auth.password, "utf-8"))
    hash_pass = sha.hexdigest()

    basicAuth = (auth.username, hash_pass)

    response = requests.post(
        f"http://127.0.0.1:5000/register", auth=basicAuth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
