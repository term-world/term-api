import yaml
import json

from flask import Flask, jsonify, request
import couchsurf

app = Flask(__name__)

@app.route('/pollwatcher', methods=['POST'])
def watcher():
  if request.method == 'POST':
    user = request.json["user"]
    if not rollcall(user):
      poll = json.loads(couchsurf.get_request())
      payload = {
        "message": f'{user}, {poll["rows"][-1]["value"]["question"]}',
        "votes": poll["rows"][-1]["value"]["options"],
        "id": poll["rows"][-1]["id"]
      }
      return jsonify(payload)
    return jsonify({})
  else:
    return {"message": "Method not supported."}

@app.route('/pollreporter', methods=['POST'])
def reporter():
  if request.method == 'POST':
    couchsurf.post_request(request.json)
    return "OK"
  else:
    return {"message": "Method not supported."}

def rollcall(username):
  response = couchsurf.query_request(
    user=username
  )
  print(response)
  if len(response['docs']):
    return False
  return True

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)