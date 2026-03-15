import csv
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "users.csv"
HEADERS = ["name", "email", "verified", "joined_date", "level", "api_key", "last_active", "status"]

def _ensure_storage_exists() -> None:
    """Make sure the CSV file exists with the complete schema headers."""
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def add_user(name: str, email: str, verified: bool = False, level: str = "lvl_1") -> None:
    """Append a new user with generated timestamps, API keys, and default levels."""
    _ensure_storage_exists()
    
    joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_active = joined_date
    api_key = f"en_{uuid.uuid4().hex}" 
    status = "active"
    
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, str(verified), joined_date, level, api_key, last_active, status])

def get_all_users() -> List[Dict[str, str]]:
    """Return every saved user as a list of dictionaries."""
    _ensure_storage_exists()
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def user_exists(name: str, email: str) -> bool:
    """Check if a user with the name OR email already exists."""
    users = get_all_users()
    for user in users:
        if user.get('name', '').lower() == name.lower() or user.get('email', '').lower() == email.lower():
            return True
    return False

def update_last_active(username: str) -> None:
    """Updates the last_active timestamp when a user logs in."""
    users = get_all_users()
    updated = False
    
    for user in users:
        if user.get('name', '').lower() == username.lower():
            user['last_active'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = True
            break
            
    if updated:
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(users)


def update_user_level(username: str, new_level: str) -> None:
    """Upgrades or downgrades a user's access level in the system."""
    users = get_all_users()
    updated = False
    
    for user in users:
        if user.get('name', '').lower() == username.lower():
            user['level'] = new_level
            updated = True
            break
            
    if updated:
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(users)