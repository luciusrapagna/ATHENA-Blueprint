from src.reports.area_distribution_report import AreaDistributionReport


def main():
    print("=" * 70)
    print("ATHENA Blueprint — RELATÓRIOS DAS 5 GRANDES ÁREAS")
    print("=" * 70)

    gerador = AreaDistributionReport()

    resumo, anexo = gerador.gerar_relatorios()

    print("\nRELATÓRIOS GERADOS COM SUCESSO")
    print(f"\nResumo: {resumo}")
    print(f"Anexo: {anexo}")


if __name__ == "__main__":
    main()
