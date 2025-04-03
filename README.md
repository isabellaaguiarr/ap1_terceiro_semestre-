# README

## Ap1 - Projeto Ciência de Dados 

### Descrição
Este projeto é composto por duas partes principais:

1. Desenvolvimento de um Sistema Web: Um site desenvolvido com Streamlit, integrado a um banco de dados, que permite funcionalidades como cadastro, edição, upload de arquivos e geração de relatórios.

2. Web Scraping de Dados Imobiliários: Um processo automatizado de coleta de dados do setor imobiliário, seguido por filtragem e armazenamento dessas informações em um banco de dados para análise e utilização posterior.

### Requisitos
Antes de executar o código, certifique-se de ter os seguintes pacotes instalados:

- Python 
- Selenium
- Pandas
- NumPy
- SQLAlchemy
- Dotenv

Para instalar os pacotes necessários, utilize o seguinte comando:
```sh
pip install selenium
pip install pandas 
pip install numpy 
pip install sqlalchemy 
pip install python-dotenv
pip install beautifulsoup4
```

### Configuração
1. **Criar um arquivo `.env`** para armazenar as credenciais do banco de dados MySQL:
   ```env
   MYSQL_HOST=seu_host
   MYSQL_PORT=sua_porta
   MYSQL_USER=seu_usuario
   MYSQL_PASSWORD=sua_senha
   MYSQL_DATABASE=nome_do_banco_de_dados
   MYSQL_DATABASE_WEB=nome_do_banco_de_dados
   ```

### Autor
Este projeto foi desenvolvido para fins de estudo.

