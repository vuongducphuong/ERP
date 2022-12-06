# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED


	# - Xuất kho
	# 	○ Bán hàng
	# 		§ Đơn giá = DON_GIA_VON
	# 		§ Thành tiền = TIEN_VON
	# 	○ Sản xuất
	# 		§ Đơn giá = DON_GIA_VON
	# 		§ Thành tiền = TIEN_VON
	# 	○ Xuất hàng cho chi nhánh khác
	# 		§ Đơn giá bán = DON_GIA
	# 		§ Thành tiền = THANH_TIEN
	# 		§ Đơn giá vốn = DON_GIA_VON
	# 		§ Tiền vốn = TIEN_VON
	# 	○ Khác
	# 		§ Đơn giá = DON_GIA_VON
	# 		§ Thành tiền = TIEN_VON
	# - Nhập kho
	# 	○ Đơn giá = DON_GIA_VON
	# 	○ Thành tiền = TIEN_VON
	# - Chuyển kho
	# 	○ Xuất kho kiêm vận chuyển nội bộ and Xuất kho gửi bán đại lý
	# 		§ Đơn giá bán = DON_GIA
	# 		§ Thành tiền = THANH_TIEN
	# 		§ Đơn giá vốn = DON_GIA_VON
	# 		§ Tiền vốn = TIEN_VON
	# 	○ Xuất kho chuyển nội bộ
	# 		§ Đơn giá = DON_GIA_VON
    #         Thành tiền = TIEN_VON

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
import json

