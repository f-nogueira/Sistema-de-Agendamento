from threading import Thread
from flask import render_template
from flask_mail import Message
from app import mail
from flask import current_app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def enviar_email_notificacao(assunto, destinatarios, template_html, **kwargs):
    # Pega a instância atual do app para usar em uma thread separada
    app = current_app._get_current_object()
    
    # Cria a mensagem de e-mail
    msg = Message(assunto, 
                  sender=('Agendamento Plenário', app.config['MAIL_USERNAME']), 
                  recipients=destinatarios)
    
    # Renderiza o corpo do e-mail usando um template HTML
    msg.html = render_template(template_html, **kwargs)
    
    # Inicia uma nova thread para enviar o e-mail em segundo plano
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

