# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision

class DANH_MUC_CONG_TRINH(models.Model):
    _name = 'danh.muc.cong.trinh'
    _description = 'Danh mục công trình'
    _parent_store = True
    _inherit = ['mail.thread']

    @api.depends('MA_PHAN_CAP','parent_id')
    def _compute_bac(self):
        for record in self:
            if record.MA_PHAN_CAP:
                record.BAC = len(record.MA_PHAN_CAP.split('/')) - 2

    # Cập nhật lại bậc
	# đã chuyển sang account_ex_phieu_thu_chi
    # @api.model_cr
    # def init(self):
        # for record in self.search([]):
            # record.write({'BAC': len(record.MA_PHAN_CAP.split('/')) - 2})

    MA_CONG_TRINH = fields.Char(string='Mã công trình (*)', help='Mã công trình',required=True)
    TEN_CONG_TRINH = fields.Char(string='Tên công trình (*)', help='Tên công trình',required=True)
    name = fields.Char(string='Name', help='Name',related='MA_CONG_TRINH', store=True, oldname='NAME')
    BAC = fields.Integer(string='Bậc', help='Bậc')
    LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình')
    TINH_TRANG = fields.Selection([('DANG_THUC_HIEN', 'Đang thực hiện'),('DA_HOAN_THANH', 'Đã hoàn thành'),], string='Tình trạng', help='Tình trạng',default='DANG_THUC_HIEN',required='True')
    NGAY_BAT_DAU = fields.Date(string='Ngày bắt đầu', help='Ngày bắt đầu')
    NGAY_KET_THUC = fields.Date(string='Ngày kết thúc', help='Ngày kết thúc')
    DU_TOAN = fields.Float(string ='Dự toán',help='Dự toán',digits= decimal_precision.get_precision('Product Price'))
    CHU_DAU_TU = fields.Char(string='Chủ đầu tư', help='Chủ đầu tư')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
   
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    CONG_TRINH_SELECTION = fields.Selection([('0', 'Công trình'),('1', 'Hạng mục công trình'),], string='Tính chất',default='0')
    LA_CHA = fields.Boolean(string='Là cha', help='Là cha')

    parent_id = fields.Many2one('danh.muc.cong.trinh', string='Thuộc công trình', help='Thuộc công trình', index=True, ondelete='restrict')
    isparent = fields.Boolean(string='là công trình tổng hợp', help='là công trình tổng hợp', compute='_compute_isparent', store=True)
    MA_PHAN_CAP = fields.Char(help='Mã phân cấp')
    THU_TU_THEO_MA_PHAN_CAP = fields.Char(string='Thứ tự theo mã phân cấp', help='Thứ tự theo mã phân cấp')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    child_ids = fields.One2many('danh.muc.cong.trinh', 'parent_id', 'Chứa', copy=True)

    _sql_constraints = [
        ('MA_CONG_TRINH_uniq', 'unique ("MA_CONG_TRINH")', 'Mã công trình <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]    

    @api.depends('child_ids')
    def _compute_isparent(self):
        for record in self:
            record.isparent = True if record.child_ids else False 

    # @api.model
    # def create(self, vals): 
    #     # if not vals.get('move_lines'):
    #        # raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     if (vals.get('TEN_CONG_TRINH')):
    #         vals['name'] = vals.get('TEN_CONG_TRINH')
    #     result = super(DANH_MUC_CONG_TRINH, self).create(vals)
    #     return result