from odoo import api, models, helper

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
    _name = 'ir.qweb.field.ghicokho'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_CO_ID.SO_TAI_KHOAN and line.TK_CO_ID.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_CO_ID.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")
class GhiConNhapConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghicokhonhap'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_CO_ID2.SO_TAI_KHOAN and line.TK_CO_ID2.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_CO_ID2.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")

class KhoConverter(models.AbstractModel):
    _name = 'ir.qweb.field.khostock'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        kho = ''
        for line in value:
            if line.KHO_ID.MA_KHO and line.KHO_ID.MA_KHO not in kho:
                kho += line.KHO_ID.MA_KHO + ","
        return kho.strip(",")

class TongTienConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tongtien'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tongtien = 0
        for line in value:
            tongtien += line.THANH_TIEN
        return helper.Obj.convert_to_vnd(tongtien)