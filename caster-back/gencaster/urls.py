"""gencaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from dataclasses import dataclass

from channels.layers import BaseChannelLayer, get_channel_layer
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

admin.site.site_header = "GenCaster admin"


@dataclass
class Context:
    channel_layer: BaseChannelLayer


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

    async def get_context(
        self, request: HttpRequest, response: HttpResponse
    ) -> Context:
        context: Context = await super().get_context(request, response)
        context.channel_layer = get_channel_layer()  # type: ignore
        return context


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
