# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class SALE_DOCUMENT_LINE(models.Model):
    _name = 'sale.document.line'
    _description = 'Chứng từ bán hàng chi tiết'
    _order = 'NGAY_HACH_TOAN desc,SALE_DOCUMENT_ID,id'
    
    # Updated 2019-04-26 by anhtuan: Remove để tránh confused với SALE_DOCUMENT_ID
    # CHUNG_TU_ID = fields.Many2one('sale.document', string='Chứng từ', help='Chứng từ')
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    name = fields.Char(string='Tên hàng', help='Tên hàng', related='MA_HANG_ID.TEN', )
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    TK_GIAM_GIA = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giảm giá', help='Tài khoản giảm giá')
    TK_TIEN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK tiền', help='Tài khoản tiền')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    # Nếu có SO_LUONG_YEU_CAU thì trường SO_LUONG là số lượng thực xuất
    SO_LUONG_YEU_CAU = fields.Float(string='SL yêu cầu', help='Số lượng yêu cầu',digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))#,  currency_field='currency_id') #Mạnh sửa bug2022: Đơn giá không cho phép nhập dấu phẩy
    THANH_TIEN = fields.Monetary(string='Thành tiền',  help='Thành tiền',store=True, currency_field='currency_id')
    TY_LE_CK = fields.Float(string='Tỉ lệ CK', help='Tỉ lệ chiết khấu ')
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế')
    THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Thuế GTGT', help='Thuế giá trị gia tăng')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', currency_field='currency_id')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế gtgt', help='Tài khoản thuế GTGT')
    GIA_TINH_THUE_XK = fields.Monetary(string='Giá tính thuế XK', help='Giá tính thuế xuất khẩu', currency_field='base_currency_id')
    THUE_XUAT_KHAU = fields.Float(string='thuế xuất khẩu', help='thuế xuất khẩu')
    TIEN_THUE_XUAT_KHAU = fields.Monetary(string='Tiền thuế xuất khẩu', help='Tiền thuế xuất khẩu', currency_field='currency_id')
    TK_THUE_XK_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế xuất khẩu', help='Tài khoản thuế xuất khẩu')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id')
    TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='Tài khoản chiết khấu') 
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Description')
    TK_GIA_VON_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giá vốn', help='Tài khoản giá vốn')
    TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho', help='Tài khoản kho')
    DON_GIA_VON = fields.Float(string='Đơn giá vốn', help='TK kho', readonly=True, digits=decimal_precision.get_precision('DON_GIA'))
    TIEN_VON = fields.Float(string='Tiền vốn', help='Đơn giá vốn', digits=decimal_precision.get_precision('VND'))
    SO_LO = fields.Char(string='Số lô', help='Tiền vốn')
    HAN_SU_DUNG = fields.Datetime(string='Hạn sử dụng', help='Số lô')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Hạn sử dụng')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Description')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn vị')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng thcp', help='Đơn đặt hàng')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Hợp đồng bán')
    SALE_DOCUMENT_ID = fields.Many2one('sale.document', string='Sale document', help='Sale document', ondelete='cascade')
    HOA_DON_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', string='Hóa đơn', help='Trong trường hợp chứng từ bán hàng có phát sinh hóa đơn, chứng từ chi tiết cũng là detail của hóa đơn.', ondelete='set null')
    PHIEU_XUAT_CHI_TIET_IDS = fields.Many2many('stock.ex.nhap.xuat.kho.chi.tiet', 'sale_ex_document_outward_detail_ref', string='Liên kết n-n tới xuất kho chi tiết')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_CK_QUY_DOI = fields.Monetary(string='Tiền CK quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỷ lệ chuyển đổi', help='Tỷ lệ chuyển đổi')
    DON_GIA_NGUYEN_TE_THEO_DVT_CHINH = fields.Float(string='Đơn giá nguyên tệ theo đvt chính', help='Đơn giá nguyên tệ theo đvt chính')
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo đvt chính', help='Số lượng theo đvt chính', compute='_compute_tinh_theo_dvt_chinh', store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo đvt chính', help='Đơn giá theo đvt chính', compute='_compute_tinh_theo_dvt_chinh', store=True)
    TI_LE_CHUYEN_DOI = fields.Float(string='Tỷ lệ chuyển đổi', help='Tỷ lệ chuyển đổi')
    DON_GIA_NGUYEN_TE = fields.Float(string='Đơn giá nguyên tệ', help='Đơn giá nguyên tệ')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='SALE_DOCUMENT_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    SO_CHUNG_TU_BAN_HANG = fields.Char(string='Số CT bán hàng', help='Số CT bán hàng')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='SALE_DOCUMENT_ID.TY_GIA', store=True)

    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='IsPromotion',default=False)
    DON_DAT_HANG_CHI_TIET_ID = fields.Many2one('account.ex.don.dat.hang.chi.tiet', string='Đơn đặt hàng chi tiết', help='SAOrderRefDetailID')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán' , related='SALE_DOCUMENT_ID.NGAY_HACH_TOAN', store=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ', related='SALE_DOCUMENT_ID.NGAY_CHUNG_TU')
    DOI_TUONG_ID = fields.Many2one(string='Khách hàng', help='Khách hàng', related='SALE_DOCUMENT_ID.DOI_TUONG_ID', store=True)
    sequence = fields.Integer()
    INDEX = fields.Integer(store=False,) 
    LAP_RAP_ID = fields.Many2one('stock.ex.lap.rap.thao.do', string='Lệnh lắp ráp', ondelete='set null')

    CHIEU_DAI = fields.Float(string='Chiều dài', digits=decimal_precision.get_precision('KICH_THUOC'))
    CHIEU_RONG = fields.Float(string='Chiều rộng', digits=decimal_precision.get_precision('KICH_THUOC'))
    CHIEU_CAO = fields.Float(string='Chiều cao', digits=decimal_precision.get_precision('KICH_THUOC'))
    BAN_KINH = fields.Float(string='Bán kính', digits=decimal_precision.get_precision('KICH_THUOC'))
    LUONG = fields.Float(string='Lượng', default=1)

    @api.model
    def default_get(self, fields):
        rec = super(SALE_DOCUMENT_LINE, self).default_get(fields)
        tk_gia_von = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
        if tk_gia_von:
            rec['TK_GIA_VON_ID'] = tk_gia_von.id
        return rec

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU','TIEN_THUE_XUAT_KHAU')
    def on_change_tinh_tien_quy_doi(self):
        for record in self:
            record.tinh_tien_quy_doi()

    def tinh_tien_quy_doi(self):        
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.SALE_DOCUMENT_ID.TY_GIA,0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.SALE_DOCUMENT_ID.TY_GIA,0)
        self.TIEN_CK_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.SALE_DOCUMENT_ID.TY_GIA,0)

    @api.onchange('TY_LE_CK','THANH_TIEN')
    def tinhtien(self):
        for record in self:
            record.TIEN_CHIET_KHAU = record.THANH_TIEN*(record.TY_LE_CK/100)
            
    
    @api.onchange('DON_GIA','SO_LUONG','SO_LUONG_YEU_CAU')
    def update_thanh_tien(self):
        self.THANH_TIEN = self.DON_GIA*self.get_so_luong()
    
    @api.onchange('DON_GIA_VON','SO_LUONG','SO_LUONG_YEU_CAU')
    def update_Tien_von(self):
        self.TIEN_VON = self.DON_GIA_VON*self.get_so_luong()

    @api.onchange('THUE_GTGT_ID','THANH_TIEN','TIEN_CHIET_KHAU')
    def update_tien_thue_gtgt(self):
        self.TIEN_THUE_GTGT = self.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT*(self.THANH_TIEN - self.TIEN_CHIET_KHAU)/100

    @api.onchange('GIA_TINH_THUE_XK','THUE_XUAT_KHAU')
    def tienthue(self):
        for record in self:
            record.TIEN_THUE_XUAT_KHAU = (record.GIA_TINH_THUE_XK * record.THUE_XUAT_KHAU)/100

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)

    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.TEN_HANG = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID
            if record.MA_HANG_ID.TEN:
                record.DIEN_GIAI_THUE ="Thuế GTGT - "+str(record.MA_HANG_ID.TEN)
            record.THUE_GTGT_ID = record.MA_HANG_ID.THUE_SUAT_GTGT_ID
            record.KHO_ID = record.MA_HANG_ID.KHO_NGAM_DINH_ID
            record.TK_KHO_ID = record.MA_HANG_ID.TAI_KHOAN_KHO_ID
            record.set_so_luong(1)

    @api.onchange('KHO_ID')
    def onchange_KHO_ID(self):
        for record in self:
            record.TK_KHO_ID = record.KHO_ID.TK_KHO_ID

    @api.depends('MA_HANG_ID','DVT_ID','SO_LUONG','DON_GIA')
    def _compute_tinh_theo_dvt_chinh(self):
        for record in self:
            if record.MA_HANG_ID:
                record.SO_LUONG_THEO_DVT_CHINH = record.MA_HANG_ID.compute_SO_LUONG_THEO_DVT_CHINH(record.SO_LUONG,record.DVT_ID.id)
                record.DON_GIA_THEO_DVT_CHINH = record.MA_HANG_ID.compute_DON_GIA_THEO_DVT_CHINH(record.DON_GIA,record.DVT_ID.id)
                
    # task 3513

    @api.onuichange('MA_HANG_ID')
    def thay_doi_ma_hang_cap_nhat_lai_toan_bo_cac_cot_dai_rong_cao_ban_kinh_luong(self):
        if self.MA_HANG_ID and self.SALE_DOCUMENT_ID.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH == True:
            self.CHIEU_DAI = 0
            self.CHIEU_RONG = 0
            self.CHIEU_CAO = 0
            self.BAN_KINH = 0
            self.LUONG = 1

    @api.onchange('CHIEU_DAI','CHIEU_RONG','CHIEU_CAO','BAN_KINH','LUONG')
    def thay_doi_chieu_dai_rong_cao_ban_kinh_de_tinh_so_luong(self):
        if self.MA_HANG_ID and self.SALE_DOCUMENT_ID.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH == True:
            sl = self.MA_HANG_ID.tinh_so_luong_theo_cong_thuc(self.CHIEU_DAI, self.CHIEU_RONG, self.CHIEU_CAO, self.BAN_KINH, self.LUONG)
            if sl is not None:
                self.set_so_luong(sl)

    # end task 3513

    # Để gọi hàm này, phải truyền các tham số sau vào context:
    # - SOURCE_ID
    # - SO_CHUNG_TU
    # - NGAY_CHUNG_TU
    def tao_lenh_lap_rap(self):
        self.ensure_one()
        if not self.LAP_RAP_ID and self.MA_HANG_ID.TINH_CHAT=='1' and self.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
            lap_rap_chi_tiet_ids = []
            for nvl in self.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                if nvl.MA_NGUYEN_VAT_LIEU_ID:
                    lap_rap_chi_tiet_ids += [(0,0,{
                    'MA_HANG_ID': nvl.MA_NGUYEN_VAT_LIEU_ID.id,
                    'TEN_HANG': nvl.TEN_NGUYEN_VAT_LIEU,
                    'KHO_ID': nvl.MA_NGUYEN_VAT_LIEU_ID.KHO_NGAM_DINH_ID.id,
                    'DVT_ID': nvl.DVT_ID.id,
                    'SO_LUONG': nvl.SO_LUONG * self.SO_LUONG,
                    # Lấy đơn giá/thành tiền quy đổi, do lệnh lắp ráp không có loại tiền
                    # Xem xét lại việc tính đơn giá và thành tiền, vì trường này là readonly
                    'DON_GIA': 0, #nvl.GIA_VON * self.SO_LUONG,
                    'THANH_TIEN': 0, #nvl.THANH_TIEN * self.SO_LUONG,
            })]
            lenh_lap_rap = {
                'SOURCE_ID': self._context.get('SOURCE_ID'),
                'LAP_RAP_THAO_DO': 'LAP_RAP',
                'DIEN_GIAI': 'Lập từ chứng từ bán hàng %s' % self._context.get('SO_CHUNG_TU'),
                'HANG_HOA_ID': self.MA_HANG_ID.id,
                'TEN_HANG_HOA': self.TEN_HANG,
                'NGAY': self._context.get('NGAY_CHUNG_TU'),
                'DVT_ID': self.DVT_ID.id,
                'SO_LUONG': self.SO_LUONG,
                # 'DON_GIA': self.DON_GIA, 
                # 'THANH_TIEN': self.THANH_TIEN_QUY_DOI,
                'SO': self.env['ir.sequence'].next_by_code('stock_ex_lap_rap_thao_do_SO'),
                'STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS': lap_rap_chi_tiet_ids,
            }
            lap_rap = self.env['stock.ex.lap.rap.thao.do'].create(lenh_lap_rap)
            # Cập nhật lại LAP_RAP_ID cho chứng từ bán hàng chi tiết
            self.LAP_RAP_ID = lap_rap.id

            lap_rap.tao_phieu_xuat_kho_nvl()
            lap_rap.tao_phieu_nhap_kho_thanh_pham()


    
    @api.model
    def create(self, values):   
        result = super(SALE_DOCUMENT_LINE, self).create(values)
        # Cập nhật lệnh lắp ráp
        if result.SALE_DOCUMENT_ID.LAP_KEM_LENH_LAP_RAP:
            result.with_context({
                'SOURCE_ID': (',').join([result.SALE_DOCUMENT_ID._name,str(result.SALE_DOCUMENT_ID.id)]),
                'SO_CHUNG_TU': result.SALE_DOCUMENT_ID.SO_CHUNG_TU,
                'NGAY_CHUNG_TU': result.SALE_DOCUMENT_ID.NGAY_CHUNG_TU,
            }).tao_lenh_lap_rap()
        return result

    @api.multi
    def write(self, values):    
        result = super(SALE_DOCUMENT_LINE, self).write(values)
        # Cập nhật lệnh lắp ráp gắn kèm
        for record in self:
            if record.SALE_DOCUMENT_ID.LAP_KEM_LENH_LAP_RAP:
                # Nếu thay đổi mã hàng thì phải re-new lệnh lắp ráp
                if 'MA_HANG_ID' in values:
                    record.LAP_RAP_ID.unlink()
                    record.with_context({
                        'SOURCE_ID': (',').join([record.SALE_DOCUMENT_ID._name,str(record.SALE_DOCUMENT_ID.id)]),
                        'SO_CHUNG_TU': record.SALE_DOCUMENT_ID.SO_CHUNG_TU,
                        'NGAY_CHUNG_TU': record.SALE_DOCUMENT_ID.NGAY_CHUNG_TU,
                    }).tao_lenh_lap_rap()
                else:
                    changes = {}
                    if 'SO_LUONG' in values:
                        changes['SO_LUONG'] = values.get('SO_LUONG')
                    if 'DVT_ID' in values:
                        changes['DVT_ID'] = values.get('DVT_ID')
                    if changes:
                        record.LAP_RAP_ID.write(changes)
        return result