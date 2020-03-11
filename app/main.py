import os

from flask import Flask, request, jsonify
#  from redis import Redis
#  from rq import Queue

from .exceptions import InvalidData
from .tasks import predict_task

#  conn = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379))
#  queue = os.getenv("REDIS_QUEUE", "machine-learning")
#  q = Queue(queue, connection=conn)

app = Flask(__name__)


@app.errorhandler(InvalidData)
def handle_invalid_data(error):
    """
        Error handler for feature names mismatch
        When all 27 inputs are not provided api should return an error
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/predict', methods=['POST'])
def get_prediction():
    #  req = request.get_json()
    #  user_id = req['parameters']['user_id']
    #  callback_url = req.get('callback_url', os.getenv("CALLBACK_URL", None))
    #  request_id = req['request_id']
    #  interval = req['parameters']['interval']

    #  job = q.enqueue(predict_task, request_id, user_id, callback_url, interval)
    #

    return jsonify({
        'request_id': request_id,
        #  'queued_at': job
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
