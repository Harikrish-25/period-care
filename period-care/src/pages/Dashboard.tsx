import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Package, MapPin, Plus } from 'lucide-react';
import KitCard from '../components/kits/KitCard';
import KitCustomizerModal from '../components/kits/KitCustomizerModal';
import OrderSuccessPopup from '../components/layout/OrderSuccessPopup';
import { authService, ordersService, kitsService } from '../services/api';
import { Kit, Order, User } from '../types';

const Dashboard: React.FC = () => {
  const [selectedKit, setSelectedKit] = useState<Kit | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSuccessPopupOpen, setIsSuccessPopupOpen] = useState(false);
  const [orderDetails, setOrderDetails] = useState<{id: number; totalAmount: number} | null>(null);
  const [recentOrders, setRecentOrders] = useState<Order[]>([]);
  const [kits, setKits] = useState<Kit[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Get current user
      const user = authService.getCurrentUserFromStorage();
      if (!user) {
        window.location.href = '/login';
        return;
      }
      setCurrentUser(user);
      
      // Load kits and orders
      const [userOrders, availableKits] = await Promise.all([
        ordersService.getUserOrders(),
        kitsService.getAllKits()
      ]);
      
      setRecentOrders(userOrders.slice(0, 3));
      setKits(availableKits);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKitSelect = (kit: Kit) => {
    setSelectedKit(kit);
    setIsModalOpen(true);
  };

  const handleOrder = async (orderData: any) => {
    if (!currentUser) return;

    try {
      const order = await ordersService.createOrder({
        kit_id: orderData.kitId,
        selected_fruits: orderData.selectedFruits,
        selected_nutrients: orderData.selectedNutrients,
        scheduled_date: orderData.scheduledDate,
        delivery_address: orderData.address,
      });

      // Set order details for popup and show success popup
      setOrderDetails({
        id: parseInt(order.id),
        totalAmount: order.totalAmount
      });
      setIsSuccessPopupOpen(true);

      setIsModalOpen(false);
      setSelectedKit(null);
      loadDashboardData();
      
    } catch (error) {
      console.error('Failed to create order:', error);
      alert('Failed to place order. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 border-4 border-pink-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 py-8">
      <div className="container mx-auto px-4">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Welcome back, {currentUser?.name}! 👋
          </h1>
          <p className="text-gray-600">Manage your period care essentials with ease</p>
        </motion.div>

        {/* Dashboard Summary */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-pink-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-pink-100 p-2 rounded-full">
                <Package className="w-5 h-5 text-pink-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Recent Orders</h3>
            </div>
            {recentOrders.length > 0 ? (
              <>
                <p className="text-2xl font-bold text-pink-600 mb-1">
                  {recentOrders.length}
                </p>
                <p className="text-sm text-gray-600">
                  Orders placed this month
                </p>
              </>
            ) : (
              <p className="text-gray-500">No orders yet</p>
            )}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-purple-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-purple-100 p-2 rounded-full">
                <Calendar className="w-5 h-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Recent Orders</h3>
            </div>
            <p className="text-2xl font-bold text-purple-600 mb-1">{recentOrders.length}</p>
            <p className="text-sm text-gray-600">Orders this month</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-green-100"
          >
            <div className="flex items-center space-x-3 mb-3">
              <div className="bg-green-100 p-2 rounded-full">
                <MapPin className="w-5 h-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Delivery Address</h3>
            </div>
            <p className="text-sm text-gray-600 line-clamp-2">
              {currentUser?.address || 'Please update your address'}
            </p>
          </motion.div>
        </div>

        {/* Kit Selection */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Choose Your Kit</h2>
            <motion.button
              className="flex items-center space-x-2 px-4 py-2 bg-pink-100 text-pink-600 rounded-lg hover:bg-pink-200 transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Plus className="w-4 h-4" />
              <span>Quick Order</span>
            </motion.button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {kits.map((kit, index) => (
              <motion.div
                key={kit.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
              >
                <KitCard 
                  kit={kit} 
                  onSelect={() => handleKitSelect(kit)}
                  featured={kit.type === 'medium'}
                />
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Recent Orders */}
        {recentOrders.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100"
          >
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Recent Orders</h3>
            <div className="space-y-4">
              {recentOrders.map((order) => {
                const kit = kits.find(k => k.id === order.kitId);
                return (
                  <div key={order.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center">
                        <Package className="w-6 h-6 text-pink-600" />
                      </div>
                      <div>
                        <p className="font-semibold text-gray-800">{kit?.name}</p>
                        <p className="text-sm text-gray-600">
                          Scheduled for {new Date(order.scheduledDate).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-800">₹{order.totalAmount}</p>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        order.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </div>

      {/* Kit Customizer Modal */}
      <KitCustomizerModal
        kit={selectedKit}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedKit(null);
        }}
        onOrder={handleOrder}
      />

      {/* Order Success Popup */}
      <OrderSuccessPopup
        isOpen={isSuccessPopupOpen}
        onClose={() => setIsSuccessPopupOpen(false)}
        orderDetails={orderDetails}
      />
    </div>
  );
};

export default Dashboard;