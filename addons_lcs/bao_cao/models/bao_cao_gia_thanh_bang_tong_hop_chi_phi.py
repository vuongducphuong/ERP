# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_gia_thanh_bang_tong_hop_chi_phi(models.Model):
    _name = 'bao.cao.gia.thanh.bang.tong.hop.chi.phi'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    THONG_KE_THEO = fields.Selection([('DOI_TUONG_THCP', 'Đối tượng Tập hợp chi phí'),('CONG_TRINH', 'Công trình'),('DON_HANG', 'Đơn hàng'),('HOP_DONG', 'Hợp đồng')], string='Thống kê theo', help='Thống kê theo',default='DOI_TUONG_THCP',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)

    KY_TINH_GIA_THANH = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    
    MA_DOI_TUONG_THCP = fields.Char(string='MA_DOI_TUONG_THCP', help='JobCode')
    TEN_DOI_TUONG_THCP = fields.Char(string='TEN_DOI_TUONG_THCP', help='JobName')

    LOAI_DOI_TUONG_THCP = fields.Char(string='LOAI_DOI_TUONG_THCP', help='JobCode')
    TONG_GIA_THANH = fields.Float(string='TONG_GIA_THANH', help='JobCode')

    DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP = fields.Float(string='DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP', help='JobCode')
    DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP = fields.Float(string='DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP', help='JobCode')
    DO_DANG_DAU_KY_CHI_PHI_CHUNG = fields.Float(string='DO_DANG_DAU_KY_CHI_PHI_CHUNG', help='JobCode')
    DO_DANG_DAU_KY_TONG = fields.Float(string='DO_DANG_DAU_KY_TONG', help='JobCode')

    KHOAN_GIAM_GIA_THANH = fields.Float(string='KHOAN_GIAM_GIA_THANH', help='JobCode')

    NGUYEN_VAT_LIEU_TRUC_TIEP = fields.Float(string='NGUYEN_VAT_LIEU_TRUC_TIEP', help='JobCode')
    NHAN_CONG_TRUC_TIEP = fields.Float(string='NHAN_CONG_TRUC_TIEP', help='JobCode')
    CHI_PHI_CHUNG = fields.Float(string='CHI_PHI_CHUNG', help='JobCode')
    PHAT_SINH_TRONG_KY_TONG = fields.Float(string='PHAT_SINH_TRONG_KY_TONG', help='JobCode')

    DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP = fields.Float(string='DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP', help='JobCode')
    DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP = fields.Float(string='DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP', help='JobCode')
    DO_DANG_CUOI_KY_CHI_PHI_CHUNG = fields.Float(string='DO_DANG_CUOI_KY_CHI_PHI_CHUNG', help='JobCode')
    DO_DANG_CUOI_KY_TONG = fields.Float(string='DO_DANG_CUOI_KY_TONG', help='JobCode')

    
    LOAI_CONG_TRINH = fields.Char(string='LOAI_CONG_TRINH', help='JobCode')
    MA_CONG_TRINH = fields.Char(string='MA_CONG_TRINH', help='JobCode')
    TEN_CONG_TRINH = fields.Char(string='TEN_CONG_TRINH', help='JobName')

    SO_HOP_DONG = fields.Char(string='SO_HOP_DONG', help='JobCode')
    TRICH_YEU = fields.Char(string='TRICH_YEU', help='JobCode')

    LUY_KE_CHI_PHI = fields.Float(string='LUY_KE_CHI_PHI', help='JobCode')
    LUY_KE_DA_NGHIEM_THU = fields.Float(string='LUY_KE_DA_NGHIEM_THU', help='JobCode')
    SO_CHUA_NGHIEM_THU_DAU_KY = fields.Float(string='SO_CHUA_NGHIEM_THU_DAU_KY', help='JobCode')
    SO_CHUA_NGHIEM_THU_CUOI_KY = fields.Float(string='SO_CHUA_NGHIEM_THU_CUOI_KY', help='JobCode')

    # Lũy kế phát sinh kỳ trước
    LK_KY_TRUOC_NVL_TRUC_TIEP = fields.Float(string='LK_KY_TRUOC_NVL_TRUC_TIEP', help='JobCode')
    LK_TRUOC_NC_TRUC_TIEP = fields.Float(string='LK_TRUOC_NC_TRUC_TIEP', help='JobCode')
    LK_TRUOC_MAY_THI_CONG = fields.Float(string='LK_TRUOC_MAY_THI_CONG', help='JobCode')
    LK_TRUOC_CHI_PHI_CHUNG = fields.Float(string='LK_TRUOC_CHI_PHI_CHUNG', help='JobCode')
    LUY_KE_TRUOC_TONG = fields.Float(string='LUY_KE_TRUOC_TONG', help='JobCode')

    # Phát sinh trong kỳ
    LK_TRONG_NVL_TRUC_TIEP = fields.Float(string='LK_TRONG_NVL_TRUC_TIEP', help='JobCode')
    LK_TRONG_NC_TRUC_TIEP = fields.Float(string='LK_TRONG_NC_TRUC_TIEP', help='JobCode')
    LK_TRONG_MAY_THI_CONG = fields.Float(string='LK_TRONG_MAY_THI_CONG', help='JobCode')
    LK_TRONG_CHI_PHI_CHUNG = fields.Float(string='LK_TRONG_CHI_PHI_CHUNG', help='JobCode')
    LK_TRONG_TONG = fields.Float(string='LK_TRONG_TONG', help='JobCode')
    
    # Lũy kế chi phí
    CP_NVL_TRUC_TIEP = fields.Float(string='CP_NVL_TRUC_TIEP', help='JobCode')
    CP_NC_TRUC_TIEP = fields.Float(string='CP_NC_TRUC_TIEP', help='JobCode')
    CP_MAY_THI_CONG = fields.Float(string='CP_MAY_THI_CONG', help='JobCode')
    CP_CHI_PHI_CHUNG = fields.Float(string='CP_CHI_PHI_CHUNG', help='JobCode')
    CP_TONG = fields.Float(string='CP_TONG', help='JobCode')

    SO_DON_HANG = fields.Char(string='SO_DON_HANG', help='JobCode')
    NGAY_DON_HANG = fields.Date(string='NGAY_DON_HANG', help='JobCode')
    DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='JobCode')
    TEN_KHACH_HANG = fields.Char(string='TEN_KHACH_HANG', help='JobCode')

    DOI_TUONG_THCP_IDS = fields.One2many('gia.thanh.ky.tinh.gia.thanh.chi.tiet')
    CHON_TAT_CA_DOI_TUONG_THCP = fields.Boolean('Tất cả đối tượng THCP', default=True)
    DOI_TUONG_THCP_MANY_IDS = fields.Many2many('gia.thanh.ky.tinh.gia.thanh.chi.tiet','tong_hop_nxk_dtthcp', string='Chọn đối tượng THCP') 

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
        self.KY_TINH_GIA_THANH = False
        self.CHON_TAT_CA_DOI_TUONG_THCP = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.CHON_TAT_CA_DON_HANG = True
        self.CHON_TAT_CA_HOP_DONG_BAN = True
       
        self.DOI_TUONG_THCP_MANY_IDS = []
        self.CONG_TRINH_MANY_IDS = []
        self.DON_HANG_MANY_IDS = []
        self.HOP_DONG_BAN_MANY_IDS = []

    
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
        result = super(bao_cao_gia_thanh_bang_tong_hop_chi_phi, self).default_get(fields_list)
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

        CHON_TAT_CA_DOI_TUONG_THCP = params['CHON_TAT_CA_DOI_TUONG_THCP'] if 'CHON_TAT_CA_DOI_TUONG_THCP' in params.keys() else 'False'
        DOI_TUONG_THCP_MANY_IDS = params['DOI_TUONG_THCP_MANY_IDS'] if 'DOI_TUONG_THCP_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_DON_HANG = params['CHON_TAT_CA_DON_HANG'] if 'CHON_TAT_CA_DON_HANG' in params.keys() else 'False'
        DON_HANG_MANY_IDS = params['DON_HANG_MANY_IDS'] if 'DON_HANG_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_HOP_DONG_BAN = params['CHON_TAT_CA_HOP_DONG_BAN'] if 'CHON_TAT_CA_HOP_DONG_BAN' in params.keys() else 'False'
        HOP_DONG_BAN_MANY_IDS = params['HOP_DONG_BAN_MANY_IDS'] if 'HOP_DONG_BAN_MANY_IDS' in params.keys() else 'False'
        KY_TINH_GIA_THANH = params['KY_TINH_GIA_THANH'] if 'KY_TINH_GIA_THANH' in params.keys() else 'False'
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO == 'DOI_TUONG_THCP':
            if KY_TINH_GIA_THANH == 'False':
                raise ValidationError('<Kỳ tính giá thành> không được bỏ trống.')
            else:
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
        KY_TINH_GIA_THANH = params['KY_TINH_GIA_THANH'] if 'KY_TINH_GIA_THANH' in params.keys() and params['KY_TINH_GIA_THANH'] != 'False' else None
       
        if params.get('CHON_TAT_CA_DOI_TUONG_THCP'):
            domain = []
            if KY_TINH_GIA_THANH:
                domain += [('KY_TINH_GIA_THANH_ID','=', KY_TINH_GIA_THANH)]
            arr_ky_tinh_gia_thanh_ct = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].search(domain).ids
        else:
            arr_ky_tinh_gia_thanh_ct = params.get('DOI_TUONG_THCP_MANY_IDS')

        arr_dtthcp = []
        if arr_ky_tinh_gia_thanh_ct:
            for line in arr_ky_tinh_gia_thanh_ct:
                dtthcp_id = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].browse(line)
                arr_dtthcp.append(dtthcp_id.MA_DOI_TUONG_THCP_ID.id)
        DOI_TUONG_THCP_IDS = arr_dtthcp

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
            'DOI_TUONG_THCP_IDS':DOI_TUONG_THCP_IDS, 
            'CONG_TRINH_IDS':CONG_TRINH_IDS, 
            'DON_HANG_IDS':DON_HANG_IDS, 
            'HOP_DONG_BAN_IDS':HOP_DONG_BAN_IDS, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'KY_TINH_GIA_THANH':KY_TINH_GIA_THANH,
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

                ky_tinh_gia_thanh_id         INTEGER := %(KY_TINH_GIA_THANH)s;


                chi_nhanh_id                 INTEGER := %(CHI_NHANH_ID)s;

                CHE_DO_KE_TOAN               VARCHAR;

                tu_ngay                      TIMESTAMP;

                den_ngay                     TIMESTAMP;

                LOAI_GIA_THANH               VARCHAR;

                ListJob                      VARCHAR; --@ListJobID

                --Tham số bên misa

                MA_PHAN_CAP_NVLTT            VARCHAR(100);

                MA_PHAN_CAP_NCTT             VARCHAR(100);

                MA_PHAN_CAP_SXC              VARCHAR(100);


                MA_PHAN_CAP_CPSX             VARCHAR(100);

                CHI_TIET_THEO_DOI_TUONG_THCP BOOLEAN;

                BEGIN

                DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP_TS
                ;

                CREATE TEMP TABLE TMP_DOI_TUONG_THCP_TS
                AS
                SELECT id AS "DOI_TUONG_THCP_ID"

                FROM danh_muc_doi_tuong_tap_hop_chi_phi
                WHERE id = any (%(DOI_TUONG_THCP_IDS)s)--@ListJobID
                ;

                SELECT value
                INTO CHE_DO_KE_TOAN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT "TU_NGAY"
                INTO tu_ngay
                FROM gia_thanh_ky_tinh_gia_thanh AS JP
                WHERE "id" = ky_tinh_gia_thanh_id
                ;

                SELECT "DEN_NGAY"
                INTO den_ngay
                FROM gia_thanh_ky_tinh_gia_thanh AS JP
                WHERE "id" = ky_tinh_gia_thanh_id
                ;

                SELECT "LOAI_GIA_THANH"
                INTO LOAI_GIA_THANH
                FROM gia_thanh_ky_tinh_gia_thanh AS JP
                WHERE "id" = ky_tinh_gia_thanh_id
                ;


                DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP_CON
                ;

                CREATE TEMP TABLE TMP_DOI_TUONG_THCP_CON

                (
                "DOI_TUONG_THCP_ID"   INT,
                "MA_DOI_TUONG_THCP"   VARCHAR(25),
                "TEN_DOI_TUONG_THCP"  VARCHAR(128),
                "LOAI_DOI_TUONG_THCP" VARCHAR(128),
                "isparent"            BOOLEAN,
                "parent_id"           INT,
                "BAC"                 INT,
                "MA_PHAN_CAP"         VARCHAR(100)
                )
                ;

                --Bảng Job để lưu Các Job chi tiết nhất: Dùng để lấy dữ liệu
                INSERT INTO TMP_DOI_TUONG_THCP_CON
                ("DOI_TUONG_THCP_ID",
                "MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP",
                "LOAI_DOI_TUONG_THCP",
                "isparent",
                "parent_id",
                "BAC",
                "MA_PHAN_CAP"
                )
                SELECT
                J2."id"
                , J2."MA_DOI_TUONG_THCP"
                , J2."TEN_DOI_TUONG_THCP"
                , J2."LOAI"
                , J2."isparent"
                , J2."parent_id"
                , J2."BAC"
                , J2."MA_PHAN_CAP"
                FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON JPD."MA_DOI_TUONG_THCP_ID" = J."id"
                INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J2 ON J2."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                || '%%'
                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                ;

                --
                --     SELECT ListJob || CAST("DOI_TUONG_THCP_ID" AS VARCHAR(50)) || ','
                --     INTO ListJob
                --     FROM TMP_DOI_TUONG_THCP_CON AS J
                --     ;

                DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
                ;

                CREATE TEMP TABLE TMP_DOI_TUONG_THCP


                (
                "DOI_TUONG_THCP_ID"   INT,
                "MA_DOI_TUONG_THCP"   VARCHAR(25),
                "TEN_DOI_TUONG_THCP"  VARCHAR(128),
                "LOAI_DOI_TUONG_THCP" VARCHAR(100),
                "isparent"            BOOLEAN,
                "parent_id"           INT,
                "BAC"                 INT,
                "MA_PHAN_CAP"         VARCHAR(100)
                )
                ;

                INSERT INTO TMP_DOI_TUONG_THCP
                (
                "DOI_TUONG_THCP_ID",
                "MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP",
                "LOAI_DOI_TUONG_THCP",
                "isparent",
                "parent_id",
                "BAC",
                "MA_PHAN_CAP"
                )
                SELECT
                J."id"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , CASE WHEN j."LOAI" = '0'
                THEN N'Phân xưởng'
                WHEN j."LOAI" = '1'
                THEN N'Sản phẩm'
                WHEN j."LOAI" = '2'
                THEN N'Quy trình sản xuất'
                WHEN j."LOAI" = '3'
                THEN N'Công đoạn'
                END AS "LOAI_DOI_TUONG_THCP"
                , J."isparent"
                , J."parent_id"
                , J."BAC"
                , J."MA_PHAN_CAP"
                FROM danh_muc_doi_tuong_tap_hop_chi_phi AS J
                LEFT JOIN TMP_DOI_TUONG_THCP_CON AS J2 ON J."id" = J2."DOI_TUONG_THCP_ID"
                LEFT JOIN gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD ON J."id" = JPD."MA_DOI_TUONG_THCP_ID"
                AND "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                WHERE (J2."DOI_TUONG_THCP_ID" IS NOT NULL
                OR JPD."MA_DOI_TUONG_THCP_ID" IS NOT NULL
                )
                ORDER BY "MA_PHAN_CAP"
                ;


                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_CPSX
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NVLTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NCTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_SXC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                (
                "DOI_TUONG_THCP_ID"                         INT            NULL,
                "CONG_TRINH_ID"                             INT            NULL,
                "DON_DAT_HANG_ID"                           INT            NULL,
                "HOP_DONG_ID"                               INT            NULL,
                "TONG_GIA_THANH"                            DECIMAL(22, 4) NULL,
                "LUY_KE_DA_NGHIEM_THU"                      DECIMAL(22, 4) NULL,
                "SO_CHUA_NGHIEM_THU"                        DECIMAL(22, 4) NULL,

                "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"  DECIMAL(22, 4) NULL,
                "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP"        DECIMAL(22, 4) NULL,

                "DO_DANG_DAU_KY_CHI_PHI_CHUNG"              DECIMAL(22, 4) NULL,
                "DO_DANG_DAU_KY_TONG"                       DECIMAL(22, 4) NULL,


                "NGUYEN_VAT_LIEU_TRUC_TIEP"                 DECIMAL(22, 4) NULL,
                "NHAN_CONG_TRUC_TIEP"                       DECIMAL(22, 4) NULL,


                "CHI_PHI_CHUNG"                             DECIMAL(22, 4) NULL,
                "PHAT_SINH_TRONG_KY_TONG"                   DECIMAL(22, 4) NULL,
                "KHOAN_GIAM_GIA_THANH"                      DECIMAL(22, 4) NULL,

                "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP" DECIMAL(22, 4) NULL,
                "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP"        DECIMAL(22, 4) NULL,

                "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"             DECIMAL(22, 4) NULL,
                "DO_DANG_CUOI_KY_TONG"                      DECIMAL(22, 4) NULL,


                "MA_DOI_TUONG_THCP"                         VARCHAR(25)    NULL,
                "TEN_DOI_TUONG_THCP"                        VARCHAR(128)   NULL,
                "LOAI_DOI_TUONG_THCP"                       VARCHAR(128)   NULL,


                "BAC"                                       INT,
                "MA_PHAN_CAP"                               VARCHAR(100)

                )
                ;


                SELECT "CHI_TIET_THEO_DTTHCP"
                INTO CHI_TIET_THEO_DOI_TUONG_THCP
                FROM gia_thanh_cau_hinh_so_du_dau_ky AS JC
                ;

                IF LOAI_GIA_THANH IN ('DON_GIAN', 'HE_SO_TY_LE', 'PHAN_BUOC') --Giản đơn/ hệ số tỷ lệ/ phân bước
                THEN

                --Dở dang đầu kỳ
                DROP TABLE IF EXISTS TMP_DO_DANG_DAU_KY
                ;

                CREATE TEMP TABLE TMP_DO_DANG_DAU_KY

                (
                "DOI_TUONG_THCP_ID"       INT,
                "KY_TINH_GIA_THANH_ID"    INT,
                "OPN_NVL_TRUC_TIEP"       DECIMAL(18, 4),
                "OPN_NHAN_CONG_TRUC_TIEP" DECIMAL(18, 4),
                "OPN_CHI_PHI_CHUNG"       DECIMAL(18, 4)
                )
                ;

                INSERT INTO TMP_DO_DANG_DAU_KY
                ("DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",
                "OPN_NVL_TRUC_TIEP",
                "OPN_NHAN_CONG_TRUC_TIEP",
                "OPN_CHI_PHI_CHUNG"
                )
                SELECT
                J."DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(CASE WHEN F."DOI_TUONG_THCP_ID" IS NULL
                THEN COALESCE(J2."CHI_PHI_NVL_TRUC_TIEP", 0)
                ELSE COALESCE(F."NVL_TRUC_TIEP", 0)
                END) AS "OPN_NVL_TRUC_TIEP"
                , SUM(CASE WHEN F."DOI_TUONG_THCP_ID" IS NULL
                THEN COALESCE(J2."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0)
                ELSE COALESCE(F."NHAN_CONG_TRUC_TIEP", 0)
                END) AS "OPN_NHAN_CONG_TRUC_TIEP"
                , SUM(CASE WHEN F."DOI_TUONG_THCP_ID" IS NULL
                THEN (CASE WHEN CHI_TIET_THEO_DOI_TUONG_THCP = TRUE
                THEN COALESCE(J2."NVL_GIAN_TIEP",
                0)
                + COALESCE(J2."CHI_PHI_NHAN_CONG_GIAN_TIEP",
                0)
                + COALESCE(J2."KHAU_HAO",
                0)
                + COALESCE(J2."CHI_PHI_MUA_NGOAI",
                0)
                + COALESCE(J2."CHI_PHI_KHAC",
                0)
                ELSE COALESCE(J2."CHI_PHI_KHAC",
                0)
                END)
                ELSE COALESCE(F."NVL_GIAN_TIEP",
                0)
                + COALESCE(F."NHAN_CONG_GIAN_TIEP",
                0)
                + COALESCE(F."KHAU_HAO",
                0)
                + COALESCE(F."GIA_TRI_MUA",
                0)
                + COALESCE(F."CHI_PHI_KHAC",
                0)

                END)    "OPN_CHI_PHI_CHUNG"
                FROM TMP_DOI_TUONG_THCP_CON AS J
                LEFT JOIN account_ex_chi_phi_do_dang AS J2 ON J."DOI_TUONG_THCP_ID" = J2."MA_DOI_TUONG_THCP_ID"

                AND "CHI_NHANH_ID" = chi_nhanh_id
                LEFT JOIN LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP('{35}', --@ListJob
                tu_ngay,
                chi_nhanh_id
                )
                AS F ON F."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                GROUP BY J."DOI_TUONG_THCP_ID"
                ;


                --Phát sinh trong kỳ

                DROP TABLE IF EXISTS TMP_PHAT_SINH_TRONG_KY
                ;

                CREATE TEMP TABLE TMP_PHAT_SINH_TRONG_KY


                (
                "DOI_TUONG_THCP_ID"    INT,
                "KY_TINH_GIA_THANH_ID" INT,

                "NVL_TRUC_TIEP"        DECIMAL(22, 4),

                "NHAN_CONG_TRUC_TIEP"  DECIMAL(22, 4),

                "CHI_PHI_CHUNG"        DECIMAL(22, 4)
                )
                ;

                -- --Phân bổ chi phí chung trong kỳ


                DROP TABLE IF EXISTS TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                ;

                CREATE TEMP TABLE TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                (
                "DOI_TUONG_THCP_ID"           INT,
                "KY_TINH_GIA_THANH_ID"        INT,

                "PHAN_BO_NVL_TRUC_TIEP"       DECIMAL(22, 4),

                "PHAN_BO_NHAN_CONG_TRUC_TIEP" DECIMAL(22, 4),

                "PHAN_BO_CHI_PHI_CHUNG"       DECIMAL(22, 4)
                )
                ;

                IF CHE_DO_KE_TOAN = '15'
                THEN

                --Chi phí phát sinh
                INSERT INTO TMP_PHAT_SINH_TRONG_KY
                ("DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",
                "NVL_TRUC_TIEP",
                "NHAN_CONG_TRUC_TIEP",
                "CHI_PHI_CHUNG"

                )
                SELECT
                J."DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '621%%'
                OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%')
                THEN COALESCE("GHI_NO", 0)
                - COALESCE("GHI_CO", 0)
                ELSE 0
                END) AS "NVL_TRUC_TIEP"
                , --621
                SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '622%%'
                THEN COALESCE("GHI_NO", 0)
                - COALESCE("GHI_CO", 0)
                ELSE 0
                END) AS "NHAN_CONG_TRUC_TIEP"
                , --622
                SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '627%%'
                THEN COALESCE("GHI_NO", 0)
                - COALESCE("GHI_CO", 0)
                ELSE 0
                END) AS "CHI_PHI_CHUNG" --627
                FROM so_cai_chi_tiet AS GL
                INNER JOIN TMP_DOI_TUONG_THCP_CON AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                AND "CHI_NHANH_ID" = chi_nhanh_id
                AND
                (((("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
                "LOAI_HACH_TOAN" = '1'))

                OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'))

                GROUP BY J."DOI_TUONG_THCP_ID"

                ;


                INSERT INTO TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                ("DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",

                "PHAN_BO_NVL_TRUC_TIEP",

                "PHAN_BO_NHAN_CONG_TRUC_TIEP",

                "PHAN_BO_CHI_PHI_CHUNG"
                )
                SELECT
                "MA_DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = "TAI_KHOAN_ID") LIKE '621%%'
                THEN COALESCE("SO_TIEN",
                0)
                ELSE 0
                END)
                , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = "TAI_KHOAN_ID") LIKE '622%%'
                THEN COALESCE("SO_TIEN",
                0)
                ELSE 0
                END)
                , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = "TAI_KHOAN_ID") LIKE '627%%'
                THEN COALESCE("SO_TIEN",
                0)
                ELSE 0
                END)
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung AS JCAD
                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                GROUP BY "MA_DOI_TUONG_THCP_ID"

                ;


                ELSE


                --Chi phí phát sinh
                INSERT INTO TMP_PHAT_SINH_TRONG_KY
                (
                "DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",
                "NVL_TRUC_TIEP",
                "NHAN_CONG_TRUC_TIEP",
                "CHI_PHI_CHUNG"

                )
                SELECT
                J."DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%'
                THEN COALESCE("GHI_NO", 0)
                - COALESCE("GHI_CO", 0)
                ELSE 0
                END)
                , --621
                SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%'
                THEN COALESCE("GHI_NO", 0)
                - COALESCE("GHI_CO", 0)
                ELSE 0
                END)
                , --622
                SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%'
                THEN COALESCE("GHI_NO", 0)
                - COALESCE("GHI_CO", 0)
                ELSE 0
                END) --6274
                FROM so_cai_chi_tiet AS GL
                INNER JOIN TMP_DOI_TUONG_THCP_CON AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
                WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = "TAI_KHOAN_ID") LIKE '154%%'
                AND GL."KHOAN_MUC_CP_ID" IS NOT NULL

                AND "CHI_NHANH_ID" = chi_nhanh_id
                GROUP BY J."DOI_TUONG_THCP_ID"

                ;


                INSERT INTO TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                ("DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",

                "PHAN_BO_NVL_TRUC_TIEP",

                "PHAN_BO_NHAN_CONG_TRUC_TIEP",

                "PHAN_BO_CHI_PHI_CHUNG"
                )
                SELECT
                "MA_DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%'
                THEN COALESCE("SO_TIEN",
                0)
                ELSE 0
                END)
                , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%'
                THEN COALESCE("SO_TIEN",
                0)
                ELSE 0
                END)
                , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%'
                THEN COALESCE("SO_TIEN",
                0)
                ELSE 0
                END)
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung AS JCAD
                LEFT JOIN danh_muc_khoan_muc_cp AS EI ON JCAD."KHOAN_MUC_CP_ID" = EI."id"
                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                GROUP BY "MA_DOI_TUONG_THCP_ID"
                ;

                END IF
                ;


                --Khoản giảm giá thành
                DROP TABLE IF EXISTS TMP_KHOAN_GIAM_GIA_THANH
                ;

                CREATE TEMP TABLE TMP_KHOAN_GIAM_GIA_THANH

                (
                "DOI_TUONG_THCP_ID"    INT,
                "KY_TINH_GIA_THANH_ID" INT,
                "KHOAN_GIAM_GIA_THANH" DECIMAL(22, 4)
                )
                ;

                INSERT INTO TMP_KHOAN_GIAM_GIA_THANH
                ("DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",
                "KHOAN_GIAM_GIA_THANH"

                )
                SELECT
                J."DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(COALESCE("GHI_CO", 0)) AS "NVL_TRUC_TIEP"
                FROM so_cai_chi_tiet AS GL
                INNER JOIN TMP_DOI_TUONG_THCP_CON AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
                WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND "MA_TAI_KHOAN" LIKE '154%%' AND "LOAI_HACH_TOAN" = '2'

                AND (CHE_DO_KE_TOAN = '15'
                OR (CHE_DO_KE_TOAN = '48'
                AND (EI."id" IS NULL
                OR EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%'
                )
                )
                )

                AND "CHI_NHANH_ID" = chi_nhanh_id
                AND "LOAI_CHUNG_TU" <> '2010'

                GROUP BY J."DOI_TUONG_THCP_ID"

                ;


                --QĐ15 = Phát sinh Có TK 154 chi tiết theo đối tượng THCP trên chứng từ có ngày hạch toán thuộc kỳ tính giá thành (Không kể PSĐƯ Nợ 155,157/Có 154 chi tiết theo đối tượng tập hợp CP)
                --QĐ48 = Phát sinh Có TK 154 chi tiết theo đối tượng THCP không chi tiết theo các KMCP sản xuất trên chứng từ có ngày hạch toán thuộc kỳ tính giá thành  (Không kể PSĐƯ Nợ 155,157/Có 154 không chi tiết theo KMCP CPSX chi tiết theo đối tượng tập hợp CP)


                --     	Dở dang cuối kỳ :lấy trên form đánh giá dở dang của kỳ tính giá thành này
                --
                DROP TABLE IF EXISTS TMP_DO_DANG_CUOI_KY
                ;

                CREATE TEMP TABLE TMP_DO_DANG_CUOI_KY

                (
                "DOI_TUONG_THCP_ID"                         INT,
                "KY_TINH_GIA_THANH_ID"                      INT,
                "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP" DECIMAL(22, 4),
                "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP"       DECIMAL(22, 4),

                "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"             DECIMAL(22, 4)
                )
                ;


                INSERT INTO TMP_DO_DANG_CUOI_KY
                ("DOI_TUONG_THCP_ID",
                "KY_TINH_GIA_THANH_ID",
                "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP",

                "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"

                )
                SELECT
                "MA_DOI_TUONG_THCP_ID"
                , ky_tinh_gia_thanh_id
                , SUM(COALESCE("NVL_TRUC_TIEP", 0))
                , SUM(COALESCE("NHAN_CONG_TRUC_TIEP", 0))
                , SUM(COALESCE("NHAN_CONG_GIAN_TIEP", 0)
                + COALESCE("NVL_GIAN_TIEP", 0)
                + COALESCE("CHI_PHI_MUA_NGOAI", 0)
                + COALESCE("CHI_PHI_KHAC", 0)
                + COALESCE("KHAU_HAO", 0))
                FROM gia_thanh_ket_qua_chi_phi_do_dang_cuoi_ky_chi_tiet AS JUD
                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                GROUP BY "MA_DOI_TUONG_THCP_ID"

                ;


                INSERT INTO TMP_KET_QUA
                ("DOI_TUONG_THCP_ID",
                "CONG_TRINH_ID",
                "DON_DAT_HANG_ID",
                "HOP_DONG_ID",
                "TONG_GIA_THANH",
                "LUY_KE_DA_NGHIEM_THU",
                "SO_CHUA_NGHIEM_THU",

                "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP",

                "DO_DANG_DAU_KY_CHI_PHI_CHUNG",
                "DO_DANG_DAU_KY_TONG",


                "NGUYEN_VAT_LIEU_TRUC_TIEP",
                "NHAN_CONG_TRUC_TIEP",


                "CHI_PHI_CHUNG",
                "PHAT_SINH_TRONG_KY_TONG",
                "KHOAN_GIAM_GIA_THANH",

                "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP",

                "DO_DANG_CUOI_KY_CHI_PHI_CHUNG",
                "DO_DANG_CUOI_KY_TONG",


                "MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP",
                "LOAI_DOI_TUONG_THCP",


                "BAC",
                "MA_PHAN_CAP"

                )
                SELECT
                J."DOI_TUONG_THCP_ID"
                , NULL AS "CONG_TRINH_ID"
                , NULL AS "DON_DAT_HANG_ID"
                , NULL AS "HOP_DONG_ID"
                , COALESCE("OPN_NVL_TRUC_TIEP", 0)
                + COALESCE("OPN_NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("OPN_CHI_PHI_CHUNG", 0)
                + COALESCE("NVL_TRUC_TIEP", 0)
                + COALESCE("PHAN_BO_NVL_TRUC_TIEP", 0)
                + COALESCE("NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("PHAN_BO_NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("CHI_PHI_CHUNG", 0)
                + COALESCE("PHAN_BO_CHI_PHI_CHUNG", 0)
                - COALESCE("KHOAN_GIAM_GIA_THANH", 0)
                - COALESCE("DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP", 0)
                - COALESCE("DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP", 0)
                - COALESCE("DO_DANG_CUOI_KY_CHI_PHI_CHUNG", 0) AS "TONG_GIA_THANH"
                , 0 AS "LUY_KE_DA_NGHIEM_THU"
                , 0 AS "SO_CHUA_NGHIEM_THU"
                , COALESCE("OPN_NVL_TRUC_TIEP", 0) AS "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"
                , COALESCE("OPN_NHAN_CONG_TRUC_TIEP", 0) AS "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP"

                , COALESCE("OPN_CHI_PHI_CHUNG", 0) AS "DO_DANG_DAU_KY_CHI_PHI_CHUNG"
                , COALESCE("OPN_NVL_TRUC_TIEP", 0)
                + COALESCE("OPN_NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("OPN_CHI_PHI_CHUNG", 0) AS "DO_DANG_DAU_KY_TONG"
                , COALESCE("NVL_TRUC_TIEP", 0)
                + COALESCE("PHAN_BO_NVL_TRUC_TIEP", 0) AS "NGUYEN_VAT_LIEU_TRUC_TIEP"
                , COALESCE("NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("PHAN_BO_NHAN_CONG_TRUC_TIEP", 0) AS "NHAN_CONG_TRUC_TIEP"

                , COALESCE("CHI_PHI_CHUNG", 0)
                + COALESCE("PHAN_BO_CHI_PHI_CHUNG", 0) AS "CHI_PHI_CHUNG"

                , COALESCE("NVL_TRUC_TIEP", 0)
                + COALESCE("PHAN_BO_NVL_TRUC_TIEP", 0)
                + COALESCE("NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("PHAN_BO_NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("CHI_PHI_CHUNG", 0)
                + COALESCE("PHAN_BO_CHI_PHI_CHUNG", 0) AS "PHAT_SINH_TRONG_KY_TONG"

                , COALESCE("KHOAN_GIAM_GIA_THANH", 0) AS "KHOAN_GIAM_GIA_THANH"
                , COALESCE("DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP", 0) AS "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"
                , COALESCE("DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP", 0) AS "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP"

                , COALESCE("DO_DANG_CUOI_KY_CHI_PHI_CHUNG", 0) AS "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"
                , COALESCE("DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP", 0)
                + COALESCE("DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP", 0)
                + COALESCE("DO_DANG_CUOI_KY_CHI_PHI_CHUNG", 0) AS "DO_DANG_CUOI_KY_TONG"

                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                , J."LOAI_DOI_TUONG_THCP"

                , J."BAC"
                , J."MA_PHAN_CAP"
                FROM TMP_DOI_TUONG_THCP AS J
                LEFT JOIN TMP_DO_DANG_DAU_KY AS OPN ON J."DOI_TUONG_THCP_ID" = OPN."DOI_TUONG_THCP_ID"
                LEFT JOIN TMP_PHAT_SINH_TRONG_KY AS U ON J."DOI_TUONG_THCP_ID" = U."DOI_TUONG_THCP_ID"
                LEFT JOIN TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY AS A ON J."DOI_TUONG_THCP_ID" = A."DOI_TUONG_THCP_ID"
                LEFT JOIN TMP_KHOAN_GIAM_GIA_THANH AS D ON J."DOI_TUONG_THCP_ID" = D."DOI_TUONG_THCP_ID"
                LEFT JOIN TMP_DO_DANG_CUOI_KY AS C ON J."DOI_TUONG_THCP_ID" = C."DOI_TUONG_THCP_ID"
                ORDER BY J."MA_PHAN_CAP"


                ;

                ELSE --Các PP khác


                -- Lấy dữ liệu hiển thị lên giao diện
                INSERT INTO TMP_KET_QUA
                (
                "DOI_TUONG_THCP_ID",
                "CONG_TRINH_ID",
                "DON_DAT_HANG_ID",
                "HOP_DONG_ID",
                "TONG_GIA_THANH",
                "LUY_KE_DA_NGHIEM_THU",
                "SO_CHUA_NGHIEM_THU",

                "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP",

                "DO_DANG_DAU_KY_CHI_PHI_CHUNG",
                "DO_DANG_DAU_KY_TONG",


                "NGUYEN_VAT_LIEU_TRUC_TIEP",
                "NHAN_CONG_TRUC_TIEP",


                "CHI_PHI_CHUNG",
                "PHAT_SINH_TRONG_KY_TONG",
                "KHOAN_GIAM_GIA_THANH",

                "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP",

                "DO_DANG_CUOI_KY_CHI_PHI_CHUNG",
                "DO_DANG_CUOI_KY_TONG",


                "MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP",
                "LOAI_DOI_TUONG_THCP"


                )
                SELECT
                JPJ."MA_DOI_TUONG_THCP_ID"
                , JPJ."MA_CONG_TRINH_ID"
                , JPJ."SO_DON_HANG_ID"
                , JPJ."SO_HOP_DONG_ID"
                , 0   AS "TONG_GIA_THANH"
                , 0   AS "LUY_KE_DA_NGHIEM_THU"
                , 0   AS "SO_CHUA_NGHIEM_THU"
                , 0   AS "DO_DANG_DAU_KY_NVL_TRUC_TIEP"
                , 0   AS "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP"

                , 0   AS "DO_DANG_DAU_KY_CHI_PHI_CHUNG"
                , 0   AS "DO_DANG_DAU_KY_TONG"
                , 0   AS "NGUYEN_VAT_LIEU_TRUC_TIEP"
                , 0   AS "NHAN_CONG_TRUC_TIEP"

                , 0   AS "CHI_PHI_CHUNG"
                , 0   AS "PHAT_SINH_TRONG_KY_TONG"
                , 0   AS "KHOAN_GIAM_GIA_THANH"
                , 0   AS "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"
                , 0   AS "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP"

                , 0   AS "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"
                , 0   AS "DO_DANG_CUOI_KY_TONG"

                , J."MA_DOI_TUONG_THCP"
                , j."TEN_DOI_TUONG_THCP"
                , CASE WHEN j."LOAI" = '0'
                THEN N'Phân xưởng'
                WHEN j."LOAI" = '1'
                THEN N'Sản phẩm'
                WHEN j."LOAI" = '2'
                THEN N'Quy trình sản xuất'
                WHEN j."LOAI" = '3'
                THEN N'Công đoạn'
                END AS "LOAI_DOI_TUONG_THCP"
                FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPJ
                LEFT JOIN account_ex_don_dat_hang AS SO ON so."id" = JPJ."SO_DON_HANG_ID"
                LEFT JOIN danh_muc_cong_trinh AS PW ON JPJ."MA_CONG_TRINH_ID" = PW."id"
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
                LEFT JOIN sale_ex_hop_dong_ban AS CT ON JPJ."SO_HOP_DONG_ID" = CT."id"
                LEFT JOIN res_partner AS AO ON CT."KHACH_HANG_ID" = AO."id"
                LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON JPJ."MA_DOI_TUONG_THCP_ID" = J."id"
                WHERE JPJ."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                ORDER BY pW."BAC" ASC
                ;


                END IF
                ;

                DROP TABLE  IF EXISTS TMP_KET_QUA_CUOI_CUNG;
                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                AS
                SELECT

                R.* FROM  TMP_KET_QUA R INNER JOIN TMP_DOI_TUONG_THCP_TS J ON J."DOI_TUONG_THCP_ID" = R."DOI_TUONG_THCP_ID";


                END $$
                ;

                SELECT 
                "MA_DOI_TUONG_THCP" AS"MA_DOI_TUONG_THCP",
                "TEN_DOI_TUONG_THCP" AS "TEN_DOI_TUONG_THCP",
                "LOAI_DOI_TUONG_THCP" AS "LOAI_DOI_TUONG_THCP",
                "TONG_GIA_THANH" AS "TONG_GIA_THANH",
                "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP" AS "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP" AS "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP",
                "DO_DANG_DAU_KY_CHI_PHI_CHUNG" AS "DO_DANG_DAU_KY_CHI_PHI_CHUNG",
                "DO_DANG_DAU_KY_TONG" AS "DO_DANG_DAU_KY_TONG",
                "NGUYEN_VAT_LIEU_TRUC_TIEP" AS "NGUYEN_VAT_LIEU_TRUC_TIEP",
                "NHAN_CONG_TRUC_TIEP" AS "NHAN_CONG_TRUC_TIEP",
                "CHI_PHI_CHUNG" AS "CHI_PHI_CHUNG",
                "PHAT_SINH_TRONG_KY_TONG" AS "PHAT_SINH_TRONG_KY_TONG",
                "KHOAN_GIAM_GIA_THANH" AS "KHOAN_GIAM_GIA_THANH",
                "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP" AS "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP" AS "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP",
                "DO_DANG_CUOI_KY_CHI_PHI_CHUNG" AS "DO_DANG_CUOI_KY_CHI_PHI_CHUNG",
                "DO_DANG_CUOI_KY_TONG" AS "DO_DANG_CUOI_KY_TONG"

                FROM  TMP_KET_QUA_CUOI_CUNG
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

                CHE_DO_KE_TOAN                      VARCHAR;

                MA_PHAN_CAP_NVLTT                   VARCHAR(100);

                MA_PHAN_CAP_NCTT                    VARCHAR(100);

                MA_PHAN_CAP_SXC                     VARCHAR(100);

                MA_PHAN_CAP_SXC_VL                  VARCHAR(100);

                MA_PHAN_CAP_SXC_DCSX                VARCHAR(100);

                MA_PHAN_CAP_SXC_NVPX                VARCHAR(100);

                MA_PHAN_CAP_SXC_KH                  VARCHAR(100);

                MA_PHAN_CAP_SXC_MN                  VARCHAR(100);

                MA_PHAN_CAP_CPSX                    VARCHAR(100);

                MA_PHAN_CAP_MTC                     VARCHAR(100);

                MA_PHAN_CAP_MTC_VL                  VARCHAR(100);

                MA_PHAN_CAP_MTC_DCSX                VARCHAR(100);

                MA_PHAN_CAP_MTC_NC                  VARCHAR(100);

                MA_PHAN_CAP_MTC_KH                  VARCHAR(100);

                MA_PHAN_CAP_MTC_MN                  VARCHAR(100);

                MA_PHAN_CAP_MTC_K                   VARCHAR(100);

                rec                                 RECORD;

                --@ListObjectID : tham số bên misa


                BEGIN


                SELECT value
                INTO CHE_DO_KE_TOAN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;


                -- KMCP: Sản xuất
                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_CPSX
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NVLTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NCTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_MTC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_SXC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                ;

                -- Chi phí sản xuất chung để lấy các phát sinh khác với CPSX


                DROP TABLE IF EXISTS TMP_TB
                ;

                CREATE TEMP TABLE TMP_TB

                (
                "CONG_TRINH_ID"  INT,
                "MA_PHAN_CAP"    VARCHAR(100)
                NULL,
                "MA_CONG_TRINH"  VARCHAR(20)

                NULL,
                "TEN_CONG_TRINH" VARCHAR(128)

                NULL

                )
                ;

                -- 1 bảng để lưu những CT đc chọn @Object
                -- 1 bảng để lưu những CT dùng để lấy dữ liệu (k lấy thằng cha)
                -- 1 bảng để
                INSERT INTO TMP_TB
                ("CONG_TRINH_ID",
                "MA_PHAN_CAP",
                "MA_CONG_TRINH",
                "TEN_CONG_TRINH"

                )
                SELECT DISTINCT
                EI."id"
                , EI."MA_PHAN_CAP"
                , EI."MA_CONG_TRINH"
                , EI."TEN_CONG_TRINH"

                FROM
                danh_muc_cong_trinh AS EI
                WHERE EI."id" = any (%(CONG_TRINH_IDS)s) --@ListObjectID
                ;
                DROP TABLE IF EXISTS TMP_TB_1
                ;
                CREATE TEMP TABLE TMP_TB_1
                (
                "CONG_TRINH_ID" INT PRIMARY KEY,
                "MA_PHAN_CAP"   VARCHAR(100)
                NULL
                )
                ;
                INSERT INTO TMP_TB_1
                SELECT
                S."CONG_TRINH_ID"
                , S."MA_PHAN_CAP"
                FROM TMP_TB S
                LEFT JOIN TMP_TB S1 ON S1."MA_PHAN_CAP" LIKE S."MA_PHAN_CAP"
                || '%%'
                AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE S1."MA_PHAN_CAP" IS NULL
                ;


                DROP TABLE IF EXISTS TMP_LIST
                ;

                CREATE TEMP TABLE TMP_LIST

                (
                "CONG_TRINH_ID" INT,
                "MA_PHAN_CAP"   VARCHAR(100)
                )
                ;

                DROP TABLE IF EXISTS TMP_BAC
                ;

                CREATE TEMP TABLE TMP_BAC


                (
                "CONG_TRINH_ID" INT PRIMARY KEY,
                "BAC"           INT
                )
                ;

                INSERT INTO TMP_BAC
                SELECT
                P."CONG_TRINH_ID"
                , COUNT(PD."MA_PHAN_CAP") AS "BAC"
                FROM TMP_TB P
                LEFT JOIN TMP_TB PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
                || '%%'
                AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                GROUP BY P."CONG_TRINH_ID"
                ;

                -- Bảng các khoản mục CP cha được chọn trong đó có chọn cả con mà là cha
                DROP TABLE IF EXISTS TMP_CHA
                ;

                CREATE TEMP TABLE TMP_CHA


                (
                "CONG_TRINH_ID" INT PRIMARY KEY
                )
                ;

                INSERT INTO TMP_CHA
                SELECT DISTINCT PD."CONG_TRINH_ID"
                FROM TMP_TB P
                LEFT JOIN TMP_TB PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
                || '%%'
                AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                WHERE PD."MA_PHAN_CAP" IS NOT NULL
                ;


                INSERT INTO TMP_LIST
                SELECT DISTINCT
                EI."id"
                , EI."MA_PHAN_CAP"
                FROM danh_muc_cong_trinh EI
                INNER JOIN TMP_TB_1 SEI ON EI."MA_PHAN_CAP" LIKE SEI."MA_PHAN_CAP"
                || '%%'
                ;

                DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                AS
                SELECT *
                FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                DROP TABLE IF EXISTS TMP_THU_THAP_CHI_PHI
                ;

                CREATE TEMP TABLE TMP_THU_THAP_CHI_PHI


                (
                "DOI_TUONG_ID"         INT,
                "SO_DA_NGHIEM_THU"     DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                "OPN_SO_DA_NGHIEM_THU" DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                "OPN_NGUYEN_VAT_LIEU"  DECIMAL(18, 4) DEFAULT (0), --Số kỹ kế kỳ trước
                "OPN_NHAN_CONG"        DECIMAL(18, 4) DEFAULT (0), -- Nhân công trực tiếp
                "OPN_MAY_THI_CONG"     DECIMAL(18, 4) DEFAULT (0), -- Máy thi công
                "OPN_CHI_PHI_CHUNG"    DECIMAL(18, 4) DEFAULT (0), -- Sản xuất chung
                "NGUYEN_VAT_LIEU"      DECIMAL(18, 4) DEFAULT (0), -- Phát sinh trong kỳ
                "NHAN_CONG"            DECIMAL(18, 4) DEFAULT (0),
                "MAY_THI_CONG"         DECIMAL(18, 4) DEFAULT (0),
                "CHI_PHI_CHUNG"        DECIMAL(18, 4) DEFAULT (0),
                "KHOAN_GIAM_GIA_THANH" DECIMAL(18, 4) DEFAULT (0), -- Khoản giảm giá thành
                "MA_PHAN_CAP"          VARCHAR(100)
                )
                ;


                /*
                1. Lấy trên số dư ban đầu
                2. Lấy trên bảng phân bổ: Cần phân biệt QD15,48
                3. Lấy trên sổ: Cần phân biệt QD15,48
                */

                /*1. Lấy số dư ban đầu*/

                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "MA_PHAN_CAP"
                )
                SELECT

                JP."CONG_TRINH_ID"
                , SUM(JO."SO_DA_NGHIEM_THU")               AS "SO_DA_NGHIEM_THU"
                , SUM(JO."SO_DA_NGHIEM_THU")               AS "SO_DA_NGHIEM_THU"
                , SUM(JO."CHI_PHI_NVL_TRUC_TIEP")          AS "OPN_NGUYEN_VAT_LIEU"
                , SUM(JO."CHI_PHI_NHAN_CONG_TRUC_TIEP")    AS "OPN_NHAN_CONG"
                , SUM(JO."MTC_CHI_PHI_KHAU_HAO_DAU_KY"
                + JO."MTC_CHI_PHI_NHAN_CONG"
                + JO."MTC_CHI_PHI_NVL_GIAN_TIEP"
                + JO."MTC_CHI_PHI_KHAC_CHUNG"
                + JO."MTC_CHI_PHI_MUA_NGOAI_DAU_KY") AS "OPN_MAY_THI_CONG"
                , SUM(JO."CHI_PHI_NHAN_CONG_GIAN_TIEP"
                + JO."NVL_GIAN_TIEP"
                + JO."KHAU_HAO"
                + JO."CHI_PHI_MUA_NGOAI"
                + JO."CHI_PHI_KHAC")                 AS "OPN_CHI_PHI_CHUNG"
                , JP."MA_PHAN_CAP"
                FROM TMP_LIST JP
                INNER JOIN account_ex_chi_phi_do_dang JO ON JO."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JO."CHI_NHANH_ID"
                WHERE
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JO."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE N'154%%'
                GROUP BY JP."CONG_TRINH_ID",
                JP."MA_PHAN_CAP"
                ;


                IF (CHE_DO_KE_TOAN = '15')
                THEN
                /*2. Lấy số liệu trên phân bổ*/
                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "MA_PHAN_CAP"
                )
                SELECT
                JP."CONG_TRINH_ID"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_NGUYEN_VAT_LIEU"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END) AS "NGUYEN_VAT_LIEU"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_NHAN_CONG"
                , (CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "NHAN_CONG"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_MAY_THI_CONG"
                , (CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "MAY_THI_CONG"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "CHI_PHI_CHUNG"
                , "MA_PHAN_CAP"
                FROM TMP_LIST JP
                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                LEFT JOIN (SELECT
                JCAD.*
                , J."TU_NGAY"
                , J."DEN_NGAY"
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = J."CHI_NHANH_ID"
                WHERE J."DEN_NGAY" <= den_ngay

                ) JCA ON JCA."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"

                GROUP BY
                JP."CONG_TRINH_ID",
                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                JCA."DEN_NGAY",
                JCA."TU_NGAY",
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID"),
                "MA_PHAN_CAP"
                ;


                /*3 Lấy số liệu trên sổ		*/

                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH",
                "MA_PHAN_CAP"

                )
                SELECT
                P."CONG_TRINH_ID"
                , (CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                AND GL."MA_TAI_KHOAN" LIKE '632%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                THEN SUM("GHI_NO")
                ELSE 0
                END) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND GL."MA_TAI_KHOAN" LIKE '632%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                THEN SUM("GHI_NO")
                ELSE 0
                END) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND ((GL."MA_TAI_KHOAN" LIKE '621%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                OR ("MA_TAI_KHOAN" LIKE N'154%%'
                AND "LOAI_HACH_TOAN" = '1'
                AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%'))
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
                )
                ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                THEN SUM("GHI_NO"
                - "GHI_CO")
                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN -SUM("GHI_CO")
                ELSE 0
                END) AS "OPN_NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND ((GL."MA_TAI_KHOAN" LIKE '621%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                OR ("MA_TAI_KHOAN" LIKE N'154%%'
                AND "LOAI_HACH_TOAN" = '1'
                AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%'))
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
                )
                ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '622%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "OPN_NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '622%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '623%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "OPN_MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '623%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '627%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '627%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                THEN SUM(GL."GHI_CO")
                ELSE 0
                END) AS "KHOAN_GIAM_GIA_THANH"
                , "MA_PHAN_CAP"
                FROM TMP_LIST AS P
                INNER JOIN so_cai_chi_tiet AS GL ON GL."CONG_TRINH_ID" = P."CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay

                AND GL."CONG_TRINH_ID" IS NOT NULL
                GROUP BY
                P."CONG_TRINH_ID",
                GL."MA_TAI_KHOAN",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."MA_TAI_KHOAN_DOI_UNG",
                GL."LOAI_HACH_TOAN",
                "MA_PHAN_CAP"

                ;


                ELSE -- QD48--------------------------------------------------------

                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "MA_PHAN_CAP"
                )

                SELECT
                JP."CONG_TRINH_ID"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_NGUYEN_VAT_LIEU"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END) AS "NGUYEN_VAT_LIEU"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_NHAN_CONG"
                , (CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "NHAN_CONG"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_MAY_THI_CONG"
                , (CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "MAY_THI_CONG"
                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (JCA."DEN_NGAY" >= tu_ngay
                AND JCA."DEN_NGAY" <= den_ngay
                )
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END)    AS "CHI_PHI_CHUNG"
                , JP."MA_PHAN_CAP" --BTAnh: JIRA 7781
                FROM TMP_LIST AS JP
                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                LEFT JOIN (SELECT
                JCAD.*
                , J."TU_NGAY"
                , J."DEN_NGAY"
                , E."MA_PHAN_CAP"
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = J."CHI_NHANH_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = JCAD."KHOAN_MUC_CP_ID"
                WHERE J."DEN_NGAY" <= den_ngay

                ) JCA ON JCA."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"

                AND JCA."KHOAN_MUC_CP_ID" IS NOT NULL
                GROUP BY JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                JCA."DEN_NGAY",
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID"),
                JCA."MA_PHAN_CAP",
                JP."CONG_TRINH_ID",
                JP."MA_PHAN_CAP"
                ;


                /*3 Lấy số liệu trên sổ		*/

                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH",
                "MA_PHAN_CAP"
                )
                SELECT
                JP."CONG_TRINH_ID"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" <= den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '632%%')
                AND (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%')
                AND (E."MA_PHAN_CAP" IS NULL
                OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                || '%%'
                )
                THEN SUM("GHI_NO")
                ELSE 0
                END) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '632%%')
                AND (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%')
                AND (E."MA_PHAN_CAP" IS NULL
                OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                || '%%'
                )
                THEN SUM("GHI_NO")
                ELSE 0
                END) AS "OPN_SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                /*PS Có TK 154 chi tiết theo công trình không chi tiết theo các KMCP sản xuất (không kể PSDU Nợ 632/154) trên các chứng từ có ngày hạch toán < Từ ngày của kỳ tập hợp chi phí*/
                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                AND (E."MA_PHAN_CAP" IS NULL
                OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                || '%%'
                )
                THEN -SUM("GHI_CO")
                ELSE 0
                END) AS "OPN_NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "NGUYEN_VAT_LIEU"
                , --NC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "OPN_NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "NHAN_CONG"
                , --MTC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "OPN_MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "MAY_THI_CONG"
                , -- CPC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                || '%%')
                THEN SUM("GHI_NO"
                - "GHI_CO")
                ELSE 0
                END) AS "CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                AND GL."LOAI_HACH_TOAN" = '2'
                )
                OR GL."LOAI_HACH_TOAN" = '1'
                )
                AND (E."MA_PHAN_CAP" IS NULL
                OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                || '%%'
                )
                THEN SUM(GL."GHI_CO")
                ELSE 0
                END) AS "KHOAN_GIAM_GIA_THANH"
                , JP."MA_PHAN_CAP"

                FROM TMP_LIST JP
                INNER JOIN so_cai_chi_tiet AS GL ON GL."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON GL."KHOAN_MUC_CP_ID" = E."id"
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay

                AND GL."CONG_TRINH_ID" IS NOT NULL
                GROUP BY
                JP."CONG_TRINH_ID",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."MA_TAI_KHOAN",
                GL."MA_TAI_KHOAN_DOI_UNG",
                E."MA_PHAN_CAP",
                GL."LOAI_HACH_TOAN",
                JP."MA_PHAN_CAP"
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
                ORDER BY JP."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH" )                                    AS "RowNum"
                , -- Lũy kế chi phí
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0
                )
                )
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0
                )
                )
                - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0
                )
                ),
                0
                )                                                                 AS "LUY_KE_CHI_PHI"
                , -- Lũy kế đã nghiệm thu
                COALESCE(SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0
                )
                ),
                0
                )                                                                 AS "LUY_KE_DA_NGHIEM_THU"
                , -- Số chưa nghiệm thu
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                0
                )
                )
                + SUM(COALESCE(CC."OPN_NHAN_CONG",
                0
                )
                )
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG",
                0
                )
                )
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG",
                0
                )
                )

                - SUM(COALESCE(CC."OPN_SO_DA_NGHIEM_THU",
                0
                )
                ), 0
                )                                                                 AS "SO_CHUA_NGHIEM_THU_DAU_KY"
                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0
                )
                )
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0
                )
                )
                - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0
                )
                )
                - SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0
                )
                ),
                0
                )                                                                 AS "SO_CHUA_NGHIEM_THU_CUOI_KY"
                , -- Lũy kế kỳ trước
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                0
                )
                ), 0
                )                                                                 AS "LK_KY_TRUOC_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG",
                0
                )
                ), 0
                )                                                                 AS "LK_TRUOC_NC_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG",
                0
                )
                ), 0
                )                                                                 AS "LK_TRUOC_MAY_THI_CONG"
                , COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG",
                0
                )
                ), 0
                )                                                                 AS "LK_TRUOC_CHI_PHI_CHUNG"
                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                0
                )
                )
                + SUM(COALESCE(CC."OPN_NHAN_CONG",
                0
                )
                )
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG",
                0
                )
                )
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG",
                0
                )
                ), 0
                )                                                                 AS "LUY_KE_TRUOC_TONG"
                , -- Lũy kế phát sinh trong kỳ
                COALESCE(SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0
                )
                ),
                0
                )                                                                 AS "LK_TRONG_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."NHAN_CONG", 0
                )
                ), 0
                )                                                                 AS "LK_TRONG_NC_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."MAY_THI_CONG", 0
                )
                ), 0
                )                                                                 AS "LK_TRONG_MAY_THI_CONG"
                , COALESCE(SUM(COALESCE(CC."CHI_PHI_CHUNG", 0
                )
                ), 0
                )                                                                 AS "LK_TRONG_CHI_PHI_CHUNG"
                , COALESCE(SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0
                )
                ), 0
                )                                                                 AS "LK_TRONG_TONG"
                , -- Khoản giảm chi phí
                COALESCE(SUM(COALESCE("KHOAN_GIAM_GIA_THANH", 0
                )
                ), 0
                )                                                                 AS "KHOAN_GIAM_GIA_THANH"
                , -- Lũy kế chi phí
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                0
                )
                )
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU",
                0
                )
                )
                - SUM(COALESCE("KHOAN_GIAM_GIA_THANH",
                0
                )
                ), 0
                )                                                                 AS "CP_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG",
                0
                )
                )
                + SUM(COALESCE(CC."NHAN_CONG", 0
                )
                ),
                0
                )                                                                 AS "CP_NC_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."MAY_THI_CONG", 0
                )
                ),
                0
                )                                                                 AS "CP_MAY_THI_CONG"
                , COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0
                )
                )
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0
                )
                ),
                0
                )                                                                 AS "CP_CHI_PHI_CHUNG"
                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0
                )
                )
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0
                )
                )
                + SUM(COALESCE(CC."NHAN_CONG", 0
                )
                )
                + SUM(COALESCE(CC."MAY_THI_CONG", 0
                )
                )
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0
                )
                ),
                0
                )
                - COALESCE(SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0
                )
                ), 0
                )                                                                 AS "CP_TONG"
                , PW."id"                                                           AS "CONG_TRINH_ID"
                , PW."TEN_CONG_TRINH"
                , PWC."name"                                                        AS "LOAI_CONG_TRINH"

                , PW."MA_CONG_TRINH"
                , CONCAT(REPEAT(' ', CAST(GP."BAC" * 4 AS INT)), PW."MA_CONG_TRINH") AS "MA_DOI_TUONG_THCP"

                , CAST(CASE WHEN PP."CONG_TRINH_ID" IS NULL
                THEN 0
                ELSE 1
                END AS BOOLEAN
                )                                                                 AS IsBold
                FROM TMP_TB AS JP
                LEFT JOIN TMP_THU_THAP_CHI_PHI CC ON CC."MA_PHAN_CAP" LIKE JP."MA_PHAN_CAP"
                || '%%'
                LEFT JOIN danh_muc_cong_trinh AS PW ON JP."CONG_TRINH_ID" = PW."id"
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
                LEFT JOIN TMP_CHA PP ON PP."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                INNER JOIN TMP_BAC GP ON GP."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                GROUP BY
                JP."CONG_TRINH_ID",
                PW."id",
                PW."TEN_CONG_TRINH",
                PWC."name",
                PW."BAC",
                PW."MA_PHAN_CAP",
                PW."MA_CONG_TRINH",
                JP."MA_PHAN_CAP",
                CONCAT(REPEAT(' ', CAST(GP."BAC" * 4 AS INT)), PW."MA_CONG_TRINH"),

                CAST(CASE WHEN PP."CONG_TRINH_ID" IS NULL
                THEN 0
                ELSE 1
                END AS BOOLEAN
                )
                ;
                END $$
                ;
                SELECT 
                "MA_CONG_TRINH" AS "MA_CONG_TRINH",
                "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
                "LOAI_CONG_TRINH" AS "LOAI_CONG_TRINH",
                "LUY_KE_CHI_PHI" AS "LUY_KE_CHI_PHI",
                "LUY_KE_DA_NGHIEM_THU" AS "LUY_KE_DA_NGHIEM_THU",
                "SO_CHUA_NGHIEM_THU_DAU_KY" AS "SO_CHUA_NGHIEM_THU_DAU_KY",
                "SO_CHUA_NGHIEM_THU_CUOI_KY" AS "SO_CHUA_NGHIEM_THU_CUOI_KY",
                "LK_KY_TRUOC_NVL_TRUC_TIEP" AS "LK_KY_TRUOC_NVL_TRUC_TIEP",
                "LK_TRUOC_NC_TRUC_TIEP" AS "LK_TRUOC_NC_TRUC_TIEP",
                "LK_TRUOC_MAY_THI_CONG" AS "LK_TRUOC_MAY_THI_CONG",
                "LK_TRUOC_CHI_PHI_CHUNG" AS "LK_TRUOC_CHI_PHI_CHUNG",
                "LUY_KE_TRUOC_TONG" AS "LUY_KE_TRUOC_TONG",
                "LK_TRONG_NVL_TRUC_TIEP" AS "LK_TRONG_NVL_TRUC_TIEP",
                "LK_TRONG_NC_TRUC_TIEP" AS "LK_TRONG_NC_TRUC_TIEP",
                "LK_TRONG_MAY_THI_CONG" AS "LK_TRONG_MAY_THI_CONG",
                "LK_TRONG_CHI_PHI_CHUNG" AS "LK_TRONG_CHI_PHI_CHUNG",
                "LK_TRONG_TONG" AS "LK_TRONG_TONG",
                "KHOAN_GIAM_GIA_THANH" AS "KHOAN_GIAM_GIA_THANH",
                "CP_NVL_TRUC_TIEP" AS "CP_NVL_TRUC_TIEP",
                "CP_NC_TRUC_TIEP" AS "CP_NC_TRUC_TIEP",
                "CP_MAY_THI_CONG" AS "CP_MAY_THI_CONG",
                "CP_CHI_PHI_CHUNG" AS "CP_CHI_PHI_CHUNG",
                "CP_TONG" AS "CP_TONG"

                FROM TMP_KET_QUA

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

                CHE_DO_KE_TOAN                      VARCHAR;

                MA_PHAN_CAP_NVLTT                   VARCHAR(100);

                MA_PHAN_CAP_NCTT                    VARCHAR(100);

                MA_PHAN_CAP_SXC                     VARCHAR(100);

                MA_PHAN_CAP_CPSX                    VARCHAR(100);

                MA_PHAN_CAP_MTC                     VARCHAR(100);

                LOAI_GIA_THANH                      VARCHAR(100) :='CONG_TRINH';

                rec                                 RECORD;

                --@ListObjectID : tham số bên misa


                BEGIN


                SELECT value
                INTO CHE_DO_KE_TOAN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;

                --     CHE_DO_KE_TOAN = '48'
                --     ;

                -- KMCP: Sản xuất
                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_CPSX
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NVLTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NCTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_MTC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_SXC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                ;



                DROP TABLE IF EXISTS TMP_THU_THAP_CHI_PHI
                ;

                CREATE TEMP TABLE TMP_THU_THAP_CHI_PHI


                (
                "DON_HANG_ID"          INT,
                "SO_DA_NGHIEM_THU"     DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                "OPN_SO_DA_NGHIEM_THU" DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                "OPN_NGUYEN_VAT_LIEU"  DECIMAL(18, 4) DEFAULT (0), --Số kỹ kế kỳ trước
                "OPN_NHAN_CONG"        DECIMAL(18, 4) DEFAULT (0), -- Nhân công trực tiếp
                "OPN_MAY_THI_CONG"     DECIMAL(18, 4) DEFAULT (0), -- Máy thi công
                "OPN_CHI_PHI_CHUNG"    DECIMAL(18, 4) DEFAULT (0), -- Sản xuất chung
                "NGUYEN_VAT_LIEU"      DECIMAL(18, 4) DEFAULT (0), -- Phát sinh trong kỳ
                "NHAN_CONG"            DECIMAL(18, 4) DEFAULT (0),
                "MAY_THI_CONG"         DECIMAL(18, 4) DEFAULT (0),
                "CHI_PHI_CHUNG"        DECIMAL(18, 4) DEFAULT (0),
                "KHOAN_GIAM_GIA_THANH" DECIMAL(18, 4) DEFAULT (0) -- Khoản giảm giá thành

                )
                ;

                DROP TABLE IF EXISTS TMP_DON_HANG_ID
                ;

                CREATE TEMP TABLE TMP_DON_HANG_ID
                AS
                SELECT id AS "DON_HANG_ID"
                FROM account_ex_don_dat_hang
                WHERE id = any (%(DON_HANG_IDS)s)
                ;

                IF EXISTS(SELECT O.*
                FROM account_ex_don_dat_hang AS SO INNER JOIN TMP_DON_HANG_ID AS O ON O."DON_HANG_ID" = SO."id"
                LIMIT 1)
                THEN
                LOAI_GIA_THANH = 'DON_HANG'
                ;
                END IF
                ;

                --     IF EXISTS(SELECT O.*
                --               FROM sale_ex_hop_dong_ban AS C INNER JOIN TMP_DON_HANG_ID AS O ON O."DON_HANG_ID" = C."id"
                --               LIMIT 1)
                --     THEN
                --         LOAI_GIA_THANH = 'HOP_DONG'
                --         ;
                --     END IF
                --     ;


                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DON_HANG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG"
                )
                SELECT

                JP."DON_HANG_ID"
                , SUM(JO."SO_DA_NGHIEM_THU")                                           AS "SO_DA_NGHIEM_THU"
                , SUM(JO."SO_DA_NGHIEM_THU")                                           AS "OPN_SO_DA_NGHIEM_THU"
                , SUM(JO."CHI_PHI_NVL_TRUC_TIEP")                                      AS "OPN_NGUYEN_VAT_LIEU"
                , SUM(JO."CHI_PHI_NHAN_CONG_TRUC_TIEP")                                AS "OPN_NHAN_CONG"
                , SUM(JO."MTC_CHI_PHI_KHAU_HAO_DAU_KY" + JO."MTC_CHI_PHI_NHAN_CONG" + JO."MTC_CHI_PHI_NVL_GIAN_TIEP" +
                JO."MTC_CHI_PHI_KHAC_CHUNG" + JO."MTC_CHI_PHI_MUA_NGOAI_DAU_KY") AS "OPN_MAY_THI_CONG"
                , SUM(JO."CHI_PHI_NHAN_CONG_GIAN_TIEP" + JO."NVL_GIAN_TIEP" + JO."KHAU_HAO" + JO."CHI_PHI_MUA_NGOAI" +
                JO."CHI_PHI_KHAC")                                               AS "OPN_CHI_PHI_CHUNG"
                FROM TMP_DON_HANG_ID JP
                LEFT JOIN account_ex_chi_phi_do_dang JO
                ON ((LOAI_GIA_THANH = 'CONG_TRINH' AND JO."MA_CONG_TRINH_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'DON_HANG' AND JO."DON_HANG_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND JO."HOP_DONG_ID" = JP."DON_HANG_ID")
                )
                WHERE JO."CHI_NHANH_ID" = chi_nhanh_id

                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JO."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE N'154%%'
                GROUP BY JP."DON_HANG_ID"

                ;

                IF (CHE_DO_KE_TOAN = '15')
                THEN
                /*2. Lấy số liệu trên phân bổ*/
                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DON_HANG_ID",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG"
                )
                SELECT
                JP."DON_HANG_ID"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , (
                CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH' AND JCA."DEN_NGAY" < tu_ngay AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (
                CASE WHEN
                (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH'
                AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"

                FROM TMP_DON_HANG_ID JP
                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                LEFT JOIN (SELECT
                JCAD.*
                , J."TU_NGAY"
                , J."DEN_NGAY"
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                WHERE J."DEN_NGAY" <=
                den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                ) JCA ON ((LOAI_GIA_THANH = 'CONG_TRINH' AND JCA."MA_CONG_TRINH_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'DON_HANG' AND JCA."SO_DON_HANG_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND JCA."SO_HOP_DONG_ID" = JP."DON_HANG_ID")
                )

                GROUP BY
                JP."DON_HANG_ID",
                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                JCA."DEN_NGAY", JCA."TU_NGAY",
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID")
                ;


                INSERT INTO TMP_THU_THAP_CHI_PHI
                (
                "DON_HANG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH"
                )
                SELECT
                P."DON_HANG_ID"
                , (CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay AND GL."MA_TAI_KHOAN" LIKE '632%%' AND
                GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND GL."MA_TAI_KHOAN" LIKE '632%%' AND
                GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "OPN_SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND ((GL."MA_TAI_KHOAN" LIKE '621%%') AND (
                (GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR GL."LOAI_HACH_TOAN" = '1')
                OR ("MA_TAI_KHOAN" LIKE N'154%%' AND
                "LOAI_HACH_TOAN" = '1' AND
                Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                (LOAI_GIA_THANH <> 'CONG_TRINH' OR
                (LOAI_GIA_THANH = 'CONG_TRINH' AND
                GL."MA_TAI_KHOAN_DOI_UNG"
                NOT LIKE '623%%')) AND
                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE
                '627%%')) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                THEN SUM("GHI_NO" - "GHI_CO")
                WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN -SUM("GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (
                (GL."MA_TAI_KHOAN" LIKE '621%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                (LOAI_GIA_THANH <> 'CONG_TRINH' OR
                (LOAI_GIA_THANH = 'CONG_TRINH' AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%')) AND
                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE
                '627%%')) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '622%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '622%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , (CASE WHEN
                LOAI_GIA_THANH = 'CONG_TRINH' AND (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '623%%')
                AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH' AND (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
                (GL."MA_TAI_KHOAN" LIKE '623%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '627%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '627%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM(GL."GHI_CO")
                ELSE 0
                END
                ) AS "KHOAN_GIAM_GIA_THANH"

                FROM TMP_DON_HANG_ID AS P INNER JOIN
                so_cai_chi_tiet AS GL ON ((LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" = P."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" = P."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" = P."DON_HANG_ID")
                )
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                AND ((LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" IS NOT NULL)
                OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" IS NOT NULL)
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" IS NOT NULL)
                )

                GROUP BY
                P."DON_HANG_ID",
                GL."MA_TAI_KHOAN",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."MA_TAI_KHOAN_DOI_UNG",
                GL."LOAI_HACH_TOAN"

                ;


                ELSE -- QD48--------------------------------------------------------

                INSERT INTO TMP_THU_THAP_CHI_PHI
                (
                "DON_HANG_ID",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG"
                )
                SELECT
                JP."DON_HANG_ID"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (-- Nếu có JCAJC"PHAT_SINH_TRONG_KY"DetailID=JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , (
                CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH' AND JCA."DEN_NGAY" < tu_ngay AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (
                CASE WHEN
                (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH'
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"

                FROM TMP_DON_HANG_ID AS JP

                LEFT JOIN (SELECT
                JCAD.*
                , J."TU_NGAY"
                , J."DEN_NGAY"
                , E."MA_PHAN_CAP"
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = JCAD."KHOAN_MUC_CP_ID"
                WHERE J."DEN_NGAY" <=
                den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                ) JCA ON ((LOAI_GIA_THANH = 'CONG_TRINH' AND JCA."MA_CONG_TRINH_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'DON_HANG' AND JCA."SO_DON_HANG_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND JCA."SO_HOP_DONG_ID" = JP."DON_HANG_ID")
                )

                AND JCA."KHOAN_MUC_CP_ID" IS NOT NULL
                GROUP BY
                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                JCA."DEN_NGAY",
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID"),
                JCA."MA_PHAN_CAP", JP."DON_HANG_ID"

                ;


                /*3 Lấy số liệu trên sổ		*/

                INSERT INTO TMP_THU_THAP_CHI_PHI
                (
                "DON_HANG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH"
                )
                SELECT
                JP."DON_HANG_ID"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" <= den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '632%%') AND
                (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '632%%') AND
                (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "OPN_SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                /*PS Có TK 154 chi tiết theo công trình không chi tiết theo các KMCP sản xuất (không kể PSDU Nợ 632/154) trên các chứng từ có ngày hạch toán < Từ ngày của kỳ tập hợp chi phí*/
                WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN -SUM("GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , --NC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , --MTC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH' AND
                (GL."MA_TAI_KHOAN" LIKE '154%%') AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH' AND
                (GL."MA_TAI_KHOAN" LIKE '154%%') AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , -- CPC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN SUM(GL."GHI_CO")
                ELSE 0
                END
                ) AS "KHOAN_GIAM_GIA_THANH"

                FROM TMP_DON_HANG_ID JP INNER JOIN so_cai_chi_tiet AS GL
                ON ((LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" = JP."DON_HANG_ID")
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" = JP."DON_HANG_ID")
                )
                LEFT JOIN danh_muc_khoan_muc_cp E ON GL."KHOAN_MUC_CP_ID" = E."id"
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                AND ((LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" IS NOT NULL)
                OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" IS NOT NULL)
                OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" IS NOT NULL)
                )

                GROUP BY
                JP."DON_HANG_ID",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."MA_TAI_KHOAN",
                GL."MA_TAI_KHOAN_DOI_UNG",
                E."MA_PHAN_CAP",
                GL."LOAI_HACH_TOAN"
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
                ORDER BY "NGAY_DON_HANG", "SO_DON_HANG", AO."MA", "SO_HOP_DONG", "NGAY_KY", PW."MA_PHAN_CAP",

                PW."MA_CONG_TRINH", PWC."name" )                                    AS "RowNum"

                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                , 0)                                                    AS "LUY_KE_CHI_PHI"
                , -- Lũy kế đã nghiệm thu
                COALESCE(SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0)), 0)    AS "LUY_KE_DA_NGHIEM_THU"
                , -- Số chưa nghiệm thu
                COALESCE(
                SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))

                - SUM(COALESCE(CC."OPN_SO_DA_NGHIEM_THU", 0))
                , 0)                                                AS "SO_CHUA_NGHIEM_THU_DAU_KY"
                , COALESCE(
                SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                - SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0))
                , 0)                                                AS "SO_CHUA_NGHIEM_THU_CUOI_KY"
                , -- Lũy kế kỳ trước
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0)), 0) AS "LK_KY_TRUOC_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG", 0)), 0)       AS "LK_TRUOC_NC_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0)), 0)    AS "LK_TRUOC_MAY_THI_CONG"
                , COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0)), 0)   AS "LK_TRUOC_CHI_PHI_CHUNG"
                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                , 0)                                                          AS "LUY_KE_TRUOC_TONG"
                , -- Lũy kế phát sinh trong kỳ
                COALESCE(SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0)), 0)     AS "LK_TRONG_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."NHAN_CONG", 0)), 0)           AS "LK_TRONG_NC_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."MAY_THI_CONG", 0)), 0)        AS "LK_TRONG_MAY_THI_CONG"
                , COALESCE(SUM(COALESCE(CC."CHI_PHI_CHUNG", 0)), 0)       AS "LK_TRONG_CHI_PHI_CHUNG"
                , COALESCE(
                SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                , 0)                                                AS "LK_TRONG_TONG"
                , -- Khoản giảm chi phí
                COALESCE(SUM(COALESCE("KHOAN_GIAM_GIA_THANH", 0)), 0)   AS "KHOAN_GIAM_GIA_THANH"
                , -- Lũy kế chi phí
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0)) + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0)) -
                SUM(COALESCE("KHOAN_GIAM_GIA_THANH", 0)), 0)   AS "CP_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG", 0)) + SUM(COALESCE(CC."NHAN_CONG", 0))
                , 0)                                                          AS "CP_NC_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                , 0)                                                          AS "CP_MAY_THI_CONG"
                , COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0)) + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                , 0)                                                          AS "CP_CHI_PHI_CHUNG"
                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                , 0)
                - COALESCE(SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                , 0)                                                          AS "CP_TONG"


                , AO."MA"                                                 AS "MA_KHACH_HANG"
                , AO."HO_VA_TEN"                                          AS "TEN_KHACH_HANG"

                , SO."id"                                                 AS "DON_HANG_ID"
                , 'account.ex.don.dat.hang'                               AS "MODEL_CHUNG_TU"
                , "SO_DON_HANG"
                , "NGAY_DON_HANG"
                , SO."LOAI_CHUNG_TU"
                , SO."DIEN_GIAI"                                               AS "DIEN_GIAI"
                , C."SO_HOP_DONG"
                , C."NGAY_KY"
                , PW."MA_PHAN_CAP"

                , PW."MA_CONG_TRINH"
                , PWC."name"
                FROM TMP_DON_HANG_ID AS JP
                LEFT JOIN TMP_THU_THAP_CHI_PHI CC ON JP."DON_HANG_ID" = CC."DON_HANG_ID"
                LEFT JOIN danh_muc_cong_trinh AS PW ON JP."DON_HANG_ID" = PW."id"
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
                LEFT JOIN sale_ex_hop_dong_ban AS C ON C."id" = JP."DON_HANG_ID"
                LEFT JOIN account_ex_don_dat_hang AS SO ON SO."id" = JP."DON_HANG_ID"
                LEFT JOIN res_partner AS AO ON ((LOAI_GIA_THANH = 'HOP_DONG' AND AO."id" = C."KHACH_HANG_ID")
                OR (LOAI_GIA_THANH = 'DON_HANG' AND AO."id" = SO."KHACH_HANG_ID"))

                GROUP BY



                AO."MA",
                AO."HO_VA_TEN",

                SO."id",
                "SO_DON_HANG",
                "NGAY_DON_HANG",
                SO."LOAI_CHUNG_TU",
                "GHI_CHU",
                C."SO_HOP_DONG",
                C."NGAY_KY",
                PW."MA_PHAN_CAP",

                PW."MA_CONG_TRINH", PWC."name"
                ORDER BY "NGAY_DON_HANG", "SO_DON_HANG", AO."MA", "SO_HOP_DONG", "NGAY_KY", PW."MA_PHAN_CAP",

                PW."MA_CONG_TRINH", PWC."name"
                ;


                END $$
                ;


                SELECT 
                "SO_DON_HANG" AS "SO_DON_HANG",
                "NGAY_DON_HANG" AS "NGAY_DON_HANG",
                "DIEN_GIAI" AS "DIEN_GIAI",
                "TEN_KHACH_HANG" AS "TEN_KHACH_HANG",
                "LUY_KE_CHI_PHI" AS "LUY_KE_CHI_PHI",
                "LUY_KE_DA_NGHIEM_THU" AS "LUY_KE_DA_NGHIEM_THU",
                "SO_CHUA_NGHIEM_THU_DAU_KY" AS "SO_CHUA_NGHIEM_THU_DAU_KY",
                "SO_CHUA_NGHIEM_THU_CUOI_KY" AS "SO_CHUA_NGHIEM_THU_CUOI_KY",
                "LK_KY_TRUOC_NVL_TRUC_TIEP" AS "LK_KY_TRUOC_NVL_TRUC_TIEP",
                "LK_TRUOC_NC_TRUC_TIEP" AS "LK_TRUOC_NC_TRUC_TIEP",
                "LK_TRUOC_MAY_THI_CONG" AS "LK_TRUOC_MAY_THI_CONG",
                "LK_TRUOC_CHI_PHI_CHUNG" AS "LK_TRUOC_CHI_PHI_CHUNG",
                "LUY_KE_TRUOC_TONG" AS "LUY_KE_TRUOC_TONG",
                "LK_TRONG_NVL_TRUC_TIEP" AS "LK_TRONG_NVL_TRUC_TIEP",
                "LK_TRONG_NC_TRUC_TIEP" AS "LK_TRONG_NC_TRUC_TIEP",
                "LK_TRONG_MAY_THI_CONG" AS "LK_TRONG_MAY_THI_CONG",
                "LK_TRONG_CHI_PHI_CHUNG" AS "LK_TRONG_CHI_PHI_CHUNG",
                "LK_TRONG_TONG" AS "LK_TRONG_TONG",
                "KHOAN_GIAM_GIA_THANH" AS "KHOAN_GIAM_GIA_THANH",
                "CP_NVL_TRUC_TIEP" AS "CP_NVL_TRUC_TIEP",
                "CP_NC_TRUC_TIEP" AS "CP_NC_TRUC_TIEP",
                "CP_MAY_THI_CONG" AS "CP_MAY_THI_CONG",
                "CP_CHI_PHI_CHUNG" AS "CP_CHI_PHI_CHUNG",
                "CP_TONG" AS "CP_TONG",
                "DON_HANG_ID" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC"

                FROM TMP_KET_QUA

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
                tu_ngay         TIMESTAMP := %(TU_NGAY)s;

                den_ngay        TIMESTAMP := %(DEN_NGAY)s;

                chi_nhanh_id      INTEGER := %(CHI_NHANH_ID)s;

                CHE_DO_KE_TOAN    VARCHAR;

                MA_PHAN_CAP_NVLTT VARCHAR(100);

                MA_PHAN_CAP_NCTT  VARCHAR(100);

                MA_PHAN_CAP_SXC   VARCHAR(100);

                MA_PHAN_CAP_CPSX  VARCHAR(100);

                MA_PHAN_CAP_MTC   VARCHAR(100);

                LOAI_GIA_THANH    VARCHAR(100) :='DON_HANG';

                rec               RECORD;

                --@ListObjectID : tham số bên misa

                BEGIN


                SELECT value
                INTO CHE_DO_KE_TOAN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;




                -- KMCP: Sản xuất
                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_CPSX
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NVLTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NCTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_MTC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_SXC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                ;


                DROP TABLE IF EXISTS TMP_TB
                ;

                CREATE TEMP TABLE TMP_TB


                (
                "HOP_DONG_ID"    INT,
                "SO_HOP_DONG"    VARCHAR(50),
                "TRICH_YEU"      VARCHAR(255),
                "THUOC_DU_AN_ID" INT
                )
                ;

                -- 1 bảng để lưu những CT đc chọn @Object
                -- 1 bảng để lưu những CT dùng để lấy dữ liệu (k lấy thằng cha)
                -- 1 bảng để
                INSERT INTO TMP_TB
                ("HOP_DONG_ID",
                "SO_HOP_DONG",
                "TRICH_YEU",
                "THUOC_DU_AN_ID")
                SELECT DISTINCT
                EI."id"
                , EI."SO_HOP_DONG"
                , EI."TRICH_YEU"
                , "THUOC_DU_AN_ID"
                FROM sale_ex_hop_dong_ban AS EI
                WHERE EI."id" = any(%(HOP_DONG_BAN_IDS)s) ----@ListObjectID
                ;


                DROP TABLE IF EXISTS TMP_TB_1
                ;

                CREATE TEMP TABLE TMP_TB_1


                (
                "HOP_DONG_ID"    INT,
                "THUOC_DU_AN_ID" INT
                )
                ;

                INSERT INTO TMP_TB_1
                SELECT
                S."HOP_DONG_ID"
                , S."THUOC_DU_AN_ID"
                FROM TMP_TB S
                LEFT JOIN TMP_TB S1 ON S1."THUOC_DU_AN_ID" = S."HOP_DONG_ID"
                WHERE S1."HOP_DONG_ID" IS NULL
                ;


                DROP TABLE IF EXISTS TMP_LIST
                ;

                CREATE TEMP TABLE TMP_LIST

                -- Bảng khoản mục CP gồm toàn bộ khoản mục CP con
                (
                "HOP_DONG_ID"    INT,
                "THUOC_DU_AN_ID" INT
                )
                ;


                INSERT INTO TMP_LIST
                SELECT DISTINCT
                C."id"
                , C."THUOC_DU_AN_ID"
                FROM sale_ex_hop_dong_ban AS C
                INNER JOIN TMP_TB_1 SEI ON (SEI."HOP_DONG_ID" = C."THUOC_DU_AN_ID")
                UNION
                SELECT
                T."HOP_DONG_ID"
                , T."THUOC_DU_AN_ID"
                FROM TMP_TB AS T
                ;

                -- Bảng các khoản mục CP cha được chọn trong đó có chọn cả con mà là cha

                DROP TABLE IF EXISTS TMP_CHA
                ;

                CREATE TEMP TABLE TMP_CHA

                (
                "HOP_DONG_ID" INT
                )
                ;

                INSERT INTO TMP_CHA
                SELECT DISTINCT P."HOP_DONG_ID"
                FROM TMP_TB P
                LEFT JOIN TMP_TB PD ON P."HOP_DONG_ID" = PD."THUOC_DU_AN_ID"
                WHERE PD."THUOC_DU_AN_ID" IS NOT NULL
                ;

                DROP TABLE IF EXISTS TMP_BAC
                ;

                CREATE TEMP TABLE TMP_BAC

                -- Tính bậc để lùi dòng cho báo cáo hình cây
                (
                "HOP_DONG_ID" INT,
                "BAC"         INT
                )
                ;

                INSERT INTO TMP_BAC
                SELECT
                P."HOP_DONG_ID"
                , COUNT(PD."HOP_DONG_ID") AS "BAC"
                FROM TMP_TB P
                LEFT JOIN TMP_TB PD
                ON (PD."HOP_DONG_ID" = P."THUOC_DU_AN_ID")
                GROUP BY P."HOP_DONG_ID"
                ;

                DROP TABLE IF EXISTS TMP_THU_THAP_CHI_PHI
                ;

                CREATE TEMP TABLE TMP_THU_THAP_CHI_PHI

                (
                "DOI_TUONG_ID"         INT,
                "SO_DA_NGHIEM_THU"     DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                "OPN_SO_DA_NGHIEM_THU" DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                "OPN_NGUYEN_VAT_LIEU"  DECIMAL(18, 4) DEFAULT (0), --Số kỹ kế kỳ trước
                "OPN_NHAN_CONG"        DECIMAL(18, 4) DEFAULT (0), -- Nhân công trực tiếp
                "OPN_MAY_THI_CONG"     DECIMAL(18, 4) DEFAULT (0), -- Máy thi công
                "OPN_CHI_PHI_CHUNG"    DECIMAL(18, 4) DEFAULT (0), -- Sản xuất chung
                "NGUYEN_VAT_LIEU"      DECIMAL(18, 4) DEFAULT (0), -- Phát sinh trong kỳ
                "NHAN_CONG"            DECIMAL(18, 4) DEFAULT (0),
                "MAY_THI_CONG"         DECIMAL(18, 4) DEFAULT (0),
                "CHI_PHI_CHUNG"        DECIMAL(18, 4) DEFAULT (0),
                "KHOAN_GIAM_GIA_THANH" DECIMAL(18, 4) DEFAULT (0), -- Khoản giảm giá thành
                "THUOC_DU_AN_ID"       INT
                )
                ;

                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "THUOC_DU_AN_ID"
                )

                SELECT

                JP."HOP_DONG_ID"
                , SUM(JO."SO_DA_NGHIEM_THU")                                           AS "SO_DA_NGHIEM_THU"
                , SUM(JO."SO_DA_NGHIEM_THU")                                           AS "OPN_SO_DA_NGHIEM_THU"
                , SUM(JO."CHI_PHI_NVL_TRUC_TIEP")                                      AS "OPN_NGUYEN_VAT_LIEU"
                , SUM(JO."CHI_PHI_NHAN_CONG_TRUC_TIEP")                                AS "OPN_NHAN_CONG"
                , SUM(JO."MTC_CHI_PHI_KHAU_HAO_DAU_KY" + JO."MTC_CHI_PHI_NHAN_CONG" + JO."MTC_CHI_PHI_NVL_GIAN_TIEP" +
                JO."MTC_CHI_PHI_KHAC_CHUNG" + JO."MTC_CHI_PHI_MUA_NGOAI_DAU_KY") AS "OPN_MAY_THI_CONG"
                , SUM(JO."CHI_PHI_NHAN_CONG_GIAN_TIEP" + JO."NVL_GIAN_TIEP" + JO."KHAU_HAO" + JO."CHI_PHI_MUA_NGOAI" +
                JO."CHI_PHI_KHAC")                                               AS "OPN_CHI_PHI_CHUNG"
                , JP."THUOC_DU_AN_ID"
                FROM TMP_LIST JP
                LEFT JOIN account_ex_chi_phi_do_dang JO ON JO."HOP_DONG_ID" = JP."HOP_DONG_ID"
                WHERE JO."CHI_NHANH_ID" = chi_nhanh_id

                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JO."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE N'154%%'
                GROUP BY JP."HOP_DONG_ID", JP."THUOC_DU_AN_ID"
                ;


                IF (CHE_DO_KE_TOAN = '15')
                THEN
                /*2. Lấy số liệu trên phân bổ*/
                INSERT INTO TMP_THU_THAP_CHI_PHI
                ("DOI_TUONG_ID",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "THUOC_DU_AN_ID"
                )
                SELECT
                JP."HOP_DONG_ID"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"
                , "THUOC_DU_AN_ID"
                FROM TMP_LIST JP
                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                LEFT JOIN (SELECT
                JCAD.*
                , J."TU_NGAY"
                , J."DEN_NGAY"
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                WHERE J."DEN_NGAY" <=
                den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                ) JCA ON JCA."SO_HOP_DONG_ID" = JP."HOP_DONG_ID"

                GROUP BY
                JP."HOP_DONG_ID",
                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                JCA."DEN_NGAY", JCA."TU_NGAY",
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID"), "THUOC_DU_AN_ID"
                ;


                /*3 Lấy số liệu trên sổ		*/

                INSERT INTO TMP_THU_THAP_CHI_PHI
                (
                "DOI_TUONG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH",
                "THUOC_DU_AN_ID"
                )
                SELECT
                P."HOP_DONG_ID"
                , (CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay AND GL."MA_TAI_KHOAN" LIKE '632%%' AND
                GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND GL."MA_TAI_KHOAN" LIKE '632%%' AND
                GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "OPN_SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND ((GL."MA_TAI_KHOAN" LIKE '621%%') AND (
                (GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR GL."LOAI_HACH_TOAN" = '1')
                OR ("MA_TAI_KHOAN" LIKE N'154%%' AND
                "LOAI_HACH_TOAN" = '1' AND
                Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                (LOAI_GIA_THANH <> 'CONG_TRINH' OR
                (LOAI_GIA_THANH = 'CONG_TRINH' AND
                GL."MA_TAI_KHOAN_DOI_UNG"
                NOT LIKE '623%%')) AND
                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE
                '627%%')) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                THEN SUM("GHI_NO" - "GHI_CO")
                WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN -SUM("GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (
                (GL."MA_TAI_KHOAN" LIKE '621%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                (LOAI_GIA_THANH <> 'CONG_TRINH' OR
                (LOAI_GIA_THANH = 'CONG_TRINH' AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%')) AND
                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE
                '627%%')) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '622%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '622%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , (CASE WHEN
                LOAI_GIA_THANH = 'CONG_TRINH' AND (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '623%%')
                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH' AND (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
                (GL."MA_TAI_KHOAN" LIKE '623%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '627%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '627%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1')
                THEN SUM(GL."GHI_CO")
                ELSE 0
                END
                ) AS "KHOAN_GIAM_GIA_THANH"
                , "THUOC_DU_AN_ID"
                FROM TMP_LIST AS P INNER JOIN
                so_cai_chi_tiet AS GL ON GL."HOP_DONG_BAN_ID" = P."HOP_DONG_ID"
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                AND GL."HOP_DONG_BAN_ID" IS NOT NULL

                GROUP BY
                P."HOP_DONG_ID",
                GL."MA_TAI_KHOAN",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."MA_TAI_KHOAN_DOI_UNG",
                GL."LOAI_HACH_TOAN", "THUOC_DU_AN_ID"

                ;


                ELSE -- QD48--------------------------------------------------------

                INSERT INTO TMP_THU_THAP_CHI_PHI
                (
                "DOI_TUONG_ID",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "THUOC_DU_AN_ID"
                )
                SELECT
                JP."HOP_DONG_ID"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (-- Nếu có JCAJC"PHAT_SINH_TRONG_KY"DetailID=JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , (
                CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH' AND JCA."DEN_NGAY" < tu_ngay AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (
                CASE WHEN
                (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH'
                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , (
                CASE WHEN JCA."DEN_NGAY" < tu_ngay AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (
                CASE WHEN (JCA."DEN_NGAY" >= tu_ngay AND JCA."DEN_NGAY" <= den_ngay) AND
                (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM(JCA."SO_TIEN")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"
                , "THUOC_DU_AN_ID"

                FROM TMP_LIST AS JP
                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                LEFT JOIN (SELECT
                JCAD.*
                , J."TU_NGAY"
                , J."DEN_NGAY"
                , E."MA_PHAN_CAP"
                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = JCAD."KHOAN_MUC_CP_ID"
                WHERE J."DEN_NGAY" <=
                den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                ) JCA ON JCA."SO_HOP_DONG_ID" = JP."HOP_DONG_ID"
                WHERE JCA."KHOAN_MUC_CP_ID" IS NOT NULL
                GROUP BY
                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                JCA."DEN_NGAY",
                (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCA."TAI_KHOAN_ID"),
                JCA."MA_PHAN_CAP", JP."HOP_DONG_ID", "THUOC_DU_AN_ID"
                ;


                /*3 Lấy số liệu trên sổ		*/

                INSERT INTO TMP_THU_THAP_CHI_PHI
                (
                "DOI_TUONG_ID",
                "SO_DA_NGHIEM_THU",
                "OPN_SO_DA_NGHIEM_THU",
                "OPN_NGUYEN_VAT_LIEU",
                "NGUYEN_VAT_LIEU",
                "OPN_NHAN_CONG",
                "NHAN_CONG",
                "OPN_MAY_THI_CONG",
                "MAY_THI_CONG",
                "OPN_CHI_PHI_CHUNG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH",
                "THUOC_DU_AN_ID"
                )
                SELECT
                JP."HOP_DONG_ID"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" <= den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '632%%') AND
                (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX ||
                '%%')
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "SO_DA_NGHIEM_THU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '632%%') AND
                (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN SUM("GHI_NO")
                ELSE 0
                END
                ) AS "OPN_SO_DA_NGHIEM_THU"
                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                /*PS Có TK 154 chi tiết theo công trình không chi tiết theo các KMCP sản xuất (không kể PSDU Nợ 632/154) trên các chứng từ có ngày hạch toán < Từ ngày của kỳ tập hợp chi phí*/
                WHEN GL."NGAY_HACH_TOAN" < tu_ngay AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN -SUM("GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NGUYEN_VAT_LIEU"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NGUYEN_VAT_LIEU"
                , --NC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_NHAN_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "NHAN_CONG"
                , --MTC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH' AND
                (GL."MA_TAI_KHOAN" LIKE '154%%') AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_MAY_THI_CONG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND LOAI_GIA_THANH = 'CONG_TRINH' AND
                (GL."MA_TAI_KHOAN" LIKE '154%%') AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "MAY_THI_CONG"
                , -- CPC
                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "OPN_CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%')
                THEN SUM("GHI_NO" - "GHI_CO")
                ELSE 0
                END
                ) AS "CHI_PHI_CHUNG"
                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND (GL."MA_TAI_KHOAN" LIKE '154%%') AND
                ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%' AND GL."LOAI_HACH_TOAN" = '2') OR
                GL."LOAI_HACH_TOAN" = '1') AND
                (E."MA_PHAN_CAP" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%')
                THEN SUM(GL."GHI_CO")
                ELSE 0
                END
                ) AS "KHOAN_GIAM_GIA_THANH"
                , "THUOC_DU_AN_ID"

                FROM TMP_LIST JP INNER JOIN so_cai_chi_tiet AS GL ON GL."HOP_DONG_BAN_ID" = JP."HOP_DONG_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON GL."KHOAN_MUC_CP_ID" = E."id"
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                AND GL."HOP_DONG_BAN_ID" IS NOT NULL

                GROUP BY
                JP."HOP_DONG_ID",
                GL."CHI_NHANH_ID",
                GL."NGAY_HACH_TOAN",
                GL."MA_TAI_KHOAN",
                GL."MA_TAI_KHOAN_DOI_UNG",
                E."MA_PHAN_CAP",
                GL."LOAI_HACH_TOAN",
                "THUOC_DU_AN_ID"
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
                ORDER BY JP."SO_HOP_DONG" )  AS "RowNum"
                , -- Lũy kế chi phí
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                , 0) AS "LUY_KE_CHI_PHI"
                ,
                COALESCE(SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0)), 0)  AS "LUY_KE_DA_NGHIEM_THU"
                ,
                COALESCE(
                SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))

                - SUM(COALESCE(CC."OPN_SO_DA_NGHIEM_THU", 0))
                , 0) AS "SO_CHUA_NGHIEM_THU_DAU_KY"
                ,  COALESCE(
                SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                - SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0))
                , 0) AS "SO_CHUA_NGHIEM_THU_CUOI_KY"
                , -- Lũy kế kỳ trước
                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0)), 0)  AS "LK_KY_TRUOC_NVL_TRUC_TIEP"
                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG", 0)), 0) AS "LK_TRUOC_NC_TRUC_TIEP"
                ,  COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0)), 0) AS "LK_TRUOC_MAY_THI_CONG"
                ,  COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0)), 0) AS "LK_TRUOC_CHI_PHI_CHUNG"
                ,  COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                , 0) AS "LUY_KE_TRUOC_TONG"
                , -- Lũy kế phát sinh trong kỳ
                COALESCE(SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0)), 0) AS "LK_TRONG_NVL_TRUC_TIEP"
                ,  COALESCE(SUM(COALESCE(CC."NHAN_CONG", 0)), 0) AS "LK_TRONG_NC_TRUC_TIEP"
                ,  COALESCE(SUM(COALESCE(CC."MAY_THI_CONG", 0)), 0) AS "LK_TRONG_MAY_THI_CONG"
                ,  COALESCE(SUM(COALESCE(CC."CHI_PHI_CHUNG", 0)), 0) AS "LK_TRONG_CHI_PHI_CHUNG"
                ,  COALESCE(
                SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                , 0) AS "LK_TRONG_TONG"
                , -- Khoản giảm chi phí
                COALESCE(SUM(COALESCE("KHOAN_GIAM_GIA_THANH", 0)), 0)  AS "KHOAN_GIAM_GIA_THANH"
                , -- Lũy kế chi phí
                COALESCE(
                SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0)) + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0)) -
                SUM(COALESCE("KHOAN_GIAM_GIA_THANH", 0)), 0) AS "CP_NVL_TRUC_TIEP"
                ,
                COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG", 0)) + SUM(COALESCE(CC."NHAN_CONG", 0)) 
                , 0) AS "CP_NC_TRUC_TIEP"
                ,  COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                , 0) AS "CP_MAY_THI_CONG"
                ,
                COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0)) + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                , 0) AS "CP_CHI_PHI_CHUNG"
                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                + SUM(COALESCE(CC."NHAN_CONG", 0))
                + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                , 0)
                - COALESCE(SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                , 0) AS "CP_TONG"

                , C."id" AS "HOP_DONG_ID"
                , C."SO_HOP_DONG"
                , C."TRICH_YEU"

                , CAST(CASE WHEN PP."HOP_DONG_ID" IS NULL
                THEN 0
                ELSE 1 END AS BIT)          AS "IsBold"

                FROM TMP_TB AS JP
                LEFT JOIN TMP_THU_THAP_CHI_PHI CC
                ON (CC."DOI_TUONG_ID" = "HOP_DONG_ID" OR CC."THUOC_DU_AN_ID" = JP."HOP_DONG_ID")
                LEFT JOIN sale_ex_hop_dong_ban AS C ON C."id" = JP."HOP_DONG_ID"
                LEFT JOIN res_partner AS AO ON AO."id" = C."KHACH_HANG_ID"
                LEFT JOIN TMP_CHA PP ON PP."HOP_DONG_ID" = JP."HOP_DONG_ID"
                LEFT JOIN TMP_BAC GP ON GP."HOP_DONG_ID" = JP."HOP_DONG_ID"

                GROUP BY
                JP."HOP_DONG_ID",
                JP."SO_HOP_DONG",
                C."THUOC_DU_AN_ID",
                C."id",
                C."SO_HOP_DONG",
                C."TRICH_YEU",

                PP."HOP_DONG_ID"

                ;


                END $$
                ;
                SELECT 
                "SO_HOP_DONG" AS "SO_HOP_DONG",
                "TRICH_YEU" AS "TRICH_YEU",
                "LUY_KE_CHI_PHI" AS "LUY_KE_CHI_PHI",
                "LUY_KE_DA_NGHIEM_THU" AS "LUY_KE_DA_NGHIEM_THU",
                "SO_CHUA_NGHIEM_THU_DAU_KY" AS "SO_CHUA_NGHIEM_THU_DAU_KY",
                "SO_CHUA_NGHIEM_THU_CUOI_KY" AS "SO_CHUA_NGHIEM_THU_CUOI_KY",
                "LK_KY_TRUOC_NVL_TRUC_TIEP" AS "LK_KY_TRUOC_NVL_TRUC_TIEP",
                "LK_TRUOC_NC_TRUC_TIEP" AS "LK_TRUOC_NC_TRUC_TIEP",
                "LK_TRUOC_MAY_THI_CONG" AS "LK_TRUOC_MAY_THI_CONG",
                "LK_TRUOC_CHI_PHI_CHUNG" AS "LK_TRUOC_CHI_PHI_CHUNG",
                "LUY_KE_TRUOC_TONG" AS "LUY_KE_TRUOC_TONG",
                "LK_TRONG_NVL_TRUC_TIEP" AS "LK_TRONG_NVL_TRUC_TIEP",
                "LK_TRONG_NC_TRUC_TIEP" AS "LK_TRONG_NC_TRUC_TIEP",
                "LK_TRONG_MAY_THI_CONG" AS "LK_TRONG_MAY_THI_CONG",
                "LK_TRONG_CHI_PHI_CHUNG" AS "LK_TRONG_CHI_PHI_CHUNG",
                "LK_TRONG_TONG" AS "LK_TRONG_TONG",
                "KHOAN_GIAM_GIA_THANH" AS "KHOAN_GIAM_GIA_THANH",
                "CP_NVL_TRUC_TIEP" AS "CP_NVL_TRUC_TIEP",
                "CP_NC_TRUC_TIEP" AS "CP_NC_TRUC_TIEP",
                "CP_MAY_THI_CONG" AS "CP_MAY_THI_CONG",
                "CP_CHI_PHI_CHUNG" AS "CP_CHI_PHI_CHUNG",
                "CP_TONG" AS "CP_TONG"

                FROM TMP_KET_QUA
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
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_tong_hop_chi_phi_theo_doi_tuong_dtthcp').read()[0]
        elif THONG_KE_THEO=='CONG_TRINH':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_tong_hop_chi_phi_theo_doi_tuong_cong_trinh').read()[0]
        elif THONG_KE_THEO=='DON_HANG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_tong_hop_chi_phi_theo_doi_tuong_don_hang').read()[0]
        elif THONG_KE_THEO=='HOP_DONG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_bang_tong_hop_chi_phi_theo_doi_tuong_hop_dong').read()[0]

        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action