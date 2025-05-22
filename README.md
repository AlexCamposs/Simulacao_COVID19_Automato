
# Simulação Epidemiológica com Autômatos Celulares: Um Estudo da COVID-19 em Ontário, Canadá

**Projeto de Conclusão de Curso – Ciência da Computação (FACOM/UFU)**  
**Autor:** Alex Campos do Nascimento  
**Orientador:** Prof. Dr. Luiz Gustavo Almeida Martins

---

## Resumo

Diante da problemática da propagação de doenças infecciosas na sociedade moderna, como a COVID-19, a utilização de modelos computacionais para simular as epidemias é de suma importância para criar medidas de prevenção e combate a tais doenças. Uma forma de realizar a modelagem epidemiológica é utilizando autômatos celulares, os quais conseguem reproduzir modelos complexos a partir de regras simples.

Neste trabalho, foi desenvolvido um modelo epidemiológico SEIRD (Suscetível, Exposto, Infectado, Recuperado e Morto) baseado em autômato celular determinístico para simular a propagação da COVID-19 em unidades de saúde pública na província canadense de Ontário. Resultados experimentais mostram que o modelo desenvolvido apresenta um comportamento semelhante aos casos ativos reais das regiões investigadas.

---

## Estrutura do Projeto

O projeto consiste em:

- Leitura e tratamento de dados geoespaciais com `geopandas`.
- Definição de um autômato celular determinístico baseado no modelo SEIRD.
- Integração de vizinhança espacial com pesos proporcionais à fronteira compartilhada entre regiões.
- Simulação diária da propagação da doença com ajuste de parâmetros de restrição de mobilidade.
- Comparação de dados simulados com dados reais da COVID-19 em Ontário (2020).

---

## Como Executar

1. **Bibliotecas Necessárias:**

   - `numpy`
   - `pandas`
   - `matplotlib`
   - `geopandas`

   Instale manualmente com:

   ```bash
   pip install numpy pandas matplotlib geopandas
   ```

2. **Dados necessários:**

   - Shapefile de fronteiras das Unidades de Saúde de Ontário (incluído na pasta `MOH_PHU_BOUNDARY_*`)
   - Dados reais de casos de COVID-19 (`conposcovidloc.csv`), **não incluído no repositório** por exceder o limite do Git. Baixe manualmente em:

     > https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario

   Após baixar, coloque o arquivo na raiz do projeto ou ajuste o caminho no código.

3. **Execução:**

   Basta rodar o script principal em Python. A simulação será executada por 274 dias. Para gerar o gráfico de uma determinada Unidade de Saúde Pública (PHU), altere a linha no final do script:

   ```python
   phu_data_filtered = real_data_filtered[real_data_filtered["Reporting_PHU"] == "NOME_DA_PHU"]
   ```

   Substitua `"NOME_DA_PHU"` pelo nome da unidade desejada, como por exemplo `"Windsor-Essex County Health Unit"`.

   O gráfico será salvo em `resultados/<nome>.png`.

---

## Resultados

O modelo foi validado com dados reais de várias regiões de Ontário, e demonstrou comportamento qualitativamente semelhante às curvas de casos ativos reais de COVID-19 ao longo do tempo.

---

## Observações

- A modelagem inicia surtos em Toronto, Ottawa e Windsor.
- O modelo inclui política de restrição de mobilidade ativada por limiares de população infectada.
- O sistema de vizinhança é calculado com base em fronteiras geográficas reais.

---

## Contato

Alex Campos do Nascimento  
Email: [alex_cn2001@hotmail.com]  
FACOM - Universidade Federal de Uberlândia

---

## Licença

Este projeto está licenciado sob a [Licença Pública Geral GNU v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

Você é livre para usar, modificar e distribuir este código, desde que qualquer trabalho derivado também seja licenciado sob os mesmos termos, garantindo que ele continue livre para todos.

Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.
