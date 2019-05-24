{
  'name':'Account Journal Task',
  'description': 'This is a Demo task.',
  'version':'1.0',
  'author':'Teckzilla',
  
 'depends': ['base','product','purchase','account','sale','website'],
  'data': [
#    'security/security_groups.xml',
   'security/ir.model.access.csv',
#    'views/account_view.xml',
    'views/departments_view.xml',
    'views/cost_center_view.xml',
    'views/sections_view.xml',
    'views/account_invoice_line.xml',
    'views/report_generalledger.xml',

#    'wizards/teacher_wizard_in student.xml',
    
     # 'views/reports.xml',


#     'demo/category_demo.xml',
#     'views/template.xml',
#     'demo/product_demo.xml',
#     'views/template.7xml',
#       'views/options.xml'
  ],
    
 
  #'qweb': ['static/xml/template.xml'],
  'installable':True,
  'application':True,
  'auto_install':False,
}