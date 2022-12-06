# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round


class SALE_EX_TRA_LAI_HANG_BAN(models.Model):
    _name = 'sale.ex.tra.lai.hang.ban'
    _description = 'Chứng từ trả lại hàng bán'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    LAP_TU = fields.Selection([('CHUNG_TU_BAN_HANG', 'Chứng từ bán hàng'), ('CHUNG_TU_BAN_HANG_CHI_TIET', 'Chi tiết bán hàng'), ], string='Lập từ', help='Lập từ', store=False)
    CHUNG_TU_BAN_HANG = fields.Many2one('sale.document', string='Chứng từ BH', help='Chứng từ bán hàng')
    CHUNG_TU_BAN_HANG_CHI_TIET = fields.Many2many('sale.document.line', string='Chi tiết BH', help='Chứng từ bán hàng chi tiết', store=False)
    CHUNG_TU_HANG_BAN_BI_TRA_LAI = fields.Selection([('BAN_HANG_HOA_DICH_VU', '1.Bán hàng hóa, dịch vụ'), ('BAN_HANG_DAI_LY_BAN_DUNG_GIA', ' 2. Bán hàng đại lý bán đúng giá'), ('BAN_HANG_UY_THAC_XUAT_KHAU', '3. Bán hàng ủy thác xuất khẩu'), ], string=' ', help=' ',default='BAN_HANG_HOA_DICH_VU',required=True)
    KIEM_TRA_PHIEU_NHAP_KHO = fields.Boolean(string='Kiêm phiếu nhập kho', help='Kiêm phiếu nhập kho', default='True')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng', compute='tinh_tong_tien',store=True, currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng' ,compute='tinh_tong_tien',store=True , currency_field='currency_id')
    TONG_CHIET_KHAU = fields.Monetary(string='Tổng chiết khấu', help='Tổng chiết khấu',compute='tinh_tong_tien',store=True , currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',compute='tinh_tong_tien',store=True, currency_field='currency_id')
    TONG_TIEN_HANG_QĐ = fields.Monetary(string='', help='Tổng tiền hàng QĐ', compute='tinh_tong_tien',store=True,  currency_field='base_currency_id')
    TIEN_THUE_GTGT_QĐ = fields.Monetary(string='', help='Tiền thuế giá trị gia tăng QĐ' ,compute='tinh_tong_tien',store=True ,  currency_field='base_currency_id')
    TONG_CHIET_KHAU_QĐ = fields.Monetary(string='', help='Tổng chiết khấu QĐ',compute='tinh_tong_tien',store=True ,  currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QĐ = fields.Monetary(string='', help='Tổng tiền thanh toán QĐ',compute='tinh_tong_tien',store=True,  currency_field='base_currency_id')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV bán hàng', help='Nhân viên bán hàng')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán' , required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ', default=fields.Datetime.now , required=True)
    SO_CHUNG_TU_GIAM_TRU_CONG_NO = fields.Char(string='Số chứng từ ', help='Số chứng từ giảm trừ công nợ', auto_num='purchase_ex_tra_lai_hang_ban_SO_CHUNG_TU_GIAM_TRU_CONG_NO')
    NGUOI_GIAO_HANG = fields.Char(string='Người giao hàng', help='Người giao hàng')
    KEM_THEO = fields.Char(string='Kèm theo CT gốc', help='Kèm theo chứng từ gốc ')

    KEM_THEO_PN = fields.Char(string='Kèm theo CT gốc', help='Kèm theo chứng từ gốc ')
    SO_PHIEU_NHAP = fields.Char(string='Số phiếu nhập', help='Số phiếu nhập', auto_num='stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_NHAP_KHO')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now ,required=True)
    LY_DO_CHI = fields.Char(string='Lý do chi', help='Lý do chi',related='DIEN_GIAI',store=True)
    NGUOI_NHAN = fields.Char(string='Người nhận', help='Người nhận')
    SO_CHUNG_TU_PHIEU_CHI = fields.Char(string='Số chứng từ', help='Số chứng từ phiếu chi', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_PHIEU_CHI')
    name = fields.Char(string='Name',related='SO_CHUNG_TU', )
    # CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    DON_VI_GIAO_DAI_LY_ID = fields.Many2one('res.partner', string='Đơn vị giao đại lý', help='Đơn vị giao đại lý')
    TEN_DON_VI_GIAO_DAI_LY = fields.Char(string='Tên đơn vị giao đại lý', help='Tên đơn vị giao đại lý') 
    DON_VI_UY_THAC_ID = fields.Many2one('res.partner', string='Đơn vị ủy thác', help='Đơn vị ủy thác',related='DON_VI_GIAO_DAI_LY_ID',store=True)
    TEN_DON_VI_UY_THAC = fields.Char(string='Tên đơn vị ủy thác', help='Tên đơn vị ủy thác',related='TEN_DON_VI_GIAO_DAI_LY',store=True)    
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null') 
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', compute='_compute_SO_CHUNG_TU',store=True)
    SO_BAN_HANG_ID = fields.Many2one('so.ban.hang', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    # Thêm một trường là Loại chứng từ 
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',store=True,compute='set_loai_chung_tu_tra_lai_hang_ban') 
    ID_CHUNG_TU_GOC = fields.Many2one('sale.document', string='ID chứng từ bán hàng', help='ID chứng từ bán hàng')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    TRA_LAI_HANG_BAN_CHI_TIET_IDS = fields.One2many('sale.ex.tra.lai.hang.ban.chi.tiet', 'TRA_LAI_HANG_BAN_ID', string='Chi tiết trả lại hàng bán', copy=True)
    PHIEU_NHAP_ID = fields.Many2one('stock.ex.nhap.xuat.kho', string='Phiếu nhập kho')
    PHIEU_CHI_ID = fields.Many2one('account.ex.phieu.thu.chi', string='Phiếu chi tiền')
    LOAI_CHUNG_TU_TEXT = fields.Char(string='Loại chứng từ', help='Loại chứng từ',compute='set_loai_chung_tu_text',store=True)
    HOA_DON_REF_ID = fields.Char(help='Ref ID của hóa đơn được import')

    HOA_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Hóa đơn mua hàng',help ='PUInvoiceRefID')

    # _sql_constraints = [
	# ('SO_CHUNG_TU_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
	# ]
    @api.onchange('CHUNG_TU_BAN_HANG_CHI_TIET')
    def _onchange_CHUNG_TU_BAN_HANG_CHI_TIET(self):
        ctbhct_ids = [line.BAN_HANG_CHI_TIET_ID.id for line in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS if line.BAN_HANG_CHI_TIET_ID]
        default = self.TRA_LAI_HANG_BAN_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
        for line in self.CHUNG_TU_BAN_HANG_CHI_TIET:
            if self.DOI_TUONG_ID and line.SALE_DOCUMENT_ID.DOI_TUONG_ID.id != self.DOI_TUONG_ID.id:
                raise ValidationError("Khách hàng trong các chứng từ chi tiết đã chọn không đồng nhất. Vui lòng chọn lại!")
            elif not self.DOI_TUONG_ID:
                self.DOI_TUONG_ID = line.SALE_DOCUMENT_ID.DOI_TUONG_ID.id
                self.TEN_KHACH_HANG = line.SALE_DOCUMENT_ID.DOI_TUONG_ID.HO_VA_TEN
            if line.id not in ctbhct_ids:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': line.MA_HANG_ID,
                    'TEN_HANG': line.TEN_HANG,
                    'DVT_ID': line.DVT_ID.id,
                    'SO_LUONG':line.SO_LUONG,
                    'DON_GIA':line.THANH_TIEN_QUY_DOI / ((line.SO_LUONG * self.TY_GIA) or 1),
                    'THANH_TIEN':line.THANH_TIEN_QUY_DOI / (self.TY_GIA or 1),
                    'KHO_ID': line.KHO_ID.id,
                    'TK_KHO_ID': line.TK_KHO_ID.id,
                    'TK_GIA_VON_ID': line.TK_GIA_VON_ID.id,
                    'THANH_TIEN_QUY_DOI':line.THANH_TIEN_QUY_DOI,
                    'TY_LE_CK_PHAN_TRAM':line.TY_LE_CK,
                    'TIEN_CHIET_KHAU':line.TIEN_CK_QUY_DOI / (self.TY_GIA or 1),
                    'TIEN_CHIET_KHAU_QUY_DOI':line.TIEN_CK_QUY_DOI,
                    'SO_CHUNG_TU_ID': line.SALE_DOCUMENT_ID.id,
                    'DIEN_GIAI_THUE':line.DIEN_GIAI_THUE,
                    'PHAN_TRAM_THUE_GTGT_ID': line.THUE_GTGT_ID.id,
                    'TIEN_THUE_GTGT':line.TIEN_THUE_GTGT_QUY_DOI / (self.TY_GIA or 1),
                    'TIEN_THUE_GTGT_QUY_DOI': line.TIEN_THUE_GTGT_QUY_DOI,
                    'DON_DAT_HANG_CHI_TIET_ID' : line.DON_DAT_HANG_CHI_TIET_ID.id,
                    'DON_DAT_HANG_ID' : line.DON_DAT_HANG_ID.id,
                    'BAN_HANG_CHI_TIET_ID': line.id,
                })
                self.TRA_LAI_HANG_BAN_CHI_TIET_IDS += self.env['sale.ex.tra.lai.hang.ban.chi.tiet'].new(new_data)
    
    @api.onuichange('CHUNG_TU_BAN_HANG_CHI_TIET')
    def _onchange_CHUNG_TU_BAN_HANG_CHI_TIET1(self):
        self.CHUNG_TU_BAN_HANG_CHI_TIET = []

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ bán hàng
    def lay_du_lieu_chung_tu_ban_hang(self, args):
        new_line =[[5]]
        chung_tu_ban_hang_id = args.get('chung_tu_ban_hang_id')
        thong_tin_chung_tu_master = self.env['sale.document'].search([('id', '=', chung_tu_ban_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        ten_khach_hang = thong_tin_chung_tu_master['TEN_KHACH_HANG']
        danh_sach_chung_tu_ban_hang = self.env['sale.document.line'].search([('SALE_DOCUMENT_ID', '=', chung_tu_ban_hang_id)])
        if danh_sach_chung_tu_ban_hang:
            default = self.TRA_LAI_HANG_BAN_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
            for ct_bh in danh_sach_chung_tu_ban_hang:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [ct_bh['MA_HANG_ID'].id,ct_bh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_bh['TEN_HANG'],
                    'DVT_ID': [ct_bh['DVT_ID'].id,ct_bh['DVT_ID'].name],
                    'SO_LUONG': ct_bh['SO_LUONG'],
                    'DON_GIA': ct_bh['DON_GIA'],
                    'THANH_TIEN': ct_bh['THANH_TIEN'],
                    'KHO_ID': [ct_bh['KHO_ID'].id,ct_bh['KHO_ID'].MA_KHO],
                    'TK_KHO_ID': [ct_bh['TK_KHO_ID'].id,ct_bh['TK_KHO_ID'].SO_TAI_KHOAN],
                    'TK_GIA_VON_ID': [ct_bh['TK_GIA_VON_ID'].id,ct_bh['TK_GIA_VON_ID'].SO_TAI_KHOAN],
                    'THANH_TIEN_QUY_DOI': ct_bh['THANH_TIEN_QUY_DOI'],
                    'TY_LE_CK_PHAN_TRAM': ct_bh['TY_LE_CK'],
                    'TIEN_CHIET_KHAU': ct_bh['TIEN_CHIET_KHAU'],
                    'TIEN_CHIET_KHAU_QUY_DOI': ct_bh['TIEN_CK_QUY_DOI'],
                    'SO_CHUNG_TU_ID':[chung_tu_ban_hang_id,args.get('chung_tu_ban_hang_name')],
                    'DIEN_GIAI_THUE': ct_bh['DIEN_GIAI_THUE'],
                    'PHAN_TRAM_THUE_GTGT_ID': [ct_bh['THUE_GTGT_ID'].id,ct_bh['THUE_GTGT_ID'].name],
                    'TIEN_THUE_GTGT': ct_bh['TIEN_THUE_GTGT'],
                    'TIEN_THUE_GTGT_QUY_DOI': ct_bh['TIEN_THUE_GTGT_QUY_DOI'],
                    'DON_DAT_HANG_CHI_TIET_ID' : ct_bh.DON_DAT_HANG_CHI_TIET_ID.id,
                    'DON_DAT_HANG_ID' : ct_bh.DON_DAT_HANG_ID.id,
                    'BAN_HANG_CHI_TIET_ID': [ct_bh.id,ct_bh.name],
                    })
                new_line += [(0,0,new_data)]
        return {'TRA_LAI_HANG_BAN_CHI_TIET_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                'TEN_KHACH_HANG': ten_khach_hang,
                'currency_id': [thong_tin_chung_tu_master.currency_id.id, thong_tin_chung_tu_master.currency_id.name]}

    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU
			
    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            if record.selection_chung_tu_ban_hang == 'tra_lai_tien_mat':
                record.validate_unique_thu_chi_tien(record.SO_CHUNG_TU_PHIEU_CHI)

    @api.model
    def create(self, vals):
        result = super(SALE_EX_TRA_LAI_HANG_BAN, self).create(vals)
        result.validate_unique_so_chung_tu()
        result.validate_thu_chi_tien()
        self.create_references(result)
        if self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
            self.up_date_don_dat_hang()
        return result
    
    def create_references(self, return_doc):
        # Kiêm phiếu nhập kho
        if return_doc.KIEM_TRA_PHIEU_NHAP_KHO:
            nhap_kho_chi_tiet_ids = []
            for line in return_doc.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                nhap_kho_chi_tiet_ids += [(0,0,{
                    'MA_HANG_ID': line.MA_HANG_ID.id,
                    'TEN_HANG': line.TEN_HANG,
                    'TK_NO_ID': line.TK_KHO_ID.id,
                    'TK_CO_ID': line.TK_GIA_VON_ID.id,
                    'KHO_ID': line.KHO_ID.id,
                    'DVT_ID': line.DVT_ID.id,
                    'SO_LUONG': line.SO_LUONG,
                    'DON_GIA': line.DON_GIA,
                    'THANH_TIEN': line.THANH_TIEN,
                    'TRA_LAI_HANG_BAN_CHI_TIET_IDS': [(4, line.id)]
                })]
            vals = {
                'type': 'NHAP_KHO',
                'SO_CHUNG_TU': return_doc.SO_PHIEU_NHAP,
                'NGAY_CHUNG_TU': return_doc.NGAY_CHUNG_TU,
                'NGAY_HACH_TOAN': return_doc.NGAY_HACH_TOAN,
                'DOI_TUONG_ID': return_doc.DOI_TUONG_ID.id,
                'TEN_NGUOI_GIAO_HANG': return_doc.TEN_KHACH_HANG,
                'LOAI_CHUNG_TU': return_doc.LOAI_CHUNG_TU,
                'SOURCE_ID': self._name + ',' + str(return_doc.id),
                'CHI_TIET_IDS': nhap_kho_chi_tiet_ids,
            }
            phieu_nhap = self.env['stock.ex.nhap.xuat.kho'].create(vals)
            return_doc.TRA_LAI_HANG_BAN_CHI_TIET_IDS.write({'PHIEU_NHAP_ID': phieu_nhap.id})
        # Luôn lập kèm hóa đơn
        vals = {
            'SO_HOA_DON': return_doc.SO_HOA_DON,
            'NGAY_HOA_DON': return_doc.NGAY_HOA_DON,
            'KY_HIEU_HD': return_doc.KY_HIEU_HD,
            'MAU_SO_HD_ID': return_doc.MAU_SO_HD_ID.id,
            'DOI_TUONG_ID': return_doc.DOI_TUONG_ID.id,
            'TEN_NHA_CUNG_CAP': return_doc.TEN_KHACH_HANG,
            'LOAI_CHUNG_TU': 3403,
            'NHAN_HOA_DON' : True,
            'SOURCE_ID': self._name + ',' + str(return_doc.id),
        }
        hoa_don = self.env['purchase.ex.hoa.don.mua.hang'].create(vals)
        return_doc.TRA_LAI_HANG_BAN_CHI_TIET_IDS.write({'HOA_DON_ID': hoa_don.id})

    @api.multi
    def write(self, values):
        result = super(SALE_EX_TRA_LAI_HANG_BAN, self).write(values)
        if helper.List.element_in_dict(['selection_chung_tu_ban_hang','SO_CHUNG_TU_PHIEU_CHI'], values):
            self.validate_thu_chi_tien()
        if helper.List.element_in_dict(['selection_chung_tu_ban_hang','SO_CHUNG_TU_GIAM_TRU_CONG_NO','SO_CHUNG_TU_PHIEU_CHI'], values):
            self.validate_unique_so_chung_tu()
        self.update_references(values)
        for record in self:
            if record.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                self.up_date_don_dat_hang()
        return result
    
    def update_references(self, values):
        # Cập nhật phiếu nhập kho/hóa đơn gắn kèm nếu có
        hoa_don_vals = helper.Obj.get_sub_dict(values, ('SO_HOA_DON','NGAY_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID','DOI_TUONG_ID','SOURCE_ID','HINH_THUC_TT'))
        phieu_nhap_vals = helper.Obj.get_sub_dict(values, ('type','SO_CHUNG_TU','NGAY_CHUNG_TU','NGAY_HACH_TOAN','DOI_TUONG_ID','LOAI_CHUNG_TU','SOURCE_ID'))
        if 'TEN_KHACH_HANG' in values:
            hoa_don_vals['TEN_NHA_CUNG_CAP'] = values.get('TEN_KHACH_HANG')
            phieu_nhap_vals['TEN_NGUOI_GIAO_HANG'] = values.get('TEN_KHACH_HANG')
        for record in self: 
            hoa_don_vals['LOAI_CHUNG_TU'] = 3403
            record.find_reference('purchase.ex.hoa.don.mua.hang').write(hoa_don_vals)
            # Update phiếu xuất và phiếu xuất chi tiết
            phieu_xuat = record.find_reference('stock.ex.nhap.xuat.kho')
            if 'CHI_TIET_IDS' in values:
                phieu_xuat.CHI_TIET_IDS.unlink()
                nhap_kho_chi_tiet_ids = []
                for line in record.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                    nhap_kho_chi_tiet_ids += [(0,0,{
                        'MA_HANG_ID': line.MA_HANG_ID.id,
                        'TEN_HANG': line.TEN_HANG,
                        'TK_NO_ID': line.TK_KHO_ID.id,
                        'TK_CO_ID': line.TK_GIA_VON_ID.id,
                        'KHO_ID': line.KHO_ID.id,
                        'DVT_ID': line.DVT_ID.id,
                        'SO_LUONG': line.SO_LUONG,
                        'DON_GIA': line.DON_GIA,
                        'THANH_TIEN': line.THANH_TIEN,
                        'TRA_LAI_HANG_BAN_CHI_TIET_IDS': [(4, line.id)]
                    })]
                phieu_nhap_vals['CHI_TIET_IDS'] = nhap_kho_chi_tiet_ids
            phieu_xuat.write(phieu_nhap_vals)

    @api.multi
    def unlink(self):
        arr_don_dat_hang = []
        for record in self:
            record.find_reference('purchase.ex.hoa.don.mua.hang').unlink()
            record.find_reference('stock.ex.nhap.xuat.kho').unlink()
            if record.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                for chi_tiet in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                    if chi_tiet.DON_DAT_HANG_ID:
                        arr_don_dat_hang.append(chi_tiet.DON_DAT_HANG_ID.id)
        result = super(SALE_EX_TRA_LAI_HANG_BAN, self).unlink()
        if arr_don_dat_hang:
            for line in arr_don_dat_hang:
                self.update_so_luong_don_dat_hang(line)
                self.update_trang_thai_don_dat_hang(line)
        return result

    def up_date_don_dat_hang(self):
        arr_don_dat_hang = []
        for chi_tiet in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                if chi_tiet.DON_DAT_HANG_ID:
                    if chi_tiet.DON_DAT_HANG_ID not in arr_don_dat_hang:
                        arr_don_dat_hang.append(chi_tiet.DON_DAT_HANG_ID.id)
        if arr_don_dat_hang:
            for line in arr_don_dat_hang:
                self.update_so_luong_don_dat_hang(line)
                self.update_trang_thai_don_dat_hang(line)

    @api.depends('selection_chung_tu_ban_hang')
    def _compute_SO_CHUNG_TU(self):
        for record in self:
            if record.selection_chung_tu_ban_hang == 'tra_lai_tien_mat':
                record.SO_CHUNG_TU = record.SO_CHUNG_TU_PHIEU_CHI
            else:
                record.SO_CHUNG_TU = record.SO_CHUNG_TU_GIAM_TRU_CONG_NO

    selection_chung_tu_ban_hang = fields.Selection([
        ('giam_tru_cong_no', 'Giảm trừ công nợ'),
        ('tra_lai_tien_mat','Trả lại tiền mặt'),
        ], default='tra_lai_tien_mat',string=" ")

    chi_tiet = fields.Selection([
        ('hang_tien', 'Hàng tiền'),
        ('thue','Thuế'),
        ('gia_von','Giá vốn'),
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')


    # Bổ sung hàm depend để lấy loại chứng từ 
    @api.depends('CHUNG_TU_HANG_BAN_BI_TRA_LAI','selection_chung_tu_ban_hang')
    def set_loai_chung_tu_tra_lai_hang_ban(self):
        for record in self:
            if record.selection_chung_tu_ban_hang=='giam_tru_cong_no':
                if record.CHUNG_TU_HANG_BAN_BI_TRA_LAI =='BAN_HANG_HOA_DICH_VU':
                    record.LOAI_CHUNG_TU = 3540
                elif record.CHUNG_TU_HANG_BAN_BI_TRA_LAI =='BAN_HANG_DAI_LY_BAN_DUNG_GIA':
                    record.LOAI_CHUNG_TU = 3542
                else: 
                    record.LOAI_CHUNG_TU = 3544
            elif record.selection_chung_tu_ban_hang=='tra_lai_tien_mat':
                if record.CHUNG_TU_HANG_BAN_BI_TRA_LAI =='BAN_HANG_HOA_DICH_VU':
                    record.LOAI_CHUNG_TU = 3541
                elif record.CHUNG_TU_HANG_BAN_BI_TRA_LAI =='BAN_HANG_DAI_LY_BAN_DUNG_GIA':
                    record.LOAI_CHUNG_TU = 3543
                else: 
                    record.LOAI_CHUNG_TU = 3545


    @api.depends('LOAI_CHUNG_TU')
    def set_loai_chung_tu_text(self):
        for record in self:
            loai_chung_tu_text =''
            ref_type = record.env['danh.muc.reftype'].search([('REFTYPE', '=', record.LOAI_CHUNG_TU)],limit=1)
            if ref_type:
                loai_chung_tu_text = ref_type.REFTYPENAME
            record.LOAI_CHUNG_TU_TEXT = loai_chung_tu_text

    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False
        
    @api.onchange('DOI_TUONG_ID')
    def laythongtinkhachhang(self):
        self.TEN_KHACH_HANG = self.DOI_TUONG_ID.HO_VA_TEN
        self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
        self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
        self.NHAN_VIEN_ID = self.DOI_TUONG_ID.NHAN_VIEN_ID.id
        if self.DOI_TUONG_ID.company_type=='person':
            self.NGUOI_GIAO_HANG = self.DOI_TUONG_ID.HO_VA_TEN
            self.NGUOI_NHAN = self.DOI_TUONG_ID.HO_VA_TEN
        else:
            self.NGUOI_GIAO_HANG =''
            self.NGUOI_NHAN =''
        # Reset các chứng từ chi tiết có đối tượng
        for line in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
            if line.BAN_HANG_CHI_TIET_ID and line.BAN_HANG_CHI_TIET_ID.DOI_TUONG_ID.id != self.DOI_TUONG_ID.id:
                self.TRA_LAI_HANG_BAN_CHI_TIET_IDS = []
                break

    @api.onchange('DON_VI_GIAO_DAI_LY_ID')
    def laythongtindonvigiaodaily(self):
        self.TEN_DON_VI_GIAO_DAI_LY = self.DON_VI_GIAO_DAI_LY_ID.HO_VA_TEN
    
    @api.onchange('DON_VI_UY_THAC_ID')
    def laythongtindonvigiaodaily1(self):
        self.TEN_DON_VI_UY_THAC = self.DON_VI_UY_THAC_ID.HO_VA_TEN



    @api.depends('TRA_LAI_HANG_BAN_CHI_TIET_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien_hang = tong_tien_thue_gtgt = tong_tien_chiet_khau = tong_tien_thanh_toan =0.0
            tong_tien_hang_qd = tong_tien_thue_gtgt_qd  = tong_tien_chiet_khau_qd = tong_tien_thanh_toan_qd =0.0
            for line in order.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                tong_tien_hang += line.THANH_TIEN
                tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
                tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt - tong_tien_chiet_khau

                tong_tien_hang_qd += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qd += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_chiet_khau_qd += line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_thanh_toan_qd = tong_tien_hang_qd + tong_tien_thue_gtgt_qd - tong_tien_chiet_khau_qd
            order.update({
                'TONG_TIEN_HANG': tong_tien_hang,
                'TIEN_THUE_GTGT': tong_tien_thue_gtgt,
                'TONG_CHIET_KHAU': tong_tien_chiet_khau,
                'TONG_TIEN_THANH_TOAN': tong_tien_thanh_toan,

                'TONG_TIEN_HANG_QĐ': tong_tien_hang_qd,
                'TIEN_THUE_GTGT_QĐ': tong_tien_thue_gtgt_qd,
                'TONG_CHIET_KHAU_QĐ': tong_tien_chiet_khau_qd,
                'TONG_TIEN_THANH_TOAN_QĐ': tong_tien_thanh_toan_qd,
            })
            
    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_ban_hang()
            record.ghi_so_cong_no()
            hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
            if hoa_don:
                hoa_don.ghi_so_thue_qua_chung_tu_tra_lai_hb()
            phieu_nhap = record.find_reference('stock.ex.nhap.xuat.kho')
            if phieu_nhap:
                phieu_nhap.action_ghi_so()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU': self.LOAI_CHUNG_TU,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.TEN_HANG,
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'SO_HOA_DON' : self.SO_HOA_DON,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.THANH_TIEN,
                'GHI_NO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'NGUOI_LIEN_HE' : self.NGUOI_NHAN,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.THANH_TIEN,
                'GHI_CO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            if line.TK_CHIET_KHAU and (line.TIEN_CHIET_KHAU !=0 or line.TIEN_CHIET_KHAU_QUY_DOI != 0):
                # Ghi sổ tk chiết khấu
                data_chiet_khau = data_ghi_no.copy()
                data_chiet_khau.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CHIET_KHAU.id,
                    'GHI_NO' : line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
					'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_chiet_khau)]
                data_chiet_khau2 = data_chiet_khau.copy()
                data_chiet_khau2.update({
                    'TAI_KHOAN_ID' : line.TK_CHIET_KHAU.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
					'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_chiet_khau2)]
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 or line.TIEN_THUE_GTGT_QUY_DOI != 0):
                # Ghi sổ thuế gtgt
                data_thue_gtgt = data_ghi_no.copy()
                data_thue_gtgt.update({
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    'TAI_KHOAN_ID' : line.TK_THUE_GTGT_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : line.TIEN_THUE_GTGT_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
					'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_thue_gtgt)]

                data_thue_gtgt2 = data_thue_gtgt.copy()
                data_thue_gtgt2.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.TIEN_THUE_GTGT_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
					'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_thue_gtgt2)]
            thu_tu += 1

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
        for line in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU_CTBH': self._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.TEN_HANG,
                'SO_TIEN_TRA_LAI': line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_TRA_LAI_NGUYEN_TE': line.THANH_TIEN,
                'SO_HOA_DON' : self.SO_HOA_DON,
                'TK_CHIET_KHAU_ID' : line.TK_CHIET_KHAU.id,
                'DVT_ID' : line.DVT_ID.id,
                'PHAN_TRAM_CHIET_KHAU' : line.TY_LE_CK_PHAN_TRAM,
                'SO_TIEN_CHIET_KHAU' : -1*line.TIEN_CHIET_KHAU_QUY_DOI,
                'SO_TIEN_CHIET_KHAU_NGUYEN_TE' : -1*line.TIEN_CHIET_KHAU,
                'SO_LUONG_TRA_LAI' : line.SO_LUONG,
                'PHAN_TRAM_THUE_VAT' : line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT' : -1*line.TIEN_THUE_GTGT_QUY_DOI,
                'SO_TIEN_VAT_NGUYEN_TE' : -1*line.TIEN_THUE_GTGT,
                'TAI_KHOAN_VAT_ID' : line.TK_THUE_GTGT_ID.id,
                'DON_GIA' : line.DON_GIA*self.TY_GIA,
                'SO_LUONG' : 0,
                'TK_NO_ID' : line.TK_CO_ID.id,
                'TK_CO_ID' : line.TK_NO_ID.id,
                'MA_HOP_DONG' : line.HOP_DONG_BAN_ID.SO_HOP_DONG,
                'TEN_HOP_DONG' : line.HOP_DONG_BAN_ID.TRICH_YEU,
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

    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'SO_HOP_DONG' : line.HOP_DONG_BAN_ID.SO_HOP_DONG,
                'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
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
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT !=0 and line.TIEN_THUE_GTGT_QUY_DOI !=0):
                if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_THUE_GTGT_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'DIEN_GIAI' : 'Thuế giá trị gia tăng',
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
                        'LOAI_HACH_TOAN' : '2',
                        'DIEN_GIAI' : 'Thuế giá trị gia tăng',
                    })
                    line_ids += [(0,0,data_ghi_co)]

            if line.TK_CHIET_KHAU and (line.TIEN_CHIET_KHAU !=0 and line.TIEN_CHIET_KHAU_QUY_DOI !=0):
                if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_CO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CHIET_KHAU.id,
                        'GHI_NO': line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_ghi_no)]
                if line.TK_CHIET_KHAU.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_CHIET_KHAU.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
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
            hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
            if hoa_don:
                hoa_don.action_bo_ghi_so()
            phieu_nhap = record.find_reference('stock.ex.nhap.xuat.kho')
            if phieu_nhap:
                phieu_nhap.action_bo_ghi_so()
        return super(SALE_EX_TRA_LAI_HANG_BAN, self).action_bo_ghi_so()



    def update_so_luong_don_dat_hang(self,id_don_dat_hang):
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