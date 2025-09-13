from sqlalchemy.orm import Session
from typing import Optional, Dict, List
import json
from datetime import date
from app.crud import order as order_crud, kit as kit_crud, fruit as fruit_crud, nutrient as nutrient_crud, user as user_crud
from app.schemas.order import OrderCreate, OrderCalculation
from app.models.order import Order
from app.services.whatsapp_service import WhatsAppService
from app.services.notification_service import NotificationService


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.whatsapp_service = WhatsAppService()
        self.notification_service = NotificationService()
    
    def calculate_order_total(self, order_data: OrderCreate) -> Optional[OrderCalculation]:
        """Calculate total order amount"""
        # Get kit price
        kit = kit_crud.get_kit_by_id(self.db, order_data.kit_id)
        if not kit or not kit.is_available:
            return None
        
        kit_price = kit.base_price
        fruits_total = 0.0
        nutrients_total = 0.0
        breakdown = {
            "kit": {"name": kit.name, "price": kit_price},
            "fruits": [],
            "nutrients": []
        }
        
        # Calculate fruits total
        if order_data.selected_fruits:
            try:
                fruit_ids = json.loads(order_data.selected_fruits)
                for fruit_id in fruit_ids:
                    fruit = fruit_crud.get_fruit_by_id(self.db, fruit_id)
                    if fruit and fruit.is_available:
                        fruits_total += fruit.price
                        breakdown["fruits"].append({
                            "name": fruit.name,
                            "price": fruit.price
                        })
            except json.JSONDecodeError:
                pass
        
        # Calculate nutrients total
        if order_data.selected_nutrients:
            try:
                nutrient_ids = json.loads(order_data.selected_nutrients)
                for nutrient_id in nutrient_ids:
                    nutrient = nutrient_crud.get_nutrient_by_id(self.db, nutrient_id)
                    if nutrient and nutrient.is_available:
                        nutrients_total += nutrient.price
                        breakdown["nutrients"].append({
                            "name": nutrient.name,
                            "price": nutrient.price
                        })
            except json.JSONDecodeError:
                pass
        
        total_amount = kit_price + fruits_total + nutrients_total
        
        return OrderCalculation(
            kit_price=kit_price,
            fruits_total=fruits_total,
            nutrients_total=nutrients_total,
            total_amount=total_amount,
            breakdown=breakdown
        )
    
    def create_order(self, order_data: OrderCreate, user_id: int) -> Optional[Order]:
        """Create a new order"""
        # Calculate total
        calculation = self.calculate_order_total(order_data)
        if not calculation:
            return None
        
        # Create order
        order = order_crud.create_order(
            self.db, 
            order_data, 
            user_id, 
            calculation.total_amount
        )
        
        if order:
            # Update user's last order date
            user_crud.update_user_last_order_date(
                self.db, 
                user_id, 
                order.created_at.date()
            )
            
            # Send WhatsApp notification (async)
            self._send_order_notification(order.id)
        
        return order
    
    def _send_order_notification(self, order_id: int):
        """Send WhatsApp notification for new order"""
        try:
            order = order_crud.get_order_with_details(self.db, order_id)
            if order:
                message = self._format_order_message(order)
                success = self.whatsapp_service.send_message(message)
                
                if success:
                    order_crud.mark_whatsapp_sent(self.db, order_id)
        except Exception as e:
            print(f"Failed to send WhatsApp notification: {e}")
    
    def _format_order_message(self, order) -> str:
        """Format order message for WhatsApp"""
        # Parse fruits and nutrients
        fruits_list = "None"
        nutrients_list = "None"
        
        if order.selected_fruits:
            try:
                fruit_ids = json.loads(order.selected_fruits)
                fruits = []
                for fruit_id in fruit_ids:
                    fruit = fruit_crud.get_fruit_by_id(self.db, fruit_id)
                    if fruit:
                        fruits.append(f"{fruit.emoji_icon} {fruit.name} (₹{fruit.price})")
                fruits_list = ", ".join(fruits) if fruits else "None"
            except:
                pass
        
        if order.selected_nutrients:
            try:
                nutrient_ids = json.loads(order.selected_nutrients)
                nutrients = []
                for nutrient_id in nutrient_ids:
                    nutrient = nutrient_crud.get_nutrient_by_id(self.db, nutrient_id)
                    if nutrient:
                        nutrients.append(f"{nutrient.name} (₹{nutrient.price})")
                nutrients_list = ", ".join(nutrients) if nutrients else "None"
            except:
                pass
        
        message = f"""🩷 New Period Care Order 🩷

Order ID: {order.id}
Customer: {order.user.name}
Mobile: {order.user.mobile}
Email: {order.user.email}
Kit Ordered: {order.kit.name} (₹{order.kit.base_price})
Selected Fruits: {fruits_list}
Selected Nutrients: {nutrients_list}
Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}
Delivery Date: {order.scheduled_date}
Delivery Address: {order.delivery_address}
Total Amount: ₹{order.total_amount}

Please prepare and confirm this order! 📦"""
        
        return message
    
    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        """Update order status"""
        return order_crud.update_order_status(self.db, order_id, status)
    
    def get_order_details(self, order_id: int) -> Optional[Order]:
        """Get order with full details"""
        return order_crud.get_order_with_details(self.db, order_id)
    
    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders for a user"""
        return order_crud.get_user_orders(self.db, user_id, skip, limit)
    
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders (admin only)"""
        return order_crud.get_orders(self.db, skip, limit)
