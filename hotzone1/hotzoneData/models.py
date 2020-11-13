from django.db import models

class Patient(models.Model):
    patient_name = models.CharField(max_length=100)
    identify_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    def __str__(self):
        return str(self.identify_number) + ' ' + self.patient_name

class Disease(models.Model):
    disease_name = models.CharField(max_length=20)
    virus = models.CharField(max_length=20)
    max_infectious_period = models.IntegerField()
    curr_case_number = models.IntegerField()
    def __str__(self):
        return self.disease_name

class Place(models.Model):
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True)
    x_coor = models.IntegerField()
    y_coor = models.IntegerField()
    def __str__(self):
        return self.location

class Case(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    case_number = models.IntegerField()
    date_confirmed = models.DateField()
    is_local = models.BooleanField()
    def __str__(self):
        return self.disease.disease_name + ' ' + str(self.case_number) + ': ' + str(self.patient.patient_name)

class CasePlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    RESIDENCE = 'Residence'
    WORKPLACE = 'Workplace'
    VISIT = 'Visit'
    CAT_CHOICES = [(RESIDENCE, RESIDENCE), (WORKPLACE, WORKPLACE), (VISIT, VISIT)]
    category = models.CharField(max_length=9, choices=CAT_CHOICES, default=VISIT)
