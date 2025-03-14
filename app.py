from flask import Flask, render_template, request, redirect, url_for, flash
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Função para carregar dados do arquivo JSON
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}

# Função para salvar dados no arquivo JSON
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Função para registrar um novo usuário
def register_user(username, password):
    users = load_users()
    for user in users["users"]:
        if user["username"] == username:
            return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users["users"].append({"username": username, "password": hashed_password})
    save_users(users)
    return True

# Função para fazer login
def login_user(username, password):
    users = load_users()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for user in users["users"]:
        if user["username"] == username and user["password"] == hashed_password:
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if login_user(username, password):
        flash('Login bem-sucedido!')
        return redirect(url_for('index'))
    else:
        flash('Nome de usuário ou senha incorretos!')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if register_user(username, password):
        flash('Usuário registrado com sucesso!')
    else:
        flash('Usuário já existe!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)