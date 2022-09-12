class TipoLavagem:
   
    FIELDS_TO_VALIDATE = ['descricao','codigo'] 
    def __init__(self,descricao,codigo,id = None) -> None:
        self.id = id
        self.descricao = descricao
        self.codigo = codigo
    
    def get_dict(self):
        return{
            'id':self.id,
            'descricao':self.descricao,
            'codigo':self.codigo
        }
        
    def __str__(self) -> str:
        return f'Descricao: {self.descricao} - Codigo: {self.codigo}'

