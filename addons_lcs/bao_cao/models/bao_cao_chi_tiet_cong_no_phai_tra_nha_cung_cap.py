# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_CHI_TIET_CONG_NO_PHAI_TRA_NHA_CUNG_CAP(models.Model):
    _name = 'bao.cao.chi.tiet.cong.no.phai.tra.nha.cung.cap'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'), ('NHAN_VIEN', 'Nhân viên'), ('HOP_DONG_MUA', 'Hợp đồng mua'), ('CONG_TRINH', 'công trình'), ('DON_MUA_HANG', 'Đơn mua hàng'), ], string='Thông kê theo', help='Thông kê theo',default ='KHONG_CHON', required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='true')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',required=True)
    TU = fields.Date(string='Từ', help='Từ',required=True)
    DEN = fields.Date(string='Đến', help='Đến',required=True)
    NHOM_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm NCC', help='Nhóm nhà cung cấp')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_CO_ID = fields.Char(string='TK công nợ', help='Tài khoản công nợ')
    TK_DOI_TUONG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    NO_PHAT_SINH = fields.Float(string='Nợ', help='Nợ phát sinh',digits= decimal_precision.get_precision('VND'))
    CO_PHAT_SINH = fields.Float(string='Có', help='Có phát sinh',digits= decimal_precision.get_precision('VND'))
    NO_SO_DU = fields.Float(string='Nợ', help='Nợ số dư',digits= decimal_precision.get_precision('VND'))
    CO_SO_DU = fields.Float(string='Có', help='Có số dư',digits= decimal_precision.get_precision('VND'))
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau', help='Cộng gộp các bút toán giống nhau')
    CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán thuế giống nhau', help='Cộng gộp các bút toán thuế giống nhau')
    name = fields.Char(string='Name', oldname='NAME')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')

    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')


    NHA_CUNG_CAP_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHA_CUNG_CAP = fields.Boolean('Tất cả nhà cung cấp', default=True)
    NHA_CUNG_CAP_MANY_IDS = fields.Many2many('res.partner','chi_tiet_cong_no_res_partner',domain=[('LA_NHA_CUNG_CAP', '=', True)], string='Chọn NCC')
    MA_PC_NHOM_NCC = fields.Char()

    NHAN_VIEN_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','chi_tiet_cong_no_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')

    HOP_DONG_IDS = fields.One2many ('purchase.ex.hop.dong.mua.hang')
    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('purchase.ex.hop.dong.mua.hang','chi_tiet_mua_hang_hdmh', string='Chọn hợp đồng') 


    CONG_TRINH_IDS = fields.One2many ('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','chi_tiet_mua_hang_danh_muc_cong_trinh', string='Chọn công trình') 

    DON_MUA_HANG_IDS = fields.One2many ('purchase.ex.don.mua.hang')
    CHON_TAT_CA_DON_MUA_HANG = fields.Boolean('Tất cả đơn mua hàng', default=True)
    DON_MUA_HANG_MANY_IDS = fields.Many2many('purchase.ex.don.mua.hang','chi_tiet_mua_hang_dmh', string='Chọn đơn mua hàng') 

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    
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
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    # Nhà cung cấp
    @api.onchange('NHA_CUNG_CAP_IDS')
    def update_NHA_CUNG_CAP_IDS(self):
        self.NHA_CUNG_CAP_MANY_IDS =self.NHA_CUNG_CAP_IDS.ids

    @api.onchange('NHOM_NCC_ID')
    def update_NHOM_NCC_ID(self):
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.MA_PC_NHOM_NCC =self.NHOM_NCC_ID.MA_PHAN_CAP

    @api.onchange('NHA_CUNG_CAP_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.NHA_CUNG_CAP_IDS = self.NHA_CUNG_CAP_MANY_IDS.ids
    
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
        if TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN

        currency_id = params['currency_id'] if 'currency_id' in params.keys() and params['currency_id'] != 'False' else None
        if currency_id == -1:
            currency_id = None
        else:
            currency_id = self.env['res.currency'].search([('id','=',currency_id)],limit=1).MA_LOAI_TIEN

        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        NHOM_NCC_ID = params['NHOM_NCC_ID'] if 'NHOM_NCC_ID' in params.keys() and params['NHOM_NCC_ID'] != 'False' else None
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 1 if 'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' in params.keys() and params['CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU']!= 'False' else 0
        CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1 if 'CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU' in params.keys() and params['CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU'] != 'False' else 0
        
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
        
        params = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'TAI_KHOAN_ID':TAI_KHOAN_ID, 
            'CHI_NHANH_ID': CHI_NHANH_ID, 
            'currency_id':currency_id, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'NHA_CUNG_CAP_IDS' : NHA_CUNG_CAP_IDS or None,
            'NHAN_VIEN_IDS' : NHAN_VIEN_IDS or None,
            'CONG_TRINH_IDS' : CONG_TRINH_IDS or None,
            'HOP_DONG_IDS' : HOP_DONG_IDS or None,
            'DON_MUA_HANG_IDS' : DON_MUA_HANG_IDS or None,

            'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' : CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU,
            'CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU' : CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU,
            'limit': limit,
            'offset': offset,

            }   


        # Execute SQL query here
        if (THONG_KE_THEO == 'NHAN_VIEN'):
            return self._lay_bao_cao_nhan_vien(params)

        elif (THONG_KE_THEO == 'KHONG_CHON'):
          return self._lay_bao_cao_khong_chon(params)
          
        elif (THONG_KE_THEO == 'HOP_DONG_MUA'):
          return self._lay_bao_cao_hop_dong_mua(params)
        
        elif (THONG_KE_THEO == 'CONG_TRINH'):
          return self._lay_bao_cao_cong_trinh(params)    
            
        else:
          return self._lay_bao_cao_don_mua_hang(params)    
        
    def _lay_bao_cao_hop_dong_mua(self, params):      
      record = []
      cr = self.env.cr
      query = """

            DO LANGUAGE plpgsql $$
            DECLARE

                chi_nhanh_id                        INTEGER :=%(CHI_NHANH_ID)s;
            
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                           DATE := %(DEN_NGAY)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
                so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;
            
               
            
               loai_tien_id                        VARCHAR(127) :=%(currency_id)s;
            
            
                CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU     INTEGER :=%(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;


                rec                                 RECORD;
                AccountNumberPercent                VARCHAR(100);
                  SO_TIEN_TON_NGUYEN_TE_TMP           FLOAT := 0;

                SO_TIEN_TON_TMP                     FLOAT := 0;

                MA_KHACH_HANG_TMP                   VARCHAR(100) := N'';

                SO_HOP_DONG_TMP                    VARCHAR(100) := N'';

                SO_TAI_KHOAN_TMP                    VARCHAR(100) := N'';

                CHI_NHANH_ID_TMP    INTEGER := NULL;

            BEGIN

                DROP TABLE IF EXISTS DS_KHACH_HANG_NCC
                ;

                CREATE TEMP TABLE DS_KHACH_HANG_NCC
                    AS
                        SELECT
                            AO.id


                        FROM res_partner AS AO
                       WHERE (AO.id  = any( %(NHA_CUNG_CAP_IDS)s))
                ;

                DROP TABLE IF EXISTS DS_HOP_DONG_MUA
                ;

                CREATE TEMP TABLE DS_HOP_DONG_MUA
                    AS
                        SELECT
                           *
                        FROM purchase_ex_hop_dong_mua_hang
                        WHERE (id = any( %(HOP_DONG_IDS)s))
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
                            , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                            , A."TINH_CHAT"
                        FROM danh_muc_he_thong_tai_khoan AS A
                        WHERE A."SO_TAI_KHOAN" = so_tai_khoan
                        ORDER BY A."SO_TAI_KHOAN",
                            A."TEN_TAI_KHOAN"
                ;
            ELSE
                CREATE TEMP TABLE TMP_TAI_KHOAN
                    AS
                        SELECT
                            A."SO_TAI_KHOAN"
                            , A."TEN_TAI_KHOAN"
                            , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                            , A."TINH_CHAT"
                        FROM danh_muc_he_thong_tai_khoan AS A
                        WHERE A."CHI_TIET_THEO_DOI_TUONG" = '1'
                              AND "DOI_TUONG_SELECTION" = '0'
                              AND "LA_TK_TONG_HOP" = '0'
                        --AND IsParent = 0
                        ORDER BY A."SO_TAI_KHOAN",
                            A."TEN_TAI_KHOAN"
                ;
            END IF
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
                "SO_HOP_DONG_MUA"           VARCHAR(200)
                ,
                "DOI_TUONG_ID"          INT
                ,
                "MA_DOI_TUONG"          VARCHAR(200)
                ,
                "TEN_DOI_TUONG"         VARCHAR(200)
        
                ,
                "NGAY_HACH_TOAN"        TIMESTAMP
                ,
                "NGAY_CHUNG_TU"         TIMESTAMP
                ,
                "SO_CHUNG_TU"           VARCHAR(200)
                ,
                "ID_CHUNG_TU"           INT
        
                ,
                "LOAI_CHUNG_TU"         VARCHAR(200)
                ,
                "DIEN_GIAI_CHUNG"       VARCHAR(200)
                ,
                "SO_TAI_KHOAN"          VARCHAR(200)
                ,
                "TINH_CHAT"             VARCHAR(200)
                ,
                "MA_TAI_KHOAN_DOI_UNG"  VARCHAR(200)
                ,
                "GHI_NO_NGUYEN_TE"      FLOAT
                ,
                "GHI_NO"                FLOAT
                ,
                "GHI_CO_NGUYEN_TE"      FLOAT
                ,
                "GHI_CO"                FLOAT
                , -- Phát sinh có quy đổi
                "DU_NO_NGUYEN_TE"  FLOAT
                , --Dư Nợ
                "DU_NO"    FLOAT
                , --   --Dư Nợ Quy đổi
                "DU_CO_NGUYEN_TE" FLOAT
                , --   --Dư Có
                "DU_CO"   FLOAT
                --   --Dư Có quy đổi
                ,
                "MODEL_CHUNG_TU"        VARCHAR(200)
        
                ,
                "OrderType"             INT
                ,
                "CHI_NHANH_ID"          INT
            )
            ;
        
        
        
            IF CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 0
            THEN
                INSERT INTO TMP_KET_QUA
                    (
        
                         "SO_HOP_DONG_MUA"
                ,
                "DOI_TUONG_ID"
                ,
                "MA_DOI_TUONG"
                ,
                "TEN_DOI_TUONG"
        
                ,
                "NGAY_HACH_TOAN"
                ,
                "NGAY_CHUNG_TU"
                ,
                "SO_CHUNG_TU"
                ,
                "ID_CHUNG_TU"
        
                ,
                "LOAI_CHUNG_TU"
                ,
                "DIEN_GIAI_CHUNG"
                ,
                "SO_TAI_KHOAN"
                ,
                "TINH_CHAT"
                ,
                "MA_TAI_KHOAN_DOI_UNG"
                ,
                "GHI_NO_NGUYEN_TE"
                ,
                "GHI_NO"
                ,
                "GHI_CO_NGUYEN_TE"
                ,
                "GHI_CO"
                , -- Phát sinh có quy đổi
                "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                "DU_NO"
                , --   --Dư Nợ Quy đổi
                "DU_CO_NGUYEN_TE"
                , --   --Dư Có
                "DU_CO"
                --   --Dư Có quy đổi
                ,
                "MODEL_CHUNG_TU"
        
                ,
                "OrderType"
                ,
                "CHI_NHANH_ID"
        
        
                     )
        
        
        
                        SELECT
                            "SO_HOP_DONG_MUA"
                            ,"DOI_TUONG_ID"
                            , "MA_DOI_TUONG"
                            , "TEN_DOI_TUONG"
        
                            , "NGAY_HACH_TOAN"
                            , "NGAY_CHUNG_TU"
                            , "SO_CHUNG_TU"
                            , "ID_CHUNG_TU"
        
                            , "LOAI_CHUNG_TU"
                            , "DIEN_GIAI_CHUNG"
                            , "SO_TAI_KHOAN"
                            , "TINH_CHAT"
                            , "MA_TAI_KHOAN_DOI_UNG"
                            , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                            , SUM("GHI_NO")           AS "GHI_NO"
                            , SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                            , SUM("GHI_CO")           AS "GHI_CO"
                            , -- Phát sinh có quy đổi
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")) > 0
                                   THEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE"))
                                    ELSE 0
                                    END
                               END)                   AS "DU_NO_NGUYEN_TE"
                            , --Dư Nợ
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN (SUM("DU_NO") - SUM("DU_CO"))
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_NO") - SUM("DU_CO")) > 0
                                   THEN SUM("DU_NO") - SUM("DU_CO")
                                    ELSE 0
                                    END
                               END)                   AS "DU_NO"
                            , --   --Dư Nợ Quy đổi
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE")) > 0
                                   THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                                    ELSE 0
                                    END
                               END)                   AS "DU_CO_NGUYEN_TE"
                            , --   --Dư Có
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN (SUM("DU_CO") - SUM("DU_NO"))
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_CO") - SUM("DU_NO")) > 0
                                   THEN (SUM("DU_CO") - SUM("DU_NO"))
                                    ELSE 0
                                    END
                               END)                   AS "DU_CO"
                            --   --Dư Có quy đổi
                            , "MODEL_CHUNG_TU"
                              ,
                            "OrderType"
                            ,
                            "CHI_NHANH_ID"
                        FROM (
        
        
                                 SELECT
                                    AOL."SO_HOP_DONG_MUA"
                                     ,AOL."DOI_TUONG_ID"
                                     , AOL."MA_DOI_TUONG"
                                     , AOL."TEN_DOI_TUONG"
        
        
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."NGAY_HACH_TOAN"
                                       END AS "NGAY_HACH_TOAN"
                                     , -- Ngày hạch toán
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE "NGAY_CHUNG_TU"
                                       END AS "NGAY_CHUNG_TU"
                                     , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."SO_CHUNG_TU"
                                       END AS "SO_CHUNG_TU"
                                     , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."ID_CHUNG_TU"
                                       END AS "ID_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."LOAI_CHUNG_TU"
                                       END AS "LOAI_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN N'Số dư đầu kỳ'
        
                                       ELSE AOL."DIEN_GIAI"
                                       END AS "DIEN_GIAI_CHUNG"
        
                                     /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
        
                                     , TBAN."SO_TAI_KHOAN"
                                     , -- TK công nợ
                                     TBAN."TINH_CHAT"
                                     , -- Tính chất tài khoản
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."MA_TK_DOI_UNG"
                                       END AS "MA_TAI_KHOAN_DOI_UNG"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                                     , -- Phát sinh có quy đổi
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO_NGUYEN_TE"
                                       ELSE 0
                                       END AS "DU_NO_NGUYEN_TE"
                                     , --Dư Nợ
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO"
                                       ELSE 0
                                       END AS "DU_NO"
                                     , --Dư Nợ Quy đổi
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO_NGUYEN_TE"
                                       ELSE 0
                                       END AS "DU_CO_NGUYEN_TE"
                                     , --Dư Có
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO"
                                       ELSE 0
                                       END AS "DU_CO"
                                     , --Dư Có quy đổi
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                                       END AS "THU_TU_TRONG_CHUNG_TU"
                                     , AOL."MODEL_CHUNG_TU"
                                     ,
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                       ELSE 1
                                       END AS "OrderType"
                                        , AOL."CHI_NHANH_ID"
                                         ,
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                       END AS "THU_TU_CHI_TIET_GHI_SO"
                                 FROM so_cong_no_chi_tiet AS AOL
                                     INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                     INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                     INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                     INNER JOIN (SELECT *
                                                 FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                              bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                         ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
        
                                      INNER JOIN DS_HOP_DONG_MUA AS LCID ON AOL."HOP_DONG_MUA_ID" = LCID.id
                                     LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
        
        
                                 WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                       AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                       AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                       AND AN."DOI_TUONG_SELECTION" = '0'
                             ) AS RSNS
        
        
                        WHERE
                            (RSNS."GHI_NO_NGUYEN_TE" <> 0
                             OR RSNS."GHI_CO_NGUYEN_TE" <> 0
                             OR RSNS."GHI_NO" <> 0
                             OR RSNS."GHI_CO" <> 0
                            )
        
                            OR
                            ("DU_CO_NGUYEN_TE" <> 0
                             OR "DU_NO_NGUYEN_TE" <> 0
                             OR "DU_CO" <> 0
                             OR "DU_NO" <> 0
                            )
        
        
                        GROUP BY
        
                            RSNS."SO_HOP_DONG_MUA"
                            ,RSNS."DOI_TUONG_ID"
                            , RSNS."MA_DOI_TUONG"
                            , RSNS."TEN_DOI_TUONG"
                            --, RSNS."DIA_CHI"
                            , RSNS."NGAY_HACH_TOAN"
                            , RSNS."NGAY_CHUNG_TU"
                            , RSNS."SO_CHUNG_TU"
                            , RSNS."ID_CHUNG_TU"
                            , RSNS."LOAI_CHUNG_TU"
                            , RSNS."MA_TAI_KHOAN_DOI_UNG"
                            , RSNS."DIEN_GIAI_CHUNG"
                            , RSNS."SO_TAI_KHOAN"
        
                            , RSNS."TINH_CHAT"
                            , RSNS."GHI_NO_NGUYEN_TE"
                            , RSNS."GHI_NO"
                            , RSNS."GHI_CO_NGUYEN_TE"
                            , RSNS."GHI_CO"
                            , RSNS."THU_TU_TRONG_CHUNG_TU"
                            , RSNS."MODEL_CHUNG_TU"
                             , RSNS."OrderType"
                            , RSNS."CHI_NHANH_ID"
                             , RSNS."THU_TU_CHI_TIET_GHI_SO"
        
        
                        HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                               OR SUM("GHI_NO") <> 0
                               OR SUM("GHI_CO_NGUYEN_TE") <> 0
                               OR SUM("GHI_CO") <> 0
                               OR SUM("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <> 0
                               OR SUM("DU_NO" - "DU_CO") <> 0
        
                        ORDER BY
        
                             RSNS."SO_HOP_DONG_MUA",
        
                            RSNS."CHI_NHANH_ID",
                            RSNS."MA_DOI_TUONG",
        
                            RSNS."SO_TAI_KHOAN",
                            RSNS."OrderType",
                              RSNS."NGAY_HACH_TOAN",
                            RSNS."NGAY_CHUNG_TU",
                            RSNS."SO_CHUNG_TU",
                            RSNS."THU_TU_CHI_TIET_GHI_SO",
                            RSNS."MA_TAI_KHOAN_DOI_UNG"
        
                ;
            ELSE
                INSERT INTO TMP_KET_QUA
                    (
        
                         "SO_HOP_DONG_MUA"
                ,
                "DOI_TUONG_ID"
                ,
                "MA_DOI_TUONG"
                ,
                "TEN_DOI_TUONG"
        
                ,
                "NGAY_HACH_TOAN"
                ,
                "NGAY_CHUNG_TU"
                ,
                "SO_CHUNG_TU"
                ,
                "ID_CHUNG_TU"
        
                ,
                "LOAI_CHUNG_TU"
                ,
                "DIEN_GIAI_CHUNG"
                ,
                "SO_TAI_KHOAN"
                ,
                "TINH_CHAT"
                ,
                "MA_TAI_KHOAN_DOI_UNG"
                ,
                "GHI_NO_NGUYEN_TE"
                ,
                "GHI_NO"
                ,
                "GHI_CO_NGUYEN_TE"
                ,
                "GHI_CO"
                , -- Phát sinh có quy đổi
                "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                "DU_NO"
                , --   --Dư Nợ Quy đổi
                "DU_CO_NGUYEN_TE"
                , --   --Dư Có
                "DU_CO"
                --   --Dư Có quy đổi
                ,
                "MODEL_CHUNG_TU"
        
                ,
                "OrderType"
                ,
                "CHI_NHANH_ID"
        
        
                     )
        
                        SELECT
                           "SO_HOP_DONG_MUA"
                            ,"DOI_TUONG_ID"
                            , "MA_DOI_TUONG"
                            , "TEN_DOI_TUONG"
        
                            , "NGAY_HACH_TOAN"
                            , "NGAY_CHUNG_TU"
                            , "SO_CHUNG_TU"
                            , "ID_CHUNG_TU"
        
                            , "LOAI_CHUNG_TU"
                            , "DIEN_GIAI_CHUNG"
                            , "SO_TAI_KHOAN"
                            , "TINH_CHAT"
                            , "MA_TAI_KHOAN_DOI_UNG"
                            , ("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                            , ("GHI_NO")           AS "GHI_NO"
                            , ("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                            , ("GHI_CO")           AS "GHI_CO"
                            , -- Phát sinh có quy đổi
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE") > 0
                                   THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                                    ELSE 0
                                    END
                               END)                AS "DU_NO_NGUYEN_TE"
                            , --Dư Nợ
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN ("DU_NO") - ("DU_CO")
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN ("DU_NO") - ("DU_CO") > 0
                                   THEN ("DU_NO") - ("DU_CO")
                                    ELSE 0
                                    END
                               END)                AS "DU_NO"
                            , --   --Dư Nợ Quy đổi
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE") > 0
                                   THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                                    ELSE 0
                                    END
                               END)                AS "DU_CO_NGUYEN_TE"
                            , --   --Dư Có
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN ("DU_CO") - ("DU_NO")
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN ("DU_CO") - ("DU_NO") > 0
                                   THEN ("DU_CO") - ("DU_NO")
                                    ELSE 0
                                    END
                               END)                AS "DU_CO"
                            --   --Dư Có quy đổi
                            , "MODEL_CHUNG_TU"
                              ,
                            "OrderType"
                            ,
                            "CHI_NHANH_ID"
        
                        FROM (
                                 SELECT
                                    AOL."SO_HOP_DONG_MUA"
                                    , AOL."DOI_TUONG_ID"
                                     , AOL."MA_DOI_TUONG"
                                     , AOL."TEN_DOI_TUONG"
                                     --, AOL."DIA_CHI"
        
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."NGAY_HACH_TOAN"
                                       END      AS "NGAY_HACH_TOAN"
                                     , -- Ngày hạch toán
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE "NGAY_CHUNG_TU"
                                       END      AS "NGAY_CHUNG_TU"
                                     , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."SO_CHUNG_TU"
                                       END      AS "SO_CHUNG_TU"
                                     , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."ID_CHUNG_TU"
                                       END      AS "ID_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."LOAI_CHUNG_TU"
                                       END      AS "LOAI_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN N'Số dư đầu kỳ'
        
                                       ELSE AOL."DIEN_GIAI_CHUNG"
                                       END      AS "DIEN_GIAI_CHUNG"
        
                                     /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
        
                                     , TBAN."SO_TAI_KHOAN"
                                     , -- TK công nợ
                                     TBAN."TINH_CHAT"
                                     , -- Tính chất tài khoản
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."MA_TK_DOI_UNG"
                                       END      AS "MA_TAI_KHOAN_DOI_UNG"
                                     , SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN 0
                                           ELSE AOL."GHI_NO_NGUYEN_TE"
                                           END) AS "GHI_NO_NGUYEN_TE"
                                     , -- Phát sinh nợ
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                           ELSE AOL."GHI_NO"
                                           END) AS "GHI_NO"
                                     , -- Phát sinh nợ quy đổi
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                           ELSE AOL."GHI_CO_NGUYEN_TE"
                                           END) AS "GHI_CO_NGUYEN_TE"
                                     , -- Phát sinh có
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                           ELSE AOL."GHI_CO"
                                           END) AS "GHI_CO"
                                     , -- Phát sinh có quy đổi
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO_NGUYEN_TE"
                                           ELSE 0
                                           END) AS "DU_NO_NGUYEN_TE"
                                     , --Dư Nợ
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO"
                                           ELSE 0
                                           END) AS "DU_NO"
                                     , --Dư Nợ Quy đổi
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO_NGUYEN_TE"
                                           ELSE 0
                                           END) AS "DU_CO_NGUYEN_TE"
                                     , --Dư Có
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO"
                                           ELSE 0
                                           END) AS "DU_CO"
                                     --Dư Có quy đổi
        
                                     , AOL."MODEL_CHUNG_TU"
                                          ,
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                       ELSE 1
                                       END AS "OrderType"
                                        , AOL."CHI_NHANH_ID"
                                         ,
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                       END AS "THU_TU_CHI_TIET_GHI_SO"
        
                                 FROM so_cong_no_chi_tiet AS AOL
                                     INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                     INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                     INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                     INNER JOIN (SELECT *
                                                 FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                              bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                         ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
        
                                     INNER JOIN DS_HOP_DONG_MUA AS LCID ON AOL."HOP_DONG_MUA_ID" = LCID.id
                                     LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
        
                                 WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                       AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                       AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                       AND AN."DOI_TUONG_SELECTION" = '0'
        
                                 GROUP BY
                                    AOL."SO_HOP_DONG_MUA"
                                     ,AOL."DOI_TUONG_ID"
                                     , AOL."MA_DOI_TUONG"
                                     , AOL."TEN_DOI_TUONG"
        
        
                                     ,
                                     AOL."NGAY_HACH_TOAN"
        
                                     , -- Ngày hạch toán
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE "NGAY_CHUNG_TU"
                                     END
                                     , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."SO_CHUNG_TU"
                                     END
                                     , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."ID_CHUNG_TU"
                                     END
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."LOAI_CHUNG_TU"
                                       END
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN N'Số dư đầu kỳ'
        
                                       ELSE AOL."DIEN_GIAI_CHUNG"
                                       END
        
                                     /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
        
                                     , TBAN."SO_TAI_KHOAN"
                                     , -- TK công nợ
                                     TBAN."TINH_CHAT"
                                     , -- Tính chất tài khoản
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."MA_TK_DOI_UNG"
                                     END
        
                                     , AOL."MODEL_CHUNG_TU"
                                             ,
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                       ELSE 1
                                       END
                                        , AOL."CHI_NHANH_ID"
                                         ,
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                       END
        
                             ) AS RSS
        
        
                        WHERE RSS."GHI_NO_NGUYEN_TE" <> 0
                              OR RSS."GHI_NO" <> 0
                              OR RSS."GHI_CO_NGUYEN_TE" <> 0
                              OR RSS."GHI_CO" <> 0
                              OR "DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE" <> 0
                              OR "DU_CO" - "DU_NO" <> 0
        
                        ORDER BY
        
                              RSS."SO_HOP_DONG_MUA",
                              RSS."CHI_NHANH_ID",
                            RSS."MA_DOI_TUONG",
        
                            RSS."SO_TAI_KHOAN",
                              RSS."OrderType",
                            RSS."NGAY_HACH_TOAN",
                            RSS."NGAY_CHUNG_TU",
                            RSS."SO_CHUNG_TU",
                          RSS."THU_TU_CHI_TIET_GHI_SO"
        
                ;
        
            END IF
            ;
        
        
             FOR rec IN
            SELECT *
            FROM TMP_KET_QUA
            WHERE "OrderType" <> 2
        
            ORDER BY
                RowNum
            LOOP
                SELECT (CASE WHEN rec."OrderType" = 0
                    THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0 --DU_NO_NGUYEN_TE
                        THEN rec."DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                          ELSE -1
                               * rec."DU_NO_NGUYEN_TE" --DU_NO_NGUYEN_TE
                          END)
                        WHEN
        
                             SO_HOP_DONG_TMP <> rec."SO_HOP_DONG_MUA"
                             OR CHI_NHANH_ID_TMP <> rec."CHI_NHANH_ID"
                           OR MA_KHACH_HANG_TMP <> rec."MA_DOI_TUONG"
                            OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
        
                            THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                        ELSE SO_TIEN_TON_NGUYEN_TE_TMP + rec."GHI_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                             - rec."GHI_NO_NGUYEN_TE" --GHI_NO_NGUYEN_TE
                        END)
                INTO SO_TIEN_TON_NGUYEN_TE_TMP
        
            ;
        
                rec."DU_NO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
                    THEN -1 * SO_TIEN_TON_NGUYEN_TE_TMP
                                         WHEN rec."TINH_CHAT" = '1'
                                             THEN 0
                                         ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
                                             THEN -1
                                                  * SO_TIEN_TON_NGUYEN_TE_TMP
                                              ELSE 0
                                              END
                                         END)
            ;
        
                UPDATE TMP_KET_QUA
                SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
                WHERE RowNum = rec.RowNum
            ;
        
                rec."DU_CO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
                    THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                         WHEN rec."TINH_CHAT" = '0'
                                             THEN 0
                                         ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
                                             THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                              ELSE 0
                                              END
                                         END)
            ;
        
                UPDATE TMP_KET_QUA
                SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
                WHERE RowNum = rec.RowNum
            ;
        
                SELECT (CASE WHEN rec."OrderType" = 0
                    THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                        THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                          ELSE -1
                               * rec."DU_NO" --DU_NO_NGUYEN_TE
                          END)
                        WHEN
        
        
                             SO_HOP_DONG_TMP <> rec."SO_HOP_DONG_MUA"
        
                           OR MA_KHACH_HANG_TMP <> rec."MA_DOI_TUONG"
                            OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                            THEN rec."GHI_CO" - rec."GHI_NO" --PHAT_SINH_CO_NGUYEN_TE
                        ELSE SO_TIEN_TON_TMP + rec."GHI_CO"--PHAT_SINH_CO_NGUYEN_TE
                             - rec."GHI_NO" --GHI_NO_NGUYEN_TE
                        END)
                INTO SO_TIEN_TON_TMP
            ;
        
                rec."DU_NO" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
                    THEN -1 * SO_TIEN_TON_TMP
                               WHEN rec."TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN SO_TIEN_TON_TMP < 0
                                   THEN -1
                                        * SO_TIEN_TON_TMP
                                    ELSE 0
                                    END
                               END)
            ;
        
                UPDATE TMP_KET_QUA
                SET "DU_NO" = rec."DU_NO"
                WHERE RowNum = rec.RowNum
            ;
        
        
                rec."DU_CO" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
                    THEN SO_TIEN_TON_TMP
                               WHEN rec."TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN SO_TIEN_TON_TMP > 0
                                   THEN SO_TIEN_TON_TMP
                                    ELSE 0
                                    END
                               END)
            ;
        
                UPDATE TMP_KET_QUA
                SET "DU_CO" = rec."DU_CO"
                WHERE RowNum = rec.RowNum
            ;
        
        
                SO_HOP_DONG_TMP = rec."SO_HOP_DONG_MUA"
            ;
        
                CHI_NHANH_ID_TMP = rec."CHI_NHANH_ID"
            ;
                 MA_KHACH_HANG_TMP = rec."MA_DOI_TUONG"
            ;
        
                SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
            ;
        
        
            END LOOP
            ;
        
        
        
        
        END $$
        ;
        
        SELECT *
        FROM TMP_KET_QUA 
       OFFSET %(offset)s
      LIMIT %(limit)s
;
 """

      cr.execute(query,params)
              # Get and show result
      for line in cr.dictfetchall():
          record.append({
              
              'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
              'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
              'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
              'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
              'TK_CO_ID': line.get('SO_TAI_KHOAN', ''),
              'TK_DOI_TUONG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
              'NO_PHAT_SINH': line.get('GHI_NO', ''),
              'CO_PHAT_SINH': line.get('GHI_CO', ''),
              'NO_SO_DU': line.get('DU_NO', ''),
              'CO_SO_DU': line.get('DU_CO', ''),
              'SO_HOP_DONG': line.get('SO_HOP_DONG_MUA', ''),
              
              'TEN_NHA_CUNG_CAP': line.get('TEN_DOI_TUONG', ''),
              'name': '',
              'ID_GOC': line.get('ID_CHUNG_TU', ''),
              'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
              })
      return record












     # lấy báo cáo nhân viên    

    def _lay_bao_cao_nhan_vien(self, params):      
      record = []
      cr = self.env.cr
      query = """

                DO LANGUAGE plpgsql $$
                DECLARE
            
                chi_nhanh_id                        INTEGER :=%(CHI_NHANH_ID)s;
            
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                           DATE := %(DEN_NGAY)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
                 so_tai_khoan                          VARCHAR(127) := %(TAI_KHOAN_ID)s;
            
               
            
                loai_tien_id                           VARCHAR(127) :=%(currency_id)s;
            
            
                CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU     INTEGER :=%(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;
            
            
              
            
            
                rec                                 RECORD;
            
                AccountNumberPercent                VARCHAR(100);
                 SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT := 0;

                SO_TIEN_TON_TMP                       FLOAT := 0;

                MA_KHACH_HANG_TMP                     VARCHAR(100) := N'';

                MA_NHAN_VIEN_TMP                     VARCHAR(100) := N'';

                SO_TAI_KHOAN_TMP                      VARCHAR(100) := N'';
            
            BEGIN
            
                DROP TABLE IF EXISTS DS_KHACH_HANG_NCC
                ;
            
                CREATE TEMP TABLE DS_KHACH_HANG_NCC
                    AS
                        SELECT
                            AO.id
                            , AO."MA"
                            , AO."HO_VA_TEN"
                            , AO."DIA_CHI"
            
                            , AO."MA_SO_THUE"
            
                        FROM res_partner AS AO
                        WHERE (AO.id  = any( %(NHA_CUNG_CAP_IDS)s))
                ;
            
                DROP TABLE IF EXISTS DS_NHAN_VIEN
                ;
            
                CREATE TEMP TABLE DS_NHAN_VIEN
                    AS
                        SELECT *
                        FROM res_partner
                        WHERE (id = any( %(NHAN_VIEN_IDS)s))
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
                                , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                                , A."TINH_CHAT"
                            FROM danh_muc_he_thong_tai_khoan AS A
                            WHERE A."SO_TAI_KHOAN" = so_tai_khoan
                            ORDER BY A."SO_TAI_KHOAN",
                                A."TEN_TAI_KHOAN"
                    ;
                ELSE
                    CREATE TEMP TABLE TMP_TAI_KHOAN
                        AS
                            SELECT
                                A."SO_TAI_KHOAN"
                                , A."TEN_TAI_KHOAN"
                                , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                                , A."TINH_CHAT"
                            FROM danh_muc_he_thong_tai_khoan AS A
                            WHERE A."CHI_TIET_THEO_DOI_TUONG" = '1'
                                  AND "DOI_TUONG_SELECTION" = '0'
                                  AND "LA_TK_TONG_HOP" = '0'
                            --AND IsParent = 0
                            ORDER BY A."SO_TAI_KHOAN",
                                A."TEN_TAI_KHOAN"
                    ;
                END IF
                ;


                /*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/


                 DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
                ;

                CREATE TEMP SEQUENCE TMP_KET_QUA_seq

                ;

                CREATE TABLE TMP_KET_QUA
                (
                    RowNum                 INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
                        PRIMARY KEY,

                                "MA_NHAN_VIEN"   VARCHAR(200)
                                , "TEN_NHAN_VIEN"   VARCHAR(200)
                                , "DOI_TUONG_ID"     INT
                                , "MA_DOI_TUONG"      VARCHAR(200)
                                , "TEN_DOI_TUONG"      VARCHAR(200)
                                --, "DIA_CHI"
                                , "NGAY_HACH_TOAN"    TIMESTAMP
                                , "NGAY_CHUNG_TU"    TIMESTAMP
                                , "SO_CHUNG_TU"   VARCHAR(200)
                                , "ID_CHUNG_TU"   INT

                                , "LOAI_CHUNG_TU"   VARCHAR(200)
                                , "DIEN_GIAI_CHUNG"  VARCHAR(200)
                                , "SO_TAI_KHOAN"   VARCHAR(200)
                                , "TINH_CHAT"   VARCHAR(200)
                                , "MA_TAI_KHOAN_DOI_UNG"   VARCHAR(200)
                                ,"GHI_NO_NGUYEN_TE"    FLOAT
                                , "GHI_NO"   FLOAT
                                , "GHI_CO_NGUYEN_TE"  FLOAT
                                , "GHI_CO"   FLOAT
                                , -- Phát sinh có quy đổi
                                  "DU_NO_NGUYEN_TE" FLOAT
                                , --Dư Nợ
                                  "DU_NO"   FLOAT
                                , --   --Dư Nợ Quy đổi
                                  "DU_CO_NGUYEN_TE"  FLOAT
                                , --   --Dư Có
                                  "DU_CO"   FLOAT
                                --   --Dư Có quy đổi
                                , "MODEL_CHUNG_TU"    VARCHAR(200)

                                 ,
                                "OrderType"            INT
                )
                ;



                IF CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 0
                THEN
                    INSERT INTO TMP_KET_QUA
                    (

                                "MA_NHAN_VIEN"
                                , "TEN_NHAN_VIEN"
                                , "DOI_TUONG_ID"
                                , "MA_DOI_TUONG"
                                , "TEN_DOI_TUONG"
                                --, "DIA_CHI"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                ,"GHI_NO_NGUYEN_TE"
                                , "GHI_NO"
                                , "GHI_CO_NGUYEN_TE"
                                , "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  "DU_CO"
                                --   --Dư Có quy đổi
                                , "MODEL_CHUNG_TU"

                                 ,
                                "OrderType"


                     )



                            SELECT
                                "MA_NHAN_VIEN"
                                , "TEN_NHAN_VIEN"
                                , "DOI_TUONG_ID"
                                , "MA_DOI_TUONG"
                                , "TEN_DOI_TUONG"
                                --, "DIA_CHI"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                                , SUM("GHI_NO")           AS "GHI_NO"
                                , SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                                , SUM("GHI_CO")           AS "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  (CASE WHEN "TINH_CHAT" = '0'
                                      THEN SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")
                                   WHEN "TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")) > 0
                                       THEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE"))
                                        ELSE 0
                                        END
                                   END)                   AS "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  (CASE WHEN "TINH_CHAT" = '0'
                                      THEN (SUM("DU_NO") - SUM("DU_CO"))
                                   WHEN "TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_NO") - SUM("DU_CO")) > 0
                                       THEN SUM("DU_NO") - SUM("DU_CO")
                                        ELSE 0
                                        END
                                   END)                   AS "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  (CASE WHEN "TINH_CHAT" = '1'
                                      THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                                   WHEN "TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE")) > 0
                                       THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                                        ELSE 0
                                        END
                                   END)                   AS "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  (CASE WHEN "TINH_CHAT" = '1'
                                      THEN (SUM("DU_CO") - SUM("DU_NO"))
                                   WHEN "TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_CO") - SUM("DU_NO")) > 0
                                       THEN (SUM("DU_CO") - SUM("DU_NO"))
                                        ELSE 0
                                        END
                                   END)                   AS "DU_CO"
                                --   --Dư Có quy đổi
                                , "MODEL_CHUNG_TU"
                                  ,
                                "OrderType"
                            FROM (


                                     SELECT
                                         AOL."MA_NHAN_VIEN"
                                         , AOL."TEN_NHAN_VIEN"
                                         , AOL."DOI_TUONG_ID"
                                         , AOL."MA_DOI_TUONG"
                                         , AOL."TEN_DOI_TUONG"
                                         --, AOL."DIA_CHI"

                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."NGAY_HACH_TOAN"
                                           END AS "NGAY_HACH_TOAN"
                                         , -- Ngày hạch toán
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE "NGAY_CHUNG_TU"
                                           END AS "NGAY_CHUNG_TU"
                                         , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."SO_CHUNG_TU"
                                           END AS "SO_CHUNG_TU"
                                         , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."ID_CHUNG_TU"
                                           END AS "ID_CHUNG_TU"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."LOAI_CHUNG_TU"
                                           END AS "LOAI_CHUNG_TU"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN 'Số dư đầu kỳ'

                                           ELSE AOL."DIEN_GIAI"
                                           END AS "DIEN_GIAI_CHUNG"

                                         /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                                         , TBAN."SO_TAI_KHOAN"
                                         , -- TK công nợ
                                         TBAN."TINH_CHAT"
                                         , -- Tính chất tài khoản
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."MA_TK_DOI_UNG"
                                           END AS "MA_TAI_KHOAN_DOI_UNG"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                                         , -- Phát sinh có quy đổi
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_NO_NGUYEN_TE"
                                           ELSE 0
                                           END AS "DU_NO_NGUYEN_TE"
                                         , --Dư Nợ
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_NO"
                                           ELSE 0
                                           END AS "DU_NO"
                                         , --Dư Nợ Quy đổi
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_CO_NGUYEN_TE"
                                           ELSE 0
                                           END AS "DU_CO_NGUYEN_TE"
                                         , --Dư Có
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_CO"
                                           ELSE 0
                                           END AS "DU_CO"
                                         , --Dư Có quy đổi
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                                           END AS "THU_TU_TRONG_CHUNG_TU"
                                         , AOL."MODEL_CHUNG_TU"

                                          , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN 0
                                           ELSE 1
                                           END AS "OrderType"
                                         ,
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                           END AS "THU_TU_CHI_TIET_GHI_SO"
                                     FROM so_cong_no_chi_tiet AS AOL
                                         INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                         INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                         INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                         INNER JOIN (SELECT *
                                                     FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                                  bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                             ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"

                                         INNER JOIN DS_NHAN_VIEN AS LEID ON AOL."NHAN_VIEN_ID" = LEID.id
                                         LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
                                     -- Danh mục ĐVT
                                     /*hoant 27.09.2017 theo cr 138363*/


                                     WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                          AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                           AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                           AND AN."DOI_TUONG_SELECTION" = '0'
                                 ) AS RSNS


                            WHERE
                                (RSNS."GHI_NO_NGUYEN_TE" <> 0
                                 OR RSNS."GHI_CO_NGUYEN_TE" <> 0
                                 OR RSNS."GHI_NO" <> 0
                                 OR RSNS."GHI_CO" <> 0
                                )

                                OR
                                ("DU_CO_NGUYEN_TE" <> 0
                                 OR "DU_NO_NGUYEN_TE" <> 0
                                 OR "DU_CO" <> 0
                                 OR "DU_NO" <> 0
                                )


                            GROUP BY

                                RSNS."MA_NHAN_VIEN"
                                , RSNS."TEN_NHAN_VIEN"
                                , RSNS."DOI_TUONG_ID"
                                , RSNS."MA_DOI_TUONG"
                                , RSNS."TEN_DOI_TUONG"
                                --, RSNS."DIA_CHI"
                                , RSNS."NGAY_HACH_TOAN"
                                , RSNS."NGAY_CHUNG_TU"
                                , RSNS."SO_CHUNG_TU"
                                , RSNS."ID_CHUNG_TU"
                                , RSNS."LOAI_CHUNG_TU"
                                , RSNS."MA_TAI_KHOAN_DOI_UNG"
                                , RSNS."DIEN_GIAI_CHUNG"
                                , RSNS."SO_TAI_KHOAN"

                                , RSNS."TINH_CHAT"
                                , RSNS."GHI_NO_NGUYEN_TE"
                                , RSNS."GHI_NO"
                                , RSNS."GHI_CO_NGUYEN_TE"
                                , RSNS."GHI_CO"
                                , RSNS."THU_TU_TRONG_CHUNG_TU"
                                , RSNS."MODEL_CHUNG_TU"
                                 , RSNS."OrderType"
                                , RSNS."THU_TU_CHI_TIET_GHI_SO"


                            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                                   OR SUM("GHI_NO") <> 0
                                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                                   OR SUM("GHI_CO") <> 0
                                   OR SUM("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <> 0
                                   OR SUM("DU_NO" - "DU_CO") <> 0

                            ORDER BY
                                RSNS."MA_NHAN_VIEN",
                                RSNS."MA_DOI_TUONG",

                                RSNS."SO_TAI_KHOAN",
                                 RSNS."OrderType",
                                RSNS."NGAY_HACH_TOAN",
                                RSNS."NGAY_CHUNG_TU",
                                RSNS."SO_CHUNG_TU",
                                RSNS."THU_TU_TRONG_CHUNG_TU",
                                  RSNS."THU_TU_CHI_TIET_GHI_SO"

                    ;
                ELSE
                    INSERT INTO TMP_KET_QUA
                    (

                                "MA_NHAN_VIEN"
                                , "TEN_NHAN_VIEN"
                                , "DOI_TUONG_ID"
                                , "MA_DOI_TUONG"
                                , "TEN_DOI_TUONG"
                                --, "DIA_CHI"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                ,"GHI_NO_NGUYEN_TE"
                                , "GHI_NO"
                                , "GHI_CO_NGUYEN_TE"
                                , "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  "DU_CO"
                                --   --Dư Có quy đổi
                                , "MODEL_CHUNG_TU"

                                 ,
                                "OrderType"


                     )

                            SELECT
                                "MA_NHAN_VIEN"
                                , "TEN_NHAN_VIEN"
                                , "DOI_TUONG_ID"
                                , "MA_DOI_TUONG"
                                , "TEN_DOI_TUONG"
                                --, "DIA_CHI"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                , ("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                                , ("GHI_NO")           AS "GHI_NO"
                                , ("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                                , ("GHI_CO")           AS "GHI_CO"

                                  , -- Phát sinh có quy đổi
                                              (CASE WHEN "TINH_CHAT" = '0'
                                                  THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                                               WHEN "TINH_CHAT" = '1'
                                                   THEN 0
                                               ELSE CASE WHEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE") > 0
                                                   THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                                                    ELSE 0
                                                    END
                                               END)                AS "DU_NO_NGUYEN_TE"
                                            , --Dư Nợ
                                              (CASE WHEN "TINH_CHAT" = '0'
                                                  THEN ("DU_NO") - ("DU_CO")
                                               WHEN "TINH_CHAT" = '1'
                                                   THEN 0
                                               ELSE CASE WHEN ("DU_NO") - ("DU_CO") > 0
                                                   THEN ("DU_NO") - ("DU_CO")
                                                    ELSE 0
                                                    END
                                               END)                AS "DU_NO"
                                            , --   --Dư Nợ Quy đổi
                                              (CASE WHEN "TINH_CHAT" = '1'
                                                  THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                                               WHEN "TINH_CHAT" = '0'
                                                   THEN 0
                                               ELSE CASE WHEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE") > 0
                                                   THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                                                    ELSE 0
                                                    END
                                               END)                AS "DU_CO_NGUYEN_TE"
                                            , --   --Dư Có
                                              (CASE WHEN "TINH_CHAT" = '1'
                                                  THEN ("DU_CO") - ("DU_NO")
                                               WHEN "TINH_CHAT" = '0'
                                                   THEN 0
                                               ELSE CASE WHEN ("DU_CO") - ("DU_NO") > 0
                                                   THEN ("DU_CO") - ("DU_NO")
                                                    ELSE 0
                                                    END
                                               END)                AS "DU_CO"
                                , "MODEL_CHUNG_TU"
                                   ,
                                "OrderType"


                            FROM (
                                     SELECT
                                         AOL."MA_NHAN_VIEN"
                                         , AOL."TEN_NHAN_VIEN"
                                         , AOL."DOI_TUONG_ID"
                                         , AOL."MA_DOI_TUONG"
                                         , AOL."TEN_DOI_TUONG"
                                         --, AOL."DIA_CHI"

                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."NGAY_HACH_TOAN"
                                           END      AS "NGAY_HACH_TOAN"
                                         , -- Ngày hạch toán
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE "NGAY_CHUNG_TU"
                                           END      AS "NGAY_CHUNG_TU"
                                         , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."SO_CHUNG_TU"
                                           END      AS "SO_CHUNG_TU"
                                         , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."ID_CHUNG_TU"
                                           END      AS "ID_CHUNG_TU"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."LOAI_CHUNG_TU"
                                           END      AS "LOAI_CHUNG_TU"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN N'Số dư đầu kỳ'

                                           ELSE AOL."DIEN_GIAI_CHUNG"
                                           END      AS "DIEN_GIAI_CHUNG"

                                         /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                                         , TBAN."SO_TAI_KHOAN"
                                         , -- TK công nợ
                                         TBAN."TINH_CHAT"
                                         , -- Tính chất tài khoản
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."MA_TK_DOI_UNG"
                                           END      AS "MA_TAI_KHOAN_DOI_UNG"
                                         , SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN 0
                                               ELSE (AOL."GHI_NO_NGUYEN_TE")
                                               END) AS "GHI_NO_NGUYEN_TE"
                                         , -- Phát sinh nợ
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN 0
                                               ELSE (AOL."GHI_NO")
                                               END) AS "GHI_NO"
                                         , -- Phát sinh nợ quy đổi
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN 0
                                               ELSE (AOL."GHI_CO_NGUYEN_TE")
                                               END) AS "GHI_CO_NGUYEN_TE"
                                         , -- Phát sinh có
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN 0
                                               ELSE (AOL."GHI_CO")
                                               END) AS "GHI_CO"
                                         , -- Phát sinh có quy đổi
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_NO_NGUYEN_TE"
                                               ELSE 0
                                               END) AS "DU_NO_NGUYEN_TE"
                                         , --Dư Nợ
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_NO"
                                               ELSE 0
                                               END) AS "DU_NO"
                                         , --Dư Nợ Quy đổi
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_CO_NGUYEN_TE"
                                               ELSE 0
                                               END) AS "DU_CO_NGUYEN_TE"
                                         , --Dư Có
                                           SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_CO"
                                               ELSE 0
                                               END) AS "DU_CO"
                                          --Dư Có quy đổi

                                         , AOL."MODEL_CHUNG_TU"
                                           , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN 0
                                           ELSE 1
                                           END AS "OrderType"
                                         ,
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                           END AS "THU_TU_CHI_TIET_GHI_SO"


                                     FROM so_cong_no_chi_tiet AS AOL
                                         INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                         INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                         INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                         INNER JOIN (SELECT *
                                                     FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                                  bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                             ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"

                                         INNER JOIN DS_NHAN_VIEN AS LEID ON AOL."NHAN_VIEN_ID" = LEID.id
                                         LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id

                                     WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                        AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                           AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                           AND AN."DOI_TUONG_SELECTION" = '0'

                                     GROUP BY
                                         AOL."MA_NHAN_VIEN"
                                         , AOL."TEN_NHAN_VIEN"
                                         , AOL."DOI_TUONG_ID"
                                         , AOL."MA_DOI_TUONG"
                                         , AOL."TEN_DOI_TUONG"


                                         ,
                                         AOL."NGAY_HACH_TOAN"

                                         , -- Ngày hạch toán
                                         CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                             THEN NULL
                                         ELSE "NGAY_CHUNG_TU"
                                         END
                                         , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                         CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                             THEN NULL
                                         ELSE AOL."SO_CHUNG_TU"
                                         END
                                         , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                         CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                             THEN NULL
                                         ELSE AOL."ID_CHUNG_TU"
                                         END
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."LOAI_CHUNG_TU"
                                           END
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN N'Số dư đầu kỳ'

                                           ELSE AOL."DIEN_GIAI_CHUNG"
                                           END

                                         /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                                         , TBAN."SO_TAI_KHOAN"
                                         , -- TK công nợ
                                         TBAN."TINH_CHAT"
                                         , -- Tính chất tài khoản
                                         CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                             THEN NULL
                                         ELSE AOL."MA_TK_DOI_UNG"
                                         END

                                         , AOL."MODEL_CHUNG_TU"
                                          , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN 0
                                           ELSE 1
                                           END
                                         ,
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                           END




                                 ) AS RSS


                            WHERE RSS."GHI_NO_NGUYEN_TE" <> 0
                                  OR RSS."GHI_NO" <> 0
                                  OR RSS."GHI_CO_NGUYEN_TE" <> 0
                                  OR RSS."GHI_CO" <> 0
                                  OR "DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE" <> 0
                                  OR "DU_CO" - "DU_NO" <> 0



                            ORDER BY

                                RSS."MA_NHAN_VIEN",
                                RSS."MA_DOI_TUONG",

                                RSS."SO_TAI_KHOAN",
                                 RSS."OrderType",
                                RSS."NGAY_HACH_TOAN",
                                RSS."NGAY_CHUNG_TU",
                                RSS."SO_CHUNG_TU",
                                 RSS."THU_TU_CHI_TIET_GHI_SO"

                    ;


                END IF
                ;


                 FOR rec IN
                SELECT *
                FROM TMP_KET_QUA
                WHERE "OrderType" <> 2

                ORDER BY
                    RowNum
                LOOP
                    SELECT (CASE WHEN rec."OrderType" = 0
                        THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0 --DU_NO_NGUYEN_TE
                            THEN rec."DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                              ELSE -1
                                   * rec."DU_NO_NGUYEN_TE" --DU_NO_NGUYEN_TE
                              END)
                                WHEN
                                      MA_NHAN_VIEN_TMP <> rec."MA_NHAN_VIEN"
                                OR    MA_KHACH_HANG_TMP <> rec."MA_DOI_TUONG"
                                OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"

                                THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                            ELSE SO_TIEN_TON_NGUYEN_TE_TMP + rec."GHI_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                                 - rec."GHI_NO_NGUYEN_TE" --GHI_NO_NGUYEN_TE
                            END)
                    INTO SO_TIEN_TON_NGUYEN_TE_TMP

                ;

                    rec."DU_NO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
                        THEN -1 * SO_TIEN_TON_NGUYEN_TE_TMP
                                             WHEN rec."TINH_CHAT" = '1'
                                                 THEN 0
                                             ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
                                                 THEN -1
                                                      * SO_TIEN_TON_NGUYEN_TE_TMP
                                                  ELSE 0
                                                  END
                                             END)
                ;

                    UPDATE TMP_KET_QUA
                    SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
                    WHERE RowNum = rec.RowNum
                ;

                    rec."DU_CO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
                        THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                             WHEN rec."TINH_CHAT" = '0'
                                                 THEN 0
                                             ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
                                                 THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                                  ELSE 0
                                                  END
                                             END)
                ;

                    UPDATE TMP_KET_QUA
                    SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
                    WHERE RowNum = rec.RowNum
                ;

                    SELECT (CASE WHEN rec."OrderType" = 0
                        THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                            THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                              ELSE -1
                                   * rec."DU_NO" --DU_NO_NGUYEN_TE
                              END)
                            WHEN
                                      MA_NHAN_VIEN_TMP <> rec."MA_NHAN_VIEN"
                                OR    MA_KHACH_HANG_TMP <> rec."MA_DOI_TUONG"
                                OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                                THEN rec."GHI_CO" - rec."GHI_NO" --PHAT_SINH_CO_NGUYEN_TE
                            ELSE SO_TIEN_TON_TMP + rec."GHI_CO"--PHAT_SINH_CO_NGUYEN_TE
                                 - rec."GHI_NO" --GHI_NO_NGUYEN_TE
                            END)
                    INTO SO_TIEN_TON_TMP
                ;

                    rec."DU_NO" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
                        THEN -1 * SO_TIEN_TON_TMP
                                   WHEN rec."TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN SO_TIEN_TON_TMP < 0
                                       THEN -1
                                            * SO_TIEN_TON_TMP
                                        ELSE 0
                                        END
                                   END)
                ;

                    UPDATE TMP_KET_QUA
                    SET "DU_NO" = rec."DU_NO"
                    WHERE RowNum = rec.RowNum
                ;


                    rec."DU_CO" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
                        THEN SO_TIEN_TON_TMP
                                   WHEN rec."TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN SO_TIEN_TON_TMP > 0
                                       THEN SO_TIEN_TON_TMP
                                        ELSE 0
                                        END
                                   END)
                ;

                    UPDATE TMP_KET_QUA
                    SET "DU_CO" = rec."DU_CO"
                    WHERE RowNum = rec.RowNum
                ;

                    MA_NHAN_VIEN_TMP = rec."MA_NHAN_VIEN"
                ;

                    MA_KHACH_HANG_TMP = rec."MA_DOI_TUONG"
                ;

                    SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
                ;


                END LOOP
                ;



            END $$
            ;

           
      SELECT *
      FROM TMP_KET_QUA
      OFFSET %(offset)s
      LIMIT %(limit)s
      ;
 """


      cr.execute(query,params)
              # Get and show result
      for line in cr.dictfetchall():
          record.append({
            
              'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
              'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
              'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
              'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
              'TK_CO_ID': line.get('SO_TAI_KHOAN', ''),
              'TK_DOI_TUONG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
              'NO_PHAT_SINH': line.get('GHI_NO', ''),
              'CO_PHAT_SINH': line.get('GHI_CO', ''),
              'NO_SO_DU': line.get('DU_NO', ''),
              'CO_SO_DU': line.get('DU_CO', ''),
              
              'TEN_NHAN_VIEN': line.get('TEN_NHAN_VIEN', ''),
              'TEN_NHA_CUNG_CAP': line.get('TEN_DOI_TUONG', ''),
             
              'ID_GOC': line.get('ID_CHUNG_TU', ''),
              'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
              })
      return record
    







    # def _lay_bao_cao_khong_chon(self, params):      
    #   record = []
    #   cr = self.env.cr
    #   query = """
    #       DO LANGUAGE plpgsql $$
    #       DECLARE

    #          chi_nhanh_id                        INTEGER :=%(CHI_NHANH_ID)s;

    #               tu_ngay                             DATE := %(TU_NGAY)s;

    #               den_ngay                            DATE := %(DEN_NGAY)s;

    #               bao_gom_du_lieu_chi_nhanh_phu_thuoc  INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    #               tai_khoan_id                            INTEGER := %(TAI_KHOAN_ID)s;

                  

    #               loai_tien_id                        INTEGER :=%(currency_id)s;


    #               CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU                          INTEGER :=%(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    #               CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU                         INTEGER := %(CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU)s;


    #           rec                                 RECORD;
    #           AccountNumberPercent            VARCHAR(100);

    #       BEGIN

    #           DROP TABLE IF EXISTS DS_KHACH_HANG_NCC
    #           ;

    #           CREATE TEMP TABLE DS_KHACH_HANG_NCC
    #               AS
    #                   SELECT
    #                       AO.id
    #                       , AO."MA"
    #                       , AO."HO_VA_TEN"
    #                       , AO."DIA_CHI"

    #                       , AO."MA_SO_THUE"

    #                   FROM res_partner AS AO
    #                   WHERE (AO.id  = any( %(NHA_CUNG_CAP_IDS)s))
    #           ;


    #           DROP TABLE IF EXISTS TMP_TAI_KHOAN
    #           ;

    #           IF tai_khoan_id <> -1
    #           THEN
    #               CREATE TEMP TABLE TMP_TAI_KHOAN
    #                   AS
    #                       SELECT
    #                           A."SO_TAI_KHOAN"
    #                           , A."TEN_TAI_KHOAN"
    #                           , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
    #                           , A."TINH_CHAT"
    #                       FROM danh_muc_he_thong_tai_khoan AS A
    #                       WHERE A."id" = tai_khoan_id
    #                       ORDER BY A."SO_TAI_KHOAN",
    #                           A."TEN_TAI_KHOAN"
    #               ;
    #           ELSE
    #               CREATE TEMP TABLE TMP_TAI_KHOAN
    #                   AS
    #                       SELECT
    #                           A."SO_TAI_KHOAN"
    #                           , A."TEN_TAI_KHOAN"
    #                           , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
    #                           , A."TINH_CHAT"
    #                       FROM danh_muc_he_thong_tai_khoan AS A
    #                       WHERE A."CHI_TIET_THEO_DOI_TUONG" = '1'
    #                             AND "DOI_TUONG_SELECTION" = '0'
    #                           AND "LA_TK_TONG_HOP" = '0'
    #                       --AND IsParent = 0
    #                       ORDER BY A."SO_TAI_KHOAN",
    #                           A."TEN_TAI_KHOAN"
    #               ;
    #           END IF
    #           ;


    #           /*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/

    #           DROP TABLE IF EXISTS TMP_KET_QUA
    #           ;

    #           IF CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 0
    #           THEN
    #               CREATE TEMP TABLE TMP_KET_QUA
    #                   AS
    #                       SELECT
    #                           "DOI_TUONG_ID"
    #                           , "MA"
    #                           , "HO_VA_TEN"
    #                           , "DIA_CHI"
    #                           , "NGAY_HACH_TOAN"
    #                           , "NGAY_CHUNG_TU"
    #                           , "SO_CHUNG_TU"
    #                           , "ID_CHUNG_TU"

    #                           , "LOAI_CHUNG_TU"
    #                           , "DIEN_GIAI_CHUNG"
    #                           , "SO_TAI_KHOAN"
    #                           , "TINH_CHAT"
    #                           , "MA_TAI_KHOAN_DOI_UNG"
    #                           , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
    #                           , SUM("GHI_NO")           AS "GHI_NO"
    #                           , SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
    #                           , SUM("GHI_CO")           AS "GHI_CO"
    #                           , -- Phát sinh có quy đổi
    #                             (CASE WHEN "TINH_CHAT" = '0'
    #                                 THEN SUM("ClosingDebitAmountOC") - SUM("ClosingCreditAmountOC")
    #                             WHEN "TINH_CHAT" = '1'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingDebitAmountOC") - SUM("ClosingCreditAmountOC")) > 0
    #                                 THEN (SUM("ClosingDebitAmountOC") - SUM("ClosingCreditAmountOC"))
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingDebitAmountOC"
    #                           , --Dư Nợ
    #                             (CASE WHEN "TINH_CHAT" = '0'
    #                                 THEN (SUM("ClosingDebitAmount") - SUM("ClosingCreditAmount"))
    #                             WHEN "TINH_CHAT" = '1'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingDebitAmount") - SUM("ClosingCreditAmount")) > 0
    #                                 THEN SUM("ClosingDebitAmount") - SUM("ClosingCreditAmount")
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingDebitAmount"
    #                           , --   --Dư Nợ Quy đổi
    #                             (CASE WHEN "TINH_CHAT" = '1'
    #                                 THEN (SUM("ClosingCreditAmountOC") - SUM("ClosingDebitAmountOC"))
    #                             WHEN "TINH_CHAT" = '0'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingCreditAmountOC") - SUM("ClosingDebitAmountOC")) > 0
    #                                 THEN (SUM("ClosingCreditAmountOC") - SUM("ClosingDebitAmountOC"))
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingCreditAmountOC"
    #                           , --   --Dư Có
    #                             (CASE WHEN "TINH_CHAT" = '1'
    #                                 THEN (SUM("ClosingCreditAmount") - SUM("ClosingDebitAmount"))
    #                             WHEN "TINH_CHAT" = '0'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingCreditAmount") - SUM("ClosingDebitAmount")) > 0
    #                                 THEN (SUM("ClosingCreditAmount") - SUM("ClosingDebitAmount"))
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingCreditAmount"
    #                           --   --Dư Có quy đổi
    #                               , "MODEL_CHUNG_TU"
    #                       FROM (


    #                               SELECT
    #                                   AOL."DOI_TUONG_ID"
    #                                   , LAOI."MA"
    #                                   , LAOI."HO_VA_TEN"
    #                                   , LAOI."DIA_CHI"

    #                                   , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                   THEN NULL
    #                                     ELSE AOL."NGAY_HACH_TOAN"
    #                                     END AS "NGAY_HACH_TOAN"
    #                                   , -- Ngày hạch toán
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN NULL
    #                                     ELSE "NGAY_CHUNG_TU"
    #                                     END AS "NGAY_CHUNG_TU"
    #                                   , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN NULL
    #                                     ELSE AOL."SO_CHUNG_TU"
    #                                     END AS "SO_CHUNG_TU"
    #                                   , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN NULL
    #                                     ELSE AOL."ID_CHUNG_TU"
    #                                     END AS "ID_CHUNG_TU"
    #                                   , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                   THEN NULL
    #                                     ELSE AOL."LOAI_CHUNG_TU"
    #                                     END AS "LOAI_CHUNG_TU"
    #                                   , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                   THEN 'Số dư đầu kỳ'
    #                                     WHEN CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1
    #                                           AND (AOL."MA_TK_DOI_UNG" LIKE '3331%%' OR AOL."MA_TK_DOI_UNG" LIKE '133%%')
    #                                         THEN 'Thuế GTGT của hàng hóa, dịch vụ'
    #                                     ELSE AOL."DIEN_GIAI"
    #                                     END AS "DIEN_GIAI_CHUNG"

    #                                   /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

    #                                   , TBAN."SO_TAI_KHOAN"
    #                                   , -- TK công nợ
    #                                   TBAN."TINH_CHAT"
    #                                   , -- Tính chất tài khoản
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN NULL
    #                                     ELSE AOL."MA_TK_DOI_UNG"
    #                                     END AS "MA_TAI_KHOAN_DOI_UNG"
    #                                   , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                   THEN 0
    #                                     ELSE AOL."GHI_NO_NGUYEN_TE"
    #                                     END AS "GHI_NO_NGUYEN_TE"
    #                                   , -- Phát sinh nợ
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN 0
    #                                     ELSE AOL."GHI_NO"
    #                                     END AS "GHI_NO"
    #                                   , -- Phát sinh nợ quy đổi
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN 0
    #                                     ELSE AOL."GHI_CO_NGUYEN_TE"
    #                                     END AS "GHI_CO_NGUYEN_TE"
    #                                   , -- Phát sinh có
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN 0
    #                                     ELSE AOL."GHI_CO"
    #                                     END AS "GHI_CO"
    #                                   , -- Phát sinh có quy đổi
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN AOL."GHI_NO_NGUYEN_TE"
    #                                     ELSE 0
    #                                     END AS "ClosingDebitAmountOC"
    #                                   , --Dư Nợ
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN AOL."GHI_NO"
    #                                     ELSE 0
    #                                     END AS "ClosingDebitAmount"
    #                                   , --Dư Nợ Quy đổi
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN AOL."GHI_CO_NGUYEN_TE"
    #                                     ELSE 0
    #                                     END AS "ClosingCreditAmountOC"
    #                                   , --Dư Có
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN AOL."GHI_CO"
    #                                     ELSE 0
    #                                     END AS "ClosingCreditAmount"
    #                                   , --Dư Có quy đổi
    #                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                         THEN 0
    #                                     ELSE 1
    #                                     END AS "OrderType"
    #                                   , AOL."MODEL_CHUNG_TU"
    #                               FROM so_cong_no_chi_tiet AS AOL
    #                                   INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
    #                                   INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
    #                                   INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
    #                                   INNER JOIN (SELECT *
    #                                               FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
    #                                                                             bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
    #                                       ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
    #                                   LEFT JOIN danh_muc_vat_tu_hang_hoa I ON I.id = AOL."MA_HANG_ID"
    #                                   --Lấy lên tên hàng từ danh mục
    #                                   LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
    #                                   -- Danh mục ĐVT
    #                                   /*hoant 27.09.2017 theo cr 138363*/
    #                                   LEFT JOIN danh_muc_don_vi_tinh AS MainUnit
    #                                       ON AOL."DVT_CHINH_ID" = MainUnit.id -- Danh mục ĐVT chính

    #                               WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
    #                                     AND (loai_tien_id = -1 OR AOL."currency_id" = loai_tien_id)
    #                                     AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
    #                                     AND AN."DOI_TUONG_SELECTION" = '0'
    #                           ) AS RSNS

    #                       GROUP BY
    #                           RSNS."DOI_TUONG_ID",
    #                           RSNS."MA"
    #                           , RSNS."DOI_TUONG_ID"
    #                           , RSNS."MA"
    #                           , RSNS."HO_VA_TEN"
    #                           , RSNS."DIA_CHI"
    #                           , RSNS."NGAY_HACH_TOAN"
    #                           , RSNS."NGAY_CHUNG_TU"
    #                           , RSNS."SO_CHUNG_TU"
    #                           , RSNS."ID_CHUNG_TU"
    #                           , RSNS."LOAI_CHUNG_TU"
    #                           , RSNS."MA_TAI_KHOAN_DOI_UNG"
    #                           , RSNS."DIEN_GIAI_CHUNG"
    #                           , RSNS."SO_TAI_KHOAN"

    #                           , RSNS."TINH_CHAT"
    #                           , RSNS."GHI_NO_NGUYEN_TE"
    #                           , RSNS."GHI_NO"
    #                           , RSNS."GHI_CO_NGUYEN_TE"
    #                           , RSNS."GHI_CO"
    #                           ,RSNS."MODEL_CHUNG_TU"


    #                       HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
    #                             OR SUM("GHI_NO") <> 0
    #                             OR SUM("GHI_CO_NGUYEN_TE") <> 0
    #                             OR SUM("GHI_CO") <> 0
    #                             OR SUM("ClosingDebitAmountOC" - "ClosingCreditAmountOC") <> 0
    #                             OR SUM("ClosingDebitAmount" - "ClosingCreditAmount") <> 0

    #                           ORDER BY
    #                               RSNS."MA",
    #                               RSNS."SO_TAI_KHOAN",

    #                               RSNS."NGAY_HACH_TOAN",
    #                               RSNS."NGAY_CHUNG_TU",
    #                               RSNS."SO_CHUNG_TU"

    #                           ;
    #                   ELSE
    #                       CREATE TEMP TABLE TMP_KET_QUA
    #                       AS

    #                           SELECT
    #                           "DOI_TUONG_ID"
    #                           , "MA"
    #                           , "HO_VA_TEN"
    #                           , "DIA_CHI"
    #                           , "NGAY_HACH_TOAN"
    #                           , "NGAY_CHUNG_TU"
    #                           , "SO_CHUNG_TU"
    #                           , "ID_CHUNG_TU"
    #                           , "LOAI_CHUNG_TU"
    #                           , "DIEN_GIAI_CHUNG"
    #                           , "SO_TAI_KHOAN"
    #                           , "TINH_CHAT"
    #                           , "MA_TAI_KHOAN_DOI_UNG"
    #                           ,  "GHI_NO_NGUYEN_TE"
    #                           ,  "GHI_NO"
    #                           ,  "GHI_CO_NGUYEN_TE"
    #                           ,  "GHI_CO"
    #                           , -- Phát sinh có quy đổi
    #                             (CASE WHEN "TINH_CHAT" = '0'
    #                                 THEN SUM("ClosingDebitAmountOC") - SUM("ClosingCreditAmountOC")
    #                             WHEN "TINH_CHAT" = '1'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingDebitAmountOC") - SUM("ClosingCreditAmountOC")) > 0
    #                                 THEN (SUM("ClosingDebitAmountOC") - SUM("ClosingCreditAmountOC"))
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingDebitAmountOC"
    #                           , --Dư Nợ
    #                             (CASE WHEN "TINH_CHAT" = '0'
    #                                 THEN (SUM("ClosingDebitAmount") - SUM("ClosingCreditAmount"))
    #                             WHEN "TINH_CHAT" = '1'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingDebitAmount") - SUM("ClosingCreditAmount")) > 0
    #                                 THEN SUM("ClosingDebitAmount") - SUM("ClosingCreditAmount")
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingDebitAmount"
    #                           , --   --Dư Nợ Quy đổi
    #                             (CASE WHEN "TINH_CHAT" = '1'
    #                                 THEN (SUM("ClosingCreditAmountOC") - SUM("ClosingDebitAmountOC"))
    #                             WHEN "TINH_CHAT" = '0'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingCreditAmountOC") - SUM("ClosingDebitAmountOC")) > 0
    #                                 THEN (SUM("ClosingCreditAmountOC") - SUM("ClosingDebitAmountOC"))
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingCreditAmountOC"
    #                           , --   --Dư Có
    #                             (CASE WHEN "TINH_CHAT" = '1'
    #                                 THEN (SUM("ClosingCreditAmount") - SUM("ClosingDebitAmount"))
    #                             WHEN "TINH_CHAT" = '0'
    #                                 THEN 0
    #                             ELSE CASE WHEN (SUM("ClosingCreditAmount") - SUM("ClosingDebitAmount")) > 0
    #                                 THEN (SUM("ClosingCreditAmount") - SUM("ClosingDebitAmount"))
    #                                   ELSE 0
    #                                   END
    #                             END)                   AS "ClosingCreditAmount"
    #                           ,"MODEL_CHUNG_TU"


    #                       FROM (
    #                               SELECT
    #                                   AD."DOI_TUONG_ID"
    #                                   , AD."MA"
    #                                   , AD."HO_VA_TEN"
    #                                   , AD."DIA_CHI"
    #                                   , AD."NGAY_HACH_TOAN"
    #                                   , AD."NGAY_CHUNG_TU"
    #                                   , AD."SO_CHUNG_TU"
    #                                   , AD."ID_CHUNG_TU"
    #                                   , AD."LOAI_CHUNG_TU"
    #                                   , AD."DIEN_GIAI_CHUNG"
    #                                   , AD."SO_TAI_KHOAN"
    #                                   , AD."TINH_CHAT"
    #                                   , AD."MA_TAI_KHOAN_DOI_UNG"
    #                                   , SUM(AD."GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
    #                                   , SUM(AD."GHI_NO")           AS "GHI_NO"
    #                                   , SUM(AD."GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
    #                                   , SUM(AD."GHI_CO")           AS "GHI_CO"

    #                                   , SUM(AD."ClosingDebitAmountOC") AS "ClosingDebitAmountOC"
    #                                   , SUM(AD."ClosingDebitAmount")           AS "ClosingDebitAmount"
    #                                   , SUM(AD."ClosingCreditAmountOC") AS "ClosingCreditAmountOC"
    #                                   , SUM(AD."ClosingCreditAmount")           AS "ClosingCreditAmount"
    #                                   ,AD."MODEL_CHUNG_TU"



    #                           FROM (


    #                               SELECT
    #                               AOL."DOI_TUONG_ID"
    #                               , LAOI."MA"
    #                               , LAOI."HO_VA_TEN"
    #                               , LAOI."DIA_CHI"

    #                               ,
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN NULL
    #                                 ELSE AOL."NGAY_HACH_TOAN"
    #                                 END AS "NGAY_HACH_TOAN"
    #                               , -- Ngày hạch toán
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN NULL
    #                                 ELSE "NGAY_CHUNG_TU"
    #                                 END AS "NGAY_CHUNG_TU"
    #                               , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN NULL
    #                                 ELSE AOL."SO_CHUNG_TU"
    #                                 END AS "SO_CHUNG_TU"
    #                               , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN NULL
    #                                 ELSE AOL."ID_CHUNG_TU"
    #                                 END AS "ID_CHUNG_TU"
    #                               , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                             THEN NULL
    #                                 ELSE AOL."LOAI_CHUNG_TU"
    #                                 END AS "LOAI_CHUNG_TU"
    #                               ,
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN 'Số dư đầu kỳ'
    #                                     ELSE CASE WHEN
    #                                             (AOL."MA_TK_DOI_UNG" LIKE '133%%' OR AOL."MA_TK_DOI_UNG" LIKE '3331%%')
    #                                             THEN 'Thuế GTGT của hàng hóa, dịch vụ'
    #                                       ELSE AOL."DIEN_GIAI_CHUNG" END
    #                                   END AS "DIEN_GIAI_CHUNG"

    #                                 /*ntquang 26.03.2018 Thi công CR195226 - khi công gộp : Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

    #                               ,TBAN."SO_TAI_KHOAN"
    #                               , -- TK công nợ
    #                               TBAN."TINH_CHAT"
    #                               , -- Tính chất tài khoản
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN NULL
    #                                 ELSE AOL."MA_TK_DOI_UNG"
    #                                 END AS "MA_TAI_KHOAN_DOI_UNG"
    #                               ,

    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN 0
    #                                 ELSE AOL."GHI_NO_NGUYEN_TE"
    #                                 END AS "GHI_NO_NGUYEN_TE"
    #                               , -- Phát sinh nợ
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN 0
    #                                 ELSE AOL."GHI_NO"
    #                                 END AS "GHI_NO"
    #                               , -- Phát sinh nợ quy đổi
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN 0
    #                                 ELSE AOL."GHI_CO_NGUYEN_TE"
    #                                 END AS "GHI_CO_NGUYEN_TE"
    #                               , -- Phát sinh có
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN 0
    #                                 ELSE AOL."GHI_CO"
    #                                 END AS "GHI_CO"
    #                               , -- Phát sinh có quy đổi
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN AOL."GHI_NO_NGUYEN_TE"
    #                                 ELSE 0
    #                                 END AS "ClosingDebitAmountOC"
    #                               , --Dư Nợ
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN AOL."GHI_NO"
    #                                 ELSE 0
    #                                 END AS "ClosingDebitAmount"
    #                               , --Dư Nợ Quy đổi
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN AOL."GHI_CO_NGUYEN_TE"
    #                                 ELSE 0
    #                                 END AS "ClosingCreditAmountOC"
    #                               , --Dư Có
    #                                 CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
    #                                     THEN AOL."GHI_CO"
    #                                 ELSE 0
    #                                 END AS "ClosingCreditAmount"
    #                                --Dư Có quy đổi
                                   
    #                               ,AOL."MODEL_CHUNG_TU"
    #                           FROM so_cong_no_chi_tiet AS AOL
    #                               INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE  TBAN."AccountNumberPercent"
    #                               INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
    #                               INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
    #                               INNER JOIN (SELECT *
    #                                       FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
    #                                       ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
    #                               LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id -- Danh mục ĐVT
    #                               /*hoant 27.09.2017 theo cr 138363*/

    #                               WHERE AOL."NGAY_HACH_TOAN" <=den_ngay
    #                                       AND ( loai_tien_id = -1 OR AOL."currency_id" = loai_tien_id )
    #                                       AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
    #                                       AND AN."DOI_TUONG_SELECTION" = '0'
    #                               ) AS AD

    #                           GROUP BY
    #                             AD."DOI_TUONG_ID",
    #                             AD."MA",
    #                             AD."HO_VA_TEN",
    #                             AD."DIA_CHI",

    #                             AD."NGAY_HACH_TOAN", -- Ngày hạch toán
    #                             AD."NGAY_CHUNG_TU", -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                             AD."SO_CHUNG_TU", -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                             --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
    #                             AD."ID_CHUNG_TU",
    #                             AD."LOAI_CHUNG_TU", --Loại chứng từ
    #                             AD."DIEN_GIAI_CHUNG", -- Diễn giải (lấy diễn giải Master)
    #                             AD."SO_TAI_KHOAN", -- TK công nợ
    #                             AD."TINH_CHAT", -- Tính chất tài khoản
    #                             AD."MA_TAI_KHOAN_DOI_UNG", --TK đối ứng
    #                             --   TMP_KET_QUA."TY_GIA", --Tỷ giá
                                
    #                           AD."MODEL_CHUNG_TU"

    #                           ) AS RSS




    #                           WHERE   RSS."GHI_NO_NGUYEN_TE" <> 0
    #                                   OR RSS."GHI_NO" <> 0
    #                                   OR RSS."GHI_CO_NGUYEN_TE"<> 0
    #                                   OR RSS."GHI_CO" <> 0
    #                                   OR "ClosingDebitAmountOC" - "ClosingCreditAmountOC" <> 0
    #                                   OR "ClosingDebitAmount" - "ClosingCreditAmount" <> 0

    #                           GROUP BY
    #                                 RSS."DOI_TUONG_ID",
    #                                 RSS."MA",
    #                                 RSS."HO_VA_TEN",
    #                                 RSS."DIA_CHI",

    #                                 RSS."NGAY_HACH_TOAN", -- Ngày hạch toán
    #                                 RSS."NGAY_CHUNG_TU", -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                                 RSS."SO_CHUNG_TU", -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
    #                                 --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
    #                                 RSS."ID_CHUNG_TU",
    #                                 RSS."LOAI_CHUNG_TU", --Loại chứng từ
    #                                 RSS."DIEN_GIAI_CHUNG", -- Diễn giải (lấy diễn giải Master)
    #                                 RSS."SO_TAI_KHOAN", -- TK công nợ
    #                                 RSS."TINH_CHAT", -- Tính chất tài khoản
    #                                 RSS."MA_TAI_KHOAN_DOI_UNG", --TK đối ứng
    #                                 --   TMP_KET_QUA."TY_GIA", --Tỷ giá

    #                                 RSS."GHI_NO_NGUYEN_TE",
    #                                 RSS."GHI_NO",
    #                                 RSS."GHI_CO_NGUYEN_TE",
    #                                 RSS."GHI_CO",
    #                                 RSS."MODEL_CHUNG_TU"



    #                           ORDER BY
    #                               RSS."MA",
    #                               RSS."SO_TAI_KHOAN",

    #                               RSS."NGAY_HACH_TOAN",
    #                               RSS."NGAY_CHUNG_TU",
    #                               RSS."SO_CHUNG_TU"
    #                                   ;



    #                   END IF;


    #       END $$
    #       ;

    #       SELECT *FROM TMP_KET_QUA ;
    #       """
    #   cr.execute(query,params)
    #   # Get and show result
    #   for line in cr.dictfetchall():
    #       record.append({
    #           'THONG_KE_THEO': '',
    #           'CHI_NHANH_ID': '',
    #           'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC': '',
    #           'KY_BAO_CAO': '',
    #           'TAI_KHOAN_ID': '',
    #           'currency_id': '',
    #           'TU': '',
    #           'DEN': '',
    #           'NHOM_NCC_ID': '',
    #           'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
    #           'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
    #           'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
    #           'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
    #           'TK_CO_ID': line.get('SO_TAI_KHOAN', ''),
    #           'TK_DOI_TUONG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
    #           'NO_PHAT_SINH': line.get('GHI_NO_NGUYEN_TE', ''),
    #           'CO_PHAT_SINH': line.get('GHI_CO_NGUYEN_TE', ''),
    #           'NO_SO_DU': line.get('GHI_NO', ''),
    #           'CO_SO_DU': line.get('GHI_CO', ''),
    #           'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU': '',
    #           'CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU': '',
    #           'TEN_NHAN_VIEN': '',
    #           'TEN_NHA_CUNG_CAP': line.get('HO_VA_TEN', ''),
    #           'name': '',
    #           'ID_GOC': line.get('ID_CHUNG_TU', ''),
    #           'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
    #           })
    #   return record


