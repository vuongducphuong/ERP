from odoo import api, models
class TenDonViConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tendonvi'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ten_don_vi = ''
        for line in value:
            if line.MA_DON_VI_ID.name and line.MA_DON_VI_ID.name not in ten_don_vi:
                ten_don_vi += line.MA_DON_VI_ID.name + ","
        return ten_don_vi.strip(",")