import React from 'react';
import { motion } from 'framer-motion';
import { Check, Star } from 'lucide-react';
import { Kit } from '../../types';

interface KitCardProps {
  kit: Kit;
  onSelect: () => void;
  featured?: boolean;
}

const KitCard: React.FC<KitCardProps> = ({ kit, onSelect, featured = false }) => {
  const getKitBadge = (type: string) => {
    switch (type) {
      case 'basic':
        return { text: 'Essential', color: 'bg-green-100 text-green-700' };
      case 'medium':
        return { text: 'Popular', color: 'bg-blue-100 text-blue-700' };
      case 'premium':
        return { text: 'Premium', color: 'bg-purple-100 text-purple-700' };
      default:
        return { text: 'Kit', color: 'bg-gray-100 text-gray-700' };
    }
  };

  const badge = getKitBadge(kit.type);

  return (
    <motion.div
      className={`relative bg-white rounded-2xl shadow-lg border-2 transition-all duration-300 overflow-hidden ${
        featured 
          ? 'border-pink-500 shadow-pink-200' 
          : 'border-gray-200 hover:border-pink-300 hover:shadow-xl'
      }`}
      whileHover={{ y: -5, scale: 1.02 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {featured && (
        <div className="absolute top-4 right-4 z-10">
          <div className="bg-pink-500 text-white p-2 rounded-full">
            <Star className="w-4 h-4 fill-current" />
          </div>
        </div>
      )}

      <div className="relative">
        <img 
          src={kit.image} 
          alt={kit.name}
          className="w-full h-48 object-cover"
        />
        <div className="absolute top-4 left-4">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${badge.color}`}>
            {badge.text}
          </span>
        </div>
      </div>

      <div className="p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-2">{kit.name}</h3>
        <p className="text-gray-600 mb-4">{kit.description}</p>
        
        <div className="mb-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-gray-700">Includes:</span>
            <span className="text-2xl font-bold text-pink-600">₹{kit.basePrice}</span>
          </div>
          <ul className="space-y-2">
            {(kit.includedItems || []).map((item, index) => (
              <li key={index} className="flex items-center space-x-2 text-sm text-gray-600">
                <Check className="w-4 h-4 text-green-500" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <motion.button
          onClick={onSelect}
          className={`w-full py-3 rounded-lg font-semibold transition-all duration-300 ${
            featured
              ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white shadow-lg'
              : 'bg-pink-50 text-pink-600 hover:bg-pink-100'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Customize Kit
        </motion.button>
      </div>
    </motion.div>
  );
};

export default KitCard;