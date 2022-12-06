# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_CONG_NO_PHAI_THU_KHACH_HANG(models.Model):
    _name = 'bao.cao.tong.hop.cong.no.phai.thu.khach.hang'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'), ('NHAN_VIEN', 'Nhân viên'), ('NHAN_VIEN_VA_KHACH_HANG', 'Nhân viên và khách hàng'), ('CONG_TRINH', 'Công trình'), ('HOP_DONG', 'Hợp đồng'), ('DON_DAT_HANG', 'Đơn đặt hàng'), ('DON_VI_KINH_DOANH', 'Đơn vị kinh doanh'), ('CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU', 'Chi tiết theo các khoản giảm trừ'), ], string='Thống kê theo', help='Thống kê theo',default='KHONG_CHON',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày', required=True)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True)
    NHOM_KH_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    MA_KHACH_HANG = fields.Char(string='Mã khách hàng', help='Mã khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    TAI_KHOAN_CONG_NO = fields.Char(string='TK công nợ', help='Tài khoản công nợ')
    NO_SO_DU_DAU_KY = fields.Float(string='Nợ', help='Nợ số dư đầu kỳ',digits= decimal_precision.get_precision('VND'))
    CO_SO_DU_DAU_KY = fields.Float(string='Có', help='Có số dư đầu kỳ',digits=decimal_precision.get_precision('VND'))
    NO_SO_PHAT_SINH = fields.Float(string='Nợ', help='Nợ số phát sinh',digits=decimal_precision.get_precision('VND'))
    CO_SO_PHAT_SINH = fields.Float(string='Có', help='Có số phát sinh',digits=decimal_precision.get_precision('VND'))
    NO_SO_DU_CUOI_KY = fields.Float(string='Nợ', help='Nợ số dư cuối kỳ',digits=decimal_precision.get_precision('VND'))
    CO_SO_DU_CUOI_KY = fields.Float(string='Có', help='Có số dư cuối kỳ',digits=decimal_precision.get_precision('VND'))
    CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY = fields.Boolean(string='Chỉ lấy khách hàng có số dư hoặc phát sinh trong kỳ', help='Chỉ lấy khách hàng có số dư hoặc phát sinh trong kỳ',default='True')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
    # các biến thêm mới của các cột trong form báo cáo Nhân viên
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    SO_TIEN_DU_NO_DAU_KY = fields.Float(string='Số tiền', help='Số tiền dư nợ đầu kỳ',digits= decimal_precision.get_precision('VND'))
    QUY_DOI_DU_NO_DAU_KY = fields.Float(string='Quy đổi', help='Quy đổi dư nợ đầu kỳ',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_DU_CO_DAU_KY = fields.Float(string='Số tiền', help='Số tiền dư có đầu kỳ',digits=decimal_precision.get_precision('VND'))
    QUY_DOI_DU_CO_DAU_KY = fields.Float(string='Quy đổi', help='Quy đổi dư có đầu kỳ',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_PHAT_SINH_NO = fields.Float(string='Số tiền', help='Số tiền phát sinh nợ',digits=decimal_precision.get_precision('VND'))
    QUY_DOI_PHAT_SINH_NO = fields.Float(string='Quy đổi', help='Quy đổi phát sinh nợ',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_PHAT_SINH_CO = fields.Float(string='Số tiền', help='Số tiền phát sinh có',digits= decimal_precision.get_precision('VND'))
    QUY_DOI_PHAT_SINH_CO = fields.Float(string='Quy đổi', help='Quy đổi phát sinh có',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_DU_NO_CUOI_KY = fields.Float(string='Số tiền', help='Số tiền dư nợ cuối kỳ',digits=decimal_precision.get_precision('VND'))
    QUY_DOI_DU_NO_CUOI_KY = fields.Float(string='Quy đổi', help='Quy đổi dư nợ cuối kỳ',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_DU_CO_CUOI_KY = fields.Float(string='Số tiền', help='Số tiền dư có cuối kỳ',digits=decimal_precision.get_precision('VND'))
    QUY_DOI_DU_CO_CUOI_KY = fields.Float(string='Quy đổi', help='Quy đổi dư có cuối kỳ',digits=decimal_precision.get_precision('VND'))
    #  các biến thêm mới cho form báo cáo khi khi selection theo Công trình
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    #  các biến thêm mới cho form báo cáo khi khi selection theo Đơn hàng
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Char(string='Ngày đơn hàng', help='Ngày đơn hàng')
    # các biến thêm mới cho form báo cáo khi khi selection theo Chi tiết theo các khoản giảm trừ
    SO_DU_DAU_KY = fields.Float(string='Số dư đầu kỳ', help='Số dư đầu kỳ',digits= decimal_precision.get_precision('VND'))
    SO_PHAI_THU = fields.Float(string='Số phải thu', help='Số phải thu',digits= decimal_precision.get_precision('VND'))
    CHIET_KHAU = fields.Float(string='Chiết khấu', help='Chiết khấu',digits= decimal_precision.get_precision('VND'))
    TRA_LAI_HOAC_GIAM_GIA = fields.Float(string='Trả lại/Giảm giá', help='Trả lại/Giảm giá',digits= decimal_precision.get_precision('VND'))
    CK_THANH_TOAN_HOAC_GT_KHAC = fields.Float(string='CK thanh toán/Giảm trừ khác ', help='CK thanh toán/Giảm trừ khác',digits= decimal_precision.get_precision('VND'))
    SO_DA_THU = fields.Float(string='Số đã thu ', help='Số đã thu',digits= decimal_precision.get_precision('VND'))
    SO_DU_CUOI_KY = fields.Float(string='Số dư cuối kỳ ', help='Số dư cuối kỳ',digits= decimal_precision.get_precision('VND'))
    # các biến thêm mới cho form báo cáo khi khi selection theo Đơn vị kinh doanh
    TEN_DON_VI =  fields.Char(string='Tên đơn vị', help='Tên đơn vị')
    Ten_khach_hang = fields.Char(string='Tên khách hàng',help='Tên khách hàng')
    # các biến thêm mới cho form báo cáo khi khi selection theo hợp đồng
    HOP_DONG_HOAC_DU_AN = fields.Char(string ='Hợp đồng/dự án', help='Hợp đồng/dự án')

    chi_tiet = fields.Selection([
        ('theo_hop_dong', 'Theo hợp đồng'),
        ('theo_du_an', 'Theo dự án'),
        ], default='theo_hop_dong', store=False)

    NHAN_VIEN_IDS = fields.One2many('res.partner')
    NHAN_VIEN_IDS_Nhanvienvakhachhang = fields.One2many('res.partner')


    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner','tong_hop_cong_no_phai_thu_kh_res_partner', domain=[('LA_KHACH_HANG', '=', True)], string='Chọn KH', help='Chọn khách hàng')
    MA_PC_NHOM_KH = fields.Char()

    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','tong_hop_cong_no_phai_thu_kh_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')

    KHACH_HANG_IDS = fields.One2many('res.partner')
    KHACH_HANG_IDS_Nhanvienvakhachhang = fields.One2many('res.partner')
    KHACH_HANG_IDS_Congtrinh = fields.One2many('res.partner')
    KHACH_HANG_IDS_Hopdong = fields.One2many('res.partner')
    KHACH_HANG_IDS_Dondathang = fields.One2many('res.partner')
    KHACH_HANG_IDS_Donvikinhdoanh = fields.One2many('res.partner')
    KHACH_HANG_IDS_Chitiettheocackhoangiamtru = fields.One2many('res.partner')

    CHON_TAT_CA_DON_VI_KINH_DOANH = fields.Boolean('Tất cả đơn vị kinh doanh', default=True)
    DON_VI_KINH_DOANH_MANY_IDS = fields.Many2many('danh.muc.to.chuc','tong_hop_cong_no_phai_thu_kh_dmtc', string='Chọn đơn vị kinh doanh')

    DON_VI_KINH_DOANH_IDS =  fields.One2many('danh.muc.to.chuc')

    CHON_TAT_CA_DON_DAT_HANG = fields.Boolean('Tất cả đơn đặt hàng', default=True)
    DON_DAT_HANG_MANY_IDS = fields.Many2many('account.ex.don.dat.hang', 'tong_hop_cong_no_phai_thu_kh_ddh', string='Chọn đơn đặt hàng')
    DON_DAT_HANG_IDS = fields.One2many('account.ex.don.dat.hang')

    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_cong_no_phai_thu_kh_ct', string='Chọn công trình')
    CONG_TRINH_IDS = fields.One2many('danh.muc.cong.trinh')

    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','tong_hop_cong_no_phai_thu_kh_hd', string='Chọn hợp đồng')
    HOP_DONG_IDS = fields.One2many('sale.ex.hop.dong.ban')

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):

        self.NHOM_KH_ID = False
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
    @api.onchange('KHACH_HANG_IDS','KHACH_HANG_IDS_Nhanvienvakhachhang','KHACH_HANG_IDS_Congtrinh','KHACH_HANG_IDS_Hopdong','KHACH_HANG_IDS_Dondathang','KHACH_HANG_IDS_Donvikinhdoanh','KHACH_HANG_IDS_Chitiettheocackhoangiamtru')
    def update_KHACH_HANG_IDS(self):
        if self.THONG_KE_THEO == 'KHONG_CHON':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_Nhanvienvakhachhang.ids
        elif self.THONG_KE_THEO == 'CONG_TRINH':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_Congtrinh.ids
        elif self.THONG_KE_THEO == 'HOP_DONG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_Hopdong.ids
        elif self.THONG_KE_THEO == 'DON_DAT_HANG':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_Dondathang.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_Donvikinhdoanh.ids
        elif self.THONG_KE_THEO == 'CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU':
            self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS_Chitiettheocackhoangiamtru.ids
        
    @api.onchange('NHOM_KH_ID')
    def update_NHOM_KHACH_HANG_ID(self):
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KH_ID.MA_PHAN_CAP

    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        if self.THONG_KE_THEO == 'KHONG_CHON':
            self.KHACH_HANG_IDS = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.KHACH_HANG_IDS_Nhanvienvakhachhang = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'CONG_TRINH':
            self.KHACH_HANG_IDS_Congtrinh = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'HOP_DONG':
            self.KHACH_HANG_IDS_Hopdong = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'DON_DAT_HANG':
            self.KHACH_HANG_IDS_Dondathang = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            self.KHACH_HANG_IDS_Donvikinhdoanh = self.KHACH_HANG_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU':
            self.KHACH_HANG_IDS_Chitiettheocackhoangiamtru = self.KHACH_HANG_MANY_IDS.ids
    # end khách hàng
    
    # Nhân viên
    @api.onchange('NHAN_VIEN_IDS','NHAN_VIEN_IDS_Nhanvienvakhachhang')
    def update_NHAN_VIEN_IDS(self):
        if self.THONG_KE_THEO == 'NHAN_VIEN':
            self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS_Nhanvienvakhachhang.ids
        
    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        if self.THONG_KE_THEO == 'NHAN_VIEN':
            self.NHAN_VIEN_IDS = self.NHAN_VIEN_MANY_IDS.ids
        elif self.THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            self.NHAN_VIEN_IDS_Nhanvienvakhachhang = self.NHAN_VIEN_MANY_IDS.ids
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
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        if TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN


        currency_id =  params['currency_id'] if 'currency_id' in params.keys() and params['currency_id'] != 'False' else None
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        NHOM_KH_ID =  params['NHOM_KH_ID'] if 'NHOM_KH_ID' in params.keys() and params['NHOM_KH_ID'] != 'False' else None
        CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY = 1 if 'CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY' in params.keys() and params['CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY'] != 'False' else 0

       
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


        params_sql = {
               'TU_NGAY':TU_NGAY_F, 
               'DEN_NGAY':DEN_NGAY_F, 
               'KHACH_HANG_IDS' : KHACH_HANG_IDS or None,
               'NHAN_VIEN_IDS' : NHAN_VIEN_IDS or None,
               'CHI_NHANH_ID' : CHI_NHANH_ID,
               'DON_DAT_HANGIDS' : DON_DAT_HANG_IDS or None,
               'DV_KINH_DOANH_IDS' : DON_VI_KINH_DOANH_IDS or None,
               'CONG_TRINHIDS' : CONG_TRINH_IDS or None,
               'HOP_DONGIDS' : HOP_DONG_IDS or None,
               'currency_id' : currency_id,
               'TAI_KHOAN_ID' : TAI_KHOAN_ID,
               'NHOM_KH_ID' : NHOM_KH_ID,
               'CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY' : CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY,
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
        # Thống kê theo nhân viên và khách hàng
        elif THONG_KE_THEO=='NHAN_VIEN_VA_KHACH_HANG' :
            return self._lay_bao_cao_thong_ke_theo_nhan_vien_vs_khach_hang(params_sql)
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
        # sql : Thống kê theo Không chọn
    def _lay_bao_cao_thong_ke_theo_khong_chon(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
            DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--tham số từ

                den_ngay                            DATE := %(DEN_NGAY)s;--tham số đến

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--tham số bao gồm số liệu chi nhánh phụ thuộc

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;--tham số chi nhánh


                so_tai_khoan                         VARCHAR(127) := %(TAI_KHOAN_ID)s;--tham số tài khoản

                loai_tien_id                        INTEGER := %(currency_id)s;--tham số loại tiền

                 chi_lay_kh_co_so_du_hoac_phat_sinh_trong_ky INTEGER :=%(CHI_LAY_KHACH_HANG_CO_SO_DU_HOAC_PHAT_SINH_TRONG_KY)s;--tham số chỉ lấy khách hàng có số dư phát sinh trong kỳ

                 KHACH_HANG_IDS                    INTEGER := -1;

                FirstDateOfYear                   DATE := to_date(CONCAT(DATE_PART('year',tu_ngay::date),'-01-01'),'YYYYMMDD');



                rec                                 RECORD;



    BEGIN
        DROP TABLE IF EXISTS TMP_LIST_BRAND
                ;

                CREATE TEMP TABLE TMP_LIST_BRAND
                    AS
                        SELECT *
                        FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
                ;


                 DROP TABLE IF EXISTS DS_KHACH_HANG
                ;

                CREATE TEMP TABLE DS_KHACH_HANG
                    AS
                         SELECT
                            AO.id AS "KHAC_HANG_ID",
                            AO."LIST_MA_NHOM_KH_NCC"  -- Mã nhóm NCC

                FROM    res_partner AS AO

                WHERE  AO."LA_KHACH_HANG" = '1'
                       AND
                       (id = any(%(KHACH_HANG_IDS)s))     --tham số khách hàng
                        OR ( KHACH_HANG_IDS IS NULL

                            )
                ;





        DROP TABLE IF EXISTS TMP_TAI_KHOAN;
        IF so_tai_khoan IS NOT NULL
            THEN
                 CREATE TEMP TABLE TMP_TAI_KHOAN
                    AS
                        SELECT  A."SO_TAI_KHOAN" ,
                                A."TEN_TAI_KHOAN" ,
                                A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent",
                                A."TINH_CHAT"
                        FROM    danh_muc_he_thong_tai_khoan AS A
                        WHERE   "SO_TAI_KHOAN" = so_tai_khoan
                        ORDER BY A."SO_TAI_KHOAN" ,
                                A."TEN_TAI_KHOAN";

        ELSE
                 CREATE TEMP TABLE TMP_TAI_KHOAN
                    AS
                        SELECT  A."SO_TAI_KHOAN" ,
                                A."TEN_TAI_KHOAN" ,
                                A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent",
                                A."TINH_CHAT"
                        FROM    danh_muc_he_thong_tai_khoan AS A
                        WHERE   "CHI_TIET_THEO_DOI_TUONG" = '1'
                                AND "DOI_TUONG_SELECTION" = '1'
                                AND "LA_TK_TONG_HOP" = '0'
                        ORDER BY A."SO_TAI_KHOAN" ,
                                A."TEN_TAI_KHOAN";
            END IF;

        -- nmtruong: sửa CR 73195: Lấy lên cột phát sinh lũy kế từ đầu năm
-- 	    FirstDateOfYear TIMESTAMP(3)
-- 	    FirstDateOfYear := '1/1/' || CAST(Year(tu_ngay) AS VARCHAR(4))

        DROP TABLE IF EXISTS TMP_KET_QUA;

          CREATE TEMP TABLE TMP_KET_QUA
                    AS
        SELECT  ROW_NUMBER() OVER ( ORDER BY "MA_DOI_TUONG" ) AS RowNum ,
                "DOI_TUONG_ID" ,
                "MA_DOI_TUONG" ,   -- Mã NCC
                "HO_VA_TEN" ,	-- Tên NCC
                "SO_TAI_KHOAN" , -- Số tài khoản
                "TINH_CHAT" , -- Tính chất tài khoản

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
                SUM("GHI_NO_NGUYEN_TE_CUOI_KY") AS "GHI_NO_NGUYEN_TE_CUOI_KY" ,	-- Phát sinh nợ
                SUM("GHI_NO_CUOI_KY") AS "GHI_NO_CUOI_KY" , -- Phát sinh nợ quy đổi
                SUM("GHI_CO_NGUYEN_TE_CUOI_KY") AS "GHI_CO_NGUYEN_TE_CUOI_KY" , -- Phát sinh có
                SUM("GHI_CO_CUOI_KY") AS "GHI_CO_CUOI_KY" , -- Phát sinh có quy đổi

                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
                ( CASE WHEN "TINH_CHAT" = '0'
                       THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY"
                                + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                       WHEN "TINH_CHAT" = '1' THEN 0
                       ELSE CASE WHEN SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                          - "GHI_CO_NGUYEN_TE_DAU_KY"
                                          + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE") > 0
                                 THEN SUM("GHI_NO_NGUYEN_TE_DAU_KY"
                                          - "GHI_CO_NGUYEN_TE_DAU_KY"
                                          + "GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                                 ELSE 0
                            END
                  END ) AS "DU_NO_NGUYEN_TE_CUOI_KY" ,	-- Dư nợ cuối kỳ
                ( CASE WHEN "TINH_CHAT" = '1'
                       THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY" - "GHI_NO_NGUYEN_TE_DAU_KY"
                                - "GHI_NO_NGUYEN_TE" + "GHI_CO_NGUYEN_TE")
                       WHEN "TINH_CHAT" = '0' THEN 0
                       ELSE CASE WHEN ( SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                            - "GHI_NO_NGUYEN_TE_DAU_KY"
                                            - "GHI_NO_NGUYEN_TE" + "GHI_CO_NGUYEN_TE") ) > 0
                                 THEN SUM("GHI_CO_NGUYEN_TE_DAU_KY"
                                          - "GHI_NO_NGUYEN_TE_DAU_KY"
                                          - "GHI_NO_NGUYEN_TE" + "GHI_CO_NGUYEN_TE")
                                 ELSE 0
                            END
                  END ) AS "DU_CO_NGUYEN_TE_CUOI_KY" ,	-- Dư có cuối kỳ
                ( CASE WHEN "TINH_CHAT" = '0'
                       THEN SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY"
                                + "GHI_NO" - "GHI_CO")
                       WHEN "TINH_CHAT" = '1' THEN 0
                       ELSE CASE WHEN SUM("GHI_NO_DAU_KY"
                                          - "GHI_CO_DAU_KY"
                                          - "GHI_CO" + "GHI_NO") > 0
                                 THEN SUM("GHI_NO_DAU_KY"
                                          - "GHI_CO_DAU_KY"
                                          - "GHI_CO" + "GHI_NO")
                                 ELSE 0
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

        FROM    ( SELECT    AOL."DOI_TUONG_ID" ,
                            AOL."MA_DOI_TUONG" ,   -- Mã NCC
                            AO."HO_VA_TEN" ,	-- Tên NCC lấy trên danh mục

                            TBAN."SO_TAI_KHOAN" , -- TK công nợ
                            TBAN."TINH_CHAT" , -- Tính chất tài khoản
                            CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                 THEN AOL."GHI_NO_NGUYEN_TE"
                                 ELSE 0
                            END AS "GHI_NO_NGUYEN_TE_DAU_KY" ,	-- Dư nợ Đầu kỳ
                            CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                 THEN AOL."GHI_NO"
                                 ELSE 0
                            END AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
                            CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                 THEN AOL."GHI_CO_NGUYEN_TE"
                                 ELSE 0
                            END AS "GHI_CO_NGUYEN_TE_DAU_KY" , -- Dư có đầu kỳ
                            CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay
                                 THEN AOL."GHI_CO"
                                 ELSE 0
                            END AS "GHI_CO_DAU_KY" , -- Dư có đầu kỳ quy đổi
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN AOL."GHI_NO_NGUYEN_TE"
                                 ELSE 0
                            END AS "GHI_NO_NGUYEN_TE" , -- Phát sinh nợ
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN AOL."GHI_NO"
                                 ELSE 0
                            END AS "GHI_NO" , -- Phát sinh nợ quy đổi
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN AOL."GHI_CO_NGUYEN_TE"
                                 ELSE 0
                            END AS "GHI_CO_NGUYEN_TE" , -- Phát sinh có
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN AOL."GHI_CO"
                                 ELSE 0
                            END AS "GHI_CO" ,
                            -- Lấy lên cột lũy kế từ đầu năm
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN FirstDateOfYear AND den_ngay
                                 THEN AOL."GHI_NO_NGUYEN_TE"
                                 ELSE 0
                            END AS "GHI_NO_NGUYEN_TE_CUOI_KY" , -- Phát sinh nợ
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN FirstDateOfYear AND den_ngay
                                 THEN AOL."GHI_NO"
                                 ELSE 0
                            END AS "GHI_NO_CUOI_KY" , -- Phát sinh nợ quy đổi
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN FirstDateOfYear AND den_ngay
                                 THEN AOL."GHI_CO_NGUYEN_TE"
                                 ELSE 0
                            END AS "GHI_CO_NGUYEN_TE_CUOI_KY" , -- Phát sinh có
                            CASE WHEN AOL."NGAY_HACH_TOAN" BETWEEN FirstDateOfYear AND den_ngay
                                 THEN AOL."GHI_CO"
                                 ELSE 0
                            END AS "GHI_CO_CUOI_KY"

                  FROM      so_cong_no_chi_tiet AS AOL
                            INNER JOIN res_partner AO ON AO.id = AOL."DOI_TUONG_ID"
                            INNER JOIN TMP_TAI_KHOAN  TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                            INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                            INNER JOIN DS_KHACH_HANG AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHAC_HANG_ID"
                            INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                            LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT
                  WHERE     AOL."NGAY_HACH_TOAN" <= den_ngay

                            AND (loai_tien_id  IS NULL
                                  OR AOL."currency_id" = loai_tien_id
                                )
                            AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'

                ) AS RSNS
        GROUP BY RSNS."DOI_TUONG_ID" ,
                RSNS."MA_DOI_TUONG" ,   -- Mã NCC
                RSNS."HO_VA_TEN" ,	-- Tên NCC

                RSNS."SO_TAI_KHOAN" , -- Số tài khoản
                RSNS."TINH_CHAT"  -- Tính chất tài khoản

        HAVING  SUM("GHI_NO_NGUYEN_TE") <> 0
                OR SUM("GHI_NO") <> 0
                OR SUM("GHI_CO_NGUYEN_TE") <> 0
                OR SUM("GHI_CO") <> 0
                OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0
                OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0
                OR(chi_lay_kh_co_so_du_hoac_phat_sinh_trong_ky = '0' AND (
                 SUM("GHI_NO_NGUYEN_TE_CUOI_KY") <>0	-- Phát sinh nợ
                OR SUM("GHI_NO_CUOI_KY") <>0 -- Phát sinh nợ quy đổi
                OR SUM("GHI_CO_NGUYEN_TE_CUOI_KY") <>0  -- Phát sinh có
                OR SUM("GHI_CO_CUOI_KY")<>0))
        ORDER BY RSNS."MA_DOI_TUONG" ;-- Mã NCC

  END $$
            ;

SELECT 

    "MA_DOI_TUONG" AS "MA_KHACH_HANG",
    "HO_VA_TEN" AS "TEN_KHACH_HANG",
    "SO_TAI_KHOAN" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_NGUYEN_TE_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_NGUYEN_TE_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO_NGUYEN_TE" AS "NO_SO_PHAT_SINH",
    "GHI_CO_NGUYEN_TE" AS "CO_SO_PHAT_SINH",
    "DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
   
FROM TMP_KET_QUA --WHERE "MA_DOI_TUONG" ='CTY_BAOOANH';
OFFSET %(offset)s
LIMIT %(limit)s;
        """
        return self.execute(query,params_sql)

    def _lay_bao_cao_thong_ke_theo_nhan_vien(self, params_sql):
        record = []
        query ="""
        ---BAO_CAO_TONG_HOP_CONG_NO_PHAI_THU_KHACH_HANG --nhân viên
DO LANGUAGE plpgsql $$
DECLARE
                tu_ngay                             DATE := %(TU_NGAY)s;--tham số từ

                den_ngay                            DATE := %(DEN_NGAY)s;--tham số đến

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;--tham số bao gồm số liệu chi nhánh phụ thuộc

                chi_nhanh_id                        INTEGER :=  %(CHI_NHANH_ID)s;--tham số chi nhánh


                so_tai_khoan                         VARCHAR(127) := %(TAI_KHOAN_ID)s;--tham số tài khoản

                loai_tien_id                        INTEGER :=  %(currency_id)s;--tham số loại tiền



                


                 rec                                 RECORD;
                rec_2                                 RECORD;
                CHE_DO_KE_TOAN                       VARCHAR(100);
                LedgerID                            INTEGER;

                CrossAmountOC                       FLOAT;

                CrossAmount                         FLOAT;

                OldRemainAmountOC                   FLOAT;

                OldRemainAmount                     FLOAT;

                RemainAmountOC                      FLOAT;

                RemainAmount                        FLOAT;


BEGIN


    SELECT value INTO CHE_DO_KE_TOAN FROM ir_config_parameter WHERE key = 'he_thong.CHE_DO_KE_TOAN' FETCH FIRST 1 ROW ONLY ;
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT
                AO.id AS "NHAN_VIEN_ID"
                , AO."MA_NHAN_VIEN"
                , AO."HO_VA_TEN"

            FROM res_partner AS AO

            WHERE (id = any (%(NHAN_VIEN_IDS)s)) 

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

    --select *from TMP_TAI_KHOAN

    DROP TABLE IF EXISTS TMP_CONG_NO_DOI_TRU
    ;

    CREATE TEMP TABLE TMP_CONG_NO_DOI_TRU
        AS
            SELECT
                DISTINCT
                G."ID_CHUNG_TU_CONG_NO" AS "ID_CHUNG_TU"
                , G."DOI_TUONG_ID"
                , G."MA_TAI_KHOAN"
                , G."currency_id"
                , G."NHAN_VIEN_ID"
                , G."TAI_KHOAN_ID"


            FROM sale_ex_doi_tru_chi_tiet G
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = G."MA_TAI_KHOAN"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
            /*Không lấy số dư đầu kỳ. Với số dư đầu kỳ lấy theo đúng thông tin trên tab chi tiết*/
            WHERE G."LOAI_CHUNG_TU_CONG_NO" NOT IN ('612', '613', '614')

    ;




    DROP TABLE IF EXISTS TMP_CHUNG_TU_THANH_TOAN
    ;

     DROP SEQUENCE IF EXISTS TMP_CHUNG_TU_THANH_TOAN_seq
    ;

    CREATE TEMP SEQUENCE TMP_CHUNG_TU_THANH_TOAN_seq
    ;

    CREATE TEMP TABLE TMP_CHUNG_TU_THANH_TOAN

        (

         RowNum             INT   DEFAULT NEXTVAL('TMP_CHUNG_TU_THANH_TOAN_seq')
            PRIMARY KEY,
        "ID_CHUNG_TU"     INT
         ,"MODEL_CHUNG_TU"   CHAR(36)
        ,
        "DOI_TUONG_ID"     INT

        ,
        "MA_TAI_KHOAN"       VARCHAR(127)
        ,
        "currency_id"   INT
        ,
        "NHAN_VIEN_ID"    INT
        ,
        "SO_TIEN_THANH_TOAN"   FLOAT
        ,
        "SO_TIEN_THANH_TOAN_QUY_DOI"    FLOAT
        ,
        "NGAY_HACH_TOAN_CONG_NO"      DATE
        ,"SO_CHUNG_TU_CONG_NO"   VARCHAR(127)
        ,
        "SO_HOA_DON_CONG_NO"    VARCHAR(127)
         ,"ID_CHUNG_TU_CONG_NO"   INT
        ,
        "MODEL_CHUNG_TU_CONG_NO"    VARCHAR(200)


        );




    INSERT INTO TMP_CHUNG_TU_THANH_TOAN
        (
            "ID_CHUNG_TU"
            ,"MODEL_CHUNG_TU"
        ,
        "DOI_TUONG_ID"

        ,
        "MA_TAI_KHOAN"
        ,
        "currency_id"
        ,
        "NHAN_VIEN_ID"
        ,
        "SO_TIEN_THANH_TOAN"
        ,
        "SO_TIEN_THANH_TOAN_QUY_DOI"
        ,
        "NGAY_HACH_TOAN_CONG_NO"
        ,"SO_CHUNG_TU_CONG_NO"
        ,
        "SO_HOA_DON_CONG_NO"
         ,"ID_CHUNG_TU_CONG_NO"
        ,
        "MODEL_CHUNG_TU_CONG_NO"
        )
            SELECT
                  G."ID_CHUNG_TU_THANH_TOAN"                   AS "ID_CHUNG_TU"
                  ,G."MODEL_CHUNG_TU_THANH_TOAN"                   AS "MODEL_CHUNG_TU"
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
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = G."MA_TAI_KHOAN"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
            GROUP BY
                G."ID_CHUNG_TU_THANH_TOAN"
                ,G."MODEL_CHUNG_TU_THANH_TOAN"
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
                 ,'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                , SUM(AL."GHI_CO_NGUYEN_TE") AS "SO_TIEN_THANH_TOAN"
                , SUM(AL."GHI_CO")           AS "SO_TIEN_THANH_TOAN_QUY_DOI"
                --, SAV."id"
                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"
                , 'sale.document'            AS "MODEL_CHUNG_TU_CHI_TIET"
            FROM sale_ex_tra_lai_hang_ban_chi_tiet SARD
                INNER JOIN so_cong_no_chi_tiet AL
                    ON (SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet')
                INNER JOIN sale_document SAV ON SAV."id" = SARD."SO_CHUNG_TU_ID"
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
                 ,'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                , SUM(AL."GHI_CO_NGUYEN_TE") AS "SO_TIEN_THANH_TOAN"
                , SUM(AL."GHI_CO")           AS "SO_TIEN_THANH_TOAN_QUY_DOI"
                --, SAV."id"
                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"
                , 'sale.document'            AS "MODEL_CHUNG_TU_CHI_TIET"
            FROM sale_ex_chi_tiet_giam_gia_hang_ban SARD
                INNER JOIN so_cong_no_chi_tiet AL
                    ON (SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL" = 'sale.ex.chi.tiet.giam.gia.hang.ban')
                INNER JOIN sale_document SAV ON SAV."id" = SARD."CHUNG_TU_BAN_HANG_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = AL."MA_TK"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
            WHERE SARD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
            GROUP BY
                SARD."GIAM_GIA_HANG_BAN_ID"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                --, SAV."id"
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
        RowNum             INT   DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,
        "NHAN_VIEN_ID"     INT
        ,
        "DOI_TUONG_ID"     INT

        ,
        "ID_CHUNG_TU"      INT
        ,
        "MODEL_CHUNG_TU"   CHAR(36)
        ,
        "LOAI_CHUNG_TU"    INT
        ,
        "NGAY_HACH_TOAN"   DATE
        ,
        "NGAY_CHUNG_TU"    DATE
        ,
        "SO_CHUNG_TU"      VARCHAR(22)


        ,
        "MA_TK"            VARCHAR(255)

        ,
        "GHI_NO_NGUYEN_TE" FLOAT
        ,
        "GHI_NO"           FLOAT
        ,
        "GHI_CO_NGUYEN_TE" FLOAT
        ,
        "GHI_CO"           FLOAT
        ,

        "OrderType"        INT
        ,
        "LedgerID"         INT
        ,
        "currency_id"      INT
        ,
        "DebtRefID"        INT
        ,
        "DebtRefModel"     VARCHAR(255)

        ,
        "CrossAmount"      FLOAT DEFAULT (0)
        ,
        "CrossAmountOC"    FLOAT DEFAULT (0)
        ,
        "IsCrossRow"       BOOLEAN   DEFAULT (FALSE )
        ,
        "CHI_TIET_ID"      INT

        ,
        "CHI_TIET_MODEL"   VARCHAR(255)
          ,"SO_HOA_DON"      VARCHAR(22)


    )
    ;


    INSERT INTO TMP_KET_QUA
    ("NHAN_VIEN_ID"
        , "DOI_TUONG_ID"
        , "ID_CHUNG_TU"
        , "MODEL_CHUNG_TU"
        , "LOAI_CHUNG_TU"
        , "NGAY_HACH_TOAN"
        , "NGAY_CHUNG_TU"
        , "SO_CHUNG_TU"
        , "MA_TK"

        , "GHI_NO_NGUYEN_TE"
        , "GHI_NO"
        , "GHI_CO_NGUYEN_TE"
        , "GHI_CO"
        , "OrderType"
        , "LedgerID"
        , "currency_id"
        , "DebtRefID"
        , "DebtRefModel"
        , "CHI_TIET_ID"
        , "CHI_TIET_MODEL"
        ,"SO_HOA_DON"


    )


        SELECT T.*
        FROM (
                 SELECT
                       COALESCE(GD."NHAN_VIEN_ID", AL."NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                     , AL."DOI_TUONG_ID"

                     , AL."ID_CHUNG_TU"
                     , AL."MODEL_CHUNG_TU"
                     , AL."LOAI_CHUNG_TU"
                     , AL."NGAY_HACH_TOAN"
                     , AL."NGAY_CHUNG_TU"
                     , AL."SO_CHUNG_TU"

                     , AL."MA_TK"                                     AS "MA_TK"
                     , AL."GHI_NO_NGUYEN_TE"
                     , AL."GHI_NO"
                     , AL."GHI_CO_NGUYEN_TE"
                     , AL."GHI_CO"

                     , 1                                              AS "OrderType"
                     , Al."id"                                        AS "LedgerID"
                     , AL."currency_id"
                     , SA."CHUNG_TU_BAN_HANG_ID"                      AS "DebtRefID"
                     , 'sale.document'                                AS "DebtRefModel"
                     , AL."CHI_TIET_ID"
                     , AL."CHI_TIET_MODEL"
                     , AL."SO_HOA_DON"
                 FROM so_cong_no_chi_tiet Al
                     INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
                     INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = Al."MA_TK"
                     LEFT JOIN TMP_CONG_NO_DOI_TRU GD ON AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU"
                                                         AND AL."TK_ID" = GD."TAI_KHOAN_ID" AND
                                                         AL."DOI_TUONG_ID" = GD."DOI_TUONG_ID" AND
                                                         AL."currency_id" = GD."currency_id"

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
                               ) SA ON (SA.id = AL."CHI_TIET_ID" AND
                                        AL."CHI_TIET_MODEL" = SA."model_chung_tu")
                 WHERE (AL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)

                       AND (AL."currency_id" = loai_tien_id OR loai_tien_id IS NULL)
                       AND (AL."GHI_NO_NGUYEN_TE" <> 0 OR AL."GHI_NO" <> 0 OR AL."GHI_CO_NGUYEN_TE" <> 0 OR
                            AL."GHI_CO" <> 0)


                 UNION ALL
                 /*Số dư đầu kỳ*/
                 SELECT
                       COALESCE(GD."NHAN_VIEN_ID", AL."NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                     , AL."DOI_TUONG_ID"

                     , AL."ID_CHUNG_TU"
                     , AL."MODEL_CHUNG_TU"
                     , NULL                                           AS "LOAI_CHUNG_TU"
                     , NULL :: DATE                                   AS "NGAY_HACH_TOAN"
                     , NULL                                           AS "NGAY_CHUNG_TU"
                     , NULL                                           AS "SO_CHUNG_TU"

                     , AL."MA_TK"                                     AS "MA_TK"
                     , AL."GHI_NO_NGUYEN_TE"
                     , AL."GHI_NO"
                     , AL."GHI_CO_NGUYEN_TE"
                     , AL."GHI_CO"

                     , 0                                              AS "OrderType"

                     , Al."id"                                        AS "LedgerID"
                     , AL."currency_id"
                     , SA."CHUNG_TU_BAN_HANG_ID"                      AS "DebtRefID"
                     , 'sale.document'                                AS "DebtRefModel"
                     , AL."CHI_TIET_ID"
                     , AL."CHI_TIET_MODEL"
                     , NULL                                           AS "SO_HOA_DON"
                 FROM so_cong_no_chi_tiet Al
                     INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
                     INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = Al."MA_TK"
                     LEFT JOIN TMP_CONG_NO_DOI_TRU GD ON AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU"
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
                               ) SA ON (SA.id = AL."CHI_TIET_ID" AND
                                        AL."CHI_TIET_MODEL" = SA."model_chung_tu")
                 WHERE (AL."NGAY_HACH_TOAN" < tu_ngay)

                       AND (AL."currency_id" = loai_tien_id OR loai_tien_id IS NULL)
                       AND (AL."GHI_NO_NGUYEN_TE" <> 0 OR AL."GHI_NO" <> 0 OR AL."GHI_CO_NGUYEN_TE" <> 0 OR
                            AL."GHI_NO" <> 0)
             ) T
        ORDER BY

            T."NGAY_HACH_TOAN" NULLS FIRST,
            T."SO_CHUNG_TU" NULLS FIRST,
            T."SO_HOA_DON" NULLS FIRST,
            T."MA_TK" NULLS FIRST,
              T."GHI_CO" NULLS FIRST,
            T."GHI_NO" NULLS FIRST,

            T."ID_CHUNG_TU" NULLS FIRST,
            T."DOI_TUONG_ID" NULLS FIRST,
            T."currency_id" NULLS FIRST,

            "CHI_TIET_ID" NULLS FIRST,
            "CHI_TIET_MODEL" NULLS FIRST

    ;




    FOR rec IN
     SELECT
            ROW_NUMBER() OVER ( ORDER BY
                                GP."NGAY_HACH_TOAN_CONG_NO" NULLS FIRST,
                                GP."SO_CHUNG_TU_CONG_NO" NULLS FIRST,
                                GP."SO_HOA_DON_CONG_NO" NULLS FIRST,
                                 GP."SO_TIEN_THANH_TOAN_QUY_DOI" NULLS FIRST
                ) AS "Rownum"
          ,GP."ID_CHUNG_TU"                AS "PayRefID"
         ,GP."MODEL_CHUNG_TU"                AS "PayRef_model_ID"
        , GP."DOI_TUONG_ID"               AS "PayAccountObject"
        , GP."NHAN_VIEN_ID"               AS "PayEmployee"
        , GP."MA_TAI_KHOAN"               AS "PayAccountNumber"
        , GP."currency_id"                AS "PayCurrency"

        , GP."SO_TIEN_THANH_TOAN"         AS "PayAmountOC"
        , GP."SO_TIEN_THANH_TOAN_QUY_DOI" AS "PayAmount"
        , GP."ID_CHUNG_TU_CONG_NO"        AS "ID_CHUNG_TU_CONG_NO"
        , GP."MODEL_CHUNG_TU_CONG_NO"     AS "MODEL_CHUNG_TU_CONG_NO"
         ,GP."NGAY_HACH_TOAN_CONG_NO"
        ,GP."SO_CHUNG_TU_CONG_NO"
        ,GP."SO_HOA_DON_CONG_NO"

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

     FOR rec_2 IN  select * FROM TMP_KET_QUA
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
                        COALESCE(rec_2."GHI_CO",0)
                ELSE
                    COALESCE(RemainAmount, 0) END)
        INTO OldRemainAmount;

          SELECT (CASE WHEN COALESCE(LedgerID, 0) <> rec_2."LedgerID"
            THEN
                COALESCE( rec_2."GHI_CO_NGUYEN_TE",0)
                ELSE RemainAmountOC END)
        INTO OldRemainAmountOC;

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
        SET "CrossAmount"           = CrossAmount,
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
        INTO LedgerID;

        UPDATE TMP_KET_QUA
        SET "LedgerID"           = rec_2."LedgerID"

        WHERE RowNum = rec_2.RowNum
    ;



END LOOP ;

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
                          ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL )
                          OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND rec."MODEL_CHUNG_TU_CONG_NO"="DebtRefModel"))
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


                    , "ID_CHUNG_TU"
                    , "MODEL_CHUNG_TU"
                    , "LOAI_CHUNG_TU"
                    , "NGAY_HACH_TOAN"
                    , "NGAY_CHUNG_TU"
                    , "SO_CHUNG_TU"
                    , "MA_TK"
                    , "GHI_NO_NGUYEN_TE"
                    , "GHI_NO"
                    , "GHI_CO_NGUYEN_TE"
                    , "GHI_CO"
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
                        , "ID_CHUNG_TU"
                        , "MODEL_CHUNG_TU"
                        , "LOAI_CHUNG_TU"
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , "SO_CHUNG_TU"
                        , "MA_TK"
                        , "GHI_NO_NGUYEN_TE"
                        , "GHI_NO"
                        , "CrossAmountOC"
                        , "CrossAmount"
                        , "OrderType"
                        , "LedgerID"
                        , "currency_id"
                        , "DebtRefID"
                        , TRUE                        AS "IsCrossRow"
                        , "CHI_TIET_ID"
                        , "CHI_TIET_MODEL"

                    FROM TMP_KET_QUA
                    WHERE "ID_CHUNG_TU" = rec."PayRefID"
                          and "MODEL_CHUNG_TU" = rec."PayRef_model_ID"
                          AND "DOI_TUONG_ID" = rec."PayAccountObject"
                          AND "MA_TK" = rec."PayAccountNumber"
                          AND "currency_id" = rec."PayCurrency"
                          AND (
                              ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL)
                              OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND
                                  rec."MODEL_CHUNG_TU_CONG_NO"="DebtRefModel"))
                          AND "IsCrossRow" = FALSE
                          AND ("GHI_CO_NGUYEN_TE" <> 0
                                    OR "GHI_CO" <> 0 )
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
                           ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO"  IS NULL)
                              OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND  rec."MODEL_CHUNG_TU_CONG_NO"="DebtRefModel"))
                      AND "IsCrossRow" = FALSE
            ;
 END LOOP
    ;



         DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
        ;

        CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
            AS
                SELECT
                      ROW_NUMBER()
                      OVER (
                          ORDER BY "MA_NHAN_VIEN" ) AS "RowNum"

                    , R."NHAN_VIEN_ID"
                    , E."MA_NHAN_VIEN"
                    , E."HO_VA_TEN"
                    , R."MA_TK"
                    , AC."TINH_CHAT"

                    , (CASE WHEN ("TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_NO" - "GHI_CO")
                                                                                  ELSE 0 END) >= 0))
                    THEN SUM(CASE WHEN R."OrderType" = 0
                        THEN ("GHI_NO" - "GHI_CO")
                             ELSE 0 END)
                       ELSE 0
                       END)                         AS "GHI_NO_DAU_KY"
                    , (CASE WHEN ("TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                                                                                  ELSE 0 END) >= 0))
                    THEN SUM(CASE WHEN R."OrderType" = 0
                        THEN ("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                             ELSE 0 END)
                       ELSE 0
                       END)                         AS "GHI_NO_NGUYEN_TE_DAU_KY"
                    , (CASE WHEN ("TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_CO" - "GHI_NO")
                                                                                  ELSE 0 END) >= 0))
                    THEN SUM(CASE WHEN R."OrderType" = 0
                        THEN ("GHI_CO" - "GHI_NO")
                             ELSE 0 END)
                       ELSE 0
                       END)                         AS "GHI_CO_DAU_KY"
                    , (CASE WHEN ("TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                                                                                  ELSE 0 END) >= 0))
                    THEN SUM(CASE WHEN R."OrderType" = 0
                        THEN ("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                             ELSE 0 END)
                       ELSE 0
                       END)                         AS "GHI_CO_NGUYEN_TE_DAU_KY"

                    , SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_NO", 0)
                          ELSE 0 END)               AS "GHI_NO"
                    , SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_NO_NGUYEN_TE", 0)
                          ELSE 0 END)               AS "GHI_NO_NGUYEN_TE"
                    , SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_CO", 0)
                          ELSE 0 END)               AS "GHI_CO"
                    , SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_CO_NGUYEN_TE", 0)
                          ELSE 0 END)               AS "GHI_CO_NGUYEN_TE"

                    , (CASE WHEN "TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND SUM("GHI_NO" - "GHI_CO") >= 0)
                    THEN SUM("GHI_NO" - "GHI_CO")
                       ELSE 0 END)                  AS "DU_NO_CUOI_KY"
                    , (CASE WHEN "TINH_CHAT" = '0' OR
                                 ("TINH_CHAT" = '2' AND SUM("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE") >= 0)
                    THEN SUM("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                       ELSE 0 END)                  AS "DU_NO_NGUYEN_TE_CUOI_KY"
                    , (CASE WHEN "TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND SUM("GHI_CO" - "GHI_NO") >= 0)
                    THEN SUM("GHI_CO" - "GHI_NO")
                       ELSE 0 END)                  AS "DU_CO_CUOI_KY"
                    , (CASE WHEN "TINH_CHAT" = '1' OR
                                 ("TINH_CHAT" = '2' AND SUM("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") >= 0)
                    THEN SUM("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                       ELSE 0 END)                  AS "DU_CO_NGUYEN_TE_CUOI_KY"

                FROM TMP_KET_QUA R
                    INNER JOIN DS_NHAN_VIEN E ON E."NHAN_VIEN_ID" = R."NHAN_VIEN_ID"
                    INNER JOIN danh_muc_he_thong_tai_khoan AC ON AC."SO_TAI_KHOAN" = R."MA_TK"
                GROUP BY
                    R."NHAN_VIEN_ID"
                    , E."MA_NHAN_VIEN"
                    , E."HO_VA_TEN"
                    , R."MA_TK"
                    , AC."TINH_CHAT"


                HAVING SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_NO" - "GHI_CO")
                           ELSE 0 END) <> 0
                       OR SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                              ELSE 0 END) <> 0
                       OR SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_NO", 0)
                              ELSE 0 END) <> 0
                       OR SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_NO_NGUYEN_TE", 0)
                              ELSE 0 END) <> 0
                       OR SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_CO", 0)
                              ELSE 0 END) <> 0
                       OR SUM(CASE WHEN R."OrderType" = 1
                    THEN COALESCE(R."GHI_CO_NGUYEN_TE", 0)
                              ELSE 0 END) <> 0
                ORDER BY E."MA_NHAN_VIEN"
        ;


