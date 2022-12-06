# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.tools.float_utils import float_round

class PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA(models.Model):
    _name = 'purchase.ex.hoa.don.mua.hang'
    _description = 'Hóa đơn mua hàng'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIEN_GIAI = fields.Char(string='Diễn giải ', help='Diễn giải ')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',required=True,default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='purchase_ex_nhan_hoa_don_mua_hang_hoa_SO_CHUNG_TU')

    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', default=fields.Date.context_today)
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    # NAME = fields.Char(string='Name', help='Name',related='SO_HOA_DON')
    name = fields.Char(string='Name', help='Name',related='SO_HOA_DON',oldname='NAME')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    LOAI_CT_BI_DIEU_CHINH = fields.Char(string='Loại chứng từ bị điều chỉnh', help='Loại chứng từ bị điều chỉnh')
    TONG_TIEN_THUE_GTGT = fields.Float(string='Tổng tiền thuế gtgt', help='Tổng tiền thuế gtgt')
    TONG_TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='Tổng tiền thuế gtgt quy đổi', help='Tổng tiền thuế gtgt quy đổi')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ', store=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True)
    TONG_GIA_TRI_HHDV_CHUA_THUE = fields.Monetary(string='Giá trị HHDV chưa thuế', help='Giá trị hàng hóa dịch vụ chưa thuế',  currency_field='base_currency_id',compute='tinh_tong_tien',store=True)
    TONG_TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng',  currency_field='base_currency_id',compute='tinh_tong_tien',store=True)
    NHAN_HOA_DON = fields.Boolean(string='Nhận hóa đơn', help='Nhận hóa đơn',default=False)

    # _sql_constraints = [
	# ('SO_CHUNG_TU_NHD_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	# ]


    # Details
    HOA_DON_CHI_TIET_IDS = fields.One2many('purchase.ex.hoa.don.mua.hang.chi.tiet', 'HOA_DON_MUA_HANG_ID', string='Hóa đơn mua hàng hóa chi tiết', copy=True)
    PURCHASE_DOCUMENT_LINE_IDS = fields.One2many('purchase.document.line', 'HOA_DON_ID', string='Chứng từ mua hàng chi tiết', copy=True)  
    SOURCE_ID = fields.Reference(selection=[
        ('purchase.document', 'Chứng từ mua hàng'),
        ('purchase.ex.giam.gia.hang.mua', 'Chứng từ giảm giá hàng mua'),
        ], string='Lập từ')
    CHI_TIET_HANG_HOA = fields.Selection([
        ('hach_toan', 'Hạch toán'),
        ('thong_ke','Thống kê'),
        ], default='hach_toan', string='NO_SAVE')
    
    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.HOA_DON_CHI_TIET_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))

    @api.model
    def create(self, vals): 
        result = super(PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA, self).create(vals)
        if result.SO_CHUNG_TU:
            result.validate_unique_so_chung_tu()
        # update lại chứng từ mua hàng
        result.update_chung_tu_mua_hang()
        return result
    
    @api.multi
    def write(self, values):
        result = super(PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA, self).write(values)
        self.update_chung_tu_mua_hang()
        return result
    
    @api.multi
    def unlink(self):
        if self.HOA_DON_CHI_TIET_IDS:
            for chi_tiet in self.HOA_DON_CHI_TIET_IDS:
                if chi_tiet.ID_CHUNG_TU_GOC:
                    chi_tiet.ID_CHUNG_TU_GOC.write({'HOA_DON_MUA_HANG_ID': False})
        result = super(PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA, self).unlink()
        return result

    def update_chung_tu_mua_hang(self): 
        if self.HOA_DON_CHI_TIET_IDS:
            for chi_tiet in self.HOA_DON_CHI_TIET_IDS:
                if chi_tiet.ID_CHUNG_TU_GOC:
                    chi_tiet.ID_CHUNG_TU_GOC.write({'HOA_DON_MUA_HANG_ID': self.id})


    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU

    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 3400
        return rec

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False

    @api.depends('HOA_DON_CHI_TIET_IDS')
    def tinh_tong_tien(self):
        for record in self:
            tong_gia_tri_hhdv_chua_thue_qd = 0.0
            tong_tien_thue_gtgt_qd        = 0.0
            for chi_tiet in record.HOA_DON_CHI_TIET_IDS:
                tong_gia_tri_hhdv_chua_thue_qd += chi_tiet.GIA_TRI_HHDV_CHUA_THUE_QUY_DOI
                tong_tien_thue_gtgt_qd        += chi_tiet.TIEN_THUE_GTGT_QUY_DOI
            
            record.update({
                'TONG_GIA_TRI_HHDV_CHUA_THUE': tong_gia_tri_hhdv_chua_thue_qd,
                'TONG_TIEN_THUE_GTGT': tong_tien_thue_gtgt_qd,
            })






    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_cong_no()
            record.ghi_so_thue_tu_ghi()
        self.write({'state':'da_ghi_so'})

    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.HOA_DON_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                'TAI_KHOAN_ID' : line.TK_THUE_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'MA_HANG_ID' : line.MA_HANG_ID.id,
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'NHAN_VIEN_ID' : self.NHAN_VIEN_ID.id,
                'GHI_NO' : line.TIEN_THUE_GTGT_QUY_DOI,
                'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.TIEN_THUE_GTGT_QUY_DOI,
                'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True
    
    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.HOA_DON_CHI_TIET_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
            })

            if line.TK_THUE_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TK_ID': line.TK_THUE_ID.id,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.TIEN_THUE_GTGT,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'GHI_CO': 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                })
                line_ids += [(0,0,data_ghi_no)]
            if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_co = data_goc.copy()
                data_ghi_co.update({
                    'TK_ID': line.TK_CO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_THUE_ID.id,
                    'GHI_NO': 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO': line.TIEN_THUE_GTGT,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                })
                line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        scn = self.env['so.cong.no'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CONG_NO_ID = scn.id
        return True

    # @api.multi
    # def action_bo_ghi_so(self, args):
    #     return super(PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA, self).action_bo_ghi_so()


    def ghi_so_thue_tu_ghi(self):
        line_ids = []
        thu_tu = 0
        for line in self.HOA_DON_CHI_TIET_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                # 'TK_VAT_ID': line.TK_THUE_GTGT_ID.id if chung_tu_mua_hang.LOAI_CHUNG_TU_MH != 'nhap_khau_nhap_kho' else line.TK_DU_THUE_GTGT_ID.id,
                'TK_VAT_ID': line.TK_THUE_ID.id,
                'PHAN_TRAM_VAT': line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.PHAN_TRAM_THUE_GTGT_ID else None,
                'SO_TIEN_VAT': float_round(line.TIEN_THUE_GTGT_QUY_DOI,0),
                'SO_TIEN_VAT_NGUYEN_TE' : float_round(line.TIEN_THUE_GTGT,0),
                'SO_TIEN_CHIU_VAT': line.GIA_TRI_HHDV_CHUA_THUE_QUY_DOI,
                'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.GIA_TRI_HHDV_CHUA_THUE,
                'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO_ID.id,
                'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                'DIEN_GIAI' : line.TEN_HANG,
                'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                'SO_HOA_DON' : self.SO_HOA_DON, 
                'NGAY_CHUNG_TU' : self.NGAY_CHUNG_TU,
                'NGAY_HACH_TOAN' : self.NGAY_HACH_TOAN,
                'MAU_SO_HD_ID' : self.MAU_SO_HD_ID.id,
                'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                'ID_CHUNG_TU_GOC' : None,
                'MODEL_CHUNG_TU_GOC' : None,
                'TEN_DOI_TUONG' : self.TEN_NHA_CUNG_CAP,
                'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True


    def ghi_so_thue_qua_chung_tu_mua_hang(self):
        line_ids = []
        thu_tu = 0
        chung_tu_mua_hang_chi_tiet_ids = self.env['purchase.document.line'].search([('order_id', '=', self.SOURCE_ID.id)])
        chung_tu_mua_hang = self.env['purchase.document'].search([('id', '=', self.SOURCE_ID.id)],limit=1)
        if chung_tu_mua_hang_chi_tiet_ids:
            for line in chung_tu_mua_hang_chi_tiet_ids:
                data = helper.Obj.inject(line, self)

                if chung_tu_mua_hang.LOAI_CHUNG_TU_MH in ('nhap_khau_khong_qua_kho','nhap_khau_nhap_kho') and chung_tu_mua_hang.currency_id.MA_LOAI_TIEN == 'VND':
                    tk_thue = line.TK_DU_THUE_GTGT_ID.id
                else:
                    tk_thue = line.TK_THUE_GTGT_ID.id

                if chung_tu_mua_hang.LOAI_CHUNG_TU_MH == 'trong_nuoc_nhap_kho':
                    so_tien_chiu_thue_quy_doi = line.GIA_TRI_NHAP_KHO - line.CHI_PHI_MUA_HANG
                    if line.TY_GIA !=0:
                        so_tien_chiu_thue_nguyen_te = float_round((line.GIA_TRI_NHAP_KHO - line.CHI_PHI_MUA_HANG)/line.TY_GIA,0)
                elif chung_tu_mua_hang.LOAI_CHUNG_TU_MH == 'nhap_khau_nhap_kho':
                    so_tien_chiu_thue_quy_doi = line.GIA_TRI_NHAP_KHO
                    if line.TY_GIA !=0:
                        so_tien_chiu_thue_nguyen_te = float_round(line.GIA_TRI_NHAP_KHO/line.TY_GIA,0)
                elif chung_tu_mua_hang.LOAI_CHUNG_TU_MH == 'nhap_khau_khong_qua_kho':
                    so_tien_chiu_thue_quy_doi = line.GIA_TINH_THUE_NK
                    if line.TY_GIA !=0:
                        so_tien_chiu_thue_nguyen_te = float_round(line.GIA_TINH_THUE_NK/line.TY_GIA,0)
                else:
                    so_tien_chiu_thue_quy_doi = float_round(line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,0)
                    if chung_tu_mua_hang.currency_id.MA_LOAI_TIEN == 'VND':
                        so_tien_chiu_thue_nguyen_te = float_round(line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,0)
                    else:
                        so_tien_chiu_thue_nguyen_te = float_round(line.THANH_TIEN - line.TIEN_CHIET_KHAU,0)

                data.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'TK_VAT_ID': tk_thue,
                    'PHAN_TRAM_VAT': line.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.THUE_GTGT_ID else None,
                    'SO_TIEN_VAT': float_round(line.TIEN_THUE_GTGT_QUY_DOI,0),
                    'SO_TIEN_VAT_NGUYEN_TE' : float_round(line.TIEN_THUE_GTGT,0),
                    'SO_TIEN_CHIU_VAT': so_tien_chiu_thue_quy_doi,
                    'SO_TIEN_CHIU_VAT_NGUYEN_TE' : so_tien_chiu_thue_nguyen_te,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_ID.id,
                    'SO_CHUNG_TU' : chung_tu_mua_hang.SO_CHUNG_TU,
                    'DIEN_GIAI' : line.name,
                    'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                    'SO_HOA_DON' : self.SO_HOA_DON, 
                    'NGAY_CHUNG_TU' : chung_tu_mua_hang.NGAY_CHUNG_TU,
                    'NGAY_HACH_TOAN' : chung_tu_mua_hang.NGAY_HACH_TOAN,
                    'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
                    'MAU_SO_HD_ID' : self.MAU_SO_HD_ID.id,
                    'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                    'MA_SO_THUE_DOI_TUONG' : chung_tu_mua_hang.MA_SO_THUE,
                    'TEN_DOI_TUONG' : chung_tu_mua_hang.TEN_DOI_TUONG,
                })
                line_ids += [(0,0,data)]
                thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True

    def ghi_so_thue_qua_chung_tu_tra_lai_hb(self):
        line_ids = []
        thu_tu = 0
        chung_tu_tra_lai_hang_ban_chi_tiet_ids = self.env['sale.ex.tra.lai.hang.ban.chi.tiet'].search([('TRA_LAI_HANG_BAN_ID', '=', self.SOURCE_ID.id)])
        chung_tu_tra_lai_hang_ban = self.env['sale.ex.tra.lai.hang.ban'].search([('id', '=', self.SOURCE_ID.id)],limit=1)
        if chung_tu_tra_lai_hang_ban_chi_tiet_ids:
            for line in chung_tu_tra_lai_hang_ban_chi_tiet_ids:
                data = helper.Obj.inject(line, self)

                data.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                    'PHAN_TRAM_VAT': line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.PHAN_TRAM_THUE_GTGT_ID else None,
                    'SO_TIEN_VAT': -1*float_round(line.TIEN_THUE_GTGT_QUY_DOI,0),
                    'SO_TIEN_VAT_NGUYEN_TE' : float_round(line.TIEN_THUE_GTGT,0),
                    'SO_TIEN_CHIU_VAT': -1*(line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI),
                    'SO_TIEN_CHIU_VAT_NGUYEN_TE' : -1*(line.THANH_TIEN - line.TIEN_CHIET_KHAU),
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO_ID.id,
                    'SO_CHUNG_TU' : chung_tu_tra_lai_hang_ban.SO_CHUNG_TU,
                    'DIEN_GIAI' : line.TEN_HANG,
                    'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                    'SO_HOA_DON' : self.SO_HOA_DON, 
                    'NGAY_CHUNG_TU' : chung_tu_tra_lai_hang_ban.NGAY_CHUNG_TU,
                    'NGAY_HACH_TOAN' : chung_tu_tra_lai_hang_ban.NGAY_HACH_TOAN,
                    'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
                    'MAU_SO_HD_ID' : self.MAU_SO_HD_ID.id,
                    'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                    'TEN_DOI_TUONG' : chung_tu_tra_lai_hang_ban.TEN_KHACH_HANG,
                    'MA_SO_THUE_DOI_TUONG' : chung_tu_tra_lai_hang_ban.MA_SO_THUE,
                })
                line_ids += [(0,0,data)]
                thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True


    def ghi_so_thue_qua_chung_tu_giam_gia_hang_mua(self):
        line_ids = []
        thu_tu = 0
        giam_gia_hang_mua = self.env['purchase.ex.giam.gia.hang.mua'].search([('id', '=', self.SOURCE_ID.id)],limit=1)
        if giam_gia_hang_mua:
            for line in giam_gia_hang_mua.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
                data = helper.Obj.inject(line, self)

                data.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                    'PHAN_TRAM_VAT': line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.PHAN_TRAM_THUE_GTGT_ID else None,
                    'SO_TIEN_VAT': -1*float_round(line.TIEN_THUE_GTGT_QUY_DOI,0),
                    'SO_TIEN_VAT_NGUYEN_TE' : float_round(line.TIEN_THUE_GTGT,0),
                    'SO_TIEN_CHIU_VAT': -1*(line.THANH_TIEN_QUY_DOI),
                    'SO_TIEN_CHIU_VAT_NGUYEN_TE' : -1*(line.THANH_TIEN),
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO_ID.id,
                    'SO_CHUNG_TU' : giam_gia_hang_mua.SO_CHUNG_TU,
                    'DIEN_GIAI' : line.TEN_HANG,
                    'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                    'SO_HOA_DON' : self.SO_HOA_DON, 
                    'NGAY_CHUNG_TU' : giam_gia_hang_mua.NGAY_CHUNG_TU,
                    'NGAY_HACH_TOAN' : giam_gia_hang_mua.NGAY_HACH_TOAN,
                    'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
                    'MAU_SO_HD_ID' : self.MAU_SO_HD_ID.id,
                    'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                    'TEN_DOI_TUONG' : giam_gia_hang_mua.TEN_NHA_CUNG_CAP,
                    'MA_SO_THUE_DOI_TUONG' : giam_gia_hang_mua.MA_SO_THUE,
                })
                line_ids += [(0,0,data)]
                thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True
        