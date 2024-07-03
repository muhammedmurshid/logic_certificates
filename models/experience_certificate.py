from odoo import models, fields, api, _
from PyPDF2 import PdfFileMerger


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
    title = fields.Selection([('mr','Mr'),('ms','Ms'),('mrs','Mrs')], default='mr', string="Title")

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
