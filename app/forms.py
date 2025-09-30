from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Agendamento

class AgendamentoForm(FlaskForm):
    titulo = StringField('Nome do Evento', validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Evento')
    data_inicio = DateTimeLocalField('Data e Hora de Início', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    data_fim = DateTimeLocalField('Data e Hora de Fim', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    local = StringField('Local do Evento', default='Plenário Roberto Bottacin Moreira')
    responsavel = StringField('Responsável pelo Evento', validators=[DataRequired()])
    status = SelectField('Status do Evento', choices=[('Confirmado', 'Confirmado'), ('Pendente', 'Pendente'), ('Cancelado', 'Cancelado')], validators=[DataRequired()])
    uso_telao = BooleanField('Utilização de Telão')
    gravacao = BooleanField('Gravação do Evento')
    uso_som = BooleanField('Utilização de Sistema de Som')
    transmissao = BooleanField('Transmissão do Evento')
    equipe_solicitada = TextAreaField('Equipe Solicitada (um nome por linha)')
    submit = SubmitField('Salvar Agendamento')

    # Permite que o formulário saiba qual agendamento estamos editando (se for o caso)
    def __init__(self, *args, **kwargs):
        self.agendamento_id = kwargs.pop('agendamento_id', None)
        super(AgendamentoForm, self).__init__(*args, **kwargs)

    # NOSSA VALIDAÇÃO CUSTOMIZADA
    def validate_data_fim(self, data_fim):
        inicio = self.data_inicio.data
        fim = data_fim.data

        # 1. Validação básica: a data de fim não pode ser antes da de início
        if inicio and fim and inicio >= fim:
            raise ValidationError('A data de fim deve ser posterior à data de início.')

        # 2. Validação de conflito: busca no banco por agendamentos que se sobreponham
        # A lógica é: um conflito existe se um evento começa antes do nosso terminar
        # E termina depois do nosso começar.
        conflitos = Agendamento.query.filter(
            Agendamento.data_fim > inicio,
            Agendamento.data_inicio < fim
        ).all()

        if conflitos:
            for conflito in conflitos:
                # Se estamos criando um novo agendamento (id é None) E achamos um conflito, dá erro.
                # OU se estamos editando E o conflito encontrado NÃO é o próprio agendamento que estamos editando.
                if self.agendamento_id is None or conflito.id != self.agendamento_id:
                    raise ValidationError(f'Conflito de horário! Já existe o evento "{conflito.titulo}" neste período.')
    
    # Checkboxes
    uso_telao = BooleanField('Utilização de Telão')
    gravacao = BooleanField('Gravação do Evento')
    uso_som = BooleanField('Utilização de Sistema de Som')
    transmissao = BooleanField('Transmissão do Evento')
    equipe = BooleanField('Equipe de Apoio')
    
    submit = SubmitField('Salvar Agendamento')