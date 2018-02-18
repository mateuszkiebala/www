from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/communes/', views.get_communes, name='communes'),
    url(r'^api/headers/', views.get_headers, name='headers'),
    url(r'^api/update_results/', views.update_results, name='update_results'),
    url(r'^api/row/', views.get_row, name='row'),
    url(r'^api/last_mod/', views.get_last_mod, name='last_mod'),
    url(r'^api/province_table/', views.get_province_table, name='province_table'),
    url(r'^api/commune_types_table', views.get_commune_types_table, name='commune_types_table'),
    url(r'^api/ranges_table', views.get_ranges_table, name='ranges_table'),
    url(r'^api/general_data', views.get_general_data, name='general_data'),
    url(r'^api/map_data', views.get_map_data, name='map_data'),
]
