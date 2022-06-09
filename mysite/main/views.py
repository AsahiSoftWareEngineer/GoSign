from django.shortcuts import render, redirect
from django.views import generic
from django.core.mail import send_mail
import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from .backend import Database
# Create your views here.

class Check(generic.TemplateView):
    
    def post(self, request, *args, **kwargs):
        token = self.kwargs["agreement_id"]
        mail_address:str = request.POST['email']
        subject = "電子署名の本人確認"
        url = "http://127.0.0.1:8000/main/certificate/"+token+"/"
        message = url
        from_email = mail_address
        recipient_list = [mail_address]
        send_mail(subject, message, from_email, recipient_list)
        Database("mail").migrate_data([token, mail_address])
        return redirect("main:confirm")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs["agreement_id"]
        data = Database("preview").get_data([id])
        return_data = {
            "file":data["file_name"],
        }
        return render(request, 'check.html', return_data)



class Confirm(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'confirm.html')
    

class CreateView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "create.html")
    
    def post(self, request, *args, **kwargs):
        data = {}
        data["agreement_name"] = request.POST["agreement_name"]
        data["client_name"] = request.POST["client_name"]
        data["client_name"] = request.POST["client_name"]
        data["host_name"] = request.POST["host_name"]
        data["host_user_name"] = request.POST["host_user_name"]
        data["file_name"] = request.FILES.get('pdf_file')
        db = Database("base")
        db.insert(data)
        return redirect("main:list")
    
class ListView(LoginRequiredMixin, generic.TemplateView):
    def post(self, request, *args, **kwargs):
        type = request.POST["type"]
        if (type == "delete"):
            id = request.POST["id"]
            Database('base').delete_data([id])
        return redirect("main:list")
    
    def get(self, request, *args, **kwargs):
        list_data = Database("base").get_data([])
        return_data = {
            "agreement_list": list_data
        }
        return render(request, "list.html", return_data)

class PreView(LoginRequiredMixin, generic.TemplateView):
    def post(self, request, *args, **kwargs):
        type = request.POST["type"]
        id = self.kwargs["agreement_id"]
        if (type == "date"):
            Database("host_certificate_date").migrate_data([id])
            pass
        return redirect("main:agreement", id)
    

    def get(self, request, *args, **kwargs):
        id = self.kwargs["agreement_id"]
        data = Database("preview").get_data([id])
        return_data = {
            "agreement_id": data["agreement_id"],
            "agreement_name": data["agreement_name"],
            "host_user_name": data["host_user_name"],
            "host_name": data["host_name"],
            "mail_address": data["mail_address"],
            "client_name": data["client_name"],
            "client_user_name": data["client_user_name"],
            "file": data["file_name"], 
            "client_agreement_date": data["client_agreement_date"],
            "host_agreement_date": data["host_agreement_date"]
        }
        return render(request, "preview.html", return_data)
    pass

class Certificate(generic.TemplateView):
    def post(self, request, *args, **kwargs):
        id = self.kwargs["agreement_id"]
        client_user_name = request.POST["client_user_name"]
        Database("date").migrate_data([id])
        Database("client_user_name").migrate_data([id, client_user_name])
        return redirect("main:complete")
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs["agreement_id"]
        data = Database("preview").get_data([id])
        return_data = {
            "file": data["file_name"]
        }
        return render(request, "certificate.html", return_data)

class CompleteView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "complete.html")
