from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

shipments = {
    1: {"content": "wooden table", "status": "in transit", "weight": 1.2},
    2: {"content": "glassware", "status": "placed", "weight": 0.6},
    3: {"content": "office chair", "status": "dispatched", "weight": 3.5},
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
def submit_shipment(weight: float, data: dict[str, str]) -> dict[str, Any]:
    content = data["content"]

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg",
        )

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }
    return {"id": new_id}
