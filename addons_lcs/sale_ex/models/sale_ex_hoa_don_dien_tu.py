# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper, tools

class SALE_EX_HOA_DON_DIEN_TU_VIEW(models.Model):
    _name = 'sale.ex.hoa.don.dien.tu'
    _description = 'Hóa đơn điện tử'
    _auto = False
    _order = "NGAY_HOA_DON desc, MAU_SO_HD_ID desc, KY_HIEU_HD desc, SO_HOA_DON desc"

    CHUNG_TU_BAN_HANG = fields.Many2one('sale.document', string='Chứng từ BH', help='Chứng từ bán hàng')# trường này chỉ hiển thị trên form chứ không được dùng nếu dùng thì dùng trường  SALE_DOCUMENT_IDS
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    HOA_DON = fields.Selection([('BAN_HANG_HOA_DICH_VU_TRONG_NUOC', '1. Bán hàng hóa dịch vụ trong nước'), ('BAN_HANG_XUAT_KHAU', '2. Bán hàng xuất khẩu'), ('BAN_HANG_DAI_LY_BAN_DUNG_GIA', '3. Bán hàng đại lý bán đúng giá'), ('BAN_HANG_UY_THAC_XUAT_KHAU', ' 4. Bán hàng ủy thác xuất khẩu '), ], string='Hóa đơn', help='Hóa đơn',default='BAN_HANG_HOA_DICH_VU_TRONG_NUOC',required=True)
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    partner_bank_id = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='TK ngân hàng', help='Tài khoản ngân hàng')
    HINH_THUC_TT = fields.Selection([('TIEN_MAT', 'Tiền mặt'),('CHUYEN_KHOAN', 'Chuyển khoản'),('TM/CK', 'TM/CK') ], string='Hình thức TT', help='Hình thức thanh toán',default='TM/CK')
    NGUOI_MUA_HANG = fields.Char(string='Người mua hàng', help='Người mua hàng')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV bán hàng', help='Nhân viên bán hàng')
    DA_HACH_TOAN = fields.Boolean(string='Đã hạch toán', help='Đã hạch toán')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now)
    name = fields.Char(string='Số hóa đơn',related='SO_HOA_DON')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu',readonly = True)
    SOURCE_ID = fields.Reference(selection=[
        ('sale.document', 'Chứng từ bán hàng'),
        ('sale.ex.giam.gia.hang.ban', 'Chứng từ giảm giá hàng bán'),
        ('purchase.ex.tra.lai.hang.mua', 'Chứng từ trả lại hàng mua'),
        ], string='Lập từ')
    MA_HANG_ID  = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng',currency_field='currency_id')    
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng',currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',currency_field='currency_id')
    TONG_TIEN_HANG_QD = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng QĐ',currency_field='base_currency_id')    
    TIEN_CHIET_KHAU_QD = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu QĐ',currency_field='base_currency_id')
    TIEN_THUE_GTGT_QD = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng QĐ',currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QD = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán QĐ', currency_field='base_currency_id')
    IN_KEM_BANG_KE = fields.Boolean(string='In kèm bảng kê', help='In kèm bảng kê')
    SO = fields.Char(string='Số', help='Số')
    NGAY_BANG_KE = fields.Date(string='Ngày', help='Ngày')
    TEN_MAT_HANG_CHUNG = fields.Char(string='Tên mặt hàng chung', help='Tên mặt hàng chung')
    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng')
    NGAY_HOP_DONG = fields.Date(string='Ngày hợp đồng', help='Ngày hợp đồng')
    DIA_DIEM_NHAN_HANG = fields.Char(string='Địa điểm nhận hàng', help='Địa điểm nhận hàng')
    DIA_DIEM_GIAO_HANG = fields.Char(string='Địa điểm giao hàng', help='Địa điểm giao hàng')
    SO_VAN_DON = fields.Char(string='Số vận đơn', help='Số vận đơn')
    SO_CONTAINER = fields.Char(string='Số container', help='Số container')
    DV_VAN_CHUYEN = fields.Char(string='Đơn vị vận chuyển', help='Đơn vị vận chuyển')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',readonly=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_TEXT = fields.Char(string='Loại', help='Loại')
    DA_HACH_TOAN_TEXT = fields.Char(string='Đã hạch toán', help='Đã hạch toán')
    SALE_DOCUMENT_IDS = fields.Many2many('sale.document', 'sale_ex_document_invoice_rel', string='Chứng từ BH', help='Chứng từ bán hàng', domain=[('DA_LAP_HOA_DON', '!=', True)])
    LAP_KEM_HOA_DON = fields.Boolean(string='Lập kèm hóa đơn', help='Lập kèm hóa đơn')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')

    LOAI_CHUNG_TU_DIEU_CHINH = fields.Integer(string='Loại chứng điều chỉnh', help='AdjustRefType')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT * FROM sale_ex_hoa_don_ban_hang
            )""" % (self._table,))

class SaleExPhatHanhHoaDonWizard(models.TransientModel):
    _name = "sale.ex.phat.hanh.hoa.don.wizard"
    _description = "Phát hành hóa đơn điện tử"

    def _default_invoice_ids(self):
        HOA_DON_IDS = self._context.get('active_model') == 'sale.ex.hoa.don.ban.hang' and self._context.get('active_ids') or []
        return [
            (0, 0, 
				{'HOA_DON_ID': inv.id, 
				'SO_HOA_DON': inv.SO_HOA_DON,
				'NGAY_HOA_DON': inv.NGAY_HOA_DON,
				'TEN_DOI_TUONG': inv.TEN_KHACH_HANG,
				'EMAIL_DOI_TUONG': inv.DOI_TUONG_ID.EMAIL,
				})
            for inv in self.env['sale.ex.hoa.don.ban.hang'].browse(HOA_DON_IDS)
        ]

    HOA_DON_IDS = fields.One2many('sale.ex.phat.hanh.hoa.don.chi.tiet', 'wizard_id', string='Users', default=_default_invoice_ids)

    @api.multi
    def phat_hanh(self):
        self.ensure_one()
        self.HOA_DON_IDS.phat_hanh()
      #   if self.env.user in self.mapped('HOA_DON_IDS.HOA_DON_ID'):
      #       return {'type': 'ir.actions.client', 'tag': 'reload'}
        return {'type': 'ir.actions.act_window_close'}


class SaleExPhatHanhHoaDonChiTiet(models.TransientModel):
    _name = 'sale.ex.phat.hanh.hoa.don.chi.tiet'
    _description = 'Các hóa đơn để phát hành'

    wizard_id = fields.Many2one('sale.ex.phat.hanh.hoa.don.wizard', string='Wizard', required=True, ondelete='cascade')
    HOA_DON_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', string='User', required=True, ondelete='cascade')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', readonly=True)
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', readonly=True)
    DOI_TUONG_ID = fields.Char(string='Khách hàng', readonly=True)
    TEN_DOI_TUONG = fields.Char(string='Tên khách hàng', readonly=True)
    EMAIL_DOI_TUONG =  fields.Boolean(string='Email khách hàng')
    GUI_EMAIL_CHO_KHACH_HANG =  fields.Boolean(string='Gửi hóa đơn cho KH', default=True)

    @api.multi
    def phat_hanh(self):
        for line in self:
            line.HOA_DON_ID.phat_hanh_hoa_don(line.GUI_EMAIL_CHO_KHACH_HANG, line.EMAIL_DOI_TUONG)

    