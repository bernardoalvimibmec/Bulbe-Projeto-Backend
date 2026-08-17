# Lista de Endpoints da API — Bulbe

## Identificação

- **Projeto:** Bulbe — evolução do frontend e implementação do backend
- **Empresa parceira:** Bulbe Energia
- **Equipe:** Squad Master
- **Integrantes:** Bernardo A. Alvim, Felipe Nunes, Caio Freitas, Davi Edmundo, Luca Bellei e Vinicius
- **Data:** 17/08/2026
- **Sprint / Etapa:** Sprint 1 — Design da API

## Convenções desta API

- **URL base:** `/v1`
- **Formato:** JSON no corpo das requisições e respostas, salvo redirecionamentos e respostas sem conteúdo.
- **Autenticação:** o mecanismo será definido na etapa de autenticação e autorização. Os endpoints de cliente devem exigir uma sessão válida.
- **Autorização:** um cliente só pode consultar recursos vinculados à própria conta. O backend deve validar o vínculo, mesmo que outro `clienteId` seja informado na URL.
- **Nomenclatura:** recursos no plural, em kebab-case quando houver mais de uma palavra, sem verbos nas URIs.
- **Identificadores:** exemplos usam strings opacas; o formato definitivo de ID será decidido na modelagem de dados.
- **Datas e horários:** ISO 8601, com fuso horário quando houver hora, por exemplo `2026-08-17T10:30:00-03:00`.
- **Valores monetários:** objeto com `valor` decimal e `moeda` no padrão ISO 4217.
- **Paginação:** `page` começa em 1 e `limit` informa o máximo de itens por página.
- **Erros:** retornam um objeto padronizado com `codigo`, `mensagem`, `detalhes` e `request_id`.
- **Versionamento:** a versão principal faz parte da URI para permitir evolução sem quebrar clientes existentes.

### Formato padrão de erro

```json
{
  "codigo": "RECURSO_NAO_ENCONTRADO",
  "mensagem": "O recurso solicitado não foi encontrado.",
  "detalhes": [],
  "request_id": "req_01"
}
```

## Visão Geral dos Endpoints

| Método | Recurso (URI) | Descrição | Requisito de Origem | Status HTTP |
| --- | --- | --- | --- | --- |
| POST | `/v1/contas` | Inicia cadastro ou primeiro acesso e vincula a conta ao cliente elegível | RF004, RF007 | 201 / 400 / 409 / 422 |
| POST | `/v1/sessoes` | Inicia uma sessão autenticada | RF003 | 201 / 400 / 401 / 429 |
| DELETE | `/v1/sessoes/atual` | Encerra a sessão autenticada atual | RF005 | 204 / 401 |
| GET | `/v1/clientes/{clienteId}` | Retorna os dados básicos do cliente vinculado à conta | RF006, RF007 | 200 / 401 / 403 / 404 |
| GET | `/v1/usinas` | Lista as usinas disponibilizadas pela Bulbe | RF008, RF011 | 200 / 503 |
| GET | `/v1/usinas/{usinaId}` | Retorna uma usina específica | RF008 | 200 / 404 / 503 |
| GET | `/v1/usinas/{usinaId}/creditos` | Retorna os créditos monetários de uma usina no período | RF009 | 200 / 400 / 404 / 503 |
| GET | `/v1/creditos-usinas/resumo` | Retorna o total de créditos gerados pelas usinas no período | RF010 | 200 / 400 / 503 |
| GET | `/v1/depoimentos` | Lista depoimentos públicos autorizados | RF012, RF013 | 200 / 503 |
| GET | `/v1/depoimentos/{depoimentoId}` | Retorna um depoimento público específico | RF012, RF013 | 200 / 404 / 503 |
| GET | `/v1/clientes/{clienteId}/ativacao` | Retorna a situação geral e o percentual da ativação | RF015, RF019 | 200 / 401 / 403 / 404 / 503 |
| GET | `/v1/clientes/{clienteId}/ativacao/etapas` | Lista as etapas concluídas, atual e pendentes da ativação | RF016, RF017, RF018, RF019 | 200 / 401 / 403 / 404 / 503 |
| PUT | `/v1/clientes/{clienteId}/preferencias-notificacao/ativacao` | Cria ou substitui a preferência de atualizações da ativação | RF020 | 200 / 400 / 401 / 403 / 422 |
| GET | `/v1/clientes/{clienteId}/faturas` | Lista as faturas do cliente | RF021 | 200 / 401 / 403 / 503 |
| GET | `/v1/clientes/{clienteId}/faturas/{faturaId}` | Retorna os dados de uma fatura específica | RF021 | 200 / 401 / 403 / 404 / 503 |
| GET | `/v1/clientes/{clienteId}/faturas/{faturaId}/pagamento` | Retorna a situação e os dados do pagamento da fatura | RF022 | 200 / 401 / 403 / 404 / 503 |
| GET | `/v1/clientes/{clienteId}/faturas/{faturaId}/repasse` | Retorna as etapas do repasse relacionado à CEMIG | RF023 | 200 / 401 / 403 / 404 / 503 |
| GET | `/v1/clientes/{clienteId}/historico-faturas-externo` | Redireciona para o histórico externo de faturas da Bulbe | RF024 | 302 / 401 / 403 / 404 / 503 |
| GET | `/v1/clientes/{clienteId}/notificacoes` | Lista notificações relevantes da conta | RF025 | 200 / 401 / 403 / 503 |
| GET | `/v1/clientes/{clienteId}/notificacoes/{notificacaoId}` | Retorna uma notificação específica | RF025 | 200 / 401 / 403 / 404 |
| PATCH | `/v1/clientes/{clienteId}/notificacoes/{notificacaoId}` | Atualiza o estado de leitura de uma notificação | RF025 | 200 / 400 / 401 / 403 / 404 |

