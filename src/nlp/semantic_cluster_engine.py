from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd


class SemanticClusterEngine:

    def __init__(self, n_clusters=5):

        self.n_clusters = n_clusters

    def gerar_clusters(self, embeddings):

        modelo = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init="auto"
        )

        clusters = modelo.fit_predict(embeddings)

        return clusters

    def reduzir_dimensionalidade(self, embeddings):

        pca = PCA(n_components=2)

        componentes = pca.fit_transform(embeddings)

        return componentes

    def criar_dataframe_cluster(
        self,
        dataframe,
        embeddings
    ):

        clusters = self.gerar_clusters(embeddings)

        componentes = self.reduzir_dimensionalidade(embeddings)

        resultado = dataframe.copy()

        resultado["cluster"] = clusters
        resultado["pca_x"] = componentes[:, 0]
        resultado["pca_y"] = componentes[:, 1]

        return resultado