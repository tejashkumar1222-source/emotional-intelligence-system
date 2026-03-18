def preprocess(df):
    df = df.copy()
    df['journal_text'] = df['journal_text'].fillna("")

    num_cols = ['sleep_hours','energy_level','stress_level','duration_min']
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    return df