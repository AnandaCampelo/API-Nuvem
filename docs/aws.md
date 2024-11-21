# Guia de Deploy no AWS com EKS

Este guia descreve os passos para configurar e implementar a aplicação no AWS usando o Elastic Kubernetes Service (EKS).

Esses foram os passos feitos para realizar deploy desta API, que está disponível [`aqui`](http://aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com/docs#/).

## Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração da AWS CLI](#configuração-da-aws-cli)
3. [Criação do Cluster EKS](#criação-do-cluster-eks)
4. [Configuração do Kubernetes](#configuração-do-kubernetes)
5. [Deploy da Aplicação e Banco de Dados](#deploy-da-aplicação-e-banco-de-dados)

## Pré-requisitos

- Conta AWS configurada
- AWS CLI instalado
- kubectl instalado
- eksctl instalado

## Configuração da AWS CLI

Rode o comando abaixo e insira as credenciais de usuário:

```sh
aws configure
```

- Access Key ID
- Secret Access Key
- Região que deseja utilizar (i.e: us-east-1)
- Formato de saída padrão: JSON

## Criação do Cluster EKS

Rode o comando abaixo para criar o cluster EKS:

```sh
eksctl create cluster --name cloud-cluster --nodes 2
```

- Este comando cria um cluster EKS com dois nós. 
- O processo pode levar vários minutos.

## Configuração do Kubernetes

Rode o comando abaixo para atualizar o **kubeconfig** para usar o novo cluster:

```sh
aws eks update-kubeconfig --name cloud-cluster
```

- Para verificar os nós do cluster:
    ```sh
    kubectl get nodes
    ```

## Deploy da Aplicação e Banco de Dados

**1. Crio o arquivo `db-deployment.yml`:**

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_USER
          value: "user"
        - name: POSTGRES_PASSWORD
          value: "password"
        - name: POSTGRES_DB
          value: "dbname"
        ports:
        - containerPort: 5432
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
```

**2. Crie o arquivo `app-deployment.yml`:**

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: seu_usuario_dockerhub/sua_imagem:sua_tag
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://user:password@postgres:5432/dbname"
        - name: SECRET_KEY
          value: "sua_senha"
        - name: OPENWEATHERMAP_API_KEY
          value: "seu_token"
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: fastapi
```

**3. Aplique os arquivos de deployment:**

```sh
kubectl apply -f db-deployment.yml
kubectl apply -f app-deployment.yml
```

**4. Verifique os pods:**

```sh
kubectl get pods
```

    NAME                        READY   STATUS    RESTARTS   AGE
    fastapi-66dccdb476-rsbfl    1/1     Running   0          5s
    postgres-59898c8667-vww4z   1/1     Running   0          3m8s


**5. Verifique os serviços:**

```sh
kubectl get services
```

    NAME              TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)        AGE
    fastapi-service   LoadBalancer   10.100.58.131   aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com   80:31152/TCP   9s
    kubernetes        ClusterIP      10.100.0.1      <none>                                                                    443/TCP        5h53m
    postgres          ClusterIP      10.100.16.70    <none>                                                                    5432/TCP       3m13s 

Procure pelo `EXTERNAL-IP` do `fastapi-service` e acesse a aplicação no navegador ([`aqui`](http://aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com/docs#/)) ou via curl:

- `registrar`:

```sh
  curl -X 'POST' \
    'http://aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com/registrar' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "nome": "string",
    "email": "string",
    "senha": "string"
  }' -w '\n'
```

- `login`:

```sh
  curl -X 'POST' \
    'http://aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "email": "string",
    "senha": "string"
  }' -w '\n'
```

- `consultar`:

```sh
  curl -X GET \
    http://aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com/consultar \
    -H 'Authorization: Bearer seu_token_jwt_aqui' \
    -H 'accept: application/json' -w '\n'
```