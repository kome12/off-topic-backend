import os
from flask import Flask, jsonify
import spotify_api
from dotenv import load_dotenv

api = Flask(__name__)

load_dotenv()

def start_api():
    api.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)

@api.route('/session', methods=['GET'])
def index():
    return jsonify('Backend is alive'), 200

@api.route('/off-topic', methods=['GET'])
def get_off_topic_episodes():
    off_topic_id = os.environ['SPOTIFY_OFF_TOPIC_SPOTIFY_ID']
    return spotify_api.get_spotify_episodes(off_topic_id)

    # return jsonify('Return off-topic episodes'), 200

@api.route('/off-topic/all', methods=['GET'])
def get_all_off_topic_episodes():
    off_topic_id = os.environ['SPOTIFY_OFF_TOPIC_SPOTIFY_ID']
    return spotify_api.get_all_spotify_episodes(off_topic_id)

if __name__ == "__main__":
    start_api()