# 🚢 Titanic ML: API de Predição e Implantação.

## 📌 Sobre o Projeto.

Este projeto foi desenvolvido como parte de um case técnico para vaga de Machine Learning Jr, com o objetivo de construir uma API completa para predição de sobrevivência de passageiros do Titanic, utilizando arquitetura serverless na AWS.

A solução implementa desde o modelo de Machine Learning até o deploy em produção utilizando boas práticas de engenharia de dados e infraestrutura como código.

---

## 🧠 Problema de Negócio.

Dado um conjunto de características de um passageiro, prever a probabilidade de sobrevivência no Titanic.

Esse tipo de problema é comum em cenários como:

* Análise de risco.
* Concessão de crédito.
* Previsão de comportamento de clientes.

---

## 🏗️ Arquitetura da Solução.

Cliente → API Gateway → AWS Lambda → Modelo ML → DynamoDB.

### Tecnologias utilizadas:

* Python.
* Scikit-learn.
* Docker.
* AWS Lambda (container).
* API Gateway.
* DynamoDB.
* Amazon ECR.
* Terraform.
* OpenAPI 3.0.

---

## 📁 Estrutura do Projeto.

```
case-titanic-api/
│
├── lambda/
│   ├── app.py             # Código principal da API
│   ├── Dockerfile         # Container da Lambda
│   ├── requirements.txt   # Dependências
│   └── model.pkl          # Modelo treinado
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── openapi.yaml       # Definição da API
│
├── README.md
└── .gitignore
```

---

## 🤖 Modelo de Machine Learning.

O modelo utilizado é um:

```python
RandomForestClassifier
```

### Features esperadas pelo modelo:

```
['Age', 'Parch', 'SibSp', 'Embarked_S', 'Sex_male', 'Pclass', 'Fare', 'Embarked_Q']
```

⚠️ A ordem das features é crítica para o funcionamento correto da predição.

---

## 🚀 Endpoints da API.

### 🔹 POST /sobreviventes

Realiza a predição de sobrevivência.

#### Exemplo de requisição:

```json
{
  "data": [[22, 0, 0, 1, 1, 3, 7.25, 0]]
}
```

#### Exemplo de resposta:

```json
[
  {
    "id": "f9d6f914-3257-4060-ad1a-a26833539c31",
    "probabilidade": 0.14212644439053707
  }
]
```

---

### 🔹 GET /sobreviventes

Lista todos os passageiros avaliados.

---

### 🔹 GET /sobreviventes/{id}

Consulta um passageiro específico.

---

### 🔹 DELETE /sobreviventes/{id}

Remove um registro do banco.

---

## 🔗 URL da API em Produção

Após o deploy no API Gateway, a API ficou disponível publicamente no seguinte endpoint:

```bash
https://frifupezv0.execute-api.us-east-1.amazonaws.com/dev
```

---

## 🧪 Como testar a API

Abaixo estão exemplos reais de uso dos endpoints.

---

### 🔹 POST /sobreviventes

```bash
POST https://frifupezv0.execute-api.us-east-1.amazonaws.com/dev/sobreviventes
```

Body:

```json
{
  "data": [[22, 0, 0, 1, 1, 3, 7.25, 0]]
}
```

---

### 🔹 GET /sobreviventes

```bash
GET https://frifupezv0.execute-api.us-east-1.amazonaws.com/dev/sobreviventes
```

---

### 🔹 DELETE /sobreviventes/{id}

```bash
DELETE https://frifupezv0.execute-api.us-east-1.amazonaws.com/dev/sobreviventes/{id}
```

Substitua `{id}` pelo identificador retornado no POST.

---

## ☁️ Infraestrutura (Terraform)

A infraestrutura foi criada com Terraform, incluindo:

* Lambda (container via ECR).
* API Gateway.
* DynamoDB.
* IAM Roles e Policies.

---

## 🐳 Deploy com Docker.

### Build da imagem:

```bash
docker buildx build --platform linux/amd64 --provenance=false -t ml-titanic:v1 .
```

### Enviar para o ECR:

```bash
docker tag ml-titanic:v1 <ECR_URL>:v1
docker push <ECR_URL>:v1
```

---

## ⚙️ Deploy com Terraform.

```bash
terraform init
terraform apply -var="lambda_image_uri=<ECR_URL>:v1"
```

---

## 🧪 Testes

Os testes foram realizados utilizando Postman/Insomnia.

### Fluxo validado:

1. POST → cria registro.
2. GET → lista registros.
3. GET por ID → consulta específica.
4. DELETE → remove registro.

---

## 🚧 Principais Desafios e Soluções.

### ❌ Problema 1: Limitação de pacote Lambda (ZIP).

Erro:

* Limite de tamanho.
* Dependências pesadas (numpy, sklearn).

✔️ Solução:

* Migração para Lambda com Docker.

---

### ❌ Problema 2: Erro "No module named numpy".

Causa:

* Dependências não estavam no container.

✔️ Solução:

* Ajuste no `requirements.txt`.
* Rebuild da imagem.

---

### ❌ Problema 3: Erro de compatibilidade (Windows vs Linux)

Causa:

* Modelo treinado em ambiente diferente.

✔️ Solução:

* Uso de container padronizado (Linux).

---

### ❌ Problema 4: Erro 404 nas rotas.

Causa:

* Estrutura do evento da API Gateway v2.

✔️ Solução:

```python
event["requestContext"]["http"]["method"]
event["rawPath"]
```

---

### ❌ Problema 5: Erro de features.

```
X has 6 features, but model expects 8
```

✔️ Solução:

* Inspeção do modelo.
* Ajuste do input.

---

## 📊 Resultado Final:

✔️ API funcionando em produção.
✔️ Predição com Machine Learning.
✔️ Persistência no DynamoDB.
✔️ Infraestrutura como código.
✔️ Deploy automatizado com Docker.

---

## 📈 Melhorias Futuras:

* Validação automática das features.
* Pipeline de treinamento.
* CI/CD com GitHub Actions.
* Monitoramento com CloudWatch estruturado.
* Versionamento de modelo.

---

## 👩‍💻 Autora:

**Marcela Morais**

---

## 💬 Observação

Este projeto demonstra não apenas conhecimento em Machine Learning, mas também em:

* Engenharia de Software.
* Cloud Computing (AWS).
* Infraestrutura como código.
* Deploy de modelos em produção.
