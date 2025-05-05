import os
import base64
import hashlib
import logging
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

def generate_salt():
    """
    Generate a random salt for key derivation
    
    Returns:
        str: A base64-encoded salt string
    """
    try:
        salt = os.urandom(32)
        return base64.b64encode(salt).decode('utf-8')
    except Exception as e:
        logger.error(f"Salt generation error: {str(e)}")
        raise RuntimeError(f"Failed to generate salt: {str(e)}")

def get_encryption_key(salt, iterations=100000):
    """
    Derive an encryption key from a salt and a master key
    
    Args:
        salt (str): Base64-encoded salt string
        iterations (int): Number of iterations for key derivation
        
    Returns:
        bytes: Derived key for encryption/decryption
    """
    try:
        # Get the master key from environment or use a fallback (not recommended for production)
        master_key = os.environ.get('ENCRYPTION_MASTER_KEY', 'default-master-key-for-development-only')
        
        # Convert salt from base64 string to bytes
        salt_bytes = base64.b64decode(salt)
        
        # Create a key derivation function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits for AES-256
            salt=salt_bytes,
            iterations=iterations,
            backend=default_backend()
        )
        
        # Derive the key
        key = kdf.derive(master_key.encode('utf-8'))
        return key
    
    except Exception as e:
        logger.error(f"Key derivation error: {str(e)}")
        raise RuntimeError(f"Failed to derive encryption key: {str(e)}")

def rotate_encryption_key(old_salt, new_salt, data):
    """
    Re-encrypt data with a new key (for key rotation)
    
    Args:
        old_salt (str): Old salt used for key derivation
        new_salt (str): New salt for key derivation
        data (bytes): Encrypted data using the old key
        
    Returns:
        bytes: Data re-encrypted with the new key
    """
    from utils.encryption import decrypt_data, encrypt_data
    
    try:
        # Get old and new keys
        old_key = get_encryption_key(old_salt)
        new_key = get_encryption_key(new_salt)
        
        # Decrypt with old key
        decrypted_data = decrypt_data(data, old_key)
        
        # Re-encrypt with new key
        return encrypt_data(decrypted_data, new_key)
    
    except Exception as e:
        logger.error(f"Key rotation error: {str(e)}")
        raise RuntimeError(f"Failed to rotate encryption key: {str(e)}")
