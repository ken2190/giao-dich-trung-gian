import requests
import random

s = 'zxcvbnmasdfghjklqwertyuiop'

def random_():
    r = ''
    for i in range(20):
        r += random.choice(s)
    return r

for i in range(1):
    uName = random_()
    fName = "Nguyen Quang Thao"
    password = "123456"
    email = "%s@gmail.com" % uName

    data = {
        "wsRequest": {
            "username": uName,
            "password": password,
            "email": email,
            "full_name": fName
        }
    }

    r = requests.post("https://00a3-113-167-239-113.ngrok.io/user", data=data)
    print(r, uName)
    print(data)