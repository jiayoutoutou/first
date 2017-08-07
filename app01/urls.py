from django.conf.urls import url

from app01 import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^login.html', views.login),

    url(r'^teacher.html', views.teacher),
    url(r'^model_modify/', views.model_modify),
    url(r'^model_message/', views.model_message),

    url(r'^search_class/', views.search_class),
    url(r'^add_class/', views.add_class),
    url(r'^del_class/', views.del_class),
    url(r'^edite_class/', views.edite_class),

    url(r'^student/', views.student),
    url(r'^model_modify_student/', views.model_modify_student),

]
