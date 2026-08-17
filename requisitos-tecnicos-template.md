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
| RF001 | Área pública navegável | O sistema deve permitir a consulta das telas institucionais sem exigir autenticação. | RF | Média |
| RF002 | CTAs públicos e item Entrar | O sistema deve direcionar os CTAs “Quero meus créditos” e o item “Entrar” para a tela de Login/Cadastro. | RF | Alta |
| RF003 | Formulário de login | O sistema deve permitir que uma conta válida inicie uma sessão autenticada usando as credenciais definidas pela Bulbe. | RF | Alta |
| RF004 | Cadastro ou primeiro acesso | O sistema deve permitir iniciar o fluxo de cadastro ou primeiro acesso conforme a política de elegibilidade aprovada pela Bulbe. | RF | Alta |
| RF005 | Item Sair nos menus | O sistema deve permitir que o cliente encerre a sessão autenticada. | RF | Alta |
| RF006 | Área individual do cliente | O sistema deve restringir a consulta de ativação, fatura, pagamento, repasse e demais dados pessoais ao cliente autenticado e autorizado. | RF | Alta |
| RF007 | Associação da conta digital | O sistema deve associar a conta autenticada ao cadastro correto do cliente Bulbe antes de disponibilizar dados individuais. | RF | Alta |
| RF008 | Cards de usinas | O sistema deve obter e apresentar a listagem de usinas consideradas ativas pela Bulbe, incluindo identificação e localização ou região aplicável. | RF | Alta |
| RF009 | Valor em reais por usina | O sistema deve obter e apresentar, para cada usina, o valor real correspondente aos créditos de energia gerados no período aplicável. | RF | Alta |
| RF010 | Card Total gerado | O sistema deve calcular e apresentar o total monetário dos créditos gerados pelas usinas incluídas, usando os mesmos dados reais e o mesmo período de referência. | RF | Alta |
| RF011 | Botão Ver todas as usinas | O sistema deve permitir consultar a listagem completa de usinas da Bulbe e os dados de geração ou crédito definidos para cada uma. | RF | Média |
| RF012 | Cards de histórias de clientes | O sistema deve obter e apresentar depoimentos válidos disponibilizados pela Bulbe, sem depender de inserção manual no HTML ou JavaScript. | RF | Média |
| RF013 | Campos dos depoimentos | O sistema deve apresentar, quando autorizados e disponíveis, identificação pública do cliente, localidade, avaliação, economia mensal, dias para ativação, percentual de desconto, tempo de conta ativa e depoimento. | RF | Média |
| RF014 | Linha do tempo institucional | O sistema deve permitir consultar o conteúdo explicativo das etapas gerais de homologação. | RF | Baixa |
| RF015 | Progresso da ativação | O sistema deve consultar a situação real da ativação do cliente autenticado. | RF | Alta |
| RF016 | Etapas concluídas da ativação | O sistema deve identificar e informar quais etapas da ativação do cliente foram efetivamente concluídas. | RF | Alta |
| RF017 | Etapa atual da ativação | O sistema deve identificar e informar a etapa atual da ativação do cliente e seu estado. | RF | Alta |
| RF018 | Etapas pendentes da ativação | O sistema deve identificar e informar as etapas da ativação que ainda estão pendentes. | RF | Alta |
| RF019 | Representação coerente do progresso | O sistema deve fornecer um estado coerente da ativação para que a interface represente percentual, etapa e indicadores sem usar controles manuais como fonte de verdade. | RF | Alta |
| RF020 | CTA Receber atualizações | O sistema deve permitir ao cliente solicitar ou configurar o recebimento de atualizações da ativação pelo canal aprovado. | RF | Média |
| RF021 | Dados da fatura | O sistema deve obter e apresentar os dados da fatura aplicável ao cliente, incluindo valor, competência ou referência e identificador exibível. | RF | Alta |
| RF022 | Situação do pagamento | O sistema deve obter e apresentar a situação real do pagamento da fatura, a forma de pagamento, quando aplicável, e a data e hora correspondentes. | RF | Alta |
| RF023 | Linha do tempo de repasse | O sistema deve obter e apresentar o estado real das etapas de repasse relacionadas à CEMIG, incluindo estados, datas, previsões e mensagens somente quando disponíveis e válidos. | RF | Alta |
| RF024 | Histórico externo de faturas | O sistema deve redirecionar o cliente para o sistema externo de histórico de faturas da Bulbe, sem implementar o histórico completo neste projeto. | RF | Média |
| RF025 | Notificações da conta | O sistema deve permitir ao cliente consultar notificações relevantes associadas à sua conta, caso esse recurso seja mantido no escopo. | RF | Baixa |
| RNF001 | Login e dados pessoais | O sistema deve proteger credenciais e dados pessoais em trânsito e em repouso por mecanismos de segurança compatíveis com o risco; os detalhes técnicos serão definidos na arquitetura. | RNF | Alta |
| RNF002 | Senhas | O sistema não deve armazenar senhas em texto puro; deve usar mecanismo reconhecido e aprovado de derivação ou hash de senha com salt. | RNF | Alta |
| RNF003 | Área individual do cliente | O sistema deve aplicar autenticação e autorização no backend, sem confiar apenas na ocultação de elementos ou na navegação do frontend. | RNF | Alta |
| RNF004 | Depoimentos e dados de clientes | O tratamento e a exposição de dados pessoais devem respeitar finalidade, minimização, consentimento ou outra base legal e as demais obrigações aplicáveis da LGPD. | RNF | Alta |
| RNF005 | Estados de ativação, pagamento e repasse | Os dados apresentados devem preservar integridade e consistência entre fonte, cliente, competência, etapa e horário de atualização. | RNF | Alta |
| RNF006 | Dados externos e falhas | O sistema deve informar indisponibilidade, ausência de dados ou falha de atualização sem apresentar valores simulados como reais, oferecendo nova tentativa quando aplicável. | RNF | Alta |
| RNF007 | Atualidade dos dados dinâmicos | O sistema deve registrar ou disponibilizar a referência temporal da informação quando sua atualidade for relevante; a frequência e a tolerância de defasagem devem ser validadas. | RNF | Média |
| RNF008 | Interfaces responsivas | A evolução do sistema deve preservar o comportamento responsivo nas larguras suportadas pelo frontend e em dispositivos móveis. | RNF | Média |
| RNF009 | Acessibilidade e usabilidade | As interfaces e mensagens de erro devem ser compreensíveis, navegáveis por teclado e compatíveis com tecnologias assistivas, de acordo com critérios a definir. | RNF | Média |
| RNF010 | Comunicação entre frontend e backend | A troca de dados entre frontend e backend deve usar contrato versionado, validação de entradas e saídas e tratamento consistente de respostas; os endpoints serão definidos em etapa posterior. | RNF | Média |
| RNF011 | Desempenho e disponibilidade | Metas mensuráveis de tempo de resposta, disponibilidade e capacidade devem ser definidas antes da implementação; nenhum valor é presumido neste documento. | RNF | Média |
| RNF012 | Compatibilidade de navegação | O sistema deve manter compatibilidade com os navegadores e versões aprovados pela equipe, ainda a definir, sem depender de caminhos absolutos locais. | RNF | Baixa |

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
