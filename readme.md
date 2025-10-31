<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=d63aff"/>
<img src="https://img.shields.io/badge/Mailgun-F83600?style=for-the-badge&logo=mailgun&logoColor=white"/>
<img src="https://img.shields.io/badge/git-F05033?style=for-the-badge&logo=git&logoColor=white"/>
</p>

<br>

<p align="center">
  <img height="100px" src="./utils/logo.png">
</p>

<br><br>

# API RESTful de Catálogo de Hotéis



Este projeto é uma API RESTful robusta desenvolvida em Python, focada na construção de um backend para um sistema de catálogo e reserva de hotéis.

A aplicação utiliza o ecossistema Flask (Flask-RESTful, Flask-SQLAlchemy) para criar endpoints seguros e eficientes para gerenciamento de hotéis, usuários e sites. É um projeto prático que demonstra conceitos essenciais de desenvolvimento backend.

## Índice

1. [Consultar Hotéis](#1-consultar-hotéis)
2. [Cadastro de Usuário](#2-cadastro-de-usuário)
3. [Login de Usuário](#3-login-de-usuário)
4. [Criar Hotel](#4-criar-hotel)
5. [Atualizar Hotel](#5-atualizar-hotel)
6. [Deletar Hotel](#6-deletar-hotel)
7. [Logout de Usuário](#7-logout-de-usuário)
8. [Consultar Dados de Usuário](#8-consultar-dados-de-usuário)
9. [Deletar Usuário](#9-deletar-usuário)
10. [Confirmação de Usuário](#10-confirmação-de-usuário)
11. [Gerenciar Sites](#11-gerenciar-sites)

---

## Principais Funcionalidades

* **Autenticação Segura:** Sistema completo de login, cadastro e logout usando **Flask-JWT-Extended**, incluindo *blocklisting* (antiga blacklist) de tokens.
* **Confirmação de E-mail:** Integração com a API da **Mailgun** para envio de e-mails de confirmação de cadastro de novos usuários.
* **CRUD Completo:** Operações de Criar, Ler, Atualizar e Deletar para múltiplos recursos (Hotéis, Usuários, Sites).
* **Filtros Dinâmicos:** Endpoint de busca de hotéis com filtros avançados por cidade, faixa de estrelas e faixa de diária, usando consultas SQL parametrizadas.
* **Persistência de Dados:** Uso do ORM **SQLAlchemy** para mapeamento objeto-relacional, com configuração adaptada de MySQL para **SQLite** local.

---


## 1. Consultar Hotéis

### 1.1. Listar Todos os Hotéis (com filtros)

Lista todos os hotéis do sistema, podendo receber filtros personalizados via query parameters.

**Endpoint:** `GET /hoteis`

**Parâmetros de Consulta (Query Parameters):**

| Parâmetro | Tipo | Descrição | Valor Padrão |
|-----------|------|-----------|--------------|
| `cidade` | string | Filtrar hotéis pela cidade escolhida | Nulo |
| `estrelas_min` | float | Avaliações mínimas de hotéis (0 a 5) | 0 |
| `estrelas_max` | float | Avaliações máximas de hotéis (0 a 5) | 5 |
| `diaria_min` | float | Valor mínimo da diária (R$ 0 a R$ 10.000) | 0 |
| `diaria_max` | float | Valor máximo da diária (R$ 0 a R$ 10.000) | 10000 |
| `limit` | integer | Quantidade máxima de elementos por página | 50 |
| `offset` | integer | Quantidade de elementos a pular (paginação) | 0 |

**Exemplo de Requisição:**

```http
GET /hoteis?estrelas_min=4.5&limit=10&offset=0&diaria_max=600
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "hoteis": [
    {
      "hotel_id": "bravo",
      "nome": "Hotel Bravo",
      "estrelas": 4.5,
      "diaria": 550.00,
      "cidade": "São Paulo",
      "site_id": 1
    },
    {
      "hotel_id": "alpha",
      "nome": "Hotel Alpha",
      "estrelas": 5.0,
      "diaria": 600.00,
      "cidade": "Rio de Janeiro",
      "site_id": 1
    }
  ]
}
```

---

### 1.2. Consultar Hotel Específico

Visualiza os dados de um hotel específico pelo seu ID.

**Endpoint:** `GET /hoteis/{hotel_id}`

**Exemplo de Requisição:**

```http
GET /hoteis/bravo
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "hotel_id": "bravo",
  "nome": "Hotel Bravo",
  "estrelas": 4.5,
  "diaria": 550.00,
  "cidade": "São Paulo",
  "site_id": 1
}
```

**Resposta de Erro (Hotel não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "Hotel not found."
}
```

---

## 2. Cadastro de Usuário

### 2.1. Criar Novo Usuário

Registra um novo usuário no sistema. Um e-mail de confirmação será enviado automaticamente.

**Endpoint:** `POST /cadastro`

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "login": "ana",
  "senha": "senha123",
  "email": "ana@email.com"
}
```

**Resposta de Sucesso:**

**Status:** `201 Created`

```json
{
  "message": "User created successfully!"
}
```

**Resposta de Erro (Login já existe):**

**Status:** `400 Bad Request`

```json
{
  "message": "The login 'ana' already exists."
}
```

**Resposta de Erro (Email já existe):**

**Status:** `400 Bad Request`

```json
{
  "message": "The email 'ana@email.com' already exists."
}
```

**Resposta de Erro (Email não fornecido):**

**Status:** `400 Bad Request`

```json
{
  "message": "The field 'email' cannot be left blank."
}
```

**Observações:**
- O usuário é criado com status `ativado: false`
- Um e-mail de confirmação é enviado para o endereço fornecido
- O usuário precisa confirmar o e-mail antes de fazer login

---

## 3. Login de Usuário

### 3.1. Autenticar Usuário

Realiza o login de um usuário e retorna um token de acesso JWT.

**Endpoint:** `POST /login`

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "login": "ana",
  "senha": "senha123"
}
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta de Erro (Credenciais inválidas):**

**Status:** `401 Unauthorized`

```json
{
  "message": "The username or password is incorrect."
}
```

**Resposta de Erro (Usuário não confirmado):**

**Status:** `400 Bad Request`

```json
{
  "message": "User not confirmed."
}
```

**Observações:**
- O token retornado deve ser usado no header `Authorization: Bearer {token}` para endpoints protegidos
- O usuário precisa ter confirmado seu e-mail para fazer login

---

## 4. Criar Hotel

### 4.1. Cadastrar Novo Hotel

Cria um novo hotel no sistema. Requer autenticação.

**Endpoint:** `POST /hoteis/{hotel_id}`

**Headers:**

```
Content-Type: application/json
Authorization: Bearer {token_de_acesso}
```

**Body:**

```json
{
  "nome": "Hotel Teste",
  "estrelas": 4.0,
  "diaria": 450.00,
  "cidade": "Curitiba",
  "site_id": 1
}
```

**Resposta de Sucesso:**

**Status:** `201 Created`

```json
{
  "hotel_id": "teste",
  "nome": "Hotel Teste",
  "estrelas": 4.0,
  "diaria": 450.00,
  "cidade": "Curitiba",
  "site_id": 1
}
```

**Resposta de Erro (Hotel já existe):**

**Status:** `400 Bad Request`

```json
{
  "message": "Hotel id 'teste' already exists."
}
```

**Resposta de Erro (Site inválido):**

**Status:** `400 Bad Request`

```json
{
  "message": "The hotel must be associated to a valid site id."
}
```

**Resposta de Erro (Não autorizado):**

**Status:** `401 Unauthorized`

```json
{
  "message": "Missing Authorization Header"
}
```

---

## 5. Atualizar Hotel

### 5.1. Atualizar Dados do Hotel

Atualiza os dados de um hotel existente ou cria um novo hotel se não existir. Requer autenticação.

**Endpoint:** `PUT /hoteis/{hotel_id}`

**Headers:**

```
Content-Type: application/json
Authorization: Bearer {token_de_acesso}
```

**Body:**

```json
{
  "nome": "Hotel Teste Atualizado",
  "estrelas": 4.5,
  "diaria": 500.00,
  "cidade": "Curitiba",
  "site_id": 1
}
```

**Resposta de Sucesso (Hotel atualizado):**

**Status:** `200 OK`

```json
{
  "hotel_id": "teste",
  "nome": "Hotel Teste Atualizado",
  "estrelas": 4.5,
  "diaria": 500.00,
  "cidade": "Curitiba",
  "site_id": 1
}
```

**Resposta de Sucesso (Hotel criado):**

**Status:** `201 Created`

```json
{
  "hotel_id": "novo",
  "nome": "Hotel Novo",
  "estrelas": 3.5,
  "diaria": 350.00,
  "cidade": "Florianópolis",
  "site_id": 1
}
```

**Resposta de Erro (Não autorizado):**

**Status:** `401 Unauthorized`

```json
{
  "message": "Missing Authorization Header"
}
```

---

## 6. Deletar Hotel

### 6.1. Remover Hotel

Deleta um hotel do sistema. Requer autenticação.

**Endpoint:** `DELETE /hoteis/{hotel_id}`

**Headers:**

```
Authorization: Bearer {token_de_acesso}
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "message": "Hotel deleted."
}
```

**Resposta de Erro (Hotel não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "Hotel not found."
}
```

**Resposta de Erro (Não autorizado):**

**Status:** `401 Unauthorized`

```json
{
  "message": "Missing Authorization Header"
}
```

---

## 7. Logout de Usuário

### 7.1. Encerrar Sessão

Invalida o token de acesso atual, fazendo logout do usuário.

**Endpoint:** `POST /logout`

**Headers:**

```
Authorization: Bearer {token_de_acesso}
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "message": "Logged out successfully!"
}
```

**Observações:**
- Após o logout, o token não poderá mais ser utilizado
- O usuário precisará fazer login novamente para obter um novo token

---

## 8. Consultar Dados de Usuário

### 8.1. Obter Informações do Usuário

Retorna os dados de um usuário específico (exceto a senha).

**Endpoint:** `GET /usuarios/{user_id}`

**Headers:**

```
Content-Type: application/json
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "user_id": 2,
  "login": "ana",
  "email": "ana@email.com",
  "ativado": true
}
```

**Resposta de Erro (Usuário não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "User not found."
}
```

---

## 9. Deletar Usuário

### 9.1. Remover Usuário

Deleta um usuário do sistema. Requer autenticação.

**Endpoint:** `DELETE /usuarios/{user_id}`

**Headers:**

```
Authorization: Bearer {token_de_acesso}
```

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "message": "User deleted."
}
```

**Resposta de Erro (Usuário não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "User not found."
}
```

**Resposta de Erro (Token expirado):**

**Status:** `401 Unauthorized`

```json
{
  "message": "Token has expired"
}
```

---

## 10. Confirmação de Usuário

### 10.1. Confirmar Cadastro

Ativa a conta do usuário após o registro. Este endpoint é acessado através do link enviado por e-mail.

**Endpoint:** `GET /confirmacao/{user_id}`

**Resposta de Sucesso:**

**Status:** `200 OK`

Retorna uma página HTML confirmando a ativação da conta.

**Resposta de Erro (Usuário não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "User id '{user_id}' not found."
}
```

**Observações:**
- Este endpoint é normalmente acessado através de um link no e-mail de confirmação
- Após a confirmação, o campo `ativado` do usuário é definido como `true`

---

## 11. Gerenciar Sites

### 11.1. Listar Todos os Sites

Retorna uma lista de todos os sites cadastrados no sistema.

**Endpoint:** `GET /sites`

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "sites": [
    {
      "site_id": 1,
      "url": "https://exemplo.com",
      "hoteis": [
        {
          "hotel_id": "bravo",
          "nome": "Hotel Bravo",
          "estrelas": 4.5,
          "diaria": 550.00,
          "cidade": "São Paulo",
          "site_id": 1
        }
      ]
    }
  ]
}
```

---

### 11.2. Consultar Site Específico

Retorna os dados de um site específico, incluindo todos os hotéis associados.

**Endpoint:** `GET /sites/{url}`

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "site_id": 1,
  "url": "https://exemplo.com",
  "hoteis": [
    {
      "hotel_id": "bravo",
      "nome": "Hotel Bravo",
      "estrelas": 4.5,
      "diaria": 550.00,
      "cidade": "São Paulo",
      "site_id": 1
    }
  ]
}
```

**Resposta de Erro (Site não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "Site not found."
}
```

---

### 11.3. Criar Novo Site

Cadastra um novo site no sistema.

**Endpoint:** `POST /sites/{url}`

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "site_id": 2,
  "url": "https://novosite.com",
  "hoteis": []
}
```

**Resposta de Erro (Site já existe):**

**Status:** `400 Bad Request`

```json
{
  "message": "The site 'https://novosite.com' already exists."
}
```

**Resposta de Erro (Erro interno):**

**Status:** `500 Internal Server Error`

```json
{
  "message": "An internal error ocurred trying to create a new site."
}
```

---

### 11.4. Deletar Site

Remove um site do sistema. Todos os hotéis associados ao site também serão deletados.

**Endpoint:** `DELETE /sites/{url}`

**Resposta de Sucesso:**

**Status:** `200 OK`

```json
{
  "message": "Site deleted."
}
```

**Resposta de Erro (Site não encontrado):**

**Status:** `404 Not Found`

```json
{
  "message": "Site not found."
}
```

**Observações:**
- Ao deletar um site, todos os hotéis vinculados a ele também são removidos
- Esta operação é irreversível

---

## Códigos de Status HTTP

A API utiliza os seguintes códigos de status:

| Código | Descrição |
|--------|-----------|
| `200 OK` | Requisição bem-sucedida |
| `201 Created` | Recurso criado com sucesso |
| `400 Bad Request` | Requisição inválida ou dados incorretos |
| `401 Unauthorized` | Falha na autenticação ou token inválido/ausente |
| `404 Not Found` | Recurso não encontrado |
| `500 Internal Server Error` | Erro interno do servidor |

---

## Autenticação

A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos:

1. Faça login através do endpoint `/login`
2. Utilize o token retornado no header das requisições:

```
Authorization: Bearer {seu_token_aqui}
```

**Endpoints que requerem autenticação:**
- `POST /hoteis/{hotel_id}`
- `PUT /hoteis/{hotel_id}`
- `DELETE /hoteis/{hotel_id}`
- `POST /logout`
- `DELETE /usuarios/{user_id}`

---

## Configuração de E-mail

O sistema utiliza Mailgun para envio de e-mails de confirmação:

- **Domínio:** `sandbox7405257bdaeb4b0791617210d2eabb5a.mailgun.org`
- **From:** `NO-REPLY <no-reply@restapi.com>`

---

## Estrutura do Banco de Dados

### Tabela: hoteis

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `hotel_id` | String (PK) | Identificador único do hotel |
| `nome` | String(80) | Nome do hotel |
| `estrelas` | Float | Avaliação do hotel (0 a 5) |
| `diaria` | Float | Valor da diária |
| `cidade` | String(40) | Cidade onde o hotel está localizado |
| `site_id` | Integer (FK) | Referência ao site |

### Tabela: usuarios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user_id` | Integer (PK) | Identificador único do usuário |
| `login` | String(40) | Login do usuário (único) |
| `senha` | String(40) | Senha do usuário |
| `email` | String(80) | E-mail do usuário (único) |
| `ativado` | Boolean | Status de ativação da conta |

### Tabela: sites

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `site_id` | Integer (PK) | Identificador único do site |
| `url` | String(80) | URL do site |

---

## Exemplos de Uso

### Exemplo 1: Buscar hotéis em São Paulo com 4+ estrelas

```http
GET /hoteis?cidade=São Paulo&estrelas_min=4&limit=20
```

### Exemplo 2: Criar conta e fazer login

```http
# 1. Criar conta
POST /cadastro
Content-Type: application/json

{
  "login": "joao",
  "senha": "minhasenha",
  "email": "joao@email.com"
}

# 2. Confirmar e-mail (clicar no link recebido)

# 3. Fazer login
POST /login
Content-Type: application/json

{
  "login": "joao",
  "senha": "minhasenha"
}
```

### Exemplo 3: Criar um novo hotel

```http
POST /hoteis/meu-hotel
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

{
  "nome": "Meu Hotel",
  "estrelas": 4.0,
  "diaria": 300.00,
  "cidade": "Salvador",
  "site_id": 1
}
```

---

## 📸 Ambiente de Desenvolvimento e Testes

Para garantir um processo de desenvolvimento eficiente e facilitar a compreensão da estrutura do projeto, utilizamos as seguintes ferramentas:

### Visual Studio Code (VS Code)

Nosso principal ambiente de desenvolvimento integrado (IDE), configurado para Python e com extensões que otimizam a produtividade, depuração e organização do código.

<p align="center">
  <img src="utils/vs_code.png" alt="Screenshot do VS Code com o projeto">
  <br>
  <sub>Uma visão do projeto no VS Code, destacando a estrutura de arquivos e um trecho de código.</sub>
</p>

### Apidog (Ferramenta de Testes de API)

Utilizamos o Apidog para testar e documentar os endpoints da API. Ele permite o envio de requisições HTTP (GET, POST, PUT, DELETE), visualização das respostas e gerenciamento de autenticação, agilizando o desenvolvimento e a validação das funcionalidades.

#### Confirmação de Usuário Cadastrado

<p align="center">
  <img src="utils/apidog_confimar.png" alt="Screenshot do Apidog testando a rota de confirmação de usuário">
  <br>
  <sub>Exemplo de requisição para confirmar o cadastro de um usuário.</sub>
</p>

#### Listagem de Sites Cadastrados

<p align="center">
  <img src="utils/apidog_lista_sites.png" alt="Screenshot do Apidog testando a rota de listagem de sites">
  <br>
  <sub>Exemplo de requisição GET para listar todos os sites registrados na API.</sub>
</p>


---


## Observações Importantes

1. **Segurança:** Nunca compartilhe seu token de acesso. Ele é pessoal e intransferível.
2. **Validação:** Todos os campos obrigatórios devem ser preenchidos nas requisições.
3. **Confirmação de E-mail:** Usuários devem confirmar seu e-mail antes de fazer login.
4. **Paginação:** Use `limit` e `offset` para paginar resultados de listagens.
5. **Relacionamentos:** Hotéis devem estar associados a um site válido (site_id).

---

## Suporte

Para dúvidas ou problemas com a API, entre em contato com a equipe de desenvolvimento.