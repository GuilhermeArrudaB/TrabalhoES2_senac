# Middleware Pokemon API 

## Descrição
Este projeto é um middleware construído com **FastAPI** que consome a [PokeAPI](https://pokeapi.co/) para buscar informações 
sobre Pokemon (como nome, ID, tipos e habilidades). Utiliza o padrão **Abstract Factory** para abstrair o acesso à API, promovendo flexibilidade e escalabilidade, 
com uma camada de repositório para gerenciar dados.

### Funcionalidades
- Buscar um Pokemon por ID ou nome (`/pokemon/{id_or_name}`).
- Listar Pokemons com paginação (`/pokemon?limit=20&offset=0`).

## Como Executar
1. Clone o repositório e navegue até o diretório do projeto.
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
4. Acesse a API em `http://localhost:8000` e a documentação em `http://localhost:8000/docs`.

## Estrutura do Projeto
- `api/endpoints/`: Endpoints FastAPI para Pokemon.
- `core/`: Configurações e implementação do Abstract Factory.
- `models/`: Modelos Pydantic para validação de dados.
- `services/`: Lógica de negócio.
- `repository/`: Gerenciamento de acesso a dados.
- `main.py`: Inicialização da aplicação.

## Uso do Abstract Factory
O padrão **Abstract Factory** é implementado em `core/factory.py` para abstrair o acesso à PokeAPI. A classe abstrata `APIServiceFactory` define métodos para 
buscar Pokemons (`get_pokemon` e `get_pokemon_list`), enquanto `PokeAPIFactory` implementa a comunicação com a PokeAPI.
Isso permite trocar a API por outra (ex.: uma API interna) criando uma nova fábrica, sem alterar o código do serviço ou endpoints, garantindo flexibilidade e manutenção fácil.

## Executando Testes
Para executar os testes unitários:
```bash
pytest tests/test_pokemon_endpoints.py -v
```
Os testes verificam cenários de sucesso, erro 404 (Pokémon não encontrado) e erros internos.