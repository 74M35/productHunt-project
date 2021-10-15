from django.shortcuts import redirect, render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
import re

def signup(request):
    if request.method == 'POST':
        #user wants to sign up
        #get password from form
        pswd = request.POST['password1']
        #get username from form
        username = request.POST['username']
        #username must begin and end with alphanumeric characters, and can only contain alphanumeric and -_.
        username_reg = "^[A-Za-z0-9]+[0-9A-Za-z-_.]*[A-Za-z0-9]$"
        #find if username begins with - _ or .
        usernamestart_reg = "^(?![._-]).+"
        #find if ends with - _ or .
        usernameend_reg = "[A-Za-z0-9]$"
        #Minimum six characters, at least one uppercase letter, one lowercase letter, one number and one special character (@$!%*?&)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        #doesn't contain only a-z A-Z 0-9 or ^@$!%*?&
        invalid_reg = "(?=[^a-z])(?=[^A-Z])(?=[^0-9])(?=[^@$!%*?&])"
        #doesn't contain numbers
        nonum_reg = "^(?!.*[0-9])"
        #doesn't contain capital letters
        nocap_reg = "^(?!.*[A-Z])"
        #doesnt contain lowercase letters
        nolow_reg = "^(?!.*[a-z])"
        #doesnt contain special characters
        nospec_reg = "^(?!.*[@$!%*?&])"
        match_re = re.compile(reg)
        #check if username is valid
        username_res = re.search(username_reg, username)
        #check if username begins with -. or _
        startuser_res = re.search(usernamestart_reg, username)
        #check if username begins with - _ or .
        enduser_res = re.search(usernameend_reg, pswd)
        #check if password is valid
        res = re.search(match_re, pswd)
        #check if password contains invalid characters
        invalid_res = re.search(invalid_reg, pswd)
        #check if password doesnt contain numbers
        nonum_res = re.search(nonum_reg, pswd)
        #check if password doesnt contain capital letters
        nocap_res = re.search(nocap_reg, pswd)
        #check if password doesnt contain lowercase letters
        nolow_res = re.search(nolow_reg, pswd)
        #check if password doesnt contain special characters
        nospec_res = re.search(nospec_reg, pswd)
        #if passwords match, check username is valid
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            #if the username section is blank or less than 2 characters, throw error
            if len(username) < 1:
                return render(request, 'accounts/signup.html', {'error':'No username entered'})
            elif len(username) < 2:
                return render(request, 'accounts/signup.html', {'error':'Username must be at least 2 characters long'})
            #if the username is not valid
            elif not username_res:
                #if username begins with -. or _
                if not startuser_res:
                    #remove alphanumeric characters
                    invalid_user = re.sub(r"[A-Za-z\d]", "", username)
                    #only show 1st character in string to show which is beginning of whole username string
                    invalid_user = invalid_user[0]
                    return render(request, 'accounts/signup.html', {'error':'Cannot have the username: '+username+' \n Username cannot begin with character: ' + invalid_user})
                elif not enduser_res:
                    #remove alphanumeric characters
                    invalid_user = re.sub(r"[A-Za-z\d]", "", username)
                    #only show 1st character in string to show which is end of whole username string
                    invalid_user = invalid_user[-0]
                    return render(request, 'accounts/signup.html', {'error':'Cannot have the username: '+username+' \n Username cannot end with character: ' + invalid_user})
                else:
                    #remove valid characters to show user what they entered was invalid
                    invalid_user = re.sub(r"[A-Za-z\d_.-]", "", username)
                    #remove duplicate invalid characters
                    removeDup = "".join(dict.fromkeys(invalid_user))
                    #if there is more than 1 invalid character after removing duplicates tell them invalid characters
                    if len(removeDup) > 1:
                        return render(request, 'accounts/signup.html', {'error':'Cannot have the username: '+username+' \n Username cannot contain characters: ' + removeDup})
                    #we can assume if there is less than 1 and there was an invalid character inputted by the user then there is 1 invalid character
                    else:
                        return render(request, 'accounts/signup.html', {'error':'Cannot have the username: '+username+' \n Username cannot contain character: ' + removeDup})
            else:
                #if the username is taken, throw error
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup.html', {'error':'Username is unavailable'})
                #if username exists check if password is valid
                except User.DoesNotExist:
                    #if password is valid, create user and return home
                    if res:
                        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                        auth.login(request, user)
                        return redirect('home')
                    #if password is invalid, check where the error is
                    if not res:
                        #if password is shorter than 6 characters, throw error
                        if len(pswd) < 6:
                            return render(request, 'accounts/signup.html', {'error':'Password needs to be at least 6 characters'})
                        #if password has invalid characters, check which characters are invalid
                        elif invalid_res:
                            invalid_char = re.sub(r"[A-Za-z\d@$!%*?&]", "", pswd)
                            removeDup = "".join(dict.fromkeys(invalid_char))
                            whitespace = re.compile("[\s]")
                            whitespace_res = re.search(whitespace, removeDup)
                            whitespace_rem_dup = re.sub(r"[\s]", "", removeDup)
                            #if password has 1 invalid character after removing duplicates, and invalid characters have a whitespace, it must be a space. so tell user they cannot have spaces
                            if len(removeDup) == 1 and whitespace_res:
                                return render(request, 'accounts/signup.html', {'error':'Password must not contain spaces'})
                            #if password has more than 1 invalid character after removing duplicates, and has a whitespace. there must be a space and at least 1 invalid character
                            elif len(removeDup) > 1 and whitespace_res:
                                #if there is more than 1 invalid character after removing the whitespace from the invalid characters list, tell the user they cannot use spaces and which characters are invalid
                                if len(whitespace_rem_dup) > 1:
                                    return render(request, 'accounts/signup.html', {'error':'Password must not contain spaces or characters: '+ whitespace_rem_dup})
                                #if there is not more than 1 invalid character after removing the whitespace. Tell the user they cannot use spaces and which character is invalid
                                #there will be at least 1 invalid character other than a space as a previous if statement checked to see if it was ONLY whitespaces which were invalid
                                else:
                                    return render(request, 'accounts/signup.html', {'error':'Password must not contain spaces or character: '+ whitespace_rem_dup})
                            #if there is more than 1 invalid character and no whitespace, tell the user which characters are invalid
                            #there wont be any spaces as a previous if statement checked to see if there were invalid characters AND whitespaces               
                            elif len(whitespace_rem_dup) > 1:
                                return render(request, 'accounts/signup.html', {'error':'Password must not contain characters: ' + whitespace_rem_dup})
                            #if the password still includes invalid characters, we can assume there is only 1 invalid character as the rest of the if statements would have sifted through. so tell the use which character is invalid
                            else:
                                return render(request, 'accounts/signup.html', {'error':'Password must not contain character: ' + whitespace_rem_dup})
                        #if password doesn't contain a number, tell user
                        elif nonum_res:
                            return render(request, 'accounts/signup.html', {'error':'Password must contain a number'})
                        #if password doesn't contain a capital letter, tell user
                        elif nocap_res:
                            return render(request, 'accounts/signup.html', {'error':'Password must contain a capital letter'})
                        #if password doesn't contain a lowercase letter, tell user
                        elif nolow_res:
                            return render(request, 'accounts/signup.html', {'error':'Password must contain a lowercase letter'})
                        #if password doesn't contain a special character, tell user
                        elif nospec_res:
                            return render(request, 'accounts/signup.html', {'error':'Password must contain a special character'})
                        else:
                            return render(request, 'accounts/signup.html', {'error':'Invalid password'})
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords must match'})
    else:
        #user wants to enter info
        return render(request, 'accounts/signup.html')

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    # change to homepage
    return render(request, 'accounts/signup.html')