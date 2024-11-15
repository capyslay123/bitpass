from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from .models import Name, Categories, AccountPassword
from .util import cipher

# Create your views here.

# HOME PAGE ---> ENTRY PAGE OF WEBSITE
def home(request):
    return render(request, 'base/home.html')

# SIGN-UP PAGE LOGIC
def sign_up(request):
    # IF USER TRIES TO GO TO SIGN UP THORUGH LINK FIRST CHECK IF USER IS ALREADY LOGGED IN, IF YES THEN REDIRECT THEM TO VAULT PAGE
    if request.user.is_authenticated:
        return redirect('vault')

    error_message = "" #IF SIGN UP ERROR OCCURS SEND ERROR MESSAGE TO USER

    MINIMUM_PASSWORD_LENGTH = 6

    if request.method == "POST":
        # GETTING VALUES FROM SIGN-UP FORM
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        try:
            # IF TRY BLOCK DOESN'T THROW ERROR MEANS USERNAME ALREADY THERE IN DB, THEREFORE THROW ERROR MESSAGE
            User.objects.get(username=username)
            error_message = "Username already taken!"
        except:
            if len(password) > MINIMUM_PASSWORD_LENGTH:
                if password == confirm_password:
                    user = User.objects.create_user(username=username, password=password)
                    Name.objects.create(user=user, name=name)
                    login(request, user) #LOGIN USER AND CREATING SESSION ID IN BROWSER
                    return redirect('vault') #REDIRECTING USER TO VAULT PAGE AFTER SUCCESSFUL LOGIN
                else:
                    error_message = "Retyped password doesn't match"
            else:
                error_message = "Password length should be greater than 6 Characters"

    context = {'error_message': error_message}

    return render(request, 'base/sign-up.html', context)

# LOGIN PAGE LOGIC
def login_page(request):
    error_message = "" #IF LOGIN ERROR OCCURS SEND ERROR MESSAGE TO USER

    # IF USER TRIES TO GO TO LOGIN THORUGH LINK FIRST CHECK IF USER IS ALREADY LOGGED IN, IF YES THEN REDIRECT THEM TO VAULT PAGE
    if request.user.is_authenticated:
        return redirect('vault')

    if request.method == "POST":
        # GETTING VALUES FROM LOGIN FORM
        username = request.POST.get('username')
        password = request.POST.get('password')

        # TO CHECK IF USER EXIST, IF NOT THEN THROWS AN ERROR MESSAGE TO USER
        try:
            user = User.objects.get(username=username)
        except:
            error_message = "Username Doesn't Exist"

        # IF THERE ARE NO ERROR MESSAGE THEN USER EXIST
        if not error_message:
            user = authenticate(request, username=username, password=password) #AUTHENTICATE PASSWORD
            
            # IF FAILS TO AUTHENTICATE THEN 'user' VALUE WILL BE NONE, THEN THROWS ERROR MESSAGE TO USER
            if user:
                login(request, user)
                return redirect('vault')
            else:
                error_message = "Username or Password Doesn't Exist"

    context = {'error_message': error_message}
 
    return render(request, 'base/login.html', context)

#LOGIC FOR CREATING CATEGORY FOR ACCOUNT PASSWORD
@login_required(login_url='login')
def add_category(request):
    if request.method == "POST":
        user = request.user # GETS CURRENT LOGGED IN USER

        # GETTING DATA FROM ADD CATEGORY FORM
        category = request.POST.get('category')

        # USED TO CHECK IF USER ALREADY HAS THE CATEGORY
        try:
            # IF USER HAS THE CATEGORY THEN SHOW ERROR, IF TRY BLOCK DOESN'T THROW EXCEPTION THEN CATEGORY ALREADY EXIST IN DB ---> SHOW ERROR TO USER
            user.categories_set.get(category_name=category)
            messages.error(request, f'{category} Category already exist') # ERROR MESSAGE
        except:
            # CATEGORY DOESN'T EXIST ---> CREATE THE CATEGORY
            Categories.objects.create(user=user, category_name=category)
            messages.success(request, 'Category Added Successfully') # SUCCESS MESSAGE
        
    # GETS THE PREVIOUS URL SO AS TO KNOW IN WHICH URL TO REDIRECT AFTER FORM SUBMIT
    previous_url = request.META.get('HTTP_REFERER')
    
    if 'vault' in previous_url:
        return redirect('vault')
    
    if 'add-password' in previous_url:
        return redirect('add-password')
    
    # WHEN USER COMES FROM URL INSTEAD FROM FORM
    if not category:
        return redirect('vault')

