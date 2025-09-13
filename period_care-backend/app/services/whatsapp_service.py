import httpx
from typing import Optional
from app.config.settings import settings


class WhatsAppService:
    def __init__(self):
        self.admin_number = settings.admin_whatsapp_number
        # In production, you would use a proper WhatsApp Business API
        # For now, this is a placeholder implementation
    
    def send_message(self, message: str, phone_number: Optional[str] = None) -> bool:
        """Send WhatsApp message"""
        try:
            target_number = phone_number or self.admin_number
            
            # Placeholder implementation
            # In production, integrate with WhatsApp Business API or service like Twilio
            print(f"📱 WhatsApp Message to {target_number}:")
            print(message)
            print("=" * 50)
            
            # You would implement actual WhatsApp API call here
            # Example using a hypothetical WhatsApp service:
            # response = httpx.post(
            #     "https://api.whatsapp.com/send",
            #     json={
            #         "phone": target_number,
            #         "message": message
            #     },
            #     headers={"Authorization": f"Bearer {whatsapp_token}"}
            # )
            # return response.status_code == 200
            
            return True  # Simulate success
            
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
            return False
    
    def send_order_notification(self, order_details: dict) -> bool:
        """Send order notification to admin"""
        message = self._format_order_message(order_details)
        return self.send_message(message)
    
    def send_reminder_notification(self, user_details: dict) -> bool:
        """Send reminder notification to user"""
        message = self._format_reminder_message(user_details)
        return self.send_message(message, user_details.get("mobile"))
    
    def send_admin_reminder_alert(self, users_list: list) -> bool:
        """Send admin alert about users due for reminders"""
        message = self._format_admin_reminder_alert(users_list)
        return self.send_message(message)
    
    def _format_order_message(self, order: dict) -> str:
        """Format order notification message"""
        return f"""🩷 New Period Care Order 🩷

Order ID: {order.get('id')}
Customer: {order.get('customer_name')}
Mobile: {order.get('customer_mobile')}
Email: {order.get('customer_email')}
Kit Ordered: {order.get('kit_name')} (₹{order.get('kit_price')})
Selected Fruits: {order.get('fruits', 'None')}
Selected Nutrients: {order.get('nutrients', 'None')}
Order Date: {order.get('order_date')}
Delivery Date: {order.get('delivery_date')}
Delivery Address: {order.get('delivery_address')}
Total Amount: ₹{order.get('total_amount')}

Please prepare and confirm this order! 📦"""
    
    def _format_reminder_message(self, user: dict) -> str:
        """Format reminder message for user"""
        return f"""🩷 Period Care Reminder 🩷

Hi {user.get('name')}!

It's been a month since your last Period Care order. 
Your period cycle might be approaching soon.

Last Order: {user.get('last_kit_name')} on {user.get('last_order_date')}

Would you like to reorder your kit?
Visit our website: {settings.frontend_url}

Stay comfortable and prepared! 💕"""
    
    def _format_admin_reminder_alert(self, users: list) -> str:
        """Format admin reminder alert"""
        user_list = []
        for user in users:
            user_list.append(f"""- Name: {user.get('name')}
- Last Order: {user.get('last_kit_name')} on {user.get('last_order_date')}
- Mobile: {user.get('mobile')}
- Email: {user.get('email')}""")
        
        return f"""📋 Monthly Reminder Alert 📋

Users due for reorder reminder:

{chr(10).join(user_list)}

Total users: {len(users)}

Consider reaching out for personalized service! 🌟"""
