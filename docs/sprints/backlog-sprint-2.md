# Backlog da Sprint 2 — API Bulbe

- **Equipe:** Squad Master
- **Sprint:** 2, de 07/10/2026 a 21/10/2026
- **Objetivo da sprint:** API respondendo de ponta a ponta com dados em memória, nas quatro camadas (Controller, Service, Repository, Domínio), com regras de negócio nos serviços e testes passando com pytest.
- **Review:** 26/10/2026, com a API rodando ao vivo.
- **Estimativa:** story points na escala de Fibonacci (1, 2, 3, 5, 8, 13).
- **Contrato:** [`docs/api/openapi.yaml`](../api/openapi.yaml) e [`docs/requisitos/lista-endpoints.md`](../requisitos/lista-endpoints.md).

> **Responsáveis:** a coluna "Responsável" é uma **proposta** para dividir a carga de forma equilibrada por área. A equipe deve confirmar ou trocar antes do Planning e registrar no board.

## Visão geral priorizada

A ordem da tabela é a ordem de prioridade. Itens técnicos (TEC) vêm primeiro porque desbloqueiam todos os outros.

| ID | Item | Endpoint(s) | Requisitos | Pontos | Prioridade | Sprint | Responsável (proposta) | Issue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEC-01 | Estrutura base, injeção de dependência e erro padronizado | todos | RNF009, RNF010 | 3 | Alta | 2 | Bernardo | #17 |
| TEC-02 | Repositórios em memória com dados de exemplo da Bulbe | todos | RNF006 | 3 | Alta | 2 | Bernardo | #18 |
| TEC-03 | Base de testes (pytest, TestClient, fixtures) | todos | — | 2 | Alta | 2 | Bernardo | #19 |
| US01 | Autenticar cliente | `POST /v1/sessoes` | RF003, RNF002 | 8 | Alta | 2 | Caio | #7 |
| US02 | Encerrar sessão | `DELETE /v1/sessoes/atual` | RF005 | 2 | Alta | 2 | Caio | #8 |
| US04 | Proteger dados individuais | `GET /v1/clientes/{clienteId}` e regra de vínculo | RF006, RNF003 | 5 | Alta | 2 | Bernardo | #10 |
| US06 | Listar usinas ativas | `GET /v1/usinas`, `GET /v1/usinas/{usinaId}` | RF008, RF011 | 3 | Alta | 2 | Felipe | #12 |
| US07 | Consultar crédito gerado por usina | `GET /v1/usinas/{usinaId}/creditos` | RF009 | 3 | Alta | 2 | Felipe | #13 |
| US08 | Consultar total gerado | `GET /v1/creditos-usinas/resumo` | RF010 | 5 | Alta | 2 | Felipe | #14 |
| US09 | Consultar progresso da ativação | `GET /v1/clientes/{clienteId}/ativacao`, `.../ativacao/etapas` | RF015–RF019 | 5 | Alta | 2 | Vinicius | #15 |
| US10 | Consultar fatura e situação do pagamento | `GET .../faturas`, `.../faturas/{faturaId}`, `.../pagamento` | RF021, RF022 | 5 | Alta | 2 | Vinicius | #16 |
| US13 | Acompanhar o repasse à CEMIG | `GET .../faturas/{faturaId}/repasse` | RF023 | 3 | Alta | 2 | Vinicius | #22 |
| US03 | Iniciar cadastro / primeiro acesso | `POST /v1/contas` | RF004 | 8 | Alta | 2 | Luca | #9 |
| US05 | Associar conta digital ao cadastro Bulbe | `POST /v1/contas` (vínculo) | RF007 | 5 | Alta | 2 | Luca | #11 |
| US11 | Listar depoimentos públicos autorizados | `GET /v1/depoimentos`, `GET /v1/depoimentos/{depoimentoId}` | RF012, RF013, RNF004 | 3 | Média | 2 | Felipe | #20 |
| US14 | Acessar histórico externo de faturas | `GET .../historico-faturas-externo` | RF024 | 2 | Média | 2 | Caio | #23 |
| US12 | Configurar atualizações da ativação | `PUT .../preferencias-notificacao/ativacao` | RF020 | 3 | Média | 2 (se houver folga) | Vinicius | #21 |
| US15 | Consultar e marcar notificações | `GET/PATCH .../notificacoes...` | RF025 | 5 | Baixa | Backlog | a definir | #24 |

