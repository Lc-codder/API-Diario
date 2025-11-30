# Gerenciador de Tarefas - Projeto Integrado

Este projeto foi desenvolvido como parte da avaliação da disciplina, integrando conhecimentos de **Programação Orientada a Objetos**, **Banco de Dados Relacional**, **APIs REST** e **Interfaces Gráficas (GUI)**.

O sistema consiste em um gerenciador de tarefas onde é possível criar, listar, atualizar e excluir tarefas, associando-as a categorias específicas. A arquitetura separa claramente o Banco de Dados, a API e a Interface do Usuário.

## 📋 Funcionalidades

* **CRUD Completo:** Criação, Leitura, Atualização e Exclusão de Tarefas e Categorias.
* **Banco de Dados Relacional:** Uso de SQLite com relacionamento entre tabelas (`tasks` e `categories`).
* **API Local:** Backend construído com FastAPI servindo os dados para a interface.
* **Interface Gráfica:** Aplicação Desktop desenvolvida com Tkinter.
* **Persistência:** Os dados são salvos localmente no arquivo `database.db`.

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface:** Tkinter
* **API:** FastAPI & Uvicorn
* **Banco de Dados:** SQLite3
* **Requisições HTTP:** Biblioteca `requests`

## 📂 Estrutura do Projeto

* `api.py`: Contém as rotas da API (GET, POST, PUT, DELETE) e inicialização do servidor FastAPI.
* `db.py`: Gerencia a conexão com o banco de dados e execução dos comandos SQL.
* `gui.py`: Contém a lógica da interface gráfica (janelas, botões, listagem) e comunicação com a API.
* `main.py`: Arquivo principal para iniciar a aplicação gráfica e garantir a criação do banco.
* `models.py`: Definição das classes/modelos de dados (`Task`, `Category`).
* `seed.py`: Script auxiliar para popular o banco de dados com dados iniciais.

## 🚀 Como Executar o Projeto

Para o funcionamento correto, o sistema requer que a **API** e a **Interface Gráfica** sejam executadas simultaneamente.

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Instale as dependências necessárias referentes ao bloco de notas "requirements".

