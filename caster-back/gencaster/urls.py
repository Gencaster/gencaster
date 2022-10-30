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
        r.headers["Access-Control-Allow-Origin"] = "*"
        print("set headers for response")
        return r

    @method_decorator(csrf_exempt)
    async def dispatch(self, request, *args, **kwargs):
        print("dispatch? :)")
        if request.method.lower() == "options":
            r = HttpResponse()
            r.headers["Access-Control-Allow-Origin"] = "*"
            r.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
            r.headers[
                "Access-Control-Allow-Headers"
            ] = "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control"
            r.headers["Access-Control-Allow-Credentials"] = "true"
            return r
        return await super().dispatch(request, *args, **kwargs)


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path(
            "graphql",
            CorsAsyncGraphQLView.as_view(schema=schema, subscriptions_enabled=True),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
)
