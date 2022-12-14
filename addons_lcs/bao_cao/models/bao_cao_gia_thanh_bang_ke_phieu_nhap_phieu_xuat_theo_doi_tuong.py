# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_gia_thanh_bang_ke_phieu_nhap_phieu_xuat_theo_doi_tuong(models.Model):
    _name = 'bao.cao.gia.thanh.bang.ke.pnx.theo.doi.tuong'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    THONG_KE_THEO = fields.Selection([('DOI_TUONG_THCP', 'Đối tượng Tập hợp chi phí'),('CONG_TRINH', 'Công trình'),('DON_HANG', 'Đơn hàng'),('HOP_DONG', 'Hợp đồng')], string='Thống kê theo', help='Thống kê theo',default='DOI_TUONG_THCP',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH ', help='Nhóm vật tư hàng hóa ')
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', ' Đơn vị chuyển đổi 2 '), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH',required=True)

    DOI_TUONG_THCP_ID = fields.Integer(string='DOI_TUONG_THCP_ID')
    MA_DOI_TUONG_THCP = fields.Char(string='MA_DOI_TUONG_THCP', help='JobCode')
    MA_HANG = fields.Char(string='MA_HANG', help='JobCode')
    TEN_HANG = fields.Char(string='TEN_HANG', help='JobCode')
    TEN_KHO = fields.Char(string='TEN_KHO', help='JobCode')
    DVT = fields.Char(string='DVT', help='JobCode')
    TEN_NHOM_VTHH = fields.Char(string='TEN_NHOM_VTHH', help='JobCode')
    MA_CONG_TRINH = fields.Char(string='MA_CONG_TRINH', help='JobCode')
    SO_DON_HANG = fields.Char(string='SO_DON_HANG', help='JobCode')
    HOP_DONG_DU_AN = fields.Char(string='HOP_DONG_DU_AN', help='JobCode')
    TRICH_YEU = fields.Char(string='TRICH_YEU', help='JobCode')
    TEN_DOI_TUONG_THCP = fields.Char(string='TEN_DOI_TUONG_THCP', help='JobName')
    TEN_CONG_TRINH = fields.Char(string='TEN_CONG_TRINH', help='JobName')
    NGAY_DON_HANG = fields.Date(string='NGAY_DON_HANG', help='JobCode')

    NGAY_HACH_TOAN = fields.Date(string='NGAY_HACH_TOAN', help='JobCode')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='JobCode')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='JobCode')
    DIEN_GIAI_CHUNG = fields.Char(string='DIEN_GIAI_CHUNG', help='JobCode')
    
   
    SO_LUONG_NHAP = fields.Float(string='SO_LUONG_NHAP', help='OpenDebitAmount',digits=decimal_precision.get_precision('VND'))
    DON_GIA_NHAP = fields.Float(string='DON_GIA_NHAP', help='OpenCreditAmount',digits=decimal_precision.get_precision('VND'))
    THANH_TIEN_NHAP = fields.Float(string='DON_GIA_NHAP', help='OpenCreditAmount',digits=decimal_precision.get_precision('VND'))
    SO_LUONG_XUAT = fields.Float(string='SO_LUONG_XUAT', help='DebitAmount',digits=decimal_precision.get_precision('VND'))
    DON_GIA_XUAT = fields.Float(string='DON_GIA_XUAT', help='CreditAmount',digits=decimal_precision.get_precision('VND'))
    THANH_TIEN_XUAT = fields.Float(string='THANH_TIEN_XUAT', help='CreditAmount',digits=decimal_precision.get_precision('VND'))
    

    SAN_PHAM_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa')
    CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
    SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','tong_hop_nxk_danh_muc_vthh', string='Chọn sản phẩm') 
    MA_PC_NHOM_VTHH = fields.Char()

    DOI_TUONG_THCP_IDS = fields.One2many('danh.muc.doi.tuong.tap.hop.chi.phi')
    CHON_TAT_CA_DOI_TUONG_THCP = fields.Boolean('Tất cả đối tượng THCP', default=True)
    DOI_TUONG_THCP_MANY_IDS = fields.Many2many('danh.muc.doi.tuong.tap.hop.chi.phi','tong_hop_nxk_dtthcp', string='Chọn đối tượng THCP') 

    CONG_TRINH_IDS = fields.One2many ('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_nxk_cong_trinh', string='Chọn công trình') 

    DON_HANG_IDS = fields.One2many('account.ex.don.dat.hang')
    CHON_TAT_CA_DON_HANG = fields.Boolean('Tất cả đơn hàng', default=True)
    DON_HANG_MANY_IDS = fields.Many2many('account.ex.don.dat.hang','tong_hop_nxk_don_hang', string='Chọn đơn hàng') 

    HOP_DONG_BAN_IDS = fields.One2many('sale.ex.hop.dong.ban')
    CHON_TAT_CA_HOP_DONG_BAN = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_BAN_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','tong_hop_nxk_hdb', string='Chọn hợp đồng') 

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):
        self.NHOM_VTHH_ID = False
        self.CHON_TAT_CA_SAN_PHAM = True
        self.CHON_TAT_CA_DOI_TUONG_THCP = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.CHON_TAT_CA_DON_HANG = True
        self.CHON_TAT_CA_HOP_DONG_BAN = True
       
        self.SAN_PHAM_MANY_IDS = []
        self.DOI_TUONG_THCP_MANY_IDS = []
        self.CONG_TRINH_MANY_IDS = []
        self.DON_HANG_MANY_IDS = []
        self.HOP_DONG_BAN_MANY_IDS = []

    # Sản phẩm
    @api.onchange('SAN_PHAM_IDS')
    def _onchange_SAN_PHAM_IDS(self):
        self.SAN_PHAM_MANY_IDS =self.SAN_PHAM_IDS.ids

    @api.onchange('SAN_PHAM_MANY_IDS')
    def _onchange_SAN_PHAM_MANY_IDS(self):
        self.SAN_PHAM_IDS =self.SAN_PHAM_MANY_IDS.ids

    @api.onchange('NHOM_VTHH_ID')
    def update_NHOM_VTHH_ID(self):
        self.SAN_PHAM_MANY_IDS = []
        self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP
        
    # end
    # đối tượng THCP
    @api.onchange('DOI_TUONG_THCP_IDS')
    def _onchange_DOI_TUONG_THCP_IDS(self):
        self.DOI_TUONG_THCP_MANY_IDS =self.DOI_TUONG_THCP_IDS.ids

    @api.onchange('DOI_TUONG_THCP_MANY_IDS')
    def _onchange_DOI_TUONG_THCP_MANY_IDS(self):
        self.DOI_TUONG_THCP_IDS =self.DOI_TUONG_THCP_MANY_IDS.ids
    # end
    # Công trình
    @api.onchange('CONG_TRINH_IDS')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.CONG_TRINH_IDS.ids
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.CONG_TRINH_IDS = self.CONG_TRINH_MANY_IDS.ids
    # end  
    # Đơn đặt hàng
    @api.onchange('DON_HANG_IDS')
    def update_DON_HANG_IDS(self):
        self.DON_HANG_MANY_IDS =self.DON_HANG_IDS.ids
        
    @api.onchange('DON_HANG_MANY_IDS')
    def _onchange_DON_HANG_MANY_IDS(self):
        self.DON_HANG_IDS = self.DON_HANG_MANY_IDS.ids
    # end  

    # Hợp đồng bán
    @api.onchange('HOP_DONG_BAN_IDS')
    def update_HOP_DONG_BAN_IDS(self):
        self.HOP_DONG_BAN_MANY_IDS =self.HOP_DONG_BAN_IDS.ids
        
    @api.onchange('HOP_DONG_BAN_MANY_IDS')
    def _onchange_HOP_DONG_BAN_MANY_IDS(self):
        self.HOP_DONG_BAN_IDS = self.HOP_DONG_BAN_MANY_IDS.ids
    # end  

    @api.model
    def default_get(self, fields_list):
        result = super(bao_cao_gia_thanh_bang_ke_phieu_nhap_phieu_xuat_theo_doi_tuong, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    
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
        SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_DOI_TUONG_THCP = params['CHON_TAT_CA_DOI_TUONG_THCP'] if 'CHON_TAT_CA_DOI_TUONG_THCP' in params.keys() else 'False'
        DOI_TUONG_THCP_MANY_IDS = params['DOI_TUONG_THCP_MANY_IDS'] if 'DOI_TUONG_THCP_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_DON_HANG = params['CHON_TAT_CA_DON_HANG'] if 'CHON_TAT_CA_DON_HANG' in params.keys() else 'False'
        DON_HANG_MANY_IDS = params['DON_HANG_MANY_IDS'] if 'DON_HANG_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_HOP_DONG_BAN = params['CHON_TAT_CA_HOP_DONG_BAN'] if 'CHON_TAT_CA_HOP_DONG_BAN' in params.keys() else 'False'
        HOP_DONG_BAN_MANY_IDS = params['HOP_DONG_BAN_MANY_IDS'] if 'HOP_DONG_BAN_MANY_IDS' in params.keys() else 'False'
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO in ('DOI_TUONG_THCP','CONG_TRINH','DON_HANG','HOP_DONG'):
            if CHON_TAT_CA_SAN_PHAM == 'False':
                if SAN_PHAM_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Mặt hàng>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'DOI_TUONG_THCP':
            if CHON_TAT_CA_DOI_TUONG_THCP == 'False':
                if DOI_TUONG_THCP_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đối tượng THCP>. Xin vui lòng chọn lại.')
        
        if THONG_KE_THEO == 'CONG_TRINH':
            if CHON_TAT_CA_CONG_TRINH == 'False':
                if CONG_TRINH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'DON_HANG':
            if CHON_TAT_CA_DON_HANG == 'False':
                if DON_HANG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đơn đặt hàng>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'HOP_DONG':
            if CHON_TAT_CA_HOP_DONG_BAN == 'False':
                if HOP_DONG_BAN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hợp đồng/Dự án>. Xin vui lòng chọn lại.')

        

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
    
        DON_VI_TINH_PARAM = params.get('DON_VI_TINH')
        if DON_VI_TINH_PARAM == 'DON_VI_CHUYEN_DOI_1':
            DON_VI_TINH = 1
        elif DON_VI_TINH_PARAM == 'DON_VI_CHUYEN_DOI_2':
            DON_VI_TINH = 2
        else:
            DON_VI_TINH = 0

        if params.get('CHON_TAT_CA_SAN_PHAM'):
            domain = []
            if MA_PC_NHOM_VTHH:
                domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
            SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
        else:
            SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')
        
        if params.get('CHON_TAT_CA_DOI_TUONG_THCP'):
            domain = []
            DOI_TUONG_THCP_IDS = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search(domain).ids
        else:
            DOI_TUONG_THCP_IDS = params.get('DOI_TUONG_THCP_MANY_IDS')

        if params.get('CHON_TAT_CA_CONG_TRINH'):
            domain = []
            CONG_TRINH_IDS = self.env['danh.muc.cong.trinh'].search(domain).ids
        else:
            CONG_TRINH_IDS = params.get('CONG_TRINH_MANY_IDS')

        if params.get('CHON_TAT_CA_DON_HANG'):
            domain = []
            DON_HANG_IDS = self.env['account.ex.don.dat.hang'].search(domain).ids
        else:
            DON_HANG_IDS = params.get('DON_HANG_MANY_IDS')

        if params.get('CHON_TAT_CA_HOP_DONG_BAN'):
            domain = []
            HOP_DONG_BAN_IDS = self.env['sale.ex.hop.dong.ban'].search(domain).ids
        else:
            HOP_DONG_BAN_IDS = params.get('HOP_DONG_BAN_MANY_IDS')

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'DON_VI_TINH':DON_VI_TINH,
            'SAN_PHAM_IDS':SAN_PHAM_IDS, 
            'DOI_TUONG_THCP_IDS':DOI_TUONG_THCP_IDS, 
            'CONG_TRINH_IDS':CONG_TRINH_IDS, 
            'DON_HANG_IDS':DON_HANG_IDS, 
            'HOP_DONG_BAN_IDS':HOP_DONG_BAN_IDS, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'limit': limit,
            'offset': offset, 
            }      
    
        # Execute SQL query here
        if THONG_KE_THEO=='DOI_TUONG_THCP':
            return self._lay_bao_cao_doi_tuong_thcp(params_sql)

        if THONG_KE_THEO=='CONG_TRINH':
            return self._lay_bao_cao_cong_trinh(params_sql)

        if THONG_KE_THEO=='DON_HANG':
            return self._lay_bao_cao_don_hang(params_sql)
        
        if THONG_KE_THEO == 'HOP_DONG':
            return self._lay_bao_cao_hop_dong(params_sql)

    ### END IMPLEMENTING CODE ###
    def _lay_bao_cao_doi_tuong_thcp(self, params_sql):      
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

                den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


                PHAN_THAP_PHAN_SO_LUONG             INTEGER;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INTEGER;

                PHAN_THAP_PHAN_DON_GIA              INTEGER;

                CHE_DO_KE_TOAN                      VARCHAR;

                VTHH_IDS                            INTEGER := -1;

                loai_dvt                            INTEGER := %(DON_VI_TINH)s; 

                rec                                 RECORD;

                --@ListJobID--Tham số bên misa
                --@InventoryItemID ----Tham số bên misa


                BEGIN

                SELECT value
                INTO CHE_DO_KE_TOAN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;

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


                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                AS
                SELECT *
                FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;

                DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
                ;

                CREATE TEMP TABLE TMP_DOI_TUONG_THCP

                (
                "DOI_TUONG_THCP_ID"  INT PRIMARY KEY,
                "MA_DOI_TUONG_THCP"  VARCHAR(25)
                NULL,
                "TEN_DOI_TUONG_THCP" VARCHAR(128)
                NULL,
                "MA_PHAN_CAP"        VARCHAR(100)
                NULL
                )
                ;

                INSERT INTO TMP_DOI_TUONG_THCP
                SELECT
                J."id"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , J."MA_PHAN_CAP"
                FROM danh_muc_doi_tuong_tap_hop_chi_phi J
                WHERE J."id" = any(%(DOI_TUONG_THCP_IDS)s) --ListJobID
                ;


                -----------------------------------------

                DROP TABLE IF EXISTS TMP_DS_DOI_TUONG_THCP
                ;

                CREATE TEMP TABLE TMP_DS_DOI_TUONG_THCP


                (
                "DOI_TUONG_THCP_ID"      INT, --PRIMARY KEY ,-- Cột này dùng để Group lên báo cáo
                "REAL_DOI_TUONG_THCP_ID" INT, -- Cột này dùng để JOIN lấy dữ liệu
                "MA_DOI_TUONG_THCP"      VARCHAR(25)
                NULL,
                "TEN_DOI_TUONG_THCP"     VARCHAR(128)
                NULL,
                "MA_PHAN_CAP"            VARCHAR(100)
                NULL
                )
                ;

                INSERT INTO TMP_DS_DOI_TUONG_THCP
                SELECT
                tJ."DOI_TUONG_THCP_ID"
                , J."id"
                , TJ."MA_DOI_TUONG_THCP"
                , TJ."TEN_DOI_TUONG_THCP"
                , J."MA_PHAN_CAP"
                FROM TMP_DOI_TUONG_THCP tJ
                INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON J."MA_PHAN_CAP" LIKE tJ."MA_PHAN_CAP"
                || '%%'
                GROUP BY tJ."DOI_TUONG_THCP_ID",
                J."id",
                TJ."MA_DOI_TUONG_THCP",
                TJ."TEN_DOI_TUONG_THCP",
                J."MA_PHAN_CAP"
                ;

                DROP TABLE IF EXISTS TMP_DS_VAT_TU_HH
                ;

                CREATE TEMP TABLE TMP_DS_VAT_TU_HH
                -- Bảng chứa danh sách hàng hóa
                (
                "MA_HANG_ID" INT,
                "MA_HANG"    VARCHAR(255),
                "DVT_ID"     INT


                )
                ;

                IF VTHH_IDS IS NULL
                THEN
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM danh_muc_vat_tu_hang_hoa
                ;
                ELSE
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM
                danh_muc_vat_tu_hang_hoa II
                WHERE II."id" = any(%(SAN_PHAM_IDS)s)--InventoryItemID
                ;
                END IF
                ;

                -----------------------------------------


                DROP TABLE IF EXISTS TMP_CAN_DOI
                ;

                CREATE TEMP TABLE TMP_CAN_DOI
                AS

                SELECT
                J."DOI_TUONG_THCP_ID"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."CHI_NHANH_ID"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."DIEN_GIAI_CHUNG"
                , GL."MA_HANG_ID"
                , GL."MA_HANG"
                , GL."TEN_HANG"
                , GL."KHO_ID"
                , GL."MA_KHO"
                , GL."TEN_KHO"
                , (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                            AS "DVT"
                , ----------------------------------------------

                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '3040', '3041', '3042', '3043', '2021'))
                THEN 0
                ELSE CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id" -- Nếu ĐVT trên chứng từ = ĐVT chọn trên tham số -> Lấy số lượng trên chứng từ
                THEN GL."SO_LUONG_NHAP"
                ELSE GL."SO_LUONG_NHAP_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1) -- Nếu ĐVT trên chứng từ <> ĐVT trên tham số thì lấy số lượng được tính qua tỷ lệ chuyển đổi trên danh mục
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_NHAP"
                , --Đoạn này xuống dưới tính lại = Thành tiền / Số lượng
                CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_NHAP"
                , ROUND(CAST(SUM(CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024',
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                THEN 0
                ELSE CASE
                -- chứng từ nhập kho thì lấy thành tiền
                WHEN GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012',
                '2013', '2014', '2015',
                '2016', '2017') --nhập kho
                THEN GL."SO_TIEN_NHAP"
                --MUA HÀNG nhập kho thì không lấy VTHH có tính chất diễn giải.
                WHEN GL."LOAI_CHUNG_TU" IN ('302', '307', '308',
                '309', '310', '318',
                '319', '320', '321',
                '322', '352', '357',
                '358', '359', '360',
                '368', '369', '370',
                '371', '372')
                AND I."TINH_CHAT" <> '2'
                AND I."TINH_CHAT" <> '3'
                THEN ROUND(CAST((GL."SO_TIEN_NHAP") AS NUMERIC),
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)


                ELSE 0
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , -----------------------------------------------------------
                --Xuất: Số lượng, Đơn giá, Thành tiền lấy từ Xuất kho, Trả lại hàng mua, mua hàng không qua kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '312', '313', '314', '315',
                '316', '324', '325', '326', '327', '328',
                '362', '363', '364', '365', '366', '374',
                '375', '376', '377', '378'))
                THEN CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id"
                THEN GL."SO_LUONG_XUAT"
                ELSE GL."SO_LUONG_XUAT_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1)
                END
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(CASE
                WHEN (GL."LOAI_CHUNG_TU" IN
                ('2020', '2021', '2022', '2023', '2024', -- đối với chứng từ xuất kho, giảm giá hàng mua, trả lại hàng mua thì lấy thành tiền.
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                AND COALESCE(GL."MA_TK_CO", '') NOT LIKE '133%%'
                THEN GL."SO_TIEN_XUAT"
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_TRONG_CHUNG_TU"


                FROM so_kho_chi_tiet AS GL
                INNER JOIN TMP_LIST_BRAND AS B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_DOI_TUONG_THCP AS J ON GL."MA_DOI_TUONG_THCP_ID" = J."REAL_DOI_TUONG_THCP_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END
                ) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN purchase_document_line PUD ON pud."id" = gl."CHI_TIET_ID"
                AND GL."MA_TK_NO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_NO_ID")
                AND GL."MA_TK_CO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_CO_ID")
                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."order_id"
                WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                AND COALESCE("MA_TK_NO", ''
                ) NOT LIKE '133%%'
                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                AND (GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', -- Nhập kho
                '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', -- Xuất kho
                '3030', '3031', '3032', '3033', -- Trả lại hàng mua
                '3040', '3041', '3042', '3043'
                ) -- Giảm giá hàng mua
                -- Hoặc (Mua hàng qua kho Và VTHH khác DV, Diễn giải)
                OR (GL."LOAI_CHUNG_TU" IN ('302', '307', '308', '309', '310', '318', '319',
                '320', '321', '322', '352', '357', '358', '359',
                '360', '368', '369', '370', '371', '372'
                )
                )
                )
                ----------------
                GROUP BY
                J."DOI_TUONG_THCP_ID",
                J."MA_DOI_TUONG_THCP",
                J."TEN_DOI_TUONG_THCP",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                GL."MA_HANG",
                GL."TEN_HANG",
                GL."KHO_ID",
                GL."MA_KHO",
                GL."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END
                ),
                GL."SO_LUONG_XUAT",
                GL."SO_LUONG_XUAT_THEO_DVT_CHINH",
                GL."DON_GIA",
                GL."SO_LUONG_NHAP",
                GL."SO_LUONG_NHAP_THEO_DVT_CHINH",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_TRONG_CHUNG_TU",
                GL."DVT_ID",
                GL."LOAI_CHUNG_TU",
                U."id"
                ;


                /*Lấy số liệu trường hợp mua hàng không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                J."DOI_TUONG_THCP_ID"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , GL."order_id"                                                                      AS "ID_CHUNG_TU"
                , 'purchase.document'                                                                AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                -- Updated 2019-09-09 by anhtuan
                -- TH mua hàng không qua kho (LOAI_CHUNG_TU=312), MISA lấy SO_CHUNG_TU qua RefNoManagement/RefNoFinance, tùy thuộc vào @IsWorkingWithManagementBook
                -- Tuy nhiên, Cloudify không sử dụng trường này. Do vậy vẫn lấy qua trường SO_CHUNG_TU
                CASE

                WHEN PV."LOAI_CHUNG_TU" NOT IN (312, 313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_PHIEU_NHAP"

                WHEN PV."LOAI_CHUNG_TU" IN (312, 313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_CHUNG_TU"

                ELSE '' END
                , CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."DIEN_GIAI_CHUNG"
                ELSE PV."LY_DO_CHI" END
                , GL."MA_HANG_ID"
                , I."MA"                                                                             AS "MA_HANG"
                , GL."name"                                                                          AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                              AS "DVT"
                , ----------------------------------------------
                ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                             AS "SO_LUONG_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                          AS "DON_GIA_NHAP"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                ROUND(CAST(SUM(GL."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                             AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                                          AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(GL."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_document_line AS GL
                INNER JOIN purchase_document AS PV ON GL."order_id" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_DOI_TUONG_THCP AS J ON GL."DOI_TUONG_THCP_ID" = J."REAL_DOI_TUONG_THCP_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."LOAI_CHUNG_TU" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )

                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = GL."order_id"
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND (PV."LOAI_CHUNG_TU" IN (312, 313, 314, 315, 316, 324, 325,
                326, 327, 328, 362, 363, 364, 365,
                366, 374, 375, 376, 377, 378)
                AND (I."MA" <> N'CPMH'
                OR (I."MA" = N'CPMH'
                --   AND PUDC."CHUNG_TU_ID" IS NULL
                AND GL."id" IS NOT NULL
                )
                )
                )
                ----------------
                GROUP BY
                J."DOI_TUONG_THCP_ID",
                J."MA_DOI_TUONG_THCP",
                J."TEN_DOI_TUONG_THCP",
                GL."order_id",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" NOT IN (312, 313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_PHIEU_NHAP"

                WHEN PV."LOAI_CHUNG_TU" IN (312, 313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_CHUNG_TU"

                ELSE '' END,
                CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."DIEN_GIAI_CHUNG"
                ELSE PV."LY_DO_CHI" END,
                PV."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                I."MA",
                GL."name",

                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."SO_LUONG",
                GL."SO_LUONG_THEO_DVT_CHINH",
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;

                /*Giảm giá hàng mua - Không giảm trừ giá trị hàng trong kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                J."DOI_TUONG_THCP_ID"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"                                                AS "ID_CHUNG_TU"
                , 'purchase.ex.giam.gia.hang.mua'                                                      AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PV."SO_CHUNG_TU"
                , PV."DIEN_GIAI"
                , GL."MA_HANG_ID"
                , I."MA"
                , GL."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                                AS "DVT"
                , ----------------------------------------------
                CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA_NHAP"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                            AS "GIA_TRI_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(GL."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"
                , ---------------------------------------------------------------------

                GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_ex_giam_gia_hang_mua_chi_tiet AS GL
                INNER JOIN purchase_ex_giam_gia_hang_mua AS PV ON GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_DOI_TUONG_THCP AS J ON GL."DOI_TUONG_THCP_ID" = J."REAL_DOI_TUONG_THCP_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."selection_chung_tu_giam_gia_hang_mua" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND PV."LOAI_CHUNG_TU" IN (3042, 3043)

                ----------------
                GROUP BY
                J."DOI_TUONG_THCP_ID",
                J."MA_DOI_TUONG_THCP",
                J."TEN_DOI_TUONG_THCP",
                GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID",
                GL."id",
                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PV."SO_CHUNG_TU",
                PV."DIEN_GIAI",
                PV."DIEN_GIAI",
                GL."MA_HANG_ID",
                I."MA",
                GL."TEN_HANG",

                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;

                /*===========================================================*/
                /*Trả lại hàng mua không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                J."DOI_TUONG_THCP_ID"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID"                                                    AS "ID_CHUNG_TU"
                , 'purchase.ex.tra.lai.hang.mua'                                                       AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" IN (3032)
                THEN PV."SO_CHUNG_TU"

                WHEN PV."LOAI_CHUNG_TU" IN (3033)
                THEN PV."SO_PHIEU_THU"
                ELSE '' END
                , CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PV."DIEN_GIAI"
                ELSE PV."LY_DO_NOP" END
                , --PV."DIEN_GIAI" AS ["DIEN_GIAI"] ,
                GL."MA_HANG_ID"
                , I."MA"
                , GL."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                                AS "DVT"
                , ----------------------------------------------
                CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                            AS "GIA_TRI"
                , ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                               AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA"
                , ROUND(CAST(SUM(GL."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI"
                , ---------------------------------------------------------------------

                GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_ex_tra_lai_hang_mua_chi_tiet AS GL
                INNER JOIN purchase_ex_tra_lai_hang_mua AS PV ON GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_DOI_TUONG_THCP AS J ON GL."DOI_TUONG_THCP_ID" = J."REAL_DOI_TUONG_THCP_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."LOAI_CHUNG_TU" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND PV."LOAI_CHUNG_TU" IN (3032, 3033)

                ----------------
                GROUP BY
                J."DOI_TUONG_THCP_ID",
                J."MA_DOI_TUONG_THCP",
                J."TEN_DOI_TUONG_THCP",
                GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" IN (3032)
                THEN PV."SO_CHUNG_TU"

                WHEN PV."LOAI_CHUNG_TU" IN (3033)
                THEN PV."SO_PHIEU_THU"
                ELSE '' END,
                CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PV."DIEN_GIAI"
                ELSE PV."LY_DO_NOP" END,
                GL."MA_HANG_ID",
                I."MA",
                GL."TEN_HANG",

                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."SO_LUONG",
                GL."SO_LUONG_DVT_CHINH",
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                AS

                SELECT
                "DOI_TUONG_THCP_ID"
                , "MA_DOI_TUONG_THCP"
                , "TEN_DOI_TUONG_THCP"
                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "CHI_NHANH_ID"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , "MA_HANG_ID"
                , "MA_HANG"
                , "TEN_HANG"
                , "KHO_ID"
                , "MA_KHO"
                , "TEN_KHO"
                , "DVT"
                , "SO_LUONG_NHAP"
                , "DON_GIA_NHAP"
                , SUM("GIA_TRI_NHAP") AS "THANH_TIEN_NHAP"
                , "SO_LUONG_XUAT"
                , "DON_GIA_XUAT"
                , SUM("GIA_TRI_XUAT") AS "THANH_TIEN_XUAT"

                , "THU_TU_TRONG_CHUNG_TU"

                FROM TMP_CAN_DOI
                GROUP BY
                "DOI_TUONG_THCP_ID",
                "MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP",
                "ID_CHUNG_TU",
                "MODEL_CHUNG_TU",
                "CHI_NHANH_ID",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG",
                "MA_HANG_ID",
                "MA_HANG",
                "TEN_HANG",
                "KHO_ID",
                "MA_KHO",
                "TEN_KHO",
                "DVT",
                "SO_LUONG_NHAP",
                "DON_GIA_NHAP",
                "SO_LUONG_XUAT",
                "DON_GIA_XUAT",

                "THU_TU_TRONG_CHUNG_TU"

                ;


                UPDATE TMP_KET_QUA
                SET "DON_GIA_NHAP" = ROUND(CAST((CASE WHEN "SO_LUONG_NHAP" = 0
                THEN 0
                ELSE "THANH_TIEN_NHAP"
                / "SO_LUONG_NHAP"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
                "DON_GIA_XUAT" = ROUND(CAST((CASE WHEN "SO_LUONG_XUAT" = 0
                THEN 0
                ELSE "THANH_TIEN_XUAT"
                / "SO_LUONG_XUAT"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;

                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS


                SELECT
                ROW_NUMBER()
                OVER (
                ORDER BY J."MA_DOI_TUONG_THCP", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_HANG",
                "THU_TU_TRONG_CHUNG_TU" ) AS "RowNum"
                , tbl.*

                FROM TMP_KET_QUA tbl
                LEFT JOIN danh_muc_to_chuc OU ON tbl."CHI_NHANH_ID" = OU."id"
                LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON tbl."DOI_TUONG_THCP_ID" = J."id"
                ORDER BY
                J."MA_PHAN_CAP",
                J."MA_DOI_TUONG_THCP",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "MA_HANG",
                "THU_TU_TRONG_CHUNG_TU"
                ;
                END $$
                ;

                SELECT 
                "MA_DOI_TUONG_THCP" AS"MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP" AS "TEN_DOI_TUONG_THCP",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG" AS "DIEN_GIAI_CHUNG",
                "MA_HANG" AS "MA_HANG",
                "TEN_HANG" AS "TEN_HANG",
                "TEN_KHO" AS "TEN_KHO",
                "DVT" AS "DVT",
                "SO_LUONG_NHAP" AS "SO_LUONG_NHAP",
                "DON_GIA_NHAP" AS "DON_GIA_NHAP",
                "THANH_TIEN_NHAP" AS "THANH_TIEN_NHAP",
                "SO_LUONG_XUAT" AS "SO_LUONG_XUAT",
                "DON_GIA_XUAT" AS "DON_GIA_XUAT",
                "THANH_TIEN_XUAT" AS "THANH_TIEN_XUAT",
                "ID_CHUNG_TU" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC"

                FROM TMP_KET_QUA_CUOI_CUNG
                ORDER BY "RowNum"
                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)

    #  Thống kê theo công trình
    def _lay_bao_cao_cong_trinh(self, params_sql):      
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

                den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

                PHAN_THAP_PHAN_SO_LUONG             INTEGER;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INTEGER;

                PHAN_THAP_PHAN_DON_GIA              INTEGER;



                VTHH_IDS                            INTEGER := -1;

                loai_dvt                            INTEGER := %(DON_VI_TINH)s;

                rec                                 RECORD;

                --@ListProjectWorkID--Tham số bên misa
                --@InventoryItemID ----Tham số bên misa


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


                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                AS
                SELECT *
                FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;

                DROP TABLE IF EXISTS TMP_CONG_TRINH_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_DUOC_CHON


                (
                "CONG_TRINH_ID"  INT PRIMARY KEY,
                "MA_CONG_TRINH"  VARCHAR(25),
                "TEN_CONG_TRINH" VARCHAR(128),
                "MA_PHAN_CAP"    VARCHAR(100)
                )
                ;

                INSERT INTO TMP_CONG_TRINH_DUOC_CHON
                SELECT
                P."id"
                , P."MA_CONG_TRINH"
                , P."TEN_CONG_TRINH"
                , P."MA_PHAN_CAP"
                FROM
                danh_muc_cong_trinh AS P
                WHERE P."id" = any(%(CONG_TRINH_IDS)s) --ListProjectWorkID
                ;

                -----------------------------------------
                --Công trình con được chọn hoặc công trình cha được chọn (nhưng không có con được chọn)
                DROP TABLE IF EXISTS TMP_CONG_TRINH_CHA_CON_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_CHA_CON_DUOC_CHON


                (
                "CONG_TRINH_ID"  INT PRIMARY KEY,
                "MA_PHAN_CAP"    VARCHAR(100),
                "MA_CONG_TRINH"  VARCHAR(20),
                "TEN_CONG_TRINH" VARCHAR(128)
                )
                ;

                INSERT INTO TMP_CONG_TRINH_CHA_CON_DUOC_CHON
                SELECT
                S."CONG_TRINH_ID"
                , S."MA_PHAN_CAP"
                , S."MA_CONG_TRINH"
                , S."TEN_CONG_TRINH"
                FROM TMP_CONG_TRINH_DUOC_CHON S
                LEFT JOIN TMP_CONG_TRINH_DUOC_CHON S1
                ON S1."MA_PHAN_CAP" LIKE S."MA_PHAN_CAP" || '%%' AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE S1."MA_PHAN_CAP" IS NULL
                ;

                --Những công trình con được chọn (không chọn cha) và những công trình con của những công trình cha được chọn (nhưng không có con được chọn)

                DROP TABLE IF EXISTS TMP_DS_CONG_TRINH
                ;

                CREATE TEMP TABLE TMP_DS_CONG_TRINH

                (
                "CONG_TRINH_ID"  INT PRIMARY KEY,
                "MA_PHAN_CAP"    VARCHAR(100),
                "MA_CONG_TRINH"  VARCHAR(20),
                "TEN_CONG_TRINH" VARCHAR(128)
                )
                ;

                INSERT INTO TMP_DS_CONG_TRINH
                SELECT DISTINCT
                PW."id"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"
                FROM TMP_CONG_TRINH_CHA_CON_DUOC_CHON SPW
                INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE SPW."MA_PHAN_CAP" || '%%'

                ;


                DROP TABLE IF EXISTS TMP_DS_VAT_TU_HH
                ;

                CREATE TEMP TABLE TMP_DS_VAT_TU_HH
                -- Bảng chứa danh sách hàng hóa
                (
                "MA_HANG_ID" INT,
                "MA_HANG"    VARCHAR(255),
                "DVT_ID"     INT


                )
                ;

                IF VTHH_IDS IS NULL
                THEN
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM danh_muc_vat_tu_hang_hoa
                ;
                ELSE
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM
                danh_muc_vat_tu_hang_hoa II
                WHERE II."id" = any(%(SAN_PHAM_IDS)s)--InventoryItemID
                ;
                END IF
                ;

                -----------------------------------------


                DROP TABLE IF EXISTS TMP_CAN_DOI
                ;

                CREATE TEMP TABLE TMP_CAN_DOI
                AS

                SELECT
                PWC."CONG_TRINH_ID"
                , PWC."MA_CONG_TRINH"
                , PWC."TEN_CONG_TRINH"

                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."CHI_NHANH_ID"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."DIEN_GIAI_CHUNG"
                , GL."MA_HANG_ID"
                , GL."MA_HANG"
                , GL."TEN_HANG"
                , GL."KHO_ID"
                , GL."MA_KHO"
                , GL."TEN_KHO"
                , (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                            AS "DVT"
                , ----------------------------------------------

                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '3040', '3041', '3042', '3043', '2021'))
                THEN 0
                ELSE CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id" -- Nếu ĐVT trên chứng từ = ĐVT chọn trên tham số -> Lấy số lượng trên chứng từ
                THEN GL."SO_LUONG_NHAP"
                ELSE GL."SO_LUONG_NHAP_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1) -- Nếu ĐVT trên chứng từ <> ĐVT trên tham số thì lấy số lượng được tính qua tỷ lệ chuyển đổi trên danh mục
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_NHAP"
                , --Đoạn này xuống dưới tính lại = Thành tiền / Số lượng
                CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_NHAP"
                , ROUND(CAST(SUM(CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024',
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                THEN 0
                ELSE CASE
                -- chứng từ nhập kho thì lấy thành tiền
                WHEN GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012',
                '2013', '2014', '2015',
                '2016', '2017') --nhập kho
                THEN GL."SO_TIEN_NHAP"
                --MUA HÀNG nhập kho thì không lấy VTHH có tính chất diễn giải.
                WHEN GL."LOAI_CHUNG_TU" IN ('302', '307', '308',
                '309', '310', '318',
                '319', '320', '321',
                '322', '352', '357',
                '358', '359', '360',
                '368', '369', '370',
                '371', '372')
                AND I."TINH_CHAT" <> '2'
                AND I."TINH_CHAT" <> '3'
                THEN ROUND(CAST((GL."SO_TIEN_NHAP") AS NUMERIC),
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)


                ELSE 0
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , -----------------------------------------------------------
                --Xuất: Số lượng, Đơn giá, Thành tiền lấy từ Xuất kho, Trả lại hàng mua, mua hàng không qua kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '312', '313', '314', '315',
                '316', '324', '325', '326', '327', '328',
                '362', '363', '364', '365', '366', '374',
                '375', '376', '377', '378'))
                THEN CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id"
                THEN GL."SO_LUONG_XUAT"
                ELSE GL."SO_LUONG_XUAT_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1)
                END
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(CASE
                WHEN (GL."LOAI_CHUNG_TU" IN
                ('2020', '2021', '2022', '2023', '2024', -- đối với chứng từ xuất kho, giảm giá hàng mua, trả lại hàng mua thì lấy thành tiền.
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                AND COALESCE(GL."MA_TK_CO", '') NOT LIKE '133%%'
                THEN GL."SO_TIEN_XUAT"
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_TRONG_CHUNG_TU"


                FROM so_kho_chi_tiet AS GL
                INNER JOIN TMP_LIST_BRAND AS B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_CONG_TRINH AS J ON GL."CONG_TRINH_ID" = J."CONG_TRINH_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END
                ) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN purchase_document_line PUD ON pud."id" = gl."CHI_TIET_ID"
                AND GL."MA_TK_NO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_NO_ID")
                AND GL."MA_TK_CO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_CO_ID")
                LEFT JOIN TMP_CONG_TRINH_CHA_CON_DUOC_CHON PWC ON J."MA_PHAN_CAP" LIKE PWC."MA_PHAN_CAP"
                || '%%'
                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."order_id"
                WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                AND COALESCE("MA_TK_NO", ''
                ) NOT LIKE '133%%'
                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                AND (GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', -- Nhập kho
                '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', -- Xuất kho
                '3030', '3031', '3032', '3033', -- Trả lại hàng mua
                '3040', '3041', '3042', '3043'
                ) -- Giảm giá hàng mua
                -- Hoặc (Mua hàng qua kho Và VTHH khác DV, Diễn giải)
                OR (GL."LOAI_CHUNG_TU" IN ('302', '307', '308', '309', '310', '318', '319',
                '320', '321', '322', '352', '357', '358', '359',
                '360', '368', '369', '370', '371', '372'
                )
                )
                )
                ----------------
                GROUP BY
                PWC."CONG_TRINH_ID",
                PWC."MA_CONG_TRINH",
                PWC."TEN_CONG_TRINH",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                GL."MA_HANG",
                GL."TEN_HANG",
                GL."KHO_ID",
                GL."MA_KHO",
                GL."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END
                ),
                GL."SO_LUONG_XUAT",
                GL."SO_LUONG_XUAT_THEO_DVT_CHINH",
                GL."DON_GIA",
                GL."SO_LUONG_NHAP",
                GL."SO_LUONG_NHAP_THEO_DVT_CHINH",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_TRONG_CHUNG_TU",
                GL."DVT_ID",
                GL."LOAI_CHUNG_TU",
                U."id"
                ;


                /*Lấy số liệu trường hợp mua hàng không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                PWC."CONG_TRINH_ID"
                , PWC."MA_CONG_TRINH"
                , PWC."TEN_CONG_TRINH"
                , GL."order_id"                                                                      AS "ID_CHUNG_TU"
                , 'purchase.document'                                                                AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_PHIEU_NHAP"

                WHEN PV."LOAI_CHUNG_TU" IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_CHUNG_TU"

                ELSE '' END
                , CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."DIEN_GIAI_CHUNG"
                ELSE PV."LY_DO_CHI" END
                , GL."MA_HANG_ID"
                , I."MA"                                                                             AS "MA_HANG"
                , GL."name"                                                                          AS "TEN_HANG"
                , GL."KHO_ID"
                , S."MA_KHO"
                , S."TEN_KHO"

                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                              AS "DVT"
                , ----------------------------------------------
                ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                             AS "SO_LUONG_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                          AS "DON_GIA_NHAP"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                ROUND(CAST(SUM(GL."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                             AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                                          AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(GL."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_document_line AS GL
                INNER JOIN purchase_document AS PV ON GL."order_id" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_CONG_TRINH AS J ON GL."CONG_TRINH_ID" = J."CONG_TRINH_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."LOAI_CHUNG_TU" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN TMP_CONG_TRINH_CHA_CON_DUOC_CHON PWC ON J."MA_PHAN_CAP" LIKE PWC."MA_PHAN_CAP"
                || '%%'

                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = GL."order_id"
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND (PV."LOAI_CHUNG_TU" IN (312, 313, 314, 315, 316, 324, 325,
                326, 327, 328, 362, 363, 364, 365,
                366, 374, 375, 376, 377, 378)
                AND (I."MA" <> N'CPMH'
                OR (I."MA" = N'CPMH'
                --   AND PUDC."CHUNG_TU_ID" IS NULL
                AND GL."id" IS NOT NULL
                )
                )
                )
                ----------------
                GROUP BY
                PWC."CONG_TRINH_ID",
                PWC."MA_CONG_TRINH",
                PWC."TEN_CONG_TRINH",
                GL."order_id",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_PHIEU_NHAP"

                WHEN PV."LOAI_CHUNG_TU" IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_CHUNG_TU"

                ELSE '' END,
                CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."DIEN_GIAI_CHUNG"
                ELSE PV."LY_DO_CHI" END,
                PV."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                I."MA",
                GL."name",
                GL."KHO_ID",
                S."MA_KHO",
                S."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."SO_LUONG",
                GL."SO_LUONG_THEO_DVT_CHINH",
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;

                /*Giảm giá hàng mua - Không giảm trừ giá trị hàng trong kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                PWC."CONG_TRINH_ID"
                , PWC."MA_CONG_TRINH"
                , PWC."TEN_CONG_TRINH"
                , GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"                                                AS "ID_CHUNG_TU"
                , 'purchase.ex.giam.gia.hang.mua'                                                      AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PV."SO_CHUNG_TU"
                , PV."DIEN_GIAI"
                , GL."MA_HANG_ID"
                , I."MA"
                , GL."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                                AS "DVT"
                , ----------------------------------------------
                CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA_NHAP"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                            AS "GIA_TRI_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(GL."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"
                , ---------------------------------------------------------------------

                GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_ex_giam_gia_hang_mua_chi_tiet AS GL
                INNER JOIN purchase_ex_giam_gia_hang_mua AS PV ON GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_CONG_TRINH AS J ON GL."CONG_TRINH_ID" = J."CONG_TRINH_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."selection_chung_tu_giam_gia_hang_mua" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN TMP_CONG_TRINH_CHA_CON_DUOC_CHON PWC ON J."MA_PHAN_CAP" LIKE PWC."MA_PHAN_CAP"
                || '%%'
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND PV."LOAI_CHUNG_TU" IN (3042, 3043)

                ----------------
                GROUP BY
                PWC."CONG_TRINH_ID",
                PWC."MA_CONG_TRINH",
                PWC."TEN_CONG_TRINH",
                GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PV."SO_CHUNG_TU",
                PV."DIEN_GIAI",
                PV."DIEN_GIAI",
                GL."MA_HANG_ID",
                I."MA",
                GL."TEN_HANG",

                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;

                /*===========================================================*/
                /*Trả lại hàng mua không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                PWC."CONG_TRINH_ID"
                , PWC."MA_CONG_TRINH"
                , PWC."TEN_CONG_TRINH"
                , GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID"                                                    AS "ID_CHUNG_TU"
                , 'purchase.ex.tra.lai.hang.mua'                                                       AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" IN (3032)
                THEN PV."SO_CHUNG_TU"

                WHEN PV."LOAI_CHUNG_TU" IN (3033)
                THEN PV."SO_PHIEU_THU"
                ELSE '' END
                , CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PV."DIEN_GIAI"
                ELSE PV."LY_DO_NOP" END
                , --PV."DIEN_GIAI" AS ["DIEN_GIAI"] ,
                GL."MA_HANG_ID"
                , I."MA"
                , GL."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                                AS "DVT"
                , ----------------------------------------------
                CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                            AS "GIA_TRI"
                , ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                               AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA"
                , ROUND(CAST(SUM(GL."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI"
                , ---------------------------------------------------------------------

                GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_ex_tra_lai_hang_mua_chi_tiet AS GL
                INNER JOIN purchase_ex_tra_lai_hang_mua AS PV ON GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DS_CONG_TRINH AS J ON GL."CONG_TRINH_ID" = J."CONG_TRINH_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."LOAI_CHUNG_TU" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN TMP_CONG_TRINH_CHA_CON_DUOC_CHON PWC ON J."MA_PHAN_CAP" LIKE PWC."MA_PHAN_CAP"
                || '%%'
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND PV."LOAI_CHUNG_TU" IN (3032, 3033)

                ----------------
                GROUP BY
                PWC."CONG_TRINH_ID",
                PWC."MA_CONG_TRINH",
                PWC."TEN_CONG_TRINH",
                GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" IN (3032)
                THEN PV."SO_CHUNG_TU"

                WHEN PV."LOAI_CHUNG_TU" IN (3033)
                THEN PV."SO_PHIEU_THU"
                ELSE '' END,
                CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PV."DIEN_GIAI"
                ELSE PV."LY_DO_NOP" END,
                GL."MA_HANG_ID",
                I."MA",
                GL."TEN_HANG",

                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."SO_LUONG",
                GL."SO_LUONG_DVT_CHINH",
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                AS

                SELECT
                "CONG_TRINH_ID"
                , "MA_CONG_TRINH"
                , "TEN_CONG_TRINH"

                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "CHI_NHANH_ID"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , "MA_HANG_ID"
                , "MA_HANG"
                , "TEN_HANG"
                , "KHO_ID"
                , "MA_KHO"
                , "TEN_KHO"
                , "DVT"
                , "SO_LUONG_NHAP"
                , "DON_GIA_NHAP"
                , SUM("GIA_TRI_NHAP") AS "THANH_TIEN_NHAP"
                , "SO_LUONG_XUAT"
                , "DON_GIA_XUAT"
                , SUM("GIA_TRI_XUAT") AS "THANH_TIEN_XUAT"

                , "THU_TU_TRONG_CHUNG_TU"

                FROM TMP_CAN_DOI
                GROUP BY
                "CONG_TRINH_ID" ,
                "MA_CONG_TRINH" ,
                "TEN_CONG_TRINH" ,
                "ID_CHUNG_TU",
                "MODEL_CHUNG_TU",
                "CHI_NHANH_ID",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG",
                "MA_HANG_ID",
                "MA_HANG",
                "TEN_HANG",
                "KHO_ID",
                "MA_KHO",
                "TEN_KHO",
                "DVT",
                "SO_LUONG_NHAP",
                "DON_GIA_NHAP",
                "SO_LUONG_XUAT",
                "DON_GIA_XUAT",

                "THU_TU_TRONG_CHUNG_TU"

                ;


                UPDATE TMP_KET_QUA
                SET "DON_GIA_NHAP" = ROUND(CAST((CASE WHEN "SO_LUONG_NHAP" = 0
                THEN 0
                ELSE "THANH_TIEN_NHAP"
                / "SO_LUONG_NHAP"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
                "DON_GIA_XUAT" = ROUND(CAST((CASE WHEN "SO_LUONG_XUAT" = 0
                THEN 0
                ELSE "THANH_TIEN_XUAT"
                / "SO_LUONG_XUAT"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;

                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS


                SELECT
                ROW_NUMBER()
                OVER (
                ORDER BY PJ."MA_CONG_TRINH", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_HANG",
                "THU_TU_TRONG_CHUNG_TU" ) AS "RowNum"
                , tbl.*

                FROM TMP_KET_QUA tbl
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = tbl."CHI_NHANH_ID"
                LEFT JOIN danh_muc_cong_trinh PJ ON tbl."MA_CONG_TRINH" = PJ."MA_CONG_TRINH"
                ORDER BY
                PJ."MA_PHAN_CAP",
                PJ."MA_CONG_TRINH",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "MA_HANG",
                "THU_TU_TRONG_CHUNG_TU"
                ;

                END $$
                ;

                SELECT 
                "MA_CONG_TRINH" AS "MA_CONG_TRINH",
                "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG" AS "DIEN_GIAI_CHUNG",
                "MA_HANG" AS "MA_HANG",
                "TEN_HANG" AS "TEN_HANG",
                "TEN_KHO" AS "TEN_KHO",
                "DVT" AS "DVT",
                "SO_LUONG_NHAP" AS "SO_LUONG_NHAP",
                "DON_GIA_NHAP" AS "DON_GIA_NHAP",
                "THANH_TIEN_NHAP" AS "THANH_TIEN_NHAP",
                "SO_LUONG_XUAT" AS "SO_LUONG_XUAT",
                "DON_GIA_XUAT" AS "DON_GIA_XUAT",
                "THANH_TIEN_XUAT" AS "THANH_TIEN_XUAT",
                "ID_CHUNG_TU" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC"

                FROM TMP_KET_QUA_CUOI_CUNG
                ORDER BY "RowNum"
                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)

    def _lay_bao_cao_don_hang(self, params_sql):      
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

                den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


                PHAN_THAP_PHAN_SO_LUONG             INTEGER;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INTEGER;

                PHAN_THAP_PHAN_DON_GIA              INTEGER;


                VTHH_IDS                            INTEGER := -1;

                loai_dvt                            INTEGER := %(DON_VI_TINH)s;

                rec                                 RECORD;

                --@ListSAOrderID--Tham số bên misa
                --@InventoryItemID ----Tham số bên misa


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


                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                AS
                SELECT *
                FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;

                DROP TABLE IF EXISTS TMP_DON_HANG
                ;

                CREATE TEMP TABLE TMP_DON_HANG
                AS

                SELECT
                id                AS "DON_DAT_HANG_ID"
                , O."SO_DON_HANG"   AS "DON_DAT_HANG"
                , O."NGAY_DON_HANG" AS "NGAY_DON_HANG"

                FROM account_ex_don_dat_hang AS O
                WHERE O."id" = any(%(DON_HANG_IDS)s) --@ListSAOrderID
                ;

                --@ListSAOrderID


                DROP TABLE IF EXISTS TMP_DS_VAT_TU_HH
                ;

                CREATE TEMP TABLE TMP_DS_VAT_TU_HH
                -- Bảng chứa danh sách hàng hóa
                (
                "MA_HANG_ID" INT,
                "MA_HANG"    VARCHAR(255),
                "DVT_ID"     INT
                )
                ;

                IF VTHH_IDS IS NULL
                THEN
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM danh_muc_vat_tu_hang_hoa
                ;
                ELSE
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM
                danh_muc_vat_tu_hang_hoa II
                WHERE II."id" = any(%(SAN_PHAM_IDS)s)--InventoryItemID
                ;
                END IF
                ;

                -----------------------------------------


                DROP TABLE IF EXISTS TMP_CAN_DOI
                ;

                CREATE TEMP TABLE TMP_CAN_DOI
                AS

                SELECT
                GL."DON_DAT_HANG_ID"
                , O."DON_DAT_HANG"
                , O."NGAY_DON_HANG"


                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."CHI_NHANH_ID"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."DIEN_GIAI_CHUNG"
                , GL."MA_HANG_ID"
                , GL."MA_HANG"
                , GL."TEN_HANG"
                , GL."KHO_ID"
                , GL."MA_KHO"
                , GL."TEN_KHO"
                , (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                            AS "DVT"
                , ----------------------------------------------

                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '3040', '3041', '3042', '3043', '2021'))
                THEN 0
                ELSE CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id" -- Nếu ĐVT trên chứng từ = ĐVT chọn trên tham số -> Lấy số lượng trên chứng từ
                THEN GL."SO_LUONG_NHAP"
                ELSE GL."SO_LUONG_NHAP_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1) -- Nếu ĐVT trên chứng từ <> ĐVT trên tham số thì lấy số lượng được tính qua tỷ lệ chuyển đổi trên danh mục
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_NHAP"
                , --Đoạn này xuống dưới tính lại = Thành tiền / Số lượng
                CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_NHAP"
                , ROUND(CAST(SUM(CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024',
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                THEN 0
                ELSE CASE
                -- chứng từ nhập kho thì lấy thành tiền
                WHEN GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012',
                '2013', '2014', '2015',
                '2016', '2017') --nhập kho
                THEN GL."SO_TIEN_NHAP"
                --MUA HÀNG nhập kho thì không lấy VTHH có tính chất diễn giải.
                WHEN GL."LOAI_CHUNG_TU" IN ('302', '307', '308',
                '309', '310', '318',
                '319', '320', '321',
                '322', '352', '357',
                '358', '359', '360',
                '368', '369', '370',
                '371', '372')
                AND I."TINH_CHAT" <> '2'
                AND I."TINH_CHAT" <> '3'
                THEN ROUND(CAST((GL."SO_TIEN_NHAP") AS NUMERIC),
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)



                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , -----------------------------------------------------------
                --Xuất: Số lượng, Đơn giá, Thành tiền lấy từ Xuất kho, Trả lại hàng mua, mua hàng không qua kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '312', '313', '314', '315',
                '316', '324', '325', '326', '327', '328',
                '362', '363', '364', '365', '366', '374',
                '375', '376', '377', '378'))
                THEN CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id"
                THEN GL."SO_LUONG_XUAT"
                ELSE GL."SO_LUONG_XUAT_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1)
                END
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(CASE
                WHEN (GL."LOAI_CHUNG_TU" IN
                ('2020', '2021', '2022', '2023', '2024', -- đối với chứng từ xuất kho, giảm giá hàng mua, trả lại hàng mua thì lấy thành tiền.
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                AND COALESCE(GL."MA_TK_CO", '') NOT LIKE '133%%'
                THEN GL."SO_TIEN_XUAT"
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_TRONG_CHUNG_TU"


                FROM so_kho_chi_tiet AS GL
                INNER JOIN TMP_LIST_BRAND AS B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DON_HANG AS O ON GL."DON_DAT_HANG_ID" = O."DON_DAT_HANG_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END
                ) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN purchase_document_line PUD ON pud."id" = gl."CHI_TIET_ID"
                AND GL."MA_TK_NO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_NO_ID")
                AND GL."MA_TK_CO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_CO_ID")

                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."order_id"
                WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                AND COALESCE("MA_TK_NO", ''
                ) NOT LIKE '133%%'
                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                AND (GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', -- Nhập kho
                '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', -- Xuất kho
                '3030', '3031', '3032', '3033', -- Trả lại hàng mua
                '3040', '3041', '3042', '3043'
                ) -- Giảm giá hàng mua
                -- Hoặc (Mua hàng qua kho Và VTHH khác DV, Diễn giải)
                OR (GL."LOAI_CHUNG_TU" IN ('302', '307', '308', '309', '310', '318', '319',
                '320', '321', '322', '352', '357', '358', '359',
                '360', '368', '369', '370', '371', '372'
                )
                )
                )
                ----------------
                GROUP BY
                GL."DON_DAT_HANG_ID",
                O."DON_DAT_HANG",
                O."NGAY_DON_HANG",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                GL."MA_HANG",
                GL."TEN_HANG",
                GL."KHO_ID",
                GL."MA_KHO",
                GL."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END
                ),
                GL."SO_LUONG_XUAT",
                GL."SO_LUONG_XUAT_THEO_DVT_CHINH",
                GL."DON_GIA",
                GL."SO_LUONG_NHAP",
                GL."SO_LUONG_NHAP_THEO_DVT_CHINH",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_TRONG_CHUNG_TU",
                GL."DVT_ID",
                GL."LOAI_CHUNG_TU",
                U."id"
                ;


                /*Lấy số liệu trường hợp mua hàng không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                GL."DON_DAT_HANG_ID"
                , O."DON_DAT_HANG"
                , O."NGAY_DON_HANG"
                , GL."order_id"                                                                      AS "ID_CHUNG_TU"
                , 'purchase.document'                                                                AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_PHIEU_NHAP"

                WHEN PV."LOAI_CHUNG_TU" IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_CHUNG_TU"

                ELSE '' END
                , CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."DIEN_GIAI_CHUNG"
                ELSE PV."LY_DO_CHI" END
                , GL."MA_HANG_ID"
                , I."MA"                                                                             AS "MA_HANG"
                , GL."name"                                                                          AS "TEN_HANG"
                , GL."KHO_ID"
                , S."MA_KHO"
                , S."TEN_KHO"

                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                              AS "DVT"
                , ----------------------------------------------
                ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                             AS "SO_LUONG_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                          AS "DON_GIA_NHAP"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                ROUND(CAST(SUM(GL."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                             AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                                          AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(GL."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_document_line AS GL
                INNER JOIN purchase_document AS PV ON GL."order_id" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DON_HANG AS O ON GL."DON_DAT_HANG_ID" = O."DON_DAT_HANG_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."LOAI_CHUNG_TU" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )


                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = GL."order_id"
                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND (PV."LOAI_CHUNG_TU" IN (312, 313, 314, 315, 316, 324, 325,
                326, 327, 328, 362, 363, 364, 365,
                366, 374, 375, 376, 377, 378)
                AND (I."MA" <> N'CPMH'
                OR (I."MA" = N'CPMH'
                --   AND PUDC."CHUNG_TU_ID" IS NULL
                AND GL."id" IS NOT NULL
                )
                )
                )
                ----------------
                GROUP BY
                GL."DON_DAT_HANG_ID",
                O."DON_DAT_HANG",
                O."NGAY_DON_HANG",
                GL."order_id",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_PHIEU_NHAP"

                WHEN PV."LOAI_CHUNG_TU" IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."SO_CHUNG_TU"

                ELSE '' END,
                CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PV."DIEN_GIAI_CHUNG"
                ELSE PV."LY_DO_CHI" END,
                PV."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                I."MA",
                GL."name",
                GL."KHO_ID",
                S."MA_KHO",
                S."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."SO_LUONG",
                GL."SO_LUONG_THEO_DVT_CHINH",
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;

                /*Giảm giá hàng mua - Không giảm trừ giá trị hàng trong kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                GL."DON_DAT_HANG_ID"
                , O."DON_DAT_HANG"
                , O."NGAY_DON_HANG"
                , GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"                                                AS "ID_CHUNG_TU"
                , 'purchase.ex.giam.gia.hang.mua'                                                      AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PV."SO_CHUNG_TU"
                , PV."DIEN_GIAI"
                , GL."MA_HANG_ID"
                , I."MA"
                , GL."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                                AS "DVT"
                , ----------------------------------------------
                CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA_NHAP"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                            AS "GIA_TRI_NHAP"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(GL."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"
                , ---------------------------------------------------------------------

                GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_ex_giam_gia_hang_mua_chi_tiet AS GL
                INNER JOIN purchase_ex_giam_gia_hang_mua AS PV ON GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DON_HANG AS O ON GL."DON_DAT_HANG_ID" = O."DON_DAT_HANG_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."selection_chung_tu_giam_gia_hang_mua" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )

                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND PV."LOAI_CHUNG_TU" IN (3042, 3043)

                ----------------
                GROUP BY
                GL."DON_DAT_HANG_ID",
                O."DON_DAT_HANG",
                O."NGAY_DON_HANG",
                GL."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PV."SO_CHUNG_TU",
                PV."DIEN_GIAI",
                PV."DIEN_GIAI",
                GL."MA_HANG_ID",
                I."MA",
                GL."TEN_HANG",

                GL."KHO_ID",
                S."MA_KHO",
                S."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;

                /*===========================================================*/
                /*Trả lại hàng mua không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                GL."DON_DAT_HANG_ID"
                , O."DON_DAT_HANG"
                , O."NGAY_DON_HANG"
                , GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID"                                                    AS "ID_CHUNG_TU"
                , 'purchase.ex.tra.lai.hang.mua'                                                       AS "MODEL_CHUNG_TU"
                , PV."CHI_NHANH_ID"
                , PV."NGAY_HACH_TOAN"
                , PV."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" IN (3032)
                THEN PV."SO_CHUNG_TU"

                WHEN PV."LOAI_CHUNG_TU" IN (3033)
                THEN PV."SO_PHIEU_THU"
                ELSE '' END
                , CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PV."DIEN_GIAI"
                ELSE PV."LY_DO_NOP" END
                , --PV."DIEN_GIAI" AS ["DIEN_GIAI"] ,
                GL."MA_HANG_ID"
                , I."MA"
                , GL."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --GL."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                                                AS "DVT"
                , ----------------------------------------------
                CAST(0 AS DECIMAL(18, 4))                                                            AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                            AS "GIA_TRI"
                , ROUND(CAST((CASE WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" = U."id"
                THEN GL."SO_LUONG"
                ELSE GL."SO_LUONG_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                               AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                            AS "DON_GIA"
                , ROUND(CAST(SUM(GL."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI"
                , ---------------------------------------------------------------------

                GL."THU_TU_SAP_XEP_CHI_TIET"

                FROM purchase_ex_tra_lai_hang_mua_chi_tiet AS GL
                INNER JOIN purchase_ex_tra_lai_hang_mua AS PV ON GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PV."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PV."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN TMP_DON_HANG AS O ON GL."DON_DAT_HANG_ID" = O."DON_DAT_HANG_ID"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = Gl."KHO_ID"
                -- LEFT JOIN danh_muc_reftype AS SRT ON PV."LOAI_CHUNG_TU" = SRT."LOAI_CHUNG_TU"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )

                WHERE PV."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PV."state" = 'da_ghi_so')

                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                AND PV."LOAI_CHUNG_TU" IN (3032, 3033)

                ----------------
                GROUP BY
                GL."DON_DAT_HANG_ID",
                O."DON_DAT_HANG",
                O."NGAY_DON_HANG",
                GL."CHUNG_TU_TRA_LAI_HANG_MUA_ID",

                PV."CHI_NHANH_ID",
                PV."NGAY_HACH_TOAN",
                PV."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PV."LOAI_CHUNG_TU" IN (3032)
                THEN PV."SO_CHUNG_TU"

                WHEN PV."LOAI_CHUNG_TU" IN (3033)
                THEN PV."SO_PHIEU_THU"
                ELSE '' END,
                CASE WHEN PV."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PV."DIEN_GIAI"
                ELSE PV."LY_DO_NOP" END,
                GL."MA_HANG_ID",
                I."MA",
                GL."TEN_HANG",

                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END),
                GL."SO_LUONG",
                GL."SO_LUONG_DVT_CHINH",
                GL."DON_GIA",
                PV."LOAI_CHUNG_TU",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_SAP_XEP_CHI_TIET",
                GL."DVT_ID",
                U."id"

                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                AS

                SELECT
                "DON_DAT_HANG_ID"
                , "DON_DAT_HANG"
                , "NGAY_DON_HANG"
                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "CHI_NHANH_ID"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , "MA_HANG_ID"
                , "MA_HANG"
                , "TEN_HANG"
                , "KHO_ID"
                , "MA_KHO"
                , "TEN_KHO"
                , "DVT"
                , "SO_LUONG_NHAP"
                , "DON_GIA_NHAP"
                , SUM("GIA_TRI_NHAP") AS "THANH_TIEN_NHAP"
                , "SO_LUONG_XUAT"
                , "DON_GIA_XUAT"
                , SUM("GIA_TRI_XUAT") AS "THANH_TIEN_XUAT"

                , "THU_TU_TRONG_CHUNG_TU"

                FROM TMP_CAN_DOI
                GROUP BY
                "DON_DAT_HANG_ID" ,
                "DON_DAT_HANG" ,
                "NGAY_DON_HANG" ,
                "ID_CHUNG_TU",
                "MODEL_CHUNG_TU",
                "CHI_NHANH_ID",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG",
                "MA_HANG_ID",
                "MA_HANG",
                "TEN_HANG",
                "KHO_ID",
                "MA_KHO",
                "TEN_KHO",
                "DVT",
                "SO_LUONG_NHAP",
                "DON_GIA_NHAP",
                "SO_LUONG_XUAT",
                "DON_GIA_XUAT",

                "THU_TU_TRONG_CHUNG_TU"

                ;


                UPDATE TMP_KET_QUA
                SET "DON_GIA_NHAP" = ROUND(CAST((CASE WHEN "SO_LUONG_NHAP" = 0
                THEN 0
                ELSE "THANH_TIEN_NHAP"
                / "SO_LUONG_NHAP"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
                "DON_GIA_XUAT" = ROUND(CAST((CASE WHEN "SO_LUONG_XUAT" = 0
                THEN 0
                ELSE "THANH_TIEN_XUAT"
                / "SO_LUONG_XUAT"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;

                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS


                SELECT  ROW_NUMBER() OVER ( ORDER BY "DON_DAT_HANG", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_HANG", "THU_TU_TRONG_CHUNG_TU" ) AS "RowNum" ,
                * ,
                OU."TEN_DON_VI" "CHI_NHANH"
                FROM    ( SELECT    *
                FROM      TMP_KET_QUA

                ) tbl
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = tbl."CHI_NHANH_ID"
                ;

                END $$
                ;

                SELECT 
                "DON_DAT_HANG" AS "SO_DON_HANG",
                "NGAY_DON_HANG" AS "NGAY_DON_HANG",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG" AS "DIEN_GIAI_CHUNG",
                "MA_HANG" AS "MA_HANG",
                "TEN_HANG" AS "TEN_HANG",
                "TEN_KHO" AS "TEN_KHO",
                "DVT" AS "DVT",
                "SO_LUONG_NHAP" AS "SO_LUONG_NHAP",
                "DON_GIA_NHAP" AS "DON_GIA_NHAP",
                "THANH_TIEN_NHAP" AS "THANH_TIEN_NHAP",
                "SO_LUONG_XUAT" AS "SO_LUONG_XUAT",
                "DON_GIA_XUAT" AS "DON_GIA_XUAT",
                "THANH_TIEN_XUAT" AS "THANH_TIEN_XUAT",
                "ID_CHUNG_TU" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC"

                FROM TMP_KET_QUA_CUOI_CUNG
                ORDER BY "RowNum"
                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_hop_dong(self, params_sql):      
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

                den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

                PHAN_THAP_PHAN_SO_LUONG             INTEGER;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INTEGER;

                PHAN_THAP_PHAN_DON_GIA              INTEGER;

                VTHH_IDS                            INTEGER := -1;

                loai_dvt                            INTEGER := %(DON_VI_TINH)s;

                rec                                 RECORD;

                --@ListContractID--Tham số bên misa
                --@InventoryItemID ----Tham số bên misa

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


                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                AS
                SELECT *
                FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS TMP_HOP_DONG_DU_AN_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_HOP_DONG_DU_AN_DUOC_CHON


                (
                "HOP_DONG_ID"    INT PRIMARY KEY,
                "SO_HOP_DONG"    VARCHAR(50),
                "THUOC_DU_AN_ID" INT,
                "NGAY_KY"        TIMESTAMP,
                "TRICH_YEU"      VARCHAR(255)
                ,
                "DOI_TUONG_ID"   INT
                )
                ;

                INSERT INTO TMP_HOP_DONG_DU_AN_DUOC_CHON
                SELECT
                C."id"
                , C."SO_HOP_DONG"
                , c."THUOC_DU_AN_ID"
                , C."NGAY_KY"
                , C."TRICH_YEU"
                , C."KHACH_HANG_ID"
                FROM
                sale_ex_hop_dong_ban C
                WHERE C."id" = any(%(HOP_DONG_BAN_IDS)s) --@ListContractID
                ;

                DROP TABLE IF EXISTS TMP_DS_HOP_DONG
                ;

                CREATE TEMP TABLE TMP_DS_HOP_DONG


                (
                "HOP_DONG_ID"    INT PRIMARY KEY,
                "THUOC_DU_AN_ID" INT
                )
                ;

                INSERT INTO TMP_DS_HOP_DONG
                SELECT DISTINCT
                C."id"
                , C."THUOC_DU_AN_ID"
                FROM TMP_HOP_DONG_DU_AN_DUOC_CHON tSC
                INNER JOIN sale_ex_hop_dong_ban C ON C."id" = tSC."HOP_DONG_ID"
                ;


                DROP TABLE IF EXISTS TMP_DS_VAT_TU_HH
                ;

                CREATE TEMP TABLE TMP_DS_VAT_TU_HH
                -- Bảng chứa danh sách hàng hóa
                (
                "MA_HANG_ID" INT,
                "MA_HANG"    VARCHAR(255),
                "DVT_ID"     INT
                )
                ;

                IF VTHH_IDS IS NULL
                THEN
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM danh_muc_vat_tu_hang_hoa
                ;
                ELSE
                INSERT INTO TMP_DS_VAT_TU_HH
                SELECT
                "id" AS "MA_HANG_ID"
                , "MA"
                , "DVT_CHINH_ID"

                FROM
                danh_muc_vat_tu_hang_hoa II
                WHERE II."id" = any(%(SAN_PHAM_IDS)s)--InventoryItemID
                ;
                END IF
                ;

                -----------------------------------------


                DROP TABLE IF EXISTS TMP_CAN_DOI
                ;

                CREATE TEMP TABLE TMP_CAN_DOI
                AS

                SELECT
                GL."HOP_DONG_BAN_ID"
                , CT2."SO_HOP_DONG"
                , CT2."TRICH_YEU"

                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."CHI_NHANH_ID"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."DIEN_GIAI_CHUNG"
                , GL."MA_HANG_ID"
                , GL."MA_HANG"
                , GL."TEN_HANG"
                , GL."KHO_ID"
                , GL."MA_KHO"
                , GL."TEN_KHO"
                , (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END)                                                            AS "DVT"
                , ----------------------------------------------

                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033', '3040', '3041', '3042', '3043', '2021'))
                THEN 0
                ELSE CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id" -- Nếu ĐVT trên chứng từ = ĐVT chọn trên tham số -> Lấy số lượng trên chứng từ
                THEN GL."SO_LUONG_NHAP"
                ELSE GL."SO_LUONG_NHAP_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1) -- Nếu ĐVT trên chứng từ <> ĐVT trên tham số thì lấy số lượng được tính qua tỷ lệ chuyển đổi trên danh mục
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_NHAP"
                , --Đoạn này xuống dưới tính lại = Thành tiền / Số lượng
                CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_NHAP"
                , ROUND(CAST(SUM(CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024',
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                THEN 0
                ELSE CASE
                -- chứng từ nhập kho thì lấy thành tiền
                WHEN GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012',
                '2013', '2014', '2015',
                '2016', '2017') --nhập kho
                THEN GL."SO_TIEN_NHAP"
                --MUA HÀNG nhập kho thì không lấy VTHH có tính chất diễn giải.
                WHEN GL."LOAI_CHUNG_TU" IN ('302', '307', '308',
                '309', '310', '318',
                '319', '320', '321',
                '322', '352', '357',
                '358', '359', '360',
                '368', '369', '370',
                '371', '372')

                THEN ROUND(CAST((GL."SO_TIEN_NHAP") AS NUMERIC),
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)


                ELSE 0
                END
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_NHAP"
                , -----------------------------------------------------------
                --Xuất: Số lượng, Đơn giá, Thành tiền lấy từ Xuất kho, Trả lại hàng mua, mua hàng không qua kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                ROUND(CAST((CASE WHEN (GL."LOAI_CHUNG_TU" IN ('2020', '2021', '2022', '2023', '2024', '2025',
                '2026', '2027', '3030', '3031', '3032',
                '3033'))
                THEN CASE
                WHEN U."id" IS NOT NULL
                AND GL."DVT_ID" =
                U."id"
                THEN GL."SO_LUONG_XUAT"
                ELSE GL."SO_LUONG_XUAT_THEO_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1)
                END
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)           AS "SO_LUONG_XUAT"
                , CAST(0 AS DECIMAL(18, 4))                                        AS "DON_GIA_XUAT"
                , ROUND(CAST(SUM(CASE
                WHEN (GL."LOAI_CHUNG_TU" IN
                ('2020', '2021', '2022', '2023', '2024', -- đối với chứng từ xuất kho, giảm giá hàng mua, trả lại hàng mua thì lấy thành tiền.
                '2025', '2026', '2027', '3030',
                '3031', '3032', '3033', '3040',
                '3041', '3042', '3043'))
                AND COALESCE(GL."MA_TK_CO", '') NOT LIKE '133%%'
                THEN GL."SO_TIEN_XUAT"
                ELSE 0
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI_XUAT"

                , GL."THU_TU_TRONG_CHUNG_TU"


                FROM so_kho_chi_tiet AS GL
                INNER JOIN TMP_LIST_BRAND AS B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN sale_ex_hop_dong_ban AS CT ON GL."HOP_DONG_BAN_ID" = cT."id"
                INNER JOIN TMP_DS_HOP_DONG C ON (GL."HOP_DONG_BAN_ID" = C."HOP_DONG_ID"
                OR CT."THUOC_DU_AN_ID" = C."HOP_DONG_ID"
                )
                INNER JOIN sale_ex_hop_dong_ban AS CT2 ON C."HOP_DONG_ID" = CT2."id"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON GL."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = GL."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END
                ) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                LEFT JOIN purchase_document_line PUD ON pud."id" = gl."CHI_TIET_ID"
                AND GL."MA_TK_NO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_NO_ID")
                AND GL."MA_TK_CO" = (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = PUD."TK_CO_ID")

                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."order_id"
                WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                AND COALESCE("MA_TK_NO", ''
                ) NOT LIKE '133%%'
                AND (loai_dvt IS NULL
                OR loai_dvt = 0
                OR UC."DVT_ID" IS NOT NULL
                )


                ---------19/07/2016 (PBI 108990)sửa lại cách lấy dữ liệu thành tiền nhập kho/xuất kho
                /*Sửa bug 18921 bổ xung thêm Reftype 2021 để lấy thêm chứng từ xuất hàng cho chi nhánh khác*/
                AND (GL."LOAI_CHUNG_TU" IN ('2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', -- Nhập kho
                '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', -- Xuất kho
                '3030', '3031', '3032', '3033', -- Trả lại hàng mua
                '3040', '3041', '3042', '3043'
                ) -- Giảm giá hàng mua
                -- Hoặc (Mua hàng qua kho Và VTHH khác DV, Diễn giải)
                OR (GL."LOAI_CHUNG_TU" IN ('302', '307', '308', '309', '310', '318', '319',
                '320', '321', '322', '352', '357', '358', '359',
                '360', '368', '369', '370', '371', '372'
                )
                )
                )
                ----------------
                GROUP BY
                GL."HOP_DONG_BAN_ID",
                CT2."SO_HOP_DONG",
                CT2."TRICH_YEU",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."DIEN_GIAI_CHUNG",
                GL."MA_HANG_ID",
                GL."MA_HANG",
                GL."TEN_HANG",
                GL."KHO_ID",
                GL."MA_KHO",
                GL."TEN_KHO",
                (CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END
                ),
                GL."SO_LUONG_XUAT",
                GL."SO_LUONG_XUAT_THEO_DVT_CHINH",
                GL."DON_GIA",
                GL."SO_LUONG_NHAP",
                GL."SO_LUONG_NHAP_THEO_DVT_CHINH",

                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                GL."THU_TU_TRONG_CHUNG_TU",
                GL."DVT_ID",
                GL."LOAI_CHUNG_TU",
                U."id"
                ;


                /*Lấy số liệu trường hợp mua hàng không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT

                PUD."HOP_DONG_BAN_ID"
                , CT2."SO_HOP_DONG"
                , CT2."TRICH_YEU"
                , PUD."order_id"
                , 'purchase.document'                                    AS "MODEL_CHUNG_TU"
                , PU."CHI_NHANH_ID"
                , PU."NGAY_HACH_TOAN"
                , PU."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PU."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PU."SO_PHIEU_NHAP"

                WHEN PU."LOAI_CHUNG_TU" IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PU."SO_CHUNG_TU"

                ELSE '' END
                , CASE WHEN PU."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PU."DIEN_GIAI_CHUNG"
                ELSE PU."LY_DO_CHI" END
                , PUD."MA_HANG_ID"
                , I."MA"
                , PUD."name"                                             AS "TEN_HANG"
                , NULL
                , --PUD."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END                                                    AS "DVT"
                , ROUND(cast((CASE WHEN U."id" IS NOT NULL
                AND PUD."DVT_ID" =
                U."id" -- Nếu ĐVT trên chứng từ = ĐVT chọn trên tham số -> Lấy số lượng trên chứng từ
                THEN PUD."SO_LUONG"
                ELSE PUD."SO_LUONG_THEO_DVT_CHINH" * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1) -- Nếu ĐVT trên chứng từ <> ĐVT trên tham số thì lấy số lượng được tính qua tỷ lệ chuyển đổi trên danh mục
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                              AS "DON_GIA"
                , ROUND(cast(SUM(ROUND(cast((PUD."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)) AS
                NUMERIC),
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                     "GIA_TRI"
                , ROUND(cast((CASE WHEN U."id" IS NOT NULL AND PUD."DVT_ID" =
                U."id" -- Nếu ĐVT trên chứng từ = ĐVT chọn trên tham số -> Lấy số lượng trên chứng từ
                THEN PUD."SO_LUONG"
                ELSE (PUD."SO_LUONG_THEO_DVT_CHINH" * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
                1)) -- Nếu ĐVT trên chứng từ <> ĐVT trên tham số thì lấy số lượng được tính qua tỷ lệ chuyển đổi trên danh mục
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                              AS "DON_GIA"
                , ROUND(cast(SUM(ROUND(cast((PUD."GIA_TRI_NHAP_KHO") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)) AS
                NUMERIC),
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                  AS "GIA_TRI"
                , PUD."THU_TU_SAP_XEP_CHI_TIET"
                /*===================================================*/
                FROM purchase_document_line AS PUD
                INNER JOIN purchase_document AS PU ON PUD."order_id" = PU."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PU."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN sale_ex_hop_dong_ban AS CT ON PUD."HOP_DONG_BAN_ID" = CT."id"
                INNER JOIN TMP_DS_HOP_DONG C ON (PUD."HOP_DONG_BAN_ID" = C."HOP_DONG_ID"
                OR CT."THUOC_DU_AN_ID" = C."HOP_DONG_ID"
                )
                INNER JOIN sale_ex_hop_dong_ban AS CT2 ON C."HOP_DONG_ID" = CT2."id"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON PUD."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = PUD."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = PUD."KHO_ID"

                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                --LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."order_id"
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = PUD."DON_VI_ID"
                WHERE (
                PU."LOAI_CHUNG_TU" IN (312, 313, 314, 315, 316, 324, 325,
                326, 327, 328, 362, 363, 364, 365,
                366, 374, 375, 376, 377, 378)
                AND (I."MA" <> N'CPMH'
                OR (I."MA" = N'CPMH'
                -- AND PUDC."CHUNG_TU_ID" IS NULL
                AND PUD."id" IS NOT NULL
                )
                )
                )
                AND PU."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PU."state" = 'da_ghi_so')
                GROUP BY
                PUD."HOP_DONG_BAN_ID",
                CT2."SO_HOP_DONG",
                CT2."TRICH_YEU",
                PUD."order_id",
                PUD."id",
                PU."CHI_NHANH_ID",
                PU."NGAY_HACH_TOAN",
                PU."NGAY_CHUNG_TU",
                /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                CASE

                WHEN PU."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PU."SO_PHIEU_NHAP"

                WHEN PU."LOAI_CHUNG_TU" IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PU."SO_CHUNG_TU"

                ELSE '' END,
                CASE WHEN PU."LOAI_CHUNG_TU" NOT IN (313, 314, 315, 316,
                325, 326, 327, 328,
                363, 364, 365, 366,
                375, 376, 377, 378)
                THEN PU."DIEN_GIAI_CHUNG"
                ELSE PU."LY_DO_CHI" END,
                --PU."DIEN_GIAI" ,
                PUD."MA_HANG_ID",
                I."MA",
                PUD."name",

                PU."LOAI_CHUNG_TU",

                PUD."THU_TU_SAP_XEP_CHI_TIET",
                U."id",
                PUD."DVT_ID",
                CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END,
                PUD."SO_LUONG",
                PUD."SO_LUONG_THEO_DVT_CHINH",
                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                ;

                /*Giảm giá hàng mua - Không giảm trừ giá trị hàng trong kho*/

                INSERT INTO TMP_CAN_DOI
                SELECT
                /*===================================================*/
                PUD."HOP_DONG_BAN_ID"
                , CT2."SO_HOP_DONG"
                , CT2."TRICH_YEU"
                , PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                , 'purchase.ex.giam.gia.hang.mua'                                      AS "MODEL_CHUNG_TU"
                , PU."CHI_NHANH_ID"
                , PU."NGAY_HACH_TOAN"
                , PU."NGAY_CHUNG_TU"
                , /*Sửa bug 19103 lấy số chứng từ trong trường hợp mua hàng không qua kho công nợ hoặc thanh toán ngay*/
                PU."SO_CHUNG_TU"
                , PU."DIEN_GIAI"
                , --PU."DIEN_GIAI" AS "DIEN_GIAI" ,
                PUD."MA_HANG_ID"
                , I."MA"
                , PUD."TEN_HANG"                                                       AS "TEN_HANG"
                , NULL
                , --PUD."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END                                                                  AS "DVT"
                , CAST(0 AS DECIMAL(18, 4))                                            AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                            AS "DON_GIA"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                            AS "GIA_TRI"
                , CAST(0 AS DECIMAL(18, 4))                                            AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                            AS "DON_GIA"
                , ROUND(SUM(PUD."THANH_TIEN_QUY_DOI"), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI"


                , PUD."THU_TU_SAP_XEP_CHI_TIET"
                /*===================================================*/
                FROM purchase_ex_giam_gia_hang_mua_chi_tiet AS PUD
                INNER JOIN purchase_ex_giam_gia_hang_mua AS PU ON PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PU."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PU."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN sale_ex_hop_dong_ban AS CT ON PUD."HOP_DONG_BAN_ID" = CT."id"
                INNER JOIN TMP_DS_HOP_DONG C ON (PUD."HOP_DONG_BAN_ID" = C."HOP_DONG_ID"
                OR CT."THUOC_DU_AN_ID" = C."HOP_DONG_ID"
                )
                INNER JOIN sale_ex_hop_dong_ban AS CT2 ON C."HOP_DONG_ID" = CT2."id"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON PUD."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = PUD."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = PUD."KHO_ID"

                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                --LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = PUD."DON_VI_ID"
                WHERE PU."LOAI_CHUNG_TU" IN (3042, 3043)
                AND PU."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PU."state" = 'da_ghi_so')
                GROUP BY
                PUD."HOP_DONG_BAN_ID",
                CT2."SO_HOP_DONG",
                CT2."TRICH_YEU",
                PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID",

                PU."CHI_NHANH_ID",
                PU."NGAY_HACH_TOAN",
                PU."NGAY_CHUNG_TU",

                PU."SO_CHUNG_TU",
                PU."DIEN_GIAI",

                PUD."MA_HANG_ID",
                I."MA",
                PUD."TEN_HANG",
                PUD."KHO_ID",
                S."MA_KHO",
                S."TEN_KHO",
                PU."LOAI_CHUNG_TU",

                PUD."TK_NO_ID",
                PUD."TK_CO_ID",
                PUD."KHOAN_MUC_CP_ID",
                OU."MA_DON_VI",
                OU."TEN_DON_VI",
                PUD."THU_TU_SAP_XEP_CHI_TIET",
                U."id",
                PUD."DVT_ID",
                CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END,
                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"

                ;

                /*===========================================================*/
                /*Trả lại hàng mua - Không qua kho*/
                INSERT INTO TMP_CAN_DOI
                SELECT
                /*===================================================*/
                PUD."HOP_DONG_BAN_ID"
                , CT2."SO_HOP_DONG"
                , CT2."TRICH_YEU"
                , PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                , 'purchase.ex.tra.lai.hang.mua'                                                        AS "MODEL_CHUNG_TU"
                , PU."CHI_NHANH_ID"
                , PU."NGAY_HACH_TOAN"
                , PU."NGAY_CHUNG_TU"
                , CASE

                WHEN PU."LOAI_CHUNG_TU" IN (3032)
                THEN PU."SO_CHUNG_TU"

                WHEN PU."LOAI_CHUNG_TU" IN (3033)
                THEN PU."SO_PHIEU_THU"
                ELSE '' END
                , CASE WHEN PU."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PU."DIEN_GIAI"
                ELSE PU."LY_DO_NOP" END
                , PUD."MA_HANG_ID"
                , I."MA"
                , PUD."TEN_HANG"                                                                        AS "TEN_HANG"
                , NULL
                , --PUD."MA_KHO_ID" ,
                NULL
                , --S."MA_KHO" ,
                NULL
                , --S."TEN_KHO" ,
                CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END                                                                                   AS "DVT"
                , CAST(0 AS DECIMAL(18, 4))                                                             AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                             AS "DON_GIA"
                , --- 18/07/2016 PTPhuong2 sửa lại công thức tính THÀNH TIỀN nhập kho (PBI 108990)
                CAST(0 AS DECIMAL(18, 4))                                                             AS "GIA_TRI"
                , ROUND(cast((CASE WHEN U."id" IS NOT NULL
                AND PUD."DVT_ID" = U."id"
                THEN PUD."SO_LUONG"
                ELSE PUD."SO_LUONG_DVT_CHINH"
                * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)                                AS "SO_LUONG"
                , CAST(0 AS DECIMAL(18, 4))                                                             AS "DON_GIA"
                , ROUND(cast(SUM(PUD."THANH_TIEN_QUY_DOI") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "GIA_TRI"

                , PUD."THU_TU_SAP_XEP_CHI_TIET"
                /*===================================================*/
                FROM purchase_ex_tra_lai_hang_mua_chi_tiet AS PUD
                INNER JOIN purchase_ex_tra_lai_hang_mua AS PU ON PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PU."id"
                INNER JOIN TMP_LIST_BRAND AS B ON PU."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                INNER JOIN sale_ex_hop_dong_ban AS CT ON PUD."HOP_DONG_BAN_ID" = CT."id"
                INNER JOIN TMP_DS_HOP_DONG C ON (PUD."HOP_DONG_BAN_ID" = C."HOP_DONG_ID"
                OR CT."THUOC_DU_AN_ID" = C."HOP_DONG_ID"
                )
                INNER JOIN sale_ex_hop_dong_ban AS CT2 ON C."HOP_DONG_ID" = CT2."id"
                INNER JOIN TMP_DS_VAT_TU_HH AS II ON PUD."MA_HANG_ID" = II."MA_HANG_ID"
                INNER JOIN danh_muc_vat_tu_hang_hoa AS I ON I."id" = PUD."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh UI ON II."DVT_ID" = UI."id"
                LEFT JOIN danh_muc_kho AS S ON S."id" = PUD."KHO_ID"

                LEFT JOIN (SELECT
                IIUC."VAT_TU_HANG_HOA_ID"
                , "DVT_ID"
                , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                THEN 1
                ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                WHERE IIUC."STT" = loai_dvt
                ) UC ON II."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
                AND U."id" = II."DVT_ID"
                )
                OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
                AND UC."DVT_ID" = U."id"
                )
                -- LEFT JOIN purchase_chi_phi PUDC ON PUDC."CHUNG_TU_ID" = PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = PUD."DON_VI_ID"
                WHERE PU."LOAI_CHUNG_TU" IN (3032, 3033)
                AND PU."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (PU."state" = 'da_ghi_so')

                GROUP BY
                PUD."HOP_DONG_BAN_ID",
                CT2."SO_HOP_DONG",
                CT2."TRICH_YEU",
                PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID",

                PU."CHI_NHANH_ID",
                PU."NGAY_HACH_TOAN",
                PU."NGAY_CHUNG_TU",
                CASE

                WHEN PU."LOAI_CHUNG_TU" IN (3032)
                THEN PU."SO_CHUNG_TU"

                WHEN PU."LOAI_CHUNG_TU" IN (3033)
                THEN PU."SO_PHIEU_THU"
                ELSE '' END,
                CASE WHEN PU."LOAI_CHUNG_TU" NOT IN (3033)
                THEN PU."DIEN_GIAI"
                ELSE PU."LY_DO_NOP" END,
                --PU."DIEN_GIAI" ,
                PUD."MA_HANG_ID",
                I."MA",
                PUD."TEN_HANG",

                PUD."THU_TU_SAP_XEP_CHI_TIET",
                U."id",
                PUD."DVT_ID",
                CASE WHEN loai_dvt = 0
                THEN UI."DON_VI_TINH"
                ELSE U."DON_VI_TINH"
                END,
                PUD."SO_LUONG",
                PUD."SO_LUONG_DVT_CHINH",
                UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"

                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                AS


                SELECT
                "HOP_DONG_BAN_ID"
                , "SO_HOP_DONG"
                , "TRICH_YEU"
                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "CHI_NHANH_ID"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , "MA_HANG_ID"
                , "MA_HANG"
                , "TEN_HANG"
                , "KHO_ID"
                , "MA_KHO"
                , "TEN_KHO"
                , "DVT"
                , "SO_LUONG_NHAP"
                , "DON_GIA_NHAP"
                , SUM("GIA_TRI_NHAP") AS "THANH_TIEN_NHAP"
                , "SO_LUONG_XUAT"
                , "DON_GIA_XUAT"
                , SUM("GIA_TRI_XUAT") AS "THANH_TIEN_XUAT"

                , "THU_TU_TRONG_CHUNG_TU"

                FROM TMP_CAN_DOI
                GROUP BY
                "HOP_DONG_BAN_ID",
                "SO_HOP_DONG",
                "TRICH_YEU",
                "ID_CHUNG_TU",
                "MODEL_CHUNG_TU",
                "CHI_NHANH_ID",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG",
                "MA_HANG_ID",
                "MA_HANG",
                "TEN_HANG",
                "KHO_ID",
                "MA_KHO",
                "TEN_KHO",
                "DVT",
                "SO_LUONG_NHAP",
                "DON_GIA_NHAP",
                "SO_LUONG_XUAT",
                "DON_GIA_XUAT",

                "THU_TU_TRONG_CHUNG_TU"
                ;

                UPDATE TMP_KET_QUA
                SET "DON_GIA_NHAP" = ROUND(CAST((CASE WHEN "SO_LUONG_NHAP" = 0
                THEN 0
                ELSE "THANH_TIEN_NHAP"
                / "SO_LUONG_NHAP"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
                "DON_GIA_XUAT" = ROUND(CAST((CASE WHEN "SO_LUONG_XUAT" = 0
                THEN 0
                ELSE "THANH_TIEN_XUAT"
                / "SO_LUONG_XUAT"
                END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;

                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS

                SELECT
                ROW_NUMBER()
                OVER (
                ORDER BY CT."SO_HOP_DONG", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_HANG", "THU_TU_TRONG_CHUNG_TU" ) AS "RowNum"
                , tbl.*

                FROM TMP_KET_QUA tbl
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = tbl."CHI_NHANH_ID"

                LEFT JOIN sale_ex_hop_dong_ban CT ON tbl."HOP_DONG_BAN_ID" = CT."id"
                LEFT JOIN sale_ex_hop_dong_ban CT2 ON CT."THUOC_DU_AN_ID" = CT2."id"
                ORDER BY

                ( CASE WHEN CT."THUOC_DU_AN_ID" IS NOT NULL THEN CT2."SO_HOP_DONG"
                ELSE CT."SO_HOP_DONG"
                END ),
                ( CASE WHEN CT."THUOC_DU_AN_ID" IS NOT NULL THEN CT2."id"
                ELSE CT."id"
                END ),
                CT."LA_DU_AN" DESC,
                CT."NGAY_GHI_DOANH_SO" DESC,
                CT."SO_HOP_DONG",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "MA_HANG",
                "THU_TU_TRONG_CHUNG_TU"

                ;

                END $$
                ;

                SELECT 
                "SO_HOP_DONG" AS "HOP_DONG_DU_AN",
                "TRICH_YEU" AS "TRICH_YEU",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI_CHUNG" AS "DIEN_GIAI_CHUNG",
                "MA_HANG" AS "MA_HANG",
                "TEN_HANG" AS "TEN_HANG",
                "TEN_KHO" AS "TEN_KHO",
                "DVT" AS "DVT",
                "SO_LUONG_NHAP" AS "SO_LUONG_NHAP",
                "DON_GIA_NHAP" AS "DON_GIA_NHAP",
                "THANH_TIEN_NHAP" AS "THANH_TIEN_NHAP",
                "SO_LUONG_XUAT" AS "SO_LUONG_XUAT",
                "DON_GIA_XUAT" AS "DON_GIA_XUAT",
                "THANH_TIEN_XUAT" AS "THANH_TIEN_XUAT",
                "ID_CHUNG_TU" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC"

                FROM TMP_KET_QUA_CUOI_CUNG
                ORDER BY "RowNum"
                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)
    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        if THONG_KE_THEO=='DOI_TUONG_THCP':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_ke_pnx_theo_doi_tuong_dtthcp').read()[0]
        elif THONG_KE_THEO=='CONG_TRINH':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_ke_pnx_theo_doi_tuong_cong_trinh').read()[0]
        elif THONG_KE_THEO=='DON_HANG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_ke_pnx_theo_doi_tuong_don_hang').read()[0]
        elif THONG_KE_THEO=='HOP_DONG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_ke_pnx_theo_doi_tuong_hop_dong').read()[0]
        
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action