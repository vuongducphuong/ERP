# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import datetime

class BAO_CAO_CHI_PHI_DU_KIEN_THEO_DON_DAT_HANG(models.Model):
    _name = 'bao.cao.chi.phi.du.kien.theo.don.dat.hang'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuôc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    TU_NGAY = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now,required='True')
    DEN_NGAY = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)

    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    LIST_TEN_NHOM_VTHH = fields.Char(string='Tên nhóm', help='Tên nhóm')
    TEN_NGUYEN_VAT_LIEU = fields.Char(string='Tên nguyên vật liệu', help='Tên nguyên vật liệu')
    DVT = fields.Char(string='Đvt', help='Đvt')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_THANH_PHAM = fields.Float(string='Số lượng thành phẩm', help='Số lượng thành phẩm', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_TON = fields.Float(string='Số lượng tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('SO_LUONG'))    
    SO_LUONG_CON_THIEU = fields.Float(string='Số lượng còn thiếu', help='Số lượng còn thiếu', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'))
    GIA_BAN = fields.Float(string='Giá bán', help='Giá bán',digits=decimal_precision.get_precision('VND'))
    NAME = fields.Char(string='Name', help='Name')
    DON_DAT_HANG_IDS = fields.One2many('account.ex.don.dat.hang')
    PHAN_TRAM = fields.Float(string='% Cost', help='% Cost')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    LA_TONG_HOP = fields.Boolean()

    THONG_KE_THEO = fields.Selection([('CHI_PHI_DU_KIEN', 'Chi phí dự kiến'),('CHI_PHI_THEO_NGUYEN_VAT_LIEU', 'Số lượng cần mua theo nguyên vật liệu'),('CHI_PHI_THEO_NGUYEN_VAT_LIEU_VA_DON_HANG', 'Số lượng cần mua theo nguyên vật liệu và đơn hàng'),], string='Thống kê theo', help='Thống kê theo',default='CHI_PHI_DU_KIEN',required=True)
    RowNumber = fields.Integer(string='STT', help='Số thứ tự')
    @api.onchange('TU_NGAY','DEN_NGAY','CHI_NHANH_ID')
    def _onchange_TU_NGAY(self):
        if self.TU_NGAY and self.DEN_NGAY:
            if self.CHI_NHANH_ID.id:
                don_dat_hang_ids =  self.env['account.ex.don.dat.hang'].search([('CHI_NHANH_ID','=',self.CHI_NHANH_ID.id),('NGAY_DON_HANG','>=',self.TU_NGAY),('NGAY_DON_HANG','<=',self.DEN_NGAY)])
            else:
                don_dat_hang_ids =  self.env['account.ex.don.dat.hang'].search([('NGAY_DON_HANG','>=',self.TU_NGAY),('NGAY_DON_HANG','<=',self.DEN_NGAY)])
            
            if don_dat_hang_ids:
                self.DON_DAT_HANG_IDS = don_dat_hang_ids.ids

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_CHI_PHI_DU_KIEN_THEO_DON_DAT_HANG, self).default_get(fields_list)
        chi_nhanh_id = self.get_chi_nhanh()
        # don_dat_hang_ids =  self.env['account.ex.don.dat.hang'].search([('CHI_NHANH_ID','=',chi_nhanh_id)])
        # if don_dat_hang_ids:
        #     result['DON_DAT_HANG_IDS'] = don_dat_hang_ids.ids
        result['CHI_NHANH_ID'] = chi_nhanh_id
        return result
 
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        DON_DAT_HANG_IDS = [mh_mh['id'] for mh_mh in params['DON_DAT_HANG_IDS']]  if 'DON_DAT_HANG_IDS' in params.keys() and params['DON_DAT_HANG_IDS'] != 'False' else None

        params_sql = {
            'DON_DAT_HANG_IDS':DON_DAT_HANG_IDS,
            'limit': limit,
            'offset': offset, 
        }
        if THONG_KE_THEO=='CHI_PHI_DU_KIEN' :
            return self._lay_bao_cao_chi_phi_du_kien(params_sql)
           
        # Thống kê theo chi phí theo nguyên vật liệu
        elif THONG_KE_THEO=='CHI_PHI_THEO_NGUYEN_VAT_LIEU' :
            return self._lay_bao_cao_chi_phi_theo_nguyen_vat_lieu(params_sql)
            
        # Thống kê theo chi phí theo nguyên vật liệu và đơn hàng
        elif THONG_KE_THEO=='CHI_PHI_THEO_NGUYEN_VAT_LIEU_VA_DON_HANG' :
            return self._lay_bao_cao_chi_phi_theo_nguyen_vat_lieu_va_don_hang(params_sql)

    def _lay_bao_cao_chi_phi_du_kien(self, params_sql):      
        record = []
        query = """
        
SELECT *
FROM (
         --- co nguyen vat lieu
         SELECT
             ddhct."sequence"
             , ddhct.id                                                      AS "ID_CHI_TIET"
             , dmnvl.id                                                      AS "DINH_MUC_NVL_ID"
             , dmnvl."sequence"                                              AS "DINH_MUC_NVL_SEQ"
             , ddh."SO_DON_HANG"
             , vthh."TEN"                                                    AS "TEN_THANH_PHAM"
             , vthhnvl."TEN"                                                 AS "TEN_NGUYEN_VAT_LIEU"
             , dvt."DON_VI_TINH"                                             AS "DVT"
             , coalesce(dmnvl."SO_LUONG", 0) * coalesce(ddhct."SO_LUONG", 0) AS "SO_LUONG"
             , coalesce(vthhnvl."DON_GIA_MUA_CO_DINH", 0)                    AS "DON_GIA"
             , coalesce(dmnvl."SO_LUONG", 0) * coalesce(vthhnvl."DON_GIA_MUA_CO_DINH", 0) *
               coalesce(ddhct."SO_LUONG", 0)                                 AS "THANH_TIEN"
             , coalesce(ddhct."THANH_TIEN", 0)                               AS "GIA_BAN"
             , coalesce(ddhct."SO_LUONG", 0)                                 AS "SO_LUONG_THANH_PHAM"
             , ddh.id                                                        AS "ID_GOC"
             , 'account.ex.don.dat.hang'                                     AS "MODEL_GOC"
         FROM account_ex_don_dat_hang AS ddh
             INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
             INNER JOIN danh_muc_vat_tu_hang_hoa vthh ON ddhct."MA_HANG_ID" = vthh.id
             INNER JOIN danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl
                 ON vthh.id = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID"
             LEFT JOIN danh_muc_vat_tu_hang_hoa vthhnvl ON dmnvl."MA_NGUYEN_VAT_LIEU_ID" = vthhnvl.id
             LEFT JOIN danh_muc_don_vi_tinh dvt ON vthhnvl."DVT_CHINH_ID" = dvt.id
         WHERE 
            (ddh.id = any(%(DON_DAT_HANG_IDS)s)) 
         UNION
         -- khong co nguyen vat lieu
         SELECT
             ddhct."sequence"
             , ddhct.id                                                                AS "ID_CHI_TIET"
             , 0                                                                       AS "DINH_MUC_NVL_ID"
             , 0                                                                       AS "DINH_MUC_NVL_SEQ"
             , ddh."SO_DON_HANG"
             , vthh."TEN"                                                              AS "TEN_THANH_PHAM"
             , vthh."TEN"                                                              AS "TEN_NGUYEN_VAT_LIEU"
             , dvt."DON_VI_TINH"                                                       AS "DVT"
             , coalesce(ddhct."SO_LUONG", 0)                                           AS "SO_LUONG"
             , coalesce(vthh."DON_GIA_MUA_CO_DINH", 0)                                 AS "DON_GIA"
             , coalesce(vthh."DON_GIA_MUA_CO_DINH", 0) * coalesce(ddhct."SO_LUONG", 0) AS "THANH_TIEN"
             , coalesce(ddhct."THANH_TIEN", 0)                                         AS "GIA_BAN"
             , coalesce(ddhct."SO_LUONG", 0)                                           AS "SO_LUONG_THANH_PHAM"
             , ddh.id                                                                  AS "ID_GOC"
             , 'account.ex.don.dat.hang'                                               AS "MODEL_GOC"
         FROM account_ex_don_dat_hang AS ddh
             INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
             INNER JOIN danh_muc_vat_tu_hang_hoa vthh ON ddhct."MA_HANG_ID" = vthh.id
             LEFT JOIN danh_muc_don_vi_tinh dvt ON vthh."DVT_CHINH_ID" = dvt.id
         WHERE NOT exists(SELECT 1
                          FROM danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl
                          WHERE vthh.id = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID")
                AND (ddh.id = any(%(DON_DAT_HANG_IDS)s)) 
     ) a
ORDER BY
    "sequence",
    "ID_CHI_TIET",
    "DINH_MUC_NVL_ID",
    "DINH_MUC_NVL_SEQ",
    "TEN_NGUYEN_VAT_LIEU"
;
           

        """
        # cr.execute(query)

        record = self.execute(query, params_sql)

        dict_don_hang = {}
        for line in record:
            key_so_don_hang = line.get('SO_DON_HANG')
            key_ten_thanh_pham = line.get('TEN_THANH_PHAM')

            if key_so_don_hang not in dict_don_hang:
                dict_don_hang[key_so_don_hang] = {}
            
            if key_ten_thanh_pham not in dict_don_hang[key_so_don_hang]:
                dict_don_hang[key_so_don_hang][key_ten_thanh_pham] = []
            
            dict_don_hang[key_so_don_hang][key_ten_thanh_pham] += [line]

        dict_cuoi = []

        for don_hang in dict_don_hang:
            tong_tien_don_dat_hang = 0
            tong_tien_gia_ban = 0
            id_goc = None
            model_goc = None
            
            dong_theo_don_dat_hang = {'TEN_THANH_PHAM' : None,
                                        'SO_DON_HANG' : don_hang,
                                        'TEN_NGUYEN_VAT_LIEU' : None,
                                        'DVT' : None,
                                        'SO_LUONG' : None,
                                        'SO_LUONG_THANH_PHAM' : None,
                                        'DON_GIA' : None,
                                        'THANH_TIEN' : None,
                                        'GIA_BAN' : None,
                                        'PHAN_TRAM' : None,
                                        'LA_TONG_HOP' : True,
                                    }
            dict_cuoi += [dong_theo_don_dat_hang]

            for thanh_pham in dict_don_hang[don_hang]:
                gia_ban = 0
                tong_chi_phi = 0
                dong_thanh_pham = {'TEN_THANH_PHAM' : thanh_pham,
                                    'SO_DON_HANG' : None,
                                    'TEN_NGUYEN_VAT_LIEU' : None,
                                    'DVT' : None,
                                    'SO_LUONG' : None,
                                    'SO_LUONG_THANH_PHAM' : None,
                                    'DON_GIA' : None,
                                    'THANH_TIEN' : None,
                                    'GIA_BAN' : None,
                                    'PHAN_TRAM' : None,
                                    'LA_TONG_HOP' : True,
                                }
                dict_cuoi += [dong_thanh_pham]

                #Lấy giá trị id gốc, model gốc
                id_goc = dict_don_hang[don_hang][thanh_pham][0].get('ID_GOC')
                model_goc = dict_don_hang[don_hang][thanh_pham][0].get('MODEL_GOC')

                for chi_tiet in dict_don_hang[don_hang][thanh_pham]:
                    gia_ban = chi_tiet.get('GIA_BAN')
                    tong_chi_phi += chi_tiet.get('THANH_TIEN')
                    key_chung = str(chi_tiet.get('SO_DON_HANG')) +','+ str(chi_tiet.get('TEN_THANH_PHAM')) +','+ str(chi_tiet.get('TEN_NGUYEN_VAT_LIEU'))
                    chi_tiet['GIA_BAN'] = None
                    chi_tiet['SO_DON_HANG'] = None
                    chi_tiet['TEN_THANH_PHAM'] = None
                    chi_tiet['ID_GOC'] = None
                    chi_tiet['MODEL_GOC'] = None
                    chi_tiet['LA_TONG_HOP'] = False
                    if key_chung not in dict_cuoi:
                        dict_cuoi.append(chi_tiet)
                # gán lại giá trị cho dòng thành phẩm
                dong_thanh_pham['ID_GOC'] = None
                dong_thanh_pham['MODEL_GOC'] = None
                dong_thanh_pham['PHAN_TRAM'] = 0
                dong_thanh_pham['GIA_BAN'] = gia_ban
                if tong_chi_phi > 0 and gia_ban > 0:
                    dong_thanh_pham['PHAN_TRAM'] = float_round((tong_chi_phi/gia_ban)*100,2)
                tong_tien_don_dat_hang += tong_chi_phi
                dong_thanh_pham['THANH_TIEN'] = tong_chi_phi 

                # chỉ lấy giá bán của thành phẩm
                tong_tien_gia_ban += dong_thanh_pham.get('GIA_BAN')
                
                
                
            dong_theo_don_dat_hang['THANH_TIEN'] = tong_tien_don_dat_hang 
            dong_theo_don_dat_hang['GIA_BAN'] = tong_tien_gia_ban
            dong_theo_don_dat_hang['PHAN_TRAM'] = 0
            if tong_tien_gia_ban > 0 and tong_tien_don_dat_hang > 0:
                dong_theo_don_dat_hang['PHAN_TRAM'] = float_round((tong_tien_don_dat_hang/tong_tien_gia_ban)*100,2)
            dong_theo_don_dat_hang['ID_GOC'] = id_goc
            dong_theo_don_dat_hang['MODEL_GOC'] = model_goc
        return dict_cuoi

    def _lay_bao_cao_chi_phi_theo_nguyen_vat_lieu(self, params_sql):      
        record = []
        query = """
            DO LANGUAGE plpgsql $$
            DECLARE
            
            BEGIN
            
                DROP TABLE IF EXISTS TMP_CHI_PHI_DU_KIEN;
                
            
            
                        CREATE TEMP TABLE TMP_CHI_PHI_DU_KIEN
                            AS
                                SELECT
                                      ROW_NUMBER()
                                      OVER (
                                          ORDER BY
                                              "LIST_TEN_NHOM_VTHH",
                                              "TEN_NGUYEN_VAT_LIEU" ) AS "RowNumber"

                                    ,"LIST_TEN_NHOM_VTHH"
                                    ,"MA_HANG_ID"
                                    , "TEN_NGUYEN_VAT_LIEU"
                                    , "DVT"
                                    , sum(coalesce("SO_LUONG",0))        AS "SO_LUONG"
                                FROM
                                (
                                    SELECT

                                    vthhnvl."LIST_TEN_NHOM_VTHH",
                                    vthhnvl."TEN"           AS "TEN_NGUYEN_VAT_LIEU"
                                    ,vthhnvl.id                                                      AS "MA_HANG_ID"
                                    , dvt."DON_VI_TINH"       AS "DVT"
                                    , (coalesce(dmnvl."SO_LUONG",0)  *coalesce(ddhct."SO_LUONG",0))        AS "SO_LUONG"
                                    FROM account_ex_don_dat_hang AS ddh
                                        INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
                                        INNER JOIN danh_muc_vat_tu_hang_hoa vthh ON ddhct."MA_HANG_ID" = vthh.id
                                        INNER JOIN danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl
                                         ON vthh.id = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID"
                                        LEFT JOIN danh_muc_vat_tu_hang_hoa vthhnvl ON dmnvl."MA_NGUYEN_VAT_LIEU_ID" = vthhnvl.id
                                        LEFT JOIN danh_muc_don_vi_tinh dvt ON vthhnvl."DVT_CHINH_ID" = dvt.id
                                    WHERE 
                                            (ddh.id = any(%(DON_DAT_HANG_IDS)s)) 

                                    union

                                    SELECT
                                            vthh."LIST_TEN_NHOM_VTHH",
                                          vthh."TEN"           AS "TEN_NGUYEN_VAT_LIEU"
                                        ,vthh.id                       AS "MA_HANG_ID"
                                        , dvt."DON_VI_TINH"       AS "DVT"
                                        , coalesce(ddhct."SO_LUONG",0)        AS "SO_LUONG"
                                    FROM account_ex_don_dat_hang AS ddh
                                        INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
                                        INNER JOIN danh_muc_vat_tu_hang_hoa vthh ON ddhct."MA_HANG_ID" = vthh.id
                                        LEFT JOIN danh_muc_don_vi_tinh dvt ON vthh."DVT_CHINH_ID" = dvt.id
                                    WHERE  not exists(select 1 from danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl WHERE vthh.id = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID")
                                            AND (ddh.id = any(%(DON_DAT_HANG_IDS)s)) 

                                ) as A


                                GROUP BY
                                    "LIST_TEN_NHOM_VTHH",
                                    "TEN_NGUYEN_VAT_LIEU",
                                    "MA_HANG_ID",
                                    "DVT"
                                ORDER BY
                                    "LIST_TEN_NHOM_VTHH",
                                    "TEN_NGUYEN_VAT_LIEU"

                        ;

                          DROP TABLE IF EXISTS TMP_KET_QUA;

                            CREATE TEMP TABLE TMP_KET_QUA
                            AS
                            --todo: can chuyen ve het theo cung 1 loai don vi tinh + xu ly nhung don hang xuat 1 phan
                            SELECT
                                duKien.*,
                                --trường hợp là chứng từ k cập nhật đơn giá mà trừ số lượng thì mới lấy số lượng vào để trừ đi lúc tính giá
                                SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0) - COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
                                                                                        0)) AS "SO_LUONG_TON"
                            FROM TMP_CHI_PHI_DU_KIEN AS duKien
                                --Chú ý: Phải LEFT JOIN để các Vật tư, kho nào chưa phát sinh thì vẫn phải lấy lên dòng có Số tồn = 0
                                LEFT JOIN so_kho_chi_tiet IL ON IL."MA_HANG_ID" = duKien."MA_HANG_ID"
                        GROUP BY duKien."RowNumber",duKien."MA_HANG_ID",duKien."LIST_TEN_NHOM_VTHH",duKien."TEN_NGUYEN_VAT_LIEU",
                            duKien."MA_HANG_ID",duKien."DVT", duKien."SO_LUONG";
            
            END $$
            ;
            
            SELECT
                ketqua.*,
                CASE WHEN ketqua."SO_LUONG_TON" > ketqua."SO_LUONG"
                    THEN 0
                ELSE ketqua."SO_LUONG" - ketqua."SO_LUONG_TON" END AS "SO_LUONG_CON_THIEU"
            FROM TMP_KET_QUA ketqua
            ORDER BY "RowNumber"
            OFFSET %(offset)s
            LIMIT %(limit)s;

            """
        return self.execute(query,params_sql)

    def _lay_bao_cao_chi_phi_theo_nguyen_vat_lieu_va_don_hang(self, params_sql):      
        record = []
        query = """

        DO LANGUAGE plpgsql $$
DECLARE


BEGIN

    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

            CREATE TEMP TABLE TMP_KET_QUA
                AS
                    SELECT
                          ROW_NUMBER()
                          OVER (
                              ORDER BY
                                  "TEN_NGUYEN_VAT_LIEU"
                                  , "SO_DON_HANG" ) AS "RowNumber"
                        , "SO_DON_HANG"
                        , "TEN_NGUYEN_VAT_LIEU"
                        , "DVT"
                        , SUM("SO_LUONG")           AS "SO_LUONG"
                        , "ID_GOC"
                        , "MODEL_GOC"
                    FROM
                        (

                            SELECT
                                ddh."SO_DON_HANG"

                                , vthhnvl."TEN"             AS "TEN_NGUYEN_VAT_LIEU"
                                , dvt."DON_VI_TINH"         AS "DVT"
                                , coalesce(dmnvl."SO_LUONG",0)  *coalesce(ddhct."SO_LUONG",0)             AS "SO_LUONG"

                                , ddh.id                    AS "ID_GOC"
                                , 'account.ex.don.dat.hang' AS "MODEL_GOC"
                            FROM account_ex_don_dat_hang AS ddh
                                INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct
                                    ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
                                INNER JOIN danh_muc_vat_tu_hang_hoa vthh ON ddhct."MA_HANG_ID" = vthh.id
                                INNER JOIN danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl
                                    ON vthh.id = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID"
                                LEFT JOIN danh_muc_vat_tu_hang_hoa vthhnvl ON dmnvl."MA_NGUYEN_VAT_LIEU_ID" = vthhnvl.id
                                LEFT JOIN danh_muc_don_vi_tinh dvt ON vthhnvl."DVT_CHINH_ID" = dvt.id

                            WHERE  (ddh.id = any(%(DON_DAT_HANG_IDS)s)) 

                              union

                                    SELECT
                                           ddh."SO_DON_HANG"

                                        , vthh."TEN"             AS "TEN_NGUYEN_VAT_LIEU"
                                        , dvt."DON_VI_TINH"         AS "DVT"
                                        , coalesce(ddhct."SO_LUONG",0)               AS "SO_LUONG"

                                        , ddh.id                    AS "ID_GOC"
                                        , 'account.ex.don.dat.hang' AS "MODEL_GOC"
                                    FROM account_ex_don_dat_hang AS ddh
                                        INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
                                        INNER JOIN danh_muc_vat_tu_hang_hoa vthh ON ddhct."MA_HANG_ID" = vthh.id
                                        LEFT JOIN danh_muc_don_vi_tinh dvt ON vthh."DVT_CHINH_ID" = dvt.id
                                    WHERE  not exists(select 1 from danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl WHERE vthh.id = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID")
                                        and (ddh.id = any(%(DON_DAT_HANG_IDS)s)) 
                        ) AS AD
                    GROUP BY
                        "SO_DON_HANG"

                        , "TEN_NGUYEN_VAT_LIEU"
                        , "DVT"
                        , "ID_GOC"
                        , "MODEL_GOC"

                    ORDER BY
                        "TEN_NGUYEN_VAT_LIEU"
                        , "SO_DON_HANG"

            ;

END $$
;

SELECT *
FROM TMP_KET_QUA
ORDER BY "RowNumber"

            OFFSET %(offset)s
            LIMIT %(limit)s;

            """
        return self.execute(query,params_sql)




    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        if THONG_KE_THEO=='CHI_PHI_DU_KIEN':
            action = self.env.ref('bao_cao.open_report_chi_phi_du_kien_theo_don_dat_hang_chi_phi_du_kien').read()[0]
        elif THONG_KE_THEO=='CHI_PHI_THEO_NGUYEN_VAT_LIEU':
            action = self.env.ref('bao_cao.open_report_chi_phi_du_kien_theo_don_dat_hang_chi_phi_du_kien_nguyen_vat_lieu').read()[0]
        elif THONG_KE_THEO=='CHI_PHI_THEO_NGUYEN_VAT_LIEU_VA_DON_HANG':
            action = self.env.ref('bao_cao.open_report_chi_phi_du_kien_theo_don_dat_hang_chi_phi_du_kien_nguyen_vat_lieu_va_so_don_hang').read()[0]
        action['options'] = {'clear_breadcrumbs': True}
        return action        