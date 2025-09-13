import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Heart, User, LogOut, Package } from 'lucide-react';
import { authService } from '../../services/mockApi';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentUser = authService.getCurrentUser();

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <motion.header 
      className="bg-white/90 backdrop-blur-lg shadow-lg sticky top-0 z-50 border-b border-pink-100"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.3 }}
              className="bg-gradient-to-r from-pink-500 to-purple-600 p-2 rounded-full"
            >
              <Heart className="w-6 h-6 text-white fill-current" />
            </motion.div>
            <span className="text-xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
              PeriodCare
            </span>
          </Link>

          <nav className="flex items-center space-x-6">
            {!currentUser ? (
              <>
                <Link
                  to="/login"
                  className={`px-4 py-2 rounded-full transition-colors ${
                    isActive('/login') 
                      ? 'bg-pink-100 text-pink-600' 
                      : 'text-gray-600 hover:text-pink-600'
                  }`}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-6 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-full hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                >
                  Register
                </Link>
              </>
            ) : (
              <div className="flex items-center space-x-4">
                {currentUser.role === 'admin' ? (
                  <Link
                    to="/admin"
                    className={`flex items-center space-x-1 px-4 py-2 rounded-full transition-colors ${
                      isActive('/admin') 
                        ? 'bg-pink-100 text-pink-600' 
                        : 'text-gray-600 hover:text-pink-600'
                    }`}
                  >
                    <Package className="w-4 h-4" />
                    <span>Admin</span>
                  </Link>
                ) : (
                  <>
                    <Link
                      to="/dashboard"
                      className={`flex items-center space-x-1 px-4 py-2 rounded-full transition-colors ${
                        isActive('/dashboard') 
                          ? 'bg-pink-100 text-pink-600' 
                          : 'text-gray-600 hover:text-pink-600'
                      }`}
                    >
                      <Package className="w-4 h-4" />
                      <span>Dashboard</span>
                    </Link>
                    <Link
                      to="/profile"
                      className={`flex items-center space-x-1 px-4 py-2 rounded-full transition-colors ${
                        isActive('/profile') 
                          ? 'bg-pink-100 text-pink-600' 
                          : 'text-gray-600 hover:text-pink-600'
                      }`}
                    >
                      <User className="w-4 h-4" />
                      <span>Profile</span>
                    </Link>
                  </>
                )}
                <motion.button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 px-4 py-2 text-gray-600 hover:text-red-600 transition-colors rounded-full hover:bg-red-50"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </motion.button>
              </div>
            )}
          </nav>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;