NOMBRE_CABECERA_CSP = "Content-Security-Policy"
ORIGENES_EXTERNOS = (
    "https://cdnjs.cloudflare.com https://code.jquery.com "
    "https://stackpath.bootstrapcdn.com https://use.fontawesome.com"
)
POLITICA_CSP = (
    "default-src 'self'; "
    f"script-src 'self' 'unsafe-inline' {ORIGENES_EXTERNOS}; "
    f"style-src 'self' 'unsafe-inline' {ORIGENES_EXTERNOS}; "
    f"font-src 'self' data: {ORIGENES_EXTERNOS}; "
    "img-src 'self' data:; "
    "frame-ancestors 'self'"
)


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        respuesta = self.get_response(request)
        if NOMBRE_CABECERA_CSP not in respuesta:
            respuesta[NOMBRE_CABECERA_CSP] = POLITICA_CSP
        return respuesta