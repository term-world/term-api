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
  #if request.method == 'POST':
    #response = couchsurf.get_request(
      #'user-finder',
      #user=username
    #)
    #status = json.loads(response)
    #if status["total_rows"] > 0:
      #return True
    #return False
  #else:
    #return {"message":"Method not supported."}
  return False #DELETE THIS ONCE FIXED!

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)