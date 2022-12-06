# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_CHI_TIET_CONG_NO_PHAI_THU_KHACH_HANG(models.Model):
    _name = 'bao.cao.chi.tiet.cong.no.phai.thu.khach.hang'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'), ('NHAN_VIEN', 'Nhân viên'), ('CONG_TRINH', 'Công trình'), ('HOP_DONG', 'Hợp đồng'), ('DON_DAT_HANG', 'Đơn đặt hàng'), ('DON_VI_KINH_DOANH', 'Đơn vị kinh doanh'), ('CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU', 'Chi tiết theo các khoản giảm trừ'), ], string='Thống kê theo', help='Thống kê theo',default='KHONG_CHON',required =True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True )
    currency_id = fields.Many2one('res.currency', string='Loại tiền ', help='Loại tiền ',required=True)
    TU_NGAY = fields.Date(string='Từ ngày ', help='Từ ngày ',required=True)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',required=True)
    NHOM_KHACH_HANG_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_CO_ID = fields.Char(string='TK công nợ', help='Tài khoản công nợ')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    NO_SO_PHAT_SINH = fields.Float(string='Nợ', help='Nợ số phát sinh',digits=decimal_precision.get_precision('VND'))
    CO_SO_PHAT_SINH = fields.Float(string='Có', help='Có số phát sinh',digits=decimal_precision.get_precision('VND'))
    NO_SO_DU = fields.Float(string='Nợ', help='Nợ số dư',digits=decimal_precision.get_precision('VND'))
    CO_SO_DU = fields.Float(string='Có', help='Có số dư',digits=decimal_precision.get_precision('VND'))
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    SO_PHAI_THU = fields.Float(string='Số phải thu', help='Số phải thu',digits= decimal_precision.get_precision('VND'))
    CHIET_KHAU = fields.Float(string='Chiết khẩu', help='Chiết khấu',digits= decimal_precision.get_precision('VND'))
    TRA_LAI_GIAM_GIA = fields.Float(string='Trả lại/giảm giá', help='Trả lại/giảm giá',digits= decimal_precision.get_precision('VND'))
    CK_THANH_TOAN_GIAM_TRU_KHAC = fields.Float(string='CK thanh toán/giảm trừ khác', help='Chuyển khoản thanh toán/giảm trừ khác',digits= decimal_precision.get_precision('VND'))
    SO_DA_THU = fields.Float(string='Số đã thu', help='Số đã thu',digits= decimal_precision.get_precision('VND'))
    SO_DU = fields.Float(string='Số dư', help='Số dư',digits= decimal_precision.get_precision('VND'))
    TAI_KHOAN_KH = fields.Char(string='Tài khoản', help='Tài khoản')
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau')
    HIEN_THI_HANG_KHUYEN_MAI_KHONG_THU_TIEN = fields.Boolean(string='Hiển thị hàng khuyến mãi không thu tiền')

    TEN_NHAN_VIEN  = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    HOP_DONG_DU_AN = fields.Char(string='Hợp đồng/dự án', help='Hợp đồng/dự án')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    TEN_DON_VI = fields.Char(string='Tên đơn vị', help='Tên đơn vị')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')



    chi_tiet = fields.Selection([
        ('theo_hop_dong', 'Theo hợp đồng'),
        ('theo_du_an', 'Theo dự án'),
        ], default='theo_hop_dong', store=False)
		
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN


    KHACH_HANG_IDS = fields.One2many('res.partner')
    KHACH_HANG_IDS_nhanvien = fields.One2many('res.partner')
    KHACH_HANG_IDS_congtrinh = fields.One2many('res.partner')
    KHACH_HANG_IDS_hopdong= fields.One2many('res.partner')
    KHACH_HANG_IDS_dondathang= fields.One2many('res.partner')
    KHACH_HANG_IDS_donvikinhdoanh= fields.One2many('res.partner')
    KHACH_HANG_IDS_theocackhoangiamtru= fields.One2many('res.partner')

    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)    
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner','chi_tiet_cong_no_phai_thu_kh_res_partner', domain=[('LA_KHACH_HANG', '=', True)], string='Chọn KH', help='Chọn khách hàng')
    MA_PC_NHOM_KH = fields.Char()


    NHAN_VIEN_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','chi_tiet_cong_no_phai_thu_kh_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')


    CHON_TAT_CA_DON_VI_KINH_DOANH = fields.Boolean('Tất cả đơn vị kinh doanh', default=True)
    DON_VI_KINH_DOANH_MANY_IDS = fields.Many2many('danh.muc.to.chuc','chi_tiet_cong_no_phai_thu_kh_dmtc', string='Chọn đơn vị kinh doanh')

    DON_VI_KINH_DOANH_IDS =  fields.One2many('danh.muc.to.chuc')

    CHON_TAT_CA_DON_DAT_HANG = fields.Boolean('Tất cả đơn đặt hàng', default=True)
    DON_DAT_HANG_MANY_IDS = fields.Many2many('account.ex.don.dat.hang', 'chi_tiet_cong_no_phai_thu_kh_ddh', string='Chọn đơn đặt hàng')
    DON_DAT_HANG_IDS = fields.One2many('account.ex.don.dat.hang')

    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','chi_tiet_cong_no_phai_thu_kh_ct', string='Chọn công trình')
    CONG_TRINH_IDS = fields.One2many('danh.muc.cong.trinh')

    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','chi_tiet_cong_no_phai_thu_kh_hd', string='Chọn hợp đồng')
    HOP_DONG_IDS = fields.One2many('sale.ex.hop.dong.ban')

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):
        
        self.NHOM_KHACH_HANG_ID = False
        self.CHON_TAT_CA_KHACH_HANG = True
        self.CHON_TAT_CA_NHAN_VIEN = True
        self.CHON_TAT_CA_DON_VI_KINH_DOANH = True
        self.CHON_TAT_CA_DON_DAT_HANG = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.CHON_TAT_CA_HOP_DONG = True

        self.HOP_DONG_MANY_IDS = []
        self.CONG_TRINH_MANY_IDS = []
        self.DON_DAT_HANG_MANY_IDS = []
        self.DON_VI_KINH_DOANH_MANY_IDS = []
        self.NHAN_VIEN_MANY_IDS = []
        self.KHACH_HANG_MANY_IDS = []

    # Khách hàng
    @api.onchange('KHACH_HANG_IDS','KHACH_HANG_IDS_nhanvien','KHACH_HANG_IDS_congtrinh','KHACH_HANG_IDS_hopdong','KHACH_HANG_IDS_dondathang','KHACH_HANG_IDS_donvikinhdoanh','KHACH_HANG_IDS_theocackhoangiamtru')
    def update_KHACH_HANG_IDS(self):
        if self.THONG_KE_THEO == 'KHONG_CHON':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_nhanvien.ids
        elif self.THONG_KE_THEO == 'CONG_TRINH':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_congtrinh.ids
        elif self.THONG_KE_THEO == 'HOP_DONG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_hopdong.ids
        elif self.THONG_KE_THEO == 'DON_DAT_HANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_dondathang.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_donvikinhdoanh.ids
        elif self.THONG_KE_THEO == 'CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_theocackhoangiamtru.ids
        
    @api.onchange('NHOM_KHACH_HANG_ID')
    def update_NHOM_KHACH_HANG_ID(self):
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KHACH_HANG_ID.MA_PHAN_CAP

    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        if self.THONG_KE_THEO == 'KHONG_CHON':
            self.KHACH_HANG_IDS = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN':
            self.KHACH_HANG_IDS_nhanvien = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'CONG_TRINH':
            self.KHACH_HANG_IDS_congtrinh = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'HOP_DONG':
            self.KHACH_HANG_IDS_hopdong = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'DON_DAT_HANG':
            self.KHACH_HANG_IDS_dondathang = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            self.KHACH_HANG_IDS_donvikinhdoanh = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU':
            self.KHACH_HANG_IDS_theocackhoangiamtru = self.KHACH_HANG_MANY_IDS.ids
    # end khách hàng
    
    # Nhân viên
    @api.onchange('NHAN_VIEN_IDS')
    def update_NHAN_VIEN_IDS(self):
        self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS.ids
      
        
    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        self.NHAN_VIEN_IDS = self.NHAN_VIEN_MANY_IDS.ids
       
    # end nhân viên

    # Đơn vị kinh doanh
    @api.onchange('DON_VI_KINH_DOANH_IDS')
    def update_DON_VI_KINH_DOANH_IDS(self):
        self.DON_VI_KINH_DOANH_MANY_IDS =self.DON_VI_KINH_DOANH_IDS.ids
        
        
    @api.onchange('DON_VI_KINH_DOANH_MANY_IDS')
    def _onchange_DON_VI_KINH_DOANH_MANY_IDS(self):
        self.DON_VI_KINH_DOANH_IDS = self.DON_VI_KINH_DOANH_MANY_IDS.ids
       
    # end Đơn vị kinh doanh
    
    # Đơn đặt hàng
    @api.onchange('DON_DAT_HANG_IDS')
    def update_DON_DAT_HANG_IDS(self):
        self.DON_DAT_HANG_MANY_IDS =self.DON_DAT_HANG_IDS.ids
        
        
    @api.onchange('DON_DAT_HANG_MANY_IDS')
    def _onchange_DON_DAT_HANG_MANY_IDS(self):
        self.DON_DAT_HANG_IDS = self.DON_DAT_HANG_MANY_IDS.ids
       
    # end Đơn đặt hàng

    # Công trình
    @api.onchange('CONG_TRINH_IDS')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.CONG_TRINH_IDS.ids
        
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.CONG_TRINH_IDS = self.CONG_TRINH_MANY_IDS.ids

    # end Công trình
    
    # Hợp đồng
    @api.onchange('HOP_DONG_IDS')
    def update_HOP_DONG_IDS(self):
        self.HOP_DONG_MANY_IDS =self.HOP_DONG_IDS.ids
        
        
    @api.onchange('HOP_DONG_MANY_IDS')
    def _onchange_HOP_DONG_MANY_IDS(self):
        self.HOP_DONG_IDS = self.HOP_DONG_MANY_IDS.ids
        
    # end Hợp đồng

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
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 1 if 'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' in params.keys() and params['CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU'] != 'False' else 0
        HIEN_THI_HANG_KHUYEN_MAI_KHONG_THU_TIEN = 1 if 'HIEN_THI_HANG_KHUYEN_MAI_KHONG_THU_TIEN' in params.keys() and params['HIEN_THI_HANG_KHUYEN_MAI_KHONG_THU_TIEN'] != 'False' else 0
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        if TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN


        currency_id = params['currency_id'] if 'currency_id' in params.keys() and params['currency_id'] != 'False' else None
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHOM_KHACH_HANG_ID = params['NHOM_KHACH_HANG_ID'] if 'NHOM_KHACH_HANG_ID' in params.keys() and params['NHOM_KHACH_HANG_ID'] != 'False' else None
        MA_PC_NHOM_KH = params.get('MA_PC_NHOM_KH')
        if params.get('CHON_TAT_CA_KHACH_HANG'):
            domain = [('LA_KHACH_HANG','=', True)]
            if MA_PC_NHOM_KH:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
            KHACH_HANG_IDS =  self.env['res.partner'].search(domain).ids
        else:
            KHACH_HANG_IDS = params.get('KHACH_HANG_MANY_IDS')

        if params.get('CHON_TAT_CA_NHAN_VIEN'):
            domain = [('LA_NHAN_VIEN','=', True)]
            NHAN_VIEN_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHAN_VIEN_IDS =  params.get('NHAN_VIEN_MANY_IDS')
        
        if params.get('CHON_TAT_CA_DON_VI_KINH_DOANH'):
            domain = []
            DON_VI_KINH_DOANH_IDS =  self.env['danh.muc.to.chuc'].search(domain).ids
        else:
            DON_VI_KINH_DOANH_IDS = params.get('DON_VI_KINH_DOANH_MANY_IDS')

        
        if params.get('CHON_TAT_CA_DON_DAT_HANG'):
            domain = []
            DON_DAT_HANG_IDS = self.env['account.ex.don.dat.hang'].search(domain).ids
        else:
            DON_DAT_HANG_IDS = params.get('DON_DAT_HANG_MANY_IDS')
        
        if params.get('CHON_TAT_CA_CONG_TRINH'):
            domain = []
            CONG_TRINH_IDS = self.env['danh.muc.cong.trinh'].search(domain).ids
        else:
            CONG_TRINH_IDS = params.get('CONG_TRINH_MANY_IDS')

        
        if params.get('CHON_TAT_CA_HOP_DONG'):
            domain = []
            HOP_DONG_IDS = self.env['sale.ex.hop.dong.ban'].search(domain).ids
        else:
            HOP_DONG_IDS = params.get('HOP_DONG_MANY_IDS')

        

        # so_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', TAI_KHOAN_ID)]).SO_TAI_KHOAN

        params_sql = {
               'TU_NGAY':TU_NGAY_F, 
               'DEN_NGAY':DEN_NGAY_F, 
               'KHACH_HANG_IDS' : KHACH_HANG_IDS or None,
               'NHAN_VIEN_IDS' : NHAN_VIEN_IDS or None,
               'CHI_NHANH_ID' : CHI_NHANH_ID,
               'DON_DAT_HANGIDS' : DON_DAT_HANG_IDS or None ,
               'DV_KINH_DOANH_IDS' : DON_VI_KINH_DOANH_IDS or None,
               'CONG_TRINHIDS' : CONG_TRINH_IDS or None,
               'HOP_DONGIDS' : HOP_DONG_IDS or None,
               'currency_id' : currency_id,
               'TAI_KHOAN_ID' : TAI_KHOAN_ID,
               'NHOM_KHACH_HANG_ID' : NHOM_KHACH_HANG_ID,
               'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' : CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU,
               'HIEN_THI_HANG_KHUYEN_MAI_KHONG_THU_TIEN' : HIEN_THI_HANG_KHUYEN_MAI_KHONG_THU_TIEN,
               'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
               'limit': limit,
               'offset': offset,
               }
        
        # Thống kê theo không chọn
        if THONG_KE_THEO=='KHONG_CHON' :
            return self._lay_bao_cao_thong_ke_theo_khong_chon(params_sql)
        # Thống kê theo nhân viên
        elif THONG_KE_THEO=='NHAN_VIEN' :
            return self._lay_bao_cao_thong_ke_theo_nhan_vien(params_sql)
        # Thống kê theo công trình
        elif THONG_KE_THEO=='CONG_TRINH' :
            return self._lay_bao_cao_thong_ke_theo_cong_trinh(params_sql)
        # Thống kê theo hợp đồng
        elif THONG_KE_THEO=='HOP_DONG' :
            return self._lay_bao_cao_thong_ke_theo_hop_dong(params_sql)
        # Thống kê theo đơn đặt hàng
        elif THONG_KE_THEO=='DON_DAT_HANG' :
            return self._lay_bao_cao_thong_ke_theo_don_dat_hang(params_sql)
        # Thống kê theo đơn vị kinh doanh
        elif THONG_KE_THEO=='DON_VI_KINH_DOANH' :
            return self._lay_bao_cao_thong_ke_theo_don_vi_kinh_doanh(params_sql)
        # Thống kê theo chi tiết theo các khoản giảm trừ
        elif THONG_KE_THEO=='CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU' :
            return self._lay_bao_cao_thong_ke_theo_chi_tiet_theo_cac_khoan_giam_tru(params_sql)

        
        # Execute SQL query here
    def _lay_bao_cao_thong_ke_theo_khong_chon(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(100) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    

   


    rec                                   RECORD;

    LOAI_TIEN_CHINH                       VARCHAR(100);

    CHE_DO_KE_TOAN                        VARCHAR(100);


    SO_TIEN_TON_NGUYEN_TE_TMP                 FLOAT:= 0;

    SO_TIEN_TON_TMP                           FLOAT:= 0;

    MA_KHACH_HANG_TMP                     VARCHAR(100):=N'';

    SO_TAI_KHOAN_TMP                      VARCHAR(100):=N'';




BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;


    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT
                "id" AS "KHACH_HANG_ID"
                , "MA_KHACH_HANG"
                , "HO_VA_TEN"
                , "DIA_CHI"
                , "LIST_MA_NHOM_KH_NCC"
                , -- Danh sách mã nhóm
                "LIST_TEN_NHOM_KH_NCC"
                , -- Danh sách tên nhóm

                "MA_SO_THUE"

            FROM res_partner AO
            WHERE (id = any (%(KHACH_HANG_IDS)s))
    ;

   


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT

                    A."id" AS "TK_ID"

                    , A."SO_TAI_KHOAN"
                    , A."TINH_CHAT"


                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" = so_tai_khoan
                      AND "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '1'


                ORDER BY
                    A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id" AS "TK_ID"
                    , A."SO_TAI_KHOAN"
                    , A."TINH_CHAT"

                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '1'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY
                    A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;


    END IF
    ;

    DROP TABLE IF EXISTS TMP_DANH_GIA_LAI_TK_NGOAI_TE
    ;

    CREATE TEMP TABLE TMP_DANH_GIA_LAI_TK_NGOAI_TE
        AS
            SELECT A.*
            FROM tong_hop_chung_tu_nghiep_vu_khac_so_du_ngoai_te A
                INNER JOIN DS_KHACH_HANG B ON A."DOI_TUONG_ID" = B."KHACH_HANG_ID"

                INNER JOIN TMP_TAI_KHOAN ACC ON A."MA_TAI_KHOAN" LIKE ACC."SO_TAI_KHOAN" || '%%'
    ;

    SELECT value
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA

    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq
    ;


    CREATE TABLE TMP_KET_QUA
    (
        RowNum             INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,

        "DOI_TUONG_ID"     INT

        ,
        "MA_KHACH_HANG"    VARCHAR(200)
        ,
        "TEN_KHACH_HANG"   VARCHAR(200)

        ,
        "NGAY_HACH_TOAN"   DATE

        ,
        "SO_CHUNG_TU"      VARCHAR(200)
        ,
        "LOAI_CHUNG_TU"    VARCHAR(200)
        , --Loại chứng từ
        "ID_CHUNG_TU"      INT
        ,
        "MODEL_CHUNG_TU"   VARCHAR(200)
        ,
        "DIEN_GIAI_CHUNG"  VARCHAR(200)
        , -- Diễn giải
        "SO_TAI_KHOAN"     VARCHAR(200)
        , -- Số tài khoản
        "TINH_CHAT"        VARCHAR(200)
        , -- Tính chất tài khoản
        "MA_TK_DOI_UNG"    VARCHAR(200)

        ,
        "GHI_NO_NGUYEN_TE" FLOAT
        ,
        "GHI_NO"           FLOAT
        , -- Diễn giải
        "GHI_CO_NGUYEN_TE" FLOAT
        , -- Số tài khoản
        "GHI_CO"           FLOAT
        , -- Tính chất tài khoản
        "DU_NO_NGUYEN_TE"  FLOAT

        ,
        "DU_NO"            FLOAT
        ,
        "DU_CO_NGUYEN_TE"  FLOAT
        , -- Diễn giải
        "DU_CO"            FLOAT
        , -- Số tài khoản
        "OrderType"        INT
        , -- Tính chất tài khoản
        "NGAY_CHUNG_TU"    DATE
        ,
        "NGAY_HOA_DON"     DATE
        ,
        "SO_HOA_DON"       VARCHAR(22)


    )
    ;

    IF v_cong_gop_but_toan_giong_nhau = 0 -- Nếu không cộng gộp
    THEN

        INSERT INTO TMP_KET_QUA

        (
            "DOI_TUONG_ID"

            ,
            "MA_KHACH_HANG"
            ,
            "TEN_KHACH_HANG"

            ,
            "NGAY_HACH_TOAN"

            ,
            "SO_CHUNG_TU"
            , "LOAI_CHUNG_TU"
            , --Loại chứng từ
            "ID_CHUNG_TU"
            ,
            "MODEL_CHUNG_TU"
            ,
            "DIEN_GIAI_CHUNG"
            , -- Diễn giải
            "SO_TAI_KHOAN"
            , -- Số tài khoản
            "TINH_CHAT"
            , -- Tính chất tài khoản
            "MA_TK_DOI_UNG"

            ,
            "GHI_NO_NGUYEN_TE"
            ,
            "GHI_NO"
            , -- Diễn giải
            "GHI_CO_NGUYEN_TE"
            , -- Số tài khoản
            "GHI_CO"
            , -- Tính chất tài khoản
            "DU_NO_NGUYEN_TE"

            , "DU_NO"

            ,"DU_CO_NGUYEN_TE"
             -- Diễn giải
            ,"DU_CO"
             -- Số tài khoản
            ,"OrderType"
             -- Tính chất tài khoản
            ,"NGAY_CHUNG_TU"

            ,"NGAY_HOA_DON"

            ,"SO_HOA_DON"
        )

            SELECT
                "DOI_TUONG_ID"
                , "MA_KHACH_HANG"
                , -- Mã NCC
                "HO_VA_TEN"
                , -- Tên NCC

                "NGAY_HACH_TOAN"


                , "SO_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , --Loại chứng từ
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , -- Diễn giải
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản
                "MA_TK_DOI_UNG"
                , --TK đối ứng

                  SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                  SUM("GHI_NO")           AS "GHI_NO"
                , -- Phát sinh nợ quy đổi
                  SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                  SUM("GHI_CO")           AS "GHI_CO"
                , -- Phát sinh có quy đổi
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN SUM("DU_NO_NGUYEN_TE"
                           )
                           - SUM("DU_CO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE")
                                   - SUM("DU_CO_NGUYEN_TE")) > 0
                       THEN (SUM("DU_NO_NGUYEN_TE")
                             - SUM("DU_CO_NGUYEN_TE"))
                        ELSE 0
                        END

                   END)                   AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN (SUM("DU_NO")
                            - SUM("DU_CO"))
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_NO")
                                   - SUM("DU_CO")) > 0
                       THEN SUM("DU_NO")
                            - SUM("DU_CO")
                        ELSE 0
                        END
                   END)                   AS "DU_NO"
                , --Dư Nợ Quy đổi
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN (SUM("DU_CO_NGUYEN_TE")
                            - SUM("DU_NO_NGUYEN_TE"))
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE")
                                   - SUM("DU_NO_NGUYEN_TE")) > 0
                       THEN (SUM("DU_CO_NGUYEN_TE")
                             - SUM("DU_NO_NGUYEN_TE"))
                        ELSE 0
                        END
                   END)                   AS "DU_CO_NGUYEN_TE"
                , --Dư Có
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN (SUM("DU_CO")
                            - SUM("DU_NO"))
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_CO")
                                   - SUM("DU_NO")) > 0
                       THEN (SUM("DU_CO")
                             - SUM("DU_NO"))
                        ELSE 0
                        END
                   END)                   AS "DU_CO" --Dư Có quy đổi
                , "OrderType"
                , "NGAY_CHUNG_TU"
                , "NGAY_HOA_DON"
                , "SO_HOA_DON"

            FROM (SELECT
                      AOL."DOI_TUONG_ID"
                      , LAOI."MA_KHACH_HANG"
                      , -- Mã NCC
                      LAOI."HO_VA_TEN"
                      , -- Tên NCC lấy trên danh mục

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."NGAY_HACH_TOAN"
                        END AS "NGAY_HACH_TOAN"
                      , -- Ngày hạch toán

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."SO_CHUNG_TU"
                        END AS "SO_CHUNG_TU"
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."ID_CHUNG_TU"
                        END AS "ID_CHUNG_TU"
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."MODEL_CHUNG_TU"
                        END AS "MODEL_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."LOAI_CHUNG_TU"
                        END AS "LOAI_CHUNG_TU"

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                        ELSE COALESCE(AOL."DIEN_GIAI",
                                      AOL."DIEN_GIAI_CHUNG")
                        END AS "DIEN_GIAI_CHUNG"
                      , -- Diễn giải (lấy diễn giải Detail, nếu null thì lấy diễn giải master)
                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."MA_TK_DOI_UNG"
                        END AS "MA_TK_DOI_UNG"
                      , --TK đối ứng
                      -- LVDIEP 17/10/2016: PBI 15608 - Sửa công thức cách lấy số liệu các báo cáo công nợ để đáp ứng theo từng chế độ QĐ48 thay TT133

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO_NGUYEN_TE"
                        END AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO"
                        END AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO_NGUYEN_TE"
                        END AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO"
                        END AS "GHI_CO"
                      , -- Phát sinh có quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0
                        END AS "DU_NO_NGUYEN_TE"
                      , --Dư Nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO"
                        ELSE 0
                        END AS "DU_NO"
                      , --Dư Nợ Quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0
                        END AS "DU_CO_NGUYEN_TE"
                      , --Dư Có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO"
                        ELSE 0
                        END AS "DU_CO"
                      --Dư Có quy đổi
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE 1
                        END AS "OrderType"
                      , -- Tên NCC lấy trên danh mục

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."NGAY_CHUNG_TU"
                        END AS "NGAY_CHUNG_TU"
                      , -- Tên NCC lấy trên danh mục

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."NGAY_HOA_DON"
                        END AS "NGAY_HOA_DON"
                      , -- Tên NCC lấy trên danh mục

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."SO_HOA_DON"
                        END AS "SO_HOA_DON"

                      , -- Tên NCC lấy trên danh mục

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                        END AS "THU_TU_TRONG_CHUNG_TU"
                      , -- Tên NCC lấy trên danh mục

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                        END AS "THU_TU_CHI_TIET_GHI_SO"

                  FROM so_cong_no_chi_tiet AS AOL
                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."SO_TAI_KHOAN"
                                                                        || '%%'
                      INNER JOIN DS_KHACH_HANG
                          AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id"
                      -- Danh mục ĐVT
                      LEFT JOIN danh_muc_don_vi_tinh AS MainUN ON AOL."DVT_CHINH_ID" = MainUN."id"
                      -- Danh mục ĐVT
                      --LEFT JOIN dbo.CustomFieldLedger AS CFL ON AOL.RefDetailID = CFL.RefDetailID

                      LEFT JOIN danh_muc_ma_thong_ke AS LI ON AOL."MA_THONG_KE_ID" = LI."id"
                      LEFT JOIN danh_muc_reftype AS SRT ON AOL."LOAI_CHUNG_TU" = SRT."id"
                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                 ) AS RSNS
            GROUP BY
                RSNS."DOI_TUONG_ID",
                RSNS."MA_KHACH_HANG", -- Mã NCC
                RSNS."HO_VA_TEN", -- Tên NCC

                RSNS."NGAY_HACH_TOAN", -- Ngày hạch toán

                RSNS."SO_CHUNG_TU", -- Số chứng từ

                RSNS."LOAI_CHUNG_TU", --Loại chứng từ
                RSNS."ID_CHUNG_TU", -- Mã chứng từ
                RSNS."MODEL_CHUNG_TU",
                RSNS."DIEN_GIAI_CHUNG", -- Diễn giải
                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT", -- Tính chất tài khoản
                RSNS."MA_TK_DOI_UNG", --TK đối ứng
                RSNS."OrderType",
                RSNS."NGAY_CHUNG_TU", -- Tính chất tài khoản
                RSNS."NGAY_HOA_DON", --TK đối ứng
                RSNS."SO_HOA_DON",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"


            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                   OR SUM("GHI_NO") <> 0
                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                   OR SUM("GHI_CO") <> 0
                   OR SUM("DU_NO_NGUYEN_TE"
                          - "DU_CO_NGUYEN_TE") <> 0
                   OR SUM("DU_NO"
                          - "DU_CO") <> 0
            ORDER BY
                RSNS."MA_KHACH_HANG",
                RSNS."SO_TAI_KHOAN",
                RSNS."OrderType",
                RSNS."NGAY_HACH_TOAN",
                RSNS."NGAY_CHUNG_TU",

                RSNS."SO_CHUNG_TU",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"

        ;

    ELSE -- Cộng gộp các bút toán giống nhau

        INSERT INTO TMP_KET_QUA

        (
            "DOI_TUONG_ID"

            ,
            "MA_KHACH_HANG"
            ,
            "TEN_KHACH_HANG"

            ,
            "NGAY_HACH_TOAN"

            ,
            "SO_CHUNG_TU"
            , "LOAI_CHUNG_TU"
            , --Loại chứng từ
            "ID_CHUNG_TU"
            ,
            "MODEL_CHUNG_TU"
            ,
            "DIEN_GIAI_CHUNG"
            , -- Diễn giải
            "SO_TAI_KHOAN"
            , -- Số tài khoản
            "TINH_CHAT"
            , -- Tính chất tài khoản
            "MA_TK_DOI_UNG"

            ,
            "GHI_NO_NGUYEN_TE"
            ,
            "GHI_NO"
            , -- Diễn giải
            "GHI_CO_NGUYEN_TE"
            , -- Số tài khoản
            "GHI_CO"
            , -- Tính chất tài khoản
            "DU_NO_NGUYEN_TE"

            , "DU_NO"
            ,
            "DU_CO_NGUYEN_TE"
            , -- Diễn giải
            "DU_CO"
            , -- Số tài khoản
            "OrderType"
            , -- Tính chất tài khoản
            "NGAY_CHUNG_TU"
            ,
            "NGAY_HOA_DON"
            ,
            "SO_HOA_DON"
        )

            SELECT
                "DOI_TUONG_ID"
                , "MA_KHACH_HANG"
                , -- Mã NCC
                "HO_VA_TEN"
                , -- Tên NCC

                "NGAY_HACH_TOAN"


                , "SO_CHUNG_TU"
                ,"LOAI_CHUNG_TU"
                , --Loại chứng từ
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , -- Diễn giải
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản
                "MA_TK_DOI_UNG"
                , --TK đối ứng

                  SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                  SUM("GHI_NO")           AS "GHI_NO"
                , -- Phát sinh nợ quy đổi
                  SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                  SUM("GHI_CO")           AS "GHI_CO"
                , -- Phát sinh có quy đổi
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN ("DU_NO_NGUYEN_TE"
                            - "DU_CO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN ("DU_NO_NGUYEN_TE"
                                   - "DU_CO_NGUYEN_TE") > 0
                       THEN "DU_NO_NGUYEN_TE"
                            - "DU_CO_NGUYEN_TE"
                        ELSE 0
                        END
                   END)                   AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN ("DU_NO"
                            - "DU_CO")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN ("DU_NO"
                                   - "DU_CO") > 0
                       THEN "DU_NO"
                            - "DU_CO"
                        ELSE 0
                        END
                   END)                   AS "DU_NO"
                , --Dư Nợ Quy đổi
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN ("DU_CO_NGUYEN_TE"
                            - "DU_NO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN ("DU_CO_NGUYEN_TE"
                                   - "DU_NO_NGUYEN_TE") > 0
                       THEN ("DU_CO_NGUYEN_TE"
                             - "DU_NO_NGUYEN_TE")
                        ELSE 0
                        END
                   END)                   AS "DU_CO_NGUYEN_TE"
                , --Dư Có
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN ("DU_CO"
                            - "DU_NO")
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN ("DU_CO"
                                   - "DU_NO") > 0
                       THEN ("DU_CO"
                             - "DU_NO")
                        ELSE 0
                        END
                   END)                   AS "DU_CO"

                , "OrderType"
                , "NGAY_CHUNG_TU"
                , "NGAY_HOA_DON"
                , "SO_HOA_DON"
            FROM (SELECT
                      AD."DOI_TUONG_ID"
                      , AD."MA_KHACH_HANG"
                      , -- Mã NCC
                      AD."HO_VA_TEN"
                      , -- Tên NCC lấy trên danh mục

                      AD."NGAY_HACH_TOAN"
                      , AD."SO_CHUNG_TU"
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn

                      AD."ID_CHUNG_TU"
                      , AD."MODEL_CHUNG_TU"

                      , AD."LOAI_CHUNG_TU"


                      , AD."DIEN_GIAI_CHUNG"
                      , -- Diễn giải (lấy diễn giải Master)
                      AD."SO_TAI_KHOAN"
                      , -- TK công nợ
                      AD."TINH_CHAT"
                      , -- Tính chất tài khoản
                      AD."MA_TK_DOI_UNG"
                      , --TK đối ứng

                      SUM(AD."GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                      SUM(AD."GHI_NO")           AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                      SUM(AD."GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                      SUM(AD."GHI_CO")           AS "GHI_CO"
                      , -- Phát sinh có quy đổi
                      SUM(AD."DU_NO_NGUYEN_TE")  AS "DU_NO_NGUYEN_TE"
                      , --Dư Nợ
                      SUM(AD."DU_NO")            AS "DU_NO"
                      , --Dư Nợ Quy đổi
                      SUM(AD."DU_CO_NGUYEN_TE")  AS "DU_CO_NGUYEN_TE"
                      , --Dư Có
                      SUM(AD."DU_CO")            AS "DU_CO" --Dư Có quy đổi
                      , AD."OrderType"
                      , AD."NGAY_CHUNG_TU"
                      , AD."NGAY_HOA_DON"

                      , AD."SO_HOA_DON"
                      , AD."THU_TU_CHI_TIET_GHI_SO"


                  FROM (SELECT
                            AOL."DOI_TUONG_ID"
                            , LAOI."MA_KHACH_HANG"
                            , -- Mã NCC
                            LAOI."HO_VA_TEN"
                            , -- Tên NCC lấy trên danh mục

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."NGAY_HACH_TOAN"
                              END AS "NGAY_HACH_TOAN"
                            , -- Ngày hạch toán

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."SO_CHUNG_TU"
                              END AS "SO_CHUNG_TU"
                            , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."ID_CHUNG_TU"
                              END AS "ID_CHUNG_TU"
                            , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."MODEL_CHUNG_TU"
                              END AS "MODEL_CHUNG_TU"
                            , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                              ELSE AOL."LOAI_CHUNG_TU"
                              END AS "LOAI_CHUNG_TU"
                            , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN N'Số dư đầu kỳ'

                              ELSE CASE WHEN AOL."MA_TK_DOI_UNG" LIKE N'133%%' OR
                                             AOL."MA_TK_DOI_UNG" LIKE N'3331%%'
                                  THEN N'Thuế GTGT của hàng hóa, dịch vụ'
                                   ELSE AOL."DIEN_GIAI_CHUNG" END
                              --ELSE AOL."DIEN_GIAI_CHUNG"
                              END AS "DIEN_GIAI_CHUNG"
                            , -- Diễn giải (lấy diễn giải Master)
                            TBAN."SO_TAI_KHOAN"
                            , -- TK công nợ
                            TBAN."TINH_CHAT"
                            , -- Tính chất tài khoản
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."MA_TK_DOI_UNG"
                              END AS "MA_TK_DOI_UNG"
                            , --TK đối ứng

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN 0
                              ELSE AOL."GHI_NO_NGUYEN_TE"
                              END AS "GHI_NO_NGUYEN_TE"
                            , -- Phát sinh nợ
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN 0
                              ELSE AOL."GHI_NO"
                              END AS "GHI_NO"
                            , -- Phát sinh nợ quy đổi
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN 0
                              ELSE AOL."GHI_CO_NGUYEN_TE"
                              END AS "GHI_CO_NGUYEN_TE"
                            , -- Phát sinh có
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN 0
                              ELSE AOL."GHI_CO"
                              END AS "GHI_CO"
                            , -- Phát sinh có quy đổi
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN AOL."GHI_NO_NGUYEN_TE"
                              ELSE 0
                              END AS "DU_NO_NGUYEN_TE"
                            , --Dư Nợ
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN AOL."GHI_NO"
                              ELSE 0
                              END AS "DU_NO"
                            , --Dư Nợ Quy đổi
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN AOL."GHI_CO_NGUYEN_TE"
                              ELSE 0
                              END AS "DU_CO_NGUYEN_TE"
                            , --Dư Có
                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN AOL."GHI_CO"
                              ELSE 0
                              END AS "DU_CO"
                            --Dư Có quy đổi
                            , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN 0
                              ELSE 1
                              END AS "OrderType"
                            , -- Tên NCC lấy trên danh mục

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."NGAY_CHUNG_TU"
                              END AS "NGAY_CHUNG_TU"
                            , -- Tên NCC lấy trên danh mục

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."NGAY_HOA_DON"
                              END AS "NGAY_HOA_DON"
                            , -- Tên NCC lấy trên danh mục

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."SO_HOA_DON"
                              END AS "SO_HOA_DON"


                            , -- Tên NCC lấy trên danh mục

                              CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                  THEN NULL
                              ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                              END AS "THU_TU_CHI_TIET_GHI_SO"
                        FROM so_cong_no_chi_tiet
                            AS AOL
                            INNER JOIN DS_KHACH_HANG
                                AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                            INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."SO_TAI_KHOAN"
                                                                              || '%%'
                            INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                            LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id"
                            -- Danh mục ĐVT

                            /*NBHIEU 19/12/2016 (CR 20082): Lấy thêm mã thống kê, và tên loại chứng từ*/
                            LEFT JOIN danh_muc_reftype
                                AS SRT ON AOL."LOAI_CHUNG_TU" = SRT."id"
                        WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                              AND (v_loai_tien_id IS NULL
                                   OR AOL."currency_id" = v_loai_tien_id
                              )
                       ) AS AD
                  GROUP BY
                      AD."DOI_TUONG_ID",
                      AD."MA_KHACH_HANG", -- Mã NCC
                      AD."HO_VA_TEN", -- Tên NCC lấy trên danh mục

                      AD."NGAY_HACH_TOAN",

                      AD."SO_CHUNG_TU",

                      AD."ID_CHUNG_TU",
                      AD."MODEL_CHUNG_TU",
                      AD."LOAI_CHUNG_TU",
                      AD."DIEN_GIAI_CHUNG",
                      AD."SO_TAI_KHOAN", -- TK công nợ
                      AD."TINH_CHAT", -- Tính chất tài khoản
                      AD."MA_TK_DOI_UNG", --TK đối ứng
                      AD."OrderType",
                      AD."NGAY_CHUNG_TU", -- Tính chất tài khoản
                      AD."NGAY_HOA_DON", --TK đối ứng
                      AD."SO_HOA_DON",

                      AD."THU_TU_CHI_TIET_GHI_SO"

                 ) AS RSS
            WHERE
                RSS."GHI_NO_NGUYEN_TE" <> 0
                OR RSS."GHI_CO_NGUYEN_TE" <> 0
                OR RSS."GHI_NO" <> 0
                OR RSS."GHI_CO" <> 0
                OR "DU_CO_NGUYEN_TE"
                   - "DU_NO_NGUYEN_TE" <> 0
                OR "DU_CO" - "DU_NO" <> 0


                            GROUP BY
                                RSS."DOI_TUONG_ID",
                                RSS."MA_KHACH_HANG", -- Mã NCC
                                RSS."HO_VA_TEN", -- Tên NCC

                                RSS."NGAY_HACH_TOAN", -- Ngày hạch toán

                                RSS."SO_CHUNG_TU", -- Số chứng từ

                                RSS."LOAI_CHUNG_TU", --Loại chứng từ
                                RSS."ID_CHUNG_TU", -- Mã chứng từ
                                RSS."MODEL_CHUNG_TU",
                                RSS."DIEN_GIAI_CHUNG", -- Diễn giải
                                RSS."SO_TAI_KHOAN", -- Số tài khoản
                                RSS."TINH_CHAT", -- Tính chất tài khoản
                                RSS."MA_TK_DOI_UNG", --TK đối ứng

                                RSS."DU_NO_NGUYEN_TE",
                                RSS."DU_NO", -- Diễn giải
                                RSS."DU_CO_NGUYEN_TE", -- Số tài khoản
                                RSS."DU_CO", -- Tính chất tài khoản
                                RSS."MA_TK_DOI_UNG", --TK đối ứng
                                RSS."OrderType",
                                 RSS."NGAY_CHUNG_TU",

                                RSS."SO_CHUNG_TU",
                                RSS."NGAY_HOA_DON",
                                RSS."SO_HOA_DON",
                                RSS."THU_TU_CHI_TIET_GHI_SO"

            ORDER BY
                RSS."MA_KHACH_HANG",
                RSS."SO_TAI_KHOAN",
                RSS."OrderType",
                RSS."NGAY_HACH_TOAN",
                RSS."NGAY_CHUNG_TU",

                RSS."SO_CHUNG_TU",
                RSS."NGAY_HOA_DON",
                RSS."SO_HOA_DON",
                RSS."THU_TU_CHI_TIET_GHI_SO"

        ;

    END IF
    ;


     FOR rec IN
        SELECT *
        FROM TMP_KET_QUA
             WHERE  "OrderType" <> 2

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
                             MA_KHACH_HANG_TMP <> rec."MA_KHACH_HANG"
                            OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"

                        THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                    ELSE SO_TIEN_TON_NGUYEN_TE_TMP + rec."GHI_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                         - rec."GHI_NO_NGUYEN_TE" --GHI_NO_NGUYEN_TE
                    END)
            INTO SO_TIEN_TON_NGUYEN_TE_TMP

        ;
            rec."DU_NO_NGUYEN_TE" = ( CASE WHEN  rec."TINH_CHAT" = '0'--DU_NO_NGUYEN_TE
                                              THEN -1 * SO_TIEN_TON_NGUYEN_TE_TMP
                                              WHEN  rec."TINH_CHAT" = '1'
                                              THEN 0
                                              ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
                                                        THEN -1
                                                             * SO_TIEN_TON_NGUYEN_TE_TMP
                                                        ELSE 0
                                                   END
                                         END );
                UPDATE TMP_KET_QUA
                SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
                  WHERE RowNum =rec.RowNum
            ;

              rec."DU_CO_NGUYEN_TE" = ( CASE WHEN  rec."TINH_CHAT" = '1'--DU_CO_NGUYEN_TE
                                               THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                               WHEN  rec."TINH_CHAT" = '0'
                                               THEN 0
                                               ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
                                                         THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                                         ELSE 0
                                                    END
                                          END );
             UPDATE TMP_KET_QUA
                SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
                  WHERE RowNum =rec.RowNum
            ;

              SELECT (CASE WHEN rec."OrderType" = 0
                THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                    THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                      ELSE -1
                           * rec."DU_NO" --DU_NO_NGUYEN_TE
                      END)
                    WHEN
                             MA_KHACH_HANG_TMP <> rec."MA_KHACH_HANG"
                            OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                        THEN rec."GHI_CO" - rec."GHI_NO" --PHAT_SINH_CO_NGUYEN_TE
                    ELSE SO_TIEN_TON_TMP + rec."GHI_CO"--PHAT_SINH_CO_NGUYEN_TE
                         - rec."GHI_NO" --GHI_NO_NGUYEN_TE
                    END)
            INTO SO_TIEN_TON_TMP
        ;

                     rec."DU_NO" = ( CASE WHEN  rec."TINH_CHAT" = '0'--DU_NO_NGUYEN_TE
                                              THEN -1 * SO_TIEN_TON_TMP
                                              WHEN  rec."TINH_CHAT" = '1'
                                              THEN 0
                                              ELSE CASE WHEN SO_TIEN_TON_TMP < 0
                                                        THEN -1
                                                             * SO_TIEN_TON_TMP
                                                        ELSE 0
                                                   END
                                         END );

                UPDATE TMP_KET_QUA
                SET "DU_NO" = rec."DU_NO"
                WHERE RowNum =rec.RowNum
            ;


                     rec."DU_CO" = ( CASE WHEN  rec."TINH_CHAT" = '1'--DU_CO_NGUYEN_TE
                                               THEN SO_TIEN_TON_TMP
                                               WHEN  rec."TINH_CHAT" = '0'
                                               THEN 0
                                               ELSE CASE WHEN SO_TIEN_TON_TMP > 0
                                                         THEN SO_TIEN_TON_TMP
                                                         ELSE 0
                                                    END
                                          END );

                UPDATE TMP_KET_QUA
                SET "DU_CO" = rec."DU_CO"
                WHERE RowNum =rec.RowNum
            ;


           MA_KHACH_HANG_TMP = rec."MA_KHACH_HANG" ;
            SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN" ;


        END LOOP
        ;


