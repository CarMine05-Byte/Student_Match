from django.shortcuts import render
from django.utils import timezone

from .models import *
from .utils import hash_password, verify_password


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
            studente = Studente.objects.filter(studente=user_valid).first()
            gruppo_disp = Gruppo.objects.all()
            partecipation = Partecipazione.objects.filter(studente=studente)
            context = {
                'studente': studente,
                'gruppo': gruppo_disp,
                'partecipa': partecipation,
                'success': "Autenticazione avvenuta con successo"
            }

            return render(request, 'home.html', context)
        else:
            return render(request, 'login.html', {'error': 'Credenziali non valide', 'user': user})

    return render(request, 'login.html', {'warning': 'Qualcosa è andato storto'})


def registration(request):
    print("Pagina di registrazione ottenuta")

    # function per prendere i ruoli
    def get_ruoli_utente(utente):
        ruoli = []

        if Studente.objects.filter(studente=utente).exists():
            ruoli.append("studente")
        if Tutor.objects.filter(tutor=utente).exists():
            ruoli.append("tutor")
        if Admin.objects.filter(admin=utente).exists():
            ruoli.append("admin")
        return ruoli

    # Estrazione dei dati
    if request.method == "POST":
        user = request.POST.get('user')
        email = request.POST.get('email')
        pwd = request.POST.get('pass')
        ruolo = request.POST.get('ruolo')

        # Controllo Duplicati
        if Utente.objects.filter(utente=user).exists():
            return render(request, 'registration.html', {'error': 'Username già registrato.'})

        if Utente.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email già registrata.'})

        # Controllo ruolo
        if ruolo not in ["studente", "tutor", "admin"]:
            return render(request, 'registration.html', {'error': 'Codice non valido'})

        # Campi Studente

        anno_corso = request.POST.get('anno_corso')
        corso_laurea_stu = request.POST.get('corso_laurea_stu')

        # Campi Tutor

        dipartimento = request.POST.get('dipartimento')
        area_competenza = request.POST.get('area_competenza')
        corso_laurea_tut = request.POST.get('corso_laurea_tut')

        # Campi Admin

        codice_invito = request.POST.get("codice_invito")
        if codice_invito != "CODICE_FOUNDER":
            return render(request, 'registration.html', {'error': 'Codice invito non valido'})

        new_user = None  # definiamo una variabile Null
        # Salva l'utente

        try:
            new_user = Utente.objects.create(
                utente=user,
                email=email,
                password=hash_password(pwd),
                ruolo=ruolo
            )
            if ruolo == "studente":
                Studente.objects.create(
                    studente=new_user,
                    anno_corso=anno_corso,
                    corso_laurea=corso_laurea_stu
                )
            elif ruolo == "tutor":
                Tutor.objects.create(
                    tutor=new_user,
                    dipartimento=dipartimento,
                    area_competenza=area_competenza,
                    laurea=corso_laurea_tut
                )
            elif ruolo == "admin":
                Admin.objects.create(
                    admin=new_user,
                    livello=1,
                    data_nomina=timezone.now().date()

                )

        except Exception as e:  # Errore di default
            print(f"Errore nella creazione oggetto utente-studente: {e}")

            if new_user is not None:
                new_user.delete()

            return render(request, 'registration.html', {'error': 'Errore Creazione Profilo'})
        ruoli_utente = get_ruoli_utente(new_user)
        print(f"Studente {user} registrato con successo!")
        return render(request, 'home.html',
                      {"user": new_user, 'ruoli': ruoli_utente, "success": "Registrazione completata con successo"})

    return render(request, 'registration.html', {'warning': 'Qualcosa è andato storto'})


def home(request):
    print("Abbiamo ottenuto la pagina home")
    if request.method == "POST":
        user = request.POST.get('user')
        email = request.POST.get('email')
        pwd = request.POST.get('pass')

        # Estraction of Datas
        user_valid = Utente.objects.filter(utente=user).first()
        if user_valid and verify_password(pwd, user_valid.password):
            studente = Studente.objects.get(studente__utente=user_valid)

            gruppo_disp = Gruppo.objects.filter(name_exam__year_course=studente.anno_corso,
                                                state=True)
            # SELECT name_exam
            # FROM FROM GROUP AS G INNER JOIN EXAM AS E ON G.name_exam=E.name
            # INNER JOIN STUDENT AS S ON G.id_student=S.id_student
            # INNER JOIN PARTECIPATE AS P ON G.id_group = P.id_group
            # WHERE E.year_course = S.year_course AND P.state = true;

            my_partecipation = Partecipazione.objects.filter(id_student=studente)

            context = {
                'user': user_valid,
                'studente': studente,
                'gruppo_disp': gruppo_disp,
                'partecipation': my_partecipation
            }

            return render(request, 'home.html', context)
        return render(request, 'login.html', {'error': 'Credenziali non valide', 'user': user})

    return render(request, 'login.html')


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
