from django.db import IntegrityError
from django.shortcuts import render

from .models import *
from .utils import hash_password, verify_password, get_corsi_laurea

MAX_TUTOR_PER_GRUPPO = 4
MAX_ADMIN_PER_GRUPPO = 2


def index(request):
    return render(request, "index.html")


# Gestisce autenticazione e inizializzazione della sessione utente.
def login(request):
    if request.method == "POST":
        ident = request.POST.get("id")
        pwd = request.POST.get("pass")
        user_valid = Utente.objects.filter(
            models.Q(utente=ident) | models.Q(email=ident)
        ).first()

        if user_valid and verify_password(pwd, user_valid.password):
            request.session["user"] = user_valid.utente
            request.session["ruolo"] = user_valid.ruolo

            return home(request, {"success": "Autenticazione avvenuta con successo"})

        request.session.flush()
        return render(request, "login.html", {"error": "Credenziali non valide", "user": ident})
    return render(request, "login.html")


# Registra l'utente e crea il profilo collegato al ruolo scelto.
def registration(request):
    corsi = get_corsi_laurea()
    registration_context = {"corsi": corsi}

    if request.method == "POST":
        user = request.POST.get("user")
        nome = (request.POST.get("nome") or "").strip()
        cognome = (request.POST.get("cognome") or "").strip()
        email = (request.POST.get("email") or "").strip()
        pwd = request.POST.get("pass")
        ruolo = request.POST.get("ruolo")

        # Controlli preliminari su username, email e ruolo.
        if Utente.objects.filter(utente=user).exists():
            return render(request, "registration.html", {
                **registration_context,
                "error": "Username già registrato.",
            })

        if email and Utente.objects.filter(email__exact=email).exists():
            return render(request, "registration.html", {
                **registration_context,
                "error": "Email già registrata.",
            })

        if ruolo not in ["studente", "tutor", "admin"]:
            return render(request, "registration.html", {
                **registration_context,
                "error": "Ruolo non scelto",
            })

        anno_corso = request.POST.get("anno_corso")
        corso_laurea_stu = request.POST.get("corso_laurea_stu")
        dipartimento = request.POST.get("dipartimento")
        area_competenza = request.POST.get("area_competenza")
        corso_laurea_tut = request.POST.get("corso_laurea_tut")
        codice_invito = (request.POST.get("codice_invito") or "").strip()

        if ruolo == "admin" and codice_invito != "ADMIN_2026":
            return render(request, "registration.html", {
                **registration_context,
                "error": "Codice invito non valido",
            })

        # Creazione dell'utente base e del profilo specifico.
        new_user = None
        try:
            new_user = Utente.objects.create(
                utente=user,
                email=email,
                password=hash_password(pwd),
                ruolo=ruolo,
                nome=nome,
                cognome=cognome
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

        except Exception:
            if new_user is not None:
                new_user.delete()
                logout(request)
            return render(request, "registration.html", {
                **registration_context,
                "error": "Errore Creazione Profilo",
            })
        ruoli_utente = get_ruoli_utente(new_user)
        # Acquisizione della sessione
        request.session["user"] = new_user.utente
        request.session["ruolo"] = new_user.ruolo
        return home(request, {
            "success": "Registrazione completata con successo",
            "ruoli ": ruoli_utente,
            "corsi": corsi,
        })

    return render(request, "registration.html", registration_context)


# Costruisce la dashboard in base al ruolo salvato in sessione.
def home(request, extra_content=None):
    user = request.session.get("user")
    ruolo = request.session.get("ruolo")

    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})

    user_valid = Utente.objects.filter(utente=user).first()
    if not user_valid:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    gruppo = Gruppo.objects.all()
    esami = Esame.objects.all()

    if ruolo == "studente":
        # Gruppi compatibili con corso e anno dello studente, esclusi quelli già richiesti.
        studente = Studente.objects.filter(studente=user_valid).first()
        if not studente:
            return render(request, "login.html", {"error": "Studente non trovato"})

        esami_stud = esami.filter(anno_corso=studente.anno_corso, corso=studente.corso_laurea)
        partecipa_stud = Partecipazione.objects.filter(studente=studente).distinct()

        gruppi_stud = gruppo.filter(
            gruppo_esame__id_esame__in=esami_stud
        ).exclude(
            id_gruppo__in=partecipa_stud.values("id_gruppo")
        ).distinct()
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
        # Gruppi seguiti dal tutor e gruppi ancora disponibili.
        tutor = Tutor.objects.filter(tutor=user_valid).first()
        supporto_tut = Supporto.objects.filter(tutor=tutor)
        gruppi_tut = gruppo.filter(id_gruppo__in=supporto_tut.values("id_gruppo")).distinct()

        gruppi_gia_seguiti = supporto_tut.values_list("id_gruppo", flat=True)
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
        # Gruppi gestiti dall'admin e gruppi gestiti da altri admin.
        admin = Admin.objects.filter(admin=user_valid).first()
        gruppi_admin = gruppo.filter(gruppo_admin__admin=admin).distinct()
        gruppi_disp = gruppo.exclude(gruppo_admin__admin=admin).distinct()

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

    return render(request, "login.html", {"error": "Ruolo non valido"})


