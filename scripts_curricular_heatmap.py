from src.analytics.curricular_heatmap import CurricularHeatmap


def main():
    print("=" * 70)
    print("ATHENA Blueprint — HEATMAP CURRICULAR INTELIGENTE")
    print("=" * 70)

    print("\n[1] LENDO MATCH TOP 3...")
    heatmap = CurricularHeatmap()

    print("\n[2] GERANDO MATRIZ QUESTAO x AULA...")
    matriz = heatmap.gerar_matriz_heatmap()

    print(f"Matriz gerada com {matriz.shape[0]} questões e {matriz.shape[1]} aulas.")

    print("\n[3] SALVANDO HEATMAP...")
    output_path = heatmap.salvar_heatmap(matriz)

    print("\n" + "=" * 70)
    print("HEATMAP CURRICULAR GERADO COM SUCESSO")
    print("=" * 70)

    print(f"\nArquivo gerado: {output_path}")


if __name__ == "__main__":
    main()
