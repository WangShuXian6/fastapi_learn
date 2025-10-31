from typing import Any
from fastapi import FastAPI, HTTPException, status  as http_status
from scalar_fastapi import get_scalar_api_reference

# 示例发货数据
shipments = {
    1: {"content": "wooden table", "status": "in transit", "weight": 1.2},
    2: {"content": "glassware", "status": "placed", "weight": 0.6},
    3: {"content": "office chair", "status": "dispatched", "weight": 3.5},
    4: {"content": "books", "status": "delivered", "weight": 2.1},
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
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} does not exist",
        )
    return shipments[id]


# 路由：使用路径参数 + 查询参数
@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    # 如果 ID 不存在，抛出异常
    if id not in shipments:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} does not exist",
        )

    shipment = shipments[id]

    # 如果字段不存在，抛出异常
    if field not in shipment:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Field '{field}' does not exist in shipment data",
        )

    # 返回该字段对应的值
    return shipment[field]

@app.put("/shipment")
def shipment_update(
    id: int,
    content: str,
    weight: float,
    status: str,
) -> dict[str, Any]:
    # 检查该 ID 是否存在
    if id not in shipments:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} does not exist"
        )

    # 使用新数据替换旧数据
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status
    }

    # 返回更新后的记录
    return shipments[id]


@app.patch("/shipment")
def patch_shipment(id: int, body: dict[str, Any]) -> dict[str, Any]:
    # 检查 ID 是否存在
    if id not in shipments:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {id} does not exist"
        )

    shipment = shipments[id]

    # 使用 Python 的字典更新功能
    shipment.update(body)

    # 保存结果
    shipments[id] = shipment
    return shipment