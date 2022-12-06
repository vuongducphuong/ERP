# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import datetime
from odoo.exceptions import ValidationError


class ASSET_KIEM_KE_TAI_SAN_CO_DINH(models.Model):
    _name = 'asset.kiem.ke'
    _description = 'Kiểm kê TSCĐ'
    _inherit = ['mail.thread']
    _order = "NGAY desc"

    MUC_DICH = fields.Char(string='Mục đich', help='Mục đich')
    KIEM_KE_DEN_NGAY_TSCD = fields.Date(string='Kiểm kê đến ngày', help='Kiểm kê đến ngày')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    SO = fields.Char(string='Số', help='Số', auto_num='asset_kiem_ke_SO')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    GIO = fields.Float(string='Giờ', help='Giờ')
    KET_LUAN = fields.Text(string='Kết luận', help='Kết luận')
    DA_XU_LY_KIEN_DINH = fields.Boolean(string='Đã xử lý kiến nghị', help='Đã xử lý kiến nghị')
    name = fields.Char(string='Name', help='Name',related='SO',store=True, oldname='NAME')

    ASSET_KIEM_KE_TAI_SAN_CO_DINH_THANH_VIEN_THAM_GIA_IDS = fields.One2many('asset.kiem.ke.thanh.vien.tham.gia', 'KIEM_KE_TAI_SAN_CO_DINH_ID', string='Kiểm kê tài sản cố định thành viên tham gia')
    ASSET_KIEM_KE_TAI_SAN_CO_DINH_TAI_SAN_IDS = fields.One2many('asset.kiem.ke.tai.san', 'KIEM_KE_TAI_SAN_CO_DINH_ID', string='Kiểm kê tài sản cố định tài sản')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    _sql_constraints = [
	('SO_CHUNG_TU_KK_uniq', 'unique ("SO")', 'Số chứng từ <<>> đã tồn tại!'),
	]


    @api.model
    def default_get(self, fields):
        rec = super(ASSET_KIEM_KE_TAI_SAN_CO_DINH, self).default_get(fields)
        current = datetime.now()
        rec['GIO'] = current.hour + 7 + current.minute/60 # GMT+7
        rec['LOAI_CHUNG_TU'] = 255
        ngay_kiem_ke = self.get_context('default_KIEM_KE_DEN_NGAY')

        tat_ca_tscd = self.lay_tat_ca_tscd(ngay_kiem_ke)
        arr_tai_san = []
        rec['ASSET_KIEM_KE_TAI_SAN_CO_DINH_TAI_SAN_IDS'] = []
        for line in tat_ca_tscd:
            if self.lay_tscd(line.get('TSCD_ID'),ngay_kiem_ke):
                tscd = self.lay_tscd(line.get('TSCD_ID'),ngay_kiem_ke)
                arr_tai_san += [(0, 0, {
                    'MA_TAI_SAN' : tscd[0].get('TSCD_ID'),
                    'TEN_TAI_SAN': tscd[0].get('TEN_TSCD'),
                    'DON_VI_SU_DUNG_ID': tscd[0].get('DON_VI_SU_DUNG_ID'),
                    'NGUYEN_GIA': tscd[0].get('NGUYEN_GIA'),
                    'GIA_TRI_TINH_KHAU_HAO': tscd[0].get('GIA_TRI_TINH_KHAU_HAO'),
                    'HAO_MON_LUY_KE' : tscd[0].get('GIA_TRI_HAO_MON_LUY_KE'),
                    'GIA_TRI_CON_LAI' : tscd[0].get('GIA_TRI_CON_LAI'),
                    'TON_TAI' : '0',
                    'CHAT_LUONG_HIEN_THOI' : '0',
                    'KIEN_NGHI_XU_LY' : '0',
                    })]

        rec['ASSET_KIEM_KE_TAI_SAN_CO_DINH_TAI_SAN_IDS'] += arr_tai_san

        return rec


    # @api.multi
    # def validate(self, vals, option=None):
        # ngay_khoa_so = str(self.lay_ngay_khoa_so())
        # if vals.get('NGAY') < ngay_khoa_so:
            # raise ValidationError("Ngày chứng từ không được nhỏ hơn ngày khóa sổ " +str(ngay_khoa_so)+ ". Vui lòng kiểm tra lại")


    @api.multi
    def btn_ghi_giam(self):
        if self.ASSET_KIEM_KE_TAI_SAN_CO_DINH_TAI_SAN_IDS:
            kien_nghi = False
            for line in self.ASSET_KIEM_KE_TAI_SAN_CO_DINH_TAI_SAN_IDS:
                if line.KIEN_NGHI_XU_LY == '1':
                    kien_nghi = True
            if kien_nghi == False:
                raise ValidationError('Không có TSCĐ được kiến nghị là ghi giảm, bạn không cần thực hiện chức năng xử lý ghi giảm')
        id_kiem_ke = self.id        
        action = self.env.ref('asset.action_open_asset_kiem_ke_btn_ghi_giam_form').read()[0]
        context = {'default_ID_KIEM_KE' : id_kiem_ke}
        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['target'] = 'new'
        return action




    def lay_tat_ca_tscd(self,ngay):

        params = {
            'NGAY': ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

         DO LANGUAGE plpgsql $$
        DECLARE

            v_ngay_hach_toan TIMESTAMP := %(NGAY)s;

            v_chi_nhanh_id   INT := %(CHI_NHANH_ID)s;


            rec              RECORD;


        BEGIN


            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
                AS
                    SELECT
                        FA."id"                   AS "TSCD_ID"
                        , FA."MA_TAI_SAN"           AS "MA_TSCD"
                        , FA."TEN_TAI_SAN"          AS "TEN_TSCD"
                        , FA."NGAY_BAT_DAU_TINH_KH" AS "NGAY_BAT_DAU_TINH_KH"
                        , FA."DON_VI_SU_DUNG_ID"    AS "DON_VI_ID"

                    FROM asset_ghi_tang AS FA
                        LEFT JOIN so_tscd_chi_tiet AS FL ON FA."id" = FL."TSCD_ID"
                        LEFT JOIN
                        (
                            SELECT "MA_TAI_SAN"
                            FROM asset_ghi_giam_tai_san AS FAD
                                INNER JOIN asset_ghi_giam AS FD ON FAD."TAI_SAN_CO_DINH_GHI_GIAM_ID" = FD."id"
                            WHERE ((FD."state" = 'da_ghi_so'

                            )

                                )
                                AND FD."NGAY_HACH_TOAN" <= v_ngay_hach_toan
                                AND FD."CHI_NHANH_ID" = v_chi_nhanh_id
                        ) AS FAD ON FA."id" = FAD."MA_TAI_SAN"
                    WHERE FL."CHI_NHANH_ID" = v_chi_nhanh_id
                        AND FL."NGAY_HACH_TOAN" <= v_ngay_hach_toan

                        AND FAD."MA_TAI_SAN" IS NULL /*Không hiển thị các TSCĐ đã ghi giảm rồi*/

                    GROUP BY
                        FA."id",
                        FA."MA_TAI_SAN",
                        FA."TEN_TAI_SAN",
                        FA."NGAY_BAT_DAU_TINH_KH",
                        FA."DON_VI_SU_DUNG_ID"


                    ORDER BY FA."MA_TAI_SAN"
            ;


        END $$

        ;

        SELECT *
        FROM TMP_KET_QUA


        """  
        
        return self.execute(query, params)


    
    def lay_tscd(self,tscd_id,ngay):

        params = {
            'NGAY_HACH_TOAN': ngay,
            'TSCD_ID' : tscd_id,
            'CHI_NHANH_ID' : self.get_chi_nhanh()
            }

        query = """   

         DO LANGUAGE plpgsql $$
        DECLARE
        ngay_hach_toan              DATE := %(NGAY_HACH_TOAN)s;
        tscd_id                     INTEGER := %(TSCD_ID)s;
        chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;

        BEGIN
        DROP TABLE IF EXISTS TMP_KET_QUA;
        CREATE TEMP TABLE TMP_KET_QUA
        AS
        SELECT  FAL.*
                FROM so_tscd_chi_tiet AS FAL
                WHERE FAL."TSCD_ID" = tscd_id
                AND FAL."CHI_NHANH_ID" = chi_nhanh_id
                AND FAL."NGAY_HACH_TOAN" <= ngay_hach_toan
                ORDER BY "NGAY_HACH_TOAN" DESC
        FETCH FIRST 1 ROW ONLY
        ;

        END $$;

        SELECT *
        FROM TMP_KET_QUA;



        """  
        
        return self.execute(query, params)