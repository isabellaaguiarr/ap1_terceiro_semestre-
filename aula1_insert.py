from sqlalchemy import create_engine, text
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
user = os.getenv('MYSQL_USER')
senha = os.getenv('MYSQL_PASSWORD')
database_name = os.getenv('MYSQL_DATABASE')

BASE_DIR = Path(__file__).parent
DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

# Adicionando novos dados / Nao rodar denovo pois ira adicionar novamente 
# So delete para apagar se repetir os dados / Muito dificil 
df_alunos = pd.read_csv(BASE_DIR / 'data' / 'tb_alunos.csv')
df_alunos.to_sql('tb_alunos', con=engine, if_exists='append', index=False)

df_alunos = pd.read_csv(BASE_DIR / 'data' / 'tb_enderecos.csv')
df_alunos.to_sql('tb_enderecos', con=engine, if_exists='append', index=False)

df_alunos = pd.read_csv(BASE_DIR / 'data' / 'tb_carros.csv')
df_alunos.to_sql('tb_carros', con=engine, if_exists='append', index=False)

df_notas = pd.read_json(BASE_DIR / 'data' / 'tb_notas.json')
df_notas.to_sql('tb_notas', con=engine, if_exists='append', index=False)

# Portas abertas e fechadas ( Pesquisar depois! )
with engine.begin() as conn:
    sql=text("""
    update tb_alunos 
    set email = "@email.com "
    where id = 
    """)
    conn.execute(sql)
