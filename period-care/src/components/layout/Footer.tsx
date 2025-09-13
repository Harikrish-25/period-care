import React from 'react';
import { Heart, Mail, Phone, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gradient-to-r from-pink-50 to-purple-50 border-t border-pink-100">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-2 rounded-full">
                <Heart className="w-5 h-5 text-white fill-current" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
                PeriodCare
              </span>
            </div>
            <p className="text-gray-600 mb-4 max-w-md">
              Empowering women with comfortable, convenient period care solutions. 
              Subscribe to monthly wellness kits with customizable fruits and nutrients.
            </p>
            <div className="flex space-x-4">
              {/* Social media links would go here */}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-gray-800 mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-pink-600 transition-colors">About Us</a></li>
              <li><a href="#" className="text-gray-600 hover:text-pink-600 transition-colors">Our Kits</a></li>
              <li><a href="#" className="text-gray-600 hover:text-pink-600 transition-colors">Subscription</a></li>
              <li><a href="#" className="text-gray-600 hover:text-pink-600 transition-colors">FAQ</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-semibold text-gray-800 mb-4">Contact</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-pink-500" />
                <span className="text-gray-600 text-sm">hello@periodcare.com</span>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-pink-500" />
                <span className="text-gray-600 text-sm">+91 99999 99999</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="w-4 h-4 text-pink-500" />
                <span className="text-gray-600 text-sm">Delhi, India</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-pink-200 mt-8 pt-8 text-center">
          <p className="text-gray-600 text-sm">
            © 2025 PeriodCare. Made with 💜 for women's wellness.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;