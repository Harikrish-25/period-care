import { User, Order, Kit, Subscription } from '../types';
import { mockUsers, mockOrders, kits, mockSubscriptions } from '../data/mockData';

// Mock API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Auth service
export const authService = {
  async login(email: string, password: string): Promise<User | null> {
    await delay(1000);
    const user = mockUsers.find(u => u.email === email);
    if (user) {
      localStorage.setItem('currentUser', JSON.stringify(user));
      return user;
    }
    return null;
  },

  async register(userData: Omit<User, 'id' | 'role'>): Promise<User> {
    await delay(1000);
    const newUser: User = {
      ...userData,
      id: `user_${Date.now()}`,
      role: 'user'
    };
    mockUsers.push(newUser);
    return newUser;
  },

  logout() {
    localStorage.removeItem('currentUser');
  },

  getCurrentUser(): User | null {
    const stored = localStorage.getItem('currentUser');
    return stored ? JSON.parse(stored) : null;
  }
};

// Orders service
export const ordersService = {
  async createOrder(orderData: Omit<Order, 'id' | 'createdAt'>): Promise<Order> {
    await delay(500);
    const newOrder: Order = {
      ...orderData,
      id: `order_${Date.now()}`,
      createdAt: new Date().toISOString()
    };
    mockOrders.push(newOrder);
    return newOrder;
  },

  async getUserOrders(userId: string): Promise<Order[]> {
    await delay(300);
    return mockOrders.filter(order => order.userId === userId);
  },

  async getAllOrders(): Promise<Order[]> {
    await delay(300);
    return mockOrders;
  },

  async updateOrderStatus(orderId: string, status: Order['status']): Promise<Order> {
    await delay(300);
    const orderIndex = mockOrders.findIndex(o => o.id === orderId);
    if (orderIndex !== -1) {
      mockOrders[orderIndex].status = status;
      return mockOrders[orderIndex];
    }
    throw new Error('Order not found');
  }
};

// Kits service
export const kitsService = {
  async getAllKits(): Promise<Kit[]> {
    await delay(200);
    return kits;
  },

  async getKitById(id: string): Promise<Kit | null> {
    await delay(200);
    return kits.find(kit => kit.id === id) || null;
  }
};

// Subscriptions service
export const subscriptionsService = {
  async createSubscription(subData: Omit<Subscription, 'id'>): Promise<Subscription> {
    await delay(500);
    const newSub: Subscription = {
      ...subData,
      id: `sub_${Date.now()}`
    };
    mockSubscriptions.push(newSub);
    return newSub;
  },

  async getUserSubscription(userId: string): Promise<Subscription | null> {
    await delay(300);
    return mockSubscriptions.find(sub => sub.userId === userId && sub.isActive) || null;
  },

  async cancelSubscription(subId: string): Promise<void> {
    await delay(300);
    const subIndex = mockSubscriptions.findIndex(s => s.id === subId);
    if (subIndex !== -1) {
      mockSubscriptions[subIndex].isActive = false;
    }
  }
};