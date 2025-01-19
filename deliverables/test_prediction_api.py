import requests

# JWT configuration – must match your service's configuration
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

# Input data for prediction endpoint with valid types
valid_input_data = {
    "gre_score": 320,
    "toefl_score": 110,
    "university_rating": 4,
    "sop": 4.0,
    "lor": 4.0,
    "cgpa": 9.0,
    "research": 1
}

def test_prediction_no_token(base_url):
    """Verify that the prediction API returns 401 if JWT token is missing."""
    response = requests.post(f"{base_url}/v1/models/gbr/predict", json=valid_input_data)
    assert response.status_code == 401

def test_prediction_valid_input(base_url, headers):
    """Verify that the prediction API returns a valid prediction for correct input data with a valid JWT."""
    response = requests.post(f"{base_url}/v1/models/gbr/predict", headers=headers, json=valid_input_data)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)

def test_prediction_invalid_input(base_url, headers):
    """Verify that the prediction API returns a 400 error Bad Request for invalid input data."""
    invalid_input_data = valid_input_data.copy()
    invalid_input_data["gre_score"] = "invalid"  # Introduce invalid data type
    
    response = requests.post(f"{base_url}/v1/models/gbr/predict", headers=headers, json=invalid_input_data)
    # FastAPI should return 400 for a validation error
    assert response.status_code == 400
