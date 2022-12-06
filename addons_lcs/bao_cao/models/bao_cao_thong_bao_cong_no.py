# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from operator import itemgetter
from odoo.addons import decimal_precision

class BAO_CAO_THONG_BAO_CONG_NO(models.Model):
    _name = 'bao.cao.thong.bao.cong.no'
    _auto = False

    CHI_NHANH_ID = fields.Many2one('res.company', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm dữ liệu chi nhánh phụ thuộc', help='Bao gồm dữ liệu của chi nhánh phụ thuộc')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',required=True, default='DAU_THANG_DEN_HIEN_TAI')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_PHIEU_THU = fields.Char(string='Số phiếu thu', help='Số phiếu thu')
    SO_PHIEU_CHI = fields.Char(string='Số phiếu chi', help='Số phiếu chi')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TAI_KHOAN = fields.Char(string='Tài khoản', help='Tài khoản')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='TK đối ứng')
    PS_NO = fields.Float(string='Nợ', digits=decimal_precision.get_precision('VND'))
    PS_CO = fields.Float(string='Có', digits=decimal_precision.get_precision('VND'))
    SO_TON = fields.Float(string='Số tồn', help='Số tồn', digits=decimal_precision.get_precision('VND'))
    NGUOI_NHAN_NOP = fields.Char(string='Người nhận/Người nộp', help='Người nhận/Người nộp')
    LOAI_PHIEU = fields.Selection([('0', 'Số tồn'),('1', 'Phiếu thu'),('2', 'Phiếu chi')])
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau')
    SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP = fields.Boolean(string='Sắp xếp chứng từ theo thứ tự lập')

    DOI_TUONG_ID = fields.Many2one('res.partner')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan')

    TAI_KHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_THONG_BAO_CONG_NO, self).default_get(fields_list)
        result['CHI_NHANH_ID'] = self.env['res.company'].search([], limit=1).id
        result['TAI_KHOAN_IDS'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','111%')]).ids
        result['currency_id'] = self.env['res.currency'].search([('TEN_LOAI_TIEN','=','VND')]).id
        return result

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    def _action_view_report(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'bao_cao.template_thong_bao_cong_no',
            'context': self._context,
            'report_type': 'qweb-html',
            'options': {'clear_breadcrumbs': True},
        }

class BAO_CAO_THONG_BAO_CONG_NO_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_thong_bao_cong_no'

    @api.model
    def get_report_values(self, docids, data=None):
        # currency_id = self.get_context('currency_id')
        # TU_NGAY_F = self.get_vntime('TU_NGAY')
        # DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        ############# SQL here #############
        # Mảng chứa kết quả
        docs = []
        docs += [self.env['bao.cao.thong.bao.cong.no'].new({
                'DOI_TUONG_ID': 144,
                'TK_NO_ID': 4004,
                'TK_CO_ID': 4003,
            })]
        return {
            'docs': docs,
            'data': data,
        }