END $$
;

SELECT 
    "TEN_KHACH_HANG" as "TEN_KHACH_HANG",
    "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
    "NGAY_HACH_TOAN" as "NGAY_CHUNG_TU",
    "SO_CHUNG_TU" as "SO_CHUNG_TU",
    "DIEN_GIAI_CHUNG" as "DIEN_GIAI",
    "SO_TAI_KHOAN" as "TK_CO_ID",
    "MA_TK_DOI_UNG" as "TK_DOI_UNG",
    "GHI_NO" as "NO_SO_PHAT_SINH",
    "GHI_CO" as "CO_SO_PHAT_SINH",
    "DU_NO" as "NO_SO_DU",
    "DU_CO" as "CO_SO_DU",

    "ID_CHUNG_TU" as "ID_GOC",
    "MODEL_CHUNG_TU" as "MODEL_GOC"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s
;
        """
        return self.execute(query,params_sql)

    def _lay_bao_cao_thong_ke_theo_nhan_vien(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_CHI_TIET_CONG_NO_PHAI_THU_KHACH_HANG
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;


    v_loai_tien_id                        INTEGER := %(currency_id)s;



    rec                                   RECORD;

    rec_2                                 RECORD;

    LOAI_TIEN_CHINH                       VARCHAR(100);

    CHE_DO_KE_TOAN                        VARCHAR(100);


    SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT:=0;

    SO_TIEN_TON_TMP                       FLOAT:=0;


    KHACH_HANG_ID_TMP                     INTEGER;

    NHAN_VIEN_ID_TMP                      INTEGER;


    OPNJournalMemo                        VARCHAR(100) = N'Số dư đầu kỳ';

    LedgerID                              INTEGER;

    CrossAmountOC                         FLOAT;

    CrossAmount                           FLOAT;

    OldRemainAmountOC                     FLOAT;

    OldRemainAmount                       FLOAT;

    RemainAmountOC                        FLOAT;

    RemainAmount                          FLOAT;


BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;

            IF (%(KHACH_HANG_IDS)s) IS NULL
            THEN
                CREATE TEMP TABLE DS_KHACH_HANG
                    AS
                        SELECT
                              "id"                  AS "KHACH_HANG_ID"
                            ,"MA_KHACH_HANG"
                           ,"HO_VA_TEN"
                           ,"DIA_CHI"
                            , "LIST_MA_NHOM_KH_NCC"
                            , "LIST_TEN_NHOM_KH_NCC"

                        FROM res_partner
                        WHERE "LA_KHACH_HANG" = '1'
                ;
            ELSE
    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT
                  "id"        AS "KHACH_HANG_ID"
                , "MA_KHACH_HANG"
                , "HO_VA_TEN" AS "TEN_KHACH_HANG"
                , "DIA_CHI"
                , "LIST_MA_NHOM_KH_NCC"
                , "LIST_TEN_NHOM_KH_NCC"


            FROM res_partner
            WHERE (id = any (%(KHACH_HANG_IDS)s)) 
    ;

            END IF
            ;

    DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT
                  AO.id          AS "NHAN_VIEN_ID"
                , AO."MA_NHAN_VIEN"
                , AO."HO_VA_TEN" AS "TEN_NHAN_VIEN"

            FROM res_partner AS AO

            WHERE (id = any (%(NHAN_VIEN_IDS)s))  

    ;


    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;


        DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id"
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"

                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" LIKE so_tai_khoan || '%%'

                ORDER BY
                    A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id"
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"

                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '1'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY
                    A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    END IF
    ;

    DROP TABLE IF EXISTS TMP_KHUYEN_MAI
    ;

    CREATE TEMP TABLE TMP_KHUYEN_MAI
        AS
            SELECT
                  SAD."id"             AS "CHUNG_TU_BAN_HANG_CHI_TIET_ID"
                , 'sale.document.line' AS "MODEL_CHUNG_TU_CHI_TIET"
                , "LA_HANG_KHUYEN_MAI"
            FROM sale_document_line SAD
                INNER JOIN sale_document SA ON SA."id" = SAD."SALE_DOCUMENT_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = SA."CHI_NHANH_ID"
            WHERE "LA_HANG_KHUYEN_MAI" = '1'
                  AND SA."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

            UNION ALL

            SELECT
                  SAD."id"                            AS "CHUNG_TU_BAN_HANG_CHI_TIET_ID"
                , 'sale.ex.tra.lai.hang.ban.chi.tiet' AS "MODEL_CHUNG_TU_CHI_TIET"
                , "LA_HANG_KHUYEN_MAI"
            FROM sale_ex_tra_lai_hang_ban_chi_tiet SAD
                INNER JOIN sale_ex_tra_lai_hang_ban SA ON SA."id" = SAD."TRA_LAI_HANG_BAN_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = SA."CHI_NHANH_ID"
            WHERE "LA_HANG_KHUYEN_MAI" = '1'
                  AND SA."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

    ;


    DROP TABLE IF EXISTS TMP_CONG_NO_DOI_TRU
    ;

    CREATE TEMP TABLE TMP_CONG_NO_DOI_TRU
        AS
            SELECT
                DISTINCT
                G."ID_CHUNG_TU"
                , G."DOI_TUONG_ID"
                , G."TAI_KHOAN_ID"
                , G."currency_id"
                , G."NHAN_VIEN_ID"

            FROM sale_ex_doi_tru_chi_tiet G
                INNER JOIN res_partner AO ON AO.id = G."DOI_TUONG_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = G."MA_TAI_KHOAN"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
            /*Không lấy số dư đầu kỳ. Với số dư đầu kỳ lấy theo đúng thông tin trên tab chi tiết*/
            WHERE G."LOAI_CHUNG_TU_CONG_NO" NOT IN ('612', '613', '614')

    ;

    DROP TABLE IF EXISTS TMP_SO_CONG_NO_CHI_TIET
    ;

    CREATE TEMP TABLE TMP_SO_CONG_NO_CHI_TIET
        AS
            SELECT

                AL.id
                , AL."DOI_TUONG_ID"
                , AL."CHI_NHANH_ID"
                , AL."ID_CHUNG_TU"
                , AL."MODEL_CHUNG_TU"
                , AL."CHI_TIET_ID"
                , AL."CHI_TIET_MODEL"
                , AL."NGAY_HACH_TOAN"
                , AL."TK_ID"
                , AL."currency_id"
                , AL."GHI_NO_NGUYEN_TE"
                , AL."GHI_NO"
                , AL."GHI_CO_NGUYEN_TE"
                , AL."GHI_CO"
                , AL."NHAN_VIEN_ID"
                , AL."MA_TK"

            FROM so_cong_no_chi_tiet AL
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
                INNER JOIN res_partner AO ON AO.id = AL."DOI_TUONG_ID"
                INNER JOIN TMP_TAI_KHOAN AN ON AN."SO_TAI_KHOAN" = AL."MA_TK"
            WHERE "NGAY_HACH_TOAN" <= v_den_ngay

    ;


    DROP TABLE IF EXISTS TMP_CHUNG_TU_THANH_TOAN
    ;

    CREATE TEMP TABLE TMP_CHUNG_TU_THANH_TOAN
        AS
            SELECT
                  G."ID_CHUNG_TU_THANH_TOAN"                   AS "ID_CHUNG_TU"
                , G."MODEL_CHUNG_TU_THANH_TOAN"                AS "MODEL_CHUNG_TU"
                , G."DOI_TUONG_ID"
                , G."MA_TAI_KHOAN"
                , G."currency_id"
                , G."NHAN_VIEN_ID"
                , SUM(G."SO_TIEN_THANH_TOAN")                  AS "SO_TIEN_THANH_TOAN"

                , SUM(CASE
                      WHEN G."LOAI_DOI_TRU" = '0'
                          THEN
                              G."SO_TIEN_THANH_TOAN_QUY_DOI" - G."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI"
                      ELSE G."SO_TIEN_THANH_TOAN_QUY_DOI" END) AS "SO_TIEN_THANH_TOAN_QUY_DOI"

                , G."NGAY_HACH_TOAN_CONG_NO"
                , G."SO_CHUNG_TU_CONG_NO"
                , G."SO_HOA_DON_CONG_NO"
                , NULL                                         AS "ID_CHUNG_TU_CONG_NO"
                , NULL                                         AS "MODEL_CHUNG_TU_CONG_NO"
            FROM sale_ex_doi_tru_chi_tiet G
                INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = G."DOI_TUONG_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = G."MA_TAI_KHOAN"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
            GROUP BY
                G."ID_CHUNG_TU_THANH_TOAN"
                , G."MODEL_CHUNG_TU_THANH_TOAN"
                , G."DOI_TUONG_ID"
                , G."MA_TAI_KHOAN"
                , G."currency_id"
                , G."SO_CHUNG_TU_CONG_NO"
                , G."NGAY_HACH_TOAN_CONG_NO"
                , G."NHAN_VIEN_ID"
                , G."SO_HOA_DON_CONG_NO"


            UNION ALL
            /*Lấy hàng bán trả lại*/
            SELECT
                SARD."TRA_LAI_HANG_BAN_ID"
                , 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                , SUM(AL."GHI_CO_NGUYEN_TE") AS "SO_TIEN_THANH_TOAN"
                , SUM(AL."GHI_CO")           AS "SO_TIEN_THANH_TOAN_QUY_DOI"

                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"
                , 'sale.document'            AS "MODEL_CHUNG_TU_CHI_TIET"
            FROM sale_ex_tra_lai_hang_ban_chi_tiet SARD
                INNER JOIN so_cong_no_chi_tiet AL
                    ON (SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet')
                INNER JOIN sale_document SAV ON SAV."id" = SARD."SO_CHUNG_TU_ID"
                INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = AL."DOI_TUONG_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = AL."MA_TK"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
            WHERE SARD."SO_CHUNG_TU_ID" IS NOT NULL
            GROUP BY
                SARD."TRA_LAI_HANG_BAN_ID"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                --, SAV."id"
                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"


            UNION ALL
            /*Lấy hàng bán giảm giá*/
            SELECT
                SARD."GIAM_GIA_HANG_BAN_ID"
                , 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                , SUM(AL."GHI_CO_NGUYEN_TE")  AS "SO_TIEN_THANH_TOAN"
                , SUM(AL."GHI_CO")            AS "SO_TIEN_THANH_TOAN_QUY_DOI"
                --, SAV."id"
                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"
                , 'sale.document'             AS "MODEL_CHUNG_TU_CHI_TIET"
            FROM sale_ex_chi_tiet_giam_gia_hang_ban SARD
                INNER JOIN so_cong_no_chi_tiet AL
                    ON (SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL" = 'sale.ex.chi.tiet.giam.gia.hang.ban')
                INNER JOIN sale_document SAV ON SAV."id" = SARD."CHUNG_TU_BAN_HANG_ID"
                INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = AL."DOI_TUONG_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = AL."MA_TK"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
            WHERE SARD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
            GROUP BY
                SARD."GIAM_GIA_HANG_BAN_ID"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"

                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA

    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq
    ;


    CREATE TABLE TMP_KET_QUA
    (
        RowNum                   INT     DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,
        "NHAN_VIEN_ID"           INT
        ,
        "DOI_TUONG_ID"           INT
        ,
        "MA_KHACH_HANG"          VARCHAR(255)
        ,
        "TEN_KHACH_HANG"         VARCHAR(255)

        ,
        "ID_CHUNG_TU"            INT
        ,
        "MODEL_CHUNG_TU"         VARCHAR(255)
        ,
        "LOAI_CHUNG_TU"          INT
        ,
        "NGAY_HACH_TOAN"         DATE
        ,
        "NGAY_CHUNG_TU"          DATE
        ,
        "SO_CHUNG_TU"            VARCHAR(22)

        ,
        "DIEN_GIAI_CHUNG"        VARCHAR(255)
        ,
        "MA_TK"                   VARCHAR(200)

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
        ,
        "GLJournalMemo"          VARCHAR(255)

        ,
        "OrderType"              INT
        ,
        "LedgerID"               INT
        ,
        "currency_id"            INT
        ,
        "DebtRefID"              INT

        ,
        "DebtRefModel"           VARCHAR(255)

        ,
        "CrossAmount"            FLOAT   DEFAULT (0)
        ,
        "CrossAmountOC"          FLOAT   DEFAULT (0)
        ,
        "IsCrossRow"             BOOLEAN DEFAULT (FALSE)
        ,
        "CHI_TIET_ID"            INT

        ,
        "CHI_TIET_MODEL"         VARCHAR(255)
        ,
        "SO_HOA_DON"             VARCHAR(22)
        ,
        "THU_TU_CHI_TIET_GHI_SO" INT
        ,
        "THU_TU_TRONG_CHUNG_TU"  INT


    )
    ;


    INSERT INTO TMP_KET_QUA
    ("NHAN_VIEN_ID"
        , "DOI_TUONG_ID"
        , "MA_KHACH_HANG"
        , "TEN_KHACH_HANG"

        , "ID_CHUNG_TU"
        , "MODEL_CHUNG_TU"
        , "LOAI_CHUNG_TU"
        , "NGAY_HACH_TOAN"
        , "NGAY_CHUNG_TU"
        , "SO_CHUNG_TU"

        , "DIEN_GIAI_CHUNG"
        , "MA_TK"

        , "MA_TAI_KHOAN_DOI_UNG"

        , "GHI_NO_NGUYEN_TE"
        , "GHI_NO"
        , "GHI_CO_NGUYEN_TE"
        , "GHI_CO"
        , "GLJournalMemo"
        , "OrderType"
        , "LedgerID"
        , "currency_id"
        , "DebtRefID"
        , "DebtRefModel"
        , "CHI_TIET_ID"
        , "CHI_TIET_MODEL"
        , "SO_HOA_DON"
        ,
     "THU_TU_CHI_TIET_GHI_SO"
        ,
     "THU_TU_TRONG_CHUNG_TU"


    )


        SELECT T.*
        FROM (
                 SELECT
                       COALESCE(GD."NHAN_VIEN_ID", AL."NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                     , AL."DOI_TUONG_ID"
                     , AO."MA_KHACH_HANG"
                     , AO."TEN_KHACH_HANG"
                     , AL."ID_CHUNG_TU"
                     , AL."MODEL_CHUNG_TU"
                     , AL."LOAI_CHUNG_TU"
                     , AL."NGAY_HACH_TOAN"
                     , AL."NGAY_CHUNG_TU"
                     , AL."SO_CHUNG_TU"
                     , COALESCE(AL."DIEN_GIAI", AL."DIEN_GIAI_CHUNG") AS "DIEN_GIAI_CHUNG"
                     , AL."MA_TK"
                     , AL."MA_TK_DOI_UNG"                             AS "MA_TAI_KHOAN_DOI_UNG"
                     , AL."GHI_NO_NGUYEN_TE"
                     , AL."GHI_NO"
                     , AL."GHI_CO_NGUYEN_TE"
                     , AL."GHI_CO"
                     , AL."DIEN_GIAI_CHUNG"                           AS "GLJournalMemo"
                     , 1                                              AS "OrderType"
                     , Al."id"                                        AS "LedgerID"
                     , AL."currency_id"
                     , SA."CHUNG_TU_BAN_HANG_ID"                      AS "DebtRefID"
                    , 'sale.document'                                AS "DebtRefModel"
                     , AL."CHI_TIET_ID"
                     , AL."CHI_TIET_MODEL"
                     , AL."SO_HOA_DON"
                     , AL."THU_TU_CHI_TIET_GHI_SO"
                     , AL."THU_TU_TRONG_CHUNG_TU"
                 FROM so_cong_no_chi_tiet Al
                     INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = Al."DOI_TUONG_ID"
                     INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
                     INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = Al."MA_TK"
                     LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = Al."DVT_ID"

                     LEFT JOIN TMP_CONG_NO_DOI_TRU GD ON AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU"
                                                         AND AL."MODEL_CHUNG_TU" = 'sale.ex.doi.tru.chi.tiet'
                                                         AND AL."TK_ID" = GD."TAI_KHOAN_ID"
                                                         AND AL."DOI_TUONG_ID" = GD."DOI_TUONG_ID"
                                                         AND AL."currency_id" = GD."currency_id"
                     LEFT JOIN (
                                   SELECT
                                       SAR."id"
                                       , SAR."SO_CHUNG_TU_ID"                AS "CHUNG_TU_BAN_HANG_ID"
                                       , 'sale.ex.tra.lai.hang.ban.chi.tiet' AS "model_chung_tu"
                                   FROM sale_ex_tra_lai_hang_ban_chi_tiet SAR
                                   WHERE SAR."SO_CHUNG_TU_ID" IS NOT NULL
                                   UNION ALL
                                   SELECT
                                       SAD.id
                                       , SAD."CHUNG_TU_BAN_HANG_ID"
                                       , 'sale.ex.chi.tiet.giam.gia.hang.ban' AS "model_chung_tu"
                                   FROM sale_ex_chi_tiet_giam_gia_hang_ban SAD
                                   WHERE SAD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                               ) SA
                         ON (SA.id = AL."CHI_TIET_ID" AND
                             AL."CHI_TIET_MODEL" = SA."model_chung_tu")

                 WHERE (AL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay)

                       AND (AL."currency_id" = v_loai_tien_id OR v_loai_tien_id IS NULL)
                       AND (AL."GHI_NO_NGUYEN_TE" <> 0 OR AL."GHI_NO" <> 0 OR AL."GHI_CO_NGUYEN_TE" <> 0 OR
                            AL."GHI_CO" <> 0)

                 UNION ALL
                 SELECT
                       COALESCE(GD."NHAN_VIEN_ID", AL."NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                     , AL."DOI_TUONG_ID"
                     , AO."MA_KHACH_HANG"
                     , AO."TEN_KHACH_HANG"
                     , AL."ID_CHUNG_TU"
                     , AL."MODEL_CHUNG_TU"
                     , NULL                                           AS "LOAI_CHUNG_TU"
                     , NULL :: DATE                                   AS "NGAY_HACH_TOAN"
                     , NULL                                           AS "NGAY_CHUNG_TU"
                     , NULL                                           AS "SO_CHUNG_TU"
                     , OPNJournalMemo                                 AS "DIEN_GIAI_CHUNG"
                     , AL."MA_TK"
                     , NULL                                           AS "MA_TAI_KHOAN_DOI_UNG"
                     , AL."GHI_NO_NGUYEN_TE"
                     , AL."GHI_NO"
                     , AL."GHI_CO_NGUYEN_TE"
                     , AL."GHI_CO"
                     , NULL                                           AS "GLJournalMemo"
                     , 0                                              AS "OrderType"
                     , Al."id"                                        AS "LedgerID"
                     , AL."currency_id"
                     , SA."CHUNG_TU_BAN_HANG_ID"                      AS "DebtRefID"
                     , 'sale.document'                                AS "DebtRefModel"
                     , AL."CHI_TIET_ID"
                     , AL."CHI_TIET_MODEL"
                     , NULL                                           AS "SO_HOA_DON"
                     , NULL                                           AS "THU_TU_CHI_TIET_GHI_SO"
                     , NULL                                           AS "THU_TU_TRONG_CHUNG_TU"


                 FROM TMP_SO_CONG_NO_CHI_TIET Al
                     INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = Al."DOI_TUONG_ID"

                     LEFT JOIN TMP_CONG_NO_DOI_TRU GD ON AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU"
                                                         AND AL."MODEL_CHUNG_TU" = 'sale.ex.doi.tru.chi.tiet'
                                                         AND AL."TK_ID" = GD."TAI_KHOAN_ID"
                                                         AND AL."DOI_TUONG_ID" = GD."DOI_TUONG_ID"
                                                         AND AL."currency_id" = GD."currency_id"
                     LEFT JOIN (
                                   SELECT
                                       SAR.id
                                       , SAR."SO_CHUNG_TU_ID"                AS "CHUNG_TU_BAN_HANG_ID"
                                       , 'sale.ex.tra.lai.hang.ban.chi.tiet' AS "model_chung_tu"
                                   FROM sale_ex_tra_lai_hang_ban_chi_tiet SAR
                                   WHERE SAR."SO_CHUNG_TU_ID" IS NOT NULL
                                   UNION ALL
                                   SELECT
                                       SAD.id
                                       , SAD."CHUNG_TU_BAN_HANG_ID"           AS "CHUNG_TU_BAN_HANG_ID"
                                       , 'sale.ex.chi.tiet.giam.gia.hang.ban' AS "model_chung_tu"
                                   FROM sale_ex_chi_tiet_giam_gia_hang_ban SAD
                                   WHERE SAD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                               ) SA
                         ON (SA.id = AL."CHI_TIET_ID" AND
                             AL."CHI_TIET_MODEL" = SA."model_chung_tu")
                     LEFT JOIN TMP_KHUYEN_MAI D
                         ON Al."CHI_TIET_ID" = D."CHUNG_TU_BAN_HANG_CHI_TIET_ID"
                            AND Al."CHI_TIET_MODEL" = D."MODEL_CHUNG_TU_CHI_TIET"

                 WHERE (AL."NGAY_HACH_TOAN" < v_tu_ngay)

                       AND (AL."currency_id" = v_loai_tien_id OR v_loai_tien_id IS NULL)
                       AND (AL."GHI_NO_NGUYEN_TE" <> 0 OR AL."GHI_NO" <> 0 OR AL."GHI_CO_NGUYEN_TE" <> 0 OR
                            AL."GHI_CO" <> 0)

             ) T

        ORDER BY

            T."NGAY_HACH_TOAN" NULLS FIRST,
			T."SO_CHUNG_TU" NULLS FIRST,
			T."SO_HOA_DON" NULLS FIRST,
			 T."MA_TK" NULLS FIRST,
			T."GHI_CO" NULLS FIRST,
			T."GHI_NO" NULLS FIRST,

            T."ID_CHUNG_TU" NULLS FIRST,
            T."MODEL_CHUNG_TU" NULLS FIRST,
            T."DOI_TUONG_ID" NULLS FIRST,
             T."currency_id" NULLS FIRST,
            T."CHI_TIET_ID" NULLS FIRST,
            T."CHI_TIET_MODEL" NULLS FIRST,
            T."THU_TU_TRONG_CHUNG_TU" NULLS FIRST,
            T."THU_TU_CHI_TIET_GHI_SO" NULLS FIRST

    ;



    FOR rec IN
    SELECT

          GP."ID_CHUNG_TU"                AS "PayRefID"
        , GP."MODEL_CHUNG_TU"             AS "PayRef_model_ID"
        , GP."DOI_TUONG_ID"               AS "PayAccountObject"
        , GP."NHAN_VIEN_ID"               AS "PayEmployee"
        , GP."MA_TAI_KHOAN"               AS "PayAccountNumber"
        , GP."currency_id"                AS "PayCurrency"

        , GP."SO_TIEN_THANH_TOAN"         AS "PayAmountOC"
        , GP."SO_TIEN_THANH_TOAN_QUY_DOI" AS "PayAmount"
        , GP."ID_CHUNG_TU_CONG_NO"        AS "ID_CHUNG_TU_CONG_NO"
        , GP."MODEL_CHUNG_TU_CONG_NO"     AS "MODEL_CHUNG_TU_CONG_NO"
        , GP."NGAY_HACH_TOAN_CONG_NO"
        , GP."SO_CHUNG_TU_CONG_NO"
        , GP."SO_HOA_DON_CONG_NO"

    FROM TMP_CHUNG_TU_THANH_TOAN GP
    WHERE GP."ID_CHUNG_TU"
          IN (SELECT T."ID_CHUNG_TU"
              FROM TMP_KET_QUA T
              WHERE T."GHI_CO_NGUYEN_TE" > 0 OR T."GHI_CO" > 0)
    ORDER BY
        GP."NGAY_HACH_TOAN_CONG_NO" NULLS FIRST,
        GP."SO_CHUNG_TU_CONG_NO" NULLS FIRST,
        GP."SO_HOA_DON_CONG_NO" NULLS FIRST,
        GP."SO_TIEN_THANH_TOAN_QUY_DOI" NULLS FIRST

    LOOP


          LedgerID = NULL; --LedgerID
        CrossAmountOC = 0;--CrossAmountOC
        CrossAmount = 0;--CrossAmount
        OldRemainAmountOC = 0;--OldRemainAmountOC
        OldRemainAmount = 0;--OldRemainAmount
        RemainAmountOC = 0;--RemainAmountOC
       RemainAmount = 0;--RemainAmount



        FOR rec_2 IN SELECT *
                     FROM TMP_KET_QUA
                     WHERE "ID_CHUNG_TU" = rec."PayRefID"
                         and "MODEL_CHUNG_TU" = rec."PayRef_model_ID"
                           AND "DOI_TUONG_ID" = rec."PayAccountObject"
                           AND "MA_TK" = rec."PayAccountNumber"
                           AND "currency_id" = rec."PayCurrency"
                           AND (
                               ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL)
                               OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND
                                   rec."MODEL_CHUNG_TU_CONG_NO" = "DebtRefModel"))
                           AND "IsCrossRow" = FALSE

        LOOP

            SELECT (CASE
                    WHEN COALESCE(LedgerID, 0) <> rec_2."LedgerID"
                        THEN
                            COALESCE(rec_2."GHI_CO", 0)
                    ELSE
                        COALESCE(RemainAmount, 0) END)
            INTO OldRemainAmount
        ;

            SELECT (CASE WHEN COALESCE(LedgerID, 0) <> rec_2."LedgerID"
                THEN
                    COALESCE(rec_2."GHI_CO_NGUYEN_TE", 0)
                    ELSE RemainAmountOC END)
            INTO OldRemainAmountOC
        ;

            SELECT (CASE WHEN OldRemainAmount < rec."PayAmount"
                THEN
                    OldRemainAmount
                    ELSE rec."PayAmount" END)
            INTO CrossAmount
        ;

            SELECT (CASE WHEN OldRemainAmountOC < rec."PayAmount"
                THEN
                    OldRemainAmountOC
                    ELSE rec."PayAmount" END)
            INTO CrossAmountOC
        ;

            RemainAmount = OldRemainAmount - CrossAmount
        ;

            RemainAmountOC = OldRemainAmountOC - CrossAmountOC
        ;

            UPDATE TMP_KET_QUA
            SET "CrossAmount"   = CrossAmount,
                "CrossAmountOC" = CrossAmountOC

            WHERE RowNum = rec_2.RowNum
        ;


            UPDATE TMP_KET_QUA
            SET "GHI_CO"           = RemainAmount,
                "GHI_CO_NGUYEN_TE" = RemainAmountOC

            WHERE RowNum = rec_2.RowNum
        ;

            rec."PayAmount" = rec."PayAmount" - CrossAmount
        ;

            rec."PayAmountOC" = rec."PayAmountOC" - CrossAmountOC
        ;

            SELECT rec_2."LedgerID"
            INTO LedgerID
        ;

            UPDATE TMP_KET_QUA
            SET "LedgerID" = rec_2."LedgerID"

            WHERE RowNum = rec_2.RowNum
        ;


        END LOOP
    ;

        UPDATE TMP_KET_QUA
        SET
            "GHI_CO"             = "CrossAmount"
            , "GHI_CO_NGUYEN_TE" = "CrossAmountOC"
            , "CrossAmount"      = 0
            , "CrossAmountOC"    = 0
            , "NHAN_VIEN_ID"     = COALESCE(rec."PayEmployee", "NHAN_VIEN_ID")
            , "IsCrossRow"       = TRUE
        WHERE "ID_CHUNG_TU" = rec."PayRefID"
                 and "MODEL_CHUNG_TU" = rec."PayRef_model_ID"
              AND "DOI_TUONG_ID" = rec."PayAccountObject"
              AND "MA_TK" = rec."PayAccountNumber"
              AND "currency_id" = rec."PayCurrency"
              AND (
                  ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL)
                  OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND rec."MODEL_CHUNG_TU_CONG_NO" = "DebtRefModel"))
              AND "IsCrossRow" = FALSE
              AND "GHI_CO_NGUYEN_TE" = 0
              AND "GHI_CO" = 0
              AND
              (
                  "CrossAmountOC" <> 0
                  OR "CrossAmount" <> 0
              )
    ;



        INSERT INTO TMP_KET_QUA
        ("NHAN_VIEN_ID"
            , "DOI_TUONG_ID"
            , "MA_KHACH_HANG"
            , "TEN_KHACH_HANG"

            , "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , "LOAI_CHUNG_TU"
            , "NGAY_HACH_TOAN"
            , "NGAY_CHUNG_TU"
            , "SO_CHUNG_TU"

            , "DIEN_GIAI_CHUNG"
            , "MA_TK"

            , "MA_TAI_KHOAN_DOI_UNG"

            , "GHI_NO_NGUYEN_TE"
            , "GHI_NO"
            , "GHI_CO_NGUYEN_TE"
            , "GHI_CO"
            , "GLJournalMemo"
            , "OrderType"
            , "LedgerID"
            , "currency_id"
            , "DebtRefID"
            , "IsCrossRow"
            , "CHI_TIET_ID"
            , "CHI_TIET_MODEL"


        )
            SELECT
                  COALESCE(rec."PayEmployee","NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                , "DOI_TUONG_ID"
                , "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"

                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"
                , "SO_CHUNG_TU"

                , "DIEN_GIAI_CHUNG"
                , "MA_TK"

                , "MA_TAI_KHOAN_DOI_UNG"

                , "GHI_NO_NGUYEN_TE"
                , "GHI_NO"
                , "CrossAmountOC"
                , "CrossAmount"
                , "GLJournalMemo"
                , "OrderType"
                , "LedgerID"
                , "currency_id"
                , "DebtRefID"
                , TRUE                        AS "IsCrossRow"
                , "CHI_TIET_ID"
                , "CHI_TIET_MODEL"

            FROM TMP_KET_QUA
            WHERE
                "ID_CHUNG_TU" = rec."PayRefID"
                      and "MODEL_CHUNG_TU" = rec."PayRef_model_ID"
                AND "DOI_TUONG_ID" = rec."PayAccountObject"
                AND "MA_TK" = rec."PayAccountNumber"
                AND "currency_id" = rec."PayCurrency"
                AND (
                    ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL)
                    OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND
                        rec."MODEL_CHUNG_TU_CONG_NO" = "DebtRefModel"))
                AND "IsCrossRow" = FALSE
                AND ("GHI_CO_NGUYEN_TE" <> 0
                     OR "GHI_CO" <> 0)
                AND
                (
                    "CrossAmountOC" <> 0
                    OR "CrossAmount" <> 0
                )
    ;

        UPDATE TMP_KET_QUA
        SET "CrossAmount"   = 0,
            "CrossAmountOC" = 0

        WHERE "ID_CHUNG_TU" = rec."PayRefID"
              and "MODEL_CHUNG_TU" = rec."PayRef_model_ID"
              AND "DOI_TUONG_ID" = rec."PayAccountObject"
              AND "MA_TK" = rec."PayAccountNumber"
              AND "currency_id" = rec."PayCurrency"
              AND (
                  ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL)
                  OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND rec."MODEL_CHUNG_TU_CONG_NO" = "DebtRefModel"))
              AND "IsCrossRow" = FALSE
    ;


    END LOOP
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG

    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_CUOI_CUNG_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_CUOI_CUNG_seq
    ;


    CREATE TABLE TMP_KET_QUA_CUOI_CUNG (
        RowNum                   INT PRIMARY KEY DEFAULT NEXTVAL('TMP_KET_QUA_CUOI_CUNG_seq')
        ,
        "NHAN_VIEN_ID"           INT
        ,
        "MA_NHAN_VIEN"           VARCHAR(255)
        ,
        "TEN_NHAN_VIEN"          VARCHAR(128)
        ,
        "DOI_TUONG_ID"           INT
        ,
        "MA_KHACH_HANG"          VARCHAR(100)
        ,
        "TEN_KHACH_HANG"         VARCHAR(255)

        ,
        "NGAY_HACH_TOAN"         DATE
        ,
        "NGAY_CHUNG_TU"          DATE
        ,
        "SO_CHUNG_TU"            VARCHAR(22)

        ,
        "LOAI_CHUNG_TU"          VARCHAR(255)
        ,
        "ID_CHUNG_TU"            INT
        ,
        "MODEL_CHUNG_TU"         VARCHAR(255)

        ,
        "DIEN_GIAI_CHUNG"        VARCHAR(255)
        ,
        "MA_TK"                  VARCHAR(200)
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
        ,
        "DU_NO_NGUYEN_TE"        FLOAT
        ,
        "DU_NO"                  FLOAT
        ,
        "DU_CO_NGUYEN_TE"        FLOAT
        ,
        "DU_CO"                  FLOAT
        ,
        "GLJournalMemo"          VARCHAR(255)
        ,
        "OrderType"              INT
        ,
        "CHI_TIET_ID"            INT

        ,
        "CHI_TIET_MODEL"         VARCHAR(200)
        ,
        "THU_TU_CHI_TIET_GHI_SO" INT
        ,
        "THU_TU_TRONG_CHUNG_TU"  INT


    )
    ;

    IF v_cong_gop_but_toan_giong_nhau = 1
    THEN
        INSERT INTO TMP_KET_QUA_CUOI_CUNG (
            "NHAN_VIEN_ID"
            , "MA_NHAN_VIEN"
            , "TEN_NHAN_VIEN"
            , "DOI_TUONG_ID"
            , "MA_KHACH_HANG"
            , "TEN_KHACH_HANG"

            , "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , "LOAI_CHUNG_TU"
            , "NGAY_HACH_TOAN"
            , "NGAY_CHUNG_TU"
            , "SO_CHUNG_TU"


            , "DIEN_GIAI_CHUNG"
            , "MA_TK"
            , "TINH_CHAT"
            , "MA_TAI_KHOAN_DOI_UNG"

            , "GHI_NO_NGUYEN_TE"
            , "GHI_NO"
            , "GHI_CO_NGUYEN_TE"
            , "GHI_CO"
            , "GLJournalMemo"
            , "OrderType"
            , "THU_TU_CHI_TIET_GHI_SO"


        )
            SELECT
                R."NHAN_VIEN_ID"
                , E."MA_NHAN_VIEN"
                , E."TEN_NHAN_VIEN"
                , R."DOI_TUONG_ID"
                , R."MA_KHACH_HANG"
                , R."TEN_KHACH_HANG"

                , (CASE WHEN R."OrderType" = 0
                THEN NULL
                   ELSE R."ID_CHUNG_TU" END)             AS "ID_CHUNG_TU"
                , (CASE WHEN R."OrderType" = 0
                THEN NULL
                   ELSE R."MODEL_CHUNG_TU" END)          AS "MODEL_CHUNG_TU"
                , R."LOAI_CHUNG_TU"
                , R."NGAY_HACH_TOAN"
                , R."NGAY_CHUNG_TU"
                , R."SO_CHUNG_TU"

                , (CASE WHEN R."OrderType" = 0
                THEN OPNJournalMemo
                   ELSE R."GLJournalMemo" END)           AS "DIEN_GIAI_CHUNG"
                , R."MA_TK"
                , AC."TINH_CHAT"
                , R."MA_TAI_KHOAN_DOI_UNG"

                , SUM(COALESCE(R."GHI_NO_NGUYEN_TE", 0)) AS "GHI_NO_NGUYEN_TE"
                , SUM(COALESCE(R."GHI_NO", 0))           AS "GHI_NO"
                , SUM(COALESCE(R."GHI_CO_NGUYEN_TE", 0)) AS "GHI_CO_NGUYEN_TE"
                , SUM(COALESCE(R."GHI_CO", 0))           AS "GHI_CO"
                , R."GLJournalMemo"
                , R."OrderType"
                , R."THU_TU_CHI_TIET_GHI_SO"

            FROM TMP_KET_QUA R
                INNER JOIN DS_NHAN_VIEN E ON E."NHAN_VIEN_ID" = R."NHAN_VIEN_ID"
                INNER JOIN danh_muc_he_thong_tai_khoan AC ON AC."SO_TAI_KHOAN" = R."MA_TK"
            GROUP BY
                R."NHAN_VIEN_ID"
                , E."MA_NHAN_VIEN"
                , E."TEN_NHAN_VIEN"
                , R."DOI_TUONG_ID"
                , R."MA_KHACH_HANG"
                , R."TEN_KHACH_HANG"
                , (CASE
                   WHEN R."OrderType" = 0
                       THEN
                           NULL
                   ELSE
                       R."ID_CHUNG_TU"
                   END
            )
                , (CASE
                   WHEN R."OrderType" = 0
                       THEN
                           NULL
                   ELSE
                       R."MODEL_CHUNG_TU"
                   END
            )
                , R."LOAI_CHUNG_TU"
                , R."NGAY_HACH_TOAN"
                , R."NGAY_CHUNG_TU"
                , R."SO_CHUNG_TU"

                , R."MA_TK"
                , AC."TINH_CHAT"
                , R."MA_TAI_KHOAN_DOI_UNG"
                , R."GLJournalMemo"
                , R."OrderType"
                , R."THU_TU_CHI_TIET_GHI_SO"

            HAVING
                SUM(COALESCE(R."GHI_NO_NGUYEN_TE", 0)) <> 0
                OR SUM(COALESCE(R."GHI_NO", 0)) <> 0
                OR SUM(COALESCE(R."GHI_CO_NGUYEN_TE", 0)) <> 0
                OR SUM(COALESCE(R."GHI_CO", 0)) <> 0
            ORDER BY
                E."MA_NHAN_VIEN" NULLS FIRST,
                R."MA_KHACH_HANG" NULLS FIRST,
                R."OrderType" NULLS FIRST,
                R."NGAY_HACH_TOAN" NULLS FIRST,
                R."NGAY_CHUNG_TU" NULLS FIRST,
                R."SO_CHUNG_TU" NULLS FIRST,
                R."THU_TU_CHI_TIET_GHI_SO" NULLS FIRST
        ;


    ELSE
        INSERT INTO TMP_KET_QUA_CUOI_CUNG (
            "NHAN_VIEN_ID"
            , "MA_NHAN_VIEN"
            , "TEN_NHAN_VIEN"
            , "DOI_TUONG_ID"
            , "MA_KHACH_HANG"
            , "TEN_KHACH_HANG"
            , "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , "LOAI_CHUNG_TU"
            , "NGAY_HACH_TOAN"
            , "NGAY_CHUNG_TU"
            , "SO_CHUNG_TU"
            , "DIEN_GIAI_CHUNG"
            , "MA_TK"
            , "TINH_CHAT"
            , "MA_TAI_KHOAN_DOI_UNG"

            , "GHI_NO_NGUYEN_TE"
            , "GHI_NO"
            , "GHI_CO_NGUYEN_TE"
            , "GHI_CO"

            , "GLJournalMemo"
            , "OrderType"
            , "CHI_TIET_ID"

            , "CHI_TIET_MODEL"
            , "THU_TU_CHI_TIET_GHI_SO"
            , "THU_TU_TRONG_CHUNG_TU"

        )
            SELECT
                R."NHAN_VIEN_ID"
                , E."MA_NHAN_VIEN"
                , E."TEN_NHAN_VIEN"
                , R."DOI_TUONG_ID"
                , R."MA_KHACH_HANG"
                , R."TEN_KHACH_HANG"

                , (CASE WHEN R."OrderType" = 0
                THEN NULL
                   ELSE R."ID_CHUNG_TU" END)             AS "ID_CHUNG_TU"
                , (CASE WHEN R."OrderType" = 0
                THEN NULL
                   ELSE R."MODEL_CHUNG_TU" END)          AS "MODEL_CHUNG_TU"
                , R."LOAI_CHUNG_TU"
                , R."NGAY_HACH_TOAN"
                , R."NGAY_CHUNG_TU"
                , R."SO_CHUNG_TU"

                , R."DIEN_GIAI_CHUNG"
                , R."MA_TK"
                , AC."TINH_CHAT"
                , R."MA_TAI_KHOAN_DOI_UNG"

                , SUM(COALESCE(R."GHI_NO_NGUYEN_TE", 0)) AS "GHI_NO_NGUYEN_TE"
                , SUM(COALESCE(R."GHI_NO", 0))           AS "GHI_NO"
                , SUM(COALESCE(R."GHI_CO_NGUYEN_TE", 0)) AS "GHI_CO_NGUYEN_TE"
                , SUM(COALESCE(R."GHI_CO", 0))           AS "GHI_CO"
                , R."GLJournalMemo"
                , R."OrderType"
                , (CASE WHEN R."OrderType" = 0
                THEN NULL
                   ELSE R."CHI_TIET_ID" END)             AS "CHI_TIET_ID"
                , (CASE WHEN R."OrderType" = 0
                THEN NULL
                   ELSE R."CHI_TIET_MODEL" END)          AS "CHI_TIET_MODEL"
                , R."THU_TU_CHI_TIET_GHI_SO"
                , R."THU_TU_TRONG_CHUNG_TU"
            FROM TMP_KET_QUA R
                INNER JOIN DS_NHAN_VIEN E ON E."NHAN_VIEN_ID" = R."NHAN_VIEN_ID"
                INNER JOIN danh_muc_he_thong_tai_khoan AC ON AC."SO_TAI_KHOAN" = R."MA_TK"
            GROUP BY
                R."NHAN_VIEN_ID"
                , E."MA_NHAN_VIEN"
                , E."TEN_NHAN_VIEN"
                , R."DOI_TUONG_ID"
                , R."MA_KHACH_HANG"
                , R."TEN_KHACH_HANG"
                , (CASE
                   WHEN R."OrderType" = 0
                       THEN
                           NULL
                   ELSE
                       R."ID_CHUNG_TU"
                   END
            )
                , (CASE
                   WHEN R."OrderType" = 0
                       THEN
                           NULL
                   ELSE
                       R."MODEL_CHUNG_TU"
                   END
            )
                , R."LOAI_CHUNG_TU"
                , R."NGAY_HACH_TOAN"
                , R."NGAY_CHUNG_TU"
                , R."SO_CHUNG_TU"
                , R."DIEN_GIAI_CHUNG"
                , R."MA_TK"
                , AC."TINH_CHAT"
                , R."MA_TAI_KHOAN_DOI_UNG"
                , R."GLJournalMemo"
                , R."OrderType"
                , (CASE
                   WHEN R."OrderType" = 0
                       THEN
                           NULL
                   ELSE
                       R."CHI_TIET_ID"
                   END
            )
                , (CASE
                   WHEN R."OrderType" = 0
                       THEN
                           NULL
                   ELSE
                       R."CHI_TIET_MODEL"
                   END
            )
                , R."THU_TU_CHI_TIET_GHI_SO"
                , R."THU_TU_TRONG_CHUNG_TU"

            HAVING SUM(COALESCE(R."GHI_NO_NGUYEN_TE", 0)) <> 0 OR SUM(COALESCE(R."GHI_NO", 0)) <> 0
                   OR SUM(COALESCE(R."GHI_CO_NGUYEN_TE", 0)) <> 0 OR SUM(COALESCE(R."GHI_CO", 0)) <> 0
            ORDER BY
                E."MA_NHAN_VIEN" NULLS FIRST,
                R."MA_KHACH_HANG" NULLS FIRST,
                R."OrderType" NULLS FIRST,
                R."NGAY_HACH_TOAN" NULLS FIRST,
                R."NGAY_CHUNG_TU" NULLS FIRST,
                R."SO_CHUNG_TU" NULLS FIRST,
                R."THU_TU_TRONG_CHUNG_TU" NULLS FIRST,
                R."THU_TU_CHI_TIET_GHI_SO" NULLS FIRST
        ;
    END IF
    ;


    FOR rec IN
    SELECT *
    FROM TMP_KET_QUA_CUOI_CUNG
    ORDER BY RowNum
    LOOP

        SELECT (CASE WHEN COALESCE(KHACH_HANG_ID_TMP, 0) <> rec."DOI_TUONG_ID"
                          OR COALESCE(NHAN_VIEN_ID_TMP, 0) <> rec."NHAN_VIEN_ID"
            THEN
                0
                ELSE SO_TIEN_TON_TMP END) + rec."GHI_NO" - rec."GHI_CO"

        INTO SO_TIEN_TON_TMP
    ;

        rec."DU_NO" = SO_TIEN_TON_TMP
    ;


        UPDATE TMP_KET_QUA_CUOI_CUNG
        SET "DU_NO" = rec."DU_NO"

        WHERE "rownum" = rec."rownum"
    ;


        SELECT (CASE
                WHEN COALESCE(KHACH_HANG_ID_TMP, 0) <> rec."DOI_TUONG_ID"
                     OR COALESCE(NHAN_VIEN_ID_TMP, 0) <> rec."NHAN_VIEN_ID"
                    THEN
                        0
                ELSE SO_TIEN_TON_NGUYEN_TE_TMP END) + rec."GHI_NO_NGUYEN_TE" - rec."GHI_CO_NGUYEN_TE"

        INTO SO_TIEN_TON_NGUYEN_TE_TMP
    ;
        rec."DU_NO_NGUYEN_TE" = SO_TIEN_TON_TMP
    ;

        UPDATE TMP_KET_QUA_CUOI_CUNG
        SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"

        WHERE "rownum" = rec."rownum"
    ;

    KHACH_HANG_ID_TMP = rec."DOI_TUONG_ID" ;
    NHAN_VIEN_ID_TMP = rec."NHAN_VIEN_ID" ;



    END LOOP
    ;


    UPDATE TMP_KET_QUA_CUOI_CUNG
    SET
        "DU_NO_NGUYEN_TE"    = (CASE WHEN "TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND "DU_NO_NGUYEN_TE" >= 0)
                            THEN "DU_NO_NGUYEN_TE"
                                ELSE 0 END)
        , "DU_NO"            = (CASE WHEN "TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND "DU_NO" >= 0)
                                THEN "DU_NO"
                                ELSE 0 END)
        , "DU_CO_NGUYEN_TE"  = (CASE WHEN "TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND "DU_NO_NGUYEN_TE" <= 0)
                                THEN (-1) * "DU_NO_NGUYEN_TE"
                                ELSE 0 END)
        , "DU_CO"            = (CASE WHEN "TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND "DU_NO" <= 0)
                                THEN (-1) * "DU_NO"
                                ELSE 0 END)
        , "GHI_NO_NGUYEN_TE" = (CASE WHEN "OrderType" = 1
                                THEN "GHI_NO_NGUYEN_TE"
                                ELSE 0 END)
        , "GHI_NO"           = (CASE WHEN "OrderType" = 1
                                THEN "GHI_NO"
                                ELSE 0 END)
        , "GHI_CO_NGUYEN_TE" = (CASE WHEN "OrderType" = 1
                                THEN "GHI_CO_NGUYEN_TE"
                                ELSE 0 END)
        , "GHI_CO"           = (CASE WHEN "OrderType" = 1
                                THEN "GHI_CO"
                                ELSE 0 END)

    ;



    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG_1

    ;

   CREATE TEMP  TABLE  TMP_KET_QUA_CUOI_CUNG_1
       AS

    SELECT
        R.*
        , CASE WHEN R."NGAY_HACH_TOAN" < v_tu_ngay
        THEN CAST(0 AS BOOLEAN)
          ELSE
              CASE WHEN PR."LA_HANG_KHUYEN_MAI" = '1'
                  THEN CAST(1 AS BOOLEAN)
              ELSE CAST(0 AS BOOLEAN) END
          END
        AS "LA_HANG_KHUYEN_MAI"
    FROM TMP_KET_QUA_CUOI_CUNG R
        LEFT JOIN TMP_KHUYEN_MAI PR ON PR."CHUNG_TU_BAN_HANG_CHI_TIET_ID" = R."CHI_TIET_ID" AND
                                       PR."MODEL_CHUNG_TU_CHI_TIET" = R."CHI_TIET_MODEL"
    WHERE (("GHI_CO" <> 0 OR "GHI_CO_NGUYEN_TE" <> 0 OR "GHI_NO" <> 0 OR "GHI_NO_NGUYEN_TE" <> 0) AND "OrderType" <> 0)
          OR
          (("DU_CO" <> 0 OR "DU_CO_NGUYEN_TE" <> 0 OR "DU_NO" <> 0 OR "DU_NO_NGUYEN_TE" <> 0) AND "OrderType" = 0)
    ;


END $$

;

SELECT  
        "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
        "NGAY_CHUNG_TU" as "NGAY_CHUNG_TU",
        "SO_CHUNG_TU" as "SO_CHUNG_TU",
        "DIEN_GIAI_CHUNG" as "DIEN_GIAI",
        "MA_TK" as "TK_CO_ID",
        "MA_TAI_KHOAN_DOI_UNG" as "TK_DOI_UNG",
        "GHI_NO" as "NO_SO_PHAT_SINH",
        "GHI_CO" as "CO_SO_PHAT_SINH",
        "DU_NO_NGUYEN_TE" as "NO_SO_DU",
        "DU_CO_NGUYEN_TE" as "CO_SO_DU",
        "TEN_NHAN_VIEN" as "TEN_NHAN_VIEN",
        "TEN_KHACH_HANG" as "TEN_KHACH_HANG",
        "ID_CHUNG_TU" as "ID_GOC",
        "MODEL_CHUNG_TU" as "MODEL_GOC"

FROM TMP_KET_QUA_CUOI_CUNG_1 
OFFSET %(offset)s
LIMIT %(limit)s
;



        """
        return self.execute(query,params_sql)

        
    def _lay_bao_cao_thong_ke_theo_cong_trinh(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    


    rec                                   RECORD;

    CHE_DO_KE_TOAN                        VARCHAR(100);

    SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT := 0;

    SO_TIEN_TON_TMP                       FLOAT := 0;

    MA_KHACH_HANG_TMP                     VARCHAR(100) :=N'';

    SO_TAI_KHOAN_TMP                      VARCHAR(100) :=N'';

    MA_CONG_TRINH_TMP                     VARCHAR(100) :=N'';


BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;


    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT
                "id" AS "KHACH_HANG_ID"

                , "LIST_MA_NHOM_KH_NCC"
                , -- Danh sách mã nhóm
                "LIST_TEN_NHOM_KH_NCC"
            -- Danh sách tên nhóm


            FROM res_partner AO
            WHERE (id = any (%(KHACH_HANG_IDS)s))  

    ;


    DROP TABLE IF EXISTS DS_CONG_TRINH_DC_CHON
    ;

    CREATE TEMP TABLE DS_CONG_TRINH_DC_CHON
        AS

            SELECT DISTINCT
                PW."id" AS "CONG_TRINH_ID"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"
                , PWC.name


            FROM danh_muc_cong_trinh PW
                LEFT JOIN danh_muc_loai_cong_trinh PWC ON PW."LOAI_CONG_TRINH" = PWC.id
            WHERE (PW.id = any (%(CONG_TRINHIDS)s))
    ;

    DROP TABLE IF EXISTS DS_CONG_TRINH_DC_CHON_CHILD
    ;

    CREATE TEMP TABLE DS_CONG_TRINH_DC_CHON_CHILD
        AS

            SELECT
                S."CONG_TRINH_ID"
                , S."MA_PHAN_CAP"
                , S."MA_CONG_TRINH"
                , S."TEN_CONG_TRINH"
                , S.name
            FROM DS_CONG_TRINH_DC_CHON S
                LEFT JOIN DS_CONG_TRINH_DC_CHON S1 ON S1."MA_PHAN_CAP" LIKE S."MA_PHAN_CAP"
                                                                            || '%%'
                                                      AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
            WHERE S1."MA_PHAN_CAP" IS NULL
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
            FROM DS_CONG_TRINH_DC_CHON_CHILD SPW
                INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE SPW."MA_PHAN_CAP"
                                                                           || '%%'
    ;


    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id"
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" = so_tai_khoan
                ORDER BY
                    A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id"
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '1'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY
                    A."SO_TAI_KHOAN",
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
        RowNum                   INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,

        "MA_CONG_TRINH"          VARCHAR(200)
        ,
        "TEN_CONG_TRINH"         VARCHAR(200)


        ,
        "DOI_TUONG_ID"           INT

        ,
        "MA_KHACH_HANG"          VARCHAR(200)
        ,
        "TEN_KHACH_HANG"         VARCHAR(200)

        ,
        "NGAY_HACH_TOAN"         DATE

        ,
        "NGAY_CHUNG_TU"          DATE

        ,
        "SO_CHUNG_TU"            VARCHAR(200)
        ,
        "LOAI_CHUNG_TU"          VARCHAR(200)
        , --Loại chứng từ
        "ID_CHUNG_TU"            INT
        ,
        "MODEL_CHUNG_TU"         VARCHAR(200)
        ,
        "DIEN_GIAI_CHUNG"        VARCHAR(200)
        , -- Diễn giải
        "SO_TAI_KHOAN"           VARCHAR(200)
        , -- Số tài khoản
        "TINH_CHAT"              VARCHAR(200)
        , -- Tính chất tài khoản
        "MA_TK_DOI_UNG"          VARCHAR(200)

        ,
        "GHI_NO_NGUYEN_TE"       FLOAT
        ,
        "GHI_NO"                 FLOAT
        , -- Diễn giải
        "GHI_CO_NGUYEN_TE"       FLOAT
        , -- Số tài khoản
        "GHI_CO"                 FLOAT
        , -- Tính chất tài khoản
        "DU_NO_NGUYEN_TE"        FLOAT

        ,
        "DU_NO"                  FLOAT
        ,
        "DU_CO_NGUYEN_TE"        FLOAT
        , -- Diễn giải
        "DU_CO"                  FLOAT
        , -- Số tài khoản
        "OrderType"              INT

        ,
        "THU_TU_TRONG_CHUNG_TU"  INT
        ,
        "THU_TU_CHI_TIET_GHI_SO" INT


    )
    ;

    IF v_cong_gop_but_toan_giong_nhau = 0 -- Nếu không cộng gộp
    THEN

        INSERT INTO TMP_KET_QUA
        (


            "MA_CONG_TRINH"
            ,
            "TEN_CONG_TRINH"


            , "DOI_TUONG_ID"

            ,
            "MA_KHACH_HANG"
            ,
            "TEN_KHACH_HANG"

            ,
            "NGAY_HACH_TOAN"

            ,
            "NGAY_CHUNG_TU"

            ,
            "SO_CHUNG_TU"
            ,
            "LOAI_CHUNG_TU"
            , --Loại chứng từ
            "ID_CHUNG_TU"
            ,
            "MODEL_CHUNG_TU"
            ,
            "DIEN_GIAI_CHUNG"
            , -- Diễn giải
            "SO_TAI_KHOAN"
            , -- Số tài khoản
            "TINH_CHAT"
            , -- Tính chất tài khoản
            "MA_TK_DOI_UNG"

            ,
            "GHI_NO_NGUYEN_TE"
            ,
            "GHI_NO"
            , -- Diễn giải
            "GHI_CO_NGUYEN_TE"
            , -- Số tài khoản
            "GHI_CO"
            , -- Tính chất tài khoản
            "DU_NO_NGUYEN_TE"

            ,
            "DU_NO"
            ,
            "DU_CO_NGUYEN_TE"
            , -- Diễn giải
            "DU_CO"
            , -- Số tài khoản
            "OrderType"

            ,
            "THU_TU_TRONG_CHUNG_TU"
            ,
            "THU_TU_CHI_TIET_GHI_SO"


        )

            SELECT

                "MA_CONG_TRINH"

                , "TEN_CONG_TRINH"
                , "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , -- Mã NCC
                "TEN_DOI_TUONG"
                , -- Tên NCC

                "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"

                , "SO_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , --Loại chứng từ
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , -- Diễn giải
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản
                "MA_TK_DOI_UNG"
                , --TK đối ứng

                SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                SUM("GHI_NO")           AS "GHI_NO"
                , -- Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                SUM("GHI_CO")           AS "GHI_CO"
                , -- Phát sinh có quy đổi
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN SUM("DU_NO_NGUYEN_TE"
                         )
                         - SUM("DU_CO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE")
                                 - SUM("DU_CO_NGUYEN_TE")) > 0
                     THEN (SUM("DU_NO_NGUYEN_TE")
                           - SUM("DU_CO_NGUYEN_TE"))
                      ELSE 0
                      END

                 END)                   AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN (SUM("DU_NO")
                          - SUM("DU_CO"))
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_NO")
                                 - SUM("DU_CO")) > 0
                     THEN SUM("DU_NO")
                          - SUM("DU_CO")
                      ELSE 0
                      END
                 END)                   AS "DU_NO"
                , --Dư Nợ Quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("DU_CO_NGUYEN_TE")
                          - SUM("DU_NO_NGUYEN_TE"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE")
                                 - SUM("DU_NO_NGUYEN_TE")) > 0
                     THEN (SUM("DU_CO_NGUYEN_TE")
                           - SUM("DU_NO_NGUYEN_TE"))
                      ELSE 0
                      END
                 END)                   AS "DU_CO_NGUYEN_TE"
                , --Dư Có
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("DU_CO")
                          - SUM("DU_NO"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_CO")
                                 - SUM("DU_NO")) > 0
                     THEN (SUM("DU_CO")
                           - SUM("DU_NO"))
                      ELSE 0
                      END
                 END)                   AS "DU_CO" --Dư Có quy đổi
                , "OrderType"
                , "THU_TU_TRONG_CHUNG_TU"
                , "THU_TU_CHI_TIET_GHI_SO"

            FROM (SELECT
                      PWC."MA_CONG_TRINH"
                      , -- Mã công trình
                      PWC."TEN_CONG_TRINH"


                      , -- Loại công trình
                      AOL."DOI_TUONG_ID"
                      , AOL."MA_DOI_TUONG"
                      , -- Mã KH
                      AOL."TEN_DOI_TUONG"
                      , -- Tên KH
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."NGAY_HACH_TOAN"
                        END AS "NGAY_HACH_TOAN"

                      , -- Tên KH
                        CASE WHEN AOL."NGAY_CHUNG_TU" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."NGAY_CHUNG_TU"
                        END AS "NGAY_CHUNG_TU"
                      , -- Ngày hạch toán

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."SO_CHUNG_TU"
                        END AS "SO_CHUNG_TU"
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."ID_CHUNG_TU"
                        END AS "ID_CHUNG_TU"
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."MODEL_CHUNG_TU"
                        END AS "MODEL_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."LOAI_CHUNG_TU"
                        END AS "LOAI_CHUNG_TU"

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                        ELSE COALESCE(AOL."DIEN_GIAI",
                                      AOL."DIEN_GIAI_CHUNG")
                        END AS "DIEN_GIAI_CHUNG"
                      , -- Diễn giải (lấy diễn giải Detail, nếu null thì lấy diễn giải master)
                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."MA_TK_DOI_UNG"
                        END AS "MA_TK_DOI_UNG"
                      , --TK đối ứng
                      -- LVDIEP 17/10/2016: PBI 15608 - Sửa công thức cách lấy số liệu các báo cáo công nợ để đáp ứng theo từng chế độ QĐ48 thay TT133

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO_NGUYEN_TE"
                        END AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO"
                        END AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO_NGUYEN_TE"
                        END AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO"
                        END AS "GHI_CO"
                      , -- Phát sinh có quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0
                        END AS "DU_NO_NGUYEN_TE"
                      , --Dư Nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO"
                        ELSE 0
                        END AS "DU_NO"
                      , --Dư Nợ Quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0
                        END AS "DU_CO_NGUYEN_TE"
                      , --Dư Có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO"
                        ELSE 0
                        END AS "DU_CO"
                      --Dư Có quy đổi
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE 1
                        END AS "OrderType"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                        END AS "THU_TU_TRONG_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                        END AS "THU_TU_CHI_TIET_GHI_SO"

                  FROM so_cong_no_chi_tiet AS AOL
                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"

                      INNER JOIN DS_KHACH_HANG
                          AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"

                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      INNER JOIN DS_CONG_TRINH LPID ON AOL."CONG_TRINH_ID" = LPID."CONG_TRINH_ID"
                      LEFT JOIN DS_CONG_TRINH_DC_CHON_CHILD PWC ON LPID."MA_PHAN_CAP" LIKE PWC."MA_PHAN_CAP"
                                                                                           || '%%'

                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id"
                      -- Danh mục ĐVT
                      LEFT JOIN danh_muc_don_vi_tinh AS U ON AOL."DVT_ID" = U."id"
                      -- Danh mục ĐVT
                      --LEFT JOIN dbo.CustomFieldLedger AS CFL ON AOL.RefDetailID = CFL.RefDetailID

                      LEFT JOIN danh_muc_ma_thong_ke AS LI ON AOL."MA_THONG_KE_ID" = LI."id"

                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '1'

                 ) AS RSNS
            GROUP BY
                RSNS."MA_CONG_TRINH",
                RSNS."TEN_CONG_TRINH",
                RSNS."DOI_TUONG_ID",
                RSNS."MA_DOI_TUONG", -- Mã NCC
                RSNS."TEN_DOI_TUONG", -- Tên NCC

                RSNS."NGAY_HACH_TOAN", -- Ngày hạch toán
                RSNS."NGAY_CHUNG_TU",
                RSNS."SO_CHUNG_TU", -- Số chứng từ

                RSNS."LOAI_CHUNG_TU", --Loại chứng từ
                RSNS."ID_CHUNG_TU", -- Mã chứng từ
                RSNS."MODEL_CHUNG_TU",
                RSNS."DIEN_GIAI_CHUNG", -- Diễn giải
                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT", -- Tính chất tài khoản
                RSNS."MA_TK_DOI_UNG", --TK đối ứng
                RSNS."OrderType",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"

            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                   OR SUM("GHI_NO") <> 0
                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                   OR SUM("GHI_CO") <> 0
                   OR SUM("DU_NO_NGUYEN_TE"
                          - "DU_CO_NGUYEN_TE") <> 0
                   OR SUM("DU_NO"
                          - "DU_CO") <> 0
            ORDER BY
                RSNS."MA_CONG_TRINH",
                RSNS."MA_DOI_TUONG",
                RSNS."SO_TAI_KHOAN",
                RSNS."OrderType",
                RSNS."NGAY_HACH_TOAN",
                RSNS."NGAY_CHUNG_TU",
                RSNS."SO_CHUNG_TU",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"

        ;

    ELSE -- Cộng gộp các bút toán giống nhau

        INSERT INTO TMP_KET_QUA
        (


            "MA_CONG_TRINH"
            ,
            "TEN_CONG_TRINH"


            , "DOI_TUONG_ID"

            ,
            "MA_KHACH_HANG"
            ,
            "TEN_KHACH_HANG"

            ,
            "NGAY_HACH_TOAN"

            ,
            "NGAY_CHUNG_TU"

            ,
            "SO_CHUNG_TU"
            ,
            "LOAI_CHUNG_TU"
            , --Loại chứng từ
            "ID_CHUNG_TU"
            ,
            "MODEL_CHUNG_TU"
            ,
            "DIEN_GIAI_CHUNG"
            , -- Diễn giải
            "SO_TAI_KHOAN"
            , -- Số tài khoản
            "TINH_CHAT"
            , -- Tính chất tài khoản
            "MA_TK_DOI_UNG"

            ,
            "GHI_NO_NGUYEN_TE"
            ,
            "GHI_NO"
            , -- Diễn giải
            "GHI_CO_NGUYEN_TE"
            , -- Số tài khoản
            "GHI_CO"
            , -- Tính chất tài khoản
            "DU_NO_NGUYEN_TE"

            ,
            "DU_NO"
            ,
            "DU_CO_NGUYEN_TE"
            , -- Diễn giải
            "DU_CO"
            , -- Số tài khoản
            "OrderType"

            ,
            "THU_TU_TRONG_CHUNG_TU"
            ,
            "THU_TU_CHI_TIET_GHI_SO"


        )

            SELECT
                "MA_CONG_TRINH"

                , "TEN_CONG_TRINH"
                , "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , -- Mã NCC
                "TEN_DOI_TUONG"
                , -- Tên NCC

                "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"

                , "SO_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , --Loại chứng từ
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "DIEN_GIAI_CHUNG"
                , -- Diễn giải
                "SO_TAI_KHOAN"
                , -- Số tài khoản
                "TINH_CHAT"
                , -- Tính chất tài khoản
                "MA_TK_DOI_UNG"
                , --TK đối ứng
                "GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                "GHI_NO"
                , -- Phát sinh nợ quy đổi
                "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                "GHI_CO"
                , -- Phát sinh có quy đổi
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN ("DU_NO_NGUYEN_TE"
                          - "DU_CO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN ("DU_NO_NGUYEN_TE"
                                 - "DU_CO_NGUYEN_TE") > 0
                     THEN "DU_NO_NGUYEN_TE"
                          - "DU_CO_NGUYEN_TE"
                      ELSE 0
                      END
                 END) AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN ("DU_NO"
                          - "DU_CO")
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN ("DU_NO"
                                 - "DU_CO") > 0
                     THEN "DU_NO"
                          - "DU_CO"
                      ELSE 0
                      END
                 END) AS "DU_NO"
                , --Dư Nợ Quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN ("DU_CO_NGUYEN_TE"
                          - "DU_NO_NGUYEN_TE")
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN ("DU_CO_NGUYEN_TE"
                                 - "DU_NO_NGUYEN_TE") > 0
                     THEN ("DU_CO_NGUYEN_TE"
                           - "DU_NO_NGUYEN_TE")
                      ELSE 0
                      END
                 END) AS "DU_CO_NGUYEN_TE"
                , --Dư Có
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN ("DU_CO"
                          - "DU_NO")
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN ("DU_CO"
                                 - "DU_NO") > 0
                     THEN ("DU_CO"
                           - "DU_NO")
                      ELSE 0
                      END
                 END) AS "DU_CO"
                --Dư Có quy đổi
                , "OrderType"
                , "THU_TU_TRONG_CHUNG_TU"
                , "THU_TU_CHI_TIET_GHI_SO"

            FROM (SELECT
                      PWC."MA_CONG_TRINH"
                      , PWC."TEN_CONG_TRINH"
                      , AOL."DOI_TUONG_ID"
                      , AOL."MA_DOI_TUONG"

                      , AOL."TEN_DOI_TUONG"

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."NGAY_HACH_TOAN"
                        END AS "NGAY_HACH_TOAN"


                      , CASE WHEN AOL."NGAY_CHUNG_TU" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."NGAY_CHUNG_TU"
                        END AS "NGAY_CHUNG_TU"


                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."SO_CHUNG_TU"
                        END AS "SO_CHUNG_TU"


                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."ID_CHUNG_TU"
                        END AS "ID_CHUNG_TU"


                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."MODEL_CHUNG_TU"
                        END AS "MODEL_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."LOAI_CHUNG_TU"
                        END AS "LOAI_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'

                        ELSE AOL."DIEN_GIAI_CHUNG"
                        --ELSE AOL."DIEN_GIAI_CHUNG"
                        END AS "DIEN_GIAI_CHUNG"

                      , TBAN."SO_TAI_KHOAN"

                      , TBAN."TINH_CHAT"

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                       THEN NULL
                        ELSE AOL."MA_TK_DOI_UNG"
                        END AS "MA_TK_DOI_UNG"


                      ,SUM (CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE AOL."GHI_NO_NGUYEN_TE"
                        END) AS "GHI_NO_NGUYEN_TE"

                      ,SUM( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE AOL."GHI_NO"
                        END )AS "GHI_NO"

                      ,SUM( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE AOL."GHI_CO_NGUYEN_TE"
                        END) AS "GHI_CO_NGUYEN_TE"

                      ,SUM ( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE AOL."GHI_CO"
                        END) AS "GHI_CO"

                      ,SUM( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0
                        END) AS "DU_NO_NGUYEN_TE"

                      ,SUM( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN AOL."GHI_NO"
                        ELSE 0
                        END )AS "DU_NO"

                      ,SUM( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0
                        END) AS "DU_CO_NGUYEN_TE"

                      ,SUM( CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN AOL."GHI_CO"
                        ELSE 0
                        END) AS "DU_CO"

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE 1
                        END AS "OrderType"
                      , 0   AS "THU_TU_TRONG_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                        END AS "THU_TU_CHI_TIET_GHI_SO"


                  FROM so_cong_no_chi_tiet
                      AS AOL

                      INNER JOIN DS_KHACH_HANG
                          AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      INNER JOIN DS_CONG_TRINH LPID ON AOL."CONG_TRINH_ID" = LPID."CONG_TRINH_ID"
                      LEFT JOIN DS_CONG_TRINH_DC_CHON_CHILD PWC ON LPID."MA_PHAN_CAP" LIKE PWC."MA_PHAN_CAP"
                                                                                           || '%%'

                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id"


                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '1'


                  GROUP BY
                      PWC."MA_CONG_TRINH"

                      , PWC."TEN_CONG_TRINH"

                      , AOL."DOI_TUONG_ID"
                      , AOL."MA_DOI_TUONG"

                      , AOL."TEN_DOI_TUONG"
                      , -- Tên KH

                      AOL."NGAY_HACH_TOAN"

                      , -- Tên KH
                      CASE WHEN AOL."NGAY_CHUNG_TU" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."NGAY_CHUNG_TU"
                      END
                      , -- Ngày hạch toán


                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."SO_CHUNG_TU"
                      END
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."ID_CHUNG_TU"
                      END
                      , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn


                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."MODEL_CHUNG_TU"
                      END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                        ELSE AOL."LOAI_CHUNG_TU"
                        END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN N'Số dư đầu kỳ'

                        ELSE AOL."DIEN_GIAI_CHUNG"
                        --ELSE AOL."DIEN_GIAI_CHUNG"
                        END
                      , -- Diễn giải (lấy diễn giải Master)
                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."MA_TK_DOI_UNG"

                      END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN 0
                        ELSE 1
                        END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                        ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                        END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                        ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                        END


                     --                           , AOL."GHI_NO_NGUYEN_TE"
                     --                           , AOL."GHI_NO"
                     --                           , AOL."GHI_CO_NGUYEN_TE"
                     --                           , AOL."GHI_CO"


                 ) AS RSS
            WHERE
                RSS."GHI_NO_NGUYEN_TE" <> 0
                OR RSS."GHI_CO_NGUYEN_TE" <> 0
                OR RSS."GHI_NO" <> 0
                OR RSS."GHI_CO" <> 0
                OR "DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE" <> 0
                OR "DU_CO" - "DU_NO" <> 0


            ORDER BY
                RSS."MA_CONG_TRINH",
                RSS."TEN_CONG_TRINH",
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
                    MA_KHACH_HANG_TMP <> rec."MA_KHACH_HANG"
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    OR MA_CONG_TRINH_TMP <> rec."MA_CONG_TRINH"

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
                    MA_KHACH_HANG_TMP <> rec."MA_KHACH_HANG"
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    OR MA_CONG_TRINH_TMP <> rec."MA_CONG_TRINH"
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

        MA_KHACH_HANG_TMP = rec."MA_KHACH_HANG"
    ;

        SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
    ;


    END LOOP
    ;


