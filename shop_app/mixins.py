from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class SuperUserRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class PageCounterReloadMixin:
    def check_reload(self, request):
        page_counter = self.request.session.get('page_counter', 0)
        message = self.request.session.get('message', False)
        page_counter += 1
        request.session['page_counter'] = page_counter
        if page_counter == 4:
            request.session['page_counter'] = 0
            request.session['message'] = True
            return HttpResponseRedirect(reverse_lazy('index'))
        return None