END $$
;

SELECT 
    "MA_NHAN_VIEN" AS "MA_NHAN_VIEN",
    "HO_VA_TEN" AS "TEN_NHAN_VIEN",
    "MA_TK" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_NGUYEN_TE_DAU_KY"   AS "SO_TIEN_DU_NO_DAU_KY",
    "GHI_NO_DAU_KY"   AS "QUY_DOI_DU_NO_DAU_KY",
    "GHI_CO_NGUYEN_TE_DAU_KY" AS "SO_TIEN_DU_CO_DAU_KY",
    "GHI_CO_DAU_KY" AS "QUY_DOI_DU_CO_DAU_KY",
    "GHI_NO_NGUYEN_TE" AS "SO_TIEN_PHAT_SINH_NO",
    "GHI_NO" AS "QUY_DOI_PHAT_SINH_NO",
    "GHI_CO_NGUYEN_TE" AS "SO_TIEN_PHAT_SINH_CO",
    "GHI_CO" AS "QUY_DOI_PHAT_SINH_CO",
    "DU_NO_NGUYEN_TE_CUOI_KY" AS "SO_TIEN_DU_NO_CUOI_KY",
    "DU_NO_CUOI_KY" AS "QUY_DOI_DU_NO_CUOI_KY",
    "DU_CO_NGUYEN_TE_CUOI_KY" AS "SO_TIEN_DU_CO_CUOI_KY",
    "DU_CO_CUOI_KY" AS "QUY_DOI_DU_CO_CUOI_KY"
