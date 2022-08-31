from django import template

from app1.models import Project_Details, Project_Module

register = template.Library()

@register.filter(name='check_data_pm')
def check_data_pm(project):
    # pro = Project_Details.objects.get(productName=product.productname)
    # print(pro.quantity, product.productquantity)
    if project.project_request == True:
        return False
    return True

@register.filter(name='change_data_pm')
def check_data_pm(project):
    # pro = Project_Details.objects.get(productName=product.productname)
    # print(pro.quantity, product.productquantity)
    project.project_request = True
    project.save()
    return True


@register.filter(name='check_data_dev')
def check_data_dev(project):
    # pro = Project_Details.objects.get(productName=product.productname)
    # print(pro.quantity, product.productquantity)
    if project.developer_request == True:
        return False
    return True

@register.filter(name='change_data_dev')
def change_data_dev(project):
    # pro = Project_Details.objects.get(productName=product.productname)
    # print(pro.quantity, product.productquantity)
    project.developer_request = True
    project.save()
    return True


@register.filter(name='check_data_tes')
def check_data_dev(project):
    # pro = Project_Details.objects.get(productName=product.productname)
    # print(pro.quantity, product.productquantity)
    if project.tester_request == True:
        return False
    return True

@register.filter(name='change_data_tes')
def change_data_dev(project):
    # pro = Project_Details.objects.get(productName=product.productname)
    # print(pro.quantity, product.productquantity)
    project.tester_request = True
    project.save()
    return True


@register.filter(name='check_progress')
def check_progress(project):
    pm = Project_Module.objects.filter(pd_id=project).count()
    if int(pm) == int(project.Project_Modules_need) and int(project.Project_Modules_need) > 0:
        return "Complete"    
    elif int(pm) >= int(project.Project_Modules_need)/2 and int(pm) < int(project.Project_Modules_need):
        return "In Progress"
    elif int(pm) <= int(project.Project_Modules_need)/2 and int(pm) >= 0:
        return "Started"
    else:
        return "Pending"
