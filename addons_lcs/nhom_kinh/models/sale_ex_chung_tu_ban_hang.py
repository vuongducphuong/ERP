# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_DOCUMENT(models.Model):
    _inherit = 'sale.document'

    LAP_TU_DON_DAT_HANG_IDS = fields.Many2many('account.ex.don.dat.hang', string='Từ đơn hàng')

    @api.onchange('LAP_TU_DON_DAT_HANG_IDS')
    def _onchange_LAP_TU_DON_DAT_HANG_IDS(self):
        self.SALE_DOCUMENT_LINE_IDS = []
        default = self.SALE_DOCUMENT_LINE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU)
        tong_tien_gia_cong = 0
        for record in self.LAP_TU_DON_DAT_HANG_IDS:
            self.DOI_TUONG_ID = record.KHACH_HANG_ID.id 
            self.TEN_KHACH_HANG = record.TEN_KHACH_HANG
            self.MA_SO_THUE = record.MA_SO_THUE
            self.DIA_CHI = record.DIA_CHI
            self.DIEN_GIAI = record.DIEN_GIAI
            self.LY_DO_NHAP_XUAT = 'Xuất kho bán hàng '+ str(record.TEN_KHACH_HANG)
            tong_tien_gia_cong += record.TONG_TIEN_GIA_CONG

            for line in record.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                san_pham =  line.MA_HANG_ID
                dien_giai_thue = ''
                kho_id = 0
                tk_gia_von_id = 0
                if san_pham:
                    ten_san_pham = san_pham.TEN
                    dien_giai_thue = 'Thuế GTGT - '+str(ten_san_pham)
                    kho_id = san_pham.TAI_KHOAN_KHO_ID.id
                tk_gia_von_632 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '632')],limit=1)
                if tk_gia_von_632:
                    tk_gia_von_id = tk_gia_von_632.id

                self.SALE_DOCUMENT_LINE_IDS += self.env['sale.document.line'].new({
                    'MA_HANG_ID': line.MA_HANG_ID.id,
                    'TEN_HANG': line.TEN_HANG,
                    'DIEN_GIAI_THUE': dien_giai_thue,
                    'KHO_ID': line.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                    'TK_NO_ID': default.get('TK_NO_ID'),
                    'TK_CO_ID': default.get('TK_CO_ID'),
                    'TK_THUE_GTGT_ID': default.get('TK_THUE_GTGT_ID'),
                    'TK_CHIET_KHAU_ID': default.get('TK_CHIET_KHAU_ID'),
                    'TK_KHO_ID': kho_id,
                    'TK_GIA_VON_ID': tk_gia_von_id,
                    'DON_GIA': line.DON_GIA,
                    'SO_LUONG': line.SO_LUONG,
                    'THANH_TIEN': line.THANH_TIEN,
                    'THANH_TIEN_QUY_DOI': line.THANH_TIEN_QUY_DOI,
                    'DVT_ID': line.DVT_ID.id,
                    'DON_VI_ID':  line.MA_HANG_ID.CHI_NHANH_ID,
                    'THUE_GTGT_ID':  line.PHAN_TRAM_THUE_GTGT_ID,
                    'TIEN_THUE_GTGT':  line.TIEN_THUE_GTGT,
                    'TIEN_THUE_GTGT_QUY_DOI':  line.TIEN_THUE_GTGT_QUY_DOI,
                    'DON_DAT_HANG_CHI_TIET_ID':  line.id,
                    'DON_DAT_HANG_ID':  record.id,
                    'CHIEU_DAI': line.CHIEU_DAI,
                    'CHIEU_RONG': line.CHIEU_RONG,
                    'LUONG': line.LUONG,
                })

        if tong_tien_gia_cong > 0:
            self.SALE_DOCUMENT_LINE_IDS += self.env['sale.document.line'].new({
                'MA_HANG_ID': self.env.ref('nhom_kinh.danh_muc_vthh_cpgc').id,
                'TEN_HANG': 'Chi phí gia công',
                'TK_NO_ID': default.get('TK_NO_ID'),
                'TK_CO_ID': default.get('TK_CO_ID'),
                'TK_THUE_GTGT_ID': default.get('TK_THUE_GTGT_ID'),
                'TK_CHIET_KHAU_ID': default.get('TK_CHIET_KHAU_ID'),
                'DON_GIA': tong_tien_gia_cong,
                'SO_LUONG': 1,
                'THANH_TIEN': tong_tien_gia_cong,
                'THANH_TIEN_QUY_DOI': tong_tien_gia_cong
            })