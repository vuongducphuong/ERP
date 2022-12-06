# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI(models.Model):
    _name = 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi'
    _description = 'Phân bổ chi phí BH QLDN chi phí khác cho đơn vị'
    _inherit = ['mail.thread']
    KY_PHAN_BO = fields.Char(string='Kỳ phân bổ', help='Kỳ phân bổ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi_SO_CHUNG_TU')

    TONG_HOP_PHAN_BO_CHI_PHI_BH_QLDN_CHI_TIET_PHAN_BO_IDS = fields.One2many('tong.hop.phan.bo.chi.phi.bh.qldn.chi.tiet.phan.bo', 'PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID', string='phân bổ chi phí BH QLDN chi tiết phân bổ')
    TONG_HOP_PHAN_BO_CHI_PHI_BH_QLDN_CHI_TIET_CHI_PHI_IDS = fields.One2many('tong.hop.phan.bo.chi.phi.bh.qldn.chi.tiet.chi.phi', 'PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID', string='phân bổ chi phí BH QLDN chi tiết chi phí')
    name = fields.Char(string='name', help='name',related='SO_CHUNG_TU',store=True)
    TIEU_THUC_PHAN_BO_ALL = fields.Selection([('1', 'Doanh thu'), ('2', ' Nguyên vật liệu trực tiếp '), ('3', 'Nhân công trực tiếp'), ('4', ' Chi phí trực tiếp '), ], string='Tiêu thức phân bổ', help='Tiêu thức phân bổ')
    PHAN_BO_SELECTION_LAY_DU_LIEU = fields.Selection([('PHAN_BO_CHO_DON_VI', 'Phân bổ cho đơn vị'), ('PHAN_BO_CHO_CONG_TRINH_DON_HANG_HOP_DONG', ' phân bổ cho công trình đơn hàng hợp đồng'), ])
    CHON_CHUNG_TU_JSON = fields.Text(store=False)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI, self).default_get(fields)
        phan_bo_selection= self.get_context('default_PHAN_BO')
        tu_ngay= self.get_context('default_TU_NGAY')
        den_ngay= self.get_context('default_DEN_NGAY')
        if phan_bo_selection:
            rec['PHAN_BO_SELECTION_LAY_DU_LIEU'] =  phan_bo_selection
        if tu_ngay and den_ngay:
            tu_nam,tu_thang,tu_ngay = tu_ngay.split('-')
            den_nam,den_thang,den_ngay = den_ngay.split('-')
            rec['KY_PHAN_BO'] = 'Từ ngày %s/%s/%s đến ngày %s/%s/%s' % (tu_ngay,tu_thang,tu_nam,den_ngay,den_thang,den_nam)
        rec['DIEN_GIAI'] = 'Phân bổ chi phí BH, QLDN, chi phí khác cho đơn vị'

        return rec