## Detalhamento dos Endpoints

### POST /v1/contas

- **Descrição:** inicia o cadastro ou primeiro acesso e associa a conta digital ao cadastro correto do cliente Bulbe.
- **Requisito de origem:** RF004, RF007.
- **Autenticação:** pública.
- **Corpo da requisição:** os campos definitivos de elegibilidade e verificação ainda dependem de validação com a Bulbe.

```json
{
  "email": "cliente@exemplo.com",
  "senha": "senha-informada-pelo-cliente",
  "identificador_cliente": "identificador-fornecido-pela-bulbe",
  "codigo_verificacao": "123456"
}
```

- **Exemplo de resposta (201):**

```json
{
  "id": "conta_01",
  "cliente_id": "cliente_01",
  "email": "cliente@exemplo.com",
  "status": "ativa",
  "criada_em": "2026-08-17T10:30:00-03:00"
}
```

- **Status codes:** `201` criada; `400` JSON ou campos inválidos; `409` conta já existente; `422` cliente inelegível ou vínculo não confirmado.

### POST /v1/sessoes

- **Descrição:** valida as credenciais e inicia uma sessão para uma conta ativa.
- **Requisito de origem:** RF003.
- **Autenticação:** pública.
- **Corpo da requisição:**

```json
{
  "email": "cliente@exemplo.com",
  "senha": "senha-informada-pelo-cliente"
}
```

- **Exemplo de resposta (201):**

```json
{
  "sessao_id": "sessao_01",
  "conta_id": "conta_01",
  "cliente_id": "cliente_01",
  "expira_em": "2026-08-17T18:30:00-03:00"
}
```

- **Status codes:** `201` sessão iniciada; `400` dados inválidos; `401` credenciais inválidas; `429` excesso de tentativas.

### DELETE /v1/sessoes/atual

- **Descrição:** invalida a sessão usada na requisição.
- **Requisito de origem:** RF005.
- **Autenticação:** obrigatória.
- **Corpo da requisição:** não se aplica.
- **Resposta (204):** sem corpo.
- **Status codes:** `204` sessão encerrada; `401` sessão ausente ou inválida.

### GET /v1/clientes/{clienteId}

