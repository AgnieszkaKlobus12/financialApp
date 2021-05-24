import base64
import os


def register_user_controller(login, passwd):
    if " " in login or " " in passwd:
        raise ValueError("Login and passwords must not contain spaces!")
    if not any(char.isdigit() for char in passwd) or passwd.isupper() or passwd.islower() or len(passwd) < 8:
        raise ValueError("Password too weak!\nPassword must have at least 8 characters, include at least "
                         "one digit, one uppercase letter and one lowercase letter.")
    class_dir = os.path.dirname(__file__)
    file = os.path.join(class_dir, "users.bin")
    users_file = open(file, "r", encoding="utf-8")
    users = users_file.readlines()
    users_file.close()
    for user in users:
        user = user.split(" ")
        if user[0] == login:
            raise ValueError("User with chosen login already exists")
    users_file.close()
    users_file = open(file, "a", encoding="utf-8")
    users_file.write(login + " " + str(base64.b64encode(passwd.encode("utf-8"))) + "\n")
    users_file.close()


def login_user_controller(login, passwd):
    if " " in login or " " in passwd:
        raise ValueError("Invalid login or password")
    class_dir = os.path.dirname(__file__)
    file = os.path.join(class_dir, "users.bin")
    users_file = open(file, "r", encoding="utf-8")
    users = users_file.readlines()
    users_file.close()
    for user in users:
        user = user.split(" ")
        if user[0] == login:
            if user[1].rstrip() == str(base64.b64encode(passwd.encode("utf-8"))):
                return True
            else:
                raise ValueError("Invalid password")
    raise ValueError("User not found")
