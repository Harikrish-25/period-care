export const ADMIN_PHONE = '+919999999999'; // Configure this with actual admin WhatsApp number

export const generateWhatsAppLink = (orderSummary: string): string => {
  const message = `🩷 New Period Care Order 🩷\n\n${orderSummary}`;
  const encodedMessage = encodeURIComponent(message);
  return `https://wa.me/${ADMIN_PHONE}?text=${encodedMessage}`;
};

export const formatOrderSummary = (order: any, kit: any, user: any): string => {
  const fruitNames = order.selectedFruits.map((f: string) => 
    f.charAt(0).toUpperCase() + f.slice(1)
  ).join(', ');
  
  const nutrientNames = order.selectedNutrients.map((n: string) => 
    n.charAt(0).toUpperCase() + n.slice(1)
  ).join(', ');

  return `Order ID: ${order.id}
Customer: ${user.name}
Mobile: ${user.mobile}
Kit: ${kit.name} (₹${kit.basePrice})
Selected Fruits: ${fruitNames || 'None'}
Selected Nutrients: ${nutrientNames || 'None'}
Delivery Date: ${order.scheduledDate}
Address: ${order.address}
Total Amount: ₹${order.totalAmount}
${order.isSubscription ? `Subscription: ${order.subscriptionType}` : ''}

Please prepare and confirm this order! 📦`;
};