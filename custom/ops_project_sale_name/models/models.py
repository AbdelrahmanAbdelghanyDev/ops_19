from odoo import models, fields, api


class cit_project_sale_name(models.Model):
    _inherit = 'sale.order.line'



    def _timesheet_create_task_prepare_values(self, project):
        res = super()._timesheet_create_task_prepare_values(project)
        res.update({'name': self.order_id.name+':'+self.name})
        return res


