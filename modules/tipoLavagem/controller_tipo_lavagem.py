from modules.tipoLavagem.dao_tipo_lavagem import DaoTipoLavagem
from modules.tipoLavagem.tipo_lavagem import TipoLavagem
from flask import Flask, make_response,jsonify,request,Blueprint


app_tipolavagem = Blueprint('tipoLavagem_blueprint',__name__)
app_name = 'tipolavagem'
dao_tipo_lavagem = DaoTipoLavagem()
class_name = TipoLavagem


@app_tipolavagem.route(f'/{app_name}/',methods = ['GET'])
def get_tipo_lavagem():
	tiposlavagem = dao_tipo_lavagem.get_all()
	data = [tipolavagem.get_dict() for tipolavagem in tiposlavagem]
	return make_response(jsonify(data))

@app_tipolavagem.route(f'/{app_name}/delete/<int:id>/',methods = ['DELETE'])
def delete_tipo_lavagem(id):
	tipo_lavagem = dao_tipo_lavagem.get_by_id(id)
	if tipo_lavagem:
		dao_tipo_lavagem.delete_tipo_lavagem(id)
		return make_response({'Tipo de Lavagem deletado com sucesso!':True})
	else:
		return make_response({'Error': 'Id Inexistente!'})		
	
@app_tipolavagem.route(f'/{app_name}/add/',methods = ['POST'])
def add_tipo_lavagem():
	data = request.form.to_dict(flat = True)
	erros = []
	for key in TipoLavagem.FIELDS_TO_VALIDATE:
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
	tipolavagem = dao_tipo_lavagem.get_by_codigo(data.get('codigo'))
	if tipolavagem:
		return make_response({'error': 'O tipo de lavagem já existe!'}, 400)
	tipolavagem = TipoLavagem(**data)
	tipolavagem = dao_tipo_lavagem.salvar(tipolavagem)
	return make_response({
		'id' : tipolavagem.id,
		'descricao':tipolavagem.descricao
		})

@app_tipolavagem.route(f'/{app_name}/<int:id>',methods = ['GET'])
def get_tipo_lavagem_by_id(id):
	tipolavagem = dao_tipo_lavagem.get_by_id(id)
	if not tipolavagem:
		return make_response({'erro': 'Tipo de lavagem não encontrado'}, 404)
	data = tipolavagem.get_dict()
	return make_response(jsonify(data))

@app_tipolavagem.route(f'/{app_name}/<string:codigo>',methods = ['GET'])
def get_tipo_lavagem_by_codigo(codigo):
	tipolavagem = dao_tipo_lavagem.get_by_codigo(codigo)
	if not(tipolavagem):
		return make_response({'erro' : 'Tipo de lavagem não encontrado'},404)
	data = tipolavagem.get_dict()
	return make_response(jsonify(data))

@app_tipolavagem.route(f'/{app_name}/update/<int:id>/',methods = ['PUT'])
def update_tipolavagem(id):
	data = request.form.to_dict(flat = True)
	erros = []
	for key in TipoLavagem.FIELDS_TO_VALIDATE:
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
	oldTipoLavagem = dao_tipo_lavagem.get_by_id(id)
	if not oldTipoLavagem:
		return make_response({'erro':'id Inexistente!'})
	newTipoLavagem = TipoLavagem(**data)
	dao_tipo_lavagem.update_tipo_lavagem(newTipoLavagem,oldTipoLavagem)
	return make_response({
		'id':oldTipoLavagem.id
		})
