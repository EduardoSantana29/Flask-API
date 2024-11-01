from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from .professor_model import ErrodeVazio, ErrodeAssociacao, ProfessorNaoEncontrado, listar_professor, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor
from config import db

professor_blueprint = Blueprint('professor', __name__)

@professor_blueprint.route('/', methods=['GET'])
def getIndex():
    return render_template("home.html")

@professor_blueprint.route('/professor', methods=['GET'])
def get_professores():
    professor = listar_professor()
    return render_template("professor.html", professor=professor)

@professor_blueprint.route('/professor/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professor_blueprint.route('/professor/adicionar', methods=['GET'])
def adicionar_professor_page():
    return render_template('criarProfessor.html')

@professor_blueprint.route('/professor', methods=['POST'])
def create_professor():
    nome = request.form['nome']
    idade = request.form['idade']
    materia = request.form['materia']
    observacoes = request.form['observacoes']
    
    novo_professor = {
        'nome': nome,
        'idade': idade,
        'materia': materia,
        'observacoes': observacoes
    }
    try:
        adicionar_professor(novo_professor)
        return redirect(url_for('professor.get_professores'))
    except ErrodeVazio:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

@professor_blueprint.route('/professor/<int:id_professor>/editar', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professor_blueprint.route('/professor/<int:id_professor>', methods=['PUT',"POST"])
def update_professor(id_professor):
        print("Dados recebidos no formulário:", request.form)
        try:
            professor = professor_por_id(id_professor)
            professor['nome'] = request.form['nome']
            professor['idade'] = request.form['idade']
            professor['materia'] = request.form['materia']
            professor['observacoes'] = request.form['observacoes']
            atualizar_professor(id_professor, professor)
            return redirect(url_for('professor.get_professor', id_professor=id_professor))
        except ProfessorNaoEncontrado:
            return jsonify({'message': 'Professor não encontrado'}), 404
        except ErrodeVazio:
            return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

@professor_blueprint.route('/professor/delete/<int:id_professor>', methods=['DELETE','POST'])
def delete_professor(id_professor):
        try:
            excluir_professor(id_professor)
            return redirect(url_for('professor.get_professores'))
        except ProfessorNaoEncontrado:
            return jsonify({'message': 'Professor não encontrado'}), 404
        except ErrodeAssociacao:
             return jsonify({'message': "Não é possível excluir o professor pois ele possui turma(s) associada(s)."}), 404