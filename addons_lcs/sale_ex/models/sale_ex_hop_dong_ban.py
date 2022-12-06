# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
class SALE_EX_HOP_DONG_BAN(models.Model):
    _inherit = 'sale.ex.hop.dong.ban'
    _order = "NGAY_GHI_DOANH_SO desc"

    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng', auto_num='sale_ex_hop_dong_ban_SO_HOP_DONG', required=True)
    NGAY_GHI_DOANH_SO = fields.Date(string='Ngày ghi doanh số', help='Ngày ghi doanh số',default=fields.Datetime.now)
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký',default=fields.Datetime.now, required=True)
    THUOC_DU_AN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Thuộc dự án', help='Thuộc dự án')
    TRICH_YEU = fields.Text(string='Trích yếu', help='Trích yếu')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    GIA_TRI_HOP_DONG = fields.Monetary(string='Giá trị hợp đồng', help='Giá trị hợp đồng', currency_field='currency_id')
    GIA_TRI_HOP_DONG_QUY_DOI = fields.Monetary(string='Giá trị hợp đồng quy đổi', help='Giá trị hợp đồng quy đổi', currency_field='currency_id')
    GTHD_QUY_DOI = fields.Monetary(string='GTHĐ quy đổi', help='Giá trị hợp đồng', currency_field='base_currency_id')
    GIA_TRI_THANH_LY = fields.Monetary(string='Giá trị thanh lý', help='Giá trị thanh lý', currency_field='currency_id')
    GTTL_QUY_DOI = fields.Monetary(string='GTTL quy đổi', help='Gttl quy đổi', currency_field='base_currency_id')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    HAN_GIAO_HANG = fields.Date(string='Hạn giao hàng', help='Hạn giao hàng')
    LA_HOP_DONG_DU_AN_PHAT_SINH_TRUOC_KHI_SU_DUNG_PHAN_MEM = fields.Boolean(string='Là hợp đồng dự án phát sinh trước khi sử dụng phần mềm', help='Là hợp đồng dự án phát sinh trước khi sử dụng phần mềm')
    SO_DA_CHI = fields.Monetary(string='Số đã chi', help='Số đã chi')
    SO_DA_THU = fields.Monetary(string='Số đã thu', help='Số đã thu', currency_field='currency_id')
    SO_DA_THU_QUY_DOI = fields.Monetary(string='Số đã thu quy đổi', help='Số đã thu quy đổi', currency_field='base_currency_id')
    GIA_TRI_DA_XUAT_HD = fields.Monetary(string='Giá trị đã xuất HĐ', help='Giá trị đã xuất hđ', currency_field='currency_id')
    GT_DA_XUAT_HD_QUY_DOI = fields.Monetary(string='GT đã xuất HĐ quy đổi', help='Gt đã xuất hđ quy đổi', currency_field='base_currency_id')
    DOANH_THU = fields.Float(string='Doanh thu', help='Doanh thu',digits= decimal_precision.get_precision('VND'))
    GIA_VON_HANG_BAN = fields.Float(string='Giá vốn hàng bán', help='Giá vốn hàng bán',digits= decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='Chi phí khác', help='Chi phí khác',digits= decimal_precision.get_precision('VND'))
    KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    NGUOI_LIEN_HE = fields.Char(string='Người liên hệ ', help='Người liên hệ ')
    DON_VI_THUC_HIEN_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị thực hiện', help='Đơn vị thực hiện')
    NGUOI_THUC_HIEN_ID = fields.Many2one('res.partner', string='Người thực hiện', help='Người thực hiện')
    TINH_TRANG_HOP_DONG = fields.Selection([('0', 'Chưa thực hiện'), ('1', ' Đang thực hiện'), ('2', ' Đã thanh lý'), ('3', ' Đã hủy bỏ'), ], string='Tình trạng hợp đồng', help='Tình trạng hợp đồng',default='0')
    NGAY_THANH_LY_HUY_BO = fields.Date(string='Ngày thanh lý hủy bỏ', help='Ngày thanh lý hủy bỏ')
    LY_DO = fields.Char(string='Lý do', help='Lý do')
    DIEU_KHOAN_KHAC = fields.Char(string='Điều khoản khác', help='Điều khoản khác')
    TINH_GIA_THANH = fields.Boolean(string='Tính giá thành', help='Tính giá thành')
    DA_XUAT_HOA_DON = fields.Boolean(string='Đã xuất hóa đơn', help='Đã xuất hóa đơn')

    TIEN_HANG = fields.Monetary(string='Tiền hàng', help='Tiền hàng', compute='tinhtongtien',store=True, currency_field='currency_id')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',  currency_field='currency_id',compute='tinhtongtien',store=True)
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt',currency_field='currency_id',compute='tinhtongtien',store=True)
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',  currency_field='currency_id',compute='tinhtongtien',store=True)

    TIEN_HANG_QUY_DOI = fields.Monetary(string='Tiền hàng quy đổi', help='Tiền hàng quy đổi', currency_field='base_currency_id',compute='tinhtongtien',store=True)
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id',compute='tinhtongtien',store=True)
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id',compute='tinhtongtien',store=True)
    TONG_TIEN_THANH_TOAN_QUY_DOI = fields.Monetary(string='Tổng tiền thanh toán quy đổi', help='Tổng tiền thanh toán quy đổi', currency_field='base_currency_id',compute='tinhtongtien',store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='', help='Đơn đặt hàng')
    HOP_DONG_DU_AN_SELECTION = fields.Selection([
        ('HOP_DONG', 'Hợp đồng'), 
        ('DU_AN', 'Dự án') 
        ],default='HOP_DONG', string='NO_SAVE')

    DU_KIEN_CHI = fields.Float(string='Dự kiến chi', help='Dự kiến chi',digits= decimal_precision.get_precision('VND'),compute="tong_du_kien_chi",store=True)
    THUC_CHI = fields.Float(string='Thực chi', help='Thực chi',digits= decimal_precision.get_precision('VND'))
    SO_CON_PHAI_CHI = fields.Float(string='Số còn phải chi', help='Số còn phải chi',digits= decimal_precision.get_precision('VND'))
    THUC_THU = fields.Float(string='Thực thu', help='Thực thu',digits= decimal_precision.get_precision('VND'))
    SO_CON_PHAI_THU = fields.Float(string='Số còn phải thu', help='Số còn phải thu',digits= decimal_precision.get_precision('VND'))
    DU_KIEN_LAI_LO = fields.Float(string='Dự kiến lãi lỗ', help='Dự kiến lãi lỗ',digits= decimal_precision.get_precision('VND'))
    LA_DU_AN = fields.Boolean(string='Là dự án', help='Là dự án')
    TINH_THANH_PHO = fields.Char(string='Tỉnh/Thành phố', help='Tỉnh thành phố')
    QUAN_HUYEN = fields.Char(string='Quận/Huyện', help='Quận huyện')
    XA_PHUONG = fields.Char(string='Xã/Phường', help='Xã phường')


    SALE_EX_HOP_DONG_BAN_CHI_TIET_THUC_THU_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.thuc.thu', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết thực thu', copy=True)
    SALE_EX_HOP_DONG_BAN_CHI_TIET_BAN_HANG_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.ban.hang', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết bán hàng', copy=True)
    SALE_EX_HOP_DONG_BAN_CHI_TIET_GHI_NHAN_DOANH_SO_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.ghi.nhan.doanh.so', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết ghi nhận doanh số', copy=True)
    SALE_EX_HOP_DONG_BAN_CHI_TIET_THUC_THI_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.thuc.thi', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết thực thi', copy=True)
    SALE_EX_HOP_DONG_BAN_CHI_TIET_DU_KIEN_CHI_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.du.kien.chi', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết dự kiến chi', copy=True)
    SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.hang.hoa.dich.vu', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết hàng hóa dịch vụ', copy=True)
   
    SALE_EX_HOP_DONG_BAN_CHI_TIET_LIEN_HE_IDS = fields.One2many('sale.ex.hop.dong.ban.chi.tiet.lien.he', 'HOP_DONG_BAN_ID', string='Hợp đồng bán chi tiết liên hệ', copy=True)

    CONG_TIEN_TRU_CK = fields.Monetary(string='Cộng tiền hàng(đã trừ CK)', help='Cộng tiền hàng(đã trừ CK)', currency_field='base_currency_id')
    TY_LE_CK_MT = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ CK',digits=decimal_precision.get_precision('VND'))
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')

    name = fields.Char(string='name', help='name',related='SO_HOP_DONG',store=True)
    isparent = fields.Boolean(string='là hợp đồng tổng hợp', help='là hợp đồng tổng hợp')

    _sql_constraints = [
        ('SO_HOP_DONG_uniq', 'unique ("SO_HOP_DONG")', 'Số hợp đồng <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.onchange('KHACH_HANG_ID')
    def thay_doi_theo_kh(self):
        self.TEN_KHACH_HANG = self.KHACH_HANG_ID.HO_VA_TEN
        self.DIA_CHI = self.KHACH_HANG_ID.DIA_CHI
       
    @api.onchange('currency_id')
    def thay_doi_loai_tien(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        for record in self.SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS:
            record.DON_GIA_QUY_DOI = self.TY_GIA * record.DON_GIA
            record.THANH_TIEN_QUY_DOI = self.TY_GIA * record.THANH_TIEN
            record.TIEN_CHIET_KHAU_QUY_DOI = self.TY_GIA * record.TIEN_CHIET_KHAU
            record.TIEN_THUE_GTGT_QUY_DOI = self.TY_GIA * record.TIEN_THUE_GTGT


    @api.onchange('TY_GIA')
    def update_thay_doi_theo_ty_gia(self):
        if self.TY_GIA == 1 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False
        
        

    @api.onchange('GIA_TRI_HOP_DONG','GIA_TRI_THANH_LY','SO_DA_THU','GIA_TRI_DA_XUAT_HD','TY_GIA')
    def thay_doi_gia_tri_hop_dong(self):
        self.GIA_TRI_THANH_LY = self.GIA_TRI_HOP_DONG 
        self.GTHD_QUY_DOI = float_round(self.GIA_TRI_HOP_DONG *self.TY_GIA, 0)
        self.GTTL_QUY_DOI = float_round(self.GIA_TRI_THANH_LY *self.TY_GIA, 0)
        self.SO_DA_THU_QUY_DOI = float_round(self.SO_DA_THU *self.TY_GIA, 0)
        self.GT_DA_XUAT_HD_QUY_DOI = float_round(self.GIA_TRI_DA_XUAT_HD *self.TY_GIA, 0)

    @api.onchange('DON_DAT_HANG_ID')
    def onchange_hop_dong_ban(self):
        if self.DON_DAT_HANG_ID:
            for record in self:
                record.KHACH_HANG_ID = record.DON_DAT_HANG_ID.KHACH_HANG_ID
                record.NGUOI_LIEN_HE = record.DON_DAT_HANG_ID.NGUOI_NHAN_HANG
                record.TEN_KHACH_HANG = record.DON_DAT_HANG_ID.TEN_KHACH_HANG
                record.DIA_CHI = record.DON_DAT_HANG_ID.DIA_CHI
        
                record.currency_id = record.DON_DAT_HANG_ID.currency_id

    
    @api.onchange('DON_DAT_HANG_ID')
    def update_hop_dong_ban_chi_tiet(self):
        if self.DON_DAT_HANG_ID:
            self.SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS = []
            for don_dat_hang_chi_tiet in self.DON_DAT_HANG_ID.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                new_line = self.env['sale.ex.hop.dong.ban.chi.tiet.hang.hoa.dich.vu'].new({
                    'MA_HANG_ID' : don_dat_hang_chi_tiet.MA_HANG_ID,
                    'TEN_HANG' : don_dat_hang_chi_tiet.TEN_HANG,
                    'DVT_ID' : don_dat_hang_chi_tiet.DVT_ID,
                    'SO_LUONG_YEU_CAU' : don_dat_hang_chi_tiet.SO_LUONG,
                    'DON_GIA' : don_dat_hang_chi_tiet.DON_GIA,
                    
                    'THANH_TIEN' : don_dat_hang_chi_tiet.THANH_TIEN,
                    'THANH_TIEN_QUY_DOI' : don_dat_hang_chi_tiet.THANH_TIEN_QUY_DOI,
                    'PHAN_TRAM_THUE_GTGT_ID' : don_dat_hang_chi_tiet.PHAN_TRAM_THUE_GTGT_ID,
                    'TIEN_THUE_GTGT' : don_dat_hang_chi_tiet.TIEN_THUE_GTGT,
                    'TIEN_THUE_GTGT_QUY_DOI' : don_dat_hang_chi_tiet.TIEN_THUE_GTGT_QUY_DOI,
                })
                self.SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS += new_line
    
    @api.model
    def default_get(self, fields):
        rec = super(SALE_EX_HOP_DONG_BAN, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if currency_id:
            rec['currency_id'] = currency_id.id
        rec['LOAI_CHUNG_TU'] = 9041
        return rec

    @api.depends('SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS')
    def tinhtongtien(self):
        for order in self:
            tong_tien_hang = tong_tien_thue_gtgt = tong_tien_thanh_toan = tong_tien_chiet_khau =tong_tien_hang_quy_doi = tong_tien_thue_gtgt_quy_doi  = tong_tien_chiet_khau_quy_doi = tong_tien_thanh_toan_quy_doi  = 0.0
            cong_tien_hang_ck=0.0
            ty_le_ck=0.0
            for line in order.SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU_IDS:
                tong_tien_hang += line.THANH_TIEN
                tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
                tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt - tong_tien_chiet_khau

                tong_tien_hang_quy_doi += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_quy_doi += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_chiet_khau_quy_doi += line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_thanh_toan_quy_doi = tong_tien_hang_quy_doi + tong_tien_thue_gtgt_quy_doi - tong_tien_chiet_khau_quy_doi
                cong_tien_hang_ck = tong_tien_hang_quy_doi - tong_tien_chiet_khau_quy_doi
            if tong_tien_hang_quy_doi>0:
                ty_le_ck = tong_tien_chiet_khau_quy_doi / tong_tien_hang_quy_doi *100
            order.update({
                'TIEN_HANG': tong_tien_hang,
                'TIEN_THUE_GTGT': tong_tien_thue_gtgt,
                'TIEN_CHIET_KHAU': tong_tien_chiet_khau,
                'TONG_TIEN_THANH_TOAN': tong_tien_thanh_toan,

                'TIEN_HANG_QUY_DOI': tong_tien_hang_quy_doi,
                'TIEN_THUE_GTGT_QUY_DOI': tong_tien_thue_gtgt_quy_doi,
                'TIEN_CHIET_KHAU_QUY_DOI': tong_tien_chiet_khau_quy_doi,
                'TONG_TIEN_THANH_TOAN_QUY_DOI': tong_tien_thanh_toan_quy_doi,

                'GIA_TRI_HOP_DONG': tong_tien_thanh_toan,
                'GTHD_QUY_DOI': tong_tien_thanh_toan_quy_doi,
                'GIA_TRI_THANH_LY': tong_tien_thanh_toan,
                'GTTL_QUY_DOI': tong_tien_thanh_toan_quy_doi,

                'TY_LE_CK_MT': ty_le_ck,
                'CONG_TIEN_TRU_CK': cong_tien_hang_ck,
            })

    @api.depends('SALE_EX_HOP_DONG_BAN_CHI_TIET_DU_KIEN_CHI_IDS')
    def tong_du_kien_chi(self):
        for  chi_tiet_du_kien_chi in self:

            tong_so_tien_du_kien =0.0
            for chi_tiet in chi_tiet_du_kien_chi.SALE_EX_HOP_DONG_BAN_CHI_TIET_DU_KIEN_CHI_IDS:
                tong_so_tien_du_kien += chi_tiet.SO_TIEN
            chi_tiet_du_kien_chi.update({
                'DU_KIEN_CHI':tong_so_tien_du_kien,
            })
        
    
    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
		DROP VIEW IF EXISTS  view_hop_dong_ban;--View_CTContract
                CREATE VIEW view_hop_dong_ban
                AS
                     SELECT  
                            CT."id" AS "ID_CHUNG_TU",
                            'sale.ex.hop.dong.ban' AS "MODEL_CHUNG_TU",
                            CT."CHI_NHANH_ID" ,
                            CT."LOAI_CHUNG_TU" ,
                            CT."HOP_DONG_DU_AN_SELECTION" ,
                            CT."THUOC_DU_AN_ID" ,
                            CT."SO_HOP_DONG" ,
                            CT."NGAY_KY" ,
                            CT."TRICH_YEU" ,
                            CT."currency_id" ,
                            CT."TY_GIA" ,
                            CT."GIA_TRI_HOP_DONG" ,
                            CT."GTHD_QUY_DOI" ,
                            CT."GIA_TRI_THANH_LY" ,
                            CT."GTTL_QUY_DOI" ,
                            CT."HAN_THANH_TOAN" ,
                            CT."HAN_GIAO_HANG" ,
                            CT."LA_HOP_DONG_DU_AN_PHAT_SINH_TRUOC_KHI_SU_DUNG_PHAN_MEM" ,
                            CT."SO_DA_CHI" ,
                            CT."SO_DA_THU" ,
                            CT."SO_DA_THU_QUY_DOI" ,
                            CT."GIA_TRI_DA_XUAT_HD" ,
                            CT."GT_DA_XUAT_HD_QUY_DOI" ,
                            CT."KHACH_HANG_ID" ,
                            CT."DIA_CHI" ,
                            CT."NGUOI_LIEN_HE" ,
                            CT."DON_VI_THUC_HIEN_ID" ,
                            CT."NGUOI_THUC_HIEN_ID" ,
                            CT."TINH_TRANG_HOP_DONG" ,
                            CT."NGAY_THANH_LY_HUY_BO" ,
                            CT."LY_DO" ,

                            CT."DIEU_KHOAN_KHAC" ,
                            CT."TINH_GIA_THANH" ,
                            CT."DA_XUAT_HOA_DON" ,
                            CT."NGAY_GHI_DOANH_SO" ,



                            CT2."SO_HOP_DONG" AS "THUOC_DU_AN" ,
                            AO1."MA" AS "MA_KHACH_HANG" ,

                            CT."TEN_KHACH_HANG" AS "TEN_KHACH_HANG" ,
                            OU."TEN_DON_VI" AS "DON_VI_SU_DUNG" ,
                            AO2."HO_VA_TEN" AS "TEN_NHAN_VIEN_BAN_HANG" ,

                            AO1."TINH_TP_ID" AS "TINH/TP" ,
                            AO1."QUAN_HUYEN_ID" AS "QUABN_HUYEN",
                            AO1."XA_PHUONG_ID" AS "XA_PHUONG"



                    FROM    sale_ex_hop_dong_ban AS CT
                            LEFT OUTER JOIN res_partner AS AO1 ON AO1."id" = CT."KHACH_HANG_ID"
                                                                        AND AO1."LA_KHACH_HANG" = TRUE
                            LEFT OUTER JOIN danh_muc_to_chuc AS OU ON OU."id" = CT."DON_VI_THUC_HIEN_ID"
                            LEFT OUTER JOIN res_partner AS AO2 ON AO2."id" = CT."NGUOI_THUC_HIEN_ID"
                                                                        AND AO2."LA_NHAN_VIEN" = TRUE

                            LEFT OUTER JOIN sale_ex_hop_dong_ban AS CT2 ON CT."THUOC_DU_AN_ID" = CT2."id" ;

		""")
