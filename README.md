# API Middleware

## Descrição
Este projeto é um middleware construído com **FastAPI** que consome a [PokéAPI](https://pokeapi.co/) e a [Digimon API](https://digimon-api.vercel.app/) para buscar informações sobre Pokemon (nome, ID, tipos, habilidades) e Digimon (nome, imagem, nível). Utiliza o padrão **Abstract Factory** para abstrair o acesso às APIs e **Facade** para simplificar a interação com os serviços, promovendo flexibilidade e escalabilidade, com uma camada de repositório para gerenciar dados e um middleware para logging de requisições.

### Funcionalidades
- Buscar um Pokemon por ID ou nome (`/pokemon/{id_or_name}`).
- Listar Pokemon com paginação (`/pokemon?limit=20&offset=0`).
- Buscar um Digimon por nome (`/digimon/{name}`).
- Listar Digimon com paginação (`/digimon?limit=20&offset=0`).
- Registrar logs de requisições (método, URL, status code, tempo de processamento) em `logs/app.log`.

## Como Executar
1. Clone o repositório e navegue até o diretório do projeto.
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
4. Acesse a API em `http://localhost:8000` e a documentação em `http://localhost:8000/docs`.

## Estrutura do Projeto
- `api/endpoints/`: Endpoints FastAPI para Pokemon e Digimon.
- `core/factories/`: Implementação do padrão Abstract Factory (classe abstrata e fábricas específicas).
- `core/adapters/`: Implementação do padrão Adapter com o adaptador do Digimon
- `core/facades/`: Implementação do padrão Facade com a facade de entidade
- `models/`: Modelos Pydantic para validação de dados.
- `services/`: Lógica de negócio.
- `repository/`: Gerenciamento de acesso a dados.
- `tests/`: Testes unitários para os endpoints.
- `logs/`: Arquivos de log gerados pelo middleware.
- `main.py`: Inicialização da aplicação.

## Uso do Abstract Factory, Facade e Adapter
O padrão **Abstract Factory** é implementado em `core/factory/` com a classe abstrata `APIServiceFactory` (em `abc_factory.py`) que define métodos genéricos (`get_entity` e `get_entity_list`), enquanto `PokeAPIFactory` (em `pokemon_factory.py`) e `DigimonAPIFactory` (em `digimon_factory.py`) implementam a comunicação com as respectivas APIs. O padrão **Facade** em `core/facade.py` simplifica a interação com o serviço, fornecendo uma interface unificada para os endpoints. O padrão **Adapter** em `core/adapters/digimon_adapter.py` uniformiza os dados da Digimon API para um formato compatível com Pokemon, facilitando a integração. Esses padrões permitem adicionar novas APIs criando novas factories e adapters, usando os endpoints de forma mais direta.

## Uso do Adapter
O padrão **Adapter** é implementado em `core/adapter.py` com a classe `DigimonAdapter`, que converte os dados da Digimon API (ex.: `name`, `img`, `level`) em um formato compatível com o da PokéAPI (ex.: `name`, `types`, `abilities`). Usado no `DigimonAPIFactory`, o adaptador mapeia o campo `level` para `types` e adiciona campos padrão, garantindo que os dados de Digimon sejam tratados uniformemente no sistema.

## Executando Testes
Para executar os testes unitários você deve acessar a pasta tests
Os testes verificam cenários de sucesso, erro 404 (entidade não encontrada) e erros internos para Pokemon e Digimon.