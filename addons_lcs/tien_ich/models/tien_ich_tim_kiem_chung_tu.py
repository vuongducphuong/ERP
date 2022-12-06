# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo import tools

class TIEN_ICH_TIM_KIEM_CHUNG_TU(models.Model):
    _name = 'tien.ich.tim.kiem.chung.tu'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False
    TIM_THEO = fields.Selection([('NGAY_CHUNG_TU', 'Ngày chứng từ'), ], string='Tìm theo', help='Tìm theo',default='NGAY_CHUNG_TU',required=True)
    DIEU_KIEN = fields.Selection([('BANG', 'Bằng'), ('NHO_HON', 'Nhỏ hơn'), ('NHO_HON_HOAC_BANG', 'Nhỏ hơn hoặc bằng'), ('LON_HON', 'Lớn hơn'), ('LON_HON_HOAC_BANG', 'Lớn hơn hoặc bằng'), ('TRONG_KHOANG', 'Trong khoảng'), ], string='Điều kiện', help='Điều kiện',required=True,default='BANG')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now,required=True)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now,required=True)
    NHOM_THEO_CHUNG_TU = fields.Boolean(string='Nhóm theo chứng từ', help='Nhóm theo chứng từ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GIA_TRI = fields.Date(string='Giá trị', help='Giá trị',default='2018-01-01',required=True)
    TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON_IDS = fields.One2many('tien.ich.tim.kiem.chung.tu.cac.dieu.kien.da.chon', 'TIM_KIEM_CHUNG_TU_ID', string='Tìm kiếm chứng từ các điều kiện đã chọn')
    TIEN_ICH_TIM_KIEM_CHUNG_TU_KET_QUA_TIM_KIEM_IDS = fields.One2many('tien.ich.tim.kiem.chung.tu.ket.qua.tim.kiem', 'TIM_KIEM_CHUNG_TU_KET_QUA_TIM_KIEM_ID', string='Tìm kiếm chứng từ kết quả tìm kiếm ')


    STT = fields.Integer(string='STT', help='Số thứ tự')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    TEN_LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK có', help='Tài khoản có')
    currency_id = fields.Many2one('res.currency',string='Loại tiền', help='Loại tiền')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    SO_TIEN_QUY_DOI = fields.Float(string='Quy đổi', help='Quy đổi',digits=decimal_precision.get_precision('Product Price'))
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa',string='Mã VTHH', help='Mã vật tư hàng hóa')
    TEN_VTHH = fields.Char(string='Tên VTHH', help='Tên vật tư hàng hóa')
    MA_KHO_NHAP_ID = fields.Many2one('stock.ex.nhap.xuat.kho' ,string='Kho nhập', help='Kho nhập')
    MA_KHO_XUAT_ID = fields.Many2one('stock.ex.nhap.xuat.kho',string='Kho xuất', help='Kho xuất')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh',string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng ', help='Số lượng ', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ chiết khấu',digits= decimal_precision.get_precision('Product Price'))
    SO_TIEN_CHIET_KHAU = fields.Float(string='Tiền CK', help='Tiền chiết khấu',digits= decimal_precision.get_precision('Product Price'))
    LOAI_TSCD_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại TSCĐ', help='Loại TSCĐ')
    TSCD_ID = fields.Many2one('asset.ghi.tang', string='Mã TSCĐ', help='Mã tài sản cố định')
    CCDC_ID = fields.Many2one('supply.ghi.tang', string='Mã CCDC', help='Mã công cụ dụng cụ')
    DOI_TUONG_NO_ID = fields.Many2one('res.partner' , string='Đối tượng nợ', help='Đối tượng nợ')
    DOI_TUONG_CO_ID = fields.Many2one('res.partner' , string='Đối tượng có', help='Đối tượng có')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc' ,string='Đơn vị', help='Đơn vị')
    NHAN_VIEN_ID = fields.Many2one('res.partner' ,string='Nhân viên', help='Nhân viên')
    TK_NGAN_HANG = fields.Many2one('danh.muc.tai.khoan.ngan.hang',string='Tài khoản ngân hàng', help='Tài khoản ngân hàng')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp' ,string='Khoản mục chi phí', help='Khoản mục chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh',string='Công trình', help='Công trình')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi',string='ĐT tập hợp chi phí', help='Đối tượng tập hợp chi phí')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang',string='Đơn mua hàng', help='Đơn mua hàng')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang',string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang',string='Hợp đồng mua', help='Hợp đồng mua')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban',string='Hợp đồng bán', help='Hợp đồng bán')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke',string='Mã thống kê', help='Mã thống kê')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='Diễn giải chung')
    DIEN_GIAI = fields.Char(string='Diễn giải chi tiết', help='Tìm kiếm chứng từ')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc' ,string='Đơn vị', help='Đơn vị')
    TINH_TRANG_GHI_SO = fields.Boolean(string='Tình trạng ghi sổ', help='Diễn giải chi tiết')
    ID_GOC = fields.Integer()
    MODEL_GOC = fields.Char ()
    SOURCE_ID = fields.Reference(selection=[], string='Lập từ')

    selection_tim_kiem_chung_tu= fields.Selection([
        ('tat_ca_chung_tu', 'Tất cả chứng từ'),
        ('chung_tu_da_ghi_so','Chứng từ đã ghi sổ'),
        ('chung_tu_chua_ghi_so','Chứng từ chưa ghi sổ'),
        ], default='tat_ca_chung_tu',string=" ")

    @api.model  
    def action_them_dieukien_open(self):
        env = self.env['tien.ich.tim.kiem.chung.tu.cac.dieu.kien.da.chon']
        self.TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON_IDS = []
        if self.TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON_IDS.VA_HOAC == False:
            new_line = env.new({
                'VA_HOAC': ' ',
                'TIM_THEO': self.TIM_THEO ,
                'TU_NGAY':  self.TU_NGAY ,
                'DEN_NGAY' : self.DEN_NGAY,
                'GIA_TRI' : self.amount,
                'DIEU_KIEN': 'Từ ngày ' + str(self.TU_NGAY) + ' đến ngày '+ str(self.DEN_NGAY) if self.DIEU_KIEN == 'TRONG_KHOANG' else str(self.DIEU_KIEN) + ' ' + str(self.amount),
            # if self.DIEU_KIEN == 'TRONG_KHOANG' :
            #     'DIEU_KIEN': 'Từ ngày' + str(self.TU_NGAY) + 'đến ngày' + str(self.DEN_NGAY),     
            # else:
            #     'DIEU_KIEN': str(self.DIEU_KIEN) + str(self.amount),
                })
            self.TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON_IDS += new_line
        else : 
            new_line = env.new({
                'VA_HOAC': 'Và',
                'TIM_THEO': self.TIM_THEO ,
                'TU_NGAY':  self.TU_NGAY ,
                'DEN_NGAY' : self.DEN_NGAY,
                'GIA_TRI' : self.amount,
                'DIEU_KIEN': 'Từ ngày ' + str(self.TU_NGAY) + ' đến ngày '+ str(self.DEN_NGAY) if self.DIEU_KIEN == 'TRONG_KHOANG' else str(self.DIEU_KIEN) + ' ' + str(self.amount),
            # if self.DIEU_KIEN =='TRONG_KHOANG' :
            #     'DIEU_KIEN': 'Từ ngày' + str(self.TU_NGAY) + 'đến ngày' + str(self.DEN_NGAY),     
            # else:
            #     'DIEU_KIEN': str(self.DIEU_KIEN) + str(self.amount),
                })
            self.TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON_IDS += new_line

    @api.model
    def action_timkiem_chungtu_open(self):
        env=self.env['tien.ich.tim.kiem.chung.tu.ket.qua.tim.kiem']
        self.TIEN_ICH_TIM_KIEM_CHUNG_TU_KET_QUA_TIM_KIEM_IDS = []
        dktk =[]
        for line in self.TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON_IDS:
            tu_ngay_dk =  line.TU_NGAY 
            den_ngay_dk = line.DEN_NGAY
            dktk += [('NGAY_CHUNG_TU','>=',tu_ngay_dk),('NGAY_CHUNG_TU','<=',den_ngay_dk)]

        chungtu_ds = self.env['account.ex.phieu.thu.chi'].search(dktk)
        for ct in chungtu_ds:
            new_line = env.new({
                'LOAI_CHUNG_TU': 'Phiếu thu',
                'NGAY_HACH_TOAN': ct.NGAY_HACH_TOAN,
                'NGAY_CHUNG_TU': ct.NGAY_CHUNG_TU,
                'SO_CHUNG_TU': ct.SO_CHUNG_TU,
                'SO_HOA_DON':'',
                'DIEN_GIAI': ct.DIEN_GIAI,
                
            })
            self.TIEN_ICH_TIM_KIEM_CHUNG_TU_KET_QUA_TIM_KIEM_IDS += new_line

    def _get_added_domain(self):
        model_list = self.execute('SELECT "MODEL_GOC" FROM tien_ich_tim_kiem_chung_tu GROUP BY "MODEL_GOC"')
        access_list = []
        for model in model_list:
            if self.env[model.get('MODEL_GOC')].check_access_rights('view', False):
                access_list += [model.get('MODEL_GOC')]
        if len(model_list) != len(access_list):
            return [('MODEL_GOC', 'in', tuple(access_list))]
        return []

    @api.model
    def search_count(self, args):
        args = (args or []) + self._get_added_domain()
        return super(TIEN_ICH_TIM_KIEM_CHUNG_TU, self).search_count(args)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = (domain or []) + self._get_added_domain()
        return super(TIEN_ICH_TIM_KIEM_CHUNG_TU, self).search_read(domain, fields, offset, limit, order)
        