- **Descrição:** retorna os dados básicos do cliente associado à conta autenticada.
- **Requisito de origem:** RF006, RF007.
- **Autenticação:** obrigatória; o cliente autenticado deve possuir vínculo com `{clienteId}`.
- **Parâmetros de rota:** `clienteId` — identificador do cliente.
- **Exemplo de resposta (200):**

```json
{
  "id": "cliente_01",
  "nome_exibicao": "Cliente Bulbe",
  "email": "cliente@exemplo.com",
  "status": "ativo"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` sem autorização para o cliente; `404` cliente não encontrado.

### GET /v1/usinas

- **Descrição:** lista as usinas disponibilizadas pela Bulbe, com paginação e filtro de situação.
- **Requisito de origem:** RF008, RF011.
- **Autenticação:** pública.
- **Parâmetros de query:** `status` (opcional), `page` (opcional), `limit` (opcional).
- **Exemplo de resposta (200):**

```json
{
  "data": [
    {
      "id": "usina_01",
      "nome": "Usina Exemplo",
      "cidade": "Montes Claros",
      "estado": "MG",
      "status": "ativa"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1,
  "atualizado_em": "2026-08-17T09:00:00-03:00"
}
```

- **Status codes:** `200` sucesso; `503` fonte oficial temporariamente indisponível.

### GET /v1/usinas/{usinaId}

- **Descrição:** retorna identificação, localização e situação de uma usina disponibilizada pela Bulbe.
- **Requisito de origem:** RF008.
- **Autenticação:** pública.
- **Parâmetros de rota:** `usinaId` — identificador da usina.
- **Exemplo de resposta (200):**

```json
{
  "id": "usina_01",
  "nome": "Usina Exemplo",
  "cidade": "Montes Claros",
  "estado": "MG",
  "regiao": "Norte de Minas",
  "status": "ativa",
  "atualizado_em": "2026-08-17T09:00:00-03:00"
}
```

- **Status codes:** `200` sucesso; `404` usina não encontrada; `503` fonte oficial indisponível.

### GET /v1/usinas/{usinaId}/creditos

- **Descrição:** retorna os créditos monetários gerados pela usina em uma competência.
- **Requisito de origem:** RF009.
- **Autenticação:** pública, desde que a Bulbe confirme que os valores podem ser divulgados.
- **Parâmetros de rota:** `usinaId` — identificador da usina.
- **Parâmetros de query:** `competencia` — período obrigatório no formato `AAAA-MM`.
- **Exemplo de resposta (200):**

```json
{
  "usina_id": "usina_01",
  "competencia": "2026-08",
  "creditos": {
    "valor": 120.00,
    "moeda": "BRL"
  },
  "atualizado_em": "2026-08-17T09:00:00-03:00"
}
```

- **Status codes:** `200` sucesso; `400` competência inválida; `404` usina ou período não encontrado; `503` fonte oficial indisponível.

### GET /v1/creditos-usinas/resumo

- **Descrição:** calcula o total monetário dos créditos a partir das usinas e do período considerados no mesmo conjunto de dados.
- **Requisito de origem:** RF010.
- **Autenticação:** pública, condicionada à aprovação dos dados que podem ser divulgados.
- **Parâmetros de query:** `competencia` — período obrigatório no formato `AAAA-MM`; `status_usina` (opcional, padrão `ativa`).
- **Exemplo de resposta (200):**

```json
{
  "competencia": "2026-08",
  "criterio": "usinas_ativas",
  "quantidade_usinas": 4,
  "total_creditos": {
    "valor": 5480.00,
    "moeda": "BRL"
  },
  "atualizado_em": "2026-08-17T09:00:00-03:00"
}
```

- **Status codes:** `200` sucesso; `400` filtros inválidos; `503` dados indisponíveis ou incompletos.

### GET /v1/depoimentos

- **Descrição:** lista somente depoimentos com publicação autorizada pela Bulbe e pelo titular dos dados.
- **Requisito de origem:** RF012, RF013.
- **Autenticação:** pública.
- **Parâmetros de query:** `page` (opcional), `limit` (opcional).
- **Exemplo de resposta (200):**

