from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Agendamento
from app.models import Usuario
from app import db # Importação importante

class AgendamentoForm(FlaskForm):
    # --- CAMPOS DO FORMULÁRIO ---
    titulo = StringField('Nome do Evento', validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Evento')
    data_inicio = DateTimeLocalField('Data e Hora de Início', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    data_fim = DateTimeLocalField('Data e Hora de Fim', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    local = StringField('Local do Evento', default='Plenário Roberto Bottacin Moreira', validators=[DataRequired()])
    responsavel = StringField('Responsável pelo Evento', validators=[DataRequired()])
    status = SelectField('Status do Evento', choices=[('Confirmado', 'Confirmado'), ('Pendente', 'Pendente'), ('Cancelado', 'Cancelado')], validators=[DataRequired()])
    
    # Checkboxes
    uso_telao = BooleanField('Utilização de Telão')
    gravacao = BooleanField('Gravação do Evento')
    uso_som = BooleanField('Utilização de Sistema de Som')
    transmissao = BooleanField('Transmissão do Evento')
    equipe_solicitada = TextAreaField('Equipe Solicitada (um nome por linha)')
    mesa_portatil = BooleanField('Mesa Portátil') 

    
    submit = SubmitField('Salvar Agendamento')

    # --- LÓGICA DE VALIDAÇÃO ---

    def __init__(self, agendamento_id=None, *args, **kwargs):
        super(AgendamentoForm, self).__init__(*args, **kwargs)
        self.agendamento_id = agendamento_id

    # Validação para garantir que a data de fim seja depois da de início
    def validate_data_fim(self, data_fim):
        if self.data_inicio.data and data_fim.data and self.data_inicio.data >= data_fim.data:
            raise ValidationError('A data de fim deve ser posterior à data de início.')

    # Validação customizada para conflitos de local e horário
    def validate_local(self, local):
        inicio = self.data_inicio.data
        fim = self.data_fim.data

        # Se as datas não foram preenchidas ou são inválidas, outra validação já vai pegar o erro.
        if not inicio or not fim or inicio >= fim:
            return

        # Consulta por conflitos no MESMO local e horário
        conflitos = Agendamento.query.filter(
            Agendamento.local == local.data, 
            Agendamento.data_fim > inicio,
            Agendamento.data_inicio < fim
        ).all()

        if conflitos:
            for conflito in conflitos:
                # Se estamos criando (id is None) OU editando e o conflito NÃO é o próprio agendamento
                if self.agendamento_id is None or conflito.id != self.agendamento_id:
                    raise ValidationError(f'Conflito! Já existe o evento "{conflito.titulo}" neste local e período.')


class UserCreationForm(FlaskForm):
    nome_usuario = StringField('Nome de Usuário', validators=[DataRequired('Este campo é obrigatório.')])
    senha = PasswordField('Senha', validators=[DataRequired('Este campo é obrigatório.')])
    senha2 = PasswordField('Repita a Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais.')])
    role = SelectField('Cargo', choices=[('user', 'Usuário'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Criar Usuário')

    def validate_nome_usuario(self, nome_usuario):
        user = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já existe. Por favor, escolha outro.')