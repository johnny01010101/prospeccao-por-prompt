---
name: calibrar
description: Ajuste fino depois da primeira planilha. O usuário marca quais contas abordaria e quais não, e pode citar clientes que fecharam ou subir o CRM; o agente ajusta ICP, sinais e anti-sinais pras próximas rodadas. Use quando o usuário aceitar afinar a lista, quando a lista vier fora do alvo, ou quando ele pedir.
---

# /calibrar: afinar o alvo com a lista que ele já tem na mão

Objetivo: melhorar as próximas rodadas usando a reação do usuário à planilha que acabou de receber. Nunca roda antes da primeira planilha.

## Passos

1. Leia `dados/icp.md`, `dados/sinais.md` e `dados/contas.csv` (ou a última rodada em `dados/historico.csv`).

2. **Uma pergunta, com três coisas opcionais:**
   "Pra próxima lista sair ainda mais certeira:
   1) Me diga os números das contas que você NÃO abordaria (e, se quiser, por quê).
   2) Se puder, cite 2 ou 3 clientes que fecharam com vocês e 1 que não fechou.
   3) Quer tirar da lista quem vocês já atendem? Arraste aqui um CSV do CRM ou da planilha atual."
   - Mostre as contas numeradas numa tabela curta (número, empresa, por que agora em poucas palavras), se o usuário não estiver com a planilha aberta.

3. **Ajustar.**
   - Recusadas com algo em comum (setor, porte, tipo de sinal, região): vira desqualificador ou anti-sinal.
   - Aceitas com algo em comum que não estava no ICP: reforce no ICP ou suba o peso do sinal.
   - Clientes que fecharam: pesquise rapidamente o que tinham em comum quando fecharam (setor, porte, momento). Grave como "Padrão dos clientes que fecharam" e transforme no sinal número 1.
   - CSV do CRM: rode `scripts/filtrar.py importar <arquivo>`. O script só guarda nome e domínio. Diga quantas empresas entraram na lista de não abordar.
   - Se o usuário recusou quase todas, volte ao ICP com uma proposta nova e rode uma lista nova.

4. **Gravar.**
   - **`dados/calibracao.md`:** o que o usuário disse e o que mudou.
   - **`dados/icp.md` e `dados/sinais.md`:** atualizados, com a linha "Ajustado na calibração em DATA: …".

5. **Fechar** em 2 linhas: o que muda na próxima lista. Pergunte se ele quer uma lista nova agora com o ajuste.