END $$
;

SELECT 
    "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
    "NGAY_CHUNG_TU" as "NGAY_CHUNG_TU",
    "SO_CHUNG_TU" as "SO_CHUNG_TU",
    "DIEN_GIAI_CHUNG" as "DIEN_GIAI",
    "SO_TAI_KHOAN" as "TK_CO_ID",
    "MA_TK_DOI_UNG" as "TK_DOI_UNG",
    "GHI_NO" as "NO_SO_PHAT_SINH",
    "GHI_CO" as "CO_SO_PHAT_SINH",
    "DU_NO" as "NO_SO_DU",
    "DU_CO" as "CO_SO_DU",
    "TEN_CONG_TRINH" as "TEN_CONG_TRINH",
    "TEN_KHACH_HANG" as "TEN_KHACH_HANG",
    "ID_CHUNG_TU" as "ID_GOC",
    "MODEL_CHUNG_TU" as "MODEL_GOC"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_hop_dong(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER :=  %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    

    KHACH_HANG_IDS                        INTEGER := -1;

    HOP_DONG_IDS                          INTEGER := -1;


    rec                                   RECORD;

    SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT := 0;

    SO_TIEN_TON_TMP                       FLOAT := 0;

    DOI_TUONG_ID_TMP                      INTEGER := 0;

    SO_HOP_DONG_TMP                       VARCHAR(100) :='';


BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;


    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT
                "id" AS "KHACH_HANG_ID"

                , "LIST_MA_NHOM_KH_NCC"
                , -- Danh sách mã nhóm
                "LIST_TEN_NHOM_KH_NCC"
            -- Danh sách tên nhóm


            FROM res_partner AO
            WHERE (id = any (%(KHACH_HANG_IDS)s))  

    ;


        DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id"
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "SO_TAI_KHOAN" = so_tai_khoan
                ORDER BY
                    A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;

    ELSE
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                    A."id"
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '1'
                      AND "LA_TK_TONG_HOP" = '0'
                ORDER BY
                    A."SO_TAI_KHOAN",
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
        RowNum                   INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,


        "SO_HOP_DONG_ID"         INT
        ,
        "SO_HOP_DONG"            VARCHAR(200)

        ,
        "DOI_TUONG_ID"           INT

        ,
        "MA_KHACH_HANG"          VARCHAR(200)
        ,
        "TEN_KHACH_HANG"         VARCHAR(200)

        ,
        "NGAY_HACH_TOAN"         DATE


        , --Loại chứng từ
        "ID_CHUNG_TU"            INT
        ,
        "MODEL_CHUNG_TU"         VARCHAR(200)

        ,
        "LOAI_CHUNG_TU"          VARCHAR(200)

        ,
        "NGAY_CHUNG_TU"          DATE

        ,
        "SO_CHUNG_TU"            VARCHAR(200)
        ,
        "DIEN_GIAI"              VARCHAR(200)
        , -- Diễn giải
        "SO_TAI_KHOAN"           VARCHAR(200)
        , -- Số tài khoản
        "TINH_CHAT"              VARCHAR(200)
        , -- Tính chất tài khoản
        "MA_TK_DOI_UNG"          VARCHAR(200)

        ,
        "GHI_NO"                 FLOAT
        ,
        "GHI_NO_NGUYEN_TE"       FLOAT

        , -- Diễn giải
        "GHI_CO"                 FLOAT
        , -- Số tài khoản
        "GHI_CO_NGUYEN_TE"       FLOAT
        , -- Tính chất tài khoản
        "DU_NO"                  FLOAT

        ,
        "DU_NO_NGUYEN_TE"        FLOAT
        ,
        "DU_CO"                  FLOAT
        , -- Diễn giải
        "DU_CO_NGUYEN_TE"        FLOAT


        ,
        "THU_TU_TRONG_CHUNG_TU"  INT
        ,
        "THU_TU_CHI_TIET_GHI_SO" INT


    )
    ;

    IF v_cong_gop_but_toan_giong_nhau = 0 -- Nếu không cộng gộp
    THEN

        INSERT INTO TMP_KET_QUA
        (


            "SO_HOP_DONG_ID"
            , "SO_HOP_DONG"

            ,
            "DOI_TUONG_ID"

            ,
            "MA_KHACH_HANG"
            ,
            "TEN_KHACH_HANG"

            ,
            "NGAY_HACH_TOAN"


            , --Loại chứng từ
            "ID_CHUNG_TU"
            ,
            "MODEL_CHUNG_TU"
            ,
            "LOAI_CHUNG_TU"

            ,
            "NGAY_CHUNG_TU"

            ,
            "SO_CHUNG_TU"
            ,
            "DIEN_GIAI"
            , -- Diễn giải
            "SO_TAI_KHOAN"
            , -- Số tài khoản
            "TINH_CHAT"
            , -- Tính chất tài khoản
            "MA_TK_DOI_UNG"

            ,
            "GHI_NO"
            ,
            "GHI_NO_NGUYEN_TE"

            , -- Diễn giải
            "GHI_CO"
            , -- Số tài khoản
            "GHI_CO_NGUYEN_TE"
            , -- Tính chất tài khoản
            "DU_NO"

            ,
            "DU_NO_NGUYEN_TE"
            ,
            "DU_CO"
            , -- Diễn giải
            "DU_CO_NGUYEN_TE"


            , "THU_TU_TRONG_CHUNG_TU"
            , "THU_TU_CHI_TIET_GHI_SO"


        )

            SELECT
                RSNS."id"
                , RSNS."SO_HOP_DONG"
                , RSNS."DOI_TUONG_ID"
                , RSNS."MA_KHACH_HANG"
                , RSNS."HO_VA_TEN"
                , RSNS."NGAY_HACH_TOAN"
                , RSNS."ID_CHUNG_TU"
                , RSNS."MODEL_CHUNG_TU"
                , RSNS."LOAI_CHUNG_TU"
                , RSNS."NGAY_CHUNG_TU"
                , RSNS."SO_CHUNG_TU"
                , RSNS."DIEN_GIAI"
                , RSNS."SO_TAI_KHOAN"
                , "TINH_CHAT"
                , RSNS."MA_TAI_KHOAN_DOI_UNG"
                , SUM("GHI_NO")           AS "GHI_NO"
                , SUM("GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"

                , -- Phát sinh có
                  SUM("GHI_CO")           AS "GHI_CO"
                , -- Phát sinh nợ quy đổi
                  SUM("GHI_CO_NGUYEN_TE") AS "GHI_CO_NGUYEN_TE"


                , --Dư Nợ
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN (SUM("DU_NO")
                            - SUM("DU_CO"))
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_NO")
                                   - SUM("DU_CO")) > 0
                       THEN SUM("DU_NO")
                            - SUM("DU_CO")
                        ELSE 0
                        END
                   END)                   AS "DU_NO"

                , -- Phát sinh có quy đổi
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN SUM("DU_NO_NGUYEN_TE"
                           )
                           - SUM("DU_CO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE")
                                   - SUM("DU_CO_NGUYEN_TE")) > 0
                       THEN (SUM("DU_NO_NGUYEN_TE")
                             - SUM("DU_CO_NGUYEN_TE"))
                        ELSE 0
                        END

                   END)                   AS "DU_NO_NGUYEN_TE"

                , (CASE WHEN "TINH_CHAT" = '1'
                THEN (SUM("DU_CO")
                      - SUM("DU_NO"))
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_CO")
                                   - SUM("DU_NO")) > 0
                       THEN (SUM("DU_CO")
                             - SUM("DU_NO"))
                        ELSE 0
                        END
                   END)                   AS "DU_CO" --Dư Có quy đổi
                , (CASE WHEN "TINH_CHAT" = '1'
                THEN (SUM("DU_CO_NGUYEN_TE")
                      - SUM("DU_NO_NGUYEN_TE"))
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE")
                                   - SUM("DU_NO_NGUYEN_TE")) > 0
                       THEN (SUM("DU_CO_NGUYEN_TE")
                             - SUM("DU_NO_NGUYEN_TE"))
                        ELSE 0
                        END
                   END)                   AS "DU_CO_NGUYEN_TE"
                , RSNS."THU_TU_TRONG_CHUNG_TU"
                , RSNS."THU_TU_CHI_TIET_GHI_SO"


            FROM (SELECT

                      C."id"
                      , C."SO_HOP_DONG"

                      , GL."DOI_TUONG_ID"
                      , A."MA_KHACH_HANG"
                      , A."HO_VA_TEN"

                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."NGAY_HACH_TOAN"
                        END AS "NGAY_HACH_TOAN"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."ID_CHUNG_TU"
                        END AS "ID_CHUNG_TU"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."MODEL_CHUNG_TU"
                        END AS "MODEL_CHUNG_TU"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."LOAI_CHUNG_TU"
                        END AS "LOAI_CHUNG_TU"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE "NGAY_CHUNG_TU"
                        END AS "NGAY_CHUNG_TU"
                      , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                        CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE GL."SO_CHUNG_TU"
                        END AS "SO_CHUNG_TU"


                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                        ELSE COALESCE(GL."DIEN_GIAI",
                                      GL."DIEN_GIAI_CHUNG")
                        END AS "DIEN_GIAI"

                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE TBAN."SO_TAI_KHOAN"
                        END AS "SO_TAI_KHOAN"
                      , -- TK công nợ
                        CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE TBAN."TINH_CHAT"
                        END AS "TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE GL."MA_TAI_KHOAN_DOI_UNG"
                        END AS "MA_TAI_KHOAN_DOI_UNG"
                      , --TK đối ứng
                        CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE GL."GHI_NO"
                        END AS "GHI_NO"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."GHI_NO_NGUYEN_TE"
                        END AS "GHI_NO_NGUYEN_TE"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."GHI_CO"
                        END AS "GHI_CO"
                      , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE GL."GHI_CO_NGUYEN_TE"
                        END AS "GHI_CO_NGUYEN_TE"
                      , CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN 0
                        ELSE GL."GHI_NO"
                        END AS "DU_NO"
                      , CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                        ELSE GL."GHI_NO_NGUYEN_TE"
                        END AS "DU_NO_NGUYEN_TE"
                      , CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                        ELSE GL."GHI_CO"
                        END AS "DU_CO"
                      , CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                        ELSE GL."GHI_CO_NGUYEN_TE"
                        END AS "DU_CO_NGUYEN_TE"


                      , CASE WHEN GL."NGAY_HACH_TOAN" <= v_tu_ngay
                    THEN NULL
                        ELSE GL."THU_TU_TRONG_CHUNG_TU"
                        END AS "THU_TU_TRONG_CHUNG_TU"
                      , CASE WHEN GL."NGAY_HACH_TOAN" <= v_tu_ngay
                    THEN NULL
                        ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                        END AS "THU_TU_CHI_TIET_GHI_SO"

                  FROM sale_ex_hop_dong_ban C

                      INNER JOIN sale_ex_hop_dong_ban C2 ON C.id = C2.id
                                                            OR C2."THUOC_DU_AN_ID" = C.id
                      INNER JOIN so_cai_chi_tiet GL ON GL."HOP_DONG_BAN_ID" = C2.id

                      INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan Acc ON Acc."SO_TAI_KHOAN" = GL."MA_TAI_KHOAN"
                      INNER JOIN res_partner A ON GL."DOI_TUONG_ID" = A."id"
                      INNER JOIN danh_muc_to_chuc OU ON C."CHI_NHANH_ID" = OU."id"
                  --         LEFT JOIN dbo.CustomFieldLedger AS CFL ON GL.RefDetailID = CFL.RefDetailID
                  --         AND GL.IsPostToManagementBook = CFL.IsPostToManagementBook
                  --         AND CFL."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                  WHERE (OU."id" = v_chi_nhanh_id
                         OR (v_bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
                             AND "HACH_TOAN_SELECTION" = 'DOC_LAP'
                         )
                        )
                        AND GL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND Acc."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND Acc."DOI_TUONG_SELECTION" = '1' -- chỉ lấy tài khoản chi tiết theo khách hàng
                        AND (GL."currency_id" = v_loai_tien_id
                             OR v_loai_tien_id IS NULL
                             OR v_loai_tien_id = -1
                        )
                        AND (C.id = any (%(HOP_DONGIDS)s)) AND (A.id = any (%(KHACH_HANG_IDS)s)) 
                       


                 ) AS RSNS
            GROUP BY
                RSNS.id,
                RSNS."SO_HOP_DONG",

                RSNS."DOI_TUONG_ID",
                RSNS."MA_KHACH_HANG",
                RSNS."HO_VA_TEN",

                RSNS."NGAY_HACH_TOAN",
                RSNS."ID_CHUNG_TU",
                RSNS."MODEL_CHUNG_TU",

                RSNS."LOAI_CHUNG_TU",
                RSNS."NGAY_CHUNG_TU",
                RSNS."SO_CHUNG_TU",

                RSNS."DIEN_GIAI",

                RSNS."SO_TAI_KHOAN",
                RSNS."TINH_CHAT",
                RSNS."MA_TAI_KHOAN_DOI_UNG",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"

            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                   OR SUM("GHI_NO") <> 0
                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                   OR SUM("GHI_CO") <> 0
                   OR SUM("DU_NO_NGUYEN_TE"
                          - "DU_CO_NGUYEN_TE") <> 0
                   OR SUM("DU_NO"
                          - "DU_CO") <> 0
            ORDER BY
                RSNS."SO_HOP_DONG",
                RSNS."MA_KHACH_HANG",
                RSNS."NGAY_HACH_TOAN",
                RSNS."NGAY_CHUNG_TU",
                RSNS."SO_CHUNG_TU",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"
        ;


    ELSE

        INSERT INTO TMP_KET_QUA
        (


            "SO_HOP_DONG_ID"
            , "SO_HOP_DONG"

            ,
            "DOI_TUONG_ID"

            ,
            "MA_KHACH_HANG"
            ,
            "TEN_KHACH_HANG"

            ,
            "NGAY_HACH_TOAN"


            , --Loại chứng từ
            "ID_CHUNG_TU"
            ,
            "MODEL_CHUNG_TU"
            ,
            "LOAI_CHUNG_TU"

            ,
            "NGAY_CHUNG_TU"

            ,
            "SO_CHUNG_TU"
            ,
            "DIEN_GIAI"
            , -- Diễn giải
            "SO_TAI_KHOAN"
            , -- Số tài khoản
            "TINH_CHAT"
            , -- Tính chất tài khoản
            "MA_TK_DOI_UNG"

            ,
            "GHI_NO"
            ,
            "GHI_NO_NGUYEN_TE"

            , -- Diễn giải
            "GHI_CO"
            , -- Số tài khoản
            "GHI_CO_NGUYEN_TE"
            , -- Tính chất tài khoản
            "DU_NO"

            ,
            "DU_NO_NGUYEN_TE"
            ,
            "DU_CO"
            , -- Diễn giải
            "DU_CO_NGUYEN_TE"


            , "THU_TU_TRONG_CHUNG_TU"
            , "THU_TU_CHI_TIET_GHI_SO"


        )

            SELECT
                C."id"
                , C."SO_HOP_DONG"

                , GL."DOI_TUONG_ID"
                , A."MA_KHACH_HANG"
                , A."HO_VA_TEN"

                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."NGAY_HACH_TOAN"
                  END      AS "NGAY_HACH_TOAN"
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."ID_CHUNG_TU"
                  END      AS "ID_CHUNG_TU"
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."MODEL_CHUNG_TU"
                  END      AS "MODEL_CHUNG_TU"
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."LOAI_CHUNG_TU"
                  END      AS "LOAI_CHUNG_TU"
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE "NGAY_CHUNG_TU"
                  END      AS "NGAY_CHUNG_TU"
                , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                  CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                  ELSE GL."SO_CHUNG_TU"
                  END      AS "SO_CHUNG_TU"


                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay

                THEN N'Số dư đầu kỳ'
                  WHEN v_cong_gop_but_toan_giong_nhau = 1
                      THEN GL."DIEN_GIAI_CHUNG"
                  ELSE GL."DIEN_GIAI"
                  END      AS "DIEN_GIAI"

                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE TBAN."SO_TAI_KHOAN"
                  END      AS "SO_TAI_KHOAN"
                , -- TK công nợ
                  CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                  ELSE TBAN."TINH_CHAT"
                  END      AS "TINH_CHAT"
                , -- Tính chất tài khoản
                  CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                  ELSE GL."MA_TAI_KHOAN_DOI_UNG"
                  END      AS "MA_TAI_KHOAN_DOI_UNG"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN 0
                      ELSE GL."GHI_NO"
                      END) AS "GHI_NO"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                      ELSE GL."GHI_NO_NGUYEN_TE"
                      END) AS "GHI_NO_NGUYEN_TE"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                      ELSE GL."GHI_CO"
                      END) AS "GHI_CO"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                      ELSE GL."GHI_CO_NGUYEN_TE"
                      END) AS "GHI_CO_NGUYEN_TE"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN 0
                      ELSE GL."GHI_NO"
                      END) AS "DU_NO"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN NULL
                      ELSE GL."GHI_NO_NGUYEN_TE"
                      END) AS "DU_NO_NGUYEN_TE"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN NULL
                      ELSE GL."GHI_CO"
                      END) AS "DU_CO"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN NULL
                      ELSE GL."GHI_CO_NGUYEN_TE"
                      END) AS "DU_CO_NGUYEN_TE"
                , 0        AS "THU_TU_TRONG_CHUNG_TU"
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                  END      AS "THU_TU_CHI_TIET_GHI_SO"


            FROM sale_ex_hop_dong_ban C

                INNER JOIN sale_ex_hop_dong_ban C2 ON C.id = C2.id
                                                      OR C2."THUOC_DU_AN_ID" = C.id
                INNER JOIN so_cai_chi_tiet GL ON GL."HOP_DONG_BAN_ID" = C2.id

                INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                INNER JOIN danh_muc_he_thong_tai_khoan Acc ON Acc."SO_TAI_KHOAN" = GL."MA_TAI_KHOAN"
                INNER JOIN res_partner A ON GL."DOI_TUONG_ID" = A."id"
                INNER JOIN danh_muc_to_chuc OU ON C."CHI_NHANH_ID" = OU."id"
            --         LEFT JOIN dbo.CustomFieldLedger AS CFL ON GL.RefDetailID = CFL.RefDetailID
            --         AND GL.IsPostToManagementBook = CFL.IsPostToManagementBook
            --         AND CFL."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            WHERE (OU."id" = v_chi_nhanh_id
                   OR (v_bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
                       AND "HACH_TOAN_SELECTION" = 'DOC_LAP'
                   )
                  )
                  AND GL."NGAY_HACH_TOAN" <= v_den_ngay

                  AND Acc."CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND Acc."DOI_TUONG_SELECTION" = '1' -- chỉ lấy tài khoản chi tiết theo khách hàng
                  AND (GL."currency_id" = v_loai_tien_id
                       OR v_loai_tien_id IS NULL
                       OR v_loai_tien_id = -1
                  )
                   AND (C.id = any (%(HOP_DONGIDS)s)) AND (A.id = any (%(KHACH_HANG_IDS)s)) 
            GROUP BY
                C."id"
                , C."SO_HOP_DONG"

                , GL."DOI_TUONG_ID"
                , A."MA_KHACH_HANG"
                , A."HO_VA_TEN"

                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."NGAY_HACH_TOAN"
                  END
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."ID_CHUNG_TU"
                  END
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."MODEL_CHUNG_TU"
                  END
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."LOAI_CHUNG_TU"
                  END
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE "NGAY_CHUNG_TU"
                  END
                , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                ELSE GL."SO_CHUNG_TU"
                END


                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay

                THEN N'Số dư đầu kỳ'
                  WHEN v_cong_gop_but_toan_giong_nhau = 1
                      THEN GL."DIEN_GIAI_CHUNG"
                  ELSE GL."DIEN_GIAI"
                  END

                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE TBAN."SO_TAI_KHOAN"
                  END
                , -- TK công nợ
                CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                ELSE TBAN."TINH_CHAT"
                END
                , -- Tính chất tài khoản
                CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                ELSE GL."MA_TAI_KHOAN_DOI_UNG"
                END
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                  END


            HAVING SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN 0
                       ELSE GL."GHI_NO"
                       END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                          ELSE GL."GHI_NO_NGUYEN_TE"
                          END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                          ELSE GL."GHI_CO"
                          END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                          ELSE GL."GHI_CO_NGUYEN_TE"
                          END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN 0
                          ELSE GL."GHI_NO"
                          END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN NULL
                          ELSE GL."GHI_NO_NGUYEN_TE"
                          END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN NULL
                          ELSE GL."GHI_CO"
                          END) <> 0
                   OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                THEN NULL
                          ELSE GL."GHI_CO_NGUYEN_TE"
                          END) <> 0
            ORDER BY
                "SO_HOP_DONG",
                "MA_KHACH_HANG",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "THU_TU_CHI_TIET_GHI_SO"
        ;


    END IF
    ;


    FOR rec IN
    SELECT *
    FROM TMP_KET_QUA


    ORDER BY
        RowNum
    LOOP

        SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
            THEN COALESCE(rec."DU_NO", 0)
                 - COALESCE(rec."DU_CO", 0)
                WHEN SO_HOP_DONG_TMP <> rec."SO_HOP_DONG"
                     OR DOI_TUONG_ID_TMP <> rec."DOI_TUONG_ID"
                    THEN COALESCE(rec."GHI_NO", 0)
                         - COALESCE(rec."GHI_CO", 0)
                ELSE SO_TIEN_TON_TMP
                     + COALESCE(rec."GHI_NO", 0)
                     - COALESCE(rec."GHI_CO", 0)
                END)
        INTO SO_TIEN_TON_TMP
    ;


        rec."DU_NO" = CASE WHEN SO_TIEN_TON_TMP > 0
            THEN SO_TIEN_TON_TMP
                      ELSE 0
                      END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO" = rec."DU_NO"
        WHERE RowNum = rec.RowNum
    ;

        rec."DU_CO" = CASE WHEN SO_TIEN_TON_TMP < 0
            THEN -SO_TIEN_TON_TMP
                      ELSE 0
                      END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO" = rec."DU_CO"
        WHERE RowNum = rec.RowNum
    ;


        SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
            THEN COALESCE(rec."DU_NO_NGUYEN_TE", 0)
                 - COALESCE(rec."DU_CO_NGUYEN_TE", 0)
                WHEN SO_HOP_DONG_TMP <> rec."SO_HOP_DONG"
                     OR DOI_TUONG_ID_TMP <> rec."DOI_TUONG_ID"
                    THEN COALESCE(rec."GHI_NO_NGUYEN_TE", 0)
                         - COALESCE(rec."GHI_CO_NGUYEN_TE", 0)
                ELSE SO_TIEN_TON_NGUYEN_TE_TMP
                     + COALESCE(rec."GHI_NO_NGUYEN_TE", 0)
                     - COALESCE(rec."GHI_CO_NGUYEN_TE", 0)
                END)
        INTO SO_TIEN_TON_NGUYEN_TE_TMP
    ;


        rec."DU_NO_NGUYEN_TE" = CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
            THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                ELSE 0
                                END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;

        rec."DU_CO_NGUYEN_TE" = CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
            THEN -SO_TIEN_TON_NGUYEN_TE_TMP
                                ELSE 0
                                END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;


        SO_HOP_DONG_TMP = rec."SO_HOP_DONG"
    ;

        DOI_TUONG_ID_TMP = rec."DOI_TUONG_ID"
    ;


    END LOOP
    ;


