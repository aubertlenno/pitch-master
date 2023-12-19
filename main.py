import login
import register

def main():
    current_action = "login"

    while True:
        if current_action == "login":
            action = login.show_login()
            if action == "register":
                current_action = "register"
            else:
                break
        elif current_action == "register":
            action = register.show_register()
            if action == "login":
                current_action = "login"
            else:
                break

if __name__ == "__main__":
    main()