# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
import json

class SUPPLY_DIEU_CHINH_CCDC(models.Model):
    _name = 'supply.dieu.chinh'
    _description = 'Điều chỉnh công cụ dụng cụ'
    _inherit = ['mail.thread']
    _order = "NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    LY_DO_DIEU_CHINH = fields.Char(string='Lý do điều chỉnh', help='Lý do điều chỉnh')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ', default=fields.Datetime.now, required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='supply_dieu_chinh_SO_CHUNG_TU',required=True)
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU')
    SO_CCDC_ID = fields.Many2one('so.ccdc', ondelete='set null')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')

    SUPPLY_CHI_TIET_DIEU_CHINH_CCDC_IDS = fields.One2many('supply.dieu.chinh.chi.tiet', 'CHI_TIET_DIEU_CHINH_CCDC_ID_ID', string='Chi tiết điều chỉnh công cụ dụng cụ')
    SUPPLY_TAP_HOP_CHUNG_TU_CCDC_IDS = fields.One2many('supply.dieu.chinh.tap.hop.chung.tu', 'TAP_HOP_CHUNG_TU_CCDC_ID_ID', string='Tập hợp chứng từ công cụ dụng cụ')

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    CHON_CHUNG_TU_JSON = fields.Text(store=False)

    _sql_constraints = [
	('SO_CHUNG_TU_DCCCDC_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập lại số chứng từ!'),
	]


    # @api.onchange('CHON_CHUNG_TU_JSON')
    # def _onchange_CHON_CHUNG_TU_JSON(self):
    #     if self.CHON_CHUNG_TU_JSON:
    #         chon_chung_tu = json.loads(self.CHON_CHUNG_TU_JSON).get('ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS', [])
    #         self.SUPPLY_TAP_HOP_CHUNG_TU_CCDC_IDS = []
    #         env = self.env['supply.dieu.chinh.tap.hop.chung.tu']
    #         for chung_tu in chon_chung_tu:
    #             new_line = env.new({
    #                     'NGAY_CHUNG_TU': chung_tu.get('NGAY_CHUNG_TU'),
    #                     'SO_CHUNG_TU': chung_tu.get('SO_CHUNG_TU'),
    #                     'DIEN_GIAI': chung_tu.get('DIEN_GIAI'),
    #                     'SO_TIEN': chung_tu.get('SO_TIEN'),
    #                     'ID_GOC': chung_tu.get('ID_GOC'),
    #                     'MODEL_GOC': chung_tu.get('MODEL_GOC'),
    #             })
    #             self.SUPPLY_TAP_HOP_CHUNG_TU_CCDC_IDS += new_line



    @api.model
    def default_get(self,default_fields):
        res = super(SUPPLY_DIEU_CHINH_CCDC, self).default_get(default_fields)
        res['LOAI_CHUNG_TU'] = 454
        return res

    # @api.model
    # def create(self, vals):
    #     if not vals.get('SUPPLY_CHI_TIET_DIEU_CHINH_CCDC_IDS'):
    #         raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     # elif not vals.get('SUPPLY_CHI_TIET_DIEU_CHINH_CCDC_IDS.MA_CCDC'):
    #     #     raise ValidationError("<Mã CCDC> không được bỏ trống.")
    #     elif (vals.get('SO_CHUNG_TU')):
    #         vals['name'] = vals.get('SO_CHUNG_TU')
    #     result = super(SUPPLY_DIEU_CHINH_CCDC, self).create(vals)
    #     return result

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_ccdc()
        self.write({'state':'da_ghi_so'})

    def ghi_so_ccdc(self):
        line_ids = []
        thu_tu = 0
        for line in self.SUPPLY_CHI_TIET_DIEU_CHINH_CCDC_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'NGAY_HACH_TOAN': self.NGAY_CHUNG_TU,
                'DIEN_GIAI' : self.LY_DO_DIEU_CHINH,
                'SO_TIEN_GHI_GIAM' : -1*line.CHENH_LECH_GIA_TRI,
                'SO_TIEN_PHAN_BO_HANG_KY' : line.SO_TIEN_PHAN_BO_HANG_KY,
                'CCDC_ID' : line.MA_CCDC.id
            })
            line_ids += [(0,0,data_ghi_no)]
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