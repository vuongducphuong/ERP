# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_MUA_HANG(models.Model):
    _name = 'bao.cao.tong.hop.mua.hang'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('MAT_HANG', 'Mặt hàng'), ('NHA_CUNG_CAP', 'Nhà cung cấp'), ('MAT_HANG_VA_NHA_CUNG_CAP', 'Mặt hàng và nhà cung cấp'), ('MAT_HANG_VA_NHAN_VIEN', 'Mặt hàng và nhân viên'), ('NHA_CUNG_CAP_VA_CONG_TRINH', 'Nhà cung cấp và công trình'), ], string='Thống kê theo', help='Thống kê theo',required=True,default='MAT_HANG')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',required=True)
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU = fields.Date(string='Từ', help='Từ ngày',required=True,default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    NHOM_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm NCC', help='Nhóm nhà cung cấp')
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    MA_NHA_CUNG_CAP = fields.Char(string='Mã nhà cung cấp', help='Mã nhà cung cấp')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    DVT = fields.Char(string='ĐVT ', help='Đơn vị tính ')
    SO_LUONG_MUA = fields.Float(string='Số lượng mua', help='Số lượng mua', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_MUA = fields.Float(string='Giá trị mua', help='Giá trị mua',digits= decimal_precision.get_precision('VND'))
    CHIET_KHAU = fields.Float(string='Chiết khấu', help='Chiết khấu',digits= decimal_precision.get_precision('VND'))
    SO_LUONG_TRA_LAI = fields.Float(string='Số lượng trả lại', help='Số lượng trả lại', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_TRA_LAI = fields.Float(string='Giá trị trả lại', help='Giá trị trả lại',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_GIAM_GIA = fields.Float(string='Giá trị giảm giá', help='Giá trị giảm giá',digits= decimal_precision.get_precision('VND'))
    TONG_SO_LUONG_MUA = fields.Float(string='Tổng số lượng mua', help='Tổng số lượng mua', digits=decimal_precision.get_precision('SO_LUONG'))
    TONG_GIA_TRI_MUA = fields.Float(string='Tổng giá trị mua', help='Tổng giá trị mua',digits= decimal_precision.get_precision('VND'))

    Sanpham_ids = fields.One2many('danh.muc.vat.tu.hang.hoa')

    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','tong_hop_mua_hang_danh_muc_vthh', string='Chọn sản phẩm') 
    MA_PC_NHOM_VTHH = fields.Char()

    Nha_cung_cap_ids = fields.One2many('res.partner')

    CHON_TAT_CA_NHA_CUNG_CAP = fields.Boolean('Tất cả nhà cung cấp', default=True)
    NHA_CUNG_CAP_MANY_IDS = fields.Many2many('res.partner','tong_hop_mua_hang_res_partner',domain=[('LA_NHA_CUNG_CAP', '=', True)], string='Chọn NCC')
    MA_PC_NHOM_NCC = fields.Char()

    Congtrinh_ids = fields.One2many('danh.muc.cong.trinh')

    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_mua_hang_danh_muc_cong_trinh', string='Chọn công trình') 

    Nhanvien_ids = fields.One2many('res.partner')

    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','tong_hop_mua_hang_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):

        self.NHOM_VTHH_ID = False
        self.NHOM_NCC_ID = False
        self.CHON_TAT_CA_SAN_PHAM = True
        self.CHON_TAT_CA_NHA_CUNG_CAP = True
        self.CHON_TAT_CA_NHAN_VIEN = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.SAN_PHAM_MANY_IDS = []
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.CONG_TRINH_MANY_IDS = []
        self.NHAN_VIEN_MANY_IDS = []
    
    # ------------------------------Mặt hàng ---------------------------------------

    @api.onchange('Sanpham_ids')
    def update_SAN_PHAM_IDS(self):
        self.SAN_PHAM_MANY_IDS = self.Sanpham_ids.ids
       
    @api.onchange('NHOM_VTHH_ID')
    def update_NHOM_VTHH_ID(self):
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP

    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        self.Sanpham_ids = self.SAN_PHAM_MANY_IDS.ids
       
       
    # ------------------------------ end Mặt hàng ---------------------------------------
    
    # ------------------------------Nhà cung cấp ---------------------------------------

    @api.onchange('Nha_cung_cap_ids')
    def update_NHA_CUNG_CAP_IDS(self):
        self.NHA_CUNG_CAP_MANY_IDS =self.Nha_cung_cap_ids.ids
       
      

    @api.onchange('NHOM_NCC_ID')
    def update_NHOM_NCC_ID(self):
        self.NHA_CUNG_CAP_MANY_IDS = []
        self.MA_PC_NHOM_NCC =self.NHOM_NCC_ID.MA_PHAN_CAP

    @api.onchange('NHA_CUNG_CAP_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.Nha_cung_cap_ids = self.NHA_CUNG_CAP_MANY_IDS.ids
       
     
    # ------------------------------ end Nhà cung cấp ---------------------------------------
    # Công trình
    @api.onchange('Congtrinh_ids')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.Congtrinh_ids.ids
        
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.Congtrinh_ids = self.CONG_TRINH_MANY_IDS.ids

    # end Công trình

    # Nhân viên
    @api.onchange('Nhanvien_ids')
    def update_NHAN_VIEN_IDS(self):
        self.NHAN_VIEN_MANY_IDS =self.Nhanvien_ids.ids
      
    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        self.Nhanvien_ids = self.NHAN_VIEN_MANY_IDS.ids
       
    # end nhân viên

  
    
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

   

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
        CHON_TAT_CA_NHA_CUNG_CAP = params['CHON_TAT_CA_NHA_CUNG_CAP'] if 'CHON_TAT_CA_NHA_CUNG_CAP' in params.keys() else 'False'
        CHON_TAT_CA_NHAN_VIEN = params['CHON_TAT_CA_NHAN_VIEN'] if 'CHON_TAT_CA_NHAN_VIEN' in params.keys() else 'False'
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
       
        SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'
        NHA_CUNG_CAP_MANY_IDS = params['NHA_CUNG_CAP_MANY_IDS'] if 'NHA_CUNG_CAP_MANY_IDS' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        NHAN_VIEN_MANY_IDS = params['NHAN_VIEN_MANY_IDS'] if 'NHAN_VIEN_MANY_IDS' in params.keys() else 'False'
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO in ('MAT_HANG','MAT_HANG_VA_NHA_CUNG_CAP','MAT_HANG_VA_NHAN_VIEN'):
            if CHON_TAT_CA_SAN_PHAM == 'False':
                if SAN_PHAM_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO in ('NHA_CUNG_CAP','MAT_HANG_VA_NHA_CUNG_CAP','NHA_CUNG_CAP_VA_CONG_TRINH'):
            if CHON_TAT_CA_NHA_CUNG_CAP == 'False':
                if NHA_CUNG_CAP_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhà cung cấp>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO=='MAT_HANG_VA_NHAN_VIEN':
            if CHON_TAT_CA_NHAN_VIEN == 'False':
                if NHAN_VIEN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO=='NHA_CUNG_CAP_VA_CONG_TRINH':
            if CHON_TAT_CA_CONG_TRINH == 'False':
                if CONG_TRINH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None 
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0       
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() and params['NHOM_VTHH_ID'] != 'False' else None 
        NHOM_NCC_ID = params['NHOM_NCC_ID'] if 'NHOM_NCC_ID' in params.keys() and params['NHOM_NCC_ID'] != 'False' else None 
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        # Execute SQL query here
        # THỐNG KÊ THEO MẶT HÀNG

        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
        MA_PC_NHOM_NCC = params.get('MA_PC_NHOM_NCC')

        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')
        
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

        
        params_sql = {
            
            'TU_NGAY':TU_NGAY, 
            'DEN_NGAY':DEN_NGAY, 
            'NHAN_VIENIDS' : NHAN_VIEN_IDS or None,
            'SAN_PHAM_IDS' : SAN_PHAM_IDS or None,
            'NHA_CUNG_CAPIDS' : NHA_CUNG_CAP_IDS or None,
            'CONG_TRINHIDS' : CONG_TRINH_IDS or None,

            'CHI_NHANH_ID' : CHI_NHANH_ID,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'NHOM_VTHH_ID' : NHOM_VTHH_ID,
            'NHOM_NCC_ID' : NHOM_NCC_ID,


            }     


        if THONG_KE_THEO=='MAT_HANG' :
            return self._lay_bao_cao_mat_hang(params_sql)
            
            
        # THỐNG KÊ THEO NHÀ CUNG CẤP
        elif THONG_KE_THEO=='NHA_CUNG_CAP':
            return self._lay_bao_cao_nha_cung_cap(params_sql)
            
            
        # THỐNG KÊ THEO MẶT HÀNG VÀ NHÀ CUNG CẤP
        elif THONG_KE_THEO=='MAT_HANG_VA_NHA_CUNG_CAP':
            return self._lay_bao_cao_mat_hang_va_nha_cung_cap(params_sql)
            
            
        # THỐNG KÊ THEO MẶT HÀNG VÀ NHÂN VIÊN
        elif THONG_KE_THEO=='MAT_HANG_VA_NHAN_VIEN':
            return self._lay_bao_cao_mat_hang_va_nhan_vien(params_sql)
            
            
        # THỐNG KÊ THEO NHÀ CUNG CẤP VÀ CÔNG TRÌNH
        elif THONG_KE_THEO=='NHA_CUNG_CAP_VA_CONG_TRINH':
            return self._lay_bao_cao_nha_cung_cap_va_cong_trinh(params_sql)
            
    


    def _lay_bao_cao_mat_hang(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--%(TU_NGAY)s

                den_ngay                            DATE := %(DEN_NGAY)s;--%(DEN_NGAY)s

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;--%(CHI_NHANH_ID)s

                --SAN_PHAMIDS                         INTEGER := -1;


                rec                                 RECORD;


            BEGIN

                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_HANG_HOA
                ;

                CREATE TEMP TABLE DS_HANG_HOA
                    AS
                        SELECT
                            II.id AS "MA_HANG_ID"
                            , II."TEN" AS "TEN_HANG"
                            , II."TINH_CHAT"
                        FROM danh_muc_vat_tu_hang_hoa II
                        WHERE (id = any(%(SAN_PHAM_IDS)s))--%(SAN_PHAM_IDS)s
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                            ROW_NUMBER()
                            OVER (
                                ORDER BY PL."MA_HANG", LII."TEN_HANG" )                                                     AS RowNum
                            , PL."MA_HANG_ID"
                            , PL."MA_HANG"
                            , -- Mã hàng
                            LII."TEN_HANG"
                            , -- Tên hàng
                            (CASE LII."TINH_CHAT"
                             WHEN '2'
                                 THEN U."DON_VI_TINH"
                             ELSE MU."DON_VI_TINH" END)                                                                         AS "DON_VI_TINH_CHINH"
                            , -- Tên ĐVC
                            SUM(
                                PL."SO_LUONG_THEO_DVT_CHINH")                                                               AS "SO_LUONG_MUA"
                            , -- Số lượng mua theo ĐVC
                            SUM(PL.
                                "SO_TIEN")                                                                          AS "GIA_TRI_MUA"

                            , -- Giá trị mua
                            SUM(
                                PL."SO_TIEN_CHIET_KHAU")                                                                    AS "SO_TIEN_CHIET_KHAU"
                            , -- Tiền chiết khấu
                            SUM(
                                PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH")                                                               AS "SO_LUONG_TRA_LAI"
                            , -- Số lượng trả lại theo ĐVT chính
                            SUM(
                                PL."SO_TIEN_TRA_LAI")                                                                       AS "GIA_TRI_TRA_LAI"
                            , -- Giá trị trả lại
                            SUM(
                                PL."SO_TIEN_GIAM_TRU")                                                                      AS "GIA_TRI_GIAM_GIA"
                            , -- Giá trị giảm giá
                            SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU" - PL."SO_TIEN_TRA_LAI" -
                                            PL."SO_TIEN_GIAM_TRU")                                                          AS "TONG_GIA_TRI_MUA"




                        FROM so_mua_hang_chi_tiet AS PL
                            INNER JOIN TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN DS_HANG_HOA AS LII ON PL."MA_HANG_ID" = LII."MA_HANG_ID"
                            LEFT JOIN danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU."id" AND LII."TINH_CHAT" <> '2' -- Danh mục ĐVT -> ĐVT chính
                            LEFT JOIN danh_muc_don_vi_tinh AS U ON PL."DVT_ID" = U."id" AND LII."TINH_CHAT" = '2'
                WHERE PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                GROUP BY
                    PL."MA_HANG_ID",
                    PL."MA_HANG", -- Mã hàng
                    LII."TEN_HANG", -- Tên hàng
                CASE LII."TINH_CHAT" WHEN '2' THEN PL."DVT_ID" ELSE PL."DVT_CHINH_ID" END , --
                CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END  -- Tên ĐVT


            ;

            END $$
            ;

            SELECT
                  "MA_HANG"            AS "MA_HANG"
                , "TEN_HANG"                AS "TEN_HANG"
                , "DON_VI_TINH_CHINH"  AS "DVT"
                , "SO_LUONG_MUA"       AS "SO_LUONG_MUA"
                , "GIA_TRI_MUA"       AS "GIA_TRI_MUA"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                , "SO_LUONG_TRA_LAI"   AS "SO_LUONG_TRA_LAI"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "TONG_GIA_TRI_MUA"    AS "TONG_GIA_TRI_MUA"


            FROM TMP_KET_QUA            ;
 
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_nha_cung_cap(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--%(TU_NGAY)s

                den_ngay                            DATE := %(DEN_NGAY)s;--%(DEN_NGAY)s

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;--%(CHI_NHANH_ID)s

                --NHA_CUNG_CAP_IDS                    INTEGER := -1;


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
                           *
                        FROM res_partner AO
                        WHERE (id = any (%(NHA_CUNG_CAPIDS)s))--%(NHA_CUNG_CAPIDS)s
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT  ROW_NUMBER() OVER ( ORDER BY PL."MA_DOI_TUONG" , PL."TEN_DOI_TUONG" ) AS RowNum ,
                            PL."DOI_TUONG_ID" ,
                            PL."MA_DOI_TUONG" , -- Mã NCC
                            PL."TEN_DOI_TUONG" , -- Tên NCC
                            SUM(PL."SO_TIEN") AS "GIA_TRI_MUA" , -- Giá trị mua
                            SUM(PL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU" , -- Tiền chiết khấu
                            SUM(PL."SO_TIEN_TRA_LAI") AS "GIA_TRI_TRA_LAI" , -- Giá trị trả lại
                            SUM(PL."SO_TIEN_GIAM_TRU") AS "GIA_TRI_GIAM_GIA" , -- Giá trị giảm giá
                            SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU" - PL."SO_TIEN_TRA_LAI"
                                - PL."SO_TIEN_GIAM_TRU") AS "TONG_GIA_TRI_MUA"


                    FROM    so_mua_hang_chi_tiet AS PL
                            INNER JOIN TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN DS_NHA_CUNG_CAP  AS LAO ON PL."DOI_TUONG_ID" = LAO.id

                    WHERE   PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                           
                  
                    GROUP BY PL."DOI_TUONG_ID" ,
                            PL."MA_DOI_TUONG" ,
                            PL."TEN_DOI_TUONG"

            ;

            END $$
            ;

            SELECT
                  "MA_DOI_TUONG"            AS "MA_NHA_CUNG_CAP"
                , "TEN_DOI_TUONG"                AS "TEN_NHA_CUNG_CAP"

                , "GIA_TRI_MUA"       AS "GIA_TRI_MUA"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"

                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "TONG_GIA_TRI_MUA"    AS "TONG_GIA_TRI_MUA"


            FROM TMP_KET_QUA

            ;


 
            """
        return self.execute(query,params_sql)



    def _lay_bao_cao_mat_hang_va_nha_cung_cap(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--%(TU_NGAY)s

                den_ngay                            DATE := %(DEN_NGAY)s;--%(DEN_NGAY)s

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;--%(CHI_NHANH_ID)s

                --DS_HANG_HOA_IDS                    INTEGER := -1;
                --NHA_CUNG_CAP_IDS                    INTEGER := -1;


                rec                                 RECORD;


            BEGIN

                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_HANG_HOA
                ;

                CREATE TEMP TABLE DS_HANG_HOA
                    AS
                        SELECT
                           II."id" AS "MA_HANG_ID",
						    II."TINH_CHAT"
                        FROM danh_muc_vat_tu_hang_hoa II
                        WHERE (id = any (%(SAN_PHAM_IDS)s))--%(SAN_PHAM_IDS)s
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                IF %(NHA_CUNG_CAPIDS)s = NULL -- Nếu không chọn NCC nào -> lấy hết ----%(NHA_CUNG_CAPIDS)s
                THEN

                CREATE TEMP TABLE TMP_KET_QUA
                    AS

                SELECT  ROW_NUMBER() OVER ( ORDER BY PL."MA_HANG" , II."TEN" , PL."MA_DOI_TUONG" , PL."TEN_DOI_TUONG" ) AS RowNum ,
                        PL."MA_HANG_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        II."TEN" AS "TEN_HANG" , -- Tên hàng
                        PL."MA_DOI_TUONG" , -- Mã NCC
                        PL."DOI_TUONG_ID" ,
                        PL."TEN_DOI_TUONG" , -- Tên NCC
                        (CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END) AS "DON_VI_TINH_CHINH" , -- Tên ĐVC
						SUM(PL."SO_LUONG_THEO_DVT_CHINH") AS "SO_LUONG_MUA" , -- Số lượng mua theo ĐVC
                        SUM(PL."SO_TIEN") AS "GIA_TRI_MUA" , -- Giá trị mua
                        SUM(PL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU" , -- Tiền chiết khấu
                        SUM(PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") AS "SO_LUONG_TRA_LAI" , -- Số lượng trả lại theo ĐVT chính
                        SUM(PL."SO_TIEN_TRA_LAI") AS "GIA_TRI_TRA_LAI" , -- Giá trị trả lại
                        SUM(PL."SO_TIEN_GIAM_TRU") AS "GIA_TRI_GIAM_GIA" , -- Giá trị giảm giá
                        SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU"
                            - PL."SO_TIEN_TRA_LAI" - PL."SO_TIEN_GIAM_TRU") AS "TONG_GIA_TRI_MUA"  --Tổng giá trị mua




                FROM    so_mua_hang_chi_tiet AS PL
                        INNER JOIN TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN DS_HANG_HOA AS LII ON PL."MA_HANG_ID" = LII."MA_HANG_ID"
                        INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON LII."MA_HANG_ID" = II."id"
                        LEFT JOIN res_partner AS AO ON PL."DOI_TUONG_ID" = AO.id -- Khách hàng, NCC, NV -> NCC, KH, Cán bộ
                        LEFT JOIN danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU."id" AND LII."TINH_CHAT" <> '2' -- Danh mục ĐVT -> ĐVT chính
						LEFT JOIN danh_muc_don_vi_tinh AS U ON PL."DVT_ID" = U."id" AND LII."TINH_CHAT" = '2'
                WHERE   PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                GROUP BY
                        PL."MA_HANG_ID" ,
                        PL."DOI_TUONG_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        II."TEN" , -- Tên hàng
                        PL."MA_DOI_TUONG" , -- Mã NCC
                        PL."TEN_DOI_TUONG" , -- Tên NCC
                        CASE LII."TINH_CHAT" WHEN '2' THEN PL."DVT_ID" ELSE PL."DVT_CHINH_ID" END , -- Nếu là dịch vụ thì nhóm theo ĐVT
						CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END ; -- Tên ĐVT



        ELSE

                 DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
                ;
                CREATE TEMP TABLE DS_NHA_CUNG_CAP
                    AS
                        SELECT
                           *
                        FROM res_partner AO
                        WHERE (id = any (%(NHA_CUNG_CAPIDS)s))--%(NHA_CUNG_CAPIDS)s
                ;

                 CREATE TEMP TABLE TMP_KET_QUA
                    AS
                SELECT  ROW_NUMBER() OVER ( ORDER BY PL."MA_HANG" , II."TEN" , PL."MA_DOI_TUONG" , PL."TEN_DOI_TUONG" ) AS RowNum ,
                        PL."MA_HANG_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        II."TEN" AS "TEN_HANG" , -- Tên hàng
                        PL."MA_DOI_TUONG" , -- Mã NCC
                        PL."DOI_TUONG_ID" ,
                        PL."TEN_DOI_TUONG" , -- Tên NCC
                        (CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END) AS "DON_VI_TINH_CHINH" , -- Tên ĐVC
						SUM(PL."SO_LUONG_THEO_DVT_CHINH") AS "SO_LUONG_MUA" , -- Số lượng mua theo ĐVC
                        SUM(PL."SO_TIEN") AS "GIA_TRI_MUA" , -- Giá trị mua
                        SUM(PL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU" , -- Tiền chiết khấu
                        SUM(PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") AS "SO_LUONG_TRA_LAI" , -- Số lượng trả lại theo ĐVT chính
                        SUM(PL."SO_TIEN_TRA_LAI") AS "GIA_TRI_TRA_LAI" , -- Giá trị trả lại
                        SUM(PL."SO_TIEN_GIAM_TRU") AS "GIA_TRI_GIAM_GIA" , -- Giá trị giảm giá
                        SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU"
                            - PL."SO_TIEN_TRA_LAI" - PL."SO_TIEN_GIAM_TRU") AS "TONG_GIA_TRI_MUA"  --Tổng giá trị mua

                FROM   so_mua_hang_chi_tiet AS PL
                        INNER JOIN TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN DS_HANG_HOA AS LII ON PL."MA_HANG_ID" = LII."MA_HANG_ID"
                        INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON LII."MA_HANG_ID" = II."id"
                        INNER JOIN DS_NHA_CUNG_CAP AS LAO ON PL."DOI_TUONG_ID" = LAO.id
                        LEFT JOIN res_partner AS AO ON LAO."id" = AO.id -- Khách hàng, NCC, NV -> NCC, KH, Cán bộ
                        LEFT JOIN danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU."id" AND LII."TINH_CHAT" <> '2' -- Danh mục ĐVT -> ĐVT chính
						LEFT JOIN danh_muc_don_vi_tinh AS U ON PL."DVT_ID" = U."id" AND LII."TINH_CHAT" = '2'
                WHERE   PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                GROUP BY
                         PL."MA_HANG_ID" ,
                        PL."DOI_TUONG_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        II."TEN" , -- Tên hàng
                        PL."MA_DOI_TUONG" , -- Mã NCC
                        PL."TEN_DOI_TUONG" , -- Tên NCC
                        CASE LII."TINH_CHAT" WHEN '2' THEN PL."DVT_ID" ELSE PL."DVT_CHINH_ID" END , -- Nếu là dịch vụ thì nhóm theo ĐVT
						CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END ; -- Tên ĐVT


           END IF ;

            END $$
            ;

            SELECT
                  "TEN_HANG"            AS "TEN_HANG"
                , "MA_DOI_TUONG"            AS "MA_NHA_CUNG_CAP"
                , "TEN_DOI_TUONG"                AS "TEN_NHA_CUNG_CAP"
                 , "DON_VI_TINH_CHINH"       AS "DVT"
                , "SO_LUONG_MUA"       AS "SO_LUONG_MUA"
                  , "GIA_TRI_MUA"       AS "GIA_TRI_MUA"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                  , "SO_LUONG_TRA_LAI" AS "SO_LUONG_TRA_LAI"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "TONG_GIA_TRI_MUA"    AS "TONG_GIA_TRI_MUA"


            FROM TMP_KET_QUA

            ;

            """
        return self.execute(query,params_sql)


    def _lay_bao_cao_mat_hang_va_nhan_vien(self, params_sql):      
        record = []
        query = """
            
                            DO LANGUAGE plpgsql $$
            DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--%(TU_NGAY)s

                den_ngay                            DATE := %(DEN_NGAY)s;--%(DEN_NGAY)s

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;--%(CHI_NHANH_ID)s

                 --DS_HANG_HOA_IDS                    INTEGER := -1;
                 --NAHN_VIEN_IDS                    INTEGER := -1;


                rec                                 RECORD;


            BEGIN

                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS DS_HANG_HOA
                ;

                CREATE TEMP TABLE DS_HANG_HOA
                    AS
                        SELECT
                           II."id" AS "MA_HANG_ID",
                             II."TEN" AS "TEN_HANG" ,
						    II."TINH_CHAT"
                        FROM danh_muc_vat_tu_hang_hoa II
                        WHERE (id = any (%(SAN_PHAM_IDS)s))--%(SAN_PHAM_IDS)s
                ;

                 DROP TABLE IF EXISTS DS_NHAN_VIEN
                ;
                CREATE TEMP TABLE DS_NHAN_VIEN
                    AS
                        SELECT
                           *
                        FROM res_partner
                        WHERE (id = any (%(NHAN_VIENIDS)s))--%(NHAN_VIENIDS)s
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;


                CREATE TEMP TABLE TMP_KET_QUA
                    AS

                SELECT
                           ROW_NUMBER() OVER ( ORDER BY PL."MA_HANG" , LII."TEN_HANG" , PL."MA_NHAN_VIEN", PL."TEN_NHAN_VIEN" ) AS RowNum ,
                        PL."MA_HANG_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        LII."TEN_HANG" , -- Tên hàng
                        PL."NHAN_VIEN_ID" ,
                        PL."MA_NHAN_VIEN" , -- Mã NCC
                        PL."TEN_NHAN_VIEN" , -- Tên NCC
                        (CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END) AS "DON_VI_TINH_CHINH" , -- Tên ĐVC
						SUM(PL."SO_LUONG_THEO_DVT_CHINH") AS "SO_LUONG_MUA" , -- Số lượng mua theo ĐVC
                        SUM(PL."SO_TIEN") AS "GIA_TRI_MUA" , -- Giá trị mua
                        SUM(PL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU" , -- Tiền chiết khấu
                        SUM(PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") AS "SO_LUONG_TRA_LAI" , -- Số lượng trả lại theo ĐVT chính
                        SUM(PL."SO_TIEN_TRA_LAI") AS "GIA_TRI_TRA_LAI" , -- Giá trị trả lại
                        SUM(PL."SO_TIEN_GIAM_TRU") AS "GIA_TRI_GIAM_GIA" , -- Giá trị giảm giá
                        SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU"
                            - PL."SO_TIEN_TRA_LAI" - PL."SO_TIEN_GIAM_TRU") AS "TONG_GIA_TRI_MUA"  --Tổng giá trị mua




                FROM    so_mua_hang_chi_tiet AS PL
                        INNER JOIN TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN DS_HANG_HOA AS LII ON PL."MA_HANG_ID" = LII."MA_HANG_ID"
                        INNER JOIN DS_NHAN_VIEN AS LE ON PL."NHAN_VIEN_ID" = LE."id"

                        LEFT JOIN danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU."id" AND LII."TINH_CHAT" <> '2' -- Danh mục ĐVT -> ĐVT chính
						LEFT JOIN danh_muc_don_vi_tinh AS U ON PL."DVT_ID" = U."id" AND LII."TINH_CHAT" = '2'
                WHERE   PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                GROUP BY
                        PL."MA_HANG_ID" ,
                        PL."NHAN_VIEN_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        LII."TEN_HANG" , -- Tên hàng
                        PL."MA_NHAN_VIEN" , -- Mã NCC
                        PL."TEN_NHAN_VIEN" , -- Tên NCC
                        CASE LII."TINH_CHAT" WHEN '2' THEN PL."DVT_ID" ELSE PL."DVT_CHINH_ID" END , -- Nếu là dịch vụ thì nhóm theo ĐVT
						CASE LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH" END ; -- Tên ĐVT





            END $$
            ;

            SELECT
                  "TEN_HANG"            AS "TEN_HANG"
                , "MA_NHAN_VIEN"            AS "MA_NHAN_VIEN"
                , "TEN_NHAN_VIEN"                AS "TEN_NHAN_VIEN"
                 , "DON_VI_TINH_CHINH"       AS "DVT"
                , "SO_LUONG_MUA"       AS "SO_LUONG_MUA"
                  , "GIA_TRI_MUA"       AS "GIA_TRI_MUA"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                  , "SO_LUONG_TRA_LAI" AS "SO_LUONG_TRA_LAI"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "TONG_GIA_TRI_MUA"    AS "TONG_GIA_TRI_MUA"


            FROM TMP_KET_QUA

            ;



            """
        return self.execute(query,params_sql)


    def _lay_bao_cao_nha_cung_cap_va_cong_trinh(self, params_sql):      
        record = []
        query = """
            
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--%(TU_NGAY)s

                den_ngay                            DATE := %(DEN_NGAY)s;--%(DEN_NGAY)s

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;--%(CHI_NHANH_ID)s

              


                rec                                 RECORD;


            BEGIN

                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS TMP_CONG_TRINH_DC_CHON
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_DC_CHON
                    AS
                        SELECT
                            PW."id"  AS "CONG_TRINH_ID",
                            PW."MA_PHAN_CAP" ,
                            PW."MA_CONG_TRINH" ,
                            PW."TEN_CONG_TRINH" ,
                            PW."LOAI_CONG_TRINH"
                        FROM danh_muc_cong_trinh PW
                        WHERE (id = any (%(CONG_TRINHIDS)s))--%(CONG_TRINHIDS)s
                ;
                 DROP TABLE IF EXISTS TMP_CONG_TRINH_DC_CHON_CHILD
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_DC_CHON_CHILD
                    AS
                        SELECT
                            S."CONG_TRINH_ID" ,
                            S."MA_PHAN_CAP",
                            S."MA_CONG_TRINH" ,
                            S."TEN_CONG_TRINH"
                FROM    TMP_CONG_TRINH_DC_CHON S
                        LEFT  JOIN TMP_CONG_TRINH_DC_CHON S1 ON S1."MA_PHAN_CAP" LIKE concat(S."MA_PHAN_CAP",'%%')
                                                              AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE   S1."MA_PHAN_CAP" IS NULL ;

                 DROP TABLE IF EXISTS TMP_CONG_TRINH
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH
                    AS
                        SELECT DISTINCT
                            PW."id"  AS "CONG_TRINH_ID",
                            PW."MA_PHAN_CAP" ,
                            PW."MA_CONG_TRINH" ,
                            PW."TEN_CONG_TRINH"

                        FROM TMP_CONG_TRINH_DC_CHON_CHILD SPW
                        INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE concat(SPW."MA_PHAN_CAP",'%%')		;

                 DROP TABLE IF EXISTS DS_NHA_CUNG_CAP
                ;
                CREATE TEMP TABLE DS_NHA_CUNG_CAP
                    AS
                        SELECT
                           id AS "DOI_TUONG_ID",
                            "LIST_MA_NHOM_KH_NCC", 
                            "LIST_TEN_NHOM_KH_NCC"

                        FROM res_partner
                        WHERE (id = any (%(NHA_CUNG_CAPIDS)s))--%(NHA_CUNG_CAPIDS)s
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;


                CREATE TEMP TABLE TMP_KET_QUA
                    AS

                SELECT
                        ROW_NUMBER() OVER ( ORDER BY PL."TEN_DOI_TUONG", PL."MA_DOI_TUONG", JP."TEN_CONG_TRINH", JP."MA_CONG_TRINH", PL."TEN_HANG", PL."MA_HANG" ) AS RowNum ,
                        PL."DOI_TUONG_ID" ,
                        PL."MA_DOI_TUONG" , -- Mã NCC
                        PL."TEN_DOI_TUONG" , -- Tên NCC
                        JP."MA_CONG_TRINH" , -- Mã công trình
                        JP."TEN_CONG_TRINH" , -- Tên công trình
                        PL."MA_HANG_ID" ,
                        PL."MA_HANG" , -- Mã hàng
                        PL."TEN_HANG" , -- Tên hàng
                        U."DON_VI_TINH" AS "DON_VI_TINH_CHINH" ,
						SUM(PL."SO_LUONG_THEO_DVT_CHINH") AS "SO_LUONG_MUA" , -- Số lượng mua theo ĐVC
                        SUM(PL."SO_TIEN") AS "GIA_TRI_MUA" , -- Giá trị mua
                        SUM(PL."SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU" , -- Tiền chiết khấu
                        SUM(PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") AS "SO_LUONG_TRA_LAI" , -- Số lượng trả lại theo ĐVT chính
                        SUM(PL."SO_TIEN_TRA_LAI") AS "GIA_TRI_TRA_LAI" , -- Giá trị trả lại
                        SUM(PL."SO_TIEN_GIAM_TRU") AS "GIA_TRI_GIAM_GIA" , -- Giá trị giảm giá
                         SUM(PL."SO_LUONG_THEO_DVT_CHINH" - PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") AS "TONG_SO_LUONG_MUA" ,
                        SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU"
                            - PL."SO_TIEN_TRA_LAI" - PL."SO_TIEN_GIAM_TRU") AS "TONG_GIA_TRI_MUA"  --Tổng giá trị mua




                FROM    so_mua_hang_chi_tiet AS PL
                        INNER JOIN TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                         INNER JOIN TMP_CONG_TRINH AS LPW ON PL."CONG_TRINH_ID" = LPW."CONG_TRINH_ID"

                        INNER JOIN DS_NHA_CUNG_CAP AS LAO ON PL."DOI_TUONG_ID" = LAO."DOI_TUONG_ID"
                        INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON PL."MA_HANG_ID" = II."id"
                        LEFT JOIN danh_muc_don_vi_tinh AS U ON II."DVT_CHINH_ID" = U."id"
                        LEFT JOIN TMP_CONG_TRINH_DC_CHON_CHILD AS JP ON LPW."MA_PHAN_CAP" LIKE concat(JP."MA_PHAN_CAP",'%%')
                WHERE   PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                GROUP BY

                PL."DOI_TUONG_ID" ,
                PL."MA_DOI_TUONG" , -- Mã NCC
                PL."TEN_DOI_TUONG" ,  -- Tên NCC
                JP."MA_CONG_TRINH" , -- Mã công trình
                JP."TEN_CONG_TRINH" , -- Tên công trình
                PL."MA_HANG_ID" ,
                PL."MA_HANG" , -- Mã hàng
                PL."TEN_HANG" , -- Tên hàng
                U."DON_VI_TINH" ,
                LAO."LIST_MA_NHOM_KH_NCC" ,
                LAO."LIST_TEN_NHOM_KH_NCC"

		HAVING 	 SUM(PL."SO_LUONG_THEO_DVT_CHINH") > 0 OR -- Số lượng mua theo ĐVC
                SUM(PL."SO_TIEN") > 0 OR  -- Giá trị mua
                SUM(PL."SO_TIEN_CHIET_KHAU") > 0 OR  -- Tiền chiết khấu
                SUM(PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") > 0 OR -- Số lượng trả lại theo ĐVT chính
                SUM(PL."SO_TIEN_TRA_LAI") > 0 OR -- Giá trị trả lại
                SUM(PL."SO_TIEN_GIAM_TRU") > 0 OR -- Giá trị giảm giá
                SUM(PL."SO_LUONG_THEO_DVT_CHINH" - PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH") > 0 OR--Tổng số lượng mua --
                SUM(PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU" - PL."SO_TIEN_TRA_LAI"
                    - PL."SO_TIEN_GIAM_TRU") > 0  ;--Tổng giá trị mua ;


            END $$
            ;

            SELECT
                  "TEN_HANG"            AS "TEN_HANG"
                , "TEN_DOI_TUONG"            AS "TEN_NHA_CUNG_CAP"
                , "TEN_CONG_TRINH"                AS "TEN_CONG_TRINH"
                 , "DON_VI_TINH_CHINH"       AS "DVT"
                , "SO_LUONG_MUA"       AS "SO_LUONG_MUA"
                  , "GIA_TRI_MUA"       AS "GIA_TRI_MUA"
                , "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU"
                  , "SO_LUONG_TRA_LAI" AS "SO_LUONG_TRA_LAI"
                , "GIA_TRI_TRA_LAI"    AS "GIA_TRI_TRA_LAI"
                , "GIA_TRI_GIAM_GIA"   AS "GIA_TRI_GIAM_GIA"
                , "TONG_SO_LUONG_MUA"    AS "TONG_SO_LUONG_MUA"
                , "TONG_GIA_TRI_MUA"    AS "TONG_GIA_TRI_MUA"


            FROM TMP_KET_QUA

            ;

            """
        return self.execute(query,params_sql)


    ### END IMPLEMENTING CODE ###

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_TONG_HOP_MUA_HANG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
       
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id

        return result


    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
        if (THONG_KE_THEO == 'MAT_HANG'):
            # san_phams = self._context.get('Sanpham_ids_mathang')
            # if len(san_phams)==1:
            #     san_pham = san_phams[0].get('TEN')
            #     param = 'Hàng hóa: %s;Từ ngày: %s đến ngày %s' % (san_pham, TU_NGAY_F, DEN_NGAY_F)
            # else:
            action = self.env.ref('bao_cao.open_report__tong_hop_mua_hang').read()[0]
        elif THONG_KE_THEO == 'NHA_CUNG_CAP':
            # nha_cung_caps = self._context.get('Nha_cung_cap_ids')
            # if len(nha_cung_caps)==1:
            #     nha_cc = nha_cung_caps[0].get('name')
            #     param = 'Nhà cung cấp: %s;Từ ngày: %s đến ngày %s' % (nha_cc, TU_NGAY_F, DEN_NGAY_F)
            # else:
            #     param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
            action = self.env.ref('bao_cao.open_report__bao_cao_tong_hop_mua_hang_nhacungcap').read()[0]
        elif THONG_KE_THEO == 'MAT_HANG_VA_NHA_CUNG_CAP':
            # san_phams = self._context.get('Sanpham_ids_mathang_nhacc')
            # nha_cung_caps = self._context.get('Nha_cung_cap_ids_mathang_nhacc')
            # if len(san_phams)==1 and len(nha_cung_caps)==1 :
            #     san_pham = san_phams[0].get('TEN')
            #     nha_cc = nha_cung_caps[0].get('name')
            #     param = 'Mặt hàng: %s;Nhà cung cấp: %s;Từ ngày: %s đến ngày %s' % (san_pham, nha_cc, TU_NGAY_F, DEN_NGAY_F)
            # elif len(san_phams)==1 and len(nha_cung_caps)!=1:
            #     san_pham = san_phams[0].get('TEN')
            #     param = 'Mặt hàng: %s;Từ ngày: %s đến ngày %s' % (san_pham, TU_NGAY_F, DEN_NGAY_F)
            # elif len(san_phams)!=1 and len(nha_cung_caps)==1:
            #     nha_cc = nha_cung_caps[0].get('name')
            #     param = 'Nhà cung cấp: %s;Từ ngày: %s đến ngày %s' % (nha_cc, TU_NGAY_F, DEN_NGAY_F)
            # else:
            #    param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
            action = self.env.ref('bao_cao.open_report__bao_cao_tong_hop_mua_hang_mathang_nhacungcap').read()[0]
        elif THONG_KE_THEO == 'MAT_HANG_VA_NHAN_VIEN':
            # san_phams = self._context.get('Sanpham_ids_mathang_nhanvien')
            # nhan_viens = self._context.get('Nhanvien_ids')
            # if len(san_phams)==1 and len(nhan_viens)==1 :
            #     san_pham = san_phams[0].get('TEN')
            #     nhan_vien = nhan_viens[0].get('name')
            #     param = 'Mặt hàng: %s;Nhân viên: %s;Từ ngày: %s đến ngày %s' % (san_pham, nhan_vien, TU_NGAY_F, DEN_NGAY_F)
            # elif len(san_phams)==1 and len(nhan_viens)!=1:
            #     san_pham = san_phams[0].get('TEN')
            #     param = 'Mặt hàng: %s;Từ ngày: %s đến ngày %s' % (san_pham, TU_NGAY_F, DEN_NGAY_F)
            # elif len(san_phams)!=1 and len(nhan_viens)==1:
            #     nhan_vien = nhan_viens[0].get('name')
            #     param = 'Nhân viên: %s;Từ ngày: %s đến ngày %s' % (nhan_vien, TU_NGAY_F, DEN_NGAY_F)
            # else:
            #    param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
            action = self.env.ref('bao_cao.open_report__bao_cao_tong_hop_mua_hang_mathang_nhanvien').read()[0]
        elif THONG_KE_THEO == 'NHA_CUNG_CAP_VA_CONG_TRINH':
            # nha_cung_caps = self._context.get('Nha_cung_cap_ids_nhacc_congtrinh')
            # cong_trinhs = self._context.get('Congtrinh_ids')
            # if len(nha_cung_caps)==1 and len(cong_trinhs)==1 :
            #     nha_cc = nha_cung_caps[0].get('name')
            #     cong_trinh = cong_trinhs[0].get('MA_CONG_TRINH')
            #     param = 'Nhà cung cấp: %s;Công trình: %s;Từ ngày: %s đến ngày %s' % (nha_cc, cong_trinh, TU_NGAY_F, DEN_NGAY_F)
            # elif len(nha_cung_caps)==1 and len(cong_trinhs)!=1:
            #     nha_cc = nha_cung_caps[0].get('name')
            #     param = 'Nhà cung cấp: %s;Từ ngày: %s đến ngày %s' % (nha_cc, TU_NGAY_F, DEN_NGAY_F)
            # elif len(nha_cung_caps)!=1 and len(cong_trinhs)==1:
            #     cong_trinh = cong_trinhs[0].get('MA_CONG_TRINH')
            #     param = 'Công trình: %s;Từ ngày: %s đến ngày %s' % (cong_trinh, TU_NGAY_F, DEN_NGAY_F)
            # else:
            #    param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
            action = self.env.ref('bao_cao.open_report__bao_cao_tong_hop_mua_hang_nhacc_congtrinh').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action