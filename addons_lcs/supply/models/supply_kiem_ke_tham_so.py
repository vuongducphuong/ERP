# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class SUPPLY_KIEM_KE_CCDC_THAM_SO(models.Model):
    _name = 'supply.kiem.ke.tham.so'
    _description = ''
    _auto = False

    KIEM_KE_DEN_NGAY = fields.Date(string='Kiểm kê đến ngày', help='Kiểm kê đến ngày',default=fields.Datetime.now)
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    def action_view_result(self):
        ngay_bat_dau_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
        ngay_tren_form = self.get_context('KIEM_KE_DEN_NGAY')
        ngay_thuc_hien_kiem_ke = datetime.strptime(ngay_tren_form, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        if ngay_thuc_hien_kiem_ke < ngay_bat_dau_tai_chinh: #Mạnh sửa bug2355 : Thêm đoạn code này để check xem nếu ngày thực hiện kiểm kê nhỏ hơn ngày tài chính thì thông báo lỗi cho người dùng.
            raise ValidationError('Ngày kiểm kê phải lớn hơn hoặc bằng ngày bắt đầu hạch toán.')
        action = self.env.ref('supply.action_open_supply_kiem_ke_tham_so_form').read()[0]

        # gi_tang = self.lay_ccdc(self.get_context('KIEM_KE_DEN_NGAY'))

        # arr_tai_san = []

        # for line in gi_tang:
        #     arr_tai_san += [(0, 0, {
        #         'MA_CCDC_ID' : line.get('CCDC_ID'),
        #         'TEN_CCDC': line.get('TEN_CCDC'),
        #         'DON_VI_SU_DUNG_ID': line.get('DOI_TUONG_PHAN_BO_ID'),
        #         'DVT': line.get('DON_VI_TINH'),
        #         'TREN_SO_KE_TOAN': line.get('SO_LUONG'),
        #         'KIEM_KE' : line.get('SO_LUONG'),
        #         'SO_LUONG_TOT' : line.get('SO_LUONG'),
        #         'SO_LUONG_HONG' : 0,
        #         'KIEN_NGHI_XU_LY' : '2',
        #         'SO_LUONG_XU_LY' : 0,
        #         })]

        context = {
            'default_KIEM_KE_DEN_NGAY': self.get_context('KIEM_KE_DEN_NGAY'),
            # 'default_SUPPLY_KIEM_KE_CCDC_CCDC_IDS' : arr_tai_san,
            }

        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['options'] = {'clear_breadcrumbs': True}
        return action



    def lay_ccdc(self,ngay):
        params = {
            'NGAY':ngay, 
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
            ngay                     DATE := %(NGAY)s;
            chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;

            BEGIN
            DROP TABLE IF EXISTS TMP_KET_QUA;
            CREATE TEMP TABLE TMP_KET_QUA
                AS
                SELECT  R.*
                FROM    (

                            SELECT  T."CCDC_ID" ,
                                T."MA_CCDC" ,
                                T."TEN_CCDC" ,
                                T."DOI_TUONG_PHAN_BO_ID" ,
                                SI."DON_VI_TINH" ,
                                ( coalesce(T."SO_LUONG_GHI_TANG",0) - coalesce(T."SO_LUONG_GHI_GIAM",0) ) AS  "SO_LUONG"
                        FROM    (

                                SELECT  SL."CCDC_ID" ,
                                        SL."MA_CCDC" ,
                                        SL."TEN_CCDC" ,
                                        SL."DOI_TUONG_PHAN_BO_ID" ,
                                        SUM(SL."SO_LUONG_GHI_TANG"  ) AS "SO_LUONG_GHI_TANG",
                                        SUM(SL."SO_LUONG_GHI_GIAM") AS "SO_LUONG_GHI_GIAM"
                                FROM    so_ccdc_chi_tiet AS SL
                                WHERE
                                        SL."NGAY_HACH_TOAN" <= ngay
                                        AND SL."CHI_NHANH_ID" = chi_nhanh_id
                                GROUP BY SL."CCDC_ID" ,
                                        SL."MA_CCDC" ,
                                        SL."TEN_CCDC" ,
                                        SL."DOI_TUONG_PHAN_BO_ID"

                                ) AS T
                                INNER JOIN supply_ghi_tang AS SI ON T."CCDC_ID" = SI.id

                        ) AS R
                        INNER JOIN danh_muc_to_chuc AS OU ON R."DOI_TUONG_PHAN_BO_ID" = OU.id
                WHERE   R."SO_LUONG" > 0
                ORDER BY R."MA_CCDC" ,
                        OU."TEN_DON_VI"
            ;

            END $$;

            SELECT *
            FROM TMP_KET_QUA;


        """  
        
        return self.execute(query, params)
