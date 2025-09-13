import { User, Order, Kit, Fruit, Nutrient, Benefit, Testimonial } from '../types';

// Backend API configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Helper function for API calls
const apiCall = async (endpoint: string, options?: RequestInit) => {
  const token = localStorage.getItem('access_token');
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options?.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
};

// Auth service
export const authService = {
  async login(email: string, password: string): Promise<User> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(error.detail || 'Login failed');
    }

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    // Get user details
    const user = await this.getCurrentUser();
    localStorage.setItem('currentUser', JSON.stringify(user));
    return user;
  },

  async register(userData: {
    name: string;
    email: string;
    mobile: string;
    address: string;
    password: string;
  }): Promise<User> {
    const response = await apiCall('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });

    return response;
  },

  async logout() {
    try {
      await apiCall('/auth/logout', { method: 'POST' });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('currentUser');
    }
  },

  async getCurrentUser(): Promise<User> {
    return apiCall('/auth/me');
  },

  getCurrentUserFromStorage(): User | null {
    const stored = localStorage.getItem('currentUser');
    return stored ? JSON.parse(stored) : null;
  }
};

// Orders service
export const ordersService = {
  async createOrder(orderData: {
    kit_id: string;
    selected_fruits?: string;
    selected_nutrients?: string;
    scheduled_date: string;
    delivery_address: string;
  }): Promise<Order> {
    return apiCall('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData),
    });
  },

  async getUserOrders(): Promise<Order[]> {
    return apiCall('/users/orders');
  },

  async getAllOrders(): Promise<Order[]> {
    return apiCall('/orders/');
  },

  async updateOrderStatus(orderId: string, status: string): Promise<Order> {
    return apiCall(`/orders/${orderId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  },

  async getOrderById(orderId: string): Promise<Order> {
    return apiCall(`/orders/${orderId}`);
  }
};

// Kits service
export const kitsService = {
  async getAllKits(): Promise<Kit[]> {
    return apiCall('/kits/');
  },

  async getKitById(id: string): Promise<Kit> {
    return apiCall(`/kits/${id}`);
  },

  async createKit(kitData: Omit<Kit, 'id' | 'created_at' | 'updated_at'>): Promise<Kit> {
    return apiCall('/kits/', {
      method: 'POST',
      body: JSON.stringify(kitData),
    });
  },

  async updateKit(id: string, kitData: Partial<Kit>): Promise<Kit> {
    return apiCall(`/kits/${id}`, {
      method: 'PUT',
      body: JSON.stringify(kitData),
    });
  },

  async deleteKit(id: string): Promise<void> {
    return apiCall(`/kits/${id}`, {
      method: 'DELETE',
    });
  }
};

// Fruits service
export const fruitsService = {
  async getAllFruits(): Promise<Fruit[]> {
    return apiCall('/fruits/');
  },

  async createFruit(fruitData: Omit<Fruit, 'id' | 'created_at' | 'updated_at'>): Promise<Fruit> {
    return apiCall('/fruits/', {
      method: 'POST',
      body: JSON.stringify(fruitData),
    });
  },

  async updateFruit(id: string, fruitData: Partial<Fruit>): Promise<Fruit> {
    return apiCall(`/fruits/${id}`, {
      method: 'PUT',
      body: JSON.stringify(fruitData),
    });
  },

  async deleteFruit(id: string): Promise<void> {
    return apiCall(`/fruits/${id}`, {
      method: 'DELETE',
    });
  }
};

// Nutrients service
export const nutrientsService = {
  async getAllNutrients(): Promise<Nutrient[]> {
    return apiCall('/nutrients/');
  },

  async createNutrient(nutrientData: Omit<Nutrient, 'id' | 'created_at' | 'updated_at'>): Promise<Nutrient> {
    return apiCall('/nutrients/', {
      method: 'POST',
      body: JSON.stringify(nutrientData),
    });
  },

  async updateNutrient(id: string, nutrientData: Partial<Nutrient>): Promise<Nutrient> {
    return apiCall(`/nutrients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(nutrientData),
    });
  },

  async deleteNutrient(id: string): Promise<void> {
    return apiCall(`/nutrients/${id}`, {
      method: 'DELETE',
    });
  }
};

// CMS service
export const cmsService = {
  // Benefits
  async getAllBenefits(): Promise<Benefit[]> {
    return apiCall('/cms/benefits');
  },

  async createBenefit(benefitData: Omit<Benefit, 'id' | 'created_at' | 'updated_at'>): Promise<Benefit> {
    return apiCall('/cms/benefits', {
      method: 'POST',
      body: JSON.stringify(benefitData),
    });
  },

  async updateBenefit(id: string, benefitData: Partial<Benefit>): Promise<Benefit> {
    return apiCall(`/cms/benefits/${id}`, {
      method: 'PUT',
      body: JSON.stringify(benefitData),
    });
  },

  async deleteBenefit(id: string): Promise<void> {
    return apiCall(`/cms/benefits/${id}`, {
      method: 'DELETE',
    });
  },

  // Testimonials
  async getAllTestimonials(): Promise<Testimonial[]> {
    return apiCall('/cms/testimonials');
  },

  async createTestimonial(testimonialData: Omit<Testimonial, 'id' | 'created_at' | 'updated_at'>): Promise<Testimonial> {
    return apiCall('/cms/testimonials', {
      method: 'POST',
      body: JSON.stringify(testimonialData),
    });
  },

  async updateTestimonial(id: string, testimonialData: Partial<Testimonial>): Promise<Testimonial> {
    return apiCall(`/cms/testimonials/${id}`, {
      method: 'PUT',
      body: JSON.stringify(testimonialData),
    });
  },

  async deleteTestimonial(id: string): Promise<void> {
    return apiCall(`/cms/testimonials/${id}`, {
      method: 'DELETE',
    });
  }
};

// Admin service
export const adminService = {
  async getDashboardStats(): Promise<{
    total_orders: number;
    pending_orders: number;
    completed_orders: number;
    total_revenue: number;
    total_users: number;
  }> {
    return apiCall('/admin/dashboard/stats');
  },

  async getAllUsers(): Promise<User[]> {
    return apiCall('/admin/users');
  },

  async updateUserStatus(userId: string, isActive: boolean): Promise<User> {
    return apiCall(`/admin/users/${userId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ is_active: isActive }),
    });
  }
};

// Users service
export const usersService = {
  async getProfile(): Promise<User> {
    return apiCall('/users/profile');
  },

  async updateProfile(userData: Partial<User>): Promise<User> {
    return apiCall('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }
};