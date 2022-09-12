from dataclasses import dataclass
import imp
from database.connect import ConnectDataBase
from modules.veiculo.veiculo import Veiculo


class VeiculoDao:

    _TABLE_NAME_ = 'veiculo'
    _INSERT_INTO_ = f'INSERT INTO {_TABLE_NAME_}(placa,tipo_id,endereco,cliente_id) values (%s, %s, %s, %s) RETURNING id'
    _SELECT_BY_PLACA = "SELECT * FROM {} WHERE PLACA = '{}'"
    _SELECT_ALL_ = f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID = {}' 
    _UPDATE = "UPDATE {} SET {}='{}', {} = '{}' , {} = '{}', {} = '{}' WHERE ID = {}"

    def __init__(self) -> None:
        self.database = ConnectDataBase().get_instance()

    
    def salvar (self,veiculo):
        if veiculo.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_,(veiculo.placa,veiculo.tipo_id,veiculo.endereco,veiculo.cliente_id))
            id = cursor.fetchone()[0]
            cursor.close()
            veiculo.id = id
            return veiculo
        else:
            raise Exception ("Erro ao salvar o Veículo!")

    def get_all(self):
        veiculos = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL_)
        all_veiculos = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for veiculo_query in all_veiculos:
            data = dict(zip(columns_name ,veiculo_query))
            veiculo = Veiculo(**data)
            veiculos.append(veiculo)
        cursor.close()
        if veiculos:
            return veiculos
        else:
            raise Exception("Erro ao buscar Veículos")

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        veiculo = cursor.fetchone()
        if not veiculo:
            return None
        data = dict(zip(columns_name, veiculo))
        veiculo = Veiculo(**data)
        cursor.close()
        return veiculo

    def get_by_placa(self,placa):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_PLACA.format(self._TABLE_NAME_,placa))
        columns_name = [desc[0] for desc in cursor.description]
        veiculo = cursor.fetchone()
        if not veiculo:
            return None
        data = dict(zip(columns_name, veiculo))
        veiculo = Veiculo(**data)
        cursor.close()
        return veiculo


    def delete_veiculo(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()

    def update_veiculo(self,newVeiculo, oldVeiculo):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME_,"placa",newVeiculo.placa,"tipo_id",newVeiculo.tipo_id,"endereco", newVeiculo.endereco,"cliente_id",newVeiculo.cliente_id,oldVeiculo.id))
        self.database.commit()
        cursor.close()