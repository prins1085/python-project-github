from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admin, Project_manager, Developer,Tester, Project_Details, Project_Module,Project_type,StackOverFlowQuestion,StackOverFlowAnswer,Models_Chats

# mesasges
from django.contrib import messages

# Gerate OTP
import random

# SMPT Email Send
import smtplib 
import email.message
# Create your views here.

# Html To Pdf -------------------

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.views.generic import View

import pdfkit

# Html To Pdf ------------------- 


def Home_Page(request):
    return render(request,"Home_page.html")


def Admin_login(request):
    if request.POST:
        unm = request.POST['username']
        ps = request.POST['password']
        print(unm,ps)

        # try:
        data = Admin.objects.get(Username = unm)
        if data.Password == ps:
            # request.session['checking'] = data.Email
            request.session['admin'] = data.Username
            return redirect('admindash')
        else:
            messages.add_message(request, messages.ERROR, "Your data is not match")
            return redirect('adminlogin')
        # except:
        #     messages.add_message(request, messages.ERROR, "Your data is not match")
        #     return redirect('adminlogin')
    return render(request,'admin_login.html')

def admin_dashboard(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        pt = Project_type.objects.all()
        pd = Project_Details.objects.all()
        return render(request,'admin_dashboard.html',{'aduser':ad,'pt':pt,'pd':pd})
    else:
        return redirect('homepage')

def Admin_Logout(request):
    if 'admin' in request.session.keys():
        del request.session['admin']
        return redirect('homepage')
    else:
        return redirect('homepage')

def Admin_Report_Generate(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        pd = Project_Details.objects.all()
        return render(request,'Admin_Report_Generate.html',{'my_template':'adminbase.html','aduser':ad,'pd':pd})
    else:
        return redirect('homepage')
    
def PM_Report_Generate(request):
    if 'p_manager' in request.session.keys():
        data = request.session['p_manager']
        pm = Project_manager.objects.get(Email = data)
        pd = Project_Details.objects.filter(Pm_id=pm)
        return render(request,'Admin_Report_Generate.html',{'my_template':"PMbase.html",'datapm':pm,'pd':pd})
    else:
        return redirect('homepage')

def Dev_Report_Generate(request):
    if "developer" in request.session.keys():
        data = request.session['developer']
        pm = Developer.objects.get(Email = data)
        pd = Project_Details.objects.filter(dev_id=pm)
        return render(request,'Admin_Report_Generate.html',{'my_template':"Devbase.html",'datadev':pm,'pd':pd})
    else:
        return redirect('homepage')

def Tes_Report_Generate(request):
    if "tester" in request.session.keys():
        data = request.session['tester']
        pm = Tester.objects.get(Email = data)
        pd = Project_Details.objects.filter(tset_id=pm)
        return render(request,'Admin_Report_Generate.html',{'my_template':"Testerbase.html",'datates':pm,'pd':pd})
    else:
        return redirect('homepage')    

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def Admin_Report(request,id):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        pd = Project_Details.objects.get(id=id)
        pm = Project_Module.objects.filter(pd_id=pd)
        # return render(request,'Admin_Report.html',)
        data = {'aduser':ad,'pm':pm,'pd':pd}
        pdf = render_to_pdf('Admin_Report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    if 'p_manager' in request.session.keys():
        data = request.session['p_manager']
        ad = Project_manager.objects.get(Email = data)
        pd = Project_Details.objects.get(id=id)
        pm = Project_Module.objects.filter(pd_id=pd)
        # return render(request,'Admin_Report.html',)
        data = {'aduser':ad,'pm':pm,'pd':pd}
        pdf = render_to_pdf('Admin_Report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    if "developer" in request.session.keys():
        data = request.session['developer']
        ad = Developer.objects.get(Email = data)
        pd = Project_Details.objects.get(id=id)
        pm = Project_Module.objects.filter(pd_id=pd)
        # return render(request,'Admin_Report.html',)
        data = {'aduser':ad,'pm':pm,'pd':pd}
        pdf = render_to_pdf('Admin_Report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    if "tester" in request.session.keys():
        data = request.session['tester']
        ad = Tester.objects.get(Email = data)
        pd = Project_Details.objects.get(id=id)
        pm = Project_Module.objects.filter(pd_id=pd)
        # return render(request,'Admin_Report.html',)
        data = {'aduser':ad,'pm':pm,'pd':pd}
        pdf = render_to_pdf('Admin_Report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('homepage')


def PM_login(request):
    if request.POST:
        em = request.POST['semail']
        ps = request.POST['spass']
        print(em,ps)

        try:
            data = Project_manager.objects.get(Email = em)
            if data.Password == ps:
                # request.session['checking'] = data.Email
                request.session['p_manager'] = data.Email
                return redirect('spmdash')
            else:
                return redirect('homepage')
        except:
            try:
                data = Developer.objects.get(Email = em)
                if data.Password == ps:
                    # request.session['checking'] = data.Email
                    request.session['developer'] = data.Email
                    return redirect('sdevdash')
                else:
                    return redirect('homepage')
            except:
                try:
                    data = Tester.objects.get(Email = em)
                    if data.Password == ps:
                        # request.session['checking'] = data.Email
                        request.session['tester'] = data.Email
                        return redirect('stestdash')
                    else:
                        return redirect('homepage')
                except:
                    return redirect('homepage')

    return render(request,'PM_Login.html')

def PM_Dashboard(request):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        if request.POST:
            # pm_id = request.session.get('p_manager')
            Name = request.POST['name']
            Details = request.POST['detail']
            
            obj = Project_Details()
            a = pm
            obj.Pm_id = a
            obj.Project_Name = Name
            obj.Project_Detail = Details
            obj.save()
        
        pdata = Project_Details.objects.filter(Pm_id=pm)
        mdata = Project_Module.objects.filter(Pm_id=pm)
        return render(request,'pm_dashboard.html',{'my_template':"PMbase.html",'pdata':pdata,'mdata':mdata,'datapm':pm})
    else:
        return redirect('homepage')

def PMAdd_ProjectDetails(request):
    return render(request,'')

def Pm_Logout(request):
    if 'p_manager' in request.session.keys():
        del request.session['p_manager']
        return redirect('homepage')
    else:
        return redirect('homepage')


def Developer_login(request):
    if request.POST:
        em = request.POST['semail']
        ps = request.POST['spass']
        print(em,ps)

        try:
            data = Developer.objects.get(Email = em)
            if data.Password == ps:
                # request.session['checking'] = data.Email
                request.session['developer'] = data.Email
                return redirect('sdevdash')
            else:
                return redirect('homepage')
        except:
            return redirect('homepage')
    return render(request,'Developer_Login.html')

def Developer_Dashboard(request):
    if "developer" in request.session.keys():
        print("!")
        dev = Developer.objects.get(Email=request.session['developer'])
        mdata = Project_Module.objects.filter(developer=dev)
        pdata = Project_Details.objects.filter(dev_id=dev)
        # pdata = set()
        # for i in mdata:
        #     pdata.add(i.pd_id.id)
        # pdata_list = list(pdata)
        # pdata_list.sort()
        # pata = []
        # for i in pdata_list:
        #     pata.append()
        # print(pata)
        # print(pdata)
        return render(request,'developer_dashboard.html',{'pata':pdata,'my_template': "Devbase.html",'mdata':mdata,"dev_nm":dev,'datadev':dev})
    else:
        return redirect('homepage')

def Developer_Logout(request):
    if "developer" in request.session.keys():
        del request.session['developer']
        return redirect('homepage')
    else:
        return redirect('homepage')


def Tester_login(request):
    if request.POST:
        em = request.POST['semail']
        ps = request.POST['spass']
        print(em,ps)

        try:
            data = Tester.objects.get(Email = em)
            if data.Password == ps:
                # request.session['checking'] = data.Email
                request.session['tester'] = data.Email
                return redirect('stestdash')
            else:
                return redirect('homepage')
        except:
            return redirect('homepage')
    return render(request,'Tester_Login.html')

def Tester_Dashboard(request):
    if "tester" in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        mdata = Project_Module.objects.filter(tester=tes)
        pdata = set()
        for i in mdata:
            pdata.add(i.pd_id.id)
        pdata_list = list(pdata)
        pdata_list.sort()
        pata = []
        for i in pdata_list:
            pata.append(Project_Details.objects.get(id=int(i),tset_id=tes))
        print(pata)
        print(pdata)
        return render(request,'Tester_dashboard.html',{'pata':pata,'my_template': "Testerbase.html",'mdata':mdata,"tes_nm":tes,'datates':tes})
    else:
        return redirect('homepage')

def Tester_Logout(request):
    if "tester" in request.session.keys():
        del request.session['tester']
        return redirect('homepage')
    else:
        return redirect('homepage')

    
def manage_staff(request):
    return render(request,'manage_staff.html')

def manage_project(request):
    pt = Project_type.objects.all()
    pd = Project_Details.objects.all()
    return render(request,'manage_project.html',{'pt':pt,'pd':pd})

def add_pm(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']

            print(sname,sgen,semail,sno,saddress,spass)

            obj = Project_manager()
            obj.Name = sname
            obj.Gender = sgen
            obj.Email = semail
            obj.Mno = sno
            obj.Address = saddress
            obj.Password = spass
            obj.save()
            
            # Send OTP Email
            sender_email = "harkhaniprins2001@gmail.com"
            sender_pass = "108510851085"
            receiver_email = str(semail)
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            Email_Message = f"""
            
            Dear {sname},
            This is Your New Username is : {semail}
            and Password is : {spass}
            
            Thank You...
            """
            
            msg = email.message.Message()
            msg['Subject'] = "New Project Manager Registerd"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            password = sender_pass

            msg.add_header('Content-Type','text/html')
            msg.set_payload(Email_Message)

            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
            print('Email Sent....')

            return redirect('viewdetails')
        return render(request,'add_pm.html',{'aduser':ad})
    else:
        return redirect('adminlogin')

def add_developer(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']

            print(sname,sgen,semail,sno,saddress,spass)

            obj = Developer()
            obj.Name = sname
            obj.Gender = sgen
            obj.Email = semail
            obj.Mno = sno
            obj.Address = saddress
            obj.Password = spass
            obj.save()
            
            # Send OTP Email
            sender_email = "harkhaniprins2001@gmail.com"
            sender_pass = "108510851085"
            receiver_email = str(semail)
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            Email_Message = f"""
            
            Dear {sname},
            This is Your New Username is : {semail}
            and Password is : {spass}
            
            Thank You...
            """
            
            msg = email.message.Message()
            msg['Subject'] = "New Developer Registerd"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            password = sender_pass

            msg.add_header('Content-Type','text/html')
            msg.set_payload(Email_Message)

            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
            print('Email Sent....')
            
            
            return redirect('viewdetails')
        return render(request,'add_dev.html',{'aduser':ad,'my_template':'adminbase.html'})
    else:
        return redirect('adminlogin')

def add_tester(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']

            print(sname,sgen,semail,sno,saddress,spass)

            obj = Tester()
            obj.Name = sname
            obj.Gender = sgen
            obj.Email = semail
            obj.Mno = sno
            obj.Address = saddress
            obj.Password = spass
            obj.save()
            
            # Send OTP Email
            sender_email = "harkhaniprins2001@gmail.com"
            sender_pass = "108510851085"
            receiver_email = str(semail)
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            Email_Message = f"""
            
            Dear {sname},
            This is Your New Username is : {semail}
            and Password is : {spass}
            
            Thank You...
            """
            
            msg = email.message.Message()
            msg['Subject'] = "New Tester Registerd"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            password = sender_pass

            msg.add_header('Content-Type','text/html')
            msg.set_payload(Email_Message)

            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
            print('Email Sent....')
            
            
            return redirect('viewdetails')
        return render(request,'add_test.html',{'aduser':ad})
    else:
        return redirect('adminlogin')

def PM_Registeration(request):
    if request.POST:
        sname = request.POST['sname']
        sgen = request.POST['sgen']
        semail = request.POST['semail']
        sno = request.POST['sno']
        saddress = request.POST['saddress']
        spass = request.POST['spass']

        print(sname,sgen,semail,sno,saddress,spass)

        obj = Project_manager()
        obj.Name = sname
        obj.Gender = sgen
        obj.Email = semail
        obj.Mno = sno
        obj.Address = saddress
        obj.Password = spass
        obj.save()
        return redirect('homepage')
    
    return render(request,'PM_Regi.html')

def view_details(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        pm = Project_manager.objects.all()
        dev = Developer.objects.all()
        test = Tester.objects.all()
        return render(request,'view_details.html',{'aduser':ad,'pm':pm , 'dev':dev , 'test':test})
    else:
        return redirect('homepage')

def PM_delete(request,id):
    if 'admin' in request.session.keys():
        data = Project_manager.objects.get(id = id)
        data.delete()
        return redirect('viewdetails')
    else:
        return redirect('homepage')

def PM_update(request,id):
    if 'admin' in request.session.keys():
        data = Project_manager.objects.get(id = id)
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']

            data.Name = sname
            data.Gender = sgen
            data.Email = semail
            data.Mno = sno
            data.Address = saddress
            data.Password = spass
            data.save()
            return redirect('viewdetails')
        return render(request,'PM_update.html',{'data':data,'my_template':'adminbase.html'})
    else:
        return redirect('homepage')
    
def Dev_delete(request,id):
    if 'admin' in request.session.keys():
        data = Developer.objects.get(id = id)
        data.delete()   
        return redirect('viewdetails')
    else:
        return redirect('homepage')

def Dev_update(request,id):
    if 'admin' in request.session.keys():
        data = Developer.objects.get(id = id)
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']

            data.Name = sname
            data.Gender = sgen
            data.Email = semail
            data.Mno = sno
            data.Address = saddress
            data.Password = spass
            data.save()
            return redirect('viewdetails')
        return render(request,'Dev_update.html',{'data':data,'my_template':'adminbase.html'})
    else:
        return redirect('admindash')

def Test_delete(request,id):
    if 'admin' in request.session.keys():
        data = Tester.objects.get(id = id)
        data.delete()  
        return redirect('viewdetails')
    else:
        return redirect('viewdetails')

def Test_update(request,id):
    if 'admin' in request.session.keys():
        data = Tester.objects.get(id = id)
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']

            data.Name = sname
            data.Gender = sgen
            data.Email = semail
            data.Mno = sno
            data.Address = saddress
            data.Password = spass
            data.save()
            return redirect('viewdetails')
        return render(request,'Test_update.html',{'data':data,'my_template':'adminbase.html'})
    else:
        return redirect('admindash')

def Developer_Registeration(request):
    if request.POST:
        sname = request.POST['sname']
        sgen = request.POST['sgen']
        semail = request.POST['semail']
        sno = request.POST['sno']
        saddress = request.POST['saddress']
        spass = request.POST['spass']

        print(sname,sgen,semail,sno,saddress,spass)

        obj = Developer()
        obj.Name = sname
        obj.Gender = sgen
        obj.Email = semail
        obj.Mno = sno
        obj.Address = saddress
        obj.Password = spass
        obj.save()
        return redirect('homepage')
    
    return render(request,'Developer_Regi.html')

def Tester_Registeration(request):
    if request.POST:
        sname = request.POST['sname']
        sgen = request.POST['sgen']
        semail = request.POST['semail']
        sno = request.POST['sno']
        saddress = request.POST['saddress']
        spass = request.POST['spass']

        print(sname,sgen,semail,sno,saddress,spass)

        obj = Tester()
        obj.Name = sname
        obj.Gender = sgen
        obj.Email = semail
        obj.Mno = sno
        obj.Address = saddress
        obj.Password = spass
        obj.save()
        return redirect('homepage')
    
    return render(request,'Tester_Regi.html')

def PM_forget_password(request):
    if request.POST:
        em = request.POST['email']

        try:
            data = Project_manager.objects.get(Email = em)
            print(data.Email)
            # OTP Genrate
            otp_no = ""
            for i in range(6):
                no = random.randint(0,9)
                otp_no += str(no)
            print(otp_no)

            # Send OTP Email
            sender_email = "harkhaniprins2001@gmail.com"
            sender_pass = "108510851085"
            receiver_email = data.Email
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            Email_Message = f"""
            This Is Your OTP Don't Share With Others
            OTP = {otp_no}
            
            Thank You...
            """
            
            msg = email.message.Message()
            msg['Subject'] = "Your OTP"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            password = sender_pass

            msg.add_header('Content-Type','text/html')
            msg.set_payload(Email_Message)

            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
            print('Email Sent....')

            request.session['otp'] = otp_no
            request.session['email'] = em
            return redirect('pmotp')

        except:            
            try:
                data = Developer.objects.get(Email = em)
                print(data.Email)
                # OTP Genrate
                otp_no = ""
                for i in range(6):
                    no = random.randint(0,9)
                    otp_no += str(no)
                print(otp_no)

                # Send OTP Email
                sender_email = "harkhaniprins2001@gmail.com"
                sender_pass = "108510851085"
                receiver_email = data.Email
                
                server = smtplib.SMTP('smtp.gmail.com',587)
                
                Email_Message = f"""
                This Is Your OTP Don't Share With Others
                OTP = {otp_no}
                
                Thank You...
                """
                
                msg = email.message.Message()
                msg['Subject'] = "Your OTP"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                password = sender_pass

                msg.add_header('Content-Type','text/html')
                msg.set_payload(Email_Message)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                print('Email Sent....')

                request.session['otp'] = otp_no
                request.session['email'] = em
                return redirect('devotp')

            except:
                try:
                    data = Tester.objects.get(Email = em)
                    print(data.Email)
                    # OTP Genrate
                    otp_no = ""
                    for i in range(6):
                        no = random.randint(0,9)
                        otp_no += str(no)
                    print(otp_no)

                    # Send OTP Email
                    sender_email = "harkhaniprins2001@gmail.com"
                    sender_pass = "108510851085"
                    receiver_email = data.Email
                    
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    
                    Email_Message = f"""
                    This Is Your OTP Don't Share With Others
                    OTP = {otp_no}
                    
                    Thank You...
                    """
                    
                    msg = email.message.Message()
                    msg['Subject'] = "Your OTP"
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    password = sender_pass

                    msg.add_header('Content-Type','text/html')
                    msg.set_payload(Email_Message)

                    server.starttls()
                    server.login(msg['From'],password)
                    server.sendmail(msg['From'],msg['To'],msg.as_string())
                    print('Email Sent....')

                    request.session['otp'] = otp_no
                    request.session['email'] = em
                    return redirect('testotp')

                except:
                    messages.add_message(request, messages.ERROR, "Email Is Not Registered")
                    return redirect('homepage')


    return render(request,'PM_forget_pass.html')

def Dev_forget_password(request):
    if request.POST:
        em = request.POST['email']

    return render(request,'Dev_forget_pass.html')

def Test_forget_password(request):
    if request.POST:
        em = request.POST['email']

        
    return render(request,'Test_forget_pass.html')

def PM_otp_page(request):
    if 'otp' in request.session.keys():
        otp_no = request.session['otp']
        if request.POST:
            otp = request.POST['otp']
            if otp == otp_no:
                del request.session['otp']
                return redirect('pm_new_password')
            else:
                messages.add_message(request, messages.ERROR, "You Have Entered Wrong OTP")
                return redirect('pmotp')
        return render(request,'PM_otp.html')     
    else:            
        return redirect('homepage')

def Dev_otp_page(request):
    if 'otp' in request.session.keys():
        otp_no = request.session['otp']
        if request.POST:
            otp = request.POST['otp']
            if otp == otp_no:
                del request.session['otp']
                return redirect('dev_new_password')
            else:
                messages.add_message(request, messages.ERROR, "You Have Entered Wrong OTP")
                return redirect('devotp')
        return render(request,'Dev_otp.html')     
    else:            
        return redirect('homepage')

def Test_otp_page(request):
    if 'otp' in request.session.keys():
        otp_no = request.session['otp']
        if request.POST:
            otp = request.POST['otp']
            if otp == otp_no:
                del request.session['otp']
                return redirect('test_new_password')
            else:
                messages.add_message(request, messages.ERROR, "You Have Entered Wrong OTP")
                return redirect('testotp')
        return render(request,'Test_otp.html')     
    else:            
        return redirect('homepage')

def PM_new_password(request):
    if request.session.has_key('email'):
        if request.POST:
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            em = request.session['email']
            data = Project_manager.objects.get(Email = em)

            if pass1 == pass2:
                data.Password = pass1
                data.save()
                del request.session['email']
                return redirect('homepage')
            else:
                messages.add_message(request, messages.ERROR, "Passwords Are Not Same ...")
        return render(request,'PM_new_password.html')
    else:       
        return redirect('homepage')

def Dev_new_password(request):
    if request.session.has_key('email'):
        if request.POST:
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            em = request.session['email']
            data = Developer.objects.get(Email = em)

            if pass1 == pass2:
                data.Password = pass1
                data.save()
                del request.session['email']
                return redirect('homepage')
            else:
                messages.add_message(request, messages.ERROR, "Passwords Are Not Same ...")
        return render(request,'Dev_new_password.html')
    else:       
        return redirect('homepage')

def Test_new_password(request):
    if request.session.has_key('email'):
        if request.POST:
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            em = request.session['email']
            data = Tester.objects.get(Email = em)

            if pass1 == pass2:
                data.Password = pass1
                data.save()
                del request.session['email']
                return redirect('homepage')
            else:
                messages.add_message(request, messages.ERROR, "Passwords Are Not Same ...")
        return render(request,'Test_new_password.html')
    else:       
        return redirect('homepage')

def PM_Profile_update(request):
    if 'p_manager' in request.session.keys():
        pmup = Project_manager.objects.get(Email = request.session['p_manager'])
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']
            profile = request.FILES.get('pic')

            if profile == None:
                profile = pmup.profile_pic

            pmup.Name = sname
            pmup.Gender = sgen
            pmup.Email = semail
            request.session['p_manager'] = semail
            pmup.Mno = sno
            pmup.Address = saddress
            pmup.Password = spass
            pmup.profile_pic = profile
            pmup.save()
            return redirect('spmdash')
        return render(request,'PM_update.html',{"key":1,"datapm":pmup,'data':pmup,'my_template':"PMbase.html"})
    else:
        return redirect('spmdash')

def Dev_Profile_update(request):
    if 'developer' in request.session.keys():
        devup = Developer.objects.get(Email = request.session['developer'])
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']
            profile = request.FILES.get('pic')

            if profile == None:
                profile = devup.profile_pic

            devup.Name = sname 
            devup.Gender = sgen
            devup.Email = semail
            request.session['developer'] = semail
            devup.Mno = sno
            devup.Address = saddress
            devup.Password = spass
            devup.profile_pic = profile
            devup.save()
            return redirect('sdevdash')
        return render(request,'Dev_update.html',{"key":1,'datadev':devup,'data':devup,'my_template':"Devbase.html"})
    else:
        return redirect('sdevdash')

def Tester_Profile_update(request):
    if 'tester' in request.session.keys():
        testup = Tester.objects.get(Email = request.session['tester'])
        if request.POST:
            sname = request.POST['sname']
            sgen = request.POST['sgen']
            semail = request.POST['semail']
            sno = request.POST['sno']
            saddress = request.POST['saddress']
            spass = request.POST['spass']
            profile = request.FILES.get('pic')

            if profile == None:
                profile = testup.profile_pic

            testup.Name = sname
            testup.Gender = sgen
            testup.Email = semail
            request.session['tester'] = semail
            testup.Mno = sno
            testup.Address = saddress
            testup.Password = spass
            testup.profile_pic = profile
            testup.save()
            return redirect('stestdash')
        return render(request,'Test_update.html',{"key":1,'datates':testup,'data':testup,'my_template':"Testerbase.html"})
    else:
        return redirect('stestdash')

def add_project_type(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        if request.POST:
            ty = request.POST['tname']
            td = request.POST['tdetail']

            obj = Project_type()
            obj.Type_name = ty
            obj.Type_Details = td
            obj.save()
            return redirect('admindash')
        return render(request,'add_project_types.html',{'aduser':ad})
    else:
        return redirect('adminlogin')


def update_project_type(request,id):
    if 'admin' in request.session.keys():
        data = Project_type.objects.get(id=id)
        if request.POST:
            sname = request.POST['sname']
            sdetail = request.POST['sdetail']
            
            data.Type_name = sname
            data.Type_Details = sdetail
            data.save()
            return redirect('admindash')
        return render(request,'update_project_type.html',{"data":data,'my_template':"adminbase.html"})
    else:
        return redirect('admindash')

 
def delete_project_type(request,id):
    if 'admin' in request.session.keys():
        data = Project_type.objects.get(id=id)
        data.delete()
        return redirect('admindash')
    else:
        return redirect('homepage')


def Update_Project(request,id):
    if 'p_manager' in request.session.keys():
        data = request.session['p_manager']
        pm = Project_manager.objects.get(Email = data)
        pd = Project_Details.objects.get(id=id)
        devs = Developer.objects.all()
        tess = Tester.objects.all()
        if request.POST:
            Devs = request.POST['Devs']
            Tess = request.POST['Tess']
            pmneed = request.POST['pmneed']
            print(Devs,Tess,pmneed)
            Devs = Developer.objects.get(id=int(Devs))
            Tess = Tester.objects.get(id=int(Tess))
            print(Devs,Tess)
            pd.dev_id = Devs
            pd.tset_id = Tess
            pd.Project_Modules_need = pmneed
            pd.save()
            return redirect('spmdash')
        
        return render(request,'add_project.html',{"key":pd,'dev':devs,'tes':tess,'my_template':"PMbase.html",'pm':pm,'datapm':pm})
    else:
        return redirect('homepage')
        
def add_project(request):
    if 'admin' in request.session.keys():
        data = request.session['admin']
        ad = Admin.objects.get(Username = data)
        if request.POST:
            ptype = request.POST['ptype']
            pms = request.POST['pms']
            pname = request.POST['pname']
            pdetail = request.POST['pdetail']

            pm = Project_manager.objects.get(id=int(pms))
            pty = Project_type.objects.get(id=int(ptype))
            
            obj = Project_Details()
            obj.Pm_id = pm
            obj.Pt_id = pty
            obj.Project_Name = pname
            obj.Project_Detail = pdetail
            # obj.save()
            
            # Send OTP Email
            sender_email = "harkhaniprins2001@gmail.com"
            sender_pass = "108510851085"
            receiver_email = str(pm.Email)
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            Email_Message = f"""
            
            Dear {pm.Name},
            Admin Allocate New Project To You.
            Project Name is {pname}
            and further details Also gives you
            
            Thank You...
            """
            
            msg = email.message.Message()
            msg['Subject'] = "New Project Allocated"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            password = sender_pass

            msg.add_header('Content-Type','text/html')
            msg.set_payload(Email_Message)

            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
            print('Email Sent....')
            obj.save()
            
            return redirect('admindash')
        pt = Project_type.objects.all()
        pms = Project_manager.objects.all()
        return render(request,'add_project.html',{'pt':pt,'my_template':"adminbase.html",'pm':pms,'aduser':ad})
    else:
        return redirect('adminlogin')

def admin_update_project(request,id):
    if 'admin' in request.session.keys():
        pd = Project_Details.objects.get(id=id)
        pt = Project_type.objects.all()
        pm = Project_manager.objects.all()
        devs = Developer.objects.all()
        tess = Tester.objects.all()
        if request.POST:
            pname = request.POST['pname']
            pdetail = request.POST['pdetail']
            pmneed = request.POST['pmneed']
            ptype = request.POST['ptype']
            pms = request.POST['pms']
            devs = request.POST['devs']
            tess = request.POST['tess']
            
            ptype = Project_type.objects.get(id=int(ptype))
            if tess != "none":
                tess = Tester.objects.get(id=int(tess))
                pd.tset_id = tess
                pd.tester_request = False
            if devs != "none":
                devs = Developer.objects.get(id=int(devs))
                pd.dev_id = devs
                pd.developer_request = False
                
            pms = Project_manager.objects.get(id=int(pms))
            
            pd.Pm_id = pms
            pd.Pt_id = ptype
            pd.Project_Name = pname
            pd.Project_Detail = pdetail
            pd.Project_Modules_need = pmneed
            pd.save()
            return redirect('admindash')
        return render(request,'admin_update_project.html',{"key":pd,"pm":pm,'pt':pt,'Devs':devs,'Tess':tess,'my_template':"adminbase.html"})
    else:
        return redirect('admindash')

def admin_delete_project(request,id):
    if 'admin' in request.session.keys():
        data = Project_Details.objects.get(id=id)
        data.delete()
        return redirect('admindash')
    else:
        return redirect('homepage')


def Project_Modules(request):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        proj = Project_Details.objects.filter(Pm_id=pm)
        return render(request,'module_proj.html',{'datapm':pm,'pm_nm':pm,'my_template': "PMbase.html",'proj':proj})
    else:
        return redirect('homepage')
    
def Projects_Add_Module(request,id):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        proj = Project_Details.objects.get(id=id)
        deve = Developer.objects.all()
        tester = Tester.objects.all()

        if request.POST:
            pdid = request.POST.get('PROJ')
            M_Name = request.POST['mname']
            M_Details = request.POST['mdetail']
            M_Progress = request.POST['progress']
            d1 = request.POST.get('Devs')
            t1 = request.POST.get('Tess')
            print(pdid,M_Name,M_Details,M_Progress,d1,t1)

            pdid = Project_Details.objects.get(id=int(pdid))
            d1 = Developer.objects.get(id=int(d1))
            t1 = Tester.objects.get(id = int(t1))

            if int(proj.Project_Modules_Done) <= int(proj.Project_Modules_need):
                obj = Project_Module()
                obj.pd_id = pdid
                obj.Module_Name = M_Name
                obj.Module_Detail = M_Details
                obj.Progress = M_Progress
                obj.developer = d1
                obj.tester = t1
                obj.Pm_id = pm
                
                
                # Send OTP Email
                sender_email = "harkhaniprins2001@gmail.com"
                sender_pass = "108510851085"
                receiver_email = str(d1.Email)+","+str(t1.Email)
                
                server = smtplib.SMTP('smtp.gmail.com',587)
                
                Email_Message = f"""
                
                Dear {pm.Name},
                Project Manager Allocate New Module To You.
                Module Name is {M_Name}
                and further details Also gives you
                
                Thank You...
                """
                
                msg = email.message.Message()
                msg['Subject'] = "New Module Allocated"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                password = sender_pass

                msg.add_header('Content-Type','text/html')
                msg.set_payload(Email_Message)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                print('Email Sent....')
                
                
                obj.save()
            
                proj.Project_Modules_Done += int(1) 
                proj.save()
            else:
                print("No More Module Add Permission")
            return redirect('spmdash')
        return render(request,'add_module_proj.html',{'datapm':pm,'pm_nm':pm,'my_template': "PMbase.html",'dev':deve,'test':tester,'proj':proj})
    else:
        return redirect('homepage')

def Projects_Update_Module(request,id):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        proj = Project_Module.objects.get(id=id)
        deve = Developer.objects.all()
        tester = Tester.objects.all()

        if request.POST:
            M_Name = request.POST['mname']
            M_Details = request.POST['mdetail']
            M_Progress = request.POST['progress']
            Devs = request.POST['Devs']
            Tess = request.POST['Tess']
            
            print(M_Name,M_Details,M_Progress)

            if Devs != None:
                devs = Developer.objects.get(id=int(Devs))
                proj.developer = devs
                proj.developer_request = False

            if Tess != None:
                tes = Tester.objects.get(id=int(Tess))
                proj.tester = tes
                proj.tester_request = False

            proj.Module_Name = M_Name
            proj.Module_Detail = M_Details
            proj.Progress = M_Progress
            proj.save()
            return redirect('spmdash')
        return render(request,'add_module_proj.html',{'datapm':pm,'pm_nm':pm,'my_template': "PMbase.html",'dev':deve,'test':tester,'key':proj})
    else:
        return redirect('homepage')

def Projects_Delete_Module(request,id):
    if 'p_manager' in request.session.keys():
        proj = Project_Module.objects.get(id=id)
        proj.delete()
        proj = Project_Details.objects.get(id=proj.pd_id.id)
        proj.Project_Modules_Done -= int(1) 
        proj.save()
        return redirect('spmdash')
    else:
        return redirect('homepage')


def PM_AllocatedProjects(request):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        pdata = Project_Details.objects.filter(Pm_id=pm)
        return render(request,'PM_AllocatedProjects.html',{'pdata':pdata,'my_template': "PMbase.html",'datapm':pm})
    else:
        return redirect('homepage')
    
def Modules_Chats(request):
    if "tester" in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        mdata = Project_Module.objects.filter(tester=tes)
        return render(request,'Module_Chats.html',{'my_template': "Testerbase.html",'mdata':mdata,"tes_nm":tes,'datates':tes})
    if "developer" in request.session.keys():
        dev = Developer.objects.get(Email=request.session['developer'])
        mdata = Project_Module.objects.filter(developer=dev)
        return render(request,'Module_Chats.html',{'my_template': "Devbase.html",'mdata':mdata,"dev_nm":dev,'datadev':dev})
    else:
        return redirect('homepage')

def Modules_Data(request):
    if "tester" in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        mdata = Project_Module.objects.filter(tester=tes)
        return render(request,'Module_Datas.html',{'my_template': "Testerbase.html",'mdata':mdata,"tes_nm":tes,'datates':tes})
    if "developer" in request.session.keys():
        dev = Developer.objects.get(Email=request.session['developer'])
        mdata = Project_Module.objects.filter(developer=dev)
        return render(request,'Module_Datas.html',{'my_template': "Devbase.html",'mdata':mdata,"dev_nm":dev,'datadev':dev})
    else:
        return redirect('homepage')

def Modules_process(request,id):
    if "tester" in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        mdata = Project_Module.objects.get(id=id)
        if request.POST:
            proc = request.POST['proc']
            mdata.Progress = int(proc)
            mdata.save()
            return redirect('Modules_Data')
        return render(request,'ModuleUpdate_process.html',{'my_template': "Testerbase.html",'mdata':mdata,"tes_nm":tes,'datates':tes})
    else:
        return redirect('homepage')

def Chat_Data_Show(request,id):
    if "tester" in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        mdata = Project_Module.objects.get(id=id)
        mc = Models_Chats.objects.filter(mod=mdata)
        
        if request.POST:
            ptext = request.POST['ptext']
            zfile = request.FILES.get('zfile')
            
            MC = Models_Chats()
            MC.proj = mdata.pd_id
            MC.mod = mdata
            MC.tset = tes
            MC.problem_text = ptext
            MC.chat_doc = zfile
            MC.save()
            return redirect('Chat_Data_Show',id)
        return render(request,'Chat_Data_Show.html',{'mc':mc,"mdata":mdata,'my_template': "Testerbase.html","tes_nm":tes,'datates':tes})
    if "developer" in request.session.keys():
        dev = Developer.objects.get(Email=request.session['developer'])
        mdata = Project_Module.objects.get(id=id)
        mc = Models_Chats.objects.filter(mod=mdata)
        
        if request.POST:
            ptext = request.POST['ptext']
            zfile = request.FILES.get('zfile')
            
            MC = Models_Chats()
            MC.proj = mdata.pd_id
            MC.mod = mdata
            MC.devl = dev
            MC.problem_text = ptext
            MC.chat_doc = zfile
            MC.save()
            return redirect('Chat_Data_Show',id)
        return render(request,'Chat_Data_Show.html',{'mc':mc,'my_template': "Devbase.html",'mdata':mdata,"dev_nm":dev,'datadev':dev})
    else:
        return redirect('homepage')
    
def Question_Answers(request):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        sofq = StackOverFlowQuestion.objects.all()
        return render(request,'question_answers.html',{'datapm':pm,'pm_nm':pm,'my_template': "PMbase.html",'sofq':sofq})
    if "developer" in request.session.keys():
        dev = Developer.objects.get(Email=request.session['developer'])
        sofq = StackOverFlowQuestion.objects.all()
        return render(request,'question_answers.html',{'datadev':dev,'my_template': "Devbase.html",'dev_nm':dev,'sofq':sofq})
    if 'tester' in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        sofq = StackOverFlowQuestion.objects.all()
        return render(request,'question_answers.html',{'datates':tes,'my_template': "Testerbase.html",'tes_nm':tes,'sofq':sofq})
    return render(request,'Home.html')
    
def AddQuestion(request):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        if request.POST:
            user_type = request.POST['user_type']
            user = request.POST['user']
            que = request.POST['que']
            print(que)
            print(pm,user,user_type,que)
            mypm = Project_manager.objects.get(id=int(user))
            if user_type == "pmnm" and pm == mypm:
                print(True)
                print(f'{user_type} == "pmnm" AND {user} == {pm}, And {type(user)} == {type(pm)}')
                obj = StackOverFlowQuestion()
                obj.pmanage = mypm
                obj.Question = que
                obj.save()
                return redirect('Question_Answers')
        return render(request,'stackQuestions.html',{'datapm':pm,'pm_nm':pm,'my_template': "PMbase.html"})
    if "developer" in request.session.keys():
        dev = Developer.objects.get(Email=request.session['developer'])
        if request.POST:
            user_type = request.POST['user_type']
            user = request.POST['user']
            que = request.POST['que']
            print(que)
            print(dev,user,user_type,que)
            mypm = Developer.objects.get(id=int(user))
            if user_type == "devnm" and dev == mypm:
                print(True)
                print(f'{user_type} == "devnm" AND {user} == {dev}, And {type(user)} == {type(dev)}')
                obj = StackOverFlowQuestion()
                obj.devl = mypm
                obj.Question = que
                obj.save()
                return redirect('Question_Answers')
        return render(request,'stackQuestions.html',{'datadev':dev,'my_template': "Devbase.html",'dev_nm':dev})
    if 'tester' in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        if request.POST:
            user_type = request.POST['user_type']
            user = request.POST['user']
            que = request.POST['que']
            print(que)
            print(tes,user,user_type,que)
            mypm = Tester.objects.get(id=int(user))
            if user_type == "tesnm" and tes == mypm:
                print(True)
                print(f'{user_type} == "tesnm" AND {user} == {tes}, And {type(user)} == {type(tes)}')
                obj = StackOverFlowQuestion()
                obj.tset = mypm
                obj.Question = que
                obj.save()
                return redirect('Question_Answers')
        return render(request,'stackQuestions.html',{'datates':tes,'my_template': "Testerbase.html",'tes_nm':tes})
    return redirect('homepage')

def Answers_data(request,id):
    if 'p_manager' in request.session.keys():
        pm = Project_manager.objects.get(Email=request.session['p_manager'])
        sofq = StackOverFlowQuestion.objects.get(id=id)
        sofA = StackOverFlowAnswer.objects.filter(Questions=sofq)
        if request.POST:
            user_type = request.POST['user_type']
            user = request.POST['user']
            que = request.POST['que']
            answer = request.POST['answer']
            ansfile = request.FILES.get('ansfile')
            
            print(pm,user,user_type,que,answer)
            mypm = Project_manager.objects.get(id=int(user))
            myque = StackOverFlowQuestion.objects.get(id=int(que))
            if user_type == "pmnm" and pm == mypm:
                print(True)
                print(f'{user_type} == "pmnm" AND {user} == {pm}, And {type(user)} == {type(pm)}')
                obj = StackOverFlowAnswer()
                obj.pmanage = mypm
                obj.Questions = myque
                obj.Answer = answer
                obj.Answer_doc = ansfile
                obj.save()
            
        return render(request,'answers_Data.html',{'pm_nm':pm,'sofA':sofA,'sofq':sofq,'datapm':pm,'my_template': "PMbase.html"})
    if "developer" in request.session.keys():
        dev = Developer.objects.get(Email=request.session['developer'])
        sofq = StackOverFlowQuestion.objects.get(id=id)
        sofA = StackOverFlowAnswer.objects.filter(Questions=sofq)
        if request.POST:
            user_type = request.POST['user_type']
            user = request.POST['user']
            que = request.POST['que']
            answer = request.POST['answer']
            ansfile = request.FILES.get('ansfile')
            
            print(dev,user,user_type,que,answer)
            mypm = Developer.objects.get(id=int(user))
            myque = StackOverFlowQuestion.objects.get(id=int(que))
            if user_type == "devnm" and dev == mypm:
                print(True)
                print(f'{user_type} == "devnm" AND {user} == {dev}, And {type(user)} == {type(dev)}')
                obj = StackOverFlowAnswer()
                obj.devl = mypm
                obj.Questions = myque
                obj.Answer = answer
                obj.Answer_doc = ansfile
                obj.save()
            
        return render(request,'answers_Data.html',{'datadev':dev,'my_template': "Devbase.html",'dev_nm':dev,'sofA':sofA,'sofq':sofq})
    if 'tester' in request.session.keys():
        tes = Tester.objects.get(Email=request.session['tester'])
        sofq = StackOverFlowQuestion.objects.get(id=id)
        sofA = StackOverFlowAnswer.objects.filter(Questions=sofq)
        if request.POST:
            user_type = request.POST['user_type']
            user = request.POST['user']
            que = request.POST['que']
            answer = request.POST['answer']
            ansfile = request.FILES.get('ansfile')
            
            print(tes,user,user_type,que,answer)
            mypm = Tester.objects.get(id=int(user))
            myque = StackOverFlowQuestion.objects.get(id=int(que))
            if user_type == "tesnm" and tes == mypm:
                print(True)
                print(f'{user_type} == "tesnm" AND {user} == {tes}, And {type(user)} == {type(tes)}')
                obj = StackOverFlowAnswer()
                obj.tset = mypm
                obj.Questions = myque
                obj.Answer = answer
                obj.Answer_doc = ansfile
                obj.save()
            
        return render(request,'answers_Data.html',{'datates':tes,'my_template': "Testerbase.html",'tes_nm':tes,'sofA':sofA,'sofq':sofq})
    return redirect('homepage')