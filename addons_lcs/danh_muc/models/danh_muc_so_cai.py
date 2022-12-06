# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision

class SO_CAI(models.Model):
    _name = 'so.cai'
    _description = 'Sổ cái'

    name = fields.Char()
    line_ids = fields.One2many('so.cai.chi.tiet', 'SO_CAI_ID')
    
    # @api.model
    # def create(self, vals):
    #     move = super(SO_CAI, self).create(vals)
    #     move.assert_balanced()
    #     return move
    
    # @api.multi
    # def write(self, vals):
    #     if 'line_ids' in vals:
    #         res = super(SO_CAI, self).write(vals)
    #         self.assert_balanced()
    #     else:
    #         res = super(SO_CAI, self).write(vals)
    #     return res

    # @api.multi
    # def assert_balanced(self):
    #     if not self.ids:
    #         return True
    #     prec = self.env['decimal.precision'].precision_get('Account')
    #     self._cr.execute("""\
    #         SELECT      "SO_CAI_ID"
    #         FROM        so_cai_chi_tiet
    #         WHERE       "SO_CAI_ID" in %s
    #         GROUP BY    "SO_CAI_ID"
    #         HAVING      abs(sum("GHI_NO") - sum("GHI_CO")) > %s
    #         """, (tuple(self.ids), 10 ** (-max(5, prec))))
    #     if len(self._cr.fetchall()) != 0:
    #         raise UserError("Định khoản không cân đối. Tổng Nợ phải bằng tổng Có!!")
    #     return True

