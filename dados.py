# Arquivo: dados.py

inserts_bovinos = {
    'RACA': """
        INSERT INTO raca (linhagem) VALUES 
        ('Nelore'), 
        ('Jersey'),
        ('Brahman');
    """,
    'PROPRIEDADE': """
        INSERT INTO propriedade (nome, localizacao) VALUES 
        ('Fazenda Esperanca', 'Praia-Grande');
    """,
    'PIQUETE': """
        INSERT INTO piquete (nome, lotacao_max, id_propriedade) VALUES 
        ('Piquete A', 30, 1),
        ('Piquete B', 30, 1),
        ('Piquete C', 25, 1),
        ('Piquete D - Maternidade', 14, 1);
    """,
    'BOVINO': """
        INSERT INTO bovino (id_raca, idbovino_matriz, sexo, nome, data_nascimento, registro_po, n_brinco) VALUES 
        (1, NULL, 'Fêmea', 'Bonita', '2020-01-10', 'ABCZ F 1045', 845102), 
        (2, NULL, 'Fêmea', 'Fafa', '2020-03-20', NULL, 845115),   
        (3, NULL, 'Fêmea', 'Cola-branca', '2019-11-10', NULL, 309481),
        (1, NULL, 'Fêmea', 'TV', '2021-05-05', NULL, 512993),     
        
        (2, NULL, 'Fêmea', 'Jaguane', '2022-01-12', NULL, 781024),
        (3, NULL, 'Macho', 'Bandido', '2021-08-22', NULL, 781055),
        (1, NULL, 'Fêmea', 'Mimosa', '2023-02-14', NULL, 912301), 
        (2, NULL, 'Fêmea', 'Estrela', '2022-09-30', NULL, 912344),
        (3, NULL, 'Macho', 'Trovao', '2021-12-01', NULL, 650112), 
        (1, NULL, 'Macho', 'Malhado', '2023-05-18', NULL, 912389),
        
        (2, NULL, 'Fêmea', 'Pintada', '2020-07-07', NULL, 443019),
        (3, NULL, 'Fêmea', 'Bruta', '2019-04-25', NULL, 219844),  
        (1, NULL, 'Macho', 'Sereno', '2022-11-11', NULL, 781090), 
        (2, NULL, 'Macho', 'Valente', '2023-03-03', NULL, 912405),
        (3, NULL, 'Macho', 'Guerreiro', '2021-10-10', NULL, 650188),
        
        (1, NULL, 'Macho', 'Boiadeiro', '2024-02-10', 'ABCZ M 8831', 990142), 
        (2, NULL, 'Fêmea', 'Lua', '2020-05-12', NULL, 845201),
        (3, NULL, 'Macho', 'Soberano', '2021-07-20', NULL, 650210),
        (1, NULL, 'Fêmea', 'Majestade', '2020-11-30', NULL, 512999),
        (2, NULL, 'Fêmea', 'Tita', '2022-02-28', NULL, 781120),
        
        (1, 1, 'Macho', 'Bunitu', '2026-05-10', NULL, 105633),
        (2, 2, 'Fêmea', 'DVD', '2026-05-15', NULL, 105641);
    """,
    'PIQUETE_BOVINO': """
        INSERT INTO piquete_bovino (data_saida, data_entrada, id_piquete, id_bovino) VALUES 
        ('2026-04-01', '2026-03-01', 1, 5), ('2026-04-01', '2026-03-01', 1, 6), 
        ('2026-04-01', '2026-03-01', 1, 7), ('2026-04-01', '2026-03-01', 1, 8), 
        ('2026-04-01', '2026-03-01', 1, 9), ('2026-04-01', '2026-03-01', 1, 10),
        ('2026-04-01', '2026-03-01', 2, 11), ('2026-04-01', '2026-03-01', 2, 12), 
        ('2026-04-01', '2026-03-01', 2, 13), ('2026-04-01', '2026-03-01', 2, 14), 
        ('2026-04-01', '2026-03-01', 2, 15), ('2026-04-01', '2026-03-01', 2, 17),
        ('2026-04-01', '2026-03-01', 2, 18), ('2026-04-01', '2026-03-01', 2, 19),
        ('2026-04-01', '2026-03-01', 2, 20),
        ('2026-04-01', '2026-03-01', 3, 1), ('2026-04-01', '2026-03-01', 3, 2),
        ('2026-04-01', '2026-03-01', 3, 3), ('2026-04-01', '2026-03-01', 3, 4),

        ('2026-05-01', '2026-04-01', 1, 5), ('2026-05-01', '2026-04-01', 1, 6), 
        ('2026-05-01', '2026-04-01', 1, 7), ('2026-05-01', '2026-04-01', 1, 8), 
        ('2026-05-01', '2026-04-01', 1, 9), ('2026-05-01', '2026-04-01', 1, 10),
        ('2026-05-01', '2026-04-01', 1, 11), ('2026-05-01', '2026-04-01', 1, 12), 
        ('2026-05-01', '2026-04-01', 1, 13), ('2026-05-01', '2026-04-01', 1, 14), 
        ('2026-05-01', '2026-04-01', 1, 15), ('2026-05-01', '2026-04-01', 1, 17),
        ('2026-05-01', '2026-04-01', 1, 18), ('2026-05-01', '2026-04-01', 1, 19),
        ('2026-05-01', '2026-04-01', 1, 20),
        
        (NULL, '2026-04-01', 4, 1), (NULL, '2026-04-01', 4, 2),
        ('2026-05-15', '2026-04-01', 3, 3), ('2026-05-15', '2026-04-01', 3, 4),
        ('2026-05-20', '2026-04-20', 4, 16),
        
        ('2026-06-01', '2026-05-01', 2, 5), ('2026-06-01', '2026-05-01', 2, 6), 
        ('2026-06-01', '2026-05-01', 2, 7), ('2026-06-01', '2026-05-01', 2, 8), 
        ('2026-06-01', '2026-05-01', 2, 9), ('2026-06-01', '2026-05-01', 2, 10),
        ('2026-06-01', '2026-05-20', 2, 16),
        ('2026-06-01', '2026-05-01', 3, 11), ('2026-06-01', '2026-05-01', 3, 12), 
        ('2026-06-01', '2026-05-01', 3, 13), ('2026-06-01', '2026-05-01', 3, 14), 
        ('2026-06-01', '2026-05-01', 3, 15), ('2026-06-01', '2026-05-01', 3, 17),
        ('2026-06-15', '2026-05-01', 3, 18), -- SOBERANO VENDIDO EM 15/06 (SAIU E NÃO ENTROU EM LUGAR NENHUM)
        ('2026-06-01', '2026-05-01', 3, 19),
        ('2026-06-01', '2026-05-01', 3, 20),
        
        (NULL, '2026-05-10', 4, 21), (NULL, '2026-05-15', 4, 22),
        (NULL, '2026-05-15', 4, 3), (NULL, '2026-05-15', 4, 4),
        
        (NULL, '2026-06-01', 3, 5), (NULL, '2026-06-01', 3, 6), 
        (NULL, '2026-06-01', 3, 7), (NULL, '2026-06-01', 3, 8), 
        (NULL, '2026-06-01', 3, 9), (NULL, '2026-06-01', 3, 10),
        (NULL, '2026-06-01', 3, 16), 
        
        (NULL, '2026-06-01', 1, 11), (NULL, '2026-06-01', 1, 12), 
        (NULL, '2026-06-01', 1, 13), (NULL, '2026-06-01', 1, 14), 
        (NULL, '2026-06-01', 1, 15), (NULL, '2026-06-01', 1, 17),
        (NULL, '2026-06-01', 1, 19), (NULL, '2026-06-01', 1, 20);
    """,
    'PESAGEM': """
        INSERT INTO pesagem (id_bovino, data, peso) VALUES 
        (1, '2026-03-01 08:00:00', 450.5), (2, '2026-03-01 08:05:00', 480.0),
        (1, '2026-04-01 08:00:00', 460.0), (2, '2026-04-01 08:05:00', 490.0),
        (1, '2026-05-01 08:00:00', 475.0), (2, '2026-05-01 08:05:00', 505.0),
        (1, '2026-06-01 08:00:00', 430.0), (2, '2026-06-01 08:05:00', 460.0),
        
        (16, '2026-04-20 10:00:00', 600.0), (16, '2026-05-01 08:30:00', 605.5),
        
        -- Adicionado pesagens para os Brahmans aparecerem na media!
        (6, '2026-04-01 08:30:00', 610.0), (9, '2026-04-01 08:35:00', 630.0),
        (12, '2026-04-01 08:40:00', 450.0), (15, '2026-04-01 08:45:00', 650.0),
        (18, '2026-04-01 08:50:00', 640.0), -- Soberano antes de ser vendido
        (3, '2026-04-01 08:55:00', 480.0),
        
        (21, '2026-05-10 09:00:00', 35.0), (21, '2026-05-20 09:00:00', 41.5), (21, '2026-05-30 09:00:00', 48.2),
        (22, '2026-05-15 09:30:00', 32.0), (22, '2026-05-25 09:30:00', 38.0), (22, '2026-06-05 09:30:00', 45.0);
    """,
    'HISTORICO': """
        INSERT INTO historico (id_bovino, data, descricao) VALUES 
        (16, '2026-04-20', 'Animal adquirido em leilao por R$ 8.500,00. Sem registros da matriz. Inserido na maternidade para periodo de quarentena/adaptacao.'),
        (1, '2026-04-01', 'Transferida para a Maternidade para inicio do monitoramento pre-parto.'),
        (2, '2026-04-01', 'Transferida para a Maternidade para inicio do monitoramento pre-parto.'),
        (1, '2026-05-10', 'Parto sem intercorrencias, nascimento do Bunitu, saudavel.'),
        (2, '2026-05-15', 'Parto com leve dificuldade, mas resolvido, nascimento da DVD.'),
        (16, '2026-05-20', 'Periodo de quarentena finalizado, acostumado ao novo manejo.'),
        (3, '2026-05-15', 'Matriz movida para a maternidade para acompanhamento especializado.'),
        (4, '2026-05-15', 'Matriz movida para a maternidade para acompanhamento especializado.'),
        (18, '2026-06-15', 'Soberano vendido para o frigorifico. Fim das atividades do animal na fazenda.');
    """,
    'VETERINARIO': """
        INSERT INTO veterinario (nome, crmv) VALUES 
        ('Dr. Carlos Silva', '12345-SC'),
        ('Dra. Ana Paula', '54321-SC');
    """,
    'TIPO_TRATAMENTO': """
        INSERT INTO tipo_tratamento (tipo) VALUES 
        ('Preventivo'), ('Remediativo'), ('Emergencial'), ('Suplementacao');
    """,
    'MEDICAMENTO': """
        INSERT INTO medicamento (nome) VALUES 
        ('Ivermectina 1%'), ('Terramicina LA'), ('Vitamina ADE'), ('Calcio Injetavel');
    """,
    'DOENCA': """
        INSERT INTO doenca (nome, sintoma) VALUES 
        ('Carrapato', 'Coceira, febre e fraqueza'), ('Berne', 'Nodulos subcutaneos'),
        ('Verme', 'Perda de peso e diarreia'), ('Hipocalcemia', 'Fraqueza muscular pos-parto');
    """,
    'TRATAMENTO': """
        INSERT INTO tratamento (id_veterinario, id_doenca, data, id_bovino, id_tipo_tratamento) VALUES 
        (1, 1, '2026-04-10', 5, 2), (2, 2, '2026-05-15', 11, 2), 
        (1, 3, '2026-06-01', 1, 4), (2, 4, '2026-06-20', 2, 3), 
        (1, 1, '2026-06-25', 15, 2), (2, 1, '2026-04-05', 6, 2), 
        (1, 3, '2026-04-12', 12, 1), (2, 2, '2026-05-08', 9, 2), 
        (1, 3, '2026-05-22', 16, 1), (2, 4, '2026-06-18', 3, 4), 
        (1, 1, '2026-06-05', 18, 2); -- Soberano tratado ANTES de ser vendido
    """,
    'RECEITA': """
        INSERT INTO receita (dose, id_medicamento, id_tratamento) VALUES 
        ('10ml', 1, 1), ('15ml', 1, 2), ('5ml', 3, 3), ('500ml', 4, 4), ('12ml', 1, 5),
        ('15ml', 1, 6), ('10ml', 1, 7), ('12ml', 2, 8), ('15ml', 1, 9), ('10ml', 3, 10), ('14ml', 1, 11);
    """,
    'VACINA': """
        INSERT INTO vacina (marca, antigeno) VALUES 
        ('Vallee', 'Aftosa'), ('Ouro Fino', 'Raiva'), ('MSD', 'Clostridiose');
    """,
    'VACINA_BOVINO': """
        INSERT INTO vacina_bovino (dose, data, id_vacina, id_bovino) VALUES 
        ('5ml', '2026-05-01', 1, 1), ('5ml', '2026-05-01', 1, 2), 
        ('5ml', '2026-05-01', 1, 3), ('2ml', '2026-05-15', 2, 4);
    """
}