from src.reports.curricular_gap_report import CurricularGapReport


def main():

    print("=" * 70)
    print("ATHENA Blueprint — RELATÓRIO DE LACUNAS")
    print("=" * 70)

    print("\n[1] GERANDO RELATÓRIO WORD...")

    report = CurricularGapReport()

    output_path = report.gerar_relatorio()

    print("\n" + "=" * 70)
    print("RELATÓRIO GERADO COM SUCESSO")
    print("=" * 70)

    print(f"\nArquivo gerado:")
    print(output_path)


if __name__ == "__main__":
    main()
