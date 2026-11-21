---
name: sinais
description: Troca, inclui ou tira sinais de compra (vagas, estruturar do zero, contratos públicos, ferramentas no site, nova liderança, expansão, investimento) e os termos de busca em dados/sinais.md. Use quando o usuário quiser mudar o que conta como sinal, ou quando a lista vier fraca. Na primeira vez, o /comecar já escolhe os sinais sozinho.
---

# /sinais: mudar o que mostra que uma empresa vai comprar agora

Objetivo: atualizar `dados/sinais.md` com uma confirmação só.

## Passos

1. Leia `dados/empresa.md`, `dados/icp.md`, `dados/sinais.md` (se existir) e `referencias/sinais.md`.

2. **Propor a mudança.**
   - Se o usuário disse o que quer, aplique.
   - Se a lista veio fraca, proponha trocar o sinal mais fraco por outro do "Menu de sinais", e explique em uma linha por quê.
   - Se houver padrão dos clientes que fecharam em `icp.md`, ele vira o sinal número 1.

3. **Termos de busca.** De 3 a 6 por sinal, em português, do jeito que aparecem em vagas, contratos e notícias brasileiras. Separe termos pro `scripts/vagas.py`, termos pro `scripts/licitacoes.py descobrir` (objeto do contrato) e termos pra busca na web.

4. **Confirmação.** Mostre em no máximo 8 linhas os sinais em ordem, um exemplo de "por que agora" pra cada e os anti-sinais. Pergunte: "Fica assim?"

5. **Gravar `dados/sinais.md`** (mesmas seções do `/comecar`) com a linha "Ajustado em DATA: …".

## Não faça

- Não use sinais que dependem de dados de pessoas (troca de emprego de alguém, post de alguém).
- Não inclua sinal que você não consegue achar em fonte pública.
