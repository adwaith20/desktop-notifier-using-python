import base64

def encrypt_to_base64(text):
    # Convert string to bytes
    bytes_text = text.encode('utf-8')
    
    # Encode bytes to base64
    encoded_bytes = base64.b64encode(bytes_text)
    
    # Convert bytes back to string
    encrypted_text = encoded_bytes.decode('utf-8')
    
    return encrypted_text