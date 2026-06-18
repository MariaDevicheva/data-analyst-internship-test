from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error


DATA_PATH = Path("data/newborns_stats.csv")
RESULTS_DIR = Path("results")

RESULTS_DIR.mkdir(exist_ok=True)


# Загрузка данных
df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(
    df["year"].astype(str)
    + "-"
    + df["month"].astype(str)
    + "-01"
)

df = df.sort_values("date").reset_index(drop=True)


# Feature Engineering
df["time_index"] = np.arange(len(df))

df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

# Заполняем пропуски в c1 медианой
df["c1"] = df["c1"].fillna(df["c1"].median())


FEATURES = [
    "time_index",
    "month",
    "month_sin",
    "month_cos",
    "c1",
    "cat1",
]

X = df[FEATURES]
y = df["target"]

# Train/Test Split
# Последние 12 месяцев используем как тестовый период.
train_size = len(df) - 12

X_train = X.iloc[:train_size]
y_train = y.iloc[:train_size]

X_test = X.iloc[train_size:]
y_test = y.iloc[train_size:]

# Обучение модели
model = RandomForestRegressor(
    n_estimators=500,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

# Оценка качества на последних 12 месяцах
test_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, test_pred)
mape = mean_absolute_percentage_error(y_test, test_pred)

# Финальное обучение на всех данных
model.fit(X, y)

# Прогноз на следующие 12 месяцев
last_date = df["date"].max()

future_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=12,
    freq="MS"
)

future = pd.DataFrame({
    "date": future_dates
})

future["year"] = future["date"].dt.year
future["month"] = future["date"].dt.month
future["time_index"] = np.arange(len(df), len(df) + 12)

future["month_sin"] = np.sin(2 * np.pi * future["month"] / 12)
future["month_cos"] = np.cos(2 * np.pi * future["month"] / 12)

# Для будущих периодов используем медиану c1 и последнее известное значение cat1
future["c1"] = df["c1"].median()
future["cat1"] = df["cat1"].iloc[-1]

future_forecast = model.predict(future[FEATURES])

forecast = pd.DataFrame({
    "date": future_dates,
    "forecast_users": future_forecast.round().astype(int)
})


# Сохранение результатов
forecast.to_csv(
    RESULTS_DIR / "forecast.csv",
    index=False
)

metrics = pd.DataFrame({
    "metric": ["MAE", "MAPE"],
    "value": [round(mae, 2), round(mape, 4)]
})

metrics.to_csv(
    RESULTS_DIR / "model_metrics.csv",
    index=False
)

# Визуализация
plt.figure(figsize=(12, 6))

plt.plot(
    df["date"],
    df["target"],
    label="Исторические данные"
)

plt.plot(
    forecast["date"],
    forecast["forecast_users"],
    label="Прогноз"
)

plt.title("Прогноз пользователей на следующие 12 месяцев")
plt.xlabel("Дата")
plt.ylabel("Количество пользователей")
plt.grid()
plt.legend()

plt.savefig(
    RESULTS_DIR / "forecast_plot.png",
    bbox_inches="tight"
)

plt.close()



# Вывод
print("\nМодель: RandomForestRegressor")
print(f"MAE на тестовом периоде: {mae:.2f}")
print(f"MAPE на тестовом периоде: {mape:.2%}")

print("\nПрогноз сохранен:")
print("results/forecast.csv")

print("\nМетрики сохранены:")
print("results/model_metrics.csv")

print("\nГрафик сохранен:")
print("results/forecast_plot.png")

print("\nПрогноз на следующие 12 месяцев:")
print(forecast)