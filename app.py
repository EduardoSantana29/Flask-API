import os
from config import app,db
from aluno.aluno_routes import aluno_blueprint
from professor.professor_routes import professor_blueprint
from turma.turma_routes import turma_blueprint

app.register_blueprint(aluno_blueprint)
app.register_blueprint(professor_blueprint)
app.register_blueprint(turma_blueprint)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )