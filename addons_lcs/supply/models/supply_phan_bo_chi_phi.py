# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision


class SUPPLY_PHAN_BO_CHI_PHI(models.Model):
    _name = 'supply.phan.bo.chi.phi'
    _description = 'Phân bổ chi phí'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc"

    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng')
    NAM = fields.Integer(string='Năm', help='Năm')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='supply_phan_bo_chi_phi_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU',store=True,)
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_CCDC_ID = fields.Many2one('so.ccdc', ondelete='set null')

    TONG_SO_TIEN_PHAN_BO = fields.Float(string='Tổng số tiền phân bổ', help='Tổng số tiền phân bổ',compute='tinh_tong_tien',store=True, digits=decimal_precision.get_precision('VND'))

    SUPPLY_PHAN_BO_CHI_PHI_PHAN_BO_IDS = fields.One2many('supply.phan.bo.chi.phi.phan.bo', 'PHAN_BO_CHI_PHI_ID', string='Phân bổ chi phí phân bổ')
    SUPPLY_PHAN_BO_CHI_PHI_MUC_CHI_PHI_IDS = fields.One2many('supply.phan.bo.chi.phi.muc.chi.phi', 'PHAN_BO_CHI_PHI_ID', string='Phân bổ chi phí mức chi phí')
    SUPPLY_PHAN_BO_CHI_PHI_HACH_TOAN_IDS = fields.One2many('supply.phan.bo.chi.phi.hach.toan', 'PHAN_BO_CHI_PHI_ID', string='Phân bổ chi phí hạch toán')

    STT_NHAP_CT = fields.Integer(string='Số thứ tự nhập chứng từ', help='RefOrder' )

    _sql_constraints = [
	('SO_CHUNG_TU_PBCCDC_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	]

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    # @api.onchange('LOAI_CHUNG_TU')
    # def update_tai_khoan_ngam_dinh(self):
    #     for line in self.SUPPLY_PHAN_BO_CHI_PHI_HACH_TOAN_IDS:
    #         tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0))
    #         for tk in tk_nds:
    #             setattr(line, tk, tk_nds.get(tk))
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.model
    def default_get(self,default_fields):
        res = super(SUPPLY_PHAN_BO_CHI_PHI, self).default_get(default_fields)
        res['LOAI_CHUNG_TU'] = 453
        return res

    @api.depends('SUPPLY_PHAN_BO_CHI_PHI_MUC_CHI_PHI_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien_phan_bo = 0
            for line in order.SUPPLY_PHAN_BO_CHI_PHI_MUC_CHI_PHI_IDS:
                
                tong_tien_phan_bo +=line.TONG_SO_TIEN_PHAN_BO
                

            order.update({
                'TONG_SO_TIEN_PHAN_BO':tong_tien_phan_bo,
            })

    
    # @api.model
    # def create(self, values):
    #     if values.get('DIEN_GIAI'):
    #         values['name'] = values.get('DIEN_GIAI')
    #     dict_phan_bo = {}
    #     for line in values.get('SUPPLY_PHAN_BO_CHI_PHI_PHAN_BO_IDS'):
    #         key = line[2].get('MA_CCDC')
    #         if not key in dict_phan_bo:
    #             dict_phan_bo[key] = {
    #                 # 'TY_LE_PB' : 0,
    #                 'SO_TIEN' : 0,
    #                 'CHI_PHI_PHAN_BO' : 0,
    #                 'TEN_CCDC' : line[2].get('TEN_CCDC'),
    #             }
    #         # dict_phan_bo[key]['TY_LE_PB'] += line[2].get('TY_LE')
    #         dict_phan_bo[key]['SO_TIEN'] += line[2].get('SO_TIEN')
    #         dict_phan_bo[key]['CHI_PHI_PHAN_BO'] = line[2].get('CHI_PHI_PHAN_BO')
        
    #     for pb in dict_phan_bo.values():
    #         if pb['SO_TIEN'] != pb['CHI_PHI_PHAN_BO']:
    #             raise ValidationError("Tổng số tiền phân bổ của từng công cụ dụng cụ " +str(pb['TEN_CCDC'])+ " không bằng chi phí phân bổ của công cụ dụng cụ đó.")

    #     result = super(SUPPLY_PHAN_BO_CHI_PHI, self).create(values)
    #     return result

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_ccdc()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.SUPPLY_PHAN_BO_CHI_PHI_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.SO_TIEN,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'TY_GIA' : 1,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_ccdc(self):
        line_ids = []
        thu_tu = 0
        for line in self.SUPPLY_PHAN_BO_CHI_PHI_MUC_CHI_PHI_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'SO_KY_PHAN_BO_GHI_GIAM' : 1,
                'SO_TIEN_PHAN_BO' : line.TONG_SO_TIEN_PHAN_BO,
                'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                'DIEN_GIAI' : '',
                'CCDC_ID' : line.MA_CCDC.id,
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
    