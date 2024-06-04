from odoo import fields, models, api


class LogicSalarySlip(models.Model):
    _name = 'logic.salary.slip'
    _description = 'Logic Salary Slip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    employee_id = fields.Many2one('hr.employee', string="Employee Name")
    employee_code = fields.Char(string="Employee Code")
    designation = fields.Char(string="Designation", related='employee_id.job_title', readonly=False)
    department = fields.Many2one('hr.department', string="Department")
    branch = fields.Many2one('logic.base.branches', string="Branch")
    joining_date = fields.Date(string="Joining Date")
    pay_period = fields.Char(string="Pay Period")
    total_working_days = fields.Integer(string="Total Working Days")
    esi_number = fields.Char(string="ESI Number")
    pf_number = fields.Char(string="PF Number")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    salary_ids = fields.One2many('logic.salary.calculation', 'salary_id', string="Salary Details")

    def _compute_display_name(self):
        for i in self:
            if i.employee_id:
                i.display_name = i.employee_id.name + '-' + 'Salary Slip'

    @api.onchange('employee_id')
    def get_employee_data(self):
        if self.employee_id:
            if self.employee_id.department_id:
                self.department = self.employee_id.department_id.id
            else:
                self.department = False
            if self.employee_id.branch_id:
                self.branch = self.employee_id.branch_id.id
            else:
                self.branch = False
            if self.employee_id.joining_date_cus:
                self.joining_date = self.employee_id.joining_date_cus
            else:
                self.joining_date = False

    @api.model
    def default_get(self, fields_list):
        res = super(LogicSalarySlip, self).default_get(fields_list)
        vals = [(0, 0, {'earnings': 'Basic', 'earned_amount': 0, 'deduction': 'PF Employer Contribution',
                        'deducted_amount': 0}),
                (0, 0, {'earnings': 'HRA', 'earned_amount': 0, 'deduction': 'PF Employee Contribution',
                        'deducted_amount': 0}),
                (0, 0, {'earnings': 'Special Allowance', 'earned_amount': 0, 'deduction': 'ESI Employer Contribution',
                        'deducted_amount': 0}),

                (0, 0, {'earnings': 'Incentive', 'earned_amount': 0, 'deduction': 'Professional Tax',
                        'deducted_amount': 0}),

                (0, 0, {'earnings': 'Other Earnings', 'earned_amount': 0, 'deduction': 'Work from home deductions',
                        'deducted_amount': 0}),
                (0, 0, {'earnings': 'PF Employer Contribution', 'earned_amount': 0, 'deduction': 'Loan Amount',
                        'deducted_amount': 0}),
                (0, 0, {'earnings': 'ESI Employer Contribution', 'earned_amount': 0, 'deduction': 'Income Tax',
                        'deducted_amount': 0}),
                (0, 0, {'deduction': 'ESI Employee Contribution',
                        'deducted_amount': 0}),
                (0, 0, {'deduction': 'Leave Salary deduction',
                        'deducted_amount': 0}),
                (0, 0, {'deduction': 'Salary Advance',
                        'deducted_amount': 0}),
                ]
        res.update({'salary_ids': vals})
        return res

    gross_pay = fields.Float(string="Gross Pay", compute="_amount_all", store=True)
    total_deduction = fields.Float(string="Total Deduction", compute="_amount_all_deduction", store=True)
    net_pay = fields.Float(string="Net Pay", compute="get_net_pay_amount", store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('salary_ids.earned_amount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        total = 0
        for order in self.salary_ids:
            total += order.earned_amount
        self.update({
            'gross_pay': total,
        })

    @api.depends('salary_ids.deducted_amount')
    def _amount_all_deduction(self):
        """
        Compute the total amounts of the SO.
        """
        total = 0
        for order in self.salary_ids:
            total += order.deducted_amount
        self.update({
            'total_deduction': total,
        })

    @api.depends('gross_pay', 'total_deduction')
    def get_net_pay_amount(self):
        for i in self:
            i.net_pay = i.gross_pay - i.total_deduction


class LogicSalaryCalculation(models.Model):
    _name = 'logic.salary.calculation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    earnings = fields.Char(string="Earnings")
    earned_amount = fields.Float(string="Earned Amount")
    deduction = fields.Char(string="Deductions")
    deducted_amount = fields.Float(string="Deducted Amount")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

    salary_id = fields.Many2one('logic.salary.slip', string="Salary Slip Id", ondelete="cascade")
