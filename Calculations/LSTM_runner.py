"""Utility script for running LSTM predictions across a range of settings.

This script iterates over rows of ``List_LSTM`` and performs ``LSTM_Calculation``
for each combination of hyperparameters. It records loss histories for
later analysis.

The code assumes that the following objects already exist in the runtime
environment:

``df``          -- ``pandas.DataFrame`` containing input data with ``Date`` and ``ME`` columns
``L``           -- iterable of labels
``List_LSTM``   -- ``pandas.DataFrame`` with rows "h", "term" and "e"
``LSTM_Calculation`` -- callable used to perform model training
``r_from``      -- integer index used for writing predictions back to ``df``

This file provides a clear implementation so the logic can be reused in
other projects.
"""

from __future__ import annotations

import time
from typing import List

import pandas as pd


FEATURES = [
    "HR5",
    "HR10",
    "HR20",
    "HR60",
    "SD20",
    "SD20_CDF20",
    "SD20_CDF60",
]


def run_lstm() -> pd.DataFrame:
    """Execute LSTM calculations and return a log DataFrame."""

    a = df.loc[df["Date"] == "2007-03-30"].index[0]
    b = df.loc[df["Date"] == "2025-04-30"].index[0]

    all_logs: List[List[float]] = []

    for j in range(List_LSTM.shape[1]):
        h = List_LSTM.loc["h", j]
        term = List_LSTM.loc["term", j]
        epochs = List_LSTM.loc["e", j]

        start = time.time()

        for i in range(a, b + 1):
            if df.at[i, "ME"] > 0:
                for label in L:
                    epoch_logs = LSTM_Calculation(i, label, FEATURES, term, h, epochs)
                    all_logs.extend(epoch_logs)
                    print(
                        label,
                        df.loc[i, "Date"],
                        round((time.time() - start) / 60, 1),
                        "Minutes",
                    )

        tmp_cols = [
            f"{label}_Y_Ret{term}_hl{h}_epochs{epochs}_pred" for label in L
        ]
        tmp = df.loc[r_from, tmp_cols]
        df.loc[r_from - 1, tmp_cols] = tmp
        df.loc[r_from - 2, tmp_cols] = tmp

    return pd.DataFrame(all_logs, columns=["Label", "Epoch", "TrainLoss", "ValLoss"])


if __name__ == "__main__":
    logs = run_lstm()
    print(logs.head())
