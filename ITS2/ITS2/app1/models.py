from django.db import models

# Create your models here.

class Project_type(models.Model):
    Type_name = models.CharField(default="",max_length=15)
    Type_Details = models.TextField(default="")

    def __str__(self):
        return self.Type_name

class Admin(models.Model):
    Username = models.CharField(default="",max_length=15)
    Password = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.Username

Genders = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

class Project_manager(models.Model):
    Name = models.CharField(default="",max_length=50)
    profile_pic = models.ImageField(upload_to="PmImgs/",max_length=300,null=True,blank=True)
    Gender = models.CharField(max_length=20,choices=Genders,default = '1')
    Email = models.EmailField(default="",max_length=100)
    Mno = models.CharField(default="",max_length=100)
    Address = models.TextField(default="")
    Password = models.CharField(max_length=100, default="")
   
    def __str__(self):
        return self.Name

class Developer(models.Model):
    Name = models.CharField(default="",max_length=50)
    profile_pic = models.ImageField(upload_to="DevImgs/",max_length=300,null=True,blank=True)
    Gender = models.CharField(max_length=20,choices=Genders,default = '1')
    Email = models.EmailField(default="",max_length=100)
    Mno = models.CharField(default="",max_length=100)
    Address = models.TextField(default="")
    Password = models.CharField(max_length=100, default="")
   

    def __str__(self):
        return self.Name

class Tester(models.Model):
    Name = models.CharField(default="",max_length=50)
    profile_pic = models.ImageField(upload_to="TestImgs/",max_length=300,null=True,blank=True)
    Gender = models.CharField(max_length=20,choices=Genders,default = '1')
    Email = models.EmailField(default="",max_length=100)
    Mno = models.CharField(default="",max_length=100)
    Address = models.TextField(default="")
    Password = models.CharField(max_length=100, default="")
   

    def __str__(self):
        return self.Name

class Project_Details(models.Model):
    Pm_id = models.ForeignKey("Project_manager", default="",on_delete=models.CASCADE)
    dev_id = models.ForeignKey("Developer", default="",on_delete=models.CASCADE,blank=True, null=True)
    tset_id = models.ForeignKey("Tester", default="",on_delete=models.CASCADE,blank=True, null=True)
    Pt_id = models.ForeignKey("Project_type", default="",on_delete=models.CASCADE)
    Project_Name = models.CharField(default="",max_length=150)
    Project_Detail = models.CharField(default="",max_length=500)
    Project_Modules_need = models.PositiveIntegerField(default=0)
    Project_Modules_Done = models.PositiveIntegerField(default=0)
    Project_Progress = models.CharField(default="Pending",max_length=100)
    Date = models.DateField(auto_now=True, blank=True, null=True)
    project_request = models.BooleanField(default = False)
    developer_request = models.BooleanField(default = False)
    tester_request = models.BooleanField(default = False)
    
    def __str__(self):
        return self.Project_Name

class Project_Module(models.Model):
    pd_id = models.ForeignKey("Project_Details", default="",on_delete=models.CASCADE)
    Module_Name = models.CharField(default="",max_length=150)
    Module_Detail = models.CharField(default="",max_length=500)
    Progress = models.PositiveIntegerField(default=0)
    Date = models.DateField(auto_now=True, blank=True, null=True)
    Pm_id = models.ForeignKey("Project_manager", default="",on_delete=models.CASCADE,blank=True, null=True)
    developer =  models.ForeignKey("Developer",on_delete=models.CASCADE,null=True,blank=True)
    tester =  models.ForeignKey("Tester",on_delete=models.CASCADE,null=True,blank=True)
    developer_request =  models.BooleanField(default=False)
    tester_request =  models.BooleanField(default=False)
    def __str__(self):
        return self.Module_Name
        
        
class StackOverFlowQuestion(models.Model):
    pmanage = models.ForeignKey("Project_manager", default="",on_delete=models.CASCADE,blank=True, null=True)
    devl = models.ForeignKey("Developer", default="",on_delete=models.CASCADE,blank=True, null=True)
    tset = models.ForeignKey("Tester", default="",on_delete=models.CASCADE,blank=True, null=True)
    Question = models.CharField(default="",max_length=500)
    date_add = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    
    def __str__(self):
        return self.Question

class StackOverFlowAnswer(models.Model):
    pmanage = models.ForeignKey("Project_manager", default="",on_delete=models.CASCADE,blank=True, null=True)
    devl = models.ForeignKey("Developer", default="",on_delete=models.CASCADE,blank=True, null=True)
    tset = models.ForeignKey("Tester", default="",on_delete=models.CASCADE,blank=True, null=True)
    Questions = models.ForeignKey("StackOverFlowQuestion", default="",on_delete=models.CASCADE,blank=True, null=True)
    Answer = models.TextField(default="")
    Answer_doc = models.FileField(upload_to="SOFA/", max_length=300,default="",blank=True, null=True)
    date_add = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    
    def __str__(self):
        return self.Answer

class Models_Chats(models.Model):
    proj = models.ForeignKey("Project_Details", default="",on_delete=models.CASCADE,blank=True, null=True)
    mod = models.ForeignKey("Project_Module", default="",on_delete=models.CASCADE,blank=True, null=True)
    devl = models.ForeignKey("Developer", default="",on_delete=models.CASCADE,blank=True, null=True)
    tset = models.ForeignKey("Tester", default="",on_delete=models.CASCADE,blank=True, null=True)
    problem_text = models.TextField(default="")
    date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    chat_doc = models.FileField(upload_to="Chats/", max_length=300,default="",blank=True, null=True)
    
    