# Mostra i dati del profilo collegato al ruolo corrente.
def profile(request):
    user = request.session.get("user")
    ruolo = request.session.get("ruolo")

    if not user:
        return render(request, "login.html", {"error": "Errore sessione login scaduta"})

    utente = Utente.objects.filter(utente=user).first()

    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    context, error = crea_context_profilo(utente, ruolo)
    if error:
        return render(request, "login.html", {"error": error})

    context["profilo_corrente"] = True

    return render(request, "profile.html", context)


# Mostra il profilo di un utente collegato a un gruppo.
def profile_utente(request, username):
    user = request.session.get("user")

    if not user:
        return render(request, "login.html", {"error": "Errore sessione login scaduta"})

    utente = Utente.objects.filter(utente=username).first()
    if not utente:
        return home(request, {"error": "Utente non trovato"})

    if utente.ruolo not in ["studente", "tutor", "admin"]:
        return home(request, {"error": "Profilo utente non consultabile."})

    context, error = crea_context_profilo(utente, utente.ruolo)
    if error:
        return home(request, {"error": error})

    gruppo_id = request.GET.get("gruppo")
    if gruppo_id and gruppo_id.isdigit():
        context["gruppo_ritorno"] = Gruppo.objects.filter(id_gruppo=gruppo_id).first()

    context["profilo_corrente"] = username == user

    return render(request, "profile.html", context)


# Crea un gruppo e collega automaticamente admin o tutor al nuovo gruppo.
def crea_gruppo(request):
    user = request.session.get("user")
    ruolo = request.session.get("ruolo")

    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})

    utente = Utente.objects.filter(utente=user).first()

    if ruolo not in ["admin", "tutor"]:
        return home(request, {
            "error": "Solo gli amministratori e i tutor possono creare e gestire il gruppo!",
        })
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
        periodo = int(request.POST.get("periodo")) or 0

        if not nome_gruppo or not max_partecipanti or not id_esame:
            return render(request, "crea_gruppo.html", {
                "error": "Compila tutti i campi obbligatori",
                "esami": esami,
            })

        esame_selezionato = Esame.objects.filter(id_esame=id_esame).first()
        if not esame_selezionato:
            return render(request, "crea_gruppo.html", {
                "error": "Esame non valido!",
                "esami": esami,
            })

        gruppo = Gruppo.objects.create(
            nome_gruppo=nome_gruppo,
            descrizione=descrizione,
            link_chat=link_chat,
            max_partecipanti=max_partecipanti
        )

        Assegnazione.objects.create(
            id_gruppo=gruppo,
            id_esame=esame_selezionato,
            periodo=timezone.now() + timedelta(days=periodo)
        )
        if ruolo == "admin":
            admin = Admin.objects.filter(admin=utente).first()

            if admin:
                Gestione.objects.create(
                    admin=admin,
                    id_gruppo=gruppo
                )
                return home(request, {"success": "Gruppo creato con successo!"})
    return render(request, "crea_gruppo.html", {"esami": esami})


