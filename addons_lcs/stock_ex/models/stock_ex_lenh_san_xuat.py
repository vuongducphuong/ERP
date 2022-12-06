# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class STOCK_EX_LENH_SAN_XUAT(models.Model):
    _name = 'stock.ex.lenh.san.xuat'
    _description = 'Lệnh sản xuất'
    _inherit = ['mail.thread']
    _order = "NGAY desc, SO_LENH desc"

    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    SO_LENH = fields.Char(string='Số lệnh', help='Số lệnh', auto_num='stock_ex_lenh_san_xuat_SO_LENH')
    TINH_TRANG = fields.Selection([('0', 'Chưa thực hiện'), ('1', ' Đang thực hiện'), ('2', ' Tạm dừng'), ('3', ' Hoàn thành'), ('4', ' Đã hủy bỏ '), ], string='Tình trạng', help='Tình trạng',default="1",required="True")
    name = fields.Char(string='Name', help='Name',related="SO_LENH",store=True, oldname='NAME')
    DA_LAP_DU_PN = fields.Boolean(string='Đã lập đủ phiếu nhập', help='Đã lập đủ phiếu nhập')
    DA_LAP_DU_PX = fields.Boolean(string='Đã lập đủ phiếu xuất', help='Đã lập đủ phiếu xuất')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')

    STOCK_EX_LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_IDS = fields.One2many('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham', 'LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID', string='Lệnh sản xuất chi tiết thành phẩm', copy=True)
    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    _sql_constraints = [
	('SO_LENH_uniq', 'unique ("SO_LENH")', 'Số lệnh <<>> đã tồn tại, vui lòng nhập số lệnh khác!'),
	]


    @api.model
    def default_get(self, fields):
        rec = super(STOCK_EX_LENH_SAN_XUAT, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 2040
        return rec

    @api.multi
    def btn_LSX_PN(self):
        id_lenh_san_xuat = self.id
        action = self.env.ref('stock_ex.open_stock_ex_lenh_san_xuat_lap_pn_form_tham_so_form').read()[0]
        context ={
            'default_ID_LENH_SAN_XUAT': id_lenh_san_xuat,
            'default_LENH_SX_PN_PX': 'PHIEU_NHAP'
         }
        action['context'] = helper.Obj.merge(context, action.get('context'))
        return action
    
    @api.multi
    def btn_LSX_PX(self):
        id_lenh_san_xuat = self.id
        action = self.env.ref('stock_ex.open_stock_ex_lenh_san_xuat_lap_px_form_tham_so_form').read()[0]
        context ={
            'default_ID_LENH_SAN_XUAT': id_lenh_san_xuat,
            'default_LENH_SX_PN_PX': 'PHIEU_XUAT'
         }
        action['context'] = helper.Obj.merge(context, action.get('context'))
        return action




    # @api.depends('STOCK_EX_LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_IDS.MA_HANG_ID')
    # def thay_doi_thanh_pham(self):
    #     # env = self.env['stock.ex.lenh.san.xuat.chi.tiet.dinh.muc.xuat.thanh.pham']
    #     self.STOCK_EX_LENH_SAN_XUAT_CHI_TIET_DINH_MUC_XUAT_THANH_PHAM_IDS = []
    #     # sl = self.SO_LUONG
    #     for thanh_pham in self.STOCK_EX_LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_IDS.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
    #         new_line = self.env['stock.ex.lenh.san.xuat.chi.tiet.dinh.muc.xuat.thanh.pham'].new({
    #             'MA_NGUYEN_VAT_LIEU_ID': thanh_pham.MA_NGUYEN_VAT_LIEU_ID,
    #             'TEN_NGUYEN_VAT_LIEU': thanh_pham.TEN_NGUYEN_VAT_LIEU,  
    #             'SO_LUONG_NVL' :thanh_pham.SO_LUONG,  
    #             'DVT_ID' : thanh_pham.DVT_ID,
    #             'SO_LUONG_NVL_TREN_SP' :thanh_pham.SO_LUONG, 
    #         })
    #         self.STOCK_EX_LENH_SAN_XUAT_CHI_TIET_DINH_MUC_XUAT_THANH_PHAM_IDS += new_line