# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class TIEN_LUONG_BANG_LUONG_CHI_TIET(models.Model):
    _name = 'tien.luong.bang.luong.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    _order = "STT,id"
    
    STT = fields.Integer(string='STT', help='Số thứ tự')
    MA_NHAN_VIEN = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên', related='MA_NHAN_VIEN.HO_VA_TEN',store=True)
    PHONG_BAN = fields.Char(string='Phòng ban', help='Phòng ban')
    CHUC_DANH = fields.Char(string='Chức danh', help='Chức danh')
    LUONG_CO_BAN = fields.Float(string='Lương cơ bản', help='Lương cơ bản',digits= decimal_precision.get_precision('VND'))
    DON_GIA_NGAY_CONG = fields.Float(string='Đơn giá ngày công', help='Đơn giá ngày công',digits= decimal_precision.get_precision('VND'))
    DON_GIA_GIO_CONG = fields.Float(string='Đơn giá giờ công', help='Đơn giá giờ công',digits= decimal_precision.get_precision('VND'))
	# Updated 2019-09-10 by anhtuan: Merge SO_NGAY_CONG_HUONG-SO_GIO_CONG_HUONG, SO_NGAY_CONG_KHONG_HUONG/SO_GIO_CONG_KHONG_HUONG (like MS)
    # SO_NGAY_CONG_HUONG = fields.Float(string='Số ngày công', help='Số ngày công hưởng 100% lương',digits= decimal_precision.get_precision('VND'))
    SO_CONG_HUONG = fields.Float(string='Số công', help='Số công hưởng 100% lương',digits= decimal_precision.get_precision('VND'), oldname='SO_GIO_CONG_HUONG')
    SO_TIEN_HUONG = fields.Float(string='Số tiền', help='Số tiền hưởng 100% lương',digits= decimal_precision.get_precision('VND'))
    SO_CONG_KHONG_HUONG = fields.Float(string='Số công', help='Số công không hưởng 100% lương',digits= decimal_precision.get_precision('VND'), oldname='SO_NGAY_CONG_KHONG_HUONG')
    # SO_GIO_CONG_KHONG_HUONG = fields.Float(string='Số giờ công', help='Số giờ công không hưởng 100% lương',digits= decimal_precision.get_precision('VND'))
    SO_TIEN_KHONG_HUONG = fields.Float(string='Số tiền', help='Số tiền không hưởng 100% lương',digits= decimal_precision.get_precision('VND'))
    SO_GIO_CONG_LAM_THEM = fields.Float(string='Số giờ công', help='Số giờ công lương làm thêm',digits= decimal_precision.get_precision('VND'))
    SO_TIEN_LAM_THEM = fields.Float(string='Số tiền', help='Số tiền lương làm thêm',digits= decimal_precision.get_precision('VND'))
    PHU_CAP_THUOC_QUY_LUONG = fields.Float(string='Phụ cấp thuộc quỹ lương', help='Phụ cấp thuộc quỹ lương',digits= decimal_precision.get_precision('VND'))
    PHU_CAP_KHAC = fields.Float(string='Phụ cấp khác', help='Phụ cấp khác',digits= decimal_precision.get_precision('VND'))
    TONG_SO = fields.Float(string='Tổng số', help='Tổng số',digits= decimal_precision.get_precision('VND'))
    SO_TIEN_TAM_UNG = fields.Float(string='Số tiền tạm ứng', help='Số tiền tạm ứng',digits= decimal_precision.get_precision('VND'))
    LUONG_DONG_BH = fields.Float(string='Lương đóng BH', help='Lương đóng bảo hiểm',digits= decimal_precision.get_precision('VND'))
    BHXH_KHAU_TRU = fields.Float(string='BHXH', help='Bảo hiểm xã hội',digits= decimal_precision.get_precision('VND'))
    BHYT_KHAU_TRU = fields.Float(string='BHYT', help='Bảo hiểm y tế',digits= decimal_precision.get_precision('VND'))
    BHTN_KHAU_TRU = fields.Float(string='BHTN', help='Bảo hiểm thất nghiệp',digits= decimal_precision.get_precision('VND'))
    KPCD_KHAU_TRU = fields.Float(string='KPCĐ', help='Kinh phí công đoàn',digits= decimal_precision.get_precision('VND'))
    THUE_TNCN_KHAU_TRU = fields.Float(string='Thuế TNCN', help='Thuế thu nhập cá nhân',digits= decimal_precision.get_precision('VND'))
    CONG_KHAU_TRU = fields.Float(string='Cộng', help='Cộng',digits= decimal_precision.get_precision('VND'))
    GIAM_TRU_GIA_CANH = fields.Float(string='Giảm trừ gia cảnh', help='Giảm trừ gia cảnh',digits= decimal_precision.get_precision('VND'))
    TONG_THU_NHAP_CHIU_THUE_TNCN = fields.Float(string='Tổng thu nhập chịu thuế TNCN', help='Tổng thu nhập chịu thuế thu nhập cá nhân',digits= decimal_precision.get_precision('VND'))
    THU_NHAP_TINH_THUE_TNCN = fields.Float(string='Thu nhập tính thuế TNCN', help='Thu nhập tính thuế thu nhập cá nhân',digits= decimal_precision.get_precision('VND'))
    SO_TIEN_CON_DUOC_LINH = fields.Float(string='Số tiền còn được lĩnh', help='Số tiền còn được lĩnh',digits= decimal_precision.get_precision('VND'))
    BHXH_CONG_TY_DONG = fields.Float(string='BHXH', help='Bảo hiểm xã hội công ty đóng',digits= decimal_precision.get_precision('VND'))
    BHYT_CONG_TY_DONG = fields.Float(string='BHYT', help='Bảo hiểm y tế công ty đóng',digits= decimal_precision.get_precision('VND'))
    BHTN_CONG_TY_DONG = fields.Float(string='BHTN', help='Bảo hiểm thất nghiệp công ty đóng',digits= decimal_precision.get_precision('VND'))
    KPCD_CONG_TY_DONG = fields.Float(string='KPCĐ', help='Kinh phí công đoàn công ty đóng',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', oldname='NAME')
    CHI_TIET_ID = fields.Many2one('tien.luong.bang.luong', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị')
    TONG_PHU_CAP = fields.Float(string='Tổng phụ cấp', help='Tổng phụ cấp' ,digits= decimal_precision.get_precision('VND') ,store=True,compute='lay_tong_phu_cap' ) 
    KY_NHAN = fields.Char(string='Ký nhận', help='Ký nhận')
    HE_SO_LUONG = fields.Float(string='Hệ số lương', help='Hệ số lương',digits= decimal_precision.get_precision('VND'))
    TAM_UNG_141 = fields.Float(string='Tạm ứng 141', help='Tạm ứng 141',digits= decimal_precision.get_precision('VND'))
    TEN_LOAI_BANG_LUONG = fields.Selection([
        ('LUONG_CO_DINH', 'Lương cố định(không dựa trên bảng chấm công)'), 
        ('LUONG_THOI_GIAN_THEO_BUOI', 'Lương thời gian theo buổi'), 
        ('LUONG_THOI_GIAN_THEO_GIO', 'Lương thời gian theo giờ'), 
        ('LUONG_TAM_UNG', 'Lương tạm ứng'), ], related='CHI_TIET_ID.TEN_LOAI_BANG_LUONG', )

    @api.depends('PHU_CAP_THUOC_QUY_LUONG','PHU_CAP_KHAC')
    def lay_tong_phu_cap(self):
        phuCap = 0
        for record in self:
            phuCap = record.PHU_CAP_THUOC_QUY_LUONG + record.PHU_CAP_KHAC
            record.update({
                'TONG_PHU_CAP': phuCap,
            })

    @api.onchange('THU_NHAP_TINH_THUE_TNCN')
    def update_thue_tncn(self):
        thue_tncn = 0
        thue_tncn = self.CHI_TIET_ID.static_PersonalIncomeTax(self.THU_NHAP_TINH_THUE_TNCN)
        self.THUE_TNCN_KHAU_TRU  = thue_tncn

    # Tổng số = Lương cơ bản + phụ cấp thuộc quỹ lương + phụ cấp khác
    @api.onchange('LUONG_CO_BAN','PHU_CAP_THUOC_QUY_LUONG','PHU_CAP_KHAC','SO_TIEN_HUONG','SO_TIEN_KHONG_HUONG','SO_TIEN_LAM_THEM')
    def update_tong_so(self):
        # Bảng lương cố định
        if self.TEN_LOAI_BANG_LUONG == 'LUONG_CO_DINH':
            self.TONG_SO = self.LUONG_CO_BAN + self.PHU_CAP_THUOC_QUY_LUONG + self.PHU_CAP_KHAC

        elif self.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_BUOI':
            # Tính tổng số
            self.TONG_SO = self.PHU_CAP_THUOC_QUY_LUONG + self.PHU_CAP_KHAC + self.SO_TIEN_HUONG + self.SO_TIEN_KHONG_HUONG + self.SO_TIEN_LAM_THEM
            
        elif self.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_GIO':
            # Tính tổng số
            self.TONG_SO = self.PHU_CAP_THUOC_QUY_LUONG + self.PHU_CAP_KHAC + self.SO_TIEN_HUONG + self.SO_TIEN_KHONG_HUONG + self.SO_TIEN_LAM_THEM
            
    @api.onchange('LUONG_CO_BAN')
    def update_don_gia_ngay_cong_va_don_gia_gio_cong(self):
        self.SO_TIEN_KHONG_HUONG = 0
        self.SO_TIEN_LAM_THEM = 0
        
        if self.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_BUOI':
        # Tính đơn giá ngày công khi thay đổi  Lương cơ bản
            env_quy_dinh_luong_bh_thue= self.env['tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'].search([],limit=1)
            so_ngay_cong_trong_thang = 0
            don_gia_ngay_cong = 0 
            if env_quy_dinh_luong_bh_thue:
                so_ngay_cong_trong_thang= env_quy_dinh_luong_bh_thue.SO_NGAY_TINH_CONG_TRONG_THANG
            if so_ngay_cong_trong_thang != 0:
                don_gia_ngay_cong = self.LUONG_CO_BAN / so_ngay_cong_trong_thang
            self.DON_GIA_NGAY_CONG = don_gia_ngay_cong

        elif self.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_GIO':
            # Tính đơn giá giờ công khi thay đổi  Lương cơ bản
            env_quy_dinh_luong_bh_thue= self.env['tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'].search([],limit=1)
            so_ngay_cong_trong_thang = 0
            so_gio_cong_trong_ngay = 0
            don_gia_ngay_cong = 0
            don_gia_gio_cong = 0
            if env_quy_dinh_luong_bh_thue:
                so_ngay_cong_trong_thang = env_quy_dinh_luong_bh_thue.SO_NGAY_TINH_CONG_TRONG_THANG
                so_gio_cong_trong_ngay = env_quy_dinh_luong_bh_thue.SO_GIO_TINH_CONG_TRONG_NGAY
            if so_ngay_cong_trong_thang != 0:
                don_gia_ngay_cong = self.LUONG_CO_BAN / so_ngay_cong_trong_thang
            if so_gio_cong_trong_ngay != 0:
                don_gia_gio_cong = don_gia_ngay_cong / so_gio_cong_trong_ngay

            self.DON_GIA_NGAY_CONG = don_gia_ngay_cong
            self.DON_GIA_GIO_CONG = don_gia_gio_cong

    # Tính lương theo giờ - Tính số tiền hưởng 100% lương sau khi thay đổi số giờ  công
    @api.onchange('SO_CONG_HUONG','DON_GIA_GIO_CONG','DON_GIA_NGAY_CONG')
    def update_so_tien_huong_100_luong_theo_gio(self):
        # Số tiền lương thời gian được hưởng 100% lương
        if self.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_GIO':
            self.SO_TIEN_HUONG = self.SO_CONG_HUONG * self.DON_GIA_GIO_CONG
        elif self.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_BUOI':
            self.SO_TIEN_HUONG = self.SO_CONG_HUONG * self.DON_GIA_NGAY_CONG
    
    # Tính lương theo buổi - Tính số tiền hưởng 100% lương sau khi thay đổi số ngày  công
    # @api.onchange('SO_NGAY_CONG_HUONG','DON_GIA_NGAY_CONG')
    # def update_so_tien_huong_100_luong_theo_buoi(self):
        # Số tiền lương thời gian được hưởng 100% lương
        # self.SO_TIEN_HUONG = self.SO_NGAY_CONG_HUONG * self.DON_GIA_NGAY_CONG
    
    # Nhân viên
    # BHXH khấu trừ = Lương đóng BH * BHXH (%) /100
    # BHYT khấu trừ = Lương đóng BH * BHYT (%) /100
    # BHTN khấu trừ = Lương đóng BH * BHTN (%) /100
    # KPCĐ khấu trừ = Lương đóng BH * KPCĐ (%) /100
    @api.onchange('LUONG_DONG_BH')
    def update_bao_hiem_nhan_vien(self):
        env = self.env['tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'].search([],limit=1)
        kpcd_khau_tru_nhan_vien = 0
        if env:
            self.BHXH_KHAU_TRU = (self.LUONG_DONG_BH * env.BAO_HIEM_XA_HOI_NV_DONG) / 100
            self.BHYT_KHAU_TRU = (self.LUONG_DONG_BH * env.BAO_HIEM_Y_TE_NV_DONG) / 100
            self.BHTN_KHAU_TRU = (self.LUONG_DONG_BH * env.BAO_HIEM_THAT_NGHIEP_NV_DONG) / 100
            kpcd_khau_tru_nhan_vien = (self.LUONG_DONG_BH * env.KINH_PHI_CONG_DOAN_NV_DONG) / 100
            self.BHXH_CONG_TY_DONG = (self.LUONG_DONG_BH * env.BAO_HIEM_XA_HOI_CONG_TY_DONG) / 100
            self.BHYT_CONG_TY_DONG = (self.LUONG_DONG_BH * env.BAO_HIEM_Y_TE_CONG_TY_DONG) / 100
            self.BHTN_CONG_TY_DONG = (self.LUONG_DONG_BH * env.BAO_HIEM_THAT_NGHIEP_CONG_TY_DONG) / 100
            self.KPCD_CONG_TY_DONG = (self.LUONG_DONG_BH * env.KINH_PHI_CONG_DOAN_CONG_TY_DONG) / 100
        
        self.KPCD_KHAU_TRU = kpcd_khau_tru_nhan_vien
           
    # Cộng các khoản khấu trừ = BHXH khấu trừ + BHYT khấu trừ + BHTN khấu trừ + KPCĐ khấu trừ + Thuế TNCN
    @api.onchange('BHXH_KHAU_TRU','BHYT_KHAU_TRU','BHTN_KHAU_TRU','KPCD_KHAU_TRU','THUE_TNCN_KHAU_TRU')
    def update_cong_cac_khoan_giam_tru(self):
        self.CONG_KHAU_TRU = self.BHXH_KHAU_TRU + self.BHYT_KHAU_TRU + self.BHTN_KHAU_TRU + self.KPCD_KHAU_TRU + self.THUE_TNCN_KHAU_TRU
   
    # Tổng thu nhập chịu thuế TNCN = Tổng số
    @api.onchange('TONG_SO')
    def update_tong_thu_nhap_chiu_thue_tncn(self):
        self.TONG_THU_NHAP_CHIU_THUE_TNCN = self.TONG_SO

    #Thu nhập tính thuế TNCN = Tổng thu nhập chịu thuế TNCN - Giảm trừ gia cảnh - (bhxh khấu trừ + bhyt khấu trừ + bhtn khấu trừ + kpcđ khấu trừ)
    @api.onchange('TONG_THU_NHAP_CHIU_THUE_TNCN','GIAM_TRU_GIA_CANH','BHXH_KHAU_TRU','BHYT_KHAU_TRU','BHTN_KHAU_TRU','KPCD_KHAU_TRU')
    def update_thu_nhap_tinh_thue_tncn(self):
        thu_nhap_tinh_thue = 0
        thu_nhap_tinh_thue = self.TONG_THU_NHAP_CHIU_THUE_TNCN - self.GIAM_TRU_GIA_CANH - (self.BHXH_KHAU_TRU + self.BHYT_KHAU_TRU + self.BHTN_KHAU_TRU)
        if thu_nhap_tinh_thue > 0:
            self.THU_NHAP_TINH_THUE_TNCN = thu_nhap_tinh_thue
        else:
            self.THU_NHAP_TINH_THUE_TNCN = 0
    # Số tiền còn được lĩnh = Tổng số  - số tiền tạm ứng - tổng các khoản khấu trừ
    @api.onchange('TONG_SO','SO_TIEN_TAM_UNG','CONG_KHAU_TRU')
    def update_so_tien_con_duoc_linh(self):
        self.SO_TIEN_CON_DUOC_LINH = self.TONG_SO - self.SO_TIEN_TAM_UNG - self.CONG_KHAU_TRU

    # Nhân viên
    # BHXH khấu trừ = Lương đóng BH * BHXH (%) /100
    # BHYT khấu trừ = Lương đóng BH * BHYT (%) /100
    # BHTN khấu trừ = Lương đóng BH * BHTN (%) /100
    # KPCĐ khấu trừ = Lương đóng BH * KPCĐ (%) /100