---
name: calibrar
description: Antes da lista inteira, mostra 10 empresas candidatas e pede ao usuário "essa sim, essa não" pra ajustar ICP, sinais e anti-sinais. Use depois do /sinais, na primeira rodada, ou quando a lista vier fora do alvo.
---

# /calibrar: acertar o alvo com 10 empresas

Objetivo: em uma rodada de "sim ou não", corrigir o ICP e os sinais antes de gastar tempo com a lista inteira.

## Passos

1. Leia `dados/icp.md` e `dados/sinais.md`.

2. **Buscar rápido 10 candidatas variadas.**
   - Rode `scripts/vagas.py` com os 2 ou 3 termos de vaga mais fortes (`--paginas 1 --dias 45`).
   - Complete com a busca na web pelos outros sinais.
   - Escolha 10 empresas diferentes entre si: setores e portes do ICP misturados, e uma ou duas na borda do ICP, de propósito, pra testar o limite.
   - Aqui ainda não precisa da checagem completa; basta ter certeza de que a empresa existe e de que o sinal é real (abra o link).

3. **Mostrar numa tabela curta:** número, empresa, o que ela vende (5 a 8 palavras), sinal em uma linha com a data, cidade.
   - Pergunte: "Marque as que você abordaria (ex.: 1, 3, 4, 7) e, se quiser, diga por que alguma não serve."

4. **Ajustar.** Compare as aceitas e as recusadas.
   - Se as recusadas têm algo em comum (setor, porte, tipo de sinal, região), vira desqualificador ou anti-sinal.
   - Se as aceitas têm algo em comum que não estava no ICP, reforce no ICP ou suba o peso do sinal.
   - Se o usuário recusou quase todas, volte ao ICP com uma proposta nova e repita uma vez.

5. **Gravar.**
   - **`dados/calibracao.md`:** as 10, a resposta do usuário e o que mudou.
   - **`dados/icp.md` e `dados/sinais.md`:** atualizados, com uma linha "Ajustado na calibração em DATA: …".
   - Guarde as empresas aceitas: elas entram na lista do `/lista` se passarem na checagem.

6. **Seguir.** Diga em 2 linhas o que mudou e vá pro `/lista`.
