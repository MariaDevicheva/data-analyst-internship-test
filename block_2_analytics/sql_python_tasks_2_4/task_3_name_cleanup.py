import pandas as pd

df = pd.DataFrame({
    "id": [1,2,3,4,5,6],
    "name": [
        "Александр",
        "Aлександр",
        "Мария",
        "Mария",
        "Сергей",
        "Cергей"
    ]
})

replacements = {
    "A": "А",
    "a": "а",
    "C": "С",
    "c": "с",
    "M": "М",
    "O": "О",
    "o": "о"
}

def normalize_name(name):
    for latin, cyr in replacements.items():
        name = name.replace(latin, cyr)
    return name.lower()

df["normalized_name"] = df["name"].apply(normalize_name)

df["new_id"] = (
    df.groupby("normalized_name")["id"]
    .transform("min")
)

print(df)

df.to_csv(
    "results/task_3_duplicates.csv",
    index=False
)