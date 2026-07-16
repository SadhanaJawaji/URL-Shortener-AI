# 🔗 URL Shortener AI
A lightweight and fast URL shortener built with FastAPI and SQLite.
It converts long URLs into short 7-character links and tracks creation time and last click time.

## ✨ Features
- URL Shortening: Convert any long `http/https` URL into a short link
- Instant Redirect: Click the short link to get redirected immediately
- Activity Tracking: Stores `Created At` and `Last Clicked At` timestamps
- Admin Dashboard: View all shortened links at `/admin`
- Zero Setup: Uses SQLite database, no external setup required
- Simple UI: Clean HTML + CSS interface

## 🛠️ Tech Stack
- Backend Framework: FastAPI
- Web Server: Uvicorn
- Database: SQLite3
- Frontend: HTML, CSS

How to Run
- Double click - run_app.bat
OR
- Start the development server: bash uvicorn main:app --reload
- Open in your browser: http://localhost:8000

Project Structure:
URL-Shortener-AI/
├── main.py # Main application entry point
├── db.py # Database functions
├── routers/
│ ├── home.py # Home routes
│ ├── shorten.py # URL shortening logic
│ └── redirect.py # Redirect logic
├── static/
│ └── style.css # CSS styles
├── README.md # Project documentation
├── app.log # Application logs
└── url.db # SQLite database


🔌 APIEndpoints    
Method  Endpoint  Description
GET     /         Home page with URL form
POST    /shorten  Create a new short URL
GET     /{code}   Redirect to the original URL
GET     /admin    View all shortened URLs with timestamps

### Test Cases

**TC01: Shorten Valid URL**
Objective: Check if valid URL is shortened  
Steps:
1. Enter `https://www.google.com` in input field
2. Click "Shorten"  
Expected Result: Short URL is generated. Example: `http://localhost:8000/aB3d9Xz`  
Status: Pass

**TC02: Redirect Functionality**
Objective: Check if short URL redirects to original URL  
Steps:
1. Copy the generated short URL from TC01
2. Paste in browser and hit enter  
Expected Result: Browser redirects to `https://www.google.com`  
Status: Pass

**TC03: Invalid URL Handling**
Objective: Check error handling for invalid URL  
Steps:
1. Enter `abc123` or `ftp://test.com` in input field
2. Click "Shorten"  
Expected Result: Error message: "URL must start with http:// or https://"  
Status: Pass

**TC04: Empty URL Submission**
Objective: Check handling of empty input  
Steps:
1. Leave input field empty
2. Click "Shorten"  
Expected Result: Form shows "Please enter a URL" or backend returns 400 error  
Status: Pass

**TC05: Duplicate URL Handling**
Objective: Check if same long URL creates new short code or reuses old one  
Steps:
1. Shorten `https://www.youtube.com` twice  
Expected Result: New short code generated each time OR same code returned  
Status: Pass

**TC06: Admin Panel View**
Objective: Check if admin page lists all URLs  
Steps:
1. Go to `http://localhost:8000/admin`  
Expected Result: Table shows all short codes, original URLs, Created At, Last Clicked At  
Status: Pass