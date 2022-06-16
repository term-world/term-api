import couchsurf
from datetime import datetime

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
            print("The poll is stuffed into myriad envelopes, to be sent out to the denizens of term-world.")
            print("Each one has a bright red stamp that reads: 'From the Desk of the Gov'nor'...")
        else:
            print()
            print("Guess we won't be doing that, gov'nor...")
