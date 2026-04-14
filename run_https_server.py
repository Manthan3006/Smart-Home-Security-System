#!/usr/bin/env python3
"""
HTTPS Server for GPS Testing
Some browsers require HTTPS for geolocation API
"""

import ssl
from app import app

if __name__ == '__main__':
    # Create a simple self-signed certificate context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')  # You'll need to generate these
    
    print("🔒 Starting HTTPS server for GPS testing...")
    print("📱 Access at: https://127.0.0.1:8443")
    print("⚠️  You'll need to accept the self-signed certificate")
    
    app.run(debug=True, host='127.0.0.1', port=8443, ssl_context=context)