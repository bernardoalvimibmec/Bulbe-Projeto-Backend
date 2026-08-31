# Documento de Requisitos Técnicos — Bulbe

## Identificação

- **Projeto:** Bulbe — evolução do frontend e implementação do backend
- **Empresa parceira:** Bulbe Energia
- **Equipe:** Squad Master
- **Integrantes:** Bernardo A. Alvim, Felipe Nunes, Caio Freitas, Luca Bellei e Vinicius Bianchetti.
- **Data:** 12/08/2026
- **Sprint / Etapa:** Sprint 1 — Elicitação

## Como este documento foi construído

Os requisitos abaixo foram levantados a partir da análise das funcionalidades implementadas no frontend do Projeto Ciência de Dados I. Para cada tela ou ação existente, a equipe identificou o que o backend ou o sistema precisa oferecer para sustentá-la, classificando cada requisito como funcional (RF) ou não funcional (RNF).

## Tabela de Requisitos

| ID | Funcionalidade do Frontend (Projeto I) | Requisito Técnico Derivado (Backend/Sistema) | Tipo | Prioridade |
| --- | --- | --- | --- | --- |
| RF001 | Área pública navegável | O backend deve disponibilizar dados institucionais públicos que façam parte da API sem exigir autenticação. | RF | Média |
| RF002 | CTAs públicos e item Entrar | O backend deve disponibilizar endpoints públicos para iniciar o cadastro ou primeiro acesso e a autenticação de clientes. | RF | Alta |
| RF003 | Formulário de login | O backend deve validar as credenciais de uma conta válida e criar uma sessão autenticada conforme as regras definidas pela Bulbe. | RF | Alta |
| RF004 | Cadastro ou primeiro acesso | O backend deve cadastrar ou iniciar o primeiro acesso de um cliente elegível conforme a política aprovada pela Bulbe. | RF | Alta |
| RF005 | Item Sair nos menus | O backend deve invalidar a sessão autenticada atual do cliente. | RF | Alta |
| RF006 | Área individual do cliente | O backend deve exigir autenticação e autorização para consultas de ativação, faturas, pagamentos, repasses, notificações e demais dados pessoais do cliente. | RF | Alta |
| RF007 | Associação da conta digital | O backend deve vincular a conta autenticada ao cadastro correto do cliente Bulbe antes de retornar dados individuais. | RF | Alta |
| RF008 | Cards de usinas | O backend deve obter da fonte de dados da Bulbe as usinas atualmente ativas e retornar sua identificação, localização e região aplicável. | RF | Alta |
| RF009 | Valor em reais por usina | O backend deve obter da fonte de dados da Bulbe o valor real dos créditos de energia gerados por cada usina no período solicitado. | RF | Alta |
| RF010 | Card Total gerado | O backend deve calcular e retornar o total monetário dos créditos das usinas incluídas, usando dados reais e o mesmo período de referência. | RF | Alta |
| RF011 | Botão Ver todas as usinas | O backend deve retornar a listagem paginada de usinas da Bulbe e os dados de geração ou créditos definidos para cada uma. | RF | Média |
| RF012 | Cards de histórias de clientes | O backend deve obter e retornar depoimentos públicos válidos e autorizados pela Bulbe, sem depender de conteúdo fixado no frontend. | RF | Média |
| RF013 | Campos dos depoimentos | O backend deve retornar, somente quando autorizados e disponíveis, os dados públicos do depoimento: identificação, localidade, avaliação, economia mensal, dias para ativação, desconto, tempo de conta ativa e texto. | RF | Média |
| RF014 | Linha do tempo institucional | O backend deve disponibilizar, quando esse conteúdo fizer parte da API, as informações das etapas gerais de homologação. | RF | Baixa |
| RF015 | Progresso da ativação | O backend deve consultar na fonte oficial a situação real da ativação do cliente autenticado e autorizado. | RF | Alta |
| RF016 | Etapas concluídas da ativação | O backend deve retornar as etapas da ativação do cliente que foram efetivamente concluídas. | RF | Alta |
| RF017 | Etapa atual da ativação | O backend deve retornar a etapa atual da ativação do cliente e o seu estado. | RF | Alta |
| RF018 | Etapas pendentes da ativação | O backend deve retornar as etapas de ativação do cliente que permanecem pendentes. | RF | Alta |
| RF019 | Representação coerente do progresso | O backend deve fornecer um estado de ativação consistente, com percentual, etapa atual, etapas concluídas e pendentes como fonte de verdade. | RF | Alta |
| RF020 | CTA Receber atualizações | O backend deve registrar e atualizar a preferência do cliente para receber atualizações da ativação pelos canais aprovados. | RF | Média |
| RF021 | Dados da fatura | O backend deve obter na fonte oficial e retornar os dados da fatura do cliente autenticado, incluindo valor, competência e identificador exibível. | RF | Alta |
| RF022 | Situação do pagamento | O backend deve obter na fonte oficial e retornar a situação real do pagamento da fatura, a forma de pagamento e a data e hora correspondentes, quando disponíveis. | RF | Alta |
| RF023 | Linha do tempo de repasse | O backend deve obter na fonte oficial e retornar o estado das etapas de repasse relacionadas à CEMIG, com estados, datas, previsões e mensagens válidas. | RF | Alta |
| RF024 | Histórico externo de faturas | O backend deve validar sessão e vínculo do cliente e retornar um redirecionamento seguro para o sistema externo de histórico de faturas da Bulbe. | RF | Média |
| RF025 | Notificações da conta | O backend deve retornar as notificações relevantes associadas à conta do cliente autenticado e autorizado, caso esse recurso permaneça no escopo. | RF | Baixa |
| RNF001 | Login e dados pessoais | O sistema deve proteger credenciais e dados pessoais em trânsito e em repouso por mecanismos de segurança compatíveis com o risco; os detalhes técnicos serão definidos na arquitetura. | RNF | Alta |
| RNF002 | Senhas | O sistema não deve armazenar senhas em texto puro; deve usar mecanismo reconhecido e aprovado de derivação ou hash de senha com salt. | RNF | Alta |
| RNF003 | Área individual do cliente | O sistema deve aplicar autenticação e autorização no backend, sem confiar apenas na ocultação de elementos ou na navegação do frontend. | RNF | Alta |
| RNF004 | Depoimentos e dados de clientes | O tratamento e a exposição de dados pessoais devem respeitar finalidade, minimização, consentimento ou outra base legal e as demais obrigações aplicáveis da LGPD. | RNF | Alta |
| RNF005 | Estados de ativação, pagamento e repasse | Os dados retornados pela API devem preservar integridade e consistência entre fonte, cliente, competência, etapa e horário de atualização. | RNF | Alta |
| RNF006 | Dados externos e falhas | A API deve retornar indisponibilidade, ausência de dados ou falha de atualização de forma explícita, sem retornar valores simulados como reais e permitindo nova tentativa quando aplicável. | RNF | Alta |
| RNF007 | Atualidade dos dados dinâmicos | O sistema deve registrar ou disponibilizar a referência temporal da informação quando sua atualidade for relevante; a frequência e a tolerância de defasagem devem ser validadas. | RNF | Média |
| RNF008 | Compatibilidade de consumo | A API deve preservar a compatibilidade do contrato versionado com os clientes suportados, inclusive em conexões de dispositivos móveis. | RNF | Média |
| RNF009 | Mensagens de erro | A API deve retornar mensagens de erro compreensíveis, estruturadas e consistentes para permitir tratamento adequado pelos clientes consumidores. | RNF | Média |
| RNF010 | Comunicação entre frontend e backend | A troca de dados entre frontend e backend deve usar contrato versionado, validação de entradas e saídas e tratamento consistente de respostas; os endpoints serão definidos em etapa posterior. | RNF | Média |
| RNF011 | Desempenho e disponibilidade | Metas mensuráveis de tempo de resposta, disponibilidade e capacidade devem ser definidas antes da implementação; nenhum valor é presumido neste documento. | RNF | Média |
| RNF012 | Compatibilidade de integração | A API deve manter compatibilidade com os protocolos, formatos e versões aprovados pela equipe, sem depender de caminhos absolutos locais. | RNF | Baixa |

## Legenda

- **RF — Requisito Funcional:** descreve o que o sistema deve fazer, uma função ou ação esperada.
- **RNF — Requisito Não Funcional:** descreve como o sistema deve se comportar, uma qualidade ou restrição técnica.
- **Prioridade Alta:** essencial para o funcionamento básico do sistema.
- **Prioridade Média:** importante, mas não bloqueia a primeira entrega.
- **Prioridade Baixa:** desejável e pode ficar para uma sprint futura.

## Observações

- A política de cadastro ou primeiro acesso, as credenciais aceitas e a forma de associação da conta digital ao cliente ainda dependem de validação com a Bulbe.
- A fonte oficial, a frequência de atualização e a tolerância de defasagem dos dados de usinas, créditos, ativação, faturas, pagamentos e repasses ainda devem ser definidas.
- O canal de atualizações, as notificações da conta e os respectivos consentimentos permanecem sujeitos à confirmação de escopo.
- As metas mensuráveis de desempenho, disponibilidade, capacidade, acessibilidade e compatibilidade serão definidas antes da implementação.

## Próximos passos

Estes requisitos serão utilizados na Aula 04 (Engenharia de Requisitos para APIs) para desenhar o contrato de endpoints da API.
