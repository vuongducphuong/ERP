from odoo import api, models

class HOP_DONG_BAN_REPORT(models.AbstractModel):
    _name = 'report.sale_ex.template_sale_ex_hop_dong_ban'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['sale.ex.hop.dong.ban'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.ex.hop.dong.ban',
            'docs': records,
            'data': data,
        }