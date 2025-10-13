from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Esta função diz ao Flask-Login como encontrar um usuário a partir do ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(64), index=True, unique=True)
    senha_hash = db.Column(db.String(128))
    agendamentos = db.relationship('Agendamento', backref='autor', lazy='dynamic')
    role = db.Column(db.String(20), index=True, default='user')
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Propriedade para verificar facilmente se o usuário é admin
    @property
    def is_admin(self):
        return self.role == 'admin'
    

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'


class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(140), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.DateTime, index=True, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.String(140), default='Plenário Roberto Bottacin Moreira')
    responsavel = db.Column(db.String(140))
    status = db.Column(db.String(64), default='Confirmado')
    uso_telao = db.Column(db.Boolean, default=False)
    gravacao = db.Column(db.Boolean, default=False)
    uso_som = db.Column(db.Boolean, default=False)
    transmissao = db.Column(db.Boolean, default=False)
    equipe_solicitada = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    mesa_portatil = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Agendamento {self.titulo}>'
    
