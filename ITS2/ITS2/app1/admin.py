from django.contrib import admin

from .models import Admin,Project_manager,Developer,Tester,Project_Details,Project_Module,Project_type,StackOverFlowQuestion,StackOverFlowAnswer,Models_Chats

# Register your models here.

admin.site.register(Admin)
admin.site.register(Project_manager)
admin.site.register(Developer)
admin.site.register(Tester)
admin.site.register(Project_Details)
admin.site.register(Project_Module)
admin.site.register(Project_type)
admin.site.register(StackOverFlowAnswer)
admin.site.register(StackOverFlowQuestion)
admin.site.register(Models_Chats)
