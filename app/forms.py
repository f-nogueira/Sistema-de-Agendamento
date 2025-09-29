from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AgendamentoForm(FlaskForm):
    titulo = StringField('Nome do Evento', validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Evento')
    equipe_solicitada = TextAreaField('Equipe Solicitada (um nome por linha)')

    # Usando DateTimeLocalField para um seletor de data e hora amigável
    data_inicio = DateTimeLocalField('Data e Hora de Início', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    data_fim = DateTimeLocalField('Data e Hora de Fim', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    
    local = StringField('Local do Evento', default='Plenário Roberto Bottacin Moreira')
    responsavel = StringField('Responsável pelo Evento', validators=[DataRequired()])
    
    status = SelectField('Status do Evento', choices=[
        ('Confirmado', 'Confirmado'),
        ('Pendente', 'Pendente'),
        ('Cancelado', 'Cancelado')
    ], validators=[DataRequired()])
    
    # Checkboxes
    uso_telao = BooleanField('Utilização de Telão')
    gravacao = BooleanField('Gravação do Evento')
    uso_som = BooleanField('Utilização de Sistema de Som')
    transmissao = BooleanField('Transmissão do Evento')
    equipe = BooleanField('Equipe de Apoio')
    
    submit = SubmitField('Salvar Agendamento')