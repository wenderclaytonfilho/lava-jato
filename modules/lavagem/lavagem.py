#Retornar os objetos, não os IDs!
from modules.funcionario.dao_funcionario import FuncionarioDao
from modules.tipoLavagemVeiculo.dao_tipo_lavagem_veiculo import DaoTipoLavagemVeiculo
from modules.veiculo.dao_veiculo import VeiculoDao

funcionarioDao = FuncionarioDao()
tlvDao = DaoTipoLavagemVeiculo()
veiculoDao = VeiculoDao()


class Lavagem:

    FIELDS_TO_VALIDATE = ['veiculo_id','funcionario_id','data_hora_entrada','data_hora_saida','tipo_lavagem_veiculo_id','codigo']
    def __init__(self,veiculo_id,funcionario_id,data_hora_entrada,data_hora_saida,tipo_lavagem_veiculo_id,codigo,id=None) -> None:
        self.id = id
        self.veiculo_id = veiculo_id
        self.funcionario_id = funcionario_id
        self.data_hora_entrada = data_hora_entrada
        self.data_hora_saida = data_hora_saida
        self.tipo_lavagem_veiculo_id = tipo_lavagem_veiculo_id
        self.codigo = codigo

    def __str__(self) -> str:
        return f'Lavagem {self.id}° - Veiculo: {self.veiculo_id} - Funcionario: {self.funcionario_id} - Entrada: {self.data_hora_entrada} -  Saída: {self.data_hora_saida}  - Tipo de Lavagem: {self.tipo_lavagem_veiculo_id} - Código: {self.codigo}'

    def get_dict(self):
        return{
            'id':self.id,
            'veiculo_id':veiculoDao.get_by_id(self.veiculo_id).get_dict(),
            'funcionario_id':funcionarioDao.get_by_id(self.funcionario_id).get_dict(),
            'data_hora_entrada':self.data_hora_entrada,
            'data_hora_saida':self.data_hora_saida,
            'tipo_lavagem_veiculo_id':tlvDao.get_by_id(self.tipo_lavagem_veiculo_id).get_dict(),
            'codigo':self.codigo
        }