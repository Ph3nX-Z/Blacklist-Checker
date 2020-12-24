import os
import re


from flask import Flask, session, request, render_template

app = Flask(__name__)

app.secret_key = os.urandom(24)

def is_email_address_valid(email):
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True
@app.route('/', methods=['GET','POST'])
def index():
    errors = ''
    if request.method == "GET": 
        return render_template("index.html", errors=errors)
    else:
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        if not name or not username:
            errors = "Please enter all the fields."
        if not errors:
            if email:
                if not is_email_address_valid(email):
                    errors = errors + "Please enter a valid email address"

        with open("blacklist.txt",'r') as blacklist:
            data = blacklist.read()
            if username in data.split("\n"):
                ban = True
            else:
                ban = False

        if not errors:
            data = {'name' : name,
                    'email' : email,
                    'username' : username,
                    'banned' : ban
                    }
            with open("log.log","a") as log:
                log.write(str(data))
            with open('log.log',"r") as log:
                if len(log.read())>100:
                    to_write = log.read().split("\n")[1:].append(str(data))
                else:
                    to_write = None
            if to_write != None:
                with open("log.log","w") as log:
                    log.write(str(to_write)+"\n")
            to_write = None
            return render_template("success.html", data=data)
        return render_template("index.html", errors=errors)
if __name__ == '__main__':
	app.run(
        threaded=True,
        port=80,
        host="0.0.0.0"

  )
