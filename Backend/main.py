from fastapi import FastAPI, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import functions
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"message": "Warehouse Dispatch API is running"}


# 1 - POST - Register a package
@app.post("/packages", status_code=201)
def add_package(package_name: str, destination: str, weight: float, arrival_date: date, token: str = Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")    
    if weight <= 0:
        raise HTTPException(status_code=422, detail="Weight must be greater than 0")
    return functions.add_package(package_name, destination, weight, arrival_date)


# 2 - GET - Get package by ID
@app.get("/packages/{package_id}")
def get_package(package_id: int, token: str = Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.get_package_by_id(package_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return result


# 3 - PATCH - Update package partially
@app.patch("/packages/{package_id}")
def update_package(
    package_id: int,
    package_name: str = None,
    destination: str = None,
    weight: float = None,
    arrival_date: date = None,
    status: str = None,
    token: str = Header(None)
):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    if status is not None and status not in ["pending", "dispatched"]:
        raise HTTPException(status_code=422, detail="Invalid status")
    result = functions.update_package(package_id, package_name, destination, weight, arrival_date, status)
    if result is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return result


# 4 - DELETE - Delete package if not dispatched
@app.delete("/packages/{package_id}")
def delete_package(package_id: int, token: str = Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.delete_package(package_id)
    if result == "not_found":
        raise HTTPException(status_code=404, detail="Package not found")
    if result == "dispatched":
        raise HTTPException(status_code=409, detail="Cannot delete a dispatched package")
    return result


# 5 - GET - Search and filter packages (Optional query params)
@app.get("/packages")
def search_packages(destination: str = None, status: str = None, arrival_date: date = None, token: str = Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    allowed_destination = ["banglore", "delhi", "mumbai", "japan", "america", "korea"]
    if destination is not None and destination.lower() not in allowed_destination:
        raise HTTPException(status_code=400, detail="Invalid destination")
    return functions.get_all_packages(destination=destination, status=status, arrival_date=arrival_date)

# 6 - Get - warehouse details
@app.get("/warehouse/statistics")
def warehouse_statistics(token = Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code = 401, detail = "Invalid or Expired token")
    statistics = functions.get_warehouse_statistics()
    return statistics


# 7 - Get - dispatch batches
@app.get("/dispatch-batches")
def get_dispatch_batches(destination=None, vehicle=None, status=None):
    batches = functions.search_dispatch_batches(destination,vehicle,status)
    return batches

@app.post("/dispatch-batches")
def create_dispatch_batch(
    destination: str = Body(),
    vehicle: str = Body(),
    package_ids: list[int] = Body(),
    token = Header(None)
):
    response = functions.create_dispatch_batch(destination,vehicle,package_ids)
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code = 401, detail = "Invalid or Expired token")
    if response == "no packages provided":
        raise HTTPException(status_code=400, detail="At least one package is required")
    if response == "duplicate package IDs":
        raise HTTPException(status_code=400, detail="Duplicate package IDs are not allowed")
    if response == "package not found":
        raise HTTPException(status_code=404, detail="One or more packages not found")
    if response == "destination mismatch":
        raise HTTPException(status_code=400, detail="All packages must have the same destination as the batch")
    if response == "package already assigned or dispatched":
        raise HTTPException(status_code=400, detail="One or more packages are already assigned or dispatched")
    return response


# --------------- AUTHENTICATION ENDPOINTS ---------------
@app.post("/register", status_code=201)
def register_user(username: str = Body(), password: str = Body()):
    if not functions.register_user(username=username, password=password):
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully"}


@app.post("/login")
def login(username: str = Body(), password: str = Body()):
    tokens = functions.verify_login(username=username, password=password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return tokens


@app.post("/refresh")
def refresh(refresh_token: str = Header(None)):
    # Make sure verify_token in functions.py uses token_type="refresh"
    username = functions.verify_token(token=refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = functions.create_token(username=username, token_type="access")
    return {"access_token": access_token} 
