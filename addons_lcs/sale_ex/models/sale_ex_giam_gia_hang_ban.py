# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class SALE_EX_GIAM_GIA_HANG_BAN(models.Model):
    _name = 'sale.ex.giam.gia.hang.ban'
    _description = 'Chứng từ giảm giá hàng bán'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"
    

    CHUNG_TU_BAN_HANG = fields.Many2one('sale.document', string='Chứng từ BH', help='Chứng từ bán hàng')
    CHUNG_TU_GIAM_GIA_HANG_BAN = fields.Selection([('BAN_HANG_HOA_DICH_VU', '1. Bán hàng hóa, dịch vụ'), ('BAN_HANG_DAI_LY_BAN_DUNG_GIA', '2. Bán hàng đại lý bán đúng giá'), ('BAN_HANG_UY_THAC_XUAT_KHAU', '3. Bán hàng ủy thác xuất khẩu'), ], string='Chứng từ giảm giá hàng bán', help='Chứng từ giảm giá hàng bán',default='BAN_HANG_HOA_DICH_VU',required=True)
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV bán hàng', help='Nhân viên bán hàng')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now,required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', compute='_compute_SO_CHUNG_TU', store=True, )
    SO_CHUNG_TU_GIAM_TRU_CONG_NO = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='sale_ex_giam_gia_hang_ban_SO_CHUNG_TU')
    DON_VI_GIAO_DAI_LY_ID = fields.Many2one('res.partner', string='Đơn vị giao ĐL', help='Đơn vị giao đại lý')
    TEN_DON_VI_GIAO_DAI_LY = fields.Char(string='Tên đơn vị giao ĐL', help='Tên đơn vị giao đại lý')
    NGUOI_NHAN = fields.Char(string='Người nhận', help='Người nhận')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    LY_DO_CHI = fields.Char(string='Lý do chi', help='Lý do chi' ,related='DIEN_GIAI')
    SO_PHIEU_CHI = fields.Char(string='Số phiếu chi', help='Số phiếu chi', auto_num='account_ex_phieu_thu_chi_SO_CHUNG_TU_PHIEU_CHI', )
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    NGUOI_MUA_HANG = fields.Char(string='Người mua hàng', help='Người mua hàng')
    TAI_KHOAN_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Tài khoản ngân hàng', help='Tài khoản ngân hàng')
    HINH_THUC_THANH_TOAN = fields.Selection([('TIEN_MAT', 'Tiền mặt'), ('CHUYEN_KHOAN', 'Chuyển khoản'), ('TM_CK', 'TM/CK'), ], string='Hình thức thanh toán', help='Hình thức thanh toán',default='TM_CK',required=True)
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now,required=True)
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng' ,compute='tinhtongtienhang', store=True, currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng' ,compute='tinhtongtienhang', store=True, currency_field='currency_id')
    TONG_CHIET_KHAU = fields.Monetary(string='Tổng chiết khấu', help='Tổng chiết khấu' ,compute='tinhtongtienhang', store=True, currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán' ,compute='tinhtongtienhang', store=True, currency_field='currency_id')
    TONG_TIEN_HANG_QĐ = fields.Monetary(string='', help='Tổng tiền hàng quy đổi' ,compute='tinhtongtienhang', store=True, currency_field='base_currency_id')
    TIEN_THUE_GTGT_QĐ = fields.Monetary(string='', help='Tiền thuế giá trị gia tăng quy đổi' ,compute='tinhtongtienhang', store=True, currency_field='base_currency_id')
    TONG_CHIET_KHAU_QĐ = fields.Monetary(string='', help='Tổng chiết khấu quy đổi',compute='tinhtongtienhang', store=True, currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QĐ = fields.Monetary(string='', help='Tổng tiền thanh toán quy đổi',compute='tinhtongtienhang', store=True, currency_field='base_currency_id')
    KEM_THEO_CT_GOC = fields.Char(string='Kèm theo CT gốc', help='Kèm theo chứng từ gốc')
    name = fields.Char(string='Name', help='Name', related='SO_CHUNG_TU', )
    IN_KEM_BANG_KE = fields.Boolean(string='In kèm bảng kê', help='In kèm bảng kê')
    SO = fields.Char(string='Số', help='Số')
    NGAY = fields.Date(string='Ngày', help='Ngày')
    TEN_MAT_HANG_CHUNG = fields.Char(string='Tên mặt hàng chung', help='Tên mặt hàng chung')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_BAN_HANG_ID = fields.Many2one('so.ban.hang', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',store=True,compute='set_loai_chung_tu_giam_gia_hang_ban') 
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU_TEXT = fields.Char(string='Loại chứng từ', help='Loại chứng từ',compute='thay_doi_loai_chung_tu_text',store=True)
    GIAM_GIA_HANG_BAN_CHI_TIET_IDS = fields.One2many('sale.ex.chi.tiet.giam.gia.hang.ban','GIAM_GIA_HANG_BAN_ID', string='Chi tiết giảm giá hàng bán', copy=True)
    HOA_DON_REF_ID = fields.Char(help='Ref ID của hóa đơn được import')    
    selection_chung_tu_giam_gia_hang_ban= fields.Selection([
        ('giam_tru_cong_no', 'Giảm trừ công nợ'),
        ('tra_lai_tien_mat','Trả lại tiền mặt'),
        ], default='giam_tru_cong_no',string=" ")
    chi_tiet = fields.Selection([
        ('hang_tien', 'Hàng tiền'),    
        ('thong_ke','Thống kê'),
        ], default='hang_tien', string='NO_SAVE')


    #VŨ THÊM
    HOA_DON_BAN_HANG_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', string='Hóa đơn bán hàng', help='SAInvoiceRefID')

    # _sql_constraints = [
	# ('SO_CHUNG_TU_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
	# ]

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ bán hàng
    def lay_du_lieu_chung_tu_ban_hang(self, args):
        new_line =[[5]]
        chung_tu_ban_hang_id = args.get('chung_tu_ban_hang_id')
        thong_tin_chung_tu_master = self.env['sale.document'].search([('id', '=', chung_tu_ban_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        ten_khach_hang = thong_tin_chung_tu_master['TEN_KHACH_HANG']
        danh_sach_chung_tu_ban_hang = self.env['sale.document.line'].search([('SALE_DOCUMENT_ID', '=', chung_tu_ban_hang_id)])
        if danh_sach_chung_tu_ban_hang:
            default = self.GIAM_GIA_HANG_BAN_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, 0, self.currency_id.name!='VND')
            for ct_bh in danh_sach_chung_tu_ban_hang:
                new_data = default.copy()
                new_data.update({
                    'MA_HANG_ID': [ct_bh['MA_HANG_ID'].id,ct_bh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_bh['TEN_HANG'],
                    'DVT_ID': [ct_bh['DVT_ID'].id,ct_bh['DVT_ID'].name],
                    'SO_LUONG': ct_bh['SO_LUONG'],
                    'DON_GIA': ct_bh['DON_GIA'],
                    'THANH_TIEN': ct_bh['THANH_TIEN'],
                    'THANH_TIEN_QUY_DOI': ct_bh['THANH_TIEN_QUY_DOI'],
                    'TY_LE_CHIET_KHAU_PHAN_TRAM': ct_bh['TY_LE_CK'],
                    'TIEN_CHIET_KHAU': ct_bh['TIEN_CHIET_KHAU'],
                    'TIEN_CHIET_KHAU_QUY_DOI': ct_bh['TIEN_CK_QUY_DOI'],
                    'SO_CHUNG_TU_BAN_HANG':[chung_tu_ban_hang_id,args.get('chung_tu_ban_hang_name')],
                    'DIEN_GIAI_THUE': ct_bh['DIEN_GIAI_THUE'],
                    'PHAN_TRAM_THUE_GTGT_ID': [ct_bh['THUE_GTGT_ID'].id,ct_bh['THUE_GTGT_ID'].name],
                    'TIEN_THUE_GTGT': ct_bh['TIEN_THUE_GTGT'],
                    'TIEN_THUE_GTGT_QUY_DOI': ct_bh['TIEN_THUE_GTGT_QUY_DOI'],
                    })
                new_line += [(0,0,new_data)]
        return {'GIAM_GIA_HANG_BAN_CHI_TIET_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                'TEN_KHACH_HANG': ten_khach_hang,}

		
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    
    @api.onchange('NGAY_CHUNG_TU')
    def _onchange_NGAY_NGAY_CHUNG_TU(self):
        self.NGAY_HOA_DON = self.NGAY_CHUNG_TU

    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            if record.selection_chung_tu_giam_gia_hang_ban == 'tra_lai_tien_mat':
                record.validate_unique_thu_chi_tien(record.SO_PHIEU_CHI)

    @api.model
    def create(self, vals):
        result = super(SALE_EX_GIAM_GIA_HANG_BAN, self).create(vals)
        result.validate_unique_so_chung_tu()
        result.validate_thu_chi_tien()
        self.create_references(result)
        return result
    
    def create_references(self, discount_doc):
        # Khi import, hóa đơn gắn kèm được sinh ra trước chứng từ giảm giá
        if discount_doc.HOA_DON_REF_ID:
            hoa_don = self.env.ref('{}.{}'.format('base_import_ex', discount_doc.HOA_DON_REF_ID), False)
            if hoa_don:
                vals = {
                    'SO_HOA_DON': hoa_don.SO_HOA_DON,
                    'NGAY_HOA_DON': hoa_don.NGAY_HOA_DON,
                    'KY_HIEU_HD': hoa_don.KY_HIEU_HD,
                    'MAU_SO_HD_ID': hoa_don.MAU_SO_HD_ID.id,
                    'DA_HACH_TOAN': True,
                    'LOAI_CHUNG_TU' : 3565,
                }
                hoa_don.write({'SOURCE_ID': discount_doc._name + ',' + str(discount_doc.id)})
                discount_doc.write(vals)
                discount_doc.GIAM_GIA_HANG_BAN_CHI_TIET_IDS.write({'HOA_DON_ID': hoa_don.id})
                return
        # Luôn lập kèm hóa đơn
        vals = {
            'SO_HOA_DON': discount_doc.SO_HOA_DON,
            'NGAY_HOA_DON': discount_doc.NGAY_HOA_DON,
            'KY_HIEU_HD': discount_doc.KY_HIEU_HD,
            'MAU_SO_HD_ID': discount_doc.MAU_SO_HD_ID.id,
            'DOI_TUONG_ID': discount_doc.DOI_TUONG_ID.id,
            'TEN_KHACH_HANG': discount_doc.TEN_KHACH_HANG,
            'LOAI_CHUNG_TU': discount_doc.LOAI_CHUNG_TU,
            'SOURCE_ID': self._name + ',' + str(discount_doc.id),
            'TONG_TIEN_THANH_TOAN': discount_doc.TONG_TIEN_THANH_TOAN,
            'DA_HACH_TOAN': True,
        }
        hoa_don = self.env['sale.ex.hoa.don.ban.hang'].create(vals)
        discount_doc.GIAM_GIA_HANG_BAN_CHI_TIET_IDS.write({'HOA_DON_ID': hoa_don.id})

    @api.multi
    def write(self, values):
        result = super(SALE_EX_GIAM_GIA_HANG_BAN, self).write(values)
        if helper.List.element_in_dict(['selection_chung_tu_giam_gia_hang_ban','SO_PHIEU_CHI'], values):
            self.validate_thu_chi_tien()
        if helper.List.element_in_dict(['selection_chung_tu_giam_gia_hang_ban','SO_PHIEU_CHI','SO_CHUNG_TU_GIAM_TRU_CONG_NO'], values):
            self.validate_unique_so_chung_tu()
        self.update_references(values)
        return result
    
    def update_references(self, values):
        # Cập nhật phiếu nhập kho/hóa đơn gắn kèm nếu có
        vals = helper.Obj.get_sub_dict(values, ('SO_HOA_DON','NGAY_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID','DOI_TUONG_ID','TEN_KHACH_HANG','LOAI_CHUNG_TU','SOURCE_ID','TONG_TIEN_THANH_TOAN'))
        for record in self: 
            record.find_reference('sale.ex.hoa.don.ban.hang').write(vals)

    @api.multi
    def unlink(self):
        for record in self:
            record.find_reference('sale.ex.hoa.don.ban.hang').unlink()
        return super(SALE_EX_GIAM_GIA_HANG_BAN, self).unlink()

    @api.depends('selection_chung_tu_giam_gia_hang_ban')
    def _compute_SO_CHUNG_TU(self):
        for record in self:
            if record.selection_chung_tu_giam_gia_hang_ban == 'tra_lai_tien_mat':
                record.SO_CHUNG_TU = record.SO_PHIEU_CHI
            else:
                record.SO_CHUNG_TU = record.SO_CHUNG_TU_GIAM_TRU_CONG_NO
    
    @api.onchange('selection_chung_tu_giam_gia_hang_ban')
    def update_hinhthucthanhtoan(self):
        if(self.selection_chung_tu_giam_gia_hang_ban == 'tra_lai_tien_mat'):
            self.HINH_THUC_THANH_TOAN = 'TIEN_MAT'
        else: 
            self.HINH_THUC_THANH_TOAN= 'TM_CK'

    @api.onchange('currency_id')
    def update_thaydoiIsTy_gia_tien(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False
            
    # Bổ sung hàm depend để lấy loại chứng từ 
    @api.depends('CHUNG_TU_GIAM_GIA_HANG_BAN','selection_chung_tu_giam_gia_hang_ban')
    def set_loai_chung_tu_giam_gia_hang_ban(self):
        if self.selection_chung_tu_giam_gia_hang_ban=='giam_tru_cong_no':
            if self.CHUNG_TU_GIAM_GIA_HANG_BAN =='BAN_HANG_HOA_DICH_VU':
                self.LOAI_CHUNG_TU = 3550
            elif self.CHUNG_TU_GIAM_GIA_HANG_BAN =='BAN_HANG_DAI_LY_BAN_DUNG_GIA':
                self.LOAI_CHUNG_TU = 3552
            else: 
                self.LOAI_CHUNG_TU = 3554
        elif self.selection_chung_tu_giam_gia_hang_ban=='tra_lai_tien_mat':
            if self.CHUNG_TU_GIAM_GIA_HANG_BAN =='BAN_HANG_HOA_DICH_VU':
                self.LOAI_CHUNG_TU = 3551
            elif self.CHUNG_TU_GIAM_GIA_HANG_BAN =='BAN_HANG_DAI_LY_BAN_DUNG_GIA':
                self.LOAI_CHUNG_TU = 3553
            else: 
                self.LOAI_CHUNG_TU = 3555

    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.GIAM_GIA_HANG_BAN_CHI_TIET_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))


    @api.depends('LOAI_CHUNG_TU')
    def thay_doi_loai_chung_tu_text(self):
        for record in self:
            loai_chung_tu_text = ''
            ref_type = record.env['danh.muc.reftype'].search([('REFTYPE', '=', record.LOAI_CHUNG_TU)],limit=1)
            if ref_type:
                loai_chung_tu_text = ref_type.REFTYPENAME
            record.LOAI_CHUNG_TU_TEXT = loai_chung_tu_text
        



    @api.onchange('DOI_TUONG_ID')
    def update_thongtinkhachhang(self):
        self.TEN_KHACH_HANG = self.DOI_TUONG_ID.HO_VA_TEN
        self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
        self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
        self.NGUOI_MUA_HANG = self.env['res.partner'].search([('parent_id','=',self.DOI_TUONG_ID.id)],limit=1).HO_VA_TEN
        # self.TAI_KHOAN_NGAN_HANG_ID = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN','=',self.DOI_TUONG_ID.id)],limit=1).acc_number
        self.NHAN_VIEN_ID = self.DOI_TUONG_ID.NHAN_VIEN_ID.id

    @api.onchange('DON_VI_GIAO_DAI_LY_ID')
    def update_laythongtindonvigiaodaily(self):
        self.TEN_DON_VI_GIAO_DAI_LY = self.DON_VI_GIAO_DAI_LY_ID.HO_VA_TEN

    @api.depends('GIAM_GIA_HANG_BAN_CHI_TIET_IDS')
    def tinhtongtienhang(self):
        for order in self:
            tongtienhang = tienthuegtgt = tienchietkhau = tongtienthanhtoan =0.0
            tong_tien_hang_qd = tong_tien_thue_gtgt_qd = tong_tien_chiet_khau_qd = tong_tien_thanh_toan_qd = 0.0
            for line in order.GIAM_GIA_HANG_BAN_CHI_TIET_IDS:
                tongtienhang += line.THANH_TIEN
                tienthuegtgt += line.TIEN_THUE_GTGT
                tienchietkhau += line.TIEN_CHIET_KHAU
                tongtienthanhtoan = tongtienhang + tienthuegtgt - tienchietkhau

                tong_tien_hang_qd += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qd += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_chiet_khau_qd += line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_thanh_toan_qd = tong_tien_hang_qd + tong_tien_thue_gtgt_qd - tong_tien_chiet_khau_qd

            order.update({
                'TONG_TIEN_HANG': tongtienhang,
                'TIEN_THUE_GTGT': tienthuegtgt,
                'TONG_CHIET_KHAU': tienchietkhau,
                'TONG_TIEN_THANH_TOAN': tongtienthanhtoan,

                'TONG_TIEN_HANG_QĐ': tong_tien_hang_qd,
                'TIEN_THUE_GTGT_QĐ': tong_tien_thue_gtgt_qd,
                'TONG_CHIET_KHAU_QĐ': tong_tien_chiet_khau_qd,
                'TONG_TIEN_THANH_TOAN_QĐ': tong_tien_thanh_toan_qd,
            })

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_ban_hang()
            record.ghi_so_cong_no()
            hoa_don = record.find_reference('sale.ex.hoa.don.ban.hang')
            if hoa_don:
                hoa_don.ghi_so_thue_tu_giam_gia_hang_ban()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_BAN_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'DIEN_GIAI' : line.TEN_HANG,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.THANH_TIEN,
                'GHI_NO_NGUYEN_TE' : line.THANH_TIEN_QUY_DOI,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'DOI_TUONG_THCP_ID' : None,
                
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
            if line.TK_CHIET_KHAU_ID and (line.TIEN_CHIET_KHAU != 0 or line.TIEN_CHIET_KHAU_QUY_DOI != 0):
                # Ghi sổ tk chiết khấu
                data_chiet_khau = data_ghi_no.copy()
                data_chiet_khau.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CHIET_KHAU_ID.id,
                    'GHI_NO' : line.TIEN_CHIET_KHAU,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_CHIET_KHAU_QUY_DOI,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
					'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_chiet_khau)]
                data_chiet_khau2 = data_chiet_khau.copy()
                data_chiet_khau2.update({
                    'TAI_KHOAN_ID' : line.TK_CHIET_KHAU_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO' : line.TIEN_CHIET_KHAU,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_CHIET_KHAU_QUY_DOI,
					'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_chiet_khau2)]
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT != 0 or line.TIEN_THUE_GTGT_QUY_DOI != 0):
                # Ghi sổ thuế gtgt
                data_thue_gtgt = data_ghi_no.copy()
                data_thue_gtgt.update({
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    'TAI_KHOAN_ID' : line.TK_THUE_GTGT_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                    'GHI_NO' : line.TIEN_THUE_GTGT,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT_QUY_DOI,
                    'GHI_CO' : 0,
                    'GHI_CO_NGUYEN_TE' : 0,
					'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_thue_gtgt)]

                data_thue_gtgt2 = data_thue_gtgt.copy()
                data_thue_gtgt2.update({
                    'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID' : line.TK_THUE_GTGT_ID.id,
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

    def ghi_so_ban_hang(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_BAN_CHI_TIET_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU_CTBH': self._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.TEN_HANG,
                'SO_HOA_DON' : self.SO_HOA_DON,
                'TK_CHIET_KHAU_ID' : line.TK_CHIET_KHAU_ID.id,
                'DVT_ID' : line.DVT_ID.id,
                'PHAN_TRAM_CHIET_KHAU' : line.TY_LE_CHIET_KHAU_PHAN_TRAM,
                'SO_TIEN_CHIET_KHAU' : -1*line.TIEN_CHIET_KHAU_QUY_DOI,
                'SO_TIEN_CHIET_KHAU_NGUYEN_TE' : -1*line.TIEN_CHIET_KHAU,
                'SO_TIEN_GIAM_TRU' : line.THANH_TIEN_QUY_DOI,
                'SO_TIEN_GIAM_TRU_NGUYEN_TE' : line.THANH_TIEN,
                'PHAN_TRAM_THUE_VAT' : line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_VAT' : -1*line.TIEN_THUE_GTGT_QUY_DOI,
                'SO_TIEN_VAT_NGUYEN_TE' : -1*line.TIEN_THUE_GTGT,
                'TAI_KHOAN_VAT_ID' : line.TK_THUE_GTGT_ID.id,
                'DON_GIA' : 0,
                'SO_LUONG' : 0,
                'TK_NO_ID' : line.TK_CO_ID.id,
                'TK_CO_ID' : line.TK_NO_ID.id,
                'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                'DIA_CHI_DOI_TUONG' : self.DIA_CHI,
            })
            line_ids += [(0,0,data)]
            thu_tu += 1
        # Tạo master
        sbh = self.env['so.ban.hang'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_BAN_HANG_ID = sbh.id
        return True

    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIAM_GIA_HANG_BAN_CHI_TIET_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.TEN_HANG,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DON_GIA_NGUYEN_TE' : line.DON_GIA,
                'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
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
                if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_CO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'LOAI_HACH_TOAN' : '2',
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    })
                    line_ids += [(0,0,data_ghi_no)]
                if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_THUE_GTGT_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'GHI_NO': line.TIEN_THUE_GTGT_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
                        'LOAI_HACH_TOAN' : '1',
                        'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    })
                    line_ids += [(0,0,data_ghi_co)]

            if line.TK_CHIET_KHAU_ID and (line.TIEN_CHIET_KHAU != 0 or line.TIEN_CHIET_KHAU_QUY_DOI !=0):
                if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_no = data_goc.copy()
                    data_ghi_no.update({
                        'TK_ID': line.TK_CO_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CHIET_KHAU_ID.id,
                        'GHI_NO': 0,
                        'GHI_NO_NGUYEN_TE' : 0,
                        'GHI_CO': line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_CO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                        'LOAI_HACH_TOAN' : '1',
                    })
                    line_ids += [(0,0,data_ghi_no)]
                if line.TK_CHIET_KHAU_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    data_ghi_co = data_goc.copy()
                    data_ghi_co.update({
                        'TK_ID': line.TK_CHIET_KHAU_ID.id,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        
                        'GHI_NO': line.TIEN_CHIET_KHAU_QUY_DOI,
                        'GHI_NO_NGUYEN_TE' : line.TIEN_CHIET_KHAU,
                        'GHI_CO': 0,
                        'GHI_CO_NGUYEN_TE' : 0,
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

    @api.multi
    def action_bo_ghi_so(self, args):
        # Bỏ ghi sổ các references
        for record in self:
            hoa_don = record.find_reference('sale.ex.hoa.don.ban.hang')
            if hoa_don:
                hoa_don.action_bo_ghi_so()
        return super(SALE_EX_GIAM_GIA_HANG_BAN, self).action_bo_ghi_so()
   