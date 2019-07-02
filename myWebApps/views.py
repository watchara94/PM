from django.shortcuts import render,redirect
from django.http import HttpResponse ,HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from api.models import UserPoints, UserLog, Package

def home(request):
    if request.user.is_authenticated:
        if request.user.username == "adminlibrary":
            return HttpResponseRedirect(reverse('myWeb:adminlibrary'))
        elif request.user.username == "adminstudentloan":
            return HttpResponseRedirect(reverse('myWeb:adminstudentloan'))
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('myWeb:adminHome'))
        else:
            user = User.objects.get(username=request.user.username)
            try:
                thisUser = UserPoints.objects.get(user=user.id)
                userlog = UserLog.objects.filter(user=user.id)
                points = thisUser.points
                log = []
                for data in userlog:
                    if(data.package_id!="-"):
                        thisPackage = Package.objects.get(package_id=data.package_id)
                        temp_data = {"id":data.id,
                                    "datetime":data.datetime,
                                    "package_id":data.package_id,
                                    "name":thisPackage.name,
                                    "points":thisPackage.points,
                                    "InEx":data.InEx}
                        log.append(temp_data)
                    else:
                        temp_data = {"id":data.id,
                                    "datetime":data.datetime,
                                    "package_id":"-",
                                    "name":"-",
                                    "points":data.points,
                                    "InEx":data.InEx}
                        log.append(temp_data)
            except:
                return render(request, 'home.html',{'points':points, 'log':log})
            else:
                return render(request, 'home.html',{'points':points, 'log':log})
                # return HttpResponseRedirect(reverse('myWeb:login'))
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def adminHome_package(request):
    if request.user.is_superuser:
        list_package = Package.objects.all()
        return render(request, 'adminHome.html',{'list_package':list_package,'package':True })
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def adminHome(request):
    if request.user.is_superuser:
        list_user = User.objects.filter(is_superuser=False).exclude(username="adminlibrary").exclude(username="adminstudentloan")
        return render(request, 'adminHome.html',{'list_user':list_user,'package':False })
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('myWeb:home'))
    else:
        return render(request, 'login.html')
        
def authenUser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('/')
    else:
        return render(request,'login.html',{'err': "Error, username or password is not correct"})

def logout(request):
    auth_logout(request)
    return render(request,'login.html',{'err': "Log Out Complete!"})

