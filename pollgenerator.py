import couchsurf

question = input("Enter polling question to ask: ")
if question:
    options = []
    while True:
        option = input("Enter possible response: ")
        if not option: break
        options.append(option)
    scope = input("Enter a neighborhood to conduct poll in, or leave field blank to conduct poll globally: ").lower()
    if not scope: scope = "global"
    confirmation = input(f"Are you sure you'd like to submit the polling question '{question}' with possible options {options} to the '{scope}' community? [y/n] ")
    if confirmation == "y":
        poll = {
            'type': "poll",
            'question': question,
            'options': options,
            'scope': scope
        }
        couchsurf.post_request(poll)
