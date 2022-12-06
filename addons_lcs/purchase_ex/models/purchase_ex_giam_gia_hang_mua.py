# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_GIAM_GIA_HANG_MUA(models.Model):
    _name = 'purchase.ex.giam.gia.hang.mua'
    _description = 'Chứng từ giảm giá hàng mua'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"

    CHUNG_TU_MUA_HANG = fields.Many2one('purchase.document', string='Chứng từ MH', help='Chứng từ mua hàng')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên NCC', help='Tên nhà cung cấp')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ', default=fields.Datetime.now,required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', compute='_compute_SO_CHUNG_TU', store=True, )
    SO_CHUNG_TU_GIAM_TRU_CONG_NO = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='purchase_ex_giam_gia_hang_mua_SO_CHUNG_TU')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn', required=True,default=fields.Datetime.now)
    NGUOI_NOP = fields.Char(string='Người nộp', help='Người nộp')
    LY_DO_NOP = fields.Char(string='Lý do nộp', help='Lý do nộp',related='DIEN_GIAI')
    KEM_THEO_CT_GOC = fields.Char(string='Kèm theo CT gốc', help='Kèm theo chứng từ gốc')
    SO_PHIEU_THU = fields.Char(string='Số phiếu thu', help='Số phiếu thu', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_PHIEU_THU')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng', compute='tinhtongtien', store=True, currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', compute='tinhtongtien', store=True, currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán', compute='tinhtongtien', store=True, currency_field='currency_id')
    TONG_TIEN_HANG_QD = fields.Monetary(string='', help='Tổng tiền hàng QĐ', compute='tinhtongtien', store=True, currency_field='base_currency_id')
    TIEN_THUE_GTGT_QD = fields.Monetary(string='', help='Tiền thuế giá trị gia tăng QĐ', compute='tinhtongtien', store=True, currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QD = fields.Monetary(string='', help='Tổng tiền thanh toán QĐ', compute='tinhtongtien', store=True, currency_field='base_currency_id')
    name = fields.Char(string='Name', help='Name', related="SO_CHUNG_TU",)
    GIAM_GIA_TRI_HANG_NHAP_KHO = fields.Boolean(string='Giảm giá trị hàng nhập kho', help='Giảm giá trị hàng nhập kho',default=True)
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_MUA_HANG_ID = fields.Many2one('so.mua.hang', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_KHO_ID = fields.Many2one('so.kho', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    GIAM_GIA_HANG_MUA_CHI_TIET_IDS = fields.One2many('purchase.ex.giam.gia.hang.mua.chi.tiet', 'GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID', string='Giảm giá hàng mua chi tiết', copy=True)
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    HOA_DON_REF_ID = fields.Char(help='Ref ID của hóa đơn được import')

    HOA_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Hóa đơn mua hàng',help ='PUInvoiceRefID')
    # _sql_constraints = [
	# ('SO_CHUNG_TU_GG_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	# ]

    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ mua hàng
    def lay_du_lieu_chung_tu_mua_hang(self, args):
        new_line =[[5]]
        chung_tu_mua_hang_id = args.get('chung_tu_mua_hang_id')
        thong_tin_chung_tu_master = self.env['purchase.document'].search([('id', '=', chung_tu_mua_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        ten_doi_tuong = thong_tin_chung_tu_master['TEN_DOI_TUONG']
        so_hd_mua_hang = thong_tin_chung_tu_master['SO_HOA_DON']
        ngay_hd_mua_hang = thong_tin_chung_tu_master['NGAY_HOA_DON']
        danh_sach_chung_tu_mua_hang = self.env['purchase.document.line'].search([('order_id', '=', chung_tu_mua_hang_id)])
        if danh_sach_chung_tu_mua_hang:
            default = self.GIAM_GIA_HANG_MUA_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
            for ct_mh in danh_sach_chung_tu_mua_hang:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [ct_mh['MA_HANG_ID'].id,ct_mh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_mh['name'],
                    'DVT_ID': [ct_mh['DVT_ID'].id,ct_mh['DVT_ID'].name],
                    'KHO_ID': [ct_mh['KHO_ID'].id,ct_mh['KHO_ID'].MA_KHO],
                    'DON_VI_ID': [ct_mh['DON_VI_ID'].id,ct_mh['DON_VI_ID'].MA_DON_VI],
                    'SO_LUONG': ct_mh['SO_LUONG'],
                    'DON_GIA': ct_mh['DON_GIA'],
                    'THANH_TIEN': ct_mh['THANH_TIEN'],
                    'THANH_TIEN_QUY_DOI': ct_mh['THANH_TIEN_QUY_DOI'],
                    'DIEN_GIAI_THUE': ct_mh['DIEN_GIAI_THUE'],
                    'PHAN_TRAM_THUE_GTGT_ID': [ct_mh['THUE_GTGT_ID'].id,ct_mh['THUE_GTGT_ID'].name],
                    'TIEN_THUE_GTGT': ct_mh['TIEN_THUE_GTGT'],
                    'TIEN_THUE_GTGT_QUY_DOI': ct_mh['TIEN_THUE_GTGT_QUY_DOI'],
                    'SO_CHUNG_TU':[chung_tu_mua_hang_id,args.get('chung_tu_mua_hang_name')],
                    'SO_HD_MUA_HANG': so_hd_mua_hang,
                    'NGAY_HD_MUA_HANG': ngay_hd_mua_hang,
                    # 'TIEN_CHIET_KHAU_QUY_DOI': ct_mh['TIEN_CK_QUY_DOI'],
                    })
                new_line += [(0,0,new_data)]
        return {'GIAM_GIA_HANG_MUA_CHI_TIET_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                'TEN_NHA_CUNG_CAP': ten_doi_tuong,}
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU

    selection_chung_tu_giam_gia_hang_mua= fields.Selection([
        ('giam_tru_cong_no', 'Giảm trừ công nợ'),
        ('tra_lai_tien_mat','Thu tiền mặt'),
        ], default='giam_tru_cong_no',string="Hình thức")
    
    CHI_TIET_HANG_HOA = fields.Selection([
        ('hang_tien', 'Hàng tiền'),    
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True, compute='set_loai_chung_tu_giam_gia_hang_mua')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    
    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            if record.selection_chung_tu_giam_gia_hang_mua == 'tra_lai_tien_mat':
                record.validate_unique_thu_chi_tien(record.SO_PHIEU_THU)

    @api.model
    def create(self, vals):
        result = super(PURCHASE_EX_GIAM_GIA_HANG_MUA, self).create(vals)
        result.validate_unique_so_chung_tu()
        result.validate_thu_chi_tien()
        self.create_references(result)
        return result

    def create_references(self, discount_doc):
        # Luôn lập kèm hóa đơn
        vals = {
            'SO_HOA_DON': discount_doc.SO_HOA_DON,
            'NGAY_HOA_DON': discount_doc.NGAY_HOA_DON,
            'KY_HIEU_HD': discount_doc.KY_HIEU_HD,
            'MAU_SO_HD_ID': discount_doc.MAU_SO_HD_ID.id,
            'DOI_TUONG_ID': discount_doc.DOI_TUONG_ID.id,
            'TEN_NHA_CUNG_CAP': discount_doc.TEN_NHA_CUNG_CAP,
            'LOAI_CHUNG_TU': 3402,
            'NHAN_HOA_DON' : True,
            'SOURCE_ID': self._name + ',' + str(discount_doc.id),
        }
        hoa_don = self.env['purchase.ex.hoa.don.mua.hang'].create(vals)
        discount_doc.GIAM_GIA_HANG_MUA_CHI_TIET_IDS.write({'HOA_DON_ID': hoa_don.id})

    @api.multi
    def write(self, values):
        result = super(PURCHASE_EX_GIAM_GIA_HANG_MUA, self).write(values)
        if helper.List.element_in_dict(['selection_chung_tu_giam_gia_hang_mua','SO_PHIEU_THU'], values):
            self.validate_thu_chi_tien()
        if helper.List.element_in_dict(['selection_chung_tu_giam_gia_hang_mua','SO_PHIEU_THU','SO_CHUNG_TU_GIAM_TRU_CONG_NO'], values):
            self.validate_unique_so_chung_tu()
        self.update_references(values)
        return result
    
    def update_references(self, values):
        # Cập nhật hóa đơn gắn kèm nếu có
        vals = helper.Obj.get_sub_dict(values, ('SO_HOA_DON','NGAY_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID','DOI_TUONG_ID','TEN_NHA_CUNG_CAP','SOURCE_ID'))
        for record in self: 
            vals['LOAI_CHUNG_TU'] = 3402
            record.find_reference('purchase.ex.hoa.don.mua.hang').write(vals)

    @api.multi
    def unlink(self):
        for record in self:
            record.find_reference('purchase.ex.hoa.don.mua.hang').unlink()
        return super(PURCHASE_EX_GIAM_GIA_HANG_MUA, self).unlink()

    @api.depends('selection_chung_tu_giam_gia_hang_mua')
    def _compute_SO_CHUNG_TU(self):
        for record in self:
            if record.selection_chung_tu_giam_gia_hang_mua == 'tra_lai_tien_mat':
                record.SO_CHUNG_TU = record.SO_PHIEU_THU
            else:
                record.SO_CHUNG_TU = record.SO_CHUNG_TU_GIAM_TRU_CONG_NO

    @api.depends('selection_chung_tu_giam_gia_hang_mua','GIAM_GIA_TRI_HANG_NHAP_KHO')
    def set_loai_chung_tu_giam_gia_hang_mua(self):
        for record in self:
            if record.GIAM_GIA_TRI_HANG_NHAP_KHO == False:
                if record.selection_chung_tu_giam_gia_hang_mua=='giam_tru_cong_no':
                    record.LOAI_CHUNG_TU = 3042
                else:
                    record.LOAI_CHUNG_TU = 3043
            else : 
                if record.selection_chung_tu_giam_gia_hang_mua=='giam_tru_cong_no':
                    record.LOAI_CHUNG_TU = 3040
                else:
                    record.LOAI_CHUNG_TU = 3041

    @api.depends('GIAM_GIA_HANG_MUA_CHI_TIET_IDS')
    def tinhtongtien(self):
        for order in self:
            tongtienhang = tienthuegtgt = tongtienthanhtoan =0.0
            tong_tien_hang_qđ = tong_tien_thue_gtgt_qđ = tong_tien_thanh_toan_qđ=0.0
            for line in order.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
                tongtienhang += line.THANH_TIEN
                tienthuegtgt += line.TIEN_THUE_GTGT
                tongtienthanhtoan = tongtienhang + tienthuegtgt 

                tong_tien_hang_qđ += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qđ += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_thanh_toan_qđ= tong_tien_hang_qđ + tong_tien_thue_gtgt_qđ
            order.update({
                'TONG_TIEN_HANG': tongtienhang,
                'TIEN_THUE_GTGT': tienthuegtgt,
                'TONG_TIEN_THANH_TOAN': tongtienthanhtoan,

                'TONG_TIEN_HANG_QD': tong_tien_hang_qđ,
                'TIEN_THUE_GTGT_QD': tong_tien_thue_gtgt_qđ,
                'TONG_TIEN_THANH_TOAN_QD': tong_tien_thanh_toan_qđ,
            })
            
    @api.onchange('DOI_TUONG_ID')
    def laythongtinnhacc(self):
        self.TEN_NHA_CUNG_CAP = self.DOI_TUONG_ID.HO_VA_TEN
        self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
        self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
        self.NHAN_VIEN_ID = self.DOI_TUONG_ID.NHAN_VIEN_ID.id
        if self.DOI_TUONG_ID.company_type=='person':
            self.NGUOI_NOP = self.DOI_TUONG_ID.HO_VA_TEN
        else:
            self.NGUOI_NOP =''

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False


    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_mua_hang()
            record.ghi_so_cong_no()
            record.ghi_so_kho()

            hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
            if hoa_don:
                hoa_don.ghi_so_thue_qua_chung_tu_giam_gia_hang_mua()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'NHAN_VIEN_ID' : self.NHAN_VIEN_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'DIEN_GIAI' : line.TEN_HANG,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.THANH_TIEN,
                'GHI_NO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.THANH_TIEN,
                'GHI_CO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]

            # ghi sổ thuế gtgt
            data_thue_gtgt = data_ghi_no.copy()
            data_thue_gtgt.update({
                'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
                'GHI_NO' : line.TIEN_THUE_GTGT,
                'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
            })
            line_ids += [(0,0,data_thue_gtgt)]

            data_thue_gtgt2 = data_thue_gtgt.copy()
            data_thue_gtgt2.update({
                'TAI_KHOAN_ID' : line.TK_THUE_GTGT_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.TIEN_THUE_GTGT,
                'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_thue_gtgt2)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_mua_hang(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'DIEN_GIAI': line.TEN_HANG,
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'SO_LUONG' : 0,
                'DON_GIA' : line.DON_GIA,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'DVT_ID' : line.DVT_ID.id,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                # 'SO_TIEN': line.THANH_TIEN,
                'PHAN_TRAM_THUE_VAT' : line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT' : -1*line.TIEN_THUE_GTGT_QUY_DOI,
                'SO_TIEN_VAT_NGUYEN_TE' : -1*line.TIEN_THUE_GTGT,
                'TAI_KHOAN_VAT_ID' : line.TK_THUE_GTGT_ID.id,
                'SO_TIEN_GIAM_TRU' : line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_GIAM_TRU_NGUYEN_TE' : line.THANH_TIEN,
                'TK_NO_ID' : line.TK_CO_ID.id,
                'TK_CO_ID' : line.TK_NO_ID.id,
                'TEN_DOI_TUONG' : self.TEN_NHA_CUNG_CAP,
                'DIA_CHI_DOI_TUONG' : self.DIA_CHI,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo master
        smh = self.env['so.mua.hang'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_MUA_HANG_ID = smh.id
        return True

    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'TEN_DOI_TUONG' : self.TEN_NHA_CUNG_CAP,
            })
            if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TK_ID': line.TK_NO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.THANH_TIEN_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.THANH_TIEN,
                    'GHI_CO': 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_ghi_no)]
            if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_co = data_goc.copy()
                data_ghi_co.update({
                    'TK_ID': line.TK_CO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                    'GHI_NO': 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO': line.THANH_TIEN_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.THANH_TIEN,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_co)]
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT != 0 or line.TIEN_THUE_GTGT_QUY_DOI !=0):
                if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_NO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                        'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'DIEN_GIAI' : 'Thuế giá trị gia tăng',
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_ghi_no)]
                if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_THUE_GTGT_ID.id,
                        'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'DIEN_GIAI' : 'Thuế giá trị gia tăng',
                        'LOAI_HACH_TOAN' : '2',
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
    
    def ghi_so_kho(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_MUA_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'TK_NO_ID' : line.TK_CO_ID.id,
                'TK_CO_ID' : line.TK_NO_ID.id,
                'SO_TIEN_XUAT' : line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_NHAP' : 0,
                'KHO_ID' : line.KHO_ID.id,
                'DVT_ID' : line.DVT_ID.id,
                'SO_LUONG_NHAP' : 0,
                'SO_LUONG_XUAT' : 0,
                'DON_GIA' : line.DON_GIA,
                'LOAI_KHU_VUC_NHAP_XUAT' : '3',
                'LOAI_KHONG_CAP_NHAT_GIA_XUAT' : '1',
                'KHONG_CAP_NHAT_GIA_XUAT' : True,
            })
            line_ids += [(0,0,data_ghi_no)]
            thu_tu += 1
        # Tạo master
        sk = self.env['so.kho'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_KHO_ID = sk.id
        return True

    @api.multi
    def action_bo_ghi_so(self, args):
        # Bỏ ghi sổ các references
        for record in self:
            hoa_don = record.find_reference('purchase.ex.hoa.don.mua.hang')
            if hoa_don:
                hoa_don.action_bo_ghi_so()
        return super(PURCHASE_EX_GIAM_GIA_HANG_MUA, self).action_bo_ghi_so()