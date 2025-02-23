{
    'name': 'HR Leave and Approval',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom HR Leave Management with Approval and Notifications',
    'description': """
        This module adds custom HR leave management with request approval and notifications.
    """,
    'author': 'Dino Herlambang',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/hr_leave_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_leave_security.xml',
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