# ADD PASSSWORD LOGIC
@login_required(login_url='login')
def add_password(request):
    user = request.user # GETS CURRENT LOGGED IN USER

    categories_of_user = user.categories_set.all() # GETS ALL THE CATEGORY OF CURRENT USER

    if request.method == "POST":

        # GETTING VALUES FROM ADD PASSWORD FORM
        title = request.POST.get('title').strip()
        url = request.POST.get('url').strip()
        category = request.POST.get('category')
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = cipher.encrypt_data(request.POST.get('password')) # ENCRYPT THE DATA COMING FROM FORM

        # SAVING FORM DATA TO DB 
        AccountPassword.objects.create(
            user=user,
            title=title,
            url=url,
            category=user.categories_set.get(category_name=category), # QUERY'IN CHILD (CATEGORY) FROM PARENT (USER)
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Password added successfully")


    context = {'categories': categories_of_user}

    return render(request, 'base/add-password.html', context)

# VAULT PAGE LOGIC ---> PASSWORD SHOWN TO USER
@login_required(login_url='login')
def vault(request):
    user = request.user # GETS CURRENT LOGGED IN USER

    # PARAMETER FOR SEARCH, GETS THE VALUE THROUGH WHICH WE CAN SEARCH / FILTER THE DB
    q = request.GET.get('q') if request.GET.get('q') else '' 

    categories_of_user = user.categories_set.all() # GETS ALL THE CATEGORY OF CURRENT USER

    # FILTERS THE ACCOUNT PASSWORD BASED ON THE SEARCH PARAMETER
    user_account_passwords = AccountPassword.objects.filter(
        Q(user=user) &
        (Q(title__icontains=q) |
         Q(category__category_name__exact=q)) # QUERY'IN THE 'ACCOUNT PASWORD' 'CATEGORY' FIELD TO THE PARENT 'CATEGORY' MODEL'S 'CATEGORY_NAME' FIELD
    )

    # USER'S ACCOUNT PASSWORD LIST WHICH WILL BE SENT TO FRONTEND
    user_accounts_passwords_lst = []

    # EXTRACTING ACCOUNT PASSWORD FROM THE DB AND STORING THE DATA TO THE LIST, THIS IS BASICALLY DONE SO THAT WE CAN DECRYPT THE PASSWORD IN THE DB SO THE USER CAN SEE THE PASSWORD IN THE FRONTEND
    for account_password in user_account_passwords:
        # FOR EVERY ACCOUNT PASSWORD THERE IS A DICTIONARY WHICH IS THEN STORED IN THE LIST
        account_password_dict = {}

        # SAVING GENERAL DATA FROM DB TO DICTIONARY
        account_password_dict['id'] = account_password.id
        account_password_dict['category'] = account_password.category
        account_password_dict['title'] = account_password.title
        account_password_dict['email'] = account_password.email
        
        # DECRYPTING THE PASSWORD
        decrypted_password = cipher.decrypt_data(eval(account_password.password))
        account_password_dict['password'] = decrypted_password

        # IF ACCOUNT PASSWORD HAS NO URL SHOW THE LOGO IN THE ACRONYM FORM
        if account_password.url:
            account_password_dict['url'] = account_password.url
        else:
            account_password_dict['url'] = None

            # LOGIC FOR ACRONYM
            account_logo_acronym = ""
            title = account_password.title
            
            for i in range(len(title)):
                if i == 0:
                    account_logo_acronym += title[0]

                if title[i] == " ":
                    account_logo_acronym += title[i + 1]
                
            # CREATING A NEW FIELD (THIS INFO IS NOT PRESENT IN DB)
            account_password_dict['acronym'] = account_logo_acronym

        account_password_dict['username'] = account_password.username if account_password.username else None

        user_accounts_passwords_lst.append(account_password_dict)

    context = {'categories': categories_of_user, 'account_passwords': user_accounts_passwords_lst}

    return render(request, 'base/vault.html', context)

# LOGIC FOR EDIT ACCOUNT PASSWORD SAVED BY USER ---> USERS CAN EDIT THEIR ACCOUNT PASSWORD DETAILS
@login_required(login_url='login')
def edit_account_password(request, pk):
    user = request.user # GETS CURRENT LOGGED IN USER

    # GETS THE ACCOUNT PASSWORD WHICH IS TO BE EDITED USING ID WHICH WILL BE PASSED IN URL
    account_password = AccountPassword.objects.get(id=int(pk))
    
    if account_password.user.id != user.id:
        return redirect('vault')

    categories_of_user = user.categories_set.all() # GETS ALL THE CATEGORY OF CURRENT USER

    title_acronym = ""
    # IF THERE WERE NO PREVIOUS URL FOR ACCOUNT PASSWORD CALCULATE THE ACRONYM AND SEND IT TO FRONTEND
    if not account_password.url:
        old_title = account_password.title
        for i in range(len(old_title)):
            if i == 0:
                title_acronym += old_title[i]
            
            if old_title[i] == " ":
                title_acronym += old_title[i + 1]

    if request.method == 'POST':
        title = request.POST.get('title').strip()
        url = request.POST.get('url').strip()
        category = request.POST.get('category')
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        # CHECKS IF USER SUBMITS EMPTY FORM
        if title or url or username or email or password:
            # FORM IS NOT EMPTY
            if title:
                account_password.title = title
            
            if url:
                account_password.url = url

            if username:
                account_password.username = username
            
            if email:
                account_password.email = email

            if password:
                account_password.password = cipher.encrypt_data(password) # ENCRYPT THE PASSWORD BEFORE SAVING TO DB

            # SINCE CATEGORY CANNOT BE EMPTY THERE IS NO NEED TO CHECK
            account_password.category = user.categories_set.get(category_name=category) # QUERY'IN CHILD (CATEGORY) FROM PARENT (USER)

            # SAVED THE CURRENT INSTANCE OF DB
            account_password.save()
            messages.success(request, "Saved Changes")
            return redirect('vault')
        else:
            # FORM IS EMPTY
            messages.error(request, "All fields cannot be empty")

    context = {'categories': categories_of_user, 'account_password' :account_password, 'title_acronym': title_acronym}
    print(context.get('account_password'))

    return render(request, 'base/edit-password.html', context)

# EDIT USER PROFILE LOGIC
@login_required(login_url='login')
def edit_profile(request):
    user = request.user # GETS CURRENT LOGGED IN USER
    name_of_user = Name.objects.get(user=user) # GETS FULL NAME OF CURRENT USER
    error_message = "" # SENDS ERROR MESSAGE TO FRONTEND

    if request.method == 'POST':
        # GETTING FORM DATA
        name = request.POST.get('name')
        username = request.POST.get('username')
        new_password = request.POST.get('new-password')
        current_password = request.POST.get('current-password')

        # CHECK IF USER SUBMITS EMPTY FORM
        if name or username or new_password:
            # USER DIDN'T SUBMIT EMPTY FORM
            if check_password(current_password, user.password): # TO CHANGE THE DATA USER NEED TO ENTER CURRENT PASSWORD
                if name and name != name_of_user:
                    name_of_user.name = name
                if username and username != user.username:
                    try:
                        # USERNAME TO BE CHANGED IS ALREADY EXIST THROW ERROR
                        User.objects.get(username=username)
                        error_message = "Username already taken"
                    except:
                        # NEW USERNAME DO NOT EXIST IN DM
                        user.username = username
                if new_password:
                    # IF USER WANT TO CHANGE THERE CURRENT PASSWORD IT SHOULD NOT BE SAME AS PREVIOUS ONE
                    if check_password(new_password, user.password):
                        # PASSWORD IS SAME AS PREVIOUS ONE
                        error_message = "New password cannot be same as old password"
                    else:
                        user.set_password(new_password)
            else:
                # IF CURRENT PASSWORD DOESN'T MATCH NO CHANGES ARE DONE AND THROWS AN ERROR TO USER
                error_message = "Old password doesn't match"
        else:
            # USER SUBMITS AN EMPTY FORM
            error_message = "All fields cannot be empty"

        # IF THERE ARE NO ERROR MESSAGE ---> FORM SUBMITTED SUCCESSFULLY, SAVE THE CHANGES TO THE DB
        if not error_message:
            user.save() # SAVE THE CURRENT INSTANCE OF 'USER' MODEL IN DB
            name_of_user.save() # SAVE THE CURRENT INSTANCE OF 'NAME' MODEL IN DB
            messages.success(request, "Changes saved successfully")
            return redirect('vault')

    return render(request, 'base/edit-profile.html', {'error_message': error_message})

# LOGOUT USER IF USER IS LOGGED IN
@login_required(login_url='login')
def logout_user(request):
    # LOGS OUT THE USER
    if request.user.is_authenticated:
        logout(request)
    
    return redirect('home')

# DELETE CATEGORIES LOGIC
@login_required(login_url='login')
def delete_categories(request, pk):
    # SINCE BOTH DELETE ACCOUNT AND DELETE CATEGORIES USING SAME TEMPLATE THIS VARIABLE PROVIDE INFO FROM WHICH VIEW DOES THE TEMPLATE RENDER FROM
    page = 'delete-categories'
    user = request.user # GET'S CURRENT LOGGED IN USER

    # IF THE ID IN THE URL DOES NOT EXIST THEN GOES TO EXCEPT BLOCK
    try:
        user_category = user.categories_set.get(id=int(pk)) # GETS THE SELECTED CATEGORY USING CATEGORY ID
    except:
        return render('home')

    if user_category:
        # IF THE CURRENT USER IS NOT THE OWNER OF THE CATEGORY THEN REDIRECT TO VAULT PAGE
        if user.id != user_category.user.id:
            return redirect('vault')
        
        if request.method == 'POST':
            user_category.delete()
            messages.success(request, f'{user_category} Category delete successfully')
            return redirect('vault')
    
    # GET THE PREVIOUS URL AND SEND IT TO FRONTEND SO IF USER PRESS CANCEL BUTTON THEN IT CAN SEND THE USER TO THE URL FROM WHERE IT CAME FROM
    previous_url = request.META.get('HTTP_REFERER') 
    
    context = {'category': user_category, 'page': page, 'previous_url': previous_url}

    return render(request, 'base/delete.html', context)

# DELETE ACCOUNT PASSWORD LOGIC
@login_required(login_url='login')
def delete_account_password(request, pk):
    user = request.user # GETS CURRENT LOGGED IN USER
    account_password = AccountPassword.objects.get(id=int(pk)) # GETS THE ACCOUNT PASSWORD TO BE DELETED

    if request.method == 'POST':
        # IF THE USER IS NOT THE USER OF THE ACCOUNT PASWORD SENT HIM TO HIS VAULT
        if user.id != account_password.user.id:
            return redirect('vault')

        account_password.delete()
        messages.success(request, "Deleted successfully")

    return redirect('vault')

# DELETE BITPASS USER ACCOUNT LOGIC ---> ALSO DELETES ALL THEIR SAVED PASSWORD
@login_required(login_url='login')
def delete_user_account(request):
    user = request.user # GETS THE LOGGED IN USER 

    # DELETES THE CURRENT USER
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    
    # SENDS THE HTTP_REFERER TO THE FRONTEnD SO WE CAN SET THE URL OF THE BACK BUTTON THROUGH JS
    return render(request, 'base/delete.html', {'previous_url': request.META.get('HTTP_REFERER')})