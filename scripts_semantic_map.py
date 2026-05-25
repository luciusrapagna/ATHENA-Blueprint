import os
import pandas as pd
import plotly.express as px

ARQUIVO = "outputs/semantic/clusters_semanticos.xlsx"
SAIDA = "outputs/semantic/mapa_semantico_clusters.html"

df = pd.read_excel(ARQUIVO)

fig = px.scatter(
    df,
    x="pca_x",
    y="pca_y",
    color="cluster",
    hover_data=df.columns,
    title="ATHENA Blueprint | Mapa Semântico Curricular"
)

os.makedirs("outputs/semantic", exist_ok=True)

fig.write_html(SAIDA)

print(f"Mapa semântico salvo em: {SAIDA}")