# Requirements Document

## Introduction

Godavari Captures is a luxury photography and cinematic reel-making studio based in Rajahmundry, Andhra Pradesh, India. This document specifies requirements for a premium single-page full-stack landing website that showcases the studio's work, enables instant bookings, and captures contact inquiries. The system uses React 19 with Tailwind CSS for the frontend, FastAPI with MongoDB for the backend, and implements a pure black luxury aesthetic with gold accents.

## Glossary

- **Landing_Page**: The single-page React application serving as the studio's web presence
- **Booking_System**: The backend API and frontend form handling instant booking requests
- **Contact_System**: The backend API and frontend form handling general inquiries
- **Portfolio_Gallery**: The filterable image grid displaying studio work across categories
- **Navigation_Bar**: The sticky header with smooth-scroll navigation links
- **Showreel_Modal**: The fullscreen video player for the studio's demo reel
- **Testimonial_Carousel**: The auto-rotating client review component
- **Backend_API**: The FastAPI server handling data persistence and retrieval
- **MongoDB_Database**: The document database storing bookings and contact messages
- **Design_System**: The visual language using black (#000000, #0A0A0A, #050505), gold (#D4AF37), Playfair Display, and Manrope fonts

## Requirements

### Requirement 1: Navigation System

**User Story:** As a visitor, I want to navigate between sections smoothly, so that I can explore the studio's offerings without page reloads.

#### Acceptance Criteria

1. THE Navigation_Bar SHALL display seven navigation links: HOME, ABOUT, SERVICES, PORTFOLIO, PACKAGES, YOUR REELS, and CONTACT
2. WHEN a navigation link is clicked, THE Landing_Page SHALL smooth-scroll to the corresponding section
3. WHEN the page is scrolled beyond 50 pixels, THE Navigation_Bar SHALL apply a backdrop blur effect
4. THE Navigation_Bar SHALL remain fixed at the top of the viewport during scrolling
5. THE Navigation_Bar SHALL display the studio logo on the left and a "BOOK INSTANTLY" CTA button on the right
6. WHERE the viewport width is below 768 pixels, THE Navigation_Bar SHALL display a hamburger menu icon
7. WHEN the hamburger menu icon is clicked, THE Landing_Page SHALL display a full-screen mobile navigation overlay
8. THE Navigation_Bar SHALL include data-testid attributes for all interactive elements

### Requirement 2: Hero Section

**User Story:** As a visitor, I want to see compelling visuals and key information immediately, so that I understand the studio's value proposition.

#### Acceptance Criteria

1. THE Landing_Page SHALL display a full-bleed background image of the Godavari Rail Bridge at sunset in the hero section
2. THE Landing_Page SHALL display the headline "We turn moments into reels" in Playfair Display font
3. THE Landing_Page SHALL display three statistics: "500+ Projects", "300+ Clients", and "3+ Years"
4. THE Landing_Page SHALL display two CTA buttons: "Book Your Session" and "View Portfolio"
5. WHEN the "Book Your Session" button is clicked, THE Landing_Page SHALL smooth-scroll to the booking form section
6. WHEN the "View Portfolio" button is clicked, THE Landing_Page SHALL smooth-scroll to the portfolio section
7. THE Landing_Page SHALL display a "Watch Showreel" button with a play icon
8. WHEN the "Watch Showreel" button is clicked, THE Showreel_Modal SHALL open and display a YouTube video player
9. WHEN the Showreel_Modal close button or overlay is clicked, THE Showreel_Modal SHALL close

### Requirement 3: Services Display

**User Story:** As a visitor, I want to see all available services, so that I can identify which service meets my needs.

#### Acceptance Criteria

1. THE Landing_Page SHALL display five service cards in a grid layout: Weddings, Photoshoots, Reel Making, Events, and Drone Shots
2. THE Landing_Page SHALL display an icon, title, and description for each service card
3. THE Landing_Page SHALL display a "Book Now" button on each service card
4. WHEN a "Book Now" button is clicked, THE Landing_Page SHALL smooth-scroll to the booking form section
5. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL display service cards in a single column layout

### Requirement 4: About Section

**User Story:** As a visitor, I want to learn about the studio's philosophy and approach, so that I can assess their fit for my needs.

#### Acceptance Criteria

1. THE Landing_Page SHALL display a two-column layout with a studio image on the left and content on the right
2. THE Landing_Page SHALL display the heading "Frames as heirlooms" in the about section
3. THE Landing_Page SHALL display descriptive text about the studio's approach
4. THE Landing_Page SHALL display four feature cells highlighting studio capabilities
5. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL stack the about section columns vertically

### Requirement 5: Instant Booking System

**User Story:** As a potential client, I want to submit a booking request instantly, so that I can secure the studio's services for my event.

#### Acceptance Criteria

1. THE Landing_Page SHALL display a booking form with fields for Name, Phone, Service, Event Date, Event Time, Location, and Message
2. WHEN the booking form is submitted with valid data, THE Booking_System SHALL send a POST request to /api/bookings
3. WHEN the booking submission succeeds, THE Landing_Page SHALL display a success message
4. WHEN the booking submission fails, THE Landing_Page SHALL display an error message
5. THE Landing_Page SHALL validate that Name contains at least 2 characters before submission
6. THE Landing_Page SHALL validate that Phone contains at least 10 digits before submission
7. THE Landing_Page SHALL validate that a Service option is selected before submission
8. THE Landing_Page SHALL validate that Event Date is provided before submission
9. THE Landing_Page SHALL display three statistics cards adjacent to the booking form: projects completed, client satisfaction rate, and years of experience
10. THE Landing_Page SHALL include data-testid attributes for all form fields and buttons

### Requirement 6: Portfolio Gallery

**User Story:** As a visitor, I want to browse the studio's work by category, so that I can evaluate their expertise in my area of interest.

#### Acceptance Criteria

1. THE Portfolio_Gallery SHALL display eight luxury photography samples in a masonry grid layout
2. THE Portfolio_Gallery SHALL display five filter chips: All, Weddings, Photoshoots, Events, and Drone
3. WHEN a filter chip is clicked, THE Portfolio_Gallery SHALL display only images matching the selected category
4. WHEN the "All" filter chip is clicked, THE Portfolio_Gallery SHALL display all images
5. THE Portfolio_Gallery SHALL highlight the active filter chip with gold accent color
6. THE Portfolio_Gallery SHALL display images with hover effects
7. WHERE the viewport width is below 768 pixels, THE Portfolio_Gallery SHALL display images in a single column layout

### Requirement 7: Pricing Packages

**User Story:** As a potential client, I want to see transparent pricing options, so that I can choose a package that fits my budget.

#### Acceptance Criteria

1. THE Landing_Page SHALL display three pricing tiers: Essential (₹24,999), Signature (₹59,999), and Heritage (₹1,29,999)
2. THE Landing_Page SHALL display package name, price, description, and feature list for each tier
3. THE Landing_Page SHALL visually highlight the Signature package as the recommended option
4. THE Landing_Page SHALL display a "Book This Package" button on each pricing card
5. WHEN a "Book This Package" button is clicked, THE Landing_Page SHALL smooth-scroll to the booking form section
6. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL stack pricing cards vertically

### Requirement 8: Testimonial Carousel

**User Story:** As a visitor, I want to read client testimonials, so that I can assess the studio's reputation and service quality.

#### Acceptance Criteria

1. THE Testimonial_Carousel SHALL display three client testimonials with name, role, and review text
2. THE Testimonial_Carousel SHALL automatically advance to the next testimonial every 6 seconds
3. WHEN the previous button is clicked, THE Testimonial_Carousel SHALL display the previous testimonial
4. WHEN the next button is clicked, THE Testimonial_Carousel SHALL display the next testimonial
5. WHEN a dot indicator is clicked, THE Testimonial_Carousel SHALL display the corresponding testimonial
6. THE Testimonial_Carousel SHALL highlight the active dot indicator with gold accent color
7. THE Testimonial_Carousel SHALL pause autoplay when the user interacts with navigation controls

### Requirement 9: Contact System

**User Story:** As a visitor, I want to send a general inquiry, so that I can ask questions or request information.

#### Acceptance Criteria

1. THE Landing_Page SHALL display a contact form with fields for Name, Email, Phone, Subject, and Message
2. WHEN the contact form is submitted with valid data, THE Contact_System SHALL send a POST request to /api/contact
3. WHEN the contact submission succeeds, THE Landing_Page SHALL display a success message
4. WHEN the contact submission fails, THE Landing_Page SHALL display an error message
5. THE Landing_Page SHALL validate that Name contains at least 2 characters before submission
6. THE Landing_Page SHALL validate that Email is in valid email format before submission
7. THE Landing_Page SHALL validate that Phone contains at least 10 digits before submission
8. THE Landing_Page SHALL validate that Subject contains at least 3 characters before submission
9. THE Landing_Page SHALL validate that Message contains at least 10 characters before submission
10. THE Landing_Page SHALL display studio contact information adjacent to the contact form: phone, email, address, and Instagram handle
11. THE Landing_Page SHALL include data-testid attributes for all form fields and buttons

### Requirement 10: Footer

**User Story:** As a visitor, I want to access key information and navigation from the footer, so that I can find what I need regardless of scroll position.

#### Acceptance Criteria

1. THE Landing_Page SHALL display a four-column footer grid with Brand, Navigation, Studio Info, and Copyright sections
2. THE Landing_Page SHALL display the studio logo, tagline, and social media link in the Brand column
3. THE Landing_Page SHALL display navigation links to all major sections in the Navigation column
4. THE Landing_Page SHALL display contact information in the Studio Info column
5. THE Landing_Page SHALL display copyright text with the current year
6. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL stack footer columns vertically

### Requirement 11: Backend API Health Check

**User Story:** As a system administrator, I want to verify the API is operational, so that I can monitor service availability.

#### Acceptance Criteria

1. WHEN a GET request is sent to /api/, THE Backend_API SHALL return a 200 status code
2. WHEN a GET request is sent to /api/, THE Backend_API SHALL return a JSON response with a status field

### Requirement 12: Backend Booking Management

**User Story:** As a system administrator, I want to store and retrieve booking requests, so that the studio can process client inquiries.

#### Acceptance Criteria

1. WHEN a POST request is sent to /api/bookings with valid data, THE Backend_API SHALL create a booking document in the MongoDB_Database
2. WHEN a POST request is sent to /api/bookings, THE Backend_API SHALL validate that name, phone, service, event_date, event_time, and location fields are provided
3. WHEN a POST request is sent to /api/bookings with valid data, THE Backend_API SHALL generate a UUID for the booking id
4. WHEN a POST request is sent to /api/bookings with valid data, THE Backend_API SHALL generate an ISO 8601 timestamp for created_at
5. WHEN a POST request is sent to /api/bookings with valid data, THE Backend_API SHALL return a 201 status code
6. WHEN a POST request is sent to /api/bookings with invalid data, THE Backend_API SHALL return a 422 status code with validation errors
7. WHEN a GET request is sent to /api/bookings, THE Backend_API SHALL return all bookings sorted by created_at in descending order
8. WHEN a GET request is sent to /api/bookings, THE Backend_API SHALL exclude the MongoDB _id field from all booking documents
9. WHEN a GET request is sent to /api/bookings, THE Backend_API SHALL return a 200 status code

### Requirement 13: Backend Contact Management

**User Story:** As a system administrator, I want to store and retrieve contact messages, so that the studio can respond to inquiries.

#### Acceptance Criteria

1. WHEN a POST request is sent to /api/contact with valid data, THE Backend_API SHALL create a contact message document in the MongoDB_Database
2. WHEN a POST request is sent to /api/contact, THE Backend_API SHALL validate that name, email, phone, subject, and message fields are provided
3. WHEN a POST request is sent to /api/contact, THE Backend_API SHALL validate that email is in valid email format using Pydantic EmailStr
4. WHEN a POST request is sent to /api/contact with valid data, THE Backend_API SHALL generate a UUID for the message id
5. WHEN a POST request is sent to /api/contact with valid data, THE Backend_API SHALL generate an ISO 8601 timestamp for created_at
6. WHEN a POST request is sent to /api/contact with valid data, THE Backend_API SHALL return a 201 status code
7. WHEN a POST request is sent to /api/contact with invalid data, THE Backend_API SHALL return a 422 status code with validation errors
8. WHEN a GET request is sent to /api/contact, THE Backend_API SHALL return all contact messages sorted by created_at in descending order
9. WHEN a GET request is sent to /api/contact, THE Backend_API SHALL exclude the MongoDB _id field from all contact message documents
10. WHEN a GET request is sent to /api/contact, THE Backend_API SHALL return a 200 status code

### Requirement 14: Design System Implementation

**User Story:** As a visitor, I want to experience a cohesive luxury aesthetic, so that the website reflects the studio's premium positioning.

#### Acceptance Criteria

1. THE Landing_Page SHALL use #000000 as the primary background color
2. THE Landing_Page SHALL use #0A0A0A for card backgrounds
3. THE Landing_Page SHALL use #050505 for alternating section backgrounds
4. THE Landing_Page SHALL use #D4AF37 as the gold accent color
5. THE Landing_Page SHALL use #C5A017 as the gold hover state color
6. THE Landing_Page SHALL use Playfair Display font from Google Fonts for all headings
7. THE Landing_Page SHALL use Manrope font from Google Fonts for body text and UI elements
8. THE Landing_Page SHALL apply square edges to all components with border-radius of 0
9. THE Landing_Page SHALL apply a film grain overlay effect to enhance the cinematic aesthetic
10. THE Landing_Page SHALL apply fade-up reveal animations to sections as they enter the viewport

### Requirement 15: Responsive Design

**User Story:** As a mobile visitor, I want the website to adapt to my screen size, so that I can access all features comfortably.

#### Acceptance Criteria

1. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL display a single-column layout for all multi-column sections
2. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL display a hamburger menu instead of horizontal navigation links
3. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL adjust font sizes for optimal readability
4. WHERE the viewport width is below 768 pixels, THE Landing_Page SHALL adjust spacing and padding for touch-friendly interactions
5. THE Landing_Page SHALL achieve a Lighthouse mobile performance score of at least 85

### Requirement 16: Accessibility and Testing

**User Story:** As a developer, I want all interactive elements to be testable, so that I can ensure functionality through automated tests.

#### Acceptance Criteria

1. THE Landing_Page SHALL include unique data-testid attributes for all buttons
2. THE Landing_Page SHALL include unique data-testid attributes for all form inputs
3. THE Landing_Page SHALL include unique data-testid attributes for all navigation links
4. THE Landing_Page SHALL include unique data-testid attributes for all filter chips
5. THE Landing_Page SHALL include unique data-testid attributes for carousel navigation controls
6. THE Landing_Page SHALL produce zero console errors during normal operation
7. THE Landing_Page SHALL use semantic HTML elements for proper document structure
8. THE Landing_Page SHALL provide alt text for all images
