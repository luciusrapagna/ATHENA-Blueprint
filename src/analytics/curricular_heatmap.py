import os
import pandas as pd
import matplotlib.pyplot as plt


class CurricularHeatmap:

    def __init__(self):
        pass

    def gerar_matriz_heatmap(
        self,
        top3_path="outputs/match/compatibilidade_curricular_top3.xlsx"
    ):
        df = pd.read_excel(top3_path)

        matriz = df.pivot_table(
            index="questao",
            columns="aula_compativel",
            values="compatibilidade_percentual",
            aggfunc="max"
        )

        matriz = matriz.fillna(0)

        return matriz

    def salvar_heatmap(
        self,
        matriz,
        output_path="outputs/figures/heatmap_curricular.png"
    ):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.figure(figsize=(12, 10))
        plt.imshow(matriz, aspect="auto")
        plt.colorbar(label="Compatibilidade curricular (%)")

        plt.title("ATHENA Blueprint — Heatmap de Compatibilidade Curricular")
        plt.xlabel("Aulas")
        plt.ylabel("Questões")

        plt.xticks(
            ticks=range(len(matriz.columns)),
            labels=matriz.columns,
            rotation=45,
            ha="right"
        )

        plt.yticks(
            ticks=range(len(matriz.index)),
            labels=matriz.index
        )

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        return output_path
