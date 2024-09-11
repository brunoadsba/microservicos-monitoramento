from app import app, db
from flask_migrate import upgrade

def init_db():
    with app.app_context():
        upgrade()

if __name__ == '__main__':
    init_db()

# Para inicializar o banco de dados e criar as tabelas necessárias, execute os seguintes comandos:
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
