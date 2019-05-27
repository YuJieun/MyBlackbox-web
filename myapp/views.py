from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from myapp.models import VideoTable, InfoTable
import requests
from math import *

@login_required
def index(request):
    videos = VideoTable.objects.filter(username=request.user.username)

    context = {
        'tag':0,    #0이면 사용자의 전체비디오(메인화면) 1이면 그 중 검색결과
        'videos': videos
    }
    print(videos)
    print(request.user.username)
    return render(request, 'layout/main.html', context)

def detail(request,videoid, date, object, color, direction, weather, lati, longi):
    # list =[]
    if request.method == 'POST':
        list = request.POST.get('data')
        print(list)


    infos = InfoTable.objects.filter(videoid=videoid)
    video = VideoTable.objects.get(id=videoid)
    videopath = video.path[26:]
    t_date = video.path[41:-11]
    hour = video.path[48:50]
    minute = video.path[50:52]
    second = video.path[52:54]

    total_second = int(second) + 60*int(minute) + 3600*int(hour)
    filter_arr=[object, direction, weather,  color]

    for info in infos:
        lat = info.latitude
        lon = info.longitude
        url = 'https://dapi.kakao.com/v2/local/geo/coord2address.json?x='+str(lon)+'&y='+str(lat)
        headers = {'Authorization': 'KakaoAK 3c99460ffccf7879bc9718eee123a66d'}
        result = json.loads(str(requests.get(url, headers=headers).text))
        print(result)
        match_first = result['documents'][0]['road_address']['address_name']
        info.location = match_first
        print(info.location)

        info_arr = [info.object, info.direction, info.weather, info.color]

        i=-1
        ch=-1
        info.match = 0
        for tmp in filter_arr:
            i+=1
            # if i == 3 and ch != 3:
            if i == 3:
                if tmp == "default":
                    if ch !=2:
                        info.match = 1
                    elif ch==2:
                        info.match = 0
                elif tmp == "black":
                    if info.color == "Black":
                        info.match = 1
                elif tmp == "greenblue":
                    if info.color == "Green":
                        info.match = 1
                    if "Blue" in info.color:
                        info.color = "Blue"
                        info.match = 1
                elif tmp == "browngold":
                    if info.color == "Brown" or info.color == "Gold":
                        info.match = 1
                elif color == "purplered":
                    if info.color == "Purple" or info.color == "Red":
                        info.match = 1
                elif color == "silverwhite":
                    if info.color == "Silver":
                        info.match = 1
                    if "White" in info.color:
                        info.color = "White"
                        info.match = 1

            elif tmp == "default":
                ch += 1
            elif tmp != info_arr[i]:
                break

        if lati == "default" and longi == "default":
            pass
        else:
            for info in infos:
                lat = info.latitude
                lon = info.longitude

                if (6371 * acos(cos(radians(float(lati))) * cos(radians(lat)) * cos(radians(lon)- radians(float(longi))) + sin(radians(float(lati))) * sin(radians(lat)))) <= 0.3:
                    info.match = 1
                else:
                    info.match = 0




    for info in infos:
        print(info.frame)
    context = {
        'date': t_date,
        'hour': hour,
        'minute': minute,
        'second': second,
        'total_second': total_second,
        'infos': infos,
        'video': video,
        'videopath': videopath
    }

    return render(request,'layout/detail.html', context)


