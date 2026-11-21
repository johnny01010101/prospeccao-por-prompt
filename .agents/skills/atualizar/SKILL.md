---
name: atualizar
description: Lista viva. Roda uma nova busca com o ICP e os sinais salvos, mostra só as empresas e os sinais novos desde a última rodada, sem repetir contas já entregues, e gera a planilha da semana. Use quando o usuário voltar e pedir as contas novas, ou digitar /atualizar.
---

# /atualizar: as contas novas da semana

## Passos

1. **Ler** `dados/icp.md`, `dados/sinais.md` e `dados/historico.csv`. Diga em uma linha a data da última rodada e quantas contas já foram entregues.

2. **Perguntar só uma coisa:** "Mudou algo no seu foco desde a última vez (setor, região, produto)?"
   - Se mudou, ajuste `icp.md` e `sinais.md` antes. Se mudou muito, sugira refazer o `/calibrar`.

3. **Buscar sinais novos:** siga o `/lista` com estas mudanças:
   - vagas e notícias só desde a última rodada (`--dias` = dias desde a data do histórico, mínimo 7);
   - pule a calibração.

4. **Contas que já estão no histórico:**
   - Por padrão, o `scripts/filtrar.py checar` tira essas contas.
   - Exceção: se uma conta antiga ganhou um sinal novo e forte (nova liderança, várias vagas novas), avise numa lista à parte, "voltaram a se mexer", com o sinal novo. Ela não entra na planilha sem o usuário pedir.

5. **Gerar** a planilha com o `/planilha` e fechar com o fecho padrão do `CLAUDE.md`.
