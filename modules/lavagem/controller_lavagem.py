from modules.lavagem.dao_lavagem import LavagemDao
from modules.lavagem.lavagem import Lavagem
from flask import Flask,make_response,jsonify,request,Blueprint
import datetime

app_lavagem = Blueprint('lavagem_blueprint',__name__)
app_name = 'lavagem'
dao_lavagem = LavagemDao()

@app_lavagem.route(f'/{app_name}/add/', methods=['POST'])
def add_lavagem():
	data = request.form.to_dict(flat = True)

	#Conversão das datas
	data_hora_entrada = data.get('data_hora_entrada')
	data_hora_saida = data.get('data_hora_saida')
	dhe_convertida = dao_lavagem.converter_data(data_hora_entrada)
	dhs_convertida = dao_lavagem.converter_data(data_hora_saida)
	print("------SEM CONVERTER------")
	print(data)
	data['data_hora_entrada'] = dhe_convertida
	data['data_hora_saida'] = dhs_convertida
	print("-------CONVERTIDA---------")
	print(data)
	#----------==--------------------------------------------------


	erros = []
	for key in Lavagem.FIELDS_TO_VALIDATE:
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
	lavagem = dao_lavagem.get_by_codigo(data.get('codigo'))
	if lavagem:
		return make_response({'error':'Já exite uma lavagem com esse código!'},400)
	lavagem = Lavagem(**data)
	lavagem = dao_lavagem.salvar(lavagem)
	return make_response({
		'id':lavagem.id,
		'veiculo_id':lavagem.veiculo_id,
		'funcionario_id':lavagem.funcionario_id,
		'data_hora_entrada': lavagem.data_hora_entrada,
		'data_hora_saida' : lavagem.data_hora_saida,
		'tipo_lavagem_veiculo_id': lavagem.tipo_lavagem_veiculo_id,
		'codigo':lavagem.codigo
		})


@app_lavagem.route(f'/{app_name}/',methods = ['GET'])
def get_lavagens():
	lavagens = dao_lavagem.get_all()
	data = [lavagem.get_dict() for lavagem in lavagens]
	return make_response(jsonify(data))
	
@app_lavagem.route(f'/{app_name}/delete/<int:id>/', methods = ['DELETE'])
def delete_lavagem(id):
	lavagem = dao_lavagem.get_by_id(id)
	if lavagem:
		dao_lavagem.delete_lavagem(id)
		return make_response({'Lavagem deletada com sucesso!': True})
	else:
		make_response({'Error':'Id Inexistente!'})

@app_lavagem.route(f'/{app_name}/<int:id>',methods =["GET"])
def get_lavagem_by_id(id):
	lavagem = dao_lavagem.get_by_id(id)
	if not lavagem:
		return make_response({
			'erro': 'Lavagem Inexistente'
			})
	data = lavagem.get_dict()
	return make_response(jsonify(data))



@app_lavagem.route(f'/{app_name}/update/<int:id>',methods=["PUT"])
def update_lavagem(id):
	data = request.form.to_dict(flat = True)
	erros = []
	for key in Lavagem.FIELDS_TO_VALIDATE:
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
	oldLavagem = dao_lavagem.get_by_id(id)
	if not oldLavagem:
		return make_response({'erro':'id Inexistente!'})
	newLavagem = Lavagem(**data)
	dao_lavagem.update_lavagem(newLavagem,oldLavagem)
	return make_response({
		'id':newLavagem.id,
		'veiculo_id':newLavagem.veiculo_id,
		'funcionario_id':newLavagem.funcionario_id,
		'data_hora_entrada': newLavagem.data_hora_entrada,
		'data_hora_saida' : newLavagem.data_hora_saida,
		'tipo_lavagem_veiculo_id': newLavagem.tipo_lavagem_veiculo_id,
		'codigo':newLavagem.codigo
		})
	
