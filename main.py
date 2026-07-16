from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
import db

from routers import home, shorten, redirect

# ================== LOGGER CONFIG ==================
# Setup logging to write logs in both console and app.log file
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(message)s", 
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to file
        logging.StreamHandler()          # Print logs to console
    ]
)
logger = logging.getLogger(__name__)

# ================== FASTAPI APP ==================
app = FastAPI(title="URL Shortener AI")

# ================== STATIC FILES ==================
# Mount static folder to serve CSS, JS, Images
# You can access files at: http://localhost:8000/static/style.css
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================== STARTUP EVENT ==================
@app.on_event("startup")
async def startup_event():
    """
    This function runs once when the server starts.
    It initializes the database and creates tables if they don't exist.
    """
    db.init_db()
    logger.info("Database initialized successfully")

# ================== ROUTERS ==================
# Include all route files. This keeps code modular
app.include_router(home.router)      # Routes for home page and admin page
app.include_router(shorten.router)   # Routes for shortening URL
app.include_router(redirect.router)  # Routes for redirecting short URL

# ================== APP START LOG ==================
logger.info("App Started - URL Shortener AI is running")