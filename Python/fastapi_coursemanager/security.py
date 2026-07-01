from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt

# Secret key used to sign the JWT tokens.
SECRET_KEY = "super-secret-key-for-course-manager-api-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SECURITY EXPLANATION:
# Bcrypt is preferred over MD5 or SHA-256 for password hashing because:
# 1. Bcrypt is intentionally slow: It uses an adaptive hashing algorithm (work factor/rounds)
#    to slow down processing. This makes brute-force and hardware-accelerated attacks 
#    (e.g., using GPUs/ASICs) computationally expensive and impractical.
# 2. Automatic Salting: Bcrypt automatically generates a unique salt for each password,
#    which protects against rainbow table attacks (precomputed dictionary attacks).
# In contrast, MD5 and SHA-256 are fast cryptographic hash functions designed for speed.
# Because they are fast, modern computers can compute billions of MD5/SHA-256 hashes per second,
# making password cracking trivial if the database is compromised.

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt directly.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its bcrypt hash.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a signed JWT token containing the payload and expiration claim.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
