# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH(models.Model):
    _name = 'asset.danh.gia.lai'
    _description = 'Đánh giá lại tài sản cố định'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc"

    BIEN_BAN_SO = fields.Char(string='Biên bản số', help='Biên bản số')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    LY_DO = fields.Selection([('NANG_CAP_TSCD_LAM_TANG_THOI_GIAN_SU_DUNG_HOAC_GIA_TRI_TAI_SAN', 'Nâng cấp TSCĐ làm tăng thời gian sử dụng hoặc giá trị tài sản'), ('THAO_DO_MOT_HAY_MOT_SO_BO_PHAN_TAI_SAN_GIAM_GIA_TRI_TAI_SAN', 'Tháo dỡ một hay một số bộ phận tài sản giảm giá trị tài sản'), ('DANH_GIA_LAI_TAI_SAN_CO_DINH_DE_XAC_DINH_GIA_TRI_DOANH_NGHIEP', 'Đánh giá lại tài sản cố định để xác định giá trị doanh nghiệp'), ('DANH_GIA_LAI_TAI_SAN_NHAM_MUC_DICH_LIEN_DOANH_GOP_VON_CHIA_TACH_HOP_NHAT_GIAI_THE', 'Đánh giá lại tài sản nhằm mục đích liên doanh, góp vốn, chia tách, hợp nhất, giải thể'), ('DANH_GIA_LAI_THEO_YEU_CAU_KE_BIEN_TAI_SAN_CUA_CO_QUAN_CO_THAM_QUYEN_NHA_NUOC', 'Đánh giá lại theo yêu cầu kê biên tài sản của cơ quan có thẩm quyền nhà nước'),('SUA_CHUA_TAI_SAN_LAM_TANG_GIA_TRI_CUA_TAI_SAN','Sửa chữa tài sản làm tăng giá trị của tàn sản') ], string='Lý do', help='Lý do',required=True,default='NANG_CAP_TSCD_LAM_TANG_THOI_GIAN_SU_DUNG_HOAC_GIA_TRI_TAI_SAN')
    KET_LUAN = fields.Text(string='Kết luận', help='Kết luận')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',required=True,default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='asset_danh_gia_lai_SO_CHUNG_TU',required=True)
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_TSCD_ID = fields.Many2one('so.tscd', ondelete='set null')
    name = fields.Char(string='Name',related='SO_CHUNG_TU',store=True, oldname='NAME')
    STT_CHUNG_TU = fields.Char(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ', auto_num='asset_STT_CHUNG_TU') 
    _sql_constraints = [
	('SO_CHUNG_TU_DGL_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	]

    ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_HACH_TOAN_IDS = fields.One2many('asset.danh.gia.lai.hach.toan', 'DANH_GIA_LAI_TAI_SAN_CO_DINH_ID', string='Đánh giá lại tài sản cố định hạch toán')
    ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_THANH_VIEN_THAM_GIA_IDS = fields.One2many('asset.danh.gia.lai.thanh.vien.tham.gia', 'DANH_GIA_LAI_TAI_SAN_CO_DINH_ID', string='Đánh giá lại tài sản cố định thành viên tham gia')
    ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH_IDS = fields.One2many('asset.danh.gia.lai.chi.tiet.dieu.chinh', 'DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID', string='Đánh giá lại tài sản cố định chi tiết điều chỉnh')

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.model
    def default_get(self, fields):
        rec = super(ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 252
        return rec

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_tscd()
        self.write({'state':'da_ghi_so'})
    
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        dien_giai_chung = ''
        if self.LY_DO == 'NANG_CAP_TSCD_LAM_TANG_THOI_GIAN_SU_DUNG_HOAC_GIA_TRI_TAI_SAN':
            dien_giai_chung = 'Nâng cấp TSCĐ làm tăng thời gian sử dụng hoặc giá trị tài sản'
        elif self.LY_DO == 'THAO_DO_MOT_HAY_MOT_SO_BO_PHAN_TAI_SAN_GIAM_GIA_TRI_TAI_SAN':
            dien_giai_chung = 'Tháo dỡ một hay một số bộ phận tài sản giảm giá trị tài sản'
        elif self.LY_DO == 'DANH_GIA_LAI_TAI_SAN_CO_DINH_DE_XAC_DINH_GIA_TRI_DOANH_NGHIEP':
            dien_giai_chung = 'Đánh giá lại tài sản cố định để xác định giá trị doanh nghiệp'
        elif self.LY_DO == 'DANH_GIA_LAI_TAI_SAN_NHAM_MUC_DICH_LIEN_DOANH_GOP_VON_CHIA_TACH_HOP_NHAT_GIAI_THE':
            dien_giai_chung = 'Đánh giá lại tài sản nhằm mục đích liên doanh, góp vốn, chia tách, hợp nhất, giải thể'
        elif self.LY_DO == 'DANH_GIA_LAI_THEO_YEU_CAU_KE_BIEN_TAI_SAN_CUA_CO_QUAN_CO_THAM_QUYEN_NHA_NUOC':
            dien_giai_chung = 'Đánh giá lại theo yêu cầu kê biên tài sản của cơ quan có thẩm quyền nhà nước'
        elif self.LY_DO == 'SUA_CHUA_TAI_SAN_LAM_TANG_GIA_TRI_CUA_TAI_SAN':
            dien_giai_chung = 'Sửa chữa tài sản làm tăng giá trị của tàn sản'

        for line in self.ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                # 'DIEN_GIAI_CHUNG': dien_giai_chung,
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
        dien_giai_chung = ''
        if self.LY_DO == 'NANG_CAP_TSCD_LAM_TANG_THOI_GIAN_SU_DUNG_HOAC_GIA_TRI_TAI_SAN':
            dien_giai_chung = 'Nâng cấp TSCĐ làm tăng thời gian sử dụng hoặc giá trị tài sản'
        elif self.LY_DO == 'THAO_DO_MOT_HAY_MOT_SO_BO_PHAN_TAI_SAN_GIAM_GIA_TRI_TAI_SAN':
            dien_giai_chung = 'Tháo dỡ một hay một số bộ phận tài sản giảm giá trị tài sản'
        elif self.LY_DO == 'DANH_GIA_LAI_TAI_SAN_CO_DINH_DE_XAC_DINH_GIA_TRI_DOANH_NGHIEP':
            dien_giai_chung = 'Đánh giá lại tài sản cố định để xác định giá trị doanh nghiệp'
        elif self.LY_DO == 'DANH_GIA_LAI_TAI_SAN_NHAM_MUC_DICH_LIEN_DOANH_GOP_VON_CHIA_TACH_HOP_NHAT_GIAI_THE':
            dien_giai_chung = 'Đánh giá lại tài sản nhằm mục đích liên doanh, góp vốn, chia tách, hợp nhất, giải thể'
        elif self.LY_DO == 'DANH_GIA_LAI_THEO_YEU_CAU_KE_BIEN_TAI_SAN_CUA_CO_QUAN_CO_THAM_QUYEN_NHA_NUOC':
            dien_giai_chung = 'Đánh giá lại theo yêu cầu kê biên tài sản của cơ quan có thẩm quyền nhà nước'
        elif self.LY_DO == 'SUA_CHUA_TAI_SAN_LAM_TANG_GIA_TRI_CUA_TAI_SAN':
            dien_giai_chung = 'Sửa chữa tài sản làm tăng giá trị của tài sản'
        for line in self.ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH_IDS:
            tscd = line.MA_TAI_SAN_ID.lay_du_lieu_tren_so(self.NGAY_HACH_TOAN)
            tk_khau_hao = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '2141')],limit=1).id
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI_CHUNG' : dien_giai_chung,
                'DIEN_GIAI' : '',
                'TSCD_ID' : line.MA_TAI_SAN_ID.id,
                'THOI_GIAN_SU_DUNG_CON_LAI' : line.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH,
                'GIA_TRI_KHAU_HAO_THANG' : line.GTKH_THANG_SAU_DIEU_CHINH,
                'GIA_TRI_TINH_KHAU_HAO' : line.GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH,
                'GIA_TRI_CON_LAI' : line.GIA_TRI_CON_LAI_SAU_DIEU_CHINH,
                'CHENH_LECH_THOI_GIAN_SU_DUNG' : line.CHENH_LECH_THOI_GIAN,
                'CHENH_LECH_GIA_TRI_TINH_KHAU_HAO' : line.CHENH_LECH_GTKH,
                'CHENH_LECH_GIA_TRI_CON_LAI' : line.CHENH_LECH_GIA_TRI,
                'GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH' : line.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH,
                'TY_LE_KHAU_HAO_THANG' : 1/line.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH*100 if line.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH !=0 else 0,
                'GIA_TRI_HAO_MON_LUY_KE' : tscd.GIA_TRI_HAO_MON_LUY_KE if tscd else 0,
                'LOAI_TSCD_ID' : tscd.LOAI_TSCD_ID.id if tscd else 0,
                'TK_NGUYEN_GIA_ID' : tscd.TK_NGUYEN_GIA_ID.id if tscd else 0,
                'NGUYEN_GIA' : tscd.NGUYEN_GIA if tscd else 0,
                'THOI_GIAN_SU_DUNG' : tscd.THOI_GIAN_SU_DUNG if tscd else 0,
                'TK_HAO_MON_ID' : tk_khau_hao,
                'DON_VI_SU_DUNG_ID' : line.DON_VI_SU_DUNG.id,
                'CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE' : line.CHENH_LECH_HAO_MON_LUY_KE,
                'TONG_CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE' : line.CHENH_LECH_HAO_MON_LUY_KE,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                
            })
            line_ids += [(0,0,data_ghi_no)]
            thu_tu += 1
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

    
    @api.model
    def create(self, vals):
        # if not vals.get('ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH_IDS.MA_TAI_SAN_ID'):
        #      raise ValidationError("<Mã tài sản> không được bỏ trống.")
        
        result = super(ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH, self).create(vals)
        return result

	# Updated 2019-04-26 by anhtuan: Có hàm chung
    # @api.multi
    # def validate(self, vals, option=None):
        # ngay_khoa_so = str(self.lay_ngay_khoa_so())
        # if vals.get('NGAY_CHUNG_TU') < ngay_khoa_so:
            # raise ValidationError("Ngày chứng từ không được nhỏ hơn ngày khóa sổ " +str(ngay_khoa_so)+ ". Vui lòng kiểm tra lại")

            
    @api.onchange('ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH_IDS')
    def tinh_hach_toan(self):
        env = self.env['asset.danh.gia.lai.hach.toan']
        self.ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_HACH_TOAN_IDS = []
        check_tk_no_khau_hao = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '2111')],limit=1)
        check_tk_Co_khau_hao = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '2141')],limit=1)
        tk_no_khau_hao = ''
        tk_Co_khau_hao = ''
        if check_tk_no_khau_hao:
            tk_no_khau_hao = check_tk_no_khau_hao.id
        if check_tk_Co_khau_hao:
            tk_Co_khau_hao = check_tk_Co_khau_hao.id
        for ts in self.ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH_IDS:
            if ts.CHENH_LECH_GIA_TRI > 0:
                new_line_dong1 = env.new({
                    'DIEN_GIAI': 'Điều chỉnh tăng giá trị của tài sản <'+str(ts.TEN_TAI_SAN)+">",
                    'TK_NO_ID': tk_no_khau_hao,
                    'TK_CO_ID': ts.TK_DANH_GIA_LAI_GTKH.id,
                    'SO_TIEN': ts.CHENH_LECH_GIA_TRI + ts.CHENH_LECH_HAO_MON_LUY_KE,   
                })
                self.ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_HACH_TOAN_IDS += new_line_dong1
            if ts.CHENH_LECH_HAO_MON_LUY_KE > 0: 
                new_line_dong2 = env.new({
                    'DIEN_GIAI': 'Điều chỉnh tăng hao mòn lũy kế của tài sản <'+str(ts.TEN_TAI_SAN)+">",
                    # 'TK_NO_ID': ts.TK_XU_LY_GIA_TRI_CON_LAI_ID.id,
                    'TK_CO_ID': tk_Co_khau_hao,
                    'SO_TIEN': ts.CHENH_LECH_HAO_MON_LUY_KE,   
                })
                self.ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_HACH_TOAN_IDS += new_line_dong2

    