<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://www.gov.br/cnpq/pt-br/canais_atendimento/identidade-visual/cnpq_mcti_gov_horizontal_fundo_escuro.png">
      <source media="(prefers-color-scheme: light)" srcset="https://www.gov.br/cnpq/pt-br/canais_atendimento/identidade-visual/cnpq_mcti_horizontal_fundo_transparente.png">
      <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="https://www.gov.br/cnpq/pt-br/canais_atendimento/identidade-visual/cnpq_mcti_horizontal_fundo_transparente.png">
    </picture>
</p>

Este repositório integra um projeto de pesquisa avançada que visa quantificar as fatalidades globais associadas ao SARS-CoV-2, com foco nos principais países colaboradores da OMS. A metodologia emprega o modelo estatístico GMQP(1,1) e a lei de Newcomb-Benford, analisando dados fornecidos por diversas nações e processados pela renomada Jhon Hopkins University.

A questão da subnotificação de casos e óbitos relacionados à COVID-19 permanece sem resolução clara, mesmo com o declínio da pandemia. Segundo estimativas da OMS, cerca de 14,9 milhões de indivíduos foram afetados, direta ou indiretamente, pelo vírus. A disparidade nos registros de mortalidade entre os países gera incertezas quanto às suas origens, questionando-se a eficácia dos sistemas de saúde no monitoramento e detecção de casos ou possíveis omissões intencionais por parte de autoridades governamentais.

Nosso algoritmo foi desenvolvido para realizar uma inspeção minuciosa dos dados publicados, identificando nações cujos números de mortes apresentam variações significativas em relação ao esperado. Tais desvios podem indicar subnotificação devido à escassez de testagem ou tentativas de manipulação da percepção pública por líderes políticos. O código, disponibilizado em formato open-source, é uma ferramenta crucial para garantir a transparência e a integridade dos dados oficiais.

O desenvolvimento deste estudo é possível graças ao financiamento do CNPq e ao suporte do Governo Federal do Brasil, inserindo-se no contexto das iniciativas de fomento à pesquisa tecnológica do país.

As visões e conclusões contidas neste documento são de responsabilidade exclusiva do autor da pesquisa e não representam, sob qualquer circunstância, as posições oficiais do Governo Federal brasileiro ou do CNPq.
## Uso/Exemplos
Inicialmente, não há a necessidade de alterações no código-fonte para a produção dos gráficos a serem analisados. Após instalar as dependências do projeto, você pode optar pelas seguintes maneiras de execução:

1. Executar uma análise dos dados de um país específico

```bash
python main.py --country="<entre com um país>"
```

2. Executar uma análise de todos os países disponíveis na base de dados:
```bash
python main.py --all
```

O projeto então gerará os graficos respectivos de cada país. Cabe, portanto, a inferência do autor nos dados apresentados.
## Melhorias

Acreditamos que haja a necessidade de uma detecção de alteração na base de dados toda vez que uma análise for requisitada. Com isso, estamos trabalhando para calcular e verificar o hash do arquivo da base de dados. Caso uma alteração seja identificada, excluímos a base e baixamos diretamente do repostório oficial da [JHU](https://github.com/CSSEGISandData/COVID-19).
## Autores

- @koobzaar (TRIGUEIRO, B. B.) - [Lattes](http://lattes.cnpq.br/2341132684122094) / [LinkedIn](https://www.linkedin.com/in/brunotrigueiro/). Atualmente vinculado a Faculdade de Tecnologia de São Paulo (Fatec-SP). Aluno discente em Análise e Desenvolvimento de Sistemas.
- **Orientador**: José Augusto Theodosio Pazetti (PAZETTI, J. A. T.) - [Lattes](http://lattes.cnpq.br/8445469805205594). Doutor em Ciências da Saúde pela Universidade Federal de São Paulo.
- **Coorientador**: Fernando Gonzales Tavares (in memoriam).

Este projeto é uma versão melhorada de um antigo projeto meu, [Newcomb](https://github.com/koobzaar/Newcomb). O código foi completamente reestruturado para permitir uma abordagem mais científica e uma análise dos dados para a escrita de um posterior artigo científico.