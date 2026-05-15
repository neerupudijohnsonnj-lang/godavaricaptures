/**
 * API client for Godavari Captures backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Create a new booking
 * @param {Object} bookingData - Booking form data
 * @returns {Promise<Object>} Created booking response
 */
export async function createBooking(bookingData) {
  const response = await fetch(`${API_BASE_URL}/api/bookings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookingData)
  })
  
  if (!response.ok) {
    throw new Error(`Booking creation failed: ${response.statusText}`)
  }
  
  return response.json()
}

/**
 * Get all bookings
 * @returns {Promise<Array>} List of bookings
 */
export async function getBookings() {
  const response = await fetch(`${API_BASE_URL}/api/bookings`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch bookings: ${response.statusText}`)
  }
  
  return response.json()
}

/**
 * Create a new contact message
 * @param {Object} contactData - Contact form data
 * @returns {Promise<Object>} Created contact response
 */
export async function createContact(contactData) {
  const response = await fetch(`${API_BASE_URL}/api/contact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contactData)
  })
  
  if (!response.ok) {
    throw new Error(`Contact creation failed: ${response.statusText}`)
  }
  
  return response.json()
}

/**
 * Get all contact messages
 * @returns {Promise<Array>} List of contact messages
 */
export async function getContacts() {
  const response = await fetch(`${API_BASE_URL}/api/contact`)
  
  if (!response.ok) {
    throw new Error(`Failed to fetch contacts: ${response.statusText}`)
  }
  
  return response.json()
}
