# Bulbe — Projeto Backend

Backend da plataforma Bulbe Energia, desenvolvido na disciplina Projeto Ciência de Dados II.

## Equipe

Squad Master — Bernardo A. Alvim, Felipe Nunes, Caio Freitas, Luca Bellei e Vinicius Bianchetti.

## Board do projeto

- **Board:** [Backend Sprint 1 (GitHub Projects)](https://github.com/users/bernardoalvimibmec/projects/3/views/1)
- **Backlog no GitHub:** [Issues](https://github.com/bernardoalvimibmec/Bulbe-Projeto-Backend/issues)
- **Backlog da Sprint 2, estimado e priorizado:** [docs/sprints/backlog-sprint-2.md](docs/sprints/backlog-sprint-2.md)

## Documentação

### Requisitos e contrato da API

- [Requisitos técnicos](docs/requisitos/requisitos-tecnicos-template.md)
- [Lista de endpoints da API](docs/requisitos/lista-endpoints.md)
- [Contrato OpenAPI (`docs/api/openapi.yaml`)](docs/api/openapi.yaml) — os 21 endpoints, com schemas, status codes e formato de erro. Mais detalhes em [docs/api](docs/api/README.md).

### Diagramas

- Diagrama de casos de uso da API: [PlantUML](docs/diagramas/casos-de-uso-api.puml) · [SVG](docs/diagramas/casos-de-uso-api.svg)
- Diagrama de sequência da autenticação: [PlantUML](docs/diagramas/sequencia-autenticacao.puml) · [SVG](docs/diagramas/sequencia-autenticacao.svg)
- Diagrama de atividades da autenticação: [PlantUML](docs/diagramas/atividade-autenticacao.puml) · [SVG](docs/diagramas/atividade-autenticacao.svg)
- Diagrama de classes do domínio: [PlantUML](docs/diagramas/classes-dominio.puml) · [SVG](docs/diagramas/classes-dominio.svg)

Os diagramas UML são versionados em PlantUML, junto às respectivas imagens exportadas em SVG. Para visualizar ou atualizá-los, abra os arquivos `.puml` com a extensão **PlantUML** no VS Code ou utilize o [editor online do PlantUML](https://www.plantuml.com/plantuml).

## Arquitetura

A API segue a arquitetura em quatro camadas:

```
src/
├── controllers/    Apresentação: rotas HTTP, validação de entrada, status codes
├── services/       Serviço: regras de negócio, orquestra os repositórios
├── repositories/   Persistência: interfaces e implementações (memória na Sprint 2, banco na Sprint 3)
├── domain/         Domínio: entidades com regras próprias e erros de negócio
└── main.py         Monta o app, registra as rotas, escolhe os repositórios e padroniza os erros
tests/              Testes com pytest e TestClient
docs/               Requisitos, contrato da API, diagramas e backlog
```

Todo erro da API sai no formato do contrato:

```json
{
  "codigo": "RECURSO_NAO_ENCONTRADO",
  "mensagem": "O recurso solicitado não foi encontrado.",
  "detalhes": [],
  "request_id": "req_01"
}
```

## Como rodar

Requer Python 3.11 ou superior.

```bash
python -m venv venv
venv\Scripts\activate            # Mac ou Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

A API sobe em http://localhost:8000 e o Swagger fica em http://localhost:8000/docs.

## Como testar

```bash
pytest
```

## Fluxo de trabalho

1. Pegue um card do board e mova para "Em andamento".
2. Crie uma branch a partir da `main`: `git checkout -b US06-listar-usinas`.
3. Implemente a story com testes e rode `pytest` antes de subir.
4. Abra um pull request e peça revisão de um colega.
5. Depois do merge, mova o card para "Concluído".
