from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
import logging
import db

# Create a router instance for all "redirect" related routes
router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{code}")
async def redirect_url(code: str):
    """
    Handles GET request when someone visits a short URL.
    Example: http://localhost:8000/aB3d9Xz
    Looks up the code in DB and redirects to the original long URL.
    """
    
    # 1. Fetch the original long URL from database using the short code
    long_url = db.get_url(code)
    
    # 2. If code exists in DB
    if long_url:
        # Update 'last_clicked_at' timestamp for analytics
        db.update_click_time(code)
        
        # Log the redirect for tracking
        logger.info(f"REDIRECT: {code} -> {long_url}")
        
        # 301/307 redirect to the original URL
        return RedirectResponse(url=long_url)
    
    # 3. If code does NOT exist, show 404 page
    return HTMLResponse(
        content="<h1>404 - Link Not Found</h1><a href='/'>Back</a>",
        status_code=404
    )