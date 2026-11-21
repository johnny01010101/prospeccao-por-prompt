# Prospecção por Prompt

**Seu time prospectando apenas empresas prontas para comprar.**

Um agente no seu Claude acha as empresas brasileiras com sinais de compra pro seu produto e diz por que cada uma está pronta pra comprar esta semana. Tudo isso aumenta a sua taxa de resposta e as reuniões marcadas.

Grátis, roda no seu Claude Code. Você cola um bloco de instalação e o Claude:

1. lê o site da sua empresa e propõe o seu ICP (você só confirma);
2. escolhe os sinais de compra do seu mercado: vagas abertas, nova liderança, expansão;
3. mostra 10 empresas pra você dizer "essa sim, essa não" e acertar o alvo;
4. busca as empresas com motivo pra comprar agora, confere cada fonte e dá uma nota de 0 a 100;
5. entrega uma planilha pronta, com a aba "comece aqui".

Só fontes públicas e só dados de empresa. Nada pra assinar, nenhuma chave de API.

## Pra quem é

- **Use se:**
  - você tem time de vendas que prospecta, ou prospecta você mesmo como fundador;
  - vende B2B no Brasil;
  - o seu time perde horas pesquisando pra quem ligar.
- **Não use se:**
  - você vende pra pessoa física;
  - quer telefone e e-mail prontos (isso é a [fulgurite](https://app.fulgurite.io/signup?utm_source=prospeccao-por-prompt&utm_medium=github&utm_campaign=prospeccao-por-prompt), não o agente);
  - não tem plano pago do Claude.

## Instalação

Veja **[INSTALAR.md](INSTALAR.md)**: 3 passos, poucos minutos, sem terminal.

## O que você recebe

Uma planilha (`saida/lista-AAAA-MM-DD.xlsx`) com 4 abas:

| Aba | O que tem |
|---|---|
| **Comece aqui** | como usar a lista na segunda-feira e o próximo passo |
| **Contas** | uma linha por empresa: nome, site, faixa A/B/C, nota, por que agora, até 3 sinais com data e link, vagas comerciais abertas, ferramentas citadas, notícia recente, o que vende, setor (CNAE), porte estimado, cidade/UF, CNPJ, situação cadastral, ano de abertura, área e cargo provável de quem decide, encaixe com o ICP, alertas, o que foi observado ou deduzido, data da verificação, próximo passo |
| **Descartadas** | as empresas que ficaram de fora e o motivo (concorrente, CNPJ baixado, já está no seu CRM…) |
| **Sinais e critérios** | o ICP, os sinais e as buscas usadas na rodada |

## Comandos

Você não precisa decorar nada: o Claude conduz. Se quiser, os comandos são:

| Comando | O que faz |
|---|---|
| `/comecar` | lê o seu site e monta o ICP; opcionalmente importa o seu CRM pra não repetir contas |
| `/sinais` | escolhe os sinais de compra do seu mercado |
| `/calibrar` | 10 empresas pra você dizer sim ou não |
| `/lista` | busca, confere e pontua as contas da rodada |
| `/planilha` | gera a planilha final |
| `/atualizar` | as contas novas da semana, sem repetir as antigas |

## Como ele decide

- **Sinais:** vaga aberta ligada ao seu produto, nova liderança na área que compra, expansão, investimento. Sinais de tipos diferentes na mesma empresa somam. Detalhes em [referencias/sinais.md](referencias/sinais.md).
- **Checagem:** toda conta passa por 9 checagens antes de entrar. Fonte aberta e lida, com data. Comprador, não concorrente. CNPJ ativo. Fora do seu CRM. Sem duplicada. Veja [referencias/nota-e-checagem.md](referencias/nota-e-checagem.md).
- **Nota:** fit com o ICP (35%), força do sinal (30%), momento (20%), qualidade da evidência (15%).

## Fontes e privacidade

- **Fontes:** vagas no portal público da Gupy e em páginas de carreira; notícias e sites das empresas pela busca na web do Claude; consulta pública de CNPJ (BrasilAPI e Minha Receita).
- **O que o agente nunca guarda nem mostra:** nome, e-mail, telefone ou perfil de pessoas, nem os sócios do CNPJ.
- **O que o agente nunca faz:** acessar páginas com login, paywall ou bloqueio, nem abrir páginas do LinkedIn.
- **Onde ficam os seus dados:** na pasta `dados/`, no seu computador. Nada é enviado pra fulgurite.

As contas são potenciais clientes com base em sinais públicos. Nenhuma delas demonstrou interesse no seu produto. Confira antes de abordar.

## E depois da lista?

O agente para no cargo provável de quem decide, de propósito. Pra achar a pessoa e o contato de cada conta, suba a aba Contas na **fulgurite** (só precisa de nome e site): [50 créditos grátis por 7 dias, sem cartão](https://app.fulgurite.io/signup?utm_source=prospeccao-por-prompt&utm_medium=github&utm_campaign=prospeccao-por-prompt).

## Estrutura

```
CLAUDE.md                 instruções do agente (orquestração e regras)
INSTALAR.md               o bloco pra colar no Claude Code
.claude/skills/           os 6 comandos
referencias/              sinais, fontes, cargos de quem decide, nota e checagem
scripts/                  Python, sem dependências (vagas, CNPJ, filtro, planilha, ambiente)
exemplos/                 dados fictícios pra testar a planilha
dados/                      os seus dados (criado na primeira rodada; não vai pro git)
saida/                    as planilhas geradas (não vai pro git)
```

Pra testar a planilha sem rodar uma busca: `python scripts/planilha.py --exemplo`.

## Licença

MIT. Feito pela [fulgurite](https://fulgurite.io).
