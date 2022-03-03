import pandas as pd
import numpy as np


def create_df_from_dict(dictionary):
    values = next(iter(dictionary.values()))
    print(len(values))
    df = pd.DataFrame(data=dictionary, index=np.arange(len(values)))
    return df
