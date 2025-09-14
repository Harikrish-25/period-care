import { Kit, Fruit, Nutrient, User, Order, Subscription, Benefit, Testimonial } from '../types';

export const kits: Kit[] = [
  {
    id: 'basic',
    name: 'Basic Care Kit',
    type: 'basic',
    basePrice: 299,
    image: 'https://via.placeholder.com/400x300/ff69b4/ffffff?text=Basic+Kit',
    includedItems: ['10 Regular Pads', 'Pain Relief Sachet', 'Hygiene Wipes'],
    description: 'Essential monthly care with comfort basics'
  },
  {
    id: 'medium',
    name: 'Comfort Care Kit',
    type: 'medium',
    basePrice: 499,
    image: 'https://via.placeholder.com/400x300/ff1493/ffffff?text=Comfort+Kit',
    includedItems: ['15 Ultra-Soft Pads', 'Pain Relief Sachets (3)', 'Hygiene Wipes', 'Comfort Balm'],
    description: 'Enhanced comfort with premium care essentials'
  },
  {
    id: 'premium',
    name: 'Premium Wellness Kit',
    type: 'premium',
    basePrice: 799,
    image: 'https://via.placeholder.com/400x300/c71585/ffffff?text=Premium+Kit',
    includedItems: ['20 Premium Pads', 'Pain Relief Sachets (5)', 'Hygiene Wipes', 'Comfort Balm', 'Heating Pad', 'Wellness Tea'],
    description: 'Complete wellness package with luxury comfort items'
  }
];

export const benefits: Benefit[] = [
  {
    id: 'pain-relief',
    title: 'Pain Relief Fruits',
    description: 'Natural ingredients that help reduce cramps and discomfort',
    icon: '🍎'
  },
  {
    id: 'custom-nutrients',
    title: 'Custom Nutrients',
    description: 'Supplements tailored to support your wellness during periods',
    icon: '💊'
  },
  {
    id: 'flexible-delivery',
    title: 'Flexible Delivery',
    description: 'Schedule deliveries that match your cycle perfectly',
    icon: '📅'
  },
  {
    id: 'premium-quality',
    title: 'Premium Quality',
    description: 'Only the best products for your comfort and health',
    icon: '⭐'
  }
];

export const testimonials: Testimonial[] = [
  {
    id: 'testimonial-1',
    name: 'Priya S.',
    rating: 5,
    text: 'The customizable kits are a game-changer! Love the fruit options and the convenience of delivery.',
    location: 'Mumbai'
  },
  {
    id: 'testimonial-2',
    name: 'Anita K.',
    rating: 5,
    text: 'Finally, a service that understands what women need. The nutrients really help with my symptoms.',
    location: 'Delhi'
  },
  {
    id: 'testimonial-3',
    name: 'Shreya M.',
    rating: 5,
    text: 'Subscription service is perfect. Never have to worry about running out of supplies again!',
    location: 'Bangalore'
  }
];

export const fruits: Fruit[] = [
  { id: 'apple', name: '🍎 Apple Slices', price: 50, benefits: 'Rich in fiber, helps with digestion' },
  { id: 'banana', name: '🍌 Banana Chips', price: 40, benefits: 'High potassium, reduces cramps' },
  { id: 'orange', name: '🍊 Orange Wedges', price: 60, benefits: 'Vitamin C boost, mood enhancement' },
  { id: 'berries', name: '🫐 Mixed Berries', price: 80, benefits: 'Antioxidants, natural pain relief' },
  { id: 'pomegranate', name: '🏮 Pomegranate', price: 70, benefits: 'Iron rich, energy boosting' },
  { id: 'dates', name: '🏺 Dates', price: 45, benefits: 'Natural sweetness, magnesium for cramps' }
];

export const nutrients: Nutrient[] = [
  { id: 'iron', name: 'Iron Supplement', price: 120, description: 'Combats fatigue and weakness' },
  { id: 'magnesium', name: 'Magnesium Complex', price: 150, description: 'Reduces cramps and muscle tension' },
  { id: 'calcium', name: 'Calcium + D3', price: 100, description: 'Bone health and mood support' },
  { id: 'omega3', name: 'Omega-3 Capsules', price: 180, description: 'Anti-inflammatory, mood regulation' },
  { id: 'vitamin_b', name: 'B-Complex', price: 90, description: 'Energy boost and hormonal balance' }
];

export const mockUsers: User[] = [
  {
    id: 'user1',
    name: 'Priya Sharma',
    email: 'priya@example.com',
    mobile: '+91 9876543210',
    address: 'Mumbai, Maharashtra',
    role: 'user'
  },
  {
    id: 'admin1',
    name: 'Admin User',
    email: 'admin@periodcare.com',
    mobile: '+91 9999999999',
    address: 'Delhi, India',
    role: 'admin'
  }
];

export const mockOrders: Order[] = [
  {
    id: 'order1',
    userId: 'user1',
    kitId: 'medium',
    selectedFruits: ['apple', 'berries'],
    selectedNutrients: ['iron', 'magnesium'],
    scheduledDate: '2025-02-15',
    address: 'Mumbai, Maharashtra',
    totalAmount: 769,
    status: 'pending',
    createdAt: '2025-01-15',
    isSubscription: false
  }
];

export const mockSubscriptions: Subscription[] = [
  {
    id: 'sub1',
    userId: 'user1',
    kitId: 'medium',
    selectedFruits: ['apple', 'berries'],
    selectedNutrients: ['iron'],
    type: 'monthly',
    nextDelivery: '2025-02-15',
    isActive: true,
    address: 'Mumbai, Maharashtra'
  }
];