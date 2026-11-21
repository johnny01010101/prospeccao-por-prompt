# Checagem de qualidade e nota da conta

## Checagem: nenhuma conta entra sem passar por todos os itens

1. **Fonte lida:** o link do sinal foi aberto e o texto confirma o que foi dito. Trecho de resultado de busca não vale. Se a página não abrir, tente outra rota legítima (página da empresa, outro portal). Se nada confirmar, descarte o sinal.
2. **Data visível:** sinal sem data não é sinal principal. Sinal vencido (ver `sinais.md`) derruba o momento.
3. **Comprador, não concorrente:** pela página em que a palavra aparece.
4. **Dentro do ICP:** setor, porte (mesmo estimado) e região.
5. **CNPJ ativo**, quando o CNPJ foi encontrado. CNPJ baixado, inapto ou suspenso: descarte.
6. **Fora das listas:** não abordar (CRM do usuário), histórico (rodadas anteriores), concorrentes e a própria empresa do usuário. Rode `python scripts/filtrar.py checar`.
7. **Sem duplicada:** mesma empresa com outro nome, outra marca ou outro domínio. Junte num registro só, somando os sinais.
8. **Anti-sinais:** um, penalidade e alerta; dois ou mais, descarte.
9. **Nada inventado:** se um campo não foi achado, fica vazio. Nunca preencher com palpite sem marcar "inferido".

Toda conta que sai vai pra `dados/descartadas.csv` com o motivo em poucas palavras.

## Nota (0 a 100)

```
nota = fit×0,35 + força_do_sinal×0,30 + momento×0,20 + evidência×0,15 + bônus − penalidade
```
Cada componente vai de 0 a 100.

| Componente | 100 | 50 | 0 |
|---|---|---|---|
| **Fit com o ICP** | setor, porte e região batem, e há time comercial ou área compradora clara | dois dos três batem | fora do ICP: não entra |
| **Força do sinal** | sinal nos 3 primeiros níveis de `sinais.md` e ligado direto ao produto | sinal médio (expansão, investimento) | só conteúdo do site |
| **Momento** | sinal de até 15 dias | 16 a 45 dias | vencido |
| **Evidência** | 2 fontes independentes, tudo observado | 1 fonte confiável | inferido, sem fonte direta |

- **Bônus:** mais 5 por tipo de sinal diferente além do primeiro (máximo de mais 10). Mais 10 se repete o gatilho dos clientes que fecharam. Mais 5 se a vaga fala em estruturar a área do zero e o produto ajuda nisso. Mais 5 se as vagas cresceram 2 ou mais desde a última rodada.
- **Penalidade:** menos 15 por anti-sinal (dois anti-sinais: descarte).

## Faixas

- **A (80 a 100):** abordar esta semana.
- **B (65 a 79):** abordar esta semana, depois das A.
- **C (50 a 64):** monitorar e rodar `/atualizar` na próxima semana.
- **Abaixo de 50:** descartada, com o motivo "nota baixa".

## "Por que agora" (uma linha)

Fórmula: o que aconteceu, quando, e por que isso importa pro produto do usuário.

- Bom: "abriu 4 vagas de executivo de vendas desde 05/11 e contratou um gerente comercial novo".
- Ruim: "empresa em crescimento" (vago, sem data, sem fonte).

Melhor 10 contas fortes do que 30 genéricas.
