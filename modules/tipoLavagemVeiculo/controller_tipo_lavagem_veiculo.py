from modules.tipoLavagemVeiculo.dao_tipo_lavagem_veiculo import DaoTipoLavagemVeiculo
from modules.tipoLavagemVeiculo.tipo_lavagem_veiculo import TipoLavagemVeiculo
from flask import Flask, make_response,jsonify,request,Blueprint


app_tipo_lavagem_veiculo = Blueprint('tipoLavagemVeiculo_blueprint',__name__)
app_name = 'tipolavagemveiculo'
dao_tipo_lavagem_veiculo = DaoTipoLavagemVeiculo()


@app_tipo_lavagem_veiculo.route(f'/{app_name}/',methods = ['GET'])
def get_tipo_lavagem_veiculo():
	tiposLavagemVeiculo = dao_tipo_lavagem_veiculo.get_all()
	data = [tipo_lavagem_veiculo.get_dict() for tipo_lavagem_veiculo in tiposLavagemVeiculo]
	return make_response(jsonify(data))

@app_tipo_lavagem_veiculo.route(f'/{app_name}/add/',methods = ['POST'])
def add_tipo_lavagem_veiculo():
	data = request.form.to_dict(flat = True)
	erros = []
	for key in TipoLavagemVeiculo.FIELDS_TO_VALIDATE:
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
	tipolavagemveiculo = dao_tipo_lavagem_veiculo.get_by_codigo(data.get('codigo'))
	if tipolavagemveiculo:
		return make_response({'error': 'O tipo lavagem veículo já existe'},400)

	tipolavagemveiculo = TipoLavagemVeiculo(**data)
	tipolavagemveiculo = dao_tipo_lavagem_veiculo.salvar(tipolavagemveiculo)
	return make_response({
		'id':tipolavagemveiculo.id,
		'tipo_lavagem-id': tipolavagemveiculo.tipo_lavagem_id,
		'tipo-veiculo-id': tipolavagemveiculo.tipo_veiculo_id,
		'codigo': tipolavagemveiculo.codigo
		})


@app_tipo_lavagem_veiculo.route(f'/{app_name}/delete/<int:id>/',methods = ['DELETE'])
def delete_tipo_lavagem_veiculo(id):
	tipo_lavagem_veiculo = dao_tipo_lavagem_veiculo.get_by_id(id)
	if tipo_lavagem_veiculo:
		dao_tipo_lavagem_veiculo.delete_tlv(id)
		return make_response({'Tipo lavagem veículo deletado com sucesso!': True})
	else:
		return make_response({'Error': 'Id inexistente!'})

@app_tipo_lavagem_veiculo.route(f'/{app_name}/update/<int:id>/',methods = ['PUT'])
def update_tipolavagemveiculo(id):
	data = request.form.to_dict(flat = True)
	erros = []
	for key in TipoLavagemVeiculo.FIELDS_TO_VALIDATE:
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
	tipolavagemveiculo = dao_tipo_lavagem_veiculo.get_by_codigo(data.get('codigo'))
	if tipolavagemveiculo:
		return make_response({'error': 'O tipo lavagem veículo já existe'},400)
	OldTipoLavagemVeiculo = dao_tipo_lavagem_veiculo.get_by_id(id)
	if not OldTipoLavagemVeiculo:
		return make_response({'erro': 'Id inexistente'})
	else:
		newTipoLavagemVeiculo = TipoLavagemVeiculo(**data)
		dao_tipo_lavagem_veiculo.update_tlv(newTipoLavagemVeiculo,OldTipoLavagemVeiculo)
		return make_response({
			'id':OldTipoLavagemVeiculo.id,
			'Message': 'Atualizado com sucesso!'
			})