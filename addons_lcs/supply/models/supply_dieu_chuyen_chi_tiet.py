# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class SUPPLY_DIEU_CHUYEN_CCDC_CHI_TIET(models.Model):
    _name = 'supply.dieu.chuyen.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC_ID = fields.Many2one('supply.ghi.tang', string='Mã CCDC', help='Mã công cụ dụng cụ')
    TEN_CCDC = fields.Char(string='Tên CCDC', help='Tên công cụ dụng cụ',related='MA_CCDC_ID.TEN_CCDC')
    TU_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Từ đơn vị', help='Từ đơn vị')
    DEN_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đến đơn vị', help='Đến đơn vị')
    SO_LUONG_DANG_DUNG = fields.Float(string='Số lượng đang dùng', help='Số lượng đang dùng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DIEU_CHUYEN = fields.Float(string='Số lượng điều chuyển', help='Số lượng điều chuyển', digits=decimal_precision.get_precision('SO_LUONG'))
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản CP ', help='Tài khoản chi phí ')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí', oldname='KHOAN_MUC_CHI_PHI_ID')
    DOI_TUONG_TONG_HOP_CHI_PHI_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tổng hợp chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID = fields.Many2one('supply.dieu.chuyen.cong.cu.dung.cu', string='Điều chuyển ccdc chi tiết id', help='Điều chuyển ccdc chi tiết id', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NGAY = fields.Date(string='Ngày', help='Ngày',related='DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID.NGAY' )
    sequence = fields.Integer()

    THU_TU_SAP_XEP = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết', help='SortOrder' )


    # SO_LUONG_DANG_DUNG = 1 
    @api.onchange('MA_CCDC_ID')
    def onchange_MA_CCDC_ID(self):
        self.thay_doi_thong_tin('ccdc')

    @api.onchange('TU_DON_VI_ID')
    def onchange_TU_DON_VI_ID(self):
        self.thay_doi_thong_tin('tu_don_vi')

    def thay_doi_thong_tin(self,truong_onchange):
        if self.MA_CCDC_ID:
            record = self.lay_du_lieu_ccdc(self.NGAY,self.MA_CCDC_ID.id)
            if len(record) == 0:
                raise ValidationError("Công cụ dụng cụ này không có mã đơn vị. Vui lòng kiểm tra lại bên ghi tăng")
            else:
                dict_don_vi = {}
                ten_ccdc = record[0].get('TEN_CCDC')
                so_luong = record[0].get('SO_LUONG')
                tu_don_vi = record[0].get('DON_VI_ID')
                if self.TU_DON_VI_ID:
                    for line in record:
                        dict_don_vi[line.get('DON_VI_ID')] = line.get('TEN_DON_VI')
                        if line.get('DON_VI_ID') == self.TU_DON_VI_ID.id:
                            ten_ccdc = line.get('TEN_CCDC')
                            so_luong = line.get('SO_LUONG')
                            tu_don_vi = line.get('DON_VI_ID')
                            return
                if truong_onchange == 'ccdc':
                    self.TEN_CCDC = ten_ccdc
                    self.TU_DON_VI_ID = tu_don_vi
                    self.SO_LUONG_DANG_DUNG = so_luong
                elif truong_onchange == 'tu_don_vi':
                    if self.TU_DON_VI_ID.id not in dict_don_vi:
                        thong_bao = 'Công cụ dụng cụ <'  + str(self.MA_CCDC_ID.TEN_CCDC) + '> chỉ được phân bổ cho đơn vị <' + ",".join(dict_don_vi.values()) + '> Bạn vui lòng chọn đơn vị khác hoặc kiểm tra lại ghi tăng'
                        raise ValidationError(thong_bao)
                    self.TEN_CCDC = ten_ccdc
                    self.SO_LUONG_DANG_DUNG = so_luong

    
    def lay_du_lieu_ccdc(self,ngay,ccdc_id):
        params = {
            'NGAY_CHUNG_TU' : ngay,
            'CCDC_ID' : ccdc_id,
            }
        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
                v_ngay_chung_tu                                         TIMESTAMP := %(NGAY_CHUNG_TU)s;

                --%%(TU_NGAY)s

                v_ccdc_id                                     INT := %(CCDC_ID)s;

                rec                                                RECORD;



            BEGIN



            DROP TABLE IF EXISTS TMP_KET_QUA
                ;
                CREATE TABLE TMP_KET_QUA

                    (
                    "CCDC_ID" INT ,
                    "MA_CCDC" VARCHAR(25) ,
                    "TEN_CCDC" VARCHAR(255) ,
                    "DON_VI_ID" INT ,
                    "SO_LUONG_GHI_TANG" DECIMAL(22, 8) ,
                    "SL_GIAM_TRONG_KY" DECIMAL(22, 8)
                    );
                INSERT  INTO TMP_KET_QUA
                        ( "CCDC_ID" ,
                        "MA_CCDC" ,
                        "TEN_CCDC" ,
                        "DON_VI_ID" ,
                        "SO_LUONG_GHI_TANG" ,
                        "SL_GIAM_TRONG_KY"               
                        )
                        SELECT  SL."CCDC_ID" ,
                                SL."MA_CCDC" ,
                                SL."TEN_CCDC" ,
                                SL."DOI_TUONG_PHAN_BO_ID" ,
                                SUM(SL."SO_LUONG_GHI_TANG") ,
                                SUM(SL."SO_LUONG_GHI_GIAM")
                        FROM    so_ccdc_chi_tiet AS SL
                        WHERE   SL."CCDC_ID" = v_ccdc_id
                        AND "NGAY_CHUNG_TU" <=v_ngay_chung_tu
                        GROUP BY SL."CCDC_ID" ,
                                SL."MA_CCDC" ,
                                SL."TEN_CCDC" ,
                                SL."DOI_TUONG_PHAN_BO_ID" ;

                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;
                CREATE TABLE TMP_KET_QUA_CUOI_CUNG
                    AS
                                
                SELECT  T."CCDC_ID" ,
                        T."MA_CCDC" ,
                        T."TEN_CCDC" ,
                        T."DON_VI_ID" ,
                        OU."MA_DON_VI" ,
                        OU."TEN_DON_VI" ,
                        OU."parent_id",
                        OU."ISPARENT",
                        OU.active,
                        T."SO_LUONG_GHI_TANG" - T."SL_GIAM_TRONG_KY" AS "SO_LUONG"
                FROM    TMP_KET_QUA AS T
                        LEFT JOIN danh_muc_to_chuc AS OU ON T."DON_VI_ID" = OU."id"
                WHERE   ( "SO_LUONG_GHI_TANG" - "SL_GIAM_TRONG_KY" > 0 )
                ORDER BY "MA_CCDC"     ;

            END $$

            ;
            SELECT  * FROM TMP_KET_QUA_CUOI_CUNG
            ;

        """  
        return self.execute(query, params)





    
        