from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),  # ✅ API routes
    path("", TemplateView.as_view(template_name="Home.html")),  # ✅ Home Page
    path("about/", TemplateView.as_view(template_name="About.html")),
    path("contact/", TemplateView.as_view(template_name="Contact.html")),
    path("login/", TemplateView.as_view(template_name="index.html")),
    path("register/", TemplateView.as_view(template_name="index.html")),
    path("dealers/", TemplateView.as_view(template_name="index.html")),
    path(
        "dealer/<int:dealer_id>/",
        TemplateView.as_view(template_name="index.html")),
    path(
        "djangoapp/postreview/<int:dealer_id>/",
        TemplateView.as_view(template_name="index.html"),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
