from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),  # ✅ API routes
    path('', TemplateView.as_view(template_name="Home.html")),  # ✅ Home Page
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),  # ✅ React Login
    path('register/', TemplateView.as_view(template_name="index.html")),  # ✅ React Register
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)