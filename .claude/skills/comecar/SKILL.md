---
name: comecar
description: Primeiro passo do Prospecção por Prompt. Lê o site do usuário, entende o que ele vende e propõe o ICP, os cargos de quem decide, os desqualificadores e os concorrentes a excluir, com uma confirmação. Opcionalmente importa a lista atual ou o CRM pra não repetir contas. Use na primeira vez, quando dados/icp.md não existe, ou quando o usuário pedir pra refazer o ICP.
---

# /comecar: entender o negócio e montar o ICP

Objetivo: sair com `dados/empresa.md`, `dados/icp.md` e, se o usuário quiser, `dados/nao-abordar.csv`, fazendo no máximo 3 perguntas.

## Passos

1. **Ambiente.** Se ainda não rodou nesta máquina, rode `scripts/ambiente.py` e resolva o que faltar sem pedir comandos ao usuário.

2. **Pergunta 1 (obrigatória):** "Qual é o site da sua empresa?"
   - Se ele não tiver site, peça uma frase sobre o que vende e pra quem.

3. **Ler o negócio.** Abra o site (home, produto ou serviços, preços, sobre, clientes ou cases, carreira). Anote:
   - o que vende, em uma linha, e o resultado que promete;
   - pra quem vende: setor, porte, região; quem usa e quem paga;
   - pistas de clientes (logos, cases) e de concorrentes;
   - preço ou forma de venda, se aparecer.
   - Marque o que foi observado e o que foi deduzido.

4. **Propor o ICP.** Com o que leu e com `referencias/cargos-de-decisao.md`, monte uma proposta curta:
   - setor ou setores (no máximo 3);
   - porte (faixa de funcionários);
   - região;
   - área que compra e cargo provável de quem decide;
   - desqualificadores (quem não comprar, ex.: concorrentes, pessoa física, porte muito pequeno);
   - concorrentes do usuário a excluir (de 3 a 8 nomes, achados na busca).

5. **Pergunta 2 (confirmação):** mostre a proposta em no máximo 10 linhas e pergunte "Está certo? Pode corrigir o que quiser."
   - Junto, de forma opcional, peça: "Se puder, me diga 2 ou 3 clientes que fecharam com vocês e 1 ou 2 que não fecharam. Isso deixa a lista bem mais certeira."
   - Se ele der nomes, pesquise rapidamente o que esses clientes tinham em comum quando fecharam (setor, porte, momento) e anote como "padrão dos clientes que fecharam" e "padrão de quem não fechou".

6. **Pergunta 3 (opcional):** "Quer que eu tire da lista quem vocês já atendem ou já abordaram? Se quiser, arraste aqui um CSV exportado do CRM ou da planilha atual."
   - Se ele mandar, rode `scripts/filtrar.py importar <arquivo>`. O script só guarda nome e domínio da empresa.
   - Diga quantas empresas entraram na lista de não abordar.

7. **Gravar os arquivos.**
   - **`dados/empresa.md`:** o que vende, pra quem, diferenciais, observado ou deduzido.
   - **`dados/icp.md`,** com as seções: Setores, Porte, Região, Quem decide (área e cargo), Desqualificadores, Concorrentes a excluir, Padrão dos clientes que fecharam, Padrão de quem não fechou, Data.

8. **Seguir.** Resuma em 3 linhas e vá direto pro `/sinais`.

## Não faça

- Não peça o ICP do zero ("qual é o seu ICP?"). Proponha e deixe a pessoa corrigir.
- Não pergunte ferramentas, stack, voz de marca nem nada que não muda a lista.
- Não guarde nome de pessoa do CRM.
