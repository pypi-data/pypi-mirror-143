from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from oscar.core.application import OscarConfig
from oscar.core.loading import get_class
from oscar.config import Shop as _Shop
from custom.views import DynamicDataView, MessageAjaxView, ToggleSidebarView


class Shop(_Shop):
    def ready(self):
        super().ready()
        self.delivery_app = apps.get_app_config('delivery')
        self.newsletter_app = apps.get_app_config('newsletter')
        self.sync_app = apps.get_app_config('sync')

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        from oscar.views.decorators import login_forbidden
        from .views import HomeView

        urls = [
            path('', HomeView.as_view(), name='home'),
            path('shop/katalog/', self.catalogue_app.urls),
            path('shop/warenkorb/', self.basket_app.urls),
            path('shop/kasse/', self.checkout_app.urls),
            path('shop/kunde/', self.customer_app.urls),
            path('shop/suche/', self.search_app.urls),
            path('dashboard/', self.dashboard_app.urls),
            path('angebote/', self.offer_app.urls),
            path('lieferzeiten/', self.delivery_app.urls),
            path('sync/', self.sync_app.urls),

            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            path('password-reset/',
                login_forbidden(
                    auth_views.PasswordResetView.as_view(
                        form_class=self.password_reset_form,
                        success_url=reverse_lazy('password-reset-done'),
                        template_name='oscar/registration/password_reset_form.html'
                    )
                ),
                name='password-reset'),
            path('password-reset/done/',
                login_forbidden(auth_views.PasswordResetDoneView.as_view(
                    template_name='oscar/registration/password_reset_done.html'
                )),
                name='password-reset-done'),
            path('password-reset/confirm/<str:uidb64>/<str:token>/',
                login_forbidden(
                    auth_views.PasswordResetConfirmView.as_view(
                        form_class=self.set_password_form,
                        success_url=reverse_lazy('password-reset-complete'),
                        template_name='oscar/registration/password_reset_confirm.html'
                    )
                ),
                name='password-reset-confirm'),
            path('password-reset/complete/',
                login_forbidden(auth_views.PasswordResetCompleteView.as_view(
                    template_name='oscar/registration/password_reset_complete.html'
                )),
                name='password-reset-complete'),
            path('dynamic-data/', DynamicDataView.as_view(), name='dynamic-data'),
            path('message-ajax-url/', MessageAjaxView.as_view(), name='message-ajax-url'),
            path('toggle-sidebar-url/', ToggleSidebarView.as_view(), name='toggle-sidebar-url'),
        ]
        return urls
