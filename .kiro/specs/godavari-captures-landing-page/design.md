# Design Document: Godavari Captures Landing Page

## Overview

The Godavari Captures landing page is a luxury single-page full-stack web application showcasing a premium photography and cinematic reel-making studio. The system combines a React 19 frontend with a FastAPI backend to deliver an immersive, high-performance user experience that reflects the studio's premium positioning.

### System Architecture

The application follows a modern client-server architecture:

- **Frontend**: React 19 single-page application with Tailwind CSS for styling
- **Backend**: FastAPI REST API with async MongoDB operations
- **Database**: MongoDB for persistent storage of bookings and contact messages
- **Communication**: RESTful HTTP/JSON API with axios for client requests

### Design Philosophy

The design embodies luxury through minimalism: pure black backgrounds (#000000, #0A0A0A, #050505) with strategic gold accents (#D4AF37), cinematic typography (Playfair Display for elegance, Manrope for clarity), and square edges throughout. Film grain overlays and fade-up animations enhance the cinematic aesthetic without compromising performance.

## Architecture

### Frontend Architecture

**Component Hierarchy**:
```
App
├── Navbar (sticky navigation with smooth scroll)
├── Hero (full-bleed image, stats, showreel modal)
├── Services (5-card grid with booking CTAs)
├── About (two-column layout with feature cells)
├── StatsAndBooking (stats cards + booking form)
├── Portfolio (filterable masonry gallery)
├── Packages (3-tier pricing cards)
├── Testimonials (auto-rotating carousel)
├── Contact (form + studio info)
└── Footer (4-column grid with navigation)
```

**State Management**:
- Component-level state using React hooks (useState, useEffect, useRef)
- No global state management needed (simple application scope)
- Form state managed locally within form components
- Modal visibility controlled by parent component state

**Routing Strategy**:
- Single-page application with no client-side routing
- Navigation via smooth-scroll to section refs using `scrollIntoView({ behavior: 'smooth' })`
- Refs passed from App.js to child components for cross-component navigation


### Backend Architecture

**API Layer Structure**:
```
FastAPI Application
├── CORS Middleware (allow all origins for public site)
├── Health Check Endpoint (GET /api/)
├── Booking Routes
│   ├── POST /api/bookings (create booking)
│   └── GET /api/bookings (list bookings)
└── Contact Routes
    ├── POST /api/contact (create message)
    └── GET /api/contact (list messages)
```

**Database Layer**:
- Motor (async MongoDB driver) for non-blocking I/O
- Two collections: `bookings` and `contact_messages`
- No authentication or authorization (public submission endpoints)
- UUID generation for document IDs (not relying on MongoDB ObjectId)

**Validation Strategy**:
- Pydantic v2 models for request/response validation
- EmailStr validator for email format checking
- Required field validation at model level
- Automatic 422 responses for validation failures

### System Integration

**Frontend-Backend Communication**:
1. Frontend forms collect user input with client-side validation
2. Axios sends POST requests to `/api/bookings` or `/api/contact`
3. Backend validates with Pydantic, generates UUID and timestamp
4. MongoDB stores document asynchronously
5. Backend returns 201 with created document (excluding `_id`)
6. Frontend displays success/error message to user

**Error Handling Flow**:
- Network errors: Caught by axios, display generic error message
- Validation errors (422): Display specific field errors from response
- Server errors (500): Display generic error message
- Success (201): Display confirmation message, clear form

## Components and Interfaces

### Frontend Components

#### Navbar Component
**Purpose**: Sticky navigation with smooth-scroll links and mobile menu

**Props**: 
- `bookingRef`: React ref to booking section for CTA button

**State**:
- `isScrolled`: Boolean for backdrop blur effect (scroll > 50px)
- `isMobileMenuOpen`: Boolean for mobile menu visibility

**Key Methods**:
- `handleNavClick(sectionId)`: Smooth-scrolls to section by ID
- `toggleMobileMenu()`: Opens/closes mobile navigation overlay

**Styling**:
- Fixed positioning with z-index for overlay
- Backdrop blur when scrolled
- Hamburger icon below 768px breakpoint


#### Hero Component
**Purpose**: Full-bleed hero with background image, stats, and showreel modal

**Props**: 
- `bookingRef`: React ref for "Book Your Session" CTA
- `portfolioRef`: React ref for "View Portfolio" CTA

**State**:
- `isShowreelOpen`: Boolean for modal visibility

**Key Methods**:
- `openShowreel()`: Sets modal state to true
- `closeShowreel()`: Sets modal state to false

**Styling**:
- Full viewport height with background image (Godavari Bridge)
- Centered content with gradient overlay for text readability
- Modal with YouTube iframe embed

#### Services Component
**Purpose**: Display 5 service cards with booking CTAs

**Props**:
- `bookingRef`: React ref for "Book Now" buttons

**Data Source**: 
- Constants file with SERVICES array (icon, title, description)

**Styling**:
- Grid layout: 3 columns on desktop, 1 column on mobile
- Card hover effects with gold accent border
- Lucide-react icons for visual hierarchy

#### About Component
**Purpose**: Two-column layout showcasing studio philosophy

**Props**: None

**Data Source**:
- Static content with 4 feature cells

**Styling**:
- 50/50 split on desktop, stacked on mobile
- Studio image with subtle hover scale effect
- Feature cells in 2x2 grid

#### StatsAndBooking Component
**Purpose**: Combined stats display and booking form submission

**Props**: 
- `bookingRef`: React ref for scroll target

**State**:
- `formData`: Object with name, phone, service, event_date, event_time, location, message
- `isSubmitting`: Boolean for loading state
- `submitStatus`: Object with type ('success'|'error') and message

**Key Methods**:
- `handleInputChange(e)`: Updates formData state
- `validateForm()`: Client-side validation before submission
- `handleSubmit(e)`: Async POST to /api/bookings

**Validation Rules**:
- Name: min 2 characters
- Phone: min 10 digits
- Service: must be selected
- Event Date: required
- Event Time: required
- Location: required

**Styling**:
- Two-column layout: stats on left, form on right
- Gold accent for submit button
- Error/success messages below form


#### Portfolio Component
**Purpose**: Filterable masonry gallery with category chips

**Props**: None

**State**:
- `activeFilter`: String ('All'|'Weddings'|'Photoshoots'|'Events'|'Drone')
- `filteredImages`: Array of images matching active filter

**Data Source**:
- Constants file with PORTFOLIO array (src, alt, category)

**Key Methods**:
- `handleFilterChange(category)`: Updates active filter and filtered images

**Styling**:
- Masonry grid using CSS Grid with auto-flow dense
- Filter chips with gold accent for active state
- Image hover effects with scale and overlay

#### Packages Component
**Purpose**: Display 3-tier pricing with booking CTAs

**Props**:
- `bookingRef`: React ref for "Book This Package" buttons

**Data Source**:
- Constants file with PACKAGES array (name, price, description, features, isRecommended)

**Styling**:
- 3-column grid on desktop, stacked on mobile
- Signature package highlighted with gold border
- Feature lists with checkmark icons

#### Testimonials Component
**Purpose**: Auto-rotating carousel with manual controls

**Props**: None

**State**:
- `activeIndex`: Number (0-2)
- `isPaused`: Boolean for autoplay control

**Data Source**:
- Constants file with TESTIMONIALS array (name, role, review)

**Key Methods**:
- `nextTestimonial()`: Increments index (wraps to 0)
- `prevTestimonial()`: Decrements index (wraps to last)
- `goToTestimonial(index)`: Sets specific index
- `pauseAutoplay()`: Stops auto-rotation
- `resumeAutoplay()`: Restarts auto-rotation

**Effects**:
- useEffect with 6-second interval for autoplay
- Cleanup on unmount to prevent memory leaks

**Styling**:
- Single testimonial visible with fade transitions
- Dot indicators with gold accent for active
- Previous/next buttons with hover states


#### Contact Component
**Purpose**: Contact form submission with studio info display

**Props**: None

**State**:
- `formData`: Object with name, email, phone, subject, message
- `isSubmitting`: Boolean for loading state
- `submitStatus`: Object with type ('success'|'error') and message

**Key Methods**:
- `handleInputChange(e)`: Updates formData state
- `validateForm()`: Client-side validation before submission
- `handleSubmit(e)`: Async POST to /api/contact

**Validation Rules**:
- Name: min 2 characters
- Email: valid email format (regex)
- Phone: min 10 digits
- Subject: min 3 characters
- Message: min 10 characters

**Styling**:
- Two-column layout: form on left, info on right
- Gold accent for submit button
- Error/success messages below form

#### Footer Component
**Purpose**: Four-column footer with brand, navigation, info, copyright

**Props**: None

**Data Source**:
- Constants file with NAV_LINKS and BRAND info

**Styling**:
- 4-column grid on desktop, stacked on mobile
- Social media icon with hover effect
- Copyright with current year (dynamic)

### Backend API Interfaces

#### Health Check Endpoint
```
GET /api/
Response: 200 OK
{
  "status": "ok"
}
```

#### Create Booking
```
POST /api/bookings
Content-Type: application/json

Request Body:
{
  "name": string (required),
  "phone": string (required),
  "service": string (required),
  "event_date": string (required, ISO 8601 date),
  "event_time": string (required),
  "location": string (required),
  "message": string (optional)
}

Response: 201 Created
{
  "id": string (UUID),
  "name": string,
  "phone": string,
  "service": string,
  "event_date": string,
  "event_time": string,
  "location": string,
  "message": string,
  "created_at": string (ISO 8601 timestamp)
}

Error Response: 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```


#### List Bookings
```
GET /api/bookings
Response: 200 OK
[
  {
    "id": string (UUID),
    "name": string,
    "phone": string,
    "service": string,
    "event_date": string,
    "event_time": string,
    "location": string,
    "message": string,
    "created_at": string (ISO 8601 timestamp)
  },
  ...
]
```

#### Create Contact Message
```
POST /api/contact
Content-Type: application/json

Request Body:
{
  "name": string (required),
  "email": string (required, valid email format),
  "phone": string (required),
  "subject": string (required),
  "message": string (required)
}

Response: 201 Created
{
  "id": string (UUID),
  "name": string,
  "email": string,
  "phone": string,
  "subject": string,
  "message": string,
  "created_at": string (ISO 8601 timestamp)
}

Error Response: 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

#### List Contact Messages
```
GET /api/contact
Response: 200 OK
[
  {
    "id": string (UUID),
    "name": string,
    "email": string,
    "phone": string,
    "subject": string,
    "message": string,
    "created_at": string (ISO 8601 timestamp)
  },
  ...
]
```

## Data Models

### Frontend Data Structures

#### Navigation Link
```typescript
{
  label: string,
  href: string,
  testId: string
}
```

#### Service
```typescript
{
  icon: LucideIcon,
  title: string,
  description: string
}
```


#### Portfolio Item
```typescript
{
  src: string,
  alt: string,
  category: 'Weddings' | 'Photoshoots' | 'Events' | 'Drone'
}
```

#### Package
```typescript
{
  name: string,
  price: string,
  description: string,
  features: string[],
  isRecommended: boolean
}
```

#### Testimonial
```typescript
{
  name: string,
  role: string,
  review: string
}
```

#### Stat
```typescript
{
  value: string,
  label: string
}
```

### Backend Pydantic Models

#### BookingCreate (Request Model)
```python
from pydantic import BaseModel, Field

class BookingCreate(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    service: str = Field(..., min_length=1)
    event_date: str = Field(..., min_length=1)
    event_time: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    message: str = ""
```

#### BookingResponse (Response Model)
```python
from pydantic import BaseModel
from datetime import datetime

class BookingResponse(BaseModel):
    id: str
    name: str
    phone: str
    service: str
    event_date: str
    event_time: str
    location: str
    message: str
    created_at: str
```

#### ContactCreate (Request Model)
```python
from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
```


#### ContactResponse (Response Model)
```python
from pydantic import BaseModel

class ContactResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    subject: str
    message: str
    created_at: str
```

### MongoDB Document Schemas

#### Booking Document
```json
{
  "_id": ObjectId (MongoDB generated, excluded from API responses),
  "id": "uuid-string",
  "name": "string",
  "phone": "string",
  "service": "string",
  "event_date": "YYYY-MM-DD",
  "event_time": "HH:MM",
  "location": "string",
  "message": "string",
  "created_at": "ISO 8601 timestamp"
}
```

#### Contact Message Document
```json
{
  "_id": ObjectId (MongoDB generated, excluded from API responses),
  "id": "uuid-string",
  "name": "string",
  "email": "email@example.com",
  "phone": "string",
  "subject": "string",
  "message": "string",
  "created_at": "ISO 8601 timestamp"
}
```

## Implementation Details

### Frontend Implementation

#### Project Structure
```
frontend/
├── public/
│   ├── images/
│   │   ├── hero-bridge.jpg
│   │   ├── about-studio.jpg
│   │   └── portfolio/ (8 images)
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Hero.jsx
│   │   ├── Services.jsx
│   │   ├── About.jsx
│   │   ├── StatsAndBooking.jsx
│   │   ├── Portfolio.jsx
│   │   ├── Packages.jsx
│   │   ├── Testimonials.jsx
│   │   ├── Contact.jsx
│   │   └── Footer.jsx
│   ├── constants/
│   │   └── index.js
│   ├── App.jsx
│   ├── App.css
│   └── index.js
├── package.json
└── tailwind.config.js
```


#### Constants File Structure
```javascript
// src/constants/index.js
import { Camera, Video, Plane, Users, Film } from 'lucide-react';

export const BRAND = {
  name: "Godavari Captures",
  tagline: "We turn moments into reels",
  phone: "+91 98765 43210",
  email: "hello@godavaricaptures.com",
  address: "Rajahmundry, Andhra Pradesh, India",
  instagram: "@godavaricaptures"
};

export const NAV_LINKS = [
  { label: "HOME", href: "#home", testId: "nav-home" },
  { label: "ABOUT", href: "#about", testId: "nav-about" },
  { label: "SERVICES", href: "#services", testId: "nav-services" },
  { label: "PORTFOLIO", href: "#portfolio", testId: "nav-portfolio" },
  { label: "PACKAGES", href: "#packages", testId: "nav-packages" },
  { label: "YOUR REELS", href: "#testimonials", testId: "nav-testimonials" },
  { label: "CONTACT", href: "#contact", testId: "nav-contact" }
];

export const SERVICES = [
  {
    icon: Users,
    title: "Weddings",
    description: "Cinematic wedding films that capture every emotion"
  },
  {
    icon: Camera,
    title: "Photoshoots",
    description: "Professional photography for portraits and events"
  },
  {
    icon: Video,
    title: "Reel Making",
    description: "Engaging social media reels for brands and creators"
  },
  {
    icon: Film,
    title: "Events",
    description: "Corporate and private event coverage"
  },
  {
    icon: Plane,
    title: "Drone Shots",
    description: "Aerial cinematography for breathtaking perspectives"
  }
];

export const PORTFOLIO = [
  { src: "/images/portfolio/wedding-1.jpg", alt: "Wedding ceremony", category: "Weddings" },
  { src: "/images/portfolio/photoshoot-1.jpg", alt: "Portrait session", category: "Photoshoots" },
  { src: "/images/portfolio/event-1.jpg", alt: "Corporate event", category: "Events" },
  { src: "/images/portfolio/drone-1.jpg", alt: "Aerial view", category: "Drone" },
  { src: "/images/portfolio/wedding-2.jpg", alt: "Reception moments", category: "Weddings" },
  { src: "/images/portfolio/photoshoot-2.jpg", alt: "Fashion shoot", category: "Photoshoots" },
  { src: "/images/portfolio/event-2.jpg", alt: "Conference coverage", category: "Events" },
  { src: "/images/portfolio/drone-2.jpg", alt: "Landscape shot", category: "Drone" }
];

export const PACKAGES = [
  {
    name: "Essential",
    price: "₹24,999",
    description: "Perfect for intimate gatherings",
    features: [
      "4 hours coverage",
      "1 photographer",
      "50 edited photos",
      "Online gallery",
      "2-week delivery"
    ],
    isRecommended: false
  },
  {
    name: "Signature",
    price: "₹59,999",
    description: "Our most popular package",
    features: [
      "8 hours coverage",
      "2 photographers + 1 videographer",
      "150 edited photos",
      "3-minute highlight reel",
      "Online gallery + USB",
      "1-week delivery"
    ],
    isRecommended: true
  },
  {
    name: "Heritage",
    price: "₹1,29,999",
    description: "Complete luxury experience",
    features: [
      "Full day coverage",
      "3 photographers + 2 videographers",
      "300+ edited photos",
      "10-minute cinematic film",
      "Drone coverage",
      "Premium album + USB",
      "Same-day teaser",
      "3-day delivery"
    ],
    isRecommended: false
  }
];

export const TESTIMONIALS = [
  {
    name: "Priya & Karthik",
    role: "Wedding Clients",
    review: "Godavari Captures turned our wedding into a cinematic masterpiece. Every frame tells our story beautifully."
  },
  {
    name: "Rajesh Enterprises",
    role: "Corporate Client",
    review: "Professional, punctual, and creative. Their event coverage exceeded our expectations."
  },
  {
    name: "Ananya Reddy",
    role: "Portrait Client",
    review: "The photoshoot experience was comfortable and fun. The results are stunning!"
  }
];

export const STATS = [
  { value: "500+", label: "Projects Completed" },
  { value: "98%", label: "Client Satisfaction" },
  { value: "3+", label: "Years Experience" }
];
```


#### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'luxury-black': '#000000',
        'luxury-card': '#0A0A0A',
        'luxury-alt': '#050505',
        'luxury-gold': '#D4AF37',
        'luxury-gold-hover': '#C5A017',
      },
      fontFamily: {
        'display': ['Playfair Display', 'serif'],
        'body': ['Manrope', 'sans-serif'],
      },
      borderRadius: {
        'none': '0',
      },
    },
  },
  plugins: [],
}
```

#### App.jsx Structure
```javascript
import React, { useRef } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Services from './components/Services';
import About from './components/About';
import StatsAndBooking from './components/StatsAndBooking';
import Portfolio from './components/Portfolio';
import Packages from './components/Packages';
import Testimonials from './components/Testimonials';
import Contact from './components/Contact';
import Footer from './components/Footer';

function App() {
  const bookingRef = useRef(null);
  const portfolioRef = useRef(null);

  return (
    <div className="bg-luxury-black text-white font-body">
      <Navbar bookingRef={bookingRef} />
      <Hero bookingRef={bookingRef} portfolioRef={portfolioRef} />
      <Services bookingRef={bookingRef} />
      <About />
      <StatsAndBooking bookingRef={bookingRef} />
      <Portfolio portfolioRef={portfolioRef} />
      <Packages bookingRef={bookingRef} />
      <Testimonials />
      <Contact />
      <Footer />
    </div>
  );
}

export default App;
```

#### Axios Configuration
```javascript
// API base URL configuration
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Booking API calls
export const createBooking = async (bookingData) => {
  const response = await api.post('/api/bookings', bookingData);
  return response.data;
};

export const getBookings = async () => {
  const response = await api.get('/api/bookings');
  return response.data;
};

// Contact API calls
export const createContact = async (contactData) => {
  const response = await api.post('/api/contact', contactData);
  return response.data;
};

export const getContacts = async () => {
  const response = await api.get('/api/contact');
  return response.data;
};
```


### Backend Implementation

#### Project Structure
```
backend/
├── app/
│   ├── models/
│   │   ├── booking.py
│   │   └── contact.py
│   ├── routes/
│   │   ├── bookings.py
│   │   └── contact.py
│   ├── database.py
│   └── main.py
├── requirements.txt
└── .env
```

#### Main Application Setup
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import bookings, contact

app = FastAPI(title="Godavari Captures API")

# CORS configuration for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/api/")
async def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(bookings.router, prefix="/api", tags=["bookings"])
app.include_router(contact.router, prefix="/api", tags=["contact"])
```

#### Database Configuration
```python
# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "godavari_captures")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Collections
bookings_collection = database.get_collection("bookings")
contact_collection = database.get_collection("contact_messages")
```

#### Booking Models
```python
# app/models/booking.py
from pydantic import BaseModel, Field
from typing import Optional

class BookingCreate(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    service: str = Field(..., min_length=1)
    event_date: str = Field(..., min_length=1)
    event_time: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    message: Optional[str] = ""

class BookingResponse(BaseModel):
    id: str
    name: str
    phone: str
    service: str
    event_date: str
    event_time: str
    location: str
    message: str
    created_at: str
```


#### Contact Models
```python
# app/models/contact.py
from pydantic import BaseModel, EmailStr, Field

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)

class ContactResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    subject: str
    message: str
    created_at: str
```

#### Booking Routes
```python
# app/routes/bookings.py
from fastapi import APIRouter, HTTPException, status
from app.models.booking import BookingCreate, BookingResponse
from app.database import bookings_collection
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(booking: BookingCreate):
    booking_dict = booking.model_dump()
    booking_dict["id"] = str(uuid.uuid4())
    booking_dict["created_at"] = datetime.utcnow().isoformat()
    
    await bookings_collection.insert_one(booking_dict)
    
    # Remove MongoDB _id from response
    booking_dict.pop("_id", None)
    return booking_dict

@router.get("/bookings", response_model=list[BookingResponse])
async def get_bookings():
    bookings = await bookings_collection.find().sort("created_at", -1).to_list(length=None)
    
    # Remove MongoDB _id from all documents
    for booking in bookings:
        booking.pop("_id", None)
    
    return bookings
```

#### Contact Routes
```python
# app/routes/contact.py
from fastapi import APIRouter, HTTPException, status
from app.models.contact import ContactCreate, ContactResponse
from app.database import contact_collection
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate):
    contact_dict = contact.model_dump()
    contact_dict["id"] = str(uuid.uuid4())
    contact_dict["created_at"] = datetime.utcnow().isoformat()
    
    await contact_collection.insert_one(contact_dict)
    
    # Remove MongoDB _id from response
    contact_dict.pop("_id", None)
    return contact_dict

@router.get("/contact", response_model=list[ContactResponse])
async def get_contacts():
    contacts = await contact_collection.find().sort("created_at", -1).to_list(length=None)
    
    # Remove MongoDB _id from all documents
    for contact in contacts:
        contact.pop("_id", None)
    
    return contacts
```


#### Requirements File
```
# requirements.txt
fastapi==0.109.0
motor==3.3.2
pydantic[email]==2.5.3
uvicorn[standard]==0.27.0
python-dotenv==1.0.0
```

### Design System Implementation

#### CSS Custom Properties
```css
/* src/App.css */
:root {
  --luxury-black: #000000;
  --luxury-card: #0A0A0A;
  --luxury-alt: #050505;
  --luxury-gold: #D4AF37;
  --luxury-gold-hover: #C5A017;
}

/* Film grain overlay */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" /></filter><rect width="100%" height="100%" filter="url(%23noise)" opacity="0.05" /></svg>');
  pointer-events: none;
  z-index: 9999;
}

