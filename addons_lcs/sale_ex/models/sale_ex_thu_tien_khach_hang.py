# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class SALE_EX_THU_TIEN_KHACH_HANG(models.Model):
    _name = 'sale.ex.thu.tien.khach.hang'
    _description = 'Thu tiền khách hàng'
    _auto = False

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    NGAY_THU_TIEN = fields.Date(string='Ngày thu tiền', help='Ngày thu tiền',default=fields.Datetime.now)
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nv bán hàng', help='Nv bán hàng')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',compute='_tinh_so_tien',digits=decimal_precision.get_precision('Product Price'))
    PHUONG_THUC_THANH_TOAN = fields.Selection([('TIEN_MAT', 'Tiền mặt'), ('TIEN_GUI', ' Tiền gửi'), ], string='Phưởng thức thanh toán', help='Phưởng thức thanh toán',default='TIEN_GUI',required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    IS_TY_GIA = fields.Boolean(default=False)


    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
      result = super(SALE_EX_THU_TIEN_KHACH_HANG, self).default_get(fields_list)
      result['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=','VND')], limit=1).id
      result['TY_GIA'] = 1
      return result
    SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET_IDS = fields.One2many('sale.ex.thu.tien.khach.hang.chi.tiet', 'THU_TIEN_KHACH_HANG_ID', string='Thu tiền khách hàng chi tiết')

    def action_view_result(self):
        if self.get_context('DOI_TUONG_ID') == 'False':
            raise ValidationError('Bạn chưa chọn khách hàng!')
        if self.get_context('SO_TIEN') == 0:
            raise ValidationError('Bạn chưa chọn chứng từ. Vui lòng kiểm tra lại!')
        action = self.env.ref('sale_ex.action_open_sale_ex_thu_tien_khach_hang_form').read()[0]

        name = self.env['res.partner'].search([('id', '=',self.get_context('DOI_TUONG_ID'))], limit=1).HO_VA_TEN
        str1 = 'Thu tiền của '
        tr_diengiai = str1 + str(name)
        tk_no = 1
        is_nguoi_nop = True
        if self.get_context('PHUONG_THUC_THANH_TOAN') =='TIEN_MAT':
            tk_no = 188
            is_nguoi_nop = True
        elif self.get_context('PHUONG_THUC_THANH_TOAN') =='TIEN_GUI':
            tk_no = 189
            is_nguoi_nop = False
        ct_cong_no_ids = self.get_context('SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET_IDS')
        arr = []
        for line in ct_cong_no_ids:
            if line['CHON'] == 'True':
                arr += [(0, 0, {
                    # 'NGAY_CHUNG_TU' : line['NGAY_CHUNG_TU'],
                    'SO_CHUNG_TU': line['SO_CHUNG_TU'],
                    # 'HAN_HACH_TOAN' : line.HAN_HACH_TOAN,
                    'SO_HOA_DON': line['SO_HOA_DON'],
                    # 'NGAY_HOA_DON': line.NGAY_HOA_DON,
                    # 'NGAY_CHUNG_TU': line.create_date,
                    'SO_PHAI_THU': line['SO_PHAI_THU'],
                    'SO_CHUA_THU': line['SO_CHUA_THU'],
                    'SO_THU' : line['SO_THU'],
                    'TK_PHAI_THU_ID': 9,
                    'DIEU_KHOAN_THANH_TOAN': line['DIEU_KHOAN_THANH_TOAN'],
                    'TY_LE_CK': line['TY_LE_CK'],
                    'TIEN_CHIET_KHAU': line['TIEN_CHIET_KHAU'],
                    'TK_CHIET_KHAU_ID': line['TK_CHIET_KHAU_ID'],
                    })]


        context = {
            'default_partner_id': self.get_context('DOI_TUONG_ID'),
            'default_IS_NGUOI_NOP': is_nguoi_nop,
            'default_LY_DO_NOP': tr_diengiai,
            'default_account_payment_ids': [(0, 0, {
                'amount':self.get_context('SO_TIEN'),
                'dien_giai':tr_diengiai,
                'tk_no_id' : tk_no,
                'tk_co_id' : 9,
                })],
            'default_ACCOUNT_EX_PHIEU_THU_TIEN_KHACH_HANG_CHUNG_TU_IDS' : arr,
            }

        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['options'] = {'clear_breadcrumbs': True}
        return action
    @api.onchange('currency_id')
    def update_LOAI_TIEN(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.currency_id.TEN_LOAI_TIEN =='VND':
            self.IS_TY_GIA = False
        else:
            self.IS_TY_GIA = True
    @api.onchange('DOI_TUONG_ID')
    def update_KHACH_HANG_ID(self):
        if self.DOI_TUONG_ID:
            env = self.env['sale.ex.thu.tien.khach.hang.chi.tiet']
            ct_cong_no_ids = self.env['account.invoice'].search([('partner_id', '=', self.DOI_TUONG_ID.id),('state', '=', 'open'),('type','=','in_invoice')])
            # ct_cong_no_ids = self.env['account.invoice'].search([('DOI_TUONG_ID', '=', 14),('state', '=', 'open'),('type','=','in_invoice')])
            self.SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET_IDS = []
            for ct in ct_cong_no_ids:
                new_line = env.new({
                    'SO_CHUNG_TU': ct.origin,
                    'SO_HOA_DON': ct.SO_HOA_DON,
                    'NGAY_HOA_DON': ct.NGAY_HOA_DON,
                    'NGAY_CHUNG_TU': ct.create_date,
                    'SO_PHAI_THU': ct.amount_total,
                    'SO_CHUA_THU': ct.residual,
                    'TK_PHAI_THU': '131',
                    'DIEU_KHOAN_TT': ct.payment_term_id.name,
                    'SO_CHUNG_TU': ct.SO_CHUNG_TU,
                    'DIEN_GIAI': ct.DIEN_GIAI,
                    'HAN_HACH_TOAN': ct.HAN_HACH_TOAN,
                    'TK_CHIET_KHAU_ID' : 168,
                })
                self.SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET_IDS += new_line

    @api.depends('SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET_IDS.SO_THU')
    def _tinh_so_tien(self):
        self.SO_TIEN = 0.0
        for line in self.SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET_IDS:
            self.SO_TIEN += line.SO_THU

            


