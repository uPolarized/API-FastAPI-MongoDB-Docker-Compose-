# API de Usuários com FastAPI, MongoDB e Docker

Projeto desenvolvido para praticar a criação de uma API RESTful completa, utilizando um ambiente totalmente containerizado com Docker Compose.

##  Tecnologias Utilizadas

* **Python 3.11**
* **FastAPI** - Para a construção da API.
* **MongoDB** - Como banco de dados NoSQL.
* **Motor** - Driver assíncrono para a comunicação com o MongoDB.
* **Pydantic V2** - Para validação e serialização de dados.
* **Docker & Docker Compose** - Para a containerização da aplicação e do banco de dados.

##  Funcionalidades

* CRUD completo de usuários (Criar, Ler, Atualizar, Deletar).
* Validação de dados na entrada (e-mail, idade, nome).
* Garante que o e-mail de cada usuário seja único.
* Sistema de busca, filtros avançados (por idade, status) e paginação na listagem de usuários.
* Geração automática de documentação interativa via Swagger UI e ReDoc.

3.  **Pronto!** A API estará disponível em `http://localhost:8000`.

##  Documentação da API

Após executar o projeto, a documentação interativa gerada pelo Swagger UI pode ser acessada em:

➡ **[http://localhost:8000/docs](http://localhost:8000/docs)**

Lá, é possível visualizar e testar todos os endpoints disponíveis.

### Endpoints Principais

* `POST /users/` - Cria um novo usuário.
* `GET /users/` - Lista todos os usuários, com suporte a filtros e paginação.
* `GET /users/{id}` - Retorna um usuário específico pelo seu ID.
* `PUT /users/{id}` - Atualiza os dados de um usuário existente.
* `DELETE /users/{id}` - Remove um usuário do sistema.