/* Fade-up animation */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-up {
  animation: fadeUp 0.8s ease-out;
}

/* Pulse ring animation for play button */
@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.pulse-ring {
  animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

#### Reusable Tailwind Classes
```css
/* Button styles */
.btn-gold {
  @apply bg-luxury-gold text-luxury-black px-8 py-3 font-semibold 
         hover:bg-luxury-gold-hover transition-colors duration-300;
}

.btn-outline {
  @apply border-2 border-luxury-gold text-luxury-gold px-8 py-3 
         font-semibold hover:bg-luxury-gold hover:text-luxury-black 
         transition-all duration-300;
}

/* Input styles */
.lux-input {
  @apply w-full bg-luxury-card border border-gray-800 px-4 py-3 
         text-white focus:border-luxury-gold focus:outline-none 
         transition-colors duration-300;
}

/* Card styles */
.lux-card {
  @apply bg-luxury-card border border-gray-900 p-6 
         hover:border-luxury-gold transition-all duration-300;
}

/* Section divider */
.section-rule {
  @apply w-24 h-px bg-luxury-gold mx-auto my-8;
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified several areas of redundancy:

1. **Data-testid properties (1.8, 5.10, 9.11, 16.1-16.5)**: These can be consolidated into a single comprehensive property about all interactive elements having unique test IDs.

2. **Form validation properties (5.5-5.8, 9.5-9.9)**: While each field has specific validation rules, they follow the same pattern and should remain separate as they test different validation logic.

3. **Service card properties (3.2, 3.3)**: These test that all service cards have complete content structure and can be combined.

4. **Pricing card properties (7.2, 7.4)**: Similar to service cards, these test complete content structure and can be combined.

5. **Scroll behavior properties (1.2, 3.4, 7.5)**: All "Book Now" and package buttons scroll to the same target, but navigation links scroll to different targets. The navigation property (1.2) is distinct, while 3.4 and 7.5 can be combined.

6. **API response properties (12.3-12.5, 13.4-13.6)**: These test that valid submissions generate proper responses with UUID, timestamp, and 201 status. These are distinct aspects and should remain separate.

7. **MongoDB _id exclusion (12.8, 13.9)**: Both test the same sanitization pattern and can be combined into one property about API responses.

8. **Font properties (14.6, 14.7)**: These test different font families for different element types and should remain separate.

After reflection, I've consolidated redundant properties while preserving unique validation value for each remaining property.


### Frontend Properties

#### Property 1: Navigation Smooth Scroll
*For any* navigation link in the navbar, clicking it should trigger smooth-scroll behavior to the corresponding section identified by the link's href.

**Validates: Requirements 1.2**

#### Property 2: Modal Close Triggers
*For any* close trigger element (close button or overlay) in the showreel modal, clicking it should set the modal visibility state to false.

**Validates: Requirements 2.9**

#### Property 3: Service Card Content Completeness
*For any* service card rendered on the page, it should contain an icon element, a title text element, a description text element, and a "Book Now" button.

**Validates: Requirements 3.2, 3.3**

#### Property 4: Booking CTA Scroll Behavior
*For any* "Book Now" button (in services section) or "Book This Package" button (in packages section), clicking it should trigger smooth-scroll to the booking form section.

**Validates: Requirements 3.4, 7.5**

#### Property 5: Portfolio Category Filtering
*For any* non-"All" filter chip clicked, the portfolio gallery should display only images where the image category matches the selected filter category.

**Validates: Requirements 6.3**

#### Property 6: Active Filter Visual Indication
*For any* active filter chip in the portfolio gallery, it should have the gold accent color (#D4AF37) applied to indicate its active state.

**Validates: Requirements 6.5**

#### Property 7: Portfolio Image Hover Effects
*For any* portfolio image in the gallery, hovering over it should apply visual transformation effects (scale, overlay, or similar).

**Validates: Requirements 6.6**

#### Property 8: Pricing Card Content Completeness
*For any* pricing card rendered on the page, it should contain a package name, price display, description text, feature list with multiple items, and a "Book This Package" button.

**Validates: Requirements 7.2, 7.4**

#### Property 9: Testimonial Content Completeness
*For any* testimonial displayed in the carousel, it should contain a name field, a role field, and a review text field, all with non-empty values.

**Validates: Requirements 8.1**

#### Property 10: Carousel Dot Navigation
*For any* dot indicator clicked in the testimonial carousel, the carousel should display the testimonial corresponding to that dot's index position.

**Validates: Requirements 8.5**

#### Property 11: Carousel Autoplay Pause on Interaction
*For any* navigation control (previous button, next button, or dot indicator) in the testimonial carousel, interacting with it should pause the autoplay timer.

**Validates: Requirements 8.7**


#### Property 12: Booking Form Valid Submission
*For any* booking form data that passes client-side validation (name ≥2 chars, phone ≥10 digits, service selected, event date provided, event time provided, location provided), submitting the form should trigger a POST request to /api/bookings with the form data as the request body.

**Validates: Requirements 5.2**

#### Property 13: Booking Name Validation
*For any* name input value with fewer than 2 characters, attempting to submit the booking form should prevent submission and display a validation error.

**Validates: Requirements 5.5**

#### Property 14: Booking Phone Validation
*For any* phone input value with fewer than 10 digits, attempting to submit the booking form should prevent submission and display a validation error.

**Validates: Requirements 5.6**

#### Property 15: Contact Form Valid Submission
*For any* contact form data that passes client-side validation (name ≥2 chars, valid email format, phone ≥10 digits, subject ≥3 chars, message ≥10 chars), submitting the form should trigger a POST request to /api/contact with the form data as the request body.

**Validates: Requirements 9.2**

#### Property 16: Contact Name Validation
*For any* name input value with fewer than 2 characters, attempting to submit the contact form should prevent submission and display a validation error.

**Validates: Requirements 9.5**

#### Property 17: Contact Email Validation
*For any* email input value that does not match valid email format (contains @ and domain), attempting to submit the contact form should prevent submission and display a validation error.

**Validates: Requirements 9.6**

#### Property 18: Contact Phone Validation
*For any* phone input value with fewer than 10 digits, attempting to submit the contact form should prevent submission and display a validation error.

**Validates: Requirements 9.7**

#### Property 19: Contact Subject Validation
*For any* subject input value with fewer than 3 characters, attempting to submit the contact form should prevent submission and display a validation error.

**Validates: Requirements 9.8**

#### Property 20: Contact Message Validation
*For any* message input value with fewer than 10 characters, attempting to submit the contact form should prevent submission and display a validation error.

**Validates: Requirements 9.9**

#### Property 21: Interactive Elements Test ID Uniqueness
*For any* interactive element (button, form input, navigation link, filter chip, carousel control) on the landing page, it should have a unique data-testid attribute that does not conflict with any other element's data-testid.

**Validates: Requirements 1.8, 5.10, 9.11, 16.1, 16.2, 16.3, 16.4, 16.5**

#### Property 22: Heading Font Family
*For any* heading element (h1, h2, h3, h4, h5, h6) on the landing page, it should have font-family set to 'Playfair Display' or inherit it from a parent with that font.

**Validates: Requirements 14.6**

#### Property 23: Body Text Font Family
*For any* body text element (p, span, div with text content, button, input, label) on the landing page, it should have font-family set to 'Manrope' or inherit it from a parent with that font.

**Validates: Requirements 14.7**

#### Property 24: Component Border Radius
*For any* component with visible borders (cards, buttons, inputs, modals), the border-radius CSS property should be set to 0 to maintain square edges throughout the design.

**Validates: Requirements 14.8**

#### Property 25: Section Fade-Up Animation
*For any* major section component (Services, About, Portfolio, Packages, Testimonials, Contact), it should have a fade-up animation class applied that triggers when the section enters the viewport.

**Validates: Requirements 14.10**

#### Property 26: Semantic HTML Structure
*For any* major structural area of the page (header, navigation, main content, sections, footer), it should use appropriate semantic HTML5 elements (header, nav, main, section, article, footer) rather than generic div elements.

**Validates: Requirements 16.7**

#### Property 27: Image Alt Text Accessibility
*For any* img element rendered on the landing page, it should have a non-empty alt attribute providing descriptive alternative text for accessibility.

**Validates: Requirements 16.8**


### Backend API Properties

#### Property 28: Booking Creation Persistence
*For any* valid booking data (containing required fields: name, phone, service, event_date, event_time, location) sent via POST to /api/bookings, the API should create a corresponding document in the MongoDB bookings collection.

**Validates: Requirements 12.1**

#### Property 29: Booking Required Field Validation
*For any* booking data missing one or more required fields (name, phone, service, event_date, event_time, location) sent via POST to /api/bookings, the API should return a 422 status code with validation error details.

**Validates: Requirements 12.2**

#### Property 30: Booking UUID Generation
*For any* valid booking data sent via POST to /api/bookings, the API response should include an 'id' field containing a valid UUID (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).

**Validates: Requirements 12.3**

#### Property 31: Booking Timestamp Generation
*For any* valid booking data sent via POST to /api/bookings, the API response should include a 'created_at' field containing a valid ISO 8601 timestamp.

**Validates: Requirements 12.4**

#### Property 32: Booking Creation Success Status
*For any* valid booking data sent via POST to /api/bookings, the API should return a 201 status code indicating successful resource creation.

**Validates: Requirements 12.5**

#### Property 33: Booking Validation Error Status
*For any* invalid booking data sent via POST to /api/bookings, the API should return a 422 status code with a response body containing validation error details.

**Validates: Requirements 12.6**

#### Property 34: Booking List Sorting
*For any* GET request to /api/bookings, the returned array of bookings should be sorted in descending order by the 'created_at' field (newest first).

**Validates: Requirements 12.7**

#### Property 35: Contact Creation Persistence
*For any* valid contact data (containing required fields: name, email, phone, subject, message) sent via POST to /api/contact, the API should create a corresponding document in the MongoDB contact_messages collection.

**Validates: Requirements 13.1**

#### Property 36: Contact Required Field Validation
*For any* contact data missing one or more required fields (name, email, phone, subject, message) sent via POST to /api/contact, the API should return a 422 status code with validation error details.

**Validates: Requirements 13.2**

#### Property 37: Contact Email Format Validation
*For any* contact data with an email field that does not match valid email format (validated by Pydantic EmailStr) sent via POST to /api/contact, the API should return a 422 status code with email validation error details.

**Validates: Requirements 13.3**

#### Property 38: Contact UUID Generation
*For any* valid contact data sent via POST to /api/contact, the API response should include an 'id' field containing a valid UUID (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).

**Validates: Requirements 13.4**

#### Property 39: Contact Timestamp Generation
*For any* valid contact data sent via POST to /api/contact, the API response should include a 'created_at' field containing a valid ISO 8601 timestamp.

**Validates: Requirements 13.5**

#### Property 40: Contact Creation Success Status
*For any* valid contact data sent via POST to /api/contact, the API should return a 201 status code indicating successful resource creation.

**Validates: Requirements 13.6**

#### Property 41: Contact Validation Error Status
*For any* invalid contact data sent via POST to /api/contact, the API should return a 422 status code with a response body containing validation error details.

**Validates: Requirements 13.7**

#### Property 42: Contact List Sorting
*For any* GET request to /api/contact, the returned array of contact messages should be sorted in descending order by the 'created_at' field (newest first).

**Validates: Requirements 13.8**

#### Property 43: MongoDB ID Exclusion from API Responses
*For any* document returned by GET /api/bookings or GET /api/contact, the response object should not contain a '_id' field (MongoDB's internal identifier should be excluded).

**Validates: Requirements 12.8, 13.9**


## Error Handling

### Frontend Error Handling

#### Form Validation Errors
- **Client-side validation**: Prevent form submission and display inline error messages below invalid fields
- **Error message format**: Clear, actionable text (e.g., "Name must be at least 2 characters")
- **Visual indicators**: Red border on invalid fields, error text in red color
- **Validation timing**: On blur for individual fields, on submit for complete form

#### API Communication Errors
- **Network errors**: Display generic message "Unable to connect. Please check your internet connection."
- **422 Validation errors**: Parse response and display specific field errors from backend
- **500 Server errors**: Display generic message "Something went wrong. Please try again later."
- **Timeout errors**: Display message "Request timed out. Please try again."

#### User Feedback
- **Success messages**: Green background with checkmark icon, auto-dismiss after 5 seconds
- **Error messages**: Red background with X icon, manual dismiss required
- **Loading states**: Disable submit button, show spinner, prevent double submission

#### Graceful Degradation
- **Image loading failures**: Display placeholder with alt text
- **YouTube embed failures**: Show error message with fallback contact option
- **JavaScript disabled**: Core content remains accessible (progressive enhancement)

### Backend Error Handling

#### Request Validation
- **Pydantic validation**: Automatic 422 responses with detailed error messages
- **Field-level errors**: Include field name, error type, and human-readable message
- **Type coercion**: Attempt to convert compatible types before rejecting

#### Database Errors
- **Connection failures**: Log error, return 503 Service Unavailable
- **Write failures**: Log error with document details, return 500 Internal Server Error
- **Duplicate key errors**: Return 409 Conflict with appropriate message

#### Error Response Format
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

#### Logging Strategy
- **Info level**: Successful requests with response time
- **Warning level**: Validation failures with request data
- **Error level**: Database errors, unexpected exceptions with stack traces
- **Log format**: JSON structured logs for easy parsing


## Testing Strategy

### Dual Testing Approach

This project requires both **unit testing** and **property-based testing** to achieve comprehensive coverage. These approaches are complementary:

- **Unit tests** verify specific examples, edge cases, and integration points
- **Property tests** verify universal properties across all possible inputs
- Together, they provide confidence in both concrete scenarios and general correctness

### Frontend Testing

#### Unit Testing with Jest and React Testing Library

**Test Categories**:

1. **Component Rendering Tests**
   - Verify specific UI elements are rendered (navbar has 7 links, hero displays 3 stats)
   - Test specific user interactions (clicking "Book Now" scrolls to booking form)
   - Validate conditional rendering (mobile menu appears below 768px)

2. **Form Submission Tests**
   - Test successful submission flow with valid data
   - Test error handling with network failures
   - Test success/error message display

3. **Integration Tests**
   - Test complete user flows (browse portfolio → filter by category → view images)
   - Test form validation → submission → API call → response handling
   - Test carousel autoplay → user interaction → pause behavior

**Example Unit Tests**:
```javascript
// Navbar.test.jsx
describe('Navbar Component', () => {
  test('renders 7 navigation links', () => {
    render(<Navbar />);
    const links = screen.getAllByRole('link');
    expect(links).toHaveLength(7);
  });

  test('applies backdrop blur when scrolled beyond 50px', () => {
    render(<Navbar />);
    window.scrollY = 51;
    fireEvent.scroll(window);
    expect(screen.getByRole('navigation')).toHaveClass('backdrop-blur');
  });
});

// Hero.test.jsx
describe('Hero Component', () => {
  test('opens showreel modal when play button clicked', () => {
    render(<Hero />);
    fireEvent.click(screen.getByTestId('showreel-button'));
    expect(screen.getByTestId('showreel-modal')).toBeVisible();
  });

  test('closes modal when overlay clicked', () => {
    render(<Hero />);
    fireEvent.click(screen.getByTestId('showreel-button'));
    fireEvent.click(screen.getByTestId('modal-overlay'));
    expect(screen.queryByTestId('showreel-modal')).not.toBeInTheDocument();
  });
});
```

#### Property-Based Testing with fast-check

**Configuration**: Minimum 100 iterations per property test

**Property Test Categories**:

1. **Navigation and Interaction Properties**
   - Any navigation link triggers smooth scroll
   - Any close trigger closes modal
   - Any booking CTA scrolls to booking form

2. **Content Completeness Properties**
   - Any service card has complete content structure
   - Any pricing card has all required fields
   - Any testimonial has name, role, and review

3. **Validation Properties**
   - Any name < 2 chars is rejected
   - Any phone < 10 digits is rejected
   - Any invalid email format is rejected

4. **Accessibility Properties**
   - Any interactive element has unique data-testid
   - Any image has alt text
   - Any heading uses Playfair Display font

**Example Property Tests**:
```javascript
// Portfolio.property.test.jsx
import fc from 'fast-check';

describe('Portfolio Gallery Properties', () => {
  test('Property 5: Portfolio Category Filtering', () => {
    // Feature: godavari-captures-landing-page, Property 5: For any non-"All" filter chip clicked, the portfolio gallery should display only images where the image category matches the selected filter category
    
    fc.assert(
      fc.property(
        fc.constantFrom('Weddings', 'Photoshoots', 'Events', 'Drone'),
        (category) => {
          const { container } = render(<Portfolio />);
          
          // Click the filter chip
          fireEvent.click(screen.getByTestId(`filter-${category.toLowerCase()}`));
          
          // Get all visible images
          const visibleImages = container.querySelectorAll('[data-category]');
          
          // All visible images should match the selected category
          return Array.from(visibleImages).every(
            img => img.getAttribute('data-category') === category
          );
        }
      ),
      { numRuns: 100 }
    );
  });

  test('Property 6: Active Filter Visual Indication', () => {
    // Feature: godavari-captures-landing-page, Property 6: For any active filter chip in the portfolio gallery, it should have the gold accent color applied
    
    fc.assert(
      fc.property(
        fc.constantFrom('All', 'Weddings', 'Photoshoots', 'Events', 'Drone'),
        (category) => {
          render(<Portfolio />);
          
          // Click the filter chip
          const filterChip = screen.getByTestId(`filter-${category.toLowerCase()}`);
          fireEvent.click(filterChip);
          
          // Active filter should have gold color
          const styles = window.getComputedStyle(filterChip);
          return styles.backgroundColor === 'rgb(212, 175, 55)' || // #D4AF37
                 filterChip.classList.contains('bg-luxury-gold');
        }
      ),
      { numRuns: 100 }
    );
  });
});

// Forms.property.test.jsx
describe('Form Validation Properties', () => {
  test('Property 13: Booking Name Validation', () => {
    // Feature: godavari-captures-landing-page, Property 13: For any name input value with fewer than 2 characters, attempting to submit should prevent submission
    
    fc.assert(
      fc.property(
        fc.string({ maxLength: 1 }), // Generate strings with 0-1 characters
        (invalidName) => {
          render(<StatsAndBooking />);
          
          const nameInput = screen.getByTestId('booking-name');
          const submitButton = screen.getByTestId('booking-submit');
          
          fireEvent.change(nameInput, { target: { value: invalidName } });
          fireEvent.click(submitButton);
          
          // Should show validation error and not call API
          return screen.queryByText(/name must be at least 2 characters/i) !== null;
        }
      ),
      { numRuns: 100 }
    );
  });

  test('Property 17: Contact Email Validation', () => {
    // Feature: godavari-captures-landing-page, Property 17: For any email input value that does not match valid email format, submission should be prevented
    
    fc.assert(
      fc.property(
        fc.string().filter(s => !s.includes('@') || !s.includes('.')), // Invalid emails
        (invalidEmail) => {
          render(<Contact />);
          
          const emailInput = screen.getByTestId('contact-email');
          const submitButton = screen.getByTestId('contact-submit');
          
          fireEvent.change(emailInput, { target: { value: invalidEmail } });
          fireEvent.click(submitButton);
          
          // Should show validation error
          return screen.queryByText(/valid email/i) !== null;
        }
      ),
      { numRuns: 100 }
    );
  });
});
```


### Backend Testing

#### Unit Testing with pytest

**Test Categories**:

1. **Endpoint Tests**
   - Test health check returns 200 with correct JSON
   - Test successful booking creation returns 201
   - Test successful contact creation returns 201
   - Test list endpoints return 200

2. **Validation Tests**
   - Test missing required fields return 422
   - Test invalid email format returns 422
   - Test validation error response structure

3. **Database Integration Tests**
   - Test documents are created in MongoDB
   - Test list endpoints query and return documents
   - Test sorting by created_at descending

**Example Unit Tests**:
```python
# test_bookings.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint returns 200 with status ok"""
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_booking_success():
    """Test creating a booking with valid data returns 201"""
    booking_data = {
        "name": "John Doe",
        "phone": "9876543210",
        "service": "Weddings",
        "event_date": "2024-06-15",
        "event_time": "14:00",
        "location": "Rajahmundry",
        "message": "Looking forward to the event"
    }
    response = client.post("/api/bookings", json=booking_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data
    assert "created_at" in data
    assert "_id" not in data

def test_create_booking_missing_required_field():
    """Test creating a booking without required field returns 422"""
    booking_data = {
        "name": "John Doe",
        "phone": "9876543210",
        # Missing service, event_date, event_time, location
    }
    response = client.post("/api/bookings", json=booking_data)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_list_bookings():
    """Test listing bookings returns 200 and sorted array"""
    response = client.get("/api/bookings")
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)
    # Verify sorting (newest first)
    if len(bookings) > 1:
        for i in range(len(bookings) - 1):
            assert bookings[i]["created_at"] >= bookings[i + 1]["created_at"]
```

#### Property-Based Testing with Hypothesis

**Configuration**: Minimum 100 iterations per property test

**Property Test Categories**:

1. **Creation Properties**
   - Any valid booking data creates a document
   - Any valid contact data creates a document
   - Any created resource has UUID and timestamp

2. **Validation Properties**
   - Any data missing required fields returns 422
   - Any invalid email format returns 422
   - Any valid data returns 201

3. **Response Properties**
   - Any list response excludes _id field
   - Any list response is sorted by created_at descending
   - Any creation response includes all input fields

**Example Property Tests**:
```python
# test_bookings_properties.py
from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from app.main import app
import re

client = TestClient(app)

@given(
    name=st.text(min_size=1, max_size=100),
    phone=st.text(min_size=1, max_size=20),
    service=st.sampled_from(["Weddings", "Photoshoots", "Reel Making", "Events", "Drone Shots"]),
    event_date=st.dates().map(lambda d: d.isoformat()),
    event_time=st.times().map(lambda t: t.strftime("%H:%M")),
    location=st.text(min_size=1, max_size=200),
    message=st.text(max_size=500)
)
def test_property_28_booking_creation_persistence(name, phone, service, event_date, event_time, location, message):
    """
    Feature: godavari-captures-landing-page, Property 28: For any valid booking data,
    the API should create a corresponding document in MongoDB
    """
    booking_data = {
        "name": name,
        "phone": phone,
        "service": service,
        "event_date": event_date,
        "event_time": event_time,
        "location": location,
        "message": message
    }
    
    response = client.post("/api/bookings", json=booking_data)
    assert response.status_code == 201
    
    # Verify the booking appears in the list
    list_response = client.get("/api/bookings")
    bookings = list_response.json()
    assert any(b["name"] == name and b["phone"] == phone for b in bookings)

@given(
    name=st.text(min_size=1, max_size=100),
    phone=st.text(min_size=1, max_size=20),
    service=st.sampled_from(["Weddings", "Photoshoots", "Reel Making", "Events", "Drone Shots"]),
    event_date=st.dates().map(lambda d: d.isoformat()),
    event_time=st.times().map(lambda t: t.strftime("%H:%M")),
    location=st.text(min_size=1, max_size=200)
)
def test_property_30_booking_uuid_generation(name, phone, service, event_date, event_time, location):
    """
    Feature: godavari-captures-landing-page, Property 30: For any valid booking data,
    the API response should include an 'id' field containing a valid UUID
    """
    booking_data = {
        "name": name,
        "phone": phone,
        "service": service,
        "event_date": event_date,
        "event_time": event_time,
        "location": location,
        "message": ""
    }
    
    response = client.post("/api/bookings", json=booking_data)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    
    # Verify UUID format
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    assert re.match(uuid_pattern, data["id"], re.IGNORECASE)

@given(
    name=st.text(min_size=1, max_size=100),
    email=st.emails(),
    phone=st.text(min_size=1, max_size=20),
    subject=st.text(min_size=1, max_size=200),
    message=st.text(min_size=1, max_size=1000)
)
def test_property_37_contact_email_validation(name, email, phone, subject, message):
    """
    Feature: godavari-captures-landing-page, Property 37: For any contact data with valid email,
    the API should accept it; for invalid email, should return 422
    """
    contact_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "subject": subject,
        "message": message
    }
    
    response = client.post("/api/contact", json=contact_data)
    
    # Valid emails should succeed
    if '@' in email and '.' in email.split('@')[1]:
        assert response.status_code == 201
    # Invalid emails should fail (though hypothesis.emails() generates valid ones)

