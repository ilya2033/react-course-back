from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Category
from .serializers import CategorySerializer
import json
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAdminUser,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q


@csrf_exempt
@api_view(["GET"])
def category_list(request,):
    skip = int(request.GET.get("skip",0))
    limit = int(request.GET.get("limit",50))
    isRoot = int(request.GET.get("root",0))
    text = request.GET.get("text","")
    orderBy = request.GET.get("orderBy","_id")


    try:
        if text:
            categories = Category.objects.filter(Q(name__contains = text) ).order_by(orderBy)[skip:skip+limit]
        elif isRoot:
            categories = Category.objects.filter(parent=None).order_by(orderBy)[skip:skip+limit]
        else:
            categories  = Category.objects.all().order_by(orderBy)[skip:skip+limit]

    except Exception as e:
        return JsonResponse({"errors":[{"message":"Не вірні дані"}]}, safe=False)


    serializer = CategorySerializer(categories, many=True)

    return JsonResponse({"data":serializer.data}, safe=False)


@csrf_exempt
@api_view(["GET"])
def category_detail(request,_id):
    try:
        goods_order_by = request.GET.get("orderBy","_id")
        goods_limit = request.GET.get("limit",20)
        goods_skip = request.GET.get("skip",0)
    except:
        return JsonResponse({"errors":[{"message":"Невірні параметри запиту"}]}, safe=False)
    try:
        category  = Category.objects.get(_id = _id)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Категорию не знайдено"}]}, safe=False)

    if category:
        serializer = CategorySerializer(category,context = {"goods_order_by":goods_order_by,"goods_limit":goods_limit,"goods_skip":goods_skip})
        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)




@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAdminUser, ))
@authentication_classes([JWTAuthentication])
def category_upsert(request):
    try:
        _id = request.POST.get('_id',None)
        name = request.POST.get("name", "")
        subcategories =  json.loads(request.POST.get("subcategories", "[]"))
        parent = request.POST.get("parent", None)
        goods = json.loads(request.POST.get("goods","[]"))
    except:
        return JsonResponse({"errors":[{"message":"Не вірні дані"}]}, safe=False)
    if _id :
        try:
            category = Category.objects.get(_id = _id)
        except Exception as e:
            return JsonResponse({"errors":[{"message":"Не вірні дані"}]}, safe=False)

        category.name = name

    else:
        category = Category.objects.create(name=name)

    if parent:
        print(parent)
        category.parent = Category.objects.get(_id=json.loads(parent)["_id"])

    category.goods.clear()
    for good in goods:
        category.goods.add(good["_id"])

    category.subcategories.clear()
    for subcategory in subcategories:
        try:
            category.subcategories.add(Category.objects.get(_id = subcategory["_id"]))
        except:
            return JsonResponse({"errors":[{"message":"Батькову категорію не знайдено"}]}, safe=False)
    if category:
        category.save()
        serializer = CategorySerializer(category)
        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)



@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAdminUser, ))
def category_delete(request,_id):

    try:
        category  = Category.objects.get(_id = _id)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Категорію не знайдено"}]}, safe=False)

    if category:
        category.delete()
        return JsonResponse({"data":{"_id":_id}}, safe=False)

    return JsonResponse({"data":{}}, safe=False)