```json
{
  "data": [
    {
      "id": "depoimento_01",
      "nome_publico": "Cliente de Minas Gerais",
      "localidade": "Montes Claros - MG",
      "avaliacao": 5,
      "economia_mensal": { "valor": 85.40, "moeda": "BRL" },
      "dias_para_ativacao": 72,
      "percentual_desconto": 15,
      "tempo_conta_ativa_meses": 8,
      "texto": "Minha experiência foi positiva."
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

- **Status codes:** `200` sucesso; `503` fonte de depoimentos indisponível.

### GET /v1/depoimentos/{depoimentoId}

- **Descrição:** retorna um depoimento público específico, desde que continue autorizado.
- **Requisito de origem:** RF012, RF013.
- **Autenticação:** pública.
- **Parâmetros de rota:** `depoimentoId` — identificador do depoimento.
- **Exemplo de resposta (200):**

```json
{
  "id": "depoimento_01",
  "nome_publico": "Cliente de Minas Gerais",
  "localidade": "Montes Claros - MG",
  "avaliacao": 5,
  "economia_mensal": { "valor": 85.40, "moeda": "BRL" },
  "dias_para_ativacao": 72,
  "percentual_desconto": 15,
  "tempo_conta_ativa_meses": 8,
  "texto": "Minha experiência foi positiva."
}
```

- **Status codes:** `200` sucesso; `404` inexistente ou não autorizado; `503` fonte indisponível.

### GET /v1/clientes/{clienteId}/ativacao

- **Descrição:** retorna o estado consolidado usado pela interface para representar o progresso real da ativação.
- **Requisito de origem:** RF015, RF019.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Parâmetros de rota:** `clienteId` — identificador do cliente.
- **Exemplo de resposta (200):**

```json
{
  "cliente_id": "cliente_01",
  "status": "em_andamento",
  "percentual": 50,
  "etapa_atual_id": "etapa_03",
  "iniciada_em": "2026-07-01",
  "previsao_conclusao": "2026-09-29",
  "atualizado_em": "2026-08-17T08:45:00-03:00"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `404` ativação não encontrada; `503` estado atual indisponível.

### GET /v1/clientes/{clienteId}/ativacao/etapas

- **Descrição:** lista, na ordem oficial, as etapas concluídas, a etapa atual e as etapas pendentes.
- **Requisito de origem:** RF016, RF017, RF018, RF019.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Parâmetros de rota:** `clienteId` — identificador do cliente.
- **Exemplo de resposta (200):**

```json
{
  "cliente_id": "cliente_01",
  "data": [
    {
      "id": "etapa_01",
      "ordem": 1,
      "nome": "Cadastro",
      "status": "concluida",
      "concluida_em": "2026-07-01T14:00:00-03:00"
    },
    {
      "id": "etapa_03",
      "ordem": 3,
      "nome": "Homologação",
      "status": "atual",
      "previsao_conclusao": "2026-09-15"
    },
    {
      "id": "etapa_04",
      "ordem": 4,
      "nome": "Créditos ativos",
      "status": "pendente",
      "previsao_conclusao": null
    }
  ],
  "atualizado_em": "2026-08-17T08:45:00-03:00"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `404` ativação não encontrada; `503` etapas indisponíveis.

### PUT /v1/clientes/{clienteId}/preferencias-notificacao/ativacao

- **Descrição:** cria ou substitui de forma idempotente a preferência de atualizações sobre ativação.
- **Requisito de origem:** RF020.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Corpo da requisição:** canais e regras permanecem sujeitos à confirmação de escopo.

```json
{
  "habilitada": true,
  "canais": ["email"]
}
```

- **Exemplo de resposta (200):**

```json
{
  "cliente_id": "cliente_01",
  "tipo": "ativacao",
  "habilitada": true,
  "canais": ["email"],
  "atualizada_em": "2026-08-17T10:40:00-03:00"
}
```

- **Status codes:** `200` preferência salva; `400` JSON inválido; `401` não autenticado; `403` outro cliente; `422` canal não suportado ou consentimento ausente.

### GET /v1/clientes/{clienteId}/faturas

- **Descrição:** lista as faturas do cliente com paginação e filtro por competência.
- **Requisito de origem:** RF021.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Parâmetros de query:** `competencia` (opcional), `page` (opcional), `limit` (opcional).
- **Exemplo de resposta (200):**

```json
{
  "data": [
    {
      "id": "fatura_01",
      "identificador_exibivel": "LIC 0000-0",
      "competencia": "2026-08",
      "valor": { "valor": 89.90, "moeda": "BRL" },
      "status": "paga"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1,
  "atualizado_em": "2026-08-17T09:10:00-03:00"
}
```

- **Status codes:** `200` sucesso, inclusive com lista vazia; `401` não autenticado; `403` outro cliente; `503` fonte de faturas indisponível.

### GET /v1/clientes/{clienteId}/faturas/{faturaId}

- **Descrição:** retorna valor, competência, identificador exibível e situação de uma fatura específica.
- **Requisito de origem:** RF021.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Exemplo de resposta (200):**

```json
{
  "id": "fatura_01",
  "cliente_id": "cliente_01",
  "identificador_exibivel": "LIC 0000-0",
  "competencia": "2026-08",
  "valor": { "valor": 89.90, "moeda": "BRL" },
  "status": "paga",
  "vencimento": "2026-08-15",
  "atualizado_em": "2026-08-17T09:10:00-03:00"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `404` fatura não encontrada; `503` fonte indisponível.

### GET /v1/clientes/{clienteId}/faturas/{faturaId}/pagamento

- **Descrição:** retorna a situação real do pagamento, a forma usada e o instante de confirmação, quando existentes.
- **Requisito de origem:** RF022.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Exemplo de resposta (200):**

```json
{
  "fatura_id": "fatura_01",
  "status": "confirmado",
  "forma": "pix",
  "pago_em": "2026-08-15T11:32:00-03:00",
  "valor": { "valor": 89.90, "moeda": "BRL" },
  "atualizado_em": "2026-08-15T11:35:00-03:00"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `404` fatura ou pagamento não encontrado; `503` estado indisponível.

### GET /v1/clientes/{clienteId}/faturas/{faturaId}/repasse

- **Descrição:** retorna os eventos e estados confirmados do repasse relacionado à CEMIG.
- **Requisito de origem:** RF023.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Exemplo de resposta (200):**

```json
{
  "fatura_id": "fatura_01",
  "status": "em_andamento",
  "etapas": [
    {
      "id": "repasse_etapa_01",
      "ordem": 1,
      "nome": "Pagamento confirmado",
      "status": "concluida",
      "ocorrido_em": "2026-08-15T11:32:00-03:00",
      "previsao": null,
      "mensagem": "Pagamento recebido pela Bulbe."
    },
    {
      "id": "repasse_etapa_02",
      "ordem": 2,
      "nome": "Repasse à CEMIG",
      "status": "atual",
      "ocorrido_em": null,
      "previsao": "2026-08-18",
      "mensagem": "Repasse em processamento."
    }
  ],
  "atualizado_em": "2026-08-17T09:20:00-03:00"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `404` fatura ou repasse não encontrado; `503` estado indisponível.

### GET /v1/clientes/{clienteId}/historico-faturas-externo

- **Descrição:** valida sessão, vínculo e destino e então redireciona para o sistema externo de histórico da Bulbe.
- **Requisito de origem:** RF024.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Corpo da requisição:** não se aplica.
- **Resposta (302):** sem JSON; cabeçalho `Location` contém uma URL HTTPS aprovada pela Bulbe e, se necessário, contexto de acesso de curta duração.

```http
Location: https://sistema-oficial.exemplo/historico
```

- **Status codes:** `302` redirecionamento; `401` não autenticado; `403` outro cliente; `404` destino não configurado; `503` sistema externo indisponível.

### GET /v1/clientes/{clienteId}/notificacoes

- **Descrição:** lista notificações relevantes associadas à conta do cliente.
- **Requisito de origem:** RF025.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Parâmetros de query:** `lida` (opcional), `page` (opcional), `limit` (opcional).
- **Exemplo de resposta (200):**

```json
{
  "data": [
    {
      "id": "notificacao_01",
      "tipo": "ativacao_atualizada",
      "titulo": "Sua ativação avançou",
      "mensagem": "A etapa de validação foi concluída.",
      "lida": false,
      "criada_em": "2026-08-17T08:45:00-03:00"
    }
  ],
  "nao_lidas": 1,
  "page": 1,
  "limit": 20,
  "total": 1
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `503` notificações indisponíveis.

### GET /v1/clientes/{clienteId}/notificacoes/{notificacaoId}

- **Descrição:** retorna uma notificação específica vinculada ao cliente.
- **Requisito de origem:** RF025.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Exemplo de resposta (200):**

```json
{
  "id": "notificacao_01",
  "tipo": "ativacao_atualizada",
  "titulo": "Sua ativação avançou",
  "mensagem": "A etapa de validação foi concluída.",
  "lida": false,
  "criada_em": "2026-08-17T08:45:00-03:00"
}
```

- **Status codes:** `200` sucesso; `401` não autenticado; `403` outro cliente; `404` notificação não encontrada.

### PATCH /v1/clientes/{clienteId}/notificacoes/{notificacaoId}

- **Descrição:** altera apenas o estado de leitura da notificação.
- **Requisito de origem:** RF025.
- **Autenticação:** obrigatória e restrita ao cliente vinculado.
- **Corpo da requisição:**

```json
{
  "lida": true
}
```

- **Exemplo de resposta (200):**

```json
{
  "id": "notificacao_01",
  "lida": true,
  "lida_em": "2026-08-17T10:50:00-03:00"
}
```

- **Status codes:** `200` atualizada; `400` campo inválido; `401` não autenticado; `403` outro cliente; `404` notificação não encontrada.

## Requisitos funcionais sem endpoint próprio

| Requisito | Motivo |
| --- | --- |
| RF001 | A consulta de páginas institucionais públicas pode ser atendida pelo próprio frontend e por arquivos estáticos. |
| RF002 | O direcionamento dos CTAs e do item Entrar é navegação do frontend para a tela de Login/Cadastro. |
| RF014 | A linha do tempo institucional é conteúdo estático no escopo atual; só exigirá endpoint se houver requisito de atualização dinâmica ou CMS. |

Os requisitos não funcionais RNF001 a RNF012 não originam endpoints isolados. Eles restringem todos os contratos aplicáveis, especialmente segurança, autorização, LGPD, consistência, tratamento de erros, referência temporal, responsividade, acessibilidade, versionamento, validação e metas operacionais.

## Observações e decisões pendentes

- Os endpoints de conta e sessão representam o comportamento necessário, mas credenciais, recuperação de acesso, política de senha, bloqueio, expiração e tecnologia de sessão serão definidos na etapa de autenticação e autorização.
- O corpo de `POST /v1/contas` é provisório porque a política de primeiro acesso e as chaves de associação com o cliente ainda não foram informadas pela Bulbe.
- A Bulbe deve confirmar se dados monetários por usina e totais podem ser públicos. Se não puderem, esses endpoints exigirão autenticação ou retornarão apenas dados autorizados.
- Competência, fórmula monetária, arredondamento, conjunto de usinas e frequência de atualização ainda precisam ser validados.
- Os estados e a ordem oficial das etapas de ativação e de repasse devem vir das fontes corporativas, não do simulador do frontend.
- Preferências de atualização e notificações são endpoints condicionais aos RF020 e RF025 permanecerem no escopo.
- O endereço e o mecanismo seguro de acesso ao histórico externo de faturas devem ser fornecidos pela Bulbe.
- Não foram criados endpoints administrativos de escrita para usinas, depoimentos, ativações, faturas ou repasses porque não há ator Administrador nem requisito de CRUD correspondente.

## Próximos passos

Este documento deverá ser formalizado em OpenAPI/Swagger em `docs/api/openapi.yaml`, validado com a Bulbe e usado como base para a modelagem dos casos de uso da API.
