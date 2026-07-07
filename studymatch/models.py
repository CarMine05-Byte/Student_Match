from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from django.core.exceptions import ValidationError

class Utente(models.Model):
    utente = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    ruolo = models.CharField(max_length=20, default="studente")
    nome = models.CharField(max_length=50, null=True)
    cognome = models.CharField(max_length=50, null=True)


class Studente(models.Model):
    studente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="studente_profile")
    anno_corso = models.SmallIntegerField(default=0)
    corso_laurea = models.CharField(max_length=100)


class Tutor(models.Model):
    tutor = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="tutor_profile")
    dipartimento = models.CharField(max_length=128)
    area_competenza = models.CharField(max_length=128)
    laurea = models.CharField(max_length=100, null=True, blank=True, default=1)


class Admin(models.Model):
    admin = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="admin_profile")
    livello = models.SmallIntegerField(default=1)
    data_nomina = models.DateField(default=timezone.now)


class Esame(models.Model):
    id_esame = models.SmallAutoField(primary_key=True)
    nome_esame = models.CharField(max_length=50)
    corso = models.CharField(max_length=100)
    anno = models.SmallIntegerField(default=1)
    semestre = models.SmallIntegerField(default=0)
    cfu = models.SmallIntegerField(default=0)


class Gruppo(models.Model):
    id_gruppo = models.SmallAutoField(primary_key=True)
    nome_gruppo = models.CharField(max_length=50)
    chat = models.TextField(null=True, blank=True)
    descrizione = models.TextField(null=True, blank=True)
    max_partecipanti = models.SmallIntegerField(default=5)


class Materiale(models.Model):
    id_materiale = models.AutoField(primary_key=True)
    nome_file = models.CharField(max_length=150)
    tipo = models.CharField(max_length=5)

    file = models.FileField(upload_to='materiali/', null=True, default=None)
    url = models.URLField(default=None, null=True)
    data_caricamento = models.DateField(auto_now_add=True)
    id_gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name="gruppo_associato")


class Notifica(models.Model):
    id_notifica = models.SmallAutoField(primary_key=True)
    messaggio = models.TextField(max_length=50)
    visuale = models.BooleanField(default=False)
    data_invio = models.TimeField(default=timezone.now)
    utente = ForeignKey(Utente, on_delete=models.CASCADE, related_name="notifica_utente")
    admin = ForeignKey(Admin, on_delete=models.CASCADE, related_name="notifica_admin")


class Partecipazione(models.Model):
    studente = models.ForeignKey(Studente, on_delete=models.CASCADE, related_name="utente_gruppo")
    id_gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name="gruppo_utente")
    data_iscrizione = models.DateField(auto_now_add=True)
    stato = models.BooleanField(default=False)

    class Meta:
        unique_together = ('studente', 'id_gruppo')


class Supporto(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="tutor_gruppo")
    id_gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name="gruppo_tutor")
    punteggio = models.IntegerField(null=True, blank=True)
    stato = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tutor', 'id_gruppo')


class Gestione(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name="admin_gruppo")
    id_gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name="gruppo_admin")

    class Meta:
        unique_together = ('admin', 'id_gruppo')


class Svolgimento(models.Model):
    studente = models.ForeignKey(Studente, on_delete=models.CASCADE, related_name="studente_successo")
    id_esame = models.ForeignKey(Esame, on_delete=models.CASCADE, related_name="esame_svolto")
    data_svolgimento = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('studente', 'id_esame')


class Assegnazione(models.Model):
    id_esame = models.ForeignKey(Esame, on_delete=models.CASCADE, related_name="esame_gruppo")
    id_gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name="gruppo_esame")
    periodo = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('id_esame', 'id_gruppo')
