from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserPoints,UserLog,Package

import json

from django.utils import timezone

max_id = 8000000000000
min_id = 5000000000000
# Create your views here.
class get_userdata(APIView):
    def get(self,request):
        print("000000000000")
        username = int(self.request.query_params.get('id'))
        if (username<=max_id and username>=min_id):
            try:
                print("11111111111")
                user = User.objects.get(username=username)
            except:
                print("2222222222")
                newUser = User.objects.create_user(username=username,password="password")
                thisUser = UserPoints.objects.create(user=newUser)
                data = {"id":username,
                        "verify":True,
                        "point(s)":thisUser.points}
            else:
                print("----------")
                print(user.id)
                thisUser = UserPoints.objects.get(user=user.id)
                data = {"id":username,
                        "verify":True,
                        "point(s)":thisUser.points}
        else:
            data = {"id":username,
                    "verify":False,
                    "error":"Invalid Id"}
        return Response(data)

class update_data(APIView):
    def post(self,request):
        print(timezone.now())
        # body = id , points, type, weight
        print("88888888888888888")
        print(request.data['id'])
        getUser = User.objects.get(username=request.data['id'])
        try:
            getPackage = Package.objects.get(package_id=request.data['package_id'])
        except:
            data = {"error": "Sorry, No Data For This Package."}
        else:
            # print(getUser)
            thisUser = UserPoints.objects.get(user=getUser)
            thisUser.points+=getPackage.points
            points = thisUser.points
            thisUser.save()
            UserLog.objects.create(user=getUser,
                                    package_id=getPackage.package_id,
                                    points=getPackage.points)
            return Response({"points":points,"package_points":getPackage.points})

class no_id(APIView):
    def get(self,request):
        waste_id = int(self.request.query_params.get('id'))
        try:
            thisPackage = Package.objects.get(package_id=waste_id)
        except:
            return Response({"have":False})
        else:
            return Response({"have":True,"material":thisPackage.material})
