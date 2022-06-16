import couchsurf
import json

def result_lookup():
    closed_poll_request = json.loads(couchsurf.get_request("poll-result-viewer"))
    print("Alright then, gov'nor--let's dig up some poll results...")
    print()