import os
import pandas as pd


class CurricularGapDetector:

    def __init__(self):
        pass

    def classificar_status(self, media):
        if media >= 70:
            return "Forte aderência curricular"
        elif media >= 50:
            return "Aderência moderada"
        elif media >= 35:
            return "Aderência baixa"
        else:
            return "Lacuna curricular crítica"

    def gerar_recomendacao(self, status):
        if status == "Forte aderência curricular":
            return "Manter a integração atual entre questões e plano de aula."
        elif status == "Aderência moderada":
            return "Revisar parcialmente a distribuição das questões e reforçar alinhamento pedagógico."
        elif status == "Aderência baixa":
            return "Recomenda-se revisão curricular e ampliação de questões relacionadas ao conteúdo."
        else:
            return "Priorizar intervenção do NDE, revisão do plano de ensino e inclusão de questões alinhadas ao conteúdo."

    def detectar_lacunas(
        self,
        match_path="outputs/match/compatibilidade_curricular_top3.xlsx",
        output_path="outputs/analytics/lacunas_curriculares.xlsx"
    ):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df = pd.read_excel(match_path)

        resumo = (
            df.groupby("aula_compativel")
            .agg(
                media_compatibilidade=("compatibilidade_percentual", "mean"),
                maior_compatibilidade=("compatibilidade_percentual", "max"),
                menor_compatibilidade=("compatibilidade_percentual", "min"),
                total_associacoes=("questao", "count"),
                questoes_unicas=("questao", "nunique")
            )
            .reset_index()
        )

        resumo["media_compatibilidade"] = resumo["media_compatibilidade"].round(2)
        resumo["maior_compatibilidade"] = resumo["maior_compatibilidade"].round(2)
        resumo["menor_compatibilidade"] = resumo["menor_compatibilidade"].round(2)

        resumo["status_curricular"] = resumo["media_compatibilidade"].apply(
            self.classificar_status
        )

        resumo["recomendacao_pedagogica"] = resumo["status_curricular"].apply(
            self.gerar_recomendacao
        )

        resumo = resumo.sort_values(
            by="media_compatibilidade",
            ascending=True
        )

        resumo.to_excel(output_path, index=False)

        return resumo, output_path
