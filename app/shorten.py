from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from urllib.parse import urlparse
import random, string
import logging
import db

# Create a router instance for all "shorten" related routes
router = APIRouter()
logger = logging.getLogger(__name__)

def generate_code(length=7):
    """
    Generate a random 7-character short code.
    Uses uppercase, lowercase letters + digits. Ex: aB3d9Xz
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_safe_url(url: str):
    """
    Validate URL before shortening.
    Returns True only if URL has http/https scheme and a domain name.
    Prevents javascript: and ftp: links.
    """
    try:
        parsed = urlparse(url)
        return parsed.scheme in ["http", "https"] and parsed.netloc
    except:
        return False

@router.post("/shorten", response_class=HTMLResponse)
async def shorten_url(request: Request, url: str = Form(...)):
    """
    Handles POST request from home page form.
    Takes long URL, validates it, generates short code, saves to DB.
    """
    
    # 1. Validate the URL format
    if not is_safe_url(url):
        return HTMLResponse("<h1>❌ Only http/https URLs allowed</h1><a href='/'>Back</a>")

    # 2. Generate unique short code
    code = generate_code()
    # Loop until we get a code that doesn't already exist in DB
    while db.get_url(code):
        code = generate_code()

    # 3. Build the full short URL using host from request
    host = request.headers.get('host') # gets "localhost:8000" or "yourdomain.com"
    short_url = f"http://{host}/{code}"

    # 4. Save to database
    db.save_url(code, url, short_url)
    logger.info(f"CREATED: {code} -> {url}") # Log for tracking

    # 5. Return success HTML page with the short URL
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Done</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>✅ Done!</h1>
            <p>Your Short URL:</p>
            <p><a href="{short_url}" target="_blank">{short_url}</a></p>
            <a href="/"><button>Shorten Another</button></a>
        </div>
    </body>
    </html>"""
    return HTMLResponse(content=html)