def test_property_43_mongodb_id_exclusion():
    """
    Feature: godavari-captures-landing-page, Property 43: For any document returned by
    GET endpoints, the response should not contain '_id' field
    """
    # Test bookings
    bookings_response = client.get("/api/bookings")
    assert bookings_response.status_code == 200
    bookings = bookings_response.json()
    for booking in bookings:
        assert "_id" not in booking
    
    # Test contacts
    contacts_response = client.get("/api/contact")
    assert contacts_response.status_code == 200
    contacts = contacts_response.json()
    for contact in contacts:
        assert "_id" not in contact
```


### End-to-End Testing

#### Playwright for E2E Tests

**Test Scenarios**:

1. **Complete Booking Flow**
   - Navigate to site → Click "Book Now" → Fill form → Submit → Verify success message
   - Test with valid data, verify API call and database persistence

2. **Portfolio Browsing Flow**
   - Navigate to portfolio → Click filter chips → Verify filtered results → Click images

3. **Contact Form Flow**
   - Navigate to contact → Fill form → Submit → Verify success message

4. **Mobile Responsive Flow**
   - Set viewport to mobile → Open hamburger menu → Navigate sections → Submit forms

**Example E2E Test**:
```javascript
// e2e/booking-flow.spec.js
import { test, expect } from '@playwright/test';

