---
name: planilha
description: Gera a planilha final (.xlsx) com as abas Comece aqui, Contas, Descartadas e Sinais e critérios, arquiva a rodada no histórico, fecha com o próximo passo na fulgurite e oferece o ajuste fino e a rotina diária. Use depois do /lista ou do /atualizar.
---

# /planilha: entregar a lista

## Passos

1. **Conferir `dados/contas.csv`:** colunas na ordem de `COLUNAS_CONTAS` (`scripts/comum.py`), nome e site preenchidos em todas as linhas, sem dado de pessoa, links completos (com https://).

2. **Gerar a planilha:** rode `scripts/planilha.py`. O arquivo sai em `saida/lista-AAAA-MM-DD.xlsx`.

3. **Arquivar a rodada:** rode `scripts/filtrar.py arquivar`. Isso faz a próxima rodada não repetir estas contas.

4. **Entregar:**
   - Antes do fecho, mostre as 3 melhores contas, cada uma com o "por que agora" ligado ao produto do usuário. É aqui que a pessoa vê que a lista foi feita pra ela.
   - Mostre o caminho completo do arquivo e ofereça abrir.
   - Termine com o fecho padrão do `CLAUDE.md`.

5. **Depois do fecho, duas ofertas curtas** (só se ainda não foram feitas):
   - **Ajuste fino** (só na primeira planilha): "Quer que a próxima saia ainda mais certeira? Me diga quais contas você não abordaria." Se ele responder, rode o `/calibrar`.
   - **Rotina diária:** "Quer que eu traga empresas novas todo dia? Eu deixo agendado: todo dia, no horário que você escolher, as N empresas com os sinais mais frescos numa planilha nova. Quantas por dia e a que horas?"
     - Se ele topar, rode `scripts/agendar.py criar --hora HH:MM --qtd N` (versão ChatGPT: `--motor codex`). Sugira 10 por dia às 08:00 se ele não tiver preferência.
     - Avise em uma linha: o computador precisa estar ligado no horário e cada rodada usa o plano dele, como uma conversa normal.
     - Pra desligar: `scripts/agendar.py remover`. Pra ver como está: `scripts/agendar.py status`.

6. **Se o usuário quiser outro formato,** CSV pra colar no CRM por exemplo, gere a partir de `dados/contas.csv`, mantendo `nome_empresa` e `site` como as duas primeiras colunas.

## Se der erro

- **"Não achei contas":** o `/lista` não gravou o arquivo. Volte e grave.
- **Erro de acento no Windows:** rode de novo com `set PYTHONIOENCODING=utf-8` antes (o script já tenta se ajustar sozinho).
- **A rotina não ligou:** mostre a mensagem do `scripts/agendar.py` e diga o que fazer em uma linha.
