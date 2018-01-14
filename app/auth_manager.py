import binascii
import hashlib


def is_request_authorized(request):
    # Hacky implementation until we do real auth.
    token = request.form.get('token')
    digest = hashlib.pbkdf2_hmac('sha256', token, b'pretzel house', 10000)
    print 'result=[%s]' % binascii.hexlify(digest)
    return binascii.hexlify(
        digest
    ) == b'79f7a50742e7dfad41993b5edf3b1954246efc52b0f46c711bcc65cdd3ed8d9c'
