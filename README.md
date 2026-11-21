# Prospecção por Prompt

**Seu time prospectando apenas empresas prontas para comprar.**

Um agente no seu Claude acha as empresas brasileiras com sinais de compra pro seu produto e diz por que cada uma está pronta pra comprar esta semana. Tudo isso aumenta a sua taxa de resposta e as reuniões marcadas.

Grátis, roda no seu Claude Code. Você cola um bloco de instalação e o Claude:

1. lê o site da sua empresa e decide o seu ICP e os sinais de compra mais fortes pro seu produto (você só confirma);
2. busca as empresas com motivo pra comprar agora, confere cada fonte e dá uma nota de 0 a 100;
3. entrega uma planilha pronta, com a aba "comece aqui", o mais rápido possível;
4. se você quiser, afina o alvo com a sua opinião sobre a lista;
5. se você quiser, deixa uma rotina diária: todo dia, as empresas com os sinais mais frescos numa planilha nova.

Só fontes públicas e só dados de empresa. Nada pra assinar, nenhuma chave de API.

## Pra quem é

- **Use se:**
  - você tem time de vendas que prospecta, ou prospecta você mesmo como fundador;
  - vende B2B no Brasil;
  - o seu time perde horas pesquisando pra quem ligar.
- **Não use se:**
  - você vende pra pessoa física;
  - quer telefone e e-mail prontos (isso é a [fulgurite](https://fulgurite.io/?utm_source=prospeccao-por-prompt&utm_medium=github&utm_campaign=prospeccao-por-prompt), não o agente);
  - não tem plano pago do Claude.

## Instalação

Veja **[INSTALAR.md](INSTALAR.md)**: 3 passos, poucos minutos, sem terminal.

Usa o ChatGPT? É só seguir o **[INSTALAR-CHATGPT.md](INSTALAR-CHATGPT.md)**.

## O que você recebe

Uma planilha (`saida/lista-AAAA-MM-DD.xlsx`) com 4 abas:

| Aba | O que tem |
|---|---|
| **Comece aqui** | como usar a lista na segunda-feira e o próximo passo |
| **Contas** | uma linha por empresa: nome, site, faixa A/B/C, nota, por que agora, até 3 sinais com data e link, vagas comerciais abertas, ferramentas citadas, notícia recente, o que vende, setor (CNAE), porte estimado, cidade/UF, CNPJ, situação cadastral, ano de abertura, área e cargo provável de quem decide, link pra achar o e-mail e o celular de quem decide na fulgurite, encaixe com o ICP, alertas, o que foi observado ou deduzido, data da verificação, próximo passo |
| **Descartadas** | as empresas que ficaram de fora e o motivo (concorrente, CNPJ baixado, já está no seu CRM…) |
| **Sinais e critérios** | o ICP, os sinais e as buscas usadas na rodada |

## Comandos

Você não precisa decorar nada: o Claude conduz. Se quiser, os comandos são:

| Comando | O que faz |
|---|---|
| `/comecar` | lê o seu site, decide o ICP e os sinais e já parte pra busca |
| `/lista` | busca, confere e pontua as contas da rodada |
| `/planilha` | gera a planilha final e oferece a rotina diária |
| `/calibrar` | ajuste fino depois da primeira lista: você diz quais não serviriam e, se quiser, sobe o seu CRM |
| `/sinais` | troca ou inclui sinais de compra |
| `/atualizar` | as contas novas, sem repetir as antigas (também roda sozinho na rotina diária) |

## Como ele decide

- **Sinais:** vaga aberta ligada ao seu produto, vaga pra estruturar a área do zero, vagas crescendo de uma rodada pra outra, contrato público ganho, ferramentas instaladas no site, nova liderança na área que compra, expansão, investimento. O agente escolhe os mais fortes pro seu caso. Sinais de tipos diferentes na mesma empresa somam. Detalhes em [referencias/sinais.md](referencias/sinais.md).
- **Checagem:** toda conta passa por 9 checagens antes de entrar. Fonte aberta e lida, com data. Comprador, não concorrente. CNPJ ativo. Fora do seu CRM. Sem duplicada. Veja [referencias/nota-e-checagem.md](referencias/nota-e-checagem.md).
- **Nota:** fit com o ICP (35%), força do sinal (30%), momento (20%), qualidade da evidência (15%).

## Fontes e privacidade

- **Fontes:** vagas nos portais públicos da Gupy e do Vagas.com e em páginas de carreira; contratos no Portal Nacional de Contratações Públicas (PNCP); o código público da home das empresas; notícias e sites das empresas pela busca na web do Claude; consulta pública de CNPJ (BrasilAPI e Minha Receita).
- **O que o agente nunca guarda nem mostra:** nome, e-mail, telefone ou perfil de pessoas, nem os sócios do CNPJ.
- **O que o agente nunca faz:** acessar páginas com login, paywall ou bloqueio, nem abrir páginas do LinkedIn.
- **Onde ficam os seus dados:** na pasta `dados/`, no seu computador. Nada é enviado pra fulgurite.

As contas são potenciais clientes com base em sinais públicos. Nenhuma delas demonstrou interesse no seu produto. Confira antes de abordar.

## E depois da lista?

O agente para no cargo provável de quem decide, de propósito: e-mail, celular e LinkedIn de quem decide, com qualidade, não ficam abertos na internet. Só existem em softwares feitos pra isso, como a fulgurite. Pra achar a pessoa e o contato de cada conta, suba a aba Contas na **fulgurite** (só precisa de nome e site): [50 créditos grátis por 7 dias, sem cartão](https://fulgurite.io/?utm_source=prospeccao-por-prompt&utm_medium=github&utm_campaign=prospeccao-por-prompt).

## Estrutura

```
CLAUDE.md                 instruções do agente (orquestração e regras)
AGENTS.md                 as mesmas instruções, na versão pro ChatGPT
INSTALAR.md               o bloco pra colar no Claude Code
.claude/skills/           os 6 comandos
.agents/skills/           os mesmos comandos, na versão pro ChatGPT
referencias/              sinais, fontes, cargos de quem decide, nota e checagem
scripts/                  Python, sem dependências (vagas, licitações, sites, CNPJ, filtro, planilha, rotina diária, ambiente)
exemplos/                 dados fictícios pra testar a planilha
dados/                    os seus dados (criado na primeira rodada; não vai pro git)
saida/                    as planilhas geradas (não vai pro git)
```

Pra testar a planilha sem rodar uma busca: `python scripts/planilha.py --exemplo`.

## Licença

MIT. Feito pela [fulgurite](https://fulgurite.io).
