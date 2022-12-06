# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import timedelta, datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
import json

class ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC(models.Model):
    _name = 'account.ex.chung.tu.nghiep.vu.khac'
    _description = 'Chứng từ nghiệp vụ khác'
    _inherit = ['mail.thread']
    _order ="NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"


    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1156
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')#, auto_num='account_ex_chung_tu_nghiep_vu_khac_SO_CHUNG_TU')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now)
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu' ,readonly='true')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')
    NGAY_BU_TRU = fields.Date(string='Ngày bù trừ', help='Ngày bù trừ',default=fields.Datetime.now)
    NGAY_DOI_TRU = fields.Date(string='Ngày đối trừ', help='Ngày đối trừ')
    THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng ', help='Tháng ')
    NAM = fields.Integer(string='Năm', help='Năm')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS = fields.One2many('account.ex.chung.tu.nghiep.vu.khac.hach.toan', 'CHUNG_TU_NGHIEP_VU_KHAC_ID', string='Chứng từ nghiệp vụ khác hạch toán')
    ACCOUNT_EX_THUE_IDS = fields.One2many('account.ex.thue', 'CHUNG_TU_KHAC_THUE_ID', string='Thuế')
    ACCOUNT_EX_TAM_UNG_PHIEU_CHI_IDS = fields.One2many('account.ex.tam.ung.phieu.chi', 'CHUNG_TU_TAM_UNG_ID', string='Tạm ứng phiếu chi')
    TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE_IDS = fields.One2many('tong.hop.chung.tu.nghiep.vu.khac.so.du.ngoai.te', 'CHUNG_TU_NGHIEP_VU_KHAC_ID', string='Chứng từ nghiệp vụ khác số dư ngoại tệ')
    TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN_IDS = fields.One2many('tong.hop.chung.tu.nghiep.vu.khac.cong.no.thanh.toan', 'CHUNG_TU_NGHIEP_VU_KHAC_ID', string='Chứng từ nghiệp vụ khác công nợ thanh toán')
    TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CHUNG_TU_CONG_NO_IDS = fields.One2many('tong.hop.chung.tu.nghiep.vu.khac.chung.tu.cong.no', 'CHUNG_TU_NGHIEP_VU_KHAC_ID', string='Chứng từ nghiệp vụ khác chứng từ công nợ')
    TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_PHAN_BO_IDS = fields.One2many('tong.hop.phan.bo.chi.phi.tra.truoc.phan.bo', 'PHAN_BO_CHI_PHI_TRA_TRUOC_ID', string='Phân bổ chi phí trả trước phân bổ')
    TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_XD_CHI_PHI_IDS = fields.One2many('tong.hop.phan.bo.chi.phi.tra.truoc.xd.chi.phi', 'PHAN_BO_CHI_PHI_TRA_TRUOC_ID', string='Phân bổ chi phí trả trước xd chi phí')
    TONG_TIEN_PHAN_BO = fields.Float(string='Tổng số tiền phân bổ', help='Tổng số tiền phân bổ',compute='tinh_tong_tien_phan_bo', store=True, digits= decimal_precision.get_precision('VND'))
    LOAI_CHUNG_TU_QTTU_NVK = fields.Selection([('NGHIEP_VU', 'Chứng từ nghiệp vụ khác'), ('QUYET_TOAN', 'Quyết toán tạm ứng'), ('BU_TRU_CN', 'Chứng từ bù trừ công nợ'),('XU_LY_CHENH_LECH_TY_GIA_XUAT_QUY', 'Xử lý chênh lệch tỷ giá tính tỷ giá xuất quỹ'), ('XU_LY_CHENH_LECH_TY_GIA_TK_NGOAI_TE', 'Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ'),('KHAU_TRU_THUE_GTGT', 'Khấu trừ thuế'),('KET_CHUYEN_LAI_LO', 'Kết chuyển lãi lỗ'),('XU_LY_CHENH_LECH_TY_GIA', 'Xử lý chênh lệch tỷ giá')], string='Loại chứng từ',default='NGHIEP_VU') 
    QUYET_TOAN_CHO_TUNG_LAN_TAM_UNG = fields.Boolean(string='Quyết toán cho từng lần tạm ứng', help='Quyết toán cho từng lần tạm ứng')
    PHIEU_CHI_TAM_UNG_ID = fields.Many2many('account.ex.phieu.thu.chi', string='Phiếu chi tạm ứng', help='Phiếu chi tạm ứng')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TEN_NV = fields.Char(string='Tên nhân viên', help='Tên nhân viên',readonly='true',related="NHAN_VIEN_ID.HO_VA_TEN",store=True)
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng',readonly='true',related="DOI_TUONG_ID.HO_VA_TEN",store=True)
    SO_TIEN_TAM_UNG = fields.Monetary(string='Số tiền tạm ứng', help='Số tiền tạm ứng', currency_field='currency_id')
    SO_TIEN_THUA_THIEU = fields.Monetary(string='Số tiền thừa thiếu', help='Số tiền thừa thiếu', currency_field='currency_id')
    SO_TIEN_TAM_UNG_QD = fields.Monetary(string='Số tiền tạm ứng QĐ', help='Số tiền tạm ứng quy đổi', currency_field='base_currency_id')
    SO_TIEN_THUA_THIEU_QD = fields.Monetary(string='Số tiền thừa/thiếu QĐ', help='Số tiền thừa thiếu quy đổi', currency_field='base_currency_id')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True)

    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ',help='Loại chứng từ')
    # Mạnh thêm mới các trường của form Khấu trừ thuế
    KY_TINH_THUE_THANG = fields.Selection([('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'), ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'), ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'), ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'), ], string='Kỳ tính thuế', help='Kỳ tính thuế',default='1')
    KY_TINH_THUE_QUY = fields.Selection([('1', 'Quý 1'), ('2', 'Quý 2'), ('3', 'Quý 3'), ('4', 'Quý 4'), ], string='Kỳ tính thuế', help='Kỳ tính thuế',default='1')
    THUE_GTGT_DAU_VAO_DUOC_KHAU_TRU = fields.Float(string='Thuế GTGT đầu vào được khấu trừ', help='Thuế giá trị gia tăng đầu vào được khấu trừ',digits=decimal_precision.get_precision('VND'))
    THUE_GTGT_DAU_RA = fields.Float(string='Thuế GTGT đầu ra', help='Thuế giá trị gia đầu ra',digits=decimal_precision.get_precision('VND'))

    LOAI_TO_KHAI = fields.Selection([('TO_KHAI_THANG', 'Tờ khai tháng'), ('TO_KHAI_QUY', 'Tờ khai quý'), ('TO_KHAI_LAN_PHAT_SINH', 'Tờ khai lần phát sinh'), ], string='Loại tờ khai', help='Loại tờ khai',default='TO_KHAI_THANG')



    TONG_CHENH_LECH = fields.Float(string='Tổng chênh lệch', help='Tổng chênh lệch',compute='tinh_tong_tien_chenh_lech',store=True,digits= decimal_precision.get_precision('VND'))
    DANH_GIA_NGOAI_TE_ID = fields.Many2one('res.currency', string='Đánh giá ngoại tệ', help='Đánh giá ngoại tệ')
    TK_XU_LY_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lãi', help='Tk xử lý lãi')
    TK_XU_LY_LO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lỗ', help='Tk xử lý lỗ ')
    CHI_TIET_NGHIEP_VU_KHAC = fields.Selection([
        ('HACH_TOAN', 'Hạch toán'),
        ('HOA_DON', 'Hóa đơn'),
        ], default='HACH_TOAN', string='NO_SAVE')
    name = fields.Char(string='Name', related="SO_CHUNG_TU", )
    SO_CHUNG_TU_TU_TANG_JSON = fields.Char(store=False)

    LOAI_CHUNG_TU_TEXT = fields.Char(string='Loại chứng từ', help='Loại chứng từ',compute='thay_doi_loai_chung_tu_text',store=True)
    SALE_EX_DOI_TRU_CHI_TIET_IDS = fields.One2many('sale.ex.doi.tru.chi.tiet', 'CHUNG_TU_NGHIEP_VU_KHAC_ID', string='Chứng từ nghiệp vụ khác chứng từ công nợ')
    TONG_HOP_CHUNG_TU_NVK_BU_TRU_CHI_TIET_IDS = fields.One2many('tong.hop.chung.tu.nvk.bu.tru.chi.tiet', 'CHUNG_TU_NGHIEP_VU_KHAC_ID', string='Chứng từ nghiệp vụ khác chứng từ công nợ')
	
    @api.onchange('LOAI_CHUNG_TU', 'currency_id')
    def update_tai_khoan_ngam_dinh(self):
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))
        for line in self.ACCOUNT_EX_THUE_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))
        for line in self.ACCOUNT_EX_TAM_UNG_PHIEU_CHI_IDS:
            tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for tk in tk_nds:
                setattr(line, tk, tk_nds.get(tk))

    @api.onchange('currency_id','TY_GIA') #Mạnh xử lý bug1976
    def lay_tien_thue_gtgt_quy_doi(self):
        for record in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            record.TIEN_THUE_GTGT_QD = float_round(record.TIEN_THUE_GTGT * self.TY_GIA, 0)

    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_HACH_TOAN:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN
            if self.LOAI_CHUNG_TU == 4012:
                self.DIEN_GIAI = 'Kết chuyển lãi lỗ đến ngày ' + str(datetime.strptime(self.NGAY_HACH_TOAN, '%Y-%m-%d').date().strftime("%d/%m/%Y"))
                self.TY_GIA = 1
                du_lieu_ket_chuyen = self.lay_du_ket_chuyen_lai_lo()
                if du_lieu_ket_chuyen:
                    self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS = du_lieu_ket_chuyen
                else:
                    self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS = []

    @api.onchange('NGAY_HACH_TOAN','NGAY_CHUNG_TU','SO_CHUNG_TU','DOI_TUONG_ID')
    def _onchange_THAM_SO_MASTER(self):
        if self.LOAI_CHUNG_TU == 4014:
            if self.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                for line in self.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                    line.NGAY_HACH_TOAN_THANH_TOAN = self.NGAY_HACH_TOAN
                    line.NGAY_CHUNG_TU_THANH_TOAN = self.NGAY_CHUNG_TU
                    line.SO_CHUNG_TU_THANH_TOAN = self.SO_CHUNG_TU
                    line.DOI_TUONG_ID = self.DOI_TUONG_ID.id

    def lay_so_chung_tu_tu_tang(self, loai_chung_tu):
        auto_num = json.loads(self.SO_CHUNG_TU_TU_TANG_JSON or '{}')
        if not auto_num.get(loai_chung_tu):
            code = 'account_ex_chung_tu_nghiep_vu_khac_SO_CHUNG_TU' + loai_chung_tu
            next_seq = self.env['ir.sequence'].next_char_by_code(code)
            auto_num[loai_chung_tu] = next_seq

        return auto_num

    def lay_so_chung_tu_tiep_theo(self):
        self.ensure_one()
        loai_chung_tu = '_QTTU' if self.LOAI_CHUNG_TU_QTTU_NVK == 'QUYET_TOAN' else ''
        code = 'account_ex_chung_tu_nghiep_vu_khac_SO_CHUNG_TU' + loai_chung_tu
        return self.env['ir.sequence'].next_char_by_code(code)

    @api.onchange('LOAI_CHUNG_TU_QTTU_NVK')
    def set_loai_chung_tu_nvk(self):
        # update_SO_CHUNG_TU
        loai_chung_tu = '_QTTU' if self.LOAI_CHUNG_TU_QTTU_NVK == 'QUYET_TOAN' else ''
        auto_num = self.lay_so_chung_tu_tu_tang(loai_chung_tu)
        self.SO_CHUNG_TU = auto_num.get(loai_chung_tu)
        self.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num)

        # update LOAI_CHUNG_TU
        for record in self:
            if record.LOAI_CHUNG_TU_QTTU_NVK == 'NGHIEP_VU':
                record.LOAI_CHUNG_TU = 4010
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'QUYET_TOAN':
                record.LOAI_CHUNG_TU = 4015
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'XU_LY_CHENH_LECH_TY_GIA_XUAT_QUY':
                record.LOAI_CHUNG_TU = 4017
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'XU_LY_CHENH_LECH_TY_GIA_TK_NGOAI_TE':
                record.LOAI_CHUNG_TU = 4016
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'BU_TRU_CN':
                record.LOAI_CHUNG_TU = 4014
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'KHAU_TRU_THUE_GTGT':
                record.LOAI_CHUNG_TU = 4011
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'KET_CHUYEN_LAI_LO':
                record.LOAI_CHUNG_TU = 4012

    @api.depends('LOAI_CHUNG_TU')
    def thay_doi_loai_chung_tu_text(self):
        for record in self:
            # if record.LOAI_CHUNG_TU == 4020: #phan bo chi phi tra truoc
            #     auto_num = record.lay_so_chung_tu_tu_tang('_PBCPTT')
            #     record.SO_CHUNG_TU = auto_num.get('_PBCPTT')
            #     record.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num)   

            loai_chung_tu_text = ''
            ref_type = record.env['danh.muc.reftype'].search([('REFTYPE', '=', record.LOAI_CHUNG_TU)],limit=1)
            if ref_type:
                loai_chung_tu_text = ref_type.REFTYPENAME
            record.LOAI_CHUNG_TU_TEXT = loai_chung_tu_text

    @api.onchange('LOAI_CHUNG_TU')
    def thay_doi_sct_pbcp(self):
        for record in self:
            if record.LOAI_CHUNG_TU == 4020: #phan bo chi phi tra truoc
                auto_num = record.lay_so_chung_tu_tu_tang('_PBCPTT')
                record.SO_CHUNG_TU = auto_num.get('_PBCPTT')
                record.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num)

            if record.LOAI_CHUNG_TU == 4012: #kết chuyển lãi lỗ
                auto_num = record.lay_so_chung_tu_tu_tang('_KCLL')
                record.SO_CHUNG_TU = auto_num.get('_KCLL')
                record.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num) 
              


    @api.onchange('currency_id')
    def update_thaydoiIsTy_gia_tien(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False
    
    @api.onchange('DIEN_GIAI')
    def thaydoidiengiai(self):
        x = self.DIEN_GIAI
        for order in self:
            for line in order.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
                line.DIEN_GIAI = order.DIEN_GIAI if line.DIEN_GIAI == x else line.DIEN_GIAI


    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        if self.LOAI_CHUNG_TU != 4014:
            for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
                line.tinh_tien_quy_doi()

    
    @api.model
    def create(self, values):
        result = super(ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC, self).create(values)
        sequence_code = 'account_ex_chung_tu_nghiep_vu_khac_SO_CHUNG_TU'
        if result.LOAI_CHUNG_TU_QTTU_NVK == 'QUYET_TOAN':
            sequence_code = 'account_ex_chung_tu_nghiep_vu_khac_SO_CHUNG_TU_QTTU'
        self.update_sequence(sequence_code, result.SO_CHUNG_TU)
        if result.LOAI_CHUNG_TU == 4014:
            if result.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                for doi_tru_chi_tiet in result.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                    doi_tru_chi_tiet.write({'ID_CHUNG_TU_THANH_TOAN' : result.id, 'MODEL_CHUNG_TU_THANH_TOAN' : result._name})
        return result
    

    @api.multi
    def action_ghi_so(self):
        for record in self:
            if record.LOAI_CHUNG_TU_QTTU_NVK == 'XU_LY_CHENH_LECH_TY_GIA_TK_NGOAI_TE':
                record.ghi_so_cai_xu_ly_chenh_lech_ty_gia()
            elif record.LOAI_CHUNG_TU_QTTU_NVK in ('NGHIEP_VU','KET_CHUYEN_LAI_LO'):
                record.ghi_so_cai_nghiep_vu_khac()
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'QUYET_TOAN':
                record.ghi_so_cai_quyet_toan_tam_ung()
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'BU_TRU_CN':
                record.ghi_so_cai_bu_tru_cong_no()
            elif record.LOAI_CHUNG_TU_QTTU_NVK == 'XU_LY_CHENH_LECH_TY_GIA_XUAT_QUY':
                record.ghi_so_cai_chenh_lech_ty_gia_xuat_quy()
            record.ghi_so_cong_no()
            if record.LOAI_CHUNG_TU_QTTU_NVK == 'QUYET_TOAN':
                record.ghi_so_thue_quyet_toan_tam_ung()
            else:
                record.ghi_so_thue()
            if record.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                for line in record.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                    if record.LOAI_CHUNG_TU == 4014:
                        line.write({'CTTT_DA_GHI_SO' : True})
                    if record.LOAI_CHUNG_TU == 4013:
                        line.write({'CTTT_DA_GHI_SO' : True,'CTCN_DA_GHI_SO' : True})
        self.write({'state':'da_ghi_so'})

    @api.multi
    def action_bo_ghi_so(self, args):
        for record in self:
            if record.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                for line in record.SALE_EX_DOI_TRU_CHI_TIET_IDS:
                    if record.LOAI_CHUNG_TU == 4014:
                        line.write({'CTTT_DA_GHI_SO' : False})
                    if record.LOAI_CHUNG_TU == 4013:
                        line.write({'CTTT_DA_GHI_SO' : False,'CTCN_DA_GHI_SO' : False})
        return super(ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC, self).action_bo_ghi_so()
    def ghi_so_cai_xu_ly_chenh_lech_ty_gia(self):
        line_ids = []
        thu_tu = 0
        # cách ghi sổ
            # Đối với tài khoản xử lý lãi và tk xử lý lỗ thì ghi vnd với ngyên tệ và quy đổi bằng nhau vì tỷ giá = 1
            # với chiều ngược lại thì ghi theo loại tiền ở master và chỉ ghi quy đổi còn nguyên tệ = 0, tỷ giá lấy theo LastExchangeRate
        currency = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1)
        tk_xu_ly_lai = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '515')], limit=1)
        tk_xu_ly_lo = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '635')], limit=1)
        currency_id = False
        tk_xu_ly_lai_id = False
        tk_xu_ly_lo_id = False
        if currency:
            currency_id = currency.id
        if tk_xu_ly_lai:
            tk_xu_ly_lai_id = tk_xu_ly_lai.id
        if tk_xu_ly_lo:
            tk_xu_ly_lo_id = tk_xu_ly_lo.id
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'TAI_KHOAN_NGAN_HANG_ID' : line.TK_NGAN_HANG_ID.id,
                'TY_GIA' : line.TY_GIA_DANH_GIA_LAI_GAN_NHAT,
                'currency_id' : self.currency_id.id,
                'NGAY_HOA_DON' : None,
            })
            # if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
            data_ghi_no = data_goc.copy()
            data_ghi_no.update({
                'TAI_KHOAN_ID': line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID': line.TK_CO_ID.id,
                'GHI_NO': line.SO_TIEN_QUY_DOI,
                # 'GHI_NO_NGUYEN_TE' : line.SO_TIEN_QUY_DOI,
                'GHI_CO': 0,
                'GHI_CO_NGUYEN_TE' : 0,
                'LOAI_HACH_TOAN' : '1',
                'DOI_TUONG_ID' : line.DOI_TUONG_NO_ID.id,
            })
            line_ids += [(0,0,data_ghi_no)]
            # if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
            data_ghi_co = data_goc.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID': line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID': line.TK_NO_ID.id,
                'GHI_NO': 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO': line.SO_TIEN_QUY_DOI,
                # 'GHI_CO_NGUYEN_TE' : line.SO_TIEN_QUY_DOI,
                'LOAI_HACH_TOAN' : '2',
                'DOI_TUONG_ID' : line.DOI_TUONG_CO_ID.id,
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1

        for chi_tiet in line_ids:
            if chi_tiet[2].get('TAI_KHOAN_ID') == self.TK_XU_LY_LAI_ID.id or chi_tiet[2].get('TAI_KHOAN_ID') == self.TK_XU_LY_LO_ID.id:
                chi_tiet[2]['currency_id'] = currency_id
                chi_tiet[2]['TY_GIA'] = 1
                chi_tiet[2]['GHI_CO_NGUYEN_TE'] = chi_tiet[2].get('GHI_CO')
                chi_tiet[2]['GHI_NO_NGUYEN_TE'] = chi_tiet[2].get('GHI_NO')
            # a = 1
            
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_cai_nghiep_vu_khac(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'DOI_TUONG_ID' : line.DOI_TUONG_NO_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'TAI_KHOAN_ID': line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_NGAN_HANG_ID' : line.TK_NGAN_HANG_ID.id,
                'GHI_NO' : line.SO_TIEN_QUY_DOI,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'NHAN_VIEN_ID' : line.NHAN_VIEN_ID.id,
                'HOP_DONG_BAN_ID' : None,
                'NGAY_HOA_DON' : None,
                'TY_GIA' : self.TY_GIA,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'DOI_TUONG_ID' : line.DOI_TUONG_CO_ID.id,
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN_QUY_DOI,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_cai_quyet_toan_tam_ung(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'TAI_KHOAN_NGAN_HANG_ID' : line.TK_NGAN_HANG_ID.id,
                'NGAY_HOA_DON' : line.NGAY_HOA_DON,
                'SO_HOA_DON' : line.SO_HOA_DON,
            })
            # if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
            data_ghi_no = data_goc.copy()
            data_ghi_no.update({
                'TAI_KHOAN_ID': line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID': line.TK_CO_ID.id,
                'GHI_NO': line.SO_TIEN_QUY_DOI,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO': 0,
                'GHI_CO_NGUYEN_TE' : 0,
                'LOAI_HACH_TOAN' : '1',
                'DOI_TUONG_ID' : line.DOI_TUONG_NO_ID.id,
                'NHAN_VIEN_ID' : None,
                'DIEN_GIAI' : line.DIEN_GIAI,
            })
            line_ids += [(0,0,data_ghi_no)]
            # if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
            data_ghi_co = data_goc.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID': line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID': line.TK_NO_ID.id,
                'GHI_NO': 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO': line.SO_TIEN_QUY_DOI,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
                'LOAI_HACH_TOAN' : '2',
                'DOI_TUONG_ID' : line.DOI_TUONG_CO_ID.id,
                'NHAN_VIEN_ID' : None,
                'DIEN_GIAI' : line.DIEN_GIAI,
            })
            line_ids += [(0,0,data_ghi_co)]
            # ghi số tài khoản thuế
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT > 0 or line.TIEN_THUE_GTGT_QD > 0):
                # if line.TK_THUE_GTGT_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_gtgt = data_goc.copy()
                data_ghi_gtgt.update({
                    'TAI_KHOAN_ID': line.TK_THUE_GTGT_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.TIEN_THUE_GTGT_QD,
                    'GHI_NO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'GHI_CO': 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                    'DOI_TUONG_ID' : line.DOI_TUONG_NO_ID.id,
                    'NHAN_VIEN_ID' : None,
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                })
                line_ids += [(0,0,data_ghi_gtgt)]
                # if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_gtgt2 = data_goc.copy()
                data_ghi_gtgt2.update({
                    'TAI_KHOAN_ID': line.TK_CO_ID.id,
                    'TAI_KHOAN_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                    'GHI_NO': 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO': line.TIEN_THUE_GTGT_QD,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'LOAI_HACH_TOAN' : '2',
                    'DOI_TUONG_ID' : line.DOI_TUONG_CO_ID.id,
                    'NHAN_VIEN_ID' : None,
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                })
                line_ids += [(0,0,data_ghi_gtgt2)]
            thu_tu += 1

        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_cai_bu_tru_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'TAI_KHOAN_ID': line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_NGAN_HANG_ID' : line.TK_NGAN_HANG_ID.id,
                'GHI_NO' : line.SO_TIEN_QUY_DOI,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'NHAN_VIEN_ID' : line.NHAN_VIEN_ID.id,
                'NGAY_HOA_DON' : None,
                'TY_GIA' : 0,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN_QUY_DOI,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_cai_chenh_lech_ty_gia_xuat_quy(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'DOI_TUONG_ID' : line.DOI_TUONG_NO_ID.id,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'TAI_KHOAN_ID': line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_NGAN_HANG_ID' : line.TK_NGAN_HANG_ID.id,
                'GHI_NO' : line.SO_TIEN_QUY_DOI,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'DOI_TUONG_ID' : line.DOI_TUONG_CO_ID.id,
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN_QUY_DOI,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True
    
    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data_goc = helper.Obj.inject(line, self)
            if self.LOAI_CHUNG_TU_QTTU_NVK in ('XU_LY_CHENH_LECH_TY_GIA_TK_NGOAI_TE','NGHIEP_VU','QUYET_TOAN'):
                if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    doi_tuong_id = line.DOI_TUONG_NO_ID.id
                elif line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                    doi_tuong_id = line.DOI_TUONG_CO_ID.id
                else:
                    doi_tuong_id = self.DOI_TUONG_ID.id
            else:
                doi_tuong_id = self.DOI_TUONG_ID.id
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                'DOI_TUONG_ID' : doi_tuong_id,
                'NHAN_VIEN_ID' : line.NHAN_VIEN_ID.id,
                'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
            })
            if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TK_ID': line.TK_NO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.SO_TIEN_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
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
                    'GHI_CO': line.SO_TIEN_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_co)]
            if line.TK_THUE_GTGT_ID and (line.TIEN_THUE_GTGT > 0 or line.TIEN_THUE_GTGT_QD > 0):
                data_ghi_gtgt = data_goc.copy()
                data_ghi_gtgt.update({
                    'TK_ID': line.TK_CO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_THUE_GTGT_ID.id,
                    'GHI_NO': 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO': line.TIEN_THUE_GTGT_QD,
                    'GHI_CO_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_gtgt)]
            thu_tu += 1
        scn = self.env['so.cong.no'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CONG_NO_ID = scn.id
        return True

    def ghi_so_thue_quyet_toan_tam_ung(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                'SO_TIEN_VAT': line.TIEN_THUE_GTGT,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'PHAN_TRAM_VAT' : line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_CHIU_VAT' : line.SO_TIEN,
                'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.SO_TIEN,
                'NGAY_HOA_DON' : self.NGAY_HACH_TOAN,
                'SO_HOA_DON' : line.SO_HOA_DON,
                'KY_HIEU_HOA_DON' : line.KY_HIEU_HD,
                'MAU_SO_HD_ID' : line.MAU_SO_HD_ID.id,
                'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO_ID.id,
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

    def ghi_so_thue(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_THUE_IDS:
            data = helper.Obj.inject(line, self)
            data.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                'SO_TIEN_VAT': line.TIEN_THUE_GT,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'PHAN_TRAM_VAT' : line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                'SO_TIEN_CHIU_VAT' : line.GIA_TRI_HHDV_CHUA_THUE,
                'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GT,
                'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.GIA_TRI_HHDV_CHUA_THUE,
                'NGAY_HOA_DON' : line.NGAY_HOA_DON,
                'SO_HOA_DON' : line.SO_HOA_DON,
                'MAU_SO_HOA_DON' : line.MAU_SO_HD_ID.id,
                'KY_HIEU_HOA_DON' : line.KY_HIEU_HD,
                'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO_ID.id,
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

    @api.model
    def default_get(self, fields):
        res = super(ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC, self).default_get(fields)
        loai_chung_tu = self.get_context('default_LOAI_CHUNG_TU_TINH_GIA_XUAT_KHO')
        if loai_chung_tu:
            res['LOAI_CHUNG_TU'] =loai_chung_tu
            res['DIEN_GIAI']='Xử lý chênh lệch xuất quỹ'

            thang = datetime.now().month
            res['NAM'] = datetime.now().year
            res['THANG'] = str(thang)
            res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')]).id
            res['TY_GIA'] = 1.0

        thang_pb_chi_phi_tra_truoc = self.get_context('default_THANG')
        nam_pb_chi_phi_tra_truoc= self.get_context('default_NAM')

        if thang_pb_chi_phi_tra_truoc:
            res['THANG']=thang_pb_chi_phi_tra_truoc
        if nam_pb_chi_phi_tra_truoc:
            res['NAM']=nam_pb_chi_phi_tra_truoc
        
        if thang_pb_chi_phi_tra_truoc and nam_pb_chi_phi_tra_truoc:
            res['NGAY_HACH_TOAN'] = helper.Datetime.lay_ngay_cuoi_thang(nam_pb_chi_phi_tra_truoc, thang_pb_chi_phi_tra_truoc)
            res['NGAY_CHUNG_TU'] = helper.Datetime.lay_ngay_cuoi_thang(nam_pb_chi_phi_tra_truoc, thang_pb_chi_phi_tra_truoc)

        # lấy dữ liệu kết chuyển lãi lỗ
        # if self._context:
        #     loai_chung_tu = self._context.get('default_LOAI_CHUNG_TU')
        #     if loai_chung_tu and loai_chung_tu == 4012:
        #         du_lieu_ket_chuyen = self.lay_du_ket_chuyen_lai_lo()
        #         if du_lieu_ket_chuyen:
        #             res['ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS'] = du_lieu_ket_chuyen
        #         else:
        #             res['ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS'] = []
        
        return res
    
    @api.depends('TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_XD_CHI_PHI_IDS')
    def tinh_tong_tien_phan_bo(self):
        for record in self:
            tong_tien_phan_bo = 0
            for line in record.TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_XD_CHI_PHI_IDS:
                tong_tien_phan_bo += line.SO_TIEN_PHAN_BO_TRONG_KY
        
            record.TONG_TIEN_PHAN_BO = tong_tien_phan_bo

    @api.depends('ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS')
    def tinh_tong_tien_chenh_lech(self):
        for order in self:
            tong_tien_chenh_lech_qd =0.0
            tong_tien_thue_gtgt_qd = 0.0
        
            for chi_tiet in order.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS:
                tong_tien_chenh_lech_qd += chi_tiet.SO_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qd += chi_tiet.TIEN_THUE_GTGT_QD
            
            order.update({
                'TONG_CHENH_LECH':tong_tien_chenh_lech_qd + tong_tien_thue_gtgt_qd,
            })


    def lay_du_ket_chuyen_lai_lo(self):
        arr_ket_chuyen_lai_lo = []
        record =[]
        if self.NGAY_HACH_TOAN == False:
            ngay_hach_toan = datetime.now().strftime("%Y-%m-%d")
        else:
            ngay_hach_toan = self.NGAY_HACH_TOAN
        params = {
            'NGAY_HACH_TOAN' : ngay_hach_toan,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }
        query = """

                DO LANGUAGE plpgsql $$
                DECLARE
                ngay_hach_toan    DATE := %(NGAY_HACH_TOAN)s;
                chi_nhanh_id      INTEGER := %(CHI_NHANH_ID)s;
                ngay_bat_dau      DATE;

                tu_tai_khoan      VARCHAR(20);
                den_tai_khoan     VARCHAR(20);
                ben_ket_chuyen    VARCHAR(20);
                thu_tu_ket_chuyen VARCHAR(20);
                dien_giai         VARCHAR(50);
                rec               RECORD;
                thu_tu_max        INTEGER;

                BEGIN

                SELECT value INTO ngay_bat_dau
                FROM ir_config_parameter
                WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
                FETCH FIRST 1 ROW ONLY;

                DROP TABLE IF EXISTS TMP_TAI_KHOAN_KET_CHUYEN;
                CREATE TEMP TABLE TMP_TAI_KHOAN_KET_CHUYEN
                    AS
                    SELECT
                        A."SO_TAI_KHOAN"   AS "MA_TAI_KHOAN_TU",
                        A."DON_VI"         AS "CHI_TIET_THEO_DON_VI",
                        A."KHOAN_MUC_CP"   AS "CHI_TIET_THEO_KHOAN_MUC_CP",
                        A."DOI_TUONG_THCP" AS "CHI_TIET_THEO_DOI_TUONG_THCP",
                        A."HOP_DONG_BAN"   AS "CHI_TIET_THEO_HOP_DONG_BAN",
                        AT."KET_CHUYEN_DEN_ID",
                        AT."MA_TAI_KHOAN_DEN",
                        AT."BEN_KET_CHUYEN",
                        AT."THU_TU_KET_CHUYEN",
                        AT."DIEN_GIAI"
                    FROM danh_muc_tai_khoan_ket_chuyen AS AT
                        INNER JOIN danh_muc_he_thong_tai_khoan AS A
                        ON LEFT(A."SO_TAI_KHOAN", length(AT."MA_TAI_KHOAN_TU")) = AT."MA_TAI_KHOAN_TU"
                    WHERE A."LA_TK_TONG_HOP" = FALSE AND AT.active = TRUE AND
                            "LOAI_KET_CHUYEN" = 'KET_CHUYEN_XAC_DINH_KET_QUA_KINH_DOANH';

                DROP TABLE IF EXISTS TMP_GL_TAI_KHOAN;
                CREATE TEMP TABLE TMP_GL_TAI_KHOAN (
                    "MA_TAI_KHOAN_NO"      VARCHAR(20),
                    "MA_TAI_KHOAN_CO"      VARCHAR(20),
                    "SO_TIEN_NGUYEN_TE"    FLOAT,
                    "SO_TIEN"              FLOAT,
                    "DIEN_GIAI"            VARCHAR(50),
                    "THU_TU_KET_CHUYEN"    VARCHAR(50),
                    "CHI_TIET_THEO_DON_VI" INTEGER,
                    "KHOAN_MUC_CP_ID"      INTEGER,
                    "DOI_TUONG_THCP_ID"    INTEGER,
                    "HOP_DONG_BAN_ID"      INTEGER
                );

                DROP TABLE IF EXISTS TMP_TEMP;
                CREATE TEMP TABLE TMP_TEMP (
                    "MA_TAI_KHOAN_NO"      VARCHAR(20),
                    "MA_TAI_KHOAN_CO"      VARCHAR(20),
                    "SO_TIEN_NGUYEN_TE"    FLOAT,
                    "SO_TIEN"              FLOAT,
                    "DIEN_GIAI"            VARCHAR(50),
                    "THU_TU_KET_CHUYEN"    VARCHAR(50),
                    "CHI_TIET_THEO_DON_VI" INTEGER,
                    "KHOAN_MUC_CP_ID"      INTEGER,
                    "DOI_TUONG_THCP_ID"    INTEGER,
                    "HOP_DONG_BAN_ID"      INTEGER
                );

                DROP TABLE IF EXISTS TMP_BALANCE;
                CREATE TEMP TABLE TMP_BALANCE
                    AS
                    SELECT
                        "MA_TAI_KHOAN",
                        CASE
                        WHEN "NGAY_HACH_TOAN" < ngay_bat_dau
                        THEN 1
                        ELSE 0
                        END           AS "NHO_HON_NGAY_GHI_TANG",
                        SUM("GHI_NO") AS "SO_TIEN_NO",
                        SUM("GHI_CO") AS "SO_TIEN_CO",
                        NULL          AS "DON_VI_ID",
                        NULL          AS "KHOAN_MUC_CP_ID",
                        NULL          AS "DOI_TUONG_THCP_ID",
                        NULL          AS "HOP_DONG_BAN_ID"
                    FROM so_cai_chi_tiet AS GL
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                            AND "NGAY_HACH_TOAN" <= ngay_hach_toan
                            AND GL."MA_TAI_KHOAN" IN (SELECT "MA_TAI_KHOAN_TU"
                                                    FROM TMP_TAI_KHOAN_KET_CHUYEN)
                    GROUP BY "MA_TAI_KHOAN",
                        CASE
                        WHEN "NGAY_HACH_TOAN" < ngay_bat_dau
                        THEN 1
                        ELSE 0
                        END
                    HAVING SUM("GHI_NO") <> 0
                            OR SUM("GHI_CO") <> 0;


                FOR rec IN
                SELECT
                    TAT."MA_TAI_KHOAN_TU",
                    TAT."MA_TAI_KHOAN_DEN",
                    TAT."BEN_KET_CHUYEN",
                    TAT."THU_TU_KET_CHUYEN",
                    TAT."DIEN_GIAI"
                --   INTO tu_tai_khoan, den_tai_khoan, ben_ket_chuyen, thu_tu_ket_chuyen, dien_giai
                FROM TMP_TAI_KHOAN_KET_CHUYEN AS TAT
                WHERE TAT."MA_TAI_KHOAN_TU" NOT LIKE '911%%' AND TAT."MA_TAI_KHOAN_DEN" NOT LIKE '421%%'
                ORDER BY TAT."THU_TU_KET_CHUYEN", TAT."MA_TAI_KHOAN_TU"
                LOOP
                    tu_tai_khoan := rec."MA_TAI_KHOAN_TU";
                    den_tai_khoan := rec."MA_TAI_KHOAN_DEN";
                    ben_ket_chuyen := rec."BEN_KET_CHUYEN";
                    thu_tu_ket_chuyen := rec."THU_TU_KET_CHUYEN";
                    dien_giai := rec."DIEN_GIAI";
                    --         RAISE NOTICE '%%', ben_ket_chuyen;
                    DELETE FROM TMP_TEMP;
                    IF ben_ket_chuyen = 'NO'
                    THEN
                    INSERT INTO TMP_GL_TAI_KHOAN (
                        SELECT
                        den_tai_khoan,
                        tu_tai_khoan,
                        SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) AS "SO_TIEN",
                        SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) AS "SO_TIEN_QUY_DOI",
                        dien_giai,
                        thu_tu_ket_chuyen,
                        NULL,
                        NULL,
                        NULL,
                        NULL
                        FROM TMP_BALANCE AS GL
                        WHERE GL."MA_TAI_KHOAN" = tu_tai_khoan
                        HAVING
                        SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) <> 0
                        OR SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) <> 0);
                    ELSEIF ben_ket_chuyen = 'CO'
                    THEN
                        INSERT INTO TMP_GL_TAI_KHOAN (
                        SELECT
                            den_tai_khoan,
                            tu_tai_khoan,
                            SUM(coalesce(GL."SO_TIEN_CO", 0) - coalesce(GL."SO_TIEN_NO", 0)) AS "SO_TIEN",
                            SUM(coalesce(GL."SO_TIEN_CO", 0) - coalesce(GL."SO_TIEN_NO", 0)) AS "SO_TIEN_QUY_DOI",
                            dien_giai,
                            thu_tu_ket_chuyen,
                            NULL,
                            NULL,
                            NULL,
                            NULL
                        FROM TMP_BALANCE AS GL
                        WHERE GL."MA_TAI_KHOAN" = tu_tai_khoan
                        HAVING
                            SUM(coalesce(GL."SO_TIEN_CO", 0) - coalesce(GL."SO_TIEN_NO", 0)) <> 0
                            OR SUM(coalesce(GL."SO_TIEN_CO", 0) - coalesce(GL."SO_TIEN_NO", 0)) <> 0);

                    ELSEIF ben_ket_chuyen = 'HAI_BEN'
                    THEN
                        INSERT INTO TMP_TEMP (
                                            SELECT
                                                den_tai_khoan,
                                                tu_tai_khoan,
                                                SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) AS "SO_TIEN",
                                                SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO",
                                                                                            0))                  AS "SO_TIEN_QUY_DOI",
                                                dien_giai,
                                                thu_tu_ket_chuyen,
                                                NULL,
                                                NULL,
                                                NULL,
                                                NULL
                                            FROM TMP_BALANCE AS GL
                                            WHERE GL."MA_TAI_KHOAN" = tu_tai_khoan
                                            HAVING
                                                SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) <> 0
                                                OR SUM(coalesce(GL."SO_TIEN_NO", 0) - coalesce(GL."SO_TIEN_CO", 0)) <> 0)

                                            UNION ALL

                                            SELECT
                                            den_tai_khoan,
                                            tu_tai_khoan,
                                            SUM(coalesce(TGA."SO_TIEN_NGUYEN_TE", 0)),
                                            SUM(coalesce(TGA."SO_TIEN", 0)),
                                            dien_giai,
                                            thu_tu_ket_chuyen,
                                            NULL :: INT,
                                            NULL :: INT,
                                            NULL :: INT,
                                            NULL :: INT
                                            FROM TMP_GL_TAI_KHOAN AS TGA
                                            WHERE TGA."MA_TAI_KHOAN_NO" = tu_tai_khoan
                                                AND TGA."THU_TU_KET_CHUYEN" < thu_tu_ket_chuyen
                                                AND TGA."SO_TIEN_NGUYEN_TE" > 0
                                            HAVING
                                            SUM(coalesce(TGA."SO_TIEN_NGUYEN_TE", 0)) <> 0
                                            OR SUM(coalesce(TGA."SO_TIEN", 0)) <> 0

                                            UNION ALL

                                            SELECT
                                            den_tai_khoan,
                                            tu_tai_khoan,
                                            (-1) * SUM(COALESCE(TGA."SO_TIEN_NGUYEN_TE", 0)),
                                            (-1) * SUM(COALESCE(TGA."SO_TIEN", 0)),
                                            dien_giai,
                                            thu_tu_ket_chuyen,
                                            NULL,
                                            NULL,
                                            NULL,
                                            NULL
                                            FROM TMP_GL_TAI_KHOAN AS TGA
                                            WHERE TGA."MA_TAI_KHOAN_CO" = tu_tai_khoan
                                                AND TGA."THU_TU_KET_CHUYEN" < thu_tu_ket_chuyen
                                                AND TGA."SO_TIEN_NGUYEN_TE" > 0
                                            HAVING
                                            SUM(COALESCE(TGA."SO_TIEN_NGUYEN_TE", 0)) <> 0
                                            OR SUM(COALESCE(TGA."SO_TIEN", 0)) <> 0;
                        /*
                        Insert dữ liệu vào bảng kết quả trả về lấy từ bảng @Temp
                        1. Sum số tiền trên bảng Temp
                            1.1 Nếu số tiền < 0 thì TK Nợ = TK Dến, TK Có = TK Từ, Số tiền = abs(Sum(Amount))
                            1.2 Nếu số tiền > 0 thì TK Nợ = TK Từ, TK Có = TK Đến, Số tiền = Sum(Amount)
                        */
                        INSERT INTO TMP_GL_TAI_KHOAN (
                        SELECT
                            (CASE WHEN SUM("SO_TIEN_NGUYEN_TE") < 0
                            THEN T."MA_TAI_KHOAN_CO"
                            ELSE T."MA_TAI_KHOAN_NO"
                            END),
                            (CASE WHEN SUM(T."SO_TIEN_NGUYEN_TE") < 0
                            THEN T."MA_TAI_KHOAN_NO"
                            ELSE T."MA_TAI_KHOAN_CO"
                            END),
                            ABS(SUM(T."SO_TIEN_NGUYEN_TE")),
                            ABS(SUM(T."SO_TIEN")),
                            T."DIEN_GIAI",
                            T."THU_TU_KET_CHUYEN",
                            T."CHI_TIET_THEO_DON_VI",
                            T."KHOAN_MUC_CP_ID",
                            T."DOI_TUONG_THCP_ID",
                            T."HOP_DONG_BAN_ID"
                        FROM TMP_TEMP AS T
                        GROUP BY
                            T."MA_TAI_KHOAN_NO",
                            T."MA_TAI_KHOAN_CO",
                            T."DIEN_GIAI",
                            T."THU_TU_KET_CHUYEN",
                            T."CHI_TIET_THEO_DON_VI",
                            T."KHOAN_MUC_CP_ID",
                            T."DOI_TUONG_THCP_ID",
                            T."HOP_DONG_BAN_ID");
                    END IF;
                END LOOP;

                SELECT MAX("THU_TU_KET_CHUYEN")
                INTO thu_tu_max
                FROM TMP_GL_TAI_KHOAN;

                DELETE FROM TMP_TEMP;

                DROP TABLE IF EXISTS TMP_SO_DU_TAI_KOAN_911;
                CREATE TEMP TABLE TMP_SO_DU_TAI_KOAN_911 (
                    "MA_TAI_KHOAN_911"         VARCHAR(20),
                    "TONG_SO_DU_TAI_KHOAN_911" FLOAT
                );

                INSERT INTO TMP_SO_DU_TAI_KOAN_911 (
                    SELECT
                    GL."MA_TAI_KHOAN",
                    coalesce(SUM(GL."SO_TIEN_NO" - GL."SO_TIEN_CO"), 0)
                    FROM TMP_BALANCE AS GL
                    WHERE "MA_TAI_KHOAN" LIKE '911%%'
                    GROUP BY GL."MA_TAI_KHOAN"
                );
                -- Lấy số kết chuyển từ các tài khoản sang 911
                DROP TABLE IF EXISTS TMP_SO_TIEN_HIEN_TAI_TAI_KOAN_911;
                CREATE TEMP TABLE TMP_SO_TIEN_HIEN_TAI_TAI_KOAN_911 (
                    "MA_TAI_KHOAN_911"              VARCHAR(20),
                    "SO_TIEN_HIEN_TAI_TAI_KOAN_911" FLOAT
                );

                INSERT INTO TMP_SO_TIEN_HIEN_TAI_TAI_KOAN_911 (
                    SELECT
                    CASE WHEN T."MA_TAI_KHOAN_NO" LIKE '911%%'
                        THEN T."MA_TAI_KHOAN_NO"
                    ELSE T."MA_TAI_KHOAN_CO" END,
                    SUM(CASE WHEN "MA_TAI_KHOAN_CO" LIKE '911%%'
                        THEN "SO_TIEN"
                        ELSE -"SO_TIEN" END)
                    FROM TMP_GL_TAI_KHOAN T
                    WHERE T."MA_TAI_KHOAN_NO" LIKE '911%%' OR T."MA_TAI_KHOAN_CO" LIKE '911%%'
                    GROUP BY CASE WHEN T."MA_TAI_KHOAN_NO" LIKE '911%%'
                    THEN T."MA_TAI_KHOAN_NO"
                            ELSE T."MA_TAI_KHOAN_CO" END
                );

                -- Thêm dòng kết chuyển từ 911 sang 421 vào kết quả trả ra
                INSERT INTO TMP_GL_TAI_KHOAN (
                    SELECT
                    CASE WHEN coalesce(C."SO_TIEN_HIEN_TAI_TAI_KOAN_911", 0) - coalesce(D."TONG_SO_DU_TAI_KHOAN_911", 0) > 0
                        THEN TAT."MA_TAI_KHOAN_TU"
                    ELSE TAT."MA_TAI_KHOAN_DEN"
                    END,
                    CASE WHEN coalesce(C."SO_TIEN_HIEN_TAI_TAI_KOAN_911", 0) - coalesce(D."TONG_SO_DU_TAI_KHOAN_911", 0) > 0
                        THEN TAT."MA_TAI_KHOAN_DEN"
                    ELSE TAT."MA_TAI_KHOAN_TU"
                    END,
                    ABS(coalesce(C."SO_TIEN_HIEN_TAI_TAI_KOAN_911", 0) - coalesce(D."TONG_SO_DU_TAI_KHOAN_911", 0)),
                    ABS(coalesce(C."SO_TIEN_HIEN_TAI_TAI_KOAN_911", 0) - coalesce(D."TONG_SO_DU_TAI_KHOAN_911", 0)),
                    TAT."DIEN_GIAI",
                    TAT."THU_TU_KET_CHUYEN",
                    NULL,
                    NULL,
                    NULL,
                    NULL
                    FROM TMP_TAI_KHOAN_KET_CHUYEN TAT
                    LEFT JOIN TMP_SO_TIEN_HIEN_TAI_TAI_KOAN_911 C ON TAT."MA_TAI_KHOAN_TU" = C."MA_TAI_KHOAN_911"
                    LEFT JOIN TMP_SO_DU_TAI_KOAN_911 D ON TAT."MA_TAI_KHOAN_TU" = D."MA_TAI_KHOAN_911"
                    WHERE TAT."MA_TAI_KHOAN_TU" LIKE '911%%' --AND TAT.ToAccount LIKE N'421%%'
                );

                DROP TABLE IF EXISTS TMP_KET_QUA;
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                    SELECT
                        CASE WHEN coalesce(AD."LA_TK_TONG_HOP", FALSE) = FALSE
                        THEN AD.id
                        ELSE NULL END AS "TK_NO_ID",
                        CASE WHEN coalesce(AD."LA_TK_TONG_HOP", FALSE) = FALSE
                        THEN TGLA."MA_TAI_KHOAN_NO"
                        ELSE NULL END AS "MA_TAI_KHOAN_NO",

                        CASE WHEN coalesce(AC."LA_TK_TONG_HOP", FALSE) = FALSE
                        THEN AC.id
                        ELSE NULL END AS "TK_CO_ID",
                        CASE WHEN coalesce(AC."LA_TK_TONG_HOP", FALSE) = FALSE
                        THEN TGLA."MA_TAI_KHOAN_CO"
                        ELSE NULL END AS "MA_TAI_KHOAN_CO",
                        TGLA."SO_TIEN_NGUYEN_TE",
                        TGLA."SO_TIEN",
                        TGLA."DIEN_GIAI",
                        TGLA."THU_TU_KET_CHUYEN",
                        TGLA."CHI_TIET_THEO_DON_VI",
                        TGLA."KHOAN_MUC_CP_ID",
                        TGLA."DOI_TUONG_THCP_ID",
                        TGLA."HOP_DONG_BAN_ID"
                    FROM TMP_GL_TAI_KHOAN AS TGLA
                        LEFT JOIN danh_muc_he_thong_tai_khoan AS AD ON TGLA."MA_TAI_KHOAN_NO" = AD."SO_TAI_KHOAN"
                        LEFT JOIN danh_muc_he_thong_tai_khoan AS AC ON TGLA."MA_TAI_KHOAN_CO" = AC."SO_TAI_KHOAN"
                    WHERE "SO_TIEN" > 0
                    ORDER BY "THU_TU_KET_CHUYEN", "MA_TAI_KHOAN_NO";

                END $$;

                SELECT *
                FROM TMP_KET_QUA;

        """  
        record = self.execute(query, params)
        for ket_chuyen in record:
            arr_ket_chuyen_lai_lo += [(0, 0, {
                'DIEN_GIAI' : ket_chuyen.get('DIEN_GIAI'),
                'TK_NO_ID': ket_chuyen.get('TK_NO_ID'),
                'TK_CO_ID': ket_chuyen.get('TK_CO_ID'),
                'SO_TIEN_QUY_DOI': ket_chuyen.get('SO_TIEN'),
                'SO_TIEN': ket_chuyen.get('SO_TIEN_NGUYEN_TE'),
                })]
        return arr_ket_chuyen_lai_lo

    @api.multi
    def get_formview_id(self, access_uid=None):
        
        if self.LOAI_CHUNG_TU == 4012:
            return self.env.ref('tong_hop.view_account_ex_ket_chuyen_lai_lo_master_form').id
        elif self.LOAI_CHUNG_TU == 4020:
            return self.env.ref('tong_hop.view_tong_hop_phan_bo_chi_phi_tra_truoc_form').id
        else:
            return self.env.ref('tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form').id

        return super(ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC, self).get_formview_id(access_uid)