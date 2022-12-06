# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_CHUNG_TU_GHI_TANG_TSCD_NGHT(models.Model):
    _name = 'bao.cao.chung.tu.ghi.tang.tscd.nght'
    _auto = False

    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ') #RefDate

    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung')#JournalMemo
    SO_CHUNG_TU = fields.Char(string='Số chứng từ')#RefNo
    SO_LUONG = fields.Float(string='Số lượng') #Quantity
    SO_TIEN = fields.Float(string='Số tiền') #Amount
    TK_NO  = fields.Char(string='TK nợ')
    TK_CO  = fields.Char(string='TK có')

    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ') #RefType1
    LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH = fields.Integer(string='Loại chứng từ') #RefType
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp') #SortOrder

    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.chung.tu.ghi.tang.tscd', string='Phiếu thu chi', help='Phiếu thu chi')
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    