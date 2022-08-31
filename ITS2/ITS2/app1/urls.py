from django.urls import path 
from .import views as v

urlpatterns = [

    path('',v.Home_Page,name="homepage"),
    path('admin_logout/',v.Admin_Logout,name="Admin_Logout"),
    path('admin_login/',v.Admin_login, name="adminlogin"),
    path('admin_dashboard/',v.admin_dashboard, name="admindash"),
    path('manage_staff/',v.manage_staff, name="managestaff"),
    path('manage_project/',v.manage_project, name="manageproject"),

    path('add_pm/',v.add_pm, name="addpm"),
    path('add_dev/',v.add_developer, name="adddev"),
    path('add_test/',v.add_tester, name="addtest"),
    path('view_detail/',v.view_details, name="viewdetails"),
    path('PM_Allocated_Projects/',v.PM_AllocatedProjects,name='PM_AllocatedProjects'),
    path('Pm_Logout/',v.Pm_Logout,name='Pm_Logout'),
    path('Developer_Logout/',v.Developer_Logout,name='Developer_Logout'),

    path('pm_update/<int:id>',v.PM_update, name="pmupdate"),
    path('dev_update/<int:id>',v.Dev_update, name="devupdate"),
    path('test_update/<int:id>',v.Test_update, name="testupdate"),

    path('pm_delete/<int:id>',v.PM_delete, name="pmdelete"),
    path('dev_delete/<int:id>',v.Dev_delete, name="devdelete"),
    path('test_delete/<int:id>',v.Test_delete, name="testdelete"),

    path('pmregi/',v.PM_Registeration,name="spm_regi"),
    path('devregi/',v.Developer_Registeration,name="sdev_regi"),
    path('testregi/',v.Tester_Registeration,name="stest_regi"),
    
    path('pmlog/',v.PM_login,name="spm_log"),
    path('devlog/',v.Developer_login,name="sdev_log"),
    path('testlog/',v.Tester_login,name="stest_log"),

    path('pm_forgetpass/',v.PM_forget_password, name="pmforgetpass"),
    path('dev_forgetpass/',v.Dev_forget_password, name="devforgetpass"),
    path('test_forgetpass/',v.Test_forget_password, name="testforgetpass"),

    path('pm_otp/',v.PM_otp_page, name="pmotp"),
    path('dev_otp/',v.Dev_otp_page, name="devotp"),
    path('test_otp/',v.Test_otp_page, name="testotp"),

    path('pm_new_password/',v.PM_new_password, name="pm_new_password"),
    path('dev_new_password/',v.Dev_new_password, name="dev_new_password"),
    path('test_new_password/',v.Test_new_password, name="test_new_password"),

    path('pmdash/',v.PM_Dashboard,name="spmdash"),
    path('devdash/',v.Developer_Dashboard,name="sdevdash"),
    path('testdash/',v.Tester_Dashboard,name="stestdash"),

    path('Add_project_type/',v.add_project_type,name='addprojecttype'),
    path('Update_Project/<int:id>',v.Update_Project,name='updateproject'),
    path('Add_project/',v.add_project,name='addproject'),
    path('Add_Module/<int:id>',v.Projects_Add_Module,name='add_module_proj'),
    path('Update_Module/<int:id>',v.Projects_Update_Module,name='update_module_proj'),
    path('Delete_Module/<int:id>',v.Projects_Delete_Module,name='delete_module_proj'),
    path('Project_Modules/',v.Project_Modules,name='Project_Modules'),

    path('Question_Answers/',v.Question_Answers,name='Question_Answers'),
    path('AddQuestion/',v.AddQuestion,name='AddQuestion'),
    path('Answers_data/<int:id>',v.Answers_data,name='Answers_data'),
    path('Modules_Chats/',v.Modules_Chats,name='Modules_Chats'),
    path('Modules_Data/',v.Modules_Data,name='Modules_Data'),
    path('Tester_Logout/',v.Tester_Logout,name='Tester_Logout'),
    
    path('Chat_Data_Show/<int:id>',v.Chat_Data_Show,name='Chat_Data_Show'),
    path('Modules_process/<int:id>',v.Modules_process,name='Modules_process'),
    
    path('Admin_Report_Generate/',v.Admin_Report_Generate,name='Admin_Report_Generate'),
    path('PM_Report_Generate/',v.PM_Report_Generate,name='PM_Report_Generate'),
    path('Dev_Report_Generate/',v.Dev_Report_Generate,name='Dev_Report_Generate'),
    path('Tes_Report_Generate/',v.Tes_Report_Generate,name='Tes_Report_Generate'),
    path('Admin_Report/<int:id>/',v.Admin_Report,name='Admin_Report'),
    
    path('Pm_profile_update/',v.PM_Profile_update,name="pm_profile_update"),
    path('Dev_profile_update/',v.Dev_Profile_update,name="dev_profile_update"),
    path('Test_profile_update/',v.Tester_Profile_update,name="test_profile_update"),
    path('admin_update_project/<int:id>',v.admin_update_project,name='adminupdateproject'),
    path('admin_delete_project/<int:id>',v.admin_delete_project,name='admindeleteproject'),
    path('update_type/<int:id>',v.update_project_type,name="updatetype"),
    path('delete_type/<int:id>',v.delete_project_type,name="deletetype"),
]