def search(request,date,object,color,direction,weather,lati,longi):
    if date == "date":
        videos = VideoTable.objects.filter(username=request.user.username)
    else:
        videos = VideoTable.objects.filter(username=request.user.username, path__contains=date)
    infos = InfoTable.objects.filter(videoid__in=videos)

    if lati != "default":
        infoGPS = InfoTable.objects.raw('''SELECT *,
                                (6371*acos(cos(radians(''' + lati + '))*cos(radians(latitude))*cos(radians(longitude)' +
                                    '-radians(' + longi + '))+sin(radians(' + lati + '''))*sin(radians(latitude))))
                                AS distance
                                FROM infos
                                HAVING distance <= 0.3
                                ORDER BY distance
                                LIMIT 0,300''')
        # infos = infos.filter(videoid__in=videos)
        ids =[]
        for info in infoGPS:
            if info.videoid not in ids:
                ids.append(info.videoid)
        infos = infos.filter(videoid__in=ids)

    if object != "default":
        infos = infos.filter(object=object)

    if color != "default":
        if color == "greenblue":
            infos = infos.filter(color__in=["Green", "Blue"])
        elif color == "black":
            infos = infos.filter(color="Black")
        elif color == "browngold":
            infos = infos.filter(color__in=["Brown", "Gold"])
        elif color == "purplered":
            infos = infos.filter(color__in=["Purple", "Red"])
        elif color == "silverwhite":
            infos = infos.filter(color__in=["Silver", "White"])

    if direction != "default":
        if direction == "left":
            infos = infos.filter(direction__contains=direction)
        if direction == "right":
            infos = infos.filter(direction__contains=direction)
        if direction == "front":
            infos = infos.filter(direction=direction)

    if weather != "default":
        if weather == "Clear":
            infos = infos.filter(weather__in=["Clear"])
        elif weather == "Clouds":
            infos = infos.filter(weather__in=["Mist", "Haze", "Clouds", "Dust", "Fog"])
        elif weather == "Rain":
            infos = infos.filter(weather__in=["Rain", "Squall"])
        elif weather == "Snow":
            infos = infos.filter(weather__in=["Snow"])
        elif weather == "Thunderstorm":
            infos = infos.filter(weather__in=["Thunderstorm"])

    # [{1:[1,2,3]},{5:[1,3,4]}]
    # test = {}
    # tests = []
    # tests.append(test)
    #
    ids=[]
    # i_ids={}
    # # videoByInfo = [{1'':[in.id, info2], '2':[]}]
    # testnum = -1
    for info in infos:
        print(info.color)
        if info.videoid not in ids:
    #         tests.append({info.videoid:[info.]})
            ids.append(info.videoid)
    #         testnum += 1
    #     else
    #
    #         # i_ids[info]
    #         # tests[]




    pathvideo = VideoTable.objects.filter(id__in=ids)

    #infos.videoid == video.id
    # pathvideo = VideoTable.objects.extra(tables=['infos'], where=[]).all()
    # print(len(pathvideo))

    #infos = InfoTable.objects.filter(videoid__in=videos, color=color, location=location, object=object)

    # info1 = {'videoid': 1, 'object':'car1', 'score':70}
    # info2 = {'videoid': 2, 'object':'car2', 'score':80}
    # info3 = {'videoid': 3, 'object':'car3', 'score':90}
    # tests[0] = [info1, info2, info3]
    # test[0].append(info1)
    # test[0].append(info2)
    # test[0].append(info3)
    # test[1] = [info1, info1, info1]
    # test[2] = [info2, info2, info2]

    context = {
        'tag': 1,
        'ids': zip(ids,pathvideo),
        'date': date,
        'object': object,
        'color': color,
        'direction': direction,
        'weather': weather,
        'lati': lati,
        'longi': longi,
        'infos': infos,
        # 'pathvideo': pathvideo #받을때 pathvideo.path로..
    }
    return render(request, 'layout/main.html', context)

@csrf_exempt
def androidRegister(request):
    content = json.loads(request.body.decode("utf-8"))
    if User.objects.filter(username=content["u_id"]).exists():
        return HttpResponse('register fail')
    user = User.objects.create_user(username=content["u_id"], email=None, password=content["u_pw"])
    if user is None:
        return HttpResponse('register fail')
    return HttpResponse('register success')

@csrf_exempt
def androidLogin(request):
    content = json.loads(request.body.decode("utf-8"))
    user_id = content["u_id"]
    user_pwd = content["u_pw"]
    if User.objects.filter(username=user_id).exists():
        user = authenticate(username=user_id, password=user_pwd)
        if user is not None:
            return HttpResponse('1') #success
        else:
            return HttpResponse('2') #wrong password
    else:
        return HttpResponse('3') #id not exist
    return HttpResponse("4")

def userLogin(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    elif request.method == 'POST':
        print(request)
        user = authenticate(username=request.POST.get('user_id'), password=request.POST.get('user_pw'))
        print(request.POST.get('user_id'))
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/join/')

def userLogout(request):
    logout(request)
    return redirect('/userLogin')
