from modules.tipoVeiculo.dao_tipo_veiculo import DaoTipoVeiculo
from modules.tipoVeiculo.tipo_veiculo import TipoVeiculo
from ntpath import join
from flask import Flask, make_response,jsonify,request,Blueprint


app_tipoveiculo = Blueprint('tipoVeiculo_blueprint',__name__)
app_name = 'tipoveiculo'
dao_tipo_veiculo = DaoTipoVeiculo()


@app_tipoveiculo.route(f'/{app_name}/',methods = ['GET'])
def get_tipo_veiculo():
	tiposveiculo = dao_tipo_veiculo.get_all()
	data = [tipoveiculo.get_dict() for tipoveiculo in tiposveiculo]
	return make_response(jsonify(data))

@app_tipoveiculo.route(f'/{app_name}/delete/<int:id>/',methods = ['DELETE'])
def delete_tipo_veiculo(id):
	tipo_veiculo = dao_tipo_veiculo.get_by_id(id)
	if tipo_veiculo:
		dao_tipo_veiculo.delete_tipo_veiculo(id)
		return make_response({'Tipo de Veículo deletado com sucesso!':True})
	else:
		return make_response({'Error': 'Id Inexistente!'})		
	
@app_tipoveiculo.route(f'/{app_name}/add/',methods = ['POST'])
def add_tipo_veiculo():
	data = request.form.to_dict(flat = True)
	erros = []
	for key in TipoVeiculo.FIELDS_TO_VALIDATE:
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
	tipoveiculo = dao_tipo_veiculo.get_by_codigo(data.get('codigo'))
	if tipoveiculo:
		return make_response({'error': 'O tipo de Veiculo já existe!'}, 400)
	tipoveiculo = TipoVeiculo(**data)
	tipoveiculo = dao_tipo_veiculo.salvar(tipoveiculo)
	return make_response({
		'id' : tipoveiculo.id,
		'descricao':tipoveiculo.descricao
		})

@app_tipoveiculo.route(f'/{app_name}/<int:id>',methods = ['GET'])
def get_tipo_veiculo_by_id(id):
	tipoveiculo = dao_tipo_veiculo.get_by_id(id)
	if not tipoveiculo:
		return make_response({'erro': 'Tipo de Veículo não encontrado'}, 404)
	data = tipoveiculo.get_dict()
	return make_response(jsonify(data))


@app_tipoveiculo.route(f'/{app_name}/<string:codigo>',methods = ['GET'])
def get_tipo_veiculo_by_codigo(codigo):
	tipoveiculo = dao_tipo_veiculo.get_by_codigo(codigo)
	if not(tipoveiculo):
		return make_response({'erro' : 'Tipo de veículo não encontrado'},404)
	data = tipoveiculo.get_dict()
	return make_response(jsonify(data))


@app_tipoveiculo.route(f'/{app_name}/update/<int:id>/',methods = ['PUT'])
def update_tipoveiculo(id):
	data = request.form.to_dict(flat = True)
	erros = []
	for key in TipoVeiculo.FIELDS_TO_VALIDATE:
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
	oldTipoVeiculo = dao_tipo_veiculo.get_by_id(id)
	if not oldTipoVeiculo:
		return make_response({'erro':'id Inexistente!'})
	newTipoVeiculo = TipoVeiculo(**data)
	dao_tipo_veiculo.update_tipo_veiculo(newTipoVeiculo,oldTipoVeiculo)
	return make_response({
		'id':oldTipoVeiculo.id
		})
