from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import Profile

USER_TYPE_MEDIA = {
    "1": "users/images/dog.gif",
    "2": "users/images/i-have-to-pee-pee.gif",
    "3": "users/images/IMG_4220.JPG",
    "4": "users/images/images-4.jpeg",
    "5": "users/images/resume_caleb_mowery.pdf",
}

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("image_page")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})

def home(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def image_page(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    media_path = USER_TYPE_MEDIA.get(profile.user_type, USER_TYPE_MEDIA["1"])
    is_pdf = media_path.lower().endswith(".pdf")
    return render(request, "imagePage.html", {
        "profile": profile,
        "media_path": media_path,
        "is_pdf": is_pdf,
    })