END $$
;

SELECT 
    "SO_HOP_DONG" as "HOP_DONG_DU_AN",
    "TEN_KHACH_HANG" as "TEN_KHACH_HANG",
    "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
    "NGAY_CHUNG_TU" as "NGAY_CHUNG_TU",
    "SO_CHUNG_TU" as "SO_CHUNG_TU",
    "DIEN_GIAI" as "DIEN_GIAI",
    "SO_TAI_KHOAN" as "TK_CO_ID",
    "MA_TK_DOI_UNG" as "TK_DOI_UNG",
    "GHI_NO" as "NO_SO_PHAT_SINH",
    "GHI_CO" as "CO_SO_PHAT_SINH",
    "DU_NO" as "NO_SO_DU",
    "DU_CO" as "CO_SO_DU",
    "ID_CHUNG_TU" as "ID_GOC",
    "MODEL_CHUNG_TU" as "MODEL_GOC"

FROM TMP_KET_QUA
 WHERE   ( "ID_CHUNG_TU" IS NOT NULL
                  AND ( "GHI_NO" <> 0
                        OR "GHI_CO" <> 0
                        OR "GHI_NO_NGUYEN_TE" <> 0
                        OR "GHI_CO_NGUYEN_TE" <> 0
                      )
                )
                OR ( "ID_CHUNG_TU" IS NULL
                     AND ( "DU_NO" <> 0
                           OR "DU_CO" <> 0
                           OR "DU_NO_NGUYEN_TE" <> 0
                           OR "DU_CO_NGUYEN_TE" <> 0
                         )
                   )

OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_don_dat_hang(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_CHI_TIET_CONG_NO_PHAI_THU_KHACH_HANG
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    rec                                   RECORD;

    SO_TIEN_TON_NGUYEN_TE_TMP             FLOAT := 0;

    SO_TIEN_TON_TMP                       FLOAT := 0;

    DOI_TUONG_ID_TMP                      INTEGER := 0;

     SO_DON_HANG_ID_TMP                      INTEGER := 0;

    SO_TAI_KHOAN_TMP                       VARCHAR(100) :='';


BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;

    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT "id" AS "KHACH_HANG_ID"
            -- Danh sách tên nhóm


            FROM res_partner AO

            WHERE (id = any (%(KHACH_HANG_IDS)s)) 

    ;

    DROP TABLE IF EXISTS DS_DON_DAT_HANG
    ;

    CREATE TEMP TABLE DS_DON_DAT_HANG
        AS

            SELECT "id" AS "DON_DAT_HANG_ID"
            -- Danh sách tên nhóm


            FROM account_ex_don_dat_hang AU

            WHERE (id = any (%(DON_DAT_HANGIDS)s))  

    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

        IF so_tai_khoan IS NOT NULL
        THEN
            CREATE TEMP TABLE TMP_TAI_KHOAN
                AS
                    SELECT
                         A."id"
                        , A."SO_TAI_KHOAN"
                        , A."TEN_TAI_KHOAN"
                        , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                        , A."TINH_CHAT"
                    FROM danh_muc_he_thong_tai_khoan AS A
                    WHERE "SO_TAI_KHOAN" = so_tai_khoan
                    ORDER BY
                        A."SO_TAI_KHOAN",
                        A."TEN_TAI_KHOAN"
            ;

        ELSE
    CREATE TEMP TABLE TMP_TAI_KHOAN
        AS
            SELECT
                  A."id"
                , A."SO_TAI_KHOAN"
                , A."TEN_TAI_KHOAN"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND "DOI_TUONG_SELECTION" = '1'
                  AND "LA_TK_TONG_HOP" = '0'
            ORDER BY
                A."SO_TAI_KHOAN",
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
              RowNum INT DEFAULT NEXTVAL ('TMP_KET_QUA_seq')
                         PRIMARY KEY ,
              "DON_DAT_HANG_ID" INTEGER ,
              "SO_DON_HANG" VARCHAR(200) ,
              "NGAY_DON_HANG" DATE,
              "TINH_TRANG" VARCHAR(255),
              "DOI_TUONG_ID" INT ,
              "MA_KHACH_HANG" VARCHAR(200),
              "HO_VA_TEN" VARCHAR(200),

              "NGAY_HACH_TOAN" DATE ,
              "ID_CHUNG_TU" INTEGER,
              "MODEL_CHUNG_TU" VARCHAR(200),
              "LOAI_CHUNG_TU" INTEGER ,
              "NGAY_CHUNG_TU" DATE ,
              "SO_CHUNG_TU" VARCHAR(200),

              "DIEN_GIAI" VARCHAR(255),

              "SO_TAI_KHOAN" VARCHAR(200),
              "TINH_CHAT" VARCHAR(200) ,
              "MA_TK_DOI_UNG" VARCHAR(200),
              "GHI_NO" FLOAT ,
              "GHI_NO_NGUYEN_TE" FLOAT ,
              "GHI_CO" FLOAT ,
              "GHI_CO_NGUYEN_TE" FLOAT ,
              "DU_NO" FLOAT ,
              "DU_NO_NGUYEN_TE" FLOAT ,
              "DU_CO" FLOAT ,
              "DU_CO_NGUYEN_TE" FLOAT,

                "THU_TU_TRONG_CHUNG_TU"  INT ,

                "THU_TU_CHI_TIET_GHI_SO" INT

            );


    IF v_cong_gop_but_toan_giong_nhau = 0 -- Nếu không cộng gộp
    THEN

        INSERT  INTO TMP_KET_QUA
            ("DON_DAT_HANG_ID"  ,
              "SO_DON_HANG"  ,
              "NGAY_DON_HANG" ,
              "TINH_TRANG" ,
              "DOI_TUONG_ID"  ,
              "MA_KHACH_HANG" ,
              "HO_VA_TEN" ,

              "NGAY_HACH_TOAN"  ,
              "ID_CHUNG_TU"  ,
              "MODEL_CHUNG_TU"  ,
              "LOAI_CHUNG_TU" ,
              "NGAY_CHUNG_TU" ,
              "SO_CHUNG_TU" ,
              "DIEN_GIAI" ,
              "SO_TAI_KHOAN" ,
              "TINH_CHAT"  ,
              "MA_TK_DOI_UNG" ,
              "GHI_NO"  ,
              "GHI_NO_NGUYEN_TE" ,
              "GHI_CO",
              "GHI_CO_NGUYEN_TE" ,
              "DU_NO" ,
              "DU_NO_NGUYEN_TE"  ,
              "DU_CO"  ,
              "DU_CO_NGUYEN_TE" ,
                "THU_TU_TRONG_CHUNG_TU"  ,

                "THU_TU_CHI_TIET_GHI_SO"


            )


                SELECT
                      C."id"              AS "DON_DAT_HANG_ID"
                    , C."SO_DON_HANG"
                    , C."NGAY_DON_HANG"
                    , (CASE C."TINH_TRANG"
                       WHEN '0'
                           THEN N'Chưa thực hiện'
                       WHEN '1'
                           THEN N'Đang thực hiện'
                       WHEN '2'
                           THEN N'Hoàn thành'
                       WHEN '3'
                           THEN N'Đã hủy bỏ'
                       END)               AS "TINH_TRANG"
                    , GL."DOI_TUONG_ID"
                    , A."MA_KHACH_HANG"
                    , A."HO_VA_TEN"

                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_HACH_TOAN"
                      END                 AS "NGAY_HACH_TOAN"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."ID_CHUNG_TU"
                      END                 AS "ID_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."MODEL_CHUNG_TU"
                      END                 AS "MODEL_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."LOAI_CHUNG_TU"
                      END                 AS "LOAI_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_CHUNG_TU"
                      END                 AS "NGAY_CHUNG_TU"
                    , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                      CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE GL."SO_CHUNG_TU"
                      END                 AS "SO_CHUNG_TU"

                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                      ELSE COALESCE(GL."DIEN_GIAI",
                                    GL."DIEN_GIAI_CHUNG")
                      END                 AS "DIEN_GIAI"

                    ,
                      TBAN."SO_TAI_KHOAN" AS "SO_TAI_KHOAN"
                    , -- TK công nợ
                      CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE TBAN."TINH_CHAT"
                      END                 AS "TINH_CHAT"
                    , -- Tính chất tài khoản
                      CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE GL."MA_TK_DOI_UNG"
                      END                 AS "MA_TK_DOI_UNG"
                    , --TK đối ứng
                      SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN 0
                          ELSE GL."GHI_NO"
                          END)            AS "GHI_NO"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_NO_NGUYEN_TE"
                          END)            AS "GHI_NO_NGUYEN_TE"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_CO"
                          END)            AS "GHI_CO"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_CO_NGUYEN_TE"
                          END)            AS "GHI_CO_NGUYEN_TE"
                    , CASE WHEN ACC."TINH_CHAT" = '0'
                    THEN
                        SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                            THEN 0
                            ELSE GL."GHI_NO" - "GHI_CO"
                            END)
                      WHEN ACC."TINH_CHAT" = '1'
                          THEN 0
                      ELSE CASE WHEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                          THEN 0
                                         ELSE GL."GHI_NO" - "GHI_CO"
                                         END) > 0
                          THEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                              THEN 0
                                   ELSE GL."GHI_NO" - "GHI_CO"
                                   END)
                           ELSE 0
                           END
                      END                 AS "DU_NO"
                    , CASE WHEN ACC."TINH_CHAT" = '0'
                    THEN
                        SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                            THEN 0
                            ELSE GL."GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                            END)
                      WHEN ACC."TINH_CHAT" = '1'
                          THEN 0
                      ELSE CASE WHEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                          THEN 0
                                         ELSE GL."GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                                         END) > 0
                          THEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                              THEN 0
                                   ELSE GL."GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                                   END)
                           ELSE 0
                           END
                      END                 AS "DU_NO_NGUYEN_TE"
                    , CASE WHEN ACC."TINH_CHAT" = '0'
                    THEN 0
                      WHEN ACC."TINH_CHAT" = '1'
                          THEN
                              SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                                  THEN NULL
                                  ELSE GL."GHI_CO" - GL."GHI_NO"
                                  END)
                      ELSE CASE WHEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                          THEN NULL
                                         ELSE GL."GHI_CO" - GL."GHI_NO"
                                         END) > 0
                          THEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                              THEN NULL
                                   ELSE GL."GHI_CO" - GL."GHI_NO"
                                   END)
                           ELSE 0
                           END
                      END                 AS "DU_CO"
                    , CASE WHEN ACC."TINH_CHAT" = '0'
                    THEN 0
                      WHEN ACC."TINH_CHAT" = '1'
                          THEN
                              SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                                  THEN NULL
                                  ELSE GL."GHI_CO_NGUYEN_TE" - GL."GHI_NO_NGUYEN_TE"
                                  END)
                      ELSE CASE WHEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                          THEN NULL
                                         ELSE GL."GHI_CO_NGUYEN_TE" - GL."GHI_NO_NGUYEN_TE"
                                         END) > 0
                          THEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                              THEN NULL
                                   ELSE GL."GHI_CO_NGUYEN_TE" - GL."GHI_NO_NGUYEN_TE"
                                   END)
                           ELSE 0
                           END
                      END                 AS "DU_CO_NGUYEN_TE"
                  , CASE WHEN GL."NGAY_HACH_TOAN" <= v_tu_ngay
                    THEN NULL
                        ELSE GL."THU_TU_TRONG_CHUNG_TU"
                        END AS "THU_TU_TRONG_CHUNG_TU"
                      , CASE WHEN GL."NGAY_HACH_TOAN" <= v_tu_ngay
                    THEN NULL
                        ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                        END AS "THU_TU_CHI_TIET_GHI_SO"

                FROM account_ex_don_dat_hang C
                    INNER JOIN DS_DON_DAT_HANG F ON C.id = F."DON_DAT_HANG_ID"
                    INNER JOIN so_cong_no_chi_tiet GL ON GL."DON_DAT_HANG_ID" = C."id"

                    INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TK" LIKE TBAN."AccountNumberPercent"
                    INNER JOIN danh_muc_he_thong_tai_khoan Acc ON Acc."SO_TAI_KHOAN" = GL."MA_TK"
                    INNER JOIN res_partner A ON GL."DOI_TUONG_ID" = A."id"
                    INNER JOIN DS_KHACH_HANG F2 ON A."id" = F2."KHACH_HANG_ID"
                    INNER JOIN danh_muc_to_chuc OU ON C."CHI_NHANH_ID" = OU."id"

                WHERE (OU."id" = v_chi_nhanh_id
                       OR (v_bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
                           AND OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                       )
                      )
                      AND GL."NGAY_HACH_TOAN" <= v_den_ngay
                      AND Acc."CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND Acc."DOI_TUONG_SELECTION" = '1' -- chỉ lấy tài khoản chi tiết theo khách hàng
                      AND (GL."currency_id" = v_loai_tien_id
                           OR v_loai_tien_id IS NULL
                           OR v_loai_tien_id = -1
                      )

                      AND ("GHI_NO" <> 0 OR "GHI_CO" <> 0
                           OR "GHI_NO_NGUYEN_TE" <> 0 OR "GHI_CO_NGUYEN_TE" <> 0
                      )
                GROUP BY

                    C."id"
                    ,
                    C."SO_DON_HANG"
                    , C."NGAY_DON_HANG"
                    , (CASE C."TINH_TRANG"
                       WHEN '0'
                           THEN N'Chưa thực hiện'
                       WHEN '1'
                           THEN N'Đang thực hiện'
                       WHEN '2'
                           THEN N'Hoàn thành'
                       WHEN '3'
                           THEN N'Đã hủy bỏ'
                       END)
                    , GL."DOI_TUONG_ID"
                    , A."MA_KHACH_HANG"
                    , A."HO_VA_TEN"

                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_HACH_TOAN"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."ID_CHUNG_TU"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."MODEL_CHUNG_TU"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."LOAI_CHUNG_TU"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_CHUNG_TU"
                      END
                    , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                    CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                        THEN NULL
                    ELSE GL."SO_CHUNG_TU"
                    END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                      ELSE COALESCE(GL."DIEN_GIAI",
                                    GL."DIEN_GIAI_CHUNG")
                      END

                    ,
                    TBAN."SO_TAI_KHOAN"
                    ,
                   CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE TBAN."TINH_CHAT"
                      END

                    , -- Tính chất tài khoản
                    CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                        THEN NULL
                    ELSE GL."MA_TK_DOI_UNG"
                    END
                      , CASE WHEN GL."NGAY_HACH_TOAN" <= v_tu_ngay
                    THEN NULL
                        ELSE GL."THU_TU_TRONG_CHUNG_TU"
                        END
                      , CASE WHEN GL."NGAY_HACH_TOAN" <= v_tu_ngay
                    THEN NULL
                        ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                        END
                    ,Acc."TINH_CHAT"

                ORDER BY
                    "NGAY_DON_HANG",
                    "SO_DON_HANG",
                    "MA_KHACH_HANG",
                    "SO_TAI_KHOAN",
                    "NGAY_HACH_TOAN",
                    "NGAY_CHUNG_TU",
                    "SO_CHUNG_TU",
                     "THU_TU_TRONG_CHUNG_TU",
                    "THU_TU_CHI_TIET_GHI_SO"

        ;


    ELSE
        INSERT  INTO TMP_KET_QUA
            ("DON_DAT_HANG_ID"  ,
              "SO_DON_HANG"  ,
              "NGAY_DON_HANG" ,
              "TINH_TRANG" ,
              "DOI_TUONG_ID"  ,
              "MA_KHACH_HANG" ,
              "HO_VA_TEN" ,

              "NGAY_HACH_TOAN"  ,
              "ID_CHUNG_TU"  ,
              "MODEL_CHUNG_TU"  ,
              "LOAI_CHUNG_TU" ,
              "NGAY_CHUNG_TU" ,
              "SO_CHUNG_TU" ,
              "DIEN_GIAI" ,
              "SO_TAI_KHOAN" ,
              "TINH_CHAT"  ,
              "MA_TK_DOI_UNG" ,
              "GHI_NO"  ,
              "GHI_NO_NGUYEN_TE" ,
              "GHI_CO",
              "GHI_CO_NGUYEN_TE" ,
              "DU_NO" ,
              "DU_NO_NGUYEN_TE"  ,
              "DU_CO"  ,
              "DU_CO_NGUYEN_TE" ,
                 "THU_TU_TRONG_CHUNG_TU"  ,

                "THU_TU_CHI_TIET_GHI_SO"
            )
                SELECT
                      C."id"   AS "DON_DAT_HANG_ID"
                    , C."SO_DON_HANG"
                    , C."NGAY_DON_HANG"
                    , (CASE C."TINH_TRANG"
                       WHEN '0'
                           THEN N'Chưa thực hiện'
                       WHEN '1'
                           THEN N'Đang thực hiện'
                       WHEN '2'
                           THEN N'Hoàn thành'
                       WHEN '3'
                           THEN N'Đã hủy bỏ'
                       END)    AS "TINH_TRANG"
                    , GL."DOI_TUONG_ID"
                    , A."MA_KHACH_HANG"
                    , A."HO_VA_TEN"

                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_HACH_TOAN"
                      END      AS "NGAY_HACH_TOAN"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."ID_CHUNG_TU"
                      END      AS "ID_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."MODEL_CHUNG_TU"
                      END      AS "MODEL_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."LOAI_CHUNG_TU"
                      END      AS "LOAI_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_CHUNG_TU"
                      END      AS "NGAY_CHUNG_TU"
                    , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                      CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE GL."SO_CHUNG_TU"
                      END      AS "SO_CHUNG_TU"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                      WHEN v_cong_gop_but_toan_giong_nhau = 1
                          THEN GL."DIEN_GIAI_CHUNG"
                      ELSE GL."DIEN_GIAI"
                      END      AS "DIEN_GIAI"

                    , TBAN."SO_TAI_KHOAN"
                    , -- TK công nợ,
                      CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE TBAN."TINH_CHAT"
                      END      AS "TINH_CHAT"
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."MA_TK_DOI_UNG"
                      END
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                          ELSE GL."GHI_NO"
                          END) AS "GHI_NO"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_NO_NGUYEN_TE"
                          END) AS "GHI_NO_NGUYEN_TE"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_CO"
                          END) AS "GHI_CO"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_CO_NGUYEN_TE"
                          END) AS "GHI_CO_NGUYEN_TE"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN 0
                          ELSE GL."GHI_NO"
                          END) AS "DU_NO"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_NO_NGUYEN_TE"
                          END) AS "DU_NO_NGUYEN_TE"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_CO"
                          END) AS "DU_CO"
                    , SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                          ELSE GL."GHI_CO_NGUYEN_TE"
                          END) AS "DU_CO_NGUYEN_TE"
                 , 0        AS "THU_TU_TRONG_CHUNG_TU"
                , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
                  ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                  END      AS "THU_TU_CHI_TIET_GHI_SO"


                FROM account_ex_don_dat_hang C
                    INNER JOIN DS_DON_DAT_HANG F ON C.id = F."DON_DAT_HANG_ID"
                    INNER JOIN so_cong_no_chi_tiet GL ON GL."DON_DAT_HANG_ID" = C."id"

                    INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TK" LIKE TBAN."AccountNumberPercent"
                    INNER JOIN danh_muc_he_thong_tai_khoan Acc ON Acc."id" = GL."TK_ID"
                    INNER JOIN res_partner A ON GL."DOI_TUONG_ID" = A."id"
                    INNER JOIN DS_KHACH_HANG F2 ON A."id" = F2."KHACH_HANG_ID"
                    INNER JOIN danh_muc_to_chuc OU ON C."CHI_NHANH_ID" = OU."id"

                WHERE (OU."id" = v_chi_nhanh_id
                       OR (v_bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
                           AND OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                       )
                      )
                      AND GL."NGAY_HACH_TOAN" <= v_den_ngay
                      AND Acc."CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND Acc."DOI_TUONG_SELECTION" = '1' -- chỉ lấy tài khoản chi tiết theo khách hàng
                      AND (GL."currency_id" = v_loai_tien_id
                           OR v_loai_tien_id IS NULL
                           OR v_loai_tien_id = -1
                      )


                GROUP BY
                    C."id"
                    ,
                    C."SO_DON_HANG"
                    , C."NGAY_DON_HANG"
                    , (CASE C."TINH_TRANG"
                       WHEN '0'
                           THEN N'Chưa thực hiện'
                       WHEN '1'
                           THEN N'Đang thực hiện'
                       WHEN '2'
                           THEN N'Hoàn thành'
                       WHEN '3'
                           THEN N'Đã hủy bỏ'
                       END)
                    , GL."DOI_TUONG_ID"
                    , A."MA_KHACH_HANG"
                    , A."HO_VA_TEN"


                     , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_HACH_TOAN"
                      END

                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."ID_CHUNG_TU"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."MODEL_CHUNG_TU"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."LOAI_CHUNG_TU"
                      END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."NGAY_CHUNG_TU"
                      END
                    , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                    CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                        THEN NULL
                    ELSE GL."SO_CHUNG_TU"
                    END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                      WHEN v_cong_gop_but_toan_giong_nhau = 1
                          THEN GL."DIEN_GIAI_CHUNG"
                      ELSE GL."DIEN_GIAI"
                      END

                    ,
                    TBAN."SO_TAI_KHOAN"
                    , -- TK công nợ,
                    CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                        THEN NULL
                    ELSE TBAN."TINH_CHAT"
                    END
                    , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."MA_TK_DOI_UNG"
                      END
                     , CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                      ELSE GL."THU_TU_CHI_TIET_GHI_SO"
                      END

                HAVING SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                           ELSE GL."GHI_NO"
                           END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                              ELSE GL."GHI_NO_NGUYEN_TE"
                              END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                              ELSE GL."GHI_CO"
                              END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                              ELSE GL."GHI_CO_NGUYEN_TE"
                              END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN 0
                              ELSE GL."GHI_NO"
                              END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                              ELSE GL."GHI_NO_NGUYEN_TE"
                              END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                              ELSE GL."GHI_CO"
                              END) <> 0
                       OR SUM(CASE WHEN GL."NGAY_HACH_TOAN" >= v_tu_ngay
                    THEN NULL
                              ELSE GL."GHI_CO_NGUYEN_TE"
                              END) <> 0
                ORDER BY

                    "NGAY_DON_HANG",
                    "SO_DON_HANG",
                    "MA_KHACH_HANG",
                    TBAN."SO_TAI_KHOAN",
                    "NGAY_HACH_TOAN",
                    "NGAY_CHUNG_TU",
                    "SO_CHUNG_TU",
                    "THU_TU_CHI_TIET_GHI_SO"
        ;


    END IF
    ;

 FOR rec IN
    SELECT *
    FROM TMP_KET_QUA


    ORDER BY
        RowNum
    LOOP

        SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
            THEN COALESCE(rec."DU_NO", 0)
                 - COALESCE(rec."DU_CO", 0)
                WHEN SO_DON_HANG_ID_TMP  <> rec."DON_DAT_HANG_ID"
                     OR DOI_TUONG_ID_TMP <> rec."DOI_TUONG_ID"
                     OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    THEN COALESCE(rec."GHI_NO", 0)
                         - COALESCE(rec."GHI_CO", 0)
                ELSE SO_TIEN_TON_TMP
                     + COALESCE(rec."GHI_NO", 0)
                     - COALESCE(rec."GHI_CO", 0)
                END)
        INTO SO_TIEN_TON_TMP
    ;


        rec."DU_NO" = CASE WHEN SO_TIEN_TON_TMP > 0
            THEN SO_TIEN_TON_TMP
                      ELSE 0
                      END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO" = rec."DU_NO"
        WHERE RowNum = rec.RowNum
    ;

        rec."DU_CO" = CASE WHEN SO_TIEN_TON_TMP < 0
            THEN -SO_TIEN_TON_TMP
                      ELSE 0
                      END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO" = rec."DU_CO"
        WHERE RowNum = rec.RowNum
    ;


        SELECT (CASE WHEN rec."ID_CHUNG_TU" IS NULL
            THEN COALESCE(rec."DU_NO_NGUYEN_TE", 0)
                 - COALESCE(rec."DU_CO_NGUYEN_TE", 0)
                WHEN SO_DON_HANG_ID_TMP  <> rec."DON_DAT_HANG_ID"
                     OR DOI_TUONG_ID_TMP <> rec."DOI_TUONG_ID"
                     OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    THEN COALESCE(rec."GHI_NO_NGUYEN_TE", 0)
                         - COALESCE(rec."GHI_CO_NGUYEN_TE", 0)
                ELSE SO_TIEN_TON_NGUYEN_TE_TMP
                     + COALESCE(rec."GHI_NO_NGUYEN_TE", 0)
                     - COALESCE(rec."GHI_CO_NGUYEN_TE", 0)
                END)
        INTO SO_TIEN_TON_NGUYEN_TE_TMP
    ;


        rec."DU_NO_NGUYEN_TE" = CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP > 0
            THEN SO_TIEN_TON_NGUYEN_TE_TMP
                                ELSE 0
                                END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;

        rec."DU_CO_NGUYEN_TE" = CASE WHEN SO_TIEN_TON_NGUYEN_TE_TMP < 0
            THEN -SO_TIEN_TON_NGUYEN_TE_TMP
                                ELSE 0
                                END
    ;

        UPDATE TMP_KET_QUA
        SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
        WHERE RowNum = rec.RowNum
    ;


        SO_DON_HANG_ID_TMP = rec."DON_DAT_HANG_ID"
    ;

        DOI_TUONG_ID_TMP = rec."DOI_TUONG_ID"
    ;
        SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
    ;


    END LOOP
    ;


