import pollgenerator
import pollcloser
import resultviewer

def display_menu(menu_options: dict) -> int:
    number_of_options = len(menu_options)
    for i in range(number_of_options):
        print(f"    {i}: {menu_options[i]}")
    print()
    user_choice = int(input("Please select an option from the above menu: "))
    return user_choice

def startup_menu():
    print("What would you like to do today, gov'nor?")
    startup_menu_options = {
        0: "Generate a poll",
        1: "Close a poll",
        2: "View poll results",
        3: "Calmly step away from the talking desk"
    }
    user_choice = display_menu(startup_menu_options)
    print()
    if user_choice == 0:
        pollgenerator.generate_poll()
    elif user_choice == 1:
        pollcloser.close_poll()
    elif user_choice == 2:
        resultviewer.result_lookup()
    elif user_choice == 3:
        print("Take care, gov'nor!")

def main():
    print()
    print("Ello, gov'nor!")
    print()
    startup_menu()


if __name__ == "__main__":
    main()