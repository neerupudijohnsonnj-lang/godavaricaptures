# Email Notification Setup for Godavari Captures

## 📧 How It Works

When a customer submits a booking through your website, you'll automatically receive an email with all the booking details.

## ⚙️ Setup Instructions

### Step 1: Create Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Enable **2-Step Verification** (if not already enabled)
4. Search for "App passwords" or go to: https://myaccount.google.com/apppasswords
5. Click **"Select app"** → Choose **"Mail"**
6. Click **"Select device"** → Choose **"Other"** → Type "Godavari Captures"
7. Click **"Generate"**
8. **Copy the 16-character password** (you'll need this in Step 2)

### Step 2: Configure Email Settings

1. Navigate to the backend folder:
   ```
   cd backend
   ```

2. Create a `.env` file (copy from `.env.example`):
   ```
   copy .env.example .env
   ```

3. Open `.env` file and fill in your details:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   RECIPIENT_EMAIL=neerupudijohnsonnj@gmail.com
   ```

4. Replace:
   - `your-email@gmail.com` → Your Gmail address
   - `your-16-char-app-password` → The password from Step 1
   - `neerupudijohnsonnj@gmail.com` → Email where you want to receive bookings (already set)

### Step 3: Restart Backend Server

1. Stop the current backend server (Ctrl+C in the terminal)
2. Start it again:
   ```
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## ✅ Test It

1. Go to your website: http://localhost:3000
2. Fill out the booking form
3. Click "Book Now"
4. Check your email inbox (neerupudijohnsonnj@gmail.com)
5. You should receive a formatted email with all booking details!

## 📧 Email Format

You'll receive emails with:
- **Subject:** "New Booking: [Service] - [Customer Name]"
- **Content:**
  - Customer Name
  - Phone Number
  - Service Type
  - Event Date
  - Location
  - Message
  - Booking ID
  - Timestamp

## 🔧 Troubleshooting

### Email not sending?

1. **Check .env file exists** in the `backend` folder
2. **Verify Gmail App Password** is correct (16 characters, no spaces)
3. **Check backend console** for error messages
4. **Ensure 2-Step Verification** is enabled on your Google account

### Still not working?

The booking will still work even if email fails! Check the backend console for error messages:
- ✅ Success: "Booking email sent to neerupudijohnsonnj@gmail.com"
- ⚠️ Not configured: "SMTP not configured. Email would be sent to: ..."
- ❌ Error: "Failed to send email: [error message]"

## 🔒 Security Notes

- **Never commit .env file** to Git (it's already in .gitignore)
- **Use App Password**, not your regular Gmail password
- **Keep your .env file private**

## 📱 Alternative: Using Other Email Providers

### Outlook/Hotmail:
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

### Yahoo:
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

### Custom SMTP:
Contact your email provider for SMTP settings.

---

**Need help?** The system will log all email attempts to the backend console for debugging.
