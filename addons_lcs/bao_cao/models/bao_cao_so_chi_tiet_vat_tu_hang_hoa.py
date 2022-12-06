# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from datetime import datetime

class BAO_CAO_SO_CHI_TIET_VAT_TU_HANG_HOA(models.Model):
    _name = 'bao.cao.so.chi.tiet.vat.tu.hang.hoa'
    _description = 'Sổ chi tiết vật tư hàng hóa'
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuôc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required='True')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now,required='True')
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vthh')
    NHOM_VTHH_ID_HAN_SU_DUNG = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    NHOM_VTHH_ID_MA_QUY_CACH = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH',required='True')
    # THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>> '), ('SO_LO_HAN_SU_DUNG', ' Số lô ,Hạn sử dụng '), ('MA_QUY_CACH', 'Mã quy cách'), ], string='Thống kê theo', help='Thống kê theo',required='True',default='KHONG_CHON')
    THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>> ') ], string='Thống kê theo', help='Thống kê theo',required='True',default='KHONG_CHON')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    KHO_ID_HAN_SU_DUNG = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    KHO_ID_MA_QUY_CACH = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    LAY_THEM_CHUNG_TU_CHUA_GHI_SO = fields.Boolean(string='Lấy thêm chứng từ chưa ghi sổ', help='Lấy thêm chứng từ chưa ghi sổ')
    MA_KHO = fields.Char(string='Mã kho', help='Mã kho')
    TEN_KHO = fields.Char(string='Tên kho', help='Tên kho')
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    SO_LO = fields.Char(string='Số lô', help='Số lô')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    SO_LUONG_NHAP = fields.Float(string='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_NHAP = fields.Float(string='Giá trị', help='Nhập giá trị',digits=decimal_precision.get_precision('VND'))
    SO_LUONG_XUAT = fields.Float(string='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_XUAT = fields.Float(string='Giá trị', help='Xuất giá trị',digits=decimal_precision.get_precision('VND'))
    SO_LUONG_TON = fields.Float(string='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_TON = fields.Float(string='Giá trị', help='Tồn giá trị',digits=decimal_precision.get_precision('VND'))
    HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
    MA_QUY_CACH_1 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 1')#, auto_num='bao_cao_so_chi_tiet_vat_tu_hang_hoa_MA_QUY_CACH_1')
    MA_QUY_CACH_2 = fields.Char(string='Mã quy cách 2', help='Mã quy cách 2')#, auto_num='bao_cao_so_chi_tiet_vat_tu_hang_hoa_MA_QUY_CACH_2')
    SO_LUONG_NHAP = fields.Float(string='Số lượng nhập', help='Số lượng nhập', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_XUAT = fields.Float(string='Số lượng xuất', help='Số lượng xuất', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_TON = fields.Float(string='Số lượng tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('SO_LUONG'))

    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','bao_cao_so_chi_tiet_vthh_danh_muc_vthh_rel', string='Chọn sản phẩm') 
    MA_PC_NHOM_VTHH = fields.Char()


    HANG_ID = fields.One2many('danh.muc.vat.tu.hang.hoa')
    HANG_ID_2 = fields.One2many('danh.muc.vat.tu.hang.hoa')
    HANG_ID_3 = fields.One2many('danh.muc.vat.tu.hang.hoa')
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN


    @api.onchange('NHOM_VTHH_ID')
    def update_SAN_PHAM_IDS(self):
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP

    @api.onchange('HANG_ID','HANG_ID_2','HANG_ID_3')
    def _onchange_HANG_ID(self):
        self.SAN_PHAM_MANY_IDS =self.HANG_ID.ids

    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        self.HANG_ID =self.SAN_PHAM_MANY_IDS.ids

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_CHI_TIET_VAT_TU_HANG_HOA, self).default_get(fields_list)
        result['KHO_ID'] = -1
        result['KHO_ID_HAN_SU_DUNG'] = -1
        result['KHO_ID_MA_QUY_CACH'] = -1
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result

    def _validate(self):
        params = self._context
        CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
        SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'
        KHO_ID = params['KHO_ID'] if 'KHO_ID' in params.keys() else 'False'
      
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')
        
        if KHO_ID == 'False':
            raise ValidationError('<Kho> không được để trống. Xin vui lòng chọn lại.')
        if CHON_TAT_CA_SAN_PHAM == 'False':
            if SAN_PHAM_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Mặt hàng>. Xin vui lòng chọn lại.')
          
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() and params['NHOM_VTHH_ID'] != 'False' else None
        DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() and params['DON_VI_TINH'] != 'False' else None
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        KHO_ID = params['KHO_ID'] if 'KHO_ID' in params.keys() and params['KHO_ID'] != 'False' else None
        KHO_ID_HAN_SU_DUNG = params['KHO_ID_HAN_SU_DUNG'] if 'KHO_ID_HAN_SU_DUNG' in params.keys() else 'False'
        KHO_ID_MA_QUY_CACH = params['KHO_ID_MA_QUY_CACH'] if 'KHO_ID_MA_QUY_CACH' in params.keys() else 'False'
        LAY_THEM_CHUNG_TU_CHUA_GHI_SO = params['LAY_THEM_CHUNG_TU_CHUA_GHI_SO'] if 'LAY_THEM_CHUNG_TU_CHUA_GHI_SO' in params.keys() else 'False'
        VTHH_IDS = [mh_mh['id'] for mh_mh in params['HANG_ID']]  if 'HANG_ID' in params.keys() and params['HANG_ID'] != 'False' else None
        CO_NHAP_XUAT_TON = 1 if 'selection_khong_chon' in params.keys() and params['selection_khong_chon'] != 'False' and params['selection_khong_chon'] == 'co_nhap_xuat_ton' else 0
        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')

        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')


        don_vi_tinh = 0
        if DON_VI_TINH == 'DON_VI_CHUYEN_DOI_1':
            don_vi_tinh = 1
        elif DON_VI_TINH == 'DON_VI_CHUYEN_DOI_2':
            don_vi_tinh = 2


        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'VTHH_IDS' : SAN_PHAM_IDS or None,
            'KHO_ID' : KHO_ID,
            'DON_VI_TINH' : don_vi_tinh,
            'NHOM_VTHH_ID' : NHOM_VTHH_ID,
            'CO_NHAP_XUAT_TON' : CO_NHAP_XUAT_TON,
            'limit': limit,
            'offset': offset,
        }


        query = """
            DO LANGUAGE plpgsql $$
            DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;

                den_ngay                            DATE := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


                kho_id                              INTEGER := %(KHO_ID)s;

                don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;

                nhom_vthh_id                        INTEGER := %(NHOM_VTHH_ID)s;

                co_nhap_xuat_ton                    INTEGER := %(CO_NHAP_XUAT_TON)s;

                rec                                 RECORD;

                PHAN_THAP_PHAN_SO_LUONG             INTEGER;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INTEGER;

                PHAN_THAP_PHAN_DON_GIA              INTEGER;

                LOAI_TIEN_CHINH                     INTEGER;

                MA_PHAN_CAP_NHOM_VTHH_DICH_VU       VARCHAR(100);

                TEN_NHOM_VTHH_DICH_VU               VARCHAR(100);

                kho_tat_ca_id                       INTEGER := -1;

                SO_LUONG_TON_TMP                    FLOAT := 0;

                GIA_TRI_TON_TMP                     FLOAT := 0;
                SO_LUONG_TON_THEO_DVC_TMP                    FLOAT := 0;

                KHO_ID_TMP                          INTEGER := 0;

                VAT_TU_HH_TMP                       INTEGER := 0;


            BEGIN

            SELECT value
            INTO PHAN_THAP_PHAN_SO_LUONG
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
            FETCH FIRST 1 ROW ONLY
            ;


            SELECT value
            INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
            FETCH FIRST 1 ROW ONLY
            ;

            SELECT value
            INTO PHAN_THAP_PHAN_DON_GIA
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
            FETCH FIRST 1 ROW ONLY
            ;


            SELECT value
            INTO LOAI_TIEN_CHINH
            FROM ir_config_parameter
            WHERE key = 'he_thong.LOAI_TIEN_CHINH'
            FETCH FIRST 1 ROW ONLY
            ;


            SELECT "MA_PHAN_CAP"
            INTO MA_PHAN_CAP_NHOM_VTHH_DICH_VU
            FROM danh_muc_nhom_vat_tu_hang_hoa_dich_vu
            WHERE "id" = nhom_vthh_id
            ;

            SELECT "TEN"
            INTO TEN_NHOM_VTHH_DICH_VU
            FROM danh_muc_nhom_vat_tu_hang_hoa_dich_vu
            WHERE "id" = nhom_vthh_id
            ;


            -- Sinh bảng tạm lưu quan hệ nhập xuất kho vật tư với hóa đơn

            DROP TABLE IF EXISTS TMP_LUU_QUAN_HE_NHAP_XUAT_KHO_VT_VOI_HOA_DON
            ;

            CREATE TEMP TABLE TMP_LUU_QUAN_HE_NHAP_XUAT_KHO_VT_VOI_HOA_DON

            (
                "NHAP_XUAT_KHO_ID"          INT,
                "NHAP_XUAT_KHO_CHI_TIET_ID" INT,
                "HOA_DON_ID"                INT,
                "SO_HOA_DON"                VARCHAR(100),
                "NGAY_HOA_DON"              TIMESTAMP
            )
            ;

            -- Lấy số liệu
            INSERT INTO TMP_LUU_QUAN_HE_NHAP_XUAT_KHO_VT_VOI_HOA_DON
                SELECT
                    T1."NHAP_XUAT_KHO_ID"
                    , NULL :: INT
                    , T1."HOA_DON_ID"
                    , S."SO_HOA_DON"
                    , S."NGAY_HOA_DON"
                FROM (
                        SELECT
                            SOR."stock_ex_nhap_xuat_kho_id"  AS "NHAP_XUAT_KHO_ID"
                            , SR."sale_ex_hoa_don_ban_hang_id" AS "HOA_DON_ID"
                        FROM sale_ex_document_outward_rel SOR
                            INNER JOIN sale_ex_document_invoice_rel SR ON SOR."sale_document_id" = SR."sale_document_id"
                        -- 							  WHERE SOR.ReferenceType = 0 -- Chỉ lấy chứng từ bán hàng sinh phiếu xuất
                        -- 								AND SR.ReferenceType = 0 -- Chỉ lấy chứng từ bán hàng lập kèm hóa đơn
                        UNION ALL
                        SELECT
                            P."id"
                            , P."HOA_DON_ID"
                        FROM purchase_ex_tra_lai_hang_mua P
                        WHERE P."HOA_DON_ID" IS NOT NULL
                            AND P."CHI_NHANH_ID" = chi_nhanh_id
                            AND P."LOAI_CHUNG_TU" IN (3030, 3031) -- Chỉ lấy các chứng từ qua kho
                            AND
                            P."state" = 'da_ghi_so'


                    ) T1
                    INNER JOIN sale_ex_hoa_don_ban_hang S ON T1."HOA_DON_ID" = S."id"

                UNION ALL
                SELECT
                    T2."NHAP_XUAT_KHO_ID"
                    , T2."NHAP_XUAT_KHO_CHI_TIET_ID"
                    , T2."HOA_DON_ID"
                    , P."SO_HOA_DON"
                    , P."NGAY_HOA_DON"
                FROM (
                        SELECT
                            S."PHIEU_NHAP_ID"       AS "NHAP_XUAT_KHO_ID"
                            ,
                            -- Trường hợp hàng bán trả lại ko kiêm phiếu nhập, sinh phiếu nhập sau thì ID này ko phải ID của phiếu nhập, là ID vớ vẩn nên cách này chưa lấy được
                            NULL :: INT             AS "NHAP_XUAT_KHO_CHI_TIET_ID"
                            , S."HOA_DON_MUA_HANG_ID" AS "HOA_DON_ID"
                        FROM sale_ex_tra_lai_hang_ban S
                        WHERE S."HOA_DON_MUA_HANG_ID" IS NOT NULL
                            AND S."PHIEU_NHAP_ID" IS NOT NULL
                            AND S."CHI_NHANH_ID" = chi_nhanh_id
                            AND
                            S."state" = 'da_ghi_so'

                        UNION ALL
                        SELECT
                            P."id"
                            , NULL :: INT
                            , P."HOA_DON_MUA_HANG_ID"
                        FROM purchase_document P
                        WHERE P."HOA_DON_MUA_HANG_ID" IS NOT NULL
                            AND P."CHI_NHANH_ID" = chi_nhanh_id

                            AND P."state" = 'da_ghi_so'

                            AND P."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 318, 319, 320, 321, 322)
                        UNION ALL
                        SELECT
                            PUD."id"
                            , NULL :: INT
                            , PUD."HOA_DON_MUA_HANG_ID"
                        FROM purchase_ex_giam_gia_hang_mua PUD
                        WHERE PUD."CHI_NHANH_ID" = chi_nhanh_id
                            AND (PUD."state" = 'da_ghi_so'

                            )
                            AND PUD."HOA_DON_MUA_HANG_ID" IS NOT NULL
                    ) T2
                    INNER JOIN purchase_ex_hoa_don_mua_hang P ON T2."HOA_DON_ID" = P."id"
                WHERE COALESCE(P."SO_HOA_DON", '') <> ''
                UNION ALL
                SELECT
                    PD."order_id" AS "NHAP_XUAT_KHO_ID"
                    , PD."id"       AS "NHAP_XUAT_KHO_CHI_TIET_ID"
                    , NULL          AS "HOA_DON_ID"
                    , PD."SO_HOA_DON_DETAIL"
                    , PD."NGAY_HOA_DON"
                FROM purchase_document P
                    INNER JOIN purchase_document_line PD ON PD."order_id" = P."id"
                WHERE COALESCE(PD."SO_HOA_DON_DETAIL", '') <> '' AND PD."NGAY_HOA_DON" IS NOT NULL
                    AND P."LOAI_CHUNG_TU" IN (352, 357, 358, 359, 360, 368, 369, 370, 371, 372)

            ;


            DROP TABLE IF EXISTS TMP_DS_VAT_TU_HANG_HOA
            ;

            CREATE TEMP TABLE TMP_DS_VAT_TU_HANG_HOA
                AS
                    SELECT
                        I."id"          AS "MA_HANG_ID"
                        , I."MA"          AS "MA_HANG"
                        , I."TEN"         AS "TEN_HANG"
                        , I."LIST_MPC_NHOM_VTHH"
                        , I."MA_NHOM_VTHH"
                        , U."id"          AS "DVT_ID"
                        , U."DON_VI_TINH" AS "TEN_DON_VI_TINH"
                        , U1."DON_VI_TINH"
                        , CASE WHEN don_vi_tinh = 0
                                    OR don_vi_tinh IS NULL
                        THEN 1
                        WHEN IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                            THEN 1

                        ELSE COALESCE(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                        END             AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                        , IU."PHEP_TINH_CHUYEN_DOI"
                    FROM danh_muc_vat_tu_hang_hoa I

                        LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IU ON I."id" = IU."VAT_TU_HANG_HOA_ID"
                                                                                AND IU."STT" = don_vi_tinh
                        LEFT JOIN danh_muc_don_vi_tinh U ON (
                                                                (
                                                                    don_vi_tinh IS NULL
                                                                    OR don_vi_tinh = 0
                                                                )
                                                                AND I."DVT_CHINH_ID" = U."id"
                                                            )
                                                            OR (
                                                                don_vi_tinh IS NOT NULL
                                                                AND don_vi_tinh <> 0
                                                                AND IU."DVT_ID" = U."id"
                                                            )
                        LEFT JOIN danh_muc_don_vi_tinh U1 ON I."DVT_CHINH_ID" = U1."id"
                    WHERE
                        (I."id" = any(%(VTHH_IDS)s))
                        AND
                        (
                            don_vi_tinh IS NULL
                            OR don_vi_tinh = 0
                            OR IU."STT" IS NOT NULL
                        )
                        AND (
                            nhom_vthh_id IS NULL
                            OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;' || MA_PHAN_CAP_NHOM_VTHH_DICH_VU || '%%'
                        )
            ;

            DROP TABLE IF EXISTS TMP_KET_QUA

            ;

            DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
            ;

            CREATE TEMP SEQUENCE TMP_KET_QUA_seq
            ;


            CREATE TABLE TMP_KET_QUA
            (
                RowNum                  INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
                    PRIMARY KEY,
                "ID_CHUNG_TU"           INT,
                "MODEL_CHUNG_TU"        VARCHAR(255),
                "LOAI_CHUNG_TU"         INT,
                "MA_KHO_ID"             INT,
                "MA_KHO"                VARCHAR(255),
                "TEN_KHO"               VARCHAR(128),
                "MA_HANG_ID"            INT,
                "MA_HANG"               VARCHAR(127),
                "TEN_HANG"              VARCHAR(255),
                "NGAY_HACH_TOAN"        TIMESTAMP,
                "NGAY_CHUNG_TU"         TIMESTAMP,
                "SO_CHUNG_TU"           VARCHAR(255),
                "DIEN_GIAI"             VARCHAR(255),
                "DVT_ID"                INT,
                "DVT"                   VARCHAR(255),
                "DON_GIA"               DECIMAL(22, 8),
                "SO_LUONG_NHAP"         DECIMAL(22, 8),
                "GIA_TRI_NHAP"          DECIMAL(25, 8),
                "SO_LUONG_XUAT"         DECIMAL(22, 8),
                "GIA_TRI_XUAT"          DECIMAL(25, 8),
                "SO_LUONG_TON"          DECIMAL(22, 8),
                "GIA_TRI_TON"           DECIMAL(25, 8),
                "STT_LOAI_CHUNG_TU"     TIMESTAMP,
                "THU_TU_TRONG_CHUNG_TU" INT,

                "SO_LUONG_NHAP_THEO_DVC"          DECIMAL(22, 8),
                "SO_LUONG_XUAT_THEO_DVC"           DECIMAL(25, 8),
                "SO_LUONG_TON_THEO_DVC"          DECIMAL(22, 8),
                "DON_GIA_BAN"          DECIMAL(22, 8),
                "SO_LENH_SAN_XUAT"           VARCHAR(255)

            )
            ;


            DROP TABLE IF EXISTS TMP_BAN_HANG_CHI_TIET
            ;

            CREATE TEMP TABLE TMP_BAN_HANG_CHI_TIET
                AS
                    SELECT
                        CASE WHEN D."SO_LUONG" <> 0
                            THEN D."THANH_TIEN_QUY_DOI" / D."SO_LUONG"
                        ELSE 0
                        END                                   AS "DON_GIA_BAN"
                        ,
                        /*Nếu đồng tiền hạch toán trùng với trên chứng từ thì lấy đơn giá còn nếu không thì chia Thành tiền/Số lượng*/
                        CASE WHEN M."currency_id" = LOAI_TIEN_CHINH
                            THEN "DON_GIA"
                        ELSE CASE WHEN "SO_LUONG" <> 0
                            THEN D."THANH_TIEN_QUY_DOI" / D."SO_LUONG"
                            ELSE 0
                            END
                        END                                   AS "DON_GIA"
                        , D."MA_HANG_ID"                        AS "MA_HANG_BAN_ID"
                        , SR.stock_ex_nhap_xuat_kho_chi_tiet_id AS "CHI_TIET_ID"
                        , D."DVT_ID"
                        , D."THANH_TIEN_QUY_DOI"                AS "DOANH_SO_BAN"
                    FROM sale_document_line D
                        INNER JOIN sale_ex_document_outward_detail_ref SR ON SR."sale_document_line_id" = D."id"
                        INNER JOIN sale_document M ON D."SALE_DOCUMENT_ID" = M."id"
                        INNER JOIN danh_muc_to_chuc B ON M."CHI_NHANH_ID" = B."id"
                    WHERE (
                            (B."id" = chi_nhanh_id
                            )
                            OR (bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1 AND B."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                            )
                        )
                        AND (

                            M."state" = 'da_ghi_so'

                        )

                    GROUP BY
                        CASE WHEN D."SO_LUONG" <> 0
                            THEN D."THANH_TIEN_QUY_DOI" / D."SO_LUONG"
                        ELSE 0
                        END
                        ,

                        CASE WHEN M."currency_id" = LOAI_TIEN_CHINH
                            THEN "DON_GIA"
                        ELSE CASE WHEN "SO_LUONG" <> 0
                            THEN D."THANH_TIEN_QUY_DOI" / D."SO_LUONG"
                            ELSE 0
                            END
                        END
                        , D."MA_HANG_ID"
                        , SR.stock_ex_nhap_xuat_kho_chi_tiet_id
                        , D."DVT_ID"
                        , D."THANH_TIEN_QUY_DOI"
            ;

            -----------------------------------------------

            INSERT INTO TMP_KET_QUA

            (
                "ID_CHUNG_TU",
                "MODEL_CHUNG_TU",
                "LOAI_CHUNG_TU",
                "MA_KHO_ID",
                "MA_KHO",
                "TEN_KHO",
                "MA_HANG_ID",
                "MA_HANG",
                "TEN_HANG",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "DIEN_GIAI",
                "DVT_ID",
                "DVT",
                "DON_GIA",
                "SO_LUONG_NHAP",
                "GIA_TRI_NHAP",
                "SO_LUONG_XUAT",
                "GIA_TRI_XUAT",
                "SO_LUONG_TON",
                "GIA_TRI_TON",
                "STT_LOAI_CHUNG_TU",
                "THU_TU_TRONG_CHUNG_TU",

                "SO_LUONG_NHAP_THEO_DVC"         ,
                "SO_LUONG_XUAT_THEO_DVC"           ,
                "SO_LUONG_TON_THEO_DVC",
                "DON_GIA_BAN",
                "SO_LENH_SAN_XUAT"
            )
                SELECT
                    NULL :: INT                                AS "ID_CHUNG_TU"
                    , NULL                                       AS "MODEL_CHUNG_TU"
                    , CAST(0 AS INT)                             AS "LOAI_CHUNG_TU"
                    , S."id"                                     AS "MA_KHO_ID"
                    , S."MA_KHO"
                    , S."TEN_KHO"
                    , I."MA_HANG_ID"
                    , I."MA_HANG"
                    , I."TEN_HANG"
                    , NULL                                       AS "NGAY_HACH_TOAN"
                    , NULL                                       AS "NGAY_CHUNG_TU"
                    , NULL                                       AS "SO_CHUNG_TU"
                    , N'Số dư đầu kỳ'                           AS "DIEN_GIAI"
                    , NULL :: INT                                AS "DVT_ID"
                    , I."DON_VI_TINH"
                    , 0                                          AS "DON_GIA"
                    , 0                                          AS "SO_LUONG_NHAP"
                    , 0                                          AS "GIA_TRI_NHAP"
                    , 0                                          AS "SO_LUONG_XUAT"
                    , 0                                          AS "GIA_TRI_XUAT"
                    , SUM(CASE

                        WHEN IL."DVT_ID" = I."DVT_ID"
                            THEN IL."SO_LUONG_NHAP" - IL."SO_LUONG_XUAT"
                        ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH") *

                            (CASE WHEN I."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                                THEN
                                    1 / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                ELSE
                                    I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                END)
                        END)                                   AS "SO_LUONG_TON"
                    , SUM(IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT") AS "GIA_TRI_TON"
                    , MIN(IL."STT_LOAI_CHUNG_TU")                AS "STT_LOAI_CHUNG_TU"
                    , MIN(IL."THU_TU_TRONG_CHUNG_TU")            AS "STT"
                    , 0                                          AS "SO_LUONG_NHAP_THEO_DVC"
                    , 0                                          AS "SO_LUONG_XUAT_THEO_DVC"
                    , SUM(IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH") AS "SO_LUONG_TON_THEO_DVC"
                    , 0                                          AS "DON_GIA_BAN"
                    , NULL                                       AS "SO_LENH_SAN_XUAT"
                FROM so_kho_chi_tiet IL
                    INNER JOIN danh_muc_kho S ON IL."KHO_ID" = S."id"
                    INNER JOIN TMP_DS_VAT_TU_HANG_HOA I ON IL."MA_HANG_ID" = I."MA_HANG_ID"

                    INNER JOIN danh_muc_to_chuc OU ON OU."id" = IL."CHI_NHANH_ID"

                WHERE IL."NGAY_HACH_TOAN" < tu_ngay
                    AND (
                        IL."KHO_ID" = kho_id
                        OR kho_id IS NULL
                        OR kho_id = kho_tat_ca_id
                    )
                    AND (
                        OU."id" = chi_nhanh_id
                        OR (
                            OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                            AND bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
                        )
                    )


                GROUP BY
                    S."id",
                    S."MA_KHO",
                    S."TEN_KHO",
                    I."MA_HANG_ID",
                    I."MA_HANG",
                    I."TEN_HANG",
                    I."DON_VI_TINH"


                UNION ALL

                SELECT
                    IL."ID_CHUNG_TU"
                    , IL."MODEL_CHUNG_TU"
                    , cast(IL."LOAI_CHUNG_TU" AS INT)
                    , S."id"
                    , S."MA_KHO"
                    , S."TEN_KHO"
                    , I."MA_HANG_ID"
                    , I."MA_HANG"
                    , I."TEN_HANG"
                    , IL."NGAY_HACH_TOAN"
                    , IL."NGAY_CHUNG_TU"
                    , IL."SO_CHUNG_TU" AS "SO_CHUNG_TU"
                    , IL."DIEN_GIAI_CHUNG"
                    , I."DVT_ID"
                    , I."DON_VI_TINH"

                    , CASE
                    WHEN IL."DVT_ID" = I."DVT_ID"
                        THEN IL."DON_GIA"
                    ELSE IL."DON_GIA_THEO_DVT_CHINH" /

                        (
                            CASE WHEN I."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                                THEN 1 / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            ELSE I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" END
                        )

                    END              AS "DON_GIA"
                    , SUM(CASE

                        WHEN IL."DVT_ID" = I."DVT_ID"
                            THEN IL."SO_LUONG_NHAP"
                        ELSE

                            CASE WHEN I."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                                THEN
                                    IL."SO_LUONG_NHAP_THEO_DVT_CHINH" / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            ELSE
                                IL."SO_LUONG_NHAP_THEO_DVT_CHINH" * I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            END

                        END)
                    , SUM(IL."SO_TIEN_NHAP")
                    , SUM(CASE

                        WHEN IL."DVT_ID" = I."DVT_ID"
                            THEN IL."SO_LUONG_XUAT"
                        ELSE

                            CASE WHEN I."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                                THEN
                                    IL."SO_LUONG_XUAT_THEO_DVT_CHINH" / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            ELSE
                                IL."SO_LUONG_XUAT_THEO_DVT_CHINH" * I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            END

                        END)
                    , SUM(IL."SO_TIEN_XUAT")
                    , 0
                    , 0
                    , MIN(IL."STT_LOAI_CHUNG_TU")
                    , MIN(IL."THU_TU_TRONG_CHUNG_TU")
                    ,SUM(IL."SO_LUONG_NHAP_THEO_DVT_CHINH") AS "SO_LUONG_NHAP_THEO_DVC"
                , SUM(IL."SO_LUONG_XUAT_THEO_DVT_CHINH") AS "SO_LUONG_XUAT_THEO_DVC"
                    , SUM(IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH") AS "SO_LUONG_TON_THEO_DVC"
                    ,  CASE WHEN SL."DVT_ID" IS NULL THEN SL."DON_GIA"
                                        WHEN IL."DVT_ID" = I."DVT_ID" THEN SL."DON_GIA"
                                        ELSE SL."DON_GIA_BAN"
                                    END AS "DON_GIA_BAN"
                    , IPO."SO_LENH"

                FROM so_kho_chi_tiet IL
                    INNER JOIN danh_muc_kho S ON IL."KHO_ID" = S."id"
                    INNER JOIN TMP_DS_VAT_TU_HANG_HOA I ON IL."MA_HANG_ID" = I."MA_HANG_ID"
                    INNER JOIN danh_muc_to_chuc OU ON OU."id" = IL."CHI_NHANH_ID"

                    LEFT JOIN res_partner AO ON AO."id" = IL."DOI_TUONG_ID"
                    LEFT JOIN danh_muc_to_chuc AS OBJ ON OBJ."id" = IL."DON_VI_ID"

                    LEFT JOIN TMP_BAN_HANG_CHI_TIET SL ON IL."MA_HANG_ID" = SL."MA_HANG_BAN_ID"
                                                        AND IL."CHI_TIET_ID" = SL."CHI_TIET_ID"

                    LEFT JOIN (SELECT DISTINCT *
                            FROM TMP_LUU_QUAN_HE_NHAP_XUAT_KHO_VT_VOI_HOA_DON) INV
                        ON INV."NHAP_XUAT_KHO_ID" = IL."ID_CHUNG_TU"
                        AND (
                            INV."NHAP_XUAT_KHO_CHI_TIET_ID" IS NULL
                            OR (
                                INV."NHAP_XUAT_KHO_CHI_TIET_ID" IS NOT NULL
                                AND INV."NHAP_XUAT_KHO_CHI_TIET_ID" = IL."CHI_TIET_ID"
                            )
                        )
                    LEFT JOIN stock_ex_lenh_san_xuat IPO ON IPO.id = IL."CHUNG_TU_LENH_SAN_XUAT_ID"

                WHERE IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                    AND (
                        IL."KHO_ID" = kho_id
                        OR kho_id IS NULL
                        OR kho_id = kho_tat_ca_id
                    )
                    AND (
                        OU."id" = chi_nhanh_id
                        OR (
                            OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                            AND bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
                        )
                    )

                GROUP BY
                    IL."ID_CHUNG_TU",
                    IL."MODEL_CHUNG_TU",
                    cast(IL."LOAI_CHUNG_TU" AS INT),
                    S."id",
                    S."MA_KHO",
                    S."TEN_KHO",
                    I."MA_HANG_ID",
                    I."MA_HANG",
                    I."TEN_HANG",
                    IL."NGAY_HACH_TOAN",
                    IL."NGAY_CHUNG_TU",
                    IL."SO_CHUNG_TU",
                    IL."DIEN_GIAI_CHUNG",
                    I."DVT_ID",

                    I."DON_VI_TINH"

                    ,
                    CASE
                    WHEN IL."DVT_ID" = I."DVT_ID"
                        THEN IL."DON_GIA"
                    ELSE IL."DON_GIA_THEO_DVT_CHINH" /

                        (
                            CASE WHEN I."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                                THEN 1 / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                            ELSE I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" END
                        )

                    END
                    ,  CASE WHEN SL."DVT_ID" IS NULL THEN SL."DON_GIA"
                                        WHEN IL."DVT_ID" = I."DVT_ID" THEN SL."DON_GIA"
                                        ELSE SL."DON_GIA_BAN"
                                    END
                    , IPO."SO_LENH"
                    ,IL."MA_TK_CO"


                ORDER BY
                    "MA_KHO" NULLS FIRST ,
                    "MA_HANG" NULLS FIRST,
                    "NGAY_HACH_TOAN" NULLS FIRST,
                    "STT_LOAI_CHUNG_TU" NULLS FIRST,
                    "NGAY_CHUNG_TU" NULLS FIRST,
                    "SO_CHUNG_TU" NULLS FIRST,
                    "STT" NULLS FIRST
            ;


            FOR rec IN SELECT * FROM TMP_KET_QUA

                    ORDER BY RowNum
            LOOP


                SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
                    THEN rec."GIA_TRI_TON"
                        WHEN KHO_ID_TMP <> rec."MA_KHO_ID"
                            OR VAT_TU_HH_TMP <> rec."MA_HANG_ID"
                            THEN rec."GIA_TRI_NHAP" - rec."GIA_TRI_XUAT"
                        ELSE GIA_TRI_TON_TMP + rec."GIA_TRI_NHAP" - rec."GIA_TRI_XUAT"
                        END)
                INTO GIA_TRI_TON_TMP
            ;

                rec."GIA_TRI_TON" = GIA_TRI_TON_TMP
            ;

                UPDATE TMP_KET_QUA
                SET "GIA_TRI_TON" = rec."GIA_TRI_TON"
                WHERE RowNum = rec.RowNum
            ;


                SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
                    THEN rec."SO_LUONG_TON"
                        WHEN KHO_ID_TMP <> rec."MA_KHO_ID"
                            OR VAT_TU_HH_TMP <> rec."MA_HANG_ID"
                            THEN rec."SO_LUONG_NHAP" - rec."SO_LUONG_XUAT"
                        ELSE SO_LUONG_TON_TMP + rec."SO_LUONG_NHAP" - rec."SO_LUONG_XUAT"
                        END)
                INTO SO_LUONG_TON_TMP
            ;

            rec."SO_LUONG_TON" = SO_LUONG_TON_TMP
            ;

                UPDATE TMP_KET_QUA
                SET "SO_LUONG_TON" = rec."SO_LUONG_TON"
                WHERE RowNum = rec.RowNum
            ;


                SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
                    THEN rec."SO_LUONG_TON_THEO_DVC"
                        WHEN KHO_ID_TMP <> rec."MA_KHO_ID"
                            OR VAT_TU_HH_TMP <> rec."MA_HANG_ID"
                            THEN rec."SO_LUONG_NHAP_THEO_DVC" - rec."SO_LUONG_XUAT_THEO_DVC"
                        ELSE SO_LUONG_TON_THEO_DVC_TMP + rec."SO_LUONG_NHAP_THEO_DVC" - rec."SO_LUONG_XUAT_THEO_DVC"
                        END)
                INTO  SO_LUONG_TON_THEO_DVC_TMP
            ;

            rec."SO_LUONG_TON_THEO_DVC" = SO_LUONG_TON_THEO_DVC_TMP
            ;

                UPDATE TMP_KET_QUA
                SET "SO_LUONG_TON_THEO_DVC" = rec."SO_LUONG_TON_THEO_DVC"
                WHERE RowNum = rec.RowNum
            ;

                KHO_ID_TMP = rec."MA_KHO_ID"
            ;

                VAT_TU_HH_TMP = rec."MA_HANG_ID"
            ;

            END LOOP


            ;


        DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
            ;

            CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS

                        SELECT
                                row_number()
                                OVER (
                                    ORDER BY  "MA_KHO" ,
                                "MA_HANG" ,
                                "NGAY_HACH_TOAN" ,
                                "STT_LOAI_CHUNG_TU" ,

                                CASE WHEN "LOAI_CHUNG_TU"=611 THEN "THU_TU_TRONG_CHUNG_TU" ELSE 0 END ,
                                "NGAY_CHUNG_TU" ,
                                "SO_CHUNG_TU" ,
                                "THU_TU_TRONG_CHUNG_TU" ) AS "ROWNUM",
                                "ID_CHUNG_TU" ,
                                "MODEL_CHUNG_TU" ,
                                "LOAI_CHUNG_TU" ,
                                "MA_KHO_ID" ,
                                "MA_KHO" ,
                                "TEN_KHO" ,
                                "MA_HANG_ID" ,
                                "MA_HANG" ,
                                "TEN_HANG" ,
                                "NGAY_HACH_TOAN" ,
                                "NGAY_CHUNG_TU" ,
                                "SO_CHUNG_TU" ,
                                "DIEN_GIAI" ,
                                "DVT" ,

                                ROUND(CAST(COALESCE(CASE WHEN "ID_CHUNG_TU" IS NULL
                                        AND "SO_LUONG_TON" <> 0
                                    THEN CAST("GIA_TRI_TON" / "SO_LUONG_TON" AS DECIMAL(22,8))
                                    WHEN "LOAI_CHUNG_TU" IN ( 3040, 3041, 3042, 3043, 3402 ) THEN 0
                                    ELSE "DON_GIA"
                                END,0)AS NUMERIC), PHAN_THAP_PHAN_DON_GIA) AS "DON_GIA" ,
                                ROUND(CAST(COALESCE("SO_LUONG_NHAP",0)AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_NHAP",
                                ROUND(CAST(COALESCE("GIA_TRI_NHAP",0)AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP",
                                ROUND(CAST(COALESCE("SO_LUONG_XUAT",0)AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_XUAT",
                                ROUND(CAST(COALESCE("GIA_TRI_XUAT",0)AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT",
                                ROUND(CAST(COALESCE("SO_LUONG_TON",0)AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_TON",
                                ROUND(CAST(COALESCE("GIA_TRI_TON",0)AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_TON",

                                RowNum ,
                                "STT_LOAI_CHUNG_TU" ,

                                "THU_TU_TRONG_CHUNG_TU"

                        FROM    TMP_KET_QUA

                            LEFT JOIN (SELECT "MA_HANG_ID" AS  "MA_HANG_ID_TEMP","MA_KHO_ID" "MA_KHO_ID_TEMP" FROM TMP_KET_QUA
                                                WHERE   "SO_LUONG_NHAP" <> 0
                                                OR "GIA_TRI_NHAP" <> 0
                                                OR "SO_LUONG_XUAT" <> 0
                                                OR "GIA_TRI_XUAT" <> 0
                                    GROUP BY "MA_HANG_ID","MA_KHO_ID") Movement ON TMP_KET_QUA."MA_HANG_ID"=Movement."MA_HANG_ID_TEMP"  AND TMP_KET_QUA."MA_KHO_ID"=Movement."MA_KHO_ID_TEMP"
                        WHERE



                                (

                                        (
                                        "ID_CHUNG_TU" IS NULL
                                        AND (
                                                "GIA_TRI_TON" <> 0
                                                OR "SO_LUONG_TON" <> 0
                                                OR "SO_LUONG_TON_THEO_DVC" <> 0

                                        )

                                        OR (
                                            "ID_CHUNG_TU" IS NOT NULL
                                            AND (
                                                "SO_LUONG_NHAP" <> 0
                                                OR "GIA_TRI_NHAP" <> 0
                                                OR "SO_LUONG_XUAT" <> 0
                                                OR "GIA_TRI_XUAT" <> 0
                                                OR "SO_LUONG_TON" <> 0
                                                OR "SO_LUONG_TON_THEO_DVC" <> 0
                                                OR "GIA_TRI_TON" <> 0
                                                )
                                        )

                                    )
                            )

                                        AND   (co_nhap_xuat_ton=1  OR (Movement."MA_HANG_ID_TEMP" IS NOT NULL AND co_nhap_xuat_ton=0))



                        ORDER BY
                                "MA_KHO" ,
                                "MA_HANG" ,
                                "NGAY_HACH_TOAN" ,
                                "STT_LOAI_CHUNG_TU" ,

                                CASE WHEN "LOAI_CHUNG_TU"=611 THEN "THU_TU_TRONG_CHUNG_TU" ELSE 0 END ,
                                "NGAY_CHUNG_TU" ,
                                "SO_CHUNG_TU" ,
                                "THU_TU_TRONG_CHUNG_TU" ;

        END $$
        ;


            SELECT *
            FROM TMP_KET_QUA_CUOI_CUNG --WHERE  "SO_CHUNG_TU" ='0122101' and "MA_HANG" ='BAN_PHIM'
            ORDER BY "ROWNUM"
            ;

            -- SELECT *FROM TMP_DS_VAT_TU_HANG_HOA

        
        
        
        
        """


        # records = self.execute(query,params_sql)
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        
        action = self.env.ref('bao_cao.open_report_so_chi_tiet_vat_tu_hang_hoa_khong_chon').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    selection_khong_chon = fields.Selection([
        ('co_nhap_xuat_ton','Có nhập xuất tồn'),
        ('phat_sinh_nhap_xuat','Phát sinh nhập xuất'),
        ], default='co_nhap_xuat_ton',string="Hiển thị")