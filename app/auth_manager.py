import binascii
import hashlib


def is_request_authorized(request):
    # Hacky implementation until we do real auth.
    token = request.form.get('token')
    digest = hashlib.pbkdf2_hmac('sha256', token, b'pretzel house', 10000)
    return binascii.hexlify(
        digest) == b'487e77206426696f2f7449367e33502a266a5a4930232667463a'
