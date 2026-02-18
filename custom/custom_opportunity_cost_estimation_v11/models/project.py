from odoo import models, fields, api


# from odoo.exceptions import UserError


class CustomProjectTask(models.Model):
    _inherit = "project.task"

    estimation_ids = fields.One2many(
        'custom.task.estimation.line',
        'task_id',
        string="estimation_line"
    )

    # @api.multi
    # def to_warehouse(self):
    #     lines = self.env['custom.task.estimation.line'].search(
    #         [('task_id', '=', self.id)])
    #     products = []
    #     for i in lines:
    #         if i.to_WH and not i.done_to_WH:
    #             products.append((0, 0, {
    #                 'product_id': i.product_id.id,
    #                 'product_uom': i.product_uom.id,
    #                 'name': i.name,
    #                 'product_uom_qty': i.actual_qty,
    #             }))
    #             i.done_to_WH = True
    #
    #     vals = {
    #         'picking_type_id': self.env.ref(
    #             "custom_opportunity_cost_estimation_v11.custom_warehouse_operation").id,
    #         'location_id': self.env.ref("stock.stock_location_stock").id,
    #         'location_dest_id': self.env.ref(
    #             "custom_opportunity_cost_estimation_v11.custom_warehouse_location").id,
    #         'move_lines': products,
    #         'origin': self.project_id.name + '/' + self.name,
    #     }
    #     self.env['stock.picking'].create(vals)

    # @api.onchange('estimation_ids')
    # def onchange_estimation_ids(self):
    #     pass



class CustomProjectProject(models.Model):
    _inherit = "project.project"

    estimation_ids = fields.One2many(
        'custom.project.estimation.line',
        'project_id'
    )
    tasks_estimations_ids = fields.One2many(
        'custom.task.estimation.line',
        'project_id'
    )

    tasks_estimations_ids_report = fields.One2many(
        'custom.task.estimation.line',
        'project_id'
    )

    # @api.multi
    # def to_warehouse(self):
    #     lines = self.env['custom.task.estimation.line'].search(
    #         [('project_id', '=', self.id)])
    #     products = []
    #     for i in lines:
    #         if i.to_WH and not i.done_to_WH:
    #             products.append((0, 0, {'product_id': i.product_id.id,
    #                                     'product_uom': i.product_uom.id,
    #                                     'name': i.name,
    #                                     'product_uom_qty': i.actual_qty,
    #                                     }))
    #             i.done_to_WH = True
    #
    #     vals = {
    #         'picking_type_id': self.env.ref(
    #             "custom_opportunity_cost_estimation_v11.custom_warehouse_operation").id,
    #         'location_id': self.env.ref("stock.stock_location_stock").id,
    #         'location_dest_id': self.env.ref(
    #             "custom_opportunity_cost_estimation_v11.custom_warehouse_location").id,
    #         'move_lines': products,
    #         'origin': self.name,
    #     }
    #     self.env['stock.picking'].create(vals)
