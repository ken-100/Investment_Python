import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def prepare_data(df: pd.DataFrame, window: int = 60, horizon: int = 20):
    """Prepare LSTM inputs and labels from a price DataFrame."""
    data = df[['Date', 'ES']].copy()
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values('Date', inplace=True)
    values = data['ES'].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(values)

    X, y = [], []
    for i in range(window, len(scaled) - horizon + 1):
        X.append(scaled[i - window:i])
        future_return = (scaled[i + horizon - 1] - scaled[i - 1])[0]
        y.append(future_return)

    X = np.array(X)
    y = np.array(y)
    return X, y, scaler, data['Date'].iloc[window:len(scaled)-horizon+1].reset_index(drop=True)


def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model


def predict_returns(df: pd.DataFrame, window: int = 60, horizon: int = 20, epochs: int = 20):
    """Train an LSTM on price data and predict expected returns."""
    X, y, scaler, dates = prepare_data(df, window, horizon)
    model = build_model((window, 1))
    model.fit(X, y, epochs=epochs, batch_size=32, verbose=0)
    preds = model.predict(X, verbose=0)
    return pd.DataFrame({
        'Date': dates,
        f'Expected_Return_{horizon}d': preds[:, 0]
    })


if __name__ == '__main__':
    # Example usage:
    # df = pd.read_csv('es_prices.csv')
    # result = predict_returns(df)
    # print(result.head())
    pass