### Carga por pessoa (proposta)

| Responsável | Itens | Pontos |
| --- | --- | --- |
| Bernardo | TEC-01, TEC-02, TEC-03, US04 | 13 |
| Caio | US01, US02, US14 | 12 |
| Felipe | US06, US07, US08, US11 | 14 |
| Luca | US03, US05 | 13 |
| Vinicius | US09, US10, US13 (+ US12 se houver folga) | 13 (+3) |
| **Compromisso da sprint** | | **65** |

US15 fica fora da Sprint 2: o RF025 tem prioridade baixa e depende de confirmação de escopo com a Bulbe.

### Dependências

- **TEC-01** desbloqueia todos os itens. **TEC-02** e **TEC-03** podem andar em paralelo com as stories públicas.
- **US01** (sessão) desbloqueia **US02** e **US04**.
- **US04** (regra de vínculo) desbloqueia todas as rotas `/v1/clientes/{clienteId}/...`: US09, US10, US12, US13, US14, US15.
- **US06**, **US07**, **US08** e **US11** são públicas e não dependem de autenticação. Podem começar no primeiro dia.

## Regras de negócio por item

O professor pediu entidades com comportamento ("nada de classes só com atributos") e regras nos serviços. Cada story abaixo aponta a regra que precisa morar no Service ou na entidade de domínio, e não no Controller.

| Item | Regra de negócio | Onde mora |
| --- | --- | --- |
| US01 | Senha conferida por hash com salt; conta precisa estar ativa; bloqueio temporário após N tentativas falhas | `Conta.validar_senha()`, `Conta.esta_ativa()`, `SessaoService` |
| US02 | Sessão já invalidada não pode ser reutilizada | `Sessao.invalidar()`, `Sessao.esta_valida()` |
| US04 | O `clienteId` da URL precisa ser o cliente vinculado à sessão; caso contrário 403, mesmo que o cliente exista | `AutorizacaoService` |
| US03 / US05 | Só cliente elegível ganha conta; uma conta por cliente (409); vínculo não confirmado resulta em 422 | `ContaService` |
| US06 | Por padrão, só usinas com status `ativa` aparecem para o público | `UsinaService` |
| US07 | Competência obrigatória no formato `AAAA-MM`; período sem dado retorna 404 explícito, nunca zero simulado | `CreditoService` |
| US08 | Total = soma dos créditos das usinas do critério na **mesma** competência; informa quantas usinas entraram no cálculo | `CreditoService.resumo()` |
| US09 | Percentual = etapas concluídas ÷ total de etapas; só uma etapa `atual`; etapas sempre na ordem oficial | `Ativacao.calcular_percentual()`, `Ativacao.obter_etapa_atual()` |
| US10 | Fatura só é visível para o cliente dono; pagamento ausente é diferente de pagamento recusado | `FaturaService` |
| US11 | Só depoimentos com `publicacao_autorizada` aparecem; dados pessoais minimizados (LGPD) | `Depoimento.pode_ser_publicado()` |
| US12 | Canal precisa ser suportado; operação idempotente (PUT repetido não duplica) | `PreferenciaNotificacao.alterar()` |
| US13 | Etapas do repasse em ordem; previsão só para etapas não concluídas | `Repasse.obter_etapa_atual()` |
| US14 | Só redireciona para destino HTTPS aprovado; destino ausente é 404 | `HistoricoFaturasService` |

## Detalhamento e critérios de aceite