END $$
;

SELECT 
    "NGAY_DON_HANG" as "NGAY_DON_HANG",
    "HO_VA_TEN" as "TEN_KHACH_HANG",
    "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
    "NGAY_CHUNG_TU" as "NGAY_CHUNG_TU",
    "SO_CHUNG_TU" as "SO_CHUNG_TU",
    "DIEN_GIAI" as "DIEN_GIAI",
    "SO_TAI_KHOAN" as "TK_CO_ID",
    "MA_TK_DOI_UNG" as "TK_DOI_UNG",
    "GHI_NO" as "NO_SO_PHAT_SINH",
    "GHI_CO" as "CO_SO_PHAT_SINH",
    "DU_NO" as "NO_SO_DU",
    "DU_CO" as "CO_SO_DU",
    "SO_DON_HANG" as "SO_DON_HANG",
    "ID_CHUNG_TU" as "ID_GOC",
    "MODEL_CHUNG_TU" as "MODEL_GOC"
FROM TMP_KET_QUA
WHERE ("ID_CHUNG_TU" IS NOT NULL
       AND ("GHI_NO" <> 0
            OR "GHI_CO" <> 0
            OR "GHI_NO_NGUYEN_TE" <> 0
            OR "GHI_CO_NGUYEN_TE" <> 0
       )
      )
      OR ("ID_CHUNG_TU" IS NULL
          AND ("DU_NO" <> 0
               OR "DU_CO" <> 0
               OR "DU_NO_NGUYEN_TE" <> 0
               OR "DU_CO_NGUYEN_TE" <> 0
          )
      )

OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_don_vi_kinh_doanh(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_CHI_TIET_CONG_NO_PHAI_THU_KHACH_HANG
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    



    rec                                   RECORD;

    CHE_DO_KE_TOAN                        VARCHAR(100);



    SO_TIEN_TON_NGUYEN_TE                  FLOAT := 0;

    SO_TIEN_TON                           FLOAT := 0;

    MA_DON_VI_TMP                         VARCHAR(100) :=N'';

    MA_DOI_TUONG_TMP                      VARCHAR(100) :=N'';

    SO_TAI_KHOAN_TMP                       VARCHAR(100) :=N'';


BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


        DROP TABLE IF EXISTS DS_KHACH_HANG
        ;

        IF (%(KHACH_HANG_IDS)s) IS NULL
        THEN
            CREATE TEMP TABLE DS_KHACH_HANG
                AS
                    SELECT
                          "id"                  AS "KHACH_HANG_ID"

                        , "LIST_MA_NHOM_KH_NCC"
                        , "LIST_TEN_NHOM_KH_NCC"

                    FROM res_partner
                    WHERE "LA_KHACH_HANG" = '1'
            ;
        ELSE
    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT
                "id" AS "KHACH_HANG_ID"

                , "LIST_MA_NHOM_KH_NCC"
                , "LIST_TEN_NHOM_KH_NCC"


            FROM res_partner
            WHERE (id = any (%(KHACH_HANG_IDS)s)) 
    ;

        END IF
        ;

    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;

    DROP TABLE IF EXISTS TMP_DON_VI
    ;

    CREATE TEMP TABLE TMP_DON_VI
        AS
            SELECT DISTINCT
                  EI."id" AS "DON_VI_ID"
                , EI."MA_PHAN_CAP"
                , EI."MA_DON_VI"
                , EI."TEN_DON_VI"
                , EI."ISPARENT"

                , 0       AS "IsParentWithChild"
            FROM danh_muc_to_chuc AS EI
            WHERE (id = any (%(DV_KINH_DOANH_IDS)s))
    ;

    UPDATE TMP_DON_VI
    SET "IsParentWithChild" = '1'
    FROM TMP_DON_VI T
        INNER JOIN TMP_DON_VI T1
            ON T1."MA_PHAN_CAP" LIKE concat(T."MA_PHAN_CAP", '%%') AND T."MA_PHAN_CAP" <> T1."MA_PHAN_CAP"
    WHERE T."ISPARENT" = '1'
    ;

    DROP TABLE IF EXISTS TMP_DON_VI_1
    ;

    CREATE TEMP TABLE TMP_DON_VI_1
        AS
            SELECT
                S."DON_VI_ID"
                , S."MA_PHAN_CAP"
            FROM TMP_DON_VI S
                LEFT JOIN TMP_DON_VI S1 ON S1."MA_PHAN_CAP" LIKE S."MA_PHAN_CAP" || '%%'
                                           AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
            WHERE S1."MA_PHAN_CAP" IS NULL
    ;

    DROP TABLE IF EXISTS DS_DON_VI
    ;

    CREATE TEMP TABLE DS_DON_VI
        AS
            SELECT DISTINCT
                T."DON_VI_ID"
                , T."MA_PHAN_CAP"
            FROM (SELECT DISTINCT
                      EI."id" AS "DON_VI_ID"
                      , EI."MA_PHAN_CAP"
                  FROM danh_muc_to_chuc EI
                      INNER JOIN TMP_DON_VI_1 SEI ON EI."MA_PHAN_CAP" LIKE SEI."MA_PHAN_CAP" || '%%'
                  UNION ALL
                  SELECT
                      EI."DON_VI_ID"
                      , EI."MA_PHAN_CAP"
                  FROM TMP_DON_VI EI
                 ) T
    ;


        DROP TABLE IF EXISTS TMP_TAI_KHOAN
        ;

            IF so_tai_khoan IS NOT NULL
            THEN
                CREATE TEMP TABLE TMP_TAI_KHOAN
                    AS
                        SELECT
                               A."id"
                            , A."SO_TAI_KHOAN"
                            , A."TEN_TAI_KHOAN"
                            , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                            , A."TINH_CHAT"
                        FROM danh_muc_he_thong_tai_khoan AS A
                        WHERE "SO_TAI_KHOAN" = so_tai_khoan
                        ORDER BY
                            A."SO_TAI_KHOAN",
                            A."TEN_TAI_KHOAN"
                ;

            ELSE
    CREATE TEMP TABLE TMP_TAI_KHOAN
        AS
            SELECT
                A."id"
                , A."SO_TAI_KHOAN"
                , A."TEN_TAI_KHOAN"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND "DOI_TUONG_SELECTION" = '1'
                  AND "LA_TK_TONG_HOP" = '0'
            ORDER BY
                A."SO_TAI_KHOAN",
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
        RowNum             INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,
        "DON_VI_ID"        INTEGER,
        "MA_DON_VI"        VARCHAR(127),
        "TEN_DON_VI"       VARCHAR(200),

        "DOI_TUONG_ID"     INTEGER,
        "MA_DOI_TUONG"    VARCHAR(200),
        "TEN_DOI_TUONG"    VARCHAR(200),

        "NGAY_HACH_TOAN"   TIMESTAMP(3),
        "NGAY_CHUNG_TU"    TIMESTAMP(3),
        "SO_CHUNG_TU"      VARCHAR(200),
        "LOAI_CHUNG_TU"    INTEGER,
        "ID_CHUNG_TU"      INTEGER,
        "MODEL_CHUNG_TU"   VARCHAR(200),
        "DIEN_GIAI"        VARCHAR(255),

        "SO_TAI_KHOAN"     VARCHAR(200),
        "TINH_CHAT"         VARCHAR(200),
        "MA_TK_DOI_UNG"     VARCHAR(200),
        "GHI_NO_NGUYEN_TE" DECIMAL(22, 8),
        "GHI_NO"           DECIMAL(22, 8),
        "GHI_CO_NGUYEN_TE" DECIMAL(22, 8),
        "GHI_CO"           DECIMAL(22, 8),
        "DU_NO_NGUYEN_TE"  DECIMAL(22, 8),
        "DU_NO"            DECIMAL(22, 8),
        "DU_CO_NGUYEN_TE"  DECIMAL(22, 8),
        "DU_CO"            DECIMAL(22, 8),
        "OrderType"        INTEGER


    )
    ;


    IF v_cong_gop_but_toan_giong_nhau = 0 -- Nếu không cộng gộp
    THEN

        INSERT INTO TMP_KET_QUA
        ("DON_VI_ID",
         "MA_DON_VI",
         "TEN_DON_VI",

         "DOI_TUONG_ID",
         "MA_DOI_TUONG",
         "TEN_DOI_TUONG",

         "NGAY_HACH_TOAN",
         "NGAY_CHUNG_TU",
         "SO_CHUNG_TU",
         "LOAI_CHUNG_TU",
         "ID_CHUNG_TU",
         "MODEL_CHUNG_TU",


         "DIEN_GIAI",
         "SO_TAI_KHOAN",
         "TINH_CHAT",
         "MA_TK_DOI_UNG",
         "GHI_NO_NGUYEN_TE",
         "GHI_NO",
         "GHI_CO_NGUYEN_TE",
         "GHI_CO",
         "DU_NO_NGUYEN_TE",
         "DU_NO",
         "DU_CO_NGUYEN_TE",
         "DU_CO",
         "OrderType"
        )


            SELECT

                P."DON_VI_ID"
                , "MA_DON_VI"
                , "TEN_DON_VI"
                , "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , "TEN_DOI_TUONG"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"

                , "SO_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"


                , "DIEN_GIAI"
                , "SO_TAI_KHOAN"
                , "TINH_CHAT"
                , "MA_TK_DOI_UNG"

                , SUM("GHI_NO_NGUYEN_TE")
                , -- Phát sinh nợ
                SUM("GHI_NO")
                , -- Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE")
                , -- Phát sinh có
                SUM("GHI_CO")
                , -- Phát sinh có quy đổi
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN (SUM("DU_NO_NGUYEN_TE")
                          - SUM("DU_CO_NGUYEN_TE"))
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_NO_NGUYEN_TE")
                                 - SUM("DU_CO_NGUYEN_TE")) > 0
                     THEN (SUM("DU_NO_NGUYEN_TE")
                           - SUM("DU_CO_NGUYEN_TE"))
                      ELSE 0
                      END
                 END) AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                (CASE WHEN "TINH_CHAT" = '0'
                    THEN (SUM("DU_NO")
                          - SUM("DU_CO"))
                 WHEN "TINH_CHAT" = '1'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_NO")
                                 - SUM("DU_CO")) > 0
                     THEN SUM("DU_NO")
                          - SUM("DU_CO")
                      ELSE 0
                      END
                 END) AS "DU_NO"
                , --Dư Nợ Quy đổi
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("DU_CO_NGUYEN_TE")
                          - SUM("DU_NO_NGUYEN_TE"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_CO_NGUYEN_TE")
                                 - SUM("DU_NO_NGUYEN_TE")) > 0
                     THEN (SUM("DU_CO_NGUYEN_TE")
                           - SUM("DU_NO_NGUYEN_TE"))
                      ELSE 0
                      END
                 END) AS "DU_CO_NGUYEN_TE"
                , --Dư Có
                (CASE WHEN "TINH_CHAT" = '1'
                    THEN (SUM("DU_CO")
                          - SUM("DU_NO"))
                 WHEN "TINH_CHAT" = '0'
                     THEN 0
                 ELSE CASE WHEN (SUM("DU_CO")
                                 - SUM("DU_NO")) > 0
                     THEN (SUM("DU_CO")
                           - SUM("DU_NO"))
                      ELSE 0
                      END
                 END) AS "DU_CO" --Dư Có quy đổi
                , "OrderType"

            FROM (
                     SELECT
                         OU."DON_VI_ID"
                         , OU."MA_PHAN_CAP"
                         , AOL."DOI_TUONG_ID"
                         , AOL."MA_DOI_TUONG"
                         , -- Mã khách hàng
                         AOL."TEN_DOI_TUONG"

                         , -- Địa chỉ
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN NULL
                           ELSE AOL."NGAY_HACH_TOAN"
                           END AS "NGAY_HACH_TOAN"
                         , -- Ngày hạch toán

                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN NULL
                           ELSE "NGAY_CHUNG_TU"
                           END AS "NGAY_CHUNG_TU"
                         , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN NULL
                           ELSE AOL."SO_CHUNG_TU"
                           END AS "SO_CHUNG_TU"


                         , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN NULL
                           ELSE AOL."ID_CHUNG_TU"
                           END AS "ID_CHUNG_TU"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN NULL
                           ELSE AOL."MODEL_CHUNG_TU"
                           END AS "MODEL_CHUNG_TU"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN NULL
                           ELSE AOL."LOAI_CHUNG_TU"
                           END AS "LOAI_CHUNG_TU"

                         , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN N'Số dư đầu kỳ'
                           ELSE COALESCE(AOL."DIEN_GIAI",
                                         AOL."DIEN_GIAI_CHUNG")
                           END AS "DIEN_GIAI"
                         , -- Diễn giải (lấy diễn giải Detail, nếu null thì lấy diễn giải master)
                         TBAN."SO_TAI_KHOAN"
                         , -- TK công nợ
                         TBAN."TINH_CHAT"
                         , -- Tính chất tài khoản
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN NULL
                           ELSE AOL."MA_TK_DOI_UNG"
                           END AS "MA_TK_DOI_UNG"


                         , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN 0
                           ELSE (AOL."GHI_NO_NGUYEN_TE")
                           END AS "GHI_NO_NGUYEN_TE"
                         , -- Phát sinh nợ
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN 0
                           ELSE (AOL."GHI_NO")
                           END AS "GHI_NO"
                         , -- Phát sinh nợ quy đổi
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN 0
                           ELSE (AOL."GHI_CO_NGUYEN_TE")
                           END AS "GHI_CO_NGUYEN_TE"
                         , -- Phát sinh có
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN 0
                           ELSE (AOL."GHI_CO")
                           END AS "GHI_CO"
                         , -- Phát sinh có quy đổi
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN AOL."GHI_NO_NGUYEN_TE"
                           ELSE 0
                           END AS "DU_NO_NGUYEN_TE"
                         , --Dư Nợ
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN AOL."GHI_NO"
                           ELSE 0
                           END AS "DU_NO"
                         , --Dư Nợ Quy đổi
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN AOL."GHI_CO_NGUYEN_TE"
                           ELSE 0
                           END AS "DU_CO_NGUYEN_TE"
                         , --Dư Có
                           CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                               THEN AOL."GHI_CO"
                           ELSE 0
                           END AS "DU_CO"
                         , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN 0
                           ELSE 1
                           END AS "OrderType"
                        , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                                 THEN NULL
                                                 ELSE AOL."THU_TU_TRONG_CHUNG_TU"
                                            END AS "THU_TU_TRONG_CHUNG_TU"
                        ,CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                             THEN NULL
                             ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                        END AS "THU_TU_CHI_TIET_GHI_SO"

                     FROM so_cong_no_chi_tiet AS AOL
                         INNER JOIN DS_KHACH_HANG
                             AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                         INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                         INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                         INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                         INNER JOIN TMP_DON_VI OU ON AOL."DON_VI_ID" = OU."DON_VI_ID"
                         LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT

                     WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                           AND (v_loai_tien_id IS NULL
                                OR AOL."currency_id" = v_loai_tien_id
                           )
                           AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                           AND AN."DOI_TUONG_SELECTION" = '1'
                           AND (OU."DON_VI_ID" IS NOT NULL
                                OR ((%(DV_KINH_DOANH_IDS)s) IS NULL
                                    AND AOL."DON_VI_ID" IS NULL
                                )
                           )
                 ) AS RSNS
                INNER JOIN TMP_DON_VI P ON ((P."ISPARENT" = '0'
                                             OR P."IsParentWithChild" = 1
                                            )
                                            AND RSNS."DON_VI_ID" = P."DON_VI_ID"
                                           )
                                           OR (P."ISPARENT" = '1'
                                               AND P."IsParentWithChild" = 0
                                               AND RSNS."MA_PHAN_CAP" LIKE P."MA_PHAN_CAP"
                                                                           || '%%'
                                           )


            GROUP BY
                RSNS."TEN_DOI_TUONG", -- Tên khách hàng
                RSNS."MA_DOI_TUONG", -- Mã khách hàng

                P."DON_VI_ID",
                P."MA_DON_VI",
                P."TEN_DON_VI",
                RSNS."DOI_TUONG_ID",

                RSNS."NGAY_HACH_TOAN", -- Ngày hạch toán
                RSNS."NGAY_CHUNG_TU", -- Ngày chứng từ
                RSNS."SO_CHUNG_TU", -- Số chứng từ

                RSNS."LOAI_CHUNG_TU", --Loại chứng từ
                RSNS."ID_CHUNG_TU", -- Mã chứng từ
                RSNS."MODEL_CHUNG_TU", -- Mã chứng từ

                RSNS."DIEN_GIAI", -- Diễn giải
                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT", -- Tính chất tài khoản
                RSNS."MA_TK_DOI_UNG", --TK đối ứng
                RSNS."OrderType",
                RSNS."THU_TU_TRONG_CHUNG_TU",
                RSNS."THU_TU_CHI_TIET_GHI_SO"

            HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                   OR SUM("GHI_NO") <> 0
                   OR SUM("GHI_CO_NGUYEN_TE") <> 0
                   OR SUM("GHI_CO") <> 0
                   OR SUM("DU_NO_NGUYEN_TE"
                          - "DU_CO_NGUYEN_TE") <> 0
                   OR SUM("DU_NO"
                          - "DU_CO") <> 0
            ORDER BY
                P."MA_DON_VI",
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
        ("DON_VI_ID",
         "MA_DON_VI",
         "TEN_DON_VI",

         "DOI_TUONG_ID",
         "MA_DOI_TUONG",
         "TEN_DOI_TUONG",

         "NGAY_HACH_TOAN",
         "NGAY_CHUNG_TU",
         "SO_CHUNG_TU",
         "LOAI_CHUNG_TU",
         "ID_CHUNG_TU",
         "MODEL_CHUNG_TU",


         "DIEN_GIAI",
         "SO_TAI_KHOAN",
         "TINH_CHAT",
         "MA_TK_DOI_UNG",
         "GHI_NO_NGUYEN_TE",
         "GHI_NO",
         "GHI_CO_NGUYEN_TE",
         "GHI_CO",
         "DU_NO_NGUYEN_TE",
         "DU_NO",
         "DU_CO_NGUYEN_TE",
         "DU_CO",
         "OrderType"
        )
            SELECT
                P."DON_VI_ID"
                , "MA_DON_VI"
                , "TEN_DON_VI"
                , "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , "TEN_DOI_TUONG"
                , "NGAY_HACH_TOAN"
                , "NGAY_CHUNG_TU"

                , "SO_CHUNG_TU"
                , "LOAI_CHUNG_TU"
                , "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"


                , "DIEN_GIAI"
                , "SO_TAI_KHOAN"
                , "TINH_CHAT"
                , "MA_TK_DOI_UNG"
                ,"GHI_NO_NGUYEN_TE"
                , -- Phát sinh nợ
                "GHI_NO"
                , -- Phát sinh nợ quy đổi
                "GHI_CO_NGUYEN_TE"
                , -- Phát sinh có
                "GHI_CO"
                , -- Phát sinh có quy đổi
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN ("DU_NO_NGUYEN_TE"
                            - "DU_CO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN ("DU_NO_NGUYEN_TE"
                                   - "DU_CO_NGUYEN_TE") > 0
                       THEN "DU_NO_NGUYEN_TE"
                            - "DU_CO_NGUYEN_TE"
                        ELSE 0
                        END
                   END) AS "DU_NO_NGUYEN_TE"
                , --Dư Nợ
                  (CASE WHEN "TINH_CHAT" = '0'
                      THEN ("DU_NO"
                            - "DU_CO")
                   WHEN "TINH_CHAT" = '1'
                       THEN 0
                   ELSE CASE WHEN ("DU_NO"
                                   - "DU_CO") > 0
                       THEN "DU_NO"
                            - "DU_CO"
                        ELSE 0
                        END
                   END) AS "DU_NO"
                , --Dư Nợ Quy đổi
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN ("DU_CO_NGUYEN_TE"
                            - "DU_NO_NGUYEN_TE")
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN ("DU_CO_NGUYEN_TE"
                                   - "DU_NO_NGUYEN_TE") > 0
                       THEN ("DU_CO_NGUYEN_TE"
                             - "DU_NO_NGUYEN_TE")
                        ELSE 0
                        END
                   END) AS "DU_CO_NGUYEN_TE"
                , --Dư Có
                  (CASE WHEN "TINH_CHAT" = '1'
                      THEN ("DU_CO"
                            - "DU_NO")
                   WHEN "TINH_CHAT" = '0'
                       THEN 0
                   ELSE CASE WHEN ("DU_CO"
                                   - "DU_NO") > 0
                       THEN ("DU_CO"
                             - "DU_NO")
                        ELSE 0
                        END
                   END) AS "DU_CO" --Dư Có quy đổi
                , "OrderType"

            FROM (SELECT
                      OU."DON_VI_ID"
                      , OU."MA_PHAN_CAP"
                      , AOL."DOI_TUONG_ID"
                      , AOL."MA_DOI_TUONG"
                      , -- Mã khách hàng
                      AOL."TEN_DOI_TUONG"

                      , -- Địa chỉ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."NGAY_HACH_TOAN"
                        END      AS "NGAY_HACH_TOAN"
                      , -- Ngày hạch toán

                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE "NGAY_CHUNG_TU"
                        END      AS "NGAY_CHUNG_TU"
                      , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."SO_CHUNG_TU"
                        END      AS "SO_CHUNG_TU"


                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."ID_CHUNG_TU"
                        END      AS "ID_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."MODEL_CHUNG_TU"
                        END      AS "MODEL_CHUNG_TU"
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN NULL
                        ELSE AOL."LOAI_CHUNG_TU"
                        END      AS "LOAI_CHUNG_TU"

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN N'Số dư đầu kỳ'
                        ELSE
                            AOL."DIEN_GIAI_CHUNG"
                        END      AS "DIEN_GIAI"
                      , -- Diễn giải (lấy diễn giải Detail, nếu null thì lấy diễn giải master)
                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN NULL
                        ELSE AOL."MA_TK_DOI_UNG"
                        END      AS "MA_TK_DOI_UNG"

                      , --Tỷ giá
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                            ELSE (AOL."GHI_NO_NGUYEN_TE")
                            END) AS "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                            ELSE (AOL."GHI_NO")
                            END) AS "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                            ELSE (AOL."GHI_CO_NGUYEN_TE")
                            END) AS "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                            ELSE (AOL."GHI_CO")
                            END) AS "GHI_CO"
                      , -- Phát sinh có quy đổi
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO_NGUYEN_TE"
                            ELSE 0
                            END) AS "DU_NO_NGUYEN_TE"
                      , --Dư Nợ
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO"
                            ELSE 0
                            END) AS "DU_NO"
                      , --Dư Nợ Quy đổi
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO_NGUYEN_TE"
                            ELSE 0
                            END) AS "DU_CO_NGUYEN_TE"
                      , --Dư Có
                        SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO"
                            ELSE 0
                            END) AS "DU_CO" --Dư Có quy đổi
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                    THEN 0
                        ELSE 1
                        END      AS "OrderType"
                        , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                                 THEN NULL
                                                 ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                                            END AS "THU_TU_CHI_TIET_GHI_SO"

                  FROM so_cong_no_chi_tiet AS AOL
                      INNER JOIN DS_KHACH_HANG
                          AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      INNER JOIN TMP_DON_VI OU ON AOL."DON_VI_ID" = OU."DON_VI_ID"
                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT

                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '1'
                        AND (OU."DON_VI_ID" IS NOT NULL
                             OR ((%(DV_KINH_DOANH_IDS)s) IS NULL
                                 AND AOL."DON_VI_ID" IS NULL
                             )
                        )
                  GROUP BY
                      AOL."TEN_DOI_TUONG"
                      , AOL."MA_DOI_TUONG"
                      , OU."DON_VI_ID"
                      , OU."MA_PHAN_CAP"
                      , AOL."DOI_TUONG_ID"
                      , -- Địa chỉ

                       CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE "NGAY_HACH_TOAN"
                      END

                      , -- Ngày hạch toán

                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE "NGAY_CHUNG_TU"
                      END
                      , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."SO_CHUNG_TU"
                      END


                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                        ELSE AOL."ID_CHUNG_TU"
                        END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                        ELSE AOL."MODEL_CHUNG_TU"
                        END
                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN NULL
                        ELSE AOL."LOAI_CHUNG_TU"
                        END

                      , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                      THEN N'Số dư đầu kỳ'
                        ELSE
                            AOL."DIEN_GIAI_CHUNG"
                        END
                      , -- Diễn giải (lấy diễn giải Detail, nếu null thì lấy diễn giải master)
                      TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN NULL
                      ELSE AOL."MA_TK_DOI_UNG"
                      END
                      ,  CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                                                 THEN 0
                                                 ELSE 1
                                            END
                    , CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                         THEN NULL
                         ELSE AOL."THU_TU_CHI_TIET_GHI_SO"
                      END
                 ) AS RSS
                INNER JOIN TMP_DON_VI P ON ((P."ISPARENT" = '0'
                                             OR P."IsParentWithChild" = 1
                                            )
                                            AND RSS."DON_VI_ID" = P."DON_VI_ID"
                                           )
                                           OR (P."ISPARENT" = '1'
                                               AND P."IsParentWithChild" = 0
                                               AND RSS."MA_PHAN_CAP" LIKE P."MA_PHAN_CAP"
                                                                           || '%%'
                                           )
            WHERE
                RSS."GHI_NO_NGUYEN_TE" <> 0
                OR RSS."GHI_CO_NGUYEN_TE" <> 0
                OR RSS."GHI_NO" <> 0
                OR RSS."GHI_CO" <> 0
                OR "DU_CO_NGUYEN_TE"
                   - "DU_NO_NGUYEN_TE" <> 0
                OR "DU_CO" - "DU_NO" <> 0
            ORDER BY
                P."MA_DON_VI",
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
        WHERE   "OrderType" <> 2
        ORDER BY  RowNum

    LOOP

        SELECT (CASE WHEN rec."OrderType" = 0
            THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0
                THEN rec."DU_CO_NGUYEN_TE"
                  ELSE -1
                       * rec."DU_NO_NGUYEN_TE"
                  END)
                WHEN
                    MA_DON_VI_TMP <> rec."MA_DON_VI"
                    OR MA_DOI_TUONG_TMP <> rec."MA_DOI_TUONG"
                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    THEN rec."GHI_CO_NGUYEN_TE" - rec."GHI_NO_NGUYEN_TE"
                ELSE SO_TIEN_TON_NGUYEN_TE + rec."GHI_CO_NGUYEN_TE"
                     - rec."GHI_NO_NGUYEN_TE"
                END)
        INTO SO_TIEN_TON_NGUYEN_TE
    ;



            rec."DU_NO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '0'
                THEN -1 * SO_TIEN_TON_NGUYEN_TE
                                 WHEN rec."TINH_CHAT" = '1'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE < 0
                                     THEN -1
                                          * SO_TIEN_TON_NGUYEN_TE
                                      ELSE 0
                                      END
                                 END);

        UPDATE TMP_KET_QUA
            set "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
                WHERE RowNum = rec.RowNum;



            rec."DU_CO_NGUYEN_TE" = (CASE WHEN rec."TINH_CHAT" = '1'
                THEN SO_TIEN_TON_NGUYEN_TE
                                 WHEN rec."TINH_CHAT" = '0'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON_NGUYEN_TE > 0
                                     THEN SO_TIEN_TON_NGUYEN_TE
                                      ELSE 0
                                      END
                                 END) ;
             UPDATE TMP_KET_QUA
                set "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
                    WHERE RowNum = rec.RowNum;




        SELECT (CASE WHEN rec."OrderType" = 0
            THEN (CASE WHEN rec."DU_NO" = 0
                THEN rec."DU_CO"
                  ELSE -1 * rec."DU_NO"
                  END)

                WHEN MA_DON_VI_TMP <> rec."MA_DON_VI"
                     OR MA_DOI_TUONG_TMP <> rec."MA_DOI_TUONG"
                     OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                    THEN rec."GHI_CO" - rec."GHI_NO"
                ELSE SO_TIEN_TON + rec."GHI_CO"
                     - rec."GHI_NO"
                END)
        INTO SO_TIEN_TON
    ;




            rec."DU_NO"           = (CASE WHEN rec."TINH_CHAT" = '0'
                THEN -1 * SO_TIEN_TON
                                 WHEN rec."TINH_CHAT" = '1'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON < 0
                                     THEN -1 * SO_TIEN_TON
                                      ELSE 0
                                      END
                                 END);

            UPDATE TMP_KET_QUA
                set "DU_NO" =rec."DU_NO"
                WHERE RowNum = rec.RowNum;

            rec."DU_CO"           = (CASE WHEN rec."TINH_CHAT" = '1'
                THEN SO_TIEN_TON
                                 WHEN rec."TINH_CHAT" = '0'
                                     THEN 0
                                 ELSE CASE WHEN SO_TIEN_TON > 0
                                     THEN SO_TIEN_TON
                                      ELSE 0
                                      END
                                 END) ;
            UPDATE TMP_KET_QUA
                set "DU_CO" =rec."DU_CO"
                    WHERE RowNum = rec.RowNum;



        MA_DON_VI_TMP = rec."MA_DON_VI"
    ;

        MA_DOI_TUONG_TMP = rec."MA_DOI_TUONG"
    ;

        SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN"
    ;

    END LOOP
    ;


END $$
;

SELECT
    RowNum
    , "DOI_TUONG_ID" 
    , "MA_DOI_TUONG"
    , "TEN_DOI_TUONG" as "TEN_KHACH_HANG"
    , "DON_VI_ID" 
    , "MA_DON_VI"
    , "TEN_DON_VI" as "TEN_DON_VI" 
    , "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN" 
    , "NGAY_CHUNG_TU" as "NGAY_CHUNG_TU" 
    , "SO_CHUNG_TU" as "SO_CHUNG_TU" 
    , "LOAI_CHUNG_TU"
    , "ID_CHUNG_TU"
    , "MODEL_CHUNG_TU"
    , "DIEN_GIAI" as "DIEN_GIAI" 
    , "SO_TAI_KHOAN" as "TK_CO_ID" 
    , "TINH_CHAT"
    , "MA_TK_DOI_UNG"  as "TK_DOI_UNG" 
    , "GHI_NO_NGUYEN_TE" 
    , "GHI_NO"    as "NO_SO_PHAT_SINH" 
    , "GHI_CO_NGUYEN_TE" 
    , "GHI_CO"   as "CO_SO_PHAT_SINH" 
    , "DU_NO_NGUYEN_TE" 
    , "DU_NO"   as "NO_SO_DU" 
    , "DU_CO_NGUYEN_TE" 
    , "DU_CO"    as "CO_SO_DU" 
    , "OrderType"
    ,"ID_CHUNG_TU" as "ID_GOC"
    ,"MODEL_CHUNG_TU" as "MODEL_GOC"
