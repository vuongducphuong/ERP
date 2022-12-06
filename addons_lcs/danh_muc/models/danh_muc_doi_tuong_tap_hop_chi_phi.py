# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class DANH_MUC_DOI_TUONG_TONG_HOP_CHI_PHI(models.Model):
    _name = 'danh.muc.doi.tuong.tap.hop.chi.phi'
    _description = 'Danh mục đối tượng tập hợp chi phí'
    _parent_store = True
    _inherit = ['mail.thread']

    MA_DOI_TUONG_THCP = fields.Char(string='Mã (*)', help='Mã', required=True)#auto_num='danh_muc_doi_tuong_tong_hop_chi_phi_MA_DOI_TUONG_THCP')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên (*)', help='Tên',required=True)
    LOAI = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'), ], string='Loại (*)', help='Loại',default='0', required='True')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean( string='Theo dõi', help='Theo dõi', default=True)
    # CHI_NHANH = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh(), oldname='CHI_NHANH') 
    BAC = fields.Integer(string='Bậc', help='Bậc')


    CHON_THANH_PHAM = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Chọn thành phẩm(*)', help='Chọn thành phẩm')
    parent_id = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Thuộc quy trình (*)', help='Thuộc quy trình')
    CONG_DOAN_THU = fields.Integer(string='Công đoạn thứ(*)', help='Công đoạn thứ')
    isparent = fields.Boolean(string='là đối tượng tổng hợp', help='Tên nhãn', compute='_compute_LA_TONG_HOP', store=True)
    
    DANH_MUC_CHI_TIET_DOI_TUONG_TONG_HOP_CHI_PHI_IDS = fields.One2many('danh.muc.chi.tiet.doi.tuong.tong.hop.chi.phi', 'DOI_TUONG_TONG_HOP_CHI_PHI_ID', string='chi tiết đối tượng tổng hợp chi phí', copy=True)
    DANH_MUC_CHI_TIET_DOI_TUONG_TINH_GIA_THANH_IDS = fields.One2many('danh.muc.chi.tiet.doi.tuong.tinh.gia.thanh', 'DOI_TUONG_TONG_HOP_CHI_PHI_ID', string='chi tiết đối tượng tính giá thành', copy=True)

    name = fields.Char(string='Name', help='Name', related='MA_DOI_TUONG_THCP', store=True)

    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')
    THU_TU_THEO_MA_PHAN_CAP = fields.Char(string='Thứ tự mã phân cấp', help='Thứ tự mã phân cấp', oldname='THU_TU_MA_PHAN_CAP')

    DOI_TUONG_THCP_SELECTION = fields.Selection([('0', 'Tập hợp chi phí đến công đoạn'),('1', 'Tập hợp chi phí đến từng sản phẩm trong công đoạn'),],  default='0',string='Tập hợp chi phí cho công đoạn')
    child_ids = fields.One2many('danh.muc.doi.tuong.tap.hop.chi.phi', 'parent_id', 'Chứa', copy=True) 

    @api.depends('child_ids')
    def _compute_LA_TONG_HOP(self):
        for record in self:
            record.isparent = True if record.child_ids else False 

    _sql_constraints = [
        ('MA_DOI_TUONG_THCP_uniq', 'unique ("MA_DOI_TUONG_THCP")', 'Mã đối tượng THCP <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.onchange('CHON_THANH_PHAM')
    def _onchange_CHON_THANH_PHAM(self):
        if self.CHON_THANH_PHAM:
            self.MA_DOI_TUONG_THCP = self.CHON_THANH_PHAM.MA
            self.TEN_DOI_TUONG_THCP = self.CHON_THANH_PHAM.TEN

    # @api.model
    # def create(self, vals): 
    #     # if not vals.get('move_lines'):
    #        # raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     if (vals.get('TEN_DOI_TUONG_THCP')):
    #         vals['name'] = vals.get('TEN_DOI_TUONG_THCP')
    #     result = super(DANH_MUC_DOI_TUONG_TONG_HOP_CHI_PHI, self).create(vals)
    #     return result