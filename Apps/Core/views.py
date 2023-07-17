from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView,TemplateView

# Create your views here.

#LOGIN

class LoginFormView(LoginView):
    template_name = 'login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


class IndexView(TemplateView):
    template_name = 'index.html'