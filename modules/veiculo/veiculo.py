from modules.cliente.dao_cliente import ClienteDao
from modules.tipoVeiculo.dao_tipo_veiculo import DaoTipoVeiculo

clienteDao = ClienteDao()
tipoVeiculoDao = DaoTipoVeiculo()


class Veiculo:


    FIELDS_TO_VALIDATE = ['placa','tipo_id','endereco','cliente_id']

    def __init__(self,placa,tipo_id,endereco,cliente_id,id = None) -> None:
        self.id = id
        self.placa = placa
        self.tipo_id = tipo_id
        self.endereco = endereco
        self.cliente_id = cliente_id
        
    def __str__(self) -> str:
        return f'Placa: {self.placa} Endereço: {self.endereco}'

    def get_dict(self):
        return{
            'id':self.id,
            'placa':self.placa,
            'tipo_id':tipoVeiculoDao.get_by_id(self.tipo_id).get_dict(),
            'endereco':self.endereco,
            'cliente':clienteDao.get_by_id(self.cliente_id).get_dict()
        }