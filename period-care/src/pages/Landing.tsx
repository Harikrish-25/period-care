import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/landing/Hero';
import KitCard from '../components/kits/KitCard';
import KitCustomizerModal from '../components/kits/KitCustomizerModal';
import { kitsService, cmsService } from '../services/api';
import { authService } from '../services/mockApi';
import { Kit, Benefit, Testimonial } from '../types';
import { Star, Quote } from 'lucide-react';

const Landing: React.FC = () => {
  const [kits, setKits] = useState<Kit[]>([]);
  const [benefits, setBenefits] = useState<Benefit[]>([]);
  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);
  const [loading, setLoading] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedKit, setSelectedKit] = useState<Kit | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  // Handle kit customization - redirect to login if not authenticated
  const handleKitCustomize = (kit: Kit) => {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      // Redirect to login page if user is not authenticated
      navigate('/login');
    } else {
      // User is logged in, open the kit customizer modal
      setSelectedKit(kit);
      setIsModalOpen(true);
    }
  };

  // Handle order placement from modal
  const handleOrder = (orderData: any) => {
    console.log('Placing order:', orderData);
    setIsModalOpen(false);
    setSelectedKit(null);
    // TODO: Implement actual order placement logic
  };

  useEffect(() => {
    // Check if user is logged in
    const currentUser = authService.getCurrentUser();
    setIsLoggedIn(!!currentUser);

    // Listen for storage changes to update login state
    const handleStorageChange = () => {
      const user = authService.getCurrentUser();
      setIsLoggedIn(!!user);
    };

    window.addEventListener('storage', handleStorageChange);

    const loadData = async () => {
      try {
        const [kitsData, benefitsData, testimonialsData] = await Promise.all([
          kitsService.getAllKits(),
          cmsService.getAllBenefits(),
          cmsService.getAllTestimonials()
        ]);
        
        setKits(kitsData);
        setBenefits(benefitsData);
        setTestimonials(testimonialsData);
      } catch (error) {
        console.error('Failed to load data:', error);
        // Fallback to imported data if API fails
        const { kits: fallbackKits, benefits: fallbackBenefits, testimonials: fallbackTestimonials } = await import('../data/mockData');
        setKits(fallbackKits);
        setBenefits(fallbackBenefits);
        setTestimonials(fallbackTestimonials);
      } finally {
        setLoading(false);
      }
    };

    loadData();

    // Cleanup
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

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
    <div className="min-h-screen">
      <Hero />
      
      {/* Featured Kits Section - Only show when user is not logged in */}
      {!isLoggedIn && (
        <section className="py-20 bg-white">
          <div className="container mx-auto px-4">
            <motion.div
              className="text-center mb-16"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-gray-800 mb-4">
                Choose Your Perfect Kit
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Three carefully curated tiers to match your comfort needs and preferences
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8 mb-16">
              {kits.map((kit, index) => (
                <motion.div
                  key={kit.id}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.2 }}
                >
                  <KitCard 
                    kit={kit} 
                    onSelect={() => handleKitCustomize(kit)} 
                    featured={kit.type === 'medium'}
                  />
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Benefits Section */}
      <section className="py-20 bg-gradient-to-r from-pink-50 to-purple-50">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-800 mb-4">
              Why Choose PeriodCare?
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <motion.div
                key={benefit.id}
                className="bg-white rounded-2xl p-6 shadow-lg border border-pink-100"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="text-4xl mb-4 text-center">{benefit.icon}</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2 text-center">
                  {benefit.title}
                </h3>
                <p className="text-gray-600 text-center">{benefit.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-gray-800 mb-4">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600">
              Join thousands of satisfied women who trust PeriodCare
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.id}
                className="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-6 border border-pink-100"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                whileHover={{ scale: 1.02 }}
              >
                <div className="flex items-center mb-4">
                  <Quote className="w-8 h-8 text-pink-400 mr-2" />
                  <div className="flex">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                </div>
                <p className="text-gray-700 mb-4 italic">"{testimonial.text}"</p>
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-gray-800">{testimonial.name}</span>
                  <span className="text-sm text-gray-600">{testimonial.location}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

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
    </div>
  );
};

export default Landing;