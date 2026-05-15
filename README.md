# Godavari Captures - Photography & Reel Making Studio

A luxury photography and reel-making studio website featuring instant booking, portfolio showcase, and automated email notifications.

![Godavari Captures](frontend/public/images/hero-godavari.jpg)

## 🌟 Features

- **Instant Booking System** - Real-time booking with email notifications
- **Portfolio Gallery** - Filterable portfolio by category (Weddings, Photoshoots, Events, Drone)
- **Responsive Design** - Mobile-first design with hamburger menu
- **Email Notifications** - Automatic booking confirmations via email
- **Luxury Aesthetic** - Black & gold color scheme with Playfair Display typography
- **Fast Performance** - Background email processing for instant responses

## 🛠️ Tech Stack

### Frontend
- **React 19** - Modern UI library
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Custom Fonts** - Playfair Display & Manrope

### Backend
- **FastAPI** - High-performance Python API
- **Pydantic** - Data validation
- **aiosmtplib** - Async email sending
- **Motor** - Async MongoDB driver (optional)

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.14+
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/godavari-captures.git
cd godavari-captures
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: http://localhost:3000

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: http://localhost:8000

### 4. Email Configuration (Optional)

To enable email notifications:

1. Copy `.env.example` to `.env` in the `backend` folder
2. Add your Gmail credentials:
   ```env
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   RECIPIENT_EMAIL=neerupudijohnsonnj@gmail.com
   ```
3. Generate Gmail App Password: https://myaccount.google.com/apppasswords

See `EMAIL_SETUP_INSTRUCTIONS.md` for detailed setup.

## 📱 Mobile Testing

The website is configured for network access. To test on mobile:

1. Ensure mobile is on the same WiFi network
2. Find your computer's IP address
3. Access: `http://YOUR_IP:3000`

## 📂 Project Structure

```
godavari-captures/
├── frontend/                 # React frontend
│   ├── public/              # Static assets
│   │   └── images/          # Images (hero, portfolio)
│   ├── src/
│   │   ├── App.jsx          # Main component
│   │   ├── constants/       # Brand data & content
│   │   ├── api/             # API client
│   │   └── index.css        # Global styles
│   └── vite.config.js       # Vite configuration
│
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── routes/          # API endpoints
│   │   ├── models/          # Pydantic models
│   │   └── email_service.py # Email functionality
│   ├── tests/               # Test files
│   └── requirements.txt     # Python dependencies
│
└── .kiro/                   # Kiro spec files
```

## 🎨 Design System

### Colors
- **Luxury Black**: `#000000`, `#0A0A0A`, `#050505`
- **Luxury Gold**: `#D4AF37`
- **Gold Hover**: `#C5A017`

### Typography
- **Headings**: Playfair Display
- **Body**: Manrope

### Components
- Square edges (border-radius: 0)
- Gold accent buttons
- Dark luxury aesthetic

## 📧 API Endpoints

### Bookings
- `POST /api/bookings` - Create new booking
- `GET /api/bookings` - List all bookings

### Health Check
- `GET /api/` - API health status

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Notes

- `.env` file is gitignored (never commit credentials)
- Use Gmail App Passwords, not regular passwords
- CORS configured for public access
- Input validation with Pydantic

## 📞 Contact Information

- **Phone**: +91 7780494179
- **Email**: neerupudijohnsonnj@gmail.com
- **Location**: Rajahmundry, Andhra Pradesh, India
- **Instagram**: @godavari.captures

## 🚀 Deployment

### Frontend (Netlify/Vercel)
```bash
cd frontend
npm run build
# Deploy dist/ folder
```

### Backend (Railway/Render)
```bash
cd backend
# Deploy with Python 3.14+
# Set environment variables in platform
```

## 📝 License

© 2026 Godavari Captures. All rights reserved.

## 🤝 Contributing

This is a private project for Godavari Captures photography studio.

## 📚 Documentation

- [Email Setup Instructions](EMAIL_SETUP_INSTRUCTIONS.md)
- [Image Setup Guide](INSTRUCTIONS_ADD_IMAGES.md)
- [API Documentation](http://localhost:8000/docs) (when backend is running)

## 🎯 Features Roadmap

- [x] Instant booking system
- [x] Email notifications
- [x] Portfolio gallery with filtering
- [x] Mobile responsive design
- [x] Background image optimization
- [ ] MongoDB integration
- [ ] Payment gateway integration
- [ ] Admin dashboard
- [ ] Customer testimonials management

## 💡 Support

For issues or questions, contact: neerupudijohnsonnj@gmail.com

---

**Built with ❤️ for Godavari Captures**
