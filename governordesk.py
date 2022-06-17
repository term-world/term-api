import couchsurf
import json
from datetime import datetime

def display_menu(menu_prompt: str, menu_options: dict) -> int:
    print(menu_prompt)
    number_of_options = len(menu_options)
    for i in range(number_of_options):
        print(f"    {i}: {menu_options[i]}")
    print()
    user_choice = int(input("Please select an option from the above menu: "))
    return user_choice

def startup_menu():
    startup_menu_prompt = "What would you like to do today, gov'nor?"
    startup_menu_options = {
        0: "Generate a poll",
        1: "Close a poll",
        2: "View poll results",
        3: "Calmly step away from the talking desk"
    }
    user_choice = display_menu(startup_menu_prompt, startup_menu_options)
    print()
    if user_choice == 0:
        generate_poll()
    elif user_choice == 1:
        close_poll()
    elif user_choice == 2:
        result_lookup()
    elif user_choice == 3:
        print("Take care, gov'nor!")

def generate_poll():
    print("Let's roll up our sleeves and make a poll, gov'nor!")
    question = input("    Enter polling question to ask: ")
    if question:
        options = []
        while True:
            option = input("    Enter possible response: ")
            if not option: break
            options.append(option)
        scope = input("    Enter a neighborhood to conduct poll in, or leave field blank to conduct poll globally: ").lower()
        if not scope: scope = "global"
        #active_days = float(input("How many days would you like to keep the poll active for? "))
        print()
        confirmation = input(f"Are you sure you'd like to submit the polling question '{question}' with possible options {options} to the '{scope}' community? [y/n] ").lower()
        if confirmation == "y":
            poll = {
                'type': "poll",
                'flag': "active",
                'submission_time': str(datetime.now()),
                #'active_period': f"{active_days} days",
                'submission_timestamp': datetime.now().timestamp(),
                #'expiry': datetime.now().timestamp() + (active_days * 86400),
                'question': question,
                'options': options,
                'scope': scope
            }
            couchsurf.post_request(poll)
            print()
            print("The poll is stuffed into myriad envelopes, all to be sent out to the denizens of term-world.")
            print("Each one has a bright red stamp that reads: 'From the Desk of the Gov'nor'...")
        else:
            print()
            print("Guess we won't be doing that, gov'nor...")

def close_poll():
    # Call all active polls, present selection to user
    print("Time to close out a poll, eh?")
    print()
    poll_request_result = json.loads(couchsurf.get_request("latest-poll"))
    active_polls = poll_request_result["rows"]
    closing_menu_prompt = "Here are all of the currently active polls, gov. Please select one to close."
    closing_menu_options = {}
    option_index = 0
    for poll in active_polls:
        question = poll["value"]["question"]
        closing_menu_options[option_index] = question
        option_index += 1
    user_choice = display_menu(closing_menu_prompt, closing_menu_options)
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

def result_lookup():
    closed_poll_request = json.loads(couchsurf.get_request("poll-result-viewer"))
    closed_polls = closed_poll_request["rows"]
    print("Alright then, gov'nor--let's dig up some poll results...")
    print()
    print("Here's what I've got on top o' the stack--the last ten polls closed:")
    print()
    for i in range(10):
        if i < len(closed_polls):
            question = closed_polls[i]["value"][0]
            outcome = closed_polls[i]["value"][1]
            print(f"    Polling question: {question}")
            print(f"    Polling outcome: {outcome}")
            print()
        else:
            print("    Oh, dear. Seems those are all the polls I've got, actually.")
            print("    I wonder if some scrappy ruffian broke into my drawers...")
            print()
            break
    finished = input("Didja find what you were looking for there, gov? [y/n] ").lower()
    if finished == "y":
        print()
        print("Very well then! Take care, gov'nor!")
    elif finished == "n":
        print()
        print("Very well! Time to roll up our sleeves, gov'nor!")


def main():
    print()
    print("Ello, gov'nor!")
    print()
    startup_menu()


if __name__ == "__main__":
    main()