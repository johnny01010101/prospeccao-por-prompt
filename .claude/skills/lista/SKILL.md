---
name: lista
description: Monta a lista de empresas da rodada. Roda os scripts de sinais em paralelo (vagas, contratos públicos, ferramentas no site) e no máximo uma busca na web, confere cada fonte, checa CNPJ, descarta concorrentes, repetidas e anti-sinais, dá nota de 0 a 100, aponta o cargo provável de quem decide e grava dados/contas.csv. Use depois do /comecar, ou quando o usuário pedir uma lista nova.
---

# /lista: as contas da rodada

Objetivo: contas verificadas em `dados/contas.csv`, com as descartadas e o motivo em `dados/descartadas.csv`. Melhor 10 fortes que 30 genéricas.

Leia antes: `dados/icp.md`, `dados/sinais.md`, `referencias/nota-e-checagem.md`, `referencias/cargos-de-decisao.md` e, se precisar, `referencias/fontes.md`.

## Modos

| Modo | Quando | Meta | Limite de esforço |
|---|---|---|---|
| **Primeira lista** | logo depois do `/comecar` | de 10 a 15 contas | entregar a planilha o mais rápido possível: scripts primeiro, uma busca na web no máximo, e só as candidatas mais fortes recebem complemento |
| **Lista completa** | o usuário pede mais contas ou uma lista nova | de 15 a 25 contas | todos os sinais de `sinais.md` |
| **Diário** | rotina diária (`/atualizar` no modo diário) | o número pedido (padrão 10) | só scripts e sinais de até 3 dias |

## 1. Buscar (em paralelo)

- Abra uma lista de tarefas visível, com uma linha por sinal, escrita com o negócio do usuário (ex.: "vagas de SDR em empresas de software de SP", não "buscar vagas").
- Rode os scripts dos sinais escolhidos ao mesmo tempo (em paralelo, quando puder):
  - **Vagas:** `scripts/vagas.py "<termo1>" "<termo2>" … --paginas 2 --dias 45` (primeira lista: `--paginas 1`). Já traz `estruturar_do_zero` e, a partir da 2ª rodada, `crescimento_vagas`.
  - **Contratos públicos:** `scripts/licitacoes.py descobrir "<termo>" --dias 45 --valor-minimo <de acordo com o porte do ICP>`.
  - **Busca na web** (nova liderança, expansão, investimento): só se o sinal estiver em `sinais.md`. Primeira lista: uma busca por sinal, últimos 90 dias.
- Se puder usar subagentes, crie um por sinal de busca na web. Cada um só pode devolver um link que abriu e leu.
- **Meta de candidatas:** primeira lista, de 20 a 30; lista completa, de 40 a 60.

## 2. Completar as candidatas mais fortes

Ordene as candidatas pelo número de sinais e complete de cima pra baixo até bater a meta do modo:
- **Site e "o que vende":** ache o site oficial e escreva o que ela vende em uma linha. Confira se é comprador e não concorrente.
- **Ferramentas e maturidade:** rode `scripts/sites.py` com todos os sites de uma vez. Use pra preencher "Ferramentas ou concorrentes citados" e como pista de time comercial (chamada comercial, página de carreira).
- **Contratos públicos de quem já está na lista:** se o sinal for útil pro ICP, rode `scripts/licitacoes.py checar <cnpj1> <cnpj2> …` de uma vez.
- **CNPJ:** procure no rodapé, na política de privacidade ou nos termos do site. Depois rode `scripts/cnpj.py <cnpj1> <cnpj2> …` de uma vez. Se houver mais de uma empresa com o mesmo nome, só aceite o CNPJ cuja razão social e cidade batem. Na primeira lista, se o CNPJ não aparecer em 1 minuto, deixe vazio e siga.
- **Porte:** estime por pistas públicas e escreva "estimado".
- **Quem decide:** área e cargo provável, por `referencias/cargos-de-decisao.md`, ajustado pelos sinais (nova liderança ou vaga de liderança aberta).
- **Setor com pouca cobertura de contatos:** se a conta for de comércio local, restaurantes, transporte, ou não tiver presença profissional pública (site fraco, poucas vagas, sem página de carreira), escreva na coluna "alertas": "setor com pouca cobertura de contatos: faça a busca grátis na fulgurite antes de gastar créditos".

## 3. Checar

- Aplique os 9 itens da checagem de `referencias/nota-e-checagem.md`. A pressa nunca pula a checagem.
- Conta que falhar vai pra `dados/descartadas.csv` (nome, site, motivo curto).
- Nada de campo inventado. O que não foi achado fica vazio. O que foi deduzido leva "inferido".

## 4. Pontuar

- Calcule a nota de 0 a 100 e a faixa (A, B, C) pela fórmula de `referencias/nota-e-checagem.md`.
- Abaixo de 50, a conta vai pras descartadas com "nota baixa".
- "Por que agora" em uma linha: o fato, a data e por que importa pro produto do usuário, citando o produto ou o problema que ele resolve. Nunca a mesma frase em duas contas.
- "Próximo passo sugerido": "abordar esta semana" (A e B) ou "monitorar" (C).

## 5. Gravar e filtrar

- Grave `dados/contas.csv` com as colunas exatas de `COLUNAS_CONTAS` em `scripts/comum.py`, na ordem. As duas primeiras (`nome_empresa` e `site`) são obrigatórias.
- Datas no formato AAAA-MM-DD. "verificado_em" é a data de hoje.
- Rode `scripts/filtrar.py checar` pra tirar quem está no CRM do usuário, no histórico ou repetido.

## 6. Pouco resultado?

- Se sobraram menos de 8 contas, amplie uma coisa por vez, nesta ordem, e avise do que mudou:
  1. aumente `--dias` pra 60;
  2. inclua termos vizinhos;
  3. abra a região;
  4. abra uma faixa de porte.
- Nunca baixe a checagem pra completar número.
- Se mesmo assim vier pouco, entregue o que tem e explique em uma linha por quê.

## 7. Seguir

- Vá direto pro `/planilha`, sem pedir confirmação. O usuário revisa na planilha.

## Se o usuário tiver pressa

Pare as buscas em andamento, cheque o que já foi achado, grave e siga pro `/planilha`, avisando quais sinais ficaram sem buscar.
