from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import get_object_or_404
import logging
from blog.models import Post

logger = logging.getLogger(__name__)


# Create your views here.
def index(request): 
    posts = Post.objects.all()
    return render(request, 'pages/home.html', {'posts': posts})

def index1(request): 
    response = HttpResponse() 
    # response.writelines('<h1>Welcome to Dong A University</h1>') 
    # response.write('This is home app') 
    # return response
    return render(request, 'pages/tintuc.html')

def index2(request): 
    response = HttpResponse() 
    # response.writelines('<h1>Welcome to Dong A University</h1>') 
    # response.write('This is home app') 
    # return response
    return render(request, 'pages/khoahoc.html')

def infomation(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
        # Truyền thông tin profile vào context
        context = {'profile': profile}
        return render(request, 'pages/info.html', context)
    else:
        return render(request, 'pages/info.html')
def contact(request):
    response = HttpResponse() 
    return render(request, 'pages/contact.html')

def add_profile(request):
    profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                profile = None

            if not profile:
                profile = Profile(user=request.user)

            profile.full_name = form.cleaned_data['full_name']
            profile.address = form.cleaned_data['address']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.university = form.cleaned_data['university']
            profile.avatar = form.cleaned_data['avatar']

            profile.save()

            return redirect('/info')
    else:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
        form = ProfileForm(request.POST or None, user=request.user)
        return render(request, 'pages/profile.html', {'form': form, 'profile': profile})
    
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            form.save()
            return redirect('/info')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'pages/profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/login')  # Chuyển hướng đến trang chính sau khi đăng nhập thành công
    else:
        form = RegistrationForm()
    return render(request, 'pages/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Chuyển hướng đến trang chính sau khi đăng nhập thành công
        else:
            # Xử lý khi đăng nhập không thành công
            return render(request, 'pages/login.html', {'error_message': 'Tên đăng nhập hoặc mật khẩu không đúng'})
    else:
        if request.user.is_authenticated:
            # Lấy thông tin người dùng đã đăng nhập
            user = request.user
            
            # Truyền thông tin người dùng vào context
            context = {'user': user}
            
            # Trả về template HTML với context
            return render(request, 'pages/login.html', context)
        else:
            return render(request, 'pages/login.html')
        
@login_required
def logout_view(request):
    logout(request)
    # Chuyển hướng đến trang đăng nhập sau khi đăng xuất
    return redirect('login')
