# app/email.py

from flask import current_app, render_template
from threading import Thread
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import asyncio
# ----------------------------------------------------
# FUNÇÃO AUXILIAR DE CONFIGURAÇÃO
# ----------------------------------------------------

def get_mail_config(app):
    """Cria o objeto de configuração do FastMail a partir das configs do Flask."""
    return ConnectionConfig(
        MAIL_USERNAME=app.config.get('MAIL_USERNAME'),
        MAIL_PASSWORD=app.config.get('MAIL_PASSWORD'),
        MAIL_SERVER=app.config.get('MAIL_SERVER'),
        MAIL_PORT=app.config.get('MAIL_PORT'),
        # Define o remetente como o MAIL_USERNAME
        MAIL_FROM=app.config.get('MAIL_USERNAME'), 
        MAIL_STARTTLS=app.config.get('MAIL_USE_TLS', False),
        MAIL_SSL_TLS=app.config.get('MAIL_USE_SSL', False),
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

# ----------------------------------------------------
# FUNÇÃO PRINCIPAL DE ENVIO
# ----------------------------------------------------

def enviar_email_notificacao(assunto, destinatarios, template_html, **kwargs):
    # Pega o objeto da aplicação fora da thread
    app = current_app._get_current_object()

    # Renderiza template HTML
    html_body = render_template(template_html, **kwargs)
    
    # Cria a mensagem do FastAPI-Mail
    message = MessageSchema(
        subject=assunto,
        recipients=destinatarios,
        body=html_body,
        subtype="html"
    )

    # Função de envio em thread
    def send():
        # Abre o contexto da aplicação para acessar a configuração
        with app.app_context():
            try:
                # 1. Cria a configuração de conexão (lê do app.config)
                conf = get_mail_config(app)
                
                # 2. Cria a instância do FastMail com a configuração
                fm = FastMail(conf)
                
                async def run_send():
                    await fm.send_message(message)
                asyncio.run(run_send())
                # 3. Envia o email
                #fm.send_message(message)
                
                print("✅ E-mail enviado com sucesso via fastapi-mail")
            except Exception as e:
                # Captura erros reais de conexão ou autenticação
                print(f"❌ Erro no envio via fastapi-mail: {e}")

    # Inicializa a thread
    Thread(target=send).start()




