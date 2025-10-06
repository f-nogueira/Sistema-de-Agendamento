from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# FastAPI-Mail é importado, mas não inicializado aqui
from fastapi_mail import FastMail, ConnectionConfig 


# Instanciando os objetos de extensão (Sem a instância global do Mail)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# REMOVIDO: mail = Mail() 

login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializando as extensões com o app (SÓ AS QUE USAM init_app)
    db.init_app(app)
    # REMOVIDO: mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Registrando o blueprint
    from app.routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app