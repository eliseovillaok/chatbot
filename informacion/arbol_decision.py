import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz

df = pd.read_csv('e:/rasa_class/informacion/data_arbol_decision.csv')
df = df.drop(columns='id_usuario')

print(df.sample(5))
print('..................................')
print(df.info())
print('..................................')

# TRANSFORMAR LOS DATOS
df = pd.get_dummies(data=df, drop_first=False)
print(df.sample(5))


x = df.drop(columns='waze')  # features
y = df['waze']  # target
print('..................................')
print(x.info())
print('..................................')

# ENTRENAMIENTO DEL ARBOL DE DECISION

# Creacion del modelo
model = DecisionTreeClassifier(max_depth=4)
# Entrenamiento del modelo
model.fit(x, y)
# ¿Que tan bien predice?
print(model.score(x, y))

# VISUALIZACION DEL ARBOL

dot_data = tree.export_graphviz(model, out_file=None,
                                feature_names=x.columns.tolist(),
                                class_names=df['waze'].astype(
                                    str).unique().tolist(),
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("E:/rasa_class/informacion/arbolPreview")
