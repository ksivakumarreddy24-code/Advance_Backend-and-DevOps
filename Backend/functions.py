from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone, date
from typing import List, Optional
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel, Field


# DATABASE 


DB_PATH = "Warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Packages(Base):
    __tablename__ = "Packages"
    id = Column(Integer, primary_key=True)
    package_name = Column(String)
    destination = Column(String)
    weight = Column(Float)
    arrival_date = Column(Date)
    status = Column(String, default="pending")

class DispatchBatches(Base):
    __tablename__ = "DispatchBatches"
    id = Column(Integer, primary_key=True)
    vehicle = Column(String)
    destination = Column(String)
    dispatch_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.now)

class BatchPackages(Base):
    __tablename__ = "BatchPackages"
    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("DispatchBatches.id"), nullable=False)
    package_id = Column(Integer, ForeignKey("Packages.id"), nullable=False)

class User(Base):
    __tablename__ = "User"
    User_id = Column(Integer, primary_key=True)
    Username = Column(String, unique=True)
    Password = Column(String)

Base.metadata.create_all(engine)





ph = PasswordHasher()
ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_CODE = "UF47T437"
ALGORITHM = "HS256"

# add package
def add_package(package_name, destination, weight, arrival_date):
    session = Session(engine)
    package = Packages(package_name=package_name,destination=destination,weight=weight,arrival_date=arrival_date)
    session.add(package)
    session.commit()
    response = {
        "id": package.id,
        "package_name": package.package_name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date": package.arrival_date,
        "status": package.status
    }
    session.close()
    return response

# get package by id
def get_package_by_id(package_id):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == package_id).first()
    if package is not None:
        response = {
            "id": package.id,
            "package_name": package.package_name,
            "destination": package.destination,
            "weight": package.weight,
            "arrival_date": package.arrival_date,
            "status": package.status
        }
    else:
        response = None
    session.close()
    return response

# update package
def update_package(package_id, package_name=None, destination=None, weight=None, arrival_date=None, status=None):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == package_id).first()
    if package is None:
        session.close()
        return None
    if package_name is not None:
        package.package_name = package_name
    if destination is not None:
        package.destination = destination
    if weight is not None:
        package.weight = weight
    if arrival_date is not None:
        package.arrival_date = arrival_date
    if status is not None:
        package.status = status
    session.commit()
    response = {
        "id": package.id,
        "package_name": package.package_name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date": package.arrival_date,
        "status": package.status
    }
    session.close()
    return response


# delete package
def delete_package(package_id):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == package_id).first()
    if package is None:
        session.close()
        return "not_found"
    if package.status == "dispatched":
        session.close()
        return "dispatched"
    response = {
        "id": package.id,
        "package_name": package.package_name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date": package.arrival_date,
        "status": package.status
    }
    session.delete(package)
    session.commit()
    session.close()
    return response

# get all packages bt filter
def get_all_packages(destination=None, status=None, arrival_date=None):
    session = Session(engine)
    query = session.query(Packages)
    if destination is not None:
        query = query.filter(Packages.destination == destination)
    if status is not None:
        query = query.filter(Packages.status == status)
    if arrival_date is not None:
        query = query.filter(Packages.arrival_date == arrival_date)
    response = []
    for package in query.all():
        response.append({
            "id": package.id,
            "package_name": package.package_name,
            "destination": package.destination,
            "weight": package.weight,
            "arrival_date": package.arrival_date,
            "status": package.status
        })
    session.close()
    return response

# dispatch batches
def search_dispatch_batches(destination=None, vehicle=None, status=None):
    session = Session(engine)
    query = session.query(DispatchBatches)
    if destination:
        query = query.filter(DispatchBatches.destination == destination)
    if vehicle:
        query = query.filter(DispatchBatches.vehicle == vehicle)
    if status:
        query = query.filter(DispatchBatches.dispatch_status == status)
    results = []
    for batch in query.all():
        results.append({
            "batch_id": batch.id,
            "destination": batch.destination,
            "vehicle": batch.vehicle,
            "status": batch.dispatch_status
        })
    session.close()
    return results

# getting warehouse deatails
def get_warehouse_statistics():
    session = Session(engine)
    packages = session.query(Packages).all()
    total_received = len(packages)
    pending = 0
    dispatched = 0
    destination_count = {}
    for package in packages:
        if package.status == "pending":
            pending += 1
        if package.status == "dispatched":
            dispatched += 1
        if package.destination:
            destination_count[package.destination] = destination_count.get(package.destination, 0) + 1
    session.close()
    return {
        "total_received": total_received,
        "pending": pending,
        "dispatched": dispatched,
        "destination_wise_count": destination_count
    }

# create dispatch batch
def create_dispatch_batch(destination, vehicle, package_ids):
    session = Session(engine)
    if len(package_ids) == 0:
        session.close()
        return "no packages provided"
    for package_id in package_ids:
        package = session.query(Packages).filter(Packages.id == package_id).first()
        if package is None:
            session.close()
            return "package not found"
        if package.destination != destination:
            session.close()
            return "destination mismatch"
        if package.status in ["assigned", "dispatched"]:
            session.close()
            return "package already assigned or dispatched"
            
    batch = DispatchBatches(destination=destination,vehicle=vehicle,dispatch_status="planned")
    session.add(batch)
    session.commit()
    
    for package_id in package_ids:
        batch_package = BatchPackages(batch_id=batch.id, package_id=package_id)
        session.add(batch_package)
        package = session.query(Packages).filter(Packages.id == package_id).first()
        package.status = "assigned"
    session.commit()
    
    response = {
        "batch_id": batch.id,
        "destination": batch.destination,
        "vehicle": batch.vehicle,
        "status": batch.dispatch_status,
        "package_ids": package_ids
    }
    session.close()
    return response

# --------------- TOKEN ---------------

def create_token(username: str, token_type: str):
    time = REFRESH_TOKEN_EXPIRY 
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    return jwt.encode(payload=payload, key=SECRET_CODE, algorithm=ALGORITHM)

def verify_token(token: str, token_type: str = "access"):
    if not token:
        return False
    try:
        payload = jwt.decode(jwt=token, key=SECRET_CODE, algorithms=[ALGORITHM])
        if payload.get("token_type") == token_type:
            return payload.get("username")
        return False
    except jwt.PyJWTError:
        return False

def register_user(username: str, password: str):
    session = Session(engine)                                         
    user_exists = session.query(User).filter(User.Username == username).first()
    if user_exists is not None:
        session.close()
        return False
