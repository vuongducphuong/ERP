# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import timedelta, datetime
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError
import json
from odoo.tools.float_utils import float_round

class ASSET_TAI_SAN_CO_DINH_GHI_TANG(models.Model):
    _name = 'asset.ghi.tang'
    _description = 'Ghi tăng tài sản cố định'
    _inherit = ['mail.thread']
    _order = "NGAY_GHI_TANG desc, MA_TAI_SAN"

    # _sql_constraints = [
	# ('SO_CT_GHI_TANG_uniq', 'unique ("SO_CT_GHI_TANG")', 'Số chứng từ ghi tăng đã tồn tại!'),
	# ]

    SO_CT_GHI_TANG = fields.Char(string='Số CT ghi tăng', help='Số chứng từ ghi tăng', auto_num='asset_ghi_tang_SO_CT_GHI_TANG')
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng', help='Ngày ghi tăng',default=fields.Datetime.now)
    MA_TAI_SAN = fields.Char(string='Mã tài sản', help='Mã tài sản')

    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản')
    NHA_SAN_XUAT = fields.Char(string='Nhà sản xuất', help='Nhà sản xuất')
    NAM_SAN_XUAT = fields.Integer(string='Năm sản xuất', help='Năm sản xuất')
    SO_HIEU = fields.Char(string='Số hiệu', help='Số hiệu')
    name = fields.Char(string='name', help='name',related='MA_TAI_SAN',store=True)
    NUOC_SAN_XUAT = fields.Char(string='Nước sản xuất', help='Nước sản xuất')
    LOAI_TAI_SAN_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại tài sản', help='Loại tài sản')
    CONG_SUAT = fields.Char(string='Công suất', help='Công suất')
    THOI_GIAN_BAO_HANH = fields.Char(string='Thời gian bảo hành', help='Thời gian bảo hành')
    DIEU_KIEN_BAO_HANH = fields.Text(string='Điều kiện bảo hành', help='Điều kiện bảo hành')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TEN_NCC = fields.Char(string='Tên ncc', help='Tên nhà cung cấp')
    BB_GIAO_NHAN_SO = fields.Char(string='Bb giao nhận số', help='Biên bản giao nhận số')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    TINH_TRANG_GHI_TANG = fields.Selection([('0', 'Mới'), ('1', 'Cũ'), ], string='Tình trạng ghi tăng', help='Tình trạng ghi tăng',default='0',required=True)
    CHAT_LUONG_HIEN_THOI = fields.Selection([('0', 'Hoạt động tốt'), ('1', 'Hỏng'), ], string='Chất lượng hiện thời', help='Chất lượng hiện thời',default='0',required=True)
    KHONG_TINH_KHAU_HAO = fields.Boolean(string='Không tính khấu hao', help='Không tính khấu hao')
    DINH_KEM = fields.Char(string='Đính kèm', help='Đính kèm')
    TK_NGUYEN_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nguyên giá', help='Tk nguyên giá')
    TK_KHAU_HAO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk khấu hao', help='Tk khấu hao')
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá',digits=decimal_precision.get_precision('VND'))
    TY_LE_TINH_KHAU_HAO_THANG = fields.Float(string='Tỷ lệ tính khấu hao tháng', help='Tỷ lệ tính khấu hao tháng')
    GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Giá trị tính khấu hao', help='Giá trị tính khấu hao',digits=decimal_precision.get_precision('VND'))
    TY_LE_TINH_KHAU_HAO_NAM = fields.Float(string='Tỷ lệ tính khấu hao năm', help='Tỷ lệ tính khấu hao năm')
    NGAY_BAT_DAU_TINH_KH = fields.Date(string='Ngày bắt đầu tính kh', help='Ngày bắt đầu tính khấu hao',default=fields.Datetime.now)
    GIA_TRI_TINH_KHAU_HAO_THANG = fields.Float(string='Giá trị tính khấu hao tháng', help='Giá trị tính khấu hao tháng',digits=decimal_precision.get_precision('VND'))
    THOI_GIAN_SU_DUNG = fields.Selection([('1', 'Năm'), ('0', 'Tháng'), ], string='Thời gian sử dụng', help='Thời gian sử dụng',default='1',required=True)
    SO_THOI_GIAN_SU_DUNG = fields.Float(string='Số thời gian sử dụng', help='Số thời gian sử dụng', compute='_compute_tinh_thoi_gian_su_dung', store=True)
    SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC = fields.Float(string='Số thời gian sử dụng', help='Số thời gian sử dụng', digits=decimal_precision.get_precision('VND'))
    GIA_TRI_KHAU_HAO_NAM = fields.Float(string='Giá trị khấu hao năm', help='Giá trị khấu hao năm',digits=decimal_precision.get_precision('VND'))
    HAO_MON_LUY_KE = fields.Float(string='Hao mòn lũy kế', help='Hao mòn lũy kế',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại',digits=decimal_precision.get_precision('VND'))
    GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN = fields.Boolean(string='Gh giá trị tính kh theo  luật thuế tndn', help='Giới hạn giá trị tính khấu hao theo luật thuế thu nhập doanh nghiệp')
    GIA_TRI_TINH_KH_THEO_LUAT = fields.Float(string='Giá trị tính kh theo luật', help='Giá trị tính khấu hao theo luật',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_KH_THANG_THEO_LUAT = fields.Float(string='Giá trị kh tháng theo luật', help='Giá trị khấu hao tháng theo luật',digits= decimal_precision.get_precision('VND'))
    NGUON_GOC_HINH_THANH = fields.Selection([('MUA_MOI', 'Mua mới'), ('XUAT_KHO', 'Xuất kho sử dụng'), ('DAU_TU_XAY_DUNG', 'Đầu tư xây dựng cơ bản hoàn thành'), ('NHAN_GOP_VON', 'Nhận góp vốn, tài trợ, biếu tặng'), ('THUE_TAI_CHINH', 'Thuê tài chính'), ('PHAT_HIEN_THUA', 'Phát hiện thừa khi kiểm kê'), ], string='Nguồn gốc hình thành', help='Nguồn gốc hình thành')
    SO_TSCD_ID = fields.Many2one('so.tscd', ondelete='set null')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    DA_TAP_HOP_DU_CHUNG_TU = fields.Boolean(string='Đã tập hợp đủ chứng từ', help='Đã tập hợp đủ chứng từ')
    DVT_THOI_GIAN_SU_DUNG_CON_LAI = fields.Selection([('1', 'Năm'), ('0', 'Tháng'), ], string='Thời gian sử dụng', help='Thời gian sử dụng',default='1',required=True)
    THOI_GIAN_SU_DUNG_CON_LAI = fields.Float(string='Số thời gian sử dụng còn lại', help='Số thời gian sử dụng còn lại', compute='_compute_tinh_thoi_gian_su_dung_con_lai', store=True)
    THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC = fields.Float(string='Số thời gian sử dụng còn lại nguyên gốc', help='Số thời gian sử dụng còn lại nguyên gốc')
    KHAI_BAO_DAU_KY = fields.Boolean(string='Khai báo đầu kỳ', help='Khai báo đầu kỳ', default=False)
    STT_CHUNG_TU = fields.Char(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ', auto_num='asset_STT_CHUNG_TU') 
    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',default = 250)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    ASSET_TAI_SAN_CO_DINH_NGUON_GOC_HINH_THANH_IDS = fields.One2many('asset.ghi.tang.nguon.goc.hinh.thanh', 'TAI_SAN_CO_DINH_GHI_TANG_ID', string='Tài sản cố định nguồn gốc hình thành')
    ASSET_TAI_SAN_CO_DINH_BO_PHAN_CAU_THANH_IDS = fields.One2many('asset.ghi.tang.bo.phan.cau.thanh', 'TAI_SAN_CO_DINH_GHI_TANG_ID', string='Tài sản cố định bộ phận cấu thành')
    ASSET_TAI_SAN_CO_DINH_DUNG_CU_PHU_TUNG_IDS = fields.One2many('asset.ghi.tang.dung.cu.phu.tung', 'TAI_SAN_CO_DINH_GHI_TANG_ID', string='Tài sản cố định dụng cụ phụ tùng')
    ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO_IDS = fields.One2many('asset.ghi.tang.thiet.lap.phan.bo', 'TAI_SAN_CO_DINH_GHI_TANG_ID', string='Tài sản cố định Thiết lập phân bổ')
    CHON_CHUNG_TU_JSON = fields.Text(store=False)
    THOI_GIAN_SU_DUNG_THANG_LIST = fields.Float(string='Thời gian sử dụng(Tháng)', help='Thời gian sử dụng(Tháng)')

    @api.depends('THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC','DVT_THOI_GIAN_SU_DUNG_CON_LAI')
    def _compute_tinh_thoi_gian_su_dung_con_lai(self):
        for record in self:
            if record.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '0':
                record.THOI_GIAN_SU_DUNG_CON_LAI = record.THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC
            elif record.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '1':
                record.THOI_GIAN_SU_DUNG_CON_LAI = record.THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC*12

    @api.depends('THOI_GIAN_SU_DUNG','SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC')
    def _compute_tinh_thoi_gian_su_dung(self):
        for record in self:
            if record.THOI_GIAN_SU_DUNG == '0':
                record.SO_THOI_GIAN_SU_DUNG = record.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC
            elif record.THOI_GIAN_SU_DUNG == '1':
                record.SO_THOI_GIAN_SU_DUNG = record.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC*12

    @api.onchange('NGAY_GHI_TANG','SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC','THOI_GIAN_SU_DUNG')
    def _onchange_NGAY_GHI_TANG(self):
        nam = self.env['ir.config_parameter'].get_param('he_thong.NAM_TAI_CHINH_BAT_DAU')
        ngay_bat_dau_nam_tai_chinh = datetime(year=int(nam), month=1, day=1)
        if self.NGAY_GHI_TANG:
            ngay_ghi_tang = datetime.strptime(self.NGAY_GHI_TANG, '%Y-%m-%d').date()
            thoi_gian_su_dung_con_lai_tinh_diff = self.diff_month(ngay_bat_dau_nam_tai_chinh,ngay_ghi_tang)
            if thoi_gian_su_dung_con_lai_tinh_diff < 0:
                thoi_gian_su_dung_con_lai = self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC
            else:
                if self.THOI_GIAN_SU_DUNG == '0':
                    thoi_gian_su_dung = self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC
                elif self.THOI_GIAN_SU_DUNG == '1':
                    thoi_gian_su_dung = self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC*12
                if thoi_gian_su_dung_con_lai_tinh_diff < thoi_gian_su_dung:
                    if self.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '0':
                        thoi_gian_su_dung_con_lai = thoi_gian_su_dung - thoi_gian_su_dung_con_lai_tinh_diff
                    elif self.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '1':
                        thoi_gian_su_dung_con_lai = (thoi_gian_su_dung - thoi_gian_su_dung_con_lai_tinh_diff)/12
                else:
                    thoi_gian_su_dung_con_lai = 0
            self.THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC = thoi_gian_su_dung_con_lai
            


    def diff_month(self,d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    @api.model
    def default_get(self, fields):
        rec = super(ASSET_TAI_SAN_CO_DINH_GHI_TANG, self).default_get(fields)
        rec['NAM_SAN_XUAT'] = datetime.now().year
        return rec

    @api.onchange('CHON_CHUNG_TU_JSON')
    def _onchange_CHON_CHUNG_TU_JSON(self):
        if self.CHON_CHUNG_TU_JSON:
            chon_chung_tu = json.loads(self.CHON_CHUNG_TU_JSON).get('ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS', [])
            self.ASSET_TAI_SAN_CO_DINH_NGUON_GOC_HINH_THANH_IDS = []
            for chung_tu in chon_chung_tu:
                self.ASSET_TAI_SAN_CO_DINH_NGUON_GOC_HINH_THANH_IDS += self.env['asset.ghi.tang.nguon.goc.hinh.thanh'].new(chung_tu)

    @api.onchange('DOI_TUONG_ID')
    def update_NHA_CUNG_CAP_ID(self):
        if self.DOI_TUONG_ID:
            self.TEN_NCC = self.DOI_TUONG_ID.HO_VA_TEN

    @api.onchange('NGUYEN_GIA')
    def update_NGUYEN_GIA(self):
        if self.NGUYEN_GIA:
            self.GIA_TRI_TINH_KHAU_HAO = self.NGUYEN_GIA
            
    @api.onchange('GIA_TRI_TINH_KHAU_HAO')
    def update_GIA_TRI_TINH_KHAU_HAO(self):
        if self.GIA_TRI_TINH_KHAU_HAO:
            if self.GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN == True:
                self.GIA_TRI_TINH_KH_THEO_LUAT = self.GIA_TRI_TINH_KHAU_HAO

    @api.onchange('TY_LE_TINH_KHAU_HAO_THANG')
    def update_TY_LE_TINH_KHAU_HAO_THANG(self):
        if self.TY_LE_TINH_KHAU_HAO_THANG:
            self.TY_LE_TINH_KHAU_HAO_NAM = self.TY_LE_TINH_KHAU_HAO_THANG*12
    
    @api.onchange('GIA_TRI_TINH_KHAU_HAO', 'TY_LE_TINH_KHAU_HAO_THANG')
    def update_GIA_TRI_KHAU_HAO(self):
        self.GIA_TRI_TINH_KHAU_HAO_THANG = (self.GIA_TRI_TINH_KHAU_HAO*self.TY_LE_TINH_KHAU_HAO_THANG)/100
        self.GIA_TRI_KHAU_HAO_NAM = (self.GIA_TRI_TINH_KHAU_HAO*self.TY_LE_TINH_KHAU_HAO_THANG*12)/100
            
    # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1893
    # @api.onchange('GIA_TRI_TINH_KHAU_HAO_THANG')
    # def update_GIA_TRI_TINH_KHAU_HAO_THANG(self):
    #     self.GIA_TRI_KHAU_HAO_NAM = self.GIA_TRI_TINH_KHAU_HAO_THANG*12
    
    @api.onchange('HAO_MON_LUY_KE','GIA_TRI_TINH_KHAU_HAO')
    def update_HAO_MON_LUY_KE(self):
        self.GIA_TRI_CON_LAI = self.GIA_TRI_TINH_KHAU_HAO - self.HAO_MON_LUY_KE
    
    @api.onchange('GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN')
    def update_GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN(self):
        if self.GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN == False:
            self.GIA_TRI_TINH_KH_THEO_LUAT = 0
        elif self.GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN == True:
            self.GIA_TRI_TINH_KH_THEO_LUAT = self.GIA_TRI_TINH_KHAU_HAO
    # @api.onchange('THOI_GIAN_SU_DUNG')
    # def update_THOI_GIAN_SU_DUNG(self):
    #     if self.THOI_GIAN_SU_DUNG:
    #         self.TY_LE_TINH_KHAU_HAO_THANG = 0
    #         self.TY_LE_TINH_KHAU_HAO_NAM = 0
    #         self.GIA_TRI_TINH_KHAU_HAO_THANG = 0
    #         self.GIA_TRI_KHAU_HAO_NAM = 0

    @api.onchange('LOAI_TAI_SAN_ID')
    def update_TK_nguyen_gia_TKKH(self):
        if self.LOAI_TAI_SAN_ID:
            self.TK_KHAU_HAO_ID = self.LOAI_TAI_SAN_ID.TK_KHAU_HAO_ID.id
            self.TK_NGUYEN_GIA_ID = self.LOAI_TAI_SAN_ID.TK_NGUYEN_GIA_ID.id
           
            



    @api.onchange('DON_VI_SU_DUNG_ID')
    def update_DON_VI_SU_DUNG_ID(self):
        if self.DON_VI_SU_DUNG_ID:
            env = self.env['asset.ghi.tang.thiet.lap.phan.bo']
            self.ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO_IDS = []
            tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', 'in', ('6422','6424'))],limit=1).id
            new_line = env.new({
                'DOI_TUONG_PHAN_BO_ID' : str(self.DON_VI_SU_DUNG_ID._name) + ',' + str(self.DON_VI_SU_DUNG_ID.id),
                'TEN_DOI_TUONG_PHAN_BO' : self.DON_VI_SU_DUNG_ID.TEN_DON_VI,
                'TY_LE_PB' : 100,
                'TK_NO_ID' : tai_khoan
            })
            self.ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO_IDS = new_line

    @api.onchange('THOI_GIAN_SU_DUNG','SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC')
    def _onchange_THOI_GIAN_SU_DUNG(self):
        if self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC > 0:
            if self.THOI_GIAN_SU_DUNG == '0':
                self.TY_LE_TINH_KHAU_HAO_THANG = (1/self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC)*100
            elif self.THOI_GIAN_SU_DUNG == '1':
                self.TY_LE_TINH_KHAU_HAO_THANG = (1/(self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC*12))*100
        else:
            self.TY_LE_TINH_KHAU_HAO_THANG = 0
            self.TY_LE_TINH_KHAU_HAO_NAM = 0
            self.GIA_TRI_TINH_KHAU_HAO_THANG = 0
            self.GIA_TRI_KHAU_HAO_NAM = 0

    
    # @api.onchange('SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC')
    # def _onchange_SO_THOI_GIAN_SU_DUNG(self):
    #     if self.THOI_GIAN_SU_DUNG == '1':
    #         self.THOI_GIAN_SU_DUNG_THANG_LIST = self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC *12
    #     else:
    #         self.THOI_GIAN_SU_DUNG_THANG_LIST = self.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC 
        

    
    @api.model
    def create(self, values):
        if not values.get('KHAI_BAO_DAU_KY'):
            self.validate_unique('SO_CT_GHI_TANG', values.get('SO_CT_GHI_TANG'))
        result = super(ASSET_TAI_SAN_CO_DINH_GHI_TANG, self).create(values)
        if result.KHAI_BAO_DAU_KY == True:
            result.action_ghi_so()
        return result

    @api.multi
    def write(self, values):
        self.validate_unique('SO_CT_GHI_TANG', values.get('SO_CT_GHI_TANG'), 'write')
        return super(ASSET_TAI_SAN_CO_DINH_GHI_TANG, self).write(values)
    
    @api.model
    def uivalidate(self, option=None):
        ngay_khoa_so = str(self.lay_ngay_khoa_so())
        ty_le_pb = 0
        for line in self.ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO_IDS:
            ty_le_pb += line.TY_LE_PB
        if ty_le_pb != 100:
            return "Tổng tỷ lệ phân bổ của từng tài sản cố định phải bằng 100%. Xin vui lòng kiển tra lại!"

        # if self.NGAY_GHI_TANG < ngay_khoa_so:
        #     return "Ngày ghi tăng không được nhỏ hơn ngày khóa sổ " +str(ngay_khoa_so)+ ". Vui lòng kiểm tra lại!"
    
    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_tscd()
        self.write({'state':'da_ghi_so'})

    def ghi_so_tscd(self):
        line_ids = []
        thu_tu = 0
        # data_ghi_no = {}
        # for line in self.ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO_IDS:
        data_ghi_no = helper.Obj.inject(self, self)
        data_ghi_no.update({
            'ID_CHUNG_TU': self.id,
            'MODEL_CHUNG_TU' : self._name,
            'TSCD_ID' : self.id,
            'NGAY_HACH_TOAN' : self.NGAY_GHI_TANG,
            'NGAY_CHUNG_TU' : self.NGAY_GHI_TANG,
            'THOI_GIAN_SU_DUNG' : self.SO_THOI_GIAN_SU_DUNG,
            'TY_LE_KHAU_HAO_THANG' : self.TY_LE_TINH_KHAU_HAO_THANG,
            'GIA_TRI_KHAU_HAO_THANG' : self.GIA_TRI_TINH_KHAU_HAO_THANG,
            'DON_VI_SU_DUNG' : self.DON_VI_SU_DUNG_ID.id,
            'LOAI_TSCD_ID' : self.LOAI_TAI_SAN_ID.id,
            'GIA_TRI_HAO_MON_LUY_KE' : self.HAO_MON_LUY_KE,
            'TK_HAO_MON_ID' : self.TK_KHAU_HAO_ID.id,
            'THOI_GIAN_SU_DUNG_CON_LAI' : self.THOI_GIAN_SU_DUNG_CON_LAI,
            'TEN_TSCD' : self.TEN_TAI_SAN,
            'SO_CHUNG_TU' : self.SO_CT_GHI_TANG,
            'THU_TU_TRONG_CHUNG_TU' : thu_tu,
        })
        line_ids = [(0,0,data_ghi_no)]
        thu_tu += 1
        # Tạo master
        stscd = self.env['so.tscd'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_TSCD_ID = stscd.id
        return True

    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()

    def lay_du_lieu_tren_so(self,ngay_hach_toan):
        du_lieu_tren_so = self.env['so.tscd.chi.tiet'].search([('TSCD_ID', '=', self.id),('NGAY_HACH_TOAN', '<', ngay_hach_toan)],limit=1, order="THU_TU_NGHIEP_VU desc, NGAY_HACH_TOAN desc")
        return du_lieu_tren_so

    def lay_du_lieu_tren_so_de_tinh_gtcl(self,ngay_hach_toan):
        du_lieu_tren_so = self.env['so.tscd.chi.tiet'].search([('TSCD_ID', '=', self.id),('NGAY_HACH_TOAN', '<', ngay_hach_toan),('LOAI_CHUNG_TU', 'in', (250,251,254,615,252))],limit=1, order="THU_TU_NGHIEP_VU desc, NGAY_HACH_TOAN desc")
        return du_lieu_tren_so

    def lay_du_lieu_ngay_tren_so(self,ngay_hach_toan):
        du_lieu_tren_so = self.env['so.tscd.chi.tiet'].search([('TSCD_ID', '=', self.id),('NGAY_HACH_TOAN', '<', ngay_hach_toan),('LOAI_CHUNG_TU', 'in', (250,251,254,615))],limit=1, order="THU_TU_NGHIEP_VU desc, NGAY_HACH_TOAN desc")
        return du_lieu_tren_so


    def lay_du_lieu_phan_bo(self,ngay):
        record = []
        params = {
            'TSCD_ID': self.id,
            'NGAY_HACH_TOAN' : ngay,
            }

        query = """   

            SELECT  FAL.*
        FROM so_tscd_chi_tiet AS FAL
        WHERE
        FAL."TSCD_ID" = %(TSCD_ID)s
--         AND FAL.BranchID = @BranchID
        AND FAL."NGAY_HACH_TOAN" <= %(NGAY_HACH_TOAN)s
        ORDER BY "NGAY_HACH_TOAN" DESC
        FETCH FIRST 1 ROW ONLY

        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'TSCD_ID': line.get('TSCD_ID', ''),
                'TEN_TSCD': line.get('TEN_TSCD', ''),
                'DON_VI_SU_DUNG_ID': line.get('DON_VI_SU_DUNG_ID', ''),
                'NGUYEN_GIA': line.get('NGUYEN_GIA', ''),
                'GIA_TRI_TINH_KHAU_HAO': line.get('GIA_TRI_TINH_KHAU_HAO', ''),
                'GIA_TRI_HAO_MON_LUY_KE': line.get('GIA_TRI_HAO_MON_LUY_KE', ''),
                'GIA_TRI_CON_LAI': line.get('GIA_TRI_CON_LAI', ''),
                'TK_NGUYEN_GIA_ID': line.get('TK_NGUYEN_GIA_ID', ''),
                'TK_HAO_MON_ID': line.get('TK_HAO_MON_ID', ''),   
                'THOI_GIAN_SU_DUNG_CON_LAI' : line.get('THOI_GIAN_SU_DUNG_CON_LAI', ''),   
            })
        
        return record


    

    def tinh_gia_tri_con_lai(self,ngay):
        record = []
        params = {
            'TSCD_ID': self.id,
            'NGAY_HACH_TOAN' : ngay,
            }

        query = """   

        DO LANGUAGE plpgsql $$
        DECLARE
        ngay_hach_toan DATE := %(NGAY_HACH_TOAN)s;
        tscd_id INTEGER := %(TSCD_ID)s;

        BEGIN
        DROP TABLE IF EXISTS TMP_KET_QUA;
        CREATE TEMP TABLE TMP_KET_QUA
            AS
            SELECT kq."GIA_TRI_CUA_TAI_SAN",
            kq."GIA_TRI_KHAU_HAO_LUY_KE",
            kq."GIA_TRI_CUA_TAI_SAN" - kq."GIA_TRI_KHAU_HAO_LUY_KE" AS "GIA_TRI_CON_LAI"
        FROM
        (
        SELECT
        -- Giá trị của tài sản
        (SELECT
                    -- giá trị khấu hao ban đầu của tài sản
                    coalesce((SELECT coalesce(gt."GIA_TRI_TINH_KHAU_HAO", 0)
                                FROM asset_ghi_tang gt
                                WHERE gt.id = tscd_id
                                ), 0)
                    -- Tổng chênh lệch giá trị khấu hao của các lần đánh giá lại
                + coalesce((SELECT SUM(dglct."CHENH_LECH_GTKH")
                            FROM asset_danh_gia_lai_chi_tiet_dieu_chinh dglct
                                INNER JOIN asset_danh_gia_lai dgl
                                ON dglct."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID" = dgl.id
                            WHERE dglct."MA_TAI_SAN_ID" = tscd_id
                                    AND dgl."NGAY_HACH_TOAN" <= ngay_hach_toan
                            ), 0))
        AS "GIA_TRI_CUA_TAI_SAN",
        -- Khấu hao lũy kế
        (
            -- Tổng các lần tính khấu hao
            (SELECT coalesce(SUM(khct."GIA_TRI_KH_THANG"), 0)
                FROM asset_tinh_khau_hao_chi_tiet khct
                INNER JOIN asset_tinh_khau_hao kh ON khct."TINH_KHAU_HAO_ID" = kh.id
                WHERE khct."MA_TAI_SAN_ID" = tscd_id
                    AND kh."NGAY_HACH_TOAN" < ngay_hach_toan)
            +
            -- Hao mòn lũy kế lúc ghi tăng
            (SELECT coalesce(gt."HAO_MON_LUY_KE", 0)
            FROM asset_ghi_tang gt
            WHERE gt.id = tscd_id)
            +
            -- tổng chênh lệch hao mòn lũy kế khi đánh giá lại
            coalesce((SELECT coalesce(SUM(dglct."CHENH_LECH_HAO_MON_LUY_KE"), 0)
                        FROM asset_danh_gia_lai_chi_tiet_dieu_chinh dglct
                            INNER JOIN asset_danh_gia_lai dgl ON dglct."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID" = dgl.id
                        WHERE dglct."MA_TAI_SAN_ID" = tscd_id
                                AND dgl."NGAY_HACH_TOAN" <= ngay_hach_toan
                        ), 0)
        )
        AS "GIA_TRI_KHAU_HAO_LUY_KE"
        ) kq
        ;
        END $$;

        SELECT *
        FROM TMP_KET_QUA;

        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'GIA_TRI_CUA_TAI_SAN': line.get('GIA_TRI_CUA_TAI_SAN', ''),
                'GIA_TRI_KHAU_HAO_LUY_KE': line.get('GIA_TRI_KHAU_HAO_LUY_KE', ''),
                'GIA_TRI_CON_LAI': line.get('GIA_TRI_CON_LAI', ''),
            })
        
        return record

    @api.model_cr
    def init(self):
        ghi_tangs = self.env['asset.ghi.tang'].search([])
        if ghi_tangs:
            for ghi_tang in ghi_tangs:
                if ghi_tang.KHAI_BAO_DAU_KY == False:
                    ghi_tang.write({'DVT_THOI_GIAN_SU_DUNG_CON_LAI' : ghi_tang.THOI_GIAN_SU_DUNG})
                thoi_gian_su_dung_con_lai = 0
                thoi_gian_su_dung_con_lai_nguyen_goc = 0
                # Tính dif giữa ngày ghi tăng và ngày bắt đầu năm tài chính
                if ghi_tang.NGAY_GHI_TANG:
                    ngay_ghi_tang = datetime.strptime(ghi_tang.NGAY_GHI_TANG, '%Y-%m-%d').date()
                    nam = self.env['ir.config_parameter'].get_param('he_thong.NAM_TAI_CHINH_BAT_DAU')
                    ngay_bat_dau_nam_tai_chinh = datetime(year=int(nam), month=1, day=1)
                    thoi_gian_su_dung_con_lai_tinh_diff = self.diff_month(ngay_bat_dau_nam_tai_chinh,ngay_ghi_tang)
                    # Tính thời gian sử dụng còn lại và thời gian sử dụng còn lại nguyên gốc
                    if thoi_gian_su_dung_con_lai_tinh_diff < 0:
                        thoi_gian_su_dung_con_lai_nguyen_goc = ghi_tang.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC
                    else:
                        if ghi_tang.THOI_GIAN_SU_DUNG == '0':
                            thoi_gian_su_dung = ghi_tang.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC
                        elif ghi_tang.THOI_GIAN_SU_DUNG == '1':
                            thoi_gian_su_dung = ghi_tang.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC*12
                        if thoi_gian_su_dung_con_lai_tinh_diff < thoi_gian_su_dung:
                            if ghi_tang.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '0':
                                thoi_gian_su_dung_con_lai_nguyen_goc = thoi_gian_su_dung - thoi_gian_su_dung_con_lai_tinh_diff
                            elif ghi_tang.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '1':
                                thoi_gian_su_dung_con_lai_nguyen_goc = (thoi_gian_su_dung - thoi_gian_su_dung_con_lai_tinh_diff)/12
                        else:
                            thoi_gian_su_dung_con_lai_nguyen_goc = 0
                    if ghi_tang.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '0':
                        thoi_gian_su_dung_con_lai = thoi_gian_su_dung_con_lai_nguyen_goc
                    else:
                        thoi_gian_su_dung_con_lai = thoi_gian_su_dung_con_lai_nguyen_goc*12
                    ghi_tang.write({'THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC' : thoi_gian_su_dung_con_lai_nguyen_goc,
                                'THOI_GIAN_SU_DUNG_CON_LAI' : thoi_gian_su_dung_con_lai
                    })