class STOCK_EX_NHAP_XUAT_KHO(models.Model):
    _name = 'stock.ex.nhap.xuat.kho'
    _description = 'Phiếu nhập/xuất kho'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, id desc"

    @api.depends('CHI_TIET_IDS.TIEN_VON')
    def tinhtongtien(self):
        for order in self:
            tongtien = 0.0
            for line in order.CHI_TIET_IDS:
                tongtien += line.TIEN_VON
                
            order.update({
                'TONG_TIEN': tongtien,
            })

    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_KHO_ID = fields.Many2one('so.kho', ondelete='set null')
    name = fields.Char(string='Số phiếu',store=True , compute='lay_thong_tin_so_chung_tu')
    type = fields.Selection([('NHAP_KHO', 'Nhập kho'), ('XUAT_KHO', 'Xuất kho'), ('CHUYEN_KHO', 'Chuyển kho')], string='Loại chuyển kho', required=True)
    LOAI_NHAP_KHO = fields.Selection([('THANH_PHAM', '1.Thành phẩm sản xuất'), ('TRA_LAI', '2. Hàng bán bị trả lại'), ('KHAC', '3. Khác (NVL thừa, HH thuê gia công...)'), ], string='Loại nhập kho', help='Loại nhập kho',default='TRA_LAI',required=True)
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng',related='TEN_NGUOI_GIAO_HANG')
    NGUOI_GIAO_HANG_TEXT = fields.Char(string='Người giao hàng text', help='Người giao hàng text')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    KEM_THEO_CHUNG_TU_GOC = fields.Char(string='Kèm theo chứng từ gốc', help='Kèm theo chứng từ gốc')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGUOI_GIAO_HANG_ID = fields.Many2one('res.partner', string='Người giao hàng', help='Người giao hàng',related='DOI_TUONG_ID')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên bán hàng', help='Nhân viên bán hàng')
    TEN_NGUOI_GIAO_HANG = fields.Char(string='Tên người giao hàng', help='Tên người giao hàng')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng',related='TEN_NGUOI_GIAO_HANG')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ ',default=fields.Datetime.now,required=True)
    LOAI_XUAT_KHO = fields.Selection([('BAN_HANG', '1. Bán hàng'), ('SAN_XUAT', '2. Sản xuất'), ('XUAT_HANG', '3. Xuất hàng cho chi nhánh khác'), ('KHAC', '4. Khác (Xuất sử dụng, góp vốn,...)'), ], string='Loại xuất kho', help='Loại xuất kho',default='BAN_HANG',required=True)
    TEN_NGUOI_NHAN = fields.Char(string='Tên người nhận', help='Tên người nhận',related='TEN_KHACH_HANG')
    BO_PHAN = fields.Char(string='Bộ phận', help='Bộ phận')
    LY_DO_XUAT = fields.Char(string='Lý do xuất', help='Lý do xuất',related='DIEN_GIAI')
    NGUOI_NHAN_TEXT = fields.Char(string='Người nhận text', help='Người nhận text') 
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    LENH_DIEU_DONG_SO = fields.Char(string='Lệnh điều động số', help='Lệnh điều động số')
    HOP_DONG_KT_SO = fields.Char(string='Hợp đồng KT số', help='Hợp đồng KT số')
    NGAY = fields.Date(string='Ngày', help='Ngày')
    CUA = fields.Char(string='Của', help='Của')
    VE_VIEC = fields.Char(string='Về việc', help='Về việc',related='DIEN_GIAI')
    NGUOI_VAN_CHUYEN_ID = fields.Many2one('res.partner', string='Người vận chuyển', help='Người vận chuyển')
    TEN_NGUOI_VAN_CHUYEN = fields.Char(string='Tên người vận chuyển', help='Tên người vận chuyển')
    HOP_DONG_SO = fields.Char(string='Hợp đồng số', help='Hợp đồng số')
    PHUONG_TIEN = fields.Selection([('O_TO', 'Ô tô'), ('MAY_BAY', 'Máy bay'), ('TAU_HOA', ' Tàu hỏa'), ('GIAO_TAY', 'Giao tay'), ], string='Phương tiện', help='Phương tiện')
    XUAT_TAI_KHO_ID = fields.Many2one('danh.muc.kho', string='Xuất tại kho', help='Xuất tại kho')
    NHAP_TAI_KHO_ID = fields.Many2one('danh.muc.kho', string='Nhập tại kho', help='Nhập tại kho')
    DIA_DIEM_GIAO_HANG_ID = fields.Char(string='Địa điểm giao hàng', help='Địa điểm giao hàng')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    MAU_SO = fields.Char(string='Mẫu số', help='Mẫu số')
    KY_HIEU = fields.Char(string='Ký hiệu', help='Ký hiệu')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    IN_KEM_BANG_KE = fields.Boolean(string='In kèm bảng kê', help='In kèm bảng kê')
    SO = fields.Char(string='Số', help='Số')
    TEN_MAT_HANG_CHUNG = fields.Char(string='Tên mặt hàng chúng', help='Tên mặt hàng chúng')

    DA_LAP_CT_BAN_HANG=fields.Char(string='đã lập chứng từ bán hàng,help')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',store=True,compute='set_loai_chung_tu_nhap_xuat_kho') 
    SO_CHUNG_TU_QT=fields.Char(string='Sổ chứng từ(Sổ QT)',help='sổ chứng từ') 
    CHI_NHANH = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')
    TONG_TIEN = fields.Float(string='Tổng tiền', help='Tổng tiền ',compute='tinhtongtien', store=True,digits=decimal_precision.get_precision('Product Price'))
    LOAI_CHUNG_TU_2=fields.Integer( string='Loại chứng từ',help='Loại chứng từ')
    NGAY_CK = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    LAP_RAP_THAO_DO_ID = fields.Many2one('stock.ex.lap.rap.thao.do', string='id Lắp ráp tháo dỡ', help='id Lắp ráp tháo dỡ', ondelete='cascade')

    LA_PHIEU_NHAP_HANG_TRA_LAI = fields.Boolean(string='Là phiếu nhập chọn hàng trả lại', help='Là phiếu nhập chọn hàng trả lại')
    LA_PHIEU_XUAT_BAN_HANG = fields.Boolean(string='Là phiếu xuất chứng từ bán hàng', help='Là phiếu xuất bán hàng')
    NGAY_HACH_TOAN_CK = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',default=fields.Datetime.now)
    NGAY_CHUNG_TU_CK = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ ',default=fields.Datetime.now)
    NGAY_GHI_SO_CK= fields.Date(string='Ngày ghi sổ kho', help='Ngày ghi sổ kho')
    TONG_TIEN_CK=fields.Float(string='Tổng tiền',help='Tổng tiền chuyển kho',digits=decimal_precision.get_precision('Product Price'))
    TONG_TIEN_HANG = fields.Float(string='Tổng tiền hàng', help='Tổng tiền hàng',compute='tinh_tong_tien')
    PHUONG_THUC_TINH_DON_GIA_NHAP = fields.Selection([('0', 'Lấy từ giá xuất bán'), ('1', 'Nhập đơn giá bằng tay')], string='UnitPriceMethod')
    TONG_DON_GIA_VON = fields.Float(string='Tổng đơn giá vốn', help='Tổng đơn giá vốn')
    
    LOAI_CK=fields.Char( string='Loại chuyển kho',help='Loại chuyển kho')
    SO_KHAC = fields.Char(string='Số khác', help='Số khác', auto_num='nhap_kho_SO_KHAC')    
    CHI_TIET_IDS = fields.One2many('stock.ex.nhap.xuat.kho.chi.tiet', 'NHAP_XUAT_ID', copy=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

    TRANG_THAI_DOANH_THU = fields.Integer(string='Trạng thái doanh thu', help='Trạng thái doanh thu') #https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2004
    LAP_TU_LENH_SAN_XUAT_PHIEU_XUAT = fields.Boolean(string='chứng từ lập từ lệnh sản xuất phiếu xuất', help='chứng từ lập từ lệnh sản xuất phiếu xuất',store=False,default=False ) 

    SO_CHUNG_TU_CK_READONLY = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_CHUYEN_KHO')
    chi_tiet = fields.Selection([
        ('hang_tien', 'Hàng tiền'),
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')

    
    chi_tiet2 = fields.Selection([
        ('hang_tien', 'Hàng tiền'),
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')

    loai_chuyen_kho = fields.Selection([
        ('van_chuyen', 'Xuất kho kiêm vận chuyển'),
        ('gui_ban','Xuất kho gửi bán đại lý'),
        ('chuyen_kho','Xuất chuyển kho nội bộ'),
        ], default='van_chuyen')

    DIEU_CHINH_GIA_TRI = fields.Boolean(string='Điều chỉnh giá trị', help='Điều chỉnh giá trị')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    SOURCE_ID = fields.Reference(selection=[], string='Lập từ')
    SO_CHUNG_TU_TU_TANG_JSON = fields.Char(store=False)

    LOAI_CHUNG_TU_TEXT=fields.Char(string='Loại chứng từ',compute='set_loai_chung_tu_text',store=True)

    # CHON_LAP_TU_ID = fields.Reference(selection=[('sale.document', 'Bán hàng'),
    #                                                     ('stock.ex.lenh.san.xuat', 'Lệnh sản xuất')], string='Lập từ')

    LAP_TU_BAN_HANG = fields.Many2one('sale.document', string='Lập từ bán hàng') #Mạnh làm task 2474
    LAP_TU_LENH_SAN_XUAT = fields.Many2one('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham', string='Lập từ lệnh sản xuất') #Mạnh làm task 2474

    LAP_TU_HANG_BAN_TRA_LAI = fields.Many2one('sale.ex.tra.lai.hang.ban', string='Lập từ CT hàng bán trả lại') #Mạnh làm task 2536
    KIEM_TRA_PHIEU_NHAP_KHO = fields.Boolean(string='Kiêm phiếu nhập kho', help='Kiêm phiếu nhập kho', default='True')
    KIEM_PHIEU_NHAP_XUAT_KHO = fields.Boolean(string='Kiêm phiếu nhập xuất kho', help='Kiêm phiếu nhập xuất kho',default='True')
    STT_NHAP_CHUNG_TU = fields.Integer(string='Số thứ tự nhập chứng từ', help='Số thứ tự nhập chứng từ') 

    @api.onchange('LAP_TU_BAN_HANG')
    def update_chi_tiet_tu_CTBH(self):
        if self.LAP_TU_BAN_HANG:
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            self.CHI_TIET_IDS  = []
            for line in self.LAP_TU_BAN_HANG.SALE_DOCUMENT_LINE_IDS:
                new_line = default.copy()
                new_line.update({
                    'MA_HANG_ID': line.MA_HANG_ID.id,
                    'TEN_HANG': line.TEN_HANG,
                    'DVT_ID': line.DVT_ID.id,
                    'KHO_ID': line.KHO_ID.id,
                    'DON_VI_ID': line.DON_VI_ID.id,
                    'SO_LUONG': line.SO_LUONG,
                    'DON_GIA_VON': line.DON_GIA,
                    'THANH_TIEN': line.THANH_TIEN,
                    'DON_DAT_HANG_ID' : line.DON_DAT_HANG_ID.id,
                    'DON_DAT_HANG_CHI_TIET_ID' : line.DON_DAT_HANG_CHI_TIET_ID.id,
                    'TK_CO_ID': new_line.get('TK_CO_ID') or line.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                })
                self.CHI_TIET_IDS += self.env['stock.ex.nhap.xuat.kho.chi.tiet'].new(new_line)
            self.DOI_TUONG_ID = self.LAP_TU_BAN_HANG.DOI_TUONG_ID.id
            self.TEN_KHACH_HANG = self.LAP_TU_BAN_HANG.TEN_KHACH_HANG
            self.NGUOI_NHAN_TEXT = self.LAP_TU_BAN_HANG.NGUOI_LIEN_HE
            self.DIA_CHI = self.LAP_TU_BAN_HANG.DIA_CHI
            if self.TEN_KHACH_HANG:
                self.LY_DO_XUAT = ' '.join(('Xuất kho bán hàng',self.TEN_KHACH_HANG))

    @api.onchange('LAP_TU_LENH_SAN_XUAT')
    def update_chi_tiet_tu_LSX(self):
        if self.LAP_TU_LENH_SAN_XUAT:
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            self.CHI_TIET_IDS  = []
            if self.type == 'XUAT_KHO':
                self.LY_DO_XUAT = ' '.join(('Xuất kho NVL sản xuất theo Lệnh sản xuất',self.LAP_TU_LENH_SAN_XUAT.SO))
                for line in self.LAP_TU_LENH_SAN_XUAT.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS:
                    new_line = default.copy()
                    new_line.update({
                        'MA_HANG_ID': line.MA_HANG_ID.id,
                        'TEN_HANG': line.TEN_NGUYEN_VAT_LIEU,
                        'DVT_ID': line.DVT_ID.id,
                        'KHO_ID': line.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                        'SO_LUONG': line.SO_LUONG_NVL,
                        'LENH_SAN_XUAT_VIEW_ID': self.LAP_TU_LENH_SAN_XUAT.name,
                        'THANH_PHAM_ID': self.LAP_TU_LENH_SAN_XUAT.id,
                        'TK_CO_ID': new_line.get('TK_CO_ID') or line.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                    })
                    self.CHI_TIET_IDS += self.env['stock.ex.nhap.xuat.kho.chi.tiet'].new(new_line)
            elif self.type == 'NHAP_KHO':
                self.DIEN_GIAI = ' '.join(('Nhập kho thành phẩm sản xuất từ Lệnh sản xuất',self.LAP_TU_LENH_SAN_XUAT.SO))
                new_line = default.copy()
                new_line.update({
                    'MA_HANG_ID': self.LAP_TU_LENH_SAN_XUAT.MA_HANG_ID.id,
                    'TEN_HANG': self.LAP_TU_LENH_SAN_XUAT.TEN_THANH_PHAM,
                    'DVT_ID': self.LAP_TU_LENH_SAN_XUAT.DVT_ID.id,
                    'KHO_ID': self.LAP_TU_LENH_SAN_XUAT.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                    'SO_LUONG': self.LAP_TU_LENH_SAN_XUAT.SO_LUONG,
                    'TK_NO_ID': new_line.get('TK_NO_ID') or self.LAP_TU_LENH_SAN_XUAT.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                    'LENH_SAN_XUAT_ID': self.LAP_TU_LENH_SAN_XUAT.LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.id,
                })
                self.CHI_TIET_IDS += self.env['stock.ex.nhap.xuat.kho.chi.tiet'].new(new_line)

    @api.onchange('LAP_TU_HANG_BAN_TRA_LAI')
    def update_chi_tiet_tu_TLHB(self):
        if self.LAP_TU_HANG_BAN_TRA_LAI:
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            self.CHI_TIET_IDS  = []
            for line in self.LAP_TU_HANG_BAN_TRA_LAI.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                new_line = default.copy()
                new_line.update({
                    'MA_HANG_ID': line.MA_HANG_ID.id,
                    'TEN_HANG': line.TEN_HANG,
                    'DVT_ID': line.DVT_ID.id,
                    'KHO_ID': line.KHO_ID.id,
                    'DON_VI_ID': line.DON_VI_ID.id,
                    'SO_LUONG': line.SO_LUONG,
                    'DON_DAT_HANG_ID' : line.DON_DAT_HANG_ID.id,
                    'DON_DAT_HANG_CHI_TIET_ID' : line.DON_DAT_HANG_CHI_TIET_ID.id,
                    'TK_NO_ID': new_line.get('TK_NO_ID') or line.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                })
                self.CHI_TIET_IDS += self.env['stock.ex.nhap.xuat.kho.chi.tiet'].new(new_line)
            self.DOI_TUONG_ID = self.LAP_TU_HANG_BAN_TRA_LAI.DOI_TUONG_ID.id
            self.TEN_KHACH_HANG = self.LAP_TU_HANG_BAN_TRA_LAI.TEN_KHACH_HANG
            self.NHAN_VIEN_ID = self.LAP_TU_HANG_BAN_TRA_LAI.NHAN_VIEN_ID.id

    _sql_constraints = [
	    ('SO_CHUNG_TU_NXK_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
	]
    
    @api.onchange('LOAI_CHUNG_TU')
    def update_tai_khoan_ngam_dinh(self):
        if self.LAP_TU_LENH_SAN_XUAT_PHIEU_XUAT == False:
            for line in self.CHI_TIET_IDS:
                tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0))
                for tk in tk_nds:
                    setattr(line, tk, tk_nds.get(tk))

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ bán hàng -> Đã thay thế bằng onchange
    def lay_du_lieu_chung_tu_ban_hang(self, args):
        new_line =[[5]]
        chung_tu_ban_hang_id = args.get('chung_tu_ban_hang_id')
        thong_tin_chung_tu_master = self.env['sale.document'].search([('id', '=', chung_tu_ban_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        ten_doi_tuong = thong_tin_chung_tu_master['TEN_KHACH_HANG']
        ly_do_xuat = ''
        if ten_doi_tuong:
            ly_do_xuat = 'Xuất kho bán hàng ' + str(ten_doi_tuong)
        nguoi_nhan = thong_tin_chung_tu_master['NGUOI_LIEN_HE']
        dia_chi = thong_tin_chung_tu_master['DIA_CHI']
        danh_sach_chung_tu_ban_hang = self.env['sale.document.line'].search([('SALE_DOCUMENT_ID', '=', chung_tu_ban_hang_id)])
        if danh_sach_chung_tu_ban_hang:
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            for ct_bh in danh_sach_chung_tu_ban_hang:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [ct_bh['MA_HANG_ID'].id,ct_bh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_bh['TEN_HANG'],
                    'DVT_ID': [ct_bh['DVT_ID'].id,ct_bh['DVT_ID'].name],
                    'KHO_ID': [ct_bh['KHO_ID'].id,ct_bh['KHO_ID'].MA_KHO],
                    'DON_VI_ID': [ct_bh['DON_VI_ID'].id,ct_bh['DON_VI_ID'].MA_DON_VI],
                    'SO_LUONG': ct_bh['SO_LUONG'],
                    'DON_GIA_VON': ct_bh['DON_GIA'],
                    'THANH_TIEN': ct_bh['THANH_TIEN'],
                    'DON_DAT_HANG_ID' : ct_bh.DON_DAT_HANG_ID.id,
                    'DON_DAT_HANG_CHI_TIET_ID' : ct_bh.DON_DAT_HANG_CHI_TIET_ID.id,
                    })
                new_line += [(0,0,new_data)]
        return {'CHI_TIET_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                'TEN_KHACH_HANG': ten_doi_tuong,
                'NGUOI_NHAN_TEXT': nguoi_nhan,
                'LY_DO_XUAT': ly_do_xuat,
                'DIA_CHI': dia_chi,
                }


    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ bán hàng -> Đã thay thế bằng onchange
    def lay_du_lieu_chung_tu_ban_hang_tra_lai(self, args):
        new_line =[[5]]
        chung_tu_ban_hang_id = args.get('chung_tu_ban_hang_id')
        thong_tin_chung_tu_master = self.env['sale.ex.tra.lai.hang.ban'].search([('id', '=', chung_tu_ban_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        danh_sach_chung_tu_ban_hang = self.env['sale.ex.tra.lai.hang.ban.chi.tiet'].search([('TRA_LAI_HANG_BAN_ID', '=', chung_tu_ban_hang_id)])
        if danh_sach_chung_tu_ban_hang:
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            for ct_bh in danh_sach_chung_tu_ban_hang:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [ct_bh['MA_HANG_ID'].id,ct_bh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_bh['TEN_HANG'],
                    'DVT_ID': [ct_bh['DVT_ID'].id,ct_bh['DVT_ID'].name],
                    'KHO_ID': [ct_bh['KHO_ID'].id,ct_bh['KHO_ID'].MA_KHO],
                    'DON_VI_ID': [ct_bh['DON_VI_ID'].id,ct_bh['DON_VI_ID'].MA_DON_VI],
                    'SO_LUONG': ct_bh['SO_LUONG'],
                    'DON_DAT_HANG_ID':  [ct_bh['DON_DAT_HANG_ID'].id,ct_bh['DON_DAT_HANG_ID'].SO_DON_HANG],
                    'DON_DAT_HANG_CHI_TIET_ID' : [ct_bh.DON_DAT_HANG_CHI_TIET_ID.id,ct_bh.DON_DAT_HANG_CHI_TIET_ID.TEN_HANG],
                    })
                new_line += [(0,0,new_data)]
        return {'CHI_TIET_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                }

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn lệnh sản xuất -> Đã thay thế bằng onchange
    def lay_du_lieu_lenh_san_xuat(self, args):
        new_line =[[5]]
        lenh_san_xuat_id = args.get('lenh_san_xuat_id')
        kho = self.env['danh.muc.kho'].search([('MA_KHO', '=', 'KNVL')],limit=1)
        lenh_san_xuat_thanh_pham =  self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].search([('id', '=', lenh_san_xuat_id)],limit=1)
        lenh_san_xuat = ''
        thanh_pham = ''
        if lenh_san_xuat_thanh_pham:
            lenh_san_xuat = lenh_san_xuat_thanh_pham.SO
            thanh_pham = lenh_san_xuat_thanh_pham.MA_HANG_ID.MA

        kho_id = None
        ma_kho = ''
        if kho:
            kho_id = kho.id
            ma_kho = kho.MA_KHO

        danh_sach_dinh_muc_nguyen_vat_lieu = self.env['stock.ex.thanh.pham.chi.tiet.dinh.muc.xuat.nvl'].search([('THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_ID', '=', lenh_san_xuat_id)])
        if danh_sach_dinh_muc_nguyen_vat_lieu:
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            for lsx in danh_sach_dinh_muc_nguyen_vat_lieu:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [lsx['MA_HANG_ID'].id,lsx['MA_HANG_ID'].MA],
                    'TEN_HANG': lsx['TEN_NGUYEN_VAT_LIEU'],
                    'DVT_ID': [lsx['DVT_ID'].id,lsx['DVT_ID'].name],
                    'KHO_ID': [kho_id,ma_kho],
                    'SO_LUONG': lsx['SO_LUONG_NVL'],
                    'LENH_SAN_XUAT_VIEW_ID': lenh_san_xuat,
                    'THANH_PHAM_ID': [lenh_san_xuat_id,thanh_pham],
                    })
                new_line += [(0,0,new_data)]
        return {'CHI_TIET_IDS': new_line,}

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn lệnh sản xuất -> Đã thay thế bằng onchange
    def lay_du_lieu_lenh_san_xuat_tren_form_nhap_kho(self, args):
        new_line =[[5]]
        lenh_san_xuat_thanh_pham_id = args.get('lenh_san_xuat_id')
        kho = self.env['danh.muc.kho'].search([('MA_KHO', '=', 'KTP')],limit=1)
        kho_id = None
        ma_kho = ''
        if kho:
            kho_id = kho.id
            ma_kho = kho.MA_KHO
        lenh_san_xuat_thanh_pham =  self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].search([('id', '=', lenh_san_xuat_thanh_pham_id)],limit=1)
        lenh_san_xuat_id = 0
        if lenh_san_xuat_thanh_pham:
            lenh_san_xuat_id = lenh_san_xuat_thanh_pham.LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID
            lenh_san_xuat_so_lenh = lenh_san_xuat_thanh_pham.SO
            default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0)
            for lsx in lenh_san_xuat_thanh_pham:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [lsx['MA_HANG_ID'].id,lsx['MA_HANG_ID'].MA],
                    'TEN_HANG': lsx['TEN_THANH_PHAM'],
                    'DVT_ID': [lsx['DVT_ID'].id,lsx['DVT_ID'].name],
                    'KHO_ID': [kho_id,ma_kho],
                    'SO_LUONG': lsx['SO_LUONG'],
                    'LENH_SAN_XUAT_ID': [lenh_san_xuat_id,lenh_san_xuat_so_lenh],
                    })
                new_line += [(0,0,new_data)]
        return {'CHI_TIET_IDS': new_line,}


    @api.depends('type','loai_chuyen_kho') #Mạnh sửa bug1984
    def lay_thong_tin_so_chung_tu(self):
        for record in self:
            if record.type == 'CHUYEN_KHO':
                if record.loai_chuyen_kho == 'van_chuyen' or record.loai_chuyen_kho == 'gui_ban':
                    record.name = record.SO_CHUNG_TU_CK_READONLY
                else:
                    record.name = record.SO_CHUNG_TU
            else:
                record.name = record.SO_CHUNG_TU
                if record.type == 'XUAT_KHO' and record.LOAI_XUAT_KHO == 'XUAT_HANG':
                    record.name = record.SO_CHUNG_TU_CK_READONLY
            

    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.onchange('type','loai_chuyen_kho')
    def update_SO_CHUNG_TU(self):
        if self.type and (self.type != 'CHUYEN_KHO' or self.loai_chuyen_kho == 'chuyen_kho'):    
            auto_num = self.lay_so_chung_tu_tu_tang(self.type)
            self.SO_CHUNG_TU = auto_num.get(self.type)
            self.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num)
        else:
            self.SO_CHUNG_TU = None

    def lay_so_chung_tu_tu_tang(self, loai_chung_tu):
        auto_num = json.loads(self.SO_CHUNG_TU_TU_TANG_JSON or '{}')
        if not auto_num.get(loai_chung_tu):
            code = 'stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_' + loai_chung_tu
            next_seq = self.env['ir.sequence'].next_char_by_code(code)
            auto_num[loai_chung_tu] = next_seq

        return auto_num

    def lay_so_chung_tu_tiep_theo(self):
        self.ensure_one()
        if self.type != 'CHUYEN_KHO' or self.loai_chuyen_kho == 'chuyen_kho':    
            code = 'stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_' + self.type
            return self.env['ir.sequence'].next_char_by_code(code)

        return ''

    @api.depends('CHI_TIET_IDS')
    def tinh_tong_tien(self):
        for record in self:
            for line in record.CHI_TIET_IDS:
                record.TONG_TIEN_HANG += line.THANH_TIEN

    @api.onchange('DOI_TUONG_ID')
    def thaydoingh(self):
        if self.DOI_TUONG_ID:
            self.TEN_DOI_TUONG = self.DOI_TUONG_ID.HO_VA_TEN
            self.TEN_KHACH_HANG = self.DOI_TUONG_ID.HO_VA_TEN
            self.NGUOI_NHAN_TEXT= self.env['res.partner'].search([('parent_id', '=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            self.NGUOI_GIAO_HANG_TEXT = self.env['res.partner'].search([('parent_id','=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            self.TEN_NGUOI_NHAN = self.DOI_TUONG_ID.HO_VA_TEN
            self.BO_PHAN = self.DOI_TUONG_ID.DIA_CHI
            self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
            self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE


    @api.onchange('NGUOI_VAN_CHUYEN_ID')
    def thaydoinvc(self):
        self.TEN_NGUOI_VAN_CHUYEN = self.NGUOI_VAN_CHUYEN_ID.HO_VA_TEN
    
    @api.model
    def default_get(self,default_fields):
        res = super(STOCK_EX_NHAP_XUAT_KHO, self).default_get(default_fields)
        id_lap_rap_thao_do = self.get_context('default_ID_LAP_RAP_THAO_DO')
          #neu có tồn tại id của lắp ráp tháo dỡ:
                #ktra nếu là phiếu nhập
                #   nếu là lắp ráp
                #       chitiet nhập kho = master tháo dỡ
        if id_lap_rap_thao_do:
            arr_nhap_xuat_kho= []
            if self.get_context('default_type') == 'NHAP_KHO':
                lap_rap_thao_do_mt = self.env['stock.ex.lap.rap.thao.do'].search([('id','=',id_lap_rap_thao_do)])
                lap_rap_thao_do_deatail_nk = self.env['stock.ex.lap.rap.thao.do.chi.tiet'].search([('LAP_RAP_THAO_DO_CHI_TIET_ID','=',id_lap_rap_thao_do)])
                if lap_rap_thao_do_mt.LAP_RAP_THAO_DO =='LAP_RAP':
                    res['DIEN_GIAI']='Nhập kho từ lắp ráp'
                    res['CHI_TIET_IDS'] = []
               
                    arr_nhap_xuat_kho +=[(0,0,{
                        'MA_HANG_ID':lap_rap_thao_do_mt.HANG_HOA_ID.id,
                        'TEN_HANG'  :lap_rap_thao_do_mt.TEN_HANG_HOA,
                        'DVT_ID':lap_rap_thao_do_mt.DVT_ID.id,
                        'SO_LUONG'  :lap_rap_thao_do_mt.SO_LUONG,
                        'DON_GIA_VON'  :lap_rap_thao_do_mt.DON_GIA,
                        'TIEN_VON'  :lap_rap_thao_do_mt.THANH_TIEN,

                        'LENH_LR_TD_ID'  :lap_rap_thao_do_mt.id,
                        'KHO_ID'  :lap_rap_thao_do_mt.HANG_HOA_ID.KHO_NGAM_DINH_ID.id,
                        'TK_NO_ID'  :lap_rap_thao_do_mt.HANG_HOA_ID.TAI_KHOAN_KHO_ID.id,
                        # 'TK_CO_ID'  :lap_rap_thao_do_mt.THANH_TIEN,
                        
                    })]
                    res['CHI_TIET_IDS'] = arr_nhap_xuat_kho
                #   nếu là tháo dỡ -- loi lenh lr
                #   chitiet nhập kho = detail tháo dỡ
                else:
                    res['DIEN_GIAI']='Nhập kho từ tháo dỡ'
                    res['CHI_TIET_IDS'] = []
                    for lap_rap_thao_ro_dt_ct in lap_rap_thao_do_deatail_nk:
                        arr_nhap_xuat_kho +=[(0,0,{
                            'MA_HANG_ID':lap_rap_thao_ro_dt_ct.MA_HANG_ID.id,
                            'TEN_HANG'  :lap_rap_thao_ro_dt_ct.TEN_HANG,
                            'DVT_ID':lap_rap_thao_ro_dt_ct.DVT_ID.id,
                            'SO_LUONG'  :lap_rap_thao_ro_dt_ct.SO_LUONG,
                            'DON_GIA_VON'  :lap_rap_thao_ro_dt_ct.DON_GIA,
                            'TIEN_VON'  :lap_rap_thao_ro_dt_ct.THANH_TIEN,
                            'KHO_ID'  :lap_rap_thao_ro_dt_ct.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                            'TK_NO_ID'  :lap_rap_thao_ro_dt_ct.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                            'LENH_LR_TD_ID'  :lap_rap_thao_do_mt.id,
                        })]
                    res['CHI_TIET_IDS'] = arr_nhap_xuat_kho
                #ktra nếu là phiếu xuất
               
               
            elif self.get_context('default_type') == 'XUAT_KHO':
                lap_rap_thao_do_mt_xk = self.env['stock.ex.lap.rap.thao.do'].search([('id','=',id_lap_rap_thao_do)])
                lap_rap_thao_do_deatail_xk = self.env['stock.ex.lap.rap.thao.do.chi.tiet'].search([('LAP_RAP_THAO_DO_CHI_TIET_ID','=',id_lap_rap_thao_do)])
                #   nếu là lắp ráp -- lỗi
                #       chi tiết xuất kho = detail tháo dỡ
                if lap_rap_thao_do_mt_xk.LAP_RAP_THAO_DO =='LAP_RAP':
                    res['LY_DO_XUAT']= 'Xuất kho để lắp ráp'
                    res['CHI_TIET_IDS'] = []
                    for lap_rap_thao_ro_dt_ct in lap_rap_thao_do_deatail_xk:
                        arr_nhap_xuat_kho +=[(0,0,{
                            'MA_HANG_ID':lap_rap_thao_ro_dt_ct.MA_HANG_ID.id,
                            'TEN_HANG'  :lap_rap_thao_ro_dt_ct.TEN_HANG,
                            'DVT_ID':lap_rap_thao_ro_dt_ct.DVT_ID.id,
                            'SO_LUONG'  :lap_rap_thao_ro_dt_ct.SO_LUONG,
                            'DON_GIA_VON'  :lap_rap_thao_ro_dt_ct.DON_GIA,
                            'TIEN_VON'  :lap_rap_thao_ro_dt_ct.THANH_TIEN,

                            'LENH_LR_TD_ID'  :lap_rap_thao_do_mt_xk.id,
                            'KHO_ID'  :lap_rap_thao_ro_dt_ct.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                            'TK_NO_ID'  :lap_rap_thao_ro_dt_ct.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                        # 'TK_CO_ID'  :lap_rap_thao_do_mt.THANH_TIEN,
                        
                        })]
                    res['CHI_TIET_IDS'] = arr_nhap_xuat_kho
                #   nếu là tháo dỡ
                #     chi tiết xuất kho = master tháo dỡ
                else:
                    res['LY_DO_XUAT'] ='Xuất kho để tháo dỡ'
                    res['CHI_TIET_IDS'] = []
                    arr_nhap_xuat_kho +=[(0,0,{
                        'MA_HANG_ID':lap_rap_thao_do_mt_xk.HANG_HOA_ID.id,
                        'TEN_HANG'  :lap_rap_thao_do_mt_xk.TEN_HANG_HOA,
                        'DVT_ID':lap_rap_thao_do_mt_xk.DVT_ID.id,
                        'SO_LUONG'  :lap_rap_thao_do_mt_xk.SO_LUONG,
                        'DON_GIA_VON'  :lap_rap_thao_do_mt_xk.DON_GIA,
                        'TIEN_VON'  :lap_rap_thao_do_mt_xk.THANH_TIEN,

                        'LENH_LR_TD_ID'  :lap_rap_thao_do_mt_xk.id,
                        'KHO_ID'  :lap_rap_thao_do_mt_xk.HANG_HOA_ID.KHO_NGAM_DINH_ID.id,
                        'TK_NO_ID'  :lap_rap_thao_do_mt_xk.HANG_HOA_ID.TAI_KHOAN_KHO_ID.id,
                        # 'TK_CO_ID'  :lap_rap_thao_do_mt.THANH_TIEN,
                        
                    })]
                    res['CHI_TIET_IDS'] = arr_nhap_xuat_kho

                #neu id_bảng_kiểm_kê_ tồn tại
                    #nếu là nhập kho
                        #bật form nhập kho
                            #gán giá trị: detail nhập kho = detail bảng kiểm kê

        id_bang_kiem_ke = self.get_context('default_ID_BANG_KIEM_KE')
        if id_bang_kiem_ke:
            arr_bang_kiem_ke_nk =[]
            if self.get_context('default_type')=='NHAP_KHO':
                bang_kiem_ke_vthh_detail = self.env['stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form'].search([('KIEM_KE_BANG_KIEM_KE_VTHH_ID','=',id_bang_kiem_ke)])
                res['CHI_TIET_IDS'] = []
                res['DIEN_GIAI'] = 'Kiểm kê phát hiện kế thừa'
                for dong_bang_kiem_ke_vthh_dt in bang_kiem_ke_vthh_detail:
                    #kiểm tra nếu số lượng chênh lêch>0
                        #thực hiện nhập kho
                    if dong_bang_kiem_ke_vthh_dt.SO_LUONG_CHENH_LECH >0:
                        arr_bang_kiem_ke_nk +=[(0,0,{
                            'MA_HANG_ID':dong_bang_kiem_ke_vthh_dt.MA_HANG_ID.id,
                            'TEN_HANG'  :dong_bang_kiem_ke_vthh_dt.TEN_HANG,
                            'DVT_ID':dong_bang_kiem_ke_vthh_dt.DVT_ID.id,
                            'SO_LUONG'  :dong_bang_kiem_ke_vthh_dt.SO_LUONG_CHENH_LECH,
                            'SO_LO'  :dong_bang_kiem_ke_vthh_dt.SO_LO,
                            # 'HAN_SU_DUNG'  :dong_bang_kiem_ke_vthh_dt.HAN_SU_DUNG,

                            'KHO_ID'  :dong_bang_kiem_ke_vthh_dt.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                            'TK_NO_ID'  :dong_bang_kiem_ke_vthh_dt.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                        
                        
                        })]
                res['CHI_TIET_IDS'] += arr_bang_kiem_ke_nk
            elif self.get_context('default_type')=='XUAT_KHO':
                arr_bang_kiem_ke_xk =[]
                bang_kiem_ke_vthh_detail = self.env['stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form'].search([('KIEM_KE_BANG_KIEM_KE_VTHH_ID','=',id_bang_kiem_ke)])
                res['CHI_TIET_IDS'] = []
                res['LY_DO_XUAT'] = 'Kiểm kê phát hiện thiếu'
                for dong_bang_kiem_ke_vthh_dt in bang_kiem_ke_vthh_detail:
                    #kiểm tra nếu số lượng chênh lêch<0
                        #thực hiện nhập kho
                    if dong_bang_kiem_ke_vthh_dt.SO_LUONG_CHENH_LECH <0:
                        arr_bang_kiem_ke_xk +=[(0,0,{
                            'MA_HANG_ID':dong_bang_kiem_ke_vthh_dt.MA_HANG_ID.id,
                            'TEN_HANG'  :dong_bang_kiem_ke_vthh_dt.TEN_HANG,
                            'DVT_ID':dong_bang_kiem_ke_vthh_dt.DVT_ID.id,
                            'SO_LUONG'  :dong_bang_kiem_ke_vthh_dt.SO_LUONG_CHENH_LECH,
                            'SO_LO'  :dong_bang_kiem_ke_vthh_dt.SO_LO,
                            # 'HAN_SU_DUNG'  :dong_bang_kiem_ke_vthh_dt.HAN_SU_DUNG,

                            'KHO_ID'  :dong_bang_kiem_ke_vthh_dt.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                            'TK_NO_ID'  :dong_bang_kiem_ke_vthh_dt.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                       
                        
                        })]
                res['CHI_TIET_IDS'] += arr_bang_kiem_ke_xk
            
        if self._context.get('id_lenh_san_xuat_thanh_pham'):
            arr_lenh_san_xuat = []
            ly_do_xuat = ''
            for line in self._context.get('id_lenh_san_xuat_thanh_pham'):
                thanh_pham = self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].browse(line)
                if self._context.get('default_type') == 'XUAT_KHO':
                    ly_do_xuat = 'Xuất kho NVL sản xuất theo Lệnh sản xuất <' + str(thanh_pham.LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.SO_LENH) + '>'
                    if thanh_pham and thanh_pham.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS:
                        for chi_tiet in thanh_pham.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS:
                            arr_lenh_san_xuat +=[(0,0,{
                                    'MA_HANG_ID': chi_tiet.MA_HANG_ID.id,
                                    'TEN_HANG'  : chi_tiet.TEN_NGUYEN_VAT_LIEU,
                                    'DVT_ID': chi_tiet.DVT_ID.id,
                                    'SO_LUONG'  : chi_tiet.SO_LUONG_NVL,
                                    # 'SO_LO'  :dong_bang_kiem_ke_vthh_dt.SO_LO,
                                    'KHO_ID'  :chi_tiet.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                                    'TK_CO_ID'  :chi_tiet.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                                    'THANH_PHAM_ID' : thanh_pham.id,
                                    'LENH_SAN_XUAT_VIEW_ID' : thanh_pham.MA_HANG_ID.MA,
                            
                                })]
                elif self._context.get('default_type') == 'NHAP_KHO':
                    ly_do_xuat = 'Nhập kho NVL sản xuất theo Lệnh sản xuất <' + str(thanh_pham.LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.SO_LENH) + '>'
                    arr_lenh_san_xuat +=[(0,0,{
                            'MA_HANG_ID': thanh_pham.MA_HANG_ID.id,
                            'TEN_HANG'  : thanh_pham.MA_HANG_ID.TEN,
                            'DVT_ID': thanh_pham.DVT_ID.id,
                            'SO_LUONG'  : thanh_pham.SO_LUONG,
                            'KHO_ID'  : thanh_pham.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                            'TK_CO_ID'  : thanh_pham.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                            'LENH_SAN_XUAT_ID' : thanh_pham.LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.id,
                            'LENH_SAN_XUAT_VIEW_ID' : thanh_pham.MA_HANG_ID.MA,
                    
                        })]

            res['CHI_TIET_IDS'] = arr_lenh_san_xuat
            res['LY_DO_XUAT'] = ly_do_xuat
            res['DIEN_GIAI'] = ly_do_xuat
        
        # id_lsx_phieu_nhap_xuat_kho= self.get_context('default_ID_LSX_LAP_PHIEU_NX')
        # #nếu id lsx_phieu_nhap_xuat_kho tồn tại
        #     #nếu là phiếu nhập
        #         #detail phiếu nhập kho = detail lệnh sản xuất
        #     #nếu là phiếu xuất
        #         #detail phiếu xuất kho = detail lệnh sản xuất
        # if id_lsx_phieu_nhap_xuat_kho:
        #     arr_nhap_xuat_kho_lsx= []
        #     if self.get_context('default_type') == 'NHAP_KHO':
        #         # lsx_mt_pn = self.env['stock.ex.lenh.san.xuat'].search([('id','=',id_lsx_phieu_nhap_xuat_kho)])
        #         lsx_detail_pn = self.env['stock.ex.lenh.san.xuat.lap.pn.chi.tiet.form'].search([('LAP_PN_CHI_TIET_ID','=',id_lsx_phieu_nhap_xuat_kho)])
        #         res['CHI_TIET_IDS'] = []
        #         for lsx_detail in lsx_detail_pn:
        #             arr_nhap_xuat_kho +=[(0,0,{
        #                 'MA_HANG_ID':lsx_detail_pn.MA_THANH_PHAM_ID.id,
        #                 'TEN_HANG'  :lsx_detail_pn.TEN_THANH_PHAM,
        #                 'DVT_ID':lsx_detail_pn.DVT_ID.id,
        #                 'SO_LUONG'  :lsx_detail_pn.SO_LUONG,
        #                 # 'DON_GIA'  :lsx_detail_pn.DON_GIA,
        #                 'LENH_SAN_XUAT_ID'  :lsx_detail_pn.id,

        #                 'KHO_ID'  :lsx_detail_pn.MA_THANH_PHAM_ID.KHO_NGAM_DINH_ID.id,
        #                 'TK_NO_ID'  :lsx_detail_pn.MA_THANH_PHAM_ID.TAI_KHOAN_KHO_ID.id,
        #                 'DOI_TUONG_THCP_ID'  :lsx_detail_pn.DOI_TUONG_THCP_ID.id,
        #                 'MA_THONG_KE_ID'  :lsx_detail_pn.MA_THONG_KE_ID.id,
        #             # 'TK_CO_ID'  :lap_rap_thao_do_mt.THANH_TIEN,
                    
        #             })]
        #         res['CHI_TIET_IDS'] = arr_nhap_xuat_kho_lsx


        loai_chung_tu = self.get_context('default_LOAI_CHUNG_TU')
        loai_chung_tu_px= self.get_context('default_LOAI_CHUNG_TU_PX')

        loai_chung_tu_bang_kiem_ke_vthh = self.get_context('default_LOAI_CHUNG_TU_KIEM_KE_VTHH')
        loai_chung_tu_bang_kiem_ke_vthh_px = self.get_context('default_LOAI_CHUNG_TU_KIEM_KE_VTHH_PX')
        if loai_chung_tu:
            res['LOAI_CHUNG_TU_2']=loai_chung_tu
        if loai_chung_tu_px:
            res['LOAI_CHUNG_TU_2']=loai_chung_tu_px
        
        if loai_chung_tu_bang_kiem_ke_vthh:
            res['LOAI_CHUNG_TU_2']=loai_chung_tu_bang_kiem_ke_vthh
        if loai_chung_tu_bang_kiem_ke_vthh_px:
            res['LOAI_CHUNG_TU_2']=loai_chung_tu_bang_kiem_ke_vthh_px
        
        # if self.get_context('LOAI_CHUNG_TU_2')==2015:
        #     res['LOAI_NHAP_KHO']='KHAC'
        return res

    @api.multi
    def validate_nhap_xuat_kho(self):
        for record in self:
            record.validate_unique_nhap_xuat_kho(record.SO_CHUNG_TU)
    
    @api.model
    def create(self, vals): 
        result = super(STOCK_EX_NHAP_XUAT_KHO, self).create(vals)
        result.validate_nhap_xuat_kho()
        if result.CHI_TIET_IDS:
            result.up_date_don_dat_hang()
        if result.type != 'CHUYEN_KHO' or result.loai_chuyen_kho == 'chuyen_kho':
            sequence_code = 'stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_' + result.type
            self.update_sequence(sequence_code, result.SO_CHUNG_TU)
        if result.LAP_RAP_THAO_DO_ID:
            result.LAP_RAP_THAO_DO_ID.THAM_CHIEU = [(4, result.id)]
        return result
    
    @api.multi
    def write(self, values):
        result = super(STOCK_EX_NHAP_XUAT_KHO, self).write(values)
        for record in self:
            if record.CHI_TIET_IDS:
                record.up_date_don_dat_hang()
        if values.get('SO_CHUNG_TU'):
            self.validate_nhap_xuat_kho()
        return result    

    @api.multi
    def unlink(self):
        arr_don_dat_hang = []
        for record in self:
            if record.CHI_TIET_IDS:
                for chi_tiet in record.CHI_TIET_IDS:
                    if chi_tiet.DON_DAT_HANG_ID:
                        arr_don_dat_hang.append(chi_tiet.DON_DAT_HANG_ID.id)
        result = super(STOCK_EX_NHAP_XUAT_KHO, self).unlink()
        if arr_don_dat_hang:
            for line in arr_don_dat_hang:
                self.update_so_luong_don_dat_hang(line)
        return result

    def up_date_don_dat_hang(self):
        arr_don_dat_hang = []
        for chi_tiet in self.CHI_TIET_IDS:
                if chi_tiet.DON_DAT_HANG_ID:
                    if chi_tiet.DON_DAT_HANG_ID.id not in arr_don_dat_hang:
                        arr_don_dat_hang.append(chi_tiet.DON_DAT_HANG_ID.id)
        if arr_don_dat_hang:
            for line in arr_don_dat_hang:
                self.update_so_luong_don_dat_hang(line)
    
    @api.depends('type','LOAI_NHAP_KHO','LOAI_XUAT_KHO','loai_chuyen_kho')
    def set_loai_chung_tu_nhap_xuat_kho(self):
        for record in self:
            if record.type =='NHAP_KHO':
                if record.LOAI_CHUNG_TU_2 == 2011:
                    record.LOAI_CHUNG_TU = record.LOAI_CHUNG_TU_2
                elif record.LOAI_CHUNG_TU_2 == 2015:
                    record.LOAI_CHUNG_TU= record.LOAI_CHUNG_TU_2
                    record.LOAI_NHAP_KHO= 'KHAC'
                elif record.LOAI_CHUNG_TU_2 == 2012:
                    record.LOAI_CHUNG_TU= record.LOAI_CHUNG_TU_2
                    record.LOAI_NHAP_KHO= 'THANH_PHAM'
                else:
                    #VU nếu loại chứng từ =2011 thì ko chạy đoạn tiếp theo
                    if record.LOAI_NHAP_KHO == 'THANH_PHAM':
                        record.LOAI_CHUNG_TU=2010
                    elif record.LOAI_NHAP_KHO=='TRA_LAI':
                        record.LOAI_CHUNG_TU=2013
                    else:
                        record.LOAI_CHUNG_TU=2014
            elif record.type =='XUAT_KHO':
                if record.LOAI_CHUNG_TU_2 == 2024:
                    record.LOAI_CHUNG_TU = record.LOAI_CHUNG_TU_2
                elif record.LOAI_CHUNG_TU_2 == 2026:
                    record.LOAI_CHUNG_TU = record.LOAI_CHUNG_TU_2
                    record.LOAI_XUAT_KHO= 'KHAC'
                elif record.LOAI_CHUNG_TU_2 == 2025:
                    record.LOAI_CHUNG_TU = record.LOAI_CHUNG_TU_2
                    record.LOAI_XUAT_KHO= 'SAN_XUAT'
                else:
                    if record.LOAI_XUAT_KHO == 'BAN_HANG':
                        record.LOAI_CHUNG_TU=2020
                    elif record.LOAI_XUAT_KHO=='SAN_XUAT':
                        record.LOAI_CHUNG_TU=2023
                    elif record.LOAI_XUAT_KHO =='XUAT_HANG' :
                        record.LOAI_CHUNG_TU=2021
                    else:
                        record.LOAI_CHUNG_TU=2022
            elif record.type =='CHUYEN_KHO':
                if record.loai_chuyen_kho == 'van_chuyen':
                    record.LOAI_CHUNG_TU=2030
                elif record.loai_chuyen_kho =='gui_ban' :
                    record.LOAI_CHUNG_TU=2031
                else:
                    record.LOAI_CHUNG_TU=2032
            
    @api.depends('LOAI_CHUNG_TU')
    def set_loai_chung_tu_text(self):
        for record in self:
            loai_chung_tu_text = ''
            ref_type = record.env['danh.muc.reftype'].search([('REFTYPE', '=', record.LOAI_CHUNG_TU)],limit=1)
            if ref_type:
                loai_chung_tu_text = ref_type.REFTYPENAME
            record.LOAI_CHUNG_TU_TEXT = loai_chung_tu_text

    @api.onchange('loai_chuyen_kho')
    def thaydoichuyenkho(self):
        str1 ='Xuất kho kiêm vận chuyển'
        str2 ='Xuất kho gửi bán đại lý'
        str3 ='Xuất chuyển kho nội bộ'
       
        if self.loai_chuyen_kho == 'van_chuyen':
            self.LOAI_CK=str1
        elif self.loai_chuyen_kho=='gui_ban':
            self.LOAI_CK=str2
        else:
            self.LOAI_CK=str3

    
    @api.multi
    def action_ghi_so(self):
        for record in self:
            # if not record.SOURCE_ID:
            record.ghi_so_cai()
            record.ghi_so_kho()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.CHI_TIET_IDS:
            if line.TK_NO_ID.id != line.TK_CO_ID.id:
                if line.DOI_TUONG_ID:
                    doi_tuong_id = line.DOI_TUONG_ID.id
                else:
                    doi_tuong_id = self.DOI_TUONG_ID.id
                if self.type == 'NHAP_KHO':
                    doi_tuong_id = self.DOI_TUONG_ID.id
                data_ghi_no = helper.Obj.inject(line, self)
                nhan_vien_id = None
                if self.NHAN_VIEN_ID:
                    nhan_vien_id = self.NHAN_VIEN_ID.id
                else:
                    if self.SOURCE_ID:
                        nhan_vien_id = self.SOURCE_ID.NHAN_VIEN_ID.id
                nguoi_lien_he = None
                so_hoa_don = None
                if self.type == 'XUAT_KHO':
                    nguoi_lien_he = self.NGUOI_NHAN_TEXT
                    if self.LOAI_XUAT_KHO == 'XUAT_HANG':
                        so_hoa_don = self.SO_CHUNG_TU_CK_READONLY
                elif self.type == 'CHUYEN_KHO':
                    if self.loai_chuyen_kho in ('van_chuyen','gui_ban'):
                        so_hoa_don = self.SO_CHUNG_TU_CK_READONLY
                else:
                    if self.LOAI_NHAP_KHO == 'THANH_PHAM':
                        # nguoi_lien_he = self.TEN_DOI_TUONG
                        nguoi_lien_he = None
                    elif self.LOAI_NHAP_KHO in ('TRA_LAI','KHAC'):
                        nguoi_lien_he = self.NGUOI_GIAO_HANG_TEXT
                data_ghi_no.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'DIEN_GIAI_CHUNG': self.LY_DO_XUAT,
                    'DIEN_GIAI' : line.TEN_HANG,
                    'NGUOI_LIEN_HE' : nguoi_lien_he,
                    'SO_LUONG' : line.SO_LUONG,
                    'DOI_TUONG_ID' : doi_tuong_id,
                    'DON_VI_ID' : line.DON_VI_ID.id,
                    'TAI_KHOAN_ID': line.TK_NO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : line.TIEN_VON,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_VON,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'SO_CHUNG_TU' : self.SO_CHUNG_TU, 
                    'LOAI_HACH_TOAN' : '1',		
                    'TY_GIA' : 1,
                    'NHAN_VIEN_ID' : nhan_vien_id,
                    'DON_GIA' : line.DON_GIA_VON if line.DON_GIA_VON else line.DON_GIA,
                    'SO_HOA_DON' : so_hoa_don,
                    'NGAY_HACH_TOAN' : self.NGAY_HACH_TOAN,
                    'NGAY_CHUNG_TU' : self.NGAY_CHUNG_TU,
                })
                if self.LOAI_XUAT_KHO in ('XUAT_HANG','BAN_HANG'):
                    data_ghi_no.update({
                        # 'DON_GIA' : line.DON_GIA_VON,
                        'GHI_NO' : line.TIEN_VON,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_VON,
                        # 'NHAN_VIEN_ID' : None,
                    })
                elif self.loai_chuyen_kho == 'gui_ban':
                    data_ghi_no.update({
                        'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                    })
                line_ids += [(0,0,data_ghi_no)]
                data_ghi_co = data_ghi_no.copy()
                data_ghi_co.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.TIEN_VON,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_VON,
                    'LOAI_HACH_TOAN' : '2',
                })
                if self.LOAI_XUAT_KHO == 'XUAT_HANG':
                    data_ghi_co.update({
                        'GHI_CO' : line.TIEN_VON,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_VON,
                    })
                line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True
    
    def ghi_so_kho(self):
        line_ids = []
        thu_tu = 0
        # Nhập kho
        if (self.type == 'NHAP_KHO'):
            for line in self.CHI_TIET_IDS:
                data = helper.Obj.inject(line, self)
                data.update({
                    'DIEN_GIAI': line.TEN_HANG,
                    'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'SO_LUONG_NHAP': line.SO_LUONG,
                    'SO_LUONG_NHAP_THEO_DVT_CHINH' : line.SO_LUONG,
                    'SO_TIEN_NHAP': line.TIEN_VON,
                    'DON_GIA' : line.DON_GIA_VON,
                    'SO_LUONG_XUAT': 0,
                    'SO_LUONG_XUAT_THEO_DVT_CHINH' : 0,
                    'SO_TIEN_XUAT': 0,
                    'KHO_ID': line.KHO_ID.id,
                    'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                    'DVT_CHINH_ID' : line.MA_HANG_ID.DVT_CHINH_ID.id,
                    'CHI_TIET_ID' : line.id,
                    'LOAI_KHU_VUC_NHAP_XUAT' : '1',
                    'NGUOI_LIEN_HE' : self.NGUOI_GIAO_HANG_TEXT,
                    'TOAN_TU_QUY_DOI' : 'NHAN' if line.TOAN_TU_QUY_DOI == '0' else 'CHIA',
                    'MA_DOI_TUONG_THCP_ID' : line.DOI_TUONG_THCP_ID.id,
                    'LA_NHAP_KHO' : True,
                })
                line_ids += [(0,0,data)]
                thu_tu += 1

        # Xuất kho
        elif (self.type == 'XUAT_KHO'):
            for line in self.CHI_TIET_IDS:
                data = helper.Obj.inject(line, self)
                data.update({
                    'DIEN_GIAI': line.TEN_HANG,
                    'DIEN_GIAI_CHUNG' : self.LY_DO_XUAT,
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'SO_LUONG_NHAP': 0,
                    'SO_LUONG_NHAP_THEO_DVT_CHINH' : 0,
                    'SO_TIEN_NHAP': 0,
                    'SO_LUONG_XUAT': line.SO_LUONG,
                    'SO_LUONG_XUAT_THEO_DVT_CHINH' : line.SO_LUONG,
                    'SO_TIEN_XUAT': line.TIEN_VON,
                    'DON_GIA' : line.DON_GIA_VON,
                    'KHO_ID': line.KHO_ID.id,
                    'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else line.DOI_TUONG_ID.id,
                    'TK_NO_ID' : line.TK_CO_ID.id,
                    'TK_CO_ID' : line.TK_NO_ID.id,
                    'CHI_TIET_ID' : line.id,
                    'LOAI_KHU_VUC_NHAP_XUAT' : '3',
                    'NGUOI_LIEN_HE' : self.NGUOI_NHAN_TEXT,
                    'LOAI_KHONG_CAP_NHAT_GIA_XUAT' : '3' if self.LOAI_CHUNG_TU == 2026 else '0',
                    'MA_HOP_DONG' : line.HOP_DONG_BAN_ID.SO_HOP_DONG,
                    'TOAN_TU_QUY_DOI' : 'NHAN' if line.TOAN_TU_QUY_DOI == '0' else 'CHIA',
                    'MA_DOI_TUONG_THCP_ID' : line.DOI_TUONG_THCP_ID.id,
                })
                line_ids += [(0,0,data)]
                thu_tu += 1
        # Chuyển kho
        else:
            for line in self.CHI_TIET_IDS:
                data_x = helper.Obj.inject(line, self)
                data_x.update({
                    'DIEN_GIAI': line.TEN_HANG,
                    'DIEN_GIAI_CHUNG' : self.LY_DO_XUAT,
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'KHO_ID': line.NHAP_TAI_KHO_ID.id,
                    'SO_LUONG_NHAP': line.SO_LUONG,
                    'SO_LUONG_NHAP_THEO_DVT_CHINH' : line.SO_LUONG,
                    'SO_TIEN_NHAP': line.TIEN_VON,
                    'DON_GIA' : line.DON_GIA_VON,
                    'SO_LUONG_XUAT': 0,
                    'SO_LUONG_XUAT_THEO_DVT_CHINH' : 0,
                    'SO_TIEN_XUAT': 0,
                    'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                    'CHI_TIET_ID' : line.id,
                    'NGAY_HACH_TOAN' : self.NGAY_HACH_TOAN,
                    'NGAY_CHUNG_TU' : self.NGAY_CHUNG_TU,
                    'LOAI_KHU_VUC_NHAP_XUAT' : '2',
                    'LA_NHAP_KHO' : True,
                    'TOAN_TU_QUY_DOI' : 'NHAN' if line.TOAN_TU_QUY_DOI == '0' else 'CHIA',
                    'MA_DOI_TUONG_THCP_ID' : line.DOI_TUONG_THCP_ID.id,
                })
                line_ids += [(0,0,data_x)]
                thu_tu += 1

                data_n = data_x.copy()
                data_n.update({
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'KHO_ID': line.XUAT_TAI_KHO_ID.id,
                    'SO_LUONG_NHAP': 0,
                    'SO_LUONG_NHAP_THEO_DVT_CHINH' : 0,
                    'SO_TIEN_NHAP': 0,
                    'SO_LUONG_XUAT': line.SO_LUONG,
                    'SO_LUONG_XUAT_THEO_DVT_CHINH' : line.SO_LUONG,
                    'SO_TIEN_XUAT': line.TIEN_VON,
                    'DON_GIA' : line.DON_GIA_VON,
                    'TK_NO_ID' : line.TK_CO_ID.id,
                    'TK_CO_ID' : line.TK_NO_ID.id,
                    'LA_NHAP_KHO' : False,
                })
                line_ids += [(0,0,data_n)]
                thu_tu += 1
        # Tạo master
        sk = self.env['so.kho'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_KHO_ID = sk.id
        return True
    
    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        fields += ['ID_GOC', 'MODEL_GOC']
        return self.env['stock.ex.nhap.xuat.kho.view'].search_read(domain, fields, offset, limit, order)
    
    # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1636
    @api.model
    def search_count(self, args):
        return self.env['stock.ex.nhap.xuat.kho.view'].search_count(args)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(STOCK_EX_NHAP_XUAT_KHO, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
        if toolbar:
            bindings = self.env['ir.actions.actions'].get_bindings('stock.ex.nhap.xuat.kho.view')
            res['toolbar']['print'] += [action for action in bindings['report'] if view_type == 'tree' or not action.get('multi')]
        return res

    @api.multi
    def get_formview_id(self, access_uid=None):
        if self.type == 'NHAP_KHO':
            return self.env.ref('stock_ex.view_nhap_kho_form').id
        elif self.type == 'XUAT_KHO':
            return self.env.ref('stock_ex.view_xuat_kho_form').id
        elif self.type == 'CHUYEN_KHO':
            return self.env.ref('stock_ex.view_chuyen_kho_form').id

        return super(STOCK_EX_NHAP_XUAT_KHO, self).get_formview_id(access_uid)


    
    def update_so_luong_don_dat_hang(self,id_don_dat_hang):
        params = {
            'ID_DON_DAT_HANG' : id_don_dat_hang,
            }
        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
                --     id_chung_tu_ban_hang INTEGER := 289;

                id_don_dat_hang INTEGER := %(ID_DON_DAT_HANG)s;

                format_so       INTEGER :=2;


            BEGIN

                SELECT value
                INTO format_so
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;

                DROP TABLE IF EXISTS TMP_DON_DAT_HANG
                ;

                CREATE TEMP TABLE TMP_DON_DAT_HANG
                    AS
                        SELECT id AS "DON_DAT_HANG_ID"
                        FROM account_ex_don_dat_hang
            --             WHERE id = id_don_dat_hang
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                            T."DON_DAT_HANG_ID"
                            , T."DON_DAT_HANG_CHI_TIET_ID"
                            , T."MA_HANG_ID"
                            , SUM("SO_LUONG_DA_GIAO")                AS "SO_LUONG_DA_GIAO"
                            , SUM("SO_LUONG_DA_GIAO_THEO_DVT_CHINH") AS "SO_LUONG_DA_GIAO_THEO_DVT_CHINH"
                        FROM
                            (
                                /*Lấy số đã giao từ chứng từ bán hàng*/
                                SELECT
                                    TOI."DON_DAT_HANG_ID"
                                    , SOD."id"                                      AS "DON_DAT_HANG_CHI_TIET_ID"
                                    , SOD."MA_HANG_ID"
                                    , SUM(ROUND(cast((CASE WHEN ((SOD."DVT_ID" ISNULL AND SVD."DVT_ID" ISNULL) OR
                                                                (SOD."DVT_ID" NOTNULL AND SVD."DVT_ID" NOTNULL AND
                                                                SOD."DVT_ID" = SVD."DVT_ID"))
                                    THEN SVD."SO_LUONG"
                                                    ELSE (CASE WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                                    '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                                        THEN ROUND(
                                                            cast((SVD."SO_LUONG_THEO_DVT_CHINH" *
                                                                    SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                AS NUMERIC),
                                                            format_so)
                                                            WHEN (SOD."TOAN_TU_QUY_DOI" = '0' AND
                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" <>
                                                                0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                                THEN ROUND(cast((SVD."SO_LUONG_THEO_DVT_CHINH" /
                                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH") AS NUMERIC),
                                                                        format_so)
                                                            ELSE SVD."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                            END)
                                                    END) AS NUMERIC), format_so)) AS "SO_LUONG_DA_GIAO"
                                    , SUM(SVD."SO_LUONG_THEO_DVT_CHINH")            AS "SO_LUONG_DA_GIAO_THEO_DVT_CHINH"
                                FROM TMP_DON_DAT_HANG AS TOI
                                    INNER JOIN account_ex_don_dat_hang_chi_tiet AS SOD
                                        ON SOD."DON_DAT_HANG_CHI_TIET_ID" = TOI."DON_DAT_HANG_ID"
                                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS SVD
                                        ON SOD."id" = SVD."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = SVD."MA_HANG_ID"
                                    INNER JOIN stock_ex_nhap_xuat_kho IO ON IO.id = SVD."NHAP_XUAT_ID"
                                WHERE IO."LOAI_CHUNG_TU" = 2020
                                GROUP BY
                                    TOI."DON_DAT_HANG_ID",
                                    SOD."id",
                                    SOD."MA_HANG_ID"

                                /*Lấy số đã giao từ chứng từ bán trả lại*/
                                UNION ALL
                                SELECT
                                    TOI."DON_DAT_HANG_ID"
                                    , SOD."id"                                                          AS "DON_DAT_HANG_CHI_TIET_ID"
                                    , SOD."MA_HANG_ID"
                                    , (-1) * COALESCE(SUM(ROUND(cast((CASE WHEN ((SOD."DVT_ID" ISNULL AND INID."DVT_ID" ISNULL)
                                                                                OR
                                                                                (SOD."DVT_ID" NOTNULL AND INID."DVT_ID" NOTNULL AND
                                                                                SOD."DVT_ID" = INID."DVT_ID"))
                                    THEN INID."SO_LUONG"
                                                                    ELSE (CASE WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                                                    '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                                                        THEN ROUND(
                                                                            cast((INID."SO_LUONG" *
                                                                                    SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                AS NUMERIC), format_so)
                                                                            WHEN (SOD."TOAN_TU_QUY_DOI" = '0' AND
                                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" <>
                                                                                0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                                                THEN ROUND(cast((INID."SO_LUONG_THEO_DVT_CHINH" /
                                                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                                AS
                                                                                                NUMERIC), format_so)
                                                                            ELSE INID."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                                            END)
                                                                    END) AS NUMERIC), format_so)), 0) AS "SO_LUONG_DA_GIAO"
                                    , (-1) * COALESCE(SUM(INID."SO_LUONG"),
                                                    0)                                                AS "SO_LUONG_DA_GIAO_THEO_DVT_CHINH"
                                FROM TMP_DON_DAT_HANG AS TOI
                                    INNER JOIN account_ex_don_dat_hang_chi_tiet AS SOD
                                        ON SOD."DON_DAT_HANG_CHI_TIET_ID" = TOI."DON_DAT_HANG_ID"
                                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS INID
                                        ON SOD."id" = INID."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = INID."MA_HANG_ID"
                                    INNER JOIN stock_ex_nhap_xuat_kho INI ON INI.id = INID."NHAP_XUAT_ID"
                                WHERE INI."LOAI_CHUNG_TU" = 2013
                                GROUP BY
                                    TOI."DON_DAT_HANG_ID",
                                    SOD."id",
                                    SOD."MA_HANG_ID"
                            ) AS T
                        GROUP BY
                            T."DON_DAT_HANG_ID",
                            T."DON_DAT_HANG_CHI_TIET_ID",
                            T."MA_HANG_ID"
                ;

                --     SELECT * FROM TMP_KET_QUA
                /*cập nhật vào đơn đặt hàng số lượng đã giao = Số lượng đã giao từ năm trước + số lượng đã giao trên các chứng từ phát sinh*/
           UPDATE	account_ex_don_dat_hang_chi_tiet SOD
            SET		"SO_LUONG_DA_GIAO_PX" = COALESCE(SOD."SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG", 0) + COALESCE(TSOD."SO_LUONG_DA_GIAO", 0)
--                     "SO_LUONG_DA_GIAO_BAN_HANG_THEO_DVT_CHINH" = COALESCE(SOD."SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG_THEO_DVT_CHINH", 0) + COALESCE(TSOD."SO_LUONG_DA_GIAO_THEO_DVT_CHINH", 0)
            FROM	account_ex_don_dat_hang_chi_tiet SOD1 LEFT JOIN TMP_KET_QUA AS TSOD on SOD1.id = TSOD."DON_DAT_HANG_CHI_TIET_ID"
            WHERE   SOD.id = SOD1.id
                    AND  exists(SELECT  FROM TMP_DON_DAT_HANG AS TOI WHERE   SOD."DON_DAT_HANG_CHI_TIET_ID" = TOI."DON_DAT_HANG_ID" FETCH FIRST 1 ROW  ONLY );

            END $$
            ;

            SELECT *
            FROM TMP_KET_QUA
            ;

        """  
        cr = self.env.cr

        return cr.execute(query, params)