from odoo import api, models

class SoluonhghigiamConverter(models.AbstractModel):
    _name = 'ir.qweb.field.soluongghigiam'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        so_luong_ghi_giam = 0.0
        for line in value:
            so_luong_ghi_giam += line.SO_LUONG_GHI_GIAM
        return so_luong_ghi_giam

class GiatriconlaicuaccdcghigiamConverter(models.AbstractModel):
    _name = 'ir.qweb.field.giatriconlaicuaccdcghigiam'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tien = 0.0
        for line in value:
            tien += line.GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM
        return tien