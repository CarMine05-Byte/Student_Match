from django.shortcuts import render, redirect

from studymatch.models import *


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        # email = request.POST.get("email")
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

        print(f"Studente {user} registrato con successo!")
        return redirect('home')
    else:
        return render(request, 'register.html')


def home(request):
    print("Abbiamo ottenuto la pagina home")
    # Estraction of Datas

    student = Student.objects.get(user=request.user)

    group_disp = Group.objects.filter(name_exam__year_course=student.year_course,
                                      state=True)
    # SELECT name_exam
    # FROM FROM GROUP AS G INNER JOIN EXAM AS E ON G.name_exam=E.name
    # INNER JOIN STUDENT AS S ON G.id_student=S.id_student
    # INNER JOIN PARTECIPATE AS P ON G.id_group = P.id_group
    # WHERE E.year_course = S.year_course AND P.state = true;

    my_partecipation = Participate.objects.filter(id_student=student)

    return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')


def create_group(request):
    return render(request, 'create_group.html')
