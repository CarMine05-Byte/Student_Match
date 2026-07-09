from django.shortcuts import render

from .models import *
from .utils import hash_password, verify_password, get_corsi_laurea


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

            # Session
            request.session['user'] = user_valid.utente
            request.session['ruolo'] = user_valid.ruolo

            return home(request, {"success": "Autenticazione avvenuta con successo"})
        else:
            request.session.flush()
            return render(request, 'login.html', {'error': 'Credenziali non valide', 'user': user})
    return render(request, 'login.html', )


def registration(request):
    print("Pagina di registrazione ottenuta")
    corsi = get_corsi_laurea()
    registration_context = {'corsi': corsi}

    # Estrazione dei dati
    if request.method == "POST":
        user = request.POST.get('user')
        email = (request.POST.get('email') or '').strip()
        pwd = request.POST.get('pass')
        ruolo = request.POST.get('ruolo')

        # Controllo Duplicati
        if Utente.objects.filter(utente=user).exists():
            return render(request, 'registration.html', {**registration_context, 'error': 'Username già registrato.'})

        if email and Utente.objects.filter(email__exact=email).exists():
            return render(request, 'registration.html', {**registration_context, 'error': 'Email già registrata.'})

        # Controllo ruolo
        if ruolo not in ["studente", "tutor", "admin"]:
            return render(request, 'registration.html', {**registration_context, 'error': 'Ruolo non scelto'})

        # Campi Studente

        anno_corso = request.POST.get('anno_corso')
        corso_laurea_stu = request.POST.get('corso_laurea_stu')

        # Campi Tutor

        dipartimento = request.POST.get('dipartimento')
        area_competenza = request.POST.get('area_competenza')
        corso_laurea_tut = request.POST.get('corso_laurea_tut')

        # Campi Admin

        codice_invito = request.POST.get("codice_invito")

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

            if ruolo == "admin" and codice_invito != "ADMIN_2026":
                return render(request, 'registration.html',
                              {**registration_context, 'error': 'Codice invito non valido'})

            if new_user is not None:
                new_user.delete()
                logout(request)
            return render(request, 'registration.html', {**registration_context, 'error': 'Errore Creazione Profilo'})
        ruoli_utente = get_ruoli_utente(new_user)
        print(f"Studente {user} registrato con successo!")
        request.session['user'] = new_user.utente
        request.session['ruolo'] = new_user.ruolo
        return home(request,
                    {"success": "Registrazione completata con successo", "ruoli ": ruoli_utente, "corsi": corsi})

    return render(request, 'registration.html', registration_context)


def home(request, extra_content=None):
    print("Abbiamo ottenuto la pagina home")

    user = request.session.get('user')
    ruolo = request.session.get('ruolo')

    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})
    # Estraction of Datas
    user_valid = Utente.objects.filter(utente=user).first()
    # SELECT * FROM UTENTE WHERE utente = $user;
    if not user_valid:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    gruppo = Gruppo.objects.all()
    esami = Esame.objects.all()

    if ruolo == "studente":
        studente = Studente.objects.filter(studente=user_valid).first()
        if not studente:
            return render(request, "login.html", {"error": "Studente non trovato"})

        partecipa_stud = Partecipazione.objects.filter(studente=studente)
        esami_stud = esami.filter(anno_corso=studente.anno_corso, corso=studente.corso_laurea)
        gruppi_stud = gruppo.filter(gruppo_esame__id_esame__in=esami_stud).exclude(
            id_gruppo__in=partecipa_stud.values('id_gruppo')).distinct()
        context = {
            "utente": user_valid,
            "studente": studente,
            "part_stud": partecipa_stud,
            "grup_stud": gruppi_stud,
            "ruolo": ruolo
        }

        if extra_content:
            context.update(extra_content)

        return render(request, "home.html", context)
    if ruolo == "tutor":
        tutor = Tutor.objects.filter(tutor=user_valid).first()
        supporto_tut = Supporto.objects.filter(tutor=tutor)
        gruppi_tut = gruppo.filter(id_gruppo__in=supporto_tut.values("id_gruppo")).distinct()

        gruppi_gia_seguiti = Supporto.objects.values_list("id_gruppo", flat=True)
        gruppi_disp_tut = gruppo.exclude(
            id_gruppo__in=gruppi_gia_seguiti
        )
        context = {
            "utente": user_valid,
            "tutor": tutor,
            "supp_tut": supporto_tut,
            "grup_tut": gruppi_tut,
            "grup_disp_tut": gruppi_disp_tut,
            "ruolo": ruolo
        }
        if extra_content:
            context.update(extra_content)

        return render(request, "home.html", context)
    if ruolo == "admin":
        admin = Admin.objects.filter(admin=user_valid).first()
        gruppi_admin = gruppo.filter(gruppo_admin__admin=admin).distinct()
        gruppi_gia_gestiti = Gestione.objects.values_list("id_gruppo", flat=True)

        gruppi_disp = Gruppo.objects.exclude(
            id_gruppo__in=gruppi_gia_gestiti
        ).distinct()

        context = {
            "utente": user_valid,
            "admin": admin,
            "grup_admin": gruppi_admin,
            "gruppi_disp": gruppi_disp,
            "ruolo": ruolo
        }

        if extra_content:
            context.update(extra_content)

        return render(request, "home.html", context)
    return render(request, 'login.html', {"error": "Ruolo non valido"})


