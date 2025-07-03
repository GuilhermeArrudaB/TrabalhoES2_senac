# API Middleware

## Descrição
Este projeto é um middleware construído com **FastAPI** que consome a [PokéAPI](https://pokeapi.co/) e a [Digimon API](https://digimon-api.vercel.app/) para buscar informações sobre Pokemon (nome, ID, tipos, habilidades) e Digimon (nome, imagem, nível). Utiliza o padrão **Abstract Factory** para abstrair o acesso às APIs, **Facade** para simplificar a interação com os serviços, **Adapter** para uniformizar os dados das APIs, **Command** para encapsular operações como objetos, e **Iterator** para iterar sobre Digimon de forma incremental, promovendo flexibilidade, escalabilidade, e desacoplamento, com uma camada de repositório para gerenciar dados e um middleware para logging de requisições.

### Funcionalidades
- Buscar um Pokemon por ID ou nome (`/pokemon/{id_or_name}`).
- Listar Pokemon com paginação (`/pokemon?limit=20&offset=0`).
- Gerar um arquivo Excel com os 10 Pokémon mais fortes, baseado na soma dos atributos (`/pokemon/top/`).
- Gerar um relatório Excel dos 10 Pokémon mais fortes, baseado na soma dos atributos (`/pokemon/top-stats/`).
- Buscar um Digimon por nome (`/digimon/{name}`).
- Listar Digimon com paginação (`/digimon?limit=20&offset=0`).
- Listar Digimon usando um iterador para busca incremental (`/digimon/iterated/?limit=10`).
- Registrar logs de requisições (método, URL, status code, tempo de processamento) em `logs/app.log`.

## Como Executar
1. Clone o repositório e navegue até o diretório do projeto.
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv\Scripts\activate  # No Unix/Linux: source venv/bin/activate
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
- `core/adapters/`: Implementação do padrão Adapter com o adaptador do Digimon.
- `core/facades/`: Implementação do padrão Facade com a facade de entidade.
- `core/command/`: Implementação do padrão Command (interface e comandos específicos).
- `core/iterator/`: Implementação do padrão Iterator para busca incremental de Digimon.
- `models/`: Modelos Pydantic para validação de dados.
- `services/`: Lógica de negócio.
- `repository/`: Gerenciamento de acesso a dados.
- `tests/`: Testes unitários para os endpoints, Facade, Adapter, Command e Iterator.
- `logs/`: Arquivos de log gerados pelo middleware.
- `output/`: Arquivos Excel gerados pelo comando GetTopPokemonCommand.
- `main.py`: Inicialização da aplicação.

## Uso do Abstract Factory
O padrão **Abstract Factory** é implementado em `core/factories/` com a classe abstrata `APIServiceFactory` (em `abc_factory.py`) que define métodos genéricos (`get_entity` e `get_entity_list`), enquanto `PokeAPIFactory` (em `pokemon_factory.py`) e `DigimonAPIFactory` (em `digimon_factory.py`) implementam a comunicação com as respectivas APIs.

## Uso do Facade
O padrão **Facade** é implementado em `core/facades.py` com a classe `EntityFacade`, que simplifica a interação com os serviços, fornecendo uma interface unificada para os endpoints. O `EntityFacade` atua como uma camada de abstração que encapsula a lógica de acesso às APIs (PokéAPI e Digimon API) por meio das fábricas específicas (`PokeAPIFactory` e `DigimonAPIFactory`), permitindo que os endpoints e comandos (como `GetPokemonCommand`, `GetDigimonCommand`, e `GetTopPokemonCommand`) realizem operações de busca e listagem de entidades sem lidar diretamente com a complexidade das fábricas ou dos serviços subjacentes. Ele suporta operações como buscar um Pokémon ou Digimon por ID/nome (`get_entity`) e listar entidades com paginação (`get_entity_list`), garantindo consistência na interação com diferentes APIs. Esse padrão promove desacoplamento, facilitando a manutenção e a adição de novas APIs, além de centralizar o tratamento de erros e a validação de dados, reduzindo a duplicação de código nos endpoints.

## Uso do Adapter
O padrão **Adapter** é implementado em `core/adapters/digimon_adapter.py` com a classe `DigimonAdapter`, que converte os dados da Digimon API (ex.: `name`, `img`, `level`) em um formato compatível com o da PokéAPI (ex.: `name`, `types`, `abilities`). Usado no `DigimonAPIFactory`, o adaptador mapeia o campo `level` para `types` e lida com a ausência de campos opcionais como `img` e `level`, garantindo que os dados de Digimon sejam tratados uniformemente no sistema.

## Uso do Command
O padrão **Command** é implementado em `core/command/` com a interface abstrata `Command` (em `abc_command.py`) e implementações específicas em `pokemon_commands.py` e `digimon_commands.py`. Os comandos `GetPokemonCommand`, `GetPokemonListCommand`, `GetDigimonCommand`, e `GetDigimonListCommand` encapsulam operações de busca de Pokemon e Digimon. O comando `GetTopPokemonCommand` gera um arquivo Excel (`output/top_pokemon.xlsx`) com os 10 Pokémon mais fortes, baseado na soma dos atributos `base_stat` (HP, Attack, Defense, etc.), acessível via endpoints `/pokemon/top/` e `/pokemon/top-stats/`.

## Uso do Iterator
O padrão **Iterator** é implementado em `core/iterator/` com a classe `DigimonIterator` (em `iterator.py`), que permite iterar sobre Digimon de forma incremental, buscando páginas de dados da Digimon API sob demanda. Usado no endpoint `/digimon/iterated/`, o iterador carrega blocos de Digimon com base no parâmetro `limit`, reduzindo o uso de memória para grandes coleções.

## Executando Testes
Para executar os testes unitários você deve acessar a pasta tests:
```bash
pytest tests/ -v
```
Os testes verificam cenários de sucesso, erro 404 (entidade não encontrada) e erros internos para os endpoints de Pokemon e Digimon, além de testar a funcionalidade do `EntityFacade` em `core/facades.py`, do `DigimonAdapter` em `core/adapters/digimon_adapter.py`, dos comandos em `core/command/`, e do iterador em `core/iterator/`.


## Estrutura de pastas do projeto
Abaixo está o diagrama da estrutura de diretórios do projeto, representando a organização das pastas e os principais arquivos relacionados aos padrões **Abstract Factory**, **Facade**, **Adapter**, **Command**, e **Iterator**. A estrutura reflete a estrutura descrita no `README.md`.

```
app/
├── api/
│   └── endpoints/
│       ├── pokemon.py           # Endpoints para Pokémon (/pokemon/, /pokemon/top/, /pokemon/top-stats/)
│       └── digimon.py           # Endpoints para Digimon (/digimon/, /digimon/iterated/)
├── core/
│   ├── adapters/
│   │   └── digimon_adapter.py   # Implementa o padrão Adapter (DigimonAdapter)
│   ├── command/
│   │   ├── abc_command.py       # Interface abstrata Command
│   │   └── pokemon 
│   │       └── pokemon_command.py # Comandos para Pokémon (GetPokemonCommand, GetPokemonListCommand, GetTopPokemonCommand)
│   │    
│   ├── factories/
│   │   ├── abc_factory.py       # Classe abstrata APIServiceFactory
│   │   ├── pokemon_factory.py   # Implementa PokeAPIFactory para PokéAPI
│   │   └── digimon_factory.py   # Implementa DigimonAPIFactory para Digimon API
│   ├── facades/
│   │   └── entity_facade.py          # Implementa o padrão Facade (EntityFacade)
│   └── iterator/
│       └── digimon_iterator.py       # Implementa o padrão Iterator (DigimonIterator)
├── models/
│   ├── pokemon.py               # Modelo Pydantic para Pokémon
│   └── digimon.py               # Modelo Pydantic para Digimon
├── services/
│   └── api_service.py           # Lógica de negócio para acesso às APIs
├── repository/
│   └── entity_repository.py     # Gerenciamento de acesso aos dados
├── tests/
│   ├── test_pokemon_endpoints.py # Testes para endpoints de Pokémon
│   ├── test_digimon_endpoints.py # Testes para endpoints de Digimon
│   ├── test_entity_facade.py     # Testes para entity Facade
│   └── test_digimon_adapter.py   # Testes para adapter de Digimon
├── logs/
│   └── app.log                  # Arquivo de log gerado pelo middleware
├── output/
│   └── top_pokemon.xlsx         # Arquivo Excel gerado pelo GetTopPokemonCommand
├── main.py                      # Inicialização da aplicação FastAPI
└── requirements.txt             # Dependências do projeto
```