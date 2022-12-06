# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class DANH_MUC_DOI_TUONG(models.Model):
    _inherit = 'res.partner'
    _order = "HO_VA_TEN"
	
    name = fields.Char(string='name', help='name',related='MA',store=True)
    # Copy từ danh_muc_res_partner, trường này sau sẽ bỏ
    MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='Mã đối tượng')
    LOAI_KHACH_HANG = fields.Selection([('0', 'Tổ chức'), ('1', 'Cá nhân'), ], string='Là tổ chức/cá nhân', help='Loại khách hàng',default='0')
    MA = fields.Char(string='Mã', help='Mã',store=True,compute='_compute_MA')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị (*)', help='Đơn vị')
    TEN_DON_VI = fields.Char('Tên đơn vị', related='DON_VI_ID.TEN_DON_VI', )
    GIOI_TINH = fields.Selection([('0', 'Nam'), ('1', 'Nữ'), ], string='Giới tính', help='Giới tính',default='0')
    NGAY_SINH = fields.Date(string='Ngày sinh', help='Ngày sinh')
    LA_KHACH_HANG = fields.Boolean(string='Là khách hàng', help='Khách hàng')
    LA_NHAN_VIEN = fields.Boolean(string='Là nhân viên', help='Là nhân viên')
    LUONG_THOA_THUAN = fields.Float(string='Lương thỏa thuận', help='Lương thỏa thuận',digits=decimal_precision.get_precision('Product Price'))
    HE_SO_LUONG = fields.Float(string='Hệ số lương', help='Hệ số lương', digits=decimal_precision.get_precision('SO_LUONG'))
    LUONG_DONG_GOP_BH = fields.Float(string='Lương đóng BH', help='Lương đóng bảo hiểm',digits=decimal_precision.get_precision('Product Price'))
    SO_NGUOI_PHU_THUOC = fields.Integer(string='Số người phụ thuộc', help='Số người phụ thuộc')
    XUNG_HO = fields.Selection([('ONG', 'Ông'), ('BA', 'Bà'), ('ANH', 'Anh'), ('CHI', 'Chị'), ('BAN', 'Bạn'), ('MR', 'Mr'), ('MRS', 'Mrs'), ('MISS', 'Miss'), ], string='Xưng hô', help='Xưng hô')
    HO_VA_TEN = fields.Char(string='Họ và tên (*)', help='Họ và tên')
    DIA_CHI = fields.Text(string='Địa chỉ', help='Địa chỉ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NHOM_KH_NCC_ID = fields.Many2many('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH, NCC', help='Nhóm kh ncc')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DT_DI_DONG = fields.Char(string='Điện thoại di động', help='Điện thoại di động')
    EMAIL = fields.Char(string='Email', help='Email')
    SO_CMND = fields.Char(string='Số CMND', help='Số chứng minh nhân dân')
    NGAY_CAP = fields.Date(string='Ngày cấp', help='Ngày cấp')
    NOI_CAP = fields.Char(string='Nơi cấp', help='Nơi cấp')
    DIEU_KHOAN_TT_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản tt', help='Điều khoản tt')
    SO_NGAY_DUOC_NO = fields.Integer(string='Số ngày được nợ', help='Số ngày được nợ')
    SO_NO_TOI_DA = fields.Float(string='Số nợ tối đa', help='Số nợ tối đa',digits=decimal_precision.get_precision('Product Price'))
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nv bán hàng', help='Nv bán hàng', default=lambda self: self.env.user.partner_id.id)
    DIEN_THOAI = fields.Char(string='Điện thoại', help='Điện thoại')
    FAX = fields.Char(string='Fax', help='Fax')
    WEBSITE = fields.Char(string='Website', help='Website')
    LA_NHA_CUNG_CAP = fields.Boolean(string='Là nhà cung cấp', help='Nhà cung cấp')
    QUOC_GIA_ID = fields.Many2one('res.country', string='Quốc gia', help='Quốc gia')
    QUAN_HUYEN_ID = fields.Many2one('res.country.state.district', string='Quận huyện', help='Quận huyện')
    TINH_TP_ID = fields.Many2one('res.country.state', string='Tỉnh tp', help='Tỉnh tp')
    XA_PHUONG_ID = fields.Many2one('res.country.state.district.ward', string='Xã phường', help='Xã phường')
    CHUC_DANH = fields.Char(string='Chức danh liên hệ', help='Chức danh liên hệ')
    DTDD_KHAC = fields.Char(string='Ddtddd khác', help='Ddtddd khác')
    DAI_DIEN_THEO_PL = fields.Char(string='Đại diện theo pl', help='Đại diện theo pl')
    TEN_NGUOI_NHAN = fields.Char(string='Tên người nhận', help='Tên người nhận')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1541
    MA_NHA_CUNG_CAP = fields.Char(string='Mã nhà cung cấp (*)', help='Mã nhà cung cấp', auto_num='danh_muc_doi_tuong_MA_NHA_CUNG_CAP')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên (*)', help='Mã nhân viên', auto_num='danh_muc_doi_tuong_MA_NHAN_VIEN')
    MA_KHACH_HANG = fields.Char(string='Mã khách hàng (*)', help='Mã khách hàng', auto_num='danh_muc_doi_tuong_MA_KHACH_HANG')
    HO_VA_TEN_LIEN_HE = fields.Char(string='Họ và tên liên hệ', help='Họ và tên liên hệ')
    DIA_CHI_LIEN_HE = fields.Text(string='Địa chỉ liên hệ', help='Địa chỉ liên hệ')
    DT_CO_DINH_LIEN_HE = fields.Char(string='ĐT cố định liên hệ', help='Điện thoại cố định liên hệ')
    EMAIL_LIEN_HE = fields.Char(string='Email thông tin liên hệ', help='Email thông tin liên hệ')
    DT_DI_DONG_LIEN_HE = fields.Char(string='ĐT di động liên hệ', help='ĐT di động liên hệ')
    DTDD_KHAC_LIEN_HE = fields.Char(string='ĐT di động khác liên hệ', help='ĐT di động khác liên hệ')
    DIA_CHI_NGUOI_NHAN = fields.Char(string='Địa chỉ người nhận', help='Địa chỉ người nhận')
    DT_NGUOI_NHAN = fields.Char(string='Điện thoại người nhận', help='Điện thoại người nhận')
    EMAIL_NGUOI_NHAN = fields.Char(string='Email người nhận', help='Email người nhận')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    # # Tùng comment trường này vì đã có là nhân viên, là nhà cung cấp, là khách hàng phân biệt (đã search và bỏ những chỗ dùng)
    KIEU_DOI_TUONG = fields.Selection([('KHACH_HANG', 'Khách hàng'), ('NHAN_VIEN', 'Nhân viên'),('NHA_CC', 'Nhà cung cấp'), ], string='Loại đối tượng', help='Loại đối tượng')
    LIST_TEN_NHOM_KH_NCC = fields.Char(string='List tên nhóm khách hàng, ncc', help='List tên nhóm khách hàng, ncc', compute='_compute_list', store=True)
    LIST_MPC_NHOM_KH_NCC = fields.Char(string='List mã phân cấp ên nhóm khách hàng, ncc', help='List mã phân cấp nhóm khách hàng, ncc', compute='_compute_list', store=True)
    DANH_MUC_DOI_TUONG_CHI_TIET_IDS = fields.One2many('danh.muc.doi.tuong.chi.tiet', 'DOI_TUONG_ID', string='Đối tượng chi tiết', copy=True)
    DANH_MUC_DOI_TUONG_DIA_DIEM_GIAO_HANG_IDS = fields.One2many('danh.muc.doi.tuong.dia.diem.giao.hang', 'DOI_TUONG_ID', string='Đối tượng Địa điểm giao hàng', copy=True)  
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    LIST_MA_NHOM_KH_NCC = fields.Char(string='List mã nhóm khách hàng, ncc', help='List mã nhóm khách hàng, ncc', compute='_compute_list', store=True)

    # vũ thêm cột này để làm báo cáo
    TEN_CHI_NHANH_NGAN_HANG = fields.Char(string='Tên chi nhánh ngân hàng', help='Tên chi nhánh ngân hàng')
    DIA_DIEM_GIAO_HANG_STRING = fields.Char(string='Địa điểm giao hàng', help='Địa điểm giao hàng')
    
    _sql_constraints = [
        ('MA_uniq', 'unique ("MA")', 'Mã đối tượng <<>> đã tồn tại!'),
    ]

    @api.depends('MA_NHA_CUNG_CAP','MA_NHAN_VIEN','MA_KHACH_HANG','LA_KHACH_HANG','LA_NHAN_VIEN','LA_NHA_CUNG_CAP')
    def _compute_MA(self):
        for record in self:
            if record.LA_NHAN_VIEN == True :
                record.MA = record.MA_NHAN_VIEN
            elif record.LA_KHACH_HANG == True:
                if record.MA_KHACH_HANG:
                    record.MA = record.MA_KHACH_HANG
                else:# https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2011
                    record.MA = record.MA_NHA_CUNG_CAP 
            elif record.LA_NHA_CUNG_CAP == True:
                record.MA = record.MA_NHA_CUNG_CAP   
            else:
                record.MA = record.MA_NHAN_VIEN or record.MA_KHACH_HANG or record.MA_NHA_CUNG_CAP

    @api.model
    def create(self, values):
        # TH import từ excel
        if self.env.context.get('import_file'):
            if values.get('MA_NHAN_VIEN'):
                values['LA_NHAN_VIEN'] = True
            elif values.get('MA_KHACH_HANG'):
                values['LA_KHACH_HANG'] = True
            elif values.get('MA_NHA_CUNG_CAP'):
                values['LA_NHA_CUNG_CAP'] = True
        if values.get('LA_NHAN_VIEN') and values.get('MA_NHAN_VIEN'):
            values['MA_KHACH_HANG'] = None
            values['MA_NHA_CUNG_CAP'] = None
        elif values.get('LA_KHACH_HANG') and values.get('MA_KHACH_HANG'):
            values['MA_NHA_CUNG_CAP'] = None
            values['MA_NHAN_VIEN'] = None
        elif values.get('LA_NHA_CUNG_CAP') and values.get('MA_NHA_CUNG_CAP'):
            values['MA_NHAN_VIEN'] = None
            values['MA_KHACH_HANG'] = None
        return super(DANH_MUC_DOI_TUONG, self).create(values)
    
    # @api.onchange('NHOM_KH_NCC_ID')
    # def _onchange_NHOM_KH_NCC_ID(self):
    @api.depends('NHOM_KH_NCC_ID')
    def _compute_list(self):
        for record in self:
            record.LIST_TEN_NHOM_KH_NCC = record.lay_nhom_kh_ncc()
            record.LIST_MPC_NHOM_KH_NCC = record.lay_ma_pc_nhom_kh_ncc()
            record.LIST_MA_NHOM_KH_NCC = record.lay_ma_nhom_kh_ncc()

    def lay_nhom_kh_ncc(self):
        nhom_khach_hang = ''
        if self.NHOM_KH_NCC_ID:
            for line in self.NHOM_KH_NCC_ID:
                if nhom_khach_hang == '':
                    nhom_khach_hang = line.TEN
                else:
                    nhom_khach_hang += "; " + line.TEN
        return nhom_khach_hang

    def lay_ma_nhom_kh_ncc(self):
        ma_nhom_khach_hang = ''
        if self.NHOM_KH_NCC_ID:
            for line in self.NHOM_KH_NCC_ID:
                if ma_nhom_khach_hang == '':
                    ma_nhom_khach_hang = line.MA
                else:
                    ma_nhom_khach_hang += "; " + line.MA
        return ma_nhom_khach_hang

    def lay_ma_pc_nhom_kh_ncc(self):
        ma_pc_nhom_khach_hang = ''
        if self.NHOM_KH_NCC_ID:
            for line in self.NHOM_KH_NCC_ID:
                # if ma_pc_nhom_khach_hang == '':
                #     ma_pc_nhom_khach_hang = line.MA_PHAN_CAP
                # else:
                #     ma_pc_nhom_khach_hang += ";" + line.MA_PHAN_CAP
                ma_pc_nhom_khach_hang += ";" + line.MA_PHAN_CAP
            ma_pc_nhom_khach_hang += ";"
        return ma_pc_nhom_khach_hang
