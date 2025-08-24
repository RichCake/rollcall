from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView


class UserListView(ListView):
    template_name = 'profiles/user_list.html'
    context_object_name = 'users'
    model = get_user_model()


class UserDetailView(DetailView):
    template_name = 'profiles/user_detail.html'
    context_object_name = 'user'
    model = get_user_model()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/user_update.html'
    context_object_name = 'user'
    model = get_user_model()
    fields = ['username', 'email', 'avatar']
    
    def get_success_url(self):
        return reverse_lazy('profiles:detail', args=[self.object.id])

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk != self.get_object().pk:
            raise Http404('Вы не имеете доступа к этой странице')
        return super().dispatch(request, *args, **kwargs)
