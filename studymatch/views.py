from django.shortcuts import render, redirect

from studymatch.models import Student


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        #email = request.POST.get("email")
        pwd = request.POST.get("pass")
        # Use Hash lib for hash password
        # pwd = hashlib.sha256(pwd.encode()).hexdigest()
        print(f"Username : {user} , Password: {pwd}")

        user_valid = Student.objects.filter(username=user, password=pwd)
        # select * from Student where username ="$user" and password = $pwd

        if user_valid.exists():
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenziali non valide', 'user': user})
    return render(request, 'login.html')


def registration(request):
    print("Pagina di registrazione ottenuta")
    # Estrazione dei dati
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pass')

        # Controllo Duplicati
        if Student.objects.filter(username=user).exists():
            return render(request, 'register.html', {'error': 'Email già registrata.'})

        # Salva l'utente
        new_user = Student(username=user, password=pwd)
        new_user.save()

        print(f"Utente {user} registrato con successo!")
        return redirect('home')
    else:
        return render(request, 'register.html')


def home(request):
    return render(request, 'profile.html')
