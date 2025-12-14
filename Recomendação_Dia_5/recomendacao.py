import pandas as pd
import joblib

def recomendacao(usuario):

    cluster_0, cluster_1, colunas, colunas_v, modelo_kmeans, df_avaliacoes, df_filmes, filme_copia = prepara_modelo()

    usuario_copia = usuario.copy()

    usuario = prepara_usuario(usuario, df_filmes, colunas, colunas_v)

    colunas_filmes = usuario[colunas_v]
    colunas_filmes.columns = colunas

    cluster_usuario = modelo_kmeans.predict(usuario)

    if cluster_usuario == 0:
        possiveis_filmes = colunas_filmes.multiply(cluster_0).round(2)
    else:
        possiveis_filmes = colunas_filmes.multiply(cluster_1).round(2)

    possiveis_filmes = pd.DataFrame(possiveis_filmes, columns=colunas)
    possiveis_filmes = possiveis_filmes.T.sort_values(by=0, ascending=False).head(3).T
    possiveis_filmes = possiveis_filmes.columns

    for i in range(3):

        filme = df_filmes[df_filmes[possiveis_filmes[i]] != 0].reset_index(drop=True)

        if i == 0:
            filmes = filme
        else:
            filmes = pd.concat([filmes, filme], axis=0)

    filmes = filmes.drop_duplicates().reset_index(drop=True)
    filmes = melhores_filmes(filmes, usuario, usuario_copia, possiveis_filmes, df_avaliacoes, filme_copia, colunas)

    return filmes



def prepara_usuario(usuario, df_filmes, colunas, colunas_v):
    filmes_avalicao = df_filmes.copy()

    usuario = pd.merge(usuario, filmes_avalicao, on='item id')
    usuario = usuario.drop(['item id','movie title'], axis=1)

    quantidade_total = usuario.groupby('user id').sum()[colunas]

    for i in range(4,23):
        usuario.iloc[:, i] = usuario.iloc[:, i] * usuario.iloc[:, 1]
        
    usuario = usuario.drop('rating', axis=1)
    
    avaliacao_total = usuario.groupby('user id').sum()[colunas]

    media_avaliacao = avaliacao_total.div(quantidade_total).round(2)
    media_avaliacao = media_avaliacao.fillna(0)

    quantidade_total.columns = colunas_v

    media_avaliacao = pd.concat([media_avaliacao, quantidade_total], axis=1).reset_index().drop('user id', axis=1)

    usuario = usuario.drop(columns=colunas)
    usuario = usuario.replace({'M': 1, 'F': 0})
    usuario = usuario.groupby('user id').mean().reset_index().drop('user id', axis=1)
    usuario = pd.concat([usuario, media_avaliacao], axis=1)
    usuario = usuario.drop(['age','unknown'], axis=1)

    return usuario



def melhores_filmes(filmes, usuario, usuario_copia, generos, df_avaliacoes, filme_copia, colunas):
    filmes_usuario = filmes[['item id']]

    filmes_avaliados = filme_copia.copy()
    avaliacoes = df_avaliacoes.copy()

    filmes_avaliados = pd.merge(avaliacoes, filmes_avaliados, on='item id')
    filmes_avaliados = pd.merge(filmes_avaliados, filmes_usuario, on='item id')

    quantidade = filmes_avaliados[['item id','movie title']].value_counts().to_frame()
    quantidade = quantidade.sort_values(by='item id').reset_index()

    avaliacoes = filmes_avaliados.groupby(['item id', 'movie title']).sum()[['rating']].reset_index()
    
    media_total = avaliacoes.iloc[:, 2].div(quantidade.iloc[:, 2]).round(2)

    avaliacoes = avaliacoes.drop('rating', axis=1)
    avaliacoes['rating_medio'] = media_total
    avaliacoes['total_avaliado'] = quantidade.iloc[:, 2]

    filmes_avaliados = filme_copia.copy()
    filmes_avaliados = filmes_avaliados.drop(['movie title', 'unknown'], axis=1)

    avaliacoes = pd.merge(avaliacoes, filmes_avaliados, on='item id')

    for i in range(len(avaliacoes['rating_medio'])):
        if avaliacoes.loc[i, generos[0]] != 0:
            avaliacoes.iloc[i, 2] = avaliacoes.iloc[i, 2] * usuario[f'v_{generos[0]}']
            avaliacoes.iloc[i, 3] = avaliacoes.iloc[i, 3] * usuario[generos[0]]

        elif avaliacoes.loc[i, generos[1]] != 0:
            avaliacoes.iloc[i, 2] = avaliacoes.iloc[i, 2] * usuario[f'v_{generos[1]}']
            avaliacoes.iloc[i, 3] = avaliacoes.iloc[i, 3] * usuario[generos[1]]

        else:
            avaliacoes.iloc[i, 2] = avaliacoes.iloc[i, 2] * usuario[f'v_{generos[2]}']
            avaliacoes.iloc[i, 3] = avaliacoes.iloc[i, 3] * usuario[generos[2]]

    avaliacoes['total'] = avaliacoes['rating_medio'] + avaliacoes['total_avaliado']
    avaliacoes = avaliacoes.drop(columns=colunas).drop(columns=['rating_medio','total_avaliado'])
    avaliacoes = avaliacoes.sort_values('total', ascending=False).reset_index(drop=True)

    
    filmes_vistos = usuario_copia['item id']
    filmes_vistos = filmes_vistos.to_frame()

    avaliacoes = avaliacoes[~avaliacoes['item id'].isin(filmes_vistos['item id'])]
    avaliacoes = avaliacoes.drop(['item id', 'total'], axis=1).reset_index(drop=True)

    filmes = avaliacoes.head(5)

    return filmes

