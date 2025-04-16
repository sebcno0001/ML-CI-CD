from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

# model dla danych wejściowych
class InputData(BaseModel):
    x: float

# trening modelu
model = LinearRegression()
X_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([2, 4, 6, 8, 10])
model.fit(X_train, y_train)


@app.post("/predict")
async def predict(request: Request):
    try:
        # próba pobrania danych 
        data = await request.json()
        
        # test czy x jest dostępny
        if 'x' not in data:
            return {"status": "error", "message": "Brak wymaganej wartości 'x'"}
        
        x_value = data['x']
        # przewidywanie
        prediction = model.predict([[x_value]])
        return {"status": "success", "message": "Działa poprawnie", "prediction": prediction.tolist()}
    
    except Exception as e:
        # inny błąd
        return {"status": "error", "message": "Coś poszło nie tak", "details": str(e)}

@app.get("/info")
async def get_model_info():
    model_info = {
        "typ_modelu": "LinearRegression",
        "cechy": X_train.shape[1],  # liczba cech w treningowym zbiorze danych
        "wspolczynniki": model.coef_.tolist(),  # współczynniki modelu
    }
    return model_info

@app.get("/health")
async def health_check():
    # czy serwer działa
    return {"status": "ok"}
