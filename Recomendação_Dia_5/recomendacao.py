import pandas as pd
import numpy as np
import joblib
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

def recomendacao(usuario):
    modelo_recomendacao, df_filmes_avaliacao, df_avaliacao_modelo, df_filmes = prepara_modelo()

    # Prepara os filmes para a classificação com relação ao usuário
    filmes = df_filmes_avaliacao.reset_index().copy()
    filmes = filmes.drop(['rating', 'age', 'gender'], axis=1)

    usuario = pd.merge(usuario, filmes, on='item id')
    usuario = usuario.drop(['user id'], axis=1)
    clusteres = modelo_recomendacao.predict(usuario.drop(['item id'], axis=1))
    usuario['cluster'] = clusteres

    # Pega os melhores clusteres mais bem avaliados com base na quantidade e soma dos mais
    # bem avaliados filmes feitos pelo usuário com base na multiplicação deles
    melhor_cluster = usuario.drop(['age','gender', 'item id'], axis=1).copy()
    mais_assistidos = melhor_cluster[['cluster']].groupby('cluster').value_counts()
    melhor_cluster = melhor_cluster.groupby('cluster').sum()
    melhor_cluster['rating'] = melhor_cluster['rating'] * mais_assistidos

    # Preparação do próximo passo
    df_avaliacao_modelo['item id'] = df_filmes_avaliacao.index

    # Procura o cluster com pelo menos 5 filmes potenciais para recomendar ao usuário
    for incremento, _ in enumerate(melhor_cluster.sort_values('rating', ascending=False).index):
        # Pega o index dos melhores clusteres na ordem decrescente, pega o melhor filme e
        # por último pega o DataFrame e o índice dos filmes mais próximos
        cluster_index = melhor_cluster.sort_values('rating', ascending=False).index[incremento]

        id_melhor_filme = melhor_filme_cluster(cluster_index, usuario, df_filmes_avaliacao)
        filmes_cluster, top_filmes = mais_proximos(df_avaliacao_modelo, cluster_index, id_melhor_filme)

        # Se o usário ja viu o filme retira do DataFrame de filmes e se o DataFrame
        # tem 5 ou mais elementos, retorna os 5 filmes mais próximos
        for x in top_filmes:
            if x in usuario['item id']:
                 filmes_cluster = filmes_cluster[filmes_cluster['item id'] != x]
                 
        if len(filmes_cluster) >= 5:
            break

    df_filmes = df_filmes[df_filmes['movie id'].isin(filmes_cluster['item id'].head())]

    return df_filmes




def mais_proximos(df_avaliacao_modelo, cluster_index, id_filme):
    # Pega os filmes do cluster especifico retirando o filme que faremos a medicao e adiciona a coluna distancia
    filmes_cluster = df_avaliacao_modelo[df_avaliacao_modelo['cluster'] == cluster_index].copy()
    filmes_cluster = filmes_cluster[filmes_cluster["item id"] != id_filme]
    filmes_cluster = filmes_cluster.reset_index(drop=True)
    filmes_cluster['distancia'] = 0

    for linha in range(len(filmes_cluster['item id'])):
        # Pega o filme que faremos a medicao
        filme = df_avaliacao_modelo[df_avaliacao_modelo['item id'] == id_filme].copy()
        filme = filme.reset_index(drop=True)

        # Calcula a distancia euclidiana do nosso filme com o restante
        valor = []
        for coluna in filme.columns:
            if coluna not in ['item id', 'cluster', 'distancia']:
                valor.append(pow(filme.loc[0, coluna] - filmes_cluster.loc[linha, coluna], 2))

        filmes_cluster.loc[linha, 'distancia'] = np.sqrt(np.sum(valor))
    
    # Devolve os filmes em ordem crescente do mais proximos em ids
    filmes_cluster = filmes_cluster.sort_values('distancia').reset_index(drop=True)
    top_filmes = []
    for linha in range(len(filmes_cluster['item id'])):
        top_filmes.append(filmes_cluster.loc[linha, 'item id'])

    return filmes_cluster, top_filmes




