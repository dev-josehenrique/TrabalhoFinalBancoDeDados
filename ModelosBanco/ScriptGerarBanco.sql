-- Arquivo: "ScriptGerarBanco.sql"

CREATE TABLE raca (
    id_raca SERIAL PRIMARY KEY,
    linhagem VARCHAR(50)
);

CREATE TABLE propriedade (
    id_propriedade SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    localizacao VARCHAR(200)
);

CREATE TABLE piquete (
    id_piquete SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    lotacao_max INTEGER,
    id_propriedade INTEGER,
    FOREIGN KEY(id_propriedade) REFERENCES propriedade (id_propriedade)
);

CREATE TABLE bovino (
    id_bovino SERIAL PRIMARY KEY,
    id_raca INTEGER,
    idbovino_matriz INTEGER,
    sexo VARCHAR(50),
    nome VARCHAR(50),
    data_nascimento DATE,
    registro_po VARCHAR(50),
    n_brinco INTEGER UNIQUE, -- Chave Candidata (CK)
    FOREIGN KEY(id_raca) REFERENCES raca (id_raca)
);

ALTER TABLE bovino ADD FOREIGN KEY(idbovino_matriz) REFERENCES bovino (id_bovino);

CREATE TABLE veterinario (
    id_veterinario SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    crmv VARCHAR(50)
);

CREATE TABLE historico (
    id_bovino INTEGER,
    data DATE,
    descricao VARCHAR(1000),
    PRIMARY KEY(id_bovino, data),
    FOREIGN KEY(id_bovino) REFERENCES bovino (id_bovino)
);

CREATE TABLE tipo_tratamento (
    id_tipo_tratamento SERIAL PRIMARY KEY,
    tipo VARCHAR(50)
);

CREATE TABLE medicamento (
    id_medicamento SERIAL PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE doenca (
    id_doenca SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    sintoma VARCHAR(200)
);

CREATE TABLE tratamento (
    id_tratamento SERIAL PRIMARY KEY,
    id_veterinario INTEGER,
    id_doenca INTEGER,
    data DATE,
    id_bovino INTEGER,
    id_tipo_tratamento INTEGER,
    UNIQUE(data, id_bovino, id_tipo_tratamento), -- Chaves Candidatas (CKs)
    FOREIGN KEY(id_veterinario) REFERENCES veterinario (id_veterinario),
    FOREIGN KEY(id_doenca) REFERENCES doenca (id_doenca),
    FOREIGN KEY(id_bovino) REFERENCES bovino (id_bovino),
    FOREIGN KEY(id_tipo_tratamento) REFERENCES tipo_tratamento (id_tipo_tratamento)
);

CREATE TABLE piquete_bovino (
    data_saida DATE,
    data_entrada DATE,
    id_piquete INTEGER,
    id_bovino INTEGER,
    PRIMARY KEY(data_entrada, id_piquete, id_bovino),
    FOREIGN KEY(id_piquete) REFERENCES piquete (id_piquete),
    FOREIGN KEY(id_bovino) REFERENCES bovino (id_bovino)
);

CREATE TABLE vacina (
    id_vacina SERIAL PRIMARY KEY,
    marca VARCHAR(50),
    antigeno VARCHAR(50)
);

CREATE TABLE vacina_bovino (
    dose VARCHAR(50),
    data DATE,
    id_vacina INTEGER,
    id_bovino INTEGER,
    PRIMARY KEY(data, id_vacina, id_bovino),
    FOREIGN KEY(id_bovino) REFERENCES bovino (id_bovino),
    FOREIGN KEY(id_vacina) REFERENCES vacina (id_vacina)
);

CREATE TABLE pesagem (
    id_bovino INTEGER,
    data TIMESTAMP,
    peso NUMERIC,
    PRIMARY KEY(id_bovino, data),
    FOREIGN KEY(id_bovino) REFERENCES bovino (id_bovino)
);

CREATE TABLE receita (
    dose VARCHAR(50),
    id_medicamento INTEGER,
    id_tratamento INTEGER,
    PRIMARY KEY(id_medicamento, id_tratamento),
    FOREIGN KEY(id_medicamento) REFERENCES medicamento (id_medicamento),
    FOREIGN KEY(id_tratamento) REFERENCES tratamento (id_tratamento)
);