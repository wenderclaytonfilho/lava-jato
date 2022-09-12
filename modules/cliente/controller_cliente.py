from flask import Flask ,make_response, jsonify, request, Blueprint
from modules.cliente.dao_cliente import ClienteDao
from modules.cliente.cliente import Cliente


app_cliente = Blueprint('cliente_blueprint', __name__)
app_name = 'cliente'
dao_cliente = ClienteDao()



@app_cliente.route(f'/{app_name}/add/',methods = ['POST'])
def add_cliente():
	data = request.form.to_dict(flat = True)
	erros = []
	for key in Cliente.FIELDS_TO_VALIDATE:
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

	cliente = dao_cliente.get_by_cpf(data.get('cpf'))
	if cliente:
		return make_response({'error': 'O cliente já existe!'}, 400)
	cliente = Cliente(**data)
	cliente = dao_cliente.salvar(cliente)
	return make_response({
		'id' : cliente.id,
		'cpf' : cliente.cpf,
		'nome' : cliente.nome
		})


@app_cliente.route(f'/{app_name}/',methods = ['GET'])
def get_clientes():
	clientes = dao_cliente.get_all()
	data = [cliente.get_dict() for cliente in clientes]
	return make_response(jsonify(data))


@app_cliente.route(f'/{app_name}/<int:id>',methods = ['GET'])
def get_cliente_by_id(id):
	cliente = dao_cliente.get_by_id(id)
	if not cliente:
		return make_response({'erro': 'Cliente não encontrado'}, 404)
	data = cliente.get_dict()
	return make_response(jsonify(data))


@app_cliente.route(f'/{app_name}/delete/<int:id>/', methods = ['DELETE'])
def delete_cliente(id):
	cliente = dao_cliente.get_by_id(id)
	if cliente:
		dao_cliente.delete_cliente(id)
		return make_response({'Cliente deletado com sucesso!' : True})
	else:
		return make_response({'Error' : 'Id inexistente!'})



@app_cliente.route(f'/{app_name}/update/<int:id>/',methods = ['PUT'])
def update_cliente(id):
	data = request.form.to_dict(flat = True)
	erros = []
	for key in Cliente.FIELDS_TO_VALIDATE:
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
	oldCliente = dao_cliente.get_by_id(id)
	if not oldCliente:
		return make_response({'erro':'id Inexistente!'})
	newCliente = Cliente(**data)
	dao_cliente.update_cliente(newCliente,oldCliente)
	return make_response({
		'id':oldCliente.id
		})

'''def check_errors(data):
	errors = []
	for key in Cliente.FIELDS_TO_VALIDATE:
		if key not in data.keys():
			errors.append({'Campo' : key,
				'message':"Campo obrigatório!"})
	if errors:
		return make_response({'errors' : errors},400)
'''