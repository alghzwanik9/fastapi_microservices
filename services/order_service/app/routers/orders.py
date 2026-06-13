from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import httpx

from ..core.database import get_db
from ..core.config import get_settings
from ..models.order import Order, OrderItem
from ..schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
    OrderStatus
)
from common.utils.rabbitmq import publish_event

router = APIRouter(prefix="/orders", tags=["orders"])
settings = get_settings()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order with items."""
    total_amount = 0.0
    order_items = []

    # Fetch product details and calculate total
    async with httpx.AsyncClient() as client:
        for item in order_data.items:
            try:
                # Call product service to get product details
                response = await client.get(
                    f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{item.product_id}"
                )
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product {item.product_id} not found"
                    )
                product = response.json()

                # Check stock availability
                if product["stock"] < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for product {product['name']}"
                    )

                unit_price = product["price"]
                subtotal = unit_price * item.quantity
                total_amount += subtotal

                order_items.append({
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": unit_price,
                    "subtotal": subtotal
                })

            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Product service unavailable: {str(e)}"
                )

    # Create order
    db_order = Order(
        user_id=order_data.user_id,
        shipping_address=order_data.shipping_address,
        total_amount=total_amount,
        status="pending"
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Create order items
    for item_data in order_items:
        db_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_item)

        # Update product stock via product service
        async with httpx.AsyncClient() as client:
            try:
                await client.patch(
                    f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{item_data['product_id']}/stock",
                    params={"quantity": -item_data['quantity']}
                )
            except httpx.HTTPError:
                pass  # Log error but continue

    db.commit()
    db.refresh(db_order)

    # Publish order created event
    publish_event(
        "order.created",
        {
            "order_id": db_order.id,
            "user_id": db_order.user_id,
            "total_amount": db_order.total_amount,
            "status": db_order.status
        }
    )

    return db_order


@router.get("/", response_model=OrderListResponse)
def list_orders(
    page: int = 1,
    limit: int = 10,
    status_filter: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List all orders with pagination and filters."""
    query = db.query(Order)

    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    if user_id:
        query = query.filter(Order.user_id == user_id)

    total = query.count()
    orders = query.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return OrderListResponse(
        orders=orders,
        total=total,
        page=page,
        limit=limit
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    """Update an existing order."""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    # Publish order updated event
    publish_event(
        "order.updated",
        {
            "order_id": order.id,
            "status": order.status
        }
    )

    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order."""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return None


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, new_status: OrderStatus, db: Session = Depends(get_db)):
    """Update order status."""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = new_status.value
    db.commit()
    db.refresh(order)

    # Publish order status changed event
    publish_event(
        "order.status_changed",
        {
            "order_id": order.id,
            "old_status": order.status,
            "new_status": new_status.value
        }
    )

    return order
