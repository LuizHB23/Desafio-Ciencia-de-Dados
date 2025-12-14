from recomendacao import recomendacao
import requests
import pandas as pd

text = requests.get('http://localhost:5163/usuario/256')

usuario = pd.read_json(text.text, encoding='UTF-8')

avaliacao = pd.json_normalize(usuario['avaliacao'])

usuario = usuario.join(avaliacao, how='left')

usuario.drop('avaliacao', axis=1, inplace=True)

usuario = usuario[['id', 'filmeId', 'nota', 'idade', 'genero']]

colunas = ['user id', 'item id', 'rating', 'age', 'gender']

usuario.columns = colunas

filmes = recomendacao(usuario)

print(filmes)

