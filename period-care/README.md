# PeriodCare - Period Care Ordering & Subscription App

A modern, responsive frontend application for ordering and subscribing to customizable period care kits. Built with React, TypeScript, and Tailwind CSS.

## ✨ Features

### Core Functionality
- **Three-Tier Kit System**: Basic, Medium, and Premium kits with different price points
- **Customization Options**: Select fruits (pain relief) and nutrients (max 2) with live price updates
- **Flexible Scheduling**: Choose delivery dates with mobile-friendly date picker
- **Subscription Management**: Monthly, 6-month, and yearly subscription options
- **WhatsApp Integration**: Orders automatically generate WhatsApp links for admin notification
- **Dual Role System**: Separate dashboards for users and admins

### User Features
- **Dashboard**: View upcoming deliveries, subscription status, and order history
- **Profile Management**: Edit personal information and addresses
- **Order Tracking**: Monitor order status and delivery schedules
- **Responsive Design**: Mobile-first approach with seamless experience across devices

### Admin Features
- **Order Management**: View, filter, and update order statuses
- **Analytics Dashboard**: Track orders, revenue, and subscription metrics
- **Real-time Updates**: Instant order status changes with WhatsApp notifications

### Design & UX
- **Modern UI**: Clean, Apple-level design aesthetics with premium feel
- **Smooth Animations**: Framer Motion page transitions and micro-interactions
- **Particle Background**: Animated hero section with particles.js
- **Accessibility**: Proper ARIA labels, keyboard navigation, and color contrast
- **Performance**: Optimized images and lazy loading for fast page loads

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd period-care-app
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## 🏗️ Project Structure

```
src/
├── components/           # Reusable components
│   ├── auth/            # Authentication forms
│   ├── kits/            # Kit-related components
│   └── layout/          # Header, Footer components
├── pages/               # Page components
├── services/            # API services (mock)
├── data/                # Mock data
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
└── App.tsx              # Main app component
```

## 🔧 Configuration

### WhatsApp Integration
Update the admin phone number in `src/utils/whatsapp.ts`:

```typescript
export const ADMIN_PHONE = '+919999999999'; // Replace with actual admin number
```

### Mock Data
Test accounts are available in `src/data/mockData.ts`:

- **User Account**: `priya@example.com` / `password123`
- **Admin Account**: `admin@periodcare.com` / `admin123`

## 📱 Demo Accounts

### User Account
- **Email**: priya@example.com
- **Password**: password123
- **Features**: Order kits, manage subscriptions, view profile

### Admin Account  
- **Email**: admin@periodcare.com
- **Password**: admin123
- **Features**: Manage orders, view analytics, update order status

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Routing**: React Router DOM
- **Background Effects**: Particles.js
- **Icons**: Lucide React
- **State Management**: React Hooks + Local Storage
- **Build Tool**: Vite

## 🎨 Design System

### Colors
- **Primary**: Pink (#ec4899) to Purple (#a855f7) gradient
- **Secondary**: Various purple shades (#8b5cf6, #7c3aed)
- **Accent**: Complementary colors for success, warning, error states
- **Neutral**: Gray scale for text and backgrounds

### Typography
- **Font**: Inter (system fallback)
- **Hierarchy**: Consistent sizing with 120% line height for headings, 150% for body
- **Weights**: Regular (400), Medium (500), Semibold (600), Bold (700)

### Spacing
- **System**: 8px base unit for consistent spacing
- **Responsive**: Mobile-first breakpoints (640px, 768px, 1024px, 1280px)

## 🔌 API Integration

The app currently uses mock services. To integrate with a real backend:

1. Replace mock services in `src/services/mockApi.ts` with actual API calls
2. Update environment variables for API endpoints
3. Implement proper error handling and loading states
4. Add authentication tokens and session management

### Expected API Endpoints
```
POST /api/auth/login
POST /api/auth/register
GET /api/kits
POST /api/orders
GET /api/orders/user/:id
PUT /api/orders/:id/status
POST /api/subscriptions
GET /api/subscriptions/user/:id
```

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

The built files will be in the `dist/` directory, ready for deployment to any static hosting service.

## 🧪 Testing

Run the linter:
```bash
npm run lint
```

## 📈 Performance Features

- **Code Splitting**: Automatic route-based code splitting with React Router
- **Image Optimization**: Responsive images with proper sizing
- **Lazy Loading**: Components and images load on demand
- **Caching**: Service worker ready for PWA implementation
- **Bundle Optimization**: Tree shaking and minification in production

## 🌟 Future Enhancements

- **Push Notifications**: Delivery reminders and order updates
- **Payment Integration**: Stripe/Razorpay for secure payments  
- **Real-time Chat**: Customer support integration
- **Advanced Analytics**: Detailed insights and reporting
- **Multi-language**: Support for regional languages
- **PWA**: Offline functionality and app-like experience

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

For questions or support, please contact:
- **Email**: hello@periodcare.com
- **WhatsApp**: +91 99999 99999

---

Made with 💜 for women's wellness by the PeriodCare team.