Os critérios descrevem o comportamento da API. Todos os itens também precisam cumprir a [Definição de Pronto](#definição-de-pronto).

### TEC-01 — Estrutura base, injeção de dependência e erro padronizado (3 pts) · issue #17

Como equipe de desenvolvimento, queremos a estrutura `src/` com as quatro camadas e um formato de erro único, para que cada story só precise adicionar a sua parte.

- `src/main.py` sobe com `uvicorn src.main:app --reload` e expõe `/docs`.
- Serviços recebem repositórios pelo construtor; `main.py` é o único lugar que decide qual implementação de repositório usar.
- Erros de negócio, de validação do Pydantic e de rota inexistente saem todos no formato do contrato: `codigo`, `mensagem`, `detalhes`, `request_id`.

### TEC-02 — Repositórios em memória com dados de exemplo (3 pts) · issue #18

Como equipe, queremos repositórios em memória com dados de exemplo coerentes, para demonstrar a API na Review II sem depender das fontes oficiais.

- Cada repositório tem uma interface (classe abstrata) e uma implementação `InMemory...`.
- Dados de exemplo com pelo menos: 4 usinas (uma inativa), créditos em duas competências, 2 clientes com conta, ativação em andamento, faturas paga e em aberto, repasse em andamento, 3 depoimentos (um não autorizado).
- Dados de exemplo ficam separados do código de produção, para serem trocados pelo seed do banco na Sprint 3.

### TEC-03 — Base de testes (2 pts) · issue #19

Como equipe, queremos uma base de testes pronta, para que cada story já nasça com testes.

- `pytest` roda a partir da raiz com um comando.
- Fixture de `TestClient` e fixtures de repositórios em memória limpos a cada teste.
- Teste de fumaça: `GET /` responde 200 e `/docs` está disponível.

### US01 — Autenticar cliente (8 pts) · issue #7

Como aplicação cliente, quero enviar credenciais válidas e receber um token de sessão, para que o usuário acesse sua área individual.

- Credenciais válidas retornam **201** com `sessao_id`, `conta_id`, `cliente_id` e `expira_em`. A issue #7 diz 200; o contrato diz 201 porque uma sessão é criada. Ajustar a issue para 201.
- Credenciais inválidas retornam 401 sem revelar qual campo falhou.
- Senha nunca armazenada nem trafegada em texto puro: hash com salt.
- Tentativas repetidas são limitadas e retornam 429.

### US02 — Encerrar sessão (2 pts) · issue #8

Como aplicação cliente, quero encerrar a sessão atual, para que o token deixe de valer quando o usuário clicar em Sair.

- `DELETE /v1/sessoes/atual` com sessão válida retorna 204 sem corpo.
- A mesma sessão, usada depois, retorna 401.
- Sem sessão ou com sessão inválida retorna 401.

### US03 — Iniciar cadastro / primeiro acesso (8 pts) · issue #9

Como aplicação cliente, quero enviar os dados de primeiro acesso, para que um cliente Bulbe elegível crie sua conta digital.

- Dados válidos de cliente elegível retornam 201 com a conta criada.
- Campos ausentes ou malformados retornam 400 no formato de erro padrão.
- Cliente que já tem conta retorna 409.
- Cliente inelegível ou vínculo não confirmado retorna 422.
- Senha guardada apenas como hash.

### US04 — Proteger dados individuais (5 pts) · issue #10

Como aplicação cliente, quero que a API recuse acesso aos dados de outro cliente, para que cada pessoa veja apenas as próprias informações.

- `GET /v1/clientes/{clienteId}` do próprio cliente retorna 200 com os dados básicos.
- Sem sessão retorna 401.
- Sessão válida consultando outro `clienteId` retorna 403, mesmo que esse cliente exista.
- A regra é reaproveitada por todas as rotas `/v1/clientes/{clienteId}/...`.

### US05 — Associar conta digital ao cadastro Bulbe (5 pts) · issue #11

Como aplicação cliente, quero que a conta criada fique vinculada ao cadastro correto do cliente, para que os dados individuais exibidos sejam os dele.

- O vínculo usa o `identificador_cliente` informado no primeiro acesso.
- Conta sem vínculo confirmado não acessa nenhuma rota de cliente.
- A resposta de criação de conta traz o `cliente_id` vinculado.

### US06 — Listar usinas ativas (3 pts) · issue #12

Como aplicação frontend, quero listar as usinas da Bulbe, para exibir os cards de usinas na página pública.

- `GET /v1/usinas` retorna a lista paginada com `page`, `limit`, `total` e `atualizado_em`.
- Sem filtro, retorna só usinas ativas; `?status=` filtra pela situação.
- `GET /v1/usinas/{usinaId}` retorna a usina com região; id inexistente retorna 404.

### US07 — Consultar crédito gerado por usina (3 pts) · issue #13

Como aplicação frontend, quero consultar os créditos de uma usina em uma competência, para exibir o valor em reais no card da usina.

- Competência válida retorna 200 com `creditos` no formato `{ valor, moeda }`.
- Competência ausente ou fora do formato `AAAA-MM` retorna 400.
- Usina inexistente ou período sem dado retorna 404, nunca um valor zero inventado.

### US08 — Consultar total gerado (5 pts) · issue #14

Como aplicação frontend, quero o total de créditos de todas as usinas no período, para exibir o card "Total gerado".

- Retorna `total_creditos`, `quantidade_usinas` e o `criterio` usado.
- O total é a soma dos créditos das usinas do critério na mesma competência.
- Competência inválida retorna 400.
- Teste unitário do cálculo no Service, sem subir a API.

### US09 — Consultar progresso da ativação (5 pts) · issue #15

Como aplicação cliente, quero o progresso real da ativação, para exibir percentual, etapa atual, etapas concluídas e pendentes.

- `.../ativacao` retorna status, percentual e etapa atual.
- `.../ativacao/etapas` retorna as etapas na ordem oficial, cada uma como `concluida`, `atual` ou `pendente`.
- O percentual é calculado a partir das etapas concluídas e bate com a lista de etapas.
- Cliente sem ativação retorna 404; outro cliente retorna 403.

### US10 — Consultar fatura e situação do pagamento (5 pts) · issue #16

Como aplicação cliente, quero os dados da fatura vigente e o status do pagamento, para exibir valor, competência e situação ao cliente.

- Valor, competência e identificador exibível visíveis.
- Situação do pagamento com forma, data e hora quando houver.
- Período sem fatura retorna resposta explícita (lista vazia ou 404 na fatura específica), não um erro genérico.
- Outro cliente retorna 403.

### US11 — Listar depoimentos públicos autorizados (3 pts) · issue #20

Como aplicação frontend, quero listar os depoimentos autorizados, para exibir as histórias de clientes sem conteúdo fixo no HTML.

- `GET /v1/depoimentos` retorna só depoimentos com publicação autorizada.
- Depoimento não autorizado consultado por id retorna 404.
- Nenhum dado pessoal além dos campos públicos do contrato.

### US12 — Configurar atualizações da ativação (3 pts) · issue #21

Como aplicação cliente, quero salvar a preferência de receber atualizações da ativação, para que o botão "Receber atualizações" funcione de verdade.

- PUT com canal suportado retorna 200 com a preferência salva.
- Repetir o mesmo PUT não cria duplicidade.
- Canal não suportado retorna 422.

### US13 — Acompanhar o repasse à CEMIG (3 pts) · issue #22

Como aplicação cliente, quero as etapas do repasse de uma fatura, para exibir a linha do tempo do repasse à CEMIG.

- Retorna status geral e etapas em ordem, com `ocorrido_em`, `previsao` e `mensagem`.
- Fatura sem repasse retorna 404; outro cliente retorna 403.

### US14 — Acessar histórico externo de faturas (2 pts) · issue #23

Como aplicação cliente, quero ser redirecionada ao histórico oficial de faturas, para que o cliente consulte faturas antigas no sistema da Bulbe.

- Retorna 302 com cabeçalho `Location` apontando para uma URL HTTPS configurada.
- Destino não configurado retorna 404; outro cliente retorna 403.

### US15 — Consultar e marcar notificações (5 pts) · issue #24 · fora da Sprint 2

Como aplicação cliente, quero listar notificações e marcá-las como lidas, para exibir o contador de não lidas.

- Lista paginada com `nao_lidas`; filtro `?lida=`.
- PATCH altera só o estado de leitura e registra `lida_em`.

## Plano da sprint, encontro a encontro

Segue o roteiro sugerido pelo professor.

| Data | Foco | Itens |
| --- | --- | --- |
| 07/10 | Domínio: entidades com regras próprias | TEC-01; entidades de todas as stories |
| 14/10 | Repositórios em memória e serviços | TEC-02; serviços de cada story |
| 19/10 | Controllers e rotas do contrato, erro padronizado, `/docs` | rotas de cada story |
| 21/10 | Testes e ensaio da review | TEC-03 concluído; pytest verde; ensaio da demo do dia 26/10 |

## Definição de Pronto

Um item só vai para **Concluído** quando:

- está integrado na `main` por pull request revisado por um colega;
- `pytest` passa localmente antes de abrir o pull request;
- o endpoint aparece em `/docs` e o README está atualizado;
- rota, verbo, status code e formato de erro seguem o contrato em `docs/api/openapi.yaml`;
- o card está movido no board, com responsável e estimativa registrados.
