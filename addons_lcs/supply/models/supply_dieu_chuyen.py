# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class SUPPLY_DIEU_CHUYEN_CCDC(models.Model):
    _name = 'supply.dieu.chuyen.cong.cu.dung.cu'
    _description = 'Điều chuyển công cụ dụng cụ'
    _inherit = ['mail.thread']
    _order = "NGAY desc, BIEN_BAN_GIAO_NHAN_SO desc"

    BIEN_BAN_GIAO_NHAN_SO = fields.Char(string='Biên bản giao nhận số', help='Biên bản giao nhận số', auto_num='supply_dieu_chuyen_BIEN_BAN_GIAO_NHAN_SO',required=True)
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now,required=True)
    NGUOI_BAN_GIAO = fields.Char(string='Người bàn giao', help='Người bàn giao')
    NGUOI_TIEP_NHAN = fields.Char(string='Người tiếp nhận', help='Người tiếp nhận')
    LY_DO_DIEU_CHUYEN = fields.Char(string='Lý do điều chuyển', help='Lý do điều chuyển')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu',readonly=True)
    name = fields.Char(string='Name', help='Name',related='BIEN_BAN_GIAO_NHAN_SO')
    CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    SO_CCDC_ID = fields.Many2one('so.ccdc', ondelete='set null')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
 
    SUPPLY_DIEU_CHUYEN_CCDC_CHI_TIET_IDS = fields.One2many('supply.dieu.chuyen.chi.tiet', 'DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID', string='Điều chuyển ccdc chi tiết')
    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    STT_NHAP_CT = fields.Integer(string='Số thứ tự nhập chứng từ', help='RefOrder' )

    _sql_constraints = [
	('BIEN_BAN_GIAO_NHAN_SO_DCCCDC_uniq', 'unique ("BIEN_BAN_GIAO_NHAN_SO")', 'Biên bản giao nhận số <<>> đã tồn tại!'),
	]


    @api.model
    def default_get(self,default_fields):
        res = super(SUPPLY_DIEU_CHUYEN_CCDC, self).default_get(default_fields)
        res['LOAI_CHUNG_TU'] = 451
        return res
        
    # @api.model
    # def create(self, vals):
    #     if not vals.get('SUPPLY_DIEU_CHUYEN_CCDC_CHI_TIET_IDS'):
    #         raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     elif (vals.get('BIEN_BAN_GIAO_NHAN_SO')):
    #         vals['name'] = vals.get('BIEN_BAN_GIAO_NHAN_SO')
    #     result = super(SUPPLY_DIEU_CHUYEN_CCDC, self).create(vals)
    #     return result

    @api.multi
    def action_ghi_so(self):
        for record in self:
        # if self.SUPPLY_DIEU_CHUYEN_CCDC_CHI_TIET_IDS:
        #     for line in self.SUPPLY_DIEU_CHUYEN_CCDC_CHI_TIET_IDS:
        #         check_dieu_chinh = self.env['so.ccdc.chi.tiet'].search([('LOAI_CHUNG_TU', 'in', ('451','452')),('NGAY_HACH_TOAN', '>',self.NGAY),('CCDC_ID','=', line.MA_CCDC_ID)],limit = 1).id
        #         if check_dieu_chinh:
        #             ten_ccdc = ''
        #             ten_ccdc += "<" + line.TEN_CCDC + ">"
        #             raise ValidationError("Ghi sổ không thành công do CCDC " +ten_ccdc+" đã có phát sinh điều chuyển hoặc ghi giảm sau ngày điều chuyển. Để ghi sổ chứng từ này thì phải bỏ ghi các chứng từ liên quan.")
            record.ghi_so_ccdc()
        self.write({'state':'da_ghi_so'})

    def ghi_so_ccdc(self):
        line_ids = []
        thu_tu = 0
        for line in self.SUPPLY_DIEU_CHUYEN_CCDC_CHI_TIET_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'NGAY_CHUNG_TU': self.NGAY,
                'NGAY_HACH_TOAN': self.NGAY,
                'SO_LUONG_GHI_GIAM' : line.SO_LUONG_DIEU_CHUYEN,
                'SO_LUONG_GHI_TANG' : 0,
                'DOI_TUONG_PHAN_BO_ID' : line.TU_DON_VI_ID.id,
                'CCDC_ID': line.MA_CCDC_ID.id,
                'SO_CHUNG_TU' : self.BIEN_BAN_GIAO_NHAN_SO,
                'DIEN_GIAI_CHUNG' : self.LY_DO_DIEU_CHUYEN,
            })
            line_ids += [(0,0,data)]

            data2 = data.copy()
            data2.update({
                'SO_LUONG_GHI_TANG' : line.SO_LUONG_DIEU_CHUYEN,
                'DOI_TUONG_PHAN_BO_ID' : line.DEN_DON_VI_ID.id,
                'SO_LUONG_GHI_GIAM' : 0,
            })
            line_ids += [(0,0,data2)]
            thu_tu += 1
        # Tạo master
        sccdc = self.env['so.ccdc'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CCDC_ID = sccdc.id
        return True

    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()
      