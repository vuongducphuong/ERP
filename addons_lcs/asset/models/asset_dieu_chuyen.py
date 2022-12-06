# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH(models.Model):
    _name = 'asset.dieu.chuyen'
    _description = 'Điều chuyển tài sản cố định'
    _inherit = ['mail.thread']
    _order = "NGAY desc, BIEN_BAN_GIAO_NHAN_SO desc"
    BIEN_BAN_GIAO_NHAN_SO = fields.Char(string='Biên bản giao nhận số', help='Biên bản giao nhận số',required=True)
    NGAY = fields.Date(string='Ngày', help='Ngày',required=True, default=fields.Datetime.now)
    NGUOI_BAN_GIAO = fields.Char(string='Người bàn giao', help='Người bàn giao')
    NGUOI_TIEP_NHAN = fields.Char(string='Người tiếp nhận', help='Người tiếp nhận')
    LY_DO_DIEU_CHUYEN = fields.Char(string='Lý do điều chuyển', help='Lý do điều chuyển')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    name = fields.Char(string='Name', help='Name',related='BIEN_BAN_GIAO_NHAN_SO',store=True)
    CHI_NHANH = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh')
    SO_TSCD_ID = fields.Many2one('so.tscd', ondelete='set null')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')

    ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH_CHI_TIET_IDS = fields.One2many('asset.dieu.chuyen.chi.tiet', 'DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID', string='Điều chuyển tài sản cố định chi tiết')
    STT_CHUNG_TU = fields.Char(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ', auto_num='asset_STT_CHUNG_TU') 
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    _sql_constraints = [
	('BIEN_BAN_GIAO_NHAN_SO_uniq', 'unique ("BIEN_BAN_GIAO_NHAN_SO")', 'Biên bản giao nhận số <<>> đã tồn tại!'),
	]


    
    @api.model
    def default_get(self, fields):
        rec = super(ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 253
        return rec

    @api.model
    def create(self, vals):
        
        result = super(ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH, self).create(vals)
        return result
        

    # @api.multi
    # def validate(self, vals, option=None):
    #     if not vals.get('ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH_CHI_TIET_IDS'):
    #         raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     elif not vals.get('BIEN_BAN_GIAO_NHAN_SO'):
    #         raise ValidationError("<Biên bản bàn giao số> không được bỏ trống.")
    #     elif (vals.get('BIEN_BAN_GIAO_NHAN_SO')):
    #         vals['name'] = vals.get('BIEN_BAN_GIAO_NHAN_SO')
    #     ngay_khoa_so = str(self.lay_ngay_khoa_so())
    #     if vals.get('NGAY') < ngay_khoa_so:
    #         raise ValidationError("Ngày chứng từ không được nhỏ hơn ngày khóa sổ " +str(ngay_khoa_so)+ ". Vui lòng kiểm tra lại")

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_tscd()
        self.write({'state':'da_ghi_so'})

    def ghi_so_tscd(self):
        line_ids = []
        thu_tu = 0
        for line in self.ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH_CHI_TIET_IDS:
            so_tscd = line.MA_TAI_SAN_ID.lay_du_lieu_tren_so(self.NGAY)
            if so_tscd:
                data_ghi_no = helper.Obj.inject(line, self)
                data_ghi_no.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'TSCD_ID' : line.MA_TAI_SAN_ID.id,
                    'NGAY_HACH_TOAN' : self.NGAY,
                    'NGAY_CHUNG_TU' : self.NGAY,
                    'THOI_GIAN_SU_DUNG' : so_tscd.THOI_GIAN_SU_DUNG,
                    'TY_LE_KHAU_HAO_THANG' : so_tscd.TY_LE_KHAU_HAO_THANG,
                    'GIA_TRI_KHAU_HAO_THANG' : so_tscd.GIA_TRI_KHAU_HAO_THANG,
                    'DON_VI_SU_DUNG_ID' : line.DEN_DON_VI_ID.id,
                    'LOAI_TSCD_ID' : so_tscd.LOAI_TSCD_ID.id,
                    'GIA_TRI_HAO_MON_LUY_KE' : so_tscd.GIA_TRI_HAO_MON_LUY_KE,
                    'TK_HAO_MON_ID' : so_tscd.TK_HAO_MON_ID.id,
                    'TK_NGUYEN_GIA_ID' : so_tscd.TK_NGUYEN_GIA_ID.id,
                    'THOI_GIAN_SU_DUNG_CON_LAI' : so_tscd.THOI_GIAN_SU_DUNG_CON_LAI,
                    'GIA_TRI_TINH_KHAU_HAO' : so_tscd.GIA_TRI_TINH_KHAU_HAO,
                    'GIA_TRI_CON_LAI' : so_tscd.GIA_TRI_CON_LAI,
                    'NGUYEN_GIA' : so_tscd.NGUYEN_GIA,
                    'SO_CHUNG_TU' : self.BIEN_BAN_GIAO_NHAN_SO,
                    'THU_TU_TRONG_CHUNG_TU' : thu_tu,
                })
                line_ids += [(0,0,data_ghi_no)]
                thu_tu += 1
            else:
                raise ValidationError('Tài sản cố định này chưa được ghi sổ. Vui lòng ghi sổ lại tài sản cố định này')
        # Tạo master
        stscd = self.env['so.tscd'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_TSCD_ID = stscd.id
        return True


    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()