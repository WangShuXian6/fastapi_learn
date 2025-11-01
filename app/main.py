from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .database import Database

db = Database()

# 新版 FastAPI 用一个 上下文管理器式的 lifespan 函数 来处理应用启动与关闭逻辑。
# ✅ Lifespan 写法（取代 on_event）
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App startup: connecting to database...")
    db.connect_to_db()
    db.create_table()
    yield   # 👈 应用运行阶段
    print("🛑 App shutdown: closing database...")
    db.close()

# ✅ 把 lifespan 传给 FastAPI 实例
app = FastAPI(lifespan=lifespan)

###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    # Return id for later use
    return {"id": new_id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    # Update data with given fields
    result = db.update(id, shipment)
    return result


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    # Remove from datastore
    db.delete(id)
    return {"detail": "Shipment deleted successfully."}


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
