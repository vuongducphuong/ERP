# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_TRA_LAI_HANG_MUA(models.Model):
    _name = 'purchase.ex.tra.lai.hang.mua'
    _description = 'Chứng từ trả lại hàng mua'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    LAP_TU = fields.Selection([('CHUNG_TU_MUA_HANG', 'Chứng từ mua hàng'), ('CHUNG_TU_MUA_HANG_CHI_TIET', 'Chi tiết mua hàng'), ], string='Lập từ', help='Lập từ', store=False)
    CHUNG_TU_MUA_HANG = fields.Many2one('purchase.document', string='Chứng từ MH', help='Chứng từ mua hàng')
    CHUNG_TU_MUA_HANG_CHI_TIET = fields.Many2many('purchase.document.line', string='Chi tiết MH', help='Chứng từ mua hàng chi tiết', store=False)
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên NCC', help='Tên nhà cung cấp')
    NGUOI_NHAN_HANG = fields.Char(string='Người nhận hàng', help='Người nhận hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    LY_DO_XUAT = fields.Char(string='Lý do xuất', help='Lý do xuất',related='DIEN_GIAI')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng')
    KEM_THEO = fields.Char(string='Kèm theo CT gốc ', help='Kèm theo chứng từ gốc')
    KEM_THEO_PT = fields.Char(string='Kèm theo CT gốc ', help='Kèm theo chứng từ gốc')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now,required=True)
    NGAY_CHUNG_TU_PHIEU_CHI = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now,required=True)
    NGAY_CHUNG_TU_PHIEU_XUAT = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now,required=True)
    SO_PHIEU_XUAT = fields.Char(string='Số phiếu xuất', help='Số phiếu xuất', auto_num='stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_XUAT_KHO')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='TK ngân hàng', help='Tài khoản ngân hàng')
    HINH_THUC_TT = fields.Selection([('TIEN_MAT', 'Tiền mặt'), ('CHUYEN_KHOAN', 'Chuyển khoản'), ('TM_CK', 'TM/CK'), ], string='Hình thức TT', help='Hình thức thanh toán',default='TM_CK',required=True)
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hợp đồng')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now,required=True)
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU', )
    LY_DO_NOP = fields.Char(string='Lý do nộp', help='Lý do nộp')
    SO_PHIEU_THU = fields.Char(string='Số phiếu thu', help='Số phiếu thu', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_PHIEU_THU')
    SO_CHUNG_TU_GIAM_TRU_CONG_NO = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='purchase_ex_tra_lai_mua_hang_SO_CHUNG_TU')
    NGUOI_NOP = fields.Char(string='Người nộp', help='Người nộp')
    CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_MUA_HANG_ID = fields.Many2one('so.mua.hang', ondelete='set null')
    SO_KHO_ID = fields.Many2one('so.kho', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    HOA_DON_REF_ID = fields.Char(help='Ref ID của hóa đơn được import')

    CHI_TIET_HANG_HOA = fields.Selection([
        ('hang_tien', 'Hàng tiền'),
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')

    PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS = fields.One2many('purchase.ex.tra.lai.hang.mua.chi.tiet', 'CHUNG_TU_TRA_LAI_HANG_MUA_ID', string='Chi tiết chứng từ trả lại hàng mua', copy=True)
    selection_chung_tu_mua_hang = fields.Selection([
        ('giam_tru_cong_no', 'Giảm trừ công nợ'),
        ('thu_tien_mat','Thu tiền mặt'),
        ], default='giam_tru_cong_no',string=" ")
    TRA_LAI_HANG_TRONG_KHO = fields.Boolean(string='Trả lại hàng trong kho', help='Trả lại hàng trong kho', default='True') 
    IN_KEM_BANG_KE = fields.Boolean(string='In kèm bảng kê', help='In kèm bảng kê')
    SO = fields.Char(string='Số', help='Số')
    NGAY = fields.Date(string='Ngày', help='Ngày')
    TEN_MAT_HANG_CHUNG = fields.Char(string='Tên mặt hàng chung', help='Tên mặt hàng chung')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', compute='_compute_SO_CHUNG_TU', store=True, )
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng',compute='tinhtongtien',store=True, currency_field='currency_id')    
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng',compute='tinhtongtien',store=True, currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',compute='tinhtongtien',store=True, currency_field='currency_id')
    TONG_TIEN_HANG_QĐ = fields.Monetary(string='', help='Tổng tiền hàng quy đổi',compute='tinhtongtien',store=True, currency_field='base_currency_id')    
    TIEN_THUE_GTGT_QĐ = fields.Monetary(string='', help='Tiền thuế giá trị gia tăng quy đổi',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QĐ = fields.Monetary(string='', help='Tổng tiền thanh toán quy đổi',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True,compute='set_loai_chung_tu_tra_lai_hang_mua')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    PHIEU_XUAT_ID = fields.Many2one('stock.ex.nhap.xuat.kho', string='Phiếu xuất kho')
    PHIEU_THU_ID = fields.Many2one('account.ex.phieu.thu.chi', string='Phiếu thu tiền')

    DIA_CHI_NGUOI_NOP = fields.Char(string='Địa chỉ người nộp', help='Địa chỉ Địa chỉ người nộp')


    # _sql_constraints = [
	# ('SO_CHUNG_TU_TLHM_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	# ]

    @api.onchange('CHUNG_TU_MUA_HANG_CHI_TIET')
    def _onchange_CHUNG_TU_MUA_HANG_CHI_TIET(self):
        ctbhct_ids = [line.MUA_HANG_CHI_TIET_ID.id for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS if line.MUA_HANG_CHI_TIET_ID]
        default = self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
        for line in self.CHUNG_TU_MUA_HANG_CHI_TIET:
            if self.DOI_TUONG_ID and line.order_id.DOI_TUONG_ID.id != self.DOI_TUONG_ID.id:
                raise ValidationError("Nhà cung cấp trong các chứng từ chi tiết đã chọn không đồng nhất. Vui lòng chọn lại!")
            elif not self.DOI_TUONG_ID:
                self.DOI_TUONG_ID = line.order_id.DOI_TUONG_ID.id
                self.TEN_KHACH_HANG = line.order_id.DOI_TUONG_ID.HO_VA_TEN
            if line.id not in ctbhct_ids:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': line.MA_HANG_ID,
                    'TEN_HANG': line.name,
                    'DVT_ID': line.DVT_ID.id,
                    'SO_LUONG':line.SO_LUONG,
                    'DON_GIA':(line.THANH_TIEN_QUY_DOI-line.TIEN_CHIET_KHAU_QUY_DOI) / ((line.SO_LUONG * self.TY_GIA) or 1),
                    'THANH_TIEN':(line.THANH_TIEN_QUY_DOI-line.TIEN_CHIET_KHAU_QUY_DOI) / (self.TY_GIA or 1),
                    'KHO_ID': line.KHO_ID.id,
                    'TK_KHO_ID': line.TK_KHO_ID.id,
                    'THANH_TIEN_QUY_DOI':line.THANH_TIEN_QUY_DOI,
                    'TY_LE_CK_PHAN_TRAM':line.TY_LE_CK,
                    'SO_CHUNG_TU_ID': line.order_id.id,
                    'DIEN_GIAI_THUE':line.DIEN_GIAI_THUE,
                    'PHAN_TRAM_THUE_GTGT_ID': line.THUE_GTGT_ID.id,
                    'TIEN_THUE_GTGT':line.TIEN_THUE_GTGT_QUY_DOI / (self.TY_GIA or 1),
                    'TIEN_THUE_GTGT_QUY_DOI':line.TIEN_THUE_GTGT_QUY_DOI,
                    'MUA_HANG_CHI_TIET_ID': line.id,
                    'DON_VI_ID': line.DON_VI_ID.id,
                    'SO_HD_MUA_HANG': line.order_id.SO_HOA_DON,
                    'NGAY_HD_MUA_HANG': line.order_id.NGAY_HOA_DON,
                })
                self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS += self.env['purchase.ex.tra.lai.hang.mua.chi.tiet'].new(new_data)
    
    @api.onuichange('CHUNG_TU_MUA_HANG_CHI_TIET')
    def _onchange_CHUNG_TU_MUA_HANG_CHI_TIET1(self):
        self.CHUNG_TU_MUA_HANG_CHI_TIET = []

    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))

    
    @api.model
    def create(self, values):
        result = super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).create(values)
        if self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            self.up_date_don_mua_hang()
        return result

    @api.multi
    def write(self, values):
        result = super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).write(values)
        if self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            self.up_date_don_mua_hang()
        return result

    def up_date_don_mua_hang(self):
        arr_don_mua_hang = []
        for chi_tiet in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                if chi_tiet.CHI_TIET_DON_MUA_HANG_ID:
                    if chi_tiet.CHI_TIET_DON_MUA_HANG_ID.id not in arr_don_mua_hang:
                        arr_don_mua_hang.append(chi_tiet.CHI_TIET_DON_MUA_HANG_ID.id)
                        chi_tiet.CHI_TIET_DON_MUA_HANG_ID.DON_MUA_HANG_CHI_TIET_ID.write({'NGAY_GIAO_HANG' : self.NGAY_HACH_TOAN})
        if arr_don_mua_hang:
            tupple_don_mua_hang = tuple(arr_don_mua_hang)
            self.cap_nhat_don_mua_hang(tupple_don_mua_hang)

    
    @api.multi
    def unlink(self):
        for record in self:
            arr_don_mua_hang = []
            if record.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                for chi_tiet in record.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                    if chi_tiet.CHI_TIET_DON_MUA_HANG_ID:
                        arr_don_mua_hang.append(chi_tiet.CHI_TIET_DON_MUA_HANG_ID.id)
        result = super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).unlink()
        if arr_don_mua_hang:
            tupple_don_mua_hang = tuple(arr_don_mua_hang)
            self.cap_nhat_don_mua_hang(tupple_don_mua_hang)
            for chi_tiet in arr_don_mua_hang:
                cap_nhat = self.env['purchase.ex.don.mua.hang.chi.tiet'].search([('id', '=',chi_tiet)],limit=1).DON_MUA_HANG_CHI_TIET_ID
                cap_nhat.write({'NGAY_GIAO_HANG' : False})
        return result

    
    

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ mua hàng
    def lay_du_lieu_chung_tu_mua_hang(self, args):
        new_line =[[5]]
        chung_tu_mua_hang_id = args.get('chung_tu_mua_hang_id')
        thong_tin_chung_tu_master = self.env['purchase.document'].search([('id', '=', chung_tu_mua_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        ten_doi_tuong = thong_tin_chung_tu_master['TEN_DOI_TUONG']
        so_hd_mua_hang = thong_tin_chung_tu_master['SO_HOA_DON']
        ngay_hd_mua_hang = thong_tin_chung_tu_master['NGAY_HOA_DON']
        loai_chung_tu_mh = thong_tin_chung_tu_master.LOAI_CHUNG_TU_MH
        danh_sach_chung_tu_mua_hang = self.env['purchase.document.line'].search([('order_id', '=', chung_tu_mua_hang_id)])
        if danh_sach_chung_tu_mua_hang:
            default = self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
            for ct_mh in danh_sach_chung_tu_mua_hang:
                
                new_data = default.copy()
                if loai_chung_tu_mh in ('trong_nuoc_nhap_kho','nhap_khau_nhap_kho'):
                    new_data.update({'TK_CO_ID' : ct_mh.MA_HANG_ID.lay_tai_khoan_kho()})
                new_data.update({
                    'MA_HANG_ID': [ct_mh['MA_HANG_ID'].id,ct_mh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_mh['name'],
                    'DVT_ID': [ct_mh['DVT_ID'].id,ct_mh['DVT_ID'].name],
                    'KHO_ID': [ct_mh['KHO_ID'].id,ct_mh['KHO_ID'].MA_KHO],
                    'DON_VI_ID': [ct_mh['DON_VI_ID'].id,ct_mh['DON_VI_ID'].MA_DON_VI],
                    'SO_LUONG': ct_mh['SO_LUONG'],
                    'DON_GIA': (ct_mh['THANH_TIEN']-ct_mh['TIEN_CHIET_KHAU'])/(ct_mh['SO_LUONG'] or 1),
                    'THANH_TIEN': ct_mh['THANH_TIEN']-ct_mh['TIEN_CHIET_KHAU'],
                    'THANH_TIEN_QUY_DOI': ct_mh['THANH_TIEN_QUY_DOI'],
                    'DIEN_GIAI_THUE': ct_mh['DIEN_GIAI_THUE'],
                    'PHAN_TRAM_THUE_GTGT_ID': [ct_mh['THUE_GTGT_ID'].id,ct_mh['THUE_GTGT_ID'].name],
                    'TIEN_THUE_GTGT': ct_mh['TIEN_THUE_GTGT'],
                    'TIEN_THUE_GTGT_QUY_DOI': ct_mh['TIEN_THUE_GTGT_QUY_DOI'],
                    'SO_CHUNG_TU':[chung_tu_mua_hang_id,args.get('chung_tu_mua_hang_name')],
                    'SO_HD_MUA_HANG': so_hd_mua_hang,
                    'NGAY_HD_MUA_HANG': ngay_hd_mua_hang,
                    'TIEN_CHIET_KHAU': ct_mh['TIEN_CHIET_KHAU'],
                    'TIEN_CHIET_KHAU_QUY_DOI': ct_mh['TIEN_CHIET_KHAU_QUY_DOI'],
                    'MUA_HANG_CHI_TIET_ID': [ct_mh.id,ct_mh.name],
                    'CHI_TIET_DON_MUA_HANG_ID': ct_mh.CHI_TIET_DON_MUA_HANG_ID.id,
                   })
                new_line += [(0,0,new_data)]
        return {'PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                'TEN_NHA_CUNG_CAP': ten_doi_tuong,
                'currency_id': [thong_tin_chung_tu_master.currency_id.id, thong_tin_chung_tu_master.currency_id.name]}

    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU
    
    @api.depends('selection_chung_tu_mua_hang','TRA_LAI_HANG_TRONG_KHO')
    def _compute_SO_CHUNG_TU(self):
        for record in self:
            if record.TRA_LAI_HANG_TRONG_KHO:
                    record.SO_CHUNG_TU = record.SO_PHIEU_XUAT
            else:
                if record.selection_chung_tu_mua_hang == 'thu_tien_mat':
                    record.SO_CHUNG_TU = record.SO_PHIEU_THU
                else:
                    record.SO_CHUNG_TU = record.SO_CHUNG_TU_GIAM_TRU_CONG_NO


    @api.depends('selection_chung_tu_mua_hang','TRA_LAI_HANG_TRONG_KHO')
    def set_loai_chung_tu_tra_lai_hang_mua(self):
        for record in self:
            if record.TRA_LAI_HANG_TRONG_KHO==True:
                if record.selection_chung_tu_mua_hang=='giam_tru_cong_no':
                    record.LOAI_CHUNG_TU = 3030
                else:
                    record.LOAI_CHUNG_TU = 3031
            else : 
                if record.selection_chung_tu_mua_hang=='giam_tru_cong_no':
                    record.LOAI_CHUNG_TU = 3032
                else:
                    record.LOAI_CHUNG_TU = 3033

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            line.tinh_tien_quy_doi()

    @api.onchange('DOI_TUONG_ID')
    def laythongtinnhacungcap(self):
        self.TEN_NHA_CUNG_CAP = self.DOI_TUONG_ID.HO_VA_TEN
        self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
        self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
        self.NHAN_VIEN_ID = self.DOI_TUONG_ID.NHAN_VIEN_ID.id
        tai_khoan_ngan_hang = self.env['danh.muc.doi.tuong.chi.tiet'].search([('DOI_TUONG_ID', '=',self.DOI_TUONG_ID.id)],limit=1)
        if tai_khoan_ngan_hang:
            self.TK_NGAN_HANG_ID = tai_khoan_ngan_hang.id
        if self.DOI_TUONG_ID.company_type=='person':
            self.NGUOI_NHAN_HANG = self.DOI_TUONG_ID.HO_VA_TEN
            self.NGUOI_NOP = self.DOI_TUONG_ID.HO_VA_TEN
        else:
            self.NGUOI_NHAN_HANG =''
            self.NGUOI_NOP =''
        # Reset các chứng từ chi tiết có đối tượng
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            if line.MUA_HANG_CHI_TIET_ID and line.MUA_HANG_CHI_TIET_ID.DOI_TUONG_ID.id != self.DOI_TUONG_ID.id:
                self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS = []
                break
    
    @api.onchange('selection_chung_tu_mua_hang')
    def update_selection_chung_tu_mua_hang(self):
        if self.selection_chung_tu_mua_hang=='thu_tien_mat':
            self.HINH_THUC_TT='TIEN_MAT'
        else:
            self.HINH_THUC_TT='TM_CK'

    @api.depends('PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS')
    def tinhtongtien(self):
        for order in self:
            tongtienhang = tienthuegtgt = tongtienthanhtoan =0.0
            tong_tien_hang_qđ = tong_tien_thue_gtgt_qđ = tong_tien_thanh_toan_qđ=0.0
            for line in order.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                tongtienhang += line.THANH_TIEN
                tienthuegtgt += line.TIEN_THUE_GTGT
                tongtienthanhtoan = tongtienhang + tienthuegtgt

                tong_tien_hang_qđ += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qđ += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_thanh_toan_qđ= tong_tien_hang_qđ + tong_tien_thue_gtgt_qđ
            order.update({
                'TONG_TIEN_HANG': tongtienhang,
                'TIEN_THUE_GTGT': tienthuegtgt,
                'TONG_TIEN_THANH_TOAN': tongtienthanhtoan,

                'TONG_TIEN_HANG_QĐ': tong_tien_hang_qđ,
                'TIEN_THUE_GTGT_QĐ': tong_tien_thue_gtgt_qđ,
                'TONG_TIEN_THANH_TOAN_QĐ': tong_tien_thanh_toan_qđ,
            })

    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).default_get(fields)
        rec['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')]).id
        rec['SO'] = ''
        rec['NGAY'] = ''
        return rec

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_mua_hang()
            record.ghi_so_kho()
            record.ghi_so_cong_no()
        self.write({'state':'da_ghi_so'})
    
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'NHAN_VIEN_ID' : self.NHAN_VIEN_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'MA_HANG_ID' : line.MA_HANG_ID.id,
                'DIEN_GIAI_CHUNG' : self.LY_DO_XUAT,
                'DIEN_GIAI' : line.TEN_HANG,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.THANH_TIEN,
                'GHI_NO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.THANH_TIEN,
                'GHI_CO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]

            # ghi sổ thuế gtgt
            if line.TIEN_THUE_GTGT and (line.TIEN_THUE_GTGT > 0 or line.TIEN_THUE_GTGT_QUY_DOI > 0):
                data_thue_gtgt = data_ghi_no.copy()
                data_thue_gtgt.update({
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                    'GHI_NO' : line.TIEN_THUE_GTGT,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_thue_gtgt)]

                data_thue_gtgt2 = data_thue_gtgt.copy()
                data_thue_gtgt2.update({
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'TAI_KHOAN_ID' : line.TK_THUE_GTGT_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.TIEN_THUE_GTGT,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_thue_gtgt2)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_mua_hang(self):
        line_ids = []
        thu_tu = 0
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'DIEN_GIAI': line.TEN_HANG,
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'SO_LUONG' : 0,
                'DON_GIA' : line.DON_GIA,
                'DIEN_GIAI_CHUNG' : self.LY_DO_XUAT,
                'DVT_ID' : line.DVT_ID.id,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                # 'SO_TIEN': line.THANH_TIEN,
                'PHAN_TRAM_THUE_VAT' : line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT' : -1*line.TIEN_THUE_GTGT_QUY_DOI,
                'SO_TIEN_VAT_NGUYEN_TE' : -1*line.TIEN_THUE_GTGT,
                'TAI_KHOAN_VAT_ID' : line.TK_THUE_GTGT_ID.id,
                'HOP_DONG_ID' : line.HOP_DONG_MUA_ID.id,
                'TK_NO_ID' : line.TK_CO_ID.id,
                'TK_CO_ID' : line.TK_NO_ID.id,
                'SO_LUONG_TRA_LAI' : line.SO_LUONG,
                'SO_TIEN_TRA_LAI' : line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_TRA_LAI_NGUYEN_TE' : line.THANH_TIEN,
                'TEN_DOI_TUONG' : self.TEN_NHA_CUNG_CAP,
                'DIA_CHI_DOI_TUONG' : self.DIA_CHI,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo master
        smh = self.env['so.mua.hang'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_MUA_HANG_ID = smh.id
        return True

    def ghi_so_kho(self):
        line_ids = []
        thu_tu = 0
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'TK_NO_ID' : line.TK_CO_ID.id,
                'TK_CO_ID' : line.TK_NO_ID.id,
                'SO_TIEN_NHAP' : 0,
                'SO_TIEN_XUAT' : line.THANH_TIEN_QUY_DOI,
                'KHO_ID' : line.KHO_ID.id,
                'DVT_ID' : line.DVT_ID.id,
                'SO_LUONG_NHAP' : 0,
                'SO_LUONG_XUAT' : line.SO_LUONG,
                'DON_GIA' : line.DON_GIA,
                'LOAI_KHU_VUC_NHAP_XUAT' : '3',
                'LOAI_KHONG_CAP_NHAT_GIA_XUAT' : '2',
                'KHONG_CAP_NHAT_GIA_XUAT' : True,
            })
            line_ids += [(0,0,data_ghi_no)]
            thu_tu += 1
        # Tạo master
        sk = self.env['so.kho'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_KHO_ID = sk.id
        return True

    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.LY_DO_XUAT,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'TEN_DOI_TUONG' : self.TEN_NHA_CUNG_CAP,
            })
            if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TK_ID': line.TK_NO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.THANH_TIEN_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.THANH_TIEN,
                    'GHI_CO': 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_ghi_no)]
                thu_tu += 1
            if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_co = data_goc.copy()
                data_ghi_co.update({
                    'TK_ID': line.TK_CO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                    'GHI_NO': 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO': line.THANH_TIEN_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.THANH_TIEN,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_co)]
                thu_tu += 1
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT > 0 or line.TIEN_THUE_GTGT_QUY_DOI > 0):
                if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_NO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                        'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    })
                    line_ids += [(0,0,data_ghi_no)]
                    thu_tu += 1
                if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_THUE_GTGT_ID.id,
                        'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'LOAI_HACH_TOAN' : '2',
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
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

    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()

    def cap_nhat_don_mua_hang(self,arr_id_don_dat_hang_chi_tiet):
        params = {
            'ARR_ID_DON_DAT_HANG_CHI_TIET' : arr_id_don_dat_hang_chi_tiet,
            }
        query = """   
                DO LANGUAGE plpgsql $$
                DECLARE
                
                    --@arrPUOrderRefDetailID
                
                    PHAN_THAP_PHAN_SO_LUONG INT;
                
                BEGIN
                
                    SELECT value
                    INTO PHAN_THAP_PHAN_SO_LUONG
                    FROM ir_config_parameter
                    WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                    FETCH FIRST 1 ROW ONLY
                    ;
                
                    --Số đã nhận = (Tổng phát sinh hiện tại + Số đã nhận từ năm trước)
                    UPDATE purchase_ex_don_mua_hang_chi_tiet POD1
                    SET "SO_LUONG_NHAN" =
                    COALESCE(PU."SO_LUONG_DA_NHAN", 0)
                    + COALESCE(POD."SO_LUONG_NHAN_NAM_TRUOC", 0) -
                    COALESCE(PUR."SO_LUONG_TRA_LAI", 0)
                    FROM purchase_ex_don_mua_hang_chi_tiet POD
                        LEFT JOIN
                        (SELECT
                            PVD."CHI_TIET_DON_MUA_HANG_ID"
                            , COALESCE(SUM(ROUND(CASE WHEN ((PVD."DVT_ID" IS NULL AND PD."DVT_ID" IS NULL) OR
                                                            (PVD."DVT_ID" IS NOT NULL AND PD."DVT_ID" IS NOT NULL AND
                                                            PVD."DVT_ID" = PD."DVT_ID")) -- Cùng ĐVT thì lấy giá trị cột Số lượng
                                THEN PVD."SO_LUONG"
                                                ELSE (CASE WHEN (PD."TOAN_TU_QUY_DOI" =
                                                                'CHIA') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên ĐMH = SL theo ĐVC trên CT mua hàng * tỷ lệ CĐ trên ĐMH
                                                    THEN ROUND(
                                                        CAST((PVD."SO_LUONG_THEO_DVT_CHINH" * PD."TY_LE_CHUYEN_DOI_RA_DVT_CHINH") AS
                                                            NUMERIC),
                                                        PHAN_THAP_PHAN_SO_LUONG)
                                                        WHEN (PD."TOAN_TU_QUY_DOI" = 'NHAN' AND PD."TY_LE_CHUYEN_DOI_RA_DVT_CHINH" !=
                                                                                                0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên ĐMH <> 0 thì SL theo ĐVT trên ĐMH = SL theo ĐVC trên CT mua hàng / tỷ lệ CĐ trên ĐMH
                                                            THEN ROUND(CAST((
                                                                                PVD."SO_LUONG_THEO_DVT_CHINH" /
                                                                                PD."TY_LE_CHUYEN_DOI_RA_DVT_CHINH") AS NUMERIC),
                                                                    PHAN_THAP_PHAN_SO_LUONG)
                                                        ELSE PVD."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CT mua hàng
                                                        END
                                                ) END, PHAN_THAP_PHAN_SO_LUONG)), 0) AS "SO_LUONG_DA_NHAN"
                        FROM purchase_document_line AS PVD
                            INNER JOIN purchase_ex_don_mua_hang_chi_tiet AS PD ON PVD."CHI_TIET_DON_MUA_HANG_ID" = PD."id"
                        GROUP BY PVD."CHI_TIET_DON_MUA_HANG_ID"
                        ) PU ON PU."CHI_TIET_DON_MUA_HANG_ID" = POD.id
                
                        LEFT JOIN
                        (
                            SELECT
                                PVD."CHI_TIET_DON_MUA_HANG_ID"
                                , COALESCE(SUM(ROUND(CAST((CASE WHEN ((PVD."DVT_ID" IS NULL AND PD."DVT_ID" IS NULL) OR
                                                                    (PVD."DVT_ID" IS NOT NULL AND PD."DVT_ID" IS NOT NULL AND
                                                                    PVD."DVT_ID" =
                                                                    PD."DVT_ID")) -- Cùng ĐVT thì lấy giá trị cột Số lượng
                                THEN PVD."SO_LUONG"
                                                        ELSE (CASE WHEN (PD."TOAN_TU_QUY_DOI" =
                                                                            'CHIA') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên ĐMH = SL theo ĐVC trên CT mua hàng * tỷ lệ CĐ trên ĐMH
                                                            THEN ROUND(
                                                                CAST((PVD."SO_LUONG_DVT_CHINH" * PD."TY_LE_CHUYEN_DOI_RA_DVT_CHINH")
                                                                        AS NUMERIC),
                                                                PHAN_THAP_PHAN_SO_LUONG)
                                                                WHEN (PD."TOAN_TU_QUY_DOI" = 'NHAN' AND
                                                                    PD."TY_LE_CHUYEN_DOI_RA_DVT_CHINH" !=
                                                                    0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên ĐMH <> 0 thì SL theo ĐVT trên ĐMH = SL theo ĐVC trên CT mua hàng / tỷ lệ CĐ trên ĐMH
                                                                    THEN ROUND(CAST((PVD."SO_LUONG_DVT_CHINH" /
                                                                                    PD."TY_LE_CHUYEN_DOI_RA_DVT_CHINH") AS NUMERIC),
                                                                                PHAN_THAP_PHAN_SO_LUONG)
                                                                ELSE PVD."SO_LUONG_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CT mua hàng
                                                                END
                                                        ) END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)), 0)
                                AS "SO_LUONG_TRA_LAI"
                            FROM purchase_ex_tra_lai_hang_mua_chi_tiet AS PVD
                                INNER JOIN purchase_ex_don_mua_hang_chi_tiet AS PD ON PVD."CHI_TIET_DON_MUA_HANG_ID" = PD."id"
                            GROUP BY PVD."CHI_TIET_DON_MUA_HANG_ID"
                        ) AS PUR ON PUR."CHI_TIET_DON_MUA_HANG_ID" = POD.id
                    WHERE pod1.id = pod.id AND pod.id IN %(ARR_ID_DON_DAT_HANG_CHI_TIET)s --@arrPUOrderRefDetailID
                    ;
                
                -- Cập nhật trạng thái của đơn mua hàng là chưa thực hiện
                    UPDATE purchase_ex_don_mua_hang PO
                    SET "TINH_TRANG" = '0'
                    FROM
                        purchase_ex_don_mua_hang_chi_tiet AS POD
                    WHERE PO."id" = POD."DON_MUA_HANG_CHI_TIET_ID"
                
                        AND NOT EXISTS(SELECT *
                                        FROM purchase_ex_don_mua_hang_chi_tiet AS PD
                                        WHERE
                
                                            PD."SO_LUONG_NHAN" > 0
                                            -- đề phòng trường hợp lập đơn mua hàng xong lập trả lại hàng mua luôn
                                            AND PD."DON_MUA_HANG_CHI_TIET_ID" = PO."id")
                        AND NOT EXISTS(SELECT *
                                        FROM purchase_ex_don_mua_hang_chi_tiet AS POD2
                                        WHERE POD2."SO_LUONG_NHAN" = 0
                                            AND POD2."SO_LUONG" = 0
                                            AND (SELECT COUNT(*)
                                                    FROM purchase_document_line AS PVD
                                                    WHERE PVD."CHI_TIET_DON_MUA_HANG_ID" = POD2."id"
                                                ) > 0
                                            AND POD2."DON_MUA_HANG_CHI_TIET_ID" = PO.id)
                        AND POD.id IN %(ARR_ID_DON_DAT_HANG_CHI_TIET)s --@arrPUOrderRefDetailID
                
                    ;
                
                
                    --Cập nhật trạng thái của đơn mua hàng là đang thực hiện
                    UPDATE purchase_ex_don_mua_hang PO
                    SET "TINH_TRANG" = '1'
                    FROM
                        purchase_ex_don_mua_hang_chi_tiet AS POD
                    WHERE
                        PO."id" = POD."DON_MUA_HANG_CHI_TIET_ID"
                        AND -- POD."SO_LUONG_DA_NHAN" <> 0
                        POD."SO_LUONG_NHAN" > 0
                        OR EXISTS(SELECT *
                                    FROM purchase_ex_don_mua_hang_chi_tiet AS POD2
                                    WHERE POD2."SO_LUONG_NHAN" = 0
                                        AND POD2."SO_LUONG" = 0
                                        AND (SELECT COUNT(*)
                                            FROM purchase_document_line AS PVD
                                            WHERE PVD."CHI_TIET_DON_MUA_HANG_ID" = POD2."id"
                                            ) > 0
                                        AND POD2."DON_MUA_HANG_CHI_TIET_ID" = PO.id)
                
                    AND       POD.id IN %(ARR_ID_DON_DAT_HANG_CHI_TIET)s --@arrPUOrderRefDetailID
                
                    ;
                
                    --Cập nhật trạng thái của đơn mua hàng là đã hoàn thành
                    UPDATE purchase_ex_don_mua_hang PO
                    SET "TINH_TRANG" = '2'
                    FROM
                        purchase_ex_don_mua_hang_chi_tiet AS POD
                    WHERE PO."id" = POD."DON_MUA_HANG_CHI_TIET_ID"
                        AND NOT EXISTS(SELECT *
                                        FROM purchase_ex_don_mua_hang_chi_tiet AS PD
                                        WHERE PD."SO_LUONG" > PD."SO_LUONG_NHAN"
                                            AND PD."DON_MUA_HANG_CHI_TIET_ID" = PO."id")
                        AND NOT EXISTS(SELECT *
                                        FROM purchase_ex_don_mua_hang_chi_tiet AS POD2
                                        WHERE POD2."SO_LUONG_NHAN" = 0
                                            AND POD2."SO_LUONG" = 0
                                            AND (SELECT COUNT(*)
                                                    FROM purchase_document_line AS PVD
                                                    WHERE PVD."CHI_TIET_DON_MUA_HANG_ID" = POD2."id"
                                                ) = 0
                                            AND POD2."DON_MUA_HANG_CHI_TIET_ID" = PO.id)
                        AND POD.id IN %(ARR_ID_DON_DAT_HANG_CHI_TIET)s --@arrPUOrderRefDetailID
                
                    ;
                
                
                END $$
                ;
        
                
        """  
        cr = self.env.cr
        return cr.execute(query, params)