def melhor_filme_cluster(cluster_index, usuario, df_filmes_avaliacao):
    # Separa o usuário com base no cluster escolhido
    usuario_modificado = usuario[usuario['cluster'] == cluster_index].copy()

    # Preparação para escolher o melhor filme
    somatorio = usuario_modificado.drop(['age','item id', 'gender'], axis=1).copy()
    somatorio['resultado'] = 0

    for linha in range(len(somatorio['rating'])):
        # Pega o id de cada filme e multiplica a coluna das avaliações
        # com base na média geral do filme
        id_filme = usuario_modificado.iloc[linha]['item id']
        somatorio.iloc[linha]['rating'] *= df_filmes_avaliacao.loc[id_filme, 'rating']

        # Soma todas as colunas de devolve o resultado
        somatorio.iloc[linha]['resultado'] = np.sum(somatorio.iloc[linha])

    # Implementa o resultado no DataFrame do usuário e escolhe o id do melhor filme
    # com base no maior resultado
    usuario_modificado['resultado'] = somatorio['resultado']
    id_melhor_filme = usuario_modificado.sort_values('resultado', ascending=False).iloc[0]['item id']

    return id_melhor_filme

#Preparatórios para as funções
#==========================================================================================================================================================

def prepara_modelo():
    # Prepara o DataFrame dos filmes
    df_filmes = pd.read_csv('../DS_Dia_4/u.item', sep='|', names=['movie id', 'movie title', 'release date', 'video release date',
                 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 
                 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
                 encoding='UTF-8')
    df_filmes_final = df_filmes.drop(['movie title', 'release date', 'video release date', 'IMDb URL'], axis=1).copy()
    df_filmes_final = df_filmes_final.rename(columns={'movie id': 'item id'})

    # Prepara o DataFrame dos usuários
    df_usuarios = pd.read_csv('../DS_Dia_4/u.user', sep='|', names=['user id', 'age', 'gender', 'occupation', 'zip code'], encoding='ISO-8859-1')
    df_usuarios = df_usuarios.drop(['zip code', 'occupation'], axis=1)

    # Prepara o DataFrame das avaliações
    df_avaliacoes = pd.read_csv('../DS_Dia_4/u.data', sep='\t', names=['user id', 'item id', 'rating', 'timestamp'], encoding='ISO-8859-1')
    df_avaliacoes = df_avaliacoes.drop('timestamp', axis=1)

    # Junta os DataFrames do usuario com o das avaliações
    df_user_aval = pd.merge(df_avaliacoes, df_usuarios, on='user id')
    df_user_aval['gender'] = df_user_aval['gender'].replace({'M': 1, 'F': 0})

    # Prepara o DataFrames para treino
    df_filmes_avaliacao = df_user_aval.copy()
    df_filmes_avaliacao = pd.merge(df_filmes_avaliacao, df_filmes_final, on='item id')
    df_filmes_avaliacao = df_filmes_avaliacao.drop(['user id'], axis=1)
    df_filmes_avaliacao = df_filmes_avaliacao.groupby('item id').mean()

    # Importa o modelo
    modelo_recomendacao = joblib.load('modelo_recomendacao.pkl')

    # Prepara o DataFrame baseado nos passos do modelo antes do KMeans e 
    # junta com suas predições
    df_avaliacao_modelo = modelo_recomendacao[:-1].transform(df_filmes_avaliacao)
    df_avaliacao_modelo = pd.DataFrame(data=df_avaliacao_modelo, columns=modelo_recomendacao.named_steps['pca'].get_feature_names_out()) 
    df_avaliacao_modelo['cluster'] = modelo_recomendacao.named_steps['kmeans'].labels_

    return modelo_recomendacao, df_filmes_avaliacao, df_avaliacao_modelo, df_filmes