from src.pedagogical_match.lesson_plan_reader import LessonPlanReader

reader = LessonPlanReader()

df = reader.carregar_planos()

print(df.head())
print(f"Total de aulas detectadas: {len(df)}")