# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_CHI_TIET_MUA_HANG(models.Model):
    _name = 'bao.cao.so.chi.tiet.mua.hang'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU = fields.Date(string='Từ', help='Từ',required=True)
    DEN = fields.Date(string='Đến', help='Đến',required=True)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    NHOM_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm NCC', help='Nhóm nhà cung cấp')
    NV_MUA_HANG_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    BAO_GOM = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')#, auto_num='bao_cao_so_chi_tiet_mua_hang_MA_HANG')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG_MUA = fields.Float(string='Số lượng mua', help='Số lượng mua', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    GIA_TRI_MUA = fields.Float(string='Giá trị mua', help='Giá trị mua',digits= decimal_precision.get_precision('VND'))
    CHIET_KHAU = fields.Float(string='Chiết khấu', help='Chiết khấu',digits= decimal_precision.get_precision('VND'))
    SO_LUONG_TRA_LAI = fields.Integer(string='Số lượng trả lại', help='Số lượng trả lại',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_TRA_LAI = fields.Float(string='Giá trị trả lại', help='Giá trị trả lại',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_GIAM_GIA = fields.Float(string='Giá trị giảm giá', help='Giá trị giảm giá',digits= decimal_precision.get_precision('VND'))


    SAN_PHAMIDS = fields.One2many('danh.muc.vat.tu.hang.hoa')
    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','chi_tiet_mua_hang_danh_muc_vthh', string='Chọn sản phẩm')
    MA_PC_NHOM_VTHH = fields.Char()

    NCC_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHA_CUNG_CAP = fields.Boolean('Tất cả nhà cung cấp', default=True)
    NHA_CUNG_CAP_MANY_IDS = fields.Many2many('res.partner','chi_tiet_mua_hang_res_partner',domain=[('LA_NHA_CUNG_CAP', '=', True)], string='Chọn NCC')
    MA_PC_NHOM_NCC = fields.Char()

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    @api.onchange('SAN_PHAMIDS')
    def update_SAN_PHAM_IDS(self):
        self.SAN_PHAM_MANY_IDS = self.SAN_PHAMIDS.ids
       
    @api.onchange('NHOM_VTHH_ID')
    def update_NHOM_VTHH_ID(self):
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP

    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        self.SAN_PHAMIDS = self.SAN_PHAM_MANY_IDS.ids

    
    @api.onchange('NCC_IDS')
    def update_NHA_CUNG_CAP_IDS(self):
        self.NHA_CUNG_CAP_MANY_IDS =self.NCC_IDS.ids
        
    @api.onchange('NHOM_NCC_ID')
    def update_NHOM_NCC_ID(self):
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.MA_PC_NHOM_NCC =self.NHOM_NCC_ID.MA_PHAN_CAP

    @api.onchange('NHA_CUNG_CAP_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.NCC_IDS = self.NHA_CUNG_CAP_MANY_IDS.ids
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.model
    def default_get(self,default_fields):
        res = super(BAO_CAO_SO_CHI_TIET_MUA_HANG, self).default_get(default_fields)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
       
        if chi_nhanh:
            res['CHI_NHANH_ID'] = chi_nhanh.id

        return res

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else -1 
        TU = params.get('TU')
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params.get('DEN')
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NV_MUA_HANG_ID = params['NV_MUA_HANG_ID'] if 'NV_MUA_HANG_ID' in params.keys() and params['NV_MUA_HANG_ID'] != 'False' else -1 
        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
        MA_PC_NHOM_NCC = params.get('MA_PC_NHOM_NCC')

        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')
        
        if params.get('CHON_TAT_CA_NHA_CUNG_CAP'):
            domain = [('LA_NHA_CUNG_CAP','=', True)]
            if MA_PC_NHOM_NCC:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_NCC +'%')]
            NHA_CUNG_CAP_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHA_CUNG_CAP_IDS = params.get('NHA_CUNG_CAP_MANY_IDS')
      
        BAO_GOM = 1 if 'BAO_GOM' in params.keys() and params['BAO_GOM'] else 0
        # Execute SQL query here
        cr = self.env.cr
        params = {
            'CHI_NHANH_ID':CHI_NHANH_ID, 
            'TU_NGAY_F':TU_NGAY_F, 
            'DEN_NGAY_F':DEN_NGAY_F, 
            'NV_MUA_HANG_ID':NV_MUA_HANG_ID, 
            'SAN_PHAMIDS':SAN_PHAM_IDS or None,
            'NCC_IDS' : NHA_CUNG_CAP_IDS or None,
            'BAO_GOM':BAO_GOM, 
           
            }      
        query = """
        DO LANGUAGE plpgsql $$
        DECLARE

        CHI_NHANH_ID                        INTEGER :=%(CHI_NHANH_ID)s;
        TU                                  DATE := %(TU_NGAY_F)s;
        DEN                                 DATE := %(DEN_NGAY_F)s;
        NV_MUA_HANG_ID                      INTEGER := %(NV_MUA_HANG_ID)s;
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC INTEGER :=%(BAO_GOM)s;
       --NCC_IDS                             INTEGER := -1;

        --'(102, 95, 97, 91, 88, 96, 94, 99, 87, 98, 86, 104, 105, 107, 81, 101, 106)'
        --SAN_PHAMIDS                         INTEGER :=-1;
        --(5, 6, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138)

        rec                                 RECORD;




        BEGIN



        DROP TABLE IF EXISTS TMP_TAI_KHOAN;
        IF %(SAN_PHAMIDS)s IS NULL
        THEN
            CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT id
                FROM danh_muc_vat_tu_hang_hoa;
        ELSE
            CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT id
                FROM danh_muc_vat_tu_hang_hoa
                WHERE id = any
                    ( %(SAN_PHAMIDS)s);
        END IF;


        IF %(NCC_IDS)s IS NULL
        THEN

            DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
            CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS
                SELECT
                    ROW_NUMBER()
                    OVER (
                        ORDER BY PL."NGAY_HACH_TOAN",
                        PL."NGAY_CHUNG_TU",
                        PL."SO_CHUNG_TU",
                        PL."NGAY_HOA_DON",
                        PL."SO_HOA_DON",
                        PL."THU_TU_TRONG_CHUNG_TU"
                        )              AS RowNum
                    , PL."ID_CHUNG_TU"
                    , PL."NGAY_HACH_TOAN"
                    , -- Ngày hạch toán
                    PL."NGAY_CHUNG_TU"
                    , -- Ngày chứng từ
                    PL."SO_CHUNG_TU"
                    , -- Số chứng từ
                    PL."NGAY_HOA_DON"
                    , -- Ngày hóa đơn
                    PL."SO_HOA_DON"
                    , -- Số hóa đơn
                    PL."DIEN_GIAI_CHUNG"
                    , PL."DIEN_GIAI"
                    , -- Diễn giải chi tiết
                    PL."MA_DOI_TUONG"
                    , -- Mã NCC
                    PL."TEN_DOI_TUONG"
                    , -- Tên NCC
                    PL."MA_HANG"
                    , -- Mã hàng
                    PL."TEN_HANG"
                    , -- Tên hàng
                    UN."DON_VI_TINH"
                    , -- Tên ĐVT
                    PL."SO_LUONG"
                    , -- Số lượng

                    CASE
                    WHEN PL."LOAI_CHUNG_TU" IN ('3040', '3041', '3042', '3043', '3402')
                        THEN
                        0
                    ELSE
                        PL."DON_GIA" -- Đơn giá quy đổi
                    END              AS "DON_GIA"

                    , MU."DON_VI_TINH" AS "TEN_DON_VI_TINH"
                    , PL."SO_TIEN"
                    , -- Thành tiền
                    PL."SO_TIEN_CHIET_KHAU"
                    , -- Tiền chiết khấu
                    --- Trả lại
                    PL."SO_LUONG_TRA_LAI"
                    , -- Số lượng trả lại
                    PL."SO_TIEN_TRA_LAI"
                    , -- Giá trị trả lại
                    -- Giảm giá (Bảng PUDiscount nhưng lấy từ trường Reduce =)) )
                    PL."SO_TIEN_GIAM_TRU"
                    , -- Giá trị giảm giá
                    CASE
                    WHEN PL."LOAI_CHUNG_TU" IN ('3030', '3031', '3032', '3033', '3040', '3041', '3042', '3043')
                        THEN
                        PL."MA_TK_CO"
                    ELSE
                        PL."MA_TK_NO"
                    END              AS "MA_TK_NO"
                    , -- TK Nợ:
                    CASE
                    WHEN PL."LOAI_CHUNG_TU" IN ('3030', '3031', '3032', '3033', '3040', '3041', '3042', '3043')
                        THEN
                        PL."MA_TK_NO"
                    ELSE
                        PL."MA_TK_CO"
                    END              AS "MA_TK_CO" --
                    ,PL."ID_CHUNG_TU"           AS "ID_GOC",
                    PL."MODEL_CHUNG_TU"        AS "MODEL_GOC" 

                FROM so_mua_hang_chi_tiet AS PL
                    INNER JOIN (SELECT *
                            FROM LAY_DANH_SACH_CHI_NHANH(CHI_NHANH_ID, BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)) AS TLB
                    ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                    INNER JOIN TMP_TAI_KHOAN LII ON PL."MA_HANG_ID" = LII.id
                    LEFT JOIN danh_muc_don_vi_tinh AS UN ON PL."DVT_ID" = UN.id
                    -- Danh mục ĐVT -> ĐVT
                    LEFT JOIN danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU.id -- Danh mục ĐVT -> ĐVT chính
                WHERE PL."NGAY_HACH_TOAN" BETWEEN TU AND DEN
                        AND (NV_MUA_HANG_ID = -1
                            OR PL."NHAN_VIEN_ID" = NV_MUA_HANG_ID
                        );


            ELSE

                DROP TABLE IF EXISTS TMP_NCC;
                CREATE TEMP TABLE TMP_NCC
                AS
                    SELECT id
                    FROM res_partner
                    WHERE id = any (%(NCC_IDS)s);


            DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
            CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS
                SELECT
                    ROW_NUMBER()
                    OVER (
                        ORDER BY PL."NGAY_HACH_TOAN",
                        PL."NGAY_CHUNG_TU",
                        PL."SO_CHUNG_TU",
                        PL."NGAY_HOA_DON",
                        PL."SO_HOA_DON",
                        PL."THU_TU_TRONG_CHUNG_TU"
                        )              AS RowNum
                    , PL."ID_CHUNG_TU"
                    , PL."NGAY_HACH_TOAN"
                    , -- Ngày hạch toán
                    PL."NGAY_CHUNG_TU"
                    , -- Ngày chứng từ
                    PL."SO_CHUNG_TU"
                    , -- Số chứng từ
                    PL."NGAY_HOA_DON"
                    , -- Ngày hóa đơn
                    PL."SO_HOA_DON"
                    , -- Số hóa đơn
                    PL."DIEN_GIAI_CHUNG"
                    , PL."DIEN_GIAI"
                    , -- Diễn giải chi tiết
                    PL."MA_DOI_TUONG"
                    , -- Mã NCC
                    PL."TEN_DOI_TUONG"
                    , -- Tên NCC
                    PL."MA_HANG"
                    , -- Mã hàng
                    PL."TEN_HANG"
                    , -- Tên hàng
                    UN."DON_VI_TINH"
                    , -- Tên ĐVT
                    PL."SO_LUONG"
                    , -- Số lượng

                    CASE
                    WHEN PL."LOAI_CHUNG_TU" IN ('3040', '3041', '3042', '3043', '3402')
                        THEN
                        0
                    ELSE
                        PL."DON_GIA" -- Đơn giá quy đổi
                    END              AS "DON_GIA"

                    , MU."DON_VI_TINH" AS "TEN_DON_VI_TINH"
                    , PL."SO_TIEN"
                    , -- Thành tiền
                    PL."SO_TIEN_CHIET_KHAU"
                    , -- Tiền chiết khấu
                    --- Trả lại
                    PL."SO_LUONG_TRA_LAI"
                    , -- Số lượng trả lại
                    PL."SO_TIEN_TRA_LAI"
                    , -- Giá trị trả lại

                    PL."SO_TIEN_GIAM_TRU"
                    , -- Giá trị giảm giá
                    CASE
                    WHEN PL."LOAI_CHUNG_TU" IN ('3030', '3031', '3032', '3033', '3040', '3041', '3042', '3043')
                        THEN
                        PL."MA_TK_CO"
                    ELSE
                        PL."MA_TK_NO"
                    END              AS "MA_TK_NO"
                    , -- TK Nợ:
                    CASE
                    WHEN PL."LOAI_CHUNG_TU" IN ('3030', '3031', '3032', '3033', '3040', '3041', '3042', '3043')
                        THEN
                        PL."MA_TK_NO"
                    ELSE
                        PL."MA_TK_CO"
                    END              AS "MA_TK_CO" --
                    ,PL."ID_CHUNG_TU"           AS "ID_GOC",
                    PL."MODEL_CHUNG_TU"        AS "MODEL_GOC"
                FROM so_mua_hang_chi_tiet AS PL
                    INNER JOIN (SELECT *
                            FROM LAY_DANH_SACH_CHI_NHANH(CHI_NHANH_ID, BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)) AS TLB
                    ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                    INNER JOIN TMP_NCC AS LAO ON PL."DOI_TUONG_ID" = LAO.id
                    INNER JOIN TMP_TAI_KHOAN LII ON PL."MA_HANG_ID" = LII.id
                    LEFT JOIN danh_muc_don_vi_tinh AS UN ON PL."DVT_ID" = UN.id
                    -- Danh mục ĐVT -> ĐVT
                    LEFT JOIN danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU.id -- Danh mục ĐVT -> ĐVT chính
                    WHERE PL."NGAY_HACH_TOAN" BETWEEN TU AND DEN
                        AND (NV_MUA_HANG_ID = -1
                            OR PL."NHAN_VIEN_ID" = NV_MUA_HANG_ID
                        );

            END IF ;

        END $$;

        SELECT  *FROM TMP_KET_QUA_CUOI_CUNG;
       

        """
        # if NCC_IDS:
        #     params.update({'NCC_IDS': tuple([tk['id'] for tk in NCC_IDS])})
        #     query += """AND PL."DOI_TUONG_ID" IN  %(NCC_IDS)s"""
        # if NV_MUA_HANG_ID != 'False':
        #     params.update({'NV_MUA_HANG_ID': NV_MUA_HANG_ID})
        #     query += """AND PL."NV_MUA_HANG_ID" =  %(NV_MUA_HANG_ID)s"""
        cr.execute(query, params)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
                'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
                'NGAY_HOA_DON': line.get('NGAY_HOA_DON', ''),
                'SO_HOA_DON': line.get('SO_HOA_DON', ''),
                'MA_HANG': line.get('MA_HANG', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT': line.get('DON_VI_TINH', ''),
                'SO_LUONG_MUA': line.get('SO_LUONG', ''),
                'DON_GIA': line.get('DON_GIA', ''),
                'GIA_TRI_MUA': line.get('SO_TIEN', ''),
                'CHIET_KHAU': line.get('SO_TIEN_CHIET_KHAU', ''),
                'SO_LUONG_TRA_LAI': line.get('SO_LUONG_TRA_LAI', ''),
                'GIA_TRI_TRA_LAI': line.get('SO_TIEN_TRA_LAI', ''),
                'GIA_TRI_GIAM_GIA': line.get('SO_TIEN_GIAM_TRU', ''),
                'ID_GOC': line.get('ID_GOC', ''),
                'MODEL_GOC': line.get('MODEL_GOC', ''),
                })
        return record

    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
        SAN_PHAMIDS = params.get('SAN_PHAMIDS')
        NCC_IDS = params.get('NCC_IDS')
        TU = params.get('TU')
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params.get('DEN')
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
        SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'

        if(TU=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')
         # validate của các trường hợp thống kê không chọn
        if CHON_TAT_CA_SAN_PHAM == 'False':
            if SAN_PHAM_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Mặt hàng>. Xin vui lòng chọn lại.')
        

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        params = self._context
        param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report__so_chi_tiet_mua_hang').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action