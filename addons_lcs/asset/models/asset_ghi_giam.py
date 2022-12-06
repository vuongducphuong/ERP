# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class ASSET_TAI_SAN_CO_DINH_GHI_GIAM(models.Model):
    _name = 'asset.ghi.giam'
    _description = 'Ghi giảm TSCĐ'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    LY_DO_GIAM = fields.Selection([('NHUONG_BAN,_THANH_LY', 'Nhượng bán thanh lý'), ('PHAT_HIEN_THIEU_KHI_KIEM_KE', 'Phát hiện thiếu khi kiểm kê'), ('GOP_VON_VAO_CONG_TY_CON', 'Góp vốn vào công ty con'), ('GOP_VON_VAO_CONG_TY_LIEN_DOANH', 'Góp vốn vào công ty liên doanh'), ('GOP_VON_VAO_CONG_TY_LIEN_KET', 'Góp vốn vào công ty liên kết'), ('DAU_TU_DAI_HAN_KHAC', 'Đầu tư dài hạn khác'), ('TRA_LAI_TSCD_THUE_TAI_CHINH', 'Trả lại TSCĐ thuê tài chính'), ('CHUYEN_TSCD_THANH_CCDC', 'Chuyển TSCĐ thành CCDC'),('NHUONG_BAN_THANH_LY_TSCD', 'Nhượng bán thanh lý TSCĐ') ], string='Lý do giảm', help='Lý do giảm',required=True,default='NHUONG_BAN,_THANH_LY')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',default=fields.Datetime.now)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='asset_ghi_giam_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name',related="SO_CHUNG_TU", oldname='NAME')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_TSCD_ID = fields.Many2one('so.tscd', ondelete='set null')
    ID_KIEM_KE = fields.Integer()
    STT_CHUNG_TU = fields.Char(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ', auto_num='asset_STT_CHUNG_TU') 
    _sql_constraints = [
	('SO_CHUNG_TU_GG_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	]

    ASSET_TAI_SAN_CO_DINH_GHI_GIAM_HACH_TOAN_IDS = fields.One2many('asset.ghi.giam.hach.toan', 'TAI_SAN_CO_DINH_GHI_GIAM_ID', string='Tài sản cố định ghi giảm hạch toán')
    ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS = fields.One2many('asset.ghi.giam.tai.san', 'TAI_SAN_CO_DINH_GHI_GIAM_ID', string='Tài sản cố định ghi giảm tài sản')

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())



    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN
            if self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS:
                for line in self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS:
                    line.update_gia_tri_tscd()

    @api.onchange('ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS')
    def tinh_hach_toan(self):
        env = self.env['asset.ghi.giam.hach.toan']
        self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_HACH_TOAN_IDS = []
        for ts in self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS:
            new_line_dong1 = env.new({
                'DIEN_GIAI': 'Giá trị hao mòn lũy kế tài sản',
                'TK_NO_ID': ts.TK_HAO_MON_ID.id,
                'TK_CO_ID': ts.TK_NGUYEN_GIA_ID.id,
                'SO_TIEN': ts.HAO_MON_LUY_KE,   
            })
            new_line_dong2 = env.new({
                'DIEN_GIAI': 'Xử lý giá trị còn lại',
                'TK_NO_ID': ts.TK_XU_LY_GIA_TRI_CON_LAI_ID.id,
                'TK_CO_ID': ts.TK_NGUYEN_GIA_ID.id,
                'SO_TIEN': ts.GIA_TRI_CON_LAI,   
            })
            self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_HACH_TOAN_IDS += new_line_dong1
            self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_HACH_TOAN_IDS += new_line_dong2

    @api.model
    def default_get(self, fields):
        rec = super(ASSET_TAI_SAN_CO_DINH_GHI_GIAM, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 251
        id_kiem_ke = self.get_context('default_ID_KIEM_KE')
        if id_kiem_ke:
            arr_tai_san = []
            kiem_ke = self.env['asset.kiem.ke.tai.san'].search([('KIEM_KE_TAI_SAN_CO_DINH_ID', '=', id_kiem_ke)])
            # env = self.env['asset.ghi.giam.tai.san']
            rec['ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS'] = []
            tk_nguyen_gia = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '2111')],limit=1).id
            tk_hao_mon = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '2141')],limit=1).id
            for line in kiem_ke:
                if line.KIEN_NGHI_XU_LY == '1':
                    arr_tai_san += [(0,0,{
                        'MA_TAI_SAN': line.MA_TAI_SAN.id,
                        'TEN_TAI_SAN': line.TEN_TAI_SAN,
                        'DON_VI_SU_DUNG_ID': line.DON_VI_SU_DUNG_ID.id,
                        'NGUYEN_GIA': line.NGUYEN_GIA,
                        'GIA_TRI_TINH_KHAU_HAO': line.GIA_TRI_TINH_KHAU_HAO,
                        'HAO_MON_LUY_KE': line.HAO_MON_LUY_KE,
                        'GIA_TRI_CON_LAI': line.GIA_TRI_CON_LAI,
                        'TK_NGUYEN_GIA_ID': tk_nguyen_gia,
                        'TK_HAO_MON_ID': tk_hao_mon,
                    })]
            rec['ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS'] += arr_tai_san

        return rec

    @api.model
    def create(self, values):
        
        result = super(ASSET_TAI_SAN_CO_DINH_GHI_GIAM, self).create(values)
        return result
    
    # @api.multi
    # def validate(self, vals, option=None):
    #     ngay_khoa_so = str(self.lay_ngay_khoa_so())
    #     if vals.get('NGAY_CHUNG_TU') < ngay_khoa_so:
    #         raise ValidationError("Ngày chứng từ không được nhỏ hơn ngày khóa sổ " +str(ngay_khoa_so)+ ". Vui lòng kiểm tra lại")

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_tscd()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        dien_giai = ''
        if self.LY_DO_GIAM == 'NHUONG_BAN,_THANH_LY':
            dien_giai = 'Nhượng bán, thanh lý'
        elif self.LY_DO_GIAM == 'PHAT_HIEN_THIEU_KHI_KIEM_KE':
            dien_giai = 'Phát hiện thiếu khi kiểm kê'
        elif self.LY_DO_GIAM == 'GOP_VON_VAO_CONG_TY_CON':
            dien_giai = 'Góp vốn vào công ty con'
        elif self.LY_DO_GIAM == 'GOP_VON_VAO_CONG_TY_LIEN_DOANH':
            dien_giai = 'Góp vốn vào công ty liên doanh'
        elif self.LY_DO_GIAM == 'GOP_VON_VAO_CONG_TY_LIEN_KET':
            dien_giai = 'Góp vốn vào công ty liên kết'
        elif self.LY_DO_GIAM == 'DAU_TU_DAI_HAN_KHAC':
            dien_giai = 'Đầu tư dài hạn khác'
        elif self.LY_DO_GIAM == 'TRA_LAI_TSCD_THUE_TAI_CHINH':
            dien_giai = 'Trả lại TSCĐ thuê tài chính'
        elif self.LY_DO_GIAM == 'CHUYEN_TSCD_THANH_CCDC':
            dien_giai = 'chuyển tSCĐ thành CCDC'
        elif self.LY_DO_GIAM == 'NHUONG_BAN_THANH_LY_TSCD':
            dien_giai = 'Nhượng bán thanh lý TSCĐ'
        for line in self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': dien_giai,
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

    def ghi_so_tscd(self):
        line_ids = []
        thu_tu = 0
        dien_giai = ''
        if self.LY_DO_GIAM == 'NHUONG_BAN,_THANH_LY':
            dien_giai = 'Nhượng bán, thanh lý'
        elif self.LY_DO_GIAM == 'PHAT_HIEN_THIEU_KHI_KIEM_KE':
            dien_giai = 'Phát hiện thiếu khi kiểm kê'
        elif self.LY_DO_GIAM == 'GOP_VON_VAO_CONG_TY_CON':
            dien_giai = 'Góp vốn vào công ty con'
        elif self.LY_DO_GIAM == 'GOP_VON_VAO_CONG_TY_LIEN_DOANH':
            dien_giai = 'Góp vốn vào công ty liên doanh'
        elif self.LY_DO_GIAM == 'GOP_VON_VAO_CONG_TY_LIEN_KET':
            dien_giai = 'Góp vốn vào công ty liên kết'
        elif self.LY_DO_GIAM == 'DAU_TU_DAI_HAN_KHAC':
            dien_giai = 'Đầu tư dài hạn khác'
        elif self.LY_DO_GIAM == 'TRA_LAI_TSCD_THUE_TAI_CHINH':
            dien_giai = 'Trả lại TSCĐ thuê tài chính'
        elif self.LY_DO_GIAM == 'CHUYEN_TSCD_THANH_CCDC':
            dien_giai = 'chuyển tSCĐ thành CCDC'
        elif self.LY_DO_GIAM == 'NHUONG_BAN_THANH_LY_TSCD':
            dien_giai = 'Nhượng bán thanh lý TSCĐ'
        for line in self.ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN_IDS:
            so_tscd = line.MA_TAI_SAN.lay_du_lieu_tren_so(self.NGAY_HACH_TOAN)
            if so_tscd:
                data_ghi_no = helper.Obj.inject(line, self)
                data_ghi_no.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    # 'TSCD_ID' : line.MA_TAI_SAN.id,
                    'DIEN_GIAI_CHUNG' : dien_giai,
                    'GIA_TRI_HAO_MON_LUY_KE' : so_tscd.GIA_TRI_HAO_MON_LUY_KE,
                    # 'GIA_TRI_HAO_MON_LUY_KE' : line.HAO_MON_LUY_KE,
                    'GIA_TRI_KHAU_HAO_THANG' : so_tscd.GIA_TRI_KHAU_HAO_THANG,
                    'TY_LE_KHAU_HAO_THANG' : so_tscd.TY_LE_KHAU_HAO_THANG,
                    'TSCD_ID' : line.MA_TAI_SAN.id,
                    'THOI_GIAN_SU_DUNG' : so_tscd.THOI_GIAN_SU_DUNG,
                    'THOI_GIAN_SU_DUNG_CON_LAI' : so_tscd.THOI_GIAN_SU_DUNG_CON_LAI,
                    'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                })
                line_ids += [(0,0,data_ghi_no)]
                thu_tu += 1
            else:
                # raise ValidationError('Tài sản cố định này chưa được ghi sổ. Vui lòng ghi sổ lại tài sản cố định này')
                _logger.warn("Tài sản cố định này chưa được ghi sổ. Vui lòng ghi sổ lại tài sản cố định này")
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