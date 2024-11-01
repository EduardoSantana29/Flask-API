from config import db

class Turma(db.Model):
    __tablename__ = 'turma'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=True)

    # Relacionamento com Alunos
    alunos = db.relationship('Aluno', backref='turma', lazy='select')

    def __init__(self, descricao, status, professor_id):
        self.descricao = descricao
        self.status = status
        self.professor_id = professor_id

    def to_dict(self):
        return {'id': self.id, 
                'descricao': self.descricao,
                'status': self.status,
                'professor_id': self.professor_id}

class TurmaNaoEncontrado(Exception):
    pass

class ErrodeAssociacao(Exception):
    pass

class ErrodeVazio(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrado
    return turma.to_dict()

def listar_turma():
    turma = Turma.query.all()
    return [turma.to_dict() for turma in turma]

def adicionar_turma(turma_data):
    if not turma_data.get('descricao') or not turma_data.get('professor_id'):
        raise ErrodeVazio

    novo_turma = Turma(descricao=str(turma_data['descricao']),
                       status=bool(turma_data['status']),
                       professor_id=int(turma_data['professor_id']))
    db.session.add(novo_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrado
    if not novos_dados.get('descricao', turma.descricao) or not novos_dados.get('professor_id', turma.professor_id):
        raise ErrodeVazio
    turma.descricao = str(novos_dados.get('descricao', turma.descricao))
    turma.status = bool(novos_dados.get('status', turma.status))
    turma.professor_id = int(novos_dados.get('professor_id', turma.professor_id))
    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrado
    if turma.alunos:
        raise ErrodeAssociacao
    db.session.delete(turma)
    db.session.commit()