# Mostra e gestisce le azioni disponibili nel dettaglio di un gruppo.
def dettaglio_gruppo(request, id_gruppo):
    user = request.session.get("user")
    ruolo = request.session.get("ruolo")
    if not user:
        return render(request, "login.html", {"error": "Sessione scaduta"})

    utente = Utente.objects.filter(utente=user).first()
    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    gruppo = Gruppo.objects.filter(id_gruppo=id_gruppo).first()
    if not gruppo:
        return home(request, {"error": "Gruppo non trovato"})

    assegnazioni = Assegnazione.objects.filter(id_gruppo=gruppo)

    context = {
        "utente": utente,
        "ruolo": ruolo,
        "gruppo": gruppo,
        "assegnazioni": assegnazioni
    }
    if ruolo == "studente":
        # Lo studente può richiedere accesso solo ai gruppi compatibili.
        studente = Studente.objects.filter(studente=utente).first()

        partecipazione_utente = (
            Partecipazione.objects.filter(
                studente=studente,
                id_gruppo=gruppo,
            ).first()
            if studente else None
        )
        gruppo_compatibile = (
            Assegnazione.objects.filter(
                id_gruppo=gruppo,
                id_esame__corso=studente.corso_laurea,
                id_esame__anno_corso=studente.anno_corso,
            ).exists()
            if studente else False
        )
        #Controllo di tentativo non autorizzato dell'utente di partecipare a un gruppo.
        if not partecipazione_utente and not gruppo_compatibile:
            return home(request, {
                "error": (
                    "Non puoi accedere a questo gruppo: non partecipi "
                    "e non puoi richiedere la partecipazione."
                )
            })

        context["studente"] = studente
        context["partecipazione_utente"] = partecipazione_utente
        context["gruppo_compatibile"] = gruppo_compatibile

        if request.method == "POST":
            gestisci_post_studente(
                request,
                studente,
                gruppo,
                gruppo_compatibile,
                context
            )
    elif ruolo == "tutor":
        # Il tutor può entrare nel gruppo e caricare materiali dopo l'ingresso.
        tutor = Tutor.objects.filter(tutor=utente).first()

        supporto_utente = (
            Supporto.objects.filter(tutor=tutor, id_gruppo=gruppo).first()
            if tutor else None
        )

        context["tutor"] = tutor
        context["supporto_utente"] = supporto_utente

        if request.method == "POST":
            gestisci_post_tutor(
                request,
                tutor,
                supporto_utente,
                gruppo,
                context
            )
    elif ruolo == "admin":
        # L'admin può prendere in gestione il gruppo o amministrarlo se già autorizzato.
        admin = Admin.objects.filter(admin=utente).first()

        gestisce_gruppo = (
            Gestione.objects.filter(admin=admin, id_gruppo=gruppo).exists()
            if admin else False
        )

        context["admin"] = admin
        context["gestisce_gruppo"] = gestisce_gruppo

        if request.method == "POST":
            gestisci_post_admin(
                request,
                admin,
                gestisce_gruppo,
                gruppo,
                context
            )
        context["richieste_studenti"] = Partecipazione.objects.filter(
            id_gruppo=gruppo,
            stato=False
        )

        partecipazioni = Partecipazione.objects.filter(
            id_gruppo=gruppo,
            stato=True,
        )
        supporti = Supporto.objects.filter(id_gruppo=gruppo)

        context["partecipazioni"] = partecipazioni
        context["supporti"] = supporti

    partecipanti_effettivi = Partecipazione.objects.filter(
        id_gruppo=gruppo,
        stato=True,
    ).count()

    residuo = gruppo.max_partecipanti - partecipanti_effettivi
    posti_disponibili = max(residuo, 0)

    context["partecipanti_effettivi"] = partecipanti_effettivi
    context["posti_disponibili"] = posti_disponibili

    return render(request, "dettaglio_gruppo.html", context)


def partecipanti_gruppo(request, id_gruppo):
    user = request.session.get("user")
    if not user:
        return render(request, "login.html", {"error": "Sessione scaduta"})

    utente = Utente.objects.filter(utente=user).first()
    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    gruppo = Gruppo.objects.filter(id_gruppo=id_gruppo).first()
    if not gruppo:
        return home(request, {"error": "Gruppo non trovato"})

    studenti_gruppo = Partecipazione.objects.filter(
        id_gruppo=gruppo,
        stato=True
    ).select_related("studente__studente")

    return render(request, "partecipanti_gruppo.html", {
        "utente": utente,
        "gruppo": gruppo,
        "studenti_gruppo": studenti_gruppo,
    })


