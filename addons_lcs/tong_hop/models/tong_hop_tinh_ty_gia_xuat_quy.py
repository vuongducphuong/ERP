# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields,helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError
class TONG_HOP_TINH_TY_GIA_XUAT_QUY(models.Model):
    _name = 'tong.hop.tinh.ty.gia.xuat.quy'
    _description = ''
    _auto = False

    THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng ', help='Tháng ',required=True,default='3')
    NAM = fields.Integer(string='Năm', help='Năm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_TINH_TY_GIA_XUAT_QUY, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_TINH_TY_GIA_XUAT_QUY_CHI_TIET_NGOAI_TE_IDS = fields.One2many('tong.hop.tinh.ty.gia.xuat.quy.chi.tiet.ngoai.te', 'TY_GIA_XUAT_QUY_ID', string='Tính tỷ giá xuất quỹ chi tiết ngoại tệ')

    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_TINH_TY_GIA_XUAT_QUY, self).default_get(fields)
        arr_tinh_gia_xuat_quy_chi_tiet = []
        tinh_gia_xuat_quy_chi_tiet = self.env['res.currency'].search(['|',('MA_LOAI_TIEN','=','USD'),('MA_LOAI_TIEN','=','UAH')])
        rec['TONG_HOP_TINH_TY_GIA_XUAT_QUY_CHI_TIET_NGOAI_TE_IDS'] =[]
        for tinh_gia_xq_dt in tinh_gia_xuat_quy_chi_tiet:
             arr_tinh_gia_xuat_quy_chi_tiet +=[(0,0,{
                    'MA_LOAI_TIEN_ID':tinh_gia_xq_dt.id,
                    'TEN_LOAI_TIEN':tinh_gia_xq_dt.TEN_LOAI_TIEN,   
                })]

        rec['TONG_HOP_TINH_TY_GIA_XUAT_QUY_CHI_TIET_NGOAI_TE_IDS'] +=arr_tinh_gia_xuat_quy_chi_tiet
        thang = datetime.now().month
        rec['NAM'] = datetime.now().year
        rec['THANG'] = str(thang)
        return rec

    # @api.multi
    # def btn_thuc_hien(self):
    #     so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(self.get_context('NAM'), int(self.get_context('THANG')))
    #     tu_ngay = '%s-%s-%s' % (self.get_context('NAM'),int(self.get_context('THANG')),1)
    #     den_ngay = '%s-%s-%s' % (self.get_context('NAM'),int(self.get_context('THANG')),so_ngay_trong_thang)
    #     kiem_tra_ton_tai = self.kiem_tra_ton_tai(tu_ngay,den_ngay)
    #     if kiem_tra_ton_tai:
    #         thong_bao = 'Kỳ tính tỷ giá xuất quỹ tháng ' + self.get_context('THANG') + ' năm ' + str(self.get_context('NAM')) + ' đã có chứng từ xử lý chênh lệch tỷ giá xuất quỹ. /n Để tính lại tỷ giá xuất quy trong tháng, bạn phải xóa chứng từ trước đi.'
    #         raise ValidationError(thong_bao)
    #     id_tinh_ty_gia_xuat_quy = self.id
    #     action = self.env.ref('tong_hop.action_open_account_ex_chung_tu_nghiep_vu_khac_ty_gia_xuat_quy_form').read()[0]
    #     context ={
    #         'default_ID_TINH_TY_GIA_XUAT_QUY': id_tinh_ty_gia_xuat_quy,
    #         'default_LOAI_CHUNG_TU_TINH_GIA_XUAT_KHO'     :4017 ,
    #      }
    #     action['context'] = helper.Obj.merge(context, action.get('context'))
       
    #     return action

    def check_ton_tai(self, args):
        so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(args.get('nam'), int(args.get('thang')))
        tu_ngay = '%s-%s-%s' % (args.get('nam'),int(args.get('thang')),1)
        den_ngay = '%s-%s-%s' % (args.get('nam'),int(args.get('thang')),so_ngay_trong_thang)
        kiem_tra_ton_tai = self.kiem_tra_ton_tai(tu_ngay,den_ngay)
        arr_ket_qua = []
        da_ton_tai = False
        dict_chung_tu_ton_tai = {}
        if kiem_tra_ton_tai:
            da_ton_tai = True
            dict_chung_tu_ton_tai = {
                'ID_CHUNG_TU' : kiem_tra_ton_tai[0].get('ID_CHUNG_TU'),
                'MODEL_CHUNG_TU' : kiem_tra_ton_tai[0].get('MODEL_CHUNG_TU'),
            }
        arr_ket_qua.append(da_ton_tai)
        arr_ket_qua.append(dict_chung_tu_ton_tai)
        return arr_ket_qua

    def lay_du_lieu_ty_gia_xuat_quy(self, args):
        new_line = [[5]]
        arr_ket_qua = []
        thang = args.get('thang')
        nam = args.get('nam')
        so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(nam, int(thang))
        # tu_ngay = '%s-%s-%s' % (nam,int(thang),1)
        tu_ngay = datetime(nam,int(thang),1).strftime('%Y-%m-%d')
        # den_ngay = '%s-%s-%s' % (nam,int(thang),so_ngay_trong_thang)
        den_ngay = datetime(nam,int(thang),so_ngay_trong_thang).strftime('%Y-%m-%d')
        lay_du_lieu = self.lay_du_lieu(tu_ngay,den_ngay)
        co_chenh_lech = False
        if lay_du_lieu:
            co_chenh_lech = True
            for du_lieu in lay_du_lieu:
                tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', du_lieu.get('TK_NO'))],limit=1).id
                tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', du_lieu.get('TK_CO'))],limit=1).id
                tai_khoan_ngan_hang_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', du_lieu.get('TK_NGAN_HANG'))],limit=1).id
                loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', du_lieu.get('LOAI_TIEN_ID'))],limit=1).id
                new_line += [(0,0,{
						'DIEN_GIAI' : du_lieu.get('DIEN_GIAI'),
						'TK_NO_ID' : [tk_no_id,du_lieu.get('TK_NO')],
						'TK_CO_ID' : [tk_co_id,du_lieu.get('TK_CO')],
						'TK_NGAN_HANG_ID' : [tai_khoan_ngan_hang_id,du_lieu.get('TK_NGAN_HANG')],
						'currency_id' : [loai_tien_id,du_lieu.get('LOAI_TIEN_ID')],
						'SO_TIEN_DA_XUAT' : du_lieu.get('SO_TIEN_DA_XUAT'),
						'QUY_DOI_THEO_CT_GOC' : du_lieu.get('QUY_DOI_THEO_CT_GOC'),
						'TY_GIA_XUAT_QUY_BINH_QUAN' : du_lieu.get('TY_GIA_XUAT_QUY_BINH_QUAN'),
						'QUY_DOI_THEO_TY_GIA_XUAT_QUY' : du_lieu.get('QUY_DOI_THEO_TY_GIA_XUAT_QUY'),
						'SO_TIEN_QUY_DOI' : du_lieu.get('THANH_TIEN'),
                        
					})]
        
        dien_giai = 'Xử lý chênh lệch tỷ giá xuất quỹ tháng ' + str(thang) + ' năm ' + str(nam)
        du_lieu_master = {
            'DIEN_GIAI' : dien_giai,
            'THANG' : thang,
            'NAM' : nam,
            'NGAY_HACH_TOAN' : den_ngay,
            'NGAY_CHUNG_TU' : den_ngay,
        }

        arr_ket_qua.append(du_lieu_master)
        arr_ket_qua.append(new_line)
        arr_ket_qua.append(co_chenh_lech)
        return arr_ket_qua

    
    def kiem_tra_ton_tai(self,tu_ngay,den_ngay):
        params = {
            'TU_NGAY' : tu_ngay,
            'DEN_NGAY' : den_ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }
        query = """  
            DO LANGUAGE plpgsql $$ --Proc_GL_CheckExists_GLCAOutputRateResolveDiff
            DECLARE

                loai_chung_tu INT := 4017;

                chi_nhanh_id  INT := %(CHI_NHANH_ID)s;

                tu_ngay       TIMESTAMP := %(TU_NGAY)s;

                den_ngay      TIMESTAMP := %(DEN_NGAY)s;

                rec           RECORD;


            BEGIN


                DROP TABLE IF EXISTS TMP_KET_QUA;
                CREATE TEMP TABLE TMP_KET_QUA
                    AS

                SELECT
                    "id" AS "ID_CHUNG_TU",
                    'account.ex.chung.tu.nghiep.vu.khac' AS "MODEL_CHUNG_TU"
                FROM account_ex_chung_tu_nghiep_vu_khac
                WHERE "LOAI_CHUNG_TU" = loai_chung_tu
                    AND "CHI_NHANH_ID" = chi_nhanh_id
                    AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                LIMIT 1
                ;

            END $$

            ;

            SELECT *
            FROM TMP_KET_QUA
            ;
 
        """  
        return self.execute(query, params)

    def lay_du_lieu(self,tu_ngay,den_ngay):
        params = {
            'TU_NGAY' : tu_ngay,
            'DEN_NGAY' : den_ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }
        query = """   

            DO LANGUAGE plpgsql $$ --Proc_GL_DiffExchangeRate
            DECLARE


                chi_nhanh_id                   INT := %(CHI_NHANH_ID)s;

                tu_ngay                        TIMESTAMP := %(TU_NGAY)s;

                den_ngay                       TIMESTAMP := %(DEN_NGAY)s;

                --loai_tien                      INT := '3;8';

                debug                          BOOLEAN := FALSE;


                rec                            RECORD;

                TK_XU_LY_LAI_CHENH_LECH_TGXQ   VARCHAR;

                TK_XU_LY_LO_CHENH_LECH_TGXQ    VARCHAR;

                LOAI_TIEN_CHINH                INT;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI INT;

                PHAN_THAP_PHAN_TY_GIA          INT;
                ID_CHUNG_TU          INT;


            BEGIN


                SELECT value
                INTO TK_XU_LY_LAI_CHENH_LECH_TGXQ
                FROM ir_config_parameter
                WHERE key = 'he_thong.TK_XU_LY_LAI_CHENH_LECH_TGXQ'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO TK_XU_LY_LO_CHENH_LECH_TGXQ
                FROM ir_config_parameter
                WHERE key = 'he_thong.TK_XU_LY_LO_CHENH_LECH_TGXQ'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO LOAI_TIEN_CHINH
                FROM ir_config_parameter
                WHERE key = 'he_thong.LOAI_TIEN_CHINH'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_TY_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_TY_GIA'
                FETCH FIRST 1 ROW ONLY
                ;


                IF TK_XU_LY_LAI_CHENH_LECH_TGXQ IS NULL
                THEN
                    TK_XU_LY_LAI_CHENH_LECH_TGXQ = '515'
                    ;
                END IF
                ;


                IF TK_XU_LY_LO_CHENH_LECH_TGXQ IS NULL
                THEN
                    TK_XU_LY_LO_CHENH_LECH_TGXQ = '635'
                    ;
                END IF
                ;


                SELECT   "SO_TAI_KHOAN" INTO  TK_XU_LY_LAI_CHENH_LECH_TGXQ
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" LIKE TK_XU_LY_LAI_CHENH_LECH_TGXQ || '%%'
                    AND "LA_TK_TONG_HOP" = FALSE
                ;

                SELECT  "SO_TAI_KHOAN" INTO TK_XU_LY_LO_CHENH_LECH_TGXQ
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" LIKE TK_XU_LY_LO_CHENH_LECH_TGXQ || '%%'
                    AND "LA_TK_TONG_HOP" = FALSE
                ;

                ----------------------------------------------


                -- 	IF debug = 1
                -- 		SELECT @"SO_TIEN"DecimalDigits AS "SO_TIEN"DecimalDigits, PHAN_THAP_PHAN_TY_GIA AS "TY_GIA"DecimalDigit, %%(loai_tien_chinh)s
                -- ----------------------------------------------

                DROP TABLE IF EXISTS TMP_TAI_KHOAN
                ;

                CREATE TEMP TABLE TMP_TAI_KHOAN
                    AS

                        SELECT
                            A."SO_TAI_KHOAN"
                            , A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , C."id"
                            , C."PHEP_TINH_QUY_DOI"

                        FROM danh_muc_he_thong_tai_khoan AS A
                            CROSS JOIN res_currency AS C

                        WHERE (A."SO_TAI_KHOAN" LIKE '111%%'
                            OR A."SO_TAI_KHOAN" LIKE '112%%'
                            )
                            AND A."CO_HACH_TOAN_NGOAI_TE" = TRUE
                            AND c.id IN (3, 23)
                ;

                ----------------------------------------------


                ----------------------------------------------

                DROP TABLE IF EXISTS TMP_TY_GIA
                ;

                CREATE TEMP TABLE TMP_TY_GIA
                    AS
                        SELECT
                            GL."currency_id"
                            , GL."MA_TAI_KHOAN"
                            , A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , A."PHEP_TINH_QUY_DOI"
                            , CASE
                            WHEN A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                                THEN GL."TAI_KHOAN_NGAN_HANG_ID"
                            ELSE NULL
                            END                         AS "TK_NGAN_HANG"
                            , SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                    THEN GL."GHI_NO" - GL."GHI_CO"
                                ELSE 0
                                END)                    AS "SO_TIEN_OPN"
                            , SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                    THEN GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE"
                                ELSE 0
                                END)                    AS "SO_TIEN_NGUYEN_TE_OPN"
                            , SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    THEN GL."GHI_NO"
                                ELSE 0
                                END)                    AS "GHI_NO"
                            , SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    THEN GL."GHI_NO_NGUYEN_TE"
                                ELSE 0
                                END)                    AS "GHI_NO_NGUYEN_TE"
                            , SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    THEN GL."GHI_CO"
                                ELSE 0
                                END)                    AS "GHI_CO"
                            , SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    THEN GL."GHI_CO_NGUYEN_TE"
                                ELSE 0
                                END)                    AS "GHI_CO_NGUYEN_TE"
                            , CAST(0.0 AS DECIMAL(18, 4)) AS "TY_GIA_XUAT_QUY"
                            , CAST(0.0 AS DECIMAL(18, 4)) AS "DiffAmountAfterSolve"

                        FROM so_cai_chi_tiet AS GL
                            INNER JOIN TMP_TAI_KHOAN AS A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN" AND GL."currency_id" = A."id"
                        WHERE GL."NGAY_HACH_TOAN" <= den_ngay

                            AND GL."CHI_NHANH_ID" = chi_nhanh_id
                            AND GL."currency_id" <> LOAI_TIEN_CHINH
                        GROUP BY
                            GL."currency_id",
                            GL."MA_TAI_KHOAN",
                            A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            A."PHEP_TINH_QUY_DOI",
                            CASE
                            WHEN A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                                THEN GL."TAI_KHOAN_NGAN_HANG_ID"
                            ELSE NULL
                            END
                        HAVING
                            SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                    THEN GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE"
                                ELSE 0
                                END)
                            + SUM(CASE
                                WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    THEN GL."GHI_NO_NGUYEN_TE"
                                ELSE 0
                                END) <> 0
                ;


                UPDATE TMP_TY_GIA
                SET "TY_GIA_XUAT_QUY" = ROUND(CAST(COALESCE(CASE
                                                            WHEN "PHEP_TINH_QUY_DOI" = 'NHAN'
                                                                THEN ("SO_TIEN_OPN" + "GHI_NO") /
                                                                    CASE WHEN ("SO_TIEN_NGUYEN_TE_OPN" + "GHI_NO_NGUYEN_TE") <> 0
                                                                        THEN ("SO_TIEN_NGUYEN_TE_OPN" + "GHI_NO_NGUYEN_TE") END
                                                            ELSE
                                                                ("SO_TIEN_NGUYEN_TE_OPN" + "GHI_NO_NGUYEN_TE") /
                                                                CASE WHEN ("SO_TIEN_OPN" + "GHI_NO") <> 0
                                                                    THEN ("SO_TIEN_OPN" + "GHI_NO") END
                                                            END, 0) AS NUMERIC), PHAN_THAP_PHAN_TY_GIA)
                ;



                    -------------------------------------------------------------------


                    DROP TABLE IF EXISTS TMP_KET_QUA
                    ;

                    CREATE TEMP TABLE TMP_KET_QUA
                        AS
                            SELECT
                                GL."ID_CHUNG_TU"
                                , GL."MODEL_CHUNG_TU"
                                , GL."SO_CHUNG_TU"
                                , GL."NGAY_CHUNG_TU"
                                , GL."LOAI_CHUNG_TU"
                                , NULL                                    AS "DIEN_GIAI"
                                , GL."MA_TAI_KHOAN"
                                , NULL                                    AS "TK_KHO"
                                , NULL                                    AS "TK_CO"
                                , CASE
                                WHEN EX."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                                    THEN GL."TAI_KHOAN_NGAN_HANG_ID"
                                ELSE NULL
                                END                                     AS "TK_NGAN_HANG"
                                , EX."currency_id"                          AS "CashOutCurrencyID"
                                , COALESCE(SUM(GL."GHI_CO_NGUYEN_TE"), 0) AS "GHI_CO_NGUYEN_TE"
                                , COALESCE(SUM(GL."GHI_CO"), 0)           AS "GHI_CO"
                                , GL."TY_GIA"
                                , EX."TY_GIA_XUAT_QUY"
                                , COALESCE(SUM(CASE
                                            WHEN EX."PHEP_TINH_QUY_DOI" = 'NHAN'
                                                THEN ROUND(CAST((GL."GHI_CO_NGUYEN_TE" * EX."TY_GIA_XUAT_QUY")AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                                            ELSE CASE
                                                    WHEN EX."TY_GIA_XUAT_QUY" <> 0
                                                        THEN ROUND(CAST((GL."GHI_CO_NGUYEN_TE" / EX."TY_GIA_XUAT_QUY")AS NUMERIC), PHAN_THAP_PHAN_TY_GIA)
                                                    ELSE 0
                                                    END
                                            END), 0)                   AS "QUY_DOI_THEO_TY_GIA_XUAT_QUY"

                            FROM so_cai_chi_tiet AS GL
                                INNER JOIN TMP_TY_GIA AS EX ON GL."MA_TAI_KHOAN" = EX."MA_TAI_KHOAN"
                    AND GL."currency_id" = EX."currency_id"
                    AND (GL."TAI_KHOAN_NGAN_HANG_ID" = EX."TK_NGAN_HANG" OR EX."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = FALSE
                    )
                    WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                    AND "CHI_NHANH_ID" = chi_nhanh_id

                    GROUP BY
                        GL."ID_CHUNG_TU",
                        GL."MODEL_CHUNG_TU",
                        GL."SO_CHUNG_TU",
                        GL."SO_CHUNG_TU",
                        GL."NGAY_CHUNG_TU",
                        GL."LOAI_CHUNG_TU",
                        GL."MA_TAI_KHOAN",
                    CASE
                    WHEN EX."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE THEN GL."TAI_KHOAN_NGAN_HANG_ID"
                    ELSE NULL
                END,
                EX."currency_id",
                GL."TY_GIA",
                EX."TY_GIA_XUAT_QUY"
                HAVING COALESCE (SUM(GL."GHI_CO_NGUYEN_TE"), 0) <> 0
                ORDER BY
                GL."NGAY_CHUNG_TU" ASC,
                GL."SO_CHUNG_TU"
            ;


                --Tính toán số lệch của từng: Loại tiền.Tài khoản.Tài khoản ngân hàng
                UPDATE TMP_TY_GIA EX
                SET "DiffAmountAfterSolve" = "SO_TIEN_OPN" + "GHI_NO" - "GHI_CO" - S."SO_TIEN"
                FROM
                (
                SELECT
                "CashOutCurrencyID",
                "MA_TAI_KHOAN",
                "TK_NGAN_HANG",
                SUM("QUY_DOI_THEO_TY_GIA_XUAT_QUY" - "GHI_CO") AS "SO_TIEN"
                FROM TMP_KET_QUA
                GROUP BY
                "CashOutCurrencyID",
                "MA_TAI_KHOAN",
                "TK_NGAN_HANG"
                ) AS S WHERE EX."currency_id" = S."CashOutCurrencyID"
                AND EX."MA_TAI_KHOAN" = S."MA_TAI_KHOAN"
                AND (EX."TK_NGAN_HANG" = S."TK_NGAN_HANG" OR EX."TK_NGAN_HANG" IS NULL AND S."TK_NGAN_HANG" IS NULL )
                AND EX."SO_TIEN_NGUYEN_TE_OPN" + EX."GHI_NO_NGUYEN_TE" - EX."GHI_CO_NGUYEN_TE" = 0 ;




            FOR rec IN

                SELECT
                                            "currency_id" AS "currency_id"
                                            , "MA_TAI_KHOAN" AS "SO_TAI_KHOAN"
                                            , "TK_NGAN_HANG"  AS "TK_NGAN_HANG_ID"
                                            ,"DiffAmountAfterSolve"
                                        FROM TMP_TY_GIA
                                        WHERE "SO_TIEN_NGUYEN_TE_OPN" + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE" = 0
                        LOOP



                    IF rec."DiffAmountAfterSolve" <> 0
                    THEN
                        SELECT
                            ID_CHUNG_TU = "ID_CHUNG_TU"
                        FROM TMP_KET_QUA
                        WHERE "CashOutCurrencyID" = rec."currency_id"
                        AND "MA_TAI_KHOAN" =   rec."SO_TAI_KHOAN"
                        AND ("TK_NGAN_HANG" = rec."TK_NGAN_HANG_ID" OR "TK_NGAN_HANG" IS NULL AND rec."TK_NGAN_HANG_ID" IS NULL );




                        UPDATE TMP_KET_QUA
                        SET "QUY_DOI_THEO_TY_GIA_XUAT_QUY" = "QUY_DOI_THEO_TY_GIA_XUAT_QUY" + rec."DiffAmountAfterSolve"
                        WHERE "ID_CHUNG_TU" = ID_CHUNG_TU ;

                END IF ;
                END LOOP ;
            --     -------------------------------------------------

            DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                    ;

                    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                        AS

                SELECT
                    R."ID_CHUNG_TU"
                    , R."MODEL_CHUNG_TU"
                    , R."SO_CHUNG_TU"
                    , R."LOAI_CHUNG_TU"
                    , CASE
                    WHEN R."QUY_DOI_THEO_TY_GIA_XUAT_QUY" > R."GHI_CO"
                        THEN N'Xử lý chênh lệch tỷ giá lỗ của chứng từ ' || ' ' || R."SO_CHUNG_TU" || N' ngày '|| ' ' ||
                            TO_CHAR( R."NGAY_CHUNG_TU", 'dd/mm/yyyy')
                    ELSE N'Xử lý chênh lệch tỷ giá lãi của chứng từ ' || ' ' ||  R."SO_CHUNG_TU" || N' ngày '|| ' ' ||
                        TO_CHAR( R."NGAY_CHUNG_TU", 'dd/mm/yyyy')
                    END AS "DIEN_GIAI"
                    , CASE
                    WHEN R."QUY_DOI_THEO_TY_GIA_XUAT_QUY" > R."GHI_CO"
                        THEN TK_XU_LY_LO_CHENH_LECH_TGXQ --Nếu lỗ
                    ELSE R."MA_TAI_KHOAN" --Nếu lãi
                    END                                    AS "TK_NO"
                    , CASE
                    WHEN R."QUY_DOI_THEO_TY_GIA_XUAT_QUY" > R."GHI_CO"
                        THEN R."MA_TAI_KHOAN" --Nếu lỗ
                    ELSE TK_XU_LY_LAI_CHENH_LECH_TGXQ --Nếu lãi
                    END                                    AS "TK_CO"
                    , (select "SO_TAI_KHOAN" from danh_muc_tai_khoan_ngan_hang T WHERE  T.id =R."TK_NGAN_HANG")   AS "TK_NGAN_HANG"
                    , --TK Ngân hàng
                    (select "MA_LOAI_TIEN" from res_currency T WHERE  T.id =R."CashOutCurrencyID")                                 "LOAI_TIEN_ID"
                    , --Loại tiền
                    R."GHI_CO_NGUYEN_TE"                                 AS "SO_TIEN_DA_XUAT"
                    , --Số tiền đã xuất
                    R."GHI_CO"                            AS "QUY_DOI_THEO_CT_GOC"
                    , --Quy đổi theo chứng từ gốc
                    R."TY_GIA_XUAT_QUY"                  AS "TY_GIA_XUAT_QUY_BINH_QUAN"
                    , --Tỷ giá xuất quỹ bình quân
                    R."QUY_DOI_THEO_TY_GIA_XUAT_QUY"                                 "QUY_DOI_THEO_TY_GIA_XUAT_QUY"
                    , --Quy đổi theo tỷ giá xuất quỹ
                    0                                     AS "THANH_TIEN_NGUYEN_TE"
                    , ABS(R."QUY_DOI_THEO_TY_GIA_XUAT_QUY" - R."GHI_CO") AS "THANH_TIEN" --Số chênh lệch
                FROM TMP_KET_QUA R
                WHERE ABS(R."QUY_DOI_THEO_TY_GIA_XUAT_QUY" - R."GHI_CO") > 0 ;


            END $$

            ;

            SELECT *
            FROM TMP_KET_QUA_CUOI_CUNG
            ;

        """  
        return self.execute(query, params)