-- Criação do banco de dados com charset UTF-8
CREATE DATABASE IF NOT EXISTS db_escola 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE db_escola;
-- Tabela de tb_enderecos
CREATE TABLE tb_enderecos (
    cep VARCHAR(10) PRIMARY KEY,
    endereco VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_carros
CREATE TABLE tb_carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fabricante VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    especificacao VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_alunos
CREATE TABLE tb_alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_aluno VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    cep VARCHAR(10),
    carro_id INT,
    FOREIGN KEY (cep) REFERENCES tb_enderecos(cep),
    FOREIGN KEY (carro_id) REFERENCES tb_carros(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_disciplinas
CREATE TABLE tb_disciplinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_disciplina VARCHAR(255) NOT NULL,
    carga INT NOT NULL,
    semestre INT NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_notas
CREATE TABLE tb_notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    disciplina_id INT NOT NULL,
    nota DECIMAL(5, 2),
    FOREIGN KEY (aluno_id) REFERENCES tb_alunos(id),
    FOREIGN KEY (disciplina_id) REFERENCES tb_disciplinas(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Ver as tabelas no Banco de dados MySQl!
use db_escola
select * from tb_alunos;
select * from tb_enderecos;
select * from tb_notas;
select * from tb_carros;
select * from tb_disciplinas;
-------------------
select * 
from tb_alunos
where id = 7 ;

select * 
from tb_alunos                      -- Só uma letra ou variações funcionam também 
where nome_aluno like "ISABELLA%" ; -- Todas as pessoas com o mesmo nome  tem que colocar % 

select * 
from tb_alunos
order by id desc; -- Ordenar 

-------------------

select a.aluno_id, b.nome_aluno, a.nota -- Filtrando as informações que eu estou buscando 
from tb_notas as a      -- a e b são apelidos
inner join tb_alunos as b -- Temporário para visualização única
on a.aluno_id=b.id   -- Merge entre duas tabelas ( eu tinha o id em notas e agora tenho seus nomes ) 

------------ Filtrando ainda mais ----------- OBS: Se jogar no python vai funcionar no VS
select a.aluno_id, b.nome_aluno, a.disciplina_id, c.nome_disciplina, a.nota 
from tb_notas as a      
inner join tb_alunos as b 
on a.aluno_id=b.id   
inner join tb_disciplinas as c
on a.disciplina_id = c.id

------------------ Criando uma view ---------------
create view vw_notas_alunos as  

select a.aluno_id, b.nome_aluno, a.disciplina_id, c.nome_disciplina, a.nota - 
from tb_notas as a     
inner join tb_alunos as b 
on a.aluno_id=b.id    
inner join tb_disciplinas as c
on a.disciplina_id = c.id

-- Chamando a view 
select * from vw_notas_alunos -- Select da view que ja está pronta 

---------------- Chamado a view e filtrando por nota -------------------
select * from vw_notas_alunos -- Select da view que ja está pronta 
where nota >= 7

-------------------

update tb_alunos -- Update de dados
set email="isabella@email.com"
where id= 7  -- ID ou NOME 
where nome="ISABELLA"
--------- Adicionar dados ou editar ------------
UPDATE tb_enderecos
SET endereco = 'Mar belo rua 10', cidade = 'Salvador', estado = 'BA'
WHERE cep = '12345-008';
----------------------
-- Deletar uma pessoa / Muito dificil 
delete from tb_alunos
where nome_aluno = 'fernanda costa'