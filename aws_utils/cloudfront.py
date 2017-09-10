import base64
import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


def _replace_unsupported_chars(some_str):
    """Replace unsupported chars: '+=/' with '-_~'"""
    return some_str.replace("+", "-") \
        .replace("=", "_") \
        .replace("/", "~")


def rsa_signer(message, key):
    """
    Based on https://boto3.readthedocs.io/en/latest/reference/services/cloudfront.html#examples
    """
    private_key = serialization.load_pem_private_key(
        key,
        password=None,
        backend=default_backend()
    )
    signer = private_key.signer(padding.PKCS1v15(), hashes.SHA1())
    signer.update(message)
    return signer.finalize()


def generate_policy_cookie(url, expiration):
    """Returns a tuple: (policy json, policy base64)"""

    policy_dict = {
        "Statement": [
            {
                "Resource": url,
                "Condition": {
                    "DateLessThan": {
                        "AWS:EpochTime": expiration
                    }
                }
            }
        ]
    }

    # Using separators=(',', ':') removes seperator whitespace
    policy_json = json.dumps(policy_dict, separators=(",", ":"))

    policy_64 = str(base64.b64encode(policy_json.encode("utf-8")), "utf-8")
    policy_64 = _replace_unsupported_chars(policy_64)
    return policy_json, policy_64


def generate_signature(policy, key):
    """Creates a signature for the policy from the key, returning a string"""
    sig_bytes = rsa_signer(policy.encode("utf-8"), key)
    sig_64 = _replace_unsupported_chars(str(base64.b64encode(sig_bytes), "utf-8"))
    return sig_64


def generate_cookies(policy, signature, cloudfront_id):
    """Returns a dictionary for cookie values in the form 'COOKIE NAME': 'COOKIE VALUE'"""
    return {
        "CloudFront-Policy": policy,
        "CloudFront-Signature": signature,
        "CloudFront-Key-Pair-Id": cloudfront_id
    }


def generate_signed_cookies(path, private_key, private_key_id, expiration):
    policy_json, policy_64 = generate_policy_cookie(path, expiration)
    signature = generate_signature(policy_json, private_key)
    return generate_cookies(policy_64, signature, private_key_id)
