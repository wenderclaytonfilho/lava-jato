from modules.funcionario.dao_funcionario import FuncionarioDao
from modules.funcionario.funcionario import Funcionario
from ntpath import join
from flask import Flask, make_response,jsonify,request,Blueprint


app_funcionario = Blueprint('funcionario_blueprint',__name__)
app_name = 'funcionario'
dao_funcionario = FuncionarioDao()
class_name = Funcionario

@app_funcionario.route(f'/{app_name}/add/',methods = ['POST'])
def add_funcionario():
	data = request.form.to_dict(flat = True)
	
	erros = []
	for key in Funcionario.FIELDS_TO_VALIDATE:
		if key not in data.keys():
			erros.append(
				{
				'coluna':key,
				'message':"Campo obrigatório!"
				})
		if erros:
			return make_response({
				'erros':erros
				},400)
	funcionario = dao_funcionario.get_by_cpf(data.get('cpf'))
	if funcionario:
		return make_response({'error': 'O funcionario já existe!'}, 400)

	funcionario = Funcionario(**data)
	funcionario = dao_funcionario.salvar(funcionario)
	return make_response({
		'id' : funcionario.id,
		'cpf' : funcionario.cpf,
		'nome' : funcionario.nome
		})


@app_funcionario.route(f'/{app_name}/',methods = ['GET'])
def get_funcionarios():
	funcionarios = dao_funcionario.get_all()
	data = [funcionario.get_dict() for funcionario in funcionarios]
	return make_response(jsonify(data))


@app_funcionario.route(f'/{app_name}/<int:id>',methods = ['GET'])
def get_funcionario_by_id(id):
	funcionario = dao_funcionario.get_by_id(id)
	if not funcionario:
		return make_response({'erro': 'Funcionario não encontrado'}, 404)
	data = funcionario.get_dict()
	return make_response(jsonify(data))


@app_funcionario.route(f'/{app_name}/delete/<int:id>/', methods = ['DELETE'])
def delete_funcionario(id):
	funcionario = dao_funcionario.get_by_id(id)
	if funcionario:
		dao_funcionario.delete_funcionario(id)
		return make_response({'Funcionário deletado com sucesso!' : True})
	else:
		return make_response({'Error' : 'Id inexistente!'})



@app_funcionario.route(f'/{app_name}/update/<int:id>/',methods = ['PUT'])
def update_funcionario(id):
	data = request.form.to_dict(flat = True)
	
	erros = []
	for key in Funcionario.FIELDS_TO_VALIDATE:
		if key not in data.keys():
			erros.append(
				{
				'coluna':key,
				'message':"Campo obrigatório!"
				})
		if erros:
			return make_response({
				'erros':erros
				},400)

	oldFuncionario = dao_funcionario.get_by_id(id)
	if not oldFuncionario:
		return make_response({'erro':'id Inexistente!'})
	newFuncionario = Funcionario(**data)
	dao_funcionario.update_funcionario(newFuncionario,oldFuncionario)
	return make_response({
		'id':oldFuncionario.id
		})

'''def check_errors(class_name,data):
	errors = []
	for key in class_name.FIELDS_TO_VALIDATE:
		if key not in data.keys():
			errors.append({'Campo' : key,
				'message':"Campo obrigatório!"})
	if errors:
		return make_response({'errors' : errors},400)
'''