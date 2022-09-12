from database.connect import ConnectDataBase
from modules.funcionario.funcionario import Funcionario


class FuncionarioDao:

    _TABLE_NAME_ = 'funcionario'
    _INSERT_INTO_ = f'INSERT INTO {_TABLE_NAME_}(nome,cpf) values (%s , %s) RETURNING id'
    _SELECT_ALL_ = f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {} = '{}' WHERE ID={}"

    def __init__(self) -> None:
        self.database = ConnectDataBase().get_instance()

    def salvar(self, funcionario):
        if funcionario.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_, (funcionario.nome, funcionario.cpf))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            funcionario.id = id
            return funcionario
        else:
            raise Exception("Não é possível salvar")

    def get_all(self):
        funcionarios = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL_)
        all_funcionarios = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for funcionario_query in all_funcionarios:
            data = dict(zip(columns_name, funcionario_query))
            funcionario = Funcionario(**data)
            funcionarios.append(funcionario)
        cursor.close()
        if funcionarios:
            return funcionarios
        else:
            raise Exception("Ocorreu um erro ao buscar os funcionários!")

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        funcionario = cursor.fetchone()
        if not funcionario:
            return None
        data = dict(zip(columns_name, funcionario))
        funcionario = Funcionario(**data)
        cursor.close()
        return funcionario

    def get_by_cpf(self,cpf):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME_, cpf))
        columns_name = [desc[0] for desc in cursor.description]
        funcionario = cursor.fetchone()
        if not funcionario:
            return None
        data = dict(zip(columns_name, funcionario))
        funcionario = Funcionario(**data)
        cursor.close()
        return funcionario
    
    def delete_funcionario(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()


    def update_funcionario(self, newFuncionario, oldFuncionario):
        cursor = self.database.cursor()
        cursor.execute(
            self._UPDATE.format(self._TABLE_NAME_,"nome",newFuncionario.nome,
            "cpf",newFuncionario.cpf,
            oldFuncionario.id
            ))
        self.database.commit()
        cursor.close()



