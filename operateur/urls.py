from django.urls import path
from . import views
urlpatterns = [

    path('', views.accueil, name='accueil'),
    path('signup/' ,views.SignupPage,name='SignupPage'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('loginoperateur/',views.loginoperateur,name='loginoperateur'),
    path('dashboardop/',views.dashboardop,name='dashboardop'),
    path('Customers/',views.Customers,name='Customers'),
    path('profilop/', views.profilop, name='profilop'),
    path('claim/', views.claim, name='claim'),
    path('claimop/', views.claimop, name='claimop'),


]
