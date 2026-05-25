import os
import re
import pandas as pd


class LessonPlanReader:

    def __init__(self, pasta_planos="data/lesson_plans"):
        self.pasta_planos = pasta_planos

    def ler_txt(self, caminho):
        with open(caminho, "r", encoding="utf-8", errors="ignore") as arquivo:
            return arquivo.read()

    def dividir_por_aulas(self, texto, nome_arquivo):
        padrao = r"(Aula\s+\d+)"
        partes = re.split(padrao, texto, flags=re.IGNORECASE)

        registros = []

        if len(partes) <= 1:
            registros.append({
                "arquivo": nome_arquivo,
                "aula": "Plano completo",
                "texto_aula": texto
            })
            return registros

        for i in range(1, len(partes), 2):
            aula = partes[i].strip()
            conteudo = partes[i + 1].strip() if i + 1 < len(partes) else ""

            registros.append({
                "arquivo": nome_arquivo,
                "aula": aula,
                "texto_aula": conteudo
            })

        return registros

    def carregar_planos(self):
        registros = []

        for nome_arquivo in os.listdir(self.pasta_planos):
            if nome_arquivo.lower().endswith(".txt"):
                caminho = os.path.join(self.pasta_planos, nome_arquivo)
                texto = self.ler_txt(caminho)
                registros.extend(
                    self.dividir_por_aulas(texto, nome_arquivo)
                )

        return pd.DataFrame(registros)