FROM TMP_KET_QUA_CUOI_CUNG
OFFSET %(offset)s
LIMIT %(limit)s;

        """
        return self.execute(query,params_sql)

    def _lay_bao_cao_thong_ke_theo_nhan_vien_vs_khach_hang(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

  

    v_den_ngay                            DATE :=  %(DEN_NGAY)s;

  

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

  

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

   


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;




   


    rec                                 RECORD;
    rec_2                                 RECORD;
    LedgerID                            INTEGER;

    CrossAmountOC                       FLOAT;

    CrossAmount                         FLOAT;

    OldRemainAmountOC                   FLOAT;

    OldRemainAmount                     FLOAT;

    RemainAmountOC                      FLOAT;

    RemainAmount                        FLOAT;


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
    IF  (%(KHACH_HANG_IDS)s) IS NULL
        THEN
		CREATE TEMP TABLE DS_KHACH_HANG
            AS
		    SELECT
                "id" AS "KHACH_HANG_ID"
			   ,"MA_KHACH_HANG"
			   ,"HO_VA_TEN"
			   ,"DIA_CHI"
			   ,"MA_SO_THUE"
			   ,"LIST_MA_NHOM_KH_NCC"
			   ,"LIST_TEN_NHOM_KH_NCC"
			   ,CASE "LOAI_KHACH_HANG" WHEN '0' THEN "DIEN_THOAI" ELSE "DT_DI_DONG" END AS "DIEN_THOAI"
		FROM    res_partner
		WHERE   "LA_KHACH_HANG" = '1';
	ELSE
        CREATE TEMP TABLE DS_KHACH_HANG
            AS

		 SELECT
                "id" AS "KHACH_HANG_ID"
			   ,"MA_KHACH_HANG"
			   ,"HO_VA_TEN"
			   ,"DIA_CHI"
			   ,"MA_SO_THUE"
			   ,"LIST_MA_NHOM_KH_NCC"
			   ,"LIST_TEN_NHOM_KH_NCC"
			   ,CASE "LOAI_KHACH_HANG" WHEN '0' THEN "DIEN_THOAI" ELSE "DT_DI_DONG" END AS "DIEN_THOAI"
		FROM    res_partner
		 WHERE (id = any (%(KHACH_HANG_IDS)s)); 
	END IF;


    DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT
                AO.id AS "NHAN_VIEN_ID"
                , AO."MA_NHAN_VIEN"
                , AO."HO_VA_TEN"

            FROM res_partner AS AO

            WHERE (id = any(%(NHAN_VIEN_IDS)s))  

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
                ORDER BY A."SO_TAI_KHOAN",
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
                ORDER BY A."SO_TAI_KHOAN",
                    A."TEN_TAI_KHOAN"
        ;
    END IF
    ;


    DROP TABLE IF EXISTS TMP_CONG_NO_DOI_TRU
    ;

    CREATE TEMP TABLE TMP_CONG_NO_DOI_TRU
        AS
            SELECT
                DISTINCT
                G."ID_CHUNG_TU_CONG_NO"
                , G."DOI_TUONG_ID"
                , G."MA_TAI_KHOAN"
                , G."currency_id"
                , G."NHAN_VIEN_ID"
                 , G."TAI_KHOAN_ID"

            FROM sale_ex_doi_tru_chi_tiet G
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = G."MA_TAI_KHOAN"
                INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = G."DOI_TUONG_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
            /*Không lấy số dư đầu kỳ. Với số dư đầu kỳ lấy theo đúng thông tin trên tab chi tiết*/
            WHERE G."LOAI_CHUNG_TU_CONG_NO" NOT IN ('612', '613', '614')

    ;

    DROP TABLE IF EXISTS TMP_CHUNG_TU_THANH_TOAN
    ;

    CREATE TEMP TABLE TMP_CHUNG_TU_THANH_TOAN
        AS
            SELECT
                G."ID_CHUNG_TU_THANH_TOAN"                   AS "ID_CHUNG_TU"
                ,G."MODEL_CHUNG_TU_THANH_TOAN"                   AS "MODEL_CHUNG_TU"
                , G."DOI_TUONG_ID"
               , G."MA_TAI_KHOAN"
                , G."currency_id"
                , G."NHAN_VIEN_ID"
                , SUM(G."SO_TIEN_THANH_TOAN")     AS "SO_TIEN_THANH_TOAN"

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
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = G."MA_TAI_KHOAN"
                 INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = G."DOI_TUONG_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
            GROUP BY
                G."ID_CHUNG_TU_THANH_TOAN"
                ,G."MODEL_CHUNG_TU_THANH_TOAN"
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
                 ,'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                , SUM(AL."GHI_CO_NGUYEN_TE") AS "SO_TIEN_THANH_TOAN"
                , SUM(AL."GHI_CO")           AS "SO_TIEN_THANH_TOAN_QUY_DOI"
                --, SAV."id"
                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                , SAV."id"
                , 'sale.document'            AS "MODEL_CHUNG_TU_CHI_TIET"
            FROM sale_ex_tra_lai_hang_ban_chi_tiet SARD
                INNER JOIN so_cong_no_chi_tiet AL
                    ON (SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet')
                INNER JOIN sale_document SAV ON SAV."id" = SARD."SO_CHUNG_TU_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = AL."MA_TK"
                INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = AL."DOI_TUONG_ID"
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
                 ,'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                , SUM(AL."GHI_CO_NGUYEN_TE") AS "SO_TIEN_THANH_TOAN"
                , SUM(AL."GHI_CO")           AS "SO_TIEN_THANH_TOAN_QUY_DOI"
                --, SAV."id"
                , SAV."NGAY_HACH_TOAN"
                , SAV."SO_CHUNG_TU"
                , SAV."SO_HOA_DON"
                 , SAV."id"
                , 'sale.document'            AS "MODEL_CHUNG_TU_CHI_TIET"
            FROM sale_ex_chi_tiet_giam_gia_hang_ban SARD
                INNER JOIN so_cong_no_chi_tiet AL
                    ON (SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL" = 'sale.ex.chi.tiet.giam.gia.hang.ban')
                INNER JOIN sale_document SAV ON SAV."id" = SARD."CHUNG_TU_BAN_HANG_ID"
                INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = AL."MA_TK"
                INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = AL."DOI_TUONG_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
            WHERE SARD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
            GROUP BY
                SARD."GIAM_GIA_HANG_BAN_ID"
                , AL."DOI_TUONG_ID"
                , AL."MA_TK"
                , AL."currency_id"
                , SAV."NHAN_VIEN_ID"
                --, SAV."id"
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
        RowNum             INT   DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,
        "NHAN_VIEN_ID"     INT
        ,
        "DOI_TUONG_ID"     INT

        ,"MA_KHACH_HANG"      VARCHAR(200)
        ,"TEN_KHACH_HANG"      VARCHAR(200)
        ,
        "ID_CHUNG_TU"      INT
        ,
        "MODEL_CHUNG_TU"   CHAR(36)
        ,
        "LOAI_CHUNG_TU"    INT
        ,
        "NGAY_HACH_TOAN"   DATE
        ,
        "NGAY_CHUNG_TU"    DATE
        ,
        "SO_CHUNG_TU"      VARCHAR(22)


        ,
        "MA_TK"            VARCHAR(255)

        ,
        "GHI_NO_NGUYEN_TE" FLOAT
        ,
        "GHI_NO"           FLOAT
        ,
        "GHI_CO_NGUYEN_TE" FLOAT
        ,
        "GHI_CO"           FLOAT
        ,

        "OrderType"        INT
        ,
        "LedgerID"         INT
        ,
        "currency_id"      INT
        ,
        "DebtRefID"        INT
        ,
        "DebtRefModel"     VARCHAR(255)

        ,
        "CrossAmount"      FLOAT DEFAULT (0)
        ,
        "CrossAmountOC"    FLOAT DEFAULT (0)
        ,
        "IsCrossRow"       BOOLEAN   DEFAULT (FALSE )
        ,
        "CHI_TIET_ID"      INT

        ,
        "CHI_TIET_MODEL"   VARCHAR(255)
        ,"SO_HOA_DON"      VARCHAR(22)


    )
    ;
     INSERT INTO TMP_KET_QUA
    (   "NHAN_VIEN_ID"
        , "DOI_TUONG_ID"
        ,"MA_KHACH_HANG"
        ,"TEN_KHACH_HANG"
        , "ID_CHUNG_TU"
        , "MODEL_CHUNG_TU"
        , "LOAI_CHUNG_TU"
        , "NGAY_HACH_TOAN"
        , "NGAY_CHUNG_TU"
        , "SO_CHUNG_TU"
        , "MA_TK"

        , "GHI_NO_NGUYEN_TE"
        , "GHI_NO"
        , "GHI_CO_NGUYEN_TE"
        , "GHI_CO"
        , "OrderType"
        , "LedgerID"
        , "currency_id"
        , "DebtRefID"
        , "DebtRefModel"
        , "CHI_TIET_ID"
        , "CHI_TIET_MODEL"
        ,"SO_HOA_DON"


    )



    SELECT T .*
            FROM (
                     SELECT
                           COALESCE(GD."NHAN_VIEN_ID", AL."NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                         , AL."DOI_TUONG_ID"
                         ,AO."MA_KHACH_HANG"
			             ,AO."HO_VA_TEN"
                         , AL."ID_CHUNG_TU"
                         , AL."MODEL_CHUNG_TU"
                         , AL."LOAI_CHUNG_TU"
                         , AL."NGAY_HACH_TOAN"
                         , AL."NGAY_CHUNG_TU"
                         , AL."SO_CHUNG_TU"

                         , AL."MA_TK"                                     AS "MA_TK"
                         , AL."GHI_NO_NGUYEN_TE"
                         , AL."GHI_NO"
                         , AL."GHI_CO_NGUYEN_TE"
                         , AL."GHI_CO"

                         , 1                                              AS "OrderType"
                         , Al."id"                                        AS "LedgerID"
                         , AL."currency_id"
                         , SA."CHUNG_TU_BAN_HANG_ID"                      AS "DebtRefID"
                         , 'sale.document'                                AS "DebtRefModel"
                         , AL."CHI_TIET_ID"
                         , AL."CHI_TIET_MODEL"
                         , AL."SO_HOA_DON"
                     FROM so_cong_no_chi_tiet Al
                        INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = AL."DOI_TUONG_ID"
                         INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
                         INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = Al."MA_TK"
                         LEFT JOIN TMP_CONG_NO_DOI_TRU GD ON AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU_CONG_NO"
                                                             AND AL."TK_ID" = GD."TAI_KHOAN_ID"
                                                             AND
                                                             AL."DOI_TUONG_ID" = GD."DOI_TUONG_ID" AND
                                                             AL."currency_id" = GD."currency_id"

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
                               ) SA ON (SA.id = AL."CHI_TIET_ID" AND
                                        AL."CHI_TIET_MODEL" = SA."model_chung_tu")
                     WHERE (AL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay)

                           AND (AL."currency_id" = v_loai_tien_id OR v_loai_tien_id IS NULL)
                           AND (AL."GHI_NO_NGUYEN_TE" <> 0 OR AL."GHI_NO" <> 0 OR AL."GHI_CO_NGUYEN_TE" <> 0 OR
                                AL."GHI_CO" <> 0)


                     UNION ALL
                     /*Số dư đầu kỳ*/
                     SELECT
                           COALESCE(GD."NHAN_VIEN_ID", AL."NHAN_VIEN_ID") AS "NHAN_VIEN_ID"
                         , AL."DOI_TUONG_ID"
                         ,AO."MA_KHACH_HANG"
			             ,AO."HO_VA_TEN"
                         , AL."ID_CHUNG_TU"
                         , AL."MODEL_CHUNG_TU"
                         , NULL                                           AS "LOAI_CHUNG_TU"
                         , NULL :: DATE                                   AS "NGAY_HACH_TOAN"
                         , NULL                                           AS "NGAY_CHUNG_TU"
                         , NULL                                           AS "SO_CHUNG_TU"

                         , AL."MA_TK"                                     AS "MA_TK"
                         , AL."GHI_NO_NGUYEN_TE"
                         , AL."GHI_NO"
                         , AL."GHI_CO_NGUYEN_TE"
                         , AL."GHI_CO"

                         , 0                                              AS "OrderType"

                         , Al."id"                                        AS "LedgerID"
                         , AL."currency_id"
                         , SA."CHUNG_TU_BAN_HANG_ID"                      AS "DebtRefID"
                         , 'sale.document'                                AS "DebtRefModel"
                         , AL."CHI_TIET_ID"
                         , AL."CHI_TIET_MODEL"
                         , NULL                                           AS "SO_HOA_DON"
                     FROM so_cong_no_chi_tiet Al
                         INNER JOIN DS_KHACH_HANG AO ON AO."KHACH_HANG_ID" = AL."DOI_TUONG_ID"
                         INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
                         INNER JOIN TMP_TAI_KHOAN AC ON AC."SO_TAI_KHOAN" = Al."MA_TK"
                         LEFT JOIN TMP_CONG_NO_DOI_TRU GD ON AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU_CONG_NO"
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
                               ) SA ON (SA.id = AL."CHI_TIET_ID" AND
                                        AL."CHI_TIET_MODEL" = SA."model_chung_tu")
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
                    T."DOI_TUONG_ID" NULLS FIRST,
                    T."currency_id" NULLS FIRST,

                    "CHI_TIET_ID" NULLS FIRST,
                    "CHI_TIET_MODEL" NULLS FIRST


    ;
     FOR rec IN
     SELECT

          GP."ID_CHUNG_TU"                AS "PayRefID"
         ,GP."MODEL_CHUNG_TU"                AS "PayRef_model_ID"
        , GP."DOI_TUONG_ID"               AS "PayAccountObject"
        , GP."NHAN_VIEN_ID"               AS "PayEmployee"
        , GP."MA_TAI_KHOAN"               AS "PayAccountNumber"
        , GP."currency_id"                AS "PayCurrency"

        , GP."SO_TIEN_THANH_TOAN"         AS "PayAmountOC"
        , GP."SO_TIEN_THANH_TOAN_QUY_DOI" AS "PayAmount"
        , GP."ID_CHUNG_TU_CONG_NO"        AS "ID_CHUNG_TU_CONG_NO"
        , GP."MODEL_CHUNG_TU_CONG_NO"     AS "MODEL_CHUNG_TU_CONG_NO"
         ,GP."NGAY_HACH_TOAN_CONG_NO"
        ,GP."SO_CHUNG_TU_CONG_NO"
        ,GP."SO_HOA_DON_CONG_NO"

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


     FOR rec_2 IN  select * FROM TMP_KET_QUA
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
                        COALESCE(rec_2."GHI_CO",0)
                ELSE
                    COALESCE(RemainAmount, 0) END)
        INTO OldRemainAmount;

          SELECT (CASE WHEN COALESCE(LedgerID, 0) <> rec_2."LedgerID"
            THEN
                COALESCE( rec_2."GHI_CO_NGUYEN_TE",0)
                ELSE RemainAmountOC END)
        INTO OldRemainAmountOC;

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
        SET "CrossAmount"           = CrossAmount,
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
        INTO LedgerID;

        UPDATE TMP_KET_QUA
        SET "LedgerID"           = rec_2."LedgerID"

        WHERE RowNum = rec_2.RowNum
    ;



END LOOP ;

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
                          ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL )
                          OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND rec."MODEL_CHUNG_TU_CONG_NO"="DebtRefModel"))
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
                     ,"MA_KHACH_HANG"
                    ,"TEN_KHACH_HANG"

                    , "ID_CHUNG_TU"
                    , "MODEL_CHUNG_TU"
                    , "LOAI_CHUNG_TU"
                    , "NGAY_HACH_TOAN"
                    , "NGAY_CHUNG_TU"
                    , "SO_CHUNG_TU"
                    , "MA_TK"
                    , "GHI_NO_NGUYEN_TE"
                    , "GHI_NO"
                    , "GHI_CO_NGUYEN_TE"
                    , "GHI_CO"
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
                         ,"MA_KHACH_HANG"
                        ,"TEN_KHACH_HANG"
                        , "ID_CHUNG_TU"
                        , "MODEL_CHUNG_TU"
                        , "LOAI_CHUNG_TU"
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , "SO_CHUNG_TU"
                        , "MA_TK"
                        , "GHI_NO_NGUYEN_TE"
                        , "GHI_NO"
                        , "CrossAmountOC"
                        , "CrossAmount"
                        , "OrderType"
                        , "LedgerID"
                        , "currency_id"
                        , "DebtRefID"
                        , TRUE                        AS "IsCrossRow"
                        , "CHI_TIET_ID"
                        , "CHI_TIET_MODEL"

                    FROM TMP_KET_QUA
                    WHERE "ID_CHUNG_TU" = rec."PayRefID"
                         and "MODEL_CHUNG_TU" = rec."PayRef_model_ID"
                          AND "DOI_TUONG_ID" = rec."PayAccountObject"
                          AND "MA_TK" = rec."PayAccountNumber"
                          AND "currency_id" = rec."PayCurrency"
                          AND (
                              ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO" IS NULL)
                              OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND
                                  rec."MODEL_CHUNG_TU_CONG_NO"="DebtRefModel"))
                          AND "IsCrossRow" = FALSE
                          AND ("GHI_CO_NGUYEN_TE" <> 0
                                    OR "GHI_CO" <> 0 )
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
                           ("DebtRefID" IS NULL AND rec."ID_CHUNG_TU_CONG_NO"  IS NULL)
                              OR ("DebtRefID" = rec."ID_CHUNG_TU_CONG_NO" AND  rec."MODEL_CHUNG_TU_CONG_NO"="DebtRefModel"))
                      AND "IsCrossRow" = FALSE
            ;
 END LOOP
    ;




    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS
            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY "MA_NHAN_VIEN" ) AS "RowNum"
                , R."NHAN_VIEN_ID"
                , E."MA_NHAN_VIEN"
                , E."HO_VA_TEN"
                , R."MA_TK"
                ,R."DOI_TUONG_ID"
                ,R."MA_KHACH_HANG"
                ,R."TEN_KHACH_HANG" AS "TEN_KHACH_HANG"
                , AC."TINH_CHAT"

                , (CASE WHEN ("TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                THEN ("GHI_NO" - "GHI_CO")
                                                                              ELSE 0 END) >= 0))
                THEN SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_NO" - "GHI_CO")
                         ELSE 0 END)
                   ELSE 0
                   END)                         AS "GHI_NO_DAU_KY"
                , (CASE WHEN ("TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                THEN ("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                                                                              ELSE 0 END) >= 0))
                THEN SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                         ELSE 0 END)
                   ELSE 0
                   END)                         AS "GHI_NO_NGUYEN_TE_DAU_KY"
                , (CASE WHEN ("TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                THEN ("GHI_CO" - "GHI_NO")
                                                                              ELSE 0 END) >= 0))
                THEN SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_CO" - "GHI_NO")
                         ELSE 0 END)
                   ELSE 0
                   END)                         AS "GHI_CO_DAU_KY"
                , (CASE WHEN ("TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND SUM(CASE WHEN R."OrderType" = 0
                THEN ("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                                                                              ELSE 0 END) >= 0))
                THEN SUM(CASE WHEN R."OrderType" = 0
                    THEN ("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                         ELSE 0 END)
                   ELSE 0
                   END)                         AS "GHI_CO_NGUYEN_TE_DAU_KY"

                , SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_NO", 0)
                      ELSE 0 END)               AS "GHI_NO"
                , SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_NO_NGUYEN_TE", 0)
                      ELSE 0 END)               AS "GHI_NO_NGUYEN_TE"
                , SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_CO", 0)
                      ELSE 0 END)               AS "GHI_CO"
                , SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_CO_NGUYEN_TE", 0)
                      ELSE 0 END)               AS "GHI_CO_NGUYEN_TE"

                , (CASE WHEN "TINH_CHAT" = '0' OR ("TINH_CHAT" = '2' AND SUM("GHI_NO" - "GHI_CO") >= 0)
                THEN SUM("GHI_NO" - "GHI_CO")
                   ELSE 0 END)                  AS "DU_NO_CUOI_KY"
                , (CASE WHEN "TINH_CHAT" = '0' OR
                             ("TINH_CHAT" = '2' AND SUM("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE") >= 0)
                THEN SUM("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                   ELSE 0 END)                  AS "DU_NO_NGUYEN_TE_CUOI_KY"
                , (CASE WHEN "TINH_CHAT" = '1' OR ("TINH_CHAT" = '2' AND SUM("GHI_CO" - "GHI_NO") >= 0)
                THEN SUM("GHI_CO" - "GHI_NO")
                   ELSE 0 END)                  AS "DU_CO_CUOI_KY"
                , (CASE WHEN "TINH_CHAT" = '1' OR
                             ("TINH_CHAT" = '2' AND SUM("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE") >= 0)
                THEN SUM("GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE")
                   ELSE 0 END)                  AS "DU_CO_NGUYEN_TE_CUOI_KY"

            FROM TMP_KET_QUA R
                INNER JOIN DS_NHAN_VIEN E ON E."NHAN_VIEN_ID" = R."NHAN_VIEN_ID"
                INNER JOIN danh_muc_he_thong_tai_khoan AC ON AC."SO_TAI_KHOAN" = R."MA_TK"
            GROUP BY
                R."NHAN_VIEN_ID"
                , E."MA_NHAN_VIEN"
                , E."HO_VA_TEN"
                , R."MA_TK"
                ,R."DOI_TUONG_ID"
                ,R."MA_KHACH_HANG"
                ,R."TEN_KHACH_HANG"
                , AC."TINH_CHAT"

            HAVING SUM(CASE WHEN R."OrderType" = 0
                THEN ("GHI_NO" - "GHI_CO")
                       ELSE 0 END) <> 0
                   OR SUM(CASE WHEN R."OrderType" = 0
                THEN ("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE")
                          ELSE 0 END) <> 0
                   OR SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_NO", 0)
                          ELSE 0 END) <> 0
                   OR SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_NO_NGUYEN_TE", 0)
                          ELSE 0 END) <> 0
                   OR SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_CO", 0)
                          ELSE 0 END) <> 0
                   OR SUM(CASE WHEN R."OrderType" = 1
                THEN COALESCE(R."GHI_CO_NGUYEN_TE", 0)
                          ELSE 0 END) <> 0
            ORDER BY
                E."MA_NHAN_VIEN",
                R."MA_KHACH_HANG"

    ;



END $$
;

SELECT 
    "MA_NHAN_VIEN" AS "MA_NHAN_VIEN",
    "HO_VA_TEN" AS "TEN_NHAN_VIEN",
    "MA_KHACH_HANG" AS "MA_KHACH_HANG",
    "TEN_KHACH_HANG" AS "TEN_KHACH_HANG",
    "MA_TK" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO" AS "NO_SO_PHAT_SINH",
    "GHI_CO" AS "CO_SO_PHAT_SINH",
    "DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
FROM TMP_KET_QUA_CUOI_CUNG
OFFSET %(offset)s
LIMIT %(limit)s;


        """
        return self.execute(query,params_sql)
        
    def _lay_bao_cao_thong_ke_theo_cong_trinh(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_PHAI_THU_KHACH_HANG: công trình
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    --tham số từ

    v_den_ngay                            DATE :=  %(DEN_NGAY)s;

    --tham số đến

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

     --tham số bao gồm số liệu chi nhánh phụ thuộc

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    --tham số chi nhánh


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

     --tham số tài khoản

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    --tham số loại tiền




    rec                                   RECORD;


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

                  AO.id AS "KHACH_HANG_ID"
                , CASE AO."LOAI_KHACH_HANG"
                  WHEN '0'
                      THEN ao."DIEN_THOAI"
                  ELSE AO."DT_DI_DONG"
                  END   AS "DIEN_THOAI"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI"
                , AO."LIST_MA_NHOM_KH_NCC"
            FROM res_partner AS AO --tham số khách hàng
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
                , PWC."name" AS "TEN_LOAI_CONG_TRINH"
                , PW."isparent"

                , 0 AS "IsParentWithChild"
            FROM
                danh_muc_cong_trinh PW
                LEFT JOIN danh_muc_loai_cong_trinh PWC ON PW."LOAI_CONG_TRINH" = PWC.id
            WHERE (PW."id" = any(%(CONG_TRINHIDS)s)) ----tham số công trình
    ;

    UPDATE  DS_CONG_TRINH_DC_CHON
        SET     "IsParentWithChild" = 1
        FROM    DS_CONG_TRINH_DC_CHON T
                INNER JOIN DS_CONG_TRINH_DC_CHON T1 ON T1."MA_PHAN_CAP" LIKE T."MA_PHAN_CAP" || '%%'
                                                         AND T."MA_PHAN_CAP" <> T1."MA_PHAN_CAP"
        WHERE   T."isparent" = '1';


     DROP TABLE IF EXISTS DS_CONG_TRINH_GRADE
    ;
     CREATE TEMP TABLE DS_CONG_TRINH_GRADE
        AS
             SELECT  PWS."CONG_TRINH_ID"  ,
                        PWS."MA_PHAN_CAP" ,
                        COUNT(PWSC."MA_PHAN_CAP") Grade
                FROM    DS_CONG_TRINH_DC_CHON PWS
                        LEFT JOIN DS_CONG_TRINH_DC_CHON PWSC ON PWS."MA_PHAN_CAP" LIKE PWSC."MA_PHAN_CAP" || '%%'
                                                              AND PWS."MA_PHAN_CAP" <> PWSC."MA_PHAN_CAP"
                GROUP BY PWS."CONG_TRINH_ID" ,
                        PWS."MA_PHAN_CAP" ;

     DROP TABLE IF EXISTS DS_CONG_TRINH_PARENT
    ;
     CREATE TEMP TABLE DS_CONG_TRINH_PARENT
        AS
             SELECT
                 DISTINCT
                        PWS."CONG_TRINH_ID"
                FROM    DS_CONG_TRINH_DC_CHON PWS
                        LEFT JOIN DS_CONG_TRINH_DC_CHON PWSC ON PWS."MA_PHAN_CAP" LIKE PWSC."MA_PHAN_CAP"
                                                              || '%%'
                                                              AND PWS."MA_PHAN_CAP" <> PWSC."MA_PHAN_CAP"
                WHERE   PWSC."MA_PHAN_CAP" IS NULL;

     DROP TABLE IF EXISTS DS_CONG_TRINH_PARENT_CHILD_DC_CHON
    ;
     CREATE TEMP TABLE DS_CONG_TRINH_PARENT_CHILD_DC_CHON
        AS
             SELECT DISTINCT
                        PWSC."CONG_TRINH_ID"
                FROM    DS_CONG_TRINH_DC_CHON PWS
                        LEFT JOIN DS_CONG_TRINH_DC_CHON PWSC ON PWS."MA_PHAN_CAP" LIKE PWSC."MA_PHAN_CAP" || '%%'
                                                              AND PWS."MA_PHAN_CAP" <> PWSC."MA_PHAN_CAP"
                WHERE   PWSC."MA_PHAN_CAP" IS NOT NULL;

     DROP TABLE IF EXISTS DS_CONG_TRINH_CHILD
    ;
     CREATE TEMP TABLE DS_CONG_TRINH_CHILD
        AS
             SELECT    DISTINCT
                        PW."id" AS "CONG_TRINH_ID",
                        PW."MA_PHAN_CAP"
                FROM    danh_muc_cong_trinh PW
                        INNER JOIN DS_CONG_TRINH_DC_CHON PWS ON PW."MA_PHAN_CAP" LIKE PWS."MA_PHAN_CAP" || '%%'
                                                              AND PW."isparent" = '0';



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
                        and  "CHI_TIET_THEO_DOI_TUONG" = '1'

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
                      AND "DOI_TUONG_SELECTION" = '1'
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
            PWS."CONG_TRINH_ID" ,
				PWS."MA_CONG_TRINH" , -- Mã công trình
				PWS."TEN_CONG_TRINH" , -- Tên công trình

				PWS."MA_PHAN_CAP" ,
				AOL."DOI_TUONG_ID" ,
				AOL."MA_DOI_TUONG" ,   -- Mã NCC

				LAOI."HO_VA_TEN" ,	-- Tên NCC lấy trên danh mục

				TBAN."SO_TAI_KHOAN" , -- TK công nợ
				TBAN."TINH_CHAT" , -- Tính chất tài khoản
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
					 THEN AOL."GHI_NO_NGUYEN_TE"
					 ELSE 0
				END AS "GHI_NO_NGUYEN_TE_DAU_KY" ,	-- Dư nợ Đầu kỳ
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
					 THEN AOL."GHI_NO"
					 ELSE 0
				END AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
					 THEN AOL."GHI_CO_NGUYEN_TE"
					 ELSE 0
				END AS "GHI_CO_NGUYEN_TE_DAU_KY" , -- Dư có đầu kỳ
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
					 THEN AOL."GHI_CO"
					 ELSE 0
				END AS "GHI_CO_DAU_KY" , -- Dư có đầu kỳ quy đổi
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay THEN 0
					 ELSE AOL."GHI_NO_NGUYEN_TE"
				END AS "GHI_NO_NGUYEN_TE" , -- Phát sinh nợ
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay THEN 0
					 ELSE AOL."GHI_NO"
				END AS "GHI_NO" , -- Phát sinh nợ quy đổi
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay THEN 0
					 ELSE AOL."GHI_CO_NGUYEN_TE"
				END AS "GHI_CO_NGUYEN_TE" , -- Phát sinh có
				CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay THEN 0
					 ELSE AOL."GHI_CO"
				END AS "GHI_CO"


		FROM      so_cong_no_chi_tiet AS AOL
				INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
				INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
				INNER JOIN DS_CONG_TRINH_CHILD LCPW ON AOL."CONG_TRINH_ID" = LCPW."CONG_TRINH_ID"
				INNER JOIN DS_CONG_TRINH_DC_CHON PWS ON --Là cha và không có con thì lấy tất cả các con
						( PWS."IsParentWithChild" = 0
						  AND LCPW."MA_PHAN_CAP" LIKE PWS."MA_PHAN_CAP"
						  || '%%'

						  OR ( PWS."IsParentWithChild" = 1
							   AND PWS."CONG_TRINH_ID" = LCPW."CONG_TRINH_ID"
							 )
						)
				INNER JOIN DS_KHACH_HANG AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
				INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
				LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id" -- Danh mục ĐVT
		WHERE     AOL."NGAY_HACH_TOAN" <= v_den_ngay

				AND ( v_loai_tien_id IS NULL
					  OR AOL."currency_id" = v_loai_tien_id
					);


--select *from DS_CONG_TRINH_CHILD
-------------------------------------------
 DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS

        SELECT  ROW_NUMBER() OVER
            ( ORDER BY "MA_DOI_TUONG",GEI.Grade, SEI."MA_CONG_TRINH" ) AS RowNum ,
                SEI."CONG_TRINH_ID" ,
                repeat(' ',cast(GEI.Grade * 4 AS INT)) || SEI."MA_CONG_TRINH" AS "MA_CONG_TRINH" ,
                repeat(' ',cast(GEI.Grade * 4 AS INT)) || SEI."TEN_CONG_TRINH" AS "TEN_CONG_TRINH",

                GEI.Grade ,

                "DOI_TUONG_ID" ,
                "MA_DOI_TUONG" ,   -- Mã NCC
                "HO_VA_TEN" ,	-- Tên NCC

                "SO_TAI_KHOAN" , -- Số tài khoản
                "TINH_CHAT" , -- Tính chất tài khoản
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
                                          - "GHI_NO_DAU_KY" + "GHI_CO"
                                          - "GHI_NO") > 0 THEN 0
                                 ELSE SUM("GHI_NO_DAU_KY"
                                          - "GHI_CO_DAU_KY" + "GHI_NO"
                                          - "GHI_CO")
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

        FROM   TMP_KET_QUA  AS RSNS
                INNER JOIN DS_CONG_TRINH_DC_CHON SEI ON RSNS."MA_PHAN_CAP" LIKE SEI."MA_PHAN_CAP" ||'%%'
                LEFT JOIN DS_CONG_TRINH_PARENT_CHILD_DC_CHON PSEI ON PSEI."CONG_TRINH_ID" = SEI."CONG_TRINH_ID"
                INNER JOIN DS_CONG_TRINH_GRADE GEI ON GEI."CONG_TRINH_ID" = SEI."CONG_TRINH_ID"
        GROUP BY SEI."CONG_TRINH_ID" ,
                PSEI."CONG_TRINH_ID" ,
                SEI."MA_CONG_TRINH" , -- Mã công trình
                SEI."TEN_CONG_TRINH" , -- Tên công trình

                GEI.Grade ,
                RSNS."DOI_TUONG_ID" ,
                RSNS."MA_DOI_TUONG" ,   -- Mã NCC
                RSNS."HO_VA_TEN" ,	-- Tên NCC

                RSNS."SO_TAI_KHOAN" , -- Số tài khoản
                RSNS."TINH_CHAT"

        HAVING  SUM("GHI_NO_NGUYEN_TE") <> 0
                OR SUM("GHI_NO") <> 0
                OR SUM("GHI_CO_NGUYEN_TE") <> 0
                OR SUM("GHI_CO") <> 0
                OR SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0
                OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0

    ;