def changepass(request):
    if request.user.is_authenticated:
        return render(request,'changepass.html')
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def passChanged(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if check_password(request.POST['Opassword'], user.password):
        if(request.POST['Npassword']==request.POST['Cpassword']):
            user.set_password(request.POST['Npassword'])
            user.save()
            user = authenticate(request, username=username, password=request.POST['Npassword'])
            auth_login(request, user)
            return HttpResponseRedirect(reverse('myWeb:home'))
        else:
            return render(request,'changepass.html',{'err':"Confirmed password does not match."})
    else:
        return render(request,'changepass.html',{'err':"Old password incorrect."})

def userPage(request,user_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = User.objects.get(id=user_id)
            thisUser = UserPoints.objects.get(user=user_id)
            userlog = UserLog.objects.filter(user=user_id)
            points = thisUser.points
            log = []
            for data in userlog:
                if(data.package_id!="-"):
                    thisPackage = Package.objects.get(package_id=data.package_id)
                    temp_data = {"id":data.id,
                                "datetime":data.datetime,
                                "package_id":data.package_id,
                                "name":thisPackage.name,
                                "points":thisPackage.points,
                                "InEx":data.InEx}
                    log.append(temp_data)
                else:
                    temp_data = {"id":data.id,
                                "datetime":data.datetime,
                                "package_id":"-",
                                "name":"-",
                                "points":data.points,
                                "InEx":data.InEx}
                    log.append(temp_data)
            return render(request,'userPage.html',{'points':points,'username':user.username, 'log':log,'user_id':user_id})
        else:
            return HttpResponseRedirect(reverse('myWeb:home'))
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def package_action(request,package_id):
    if request.user.is_superuser:
        try:
            if(request.POST['save']):
                thisPackage = Package.objects.get(package_id=package_id)
                thisPackage.package_id = request.POST['package_id']
                thisPackage.name = request.POST['name']
                thisPackage.type = request.POST['type']
                thisPackage.points = request.POST['points']
                thisPackage.material = request.POST['material']
                thisPackage.save()
            else:
                Package.objects.get(package_id=package_id).delete()
        except:
            Package.objects.get(package_id=package_id).delete()
        return HttpResponseRedirect(reverse('myWeb:home_package'))
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def new_package(request):
    if request.user.is_superuser:

            try:
                Package.objects.create(package_id=request.POST['package_id'],
                                        name=request.POST['name'],
                                        type=request.POST['type'],
                                        material=request.POST['material'],
                                        points=request.POST['points'])
            except:
                return render(request,'adminHome.html',{'err':"Please Fill All Data."})
            else:
                return HttpResponseRedirect(reverse('myWeb:home_package'))
    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def delete_log(request,id):
    if request.user.is_superuser:
        username = UserLog.objects.get(id=id).user
        thisUser = User.objects.get(username=username)
        thisUserPoint = UserPoints.objects.get(user=thisUser.id)
        if(UserLog.objects.get(id=id).InEx == "Income"):
            delete_points = Package.objects.get(package_id=UserLog.objects.get(id=id).package_id).points
            thisUserPoint.points = thisUserPoint.points-delete_points
            thisUserPoint.save()
        else:
            delete_points = UserLog.objects.get(id=id).points
            thisUserPoint.points = thisUserPoint.points+delete_points
            thisUserPoint.save()
        UserLog.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse('myWeb:userPage', args=(),
                                    kwargs={'user_id': thisUser.id}))

    else:
        return HttpResponseRedirect(reverse('myWeb:login'))

def expense(request,user_id):
    if request.user.is_superuser:
        thisUserPoints = UserPoints.objects.get(user=user_id)
        if(thisUserPoints.points>=int(request.POST["ex_points"])):
            thisUserPoints.points=thisUserPoints.points - int(request.POST['ex_points'])
            thisUserPoints.save()
            thisUser = User.objects.get(id=user_id)
            UserLog.objects.create(user=thisUser,InEx="Expense",points=int(request.POST["ex_points"]))
            return HttpResponseRedirect(reverse('myWeb:userPage', args=(),
                                                kwargs={'user_id': user_id}))
        else:
            user = User.objects.get(id=user_id)
            thisUser = UserPoints.objects.get(user=user_id)
            userlog = UserLog.objects.filter(user=user_id)
            points = thisUser.points
            log = []
            for data in userlog:
                if(data.package_id!="-"):
                    thisPackage = Package.objects.get(package_id=data.package_id)
                    temp_data = {"id":data.id,
                                "datetime":data.datetime,
                                "package_id":data.package_id,
                                "name":thisPackage.name,
                                "points":thisPackage.points,
                                "InEx":data.InEx}
                    log.append(temp_data)
                else:
                    temp_data = {"id":data.id,
                                "datetime":data.datetime,
                                "package_id":"-",
                                "name":"-",
                                "points":data.points,
                                "InEx":data.InEx}
                    log.append(temp_data)
            return render(request,'userPage.html',{'points':points,'username':user.username, 'log':log,'user_id':user_id,"err":"Expense exceeds certain points"})

    else:
        return HttpResponseRedirect(reverse('myWeb:home'))

def adminchangepass(request,user_id):
    if request.user.is_superuser:
        user = User.objects.get(id=user_id).username
        print(user)
        return render(request,'changepass.html',{'users':user,'user_id':user_id})
    else:
        return HttpResponseRedirect(reverse('myWeb:home'))

def adminpassChanged(request,user_id):
    if request.user.is_superuser: 
        user = User.objects.get(id=user_id)
        username = user.username
        if(request.POST['Npassword']==request.POST['Cpassword']):
            user.set_password(request.POST['Npassword'])
            user.save()
            return HttpResponseRedirect(reverse('myWeb:home'))
        else:
            return render(request,'changepass.html',{'err':"Confirmed password does not match.","users":username,"user_id":user_id})
    else:
        return HttpResponseRedirect(reverse('myWeb:home'))

def adminlibrary(request):
    # return HttpResponseRedirect(reverse('myWeb:logout'))
    if request.user.username == "adminlibrary":
        list_all_user = User.objects.exclude(username="adminlibrary").exclude(username="adminstudentloan").filter(is_superuser=False)
        return render(request,'homelibrary.html',{"list_all_user":list_all_user})
    else:
        return HttpResponseRedirect(reverse('myWeb:home'))

def libraryuserPage(request,user_id):
    if request.user.username == "adminlibrary":
        user = User.objects.get(id=user_id)
        points = UserPoints.objects.get(user=user).points
        username = user.username
        return render(request,'pointcheck.html',{"user_id":user_id,'username':username,'points':points})
    else:
        return HttpResponseRedirect(reverse('myWeb:home'))

def libraryexpense(request,user_id):
    if request.user.username == "adminlibrary":
        thisUserPoints = UserPoints.objects.get(user=user_id)
        if(thisUserPoints.points>=int(request.POST["ex_points"])):
            thisUserPoints.points=thisUserPoints.points - int(request.POST['ex_points'])
            thisUserPoints.save()
            thisUser = User.objects.get(id=user_id)
            UserLog.objects.create(user=thisUser,InEx="Expense",points=int(request.POST["ex_points"]))
            return HttpResponseRedirect(reverse('myWeb:libraryuserPage', args=(),
                                                kwargs={'user_id': user_id}))
    else:
        return HttpResponseRedirect(reverse('myWeb:home'))

def adminstudentloan(request):
    # return HttpResponseRedirect(reverse('myWeb:logout'))
    if request.user.username == "adminstudentloan":
        list_all_user = User.objects.exclude(username="adminlibrary").exclude(username="adminstudentloan").filter(is_superuser=False)
        return render(request,'e-Studentloan.html',{"list_all_user":list_all_user})
    else:
        return HttpResponseRedirect(reverse('myWeb:home'))
    
def studentloanuserPage(request,user_id):
    if request.user.username == "adminstudentloan":
        user = User.objects.get(id=user_id)
        print(user)
        username = user.username
        thisUser = UserPoints.objects.get(user=user_id)#เอามาแค่ user_id
        userlog = UserLog.objects.filter(user=user_id)#เอามาทั้งออปเจค
        points = thisUser.points
        log = []
        for data in userlog:
            if(data.package_id!="-"):
                thisPackage = Package.objects.get(package_id=data.package_id)
                temp_data = {"id":data.id,
                            "datetime":data.datetime,
                            "package_id":data.package_id,
                            "name":thisPackage.name,
                            "points":thisPackage.points,
                            "InEx":data.InEx}
                log.append(temp_data)
            else:
                temp_data = {"id":data.id,
                            "datetime":data.datetime,
                            "package_id":"-",
                            "name":"-",
                            "points":data.points,
                            "InEx":data.InEx}
                log.append(temp_data)
        return render(request,'usercheck.html',{'log':log,'points':points,"user_id":user_id,'username':username})
    else:
        return HttpResponseRedirect(reverse("myWeb:home"))
    
def searchuser(request):
    userget = request.POST['studentid']
    list_all_user = User.objects.exclude(username="adminlibrary").exclude(username="adminstudentloan").filter(is_superuser=False).filter(username__contains= userget)
    return render(request,'e-Studentloan.html',{"list_all_user":list_all_user})

def searchpoint(request):
    userget = request.POST['studentid']
    list_all_user = User.objects.exclude(username="adminlibrary").exclude(username="adminstudentloan").filter(is_superuser=False).filter(username__contains= userget)
    return render(request,'homelibrary.html',{"list_all_user":list_all_user})


