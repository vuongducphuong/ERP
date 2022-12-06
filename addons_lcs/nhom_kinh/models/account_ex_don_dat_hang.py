# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class ACCOUNT_EX_DON_DAT_HANG(models.Model):
    _inherit = 'account.ex.don.dat.hang'

    TONG_TIEN_GIA_CONG = fields.Monetary(string='Tiền gia công', currency_field='base_currency_id', compute='tinh_tong_tien', store=True)
    # CHUNG_TU_BAN_HANG_ID = fields.Many2one('sale.document', string='Chứng từ bán hàng', help='Chứng từ bán hàng tạo từ đơn đặt hàng này', ondelete='set null')
    PHUONG_TIEN_VAN_CHUYEN = fields.Char(string='Phương tiện VC', help='Phương tiện vận chuyển')

    NO_CU = fields.Monetary(string='Nợ cũ', currency_field='base_currency_id', store=False)
    SO_THANH_TOAN = fields.Monetary(string='Số thanh toán', currency_field='base_currency_id')
    TONG_NO = fields.Monetary(string='Tổng nợ', currency_field='base_currency_id', store=False)

    TONG_SL_TAM = fields.Float(string='Tổng số lượng tấm',digits= decimal_precision.get_precision('SO_LUONG'),compute='tinh_tong_tien', store=True)
    TONG_SL_M2 = fields.Float(string='Tổng số lượng m2',digits= decimal_precision.get_precision('SO_LUONG'),compute='tinh_tong_tien', store=True)
    TONG_SL_MM = fields.Float(string='Tổng số lượng mm',digits= decimal_precision.get_precision('SO_LUONG'),compute='tinh_tong_tien', store=True)
    TONG_SL_LO = fields.Float(string='Tổng số lượng lỗ',digits= decimal_precision.get_precision('SO_LUONG'),compute='tinh_tong_tien', store=True)
    TONG_SL_KHOET = fields.Float(string='Tổng số lượng khoét',digits= decimal_precision.get_precision('SO_LUONG'),compute='tinh_tong_tien', store=True)
    
    TONG_THANH_TIEN_M2 = fields.Monetary(string='Tổng thành tiền m2', currency_field='base_currency_id',compute='tinh_tong_tien', store=True)
    TONG_THANH_TIEN_GIA_CONG = fields.Monetary(string='Tổng thành tiền gia công',currency_field='base_currency_id',compute='tinh_tong_tien', store=True)
    TONG_THANH_TIEN_TONG_CONG= fields.Monetary(string='Tổng thành tiền tổng',currency_field='base_currency_id',compute='tinh_tong_tien', store=True)

    @api.depends('ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien_hang = tong_tien_hang_quy_doi  = tong_tien_thue_gtgt = tong_tien_thue_gtgt_quy_doi = tong_tien_thanh_toan = tong_tien_thanh_toan_quy_doi = tong_chiet_khau = tong_chiet_khau_qd = 0
            phan_tram_thue = tien_gia_cong = 0

            sum_TONG_SL_TAM = 0
            sum_TONG_SL_M2 = 0
            sum_TONG_SL_MM = 0
            sum_TONG_SL_LO = 0
            sum_TONG_SL_KHOET = 0

            sum_TONG_THANH_TIEN_M2 = 0
            sum_TONG_THANH_TIEN_GIA_CONG = 0
            # sum_TONG_THANH_TIEN_TONG_CONG = 0
            
            for line in order.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                if line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT > phan_tram_thue:
                    phan_tram_thue= line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT
                tong_tien_hang +=line.THANH_TIEN
                tong_tien_hang_quy_doi +=line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt +=line.TIEN_THUE_GTGT
                tong_tien_thue_gtgt_quy_doi +=line.TIEN_THUE_GTGT_QUY_DOI
                tien_gia_cong += line.THANH_TIEN_GIA_CONG_1 + line.THANH_TIEN_GIA_CONG_2 + line.THANH_TIEN_GIA_CONG_3
                tong_chiet_khau +=line.TIEN_CHIET_KHAU
                tong_chiet_khau_qd +=line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt + tien_gia_cong
                tong_tien_thanh_toan_quy_doi = tong_tien_hang_quy_doi + tong_tien_thue_gtgt_quy_doi + tien_gia_cong # Giả thiết không có gia công quy đổi
                
                sum_TONG_SL_TAM +=line.LUONG
                sum_TONG_SL_M2 +=line.SO_LUONG
                sum_TONG_SL_MM +=line.SO_LUONG_GIA_CONG_1
                sum_TONG_SL_LO +=line.SO_LUONG_GIA_CONG_2
                sum_TONG_SL_KHOET +=line.SO_LUONG_GIA_CONG_3
                sum_TONG_THANH_TIEN_M2 +=line.THANH_TIEN
                sum_TONG_THANH_TIEN_GIA_CONG +=line.THANH_TIEN_GIA_CONG
                # sum_TONG_THANH_TIEN_TONG_CONG +=line.THANH_TIEN_TONG_CONG


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
                'TONG_TIEN_GIA_CONG': tien_gia_cong,

                'TONG_SL_TAM': sum_TONG_SL_TAM,
                'TONG_SL_M2': sum_TONG_SL_M2,
                'TONG_SL_MM': sum_TONG_SL_MM,
                'TONG_SL_LO': sum_TONG_SL_LO,
                'TONG_SL_KHOET': sum_TONG_SL_KHOET,
                'TONG_THANH_TIEN_M2': sum_TONG_THANH_TIEN_M2,
                'TONG_THANH_TIEN_GIA_CONG': sum_TONG_THANH_TIEN_GIA_CONG,
                # 'TONG_THANH_TIEN_TONG_CONG': sum_TONG_THANH_TIEN_TONG_CONG,
            })

    def tinh_cong_no_khach_hang(self, khach_hang_id, ngay):
        if not self.KHACH_HANG_ID:
            raise ValidationError('Bạn cần chọn khách hàng để xem chi tiết công nợ!')
        so_tien_no = super(ACCOUNT_EX_DON_DAT_HANG, self).tinh_cong_no_khach_hang(khach_hang_id, ngay)
            
        query = """
        SELECT sum(ddh."TONG_TIEN_THANH_TOAN") as tong_tien
        FROM account_ex_don_dat_hang ddh
        WHERE ddh."KHACH_HANG_ID" = %s 
            AND ddh."NGAY_DON_HANG" <= '%s'
            AND ddh."TINH_TRANG" != '3'
            AND (ddh."CHUNG_TU_BAN_HANG_ID" ISNULL
                OR NOT EXISTS(
                SELECT id FROM sale_document as sale
                WHERE sale.id =  ddh."CHUNG_TU_BAN_HANG_ID"
                AND sale.state = 'da_ghi_so'
                LIMIT 1
            )) """ % (khach_hang_id, ngay)
        result = self.execute(query)
        if result:
            so_tien_no += (result[0].get('tong_tien') or 0)
        return so_tien_no
        
    # -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

class ACCOUNT_EX_DON_DAT_HANG_REPORT(models.AbstractModel):
    _name = 'report.nhom_kinh.template_account_ex_don_dat_hang'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['account.ex.don.dat.hang'].browse(docids)
        for rec in records:
            rec.TONG_NO = rec.tinh_cong_no_khach_hang(rec.KHACH_HANG_ID.id, rec.NGAY_DON_HANG)
            rec.NO_CU = rec.TONG_NO - rec.TONG_TIEN_THANH_TOAN
        return {
            'doc_ids': docids,
            'doc_model': 'account.ex.don.dat.hang',
            'docs': records,
            'data': data,
        }
