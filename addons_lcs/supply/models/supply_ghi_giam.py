# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision


class SUPPLY_CCDC_GHI_GIAM(models.Model):
    _name = 'supply.ghi.giam'
    _description = 'Ghi giảm công cụ dụng cụ'
    _inherit = ['mail.thread']
    _order = "NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    LY_DO_GHI_GIAM = fields.Selection([('NHUONG_BAN_THANH_LY', 'Nhượng bán, thanh lý'), ('PHAT_HIEN_THIEU_KHI_KIEM_KE', 'Phát hiện thiếu khi kiểm kê'), ('KHAC', 'Khác'), ], string='Lý do ghi giảm', help='Lý do ghi giảm',required=True,default='NHUONG_BAN_THANH_LY')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='supply_ghi_giam_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU', oldname='NAME')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CCDC_ID = fields.Many2one('so.ccdc', ondelete='set null')
    ID_KIEM_KE = fields.Integer()

    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại của CCDC ghi giảm', help='Giá trị còn lại của công cụ dụng cụ ghi giảm',compute='tinh_tong_gia_tri_con_lai',strore=True,digits=decimal_precision.get_precision('VND'))

    SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS = fields.One2many('supply.ghi.giam.chi.tiet', 'CCDC_GHI_GIAM_ID', string='Công cụ dụng cụ ghi giảm chi tiết')

    _sql_constraints = [
	('SO_CHUNG_TU_GGCCDC_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập lại số chứng từ!'),
	]


    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    @api.depends('SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS')
    def tinh_tong_gia_tri_con_lai(self):
        for order in self:
            tong_gia_tri_con_lai = 0
            for line in order.SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS:
                
                tong_gia_tri_con_lai +=line.GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM
                

            order.update({
                'GIA_TRI_CON_LAI':tong_gia_tri_con_lai,
            })



    @api.model
    def default_get(self,default_fields):
        res = super(SUPPLY_CCDC_GHI_GIAM, self).default_get(default_fields)
        res['LOAI_CHUNG_TU'] = 452

        id_kiem_ke = self.get_context('default_ID_KIEM_KE')
        if id_kiem_ke:
            arr_tai_san = []
            kiem_ke = self.env['supply.kiem.ke.cong.cu.dung.cu'].search([('KIEM_KE_CCDC_ID', '=', id_kiem_ke)])
            res['SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS'] = []
            for line in kiem_ke:
                if line.KIEN_NGHI_XU_LY == '1':
                    arr_tai_san += [(0,0,{
                        'MA_CCDC_ID': line.MA_CCDC_ID.id,
                        'TEN_CCDC': line.TEN_CCDC,
                        'DON_VI_SU_DUNG_ID': line.DON_VI_SU_DUNG_ID.id,
                        'SO_LUONG_DANG_DUNG': line.SO_LUONG_TOT,
                        'SO_LUONG_GHI_GIAM': line.SO_LUONG_XU_LY,
                    })]
            res['SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS'] += arr_tai_san

        return res

    @api.multi
    def action_ghi_so(self):
        for record in self:
        # check_dieu_chinh = self.env['so.ccdc.chi.tiet'].search([('LOAI_CHUNG_TU', 'in', ('453','454','451','452')),('NGAY_CHUNG_TU', '>',self.NGAY_CHUNG_TU)],limit = 1).id
        # # check_dieu_chinh = self.env['so.ccdc.chi.tiet'].search([],limit = 1).id
        # if check_dieu_chinh:
        #     ten_ccdc = ''
        #     for line in self.SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS:
        #         ten_ccdc += "<" + line.TEN_CCDC + ">"
        #     raise ValidationError("Ghi sổ không thành công do CCDC " +ten_ccdc+" đã có phát sinh phân bổ, điều chỉnh, điều chuyển hoặc ghi giảm sau ngày hạch toán của chứng từ này. Để ghi sổ chứng từ này thì phải bỏ ghi các chứng từ liên quan.")
            record.ghi_so_ccdc()
        self.write({'state':'da_ghi_so'})
    
    def ghi_so_ccdc(self):
        line_ids = []
        thu_tu = 0
        dien_giai = ''
        if self.LY_DO_GHI_GIAM:
            if self.LY_DO_GHI_GIAM == 'NHUONG_BAN_THANH_LY':
                dien_giai = 'Nhượng bán, thanh lý'
            elif self.LY_DO_GHI_GIAM == 'PHAT_HIEN_THIEU_KHI_KIEM_KE':
                dien_giai = 'Phát hiện thiếu khi kiểm kê'
            elif self.LY_DO_GHI_GIAM == 'KHAC':
                dien_giai = 'Khác'
        for line in self.SUPPLY_CCDC_GHI_GIAM_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'NGAY_CHUNG_TU': self.NGAY_CHUNG_TU,
                'NGAY_HACH_TOAN': self.NGAY_CHUNG_TU,
                'DIEN_GIAI_CHUNG' : self.LY_DO_GHI_GIAM,
                'SO_LUONG_GHI_GIAM' : line.SO_LUONG_GHI_GIAM,
                'DOI_TUONG_PHAN_BO_ID' : line.DON_VI_SU_DUNG_ID.id,
                'CCDC_ID': line.MA_CCDC_ID.id,
                'DIEN_GIAI_CHUNG' : dien_giai,
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

    
    
    

