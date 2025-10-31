from flask import Flask, jsonify, render_template
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
import datetime

import os

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Altere as configurações para ler do 'os.environ'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')


# Configurações atualizadas para a versão nova do Flask-JWT-Extended
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token não expira (opcional)
app.config['JWT_IDENTITY_CLAIM'] = 'sub'  # Padrão, mas explícito
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

# Variável para controlar se o banco já foi criado
banco_criado = False

@app.route("/")
def index():
    """Rota principal com página HTML personalizada"""
    server_info = {
        "status": "online",
        "timestamp": datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
        "ambiente": "Desenvolvimento" if os.environ.get('FLASK_ENV') == 'development' else "Produção",
        "versao": "1.0.0",
        "endpoints": [
            {"nome": "Status da API", "rota": "/status", "metodo": "GET"},
            {"nome": "Confirmação de Email", "rota": "/confirmar-email/<token>", "metodo": "GET"},
            {"nome": "Health Check", "rota": "/health", "metodo": "GET"}
        ]
    }
    return render_template('index.html', info=server_info)

@app.before_request
def cria_banco():
    global banco_criado
    if not banco_criado:
        # É uma boa prática importar o 'banco' aqui dentro
        # para evitar importação circular, caso 'sql_alchemy' importe 'app'.
        # No entanto, se 'sql_alchemy' for inicializado apenas no main,
        # precisamos garantir que ele esteja acessível.
        # A forma mais segura é garantir que 'banco' seja importado
        # antes da primeira requisição.
        from sql_alchemy import banco
        banco.create_all()
        banco_criado = True


# CORREÇÃO: Mudou de token_in_blacklist_loader para token_in_blocklist_loader
# E adicionou jwt_header como primeiro parâmetro
@jwt.token_in_blocklist_loader
def verifica_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLOCKLIST


# CORREÇÃO: Função deve receber os parâmetros jwt_header e jwt_payload
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401  # unauthorized


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    
    # Movendo o 'cria_banco' para dentro do contexto da aplicação
    # para garantir que 'banco' esteja inicializado.
    # Isso é mais seguro do que usar 'before_request' globalmente
    # se você só precisa criar o banco uma vez no início.
    # (Embora sua lógica original com 'before_request' e a flag 'banco_criado' também funcione)
    
    # Para manter sua lógica original:
    app.run(debug=True)
    
    # Uma alternativa mais limpa para criar o banco apenas uma vez (sem a flag global):
    @app.before_first_request # Obsoleto em Flasks mais novos
    def cria_banco_inicial():
        banco.create_all()
    
    # A forma moderna (executar apenas uma vez ao iniciar):
    # with app.app_context():
    #     banco.create_all()
    # app.run(debug=True)