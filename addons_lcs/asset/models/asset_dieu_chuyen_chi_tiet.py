# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH_CHI_TIET(models.Model):
    _name = 'asset.dieu.chuyen.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN_ID = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản',related='MA_TAI_SAN_ID.TEN_TAI_SAN',store=True)
    TU_DON_VI = fields.Many2one('danh.muc.to.chuc',string='Từ đơn vị', help='Từ đơn vị')
    DEN_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đến đơn vị', help='Đến đơn vị')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tài khoản chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID = fields.Many2one('asset.dieu.chuyen', string='Điều chuyển tài khoản cố định', help='Điều chuyển tài khoản cố định', ondelete='cascade')

    @api.model
    def create(self, vals):
        if not vals.get('MA_TAI_SAN_ID'):
            raise ValidationError("Mã tài sản không được bỏ trống.")
        elif not vals.get('DEN_DON_VI_ID'):
            raise ValidationError("Đến đơn vị không được bỏ trống.")
        result = super(ASSET_DIEU_CHUYEN_TAI_SAN_CO_DINH_CHI_TIET, self).create(vals)
        return result

    @api.onchange('MA_TAI_SAN_ID')
    def capnhattaisancodinh(self):
        if self.MA_TAI_SAN_ID:
            self.TEN_TAI_SAN = self.MA_TAI_SAN_ID.name
            tscd = self.lay_du_lieu_phan_bo(self.MA_TAI_SAN_ID.id)
            if tscd:
                self.TU_DON_VI = tscd[0].get('DON_VI_SU_DUNG_ID')



    def lay_du_lieu_phan_bo(self,tscd_id):
        record = []
        params = {
            'TSCD_ID': tscd_id,
            }

        query = """   

            SELECT
  CASE WHEN (
SELECT COUNT(FTD.id)
                     FROM   asset_dieu_chuyen_chi_tiet AS FTD
                            INNER JOIN asset_dieu_chuyen AS FT ON FTD."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = FT.id
                     WHERE  FTD."MA_TAI_SAN_ID" = %(TSCD_ID)s
                   ) > 0
  THEN (
    SELECT
                            FTD."DEN_DON_VI_ID"
                    FROM    asset_dieu_chuyen_chi_tiet AS FTD
                            INNER JOIN asset_dieu_chuyen AS FT ON FTD."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = FT.id
                    WHERE   FTD."MA_TAI_SAN_ID" = %(TSCD_ID)s
                    ORDER BY FT."NGAY" DESC ,
                            FT."BIEN_BAN_GIAO_NHAN_SO" DESC
    FETCH FIRST 1 ROW ONLY
  )
  ELSE (
    SELECT  FA."DON_VI_SU_DUNG_ID"
                    FROM    asset_ghi_tang AS FA
                     WHERE   FA.id = %(TSCD_ID)s
  )
    END

        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'DON_VI_SU_DUNG_ID': line.get('DON_VI_SU_DUNG_ID', ''), 
            })
        
        return record