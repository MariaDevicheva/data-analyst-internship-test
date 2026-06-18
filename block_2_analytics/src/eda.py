import pandas as pd
import matplotlib.pyplot as plt


# Загрузка данных
df = pd.read_csv("data/newborns_stats.csv")

# создаем дату
df["date"] = pd.to_datetime(
    df["year"].astype(str)
    + "-"
    + df["month"].astype(str)
    + "-01"
)

# Общая информация
print("\nИНФОРМАЦИЯ О ДАТАСЕТЕ")
print(f"Количество строк: {df.shape[0]}")
print(f"Количество столбцов: {df.shape[1]}")

print("\nТипы данных:")
print(df.dtypes)


# Пропуски
print("\nПРОПУЩЕННЫЕ ЗНАЧЕНИЯ")
print(df.isna().sum())


# Статистика target
print("\nОПИСАТЕЛЬНАЯ СТАТИСТИКА TARGET")
print(df["target"].describe())

# Среднее по годам
print("\nСРЕДНЕЕ ЗНАЧЕНИЕ TARGET ПО ГОДАМ")
year_stats = (
    df.groupby("year")["target"]
    .mean()
    .round(2)
)

print(year_stats)

# График динамики
plt.figure(figsize=(12, 6))

plt.plot(
    df["date"],
    df["target"]
)

plt.title("Динамика количества пользователей")
plt.xlabel("Дата")
plt.ylabel("Target")
plt.grid()

plt.savefig(
    "results/eda_target_trend.png",
    bbox_inches="tight"
)

plt.close()

print("\nГрафик сохранен:")
print("results/eda_target_trend.png")