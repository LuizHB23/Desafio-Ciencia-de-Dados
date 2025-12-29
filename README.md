# 🚀 Desafio: 6 Dias de Ciência de Dados

Este repositório contém a resolução de um desafio intensivo de 6 dias, abrangendo desde a limpeza e análise de dados públicos até a implementação de modelos de Machine Learning com integração em sistemas externos e validação estatística.

Os arquivos foram pensados para serem portáteis, portanto é possível reproduzí-los com um clone.

---

## 📅 Estrutura do Desafio

O projeto foi dividido em duas grandes temáticas, utilizando datasets distintos para explorar diferentes facetas da Ciência de Dados.

### **Parte 1: Análise de Gastos Públicos (Dias 1 a 3)**
Focada nos dados do portal **CEAPS** (Cota para Exercício da Atividade Parlamentar dos Senadores), cobrindo o período de 2008 a 2022.

* **Dia 1 - ETL e Tratamento de Dados:** * Consolidação de múltiplos arquivos CSV.
    * Limpeza de valores nulos e tratamento de strings.
    * Conversão de tipos (Datas e Valores Monetários corrigidos para `float`).
* **Dia 2 - Análise Exploratória (EDA):** * Identificação dos senadores e partidos com maiores gastos.
    * Análise temporal de despesas ao longo dos anos.
    * Visualização de dados com Seaborn e Matplotlib.
* **Dia 3 - Previsão de Séries Temporais:** * Implementação do algoritmo **Prophet** (Facebook) para prever gastos futuros.
    * Avaliação de performance com métricas de erro (MAE).

### **Parte 2: Sistema de Recomendação e Produção (Dias 4 a 6)**
Utilização do dataset **MovieLens** para criar uma experiência personalizada de sugestão de filmes.

* **Dia 4 - Machine Learning (Clusterização):** * Processamento de dados com `StandardScaler` e Redução de Dimensionalidade com `PCA`.
    * Treinamento de modelo **K-Means** para segmentação de filmes.
    * Criação de motor de recomendação baseado em distância euclidiana.
* **Dia 5 - Engenharia e Integração (API):** * Desenvolvimento de uma infraestrutura em **C# (.NET)** para gerir utilizadores e avaliações.
    * Scripts de integração em **Python** (`usuario.py` e `recomendacao.py`) para consumir a API e gerar recomendações em tempo real.
* **Dia 6 - Teste A/B e Validação Estatística:** * Simulação de performance do modelo vs. site original.
    * Cálculo de **Z-score**, **P-valor** e intervalos de confiança.
    * Conclusão baseada em evidências estatísticas sobre a eficácia da recomendação nas conversões de vendas.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagens:** Python 3.x, C# (Backend), .NET 9.0.
* **Bibliotecas de Dados:** Pandas, NumPy, Scikit-Learn, Prophet.
* **Visualização:** Matplotlib, Seaborn.
* **Integração:** .NET Minimal APIs, Requests, JSON Serialization, Joblib.

---

## 📂 Arquivos no Repositório

| Arquivo | Descrição |
| :--- | :--- |
| `dia_1_dia_3.ipynb` | Notebook com ETL, EDA e Previsão de Gastos (Senado). |
| `dia_4.ipynb` | Notebook com a construção do modelo K-Means (MovieLens). |
| `Dia_6.ipynb` | Análise estatística e Teste A/B do modelo. |
| `recomendacao.py` | Lógica de predição e recomendação em Python. |
| `usuario.py` | Script cliente para interagir com a API e o modelo. |
| `*.cs` | Código fonte em C# para a API de gestão de utilizadores e dados. |

---

## 💡 Como Executar

1.  **Modelos:** Execute os notebooks para gerar o arquivo `modelo_recomendacao.pkl`.
2.  **API:** Inicie o serviço .NET para disponibilizar os endpoints de utilizadores.
3.  **Client:** Execute o `usuario.py` para inserir um ID de utilizador e receber as 5 recomendações de filmes.

---

**Projeto desenvolvido como parte de um desafio prático de Ciência de Dados.**




