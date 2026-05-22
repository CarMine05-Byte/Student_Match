from django.db import models
from django.db.models import ForeignKey


# Questo modello non è ancora implementato perchè non definitivo.

class Utente(models.Model):
    user = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=20)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)


class Studente(models.Model):
    studente = models.ForeignKey(Utente, primary_key=True, on_delete=models.CASCADE, related_name="Studente")
    anno_corso = models.SmallIntegerField
    corso_laurea = models.CharField(max_length=100)


class Tutor(models.Model):
    tutor = models.ForeignKey(Utente, primary_key=True, on_delete=models.CASCADE, related_name="Tutor")
    dipartimento = models.CharField(max_length=128)


class Admin(models.Model):
    admin = models.ForeignKey(Utente, primary_key=True, on_delete=models.CASCADE, related_name="Admin")
    livello = models.SmallIntegerField


class Esame(models.Model):
    nome_esame = models.CharField(primary_key=True, max_length=50)
    corso = models.CharField(max_length=100)
    anno_corso = models.SmallIntegerField
    semestre = models.SmallIntegerField
    cfu = models.SmallIntegerField

class Svolgimento(models.Model):
    user = models.ForeignKey(Utente, primary_key=True, on_delete=models.CASCADE, related_name="utente_successo")
    nome_esame = models.ForeignKey(Esame, primary_key=True, on_delete=models.CASCADE, related_name="esame_svolto")

class Materiale(models.Model):
    id_materiale = models.AutoField
    nome_file = models.CharField(max_length=150)
    tipo = models.CharField(max_length=5)

    file = models.FileField(upload_to='materiali/', blank=True, null=True, default=None)

    url = models.URLField(blank = True, default=None, null=True)
    data_caricamento = models.DateField


class Gruppo(models.Model):
    id_gruppo = models.SmallAutoField(primary_key=True)
    nome_gruppo = models.CharField(max_length=50)
    chat = models.TextField
    descrizione = models.TextField
    max_partecipanti = models.SmallIntegerField(max_length=100)
    id_materiale = models.ForeignKey(Materiale, on_delete=models.CASCADE, related_name="materiale_associato")

class Assegnazione(models.Model):
    nome_esame = models.ForeignKey(Esame, primary_key=True, on_delete=models.CASCADE, related_name="esame_gruppo")
    id_gruppo  = models.ForeignKey(Gruppo, primary_key=True, on_delete=models.CASCADE, related_name="gruppo_esame")

class Partecipazione(models.Model):
    user = models.ForeignKey(Utente, primary_key=True, on_delete=models.CASCADE, related_name="utente_partecipante")
    id_gruppo = models.ForeignKey(Gruppo, primary_key=True, on_delete=models.CASCADE, related_name="gruppo_utente")
    data_iscrizione = models.DateField
    stato = models.BooleanField(default=False)

class Notifica(models.Model):
    id_notifica = models.SmallAutoField(primary_key=True)
    messaggio = models.TextField(max_length=50)
    visuale = models.BooleanField(default=False)
    data_invio = models.TimeField
    id_user = ForeignKey(Utente, on_delete=models.CASCADE, related_name="notifica_utente")

