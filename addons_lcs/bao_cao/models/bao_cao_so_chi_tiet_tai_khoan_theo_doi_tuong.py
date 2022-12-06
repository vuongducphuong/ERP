# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_CHI_TIET_TAI_KHOAN_THEO_DOI_TUONG(models.Model):
    _name = 'bao.cao.so.chi.tiet.tai.khoan.theo.doi.tuong'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='true')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI', required ='True')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản', required=True)
    TU = fields.Date(string='Từ', help='Từ',default= fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default= fields.Datetime.now)
    LOAI_DOI_TUONG = fields.Selection([('0', '<<Tất cả>>'), ('1', 'Khách hàng'), ('2', 'Nhà cung cấp'), ('3', 'Nhân viên'), ], string='Loại đối tượng', help='Loại đối tượng',default='0', required = 'True')
    NHOM_KH_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH/NCC', help='Nhóm khách hàng/nhà cung cấp')
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau', help='Cộng gộp các bút toán giống nhau')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    TK_CO_ID = fields.Char(string='TK công nợ', help='Tài khoản công nợ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    NO_PHAT_SINH = fields.Float(string='Nợ', help='Nợ phát sinh',digits=decimal_precision.get_precision('VND'))
    CO_PHAT_SINH = fields.Float(string='Có', help='Có phát sinh',digits=decimal_precision.get_precision('VND'))
    NO_DU = fields.Float(string='Nợ', help='Nợ dư',digits=decimal_precision.get_precision('VND'))
    CO_DU = fields.Float(string='Có', help='Có dư',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    DOI_TUONG_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_DOI_TUONG = fields.Boolean('Tất cả đối tượng', default=True)
    DOI_TUONG_MANY_IDS = fields.Many2many('res.partner','so_chi_tiet_tai_khoan_res_partner',domain=['|','|',('LA_NHAN_VIEN', '=', True),('LA_KHACH_HANG', '=', True),('LA_NHA_CUNG_CAP', '=', True)], string='Chọn đối tượng')

    NHAN_VIEN_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','so_chi_tiet_tai_khoan_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')

    KHACH_HANG_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner','so_chi_tiet_tai_khoan_res_partner', domain=[('LA_KHACH_HANG', '=', True)], string='Chọn khách hàng')

    NHA_CUNG_CAP_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHA_CUNG_CAP = fields.Boolean('Tất cả nhà cung cấp', default=True)
    NHA_CUNG_CAP_MANY_IDS = fields.Many2many('res.partner','so_chi_tiet_tai_khoan_res_partner', domain=[('LA_NHA_CUNG_CAP', '=', True)], string='Chọn nhà cung cấp')
    MA_PC_NHOM_KH = fields.Char()

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_CHI_TIET_TAI_KHOAN_THEO_DOI_TUONG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=','131')],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if tai_khoan:
            result['TAI_KHOAN_IDS'] = tai_khoan.id
        result['TAI_KHOAN_ID'] = -1
        return result
    
    @api.onchange('LOAI_DOI_TUONG')
    def _onchange_LOAI_DOI_TUONG(self):
        self.CHON_TAT_CA_DOI_TUONG = True
        self.CHON_TAT_CA_NHAN_VIEN = True
        self.CHON_TAT_CA_KHACH_HANG = True
        self.CHON_TAT_CA_NHA_CUNG_CAP = True
        self.DOI_TUONG_MANY_IDS = []
        self.NHAN_VIEN_MANY_IDS = []
        self.KHACH_HANG_MANY_IDS = []
        self.NHA_CUNG_CAP_MANY_IDS = []
    
    # Đối tượng
    @api.onchange('DOI_TUONG_IDS')
    def update_DOI_TUONG_IDS(self):
        self.DOI_TUONG_MANY_IDS =self.DOI_TUONG_IDS.ids
        
    @api.onchange('DOI_TUONG_MANY_IDS')
    def _onchange_DOI_TUONG_MANY_IDS(self):
        self.DOI_TUONG_IDS = self.DOI_TUONG_MANY_IDS.ids

    # Nhân viên
    @api.onchange('NHAN_VIEN_IDS')
    def update_NHAN_VIEN_IDS(self):
        self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS.ids
        
    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        self.NHAN_VIEN_IDS = self.NHAN_VIEN_MANY_IDS.ids

    # Khách hàng
    @api.onchange('KHACH_HANG_IDS')
    def update_KHACH_HANG_IDS(self):
        self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS.ids
        
    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.KHACH_HANG_IDS = self.KHACH_HANG_MANY_IDS.ids
    
    # Nhà cung cấp
    @api.onchange('NHA_CUNG_CAP_IDS')
    def update_NHA_CUNG_CAP_IDS(self):
        self.NHA_CUNG_CAP_MANY_IDS =self.NHA_CUNG_CAP_IDS.ids
        
    @api.onchange('NHA_CUNG_CAP_MANY_IDS')
    def _onchange_NHA_CUNG_CAP_MANY_IDS(self):
        self.NHA_CUNG_CAP_IDS = self.NHA_CUNG_CAP_MANY_IDS.ids
    
    @api.onchange('NHOM_KH_NCC_ID')
    def update_NHOM_KH_NCC_ID(self):
        # Khi thay đổi NHOM_KH_ID thì clear hết KH đã chọn
        self.DOI_TUONG_MANY_IDS = []
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KH_NCC_ID.MA_PHAN_CAP

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DOITUONG_IDS = params['DOITUONG_IDS'] if 'DOITUONG_IDS' in params.keys() else 'False'

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')


        LOAI_DOI_TUONG = params['LOAI_DOI_TUONG'] if 'LOAI_DOI_TUONG' in params.keys() else 'False'
        CHON_TAT_CA_DOI_TUONG = params['CHON_TAT_CA_DOI_TUONG'] if 'CHON_TAT_CA_DOI_TUONG' in params.keys() else 'False'

        DOI_TUONG_MANY_IDS = params['DOI_TUONG_MANY_IDS'] if 'DOI_TUONG_MANY_IDS' in params.keys() else 'False'
        CHON_TAT_CA_KHACH_HANG = params['CHON_TAT_CA_KHACH_HANG'] if 'CHON_TAT_CA_KHACH_HANG' in params.keys() else 'False'
        KHACH_HANG_MANY_IDS = params['KHACH_HANG_MANY_IDS'] if 'KHACH_HANG_MANY_IDS' in params.keys() else 'False'
        CHON_TAT_CA_NHA_CUNG_CAP = params['CHON_TAT_CA_NHA_CUNG_CAP'] if 'CHON_TAT_CA_NHA_CUNG_CAP' in params.keys() else 'False'
        NHA_CUNG_CAP_MANY_IDS = params['NHA_CUNG_CAP_MANY_IDS'] if 'NHA_CUNG_CAP_MANY_IDS' in params.keys() else 'False'
        CHON_TAT_CA_NHAN_VIEN = params['CHON_TAT_CA_NHAN_VIEN'] if 'CHON_TAT_CA_NHAN_VIEN' in params.keys() else 'False'
        NHAN_VIEN_MANY_IDS = params['NHAN_VIEN_MANY_IDS'] if 'NHAN_VIEN_MANY_IDS' in params.keys() else 'False'

        if LOAI_DOI_TUONG =='0':
            if CHON_TAT_CA_DOI_TUONG == 'False':
                if DOI_TUONG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đối tượng>. Xin vui lòng chọn lại.')
        elif LOAI_DOI_TUONG =='1':
            if CHON_TAT_CA_KHACH_HANG == 'False':
                if KHACH_HANG_MANY_IDS == []:
                 raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')
        elif LOAI_DOI_TUONG =='2':          
            if CHON_TAT_CA_NHA_CUNG_CAP == 'False':
                if NHA_CUNG_CAP_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhà cung cấp>. Xin vui lòng chọn lại.')
        elif LOAI_DOI_TUONG =='3':           
            if CHON_TAT_CA_NHAN_VIEN == 'False':
                if NHAN_VIEN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 1 if 'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' in params.keys() and params['CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU'] != 'False' else 0
        LOAI_DOI_TUONG = params['LOAI_DOI_TUONG'] if 'LOAI_DOI_TUONG' in params.keys() else 'False'
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHOM_KH_NCC_ID = params['NHOM_KH_NCC_ID'] if 'NHOM_KH_NCC_ID' in params.keys() and params['NHOM_KH_NCC_ID'] != 'False' else None
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        if  TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN

        MA_PC_NHOM_KH = params.get('MA_PC_NHOM_KH')
        DOI_TUONG_IDS = None
        if LOAI_DOI_TUONG =='3':
            if params.get('CHON_TAT_CA_NHAN_VIEN'):
                domain = [('LA_NHAN_VIEN','=', True)]
                DOI_TUONG_IDS =  self.env['res.partner'].search(domain).ids
            else:
                DOI_TUONG_IDS =  params.get('NHAN_VIEN_MANY_IDS')

        elif LOAI_DOI_TUONG =='1':
            if params.get('CHON_TAT_CA_KHACH_HANG'):
                domain = [('LA_KHACH_HANG','=', True)]
                if MA_PC_NHOM_KH:
                    domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
                DOI_TUONG_IDS =  self.env['res.partner'].search(domain).ids
            else:
                DOI_TUONG_IDS = params.get('KHACH_HANG_MANY_IDS')

        elif LOAI_DOI_TUONG =='2':
            if params.get('CHON_TAT_CA_NHA_CUNG_CAP'):
                domain = [('LA_NHA_CUNG_CAP','=', True)]
                if MA_PC_NHOM_KH:
                    domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
                DOI_TUONG_IDS =  self.env['res.partner'].search(domain).ids
            else:
                DOI_TUONG_IDS = params.get('NHA_CUNG_CAP_MANY_IDS')

        elif LOAI_DOI_TUONG =='0':
            if params.get('CHON_TAT_CA_DOI_TUONG'):
                domain = []
                if MA_PC_NHOM_KH:
                    domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
                DOI_TUONG_IDS =  self.env['res.partner'].search(domain).ids
            else:
                DOI_TUONG_IDS = params.get('DOI_TUONG_MANY_IDS')
        

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' : CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU,
            'LOAI_DOI_TUONG' : int(LOAI_DOI_TUONG),
            'NHOM_KH_NCC_ID' : NHOM_KH_NCC_ID,
            'TAI_KHOAN_ID' : TAI_KHOAN_ID,
            'DOITUONG_IDS' : DOI_TUONG_IDS or None,
            'limit': limit,
            'offset': offset,
        }
        # Execute SQL query here
        query = """
        --BAO_CAO_SO_CHI_TIET_TAI_KHOAN_THEO_DOI_TUONG: chỉ lấy phát sinh
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;
    --tham số từ

    v_den_ngay                            DATE := %(DEN_NGAY)s;
    --tham số đến

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
    --tham số bao gồm số liệu chi nhánh phụ thuộc

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;
    --tham số chi nhánh

    v_tai_khoan_id                        INTEGER := %(TAI_KHOAN_ID)s;
    --tham số tài khoản

    v_loai_doi_tuong                      INTEGER := %(LOAI_DOI_TUONG)s;
    --tham số loại đối tượng

    v_nhom_kh_ncc_id                      INTEGER := %(NHOM_KH_NCC_ID)s;
    --tham số Nhóm KH/NCC

    v_cong_gop_cac_but_toan_giong_nhau    INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;
    --cộng gộp các bút toán giống nhau

    

    rec                                   RECORD;
    SO_DU_CUOI_KY_TMP                     FLOAT :=0;
    SO_TAI_KHOAN_TMP                      VARCHAR(127) ;
    MA_DOI_TUONG_TMP                      VARCHAR(127) ;

BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;
    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;
    DROP TABLE IF EXISTS DS_TAI_KHOAN
    ;
    CREATE TEMP TABLE DS_TAI_KHOAN
    (
        "SO_TAI_KHOAN"         VARCHAR(127),
        "AccountNumberPercent" VARCHAR(127)
    )

    ;

        IF v_tai_khoan_id IS NOT NULL
        THEN
            INSERT INTO DS_TAI_KHOAN
                SELECT
                    v_tai_khoan_id
                    , v_tai_khoan_id || '%%'
            ;
        ELSE
        INSERT INTO DS_TAI_KHOAN
        SELECT
            A."SO_TAI_KHOAN"
            , A."SO_TAI_KHOAN" || '%%'
        FROM danh_muc_he_thong_tai_khoan AS A
        WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
              AND "LA_TK_TONG_HOP" = '0'
    ;

        END IF
        ;

    DROP TABLE IF EXISTS DS_DOI_TUONG
    ;

    CREATE TEMP TABLE DS_DOI_TUONG
        AS
            SELECT *
            FROM res_partner
            WHERE id = any (%(DOITUONG_IDS)s)
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        RowNum           INT DEFAULT NEXTVAL('TMP_KET_QUA_seq') PRIMARY KEY,
        "ID_CHUNG_TU"    INT,
        "MODEL_CHUNG_TU" VARCHAR(127),
        "NGAY_HACH_TOAN" DATE,
        "NGAY_CHUNG_TU"  DATE,
        "SO_CHUNG_TU"    VARCHAR(127), --SO_CHUNG_TU
        "DIEN_GIAI"      VARCHAR(255),
        "SO_TAI_KHOAN"   VARCHAR(127),
        "TK_DOI_UNG"     VARCHAR(127),
        "PHAT_SINH_NO"   FLOAT,
        "PHAT_SINH_CO"   FLOAT,
        "SO_DU_NO"       FLOAT,
        "SO_DU_CO"       FLOAT,
        "MA_DOI_TUONG"   VARCHAR(255),
        "TEN_DOI_TUONG"  VARCHAR(255),
         "OrderType"    INT



    )
    ;

    ----------------------------------

    --Lấy dữ liệu trong kỳ
    IF v_cong_gop_cac_but_toan_giong_nhau = 1
    THEN
        INSERT INTO TMP_KET_QUA
        (
            "ID_CHUNG_TU",
            "MODEL_CHUNG_TU",
            "NGAY_HACH_TOAN",
            "NGAY_CHUNG_TU",
            "SO_CHUNG_TU", --SO_CHUNG_TU
            "DIEN_GIAI",
            "SO_TAI_KHOAN",
            "TK_DOI_UNG",
            "PHAT_SINH_NO",
            "PHAT_SINH_CO",
            "SO_DU_NO",
            "SO_DU_CO",
            "MA_DOI_TUONG",
            "TEN_DOI_TUONG",
             "OrderType"
        )


            SELECT
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "DIEN_GIAI"
                , "SO_TAI_KHOAN"
                , "TK_DOI_UNG"
                , COALESCE("PHAT_SINH_NO", 0)
                , COALESCE("PHAT_SINH_CO", 0)
                , COALESCE("SO_DU_NO", 0)
                , COALESCE("SO_DU_CO", 0)
                , "MA_DOI_TUONG"
                , "TEN_DOI_TUONG"
                , "OrderType"

            FROM
                (SELECT
                       NULL :: INT      AS "ID_CHUNG_TU"
                     , NULL             AS "MODEL_CHUNG_TU"
                     , NULL :: DATE     AS "NGAY_HACH_TOAN"
                     , NULL :: DATE     AS "NGAY_CHUNG_TU"
                     , NULL             AS "SO_CHUNG_TU"
                     , N'Số dư đầu kỳ' AS "DIEN_GIAI"
                     , A."SO_TAI_KHOAN"
                     , NULL             AS "TK_DOI_UNG"
                     , 0                AS "PHAT_SINH_NO"
                     , 0                AS "PHAT_SINH_CO"
                     , CASE WHEN SUM(GL."GHI_NO" - GL."GHI_CO") > 0
                        THEN SUM(GL."GHI_NO" - GL."GHI_CO")
                       ELSE 0
                       END              AS "SO_DU_NO"
                     , CASE WHEN SUM(GL."GHI_CO" - GL."GHI_NO") > 0
                        THEN SUM(GL."GHI_CO" - GL."GHI_NO")
                       ELSE 0
                       END              AS "SO_DU_CO"
                     , GL."MA_DOI_TUONG"
                     , GL."TEN_DOI_TUONG"
                    ,0 AS "OrderType"
                     ,0 as "THU_TU_TRONG_CHUNG_TU"
                    ,0 as "THU_TU_CHI_TIET_GHI_SO"
                    ,'0' As "LOAI_HACH_TOAN"


                 FROM so_cai_chi_tiet AS GL
                     INNER JOIN TMP_LIST_BRAND BR ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                     INNER JOIN DS_DOI_TUONG AO ON AO.id = GL."DOI_TUONG_ID"
                     INNER JOIN DS_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
                 WHERE (GL."NGAY_HACH_TOAN" < v_tu_ngay)

                 GROUP BY
                     A."SO_TAI_KHOAN",
                     GL."MA_DOI_TUONG",
                     GL."TEN_DOI_TUONG"
                 HAVING SUM(GL."GHI_NO" - GL."GHI_CO") <> 0
                 UNION ALL
                 SELECT
                     GL."ID_CHUNG_TU"
                     , GL."MODEL_CHUNG_TU"
                     , GL."NGAY_HACH_TOAN"
                     , GL."NGAY_CHUNG_TU"
                     , GL."SO_CHUNG_TU"
                     , GL."DIEN_GIAI_CHUNG"
                     , A."SO_TAI_KHOAN"
                     , GL."MA_TAI_KHOAN_DOI_UNG"
                     , SUM(GL."GHI_NO")   AS "PHAT_SINH_NO"
                     , SUM(GL."GHI_CO")   AS "PHAT_SINH_CO"
                     , 0                  AS "SO_DU_NO"
                     , 0                  AS "SO_DU_CO"
                     , GL."MA_DOI_TUONG"
                     , GL."TEN_DOI_TUONG" AS "TEN_DOI_TUONG"
                    , 1 AS "OrderType"
                     ,Min(GL."THU_TU_TRONG_CHUNG_TU") as "THU_TU_TRONG_CHUNG_TU"
                    ,Min(GL."THU_TU_CHI_TIET_GHI_SO") as "THU_TU_CHI_TIET_GHI_SO"
                    ,Min(GL."LOAI_HACH_TOAN") As "LOAI_HACH_TOAN"


                 FROM so_cai_chi_tiet AS GL
                     INNER JOIN TMP_LIST_BRAND BR ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                     INNER JOIN DS_DOI_TUONG AO ON AO.id = GL."DOI_TUONG_ID"
                     INNER JOIN DS_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"

                 /*hoant 19.10.2017 theo cr 149455*/
                 --                 LEFT JOIN (
                 --
                 --                 SELECT V.VoucherRefDetailID,
                 --                 V."DOI_TUONG_ID",
                 --                 /*ntquang 31.01.2018 - CR137123 */
                 --                 CASE WHEN COALESCE ( TEMP.SettlementThistime"SO_TIEN", 0) >= COALESCE (V."SO_TIEN", 0) OR V1.Voucher"ID_CHUNG_TU" IS NOT NULL THEN 1 ELSE 0 END "DA_QUYET_TOAN_TAM_UNG"
                 --                                                                                                                                                      FROM
                 --                 ( SELECT T.VoucherRefDetailID
                 --                   , SUM(T.SettlementThistime"SO_TIEN") AS SettlementThistime"SO_TIEN"
                 --                                                        , SUM(T.SettlementThistime"SO_TIEN") AS SettlementThistime"SO_TIEN"
                 --                                                                                             FROM account_ex_chung_tu_nghiep_vu_khacDetailAdvancedPayment T
                 --                                                                                             INNER JOIN account_ex_chung_tu_nghiep_vu_khac A ON A."ID_CHUNG_TU" = T."ID_CHUNG_TU"
                 --                                                                                                                                             WHERE (A.DisplayOnBook = @IsWorkingWithManagementBook
                 --                                                                                                                                                    OR A.DisplayOnBook = 2
                 --
                 --                                                                                                                                                   )
                 --                 GROUP BY T.VoucherRefDetailID
                 --                 ) TEMP
                 --                   INNER JOIN [dbo].[View_AdvanceVoucher] V ON TEMP.VoucherRefDetailID = V.VoucherRefDetailID
                 --                                                          --ntquang 31.01.2018 - CR137123
                 --                                                          LEFT JOIN (
                 --                 SELECT GLD.Voucher"ID_CHUNG_TU",
                 --                 GLD.VoucherRefDetailID
                 --                 FROM account_ex_chung_tu_nghiep_vu_khacDetailAdvancedPayment GLD
                 --                      INNER JOIN account_ex_chung_tu_nghiep_vu_khac GL ON GL."ID_CHUNG_TU" = GLD."ID_CHUNG_TU"
                 --                                                                                           WHERE GL.IsExecuted = 1  ) V1 ON V1.Voucher"ID_CHUNG_TU" = V.Voucher"ID_CHUNG_TU"
                 --                                                                                                                                                               AND V1.VoucherRefDetailID = V.VoucherRefDetailID
                 --                                                                                                                                                               /*KDCHIEN 13.07.2018:242506:Bị Duplicate dữ liệu khi phiếu chi có 2 dòng dữ liệu*/
                 --                                                                                                                                                               INNER JOIN TMP_LIST_BRAND BR ON BR."CHI_NHANH_ID" = V."CHI_NHANH_ID"
                 --
                 --                                                                                                                                                                                                                     WHERE (V."TK_KHO" LIKE '141%%'
                 --                                                                                                                                                                                                                            AND (V."TK_CO" LIKE '11%%'
                 --                                                                                                                                                                                                                                 OR V."TK_CO" LIKE '136%%'
                 --                                                                                                                                                                                                                                )
                 --                                                                                                                                                                                                                           )
                 --
                 --                           ) AD ON AD."DOI_TUONG_ID" = GL."DOI_TUONG_ID" AND AD.VoucherRefDetailID=GL."CHI_TIET_ID"
                 WHERE (GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay)

                 GROUP BY
                     GL."ID_CHUNG_TU",
                     GL."MODEL_CHUNG_TU",
                     GL."NGAY_HACH_TOAN",
                     GL."NGAY_CHUNG_TU",
                     GL."SO_CHUNG_TU",
                     GL."DIEN_GIAI_CHUNG",
                     A."SO_TAI_KHOAN",
                     GL."MA_TAI_KHOAN_DOI_UNG",
                     GL."MA_DOI_TUONG",
                     GL."TEN_DOI_TUONG"
                 HAVING SUM(GL."GHI_NO") <> 0 OR SUM(GL."GHI_CO") <> 0
                ) T
            ORDER BY
                "TEN_DOI_TUONG",
                "MA_DOI_TUONG",
                "SO_TAI_KHOAN",
                 "OrderType",

                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "THU_TU_TRONG_CHUNG_TU",
                "THU_TU_CHI_TIET_GHI_SO",
                "LOAI_HACH_TOAN"

        ;


    ELSE

        INSERT INTO TMP_KET_QUA
        (
            "ID_CHUNG_TU",
            "MODEL_CHUNG_TU",
            "NGAY_HACH_TOAN",
            "NGAY_CHUNG_TU",
            "SO_CHUNG_TU", --SO_CHUNG_TU
            "DIEN_GIAI",
            "SO_TAI_KHOAN",
            "TK_DOI_UNG",
            "PHAT_SINH_NO",
            "PHAT_SINH_CO",
            "SO_DU_NO",
            "SO_DU_CO",
            "MA_DOI_TUONG",
            "TEN_DOI_TUONG",
             "OrderType"

        )
            SELECT
                "ID_CHUNG_TU"
                 ,"MODEL_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "DIEN_GIAI"
                , "SO_TAI_KHOAN"
                , "TK_DOI_UNG"
                , "PHAT_SINH_NO"
                , "PHAT_SINH_CO"
                , "SO_DU_NO"
                , "SO_DU_CO"
                , "MA_DOI_TUONG"
                , "TEN_DOI_TUONG"
                , "OrderType"

            FROM
                (SELECT
                     NULL    ::INT         AS "ID_CHUNG_TU"
                    , NULL             AS "MODEL_CHUNG_TU"
                     , NULL     ::DATE        AS "NGAY_HACH_TOAN"
                     , NULL     ::DATE         AS "NGAY_CHUNG_TU"
                     , NULL             AS "SO_CHUNG_TU"
                     , N'Số dư đầu kỳ' AS "DIEN_GIAI"
                     , A."SO_TAI_KHOAN"
                     , NULL             AS "TK_DOI_UNG"
                     , 0                AS "PHAT_SINH_NO"
                     , 0                AS "PHAT_SINH_CO"
                     , CASE WHEN SUM(GL."GHI_NO" - GL."GHI_CO") > 0
                        THEN SUM(GL."GHI_NO" - GL."GHI_CO")
                       ELSE 0
                       END              AS "SO_DU_NO"
                     , CASE WHEN SUM(GL."GHI_CO" - GL."GHI_NO") > 0
                        THEN SUM(GL."GHI_CO" - GL."GHI_NO")
                       ELSE 0
                       END              AS "SO_DU_CO"
                     , GL."MA_DOI_TUONG"
                     , GL."TEN_DOI_TUONG"
                     ,0 AS "OrderType"
                     ,0 as "THU_TU_TRONG_CHUNG_TU"
                    ,0 as "THU_TU_CHI_TIET_GHI_SO"
                    ,'0' As "LOAI_HACH_TOAN"

                 FROM so_cai_chi_tiet AS GL
                     INNER JOIN TMP_LIST_BRAND BR ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                     INNER JOIN DS_DOI_TUONG AO ON AO.id = GL."DOI_TUONG_ID"
                     INNER JOIN DS_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
                 WHERE (GL."NGAY_HACH_TOAN" < v_tu_ngay)

                 GROUP BY
                     A."SO_TAI_KHOAN",
                     GL."MA_DOI_TUONG",
                     GL."TEN_DOI_TUONG"
                 HAVING SUM(GL."GHI_NO" - GL."GHI_CO") <> 0
                 UNION ALL
                 SELECT
                     GL."ID_CHUNG_TU"
                     ,GL."MODEL_CHUNG_TU"
                     , GL."NGAY_HACH_TOAN"
                     , GL."NGAY_CHUNG_TU"
                     , GL."SO_CHUNG_TU"
                     , CASE WHEN GL."DIEN_GIAI" IS NULL
                                 OR LTRIM(GL."DIEN_GIAI") = ''
                     THEN GL."DIEN_GIAI_CHUNG"
                       ELSE GL."DIEN_GIAI"
                       END AS "DIEN_GIAI"
                     , A."SO_TAI_KHOAN"
                     , "MA_TAI_KHOAN_DOI_UNG"
                     , GL."GHI_NO"
                     , GL."GHI_CO"
                     , 0   AS "SO_DU_NO"
                     , 0   AS "SO_DU_CO"
                     , GL."MA_DOI_TUONG"
                     , GL."TEN_DOI_TUONG"
                      , 1 AS "OrderType"
                     ,GL."THU_TU_TRONG_CHUNG_TU"
                    ,GL."THU_TU_CHI_TIET_GHI_SO"
                    ,GL."LOAI_HACH_TOAN"


                 FROM so_cai_chi_tiet AS GL
                     INNER JOIN TMP_LIST_BRAND BR ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                     INNER JOIN DS_DOI_TUONG AO ON AO.id = GL."DOI_TUONG_ID"
                     INNER JOIN DS_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"

--                 LEFT JOIN (
--
--                 SELECT V.VoucherRefDetailID
--                 ,
--                 V."DOI_TUONG_ID"
--                 --ntquang 31.01.2018 - CR137123
--                 , CASE WHEN COALESCE ( TEMP.SettlementThistime"SO_TIEN", 0)>= COALESCE (V."SO_TIEN", 0) OR V1.Voucher"ID_CHUNG_TU" IS NOT NULL THEN 1 ELSE 0 END "DA_QUYET_TOAN_TAM_UNG"
--                                                                                                                                                   FROM
--                 ( SELECT T.VoucherRefDetailID
--                   , SUM(T.SettlementThistime"SO_TIEN") AS SettlementThistime"SO_TIEN"
--                                                        , SUM(T.SettlementThistime"SO_TIEN") AS SettlementThistime"SO_TIEN"
--                                                         FROM account_ex_chung_tu_nghiep_vu_khacDetailAdvancedPayment T
--                                                 INNER JOIN account_ex_chung_tu_nghiep_vu_khac A ON A."ID_CHUNG_TU" = T."ID_CHUNG_TU"
--                                                 WHERE (A.DisplayOnBook = @IsWorkingWithManagementBook
--                                                 OR A.DisplayOnBook = 2
--
--                                                                                                                                                   )
--                 GROUP BY T.VoucherRefDetailID
--                 ) TEMP
--                   INNER JOIN [dbo].[View_AdvanceVoucher] V ON TEMP.VoucherRefDetailID = V.VoucherRefDetailID
--                                                          --ntquang 31.01.2018 - CR137123
--                                                          LEFT JOIN (
--                 SELECT GLD.Voucher"ID_CHUNG_TU",
--                 GLD.VoucherRefDetailID
--                 FROM account_ex_chung_tu_nghiep_vu_khacDetailAdvancedPayment GLD
--                      INNER JOIN account_ex_chung_tu_nghiep_vu_khac GL ON GL."ID_CHUNG_TU" = GLD."ID_CHUNG_TU"
--                                                                                           WHERE GL.IsExecuted = 1  ) V1 ON V1.Voucher"ID_CHUNG_TU" = V.Voucher"ID_CHUNG_TU"
--                                                                                                                                                               AND V1.VoucherRefDetailID = V.VoucherRefDetailID
--                                                                                                                                                               /*KDCHIEN 13.07.2018:242506:Bị Duplicate dữ liệu khi phiếu chi có 2 dòng dữ liệu*/
--
--                                                                                                                                                               INNER JOIN TMP_LIST_BRAND BR ON BR."CHI_NHANH_ID" = V."CHI_NHANH_ID"
--
--                                                                                                                                                                                                                     WHERE (V."TK_KHO" LIKE '141%%'
--                                                                                                                                                                                                                            AND (V."TK_CO" LIKE '11%%'
--                                                                                                                                                                                                                                 OR V."TK_CO" LIKE '136%%'
--                                                                                                                                                                                                                                )
--                                                                                                                                                                                                                           )
--
--                           ) AD ON AD."DOI_TUONG_ID" = GL."DOI_TUONG_ID" AND AD.VoucherRefDetailID=GL."CHI_TIET_ID"


                          WHERE (GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay )

                AND ( GL."GHI_NO" <> 0
                      OR GL."GHI_CO" <> 0
                    )
                ) T
            ORDER BY
                 "TEN_DOI_TUONG",
                "MA_DOI_TUONG",
                "SO_TAI_KHOAN",
                 "OrderType",

                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "THU_TU_TRONG_CHUNG_TU",
                "THU_TU_CHI_TIET_GHI_SO",
                "LOAI_HACH_TOAN"
        ;


 END IF
    ;

        FOR rec IN
        SELECT *
        FROM TMP_KET_QUA
        ORDER BY
            RowNum

        LOOP

            SELECT CASE WHEN MA_DOI_TUONG_TMP <> rec."MA_DOI_TUONG" OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                THEN rec."SO_DU_NO" - rec."SO_DU_CO" + rec."PHAT_SINH_NO" - rec."PHAT_SINH_CO"
                                  ELSE SO_DU_CUOI_KY_TMP + rec."SO_DU_NO" - rec."SO_DU_CO" + rec."PHAT_SINH_NO" - rec."PHAT_SINH_CO"
                                  END
                INTO SO_DU_CUOI_KY_TMP

        ;


                rec. "SO_DU_NO" =    CASE WHEN SO_DU_CUOI_KY_TMP > 0
                                    THEN SO_DU_CUOI_KY_TMP
                                    ELSE 0
                                    END;
                UPDATE TMP_KET_QUA
                    SET "SO_DU_NO" = rec."SO_DU_NO"
                    WHERE  RowNum =rec.RowNum ;


                rec. "SO_DU_CO" = CASE WHEN SO_DU_CUOI_KY_TMP < 0
                                THEN - SO_DU_CUOI_KY_TMP
                               ELSE 0
                               END;
                 UPDATE TMP_KET_QUA
                    SET "SO_DU_CO" = rec."SO_DU_CO"
                    WHERE  RowNum =rec.RowNum ;

                SELECT
                    rec."MA_DOI_TUONG" INTO MA_DOI_TUONG_TMP
                    FROM TMP_KET_QUA ;
                UPDATE TMP_KET_QUA
                    SET "MA_DOI_TUONG" = rec."MA_DOI_TUONG"
                    WHERE RowNum =rec.RowNum;

                SELECT
                    rec."SO_TAI_KHOAN" INTO  SO_TAI_KHOAN_TMP
                    FROM TMP_KET_QUA;
                UPDATE TMP_KET_QUA
                    SET "SO_TAI_KHOAN" =rec."SO_TAI_KHOAN"
                    WHERE RowNum =rec.RowNum;



            END LOOP ;




END $$
;
 SELECT
                RowNum
                , R."ID_CHUNG_TU" AS "ID_GOC"
                , R."MODEL_CHUNG_TU" AS "MODEL_GOC"
                , "MA_DOI_TUONG"
                , "TEN_DOI_TUONG"  as "TEN_DOI_TUONG"
                , "SO_TAI_KHOAN"   as "TK_CO_ID"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"

                , "DIEN_GIAI"
                , "TK_DOI_UNG"
                , "PHAT_SINH_NO" as "NO_PHAT_SINH"
                , "PHAT_SINH_CO"  as "CO_PHAT_SINH"
                , "SO_DU_NO"  as "NO_DU"
                , "SO_DU_CO"  as "CO_DU"

            FROM TMP_KET_QUA R

             LEFT JOIN lay_chung_tu_chi V ON V."ID_CHUNG_TU" = R."ID_CHUNG_TU" AND V."MODEL_CHUNG_TU" = R."MODEL_CHUNG_TU"



            ORDER BY RowNum 
            
            OFFSET %(offset)s
            LIMIT %(limit)s;



        """
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU = self.get_vntime('TU')
        DEN = self.get_vntime('DEN')
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan =''
        if TAI_KHOAN_ID:
            if TAI_KHOAN_ID == -1 :
                tai_khoan ='Tất cả'
            else:
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID).SO_TAI_KHOAN

        LOAI_DOI_TUONG = self.get_context('LOAI_DOI_TUONG')
        loai_doi_tuong = ''
        if LOAI_DOI_TUONG:
            if LOAI_DOI_TUONG == '0':
                loai_doi_tuong = 'Tất cả'
            elif LOAI_DOI_TUONG == '1':
                loai_doi_tuong = 'Khách hàng'
            elif LOAI_DOI_TUONG == '3':
                loai_doi_tuong = 'Nhân viên'
            elif LOAI_DOI_TUONG == '2':
                loai_doi_tuong = 'Nhà cung cấp'

        param = 'Tài khoản: %s; Loại đối tượng: %s; Từ : %s đến  %s' % (tai_khoan, loai_doi_tuong, TU, DEN)
        action = self.env.ref('bao_cao.open_report__so_chi_tiet_tai_khoan_theo_doi_tuong').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action

    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
        DROP VIEW IF EXISTS lay_chung_tu_chi
    ;
    CREATE or REPLACE VIEW lay_chung_tu_chi as (--View_CAVoucherIsSettlementAdvanced


	SELECT
            CAP."id" AS "ID_CHUNG_TU",
            'account.ex.phieu.thu.chi' as "MODEL_CHUNG_TU"


    FROM    account_ex_phieu_thu_chi CAP
            WHERE CAP."CHUNG_TU_NGHIEP_VU_KHAC_ID" IS NOT NULL
            AND CAP."LOAI_PHIEU" ='PHIEU_CHI' AND CAP."TYPE_NH_Q" = 'QUY'
    UNION ALL
    SELECT
           CAP."id" AS "ID_CHUNG_TU",
        'account.ex.phieu.thu.chi' as "MODEL_CHUNG_TU"
    FROM    account_ex_phieu_thu_chi CAP
            WHERE CAP."CHUNG_TU_NGHIEP_VU_KHAC_ID" IS NOT NULL
            AND CAP."LOAI_PHIEU" ='PHIEU_THU' AND CAP."TYPE_NH_Q" = 'QUY'
        )


        """)