# Permette agli admin di creare nuovi esami associabili ai gruppi.
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
            return render(request, "crea_esame.html", {
                "corsi": corsi,
                "error": "Compila tutti i campi.",
            })

        esame_esistente = Esame.objects.filter(
            nome_esame=nome_esame,
            corso=corso,
            anno_corso=anno_corso
        ).exists()

        if esame_esistente:
            return render(request, "crea_esame.html", {
                "corsi": corsi,
                "error": "Questo esame è già presente.",
            })
        Esame.objects.create(
            nome_esame=nome_esame,
            corso=corso,
            anno_corso=anno_corso,
            semestre=semestre,
            cfu=cfu
        )

        return render(request, "crea_esame.html", {
            "corsi": corsi,
            "success": "Esame creato correttamente.",
        })
    return render(request, "crea_esame.html", {"corsi": corsi})


# Gestisce lettura e invio delle notifiche tra admin, studenti e gruppi.
def notifica(request):
    user = request.session.get("user")
    if not user:
        return render(request, "login.html", {"error": "Sessione Scaduta"})

    utente = Utente.objects.filter(utente=user).first()
    if not utente:
        request.session.flush()
        return render(request, "login.html", {"error": "Utente non trovato"})

    context = {
        "notifiche": notifica_ric(utente),
        "gruppi_gestiti": gruppi_gestiti_admin(utente),
    }

    if request.method == "POST":
        azione = request.POST.get("azione")

        if azione == "invia":
            admin = Admin.objects.filter(admin=utente).first()
            id_gruppo = request.POST.get("id_gruppo")
            testo = (request.POST.get("testo") or "").strip()

            if not id_gruppo:
                context["error"] = "Seleziona un gruppo."
            else:
                gruppo = Gruppo.objects.filter(id_gruppo=id_gruppo).first()
                context.update(notifica_inv(admin, gruppo, testo))
        elif azione == "letta":
            lette = notifica_lette(utente)
            context["success"] = f"{lette} notifiche segnate come lette."

        context["notifiche"] = notifica_ric(utente)

    return render(request, "notifiche.html", context)


# Restituisce i ruoli effettivamente collegati a un utente.
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


###FUNZIONI AUSILIARI######################################################################################################################################################################
# Funzioni ausiliarie per materiali e partecipazione ai gruppi.
def carica_materiale_gruppo(request, gruppo, context):
    materiale_file = request.FILES.get("file_materiale")

    if not materiale_file:
        context["error"] = "Seleziona un file da caricare."
        return

    nome_file = materiale_file.name[:150]

    if Materiale.objects.filter(nome_file=nome_file).exists():
        context["error"] = "Esiste già un file con questo nome."
        return

    materiale = Materiale.objects.create(
        nome_file=nome_file,
        tipo="file",
        file=materiale_file,
    )

    Condivisione.objects.create(
        file=materiale,
        id_gruppo=gruppo,
    )

    context["success"] = "File caricato correttamente."


def richiedi_partecipazione_gruppo(studente, gruppo, gruppo_compatibile, context):
    if not studente:
        context["error"] = "Profilo studente non trovato."
        return

    if not gruppo_compatibile:
        context["error"] = (
            "Non puoi partecipare a un gruppo associato"
            "a un corso o anno diverso dal tuo."
        )
        return

    partecipazione = Partecipazione.objects.filter(
        studente=studente,
        id_gruppo=gruppo
    ).first()

    if partecipazione:
        context["error"] = "Hai già inviato una richiesta per questo gruppo."
        return

    partecipazione = Partecipazione.objects.create(
        studente=studente,
        id_gruppo=gruppo,
        stato=False
    )
    context["partecipazione_utente"] = partecipazione
    context["success"] = "Richiesta di partecipazione inviata."


# Funzioni ausiliarie per tutor e admin nel dettaglio gruppo.
def entra_come_tutor_gruppo(tutor, gruppo, context):
    if not tutor:
        context["error"] = "Profilo tutor non trovato."
        return

    supporto_check = Supporto.objects.filter(
        tutor=tutor,
        id_gruppo=gruppo
    ).first()

    if supporto_check:
        context["error"] = "Stai già supportando questo gruppo."
        return

    num_tutor = Supporto.objects.filter(id_gruppo=gruppo).count() >= MAX_TUTOR_PER_GRUPPO
    if not num_tutor:
        context["error"] = "Il gruppo ha già il numero massimo di tutor"
        return

    try:
        supporto = Supporto.objects.create(
            tutor=tutor,
            id_gruppo=gruppo
        )
    except IntegrityError:
        context["error"] = "Il gruppo ha già il numero massimo di tutor"
        return

    context["supporto_utente"] = supporto
    context["success"] = "Sei entrato nel gruppo come tutor."