def profile(request):
    print("Pagina profilo ottenuta!")

    user = request.session.get('user')
    ruolo = request.session.get('ruolo')

    if not user:
        return render(request, "login.html", {"error": "Errore sessione login scaduta"})

    utente = Utente.objects.filter(utente=user).first()

    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    context = {
        "utente": utente,
        "ruolo": ruolo
    }
    if ruolo == "studente":
        studente = Studente.objects.filter(studente=utente).first()
        if not studente:
            return render(request, "login.html", {"error": "Profilo Studente non trovato"})
        context["studente"] = studente
    elif ruolo == "tutor":
        tutor = Tutor.objects.filter(tutor=utente).first()
        if not tutor:
            return render(request, "login.html", {"error": "Profilo Tutor non trovaot"})
        context["tutor"] = tutor
    elif ruolo == "admin":
        admin = Admin.objects.filter(admin=utente).first()
        if not admin:
            return render(request, "login.html", {"error": "Profilo Admin non trovato"})
        context["admin"] = admin
    else:
        return render(request, "login.html", {"error": "Ruolo non trovato"})

    return render(request, 'profile.html', context)


def crea_gruppo(request):
    print("Pagina creazione gruppo ottenuta")

    user = request.session.get("user")
    ruolo = request.session.get("ruolo")

    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})

    utente = Utente.objects.filter(utente=user).first()

    if ruolo not in ["admin", "tutor"]:
        return home(request, {"error": "Solo gli amministratori e i tutor possono creare e gestire il gruppo!"})
    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato!"})

    esami = Esame.objects.all()

    if request.method == "POST":
        nome_gruppo = request.POST.get("nome_gruppo")
        descrizione = request.POST.get("descrizione")
        link_chat = request.POST.get("link_chat")
        max_partecipanti = request.POST.get("max_partecipanti")
        id_esame = request.POST.get("id_esame")
        periodo = request.POST.get("periodo") or 0

        if not nome_gruppo or not max_partecipanti or not id_esame:
            return render(request, "crea_gruppo.html", {"error": "Compila tutti i campi obbligatori", "esami": esami})

        esame_selezionato = Esame.objects.filter(id_esame=id_esame).first()
        if not esame_selezionato:
            return render(request, "crea_gruppo.html", {"error": "Esame non valido!", "esami": esami})

        # Esami
        gruppo = Gruppo.objects.create(
            nome_gruppo=nome_gruppo,
            descrizione=descrizione,
            link_chat=link_chat,
            max_partecipanti=max_partecipanti
        )
        Assegnazione.objects.create(
            id_gruppo=gruppo,
            id_esame=esame_selezionato,
            periodo=periodo
        )
        if ruolo == "admin":
            admin = Admin.objects.filter(admin=utente).first()

            if admin:
                Gestione.objects.create(
                    admin=admin,
                    id_gruppo=gruppo
                )
                return home(request, {"success": "Gruppo creato con successo!"})
        if ruolo == "tutor":
            tutor = Tutor.objects.filter(tutor=utente).first()

            if tutor:
                Supporto.objects.create(
                    tutor=tutor,
                    id_gruppo=gruppo,
                    punteggio=0
                )
                return home(request, {"success": "Gruppo creato con successo!"})
    return render(request, "crea_gruppo.html", {"esami": esami})


