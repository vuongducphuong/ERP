from odoo import api, models

class GhiNoConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghino'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_no = ''
        for line in value:
            if line.TK_NO_ID.SO_TAI_KHOAN and line.TK_NO_ID.SO_TAI_KHOAN not in ghi_no:
                ghi_no += line.TK_NO_ID.SO_TAI_KHOAN + ","
        return ghi_no.strip(",")

class GhiCoConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghico'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_CO_ID.SO_TAI_KHOAN and line.TK_CO_ID.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_CO_ID.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")
    
class TaiKhoanConverter(models.AbstractModel):
    _name = 'ir.qweb.field.taikhoan'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tai_khoan = ''
        for line in value:
            if line.TK_NO_ID.SO_TAI_KHOAN and line.TK_NO_ID.SO_TAI_KHOAN not in tai_khoan:
                tai_khoan += line.TK_NO_ID.SO_TAI_KHOAN + ","
        return tai_khoan.strip(",")

    
class TaiKhoanBaoNoConverter(models.AbstractModel):
    _name = 'ir.qweb.field.taikhoanbaono'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tai_khoan_bao_no = ''
        for line in value:
            if line.TK_CO_ID.SO_TAI_KHOAN and line.TK_CO_ID.SO_TAI_KHOAN not in tai_khoan_bao_no:
                tai_khoan_bao_no += line.TK_CO_ID.SO_TAI_KHOAN + ","
        return tai_khoan_bao_no.strip(",")