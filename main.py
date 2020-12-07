from flask import Flask, request, render_template
from faker import Faker
import csv
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/requirements/')
def requirements():
    with open('requirements.txt', 'r') as f:
        content=f.read()
    return render_template('content.html', content=content)


@app.route('/generate-users/')
@app.route('/generate-users/<int:amount>')
def generate_users(amount = 100):
    fake = Faker('en_US')
    users_list = []
    for _ in range(amount):
        name = fake.name()
        name_mod = name.lower().split(' ')
        if len(name_mod) > 2:
            name_mod.pop(0)
        email = name_mod[0] + '.' + name_mod[1] + '@' + fake.email().split('@')[1]
        users_list.append([name, email])
    return render_template('list.html', data=users_list)


@app.route('/mean/')
def mean():
    counter = height = weight = 0
    with open("hw.csv") as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            counter += 1
            height += float(line[' "Height(Inches)"'].lstrip(' ')) * 2.54
            weight += float(line[' "Weight(Pounds)"'].lstrip(' ')) * 0.453592
    return f"Average height: {height/counter} sm.<br/>Average weight: {weight/counter} kg."


@app.route('/space/')
def space():
     r = requests.get('http://api.open-notify.org/astros.json')
     return f"Amount astronauts in the Space: {r.json().get('number', 0)}"
