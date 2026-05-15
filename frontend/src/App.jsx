import { useState } from 'react'
import { BRAND, NAV_LINKS, SERVICES, STATS, PORTFOLIO } from './constants'

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [showreelOpen, setShowreelOpen] = useState(false)
  const [portfolioFilter, setPortfolioFilter] = useState('all')
  const [bookingForm, setBookingForm] = useState({
    name: '', phone: '', service: 'Weddings', event_date: '', location: '', message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Filter portfolio images
  const filteredPortfolio = portfolioFilter === 'all' 
    ? PORTFOLIO 
    : PORTFOLIO.filter(item => item.category === portfolioFilter)

  const handleBookingSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // Check if backend is configured
    const API_URL = import.meta.env.VITE_API_URL
    
    if (!API_URL) {
      alert('📧 Thank you for your interest!\n\nPlease contact us directly:\n\n📞 Phone: +91 7780494179\n✉️ Email: neerupudijohnsonnj@gmail.com\n\nWe will get back to you shortly!')
      setIsSubmitting(false)
      setBookingForm({ name: '', phone: '', service: 'Weddings', event_date: '', location: '', message: '' })
      return
    }
    
    try {
      const response = await fetch(`${API_URL}/api/bookings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...bookingForm, event_time: ''})
      })
      if (response.ok) {
        alert('Booking submitted successfully! You will receive a confirmation email shortly.')
        setBookingForm({ name: '', phone: '', service: 'Weddings', event_date: '', location: '', message: '' })
      } else {
        const errorData = await response.json()
        alert(`Error: ${errorData.detail || 'Failed to submit booking'}`)
      }
    } catch (error) {
      alert('📧 Unable to connect to booking system.\n\nPlease contact us directly:\n\n📞 Phone: +91 7780494179\n✉️ Email: neerupudijohnsonnj@gmail.com')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="bg-luxury-black text-white font-body">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-luxury-black/90 backdrop-blur-sm z-50 border-b border-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <a href="#home" className="font-display text-2xl text-luxury-gold">
              {BRAND.name}
            </a>
            <div className="hidden md:flex space-x-8">
              {NAV_LINKS.map(link => (
                <a key={link.href} href={link.href} className="hover:text-luxury-gold transition-colors">
                  {link.label}
                </a>
              ))}
            </div>
            <a href="#booking" className="btn-gold hidden md:block">Book Instantly</a>
            <button className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
        
        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden fixed inset-0 top-16 bg-luxury-black/95 backdrop-blur-md z-40">
            <div className="flex flex-col items-center justify-start pt-12 px-6 space-y-6">
              {NAV_LINKS.map(link => (
                <a 
                  key={link.href} 
                  href={link.href} 
                  className="text-xl w-full text-center py-3 hover:text-luxury-gold transition-colors border-b border-gray-800"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.label}
                </a>
              ))}
              <a 
                href="#booking" 
                className="btn-gold w-full text-center mt-4" 
                onClick={() => setMobileMenuOpen(false)}
              >
                Book Instantly
              </a>
            </div>
          </div>
        )}
      </nav>

      {/* Hero */}
      <section id="home" className="min-h-screen flex items-center justify-center pt-16 px-4 relative overflow-hidden">
        {/* Godavari Bridge Sunset Background - High Quality */}
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: 'url(/images/hero-godavari.jpg)',
            backgroundPosition: 'center center',
            backgroundSize: 'cover',
            backgroundRepeat: 'no-repeat',
            imageRendering: '-webkit-optimize-contrast',
            WebkitBackfaceVisibility: 'hidden',
            backfaceVisibility: 'hidden',
            transform: 'translateZ(0)',
            willChange: 'transform'
          }}
        ></div>
        
        {/* Dark overlay for text readability - Lighter to show image better */}
        <div className="absolute inset-0 bg-gradient-to-b from-luxury-black/50 via-luxury-black/60 to-luxury-black z-0"></div>
        
        <div className="text-center max-w-4xl relative z-10">
          <h1 className="font-display text-5xl md:text-7xl mb-6 text-luxury-gold">
            Capturing Moments. Creating Stories.
          </h1>
          <p className="text-2xl md:text-3xl mb-8">{BRAND.tagline}</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <a href="#booking" className="btn-gold">Book Instantly</a>
            <a href="#portfolio" className="btn-outline">View Portfolio</a>
          </div>
          <div className="flex justify-center mb-12">
            <button 
              onClick={() => setShowreelOpen(true)}
              className="flex items-center gap-3 text-luxury-gold hover:text-luxury-gold-hover transition-all group"
            >
              <div className="w-12 h-12 rounded-full border-2 border-luxury-gold flex items-center justify-center group-hover:bg-luxury-gold/10 transition-all">
                <svg className="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z" />
                </svg>
              </div>
              <span className="font-semibold">Watch Showreel</span>
            </button>
          </div>
          <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            {STATS.map((stat, i) => (
              <div key={i} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-luxury-gold">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Showreel Modal */}
      {showreelOpen && (
        <div 
          className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4"
          onClick={() => setShowreelOpen(false)}
        >
          <div className="relative w-full max-w-4xl aspect-video" onClick={(e) => e.stopPropagation()}>
            <button 
              onClick={() => setShowreelOpen(false)}
              className="absolute -top-12 right-0 text-white hover:text-luxury-gold text-2xl"
            >
              ✕
            </button>
            <iframe
              className="w-full h-full"
              src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
              title="Godavari Captures Showreel"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        </div>
      )}

      {/* Services */}
      <section id="services" className="py-20 px-4 bg-luxury-alt">
        <div className="max-w-7xl mx-auto">
          <h2 className="font-display text-4xl md:text-5xl text-center mb-4 text-luxury-gold">What We Do</h2>
          <p className="text-center text-gray-400 mb-12">Crafted services</p>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {SERVICES.map((service, i) => (
              <div key={i} className="bg-luxury-card p-6 border border-gray-900 hover:border-luxury-gold transition-all">
                <h3 className="font-display text-xl mb-2">{service.title}</h3>
                <p className="text-gray-400 text-sm mb-4">{service.description}</p>
                <a href="#booking" className="text-luxury-gold hover:text-luxury-gold-hover text-sm">Book Now →</a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div 
              className="h-96 bg-cover bg-center relative overflow-hidden"
              style={{
                backgroundImage: 'url(https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=800&q=80)'
              }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-luxury-gold/10 to-transparent"></div>
            </div>
            <div>
              <h2 className="font-display text-4xl mb-4 text-luxury-gold">Frames as heirlooms</h2>
              <p className="text-gray-300 mb-6">
                Godavari Captures is a boutique photography & cinematic reel-making house, born on the banks of the Godavari. 
                We treat every wedding, brand and family like our only project — pairing documentary instincts with editorial taste.
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-luxury-card p-4 border border-gray-900">
                  <div className="text-luxury-gold font-semibold">Cinematic</div>
                  <div className="text-sm text-gray-400">Visual language</div>
                </div>
                <div className="bg-luxury-card p-4 border border-gray-900">
                  <div className="text-luxury-gold font-semibold">Editorial</div>
                  <div className="text-sm text-gray-400">Direction & edit</div>
                </div>
                <div className="bg-luxury-card p-4 border border-gray-900">
                  <div className="text-luxury-gold font-semibold">Drone-Ready</div>
                  <div className="text-sm text-gray-400">Aerial coverage</div>
                </div>
                <div className="bg-luxury-card p-4 border border-gray-900">
                  <div className="text-luxury-gold font-semibold">48h Reels</div>
                  <div className="text-sm text-gray-400">Fast turnaround</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Portfolio */}
      <section id="portfolio" className="py-20 px-4 bg-luxury-alt">
        <div className="max-w-7xl mx-auto">
          <h2 className="font-display text-4xl md:text-5xl text-center mb-4 text-luxury-gold">Selected Work</h2>
          <p className="text-center text-gray-400 mb-8">The portfolio</p>
          
          {/* Filter Chips */}
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {['all', 'weddings', 'photoshoots', 'events', 'drone'].map(filter => (
              <button
                key={filter}
                onClick={() => setPortfolioFilter(filter)}
                className={`px-6 py-2 border transition-all ${
                  portfolioFilter === filter 
                    ? 'border-luxury-gold text-luxury-gold' 
                    : 'border-gray-800 text-gray-400 hover:border-luxury-gold hover:text-luxury-gold'
                }`}
              >
                {filter.charAt(0).toUpperCase() + filter.slice(1)}
              </button>
            ))}
          </div>

          {/* Portfolio Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {filteredPortfolio.map((item, i) => (
              <div key={i} className="relative group overflow-hidden aspect-square bg-luxury-card border border-gray-900">
                {/* Background image with fallback */}
                <div 
                  className="absolute inset-0 bg-cover bg-center"
                  style={{
                    backgroundImage: `url(${item.src}), linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(10, 10, 10, 1) 100%)`
                  }}
                >
                  {/* Fallback icon when image is not loaded */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <svg className="w-16 h-16 text-luxury-gold/30" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                    </svg>
                  </div>
                </div>
                
                {/* Hover overlay with title */}
                <div className="absolute inset-0 bg-luxury-black/80 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="text-center px-4">
                    <div className="text-white font-display text-lg mb-1">{item.alt}</div>
                    <div className="text-luxury-gold text-sm capitalize">{item.category}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Booking */}
      <section id="booking" className="py-20 px-4 bg-luxury-black">
        <div className="max-w-7xl mx-auto">
          <h2 className="font-display text-4xl md:text-5xl text-center mb-4 text-luxury-gold">Instant Booking</h2>
          <p className="text-center text-gray-400 mb-12">Reserve your date</p>
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="font-display text-2xl mb-6 text-luxury-gold">By The Numbers</h3>
              <p className="text-gray-400 mb-6">A studio built on trust</p>
              <div className="space-y-4">
                <div className="bg-luxury-card p-6 border border-gray-900">
                  <div className="text-3xl font-bold text-luxury-gold">500+</div>
                  <div className="text-gray-400">Projects Completed</div>
                </div>
                <div className="bg-luxury-card p-6 border border-gray-900">
                  <div className="text-3xl font-bold text-luxury-gold">300+</div>
                  <div className="text-gray-400">Happy Clients</div>
                </div>
                <div className="bg-luxury-card p-6 border border-gray-900">
                  <div className="text-3xl font-bold text-luxury-gold">3+</div>
                  <div className="text-gray-400">Years of Experience</div>
                </div>
              </div>
            </div>
            <form onSubmit={handleBookingSubmit} className="space-y-4">
              <input
                type="text"
                placeholder="Name"
                value={bookingForm.name}
                onChange={(e) => setBookingForm({...bookingForm, name: e.target.value})}
                className="w-full bg-luxury-card border border-gray-800 px-4 py-3 text-white focus:border-luxury-gold focus:outline-none"
                required
              />
              <input
                type="tel"
                placeholder="Phone (10 digits)"
                value={bookingForm.phone}
                onChange={(e) => {
                  const value = e.target.value.replace(/\D/g, '').slice(0, 10);
                  setBookingForm({...bookingForm, phone: value});
                }}
                className="w-full bg-luxury-card border border-gray-800 px-4 py-3 text-white focus:border-luxury-gold focus:outline-none"
                pattern="[0-9]{10}"
                maxLength="10"
                title="Please enter exactly 10 digits"
                required
              />
              <select
                value={bookingForm.service}
                onChange={(e) => setBookingForm({...bookingForm, service: e.target.value})}
                className="w-full bg-luxury-card border border-gray-800 px-4 py-3 text-white focus:border-luxury-gold focus:outline-none"
              >
                {SERVICES.map(s => <option key={s.title} value={s.title}>{s.title}</option>)}
              </select>
              <input
                type="date"
                value={bookingForm.event_date}
                onChange={(e) => setBookingForm({...bookingForm, event_date: e.target.value})}
                className="w-full bg-luxury-card border border-gray-800 px-4 py-3 text-white focus:border-luxury-gold focus:outline-none"
                required
              />
              <input
                type="text"
                placeholder="Location"
                value={bookingForm.location}
                onChange={(e) => setBookingForm({...bookingForm, location: e.target.value})}
                className="w-full bg-luxury-card border border-gray-800 px-4 py-3 text-white focus:border-luxury-gold focus:outline-none"
                required
              />
              <textarea
                placeholder="Message (optional)"
                value={bookingForm.message}
                onChange={(e) => setBookingForm({...bookingForm, message: e.target.value})}
                className="w-full bg-luxury-card border border-gray-800 px-4 py-3 text-white focus:border-luxury-gold focus:outline-none h-24"
              />
              <button 
                type="submit" 
                className="btn-gold w-full"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Submitting...' : 'Book Now'}
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-luxury-alt py-12 px-4 border-t border-gray-900">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="font-display text-2xl text-luxury-gold mb-2">{BRAND.name}</div>
              <p className="text-gray-400 text-sm">{BRAND.tagline}</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Navigate</h4>
              <div className="space-y-2">
                {NAV_LINKS.map(link => (
                  <a key={link.href} href={link.href} className="block text-gray-400 hover:text-luxury-gold text-sm">
                    {link.label}
                  </a>
                ))}
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Studio</h4>
              <div className="space-y-2 text-sm text-gray-400">
                <p>{BRAND.phone}</p>
                <p>{BRAND.email}</p>
                <p>{BRAND.instagram}</p>
                <p>{BRAND.address}</p>
              </div>
            </div>
            <div>
              <p className="text-gray-400 text-sm">
                © 2026 Godavari Captures. All rights reserved.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
