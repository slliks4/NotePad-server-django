from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView


from .import views

urlpatterns = [
    path('', views.Endpoints),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

    path('create_user/', views.Create_user, name='create_user'),
    path('user_detail/', views.User_detail, name='user_detail'),
    
    path('notes/', views.All_notes, name='notes'),
    path('note_detail/<int:noteid>/<str:noteslug>', views.Note_detail, name='note_detail')
]
