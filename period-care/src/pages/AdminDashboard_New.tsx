import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart3, Package, Users, TrendingUp, Calendar, CheckCircle, XCircle, Clock,
  Edit, Trash2, Plus, Save, X, Settings, MessageSquare, Star
} from 'lucide-react';
import { ordersService } from '../services/mockApi';
import { Order, Kit, Benefit, Testimonial } from '../types';
import { kits as initialKits, benefits as initialBenefits, testimonials as initialTestimonials } from '../data/mockData';

// Kit Edit Form Component
const KitForm: React.FC<{
  kit?: Kit;
  onSave: (kit: Kit) => void;
  onCancel: () => void;
}> = ({ kit, onSave, onCancel }) => {
  const [formData, setFormData] = useState<Kit>(
    kit || {
      id: '',
      name: '',
      type: 'basic',
      basePrice: 0,
      image: '',
      includedItems: [],
      description: ''
    }
  );
  const [itemsText, setItemsText] = useState(kit?.includedItems.join(', ') || '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      ...formData,
      includedItems: itemsText.split(',').map(item => item.trim())
    });
  };

  return (
    <motion.form
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-xl shadow-lg border"
    >
      <h3 className="text-lg font-semibold mb-4">{kit ? 'Edit Kit' : 'Add New Kit'}</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <input
          type="text"
          placeholder="Kit Name"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          required
        />
        
        <select
          value={formData.type}
          onChange={(e) => setFormData(prev => ({ ...prev, type: e.target.value as any }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
        >
          <option value="basic">Basic</option>
          <option value="medium">Medium</option>
          <option value="premium">Premium</option>
        </select>
        
        <input
          type="number"
          placeholder="Base Price"
          value={formData.basePrice}
          onChange={(e) => setFormData(prev => ({ ...prev, basePrice: Number(e.target.value) }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          required
        />
        
        <input
          type="url"
          placeholder="Image URL"
          value={formData.image}
          onChange={(e) => setFormData(prev => ({ ...prev, image: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
        />
      </div>
      
      <textarea
        placeholder="Description"
        value={formData.description}
        onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent mb-4"
        rows={3}
        required
      />
      
      <textarea
        placeholder="Included Items (comma separated)"
        value={itemsText}
        onChange={(e) => setItemsText(e.target.value)}
        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent mb-4"
        rows={2}
      />
      
      <div className="flex space-x-3">
        <motion.button
          type="submit"
          className="flex items-center space-x-2 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Save className="w-4 h-4" />
          <span>Save</span>
        </motion.button>
        
        <motion.button
          type="button"
          onClick={onCancel}
          className="flex items-center space-x-2 bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <X className="w-4 h-4" />
          <span>Cancel</span>
        </motion.button>
      </div>
    </motion.form>
  );
};

// Benefit Form Component
const BenefitForm: React.FC<{
  benefit?: Benefit;
  onSave: (benefit: Benefit) => void;
  onCancel: () => void;
}> = ({ benefit, onSave, onCancel }) => {
  const [formData, setFormData] = useState<Benefit>(
    benefit || { id: '', title: '', description: '', icon: '' }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <motion.form
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-xl shadow-lg border"
    >
      <h3 className="text-lg font-semibold mb-4">{benefit ? 'Edit Benefit' : 'Add New Benefit'}</h3>
      
      <div className="grid grid-cols-1 gap-4 mb-4">
        <input
          type="text"
          placeholder="Title"
          value={formData.title}
          onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          required
        />
        
        <input
          type="text"
          placeholder="Icon (emoji)"
          value={formData.icon}
          onChange={(e) => setFormData(prev => ({ ...prev, icon: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          required
        />
        
        <textarea
          placeholder="Description"
          value={formData.description}
          onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
          className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          rows={3}
          required
        />
      </div>
      
      <div className="flex space-x-3">
        <motion.button
          type="submit"
          className="flex items-center space-x-2 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Save className="w-4 h-4" />
          <span>Save</span>
        </motion.button>
        
        <motion.button
          type="button"
          onClick={onCancel}
          className="flex items-center space-x-2 bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <X className="w-4 h-4" />
          <span>Cancel</span>
        </motion.button>
      </div>
    </motion.form>
  );
};

// Testimonial Form Component
const TestimonialForm: React.FC<{
  testimonial?: Testimonial;
  onSave: (testimonial: Testimonial) => void;
  onCancel: () => void;
}> = ({ testimonial, onSave, onCancel }) => {
  const [formData, setFormData] = useState<Testimonial>(
    testimonial || { id: '', name: '', rating: 5, text: '', location: '' }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <motion.form
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-xl shadow-lg border"
    >
      <h3 className="text-lg font-semibold mb-4">{testimonial ? 'Edit Testimonial' : 'Add New Testimonial'}</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <input
          type="text"
          placeholder="Name"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          required
        />
        
        <input
          type="text"
          placeholder="Location"
          value={formData.location}
          onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          required
        />
        
        <select
          value={formData.rating}
          onChange={(e) => setFormData(prev => ({ ...prev, rating: Number(e.target.value) }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
        >
          <option value={5}>5 Stars</option>
          <option value={4}>4 Stars</option>
          <option value={3}>3 Stars</option>
          <option value={2}>2 Stars</option>
          <option value={1}>1 Star</option>
        </select>
      </div>
      
      <textarea
        placeholder="Testimonial Text"
        value={formData.text}
        onChange={(e) => setFormData(prev => ({ ...prev, text: e.target.value }))}
        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent mb-4"
        rows={4}
        required
      />
      
      <div className="flex space-x-3">
        <motion.button
          type="submit"
          className="flex items-center space-x-2 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Save className="w-4 h-4" />
          <span>Save</span>
        </motion.button>
        
        <motion.button
          type="button"
          onClick={onCancel}
          className="flex items-center space-x-2 bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <X className="w-4 h-4" />
          <span>Cancel</span>
        </motion.button>
      </div>
    </motion.form>
  );
};

const AdminDashboard: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [kits, setKits] = useState<Kit[]>(initialKits);
  const [benefits, setBenefits] = useState<Benefit[]>(initialBenefits);
  const [testimonials, setTestimonials] = useState<Testimonial[]>(initialTestimonials);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed' | 'cancelled'>('all');
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'orders' | 'kits' | 'content'>('orders');
  
  // Edit states
  const [editingKit, setEditingKit] = useState<Kit | null>(null);
  const [editingBenefit, setEditingBenefit] = useState<Benefit | null>(null);
  const [editingTestimonial, setEditingTestimonial] = useState<Testimonial | null>(null);
  const [showAddKit, setShowAddKit] = useState(false);
  const [showAddBenefit, setShowAddBenefit] = useState(false);
  const [showAddTestimonial, setShowAddTestimonial] = useState(false);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const allOrders = await ordersService.getAllOrders();
      setOrders(allOrders);
    } catch (error) {
      console.error('Failed to load orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (orderId: string, status: Order['status']) => {
    try {
      await ordersService.updateOrderStatus(orderId, status);
      setOrders(prev => prev.map(order => 
        order.id === orderId ? { ...order, status } : order
      ));
    } catch (error) {
      console.error('Failed to update order status:', error);
    }
  };

  // Kit Management Functions
  const handleKitSave = (kit: Kit) => {
    if (editingKit) {
      setKits(prev => prev.map(k => k.id === kit.id ? kit : k));
    } else {
      setKits(prev => [...prev, { ...kit, id: Date.now().toString() }]);
    }
    setEditingKit(null);
    setShowAddKit(false);
  };

  const handleKitDelete = (kitId: string) => {
    setKits(prev => prev.filter(k => k.id !== kitId));
  };

  // Benefit Management Functions
  const handleBenefitSave = (benefit: Benefit) => {
    if (editingBenefit) {
      setBenefits(prev => prev.map(b => b.id === benefit.id ? benefit : b));
    } else {
      setBenefits(prev => [...prev, { ...benefit, id: Date.now().toString() }]);
    }
    setEditingBenefit(null);
    setShowAddBenefit(false);
  };

  const handleBenefitDelete = (benefitId: string) => {
    setBenefits(prev => prev.filter(b => b.id !== benefitId));
  };

  // Testimonial Management Functions
  const handleTestimonialSave = (testimonial: Testimonial) => {
    if (editingTestimonial) {
      setTestimonials(prev => prev.map(t => t.id === testimonial.id ? testimonial : t));
    } else {
      setTestimonials(prev => [...prev, { ...testimonial, id: Date.now().toString() }]);
    }
    setEditingTestimonial(null);
    setShowAddTestimonial(false);
  };

  const handleTestimonialDelete = (testimonialId: string) => {
    setTestimonials(prev => prev.filter(t => t.id !== testimonialId));
  };

  const filteredOrders = orders.filter(order => 
    filter === 'all' ? true : order.status === filter
  );

  const stats = {
    total: orders.length,
    pending: orders.filter(o => o.status === 'pending').length,
    completed: orders.filter(o => o.status === 'completed').length,
    cancelled: orders.filter(o => o.status === 'cancelled').length,
    revenue: orders.filter(o => o.status === 'completed').reduce((sum, o) => sum + o.totalAmount, 0),
    subscriptions: orders.filter(o => o.isSubscription).length
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-600" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'cancelled':
        return <XCircle className="w-4 h-4 text-red-600" />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 border-4 border-pink-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Manage orders, kits, and website content</p>
        </motion.div>

        {/* Navigation Tabs */}
        <div className="flex space-x-4 mb-8">
          {[
            { id: 'orders', label: 'Orders', icon: BarChart3 },
            { id: 'kits', label: 'Kit Management', icon: Package },
            { id: 'content', label: 'Content Management', icon: Settings }
          ].map(tab => (
            <motion.button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg transition-colors ${
                activeTab === tab.id
                  ? 'bg-pink-500 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <tab.icon className="w-5 h-5" />
              <span>{tab.label}</span>
            </motion.button>
          ))}
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-blue-100 p-2 rounded-full">
                <Package className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Total Orders</h3>
            </div>
            <p className="text-2xl font-bold text-blue-600">{stats.total}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-yellow-100 p-2 rounded-full">
                <Clock className="w-5 h-5 text-yellow-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Pending</h3>
            </div>
            <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-purple-100 p-2 rounded-full">
                <Users className="w-5 h-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Subscriptions</h3>
            </div>
            <p className="text-2xl font-bold text-purple-600">{stats.subscriptions}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-green-100 p-2 rounded-full">
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Revenue</h3>
            </div>
            <p className="text-2xl font-bold text-green-600">₹{stats.revenue.toLocaleString()}</p>
          </motion.div>
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'orders' && (
            <motion.div
              key="orders"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-white rounded-xl shadow-lg border border-gray-100"
            >
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-800">Orders Management</h2>
                  <div className="flex space-x-2">
                    {['all', 'pending', 'completed', 'cancelled'].map(status => (
                      <button
                        key={status}
                        onClick={() => setFilter(status as any)}
                        className={`px-4 py-2 rounded-lg transition-colors ${
                          filter === status
                            ? 'bg-pink-500 text-white'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {status.charAt(0).toUpperCase() + status.slice(1)}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left p-4 font-semibold text-gray-800">Order ID</th>
                      <th className="text-left p-4 font-semibold text-gray-800">Kit</th>
                      <th className="text-left p-4 font-semibold text-gray-800">Date</th>
                      <th className="text-left p-4 font-semibold text-gray-800">Amount</th>
                      <th className="text-left p-4 font-semibold text-gray-800">Status</th>
                      <th className="text-left p-4 font-semibold text-gray-800">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredOrders.map((order, index) => {
                      const kit = kits.find(k => k.id === order.kitId);
                      return (
                        <motion.tr
                          key={order.id}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.05 }}
                          className="border-b border-gray-100 hover:bg-gray-50"
                        >
                          <td className="p-4">
                            <span className="font-mono text-sm text-gray-600">
                              #{order.id.slice(0, 8)}
                            </span>
                          </td>
                          <td className="p-4">
                            <div className="flex items-center space-x-3">
                              <img 
                                src={kit?.image} 
                                alt={kit?.name}
                                className="w-10 h-10 rounded-lg object-cover"
                              />
                              <span className="font-medium text-gray-800">{kit?.name}</span>
                            </div>
                          </td>
                          <td className="p-4 text-gray-600">
                            {new Date(order.scheduledDate).toLocaleDateString()}
                          </td>
                          <td className="p-4 font-semibold text-gray-800">
                            ₹{order.totalAmount}
                          </td>
                          <td className="p-4">
                            <div className="flex items-center space-x-2">
                              {getStatusIcon(order.status)}
                              <span className={`px-3 py-1 rounded-full text-sm ${
                                order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                order.status === 'completed' ? 'bg-green-100 text-green-800' :
                                'bg-red-100 text-red-800'
                              }`}>
                                {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                              </span>
                            </div>
                          </td>
                          <td className="p-4">
                            <div className="flex space-x-2">
                              {order.status === 'pending' && (
                                <>
                                  <motion.button
                                    onClick={() => handleStatusUpdate(order.id, 'completed')}
                                    className="px-3 py-1 bg-green-500 text-white text-sm rounded-lg hover:bg-green-600 transition-colors"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                  >
                                    Complete
                                  </motion.button>
                                  <motion.button
                                    onClick={() => handleStatusUpdate(order.id, 'cancelled')}
                                    className="px-3 py-1 bg-red-500 text-white text-sm rounded-lg hover:bg-red-600 transition-colors"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                  >
                                    Cancel
                                  </motion.button>
                                </>
                              )}
                              {order.status !== 'pending' && (
                                <span className="text-xs text-gray-400">No actions</span>
                              )}
                            </div>
                          </td>
                        </motion.tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {filteredOrders.length === 0 && (
                <div className="text-center py-12">
                  <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No orders found for the selected filter</p>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'kits' && (
            <motion.div
              key="kits"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Kit Management</h2>
                  <motion.button
                    onClick={() => setShowAddKit(true)}
                    className="flex items-center space-x-2 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Plus className="w-4 h-4" />
                    <span>Add Kit</span>
                  </motion.button>
                </div>

                {(showAddKit || editingKit) && (
                  <div className="mb-6">
                    <KitForm
                      kit={editingKit || undefined}
                      onSave={handleKitSave}
                      onCancel={() => {
                        setEditingKit(null);
                        setShowAddKit(false);
                      }}
                    />
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {kits.map((kit) => (
                    <motion.div
                      key={kit.id}
                      className="border rounded-xl p-4 hover:shadow-lg transition-shadow"
                      whileHover={{ y: -5 }}
                    >
                      <img 
                        src={kit.image} 
                        alt={kit.name}
                        className="w-full h-32 object-cover rounded-lg mb-3"
                      />
                      <h3 className="font-semibold text-gray-800 mb-2">{kit.name}</h3>
                      <p className="text-sm text-gray-600 mb-2">{kit.description}</p>
                      <p className="text-lg font-bold text-pink-600 mb-3">₹{kit.basePrice}</p>
                      <div className="flex space-x-2">
                        <motion.button
                          onClick={() => setEditingKit(kit)}
                          className="flex items-center space-x-1 bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Edit className="w-3 h-3" />
                          <span>Edit</span>
                        </motion.button>
                        <motion.button
                          onClick={() => handleKitDelete(kit.id)}
                          className="flex items-center space-x-1 bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Trash2 className="w-3 h-3" />
                          <span>Delete</span>
                        </motion.button>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'content' && (
            <motion.div
              key="content"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Benefits Management */}
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Why Choose PeriodCare?</h2>
                  <motion.button
                    onClick={() => setShowAddBenefit(true)}
                    className="flex items-center space-x-2 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Plus className="w-4 h-4" />
                    <span>Add Benefit</span>
                  </motion.button>
                </div>

                {(showAddBenefit || editingBenefit) && (
                  <div className="mb-6">
                    <BenefitForm
                      benefit={editingBenefit || undefined}
                      onSave={handleBenefitSave}
                      onCancel={() => {
                        setEditingBenefit(null);
                        setShowAddBenefit(false);
                      }}
                    />
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {benefits.map((benefit) => (
                    <motion.div
                      key={benefit.id}
                      className="border rounded-xl p-4 hover:shadow-lg transition-shadow"
                      whileHover={{ y: -2 }}
                    >
                      <div className="flex items-center space-x-3 mb-3">
                        <span className="text-2xl">{benefit.icon}</span>
                        <h3 className="font-semibold text-gray-800">{benefit.title}</h3>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{benefit.description}</p>
                      <div className="flex space-x-2">
                        <motion.button
                          onClick={() => setEditingBenefit(benefit)}
                          className="flex items-center space-x-1 bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Edit className="w-3 h-3" />
                          <span>Edit</span>
                        </motion.button>
                        <motion.button
                          onClick={() => handleBenefitDelete(benefit.id)}
                          className="flex items-center space-x-1 bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Trash2 className="w-3 h-3" />
                          <span>Delete</span>
                        </motion.button>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Testimonials Management */}
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">What Our Users Say</h2>
                  <motion.button
                    onClick={() => setShowAddTestimonial(true)}
                    className="flex items-center space-x-2 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Plus className="w-4 h-4" />
                    <span>Add Testimonial</span>
                  </motion.button>
                </div>

                {(showAddTestimonial || editingTestimonial) && (
                  <div className="mb-6">
                    <TestimonialForm
                      testimonial={editingTestimonial || undefined}
                      onSave={handleTestimonialSave}
                      onCancel={() => {
                        setEditingTestimonial(null);
                        setShowAddTestimonial(false);
                      }}
                    />
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {testimonials.map((testimonial) => (
                    <motion.div
                      key={testimonial.id}
                      className="border rounded-xl p-4 hover:shadow-lg transition-shadow"
                      whileHover={{ y: -2 }}
                    >
                      <div className="flex items-center space-x-2 mb-3">
                        <MessageSquare className="w-4 h-4 text-pink-500" />
                        <div className="flex">
                          {[...Array(testimonial.rating)].map((_, i) => (
                            <Star key={i} className="w-3 h-3 text-yellow-400 fill-current" />
                          ))}
                        </div>
                      </div>
                      <p className="text-sm text-gray-700 mb-3 italic">"{testimonial.text}"</p>
                      <div className="flex justify-between items-center mb-3">
                        <span className="font-semibold text-gray-800">{testimonial.name}</span>
                        <span className="text-xs text-gray-600">{testimonial.location}</span>
                      </div>
                      <div className="flex space-x-2">
                        <motion.button
                          onClick={() => setEditingTestimonial(testimonial)}
                          className="flex items-center space-x-1 bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Edit className="w-3 h-3" />
                          <span>Edit</span>
                        </motion.button>
                        <motion.button
                          onClick={() => handleTestimonialDelete(testimonial.id)}
                          className="flex items-center space-x-1 bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Trash2 className="w-3 h-3" />
                          <span>Delete</span>
                        </motion.button>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default AdminDashboard;
