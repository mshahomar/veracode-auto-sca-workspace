import hmac
import hashlib
from typing import Union
from datetime import datetime

PREFIX = "VERACODE-HMAC-SHA-256"
VER_STR = "vcode_request_version_1"

def hmac256(data: bytes, key: bytes, format: Union[str, None] = None) -> Union[bytes, str]:
    """
    Computes the HMAC-SHA256 hash of the given data using the provided key.

    Args:
        data (bytes): The data to be hashed.
        key (bytes): The key to be used for the HMAC computation.
        format (Union[str, None]): The format in which to return the hash. If None, returns the hash as bytes.

    Returns:
        Union[bytes, str]: The computed HMAC-SHA256 hash, either as bytes or a hexadecimal string.
    """
    hash_obj = hmac.new(key, data, hashlib.sha256)
    if format is None:
        return hash_obj.digest()
    else:
        return hash_obj.hexdigest()

def get_byte_array(hex_str: str) -> bytes:
    """
    Converts a hexadecimal string to a byte array.

    Args:
        hex_str (str): The hexadecimal string to be converted.

    Returns:
        bytes: The byte array representation of the hexadecimal string.
    """
    return bytes.fromhex(hex_str)

def generate_header(url: str, method: str, host: str, id: str, key: str) -> str:
    """
    Generates the authorization header for the Veracode API request.

    Args:
        url (str): The API endpoint path.
        method (str): The HTTP method (GET, POST, etc.).
        host (str): The host name for the API request.
        id (str): The Veracode ID.
        key (str): The Veracode Key.

    Returns:
        str: The authorization header value.
    """
    data = f"id={id}&host={host}&url={url}&method={method}"
    timestamp = str(int(datetime.now().timestamp() * 1000))  # Milliseconds since epoch
    nonce = hmac256(get_byte_array(key), b'', 'hex')

    # Calculate signature
    hashed_nonce = hmac256(get_byte_array(nonce), get_byte_array(key))
    hashed_timestamp = hmac256(timestamp.encode(), hashed_nonce)
    hashed_ver_str = hmac256(VER_STR.encode(), hashed_timestamp)
    signature = hmac256(data.encode(), hashed_ver_str, 'hex')

    return f"{PREFIX} id={id},ts={timestamp},nonce={nonce},sig={signature}"