def dettaglio_gruppo(request, id_gruppo):
    user = request.session.get('user')
    ruolo = request.session.get('ruolo')

    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})

    utente = Utente.objects.filter(utente=user).first()
    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    gruppo = Gruppo.objects.filter(id_gruppo=id_gruppo).first()
    if not gruppo:
        return home(request, {"error": "Gruppo non trovato"})

    partecipazioni = Partecipazione.objects.filter(id_gruppo=gruppo)
    supporti = Supporto.objects.filter(id_gruppo=gruppo)
    assegnazioni = Assegnazione.objects.filter(id_gruppo=gruppo)
    posti_occupati = partecipazioni.count()
    posti_disponibili = max(gruppo.max_partecipanti - posti_occupati, 0)

    context = {
        "utente": utente,
        "ruolo": ruolo,
        "gruppo": gruppo,
        "assegnazioni": assegnazioni,
        "partecipazioni": partecipazioni,
        "supporti": supporti,
        "posti_occupati": posti_occupati,
        "posti_disponibili": posti_disponibili,
    }

    if ruolo == "studente":
        studente = Studente.objects.filter(studente=utente).first()
        context["studente"] = studente
        context["iscritto"] = Partecipazione.objects.filter(
            studente=studente,
            id_gruppo=gruppo
        ).exists() if studente else False
    elif ruolo == "tutor":
        tutor = Tutor.objects.filter(tutor=utente).first()
        context["tutor"] = tutor
        context["segue_gruppo"] = Supporto.objects.filter(
            tutor=tutor,
            id_gruppo=gruppo
        ).exists() if tutor else False
    elif ruolo == "admin":
        admin = Admin.objects.filter(admin=utente).first()
        context["admin"] = admin
        context["gestisce_gruppo"] = Gestione.objects.filter(
            admin=admin,
            id_gruppo=gruppo
        ).exists() if admin else False

    return render(request, 'dettaglio_gruppo.html', context)


def esame(request):
    user = request.session.get("user")
    ruolo = request.session.get("ruolo")

    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})

    if ruolo != "admin":
        return home(request, {"error": "Solo gli admin possono creare esami."})

    corsi = get_corsi_laurea()

    if request.method == "POST":
        nome_esame = request.POST.get("nome_esame")
        corso = request.POST.get("corso")
        anno_corso = request.POST.get("anno_corso")
        semestre = request.POST.get("semestre")
        cfu = request.POST.get("cfu")

        if not nome_esame or not corso or not anno_corso or not semestre or not cfu:
            return render(request, "crea_esame.html", {"corsi": corsi, "error": "Compila tutti i campi."})

        esame_esistente = Esame.objects.filter(
            nome_esame=nome_esame,
            corso=corso,
            anno_corso=anno_corso
        ).exists()

        if esame_esistente:
            return render(request, "crea_esame.html", {
                "corsi": corsi,
                "error": "Questo esame è già presente."
            })
        Esame.objects.create(
            nome_esame=nome_esame,
            corso=corso,
            anno_corso=anno_corso,
            semestre=semestre,
            cfu=cfu
        )

        return render(request, "crea_esame.html", {"corsi": corsi, "success": "Esame creato correttamente."})
    return render(request, 'crea_esame.html', {"corsi": corsi})


def notifica(request):
    return render(request, 'notifiche.html')


def get_ruoli_utente(utente):
    ruoli = []

    if Studente.objects.filter(studente=utente).exists():
        ruoli.append("studente")
    if Tutor.objects.filter(tutor=utente).exists():
        ruoli.append("tutor")
    if Admin.objects.filter(admin=utente).exists():
        ruoli.append("admin")
    return ruoli


def logout(request):
    request.session.flush()
    return render(request, "login.html")
