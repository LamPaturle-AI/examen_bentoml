import numpy as np
import bentoml
from bentoml import Context
from bentoml.io import JSON
from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta, timezone

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

# User credentials for authentication
USERS = {
    "max": "lamenace",
    "bob": "sinclair"
}

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/v1/models/gbr/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response
    
# Pydantic model to validate input data
class AdmissionInput(BaseModel):
    gre_score: int
    toefl_score: int
    university_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int

# Get the model from the Model Store
admissions_gbr_runner = bentoml.sklearn.get("admissions_gbr:latest").to_runner()

# Create a service API
gbr_service = bentoml.Service("gbr_service", runners=[admissions_gbr_runner])

# Add the JWTAuthMiddleware to the service
gbr_service.add_asgi_middleware(JWTAuthMiddleware)

# Create a login API endpoint for the service
@gbr_service.api(input=JSON(), output=JSON())
def login(credentials: dict, ctx: Context) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        ctx.response.status_code = 401
        return {"detail": "Invalid credentials"}
    
# Create a predict API endpoint for the service
@gbr_service.api(
    input=JSON(pydantic_model=AdmissionInput),
    output=JSON(),
    route='v1/models/gbr/predict'
)
async def classify(input_data: AdmissionInput, ctx: Context) -> dict:
    try:
        input_series = np.array([
            input_data.gre_score, 
            input_data.toefl_score, 
            input_data.university_rating, 
            input_data.sop,
            input_data.lor, 
            input_data.cgpa, 
            input_data.research
        ])
        
        result = await admissions_gbr_runner.predict.async_run(input_series.reshape(1, -1))

        return {
            "prediction": result.tolist(),
            "user": ctx.request.state.user if hasattr(ctx.request.state, "user") else None
        }

    except ValidationError as e:
        # Handle validation errors explicitly
        ctx.response.status_code = 422
        return {
            "error": "Invalid input data",
            "details": e.errors()
        }

    except Exception as e:
        # Handle other unexpected errors
        ctx.response.status_code = 500
        return {
            "error": "Internal Server Error",
            "details": str(e)
        }

# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token