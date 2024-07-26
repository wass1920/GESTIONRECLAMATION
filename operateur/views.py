from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .models import Operateur, User
from .forms import SignUpForm, ReclamationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm 
from django.db import connection
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.db import connection
cursor = connection.cursor()
cursor.execute("DELETE FROM django_migrations WHERE app='operateur' AND name='0014_claim_timestamp';")
def home(request):
    operateur = get_user_model()
    return render(request, 'login.html', {'operateur': operateur})

def accueil(request):

    return render(request, 'accueil.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('dashboard')  # Redirige vers le tableau de bord
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        except Operateur.DoesNotExist:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'login.html')



def SignupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            operateur = form.cleaned_data['operateur']
            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO operateur_user (username, email, password, operateur) VALUES (%s, %s, %s, %s)", [username, email, password, operateur])
            
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def claim(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        form =ReclamationForm(request.POST)
        if form.is_valid():
            text=request.POST.get('claim', '')
            with connection.cursor() as cursor:
                cursor.execute("SELECT username, operateur FROM operateur_user WHERE id = %s", [user_id])
                row = cursor.fetchone()
                user, operator = row
                heure = timezone.now()
                cursor.execute("INSERT INTO operateur_claim (text, user, operator,heure) VALUES (%s, %s, %s, %s)", [text, user, operator,heure])

            return render(request, 'claim.html')
    else:
        return render(request, 'claim.html')
    if request.method == 'POST':
        form =ReclamationForm(request.POST)
        if form.is_valid():
            text=request.POST.get('claim', '')
            with connection.cursor() as cursor:
                cursor.execute("SELECT username, operateur FROM operateur_user WHERE id = %s", [user_id])
                row = cursor.fetchone()
                user, operator = row
                heure = timezone.now()
                cursor.execute("INSERT INTO operateur_claim (text, user, operator,heure) VALUES (%s, %s, %s, %s)", [text, user, operator,heure])
            return render(request, 'claim.html')
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, operateur FROM operateur_user WHERE id = %s", [user_id])
        row = cursor.fetchone()
        user, operator = row
        heure = timezone.now()
        cursor.execute("INSERT INTO operateur_claim (text, user, operator,heure) VALUES (%s, %s, %s, %s)", [text, user, operator,heure])

    return render(request, 'claim.html')

    
    

        

def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, password FROM operateur_user WHERE id = %s", [request.user.id])
        row = cursor.fetchone()
        username = row[0] if row else ''
        password = row[1] if row else ''
    return render(request, 'dashboard.html', {'username': username, 'password': password})



def profil(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        # Mettre à jour les champs dans la base de données
        with connection.cursor() as cursor:
            
            cursor.execute("UPDATE operateur_user SET username=%s, email=%s ,password=%s WHERE id=%s", [username, email, password, user_id])

        return redirect('profil')  # Rediriger vers la page de profil après la modification
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, email FROM operateur_user WHERE id = %s", [user_id])
            row = cursor.fetchone()
            username, email = row
            password=''
        
        return render(request, 'profil.html', {'username': username, 'email': email, 'password':password})

def loginoperateur(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            operateur = Operateur.objects.get(name=username)
            if operateur.password == password:
                request.session['user_id'] = operateur.id
                return redirect('dashboardop')  # Redirige vers le tableau de bord
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        except Operateur.DoesNotExist:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'loginoperateur.html')


def dashboardop(request):
    user_id = request.session.get('user_id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM operateur_operateur WHERE id = %s", [user_id])
        row = cursor.fetchone()
        x = row[0]
        cursor.execute("SELECT count(user) FROM operateur_claim where operator = %s",[x])
        row = cursor.fetchone()
        claim = row[0]
        cursor.execute("SELECT count(username) FROM operateur_user where operateur = %s",[x])
        row = cursor.fetchone()
        client= row[0]

    context = {
        'claim': claim,
        'client': client,
        'user':x
    }

    return render(request, 'dashboardop.html', context )



def Customers(request):
    user_id = request.session.get('user_id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM operateur_operateur WHERE id = %s", [user_id])
        row = cursor.fetchone()
        op=row[0]
        cursor.execute("SELECT username, email, id FROM operateur_user WHERE operateur = %s", [op])
        rows = cursor.fetchall()  
        users = []
        x = 0
        for row in rows:
            x = x+1 
            user = {
                'username': row[0],  # Utilisez row au singulier pour accéder à chaque ligne
                'email': row[1],
                'id' : row[2]
                
            }
            users.append(user)
    context = {
        'users': users,
        'user_count': x
    }
    return render(request, 'customers.html', context)


def profilop(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            
            cursor.execute("UPDATE operateur_operateur SET  email=%s ,password=%s WHERE id=%s", [ email, password, user_id])

        return redirect('profilop')  # Rediriger vers la page de profil après la modification
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT  email FROM operateur_operateur WHERE id = %s", [user_id])
            row = cursor.fetchone()

            print(row)
            email = row[0]
            password=''
        
        return render(request, 'profilop.html', { 'email': email, 'password':password})





def claimop(request):
    user_id = request.session.get('user_id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM operateur_operateur WHERE id = %s ", [user_id])
        row = cursor.fetchone()
        op = row[0]
        cursor.execute("SELECT  text, user FROM operateur_claim WHERE operator = %s", [op])
        rows = cursor.fetchall()  
        users = set()
        messages = []
        for row in rows:
            text = row[0]
            user = row[1]
            cursor.execute("SELECT COUNT(user) FROM operateur_claim WHERE user = %s GROUP BY USER", [user])
            count_row = cursor.fetchone()
            x = count_row[0]
            message = {
                'text': text,
                'user': user,
                'x': x
            }
            messages.append(message)
        
        cursor.execute("SELECT COUNT(*) FROM operateur_claim")
        total_claims_row = cursor.fetchone()
        numclaimstotal = total_claims_row[0]

    context = {
        'users': messages,
        'numclaimstotal':numclaimstotal
    }
    return render(request, 'claimop.html', context)




