from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app, abort
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Usuario, Agendamento
from app.forms import AgendamentoForm, UserCreationForm, UserEditForm
from app import db

bp = Blueprint('main', __name__)

# --- Rota Principal (Redirecionamento) ---
@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('main.calendario_publico'))

# --- Rota de Login ---
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

# --- Rota de Logout ---
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# --- Rota Admin Dashboard ---
@bp.route('/admin')
@login_required
def admin_dashboard():
    agendamentos = Agendamento.query.order_by(Agendamento.data_inicio.asc()).all()
    return render_template('admin_dashboard.html', agendamentos=agendamentos)

# --- Rota novo_agendamento ---
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
        flash('Agendamento criado com sucesso!')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('criar_agendamento.html', title='Novo Agendamento', form=form)

# --- Rota editar_agendamento ---
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

# --- Rota excluir_agendamento ---
@bp.route('/agendamento/excluir/<int:agendamento_id>', methods=['POST'])
@login_required
def excluir_agendamento(agendamento_id):
    if not current_user.is_admin:
        abort(403)
    agendamento_para_excluir = Agendamento.query.get_or_404(agendamento_id)
    db.session.delete(agendamento_para_excluir)
    db.session.commit()
    flash('Agendamento excluído com sucesso!')
    return redirect(url_for('main.admin_dashboard'))

# --- Rota calendário público ---
@bp.route('/calendario')
def calendario_publico():
    return render_template('calendario_publico.html', title="Calendário de Eventos")

# --- ROTA PARA LISTAR USUÁRIOS ---
@bp.route('/admin/usuarios')
@login_required
def lista_usuarios():
    if not current_user.is_admin:
        abort(403) # Proibido
    users = Usuario.query.all()
    return render_template('lista_usuarios.html', users=users, title="Gestão de Usuários")

# --- ROTA PARA CRIAR UM NOVO USUÁRIO ---
@bp.route('/admin/criar_usuario', methods=['GET', 'POST'])
@login_required
def criar_usuario():
    if not current_user.is_admin:
        abort(403) # Proibido
    form = UserCreationForm()
    if form.validate_on_submit():
        user = Usuario(nome_usuario=form.nome_usuario.data, role=form.role.data)
        user.set_senha(form.senha.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!')
        return redirect(url_for('main.lista_usuarios'))
    return render_template('criar_usuario.html', title='Criar Novo Usuário', form=form)

# --- INÍCIO DA CORREÇÃO ---
# Rota API de Agendamentos (VERSÃO COMPLETA)
@bp.route('/api/agendamentos')
def api_agendamentos():
    query = Agendamento.query.all()
    eventos = []
    for agendamento in query:
        cor = ''
        if agendamento.status == 'Confirmado':
            cor = "#28a745" # Verde
        elif agendamento.status == 'Pendente':
            cor = '#ffc107' # Amarelo
        elif agendamento.status == 'Cancelado':
            cor = "#dc3545" # Vermelho
        
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
                'mesa_portatil': agendamento.mesa_portatil,
                'equipe_solicitada': agendamento.equipe_solicitada or 'Nenhuma equipe designada.'
            }
        })
    return jsonify(eventos)

# --- ROTA PARA EDITAR UM USUÁRIO ---
@bp.route('/admin/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(user_id):
    if not current_user.is_admin:
        abort(403)

    user = Usuario.query.get_or_404(user_id)
    form = UserEditForm(original_username=user.nome_usuario)

    if form.validate_on_submit():
        user.nome_usuario = form.nome_usuario.data
        user.role = form.role.data
        # Só atualiza a senha se um novo valor for digitado
        if form.senha.data:
            user.set_senha(form.senha.data)
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('main.lista_usuarios'))
    elif request.method == 'GET':
        form.nome_usuario.data = user.nome_usuario

    return render_template('editar_usuario.html', title='Editar Usuário', form=form, user=user)

# --- ROTA PARA ATIVAR/INATIVAR UM USUÁRIO (Soft Delete) ---
@bp.route('/admin/toggle_status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.is_admin:
        abort(403)

    user_to_toggle = Usuario.query.get_or_404(user_id)

    # Regra de segurança: um admin não pode inativar a si mesmo
    if user_to_toggle.id == current_user.id:
        flash('Você não pode alterar o status da sua própria conta.', 'danger')
        return redirect(url_for('main.lista_usuarios'))

    # Inverte o status atual
    user_to_toggle.is_active = not user_to_toggle.is_active
    db.session.commit()

    status_text = "ativado" if user_to_toggle.is_active else "inativado"
    flash(f'Usuário {user_to_toggle.nome_usuario} foi {status_text} com sucesso.')
    return redirect(url_for('main.lista_usuarios'))