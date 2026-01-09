SPECIAL_LIMITS = {
    "/v1/api/auth/login": {"times": 5, "seconds": 60},
    "/v1/api/auth/register": {"times": 3, "seconds": 3600},
    "/v1/api/payments/place-order": {"times": 5, "seconds": 60},
}

DEFAULT_LIMIT = {"times": 30, "seconds": 60}