from config import db

class Professor(db.Model):
    __tablename__ = 'professor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text, nullable=False)

    # Relacionamento com Turma
    turmas = db.relationship('Turma', backref='professor', lazy=True)

    def __init__(self, nome, idade, materia, observacoes):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dict(self):
        return {'id': self.id, 
                'nome': self.nome,
                'idade': self.idade,
                'materia': self.materia,
                'observacoes': self.observacoes}
    
class ProfessorNaoEncontrado(Exception):
    pass

class ErrodeAssociacao(Exception):
    pass

class ErrodeVazio(Exception):
    pass

def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor.to_dict()

def listar_professor():
    professor = Professor.query.all()
    return [professor.to_dict() for professor in professor]

def adicionar_professor(professor_data):
    if not professor_data.get('nome') or not professor_data.get('idade') or not professor_data.get('materia') or not professor_data.get('observacoes'):
        raise ErrodeVazio
    
    novo_professor = Professor(nome=str(professor_data['nome']),
                               idade=int(professor_data['idade']),
                               materia=str(professor_data['materia']),
                               observacoes=str(professor_data['observacoes']))
    db.session.add(novo_professor)
    db.session.commit()

def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    if not novos_dados.get('nome', professor.nome) or not novos_dados.get('idade', professor.idade) or not novos_dados.get('materia', professor.materia) or not novos_dados.get('observacoes', professor.observacoes):
        raise ErrodeVazio
    professor.nome = str(novos_dados.get('nome', professor.nome))
    professor.idade = int(novos_dados.get('idade', professor.idade))
    professor.materia = str(novos_dados.get('materia', professor.materia))
    professor.observacoes = str(novos_dados.get('observacoes', professor.observacoes))
    db.session.commit()

def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
       raise ProfessorNaoEncontrado
    if professor.turmas:
        raise ErrodeAssociacao
    db.session.commit()
    db.session.delete(professor)
    db.session.commit()