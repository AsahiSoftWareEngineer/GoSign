from .models import List
import secrets
import datetime
class Database:
    def __init__(self, table_name):
        self.table_name:str = table_name
    def insert(self, data):
        if(self.table_name == "base"):
            agreement_id = str(secrets.token_hex())
            db = List(
                agreement_id=agreement_id, 
                agreement_name=data["agreement_name"], 
                client_name=data["client_name"],
                client_user_name="None",
                host_name=data["host_name"],
                host_user_name=data["host_user_name"],
                mail_address="None",
                client_agreement_date="None",
                host_agreement_date="None",
                file_name=data["file_name"],
                )
            db.save()
        
    def get_data(self, data):
        if (self.table_name == "base"):
            data = List.objects.all()
            name_list = []
            id_list = []
            for i in data:
                name_list.append(i.agreement_name)
                id_list.append(i.agreement_id)
            return zip(id_list, name_list)
            pass
        elif(self.table_name == "preview"):
            data = List.objects.filter(agreement_id=data[0])
            data_dict = {}
            for i in data:
                data_dict["agreement_id"] = i.agreement_id
                data_dict["agreement_name"] = i.agreement_name
                data_dict["client_name"] = i.client_name
                data_dict["client_user_name"] = i.client_user_name
                data_dict["host_name"] = i.host_name
                data_dict["host_user_name"] = i.host_user_name
                data_dict["mail_address"] = i.mail_address
                data_dict["client_agreement_date"] = i.client_agreement_date
                data_dict["host_agreement_date"] = i.host_agreement_date
                data_dict["file_name"] = str(i.file_name)
            return data_dict
    
    def delete_data(self, data):
        if (self.table_name == "base"):
            data = List.objects.filter(agreement_id=data[0])
            data.delete()
        pass
    
    def migrate_data(self, data):
        t_delta = datetime.timedelta(hours=9)
        if (self.table_name == "mail"):
            db = List.objects.get(agreement_id=data[0])
            db.mail_address = data[1]
            db.save()
        elif(self.table_name == "date"):
            date = datetime.datetime.now(datetime.timezone(t_delta, 'JST')).strftime("%Y/%m/%d-%H:%M:%s")
            db = List.objects.get(agreement_id=data[0])
            db.client_agreement_date = date
            db.save()
        elif(self.table_name == "client_user_name"):
            db = List.objects.get(agreement_id=data[0])
            db.client_user_name = data[1]
            db.save()
        elif(self.table_name == "host_certificate_date"):
            date = datetime.datetime.now(datetime.timezone(t_delta, 'JST')).strftime("%Y/%m/%d-%H:%M:%S")
            db = List.objects.get(agreement_id=data[0])
            db.host_agreement_date = date
            db.save()
                
                
                
                
                
        