from app import create_app, db
from app.models import Usuario
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Usuario': Usuario}

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
    