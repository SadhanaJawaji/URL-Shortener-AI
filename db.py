import sqlite3

# ================== DATABASE CONFIG ==================
DB_NAME = "url.db" # SQLite database file name. Will be created automatically

# Connect to SQLite database
# check_same_thread=False is used because FastAPI runs with multiple threads
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor() # Cursor object to execute SQL queries

def init_db():
    """
    Initialize the database and create 'urls' table if it doesn't exist.
    This runs once when the app starts.
    """
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
        code TEXT PRIMARY KEY, 
        long_url TEXT NOT NULL, 
        short_url TEXT NOT NULL, 
        created_at TEXT, 
        last_clicked_at TEXT 
    )''')
    conn.commit() # Save changes to database
    print("✅ DB Ready - Table 'urls' initialized")

def save_url(code, long_url, short_url):
    """
    Save a new URL mapping to the database.
    Returns True if saved successfully, False if code already exists.
    """
    try:
        c.execute(
            "INSERT INTO urls (code, long_url, short_url, created_at, last_clicked_at) VALUES (?,?,?, CURRENT_TIMESTAMP, ?)",
            (code, long_url, short_url, None) # last_clicked_at = None initially
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This error comes if 'code' already exists because it's PRIMARY KEY
        return False

def get_url(code):
    """
    Fetch the original long URL for a given short code.
    Returns None if code is not found.
    """
    c.execute("SELECT long_url FROM urls WHERE code=?", (code,))
    row = c.fetchone() # Get first matching row
    return row[0] if row else None

def update_click_time(code):
    """
    Update 'last_clicked_at' timestamp when a short URL is accessed.
    """
    c.execute("UPDATE urls SET last_clicked_at = datetime('now') WHERE code=?", (code,))
    conn.commit()

def get_all_urls():
    """
    Fetch all URLs from the database.
    Ordered by newest created first. Used for admin panel.
    """
    c.execute("SELECT code, long_url, short_url, created_at, last_clicked_at FROM urls ORDER BY created_at DESC")
    return c.fetchall() # Returns list of tuples
