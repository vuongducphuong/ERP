# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TINH_HINH_THUC_HIEN_DON_DAT_HANG(models.Model):
    _name = 'bao.cao.tinh.hinh.thuc.hien.don.dat.hang'
   
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày',required=True,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    NHOM_KH_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO = fields.Boolean(string='Lấy tình hình đã thực hiện đến cuối kỳ báo cáo', help='Lấy tình hình đã thực hiện đến cuối kỳ báo cáo')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    NGAY_GIAO_HANG = fields.Date(string='Ngày giao hàng', help='Ngày giao hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG_DAT_HANG = fields.Float(string='Số lượng đặt hàng', help='Số lượng đặt hàng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DA_GIAO = fields.Float(string='Số lượng đã giao', help='Số lượng đã giao', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_CON_LAI = fields.Float(string='Số lượng còn lại', help='Số lượng còn lại', digits=decimal_precision.get_precision('SO_LUONG'))
    DOANH_SO_DAT_HANG = fields.Float(string='Doanh số đặt hàng', help='Doanh số đặt hàng',digits= decimal_precision.get_precision('VND'))
    DOANH_SO_DA_THUC_HIEN = fields.Float(string='Doanh số đã thực hiện', help='Doanh số đã thực hiện',digits= decimal_precision.get_precision('VND'))
    DOANH_SO_CHUA_THUC_HIEN = fields.Float(string='Doanh số chưa thực hiện', help='Doanh số chưa thực hiện',digits= decimal_precision.get_precision('VND'))
    TINH_TRANG = fields.Char(string='Tình trạng', help='Tình trạng')
    name = fields.Char(string='Name', oldname='NAME')

    mat_hang_ids = fields.One2many('danh.muc.vat.tu.hang.hoa')
    khach_hang_ids = fields.One2many('res.partner')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','tinh_hinh_thuc_hien_ddh_vthh_rel', string='Chọn sản phẩm') 
    MA_PC_NHOM_VTHH = fields.Char()

    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner','tinh_hinh_thuc_hien_ddh_res_rel',domain=[('LA_KHACH_HANG', '=', True)], string='Chọn KH')
    MA_PC_NHOM_KH = fields.Char()

    @api.onchange('mat_hang_ids')
    def update_SAN_PHAM_IDS(self):
        self.SAN_PHAM_MANY_IDS =self.mat_hang_ids.ids
    
    @api.onchange('khach_hang_ids')
    def update_KHACH_HANG_IDS(self):
        self.KHACH_HANG_MANY_IDS =self.khach_hang_ids.ids
    
    @api.onchange('NHOM_VTHH_ID')
    def update_NHOM_VTHH_ID(self):
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP
    
    @api.onchange('NHOM_KH_ID')
    def update_NHOM_KH_ID(self):
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KH_ID.MA_PHAN_CAP
    
    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        self.mat_hang_ids = self.SAN_PHAM_MANY_IDS.ids
    
    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.khach_hang_ids = self.KHACH_HANG_MANY_IDS.ids
       
    

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    
    def _validate(self):
        params = self._context
        mat_hang_ids = params['mat_hang_ids'] if 'mat_hang_ids' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
        SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        if(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        if(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if CHON_TAT_CA_SAN_PHAM == 'False':
            if SAN_PHAM_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Mặt hàng>. Xin vui lòng chọn lại.')

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_TINH_HINH_THUC_HIEN_DON_DAT_HANG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI",limit=1)
        
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
       
        return result

   
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO = 1 if 'LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO' in params.keys() and params['LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO'] != 'False' else 0
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() and params['NHOM_VTHH_ID'] != 'False' else None
        DON_VI_ID = params['DON_VI_ID'] if 'DON_VI_ID' in params.keys() and params['DON_VI_ID'] != 'False' else None
        NHOM_KH_ID = params['NHOM_KH_ID'] if 'NHOM_KH_ID' in params.keys() and params['NHOM_KH_ID'] != 'False' else None
        NHAN_VIEN_ID = params['NHAN_VIEN_ID'] if 'NHAN_VIEN_ID' in params.keys() and params['NHAN_VIEN_ID'] != 'False' else None
        
        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
        MA_PC_NHOM_KH = params.get('MA_PC_NHOM_KH')

        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')

        if params.get('CHON_TAT_CA_KHACH_HANG'):
            domain = [('LA_KHACH_HANG','=', True)]
            if MA_PC_NHOM_KH:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
            KHACH_HANG_IDS =  self.env['res.partner'].search(domain).ids
        else:
            KHACH_HANG_IDS = params.get('KHACH_HANG_MANY_IDS')

        params_sql = {
        'TU_NGAY':TU_NGAY_F,
        'DEN_NGAY':DEN_NGAY_F,
        'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
        'LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO':LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO,
        'CHI_NHANH_ID':CHI_NHANH_ID,
        'NHOM_VTHH_ID':NHOM_VTHH_ID,
        'DON_VI_ID':DON_VI_ID,
        'NHOM_KH_ID':NHOM_KH_ID,
        'NHAN_VIEN_ID':NHAN_VIEN_ID,
        'khach_hang_ids':KHACH_HANG_IDS or None,
        'mat_hang_ids':SAN_PHAM_IDS or None,
        'limit': limit,
        'offset': offset,
        }

        # Execute SQL query here
        query = """
        --BAO_CAO_TINH_HINH_THUC_HIEN_DON_DAT_HANG
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                                        DATE := %(TU_NGAY)s;

    --tham số từ

    v_den_ngay                                       DATE := %(DEN_NGAY)s;

    --tham số đến

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc            INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    v_chi_nhanh_id                                   INTEGER := %(CHI_NHANH_ID)s;

    --tham số chi nhánh


    v_nhom_vthh_id                                   INTEGER :=  %(NHOM_VTHH_ID)s;

    --tham số nhóm VTHH

    v_don_vi_id                                      INTEGER := %(DON_VI_ID)s;

    --tham số đơn vị

    v_nhan_vien_id                                   INTEGER := %(NHAN_VIEN_ID)s;

    --tham số nhân viên

    v_nhom_kh_id                                     INTEGER := %(NHOM_KH_ID)s;

    --tham số nhóm KH

    v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao INTEGER := %(LAY_TINH_HINH_DA_THUC_HIEN_DEN_CUOI_KY_BAO_CAO)s;

    --lấy tình hình đã thực hiện đến cuối kỳ báo cáo



    rec                                              RECORD;

    PHAN_THAP_PHAN_SO_LUONG                          INTEGER;

    LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG              VARCHAR(127);

    LIST_DON_VI                                      VARCHAR(500) := '(,';


BEGIN

     SELECT value
    INTO LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG
    FROM ir_config_parameter
    WHERE key = 'he_thong.LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;

    DROP TABLE IF EXISTS DS_HANG_HOA
    ;

    CREATE TEMP TABLE DS_HANG_HOA
        AS
            SELECT *


            FROM danh_muc_vat_tu_hang_hoa --tham số hàng hóa
            WHERE (id = any (%(mat_hang_ids)s))
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;

    CREATE TEMP TABLE DS_KHACH_HANG
        AS
            SELECT AO.id AS "KHACH_HANG_ID"

            FROM res_partner AS AO --tham số khách hàng
            WHERE (id = any (%(khach_hang_ids)s))
    ;


     SELECT string_agg(CAST("id" AS VARCHAR(127)), ',')
    INTO LIST_DON_VI
    FROM
            LAY_DS_DON_VI(v_don_vi_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)


    ;

    LIST_DON_VI = '(,' || LIST_DON_VI || ',)'


    ;


    DROP TABLE IF EXISTS TMP_GIA_TRI_CHIET_KHAU_HANG_BAN_TL
    ;

    CREATE TEMP TABLE TMP_GIA_TRI_CHIET_KHAU_HANG_BAN_TL
        AS

            SELECT
                "DON_DAT_HANG_CHI_TIET_ID"
                , "MA_HANG_ID"
                , SUM("SO_TIEN_TRUOC_THUE") AS "SO_TIEN_TRUOC_THUE"
                , SUM("THUE_GTGT")          AS "THUE_GTGT"
            FROM
                (SELECT
                     "DON_DAT_HANG_CHI_TIET_ID"
                     , "MA_HANG_ID"
                     , SUM(SAVD."THANH_TIEN_QUY_DOI" - SAVD."TIEN_CK_QUY_DOI") AS "SO_TIEN_TRUOC_THUE"
                     , SUM(SAVD."TIEN_THUE_GTGT_QUY_DOI")                      AS "THUE_GTGT"
                 FROM sale_document_line SAVD
                     INNER JOIN sale_document SV ON SV."id" = SAVD."SALE_DOCUMENT_ID"
                 WHERE
                     "DON_DAT_HANG_CHI_TIET_ID" IS NOT NULL AND

                     (v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 0 OR
                      (v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 1 AND SV."NGAY_HACH_TOAN" <= v_den_ngay))
                 GROUP BY
                     "DON_DAT_HANG_CHI_TIET_ID",
                     "MA_HANG_ID"
                 UNION ALL
                 SELECT
                     "DON_DAT_HANG_CHI_TIET_ID"
                     , "MA_HANG_ID"
                     , (-1) * COALESCE(SUM(SARD."THANH_TIEN_QUY_DOI" - SARD."TIEN_CHIET_KHAU_QUY_DOI"),
                                       0)                                     AS "SO_TIEN_TRUOC_THUE"
                     , (-1) * COALESCE(SUM(SARD."TIEN_THUE_GTGT_QUY_DOI"), 0) AS "THUE_GTGT"
                 FROM sale_ex_tra_lai_hang_ban_chi_tiet SARD
                     INNER JOIN sale_ex_tra_lai_hang_ban SAR ON SAR."id" = SARD."TRA_LAI_HANG_BAN_ID"
                 WHERE "DON_DAT_HANG_CHI_TIET_ID" IS NOT NULL AND

                       (v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 0 OR
                        (v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 1 AND SAR."NGAY_HACH_TOAN" <= v_den_ngay))
                 GROUP BY
                     "DON_DAT_HANG_CHI_TIET_ID",
                     "MA_HANG_ID"
                 UNION ALL
                 SELECT
                     "DON_DAT_HANG_CHI_TIET_ID"
                     , "MA_HANG_ID"
                     , (-1) * COALESCE(SUM(SADD."THANH_TIEN_QUY_DOI" - SADD."TIEN_CHIET_KHAU_QUY_DOI"),
                                       0)                                     AS "SO_TIEN_TRUOC_THUE"
                     , (-1) * COALESCE(SUM(SADD."TIEN_THUE_GTGT_QUY_DOI"), 0) AS "THUE_GTGT"
                 FROM sale_ex_chi_tiet_giam_gia_hang_ban SADD
                     INNER JOIN sale_ex_giam_gia_hang_ban SAD ON SAD."id" = SADD."GIAM_GIA_HANG_BAN_ID"
                 WHERE
                     "DON_DAT_HANG_CHI_TIET_ID" IS NOT NULL AND


                     (v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 0 OR
                      (v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 1 AND SAD."NGAY_HACH_TOAN" <= v_den_ngay))
                 GROUP BY
                     "DON_DAT_HANG_CHI_TIET_ID",
                     "MA_HANG_ID"
                ) AS T
            GROUP BY
                "DON_DAT_HANG_CHI_TIET_ID",
                "MA_HANG_ID"
    ;


    SELECT value
    INTO PHAN_THAP_PHAN_SO_LUONG
    FROM ir_config_parameter
    WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
    FETCH FIRST 1 ROW ONLY
    ;

    DROP TABLE IF EXISTS TMP_SO_LUONG_DA_GIAO
    ;
    /*Nếu có check Lấy tình hình đã thực hiện đến cuối kỳ báo cáo thì thực hiện*/
    CREATE TEMP TABLE TMP_SO_LUONG_DA_GIAO
    (

        "ID_CHUNG_TU"                                     INTEGER
        ,
        "MODEL_CHUNG_TU"                         VARCHAR(500)
        ,
        "SO_LUONG_DA_GIAO_TEM"                   FLOAT
        ,
        "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM" FLOAT

    )
    ;


    IF v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 1
    THEN
        IF LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG ='True'/*Tùy chọn VTHH: Cách lấy số lượng đã giao của VTHH trên đơn đặt hàng, hợp đồng bán: Lấy từ chứng từ bán hàng, hàng bán trả lại */
        THEN

            INSERT INTO  TMP_SO_LUONG_DA_GIAO
            ("ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , "SO_LUONG_DA_GIAO_TEM"
            , "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM"
            )


            SELECT

                T."ID_CHUNG_TU"
                , 'account.ex.don.dat.hang.chi.tiet'        AS "MODEL_CHUNG_TU"
                , SUM("SO_LUONG_DA_GIAO")                   AS "SO_LUONG_DA_GIAO_TEM"
                , SUM("SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH") AS "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM"
            FROM
                (

                    SELECT

                        SOD."id"    AS "ID_CHUNG_TU"
                        , 'account.ex.don.dat.hang.chi.tiet'                          AS "MODEL_CHUNG_TU"
                        , SUM(ROUND(CAST((CASE WHEN ((SOD."DVT_ID" IS NULL AND SVD."DVT_ID" IS NULL) OR
                                                     (SOD."DVT_ID" IS NOT NULL AND SVD."DVT_ID" IS NOT NULL
                                                      AND
                                                      SOD."DVT_ID" = SVD."DVT_ID"))
                        THEN
                                          SVD."SO_LUONG"
                                          ELSE (CASE WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                           '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                              THEN ROUND(CAST((
                                                                  SVD."SO_LUONG_THEO_DVT_CHINH" *
                                                                  SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH") AS
                                                              NUMERIC),
                                                         PHAN_THAP_PHAN_SO_LUONG)
                                                WHEN (SOD."TOAN_TU_QUY_DOI" = '0' AND
                                                      SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" !=
                                                      0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                    THEN ROUND(CAST((SVD."SO_LUONG_THEO_DVT_CHINH" /
                                                                     SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH") AS
                                                                    NUMERIC), PHAN_THAP_PHAN_SO_LUONG
                                                    )
                                                ELSE SVD."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                END)
                                          END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG))
                                                            AS "SO_LUONG_DA_GIAO"
                        , SUM(
                              SVD."SO_LUONG_THEO_DVT_CHINH")                          AS "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH"
                    FROM
                        account_ex_don_dat_hang_chi_tiet AS SOD
                        INNER JOIN sale_document_line AS SVD
                            ON SOD.id = SVD."DON_DAT_HANG_CHI_TIET_ID" AND   SOD."MA_HANG_ID" = SVD."MA_HANG_ID"
                        INNER JOIN sale_document AS SV ON SV."id" = SVD."SALE_DOCUMENT_ID"
                        INNER JOIN TMP_LIST_BRAND AS TLB ON SV."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                    WHERE SV."NGAY_HACH_TOAN" <= v_den_ngay
                    GROUP BY

                        SOD."id"
                        , "MODEL_CHUNG_TU"

                    /*Lấy số đã giao từ chứng từ bán trả lại*/
                    UNION ALL
                    SELECT

                        SOD."id"                           AS "ID_CHUNG_TU"
                        , 'account.ex.don.dat.hang.chi.tiet'                   AS "MODEL_CHUNG_TU"
                        , (-1) * COALESCE(SUM(ROUND(CAST((
                                                             CASE WHEN (
                                                                 (SOD."DVT_ID" IS NULL AND
                                                                  SVD."DVT_ID" IS NULL)
                                                                 OR
                                                                 (SOD."DVT_ID" IS NOT NULL AND
                                                                  SVD."DVT_ID" IS NOT NULL AND
                                                                  SOD."DVT_ID" = SVD."DVT_ID"))
                                                                 THEN SVD."SO_LUONG"
                                                             ELSE (CASE WHEN (
                                                                 SOD."TOAN_TU_QUY_DOI" =
                                                                 '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                                                 THEN ROUND(CAST((
                                                                                     SVD."SO_LUONG_THEO_DVT_CHINH"
                                                                                     *
                                                                                     SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                 AS NUMERIC),
                                                                            PHAN_THAP_PHAN_SO_LUONG
                                                                 )
                                                                   WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                                         '0' AND
                                                                         SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH"
                                                                         !=
                                                                         0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                                       THEN ROUND(CAST((
                                                                                           SVD."SO_LUONG_THEO_DVT_CHINH"
                                                                                           /
                                                                                           SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                       AS NUMERIC),
                                                                                  PHAN_THAP_PHAN_SO_LUONG)
                                                                   ELSE SVD."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                                   END)
                                                             END) AS NUMERIC),
                                                    PHAN_THAP_PHAN_SO_LUONG))) AS "SO_LUONG_DA_GIAO"
                        , (-1) * COALESCE(SUM(SVD."SO_LUONG_THEO_DVT_CHINH"),
                                          0)                                   AS "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH"
                    FROM
                        account_ex_don_dat_hang_chi_tiet AS SOD
                        INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet AS SVD
                            ON SOD.id = SVD."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = SVD."MA_HANG_ID"
                        INNER JOIN sale_ex_tra_lai_hang_ban AS SV ON SV."id" = SVD."TRA_LAI_HANG_BAN_ID"
                        INNER JOIN TMP_LIST_BRAND AS TLB ON SV."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                    WHERE SV."NGAY_HACH_TOAN" <= v_den_ngay
                    GROUP BY
                        SOD."id"
                        , "MODEL_CHUNG_TU"
                ) AS T
            GROUP BY
                T."ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"

            ;


        ELSE

           INSERT INTO  TMP_SO_LUONG_DA_GIAO
            ("ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , "SO_LUONG_DA_GIAO_TEM"
            , "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM"
            )
                    SELECT

                        T."ID_CHUNG_TU"
                        , 'account.ex.don.dat.hang.chi.tiet'        AS "MODEL_CHUNG_TU"
                        , SUM("SO_LUONG_DA_GIAO")                   AS "SO_LUONG_DA_GIAO_TEM"
                        , SUM("SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH") AS "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM"

                    FROM
                        (

                            SELECT
                                SOD."id"                                AS "ID_CHUNG_TU"
                                , 'account.ex.don.dat.hang.chi.tiet'                          AS "MODEL_CHUNG_TU"
                                , SUM(ROUND(CAST((CASE WHEN ((SOD."DVT_ID" IS NULL AND IOD."DVT_ID" IS NULL) OR
                                                             (SOD."DVT_ID" IS NOT NULL AND IOD."DVT_ID" IS NOT NULL
                                                              AND
                                                              SOD."DVT_ID" = IOD."DVT_ID"))
                                THEN IOD."SO_LUONG_THEO_DVT_CHINH"
                                                  ELSE (CASE WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                                   '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                                      THEN ROUND(CAST((
                                                                          IOD."SO_LUONG_THEO_DVT_CHINH" *
                                                                          SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH") AS
                                                                      NUMERIC),
                                                                 PHAN_THAP_PHAN_SO_LUONG)
                                                        WHEN (SOD."TOAN_TU_QUY_DOI" = '0' AND
                                                              SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" !=
                                                              0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                            THEN ROUND(CAST((IOD."SO_LUONG_THEO_DVT_CHINH" /
                                                                             SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH") AS
                                                                            NUMERIC), PHAN_THAP_PHAN_SO_LUONG
                                                            )
                                                        ELSE IOD."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                        END)
                                                  END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)) AS "SO_LUONG_DA_GIAO"
                                , SUM(
                                      IOD."SO_LUONG_THEO_DVT_CHINH")                          AS "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH"
                            FROM
                                account_ex_don_dat_hang_chi_tiet AS SOD
                                INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS IOD
                                    ON SOD.id = IOD."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = IOD."MA_HANG_ID"
                                INNER JOIN stock_ex_nhap_xuat_kho IO ON IO."id" = IOD."NHAP_XUAT_ID"
                                INNER JOIN TMP_LIST_BRAND AS TLB ON IO."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            WHERE IO."LOAI_XUAT_KHO" = '2020' /*Chỉ lấy xuất kho bán hàng*/
                                  AND IO."NGAY_HACH_TOAN" <= v_den_ngay
                            GROUP BY
                                SOD."id"
                                , "MODEL_CHUNG_TU"

                            /*Lấy số đã giao từ chứng từ bán trả lại*/
                            UNION ALL
                            SELECT

                                SOD."id"              AS "ID_CHUNG_TU"
                                , 'account.ex.don.dat.hang.chi.tiet' AS "MODEL_CHUNG_TU"
                                , (-1) *
                                  COALESCE(SUM(ROUND(CAST((CASE WHEN ((SOD."DVT_ID" IS NULL AND INID."DVT_ID" IS NULL)
                                                                      OR (SOD."DVT_ID" IS NOT NULL AND
                                                                          INID."DVT_ID" IS NOT NULL AND
                                                                          SOD."DVT_ID" = INID."DVT_ID"))
                                      THEN INID."SO_LUONG"
                                                           ELSE (CASE WHEN (SOD."TOAN_TU_QUY_DOI" =
                                                                            '1') -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
                                                               THEN ROUND(CAST((INID."SO_LUONG_THEO_DVT_CHINH" *
                                                                                SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                               AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG
                                                               )
                                                                 WHEN (SOD."TOAN_TU_QUY_DOI" = '0' AND
                                                                       SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" !=
                                                                       0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
                                                                     THEN ROUND(CAST((
                                                                                         INID."SO_LUONG_THEO_DVT_CHINH"
                                                                                         /
                                                                                         SOD."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH")
                                                                                     AS NUMERIC),
                                                                                PHAN_THAP_PHAN_SO_LUONG
                                                                     )
                                                                 ELSE INID."SO_LUONG_THEO_DVT_CHINH" -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
                                                                 END)
                                                           END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)),
                                           0)                        AS "SO_LUONG_DA_GIAO"
                                , (-1) * COALESCE(SUM(INID."SO_LUONG_THEO_DVT_CHINH"),
                                                  0)                 AS "SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH"
                            FROM
                                account_ex_don_dat_hang_chi_tiet AS SOD
                                INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS INID
                                    ON SOD.id = INID."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = INID."MA_HANG_ID"
                                INNER JOIN stock_ex_nhap_xuat_kho AS INI ON INI."id" = INID."NHAP_XUAT_ID"
                                INNER JOIN TMP_LIST_BRAND AS TLB ON INI."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            WHERE INI."LOAI_NHAP_KHO" = '2013'/*Chỉ lấy nhập kho hàng bán trản lại*/
                                  AND INI."NGAY_HACH_TOAN" <= v_den_ngay
                            GROUP BY

                                SOD."id"
                                , "MODEL_CHUNG_TU"

                        ) AS T
                    GROUP BY
                        T."ID_CHUNG_TU"
                        , "MODEL_CHUNG_TU"
            ;
        END IF
        ;
    END IF
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

   

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS
            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY Branch."TEN_DON_VI", SO."NGAY_DON_HANG", SO."SO_DON_HANG", SO."id" ) AS RowNum
                , SO."id"                                       AS "ID_CHUNG_TU"
                , 'account.ex.don.dat.hang'                                                AS "MODEL_CHUNG_TU"
                , SO."LOAI_CHUNG_TU"
                , SO."NGAY_DON_HANG"
                , --Ngày đơn hàng
                SO."SO_DON_HANG"
                , --Số đơn hàng
                SO."NGAY_GIAO_HANG"
                , --Ngày Nhận hàng
                AO."MA_KHACH_HANG"
                , --Mã Khách hàng
                SO."TEN_KHACH_HANG"
                , --Tên Khách hàng


                II."MA"
                , --Mã hàng
                  SOD."TEN_HANG"                                                                    AS "TEN_HANG"
                , --Tên hàng


                U."DON_VI_TINH"
                , --ĐVT
                SOD."SO_LUONG"
                , --Số lượng đặt hàng
                  CASE WHEN v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 1
                      THEN
                          (CASE LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG
                            WHEN 'True'
                               THEN
                                   COALESCE("SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG", 0) +
                                    COALESCE("SO_LUONG_DA_GIAO_TEM", 0)
                           ELSE COALESCE("SO_LUONG_DA_GIAO_NAM_TRUOC_PX", 0) +
                                COALESCE("SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM", 0)
                           END)
                  ELSE
                      (CASE LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG
                       WHEN 'True'
                           THEN "SO_LUONG_DA_GIAO_BAN_HANG"
                       ELSE "SO_LUONG_DA_GIAO_PX"
                       END)
                  END
                                                                                                    AS "SO_LUONG_DA_GIAO"
                , --Số lượng đã giao

                  (SOD."SO_LUONG" - (
                      CASE WHEN v_lay_tinh_hinh_da_thuc_hien_den_cuoi_ky_bao_cao = 1
                          THEN
                              (CASE LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG
                               WHEN 'True'
                                   THEN
                                       COALESCE("SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG", 0) +
                                        COALESCE("SO_LUONG_DA_GIAO_TEM", 0)
                               ELSE COALESCE("SO_LUONG_DA_GIAO_NAM_TRUOC_PX", 0) +
                                    COALESCE("SO_LUONG_DA_GIAO_THEO_DON_VI_CHINH_TEM", 0)
                               END)
                      ELSE
                          (CASE LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG
                           WHEN 'True'
                               THEN "SO_LUONG_DA_GIAO_BAN_HANG"
                           ELSE "SO_LUONG_DA_GIAO_PX"
                           END)
                      END


                  )

                  )                                                                                 AS "SO_LUONG_CON_LAI"
                , --Số lượng còn lại

                  coalesce(SOD."THANH_TIEN_QUY_DOI",0) - coalesce(SOD."TIEN_CHIET_KHAU_QUY_DOI",0) +
                  coalesce(SOD."TIEN_THUE_GTGT_QUY_DOI",0)                                          AS "DOANH_SO_DAT_HANG"
                , --Giá trị đặt hàng

                  coalesce(SOD."SO_TIEN_QUY_DOI_DA_GIAO_NAM_TRUOC",0) + COALESCE(SAVD."SO_TIEN_TRUOC_THUE", 0) +
                  COALESCE(SAVD."THUE_GTGT",
                           0)                                                                       AS "DOANH_SO_DA_THUC_HIEN"
                , --Giá trị đã thực hiện
                  coalesce(SOD."THANH_TIEN_QUY_DOI",0) - coalesce(SOD."TIEN_CHIET_KHAU_QUY_DOI",0) + coalesce(SOD."TIEN_THUE_GTGT_QUY_DOI",0) -
                  (coalesce(SOD."SO_TIEN_QUY_DOI_DA_GIAO_NAM_TRUOC",0)
                   + COALESCE(SAVD."SO_TIEN_TRUOC_THUE", 0)
                   + COALESCE(SAVD."THUE_GTGT",
                              0))                                                                   AS "DOANH_SO_CHUA_THUC_HIEN"
                , --Giá trị chưa thực hiện
                  CASE "TINH_TRANG"
                  WHEN '0'
                      THEN N'Chưa thực hiện'
                  WHEN '1'
                      THEN N'Đang thực hiện'
                  WHEN '2'
                      THEN N'Hoàn thành'
                  WHEN '3'
                      THEN N'Đã huỷ bỏ'
                  END                                                                               AS "TINH_TRANG"


            FROM account_ex_don_dat_hang AS SO
                INNER JOIN account_ex_don_dat_hang_chi_tiet AS SOD ON SO."id" = SOD."DON_DAT_HANG_CHI_TIET_ID"
                INNER JOIN danh_muc_to_chuc AS Branch ON Branch."id" = SO."CHI_NHANH_ID"

                INNER JOIN TMP_LIST_BRAND AS TLB ON SO."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                INNER JOIN DS_HANG_HOA AS LII ON SOD."MA_HANG_ID" = LII."id"
                INNER JOIN DS_KHACH_HANG AS LAO ON SO."KHACH_HANG_ID" = LAO."KHACH_HANG_ID"
                INNER JOIN res_partner AO ON AO."id" = LAO."KHACH_HANG_ID"
                LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON SOD."MA_HANG_ID" = II."id"
                LEFT JOIN danh_muc_don_vi_tinh AS U ON SOD."DVT_ID" = U."id"
                LEFT JOIN TMP_GIA_TRI_CHIET_KHAU_HANG_BAN_TL SAVD
                    ON SOD."id" = SAVD."DON_DAT_HANG_CHI_TIET_ID" AND SOD."MA_HANG_ID" = SAVD."MA_HANG_ID"
                LEFT JOIN res_partner E ON (SO."NV_BAN_HANG_ID" = E."id")
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = E."DON_VI_ID"
                LEFT JOIN danh_muc_ma_thong_ke AS LI ON SOD."MA_THONG_KE_ID" = LI."id"
                LEFT JOIN danh_muc_kho S ON SOD."MA_KHO_ID" = S."id"

                LEFT JOIN danh_muc_don_vi_tinh UM ON UM."id" = II."DVT_CHINH_ID"

                LEFT JOIN TMP_SO_LUONG_DA_GIAO VTemp
                    ON (SOD."id" = VTemp."ID_CHUNG_TU" AND "MODEL_CHUNG_TU" = 'account.ex.don.dat.hang.chi.tiet')
            WHERE SO."NGAY_DON_HANG" BETWEEN v_tu_ngay AND v_den_ngay
                  AND (v_nhan_vien_id IS NULL
                       OR SO."NV_BAN_HANG_ID" = v_nhan_vien_id
                  )
                  AND (v_don_vi_id IS NULL
                       OR LIST_DON_VI LIKE '%%' || CAST(E."DON_VI_ID" AS VARCHAR(127)) || '%%'
                  )
    ;

END $$
;

SELECT 
    "NGAY_DON_HANG" as "NGAY_DON_HANG",
    "SO_DON_HANG" as "SO_DON_HANG",
    "NGAY_GIAO_HANG" as "NGAY_GIAO_HANG",
    "TEN_KHACH_HANG" as "TEN_KHACH_HANG",
    "TEN_HANG" as "TEN_HANG",
    "DON_VI_TINH" as "DVT",
    "SO_LUONG" as "SO_LUONG_DAT_HANG",
    "SO_LUONG_DA_GIAO" as "SO_LUONG_DA_GIAO",
    "SO_LUONG_CON_LAI" as "SO_LUONG_CON_LAI",
    "DOANH_SO_DAT_HANG" as "DOANH_SO_DAT_HANG",
    "DOANH_SO_DA_THUC_HIEN" as "DOANH_SO_DA_THUC_HIEN",
    "DOANH_SO_CHUA_THUC_HIEN" as "DOANH_SO_CHUA_THUC_HIEN",
    "TINH_TRANG" as "TINH_TRANG",
    "ID_CHUNG_TU" as "ID_GOC",
    "MODEL_CHUNG_TU" as "MODEL_GOC"

FROM TMP_KET_QUA_CUOI_CUNG
OFFSET %(offset)s
LIMIT %(limit)s;

;

        """
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
       
        # mat_hang_ids = self._context.get('mat_hang_ids')
        # khach_hang_ids = self._context.get('khach_hang_ids')
    
        param = 'Từ ngày %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        
        action = self.env.ref('bao_cao.open_report_tinh_hinh_thuc_hien_don_dat_hang').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action