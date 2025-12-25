🚀 Desafio 6 Dias de Ciência de Dados
Este repositório contém a resolução de um desafio intensivo de 6 dias, cobrindo todo o pipeline de dados: desde a limpeza e análise exploratória até à construção de modelos de Machine Learning, integração via API e testes estatísticos.

📋 Estrutura do Projeto
O desafio foi dividido em duas grandes temáticas: Análise de Gastos Públicos (Senado Federal) e Sistemas de Recomendação de Filmes (MovieLens).

Parte 1: Análise e Previsão (Dias 1 a 3)
Focada em dados reais do portal CEAPS (Cota para Exercício da Atividade Parlamentar dos Senadores).

Dia 1: ETL & Data Cleaning

Tratamento de dados de 2008 a 2022.

Limpeza de valores nulos, correção de tipos de dados e formatação de valores monetários.

Dia 2: Análise Exploratória de Dados (EDA)

Investigação de padrões de gastos por senador, estado e tipo de despesa.

Visualização de dados com Matplotlib e Seaborn.

Dia 3: Time Series Forecasting

Implementação do algoritmo Prophet para prever gastos futuros.

Análise de erros (MAE) e tendências sazonais.

Parte 2: Recomendação e Produção (Dias 4 a 6)
Focada no dataset MovieLens para criar uma experiência personalizada.

Dia 4: Sistema de Recomendação

Construção de um modelo de clusterização utilizando K-Means.

Redução de dimensionalidade com PCA e normalização com StandardScaler.

Criação de uma função de recomendação baseada em distância euclidiana.

Dia 5: Integração & API (Deploy Simulado)

Desenvolvimento de uma infraestrutura de backend para consumir o modelo.

Arquivos em C# (.NET) para gestão de usuários e avaliações (RecomendacaoExtensions.cs, JsonModifica.cs).

Scripts de integração em Python (usuario.py, recomendacao.py) para conectar o modelo à API.

Dia 6: Teste A/B e Validação Estatística

Simulação de um teste A/B para validar a eficácia do modelo de recomendação.

Cálculo de Z-score, P-valor e intervalos de confiança para tomada de decisão baseada em dados.

🛠️ Tecnologias Utilizadas
Linguagens: Python, C#

Data Science: Pandas, NumPy, Scikit-Learn, Prophet.

Visualização: Matplotlib, Seaborn.

Engenharia/Backend: .NET Core (Minimal APIs), JSON Serialization, Requests.

Estatística: Testes de hipótese (A/B Testing).

📈 Resultados
Previsão de Gastos: Identificação de tendências de aumento com margem de erro mapeada.

Recomendação: Sistema capaz de sugerir 5 filmes semelhantes baseados no perfil de clusterização do usuário.

Validação: No teste A/B realizado no Dia 6, a análise estatística permitiu concluir se o novo modelo de recomendação trouxe impacto real nas conversões de vendas.