END $$
;

SELECT 

    "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
    "MA_DOI_TUONG" AS "MA_KHACH_HANG",
    "HO_VA_TEN" AS "TEN_KHACH_HANG",
    "SO_TAI_KHOAN" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO" AS "NO_SO_PHAT_SINH",
    "GHI_CO" AS "CO_SO_PHAT_SINH",
    "DU_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY"

FROM  TMP_KET_QUA_CUOI_CUNG
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

   

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

    


   


    rec                                   RECORD;


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

                AO.id AS "KHACH_HANG_ID"
                , AO."MA_KHACH_HANG"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI"
                , AO."MA_SO_THUE"
                , AO."LIST_MA_NHOM_KH_NCC"
            FROM res_partner AS AO 
            WHERE (id = any (%(KHACH_HANG_IDS)s))
    ;


    DROP TABLE IF EXISTS DS_HOP_DONG
    ;

    CREATE TEMP TABLE DS_HOP_DONG
        AS
            SELECT
                C.id AS "HOP_DONG_BAN_ID"
                , C."SO_HOP_DONG"
                , C."NGAY_KY"
                , C."TRICH_YEU"
            FROM sale_ex_hop_dong_ban C
            WHERE (id = any (%(HOP_DONGIDS)s))
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

                ORDER BY A."SO_TAI_KHOAN",
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
                    ORDER BY "SO_HOP_DONG", "MA_KHACH_HANG" ) AS RowNum
                , "HOP_DONG_BAN_ID"
                , "SO_HOP_DONG"
                , -- Mã hợp đồng bán
                "NGAY_KY"
                , -- Ngày ký hợp đồng bán
                "TRICH_YEU"
                , -- Trích yếu hợp đồng bán
                "DOI_TUONG_ID"
                , "MA_KHACH_HANG"
                , -- Mã NCC
                "HO_VA_TEN"


                , "SO_TAI_KHOAN"
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
                                    - "GHI_NO_DAU_KY" + "GHI_CO"
                                    - "GHI_NO") > 0
                     THEN 0
                      ELSE SUM("GHI_NO_DAU_KY"
                               - "GHI_CO_DAU_KY" + "GHI_NO"
                               - "GHI_CO")
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
                      LCID."HOP_DONG_BAN_ID"
                      , LCID."SO_HOP_DONG"
                      , LCID."NGAY_KY"
                      , LCID."TRICH_YEU"
                      , -- Trích yếu hợp đồng bán
                      AOL."DOI_TUONG_ID"
                      , LAOI."MA_KHACH_HANG"

                      ,LAOI."HO_VA_TEN"

                      ,TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO_NGUYEN_TE"
                        ELSE 0
                        END AS           "GHI_NO_NGUYEN_TE_DAU_KY"
                      , -- Dư nợ Đầu kỳ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_NO"
                        ELSE 0
                        END AS           "GHI_NO_DAU_KY"
                      , -- Dư nợ Đầu kỳ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO_NGUYEN_TE"
                        ELSE 0
                        END AS           "GHI_CO_NGUYEN_TE_DAU_KY"
                      , -- Dư có đầu kỳ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN AOL."GHI_CO"
                        ELSE 0
                        END AS           "GHI_CO_DAU_KY"
                      , -- Dư có đầu kỳ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO_NGUYEN_TE"
                        END AS           "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_NO"
                        END AS           "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO_NGUYEN_TE"
                        END AS           "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                        CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                            THEN 0
                        ELSE AOL."GHI_CO"
                        END AS           "GHI_CO"

                  FROM so_cong_no_chi_tiet AS AOL
                      INNER JOIN sale_ex_hop_dong_ban C ON C.id = AOL."HOP_DONG_BAN_ID"
                      INNER JOIN DS_HOP_DONG LCID ON (C.id = LCID."HOP_DONG_BAN_ID"
                                                      OR C."THUOC_DU_AN_ID" = LCID."HOP_DONG_BAN_ID"
                          )
                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN DS_KHACH_HANG AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN."id"
                      -- Danh mục ĐVT
                      LEFT JOIN danh_muc_to_chuc OU ON OU."id" = C."CHI_NHANH_ID"
                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                 ) AS RSNS

            GROUP BY
                RSNS."HOP_DONG_BAN_ID",
                RSNS."SO_HOP_DONG", -- Mã hợp đồng bán
                RSNS."NGAY_KY", -- Ngày ký hợp đồng bán
                RSNS."TRICH_YEU", -- Trích yếu hợp đồng bán
                RSNS."DOI_TUONG_ID",
                RSNS."MA_KHACH_HANG", -- Mã NCC
                RSNS."HO_VA_TEN", -- Tên NCC


                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT" -- Tính chất tài khoản

            HAVING
                SUM("GHI_NO_NGUYEN_TE") <> 0 OR
                SUM("GHI_NO") <> 0 OR
                SUM("GHI_CO_NGUYEN_TE") <> 0 OR
                SUM("GHI_CO") <> 0 OR
                SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0 OR
                SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0

    ;


