# A importação do current_app é necessária para acessar a configuração
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Usuario, Agendamento
from app.forms import AgendamentoForm
from app.email import enviar_email_notificacao # Certifique-se que esta linha existe
from app import db

bp = Blueprint('main', __name__)

# --- (Nenhuma mudança nas rotas index, login, logout, admin_dashboard) ---
@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('main.calendario_publico'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')
        user = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        if user is None or not user.check_senha(senha):
            flash('Nome de usuário ou senha inválidos!')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.admin_dashboard'))
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/admin')
@login_required
def admin_dashboard():
    agendamentos = Agendamento.query.order_by(Agendamento.data_inicio.asc()).all()
    return render_template('admin_dashboard.html', agendamentos=agendamentos)

# --- Rota novo_agendamento (ATUALIZADA) ---
@bp.route('/agendamento/novo', methods=['GET', 'POST'])
@login_required
def novo_agendamento():
    form = AgendamentoForm()
    if form.validate_on_submit():
        agendamento = Agendamento(
            titulo=form.titulo.data, descricao=form.descricao.data,
            data_inicio=form.data_inicio.data, data_fim=form.data_fim.data,
            local=form.local.data, responsavel=form.responsavel.data,
            status=form.status.data, uso_telao=form.uso_telao.data,
            gravacao=form.gravacao.data, uso_som=form.uso_som.data,
            transmissao=form.transmissao.data, equipe_solicitada=form.equipe_solicitada.data,
            autor=current_user
        )
        db.session.add(agendamento)
        db.session.commit()
        enviar_email_notificacao(
            assunto=f"Novo Agendamento: {agendamento.titulo}",
            # ATUALIZADO: Usando a lista de e-mails da configuração
            destinatarios=current_app.config['ADMINS'],
            template_html="email/notificacao.html",
            agendamento=agendamento,
            status_acao="criado"
        )
        flash('Agendamento criado com sucesso!')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('criar_agendamento.html', title='Novo Agendamento', form=form)

# --- Rota editar_agendamento (ATUALIZADA) ---
@bp.route('/agendamento/editar/<int:agendamento_id>', methods=['GET', 'POST'])
@login_required
def editar_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    form = AgendamentoForm(agendamento_id=agendamento_id)
    if form.validate_on_submit():
        agendamento.titulo = form.titulo.data
        agendamento.descricao = form.descricao.data
        agendamento.data_inicio = form.data_inicio.data
        agendamento.data_fim = form.data_fim.data
        agendamento.local = form.local.data
        agendamento.responsavel = form.responsavel.data
        agendamento.status = form.status.data
        agendamento.uso_telao = form.uso_telao.data
        agendamento.gravacao = form.gravacao.data
        agendamento.uso_som = form.uso_som.data
        agendamento.transmissao = form.transmissao.data
        agendamento.equipe_solicitada = form.equipe_solicitada.data
        db.session.commit()
        enviar_email_notificacao(
            assunto=f"Agendamento Atualizado: {agendamento.titulo}",
            # ATUALIZADO: Usando a lista de e-mails da configuração
            destinatarios=current_app.config['ADMINS'],
            template_html="email/notificacao.html",
            agendamento=agendamento,
            status_acao="atualizado"
        )
        flash('Agendamento atualizado com sucesso!')
        return redirect(url_for('main.admin_dashboard'))
    elif request.method == 'GET':
        form.titulo.data = agendamento.titulo
        form.descricao.data = agendamento.descricao
        form.data_inicio.data = agendamento.data_inicio
        form.data_fim.data = agendamento.data_fim
        form.local.data = agendamento.local
        form.responsavel.data = agendamento.responsavel
        form.status.data = agendamento.status
        form.uso_telao.data = agendamento.uso_telao
        form.gravacao.data = agendamento.gravacao
        form.uso_som.data = agendamento.uso_som
        form.transmissao.data = agendamento.transmissao
        form.equipe_solicitada.data = agendamento.equipe_solicitada
    return render_template('editar_agendamento.html', title='Editar Agendamento', form=form)

# --- (Nenhuma mudança nas rotas excluir_agendamento, calendario_publico, api_agendamentos) ---
@bp.route('/agendamento/excluir/<int:agendamento_id>', methods=['POST'])
@login_required
def excluir_agendamento(agendamento_id):
    agendamento_para_excluir = Agendamento.query.get_or_404(agendamento_id)
    db.session.delete(agendamento_para_excluir)
    db.session.commit()
    flash('Agendamento excluído com sucesso!')
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/calendario')
def calendario_publico():
    return render_template('calendario_publico.html', title="Calendário de Eventos")

@bp.route('/api/agendamentos')
def api_agendamentos():
    query = Agendamento.query.all()
    eventos = []
    for agendamento in query:
        cor = ''
        if agendamento.status == 'Confirmado':
            cor = "#0dfd21"
        elif agendamento.status == 'Pendente':
            cor = '#ffc107'
        elif agendamento.status == 'Cancelado':
            cor = "#ff0000"
        eventos.append({
            'title': agendamento.titulo,
            'start': agendamento.data_inicio.isoformat(),
            'end': agendamento.data_fim.isoformat(),
            'color': cor,
            'extendedProps': {
                'description': agendamento.descricao or 'Nenhuma descrição fornecida.',
                'responsavel': agendamento.responsavel,
                'local': agendamento.local,
                'status': agendamento.status,
                'uso_telao': agendamento.uso_telao,
                'gravacao': agendamento.gravacao,
                'uso_som': agendamento.uso_som,
                'transmissao': agendamento.transmissao,
                'equipe_solicitada': agendamento.equipe_solicitada or ''
            }
        })
    return jsonify(eventos)