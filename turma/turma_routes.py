from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from .turma_model import ErrodeVazio, ErrodeAssociacao, TurmaNaoEncontrado, listar_turma, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma
from config import db

turma_blueprint = Blueprint('turma', __name__)

@turma_blueprint.route('/', methods=['GET'])
def getIndex():
    return render_template("home.html")

@turma_blueprint.route('/turma', methods=['GET'])
def get_turmas():
    turma = listar_turma()
    return render_template("turma.html", turma=turma)

@turma_blueprint.route('/turma/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_id.html', turma=turma)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrado'}), 404

@turma_blueprint.route('/turma/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('criarTurma.html')

@turma_blueprint.route('/turma', methods=['POST'])
def create_turma():
    descricao = request.form['descricao']
    status = request.form.get('status')
    professor_id = request.form['professor_id']
    
    novo_turma = {
        'descricao': descricao,
        'status': status,
        'professor_id': professor_id
    }
    try:
        adicionar_turma(novo_turma)
        return redirect(url_for('turma.get_turmas'))
    except ErrodeVazio:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

@turma_blueprint.route('/turma/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_update.html', turma=turma)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrado'}), 404

@turma_blueprint.route('/turma/<int:id_turma>', methods=['PUT',"POST"])
def update_turma(id_turma):
        print("Dados recebidos no formulário:", request.form)
        try:
            turma = turma_por_id(id_turma)
            turma['descricao'] = request.form['descricao']
            turma['status'] = 'status' in request.form  
            turma['professor_id'] = request.form['professor_id']
            atualizar_turma(id_turma, turma)
            return redirect(url_for('turma.get_turma', id_turma=id_turma))
        except TurmaNaoEncontrado:
            return jsonify({'message': 'Turma não encontrado'}), 404
        except ErrodeVazio:
            return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

@turma_blueprint.route('/turma/delete/<int:id_turma>', methods=['DELETE','POST'])
def delete_turma(id_turma):
        try:
            excluir_turma(id_turma)
            return redirect(url_for('turma.get_turmas'))
        except TurmaNaoEncontrado:
            return jsonify({'message': 'Turma não encontrado'}), 404
        except ErrodeAssociacao:
             return jsonify({'message': "Não é possível excluir a turma pois ela possui aluno(s) associado(s)."}), 404