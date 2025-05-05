from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.encryption import encrypt_data, decrypt_data
from utils.key_management import get_encryption_key
import logging

logger = logging.getLogger(__name__)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_encrypted = db.Column(db.LargeBinary, nullable=False)
    email_encrypted = db.Column(db.LargeBinary, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    salt = db.Column(db.String(64), nullable=False, unique=True)
    
    # Relationship with diary entries
    entries = db.relationship('DiaryEntry', backref='author', lazy=True)
    
    @property
    def username(self):
        """Decrypt username for display purposes"""
        try:
            key = get_encryption_key(self.salt)
            return decrypt_data(self.username_encrypted, key)
        except Exception as e:
            logger.error(f"Error decrypting username: {str(e)}")
            return "Error decrypting username"
    
    @username.setter
    def username(self, username):
        """Encrypt username before storing"""
        try:
            key = get_encryption_key(self.salt)
            self.username_encrypted = encrypt_data(username, key)
        except Exception as e:
            logger.error(f"Error encrypting username: {str(e)}")
            raise
    
    @property
    def email(self):
        """Decrypt email for display purposes"""
        try:
            key = get_encryption_key(self.salt)
            return decrypt_data(self.email_encrypted, key)
        except Exception as e:
            logger.error(f"Error decrypting email: {str(e)}")
            return "Error decrypting email"
    
    @email.setter
    def email(self, email):
        """Encrypt email before storing"""
        try:
            key = get_encryption_key(self.salt)
            self.email_encrypted = encrypt_data(email, key)
        except Exception as e:
            logger.error(f"Error encrypting email: {str(e)}")
            raise
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)


class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_encrypted = db.Column(db.LargeBinary, nullable=False)
    content_encrypted = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def title(self):
        """Decrypt title for display purposes"""
        try:
            user = User.query.get(self.user_id)
            key = get_encryption_key(user.salt)
            return decrypt_data(self.title_encrypted, key)
        except Exception as e:
            logger.error(f"Error decrypting diary title: {str(e)}")
            return "Error decrypting title"
    
    @title.setter
    def title(self, title):
        """Encrypt title before storing"""
        try:
            user = User.query.get(self.user_id)
            key = get_encryption_key(user.salt)
            self.title_encrypted = encrypt_data(title, key)
        except Exception as e:
            logger.error(f"Error encrypting diary title: {str(e)}")
            raise
    
    @property
    def content(self):
        """Decrypt content for display purposes"""
        try:
            user = User.query.get(self.user_id)
            key = get_encryption_key(user.salt)
            return decrypt_data(self.content_encrypted, key)
        except Exception as e:
            logger.error(f"Error decrypting diary content: {str(e)}")
            return "Error decrypting content"
    
    @content.setter
    def content(self, content):
        """Encrypt content before storing"""
        try:
            user = User.query.get(self.user_id)
            key = get_encryption_key(user.salt)
            self.content_encrypted = encrypt_data(content, key)
        except Exception as e:
            logger.error(f"Error encrypting diary content: {str(e)}")
            raise
