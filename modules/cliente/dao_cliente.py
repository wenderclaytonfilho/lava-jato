from database.connect import ConnectDataBase
from modules.cliente.cliente import Cliente


class ClienteDao:

    _TABLE_NAME_ = 'cliente'
    _INSERT_INTO_ = f'INSERT INTO {_TABLE_NAME_}(nome,cpf) values (%s , %s) RETURNING id'
    _SELECT_ALL_ = f'SELECT * FROM {_TABLE_NAME_}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {} = '{}' WHERE ID={}"

    def __init__(self) -> None:
        self.database = ConnectDataBase().get_instance()

    def salvar(self, cliente):
        if cliente.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO_, (cliente.nome, cliente.cpf))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            cliente.id = id
            return cliente
        else:
            raise Exception("Ocorreu um erro ao salvar o cliente")

    def get_all(self):
        clientes = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL_)
        all_clientes = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for cliente_query in all_clientes:
            data = dict(zip(columns_name, cliente_query))
            cliente = Cliente(**data)
            clientes.append(cliente)
        cursor.close()
        if clientes:
            return clientes
        else:
            raise Exception("Ocorreu um erro ao buscar os clientes!")

    def get_by_cpf(self,cpf):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME_, cpf))
        columns_name = [desc[0] for desc in cursor.description]
        cliente = cursor.fetchone()
        if not cliente:
            return None
        data = dict(zip(columns_name, cliente))
        cliente = Cliente(**data)
        cursor.close()
        return cliente        
            
    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME_, id))
        columns_name = [desc[0] for desc in cursor.description]
        cliente = cursor.fetchone()
        if not cliente:
            return None
        data = dict(zip(columns_name, cliente))
        cliente = Cliente(**data)
        cursor.close()
        return cliente

    
    def delete_cliente(self,id):
        cursor =self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME_,id))
        self.database.commit()
        cursor.close()


    def update_cliente(self, newCliente, oldCliente):
        cursor = self.database.cursor()
        cursor.execute(
            self._UPDATE.format(self._TABLE_NAME_,"nome",newCliente.nome,
            "cpf",newCliente.cpf,
            oldCliente.id
            ))
        self.database.commit()
        cursor.close()



