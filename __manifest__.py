{
    'name': 'HR Leave Management',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Manage employee leaves',
    'description': """
        This module helps you to manage employee leaves.
    """,
    'author': 'Dino Herlambang',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/hr_leave_security.xml',
        'security/ir.model.access.csv',
        'views/hr_leave_views.xml',
        'views/hr_dashboard_views.xml',
        'views/hr_leave_settings_views.xml',
        'views/hr_leave_approval_views.xml',
        'views/hr_leave_menus.xml',
        'views/hr_employee_views.xml',
        'data/hr_leave_data.xml',
        'data/hr_leave_sequence.xml',
    ],
    'installable': True,
    'application': True,
}
