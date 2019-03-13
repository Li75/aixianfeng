import hashlib
import random
import time

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.core.cache import cache

from app.models import Wheel, Nav, Mustbuy, Shop, Foodtype, Goods, User, Cart, Order, OrderGoods


def home(request):
    wheels = Wheel.objects.all()

    navs = Nav.objects.all()

    mustbuys = Mustbuy.objects.all()

    shops = Shop.objects.all()
    shophead = shops[0]
    shoptabs = shops[1:3]
    shopclass_list = shops[3:7]
    shopcommends = shops[7:11]

    response_dir = {
        'wheels': wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptabs':shoptabs,
        'shopclass_list':shopclass_list,
        'shopcommends':shopcommends,
    }
    return render(request, 'home/home.html', context=response_dir)


def market(request, childid='0', sortid='0'):

    foodtypes = Foodtype.objects.all()
    # 商品信息
    # goods_list = Goods.objects.all()[0:5]
    # 默认打开页面  热销榜
    # 点击左侧分类，即显示对应分类 商品信息  【传参数categoryid】
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    # 客户端 需要记录 点击的分类下标 【cookies， 会自动携带】
    index = int(request.COOKIES.get('index', '0'))
    # 根据index 获取 对应的 分类ID
    categoryid = foodtypes[index].typeid
    # 根据 分类ID 获取对应分类信息
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    # 子类
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    # 排序
    # 0默认综合排序   1销量排序     2价格最低   3价格最高
    if sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')

    # 获取子类信息
    childtypenames = foodtypes[index].childtypenames
    # 存储子类信息 列表
    childtype_list = []
    # 将对应的子类拆分出来
    for item in childtypenames.split('#'):
        # item   全部分类:0
        # item   子类名称: 子类ID
        item_arr = item.split(':')
        temp_dir = {
            'name': item_arr[0],
            'id': item_arr[1]
        }

        childtype_list.append(temp_dir)

    response_dir = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'childtype_list': childtype_list,
        'childid': childid
    }
    print(response_dir)
    return render(request,'market/market.html', context=response_dir)



def cart(request):
    return render(request, 'cart/cart.html')



def mine(request):
    # 获取
    token = request.session.get('token')
    userid = cache.get(token)
    user = None
    if userid:
        user = User.objects.get(pk=userid)

    return render(request, 'mine/mine.html', context={'user':user})




def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def generate_token():
    temp = str(time.time()) + str(random.random())
    md5 = hashlib.md5()
    md5.update(temp.encode('utf-8'))
    return md5.hexdigest()



def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':

        username = request.POST.get('username')
        password = generate_password(request.POST.get('password'))
        phone = request.POST.get('phone')

        user = User()
        user.username = username
        user.password = password
        user.phone = phone
        user.save()
        # 状态保持
        token = generate_token()
        cache.set(token, user.id, 60*60*24*3)
        request.session['token'] = token

        return redirect('app:mine')


def login(request):
    if request.method == 'GET':
        return render(request,'mine/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        back = request.COOKIES.get('back')
        users = User.objects.filter(username=username)
        if users.exists():#同户存在
            user = users.first()
            if user.password == generate_password(password):
                token = generate_token()
                cache.set(token, user.id, 60 * 60 * 24 * 3)
                request.session['token'] = token

                if back == 'mine':
                    return redirect('app:mine')
                else:
                    return redirect('app:cart')
            else:
                return render(request,'mine/login.html',context={'pwd_err':'密码错误!'})
        else:
            return render(request,'mine/login.html',context={'user_err':'用户不存在!'})



def logout(request,):
    request.session.flush()
    return redirect('app:mine')


def checkusername(request):
    username = request.GET.get('username')
    users = User.objects.filter(username=username)
    if users.exists():
        response_data = {
            'status': 1,
            'msg': '账号可以使用!'
        }
    else:
        response_data = {
            'status': 0,
            'msg': '账号不可以使用!'
        }
    return JsonResponse(response_data)


def addcart(request):
    token = request.session.get('token')
    response_data = {}

    if token:
        userid = cache.get(token)
        if userid:
            user = User.objects.get(pk=userid)
            goodsid =request.GET.get('goodsid')
            goods = Goods.objects.get(pk=goodsid)

            carts = Cart.objects.filter(user=user).filter(goods=goods)
            if carts.exists():
                cart = carts.first()
                cart.number = cart.number + 1
                cart.save()
            else:
                cart = Cart()
                cart.user = user
                cart.goods = goods
                cart.number = 1
                cart.save()

            response_data['status'] = 1
            response_data['number'] = cart.number
            response_data['msg'] = '添加{}购物车成功:{}'.format(cart.goods.productlongname,cart.number)
            return JsonResponse(response_data)


def subcart(request):
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number -1
    cart.save()

    response_data = {
        'msg':'删除商品成功!',
        'status':1,
        'number':cart.number
    }
    return JsonResponse(response_data)


def generate_identifier():
    temp = str(time.time()) + str(random.random())
    return temp


def makeorder(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    order = Order()
    order.user = user
    order.identifier = generate_identifier()    #生成订单号
    order.save()

    carts = user.cart_set.filter(isdelete=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = carts.goods
        orderGoods.number = carts.number
        orderGoods.save()
        #生成订单商品移除购物车
        cart.delete()
    return render(request,'order/orderdetail.html',context={'order':order})


def changecartselect(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    response_data = {
        'msg':'状态修改成功!',
        'status':1,
        'isselect':cart.isselect
    }
    return JsonResponse(response_data)


def changeall(request):
    isall = request.GET.get('isall')

    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)
    carts = user.cart_set.all()

    if isall == 'true':
        isall = True
    else:
        isall = False

    for cart in carts:
        cart.isselect = isall
        cart.save()

    response_data = {
        'msg':'全选/取消全选  成功',
        'status':1
    }
    return JsonResponse(response_data)


def orderlist(request):
    token = request.GET.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    order = user.order_set.all()
    return render(request,'order/orderlist.html',context={'order':order})


def orderdetail(request,identifier):
    order = Order.objects.filter(identifier=identifier).first()
    return render(request,'order/orderdetail.html',context={'order':order})