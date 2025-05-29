# API Middleware

## Descrição
Este projeto é um middleware construído com **FastAPI** que consome a [PokéAPI](https://pokeapi.co/) e a [Digimon API](https://digimon-api.vercel.app/) para buscar informações sobre Pokémon (nome, ID, tipos, habilidades) e Digimon (nome, imagem, nível). 
Utiliza o padrão **Abstract Factory** para abstrair o acesso às APIs, promovendo flexibilidade e escalabilidade, com uma camada de repositório para gerenciar dados.

### Funcionalidades
- Buscar um Pokémon por ID ou nome (`/pokemon/{id_or_name}`).
- Listar Pokémon com paginação (`/pokemon?limit=20&offset=0`).

- Buscar um Digimon por nome (`/digimon/{name}`).
- Listar Digimon com paginação (`/digimon?limit=20&offset=0`).

## Como Executar
1. Clone o repositório e navegue até o diretório do projeto.
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```
3. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
4. Acesse a API em `http://localhost:8000` e a documentação em `http://localhost:8000/docs`.

## Estrutura do Projeto
- `api/endpoints/`: Endpoints FastAPI para Pokémon e Digimon.
- `core/`: Configurações e implementação do Abstract Factory.
- `models/`: Modelos Pydantic para validação de dados.
- `services/`: Lógica de negócio.
- `repository/`: Gerenciamento de acesso a dados.
- `tests/`: Testes unitários para os endpoints.
- `main.py`: Inicialização da aplicação.

## Uso do Abstract Factory
O padrão **Abstract Factory** é implementado em `core/factory.py` para abstrair o acesso às APIs.
A classe abstrata `APIServiceFactory` define métodos genéricos (`get_entity` e `get_entity_list`), enquanto `PokeAPIFactory` e `DigimonAPIFactory` implementam a comunicação com as respectivas APIs.
Isso permite adicionar novas APIs criando novas fábricas, sem alterar o código do serviço ou endpoints.

## Executando Testes
Para executar os testes unitários:
```bash
pytest tests/ -v
```
Os testes verificam cenários de sucesso, erro 404 (entidade não encontrada) e erros internos para Pokémon e Digimon.