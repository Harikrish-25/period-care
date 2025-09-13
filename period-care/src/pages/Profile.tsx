import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Phone, MapPin, Package, Calendar, Edit2, Save, X } from 'lucide-react';
import { authService, ordersService, subscriptionsService } from '../services/mockApi';
import { Order, Subscription } from '../types';

const Profile: React.FC = () => {
  const [user, setUser] = useState(authService.getCurrentUser());
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    mobile: user?.mobile || '',
    address: user?.address || ''
  });
  const [orders, setOrders] = useState<Order[]>([]);
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfileData();
  }, []);

  const loadProfileData = async () => {
    if (!user) return;
    
    try {
      const [userOrders, userSub] = await Promise.all([
        ordersService.getUserOrders(user.id),
        subscriptionsService.getUserSubscription(user.id)
      ]);
      
      setOrders(userOrders);
      setSubscription(userSub);
    } catch (error) {
      console.error('Failed to load profile data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = () => {
    // In a real app, this would update the user data via API
    const updatedUser = { ...user!, ...formData };
    localStorage.setItem('currentUser', JSON.stringify(updatedUser));
    setUser(updatedUser);
    setEditing(false);
  };

  const handleCancel = () => {
    setFormData({
      name: user?.name || '',
      email: user?.email || '',
      mobile: user?.mobile || '',
      address: user?.address || ''
    });
    setEditing(false);
  };

  const handleCancelSubscription = async () => {
    if (!subscription) return;
    
    try {
      await subscriptionsService.cancelSubscription(subscription.id);
      setSubscription(null);
    } catch (error) {
      console.error('Failed to cancel subscription:', error);
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Profile Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-pink-100"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="w-20 h-20 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center">
                <User className="w-10 h-10 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-800">{user.name}</h1>
                <p className="text-gray-600">Member since January 2025</p>
              </div>
            </div>
            <motion.button
              onClick={() => setEditing(!editing)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                editing 
                  ? 'bg-gray-100 text-gray-600 hover:bg-gray-200' 
                  : 'bg-pink-100 text-pink-600 hover:bg-pink-200'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {editing ? <X className="w-4 h-4" /> : <Edit2 className="w-4 h-4" />}
              <span>{editing ? 'Cancel' : 'Edit Profile'}</span>
            </motion.button>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-pink-500" />
                {editing ? (
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="flex-1 p-2 border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                ) : (
                  <span className="text-gray-700">{user.email}</span>
                )}
              </div>

              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-pink-500" />
                {editing ? (
                  <input
                    type="text"
                    value={formData.mobile}
                    onChange={(e) => setFormData({ ...formData, mobile: e.target.value })}
                    className="flex-1 p-2 border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                ) : (
                  <span className="text-gray-700">{user.mobile}</span>
                )}
              </div>
            </div>

            <div>
              <div className="flex items-start space-x-3">
                <MapPin className="w-5 h-5 text-pink-500 mt-1" />
                {editing ? (
                  <textarea
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    className="flex-1 p-2 border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none resize-none"
                    rows={3}
                  />
                ) : (
                  <span className="text-gray-700">{user.address}</span>
                )}
              </div>
            </div>
          </div>

          {editing && (
            <div className="flex space-x-3 mt-6 pt-6 border-t border-gray-200">
              <motion.button
                onClick={handleSave}
                className="flex items-center space-x-2 px-6 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg font-semibold"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Save className="w-4 h-4" />
                <span>Save Changes</span>
              </motion.button>
              <button
                onClick={handleCancel}
                className="px-6 py-2 border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
            </div>
          )}
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Subscription Status */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl shadow-lg p-6 border border-purple-100"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="bg-purple-100 p-2 rounded-full">
                <Calendar className="w-5 h-5 text-purple-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-800">Subscription</h2>
            </div>

            {subscription ? (
              <div className="space-y-4">
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="font-semibold text-purple-800 mb-1">
                    {subscription.type.charAt(0).toUpperCase() + subscription.type.slice(1)} Plan
                  </p>
                  <p className="text-sm text-purple-600">
                    Next delivery: {new Date(subscription.nextDelivery).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={handleCancelSubscription}
                  className="w-full py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                >
                  Cancel Subscription
                </button>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-4">No active subscription</p>
                <button className="px-6 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all">
                  Start Subscription
                </button>
              </div>
            )}
          </motion.div>

          {/* Order History */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-2xl shadow-lg p-6 border border-pink-100"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="bg-pink-100 p-2 rounded-full">
                <Package className="w-5 h-5 text-pink-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-800">Order History</h2>
            </div>

            {orders.length > 0 ? (
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {orders.map((order) => (
                  <div key={order.id} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <p className="font-semibold text-gray-800">Order #{order.id.slice(0, 8)}</p>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        order.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-1">
                      Scheduled: {new Date(order.scheduledDate).toLocaleDateString()}
                    </p>
                    <p className="text-sm font-semibold text-pink-600">₹{order.totalAmount}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500">No orders yet</p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Profile;