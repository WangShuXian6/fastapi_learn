from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

shipments = {
    1: {"content": "wooden table", "status": "in transit", "weight": 1.2},
    2: {"content": "glassware", "status": "placed", "weight": 0.6},
    3: {"content": "office chair", "status": "dispatched", "weight": 3.5},
    4: {"content": "books", "status": "delivered", "weight": 2.1},
    5: {"content": "gaming laptop", "status": "packed", "weight": 1.8},
    6: {"content": "microwave oven", "status": "in transit", "weight": 6.0},
    7: {"content": "desk lamp", "status": "processing", "weight": 0.9},
}

app = FastAPI()


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} does not exist",
        )
    return shipments[id]

@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, int]:
    # 如果重量超过限制，抛出异常
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg",
        )

    # 计算新的 ID
    last_id = max(shipments.keys())
    new_id = last_id + 1

    # 构建新发货数据
    new_shipment = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }

    # 添加到数据字典中
    shipments[new_id] = new_shipment

    # 返回新创建的 ID
    return {"id": new_id}
