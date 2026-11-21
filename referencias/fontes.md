# Fontes públicas e como usar cada uma

Regra geral: só páginas públicas, abertas sem login. Nunca contornar login, paywall, captcha ou bloqueio. Ir devagar (uma requisição por segundo nos scripts).

## Vagas abertas

- **Portal Gupy (via script):** a maior fonte de vagas de empresas médias e grandes no Brasil.
  `python scripts/vagas.py "termo 1" "termo 2" --paginas 2 --dias 45 --descricao`
  Devolve as empresas agrupadas, com a quantidade de vagas, os cargos, as datas, as cidades e o link de cada vaga. Com `--descricao`, traz o começo do texto da vaga, que serve pra achar ferramentas citadas e frases como "estruturar a área do zero".
- **Páginas de carreira das próprias empresas:** use a busca na web com `site:gupy.io`, `site:vagas.solides.com.br`, `site:jobs.kenoby.com`, `site:boards.greenhouse.io` ou `site:jobs.lever.co`, mais o termo.
- **Outros portais públicos** (Vagas.com.br, InfoJobs, Catho, Indeed Brasil): use a busca na web e abra só as páginas públicas da vaga.
- **LinkedIn:** não abra páginas do LinkedIn (exige login e os termos proíbem coleta automática). Se um resultado de busca do LinkedIn aparecer, use no máximo o título do resultado como pista e confirme o sinal em outra fonte.

## Notícias e anúncios

- Use a busca na web do Claude com o nome da empresa mais palavras como "expansão", "nova unidade", "investimento", "contrata", "novo diretor", "aquisição", "rodada".
- Prefira veículos de negócios, o site da própria empresa (sala de imprensa, blog) e comunicados oficiais.
- Abra a notícia e confira a data antes de usar.

## Dados da empresa (CNPJ)

- **Consulta pública de CNPJ (via script):** BrasilAPI, com a Minha Receita de reserva.
  `python scripts/cnpj.py 00.000.000/0001-00`
  Devolve razão social, nome fantasia, atividade (CNAE), porte da Receita, município, UF, situação cadastral e ano de abertura. O script já descarta sócios, CPF, e-mail e telefone.
- **Como achar o CNPJ:** rodapé do site da empresa, página de política de privacidade ou termos, ou a busca na web com "nome da empresa" + "CNPJ". Confira se a razão social bate com a empresa certa (cuidado com homônimos).
- **Porte da Receita** (ME, EPP, DEMAIS) não é número de funcionários. Estime o número de funcionários por outras pistas (vagas, site, notícias) e marque como "estimado".

## Site da empresa

- **O que olhar:** o que ela vende (uma linha), pra quem vende, onde atua, se tem time comercial (página de contato comercial, "fale com um consultor", vagas de vendas).
- **Interpretação:** página de produto mostra o que a empresa vende; página de carreira mostra do que ela precisa.

## O que nunca usar

- Bases compradas, vazadas ou de "lista de contatos".
- Dados de pessoas: nome de funcionário, e-mail, telefone, perfil pessoal.
- Grupos privados, conteúdo atrás de login, páginas com bloqueio de robôs.
