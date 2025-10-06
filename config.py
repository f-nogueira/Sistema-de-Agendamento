# config.py

import os
# Para garantir que o .env seja carregado antes que o Flask inicie
from dotenv import load_dotenv

# Carrega o arquivo .env (assumindo que você usa python-dotenv)
load_dotenv() 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-dificil-de-adivinhar'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Configurações de E-mail (LÊ TUDO DO ARQUIVO .ENV) ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    
    # 💡 CORREÇÃO DA PORTA: Lê como inteiro; usa 465 como fallback seguro.
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465) 
    
    # 💡 CORREÇÃO DA SEGURANÇA: Lê True/False de forma segura.
    # Usando SSL/465, que é a solução para o erro WRONG_VERSION_NUMBER.
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True' 
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') == 'True'

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Garante que ADMINS seja uma lista, mesmo que vazia
    ADMINS = os.environ.get('ADMINS').split(',') if os.environ.get('ADMINS') else []

    # Configuração do remetente padrão (Opcional)
    MAIL_DEFAULT_SENDER = ("Agendamento Plenário", os.environ.get('MAIL_USERNAME'))