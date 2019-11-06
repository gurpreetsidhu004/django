from django.urls import include, path
from django.views.generic import TemplateView


from . import views

urlpatterns = [

	path('signin', views.Sign_in, name ='signin'),
    path('logout', views.sign_out, name = 'logout'),
    path('signup', views.SignUP, name = 'signup'),
	path('upload', views.api_nlp_view, name='upload'),
	path('excel', views.excel_2_db, name='excel'),
	path("blog/posts/", views.all_post, name="posts"),
	path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
	path("blog/category/<category>/", views.blog_category, name="blog_category"),
	path("blog/tag/<tag>/", views.tag_filter, name="tag_filter_base"),
	path("Ghost/<int:pk>/", views.send_to_ghost, name="blog_ghost"),
	path('blog/get_data/', views.refresh_image, name='image_search'),
	path('', TemplateView.as_view(template_name='landing.html'), name='home'),
	path('ai_model/', views.ai_model, name="ai_model"),
    path('post/', views.book_list, name='book_list'),
    path('post/create/', views.book_create, name='book_create'),
    path('post/<int:pk>/update/', views.book_update, name='book_update'),
    path('post/<int:pk>/delete/$', views.book_delete, name='book_delete'),
	path('populate_tags_details', views.populate_tags_details, name='testing'),
	path('Ghost/all/',views.send_all_post_2_ghost, name='all_hit')

]