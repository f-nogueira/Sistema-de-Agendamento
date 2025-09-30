from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# Instanciando os objetos de extensão
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail() # <-- ADICIONADO: Crie a instância do Mail aqui

login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializando as extensões com o app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app) # <-- ADICIONADO: Conecte o Mail ao app aqui

    # Registrando o blueprint
    from app.routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app