# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import datetime

class SUPPLY_KIEM_KE_CCDC(models.Model):
    _name = 'supply.kiem.ke'
    _description = 'Kiểm kê CCDC'
    _inherit = ['mail.thread']
    _order = "NGAY desc"

    MUC_DICH = fields.Char(string='Mục đích', help='Mục đích')
    KIEM_KE_DEN_NGAY_CCDC= fields.Date(string='Kiểm kê đến ngày', help='Kiểm kê đến ngày')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    SO = fields.Char(string='Số', help='Số', auto_num='supply_kiem_ke_SO')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    GIO = fields.Float(string='Giờ', help='Giờ')
    KET_LUAN = fields.Text(string='Kết luận', help='Kết luận')
    DA_XU_LY_KIEN_NGHI = fields.Boolean(string='Đã xử lý kiến nghị', help='Đã xử lý kiến nghị')
    name = fields.Char(string='Name', help='Name')
    

    SUPPLY_KIEM_KE_CCDC_CCDC_IDS = fields.One2many('supply.kiem.ke.cong.cu.dung.cu', 'KIEM_KE_CCDC_ID', string='Kiểm kê công cụ dụng cụ ccdc')
    SUPPLY_KIEM_KE_CCDC_TV_THAM_GIA_IDS = fields.One2many('supply.kiem.ke.thanh.vien.tham.gia', 'KIEM_KE_CCDC_ID', string='Kiểm kê công cụ dụng cụ tv tham gia')

    _sql_constraints = [
	('SO_KKCCDC_uniq', 'unique ("SO")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập lại số chứng từ!'),
	]

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    @api.model
    def create(self, values):
        if values.get('SO'):
            values['name'] = values.get('SO')
        result = super(SUPPLY_KIEM_KE_CCDC, self).create(values)

        return result

    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_KIEM_KE_CCDC, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 455
        current = datetime.now()
        rec['GIO'] = current.hour + 7 + current.minute/60 # GMT+7

        ngay_kiem_ke = self.get_context('default_KIEM_KE_DEN_NGAY')

        gi_tang = self.lay_ccdc(ngay_kiem_ke)
        rec['SUPPLY_KIEM_KE_CCDC_CCDC_IDS'] = []
        arr_tai_san = []

        for line in gi_tang:
            arr_tai_san += [(0, 0, {
                'MA_CCDC_ID' : line.get('CCDC_ID'),
                'TEN_CCDC': line.get('TEN_CCDC'),
                'DON_VI_SU_DUNG_ID': line.get('DON_VI_ID'),
                'DVT': line.get('DON_VI_TINH'),
                'TREN_SO_KE_TOAN': line.get('SO_LUONG'),
                'KIEM_KE' : line.get('SO_LUONG'),
                'SO_LUONG_TOT' : line.get('SO_LUONG'),
                'SO_LUONG_HONG' : 0,
                'KIEN_NGHI_XU_LY' : '2',
                'SO_LUONG_XU_LY' : 0,
                })]

        rec['SUPPLY_KIEM_KE_CCDC_CCDC_IDS'] += arr_tai_san

        return rec


    @api.multi
    def btn_ghi_giam(self):
        id_kiem_ke = self.id        
        action = self.env.ref('supply.action_open_supply_kiem_ke_btn_ghi_giam_form').read()[0]
        context = {'default_ID_KIEM_KE' : id_kiem_ke}
        action['context'] = helper.Obj.merge(context, action.get('context'))
        return action

    
    @api.multi
    def btn_ghi_tang(self):
        id_kiem_ke = self.id        
        action = self.env.ref('supply.action_open_supply_kiem_ke_btn_ghi_tang_form').read()[0]
        context = {'default_ID_KIEM_KE' : id_kiem_ke}
        action['context'] = helper.Obj.merge(context, action.get('context'))
        return action
    


    def lay_ccdc(self,ngay):
        params = {
            'NGAY':ngay, 
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE

                v_ngay_chung_tu                                     TIMESTAMP := %(NGAY)s;

                v_chi_nhanh_id                                     INT := %(CHI_NHANH_ID)s ;

                rec                                                RECORD;



            BEGIN



            DROP TABLE IF EXISTS TMP_KET_QUA
                ;
                CREATE TEMP TABLE TMP_KET_QUA


                    (
                    "CCDC_ID" INT ,
                    "MA_CCDC" VARCHAR(25) ,
                    "TEN_CCDC" VARCHAR(255) ,
                    "DON_VI_ID" INT ,
                    "SO_LUONG_GHI_TANG" DECIMAL(22, 8) ,
                    "SL_GIAM_TRONG_KY" DECIMAL(22, 8)
                    ) ;
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
                        WHERE   SL."NGAY_HACH_TOAN" <= v_ngay_chung_tu
                                AND SL."CHI_NHANH_ID" = v_chi_nhanh_id

                        GROUP BY SL."CCDC_ID" ,
                                SL."MA_CCDC" ,
                                SL."TEN_CCDC" ,
                                SL."DOI_TUONG_PHAN_BO_ID"
                ;

            DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;
                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG

                    (
                    "CCDC_ID" INT ,
                    "MA_CCDC" VARCHAR(25) ,
                    "TEN_CCDC" VARCHAR(255) ,
                    "DON_VI_ID" INT ,
                    "DVT" VARCHAR(20) ,
                    "SO_LUONG" DECIMAL(22, 8)
                    ) ;
                INSERT  INTO TMP_KET_QUA_CUOI_CUNG
                        ( "CCDC_ID" ,
                        "MA_CCDC" ,
                        "TEN_CCDC" ,
                        "DON_VI_ID" ,
                        "DVT" ,
                        "SO_LUONG"
                        )
                        SELECT  T."CCDC_ID" ,
                                T."MA_CCDC" ,
                                T."TEN_CCDC" ,
                                T."DON_VI_ID" ,
                                SI."DON_VI_TINH" ,
                                CAST(( T."SO_LUONG_GHI_TANG" - T."SL_GIAM_TRONG_KY" ) AS DECIMAL(18,
                                                                        4)) AS "SO_LUONG"
                        FROM    TMP_KET_QUA AS T
                                INNER JOIN supply_ghi_tang AS SI ON T."CCDC_ID" = SI."id" ;




            END $$

            ;
            SELECT  R.*
                FROM    TMP_KET_QUA_CUOI_CUNG AS R
                        INNER JOIN danh_muc_to_chuc AS OU ON R."DON_VI_ID" = OU."id"
                WHERE   R."SO_LUONG" > 0
                ORDER BY R."MA_CCDC" ,
                        OU."TEN_DON_VI" ;

        """  
        
        return self.execute(query, params)