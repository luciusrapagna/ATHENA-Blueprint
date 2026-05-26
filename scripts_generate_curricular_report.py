from src.reports.curricular_report import CurricularReportGenerator


def main():

    print("=" * 70)
    print("ATHENA Blueprint — RELATÓRIO CURRICULAR")
    print("=" * 70)

    print("\n[1] GERANDO RELATÓRIO WORD...")

    generator = CurricularReportGenerator()

    output_path = generator.gerar_relatorio()

    print("\n" + "=" * 70)
    print("RELATÓRIO GERADO COM SUCESSO")
    print("=" * 70)

    print(f"\nArquivo gerado:")
    print(output_path)


if __name__ == "__main__":
    main()
