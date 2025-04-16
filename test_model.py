from fastapi.testclient import TestClient
from app import app
import numpy as np

client = TestClient(app)

def test_predictions_not_none():
    """
    Test 1: Sprawdza, czy otrzymujemy jakąkolwiek predykcję.
    """
    response = client.post("/predict", json={"x": 4})
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    assert json_data["prediction"] is not None, "Prediction should not be None."

def test_predictions_length():
    """
    Test 2: Sprawdza, czy długość listy predykcji jest większa od 0 i równa 1 (bo podajemy jedno x).
    """
    response = client.post("/predict", json={"x": 3})
    prediction = response.json().get("prediction")
    assert isinstance(prediction, list)
    assert len(prediction) == 1, "Prediction list should contain exactly one value."

def test_predictions_value_range():
    """
    Test 3: Sprawdza, czy wartość predykcji mieści się w spodziewanym zakresie (dla x=1–5 to y=2–10).
    """
    for x in range(1, 6):  # testy dla x = 1..5
        response = client.post("/predict", json={"x": x})
        pred = response.json()["prediction"][0]
        assert 1.5 <= pred <= 10.5, f"Predicted value {pred} for x={x} is out of expected range."

def test_model_accuracy():
    """
    Test 4: Sprawdza, czy model przewiduje poprawnie dla zestawu testowego (accuracy >= 70%).
    """
    test_inputs = [1, 2, 3, 4, 5]
    expected_outputs = [2, 4, 6, 8, 10]
    correct = 0

    for x, expected in zip(test_inputs, expected_outputs):
        response = client.post("/predict", json={"x": x})
        pred = round(response.json()["prediction"][0])
        if pred == expected:
            correct += 1

    accuracy = correct / len(test_inputs)
    assert accuracy >= 0.7, f"Model accuracy is too low: {accuracy:.2f}"
