from odoo import api, models

class TinhkhauhaothangConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tinhkhthang'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tinh_khau_hao = 0.0
        for line in value:
            tinh_khau_hao += line.GIA_TRI_KH_THANG
        return tinh_khau_hao