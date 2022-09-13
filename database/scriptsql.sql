create table if not exists cliente(
    id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	cpf varchar(100) 
);

create table if not exists funcionario(
    id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	cpf varchar(100)
);


create table if not exists tipo_lavagem(
	 id SERIAL PRIMARY KEY,
	 descricao varchar(150),
	 codigo varchar(4)
);

create table if not exists tipo_veiculo(
	 id SERIAL PRIMARY KEY,
	 descricao varchar(150),
	 codigo varchar(4)
);

create table if not exists tipo_lavagem_veiculo(
	 id SERIAL PRIMARY KEY,
	 tipo_lavagem_id INTEGER REFERENCES tipo_lavagem(id),
	 tipo_veiculo_id INTEGER REFERENCES tipo_veiculo(id),
	 codigo varchar(4)
);

create table if not exists veiculo(
	id SERIAL PRIMARY KEY,
	placa VARCHAR(15) NOT NULL,
	tipo_id INTEGER REFERENCES tipo_veiculo(id),
	cliente_id INTEGER REFERENCES cliente(id),
	endereco VARCHAR (50)
);

create table if not exists lavagem( 
	id SERIAL PRIMARY KEY,
	veiculo_id INTEGER REFERENCES veiculo(id),
	funcionario_id INTEGER REFERENCES funcionario(id),
	data_hora_entrada TIMESTAMP WITHOUT TIME ZONE,
	data_hora_saida TIMESTAMP WITHOUT TIME ZONE,
	tipolavagem_id INTEGER REFERENCES tipo_lavagem(id),
	 codigo varchar(4)
);
