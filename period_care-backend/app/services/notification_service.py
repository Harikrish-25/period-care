import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from app.config.settings import settings


class NotificationService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
    
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Send email notification"""
        try:
            if not self.smtp_username or not self.smtp_password:
                print(f"📧 Email to {to_email}: {subject}")
                print(body)
                print("=" * 50)
                return True  # Simulate success when no email config
            
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, 587)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_username, to_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        subject = "Welcome to Period Care! 🩷"
        body = f"""Dear {user_name},

Welcome to Period Care! We're excited to have you join our community of empowered women.

Your account has been successfully created. You can now:
• Browse our curated period care kits
• Customize your orders with fruits and nutrients
• Schedule convenient deliveries
• Manage your profile and orders

We're here to support your wellness journey every step of the way.

Stay comfortable, stay prepared! 💕

Best regards,
The Period Care Team

Visit us: {settings.frontend_url}"""
        
        return self.send_email(user_email, subject, body)
    
    def send_order_confirmation(self, user_email: str, user_name: str, order_details: dict) -> bool:
        """Send order confirmation email"""
        subject = f"Order Confirmation #{order_details.get('id')} - Period Care"
        body = f"""Dear {user_name},

Thank you for your order! We've received your Period Care order and are preparing it for delivery.

Order Details:
• Order ID: #{order_details.get('id')}
• Kit: {order_details.get('kit_name')}
• Total Amount: ₹{order_details.get('total_amount')}
• Delivery Date: {order_details.get('delivery_date')}
• Delivery Address: {order_details.get('delivery_address')}

We'll send you updates as your order is processed and shipped.

Thank you for choosing Period Care! 🩷

Best regards,
The Period Care Team"""
        
        return self.send_email(user_email, subject, body)
    
    def send_reminder_email(self, user_email: str, user_name: str, last_order_date: str) -> bool:
        """Send monthly reminder email"""
        subject = "Time for Your Period Care Reorder 🩷"
        body = f"""Dear {user_name},

It's been a month since your last Period Care order ({last_order_date}). 
Your period cycle might be approaching soon.

Don't let it catch you unprepared! Reorder your period care kit today and stay comfortable throughout your cycle.

Why reorder with us:
• High-quality, trusted products
• Customizable with fruits and nutrients
• Convenient home delivery
• Always ready when you need it

Reorder now: {settings.frontend_url}

Stay prepared, stay confident! 💕

Best regards,
The Period Care Team"""
        
        return self.send_email(user_email, subject, body)
    
    def send_admin_notification(self, subject: str, message: str) -> bool:
        """Send notification to admin"""
        admin_email = "admin@periodcare.com"  # You can make this configurable
        return self.send_email(admin_email, subject, message)
    
    def send_bulk_reminders(self, users_data: List[dict]) -> dict:
        """Send reminder emails to multiple users"""
        results = {
            "sent": 0,
            "failed": 0,
            "total": len(users_data)
        }
        
        for user in users_data:
            success = self.send_reminder_email(
                user.get('email'),
                user.get('name'),
                user.get('last_order_date')
            )
            
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results
