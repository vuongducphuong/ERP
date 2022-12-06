# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round


class TIEN_LUONG_BANG_LUONG(models.Model):
    _name = 'tien.luong.bang.luong'
    _description = 'Bảng lương'
    _inherit = ['mail.thread']
    _order = "NAM desc, THANG desc"

    THANG = fields.Integer(string='Tháng ', help='Tháng ')
    NAM = fields.Integer(string='Năm', help='Năm')
    TONG_SO_TIEN = fields.Float(string='Tổng số tiền', help='Tổng số tiền',digits=decimal_precision.get_precision('VND'),compute='lay_tong_so_tien',store=True)
    LOAI_BANG_LUONG = fields.Char(string='Loại bảng lương', help='Loại bảng lương')
    TEN_BANG_LUONG = fields.Char(string='Tên bảng lương', help='Tên bảng lương')
    name = fields.Char(string='Name', help='Name',related='TEN_BANG_LUONG',oldname='NAME')

    TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS = fields.One2many('tien.luong.bang.luong.chi.tiet', 'CHI_TIET_ID', string='Bảng lương chi tiết')

    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',store=True) 


    # TEN_LOAI_BANG_LUONG = fields.Char(string='Tên loại bảng lương', help='Tên loại bảng lương')
    TEN_LOAI_BANG_LUONG = fields.Selection([
        ('LUONG_CO_DINH', 'Lương cố định(không dựa trên bảng chấm công)'), 
        ('LUONG_THOI_GIAN_THEO_BUOI', 'Lương thời gian theo buổi'), 
        ('LUONG_THOI_GIAN_THEO_GIO', 'Lương thời gian theo giờ'), 
        ('LUONG_TAM_UNG', 'Lương tạm ứng'), ], string='Tên loại bảng lương', help='Tên loại bảng lương',default='LUONG_CO_DINH', required=True)

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    @api.depends('TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS')
    def lay_tong_so_tien(self):
        for record in self:
            tong_so_tien = 0
            if record.TEN_LOAI_BANG_LUONG == 'LUONG_CO_DINH' or record.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_BUOI' or record.TEN_LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_GIO':
                for line in record.TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS:
                    tong_so_tien += line.SO_TIEN_CON_DUOC_LINH
            else:
                for line in record.TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS:
                    tong_so_tien += line.SO_TIEN_TAM_UNG

            record.TONG_SO_TIEN = tong_so_tien

    @api.model
    def default_get(self, fields):
        rec = super(TIEN_LUONG_BANG_LUONG, self).default_get(fields)
        thang = self._context.get('default_THANG')
        nam = self._context.get('default_NAM')
        ten_loai_bang_luong = self._context.get('default_TEN_LOAI_BANG_LUONG')
        rec['TEN_LOAI_BANG_LUONG'] = ten_loai_bang_luong
        loai_chung_tu = 0
        if ten_loai_bang_luong == 'LUONG_CO_DINH':
            rec['LOAI_BANG_LUONG'] = 'Bảng lương cố định(không dựa trên bảng chấm công)'
            rec['LOAI_CHUNG_TU'] = 6020
            loai_chung_tu = 6020
        elif ten_loai_bang_luong == 'LUONG_THOI_GIAN_THEO_BUOI':
            rec['LOAI_CHUNG_TU'] = 6021
            rec['LOAI_BANG_LUONG'] = 'Bảng lương thời gian theo buổi'
            loai_chung_tu = 6021
        elif ten_loai_bang_luong == 'LUONG_THOI_GIAN_THEO_GIO':
            rec['LOAI_CHUNG_TU'] = 6022
            rec['LOAI_BANG_LUONG'] ='Bảng lương thời gian theo giờ'
            loai_chung_tu = 6022
        else:
            rec['LOAI_CHUNG_TU'] = 6023
            rec['LOAI_BANG_LUONG'] ='Bảng lương tạm ứng'
            loai_chung_tu = 6023
        rec['THANG'] = thang
        rec['NAM'] = nam

        default_arr_list_don_vi = self._context.get('default_arr_list_don_vi')
        hinh_thuc_tao_bang_luong = self._context.get('default_hinh_thuc_tao_bang_luong')
        
        #sql tra ve 1 list employees
        if hinh_thuc_tao_bang_luong:
            default_TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI = self._context.get('default_TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI')
            default_LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI = self._context.get('default_LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI')
            nhan_vien_list = []
            arr_list_don_vi = []
            bang_luong_id = 0
            tao_moi_hoan_toan = 0
            if default_arr_list_don_vi:
                arr_list_don_vi = default_arr_list_don_vi

            if hinh_thuc_tao_bang_luong == 'TAO_MOI_HOAN_TOAN':
                bang_luong_id = 0
                tao_moi_hoan_toan = 1
            elif hinh_thuc_tao_bang_luong == 'DUA_TREN_BANG_LUONG_KHAC':
                bang_luong_id = self._context.get('default_bang_luong_id')
                tao_moi_hoan_toan = 0
            
            # trả về một danh sách nhân viên
            danh_sach_nhan_viens = self.lay_thong_tin_bang_luong_tich_chon_dua_tren_bang_luong_khac(thang, nam, \
                                            default_TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI, default_LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI, \
                                            bang_luong_id, arr_list_don_vi, loai_chung_tu, tao_moi_hoan_toan)
                                    # lay_thong_tin_bang_luong_tich_chon_dua_tren_bang_luong_khac(self,thang,nam,tu_dong_them_nv_moi,lay_ca_nhan_vien_ngung_theo_doi,id_bang_luong_khac,list_don_vi,loai_chung_tu,tao_moi_hoan_toan):

            field_name = ['DON_VI_ID','PHONG_BAN','MA_NHAN_VIEN','TEN_NHAN_VIEN','CHUC_DANH','LUONG_CO_BAN','LUONG_DONG_BH','GIAM_TRU_GIA_CANH','TEN_LOAI_BANG_LUONG'] 
            field_onchange = self.TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS.get_field_onchange()
            for nhan_vien in danh_sach_nhan_viens:
                line_data = {
                    'STT' : nhan_vien.get('rownumber'),
                    'DON_VI_ID' : nhan_vien.get('DON_VI_ID'),
                    'PHONG_BAN': nhan_vien.get('TEN_DON_VI_SORT'),
                    'MA_NHAN_VIEN': nhan_vien.get('NHAN_VIEN_ID'),
                    'TEN_NHAN_VIEN' :nhan_vien.get('TEN_NHAN_VIEN'),
                    'CHUC_DANH' :nhan_vien.get('CHUC_DANH'),
                    'LUONG_CO_BAN' :nhan_vien.get('LUONG_CO_BAN'),
                    'LUONG_DONG_BH' :nhan_vien.get('LUONG_DONG_BH'),
                    'GIAM_TRU_GIA_CANH' :self.ham_tinh_giam_tru_gia_canh(nhan_vien.get('NHAN_VIEN_ID')),
                    'TEN_LOAI_BANG_LUONG': ten_loai_bang_luong,
                    'THUE_TNCN_KHAU_TRU' :self.static_PersonalIncomeTax(nhan_vien.get('THU_NHAP_TINH_THUE_TNCN')),
                }
                line_data = self.TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS.update_by_onchange(line_data, field_name, field_onchange)
                nhan_vien_list += [(0,0,line_data)]

            rec ['TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS'] = nhan_vien_list
        return rec
   
    def ham_tinh_giam_tru_gia_canh(self,nhan_vien_id):
        #Giảm trừ gia cảnh = Giảm trừ bản thân + Giảm trừ phụ thuộc * số người phụ thuộc (Kiểm tra nhân viên)
        env_quy_dinh_luong_bh_thue= self.env['tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'].search([],limit=1)
        giam_tru_gia_canh = 0
        so_nguoi_phu_thuoc = 0 
        giam_tru_ban_than = 0 
        nhan_vien = self.env['res.partner'].search([('id','=', nhan_vien_id)],limit=1)
        if nhan_vien:
            so_nguoi_phu_thuoc = nhan_vien.SO_NGUOI_PHU_THUOC
        if env_quy_dinh_luong_bh_thue:
            giam_tru_ban_than= env_quy_dinh_luong_bh_thue.THUE_GIAM_TRU_BAN_THAN
            giam_tru_phu_thuoc= env_quy_dinh_luong_bh_thue.THUE_GIAM_TRU_NGUOI_PHU_THUOC
            giam_tru_gia_canh = giam_tru_ban_than + (giam_tru_phu_thuoc * so_nguoi_phu_thuoc)
        return giam_tru_gia_canh

    # param: thu_nhap_chiu_thue = Phần thu nhập sau khi đã giảm trừ
    # Todo: Tạm thời fixed các mốc trong biểu thuế để Mạnh test hàm trước
    def static_PersonalIncomeTax(self, thu_nhap_chiu_thue):
        personalIncomeTax = 0
        if thu_nhap_chiu_thue <= 0:
            return personalIncomeTax
        if thu_nhap_chiu_thue <= 5000000:
            personalIncomeTax = thu_nhap_chiu_thue * 0.05
        elif thu_nhap_chiu_thue <= 10000000:
            personalIncomeTax = (thu_nhap_chiu_thue - 5000000) * 0.1 + 250000
        elif thu_nhap_chiu_thue <= 18000000:
            personalIncomeTax = (thu_nhap_chiu_thue - 10000000) * 0.15 + 750000
        elif thu_nhap_chiu_thue <= 32000000:
            personalIncomeTax = (thu_nhap_chiu_thue - 18000000) * 0.2 + 1950000
        elif thu_nhap_chiu_thue <= 52000000:
            personalIncomeTax = (thu_nhap_chiu_thue - 32000000) * 0.25 + 4750000
        elif thu_nhap_chiu_thue <= 80000000:
            personalIncomeTax = (thu_nhap_chiu_thue - 52000000) * 0.30 + 9750000
        else:
            personalIncomeTax = (thu_nhap_chiu_thue - 80000000) * 0.35 + 18150000
        return round(personalIncomeTax)

    def lay_thong_tin_bang_luong_tich_chon_dua_tren_bang_luong_khac(self,thang,nam,tu_dong_them_nv_moi,lay_ca_nhan_vien_ngung_theo_doi,id_bang_luong_khac,list_don_vi,loai_chung_tu,tao_moi_hoan_toan):
        sql_param={
            'thang': int(thang),
            'nam': int(nam),
            'tu_dong_them_nv_moi': tu_dong_them_nv_moi,
            'lay_ca_nhan_vien_ngung_theo_doi': lay_ca_nhan_vien_ngung_theo_doi ,
            'id_bang_luong_khac': id_bang_luong_khac ,
            'list_don_vi': list_don_vi ,
            'loai_chung_tu': loai_chung_tu ,
            'tao_moi_hoan_toan': tao_moi_hoan_toan ,
        }
        query = """
        DO LANGUAGE plpgsql $$
DECLARE

    thang                           INTEGER := %(thang)s;


    nam                             INTEGER := %(nam)s;

    RefFollowID                     INTEGER := %(id_bang_luong_khac)s;

    --RefFollowID


    tu_dong_them_nhan_vien_moi      BOOLEAN := %(tu_dong_them_nv_moi)s;

    --@AddNewEmployee

    lay_ca_nhan_vien_ngung_theo_doi BOOLEAN := %(lay_ca_nhan_vien_ngung_theo_doi)s;

    --@AddInactiveEmployee

    tao_dua_tren_bang_luong_san_co  INTEGER := %(tao_moi_hoan_toan)s;

    --@IsCreateNew

    so_du_hien_thi_141              BOOLEAN :=TRUE;

    --@IsDisplayBalance141

    loai_chung_tu                   INTEGER := %(loai_chung_tu)s;

    LUONG_CO_BAN_DUA_TREN           VARCHAR(128);

    so_du_141                       DECIMAL(18, 4);

    chi_tiet_boi_tai_tai_khoan      BOOLEAN;

    tinh_chat                       INTEGER;

    tai_khoan_141                   VARCHAR(10);

    chi_nhanh_id                    INTEGER;

    ngay_gan                        TIMESTAMP;

    ngay_bat_dau                    TIMESTAMP;

    la_ngoai_le_141                 BOOLEAN;

    so_tien_tam_ung                 DECIMAL(18, 4);

    rec                             RECORD;

BEGIN

    DROP TABLE IF EXISTS TMP_DON_VI
    ;
    CREATE TEMP TABLE TMP_DON_VI

    (
        "DON_VI_ID" INT
    )
    ;
    INSERT INTO TMP_DON_VI
        SELECT id
        FROM danh_muc_to_chuc
        WHERE id = any(%(list_don_vi)s) --@OrganizationUnitID
    ;
    DROP TABLE IF EXISTS TMP_KET_QUA
    ;
    CREATE TEMP TABLE TMP_KET_QUA
    (
        "TIEN_LUONG_BANG_LUONG_CHI_TIET_ID" INT            NOT NULL,
        "ID_CHUNG_TU"                       INT            NOT NULL,
        "STT"                               INT            NOT NULL,
        "NHAN_VIEN_ID"                      INT            NULL,
        "DON_VI_ID"                         INT            NULL,
        "HE_SO_LUONG"                       DECIMAL(18, 4) NULL,
        "LUONG_CO_BAN"                      DECIMAL(18, 4) NULL,
        "DON_GIA_NGAY_CONG"                 DECIMAL(18, 4) NULL,
        "DON_GIA_GIO_CONG"                  DECIMAL(18, 4) NULL,
        "SO_CONG_HUONG"                 DECIMAL(18, 4) NULL,
        "SO_TIEN_HUONG"                     DECIMAL(18, 4) NULL,
        "SO_CONG_KHONG_HUONG"          DECIMAL(18, 4) NULL,
        "SO_TIEN_KHONG_HUONG"               DECIMAL(18, 4) NULL,
        "SO_GIO_CONG_LAM_THEM"              DECIMAL(18, 4) NULL,
        "SO_TIEN_LAM_THEM"                  DECIMAL(18, 4) NULL,
        "PHU_CAP_THUOC_QUY_LUONG"           DECIMAL(18, 4) NULL,
        "PHU_CAP_KHAC"                      DECIMAL(18, 4) NULL,
        "TONG_SO"                           DECIMAL(18, 4) NOT NULL,
        "BHXH_KHAU_TRU"                     DECIMAL(18, 4) NULL,
        "BHYT_KHAU_TRU"                     DECIMAL(18, 4) NULL,
        "BHTN_KHAU_TRU"                     DECIMAL(18, 4) NULL,
        "THUE_TNCN_KHAU_TRU"                DECIMAL(18, 4) NULL,
        "TONG_THU_NHAP_CHIU_THUE_TNCN" DECIMAL(18, 4) NULL,
        "CONG_KHAU_TRU"                     DECIMAL(18, 4) NULL,
        "GIAM_TRU_GIA_CANH"                 DECIMAL(18, 4) NULL,
        "THU_NHAP_TINH_THUE_TNCN"           DECIMAL(18, 4) NULL,
        "KY_NHAN"                           VARCHAR(128)   NULL,

        "SO_TIEN_TAM_UNG"                   DECIMAL(18, 4) NULL,
        "TAM_UNG_141"                       DECIMAL(18, 4) NULL,
        "LUONG_DONG_BH"                     DECIMAL(18, 4) NULL,
        "KPCD_KHAU_TRU"                     DECIMAL(18, 4) NULL,
        "SO_TIEN_CON_DUOC_LINH"             DECIMAL(18, 4) NULL,
        "BHXH_CONG_TY_DONG"                 DECIMAL(18, 4) NULL,
        "BHYT_CONG_TY_DONG"                 DECIMAL(18, 4) NULL,
        "BHTN_CONG_TY_DONG"                 DECIMAL(18, 4) NULL,
        "KPCD_CONG_TY_DONG"                 DECIMAL(18, 4) NULL,
        "MA_NHAN_VIEN"                      VARCHAR(25),
        "TEN_NHAN_VIEN"                     VARCHAR(128),
        "CHUC_DANH"                         VARCHAR(128),
        "TEN_DON_VI"                        VARCHAR(255),
        "TEN_DON_VI_SORT"                   VARCHAR(255)
    )
    ;

    SELECT value
    INTO LUONG_CO_BAN_DUA_TREN
    FROM ir_config_parameter
    WHERE key = 'he_thong.LUONG_CO_BAN_DUA_TREN'
    FETCH FIRST 1 ROW ONLY
    ;


    IF tao_dua_tren_bang_luong_san_co = 0 --Tạo dựa trên bảng lương sẵn có
    THEN

        IF tu_dong_them_nhan_vien_moi = FALSE
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    PSSD."id"
                    , PSSD."CHI_TIET_ID"
                    , PSSD."STT"
                    , AO."id"                         AS                           "NHAN_VIEN_ID"
                    , AO."DON_VI_ID"
                    , COALESCE(PSSD."HE_SO_LUONG", 0) AS                           "HE_SO_LUONG"
                    , CASE WHEN LUONG_CO_BAN_DUA_TREN = 'LUONG_THOA_THUAN'
                    THEN COALESCE(AO."LUONG_THOA_THUAN", 0)
                      ELSE COALESCE(PSSD."LUONG_CO_BAN", 0)
                      END                             AS                           "LUONG_CO_BAN"
                    , COALESCE("DON_GIA_NGAY_CONG",
                               CAST(0 AS DECIMAL))                                 "DON_GIA_NGAY_CONG"
                    , COALESCE("DON_GIA_GIO_CONG",
                               CAST(0 AS DECIMAL))                                 "DON_GIA_GIO_CONG"
                    , COALESCE("SO_CONG_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_CONG_HUONG"
                    , COALESCE("SO_TIEN_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_TIEN_HUONG"
                    , COALESCE("SO_CONG_KHONG_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_CONG_KHONG_HUONG"
                    , COALESCE("SO_TIEN_KHONG_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_TIEN_KHONG_HUONG"
                    , COALESCE("SO_GIO_CONG_LAM_THEM", CAST(0 AS DECIMAL))         "SO_GIO_CONG_LAM_THEM"
                    , COALESCE("SO_TIEN_LAM_THEM", CAST(0 AS DECIMAL))             "SO_TIEN_LAM_THEM"
                    , COALESCE("PHU_CAP_THUOC_QUY_LUONG",
                               CAST(0 AS DECIMAL))                                 "PHU_CAP_THUOC_QUY_LUONG"
                    , COALESCE("PHU_CAP_KHAC", CAST(0 AS DECIMAL))                 "PHU_CAP_KHAC"
                    , COALESCE("TONG_SO", CAST(0 AS DECIMAL))                      "TONG_SO"
                    , COALESCE("BHXH_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "BHXH_KHAU_TRU"
                    , COALESCE("BHYT_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "BHYT_KHAU_TRU"
                    , COALESCE("BHTN_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "BHTN_KHAU_TRU"
                    , COALESCE("THUE_TNCN_KHAU_TRU", CAST(0 AS DECIMAL))           "THUE_TNCN_KHAU_TRU"
                    , COALESCE("TONG_THU_NHAP_CHIU_THUE_TNCN", CAST(0 AS DECIMAL)) "TONG_THU_NHAP_CHIU_THUE_TNCN"
                    , COALESCE("CONG_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "CONG_KHAU_TRU"
                    , COALESCE("GIAM_TRU_GIA_CANH",
                               CAST(0 AS DECIMAL))                                 "GIAM_TRU_GIA_CANH"
                    , COALESCE("THU_NHAP_TINH_THUE_TNCN",
                               CAST(0 AS DECIMAL))                                 "THU_NHAP_TINH_THUE_TNCN"
                    , COALESCE("KY_NHAN", '')                                      "KY_NHAN"

                    , COALESCE("SO_TIEN_TAM_UNG",
                               CAST(0 AS DECIMAL))                                 "SO_TIEN_TAM_UNG"
                    , COALESCE("TAM_UNG_141",
                               CAST(0 AS DECIMAL))                                 "TAM_UNG_141"
                    , COALESCE("LUONG_DONG_BH",
                               COALESCE(AO."LUONG_DONG_GOP_BH", 0))                "LUONG_DONG_BH"
                    , COALESCE("KPCD_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "KPCD_KHAU_TRU"
                    , COALESCE("SO_TIEN_CON_DUOC_LINH", CAST(0 AS DECIMAL))        "SO_TIEN_CON_DUOC_LINH"
                    , COALESCE("BHXH_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "BHXH_CONG_TY_DONG"
                    , COALESCE("BHYT_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "BHYT_CONG_TY_DONG"
                    , COALESCE("BHTN_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "BHTN_CONG_TY_DONG"
                    , COALESCE("KPCD_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "KPCD_CONG_TY_DONG"
                    , AO."MA"                         AS                           "MA_NHAN_VIEN"
                    , AO."HO_VA_TEN"                  AS                           "TEN_NHAN_VIEN"
                    , AO."CHUC_DANH"
                    , OU."TEN_DON_VI"
                    , (OU."MA_DON_VI" || ' - '
                       || OU."TEN_DON_VI")            AS                           "TEN_DON_VI_SORT"
                FROM tien_luong_bang_luong_chi_tiet AS PSSD
                    INNER JOIN TMP_DON_VI AS G ON G."DON_VI_ID" = PSSD."DON_VI_ID"
                    INNER JOIN res_partner AS AO ON PSSD."MA_NHAN_VIEN" = AO."id"
                                                    AND "LA_NHAN_VIEN" = TRUE
                                                    AND (AO."active" = TRUE
                                                         OR AO."active" = lay_ca_nhan_vien_ngung_theo_doi
                                                    )
                    INNER JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"
                WHERE "CHI_TIET_ID" = RefFollowID
            ;
        ELSE
            -- Tự động thêm nhân viên mới

            INSERT INTO TMP_KET_QUA
                SELECT
                      0                                                            "TIEN_LUONG_BANG_LUONG_CHI_TIET_ID"
                    , 0                                                            "ID_CHUNG_TU"
                    , 0                                       AS                   "STT"
                    , AO."id"                                 AS                   "NHAN_VIEN_ID"
                    , AO."DON_VI_ID"
                    , COALESCE(D."HE_SO_LUONG",
                               COALESCE(AO."HE_SO_LUONG", 0)) AS                   "HE_SO_LUONG"
                    , CASE WHEN LUONG_CO_BAN_DUA_TREN = 'LUONG_THOA_THUAN'
                    THEN COALESCE(AO."LUONG_THOA_THUAN", 0)
                      ELSE (CASE WHEN D."MA_NHAN_VIEN" IS NULL
                          THEN COALESCE(AO."LUONG_DONG_GOP_BH", 0)
                            ELSE COALESCE(D."LUONG_CO_BAN", 0)
                            END)
                      END                                     AS                   "LUONG_CO_BAN"
                    , COALESCE("DON_GIA_NGAY_CONG",
                               CAST(0 AS DECIMAL))                                 "DON_GIA_NGAY_CONG"
                    , COALESCE("DON_GIA_GIO_CONG",
                               CAST(0 AS DECIMAL))                                 "DON_GIA_GIO_CONG"
                    , COALESCE("SO_CONG_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_CONG_HUONG"
                    , COALESCE("SO_TIEN_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_TIEN_HUONG"
                    , COALESCE("SO_CONG_KHONG_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_CONG_KHONG_HUONG"
                    , COALESCE("SO_TIEN_KHONG_HUONG",
                               CAST(0 AS DECIMAL))                                 "SO_TIEN_KHONG_HUONG"
                    , COALESCE("SO_GIO_CONG_LAM_THEM", CAST(0 AS DECIMAL))         "SO_GIO_CONG_LAM_THEM"
                    , COALESCE("SO_TIEN_LAM_THEM", CAST(0 AS DECIMAL))             "SO_TIEN_LAM_THEM"
                    , COALESCE("PHU_CAP_THUOC_QUY_LUONG",
                               CAST(0 AS DECIMAL))                                 "PHU_CAP_THUOC_QUY_LUONG"
                    , COALESCE("PHU_CAP_KHAC", CAST(0 AS DECIMAL))                 "PHU_CAP_KHAC"
                    , COALESCE("TONG_SO", CAST(0 AS DECIMAL))                      "TONG_SO"
                    , COALESCE("BHXH_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "BHXH_KHAU_TRU"
                    , COALESCE("BHYT_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "BHYT_KHAU_TRU"
                    , COALESCE("BHTN_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "BHTN_KHAU_TRU"
                    , COALESCE("THUE_TNCN_KHAU_TRU", CAST(0 AS DECIMAL))           "THUE_TNCN_KHAU_TRU"
                    , COALESCE("TONG_THU_NHAP_CHIU_THUE_TNCN", CAST(0 AS DECIMAL)) "TONG_THU_NHAP_CHIU_THUE_TNCN"
                    , COALESCE("CONG_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "CONG_KHAU_TRU"
                    , COALESCE("GIAM_TRU_GIA_CANH",
                               CAST(0 AS DECIMAL))                                 "GIAM_TRU_GIA_CANH"
                    , COALESCE("THU_NHAP_TINH_THUE_TNCN",
                               CAST(0 AS DECIMAL))                                 "THU_NHAP_TINH_THUE_TNCN"
                    , COALESCE("KY_NHAN", '')                                      "KY_NHAN"

                    , COALESCE("SO_TIEN_TAM_UNG",
                               CAST(0 AS DECIMAL))                                 "SO_TIEN_TAM_UNG"
                    , COALESCE("TAM_UNG_141",
                               CAST(0 AS DECIMAL))                                 "TAM_UNG_141"
                    , COALESCE("LUONG_DONG_BH",
                               COALESCE(AO."LUONG_DONG_GOP_BH", 0))                "LUONG_DONG_BH"
                    , COALESCE("KPCD_KHAU_TRU",
                               CAST(0 AS DECIMAL))                                 "KPCD_KHAU_TRU"
                    , COALESCE("SO_TIEN_CON_DUOC_LINH", CAST(0 AS DECIMAL))        "SO_TIEN_CON_DUOC_LINH"
                    , COALESCE("BHXH_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "BHXH_CONG_TY_DONG"
                    , COALESCE("BHYT_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "BHYT_CONG_TY_DONG"
                    , COALESCE("BHTN_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "BHTN_CONG_TY_DONG"
                    , COALESCE("KPCD_CONG_TY_DONG",
                               CAST(0 AS DECIMAL))                                 "KPCD_CONG_TY_DONG"
                    , AO."MA"                                 AS                   "MA_NHAN_VIEN"
                    , AO."HO_VA_TEN"                          AS                   "TEN_NHAN_VIEN"
                    , AO."CHUC_DANH"
                    , OU."TEN_DON_VI"
                    , (OU."MA_DON_VI" || ' - '
                       || OU."TEN_DON_VI")                    AS                   "TEN_DON_VI_SORT"
                FROM res_partner AS AO
                    INNER JOIN TMP_DON_VI AS G ON G."DON_VI_ID" = AO."DON_VI_ID"
                                                  AND "LA_NHAN_VIEN" = TRUE
                                                  AND (AO."active" = TRUE
                                                       OR AO."active" = lay_ca_nhan_vien_ngung_theo_doi
                                                  )
                    LEFT JOIN tien_luong_bang_luong_chi_tiet AS D ON D."MA_NHAN_VIEN" = AO."id"
                                                                     AND "CHI_TIET_ID" = RefFollowID
                    LEFT JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"
            ;


        END IF
        ;

    ELSE --Tạo mới

        INSERT INTO TMP_KET_QUA
            SELECT
                  0                                      "TIEN_LUONG_BANG_LUONG_CHI_TIET_ID"
                , 0                                      "ID_CHUNG_TU"
                , 0                                   AS "STT"
                , AO."id"                             AS "NHAN_VIEN_ID"
                , AO."DON_VI_ID"
                , COALESCE(AO."HE_SO_LUONG", 0)       AS "HE_SO_LUONG"
                , CASE WHEN LUONG_CO_BAN_DUA_TREN = 'LUONG_THOA_THUAN'
                THEN COALESCE(AO."LUONG_THOA_THUAN", 0)
                  ELSE COALESCE(AO."LUONG_DONG_GOP_BH", 0)
                  END                                 AS "LUONG_CO_BAN"
                , CAST(0 AS DECIMAL)                  AS "DON_GIA_NGAY_CONG"
                , CAST(0 AS DECIMAL)                  AS "DON_GIA_GIO_CONG"
                , CAST(0 AS DECIMAL)                  AS "SO_CONG_HUONG"
                , CAST(0 AS DECIMAL)                  AS "SO_TIEN"
                , CAST(0 AS DECIMAL)                  AS "SO_CONG_KHONG_HUONG"
                , CAST(0 AS DECIMAL)                  AS "SO_TIEN"
                , CAST(0 AS DECIMAL)                  AS "SO_GIO_CONG_LAM_THEM"
                , CAST(0 AS DECIMAL)                  AS "SO_TIEN"
                , CAST(0 AS DECIMAL)                  AS "PHU_CAP_THUOC_QUY_LUONG"
                , CAST(0 AS DECIMAL)                  AS "PHU_CAP_KHAC"
                , CAST(0 AS DECIMAL)                  AS "TONG_SO"
                , CAST(0 AS DECIMAL)                  AS "BHXH"
                , CAST(0 AS DECIMAL)                  AS "BHYT"
                , CAST(0 AS DECIMAL)                  AS "BHTN"
                , CAST(0 AS DECIMAL)                  AS "THUE_TNCN_KHAU_TRU"
                , CAST(0 AS DECIMAL)                  AS "TONG_THU_NHAP_CHIU_THUE_TNCN"
                , CAST(0 AS DECIMAL)                  AS "CONG"
                , CAST(0 AS DECIMAL)                  AS "GIAM_TRU_GIA_CANH"
                , CAST(0 AS DECIMAL)                  AS "THU_NHAP_TINH_THUE_TNCN"
                , ''                                  AS "KY_NHAN"

                , CAST(0 AS DECIMAL)                  AS "SO_TIEN_TAM_UNG"
                , CAST(0 AS DECIMAL)                  AS "TAM_UNG_141"
                , COALESCE(AO."LUONG_DONG_GOP_BH", 0) AS "LUONG_DONG_BH"
                , CAST(0 AS DECIMAL)                  AS "KPCD"
                , CAST(0 AS DECIMAL)                  AS "SO_TIEN"
                , CAST(0 AS DECIMAL)                  AS "BHXH"
                , CAST(0 AS DECIMAL)                  AS "BHYT"
                , CAST(0 AS DECIMAL)                  AS "BHTN"
                , CAST(0 AS DECIMAL)                  AS "KPCD"
                , Ao."MA"                             AS "MA_NHAN_VIEN"
                , Ao."HO_VA_TEN"                      AS "TEN_NHAN_VIEN_BAN_HANG"
                , AO."CHUC_DANH"
                , DOU."TEN_DON_VI"
                , (DOU."MA_DON_VI" || ' - '
                   || DOU."TEN_DON_VI")               AS "TEN_DON_VI_SORT"
            FROM res_partner AS AO
                INNER JOIN TMP_DON_VI AS OU ON AO."DON_VI_ID" = OU."DON_VI_ID"
                                               AND "LA_NHAN_VIEN" = TRUE
                                               AND (AO."active" = TRUE)
                INNER JOIN danh_muc_to_chuc DOU ON DOU."id" = OU."DON_VI_ID"
        ;


    END IF
    ;

    ngay_bat_dau = CAST(SUBSTR(CAST(thang AS VARCHAR(10)), 1, 10) || '/1/'
                        || SUBSTR(CAST(nam AS VARCHAR(10)), 1, 10) AS TIMESTAMP)
    ;

    ngay_gan := ngay_bat_dau + INTERVAL '1 month' + INTERVAL '-1 day'
    ;

    tai_khoan_141 = '141'
    ;

    so_du_141 = 0
    ;


    IF EXISTS(SELECT *
              FROM danh_muc_he_thong_tai_khoan
              WHERE "SO_TAI_KHOAN" = tai_khoan_141)
    THEN
        la_ngoai_le_141 = TRUE
        ;
    END IF
    ;

    -- Nếu không phải là Bảng lương tạm ứng
    IF loai_chung_tu <> 6023
    THEN

        SELECT OU."id"
        INTO chi_nhanh_id
        FROM danh_muc_to_chuc OU
            INNER JOIN TMP_DON_VI T ON T."DON_VI_ID" = OU."id"
        ;


        FOR rec IN
        SELECT "NHAN_VIEN_ID" AS "NHAN_VIEN_ID"
        FROM TMP_KET_QUA

        LOOP

            /*Nếu có tài khoản 141*/
            IF la_ngoai_le_141 = TRUE
            THEN

                SELECT "DOI_TUONG"
                INTO chi_tiet_boi_tai_tai_khoan

                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" = tai_khoan_141
                ;

                SELECT "TINH_CHAT"
                INTO tinh_chat
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" = tai_khoan_141
                ;


                -- Nếu có hiển thị cột 141 và TK 141 chi tiết theo Đối tượng thì lấy số liệu lên
                IF so_du_hien_thi_141 = TRUE
                   AND chi_tiet_boi_tai_tai_khoan = TRUE
                THEN
                    SELECT CASE
                           WHEN tinh_chat = '0' --Dư Nợ
                               THEN SUM("GHI_NO")
                                    - SUM("GHI_CO")
                           --Dư có
                           WHEN tinh_chat = '1'
                               THEN SUM("GHI_CO")
                                    - SUM("GHI_NO")
                           -- Lưỡng tính
                           ELSE CASE
                                WHEN SUM("GHI_NO")
                                     - SUM("GHI_CO") > 0
                                    THEN SUM("GHI_NO")
                                         - SUM("GHI_CO")
                                ELSE SUM("GHI_CO")
                                     - SUM("GHI_NO")
                                END
                           END
                    INTO so_du_141
                    FROM so_cong_no_chi_tiet
                    WHERE "NGAY_HACH_TOAN" <= ngay_gan
                          AND "DOI_TUONG_ID" = rec."NHAN_VIEN_ID"
                          AND "CHI_NHANH_ID" = chi_nhanh_id


                          AND ("MA_TK" LIKE '141%%'

                          )
                    ;

                    UPDATE TMP_KET_QUA
                    SET "TAM_UNG_141" = COALESCE(so_du_141,
                                                 0)
                    WHERE "NHAN_VIEN_ID" = rec."NHAN_VIEN_ID"
                    ;

                END IF
                ;
            END IF
        ;


            -- Xử  lý lấy phần Tạm ứng lương trong kỳ
            SELECT SUM("SO_TIEN_TAM_UNG")
            INTO so_tien_tam_ung
            FROM tien_luong_bang_luong_chi_tiet D
                INNER JOIN tien_luong_bang_luong M ON M."id" = D."CHI_TIET_ID"
                                                      AND M."THANG" = thang
                                                      AND M."NAM" = nam
                                                      AND D."MA_NHAN_VIEN" = rec."NHAN_VIEN_ID"
                                                      AND M."LOAI_CHUNG_TU" = 6023
        ;

            UPDATE TMP_KET_QUA
            SET "SO_TIEN_TAM_UNG" = COALESCE(so_tien_tam_ung,
                                             0)
            WHERE "NHAN_VIEN_ID" = rec."NHAN_VIEN_ID"
        ;

        END LOOP
        ;
    END IF
    ;

END $$
;

SELECT ROW_NUMBER()
                                                    OVER (
                                                        ORDER BY  to_chuc."MA_DON_VI",
   ket_qua."TEN_DON_VI",
   ket_qua."TEN_NHAN_VIEN" ) AS RowNumber, ket_qua."TEN_DON_VI",ket_qua.*, to_chuc."MA_DON_VI"
FROM TMP_KET_QUA ket_qua LEFT JOIN  danh_muc_to_chuc to_chuc on ket_qua."DON_VI_ID" = to_chuc.id
ORDER BY
   to_chuc."MA_DON_VI",
   ket_qua."TEN_DON_VI",
   ket_qua."TEN_NHAN_VIEN"
;
        """
        return self.execute(query,sql_param)

    
    
            


     
