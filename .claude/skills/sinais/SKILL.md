---
name: sinais
description: Escolhe os sinais de compra que importam pro mercado do usuário (vagas, nova liderança, expansão etc.), os anti-sinais e os termos de busca em português, e grava em kit/sinais.md. Use depois do /comecar, ou quando o usuário quiser mudar o que conta como sinal.
---

# /sinais: o que mostra que uma empresa vai comprar agora

Objetivo: gravar `kit/sinais.md` com de 4 a 6 sinais, os anti-sinais e os termos de busca, com uma confirmação do usuário.

## Passos

1. Leia `kit/empresa.md`, `kit/icp.md` e `referencias/sinais.md`.

2. **Escolher os sinais.**
   - Encontre na tabela "Sinais por tipo de produto vendido" a linha (ou linhas) que combinam com o que o usuário vende. Se nenhuma servir, monte uma com a pergunta: "qual cargo a empresa contrata quando passa a ter o problema que ele resolve? Que evento cria esse problema?".
   - Se houver padrão dos clientes que fecharam em `icp.md`, transforme esse padrão no sinal número 1.
   - Ordene pela confiabilidade de `referencias/sinais.md`. Vaga aberta ligada ao problema costuma ser o sinal principal no Brasil.

3. **Termos de busca.** Pra cada sinal, escreva de 3 a 6 termos em português, do jeito que aparecem em vagas e notícias brasileiras (ex.: "executivo de vendas", "pré-vendas", "estruturar área comercial"). Separe:
   - termos pro `scripts/vagas.py`: cargos;
   - termos pra busca na web: notícias, expansão, liderança.

4. **Anti-sinais.** Liste os de `referencias/sinais.md` que valem pro caso, mais o padrão de quem não fechou (se houver) e os concorrentes do `icp.md`.

5. **Confirmação.** Mostre em no máximo 12 linhas: os sinais em ordem, um exemplo de "por que agora" pra cada, e os anti-sinais. Pergunte: "Faz sentido? Quer tirar ou incluir algum?"

6. **Gravar `kit/sinais.md`,** com as seções:
   - Sinais (em ordem, cada um com: o que é, por que indica compra, validade em dias, peso alto, médio ou baixo);
   - Termos pra vagas;
   - Termos pra busca na web;
   - Anti-sinais;
   - Data.

7. **Seguir.** Resuma em 2 linhas e vá pro `/calibrar`.

## Não faça

- Não use sinais que dependem de dados de pessoas (troca de emprego de alguém, post de alguém).
- Não inclua sinal que você não consegue achar em fonte pública.
