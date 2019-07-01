from django.shortcuts import render, get_object_or_404
from .models import Resource
from .forms import NewResourceForm, UserForm, UserProfileInfoForm, UserLoginForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# Index view which will be used as the homepage
def index(request):
    return render(request, 'res_app/index.html', {})

# View to list all resources
def resource_list(request):
    res_list = Resource.objects.order_by("pk")
    res_dict = {'res_list':res_list}
    return render(request, 'res_app/resource_list.html', context=res_dict)

# View to list the details of a specific resource selected from the resource list
def res_details(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'res_app/res_details.html', {'res_details':resource})

# View to create new resources
def new_res(request):
    res_form = NewResourceForm()
    if request.method == 'POST':
        res_form = NewResourceForm(request.POST)

        if res_form.is_valid():
            res_form.save(commit=True)
            return resource_list(request)

        else:
            print("ERROR: Invalid Form!")
    else:
        return render(request, 'res_app/new_res.html', {'res_form':res_form})

# View to edit resources
def res_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        res_form = NewResourceForm(request.POST, instance=resource)
        if res_form.is_valid():
            resource = res_form.save(commit=False)
            res_form.save()
            return res_details(request, pk=resource.pk)
    else:
        res_form = NewResourceForm(instance = resource)
        return render(request, 'res_app/new_res.html', {'res_form':res_form})

# View for a user to register on the site
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # grab the basic user information from the user_form, set a password
            # and save the user object
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # grab the profile_form information but don't commit until a relationship
            # has been created with the user_form
            profile = profile_form.save(commit=False)
            # set up the one-to-one relationship between the two forms
            profile.user = user

            # check if the user has provided a profile picture
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.files['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'res_app/registration.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'registered': registered})



# View for a registered user to log in to the site
def user_login(request):

    # check if a POST request has been submitted by the user, if so grab the posted data
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        print(user_form.errors)

        # if the user form is valid grab the data
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE")
            else:
                print('Someone tried to login and failed')
                print(f"Username '{username}' and password '{password}' entered incorrectly")
                return HttpResponse("Invalid login details provided")
        else:
            print('User form is invalid')
    else:
        # create a new form from the UserLoginForm
        user_form = UserLoginForm()

    return render(request, 'res_app/login.html', {'user_form':user_form})

# View for a user to log out of the site when they are logged in
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
