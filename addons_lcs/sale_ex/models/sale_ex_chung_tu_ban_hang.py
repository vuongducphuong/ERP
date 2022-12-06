# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError , UserError
from odoo.addons import decimal_precision
import json
import ast

class SALE_DOCUMENT(models.Model):
    _name = 'sale.document'
    _description = 'Chứng từ bán hàng'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"


    @api.depends('SALE_DOCUMENT_LINE_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien_hang = tong_tien_thue_gtgt = tong_tien_chiet_khau = tong_tien_thanh_toan =0.0
            tong_tien_hang_qd = 0.0
            tong_tien_chiet_khau_qd = 0.0
            tong_tien_thue_gtgt_qd = 0.0
            tong_tien_thanh_toan_qd = 0.0
            for line in order.SALE_DOCUMENT_LINE_IDS:
                tong_tien_hang += line.THANH_TIEN
                tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
                tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt - tong_tien_chiet_khau

                tong_tien_hang_qd += line.THANH_TIEN_QUY_DOI
                tong_tien_chiet_khau_qd += line.TIEN_CK_QUY_DOI
                tong_tien_thue_gtgt_qd += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_thanh_toan_qd = tong_tien_hang_qd + tong_tien_thue_gtgt_qd - tong_tien_chiet_khau_qd


            order.update({
                'TONG_TIEN_HANG': tong_tien_hang,
                'TONG_TIEN_THUE_GTGT': tong_tien_thue_gtgt,
                'TONG_TIEN_CHIET_KHAU': tong_tien_chiet_khau,
                'TONG_TIEN_THANH_TOAN': tong_tien_thanh_toan,

                'TONG_TIEN_HANG_QĐ': tong_tien_hang_qd,
                'TONG_TIEN_CHIET_KHAU_QĐ': tong_tien_chiet_khau_qd,
                'TONG_TIEN_THUE_GTGT_QĐ': tong_tien_thue_gtgt_qd,
                'TONG_TIEN_THANH_TOAN_QĐ': tong_tien_thanh_toan_qd,
            })
    
    name = fields.Char(string='Name', related="SO_CHUNG_TU", )
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_KHO_ID = fields.Many2one('so.kho', ondelete='set null')
    SO_BAN_HANG_ID = fields.Many2one('so.ban.hang', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    LOAI_CHUNG_TU_CTBH = fields.Selection([('CUSTOMER_INVOICE', 'Customer Invoice'), ('VENDOR_BILL', 'Vendor Bill'), ('CUSTOMER_CREDIT_NOTE', 'Customer Credit Note'), ('VENDOR_CREDIT_NOTE', 'Vendor Credit Note'), ('VENDOR_CREDIT_NOTE', 'Vendor Credit Note'), ], string='Loại chứng từ', help='Loại chứng từ')
    LOAI_NGHIEP_VU = fields.Selection([('TRONG_NUOC', '1. Bán hàng hóa, dịch vụ trong nước'), ('XUAT_KHAU', '2. Bán hàng xuất khẩu'), ('DAI_LY', '3. Bán hàng đại lý đúng giá'), ('UY_THAC', '4. Bán hàng ủy thác xuất khẩu'), ], string='Loại nghiệp vụ', help='Loại nghiệp vụ',default='TRONG_NUOC',required=True)
    THU_TIEN_NGAY = fields.Boolean(string='Thu tiền ngay', help='Thu tiền ngay', default_by_last=True)
    LOAI_THANH_TOAN = fields.Selection([('TIEN_MAT', 'Tiền mặt'), ('CHUYEN_KHOAN', 'Chuyển khoản'), ], string='Loại thanh toán', help='Loại thanh toán',default='TIEN_MAT')
    # LOAI_GIAM_TRU = fields.Selection([('GIAM_TRU_CONG_NO', 'Giảm trừ công nợ'), ('TRA_LAI_TIEN_MAT', 'Trả lại tiền mặt'), ], string='Loại giảm trừ', help='Loại giảm trừ')
    DON_GIA_NHAP_KHO = fields.Selection([('THU_CONG', 'Thủ công'), ('TU_DONG', 'Tự động'), ], string='Đơn giá nhập kho', help='Đơn giá nhập kho')
    KIEM_PHIEU_NHAP_XUAT_KHO = fields.Boolean(string='Kiêm phiếu nhập xuất kho', help='Kiêm phiếu nhập xuất kho', default_by_last=True)
    LAP_KEM_HOA_DON = fields.Boolean(string='Lập kèm hóa đơn', help='Lập kèm hóa đơn', default_by_last=True)
    DA_LAP_HOA_DON = fields.Boolean(string='Đã lập hóa đơn', help='Đã lập hóa đơn',default=False)
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng', domain=[('LA_KHACH_HANG','=',True)], track_visibility='onchange')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    NGUOI_NOP_NHAN = fields.Char(string='Người nộp/nhận', help='Người nộp/nhận',related='NGUOI_LIEN_HE',storre=False)
    NGUOI_GIAO_NHAN_HANG = fields.Char(string='Người giao/nhận hàng', help='Người giao/nhận hàng')
    NGUOI_LIEN_HE = fields.Char(string='Người liên hệ', help='Người liên hệ')
    NGUOI_MUA_HANG = fields.Char(string='Người mua hàng', help='Người mua hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    NOP_VAO_TK_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Nộp vào tk', help='Nộp vào tk')
    # Đây là tài khoản ngân hàng của khách hàng
    TK_NGAN_HANG = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='TK ngân hàng', help='TK ngân hàng')
    HINH_THUC_TT = fields.Selection([('TIEN_MAT', 'Tiền mặt'), ('CHUYEN_KHOAN', 'Chuyển khoản'), ('TIEN_MAT_CHUYEN_KHOAN', 'TM/CK'), ], string='Hình thức tt', help='Hình thức tt')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    DIEN_GIAI_GGHB = fields.Char(string='Diễn giải', help='Diễn giải')
    LY_DO_NHAP_XUAT = fields.Char(string='Lý do nhập/xuất', help='Lý do nhập/xuất', default="Xuất kho bán hàng")
    TK_THUE_XK_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='Tài khoản thuế xuất khẩu', help='Tài khoản thuế xuất khẩu')
    DON_VI_GIAO_DAI_LY_ID = fields.Many2one('res.partner', string='Đơn vị giao đại lý', help='Đơn vị giao đại lý')
    DON_VI_UY_THAC_ID = fields.Many2one('res.partner', string='Đơn vị ủy thác', help='Đơn vị ủy thác',related='DON_VI_GIAO_DAI_LY_ID')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nv bán hàng', help='Nv bán hàng', domain=[('LA_NHAN_VIEN','=',True)])
    KEM_THEO_CHUNG_TU_GOC = fields.Char(string='Kèm theo CTG', help='Kèm theo chứng từ gốc')
    THAM_CHIEU_ID = fields.Char(string='Tham chiếu', help='Tham chiếu',readonly='True')
    DIEU_KHOAN_TT_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản TT', help='Điều khoản thanh toán')
    SO_NGAY_DUOC_NO = fields.Integer(string='Số ngày được nợ', help='Số ngày được nợ')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now)
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    CHI_TIET_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Chi tiết', help='Chi tiết')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng',compute='tinh_tong_tien', store=True, currency_field='currency_id')
    TONG_TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',compute='tinh_tong_tien', store=True, currency_field='currency_id')
    TONG_TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế gtgt', help='Tiền thuế gtgt',compute='tinh_tong_tien', store=True, currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền TT', help='Tổng tiền thanh toán',compute='tinh_tong_tien', store=True, currency_field='currency_id', track_visibility='onchange')   
    TONG_TIEN_HANG_QĐ = fields.Monetary(string='', help='Tổng tiền hàng',compute='tinh_tong_tien', store=True, currency_field='base_currency_id')
    TONG_TIEN_CHIET_KHAU_QĐ = fields.Monetary(string='', help='Tiền chiết khấu',compute='tinh_tong_tien', store=True, currency_field='base_currency_id')
    TONG_TIEN_THUE_GTGT_QĐ = fields.Monetary(string='', help='Tiền thuế gtgt',compute='tinh_tong_tien', store=True, currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QĐ = fields.Monetary(string='', help='Tổng tiền thanh toán quy đổi',compute='tinh_tong_tien', store=True, currency_field='base_currency_id')
    IN_KEM_BAN_KE = fields.Boolean(string='In kèm bảng kê', help='In kèm bảnh kê')
    SO = fields.Char(string='Số', help='Số')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    TEN_MAT_HANG_CHUNG = fields.Char(string='Tên mặt hàng chung', help='Tên mặt hàng chung')
    DIA_DIEM_GIAO_HANG_ID = fields.Char(string='Địa điểm GH', help='Địa điểm giao hàng')
    DIEU_KHOAN_KHAC = fields.Text(string='Điều khoản khác', help='Điều khoản khác')
    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng')
    NGAY_HOP_DONG = fields.Date(string='Ngày hợp đồng', help='Ngày hợp đồng',default=fields.Datetime.now)
    DIA_DIEM_NHAN_HANG = fields.Char(string='Địa điểm NH', help='Địa điểm nhận hàng')
    SO_VAN_DON = fields.Char(string='Số vận đơn', help='Số vận đơn')
    SO_CONTAINER = fields.Char(string='Số container', help='Số container')
    DV_VAN_CHUYEN = fields.Char(string='Đv vận chuyển', help='Đv vận chuyển')
    TEN_TK = fields.Char(string='Tên TK', help='Tên TK')
    TIEN_CHIET_KHAU = fields.Float(string ='Tiền chiết khấu',help='Tiền chiết khấu')
    TIEN_THUE_GTGT = fields.Float(string ='Tiền thuế GTGT',help='Tiền thuế GTGT')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh(),oldname='LOAI_TIEN_ID')
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    LOAI_CT = fields.Selection([('CTBH', 'Chứng từ bán hàng'), ('GGHB', 'Giảm giá hàng bán')], string='Loại chứng từ')    
    SALE_DOCUMENT_LINE_IDS = fields.One2many('sale.document.line', 'SALE_DOCUMENT_ID', string='Chi tiết chứng từ',required=True, copy=True)
    TEN_DON_VI = fields.Char(string='Tên đơn vị giao đại lý', help='Tên đơn vị giao đại lý')
    TEN_DON_VI_UY_THAC = fields.Char(string='Tên đơn ủy thác', help='Tên đơn ủy thác',related='TEN_DON_VI')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', compute='_compute_SO_CHUNG_TU', store=True)
    SO_CHUNG_TU_GHI_NO = fields.Char(string='Số chứng từ ghi nợ', help='Số chứng từ ghi nợ', auto_num='sale_ex_chung_tu_ban_hang_ex_SO_CHUNG_TU_GHI_NO')
    SO_CHUNG_TU_PHIEU_THU_TIEN_MAT = fields.Char(string='Số chứng từ phiếu thu', help='Số chứng từ phiếu thu', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_PHIEU_THU')
    SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN = fields.Char(string='Số chứng từ', help='Số chứng từ phiếu thu', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_THU_TIEN_GUI')
    SO_CHUNG_TU_PHIEU_XUAT = fields.Char(string='Số chứng từ phiếu xuất', help='Số chứng từ phiếu xuất', auto_num='stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_XUAT_KHO')
    SO_CHUNG_TU_HOA_DON = fields.Char(string='Số hóa đơn', help='Số chứng từ hóa đơn', auto_num='sale_ex_hoa_don_ban_hang_SO_HOA_DON')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn',)

    # Task 3513
    CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH = fields.Boolean()
    TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG = fields.Boolean()
    
    # SO_CHUNG_TU_GIAM_GIA = fields.Char(string='Số chứng từ giảm giá', help='Số chứng từ giảm giá', auto_num='sale_ex_chung_tu_ban_hang_ex_SO_CHUNG_TU_GIAM_GIA')
    # SO_PHIEU_CHI_GGHB = fields.Char(string='Số phiếu chi', help='Số phiếu chi', auto_num='sale_ex_chung_tu_ban_hang_ex_SO_PHIEU_CHI')
    # Updated 2019-04-17 by anhtuan: Relation với phiếu xuất và hóa đơn là Many2many. Không sinh ra phiếu thu
    PHIEU_XUAT_IDS = fields.Many2many('stock.ex.nhap.xuat.kho', 'sale_ex_document_outward_rel')#, 'SALE_DOCUMENT_ID', 'SALE_OUTWARD_ID', string='Phiếu xuất kho')
    HOA_DON_IDS = fields.Many2many('sale.ex.hoa.don.ban.hang', 'sale_ex_document_invoice_rel')#, 'SALE_DOCUMENT_ID', 'SALE_INVOICE_ID', string='Hóa đơn', help='Hóa đơn')
    PHAN_BO_CHIET_KHAU_JSON = fields.Text()
    LAP_KEM_LENH_LAP_RAP = fields.Boolean('Lập kèm lệnh lắp ráp', default_by_last=True)
    LAP_TU_DON_DAT_HANG_IDS = fields.Many2many('account.ex.don.dat.hang', string='Từ đơn hàng')

    @api.onchange('LAP_TU_DON_DAT_HANG_IDS')
    def _onchange_LAP_TU_DON_DAT_HANG_IDS(self):
        self.SALE_DOCUMENT_LINE_IDS = []
        dict_so_luong_ton = {}
        ds_don_hang_hop_le = [[5]]
        ds_don_hang_khong_hop_le = ''
        default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU)
        for record in self.LAP_TU_DON_DAT_HANG_IDS:
            self.DOI_TUONG_ID = record.KHACH_HANG_ID.id 
            self.TEN_KHACH_HANG = record.TEN_KHACH_HANG
            self.MA_SO_THUE = record.MA_SO_THUE
            self.DIA_CHI = record.DIA_CHI
            self.DIEN_GIAI = record.DIEN_GIAI
            self.LY_DO_NHAP_XUAT = 'Xuất kho bán hàng '+ str(record.TEN_KHACH_HANG)
            new_document_line = []
            co_the_tao_ctbh = True
            ten_hang_khong_hop_le = ''
            for line in record.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                dien_giai_thue = ''
                kho_id = 0
                tk_gia_von_id = 0
                if line.MA_HANG_ID:
                    ten_san_pham = line.MA_HANG_ID.TEN
                    dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                    kho_id = line.MA_HANG_ID.TAI_KHOAN_KHO_ID.id
                    if not line.MA_HANG_ID.CHO_PHEP_XUAT_QUA_SL_TON:
                        ma_hang_id = line.MA_HANG_ID.id
                        if ma_hang_id not in dict_so_luong_ton:
                            dict_so_luong_ton[ma_hang_id] = line.MA_HANG_ID.lay_so_luong_ton_tat_ca_kho(record.NGAY_DON_HANG + ' 00:00:00', record.NGAY_DON_HANG + ' 23:59:59',record.CHI_NHANH_ID.id)
                        dict_so_luong_ton[ma_hang_id] -= line.SO_LUONG
                        if dict_so_luong_ton[ma_hang_id] < 0:
                            co_the_tao_ctbh = False
                            ten_hang_khong_hop_le += ''.join(['+ ',line.MA_HANG_ID.MA, ' - ',line.MA_HANG_ID.TEN,'\n'])
                            continue
                tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                if tk_gia_von_632:
                    tk_gia_von_id = tk_gia_von_632.id

                new_document_line += [{
                    'MA_HANG_ID': line.MA_HANG_ID.id,
                    'TEN_HANG': line.TEN_HANG,
                    'DIEN_GIAI_THUE': dien_giai_thue,
                    'KHO_ID': line.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                    'TK_NO_ID': default.get('TK_NO_ID'),
                    'TK_CO_ID': default.get('TK_CO_ID'),
                    'TK_THUE_GTGT_ID': default.get('TK_THUE_GTGT_ID'),
                    'TK_CHIET_KHAU_ID': default.get('TK_CHIET_KHAU_ID'),
                    'TK_KHO_ID': kho_id,
                    'TK_GIA_VON_ID': tk_gia_von_id,
                    'DON_GIA': line.DON_GIA,
                    self.env['sale.document.line'].get_field_so_luong(): line.SO_LUONG,
                    'THANH_TIEN': line.THANH_TIEN,
                    'THANH_TIEN_QUY_DOI': line.THANH_TIEN_QUY_DOI,
                    'DVT_ID': line.DVT_ID.id,
                    'DON_VI_ID':  line.MA_HANG_ID.CHI_NHANH_ID,
                    'THUE_GTGT_ID':  line.PHAN_TRAM_THUE_GTGT_ID,
                    'TIEN_THUE_GTGT':  line.TIEN_THUE_GTGT,
                    'TIEN_THUE_GTGT_QUY_DOI':  line.TIEN_THUE_GTGT_QUY_DOI,
                    'DON_DAT_HANG_CHI_TIET_ID':  line.id,
                    'DON_DAT_HANG_ID':  record.id,
                }]
            if co_the_tao_ctbh:
                ds_don_hang_hop_le += [[4, record.id]]
                for new_line in new_document_line:
                    self.SALE_DOCUMENT_LINE_IDS += self.env['sale.document.line'].new(new_line)
            else:
                ds_don_hang_khong_hop_le += ''.join(['- ',record.SO_DON_HANG,'\n',ten_hang_khong_hop_le])
        self.LAP_TU_DON_DAT_HANG_IDS = ds_don_hang_hop_le
        if ds_don_hang_khong_hop_le:
            msg = ''.join(['Các đơn đặt hàng dưới đây không đủ số lượng hàng trong kho để thực hiện xuất: \n',ds_don_hang_khong_hop_le])
            return {'warning': {'title': 'Đơn đặt hàng không đủ số lượng tồn', 'message': msg}}

    @api.model
    def uivalidate(self, option=None):
        if self.KIEM_PHIEU_NHAP_XUAT_KHO == True:
            if self.SO_CHUNG_TU_PHIEU_XUAT == False:
                return "<Số phiếu xuất> Không được bỏ trống"
        if self.LAP_KEM_HOA_DON == True:
            if self.SO_HOA_DON == False:
                return "<Số hóa đơn> Không được bỏ trống"

    @api.onchange('PHAN_BO_CHIET_KHAU_JSON')
    def _onchange_PHAN_BO_CHIET_KHAU_JSON(self):
        if self.PHAN_BO_CHIET_KHAU_JSON:
            du_lieu_phan_bo = ast.literal_eval(self.PHAN_BO_CHIET_KHAU_JSON)
            hinh_thuc_chiet_khau = du_lieu_phan_bo.get('HINH_THUC_CHIET_KHAU')
            phan_bo_chiet_khau_ids = du_lieu_phan_bo.get('SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS')

            dict_phan_bo = {}
            if phan_bo_chiet_khau_ids:
                for phan_bo in phan_bo_chiet_khau_ids:
                    key = str(phan_bo.get('MA_HANG_ID')) + ',' + str(phan_bo.get('INDEX'))
                    if key not in dict_phan_bo:
                        dict_phan_bo[key] = []
                    dict_phan_bo[key] = phan_bo
            if hinh_thuc_chiet_khau == 'GHI_DE':
                if self.SALE_DOCUMENT_LINE_IDS:
                    for line in self.SALE_DOCUMENT_LINE_IDS:
                        key_ban_hang_chi_tiet = str(line.MA_HANG_ID.id) + ',' + str(line.INDEX)
                        if key_ban_hang_chi_tiet in dict_phan_bo:
                            chi_tiet = dict_phan_bo[key_ban_hang_chi_tiet]
                            line.TY_LE_CK = chi_tiet.get('TY_LE_PHAN_BO')
                            line.TIEN_CHIET_KHAU = chi_tiet.get('TIEN_CHIET_KHAU')
                            line.TIEN_CK_QUY_DOI = line.TIEN_CHIET_KHAU*line.TY_GIA
            elif hinh_thuc_chiet_khau == 'CONG_THEM':
                if self.SALE_DOCUMENT_LINE_IDS:
                    for line in self.SALE_DOCUMENT_LINE_IDS:
                        key_ban_hang_chi_tiet = str(line.MA_HANG_ID.id) + ',' + str(line.INDEX)
                        if key_ban_hang_chi_tiet in dict_phan_bo:
                            chi_tiet = dict_phan_bo[key_ban_hang_chi_tiet]
                            if line.TY_LE_CK + chi_tiet.get('TY_LE_PHAN_BO') > 100:
                                ty_le_ck = 100
                            else:
                                ty_le_ck = line.TY_LE_CK + chi_tiet.get('TY_LE_PHAN_BO')
                            if line.TIEN_CHIET_KHAU + chi_tiet.get('TIEN_CHIET_KHAU') > line.THANH_TIEN:
                                tien_ck = line.THANH_TIEN
                            else:
                                tien_ck = line.TIEN_CHIET_KHAU + chi_tiet.get('TIEN_CHIET_KHAU')
                            line.TY_LE_CK = ty_le_ck
                            line.TIEN_CHIET_KHAU = tien_ck
                            line.TIEN_CK_QUY_DOI = line.TIEN_CHIET_KHAU*line.TY_GIA
            self.tinh_tong_tien()
        
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU

    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        for line in self.SALE_DOCUMENT_LINE_IDS:
            line.tinh_tien_quy_doi()

    #quanhm: trùng code với khi import
    @api.depends('IS_PHIEU_THU','SO_CHUNG_TU_GHI_NO','SO_CHUNG_TU_PHIEU_THU_TIEN_MAT','SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN')
    def _compute_SO_CHUNG_TU(self):
        for record in self:
            if record.IS_PHIEU_THU:
                record.SO_CHUNG_TU = record.SO_CHUNG_TU_PHIEU_THU_TIEN_MAT if record.LOAI_THANH_TOAN == 'TIEN_MAT' else record.SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN
            else:
                record.SO_CHUNG_TU = record.SO_CHUNG_TU_GHI_NO

    # _sql_constraints = [
    #     ('SO_CHUNG_TU_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
    # ]

    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            if record.THU_TIEN_NGAY:
                if record.LOAI_THANH_TOAN == 'TIEN_MAT':
                    record.validate_unique_thu_chi_tien(record.SO_CHUNG_TU_PHIEU_THU_TIEN_MAT)
                elif record.LOAI_THANH_TOAN == 'CHUYEN_KHOAN':
                    record.validate_unique_thu_chi_tien(record.SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN)
    @api.model
    def validate_so_hoa_don(self): #Mạnh sửa bug1989
        if self.LAP_KEM_HOA_DON == True and not self.SO_HOA_DON:
            raise UserError("<Số hóa đơn> không được bỏ trống!")

    @api.model
    def create(self, vals):
        result = super(SALE_DOCUMENT, self).create(vals)
        # result.validate_so_hoa_don() #Mạnh sửa bug1989 Tùng commnet đợi xử lý task 2225
        result.validate_unique_so_chung_tu({self._name.replace('.','_'): 'SO_CHUNG_TU'}, 'SO_CHUNG_TU')
        result.validate_thu_chi_tien()
        if not self._context.get('fromMS'):#vals.get('TAO_TU_IMPORT'):
            self.create_references(result)
        if self.SALE_DOCUMENT_LINE_IDS:
            self.up_date_don_dat_hang()
        # Cập nhật CHUNG_TU_BAN_HANG_ID cho đơn đặt hàng
        don_gang_ids = result.LAP_TU_DON_DAT_HANG_IDS.ids
        if don_gang_ids:
            self.env.cr.execute('UPDATE account_ex_don_dat_hang SET "CHUNG_TU_BAN_HANG_ID"=%s WHERE (id = any (ARRAY%s))' % (result.id, don_gang_ids))
        return result

    def create_references(self, sale_doc):
        if sale_doc.KIEM_PHIEU_NHAP_XUAT_KHO:
            xuat_kho_chi_tiet_ids = []
            for line in sale_doc.SALE_DOCUMENT_LINE_IDS:
                xuat_kho_chi_tiet_ids += [(0,0,{
                    'MA_HANG_ID': line.MA_HANG_ID.id,
                    'TEN_HANG': line.TEN_HANG,
                    'TK_NO_ID': line.TK_GIA_VON_ID.id,
                    'TK_CO_ID': line.TK_KHO_ID.id,
                    'KHO_ID': line.KHO_ID.id,
                    'DVT_ID': line.DVT_ID.id,
                    'SO_LUONG': line.SO_LUONG,
                    'SO_LUONG_YEU_CAU': line.SO_LUONG_YEU_CAU,
                    'DON_GIA': line.DON_GIA,
                    'THANH_TIEN': line.THANH_TIEN,
                    'SALE_DOCUMENT_LINE_IDS': [(4, line.id)]
                })]
            vals = {
                'type': 'XUAT_KHO',
                'SO_CHUNG_TU': sale_doc.SO_CHUNG_TU_PHIEU_XUAT,
                'NGAY_CHUNG_TU': sale_doc.NGAY_CHUNG_TU,
                'NGAY_HACH_TOAN': sale_doc.NGAY_HACH_TOAN,
                'DOI_TUONG_ID': sale_doc.DOI_TUONG_ID.id if sale_doc.DOI_TUONG_ID else None,
                'LOAI_CHUNG_TU': sale_doc.LOAI_CHUNG_TU,
                'NGUOI_NHAN_TEXT': sale_doc.NGUOI_GIAO_NHAN_HANG,
                'LY_DO_XUAT': sale_doc.LY_DO_NHAP_XUAT,
                'currency_id': sale_doc.currency_id.id,
                'TY_GIA': sale_doc.TY_GIA,
                'SOURCE_ID': self._name + ',' + str(sale_doc.id),
                'SALE_DOCUMENT_IDS': [(4, sale_doc.id)],
                'CHI_TIET_IDS': xuat_kho_chi_tiet_ids,
            }
            phieu_xuat = sale_doc.find_reference('stock.ex.nhap.xuat.kho')
            if phieu_xuat:
                phieu_xuat.CHI_TIET_IDS.unlink()
                phieu_xuat.write(vals)
            else:
                self.env['stock.ex.nhap.xuat.kho'].create(vals)

        # Lập kèm hóa đơn
        loai_chung_tu_hoa_don = False
        if sale_doc.LOAI_NGHIEP_VU == 'TRONG_NUOC':
            loai_chung_tu_hoa_don = 3560
        elif sale_doc.LOAI_NGHIEP_VU == 'XUAT_KHAU':
            loai_chung_tu_hoa_don = 3561
        elif sale_doc.LOAI_NGHIEP_VU == 'DAI_LY':
            loai_chung_tu_hoa_don = 3562
        elif sale_doc.LOAI_NGHIEP_VU == 'UY_THAC':
            loai_chung_tu_hoa_don = 3563
        if sale_doc.LAP_KEM_HOA_DON:
            vals = {
                'SO_HOA_DON': sale_doc.SO_HOA_DON,
                'NGAY_HOA_DON': sale_doc.NGAY_HOA_DON,
                'KY_HIEU_HD': sale_doc.KY_HIEU_HD,
                'MAU_SO_HD_ID': sale_doc.MAU_SO_HD_ID.id,
                'DOI_TUONG_ID': sale_doc.DOI_TUONG_ID.id,
                'TEN_KHACH_HANG': sale_doc.TEN_KHACH_HANG,
                'LOAI_CHUNG_TU': loai_chung_tu_hoa_don,
                'currency_id': sale_doc.currency_id.id,
                'TY_GIA': sale_doc.TY_GIA,
                'DA_HACH_TOAN': True,
                'SOURCE_ID': self._name + ',' + str(sale_doc.id),
                'SALE_DOCUMENT_IDS': [(4, sale_doc.id)],
            }
            hoa_don = sale_doc.upsert_reference('sale.ex.hoa.don.ban.hang', vals)
            sale_doc.SALE_DOCUMENT_LINE_IDS.write({'HOA_DON_ID': hoa_don.id})

        if sale_doc.LAP_KEM_LENH_LAP_RAP:
            sale_doc.lap_kem_lenh_lap_rap()
        
    def lap_kem_lenh_lap_rap(self):
        for line in self.SALE_DOCUMENT_LINE_IDS:
            line.with_context({
                'SOURCE_ID': (',').join([self._name,str(self.id)]),
                'SO_CHUNG_TU': self.SO_CHUNG_TU,
                'NGAY_CHUNG_TU': self.NGAY_CHUNG_TU,
            }).tao_lenh_lap_rap()
            # lap_rap_chi_tiet_ids = []
            # for nvl in line.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
            #     if nvl.MA_NGUYEN_VAT_LIEU_ID:
            #         lap_rap_chi_tiet_ids += [(0,0,{
            #         'MA_HANG_ID': nvl.MA_NGUYEN_VAT_LIEU_ID.id,
            #         'TEN_HANG': nvl.TEN_NGUYEN_VAT_LIEU,
            #         'KHO_ID': nvl.MA_NGUYEN_VAT_LIEU_ID.KHO_NGAM_DINH_ID.id,
            #         'DVT_ID': nvl.DVT_ID.id,
            #         'SO_LUONG': nvl.SO_LUONG * line.SO_LUONG,
            #         # Lấy đơn giá/thành tiền quy đổi, do lệnh lắp ráp không có loại tiền
            #         # Xem xét lại việc tính đơn giá và thành tiền, vì trường này là readonly
            #         'DON_GIA': 0, #nvl.GIA_VON * line.SO_LUONG,
            #         'THANH_TIEN': 0, #nvl.THANH_TIEN * line.SO_LUONG,
            # })]
            # lenh_lap_rap = {
            #     'SOURCE_ID': (',').join([self._name,str(self.id)]),
            #     'LAP_RAP_THAO_DO': 'LAP_RAP',
            #     'DIEN_GIAI': 'Lập từ chứng từ bán hàng %s' % self.SO_CHUNG_TU,
            #     'HANG_HOA_ID': line.MA_HANG_ID.id,
            #     'TEN_HANG_HOA': line.TEN_HANG,
            #     'NGAY': self.NGAY_CHUNG_TU,
            #     'DVT_ID': line.DVT_ID.id,
            #     'SO_LUONG': line.SO_LUONG,
            #     # 'DON_GIA': line.DON_GIA, 
            #     # 'THANH_TIEN': line.THANH_TIEN_QUY_DOI,
            #     'SO': self.env['ir.sequence'].next_by_code('stock_ex_lap_rap_thao_do_SO'),
            #     'STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS': lap_rap_chi_tiet_ids,
            # }
            # lap_rap = self.env['stock.ex.lap.rap.thao.do'].create(lenh_lap_rap)
            # # Cập nhật lại LAP_RAP_ID cho chứng từ bán hàng chi tiết
            # line.LAP_RAP_ID = lap_rap.id

            # Tạo phiếu xuất kho nguyên vật liệu
            # xuat_kho_lap_rap_chi_tiet = []
            # default_2024 = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].lay_tai_khoan_ngam_dinh(2024)
            # for lap_rap_thao_ro_dt_ct in lap_rap.STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS:
            #     xuat_kho_lap_rap_chi_tiet +=[(0,0,{
            #         'MA_HANG_ID':lap_rap_thao_ro_dt_ct.MA_HANG_ID.id,
            #         'TEN_HANG'  :lap_rap_thao_ro_dt_ct.TEN_HANG,
            #         'DVT_ID':lap_rap_thao_ro_dt_ct.DVT_ID.id,
            #         'SO_LUONG'  :lap_rap_thao_ro_dt_ct.SO_LUONG,
            #         'DON_GIA_VON'  :lap_rap_thao_ro_dt_ct.DON_GIA,
            #         'TIEN_VON'  :lap_rap_thao_ro_dt_ct.THANH_TIEN,
            #         'LENH_LR_TD_ID'  :lap_rap.id,
            #         'KHO_ID'  :lap_rap_thao_ro_dt_ct.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
            #         'TK_NO_ID'  : default_2024.get('TK_NO_ID'),
            #         'TK_CO_ID':  default_2024.get('TK_CO_ID') or lap_rap_thao_ro_dt_ct.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
            #     })]
            # so_chung_tu_xk = self.env['ir.sequence'].next_by_code('stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_XUAT_KHO')
            # xuat_kho_de_lap_rap = {
            #     'name': so_chung_tu_xk,
            #     'SO_CHUNG_TU': so_chung_tu_xk,
            #     'LOAI_XUAT_KHO': 'SAN_XUAT',
            #     'LOAI_CHUNG_TU_2': 2024,
            #     'LOAI_CHUNG_TU': 2024,
            #     'type': 'XUAT_KHO',
            #     'LY_DO_XUAT': 'Xuất kho để lắp ráp, theo chứng từ bán hàng %s' % self.SO_CHUNG_TU,
            #     'CHI_TIET_IDS': xuat_kho_lap_rap_chi_tiet,
            # }
            # xuat_kho_id = self.env['stock.ex.nhap.xuat.kho'].create(xuat_kho_de_lap_rap)
            
            # Tạo phiếu nhập kho thành phẩm
            # default_2011 = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].lay_tai_khoan_ngam_dinh(2011)
            # nhap_kho_lap_rap_chi_tiet = [(0,0,{
            #     'MA_HANG_ID':lap_rap.HANG_HOA_ID.id,
            #     'TEN_HANG'  :lap_rap.TEN_HANG_HOA,
            #     'DVT_ID':lap_rap.DVT_ID.id,
            #     'SO_LUONG'  :lap_rap.SO_LUONG,
            #     'DON_GIA_VON'  :lap_rap.DON_GIA,
            #     'TIEN_VON'  :lap_rap.THANH_TIEN,
            #     'LENH_LR_TD_ID'  :lap_rap.id,
            #     'KHO_ID'  :lap_rap.HANG_HOA_ID.KHO_NGAM_DINH_ID.id,
            #     'TK_NO_ID'  : default_2011.get('TK_NO_ID') or lap_rap.HANG_HOA_ID.TAI_KHOAN_KHO_ID.id,
            #     'TK_CO_ID':  default_2011.get('TK_CO_ID'),
            # })]
            # so_chung_tu_nk = self.env['ir.sequence'].next_by_code('stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_NHAP_KHO')
            # nhap_kho_tu_lap_rap = {
            #     'name': so_chung_tu_nk,
            #     'SO_CHUNG_TU': so_chung_tu_nk,
            #     'LOAI_NHAP_KHO': 'THANH_PHAM',
            #     'LOAI_CHUNG_TU_2': 2011,
            #     'LOAI_CHUNG_TU': 2011,
            #     'type': 'NHAP_KHO',
            #     'DIEN_GIAI': 'Nhập kho từ lắp ráp, theo chứng từ bán hàng %s' % self.SO_CHUNG_TU,
            #     'CHI_TIET_IDS': nhap_kho_lap_rap_chi_tiet,
            # }
            # nhap_kho_id = self.env['stock.ex.nhap.xuat.kho'].create(nhap_kho_tu_lap_rap)
            # lap_rap.write({'THAM_CHIEU': [(6,0, (xuat_kho_id.id, nhap_kho_id.id))]})

    @api.multi
    def xem_ds_lenh_lap_rap(self):
        self.ensure_one()
        ref = self.find_reference('stock.ex.lap.rap.thao.do', None)
        action = self.env.ref('stock_ex.open_menu_stock_ex_lap_rap_thao_do').read()[0]
        if len(ref) > 1:
            action['domain'] = [('id', 'in', ref.ids)]
        elif len(ref) == 1:
            action['views'] = [(self.env.ref('stock_ex.view_stock_ex_lap_rap_thao_do_form').id, 'form')]
            action['res_id'] = ref.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    @api.multi
    def write(self, values):
        if values.get('LAP_TU_DON_DAT_HANG_IDS'):
            for record in self:
                self.env.cr.execute("""
                    UPDATE account_ex_don_dat_hang SET "CHUNG_TU_BAN_HANG_ID" = NULL WHERE (id = any (ARRAY%(don_hang_cu_ids)s));
                    UPDATE account_ex_don_dat_hang SET "CHUNG_TU_BAN_HANG_ID" = %(ct_ban_hang_id)s WHERE (id = any (ARRAY%(don_hang_moi_ids)s));""" % {
                        'don_hang_cu_ids': record.LAP_TU_DON_DAT_HANG_IDS.ids or [0],
                        'don_hang_moi_ids': values.get('LAP_TU_DON_DAT_HANG_IDS')[0][2] or [0],
                        'ct_ban_hang_id': record.id
                    })
        result = super(SALE_DOCUMENT, self).write(values)
        if helper.List.element_in_dict(['THU_TIEN_NGAY','LOAI_THANH_TOAN','SO_CHUNG_TU_PHIEU_THU_TIEN_MAT','SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN'], values):
            self.validate_unique_so_chung_tu({self._name.replace('.','_'): 'SO_CHUNG_TU'}, 'SO_CHUNG_TU')
            self.validate_thu_chi_tien()
        elif helper.List.element_in_dict(['SO_CHUNG_TU_GHI_NO'], values):
            self.validate_unique_so_chung_tu({self._name.replace('.','_'): 'SO_CHUNG_TU'}, 'SO_CHUNG_TU')
        
        for record in self:
            record.update_references(values)
            if record.SALE_DOCUMENT_LINE_IDS:
                self.up_date_don_dat_hang()
            
            # Cập nhật lệnh lắp ráp. Lưu ý rằng có thể có nhiều lệnh lắp ráp tạo ra từ chứng từ này
            if values.get('LAP_KEM_LENH_LAP_RAP'):
                record.lap_kem_lenh_lap_rap()
            elif values.get('LAP_KEM_LENH_LAP_RAP') is False:
                for line in record.SALE_DOCUMENT_LINE_IDS:
                    line.LAP_RAP_ID.unlink()
            
            if record.LAP_KEM_LENH_LAP_RAP and 'NGAY_CHUNG_TU' in values:
                record.find_reference('stock.ex.lap.rap.thao.do').write({'NGAY': values.get('NGAY_CHUNG_TU')})

        return result

    def update_references(self, values={}):
        # LAP_KEM_HOA_DON
        # Xóa hóa đơn gắn kèm khi không lập kèm hóa đơn
        if not self.LAP_KEM_HOA_DON:
            self.find_reference('sale.ex.hoa.don.ban.hang').unlink()
        # Tạo/Cập nhật hóa đơn gắn kèm khi tích chọn lập kèm hóa đơn
        else:
            vals = helper.Obj.get_sub_dict(values, ('SO_HOA_DON','NGAY_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID','DOI_TUONG_ID','TEN_KHACH_HANG','LOAI_CHUNG_TU','currency_id','TY_GIA','TONG_TIEN_THANH_TOAN'))
            hoa_don = self.find_reference('sale.ex.hoa.don.ban.hang')
            if hoa_don:
                hoa_don.write(vals)
            # Updated 2019-07-20 by anhtuan: Không tạo thêm hóa đơn khi import
            elif not self._context.get('fromMS'):
                vals.update({
                    'SOURCE_ID': self._name + ',' + str(self.id),
                    'SALE_DOCUMENT_IDS': [(4, self.id)],
                    'TONG_TIEN_THANH_TOAN': self.TONG_TIEN_THANH_TOAN,
                    'DA_HACH_TOAN': True,
                })
                hoa_don = self.env['sale.ex.hoa.don.ban.hang'].create(vals)
                self.SALE_DOCUMENT_LINE_IDS.write({'HOA_DON_ID': hoa_don.id})
        
        # KIEM_PHIEU_NHAP_XUAT_KHO
        # Xóa phiếu xuất gắn kèm khi không kiêm phiếu xuất kho
        if not self.KIEM_PHIEU_NHAP_XUAT_KHO:
            self.find_reference('stock.ex.nhap.xuat.kho').unlink()
        # Tạo phiếu xuất gắn kèm khi tích chọn kiêm phiếu xuất kho
        else:
            phieu_xuat = self.find_reference('stock.ex.nhap.xuat.kho')
            if phieu_xuat:
                vals = helper.Obj.get_sub_dict(values, ('type','NGAY_CHUNG_TU','NGAY_HACH_TOAN','DOI_TUONG_ID','TEN_KHACH_HANG','LOAI_CHUNG_TU','NGUOI_NHAN_TEXT','LY_DO_XUAT','currency_id','TY_GIA'))
                if 'SO_CHUNG_TU_PHIEU_XUAT' in values:
                    vals.update({
                        'SO_CHUNG_TU': values.get('SO_CHUNG_TU_PHIEU_XUAT'),
                    })
                if 'SALE_DOCUMENT_LINE_IDS' in values:
                    phieu_xuat.CHI_TIET_IDS.unlink()
                    xuat_kho_chi_tiet_ids = []
                    for line in self.SALE_DOCUMENT_LINE_IDS:
                        xuat_kho_chi_tiet_ids += [(0,0,{
                            'MA_HANG_ID': line.MA_HANG_ID.id,
                            'TEN_HANG': line.TEN_HANG,
                            'TK_NO_ID': line.TK_GIA_VON_ID.id,
                            'TK_CO_ID': line.TK_KHO_ID.id,
                            'KHO_ID': line.KHO_ID.id,
                            'DVT_ID': line.DVT_ID.id,
                            'SO_LUONG': line.SO_LUONG,
                            'SO_LUONG_YEU_CAU': line.SO_LUONG_YEU_CAU,
                            'DON_GIA': line.DON_GIA,
                            'THANH_TIEN': line.THANH_TIEN,
                            'SALE_DOCUMENT_LINE_IDS': [(4, line.id)]
                        })]
                    vals.update({
                        'CHI_TIET_IDS': xuat_kho_chi_tiet_ids,
                    })
                phieu_xuat.write(vals)
            elif not self._context.get('fromMS'):
                xuat_kho_chi_tiet_ids = []
                for line in self.SALE_DOCUMENT_LINE_IDS:
                    xuat_kho_chi_tiet_ids += [(0,0,{
                        'MA_HANG_ID': line.MA_HANG_ID.id,
                        'TEN_HANG': line.TEN_HANG,
                        'TK_NO_ID': line.TK_GIA_VON_ID.id,
                        'TK_CO_ID': line.TK_KHO_ID.id,
                        'KHO_ID': line.KHO_ID.id,
                        'DVT_ID': line.DVT_ID.id,
                        'SO_LUONG': line.SO_LUONG,
                        'SO_LUONG_YEU_CAU': line.SO_LUONG_YEU_CAU,
                        'DON_GIA': line.DON_GIA,
                        'THANH_TIEN': line.THANH_TIEN,
                        'SALE_DOCUMENT_LINE_IDS': [(4, line.id)]
                    })]

                vals = {
                    'type': 'XUAT_KHO',
                    'SO_CHUNG_TU': values.get('SO_CHUNG_TU', self.SO_CHUNG_TU_PHIEU_XUAT),
                    'NGAY_CHUNG_TU': values.get('NGAY_CHUNG_TU', self.NGAY_CHUNG_TU),
                    'NGAY_HACH_TOAN': values.get('NGAY_HACH_TOAN', self.NGAY_HACH_TOAN),
                    'DOI_TUONG_ID': values.get('DOI_TUONG_ID', self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else None),
                    'LOAI_CHUNG_TU': values.get('LOAI_CHUNG_TU', self.LOAI_CHUNG_TU),
                    'NGUOI_NHAN_TEXT': values.get('NGUOI_NHAN_TEXT', self.NGUOI_GIAO_NHAN_HANG),
                    'LY_DO_XUAT': values.get('LY_DO_XUAT', self.LY_DO_NHAP_XUAT),
                    'currency_id': values.get('currency_id', self.currency_id.id),
                    'TY_GIA': values.get('TY_GIA', self.TY_GIA),
                    'SOURCE_ID': self._name + ',' + str(self.id),
                    'CHI_TIET_IDS': xuat_kho_chi_tiet_ids,
                }
                self.env['stock.ex.nhap.xuat.kho'].create(vals)

    
    @api.multi
    def unlink(self):
        arr_don_dat_hang = []
        # id_don_dat_hang = False
        # if self.CHON_LAP_TU_ID and self.CHON_LAP_TU_ID._name == 'account.ex.don.dat.hang':               
        #     id_don_dat_hang = self.CHON_LAP_TU_ID.id
        for record in self:
            # Xóa chứng từ xuất kho gắn kèm
            record.find_reference('stock.ex.nhap.xuat.kho').unlink()
            if record.SALE_DOCUMENT_LINE_IDS:
                for chi_tiet in record.SALE_DOCUMENT_LINE_IDS:
                    if chi_tiet.DON_DAT_HANG_ID:
                        arr_don_dat_hang.append(chi_tiet.DON_DAT_HANG_ID.id)
                    # Xóa lắp ráp gắn kèm
                    chi_tiet.LAP_RAP_ID.unlink()

        result = super(SALE_DOCUMENT, self).unlink()
        if arr_don_dat_hang:
            for line in arr_don_dat_hang:
                self.update_don_dat_hang(line)
                self.update_trang_thai_don_dat_hang(line)
        # if id_don_dat_hang != False:
                don_dat_hang = self.env['account.ex.don.dat.hang'].browse(line)
                if don_dat_hang:
                    don_dat_hang.write({'NGAY_GIAO_HANG' : False})
        return result

    def up_date_don_dat_hang(self):
        arr_don_dat_hang = []
        for chi_tiet in self.SALE_DOCUMENT_LINE_IDS:
                if chi_tiet.DON_DAT_HANG_ID:
                    if chi_tiet.DON_DAT_HANG_ID.id not in arr_don_dat_hang:
                        arr_don_dat_hang.append(chi_tiet.DON_DAT_HANG_ID.id)
        if arr_don_dat_hang:
            for line in arr_don_dat_hang:
                self.update_don_dat_hang(line)
                self.update_trang_thai_don_dat_hang(line)
        
        if self.CHON_LAP_TU_ID:
            self.CHON_LAP_TU_ID.NGAY_GIAO_HANG = self.NGAY_HACH_TOAN
    
    
    # Thêm một trường là Loại chứng từ 
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',store=True,compute='set_loai_chung_tu_ban_hang') 

    # Thêm một trường chọn từ đơn hàng hoặc báo giá - 19/3/2019 - ManhPV
    CHON_LAP_TU_ID = fields.Reference(selection=[('sale.ex.bao.gia', 'Lập từ Báo giá'),
                                                        ('account.ex.don.dat.hang', 'Lập từ Đơn đặt hàng'),
                                                        ('sale.ex.hop.dong.ban', 'Lập từ Hợp đồng bán'),
                                                        ('stock.ex.nhap.xuat.kho', 'Lập từ Phiếu xuất'),
                                                        ('sale.ex.hoa.don.ban.hang', 'Lập từ Hóa đơn'),
                                                        ('purchase.document', 'Lập từ Mua hàng'),
                                                        ('stock.ex.nhap.xuat.kho','Lập từ Chuyển kho')], string='Lập từ')

    #model phần giảm giá hàng bán
    # LOAI_NGHIEP_VU_GTHB = fields.Selection([('DICH_VU', '1. Bán hàng hóa, dịch vụ'),('DAI_LY', '2. Bán hàng đại lý đúng giá'), ('XUAT_KHAU', '3. Bán hàng ủy thác xuất khẩu')], string='Loại nghiệp vụ', help='Loại nghiệp vụ',default='DICH_VU',required=True)
    # LOAI_GIAM_TRU_GGHB = fields.Selection([
        # ('GIAM_TRU_CONG_NO','Giảm trừ công nợ'),
        # ('TRA_LAI_TIEN_MAT','Trả lại tiền mặt'),
        # ], default='GIAM_TRU_CONG_NO')
    # chi_tiet_gghb = fields.Selection([
        # ('hang_tien', 'Hàng tiền'),
        # ('thong_ke', 'Thống kê'),   
        # ], default='hang_tien', string='NO_SAVE')
    #------------------------------------------------------------------ 
    # Detail
    chi_tiet = fields.Selection([
        ('hang_tien', 'Hàng tiền'),
        ('thue', 'Thuế'),
        ('gia_von','Giá vốn'),
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')
    IS_CHUNG_TU_GHI_NO = fields.Boolean(default=True,compute='set_is_phieu_thu_ghi_no',sotre=False)
    IS_PHIEU_THU = fields.Boolean(default=False,compute='set_is_phieu_thu_ghi_no',store=False)
    IS_GIAM_TRU_CONG_NO = fields.Boolean(default=True)
    IS_HOA_DON_GGHB = fields.Boolean(default=True)
    IS_PHIEU_CHI_GGHB = fields.Boolean(default=False)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU_TEXT = fields.Char(string='Loại chứng từ',compute='set_loai_chung_tu_text',store=True)
    XUAT_KHO_REF_ID = fields.Char(help='Ref ID của phiếu xuất được import')
    DA_LAP_HOA_DON_TEXT = fields.Char(string='Đã lập hóa đơn', help='Đã lập hóa đơn')#,compute='set_da_lap_hoa_don_text',store=True)
    # Bổ sung hàm depend để lấy loại chứng từ        
    @api.depends('LOAI_NGHIEP_VU','THU_TIEN_NGAY','LOAI_THANH_TOAN')
    def set_loai_chung_tu_ban_hang(self):
        if self.THU_TIEN_NGAY==False:
            if self.LOAI_NGHIEP_VU =='TRONG_NUOC':
                self.LOAI_CHUNG_TU = 3530
            elif self.LOAI_NGHIEP_VU =='DAI_LY':
                self.LOAI_CHUNG_TU = 3534
            elif self.LOAI_NGHIEP_VU == 'XUAT_KHAU':
                self.LOAI_CHUNG_TU = 3532
            elif self.LOAI_NGHIEP_VU == 'UY_THAC':
                self.LOAI_CHUNG_TU = 3536
        elif self.THU_TIEN_NGAY==True:
            if self.LOAI_NGHIEP_VU =='TRONG_NUOC' and self.LOAI_THANH_TOAN=='TIEN_MAT':
                self.LOAI_CHUNG_TU = 3531
            elif self.LOAI_NGHIEP_VU =='TRONG_NUOC' and self.LOAI_THANH_TOAN=='CHUYEN_KHOAN':
                self.LOAI_CHUNG_TU = 3537
            elif self.LOAI_NGHIEP_VU =='DAI_LY' and self.LOAI_THANH_TOAN=='TIEN_MAT':
                self.LOAI_CHUNG_TU = 3535
            elif self.LOAI_NGHIEP_VU =='DAI_LY' and self.LOAI_THANH_TOAN=='CHUYEN_KHOAN':
                self.LOAI_CHUNG_TU = 3538

    # @api.onchange('LOAI_GIAM_TRU_GGHB')
    # def update_LOAI_GIAM_TRU_GGHB(self):
        # if self.LOAI_GIAM_TRU_GGHB == 'TRA_LAI_TIEN_MAT':
            # self.IS_GIAM_TRU_CONG_NO = False
            # self.IS_PHIEU_CHI_GGHB = True
        # if self.LOAI_GIAM_TRU_GGHB == 'GIAM_TRU_CONG_NO':
            # self.IS_GIAM_TRU_CONG_NO = True
            # self.IS_PHIEU_CHI_GGHB = False


    @api.depends('LOAI_CHUNG_TU')
    def set_loai_chung_tu_text(self):
        for record in self:
            loai_chung_tu_text=''
            reftype= record.env['danh.muc.reftype'].search([('REFTYPE', '=',record.LOAI_CHUNG_TU)],limit=1)
            if reftype:
                loai_chung_tu_text = reftype.REFTYPENAME
            record.LOAI_CHUNG_TU_TEXT = loai_chung_tu_text

    # @api.depends('DA_LAP_HOA_DON')
    @api.onchange('DA_LAP_HOA_DON')
    def set_da_lap_hoa_don_text(self):
        if self.DA_LAP_HOA_DON:
            self.DA_LAP_HOA_DON_TEXT = 'Đã lập'
        else:
            self.DA_LAP_HOA_DON_TEXT = 'Chưa lập'

    @api.onchange('DON_VI_GIAO_DAI_LY_ID')
    def ttt(self):
        self.TEN_DON_VI = self.DON_VI_GIAO_DAI_LY_ID.HO_VA_TEN
    @api.onchange('NOP_VAO_TK_ID')
    def tttk(self):
        if self.NOP_VAO_TK_ID:
            self.TEN_TK = str(self.NOP_VAO_TK_ID.NGAN_HANG_ID.TEN_DAY_DU) + "-" + str(self.NOP_VAO_TK_ID.CHI_NHANH)



    @api.onchange('DON_VI_UY_THAC_ID')
    def ttdvut(self):
        self.TEN_DON_VI_UY_THAC = self.DON_VI_UY_THAC_ID.HO_VA_TEN

    @api.onchange('DOI_TUONG_ID')
    def adnc(self):
        if self.DOI_TUONG_ID:
            self.TEN_KHACH_HANG = self.DOI_TUONG_ID.HO_VA_TEN
            self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
            self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
            self.NGUOI_LIEN_HE = self.env['res.partner'].search([('parent_id','=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            if self.DOI_TUONG_ID.DANH_MUC_DOI_TUONG_CHI_TIET_IDS:
                self.TK_NGAN_HANG = self.DOI_TUONG_ID.DANH_MUC_DOI_TUONG_CHI_TIET_IDS[0]
            else:
                self.TK_NGAN_HANG = False
            self.NGUOI_NOP_NHAN = self.env['res.partner'].search([('parent_id','=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            self.NGUOI_GIAO_NHAN_HANG = self.env['res.partner'].search([('parent_id','=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            self.NGUOI_MUA_HANG = self.env['res.partner'].search([('parent_id','=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            self.NHAN_VIEN_ID = self.DOI_TUONG_ID.NHAN_VIEN_ID.id

    @api.onchange('LOAI_NGHIEP_VU','LAP_KEM_HOA_DON')
    def _onchange_nghiep_vu(self):
        if self.LOAI_NGHIEP_VU in ('XUAT_KHAU','UY_THAC'):
            self.THU_TIEN_NGAY = False
        if self.LAP_KEM_HOA_DON and self.LOAI_NGHIEP_VU in ('XUAT_KHAU','UY_THAC'):
            self.SO_HOA_DON = self.SO_CHUNG_TU_HOA_DON
        else:
            self.SO_HOA_DON = None

        if self.LAP_KEM_HOA_DON == False:
            self.NGAY_HOA_DON = False
            self.SO_HOA_DON = False
        else:
            self.NGAY_HOA_DON = self.NGAY_CHUNG_TU

    @api.onchange('TEN_KHACH_HANG','SO_HOA_DON','THU_TIEN_NGAY')
    def _onchange_dien_giai(self):
        dien_giai = 'Thu tiền bán hàng' if self.THU_TIEN_NGAY else 'Bán hàng'
        ly_do_xuat = 'Xuất kho bán hàng'
        if self.TEN_KHACH_HANG:
            dien_giai += ' ' + self.TEN_KHACH_HANG
            ly_do_xuat += ' '+ self.TEN_KHACH_HANG
        if self.SO_HOA_DON:
            dien_giai += ' theo hóa đơn ' + self.SO_HOA_DON
            ly_do_xuat += ' theo hóa đơn '+ self.SO_HOA_DON
        self.DIEN_GIAI = dien_giai
        self.LY_DO_NHAP_XUAT = ly_do_xuat

    # Thêm hàm onchange để lấy dữ liệu từ các chứng từ sau khi thay đổi selection - 19/03/2019 - ManhPV
    @api.onchange('CHON_LAP_TU_ID')
    def lay_cac_chung_tu(self):
        if(self.CHON_LAP_TU_ID):
            if self.CHON_LAP_TU_ID._name =='sale.ex.bao.gia':
                str_dien_giai=''
                str_ly_do_xuat=''
                if self.CHON_LAP_TU_ID.TEN_KHACH_HANG:
                    str_dien_giai= 'Đơn đặt hàng của '+ str(self.CHON_LAP_TU_ID.TEN_KHACH_HANG)
                    str_ly_do_xuat= 'Xuất kho bán hàng '+ str(self.CHON_LAP_TU_ID.TEN_KHACH_HANG)
                self.DOI_TUONG_ID = self.CHON_LAP_TU_ID.KHACH_HANG_ID.id 
                self.TEN_KHACH_HANG = self.CHON_LAP_TU_ID.TEN_KHACH_HANG
                self.MA_SO_THUE = self.CHON_LAP_TU_ID.MA_SO_THUE
                self.DIA_CHI = self.CHON_LAP_TU_ID.DIA_CHI
                self.currency_id = self.CHON_LAP_TU_ID.currency_id.id
                self.TY_GIA = self.CHON_LAP_TU_ID.TY_GIA
                self.DIEN_GIAI = str_dien_giai
                self.LY_DO_NHAP_XUAT = str_ly_do_xuat
                if(self.CHON_LAP_TU_ID.SALE_EX_BAO_GIA_CHI_TIET_IDS):  
                    default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')                  
                    self.SALE_DOCUMENT_LINE_IDS = []
                    for line in self.CHON_LAP_TU_ID.SALE_EX_BAO_GIA_CHI_TIET_IDS:
                        san_pham =  line.MA_HANG_ID
                        dien_giai_thue = ''
                        kho_id = 0
                        tk_gia_von_id = 0
                        if san_pham:
                            ten_san_pham = san_pham.TEN
                            dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                            kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                        tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                        if tk_gia_von_632:
                            tk_gia_von_id = tk_gia_von_632.id
                        detail = self.env['sale.document.line'].new()
                        detail.MA_HANG_ID = line.MA_HANG_ID.id
                        detail.DIEN_GIAI_THUE = dien_giai_thue
                        detail.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                        detail.TK_NO_ID = default.get('TK_NO_ID')
                        detail.TK_CO_ID = default.get('TK_CO_ID')
                        detail.TK_THUE_GTGT_ID = default.get('TK_THUE_GTGT_ID')
                        detail.TK_CHIET_KHAU_ID = default.get('TK_CHIET_KHAU_ID')
                        detail.TK_KHO_ID = kho_id
                        detail.TK_GIA_VON_ID = tk_gia_von_id
                        detail.DON_GIA = line.DON_GIA
                        detail.SO_LUONG = line.SO_LUONG
                        detail.DVT_ID = line.DVT_ID.id
                        detail.TY_LE_CK =  line.TY_LE_CK
                        detail.TIEN_CHIET_KHAU =  line.TIEN_CHIET_KHAU
                        detail.TIEN_CK_QUY_DOI =  line.TIEN_CHIET_KHAU_QUY_DOI
                        detail.DON_VI_ID =  line.MA_HANG_ID.CHI_NHANH_ID
                        detail.THUE_GTGT_ID =  line.PHAN_TRAM_THUE_GTGT_ID
                        detail.TIEN_THUE_GTGT =  line.TIEN_THUE_GTGT
                        detail.TIEN_THUE_GTGT_QUY_DOI =  line.TIEN_THUE_GTGT_QUY_DOI
                        detail.TEN_HANG = line.TEN_HANG
                        detail.THANH_TIEN = line.THANH_TIEN
                        detail.THANH_TIEN_QUY_DOI = line.THANH_TIEN_QUY_DOI
                        self.SALE_DOCUMENT_LINE_IDS += detail

            elif self.CHON_LAP_TU_ID._name =='account.ex.don.dat.hang':
                str_ly_do_xuat= ''
                if self.CHON_LAP_TU_ID.TEN_KHACH_HANG:
                    str_ly_do_xuat= 'Xuất kho bán hàng '+ str(self.CHON_LAP_TU_ID.TEN_KHACH_HANG)
                self.DOI_TUONG_ID = self.CHON_LAP_TU_ID.KHACH_HANG_ID.id 
                self.TEN_KHACH_HANG = self.CHON_LAP_TU_ID.TEN_KHACH_HANG
                self.MA_SO_THUE = self.CHON_LAP_TU_ID.MA_SO_THUE
                self.DIA_CHI = self.CHON_LAP_TU_ID.DIA_CHI
                self.DIEN_GIAI = self.CHON_LAP_TU_ID.DIEN_GIAI
                self.LY_DO_NHAP_XUAT = str_ly_do_xuat
                self.currency_id = self.CHON_LAP_TU_ID.currency_id.id
                self.TY_GIA = self.CHON_LAP_TU_ID.TY_GIA
                if(self.CHON_LAP_TU_ID.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS):
                    default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')                    
                    self.SALE_DOCUMENT_LINE_IDS = []
                    for line in self.CHON_LAP_TU_ID.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                        san_pham =  line.MA_HANG_ID
                        dien_giai_thue = ''
                        kho_id = 0
                        tk_gia_von_id = 0
                        if san_pham:
                            ten_san_pham = san_pham.TEN
                            dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                            kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                        tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                        if tk_gia_von_632:
                            tk_gia_von_id = tk_gia_von_632.id

                        detail = self.env['sale.document.line'].new()
                        detail.MA_HANG_ID = line.MA_HANG_ID.id
                        detail.TEN_HANG = line.TEN_HANG
                        detail.DIEN_GIAI_THUE = dien_giai_thue
                        detail.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                        detail.TK_NO_ID = default.get('TK_NO_ID')
                        detail.TK_CO_ID = default.get('TK_CO_ID')
                        detail.TK_THUE_GTGT_ID = default.get('TK_THUE_GTGT_ID')
                        detail.TK_CHIET_KHAU_ID = default.get('TK_CHIET_KHAU_ID')
                        detail.TK_KHO_ID = kho_id
                        detail.TK_GIA_VON_ID = tk_gia_von_id
                        detail.DON_GIA = line.DON_GIA
                        detail.SO_LUONG = line.SO_LUONG
                        detail.THANH_TIEN = line.THANH_TIEN
                        detail.THANH_TIEN_QUY_DOI = line.THANH_TIEN_QUY_DOI
                        detail.DVT_ID = line.DVT_ID.id
                        detail.DON_VI_ID =  line.MA_HANG_ID.CHI_NHANH_ID
                        detail.THUE_GTGT_ID =  line.PHAN_TRAM_THUE_GTGT_ID
                        detail.TIEN_THUE_GTGT =  line.TIEN_THUE_GTGT
                        detail.TIEN_THUE_GTGT_QUY_DOI =  line.TIEN_THUE_GTGT_QUY_DOI
                        detail.DON_DAT_HANG_CHI_TIET_ID =  line.id
                        detail.DON_DAT_HANG_ID =  self.CHON_LAP_TU_ID.id
                        self.SALE_DOCUMENT_LINE_IDS += detail
                

            elif self.CHON_LAP_TU_ID._name =='sale.ex.hop.dong.ban':
                str_dien_giai= ''
                str_ly_do_xuat= ''
                if self.CHON_LAP_TU_ID.TEN_KHACH_HANG:
                    str_dien_giai= 'Đơn đặt hàng của '+ str(self.CHON_LAP_TU_ID.TEN_KHACH_HANG)
                    str_ly_do_xuat= 'Xuất kho bán hàng '+ str(self.CHON_LAP_TU_ID.TEN_KHACH_HANG)
                self.DOI_TUONG_ID = self.CHON_LAP_TU_ID.KHACH_HANG_ID.id 
                self.TEN_KHACH_HANG = self.CHON_LAP_TU_ID.TEN_KHACH_HANG
                self.DIA_CHI = self.CHON_LAP_TU_ID.DIA_CHI
                self.MA_SO_THUE = self.CHON_LAP_TU_ID.KHACH_HANG_ID.MA_SO_THUE
                self.DIEN_GIAI = str_dien_giai
                self.LY_DO_NHAP_XUAT = str_ly_do_xuat
                self.NHAN_VIEN_ID = self.CHON_LAP_TU_ID.NGUOI_THUC_HIEN_ID.id
                self.currency_id = self.CHON_LAP_TU_ID.currency_id.id
                self.TY_GIA = self.CHON_LAP_TU_ID.TY_GIA
                if self.CHON_LAP_TU_ID.SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS:
                    default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')                    
                    self.SALE_DOCUMENT_LINE_IDS = []
                    for line in self.CHON_LAP_TU_ID.SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS:
                        san_pham =  line.MA_HANG_ID
                        dien_giai_thue = ''
                        kho_id = 0
                        tk_gia_von_id = 0
                        if san_pham:
                            ten_san_pham = san_pham.TEN
                            dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                            kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                        tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                        if tk_gia_von_632:
                            tk_gia_von_id = tk_gia_von_632.id

                        detail = self.env['sale.document.line'].new()
                        detail.MA_HANG_ID = line.MA_HANG_ID.id
                        detail.TEN_HANG = line.TEN_HANG
                        detail.DIEN_GIAI_THUE = dien_giai_thue
                        detail.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                        detail.TK_NO_ID = default.get('TK_NO_ID')
                        detail.TK_CO_ID = default.get('TK_CO_ID')
                        detail.TK_THUE_GTGT_ID = default.get('TK_THUE_GTGT_ID')
                        detail.TK_CHIET_KHAU_ID = default.get('TK_CHIET_KHAU_ID')
                        detail.TK_KHO_ID = kho_id
                        detail.TK_GIA_VON_ID = tk_gia_von_id
                        detail.DON_GIA = line.DON_GIA
                        detail.SO_LUONG = line.SO_LUONG
                        detail.THANH_TIEN = line.THANH_TIEN
                        detail.THANH_TIEN_QUY_DOI = line.THANH_TIEN_QUY_DOI
                        detail.DVT_ID = line.DVT_ID.id
                        detail.DON_VI_ID =  line.MA_HANG_ID.CHI_NHANH_ID
                        detail.THUE_GTGT_ID =  line.PHAN_TRAM_THUE_GTGT_ID
                        detail.TIEN_THUE_GTGT =  line.TIEN_THUE_GTGT
                        detail.TIEN_THUE_GTGT_QUY_DOI =  line.TIEN_THUE_GTGT_QUY_DOI
                        detail.HOP_DONG_BAN_ID =  self.CHON_LAP_TU_ID.id
                        self.SALE_DOCUMENT_LINE_IDS += detail

            elif self.CHON_LAP_TU_ID._name =='purchase.document':
                self.currency_id = self.CHON_LAP_TU_ID.currency_id.id
                self.TY_GIA = self.CHON_LAP_TU_ID.TY_GIA
                if self.CHON_LAP_TU_ID.CHI_TIET_IDS:
                    default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')                    
                    self.SALE_DOCUMENT_LINE_IDS = []
                    for line in self.CHON_LAP_TU_ID.CHI_TIET_IDS:
                        san_pham =  line.MA_HANG_ID
                        don_gia = 0
                        dien_giai_thue = ''
                        kho_id = 0
                        tk_gia_von_id = 0
                        thanh_tien = 0
                        if san_pham:
                            ten_san_pham = san_pham.TEN
                            dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                            don_gia = san_pham.compute_DON_GIA_BAN(line.DVT_ID.id)
                            kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                        tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                        if tk_gia_von_632:
                            tk_gia_von_id = tk_gia_von_632.id
                        so_luong = line.SO_LUONG
                        thanh_tien = don_gia * so_luong
                        thanh_tien_quy_doi = thanh_tien * self.CHON_LAP_TU_ID.TY_GIA
                        detail = self.env['sale.document.line'].new()
                        detail.MA_HANG_ID = line.MA_HANG_ID.id
                        detail.TEN_HANG = line.name
                        detail.DIEN_GIAI_THUE = dien_giai_thue
                        detail.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                        detail.TK_NO_ID = default.get('TK_NO_ID')
                        detail.TK_CO_ID = default.get('TK_CO_ID')
                        detail.TK_THUE_GTGT_ID = default.get('TK_THUE_GTGT_ID')
                        detail.TK_CHIET_KHAU_ID = default.get('TK_CHIET_KHAU_ID')
                        detail.TK_KHO_ID = kho_id
                        detail.TK_GIA_VON_ID = tk_gia_von_id
                        detail.DON_GIA = don_gia
                        detail.SO_LUONG = so_luong
                        detail.DVT_ID = line.DVT_ID.id
                        detail.TY_LE_CK =  line.TY_LE_CK
                        detail.TIEN_CHIET_KHAU =  line.TIEN_CHIET_KHAU
                        detail.TIEN_CK_QUY_DOI =  line.TIEN_CHIET_KHAU_QUY_DOI
                        detail.THANH_TIEN = thanh_tien
                        detail.THANH_TIEN_QUY_DOI = thanh_tien_quy_doi
                        detail.DON_VI_ID =  line.DON_VI_ID.id
                        detail.THUE_GTGT_ID =  line.THUE_GTGT_ID
                        self.SALE_DOCUMENT_LINE_IDS += detail

            elif self.CHON_LAP_TU_ID._name =='stock.ex.nhap.xuat.kho':
                if(self.CHON_LAP_TU_ID.CHI_TIET_IDS):
                    default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')                                      
                    self.SALE_DOCUMENT_LINE_IDS = []
                    for line in self.CHON_LAP_TU_ID.CHI_TIET_IDS:
                        san_pham =  line.MA_HANG_ID
                        dien_giai_thue = ''
                        kho_id = 0
                        tk_gia_von_id = 0
                        if san_pham:
                            ten_san_pham = san_pham.TEN
                            dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                            don_gia = san_pham.compute_DON_GIA_BAN(line.DVT_ID.id)
                            kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                        tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                        if tk_gia_von_632:
                            tk_gia_von_id = tk_gia_von_632.id

                        so_luong = line.SO_LUONG
                        thanh_tien = don_gia * so_luong
                        detail = self.env['sale.document.line'].new()
                        detail.MA_HANG_ID = line.MA_HANG_ID.id
                        detail.TEN_HANG = line.TEN_HANG
                        detail.DIEN_GIAI_THUE = dien_giai_thue
                        detail.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                        detail.TK_NO_ID = default.get('TK_NO_ID')
                        detail.TK_CO_ID = default.get('TK_CO_ID')
                        detail.TK_THUE_GTGT_ID = default.get('TK_THUE_GTGT_ID')
                        detail.TK_CHIET_KHAU_ID = default.get('TK_CHIET_KHAU_ID')
                        detail.TK_KHO_ID = kho_id
                        detail.TK_GIA_VON_ID = tk_gia_von_id
                        detail.DON_GIA = don_gia
                        detail.SO_LUONG = so_luong
                        detail.DVT_ID = line.DVT_ID.id
                        detail.DON_VI_ID =  line.MA_HANG_ID.CHI_NHANH_ID
                        detail.THANH_TIEN = thanh_tien
                        detail.THUE_GTGT_ID =  line.MA_HANG_ID.THUE_SUAT_GTGT_ID
                        self.SALE_DOCUMENT_LINE_IDS += detail

            elif self.CHON_LAP_TU_ID._name =='sale.ex.hoa.don.ban.hang':
                self.DOI_TUONG_ID = self.CHON_LAP_TU_ID.DOI_TUONG_ID.id 
                self.TEN_KHACH_HANG = self.CHON_LAP_TU_ID.TEN_KHACH_HANG
                self.MA_SO_THUE = self.CHON_LAP_TU_ID.MA_SO_THUE
                self.DIA_CHI = self.CHON_LAP_TU_ID.DIA_CHI
                self.NHAN_VIEN_ID = self.CHON_LAP_TU_ID.NHAN_VIEN_ID.id
                self.currency_id = self.CHON_LAP_TU_ID.currency_id.id
                self.TY_GIA = self.CHON_LAP_TU_ID.TY_GIA
                if(self.CHON_LAP_TU_ID.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS):
                    default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')                    
                    self.SALE_DOCUMENT_LINE_IDS = []
                    for line in self.CHON_LAP_TU_ID.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
                        san_pham =  line.MA_HANG_ID
                        dien_giai_thue = ''
                        kho_id = 0
                        tk_gia_von_id = 0
                        if san_pham:
                            ten_san_pham = san_pham.TEN
                            dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                            kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                        tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                        if tk_gia_von_632:
                            tk_gia_von_id = tk_gia_von_632.id
                        so_luong = line.SO_LUONG
                        don_gia = line.DON_GIA
                        thanh_tien = don_gia * so_luong
                        thanh_tien_quy_doi = thanh_tien * self.CHON_LAP_TU_ID.TY_GIA
                        detail = self.env['sale.document.line'].new()
                        detail.MA_HANG_ID = line.MA_HANG_ID.id
                        detail.TEN_HANG = line.TEN_HANG
                        detail.DIEN_GIAI_THUE = dien_giai_thue
                        detail.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                        detail.TK_NO_ID = default.get('TK_NO_ID')
                        detail.TK_CO_ID = default.get('TK_CO_ID')
                        detail.TK_THUE_GTGT_ID = default.get('TK_THUE_GTGT_ID')
                        detail.TK_CHIET_KHAU_ID = default.get('TK_CHIET_KHAU_ID')
                        detail.TK_KHO_ID = kho_id
                        detail.TK_GIA_VON_ID = tk_gia_von_id
                        detail.DON_GIA = don_gia
                        detail.SO_LUONG = so_luong
                        detail.THANH_TIEN = thanh_tien
                        detail.THANH_TIEN_QUY_DOI = thanh_tien_quy_doi
                        detail.DVT_ID = line.DVT_ID.id
                        detail.TY_LE_CK =  line.TY_LE_CK
                        detail.TIEN_CK_QUY_DOI =  line.TIEN_CHIET_KHAU_QUY_DOI
                        detail.DON_VI_ID =  line.MA_HANG_ID.CHI_NHANH_ID
                        detail.THUE_GTGT_ID =  line.THUE_GTGT
                        detail.TIEN_THUE_GTGT =  line.TIEN_THUE_GTGT
                        detail.TIEN_THUE_GTGT_QUY_DOI =  line.TIEN_THUE_GTGT_QUY_DOI
                        self.SALE_DOCUMENT_LINE_IDS += detail
            
    @api.onchange('LAP_KEM_HOA_DON')
    def tdckeck(self):
        self.IN_KEM_BANH_KE = not self.LAP_KEM_HOA_DON
        # self.DA_LAP_HOA_DON = self.LAP_KEM_HOA_DON #Mạnh comment đoạn code này là do thiết lập vòng, Bug 1795
        
    @api.onchange('LOAI_THANH_TOAN')
    def thaydoiltt(self):
        if self.LOAI_THANH_TOAN == 'TIEN_MAT':
            self.HINH_THUC_TT = 'TIEN_MAT'
        elif self.LOAI_THANH_TOAN == 'CHUYEN_KHOAN':
            self.HINH_THUC_TT = 'CHUYEN_KHOAN'
        elif self.LOAI_THANH_TOAN == '':
            self.HINH_THUC_TT = 'TIEN_MAT_CHUYEN_KHOAN'
        else:
            self.HINH_THUC_TT = ''
    
    @api.onchange('THU_TIEN_NGAY')
    def thaydoittn(self):
        if self.THU_TIEN_NGAY == False:
            self.LOAI_THANH_TOAN = ''
        else:
            self.LOAI_THANH_TOAN = 'TIEN_MAT'
            
    @api.depends('THU_TIEN_NGAY')
    def set_is_phieu_thu_ghi_no(self):
        for record in self:
            if record.THU_TIEN_NGAY == False:
                record.IS_PHIEU_THU = False
                record.IS_CHUNG_TU_GHI_NO = True
            else:
                record.IS_PHIEU_THU = True
                record.IS_CHUNG_TU_GHI_NO = False

    @api.onchange('currency_id')
    def update_thaydoiIsTy_gia_tien(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False   

    @api.model
    def default_get(self,default_fields):
        res = super(SALE_DOCUMENT, self).default_get(default_fields)
        # TK_NGAN_HANG là danh.muc.doi.tuong.chi.tiet, không phải danh.muc.tai.khoan.ngan.hang
        # if self.DOI_TUONG_ID:
        # res['TK_NGAN_HANG'] = self.env['danh.muc.tai.khoan.ngan.hang'].search([],limit=1).id
        res['HINH_THUC_TT'] = 'TIEN_MAT_CHUYEN_KHOAN' if self.THU_TIEN_NGAY == False else 'TIEN_MAT'
        # res['DIEN_GIAI'] = 'Bán hàng'
        # res['LY_DO_NHAP_XUAT'] = 'Xuất kho bán hàng'
        res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=','VND')],limit=1).id

        # Task 3513
        # Giải pháp tạm thời
        res['CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH'] = self.env['ir.config_parameter'].get_param('he_thong.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH')
        res['TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG'] = self.env['ir.config_parameter'].get_param('he_thong.TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG')=='True'

        # res['TK_THUE_XK_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('code', '=like', '3333')])
        return res
    
    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_ban_hang()
            # if record.KIEM_PHIEU_NHAP_XUAT_KHO == 'True':
            #     record.ghi_so_kho()
            record.ghi_so_cong_no()
            # Ghi sổ các references
            # hoa_don = record.find_reference('sale.ex.hoa.don.ban.hang')
            # if hoa_don:
            if record.HOA_DON_IDS:
                for hoa_don in record.HOA_DON_IDS:
                    if self.LOAI_NGHIEP_VU not in ('DAI_LY','UY_THAC'):
                        hoa_don.ghi_so_thue()
            phieu_xuat = record.find_reference('stock.ex.nhap.xuat.kho')
            if phieu_xuat:
                phieu_xuat.action_ghi_so()
            if record.LAP_KEM_LENH_LAP_RAP:
                for ref in record.find_reference('stock.ex.lap.rap.thao.do', None):
                    ref.THAM_CHIEU.action_ghi_so()
                
        self.write({'state':'da_ghi_so'})

    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        loai_tien_vnd = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1).id
        tai_khoan_5111 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '5111')],limit=1).id

        for line in self.SALE_DOCUMENT_LINE_IDS:
            so_hoa_don = None
            ngay_hoa_don = None
            if self.LAP_KEM_HOA_DON == False:
                if line.HOA_DON_ID:
                    hoa_don_ban_hang = self.env['sale.ex.hoa.don.ban.hang'].search([('id', '=', line.HOA_DON_ID.id)])
                    if hoa_don_ban_hang:
                        so_hoa_don = hoa_don_ban_hang.SO_HOA_DON
                        ngay_hoa_don = hoa_don_ban_hang.NGAY_HOA_DON
                else:
                    if self.HOA_DON_IDS:
                        if len(self.HOA_DON_IDS) == 1:
                            so_hoa_don = self.HOA_DON_IDS[0].SO_HOA_DON
                            ngay_hoa_don = self.HOA_DON_IDS[0].NGAY_HOA_DON
            else:
                so_hoa_don = self.SO_HOA_DON
                ngay_hoa_don = self.NGAY_HOA_DON

            nguoi_lien_he = None
            if self.THU_TIEN_NGAY == True:
                nguoi_lien_he = self.NGUOI_NOP_NHAN
            # else:
            #     nguoi_lien_he = self.NGUOI_GIAO_NHAN_HANG

            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'LOAI_CHUNG_TU_CTBH': self._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                    'SO_TIEN': line.THANH_TIEN,
                    'currency_id' : self.currency_id.id,
                    'TEN_LOAI_TIEN' : self.currency_id.TEN_LOAI_TIEN,
                    'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                    'TAI_KHOAN_NGAN_HANG_ID' : self.NOP_VAO_TK_ID.id,
                    'DIA_CHI_DOI_TUONG' : self.DIA_CHI,
                    'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE,
                    'NHAN_VIEN_ID' : self.NHAN_VIEN_ID.id,
                    # 'SO_HOA_DON' : self.SO_CHUNG_TU_HOA_DON,
                    'DIEN_GIAI' : line.TEN_HANG,
                    'DON_VI_ID' : line.DON_VI_ID.id,
                    'LOAI_NGHIEP_VU' : False,
                    'NGUOI_NHAN_NOP' : self.NGUOI_NOP_NHAN,
                    'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                    'SO_HOA_DON' : so_hoa_don,
                    'NGAY_HOA_DON' : ngay_hoa_don,
                    'DON_GIA' : line.DON_GIA*self.TY_GIA,
                    'NGUOI_LIEN_HE' : nguoi_lien_he,
                })
            if self.LOAI_CHUNG_TU in (3534,3535,3536,3538):
            # 3.534	Bán hàng đại lý bán đúng giá - Chưa thu tiền
            # 3.535	Bán hàng đại lý bán đúng giá - Tiền mặt
            # 3.536	Bán hàng nhận ủy thác xuất khẩu
            # 3.538	Bán hàng đại lý bán đúng giá - Chuyển khoản
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : line.THANH_TIEN_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI - line.TIEN_CK_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.THANH_TIEN + line.TIEN_THUE_GTGT - line.TIEN_CHIET_KHAU,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_ghi_no)]
                if self.LOAI_CHUNG_TU == 3534:
                    if line.TK_NO_ID.id == tai_khoan_5111 and line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == False:
                        doi_tuong_id = None
                    else:
                        doi_tuong_id = self.DON_VI_GIAO_DAI_LY_ID.id
                elif self.LOAI_CHUNG_TU == 3536:
                    doi_tuong_id = self.DON_VI_UY_THAC_ID.id
                else:
                    doi_tuong_id = self.DOI_TUONG_ID.id

                data_ghi_co = data_goc.copy()
                data_ghi_co.update({
                    'DOI_TUONG_ID' : doi_tuong_id,
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.THANH_TIEN_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI - line.TIEN_CK_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : (line.THANH_TIEN_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI - line.TIEN_CK_QUY_DOI) if self.LOAI_CHUNG_TU != 3536 else (line.THANH_TIEN + line.TIEN_THUE_GTGT - line.TIEN_CHIET_KHAU),
                    # 'currency_id' : loai_tien_vnd if self.LOAI_CHUNG_TU != 3536 else self.currency_id.id,
                    # 'TY_GIA' : 1 if self.LOAI_CHUNG_TU != 3536 else self.TY_GIA,
                    'LOAI_HACH_TOAN' : '2',
                })
                
                line_ids += [(0,0,data_ghi_co)]
                if line.TK_THUE_XK_ID and line.TIEN_THUE_XUAT_KHAU != 0:
                    data_thue_nk = data_goc.copy()
                    data_thue_nk.update({
                        'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_XK_ID.id,
                        'GHI_NO' : line.TIEN_THUE_XUAT_KHAU,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_XUAT_KHAU,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_thue_nk)]
                    data_thue_nk2 = data_goc.copy()
                    data_thue_nk2.update({
                        'TAI_KHOAN_ID' : line.TK_THUE_XK_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_XUAT_KHAU,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_XUAT_KHAU,
                        # 'currency_id' : loai_tien_vnd,
                        # 'TY_GIA' : 1,
                        'LOAI_HACH_TOAN' : '2',
                    })
                    line_ids += [(0,0,data_thue_nk2)]
            else:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : (line.THANH_TIEN_QUY_DOI - line.TIEN_THUE_XUAT_KHAU) if self.LOAI_CHUNG_TU == 3532 else line.THANH_TIEN_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : (line.THANH_TIEN) if self.LOAI_CHUNG_TU == 3532 else line.THANH_TIEN,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                })

                line_ids += [(0,0,data_ghi_no)]
                data_ghi_co1 = data_goc.copy()
                data_ghi_co1.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : (line.THANH_TIEN_QUY_DOI - line.TIEN_THUE_XUAT_KHAU) if self.LOAI_CHUNG_TU == 3532 else line.THANH_TIEN_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : (line.THANH_TIEN_QUY_DOI - line.TIEN_THUE_XUAT_KHAU) if self.LOAI_CHUNG_TU == 3532 else line.THANH_TIEN_QUY_DOI,
                    # 'currency_id' : loai_tien_vnd,
                    # 'TY_GIA' : 1,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_co1)]
                # Nếu có chiết khấu
                if line.TK_CHIET_KHAU_ID and (line.TIEN_CHIET_KHAU != 0 or line.TIEN_CK_QUY_DOI !=0):
                    data_chiet_khau = data_goc.copy()
                    data_chiet_khau.update({
                        'TAI_KHOAN_ID' : line.TK_CHIET_KHAU_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : line.TIEN_CK_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_CK_QUY_DOI,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        # 'currency_id' : loai_tien_vnd,
                        # 'TY_GIA' : 1,
                    })
                    line_ids += [(0,0,data_chiet_khau)]
                    data_chiet_khau2 = data_goc.copy()
                    data_chiet_khau2.update({
                        'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_CHIET_KHAU_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_CK_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                        
                        'LOAI_HACH_TOAN' : '2',
                    })
                    line_ids += [(0,0,data_chiet_khau2)]
                # Nếu có thuế gtgt
                if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT != 0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                    data_thue_gtgt = data_goc.copy()
                    data_thue_gtgt.update({
                        'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                        'GHI_NO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    })
                    line_ids += [(0,0,data_thue_gtgt)]
                    data_thue_gtgt2 = data_goc.copy()
                    data_thue_gtgt2.update({
                        'TAI_KHOAN_ID' : line.TK_THUE_GTGT_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
                        # 'currency_id' : loai_tien_vnd,
                        'LOAI_HACH_TOAN' : '2',
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        # 'TY_GIA' : 1,
                    })
                    line_ids += [(0,0,data_thue_gtgt2)]

                # Nếu là bán hàng xuất khẩu
                if self.LOAI_CHUNG_TU == 3532:
                    data_bh_xk = data_goc.copy()
                    data_bh_xk.update({
                        'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_XK_ID.id,
                        'GHI_NO' : line.TIEN_THUE_XUAT_KHAU,
                        # 'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_XUAT_KHAU,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_bh_xk)]
                    data_bh_xk2 = data_goc.copy()
                    data_bh_xk2.update({
                        'TAI_KHOAN_ID' : line.TK_THUE_XK_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_XUAT_KHAU,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_XUAT_KHAU,
                        # 'currency_id' : loai_tien_vnd,
                        'LOAI_HACH_TOAN' : '2',
                        # 'TY_GIA' : 1,
                    })
                    line_ids += [(0,0,data_bh_xk2)]
            thu_tu += 1

        if line_ids:
            for chi_tiet in line_ids:
                tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', chi_tiet[2].get('TAI_KHOAN_ID'))])
                if tai_khoan_id.CO_HACH_TOAN_NGOAI_TE == True:
                    chi_tiet[2]['currency_id'] = self.currency_id.id
                    chi_tiet[2]['TY_GIA'] = self.TY_GIA
                else:
                    chi_tiet[2]['currency_id'] = loai_tien_vnd
                    chi_tiet[2]['TY_GIA'] = 1
                    chi_tiet[2]['GHI_CO_NGUYEN_TE'] = chi_tiet[2].get('GHI_CO')
                    chi_tiet[2]['GHI_NO_NGUYEN_TE'] = chi_tiet[2].get('GHI_NO')
            
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True
    
    def ghi_so_ban_hang(self):
        line_ids = []
        thu_tu = 0
        for line in self.SALE_DOCUMENT_LINE_IDS:
            # so_hoa_don = None
            # ngay_hoa_don = None
            # if self.LAP_KEM_HOA_DON == False:
            #     if line.HOA_DON_ID:
            #         hoa_don_ban_hang = self.env['sale.ex.hoa.don.ban.hang'].search([('id', '=', line.HOA_DON_ID.id)])
            #         if hoa_don_ban_hang:
            #             so_hoa_don = hoa_don_ban_hang.SO_HOA_DON
            #             ngay_hoa_don = hoa_don_ban_hang.NGAY_HOA_DON
            #     else:
            #         if self.HOA_DON_IDS:
            #             if len(self.HOA_DON_IDS) == 1:
            #                 so_hoa_don = self.HOA_DON_IDS[0].SO_HOA_DON
            #                 ngay_hoa_don = self.HOA_DON_IDS[0].NGAY_HOA_DON
            # else:
            #     so_hoa_don = self.SO_HOA_DON
            #     ngay_hoa_don = self.NGAY_HOA_DON
            
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU_CTBH': self._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.TEN_HANG,
                'SO_TIEN': line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_NGUYEN_TE' : line.THANH_TIEN,
                'SO_HOA_DON' : self.SO_HOA_DON,
                'DVT_ID' : line.DVT_ID.id,
                'DVT_CHINH_ID' : line.DVT_ID.id,
                'TK_CHIET_KHAU_ID' : line.TK_CHIET_KHAU_ID.id,
                'PHAN_TRAM_CHIET_KHAU' : line.TY_LE_CK,
                'SO_TIEN_CHIET_KHAU' : line.TIEN_CK_QUY_DOI,
                'SO_TIEN_CHIET_KHAU_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                'SO_LUONG_THEO_DVT_CHINH' : line.SO_LUONG,
                # 'SO_TIEN_TRA_LAI' : line.THANH_TIEN,
                'PHAN_TRAM_THUE_VAT' : line.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT' : line.TIEN_THUE_GTGT_QUY_DOI,
                'TAI_KHOAN_VAT_ID' : line.TK_THUE_GTGT_ID.id,
                'HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
                'DON_GIA' : line.DON_GIA*self.TY_GIA,
                'KHO_ID' : line.KHO_ID.id if line.KHO_ID else line.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                'TK_NO_ID' : line.TK_NO_ID.id,
                'TK_CO_ID' : line.TK_CO_ID.id,
                'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
                'THU_TU_TRONG_CHUNG_TU' : thu_tu,
                'PHAN_TRAM_THUE_NHAP_KHAU' : line.THUE_XUAT_KHAU,
                'MA_HOP_DONG' : line.HOP_DONG_BAN_ID.SO_HOP_DONG,
                'TEN_HOP_DONG' : line.HOP_DONG_BAN_ID.TRICH_YEU,
                'MA_DIEU_KHOAN_THANH_TOAN' : self.DIEU_KHOAN_TT_ID.MA_DIEU_KHOAN,
                'TEN_DIEU_KHOAN_THANH_TOAN' : self.DIEU_KHOAN_TT_ID.TEN_DIEU_KHOAN,
                'DIEU_KHOAN_THANH_TOAN_ID' : self.DIEU_KHOAN_TT_ID.id,
                'SO_TIEN_NHAP_KHAU' : line.TIEN_THUE_XUAT_KHAU,
                'LA_HANG_KHUYEN_MAI' : line.LA_HANG_KHUYEN_MAI,
                'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                'DIA_CHI_DOI_TUONG' : self.DIA_CHI,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo master
        sbh = self.env['so.ban.hang'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_BAN_HANG_ID = sbh.id
        return True

    def ghi_so_kho(self):
        line_ids = []
        thu_tu = 0
        for line in self.SALE_DOCUMENT_LINE_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU_CTBH': self._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'SO_TIEN': line.TIEN_VON,
                'DON_GIA' : line.DON_GIA_VON,
                'SO_LUONG_XUAT_THEO_DVT_CHINH' : line.SO_LUONG,
                'CHI_TIET_ID' : line.id,
                'SO_LUONG_XUAT' : line.SO_LUONG,
                'SO_LUONG_NHAP' : 0,
                'SO_LUONG_NHAP_THEO_DVT_CHINH' : 0,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo move
        sk = self.env['so.kho'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_KHO_ID = sk.id
        return True
    

    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.SALE_DOCUMENT_LINE_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DON_GIA' : line.DON_GIA*self.TY_GIA,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
                'NGAY_HOA_DON' : self.NGAY_HOA_DON if self.LAP_KEM_HOA_DON == True else None,
                'SO_HOA_DON' : self.SO_HOA_DON if self.LAP_KEM_HOA_DON == True else None,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'SO_HOP_DONG' : line.HOP_DONG_BAN_ID.SO_HOP_DONG,
                'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
            })

            if self.LOAI_CHUNG_TU == 3534:
                doi_tuong_id = self.DON_VI_GIAO_DAI_LY_ID.id
            elif self.LOAI_CHUNG_TU == 3536:
                doi_tuong_id = self.DON_VI_UY_THAC_ID.id
            else:
                doi_tuong_id = self.DOI_TUONG_ID.id

            if self.LOAI_CHUNG_TU in (3534,3535,3536,3538):
                if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_NO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': line.THANH_TIEN_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI - line.TIEN_CK_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.THANH_TIEN + line.TIEN_THUE_GTGT - line.TIEN_CHIET_KHAU,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_ghi_no)]
                if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_CO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.THANH_TIEN_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI - line.TIEN_CK_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.THANH_TIEN + line.TIEN_THUE_GTGT - line.TIEN_CHIET_KHAU,
                        'DOI_TUONG_ID' : doi_tuong_id,
                        'LOAI_HACH_TOAN' : '2',
                    })
                    line_ids += [(0,0,data_ghi_co)]
                if line.TK_THUE_XK_ID and (line.TIEN_THUE_XUAT_KHAU !=0):
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_XK_ID.id,
                            'GHI_NO': line.TIEN_THUE_XUAT_KHAU,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                    if line.TK_THUE_XK_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_XK_ID.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_XUAT_KHAU,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DOI_TUONG_ID' : doi_tuong_id,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
            else:
                if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_NO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': line.THANH_TIEN_QUY_DOI - line.TIEN_THUE_XUAT_KHAU if self.LOAI_CHUNG_TU == 3532 else line.THANH_TIEN_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.THANH_TIEN,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_ghi_no)]
                if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_CO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.THANH_TIEN_QUY_DOI - line.TIEN_THUE_XUAT_KHAU if self.LOAI_CHUNG_TU == 3532 else line.THANH_TIEN_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.THANH_TIEN,
                        'DOI_TUONG_ID' : doi_tuong_id,
                        'LOAI_HACH_TOAN' : '2',
                    })
                    line_ids += [(0,0,data_ghi_co)]

                if line.TK_CHIET_KHAU_ID and (line.TIEN_CHIET_KHAU !=0 or line.TIEN_CK_QUY_DOI !=0):
                    if line.TK_CHIET_KHAU_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_CHIET_KHAU_ID.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': line.TIEN_CK_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_CHIET_KHAU_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_CK_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                            'DOI_TUONG_ID' : doi_tuong_id,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]

                if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                            'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                            'LOAI_HACH_TOAN' : '1',
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        })
                        line_ids += [(0,0,data_ghi_no)]
                    if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_GTGT_ID.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'DOI_TUONG_ID' : doi_tuong_id,
                            'LOAI_HACH_TOAN' : '2',
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        })
                        line_ids += [(0,0,data_ghi_co)]

                if self.LOAI_CHUNG_TU == 3532 and line.TIEN_THUE_XUAT_KHAU > 0:
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_XK_ID.id,
                            'GHI_NO': line.TIEN_THUE_XUAT_KHAU,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                    if line.TK_THUE_XK_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_XK_ID.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_XUAT_KHAU,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DOI_TUONG_ID' : doi_tuong_id,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        scn = self.env['so.cong.no'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CONG_NO_ID = scn.id
        return True
    
    @api.multi
    def action_bo_ghi_so(self, args):
        # Bỏ ghi sổ các references
        for record in self:
            # hoa_don = record.find_reference('sale.ex.hoa.don.ban.hang')
            # if hoa_don:
            #     hoa_don.action_bo_ghi_so()

            if record.HOA_DON_IDS:
                for hoa_don in record.HOA_DON_IDS:
                    hoa_don.action_bo_ghi_so()
            phieu_xuat = record.find_reference('stock.ex.nhap.xuat.kho')
            if phieu_xuat:
                phieu_xuat.action_bo_ghi_so()
            # Bỏ ghi lệnh lắp ráp
            if record.LAP_KEM_LENH_LAP_RAP:
                for ref in record.find_reference('stock.ex.lap.rap.thao.do', None):
                    # Vì các tham chiếu không có chứng từ liên quan, nên dùng trực tiếp hàm bo_ghi_so
                    for tc in ref.THAM_CHIEU:
                        tc.bo_ghi_so()
        return super(SALE_DOCUMENT, self).action_bo_ghi_so()


    def update_don_dat_hang(self,id_don_dat_hang):
        params = {
            'ID_DON_DAT_HANG' : id_don_dat_hang,
            }
        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
            --     id_chung_tu_ban_hang INTEGER := 289;

                id_don_dat_hang      INTEGER := %(ID_DON_DAT_HANG)s;

                format_so            INTEGER :=2;


            BEGIN

                SELECT value INTO  format_so
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY ;

                DROP TABLE IF EXISTS TMP_DON_DAT_HANG
                ;

                CREATE TEMP TABLE TMP_DON_DAT_HANG
                    AS
                        SELECT id AS "DON_DAT_HANG_ID"
                        FROM account_ex_don_dat_hang
                        WHERE id = id_don_dat_hang
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
                                    INNER JOIN sale_document_line AS SVD
                                        ON SOD."id" = SVD."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = SVD."MA_HANG_ID"
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
                                    , (-1) * COALESCE(SUM(ROUND(cast((CASE WHEN ((SOD."DVT_ID" ISNULL AND SVD."DVT_ID" ISNULL)
                                                                                OR
                                                                                (SOD."DVT_ID" NOTNULL AND SVD."DVT_ID" NOTNULL AND
                                                                                SOD."DVT_ID" = SVD."DVT_ID"))
                                    THEN SVD."SO_LUONG"
                                                                    ELSE (CASE WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                                                    '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                                                        THEN ROUND(
                                                                            cast((SVD."SO_LUONG" *
                                                                                    SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                AS NUMERIC), format_so)
                                                                            WHEN (SOD."TOAN_TU_QUY_DOI" = '0' AND
                                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" <>
                                                                                0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                                                THEN ROUND(cast((SVD."SO_LUONG_THEO_DVT_CHINH" /
                                                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                                AS
                                                                                                NUMERIC), format_so)
                                                                            ELSE SVD."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                                            END)
                                                                    END) AS NUMERIC), format_so)), 0) AS "SO_LUONG_DA_GIAO"
                                    , (-1) * COALESCE(SUM(SVD."SO_LUONG"),
                                                    0)                                                AS "SO_LUONG_DA_GIAO_THEO_DVT_CHINH"
                                FROM TMP_DON_DAT_HANG AS TOI
                                    INNER JOIN account_ex_don_dat_hang_chi_tiet AS SOD
                                        ON SOD."DON_DAT_HANG_CHI_TIET_ID" = TOI."DON_DAT_HANG_ID"
                                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet AS SVD
                                        ON SOD."id" = SVD."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = SVD."MA_HANG_ID"
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
                SET		"SO_LUONG_DA_GIAO_BAN_HANG" = COALESCE(SOD."SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG", 0) + COALESCE(TSOD."SO_LUONG_DA_GIAO", 0),
                        "SO_LUONG_DA_GIAO_BAN_HANG_THEO_DVT_CHINH" = COALESCE(SOD."SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG_THEO_DVT_CHINH", 0) + COALESCE(TSOD."SO_LUONG_DA_GIAO_THEO_DVT_CHINH", 0)
                FROM	account_ex_don_dat_hang_chi_tiet SOD1 LEFT JOIN TMP_KET_QUA AS TSOD on SOD1.id = TSOD."DON_DAT_HANG_CHI_TIET_ID"
                WHERE   SOD.id = SOD1.id
                        AND  exists(SELECT  FROM TMP_DON_DAT_HANG AS TOI WHERE   SOD."DON_DAT_HANG_CHI_TIET_ID" = TOI."DON_DAT_HANG_ID" FETCH FIRST 1 ROW  ONLY );

            END $$
            ;

            -- SELECT *
            -- FROM TMP_KET_QUA
            -- ;

        """  
        cr = self.env.cr

        return cr.execute(query, params)

    

    def update_trang_thai_don_dat_hang(self,id_don_dat_hang):
        params = {
            'ID_DON_DAT_HANG' : id_don_dat_hang,
            }
        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
                id_chung_tu_ban_hang INTEGER := NULL ;

                id_don_dat_hang_list      INTEGER := %(ID_DON_DAT_HANG)s;

                format_so            INTEGER :=2;

                lay_tu_chung_tu INTEGER:=1 ;--1: lấy từ CT bán hàng, 0: lấy từ Phiếu xuất kho

                imax INTEGER;
                i INTEGER:=1;
                rec record;
                don_dat_hang_id INTEGER;

                so_luong_yeu_cau INTEGER;
                so_luong_da_giao INTEGER;
                tong_so_dong_detail INTEGER;
                da_chon_het_so_dong_slyc INTEGER;
                so_dong_co_slyc_bang_0 INTEGER;
                tong_so_dong_co_slyc_bang_0 INTEGER;
                chenh_lech_so_dong INTEGER;


            BEGIN

                SELECT value INTO  format_so
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY ;

                DROP TABLE IF EXISTS TMP_CHI_TIET
                ;

                DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
            ;

            CREATE TEMP SEQUENCE TMP_KET_QUA_seq
            ;

                CREATE TEMP TABLE TMP_CHI_TIET(
                    "ROW_ID" INT DEFAULT NEXTVAL('TMP_KET_QUA_seq') PRIMARY KEY,
                    "ID_CHUNG_TU" INTEGER,
                    "DON_DAT_HANG_ID" INTEGER
                );

                INSERT  INTO TMP_CHI_TIET("ID_CHUNG_TU","DON_DAT_HANG_ID") (
                        SELECT DISTINCT
                                ID."SALE_DOCUMENT_ID" ,
                                ID."DON_DAT_HANG_ID"
                        FROM    sale_document_line ID
                        WHERE   ID."SALE_DOCUMENT_ID" = id_chung_tu_ban_hang
                        UNION ALL
                        SELECT DISTINCT
                                OD."NHAP_XUAT_ID" ,
                                OD."DON_DAT_HANG_ID"
                        FROM    stock_ex_nhap_xuat_kho_chi_tiet OD
                        WHERE   OD."NHAP_XUAT_ID" = id_chung_tu_ban_hang)
                ;

                INSERT  INTO TMP_CHI_TIET("ID_CHUNG_TU","DON_DAT_HANG_ID")(
                    SELECT NULL::INTEGER ,id FROM account_ex_don_dat_hang
            --         WHERE id = id_don_dat_hang_list
                );

                SELECT max("ROW_ID") INTO imax from TMP_CHI_TIET;

                FOR rec IN
                    select * from TMP_CHI_TIET

                LOOP
                    don_dat_hang_id := rec."DON_DAT_HANG_ID";
            --         RAISE NOTICE '%%', rec."DON_DAT_HANG_ID";
                    IF (SELECT "TINH_TRANG" FROM account_ex_don_dat_hang WHERE id = don_dat_hang_id FETCH FIRST 1 ROW ONLY ) <> '3'
                        THEN
                            SELECT  SUM("SO_LUONG") ,
                                    SUM(CASE lay_tu_chung_tu WHEN 1 THEN "SO_LUONG_DA_GIAO_BAN_HANG" ELSE "SO_LUONG_DA_GIAO_PX" END) INTO so_luong_yeu_cau,so_luong_da_giao
                            FROM    account_ex_don_dat_hang_chi_tiet
                            WHERE   "DON_DAT_HANG_CHI_TIET_ID" = don_dat_hang_id;

            --                 RAISE NOTICE '%%', so_luong_yeu_cau;
                        IF lay_tu_chung_tu = 1
                            THEN
                                tong_so_dong_detail := (SELECT COUNT(*) FROM sale_document_line WHERE "DON_DAT_HANG_ID" = don_dat_hang_id) +
                                (SELECT COUNT(*) FROM sale_ex_tra_lai_hang_ban_chi_tiet WHERE "DON_DAT_HANG_ID" = don_dat_hang_id );
                            ELSE
                                tong_so_dong_detail := (SELECT COUNT(*) FROM stock_ex_nhap_xuat_kho_chi_tiet WHERE "DON_DAT_HANG_ID" = don_dat_hang_id) +
                                    (SELECT COUNT(*) FROM stock_ex_nhap_xuat_kho_chi_tiet WHERE "DON_DAT_HANG_ID" = don_dat_hang_id );
                        END IF;

                        SELECT COUNT(*) INTO so_dong_co_slyc_bang_0 FROM account_ex_don_dat_hang_chi_tiet  WHERE "DON_DAT_HANG_CHI_TIET_ID" = don_dat_hang_id AND "SO_LUONG" = 0;
                        IF so_dong_co_slyc_bang_0 = 0
                            THEN
                            da_chon_het_so_dong_slyc = 1;
                            ELSE
                                IF lay_tu_chung_tu = 1
                                    THEN
                                        SELECT COUNT(*) INTO  tong_so_dong_co_slyc_bang_0
                                        FROM account_ex_don_dat_hang_chi_tiet OD
                                            INNER JOIN sale_document_line VD ON OD."id" = VD."DON_DAT_HANG_ID"
                                        WHERE OD."DON_DAT_HANG_CHI_TIET_ID" = don_dat_hang_id AND OD."SO_LUONG" = 0;
                                    ELSE
                                    SELECT COUNT(*) INTO  tong_so_dong_co_slyc_bang_0
                                    FROM account_ex_don_dat_hang_chi_tiet OD
                                        INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet ID ON OD."id" = ID."DON_DAT_HANG_ID"
                                        WHERE OD."DON_DAT_HANG_CHI_TIET_ID" = don_dat_hang_id AND OD."SO_LUONG" = 0;
                                END IF;

                                IF so_dong_co_slyc_bang_0 = tong_so_dong_co_slyc_bang_0
                                    THEN
                                        da_chon_het_so_dong_slyc = 1;
                                    ELSE
                                        da_chon_het_so_dong_slyc = 0;
                                END IF;

                        END IF;

                        --Nếu không có dòng nào được chọn thì set là "Chưa thực hiện"
                        IF tong_so_dong_detail = 0
                            THEN
                                UPDATE account_ex_don_dat_hang SET "TINH_TRANG" = '0' WHERE id = don_dat_hang_id;
                            ELSE
                                IF so_luong_yeu_cau > 0
                                    THEN
                                        --Biến đếm số VTHH chưa giao hết
                                        SELECT	COUNT(*) INTO chenh_lech_so_dong
                                        FROM	account_ex_don_dat_hang_chi_tiet
                                        WHERE	"DON_DAT_HANG_CHI_TIET_ID" = don_dat_hang_id AND "SO_LUONG" > (CASE lay_tu_chung_tu WHEN 1 THEN "SO_LUONG_DA_GIAO_BAN_HANG" ELSE "SO_LUONG_DA_GIAO_PX" END);
                                        --Nếu còn mặt hàng chưa giao thì tình trạng là "Đang thực hiện"
                                        IF chenh_lech_so_dong > 0 OR (chenh_lech_so_dong = 0 AND da_chon_het_so_dong_slyc = 0)
                                            THEN
                                                UPDATE account_ex_don_dat_hang SET "TINH_TRANG" = '1' WHERE id = don_dat_hang_id;
                                            ELSE
                                                UPDATE account_ex_don_dat_hang SET "TINH_TRANG" = '2' WHERE id = don_dat_hang_id;
                                        END IF;
                                ELSE
                                    IF so_dong_co_slyc_bang_0 = tong_so_dong_co_slyc_bang_0
                                        THEN
                                            UPDATE account_ex_don_dat_hang SET "TINH_TRANG" = '2' WHERE id = don_dat_hang_id;
                                        ELSE
                                            UPDATE account_ex_don_dat_hang SET "TINH_TRANG" = '1' WHERE id = don_dat_hang_id;
                                    END IF;

                                END IF;
                        END IF;

                    END IF;
                    i := i+1;
                END LOOP;


            END $$
            ;

            -- SELECT *
            -- FROM TMP_CHI_TIET
            -- ;

        """  
        cr = self.env.cr

        return cr.execute(query, params)