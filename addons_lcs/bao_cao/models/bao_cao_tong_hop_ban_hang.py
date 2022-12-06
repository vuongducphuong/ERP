# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_BAN_HANG(models.Model):
    _name = 'bao.cao.tong.hop.ban.hang'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('MAT_HANG', 'Mặt hàng'),('MAT_HANG_KHACH_HANG', 'Mặt hàng và khách hàng'),('MAT_HANG_NHAN_VIEN', 'Mặt hàng và nhân viên'),('KHACH_HANG', 'Khách hàng'),('NHAN_VIEN', 'Nhân viên'),('NHAN_VIEN_VA_KHACH_HANG', 'Nhân viên và khách hàng'),('NHAN_VIEN_KHACH_HANG_MATHANG', 'Nhân viên, khách hàng và mặt hàng'),('DIA_PHUONG', 'Địa phương'),('DON_VI_KINH_DOANH', 'Đơn vị kinh doanh'),('DON_VI_KINH_DOANH_VA_MAT_HANG', 'Đơn vị kinh doanh và mặt hàng'),('NHOM_KHACH_HANG', 'Nhóm khách hàng'),], string='Thống kê theo', help='Thống kê theo',default='MAT_HANG',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    CHI_LAY_KHACH_HANG_CO_PHAT_SINH = fields.Boolean(string='Chỉ lấy khách hàng có phát sinh', help='Chỉ lấy khách hàng có phát sinh',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',required=True,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày ', help='Đến ngày',required=True,default=fields.Datetime.now)
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', ' Đơn vị chuyển đổi 2 '), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH',required=True)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH ', help='Nhóm vật tư hàng hóa ')
    CHON_KHACH_HANG = fields.Boolean(string='Chọn KH', help='Chọn khách hàng')
    MAT_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mặt hàng ', help='Mặt hàng ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NHOM_KHACH_HANG_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm khách hàng', help='Thống kê theo')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Chi nhánh')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')

    
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG_BAN = fields.Float(string='Số lượng bán ', help='Số lượng bán ', digits=decimal_precision.get_precision('SO_LUONG'))
    DOANH_SO_BAN = fields.Float(string='Doanh số bán', help='Doanh số bán',digits= decimal_precision.get_precision('VND'))
    CHIET_KHAU = fields.Float(string='Chiết khấu', help='Chiết khấu',digits= decimal_precision.get_precision('VND'))
    SO_LUONG_TRA_LAI = fields.Integer(string='Số lượng trả lại', help='Số lượng trả lại',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_TRA_LAI = fields.Float(string='Giá trị trả lại', help='Giá trị trả lại',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_GIAM_GIA = fields.Float(string='Giá trị giảm giá', help='Giá trị giảm giá',digits= decimal_precision.get_precision('VND'))
    DOANH_THU_THUAN = fields.Float(string='Doanh thu thuần', help='Doanh thu thuần',digits= decimal_precision.get_precision('VND'))
    MA_KHACH_HANG = fields.Char(string='Mã khách hàng', help='Mã khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')

    TINH_THANH_PHO = fields.Char(string='Tỉnh/Thành phố', help='Tỉnh/Thành phố')
    QUAN_HUYEN = fields.Char(string='Quận/Huyện', help='Quận/Huyện')
    XA_PHUONG = fields.Char(string='Xã/Phường', help='Xã/Phường')

    DON_VI_KINH_DOANH  = fields.Char(string='Đơn vị kinh doanh', help='Đơn vị kinh doanh')
    TIEN_VON  = fields.Float(string='Tiền vốn', help='Tiền vốn',digits= decimal_precision.get_precision('VND'))
    DON_GIA_VON  = fields.Float(string='Đơn giá vốn', help='Đơn giá vốn',digits= decimal_precision.get_precision('VND'))
    LAI_GOP  = fields.Float(string='Lãi gộp', help='Lãi gộp',digits= decimal_precision.get_precision('VND'))
    TY_LE_LAI_GOP  = fields.Float(string='Tỷ lệ lãi gộp (%)', help='Tỷ lệ lãi gộp (%)',digits= decimal_precision.get_precision('VND'))
    MA_NHOM_KH  = fields.Char(string='Mã nhóm khách hàng', help='Mã nhóm khách hàng')
    TEN_NHOM_KH  = fields.Char(string='Tên nhóm khách hàng', help='Tên nhóm khách hàng')
    MA_DON_VI  = fields.Char(string='Mã đơn vị', help='Mã đơn vị')
    TEN_DON_VI  = fields.Char(string='Tên đơn vị', help='Tên đơn vị')
    SO_LUONG_KM = fields.Float(string='Số lượng KM', help='Số lượng khuyến mãi', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_HANG_KM_TRA_LAI = fields.Float(string='SL hàng KM trả lại', help='Số lượng hàng khuyến mãi trả lại', digits=decimal_precision.get_precision('SO_LUONG'))





    MAT_HANG_IDS_ID_MATHANG = fields.One2many('danh.muc.vat.tu.hang.hoa')
    MAT_HANG_IDS_ID_MATHANG_KH = fields.One2many('danh.muc.vat.tu.hang.hoa')
    MAT_HANG_IDS_ID_MATHANG_NV = fields.One2many('danh.muc.vat.tu.hang.hoa')
    MAT_HANG_IDS_ID_DVKD = fields.One2many('danh.muc.vat.tu.hang.hoa')
    MAT_HANG_IDS_ID_DVKD_MATHANG = fields.One2many('danh.muc.vat.tu.hang.hoa')


    KHACH_HANG_IDS_ID_MATHANG_KH = fields.One2many('res.partner')
    NHAN_VIEN_IDS_ID_MATHANG_NV = fields.One2many('res.partner')
    KHACH_HANG_IDS_ID_KHACH_HANG = fields.One2many('res.partner')
    NHAN_VIEN_IDS_ID_NHANVIEN = fields.One2many('res.partner')
    NHAN_VIEN_IDS_ID_NV_KH = fields.One2many('res.partner')
    KHACH_HANG_IDS_ID_NV_KH = fields.One2many('res.partner')
    NHAN_VIEN_IDS_ID_NV_KH_MH = fields.One2many('res.partner')
    KHACH_HANG_IDS_ID_NV_KH_MH = fields.One2many('res.partner')

    CHON_KHACH_HANG_IDS = fields.One2many('res.partner')

    DON_VI_IDS_DVKD_MH = fields.One2many('danh.muc.to.chuc')
    NHOM_KH_IDS = fields.One2many('danh.muc.nhom.khach.hang.nha.cung.cap')

    

    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','bao_cao_so_chi_tiet_vthh_danh_muc_vthh_rel', string='Chọn sản phẩm') 
    MA_PC_NHOM_VTHH = fields.Char()

    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner', domain=[('LA_KHACH_HANG', '=', True)], string='Chọn KH')
    MA_PC_NHOM_KH = fields.Char()

    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')
    MA_PC_NHOM_NV = fields.Char()


    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):
        self.CHON_TAT_CA_SAN_PHAM = True
        self.CHON_TAT_CA_KHACH_HANG = True
        self.CHON_TAT_CA_NHAN_VIEN = True
        self.SAN_PHAM_MANY_IDS = []
        self.KHACH_HANG_MANY_IDS = []
        self.NHAN_VIEN_MANY_IDS = []

    # ------------------------------Mặt hàng ---------------------------------------

    @api.onchange('MAT_HANG_IDS_ID_MATHANG','MAT_HANG_IDS_ID_MATHANG_KH','MAT_HANG_IDS_ID_MATHANG_NV','MAT_HANG_IDS_ID_DVKD','MAT_HANG_IDS_ID_DVKD_MATHANG')
    def update_SAN_PHAM_IDS(self):
        if self.THONG_KE_THEO == 'MAT_HANG':
            self.SAN_PHAM_MANY_IDS =self.MAT_HANG_IDS_ID_MATHANG.ids
        elif self.THONG_KE_THEO == 'MAT_HANG_KHACH_HANG':
            self.SAN_PHAM_MANY_IDS =self.MAT_HANG_IDS_ID_MATHANG_KH.ids
        elif self.THONG_KE_THEO == 'MAT_HANG_NHAN_VIEN':
            self.SAN_PHAM_MANY_IDS =self.MAT_HANG_IDS_ID_MATHANG_NV.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH_VA_MAT_HANG':
            self.SAN_PHAM_MANY_IDS =self.MAT_HANG_IDS_ID_DVKD_MATHANG.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            self.SAN_PHAM_MANY_IDS =self.MAT_HANG_IDS_ID_DVKD.ids


    @api.onchange('NHOM_VTHH_ID')
    def update_NHOM_VTHH_ID(self):
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP

    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        if self.THONG_KE_THEO == 'MAT_HANG':
            self.MAT_HANG_IDS_ID_MATHANG = self.SAN_PHAM_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'MAT_HANG_KHACH_HANG':
            self.MAT_HANG_IDS_ID_MATHANG_KH = self.SAN_PHAM_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'MAT_HANG_NHAN_VIEN':
            self.MAT_HANG_IDS_ID_MATHANG_NV = self.SAN_PHAM_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH_VA_MAT_HANG':
            self.MAT_HANG_IDS_ID_DVKD_MATHANG = self.SAN_PHAM_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            self.MAT_HANG_IDS_ID_DVKD_MATHANG = self.SAN_PHAM_MANY_IDS.ids

    # ------------------------------ end Mặt hàng ---------------------------------------
    
    # ------------------------------Khách hàng ---------------------------------------

    @api.onchange('KHACH_HANG_IDS_ID_MATHANG_KH','KHACH_HANG_IDS_ID_KHACH_HANG','KHACH_HANG_IDS_ID_NV_KH','KHACH_HANG_IDS_ID_NV_KH_MH','CHON_KHACH_HANG_IDS')
    def update_KHACH_HANG_IDS(self):
        if self.THONG_KE_THEO == 'MAT_HANG_KHACH_HANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_ID_MATHANG_KH.ids
        elif self.THONG_KE_THEO == 'KHACH_HANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_ID_KHACH_HANG.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_ID_NV_KH.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_KHACH_HANG_MATHANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_ID_NV_KH_MH.ids
        elif self.THONG_KE_THEO == 'CHON_KHACH_HANG':
            self.KHACH_HANG_MANY_IDS =self.CHON_KHACH_HANG_IDS.ids


    @api.onchange('NHOM_KHACH_HANG_ID')
    def update_NHOM_KHACH_HANG_ID(self):
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KHACH_HANG_ID.MA_PHAN_CAP

    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        if self.THONG_KE_THEO == 'MAT_HANG_KHACH_HANG':
            self.KHACH_HANG_IDS_ID_MATHANG_KH = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'KHACH_HANG':
            self.KHACH_HANG_IDS_ID_KHACH_HANG = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.KHACH_HANG_IDS_ID_NV_KH = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_KHACH_HANG_MATHANG':
            self.KHACH_HANG_IDS_ID_NV_KH_MH = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'CHON_KHACH_HANG':
            self.CHON_KHACH_HANG_IDS = self.KHACH_HANG_MANY_IDS.ids

    # ------------------------------ end Khách hàng ---------------------------------------

    # ------------------------------Nhân viên ---------------------------------------

    @api.onchange('NHAN_VIEN_IDS_ID_MATHANG_NV','NHAN_VIEN_IDS_ID_NHANVIEN','NHAN_VIEN_IDS_ID_NV_KH','NHAN_VIEN_IDS_ID_NV_KH_MH')
    def update_NHAN_VIEN_IDS(self):
        if self.THONG_KE_THEO == 'MAT_HANG_NHAN_VIEN':
            self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS_ID_MATHANG_NV.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN':
            self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS_ID_NHANVIEN.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS_ID_NV_KH.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_KHACH_HANG_MATHANG':
            self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS_ID_NV_KH_MH.ids


    @api.onchange('DON_VI_ID')
    def update_DON_VI_ID(self):
        self.NHAN_VIEN_MANY_IDS = []

    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        if self.THONG_KE_THEO == 'MAT_HANG_NHAN_VIEN':
            self.NHAN_VIEN_IDS_ID_MATHANG_NV = self.NHAN_VIEN_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN':
            self.NHAN_VIEN_IDS_ID_NHANVIEN = self.NHAN_VIEN_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.NHAN_VIEN_IDS_ID_NV_KH = self.NHAN_VIEN_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_KHACH_HANG_MATHANG':
            self.NHAN_VIEN_IDS_ID_NV_KH_MH = self.NHAN_VIEN_MANY_IDS.ids


    # ------------------------------ end Nhân viên ---------------------------------------

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_TONG_HOP_BAN_HANG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI",limit=1)
        if chi_nhanh:
          result['CHI_NHANH_ID'] = chi_nhanh.id
        # Updated 2019-09-18 by anhtuan: Tạm thời bỏ qua trường hợp nhóm Khách hàng = <<Khác>>
        # Mặc dù câu SQL đã hỗ trọ TH này (id = -2)
        result['DON_VI_IDS_DVKD_MH'] = self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI").ids
        result['NHOM_KH_IDS'] = self.env['danh.muc.nhom.khach.hang.nha.cung.cap'].search([],order="MA").ids

        return result
    
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    # Todo: Cần check onchange theo THONG_KE_THEO và remove hàm default_get để tăng performance khi load form tham số
    # @api.onchange('field_name')
    # def _cap_nhat(self):
    #     for item in self:
    #         item.FIELDS_IDS = self.env['model_name'].search([])

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
        SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'
        CHON_TAT_CA_KHACH_HANG = params['CHON_TAT_CA_KHACH_HANG'] if 'CHON_TAT_CA_KHACH_HANG' in params.keys() else 'False'
        KHACH_HANG_MANY_IDS = params['KHACH_HANG_MANY_IDS'] if 'KHACH_HANG_MANY_IDS' in params.keys() else 'False'
        CHON_TAT_CA_NHAN_VIEN = params['CHON_TAT_CA_NHAN_VIEN'] if 'CHON_TAT_CA_NHAN_VIEN' in params.keys() else 'False'
        NHAN_VIEN_MANY_IDS = params['NHAN_VIEN_MANY_IDS'] if 'NHAN_VIEN_MANY_IDS' in params.keys() else 'False'

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO in ('MAT_HANG','MAT_HANG_KHACH_HANG','MAT_HANG_NHAN_VIEN','DON_VI_KINH_DOANH_VA_MAT_HANG','DON_VI_KINH_DOANH'):
            if CHON_TAT_CA_SAN_PHAM == 'False':
                if SAN_PHAM_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
        if THONG_KE_THEO in ('MAT_HANG_KHACH_HANG','KHACH_HANG','NHAN_VIEN_VA_KHACH_HANG','NHAN_VIEN_KHACH_HANG_MATHANG','CHON_KHACH_HANG'):
            if CHON_TAT_CA_KHACH_HANG == 'False':
                if KHACH_HANG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')
        if THONG_KE_THEO in ('MAT_HANG_NHAN_VIEN','NHAN_VIEN','NHAN_VIEN_VA_KHACH_HANG','NHAN_VIEN_KHACH_HANG_MATHANG'):
            if CHON_TAT_CA_NHAN_VIEN == 'False':
                if NHAN_VIEN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):


        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

      


        MAT_HANG_IDS_ID_MATHANG = [mh_mh['id'] for mh_mh in params['MAT_HANG_IDS_ID_MATHANG']]  if 'MAT_HANG_IDS_ID_MATHANG' in params.keys() and params['MAT_HANG_IDS_ID_MATHANG'] != 'False' else None

        MAT_HANG_IDS_ID_MATHANG_KH =[mh_mh_kh['id'] for mh_mh_kh in params['MAT_HANG_IDS_ID_MATHANG_KH']]  if 'MAT_HANG_IDS_ID_MATHANG_KH' in params.keys() and params['MAT_HANG_IDS_ID_MATHANG_KH'] != 'False' else None
        
        KHACH_HANG_IDS_ID_MATHANG_KH = [kh_mh_kh['id'] for kh_mh_kh in params['KHACH_HANG_IDS_ID_MATHANG_KH']]  if 'KHACH_HANG_IDS_ID_MATHANG_KH' in params.keys() and params['KHACH_HANG_IDS_ID_MATHANG_KH'] != 'False' else None
        
        KHACH_HANG_IDS_ID_KHACH_HANG = [kh_kh['id'] for kh_kh in params['KHACH_HANG_IDS_ID_KHACH_HANG']]  if 'KHACH_HANG_IDS_ID_KHACH_HANG' in params.keys() and params['KHACH_HANG_IDS_ID_KHACH_HANG'] != 'False' else None
        
        MAT_HANG_IDS_ID_MATHANG_NV = [mh_mh_nv['id'] for mh_mh_nv in params['MAT_HANG_IDS_ID_MATHANG_NV']]  if 'MAT_HANG_IDS_ID_MATHANG_NV' in params.keys() and params['MAT_HANG_IDS_ID_MATHANG_NV'] != 'False' else None
        
        NHAN_VIEN_IDS_ID_MATHANG_NV = [nv_mh_nv['id'] for nv_mh_nv in params['NHAN_VIEN_IDS_ID_MATHANG_NV']]  if 'NHAN_VIEN_IDS_ID_MATHANG_NV' in params.keys() and params['NHAN_VIEN_IDS_ID_MATHANG_NV'] != 'False' else None
        
        NHAN_VIEN_IDS_ID_NHANVIEN = [nv_nv['id'] for nv_nv in params['NHAN_VIEN_IDS_ID_NHANVIEN']]  if 'NHAN_VIEN_IDS_ID_NHANVIEN' in params.keys() and params['NHAN_VIEN_IDS_ID_NHANVIEN'] != 'False' else None
        
        NHAN_VIEN_IDS_ID_NV_KH = [nv_nv_kh['id'] for nv_nv_kh in params['NHAN_VIEN_IDS_ID_NV_KH']]  if 'NHAN_VIEN_IDS_ID_NV_KH' in params.keys() and params['NHAN_VIEN_IDS_ID_NV_KH'] != 'False' else None
        
        KHACH_HANG_IDS_ID_NV_KH = [kh_nv_kh['id'] for kh_nv_kh in params['KHACH_HANG_IDS_ID_NV_KH']]  if 'KHACH_HANG_IDS_ID_NV_KH' in params.keys() and params['KHACH_HANG_IDS_ID_NV_KH'] != 'False' else None
       
        NHAN_VIEN_IDS_ID_NV_KH_MH = [nv_nv_kh_mh['id'] for nv_nv_kh_mh in params['NHAN_VIEN_IDS_ID_NV_KH_MH']]  if 'NHAN_VIEN_IDS_ID_NV_KH_MH' in params.keys() and params['NHAN_VIEN_IDS_ID_NV_KH_MH'] != 'False' else None
        

        KHACH_HANG_IDS_ID_NV_KH_MH = [kh_nv_kh_mh['id'] for kh_nv_kh_mh in params['KHACH_HANG_IDS_ID_NV_KH_MH']]  if 'KHACH_HANG_IDS_ID_NV_KH_MH' in params.keys() and params['KHACH_HANG_IDS_ID_NV_KH_MH'] != 'False' else None
        
        MAT_HANG_IDS_ID_DVKD = [mh_dvkd['id'] for mh_dvkd in params['MAT_HANG_IDS_ID_DVKD']]  if 'MAT_HANG_IDS_ID_DVKD' in params.keys() and params['MAT_HANG_IDS_ID_DVKD'] != 'False' else None
        
        MAT_HANG_IDS_ID_DVKD_MATHANG = [mh_dvkd_mh['id'] for mh_dvkd_mh in params['MAT_HANG_IDS_ID_DVKD_MATHANG']]  if 'MAT_HANG_IDS_ID_DVKD_MATHANG' in params.keys() and params['MAT_HANG_IDS_ID_DVKD_MATHANG'] != 'False' else None
        
        DON_VI_IDS_DVKD_MH = [dv_dvkd_mh['id'] for dv_dvkd_mh in params['DON_VI_IDS_DVKD_MH']]  if 'DON_VI_IDS_DVKD_MH' in params.keys() and params['DON_VI_IDS_DVKD_MH'] != 'False' else None

        NHOM_KH_IDS = [nh_kh['id'] for nh_kh in params['NHOM_KH_IDS']]  if 'NHOM_KH_IDS' in params.keys() and params['NHOM_KH_IDS'] != 'False' else None

        NHAN_VIEN_ID = params['NHAN_VIEN_ID'] if 'NHAN_VIEN_ID' in params.keys() and params['NHAN_VIEN_ID'] != 'False' else None
        DON_VI_ID = params['DON_VI_ID'] if 'DON_VI_ID' in params.keys() and params['DON_VI_ID'] != 'False' else None
        MAT_HANG_ID = params['MAT_HANG_ID'] if 'MAT_HANG_ID' in params.keys() and params['MAT_HANG_ID'] != 'False' else None

        TINH_THANH_PHO_ID = params['TINH_THANH_PHO_ID'] if 'TINH_THANH_PHO_ID' in params.keys() and params['TINH_THANH_PHO_ID'] != 'False' else None
        QUAN_HUYEN_ID = params['QUAN_HUYEN_ID'] if 'QUAN_HUYEN_ID' in params.keys() and params['QUAN_HUYEN_ID'] != 'False' else None
        XA_PHUONG_ID = params['XA_PHUONG_ID'] if 'XA_PHUONG_ID' in params.keys() and params['XA_PHUONG_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CHI_LAY_KHACH_HANG_CO_PHAT_SINH = 1 if 'CHI_LAY_KHACH_HANG_CO_PHAT_SINH' in params.keys() and params['CHI_LAY_KHACH_HANG_CO_PHAT_SINH'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None

        CHON_KHACH_HANG_IDS = [chon_kh['id'] for chon_kh in params['CHON_KHACH_HANG_IDS']]  if 'CHON_KHACH_HANG_IDS' in params.keys() and params['CHON_KHACH_HANG_IDS'] != 'False' else None

        dv = 0
        nv = 0
        DON_VI = 0
        NHAN_VIEN = 0
        MAT_HANG = 0
        TINH_TP = 0
        QUAN_H = 0
        XA_P = 0
        MA_PC = '-1'
        if DON_VI_ID == 'False':
            dv = 1
            DON_VI = -1
        else:
            DON_VI = DON_VI_ID
            MA_PC = self.env['danh.muc.to.chuc'].search([('id', '=', DON_VI_ID)], limit=1).MA_PHAN_CAP

        if NHAN_VIEN_ID == 'False':
            nv = 1
        else:
            NHAN_VIEN = NHAN_VIEN_ID

        if MAT_HANG_ID == 'False':
            MAT_HANG = -1
        else:
            MAT_HANG = MAT_HANG_ID

        if TINH_THANH_PHO_ID == 'False':
            TINH_TP = -1
        else:
            TINH_TP = TINH_THANH_PHO_ID

        if QUAN_HUYEN_ID == 'False':
            QUAN_H = -1
        else:
            QUAN_H = QUAN_HUYEN_ID

        if XA_PHUONG_ID == 'False':
            XA_P = -1
        else:
            XA_P = XA_PHUONG_ID


        DON_VI_TINH_PARAM = params.get('DON_VI_TINH')
        if DON_VI_TINH_PARAM == 'DON_VI_CHUYEN_DOI_1':
            DON_VI_TINH = 1
        elif DON_VI_TINH_PARAM == 'DON_VI_CHUYEN_DOI_2':
            DON_VI_TINH = 2
        else:
            DON_VI_TINH = 0

        # DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() else 'False'
        # Execute SQL query here
        # Thống kê theo Mặt hàng  
        if self.get_context('MAT_HANG_IDS_ID_MATHANG'):
            SAN_PHAMIDS = [mh_mh['id'] for mh_mh in params['MAT_HANG_IDS_ID_MATHANG']]  if 'MAT_HANG_IDS_ID_MATHANG' in params.keys() and params['MAT_HANG_IDS_ID_MATHANG'] != 'False' else None
        elif self.get_context('MAT_HANG_IDS_ID_MATHANG_KH'):
            SAN_PHAMIDS = [mh_mh_kh['id'] for mh_mh_kh in params['MAT_HANG_IDS_ID_MATHANG_KH']]  if 'MAT_HANG_IDS_ID_MATHANG_KH' in params.keys() and params['MAT_HANG_IDS_ID_MATHANG_KH'] != 'False' else None
        elif self.get_context('MAT_HANG_IDS_ID_MATHANG_NV'):
            SAN_PHAMIDS = [mh_mh_nv['id'] for mh_mh_nv in params['MAT_HANG_IDS_ID_MATHANG_NV']]  if 'MAT_HANG_IDS_ID_MATHANG_NV' in params.keys() and params['MAT_HANG_IDS_ID_MATHANG_NV'] != 'False' else None
        elif self.get_context('MAT_HANG_IDS_ID_DVKD'):
            SAN_PHAMIDS = [mh_dvkd['id'] for mh_dvkd in params['MAT_HANG_IDS_ID_DVKD']]  if 'MAT_HANG_IDS_ID_DVKD' in params.keys() and params['MAT_HANG_IDS_ID_DVKD'] != 'False' else None
        elif self.get_context('MAT_HANG_IDS_ID_DVKD_MATHANG'):
            SAN_PHAMIDS = [mh_dvkd_mh['id'] for mh_dvkd_mh in params['MAT_HANG_IDS_ID_DVKD_MATHANG']]  if 'MAT_HANG_IDS_ID_DVKD_MATHANG' in params.keys() and params['MAT_HANG_IDS_ID_DVKD_MATHANG'] != 'False' else None
        else:
            SAN_PHAMIDS = ()
        
        if self.get_context('KHACH_HANG_IDS_ID_KHACH_HANG'):
            KHACH_HANG_IDS = [kh_kh['id'] for kh_kh in params['KHACH_HANG_IDS_ID_KHACH_HANG']]  if 'KHACH_HANG_IDS_ID_KHACH_HANG' in params.keys() and params['KHACH_HANG_IDS_ID_KHACH_HANG'] != 'False' else None
        elif self.get_context('KHACH_HANG_IDS_ID_NV_KH'):
            KHACH_HANG_IDS = [kh_nv_kh['id'] for kh_nv_kh in params['KHACH_HANG_IDS_ID_NV_KH']]  if 'KHACH_HANG_IDS_ID_NV_KH' in params.keys() and params['KHACH_HANG_IDS_ID_NV_KH'] != 'False' else None
        elif self.get_context('KHACH_HANG_IDS_ID_NV_KH_MH'):
            KHACH_HANG_IDS = [kh_nv_kh_mh['id'] for kh_nv_kh_mh in params['KHACH_HANG_IDS_ID_NV_KH_MH']]  if 'KHACH_HANG_IDS_ID_NV_KH_MH' in params.keys() and params['KHACH_HANG_IDS_ID_NV_KH_MH'] != 'False' else None
        elif self.get_context('KHACH_HANG_IDS_ID_MATHANG_KH'):
            KHACH_HANG_IDS =  [kh_mh_kh['id'] for kh_mh_kh in params['KHACH_HANG_IDS_ID_MATHANG_KH']]  if 'KHACH_HANG_IDS_ID_MATHANG_KH' in params.keys() and params['KHACH_HANG_IDS_ID_MATHANG_KH'] != 'False' else None
        else:
            KHACH_HANG_IDS = ()
        
        if self.get_context('NHAN_VIEN_IDS_ID_NHANVIEN'):
            NHAN_VIEN_IDS = [nv_nv['id'] for nv_nv in params['NHAN_VIEN_IDS_ID_NHANVIEN']]  if 'NHAN_VIEN_IDS_ID_NHANVIEN' in params.keys() and params['NHAN_VIEN_IDS_ID_NHANVIEN'] != 'False' else None
        elif self.get_context('NHAN_VIEN_IDS_ID_NV_KH'):
            NHAN_VIEN_IDS =  [nv_nv_kh['id'] for nv_nv_kh in params['NHAN_VIEN_IDS_ID_NV_KH']]  if 'NHAN_VIEN_IDS_ID_NV_KH' in params.keys() and params['NHAN_VIEN_IDS_ID_NV_KH'] != 'False' else None
        elif self.get_context('NHAN_VIEN_IDS_ID_NV_KH_MH'):
            NHAN_VIEN_IDS =  [nv_nv_kh_mh['id'] for nv_nv_kh_mh in params['NHAN_VIEN_IDS_ID_NV_KH_MH']]  if 'NHAN_VIEN_IDS_ID_NV_KH_MH' in params.keys() and params['NHAN_VIEN_IDS_ID_NV_KH_MH'] != 'False' else None
        elif self.get_context('NHAN_VIEN_IDS_ID_MATHANG_NV'):
            NHAN_VIEN_IDS =  [nv_mh_nv['id'] for nv_mh_nv in params['NHAN_VIEN_IDS_ID_MATHANG_NV']]  if 'NHAN_VIEN_IDS_ID_MATHANG_NV' in params.keys() and params['NHAN_VIEN_IDS_ID_MATHANG_NV'] != 'False' else None
        else:
            NHAN_VIEN_IDS = ()

        if self.get_context('DON_VI_IDS_DVKD_MH'):
            DON_VI_IDS = [dv_dvkd_mh['id'] for dv_dvkd_mh in params['DON_VI_IDS_DVKD_MH']]  if 'DON_VI_IDS_DVKD_MH' in params.keys() and params['DON_VI_IDS_DVKD_MH'] != 'False' else None
        else:
            DON_VI_IDS = ()


        if self.get_context('NHOM_KH_IDS'):
            NHOM_KHIDS = [nh_kh['id'] for nh_kh in params['NHOM_KH_IDS']]  if 'NHOM_KH_IDS' in params.keys() and params['NHOM_KH_IDS'] != 'False' else None
        else:
            NHOM_KHIDS = ()

        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
        MA_PC_NHOM_KH = params.get('MA_PC_NHOM_KH')
        MA_PC_NHOM_NV = params.get('MA_PC_NHOM_NV')

        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')

        if params.get('CHON_TAT_CA_KHACH_HANG'):
            domain = [('LA_KHACH_HANG','=', True)]
            if MA_PC_NHOM_KH:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
            KHACH_HANG_IDS =  self.env['res.partner'].search(domain).ids
        else:
            KHACH_HANG_IDS = params.get('KHACH_HANG_MANY_IDS')

        if params.get('CHON_TAT_CA_NHAN_VIEN'):
            domain = [('LA_NHAN_VIEN','=', True)]
            if DON_VI_ID:
                domain += [('DON_VI_ID','=', DON_VI_ID)]
            NHAN_VIEN_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHAN_VIEN_IDS =  params.get('NHAN_VIEN_MANY_IDS')

        check_kh = ''
        if self.get_context('KHACH_HANG_IDS_ID_MATHANG_KH'):
            check_kh = 'True'
        else:
            check_kh = 'False'

        # query_mat_hang = """INNER JOIN (SELECT * FROM danh_muc_vat_tu_hang_hoa WHERE id in (459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498)) AS LII ON SL."MA_HANG_ID" = LII.id"""

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            # 'TU_NGAY':'2018-01-01', 
            # 'DEN_NGAY':'2020-01-05', 
            'DON_VI_TINH':DON_VI_TINH,
            'CHECK_KH' : check_kh,
            'SAN_PHAMIDS' : SAN_PHAM_IDS or None,
            'NHAN_VIEN_ID' : NHAN_VIEN_ID,
            'MAT_HANG_ID' : MAT_HANG_ID,
            'dv_id' : dv,
            'DON_VI' : DON_VI,
            'nv_id' : nv,
            'MAT_HANG' : MAT_HANG,
            'NHAN_VIEN' : NHAN_VIEN,
            'TINH_TP' : TINH_TP,
            'QUAN_H' : QUAN_H,
            'XA_P' : XA_P,
            'MA_PC' : MA_PC,
            'DON_VI_ID':DON_VI_ID,
            'DON_VI_IDS' : DON_VI_IDS_DVKD_MH,
            'NHAN_VIEN_IDS' : NHAN_VIEN_IDS or None,
            'KHACH_HANG_IDS' : KHACH_HANG_IDS or None,
            'NHOM_KHIDS' : NHOM_KHIDS,
            'CHI_NHANH_ID':CHI_NHANH_ID, 
            'TINH_THANH_PHO_ID':TINH_THANH_PHO_ID, 
            'QUAN_HUYEN_ID':QUAN_HUYEN_ID, 
            'XA_PHUONG_ID':XA_PHUONG_ID, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_LAY_KHACH_HANG_CO_PHAT_SINH':CHI_LAY_KHACH_HANG_CO_PHAT_SINH,
            'CHON_KHACH_HANG_IDS':CHON_KHACH_HANG_IDS,
            'limit': limit,
            'offset': offset, 
            }      

        if THONG_KE_THEO=='MAT_HANG' :
            return self._lay_bao_cao_mat_hang(params_sql)
           
        # Thống kê theo Mặt hàng và khách hàng
        elif THONG_KE_THEO=='MAT_HANG_KHACH_HANG' :
            return self._lay_bao_cao_mat_hang_va_khach_hang(params_sql)
            
        # Thống kê theo Mặt hàng và nhân viên
        elif THONG_KE_THEO=='MAT_HANG_NHAN_VIEN' :
            return self._lay_bao_cao_mat_hang_va_nhan_vien(params_sql)
        # Thống kê theo Khách hàng
        elif THONG_KE_THEO=='KHACH_HANG' :
            return self._lay_bao_cao_khach_hang(params_sql)
        # Thống kê theo nhân viên
        elif THONG_KE_THEO=='NHAN_VIEN' :
            return self._lay_bao_cao_nhan_vien(params_sql)
        # Thống kê theo nhân viên và khách hàng
        elif THONG_KE_THEO=='NHAN_VIEN_VA_KHACH_HANG' :
            return self._lay_bao_cao_nhan_vien_va_khach_hang(params_sql)
        # Thống kê theo nhân viên, khách hàng và mặt hàng
        elif THONG_KE_THEO=='NHAN_VIEN_KHACH_HANG_MATHANG' :
            return self._lay_bao_cao_nhan_vien_khach_hang_va_mat_hang(params_sql)
                      
        # Thống kê theo địa phương
        elif THONG_KE_THEO=='DIA_PHUONG' :
            return self._lay_bao_cao_theo_dia_phuong(params_sql)
            
            
        # Thống kê theo đơn vị kinh doanh
        elif THONG_KE_THEO=='DON_VI_KINH_DOANH' :
            return self._lay_bao_cao_theo_don_vi_kinh_doanh(params_sql)
        # Thống kê theo đơn vị kinh doanh và mặt hàng
        elif THONG_KE_THEO=='DON_VI_KINH_DOANH_VA_MAT_HANG' :
            return self._lay_bao_cao_theo_don_vi_kinh_doanh_va_mat_hang(params_sql)
         # Thống kê theo Nhóm khách hàng
        elif THONG_KE_THEO=='NHOM_KHACH_HANG' :
            return self._lay_bao_cao_theo_nhom_khach_hang(params_sql)
            
            



    def _lay_bao_cao_mat_hang(self, params_sql):      
        record = []
        query = """
            
            DO LANGUAGE plpgsql $$
            DECLARE
            tu_ngay                             DATE := %(TU_NGAY)s;
        
            den_ngay                            DATE := %(DEN_NGAY)s;
        
            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
        
           
        
            don_vi_tinh                        INTEGER := %(DON_VI_TINH)s;
        
            chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;
        
           
        
        
            rec                                 RECORD;
            PHAN_THAP_PHAN_DON_GIA               INT;
        
        
        
          
        
        
        BEGIN

            SELECT value
            INTO PHAN_THAP_PHAN_DON_GIA
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
            FETCH FIRST 1 ROW ONLY
            ;
        
            DROP TABLE IF EXISTS TMP_LIST_BRAND
            ;
        
            CREATE TEMP TABLE TMP_LIST_BRAND
                AS
                    SELECT *
                    FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
            ;
        
        
            DROP TABLE IF EXISTS DS_HANG_HOA
            ;
        
            CREATE TEMP TABLE DS_HANG_HOA
                AS
                    SELECT  II.id ,
                                II."TEN" ,
        
                                II."NGUON_GOC" ,
        
                                II."TINH_CHAT" ,
                                II."DVT_CHINH_ID"
                        FROM    danh_muc_vat_tu_hang_hoa II
                        WHERE (id = any( %(SAN_PHAMIDS)s))
            ;

             DROP TABLE IF EXISTS DS_KHACH_HANG
            ;

            CREATE TEMP TABLE DS_KHACH_HANG
                AS
                    SELECT
                        AO.id ,
                        AO."LA_KHACH_HANG"
                        FROM    res_partner AO
                        WHERE (AO."LA_KHACH_HANG" ='1' AND
                               (id =any( %(CHON_KHACH_HANG_IDS)s) OR id IS NULL
                                 ) )
                ;

        
        
        
        
        
        
            DROP TABLE IF EXISTS TMP_DON_VI_CHUYEN_DOI
            ;
        
            CREATE TEMP TABLE TMP_DON_VI_CHUYEN_DOI
                AS
                    SELECT
                        IIUC."VAT_TU_HANG_HOA_ID"
                        , "DVT_ID"
                        , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                        THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                           WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                               THEN 1
                           ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                           END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                    FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                    WHERE IIUC."STT" = don_vi_tinh
            ;
        
            DROP TABLE IF EXISTS TMP_KET_QUA
            ;
        
            CREATE TEMP TABLE TMP_KET_QUA
                AS
                    SELECT
                        T."MA_HANG_ID"
                        , T."MA_HANG"
                        , -- Mã hàng
                        T."TEN"
                        , -- Tên hàng
                        T."DON_VI_TINH_CHINH"
                        , T."DON_VI_TINH"
                        , SUM(T."SO_LUONG_BAN")                           AS "SO_LUONG_BAN"
                        , SUM(T."SO_LUONG_THEO_DVT_CHINH")            AS "SO_LUONG_THEO_DVT_CHINH"
                        , SUM(T."SO_LUONG_KHUYEN_MAI")                AS "SO_LUONG_KHUYEN_MAI"
                        , SUM(T."SO_LUONG_KHUYEN_MAI_THEO_DVT_CHINH") AS "SO_LUONG_KHUYEN_MAI_THEO_DVT_CHINH"
                        , SUM(T."SO_LUONG_TRA_LAI")                   AS "SO_LUONG_TRA_LAI"
                        , SUM(T."SO_LUONG_TRA_LAI_THEO_DVT_CHINH")    AS "SO_LUONG_TRA_LAI_THEO_DVT_CHINH"
                        , SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI")        AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                        , --                 SUM(T.MainReturnPromotionQuantity) AS MainReturnPromotionQuantity ,
                          SUM(T."DOANH_SO_BAN")                            AS "DOANH_SO_BAN"
                        ,
                          SUM(T."DOANH_SO_BAN" - T."SO_TIEN_NHAP_KHAU")    AS SaleAmountNotExportTax
                        , -- Doanh thu chưa bao gồm thuế xuất khẩu = Doanh số - Thuế xuất khẩu
                          SUM(T."SO_TIEN_NHAP_KHAU")                  AS "SO_TIEN_NHAP_KHAU"
                        , -- Thuế xuất khẩu
                          SUM(T."SO_TIEN_CHIET_KHAU")                 AS "SO_TIEN_CHIET_KHAU"
                        , SUM(T."GIA_TRI_TRA_LAI")                    AS "GIA_TRI_TRA_LAI"
                        , SUM(COALESCE(T."GIA_TRI_GIAM_GIA", 0))      AS "GIA_TRI_GIAM_GIA"
                        , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - "GIA_TRI_TRA_LAI" -
                              "GIA_TRI_GIAM_GIA" )     AS "DOANH_THU_THUAN"

                        , CASE WHEN SUM(T."SO_LUONG_BAN" + T."SO_LUONG_KHUYEN_MAI"
                              - T."SO_LUONG_TRA_LAI" - T."SO_LUONG_KHUYEN_MAI_TRA_LAI") <> 0
                         THEN ROUND(CAST(SUM(T."TIEN_VON") / SUM(T."SO_LUONG_BAN"
                                                        + T."SO_LUONG_KHUYEN_MAI"
                                                        - T."SO_LUONG_TRA_LAI"
                                                        - T."SO_LUONG_KHUYEN_MAI_TRA_LAI")AS NUMERIC),
                                PHAN_THAP_PHAN_DON_GIA)
                         ELSE 0
                        END AS "DON_GIA_VON"
                        , SUM(T."TIEN_VON") AS "TIEN_VON"
                        ,CASE WHEN SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                              - T."GIA_TRI_GIAM_GIA") > 0
                          AND SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU"
                                  - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA"
                                  - T."TIEN_VON") > 0
                          OR SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU"
                                 - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA") < 0
                          AND SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU"
                                  - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA"
                                  - T."TIEN_VON") < 0
                     THEN SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                              - T."GIA_TRI_GIAM_GIA" - T."TIEN_VON") * 100
                          / SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU"
                                - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA")
                     ELSE 0
                        END AS "TY_LE_LAI_GOP"
                        , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" --SO_TIEN -SO_TIEN_CHIET_KHAU -SO_TIEN_TRA_LAI -SO_TIEN_GIAM_TRU -GIA_VON
                        - T."GIA_TRI_GIAM_GIA" - T."TIEN_VON") AS "LAI_GOP"

                        
        
        
                    FROM (
                             SELECT
                                 SL."MA_HANG_ID"
                                 , SL."MA_HANG"
                                 , -- Mã hàng
                                 LII."TEN"
                                 , -- Tên hàng
                                 UI."DON_VI_TINH" AS "DON_VI_TINH_CHINH"
        
                                 ,CASE WHEN LII."DVT_CHINH_ID" IS NULL THEN ''
                                         ELSE U."DON_VI_TINH"
                                    END AS "DON_VI_TINH"
                                 , SUM(CASE SL."LA_HANG_KHUYEN_MAI"
                                       WHEN FALSE
                                           THEN SL."SO_LUONG_THEO_DVT_CHINH"
                                       ELSE 0
                                       END)                     AS "SO_LUONG_THEO_DVT_CHINH"
                                 , -- Số lượng bán theo ĐVC
                                   SUM(CASE SL."LA_HANG_KHUYEN_MAI"
                                       WHEN TRUE
                                           THEN SL."SO_LUONG_THEO_DVT_CHINH"
                                       ELSE 0
                                       END)                     AS "SO_LUONG_KHUYEN_MAI_THEO_DVT_CHINH"
                                 , -- Số lượng KM
                                   SUM(CASE SL."LA_HANG_KHUYEN_MAI"
                                       WHEN FALSE
                                           THEN SL."SL_TRA_LAI_THEO_DVT_CHINH"
                                       ELSE 0
                                       END)                     AS "SO_LUONG_TRA_LAI_THEO_DVT_CHINH"
                                 , -- Số lượng trả lại theo ĐVT chính
                                   SUM(CASE SL."LA_HANG_KHUYEN_MAI"
                                       WHEN TRUE
                                           THEN SL."SL_TRA_LAI_THEO_DVT_CHINH"
                                       ELSE 0
                                       END)                     AS "SO_LUONG_KHUYEN_MAI_TRA_LAI_DVT_CHINH"
                                 , -- Số lượng trả lại theo ĐVT chính
                                   SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                                 , -- Doanh số bán
                                   SUM(SL."SO_TIEN_NHAP_KHAU")  AS "SO_TIEN_NHAP_KHAU"
                                 , -- Thuế xuất khẩu
                                   SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                 , -- Tiền chiết khấu
                                   SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                 , -- Giá trị trả lại
                                   SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                                 , -- Giá trị giảm giá
                                   SUM(CASE WHEN U."id" <> -1
                                         AND SL."DVT_ID" = U.id
                                       THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN 0
                                            ELSE SL."SO_LUONG"
                                            END
                                       ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN 0
                                            ELSE SL."SO_LUONG_THEO_DVT_CHINH"  * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                            END
                                       END)                     AS "SO_LUONG_BAN"
                                 ,SUM(CASE WHEN U."id" <> -1
                                         AND SL."DVT_ID" = U.id
                                       THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN SL."SO_LUONG"
                                                ELSE 0
                                            END
                                       ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN SL."SO_LUONG_THEO_DVT_CHINH"  * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                            ELSE  0
                                            END
                                       END)                     AS "SO_LUONG_KHUYEN_MAI"
        
                                 ,  SUM(CASE WHEN U."id" <> -1
                                         AND SL."DVT_ID" = U.id
                                       THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN 0
                                            ELSE SL."SO_LUONG_TRA_LAI"
                                            END
                                       ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN 0
                                            ELSE SL."SL_TRA_LAI_THEO_DVT_CHINH"  * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                            END
                                       END)                     AS "SO_LUONG_TRA_LAI"
                                 ,SUM(CASE WHEN U."id" <> -1
                                         AND SL."DVT_ID" = U.id
                                       THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN SL."SO_LUONG_TRA_LAI"
                                                ELSE 0
                                            END
                                       ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN SL."SL_TRA_LAI_THEO_DVT_CHINH"  * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                            ELSE  0
                                            END
                                       END)                     AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                                        , 0 AS "TIEN_VON"
                             FROM so_ban_hang_chi_tiet AS SL
                                INNER JOIN TMP_LIST_BRAND AS BR ON SL."CHI_NHANH_ID" = BR."CHI_NHANH_ID"
                                INNER JOIN DS_HANG_HOA AS LII ON SL."MA_HANG_ID" = LII.id
                                LEFT JOIN DS_KHACH_HANG AO ON SL."DOI_TUONG_ID" = AO.id
                                LEFT JOIN danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI.id
                                LEFT JOIN TMP_DON_VI_CHUYEN_DOI AS UC ON LII.id = UC."VAT_TU_HANG_HOA_ID"
                                LEFT JOIN danh_muc_don_vi_tinh U ON ( UC."VAT_TU_HANG_HOA_ID" IS NULL
                                                              AND U.id = LII."DVT_CHINH_ID"
                                                            )
                                                            OR ( UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                                                 AND UC."DVT_ID" = U.id
                                                            )
        
                             WHERE
                                 (
                                    don_vi_tinh  IS NULL
                                        OR don_vi_tinh =0
                                     OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                 )
                                 AND SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    AND ( ( %(CHON_KHACH_HANG_IDS)s) IS NULL
                                  OR AO.id IS NOT NULL
                                     )
        
                             GROUP BY
                                 SL."MA_HANG_ID",
                                 SL."MA_HANG", -- Mã hàng
                                 LII."TEN", -- Tên hàng
                                 UI."DON_VI_TINH",
                                 CASE WHEN LII."DVT_CHINH_ID" IS NULL THEN ''
                                         ELSE U."DON_VI_TINH"
                                    END
                             UNION ALL
        
                             SELECT
                                 IL."MA_HANG_ID"
                                 , IL."MA_HANG"
                                 , -- Mã hàng
                                 LII."TEN"
                                 , -- Tên hàng
                                 UI."DON_VI_TINH" AS "DON_VI_TINH"
                                 ,CASE WHEN LII."DVT_CHINH_ID"  IS NULL THEN ''
                                         ELSE U."DON_VI_TINH"
                                    END AS "DON_VI_TINH"
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                ,  SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "TIEN_VON"
                             FROM so_kho_chi_tiet IL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN DS_HANG_HOA AS LII ON IL."MA_HANG_ID" = LII.id
                                LEFT JOIN DS_KHACH_HANG AO ON IL."DOI_TUONG_ID" = AO.id
                                LEFT JOIN danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI.id
                                LEFT JOIN TMP_DON_VI_CHUYEN_DOI AS UC ON LII.id = UC."VAT_TU_HANG_HOA_ID"
                                LEFT JOIN danh_muc_don_vi_tinh U ON ( UC."VAT_TU_HANG_HOA_ID" IS NULL
                                                              AND U.id = LII."DVT_CHINH_ID"
                                                            )
                                                            OR ( UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                                                 AND UC."DVT_ID" = U.id
                                                            )
                             WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                   --           AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                   AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                   AND (IL."LOAI_CHUNG_TU" = '2020'
                                        OR IL."LOAI_CHUNG_TU" = '2013'
                                   )
        
                                   AND (
        
                                        don_vi_tinh   IS NULL
                                        OR don_vi_tinh =0
                                        OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
        
                                   )
                                       AND ( ( %(CHON_KHACH_HANG_IDS)s) IS NULL
                                             OR AO."id" IS NOT NULL
                                           )
                             GROUP BY
                                IL."MA_HANG_ID",
                                 IL."MA_HANG", -- Mã hàng
                                 LII."TEN", -- Tên hàng
                                 UI."DON_VI_TINH",
                                 CASE WHEN LII."DVT_CHINH_ID" IS NULL THEN ''
                                         ELSE U."DON_VI_TINH"
                                END
        
        
                         ) T
                    GROUP BY
                        T."MA_HANG_ID",
                        T."MA_HANG", -- Mã hàng
                        T."TEN", -- Tên hàng
                        T."DON_VI_TINH_CHINH",
                        T."DON_VI_TINH"
        
        
                    HAVING SUM(T."SO_LUONG_BAN"
                           ) <> 0
                           OR SUM(T."SO_LUONG_KHUYEN_MAI"
                              ) <> 0
                           OR SUM(T."SO_LUONG_TRA_LAI"
                              ) <> 0
                           OR SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI"
                              ) <> 0
                           OR SUM(T."DOANH_SO_BAN"
                              ) <> 0
                           OR SUM(T."SO_TIEN_CHIET_KHAU"
                              ) <> 0
                           OR SUM(T."GIA_TRI_TRA_LAI"
                              ) <> 0
                           OR SUM(T."GIA_TRI_GIAM_GIA"
                              ) <> 0
        
        
            ;
        
        END $$
        ;
        
        SELECT 
                "MA_HANG" AS"MA_HANG",
                "TEN" AS "TEN_HANG",
                "DON_VI_TINH_CHINH" AS "DVT",
                "SO_LUONG_BAN" AS "SO_LUONG_BAN",
                "DOANH_SO_BAN" AS"DOANH_SO_BAN",
                "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU",
                "SO_LUONG_TRA_LAI" AS"SO_LUONG_TRA_LAI",
                "GIA_TRI_TRA_LAI" AS "GIA_TRI_TRA_LAI",
                "GIA_TRI_GIAM_GIA" AS"GIA_TRI_GIAM_GIA",
                 "DOANH_THU_THUAN" AS "DOANH_THU_THUAN",
                 "DON_GIA_VON" AS "DON_GIA_VON",
                "TIEN_VON" AS"TIEN_VON",
                "LAI_GOP" AS "LAI_GOP",
                 "TY_LE_LAI_GOP" AS "TY_LE_LAI_GOP"


        FROM TMP_KET_QUA

        OFFSET %(offset)s
        LIMIT %(limit)s;

    
            
            """
        return self.execute(query,params_sql)

    def _lay_bao_cao_mat_hang_va_khach_hang(self, params_sql):      
        record = []
        query = """
            
                     DO LANGUAGE plpgsql $$
    DECLARE
    tu_ngay                             DATE :=%(TU_NGAY)s;

    den_ngay                            DATE := %(DEN_NGAY)s;

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --chon_khach_hang                     VARCHAR(255) := 'True';

    loai_don_vi_tinh                    INTEGER := %(DON_VI_TINH)s;

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    --SAN_PHAMIDS                         INTEGER := -1;
    --KHACH_HANG_IDS                         INTEGER := -1;


    rec                                 RECORD;

BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;



    IF ( %(SAN_PHAMIDS)s) IS NOT NULL
    THEN
         DROP TABLE IF EXISTS DS_HANG_HOA;

        CREATE TEMP TABLE DS_HANG_HOA
            AS
                SELECT
                      II."id"                        AS "MA_HANG_ID"
                    , II."TEN"
                    , COALESCE(UI."DON_VI_TINH", '') AS "DON_VI_TINH_CHINH"
                    , CASE WHEN II."DVT_CHINH_ID" IS NULL
                    THEN ''
                      ELSE U."DON_VI_TINH"
                      END                            AS "DON_VI_TINH"
                    , "NGUON_GOC"
                    , II."TINH_CHAT"
                    , II."DVT_CHINH_ID"
                    , U."id"                         AS "DON_VI_CHUYEN_DOI"
                    , (CASE WHEN IIUC."VAT_TU_HANG_HOA_ID" IS NULL
                    THEN 1
                       WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
                           THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                       WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                           THEN 1
                       ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                       END)                          AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM
                    danh_muc_vat_tu_hang_hoa AS II
                    LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC ON IIUC."STT" = loai_don_vi_tinh
                    LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_CHINH_ID" = UI."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON (IIUC."VAT_TU_HANG_HOA_ID" IS NULL AND U."id" = II."DVT_CHINH_ID")
                                                        OR (IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL AND IIUC."DVT_ID" = U."id")
                WHERE
                    (II.id = any( %(SAN_PHAMIDS)s))
                      AND
                      (loai_don_vi_tinh IS NULL OR loai_don_vi_tinh = 0 OR IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL)
        ;

    ELSE
        CREATE TEMP TABLE DS_HANG_HOA
            AS
                SELECT
                      II."id"                        AS "MA_HANG_ID"
                    , II."TEN"
                    , COALESCE(UI."DON_VI_TINH", '') AS "DON_VI_TINH_CHINH"
                    , CASE WHEN II."DVT_CHINH_ID" IS NULL
                    THEN ''
                      ELSE U."DON_VI_TINH"
                      END                            AS "DON_VI_TINH"
                    , "NGUON_GOC"
                    , II."TINH_CHAT"
                    , II."DVT_CHINH_ID"
                    , U."id"                         AS "DON_VI_CHUYEN_DOI"
                    , (CASE WHEN IIUC."VAT_TU_HANG_HOA_ID" IS NULL
                    THEN 1
                       WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
                           THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                       WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                           THEN 1
                       ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                       END)                          AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM
                    danh_muc_vat_tu_hang_hoa AS II
                    LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                        ON IIUC."VAT_TU_HANG_HOA_ID" = II."id" AND IIUC."STT" = loai_don_vi_tinh
                    LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_CHINH_ID" = UI."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON (IIUC."VAT_TU_HANG_HOA_ID" IS NULL AND U."id" = II."DVT_CHINH_ID")
                                                        OR (IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL AND IIUC."DVT_ID" = U."id")
                WHERE

                    (loai_don_vi_tinh IS NULL OR loai_don_vi_tinh = 0 OR IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL)
        ;

    END IF
    ;

    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;

    CREATE TEMP TABLE DS_KHACH_HANG
        AS
            SELECT
                AO.id
                , AO."MA_KHACH_HANG"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI"
                , CASE WHEN AO."LOAI_KHACH_HANG" = '0'
                THEN AO."DIEN_THOAI"
                  ELSE AO."DT_DI_DONG"
                  END
                , AO."TINH_TP_ID"
                , AO."QUAN_HUYEN_ID"
                , AO."XA_PHUONG_ID"
                , AO."LIST_TEN_NHOM_KH_NCC"
                , AO."LIST_MA_NHOM_KH_NCC"
            FROM res_partner AS AO
            WHERE (id = any( %(KHACH_HANG_IDS)s))
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS
            SELECT
                T."MA_HANG_ID"
                , T."MA_HANG"

                , LII."TEN"

                , T."DON_VI_TINH_CHINH"
                , T."DON_VI_TINH"
                , T."DOI_TUONG_ID"
                , LAO."MA_KHACH_HANG"
                ,LAO."LIST_TEN_NHOM_KH_NCC"
                ,LAO."LIST_MA_NHOM_KH_NCC"
                , LAO."HO_VA_TEN"

                , SUM(T."SO_LUONG_BAN")                      AS "SO_LUONG_BAN"
                , SUM(T."SO_LUONG_KHUYEN_MAI")              AS "SO_LUONG_KHUYEN_MAI"
                , SUM(T."SO_LUONG_TRA_LAI")              AS "SO_LUONG_TRA_LAI"
                 , SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI")        AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                , SUM(T."DOANH_SO_BAN")                       AS "DOANH_SO_BAN"
                , SUM(T."SO_TIEN_CHIET_KHAU")            AS "SO_TIEN_CHIET_KHAU"
                , SUM(T."GIA_TRI_TRA_LAI")               AS "GIA_TRI_TRA_LAI"
                , SUM(COALESCE(T."GIA_TRI_GIAM_GIA", 0)) AS "GIA_TRI_GIAM_GIA"
                , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - "GIA_TRI_TRA_LAI" -
                      "GIA_TRI_GIAM_GIA")                AS "DOANH_THU_THUAN"
                 , SUM(T."SO_TIEN_CHI_PHI")                       AS "SO_TIEN_CHI_PHI"


            FROM (
                     SELECT
                         SL."MA_HANG_ID"
                         , SL."MA_HANG"
                         , -- Mã hàng
                         LII."DON_VI_TINH_CHINH"
                         , LII."DON_VI_TINH"
                         , SL."DOI_TUONG_ID"


                         , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"

                         , SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                         , -- Tiền chiết khấu
                           SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                         , -- Giá trị trả lại
                           SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                         , -- Giá trị giảm giá
                           SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                         AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                               THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                   THEN 0
                                    ELSE SL."SO_LUONG"
                                    END
                               ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                   THEN 0
                                    ELSE SL."SO_LUONG_THEO_DVT_CHINH" *
                                         COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                    END
                               END)                     AS "SO_LUONG_BAN"
                          ,SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                       AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                       THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN SL."SO_LUONG"
                                                ELSE 0
                                            END
                                       ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN SL."SO_LUONG_THEO_DVT_CHINH"  * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                            ELSE  0
                                            END
                                       END)                     AS "SO_LUONG_KHUYEN_MAI"


                         , SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                         AND SL."DVT_ID" =LII."DON_VI_CHUYEN_DOI"
                         THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                             THEN 0
                              ELSE SL."SO_LUONG_TRA_LAI"
                              END
                               ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                   THEN 0
                                    ELSE SL."SL_TRA_LAI_THEO_DVT_CHINH" *
                                         COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                    END
                               END)                     AS "SO_LUONG_TRA_LAI"
                         ,SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                         AND SL."DVT_ID" =LII."DON_VI_CHUYEN_DOI"
                                       THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN SL."SO_LUONG_TRA_LAI"
                                                ELSE 0
                                            END
                                       ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                           THEN SL."SL_TRA_LAI_THEO_DVT_CHINH"  * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                            ELSE  0
                                            END
                                       END)                     AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                        , 0 AS "SO_TIEN_CHI_PHI"

                     FROM so_ban_hang_chi_tiet AS SL
                         INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                         INNER JOIN DS_HANG_HOA  AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                         INNER JOIN DS_KHACH_HANG AS AO ON SL."DOI_TUONG_ID" = AO.id


                     WHERE
                         SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay


                     GROUP BY
                         SL."MA_HANG_ID",
                         SL."MA_HANG",

                         LII."DON_VI_TINH_CHINH",
                          LII."DON_VI_TINH",
                         SL."DOI_TUONG_ID"


                     UNION ALL

                     SELECT
                         IL."MA_HANG_ID"
                         , IL."MA_HANG"

                        , LII."DON_VI_TINH_CHINH"
                          ,LII."DON_VI_TINH"
                           ,IL."DOI_TUONG_ID"


                         , 0 
                         , 0
                         , 0
                         , 0
                         , 0
                         , 0
                         , 0
                         , 0

                        ,SUM("SO_TIEN_XUAT" -"SO_TIEN_NHAP") AS "SO_TIEN_CHI_PHI"
                     FROM so_kho_chi_tiet IL
                         INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                         INNER JOIN DS_HANG_HOA AS LII ON IL."MA_HANG_ID" = LII."MA_HANG_ID"
                         INNER JOIN DS_KHACH_HANG AS AO ON IL."DOI_TUONG_ID" = AO.id


                     WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                           AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                           AND (IL."LOAI_CHUNG_TU" = '2020'
                                OR IL."LOAI_CHUNG_TU" = '2013'
                           )


                     GROUP BY
                         IL."MA_HANG_ID",
                         IL."MA_HANG", -- Mã hàng
                          LII."DON_VI_TINH_CHINH",
                          LII."DON_VI_TINH",
                           IL."DOI_TUONG_ID"


                 ) T
                INNER JOIN DS_HANG_HOA AS LII ON T."MA_HANG_ID" = LII."MA_HANG_ID"
                INNER JOIN DS_KHACH_HANG LAO ON T."DOI_TUONG_ID" = LAO.id
            GROUP BY
                T."MA_HANG_ID" , --MA_HANG_ID
                T."MA_HANG" , -- Mã hàng --MA_HANG
                LII."TEN" , -- Tên hàng --TEN
                T."DON_VI_TINH_CHINH" ,

                "NGUON_GOC" , --nvtoan add 24/07/2017
                T."DON_VI_TINH" ,
                T."DOI_TUONG_ID" ,
                LAO."MA_KHACH_HANG" ,
                LAO."LIST_TEN_NHOM_KH_NCC",
                LAO."LIST_MA_NHOM_KH_NCC",
                LAO."HO_VA_TEN" ,
                LAO."DIA_CHI"



            HAVING SUM(T."SO_LUONG_BAN"
                   ) <> 0
                   OR SUM(T."SO_LUONG_KHUYEN_MAI"
                      ) <> 0
                   OR SUM(T."SO_LUONG_TRA_LAI"
                      ) <> 0
                   OR SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI"
                      ) <> 0
                   OR SUM(T."DOANH_SO_BAN"
                      ) <> 0
                   OR SUM(T."SO_TIEN_CHIET_KHAU"
                      ) <> 0
                   OR SUM(T."GIA_TRI_TRA_LAI"
                      ) <> 0
                   OR SUM(T."GIA_TRI_GIAM_GIA"
                      ) <> 0
                    OR SUM(T."SO_TIEN_CHI_PHI") <> 0


    ;

END $$
;
        SELECT
                "MA_KHACH_HANG" AS "MA_KHACH_HANG",
                "LIST_MA_NHOM_KH_NCC" AS "MA_NHOM_KH",
                "LIST_TEN_NHOM_KH_NCC" AS "TEN_NHOM_KH",
                "HO_VA_TEN" AS "TEN_KHACH_HANG",
                "TEN" AS "TEN_HANG",
                "DON_VI_TINH_CHINH" AS"DVT",
                "SO_LUONG_BAN" AS "SO_LUONG_BAN",
                "DOANH_SO_BAN" AS"DOANH_SO_BAN",
                "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU",
                "SO_LUONG_TRA_LAI" AS"SO_LUONG_TRA_LAI",
                "GIA_TRI_TRA_LAI" AS "GIA_TRI_TRA_LAI",
                "GIA_TRI_GIAM_GIA" AS"GIA_TRI_GIAM_GIA",
                "DOANH_THU_THUAN" AS "DOANH_THU_THUAN",
                 "SO_TIEN_CHI_PHI" AS "SO_TIEN_CHI_PHI"

            FROM TMP_KET_QUA
            OFFSET %(offset)s
            LIMIT %(limit)s;   


            
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_mat_hang_va_nhan_vien(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                            DATE := %(DEN_NGAY)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s ;
            
            
                loai_don_vi_tinh                    INTEGER := %(DON_VI_TINH)s;
            
                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;
            
              
            
            
                rec                                 RECORD;
            
            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;
            
                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;
            
            
                     DROP TABLE IF EXISTS DS_HANG_HOA;
            
                    CREATE TEMP TABLE DS_HANG_HOA
                        AS
                            SELECT
                                  II."id"                        AS "MA_HANG_ID"
                                , II."TEN"
                                , COALESCE(UI."DON_VI_TINH", '') AS "DON_VI_TINH_CHINH"
                                , CASE WHEN II."DVT_CHINH_ID" IS NULL
                                THEN ''
                                  ELSE U."DON_VI_TINH"
                                  END                            AS "DON_VI_TINH"
                                , "NGUON_GOC"
                                , II."TINH_CHAT"
                                , II."DVT_CHINH_ID"
                                , U."id"                         AS "DON_VI_CHUYEN_DOI"
                                , (CASE WHEN IIUC."VAT_TU_HANG_HOA_ID" IS NULL
                                THEN 1
                                   WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
                                       THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                   WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                                       THEN 1
                                   ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                   END)                          AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            FROM
                                danh_muc_vat_tu_hang_hoa AS II
                                LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC ON IIUC."STT" = loai_don_vi_tinh
                                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_CHINH_ID" = UI."id"
                                LEFT JOIN danh_muc_don_vi_tinh U ON (IIUC."VAT_TU_HANG_HOA_ID" IS NULL AND U."id" = II."DVT_CHINH_ID")
                                                                    OR (IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL AND IIUC."DVT_ID" = U."id")
                            WHERE
                                (II.id = any( %(SAN_PHAMIDS)s))--  %(SAN_PHAMIDS)s
                                  AND
                                  (loai_don_vi_tinh IS NULL OR loai_don_vi_tinh = 0 OR IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL)
                    ;
            
            
                DROP TABLE IF EXISTS DS_NHAN_VIEN
                ;
            
                CREATE TEMP TABLE DS_NHAN_VIEN
                    AS
                        SELECT
                            AO.id
                            , AO."MA_NHAN_VIEN"
                            , AO."HO_VA_TEN"
                            , AO."DIA_CHI"
                            ,AO."DIEN_THOAI"
                           , Ou.id AS "DON_VI_ID"
                            ,OU."MA_DON_VI"
                            ,OU."TEN_DON_VI"
                        FROM res_partner AS AO
                             LEFT JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU.id
            
                        WHERE (AO."id" = any( %(NHAN_VIEN_IDS)s)) --%(NHAN_VIEN_IDS)s
                ;
            
            
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                            T."MA_HANG_ID"
                            , T."MA_HANG"
            
                            , LII."TEN"
            
                            , T."DON_VI_TINH_CHINH"
                            , T."DON_VI_TINH"
                            , T."NHAN_VIEN_ID"
                            , AO."MA_NHAN_VIEN"
            
                            , AO."HO_VA_TEN"
            
                            , SUM(T."SO_LUONG_BAN")                      AS "SO_LUONG_BAN"
                            , SUM(T."SO_LUONG_KHUYEN_MAI")              AS "SO_LUONG_KHUYEN_MAI"
                            , SUM(T."SO_LUONG_TRA_LAI")              AS "SO_LUONG_TRA_LAI"
                             , SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI")        AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                            , SUM(T."DOANH_SO_BAN")                       AS "DOANH_SO_BAN"
                            , SUM(T."SO_TIEN_CHIET_KHAU")            AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")               AS "GIA_TRI_TRA_LAI"
                            , SUM(COALESCE(T."GIA_TRI_GIAM_GIA", 0)) AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - "GIA_TRI_TRA_LAI" -
                                  "GIA_TRI_GIAM_GIA")                AS "DOANH_THU_THUAN"
                             , SUM(T."SO_TIEN_CHI_PHI")                       AS "SO_TIEN_CHI_PHI"
            
            
                        FROM (
                                 SELECT
                                     SL."MA_HANG_ID"
                                     , SL."MA_HANG"
                                     , -- Mã hàng
                                     LII."DON_VI_TINH_CHINH"
                                     , LII."DON_VI_TINH"
                                     , SL."NHAN_VIEN_ID"
            
            
                                     , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
            
                                     , SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                     , -- Tiền chiết khấu
                                       SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                     , -- Giá trị trả lại
                                       SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                                     , -- Giá trị giảm giá
                                       SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                     AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                           THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN 0
                                                ELSE SL."SO_LUONG"
                                                END
                                           ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN 0
                                                ELSE SL."SO_LUONG_THEO_DVT_CHINH" *
                                                     COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                                END
                                           END)                     AS "SO_LUONG_BAN"
                                      ,SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                   AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                                   THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                                           THEN SL."SO_LUONG"
                                                            ELSE 0
                                                        END
                                                   ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                                       THEN SL."SO_LUONG_THEO_DVT_CHINH"  * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                                        ELSE  0
                                                        END
                                                   END)                     AS "SO_LUONG_KHUYEN_MAI"
            
            
                                     , SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                     AND SL."DVT_ID" =LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                         THEN 0
                                          ELSE SL."SO_LUONG_TRA_LAI"
                                          END
                                           ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                               THEN 0
                                                ELSE SL."SL_TRA_LAI_THEO_DVT_CHINH" *
                                                     COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                                END
                                           END)                     AS "SO_LUONG_TRA_LAI"
                                     ,SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                     AND SL."DVT_ID" =LII."DON_VI_CHUYEN_DOI"
                                                   THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                                           THEN SL."SO_LUONG_TRA_LAI"
                                                            ELSE 0
                                                        END
                                                   ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = TRUE
                                                       THEN SL."SL_TRA_LAI_THEO_DVT_CHINH"  * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                                        ELSE  0
                                                        END
                                                   END)                     AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                                    , 0 AS "SO_TIEN_CHI_PHI"
            
                                 FROM so_ban_hang_chi_tiet AS SL
                                     INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                     INNER JOIN DS_HANG_HOA  AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                                     INNER JOIN DS_NHAN_VIEN AS AO ON SL."NHAN_VIEN_ID" = AO.id
            
            
                                 WHERE
                                     SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
            
                                 GROUP BY
                                     SL."MA_HANG_ID",
                                     SL."MA_HANG",
            
                                     LII."DON_VI_TINH_CHINH",
                                      LII."DON_VI_TINH",
                                     SL."NHAN_VIEN_ID"
            
            
                                 UNION ALL
            
                                 SELECT
                                     IL."MA_HANG_ID"
                                     , IL."MA_HANG"
            
                                    , LII."DON_VI_TINH_CHINH"
                                      ,LII."DON_VI_TINH"
                                       ,IL."NHAN_VIEN_ID"
            
            
                                     , 0
                                     , 0
                                     , 0
                                     , 0
                                     , 0
                                     , 0
                                     , 0
                                     , 0
                                     ,SUM("SO_TIEN_XUAT" -"SO_TIEN_NHAP") AS "SO_TIEN_CHI_PHI"
            --
            
                                 FROM so_kho_chi_tiet IL
                                     INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                     INNER JOIN DS_HANG_HOA AS LII ON IL."MA_HANG_ID" = LII."MA_HANG_ID"
                                     INNER JOIN DS_NHAN_VIEN AS AO ON IL."NHAN_VIEN_ID" = AO.id
            
            
                                 WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
                                       AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                       AND (IL."LOAI_CHUNG_TU" = '2020'
                                            OR IL."LOAI_CHUNG_TU" = '2013'
                                       )
            
            
                                 GROUP BY
                                     IL."MA_HANG_ID",
                                     IL."MA_HANG", -- Mã hàng
                                      LII."DON_VI_TINH_CHINH",
                                      LII."DON_VI_TINH",
                                       IL."NHAN_VIEN_ID"
            
            
                             )AS T
                            INNER JOIN DS_HANG_HOA AS LII ON T."MA_HANG_ID" = LII."MA_HANG_ID"
                            INNER JOIN DS_NHAN_VIEN AO ON T."NHAN_VIEN_ID" = AO.id
                        GROUP BY
                            T."MA_HANG_ID" , --MA_HANG_ID
                            T."MA_HANG" , -- Mã hàng --MA_HANG
                            LII."TEN" , -- Tên hàng --TEN
                            T."DON_VI_TINH_CHINH" ,
                            T."DON_VI_TINH" ,
                            T."NHAN_VIEN_ID" ,
                            AO."MA_NHAN_VIEN" ,
                            AO."HO_VA_TEN" ,
                            AO."DIA_CHI"
            
            
            
                        HAVING SUM(T."SO_LUONG_BAN"
                               ) <> 0
                               OR SUM(T."SO_LUONG_KHUYEN_MAI"
                                  ) <> 0
                               OR SUM(T."SO_LUONG_TRA_LAI"
                                  ) <> 0
                               OR SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI"
                                  ) <> 0
                               OR SUM(T."DOANH_SO_BAN"
                                  ) <> 0
                               OR SUM(T."SO_TIEN_CHIET_KHAU"
                                  ) <> 0
                               OR SUM(T."GIA_TRI_TRA_LAI"
                                  ) <> 0
                               OR SUM(T."GIA_TRI_GIAM_GIA"
                                  ) <> 0
                                OR SUM(T."SO_TIEN_CHI_PHI") <> 0
            
            
                ;
            
            END $$
            ;
                    SELECT
                            "MA_NHAN_VIEN" AS "MA_NHAN_VIEN",
                            "HO_VA_TEN" AS"TEN_NHAN_VIEN",
                            "TEN" AS "TEN_HANG",
                            "DON_VI_TINH_CHINH" AS"DVT",
                            "SO_LUONG_BAN" AS "SO_LUONG_BAN",
                            "DOANH_SO_BAN" AS"DOANH_SO_BAN",
                            "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU",
                            "SO_LUONG_TRA_LAI" AS"SO_LUONG_TRA_LAI",
                            "GIA_TRI_TRA_LAI" AS "GIA_TRI_TRA_LAI",
                            "GIA_TRI_GIAM_GIA" AS"GIA_TRI_GIAM_GIA",
                            "DOANH_THU_THUAN" AS "DOANH_THU_THUAN"

                        FROM TMP_KET_QUA 
                        OFFSET %(offset)s
                        LIMIT %(limit)s;
            """
        return self.execute(query,params_sql)


    def _lay_bao_cao_khach_hang(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s; 

                den_ngay                            DATE := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s; 

                chi_lay_khach_hang_co_phat_sinh     INTEGER := %(CHI_LAY_KHACH_HANG_CO_PHAT_SINH)s; 


                don_vi_id                           INTEGER := %(DON_VI)s;

                nhan_vien_id                        INTEGER := %(NHAN_VIEN)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


             


                rec                                 RECORD;

                MA_PHAN_CAP                         VARCHAR(100);


            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_KHACH_HANG
                ;

                CREATE TEMP TABLE DS_KHACH_HANG
                    AS
                        SELECT
                              "id"                                  AS "DOI_TUONG_ID"
                            , "MA_KHACH_HANG"
                            , "HO_VA_TEN"
                            , "DIA_CHI"
                            , "MA_SO_THUE"
                            , AOD."DIEN_THOAI"
                            , CASE WHEN AOD."LOAI_KHACH_HANG" = '1'
                            THEN AOD."DT_DI_DONG"
                              WHEN AOD."LOAI_KHACH_HANG" = '0'
                                  THEN NULL END                     AS "DT_DI_DONG"
                            , CASE WHEN AOD."LOAI_KHACH_HANG" = '1'
                            THEN NULL
                              WHEN AOD."LOAI_KHACH_HANG" = '0'
                                  THEN AOD."FAX" END                AS "FAX"
                            , AOD."EMAIL"
                            , CASE WHEN AOD."LOAI_KHACH_HANG" = '1'
                            THEN NULL
                              WHEN AOD."LOAI_KHACH_HANG" = '0'
                                  THEN AOD."HO_VA_TEN_LIEN_HE" END  AS "HO_VA_TEN_LIEN_HE"
                            , CASE WHEN AOD."LOAI_KHACH_HANG" = '1'
                            THEN NULL
                              WHEN AOD."LOAI_KHACH_HANG" = '0'
                                  THEN AOD."CHUC_DANH" END          AS "CHUC_DANH"
                            , CASE WHEN AOD."LOAI_KHACH_HANG" = '1'
                            THEN NULL
                              WHEN AOD."LOAI_KHACH_HANG" = '0'
                                  THEN AOD."DT_DI_DONG_LIEN_HE" END AS "DT_DI_DONG_LIEN_HE"
                            , CASE WHEN AOD."LOAI_KHACH_HANG" = '1'
                            THEN NULL
                              WHEN AOD."LOAI_KHACH_HANG" = '0'
                                  THEN AOD."EMAIL_LIEN_HE" END      AS "EMAIL_LIEN_HE"
                            , AOD."TINH_TP_ID"
                            , AOD."QUAN_HUYEN_ID"
                            , AOD."XA_PHUONG_ID"
                        FROM res_partner AOD

                        WHERE (AOD."id" = any(%(KHACH_HANG_IDS)s))


                ;


                SELECT concat("MA_PHAN_CAP", '%%')
                INTO MA_PHAN_CAP
                FROM danh_muc_to_chuc
                WHERE "id" = don_vi_id
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY AO."MA_KHACH_HANG", AO."HO_VA_TEN" ) AS "SO_DONG"
                            , AO."DOI_TUONG_ID"
                            , AO."MA_KHACH_HANG"
                            , AO."HO_VA_TEN"
                            , AO."TINH_TP_ID"
                            , AO."QUAN_HUYEN_ID"
                            , AO."XA_PHUONG_ID"
                            , SUM(T."DOANH_SO_BAN")                             AS "DOANH_SO_BAN"
                            , SUM(T."SO_TIEN_CHIET_KHAU")                       AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")                          AS "GIA_TRI_TRA_LAI"
                            , SUM(T."GIA_TRI_GIAM_GIA")                         AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                                  - T."GIA_TRI_GIAM_GIA")                       AS "DOANH_THU_THUAN"
                            , SUM(T."GIA_VON")                                  AS "GIA_VON"


                        FROM (SELECT
                                  SL."DOI_TUONG_ID"
                                  , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                                  , -- Doanh số bán
                                    SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                  , -- Tiền chiết khấu
                                    SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                  , -- Giá trị trả lại
                                    SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"  -- Giá trị giảm giá
                                  , 0                            AS "GIA_VON"
                              FROM so_ban_hang_chi_tiet AS SL
                                  INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  INNER JOIN DS_KHACH_HANG AOL ON AOL."DOI_TUONG_ID" = SL."DOI_TUONG_ID"
                                  LEFT JOIN danh_muc_to_chuc OU ON OU."id" = SL."DON_VI_ID"
                              WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                    AND (SL."NHAN_VIEN_ID" = nhan_vien_id
                                         OR nhan_vien_id IS NULL
                                    )
                                    AND (don_vi_id IS NULL
                                         OR OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP
                                    )
                              GROUP BY SL."DOI_TUONG_ID"
                              UNION ALL
                              SELECT
                                  IL."DOI_TUONG_ID"
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                              FROM so_kho_chi_tiet IL
                                  INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  INNER JOIN DS_KHACH_HANG AS LAO ON IL."DOI_TUONG_ID" = LAO."DOI_TUONG_ID"
                                  LEFT JOIN danh_muc_to_chuc OU ON OU."id" = IL."DON_VI_ID"
                              WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                    AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                    AND (nhan_vien_id IS NULL
                                         OR IL."NHAN_VIEN_ID" = nhan_vien_id
                                    )
                                    AND (don_vi_id IS NULL
                                         OR OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP
                                    )
                                    AND (IL."LOAI_CHUNG_TU" = '2020'
                                         OR IL."LOAI_CHUNG_TU" = '2013'
                                    )
                              GROUP BY IL."DOI_TUONG_ID"
                             ) T
                            INNER JOIN DS_KHACH_HANG AO ON AO."DOI_TUONG_ID" = T."DOI_TUONG_ID"
                        GROUP BY
                            AO."DOI_TUONG_ID",
                            AO."MA_KHACH_HANG",
                            AO."HO_VA_TEN",

                            AO."TINH_TP_ID",
                            AO."QUAN_HUYEN_ID",
                            AO."XA_PHUONG_ID"
                        HAVING SUM(T."DOANH_SO_BAN") <> 0
                               OR SUM(T."SO_TIEN_CHIET_KHAU") <> 0
                               OR SUM(T."GIA_TRI_TRA_LAI") <> 0
                               OR SUM(T."GIA_TRI_GIAM_GIA") <> 0
                               OR SUM(T."GIA_VON") <> 0
                ;


                /*Phân tách trường hợp NSD tích chọn cho phép in hiển thị cả khách hàng không phát sinh số liệu trong kỳ lên báo cáo*/

                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;

                IF chi_lay_khach_hang_co_phat_sinh = 1
                THEN
                    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                        AS
                            SELECT

                                T."SO_DONG"
                                , T."DOI_TUONG_ID"
                                , T."MA_KHACH_HANG"
                                , T."HO_VA_TEN"
                                , T."TINH_TP_ID"
                                , T."QUAN_HUYEN_ID"
                                , T."XA_PHUONG_ID"
                                , T."DOANH_SO_BAN"
                                , T."SO_TIEN_CHIET_KHAU"
                                , T."GIA_TRI_TRA_LAI"
                                , T."GIA_TRI_GIAM_GIA"
                                , T."DOANH_THU_THUAN"
                                , T."GIA_VON"

                            FROM TMP_KET_QUA T
                    ;

                ELSE

                    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                        AS
                            SELECT
                                ROW_NUMBER()
                                OVER (
                                    ORDER BY AO."MA_KHACH_HANG", AO."HO_VA_TEN" ) AS "SO_DONG"
                                , AO."DOI_TUONG_ID"
                                , AO."MA_KHACH_HANG"
                                , AO."HO_VA_TEN"
                                , AO."TINH_TP_ID"
                                , AO."QUAN_HUYEN_ID"
                                , AO."XA_PHUONG_ID"
                                , T."DOANH_SO_BAN"
                                , T."SO_TIEN_CHIET_KHAU"
                                , T."GIA_TRI_TRA_LAI"
                                , T."GIA_TRI_GIAM_GIA"
                                , T."DOANH_THU_THUAN"
                                , T."GIA_VON"
                            FROM DS_KHACH_HANG AS AO
                                LEFT JOIN TMP_KET_QUA T ON T."DOI_TUONG_ID" = AO."DOI_TUONG_ID"
                    ;
                END IF
                ;


            END $$
            ;

            SELECT
                  "MA_KHACH_HANG"      AS "MA_KHACH_HANG"
                , "HO_VA_TEN"          AS "TEN_KHACH_HANG"
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"
                , "TINH_TP_ID"         AS "TINH_THANH_PHO"
                , "QUAN_HUYEN_ID"      AS "QUAN_HUYEN"
                , "XA_PHUONG_ID"       AS "XA_PHUONG"


            FROM TMP_KET_QUA_CUOI_CUNG
            OFFSET %(offset)s
            LIMIT %(limit)s;






            
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_nhan_vien(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;

                den_ngay                            DATE := %(DEN_NGAY)s; 

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s; 


                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s; 


               


                rec                                 RECORD;




            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_NHAN_VIEN
                ;

                CREATE TEMP TABLE DS_NHAN_VIEN
                    AS
                        SELECT

                            AO."id" AS "NHAN_VIEN_ID"
                            ,AO."MA_NHAN_VIEN"
                            , AO."HO_VA_TEN"
                            , OU."id" AS "DON_VI_ID"
                            , OU."TEN_DON_VI"
                        FROM res_partner AO LEFT JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"

                        WHERE (AO."id" = any (%(NHAN_VIEN_IDS)s)) 
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY LAO."MA_NHAN_VIEN" ) AS RowNum
                                , T."NHAN_VIEN_ID"
                                , LAO."MA_NHAN_VIEN"
                                , LAO."HO_VA_TEN"
                                , LAO."DON_VI_ID"
                                , LAO."TEN_DON_VI"
                                , SUM(T."DOANH_SO_BAN")             AS "DOANH_SO_BAN"
                                , SUM(T."SO_TIEN_CHIET_KHAU")       AS "SO_TIEN_CHIET_KHAU"
                                , SUM(T."GIA_TRI_TRA_LAI")          AS "GIA_TRI_TRA_LAI"
                                , SUM(T."GIA_TRI_GIAM_GIA")         AS "GIA_TRI_GIAM_GIA"
                                , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                                      - T."GIA_TRI_GIAM_GIA")       AS "DOANH_THU_THUAN"
                                , SUM(T."GIA_VON")                  AS "GIA_VON"


                         From
                       (SELECT
                            SL."NHAN_VIEN_ID" ,
                            SUM(SL."SO_TIEN") AS "DOANH_SO_BAN" , -- Doanh số bán
                            SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU" , -- Tiền chiết khấu
                            SUM(SL."SO_TIEN_TRA_LAI") AS "GIA_TRI_TRA_LAI" , -- Giá trị trả lại
                            SUM(SL."SO_TIEN_GIAM_TRU") AS "GIA_TRI_GIAM_GIA" , -- Giá trị giảm giá
                            0 AS "GIA_VON"
                    FROM    so_ban_hang_chi_tiet AS SL
                            INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN DS_NHAN_VIEN AS LAO ON SL."NHAN_VIEN_ID" = LAO."NHAN_VIEN_ID"
                    WHERE   SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                    GROUP BY SL."NHAN_VIEN_ID" ,
                            SL."MA_NHAN_VIEN" ,
                            LAO."HO_VA_TEN" ,
                            LAO."DON_VI_ID" ,
                            LAO."TEN_DON_VI"
                    UNION ALL
                        SELECT  IL."NHAN_VIEN_ID" ,
                                0,
                                0,
                                0,
                                0,
                                SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                            FROM    so_kho_chi_tiet IL
                                    INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                    INNER JOIN DS_NHAN_VIEN AS LAO ON IL."NHAN_VIEN_ID" = LAO."NHAN_VIEN_ID"
                            WHERE   IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                    AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                    AND ( IL."LOAI_CHUNG_TU" = '2020'
                                          OR IL."LOAI_CHUNG_TU" = '2013'
                                        )
                            GROUP BY IL."NHAN_VIEN_ID"
                    ) AS T
                    INNER JOIN DS_NHAN_VIEN LAO ON LAO."NHAN_VIEN_ID" = T."NHAN_VIEN_ID"
                    GROUP BY T."NHAN_VIEN_ID" ,
                            LAO."MA_NHAN_VIEN" , -- Mã NCC
                            LAO."HO_VA_TEN" ,
                            LAO."DON_VI_ID" ,
                            LAO."TEN_DON_VI"

                    HAVING
                    SUM(T."DOANH_SO_BAN") <> 0 OR SUM(T."SO_TIEN_CHIET_KHAU") <> 0 OR SUM(T."GIA_TRI_TRA_LAI") <> 0 OR SUM(T."GIA_TRI_GIAM_GIA") <> 0 OR SUM(T."GIA_VON") <>0;

            END $$
            ;

            SELECT
                  "MA_NHAN_VIEN"                   AS "MA_NHAN_VIEN"
                , "HO_VA_TEN"          AS "TEN_NHAN_VIEN"
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"

                , "TEN_DON_VI"       AS "DON_VI_KINH_DOANH"


            FROM TMP_KET_QUA
            OFFSET %(offset)s
            LIMIT %(limit)s;
            
            """
        return self.execute(query,params_sql)




    def _lay_bao_cao_nhan_vien_va_khach_hang(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;

                den_ngay                            DATE := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s; 

               

                rec                                 RECORD;


            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_KHACH_HANG
                ;

                CREATE TEMP TABLE DS_KHACH_HANG
                    AS
                        SELECT
                            CU."id" AS "KHACH_HANG_ID"
                            , CU."MA_KHACH_HANG"
                            , CU."HO_VA_TEN" AS "TEN_KHACH_HANG"
                            , CU."DIA_CHI"
                            , CU."MA_SO_THUE"
                            , CU."LIST_MA_NHOM_KH_NCC"
                            , CU."LIST_TEN_NHOM_KH_NCC"

                        FROM res_partner AS CU
                        WHERE ("id" = any (%(KHACH_HANG_IDS)s)) 
                ;


                DROP TABLE IF EXISTS DS_NHAN_VIEN
                ;

                CREATE TEMP TABLE DS_NHAN_VIEN
                    AS
                        SELECT

                              AO."id" AS "NHAN_VIEN_ID"
                            , AO."MA_NHAN_VIEN"
                            , AO."HO_VA_TEN" AS "TEN_NHAN_VIEN"
                            , O."id"  AS "DON_VI_ID"
                            , O."TEN_DON_VI"
                        FROM res_partner AO LEFT JOIN danh_muc_to_chuc O ON AO."DON_VI_ID" = O."id"

                        WHERE (AO."id" =  any(%(NHAN_VIEN_IDS)s)) 
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY E."MA_NHAN_VIEN", CU."MA_KHACH_HANG" ) AS RowNum
                            , E."NHAN_VIEN_ID"
                            , E."MA_NHAN_VIEN"
                            , -- Mã nhân viên
                            E."TEN_NHAN_VIEN"
                            , CU."KHACH_HANG_ID"
                            , CU."MA_KHACH_HANG"
                            , CU."TEN_KHACH_HANG"
                            , CU."DIA_CHI"

                            ,CU."MA_SO_THUE"
                            , CU."LIST_MA_NHOM_KH_NCC"
                            , CU."LIST_TEN_NHOM_KH_NCC"
                            , E."TEN_DON_VI"                                      AS "DON_VI_KHINH_DOANH"
                            , SUM(T."DOANH_SO_BAN")                               AS "DOANH_SO_BAN"

                            , SUM(T."SO_TIEN_CHIET_KHAU")                         AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")                            AS "GIA_TRI_TRA_LAI"
                            , SUM(T."GIA_TRI_GIAM_GIA")                           AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                                  - T."GIA_TRI_GIAM_GIA")                         AS "DOANH_THU_THUAN"
                            , SUM(T."GIA_VON")                                    AS "GIA_VON"
                            ,SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" -T."GIA_VON") AS "LAI_GOP"
                            , CASE WHEN SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA") > 0
                                        AND SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" -
                                                T."GIA_VON") > 0
                                        OR
                                        SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA") < 0
                                        AND SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" -
                                                T."GIA_VON") < 0
                            THEN
                                SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" - T."GIA_VON")
                                * 100 / SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA")
                              ELSE 0
                              END                                                 AS "TY_LE_LAI_GOP"


                        FROM
                            (SELECT
                                 SL."NHAN_VIEN_ID"
                                 , SL."DOI_TUONG_ID"
                                 , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"

                                 , -- Doanh số bán
                                   SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                 , -- Tiền chiết khấu
                                   SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                 , -- Giá trị trả lại
                                   SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"  -- Giá trị giảm giá
                                 , 0                            AS "GIA_VON"
                             FROM so_ban_hang_chi_tiet AS SL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN DS_KHACH_HANG AS CU ON SL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
                                 INNER JOIN DS_NHAN_VIEN AS E ON SL."NHAN_VIEN_ID" = E."NHAN_VIEN_ID"
                             WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                             GROUP BY
                                 SL."NHAN_VIEN_ID",
                                 SL."DOI_TUONG_ID"
                             UNION ALL
                             SELECT
                                 IL."NHAN_VIEN_ID"
                                 , IL."DOI_TUONG_ID"
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                             FROM so_kho_chi_tiet IL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN DS_KHACH_HANG AS CU ON IL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
                                 INNER JOIN DS_NHAN_VIEN AS E ON IL."NHAN_VIEN_ID" = E."NHAN_VIEN_ID"
                             WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                   AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                   AND (IL."LOAI_CHUNG_TU" = '2020'
                                        OR IL."LOAI_CHUNG_TU" = '2013'
                                   )
                             GROUP BY IL."NHAN_VIEN_ID",
                                 IL."DOI_TUONG_ID"
                            ) AS T
                            INNER JOIN DS_NHAN_VIEN E ON E."NHAN_VIEN_ID" = T."NHAN_VIEN_ID"
                            INNER JOIN DS_KHACH_HANG CU ON CU."KHACH_HANG_ID" = T."DOI_TUONG_ID"
                        GROUP BY
                            E."NHAN_VIEN_ID",
                            E."MA_NHAN_VIEN", -- Mã nhân viên
                            E."TEN_NHAN_VIEN",
                            CU."KHACH_HANG_ID",
                            CU."MA_KHACH_HANG",
                            CU."TEN_KHACH_HANG",
                            CU."DIA_CHI", -- Địa chỉ
                            CU."MA_SO_THUE",
                            CU."LIST_MA_NHOM_KH_NCC",
                            CU."LIST_TEN_NHOM_KH_NCC",

                            E."TEN_DON_VI"

                        HAVING
                            SUM(T."DOANH_SO_BAN"
                            ) <> 0 OR SUM(T."SO_TIEN_CHIET_KHAU"
                                      ) <> 0 OR SUM(T."GIA_TRI_TRA_LAI"
                                                ) <> 0 OR SUM(T."GIA_TRI_GIAM_GIA"
                                                          ) <> 0 OR SUM(T."GIA_VON"
                                                                    ) <> 0
                ;

            END $$
            ;

            SELECT
                  "MA_NHAN_VIEN"       AS "MA_NHAN_VIEN"
                , "TEN_NHAN_VIEN"          AS "TEN_NHAN_VIEN"
                 ,"MA_KHACH_HANG"       AS "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"          AS "TEN_KHACH_HANG"
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"
                , "GIA_VON"   AS "TIEN_VON"
                , "LAI_GOP"    AS "LAI_GOP"
                , "TY_LE_LAI_GOP"    AS "TY_LE_LAI_GOP"
                , "LIST_MA_NHOM_KH_NCC"    AS "MA_NHOM_KH"
                , "LIST_TEN_NHOM_KH_NCC"    AS "TEN_NHOM_KH"

                , "DON_VI_KHINH_DOANH"         AS "DON_VI_KINH_DOANH"


            FROM TMP_KET_QUA
            OFFSET %(offset)s
            LIMIT %(limit)s;
            

            
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_nhan_vien_khach_hang_va_mat_hang(self, params_sql):      
        record = []
        query = """
            
                                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s; 

                den_ngay                            DATE := %(DEN_NGAY)s; 

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

                don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;

              

                rec                                 RECORD;


            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_KHACH_HANG
                ;

                CREATE TEMP TABLE DS_KHACH_HANG
                    AS
                        SELECT
                              CU."id"        AS "KHACH_HANG_ID"
                            , CU."MA_KHACH_HANG"
                            , CU."HO_VA_TEN" AS "TEN_KHACH_HANG"
                            , CU."DIA_CHI"

                            , CASE WHEN CU."LOAI_KHACH_HANG" = '0'
                            THEN CU."DIEN_THOAI"
                              ELSE CU."DT_DI_DONG"
                              END

                        FROM res_partner AS CU
                        WHERE ("id" = any (%(KHACH_HANG_IDS)s))
                ;

                DROP TABLE IF EXISTS DS_HANG_HOA
                ;

                CREATE TEMP TABLE DS_HANG_HOA
                    AS
                        SELECT
                              II."id"                        AS "MA_HANG_ID"
                            , II."TEN"                       AS "TEN_HANG"
                            , COALESCE(UI."DON_VI_TINH", '') AS "DON_VI_TINH_CHINH"
                            , CASE WHEN II."DVT_CHINH_ID" IS NULL
                            THEN ''
                              ELSE U."DON_VI_TINH"
                              END                            AS "DON_VI_TINH"
                            , "NGUON_GOC"
                            , II."TINH_CHAT"
                            , II."DVT_CHINH_ID"
                            , U."id"                         AS "DON_VI_CHUYEN_DOI"
                            , (CASE WHEN IIUC."VAT_TU_HANG_HOA_ID" IS NULL
                            THEN 1
                               WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
                                   THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                               WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                                   THEN 1
                               ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                               END)                          AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                        FROM
                            danh_muc_vat_tu_hang_hoa AS II
                            LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                                ON IIUC."VAT_TU_HANG_HOA_ID" = II."id" AND IIUC."STT" = don_vi_tinh
                            LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_CHINH_ID" = UI."id"
                            LEFT JOIN danh_muc_don_vi_tinh U ON (IIUC."VAT_TU_HANG_HOA_ID" IS NULL AND U."id" = II."DVT_CHINH_ID")
                                                                OR (IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL AND IIUC."DVT_ID" = U."id")
                        WHERE

                            (don_vi_tinh IS NULL OR don_vi_tinh = 0 OR IIUC."VAT_TU_HANG_HOA_ID" IS NOT NULL)
                ;


                DROP TABLE IF EXISTS DS_NHAN_VIEN
                ;

                CREATE TEMP TABLE DS_NHAN_VIEN
                    AS
                        SELECT

                              AO."id"        AS "NHAN_VIEN_ID"
                            , AO."MA_NHAN_VIEN"
                            , AO."HO_VA_TEN" AS "TEN_NHAN_VIEN"
                            , AO."DIA_CHI_LIEN_HE"
                            , AO."DT_DI_DONG_LIEN_HE"
                            , OU."id"        AS "DON_VI_ID"
                            , OU."MA_DON_VI"
                            , OU."TEN_DON_VI"
                        FROM res_partner AO LEFT JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"

                        WHERE (AO."id" = any (%(NHAN_VIEN_IDS)s))
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY AO."MA_NHAN_VIEN", CU."MA_KHACH_HANG", T."MA_HANG" ) AS RowNum
                            , T."MA_HANG_ID"
                            , T."MA_HANG"
                            , -- Mã hàng
                            LII."TEN_HANG"
                            , -- Tên hàng
                            T."DON_VI_TINH_CHINH"
                            , T."DON_VI_TINH"
                            , T."NHAN_VIEN_ID"
                            , AO."MA_NHAN_VIEN"
                            , AO."TEN_NHAN_VIEN"
                            , CU."KHACH_HANG_ID"
                            , CU."MA_KHACH_HANG"
                            , CU."TEN_KHACH_HANG"
                            , SUM(T."SO_LUONG_BAN")                                             AS "SO_LUONG_BAN"
                            , SUM(T."SO_LUONG_KHUYEN_MAI")                                      AS "SO_LUONG_KHUYEN_MAI"
                            , SUM(T."SO_LUONG_TRA_LAI")                                         AS "SO_LUONG_TRA_LAI"
                            , SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI")                              AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                            , SUM(T."DOANH_SO_BAN")                                             AS "DOANH_SO_BAN"
                            , SUM(T."SO_TIEN_CHIET_KHAU")                                       AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")                                          AS "GIA_TRI_TRA_LAI"
                            , SUM(T."GIA_TRI_GIAM_GIA")                                         AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                                  - T."GIA_TRI_GIAM_GIA")                                       AS "DOANH_THU_THUAN"
                            , SUM(T."GIA_VON")                                                  AS "GIA_VON"

                        FROM (SELECT
                                  CU."KHACH_HANG_ID"
                                  , SL."MA_HANG_ID"
                                  , SL."MA_HANG"
                                  , LII."DON_VI_TINH_CHINH"
                                  , LII."DON_VI_TINH"
                                  , SL."NHAN_VIEN_ID"
                                  , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                                  , -- Doanh số bán
                                    SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                  , -- Tiền chiết khấu
                                    SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                  , -- Giá trị trả lại
                                    SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                                  , -- Giá trị giảm giá

                                    SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                  AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                        THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN 0
                                             ELSE SL."SO_LUONG"
                                             END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN 0
                                             ELSE SL."SO_LUONG_THEO_DVT_CHINH"
                                                  * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                                                             1)
                                             END
                                        END)                     AS "SO_LUONG_BAN"
                                  , SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                  AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                    THEN SL."SO_LUONG"
                                     ELSE 0
                                     END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN SL."SO_LUONG_THEO_DVT_CHINH"
                                                 * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                                                            1)
                                             ELSE 0
                                             END
                                        END)                     AS "SO_LUONG_KHUYEN_MAI"
                                  , SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                  AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                    THEN 0
                                     ELSE SL."SO_LUONG_TRA_LAI"
                                     END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN 0
                                             ELSE SL."SL_TRA_LAI_THEO_DVT_CHINH"
                                                  * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                                                             1)
                                             END
                                        END)                     AS "SO_LUONG_TRA_LAI"
                                  , SUM(CASE WHEN LII."DON_VI_CHUYEN_DOI" IS NOT NULL
                                                  AND SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                    THEN SL."SO_LUONG_TRA_LAI"
                                     ELSE 0
                                     END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN SL."SL_TRA_LAI_THEO_DVT_CHINH"
                                                 * COALESCE(LII."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                                                            1)
                                             ELSE 0
                                             END
                                        END)                     AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                                  , 0                            AS "GIA_VON"
                              FROM so_ban_hang_chi_tiet AS SL
                                  INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  INNER JOIN DS_HANG_HOA AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                                  INNER JOIN DS_NHAN_VIEN AS AO ON SL."NHAN_VIEN_ID" = AO."NHAN_VIEN_ID"
                                  INNER JOIN DS_KHACH_HANG AS CU ON SL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
                              WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                              GROUP BY SL."MA_HANG_ID",
                                  SL."MA_HANG",
                                  LII."DON_VI_TINH_CHINH",
                                  LII."DON_VI_TINH",
                                  SL."NHAN_VIEN_ID",
                                  CU."KHACH_HANG_ID"
                              UNION ALL
                              SELECT
                                  CU."KHACH_HANG_ID"
                                  , IL."MA_HANG_ID"
                                  , IL."MA_HANG"
                                  , LII."DON_VI_TINH_CHINH"
                                  , LII."DON_VI_TINH"
                                  , IL."NHAN_VIEN_ID"
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0

                                  , SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                              FROM so_kho_chi_tiet IL
                                  INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  INNER JOIN DS_HANG_HOA AS LII ON IL."MA_HANG_ID" = LII."MA_HANG_ID"
                                  INNER JOIN DS_NHAN_VIEN AS AO ON IL."NHAN_VIEN_ID" = AO."NHAN_VIEN_ID"
                                  INNER JOIN DS_KHACH_HANG AS CU ON IL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
                              WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                    AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                    AND (IL."LOAI_CHUNG_TU" = '2020'
                                         OR IL."LOAI_CHUNG_TU" = '2013'
                                    )
                              GROUP BY IL."MA_HANG_ID",
                                  IL."MA_HANG", -- Mã hàng
                                  LII."DON_VI_TINH_CHINH",
                                  LII."DON_VI_TINH",
                                  IL."NHAN_VIEN_ID",
                                  CU."KHACH_HANG_ID"
                             ) AS T
                            INNER JOIN DS_NHAN_VIEN AO ON AO."NHAN_VIEN_ID" = T."NHAN_VIEN_ID"
                            INNER JOIN DS_HANG_HOA LII ON LII."MA_HANG_ID" = T."MA_HANG_ID"
                            INNER JOIN DS_KHACH_HANG AS CU ON T."KHACH_HANG_ID" = CU."KHACH_HANG_ID"
                        GROUP BY T."MA_HANG_ID",
                            T."MA_HANG", -- Mã hàng
                            LII."TEN_HANG", -- Tên hàng
                            T."DON_VI_TINH_CHINH",
                            T."DON_VI_TINH",
                            T."NHAN_VIEN_ID",
                            AO."MA_NHAN_VIEN",
                            AO."TEN_NHAN_VIEN",

                            CU."KHACH_HANG_ID",
                            CU."MA_KHACH_HANG",
                            CU."TEN_KHACH_HANG"

                        HAVING SUM(T."SO_LUONG_BAN") <> 0
                               OR SUM(T."SO_LUONG_KHUYEN_MAI") <> 0
                               OR SUM(T."SO_LUONG_TRA_LAI") <> 0
                               OR SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI") <> 0
                               OR SUM(T."DOANH_SO_BAN") <> 0
                               OR SUM(T."SO_TIEN_CHIET_KHAU") <> 0
                               OR SUM(T."GIA_TRI_TRA_LAI") <> 0
                               OR SUM(T."GIA_TRI_GIAM_GIA") <> 0
                               OR SUM(T."GIA_VON") <> 0
                ;

            END $$
            ;

            SELECT

                  "TEN_NHAN_VIEN"      AS "TEN_NHAN_VIEN"

                , "TEN_KHACH_HANG"     AS "TEN_KHACH_HANG"
                , "MA_HANG"            AS "MA_HANG"
                , "DON_VI_TINH_CHINH"  AS "DVT"
                , "SO_LUONG_BAN"       AS "SO_LUONG_BAN"
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                , "SO_LUONG_TRA_LAI"   AS "SO_LUONG_TRA_LAI"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"


            FROM TMP_KET_QUA 
            OFFSET %(offset)s
            LIMIT %(limit)s;


            

            
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_theo_dia_phuong(self, params_sql):      
        record = []
        query = """
            
                            DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;

                den_ngay                            DATE := %(DEN_NGAY)s;
                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s; 

                tinh_tp_id                          INTEGER :=%(TINH_THANH_PHO_ID)s; 

                quan_huyen_id                       INTEGER := %(QUAN_HUYEN_ID)s;

                phuong_xa_id                        INTEGER := %(XA_PHUONG_ID)s;

                nhan_vien_id                        INTEGER := %(NHAN_VIEN_ID)s;

                mat_hang_id                         INTEGER := %(MAT_HANG_ID)s;


                rec                                 RECORD;


            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY T."TINH_TP_ID", T."QUAN_HUYEN_ID", T."XA_PHUONG_ID" ) AS RowNum
                            , mat_hang_id                                                        AS "MA_HANG_ID"
                            , T."TINH_TP_ID"
                            , T."QUAN_HUYEN_ID"
                            , T."XA_PHUONG_ID"
                            , SUM(T."DOANH_SO_BAN")                                              AS "DOANH_SO_BAN"
                            , SUM(T."SO_TIEN_CHIET_KHAU")                                        AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")                                           AS "GIA_TRI_TRA_LAI"
                            , SUM(T."GIA_TRI_GIAM_GIA")                                          AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                                  - T."GIA_TRI_GIAM_GIA")                                        AS "DOANH_THU_THUAN"
                        FROM
                            (SELECT
                                 AO."TINH_TP_ID"
                                 , AO."QUAN_HUYEN_ID"
                                 , AO."XA_PHUONG_ID"
                                 , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                                 , -- Doanh số bán
                                   SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                 , -- Tiền chiết khấu
                                   SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                 , -- Giá trị trả lại
                                   SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"


                             FROM so_ban_hang_chi_tiet AS SL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON SL."MA_HANG_ID" = II."id"
                                 INNER JOIN res_partner AS AO ON SL."DOI_TUONG_ID" = AO.id
                             WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                   AND (nhan_vien_id IS NULL
                                        OR SL."NHAN_VIEN_ID" = nhan_vien_id)
                                   AND (mat_hang_id IS NULL
                                        OR SL."MA_HANG_ID" = mat_hang_id
                                   )
                                   AND (tinh_tp_id IS NULL
                                        OR AO."TINH_TP_ID" = tinh_tp_id
                                   )
                                   AND (quan_huyen_id IS NULL
                                        OR AO."QUAN_HUYEN_ID" = quan_huyen_id
                                   )
                                   AND (phuong_xa_id IS NULL
                                        OR AO."XA_PHUONG_ID" = phuong_xa_id
                                   )
                             GROUP BY
                                 AO."TINH_TP_ID",
                                 AO."QUAN_HUYEN_ID",
                                 AO."XA_PHUONG_ID"
                             UNION ALL
                             SELECT
                                 AO."TINH_TP_ID"
                                 , AO."QUAN_HUYEN_ID"
                                 , AO."XA_PHUONG_ID"
                                 , 0
                                 , 0
                                 , 0
                                 , 0


                             FROM so_kho_chi_tiet IL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN res_partner AS AO ON IL."DOI_TUONG_ID" = AO.id
                             WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                   AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                   AND (nhan_vien_id IS NULL
                                        OR IL."NHAN_VIEN_ID" = nhan_vien_id)
                                   AND (mat_hang_id IS NULL
                                        OR il."MA_HANG_ID" = mat_hang_id
                                   )
                                   AND (tinh_tp_id IS NULL
                                        OR ao."TINH_TP_ID" = tinh_tp_id
                                   )
                                   AND (quan_huyen_id IS NULL
                                        OR ao."QUAN_HUYEN_ID" = quan_huyen_id
                                   )
                                   AND (phuong_xa_id IS NULL
                                        OR ao."XA_PHUONG_ID" = phuong_xa_id
                                   )
                                   AND (IL."LOAI_CHUNG_TU" = '2020'
                                        OR IL."LOAI_CHUNG_TU" = '2013'
                                   )
                             GROUP BY
                                 AO."TINH_TP_ID",
                                 AO."QUAN_HUYEN_ID",
                                 AO."XA_PHUONG_ID"
                            ) T
                        GROUP BY
                            T."TINH_TP_ID",
                            T."QUAN_HUYEN_ID",
                            T."XA_PHUONG_ID"
                ;

            END $$
            ;

            SELECT

                  TP."name"         AS "TINH_THANH_PHO"

                ,  QH."TEN_DAY_DU"      AS "QUAN_HUYEN"
                ,  XP."TEN_DAY_DU"       AS "XA_PHUONG"
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"

                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"


            FROM TMP_KET_QUA AS KQ
                LEFT JOIN res_country_state TP ON KQ."TINH_TP_ID" =TP.id
                LEFT JOIN res_country_state_district QH ON KQ."QUAN_HUYEN_ID" =QH.id
                LEFT JOIN res_country_state_district_ward XP ON KQ."XA_PHUONG_ID" =XP.id
            OFFSET %(offset)s
            LIMIT %(limit)s;
  
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_theo_don_vi_kinh_doanh(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                            DATE := %(DEN_NGAY)s;
            
                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
                don_vi_id                           INTEGER := %(DON_VI_ID)s ;
            
            
                rec                                 RECORD;
            
                MA_PHAN_CAP                         VARCHAR(100);
            
            
            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;
            
                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;
            
                DROP TABLE IF EXISTS DS_HANG_HOA
                ;
            
                CREATE TEMP TABLE DS_HANG_HOA
                    AS
                        SELECT *
                        FROM danh_muc_vat_tu_hang_hoa
                        WHERE (id = any (%(SAN_PHAMIDS)s))
                ;
            
                SELECT concat("MA_PHAN_CAP", '%%')
                INTO MA_PHAN_CAP
                FROM danh_muc_to_chuc
                WHERE "id" = don_vi_id
                ;
            
            
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY T."MA_DON_VI", T."TEN_DON_VI" ) AS RowNum
                            , T."DON_VI_ID"
                            , T."MA_DON_VI"
                            , T."TEN_DON_VI"
                            , SUM(T."DOANH_SO_BAN")                        AS "DOANH_SO_BAN"
                            , SUM(T."SO_TIEN_CHIET_KHAU")                  AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")                     AS "GIA_TRI_TRA_LAI"
                            , SUM(T."GIA_TRI_GIAM_GIA")                    AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI"
                                  - T."GIA_TRI_GIAM_GIA")                  AS "DOANH_THU_THUAN"
                            , SUM(T."GIA_VON")                             AS "GIA_VON"
                        FROM
                            (SELECT
                                 SL."DON_VI_ID"
                                 , OU."MA_DON_VI"
                                 , OU."TEN_DON_VI"
                                 , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                                 , -- Doanh số bán
                                   SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                 , -- Tiền chiết khấu
                                   SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                 , -- Giá trị trả lại
                                   SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                                 , -- Giá trị giảm giá
                                   0                            AS "GIA_VON"
                             FROM so_ban_hang_chi_tiet AS SL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN DS_HANG_HOA AS II ON SL."MA_HANG_ID" = II."id"
                                 INNER JOIN danh_muc_to_chuc OU ON OU."id" = SL."DON_VI_ID"
            
                             WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                   AND (don_vi_id IS NULL OR OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP)
                             GROUP BY
                                 SL."DON_VI_ID",
                                 OU."MA_DON_VI",
                                 OU."TEN_DON_VI"
            
                             UNION ALL
                             SELECT
                                 IL."DON_VI_ID"
                                 , OU."MA_DON_VI"
                                 , OU."TEN_DON_VI"
                                 , 0
                                 , 0
                                 , 0
                                 , 0
                                 , SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                             FROM so_kho_chi_tiet IL
                                 INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                 INNER JOIN DS_HANG_HOA AS II ON iL."MA_HANG_ID" = II."id"
                                 INNER JOIN danh_muc_to_chuc OU ON OU."id" = iL."DON_VI_ID"
                             WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
                                   AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                   AND (IL."LOAI_CHUNG_TU" = '2020'
                                        OR IL."LOAI_CHUNG_TU" = '2013'
                                   )
                                   AND (don_vi_id IS NULL OR OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP)
                             GROUP BY
                                 IL."DON_VI_ID",
                                 OU."MA_DON_VI",
                                 OU."TEN_DON_VI"
                            ) T
                        GROUP BY
                            T."DON_VI_ID",
                            T."MA_DON_VI",
                            T."TEN_DON_VI"
                        HAVING SUM(T."DOANH_SO_BAN") <> 0
                               OR SUM(T."SO_TIEN_CHIET_KHAU") <> 0
                               OR SUM(T."GIA_TRI_TRA_LAI") <> 0
                               OR SUM(T."GIA_TRI_TRA_LAI") <> 0
                               OR SUM(T."GIA_VON") <> 0
                ;
            
            END $$
            ;
            
            SELECT
            
                  "MA_DON_VI"          AS "MA_DON_VI"
            
                , "TEN_DON_VI"         AS "TEN_DON_VI"
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
            
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"
            
            
            FROM TMP_KET_QUA
            OFFSET %(offset)s
            LIMIT %(limit)s;
            

            

  
            """
        return self.execute(query,params_sql)


    def _lay_bao_cao_theo_don_vi_kinh_doanh_va_mat_hang(self, params_sql):      
        record = []
        query = """
            
                            DO LANGUAGE plpgsql $$
            DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                            DATE := %(DEN_NGAY)s;
            
                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
              
            
                don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;
            
            
                rec                                 RECORD;
            
                MA_PHAN_CAP                         VARCHAR(100);
            
            
            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;
            
                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;
            
                DROP TABLE IF EXISTS DS_HANG_HOA
                ;
            
                CREATE TEMP TABLE DS_HANG_HOA
                    AS
                        SELECT
                              II.id    AS "MA_HANG_ID"
                            , II."TEN" AS "TEN_HANG"
                            , II."TINH_CHAT"
                            , II."DVT_CHINH_ID"
                        FROM danh_muc_vat_tu_hang_hoa AS II
                        WHERE (id = any (%(SAN_PHAMIDS)s))
                ;
            
                DROP TABLE IF EXISTS TMP_DON_VI
                ;
            
                CREATE TEMP TABLE TMP_DON_VI
                    AS
                        SELECT
                            EI."id" AS "DON_VI_ID"
                            , EI."MA_PHAN_CAP"
                            , EI."MA_DON_VI"
                            , EI."TEN_DON_VI"
                            , EI."ISPARENT"
            
                            ,0 AS "IsParentWithChild"
                        FROM danh_muc_to_chuc AS EI
                        WHERE (id = any (%(DON_VI_IDS)s))
                ;
            
            
                UPDATE TMP_DON_VI
                SET "IsParentWithChild" = '1'
                FROM TMP_DON_VI T
                    INNER JOIN TMP_DON_VI T1
                        ON T1."MA_PHAN_CAP" LIKE concat(T."MA_PHAN_CAP", '%%') AND T."MA_PHAN_CAP" <> T1."MA_PHAN_CAP"
                WHERE T."ISPARENT" = '1'
                ;
            
            
                DROP TABLE IF EXISTS TMP_DON_VI_CHUYEN_DOI
                ;
            
                CREATE TEMP TABLE TMP_DON_VI_CHUYEN_DOI
                    AS
                        SELECT
                            IIUC."VAT_TU_HANG_HOA_ID"
                            , "DVT_ID"
                            , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
                            THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                               WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                                   THEN 1
                               ELSE 1
                                    / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                               END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                        FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                        WHERE IIUC."STT" = don_vi_tinh
                ;
            
            
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              ROW_NUMBER()
                              OVER (
                                  ORDER BY P."MA_DON_VI", T."MA_HANG" ) AS RowNum
                            , P."DON_VI_ID"
                            , P."MA_DON_VI"                             AS "MA_DON_VI"
                            , P."TEN_DON_VI"                            AS "TEN_DON_VI"
                            , T."MA_HANG_ID"
                            , T."MA_HANG"  -- Mã hàng
                            , T."TEN_HANG"  -- Tên hàng
                            , T."DON_VI_TINH_CHINH"
                            , T."DON_VI_TINH"
                            , SUM(T."SO_LUONG_BAN")                     AS "SO_LUONG_BAN"
                            , SUM(T."SO_LUONG_KHUYEN_MAI")              AS "SO_LUONG_KHUYEN_MAI"
                            , SUM(T."SO_LUONG_TRA_LAI")                 AS "SO_LUONG_TRA_LAI"
                            , SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI")      AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                            , SUM(T."DOANH_SO_BAN")                     AS "DOANH_SO_BAN"
                            , SUM(T."SO_TIEN_CHIET_KHAU")               AS "SO_TIEN_CHIET_KHAU"
                            , SUM(T."GIA_TRI_TRA_LAI")                  AS "GIA_TRI_TRA_LAI"
                            , SUM(COALESCE(T."GIA_TRI_GIAM_GIA", 0))    AS "GIA_TRI_GIAM_GIA"
                            , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - "GIA_TRI_TRA_LAI" -
                                  "GIA_TRI_GIAM_GIA")                   AS "DOANH_THU_THUAN"
                        FROM (SELECT
                                  OU."DON_VI_ID"
                                  , OU."MA_PHAN_CAP"
                                  , SL."MA_HANG_ID"
                                  , SL."MA_HANG"
                                  , -- Mã hàng
                                  LII."TEN_HANG"
            
            
                                  , UI."DON_VI_TINH"                        AS "DON_VI_TINH_CHINH"
                                  , CASE WHEN LII."DVT_CHINH_ID" IS NULL
                                THEN ''
                                    ELSE U."DON_VI_TINH"
                                    END                          AS "DON_VI_TINH"
            
                                  , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                                  , -- Doanh số bán
                                    SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                                  , -- Tiền chiết khấu
                                    SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                                  , -- Giá trị trả lại
                                    SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                                  , -- Giá trị giảm giá
                                    SUM(CASE WHEN U."id" IS NOT NULL
                                                  AND SL."DVT_ID" = U."id"
                                        THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN 0
                                             ELSE SL."SO_LUONG"
                                             END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN 0
                                             ELSE SL."SO_LUONG_THEO_DVT_CHINH"
                                                  * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                             END
                                        END)                     AS "SO_LUONG_BAN"
                                  , SUM(CASE WHEN U."id" IS NOT NULL
                                                  AND SL."DVT_ID" = U."id"
                                THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                    THEN SL."SO_LUONG"
                                     ELSE 0
                                     END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" ='1'
                                            THEN SL."SO_LUONG_THEO_DVT_CHINH"
                                                 * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                             ELSE 0
                                             END
                                        END)                     AS "SO_LUONG_KHUYEN_MAI"
                                  , SUM(CASE WHEN U."id" IS NOT NULL
                                                  AND SL."DVT_ID" = U."id"
                                THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                    THEN 0
                                     ELSE SL."SO_LUONG_TRA_LAI"
                                     END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN 0
                                             ELSE SL."SO_LUONG_THEO_DVT_CHINH"
                                                  * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                             END
                                        END)                     AS "SO_LUONG_TRA_LAI"
                                  , SUM(CASE WHEN U."id" IS NOT NULL
                                                  AND SL."DVT_ID" = U."id"
                                THEN CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                    THEN SL."SO_LUONG_TRA_LAI"
                                     ELSE 0
                                     END
                                        ELSE CASE WHEN SL."LA_HANG_KHUYEN_MAI" = '1'
                                            THEN SL."SO_LUONG_THEO_DVT_CHINH"
                                                 * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                             ELSE 0
                                             END
                                        END)                     AS "SO_LUONG_KHUYEN_MAI_TRA_LAI"
                                  , 0                            AS "GIA_VON"
                              FROM so_ban_hang_chi_tiet AS SL
                                  INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  INNER JOIN DS_HANG_HOA AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                                  INNER JOIN TMP_DON_VI OU ON SL."DON_VI_ID" = OU."DON_VI_ID"
                                  LEFT JOIN danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI."id"
                                  LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON LII."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                                  LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                                                                       AND U."id" = LII."DVT_CHINH_ID"
                                                                      )
                                                                      OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                                                          AND UC."DVT_ID" = U."id"
                                                                      )
                              WHERE (don_vi_tinh IS NULL
                                     OR don_vi_tinh = 0
                                     OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                    )
                                    AND SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
                              GROUP BY OU."DON_VI_ID",
                                  OU."MA_PHAN_CAP",
                                  SL."MA_HANG_ID",
                                  SL."MA_HANG", -- Mã hàng
                                  LII."TEN_HANG", -- Tên hàng
            
                                  UI."DON_VI_TINH",
                                  CASE WHEN LII."DVT_CHINH_ID" IS NULL
                                      THEN ''
                                  ELSE U."DON_VI_TINH"
                                  END
                              UNION ALL
                              SELECT
                                  OU."DON_VI_ID"
                                  , OU."MA_PHAN_CAP"
                                  , IL."MA_HANG_ID"
                                  , IL."MA_HANG"
                                  , -- Mã hàng
                                  LII."TEN_HANG"
            
                                  , UI."DON_VI_TINH"                               AS "DON_VI_TINH_CHINH"
                                  , CASE WHEN LII."DVT_CHINH_ID" IS NULL
                                  THEN ''
                                    ELSE U."DON_VI_TINH"
                                    END                                        AS "DON_VI_TINH"
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
                                  , 0
            
                                  , SUM(IL."SO_TIEN_XUAT" - IL."SO_TIEN_NHAP") AS "GIA_VON"
                              FROM so_kho_chi_tiet IL
                                  INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  INNER JOIN DS_HANG_HOA AS LII ON iL."MA_HANG_ID" = LII."MA_HANG_ID"
                                  INNER JOIN TMP_DON_VI OU ON IL."DON_VI_ID" = OU."DON_VI_ID"
                                  LEFT JOIN danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI."id"
                                  LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON LII."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                                  LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                                                                       AND U."id" = LII."DVT_CHINH_ID"
                                                                      )
                                                                      OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                                                          AND UC."DVT_ID" = U."id"
                                                                      )
                              WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
                                    AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                                    AND (IL."LOAI_CHUNG_TU" = '2020'
                                         OR IL."LOAI_CHUNG_TU" = '2013'
                                    )
                                    AND (don_vi_tinh IS NULL
                                         OR don_vi_tinh = 0
                                         OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                                    )
                              GROUP BY
                                  OU."DON_VI_ID",
                                  OU."MA_PHAN_CAP",
                                  IL."MA_HANG_ID",
                                  IL."MA_HANG", -- Mã hàng
                                  LII."TEN_HANG", -- Tên hàng
            
                                  UI."DON_VI_TINH",
                                  CASE WHEN LII."DVT_CHINH_ID" IS NULL
                                      THEN ''
                                  ELSE U."DON_VI_TINH"
                                  END
                              HAVING SUM(IL."SO_TIEN_XUAT" - IL."SO_TIEN_NHAP") <> 0
                             ) T
                            INNER JOIN TMP_DON_VI P ON
                                                        ((P."ISPARENT" = '0' OR P."ISPARENT" = '1'
                                                         ) AND T."DON_VI_ID" = P."DON_VI_ID"
                                                        )
                                                        OR (P."ISPARENT" = '1' AND P."IsParentWithChild" = '0' AND
                                                            T."MA_PHAN_CAP" LIKE concat(P."MA_PHAN_CAP" , '%%')
                                                        )
                        GROUP BY
                            P."DON_VI_ID",
                            P."MA_DON_VI",
                            P."TEN_DON_VI",
                            T."MA_HANG_ID",
                            T."MA_HANG", -- Mã hàng                ,
                            T."TEN_HANG", -- Tên hàng                ,
                            T."DON_VI_TINH_CHINH",
                            T."DON_VI_TINH"
            
                        HAVING
                            SUM(T."SO_LUONG_BAN"
                            ) <> 0 OR
                            SUM(T."SO_LUONG_KHUYEN_MAI"
                            ) <> 0 OR
                            SUM(T."SO_LUONG_TRA_LAI"
                            ) <> 0 OR
                            SUM(T."SO_LUONG_KHUYEN_MAI_TRA_LAI"
                            ) <> 0 OR
                            SUM(T."DOANH_SO_BAN"
                            ) <> 0 OR
                            SUM(T."SO_TIEN_CHIET_KHAU"
                            ) <> 0 OR
                            SUM(T."GIA_TRI_TRA_LAI"
                            ) <> 0 OR
                            SUM(T."GIA_TRI_GIAM_GIA"
                            ) <> 0 OR
                            SUM(T."GIA_VON"
                            ) <> 0
                ;
            
            END $$
            ;
            
            SELECT
            
                  "TEN_DON_VI"          AS "TEN_DON_VI"
            
                , "MA_HANG"         AS "MA_HANG"
                , "TEN_HANG"       AS "TEN_HANG"
                , "DON_VI_TINH_CHINH" AS "DVT"
                , "SO_LUONG_BAN"    AS "SO_LUONG_BAN"
                , "SO_LUONG_KHUYEN_MAI"   AS "SO_LUONG_KM"
                , "DOANH_SO_BAN"    AS "DOANH_SO_BAN"
            
                , "SO_TIEN_CHIET_KHAU"         AS "CHIET_KHAU"
                , "SO_LUONG_TRA_LAI"       AS "SO_LUONG_TRA_LAI"
                , "SO_LUONG_KHUYEN_MAI_TRA_LAI" AS "SO_LUONG_HANG_KM_TRA_LAI"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"
            
            
            FROM TMP_KET_QUA
            OFFSET %(offset)s
            LIMIT %(limit)s;
            
  
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_theo_nhom_khach_hang(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
            DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                            DATE := %(DEN_NGAY)s;
            
                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
               
            
                nhom_kh_khac_id                     INTEGER := -2;
            
                MA_PHAN_CAP_KHAC                      VARCHAR(100):= '/9999999/';
            
            
                rec                                 RECORD;
            
                MA_PHAN_CAP                         VARCHAR(100);
                IsIncludeOtherID                    INTEGER;
            
            
            BEGIN
                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;
            
                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;
            
                DROP TABLE IF EXISTS TMP_NHOM_KH_NCC
                ;
            
                CREATE TEMP TABLE TMP_NHOM_KH_NCC
                    AS
                        SELECT
                            EI.id AS "NHOM_KH_NCC_ID"
                            , EI."MA_PHAN_CAP"
                            , EI."MA"
                            , EI."TEN"
            
                        FROM danh_muc_nhom_khach_hang_nha_cung_cap AS EI
                        WHERE (id = any (%(NHOM_KHIDS)s)) 
                ;
            
                DROP TABLE IF EXISTS TMP_NHOM_KH_NCC_1
                ;
            
                CREATE TEMP TABLE TMP_NHOM_KH_NCC_1
                    AS
                        SELECT
                            S."NHOM_KH_NCC_ID"
                            , S."MA_PHAN_CAP"
                        FROM TMP_NHOM_KH_NCC S
                            LEFT JOIN TMP_NHOM_KH_NCC S1
                                ON S1."MA_PHAN_CAP" LIKE concat(S."MA_PHAN_CAP", '%%') AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                        WHERE S1."MA_PHAN_CAP" IS NULL
            
                ;
            
                 IF nhom_kh_khac_id = any (%(NHOM_KHIDS)s)  
                        THEN
                              IsIncludeOtherID = 1 ;
                            INSERT  INTO TMP_NHOM_KH_NCC
                                    SELECT
                                        nhom_kh_khac_id,
                                         MA_PHAN_CAP_KHAC ,
                                            N'<<Khác>>' ,
                                            N'<<Khác>>' ;
            
            
                  ELSE
                         IsIncludeOtherID =0;
                  END IF  ;
            
                DROP TABLE IF EXISTS TMP_LIST_NHOM_KH_NCC
                ;
            
                CREATE TEMP TABLE TMP_LIST_NHOM_KH_NCC
                    AS
                        SELECT DISTINCT
                            T.id
                            , T."MA_PHAN_CAP"
                        FROM (SELECT DISTINCT
                                  EI.id
                                  , EI."MA_PHAN_CAP"
                              FROM danh_muc_nhom_khach_hang_nha_cung_cap EI
                                  INNER JOIN TMP_NHOM_KH_NCC_1 SEI ON EI."MA_PHAN_CAP" LIKE concat(SEI."MA_PHAN_CAP", '%%')
                              UNION ALL
                              SELECT
                                  EI."NHOM_KH_NCC_ID"
                                  , EI."MA_PHAN_CAP"
                              FROM TMP_NHOM_KH_NCC EI
                             ) T
                ;
            
            
                DROP TABLE IF EXISTS TMP_BAC_NHOM_KH_NCC
                ;
            
                CREATE TEMP TABLE TMP_BAC_NHOM_KH_NCC
                    AS
                        SELECT
                            P."NHOM_KH_NCC_ID"
                            , COUNT(PD."MA_PHAN_CAP") Grade
                        FROM TMP_NHOM_KH_NCC P
                            LEFT JOIN TMP_NHOM_KH_NCC PD ON P."MA_PHAN_CAP" LIKE concat(PD."MA_PHAN_CAP", '%%')
                                                            AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                        GROUP BY P."NHOM_KH_NCC_ID"
                ;
            
                DROP TABLE IF EXISTS TMP_PARENT_NHOM_KH_NCC
                ;
            
                CREATE TEMP TABLE TMP_PARENT_NHOM_KH_NCC
                    AS
                        SELECT DISTINCT PD."NHOM_KH_NCC_ID"
                        FROM TMP_NHOM_KH_NCC P
                            LEFT JOIN TMP_NHOM_KH_NCC PD ON P."MA_PHAN_CAP" LIKE concat(PD."MA_PHAN_CAP", '%%')
                                                            AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                        WHERE PD."MA_PHAN_CAP" IS NOT NULL
                ;
            
            
                DROP TABLE IF EXISTS DS_KH_NCC
                ;
            
                CREATE TEMP TABLE DS_KH_NCC
                    AS
                        SELECT
                            AO.id
                            , AOG."MA_PHAN_CAP"
                        FROM res_partner AS AO
                                JOIN TMP_LIST_NHOM_KH_NCC AOG ON AO."LIST_MPC_NHOM_KH_NCC" LIKE  concat('%%;',AOG."MA_PHAN_CAP",';%%')
                    WHERE AO."LIST_MPC_NHOM_KH_NCC" IS NOT NULL
                    AND AO."LIST_MPC_NHOM_KH_NCC" <> ''
                    AND AO."LA_KHACH_HANG" = '1'
                ;
            
            
                IF 	IsIncludeOtherID = 1
                    THEN
                        INSERT INTO DS_KH_NCC
                                ( id, "MA_PHAN_CAP")
                        SELECT
                            id,
                            MA_PHAN_CAP_KHAC
                        FROM res_partner AS AO
                        WHERE (AO."LIST_MPC_NHOM_KH_NCC" IS NULL
                                OR AO."LIST_MPC_NHOM_KH_NCC" = ''
                            )
                            AND AO."LA_KHACH_HANG" = '1';
                END IF ;
            
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                              AO."MA_PHAN_CAP"             AS "MA_PHAN_CAP"
                            , SUM(SL."SO_TIEN")            AS "DOANH_SO_BAN"
                            , -- Doanh số bán
                              SUM(SL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU"
                            , -- Tiền chiết khấu
                              SUM(SL."SO_TIEN_TRA_LAI")    AS "GIA_TRI_TRA_LAI"
                            , -- Giá trị trả lại
                              SUM(SL."SO_TIEN_GIAM_TRU")   AS "GIA_TRI_GIAM_GIA"
                            , -- Giá trị giảm giá
                              0                            AS "GIA_VON"
                        FROM so_ban_hang_chi_tiet AS SL
                            INNER JOIN TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN DS_KH_NCC AO ON AO.id = SL."DOI_TUONG_ID"
                        WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
            
                        GROUP BY AO."MA_PHAN_CAP"
                        HAVING SUM(SL."SO_TIEN"
                               ) <> 0 -- Doanh số bán
                               OR SUM(SL."SO_TIEN_CHIET_KHAU"
                                  ) <> 0-- Tiền chiết khấu
                               OR SUM(SL."SO_TIEN_TRA_LAI"
                                  ) <> 0 -- Giá trị trả lại
                               OR SUM(SL."SO_TIEN_GIAM_TRU"
                                  ) <> 0 -- Giá trị giảm giá
            
                        -- Lấy giá vốn
                        UNION ALL
                        SELECT
                              AO."MA_PHAN_CAP"                     AS "MA_PHAN_CAP"
                            , 0
                            , 0
                            , 0
                            , 0
                            , SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                        FROM so_kho_chi_tiet IL
                            INNER JOIN TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN DS_KH_NCC AO ON AO.id = IL."DOI_TUONG_ID"
                        WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
                              AND IL."MA_TK_CO" LIKE '632%%' --- cứ phát sinh 632 là lấy
                              AND (IL."LOAI_CHUNG_TU" = '2020'
                                   OR IL."LOAI_CHUNG_TU" = '2013'
                              )
                        GROUP BY AO."MA_PHAN_CAP"
                ;
            
            
                ---------------------------------------------------------
             DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                    AS
                SELECT
                    --           ROW_NUMBER()
                    --           OVER (
                    --               ORDER BY P.SortMISACodeID )                                                                      AS RowNum
                    P."NHOM_KH_NCC_ID"
                   ,concat(repeat(' ',cast(GP.Grade * 6 as int)),P."MA")      as "MA_NHOM_KH"
                   ,concat(repeat(' ',cast(GP.Grade * 6 as int)),P."TEN")                                                          AS "TEN_NHOM_KH"
            
                    , SUM(
                          T."DOANH_SO_BAN")                                                                       AS "DOANH_SO_BAN"
                    , SUM(
                          T."SO_TIEN_CHIET_KHAU")                                                                 AS "SO_TIEN_CHIET_KHAU"
                    , SUM(
                          T."GIA_TRI_TRA_LAI")                                                                    AS "GIA_TRI_TRA_LAI"
                    , SUM(
                          T."GIA_TRI_GIAM_GIA")                                                                   AS "GIA_TRI_GIAM_GIA"
                    , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA") AS
                                                                                                                     "DOANH_THU_THUAN"
                    , SUM(
                          T."GIA_VON")                                                                            AS "GIA_VON"
                    , SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" -
                          T."GIA_VON")                                                                            AS "LAI_GOP"
                    , (CASE WHEN
                    SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA") > 0
                    AND SUM(
                            T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" - T."GIA_VON") >
                        0
                    OR SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA") < 0 AND
                       SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" -
                           T."GIA_VON") < 0
                    THEN SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" - T."GIA_VON") *
                         100
                         / SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA")
                       ELSE 0
                       END)                                                                                       AS "TY_LE_LAI_GOP"
                FROM TMP_KET_QUA AS T
                    INNER JOIN TMP_NHOM_KH_NCC P ON T."MA_PHAN_CAP" LIKE concat(P."MA_PHAN_CAP", '%%')
                    LEFT JOIN TMP_PARENT_NHOM_KH_NCC PP ON PP."NHOM_KH_NCC_ID" = P."NHOM_KH_NCC_ID"
                    LEFT JOIN TMP_BAC_NHOM_KH_NCC GP ON GP."NHOM_KH_NCC_ID" = P."NHOM_KH_NCC_ID"
                GROUP BY
                    --P.SortMISACodeID,
                    P."NHOM_KH_NCC_ID",
                    P."MA_PHAN_CAP",
            
                   concat(repeat(' ',cast(GP.Grade * 6 as int)),P."MA"),
                   concat(repeat(' ',cast(GP.Grade * 6 as int)),P."TEN")
            
                HAVING SUM(T."DOANH_SO_BAN") <> 0
                       OR SUM(T."SO_TIEN_CHIET_KHAU") <> 0
                       OR SUM(T."GIA_TRI_TRA_LAI") <> 0
                       OR SUM(T."GIA_TRI_GIAM_GIA") <> 0
                       OR SUM(T."GIA_VON") <> 0
                ;
            
            END $$
            ;
            
            SELECT
            
                  "MA_NHOM_KH"         AS "MA_NHOM_KH"
            
                , "TEN_NHOM_KH"        AS "TEN_NHOM_KH"
            
                , "DOANH_SO_BAN"       AS "DOANH_SO_BAN"
            
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
            
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "DOANH_THU_THUAN"    AS "DOANH_THU_THUAN"
                , "GIA_VON"            AS "TIEN_VON"
                , "LAI_GOP"            AS "LAI_GOP"
                , "TY_LE_LAI_GOP"      AS "TY_LE_LAI_GOP"
            
            
            FROM TMP_KET_QUA_CUOI_CUNG
            OFFSET %(offset)s
            LIMIT %(limit)s;
            



            """
        return self.execute(query,params_sql)

    




    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = ' Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        if THONG_KE_THEO=='MAT_HANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_mathang').read()[0]
        elif THONG_KE_THEO=='MAT_HANG_KHACH_HANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_mathang_khachhang').read()[0]
        elif THONG_KE_THEO=='MAT_HANG_NHAN_VIEN':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_mathang_nhanvien').read()[0]
        elif THONG_KE_THEO=='KHACH_HANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_KhachHang').read()[0]
        elif THONG_KE_THEO=='NHAN_VIEN':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_nhanvien').read()[0]
        elif THONG_KE_THEO=='NHAN_VIEN_VA_KHACH_HANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_nhanvienvakh').read()[0]
        elif THONG_KE_THEO=='NHAN_VIEN_KHACH_HANG_MATHANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_nhanvien_kh_mh').read()[0]
        elif THONG_KE_THEO=='DIA_PHUONG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_diaphuong').read()[0]
        elif THONG_KE_THEO=='DON_VI_KINH_DOANH':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_donvikinhdoanh').read()[0]
        elif THONG_KE_THEO=='DON_VI_KINH_DOANH_VA_MAT_HANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_donvikinhdoanh_mh').read()[0]
        elif THONG_KE_THEO=='NHOM_KHACH_HANG':
            action = self.env.ref('bao_cao.open_report_tong_hop_ban_hang_nhomkh').read()[0]
        
        
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action