from django.db import models

class Student(models.Model):
    id_student = models.AutoField(primary_key=True)
    email = models.CharField(max_length=150)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=150)
    year_course = models.SmallIntegerField(max_length=5)

class Exam(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    course = models.CharField(max_length=50)
    year_course = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="anno_corso")
    semester = models.SmallIntegerField(max_length=2)
    cfu = models.SmallIntegerField(max_length=1000)

class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField
    date_creation = models.DateField
    max = models.SmallIntegerField
    id_exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="Esami in palio")
    id_creator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="Relatore")


class Participate(models.Model):
    id_participate = models.AutoField(primary_key=True)
    id_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studente_partecipante")
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="Gruppo Riferito")
    date_registration = models.DateField
    state = models.BooleanField(default=False)

