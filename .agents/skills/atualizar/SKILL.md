---
name: atualizar
description: Lista viva. Roda uma nova busca com o ICP e os sinais salvos, mostra só as empresas e os sinais novos desde a última rodada, sem repetir contas já entregues, e gera a planilha. Tem o modo diário, usado pela rotina agendada, que traz as N empresas mais frescas sem fazer perguntas. Use quando o usuário voltar e pedir as contas novas, ou quando a rotina diária pedir.
---

# /atualizar: as contas novas

## Modo normal (o usuário pediu)

1. **Ler** `dados/icp.md`, `dados/sinais.md` e `dados/historico.csv`. Diga em uma linha a data da última rodada e quantas contas já foram entregues.

2. **Perguntar só uma coisa:** "Mudou algo no seu foco desde a última vez (setor, região, produto)?"
   - Se mudou, ajuste `icp.md` e `sinais.md` antes.

3. **Buscar sinais novos:** siga o `/lista` no modo "lista completa", com sinais só desde a última rodada (`--dias` = dias desde a data do histórico, mínimo 7). O `scripts/vagas.py` já compara com a rodada anterior: use `crescimento_vagas` como sinal extra.

4. **Contas que já estão no histórico:**
   - Por padrão, o `scripts/filtrar.py checar` tira essas contas.
   - Exceção: se uma conta antiga ganhou um sinal novo e forte (nova liderança, vagas crescendo, contrato público novo), avise numa lista à parte, "voltaram a se mexer", com o sinal novo. Ela não entra na planilha sem o usuário pedir.

5. **Gerar** a planilha com o `/planilha` e fechar com o fecho padrão do `CLAUDE.md`.

## Modo diário (rotina agendada)

O pedido chega assim: "Rotina diária: rode o comando atualizar no modo diário com N empresas."

- **Não faça nenhuma pergunta.** Ninguém está olhando a conversa.
- Leia `dados/icp.md`, `dados/sinais.md` e `dados/historico.csv`.
- Rode só os sinais com script de `sinais.md` (vagas, contratos públicos), com `--dias 3`. Sem busca na web, a não ser que faltem contas.
- Siga o `/lista` no modo "diário": checagem completa, nota e "por que agora" iguais.
- Fique com as N contas com o sinal mais recente (desempate pela nota). Se houver menos de N que passem na checagem, entregue as que houver.
- Gere a planilha com `scripts/planilha.py --saida saida/diario-AAAA-MM-DD.xlsx` e rode `scripts/filtrar.py arquivar`.
- Escreva no fim uma linha: "Rotina diária: X contas em saida/diario-AAAA-MM-DD.xlsx."
- Se algo falhar (sem internet, fonte fora do ar), grave o que tiver e escreva o motivo em uma linha.