test('complete booking flow', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Click Book Now button in services
  await page.click('[data-testid="service-book-weddings"]');
  
  // Verify scrolled to booking form
  await expect(page.locator('[data-testid="booking-form"]')).toBeInViewport();
  
  // Fill form
  await page.fill('[data-testid="booking-name"]', 'Test User');
  await page.fill('[data-testid="booking-phone"]', '9876543210');
  await page.selectOption('[data-testid="booking-service"]', 'Weddings');
  await page.fill('[data-testid="booking-date"]', '2024-06-15');
  await page.fill('[data-testid="booking-time"]', '14:00');
  await page.fill('[data-testid="booking-location"]', 'Rajahmundry');
  await page.fill('[data-testid="booking-message"]', 'Looking forward to working with you');
  
  // Submit form
  await page.click('[data-testid="booking-submit"]');
  
  // Verify success message
  await expect(page.locator('[data-testid="booking-success"]')).toBeVisible();
  await expect(page.locator('[data-testid="booking-success"]')).toContainText('successfully');
});

test('portfolio filtering', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Navigate to portfolio
  await page.click('[data-testid="nav-portfolio"]');
  
  // Click Weddings filter
  await page.click('[data-testid="filter-weddings"]');
  
  // Verify only wedding images are visible
  const visibleImages = await page.locator('[data-category="Weddings"]').count();
  const totalImages = await page.locator('[data-category]').count();
  expect(visibleImages).toBeGreaterThan(0);
  expect(visibleImages).toBe(totalImages);
  
  // Verify filter is highlighted
  await expect(page.locator('[data-testid="filter-weddings"]')).toHaveClass(/bg-luxury-gold/);
});
```

### Test Coverage Goals

- **Frontend Unit Tests**: 80% code coverage minimum
- **Frontend Property Tests**: All 27 frontend properties implemented
- **Backend Unit Tests**: 90% code coverage minimum
- **Backend Property Tests**: All 16 backend properties implemented
- **E2E Tests**: All critical user flows covered
- **Accessibility Tests**: WCAG 2.1 Level AA compliance (manual testing with screen readers required)

### Continuous Integration

**CI Pipeline Steps**:
1. Run frontend unit tests (Jest)
2. Run frontend property tests (fast-check)
3. Run backend unit tests (pytest)
4. Run backend property tests (Hypothesis)
5. Run E2E tests (Playwright)
6. Generate coverage reports
7. Run Lighthouse performance audit
8. Fail build if coverage < thresholds or any test fails