END $$
;

SELECT 
    "SO_HOP_DONG" AS "HOP_DONG_HOAC_DU_AN",
    "HO_VA_TEN" AS "TEN_KHACH_HANG",
    "SO_TAI_KHOAN" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_NGUYEN_TE_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_NGUYEN_TE_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO_NGUYEN_TE" AS "NO_SO_PHAT_SINH",
    "GHI_CO_NGUYEN_TE" AS "CO_SO_PHAT_SINH",
    "DU_NO_NGUYEN_TE_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_NGUYEN_TE_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_don_dat_hang(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

   

    v_den_ngay                            DATE := %(DEN_NGAY)s;

   

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

   

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

   




    rec                                   RECORD;


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

                AO.id AS "KHACH_HANG_ID"
                , AO."MA_KHACH_HANG"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI"
                , AO."MA_SO_THUE"
                , AO."LIST_MA_NHOM_KH_NCC"
            FROM res_partner AS AO 
            WHERE (id = any (%(KHACH_HANG_IDS)s))
    ;


    DROP TABLE IF EXISTS DS_DON_DAT_HANG
    ;

    CREATE TEMP TABLE DS_DON_DAT_HANG
        AS
            SELECT
                C."id" AS "DON_DAT_HANG_ID"
                ,C."SO_DON_HANG"
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
                   END) AS "TINH_TRANG"


            FROM account_ex_don_dat_hang C
            WHERE (id = any (%(DON_DAT_HANGIDS)s))
    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    IF so_tai_khoan IS NOT NULL
    THEN
        CREATE TEMP TABLE TMP_TAI_KHOAN
            AS
                SELECT
                      A."SO_TAI_KHOAN"                   AS "SO_TAI_KHOAN"
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
                      A."SO_TAI_KHOAN"                   AS "SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                    , A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '1'
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
                    ORDER BY "NGAY_DON_HANG", "SO_DON_HANG", "MA_KHACH_HANG" ,"SO_TAI_KHOAN" ) AS RowNum
                , "DON_DAT_HANG_ID"
                , "SO_DON_HANG"
                , -- Mã hợp đồng bán
                "NGAY_DON_HANG"
                , -- Ngày ký hợp đồng bán
                "TINH_TRANG"
                , -- Trích yếu hợp đồng bán
                "DOI_TUONG_ID"
                , "MA_KHACH_HANG"
                , -- Mã NCC
                "HO_VA_TEN"


                , "SO_TAI_KHOAN"
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
                 ELSE CASE WHEN SUM("GHI_NO_DAU_KY" -
                                    "GHI_CO_DAU_KY" + "GHI_NO"
                                    - "GHI_CO") > 0
                     THEN 0
                      ELSE SUM("GHI_NO_DAU_KY"
                               - "GHI_CO_DAU_KY" + "GHI_NO"
                               - "GHI_CO")
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
                      SA."DON_DAT_HANG_ID"
                      , SA."SO_DON_HANG"
                      , SA."NGAY_DON_HANG"
                      , SA."TINH_TRANG"
                      , -- Trích yếu hợp đồng bán
                      AOL."DOI_TUONG_ID"
                      , LAOI."MA_KHACH_HANG"

                      , LAOI."HO_VA_TEN"

                      , TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_NO_NGUYEN_TE"
                      ELSE 0
                      END AS "GHI_NO_NGUYEN_TE_DAU_KY"
                      , -- Dư nợ Đầu kỳ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_NO"
                      ELSE 0
                      END AS "GHI_NO_DAU_KY"
                      , -- Dư nợ Đầu kỳ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_CO_NGUYEN_TE"
                      ELSE 0
                      END AS "GHI_CO_NGUYEN_TE_DAU_KY"
                      , -- Dư có đầu kỳ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_CO"
                      ELSE 0
                      END AS "GHI_CO_DAU_KY"
                      , -- Dư có đầu kỳ quy đổi
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

                  FROM so_cong_no_chi_tiet AS AOL

                      INNER JOIN DS_DON_DAT_HANG SA ON (AOL."DON_DAT_HANG_ID" = SA."DON_DAT_HANG_ID"

                          )
                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                      INNER JOIN DS_KHACH_HANG AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_to_chuc AS OU ON OU."id" = AOL."CHI_NHANH_ID"
                      -- Danh mục ĐVT

                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                 ) AS RSNS

            GROUP BY
                RSNS."DON_DAT_HANG_ID",
                RSNS."SO_DON_HANG", -- Mã hợp đồng bán
                RSNS."NGAY_DON_HANG", -- Ngày ký hợp đồng bán
                RSNS."TINH_TRANG", -- Trích yếu hợp đồng bán
                RSNS."DOI_TUONG_ID",
                RSNS."MA_KHACH_HANG", -- Mã NCC
                RSNS."HO_VA_TEN", -- Tên NCC


                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT" -- Tính chất tài khoản

            HAVING
                SUM("GHI_NO_NGUYEN_TE") <> 0 OR
                SUM("GHI_NO") <> 0 OR
                SUM("GHI_CO_NGUYEN_TE") <> 0 OR
                SUM("GHI_CO") <> 0 OR
                SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY") <> 0 OR
                SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0

    ;


