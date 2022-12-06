# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision


class ACCOUNT_TRA_TIEN_NHA_CUNG_CAP(models.Model):
    _name = "account.tra.tien.nha.cung.cap"
    _auto = False
    _description = "Trả tiền nhà cung cấp"

    phuong_thuc_thanh_toan = fields.Selection([('tien_mat','Tiền mặt'), ('UY_NHIEM_CHI', 'Ủy nhiệm chi'), ('SEC_TIEN_MAT', 'Séc tiền mặt'), ('SEC_CHUYEN_KHOAN', 'Séc chuyển khoản')], string='Phương thức TT', default='tien_mat', help='Phương thức thanh toán',required=True)
    loai_tien = fields.Many2one('res.currency',string='Loại tiền', help='Loại tiền')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp')
    ngay_tra_tien = fields.Date('Ngày trả tiền',default=fields.Datetime.now)
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV mua hàng',help='Nhân viên mua hàng')
    so_tien = fields.Float('Số tiền',compute='_tinh_so_tien',digits=decimal_precision.get_precision('Product Price'))
    PURCHASE_EX_CHUNG_TU_CONG_NO_IDS = fields.One2many('purchase.ex.chung.tu.cong.no', 'TRA_TIEN_NHA_CUNG_CAP_ID', string='Chứng từ công nợ')


    @api.model
    def default_get(self, fields):
        rec = super(ACCOUNT_TRA_TIEN_NHA_CUNG_CAP, self).default_get(fields)
        rec['loai_tien'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=','VND')],limit=1).id
        return rec

    def action_view_result(self):
        # self._validate()
        if self.get_context('so_tien') == 0:
            raise ValidationError('Bạn chưa chọn chứng từ. Vui lòng kiểm tra lại!')
        action = self.env.ref('purchase_ex.action_account_phieuchi_tra_tien_nha_cung_cap').read()[0]
        str1 = 'Trả tiền cho '
        name = self.env['res.partner'].search([('id', '=',self.get_context('DOI_TUONG_ID'))], limit=1).HO_VA_TEN
        tk_co_tien_mat = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like','111%')], limit=1).id
        tk_co_uy_nhiem_chi = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like','112%')], limit=1).id
        tk_co_sec_tien_mat = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like','121%')], limit=1).id
        tk_co_sec_chuyen_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like','112%')], limit=1).id
        tk_co = 1
        if self.get_context('phuong_thuc_thanh_toan') == 'tien_mat':
            tk_co = tk_co_tien_mat
        elif self.get_context('phuong_thuc_thanh_toan') == 'UY_NHIEM_CHI':
            tk_co = tk_co_uy_nhiem_chi
        elif self.get_context('phuong_thuc_thanh_toan') == 'SEC_TIEN_MAT':
            tk_co = tk_co_sec_tien_mat
        elif self.get_context('phuong_thuc_thanh_toan') == 'SEC_CHUYEN_KHOAN':
            tk_co = tk_co_sec_chuyen_khoan
        tr_diengiai = str1 + str(name)

        # Inactive 2019-04-01 by anhtuan: Đợi SQL
        # ct_cong_no_ids = self.env['account.invoice'].search([('partner_id', '=', self.get_context('DOI_TUONG_ID')),('state', '=', 'open')])
        arr = []
        # for line in ct_cong_no_ids:
        #     arr += [(0, 0, {
        #         'SO_CHUNG_TU': line.origin,
        #         'SO_HOA_DON': line.SO_HOA_DON,
        #         # 'NGAY_HOA_DON': line.NGAY_HOA_DON,
        #         # 'NGAY_CHUNG_TU': line.create_date,
        #         'TONG_NO': line.TONG_TIEN_THANH_TOAN,
        #         'SO_CON_NO': line.residual,
        #         'TK_PHAI_TRA': '331',
        #         'DIEU_KHOAN_TT': line.DIEU_KHOAN_THANH_TOAN_ID.name,
        #         'SO_CHUNG_TU': line.SO_CHUNG_TU,
        #         'DIEN_GIAI': line.DIEN_GIAI,
        #         # 'HAN_THANH_TOAN': line.HAN_HACH_TOAN,
        #         })]

        context = {
            'default_partner_id': self.get_context('DOI_TUONG_ID'),
            'PHUONG_THUC_TT' : self.get_context('phuong_thuc_thanh_toan'),
            'default_account_payment_ids': [(0, 0, {
                'amount':self.get_context('so_tien'),
                'DIEN_GIAI_CHUNG':tr_diengiai,
                'tk_no_id' : 71,
                'tk_co_id' : tk_co,
                })],
            'default_ACCOUNT_EX_SEC_CHUYEN_KHOAN_TRA_TIEN_NHA_CUNG_CAP_IDS' : arr,
            }
        
        
        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['domain'] = [('account_payment_ids.tk_co_id.SO_TAI_KHOAN', 'like', '111')]
        # action['options'] = {'clear_breadcrumbs': True}

        return action

    def _validate(self):
        ct_cong_no = self.get_context('PURCHASE_EX_CHUNG_TU_CONG_NO_IDS')
        if(not len(ct_cong_no)):
            raise ValidationError('Bạn chưa chọn chứng từ. Vui lòng kiểm tra lại!')

    @api.onchange('DOI_TUONG_ID')
    def _update_ct_cong_no(self):
        env = self.env['purchase.ex.chung.tu.cong.no']
		# Inactive 2019-04-01 by anhtuan: Đợi SQL
        # ct_cong_no_ids = self.env['account.invoice'].search([('partner_id', '=', self.DOI_TUONG_ID.id),('state', '=', 'open'),('type','=','in_invoice')])
        # self.PURCHASE_EX_CHUNG_TU_CONG_NO_IDS = []
        # for ct in ct_cong_no_ids:
            # new_line = env.new({
                # 'SO_CHUNG_TU': ct.origin,
                # 'SO_HOA_DON': ct.SO_HOA_DON,
                # 'NGAY_HOA_DON': ct.NGAY_HOA_DON,
                # 'NGAY_CHUNG_TU': ct.create_date,
                # 'TONG_NO': ct.TONG_TIEN_THANH_TOAN,
                # 'SO_CON_NO': ct.residual,
                # 'TK_PHAI_TRA': '331',
                # 'DIEU_KHOAN_TT': ct.DIEU_KHOAN_THANH_TOAN_ID.name,
                # 'SO_CHUNG_TU': ct.SO_CHUNG_TU,
                # 'DIEN_GIAI': ct.DIEN_GIAI,
                # 'HAN_HACH_TOAN': ct.HAN_HACH_TOAN,
            # })
            # self.PURCHASE_EX_CHUNG_TU_CONG_NO_IDS += new_line
    @api.depends('PURCHASE_EX_CHUNG_TU_CONG_NO_IDS.SO_TRA')
    def _tinh_so_tien(self):
        self.so_tien = 0.0
        for line in self.PURCHASE_EX_CHUNG_TU_CONG_NO_IDS:
            self.so_tien += line.SO_TRA

class PURCHASE_EX_CHUNG_TU_CONG_NO(models.Model):
    _name = 'purchase.ex.chung.tu.cong.no'
    _description = ''
    _inherit = ['mail.thread']
    
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chừng từ', help='Số chừng từ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    HAN_HACH_TOAN = fields.Date(string='Hạn hạch toán', help='Hạn hạch toán')
    TONG_NO = fields.Float(string='Tổng nợ', help='Tổng nợ',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_NO = fields.Float(string='Số còn nợ', help='Số còn nợ',digits=decimal_precision.get_precision('Product Price'))
    SO_TRA = fields.Float(string='Số trả', help='Số trả',digits=decimal_precision.get_precision('Product Price'))
    TK_PHAI_TRA = fields.Char(string='TK phải trả', help='Tài khoản phải trả')
    DIEU_KHOAN_TT = fields.Char(string='Điều khoản TT', help='Điều khoản thanh toán')
    TY_LE_CK = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ chiết khấu')
    TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='Tiền chiết khấu',digits=decimal_precision.get_precision('Product Price'))
    TK_CHIET_KHAU = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='Tài khoản chiết khấu')
    TRA_TIEN_NHA_CUNG_CAP_ID = fields.Many2one('account.tra.tien.nha.cung.cap', string='Trả tiền nhà cung cấp', help='Trả tiền nhà cung cấp')
    AUTO_SELECT = fields.Boolean()
    @api.onchange('AUTO_SELECT')
    def update_AUTO_SELECT(self):
        if  self.AUTO_SELECT == True:
            if self.SO_TRA == 0:
                self.SO_TRA = self.SO_CON_NO
        if self.AUTO_SELECT == False:
            self.SO_TRA = 0

    @api.onchange('SO_TRA')
    def update_SO_TRA(self):
        if self.SO_TRA > 0:
            self.AUTO_SELECT = True

    @api.onchange('TY_LE_CK')
    def update_TY_LE_CK(self):
        self.TIEN_CHIET_KHAU = (self.TY_LE_CK*self.SO_TRA)/100
