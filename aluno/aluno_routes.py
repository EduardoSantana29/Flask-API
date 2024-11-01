from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from .aluno_model import ErrodeVazio, AlunoNaoEncontrado, listar_aluno, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from config import db
from datetime import datetime

aluno_blueprint = Blueprint('aluno', __name__)

@aluno_blueprint.route('/', methods=['GET'])
def getIndex():
    return render_template("home.html")

@aluno_blueprint.route('/aluno', methods=['GET'])
def get_alunos():
    aluno = listar_aluno()
    return render_template("aluno.html", aluno=aluno)

@aluno_blueprint.route('/aluno/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@aluno_blueprint.route('/aluno/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('criarAluno.html')

@aluno_blueprint.route('/aluno', methods=['POST'])
def create_aluno():
    nome = request.form['nome']
    idade = request.form['idade']
    data_nascimento = request.form['data_nascimento']
    nota_primeiro_semestre = request.form['nota_primeiro_semestre']
    nota_segundo_semestre = request.form['nota_segundo_semestre']
    media_final = request.form['media_final']
    turma_id = request.form['turma_id']
    
    novo_aluno = {
        'nome': nome,
        'idade': idade,
        'data_nascimento': data_nascimento,
        'nota_primeiro_semestre': nota_primeiro_semestre,
        'nota_segundo_semestre': nota_segundo_semestre,
        'media_final': media_final,
        'turma_id': turma_id
    }
    try:
        adicionar_aluno(novo_aluno)
        return redirect(url_for('aluno.get_alunos'))
    except ErrodeVazio:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

@aluno_blueprint.route('/aluno/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@aluno_blueprint.route('/aluno/<int:id_aluno>', methods=['PUT',"POST"])
def update_aluno(id_aluno):
        print("Dados recebidos no formulário:", request.form)
        try:
            aluno = aluno_por_id(id_aluno)
            aluno['nome'] = request.form['nome']
            aluno['idade'] = request.form['idade']
            request.form['data_nascimento']
            aluno['data_nascimento'] = request.form['data_nascimento']
            aluno['nota_primeiro_semestre'] = request.form['nota_primeiro_semestre']
            aluno['nota_segundo_semestre'] = request.form['nota_segundo_semestre']
            aluno['media_final'] = request.form['media_final']
            aluno['turma_id'] = request.form['turma_id']
            atualizar_aluno(id_aluno, aluno)
            return redirect(url_for('aluno.get_aluno', id_aluno=id_aluno))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
        except ErrodeVazio:
            return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

@aluno_blueprint.route('/aluno/delete/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return redirect(url_for('aluno.get_alunos'))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404