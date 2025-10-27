import bcrypt
import pyotp
import json
import qrcode
from io import BytesIO
import base64
import sys
import os
from pathlib import Path

# Add parent directory to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.config import APP_NAME


def generate_user_config(username: str, password: str) -> dict:
    """Generate user configuration with hashed password and TOTP secret"""
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Generate TOTP secret
    totp_secret = pyotp.random_base32()
    
    return {
        "username": username,
        "password_hash": password_hash,
        "totp_secret": totp_secret,
        "role": "admin"
    }


def generate_qr_code(username: str, totp_secret: str, issuer: str = None) -> str:
    """Generate QR code for Google Authenticator setup"""
    if issuer is None:
        issuer = APP_NAME
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
        name=username,
        issuer_name=issuer
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for easy display
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str


if __name__ == "__main__":
    import os
    import sys
    from pathlib import Path
    
    # Add util to path for importing
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    from util.paths import get_temp_dir
    
    # Get temp directory using unified path management
    temp_dir = get_temp_dir()
    
    # Ensure temp directory exists
    temp_dir.mkdir(exist_ok=True)
    
    # Example user creation
    username = "admin"
    password = "hello"
    
    user_config = generate_user_config(username, password)
    
    # Create users.json in temp directory
    users_data = {
        "users": [user_config]
    }
    
    users_json_path = temp_dir / 'users.json'
    with open(users_json_path, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2)
    
    print(f"User configuration created for: {username}")
    print(f"TOTP Secret: {user_config['totp_secret']}")
    print(f"Manual entry URI: otpauth://totp/{APP_NAME}:{username}?secret={user_config['totp_secret']}&issuer={APP_NAME}")
    
    # Generate QR code
    qr_code = generate_qr_code(username, user_config['totp_secret'])
    
    # Save QR code as HTML for easy viewing in temp directory
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Authenticator Setup</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 2rem; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .qr-code {{ margin: 2rem 0; }}
            .secret {{ background: #f5f5f5; padding: 1rem; border-radius: 4px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Google Authenticator Setup</h1>
            <p>Scan this QR code with Google Authenticator:</p>
            <div class="qr-code">
                <img src="data:image/png;base64,{qr_code}" alt="QR Code">
            </div>
            <p><strong>Or manually enter this secret:</strong></p>
            <div class="secret">{user_config['totp_secret']}</div>
            <p><strong>Account:</strong> {username}</p>
            <p><strong>Issuer:</strong> {APP_NAME}</p>
        </div>
    </body>
    </html>
    """
    
    html_path = temp_dir / 'authenticator_setup.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Files saved to temp directory:")
    print(f"  - users.json: {users_json_path}")
    print(f"  - authenticator_setup.html: {html_path}")
    print("Open the HTML file in your browser to set up Google Authenticator")