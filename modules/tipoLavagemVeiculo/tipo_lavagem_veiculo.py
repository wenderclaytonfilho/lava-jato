from modules.tipoVeiculo.dao_tipo_veiculo import DaoTipoVeiculo
from modules.tipoLavagem.dao_tipo_lavagem import DaoTipoLavagem


daoTipoVeiculo = DaoTipoVeiculo()
daoTipoLavagem = DaoTipoLavagem()



class TipoLavagemVeiculo:

    FIELDS_TO_VALIDATE = ['tipo_veiculo_id','tipo_lavagem_id','codigo']

    def __init__(self,tipo_veiculo_id,tipo_lavagem_id,codigo, id = None) -> None:
        self.id = id
        self.tipo_veiculo_id = tipo_veiculo_id
        self.tipo_lavagem_id = tipo_lavagem_id
        self.codigo = codigo
    

    def get_dict(self):
        return({
            'id':self.id,
            'tipo_veiculo_id':daoTipoVeiculo.get_by_id(self.tipo_veiculo_id).get_dict(),
            'tipo_lavagem_id':daoTipoLavagem.get_by_id(self.tipo_lavagem_id).get_dict(),
            'codigo':self.codigo
            })

    def __str__(self) -> str:
        return f'Tipo de Veículo: {self.tipo_veiculo_id} Tipo de Lavagem: {self.tipo_lavagem_id} Código: {self.codigo}' 
        