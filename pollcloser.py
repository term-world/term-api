import couchsurf
import json
from datetime import datetime

def close_poll():
    # Call all active polls, present selection to user
    print("Time to close out a poll, eh?")
    print()
    poll_request_result = json.loads(couchsurf.get_request("latest-poll"))
    active_polls = poll_request_result["rows"]
    print("Here are all of the currently active polls: ")
    choice_index = 0
    for poll in active_polls:
        question = poll["value"]["question"]
        print(f"    {choice_index}: {question}")
        choice_index += 1
    print()
    user_choice = int(input("Please select the number of the poll you'd like to close: "))
    print()
    poll_selected = active_polls[user_choice]
    confirmation = input(f"Are you sure you'd like to close down the poll: {poll_selected['value']['question']}? [y/n] ")

    # Once user confirms their selection...
    if confirmation == "y":

        # Call all votes tied to the selected poll
        print()
        print("Closing poll and generating poll results...")
        poll_id = poll_selected['id']
        vote_request_result = json.loads(
            couchsurf.get_request(
                "poll-result-generator",
                id=poll_id))
        votes_to_count = vote_request_result['rows']
    
        # Define vote categories for tallying votes
        vote_categories = {}
        for option in poll_selected['value']['options']:
            vote_categories[option] = 0

        # Tally votes
        for vote in votes_to_count:
            vote_selection = vote['value']
            vote_categories[vote_selection] += 1
        print()
        print("Outcome of vote is as follows: ")
        print(f"    {vote_categories}")

        # Update poll doc in CouchDB with results and "inactive" flag
        poll_update_doc = {
            '_rev': poll_selected['value']['rev'],
            'type': "poll",
            'flag': "inactive",
            'submission_time': poll_selected['value']['submission_time'],
            'submission_timestamp': poll_selected['value']['submission_timestamp'],
            'closing_time': str(datetime.now()),
            'closing_timestamp': datetime.now().timestamp(),
            'question': poll_selected['value']['question'],
            'outcome': str(vote_categories),
            'scope': poll_selected['value']['scope']
        }
        couchsurf.put_request(poll_id, poll_update_doc)
        print()
        print("The above results have been neatly filed in my expansive drawers, gov'nor.")

    else:
        print("Guess we won't be doing that, gov'nor...")