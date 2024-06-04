import json
from flask import Flask, jsonify, request,session,make_response
from flask_cors import CORS
import jwt
import requests
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_jwt_secret_key'  # Set a secret key for JWT
CORS(app)   

users = {
    'admin': 'password'
}

@app.route('/login', methods=['POST'])
def login():
    # username = request.form['username']
    # password = request.form['password']
    # if username in users and users[username] == password:
    #     access_token = create_access_token(identity=username)
    #     response = jsonify({'login': True})
    #     response.set_cookie('access_token_cookie', access_token)
    #     return response
    # else:
    #     return jsonify({'login': False}), 401
    auth = request.json
    try:
        username=auth['username']
        password=auth['password']
        if users[username]==password:
            token = jwt.encode({'user': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token': token})
    except requests.RequestException as e:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    
@app.route('/logout')
def logout():
    response = jsonify({'logout': True})
    response.delete_cookie('access_token_cookie')
    return response

def read_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = read_config('config.json')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/get_data', methods=['GET'])
@token_required
def get_new_data():
    heatmap_data = {
    "type": "FeatureCollection",
    "features": []
    }
    data_url = "http://localhost:9090/get_data"
    try:
        response = requests.get(data_url)
        response.raise_for_status()
        external_data = response.json()
        heatmap_data["features"] = external_data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500


    return jsonify(heatmap_data)

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify({"status":random.randint(0,1)})



   


if __name__ == '__main__':
   app.run(port=8585)