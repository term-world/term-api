import yaml
import json

from flask import Flask, jsonify, request
import couchsurf

app = Flask(__name__)

@app.route('/pollwatcher', methods=['POST'])
def watcher():
  if request.method == 'POST':
    user = request.json["user"]
    request_result = json.loads(couchsurf.get_request())
    all_polls = request_result["rows"]
    poll_found = False
    for poll in all_polls:
      if not rollcall2(poll["id"], user):
        selected_poll = poll
        poll_found = True
        break
    if poll_found == True:
      payload = {
        "message": f'{user}, {selected_poll["value"]["question"]}',
        "votes": selected_poll["value"]["options"],
        "id": selected_poll["id"]
      }
      return jsonify(payload)
    else:
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

def rollcall2(id, username):
  request_result = json.loads(couchsurf.get_request("vote-finder", id))
  votes_to_search = request_result["rows"]
  didja_vote = False
  for vote in votes_to_search:
    if vote["value"] == username:
      didja_vote = True
  return didja_vote

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)