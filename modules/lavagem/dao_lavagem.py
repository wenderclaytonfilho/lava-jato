from datetime import datetime
from database.connect import ConnectDataBase
from modules.lavagem.lavagem import Lavagem ##


class LavagemDao:

    _TABLE_NAME_ = 'lavagem'
    _INSERT_INTO_ = "INSERT INTO {} (veiculo_id,funcionario_id,data_hora_entrada,data_hora_saida,tipo_lavagem_veiculo_id,codigo) values ('{}' ,'{}','{}','{}' ,'{}' ,'{}') RETURNING id"
    _SELECT_ALL_ = f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_CODIGO = "SELECT * FROM {} WHERE CODIGO = '{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID = {}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {} = '{}', {} = '{}', {} = '{}', {} = '{}' , {} = '{}', {} = '{}' WHERE ID = {}"

    def __init__(self) ->None:
        self.database = ConnectDataBase().get_instance()

    def salvar(self,lavagem):
        if lavagem.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_.format(self._TABLE_NAME_,lavagem.veiculo_id, lavagem.funcionario_id, lavagem.data_hora_entrada , lavagem.data_hora_saida, lavagem.tipo_lavagem_veiculo_id,lavagem.codigo))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            lavagem.id = id
            return lavagem
        else:
            raise Exception("Ocorreu um erro ao salvar a Lavagem")
    
    def get_all(self):
        lavagens = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL_)
        all_lavagens = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for lavagem_query in all_lavagens:
            data = dict(zip(columns_name , lavagem_query))
            lavagem = Lavagem(**data)
            lavagens.append(lavagem)
        cursor.close()
        if lavagens:
            return lavagens
        else:
            raise Exception("Erro ao buscar todas as lavagens!")

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        lavagem = cursor.fetchone()
        if not lavagem:
            return None
        data = dict(zip(columns_name, lavagem))
        lavagem = Lavagem(**data)
        cursor.close()
        return lavagem

    def get_by_codigo(self,codigo):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CODIGO.format(self._TABLE_NAME_, codigo))
        columns_name = [desc[0] for desc in cursor.description]
        lavagem = cursor.fetchone()
        if not lavagem:
            return None
        data = dict(zip(columns_name, lavagem))
        lavagem = Lavagem(**data)
        cursor.close()
        return lavagem


    def delete_lavagem(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()

    def update_lavagem(self, newLavagem, oldLavagem):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME_,"veiculo_id",newLavagem.veiculo_id,"funcionario_id", newLavagem.funcionario_id, "data_hora_entrada",newLavagem.data_hora_entrada,"data_hora_saida", newLavagem.data_hora_saida, "tipo_lavagem_veiculo_id",newLavagem.tipo_lavagem_veiculo_id,'codigo',newLavagem.codigo, oldLavagem.id))
        self.database.commit()
        cursor.close()

    def converter_data(self, data):
        return datetime.strptime(data,"%Y-%m-%d %H:%M:%S")