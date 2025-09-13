import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus, Minus, Calendar, MapPin } from 'lucide-react';
import { Kit } from '../../types';
import { fruits, nutrients } from '../../data/mockData';

interface KitCustomizerModalProps {
  kit: Kit | null;
  isOpen: boolean;
  onClose: () => void;
  onOrder: (orderData: any) => void;
}

const KitCustomizerModal: React.FC<KitCustomizerModalProps> = ({ 
  kit, 
  isOpen, 
  onClose, 
  onOrder 
}) => {
  const [selectedFruits, setSelectedFruits] = useState<string[]>([]);
  const [selectedNutrients, setSelectedNutrients] = useState<string[]>([]);
  const [scheduledDate, setScheduledDate] = useState('');
  const [address, setAddress] = useState('');
  const [isSubscription, setIsSubscription] = useState(false);
  const [subscriptionType, setSubscriptionType] = useState<'monthly' | '6-month' | 'yearly'>('monthly');

  useEffect(() => {
    if (isOpen && kit) {
      // Reset form when modal opens
      setSelectedFruits([]);
      setSelectedNutrients([]);
      setScheduledDate('');
      setAddress('');
      setIsSubscription(false);
      setSubscriptionType('monthly');
    }
  }, [isOpen, kit]);

  if (!kit) return null;

  const toggleFruit = (fruitId: string) => {
    setSelectedFruits(prev => 
      prev.includes(fruitId) 
        ? prev.filter(id => id !== fruitId)
        : [...prev, fruitId]
    );
  };

  const toggleNutrient = (nutrientId: string) => {
    setSelectedNutrients(prev => 
      prev.includes(nutrientId) 
        ? prev.filter(id => id !== nutrientId)
        : prev.length < 2 
          ? [...prev, nutrientId]
          : prev
    );
  };

  const calculateTotal = () => {
    const fruitsTotal = selectedFruits.reduce((sum, fruitId) => {
      const fruit = fruits.find(f => f.id === fruitId);
      return sum + (fruit?.price || 0);
    }, 0);

    const nutrientsTotal = selectedNutrients.reduce((sum, nutrientId) => {
      const nutrient = nutrients.find(n => n.id === nutrientId);
      return sum + (nutrient?.price || 0);
    }, 0);

    return kit.basePrice + fruitsTotal + nutrientsTotal;
  };

  const handleOrder = () => {
    const orderData = {
      kitId: kit.id,
      selectedFruits,
      selectedNutrients,
      scheduledDate,
      address,
      totalAmount: calculateTotal(),
      isSubscription,
      subscriptionType: isSubscription ? subscriptionType : undefined
    };
    onOrder(orderData);
  };

  const minDate = new Date().toISOString().split('T')[0];

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          
          <motion.div
            className="relative bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ duration: 0.3 }}
          >
            <div className="sticky top-0 bg-white border-b border-gray-200 p-6 z-10">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-800">Customize Your {kit.name}</h2>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>

            <div className="p-6 space-y-8">
              <div className="grid md:grid-cols-2 gap-8">
                {/* Kit Details */}
                <div>
                  <img 
                    src={kit.image} 
                    alt={kit.name}
                    className="w-full h-48 object-cover rounded-xl mb-4"
                  />
                  <h3 className="text-lg font-semibold mb-2">Base Kit Includes:</h3>
                  <ul className="space-y-2">
                    {kit.includedItems.map((item, index) => (
                      <li key={index} className="flex items-center space-x-2 text-gray-600">
                        <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Customization */}
                <div className="space-y-6">
                  {/* Fruits Selection */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Select Fruits (Pain Relief)</h3>
                    <div className="grid grid-cols-2 gap-3">
                      {fruits.map(fruit => (
                        <motion.div
                          key={fruit.id}
                          className={`p-3 border rounded-lg cursor-pointer transition-all ${
                            selectedFruits.includes(fruit.id)
                              ? 'border-pink-500 bg-pink-50'
                              : 'border-gray-200 hover:border-pink-300'
                          }`}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => toggleFruit(fruit.id)}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-medium">{fruit.name}</span>
                            <span className="text-pink-600 font-semibold">₹{fruit.price}</span>
                          </div>
                          <p className="text-xs text-gray-500">{fruit.benefits}</p>
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  {/* Nutrients Selection */}
                  <div>
                    <h3 className="text-lg font-semibold mb-2">Select Nutrients (Max 2)</h3>
                    <p className="text-sm text-gray-600 mb-4">Choose up to 2 supplements for enhanced wellness</p>
                    <div className="space-y-3">
                      {nutrients.map(nutrient => (
                        <motion.div
                          key={nutrient.id}
                          className={`p-3 border rounded-lg cursor-pointer transition-all ${
                            selectedNutrients.includes(nutrient.id)
                              ? 'border-purple-500 bg-purple-50'
                              : selectedNutrients.length >= 2
                              ? 'border-gray-200 opacity-50 cursor-not-allowed'
                              : 'border-gray-200 hover:border-purple-300'
                          }`}
                          whileHover={selectedNutrients.length < 2 || selectedNutrients.includes(nutrient.id) ? { scale: 1.02 } : {}}
                          whileTap={selectedNutrients.length < 2 || selectedNutrients.includes(nutrient.id) ? { scale: 0.98 } : {}}
                          onClick={() => toggleNutrient(nutrient.id)}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-medium">{nutrient.name}</span>
                            <span className="text-purple-600 font-semibold">₹{nutrient.price}</span>
                          </div>
                          <p className="text-sm text-gray-600">{nutrient.description}</p>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Scheduling & Address */}
              <div className="grid md:grid-cols-2 gap-6 pt-6 border-t border-gray-200">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Calendar className="w-4 h-4 inline mr-1" />
                    Delivery Date
                  </label>
                  <input
                    type="date"
                    value={scheduledDate}
                    min={minDate}
                    onChange={(e) => setScheduledDate(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <MapPin className="w-4 h-4 inline mr-1" />
                    Delivery Address
                  </label>
                  <textarea
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    placeholder="Enter your complete delivery address"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none resize-none"
                    rows={3}
                    required
                  />
                </div>
              </div>

              {/* Subscription Option */}
              <div className="pt-6 border-t border-gray-200">
                <div className="flex items-center space-x-3 mb-4">
                  <input
                    type="checkbox"
                    id="subscription"
                    checked={isSubscription}
                    onChange={(e) => setIsSubscription(e.target.checked)}
                    className="w-5 h-5 text-pink-600"
                  />
                  <label htmlFor="subscription" className="text-lg font-semibold text-gray-800">
                    Subscribe for Regular Deliveries
                  </label>
                </div>
                
                {isSubscription && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="space-y-3"
                  >
                    <p className="text-gray-600">Choose your subscription frequency:</p>
                    <div className="grid grid-cols-3 gap-4">
                      {[
                        { value: 'monthly', label: 'Monthly', discount: '0%' },
                        { value: '6-month', label: '6 Months', discount: '10%' },
                        { value: 'yearly', label: 'Yearly', discount: '20%' }
                      ].map(option => (
                        <motion.div
                          key={option.value}
                          className={`p-4 border rounded-lg cursor-pointer transition-all ${
                            subscriptionType === option.value
                              ? 'border-pink-500 bg-pink-50'
                              : 'border-gray-200 hover:border-pink-300'
                          }`}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => setSubscriptionType(option.value as any)}
                        >
                          <div className="text-center">
                            <p className="font-semibold">{option.label}</p>
                            <p className="text-sm text-green-600">{option.discount} off</p>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </div>

              {/* Order Summary */}
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4">Order Summary</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Base Kit</span>
                    <span>₹{kit.basePrice}</span>
                  </div>
                  {selectedFruits.map(fruitId => {
                    const fruit = fruits.find(f => f.id === fruitId);
                    return fruit ? (
                      <div key={fruitId} className="flex justify-between text-sm">
                        <span>{fruit.name}</span>
                        <span>₹{fruit.price}</span>
                      </div>
                    ) : null;
                  })}
                  {selectedNutrients.map(nutrientId => {
                    const nutrient = nutrients.find(n => n.id === nutrientId);
                    return nutrient ? (
                      <div key={nutrientId} className="flex justify-between text-sm">
                        <span>{nutrient.name}</span>
                        <span>₹{nutrient.price}</span>
                      </div>
                    ) : null;
                  })}
                  <div className="border-t pt-2 flex justify-between font-bold text-lg">
                    <span>Total</span>
                    <span className="text-pink-600">₹{calculateTotal()}</span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-4 pt-6">
                <button
                  onClick={onClose}
                  className="flex-1 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <motion.button
                  onClick={handleOrder}
                  disabled={!scheduledDate || !address}
                  className="flex-1 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {isSubscription ? 'Subscribe Now' : 'Place Order'}
                </motion.button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default KitCustomizerModal;