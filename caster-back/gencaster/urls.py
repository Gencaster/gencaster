from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import HttpResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

admin.site.site_header = "GenCaster admin"


class CorsAsyncGraphQLView(AsyncGraphQLView):
    """A hack to add CORS headers to our GraphQL endpoint."""

    def _create_response(self, response_data, sub_response):
        r = super()._create_response(response_data, sub_response)
        return r

    @method_decorator(csrf_exempt)
    async def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "options":
            return HttpResponse()
        return await super().dispatch(request, *args, **kwargs)


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path(
            "graphql",
            CorsAsyncGraphQLView.as_view(
                schema=schema,
                subscriptions_enabled=True,
                graphiql=settings.DEBUG,
            ),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
)
