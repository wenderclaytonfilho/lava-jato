from database.connect import ConnectDataBase
from modules.tipoLavagem.tipo_lavagem import TipoLavagem

class DaoTipoLavagem:

    _TABLE_NAME_ = "tipo_lavagem"
    _INSERT_INTO_ = f'INSERT INTO {_TABLE_NAME_} (descricao,codigo) values (%s,%s) RETURNING id' 
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_CODIGO = "SELECT * FROM {} WHERE CODIGO = '{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {} = '{}', {} = '{}' WHERE ID = {}"

    def __init__(self) -> None:
        self.database = ConnectDataBase().get_instance()

    def salvar(self,tipo_lavagem):
        if tipo_lavagem.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_,(tipo_lavagem.descricao,tipo_lavagem.codigo))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            tipo_lavagem.id = id
            return tipo_lavagem
        else:
            raise Exception("Erro ao salvar o tipo de Lavagem!")

    
    def get_all(self):
        tipos_lavagem = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_tipos = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for tipos_query in all_tipos:
            data = dict(zip(columns_name,tipos_query))
            tipo_lavagem = TipoLavagem(**data)
            tipos_lavagem.append(tipo_lavagem)
        cursor.close()
        if tipos_lavagem:
            return tipos_lavagem
        else:
            raise Exception ("Erro ao buscar todos os tipos de lavagem!")

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        tipo_lavagem = cursor.fetchone()
        if not tipo_lavagem:
            return None
        data = dict(zip(columns_name, tipo_lavagem))
        tipo_lavagem = TipoLavagem(**data)
        cursor.close()
        return tipo_lavagem

    def get_by_codigo(self, codigo):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CODIGO.format(self._TABLE_NAME_, codigo))
        columns_name = [desc[0] for desc in cursor.description]
        tipo_lavagem = cursor.fetchone()
        if not tipo_lavagem:
            return None
        data = dict(zip(columns_name, tipo_lavagem))
        tipo_lavagem = TipoLavagem(**data)
        cursor.close()
        return tipo_lavagem

    
    def delete_tipo_lavagem(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()

    def update_tipo_lavagem(self,newTipoLavagem, oldTipoLavagem):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME_,"descricao",newTipoLavagem.descricao,'codigo',newTipoLavagem.codigo,oldTipoLavagem.id))
        self.database.commit()
        cursor.close()