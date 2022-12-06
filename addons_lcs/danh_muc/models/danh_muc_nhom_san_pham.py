# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_SAN_PHAM(models.Model):
    _inherit = "product.category"
    _description = 'Nhóm vật tư hàng hóa'
    TEN = fields.Char(string='Tên', help='Tên')
    THUOC_NHOM_ID = fields.Many2one('product.category', string='Thuộc nhóm', help='Thuộc nhóm', related='parent_id', store=True,  )
    FORE_REMOVAL_STRATEGY_ID = fields.Many2one('product.removal', string='Fore removal strategy', help='Fore removal strategy')
    PHUONG_PHAP_TINH_GIA = fields.Selection([('GIA_TIEU_CHUAN', 'Gía tiêu chuẩn'), ('VAO_TRUOC_RA_TRUOC_FIFO', 'Vào trước ra trước(FIFO)'), ('GIA_TRUNG_BINH_AVCO', 'Gía trung bình(AVCO)'), ], string='Phương pháp tính giá', help='Phương pháp tính giá',default='GIA_TIEU_CHUAN')
    TINH_GIA_TON_KHO = fields.Selection([('THU_CONG', 'Thủ công'), ('TU_DONG', 'Tự động'), ], string='Tính giá tồn kho', help='Tính giá tồn kho',default='THU_CONG')
    KHO_NGAM_DINH_ID = fields.Many2one('danh.muc.kho', string='Kho ngầm định', help='Kho ngầm định')
    TAI_KHOAN_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản kho', help='Tài khoản kho')
    TK_DOANH_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK doanh thu', help='TK doanh thu')
    TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='TK chiết khấu')
    TK_GIAM_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giảm giá', help='TK giảm giá')
    TK_TRA_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK trả lại', help='TK trả lại')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tk chi phí')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)

    @api.model
    def default_get(self,default_fields):
        res = super(DANH_MUC_NHOM_SAN_PHAM, self).default_get(default_fields)
        res['KHO_NGAM_DINH_ID'] = self.env['danh.muc.kho'].search([('MA_KHO', '=','KHH')],limit=1).id
        res['TK_DOANH_THU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=','5111')],limit=1).id
        res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=','632')],limit=1).id


        # res['KHO_NGAM_DINH_ID'] = self.env['danh.muc.kho'].search([('code', '=', 'KHH')])

        return res
