# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_HE_THONG_TAI_KHOAN(models.Model):
    _name = 'danh.muc.he.thong.tai.khoan'
    _description = 'Hệ thống tài khoản'
    _parent_store = True
    _inherit = ['mail.thread']
    _order = 'name' 


    name = fields.Char(string='Name',help='Name')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản (*)', help='Số tài khoản',related='name',store=True , required=True)
    TEN_TAI_KHOAN = fields.Text(string='Tên tài khoản (*)', help='Tên tài khoản', required=True)
    TEN_TIENG_ANH = fields.Text(string='Tên tiếng anh', help='Tên tiếng anh')
    parent_id = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK tổng hợp', help='Tài khoản tổng hợp')
    TINH_CHAT = fields.Selection([('0', 'Dư Nợ'), ('1', 'Dư Có'), ('2', 'Lưỡng tính'), ('3', 'Không có số dư'), ], string='Tính chất', help='Tính chất',default='0')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    CO_HACH_TOAN_NGOAI_TE = fields.Boolean(string='Có hạch toán ngoại tệ', help='Có hạch toán ngoại tệ')
    
    DOI_TUONG = fields.Boolean(string=' ', help='Đối tượng')
    TAI_KHOAN_NGAN_HANG = fields.Boolean(string=' ', help='Tài khoản ngân hàng')
    DOI_TUONG_THCP = fields.Boolean( string=' ', help='Đối tượng tổng hợp chi phí')
    CONG_TRINH = fields.Boolean( string=' ', help='Công trình')
    DON_DAT_HANG = fields.Boolean( string=' ', help='Đơn đặt hàng')
    HOP_DONG_BAN = fields.Boolean( string=' ', help='Hợp đồng bán')
    HOP_DONG_MUA = fields.Boolean( string=' ', help='Hợp đồng mua')
    KHOAN_MUC_CP = fields.Boolean( string=' ', help='Khoản mục chi phí')
    DON_VI = fields.Boolean( string=' ', help='Đơn vị')
    MA_THONG_KE = fields.Boolean( string=' ', help='Mã thống kê')

    DOI_TUONG_SELECTION = fields.Selection([('0', 'Nhà cung cấp'), ('1', 'Khách hàng'), ('2', 'Nhân viên '), ], string='Đối tượng', help='Đối tượng')
    TAI_KHOAN_NH_SELECTION = fields.Selection([], string='TK ngân hàng', help='Tài khoản ngân hàng', store=False)
    DOI_TUONG_THCP_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Đối tượng THCP', help='Đối tượng tổng hợp chi phí')
    CONG_TRINH_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Công trình', help='Công trình')
    DON_DAT_HANG_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Hợp đồng bán', help='Hợp đồng bán')
    HOP_DONG_MUA_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Hợp đồng mua', help='Hợp đồng mua')
    KHOAN_MUC_CP_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Khoản mục CP', help='Khoản mục chi phí')
    DON_VI_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Đơn vị', help='Đơn vị')
    MA_THONG_KE_SELECTION = fields.Selection([('0', 'Chỉ cảnh báo'), ('1', ' Bắt buộc nhập'), ], string='Mã thống kê', help='Mã thống kê')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    BAC = fields.Integer(string='Bậc', help='Bậc')
    LA_TK_TONG_HOP = fields.Boolean(string='Là tài khoản tổng hợp', compute='_compute_LA_TK_TONG_HOP', store=True)
    child_ids = fields.One2many('danh.muc.he.thong.tai.khoan', 'parent_id', 'Chứa', copy=True)
    MA_PHAN_CAP = fields.Char(help='Mã phân cấp')
    CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG = fields.Boolean(string='Chi tiết theo tài khoản ngân hàng', help='Chi tiết theo tài khoản ngân hàng', compute='_compute_chi_tiet_theo_tknh', store=True)
    # trường CHI_TIET_THEO_DOI_TUONG là trường cũ nhưng đã dùng ở nhiều chỗ nên để compute để để đồng bộ 2 trường
    CHI_TIET_THEO_DOI_TUONG = fields.Boolean(string='CHi tiết theo đối tượng', help='CHi tiết theo đối tượng', compute='_compute_chi_tiet_theo_doi_tuong', store=True)

    _sql_constraints = [
	('SO_TAI_KHOAN_uniq', 'unique ("SO_TAI_KHOAN")', 'Số tài khoản <<>> đã tồn tại!'),
	]

    @api.depends('DOI_TUONG')
    def _compute_chi_tiet_theo_doi_tuong(self):
        for record in self:
            if record.DOI_TUONG:
                record.CHI_TIET_THEO_DOI_TUONG = record.DOI_TUONG
    
    @api.depends('TAI_KHOAN_NGAN_HANG')
    def _compute_chi_tiet_theo_tknh(self):
        for record in self:
            if record.TAI_KHOAN_NGAN_HANG:
                record.CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG
    
    @api.onchange('DOI_TUONG','DOI_TUONG_THCP','CONG_TRINH','DON_DAT_HANG','HOP_DONG_BAN','HOP_DONG_MUA','KHOAN_MUC_CP','DON_VI','MA_THONG_KE')
    def update_doi_tuong_selection(self):
        if self.DOI_TUONG == False:
            self.DOI_TUONG_SELECTION = None
        elif self.DOI_TUONG_THCP == False:
            self.DOI_TUONG_THCP_SELECTION  = None
        elif self.CONG_TRINH == False:
            self.CONG_TRINH_SELECTION  = None
        elif self.DON_DAT_HANG == False:
            self.DON_DAT_HANG_SELECTION  = None
        elif self.HOP_DONG_BAN == False:
            self.HOP_DONG_BAN_SELECTION  = None
        elif self.HOP_DONG_MUA == False:
            self.HOP_DONG_MUA_SELECTION  = None
        elif self.KHOAN_MUC_CP == False:
            self.KHOAN_MUC_CP_SELECTION  = None
        elif self.DON_VI == False:
            self.DON_VI_SELECTION  = None
        elif self.MA_THONG_KE == False:
            self.MA_THONG_KE_SELECTION  = None


    @api.depends('child_ids')
    def _compute_LA_TK_TONG_HOP(self):
        for record in self:
            record.LA_TK_TONG_HOP = True if record.child_ids else False

    @api.model
    def name_search_extend(self, name='', args=None, operator='ilike', limit=100, fields=[], record={}, extends=None):
        # Chỉ lọc các tài khoản không là tài khoản tổng hợp
        if not self._context.get('show_all'):
            args += [('LA_TK_TONG_HOP', '=', False)]
        if self.env.user.HAN_CHE_TAI_KHOAN_KHI_NHAP_CHUNG_TU and extends and extends.get('loaiChungTu'):
            loai_chung_tu = extends.get('loaiChungTu').get('LOAI_CHUNG_TU')
            nhom_chung_tu = extends.get('loaiChungTu').get('NHOM_CHUNG_TU', 0)
            ten_cot_chuyen_doi = extends.get('loaiChungTu').get('TEN_COT_CHUYEN_DOI')
            tk_nd = self.env['danh.muc.tai.khoan.ngam.dinh.chi.tiet'].search([('LOAI_CHUNG_TU', '=', loai_chung_tu),('NHOM_CHUNG_TU', '=', nhom_chung_tu),('TEN_COT_CHUYEN_DOI', '=', ten_cot_chuyen_doi)],limit=1)
            if tk_nd:
                tk_ids = []
                for ltk in tk_nd.LOC_TAI_KHOAN:
                    domains = self.get_name_search_args(name, args, operator, fields)
                    domains += [('MA_PHAN_CAP', '=ilike', ltk.MA_PHAN_CAP + '%'),('LA_TK_TONG_HOP', '=', False)]
                    tk_ids += self.env['danh.muc.he.thong.tai.khoan'].search(domains).ids
                # if tk_ids:
                return {
                    'total_count': len(tk_ids),
                    'records': self.browse(tk_ids).name_get_extend(fields),
                }
        return super(DANH_MUC_HE_THONG_TAI_KHOAN, self).name_search_extend(name, args, operator, limit, fields, record, extends)
