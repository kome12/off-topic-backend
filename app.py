from flask import Flask, jsonify

api = Flask(__name__)

def start_api():
    api.run()

@api.route('/session', methods=['GET'])
def index():
    return jsonify('Backend is alive'), 200


if __name__ == "__main__":
    start_api()