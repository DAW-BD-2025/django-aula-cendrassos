from rest_framework.renderers import BaseRenderer


class PDFPassthroughRenderer(BaseRenderer):
    """Permetre la negociació de contingut de DRF per a respostes en format PDF sense processar."""

    media_type = "application/pdf"
    format = "pdf"
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
