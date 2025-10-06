# Sistema de Agendamento do Plenário - Câmara Municipal de Ribeirão Pires

## 📖 Descrição

Este é um sistema web interno desenvolvido para a Câmara Municipal de Ribeirão Pires com o objetivo de gerenciar e visualizar os agendamentos de eventos no plenário. A aplicação substitui o processo manual anterior, oferecendo uma interface de calendário interativa, controle de acesso por perfis de usuário e notificações automáticas por e-mail.

## ✨ Funcionalidades Principais

* **Visualização em Calendário:** Interface intuitiva com [FullCalendar.js](https://fullcalendar.io/) para visualizar todos os eventos por mês, semana ou dia.
* **Controle de Acesso:** Sistema de login com três perfis de usuário:
    * **Admin:** Controle total sobre usuários e agendamentos.
    * **Cerimonial:** Pode criar, editar e excluir agendamentos.
    * **Presidência:** Apenas visualiza os agendamentos (acesso restrito).
* **Gestão de Agendamentos (CRUD):**
    * Criação de novos eventos com título, data, hora e status.
    * Edição de eventos existentes.
    * Exclusão de eventos.
* **Status de Eventos:** Cada evento possui um status ("Pendente" ou "Confirmado"), indicado por cores diferentes no calendário.
* **Notificações por E-mail:** Envio automático de e-mails para os setores responsáveis quando um novo agendamento é criado ou um existente é atualizado.
* **Painel de Admin:** Uma área restrita para o administrador criar e gerenciar os usuários do sistema.
* **Página Pública:** Um calendário público de acesso livre que exibe apenas os eventos confirmados.

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * [Python](https://www.python.org/) 3.12+
    * [Flask](https://flask.palletsprojects.com/)
    * [FastAPI](https://fastapi.tiangolo.com/) (para o serviço de e-mails)
    * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) (ORM)
    * [Flask-Migrate](https://flask-migrate.readthedocs.io/) (Migrações de Banco de Dados com Alembic)
    * [Flask-Login](https://flask-login.readthedocs.io/) (Controle de Sessão de Usuários)
* **Frontend:**
    * HTML5 / CSS3 / JavaScript
    * [Bootstrap 5](https://getbootstrap.com/)
    * [FullCalendar.js](https://fullcalendar.io/)
    * [Jinja2](https://jinja.palletsprojects.com/)
* **Banco de Dados:**
    * SQLite (para simplicidade e portabilidade no ambiente local)
* **Versionamento:**
    * Git & GitHub

## 🚀 Configuração e Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/f-nogueira/Sistema-de-Agendamento.git](https://github.com/f-nogueira/Sistema-de-Agendamento.git)
    cd Sistema-de-Agendamento
    ```

2.  **Criar e Ativar o Ambiente Virtual (`venv`):**
    ```bash
    # Criar o venv
    python -m venv venv

    # Ativar no Windows (PowerShell)
    .\venv\Scripts\Activate.ps1

    # Ativar no macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar as Variáveis de Ambiente:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Use o modelo abaixo e preencha com as informações necessárias.
    ```env
    FLASK_APP=run.py
    SECRET_KEY='sua-chave-secreta-aqui'

    # Adicione aqui outras variáveis necessárias para o serviço de e-mail, se houver.
    ```

5.  **Criar o Banco de Dados:**
    ```bash
    flask db upgrade
    ```

6.  **Criar o Primeiro Usuário (Admin):**
    * Inicie o shell do Flask:
        ```bash
        flask shell
        ```
    * Dentro do shell, execute os seguintes comandos:
        ```python
        from app import db
        from app.models import Usuario

        admin = Usuario(nome_usuario='admin')
        admin.set_senha('senha-forte-admin')
        db.session.add(admin)
        db.session.commit()
        exit()
        ```

## 🏃‍♀️ Executando a Aplicação

Para rodar a aplicação, utilize o servidor de desenvolvimento do Flask.

```bash
python run.py
