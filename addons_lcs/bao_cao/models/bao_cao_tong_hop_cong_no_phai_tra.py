# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA(models.Model):
    _name = 'bao.cao.tong.hop.cong.no.phai.tra'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'),('NHAN_VIEN', 'Nhân viên'), ('CONG_TRINH', 'Công trình'), ('HOP_DONG_MUA', 'Hợp đồng mua'), ('DON_MUA_HANG', 'Đơn mua hàng'), ], string='Thống kê theo', help='Thống kê theo',default="KHONG_CHON", required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default="true")
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default="DAU_THANG_DEN_HIEN_TAI",required=True)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',required=True )
    TU = fields.Date(string='Từ', help='Từ',required=True)
    DEN = fields.Date(string='Đến', help='Đến',required=True)
    NHOM_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm NCC', help='Nhóm nhà cung cấp')
    CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY = fields.Boolean(string='Chỉ lấy nhà cung cấp có số dư và phát sinh trong kỳ', help='Chỉ lấy nhà cung cấp có số dư và phát sinh trong kỳ',default='true')
    MA_NHA_CUNG_CAP = fields.Char(string='Mã nhà cung cấp', help='Mã nhà cung cấp')#, auto_num='bao_cao_tong_hop_cong_no_phai_tra_MA_NHA_CUNG_CAP')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
    TK_CO_ID = fields.Char(string='TK công nợ', help='Tài khoản công nợ')
    NO_SO_DU_DAU_KY = fields.Float(string='Nợ', help='Nợ số dư đầu kỳ',digits= decimal_precision.get_precision('VND'))
    CO_SO_DU_DAU_KY = fields.Float(string='Có', help='Có số dư đầu kỳ',digits= decimal_precision.get_precision('VND'))
    NO_PHAT_SINH = fields.Float(string='Nợ', help='Nợ phát sinh',digits= decimal_precision.get_precision('VND'))
    CO_PHAT_SINH = fields.Float(string='Có', help='Có phát sinh',digits= decimal_precision.get_precision('VND'))
    NO_SO_DU_CUOI_KY = fields.Float(string='Nợ', help='Nợ số dư cuối kỳ',digits= decimal_precision.get_precision('VND'))
    CO_SO_DU_CUOI_KY = fields.Float(string='Có', help='Có số dư cuối kỳ',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Có', oldname='NAME')

    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    SO_HOP_DONG  = fields.Char(string='Số hợp đồng', help='Số hợp đồng')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    SO_DON_HANG =  fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')


    NHACUNGCAP_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHA_CUNG_CAP = fields.Boolean('Tất cả nhà cung cấp', default=True)
    NHA_CUNG_CAP_MANY_IDS = fields.Many2many('res.partner','tong_hop_cong_no_res_partner',domain=[('LA_NHA_CUNG_CAP', '=', True)], string='Chọn NCC')
    MA_PC_NHOM_NCC = fields.Char()

    NHAN_VIEN_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','tong_hop_cong_no_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')

    HOP_DONG_IDS = fields.One2many ('purchase.ex.hop.dong.mua.hang')
    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('purchase.ex.hop.dong.mua.hang','tong_hop_mua_hang_hdmh', string='Chọn hợp đồng') 

    CONG_TRINH_IDS = fields.One2many ('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_mua_hang_danh_muc_cong_trinh', string='Chọn công trình') 

    DON_MUA_HANG_IDS = fields.One2many ('purchase.ex.don.mua.hang')
    CHON_TAT_CA_DON_MUA_HANG = fields.Boolean('Tất cả đơn mua hàng', default=True)
    DON_MUA_HANG_MANY_IDS = fields.Many2many('purchase.ex.don.mua.hang','tong_hop_mua_hang_dmh', string='Chọn đơn mua hàng') 

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):

        self.NHOM_NCC_ID = False
        self.CHON_TAT_CA_NHA_CUNG_CAP = True
        self.CHON_TAT_CA_NHAN_VIEN = True
        self.CHON_TAT_CA_HOP_DONG = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.CHON_TAT_CA_DON_MUA_HANG = True
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.CONG_TRINH_MANY_IDS = []
        self.NHAN_VIEN_MANY_IDS = []
        self.HOP_DONG_MANY_IDS = []
        self.DON_MUA_HANG_MANY_IDS = []

    # Nhà cung cấp
    @api.onchange('NHACUNGCAP_IDS')
    def update_NHA_CUNG_CAP_IDS(self):
        self.NHA_CUNG_CAP_MANY_IDS =self.NHACUNGCAP_IDS.ids

    @api.onchange('NHOM_NCC_ID')
    def update_NHOM_NCC_ID(self):
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.MA_PC_NHOM_NCC =self.NHOM_NCC_ID.MA_PHAN_CAP

    @api.onchange('NHA_CUNG_CAP_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.NHACUNGCAP_IDS = self.NHA_CUNG_CAP_MANY_IDS.ids

    # Nhân viên
    @api.onchange('NHAN_VIEN_IDS')
    def update_NHAN_VIEN_IDS(self):
        self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS.ids
        
    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        self.NHAN_VIEN_IDS = self.NHAN_VIEN_MANY_IDS.ids

    # Công trình
    @api.onchange('CONG_TRINH_IDS')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.CONG_TRINH_IDS.ids
        
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.CONG_TRINH_IDS = self.CONG_TRINH_MANY_IDS.ids
    
    # Hợp đồng
    @api.onchange('HOP_DONG_IDS')
    def update_HOP_DONG_IDS(self):
        self.HOP_DONG_MANY_IDS =self.HOP_DONG_IDS.ids
        
        
    @api.onchange('HOP_DONG_MANY_IDS')
    def _onchange_HOP_DONG_MANY_IDS(self):
        self.HOP_DONG_IDS = self.HOP_DONG_MANY_IDS.ids

    # Đơn mua hàng
    @api.onchange('DON_MUA_HANG_IDS')
    def update_DON_MUA_HANG_IDS(self):
        self.DON_MUA_HANG_MANY_IDS =self.DON_MUA_HANG_IDS.ids
        
        
    @api.onchange('DON_MUA_HANG_MANY_IDS')
    def _onchange_DON_MUA_HANG_MANY_IDS(self):
        self.DON_MUA_HANG_IDS = self.DON_MUA_HANG_MANY_IDS.ids

    # end

    @api.model
    def default_get(self,default_fields):
        result = super(BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA, self).default_get(default_fields)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if loai_tien:
            result['currency_id'] = loai_tien.id
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_DOI_TUONG', '=', 'True'),('DOI_TUONG_SELECTION', '=like', '0')],limit=1)
        if tai_khoan:
            result['TAI_KHOAN_ID'] = tai_khoan.id
       
        return result

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
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        if  TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN

        currency_id = params['currency_id'] if 'currency_id' in params.keys() and params['currency_id'] != 'False' else None
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHOM_NCC_ID = params['NHOM_NCC_ID'] if 'NHOM_NCC_ID' in params.keys() and params['NHOM_NCC_ID'] != 'False' else None
        
        CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY = 1 if 'CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY' in params.keys() and params['CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY'] != 'False' else 0
        
        MA_PC_NHOM_NCC = params.get('MA_PC_NHOM_NCC')
       
        if params.get('CHON_TAT_CA_NHAN_VIEN'):
            domain = [('LA_NHAN_VIEN','=', True)]
            NHAN_VIEN_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHAN_VIEN_IDS =  params.get('NHAN_VIEN_MANY_IDS')
        
        if params.get('CHON_TAT_CA_NHA_CUNG_CAP'):
            domain = [('LA_NHA_CUNG_CAP','=', True)]
            if MA_PC_NHOM_NCC:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_NCC +'%')]
            NHA_CUNG_CAP_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHA_CUNG_CAP_IDS = params.get('NHA_CUNG_CAP_MANY_IDS')
        
        if params.get('CHON_TAT_CA_CONG_TRINH'):
            domain = []
            CONG_TRINH_IDS = self.env['danh.muc.cong.trinh'].search(domain).ids
        else:
            CONG_TRINH_IDS = params.get('CONG_TRINH_MANY_IDS')

        if params.get('CHON_TAT_CA_HOP_DONG'):
            domain = []
            HOP_DONG_IDS = self.env['purchase.ex.hop.dong.mua.hang'].search(domain).ids
        else:
            HOP_DONG_IDS = params.get('HOP_DONG_MANY_IDS')
        
        if params.get('CHON_TAT_CA_DON_MUA_HANG'):
            domain = []
            DON_MUA_HANG_IDS = self.env['purchase.ex.don.mua.hang'].search(domain).ids
        else:
            DON_MUA_HANG_IDS = params.get('DON_MUA_HANG_MANY_IDS')

        params_sql = {
               'TU_NGAY':TU_NGAY_F, 
               'DEN_NGAY':DEN_NGAY_F, 
               'NHOM_NCC_ID' : NHOM_NCC_ID,
               'NHA_CUNG_CAPIDS' : NHA_CUNG_CAP_IDS or None,
               'NHAN_VIENIDS' : NHAN_VIEN_IDS or None,
               'CHI_NHANH_ID' : CHI_NHANH_ID,
               'HOP_DONGIDS' : HOP_DONG_IDS or None,
               'TAI_KHOAN_ID' : TAI_KHOAN_ID,
               'CONG_TRINHIDS' : CONG_TRINH_IDS or None,
               'DON_MUA_HANGIDS' : DON_MUA_HANG_IDS or None,
               'currency_id' : currency_id,
               'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
               'CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY' : CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY,
               'limit': limit,
               'offset': offset,
                
               }  

        # Thống kê theo không chọn
        if THONG_KE_THEO=='KHONG_CHON':
            return self._lay_bao_cao_thong_ke_theo_khong_chon(params_sql)
        # Thống kê theo nhân viên
        elif THONG_KE_THEO=='NHAN_VIEN':
            return self._lay_bao_cao_thong_ke_theo_nhan_vien(params_sql)
        # Thống kê theo công trình
        elif THONG_KE_THEO=='CONG_TRINH':
            return self._lay_bao_cao_thong_ke_theo_cong_trinh(params_sql)
        # Thống kê theo hợp đồng
        elif THONG_KE_THEO=='HOP_DONG_MUA':
            return self._lay_bao_cao_thong_ke_theo_hop_dong(params_sql)
        # Thống kê theo đơn đặt hàng
        elif THONG_KE_THEO=='DON_MUA_HANG':
            return self._lay_bao_cao_thong_ke_theo_don_mua_hang(params_sql)
        
    def _lay_bao_cao_thong_ke_theo_khong_chon(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                                      DATE := %(TU_NGAY)s;

   

    den_ngay                                     DATE := %(DEN_NGAY)s;

   

    bao_gom_du_lieu_chi_nhanh_phu_thuoc          INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    

    chi_nhanh_id                                 INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                                 VARCHAR(127) := %(TAI_KHOAN_ID)s;


    

    loai_tien_id                                 INTEGER := %(currency_id)s;

   

    chi_lay_ncc_co_so_du_hoac_phat_sinh_trong_ky INTEGER := %(CHI_LAY_NHA_CUNG_CAP_CO_SO_DU_VA_PHAT_SINH_TRONG_KY)s;

   

   

    StartDateOfPeriod                            DATE := to_date(CONCAT(DATE_PART('year', tu_ngay :: DATE), '-01-01'),
                                                                 'YYYYMMDD');


    rec                                          RECORD;


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
    ;

    CREATE TEMP TABLE DS_NHA_CUNG_CAP
        AS
            SELECT
                AO.id
                , AO."MA_NHA_CUNG_CAP"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI"
                , AO."MA_SO_THUE"
                , AO."LIST_MA_NHOM_KH_NCC"
                , AO."LIST_TEN_NHOM_KH_NCC"
                , AO."SO_NO_TOI_DA"


            FROM res_partner AS AO

            WHERE  AO."LA_NHA_CUNG_CAP" = '1'  AND ( (%(NHA_CUNG_CAPIDS)s) IS NULL OR  (id = any (%(NHA_CUNG_CAPIDS)s)))





    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" = so_tai_khoan
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '0'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;
    END IF
    ;



    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS
            SELECT
                ROW_NUMBER()
                OVER (
                    ORDER BY "MA_NHA_CUNG_CAP" )   AS RowNum
                , "DOI_TUONG_ID"
                , "MA_NHA_CUNG_CAP"
                , -- Mã NCC
                "HO_VA_TEN"
                , -- Tên NCC
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản

                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY")
                         - SUM("GHI_CO_NGUYEN_TE_DAU_KY")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                     - "GHI_CO_NGUYEN_TE_DAU_KY")) > 0
                     THEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                               - "GHI_CO_NGUYEN_TE_DAU_KY"))
                      ELSE 0
                      END
                 END)                           AS "GHI_NO_NGUYEN_TE_DAU_KY"
                , -- Dư nợ Đầu kỳ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN (SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"))
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_NO_DAU_KY"
                                     - "GHI_CO_DAU_KY")) > 0
                     THEN SUM("GHI_NO_DAU_KY"
                              - "GHI_CO_DAU_KY")
                      ELSE 0
                      END
                 END)                           AS "GHI_NO_DAU_KY"
                , -- Dư nợ Đầu kỳ quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                              - "GHI_NO_NGUYEN_TE_DAU_KY"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                     - "GHI_NO_NGUYEN_TE_DAU_KY")) > 0
                     THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                               - "GHI_NO_NGUYEN_TE_DAU_KY"))
                      ELSE 0
                      END
                 END)                           AS "GHI_CO_NGUYEN_TE_DAU_KY"
                , -- Dư có đầu kỳ
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
                                     - "GHI_NO_DAU_KY")) > 0
                     THEN (SUM("GHI_CO_DAU_KY"
                               - "GHI_NO_DAU_KY"))
                      ELSE 0
                      END
                 END)                           AS "GHI_CO_DAU_KY"
                , -- Dư có đầu kỳ quy đổi
                SUM("GHI_NO_NGUYEN_TE")         AS "GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                SUM("GHI_NO")                   AS "GHI_NO"
                , -- Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE")         AS "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                SUM("GHI_CO")                   AS "GHI_CO"
                , -- Phát sinh có quy đổi
                SUM("GHI_NO_NGUYEN_TE_CUOI_KY") AS "GHI_NO_NGUYEN_TE_CUOI_KY"
                , -- Lũy kế Phát sinh nợ
                SUM("GHI_NO_CUOI_KY")           AS "GHI_NO_CUOI_KY"
                , -- Lũy kế Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE_CUOI_KY") AS "GHI_CO_NGUYEN_TE_CUOI_KY"
                , -- Lũy kế Phát sinh có
                SUM("GHI_CO_CUOI_KY")           AS "GHI_CO_CUOI_KY"
                , -- Lũy kế Phát sinh có quy đổi
                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY"
                             + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                    - "GHI_NO_NGUYEN_TE_DAU_KY"
                                    + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") > 0
                     THEN 0
                      ELSE SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                               - "GHI_CO_NGUYEN_TE_DAU_KY"
                               + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                      END
                 END)                           AS "DU_NO_NGUYEN_TE_CUOI_KY"
                , -- Dư nợ cuối kỳ
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY" - "GHI_NO_NGUYEN_TE_DAU_KY"
                             + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                     - "GHI_NO_NGUYEN_TE_DAU_KY"
                                     + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")) > 0
                     THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                              - "GHI_NO_NGUYEN_TE_DAU_KY"
                              + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                      ELSE 0
                      END
                 END)                           AS "DU_CO_NGUYEN_TE_CUOI_KY"
                , -- Dư có cuối kỳ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"
                             + "GHI_NO" - "GHI_CO")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN SUM("GHI_CO_DAU_KY"
                                    - "GHI_NO_DAU_KY" + "GHI_CO"
                                    - "GHI_NO") > 0
                     THEN 0
                      ELSE SUM("GHI_NO_DAU_KY"
                               - "GHI_CO_DAU_KY" + "GHI_NO"
                               - "GHI_CO")
                      END
                 END)                           AS "DU_NO_CUOI_KY"
                , -- Dư nợ cuối kỳ quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"
                             + "GHI_CO" - "GHI_NO")
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
                                     - "GHI_NO_DAU_KY"
                                     + "GHI_CO" - "GHI_NO")) > 0
                     THEN SUM("GHI_CO_DAU_KY"
                              - "GHI_NO_DAU_KY" + "GHI_CO"
                              - "GHI_NO")
                      ELSE 0
                      END
                 END)                           AS "DU_CO_CUOI_KY" -- Dư có cuối kỳ quy đổi

            FROM (SELECT
                      AOL."DOI_TUONG_ID"
                      , LAOI."MA_NHA_CUNG_CAP"
                      , -- Mã NCC
                      LAOI."HO_VA_TEN"
                      , -- Tên NCC lấy trên danh mục

                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0
                        END        AS "GHI_NO_NGUYEN_TE_DAU_KY"
                      , -- Dư nợ Đầu kỳ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_NO"
                        ELSE 0
                        END        AS "GHI_NO_DAU_KY"
                      , -- Dư nợ Đầu kỳ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0
                        END        AS "GHI_CO_NGUYEN_TE_DAU_KY"
                      , -- Dư có đầu kỳ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_CO"
                        ELSE 0
                        END        AS "GHI_CO_DAU_KY"
                      , -- Dư có đầu kỳ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO_NGUYEN_TE"
                        END        AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO"
                        END        AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO_NGUYEN_TE"
                        END        AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO"
                        END        AS "GHI_CO"
                      , CASE WHEN "NGAY_HACH_TOAN" BETWEEN StartDateOfPeriod AND den_ngay
                    THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0 END AS "GHI_NO_NGUYEN_TE_CUOI_KY"
                      , CASE WHEN "NGAY_HACH_TOAN" BETWEEN StartDateOfPeriod AND den_ngay
                    THEN AOL."GHI_NO"
                        ELSE 0 END AS "GHI_NO_CUOI_KY"
                      , CASE WHEN "NGAY_HACH_TOAN" BETWEEN StartDateOfPeriod AND den_ngay
                    THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0 END AS "GHI_CO_NGUYEN_TE_CUOI_KY"
                      , CASE WHEN "NGAY_HACH_TOAN" BETWEEN StartDateOfPeriod AND den_ngay
                    THEN AOL."GHI_CO"
                        ELSE 0 END AS "GHI_CO_CUOI_KY"

                  FROM so_cong_no_chi_tiet AS AOL

                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN DS_NHA_CUNG_CAP AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."id"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT
                  WHERE AOL."NGAY_HACH_TOAN" <= den_ngay

                        AND (loai_tien_id IS NULL
                             OR AOL."currency_id" = loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '0'

                 ) AS RSNS
            GROUP BY RSNS."DOI_TUONG_ID",
                RSNS."MA_NHA_CUNG_CAP", -- Mã NCC
                RSNS."HO_VA_TEN", -- Tên NCC

                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT" -- Tính chất tài khoản

            HAVING
                SUM("GHI_NO_NGUYEN_TE") <> 0
                OR SUM("GHI_NO") <> 0
                OR SUM("GHI_CO_NGUYEN_TE") <> 0
                OR SUM("GHI_CO") <> 0
                OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0
                OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0
                OR (chi_lay_ncc_co_so_du_hoac_phat_sinh_trong_ky = 0 AND
                    (SUM("GHI_NO_NGUYEN_TE_CUOI_KY") <> 0
                     OR SUM("GHI_NO_CUOI_KY") <> 0
                     OR SUM("GHI_CO_NGUYEN_TE_CUOI_KY") <> 0
                     OR SUM("GHI_CO_CUOI_KY") <> 0))
            ORDER BY RSNS."MA_NHA_CUNG_CAP"
    ;


END $$
;

SELECT


    "MA_NHA_CUNG_CAP"  AS "MA_NHA_CUNG_CAP",
    "HO_VA_TEN" AS "TEN_NHA_CUNG_CAP",
    "SO_TAI_KHOAN"   AS "TK_CO_ID" ,
    "GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO"         AS "NO_PHAT_SINH",
    "GHI_CO" AS "CO_PHAT_SINH",
    "DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"

FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s;

        """
        return self.execute(query,params_sql)

    def _lay_bao_cao_thong_ke_theo_nhan_vien(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

    

    den_ngay                            DATE := %(DEN_NGAY)s;

   

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

   

    loai_tien_id                        INTEGER := %(currency_id)s;

   


    




    rec                                 RECORD;


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
    ;

    CREATE TEMP TABLE DS_NHA_CUNG_CAP
        AS
            SELECT
                AO.id AS "NHA_CUNG_CAP_ID"
                , AO."LIST_MA_NHOM_KH_NCC"
            FROM res_partner AS AO
            WHERE (id = any (%(NHA_CUNG_CAPIDS)s))
    ;

    DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT AU.id AS "NHAN_VIEN_ID"


            FROM res_partner AS AU

            WHERE (id = any (%(NHAN_VIENIDS)s))

    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" = so_tai_khoan
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '0'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;
    END IF
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS
            SELECT
                ROW_NUMBER()
                OVER (
                    ORDER BY "MA_NHAN_VIEN", "MA_DOI_TUONG" ) AS RowNum
                , "NHAN_VIEN_ID"
                , "MA_NHAN_VIEN"
                , -- Mã NV
                "TEN_NHAN_VIEN"

                , "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , -- Mã NCC
                "TEN_DOI_TUONG"
                , -- Tên NCC
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản

                ( CASE WHEN "TINH_CHAT" = '0'
                       THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY")
                            - SUM("GHI_CO_NGUYEN_TE_DAU_KY")
                       WHEN "TINH_CHAT" = '1' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                            - "GHI_CO_NGUYEN_TE_DAU_KY") ) > 0
                                 THEN ( SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                            - "GHI_CO_NGUYEN_TE_DAU_KY") )
                                 ELSE 0
                            END
                  END ) AS "GHI_NO_NGUYEN_TE_DAU_KY" ,	-- Dư nợ Đầu kỳ
                ( CASE WHEN "TINH_CHAT" = '0'
                       THEN ( SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") )
                       WHEN "TINH_CHAT" = '1' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_NO_DAU_KY"
                                            - "GHI_CO_DAU_KY") ) > 0
                                 THEN SUM("GHI_NO_DAU_KY"
                                          - "GHI_CO_DAU_KY")
                                 ELSE 0
                            END
                  END ) AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
                ( CASE WHEN "TINH_CHAT" = '1'
                       THEN ( SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                  - "GHI_NO_NGUYEN_TE_DAU_KY") )
                       WHEN "TINH_CHAT" = '0' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                            - "GHI_NO_NGUYEN_TE_DAU_KY") ) > 0
                                 THEN ( SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                            - "GHI_NO_NGUYEN_TE_DAU_KY") )
                                 ELSE 0
                            END
                  END ) AS "GHI_CO_NGUYEN_TE_DAU_KY" , -- Dư có đầu kỳ
                ( CASE WHEN "TINH_CHAT" = '1'
                       THEN ( SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY") )
                       WHEN "TINH_CHAT" = '0' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_CO_DAU_KY"
                                            - "GHI_NO_DAU_KY") ) > 0
                                 THEN ( SUM("GHI_CO_DAU_KY"
                                            - "GHI_NO_DAU_KY") )
                                 ELSE 0
                            END
                  END ) AS "GHI_CO_DAU_KY" , -- Dư có đầu kỳ quy đổi
                SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE" ,	-- Phát sinh nợ
                SUM("GHI_NO") AS "GHI_NO" , -- Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE" , -- Phát sinh có
                SUM("GHI_CO") AS "GHI_CO" , -- Phát sinh có quy đổi

                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
                ( CASE WHEN "TINH_CHAT" = '0'
                       THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY"
                                + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                       WHEN "TINH_CHAT" = '1' THEN 0
                       ELSE CASE WHEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                            - "GHI_NO_NGUYEN_TE_DAU_KY"
                                            + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") > 0
                                 THEN 0
                                 ELSE SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                          - "GHI_CO_NGUYEN_TE_DAU_KY"
                                          + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                            END
                  END ) AS "DU_NO_NGUYEN_TE_CUOI_KY" ,	-- Dư nợ cuối kỳ
                ( CASE WHEN "TINH_CHAT" = '1'
                       THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY" - "GHI_NO_NGUYEN_TE_DAU_KY"
                                + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                       WHEN "TINH_CHAT" = '0' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                            - "GHI_NO_NGUYEN_TE_DAU_KY"
                                            + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") ) > 0
                                 THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                          - "GHI_NO_NGUYEN_TE_DAU_KY"
                                          + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                                 ELSE 0
                            END
                  END ) AS "DU_CO_NGUYEN_TE_CUOI_KY" ,	-- Dư có cuối kỳ
                ( CASE WHEN "TINH_CHAT" = '0'
                       THEN SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"
                                + "GHI_NO" - "GHI_CO")
                       WHEN "TINH_CHAT" = '1' THEN 0
                       ELSE CASE WHEN SUM("GHI_CO_DAU_KY"
                                            - "GHI_NO_DAU_KY"
                                            + "GHI_CO" - "GHI_NO") > 0
                                 THEN 0
                                 ELSE SUM("GHI_NO_DAU_KY"
                                          - "GHI_CO_DAU_KY"
                                          + "GHI_NO" - "GHI_CO")
                            END
                  END ) AS "DU_NO_CUOI_KY" ,	-- Dư nợ cuối kỳ quy đổi
                ( CASE WHEN "TINH_CHAT" = '1'
                       THEN SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"
                                + "GHI_CO" - "GHI_NO")
                       WHEN "TINH_CHAT" = '0' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_CO_DAU_KY"
                                            - "GHI_NO_DAU_KY"
                                            + "GHI_CO" - "GHI_NO") ) > 0
                                 THEN SUM("GHI_CO_DAU_KY"
                                          - "GHI_NO_DAU_KY" + "GHI_CO"
                                          - "GHI_NO")
                                 ELSE 0
                            END
                  END ) AS "DU_CO_CUOI_KY" 	-- Dư có cuối kỳ quy đổi

            FROM (SELECT


                        AOL."NHAN_VIEN_ID",
                        AOL."MA_NHAN_VIEN" , -- Mã NV
                        AOL."TEN_NHAN_VIEN" , -- Tên NV
                        AOL."DOI_TUONG_ID" ,
                        AOL."MA_DOI_TUONG" ,   -- Mã NCC
                        AOL."TEN_DOI_TUONG" ,

                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0
                        END        AS "GHI_NO_NGUYEN_TE_DAU_KY"
                      , -- Dư nợ Đầu kỳ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_NO"
                        ELSE 0
                        END        AS "GHI_NO_DAU_KY"
                      , -- Dư nợ Đầu kỳ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0
                        END        AS "GHI_CO_NGUYEN_TE_DAU_KY"
                      , -- Dư có đầu kỳ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN AOL."GHI_CO"
                        ELSE 0
                        END        AS "GHI_CO_DAU_KY"
                      , -- Dư có đầu kỳ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO_NGUYEN_TE"
                        END        AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO"
                        END        AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO_NGUYEN_TE"
                        END        AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO"
                        END        AS "GHI_CO"


                  FROM so_cong_no_chi_tiet AS AOL

                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN DS_NHAN_VIEN LEID ON AOL."NHAN_VIEN_ID" = LEID."NHAN_VIEN_ID"
                      INNER JOIN DS_NHA_CUNG_CAP AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."NHA_CUNG_CAP_ID"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT
                  WHERE AOL."NGAY_HACH_TOAN" <= den_ngay

                        AND (loai_tien_id IS NULL
                             OR AOL."currency_id" = loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '0'

                 ) AS RSNS
            GROUP BY
                RSNS."NHAN_VIEN_ID",
				RSNS."MA_NHAN_VIEN" , -- Mã NV
                RSNS."TEN_NHAN_VIEN" , -- Tên NV
                RSNS."DOI_TUONG_ID" ,
                RSNS."MA_DOI_TUONG" ,   -- Mã NCC
                RSNS."TEN_DOI_TUONG" ,

                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT" -- Tính chất tài khoản

            HAVING
                SUM("GHI_NO_NGUYEN_TE") <>0
                OR SUM("GHI_NO") <>0
                OR SUM("GHI_CO_NGUYEN_TE") <>0
                OR SUM("GHI_CO") <>0
                OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY")<>0
                OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY")<>0

        ORDER BY RSNS."MA_NHAN_VIEN" ,
                RSNS."MA_DOI_TUONG"
    ;


END $$
;

SELECT


    "TEN_NHAN_VIEN" AS "TEN_NHAN_VIEN",
    "MA_DOI_TUONG"  AS "MA_NHA_CUNG_CAP",
    "TEN_DOI_TUONG" AS "TEN_NHA_CUNG_CAP",
    "SO_TAI_KHOAN"   AS "TK_CO_ID" ,
    "GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO"         AS "NO_PHAT_SINH",
    "GHI_CO" AS "CO_PHAT_SINH",
    "DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"




FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s;


        """
        return self.execute(query,params_sql)

        
    def _lay_bao_cao_thong_ke_theo_cong_trinh(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

    

    den_ngay                            DATE := %(DEN_NGAY)s;

   

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;


    

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

   

    loai_tien_id                        INTEGER := %(currency_id)s;

   



    rec                                 RECORD;


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
    ;

    CREATE TEMP TABLE DS_NHA_CUNG_CAP
        AS
            SELECT
                  AO.id          AS "NHA_CUNG_CAP_ID"
                , AO."HO_VA_TEN" AS "TEN_NHA_CUNG_CAP"
                , AO."DIA_CHI"
                , AO."MA_SO_THUE"
                , AO."LIST_MA_NHOM_KH_NCC"
                , AO."LIST_TEN_NHOM_KH_NCC"

            FROM res_partner AS AO
            WHERE (id = any (%(NHA_CUNG_CAPIDS)s))
    ;

    DROP TABLE IF EXISTS TMP_CONG_TRINH
    ;

    CREATE TEMP TABLE TMP_CONG_TRINH
        AS
            SELECT DISTINCT
                PW."id" AS "CONG_TRINH_ID"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"
                , PW."LOAI_CONG_TRINH"
            FROM danh_muc_cong_trinh AS PW

            WHERE (id = any (%(CONG_TRINHIDS)s))

    ;

    DROP TABLE IF EXISTS DS_CONG_TRINH
    ;

    CREATE TEMP TABLE DS_CONG_TRINH
        AS
            SELECT DISTINCT
                PW."id" AS "CONG_TRINH_ID"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"

            FROM TMP_CONG_TRINH SPW
                INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE SPW."MA_PHAN_CAP"
                                                                           || '%%'

    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" = so_tai_khoan
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '0'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;
    END IF
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS
            SELECT
                ROW_NUMBER()
                OVER (
                    ORDER BY "MA_CONG_TRINH", "MA_DOI_TUONG" ) AS RowNum
                , "CONG_TRINH_ID"
                , "MA_CONG_TRINH"
                , -- Mã NV
                "TEN_CONG_TRINH"

                , "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , -- Mã NCC
                "TEN_NHA_CUNG_CAP"
                , -- Tên NCC
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản

                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY")
                         - SUM("GHI_CO_NGUYEN_TE_DAU_KY")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                     - "GHI_CO_NGUYEN_TE_DAU_KY")) > 0
                     THEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                               - "GHI_CO_NGUYEN_TE_DAU_KY"))
                      ELSE 0
                      END
                 END)                                         AS "GHI_NO_NGUYEN_TE_DAU_KY"
                , -- Dư nợ Đầu kỳ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN (SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"))
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_NO_DAU_KY"
                                     - "GHI_CO_DAU_KY")) > 0
                     THEN SUM("GHI_NO_DAU_KY"
                              - "GHI_CO_DAU_KY")
                      ELSE 0
                      END
                 END)                                         AS "GHI_NO_DAU_KY"
                , -- Dư nợ Đầu kỳ quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                              - "GHI_NO_NGUYEN_TE_DAU_KY"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                     - "GHI_NO_NGUYEN_TE_DAU_KY")) > 0
                     THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                               - "GHI_NO_NGUYEN_TE_DAU_KY"))
                      ELSE 0
                      END
                 END)                                         AS "GHI_CO_NGUYEN_TE_DAU_KY"
                , -- Dư có đầu kỳ
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
                                     - "GHI_NO_DAU_KY")) > 0
                     THEN (SUM("GHI_CO_DAU_KY"
                               - "GHI_NO_DAU_KY"))
                      ELSE 0
                      END
                 END)                                         AS "GHI_CO_DAU_KY"
                , -- Dư có đầu kỳ quy đổi
                SUM("GHI_NO_NGUYEN_TE")                       AS "GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                SUM("GHI_NO")                                 AS "GHI_NO"
                , -- Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE")                       AS "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                SUM("GHI_CO")                                 AS "GHI_CO"
                , -- Phát sinh có quy đổi

                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY"
                             + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                    - "GHI_NO_NGUYEN_TE_DAU_KY"
                                    + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") > 0
                     THEN 0
                      ELSE SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                               - "GHI_CO_NGUYEN_TE_DAU_KY"
                               + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                      END
                 END)                                         AS "DU_NO_NGUYEN_TE_CUOI_KY"
                , -- Dư nợ cuối kỳ
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY" - "GHI_NO_NGUYEN_TE_DAU_KY"
                             + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                     - "GHI_NO_NGUYEN_TE_DAU_KY"
                                     + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")) > 0
                     THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                              - "GHI_NO_NGUYEN_TE_DAU_KY"
                              + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                      ELSE 0
                      END
                 END)                                         AS "DU_CO_NGUYEN_TE_CUOI_KY"
                , -- Dư có cuối kỳ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"
                             + "GHI_NO" - "GHI_CO")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN SUM("GHI_CO_DAU_KY"
                                    - "GHI_NO_DAU_KY"
                                    + "GHI_CO" - "GHI_NO") > 0
                     THEN 0
                      ELSE SUM("GHI_NO_DAU_KY"
                               - "GHI_CO_DAU_KY"
                               + "GHI_NO" - "GHI_CO")
                      END
                 END)                                         AS "DU_NO_CUOI_KY"
                , -- Dư nợ cuối kỳ quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"
                             + "GHI_CO" - "GHI_NO")
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
                                     - "GHI_NO_DAU_KY"
                                     + "GHI_CO" - "GHI_NO")) > 0
                     THEN SUM("GHI_CO_DAU_KY"
                              - "GHI_NO_DAU_KY" + "GHI_CO"
                              - "GHI_NO")
                      ELSE 0
                      END
                 END)                                         AS "DU_CO_CUOI_KY" -- Dư có cuối kỳ quy đổi

            FROM (SELECT


                      PW."CONG_TRINH_ID"
                      , PW."MA_CONG_TRINH"
                      , -- Mã công trình
                      PW."TEN_CONG_TRINH"
                      , -- Tên công trình

                      AOL."DOI_TUONG_ID"
                      , AOL."MA_DOI_TUONG"
                      , -- Mã NCC
                      LAOI."TEN_NHA_CUNG_CAP"

                      , TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN AOL."GHI_NO_NGUYEN_TE"
                      ELSE 0
                      END AS "GHI_NO_NGUYEN_TE_DAU_KY"
                      , -- Dư nợ Đầu kỳ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN AOL."GHI_NO"
                      ELSE 0
                      END AS "GHI_NO_DAU_KY"
                      , -- Dư nợ Đầu kỳ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN AOL."GHI_CO_NGUYEN_TE"
                      ELSE 0
                      END AS "GHI_CO_NGUYEN_TE_DAU_KY"
                      , -- Dư có đầu kỳ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN AOL."GHI_CO"
                      ELSE 0
                      END AS "GHI_CO_DAU_KY"
                      , -- Dư có đầu kỳ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN 0
                      ELSE AOL."GHI_NO_NGUYEN_TE"
                      END AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN 0
                      ELSE AOL."GHI_NO"
                      END AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN 0
                      ELSE AOL."GHI_CO_NGUYEN_TE"
                      END AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                      CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                          THEN 0
                      ELSE AOL."GHI_CO"
                      END AS "GHI_CO"


                  FROM so_cong_no_chi_tiet AS AOL

                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"

                       INNER JOIN DS_CONG_TRINH LPID ON AOL."CONG_TRINH_ID" = LPID."CONG_TRINH_ID"
                        INNER JOIN TMP_CONG_TRINH PW ON LPID."MA_PHAN_CAP" LIKE PW."MA_PHAN_CAP"
                                                              || '%%'
                        LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC.id

                      INNER JOIN DS_NHA_CUNG_CAP AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."NHA_CUNG_CAP_ID"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT
                  WHERE AOL."NGAY_HACH_TOAN" <= den_ngay

                        AND (loai_tien_id IS NULL
                             OR AOL."currency_id" = loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '0'

                 ) AS RSNS
            GROUP BY
                RSNS."CONG_TRINH_ID",
                RSNS."MA_CONG_TRINH", -- Mã NV
                RSNS."TEN_CONG_TRINH", -- Tên NV
                RSNS."DOI_TUONG_ID",
                RSNS."MA_DOI_TUONG", -- Mã NCC
                RSNS."TEN_NHA_CUNG_CAP",

                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT" -- Tính chất tài khoản

             HAVING  SUM("GHI_NO_NGUYEN_TE") <> 0
                OR SUM("GHI_NO") <> 0
                OR SUM("GHI_CO_NGUYEN_TE") <> 0
                OR SUM("GHI_CO") <> 0
                OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0
                OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0
        ORDER BY RSNS."MA_CONG_TRINH" , -- Mã công trình
                RSNS."MA_DOI_TUONG" -- Mã NCC
    ;


END $$
;

SELECT

    "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
    "MA_DOI_TUONG"  AS "MA_NHA_CUNG_CAP",
    "TEN_NHA_CUNG_CAP" AS "TEN_NHA_CUNG_CAP",
    "SO_TAI_KHOAN"   AS "TK_CO_ID" ,
    "GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO"         AS "NO_PHAT_SINH",
    "GHI_CO" AS "CO_PHAT_SINH",
    "DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s;


        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_hop_dong(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

    

    den_ngay                            DATE := %(DEN_NGAY)s;

   

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

   

    loai_tien_id                        INTEGER := %(currency_id)s;

   


    


    rec                                 RECORD;


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
    ;

    CREATE TEMP TABLE DS_NHA_CUNG_CAP
        AS
            SELECT
                AO.id AS "NHA_CUNG_CAP_ID"
                , AO."LIST_MA_NHOM_KH_NCC"
            FROM res_partner AS AO
            WHERE (id = any (%(NHA_CUNG_CAPIDS)s))
    ;

    DROP TABLE IF EXISTS DS_HOP_DONG
    ;

    CREATE TEMP TABLE DS_HOP_DONG
        AS
            SELECT
                PUC."id" AS "HOP_DONG_MUA_ID"
                , OU."TEN_DON_VI"
            FROM purchase_ex_hop_dong_mua_hang PUC
                INNER JOIN danh_muc_to_chuc OU ON OU."id" = PUC."CHI_NHANH_ID"
            WHERE (PUC."id" = any (%(HOP_DONGIDS)s))
    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
			;

			IF so_tai_khoan IS NOT NULL
			THEN
				CREATE TEMP TABLE TMP_TAI_KHOAN
					AS
						SELECT
							A."SO_TAI_KHOAN"
							, A."TEN_TAI_KHOAN"
							, A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
							, A."TINH_CHAT"
						FROM danh_muc_he_thong_tai_khoan AS A
						WHERE "SO_TAI_KHOAN" = so_tai_khoan
						ORDER BY A."SO_TAI_KHOAN",
							A."TEN_TAI_KHOAN"
				;

			ELSE
				CREATE TEMP TABLE TMP_TAI_KHOAN
					AS
						SELECT
							A."SO_TAI_KHOAN"
							, A."TEN_TAI_KHOAN"
							, A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
							, A."TINH_CHAT"
						FROM danh_muc_he_thong_tai_khoan AS A
						WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
							  AND "DOI_TUONG_SELECTION" = '0'
							  AND "LA_TK_TONG_HOP" = '0'
						ORDER BY A."SO_TAI_KHOAN",
							A."TEN_TAI_KHOAN"
				;
			END IF
			;


			DROP TABLE IF EXISTS TMP_KET_QUA
			;

			CREATE TEMP TABLE TMP_KET_QUA
				AS
					SELECT
						ROW_NUMBER()
						OVER (
							ORDER BY "SO_HOP_DONG_MUA", "MA_DOI_TUONG" ) AS RowNum
						, "HOP_DONG_MUA_ID"
						, "SO_HOP_DONG_MUA"

						, "DOI_TUONG_ID"
						, "MA_DOI_TUONG"
						, -- Mã NCC
						"TEN_DOI_TUONG"
						, -- Tên NCC
						"SO_TAI_KHOAN"
						, -- Số tài khoản
						"TINH_CHAT"
						, -- Tính chất tài khoản

						(CASE WHEN "TINH_CHAT" = '0'
							THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY")
								 - SUM("GHI_CO_NGUYEN_TE_DAU_KY")
						 WHEN "TINH_CHAT" = '1'
							 THEN 0
						 ELSE CASE WHEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
											 - "GHI_CO_NGUYEN_TE_DAU_KY")) > 0
							 THEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
									   - "GHI_CO_NGUYEN_TE_DAU_KY"))
							  ELSE 0
							  END
						 END)                                          AS "GHI_NO_NGUYEN_TE_DAU_KY"
						, -- Dư nợ Đầu kỳ
						(CASE WHEN "TINH_CHAT" = '0'
							THEN (SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"))
						 WHEN "TINH_CHAT" = '1'
							 THEN 0
						 ELSE CASE WHEN (SUM("GHI_NO_DAU_KY"
											 - "GHI_CO_DAU_KY")) > 0
							 THEN SUM("GHI_NO_DAU_KY"
									  - "GHI_CO_DAU_KY")
							  ELSE 0
							  END
						 END)                                          AS "GHI_NO_DAU_KY"
						, -- Dư nợ Đầu kỳ quy đổi
						(CASE WHEN "TINH_CHAT" = '1'
							THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
									  - "GHI_NO_NGUYEN_TE_DAU_KY"))
						 WHEN "TINH_CHAT" = '0'
							 THEN 0
						 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
											 - "GHI_NO_NGUYEN_TE_DAU_KY")) > 0
							 THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
									   - "GHI_NO_NGUYEN_TE_DAU_KY"))
							  ELSE 0
							  END
						 END)                                          AS "GHI_CO_NGUYEN_TE_DAU_KY"
						, -- Dư có đầu kỳ
						(CASE WHEN "TINH_CHAT" = '1'
							THEN (SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"))
						 WHEN "TINH_CHAT" = '0'
							 THEN 0
						 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
											 - "GHI_NO_DAU_KY")) > 0
							 THEN (SUM("GHI_CO_DAU_KY"
									   - "GHI_NO_DAU_KY"))
							  ELSE 0
							  END
						 END)                                          AS "GHI_CO_DAU_KY"
						, -- Dư có đầu kỳ quy đổi
						SUM("GHI_NO_NGUYEN_TE")                        AS "GHI_NO_NGUYEN_TE"
						, -- Phát sinh nợ
						SUM("GHI_NO")                                  AS "GHI_NO"
						, -- Phát sinh nợ quy đổi
						SUM("GHI_CO_NGUYEN_TE")                        AS "GHI_CO_NGUYEN_TE"
						, -- Phát sinh có
						SUM("GHI_CO")                                  AS "GHI_CO"
						, -- Phát sinh có quy đổi

						/* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
						Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
						Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
						(CASE WHEN "TINH_CHAT" = '0'
							THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY"
									 + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
						 WHEN "TINH_CHAT" = '1'
							 THEN 0
						 ELSE CASE WHEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
											- "GHI_NO_NGUYEN_TE_DAU_KY"
											+ "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") > 0
							 THEN 0
							  ELSE SUM("GHI_NO_NGUYEN_TE_DAU_KY"
									   - "GHI_CO_NGUYEN_TE_DAU_KY"
									   + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
							  END
						 END)                                          AS "DU_NO_NGUYEN_TE_CUOI_KY"
						, -- Dư nợ cuối kỳ
						(CASE WHEN "TINH_CHAT" = '1'
							THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY" - "GHI_NO_NGUYEN_TE_DAU_KY"
									 + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
						 WHEN "TINH_CHAT" = '0'
							 THEN 0
						 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
											 - "GHI_NO_NGUYEN_TE_DAU_KY"
											 + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")) > 0
							 THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
									  - "GHI_NO_NGUYEN_TE_DAU_KY"
									  + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
							  ELSE 0
							  END
						 END)                                          AS "DU_CO_NGUYEN_TE_CUOI_KY"
						, -- Dư có cuối kỳ
						(CASE WHEN "TINH_CHAT" = '0'
							THEN SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"
									 + "GHI_NO" - "GHI_CO")
						 WHEN "TINH_CHAT" = '1'
							 THEN 0
						 ELSE CASE WHEN SUM("GHI_CO_DAU_KY"
											- "GHI_NO_DAU_KY"
											+ "GHI_CO" - "GHI_NO") > 0
							 THEN 0
							  ELSE SUM("GHI_NO_DAU_KY"
									   - "GHI_CO_DAU_KY"
									   + "GHI_NO" - "GHI_CO")
							  END
						 END)                                          AS "DU_NO_CUOI_KY"
						, -- Dư nợ cuối kỳ quy đổi
						(CASE WHEN "TINH_CHAT" = '1'
							THEN SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"
									 + "GHI_CO" - "GHI_NO")
						 WHEN "TINH_CHAT" = '0'
							 THEN 0
						 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
											 - "GHI_NO_DAU_KY"
											 + "GHI_CO" - "GHI_NO")) > 0
							 THEN SUM("GHI_CO_DAU_KY"
									  - "GHI_NO_DAU_KY" + "GHI_CO"
									  - "GHI_NO")
							  ELSE 0
							  END
						 END)                                          AS "DU_CO_CUOI_KY" -- Dư có cuối kỳ quy đổi

					FROM (SELECT


							  AOL."HOP_DONG_MUA_ID"
							  , AOL."SO_HOP_DONG_MUA"

							  ,AOL."DOI_TUONG_ID"
							  , AOL."MA_DOI_TUONG"
							  , -- Mã NCC
							  AOL."TEN_DOI_TUONG"

							  , TBAN."SO_TAI_KHOAN"
							  , -- TK công nợ
							  TBAN."TINH_CHAT"
							  , -- Tính chất tài khoản
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN AOL."GHI_NO_NGUYEN_TE"
								ELSE 0
								END AS "GHI_NO_NGUYEN_TE_DAU_KY"
							  , -- Dư nợ Đầu kỳ
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN AOL."GHI_NO"
								ELSE 0
								END AS "GHI_NO_DAU_KY"
							  , -- Dư nợ Đầu kỳ quy đổi
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN AOL."GHI_CO_NGUYEN_TE"
								ELSE 0
								END AS "GHI_CO_NGUYEN_TE_DAU_KY"
							  , -- Dư có đầu kỳ
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN AOL."GHI_CO"
								ELSE 0
								END AS "GHI_CO_DAU_KY"
							  , -- Dư có đầu kỳ quy đổi
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN 0
								ELSE AOL."GHI_NO_NGUYEN_TE"
								END AS "GHI_NO_NGUYEN_TE"
							  , -- Phát sinh nợ
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN 0
								ELSE AOL."GHI_NO"
								END AS "GHI_NO"
							  , -- Phát sinh nợ quy đổi
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN 0
								ELSE AOL."GHI_CO_NGUYEN_TE"
								END AS "GHI_CO_NGUYEN_TE"
							  , -- Phát sinh có
								CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
									THEN 0
								ELSE AOL."GHI_CO"
								END AS "GHI_CO"


						  FROM so_cong_no_chi_tiet AS AOL

							  INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
							  INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"

							  INNER JOIN DS_HOP_DONG LCID ON AOL."HOP_DONG_MUA_ID" = LCID."HOP_DONG_MUA_ID"

							  INNER JOIN DS_NHA_CUNG_CAP AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."NHA_CUNG_CAP_ID"
							  INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
							  LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT
						  WHERE AOL."NGAY_HACH_TOAN" <= den_ngay

								AND (loai_tien_id IS NULL
									 OR AOL."currency_id" = loai_tien_id
								)
								AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
								AND AN."DOI_TUONG_SELECTION" = '0'

						 ) AS RSNS
					GROUP BY
						RSNS."HOP_DONG_MUA_ID",
						RSNS."SO_HOP_DONG_MUA", -- Mã NV

						RSNS."DOI_TUONG_ID",
						RSNS."MA_DOI_TUONG", -- Mã NCC
						RSNS."TEN_DOI_TUONG",

						RSNS."SO_TAI_KHOAN", -- Số tài khoản
						RSNS."TINH_CHAT" -- Tính chất tài khoản

					  HAVING
						SUM("GHI_NO_NGUYEN_TE") <>0
						OR SUM("GHI_NO") <>0
						OR SUM("GHI_CO_NGUYEN_TE") <>0
						OR SUM("GHI_CO") <>0
						OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY")<>0
						OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY")<>0
			;


		END $$
		;

		SELECT

			"SO_HOP_DONG_MUA" AS "SO_HOP_DONG",
			"MA_DOI_TUONG"  AS "MA_NHA_CUNG_CAP",
			"TEN_DOI_TUONG" AS "TEN_NHA_CUNG_CAP",
			"SO_TAI_KHOAN"   AS "TK_CO_ID" ,
			"GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
			"GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
			"GHI_NO"         AS "NO_PHAT_SINH",
			"GHI_CO" AS "CO_PHAT_SINH",
			"DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
			"DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"

		FROM TMP_KET_QUA
		OFFSET %(offset)s
        LIMIT %(limit)s;


        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_don_mua_hang(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_PHAI_TRA
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

    

    den_ngay                            DATE := %(DEN_NGAY)s;

   

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

   

    loai_tien_id                        INTEGER := %(currency_id)s;

   


    NHA_CUNG_CAP_IDS                    INTEGER := -1;

    DON_MUA_HANG_IDS                    INTEGER := -1;


    rec                                 RECORD;


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
    ;

    CREATE TEMP TABLE DS_NHA_CUNG_CAP
        AS
            SELECT
                AO.id AS "NHA_CUNG_CAP_ID"
                , AO."LIST_MA_NHOM_KH_NCC"
                , AO."LIST_TEN_NHOM_KH_NCC"
            FROM res_partner AS AO
            WHERE (id = any (%(NHA_CUNG_CAPIDS)s))
    ;

    DROP TABLE IF EXISTS DS_DON_MUA_HANG
    ;

    CREATE TEMP TABLE DS_DON_MUA_HANG
        AS
            SELECT
                  PUO."id" AS "DON_MUA_HANG_ID"
                , PUO."SO_DON_HANG"
                , PUO."NGAY_DON_HANG"
                , CASE PUO."TINH_TRANG"
                  WHEN '0'
                      THEN N'Chưa thực hiện'
                  WHEN '1'
                      THEN N'Đang thực hiện'
                  WHEN '2'
                      THEN N'Hoàn thành'
                  WHEN '3'
                      THEN N'Đã hủy bỏ'
                  END      AS "TINH_TRANG"
            FROM purchase_ex_don_mua_hang PUO

            WHERE (PUO."id" = any (%(DON_MUA_HANGIDS)s))
    ;


    		DROP TABLE IF EXISTS TMP_TAI_KHOAN
		;

		IF so_tai_khoan IS NOT NULL
		THEN
			CREATE TEMP TABLE TMP_TAI_KHOAN
				AS
					SELECT
						A."SO_TAI_KHOAN"
						, A."TEN_TAI_KHOAN"
						, A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"

					FROM danh_muc_he_thong_tai_khoan AS A
					WHERE "SO_TAI_KHOAN" = so_tai_khoan
					ORDER BY A."SO_TAI_KHOAN",
						A."TEN_TAI_KHOAN"
			;

		ELSE
			CREATE TEMP TABLE TMP_TAI_KHOAN
				AS
					SELECT
						A."SO_TAI_KHOAN"
						, A."TEN_TAI_KHOAN"
						, A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
						, A."TINH_CHAT"
					FROM danh_muc_he_thong_tai_khoan AS A
					WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
						  AND "DOI_TUONG_SELECTION" = '0'
						  AND "LA_TK_TONG_HOP" = '0'
					ORDER BY A."SO_TAI_KHOAN",
						A."TEN_TAI_KHOAN"
			;
		END IF
		;


		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
			AS
				SELECT
					ROW_NUMBER()
					OVER (
						ORDER BY "NGAY_DON_HANG","SO_DON_HANG", "MA_DOI_TUONG","TEN_DOI_TUONG" ) AS RowNum
					, "DON_MUA_HANG_ID"
					, "SO_DON_HANG"
					 , "NGAY_DON_HANG"
					, "DOI_TUONG_ID"
					, "MA_DOI_TUONG"
					, -- Mã NCC
					"TEN_DOI_TUONG"
					, -- Tên NCC
					"SO_TAI_KHOAN"
					, -- Số tài khoản
					"TINH_CHAT"
					, -- Tính chất tài khoản

					(CASE WHEN "TINH_CHAT" = '0'
						THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY")
							 - SUM("GHI_CO_NGUYEN_TE_DAU_KY")
					 WHEN "TINH_CHAT" = '1'
						 THEN 0
					 ELSE CASE WHEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
										 - "GHI_CO_NGUYEN_TE_DAU_KY")) > 0
						 THEN (SUM("GHI_NO_NGUYEN_TE_DAU_KY"
								   - "GHI_CO_NGUYEN_TE_DAU_KY"))
						  ELSE 0
						  END
					 END)                                        AS "GHI_NO_NGUYEN_TE_DAU_KY"
					, -- Dư nợ Đầu kỳ
					(CASE WHEN "TINH_CHAT" = '0'
						THEN (SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"))
					 WHEN "TINH_CHAT" = '1'
						 THEN 0
					 ELSE CASE WHEN (SUM("GHI_NO_DAU_KY"
										 - "GHI_CO_DAU_KY")) > 0
						 THEN SUM("GHI_NO_DAU_KY"
								  - "GHI_CO_DAU_KY")
						  ELSE 0
						  END
					 END)                                        AS "GHI_NO_DAU_KY"
					, -- Dư nợ Đầu kỳ quy đổi
					(CASE WHEN "TINH_CHAT" = '1'
						THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
								  - "GHI_NO_NGUYEN_TE_DAU_KY"))
					 WHEN "TINH_CHAT" = '0'
						 THEN 0
					 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
										 - "GHI_NO_NGUYEN_TE_DAU_KY")) > 0
						 THEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
								   - "GHI_NO_NGUYEN_TE_DAU_KY"))
						  ELSE 0
						  END
					 END)                                        AS "GHI_CO_NGUYEN_TE_DAU_KY"
					, -- Dư có đầu kỳ
					(CASE WHEN "TINH_CHAT" = '1'
						THEN (SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"))
					 WHEN "TINH_CHAT" = '0'
						 THEN 0
					 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
										 - "GHI_NO_DAU_KY")) > 0
						 THEN (SUM("GHI_CO_DAU_KY"
								   - "GHI_NO_DAU_KY"))
						  ELSE 0
						  END
					 END)                                        AS "GHI_CO_DAU_KY"
					, -- Dư có đầu kỳ quy đổi
					SUM("GHI_NO_NGUYEN_TE")                      AS "GHI_NO_NGUYEN_TE"
					, -- Phát sinh nợ
					SUM("GHI_NO")                                AS "GHI_NO"
					, -- Phát sinh nợ quy đổi
					SUM("GHI_CO_NGUYEN_TE")                      AS "GHI_CO_NGUYEN_TE"
					, -- Phát sinh có
					SUM("GHI_CO")                                AS "GHI_CO"
					, -- Phát sinh có quy đổi

					/* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
					Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
					Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
					(CASE WHEN "TINH_CHAT" = '0'
						THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY"
								 + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
					 WHEN "TINH_CHAT" = '1'
						 THEN 0
					 ELSE CASE WHEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
										- "GHI_NO_NGUYEN_TE_DAU_KY"
										+ "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") > 0
						 THEN 0
						  ELSE SUM("GHI_NO_NGUYEN_TE_DAU_KY"
								   - "GHI_CO_NGUYEN_TE_DAU_KY"
								   + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
						  END
					 END)                                        AS "DU_NO_NGUYEN_TE_CUOI_KY"
					, -- Dư nợ cuối kỳ
					(CASE WHEN "TINH_CHAT" = '1'
						THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY" - "GHI_NO_NGUYEN_TE_DAU_KY"
								 + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
					 WHEN "TINH_CHAT" = '0'
						 THEN 0
					 ELSE CASE WHEN (SUM("GHI_CO_NGUYEN_TE_DAU_KY"
										 - "GHI_NO_NGUYEN_TE_DAU_KY"
										 + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")) > 0
						 THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
								  - "GHI_NO_NGUYEN_TE_DAU_KY"
								  + "GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
						  ELSE 0
						  END
					 END)                                        AS "DU_CO_NGUYEN_TE_CUOI_KY"
					, -- Dư có cuối kỳ
					(CASE WHEN "TINH_CHAT" = '0'
						THEN SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"
								 + "GHI_NO" - "GHI_CO")
					 WHEN "TINH_CHAT" = '1'
						 THEN 0
					 ELSE CASE WHEN SUM("GHI_CO_DAU_KY"
										- "GHI_NO_DAU_KY"
										+ "GHI_CO" - "GHI_NO") > 0
						 THEN 0
						  ELSE SUM("GHI_NO_DAU_KY"
								   - "GHI_CO_DAU_KY"
								   + "GHI_NO" - "GHI_CO")
						  END
					 END)                                        AS "DU_NO_CUOI_KY"
					, -- Dư nợ cuối kỳ quy đổi
					(CASE WHEN "TINH_CHAT" = '1'
						THEN SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"
								 + "GHI_CO" - "GHI_NO")
					 WHEN "TINH_CHAT" = '0'
						 THEN 0
					 ELSE CASE WHEN (SUM("GHI_CO_DAU_KY"
										 - "GHI_NO_DAU_KY"
										 + "GHI_CO" - "GHI_NO")) > 0
						 THEN SUM("GHI_CO_DAU_KY"
								  - "GHI_NO_DAU_KY" + "GHI_CO"
								  - "GHI_NO")
						  ELSE 0
						  END
					 END)                                        AS "DU_CO_CUOI_KY" -- Dư có cuối kỳ quy đổi

				FROM (SELECT


						  AOL."DON_MUA_HANG_ID"
						  , -- ID đơn mua hàng
						  LCID."SO_DON_HANG"
						  , -- Số đơn hàng
						  LCID."NGAY_DON_HANG"


						  , --Tình trạng đơn mua hàng
						  AOL."DOI_TUONG_ID"
						  , AOL."MA_DOI_TUONG"
						  , -- Mã NCC
						  AOL."TEN_DOI_TUONG"

						  ,TBAN."SO_TAI_KHOAN"
						  , -- TK công nợ
						  AN."TINH_CHAT"

						  , -- Tính chất tài khoản
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN AOL."GHI_NO_NGUYEN_TE"
						  ELSE 0
						  END                   AS "GHI_NO_NGUYEN_TE_DAU_KY"
						  , -- Dư nợ Đầu kỳ
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN AOL."GHI_NO"
						  ELSE 0
						  END                   AS "GHI_NO_DAU_KY"
						  , -- Dư nợ Đầu kỳ quy đổi
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN AOL."GHI_CO_NGUYEN_TE"
						  ELSE 0
						  END                   AS "GHI_CO_NGUYEN_TE_DAU_KY"
						  , -- Dư có đầu kỳ
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN AOL."GHI_CO"
						  ELSE 0
						  END                   AS "GHI_CO_DAU_KY"
						  , -- Dư có đầu kỳ quy đổi
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN 0
						  ELSE AOL."GHI_NO_NGUYEN_TE"
						  END                   AS "GHI_NO_NGUYEN_TE"
						  , -- Phát sinh nợ
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN 0
						  ELSE AOL."GHI_NO"
						  END                   AS "GHI_NO"
						  , -- Phát sinh nợ quy đổi
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN 0
						  ELSE AOL."GHI_CO_NGUYEN_TE"
						  END                   AS "GHI_CO_NGUYEN_TE"
						  , -- Phát sinh có
						  CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
							  THEN 0
						  ELSE AOL."GHI_CO"
						  END                   AS "GHI_CO"


					  FROM so_cong_no_chi_tiet AS AOL

						  INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
						  INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"

						  INNER JOIN DS_DON_MUA_HANG LCID ON AOL."DON_MUA_HANG_ID" = LCID."DON_MUA_HANG_ID"

						  INNER JOIN DS_NHA_CUNG_CAP AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."NHA_CUNG_CAP_ID"
						  INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"

					  WHERE AOL."NGAY_HACH_TOAN" <= den_ngay

							AND (loai_tien_id IS NULL
								 OR AOL."currency_id" = loai_tien_id
							)
							AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
							AND AN."DOI_TUONG_SELECTION" = '0'

					 ) AS RSNS
				GROUP BY
					RSNS."DON_MUA_HANG_ID",
					RSNS."SO_DON_HANG",
					 RSNS."NGAY_DON_HANG",

					RSNS."DOI_TUONG_ID",
					RSNS."MA_DOI_TUONG", -- Mã NCC
					RSNS."TEN_DOI_TUONG",

					RSNS."SO_TAI_KHOAN", -- Số tài khoản
					RSNS."TINH_CHAT" -- Tính chất tài khoản

				HAVING
					SUM("GHI_NO_NGUYEN_TE") <> 0
					OR SUM("GHI_NO") <> 0
					OR SUM("GHI_CO_NGUYEN_TE") <> 0
					OR SUM("GHI_CO") <> 0
					OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0
					OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0
		;


	END $$
	;

	SELECT

		"SO_DON_HANG" AS "SO_DON_HANG",
		"NGAY_DON_HANG"  AS "NGAY_DON_HANG",
		"TEN_DOI_TUONG" AS "TEN_NHA_CUNG_CAP",
		"SO_TAI_KHOAN"   AS "TK_CO_ID" ,
		"GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
		"GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
		"GHI_NO"         AS "NO_PHAT_SINH",
		"GHI_CO" AS "CO_PHAT_SINH",
		"DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
		"DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
	FROM TMP_KET_QUA
	OFFSET %(offset)s
    LIMIT %(limit)s;


        """
        return self.execute(query,params_sql)
    
    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_DON_MUA_HANG = params['CHON_TAT_CA_DON_MUA_HANG'] if 'CHON_TAT_CA_DON_MUA_HANG' in params.keys() else 'False'
        CHON_TAT_CA_NHA_CUNG_CAP = params['CHON_TAT_CA_NHA_CUNG_CAP'] if 'CHON_TAT_CA_NHA_CUNG_CAP' in params.keys() else 'False'
        CHON_TAT_CA_NHAN_VIEN = params['CHON_TAT_CA_NHAN_VIEN'] if 'CHON_TAT_CA_NHAN_VIEN' in params.keys() else 'False'
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CHON_TAT_CA_HOP_DONG = params['CHON_TAT_CA_HOP_DONG'] if 'CHON_TAT_CA_HOP_DONG' in params.keys() else 'False'
       
        HOP_DONG_MANY_IDS = params['HOP_DONG_MANY_IDS'] if 'HOP_DONG_MANY_IDS' in params.keys() else 'False'
        NHA_CUNG_CAP_MANY_IDS = params['NHA_CUNG_CAP_MANY_IDS'] if 'NHA_CUNG_CAP_MANY_IDS' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        NHAN_VIEN_MANY_IDS = params['NHAN_VIEN_MANY_IDS'] if 'NHAN_VIEN_MANY_IDS' in params.keys() else 'False'
        DON_MUA_HANG_MANY_IDS = params['DON_MUA_HANG_MANY_IDS'] if 'DON_MUA_HANG_MANY_IDS' in params.keys() else 'False'
        

        if(TU=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO in ('KHONG_CHON','NHAN_VIEN','CONG_TRINH','HOP_DONG_MUA','DON_MUA_HANG'):
            if CHON_TAT_CA_NHA_CUNG_CAP == 'False':
                if NHA_CUNG_CAP_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhà cung cấp>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'NHAN_VIEN':
            if CHON_TAT_CA_NHAN_VIEN == 'False':
                if NHAN_VIEN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')
        
        if THONG_KE_THEO == 'HOP_DONG_MUA':
            if CHON_TAT_CA_HOP_DONG == 'False':
                if HOP_DONG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hợp đồng>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'CONG_TRINH':
            if CHON_TAT_CA_CONG_TRINH == 'False':
                if CONG_TRINH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'DON_MUA_HANG':
            if CHON_TAT_CA_DON_MUA_HANG == 'False':
                if DON_MUA_HANG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đơn mua hàng>. Xin vui lòng chọn lại.')

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        currency_id = self.get_context('currency_id')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        loai_tien =''
        loai_tien_id = self.env['res.currency'].browse(currency_id)
        if loai_tien_id:
            loai_tien = loai_tien_id.MA_LOAI_TIEN
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan = ''
        so_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        if so_tai_khoan:
            tai_khoan = so_tai_khoan.SO_TAI_KHOAN
        param = 'Tài khoản: %s; Loại tiền: %s;Từ ngày: %s đến ngày %s' % (tai_khoan, loai_tien, TU_NGAY_F, DEN_NGAY_F)
        if (THONG_KE_THEO == 'KHONG_CHON'):
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_tra').read()[0]
        elif (THONG_KE_THEO == 'NHAN_VIEN'):
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_tra_nhanvien').read()[0]
        elif (THONG_KE_THEO == 'HOP_DONG_MUA'):
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_tra_hopdongmua').read()[0]
        elif (THONG_KE_THEO == 'CONG_TRINH'):
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_tra_congtrinh').read()[0]
        elif (THONG_KE_THEO == 'DON_MUA_HANG'):
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_tra_donmuahang').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action