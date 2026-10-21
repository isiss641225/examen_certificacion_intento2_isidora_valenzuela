from flask import Flask

app = Flask(__name__)
app.secret_key = "clave_secreta_querido_diario"
app.config['SESSION_PERMANENT'] = False