FROM TMP_KET_QUA RS
ORDER BY RS.rownum
OFFSET %(offset)s
LIMIT %(limit)s
;
        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_chi_tiet_theo_cac_khoan_giam_tru(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_CHI_TIET_CONG_NO_PHAI_THU_KHACH_HANG
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    
    v_cong_gop_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    

   rec                                   RECORD;

    LOAI_TIEN_CHINH                       VARCHAR(100);

    CHE_DO_KE_TOAN                        VARCHAR(100);



    SO_TIEN_TON_NGUYEN_TE                 FLOAT := 0;

    SO_TIEN_TON                           FLOAT := 0;


    MA_DOI_TUONG_TMP                      VARCHAR(100) :=N'';

    SO_TAI_KHOAN_TMP                       VARCHAR(100) :=N'';


BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;


    CREATE TEMP TABLE DS_KHACH_HANG
        AS

            SELECT "id" AS "KHACH_HANG_ID"


            FROM res_partner
            WHERE (id = any (%(KHACH_HANG_IDS)s)) 
    ;


    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

                IF so_tai_khoan IS NOT NULL
                THEN
                    CREATE TEMP TABLE TMP_TAI_KHOAN
                        AS
                            SELECT
                                     A."id"
                                , A."SO_TAI_KHOAN"

                                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                                , A."TINH_CHAT"
                                 , A."CHI_TIET_THEO_DOI_TUONG"
                            FROM danh_muc_he_thong_tai_khoan AS A
                            WHERE "SO_TAI_KHOAN" = so_tai_khoan
                                    AND "CHI_TIET_THEO_DOI_TUONG" = '1'
                                    AND "DOI_TUONG_SELECTION" = '1'
                            ORDER BY
                                A."SO_TAI_KHOAN",
                                A."TEN_TAI_KHOAN"
                    ;

                ELSE
    CREATE TEMP TABLE TMP_TAI_KHOAN
        AS
            SELECT
                A."id"
                , A."SO_TAI_KHOAN"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                , A."TINH_CHAT"
                , A."CHI_TIET_THEO_DOI_TUONG"
            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND "DOI_TUONG_SELECTION" = '1'
                  AND "LA_TK_TONG_HOP" = '0'
            ORDER BY
                A."SO_TAI_KHOAN",
                A."TEN_TAI_KHOAN"
    ;

                END IF ;


    DROP TABLE IF EXISTS TMP_KET_QUA

    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq
    ;


    CREATE TABLE TMP_KET_QUA
    (
        RowNum                         INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,
        "SO_TAI_KHOAN"                 VARCHAR(100),
        "KHACH_HANG_ID"                INT,
        "MA_KHACH_HANG"                VARCHAR(100)
        , -- Mã NCC
        "HO_VA_TEN"                    VARCHAR(255)
        , -- Tên NCC

        "NGAY_HACH_TOAN"               TIMESTAMP(3), -- Ngày hạch toán
        "NGAY_CHUNG_TU"                TIMESTAMP(3), -- Ngày chứng từ
        "SO_CHUNG_TU"                  VARCHAR(255), -- Số chứng từ

        "NGAY_HOA_DON"                 TIMESTAMP(3),
        "SO_HOA_DON"                   VARCHAR(100),

        "LOAI_CHUNG_TU"                  VARCHAR(100), --Loại chứng từ
        "ID_CHUNG_TU"                   INT, -- Mã chứng từ
        "MODEL_CHUNG_TU"               VARCHAR(255),
        "DIEN_GIAI_CHUNG"              VARCHAR(255), -- Diễn giải
        "HAN_THANH_TOAN"               TIMESTAMP(3),

        "SO_PHAI_THU_NGUYEN_TE"        FLOAT, -- Phải thu
        "SO_PHAI_THU"                  FLOAT, -- Phải thu quy đổi
        "SO_TIEN_CHIET_KHAU_NGUYEN_TE" FLOAT, -- Chiết khấu
        "SO_TIEN_CHIET_KHAU"           FLOAT, -- Chiết khấu quy đổi
        "SO_TIEN_TRA_LAI_NGUYEN_TE"    FLOAT, --Trả lại/Giảm giá
        "SO_TIEN_TRA_LAI"              FLOAT, --Trả lại/giảm giá Quy đổi
        "CK_GIAM_TRU_KHAC_NGUYEN_TE"   FLOAT, --Chiết khấu giảm trừ khác
        "CK_GIAM_TRU_KHAC"             FLOAT, --Chiết khấu giảm trừ khác quy đổi
        "SO_DA_THU_NGUYEN_TE"          FLOAT, -- Số đã thu
        "SO_DA_THU"                    FLOAT, -- Số đã thu quy đổi

        "SO_DU_NGUYEN_TE"              FLOAT, -- Số còn phải thu
        "SO_DU"                        FLOAT, -- Số còn phải thu quy đổi
        "OrderType"                    INTEGER


    )
    ;


    INSERT INTO TMP_KET_QUA
    ("SO_TAI_KHOAN"
        , "KHACH_HANG_ID"
        , "MA_KHACH_HANG"
        , "HO_VA_TEN"
        , "NGAY_HACH_TOAN"
        , "NGAY_CHUNG_TU"
        , "SO_CHUNG_TU"
        , "NGAY_HOA_DON"
        , "SO_HOA_DON"

        , "LOAI_CHUNG_TU"
        , "ID_CHUNG_TU"
        , "MODEL_CHUNG_TU"
        , "DIEN_GIAI_CHUNG"
        , "HAN_THANH_TOAN"

        , "SO_PHAI_THU_NGUYEN_TE"
        , "SO_PHAI_THU"
        , "SO_TIEN_CHIET_KHAU_NGUYEN_TE"
        , "SO_TIEN_CHIET_KHAU"
        , "SO_TIEN_TRA_LAI_NGUYEN_TE"
        , "SO_TIEN_TRA_LAI"
        , "CK_GIAM_TRU_KHAC_NGUYEN_TE"
        , "CK_GIAM_TRU_KHAC"
        , "SO_DA_THU_NGUYEN_TE"
        , "SO_DA_THU"

        , "SO_DU_NGUYEN_TE"
        , "SO_DU"
        , "OrderType"

    )


        SELECT

            TBAN."SO_TAI_KHOAN"

            , AO.id
            , AO."MA_KHACH_HANG"
            , AO."HO_VA_TEN"

            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."NGAY_HACH_TOAN"
              END AS "NGAY_HACH_TOAN"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."NGAY_CHUNG_TU"
              END AS "NGAY_CHUNG_TU"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."SO_CHUNG_TU"
              END AS "SO_CHUNG_TU"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."NGAY_HOA_DON"
              END AS "NGAY_HOA_DON"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."SO_HOA_DON"
              END AS "SO_HOA_DON"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."LOAI_CHUNG_TU"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."ID_CHUNG_TU"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."MODEL_CHUNG_TU"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN N'Số dư đầu kỳ'
              ELSE SL."DIEN_GIAI_CHUNG"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."HAN_THANH_TOAN"
              END

            , SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                            AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
            THEN SL."GHI_NO_NGUYEN_TE"
                  ELSE 0
                  END)
            , SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                            AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
            THEN SL."GHI_NO"
                  ELSE 0
                  END)
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                     --THEN SL."GHI_CO_NGUYEN_TE"
                     WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                         THEN SL."GHI_CO_NGUYEN_TE"
                     ELSE 0
                     END)
              ELSE SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                       --THEN SL."GHI_CO_NGUYEN_TE"
                       WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                            AND SL."LOAI_NGHIEP_VU" ='0'
                           THEN SL."GHI_CO_NGUYEN_TE"
                       ELSE 0
                       END)
              END AS "SO_TIEN_CHIET_KHAU_NGUYEN_TE"
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                     --THEN SL."GHI_CO"
                     WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                         THEN SL."GHI_CO"
                     ELSE 0
                     END)
              ELSE SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                       --THEN SL."GHI_CO"
                       WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                            AND SL."LOAI_NGHIEP_VU" ='0'
                           THEN SL."GHI_CO"
                       ELSE 0
                       END)
              END AS "SO_TIEN_CHIET_KHAU"
            ,
            /*  = PS Nợ TK 5212, TK 5213, 33311/Có TK phải thu tương ứng với từng khách hàng trên từng chứng từ chi tiết*/

              CASE WHEN CHE_DO_KE_TOAN = '15'

                  THEN SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                                     OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                                     OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                      THEN SL."GHI_CO_NGUYEN_TE"
                           ELSE 0
                           END)
              ELSE SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                  AND SL."LOAI_NGHIEP_VU" IN ('1',
                                                              '2')
                                 )
                                 OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                  THEN SL."GHI_CO_NGUYEN_TE"
                       ELSE 0
                       END)
              END AS "SO_TIEN_TRA_LAI_NGUYEN_TE"
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                               OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                               OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                THEN SL."GHI_CO"
                     ELSE 0
                     END)
              ELSE SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                  AND SL."LOAI_NGHIEP_VU" IN ('1',
                                                              '2')
                                 )
                                 OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                  THEN SL."GHI_CO"
                       ELSE 0
                       END)
              END AS "SO_TIEN_TRA_LAI"
            ,
            /*  = PS nợ TK (không bao gồm các TK 11x, 521, 33311/Có TK phải thu tương ứng từng khách hàng trên từng chứng từ chi tiết*/

            CASE WHEN CHE_DO_KE_TOAN = '15'

                THEN (SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                    AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                    THEN SL."GHI_CO_NGUYEN_TE"
                          ELSE 0
                          END)
                      - (SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                             --THEN SL."GHI_CO_NGUYEN_TE"
                             WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                                 THEN SL."GHI_CO_NGUYEN_TE"
                             ELSE 0
                             END))
                      - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                                       OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                                       OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                    THEN SL."GHI_CO_NGUYEN_TE"
                             ELSE 0
                             END))
                      - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                    THEN SL."GHI_CO_NGUYEN_TE"
                             ELSE 0
                             END)))
            ELSE (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                         AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                THEN SL."GHI_CO_NGUYEN_TE"
                               ELSE 0
                               END), 0)
                  - (COALESCE(SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                                  --THEN SL."GHI_CO_NGUYEN_TE"
                                  WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                       AND SL."LOAI_NGHIEP_VU" ='0'
                                      THEN SL."GHI_CO_NGUYEN_TE"
                                  ELSE 0
                                  END), 0))
                  - (COALESCE(SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                             AND SL."LOAI_NGHIEP_VU" IN (
                '1', '2')
                                            )
                                            OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                THEN SL."GHI_CO_NGUYEN_TE"
                                  ELSE 0
                                  END), 0))
                  - (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                THEN SL."GHI_CO_NGUYEN_TE"
                                  ELSE 0
                                  END), 0)))
            END
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN (SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                THEN SL."GHI_CO"
                      ELSE 0
                      END)
                  - (SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                         --THEN SL."GHI_CO_NGUYEN_TE"
                         WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                             THEN SL."GHI_CO"
                         ELSE 0
                         END))
                  - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                                   OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                                   OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                THEN SL."GHI_CO"
                         ELSE 0
                         END))
                  - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                THEN SL."GHI_CO"
                         ELSE 0
                         END)))
              ELSE (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                           AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                  THEN SL."GHI_CO"
                                 ELSE 0
                                 END), 0)
                    - (COALESCE(SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                                    --THEN SL."GHI_CO_NGUYEN_TE"
                                    WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                         AND SL."LOAI_NGHIEP_VU" ='0'
                                        THEN SL."GHI_CO"
                                    ELSE 0
                                    END), 0))
                    - (COALESCE(SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                               AND SL."LOAI_NGHIEP_VU" IN (
                  '1', '2')
                                              )
                                              OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                  THEN SL."GHI_CO"
                                    ELSE 0
                                    END), 0))
                    - (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                  THEN SL."GHI_CO"
                                    ELSE 0
                                    END), 0)))
              END
            , /*  = PS Nợ TK 11x/Có TK phải thu tương ứng với từng khách hàng chọn xem báo cáo*/

            SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                THEN SL."GHI_CO_NGUYEN_TE"
                ELSE 0
                END)
            , SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
            THEN SL."GHI_CO"
                  ELSE 0
                  END)
            , 0
            , 0


            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN 0
              ELSE 1
              END AS OrderType

        FROM so_cai_chi_tiet AS SL
            INNER JOIN res_partner AO ON SL."DOI_TUONG_ID" = AO.id

            INNER JOIN TMP_TAI_KHOAN TBAN ON SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                             OR (SL."MA_TAI_KHOAN_DOI_UNG" LIKE TBAN."AccountNumberPercent"
                                                 AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                             )
            INNER JOIN DS_KHACH_HANG AS LAOI ON SL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
            INNER JOIN TMP_LIST_BRAND BIDL ON SL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
            LEFT JOIN res_partner A1 ON SL."NHAN_VIEN_ID" = A1."id"
                                        AND A1."LA_NHAN_VIEN" = '1'

        WHERE SL."NGAY_HACH_TOAN" < v_tu_ngay

              AND (v_loai_tien_id IS NULL
                   OR SL."currency_id" = v_loai_tien_id
              )
              AND TBAN."SO_TAI_KHOAN" IS NOT NULL


        GROUP BY

            TBAN."SO_TAI_KHOAN"
            ,
            AO.id,
            AO."MA_KHACH_HANG",
            AO."HO_VA_TEN",


           SL."NGAY_HACH_TOAN"
            ,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."NGAY_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."SO_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."NGAY_HOA_DON"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."SO_HOA_DON"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."LOAI_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."ID_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."MODEL_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN N'Số dư đầu kỳ'
            ELSE SL."DIEN_GIAI_CHUNG"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."HAN_THANH_TOAN"
            END


        UNION ALL
        /*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/
        SELECT
           
            TBAN."SO_TAI_KHOAN"
            , AO.id
            , AO."MA_KHACH_HANG"
            , AO."HO_VA_TEN"

            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."NGAY_HACH_TOAN"
              END AS "NGAY_HACH_TOAN"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."NGAY_CHUNG_TU"
              END AS "NGAY_CHUNG_TU"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."SO_CHUNG_TU"
              END AS "SO_CHUNG_TU"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."NGAY_HOA_DON"
              END AS "NGAY_HOA_DON"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."SO_HOA_DON"
              END AS "SO_HOA_DON"
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."LOAI_CHUNG_TU"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."ID_CHUNG_TU"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."MODEL_CHUNG_TU"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN N'Số dư đầu kỳ'
              ELSE SL."DIEN_GIAI_CHUNG"
              END
            , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN NULL
              ELSE SL."HAN_THANH_TOAN"
              END

            , SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                            AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
            THEN SL."GHI_NO_NGUYEN_TE"
                  ELSE 0
                  END)
            , SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                            AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
            THEN SL."GHI_NO"
                  ELSE 0
                  END)
            , 

              CASE WHEN CHE_DO_KE_TOAN = '15'

                  THEN SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                           --THEN SL."GHI_CO_NGUYEN_TE"
                           WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                               THEN SL."GHI_CO_NGUYEN_TE"
                           ELSE 0
                           END)
              ELSE SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                       --THEN SL."GHI_CO_NGUYEN_TE"
                       WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                            AND SL."LOAI_NGHIEP_VU" ='0'
                           THEN SL."GHI_CO_NGUYEN_TE"
                       ELSE 0
                       END)
              END AS "SO_TIEN_CHIET_KHAU_NGUYEN_TE"
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                     --THEN SL."GHI_CO"
                     WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                         THEN SL."GHI_CO"
                     ELSE 0
                     END)
              ELSE SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                       --THEN SL."GHI_CO"
                       WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                            AND SL."LOAI_NGHIEP_VU" ='0'
                           THEN SL."GHI_CO"
                       ELSE 0
                       END)
              END AS "SO_TIEN_CHIET_KHAU"
            ,
           
              CASE WHEN CHE_DO_KE_TOAN = '15'

                  THEN SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                                     OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                                     OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                      THEN SL."GHI_CO_NGUYEN_TE"
                           ELSE 0
                           END)
              ELSE SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                  AND SL."LOAI_NGHIEP_VU" IN ('1',
                                                              '2')
                                 )
                                 OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                  THEN SL."GHI_CO_NGUYEN_TE"
                       ELSE 0
                       END)
              END AS "SO_TIEN_TRA_LAI_NGUYEN_TE"
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                               OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                               OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                THEN SL."GHI_CO"
                     ELSE 0
                     END)
              ELSE SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                  AND SL."LOAI_NGHIEP_VU" IN ('1',
                                                              '2')
                                 )
                                 OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                  THEN SL."GHI_CO"
                       ELSE 0
                       END)
              END AS "SO_TIEN_TRA_LAI"
            ,
          

            CASE WHEN CHE_DO_KE_TOAN = '15'

                THEN (SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                    AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                    THEN SL."GHI_CO_NGUYEN_TE"
                          ELSE 0
                          END)
                      - (SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
                             --THEN SL."GHI_CO_NGUYEN_TE"
                             WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                                 THEN SL."GHI_CO_NGUYEN_TE"
                             ELSE 0
                             END))
                      - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                                       OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                                       OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                    THEN SL."GHI_CO_NGUYEN_TE"
                             ELSE 0
                             END))
                      - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                    THEN SL."GHI_CO_NGUYEN_TE"
                             ELSE 0
                             END)))
            ELSE (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                         AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                THEN SL."GHI_CO_NGUYEN_TE"
                               ELSE 0
                               END), 0)
                  - (COALESCE(SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                                  --THEN SL."GHI_CO_NGUYEN_TE"
                                  WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                       AND SL."LOAI_NGHIEP_VU" ='0'
                                      THEN SL."GHI_CO_NGUYEN_TE"
                                  ELSE 0
                                  END), 0))
                  - (COALESCE(SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                             AND SL."LOAI_NGHIEP_VU" IN (
                '1', '2')
                                            )
                                            OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                THEN SL."GHI_CO_NGUYEN_TE"
                                  ELSE 0
                                  END), 0))
                  - (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                THEN SL."GHI_CO_NGUYEN_TE"
                                  ELSE 0
                                  END), 0)))
            END
            , CASE WHEN CHE_DO_KE_TOAN = '15'

            THEN (SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                THEN SL."GHI_CO"
                      ELSE 0
                      END)
                  - (SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                         --THEN SL."GHI_CO_NGUYEN_TE"
                         WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
                             THEN SL."GHI_CO"
                         ELSE 0
                         END))
                  - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
                                   OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
                                   OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                THEN SL."GHI_CO"
                         ELSE 0
                         END))
                  - (SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                THEN SL."GHI_CO"
                         ELSE 0
                         END)))
              ELSE (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                           AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                  THEN SL."GHI_CO"
                                 ELSE 0
                                 END), 0)
                    - (COALESCE(SUM(CASE --WHEN SL."MA_TAI_KHOAN" LIKE '5211%%'
                                    --THEN SL."GHI_CO_NGUYEN_TE"
                                    WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                         AND SL."LOAI_NGHIEP_VU" ='0'
                                        THEN SL."GHI_CO"
                                    ELSE 0
                                    END), 0))
                    - (COALESCE(SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%'
                                               AND SL."LOAI_NGHIEP_VU" IN (
                  '1', '2')
                                              )
                                              OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
                  THEN SL."GHI_CO"
                                    ELSE 0
                                    END), 0))
                    - (COALESCE(SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                  THEN SL."GHI_CO"
                                    ELSE 0
                                    END), 0)))
              END
            , /*  = PS Nợ TK 11x/Có TK phải thu tương ứng với từng khách hàng chọn xem báo cáo*/
            SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
                THEN SL."GHI_CO_NGUYEN_TE"
                ELSE 0
                END)
            , SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
            THEN SL."GHI_CO"
                  ELSE 0
                  END)
            , 0
            , 0
             , CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
            THEN 0
              ELSE 1
              END AS OrderType

        FROM so_cai_chi_tiet AS SL
            INNER JOIN res_partner AO ON SL."DOI_TUONG_ID" = AO.id

            INNER JOIN TMP_TAI_KHOAN TBAN ON SL."MA_TAI_KHOAN" LIKE TBAN."AccountNumberPercent"
                                             OR (SL."MA_TAI_KHOAN_DOI_UNG" LIKE TBAN."AccountNumberPercent"
                                                 AND TBAN."CHI_TIET_THEO_DOI_TUONG" = '1'
                                             )
            INNER JOIN DS_KHACH_HANG AS LAOI ON SL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
            INNER JOIN TMP_LIST_BRAND BIDL ON SL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
            LEFT JOIN res_partner A1 ON SL."NHAN_VIEN_ID" = A1."id"
                                        AND A1."LA_NHAN_VIEN" = '1'

        WHERE SL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

              AND (v_loai_tien_id IS NULL
                   OR SL."currency_id" = v_loai_tien_id
              )
              AND TBAN."SO_TAI_KHOAN" IS NOT NULL


        GROUP BY

            TBAN."SO_TAI_KHOAN"
            ,
            AO.id,
            AO."MA_KHACH_HANG",
            AO."HO_VA_TEN",


            SL."NGAY_HACH_TOAN"
           ,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."NGAY_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."SO_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."NGAY_HOA_DON"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."SO_HOA_DON"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."LOAI_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."ID_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."MODEL_CHUNG_TU"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN N'Số dư đầu kỳ'
            ELSE SL."DIEN_GIAI_CHUNG"
            END,
            CASE WHEN SL."NGAY_HACH_TOAN" < v_tu_ngay
                THEN NULL
            ELSE SL."HAN_THANH_TOAN"
            END

        ORDER BY
            "MA_KHACH_HANG",
            "HO_VA_TEN",
            "SO_TAI_KHOAN",
            OrderType,
            "NGAY_HACH_TOAN",
            "NGAY_CHUNG_TU",
            "SO_CHUNG_TU",
            "NGAY_HOA_DON",
            "SO_HOA_DON"
    ;

    --  Sắp xếp theo Tài khoản (Khi chọn cả TK cha và TK con thì sắp xếp TK cha-> TK con) ->  Mã khách hàng -> Ngày hạch toán-> Ngày CT -> Số CT, ngày hóa đơn, Số hóa đơn (Luôn sắp xếp các số dư đầu kỳ lên trước các chứng từ)


    /*Tinh số dư đầu kỳ*/

          UPDATE  TMP_KET_QUA
            SET
                "SO_DU_NGUYEN_TE" = "SO_PHAI_THU_NGUYEN_TE" - "SO_TIEN_CHIET_KHAU_NGUYEN_TE"
                - "SO_TIEN_TRA_LAI_NGUYEN_TE" - "CK_GIAM_TRU_KHAC_NGUYEN_TE" - "SO_DA_THU_NGUYEN_TE" ,
                "SO_DU" = "SO_PHAI_THU" - "SO_TIEN_CHIET_KHAU"
                - "SO_TIEN_TRA_LAI" - "CK_GIAM_TRU_KHAC" - "SO_DA_THU" ,
                "SO_PHAI_THU_NGUYEN_TE" = 0 ,
                "SO_PHAI_THU" = 0 ,
                "SO_TIEN_CHIET_KHAU_NGUYEN_TE" = 0 ,
                "SO_TIEN_CHIET_KHAU" = 0 ,
                "SO_TIEN_TRA_LAI" = 0 ,
                "SO_TIEN_TRA_LAI_NGUYEN_TE" = 0 ,
                "CK_GIAM_TRU_KHAC_NGUYEN_TE" = 0 ,
                "CK_GIAM_TRU_KHAC" = 0 ,
                "SO_DA_THU_NGUYEN_TE" = 0 ,
                "SO_DA_THU" = 0
        WHERE   "OrderType" = 0;



    FOR rec IN
    SELECT *
    FROM TMP_KET_QUA
         ORDER BY RowNum

    LOOP

            SELECT
                 COALESCE(( CASE WHEN rec."OrderType" = 0
                                               THEN rec."SO_DU_NGUYEN_TE"
                                               WHEN MA_DOI_TUONG_TMP <> rec."MA_KHACH_HANG"
                                                    OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                                               THEN rec."SO_PHAI_THU_NGUYEN_TE"
                                                    - rec."SO_TIEN_CHIET_KHAU_NGUYEN_TE"
                                                    - rec."SO_TIEN_TRA_LAI_NGUYEN_TE"
                                                    - rec."CK_GIAM_TRU_KHAC_NGUYEN_TE"
                                                    - rec."SO_DA_THU_NGUYEN_TE"
                                               ELSE SO_TIEN_TON_NGUYEN_TE
                                                    + rec."SO_PHAI_THU_NGUYEN_TE"
                                                    - rec."SO_TIEN_CHIET_KHAU_NGUYEN_TE"
                                                    - rec."SO_TIEN_TRA_LAI_NGUYEN_TE"
                                                    - rec."CK_GIAM_TRU_KHAC_NGUYEN_TE"
                                                    - rec."SO_DA_THU_NGUYEN_TE"
                                          END ), 0)
                      INTO SO_TIEN_TON_NGUYEN_TE ;
         rec."SO_DU_NGUYEN_TE" = SO_TIEN_TON_NGUYEN_TE ;
          UPDATE TMP_KET_QUA
                set "SO_DU_NGUYEN_TE" =rec."SO_DU_NGUYEN_TE"
                WHERE RowNum = rec.RowNum;


                SELECT COALESCE(( CASE WHEN rec."OrderType" = 0
                                             THEN rec."SO_DU"
                                             WHEN MA_DOI_TUONG_TMP <> rec."MA_KHACH_HANG"
                                                  OR SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN"
                                             THEN rec."SO_PHAI_THU"
                                                    - rec."SO_TIEN_CHIET_KHAU"
                                                    - rec."SO_TIEN_TRA_LAI"
                                                    - rec."CK_GIAM_TRU_KHAC"
                                                    - rec."SO_DA_THU"
                                               ELSE SO_TIEN_TON
                                                    + rec."SO_PHAI_THU"
                                                    - rec."SO_TIEN_CHIET_KHAU"
                                                    - rec."SO_TIEN_TRA_LAI"
                                                    - rec."CK_GIAM_TRU_KHAC"
                                                    - rec."SO_DA_THU"
                                        END ), 0)
                    INTO SO_TIEN_TON ;

          rec."SO_DU" = SO_TIEN_TON ;
          UPDATE TMP_KET_QUA
                set "SO_DU" =rec."SO_DU"
                WHERE RowNum = rec.RowNum;

        MA_DOI_TUONG_TMP = rec."MA_KHACH_HANG" ;
        SO_TAI_KHOAN_TMP = rec."SO_TAI_KHOAN";

      END LOOP
    ;




END $$
;

SELECT 
    "NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
    "NGAY_CHUNG_TU" as "NGAY_CHUNG_TU",
    "SO_CHUNG_TU" as "SO_CHUNG_TU",
    "NGAY_HOA_DON" as "NGAY_HOA_DON",
    "SO_HOA_DON" as "SO_HOA_DON",
    "DIEN_GIAI_CHUNG" as "DIEN_GIAI",
    "HAN_THANH_TOAN" as "HAN_THANH_TOAN",
    "SO_TAI_KHOAN" as "TAI_KHOAN_KH",
    "SO_PHAI_THU" as "SO_PHAI_THU",
    "SO_TIEN_CHIET_KHAU" as "CHIET_KHAU",
    "SO_TIEN_TRA_LAI" as "TRA_LAI_GIAM_GIA",
    "CK_GIAM_TRU_KHAC" as "CK_THANH_TOAN_GIAM_TRU_KHAC",
    "SO_DA_THU" as "SO_DA_THU",
    "SO_DU" as "SO_DU",
    "HO_VA_TEN" as "TEN_KHACH_HANG",
    "ID_CHUNG_TU" as "ID_GOC",
    "MODEL_CHUNG_TU" as "MODEL_GOC"
FROM TMP_KET_QUA

WHERE ( "SO_PHAI_THU_NGUYEN_TE" <> 0
        OR "SO_PHAI_THU" <> 0
        OR "SO_TIEN_CHIET_KHAU_NGUYEN_TE" <> 0
        OR "SO_TIEN_CHIET_KHAU" <> 0
        OR "SO_TIEN_TRA_LAI" <> 0
        OR "SO_TIEN_TRA_LAI_NGUYEN_TE" <> 0
        OR "CK_GIAM_TRU_KHAC_NGUYEN_TE" <> 0
        OR "CK_GIAM_TRU_KHAC" <> 0
        OR "SO_DA_THU_NGUYEN_TE" <> 0
        OR "SO_DA_THU" <> 0
        )
        OR ( ( "SO_DU_NGUYEN_TE" <> 0
        OR "SO_DU" <> 0
)
            AND "OrderType" = 0
)
OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)



    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_CHI_TIET_CONG_NO_PHAI_THU_KHACH_HANG, self).default_get(fields_list)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_DOI_TUONG', '=', 'True'),('DOI_TUONG_SELECTION', '=', '1')],limit=1)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
      
        if tai_khoan:
            result['TAI_KHOAN_ID'] = tai_khoan.id
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if loai_tien:
            result['currency_id'] = loai_tien.id
        

        return result
    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_KHACH_HANG = params['CHON_TAT_CA_KHACH_HANG'] if 'CHON_TAT_CA_KHACH_HANG' in params.keys() else 'False'
        CHON_TAT_CA_NHAN_VIEN = params['CHON_TAT_CA_NHAN_VIEN'] if 'CHON_TAT_CA_NHAN_VIEN' in params.keys() else 'False'
        CHON_TAT_CA_DON_VI_KINH_DOANH = params['CHON_TAT_CA_DON_VI_KINH_DOANH'] if 'CHON_TAT_CA_DON_VI_KINH_DOANH' in params.keys() else 'False'
        CHON_TAT_CA_DON_DAT_HANG = params['CHON_TAT_CA_DON_DAT_HANG'] if 'CHON_TAT_CA_DON_DAT_HANG' in params.keys() else 'False'
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CHON_TAT_CA_HOP_DONG = params['CHON_TAT_CA_HOP_DONG'] if 'CHON_TAT_CA_HOP_DONG' in params.keys() else 'False'

        HOP_DONG_MANY_IDS = params['HOP_DONG_MANY_IDS'] if 'HOP_DONG_MANY_IDS' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        DON_DAT_HANG_MANY_IDS = params['DON_DAT_HANG_MANY_IDS'] if 'DON_DAT_HANG_MANY_IDS' in params.keys() else 'False'
        DON_VI_KINH_DOANH_MANY_IDS = params['DON_VI_KINH_DOANH_MANY_IDS'] if 'DON_VI_KINH_DOANH_MANY_IDS' in params.keys() else 'False'
        NHAN_VIEN_MANY_IDS = params['NHAN_VIEN_MANY_IDS'] if 'NHAN_VIEN_MANY_IDS' in params.keys() else 'False'
        KHACH_HANG_MANY_IDS = params['KHACH_HANG_MANY_IDS'] if 'KHACH_HANG_MANY_IDS' in params.keys() else 'False'

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO in ('KHONG_CHON','NHAN_VIEN','CONG_TRINH','HOP_DONG','DON_DAT_HANG','DON_VI_KINH_DOANH','CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU'):
            if CHON_TAT_CA_KHACH_HANG == 'False':
                if KHACH_HANG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO =='NHAN_VIEN':
            if CHON_TAT_CA_NHAN_VIEN == 'False':
                if NHAN_VIEN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO=='CONG_TRINH':
            if CHON_TAT_CA_CONG_TRINH == 'False':
                if CONG_TRINH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')
        
        if THONG_KE_THEO=='HOP_DONG':
            if CHON_TAT_CA_HOP_DONG == 'False':
                if HOP_DONG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hợp đồng>. Xin vui lòng chọn lại.')
        
        if THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            if CHON_TAT_CA_DON_VI_KINH_DOANH == 'False':
                if DON_VI_KINH_DOANH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đơn vị>. Xin vui lòng chọn lại.')


    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        currency_id = self.get_context('currency_id')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        loai_tien = self.env['res.currency'].browse(currency_id).name
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan = ''
        tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        if tai_khoan_id:
            tai_khoan = tai_khoan_id.SO_TAI_KHOAN
        param = 'Tài khoản: %s; Loại tiền: %s; Từ ngày: %s đến ngày %s' % (tai_khoan, loai_tien, TU_NGAY_F, DEN_NGAY_F)
        if THONG_KE_THEO =='KHONG_CHON':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang').read()[0]
        elif THONG_KE_THEO=='NHAN_VIEN':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang_nhanvien').read()[0]
        elif THONG_KE_THEO=='CONG_TRINH':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang_congtrinh').read()[0]
        elif THONG_KE_THEO=='HOP_DONG':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang_hopdong').read()[0]
        elif THONG_KE_THEO=='DON_DAT_HANG':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang_dondathang').read()[0]
        elif THONG_KE_THEO=='DON_VI_KINH_DOANH':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang_donvikinhdoanh').read()[0]
        elif THONG_KE_THEO=='CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU':
            action = self.env.ref('bao_cao.open_report__chi_tiet_cong_no_phai_thu_khach_hang_theocackhoangiamtru').read()[0]
            
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action