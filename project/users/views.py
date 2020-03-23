from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .tokens import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from .models import Profile
from blog.models import Post
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'users/email_konfirmasi_daftar.html')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'users/email_konfirmasi_daftar_done.html')
    else:
        return render (request, 'users/email_konfirmasi_invalid.html')


@login_required
def Profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Anda berhasil mengubah akun')
            # return redirect('users:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'users': request.user
    }
    return render(request, 'users/profile.html', context)


class Bookmarks(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'users/bookmark.html'

    def get(self, request, *args, **kwargs):
        users = request.user
        likes = users.requirement_post_likes.all()
        bookmarks = users.bookmarks.all()
        print(bookmarks)
        
        self.context = {
            'likes':likes,
            'users':users,
            'bookmarks':bookmarks,
        }
        return render(self.request, self.template_name, self.context)


