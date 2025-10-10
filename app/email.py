from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread

def enviar_email_notificacao(assunto, destinatarios, template_html, **kwargs):
    """
    Envia e-mails de notificação via Flask-Mail usando template Jinja.
    """

    # Renderiza o HTML fora da thread (tem que estar no contexto da requisição)
    html_corpo = render_template(template_html, **kwargs)

    def enviar(app):
        with app.app_context():
            try:
                msg = Message(
                    subject=assunto,
                    recipients=destinatarios,
                    html=html_corpo
                )
                mail.send(msg)
                print(f"✅ E-mail enviado para {destinatarios}")
            except Exception as e:
                print(f"❌ Erro ao enviar e-mail: {e}")

    # Passa a instância do app para a thread
    Thread(target=enviar, args=(current_app._get_current_object(),)).start()


