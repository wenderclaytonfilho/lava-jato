from flask import Flask

from modules.cliente.controller_cliente import app_cliente
from modules.funcionario.controller_funcionario import app_funcionario
from modules.tipoVeiculo.controller_tipo_veiculo import app_tipoveiculo
from modules.tipoLavagem.controller_tipo_lavagem import app_tipolavagem
from modules.veiculo.controller_veiculo import app_veiculo
from modules.tipoLavagemVeiculo.controller_tipo_lavagem_veiculo import app_tipo_lavagem_veiculo
from modules.lavagem.controller_lavagem import app_lavagem


app = Flask(__name__)

app.register_blueprint(app_cliente)
app.register_blueprint(app_funcionario)
app.register_blueprint(app_veiculo)
app.register_blueprint(app_tipoveiculo)
app.register_blueprint(app_tipolavagem)
app.register_blueprint(app_tipo_lavagem_veiculo)
app.register_blueprint(app_lavagem)

app.run()