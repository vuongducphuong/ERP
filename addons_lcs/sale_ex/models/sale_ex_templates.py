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

class KhoConverter(models.AbstractModel):
    _name = 'ir.qweb.field.kho'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        kho = ''
        for line in value:
            if line.KHO_ID.name and line.KHO_ID.name not in kho:
                kho += line.KHO_ID.name + ","
        return kho.strip(",")

class ChieuKhauConverter(models.AbstractModel):
    _name = 'ir.qweb.field.chieukhau'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        chiet_khau = 0
        for line in value:
            chiet_khau += line.TY_LE_CK
        return chiet_khau

class TienChieuKhauConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tienchieukhau'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tien_chiet_khau = 0.0
        for line in value:
            tien_chiet_khau += line.TIEN_CHIET_KHAU
        return tien_chiet_khau
class TienDaTruCKConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tiendatruck'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tien_chiet_khau = 0.0
        thanh_tien = 0.0
        tien_da_tru_ck = 0.0
        for line in value:
            tien_chiet_khau += line.TIEN_CHIET_KHAU
            thanh_tien += line.THANH_TIEN
        tien_da_tru_ck = thanh_tien - tien_chiet_khau
        return tien_da_tru_ck

class TienThueGTGTConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tienthuegtgt'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tien_thue_gtgt = 0.0
        for line in value:
            tien_thue_gtgt += line.TIEN_THUE_GTGT
        return tien_thue_gtgt