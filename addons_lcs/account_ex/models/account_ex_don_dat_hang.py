# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class ACCOUNT_EX_DON_DAT_HANG(models.Model):
    _name = 'account.ex.don.dat.hang'
    _description = 'Đơn đặt hàng'
    _inherit = ['mail.thread']
    _order = "NGAY_DON_HANG desc, SO_DON_HANG desc"

    BAO_GIA_ID = fields.Many2one('sale.ex.bao.gia', string='Báo giá', help='Số báo giá')
    KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng', track_visibility='onchange')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    NGUOI_NHAN_HANG = fields.Char(string='Ng. nhận hàng', help='Người nhận hàng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NV_BAN_HANG_ID = fields.Many2one('res.partner', string='Nv bán hàng', help='Nv bán hàng', default=lambda self: self.env.user.partner_id.id)
    DIEU_KHOAN_TT_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản TT', help='Điều khoản tt')
    SO_NGAY_DUOC_NO = fields.Integer(string='Số ngày nợ', help='Số ngày được nợ')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng',default=fields.Datetime.now)
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng', auto_num='account_ex_don_dat_hang_SO_DON_HANG')
    TINH_TRANG = fields.Selection([('0', 'Chưa thực hiện'), ('1', 'Đang thực hiện'), ('2', 'Hoàn thành'), ('3', ' Hủy bỏ'), ], string='Tình trạng', help='Tình trạng',default='0',required="True", track_visibility='onchange')
    NGAY_GIAO_HANG = fields.Date(string='Ngày giao hàng', help='Ngày giao hàng')
    TINH_GIA_THANH = fields.Boolean(string='Tính giá thành', help='Tính giá thành')
    
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    DIA_DIEM_GIAO_HANG = fields.Char(string='Địa điểm giao hàng', help='Địa điểm giao hàng')
    DIEU_KHOAN_KHAC = fields.Char(string='Điều khoản khác', help='Điều khoản khác')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng',compute='tinh_tong_tien',store=True, currency_field='currency_id')
    TONG_TIEN_HANG_QUY_DOI = fields.Monetary(string='Tổng tiền hàng quy đổi', help='Tổng tiền hàng quy đổi',compute='tinh_tong_tien',store=True, currency_field='base_currency_id')
    TONG_TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tổng tiền thuế gtgt',compute='tinh_tong_tien',store=True, currency_field='currency_id')
    TONG_TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tổng tiền thuế gtgt quy đổi',compute='tinh_tong_tien', help='Tổng tiền thuế gtgt quy đổi',store=True, currency_field='base_currency_id')
    # Updated 2019-08-19 by anhtuan: Tiền chiết khấu cũng phải là trường compute
    TONG_CHIET_KHAU = fields.Monetary(string='Tổng chiết khấu', help='Tổng chiết khấu', currency_field='currency_id',compute='tinh_tong_tien',store=True)
    TONG_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tổng chiết khấu quy đổi', help='Tổng chiết khấu quy đổi', currency_field='base_currency_id',compute='tinh_tong_tien',store=True)
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',compute='tinh_tong_tien',store=True, currency_field='currency_id', track_visibility='onchange')
    TONG_TIEN_THANH_TOAN_QUY_DOI = fields.Monetary(string='Tổng tiền thanh toán quy đổi', help='Tổng tiền thanh toán quy đổi',compute='tinh_tong_tien',store=True, currency_field='base_currency_id')
    name = fields.Char(string='Name' ,related="SO_DON_HANG")
    
    ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS = fields.One2many('account.ex.don.dat.hang.chi.tiet', 'DON_DAT_HANG_CHI_TIET_ID', string='Đơn đặt hàng chi tiết', copy=True)
    PHAN_TRAM_THUE = fields.Float(string='phần trăm thuế GTGT', help='phần trăm thuế GTGT',compute='tinh_tong_tien',strore=True,digits=decimal_precision.get_precision('Product Price'))

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    # currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    # LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    GIA_TRI_DA_XUAT_HD = fields.Float(string='Giá trị đã xuất hóa đơn', help='Giá trị đã xuất hóa đơn')


    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    
    DOI_TUONG_ID = fields.Many2one('res.partner', related='KHACH_HANG_ID', )
    date_order = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    state = fields.Char(string='Trạng thái', help='Trạng thái')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    CHECK_TINH_GIA_THANH = fields.Boolean(string='Check tính giá thành', help='Check tính giá thành')
    CHUNG_TU_BAN_HANG_ID = fields.Many2one('sale.document', string='Chứng từ bán hàng', help='Chứng từ bán hàng tạo từ đơn đặt hàng này', ondelete='set null')

    _sql_constraints = [
	('SO_DON_HANG_DDH_uniq', 'unique ("SO_DON_HANG")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),

    ]

    CHON_CHI_PHI_JSON = fields.Text(store=False)

    def kiem_tra_ton_kho_toi_thieu(self):
        self.ensure_one()
        error = ''
        for line in self.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
            if line.MA_HANG_ID:
                ton_kho_toi_thieu = line.MA_HANG_ID.SO_LUONG_TON_TOI_THIEU
                if ton_kho_toi_thieu > 0:
                    ton_kho = line.MA_HANG_ID.lay_so_luong_ton_tat_ca_kho(self.NGAY_DON_HANG + ' 00:00:00', self.NGAY_DON_HANG + ' 23:59:59',self.CHI_NHANH_ID.id)
                    if ton_kho < ton_kho_toi_thieu:
                        error += '- Tên hàng: %s, Số lượng tồn: %s, Số lượng tồn tối thiểu: %s\n' % (line.MA_HANG_ID.TEN, ton_kho, ton_kho_toi_thieu)

        return error

    @api.model
    def create(self, values):   
        result = super(ACCOUNT_EX_DON_DAT_HANG, self).create(values)
        error = result.kiem_tra_ton_kho_toi_thieu()
        if error:
            error = 'Hàng hóa còn lại trong kho thấp hơn số lượng tồn tối thiểu:\n' + error
            return result.with_context({'error': {'title': 'Thông báo', 'text': error}})
        return result

    @api.model
    def default_get(self, fields):
        rec = super(ACCOUNT_EX_DON_DAT_HANG, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 3520

        # rec['KHACH_HANG_ID'] = self._context.get('default_KHACH_HANG_ID')
        # rec['TEN_KHACH_HANG'] = self._context.get('default_TEN_KHACH_HANG')
        # rec['DIA_CHI'] = self._context.get('default_DIA_CHI')
        # rec['NGUOI_NHAN_HANG'] = self._context.get('default_NGUOI_LIEN_HE')
        # rec['NV_BAN_HANG_ID'] = self._context.get('default_NV_MUA_HANG_ID')
       

        return rec

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI

    @api.onchange('TY_GIA')
    def update_thaydoiIsTy_gia(self):
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False
        for line in self.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
            line.tinh_tien_quy_doi()

    @api.onchange('KHACH_HANG_ID')
    def update_khach_hang(self):
        if self.KHACH_HANG_ID:
            self.TEN_KHACH_HANG = self.KHACH_HANG_ID.HO_VA_TEN
            self.DIA_CHI = self.KHACH_HANG_ID.DIA_CHI
            self.MA_SO_THUE = self.KHACH_HANG_ID.MA_SO_THUE
            if self.KHACH_HANG_ID.NHAN_VIEN_ID:
                self.NV_BAN_HANG_ID = self.KHACH_HANG_ID.NHAN_VIEN_ID.id
    
    @api.onchange('BAO_GIA_ID')
    def onchange_bao_gia(self):
        if self.BAO_GIA_ID:
            self.KHACH_HANG_ID = self.BAO_GIA_ID.KHACH_HANG_ID
            self.DIEN_GIAI = self.BAO_GIA_ID.GHI_CHU
            self.TEN_KHACH_HANG = self.BAO_GIA_ID.TEN_KHACH_HANG
            self.DIA_CHI = self.BAO_GIA_ID.DIA_CHI
            self.MA_SO_THUE = self.BAO_GIA_ID.MA_SO_THUE
            self.NGUOI_NHAN_HANG = self.BAO_GIA_ID.NGUOI_LIEN_HE
            if self.BAO_GIA_ID.NV_MUA_HANG_ID:
                self.NV_BAN_HANG_ID = self.BAO_GIA_ID.NV_MUA_HANG_ID
            self.currency_id = self.BAO_GIA_ID.currency_id

    @api.depends('ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien_hang = tong_tien_hang_quy_doi  = tong_tien_thue_gtgt = tong_tien_thue_gtgt_quy_doi = tong_tien_thanh_toan = tong_tien_thanh_toan_quy_doi = tong_chiet_khau = tong_chiet_khau_qd = 0
            phan_tram_thue=0
            for line in order.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                if line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT > phan_tram_thue:
                    phan_tram_thue= line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT
                tong_tien_hang +=line.THANH_TIEN
                tong_tien_hang_quy_doi +=line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt +=line.TIEN_THUE_GTGT
                tong_tien_thue_gtgt_quy_doi +=line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt
                tong_tien_thanh_toan_quy_doi = tong_tien_hang_quy_doi + tong_tien_thue_gtgt_quy_doi
                tong_chiet_khau +=line.TIEN_CHIET_KHAU
                tong_chiet_khau_qd +=line.TIEN_CHIET_KHAU_QUY_DOI

            order.update({
                'TONG_TIEN_HANG':tong_tien_hang,
                'TONG_TIEN_HANG_QUY_DOI':tong_tien_hang_quy_doi,
                'TONG_TIEN_THUE_GTGT':tong_tien_thue_gtgt,
                'TONG_TIEN_THUE_GTGT_QUY_DOI':tong_tien_thue_gtgt_quy_doi,
                'TONG_TIEN_THANH_TOAN':tong_tien_thanh_toan,
                'TONG_TIEN_THANH_TOAN_QUY_DOI':tong_tien_thanh_toan_quy_doi,
                'PHAN_TRAM_THUE': phan_tram_thue,
                'TONG_CHIET_KHAU': tong_chiet_khau,
                'TONG_CHIET_KHAU_QUY_DOI': tong_chiet_khau_qd,
            })


    @api.onchange('BAO_GIA_ID')
    def update_don_dat_hang_chi_tiet(self):
        if self.BAO_GIA_ID:
            #self là tập hợp các giá trị của model hiện tại
            #don_dat_hang=self
            #env = self.env['sale.ex.bao.gia.chi.tiet']
            self.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS = []
            #self.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS = []
                #xóa trắng đơn đặt hàng chi tiết

            #for trong bao giá chi tiết
                #tạo ra đơn đặt hàng chi tiết mới
                #gán cộng bằng vào chi tiết ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS
            for bao_gia_chi_tiet in self.BAO_GIA_ID.SALE_EX_BAO_GIA_CHI_TIET_IDS:
                new_line = self.env['account.ex.don.dat.hang.chi.tiet'].new({
                    'MA_HANG_ID' : bao_gia_chi_tiet.MA_HANG_ID,
                    'TEN_HANG' : bao_gia_chi_tiet.TEN_HANG,
                    'DVT_ID' : bao_gia_chi_tiet.DVT_ID,
                    'SO_LUONG' : bao_gia_chi_tiet.SO_LUONG,
                    'DON_GIA' : bao_gia_chi_tiet.DON_GIA,
                    
                    'THANH_TIEN' : bao_gia_chi_tiet.THANH_TIEN,
                    'THANH_TIEN_QUY_DOI' : bao_gia_chi_tiet.THANH_TIEN_QUY_DOI,
                    'PHAN_TRAM_THUE_GTGT_ID' : bao_gia_chi_tiet.PHAN_TRAM_THUE_GTGT_ID,
                    'TIEN_THUE_GTGT' : bao_gia_chi_tiet.TIEN_THUE_GTGT,
                    'TIEN_THUE_GTGT_QUY_DOI' : bao_gia_chi_tiet.TIEN_THUE_GTGT_QUY_DOI,
                })
                self.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS += new_line

    def tinh_cong_no_khach_hang(self, khach_hang_id, ngay):
        so_tien_no = 0
        query = """
            SELECT  COALESCE(SUM(COALESCE("GHI_NO", 0) - COALESCE("GHI_CO", 0)),0) as so_tien_no
            FROM    so_cong_no_chi_tiet AOL
                    INNER JOIN danh_muc_he_thong_tai_khoan A ON AOL."TK_ID" = A.id
            WHERE   A."DOI_TUONG_SELECTION" = '1'
                    AND a."DOI_TUONG" = TRUE
                    AND AOl."DOI_TUONG_ID" = %s
                    AND  '%s'  >= AOL."NGAY_HACH_TOAN"
        """ % (khach_hang_id, ngay)
        result = self.execute(query)
        if result:
            so_tien_no = result[0].get('so_tien_no') or 0
        return so_tien_no 

    def btn_xem_cong_no(self, args):
        if not self.KHACH_HANG_ID:
            raise ValidationError('Bạn cần chọn khách hàng để xem chi tiết công nợ!')
        to_date = self.NGAY_DON_HANG or datetime.today().strftime('%Y-%m-%d')
        so_tien_no = self.tinh_cong_no_khach_hang(self.KHACH_HANG_ID.id, to_date)        
        return """Dư Nợ của khách hàng <%s> tính đến hết ngày <%s>: %s (đ)""" % (self.TEN_KHACH_HANG, datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%Y'), '{:,}'.format(so_tien_no))