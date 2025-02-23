# HR Leave and Approval

This Odoo module adds custom HR leave management with request approval and notifications.

## Features

- Manage leave requests for employees.
- Approve or refuse leave requests.
- Send notifications upon leave approval.
- Configure allowable leave days based on employee rank.
- Prevent overlapping leave requests for the same employee.
- Track changes and activities on leave requests.
- View HR dashboard with total employees and employees on leave.

## Installation

1. Clone the repository into your Odoo addons directory:
    ```sh
    git clone https://github.com/dinoherlambang/dh_hr_leave.git
    ```

2. Update the Odoo module list:
    ```sh
    ./odoo-bin -u all
    ```

3. Install the `HR Leave and Approval` module from the Odoo Apps menu.

## Usage

1. Navigate to the **Leave Management** menu.
2. Create and manage leave requests.
3. Approve or refuse leave requests.
4. Configure allowable leave days in the **Leave Settings** menu.
5. View the HR dashboard for an overview of total employees and employees on leave.

## Models

- `hr.leave`: Manages leave requests.
- `hr.leave.settings`: Configures allowable leave days based on rank.
- `hr.dashboard`: Displays HR dashboard with total employees and employees on leave.

## Views

- [hr_leave_views.xml](http://_vscodecontentref_/0): Defines views for leave requests.
- [hr_dashboard_views.xml](http://_vscodecontentref_/1): Defines views for the HR dashboard.
- [hr_leave_settings_views.xml](http://_vscodecontentref_/2): Defines views for leave settings.
- [hr_leave_menus.xml](http://_vscodecontentref_/3): Defines menu items for the module.

## Security

- [hr_leave_security.xml](http://_vscodecontentref_/4): Defines access rules for leave management.
- [ir.model.access.csv](http://_vscodecontentref_/5): Defines model access permissions.

## Data

- [hr_leave_data.xml](http://_vscodecontentref_/6): Contains email templates for leave approval notifications.

## Authors

- Dino Herlambang

## License

This project is licensed under the MIT License - see the LICENSE file for details.