from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Usuario, Agendamento
from app.forms import AgendamentoForm
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # Por enquanto, nossa página inicial vai ser a de login
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona para a página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard')) # Vamos criar essa página em breve

    if request.method == 'POST':
        # Pega os dados do formulário
        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')

        # Busca o usuário no banco de dados
        user = Usuario.query.filter_by(nome_usuario=nome_usuario).first()

        # Verifica se o usuário existe e se a senha está correta
        if user is None or not user.check_senha(senha):
            flash('Nome de usuário ou senha inválidos!')
            return redirect(url_for('main.login'))

        # Se tudo estiver certo, faz o login do usuário
        login_user(user)
        return redirect(url_for('main.admin_dashboard')) # Redireciona para o painel de admin

    # Se o método for GET, apenas mostra a página de login
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/admin')
@login_required 
def admin_dashboard():
    # Esta função só será executada se o usuário estiver logado
    return render_template('admin.html')

@bp.route('/agendamento/novo', methods=['GET', 'POST'])
@login_required
def novo_agendamento():
    form = AgendamentoForm()
    if form.validate_on_submit():
        # Se o formulário for válido, pegue os dados e crie um novo objeto Agendamento
        agendamento = Agendamento(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            local=form.local.data,
            responsavel=form.responsavel.data,
            status=form.status.data,
            uso_telao=form.uso_telao.data,
            gravacao=form.gravacao.data,
            uso_som=form.uso_som.data,
            transmissao=form.transmissao.data,
            autor=current_user # Associa o agendamento ao usuário logado
        )
        db.session.add(agendamento)
        db.session.commit()
        flash('Agendamento criado com sucesso!')
        return redirect(url_for('main.admin_dashboard'))
    
    # Se for um GET, apenas renderize a página com o formulário
    return render_template('agendamento.html', title='Novo Agendamento', form=form)