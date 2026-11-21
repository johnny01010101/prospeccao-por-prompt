---
name: comecar
description: Primeiro passo do Prospecção por Prompt. Pede só o site, lê o negócio, decide sozinho o ICP e os 2 a 4 sinais de compra mais fortes, mostra tudo numa confirmação só e já parte pra lista. Use na primeira vez, quando dados/icp.md não existe, ou quando o usuário pedir pra refazer o ICP.
---

# /comecar: do site à busca, com uma pergunta e uma confirmação

Objetivo: em poucos minutos, sair com `dados/empresa.md`, `dados/icp.md` e `dados/sinais.md` e começar a buscar. Valor rápido vem antes de perfeição: o ajuste fino fica pra depois da primeira planilha.

**Rápido não pode parecer genérico.** A pessoa precisa sentir que você estudou a empresa dela. Por isso, poucas perguntas, mas cada frase sua cita algo concreto do site dela: o produto pelo nome, um cliente ou case que aparece lá, o diferencial, o tipo de cliente que ela atende. Nunca use frases que serviriam pra qualquer empresa.

## Passos

1. **Ambiente.** Se ainda não rodou nesta máquina, rode `scripts/ambiente.py` e resolva o que faltar sem pedir comandos ao usuário.

2. **Única pergunta obrigatória:** "Qual é o site da sua empresa?"
   - Sem site: peça uma frase sobre o que vende e pra quem.

3. **Ler o negócio (rápido).** Abra a home e, no máximo, mais 2 páginas (produto ou serviços, clientes ou cases). Anote o que vende, pra quem, pistas de clientes e de concorrentes. Marque o que foi observado e o que foi deduzido.

4. **Decidir sozinho, sem perguntar:**
   - **ICP:** setores (até 3), porte, região, área que compra e cargo provável de quem decide (`referencias/cargos-de-decisao.md`), desqualificadores e de 3 a 8 concorrentes a excluir.
   - **Sinais:** escolha de 2 a 4 no "Menu de sinais" de `referencias/sinais.md`. Critérios, nesta ordem: o mais ligado ao problema que o produto resolve, o mais confiável, o mais rápido de buscar. Pelo menos um sinal com script. No máximo um sinal de busca na web.
   - **Termos de busca:** de 3 a 6 por sinal, em português, do jeito que aparecem em vagas e notícias brasileiras.

5. **Uma confirmação só.** Mostre em no máximo 10 linhas:
   ```
   Li o site de vocês. Entendi que a <empresa> vende <produto, pelo nome> pra <quem>,
   e que o diferencial é <o que o site destaca>. Vi <um cliente, case ou número do site>.
   Vou buscar empresas de <setores>, <porte>, em <região>.
   Sinais que vou usar, e por quê pra vocês:
   1) <sinal>: <por que, ligado ao produto deles, em poucas palavras>
   2) <sinal>: <por quê>
   Vou tirar: <concorrentes pelo nome e desqualificadores, curto>
   Posso começar? Se algo estiver errado, é só corrigir.
   ```
   - Exemplo de "por quê" bom: "vaga de SDR: quem contrata SDR vai precisar de lista, e é isso que o <produto> resolve". Ruim: "vagas abertas indicam crescimento".
   - Se a pessoa corrigir, ajuste e comece, sem nova rodada de perguntas. Agradeça citando o que mudou ("boa, tirei o varejo e foquei em indústria").
   - Não peça clientes que fecharam nem o CRM agora. Isso entra depois da primeira planilha.

6. **Gravar os arquivos.**
   - **`dados/empresa.md`:** o que vende, pra quem, diferenciais, observado ou deduzido.
   - **`dados/icp.md`:** Setores, Porte, Região, Quem decide (área e cargo), Desqualificadores, Concorrentes a excluir, Padrão dos clientes que fecharam (vazio por enquanto), Padrão de quem não fechou (vazio), Data.
   - **`dados/sinais.md`:** Sinais (em ordem, com o que é, por que indica compra, validade em dias, peso, script ou busca na web), Termos pra vagas, Termos pra busca na web, Anti-sinais (de `referencias/sinais.md`, mais os concorrentes), Data.

7. **Seguir na hora** pro `/lista` no modo "primeira lista". Diga em uma linha o que vai buscar primeiro, com as palavras do negócio dela (ex.: "Começando pelas indústrias de SP que abriram vaga de compras: é aí que o <produto> entra.").

## Não faça

- Não pergunte "qual é o seu ICP?" nem "quais sinais você quer?". Você decide e a pessoa corrige.
- Não pergunte ferramentas, stack, voz de marca nem nada que não muda a lista.
- Não guarde nome de pessoa.
