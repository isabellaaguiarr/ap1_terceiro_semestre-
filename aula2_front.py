from sqlalchemy import create_engine, text
import streamlit as st
from pathlib import Path
from fpdf import FPDF
import pandas as pd 
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
user = os.getenv('MYSQL_USER')
senha = os.getenv('MYSQL_PASSWORD')
database_name = os.getenv('MYSQL_DATABASE')

DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

st.title("Sistema Escolar")
menu = st.sidebar.selectbox("Selecionar", ["Entrada","Cadastrar endereço", "Cadastrar aluno", "Editar aluno", "Cadastrar notas", "Upload de arquivos", "Relatório de notas"])

# Cadastrar enderecos novos 
def cadastrar_endereco(params: dict):
    sql = text("""
        INSERT INTO tb_enderecos (cep, endereco, cidade, estado)
        VALUES (:cep, :endereco, :cidade, :estado)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

if menu == "Cadastrar endereço":
    st.subheader("Cadastro de Endereço")

    cep = st.text_input("Cadastrar CEP:")
    endereco = st.text_input("Cadastrar Endereço:")
    cidade = st.text_input("Cadastrar Cidade:")
    estado = st.text_input("Cadastrar Estado:")

    if st.button("Cadastrar"):
            params = {
                'cep': cep,
                'endereco': endereco,
                'cidade': cidade,
                'estado': estado,
            }
            cadastrar_endereco(params)
            st.success("Cadastrado com sucesso!")

# Cadastrar alunos novos (Tem que ter um cep ja existente!)
def cadastrar_aluno(params: dict):
    sql = text("""
        INSERT INTO tb_alunos (nome_aluno, email, cep, carro_id)
        VALUES (:nome_aluno, :email, :cep, :carro_id)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

if menu == "Cadastrar aluno":
    st.subheader("Cadastro de aluno")

    nome_aluno = st.text_input("Cadastrar Nome do aluno:")
    email = st.text_input("Cadastrar Email:")
    cep = st.text_input("Cadastrar Cep:")
    carro_id = text(st.text_input("Cadastrar Carro:"))

    if st.button("Cadastrar"):
            params = {
                'nome_aluno': nome_aluno,
                'email': email,
                'cep': cep,
                'carro_id': carro_id, 
            }
            cadastrar_aluno(params)
            st.success("Cadastrado com sucesso!")

# Lista com o nome dos alunos e o id
def dados_alunos():
    with engine.connect() as conn:
         query = text("SELECT id, nome_aluno FROM tb_alunos")
         resultado = conn.execute(query)
         alunos = [{"id": row[0], "nome": row[1]} for row in resultado]
    return alunos

# Editar informações dos alunos ja existentes 
def editar_alunos(id, nome_aluno=None, email=None, cep=None, carro_id=None):
    with engine.begin() as conn:
        dados_atualizar = []
        params = {"id": id}

        if nome_aluno:
            dados_atualizar.append("nome_aluno = :nome_aluno")
            params["nome_aluno"] = nome_aluno

        if email:
            dados_atualizar.append("email = :email")
            params["email"] = email

        if cep:
            dados_atualizar.append("cep = :cep")
            params["cep"] = cep

        if carro_id:
            dados_atualizar.append("carro_id = :carro_id")
            params["carro_id"] = carro_id

        if not dados_atualizar:
            return {"message": "Nenhum dado para atualizar"}

        query = f"""
            UPDATE tb_alunos
            SET {", ".join(dados_atualizar)}
            WHERE id = :id
        """
        resultado = conn.execute(text(query), params)

        if resultado.rowcount == 0:
            return {"message": "Aluno não encontrado"}
        return {"message": "Dados do aluno atualizados com sucesso"}

if menu == "Editar aluno":
    st.subheader("Editar aluno")

    # Trazendo os nomes para o usuario selecionar 
    lista_alunos = dados_alunos()
    alunos_dict = {aluno["nome"]: aluno["id"] for aluno in lista_alunos}
    nome_selecionado = st.selectbox("Selecione o aluno:", list(alunos_dict.keys()))
    id = alunos_dict[nome_selecionado]

    nome_aluno = st.text_input("Editar Nome do aluno:", nome_selecionado)
    email = st.text_input("Editar Email:")
    cep = st.text_input("Editar Cep:")
    carro_id = st.text_input("Editar Carro:")

    if st.button("Editar"):
        params = {
            'id': id,
            'nome_aluno': nome_aluno ,
            'email': email ,
            'cep': cep ,
            'carro_id': carro_id , 
        }
        editar_alunos(**params)
        st.success("Editado com sucesso!")
        
# Lista com o nome das disciplinas e o id
def dados_disciplinas():
     with engine.connect() as conn:
          query2 = text("SELECT id, nome_disciplina FROM tb_disciplinas")
          resultado = conn.execute(query2)
          disciplinas = [{"id": row[0], "nome": row[1]} for row in resultado]
     return disciplinas
     
# Cadastrar as notas dos alunos 
def cadastrar_notas(params: dict):
    sql = text(""" 
        INSERT INTO tb_notas (aluno_id, disciplina_id, nota)
        VALUES (:aluno_id, :disciplina_id, :nota)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

if menu == "Cadastrar notas":
    st.subheader("Cadastro de notas")

    lista_alunos = dados_alunos()
    alunos_dict = {aluno["nome"]: aluno["id"] for aluno in lista_alunos}
    nome_selecionado = st.selectbox("Selecione o aluno:", list(alunos_dict.keys()))
    aluno_id = alunos_dict[nome_selecionado]

    lista_disciplinas = dados_disciplinas()
    disciplinas_dict = {disciplina["nome"]: disciplina["id"] for disciplina in lista_disciplinas}
    disciplina_selecionada = st.selectbox("Selecione a disciplina:", list(disciplinas_dict.keys()))
    disciplina_id = disciplinas_dict[disciplina_selecionada]

    nota = st.text_input("Cadastrar a nota:")

    if st.button("Cadastrar"):
            params = {
                'aluno_id': aluno_id,
                'disciplina_id': disciplina_id,
                'nota': nota,
            }
            cadastrar_notas(params)
            st.success("Cadastrado com sucesso!") 

# Upload de arquivos para o banco de dados
if menu == "Upload de arquivos":
    st.subheader("Upload de arquivos")
# Upload do arquivo
    arquivo = st.file_uploader("Envie um arquivo CSV, Excel ou JSON", type=["csv", "xlsx", "json"])    #  st.file_uploader permite o envio de arquivos
    if arquivo is not None:
        # Verifica o formato do arquivo
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        elif arquivo.name.endswith(".xlsx"):
            df = pd.read_excel(arquivo)
        elif arquivo.name.endswith(".json"):
            df = pd.read_json(arquivo)
        else: 
            st.stop()
        st.write("Pré-visualização dos dados:")
        st.dataframe(df)

# Adicionar os novos dados ao banco de dados
        tabelas = ["tb_alunos", "tb_enderecos", "tb_notas", "tb_carros", "tb_disciplinas"]
        tabela_escolhida = st.selectbox("Escolha a tabela para inserir os dados:", tabelas)

        def adicionar_dados(df, tabela):
            with engine.begin() as conn:
                for _, row in df.iterrows():
                    row = row.where(pd.notna(row), None)
                    colunas = ", ".join(row.index)  # Nome das colunas do arquivo
                    valores = ", ".join([f":{col}" for col in row.index]) 

                    query = text(f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})")
                    conn.execute(query, row.to_dict())

        if st.button("Enviar para o Banco"):    
                adicionar_dados(df, tabela_escolhida)
                st.success("Cadastrado com sucesso!")

# Consultar as notas ja lancadas dos alunos
def consultar_notas(aluno_id):
    sql = text(""" 
        SELECT a.nome_disciplina AS disciplina, b.nota
        FROM tb_notas b
        JOIN tb_disciplinas a ON b.disciplina_id = a.id
        WHERE b.aluno_id = :aluno_id
    """)
    with engine.begin() as conn:
        resultado = conn.execute(sql, {"aluno_id": aluno_id}).fetchall()
    return resultado

# Transformar o relatorio de nota em pdf 
def gerar_relatorio_pdf(nome_aluno, notas):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Relatório de Notas - {nome_aluno}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Disciplina", border=1, align="C")
    pdf.cell(40, 10, "Nota", border=1, align="C")
    pdf.ln()
    
    pdf.set_font("Arial", "", 12)
    for disciplina, nota in notas:
        pdf.cell(100, 10, disciplina, border=1)
        pdf.cell(40, 10, str(nota), border=1, align="C")
        pdf.ln()
    
    # Salvar PDF em memoria
    return pdf.output(dest="S").encode("latin1")

# Relatorio de notas (tem que tentar virar pdf)
if menu == "Relatório de notas":
    st.subheader("Relatório de notas")
    lista_alunos = dados_alunos()
    alunos_dict = {aluno["nome"]: aluno["id"] for aluno in lista_alunos}
    nome_selecionado = st.selectbox("Selecione o aluno:", list(alunos_dict.keys()))
    aluno_id = alunos_dict[nome_selecionado]

    if st.button("Gerar Relatório"):
        notas = consultar_notas(aluno_id)
        
        if notas:
            df = pd.DataFrame(notas, columns=["Disciplina", "Nota"])
            st.dataframe(df)

            # Botao para exportar para PDF
            pdf_bytes = gerar_relatorio_pdf(nome_selecionado, notas)
            st.download_button(label="Baixar Relatório em PDF",
                               data=pdf_bytes,
                               file_name=f"Relatorio_Notas_{nome_selecionado}.pdf",
                               mime="application/pdf")
        else:
            st.warning("Nenhuma nota encontrada para este aluno.")


