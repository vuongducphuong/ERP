# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime


class GIA_THANH_KY_TINH_GIA_THANH(models.Model):
    _name = 'gia.thanh.ky.tinh.gia.thanh'
    _description = 'Kỳ tính giá thành'
    _inherit = ['mail.thread']
    KY = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ', help='Kỳ tính giá thành', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    TEN = fields.Char(string='Tên', help='Tên ')
    LOAI_GIA_THANH = fields.Selection([('DON_GIAN', 'Đơn giản'), ('HE_SO_TY_LE', 'Hệ số tỷ lệ'),('PHAN_BUOC', 'Phân bước'), ('CONG_TRINH', 'Công trình'), ('DON_HANG', 'Đơn hàng'), ('HOP_DONG', 'Hợp đồng'), ], string='Loại giá thành', help='Loại giá thành')
    TEN_LOAI_GIA_THANH = fields.Char(string='Tên loại giá thành', help='Tên loại giá thành', compute='_compute_loai_gia_thanh', store=True)
    DO_DANG_DAU_KY = fields.Float(string='Dở dang đầu kỳ', help='Dở dang đầu kỳ',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_TRONG_KY = fields.Float(string='Phát sinh trong kỳ', help='Phát sinh trong kỳ',digits=decimal_precision.get_precision('VND'))
    KHOAN_GIAM_GIA_THANH = fields.Float(string='Khoản giảm giá thành', help='Khoản giảm giá thành',digits=decimal_precision.get_precision('VND'))
    DO_DANG_CUOI_KY = fields.Float(string='Dở dang cuối kỳ', help='Dở dang cuối kỳ',digits=decimal_precision.get_precision('VND'))
    TONG_GIA_THANH = fields.Float(string='Tổng giá thành', help='Tổng giá thành',digits=decimal_precision.get_precision('VND'))
    LUY_KE_PHAT_SINH_KY_TRUOC = fields.Float(string='Lũy kế phát sinh kỳ trước', help='Lũy kế phát sinh kỳ trước',digits=decimal_precision.get_precision('VND'))
    LUY_KE_CHI_PHI = fields.Float(string='Lũy kế chi phí', help='Lũy kế chi phí',digits=decimal_precision.get_precision('VND'))
    LUY_KE_DA_NGHIEM_THU = fields.Float(string='Lũy kế đã nghiệm thu', help='Lũy kế đã nghiệm thu',digits=decimal_precision.get_precision('VND'))
    SO_CHUA_NGHIEM_THU = fields.Float(string='Số chưa nghiệm thu', help='Số chưa nghiệm thu',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name' , related ='TEN', oldname='NAME')

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET_IDS = fields.One2many('gia.thanh.ky.tinh.gia.thanh.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='kỳ tính giá thành chi tiết')

    GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS = fields.One2many('gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung', 'KY_TINH_GIA_THANH_ID', string='chi tiết chứng từ phân bổ chi phí chung')

    # Các bảng chi tiết là con của kỳ tính giá thành
    GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS = fields.One2many('gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='xác định chi phí phân bổ chi tiết')
    GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS = fields.One2many('gia.thanh.bang.gia.thanh.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='Bảng giá thành chi tiết')
    GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS = fields.One2many('gia.thanh.xac.dinh.do.dang.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='Xác định dở dang chi tiết')
    GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS = fields.One2many('gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='Kết quả chi phí dở dang cuối kỳ chi tiết')
    GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS = fields.One2many('gia.thanh.ket.qua.phan.bo.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='Kết quả phân bổ chi tiết')
    GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS = fields.One2many('gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='Xác định tỷ lệ phân bổ đối tượng tính giá thành chi tiết')
    GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS = fields.One2many('gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet', 'KY_TINH_GIA_THANH_ID', string='Tỷ lệ phân bổ đối tượng THCP chi tiết')
    
    @api.multi
    @api.depends('LOAI_GIA_THANH')
    def _compute_loai_gia_thanh(self):
        for record in self:
            if record.LOAI_GIA_THANH == 'DON_GIAN':
                record.TEN_LOAI_GIA_THANH = 'PP Giản đơn'
            elif record.LOAI_GIA_THANH == 'HE_SO_TY_LE':
                record.TEN_LOAI_GIA_THANH = 'PP Hệ số/Tỷ lệ'
            elif record.LOAI_GIA_THANH == 'CONG_TRINH':
                record.TEN_LOAI_GIA_THANH = 'Công trình'
            elif record.LOAI_GIA_THANH == 'DON_HANG':
                record.TEN_LOAI_GIA_THANH = 'Đơn hàng'
            elif record.LOAI_GIA_THANH == 'HOP_DONG':
                record.TEN_LOAI_GIA_THANH = 'Hợp đồng'
            elif record.LOAI_GIA_THANH == 'PHAN_BUOC':
                record.TEN_LOAI_GIA_THANH = 'Phân bước'
    
    @api.model
    def default_get(self, fields):
        rec = super(GIA_THANH_KY_TINH_GIA_THANH, self).default_get(fields)
        return rec

    @api.onchange('KY')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY, 'TU_NGAY', 'DEN_NGAY')
    
    @api.onchange('TU_NGAY','DEN_NGAY')
    def _onchange_tu_ngay_va_den_ngay(self):
        self.TEN = 'Kỳ tính giá thành từ ngày ' + datetime.strptime(self.TU_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y') + ' đến ngày ' + datetime.strptime(self.DEN_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y')

    def kiem_tra_ton_tai_ket_chuyen(self,args):
        id_ky_tinh_gia_thanh = args.get('id_ky_tinh_gia_thanh')
        ket_chuyen  = self.env['gia.thanh.ket.chuyen.chi.phi'].search([('KY_TINH_GIA_THANH_ID', '=', id_ky_tinh_gia_thanh)],limit=1)
        id_kc =  0
        if ket_chuyen:
            id_kc = ket_chuyen.id
        return id_kc

    def kiem_tra_ton_tai_nghiem_thu(self,args):
        id_ky_tinh_gia_thanh = args.get('id_ky_tinh_gia_thanh')
        ket_chuyen  = self.env['gia.thanh.nghiem.thu'].search([('KY_TINH_GIA_THANH_ID', '=', id_ky_tinh_gia_thanh)],limit=1)
        id_nt =  0
        if ket_chuyen:
            id_nt = ket_chuyen.id
        return id_nt
    

        


    