from django.db import models

class Base(models.Model):
    agreement_id = models.TextField()
    agreement_name = models.TextField()
    client_name = models.TextField()
    client_user_name = models.TextField()
    host_name = models.TextField()
    host_user_name = models.TextField()
    mail_address = models.TextField()
    client_agreement_date = models.TextField()
    host_agreement_date = models.TextField()
    file_name = models.FileField(upload_to='pdf/')
    
    