from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/shipment")
def get_shipment1():
    return {
        "content": "wooden table",
        "status": "in transit",
    }


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


def root(number: int | float) -> float:
    return number**0.5


root(1)

shipments = {
    1: {"content": "wooden table", "status": "in transit", "weight": 1.2},
    2: {"content": "glassware", "status": "placed", "weight": 0.6},
    3: {"content": "office chair", "status": "dispatched", "weight": 3.5},
    4: {"content": "books", "status": "delivered", "weight": 2.1},
    5: {"content": "gaming laptop", "status": "packed", "weight": 1.8},
    6: {"content": "microwave oven", "status": "in transit", "weight": 6.0},
    7: {"content": "desk lamp", "status": "processing", "weight": 0.9},
}


@app.get("/shipment/latest")
def get_latest_shipment():
    latest_id = max(shipments.keys())  # 获取最大 ID
    return shipments[latest_id]  # 返回对应数据


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    # 判断给定 ID 是否存在
    if id not in shipments:
        return {"detail": f"Shipment with ID {id} does not exist"}
    return shipments[id]