END $$
;

SELECT 
    "SO_DON_HANG" AS "SO_DON_HANG",
    "NGAY_DON_HANG" AS "NGAY_DON_HANG",
    "HO_VA_TEN" AS "TEN_KHACH_HANG",
    "SO_TAI_KHOAN" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_NGUYEN_TE_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_NGUYEN_TE_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO_NGUYEN_TE" AS "NO_SO_PHAT_SINH",
    "GHI_CO_NGUYEN_TE" AS "CO_SO_PHAT_SINH",
    "DU_NO_NGUYEN_TE_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_NGUYEN_TE_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_don_vi_kinh_doanh(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

   

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;

  



    rec                                   RECORD;


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
                    , "MA_KHACH_HANG"
                    , "HO_VA_TEN"

                    , "LIST_MA_NHOM_KH_NCC"

                    , CASE "LOAI_KHACH_HANG"
                      WHEN '0'
                          THEN "DIEN_THOAI"
                      ELSE "DT_DI_DONG" END AS "DIEN_THOAI"
                FROM res_partner
                WHERE "LA_KHACH_HANG" = '1'
        ;
    ELSE
        CREATE TEMP TABLE DS_KHACH_HANG
            AS

                SELECT
                    "id" AS "KHACH_HANG_ID"
                    , "MA_KHACH_HANG"
                    , "HO_VA_TEN"

                    , "LIST_MA_NHOM_KH_NCC"


                FROM res_partner
                WHERE (id = any (%(KHACH_HANG_IDS)s))
        ;

       
    END IF
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
                          A."SO_TAI_KHOAN"         AS "SO_TAI_KHOAN"
                        , A."TEN_TAI_KHOAN"
                        , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                        , A."TINH_CHAT"
                    FROM danh_muc_he_thong_tai_khoan AS A
                    WHERE "SO_TAI_KHOAN" = so_tai_khoan
                            AND "CHI_TIET_THEO_DOI_TUONG" = '1'
                    ORDER BY A."SO_TAI_KHOAN",
                        A."TEN_TAI_KHOAN"
            ;

        ELSE
    CREATE TEMP TABLE TMP_TAI_KHOAN
        AS
            SELECT
                  A."SO_TAI_KHOAN"         AS "SO_TAI_KHOAN"
                , A."TEN_TAI_KHOAN"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND "DOI_TUONG_SELECTION" = '1'
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
                      ORDER BY P."MA_DON_VI", "MA_DOI_TUONG" ) AS RowNum
                , P."DON_VI_ID"
                , P."MA_DON_VI"                                 AS "MA_DON_VI"
                , P."TEN_DON_VI"                                AS "TEN_DON_VI"

                , -- Trích yếu hợp đồng bán
                "DOI_TUONG_ID"
                , "MA_DOI_TUONG"
                , -- Mã NCC
                "TEN_DOI_TUONG"


                , "SO_TAI_KHOAN"
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
                   ELSE CASE WHEN SUM("GHI_CO_DAU_KY" - "GHI_NO_DAU_KY"
                                      + "GHI_CO" - "GHI_NO") > 0
                       THEN 0
                        ELSE SUM("GHI_NO_DAU_KY"
                                 - "GHI_CO_DAU_KY" + "GHI_NO"
                                 - "GHI_CO")
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
                      OU."DON_VI_ID"
                      , OU."MA_PHAN_CAP"

                     , AOL."DOI_TUONG_ID"
                      , AOL."MA_DOI_TUONG"
                      , -- Mã khách hàng
                      AOL."TEN_DOI_TUONG"


                      , TBAN."SO_TAI_KHOAN"
                      , -- TK công nợ
                      TBAN."TINH_CHAT"
                      , -- Tính chất tài khoản
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_NO_NGUYEN_TE"
                      ELSE 0
                      END AS              "GHI_NO_NGUYEN_TE_DAU_KY"
                      , -- Dư nợ Đầu kỳ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_NO"
                      ELSE 0
                      END AS              "GHI_NO_DAU_KY"
                      , -- Dư nợ Đầu kỳ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_CO_NGUYEN_TE"
                      ELSE 0
                      END AS              "GHI_CO_NGUYEN_TE_DAU_KY"
                      , -- Dư có đầu kỳ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN AOL."GHI_CO"
                      ELSE 0
                      END AS              "GHI_CO_DAU_KY"
                      , -- Dư có đầu kỳ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN 0
                      ELSE AOL."GHI_NO_NGUYEN_TE"
                      END AS              "GHI_NO_NGUYEN_TE"
                      , -- Phát sinh nợ
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN 0
                      ELSE AOL."GHI_NO"
                      END AS              "GHI_NO"
                      , -- Phát sinh nợ quy đổi
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN 0
                      ELSE AOL."GHI_CO_NGUYEN_TE"
                      END AS              "GHI_CO_NGUYEN_TE"
                      , -- Phát sinh có
                      CASE WHEN AOL."NGAY_HACH_TOAN" < v_tu_ngay
                          THEN 0
                      ELSE AOL."GHI_CO"
                      END AS              "GHI_CO"

                  FROM so_cong_no_chi_tiet AS AOL

                      INNER JOIN TMP_TAI_KHOAN TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
                      INNER JOIN danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"

                      INNER JOIN DS_DON_VI OU ON AOL."DON_VI_ID" = OU."DON_VI_ID"

                      INNER JOIN DS_KHACH_HANG AS LAOI ON AOL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
                      INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
                      LEFT JOIN danh_muc_to_chuc AS UN ON UN."id" = AOL."DVT_ID"
                  -- Danh mục ĐVT

                  WHERE AOL."NGAY_HACH_TOAN" <= v_den_ngay

                        AND (v_loai_tien_id IS NULL
                             OR AOL."currency_id" = v_loai_tien_id
                        )
                        AND AN."CHI_TIET_THEO_DOI_TUONG" = '1'
                        AND AN."DOI_TUONG_SELECTION" = '1'
                 ) AS RSNS
                INNER JOIN TMP_DON_VI P ON
                                            ((P."ISPARENT" = '0' OR P."IsParentWithChild" = 1) AND
                                             RSNS."DON_VI_ID" = P."DON_VI_ID")
                                            OR (P."ISPARENT" = '1' AND P."IsParentWithChild" = 0 AND
                                                RSNS."MA_PHAN_CAP" LIKE P."MA_PHAN_CAP" || '%%')


            GROUP BY

	            P."DON_VI_ID" ,
                P."MA_DON_VI",
                P."TEN_DON_VI"  ,
                RSNS."DOI_TUONG_ID",
                RSNS."MA_DOI_TUONG",   -- Mã khách hàng
                RSNS."TEN_DOI_TUONG",	-- Tên khách hàng

                RSNS."SO_TAI_KHOAN", -- Số tài khoản
                RSNS."TINH_CHAT" -- Tính chất tài khoản

        HAVING
				SUM("GHI_NO_NGUYEN_TE")<>0 OR
                SUM("GHI_NO")<>0 OR
                SUM("GHI_CO_NGUYEN_TE") <>0 OR
                SUM("GHI_CO") <>0 OR
                SUM("GHI_NO_NGUYEN_TE_DAU_KY" - "GHI_CO_NGUYEN_TE_DAU_KY")<>0 OR
                SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY")<>0
        ORDER BY P."MA_DON_VI",
                RSNS."MA_DOI_TUONG" -- Mã khách hàng

    ;


