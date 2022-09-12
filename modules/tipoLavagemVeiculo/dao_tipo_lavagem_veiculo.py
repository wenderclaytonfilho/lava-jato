from database.connect import ConnectDataBase
from modules.tipoLavagemVeiculo.tipo_lavagem_veiculo import TipoLavagemVeiculo


class DaoTipoLavagemVeiculo:

    _TABLE_NAME_ = 'tipo_lavagem_veiculo'
    _INSERT_INTO_ = f'INSERT INTO {_TABLE_NAME_} (tipo_veiculo_id,tipo_lavagem_id,codigo) values (%s, %s, %s) RETURNING id'
    _SELECT_ALL_ =  f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_CODIGO = "SELECT * FROM {} WHERE CODIGO = '{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {} = '{}', {} = '{}', {} = '{}' WHERE ID = {}"

    def __init__(self) -> None:
        self.database = ConnectDataBase().get_instance()

    def salvar (self, tipoLavagemVeiculo):
        if tipoLavagemVeiculo.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_,(tipoLavagemVeiculo.tipo_veiculo_id,tipoLavagemVeiculo.tipo_lavagem_id,tipoLavagemVeiculo.codigo))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            tipoLavagemVeiculo.id = id
            return tipoLavagemVeiculo
        else:
            raise Exception("Erro ao salvar o Tipo De lavagem e Veículo")

    def get_all(self):
        tiposLavagemVeiculo = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL_)
        all_tiposLavagemVeiculo = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for tlv_query in all_tiposLavagemVeiculo:
            data = dict(zip(columns_name, tlv_query))
            tipoLavagemVeiculo = TipoLavagemVeiculo(**data)
            tiposLavagemVeiculo.append(tipoLavagemVeiculo)
        cursor.close()
        if tiposLavagemVeiculo:
            return tiposLavagemVeiculo
        else:
            raise Exception("Ocorreu um erro ao buscar os tiposLavagemVeiculo!")

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        tipoLavagemVeiculo = cursor.fetchone()
        if not tipoLavagemVeiculo:
            return None
        data = dict(zip(columns_name, tipoLavagemVeiculo))
        tipoLavagemVeiculo = TipoLavagemVeiculo(**data)
        cursor.close()
        return tipoLavagemVeiculo    

    def get_by_codigo(self,codigo):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CODIGO.format(self._TABLE_NAME_, codigo))
        columns_name = [desc[0] for desc in cursor.description]
        tipoLavagemVeiculo = cursor.fetchone()
        if not tipoLavagemVeiculo:
            return None
        data = dict(zip(columns_name, tipoLavagemVeiculo))
        tipoLavagemVeiculo = TipoLavagemVeiculo(**data)
        cursor.close()
        return tipoLavagemVeiculo    

     #Tlv -> TipoLavagemVeiculo
    def delete_tlv(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()
    
    #Tlv -> TipoLavagemVeiculo
    def update_tlv(self, newTlv, oldTlv):
        cursor = self.database.cursor()
        cursor.execute(
            self._UPDATE.format(self._TABLE_NAME_,"tipo_veiculo_id",newTlv.tipo_veiculo_id,"tipo_lavagem_id",newTlv.tipo_lavagem_id,"codigo",newTlv.codigo,oldTlv.id
            ))
        self.database.commit()
        cursor.close()
