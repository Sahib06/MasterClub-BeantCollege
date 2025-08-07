import qrcode
import base64
import io
import json
from datetime import datetime, timedelta
from typing import Dict, Any
import uuid

class QRGenerator:
    @staticmethod
    def generate_session_token() -> str:
        """Generate a unique session token"""
        return str(uuid.uuid4())
    
    @staticmethod
    def create_session_data(
        session_token: str,
        subject: str,
        class_name: str,
        section: str = None,
        duration_minutes: int = 10
    ) -> Dict[str, Any]:
        """Create session data for QR code"""
        expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
        
        session_data = {
            "session_token": session_token,
            "subject": subject,
            "class": class_name,
            "section": section,
            "expires_at": expires_at.isoformat(),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return session_data
    
    @staticmethod
    def generate_qr_code(session_data: Dict[str, Any]) -> str:
        """Generate QR code from session data and return as base64 string"""
        # Convert session data to JSON string
        qr_data = json.dumps(session_data, separators=(',', ':'))
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Encode to base64
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return img_str
    
    @staticmethod
    def parse_qr_data(qr_data: str) -> Dict[str, Any]:
        """Parse QR code data back to dictionary"""
        try:
            return json.loads(qr_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid QR code data format")
    
    @staticmethod
    def is_session_expired(session_data: Dict[str, Any]) -> bool:
        """Check if session has expired"""
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        return datetime.utcnow() > expires_at 