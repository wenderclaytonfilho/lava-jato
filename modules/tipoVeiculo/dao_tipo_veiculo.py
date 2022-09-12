from database.connect import ConnectDataBase
from modules.tipoVeiculo.tipo_veiculo import TipoVeiculo

class DaoTipoVeiculo:

    _TABLE_NAME_ = "tipo_veiculo"
    _INSERT_INTO_ = f'INSERT INTO {_TABLE_NAME_} (descricao,codigo) values (%s, %s) RETURNING id' 
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_CODIGO = "SELECT * FROM {} WHERE CODIGO='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {} = '{}' WHERE ID = {}"

    def __init__(self) -> None:
        self.database = ConnectDataBase().get_instance()

    def salvar(self,tipo_veiculo):
        if tipo_veiculo.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_,(tipo_veiculo.descricao,tipo_veiculo.codigo))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            tipo_veiculo.id = id
            return tipo_veiculo
        else:
            raise Exception("Erro ao salvar o tipo de Veículo!")

    
    def get_all(self):
        tiposveiculo = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_tipos = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for tipos_query in all_tipos:
            data = dict(zip(columns_name,tipos_query))
            tipo_veiculo = TipoVeiculo(**data)
            tiposveiculo.append(tipo_veiculo)
        cursor.close()
        if tiposveiculo:
            return tiposveiculo
        else:
            raise Exception ("Erro ao buscar todos os tipos de Veículo!")

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        tipo_veiculo = cursor.fetchone()
        if not tipo_veiculo:
            return None
        data = dict(zip(columns_name, tipo_veiculo))
        tipo_veiculo = TipoVeiculo(**data)
        cursor.close()
        return tipo_veiculo

    def get_by_codigo(self, codigo):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CODIGO.format(self._TABLE_NAME_, codigo))
        columns_name = [desc[0] for desc in cursor.description]
        tipo_veiculo = cursor.fetchone()
        if not tipo_veiculo:
            return None
        data = dict(zip(columns_name, tipo_veiculo))
        tipo_veiculo = TipoVeiculo(**data)
        cursor.close()
        return tipo_veiculo

    def delete_tipo_veiculo(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()

    def update_tipo_veiculo(self,newTipoVeiculo, oldTipoVeiculo):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME_,"descricao",newTipoVeiculo.descricao,oldTipoVeiculo.id))
        self.database.commit()
        cursor.close()