from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import db

# Create a router instance for home page and admin page routes
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home():
    """
    Home page route: /
    Shows the main form where user can paste a long URL to shorten.
    """
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <!-- Link to CSS for styling -->
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>🔗 URL Shortener</h1>
            
            <!-- Form to submit long URL. Sends POST request to /shorten -->
            <form action="/shorten" method="post">
                <!-- Input type=url validates http/https format -->
                <input type="url" name="url" placeholder="https://example.com" required>
                <button>Shorten</button>
            </form>
            
            <br>
            <!-- Link to admin page to view all shortened URLs -->
            <a href="/admin">View All Links</a>
        </div>
    </body>
    </html>"""
    return HTMLResponse(content=html)

@router.get("/admin", response_class=HTMLResponse)
async def admin():
    """
    Admin page route: /admin
    Fetches all URLs from DB and displays them in a table with analytics.
    """
    # 1. Get all URLs from database
    urls = db.get_all_urls()
    
    # 2. Build table rows dynamically
    rows = ""
    for code, long_url, short_url, created_at, last_clicked_at in urls:
        # If never clicked, show "Never" instead of None
        last = last_clicked_at if last_clicked_at else "Never"
        
        # Truncate long URL to 50 chars for better table view
        rows += f"<tr><td><a href='{short_url}' target='_blank'>{short_url}</a></td><td>{long_url[:50]}...</td><td>{created_at}</td><td>{last}</td></tr>"

    # 3. Return HTML table with all data
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Admin</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>📋 All Links</h1>
            <table border="1" style="width:100%; border-collapse: collapse;">
                <tr>
                    <th>Short URL</th>
                    <th>Long URL</th>
                    <th>Created At</th>
                    <th>Last Clicked</th>
                </tr>
                {rows} <!-- Insert all dynamic rows here -->
            </table>
            <br>
            <a href="/">Back Home</a>
        </div>
    </body>
    </html>"""
    return HTMLResponse(content=html)