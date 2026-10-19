from rest_framework.renderers import BaseRenderer, JSONRenderer


class PDFPassthroughRenderer(BaseRenderer):
    """Permetre la negociació de contingut de DRF per a respostes en format PDF sense processar."""

    media_type = "application/pdf"
    format = "pdf"
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        if response is not None and getattr(response, "exception", False):
            response["Content-Type"] = "application/json"
            return JSONRenderer().render(data, "application/json", renderer_context)

        return data
