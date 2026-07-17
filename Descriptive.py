import pandas as pd
import numpy as np


class Descriptive():
    def init(self):
        pass

    def segreQuanQual(self, dataset):
        quantative = []
        qualtative = []

        for i in dataset.columns:
            # pandas 3.0 defaults inferred text columns to a 'str' dtype
            # (not 'object'), so a plain `dtype == 'object'` check misses
            # them. is_numeric_dtype is robust across pandas versions.
            if pd.api.types.is_numeric_dtype(dataset[i]):
                quantative.append(i)
            else:
                qualtative.append(i)
        print("The Quantitative Data:", quantative)
        print("The Qualtitative Data", qualtative)
        return quantative, qualtative

    def descriptive_Analysis(self, dataset, quantative):
        rows = ["Null_count", "NonNull_count", "Total_Count", "Mean", "Median", "Mode",
                "Std", "Min", "Q1:25%", "Q2:50%", "Q3:75%", "Q4:100%", "IQR", "1.5Rule",
                "Lesser", "Greater"]
        des_data = pd.DataFrame(index=rows, columns=quantative)

        for i in quantative:
            col = dataset[i]
            desc = col.describe()

            mode_series = col.mode()
            mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan

            q1 = desc.get("25%", np.nan)
            q3 = desc.get("75%", np.nan)
            iqr = q3 - q1
            rule = 1.5 * iqr

            # Single .loc assignment per column avoids chained-assignment,
            # which silently fails to write under pandas' Copy-on-Write.
            des_data.loc[:, i] = [
                col.isnull().sum(),
                col.count(),
                len(col),
                col.mean(),
                col.median(),
                mode_val,
                desc.get("std", np.nan),
                desc.get("min", np.nan),
                q1,
                desc.get("50%", np.nan),
                q3,
                desc.get("max", np.nan),
                iqr,
                rule,
                q1 - rule,
                q3 + rule,
            ]
        return des_data

    def outliercolumn(self, quantative, des_data):
        lesser = []
        greater = []

        for i in quantative:
            if des_data.loc["Lesser", i] > des_data.loc["Min", i]:
                lesser.append(i)
            if des_data.loc["Greater", i] < des_data.loc["Q4:100%", i]:
                greater.append(i)

        print("Lesser Range", lesser)
        print("Greater Range", greater)
        return lesser, greater

    def changeoutlier(self, dataset, des_Data, lesser, greater):
        for i in lesser:
            threshold = des_Data.loc["Lesser", i]
            # IQR bounds are floats even for int columns; pandas 3.0 raises
            # on assigning a float into an int column instead of upcasting,
            # so cast first.
            if pd.api.types.is_integer_dtype(dataset[i]):
                dataset[i] = dataset[i].astype(float)
            dataset.loc[dataset[i] < threshold, i] = threshold
        for j in greater:
            threshold = des_Data.loc["Greater", j]
            if pd.api.types.is_integer_dtype(dataset[j]):
                dataset[j] = dataset[j].astype(float)
            dataset.loc[dataset[j] > threshold, j] = threshold
        return des_Data