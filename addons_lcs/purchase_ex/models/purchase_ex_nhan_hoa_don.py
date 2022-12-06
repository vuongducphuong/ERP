# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_NHAN_HOA_DON(models.Model):
    _name = 'purchase.ex.nhan.hoa.don'
    _description = ''
    _auto = False

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà CC', help='Tên nhà cung cấp')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    KY = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ', help='Kỳ',default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU = fields.Date(string='Từ', help='Từ ngày',required=True, default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS = fields.One2many('purchase.ex.nhan.hoa.don.chi.tiet', 'NHAN_HOA_DON_CHI_TIET_ID', string='Nhận hóa đơn chi tiết')

    @api.onchange('KY')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY, 'TU', 'DEN')

    def _validate(self): 
        params = self._context
        PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS = params['PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS'] if 'PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS' in params.keys() else 'False'
        if PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS=='False':
            raise ValidationError('Bạn phải chọn ít nhất 1 dòng chi tiết!')

    def action_view_result(self):

        self._validate()
        action = self.env.ref('purchase_ex.action_open_purchase_ex_nhan_hoa_don_form').read()[0]
        name = ''
        masothue = ''
        diachi = ''
        dien_giai = ''
        doi_tuong = self.env['res.partner'].search([('id', '=',self.get_context('DOI_TUONG_ID'))], limit=1)
        if doi_tuong:
            name = doi_tuong.HO_VA_TEN
            masothue = doi_tuong.MA_SO_THUE
            diachi = doi_tuong.DIA_CHI
            dien_giai = 'Mua hàng của công ty ' + str(name)
        # str1 = 'Thu tiền của '
        # tr_diengiai = str1 + str(name)
        # tk_no = 1
        # is_nguoi_nop = True
        # if self.get_context('PHUONG_THUC_THANH_TOAN') =='TIEN_MAT':
        #     tk_no = 188
        #     is_nguoi_nop = True
        # elif self.get_context('PHUONG_THUC_THANH_TOAN') =='TIEN_GUI':
        #     tk_no = 189
        #     is_nguoi_nop = False
        ct_mua_hang_ids = self.get_context('PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS')
        arr = []
        nhan_vien_mua_hang_id = 0
        so_chung_tu_mua_hang = ''
        for line in ct_mua_hang_ids:
            if line['AUTO_SELECT'] == 'True':
                id = line.get('ID_ct_muahang')
                chung_tu_mua_hang = self.env['purchase.document'].search([('id', '=', id)], limit=1)
                if len(ct_mua_hang_ids) == 1:
                    nhan_vien_mua_hang_id = chung_tu_mua_hang.NHAN_VIEN_ID.id
                    so_chung_tu_mua_hang = chung_tu_mua_hang.SO_CHUNG_TU_MUA_HANG
                ct_mua_hang_chitiet  =  self.env['purchase.document.line'].search([('order_id', '=', id)])
                for dl in ct_mua_hang_chitiet:
                    tkthue = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1331')],limit=1).id
                    tkcongno = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=',dl.TK_CO_ID.SO_TAI_KHOAN )],limit=1).id
                    giatrihhchuathue = dl.THANH_TIEN - dl.TIEN_CHIET_KHAU 
                    strDiengiaithue = 'Thuế GTGT' + '-' + str(dl.MA_HANG_ID.TEN)
                    arr += [(0, 0, {
                        'MA_HANG_ID' : dl.MA_HANG_ID.id,
                        'TEN_HANG' : dl.MA_HANG_ID.TEN,
                        'TK_THUE_ID' :tkthue,
                        'TK_CO_ID' : tkcongno,
                        'GIA_TRI_HHDV_CHUA_THUE' : giatrihhchuathue ,
                        'DIEN_GIAI_THUE' : strDiengiaithue,
                        'SO_CHUNG_TU_MUA_HANG' : so_chung_tu_mua_hang,
                        'ID_CHUNG_TU_GOC' : chung_tu_mua_hang.id,
                        'DON_VI_ID' : dl.DON_VI_ID.id,
                        'PHAN_TRAM_THUE_GTGT_ID' : dl.MA_HANG_ID.THUE_SUAT_GTGT_ID.id,
                        'TIEN_THUE_GTGT' : (dl.MA_HANG_ID.THUE_SUAT_GTGT_ID.PHAN_TRAM_THUE_GTGT*giatrihhchuathue)/100,
                        'TIEN_THUE_GTGT_QUY_DOI' : dl.TIEN_THUE_GTGT_QUY_DOI,
                        
                        'NHOM_HHDV_MUA_VAO_ID' : dl.NHOM_HHDV_ID.id,
                        'DON_MUA_HANG_ID' : dl.DON_MUA_HANG_ID.name,
                        'SO_CHUNG_TU_MUA_HANG' : chung_tu_mua_hang.SO_CHUNG_TU,
                        'CONG_TRINH_ID' : dl.CONG_TRINH_ID.id,
                        'HOP_DONG_MUA_ID' : dl.HOP_DONG_MUA_ID.id,
                        'MA_THONG_KE_ID' : dl.MA_THONG_KE_ID.id,
                        })]


        context = {
            'default_DOI_TUONG_ID': self.get_context('DOI_TUONG_ID'),
            'default_TEN_NHA_CUNG_CAP': name ,
            'default_MA_SO_THUE': masothue ,
            'default_DIA_CHI': diachi ,
            'default_NHAN_VIEN_ID': nhan_vien_mua_hang_id ,
            'default_DIEN_GIAI': dien_giai ,

            # 'default_IS_NGUOI_NOP': is_nguoi_nop,
            # 'default_LY_DO_NOP': tr_diengiai,
            # 'default_account_payment_ids': [(0, 0, {
            #     'amount':self.get_context('SO_TIEN'),
            #     'DIEN_GIAI_CHUNG':tr_diengiai,
            #     'tk_no_id' : tk_no,
            #     'tk_co_id' : 9,
            #     })],
            'default_HOA_DON_CHI_TIET_IDS' : arr,
            }

        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['options'] = {'clear_breadcrumbs': True}
        return action

    @api.onchange('DOI_TUONG_ID')
    def update_NHA_CUNG_CAP_ID(self):
       
        self.TEN_NHA_CUNG_CAP = self.env['res.partner'].search([('id', '=',self.get_context('DOI_TUONG_ID'))], limit=1).HO_VA_TEN
        

    def lay_du_lieu_hoa_don(self, args):
        new_line = [[5]]
        if args.get('doi_tuong_id'):
            ct_mua_hang_ids = self.lay_du_lieu_chung_tu(args.get('doi_tuong_id'),args.get('tu_ngay'),args.get('den_ngay'))
            if ct_mua_hang_ids:
                for ct in ct_mua_hang_ids:
                    new_line += [(0,0,{
                        'ID_ct_muahang' : ct.get('ID_CHUNG_TU'),
                        'NGAY_HACH_TOAN': ct.get('NGAY_HACH_TOAN'),
                        'NGAY_CHUNG_TU': ct.get('NGAY_CHUNG_TU'),
                        'SO_CHUNG_TU': ct.get('SO_CHUNG_TU'),
                        'LOAI_TIEN': ct.get('MA_LOAI_TIEN'),
                        'TY_GIA': ct.get('TY_GIA'),
                        'SO_TIEN': ct.get('TONG_TIEN_QUY_DOI'),
                        'DIEN_GIAI': ct.get('DIEN_GIAI_CHUNG'),
                        
                    })]
        return new_line

    def lay_du_lieu_chung_tu(self,doi_tuong,tu_ngay,den_ngay):
        params = {
            'TU_NGAY' : tu_ngay,
            'DEN_NGAY' : den_ngay,
            'DOI_TUONG_ID' : doi_tuong,
            }
        query = """   
                DO LANGUAGE plpgsql $$ DECLARE
                doi_tuong_id INTEGER := %(DOI_TUONG_ID)s;
                tu_ngay     DATE := %(TU_NGAY)s;
                den_ngay     DATE := %(DEN_NGAY)s;
                --   chung_tu_cu INTEGER :=1;
                --   id_hoa_don_mua_hang INTEGER := 1;


                BEGIN

                DROP TABLE IF EXISTS TMP_DT_ID;
                CREATE TEMP TABLE TMP_DT_ID(
                    "ID_CHUNG_TU" INTEGER
                );

                DROP TABLE IF EXISTS TMP_TBALE_1;
                CREATE TEMP TABLE TMP_TBALE_1
                AS
                    /*Chứng từ Mua hàng hóa*/
                    SELECT
                            PV.id AS "ID_CHUNG_TU" ,
                            PV."LOAI_CHUNG_TU" ,
                            PV."SO_CHUNG_TU" ,
                            PV."NGAY_HACH_TOAN" ,
                            PV."NGAY_CHUNG_TU" ,
                            PV."DOI_TUONG_ID" ,
                            PV."TEN_DOI_TUONG" ,
                            PV."TONG_TIEN_HANG" - "SO_TIEN_CHIET_KHAU" AS "TONG_TIEN_QUY_DOI" ,
                            CASE WHEN PV."SO_PHIEU_NHAP" IS NULL THEN PV."LY_DO_CHI"
                                ELSE PV."DIEN_GIAI_CHUNG"
                            END AS "DIEN_GIAI_CHUNG" ,
                            PV."currency_id" ,
                            PV."TY_GIA" ,
                            PV."NHAN_VIEN_ID" ,
                            PV."CHI_NHANH_ID",
                                PV."HAN_THANH_TOAN"
                    FROM    purchase_document AS PV
                            LEFT JOIN TMP_DT_ID AS DRI ON PV.id = DRI."ID_CHUNG_TU"
                    WHERE   ("DOI_TUONG_ID" = doi_tuong_id or doi_tuong_id ISNULL )
                            AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND PV."LOAI_HOA_DON" = '0'
                            AND PV."HOA_DON_MUA_HANG_ID" IS NULL
                            AND DRI."ID_CHUNG_TU" IS NULL
                            AND state = 'da_ghi_so'
                    UNION
                    SELECT
                            PV.id AS "ID_CHUNG_TU" ,
                            PV."LOAI_CHUNG_TU" ,
                            PV."SO_CHUNG_TU" ,
                            PV."NGAY_HACH_TOAN" ,
                            PV."NGAY_CHUNG_TU" ,
                            PV."DOI_TUONG_ID" ,
                            PV."TEN_DOI_TUONG" ,
                            PV."TONG_TIEN_HANG" - "SO_TIEN_CHIET_KHAU" AS "TONG_TIEN_QUY_DOI" ,
                            CASE WHEN PV."SO_PHIEU_NHAP" IS NULL THEN PV."LY_DO_CHI"
                                ELSE PV."DIEN_GIAI_CHUNG"
                            END AS "DIEN_GIAI_CHUNG" ,
                            PV."currency_id" ,
                            PV."TY_GIA" ,
                            PV."NHAN_VIEN_ID" ,
                            PV."CHI_NHANH_ID",
                                PV."HAN_THANH_TOAN"
                    FROM    purchase_document AS PV
                            INNER JOIN TMP_DT_ID AS DRI ON PV.id = DRI."ID_CHUNG_TU"
                    WHERE   ("DOI_TUONG_ID" = doi_tuong_id or doi_tuong_id ISNULL )
                            AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            /*VNTUAN 24.07.2015: chỉ lấy các chứng từ không kèm hóa đơn*/
                            AND PV."LOAI_HOA_DON" = '0'
                            AND state = 'da_ghi_so'
                ;

                END $$;

                SELECT a1."MA_LOAI_TIEN",a.*
                FROM TMP_TBALE_1 a
                LEFT JOIN res_currency a1 ON a."currency_id" = a1.id
        """  
        return self.execute(query, params)
