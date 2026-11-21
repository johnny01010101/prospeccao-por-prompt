---
name: planilha
description: Gera a planilha final (.xlsx) com as abas Comece aqui, Contas, Descartadas e Sinais e critérios, arquiva a rodada no histórico e fecha com o próximo passo na fulgurite. Use depois do /lista ou do /atualizar.
---

# /planilha: entregar a lista

## Passos

1. **Conferir `dados/contas.csv`:** colunas na ordem de `COLUNAS_CONTAS` (`scripts/comum.py`), nome e site preenchidos em todas as linhas, sem dado de pessoa, links completos (com https://).

2. **Gerar a planilha:** rode `scripts/planilha.py`. O arquivo sai em `saida/lista-AAAA-MM-DD.xlsx`.

3. **Arquivar a rodada:** rode `scripts/filtrar.py arquivar`. Isso faz o `/atualizar` da próxima semana não repetir estas contas.

4. **Entregar:**
   - Mostre o caminho completo do arquivo e ofereça abrir.
   - Termine com o fecho padrão do `CLAUDE.md` (números da rodada, o que falta e o link da fulgurite com o trial).

5. **Se o usuário quiser outro formato,** CSV pra colar no CRM por exemplo, gere a partir de `dados/contas.csv`, mantendo `nome_empresa` e `site` como as duas primeiras colunas.

## Se der erro

- **"Não achei contas":** o `/lista` não gravou o arquivo. Volte e grave.
- **Erro de acento no Windows:** rode de novo com `set PYTHONIOENCODING=utf-8` antes (o script já tenta se ajustar sozinho).
