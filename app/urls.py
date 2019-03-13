from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^market/$',views.market,name='market'),
    url(r'^market/(?P<childid>\d+)/(?P<sortid>\d+)/$', views.market, name='market'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^mine/$',views.mine,name='mine'),
    # url(r'^base/$',views.base,name='base'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^checkusername/$',views.checkusername,name='checkusername'),
    url(r'^addcart/$',views.addcart,name='addcart'),
    url(r'^subcart/$',views.subcart,name='subcart'),
    url(r'^makeorder/$',views.makeorder,name='makeorder'),
    url(r'^changecartselect/$',views.changecartselect,name='changecartselect'),
    url(r'^changeall/$',views.changeall,name='changeall'),
    url(r'^orderlist/$',views.orderlist,name='orderlist'),
    url(r'^orderdetail/(?P<identifier>[\d.]+)/$',views.orderdetail,name='orderdetail')

]