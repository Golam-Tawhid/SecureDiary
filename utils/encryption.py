import os
import base64
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

def encrypt_data(data, key):
    """
    Encrypt data using AES-GCM mode
    
    Args:
        data (str): The data to encrypt
        key (bytes): The encryption key
        
    Returns:
        bytes: The encrypted data including IV and tag
    """
    try:
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate a random 96-bit IV
        iv = os.urandom(12)
        
        # Create an encryptor object
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
        
        # Add padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt the data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Concatenate IV, ciphertext, and tag for storage
        return iv + encryptor.tag + ciphertext
    
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        raise RuntimeError(f"Failed to encrypt data: {str(e)}")

def decrypt_data(encrypted_data, key):
    """
    Decrypt data that was encrypted using AES-GCM mode
    
    Args:
        encrypted_data (bytes): The encrypted data including IV and tag
        key (bytes): The encryption key
        
    Returns:
        str: The decrypted data as a UTF-8 string
    """
    try:
        # Extract IV (first 12 bytes)
        iv = encrypted_data[:12]
        # Extract tag (next 16 bytes)
        tag = encrypted_data[12:28]
        # Extract ciphertext (remaining bytes)
        ciphertext = encrypted_data[28:]
        
        # Create a decryptor object
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        
        # Decrypt the data
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        # Return as string
        return data.decode('utf-8')
    
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        raise RuntimeError(f"Failed to decrypt data: {str(e)}")

def generate_hmac(data, key):
    """
    Generate HMAC for data integrity verification
    
    Args:
        data (bytes): The data to generate HMAC for
        key (bytes): The HMAC key
        
    Returns:
        bytes: The HMAC value
    """
    from cryptography.hazmat.primitives import hmac, hashes
    
    try:
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(data)
        return h.finalize()
    
    except Exception as e:
        logger.error(f"HMAC generation error: {str(e)}")
        raise RuntimeError(f"Failed to generate HMAC: {str(e)}")

def verify_hmac(data, key, hmac_value):
    """
    Verify HMAC for data integrity
    
    Args:
        data (bytes): The data to verify
        key (bytes): The HMAC key
        hmac_value (bytes): The HMAC to verify against
        
    Returns:
        bool: True if HMAC verification succeeded, False otherwise
    """
    from cryptography.hazmat.primitives import hmac, hashes
    from cryptography.exceptions import InvalidSignature
    
    try:
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(data)
        h.verify(hmac_value)
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        logger.error(f"HMAC verification error: {str(e)}")
        return False