#lấy báo cáo công trình
    def _lay_bao_cao_cong_trinh(self, params):      
      record = []
      cr = self.env.cr
      query = """

                        DO LANGUAGE plpgsql $$
            DECLARE

                chi_nhanh_id                        INTEGER :=%(CHI_NHANH_ID)s;
            
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                           DATE := %(DEN_NGAY)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
                so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;
            
               
            
                loai_tien_id                        VARCHAR(127) :=%(currency_id)s;
            
            
                CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU     INTEGER :=%(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;


                rec                                 RECORD;
                AccountNumberPercent                VARCHAR(100);

                 SO_TIEN_TON_NGUYEN_TE_TMP           FLOAT := 0;

                SO_TIEN_TON_TMP                     FLOAT := 0;

                MA_KHACH_HANG_TMP                   VARCHAR(100) := N'';

                MA_CONG_TRINH_TMP                     VARCHAR(100) := N'';

                SO_TAI_KHOAN_TMP                    VARCHAR(100) := N'';

            BEGIN

                DROP TABLE IF EXISTS DS_KHACH_HANG_NCC
                ;

                CREATE TEMP TABLE DS_KHACH_HANG_NCC
                    AS
                        SELECT
                            AO.id



                        FROM res_partner AS AO
                        WHERE (AO.id  = any( %(NHA_CUNG_CAP_IDS)s))
                ;

                DROP TABLE IF EXISTS DS_CONG_TRINH
                ;

                CREATE TEMP TABLE DS_CONG_TRINH
                    AS
                        SELECT
                            PW.id,
                            PW."MA_PHAN_CAP",
                            PW."MA_CONG_TRINH",
                            PW."TEN_CONG_TRINH",
                            PW."LOAI_CONG_TRINH"


                        FROM danh_muc_cong_trinh AS PW
                        WHERE (id = any( %(CONG_TRINH_IDS)s))
                ;

                DROP TABLE IF EXISTS DS_LOAI_CONG_TRINH
                ;

                CREATE TEMP TABLE DS_LOAI_CONG_TRINH
                    AS
                        SELECT
                            DISTINCT
                            PW.id,
                            PW."MA_PHAN_CAP",
                            PW."MA_CONG_TRINH",
                            PW."TEN_CONG_TRINH"


                        FROM DS_CONG_TRINH AS SPW
                        INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE concat(SPW."MA_PHAN_CAP",'%%')



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
                                , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                                , A."TINH_CHAT"
                            FROM danh_muc_he_thong_tai_khoan AS A
                            WHERE A."SO_TAI_KHOAN" = so_tai_khoan
                            ORDER BY A."SO_TAI_KHOAN",
                                A."TEN_TAI_KHOAN"
                    ;
                ELSE
                    CREATE TEMP TABLE TMP_TAI_KHOAN
                        AS
                            SELECT
                                A."SO_TAI_KHOAN"
                                , A."TEN_TAI_KHOAN"
                                , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                                , A."TINH_CHAT"
                            FROM danh_muc_he_thong_tai_khoan AS A
                            WHERE A."CHI_TIET_THEO_DOI_TUONG" = '1'
                                  AND "DOI_TUONG_SELECTION" = '0'
                                  AND "LA_TK_TONG_HOP" = '0'
                            --AND IsParent = 0
                            ORDER BY A."SO_TAI_KHOAN",
                                A."TEN_TAI_KHOAN"
                    ;
                END IF
                ;
            
            
                /*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
                ;
            
                CREATE TEMP SEQUENCE TMP_KET_QUA_seq
            
                ;
            
                CREATE TABLE TMP_KET_QUA
                (
                    RowNum                   INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
                        PRIMARY KEY,
                    "MA_CONG_TRINH"          VARCHAR(200)
                    ,
                    "TEN_CONG_TRINH"         VARCHAR(200)
                    ,
                    "DOI_TUONG_ID"           INT
                    ,
                    "MA_DOI_TUONG"           VARCHAR(200)
                    ,
                    "TEN_DOI_TUONG"          VARCHAR(200)
            
                    ,
                    "NGAY_HACH_TOAN"         TIMESTAMP
                    ,
                    "NGAY_CHUNG_TU"          TIMESTAMP
                    ,
                    "SO_CHUNG_TU"            VARCHAR(200)
                    ,
                    "ID_CHUNG_TU"            INT
            
                    ,
                    "LOAI_CHUNG_TU"          VARCHAR(200)
                    ,
                    "DIEN_GIAI_CHUNG"        VARCHAR(200)
                    ,
                    "SO_TAI_KHOAN"           VARCHAR(200)
                    ,
                    "TINH_CHAT"              VARCHAR(200)
                    ,
                    "MA_TAI_KHOAN_DOI_UNG"   VARCHAR(200)
                    ,
                    "GHI_NO_NGUYEN_TE"       FLOAT
                    ,
                    "GHI_NO"                 FLOAT
                    ,
                    "GHI_CO_NGUYEN_TE"       FLOAT
                    ,
                    "GHI_CO"                 FLOAT
                    , -- Phát sinh có quy đổi
                    "DU_NO_NGUYEN_TE"        FLOAT
                    , --Dư Nợ
                    "DU_NO"                  FLOAT
                    , --   --Dư Nợ Quy đổi
                    "DU_CO_NGUYEN_TE"        FLOAT
                    , --   --Dư Có
                    "DU_CO"                  FLOAT
            
                    ,
                    "MODEL_CHUNG_TU"         VARCHAR(200)
                    ,
                    "IsBold"                 BOOLEAN
                    ,
                    "OrderType"              INT
                    ,
                    "THU_TU_TRONG_CHUNG_TU"  INT
                    ,
                    "THU_TU_CHI_TIET_GHI_SO" INT
                )
                ;
            
            
                IF CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 0
                THEN
                    INSERT INTO TMP_KET_QUA
                    (
                        "MA_CONG_TRINH"
                        , "TEN_CONG_TRINH"
                        , "DOI_TUONG_ID"
                        , "MA_DOI_TUONG"
                        , "TEN_DOI_TUONG"
            
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , "SO_CHUNG_TU"
                        , "ID_CHUNG_TU"
            
                        , "LOAI_CHUNG_TU"
                        , "DIEN_GIAI_CHUNG"
                        , "SO_TAI_KHOAN"
                        , "TINH_CHAT"
                        , "MA_TAI_KHOAN_DOI_UNG"
                        , "GHI_NO_NGUYEN_TE"
                        , "GHI_NO"
                        , "GHI_CO_NGUYEN_TE"
                        , "GHI_CO"
                        , -- Phát sinh có quy đổi
                        "DU_NO_NGUYEN_TE"
                        , --Dư Nợ
                        "DU_NO"
                        , --   --Dư Nợ Quy đổi
                        "DU_CO_NGUYEN_TE"
                        , --   --Dư Có
                        "DU_CO"
                        --   --Dư Có quy đổi
                        , "MODEL_CHUNG_TU"
                        , "IsBold"
                        , "OrderType"
                        , "THU_TU_TRONG_CHUNG_TU"
                        , "THU_TU_CHI_TIET_GHI_SO"
            
                    )
            
            
                        SELECT
                            "MA_CONG_TRINH"
                            , "TEN_CONG_TRINH"
                            , "DOI_TUONG_ID"
                            , "MA_DOI_TUONG"
                            , "TEN_DOI_TUONG"
                            --, "DIA_CHI"
                            , "NGAY_HACH_TOAN"
                            , "NGAY_CHUNG_TU"
                            , "SO_CHUNG_TU"
                            , "ID_CHUNG_TU"
            
                            , "LOAI_CHUNG_TU"
                            , "DIEN_GIAI_CHUNG"
                            , "SO_TAI_KHOAN"
                            , "TINH_CHAT"
                            , "MA_TAI_KHOAN_DOI_UNG"
                            , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                            , SUM("GHI_NO")           AS "GHI_NO"
                            , SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                            , SUM("GHI_CO")           AS "GHI_CO"
                            , -- Phát sinh có quy đổi
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")) > 0
                                   THEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE"))
                                    ELSE 0
                                    END
                               END)                   AS "DU_NO_NGUYEN_TE"
                            , --Dư Nợ
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN (SUM("DU_NO") - SUM("DU_CO"))
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_NO") - SUM("DU_CO")) > 0
                                   THEN SUM("DU_NO") - SUM("DU_CO")
                                    ELSE 0
                                    END
                               END)                   AS "DU_NO"
                            , --   --Dư Nợ Quy đổi
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE")) > 0
                                   THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                                    ELSE 0
                                    END
                               END)                   AS "DU_CO_NGUYEN_TE"
                            , --   --Dư Có
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN (SUM("DU_CO") - SUM("DU_NO"))
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN (SUM("DU_CO") - SUM("DU_NO")) > 0
                                   THEN (SUM("DU_CO") - SUM("DU_NO"))
                                    ELSE 0
                                    END
                               END)                   AS "DU_CO"
            
                            , "MODEL_CHUNG_TU"
                            , "IsBold"
                            , "OrderType"
                            , "THU_TU_TRONG_CHUNG_TU"
                            , "THU_TU_CHI_TIET_GHI_SO"
            
                        FROM (
            
            
                                 SELECT
            
            
                                     PW."MA_CONG_TRINH"
                                     , PW."TEN_CONG_TRINH"
                                     , AOL."DOI_TUONG_ID"
                                     , AOL."MA_DOI_TUONG"
                                     , AOL."TEN_DOI_TUONG"
                                     --, AOL."DIA_CHI"
            
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."NGAY_HACH_TOAN"
                                       END AS "NGAY_HACH_TOAN"
                                     , -- Ngày hạch toán
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE "NGAY_CHUNG_TU"
                                       END AS "NGAY_CHUNG_TU"
                                     , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."SO_CHUNG_TU"
                                       END AS "SO_CHUNG_TU"
                                     , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."ID_CHUNG_TU"
                                       END AS "ID_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."LOAI_CHUNG_TU"
                                       END AS "LOAI_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN N'Số dư đầu kỳ'
            
                                       ELSE AOL."DIEN_GIAI"
                                       END AS "DIEN_GIAI_CHUNG"
            
                                     /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
            
                                     , TBAN."SO_TAI_KHOAN"
                                     , -- TK công nợ
                                     TBAN."TINH_CHAT"
                                     , -- Tính chất tài khoản
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."MA_TK_DOI_UNG"
                                       END AS "MA_TAI_KHOAN_DOI_UNG"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                                     , -- Phát sinh có quy đổi
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO_NGUYEN_TE"
                                       ELSE 0
                                       END AS "DU_NO_NGUYEN_TE"
                                     , --Dư Nợ
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO"
                                       ELSE 0
                                       END AS "DU_NO"
                                     , --Dư Nợ Quy đổi
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO_NGUYEN_TE"
                                       ELSE 0
                                       END AS "DU_CO_NGUYEN_TE"
                                     , --Dư Có
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO"
                                       ELSE 0
                                       END AS "DU_CO"
            
                                     , AOL."MODEL_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN TRUE
                                       ELSE FALSE
                                       END AS "IsBold"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN 0
                                       ELSE 1
                                       END AS "OrderType"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                                       END AS "THU_TU_TRONG_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                       END AS "THU_TU_CHI_TIET_GHI_SO"
            
                                 FROM so_cong_no_chi_tiet AS AOL
                                     INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                     INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                     INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                     INNER JOIN (SELECT *
                                                 FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                              bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                         ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
            
                                     INNER JOIN DS_LOAI_CONG_TRINH AS LPID ON AOL."CONG_TRINH_ID" = LPID.id
                                     INNER JOIN DS_CONG_TRINH PW ON LPID."MA_PHAN_CAP" LIKE concat(PW."MA_PHAN_CAP", '%%')
            
                                     LEFT JOIN danh_muc_loai_cong_trinh
                                         AS PWC ON PW."LOAI_CONG_TRINH" = PWC.id
                                     LEFT JOIN danh_muc_don_vi_tinh AS U ON AOL."DVT_ID" = U.id
                                     LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
            
            
                                 WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                       AND (loai_tien_id IS NULL OR (SELECT "MA_LOAI_TIEN"
                                                                     FROM res_currency T
                                                                     WHERE T.id = AOL."currency_id") = loai_tien_id)
                                       AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                       AND AN."DOI_TUONG_SELECTION" = '0'
                             ) AS RSNS
            
            
                        GROUP BY
            
                            RSNS."MA_CONG_TRINH"
                            , RSNS."TEN_CONG_TRINH"
                            , RSNS."DOI_TUONG_ID"
                            , RSNS."MA_DOI_TUONG"
                            , RSNS."TEN_DOI_TUONG"
            
                            , RSNS."NGAY_HACH_TOAN"
                            , RSNS."NGAY_CHUNG_TU"
                            , RSNS."SO_CHUNG_TU"
                            , RSNS."ID_CHUNG_TU"
                            , RSNS."LOAI_CHUNG_TU"
                            , RSNS."MA_TAI_KHOAN_DOI_UNG"
                            , RSNS."DIEN_GIAI_CHUNG"
                            , RSNS."SO_TAI_KHOAN"
            
                            , RSNS."TINH_CHAT"
                            , RSNS."MODEL_CHUNG_TU"
                            , RSNS."IsBold"
                            , RSNS."OrderType"
                            , RSNS."THU_TU_TRONG_CHUNG_TU"
                            , RSNS."THU_TU_CHI_TIET_GHI_SO"
            
            
                        HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                               OR SUM("GHI_NO") <> 0
                               OR SUM("GHI_CO_NGUYEN_TE") <> 0
                               OR SUM("GHI_CO") <> 0
                               OR SUM("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <> 0
                               OR SUM("DU_NO" - "DU_CO") <> 0
            
                        ORDER BY
                            RSNS."TEN_CONG_TRINH",
                            RSNS."TEN_DOI_TUONG",
                            RSNS."MA_CONG_TRINH",
                            RSNS."SO_TAI_KHOAN",
                            RSNS."OrderType",
                            RSNS."NGAY_HACH_TOAN",
                            RSNS."NGAY_CHUNG_TU",
                            RSNS."SO_CHUNG_TU",
                            RSNS."THU_TU_TRONG_CHUNG_TU",
                            RSNS."THU_TU_CHI_TIET_GHI_SO"
            
                    ;
                ELSE
                    INSERT INTO TMP_KET_QUA
                    (
                        "MA_CONG_TRINH"
                        , "TEN_CONG_TRINH"
                        , "DOI_TUONG_ID"
                        , "MA_DOI_TUONG"
                        , "TEN_DOI_TUONG"
            
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , "SO_CHUNG_TU"
                        , "ID_CHUNG_TU"
            
                        , "LOAI_CHUNG_TU"
                        , "DIEN_GIAI_CHUNG"
                        , "SO_TAI_KHOAN"
                        , "TINH_CHAT"
                        , "MA_TAI_KHOAN_DOI_UNG"
                        , "GHI_NO_NGUYEN_TE"
                        , "GHI_NO"
                        , "GHI_CO_NGUYEN_TE"
                        , "GHI_CO"
                        , -- Phát sinh có quy đổi
                        "DU_NO_NGUYEN_TE"
                        , --Dư Nợ
                        "DU_NO"
                        , --   --Dư Nợ Quy đổi
                        "DU_CO_NGUYEN_TE"
                        , --   --Dư Có
                        "DU_CO"
                        --   --Dư Có quy đổi
                        , "MODEL_CHUNG_TU"
                        , "IsBold"
                        , "OrderType"
                        , "THU_TU_TRONG_CHUNG_TU"
                        , "THU_TU_CHI_TIET_GHI_SO"
            
                    )
            
                        SELECT
                            "MA_CONG_TRINH"
                            , "TEN_CONG_TRINH"
                            , "DOI_TUONG_ID"
                            , "MA_DOI_TUONG"
                            , "TEN_DOI_TUONG"
            
                            , "NGAY_HACH_TOAN"
                            , "NGAY_CHUNG_TU"
                            , "SO_CHUNG_TU"
                            , "ID_CHUNG_TU"
            
                            , "LOAI_CHUNG_TU"
                            , "DIEN_GIAI_CHUNG"
                            , "SO_TAI_KHOAN"
                            , "TINH_CHAT"
                            , "MA_TAI_KHOAN_DOI_UNG"
                            , ("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                            , ("GHI_NO")           AS "GHI_NO"
                            , ("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                            , ("GHI_CO")           AS "GHI_CO"
                            , -- Phát sinh có quy đổi
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE") > 0
                                   THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                                    ELSE 0
                                    END
                               END)                AS "DU_NO_NGUYEN_TE"
                            , --Dư Nợ
                              (CASE WHEN "TINH_CHAT" = '0'
                                  THEN ("DU_NO") - ("DU_CO")
                               WHEN "TINH_CHAT" = '1'
                                   THEN 0
                               ELSE CASE WHEN ("DU_NO") - ("DU_CO") > 0
                                   THEN ("DU_NO") - ("DU_CO")
                                    ELSE 0
                                    END
                               END)                AS "DU_NO"
                            , --   --Dư Nợ Quy đổi
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE") > 0
                                   THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                                    ELSE 0
                                    END
                               END)                AS "DU_CO_NGUYEN_TE"
                            , --   --Dư Có
                              (CASE WHEN "TINH_CHAT" = '1'
                                  THEN ("DU_CO") - ("DU_NO")
                               WHEN "TINH_CHAT" = '0'
                                   THEN 0
                               ELSE CASE WHEN ("DU_CO") - ("DU_NO") > 0
                                   THEN ("DU_CO") - ("DU_NO")
                                    ELSE 0
                                    END
                               END)                AS "DU_CO"
                            --   --Dư Có quy đổi
                            , "MODEL_CHUNG_TU"
                            , "IsBold"
                            , "OrderType"
                            , 0                    AS "THU_TU_TRONG_CHUNG_TU"
                            , "THU_TU_CHI_TIET_GHI_SO"
            
            
                        FROM (
                                 SELECT
            
                                     PW."MA_CONG_TRINH"
                                     , PW."TEN_CONG_TRINH"
            
                                     , AOL."DOI_TUONG_ID"
                                     , AOL."MA_DOI_TUONG"
                                     , AOL."TEN_DOI_TUONG"
                                     --, AOL."DIA_CHI"
            
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."NGAY_HACH_TOAN"
                                       END      AS "NGAY_HACH_TOAN"
                                     , -- Ngày hạch toán
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE "NGAY_CHUNG_TU"
                                       END      AS "NGAY_CHUNG_TU"
                                     , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."SO_CHUNG_TU"
                                       END      AS "SO_CHUNG_TU"
                                     , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."ID_CHUNG_TU"
                                       END      AS "ID_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."LOAI_CHUNG_TU"
                                       END      AS "LOAI_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN N'Số dư đầu kỳ'
            
                                       ELSE AOL."DIEN_GIAI_CHUNG"
                                       END      AS "DIEN_GIAI_CHUNG"
            
                                     /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
            
                                     , TBAN."SO_TAI_KHOAN"
                                     , -- TK công nợ
                                     TBAN."TINH_CHAT"
                                     , -- Tính chất tài khoản
                                       CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN NULL
                                       ELSE AOL."MA_TK_DOI_UNG"
                                       END      AS "MA_TAI_KHOAN_DOI_UNG"
                                     , SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN 0
                                           ELSE AOL."GHI_NO_NGUYEN_TE"
                                           END) AS "GHI_NO_NGUYEN_TE"
                                     , -- Phát sinh nợ
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                           ELSE AOL."GHI_NO"
                                           END) AS "GHI_NO"
                                     , -- Phát sinh nợ quy đổi
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                           ELSE AOL."GHI_CO_NGUYEN_TE"
                                           END) AS "GHI_CO_NGUYEN_TE"
                                     , -- Phát sinh có
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 0
                                           ELSE AOL."GHI_CO"
                                           END) AS "GHI_CO"
                                     , -- Phát sinh có quy đổi
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO_NGUYEN_TE"
                                           ELSE 0
                                           END) AS "DU_NO_NGUYEN_TE"
                                     , --Dư Nợ
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_NO"
                                           ELSE 0
                                           END) AS "DU_NO"
                                     , --Dư Nợ Quy đổi
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO_NGUYEN_TE"
                                           ELSE 0
                                           END) AS "DU_CO_NGUYEN_TE"
                                     , --Dư Có
                                       SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN AOL."GHI_CO"
                                           ELSE 0
                                           END) AS "DU_CO"
            
                                     , AOL."MODEL_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN TRUE
                                       ELSE FALSE
                                       END      AS "IsBold"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN 0
                                       ELSE 1
                                       END      AS "OrderType"
            
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                       END      AS "THU_TU_CHI_TIET_GHI_SO"
            
            
                                 FROM so_cong_no_chi_tiet AS AOL
                                     INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                     INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                     INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                     INNER JOIN (SELECT *
                                                 FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                              bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                         ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
            
                                     INNER JOIN DS_LOAI_CONG_TRINH AS LPID ON AOL."CONG_TRINH_ID" = LPID.id
                                     INNER JOIN DS_CONG_TRINH PW ON LPID."MA_PHAN_CAP" LIKE concat(PW."MA_PHAN_CAP", '%%')
            
                                     LEFT JOIN danh_muc_loai_cong_trinh
                                         AS PWC ON PW."LOAI_CONG_TRINH" = PWC.id
            
                                     LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
            
                                 WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                       AND (loai_tien_id IS NULL OR (SELECT "MA_LOAI_TIEN"
                                                                     FROM res_currency T
                                                                     WHERE T.id = AOL."currency_id") = loai_tien_id)
                                       AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                       AND AN."DOI_TUONG_SELECTION" = '0'
            
                                 GROUP BY
            
            
                                     PW."MA_CONG_TRINH"
                                     , PW."TEN_CONG_TRINH"
                                     , AOL."DOI_TUONG_ID"
                                     , AOL."MA_DOI_TUONG"
                                     , AOL."TEN_DOI_TUONG"
            
            
                                     ,
                                     AOL."NGAY_HACH_TOAN"
            
                                     , -- Ngày hạch toán
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE "NGAY_CHUNG_TU"
                                     END
                                     , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."SO_CHUNG_TU"
                                     END
                                     , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."ID_CHUNG_TU"
                                     END
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN NULL
                                       ELSE AOL."LOAI_CHUNG_TU"
                                       END
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN N'Số dư đầu kỳ'
            
                                       ELSE AOL."DIEN_GIAI_CHUNG"
                                       END
            
                                     /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
            
                                     , TBAN."SO_TAI_KHOAN"
                                     , -- TK công nợ
                                     TBAN."TINH_CHAT"
                                     , -- Tính chất tài khoản
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."MA_TK_DOI_UNG"
                                     END
            
                                     , AOL."MODEL_CHUNG_TU"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN TRUE
                                       ELSE FALSE
                                       END
                                     ,
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN 0
                                     ELSE 1
                                     END
            
                                     ,
                                     CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                     ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                     END
            
                             ) AS RSS
                        WHERE RSS."GHI_NO_NGUYEN_TE" <> 0
                              OR RSS."GHI_NO" <> 0
                              OR RSS."GHI_CO_NGUYEN_TE" <> 0
                              OR RSS."GHI_CO" <> 0
                              OR "DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE" <> 0
                              OR "DU_CO" - "DU_NO" <> 0
            
                        ORDER BY
                            RSS."TEN_CONG_TRINH",
                            RSS."TEN_DOI_TUONG",
                            RSS."MA_CONG_TRINH",
                            RSS."SO_TAI_KHOAN",
                            RSS."OrderType",
                            RSS."NGAY_HACH_TOAN",
                            RSS."NGAY_CHUNG_TU",
                            RSS."SO_CHUNG_TU",
                            RSS."THU_TU_CHI_TIET_GHI_SO"
                    ;
                END IF
                ;
            
                FOR rec IN
                SELECT *
                FROM TMP_KET_QUA
                WHERE "OrderType" <> 2
            
                ORDER BY
                    RowNum
                LOOP
                    SELECT (CASE WHEN rec."OrderType" = 0
                        THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0 --DU_NO_NGUYEN_TE
                            THEN rec."DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                              ELSE -1
                                   * rec."DU_NO_NGUYEN_TE" --DU_NO_NGUYEN_TE
                              END)
                            WHEN
            
                                MA_CONG_TRINH_TMP <> rec."MA_CONG_TRINH"
            
                                OR MA_KHACH_HANG_TMP <> rec."MA_DOI_TUONG"
                                OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
            
                                THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                            ELSE SO_TIEN_TON_NGUYEN_TE_TMP + rec."GHI_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                                 - rec."GHI_NO_NGUYEN_TE" --GHI_NO_NGUYEN_TE
                            END)
                    INTO SO_TIEN_TON_NGUYEN_TE_TMP
            
                ;
            
                    rec."DU_NO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
                        THEN -1 * SO_TIEN_TON_NGUYEN_TE_TMP
                                             WHEN rec."TINH_CHAT" = '1'
                                                 THEN 0
                                             ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
                                                 THEN -1
                                                      * SO_TIEN_TON_NGUYEN_TE_TMP
                                                  ELSE 0
                                                  END
                                             END)
                ;
            
                    UPDATE TMP_KET_QUA
                    SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
                    WHERE RowNum = rec.RowNum
                ;
            
                    rec."DU_CO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
                        THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                             WHEN rec."TINH_CHAT" = '0'
                                                 THEN 0
                                             ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
                                                 THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                                  ELSE 0
                                                  END
                                             END)
                ;
            
                    UPDATE TMP_KET_QUA
                    SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
                    WHERE RowNum = rec.RowNum
                ;
            
                    SELECT (CASE WHEN rec."OrderType" = 0
                        THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                            THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                              ELSE -1
                                   * rec."DU_NO" --DU_NO_NGUYEN_TE
                              END)
                            WHEN
            
            
                                MA_CONG_TRINH_TMP <> rec."MA_CONG_TRINH"
            
                                OR MA_KHACH_HANG_TMP <> rec."MA_DOI_TUONG"
                                OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                                THEN rec."GHI_CO" - rec."GHI_NO" --PHAT_SINH_CO_NGUYEN_TE
                            ELSE SO_TIEN_TON_TMP + rec."GHI_CO"--PHAT_SINH_CO_NGUYEN_TE
                                 - rec."GHI_NO" --GHI_NO_NGUYEN_TE
                            END)
                    INTO SO_TIEN_TON_TMP
                ;
            
                    rec."DU_NO" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
                        THEN -1 * SO_TIEN_TON_TMP
                                   WHEN rec."TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN SO_TIEN_TON_TMP < 0
                                       THEN -1
                                            * SO_TIEN_TON_TMP
                                        ELSE 0
                                        END
                                   END)
                ;
            
                    UPDATE TMP_KET_QUA
                    SET "DU_NO" = rec."DU_NO"
                    WHERE RowNum = rec.RowNum
                ;
            
            
                    rec."DU_CO" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
                        THEN SO_TIEN_TON_TMP
                                   WHEN rec."TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN SO_TIEN_TON_TMP > 0
                                       THEN SO_TIEN_TON_TMP
                                        ELSE 0
                                        END
                                   END)
                ;
            
                    UPDATE TMP_KET_QUA
                    SET "DU_CO" = rec."DU_CO"
                    WHERE RowNum = rec.RowNum
                ;
            
            
                    MA_CONG_TRINH_TMP = rec."MA_CONG_TRINH"
                ;
            
            
            
                    MA_KHACH_HANG_TMP = rec."MA_DOI_TUONG"
                ;
            
                    SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
                ;
            
            
                END LOOP
                ;
            
            
            END $$
            ;
            
           SELECT *
          FROM TMP_KET_QUA
          OFFSET %(offset)s
          LIMIT %(limit)s
          ;



 """

      cr.execute(query,params)
              # Get and show result
      for line in cr.dictfetchall():
          record.append({
              
              'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
              'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
              'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
              'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
              'TK_CO_ID': line.get('SO_TAI_KHOAN', ''),
              'TK_DOI_TUONG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
              'NO_PHAT_SINH': line.get('GHI_NO', ''),
              'CO_PHAT_SINH': line.get('GHI_CO', ''),
              'NO_SO_DU': line.get('DU_NO', ''),
              'CO_SO_DU': line.get('DU_CO', ''),
              'TEN_CONG_TRINH': line.get('TEN_CONG_TRINH', ''),
              
              'TEN_NHA_CUNG_CAP': line.get('TEN_DOI_TUONG', ''),
              'name': '',
              'ID_GOC': line.get('ID_CHUNG_TU', ''),
              'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
              })
      return record
    


    # lấy báo cáo đơn mua hàng

    def _lay_bao_cao_don_mua_hang(self, params):      
      record = []
      cr = self.env.cr
      query = """

            DO LANGUAGE plpgsql $$
            DECLARE

                chi_nhanh_id                        INTEGER :=%(CHI_NHANH_ID)s;
            
                tu_ngay                             DATE := %(TU_NGAY)s;
            
                den_ngay                           DATE := %(DEN_NGAY)s;
            
                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
            
                 so_tai_khoan                          VARCHAR(127) := %(TAI_KHOAN_ID)s;
                                     
               loai_tien_id                           VARCHAR(127) :=%(currency_id)s;
                        
                CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU     INTEGER :=%(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;
            
                rec                                 RECORD;

                AccountNumberPercent                VARCHAR(100);
                   SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT := 0;

                SO_TIEN_TON_TMP                       FLOAT := 0;

                MA_KHACH_HANG_TMP                     VARCHAR(100) := N'';

                SO_TAI_KHOAN_TMP                      VARCHAR(100) := N'';
                 DON_MUA_HANG_ID_TMP    INTEGER ;

            BEGIN

                DROP TABLE IF EXISTS DS_KHACH_HANG_NCC
                ;

                CREATE TEMP TABLE DS_KHACH_HANG_NCC
                    AS
                        SELECT
                            AO.id
                            , AO."MA"
                            , AO."HO_VA_TEN"
                            , AO."DIA_CHI"

                            , AO."MA_SO_THUE"

                        FROM res_partner AS AO
                        WHERE (AO.id  = any( %(NHA_CUNG_CAP_IDS)s))
                ;

                DROP TABLE IF EXISTS DS_DON_MUA_HANG
                ;

                CREATE TEMP TABLE DS_DON_MUA_HANG
                    AS
                        SELECT
                            id AS "DON_MUA_HANG_ID"
                            , "SO_DON_HANG"
                            , "NGAY_DON_HANG"
                            , "TINH_TRANG"
                        FROM purchase_ex_don_mua_hang
                        WHERE (id = any( %(DON_MUA_HANG_IDS)s))
                ;


                DROP TABLE IF EXISTS TMP_TAI_KHOAN
                ;

                IF so_tai_khoan IS NOT NULL
                THEN
                    CREATE TEMP TABLE TMP_TAI_KHOAN
                        AS
                            SELECT
                                so_tai_khoan
                                , A."SO_TAI_KHOAN"
                                , A."TEN_TAI_KHOAN"
                                , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
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
                                , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                                , A."TINH_CHAT"
                            FROM danh_muc_he_thong_tai_khoan AS A
                            WHERE A."CHI_TIET_THEO_DOI_TUONG" = '1'
                                  AND "DOI_TUONG_SELECTION" = '0'
                                  AND "LA_TK_TONG_HOP" = '0'
                            --AND IsParent = 0
                            ORDER BY A."SO_TAI_KHOAN",
                                A."TEN_TAI_KHOAN"
                    ;
                END IF
                ;


                /*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/

                DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq

    ;

    CREATE TABLE TMP_KET_QUA
    (
        RowNum                 INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,

                                "SO_DON_HANG"   VARCHAR(200)
                                , "NGAY_DON_HANG"  TIMESTAMP

                                , "DOI_TUONG_ID"  INT
                                , "MA"   VARCHAR(200)
                                , "HO_VA_TEN"   VARCHAR(200)
                                --, "DIA_CHI"
                                ,"NGAY_HACH_TOAN"  TIMESTAMP
                                , "NGAY_CHUNG_TU"  TIMESTAMP
                                , "SO_CHUNG_TU"   VARCHAR(200)
                                ,"ID_CHUNG_TU"   INT

                                , "LOAI_CHUNG_TU"  VARCHAR(200)
                                , "DIEN_GIAI_CHUNG"  VARCHAR(200)
                                , "SO_TAI_KHOAN"  VARCHAR(200)
                                , "TINH_CHAT"   VARCHAR(200)
                                , "MA_TAI_KHOAN_DOI_UNG"   VARCHAR(200)
                                , "GHI_NO_NGUYEN_TE"  FLOAT
                                , "GHI_NO"  FLOAT
                                , "GHI_CO_NGUYEN_TE" FLOAT
                                , "GHI_CO"  FLOAT
                                , -- Phát sinh có quy đổi
                                  "DU_NO_NGUYEN_TE"  FLOAT
                                , --Dư Nợ
                                  "DU_NO"  FLOAT
                                , --   --Dư Nợ Quy đổi
                                  "DU_CO_NGUYEN_TE"  FLOAT
                                , --   --Dư Có
                                  "DU_CO"  FLOAT

                                , "MODEL_CHUNG_TU"   VARCHAR(200)

                                ,"OrderType"            INT
                                ,"DON_MUA_HANG_ID" INT
    )
    ;

                IF CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 0
                THEN
                    INSERT INTO TMP_KET_QUA
                   (

                      "SO_DON_HANG"
                                , "NGAY_DON_HANG"

                                , "DOI_TUONG_ID"
                                , "MA"
                                , "HO_VA_TEN"
                                --, "DIA_CHI"
                                ,"NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                ,"ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                , "GHI_NO_NGUYEN_TE"
                                , "GHI_NO"
                                , "GHI_CO_NGUYEN_TE"
                                , "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  "DU_CO"

                                , "MODEL_CHUNG_TU"
                                 ,
                                "OrderType"
                                ,"DON_MUA_HANG_ID"

                    )

                            SELECT
                                "SO_DON_HANG"
                                , "NGAY_DON_HANG"

                                , "DOI_TUONG_ID"
                                , "MA"
                                , "HO_VA_TEN"
                                --, "DIA_CHI"
                                , RSNS."NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , RSNS."ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                                , SUM("GHI_NO")           AS "GHI_NO"
                                , SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                                , SUM("GHI_CO")           AS "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  (CASE WHEN "TINH_CHAT" = '0'
                                      THEN SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")
                                   WHEN "TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")) > 0
                                       THEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE"))
                                        ELSE 0
                                        END
                                   END)                   AS "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  (CASE WHEN "TINH_CHAT" = '0'
                                      THEN (SUM("DU_NO") - SUM("DU_CO"))
                                   WHEN "TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_NO") - SUM("DU_CO")) > 0
                                       THEN SUM("DU_NO") - SUM("DU_CO")
                                        ELSE 0
                                        END
                                   END)                   AS "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  (CASE WHEN "TINH_CHAT" = '1'
                                      THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                                   WHEN "TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE")) > 0
                                       THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                                        ELSE 0
                                        END
                                   END)                   AS "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  (CASE WHEN "TINH_CHAT" = '1'
                                      THEN (SUM("DU_CO") - SUM("DU_NO"))
                                   WHEN "TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN (SUM("DU_CO") - SUM("DU_NO")) > 0
                                       THEN (SUM("DU_CO") - SUM("DU_NO"))
                                        ELSE 0
                                        END
                                   END)                   AS "DU_CO"
                                --   --Dư Có quy đổi
                                , "MODEL_CHUNG_TU"

                                   ,
                                "OrderType"
                            ,"DON_MUA_HANG_ID"
                            FROM (


                                     SELECT
                                         PU."SO_DON_HANG"
                                         , PU."NGAY_DON_HANG"
                                         , AOL."DOI_TUONG_ID"
                                         , LAOI."MA"
                                         , LAOI."HO_VA_TEN"
                                         --, AOL."DIA_CHI"

                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."NGAY_HACH_TOAN"
                                           END AS "NGAY_HACH_TOAN"
                                         , -- Ngày hạch toán
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE "NGAY_CHUNG_TU"
                                           END AS "NGAY_CHUNG_TU"
                                         , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."SO_CHUNG_TU"
                                           END AS "SO_CHUNG_TU"
                                         , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."ID_CHUNG_TU"
                                           END AS "ID_CHUNG_TU"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN NULL
                                           ELSE AOL."LOAI_CHUNG_TU"
                                           END AS "LOAI_CHUNG_TU"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                         THEN N'Số dư đầu kỳ'

                                           ELSE COALESCE(AOL."DIEN_GIAI", AOL."DIEN_GIAI_CHUNG")
                                           END AS "DIEN_GIAI_CHUNG"

                                         /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                                         , TBAN."SO_TAI_KHOAN"
                                         , -- TK công nợ
                                         TBAN."TINH_CHAT"
                                         , -- Tính chất tài khoản
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN NULL
                                           ELSE AOL."MA_TK_DOI_UNG"
                                           END AS "MA_TAI_KHOAN_DOI_UNG"
                                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                                         , -- Phát sinh có quy đổi
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_NO_NGUYEN_TE"
                                           ELSE 0
                                           END AS "DU_NO_NGUYEN_TE"
                                         , --Dư Nợ
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_NO"
                                           ELSE 0
                                           END AS "DU_NO"
                                         , --Dư Nợ Quy đổi
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_CO_NGUYEN_TE"
                                           ELSE 0
                                           END AS "DU_CO_NGUYEN_TE"
                                         , --Dư Có
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN AOL."GHI_CO"
                                           ELSE 0
                                           END AS "DU_CO"

                                         , AOL."MODEL_CHUNG_TU"
                                        ,
                                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                               THEN 0
                                           ELSE 1
                                           END AS "OrderType"

                                        , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN 2

                                       ELSE 0
                                       END AS "GroupOrder"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN ''

                                       ELSE ''
                                       END AS "AccountNoToOrder"
                                     , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                     THEN 2

                                       ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                                       END AS "THU_TU_TRONG_CHUNG_TU"
                                     , CASE
                                       WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                           THEN 2

                                       ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                       END AS "THU_TU_CHI_TIET_GHI_SO"
                                     ,PU."DON_MUA_HANG_ID"
                                     FROM so_cong_no_chi_tiet AS AOL
                                         INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                         INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                         INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                         INNER JOIN (SELECT *
                                                     FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                                  bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                             ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"

                                         INNER JOIN DS_DON_MUA_HANG AS PU ON PU."DON_MUA_HANG_ID" = AOL."DON_MUA_HANG_ID"


                                     WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                           AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                           AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                           AND AN."DOI_TUONG_SELECTION" = '0'
                                 ) AS RSNS

                            GROUP BY

                                RSNS."SO_DON_HANG"
                                , RSNS."NGAY_DON_HANG"
                                , RSNS."DOI_TUONG_ID"
                                , RSNS."MA"
                                , RSNS."HO_VA_TEN"

                                , RSNS."NGAY_HACH_TOAN"
                                , RSNS."NGAY_CHUNG_TU"
                                , RSNS."SO_CHUNG_TU"
                                , RSNS."ID_CHUNG_TU"
                                , RSNS."LOAI_CHUNG_TU"
                                , RSNS."MA_TAI_KHOAN_DOI_UNG"
                                , RSNS."DIEN_GIAI_CHUNG"
                                , RSNS."SO_TAI_KHOAN"

                                , RSNS."TINH_CHAT"
                                , RSNS."GHI_NO_NGUYEN_TE"
                                , RSNS."GHI_NO"
                                , RSNS."GHI_CO_NGUYEN_TE"
                                , RSNS."GHI_CO"

                                , RSNS."MODEL_CHUNG_TU"
                                , RSNS."OrderType"

                                , RSNS."GroupOrder"
                                , RSNS."AccountNoToOrder"
                                , RSNS."THU_TU_TRONG_CHUNG_TU"
                                , RSNS."THU_TU_CHI_TIET_GHI_SO"
                                 , RSNS."DON_MUA_HANG_ID"


                            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                                   OR SUM("GHI_NO") <> 0
                                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                                   OR SUM("GHI_CO") <> 0
                                   OR SUM("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <> 0
                                   OR SUM("DU_NO" - "DU_CO") <> 0

                            ORDER BY
                                 RSNS."NGAY_DON_HANG",
                                RSNS."SO_DON_HANG",
                                RSNS."MA",

                                 RSNS."SO_TAI_KHOAN",
                                RSNS."OrderType",
                                RSNS."NGAY_HACH_TOAN",
                                RSNS."NGAY_CHUNG_TU",
                                RSNS."SO_CHUNG_TU",
                                RSNS."GroupOrder",
                                RSNS."AccountNoToOrder",
                                RSNS."THU_TU_TRONG_CHUNG_TU",
                                RSNS."THU_TU_CHI_TIET_GHI_SO"


                    ;
                ELSE
                     INSERT INTO TMP_KET_QUA
                   (

                      "SO_DON_HANG"
                                , "NGAY_DON_HANG"

                                , "DOI_TUONG_ID"
                                , "MA"
                                , "HO_VA_TEN"

                                ,"NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                ,"ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                , "GHI_NO_NGUYEN_TE"
                                , "GHI_NO"
                                , "GHI_CO_NGUYEN_TE"
                                , "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  "DU_CO"

                                , "MODEL_CHUNG_TU"
                                 ,
                                "OrderType"
                                 ,"DON_MUA_HANG_ID"

                    )


                            SELECT
                                "SO_DON_HANG"
                                , "NGAY_DON_HANG"
                                , "DOI_TUONG_ID"
                                , "MA"
                                , "HO_VA_TEN"
                                --, "DIA_CHI"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "ID_CHUNG_TU"

                                , "LOAI_CHUNG_TU"
                                , "DIEN_GIAI_CHUNG"
                                , "SO_TAI_KHOAN"
                                , "TINH_CHAT"
                                , "MA_TAI_KHOAN_DOI_UNG"
                                , ("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                                , ("GHI_NO")           AS "GHI_NO"
                                , ("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                                , ("GHI_CO")           AS "GHI_CO"
                                , -- Phát sinh có quy đổi
                                  (CASE WHEN "TINH_CHAT" = '0'
                                      THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                                   WHEN "TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE") > 0
                                       THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                                        ELSE 0
                                        END
                                   END)                AS "DU_NO_NGUYEN_TE"
                                , --Dư Nợ
                                  (CASE WHEN "TINH_CHAT" = '0'
                                      THEN ("DU_NO") - ("DU_CO")
                                   WHEN "TINH_CHAT" = '1'
                                       THEN 0
                                   ELSE CASE WHEN ("DU_NO") - ("DU_CO") > 0
                                       THEN ("DU_NO") - ("DU_CO")
                                        ELSE 0
                                        END
                                   END)                AS "DU_NO"
                                , --   --Dư Nợ Quy đổi
                                  (CASE WHEN "TINH_CHAT" = '1'
                                      THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                                   WHEN "TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE") > 0
                                       THEN ("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")
                                        ELSE 0
                                        END
                                   END)                AS "DU_CO_NGUYEN_TE"
                                , --   --Dư Có
                                  (CASE WHEN "TINH_CHAT" = '1'
                                      THEN ("DU_CO") - ("DU_NO")
                                   WHEN "TINH_CHAT" = '0'
                                       THEN 0
                                   ELSE CASE WHEN ("DU_CO") - ("DU_NO") > 0
                                       THEN ("DU_CO") - ("DU_NO")
                                        ELSE 0
                                        END
                                   END)                AS "DU_CO"
                                --   --Dư Có quy đổi
                                , "MODEL_CHUNG_TU"
                                  ,
                                "OrderType"
                                     ,"DON_MUA_HANG_ID"


                            FROM (
                                     SELECT
                                         AD."SO_DON_HANG"
                                         , AD."NGAY_DON_HANG"
                                         , AD."DOI_TUONG_ID"
                                         , AD."MA"
                                         , AD."HO_VA_TEN"

                                         , AD."NGAY_HACH_TOAN"
                                         , AD."NGAY_CHUNG_TU"
                                         , AD."SO_CHUNG_TU"
                                         , AD."ID_CHUNG_TU"
                                         , AD."LOAI_CHUNG_TU"
                                         , AD."DIEN_GIAI_CHUNG"
                                         , AD."SO_TAI_KHOAN"
                                         , AD."TINH_CHAT"
                                         , AD."MA_TAI_KHOAN_DOI_UNG"
                                         , SUM(AD."GHI_NO_NGUYEN_TE")      AS "GHI_NO_NGUYEN_TE"
                                         , SUM(AD."GHI_NO")                AS "GHI_NO"
                                         , SUM(AD."GHI_CO_NGUYEN_TE")      AS "GHI_CO_NGUYEN_TE"
                                         , SUM(AD."GHI_CO")                AS "GHI_CO"

                                         , SUM(AD."DU_NO_NGUYEN_TE")  AS "DU_NO_NGUYEN_TE"
                                         , SUM(AD."DU_NO")    AS "DU_NO"
                                         , SUM(AD."DU_CO_NGUYEN_TE") AS "DU_CO_NGUYEN_TE"
                                         , SUM(AD."DU_CO")   AS "DU_CO"
                                         , AD."MODEL_CHUNG_TU"
                                         , AD."OrderType"
                                         , AD."THU_TU_CHI_TIET_GHI_SO"
                                         , AD."DON_MUA_HANG_ID"

                                     FROM (


                                              SELECT
                                                  PU."SO_DON_HANG"
                                                  , PU."NGAY_DON_HANG"
                                                  , AOL."DOI_TUONG_ID"
                                                  , LAOI."MA"
                                                  , LAOI."HO_VA_TEN"


                                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                  THEN NULL
                                                    ELSE AOL."NGAY_HACH_TOAN"
                                                    END AS "NGAY_HACH_TOAN"
                                                  , -- Ngày hạch toán
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN NULL
                                                    ELSE "NGAY_CHUNG_TU"
                                                    END AS "NGAY_CHUNG_TU"
                                                  ,
                                                  -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN NULL
                                                    ELSE AOL."SO_CHUNG_TU"
                                                    END AS "SO_CHUNG_TU"
                                                  , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN NULL
                                                    ELSE AOL."ID_CHUNG_TU"
                                                    END AS "ID_CHUNG_TU"
                                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                  THEN NULL
                                                    ELSE AOL."LOAI_CHUNG_TU"
                                                    END AS "LOAI_CHUNG_TU"
                                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                  THEN N'Số dư đầu kỳ'
                                                    ELSE AOL."DIEN_GIAI_CHUNG"


                                                    END AS "DIEN_GIAI_CHUNG"

                                                  /*ntquang 26.03.2018 Thi công CR195226 - khi công gộp : Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                                                  , TBAN."SO_TAI_KHOAN"
                                                  , -- TK công nợ
                                                  TBAN."TINH_CHAT"
                                                  , -- Tính chất tài khoản
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN NULL
                                                    ELSE AOL."MA_TK_DOI_UNG"
                                                    END AS "MA_TAI_KHOAN_DOI_UNG"
                                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                                                  , -- Phát sinh có quy đổi
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN AOL."GHI_NO_NGUYEN_TE"
                                                    ELSE 0
                                                    END AS "DU_NO_NGUYEN_TE"
                                                  , --Dư Nợ
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN AOL."GHI_NO"
                                                    ELSE 0
                                                    END AS "DU_NO"
                                                  , --Dư Nợ Quy đổi
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN AOL."GHI_CO_NGUYEN_TE"
                                                    ELSE 0
                                                    END AS "DU_CO_NGUYEN_TE"
                                                  , --Dư Có
                                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                                        THEN AOL."GHI_CO"
                                                    ELSE 0
                                                    END AS "DU_CO"
                                                  --Dư Có quy đổi

                                                  , AOL."MODEL_CHUNG_TU"
                                                , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                              THEN 0
                                                ELSE 1
                                                END AS "OrderType"
                                              , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                              THEN NULL
                                                ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                                END AS "THU_TU_CHI_TIET_GHI_SO"
                                               , PU."DON_MUA_HANG_ID"


                                              FROM so_cong_no_chi_tiet AS AOL
                                                  INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                                  INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                                  INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                                  INNER JOIN (SELECT *
                                                              FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                                           bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                                      ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"

                                                  INNER JOIN DS_DON_MUA_HANG AS PU ON PU."DON_MUA_HANG_ID" = AOL."DON_MUA_HANG_ID"


                                              WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                                    AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                                    AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                                    AND AN."DOI_TUONG_SELECTION" = '0'
                                          ) AS AD

                                     GROUP BY
                                         AD."SO_DON_HANG",
                                         AD."NGAY_DON_HANG",
                                         AD."DOI_TUONG_ID",
                                         AD."MA",
                                         AD."HO_VA_TEN",


                                         AD."NGAY_HACH_TOAN", -- Ngày hạch toán
                                         AD."NGAY_CHUNG_TU",
                                         -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                         AD."SO_CHUNG_TU",
                                         -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                         --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
                                         AD."ID_CHUNG_TU",
                                         AD."LOAI_CHUNG_TU", --Loại chứng từ
                                         AD."DIEN_GIAI_CHUNG", -- Diễn giải (lấy diễn giải Master)
                                         AD."SO_TAI_KHOAN", -- TK công nợ
                                         AD."TINH_CHAT", -- Tính chất tài khoản
                                         AD."MA_TAI_KHOAN_DOI_UNG", --TK đối ứng
                                         AD."MODEL_CHUNG_TU",
                                          AD."OrderType",
                                            AD."THU_TU_CHI_TIET_GHI_SO",
                                           AD."DON_MUA_HANG_ID"


                                 ) AS RSS


                            WHERE RSS."GHI_NO_NGUYEN_TE" <> 0
                                  OR RSS."GHI_NO" <> 0
                                  OR RSS."GHI_CO_NGUYEN_TE" <> 0
                                  OR RSS."GHI_CO" <> 0
                                  OR "DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE" <> 0
                                  OR "DU_NO" - "DU_CO" <> 0

                            ORDER BY
                                RSS."NGAY_DON_HANG",
                                RSS."SO_DON_HANG",
                                RSS."MA",
                                RSS."SO_TAI_KHOAN",
                                  RSS."OrderType",

                                RSS."NGAY_HACH_TOAN",
                                RSS."NGAY_CHUNG_TU",
                                RSS."SO_CHUNG_TU",
                                  RSS."THU_TU_CHI_TIET_GHI_SO"
                    ;
                END IF
                ;
                 FOR rec IN
    SELECT *
    FROM TMP_KET_QUA
    WHERE "OrderType" <> 2

    ORDER BY
        RowNum
    LOOP
        SELECT (CASE WHEN rec."OrderType" = 0
            THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0 --DU_NO_NGUYEN_TE
                THEN rec."DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                  ELSE -1
                       * rec."DU_NO_NGUYEN_TE" --DU_NO_NGUYEN_TE
                  END)
                WHEN
                    MA_KHACH_HANG_TMP <> rec."MA"
                        OR rec."DON_MUA_HANG_ID" <>  DON_MUA_HANG_ID_TMP
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"

                    THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                ELSE SO_TIEN_TON_NGUYEN_TE_TMP + rec."GHI_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                     - rec."GHI_NO_NGUYEN_TE" --GHI_NO_NGUYEN_TE
                END)
        INTO SO_TIEN_TON_NGUYEN_TE_TMP

    ;

        rec."DU_NO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
            THEN -1 * SO_TIEN_TON_NGUYEN_TE_TMP
                                 WHEN rec."TINH_CHAT" = '1'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
                                     THEN -1
                                          * SO_TIEN_TON_NGUYEN_TE_TMP
                                      ELSE 0
                                      END
                                 END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;

        rec."DU_CO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
            THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                 WHEN rec."TINH_CHAT" = '0'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
                                     THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                      ELSE 0
                                      END
                                 END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;

        SELECT (CASE WHEN rec."OrderType" = 0
            THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                  ELSE -1
                       * rec."DU_NO" --DU_NO_NGUYEN_TE
                  END)
                 WHEN
                    MA_KHACH_HANG_TMP <> rec."MA"
                        OR rec."DON_MUA_HANG_ID" <>  DON_MUA_HANG_ID_TMP
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    THEN rec."GHI_CO" - rec."GHI_NO" --PHAT_SINH_CO_NGUYEN_TE
                ELSE SO_TIEN_TON_TMP + rec."GHI_CO"--PHAT_SINH_CO_NGUYEN_TE
                     - rec."GHI_NO" --GHI_NO_NGUYEN_TE
                END)
        INTO SO_TIEN_TON_TMP
    ;

        rec."DU_NO" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
            THEN -1 * SO_TIEN_TON_TMP
                       WHEN rec."TINH_CHAT" = '1'
                           THEN 0
                       ELSE CASE WHEN SO_TIEN_TON_TMP < 0
                           THEN -1
                                * SO_TIEN_TON_TMP
                            ELSE 0
                            END
                       END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO" = rec."DU_NO"
        WHERE RowNum = rec.RowNum
    ;


        rec."DU_CO" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
            THEN SO_TIEN_TON_TMP
                       WHEN rec."TINH_CHAT" = '0'
                           THEN 0
                       ELSE CASE WHEN SO_TIEN_TON_TMP > 0
                           THEN SO_TIEN_TON_TMP
                            ELSE 0
                            END
                       END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO" = rec."DU_CO"
        WHERE RowNum = rec.RowNum
    ;


        MA_KHACH_HANG_TMP = rec."MA"
    ;
         DON_MUA_HANG_ID_TMP = rec."DON_MUA_HANG_ID"
    ;
        SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
    ;


    END LOOP
    ;




            END $$
            ;
           SELECT *
          FROM TMP_KET_QUA
          OFFSET %(offset)s
          LIMIT %(limit)s
          ;

 """
      cr.execute(query,params)
      for line in cr.dictfetchall():
          record.append({
              
              'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
              'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
              'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
              'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
              'TK_CO_ID': line.get('SO_TAI_KHOAN', ''),
              'TK_DOI_TUONG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
              'NO_PHAT_SINH': line.get('GHI_NO', ''),
              'CO_PHAT_SINH': line.get('GHI_CO', ''),
              'NO_SO_DU': line.get('DU_NO', ''),
              'CO_SO_DU': line.get('DU_CO', ''),
              'SO_DON_HANG': line.get('SO_DON_HANG', ''),             
              'ID_GOC': line.get('ID_CHUNG_TU', ''),
              'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
              'TEN_NHA_CUNG_CAP': line.get('HO_VA_TEN', ''),
              'NGAY_DON_HANG': line.get('NGAY_DON_HANG', ''),
              })
      return record
 
