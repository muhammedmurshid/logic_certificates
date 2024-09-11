from odoo import models, fields, api, _
from PyPDF2 import PdfFileMerger
from datetime import datetime


class LogicExperienceCertificates(models.Model):
    _name = 'logic.experience.certificates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Logic Experience Certificates'
    _rec_name = 'display_name'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=1)
    designation = fields.Char(string='Designation', related='employee_id.job_title', readonly=False)
    address = fields.Char(string='Address')
    state = fields.Char(string='State')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    pincode = fields.Char(string='Pincode')
    country = fields.Char(string='Country')
    hr_manager = fields.Char(string='HR Manager')

    joining_date = fields.Date(string='Joining Date')
    leaving_date = fields.Date(string='Leaving Date')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    title = fields.Selection([('mr', 'Mr'), ('ms', 'Ms'), ('mrs', 'Mrs')], default='mr', string="Title")
    current_date = fields.Char(string='Date', compute='_compute_display_date', store=True)

    @api.depends('employee_id')
    def _compute_display_date(self):
        date = datetime.today().strftime('%d/%m/%Y')
        self.current_date = date
        print(date, 'jjjj')

    @api.depends('title')
    def _compute_display_gender(self):
        if self.title:
            if self.title == 'mr':
                self.gender = 'his'
            else:
                self.gender = 'her'

    gender = fields.Selection([('his', 'His'), ('her', 'Her')], string="Gender",
                              compute='_compute_display_gender', store=True)

    def _compute_display_name(self):
        for i in self:
            if i.employee_id:
                i.display_name = i.employee_id.name + '-' + 'Experience Certificate'

    @api.onchange('employee_id')
    def get_employee_joining_date(self):
        if self.employee_id:
            if self.employee_id.joining_date_cus:
                self.joining_date = self.employee_id.joining_date_cus
            else:
                self.joining_date = False
            if self.employee_id.joining_date:
                self.joining_date = self.employee_id.joining_date
            else:
                self.joining_date = False
            if self.employee_id.address_home_id:
                self.state = self.employee_id.address_home_id.state_id.name
                self.country = self.employee_id.address_home_id.country_id.name
            else:
                self.state = False
                self.country = False

    @api.model
    def _redirect_based_on_user_group(self):
        # Get the current user
        user = self.env.user
        print(user.groups_id,'user')

        # Check if the user belongs to a specific group
        hr_manager_group = self.env.ref('logic_certificates.hr_manager_certificates')
        employees = self.env.ref('logic_certificates.employees_for_certificates')
        print(hr_manager_group, 'hr')
        print(employees, 'emplo')
        if employees in user.groups_id:
            print('yes')
            # Redirect to Experience Certificates if the user is an HR manager
            return {
                'type': 'ir.actions.act_window',
                'name': 'Salary Slips',
                'res_model': 'logic.salary.slip',
                'view_mode': 'tree,form',
                'target': 'current',
                'views': [(self.env.ref('logic_certificates.model_logic_salary_slip_list').id, 'tree'),
                          (self.env.ref('logic_certificates.model_logic_salary_slip_form_view').id, 'form')],
            }

        else:
            print('no')
            # Redirect to Salary Slips for other users
            return {
                'type': 'ir.actions.act_window',
                'name': 'Experience Certificates',
                'res_model': 'logic.experience.certificates',
                'view_mode': 'tree,form',
                'target': 'current',
                'views': [(self.env.ref('logic_certificates.model_logic_experience_list').id, 'tree'),
                          (self.env.ref('logic_certificates.model_logic_experience_form').id, 'form')],
            }