def accetta_partecipazione_gruppo(richiesta_id, gruppo, context):
    richiesta = Partecipazione.objects.filter(
        id=richiesta_id,
        id_gruppo=gruppo,
        stato=False
    ).first()
    conteggio = Partecipazione.objects.filter(
        id_gruppo=gruppo,
        stato=True
    ).count()

    if not richiesta:
        context["error"] = "Richiesta di partecipazione non trovata."
    elif conteggio >= gruppo.max_partecipanti:
        context["error"] = (
            "Non puoi accettare la richiesta:"
            "il gruppo ha raggiunto il limite massimo"
        )
    else:
        richiesta.stato = True
        richiesta.save()
        context["success"] = "Richiesta di partecipazione accettata."


def rifiuta_partecipazione_gruppo(richiesta_id, gruppo, context):
    richiesta = Partecipazione.objects.filter(
        id=richiesta_id,
        id_gruppo=gruppo,
        stato=False
    ).first()

    if richiesta:
        richiesta.delete()
        context["success"] = "Richiesta di partecipazione rifiutata."
    else:
        context["error"] = "Richiesta di partecipazione non trovata."


def entra_come_admin_gruppo(admin, gruppo, context):
    if not admin:
        context["error"] = "Profilo admin non trovato."
        return

    gestione = Gestione.objects.filter(
        admin=admin,
        id_gruppo=gruppo
    ).first()

    if gestione:
        context["error"] = "Gestisci già questo gruppo."
        return
    gestione_count = Gestione.objects.filter(id_gruppo=gruppo).count() >= MAX_ADMIN_PER_GRUPPO

    if gestione_count:
        context["error"] = "Il gruppo ha già il numero massimo di amministratori."

    try:
        Gestione.objects.create(
            admin=admin,
            id_gruppo=gruppo
        )
    except IntegrityError:
        context["error"] = "il gruppo ha già il numero massimo di amministratori"
        return
    context["gestisce_gruppo"] = True
    context["success"] = "Ora gestisci questo gruppo."


def modifica_gruppo(request, gruppo, context):
    nome_gruppo = (request.POST.get("nome_gruppo") or "").strip()
    descrizione = (request.POST.get("descrizione") or "").strip()
    link_chat = (request.POST.get("link_chat") or "").strip()
    max_partecipanti = request.POST.get("max_partecipanti")

    try:
        max_partecipanti = int(max_partecipanti)
    except (TypeError, ValueError):
        max_partecipanti = 0

    partecipanti_confermati = Partecipazione.objects.filter(
        id_gruppo=gruppo,
        stato=True
    ).count()

    if not nome_gruppo:
        context["error"] = "Inserisci il nome del gruppo."
    elif max_partecipanti < partecipanti_confermati:
        context["error"] = (
            "I posti massimi non possono essere inferiori "
            "ai partecipanti già confermati."
        )
    elif max_partecipanti < 1:
        context["error"] = "Inserisci almeno un posto disponibile."
    else:
        gruppo.nome_gruppo = nome_gruppo
        gruppo.descrizione = descrizione
        gruppo.link_chat = link_chat
        gruppo.max_partecipanti = max_partecipanti
        gruppo.save()
        context["success"] = "Gruppo aggiornato correttamente."


# Dispatcher delle azioni POST per ruolo nella pagina dettaglio gruppo.
def gestisci_post_studente(request, studente, gruppo, gruppo_compatibile, context):
    azione = request.POST.get("azione")

    if azione == "richiedi_partecipazione":
        richiedi_partecipazione_gruppo(
            studente,
            gruppo,
            gruppo_compatibile,
            context
        )


def gestisci_post_tutor(request, tutor, supporto_utente, gruppo, context):
    azione = request.POST.get("azione")

    if azione == "entra_supporto":
        entra_come_tutor_gruppo(tutor, gruppo, context)
    elif azione == "carica_materiale":
        if supporto_utente:
            carica_materiale_gruppo(request, gruppo, context)
        else:
            context["error"] = "Devi supportare il gruppo per caricare materiali."


