import shelve
import yaml

from flask import Flask, jsonify, request

app = Flask(__name__)

fh = open("config.yaml")
data = yaml.load(fh)

@app.route('/pollwatcher', methods=['POST'])
def watcher():
  if request.method == 'POST':

    polls = shelve.open(data["POLL_DB"])
    poll = next(iter(polls))

    user = request.json["user"]

    payload = {
      "message": f"{user}, {polls[poll]['question']}",
      "votes": polls[poll]["options"]
    }

    polls.close()

    return jsonify(payload)

  else:
    return {
      "message": "Method not supported."
    }

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)
