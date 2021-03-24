from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import MultipleObjectMixin

from profile_app.forms import UpdateUserForm, RegisterUserForm


# Create your views here.


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        view = ProfileDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UpdateUserView.as_view()
        return view(request, *args, **kwargs)


class UpdateUserView(UpdateView):
    template_name = 'user/profile_detail.html'
    form_class = UpdateUserForm
    model = User

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(UpdateUserView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.object.pk})


class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'user/profile_detail.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        self.object = self.get_object(User.objects.prefetch_related('article_set'))
        object_list = self.object.article_set.all()
        context = super(ProfileDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = UpdateUserForm()
        return context


@login_required
def user_profile(request):
    return redirect('profile_detail', user_id=request.user.id)


@login_required
def delete_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    logout(request)
    user.delete()
    return redirect('main_page')


class RegistraionView(SuccessMessageMixin, CreateView):
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('main_page')
    form_class = RegisterUserForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        self.object = form.save()
        self.object.set_password(form.cleaned_data['password'])
        login(request=self.request, user=self.object)
        return super().form_valid(form)
