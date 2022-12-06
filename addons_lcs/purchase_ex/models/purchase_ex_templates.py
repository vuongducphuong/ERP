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

class GhiNotralaihangmuaConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghinohangmua'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_no = ''
        for line in value:
            if line.TK_CO_ID.SO_TAI_KHOAN and line.TK_CO_ID.SO_TAI_KHOAN not in ghi_no:
                ghi_no += line.TK_CO_ID.SO_TAI_KHOAN + ","
        return ghi_no.strip(",")

class GhiNotralaihangmuatktienConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghinohangmuatktien'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_no = ''
        for line in value:
            if line.TK_TIEN_ID.SO_TAI_KHOAN and line.TK_TIEN_ID.SO_TAI_KHOAN not in ghi_no:
                ghi_no += line.TK_TIEN_ID.SO_TAI_KHOAN + ","
        return ghi_no.strip(",")

class GhiCoChungTuMuaHangConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghicohangmua'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_CO_ID.SO_TAI_KHOAN and line.TK_CO_ID.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_CO_ID.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")
		
class GhiCoChungTuTraLaiHangMuaConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghicotralaihangmua'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_KHO.SO_TAI_KHOAN and line.TK_KHO.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_KHO.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")
class GhiCotralaihangmuaphieuthuConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghicohangmuatkcpvatkt'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_NO_ID.SO_TAI_KHOAN and line.TK_NO_ID.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_NO_ID.SO_TAI_KHOAN + ","
            if line.TK_THUE_GTGT_ID.SO_TAI_KHOAN and line.TK_THUE_GTGT_ID.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_THUE_GTGT_ID.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")
class GhiCoGiamhangmuaphieuthuConverter(models.AbstractModel):
    _name = 'ir.qweb.field.ghicohangmuatkkhovatkt'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        ghi_co = ''
        for line in value:
            if line.TK_KHO.SO_TAI_KHOAN and line.TK_KHO.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_KHO.SO_TAI_KHOAN + ","
            if line.TK_THUE_GTGT_ID.SO_TAI_KHOAN and line.TK_THUE_GTGT_ID.SO_TAI_KHOAN not in ghi_co:
                ghi_co += line.TK_THUE_GTGT_ID.SO_TAI_KHOAN + ","
        return ghi_co.strip(",")

class KhoMuaHangConverter(models.AbstractModel):
    _name = 'ir.qweb.field.khomuahang'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        kho = ''
        for line in value:
            if line.KHO_ID.TEN_KHO and line.KHO_ID.TEN_KHO not in kho:
                kho += line.KHO_ID.TEN_KHO + ","
        return kho.strip(",")

class KhotralaihangmuaConverter(models.AbstractModel):
    _name = 'ir.qweb.field.khohang'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        kho = ''
        for line in value:
            if line.KHO.name and line.KHO.name not in kho:
                kho += line.KHO.name + ","
        return kho.strip(",")

class TongTienThueGTGTConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tongtienthuegtgt'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tongtien_thue_GTGT = 0
        for line in value:
            tongtien_thue_GTGT += line.TIEN_THUE_GTGT 
        return helper.Obj.convert_to_vnd(tongtien_thue_GTGT)

class TongTienGiamgiahangmuaConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tongtiengiamgiahangmua'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tongtien = 0
        for line in value:
            tongtien += line.THANH_TIEN + line.TIEN_THUE_GTGT 
        return helper.Obj.convert_to_vnd(tongtien)

class TongTienConverter(models.AbstractModel):
    _name = 'ir.qweb.field.tongtienmuahang'
    _inherit = 'ir.qweb.field'

    @api.model
    def value_to_html(self, value, options):
        tongtien = 0
        for line in value:
            tongtien += line.THANH_TIEN_QUY_DOI 
        return helper.Obj.convert_to_vnd(tongtien)