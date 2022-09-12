from flask import Flask,make_response,jsonify,request,Blueprint
from modules.veiculo.dao_veiculo import VeiculoDao
from modules.veiculo.veiculo import Veiculo


app_veiculo = Blueprint('veiculo_blueprint',__name__)
app_name = 'veiculo'
dao_veiculo = VeiculoDao()


@app_veiculo.route(f'/{app_name}/add/',methods = ['POST'])
def add_veiculo():
	data = request.form.to_dict(flat = True)

	erros = []
	for key in Veiculo.FIELDS_TO_VALIDATE:
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

	veiculo = dao_veiculo.get_by_placa(data.get('placa'))
	if veiculo:
		return make_response({'erro':'Esse veículo já está cadastrado!'} , 400)
	veiculo = Veiculo(**data)
	veiculo = dao_veiculo.salvar(veiculo)
	return make_response({
			'id':veiculo.id,
            'placa':veiculo.placa,
            'tipo_id':veiculo.tipo_id,
            'endereco':veiculo.endereco,
            'cliente':veiculo.cliente_id
		})


@app_veiculo.route(f'/{app_name}/',methods = ['GET'])
def get_veiculos():
	veiculos = dao_veiculo.get_all()
	data = [veiculo.get_dict() for veiculo in veiculos]
	return make_response(jsonify(data))


@app_veiculo.route(f'/{app_name}/<int:id>',methods = ['GET'])
def get_veiculo_by_id(id):
	veiculo = dao_veiculo.get_by_id(id)
	if not veiculo:
		return make_response({'erro':'Veículo não encontrado!'})
	data = veiculo.get_dict()
	return make_response(jsonify(data))


@app_veiculo.route(f'/{app_name}/<string:placa>',methods = ['GET'])
def get_veiculo_by_placa(placa):
	veiculo = dao_veiculo.get_by_placa(placa)
	if not veiculo:
		return make_response({'erro':'Veículo não encontrado!'})
	data = veiculo.get_dict()
	return make_response(jsonify(data))


@app_veiculo.route(f'/{app_name}/delete/<int:id>',methods =['DELETE'])
def delete_veiculo(id):
	veiculo = dao_veiculo.get_by_id(id)
	if veiculo:
		dao_veiculo.delete_veiculo(id)
		return make_response({'Veículo deletado com sucesso': True})
	else:
		return make_response({'Error':'ID Inexistente!'})


@app_veiculo.route(f'/{app_name}/update/<int:id>',methods = ['PUT'])
def update_veiculo(id):
	data = request.form.to_dict(flat = true)
	erros = []
	for key in Veiculo.FIELDS_TO_VALIDATE:
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
	oldVeiculo = dao_veiculo.get_by_id(id)
	if not oldVeiculo:
		return make_response({'Erro':'Id Inexistente'})
	newVeiculo = Veiculo(**data)
	dao_veiculo.update_veiculo(newVeiculo,oldVeiculo)
	return make_response({
			'id':veiculo.id,
            'placa':veiculo.placa,
            'tipo_id':veiculo.tipo_id,
            'endereco':veiculo.endereco,
            'cliente':veiculo.cliente_id
		})