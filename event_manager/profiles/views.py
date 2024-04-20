from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView


class UserListView(ListView):
    template_name = 'profiles/user_list.html'
    context_object_name = 'users'
    model = get_user_model()


class UserDetailView(DetailView):
    template_name = 'profiles/user_detail.html'
    context_object_name = 'user'
    model = get_user_model()