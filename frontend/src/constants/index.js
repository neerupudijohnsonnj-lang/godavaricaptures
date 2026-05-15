/**
 * Brand and content constants for Godavari Captures landing page
 */

export const BRAND = {
  name: "Godavari Captures",
  tagline: "We turn moments into reels",
  phone: "+91 7780494179",
  email: "neerupudijohnsonnj@gmail.com",
  address: "Rajahmundry, Andhra Pradesh, India",
  instagram: "@godavari.captures"
};

export const NAV_LINKS = [
  { label: "HOME", href: "#home", testId: "nav-home" },
  { label: "ABOUT", href: "#about", testId: "nav-about" },
  { label: "SERVICES", href: "#services", testId: "nav-services" },
  { label: "PORTFOLIO", href: "#portfolio", testId: "nav-portfolio" }
];

export const SERVICES = [
  {
    title: "Weddings",
    description: "Capture your special day beautifully"
  },
  {
    title: "Photoshoots",
    description: "Portraits, fashion & creative shoots"
  },
  {
    title: "Reel Making",
    description: "Trending reels for social media"
  },
  {
    title: "Events",
    description: "Corporate, parties & special events"
  },
  {
    title: "Drone Shots",
    description: "Aerial photography & videography"
  }
];

export const STATS = [
  { value: "500+", label: "Projects" },
  { value: "300+", label: "Happy Clients" },
  { value: "3+", label: "Years" }
];

export const PACKAGES = [
  {
    name: "Essential",
    price: "₹24,999",
    description: "Half-day coverage",
    features: [
      "4 hours of coverage",
      "1 lead photographer",
      "200+ edited photos",
      "1 cinematic reel (30s)",
      "Online private gallery"
    ],
    isRecommended: false
  },
  {
    name: "Signature",
    price: "₹59,999",
    description: "Full-day coverage",
    features: [
      "10 hours of coverage",
      "2 photographers + cinematographer",
      "500+ edited photos",
      "3 cinematic reels + 5min film",
      "Drone aerial coverage",
      "Premium photo album"
    ],
    isRecommended: true
  },
  {
    name: "Heritage",
    price: "₹1,29,999",
    description: "Multi-day coverage",
    features: [
      "3-day full coverage",
      "Full crew + drone team",
      "1000+ edited photos",
      "Trailer + full film + reels",
      "Luxury hardcover album",
      "Same-day teaser"
    ],
    isRecommended: false
  }
];

export const TESTIMONIALS = [
  {
    name: "Neha Reddy",
    role: "Founder, Velvet Studio",
    review: "The reels they made went viral on Instagram. Best decision for our brand launch."
  },
  {
    name: "Arjun & Priya",
    role: "Wedding Couple",
    review: "They captured our wedding day perfectly. Every moment, every emotion - it's all there in the most beautiful way."
  },
  {
    name: "Vikram Malhotra",
    role: "CEO, TechVision",
    review: "Professional, creative, and delivered ahead of schedule. The corporate event coverage exceeded our expectations."
  }
];

export const PORTFOLIO = [
  { src: "https://images.unsplash.com/photo-1519741497674-611481863552?w=800&q=80", alt: "Royal Vows", category: "weddings" },
  { src: "https://images.unsplash.com/photo-1606800052052-a08af7148866?w=800&q=80", alt: "Sindoor Mornings", category: "weddings" },
  { src: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=800&q=80", alt: "Golden Hour", category: "photoshoots" },
  { src: "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=80", alt: "Above The River", category: "drone" },
  { src: "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&q=80", alt: "Candlelit Soirée", category: "events" },
  { src: "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80", alt: "Editorial", category: "photoshoots" },
  { src: "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800&q=80", alt: "Mehndi Hues", category: "weddings" },
  { src: "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80", alt: "Bridge of Light", category: "drone" }
];
