export interface User {
  id: string;
  name: string;
  email: string;
  mobile: string;
  address: string;
  role: 'user' | 'admin';
}

export interface Kit {
  id: string;
  name: string;
  type: 'basic' | 'medium' | 'premium';
  basePrice: number;
  image: string;
  includedItems: string[];
  description: string;
}

export interface Fruit {
  id: string;
  name: string;
  price: number;
  benefits: string;
}

export interface Nutrient {
  id: string;
  name: string;
  price: number;
  description: string;
}

export interface Order {
  id: string;
  userId: string;
  kitId: string;
  selectedFruits: string[];
  selectedNutrients: string[];
  scheduledDate: string;
  address: string;
  totalAmount: number;
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: string;
  isSubscription: boolean;
  subscriptionType?: 'monthly' | '6-month' | 'yearly';
}

export interface Benefit {
  id: string;
  title: string;
  description: string;
  icon: string;
}

export interface Testimonial {
  id: string;
  name: string;
  rating: number;
  text: string;
  location: string;
}

export interface Subscription {
  id: string;
  userId: string;
  kitId: string;
  selectedFruits: string[];
  selectedNutrients: string[];
  type: 'monthly' | '6-month' | 'yearly';
  nextDelivery: string;
  isActive: boolean;
  address: string;
}