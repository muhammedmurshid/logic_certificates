from odoo import models, fields, api, _
from PyPDF2 import PdfFileMerger


class LogicBonafideCertificates(models.Model):
    _name = 'logic.bonafide.certificates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Logic Experience Certificates'
    _rec_name = 'display_name'

    student_id = fields.Many2one('logic.students', string='Student',)
    course_id = fields.Many2one('logic.base.courses', string='Course')
    admission_number = fields.Char(string='Admission Number')
    address = fields.Char(string='Address')
    place = fields.Char(string='Place')
    academic_head = fields.Many2one('res.users', string='Academic Head')
    academic_head_designation = fields.Char(string='Designation', related='academic_head.employee_id.job_title', readonly=False)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    website = fields.Char(string='Website')
    head_mail = fields.Char(string='Email', related='academic_head.employee_id.work_email', readonly=False)
    date_of_joining = fields.Date(string='Date of Joining')
    mode_of_study = fields.Selection([('online','Online'),('offline','Offline')], default='offline', string="Mode of Study")
    current_status = fields.Char(string='Current Status')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    title = fields.Selection([('mr', 'Mr'), ('ms', 'Ms'), ('mrs', 'Mrs')], default='mr', string="Title")

    @api.onchange('company_id')
    def _onchange_company_website(self):
        if self.company_id:
            self.website = self.company_id.website
    def _compute_display_name(self):
        for i in self:
            if i.student_id:
                i.display_name = i.student_id.name + '-' + 'BONAFIDE CERTIFICATE'
