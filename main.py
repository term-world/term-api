import yaml
import json

from flask import Flask, jsonify, request
import couchsurf


app = Flask(__name__)

fh = open("config.yaml")
data = yaml.load(fh, Loader=yaml.CLoader)

@app.route('/pollwatcher', methods=['POST'])
def watcher():
  if request.method == 'POST':
    poll = json.loads(couchsurf.get_request())
    user = request.json["user"]
    payload = {
      "message": f'{user}, {poll["rows"][0]["key"]["question"]}',
      "votes": poll["rows"][0]["key"]["options"]
    }
    return jsonify(payload)
  else:
    return {"message": "Method not supported."}

@app.route('/pollreporter', methods=['POST'])
def reporter():
  if request.method == 'POST':
    couchsurf.post_request(request.json)
    return "OK"
  else:
    return {"message": "Method not supported."}
    


if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)
