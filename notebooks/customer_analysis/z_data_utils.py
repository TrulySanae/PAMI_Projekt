import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer
from sklearn.utils import check_random_state


# Adult income dataset
def load_and_preprocess_adult_income_dataset(split_on, raw_data, split_on_values, random_state=None, max_samples=None,
                                             dataset_path=str, return_column_names=False):
    rng = check_random_state(random_state)
    # Drop not chosen categorical values to make following steps easier.
    if split_on_values != None:
        raw_data = raw_data[raw_data[split_on].isin(split_on_values)]

    # Attribute mit Kommazahlen auf 2 Nachkommastellen runden
    def round_floats(df):
        df_copy = df.copy()  # Erstelle eine Kopie des DataFrames, um die Warnung zu vermeiden
        for col in df_copy.columns:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy.loc[:, col] = df_copy[col].round(2)  # Verwende .loc, um den Wert zu setzen
        return df_copy

    # Aufruf der Funktion auf den Subset DataFrame
    raw_data = round_floats(raw_data)

    # Funktion , die binäre Variablen erkennt, damit preprocess_data() verwendet werden kann
    def binary_variables(df):
        binary_vars = []
        for col in df.columns:
            if df[col].nunique() == 2:  # Check if there are exactly two unique values
                binary_vars.append(col)
        return binary_vars

    binary_variables = binary_variables(raw_data)
    def preprocess_data(raw_data, binary_variables):
        new_data = raw_data.copy()
        binarizer = LabelBinarizer(neg_label=0, pos_label=1)
        # Binarizing the binary_variables:
        for binary_var in binary_variables:
            new_data[binary_var] = binarizer.fit_transform(raw_data[binary_var])
        return new_data

    processed_data = preprocess_data(raw_data, binary_variables)

    source_data = processed_data.query(f'{split_on}==0').drop(columns=split_on)
    target_data = processed_data.query(f'{split_on}==1').drop(columns=split_on)

    if max_samples == 'balanced':
        # balance the two datasets
        max_samples = min(source_data.shape[0], target_data.shape[0])

    n_positive_samples = min(max_samples, source_data.shape[0]) if max_samples is not None else source_data.shape[0]
    source_data = source_data.sample(n_positive_samples, replace=False, random_state=rng)

    n_negative_samples = min(max_samples, target_data.shape[0]) if max_samples is not None else target_data.shape[0]
    target_data = target_data.sample(n_negative_samples, replace=False, random_state=rng)

    source = source_data.to_numpy().astype(float)
    target = target_data.to_numpy().astype(float)

    print(f'Finished preprocessing {dataset_path}. ',
          f'Split on {split_on} with resulting source shape: {source.shape}, target shape: {target.shape}.')
    if return_column_names:
        return source, target, source_data.columns.to_list()
    else:
        return source, target