def gestisci_post_admin(request, admin, gestisce_gruppo, gruppo, context):
    azione = request.POST.get("azione")
    richiesta_id = request.POST.get("richiesta_id")

    if azione == "entra_gestione":
        entra_come_admin_gruppo(admin, gruppo, context)
        return

    if not gestisce_gruppo:
        context["error"] = "Non sei autorizzato a gestire le richieste di questo gruppo"
    elif azione == "accetta_partecipazione":
        accetta_partecipazione_gruppo(richiesta_id, gruppo, context)
    elif azione == "rifiuta_partecipazione":
        rifiuta_partecipazione_gruppo(richiesta_id, gruppo, context)
    elif azione == "carica_materiale":
        carica_materiale_gruppo(request, gruppo, context)
    elif azione == "modifica_link_chat":
        gruppo.link_chat = (request.POST.get("link_chat") or "").strip()
        gruppo.save()
        context["success"] = "Link chat aggiornato correttamente."
    elif azione == "invia_notifica":
        testo = (request.POST.get("testo_notifica") or "").strip()
        context.update(notifica_inv(admin, gruppo, testo))
    elif azione == "modifica_gruppo":
        modifica_gruppo(request, gruppo, context)


def gruppi_gestiti_admin(utente):
    admin = Admin.objects.filter(admin=utente).first()
    if not admin:
        return Gestione.objects.none()

    return Gestione.objects.filter(admin=admin).select_related("id_gruppo")


# Funzione per indirizzare i profili degli utenti di un gruppo.
def crea_context_profilo(utente, ruolo):
    context = {
        "utente": utente,
        "ruolo": ruolo
    }

    if ruolo == "studente":
        studente = Studente.objects.filter(studente=utente).first()
        if not studente:
            return None, "Profilo Studente non trovato"
        context["studente"] = studente
    elif ruolo == "tutor":
        tutor = Tutor.objects.filter(tutor=utente).first()
        if not tutor:
            return None, "Profilo Tutor non trovato"
        context["tutor"] = tutor
    elif ruolo == "admin":
        admin = Admin.objects.filter(admin=utente).first()
        if not admin:
            return None, "Profilo Admin non trovato"
        context["admin"] = admin
    else:
        return None, "Ruolo non trovato"

    return context, None


# Funzioni ausiliarie per invio, ricezione e stato lettura delle notifiche.
def notifica_ric(utente):
    return Invio.objects.filter(
        destinatario=utente
    ).select_related(
        "mittente",
        "mittente__admin",
    ).order_by("-data_invio")


def notifica_lette(user):
    return Invio.objects.filter(destinatario=user, letta=False).update(letta=True)


def notifica_inv(admin, gruppo, testo):
    if not admin:
        return {"error": "Solo un admin può inviare notifiche."}

    if not gruppo:
        return {"error": "Gruppo non trovato."}

    if not Gestione.objects.filter(admin=admin, id_gruppo=gruppo).exists():
        return {"error": "Non sei autorizzato a gestire questo gruppo."}

    return crea_notifiche_gruppo(admin, gruppo, testo)


def crea_notifiche_gruppo(admin, gruppo, testo):
    if not admin:
        return {"error": "Profilo admin non trovato."}

    if not testo:
        return {"error": "Il testo della notifica non può essere vuoto."}

    studenti = Partecipazione.objects.filter(
        id_gruppo=gruppo,
        stato=True,
    ).values_list("studente__studente_id", flat=True)

    tutor = Supporto.objects.filter(
        id_gruppo=gruppo
    ).values_list("tutor__tutor_id", flat=True)

    altri_admin = Gestione.objects.filter(
        id_gruppo=gruppo
    ).exclude(
        admin=admin
    ).values_list("admin__admin_id", flat=True)

    destinatari = set(studenti) | set(tutor) | set(altri_admin)
    destinatari.discard(admin.admin_id)

    if not destinatari:
        return {"error": "Non sono presenti destinatari."}

    for destinatario_id in destinatari:
        Invio.objects.create(
            mittente=admin,
            destinatario_id=destinatario_id,
            testo=testo,
        )

    return {"success": f"Notifica inviata a {len(destinatari)} destinatari."}
