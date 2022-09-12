import psycopg2

class ConnectDataBase:
    
    def __init__(self):
        self._connect = psycopg2.connect(
            host = "localhost",
            database="PedroLavagens",
            user ="postgres",
            password = "admin"
        )

    def get_instance(self):
        return self._connect