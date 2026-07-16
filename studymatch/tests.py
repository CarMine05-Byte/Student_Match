from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Assegnazione, Esame, Gruppo, Partecipazione, Studente, Utente


class DettaglioGruppoAccessTests(TestCase):
    def setUp(self):
        self.utente = Utente.objects.create(
            utente="mario",
            email="mario@example.com",
            password="password",
            ruolo="studente",
        )
        self.studente = Studente.objects.create(
            studente=self.utente,
            anno_corso=1,
            corso_laurea="Informatica",
        )

        session = self.client.session
        session["user"] = self.utente.utente
        session["ruolo"] = self.utente.ruolo
        session.save()

    def crea_gruppo(self, corso, anno_corso):
        esame = Esame.objects.create(
            nome_esame="Programmazione",
            corso=corso,
            anno_corso=anno_corso,
            semestre=1,
            cfu=9,
        )
        gruppo = Gruppo.objects.create(
            nome_gruppo=f"Gruppo {corso}",
            descrizione="Gruppo di studio",
            max_partecipanti=5,
        )
        Assegnazione.objects.create(
            id_esame=esame,
            id_gruppo=gruppo,
            periodo=timezone.now() + timedelta(days=7),
        )

        return gruppo

    def test_studente_non_partecipante_e_non_compatibile_torna_alla_home_con_errore(self):
        gruppo = self.crea_gruppo(corso="Matematica", anno_corso=2)

        response = self.client.get(
            reverse("dettaglio_gruppo", args=[gruppo.id_gruppo])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Non puoi accedere a questo gruppo")

    def test_studente_non_partecipante_ma_compatibile_vede_il_dettaglio(self):
        gruppo = self.crea_gruppo(corso="Informatica", anno_corso=1)

        response = self.client.get(
            reverse("dettaglio_gruppo", args=[gruppo.id_gruppo])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dettaglio_gruppo.html")
        self.assertContains(response, gruppo.nome_gruppo)

    def test_studente_partecipante_vede_il_dettaglio_anche_se_non_compatibile(self):
        gruppo = self.crea_gruppo(corso="Matematica", anno_corso=2)
        Partecipazione.objects.create(
            studente=self.studente,
            id_gruppo=gruppo,
            stato=False,
        )

        response = self.client.get(
            reverse("dettaglio_gruppo", args=[gruppo.id_gruppo])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dettaglio_gruppo.html")
        self.assertContains(response, gruppo.nome_gruppo)