#Preparatórios para as funções
#==========================================================================================================================================================

def prepara_modelo():
    df_filmes = pd.read_csv('H:\\GitHub\Python\\7DaysOfCode\\Ciência de Dados\\DS_Dia_4\\u.item', sep='|', names=['item id', 'movie title', 'release date', 'video release date',
                    'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 
                    'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
                    encoding='ISO-8859-1')

    df_filmes = df_filmes.drop(columns=['release date', 'video release date', 'IMDb URL'])

    df_usuarios = pd.read_csv('H:\\GitHub\Python\\7DaysOfCode\\Ciência de Dados\\DS_Dia_4\\u.user', sep='|', names=['user id', 'age', 'gender', 'occupation', 'zip code'], encoding='ISO-8859-1')
    df_usuarios = df_usuarios.drop(['zip code','occupation'], axis=1)

    df_avaliacoes = pd.read_csv('H:\\GitHub\Python\\7DaysOfCode\\Ciência de Dados\\DS_Dia_4\\u.data', sep='\t', names=['user id', 'item id', 'rating', 'timestamp'], encoding='ISO-8859-1')
    df_avaliacoes = df_avaliacoes.drop('timestamp', axis=1)

    df_user_aval = pd.merge(df_avaliacoes, df_usuarios, on='user id')
    df_user_aval['gender'] = df_user_aval['gender'].replace({'M': 1, 'F': 0})

    filme_copia = df_filmes.copy()
    df_treino = df_user_aval.copy()
    df_treino = pd.merge(df_treino, filme_copia, on='item id')
    df_treino = df_treino.drop(['item id','movie title'], axis=1)

    df_quantidade_filmes = df_treino.groupby('user id').sum()[['unknown', 'Action',
        'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
        'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]

    for i in range(4,23):
        df_treino.iloc[:, i] = df_treino.iloc[:,i]*df_treino.iloc[:, 1]

    df_treino = df_treino.drop('rating', axis=1)

    quantidade_filmes = df_treino.groupby('user id').sum()
    quantidade_filmes = quantidade_filmes.drop(['age', 'gender'], axis=1)

    quantidade_filmes = quantidade_filmes.div(df_quantidade_filmes).round(2)
    quantidade_filmes = quantidade_filmes.fillna(0)

    df_quantidade_filmes.columns = ['v_unknown', 'v_Action',
        'v_Adventure', 'v_Animation', 'v_Childrens', 'v_Comedy', 'v_Crime', 'v_Documentary',
        'v_Drama', 'v_Fantasy', 'v_Film-Noir', 'v_Horror', 'v_Musical', 'v_Mystery',
        'v_Romance', 'v_Sci-Fi', 'v_Thriller', 'v_War', 'v_Western']

    quantidade_filmes = pd.concat([quantidade_filmes, df_quantidade_filmes], axis=1)

    df_treino = df_treino.drop(['unknown', 'Action',
                                'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary',
                                'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                                'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'], axis=1)

    df_treino = df_treino.groupby('user id').mean()

    df_treino = pd.concat([df_treino, quantidade_filmes], axis=1)

    modelo_kmeans = joblib.load('modelo_kmeans.pkl')

    df_treino['cluster'] = modelo_kmeans.labels_

    cluster_media = df_treino.groupby('cluster').mean()

    colunas = ['Action', 'Adventure', 'Animation', 'Childrens', 'Comedy',
        'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
        'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    colunas_v = ['v_Action', 'v_Adventure', 'v_Animation', 'v_Childrens', 'v_Comedy',
        'v_Crime', 'v_Documentary', 'v_Drama', 'v_Fantasy', 'v_Film-Noir', 'v_Horror',
        'v_Musical', 'v_Mystery', 'v_Romance', 'v_Sci-Fi', 'v_Thriller', 'v_War', 'v_Western']

    cluster_0 = cluster_media.query('index == 0')[colunas]
    cluster_1 = cluster_media.query('index == 1')[colunas]

    cluster_0 = cluster_0.reset_index().drop('cluster', axis=1)
    cluster_1 = cluster_1.reset_index().drop('cluster', axis=1)

    return cluster_0, cluster_1, colunas, colunas_v, modelo_kmeans, df_avaliacoes, df_filmes, filme_copia