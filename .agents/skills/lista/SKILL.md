---
name: lista
description: Monta a lista de empresas da rodada. Busca sinais em paralelo (vagas, notícias, sites), confere cada fonte, checa CNPJ, descarta concorrentes, repetidas e anti-sinais, dá nota de 0 a 100, aponta o cargo provável de quem decide e grava dados/contas.csv. Use depois do /calibrar, ou quando o usuário pedir uma lista nova.
---

# /lista: as contas da rodada

Objetivo: de 15 a 25 contas verificadas em `dados/contas.csv`, com as descartadas e o motivo em `dados/descartadas.csv`. Melhor 10 fortes que 30 genéricas.

Leia antes: `dados/icp.md`, `dados/sinais.md`, `dados/calibracao.md` (se existir), `referencias/fontes.md`, `referencias/nota-e-checagem.md`, `referencias/cargos-de-decisao.md`.

## 1. Buscar (em paralelo)

- Abra uma lista de tarefas visível.
- Se puder usar subagentes, crie um por tipo de sinal. Cada um recebe o resumo do ICP, o sinal, os termos e as regras de `CLAUDE.md`, e só pode devolver um link que abriu e leu. Sem subagentes, faça um sinal por vez.
- **Vagas:** `scripts/vagas.py "<termo1>" "<termo2>" … --paginas 2 --dias 45 --descricao`. Use todos os termos de vaga do `sinais.md`. Junte o resultado por empresa.
- **Outros sinais:** busca na web com os termos do `sinais.md`, priorizando os últimos 90 dias.
- **Ponto de partida:** junte as empresas aceitas na calibração.
- **Meta de candidatas:** de 40 a 60, antes da checagem.

## 2. Completar cada candidata

Pra cada empresa (comece pelas que têm mais sinais):
- **Site e "o que vende":** ache o site oficial e escreva o que ela vende em uma linha. Confira se é comprador e não concorrente.
- **CNPJ:** procure no rodapé, na política de privacidade ou nos termos do site, ou na busca na web. Depois rode `scripts/cnpj.py <cnpj>` pra pegar atividade, cidade, UF, situação e ano de abertura. Se houver mais de uma empresa com o mesmo nome, só aceite o CNPJ cuja razão social e cidade batem.
- **Porte:** estime o número de funcionários por pistas públicas e escreva "estimado".
- **Sinais extras:** procure de 1 a 2 sinais a mais pra cada candidata forte (outra vaga, notícia, nova liderança). Sinais de tipos diferentes somam.
- **Vagas comerciais abertas:** a quantidade e os cargos.
- **Ferramentas ou concorrentes citados:** procure nas descrições das vagas e no site (ex.: "experiência com X").
- **Quem decide:** área e cargo provável, por `referencias/cargos-de-decisao.md`, ajustado pelos sinais (nova liderança ou vaga de liderança aberta).
- **Setor com pouca cobertura de contatos:** se a conta for de comércio local, restaurantes, transporte, ou não tiver presença profissional pública (site fraco, poucas vagas, sem página de carreira), escreva na coluna "alertas": "setor com pouca cobertura de contatos: faça a busca grátis na fulgurite antes de gastar créditos". A conta continua na lista; o aviso é só pra pessoa não se frustrar no próximo passo.

## 3. Checar

- Aplique os 9 itens da checagem de `referencias/nota-e-checagem.md`.
- Conta que falhar vai pra `dados/descartadas.csv` (nome, site, motivo curto).
- Nada de campo inventado. O que não foi achado fica vazio. O que foi deduzido leva "inferido".

## 4. Pontuar

- Calcule a nota de 0 a 100 e a faixa (A, B, C) pela fórmula de `referencias/nota-e-checagem.md`.
- Abaixo de 50, a conta vai pras descartadas com "nota baixa".
- Escreva o "por que agora" em uma linha: o fato, a data e por que importa pro produto do usuário.
- Preencha "próximo passo sugerido": "abordar esta semana" (A e B) ou "monitorar" (C).

## 5. Gravar e filtrar

- Grave `dados/contas.csv` com as colunas exatas de `COLUNAS_CONTAS` em `scripts/comum.py`, na ordem. As duas primeiras (`nome_empresa` e `site`) são obrigatórias.
- Datas no formato AAAA-MM-DD. "verificado_em" é a data de hoje.
- Rode `scripts/filtrar.py checar` pra tirar quem está no CRM do usuário, no histórico ou repetido.

## 6. Pouco resultado?

- Se sobraram menos de 10 contas, amplie uma coisa por vez, nesta ordem, e avise o usuário do que mudou:
  1. aumente `--dias` pra 60;
  2. inclua termos vizinhos;
  3. abra a região;
  4. abra uma faixa de porte.
- Nunca baixe a checagem pra completar número.
- Se mesmo assim vier pouco, entregue o que tem e explique em uma linha por quê (ex.: "mercado pequeno, poucas vagas públicas").

## 7. Mostrar e seguir

- Mostre um resumo: total por faixa, as 5 melhores (empresa, nota, por que agora), quantas foram descartadas e os 3 motivos mais comuns.
- Pergunte só se o usuário quer tirar alguma. Em seguida, rode o `/planilha`.

## Se o usuário tiver pressa

Pare as buscas em andamento, cheque o que já foi achado, grave e siga pro `/planilha`, avisando quais sinais ficaram sem buscar.
