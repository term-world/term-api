import couchsurf
from datetime import datetime

question = input("Enter polling question to ask: ")
if question:
    options = []
    while True:
        option = input("Enter possible response: ")
        if not option: break
        options.append(option)
    scope = input("Enter a neighborhood to conduct poll in, or leave field blank to conduct poll globally: ").lower()
    if not scope: scope = "global"
    active_days = float(input("How many days would you like to keep the poll active for? "))
    confirmation = input(f"Are you sure you'd like to submit the polling question '{question}' with possible options {options} to the '{scope}' community for {active_days} days? [y/n] ")
    if confirmation == "y":
        poll = {
            'type': "poll",
            'submission_time': str(datetime.now()),
            'active_period': f"{active_days} days",
            'timestamp': datetime.now().timestamp(),
            'expiry': datetime.now().timestamp() + (active_days * 86400),
            'question': question,
            'options': options,
            'scope': scope
        }
        couchsurf.post_request(poll)