END $$
;

SELECT
    "TEN_DOI_TUONG" AS "Ten_khach_hang",
    "TEN_DON_VI" AS "TEN_DON_VI",
    "SO_TAI_KHOAN" AS "TAI_KHOAN_CONG_NO",
    "GHI_NO_NGUYEN_TE_DAU_KY" AS "NO_SO_DU_DAU_KY",
    "GHI_CO_NGUYEN_TE_DAU_KY" AS "CO_SO_DU_DAU_KY",
    "GHI_NO_NGUYEN_TE" AS "NO_SO_PHAT_SINH",
    "GHI_CO_NGUYEN_TE" AS "CO_SO_PHAT_SINH",
    "DU_NO_NGUYEN_TE_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
    "DU_CO_NGUYEN_TE_CUOI_KY" AS "CO_SO_DU_CUOI_KY"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s
;
    """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_chi_tiet_theo_cac_khoan_giam_tru(self, params_sql):      
        record = []
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    

    v_den_ngay                            DATE := %(DEN_NGAY)s;

   

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

   

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    

    v_loai_tien_id                        INTEGER := %(currency_id)s;



    rec                                   RECORD;
    LOAI_TIEN_CHINH      VARCHAR(100);
    CHE_DO_KE_TOAN      VARCHAR(100);
    




BEGIN


    SELECT value INTO LOAI_TIEN_CHINH FROM ir_config_parameter WHERE key = 'he_thong.LOAI_TIEN_CHINH' FETCH FIRST 1 ROW ONLY ;
    SELECT value INTO CHE_DO_KE_TOAN FROM ir_config_parameter WHERE key = 'he_thong.CHE_DO_KE_TOAN' FETCH FIRST 1 ROW ONLY ;

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
                Ao.id AS "KHACH_HANG_ID"
                , AO."MA_KHACH_HANG"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI"
                , AO."MA_SO_THUE"

    ,CASE WHEN AO."LOAI_KHACH_HANG" = '0' THEN AO."DIEN_THOAI"
    WHEN AO."LOAI_KHACH_HANG" = '1' THEN AO."DT_DI_DONG"
            END AS "DT_DI_DONG",
            AO."LIST_MA_NHOM_KH_NCC",
            AO."LIST_TEN_NHOM_KH_NCC"


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
                    so_tai_khoan
                  ,A."SO_TAI_KHOAN"         AS "SO_TAI_KHOAN"


                , A."TINH_CHAT"
                , A."CHI_TIET_THEO_DOI_TUONG"

            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE (("SO_TAI_KHOAN" like so_tai_khoan || '%%')
                   AND "CHI_TIET_THEO_DOI_TUONG" = '1'
                   AND "DOI_TUONG_SELECTION" = '1'

                    )
            ORDER BY
                A."SO_TAI_KHOAN",
                A."TEN_TAI_KHOAN"
    ;

ELSE
    CREATE TEMP TABLE TMP_TAI_KHOAN
        AS
            SELECT
                  A."SO_TAI_KHOAN"         AS "SO_TAI_KHOAN"


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

END IF
;


DROP TABLE IF EXISTS TMP_KET_QUA
;

CREATE TEMP TABLE TMP_KET_QUA
    AS
        SELECT
			A."KHACH_HANG_ID" ,
			A."MA_KHACH_HANG" ,
			A."HO_VA_TEN" ,

			A."SO_TAI_KHOAN",
			SUM("SO_DU_DAU_KY_NGUYEN_TE") AS "SO_DU_DAU_KY_NGUYEN_TE",
			SUM("SO_DU_DAU_KY") AS "SO_DU_DAU_KY",
			SUM("SO_TIEN_PHAI_THU") AS "SO_TIEN_PHAI_THU",
			SUM("SO_TIEN_PHAI_THU_QD") AS "SO_TIEN_PHAI_THU_QD",
			SUM("SO_TIEN_CHIET_KHAU") AS "SO_TIEN_CHIET_KHAU",
			SUM("SO_TIEN_CHIET_KHAU_QD") AS "SO_TIEN_CHIET_KHAU_QD",
			SUM("SO_TIEN_TRA_LAI") AS "SO_TIEN_TRA_LAI",
			SUM("SO_TIEN_TRA_LAI_QD") AS "SO_TIEN_TRA_LAI_QD",
			SUM("CK_GIAM_TRU_KHAC") AS "CK_GIAM_TRU_KHAC",
			SUM("CK_GIAM_TRU_KHAC_QD") AS "CK_GIAM_TRU_KHAC_QD",
			SUM("SO_DA_THU") AS "SO_DA_THU",
			SUM("SO_DA_THU_QD") AS "SO_DA_THU_QD",
			cast(0 AS FLOAT) AS "SO_DU_CUOI_KY",
			cast(0 AS FLOAT) AS "SO_DU_CUOI_KY_QD"


        FROM
          (
				/* Dư đầu kỳ - tách việc iner join có Or thành UNIOn ALL cho chạy nhanh*/
				SELECT
						LAOI."KHACH_HANG_ID" ,
						LAOI."MA_KHACH_HANG" ,
						LAOI."HO_VA_TEN" ,

						TBAN."SO_TAI_KHOAN",

						SUM(SL."GHI_NO_NGUYEN_TE" - SL."GHI_CO_NGUYEN_TE") AS "SO_DU_DAU_KY_NGUYEN_TE",
						SUM(SL."GHI_NO" - SL."GHI_CO") AS "SO_DU_DAU_KY",

						0 AS "SO_TIEN_PHAI_THU"  ,	-- Phải thu
						0 AS "SO_TIEN_PHAI_THU_QD"  , -- Phải thu quy đổi

						0 AS "SO_TIEN_CHIET_KHAU"  , -- Chiết khấu
						0 AS "SO_TIEN_CHIET_KHAU_QD"  , -- Chiết khấu quy đổi

						0 AS "SO_TIEN_TRA_LAI"  , --Trả lại/Giảm giá
						0 AS "SO_TIEN_TRA_LAI_QD"  , --Trả lại/giảm giá Quy đổi

						0 AS "CK_GIAM_TRU_KHAC"  ,	--Chiết khấu TT/ giảm trừ khác
						0 AS "CK_GIAM_TRU_KHAC_QD"  , --Chiết khấu TT/ giảm trừ khác quy đổi

						0 AS "SO_DA_THU"  ,	-- Số đã thu
						0 AS "SO_DA_THU_QD"  , -- Số đã thu quy đổi

				        0 AS "SO_DU_CUOI_KY"  ,	-- Số dư cuối kỳ
						0 AS "SO_DU_CUOI_KY_QD"  -- Số dư cuối kỳ quy đổi



				 FROM    so_cai_chi_tiet AS SL
						INNER JOIN DS_KHACH_HANG AS LAOI ON SL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
						INNER JOIN TMP_TAI_KHOAN TBAN ON SL."MA_TAI_KHOAN" = TBAN."SO_TAI_KHOAN"
						INNER JOIN TMP_LIST_BRAND BIDL ON SL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
				 WHERE  SL."NGAY_HACH_TOAN" < v_tu_ngay

						AND (v_loai_tien_id IS NULL OR SL."currency_id" = v_loai_tien_id)
				 GROUP BY
					LAOI."KHACH_HANG_ID" ,
					LAOI."MA_KHACH_HANG" ,
					LAOI."HO_VA_TEN" ,

					TBAN."SO_TAI_KHOAN"
				UNION ALL
					/* Phát sinh trong kỳ */
				SELECT
					LAOI."KHACH_HANG_ID" ,
					LAOI."MA_KHACH_HANG" ,
					LAOI."HO_VA_TEN" ,

					TBAN."SO_TAI_KHOAN",
					0 AS "SO_DU_DAU_KY_NGUYEN_TE",
					0 AS "SO_DU_DAU_KY",
					/*Số phải thu :Ghi tổng số tiền phát sinh Nợ nguyên tệ của TK phải thu chi tiết theo từng khách hàng trong khoảng thời gian xem báo cáo*/
					SUM(SL."GHI_NO_NGUYEN_TE") AS "SO_TIEN_PHAI_THU" ,
					SUM(SL."GHI_NO") AS "SO_TIEN_PHAI_THU_QD",
					 /*Chiết khấu
					  - Đối với QĐ 48,TT200:   = Tổng ps nợ 5211/có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					  - Đối với TT133 =  Tổng Phát sinh đối ứng nợ 511_chi tiết nghiệp vụ Chiết khấu thương mại/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					 */
					CASE WHEN CHE_DO_KE_TOAN = '15'  THEN
							SUM(CASE
								 WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
								 THEN SL."GHI_CO_NGUYEN_TE"
								 ELSE 0
							END)
						ELSE
							SUM(CASE
								 WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%' AND SL."LOAI_NGHIEP_VU" = '0'
								 THEN SL."GHI_CO_NGUYEN_TE"
								 ELSE 0
							END)
					END AS "SO_TIEN_CHIET_KHAU" ,

					CASE WHEN CHE_DO_KE_TOAN = '15'  THEN
							SUM(CASE
								 WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
								 THEN SL."GHI_CO"
								 ELSE 0
							END)
						ELSE
							SUM(CASE --WHEN SL."MA_TK" LIKE '5211%%'
								 --THEN SL."GHI_CO"
								 WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%' AND SL."LOAI_NGHIEP_VU" = '0'
								 THEN SL."GHI_CO"
								 ELSE 0
							END)
					END AS "SO_TIEN_CHIET_KHAU_QD" ,

					/* Giảm giá, trả lại
					- Đối với QĐ 48, TT200: = Tổng PS Nợ TK 5212, TK 5213, 33311/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					- Đối với TT 133: Tổng PS đối ứng Nợ TK 511_chi tiết nghiệp vụ Giảm giá hàng bán, trả lại hàng bán, 33311/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					* */
					CASE WHEN CHE_DO_KE_TOAN = '15'  THEN
							SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
									  OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
									  OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
								 THEN SL."GHI_CO_NGUYEN_TE"
								 ELSE 0
							END)
						ELSE
							SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%' AND SL."LOAI_NGHIEP_VU" IN ('1', '2'))
									  OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
								 THEN SL."GHI_CO_NGUYEN_TE"
								 ELSE 0
							END)
					END AS "SO_TIEN_TRA_LAI" ,

					CASE WHEN CHE_DO_KE_TOAN = '15'  THEN
							SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
									  OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
									  OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
								 THEN SL."GHI_CO"
								 ELSE 0
							END)
						ELSE
							SUM(CASE WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%' AND SL."LOAI_NGHIEP_VU" IN ('1', '2'))
									  OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
								 THEN SL."GHI_CO"
								 ELSE 0
							END)
					END AS "SO_TIEN_TRA_LAI_QD" ,
					/*  CK thanh toán/Giảm trừ khác quy đổi
				   - Đối với QĐ 48, TT 200:   =Tổng  PS nợ TK (không bao gồm các TK 11x, 5211,5212,5213, 33311/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số quy đổi)
					- Đối với TT 133:  = Tổng PS nợ TK (không bao gồm các TK 11x, 33311 và TK 511_chi tiết nghiệp vụ Chiết khấu thương mại, Giảm giá hàng bán, Trả lại hàng bán)/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số quy đổi)
					* */
						CASE WHEN CHE_DO_KE_TOAN = '15'  THEN
								( SUM(SL."GHI_CO_NGUYEN_TE")
								  - SUM(CASE
											   WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
													OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
													OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
													OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
													OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
											   THEN SL."GHI_CO_NGUYEN_TE"
											   ELSE 0
										  END)
								  )
							ELSE
								(
									SUM(SL."GHI_CO_NGUYEN_TE")
								  - SUM(CASE
											   WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%' AND SL."LOAI_NGHIEP_VU" IN ('0','1', '2'))
													OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
													OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
											   THEN SL."GHI_CO_NGUYEN_TE"
											   ELSE 0
										  END)
								)
						END  AS "CK_GIAM_TRU_KHAC",

					 CASE WHEN CHE_DO_KE_TOAN = '15'  THEN
							( SUM(SL."GHI_CO")
							  - SUM(CASE
										   WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5211%%'
												OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5212%%'
												OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '5213%%'
												OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
												OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
										   THEN SL."GHI_CO"
										   ELSE 0
									  END)
							)
						ELSE
							(
								SUM(SL."GHI_CO")
							  - SUM(CASE
										   WHEN (SL."MA_TAI_KHOAN_DOI_UNG" LIKE '511%%' AND SL."LOAI_NGHIEP_VU" IN ('0','1', '2'))
												OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '33311%%'
												OR SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
										   THEN SL."GHI_CO"
										   ELSE 0
										END)
							)
						END AS "CK_GIAM_TRU_KHAC_QD",

						/*  Số đã thu
						 = Tổng PS Nợ TK 11x/Có TK phải thu tương ứng với từng khách hàng chọn xem báo cáo theo số tiền nguyên tệ trong khoảng thời gian xem báo cáo

						* */
						SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
								 THEN SL."GHI_CO_NGUYEN_TE"
								 ELSE 0
							END) ,
						SUM(CASE WHEN SL."MA_TAI_KHOAN_DOI_UNG" LIKE '11%%'
								 THEN SL."GHI_CO"
								 ELSE 0
							END) ,
						0 ,
						0

				FROM    so_cai_chi_tiet AS SL
						INNER  JOIN DS_KHACH_HANG AS LAOI ON SL."DOI_TUONG_ID" = LAOI."KHACH_HANG_ID"
						INNER JOIN TMP_TAI_KHOAN TBAN ON SL."MA_TAI_KHOAN" = TBAN."SO_TAI_KHOAN"
						INNER JOIN TMP_LIST_BRAND BIDL ON SL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
				WHERE   SL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay and v_den_ngay

						AND ( v_loai_tien_id IS NULL
							  OR SL."currency_id" = v_loai_tien_id
							)
				GROUP BY
				LAOI."KHACH_HANG_ID" ,
				LAOI."MA_KHACH_HANG" ,
				LAOI."HO_VA_TEN" ,

				TBAN."SO_TAI_KHOAN"
			) AS A
			GROUP BY
				A."KHACH_HANG_ID" ,
				A."MA_KHACH_HANG" ,
				A."HO_VA_TEN" ,

				A."SO_TAI_KHOAN";


			/*Tính số dư cuối kỳ*/

		UPDATE TMP_KET_QUA

		SET "SO_DU_CUOI_KY" =  COALESCE("SO_DU_DAU_KY_NGUYEN_TE",0) + COALESCE("SO_TIEN_PHAI_THU",0) - COALESCE("SO_TIEN_CHIET_KHAU",0) - COALESCE("SO_TIEN_TRA_LAI",0) - COALESCE("CK_GIAM_TRU_KHAC",0) - COALESCE("SO_DA_THU",0),
			"SO_DU_CUOI_KY_QD" = COALESCE("SO_DU_DAU_KY",0) + COALESCE("SO_TIEN_PHAI_THU_QD",0) - COALESCE("SO_TIEN_CHIET_KHAU_QD",0)- COALESCE("SO_TIEN_TRA_LAI_QD",0) - COALESCE("CK_GIAM_TRU_KHAC_QD",0) - COALESCE("SO_DA_THU_QD",0)

;

    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS
             SELECT
                "KHACH_HANG_ID"  ,
              "MA_KHACH_HANG" ,   -- Mã KH
              "HO_VA_TEN" ,	-- Tên KH

              "SO_TAI_KHOAN"   ,  -- Tài khoản
                "SO_DU_DAU_KY_NGUYEN_TE",
                 "SO_DU_DAU_KY"	,-- Số dư đầu kỳ
			 -- Dư đầu kỳ quy đổi

              "SO_TIEN_PHAI_THU",	-- Phải thu
              "SO_TIEN_PHAI_THU_QD" , -- Phải thu quy đổi

              "SO_TIEN_CHIET_KHAU" , -- Chiết khấu
              "SO_TIEN_CHIET_KHAU_QD" , -- Chiết khấu quy đổia

              "SO_TIEN_TRA_LAI" , --Trả lại/Giảm giá
              "SO_TIEN_TRA_LAI_QD" , --Trả lại/giảm giá Quy đổi

              "CK_GIAM_TRU_KHAC",	--Chiết khấu TT/ giảm trừ khác
              "CK_GIAM_TRU_KHAC_QD", --Chiết khấu TT/ giảm trừ khác quy đổi

              "SO_DA_THU" ,	-- Số đã thu
              "SO_DA_THU_QD" , -- Số đã thu quy đổi

              "SO_DU_CUOI_KY" ,	-- Số dư cuối kỳ
              "SO_DU_CUOI_KY_QD"  -- Số dư cuối kỳ quy đổi


   FROM   TMP_KET_QUA
   WHERE
       "SO_DU_DAU_KY_NGUYEN_TE" <>0
	  OR "SO_DU_DAU_KY" <> 0
      OR "SO_TIEN_PHAI_THU" <> 0
      OR "SO_TIEN_PHAI_THU_QD" <> 0
      OR "SO_TIEN_CHIET_KHAU" <> 0
      OR "SO_TIEN_CHIET_KHAU_QD" <> 0
      OR "SO_TIEN_TRA_LAI" <> 0
      OR "SO_TIEN_TRA_LAI_QD" <> 0
      OR "CK_GIAM_TRU_KHAC" <> 0
      OR "CK_GIAM_TRU_KHAC_QD" <> 0
      OR "SO_DA_THU"  <> 0
      OR "SO_DA_THU_QD" <> 0
      OR "SO_DU_CUOI_KY" <> 0
      OR "SO_DU_CUOI_KY_QD" <> 0

		   ORDER BY
                 "MA_KHACH_HANG",
                 "HO_VA_TEN",
                 "SO_TAI_KHOAN"

;



END $$
;

SELECT 
    "MA_KHACH_HANG" AS "MA_KHACH_HANG",
    "HO_VA_TEN" AS "TEN_KHACH_HANG",
    "SO_TAI_KHOAN" AS "TAI_KHOAN_CONG_NO",
    "SO_DU_DAU_KY_NGUYEN_TE" AS "SO_DU_DAU_KY",
    "SO_TIEN_PHAI_THU" AS "SO_PHAI_THU",
    "SO_TIEN_CHIET_KHAU" AS "CHIET_KHAU",
    "SO_TIEN_TRA_LAI" AS "TRA_LAI_HOAC_GIAM_GIA",
    "CK_GIAM_TRU_KHAC" AS "CK_THANH_TOAN_HOAC_GT_KHAC",
    "SO_DA_THU" AS "SO_DA_THU",
    "SO_DU_CUOI_KY" AS "SO_DU_CUOI_KY"
FROM TMP_KET_QUA_CUOI_CUNG
OFFSET %(offset)s
LIMIT %(limit)s
;

        """
        return self.execute(query,params_sql)
   

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_TONG_HOP_CONG_NO_PHAI_THU_KHACH_HANG, self).default_get(fields_list)
        chi_nhanh =  self.env['danh.muc.to.chuc'].search([],limit=1)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_DOI_TUONG', '=', 'True'),('DOI_TUONG_SELECTION', '=like', '1')],limit=1)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if tai_khoan:
            result['TAI_KHOAN_ID'] = tai_khoan.id
        if loai_tien:
            result['currency_id'] = loai_tien.id
      

        return result

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

        
    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'

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


        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO in ('KHONG_CHON','NHAN_VIEN_VA_KHACH_HANG','CONG_TRINH','HOP_DONG','DON_DAT_HANG','DON_VI_KINH_DOANH','CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU'):
            if CHON_TAT_CA_KHACH_HANG == 'False':
                if KHACH_HANG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO in ('NHAN_VIEN','NHAN_VIEN_VA_KHACH_HANG'):
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

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        currency_id = self.get_context('currency_id')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        loai_tien_id = self.env['res.currency'].browse(currency_id)
        loai_tien = ''
        if loai_tien_id: 
            loai_tien = loai_tien_id.MA_LOAI_TIEN
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan = ''
        tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        if tai_khoan_id:
            tai_khoan = tai_khoan_id.SO_TAI_KHOAN
        param = 'Tài khoản: %s; Loại tiền: %s; Từ ngày: %s đến ngày %s' % (tai_khoan, loai_tien, TU_NGAY_F, DEN_NGAY_F)
        if (THONG_KE_THEO == 'KHONG_CHON'):
            action = self.env.ref('bao_cao.open_report__ttong_hop_cong_no_phai_thu_khach_hang_khongchon').read()[0]
        elif THONG_KE_THEO == 'NHAN_VIEN':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_nhanvien').read()[0]
        elif THONG_KE_THEO == 'NHAN_VIEN_VA_KHACH_HANG':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_nhanvienvakh').read()[0]
        elif THONG_KE_THEO == 'CONG_TRINH':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_congtrinh').read()[0]
        elif THONG_KE_THEO == 'DON_DAT_HANG':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_dondathang').read()[0]
        elif THONG_KE_THEO == 'CHI_TIET_THEO_CAC_KHOAN_GIAM_TRU':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_cackhoangiamtru').read()[0]
        elif THONG_KE_THEO == 'DON_VI_KINH_DOANH':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_donvikinhdoanh').read()[0]
        elif THONG_KE_THEO == 'HOP_DONG':
            action = self.env.ref('bao_cao.open_report__tong_hop_cong_no_phai_thu_khach_hang_hopdong').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action