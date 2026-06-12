from django.shortcuts import render

from studymatch.models import *
from studymatch.utils import hash_password, verify_password


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        # email = request.POST.get("email")
        pwd = request.POST.get("pass")
        # Use Hash lib for hash password
        print(f"Username : {user}")

        user_valid = Utente.objects.filter(utente=user).first()
        # select * from Student where utente ="$user"

        if user_valid and verify_password(pwd, user_valid.password):  # verifichiamo la password
            print(f"Utente Verificato : {user}")

            return render(request, 'home.html',
                          {'user': user_valid, 'Success': "Autenticazione avvenuta con successo!"})
        else:
            return render(request, 'login.html', {'error': 'Credenziali non valide', 'user': user})

    return render(request, 'login.html')


def registration(request):
    print("Pagina di registrazione ottenuta")

    # Estrazione dei dati
    if request.method == "POST":
        user = request.POST.get('user')
        email = request.POST.get('email')
        pwd = request.POST.get('pass')

        # Controllo Duplicati
        if Utente.objects.filter(utente=user).exists():
            return render(request, 'registration.html', {'error': 'Username già registrato.'})

        if Utente.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email già registrata.'})
        new_user = None  # definiamo una variabile Null
        # Salva l'utente

        try:
            new_user = Utente.objects.create(
                utente=user,
                email=email,
                password=hash_password(pwd),
                ruolo="studente"
            )
            # Creiamo lo studente
            Studente.objects.create(
                studente=new_user
            )

        except Exception as e:  # Errore di default
            print(f"Errore nella creazione oggetto utente-studente: {e}")

            if new_user is not None:
                new_user.delete()

            return render(request, 'registration.html', {'error': 'Errore Creazione Profilo'})

        print(f"Studente {user} registrato con successo!")
        return render(request, 'home.html', {"user": new_user, "success": "Registrazione completata con successo"})

    return render(request, 'registration.html')


def home(request):
    print("Abbiamo ottenuto la pagina home")
    # Estraction of Datas

    studente = Studente.objects.get(studente__utente=request.user)

    gruppo_disp = Gruppo.objects.filter(name_exam__year_course=studente.anno_corso,
                                        state=True)

    # SELECT name_exam
    # FROM FROM GROUP AS G INNER JOIN EXAM AS E ON G.name_exam=E.name
    # INNER JOIN STUDENT AS S ON G.id_student=S.id_student
    # INNER JOIN PARTECIPATE AS P ON G.id_group = P.id_group
    # WHERE E.year_course = S.year_course AND P.state = true;

    my_partecipation = Partecipazione.objects.filter(id_student=studente)

    context = {
        'studente': studente,
        'gruppo_disp': gruppo_disp,
        'partecipation': my_partecipation
    }

    return render(request, 'home.html', context)


def profile(request):
    return render(request, 'profile.html')


def crea_gruppo(request):
    return render(request, 'create_group.html')


def gruppi(request):
    return render(request, 'gruppi.html')


def dettaglio_gruppo(request):
    return render(request, 'dettaglio_gruppo.html')


def esame(request):
    return render(request, 'esami.html')


def notifica(request):
    return render(request, 'notifiche.html')
