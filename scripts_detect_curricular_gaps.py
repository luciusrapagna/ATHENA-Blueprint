from src.analytics.curricular_gap_detector import CurricularGapDetector


def main():
    print("=" * 70)
    print("ATHENA Blueprint — DETECTOR DE LACUNAS CURRICULARES")
    print("=" * 70)

    print("\n[1] LENDO MATCH CURRICULAR TOP 3...")

    detector = CurricularGapDetector()

    print("\n[2] CALCULANDO MÉDIAS DE COMPATIBILIDADE POR AULA...")

    resumo, output_path = detector.detectar_lacunas()

    print("\n[3] LACUNAS DETECTADAS:\n")
    print(resumo)

    print("\n" + "=" * 70)
    print("DETECÇÃO DE LACUNAS FINALIZADA COM SUCESSO")
    print("=" * 70)

    print(f"\nArquivo gerado: {output_path}")


if __name__ == "__main__":
    main()
