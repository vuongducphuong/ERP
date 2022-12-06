# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_CHI_TIET_BAN_HANG(models.Model):
    _name = 'bao.cao.so.chi.tiet.ban.hang'
    _auto = False
    
    THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'), ('NHAN_VIEN', 'Nhân viên'), ], string='Thống kê theo', help='Thống kê theo', default ='KHONG_CHON', required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True, default=lambda self: self.get_chi_nhanh())
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc ', help='Bao gồm số liệu chi nhánh phụ thuộc ', default ='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày ',required=True)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True)
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    NHOM_KH_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải ', help='Diễn giải ')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='Diễn giải chung')
    MA_KHACH_HANG = fields.Char(string='Mã khách hàng', help='Mã khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    TONG_SO_LUONG_BAN = fields.Float(string='Số lượng bán', help='Số lượng bán', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA') )
    DOANH_SO_BAN = fields.Float(string='Doanh số bán', help='Doanh số bán',digits= decimal_precision.get_precision('VND'))
    CHIET_KHAU = fields.Float(string='Chiết khấu', help='Doanh số bán',digits= decimal_precision.get_precision('VND'))
    TONG_SO_LUONG_TRA_LAI = fields.Float(string='Số lượng trả lại', help='Số lượng trả lại', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_TRA_LAI = fields.Float(string='Giá trị trả lại', help='Giá trị trả lại',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_GIAM_GIA = fields.Float(string='Giá trị giảm giá', help='Giá trị trả lại',digits= decimal_precision.get_precision('VND'))
    SO_LUONG_BAN = fields.Float(string='Số lượng bán', help='Số lượng bán', digits=decimal_precision.get_precision('SO_LUONG'))
    TEN_NHAN_VIEN_BAN_HANG =  fields.Char(string='Tên nhân viên bán hàng ', help='Tên nhân viên bán hàng')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    DON_GIA_VON = fields.Float(string='Đơn giá vốn', help='Đơn giá vốn',digits= decimal_precision.get_precision('DON_GIA') )
    GIA_VON = fields.Float(string='Giá vốn', help='Giá vốn')
    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa', string='Chọn sản phẩm')
    SAN_PHAM_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa', string='Sản phẩm')
    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner', domain=[('LA_KHACH_HANG', '=', True)], string='Chọn KH')
    KHACH_HANG_IDS = fields.One2many('res.partner', domain=[('LA_KHACH_HANG', '=', True)], string='Khách hàng')
    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')
    NHAN_VIEN_IDS = fields.One2many('res.partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Nhân viên')
    MA_PC_NHOM_VTHH = fields.Char()
    MA_PC_NHOM_KH = fields.Char()
    MA_NHOM_KH  = fields.Char(string='Mã nhóm khách hàng', help='Mã nhóm khách hàng')
    TEN_NHOM_KH  = fields.Char(string='Tên nhóm khách hàng', help='Tên nhóm khách hàng')

    # Onchange cho các field relation Many2many-One2many
    @api.onchange('SAN_PHAM_IDS')
    def _onchange_SAN_PHAM_IDS(self):
        self.SAN_PHAM_MANY_IDS =self.SAN_PHAM_IDS.ids

    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        self.SAN_PHAM_IDS =self.SAN_PHAM_MANY_IDS.ids

    @api.onchange('KHACH_HANG_IDS')
    def _onchange_KHACH_HANG_IDS(self):
        self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS.ids

    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.KHACH_HANG_IDS =self.KHACH_HANG_MANY_IDS.ids

    @api.onchange('NHAN_VIEN_IDS')
    def _onchange_NHAN_VIEN_IDS(self):
        self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS.ids

    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        self.NHAN_VIEN_IDS =self.NHAN_VIEN_MANY_IDS.ids
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.onchange('NHOM_KH_ID')
    def update_KHACH_HANG_IDS(self):
        # Khi thay đổi NHOM_KH_ID thì clear hết KH đã chọn
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KH_ID.MA_PHAN_CAP
      

    @api.onchange('NHOM_VTHH_ID')
    def update_SAN_PHAM_IDS(self):
        # Khi thay đổi NHOM_VTHH_ID thì clear hết VTHH đã chọn
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP
      

    @api.onchange('DON_VI_ID')
    def update_NHAN_VIEN_IDS(self):
        # Khi thay đổi DON_VI_ID thì clear hết NV đã chọn
        self.NHAN_VIEN_MANY_IDS = []
       
    ### START IMPLEMENTING CODE ###

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    def _validate(self):
        params = self._context

        THONG_KE_THEO = params.get('THONG_KE_THEO')
        # SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')
        NHAN_VIEN_IDS = params.get('NHAN_VIEN_MANY_IDS')
        TU_NGAY = params.get('TU_NGAY')
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params.get('DEN_NGAY')
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        if not TU_NGAY:
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        if not DEN_NGAY:
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        if TU_NGAY_F > DEN_NGAY_F:
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')
        if THONG_KE_THEO == 'NHAN_VIEN' and not (NHAN_VIEN_IDS or params.get('CHON_TAT_CA_NHAN_VIEN')):
        # kiểm tra danh dách nhân viên bị trống 
            raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params.get('THONG_KE_THEO')
        # TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        CHI_NHANH_ID = params.get('CHI_NHANH_ID')
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params.get('BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC')
        DON_VI_ID = params.get('DON_VI_ID')
        TU_NGAY = params.get('TU_NGAY')
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params.get('DEN_NGAY')
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHAN_VIEN_ID = params.get('NHAN_VIEN_ID')
        NHOM_VTHH_ID = params.get('NHOM_VTHH_ID')
        NHOM_KH_ID = params.get('NHOM_KH_ID')
        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
        MA_PC_NHOM_KH = params.get('MA_PC_NHOM_KH')
        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')
        if params.get('CHON_TAT_CA_NHAN_VIEN'):
            domain = [('LA_NHAN_VIEN','=', True)]
            if DON_VI_ID:
                domain += [('DON_VI_ID','=', DON_VI_ID)]
            NHAN_VIEN_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHAN_VIEN_IDS =  params.get('NHAN_VIEN_MANY_IDS')
        
        if params.get('CHON_TAT_CA_KHACH_HANG'):
            domain = [('LA_KHACH_HANG','=', True)]
            if MA_PC_NHOM_KH:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
            KHACH_HANG_IDS =  self.env['res.partner'].search(domain).ids
        else:
            KHACH_HANG_IDS = params.get('KHACH_HANG_MANY_IDS')
        
        params = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'CHI_NHANH_ID' : CHI_NHANH_ID,
            'SAN_PHAMS' : SAN_PHAM_IDS or None,
            'KHACH_HANGS' : KHACH_HANG_IDS or None,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : int(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC == 'True'),
            'DON_VI_ID' : DON_VI_ID,
            'NHAN_VIEN_ID' : NHAN_VIEN_ID,
            'NHOM_KH_ID' : NHOM_KH_ID,
            'NHAN_VIEN_IDS' : NHAN_VIEN_IDS or None,
            'limit': limit,
            'offset': offset,
            }

        if (THONG_KE_THEO == 'KHONG_CHON'):
            return self._lay_bao_cao_khong_chon(params)
        else:
            return self._lay_bao_cao_nhan_vien(params)    
        

    #lấy báo cáo thống kê theo không chọn
    def _lay_bao_cao_khong_chon(self, params):      
        record = []
        cr = self.env.cr      
        query = """

                    DO LANGUAGE plpgsql $$
                    DECLARE
                    tu_ngay                     DATE := %(TU_NGAY)s;
                    den_ngay                    DATE := %(DEN_NGAY)s;
                    chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;
                    bao_gom_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
                    don_vi_id INTEGER := %(DON_VI_ID)s;
                    nhan_vien_id INTEGER := %(NHAN_VIEN_ID)s;
                   
                    nhom_kh_id                  INTEGER := %(NHOM_KH_ID)s;
                    misa_code                   VARCHAR(127);
                    LIST_DON_VI                 VARCHAR(500) := '(,';

                    BEGIN
                    DROP TABLE IF EXISTS TMP_DOI_TUONG
                ;
            
                CREATE TEMP TABLE TMP_DOI_TUONG (
                    "DOI_TUONG_ID"         INTEGER,
                    "LIST_TEN_NHOM_KH_NCC" VARCHAR(500)
                )
                ;
            
            
                DROP TABLE IF EXISTS TMP_VTHH
                ;
            
                CREATE TEMP TABLE TMP_VTHH (
                    "MA_HANG_ID" INTEGER
            
                )
                ;
            
                IF (%(SAN_PHAMS)s) IS NOT NULL
                THEN
                    INSERT INTO TMP_VTHH (
                        SELECT "id"
                        FROM danh_muc_vat_tu_hang_hoa T
                        WHERE (id = any( %(SAN_PHAMS)s))
                    )
                    ;
                ELSE
                    INSERT INTO TMP_VTHH (
                        SELECT "id"
                        FROM danh_muc_vat_tu_hang_hoa II)
                    ;
                END IF
                ;
            
            
                --   Trường hợp nếu không tích chọn có nghĩa là lấy hết khách hàng
                IF ( %(KHACH_HANGS)s)  IS NOT NULL
                THEN
                    INSERT INTO TMP_DOI_TUONG (
                        SELECT
                            id
                            , "LIST_TEN_NHOM_KH_NCC"
                        FROM res_partner
                        WHERE (id = any( %(KHACH_HANGS)s))
                    )
                    ;
                ELSE
                    --     trường hợp nếu không chọn nhóm khách hàng
                    IF nhom_kh_id IS NULL
                    THEN
                        INSERT INTO TMP_DOI_TUONG (
                            SELECT
                                AO.id
                                , "LIST_TEN_NHOM_KH_NCC"
                            FROM res_partner AO
                        )
                        ;
                    ELSE
                        --       trường hợp nếu chọn nhóm khách hàng là khác
                        IF nhom_kh_id <> -2
                        THEN
                            misa_code = (SELECT "MA_PHAN_CAP"
                                         FROM danh_muc_nhom_khach_hang_nha_cung_cap
                                         WHERE id = nhom_kh_id)
                            ;
            
                            INSERT INTO TMP_DOI_TUONG (
                                SELECT
                                    DISTINCT
                                    AO.id
                                    , "LIST_TEN_NHOM_KH_NCC"
                                FROM res_partner AO
                                    INNER JOIN danh_muc_nhom_khach_hang_nha_cung_cap AOG
                                        ON AO."LIST_MPC_NHOM_KH_NCC" LIKE '%%;' || AOG."MA_PHAN_CAP" || ';%%'
                                WHERE AOG."MA_PHAN_CAP" LIKE misa_code || '%%'
                            )
                            ;
                        ELSE
                            INSERT INTO TMP_DOI_TUONG (
                                SELECT
                                    id
                                    , "LIST_TEN_NHOM_KH_NCC"
                                FROM res_partner AO
                                WHERE AO."LIST_TEN_NHOM_KH_NCC" IS NULL OR ao."LIST_TEN_NHOM_KH_NCC" = ''
                            )
                            ;
                        END IF
                        ;
                    END IF
                    ;
                END IF
                ;
            
                SELECT string_agg(CAST("id" AS VARCHAR(127)), ',')
                INTO LIST_DON_VI
                FROM
                        LAY_DS_DON_VI(don_vi_id, bao_gom_chi_nhanh_phu_thuoc)
            
                ;
            
                LIST_DON_VI = '(,' || LIST_DON_VI || ',)'
            
            
                ;
            
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
                 DROP TABLE IF EXISTS TMP_KET_QUA1
                    ;
            
                IF (%(KHACH_HANGS)s) IS NULL
                THEN
            
                    CREATE TEMP TABLE TMP_KET_QUA
                        AS
                            SELECT
                                row_number()
                                OVER (
                                    ORDER BY "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU" ) AS "ROWNUM"
                                , SL."ID_CHUNG_TU"
                                , SL."MODEL_CHUNG_TU"
                                , SL."NGAY_HACH_TOAN"
                                , -- Ngày hạch toán
                                SL."NGAY_CHUNG_TU"
                                , -- Ngày chứng từ
                                SL."SO_CHUNG_TU"
                                , -- Số chứng từ
                                SL."NGAY_HOA_DON"
                                , -- Ngày hóa đơn
                                SL."SO_HOA_DON"
                                , -- Số hóa đơn
                                SL."DIEN_GIAI_CHUNG"
                                , -- Diễn giải thông tin chung
                                SL."DIEN_GIAI"
                                , -- Diễn giải chi tiết
                                SL."MA_DOI_TUONG"
                                , -- Mã KH trên chứng từ
                                SL."TEN_DOI_TUONG"
                                , -- Tên KH trên chứng từ
                                SL."MA_HANG"
                                , -- Mã hàng
                                SL."TEN_HANG"
                                , -- Tên hàng
                                UN."DON_VI_TINH"
                                , -- Tên ĐVT
                                SL."SO_LUONG"                                                   AS "SO_LUONG"
                                , -- Tổng Số lượng bán
                                SL."DON_GIA"
                                , -- Đơn giá quy đổi
                                coalesce(SL."SO_TIEN", 0)                                       AS "TONG_TIEN_THANH_TOAN"
                                , -- Tổng tiền thanh toán
                                SL."SO_TIEN_CHIET_KHAU"
                                , SL."SO_LUONG_TRA_LAI"
                                , SL."SO_TIEN_TRA_LAI"
                                , SL."SO_TIEN_GIAM_TRU"
                                , SL."LOAI_CHUNG_TU"
                                , SL."CHI_TIET_ID"
                                , SL."CHI_TIET_MODEL"
                                , AO."LIST_MA_NHOM_KH_NCC"
                                , AO."LIST_TEN_NHOM_KH_NCC"
                            FROM so_ban_hang_chi_tiet AS SL
                                INNER JOIN (SELECT *
                                            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc)) AS TLB
                                    ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                INNER JOIN TMP_VTHH AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                                LEFT JOIN danh_muc_don_vi_tinh AS UN ON SL."DVT_ID" = UN.id
                                -- Danh mục ĐVT -> ĐVT
                                LEFT JOIN danh_muc_to_chuc AS OU ON SL."DON_VI_ID" = OU.id
                                LEFT JOIN res_partner AS AO ON SL."DOI_TUONG_ID" = AO.id
                            WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                  AND (don_vi_id IS NULL
                                       OR (
                                           LIST_DON_VI LIKE '%%'
                                                            || CAST(SL."DON_VI_ID" AS VARCHAR(127))
                                                            || '%%'
            
            
                                           AND don_vi_id IS NOT NULL
                                       )
                                  )
                                  AND (nhan_vien_id IS NULL
                                       OR (SL."NHAN_VIEN_ID" = nhan_vien_id
                                           AND nhan_vien_id IS NOT NULL
                                       )
                                  )
                                  AND (SL."SO_LUONG" <> 0
                                       OR SL."SO_LUONG_THEO_DVT_CHINH" <> 0
                                       OR SL."SO_TIEN" <> 0
                                       OR SL."SO_TIEN_CHIET_KHAU" <> 0
                                       OR SL."SO_LUONG_TRA_LAI" <> 0
                                       OR SL."SO_LUONG_THEO_DVT_CHINH" <> 0
                                       OR SL."SO_TIEN_TRA_LAI" <> 0
                                       OR SL."SO_TIEN_GIAM_TRU" <> 0
                                       OR SL."SO_TIEN_VAT" <> 0
                                       OR SL."SO_TIEN" <> 0
                                  )
                    ;
            
            
                ELSE
            
                    CREATE TEMP TABLE TMP_KET_QUA1
                        AS
                            SELECT
                                row_number()
                                OVER (
                                    ORDER BY "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU" ) AS "ROWNUM"
                                , SL."ID_CHUNG_TU"
                                , SL."MODEL_CHUNG_TU"
                                , SL."NGAY_HACH_TOAN"
                                , -- Ngày hạch toán
                                SL."NGAY_CHUNG_TU"
                                , -- Ngày chứng từ
                                SL."SO_CHUNG_TU"
                                , -- Số chứng từ
                                SL."NGAY_HOA_DON"
                                , -- Ngày hóa đơn
                                SL."SO_HOA_DON"
                                , -- Số hóa đơn
                                SL."DIEN_GIAI_CHUNG"
                                , -- Diễn giải thông tin chung
                                SL."DIEN_GIAI"
                                , -- Diễn giải chi tiết
                                SL."MA_DOI_TUONG"
                                , -- Mã KH trên chứng từ
                                SL."TEN_DOI_TUONG"
                                , -- Tên KH trên chứng từ
                                SL."MA_HANG"
                                , -- Mã hàng
                                SL."TEN_HANG"
                                , -- Tên hàng
                                UN."DON_VI_TINH"
                                , -- Tên ĐVT
                                SL."SO_LUONG"                                                   AS "SO_LUONG"
                                , -- Tổng Số lượng bán
                                SL."DON_GIA"
                                , -- Đơn giá quy đổi
                                SL."SO_TIEN"                                                    AS "TONG_TIEN_THANH_TOAN"
                                , -- Tổng tiền thanh toán
                                SL."SO_TIEN_CHIET_KHAU"
                                , SL."SO_LUONG_TRA_LAI"
                                , SL."SO_TIEN_TRA_LAI"
                                , SL."SO_TIEN_GIAM_TRU"
                                , SL."LOAI_CHUNG_TU"
                                , SL."CHI_TIET_ID"
                                , SL."CHI_TIET_MODEL"
                                , AO."LIST_MA_NHOM_KH_NCC"
                                , LAOI."LIST_TEN_NHOM_KH_NCC"
                            FROM so_ban_hang_chi_tiet AS SL
                                INNER JOIN (SELECT *
                                            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc)) AS TLB
                                    ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                                INNER JOIN TMP_DOI_TUONG AS LAOI ON SL."DOI_TUONG_ID" = LAOI."DOI_TUONG_ID"
                                INNER JOIN TMP_VTHH AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                                INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON LII."MA_HANG_ID" = II.id
                                LEFT JOIN danh_muc_don_vi_tinh AS UN ON SL."DVT_ID" = UN.id
                                -- Danh mục ĐVT -> ĐVT
                                LEFT JOIN danh_muc_to_chuc AS OU ON SL."DVT_ID" = OU.id
            					LEFT JOIN res_partner AS AO ON SL."DOI_TUONG_ID" = AO.id
                            WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                  AND (don_vi_id IS NULL
                                       OR (
                                           LIST_DON_VI LIKE '%%'
                                                            || CAST(SL."DON_VI_ID" AS VARCHAR(127))
                                                            || '%%'
            
            
                                           AND don_vi_id IS NOT NULL
                                       )
                                  )
                                  AND (nhan_vien_id IS NULL
                                       OR (SL."NHAN_VIEN_ID" = nhan_vien_id
                                           AND nhan_vien_id IS NOT NULL
                                       )
                                  )
                                  AND (SL."SO_LUONG" <> 0
                                       OR SL."SO_LUONG_THEO_DVT_CHINH" <> 0
                                       OR SL."SO_TIEN" <> 0
                                       OR SL."SO_TIEN_CHIET_KHAU" <> 0
                                       OR SL."SO_LUONG_TRA_LAI" <> 0
                                       OR SL."SO_TIEN_TRA_LAI" <> 0
                                       OR SL."SO_TIEN_GIAM_TRU" <> 0
                                       OR SL."SO_TIEN_VAT" <> 0
                                  )
                    ;
                END IF
                ;
            
                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;
            
                IF (%(KHACH_HANGS)s) IS NULL -- Nếu lấy tất
                THEN
            
            
                    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                        AS
                            SELECT
                                R.*
                                , CASE WHEN R."LOAI_CHUNG_TU" IN ('3540', '3541', '3542', '3543', '3544',
                                                                  '3545')
                                THEN COALESCE(L."DON_GIA", 0)
                                  ELSE COALESCE(IL."DON_GIA", 0)
                                  END AS "DON_GIA_VON"
                                , CASE WHEN R."LOAI_CHUNG_TU" IN ('3540', '3541', '3542', '3543', '3544',
                                                                  '3545')
                                THEN -1 * COALESCE(L."SO_TIEN_NHAP", 0)
                                  ELSE COALESCE(IL."SO_TIEN_XUAT", 0)
                                  END AS "GIA_VON"
            
                            FROM TMP_KET_QUA R
                                LEFT JOIN sale_ex_document_outward_detail_ref RD
                                    ON R."CHI_TIET_ID" = RD."sale_document_line_id" AND R."CHI_TIET_MODEL" = 'sale.document.line'
                                LEFT JOIN so_kho_chi_tiet IL ON RD."stock_ex_nhap_xuat_kho_chi_tiet_id" = IL."CHI_TIET_ID" AND
                                                                IL."CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
            
                                LEFT JOIN sale_ex_return_inward_detail_ref SR
                                    ON R."CHI_TIET_ID" = Sr."sale_ex_tra_lai_hang_ban_chi_tiet_id" AND
                                       R."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet'
                                LEFT JOIN so_kho_chi_tiet L ON L."CHI_TIET_ID" = SR."stock_ex_nhap_xuat_kho_chi_tiet_id" AND
                                                               L."CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
            
                            ORDER BY "ROWNUM"
                    ;
            
            
                ELSE
            
                    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                        AS
            
                            SELECT
                                R.*
                                , CASE WHEN R."LOAI_CHUNG_TU" IN ('3540', '3541', '3542', '3543', '3544',
                                                                  '3545')
                                THEN COALESCE(L."DON_GIA", 0)
                                  ELSE COALESCE(IL."DON_GIA", 0)
                                  END AS "DON_GIA_VON"
                                , CASE WHEN R."LOAI_CHUNG_TU" IN ('3540', '3541', '3542', '3543', '3544',
                                                                  '3545')
                                THEN -1 * COALESCE(L."SO_TIEN_NHAP", 0)
                                  ELSE COALESCE(IL."SO_TIEN_XUAT", 0)
                                  END AS "GIA_VON"
            
                            FROM TMP_KET_QUA1 R
                                LEFT JOIN sale_ex_document_outward_detail_ref RD
                                    ON R."CHI_TIET_ID" = RD."sale_document_line_id" AND R."CHI_TIET_MODEL" = 'sale.document.line'
                                LEFT JOIN so_kho_chi_tiet IL ON RD."stock_ex_nhap_xuat_kho_chi_tiet_id" = IL."CHI_TIET_ID" AND
                                                                IL."CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
            
                                LEFT JOIN sale_ex_return_inward_detail_ref SR
                                    ON R."CHI_TIET_ID" = Sr."sale_ex_tra_lai_hang_ban_chi_tiet_id" AND
                                       R."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet'
                                LEFT JOIN so_kho_chi_tiet L ON L."CHI_TIET_ID" = SR."stock_ex_nhap_xuat_kho_chi_tiet_id" AND
                                                               L."CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
            
            
                            ORDER BY "ROWNUM"
                    ;
            
                END IF
                ;
            
            
            END $$
            ;
            
            SELECT *
            FROM TMP_KET_QUA_CUOI_CUNG
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
                'NGAY_HOA_DON': line.get('NGAY_HOA_DON', ''),
                'SO_HOA_DON': line.get('SO_HOA_DON', ''),
                'DIEN_GIAI_CHUNG': line.get('DIEN_GIAI_CHUNG', ''),
                'MA_KHACH_HANG': line.get('MA_DOI_TUONG', ''),
                'TEN_KHACH_HANG': line.get('TEN_DOI_TUONG', ''),
                'MA_HANG': line.get('MA_HANG', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT': line.get('DON_VI_TINH', ''),
                'TONG_SO_LUONG_BAN': line.get('SO_LUONG', ''),
                'DON_GIA': line.get('DON_GIA', ''),
                'DOANH_SO_BAN': line.get('TONG_TIEN_THANH_TOAN', ''),
                'CHIET_KHAU': line.get('SO_TIEN_CHIET_KHAU', ''),
                'TONG_SO_LUONG_TRA_LAI': line.get('SO_LUONG_TRA_LAI', ''),
                'GIA_TRI_TRA_LAI': line.get('SO_TIEN_TRA_LAI', ''),
                'GIA_TRI_GIAM_GIA': line.get('SO_TIEN_GIAM_TRU', ''),
                'TEN_NHAN_VIEN_BAN_HANG': line.get('TEN_NHAN_VIEN', ''),
                'ID_GOC': line.get('ID_CHUNG_TU', ''),
                'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
                'DON_GIA_VON': line.get('DON_GIA_VON', ''),
                'GIA_VON': line.get('GIA_VON', ''),
                'DIEN_GIAI': line.get('DIEN_GIAI', ''),
                'MA_NHOM_KH': line.get('LIST_MA_NHOM_KH_NCC', ''),
                'TEN_NHOM_KH': line.get('LIST_TEN_NHOM_KH_NCC', ''),
                })
        return record
    
    # lấy báo cáo nhân viên    
    def _lay_bao_cao_nhan_vien(self, params):      
        record = []
        cr = self.env.cr

        query = """

                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                     DATE := %(TU_NGAY)s;
                den_ngay                    DATE := %(DEN_NGAY)s;
                chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;
                bao_gom_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                BEGIN
                DROP TABLE IF EXISTS TMP_NHAN_VIEN;
                CREATE TEMP TABLE TMP_NHAN_VIEN (
                    "NHAN_VIEN_ID"         INTEGER,
                    "TEN_NHAN_VIEN" VARCHAR(127),
                    "DON_VI_ID" INTEGER,
                    "TEN_DON_VI" VARCHAR(127)
                );

                INSERT INTO TMP_NHAN_VIEN(
                    SELECT AO.id,
                        AO."HO_VA_TEN",
                        OU.id,
                        OU."TEN_DON_VI"
                    FROM res_partner AO
                    LEFT JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU.id
                    WHERE AO.id = any (%(NHAN_VIEN_IDS)s) 
                );


                    DROP TABLE IF EXISTS TMP_KET_QUA
            ;
        
            CREATE TEMP TABLE TMP_KET_QUA
                AS
                    SELECT
                        row_number()
                        OVER (
                            ORDER BY SL."TEN_NHAN_VIEN", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU" ) AS "ROWNUM"
                        , SL."ID_CHUNG_TU"
                        , SL."MODEL_CHUNG_TU"
                        , SL."NGAY_HACH_TOAN"
                        , -- Ngày hạch toán
                        SL."NGAY_CHUNG_TU"
                        , -- Ngày chứng từ
                        SL."SO_CHUNG_TU"
                        , -- Số chứng từ
                        SL."NGAY_HOA_DON"
                        , -- Ngày hóa đơn
                        SL."SO_HOA_DON"
                        , -- Số hóa đơn
                        SL."DIEN_GIAI_CHUNG"
                        , -- Diễn giải thông tin chung
                        SL."MA_HANG"
                        , -- Mã hàng
                        SL."TEN_HANG"
                        , -- Tên hàng
                        UN."DON_VI_TINH"
                        , -- Tên ĐVT
                        SL."SO_LUONG"
                        , -- Số lượng
                        SL."DON_GIA"
                        , -- Đơn giá quy đổi
                        SL."SO_TIEN"                                                                        AS "TONG_TIEN_THANH_TOAN"
                        , SL."SO_TIEN_CHIET_KHAU"
                        , -- Tỷ lệ chuyển đổi
                        SL."SO_LUONG_TRA_LAI"
                        , -- Số lượng theo ĐVC
                        SL."SO_TIEN_TRA_LAI"
                        , -- Đơn giá theo ĐVC
                        SL."SO_TIEN_GIAM_TRU"
                        , SL."NHAN_VIEN_ID"
                        , SL."MA_NHAN_VIEN"
                        , SL."TEN_NHAN_VIEN"
        
                        , SL."LOAI_CHUNG_TU"
                        , SL."CHI_TIET_ID"
                        , SL."CHI_TIET_MODEL"
                    FROM so_ban_hang_chi_tiet AS SL
                        INNER JOIN (SELECT *
                                    FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc)) AS TLB
                            ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN TMP_NHAN_VIEN AS E ON E."NHAN_VIEN_ID" = SL."NHAN_VIEN_ID"
                        LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON II.id = SL."MA_HANG_ID"
                        LEFT JOIN danh_muc_don_vi_tinh AS UN ON SL."DVT_ID" = UN.id
                        -- Danh mục ĐVT -> ĐVT
                        LEFT JOIN danh_muc_to_chuc AS OU ON SL."DON_VI_ID" = OU.id
                        LEFT JOIN res_partner AS AO ON SL."DOI_TUONG_ID" = AO.id
        
                    WHERE SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                          AND (SL."SO_LUONG" <> 0
                               OR SL."SO_LUONG_THEO_DVT_CHINH" <> 0
                               OR SL."SO_TIEN" <> 0
                               OR SL."SO_TIEN_CHIET_KHAU" <> 0
                               OR SL."SO_LUONG_TRA_LAI" <> 0
                               OR SL."SO_TIEN_TRA_LAI" <> 0
                               OR SL."SO_TIEN_GIAM_TRU" <> 0
                               OR SL."SO_TIEN_VAT" <> 0
                          )
            ;
        
            DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
            ;
        
        
            CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS
                    SELECT
                        R.*
                        , CASE WHEN R."LOAI_CHUNG_TU" IN ('3540', '3541', '3542', '3543', '3544',
                                                          '3545')
                        THEN COALESCE(L."DON_GIA", 0)
                          ELSE COALESCE(IL."DON_GIA", 0)
                          END AS "DON_GIA_VON"
                        , CASE WHEN R."LOAI_CHUNG_TU" IN ('3540', '3541', '3542', '3543', '3544',
                                                          '3545')
                        THEN -1 * COALESCE(L."SO_TIEN_NHAP", 0)
                          ELSE COALESCE(IL."SO_TIEN_XUAT", 0)
                          END AS "GIA_VON"
        
                    FROM TMP_KET_QUA R
                        LEFT JOIN sale_ex_document_outward_detail_ref RD
                            ON R."CHI_TIET_ID" = RD."sale_document_line_id" AND R."CHI_TIET_MODEL" = 'sale.document.line'
                        LEFT JOIN so_kho_chi_tiet IL ON RD."stock_ex_nhap_xuat_kho_chi_tiet_id" = IL."CHI_TIET_ID" AND
                                                        IL."CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
        
                        LEFT JOIN sale_ex_return_inward_detail_ref SR
                            ON R."CHI_TIET_ID" = Sr."sale_ex_tra_lai_hang_ban_chi_tiet_id" AND
                               R."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet'
                        LEFT JOIN so_kho_chi_tiet L ON L."CHI_TIET_ID" = SR."stock_ex_nhap_xuat_kho_chi_tiet_id" AND
                                                       L."CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
        
                    ORDER BY "ROWNUM"
            ;
        
        END $$
        ;
        
        SELECT *
        FROM TMP_KET_QUA_CUOI_CUNG
        ORDER BY "ROWNUM"
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
                'NGAY_HOA_DON': line.get('NGAY_HOA_DON', ''),
                'SO_HOA_DON': line.get('SO_HOA_DON', ''),
                'DIEN_GIAI_CHUNG': line.get('DIEN_GIAI_CHUNG', ''),
                'MA_KHACH_HANG': line.get('MA_DOI_TUONG', ''),
                'TEN_KHACH_HANG': line.get('TEN_DOI_TUONG', ''),
                'MA_HANG': line.get('MA_HANG', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT': line.get('DON_VI_TINH', ''),
                'TONG_SO_LUONG_BAN': line.get('SO_LUONG', ''),
                'DON_GIA': line.get('DON_GIA', ''),
                'DOANH_SO_BAN': line.get('TONG_TIEN_THANH_TOAN', ''),
                'CHIET_KHAU': line.get('SO_TIEN_CHIET_KHAU', ''),
                'TONG_SO_LUONG_TRA_LAI': line.get('SO_LUONG_TRA_LAI', ''),
                'GIA_TRI_TRA_LAI': line.get('SO_TIEN_TRA_LAI', ''),
                'GIA_TRI_GIAM_GIA': line.get('SO_TIEN_GIAM_TRU', ''),
                'TEN_NHAN_VIEN_BAN_HANG': line.get('TEN_NHAN_VIEN', ''),
                'ID_GOC': line.get('ID_CHUNG_TU', ''),
                'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
                'DON_GIA_VON': line.get('DON_GIA_VON', ''),
                'GIA_VON': line.get('GIA_VON', ''),
                })
        return record
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        param = 'Từ ngày: %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)

        if (THONG_KE_THEO == 'KHONG_CHON'):
            action = self.env.ref('bao_cao.open_report__so_chi_tiet_ban_hang').read()[0]
        elif THONG_KE_THEO == 'NHAN_VIEN':
            action = self.env.ref('bao_cao.open_report__so_chi_tiet_ban_hang_theo_nhan_vien').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action