#lấy báo cáo thống kê theo không chọn
    def _lay_bao_cao_khong_chon(self, params):      
      record = []
      cr = self.env.cr
      query = """
          DO LANGUAGE plpgsql $$
          DECLARE

             chi_nhanh_id                        INTEGER :=%(CHI_NHANH_ID)s;

                  tu_ngay                             DATE := %(TU_NGAY)s;

                  den_ngay                            DATE := %(DEN_NGAY)s;

                  bao_gom_du_lieu_chi_nhanh_phu_thuoc  INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                  so_tai_khoan                          VARCHAR(127) := %(TAI_KHOAN_ID)s;

                  

                  loai_tien_id                         VARCHAR(127) :=%(currency_id)s;


                  CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU                          INTEGER :=%(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

                  CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU                         INTEGER := %(CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU)s;


              rec                                 RECORD;
              AccountNumberPercent            VARCHAR(100);
              SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT := 0;

              SO_TIEN_TON_TMP                       FLOAT := 0;

              MA_KHACH_HANG_TMP                     VARCHAR(100) := N'';

              SO_TAI_KHOAN_TMP                      VARCHAR(100) := N'';

          BEGIN

              DROP TABLE IF EXISTS DS_KHACH_HANG_NCC
              ;

              CREATE TEMP TABLE DS_KHACH_HANG_NCC
                  AS
                      SELECT
                          AO.id
                          , AO."MA"
                          , AO."HO_VA_TEN"
                          , AO."DIA_CHI"

                          , AO."MA_SO_THUE"

                      FROM res_partner AS AO
                      WHERE (AO.id  = any( %(NHA_CUNG_CAP_IDS)s))
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
                    , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE A."SO_TAI_KHOAN" = so_tai_khoan
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;
    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , concat(A."SO_TAI_KHOAN", '%%') AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE A."CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '0'
                      AND "LA_TK_TONG_HOP" = '0'
                --AND IsParent = 0
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;
    END IF
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq

    ;

    CREATE TABLE TMP_KET_QUA
    (
        RowNum                 INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,

        "DOI_TUONG_ID"         INT
        ,
        "MA"                   VARCHAR(200)
        ,
        "HO_VA_TEN"            VARCHAR(200)
        ,
        "DIA_CHI"              VARCHAR(200)
        ,
        "NGAY_HACH_TOAN"       TIMESTAMP
        ,
        "NGAY_CHUNG_TU"        TIMESTAMP
        ,
        "SO_CHUNG_TU"          VARCHAR(200)
        ,
        "ID_CHUNG_TU"          INT

        ,
        "LOAI_CHUNG_TU"        VARCHAR(200)
        ,
        "DIEN_GIAI_CHUNG"      VARCHAR(200)
        ,
        "SO_TAI_KHOAN"         VARCHAR(200)
        ,
        "TINH_CHAT"            VARCHAR(200)
        ,
        "MA_TAI_KHOAN_DOI_UNG" VARCHAR(200)
        ,
        "GHI_NO_NGUYEN_TE"     FLOAT
        ,
        "GHI_NO"               FLOAT
        ,
        "GHI_CO_NGUYEN_TE"     FLOAT
        ,
        "GHI_CO"               FLOAT
        , -- Phát sinh có quy đổi
        "DU_NO_NGUYEN_TE"      FLOAT
        , --Dư Nợ
        "DU_NO"                FLOAT
        , --   --Dư Nợ Quy đổi
        "DU_CO_NGUYEN_TE"      FLOAT
        , --   --Dư Có
        "DU_CO"                FLOAT

        ,
        "MODEL_CHUNG_TU"       VARCHAR(200)
        ,
        "OrderType"            INT

        ,
        "SO_HOA_DON"           VARCHAR(200)
    )
    ;


    IF CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 0
    THEN
        INSERT INTO TMP_KET_QUA

        ("DOI_TUONG_ID"
            ,
         "MA"
            ,
         "HO_VA_TEN"
            ,
         "DIA_CHI"
            ,
         "NGAY_HACH_TOAN"
            ,
         "NGAY_CHUNG_TU"
            ,
         "SO_CHUNG_TU"
            ,
         "ID_CHUNG_TU"
            ,
         "LOAI_CHUNG_TU"
            ,
         "DIEN_GIAI_CHUNG"
            ,
         "SO_TAI_KHOAN"
            ,
         "TINH_CHAT"
            ,
         "MA_TAI_KHOAN_DOI_UNG"
            ,
         "GHI_NO_NGUYEN_TE"
            ,
         "GHI_NO"
            ,
         "GHI_CO_NGUYEN_TE"
            ,
         "GHI_CO"
            , -- Phát sinh có quy đổi
         "DU_NO_NGUYEN_TE"
            , --Dư Nợ
         "DU_NO"
            , --   --Dư Nợ Quy đổi
         "DU_CO_NGUYEN_TE"
            , --   --Dư Có
         "DU_CO"

            ,
         "MODEL_CHUNG_TU"
            ,
         "OrderType"
            ,
         "SO_HOA_DON"
        )

            SELECT
                "DOI_TUONG_ID"
                , "MA"
                , "HO_VA_TEN"
                , "DIA_CHI"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "ID_CHUNG_TU"

                , "LOAI_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , "SO_TAI_KHOAN"
                , "TINH_CHAT"
                , "MA_TAI_KHOAN_DOI_UNG"
                , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                , SUM("GHI_NO")           AS "GHI_NO"
                , SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                , SUM("GHI_CO")           AS "GHI_CO"
                , -- Phát sinh có quy đổi
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE")) > 0
                       THEN (SUM("DU_NO_NGUYEN_TE") - SUM("DU_CO_NGUYEN_TE"))
                        ELSE 0
                        END
                   END)                   AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN (SUM("DU_NO") - SUM("DU_CO"))
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_NO") - SUM("DU_CO")) > 0
                       THEN SUM("DU_NO") - SUM("DU_CO")
                        ELSE 0
                        END
                   END)                   AS "DU_NO"
                , --   --Dư Nợ Quy đổi
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE")) > 0
                       THEN (SUM("DU_CO_NGUYEN_TE") - SUM("DU_NO_NGUYEN_TE"))
                        ELSE 0
                        END
                   END)                   AS "DU_CO_NGUYEN_TE"
                , --   --Dư Có
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN (SUM("DU_CO") - SUM("DU_NO"))
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_CO") - SUM("DU_NO")) > 0
                       THEN (SUM("DU_CO") - SUM("DU_NO"))
                        ELSE 0
                        END
                   END)                   AS "DU_CO"
                --   --Dư Có quy đổi
                , "MODEL_CHUNG_TU"
                , "OrderType"
                , "SO_HOA_DON"

            FROM (


                     SELECT
                         AOL."DOI_TUONG_ID"
                         , LAOI."MA"
                         , LAOI."HO_VA_TEN"
                         , LAOI."DIA_CHI"

                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN NULL
                           ELSE AOL."NGAY_HACH_TOAN"
                           END AS "NGAY_HACH_TOAN"
                         , -- Ngày hạch toán
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN NULL
                           ELSE "NGAY_CHUNG_TU"
                           END AS "NGAY_CHUNG_TU"
                         , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN NULL
                           ELSE AOL."SO_CHUNG_TU"
                           END AS "SO_CHUNG_TU"
                         , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN NULL
                           ELSE AOL."ID_CHUNG_TU"
                           END AS "ID_CHUNG_TU"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN NULL
                           ELSE AOL."LOAI_CHUNG_TU"
                           END AS "LOAI_CHUNG_TU"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN 'Số dư đầu kỳ'
                           WHEN CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1
                                AND (AOL."MA_TK_DOI_UNG" LIKE '3331%%' OR AOL."MA_TK_DOI_UNG" LIKE '133%%')
                               THEN 'Thuế GTGT của hàng hóa, dịch vụ'
                           ELSE AOL."DIEN_GIAI"
                           END AS "DIEN_GIAI_CHUNG"

                         /* Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                         , TBAN."SO_TAI_KHOAN"
                         , -- TK công nợ
                         TBAN."TINH_CHAT"
                         , -- Tính chất tài khoản
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN NULL
                           ELSE AOL."MA_TK_DOI_UNG"
                           END AS "MA_TAI_KHOAN_DOI_UNG"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                         , -- Phát sinh có quy đổi
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN AOL."GHI_NO_NGUYEN_TE"
                           ELSE 0
                           END AS "DU_NO_NGUYEN_TE"
                         , --Dư Nợ
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN AOL."GHI_NO"
                           ELSE 0
                           END AS "DU_NO"
                         , --Dư Nợ Quy đổi
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN AOL."GHI_CO_NGUYEN_TE"
                           ELSE 0
                           END AS "DU_CO_NGUYEN_TE"
                         , --Dư Có
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN AOL."GHI_CO"
                           ELSE 0
                           END AS "DU_CO"

                         , AOL."MODEL_CHUNG_TU"
                         , --Dư Có quy đổi
                           CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN 0
                           ELSE 1
                           END AS "OrderType"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN NULL
                           ELSE AOL."SO_HOA_DON"
                           END AS "SO_HOA_DON"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN 2
                           WHEN (CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1
                                 AND (AOL."MA_TK_DOI_UNG" LIKE '3331%%' OR AOL."MA_TK_DOI_UNG" LIKE '133%%')
                           )
                               THEN 1
                           ELSE 0
                           END AS "GroupOrder"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN ''
                           WHEN (CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1
                                 AND (AOL."MA_TK_DOI_UNG" LIKE '3331%%' OR AOL."MA_TK_DOI_UNG" LIKE '133%%')
                           )
                               THEN AOL."SO_HOA_DON" || '_' || AOL."MA_TK_DOI_UNG"
                           ELSE ''
                           END AS "AccountNoToOrder"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                         THEN 2
                           WHEN (CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1
                                 AND (AOL."MA_TK_DOI_UNG" LIKE '3331%%' OR AOL."MA_TK_DOI_UNG" LIKE '133%%')
                           )
                               THEN 0
                           ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                           END AS "THU_TU_TRONG_CHUNG_TU"
                         , CASE
                           WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                               THEN 2
                           WHEN (CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU = 1
                                 AND (AOL."MA_TK_DOI_UNG" LIKE '3331%%' OR AOL."MA_TK_DOI_UNG" LIKE '133%%')
                           )
                               THEN 0
                           ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                           END AS "THU_TU_CHI_TIET_GHI_SO"


                     FROM so_cong_no_chi_tiet AS AOL
                         INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                         INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                         INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                         INNER JOIN (SELECT *
                                     FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                  bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                             ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                         LEFT JOIN danh_muc_vat_tu_hang_hoa I ON I.id = AOL."MA_HANG_ID"
                         --Lấy lên tên hàng từ danh mục
                         LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
                         -- Danh mục ĐVT
                         /*hoant 27.09.2017 theo cr 138363*/
                         LEFT JOIN danh_muc_don_vi_tinh AS MainUnit
                             ON AOL."DVT_CHINH_ID" = MainUnit.id -- Danh mục ĐVT chính

                     WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                            AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                           AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                           AND AN."DOI_TUONG_SELECTION" = '0'
                 ) AS RSNS

            GROUP BY
                RSNS."DOI_TUONG_ID",
                RSNS."MA"
                , RSNS."DOI_TUONG_ID"
                , RSNS."MA"
                , RSNS."HO_VA_TEN"
                , RSNS."DIA_CHI"
                , RSNS."NGAY_HACH_TOAN"
                , RSNS."NGAY_CHUNG_TU"
                , RSNS."SO_CHUNG_TU"
                , RSNS."ID_CHUNG_TU"
                , RSNS."LOAI_CHUNG_TU"
                , RSNS."MA_TAI_KHOAN_DOI_UNG"
                , RSNS."DIEN_GIAI_CHUNG"
                , RSNS."SO_TAI_KHOAN"

                , RSNS."TINH_CHAT"
                , RSNS."GHI_NO_NGUYEN_TE"
                , RSNS."GHI_NO"
                , RSNS."GHI_CO_NGUYEN_TE"
                , RSNS."GHI_CO"
                , RSNS."MODEL_CHUNG_TU"
                , RSNS."OrderType"
                , RSNS."SO_HOA_DON"
                , RSNS."GroupOrder"
                , RSNS."AccountNoToOrder"
                , RSNS."THU_TU_TRONG_CHUNG_TU"
                , RSNS."THU_TU_CHI_TIET_GHI_SO"


            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                   OR SUM("GHI_NO") <> 0
                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                   OR SUM("GHI_CO") <> 0
                   OR SUM("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <> 0
                   OR SUM("DU_NO" - "DU_CO") <> 0

            ORDER BY
                RSNS."MA",
                RSNS."SO_TAI_KHOAN",
                RSNS."OrderType",
                RSNS."NGAY_HACH_TOAN",
                RSNS."NGAY_CHUNG_TU",
                RSNS."SO_CHUNG_TU",
                RSNS."GroupOrder",
                RSNS."AccountNoToOrder",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"

        ;
    ELSE
        INSERT INTO TMP_KET_QUA

        ("DOI_TUONG_ID"
            ,
         "MA"
            ,
         "HO_VA_TEN"
            ,
         "DIA_CHI"
            ,
         "NGAY_HACH_TOAN"
            ,
         "NGAY_CHUNG_TU"
            ,
         "SO_CHUNG_TU"
            ,
         "ID_CHUNG_TU"
            ,
         "LOAI_CHUNG_TU"
            ,
         "DIEN_GIAI_CHUNG"
            ,
         "SO_TAI_KHOAN"
            ,
         "TINH_CHAT"
            ,
         "MA_TAI_KHOAN_DOI_UNG"
            ,
         "GHI_NO_NGUYEN_TE"
            ,
         "GHI_NO"
            ,
         "GHI_CO_NGUYEN_TE"
            ,
         "GHI_CO"
            , -- Phát sinh có quy đổi
         "DU_NO_NGUYEN_TE"
            , --Dư Nợ
         "DU_NO"
            , --   --Dư Nợ Quy đổi
         "DU_CO_NGUYEN_TE"
            , --   --Dư Có
         "DU_CO"

            ,
         "MODEL_CHUNG_TU"
            ,
         "OrderType"
        )

            SELECT
                "DOI_TUONG_ID"
                , "MA"
                , "HO_VA_TEN"
                , "DIA_CHI"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "ID_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , "SO_TAI_KHOAN"
                , "TINH_CHAT"
                , "MA_TAI_KHOAN_DOI_UNG"
                , "GHI_NO_NGUYEN_TE"
                , "GHI_NO"
                , "GHI_CO_NGUYEN_TE"
                , "GHI_CO"
                , -- Phát sinh có quy đổi
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN ("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE")) > 0
                     THEN (("DU_NO_NGUYEN_TE") - ("DU_CO_NGUYEN_TE"))
                      ELSE 0
                      END
                 END) AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN (("DU_NO") - ("DU_CO"))
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (("DU_NO") - ("DU_CO")) > 0
                     THEN ("DU_NO") - ("DU_CO")
                      ELSE 0
                      END
                 END) AS "DU_NO"
                , --   --Dư Nợ Quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE")) > 0
                     THEN (("DU_CO_NGUYEN_TE") - ("DU_NO_NGUYEN_TE"))
                      ELSE 0
                      END
                 END) AS "DU_CO_NGUYEN_TE"
                , --   --Dư Có
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (("DU_CO") - ("DU_NO"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (("DU_CO") - ("DU_NO")) > 0
                     THEN (("DU_CO") - ("DU_NO"))
                      ELSE 0
                      END
                 END) AS "DU_CO"
                , "MODEL_CHUNG_TU"
                , "OrderType"


            FROM (
                     SELECT
                         AD."DOI_TUONG_ID"
                         , AD."MA"
                         , AD."HO_VA_TEN"
                         , AD."DIA_CHI"
                         , AD."NGAY_HACH_TOAN"
                         , AD."NGAY_CHUNG_TU"
                         , AD."SO_CHUNG_TU"
                         , AD."ID_CHUNG_TU"
                         , AD."LOAI_CHUNG_TU"
                         , AD."DIEN_GIAI_CHUNG"
                         , AD."SO_TAI_KHOAN"
                         , AD."TINH_CHAT"
                         , AD."MA_TAI_KHOAN_DOI_UNG"
                         , SUM(AD."GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                         , SUM(AD."GHI_NO")           AS "GHI_NO"
                         , SUM(AD."GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                         , SUM(AD."GHI_CO")           AS "GHI_CO"

                         , SUM(AD."DU_NO_NGUYEN_TE")  AS "DU_NO_NGUYEN_TE"
                         , SUM(AD."DU_NO")            AS "DU_NO"
                         , SUM(AD."DU_CO_NGUYEN_TE")  AS "DU_CO_NGUYEN_TE"
                         , SUM(AD."DU_CO")            AS "DU_CO"
                         , AD."MODEL_CHUNG_TU"
                         , AD."OrderType"
                         , AD."THU_TU_CHI_TIET_GHI_SO"


                     FROM (


                              SELECT
                                  AOL."DOI_TUONG_ID"
                                  , LAOI."MA"
                                  , LAOI."HO_VA_TEN"
                                  , LAOI."DIA_CHI"

                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                  THEN NULL
                                    ELSE AOL."NGAY_HACH_TOAN"
                                    END AS "NGAY_HACH_TOAN"
                                  , -- Ngày hạch toán
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN NULL
                                    ELSE "NGAY_CHUNG_TU"
                                    END AS "NGAY_CHUNG_TU"
                                  , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN NULL
                                    ELSE AOL."SO_CHUNG_TU"
                                    END AS "SO_CHUNG_TU"
                                  , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN NULL
                                    ELSE AOL."ID_CHUNG_TU"
                                    END AS "ID_CHUNG_TU"
                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                  THEN NULL
                                    ELSE AOL."LOAI_CHUNG_TU"
                                    END AS "LOAI_CHUNG_TU"
                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                  THEN N'Số dư đầu kỳ'
                                    ELSE CASE WHEN
                                        (AOL."MA_TK_DOI_UNG" LIKE '133%%' OR AOL."MA_TK_DOI_UNG" LIKE '3331%%')
                                        THEN N'Thuế GTGT của hàng hóa, dịch vụ'
                                         ELSE AOL."DIEN_GIAI_CHUNG" END
                                    END AS "DIEN_GIAI_CHUNG"

                                  /*ntquang 26.03.2018 Thi công CR195226 - khi công gộp : Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */

                                  , TBAN."SO_TAI_KHOAN"
                                  , -- TK công nợ
                                  TBAN."TINH_CHAT"
                                  , -- Tính chất tài khoản
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN NULL
                                    ELSE AOL."MA_TK_DOI_UNG"
                                    END AS "MA_TAI_KHOAN_DOI_UNG"
                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
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
                                  , -- Phát sinh có quy đổi
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN AOL."GHI_NO_NGUYEN_TE"
                                    ELSE 0
                                    END AS "DU_NO_NGUYEN_TE"
                                  , --Dư Nợ
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN AOL."GHI_NO"
                                    ELSE 0
                                    END AS "DU_NO"
                                  , --Dư Nợ Quy đổi
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN AOL."GHI_CO_NGUYEN_TE"
                                    ELSE 0
                                    END AS "DU_CO_NGUYEN_TE"
                                  , --Dư Có
                                    CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN AOL."GHI_CO"
                                    ELSE 0
                                    END AS "DU_CO"
                                  --Dư Có quy đổi

                                  , AOL."MODEL_CHUNG_TU"
                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                  THEN 0
                                    ELSE 1
                                    END AS "OrderType"
                                  , CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                  THEN NULL
                                    ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                    END AS "THU_TU_CHI_TIET_GHI_SO"
                              FROM so_cong_no_chi_tiet AS AOL
                                  INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                                  INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                  INNER JOIN DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                  INNER JOIN (SELECT *
                                              FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id,
                                                                           bao_gom_du_lieu_chi_nhanh_phu_thuoc)) AS TLB
                                      ON AOL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                  LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id -- Danh mục ĐVT
                              /*hoant 27.09.2017 theo cr 138363*/

                              WHERE AOL."NGAY_HACH_TOAN" <= den_ngay
                                    AND (loai_tien_id IS NULL OR (select "MA_LOAI_TIEN" from res_currency T WHERE T.id= AOL."currency_id") = loai_tien_id)
                                    AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                    AND AN."DOI_TUONG_SELECTION" = '0'
                          ) AS AD

                     GROUP BY
                         AD."DOI_TUONG_ID",
                         AD."MA",
                         AD."HO_VA_TEN",
                         AD."DIA_CHI",

                         AD."NGAY_HACH_TOAN", -- Ngày hạch toán
                         AD."NGAY_CHUNG_TU",
                         -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                         AD."SO_CHUNG_TU",
                         -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                         --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
                         AD."ID_CHUNG_TU",
                         AD."LOAI_CHUNG_TU", --Loại chứng từ
                         AD."DIEN_GIAI_CHUNG", -- Diễn giải (lấy diễn giải Master)
                         AD."SO_TAI_KHOAN", -- TK công nợ
                         AD."TINH_CHAT", -- Tính chất tài khoản
                         AD."MA_TAI_KHOAN_DOI_UNG", --TK đối ứng
                         --   TMP_KET_QUA."TY_GIA", --Tỷ giá

                         AD."MODEL_CHUNG_TU",
                         AD."OrderType",
                         AD."THU_TU_CHI_TIET_GHI_SO"


                 ) AS RSS


            WHERE RSS."GHI_NO_NGUYEN_TE" <> 0
                  OR RSS."GHI_NO" <> 0
                  OR RSS."GHI_CO_NGUYEN_TE" <> 0
                  OR RSS."GHI_CO" <> 0
                  OR "DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE" <> 0
                  OR "DU_NO" - "DU_CO" <> 0


            ORDER BY
                RSS."MA",
                RSS."SO_TAI_KHOAN",
                RSS."OrderType",
                RSS."NGAY_HACH_TOAN",
                RSS."NGAY_CHUNG_TU",
                RSS."SO_CHUNG_TU",
                RSS."THU_TU_CHI_TIET_GHI_SO",
                  RSS."MA_TAI_KHOAN_DOI_UNG"

        ;


    END IF
    ;

    FOR rec IN
    SELECT *
    FROM TMP_KET_QUA
    WHERE "OrderType" <> 2

    ORDER BY
        RowNum
    LOOP
        SELECT (CASE WHEN rec."OrderType" = 0
            THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0 --DU_NO_NGUYEN_TE
                THEN rec."DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                  ELSE -1
                       * rec."DU_NO_NGUYEN_TE" --DU_NO_NGUYEN_TE
                  END)
                WHEN
                    MA_KHACH_HANG_TMP <> rec."MA"
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"

                    THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                ELSE SO_TIEN_TON_NGUYEN_TE_TMP + rec."GHI_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                     - rec."GHI_NO_NGUYEN_TE" --GHI_NO_NGUYEN_TE
                END)
        INTO SO_TIEN_TON_NGUYEN_TE_TMP

    ;

        rec."DU_NO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
            THEN -1 * SO_TIEN_TON_NGUYEN_TE_TMP
                                 WHEN rec."TINH_CHAT" = '1'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
                                     THEN -1
                                          * SO_TIEN_TON_NGUYEN_TE_TMP
                                      ELSE 0
                                      END
                                 END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;

        rec."DU_CO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
            THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                 WHEN rec."TINH_CHAT" = '0'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
                                     THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                      ELSE 0
                                      END
                                 END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;

        SELECT (CASE WHEN rec."OrderType" = 0
            THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                  ELSE -1
                       * rec."DU_NO" --DU_NO_NGUYEN_TE
                  END)
                WHEN
                    MA_KHACH_HANG_TMP <> rec."MA"
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    THEN rec."GHI_CO" - rec."GHI_NO" --PHAT_SINH_CO_NGUYEN_TE
                ELSE SO_TIEN_TON_TMP + rec."GHI_CO"--PHAT_SINH_CO_NGUYEN_TE
                     - rec."GHI_NO" --GHI_NO_NGUYEN_TE
                END)
        INTO SO_TIEN_TON_TMP
    ;

        rec."DU_NO" = (CASE WHEN rec."TINH_CHAT" = '0' --DU_NO_NGUYEN_TE
            THEN -1 * SO_TIEN_TON_TMP
                       WHEN rec."TINH_CHAT" = '1'
                           THEN 0
                       ELSE CASE WHEN SO_TIEN_TON_TMP < 0
                           THEN -1
                                * SO_TIEN_TON_TMP
                            ELSE 0
                            END
                       END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO" = rec."DU_NO"
        WHERE RowNum = rec.RowNum
    ;


        rec."DU_CO" = (CASE WHEN rec."TINH_CHAT" = '1' --DU_CO_NGUYEN_TE
            THEN SO_TIEN_TON_TMP
                       WHEN rec."TINH_CHAT" = '0'
                           THEN 0
                       ELSE CASE WHEN SO_TIEN_TON_TMP > 0
                           THEN SO_TIEN_TON_TMP
                            ELSE 0
                            END
                       END)
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO" = rec."DU_CO"
        WHERE RowNum = rec.RowNum
    ;


        MA_KHACH_HANG_TMP = rec."MA"
    ;

        SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
    ;


    END LOOP
    ;


END $$
;

SELECT *
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s
;
          """
      cr.execute(query,params)
      # Get and show result
      for line in cr.dictfetchall():
          record.append({
              
              'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
              'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
              'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
              'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
              'TK_CO_ID': line.get('SO_TAI_KHOAN', ''),
              'TK_DOI_TUONG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
              'NO_PHAT_SINH': line.get('GHI_NO', ''),
              'CO_PHAT_SINH': line.get('GHI_CO', ''),
              'NO_SO_DU': line.get('DU_NO', ''),
              'CO_SO_DU': line.get('DU_CO', ''),
              
              'TEN_NHAN_VIEN': '',
              'TEN_NHA_CUNG_CAP': line.get('HO_VA_TEN', ''),
              'name': '',
              'ID_GOC': line.get('ID_CHUNG_TU', ''),
              'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
              })
      return record

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    @api.model
    def default_get(self, fields_list):
      result = super(BAO_CAO_CHI_TIET_CONG_NO_PHAI_TRA_NHA_CUNG_CAP, self).default_get(fields_list)
      chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
      tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_DOI_TUONG', '=', 'True'),('DOI_TUONG_SELECTION', '=like', '0')],limit=1)
      if chi_nhanh:
        result['CHI_NHANH_ID'] = chi_nhanh.id
      loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
      if loai_tien:
        result['currency_id'] = loai_tien.id
      if tai_khoan:
        result['TAI_KHOAN_ID'] = tai_khoan.id
      return result
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
        loai_tien = ''
        loai_tien_id =  self.env['res.currency'].browse(currency_id)
        if loai_tien_id:
          loai_tien =loai_tien_id.MA_LOAI_TIEN
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan = ''
        tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        if tai_khoan_id:
          tai_khoan = tai_khoan_id.SO_TAI_KHOAN
        param = 'Tài khoản: %s; Loại tiền: %s; Từ ngày: %s đến ngày %s' % (tai_khoan, loai_tien, TU_NGAY_F, DEN_NGAY_F)
        if (THONG_KE_THEO == 'KHONG_CHON'):
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_tra_nha_cung_cap_khongchon').read()[0]
        elif (THONG_KE_THEO == 'NHAN_VIEN'):
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_tra_nha_cung_cap_nhanvien').read()[0]
        elif (THONG_KE_THEO == 'HOP_DONG_MUA'):
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_tra_nha_cung_cap_hopdongmua').read()[0]
        elif (THONG_KE_THEO == 'CONG_TRINH'):
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_tra_nha_cung_cap_congtrinh').read()[0]
        elif (THONG_KE_THEO == 'DON_MUA_HANG'):
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_tra_nha_cung_cap_donmuahang').read()[0]
        #action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action