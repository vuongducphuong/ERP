# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json

from datetime import datetime
from odoo import api, fields, models, _, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round
import ast

class PURCHASE_DOCUMENT(models.Model):
    _name = "purchase.document"
    _inherit = ['mail.thread']
    _description = "Chứng từ mua hàng"
    _order = "NGAY_HACH_TOAN desc,NGAY_CHUNG_TU desc,SO_CHUNG_TU desc"
  
    name = fields.Char('Chứng từ mua hàng', related='SO_CHUNG_TU')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_KHO_ID = fields.Many2one('so.kho', ondelete='set null')
    SO_MUA_HANG_ID = fields.Many2one('so.mua.hang', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    type = fields.Selection([
        ('hang_hoa', 'Chứng từ mua hàng hóa'),
        ('dich_vu', 'Chứng từ mua dịch vụ')
        ], string='Status', default='hang_hoa')
    NGAY_DAT_HANG = fields.Datetime('Order Date', required=True, index=True, copy=False, default=fields.Datetime.now,\
        help="Depicts the date where the Quotation should be validated and converted into a purchase order.")
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', domain=[('LA_NHA_CUNG_CAP','=',True)], track_visibility='onchange')
    TEN_DOI_TUONG = fields.Char('Tên NCC')
    DIA_CHI_NHAN_HANG = fields.Many2one('res.partner', string='Drop Ship Address', \
        help="Put an address if you want to deliver directly from the vendor to the customer. "\
             "Otherwise, keep empty to deliver to your own company.")

    CHI_TIET_IDS = fields.One2many('purchase.document.line', 'order_id', string='Order Lines', copy=True)
    PHI_TRUOC_HAI_QUAN_IDS = fields.One2many('purchase.phi.truoc.hai.quan', 'purchase_document_id', string='Phí trước hải quan', copy=True)
    PHI_HANG_VE_KHO_IDS = fields.One2many('purchase.phi.hang.ve.kho', 'purchase_document_id', string='Phí hàng về kho', copy=True)
    CHI_PHI_MUA_HANG_IDS = fields.One2many('purchase.chi.phi.mua.hang', 'purchase_document_id', string='Chi phí mua hàng', copy=True)
    CHI_PHI_IDS = fields.One2many('purchase.chi.phi', 'purchase_document_id', string='Chi phí', copy=True)
    GHI_CHU = fields.Text('Terms and Conditions')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', store=True, readonly=True, compute='_amount_all', currency_field='currency_id')
    TONG_TIEN_DICH_VU = fields.Monetary(string='Tổng tiền dịch vụ', store=True, readonly=True, compute='_amount_all', currency_field='currency_id')
    TONG_TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', store=True, readonly=True, compute='_amount_all', currency_field='currency_id')
    TONG_GIA_TRI = fields.Monetary(string='Tổng giá trị', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    TONG_TIEN_THUE_NK = fields.Monetary(string='Thuế NK', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    THUE_TTDB = fields.Monetary(string='Thuế TTĐB', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    PHI_TRUOC_HAI_QUAN = fields.Monetary(string='Phí trước hải quan', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    # PHI_HANG_VE_KHO = fields.Monetary(string='Phí hàng về kho', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    CHI_PHI_MUA_HANG = fields.Monetary(string='Chi phí mua hàng', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    SO_TIEN_THUE = fields.Monetary(string='Thuế', store=True, readonly=True, compute='_amount_all', currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền TT', help='Tổng tiền thanh toán',store=True, readonly=True, compute='_amount_all', currency_field='currency_id', track_visibility='onchange')
    DIEU_KHOAN_THANH_TOAN_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan',string="Điều khoản TT",help= 'Điều khoản thanh toán')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ',help='Loại chứng từ',compute='set_ma_loai_chung_tu',store=True)
    TONG_TIEN_HANG_QUY_DOI = fields.Monetary(string='',help='Tổng tiền hàng quy đổi',readonly=True, currency_field='base_currency_id',compute='_amount_all',store=True)
    TONG_TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='',help='Tổng tiền thuế quy đổi',readonly=True, currency_field='base_currency_id',compute='_amount_all',store=True)
    TONG_TIEN_CK_GTGT_QUY_DOI = fields.Monetary(string='',help='Tổng tiền chiết khấu quy đổi',readonly=True, currency_field='base_currency_id',compute='_amount_all',store=True)
    TONG_TIEN_THANH_TOAN_QUY_DOI = fields.Monetary(string='',help='Tổng tiền thanh toán quy đổi',readonly=True, currency_field='base_currency_id',compute='_amount_all',store=True)
    TONG_TIEN_DICH_VU_QUY_DOI = fields.Monetary(string='',help='Tổng tiền dịch vụ quy đổi',readonly=True, currency_field='base_currency_id',compute='_amount_all',store=True)

    # Thông tin chung
    NGUOI_GIAO_HANG = fields.Char('Người giao hàng',)
    DIEN_GIAI_CHUNG = fields.Char('Diễn giải')
    DIEN_GIAI = fields.Char('Diễn giải',related='DIEN_GIAI_CHUNG')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng', domain=[('LA_NHAN_VIEN','=',True)])
    KEM_THEO = fields.Char(string='Kèm theo CTG', help='Kèm theo chứng từ gốc')

    KEM_THEO_PC = fields.Char(string='Kèm theo CTG', help='Kèm theo chứng từ gốc')
    THAM_CHIEU = fields.Char('Tham chiếu')
    NGUOI_NHAN = fields.Char('Người nhận')
    DIA_CHI = fields.Char(string='Địa chỉ')
    LY_DO_CHI = fields.Char('Lý do chi')
    MA_SO_THUE = fields.Char('Mã số thuế', related='DOI_TUONG_ID.MA_SO_THUE',store=True)
    SO_CMND = fields.Char('Số CMND')
    SO_CMND_KHAC = fields.Char(string='Số CMND')
    NGAY_CAP_CMND = fields.Date(string='Ngày cấp')
    NOI_CAP_CMND = fields.Char('Nơi cấp')
    SO_NGAY_DUOC_NO = fields.Integer(string='Số ngày nợ', help='Số ngày được nợ')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán')
    TK_CHI_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Tài khoản chi')
    CHI_NHANH_TK_CHI = fields.Char('Ngân hàng')
    TK_NHAN_ID = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='Tài khoản nhận')
    CHI_NHANH_TK_NHAN = fields.Char('Ngân hàng')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    # Bổ sung trường để lấy tài khoản tiền
    TAI_KHOAN_TIEN  = fields.Many2one('danh.muc.he.thong.tai.khoan',string='Tài khoản tiền', help='Tài khoản tiền')
    # Bổ sung Discount
    def _get_default_discount(self):
        if self.DOI_TUONG_ID:
            return self.DOI_TUONG_ID.purchase_discount
    LOAI_CHIET_KHAU = fields.Selection([('percent', 'Toàn bộ đơn theo phần trăm'), ('amount', 'Toàn bộ đơn bằng tiền mặt'), ('none', 'Từng dòng sản phẩm theo phần trăm')], string='Loại chiết khấu',
                                     readonly=True, default='percent')
    TY_LE_CHIET_KHAU = fields.Float(string='Chiết khấu', digits=dp.get_precision('Account'),
                                 readonly=True, default=_get_default_discount)
    SO_TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', store=True, readonly=True, compute='_amount_all', currency_field='currency_id')
    # Chứng từ
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', default=fields.Datetime.now)
    NGAY_CHUNG_TU_PHIEU_NHAP = fields.Date(string='Ngày chứng từ', default=fields.Datetime.now)
    NGAY_CHUNG_TU_PHIEU_CHI = fields.Date(string='Ngày chứng từ', default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', compute='_compute_SO_CHUNG_TU', store=True, )
    SO_CHUNG_TU_MUA_HANG = fields.Char(string='Số chứng từ', auto_num='purchase_SO_CHUNG_TU_MUA_HANG')
    SO_CHUNG_TU_MUA_DICH_VU = fields.Char(string='Số chứng từ', auto_num='purchase_SO_CHUNG_TU_MUA_DICH_VU')
    SO_PHIEU_NHAP = fields.Char(string='Số phiếu nhập', auto_num='stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_NHAP_KHO')
    SO_PHIEU_CHI = fields.Char(string='Số chứng từ', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_PHIEU_CHI')
    SO_UY_NHIEM_CHI = fields.Char(string='Số chứng từ', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_UY_NHIEM_CHI')
    SO_SEC_CHUYEN_KHOAN = fields.Char(string='Số chứng từ', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_SEC_CHUYEN_KHOAN')
    SO_SEC_TIEN_MAT = fields.Char(string='Số chứng từ', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_SEC_TIEN_MAT')

    # Hóa đơn
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd' ,string='Mẫu số HĐ')
    KY_HIEU_HD = fields.Char(string='Kí hiệu HĐ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', default=fields.Date.context_today)
    
    # Tham chiếu
    DON_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn hàng')
    # Updated 2019-04-16 by anhtuan: Chứng từ bán hàng không tạo phiếu nhập/phiếu chi
    # Chỉ tạo hóa đơn. Có thể truy xuất hóa đơn này bằng cách seach với điều kiện ID_CHUNG_TU_GOC/SOURCE_ID = purchase_doc.id

    # CHI_PHI_MUA_HANG = fields.Float(string='CP mua hàng', help='Chi phí mua hàng')
    GIA_TRI_NHAP_KHO = fields.Monetary(string='Giá trị nhập kho',compute='_amount_all', currency_field='base_currency_id', store=True, )
    DA_NHAN_HOA_DON = fields.Boolean(string='Đã nhận hóa đơn')
    NHAN_HOA_DON = fields.Char(string='Nhận hóa đơn',compute='thay_doi_nhan_hoa_don',store=True)
    LA_CHI_PHI_MUA_HANG = fields.Boolean(string='Là chi phí mua hàng',help='Là chi phí mua hàng')
    so_chung_tu_qt = fields.Char('Số chứng từ (Sổ QT)')

    IS_TH1 = fields.Boolean(default='True',compute='thay_doi_hoa_don',store=True)
    IS_TH2 = fields.Boolean(default='False',compute='thay_doi_hoa_don',store=True)
    IS_TH3 = fields.Boolean(default='False',compute='thay_doi_hoa_don',store=True)
    IS_TH4 = fields.Boolean(default='False',compute='thay_doi_hoa_don',store=True)
    NOI_DUNG_THANH_TOAN = fields.Char( string='Nội dung TT', help='Nội dung TT',related='DIEN_GIAI_CHUNG')
    CHON_CHI_PHI_JSON = fields.Text(store=False)
    PHAN_BO_CHIET_KHAU_JSON = fields.Text(store=False)
    PHAN_BO_CHIET_KHAU_JSON_MDV = fields.Text(store=False)
    HOA_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Hóa đơn mua hàng hóa', help='Hóa đơn mua hàng hóa', ondelete='set null')
    SO_CHUNG_TU_TU_TANG_JSON = fields.Char(store=False)
    PHAN_BO_CHI_PHI_MUA_HANG_IDS = fields.One2many('purchase.ex.phan.bo.chi.phi.mua.hang', 'CHUNG_TU_MUA_HANG_ID', string='Phân bổ chi phí mua hàng', copy=True)
    PHUONG_THUC_PHAN_BO = fields.Selection([('TY_LE_PT_THEO_SO_LUONG', 'Tỷ lệ % theo số lượng'), ('TY_LE_PT_THEO_GIA_TRI', 'Tỷ lệ % theo giá trị'), ('TU_NHAP_PT', 'Tự nhập %'), ('TU_NHAP_GIA_TRI', 'Tự nhập giá trị')], string='Phương thức phân bổ',default='TY_LE_PT_THEO_SO_LUONG')
    TONG_CHI_PHI_MUA_HANG = fields.Float(string='Tổng chi phí mua hàng', help='Tổng chi phí mua hàng')
    HOA_DON_REF_ID = fields.Char(help='Ref ID của hóa đơn được import')

    LA_PHIEU_MUA_HANG = fields.Boolean(string='Là phiếu mua hàng',help='Là phiếu mua hàng')
    #Trường dành cho mẫu in
    HO_VA_TEN_NGUOI_GIAO = fields.Char(string='Họ và tên người giao', help='Họ và tên người giao',store=False)
    LAP_TU_DON_MUA_HANG_JSON = fields.Char(store=False)
    import_options = fields.Text(string='Lưu import option', store=False)
    # _sql_constraints = [
    #     ('SO_CHUNG_TU_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
    # ]
    CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH = fields.Boolean()

    @api.onchange('import_options')
    def update_hang_tien(self):
        if self.import_options:
            _fields = self.CHI_TIET_IDS._fields
            import_options = json.loads(self.import_options)
            base_import = self.env['base_import.import'].browse(import_options.get('import_id'))
            if base_import:
                import_fields, data = base_import.get_import_data(import_options.get('fields'), import_options.get('import_options'))
                default = self.CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
                for d in data:
                    line = default.copy()
                    for idx, val in enumerate(import_fields):
                        _f  = _fields.get(val)
                        if d[idx]:
                            if val == 'THUE_GTGT_ID' and '%' not in d[idx]:
                                d[idx] = (d[idx] or '') + '%'
                            line[val] = self.get_value_for_db(_f, d[idx], True)
                    # Bổ sung tài khoản nợ, lấy mặc định từ vật tư hàng hóa và kho
                    new_line = self.env['purchase.document.line'].new(line)
                    update = {}
                    # Cập nhật tên hàng
                    if new_line.name:
                        update['TEN'] = new_line.name
                    else:
                        new_line.name = new_line.MA_HANG_ID.TEN
                    # Cập nhật tàu khoản kho/nợ
                    if new_line.TK_NO_ID:
                        update['TAI_KHOAN_KHO_ID'] = new_line.TK_NO_ID.id
                    else:
                        new_line.TK_NO_ID = new_line.MA_HANG_ID.TAI_KHOAN_KHO_ID.id or new_line.KHO_ID.TK_KHO_ID.id
                    # Cập nhật kho ngầm định
                    if new_line.KHO_ID:
                        update['KHO_NGAM_DINH_ID'] = new_line.KHO_ID.id
                    else:
                        new_line.KHO_ID = new_line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
                    # Cập nhật đơn vị tính
                    if new_line.DVT_ID:
                        update['DVT_CHINH_ID'] = new_line.DVT_ID.id
                    else:
                        new_line.DVT_ID = new_line.MA_HANG_ID.DVT_CHINH_ID.id
                    # Cập nhật thuế xuất
                    if not new_line.THUE_GTGT_ID:
                        new_line.THUE_GTGT_ID = new_line.MA_HANG_ID.THUE_SUAT_GTGT_ID.id
                    # Cập nhật thành tiền:
                    if not new_line.THANH_TIEN:
                        new_line.THANH_TIEN = new_line.SO_LUONG * new_line.DON_GIA
                    # Cập nhật tiền chiết khấu
                    if not new_line.TIEN_CHIET_KHAU:
                        new_line.TIEN_CHIET_KHAU = new_line.THANH_TIEN * new_line.TY_LE_CK / 100
                    # Cập nhật tiền thuế
                    if new_line.THUE_GTGT_ID:
                        new_line.TIEN_THUE_GTGT = new_line.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT * (new_line.THANH_TIEN - new_line.TIEN_CHIET_KHAU) / 100
                    # Cập nhật thông tin vật tư hàng hóa khi tạo mới
                    if new_line.MA_HANG_ID and new_line.MA_HANG_ID.MA == new_line.MA_HANG_ID.TEN:
                        new_line.MA_HANG_ID.write(update)
                    self.CHI_TIET_IDS += new_line

    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.CHI_TIET_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))

    @api.onchange('LAP_TU_DON_MUA_HANG_JSON')
    def update_lap_tu_don_mua_hang(self):
        if self.LAP_TU_DON_MUA_HANG_JSON:
            id_so_luong_ids = self.LAP_TU_DON_MUA_HANG_JSON.split(';')
            for ct in id_so_luong_ids:
                if ct != '':
                    chi_tiet  = ct.split(',')
                    id_don_mua_hang_chi_tiet = int(chi_tiet[0])
                    so_luong_nhan = float(chi_tiet[1])
                    don_mua_hang_chi_tiet = self.env['purchase.ex.don.mua.hang.chi.tiet'].browse(id_don_mua_hang_chi_tiet)
                    if don_mua_hang_chi_tiet:
                        mas_ter = don_mua_hang_chi_tiet.DON_MUA_HANG_CHI_TIET_ID
                        self.DOI_TUONG_ID = mas_ter.NHA_CUNG_CAP_ID.id
                        self.currency_id = mas_ter.currency_id.id
                        env = self.env['purchase.document.line']
                        tai_khoan_ngam_dinh = env.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU,0, self.currency_id.name!='VND')
                        if self.LOAI_CHUNG_TU_MH in ('trong_nuoc_nhap_kho','nhap_khau_nhap_kho'):        
                            tk_no = don_mua_hang_chi_tiet.MA_HANG_ID.lay_tai_khoan_kho()
                        else:
                            tk_no = tai_khoan_ngam_dinh.get('TK_NO_ID')
                        new_line = env.new({
                            'MA_HANG_ID': don_mua_hang_chi_tiet.MA_HANG_ID.id,
                            'name': don_mua_hang_chi_tiet.TEN_HANG,
                            'DVT_ID' : don_mua_hang_chi_tiet.DVT_ID.id,
                            env.get_field_so_luong(): so_luong_nhan,
                            'DON_GIA': don_mua_hang_chi_tiet.DON_GIA,
                            'THANH_TIEN': don_mua_hang_chi_tiet.THANH_TIEN,
                            'GIA_TRI_NHAP_KHO': don_mua_hang_chi_tiet.THANH_TIEN,
                            'DON_MUA_HANG_ID': don_mua_hang_chi_tiet.DON_MUA_HANG_CHI_TIET_ID.id,
                            'KHO_ID': don_mua_hang_chi_tiet.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                            'TK_THUE_GTGT_ID': tai_khoan_ngam_dinh.get('TK_THUE_GTGT'),
                            'TK_CO_ID': tai_khoan_ngam_dinh.get('TK_CO_ID'),
                            'TK_NO_ID': tk_no,
                            'CHI_TIET_DON_MUA_HANG_ID': id_don_mua_hang_chi_tiet,
                            'TY_GIA' : mas_ter.TY_GIA,
                        })
                        new_line.tinh_tien_quy_doi()
                        self.CHI_TIET_IDS += new_line
                

                
    @api.depends('type','LOAI_CHUNG_TU_MH','DA_THANH_TOAN','LOAI_THANH_TOAN',
    'SO_PHIEU_NHAP','SO_PHIEU_CHI','SO_UY_NHIEM_CHI','SO_SEC_CHUYEN_KHOAN','SO_SEC_TIEN_MAT','SO_CHUNG_TU_MUA_HANG')
    def _compute_SO_CHUNG_TU(self):
        for record in self:
            if 'hang_hoa' == record.type and record.LOAI_CHUNG_TU_MH in ('trong_nuoc_nhap_kho','nhap_khau_nhap_kho'):
                record.SO_CHUNG_TU = record.SO_PHIEU_NHAP
            else:
                if record.DA_THANH_TOAN:
                    if record.LOAI_THANH_TOAN == 'uy_nhiem_chi':
                        record.SO_CHUNG_TU = record.SO_UY_NHIEM_CHI
                    elif record.LOAI_THANH_TOAN == 'sec_chuyen_khoan':
                        record.SO_CHUNG_TU = record.SO_SEC_CHUYEN_KHOAN
                    elif record.LOAI_THANH_TOAN == 'sec_tien_mat':
                        record.SO_CHUNG_TU = record.SO_SEC_TIEN_MAT
                    else:
                        record.SO_CHUNG_TU = record.SO_PHIEU_CHI
                else:
                    record.SO_CHUNG_TU = record.SO_CHUNG_TU_MUA_HANG


    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        for line in self.CHI_TIET_IDS:
            line.tinh_tien_quy_doi()
            line.tinh_tien_thue_nk()
            line.lay_gia_tri_nhap_kho()
            line.lay_gia_tri_tinh_thue_nk()
            line.ham_tinh_thue_gtgt()
            line.tinh_don_gia_quy_doi()

    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            if record.DA_THANH_TOAN:
                if record.LOAI_THANH_TOAN == 'uy_nhiem_chi':
                    record.validate_unique_thu_chi_tien(record.SO_UY_NHIEM_CHI)
                elif record.LOAI_THANH_TOAN == 'sec_chuyen_khoan':
                    record.validate_unique_thu_chi_tien(record.SO_SEC_CHUYEN_KHOAN)
                elif record.LOAI_THANH_TOAN == 'sec_tien_mat':
                    record.validate_unique_thu_chi_tien(record.SO_SEC_TIEN_MAT)
                elif record.LOAI_THANH_TOAN == 'tien_mat':
                    record.validate_unique_thu_chi_tien(record.SO_PHIEU_CHI)
    
    @api.multi
    def validate_nhap_xuat_kho(self):
        for record in self:
            if record.LOAI_CHUNG_TU_MH in ('trong_nuoc_nhap_kho','nhap_khau_nhap_kho'):
                record.validate_unique_nhap_xuat_kho(record.SO_PHIEU_NHAP)

    @api.model
    def create(self, vals):
        result = super(PURCHASE_DOCUMENT, self).create(vals)
        result.validate_unique_so_chung_tu({self._name.replace('.','_'): 'SO_CHUNG_TU'}, 'SO_CHUNG_TU')
        result.validate_thu_chi_tien()
        result.validate_nhap_xuat_kho()
        if not self._context.get('fromMS'):
            self.create_references(result)
        if self.CHI_TIET_IDS:
            self.up_date_don_mua_hang()
        return result

    @api.multi
    def write(self, values):
        result = super(PURCHASE_DOCUMENT, self).write(values)
        if helper.List.element_in_dict(['DA_THANH_TOAN','LOAI_THANH_TOAN','SO_UY_NHIEM_CHI','SO_SEC_CHUYEN_KHOAN','SO_SEC_TIEN_MAT','SO_PHIEU_CHI'], values):
            self.validate_thu_chi_tien()
        if helper.List.element_in_dict(['LOAI_CHUNG_TU_MH','SO_PHIEU_NHAP'], values):
            self.validate_nhap_xuat_kho()
        if helper.List.element_in_dict(['type','LOAI_CHUNG_TU_MH','DA_THANH_TOAN','LOAI_THANH_TOAN','SO_PHIEU_NHAP','SO_PHIEU_CHI','SO_UY_NHIEM_CHI','SO_SEC_CHUYEN_KHOAN','SO_SEC_TIEN_MAT','SO_CHUNG_TU_MUA_HANG'], values):
            self.validate_unique_so_chung_tu({self._name.replace('.','_'): 'SO_CHUNG_TU'}, 'SO_CHUNG_TU')
        self.update_references(values)
        if self.CHI_TIET_IDS:
            self.up_date_don_mua_hang()
        return result

    def up_date_don_mua_hang(self):
        arr_don_mua_hang = []
        for chi_tiet in self.CHI_TIET_IDS:
                if chi_tiet.CHI_TIET_DON_MUA_HANG_ID:
                    if chi_tiet.CHI_TIET_DON_MUA_HANG_ID.id not in arr_don_mua_hang:
                        arr_don_mua_hang.append(chi_tiet.CHI_TIET_DON_MUA_HANG_ID.id)
                        chi_tiet.CHI_TIET_DON_MUA_HANG_ID.DON_MUA_HANG_CHI_TIET_ID.write({'NGAY_GIAO_HANG' : self.NGAY_HACH_TOAN})
        if arr_don_mua_hang:
            tupple_don_mua_hang = tuple(arr_don_mua_hang)
            self.cap_nhat_don_mua_hang(tupple_don_mua_hang)

    def create_references(self, purchase_doc):
        # Lập kèm hóa đơn, chỉ với chứng từ mua hàng hóa
        if purchase_doc.LOAI_HOA_DON == "1" and purchase_doc.type == 'hang_hoa': # Có hóa đơn
            vals = {
                'SO_HOA_DON': purchase_doc.SO_HOA_DON,
                'NGAY_HOA_DON': purchase_doc.NGAY_HOA_DON,
                'KY_HIEU_HD': purchase_doc.KY_HIEU_HD,
                'MAU_SO_HD_ID': purchase_doc.MAU_SO_HD_ID.id,
                'DOI_TUONG_ID': purchase_doc.DOI_TUONG_ID.id,
                'TEN_NHA_CUNG_CAP': purchase_doc.TEN_DOI_TUONG,
                'LOAI_CHUNG_TU': 3400,
                'NHAN_HOA_DON' : True,
                'SOURCE_ID': self._name + ',' + str(purchase_doc.id),
            }
            hoa_don = purchase_doc.upsert_reference('purchase.ex.hoa.don.mua.hang', vals)
            if purchase_doc.HOA_DON_MUA_HANG_ID.id != hoa_don.id:
                super(PURCHASE_DOCUMENT, purchase_doc).write({
                    'HOA_DON_MUA_HANG_ID': hoa_don.id,
                })
            purchase_doc.CHI_TIET_IDS.write({'HOA_DON_ID': hoa_don.id})

    def update_references(self, values):
        for record in self:
            # Tạo hóa đơn gắn kèm khi tích chọn lập kèm hóa đơn
            if record.LOAI_HOA_DON == "1" and record.type == 'hang_hoa':
                vals = helper.Obj.get_sub_dict(values, ('SO_HOA_DON','NGAY_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID','DOI_TUONG_ID','currency_id','TY_GIA','TONG_TIEN_THANH_TOAN','SOURCE_ID'))
                vals['LOAI_CHUNG_TU'] = 3400
                if 'TEN_DOI_TUONG' in values:
                    vals['TEN_NHA_CUNG_CAP'] = values.get('TEN_DOI_TUONG')
                hoa_don = record.upsert_reference('purchase.ex.hoa.don.mua.hang', vals)
                if record.HOA_DON_MUA_HANG_ID.id != hoa_don.id:
                    super(PURCHASE_DOCUMENT, record).write({
                        'HOA_DON_MUA_HANG_ID': hoa_don.id,
                    })
                record.CHI_TIET_IDS.write({'HOA_DON_ID': hoa_don.id})
            
            # Xóa hóa đơn gắn kèm khi không lập kèm hóa đơn
            else:
                hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
                if hoa_don:
                    if hoa_don.state ==  'da_ghi_so':
                        hoa_don.action_bo_ghi_so()
                    hoa_don.unlink()

    @api.multi
    def unlink(self):
        for record in self:
            arr_don_mua_hang = []
            record.find_reference('purchase.ex.hoa.don.mua.hang').unlink()
            if record.CHI_TIET_IDS:
                for chi_tiet in record.CHI_TIET_IDS:
                    if chi_tiet.CHI_TIET_DON_MUA_HANG_ID:
                        arr_don_mua_hang.append(chi_tiet.CHI_TIET_DON_MUA_HANG_ID.id)
        result = super(PURCHASE_DOCUMENT, self).unlink()
        if arr_don_mua_hang:
            tupple_don_mua_hang = tuple(arr_don_mua_hang)
            self.cap_nhat_don_mua_hang(tupple_don_mua_hang)
            for chi_tiet in arr_don_mua_hang:
                cap_nhat = self.env['purchase.ex.don.mua.hang.chi.tiet'].search([('id', '=',chi_tiet)],limit=1).DON_MUA_HANG_CHI_TIET_ID
                cap_nhat.write({'NGAY_GIAO_HANG' : False})
        return result


    @api.onchange('CHON_CHI_PHI_JSON')
    def _onchange_CHON_CHI_PHI_JSON(self):
        if self.CHON_CHI_PHI_JSON:
            chon_chi_phi = json.loads(self.CHON_CHI_PHI_JSON).get('PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS', [])
            self.CHI_PHI_MUA_HANG_IDS = []
            for chi_phi in chon_chi_phi:
                self.CHI_PHI_MUA_HANG_IDS += self.env['purchase.chi.phi.mua.hang'].new(chi_phi)

    @api.onchange('PHAN_BO_CHIET_KHAU_JSON')
    def _onchange_PHAN_BO_CHIET_KHAU_JSON(self):
        if self.PHAN_BO_CHIET_KHAU_JSON:
            phuong_phap_phan_bo = ast.literal_eval(self.PHAN_BO_CHIET_KHAU_JSON).get('PHUONG_PHAP_PHAN_BO')
            so_tien_phan_bo = ast.literal_eval(self.PHAN_BO_CHIET_KHAU_JSON).get('SO_TIEN')
            if phuong_phap_phan_bo=='THEO_SO_LUONG':
                # Tính tổng số lượng
                tong_so_luong = 0
                for record in self.CHI_TIET_IDS:
                    tong_so_luong += record.SO_LUONG 
                if tong_so_luong==0:
                    raise ValidationError('Tổng số lượng sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                # Xác định dòng cuối cùng: dòng cuối cùng = record [len(self.CHI_TIET_IDS)-1]
                # khai báo index i = 0
                i = 0
                tong_so_tien_chiet_khau_o_dong_khac = 0
                for record in self.CHI_TIET_IDS:
                    # i = i+1
                    i += 1
                    if(i != len(self.CHI_TIET_IDS)):                        
                        # dong khac
                         #  số tiền chiết khấu từng dòng = (số tiền phân bổ / tổng số lượng) * số lượng từng dòng
                        tien_chiet_khau = (so_tien_phan_bo / tong_so_luong) * record. SO_LUONG
                        record.TIEN_CHIET_KHAU = tien_chiet_khau
                        record.TIEN_CHIET_KHAU_QUY_DOI = float_round(record.TIEN_CHIET_KHAU * self.TY_GIA, 0)
                        tong_so_tien_chiet_khau_o_dong_khac += tien_chiet_khau
                        if record.THANH_TIEN==0:
                            raise ValidationError('Thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                        record.TY_LE_CK = (tien_chiet_khau / record.THANH_TIEN)*100
                
                # số tiền chiết khấu của dòng cuối cùng = số tiền phân bổ  - tổng số tiền chiết khấu ở các dòng khác 
                if (len(self.CHI_TIET_IDS) > 0):
                    tien_chiet_khau_dong_cuoi_cung = so_tien_phan_bo - tong_so_tien_chiet_khau_o_dong_khac
                    self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TIEN_CHIET_KHAU = tien_chiet_khau_dong_cuoi_cung
                    self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TIEN_CHIET_KHAU_QUY_DOI = tien_chiet_khau_dong_cuoi_cung*self.TY_GIA
                    if record.THANH_TIEN==0:
                        raise ValidationError('Thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                    self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TY_LE_CK = (tien_chiet_khau_dong_cuoi_cung / record.THANH_TIEN ) * 100
            else:
                tong_thanh_tien = 0
                for record in self.CHI_TIET_IDS:
                    tong_thanh_tien += record.THANH_TIEN 
                if tong_thanh_tien==0:
                    raise ValidationError('Tổng thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                # Xác định dòng cuối cùng: dòng cuối cùng = record [len(self.CHI_TIET_IDS)-1]
                # khai báo index i = 0
                i = 0
                tong_so_tien_chiet_khau_o_dong_khac = 0
                for record in self.CHI_TIET_IDS:
                    # i = i+1
                    i += 1
                    if(i != len(self.CHI_TIET_IDS)):                        
                        # dong khac
                         #  số tiền chiết khấu từng dòng = (số tiền phân bổ / tổng số lượng) * số lượng từng dòng
                        tien_chiet_khau = (so_tien_phan_bo / tong_thanh_tien) * record. THANH_TIEN
                        record.TIEN_CHIET_KHAU = tien_chiet_khau
                        record.TIEN_CHIET_KHAU_QUY_DOI = float_round(record.TIEN_CHIET_KHAU * self.TY_GIA, 0)
                        tong_so_tien_chiet_khau_o_dong_khac += tien_chiet_khau
                        if record.THANH_TIEN==0:
                            raise ValidationError('Thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                        record.TY_LE_CK = (tien_chiet_khau / record.THANH_TIEN)*100
                
                # số tiền chiết khấu của dòng cuối cùng = số tiền phân bổ  - tổng số tiền chiết khấu ở các dòng khác 
                if (len(self.CHI_TIET_IDS) > 0):
                    tien_chiet_khau_dong_cuoi_cung = so_tien_phan_bo - tong_so_tien_chiet_khau_o_dong_khac
                    self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TIEN_CHIET_KHAU = tien_chiet_khau_dong_cuoi_cung
                    self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TIEN_CHIET_KHAU_QUY_DOI = tien_chiet_khau_dong_cuoi_cung*self.TY_GIA
                    if record.THANH_TIEN==0:
                        raise ValidationError('Thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                    self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TY_LE_CK = (tien_chiet_khau_dong_cuoi_cung / record.THANH_TIEN ) * 100
            self._amount_all() 

    @api.onchange('PHAN_BO_CHIET_KHAU_JSON_MDV')
    def _onchange_PHAN_BO_CHIET_KHAU_JSON_MDV(self):
        if self.PHAN_BO_CHIET_KHAU_JSON_MDV:
            phuong_phap_phan_bo = json.loads(self.PHAN_BO_CHIET_KHAU_JSON_MDV).get('PHUONG_PHAP_PHAN_BO')
            so_tien_phan_bo = json.loads(self.PHAN_BO_CHIET_KHAU_JSON_MDV).get('SO_TIEN')
            if phuong_phap_phan_bo=='THEO_SO_LUONG':
                # Tính tổng số lượng
                tong_so_luong = 0
                for record in self.CHI_TIET_IDS:
                    tong_so_luong += record.SO_LUONG 
                if tong_so_luong==0:
                    raise ValidationError('Tổng số lượng sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                for record in self.CHI_TIET_IDS:
                    tien_thue_gtgt_sau_khi_phan_bo = 0
                    if record.THUE_GTGT_ID:
                        tien_thue_gtgt_truoc_phan_bo = (record.THANH_TIEN * record.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT) / 100
                        tien_thue_phan_bo = (so_tien_phan_bo * record.SO_LUONG * record.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT) / (tong_so_luong * 100)
                        tien_thue_gtgt_sau_khi_phan_bo = tien_thue_gtgt_truoc_phan_bo - tien_thue_phan_bo
                    record.TIEN_THUE_GTGT = tien_thue_gtgt_sau_khi_phan_bo
            else:
                # Tính tổng thành tiền
                tong_thanh_tien = 0
                for record in self.CHI_TIET_IDS:
                    tong_thanh_tien += record.THANH_TIEN 
                if tong_thanh_tien==0:
                    raise ValidationError('Tổng thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                for record in self.CHI_TIET_IDS:
                    tien_thue_gtgt_sau_khi_phan_bo = 0
                    if record.THUE_GTGT_ID:
                        tien_thue_gtgt_truoc_phan_bo = (record.THANH_TIEN * record.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT) / 100
                        tien_thue_phan_bo = (so_tien_phan_bo * record.THANH_TIEN * record.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT) / (tong_thanh_tien * 100)
                        tien_thue_gtgt_sau_khi_phan_bo = tien_thue_gtgt_truoc_phan_bo - tien_thue_phan_bo
                    record.TIEN_THUE_GTGT = tien_thue_gtgt_sau_khi_phan_bo
            self.SO_TIEN_CHIET_KHAU = so_tien_phan_bo
            self._amount_all() 



    @api.depends('CHI_TIET_IDS','LOAI_CHUNG_TU_MH','LOAI_HOA_DON')
    def _amount_all(self):
        for order in self:
            tong_tien_hang =  so_tien_chiet_khau = tien_thue_gtgt = tong_gia_tri = thue_nhap_khau = phi_ttdb = phi_truoc_hq = phi_hang_ve_kho = chi_phi_mua_hang = gt_nhap_kho=0.0
            tong_tien_hang_quy_doi = tong_tien_chiet_khau_quy_doi = tong_tien_thue_gtgt_quy_doi = tong_tien_thanh_toan_quy_doi = 0.0
            tong_tien_thanh_toan = 0.0
            

            for line in order.CHI_TIET_IDS:
                tong_tien_hang += line.THANH_TIEN
                # SO_TIEN_THUE += line.TIEN_THUE
                so_tien_chiet_khau += line.TIEN_CHIET_KHAU 
                tien_thue_gtgt += line.TIEN_THUE_GTGT

                tong_gia_tri += line.GIA_TRI_NHAP_KHO

                thue_nhap_khau += line.TIEN_THUE_NK
                phi_ttdb += line.TIEN_THUE_TTDB
                phi_truoc_hq += line.PHI_TRUOC_HAI_QUAN
                # phi_hang_ve_kho += line.PHI_HANG_VE_KHO
                chi_phi_mua_hang += line.CHI_PHI_MUA_HANG
                if order.LOAI_CHUNG_TU_MH not in ('trong_nuoc_khong_qua_kho','nhap_khau_khong_qua_kho'):
                    gt_nhap_kho += line.GIA_TRI_NHAP_KHO


                tong_tien_hang_quy_doi += line.THANH_TIEN_QUY_DOI
                tong_tien_chiet_khau_quy_doi += line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_thue_gtgt_quy_doi += line.TIEN_THUE_GTGT_QUY_DOI 
               
                if order.LOAI_CHUNG_TU_MH == 'nhap_khau_nhap_kho' or order.LOAI_CHUNG_TU_MH == 'nhap_khau_khong_qua_kho':              
                    tong_tien_thanh_toan = tong_tien_hang - so_tien_chiet_khau
                    tong_tien_thanh_toan_quy_doi = tong_tien_hang_quy_doi  - tong_tien_chiet_khau_quy_doi
                else:
                    tong_tien_thanh_toan = tong_tien_hang + tien_thue_gtgt - so_tien_chiet_khau
                    tong_tien_thanh_toan_quy_doi = tong_tien_hang_quy_doi + tong_tien_thue_gtgt_quy_doi - tong_tien_chiet_khau_quy_doi
            order.update({
                'TONG_TIEN_HANG': tong_tien_hang,
                # 'SO_TIEN_THUE': SO_TIEN_THUE,
                'SO_TIEN_CHIET_KHAU': so_tien_chiet_khau,
                'TONG_TIEN_THUE_GTGT' : tien_thue_gtgt,
                'TONG_GIA_TRI' : tong_gia_tri,
                'TONG_TIEN_THUE_NK' : thue_nhap_khau,
                'THUE_TTDB' : phi_ttdb,
                'PHI_TRUOC_HAI_QUAN' : phi_truoc_hq,
                # 'PHI_HANG_VE_KHO' : phi_hang_ve_kho,
                'CHI_PHI_MUA_HANG' : chi_phi_mua_hang,
                'GIA_TRI_NHAP_KHO' : gt_nhap_kho,
                'TONG_TIEN_THANH_TOAN': tong_tien_thanh_toan,

                'TONG_TIEN_HANG_QUY_DOI': tong_tien_hang_quy_doi,
                'TONG_TIEN_CK_GTGT_QUY_DOI': tong_tien_chiet_khau_quy_doi,
                'TONG_TIEN_THUE_GTGT_QUY_DOI': tong_tien_thue_gtgt_quy_doi,
                'TONG_TIEN_THANH_TOAN_QUY_DOI': tong_tien_thanh_toan_quy_doi ,
            })

    # @api.depends('CHI_TIET_IDS')
    # def _amount_all(self):
    #     for order in self:
    #         tong_tien_hang_quy_doi = tong_tien_chiet_khau_quy_doi = tong_tien_thue_gtgt_quy_doi = tong_tien_thanh_toan_quy_doi = tong_cp_mua_hang =tong_gia_tri_nhap_kho = 0.0
        
    #         for line in order.CHI_TIET_IDS:
    #             tong_tien_hang_quy_doi += line.THANH_TIEN_QUY_DOI
    #             tong_tien_chiet_khau_quy_doi += line.TIEN_CHIET_KHAU_QUY_DOI
    #             tong_tien_thue_gtgt_quy_doi += line.TIEN_THUE_GTGT_QUY_DOI 
    #             tong_tien_thanh_toan_quy_doi = tong_tien_hang_quy_doi + tong_tien_thue_gtgt_quy_doi - tong_tien_chiet_khau_quy_doi
    #             tong_cp_mua_hang += line.CHI_PHI_MUA_HANG
    #             tong_gia_tri_nhap_kho += line.GIA_TRI_NHAP_KHO

    #             # so_hoa_don_master = line.SO_HOA_DON_DETAIL

               
                
    #         order.update({
    #             'TONG_TIEN_HANG_QUY_DOI': tong_tien_hang_quy_doi,
    #             'TONG_TIEN_CK_GTGT_QUY_DOI': tong_tien_chiet_khau_quy_doi,
    #             'TONG_TIEN_THUE_GTGT_QUY_DOI': tong_tien_thue_gtgt_quy_doi,
    #             'TONG_TIEN_THANH_TOAN_QUY_DOI': tong_tien_thanh_toan_quy_doi ,
    #             'CHI_PHI_MUA_HANG' : tong_cp_mua_hang,
    #             'GIA_TRI_NHAP_KHO' : tong_gia_tri_nhap_kho,

    #             # 'SO_HOA_DON' : so_hoa_don_master,
                
    #         })

    # Inactive 2019-04-01 by anhtuan: Logic không rõ ràng
    # Với chứng từ mua hàng, SO_HOA_DON không phải trường compute
    # @api.depends('CHI_TIET_IDS.SO_HOA_DON_DETAIL')
    # def thay_doi_so_hoa_don(self):
    #     for order in self:
    #         so_hoa_don_master = ''
    #         for line in order.CHI_TIET_IDS:
    #             so_hoa_don_master = line.SO_HOA_DON_DETAIL
    #         order.update({
    #             'SO_HOA_DON' : so_hoa_don_master,
    #         })

    @api.onchange('DOI_TUONG_ID')
    def _update_thong_tin_partner(self):
        self.TEN_DOI_TUONG = self.DOI_TUONG_ID.HO_VA_TEN 
        self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
        self.DIEU_KHOAN_THANH_TOAN_ID = self.DOI_TUONG_ID.DIEU_KHOAN_TT_ID.id
        self.NHAN_VIEN_ID = self.DOI_TUONG_ID.NHAN_VIEN_ID.id
        if len(self.DOI_TUONG_ID.DANH_MUC_DOI_TUONG_CHI_TIET_IDS) > 0:
            self.TK_NHAN_ID = self.DOI_TUONG_ID.DANH_MUC_DOI_TUONG_CHI_TIET_IDS[0].id
        else:
            self.TK_NHAN_ID = False

    @api.onchange('DOI_TUONG_ID','SO_HOA_DON')
    def _update_dien_giai(self):
        if self.type == 'hang_hoa':
            if self.SO_HOA_DON:
                self.DIEN_GIAI = "Mua hàng của " + self.DOI_TUONG_ID.HO_VA_TEN + ' theo hóa đơn ' + str(self.SO_HOA_DON) if self.DOI_TUONG_ID.HO_VA_TEN else ""
                self.LY_DO_CHI = "Chi tiền mua hàng " + self.DOI_TUONG_ID.HO_VA_TEN + ' theo hóa đơn ' + str(self.SO_HOA_DON)  if self.DOI_TUONG_ID.HO_VA_TEN else ""
            else:
                self.DIEN_GIAI = "Mua hàng của " + self.DOI_TUONG_ID.HO_VA_TEN if self.DOI_TUONG_ID.HO_VA_TEN else ""
                self.LY_DO_CHI = "Chi tiền mua hàng " + self.DOI_TUONG_ID.HO_VA_TEN if self.DOI_TUONG_ID.HO_VA_TEN else ""
        elif self.type == 'dich_vu':
            self.DIEN_GIAI = "Mua dịch vụ của " + self.DOI_TUONG_ID.HO_VA_TEN if self.DOI_TUONG_ID.HO_VA_TEN else "Mua dịch vụ"
            self.LY_DO_CHI = "Chi tiền mua dịch vụ của " + self.DOI_TUONG_ID.HO_VA_TEN if self.DOI_TUONG_ID.HO_VA_TEN else "Chi tiền mua dịch vụ"

    @api.onchange('DIEU_KHOAN_THANH_TOAN_ID')
    def _onchange_DIEU_KHOAN_THANH_TOAN_ID(self):
        self.SO_NGAY_DUOC_NO = self.DIEU_KHOAN_THANH_TOAN_ID.SO_NGAY_DUOC_NO

    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU
            
    @api.model
    def _get_default_doc_type(self):
        return 'trong_nuoc_nhap_kho'

    LOAI_CHUNG_TU_MH = fields.Selection([
        ('trong_nuoc_nhap_kho', '1. Mua hàng trong nước nhập kho'),
        ('trong_nuoc_khong_qua_kho', '2. Mua hàng trong nước không qua kho'),
        ('nhap_khau_nhap_kho', '3. Mua hàng nhập khẩu nhập kho'),
        ('nhap_khau_khong_qua_kho', '4. Mua hàng nhập khẩu không qua kho'),
        ], string='Loại chứng từ', default=_get_default_doc_type, help='Loại chứng từ mua hàng' ,required=True,)
    DA_THANH_TOAN = fields.Boolean(string="Trả tiền ngay", default_by_last=True)
    LOAI_THANH_TOAN = fields.Selection([
        ('tien_mat', 'Tiền mặt'),
        ('uy_nhiem_chi', 'Ủy nhiệm chi'),
        ('sec_chuyen_khoan', 'Séc chuyển khoản'),
        ('sec_tien_mat', 'Séc tiền mặt'),
        ], string='Hình thức TT', default='tien_mat', help='Hình thức thanh toán',required=True)
    LOAI_HOA_DON = fields.Selection([
        ('1', 'Nhận kèm hóa đơn'),
        ('0', 'Không kèm hóa đơn'),
        ('2', 'Không có hóa đơn'),
        ], string='Hóa đơn', default_by_last=True, required=True,)
    LOAI_CHUNG_TU_TEXT = fields.Char(string='Loại chứng từ',compute='set_loai_chung_tu_text',store=True)

    @api.depends('LOAI_CHUNG_TU')
    def set_loai_chung_tu_text(self):
        for record in self:
            loai_chung_tu_text=''
            reftype= record.env['danh.muc.reftype'].search([('REFTYPE', '=',record.LOAI_CHUNG_TU)],limit=1)
            if reftype:
                loai_chung_tu_text = reftype.REFTYPENAME
            record.LOAI_CHUNG_TU_TEXT = loai_chung_tu_text

    # Bổ sung hàm depend tạo Mã loại chứng từ
    @api.depends('type','LOAI_CHUNG_TU_MH','DA_THANH_TOAN','LOAI_THANH_TOAN')
    def set_ma_loai_chung_tu(self):
        for record in self:
            if record.type=='hang_hoa':
                if record.DA_THANH_TOAN == False:
                    if record.LOAI_CHUNG_TU_MH =='trong_nuoc_nhap_kho':
                        record.LOAI_CHUNG_TU = 302
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_khong_qua_kho':
                        record.LOAI_CHUNG_TU = 312
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_nhap_kho':
                        record.LOAI_CHUNG_TU = 318
                    else:
                        record.LOAI_CHUNG_TU = 324
                elif record.DA_THANH_TOAN == True:
                    if record.LOAI_CHUNG_TU_MH =='trong_nuoc_nhap_kho' and record.LOAI_THANH_TOAN=='tien_mat':
                        record.LOAI_CHUNG_TU = 307
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_nhap_kho' and record.LOAI_THANH_TOAN=='uy_nhiem_chi':
                        record.LOAI_CHUNG_TU = 308
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_nhap_kho' and record.LOAI_THANH_TOAN=='sec_chuyen_khoan':
                        record.LOAI_CHUNG_TU = 309
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_nhap_kho' and record.LOAI_THANH_TOAN=='sec_tien_mat':
                        record.LOAI_CHUNG_TU = 310
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_khong_qua_kho' and record.LOAI_THANH_TOAN=='tien_mat':
                        record.LOAI_CHUNG_TU = 313
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_khong_qua_kho' and record.LOAI_THANH_TOAN=='uy_nhiem_chi':
                        record.LOAI_CHUNG_TU = 314
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_khong_qua_kho' and record.LOAI_THANH_TOAN=='sec_chuyen_khoan':
                        record.LOAI_CHUNG_TU = 315
                    elif record.LOAI_CHUNG_TU_MH =='trong_nuoc_khong_qua_kho' and record.LOAI_THANH_TOAN=='sec_tien_mat':
                        record.LOAI_CHUNG_TU = 316
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_nhap_kho' and record.LOAI_THANH_TOAN=='tien_mat':
                        record.LOAI_CHUNG_TU = 319
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_nhap_kho' and record.LOAI_THANH_TOAN=='uy_nhiem_chi':
                        record.LOAI_CHUNG_TU = 320
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_nhap_kho' and record.LOAI_THANH_TOAN=='sec_chuyen_khoan':
                        record.LOAI_CHUNG_TU = 321
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_nhap_kho' and record.LOAI_THANH_TOAN=='sec_tien_mat':
                        record.LOAI_CHUNG_TU = 322
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_khong_qua_kho' and record.LOAI_THANH_TOAN=='tien_mat':
                        record.LOAI_CHUNG_TU = 325
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_khong_qua_kho' and record.LOAI_THANH_TOAN=='uy_nhiem_chi':
                        record.LOAI_CHUNG_TU = 326
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_khong_qua_kho' and record.LOAI_THANH_TOAN=='sec_chuyen_khoan':
                        record.LOAI_CHUNG_TU = 327
                    elif record.LOAI_CHUNG_TU_MH =='nhap_khau_khong_qua_kho' and record.LOAI_THANH_TOAN=='sec_tien_mat':
                        record.LOAI_CHUNG_TU = 328
            elif record.type=='dich_vu':
                if record.DA_THANH_TOAN == False:
                    record.LOAI_CHUNG_TU = 330
                elif record.DA_THANH_TOAN == True:
                    if record.LOAI_THANH_TOAN=='tien_mat':
                        record.LOAI_CHUNG_TU = 331
                    elif record.LOAI_THANH_TOAN=='uy_nhiem_chi':
                        record.LOAI_CHUNG_TU = 332
                    elif record.LOAI_THANH_TOAN=='sec_chuyen_khoan':
                        record.LOAI_CHUNG_TU = 333
                    else:
                        record.LOAI_CHUNG_TU = 334

    


    @api.onchange('NGAY_CHUNG_TU')
    def onchange_ngay_hoa_don_detail(self):
        for order in self:
            for line in order.CHI_TIET_IDS:
                line.NGAY_HOA_DON = order.NGAY_CHUNG_TU 

    # Hàm để lấy thông tin chi nhánh và tên ngân hàng tài khoản nhận
    @api.onchange('TK_NHAN_ID')
    def _update_thong_tin_nhan(self):
        thong_tin_ngan_hang_tk_nhan = ''
        # kiểm tra nếu có tên và chi nhánh của ngân hàng thì lấy luôn thông tin
        if self.TK_NHAN_ID.TEN_NGAN_HANG and self.TK_NHAN_ID.CHI_NHANH:
            thong_tin_ngan_hang_tk_nhan = str(self.TK_NHAN_ID.TEN_NGAN_HANG) + ' - ' +  str(self.TK_NHAN_ID.CHI_NHANH)
        # Nếu không có 1 trong hai thông tin trên thì xét từng trường hợp
        else:
            if self.TK_NHAN_ID.TEN_NGAN_HANG:
                thong_tin_ngan_hang_tk_nhan = str(self.TK_NHAN_ID.TEN_NGAN_HANG)
            elif self.TK_NHAN_ID.CHI_NHANH:
                thong_tin_ngan_hang_tk_nhan = str(self.TK_NHAN_ID.CHI_NHANH)
        self.CHI_NHANH_TK_NHAN = thong_tin_ngan_hang_tk_nhan

    # Hàm để lấy thông tin chi nhánh và tên ngân hàng
    @api.onchange('TK_CHI_ID')
    def _update_thong_tin_chi_nhanh_tk_ngan_hang(self):
        thong_tin_ngan_hang = ''
        # kiểm tra nếu có tên và chi nhánh của ngân hàng thì lấy luôn thông tin
        if self.TK_CHI_ID.NGAN_HANG_ID.name and self.TK_CHI_ID.CHI_NHANH:
            thong_tin_ngan_hang = str(self.TK_CHI_ID.NGAN_HANG_ID.name) + ' - ' +  str(self.TK_CHI_ID.CHI_NHANH)
        # Nếu không có 1 trong hai thông tin trên thì xét từng trường hợp
        else:
            if self.TK_CHI_ID.NGAN_HANG_ID.name:
                thong_tin_ngan_hang = str(self.TK_CHI_ID.NGAN_HANG_ID.name)
            elif self.TK_CHI_ID.CHI_NHANH:
                thong_tin_ngan_hang = str(self.TK_CHI_ID.CHI_NHANH)
        self.CHI_NHANH_TK_CHI = thong_tin_ngan_hang

    @api.depends('LOAI_HOA_DON')
    def thay_doi_nhan_hoa_don(self):
        if self.LOAI_HOA_DON == '1':
            self.NHAN_HOA_DON = 'Đã nhận HĐ'
        elif self.LOAI_HOA_DON == '0': 
            self.NHAN_HOA_DON = 'Chưa nhận HĐ'
        else:
            self.NHAN_HOA_DON = 'Ko có HĐ'

    @api.onchange('LOAI_HOA_DON')
    def _onchange_LOAI_HOA_DON(self):
        if self.LOAI_HOA_DON in ('0','2'):
            if self.CHI_TIET_IDS:
                for line in self.CHI_TIET_IDS:
                    line.TK_THUE_GTGT_ID = False
                    line.THUE_GTGT_ID = False
                    line.TIEN_THUE_GTGT = 0
                    line.TIEN_THUE_GTGT_QUY_DOI = 0

    @api.depends('LOAI_CHUNG_TU_MH')
    def thay_doi_hoa_don(self):
        for record in self:
            if record.LOAI_CHUNG_TU_MH == 'trong_nuoc_nhap_kho':
                record.IS_TH1 = True
                record.IS_TH2 = False
                record.IS_TH3 = False
                record.IS_TH4 = False
            elif record.LOAI_CHUNG_TU_MH == 'trong_nuoc_khong_qua_kho':
                record.IS_TH2 = True
                record.IS_TH1 = False
                record.IS_TH3 = False
                record.IS_TH4 = False
            elif record.LOAI_CHUNG_TU_MH == 'nhap_khau_nhap_kho':
                record.IS_TH3 = True
                record.IS_TH1 = False
                record.IS_TH2 = False
                record.IS_TH4 = False
                record.LOAI_HOA_DON = '1'
            elif record.LOAI_CHUNG_TU_MH == 'nhap_khau_khong_qua_kho':
                record.IS_TH4 = True
                record.IS_TH1 = False
                record.IS_TH3 = False
                record.IS_TH2 = False
                record.LOAI_HOA_DON = '1'

    @api.onchange('LOAI_CHUNG_TU_MH')
    def thay_doi_hoa_don_mh(self):
        if self.LOAI_CHUNG_TU_MH in ('nhap_khau_nhap_kho','nhap_khau_khong_qua_kho') :
            self.LOAI_HOA_DON = '1'
        if self.CHI_TIET_IDS:
            for line in self.CHI_TIET_IDS:
                if self.LOAI_CHUNG_TU_MH in ('trong_nuoc_khong_qua_kho','nhap_khau_khong_qua_kho') :
                    line.KHO_ID = False
                else:
                    if line.MA_HANG_ID:
                        line.KHO_ID = line.MA_HANG_ID.KHO_NGAM_DINH_ID.id
    
    # Detail
    CHI_TIET_HANG_HOA = fields.Selection([
        ('hang_tien', 'Hàng tiền'),
        ('thue', 'Thuế'),
        ('thong_ke', 'Thống kê'),
        ], default='hang_tien', string='NO_SAVE')
    CHI_TIET_DICH_VU = fields.Selection([
        ('HACH_TOAN', 'Hạch toán'),
        ('THUE', 'Thuế'),
        ('THONG_KE', 'Thống kê'),
        ], default='HACH_TOAN', string='NO_SAVE')
    @api.model
    def default_get(self,default_fields):
        res = super(PURCHASE_DOCUMENT, self).default_get(default_fields)
        res['NHAN_HOA_DON'] = 'Đã nhận HĐ'
        if res.get('type') == 'dich_vu':
            res['LOAI_HOA_DON'] = '1'
            res['DIEN_GIAI'] = 'Mua dịch vụ'
        elif res.get('type') == 'hang_hoa':
            res['LOAI_HOA_DON'] = '1'
        # res['currency_id'] = self.env['res.currency'].search([('name', '=', 'VND')]).id
        # elif res.get('DA_THANH_TOAN')==False:
        #     res['LOAI_CHUNG_TU_TEXT'] = 'Chứng từ mua dịch vụ - Chưa thanh toán'
        # elif res.get('DA_THANH_TOAN'):
        #     if res.get('LOAI_THANH_TOAN')=='tien_mat':
        #         res['LOAI_CHUNG_TU_TEXT'] = 'Chứng từ mua dịch vụ - Tiền mặt'
        #     elif res.get('LOAI_THANH_TOAN')=='uy_nhiem_chi':
        #         res['LOAI_CHUNG_TU_TEXT'] = 'Chứng từ mua dịch vụ - Uỷ nhiệm chi'
        #     elif res.get('LOAI_THANH_TOAN')=='sec_chuyen_khoan':
        #         res['LOAI_CHUNG_TU_TEXT'] = 'Chứng từ mua dịch vụ - Séc chuyển khoản'
        #     else:
        #         res['LOAI_CHUNG_TU_TEXT'] = 'Chứng từ mua dịch vụ - Séc tiền mặt'
        res['CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH'] = self.env['ir.config_parameter'].get_param('he_thong.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH')
        
        return res


    # @api.onchange('LOAI_THANH_TOAN')
    # def update_SO_CHUNG_TU(self):
    #     loai_chung_tu = False
    #     if self.LOAI_THANH_TOAN == 'tien_mat':
    #         loai_chung_tu='tien_mat'
    #     elif self.LOAI_THANH_TOAN =='uy_nhiem_chi':
    #         loai_chung_tu='uy_nhiem_chi'
    #     elif self.LOAI_THANH_TOAN =='sec_chuyen_khoan':
    #         loai_chung_tu='sec_chuyen_khoan'
    #     else:
    #         loai_chung_tu='sec_tien_mat'
        
    #     if loai_chung_tu:    
    #         auto_num = self.lay_so_chung_tu_tu_tang(loai_chung_tu)
    #         self.SO_CHUNG_TU = auto_num.get(loai_chung_tu)
    #         self.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num)



    # def lay_so_chung_tu_tu_tang(self, loai_chung_tu):
    #     auto_num = json.loads(self.SO_CHUNG_TU_TU_TANG_JSON or '{}')
    #     if not auto_num.get(loai_chung_tu):
    #         code = 'purchase_SO_CHUNG_TU_' + loai_chung_tu
    #         next_seq = self.env['ir.sequence'].next_char_by_code(code)
    #         auto_num[loai_chung_tu] = next_seq
    #     return auto_num









    @api.onchange('currency_id')
    def cap_nhat_cac_cot_o_hang_tien(self):
        if self.currency_id:
            if self.currency_id.MA_LOAI_TIEN =='VND':
                self.TAI_KHOAN_TIEN =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1112')],limit=1).id
            else:
                self.TAI_KHOAN_TIEN = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1111')],limit=1).id
            self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
            if self.TY_GIA == 1.0 :
                self.LA_TIEN_CO_SO = True
            else:
                self.LA_TIEN_CO_SO = False

    @api.multi
    def action_ghi_so(self):
        for record in self:
            if record.type == 'hang_hoa':
                record.ghi_so_cai_mua_hang()
            elif record.type == 'dich_vu':
                record.ghi_so_cai_mua_dich_vu()
                # Nhận kèm hóa đơn - https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3521/
                if record.LOAI_HOA_DON == '1':
                    record.ghi_so_thue()
            record.ghi_so_mua_hang()
            if not record.DA_THANH_TOAN:
                if record.type == 'hang_hoa':
                    record.ghi_so_cong_no_mua_hang()
                elif record.type == 'dich_vu':
                    record.ghi_so_cong_no_mua_dich_vu()
            if record.type == 'hang_hoa':
                if record.LOAI_CHUNG_TU_MH in ('trong_nuoc_nhap_kho','nhap_khau_nhap_kho'):
                    record.ghi_so_kho()
            # Ghi sổ các references
            hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
            if record.type == 'hang_hoa':
                if hoa_don:
                    hoa_don.action_ghi_so()
                    hoa_don.ghi_so_thue_qua_chung_tu_mua_hang()
        self.write({'state':'da_ghi_so'})

    @api.multi
    def action_bo_ghi_so(self, args):
        # Bỏ ghi sổ các references
        for record in self:
            hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
            if hoa_don:
                hoa_don.action_bo_ghi_so()
        return super(PURCHASE_DOCUMENT, self).action_bo_ghi_so()
        
    
    def ghi_so_cai_mua_hang(self):
        line_ids = []
        thu_tu = 0
        loai_tien_vnd = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1).id
        for line in self.CHI_TIET_IDS:
            # dien_giai_chung = self.DIEN_GIAI_CHUNG
            so_chung_tu_cap_phu = self.SO_CHUNG_TU
            # nguoi_lien_he = self.NGUOI_GIAO_HANG
            if 'hang_hoa' == self.type and self.LOAI_CHUNG_TU_MH in ('trong_nuoc_nhap_kho','nhap_khau_nhap_kho'):
                if self.DA_THANH_TOAN:
                    # dien_giai_chung = self.LY_DO_CHI
                    # nguoi_lien_he = self.NGUOI_NHAN
                    if self.LOAI_THANH_TOAN == 'uy_nhiem_chi':
                        so_chung_tu_cap_phu = self.SO_UY_NHIEM_CHI
                    elif self.LOAI_THANH_TOAN == 'sec_chuyen_khoan':
                        so_chung_tu_cap_phu = self.SO_SEC_CHUYEN_KHOAN
                    elif self.LOAI_THANH_TOAN == 'sec_tien_mat':
                        so_chung_tu_cap_phu = self.SO_SEC_TIEN_MAT
                    else:
                        so_chung_tu_cap_phu = self.SO_PHIEU_CHI

            if self.LOAI_HOA_DON == '1':
                ngay_hoa_don = self.NGAY_HOA_DON
                so_hoa_don = self.SO_HOA_DON
            else:
                if self.HOA_DON_MUA_HANG_ID:
                    ngay_hoa_don = self.HOA_DON_MUA_HANG_ID.NGAY_HOA_DON
                    so_hoa_don = self.HOA_DON_MUA_HANG_ID.SO_HOA_DON
                else:
                    ngay_hoa_don = None
                    so_hoa_don = None
                
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,
                'MODEL_CHUNG_TU' : self._name,
                'CHI_TIET_ID' : line.id,
                'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI' : line.name,
                'DVT_ID' : line.DVT_ID.id,
                'SO_LUONG' : line.SO_LUONG,
                'DON_GIA' : line.DON_GIA,
                'LOAI_HACH_TOAN' : '1',
                # 'currency_id' : loai_tien_vnd,
                # 'TY_GIA' : 1,
                'TAI_KHOAN_NGAN_HANG_ID' : self.TK_CHI_ID.id,
                'SO_HOA_DON' : so_hoa_don,
                'NGAY_HOA_DON' : ngay_hoa_don,
                'NGUOI_LIEN_HE' : self.NGUOI_GIAO_HANG,
                'DON_GIA' : line.DON_GIA*self.TY_GIA,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI_CHUNG,
            })
            
            if self.LOAI_CHUNG_TU in (368, 369, 370, 371, 372, 374, 375, 376, 377, 378,318, 319, 320, 321, 322, 324, 325, 326, 327, 328):
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TAI_KHOAN_ID': line.TK_NO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                    'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                    # 'currency_id' : self.currency_id.id if line.TK_NO_ID.CO_HACH_TOAN_NGOAI_TE == True else loai_tien_vnd,
                    # 'TY_GIA' : self.TY_GIA if line.TK_NO_ID.CO_HACH_TOAN_NGOAI_TE == True else 1,
                })
                line_ids += [(0,0,data_ghi_no)]

                data_ghi_co = data_goc.copy()
                data_ghi_co.update({
                    'TAI_KHOAN_ID': line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                    'LOAI_HACH_TOAN' : '2',
                    'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    # 'currency_id' : self.currency_id.id if line.TK_CO_ID.CO_HACH_TOAN_NGOAI_TE == True else loai_tien_vnd,
                    # 'TY_GIA' : self.TY_GIA if line.TK_CO_ID.CO_HACH_TOAN_NGOAI_TE == True else 1,
                    'NGUOI_LIEN_HE' : self.NGUOI_NHAN,
                    'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                })
                line_ids += [(0,0,data_ghi_co)]

                if line.TK_THUE_BVMT and (line.TIEN_THUE_BVMT or line.TIEN_THUE_BVMT_QUY_DOI):
                    data_thue_bvmt = data_goc.copy()
                    data_thue_bvmt.update({
                        'TAI_KHOAN_ID': line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_BVMT.id,
                        'GHI_NO' : line.TIEN_THUE_BVMT,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_BVMT,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    })
                    line_ids += [(0,0,data_thue_bvmt)]

                    data_thue_bvmt2 = data_goc.copy()
                    data_thue_bvmt2.update({
                        'TAI_KHOAN_ID': line.TK_THUE_BVMT.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_BVMT,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_BVMT,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    })
                    line_ids += [(0,0,data_thue_bvmt2)]

                if line.TK_THUE_NK_ID and (line.TIEN_THUE_NK or line.TIEN_THUE_NK_QUY_DOI):
                    data_thue_nk = data_goc.copy()
                    data_thue_nk.update({
                        'TAI_KHOAN_ID': line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_NK_ID.id,
                        'GHI_NO' : line.TIEN_THUE_NK_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_NK,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    })
                    line_ids += [(0,0,data_thue_nk)]

                    data_thue_nk2 = data_goc.copy()
                    data_thue_nk2.update({
                        'TAI_KHOAN_ID': line.TK_THUE_NK_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_NK_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_NK,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    })
                    line_ids += [(0,0,data_thue_nk2)]

                if line.TK_THUE_TTDB_ID and (line.TIEN_THUE_TTDB or line.TIEN_THUE_TTDB_QUY_DOI):
                    data_thue_ttdb = data_goc.copy()
                    data_thue_ttdb.update({
                        'TAI_KHOAN_ID': line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_TTDB_ID.id,
                        'GHI_NO' : line.TIEN_THUE_TTDB_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_TTDB,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    })
                    line_ids += [(0,0,data_thue_ttdb)]

                    data_thue_ttdb2 = data_goc.copy()
                    data_thue_ttdb2.update({
                        'TAI_KHOAN_ID': line.TK_THUE_TTDB_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_TTDB_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_TTDB,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                    })
                    line_ids += [(0,0,data_thue_ttdb2)]

                if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT != 0 or line.TIEN_THUE_GTGT_QUY_DOI != 0):
                    data_thue_gtgt_doi_ung = data_goc.copy()
                    data_thue_gtgt_doi_ung.update({
                        'TAI_KHOAN_ID': line.TK_DU_THUE_GTGT_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                        'GHI_NO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : float_round(line.TIEN_THUE_GTGT,0),
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                    })
                    line_ids += [(0,0,data_thue_gtgt_doi_ung)]

                    data_thue_gtgt_doi_ung2 = data_goc.copy()
                    data_thue_gtgt_doi_ung2.update({
                        'TAI_KHOAN_ID': line.TK_THUE_GTGT_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_DU_THUE_GTGT_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : float_round(line.TIEN_THUE_GTGT,0),
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                    })
                    line_ids += [(0,0,data_thue_gtgt_doi_ung2)]

                if line.TK_DU_THUE_GTGT_ID and not line.TK_DU_THUE_GTGT_ID and (line.TIEN_THUE_GTGT != 0 or line.TIEN_THUE_GTGT_QUY_DOI != 0):
                    data_thue_gtgt = data_goc.copy()
                    data_thue_gtgt.update({
                        'TAI_KHOAN_ID': line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                        'GHI_NO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    })
                    line_ids += [(0,0,data_thue_gtgt)]

                    data_thue_gtgt2 = data_goc.copy()
                    data_thue_gtgt2.update({
                        'TAI_KHOAN_ID': line.TK_THUE_GTGT_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    })
                    line_ids += [(0,0,data_thue_gtgt2)]
            else:
                if not line.TK_THUE_GTGT_ID or self.LOAI_HOA_DON != '1':
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TAI_KHOAN_ID': line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                        'GHI_NO' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                        # 'currency_id' : self.currency_id.id,
                    })
                    line_ids += [(0,0,data_ghi_no)]

                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TAI_KHOAN_ID': line.TK_CO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU + line.TIEN_THUE_GTGT,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        # 'currency_id' : self.currency_id.id,
                        # 'TY_GIA' : self.TY_GIA,
                        'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                        'NGUOI_LIEN_HE' : self.NGUOI_NHAN if self.DA_THANH_TOAN == True else self.NGUOI_GIAO_HANG,
                    })
                    line_ids += [(0,0,data_ghi_co)]

                if line.TK_THUE_GTGT_ID and self.LOAI_HOA_DON == '1':
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TAI_KHOAN_ID': line.TK_NO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                        'GHI_NO' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                    })
                    line_ids += [(0,0,data_ghi_no)]

                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TAI_KHOAN_ID': line.TK_CO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                        'NGUOI_LIEN_HE' : self.NGUOI_NHAN if self.DA_THANH_TOAN == True else self.NGUOI_GIAO_HANG,
                    })
                    line_ids += [(0,0,data_ghi_co)]

                if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT != 0 or line.TIEN_THUE_GTGT_QUY_DOI != 0):
                    data_thue_gtgt = data_goc.copy()
                    data_thue_gtgt.update({
                        'TAI_KHOAN_ID': line.TK_THUE_GTGT_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                        'GHI_NO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO' : 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                    })
                    line_ids += [(0,0,data_thue_gtgt)]

                    data_thue_gtgt2 = data_goc.copy()
                    data_thue_gtgt2.update({
                        'TAI_KHOAN_ID': line.TK_CO_ID.id,
                        'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                        'GHI_NO' : 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO' : line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'LOAI_HACH_TOAN' : '2',
                        'SO_CHUNG_TU' : so_chung_tu_cap_phu,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        'DIEN_GIAI_CHUNG' : self.LY_DO_CHI if self.DA_THANH_TOAN == True else self.DIEN_GIAI_CHUNG,
                        'NGUOI_LIEN_HE' : self.NGUOI_NHAN if self.DA_THANH_TOAN == True else self.NGUOI_GIAO_HANG,
                    })
                    line_ids += [(0,0,data_thue_gtgt2)]
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


    def ghi_so_cai_mua_dich_vu(self):
        line_ids = []
        thu_tu = 0
        for line in self.CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                'GHI_NO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
                'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
                'DIEN_GIAI' : line.name,
                'DVT_ID' : line.DVT_ID.id,
                'SO_LUONG' : line.SO_LUONG,
                'DON_GIA' : line.DON_GIA,
                'LOAI_HACH_TOAN' : '1',
                'NGAY_HOA_DON' : line.NGAY_HOA_DON,
                'SO_HOA_DON' : line.SO_HOA_DON_DETAIL,
                'NGUOI_LIEN_HE' : self.NGUOI_NHAN,
            })
            
            if self.LOAI_THANH_TOAN == 'tien_mat':
                data_ghi_no.update({
                    'TAI_KHOAN_NGAN_HANG_ID' : self.TK_CHI_ID.id,
                })
            # elif self.LOAI_THANH_TOAN == 'uy_nhiem_chi':
            #     data_ghi_no.update({
            #         'DIEN_GIAI' : self.NOI_DUNG_THANH_TOAN,
            #     })
            elif self.LOAI_THANH_TOAN == 'sec_chuyen_khoan':
                data_ghi_no.update({
                    'TAI_KHOAN_NGAN_HANG_ID' : self.TK_CHI_ID.id,
                    # 'DIEN_GIAI' : self.NOI_DUNG_THANH_TOAN,
                })
            # else:
            #     data_ghi_no.update({
            #         'DIEN_GIAI' : self.NOI_DUNG_THANH_TOAN,
            #     })
            line_ids += [(0,0,data_ghi_no)]
            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID': line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                'GHI_CO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
                'LOAI_HACH_TOAN' : '2',
                'NGUOI_LIEN_HE' : self.NGUOI_NHAN,
            })
            line_ids += [(0,0,data_ghi_co)]
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                data_gtgt1 = data_ghi_no.copy()
                data_gtgt1.update({
                    'TAI_KHOAN_ID' : line.TK_THUE_GTGT_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    'GHI_NO' : line.TIEN_THUE_GTGT,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
					'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_gtgt1)]

                data_gtgt2 = data_gtgt1.copy()
                data_gtgt2.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.TIEN_THUE_GTGT,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
					'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_gtgt2)]
            thu_tu += 1
        # Tạo master
        scdv = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = scdv.id
        return True

    def ghi_so_mua_hang(self):
        line_ids = []
        thu_tu = 0
        for line in self.CHI_TIET_IDS:
            sl = line.MA_HANG_ID.compute_SO_LUONG(line.SO_LUONG,line.DVT_ID.id)
            if self.type == 'hang_hoa':
                if self.LOAI_HOA_DON == '1':
                    ngay_hoa_don = self.NGAY_HOA_DON
                    so_hoa_don = self.SO_HOA_DON
                else:
                    if self.HOA_DON_MUA_HANG_ID:
                        ngay_hoa_don = self.HOA_DON_MUA_HANG_ID.NGAY_HOA_DON
                        so_hoa_don = self.HOA_DON_MUA_HANG_ID.SO_HOA_DON
                    else:
                        ngay_hoa_don = None
                        so_hoa_don = None
            else:
                ngay_hoa_don = line.NGAY_HOA_DON
                so_hoa_don = line.SO_HOA_DON_DETAIL
            data = helper.Obj.inject(line, self)
            data.update({
                'DIEN_GIAI': line.name,
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'SO_LUONG' : line.SO_LUONG,
                'DON_GIA' : line.THANH_TIEN_QUY_DOI/line.SO_LUONG if line.SO_LUONG != 0 else 0,
                'currency_id' : self.currency_id.id,
                'PHAN_TRAM_CHIET_KHAU' : line.TY_LE_CK,
                'DVT_ID' : line.DVT_ID.id,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'SO_TIEN': line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_CHIET_KHAU': line.TIEN_CHIET_KHAU_QUY_DOI,
                'SO_TIEN_CHIET_KHAU_NGUYEN_TE': line.TIEN_CHIET_KHAU,
                'PHAN_TRAM_THUE_VAT' : line.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT' : line.TIEN_THUE_GTGT_QUY_DOI,
                'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                'TAI_KHOAN_VAT_ID' : line.TK_THUE_GTGT_ID.id,
                'SO_TIEN_NHAP_KHAU' : line.TIEN_THUE_NK,
                'SO_TIEN_NHAP_KHAU' : line.TIEN_THUE_NK,
                'TAI_KHOAN_NHAP_KHAU_ID' : line.TK_THUE_NK_ID.id,
                'HOP_DONG_ID' : line.HOP_DONG_MUA_ID.id,
                # 'DVT_CHINH_ID' : line.MA_HANG_ID.DVT_CHINH_ID.id,
                'SO_LUONG_THEO_DVT_CHINH' : sl,
                'SO_HOA_DON' : so_hoa_don,
                'NGAY_HOA_DON' : ngay_hoa_don,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
                'DIEU_KHOAN_THANH_TOAN_ID' : self.DIEU_KHOAN_THANH_TOAN_ID.id,
                'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
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

    def ghi_so_cong_no_mua_hang(self):
        line_ids = []
        thu_tu = 0
        for line in self.CHI_TIET_IDS:
            
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.name,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI_CHUNG,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'SO_LUONG' : line.SO_LUONG,
                'DON_GIA' : line.DON_GIA,
                'currency_id' : self.currency_id.id,
                'TY_GIA' : self.TY_GIA,
                'DON_GIA' : line.THANH_TIEN_QUY_DOI/line.SO_LUONG if line.SO_LUONG != 0 else line.DON_GIA,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
            })
            if self.LOAI_CHUNG_TU in (352, 357, 358, 359, 360, 362, 363, 364, 365, 366,302, 307, 308, 309, 310, 312, 313, 314, 315, 316):
                if not line.TK_THUE_GTGT_ID or self.LOAI_HOA_DON != '1':
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                            'GHI_NO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU + line.TIEN_THUE_GTGT,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
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
                            'GHI_CO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU + line.TIEN_THUE_GTGT,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        
                    # ghi_no = line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI + line.TIEN_THUE_GTGT_QUY_DOI
                    # ghi_no_nguyen_te = line.THANH_TIEN - line.TIEN_CHIET_KHAU + line.TIEN_THUE_GTGT
                if line.TK_THUE_GTGT_ID and self.LOAI_HOA_DON == '1':
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                            'GHI_NO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
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
                            'GHI_CO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        
                if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                    if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_THUE_GTGT_ID.id,
                            'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                            'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                        
                    if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_CO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        
            else:
                if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_NO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
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
                        'GHI_CO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                        'LOAI_HACH_TOAN' : '2',
                    })
                    line_ids += [(0,0,data_ghi_co)]
                    

                if line.TK_THUE_BVMT and (line.TIEN_THUE_BVMT !=0 or line.TIEN_THUE_BVMT_QUY_DOI !=0):
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_BVMT.id,
                            'GHI_NO': line.TIEN_THUE_BVMT_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_BVMT,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                        
                    if line.TK_THUE_BVMT.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_BVMT.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_BVMT_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_BVMT,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        

                if line.TK_THUE_NK_ID and (line.TIEN_THUE_NK !=0 or line.TIEN_THUE_NK_QUY_DOI !=0):
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_NK_ID.id,
                            'GHI_NO': line.TIEN_THUE_NK_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_NK,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                        
                    if line.TK_THUE_NK_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_NK_ID.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_NK_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_NK,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        

                if line.TK_THUE_TTDB_ID and (line.TIEN_THUE_TTDB !=0 or line.TIEN_THUE_TTDB_QUY_DOI !=0):
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_TTDB_ID.id,
                            'GHI_NO': line.TIEN_THUE_TTDB_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_TTDB,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                        
                    if line.TK_THUE_TTDB_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_TTDB_ID.id,
                            'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_TTDB_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_TTDB,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        

                if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                    if line.TK_DU_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_DU_THUE_GTGT_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                            'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                            'LOAI_HACH_TOAN' : '1',
                        })
                        line_ids += [(0,0,data_ghi_no)]
                        
                    if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_co = data_goc.copy()
                        data_ghi_co.update({
                            'TK_ID': line.TK_THUE_GTGT_ID.id,
                            'TK_DOI_UNG_ID': line.TK_DU_THUE_GTGT_ID.id,
                            'GHI_NO': 0,
                            'GHI_NO_NGUYEN_TE' : 0,
                            'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                            'LOAI_HACH_TOAN' : '2',
                        })
                        line_ids += [(0,0,data_ghi_co)]
                        

                if line.TK_DU_THUE_GTGT_ID and not line.TK_DU_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                    if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                        data_ghi_no = data_goc.copy()
                        data_ghi_no.update({
                            'TK_ID': line.TK_NO_ID.id,
                            'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                            'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                            'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'GHI_CO': 0,
                            'GHI_CO_NGUYEN_TE' : 0,
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                            'LOAI_HACH_TOAN' : '1',
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
                            'DIEN_GIAI' : line.DIEN_GIAI_THUE,
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

    def ghi_so_cong_no_mua_dich_vu(self):
        line_ids = []
        thu_tu = 0
        for line in self.CHI_TIET_IDS:
            
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.name,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI_CHUNG,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'SO_LUONG' : line.SO_LUONG,
                'DON_GIA' : line.DON_GIA,
                'currency_id' : self.currency_id.id,
                'TY_GIA' : self.TY_GIA,
                'DON_GIA' : line.THANH_TIEN_QUY_DOI/line.SO_LUONG if line.SO_LUONG != 0 else line.DON_GIA,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
            })
            if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TK_ID': line.TK_NO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                    'GHI_CO': 0,
                    'GHI_CO_NGUYEN_TE' : 0,
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
                    'GHI_CO': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_co)]
                
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_THUE_GTGT_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_ghi_no)]
                    
                if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_CO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
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

    def ghi_so_thue(self):
        line_ids = []
        thu_tu = 0
        
        for line in self.CHI_TIET_IDS:
            data = helper.Obj.inject(line, self)
            # nam = self.NGAY_HOA_DON.year
            # thang = self.NGAY_HOA_DON.month
            # ngay_chung_tu = '%s-%s-01'%(nam,thang)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                'PHAN_TRAM_VAT': line.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT': line.TIEN_THUE_GTGT,
                'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                'SO_TIEN_CHIU_VAT': line.THANH_TIEN,
                'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.THANH_TIEN,
                'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                # 'DOI_TUONG_ID' : line.DOI_TUONG_ID.id,
                'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_ID.id,
                'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                'NGAY_HACH_TOAN' : self.NGAY_HACH_TOAN,
                'DIEN_GIAI' : line.name,
                'NGAY_HOA_DON' : line.NGAY_HOA_DON,
                'SO_HOA_DON' : line.SO_HOA_DON_DETAIL,
                'MAU_SO_HD_ID' : line.MAU_SO_HD_ID.id,
                'KY_HIEU_HOA_DON' : line.KY_HIEU_HOA_DON,
                'MA_SO_THUE_DOI_TUONG' : line.MA_SO_THUE_NCC,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True
    
    def ghi_so_kho(self):
        line_ids = []
        thu_tu = 0
        for line in self.CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI' : line.name,
                'TK_NO_ID' : line.TK_NO_ID.id,
                'TK_CO_ID' : line.TK_CO_ID.id,
                'SO_TIEN_NHAP' : line.GIA_TRI_NHAP_KHO,
                'SO_TIEN_XUAT' : 0,
                'KHO_ID' : line.KHO_ID.id,
                'DVT_ID' : line.DVT_ID.id,
                'SO_LUONG_NHAP' : line.SO_LUONG,
                'SO_LUONG_XUAT' : 0,
                # 'DON_GIA' : line.DON_GIA,
                'DON_GIA' : float_round(line.GIA_TRI_NHAP_KHO/line.SO_LUONG,0) if line.SO_LUONG != 0 else line.DON_GIA,
                'currency_id' : self.currency_id.id,
                'DVT_CHINH_ID' : line.DVT_ID.id,
                'NGAY_HET_HAN' : self.HAN_THANH_TOAN,
                'LOAI_KHU_VUC_NHAP_XUAT' : '1',
                'LA_NHAP_KHO' : True,
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

    ################################################
    ##############START _BO_GHI_SO_#################
    ################################################
    # @api.multi
    # def action_bo_ghi_so(self, args=None):
    #     # Todof: Hiện tại chưa support multi
    #     self.ensure_one()
    #     loi = False
    #     str_loi = ''
    #     id_chung_tu_lien_quan = 0
    #     loai_loi = ''
    #     # 1. check_cac_chung_tu_lien_quan_khac
    #     cac_chung_tu_lien_quan_khac = self.check_cac_chung_tu_lien_quan_khac(self.id,self._name,self.get_chi_nhanh())
    #     if cac_chung_tu_lien_quan_khac:
    #         str_loi = 'Chứng từ này đã có phát sinh <' +str(cac_chung_tu_lien_quan_khac[0].get('TEN_LOI'))+' >. Để bỏ ghi sổ chứng từ này thì phải xóa chứng từ liên quan. Bỏ ghi sổ không thành công. Bạn có muốn xem chi tiết danh sách chứng từ liên quan không?'
    #         loi = True
    #         loai_loi = 'CAC_CHUNG_TU_LIEN_QUAN'
    #     # 2. check_chung_tu_ghi_so
    #     if not loi:
    #         chung_tu_ghi_so = self.check_chung_tu_ghi_so(self.id,self._name,self.get_chi_nhanh())
    #         if chung_tu_ghi_so:
    #             str_loi = 'Bỏ ghi sổ không thành công. Chứng từ này đã được lập chứng từ ghi sổ '+str(chung_tu_ghi_so[0].get('SO_CHUNG_TU'))+ '. Bạn có muốn xem không?'
    #             loi = True
    #             loai_loi = 'CHUNG_TU_GHI_SO'
    #     # 3. check_chung_chi_phi
    #     if not loi:
    #         if self._name == 'purchase.document':
    #             chung_chi_phi = self.check_chung_chi_phi(self.id,self.get_chi_nhanh())
    #             if chung_chi_phi:
    #                 str_loi = 'Hóa đơn mua dịch vụ đã được chọn để phân bổ chi phí mua hàng. Bạn có muốn bỏ ghi không?'
    #                 loi = True
    #                 # sql chắc chắn trả về 1 dòng
    #                 id_chung_tu_lien_quan = chung_chi_phi[0].get('ID_CHUNG_TU')
    #                 loai_loi = 'PB_CHI_PHI'
    #     # 4. check_doi_tru_chung_tu
    #     if not loi:
    #         doi_tru_chung_tu = self.check_doi_tru_chung_tu(self.id,self._name,self.get_chi_nhanh())
    #         if doi_tru_chung_tu:
    #             str_loi = 'Chứng từ này đã có phát sinh đối trừ chứng từ. Để bỏ ghi chứng từ này thì bạn phải bỏ đối trừ. Bạn có muốn thực hiện không?'
    #             loi = True
    #             loai_loi = 'DOI_TRU_CHUNG_TU'
    #     if loi == False:
    #         self.bo_ghi_so()
    #     return {
    #         'loi' : loi,
    #         'str_loi' : str_loi,
    #         'id_chung_tu_lien_quan' : id_chung_tu_lien_quan,
    #         'loai_loi' : loai_loi,
    #         }

    # def check_cac_chung_tu_lien_quan_khac(self,id_chung_tu,model_chung_tu,chi_nhanh_id):
    #     params = {
    #         'ID_CHUNG_TU' : id_chung_tu,
    #         'CHI_NHANH_ID' : chi_nhanh_id,
    #         'MODEL_CHUNG_TU' : model_chung_tu,
    #         }
    #     query = """ 

    #     DO LANGUAGE plpgsql $$ DECLARE

    #         id_chung_tu  INTEGER := %(ID_CHUNG_TU)s;
    #         model_chung_tu VARCHAR(50):= %(MODEL_CHUNG_TU)s;
    #         chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s ;


    #         BEGIN

    #         DROP TABLE IF EXISTS TMP_KET_QUA;
    #         CREATE TEMP TABLE TMP_KET_QUA(
    #         "LOAI_LOI" INTEGER,
    #         "TEN_LOI" VARCHAR(50)
    #         );

    #         --Kiểm tra tồn tại chứng từ Thu tiền khách hàng (Cả tiền mặt & tiền gửi)
    #         IF EXISTS ( SELECT  *
    #                     FROM    sale_ex_doi_tru_chi_tiet
    #                     WHERE   "ID_CHUNG_TU_CONG_NO" = id_chung_tu
    #                             AND "MODEL_CHUNG_TU_CONG_NO" = model_chung_tu
    #                             AND "LOAI_DOI_TRU" = '0'
    #                             AND "LOAI_CHUNG_TU_THANH_TOAN" IN ( 1011, 1012, 1502, 1503 )
    #                             AND "CHI_NHANH_ID" = chi_nhanh_id )
    #         THEN
    #             INSERT  INTO TMP_KET_QUA VALUES  ( 0, N'Thu tiền khách hàng' );
    #         END IF ;

    #         --Kiểm tra tồn tại chứng từ Trả tiền NCC (Cả tiền mặt & tiền gửi)
    #         IF EXISTS ( SELECT  *
    #                     FROM    sale_ex_doi_tru_chi_tiet
    #                     WHERE   "ID_CHUNG_TU_CONG_NO" = id_chung_tu
    #                             AND "MODEL_CHUNG_TU_CONG_NO" = model_chung_tu
    #                             AND "LOAI_DOI_TRU" = '0'
    #                             AND "LOAI_CHUNG_TU_THANH_TOAN" IN ( 1021, 1511, 1521, 1531 )
    #                             AND "CHI_NHANH_ID" = chi_nhanh_id)
    #         THEN
    #             INSERT  INTO TMP_KET_QUA
    #             VALUES  ( 1, N'Trả tiền nhà cung cấp' );
    #         END IF ;

    #         --Kiểm tra tồn tại Bù trừ công nợ
    #         IF EXISTS ( SELECT  *
    #                     FROM    sale_ex_doi_tru_chi_tiet
    #                     WHERE   "ID_CHUNG_TU_CONG_NO" = id_chung_tu
    #                             AND "MODEL_CHUNG_TU_CONG_NO" = model_chung_tu
    #                             AND "LOAI_DOI_TRU" = '2'
    #                             AND "CHI_NHANH_ID" = chi_nhanh_id)
    #         THEN
    #             INSERT  INTO TMP_KET_QUA
    #             VALUES  ( 2, N'Bù trừ công nợ' );
    #         END IF ;

    #         --Kiểm tra tồn tại Chứng từ đánh giá lại TK ngoại tệ
    #         IF EXISTS ( SELECT  *
    #                     FROM    account_ex_chung_tu_nghiep_vu_khac GL
    #                             INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan AS GVDDP ON GL.id = GVDDP."CHUNG_TU_NGHIEP_VU_KHAC_ID"
    #                     WHERE   "CHI_NHANH_ID" = chi_nhanh_id
    #             AND "LOAI_CHUNG_TU" = 4016
    #                             AND GVDDP."ID_CHUNG_TU_GOC" = id_chung_tu AND "MODEL_CHUNG_TU_GOC" = model_chung_tu)
    #         THEN
    #             INSERT  INTO TMP_KET_QUA
    #             VALUES  ( 3, N'Đánh giá lại tài khoản ngoại tệ' );
    #         END IF ;
    #         END $$;

    #         SELECT *FROM TMP_KET_QUA

    #     """  
    #     return self.execute(query, params)


    # def check_chung_chi_phi(self,id_chung_tu,chi_nhanh_id):
    #     params = {
    #         'ID_CHUNG_TU' : id_chung_tu,
    #         'CHI_NHANH_ID' : chi_nhanh_id,
    #         }
    #     query = """ 

    #         DO LANGUAGE plpgsql $$ DECLARE

    #         id_chung_tu  INTEGER := %(ID_CHUNG_TU)s;
    #         chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s ;


    #         BEGIN
    #             DROP TABLE IF EXISTS TMP_KET_QUA
    #             ;

    #             CREATE TEMP TABLE TMP_KET_QUA (
    #                 "ID_CHUNG_TU" INTEGER,
    #                 "LOAI_LOI"    INTEGER,
    #                 "TEN_LOI"     VARCHAR(50)
    #             )
    #             ;

    #             IF EXISTS(
    #                 SELECT
    #                     PC."ID_CHUNG_TU_GOC"
    #                     , *
    #                 FROM purchase_document PU
    #                     INNER JOIN purchase_chi_phi PC ON PC."purchase_document_id" = PU.id
    #                 WHERE PC."ID_CHUNG_TU_GOC" = id_chung_tu AND "CHI_NHANH_ID" = chi_nhanh_id
    #             )
    #             THEN
    #                 INSERT INTO TMP_KET_QUA (
    #                     SELECT
    #                         PU.id        AS "ID_CHUNG_TU"
    #                         , 0            AS "LOAI_LOI"
    #                         , N'Mua hàng' AS "TEN_LOI"
    #                     FROM purchase_document PU
    #                         INNER JOIN purchase_chi_phi PC ON PC."purchase_document_id" = PU.id
    #                     WHERE PC."ID_CHUNG_TU_GOC" = id_chung_tu AND PU."CHI_NHANH_ID" = chi_nhanh_id AND state = 'da_ghi_so')
    #                 ;
    #             END IF
    #             ;

    #         END $$;

    #         SELECT *FROM TMP_KET_QUA;

    #     """  
    #     return self.execute(query, params)

    # def check_doi_tru_chung_tu(self,id_chung_tu,model_chung_tu,chi_nhanh_id):
    #     params = {
    #         'ID_CHUNG_TU' : id_chung_tu,
    #         'CHI_NHANH_ID' : chi_nhanh_id,
    #         'MODEL_CHUNG_TU' : model_chung_tu,
    #         }
    #     query = """ 

    #     DO LANGUAGE plpgsql $$ DECLARE

    #         id_chung_tu  INTEGER := %(ID_CHUNG_TU)s;
    #         chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s ;
    #         model_chung_tu VARCHAR(50) := %(MODEL_CHUNG_TU)s ;


    #         BEGIN

    #             DROP TABLE IF EXISTS TMP_KET_QUA
    #             ;

    #             CREATE TEMP TABLE TMP_KET_QUA
    #                 AS
    #                     SELECT
    #                         id_chung_tu AS RefID
    #                         , GVCED.*
    #                     FROM sale_ex_doi_tru_chi_tiet AS GVCED
    #                     WHERE (("ID_CHUNG_TU_THANH_TOAN" = id_chung_tu AND "MODEL_CHUNG_TU_THANH_TOAN" = model_chung_tu) OR
    #                         ("ID_CHUNG_TU_CONG_NO" = id_chung_tu AND "MODEL_CHUNG_TU_CONG_NO" = model_chung_tu))
    #                         AND "CHI_NHANH_ID" = chi_nhanh_id
    #                         AND "LOAI_DOI_TRU" = '1'
    #                     ORDER BY GVCED."NGAY_HACH_TOAN_CONG_NO" DESC, GVCED."NGAY_HACH_TOAN_THANH_TOAN" DESC
    #             ;


    #         END $$
    #         ;

    #         SELECT *
    #         FROM TMP_KET_QUA
    #         ;

    #     """  
    #     return self.execute(query, params)

    # def check_chung_tu_ghi_so(self,id_chung_tu,model_chung_tu,chi_nhanh_id):
    #     params = {
    #         'ID_CHUNG_TU' : id_chung_tu,
    #         'CHI_NHANH_ID' : chi_nhanh_id,
    #         'MODEL_GOC' : model_chung_tu,
    #         }
    #     query = """ 

    #     DO LANGUAGE plpgsql $$ DECLARE

    #         id_chung_tu  INTEGER := %(ID_CHUNG_TU)s;
    #         chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s ;
    #         model_goc VARCHAR(50) := %(MODEL_GOC)s;

    #         BEGIN

    #         DROP TABLE IF EXISTS TMP_KET_QUA;
    #         CREATE TEMP TABLE TMP_KET_QUA
    #         AS
    #         SELECT DISTINCT L.* FROM tong_hop_chung_tu_ghi_so_chi_tiet D
    #         INNER JOIN tong_hop_chung_tu_ghi_so L ON L.id = D."CHUNG_TU_GHI_SO_ID"
    #         WHERE D."ID_CHUNG_TU_GOC" = id_chung_tu AND "MODEL_GOC" = model_goc
    #         -- Sắp xếp theo thứ tự giảm dần của Ngày chứng từ hoặc Số Chứng từ
    #         ORDER BY "NGAY_CHUNG_TU" DESC,
    #             "SO_CHUNG_TU" DESC
    #         ;

    #         END $$;

    #         SELECT *FROM TMP_KET_QUA  

    #     """  
    #     return self.execute(query, params)

    # def bo_ghi_so_cac_chung_tu_lien_quan(self, args):
    #     # loi = self.search([('id', '=', args.get('_id'))], limit=1).action_bo_ghi_so(args)
    #     loi = self.env[args.get('model_chung_tu_lien_quan')].search([('id', '=', args.get('id_chung_tu_lien_quan'))]).action_bo_ghi_so(None).get('loi')
    #     if loi == False:
    #         loi = self.action_bo_ghi_so(None).get('loi')
    #     return loi
    ################################################
    ###############END _BO_GHI_SO_##################
    ################################################

    def chung_tu_phan_bo_chi_phi_mua_hang(self, args):
        new_line = [[5]]
        tong_chi_phi_mua_hang = args.get('tong_chi_phi_mua_hang')
        phuong_thuc_phan_bo = args.get('phuong_thuc_phan_bo')
        chi_tiet = args.get('chi_tiet')
        tong_thanh_tien = args.get('tong_thanh_tien')

        tong_so_luong = 0
        tong_thanh_tien = 0
        for phan_bo_chi_tiet in chi_tiet:
            tong_so_luong += phan_bo_chi_tiet.get('SO_LUONG')
            tong_thanh_tien += phan_bo_chi_tiet.get('THANH_TIEN')
            
        if len(chi_tiet) == 1:
            for phan_bo_chi_tiet in chi_tiet:
                new_line += [(0,0,{
                    'MA_HANG_ID' : phan_bo_chi_tiet.get('MA_HANG_ID'),
                    'TEN_HANG' : phan_bo_chi_tiet.get('TEN_HANG'),
                    'SO_LUONG' : phan_bo_chi_tiet.get('SO_LUONG'),
                    'THANH_TIEN' : phan_bo_chi_tiet.get('THANH_TIEN'),
                    'TY_LE_PHAN_BO' : 100,
                    'CHI_PHI_MUA_HANG' : tong_chi_phi_mua_hang
                    })]
        elif len(chi_tiet) > 1:
            if phuong_thuc_phan_bo == 'TY_LE_PT_THEO_SO_LUONG':
                i = 1
                ty_le_da_phan_bo = 0
                chi_phi_mua_hang_da_phan_bo = 0
                for phan_bo_chi_tiet in chi_tiet:
                    if i != len(chi_tiet):
                        new_line += [(0,0,{
                        'MA_HANG_ID' : phan_bo_chi_tiet.get('MA_HANG_ID'),
                        'TEN_HANG' : phan_bo_chi_tiet.get('TEN_HANG'),
                        'SO_LUONG' : phan_bo_chi_tiet.get('SO_LUONG'),
                        'THANH_TIEN' : phan_bo_chi_tiet.get('THANH_TIEN'),
                        'TY_LE_PHAN_BO' : phan_bo_chi_tiet.get('SO_LUONG')/tong_so_luong*100,
                        'CHI_PHI_MUA_HANG' : phan_bo_chi_tiet.get('SO_LUONG')/tong_so_luong*tong_chi_phi_mua_hang,
                        })]
                        ty_le_da_phan_bo += phan_bo_chi_tiet.get('SO_LUONG')/tong_so_luong*100
                        chi_phi_mua_hang_da_phan_bo += phan_bo_chi_tiet.get('SO_LUONG')/tong_so_luong*tong_chi_phi_mua_hang
                    else:
                        new_line += [(0,0,{
                        'MA_HANG_ID' : phan_bo_chi_tiet.get('MA_HANG_ID'),
                        'TEN_HANG' : phan_bo_chi_tiet.get('TEN_HANG'),
                        'SO_LUONG' : phan_bo_chi_tiet.get('SO_LUONG'),
                        'THANH_TIEN' : phan_bo_chi_tiet.get('THANH_TIEN'),
                        'TY_LE_PHAN_BO' : 100 - ty_le_da_phan_bo,
                        'CHI_PHI_MUA_HANG' : tong_chi_phi_mua_hang - chi_phi_mua_hang_da_phan_bo,
                        })]
                    i += 1

            if phuong_thuc_phan_bo == 'TY_LE_PT_THEO_GIA_TRI':
                i = 1
                ty_le_da_phan_bo = 0
                chi_phi_mua_hang_da_phan_bo = 0
                for phan_bo_chi_tiet in chi_tiet:
                    if i != len(chi_tiet):
                        new_line += [(0,0,{
                        'MA_HANG_ID' : phan_bo_chi_tiet.get('MA_HANG_ID'),
                        'TEN_HANG' : phan_bo_chi_tiet.get('TEN_HANG'),
                        'SO_LUONG' : phan_bo_chi_tiet.get('SO_LUONG'),
                        'THANH_TIEN' : phan_bo_chi_tiet.get('THANH_TIEN'),
                        'TY_LE_PHAN_BO' : phan_bo_chi_tiet.get('THANH_TIEN')/tong_thanh_tien*100,
                        'CHI_PHI_MUA_HANG' : phan_bo_chi_tiet.get('THANH_TIEN')/tong_thanh_tien*tong_chi_phi_mua_hang,
                        })]
                        ty_le_da_phan_bo += phan_bo_chi_tiet.get('THANH_TIEN')/tong_thanh_tien*100
                        chi_phi_mua_hang_da_phan_bo += phan_bo_chi_tiet.get('THANH_TIEN')/tong_thanh_tien*tong_chi_phi_mua_hang
                    else:
                        new_line += [(0,0,{
                        'MA_HANG_ID' : phan_bo_chi_tiet.get('MA_HANG_ID'),
                        'TEN_HANG' : phan_bo_chi_tiet.get('TEN_HANG'),
                        'SO_LUONG' : phan_bo_chi_tiet.get('SO_LUONG'),
                        'THANH_TIEN' : phan_bo_chi_tiet.get('THANH_TIEN'),
                        'TY_LE_PHAN_BO' : 100 - ty_le_da_phan_bo,
                        'CHI_PHI_MUA_HANG' : tong_chi_phi_mua_hang - chi_phi_mua_hang_da_phan_bo,
                        })]
                    i += 1

            if phuong_thuc_phan_bo == 'TU_NHAP_PT':
                for phan_bo_chi_tiet in chi_tiet:
                    new_line += [(0,0,{
                    'MA_HANG_ID' : phan_bo_chi_tiet.get('MA_HANG_ID'),
                    'TEN_HANG' : phan_bo_chi_tiet.get('TEN_HANG'),
                    'SO_LUONG' : phan_bo_chi_tiet.get('SO_LUONG'),
                    'THANH_TIEN' : phan_bo_chi_tiet.get('THANH_TIEN'),
                    'TY_LE_PHAN_BO' : phan_bo_chi_tiet.get('TY_LE_PHAN_BO'),
                    'CHI_PHI_MUA_HANG' : phan_bo_chi_tiet.get('TY_LE_PHAN_BO')/100*tong_chi_phi_mua_hang,
                    })]
                        

            if phuong_thuc_phan_bo == 'TU_NHAP_GIA_TRI':
                new_line = chi_tiet

        return new_line


    @api.model
    def uivalidate(self, option=None):
        if self.type == 'hang_hoa':
            if self.LOAI_HOA_DON == '1':
                if self.SO_HOA_DON == False:
                    return "<Số hóa đơn> Không được bỏ trống"

    #Mạnh cap nhat de len mau in vt_01_phieu_nhap_kho
    def print_cap_nhat_de_in(self):
        if self.TEN_DOI_TUONG == False:
            self.TEN_DOI_TUONG = ''
        if self.NGUOI_GIAO_HANG == False:
            self.NGUOI_GIAO_HANG = ''
        
        if self.TEN_DOI_TUONG  == self.NGUOI_GIAO_HANG:
            self.HO_VA_TEN_NGUOI_GIAO = self.TEN_DOI_TUONG
        else:
            if self.TEN_DOI_TUONG == '':
                self.HO_VA_TEN_NGUOI_GIAO =  self.NGUOI_GIAO_HANG
            elif self.NGUOI_GIAO_HANG == '':
                self.HO_VA_TEN_NGUOI_GIAO = self.TEN_DOI_TUONG 
            else:
                self.HO_VA_TEN_NGUOI_GIAO = self.NGUOI_GIAO_HANG + " - " + self.TEN_DOI_TUONG

    #Mạnh bổ sung 2 trường là Tên tài khoản ngân hàng, và địa chỉ ngân hàng để phục vụ cho làm mẫu in ủy nhiệm chi ngân hàng
    TEN_TK_NGAN_HANG  = fields.Char(string='Tên tài khoản Ngân hàng',compute='lay_thong_tin_cua_to_chuc' ,store=False)
    DIA_CHI_NGAN_HANG  = fields.Char(string='Địa chỉ Ngân hàng',compute='lay_thong_tin_cua_to_chuc' ,store=False)

    @api.depends('CHI_NHANH_ID')
    def lay_thong_tin_cua_to_chuc(self):
        for record in self:
            record.TEN_TK_NGAN_HANG = record.CHI_NHANH_ID.TEN_DON_VI
            record.DIA_CHI_NGAN_HANG = record.CHI_NHANH_ID.DIA_CHI

    @api.model
    def chuyen_sang_mau_in_uy_nhiem_chi(self, docids):
        purchase_doc = self.env['purchase.document'].browse(docids)
        records = []
        for pu in purchase_doc:
            account = self.env['account.ex.phieu.thu.chi'].new({
                'SO_CHUNG_TU': pu.SO_CHUNG_TU,
                'NGAY_CHUNG_TU': pu.NGAY_CHUNG_TU,
                'NGAY_HACH_TOAN': pu.NGAY_HACH_TOAN,
                'TAI_KHOAN_CHI_GUI_ID': pu.TK_CHI_ID,
                'SO_TIEN_1': pu.TONG_TIEN_HANG,
                'currency_id': pu.currency_id,
                'TEN_TK_CHI': pu.CHI_NHANH_TK_CHI,
                'TEN_DOI_TUONG': pu.TEN_DOI_TUONG,
                'TAI_KHOAN_THU_NHAN_ID': pu.TK_NHAN_ID,
                'TEN_TK_NHAN': pu.CHI_NHANH_TK_NHAN,
                'TAI_NGAN_HANG_MAU_IN': pu.CHI_NHANH_TK_NHAN,
                'TEN_NOI_DUNG_TT': pu.LY_DO_CHI,
                'DOI_TUONG_ID': pu.DOI_TUONG_ID,
                'DIA_CHI': pu.DIA_CHI,
                'TEN_TK_NGAN_HANG': pu.TEN_TK_NGAN_HANG,
                'DIA_CHI_NGAN_HANG': pu.DIA_CHI_NGAN_HANG,
            })            
            records += [account]
        return records

    @api.multi
    def get_menu_id(self):
        if self.type == 'hang_hoa':
            return self.env.ref('menu.menu_mua_hang_chung_tu_hang_hoa_ex').id
        else:
            return self.env.ref('menu.menu_purchase_ex_chung_tu_mua_dich_vu').id

        return super(PURCHASE_DOCUMENT, self).get_menu_id()
                

