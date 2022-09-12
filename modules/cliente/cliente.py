class Cliente:

    FIELDS_TO_VALIDATE = ['nome','cpf']
    def __init__(self,nome,cpf,id=None) -> None:
        self.id = id
        self.nome = nome
        self.cpf = cpf
    
    def get_dict(self):
        return{
        'id':self.id,
        'nome':self.nome,
        'cpf':self.cpf}

    def __str__(self) -> str:
        return f'Nome: {self.nome} CPF: {self.cpf}'