class SO_CAI_CHI_TIET(models.Model):
    _name = 'so.cai.chi.tiet'
    _description = 'Sổ cái chi tiết'

    name = fields.Char(string="name")
    SO_CAI_ID = fields.Many2one('so.cai', ondelete="cascade")
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='RefType')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='InvNo')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='InvDate')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='AccountNumber')
    MA_TAI_KHOAN = fields.Char(string='Mã tài khoản', help='AccountNumber', compute='_compute_tai_khoan', store=True, )
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản', compute='_compute_tai_khoan', store=True, )
    TAI_KHOAN_DOI_UNG_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='CorrespondingAccountNumber', help='Tài khoản đối ứng')
    MA_TAI_KHOAN_DOI_UNG = fields.Char(string='Mã tài khoản đối ứng', help='CorrespondingAccountNumber', compute='_compute_tai_khoan_doi_ung', store=True, )
    TAI_KHOAN_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Tài khoản ngân hàng', help='BankAccountID')
    SO_TAI_KHOAN_NGAN_HANG = fields.Char(string='Số tài khoản ngân hàng', help='BankAccountNumber', compute='_compute_tai_khoan_ngan_hang', store=True, )
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='', compute='_compute_tai_khoan_ngan_hang', store=True,)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True)
    TEN_LOAI_TIEN = fields.Char(string='Tên loại tiền', help='CurrencyID', compute='_compute_loai_tien', store=True, )
    TY_GIA = fields.Float(string='Tỉ giá', help='ExchangeRate')
    GHI_NO = fields.Float(string='Ghi nợ', help='DebitAmount')
    GHI_CO = fields.Float(string='Ghi có', help='CreditAmount')
    GHI_NO_NGUYEN_TE = fields.Float(string='Ghi nợ nguyên tệ', help='DebitAmountOC')
    GHI_CO_NGUYEN_TE = fields.Float(string='Ghi có nguyên tệ', help='CreditAmountOC')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='JournalMemo')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description')
    NGUOI_LIEN_HE = fields.Char(string='Người liên hệ', help='ContactName')
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='InventoryItemID')
    MA_HANG = fields.Char(string='Mã sản phẩm', help='InventoryItemCode', compute='_compute_ma_hang', store=True)
    TEN_HANG = fields.Text(string='Tên sản phẩm', help='InventoryItemName', compute='_compute_ma_hang', store=True)
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đvt', help='UnitID')
    SO_LUONG = fields.Float(string='Số lượng', help='Quantity', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='UnitPrice', digits=decimal_precision.get_precision('DON_GIA'))
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='AccountObjectID')
    MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='AccountObjectCode', compute='_compute_doi_tuong', store=True, )
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectName' )
    DIA_CHI_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectAddress' )
    MA_SO_THUE_DOI_TUONG = fields.Char(string='Mã số thuế đối tượng', help='AccountObjectTaxCode')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='EmployeeID')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên bán hàng', help='EmployeeCode', compute='_compute_nhan_vien', store=True, )
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên bán hàng', help='EmployeeName', compute='_compute_nhan_vien', store=True, )
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Phòng ban nhân viên', help='?', oldname='PHONG_BAN_NHAN_VIEN_ID')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', readonly=True)
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='SortOrder')
    LOAI_NGHIEP_VU = fields.Selection([('0', 'Chiết khấu thương mại'), ('1', 'Giảm giá hàng bán'),('2', 'Trả lại hàng bán'),('3', '') ], string='Loại nghiệp vụ', help='BusinessType')
    CHI_TIET_ID = fields.Integer(string='Chi tiết', help='Chi tiết')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)
    GIA_VON = fields.Float(string='Giá vốn', help='UnitPrice')
    LOAI_HACH_TOAN = fields.Selection([('1', 'Chứng từ ghi nợ'), ('2', 'Chứng từ ghi có')], string='Loại hạch toán' , help='EntryType')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='ProjectWorkID')
    NGUOI_NHAN_NOP = fields.Char(string='Người nhận nộp', help='?')

    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='DueDate')

    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='ListItemID')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='JobID')

    THU_TU_CHI_TIET_GHI_SO = fields.Integer(string='Thứ tự chi tiết ghi sổ', help='DetailPostOrder')

    DON_GIA_NGUYEN_TE = fields.Float(string='Đơn giá nguyên tệ', help='UnitPriceOC')
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo đơn vị tính chính', help='MainUnitPrice')
    TEN_LOAI_CHUNG_TU = fields.Char(string='Tên loại chứng từ', help='RefTypeName', compute='_compute_loai_chung_tu', store=True)
    # 



    # Compute
    @api.depends('TAI_KHOAN_ID')
    def _compute_tai_khoan(self):
        for record in self:
            if record.TAI_KHOAN_ID:
                record.MA_TAI_KHOAN = record.TAI_KHOAN_ID.SO_TAI_KHOAN
                record.TEN_TAI_KHOAN = record.TAI_KHOAN_ID.TEN_TAI_KHOAN
    
    @api.depends('TAI_KHOAN_DOI_UNG_ID')
    def _compute_tai_khoan_doi_ung(self):
        for record in self:
            if record.TAI_KHOAN_DOI_UNG_ID:
                record.MA_TAI_KHOAN_DOI_UNG = record.TAI_KHOAN_DOI_UNG_ID.SO_TAI_KHOAN

    @api.depends('currency_id')
    def _compute_loai_tien(self):
        for record in self:
            if record.currency_id:
                record.TEN_LOAI_TIEN = record.currency_id.MA_LOAI_TIEN

    @api.depends('DOI_TUONG_ID')
    def _compute_doi_tuong(self):
        for record in self:
            if record.DOI_TUONG_ID:
                # record.TEN_DOI_TUONG = record.DOI_TUONG_ID.HO_VA_TEN
                record.MA_DOI_TUONG = record.DOI_TUONG_ID.MA
                # record.DIA_CHI_DOI_TUONG = record.DOI_TUONG_ID.DIA_CHI
                # record.MA_SO_THUE_DOI_TUONG = record.DOI_TUONG_ID.MA_SO_THUE

    @api.depends('MA_HANG_ID')
    def _compute_ma_hang(self):
        for record in self:
            record.MA_HANG = record.MA_HANG_ID.MA
            record.TEN_HANG = record.MA_HANG_ID.TEN

    @api.depends('NHAN_VIEN_ID')
    def _compute_nhan_vien(self):
        for record in self:
            if record.NHAN_VIEN_ID:
                record.MA_NHAN_VIEN = record.NHAN_VIEN_ID.MA
                record.TEN_NHAN_VIEN = record.NHAN_VIEN_ID.HO_VA_TEN

    @api.depends('TAI_KHOAN_NGAN_HANG_ID')
    def _compute_tai_khoan_ngan_hang(self):
        for record in self:
            record.SO_TAI_KHOAN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG_ID.SO_TAI_KHOAN
            record.TEN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG_ID.CHI_NHANH

    @api.depends('LOAI_CHUNG_TU')
    def _compute_loai_chung_tu(self):
        for record in self:
            ten_loai_chung_tu = ''
            loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', int(record.LOAI_CHUNG_TU))],limit=1)
            if loai_chung_tu:
                ten_loai_chung_tu = loai_chung_tu.REFTYPENAME
            record.TEN_LOAI_CHUNG_TU = ten_loai_chung_tu

    
    @api.model
    def create(self, values):
        if 'MA_SO_THUE_DOI_TUONG' not in values and 'DOI_TUONG_ID' in values:
            ma_so_thue = self.env['res.partner'].search([('id', '=', values.get('DOI_TUONG_ID'))],limit=1).MA_SO_THUE
            if ma_so_thue:
                values['MA_SO_THUE_DOI_TUONG'] = ma_so_thue
        loi = self.validate_theo_tai_khoan(values)
        if values.get('MODEL_CHUNG_TU') != 'account.ex.so.du.tai.khoan.chi.tiet':
            if not (values.get('TAI_KHOAN_ID') and values.get('TAI_KHOAN_DOI_UNG_ID')):
                ten_loai_chung_tu = ''
                ma_hang = ''
                loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', int(values.get('LOAI_CHUNG_TU')))],limit=1)
                if loai_chung_tu:
                    ten_loai_chung_tu = loai_chung_tu.REFTYPENAME
                
                if values.get('MA_HANG_ID'):
                    hang = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', '=', values.get('MA_HANG_ID'))],limit=1)
                    ma_hang = hang.TEN
                err = 'Định khoản không hợp lệ\n- Loại chứng từ: ' + ten_loai_chung_tu + '\n- Số chứng từ: ' + str(values.get('SO_CHUNG_TU')) + '\n- Mã hàng: ' + ma_hang
                if self._context.get('bao_tri'):
                    err += '. Số chứng từ %s - %s' % (values.get('SO_CHUNG_TU'), values.get('DIEN_GIAI'))
                raise ValidationError(err)
        if loi[0] == 'True' and not self._context.get('fromMS'):
            raise ValidationError(loi[1])
        result = super(SO_CAI_CHI_TIET, self).create(values)
            
        return result
    

    def validate_theo_tai_khoan(self,values):
        loi = ''
        cac_cot_bat_buoc_nhap = []
        arr_return = []
        thong_bao_loi = []
        thong_bao_loi.append('Lỗi ghi sổ chứng từ:')
        if values.get('TAI_KHOAN_ID'):
            tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', values.get('TAI_KHOAN_ID'))])
            if not values.get('DOI_TUONG_ID'):
                if tai_khoan.DOI_TUONG == True:
                    if tai_khoan.DOI_TUONG_SELECTION == '0':
                        cac_cot_bat_buoc_nhap.append('<Nhà cung cấp>')
                    elif tai_khoan.DOI_TUONG_SELECTION == '1':
                        cac_cot_bat_buoc_nhap.append('<Khách hàng>')
                    elif tai_khoan.DOI_TUONG_SELECTION == '2':
                        cac_cot_bat_buoc_nhap.append('<Nhân viên>')
            else:
                doi_tuong = self.env['res.partner'].search([('id', '=', values.get('DOI_TUONG_ID'))])
                if tai_khoan.DOI_TUONG == True:
                    if tai_khoan.DOI_TUONG_SELECTION == '0' and doi_tuong.LA_NHA_CUNG_CAP == False:
                        cac_cot_bat_buoc_nhap.append('<Nhà cung cấp>')
                    elif tai_khoan.DOI_TUONG_SELECTION == '1' and doi_tuong.LA_KHACH_HANG == False:
                        cac_cot_bat_buoc_nhap.append('<Khách hàng>')
                    elif tai_khoan.DOI_TUONG_SELECTION == '2' and doi_tuong.LA_NHAN_VIEN == False:
                        cac_cot_bat_buoc_nhap.append('<Nhân viên>')
            if not values.get('TAI_KHOAN_NGAN_HANG_ID'):
                if tai_khoan.TAI_KHOAN_NGAN_HANG == True:
                    cac_cot_bat_buoc_nhap.append('<Tài khoản ngân hàng>')
            if not values.get('CONG_TRINH_ID'):
                if tai_khoan.CONG_TRINH == True:
                    if tai_khoan.CONG_TRINH_SELECTION == '1':
                        cac_cot_bat_buoc_nhap.append('<Công trình>')
            if not values.get('KHOAN_MUC_CP_ID'):
                if tai_khoan.KHOAN_MUC_CP == True:
                    if tai_khoan.KHOAN_MUC_CP_SELECTION == '1':
                        cac_cot_bat_buoc_nhap.append('<Khoản mục chi phí>')
        if len(cac_cot_bat_buoc_nhap) > 0:
            loi = 'TK '+ str(tai_khoan.SO_TAI_KHOAN)+ ' chi tiết theo ' + ",".join(cac_cot_bat_buoc_nhap) +', chứng từ hạch toán thiếu '+ ",".join(cac_cot_bat_buoc_nhap) + '.'  #+ str(values.get('SO_CHUNG_TU'))
            thong_bao_loi.append(loi)
        # cac_cot_bat_buoc_nhap = []
        # if values.get('TAI_KHOAN_DOI_UNG_ID'):
        #     tai_khoan_doi_ung = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', values.get('TAI_KHOAN_DOI_UNG_ID'))])
        #     if not values.get('DOI_TUONG_ID'):
        #         if tai_khoan_doi_ung.DOI_TUONG == True:
        #             if tai_khoan_doi_ung.DOI_TUONG_SELECTION == '0':
        #                 cac_cot_bat_buoc_nhap.append('<Nhà cung cấp>')
        #             elif tai_khoan_doi_ung.DOI_TUONG_SELECTION == '1':
        #                 cac_cot_bat_buoc_nhap.append('<Khách hàng>')
        #             elif tai_khoan_doi_ung.DOI_TUONG_SELECTION == '2':
        #                 cac_cot_bat_buoc_nhap.append('<Nhân viên>')
        #     else:
        #         doi_tuong = self.env['res.partner'].search([('id', '=', values.get('DOI_TUONG_ID'))])
        #         if tai_khoan_doi_ung.DOI_TUONG == True:
        #             if tai_khoan_doi_ung.DOI_TUONG_SELECTION == '0' and doi_tuong.LA_NHA_CUNG_CAP == False:
        #                 cac_cot_bat_buoc_nhap.append('<Nhà cung cấp>')
        #             elif tai_khoan_doi_ung.DOI_TUONG_SELECTION == '1' and doi_tuong.LA_KHACH_HANG == False:
        #                 cac_cot_bat_buoc_nhap.append('<Khách hàng>')
        #             elif tai_khoan_doi_ung.DOI_TUONG_SELECTION == '2' and doi_tuong.LA_NHAN_VIEN == False:
        #                 cac_cot_bat_buoc_nhap.append('<Nhân viên>')
        #     if not values.get('TAI_KHOAN_NGAN_HANG_ID'):
        #         if tai_khoan_doi_ung.TAI_KHOAN_NGAN_HANG == True:
        #             cac_cot_bat_buoc_nhap.append('<Tài khoản ngân hàng>')
        #     if not values.get('CONG_TRINH_ID'):
        #         if tai_khoan_doi_ung.CONG_TRINH == True:
        #             if tai_khoan_doi_ung.CONG_TRINH_SELECTION == '1':
        #                 cac_cot_bat_buoc_nhap.append('<Công trình>')
        #     if not values.get('KHOAN_MUC_CP_ID'):
        #         if tai_khoan_doi_ung.KHOAN_MUC_CP == True:
        #             if tai_khoan_doi_ung.KHOAN_MUC_CP_SELECTION == '1':
        #                 cac_cot_bat_buoc_nhap.append('<Khoản mục chi phí>')
        # if len(cac_cot_bat_buoc_nhap) > 0:
        #     loi = 'TK '+ str(tai_khoan_doi_ung.SO_TAI_KHOAN) + ' chi tiết theo ' + ",".join(cac_cot_bat_buoc_nhap) +', chứng từ hạch toán thiếu '+ ",".join(cac_cot_bat_buoc_nhap) + '.' + str(values.get('SO_CHUNG_TU'))
        #     thong_bao_loi.append(loi)
        thong_bao_loi.append('Ghi sổ không thành công')
        Loi_hien_thi = "\n".join(thong_bao_loi)
        if loi == '':
            arr_return.append('False')
            arr_return.append(Loi_hien_thi)
        else:
            arr_return.append('True')
            arr_return.append(Loi_hien_thi)
        return arr_return
