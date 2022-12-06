# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

import base64
import json
import logging
import requests

from odoo import api, models, fields, helper, tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.http import request

_logger = logging.getLogger(__name__)

TIMEOUT = 60
DICT_HTTT = {
    'TIEN_MAT': 1,
    'CHUYEN_KHOAN': 2,
    'TM/CK': 3,
}
DICT_LOAI_VTHH = {
    '0': 0,
    '1': 3,
    '2': 1,
    '3': 3,
    '4': 3,
}

class SALE_EX_HOA_DON_BAN_HANG(models.Model):
    _name = 'sale.ex.hoa.don.ban.hang'
    _description = 'Hóa đơn bán hàng'
    _inherit = ['mail.thread']
    _order = "NGAY_HOA_DON desc, MAU_SO_HD_ID desc, KY_HIEU_HD desc, SO_HOA_DON desc"

    CHUNG_TU_BAN_HANG = fields.Many2one('sale.document', string='Chứng từ BH', help='Chứng từ bán hàng')# trường này chỉ hiển thị trên form chứ không được dùng nếu dùng thì dùng trường  SALE_DOCUMENT_IDS
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    HOA_DON = fields.Selection([('BAN_HANG_HOA_DICH_VU_TRONG_NUOC', '1. Bán hàng hóa dịch vụ trong nước'), ('BAN_HANG_XUAT_KHAU', '2. Bán hàng xuất khẩu'), ('BAN_HANG_DAI_LY_BAN_DUNG_GIA', '3. Bán hàng đại lý bán đúng giá'), ('BAN_HANG_UY_THAC_XUAT_KHAU', ' 4. Bán hàng ủy thác xuất khẩu '), ], string='Hóa đơn', help='Hóa đơn',default='BAN_HANG_HOA_DICH_VU_TRONG_NUOC',required=True)
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    partner_bank_id = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='TK ngân hàng', help='Tài khoản ngân hàng')
    HINH_THUC_TT = fields.Selection([('TIEN_MAT', 'Tiền mặt'),('CHUYEN_KHOAN', 'Chuyển khoản'),('TM/CK', 'TM/CK') ], string='Hình thức TT', help='Hình thức thanh toán',default='TM/CK')
    NGUOI_MUA_HANG = fields.Char(string='Người mua hàng', help='Người mua hàng')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='NV bán hàng', help='Nhân viên bán hàng')
    DA_HACH_TOAN = fields.Boolean(string='Đã hạch toán', help='Đã hạch toán')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hóa đơn')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now)
    name = fields.Char(string='Số hóa đơn',related='SO_HOA_DON')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu',readonly = True)
    SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS = fields.One2many('sale.ex.chi.tiet.hoa.don.ban.hang', 'HOA_DON_ID_ID', string='chi tiết hóa đơn bán hàng', copy=True)

    #Trường này dùng để tính toán chứng từ bán hàng , ko hiển thị trên view VŨ
    SALE_DOCUMENT_LINE_IDS = fields.One2many('sale.document.line', 'HOA_DON_ID', string='document line',required=True, copy=True)
    SOURCE_ID = fields.Reference(selection=[
        ('sale.document', 'Chứng từ bán hàng'),
        ('sale.ex.giam.gia.hang.ban', 'Chứng từ giảm giá hàng bán'),
        ('purchase.ex.tra.lai.hang.mua', 'Chứng từ trả lại hàng mua'),
        ], string='Lập từ')
    MA_HANG_ID  = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng',compute='tinh_tong_tien' , store=True, currency_field='currency_id')    
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',compute='tinh_tong_tien' , store=True, currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng',compute='tinh_tong_tien' , store=True, currency_field='currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',compute='tinh_tong_tien' , store=True, currency_field='currency_id')
    TONG_TIEN_HANG_QD = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng QĐ',compute='tinh_tong_tien' , store=True, currency_field='base_currency_id')    
    TIEN_CHIET_KHAU_QD = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu QĐ',compute='tinh_tong_tien' , store=True, currency_field='base_currency_id')
    TIEN_THUE_GTGT_QD = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng QĐ',compute='tinh_tong_tien' , store=True, currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN_QD = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán QĐ',compute='tinh_tong_tien_qd' , store=True, currency_field='base_currency_id')
    IN_KEM_BANG_KE = fields.Boolean(string='In kèm bảng kê', help='In kèm bảng kê')
    SO = fields.Char(string='Số', help='Số')
    NGAY_BANG_KE = fields.Date(string='Ngày', help='Ngày')
    TEN_MAT_HANG_CHUNG = fields.Char(string='Tên mặt hàng chung', help='Tên mặt hàng chung')
    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng')
    NGAY_HOP_DONG = fields.Date(string='Ngày hợp đồng', help='Ngày hợp đồng')
    DIA_DIEM_NHAN_HANG = fields.Char(string='Địa điểm nhận hàng', help='Địa điểm nhận hàng')
    DIA_DIEM_GIAO_HANG = fields.Char(string='Địa điểm giao hàng', help='Địa điểm giao hàng')
    SO_VAN_DON = fields.Char(string='Số vận đơn', help='Số vận đơn')
    SO_CONTAINER = fields.Char(string='Số container', help='Số container')
    DV_VAN_CHUYEN = fields.Char(string='Đơn vị vận chuyển', help='Đơn vị vận chuyển')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',readonly=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',store=True , compute='set_loai_chung_tu_hoa_don_ban_hang')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_TEXT = fields.Char(string='Loại', help='Loại',compute='thay_doi_loai_text',store=True)
    DA_HACH_TOAN_TEXT = fields.Char(string='Đã hạch toán', help='Đã hạch toán',compute='thay_doi_hach_toan_text',store=True)
    SALE_DOCUMENT_IDS = fields.Many2many('sale.document', 'sale_ex_document_invoice_rel', string='Chứng từ BH', help='Chứng từ bán hàng', domain=[('DA_LAP_HOA_DON', '!=', True)])
    LAP_KEM_HOA_DON = fields.Boolean(string='Lập kèm hóa đơn', help='Lập kèm hóa đơn', compute='_compute_LAP_KEM_HOA_DON', store=True)
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')

    _sql_constraints = [
	('SO_HOA_DON_uniq', 'unique ("MAU_SO_HD_ID","KY_HIEU_HD","SO_HOA_DON")', 'Mẫu số HĐ, ký hiệu HĐ và số hóa đơn này đã tồn tại, vui lòng nhập số hóa đơn khác!'),
	]

    LOAI_CHUNG_TU_DIEU_CHINH = fields.Integer(string='Loại chứng điều chỉnh', help='AdjustRefType')

    @api.model
    def validate_so_hoa_don(self):
        if (self.KY_HIEU_HD or self.MAU_SO_HD_ID) and not self.SO_HOA_DON:
            raise UserError("<Số hóa đơn> không được bỏ trống!")
        if self.SO_HOA_DON or self.KY_HIEU_HD or self.MAU_SO_HD_ID:
            domain = [
                ('id','!=', self.id),
                ('SO_HOA_DON','=', self.SO_HOA_DON),
                ('KY_HIEU_HD','=', self.KY_HIEU_HD),
                ('MAU_SO_HD_ID','=', self.MAU_SO_HD_ID.id),]
            if self.search(domain, limit=1):
                err_msg = ''
                if self.MAU_SO_HD_ID:
                    err_msg += 'Mẫu số HĐ <' + str(self.MAU_SO_HD_ID.name) + '>'
                if self.KY_HIEU_HD:
                    if err_msg:
                        err_msg += ', '
                    err_msg += 'Ký hiệu HĐ <' + str(self.KY_HIEU_HD) + '>'
                if self.SO_HOA_DON:
                    if err_msg:
                        err_msg += ', '
                    err_msg += 'Số hóa đơn <' + str(self.SO_HOA_DON) + '>'
                err_msg += ' đã tồn tại. Vui lòng nhập số khác!'
                raise ValidationError(err_msg)

    @api.model
    def create(self, values):
        result = super(SALE_EX_HOA_DON_BAN_HANG, self).create(values)
        # result.validate_so_hoa_don()
        if not result.SOURCE_ID:
            if result.SALE_DOCUMENT_IDS:
                for ctbh in result.SALE_DOCUMENT_IDS:
                    ctbh.write({'SO_HOA_DON': result.SO_HOA_DON,
                                'NGAY_HOA_DON': result.NGAY_HOA_DON,
                                'DA_LAP_HOA_DON': True,})
        if result.SALE_DOCUMENT_IDS:
            for ct in result.SALE_DOCUMENT_IDS:
                if ct.state == 'da_ghi_so':
                    ct.action_bo_ghi_so(None)
                    ct.action_ghi_so()
        return result

    
    @api.multi
    def write(self, values):
        result = super(SALE_EX_HOA_DON_BAN_HANG, self).write(values)
        need_validate = helper.List.element_in_dict(['SO_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID'], values)
        for record in self:
            # if need_validate:
            #     record.validate_so_hoa_don()
            if not record.SOURCE_ID:
                if record.SALE_DOCUMENT_IDS:
                    for ctbh in record.SALE_DOCUMENT_IDS:
                        ctbh.write({'SO_HOA_DON': record.SO_HOA_DON,
                                    'NGAY_HOA_DON': record.NGAY_HOA_DON,
                                    'DA_LAP_HOA_DON': True,})
            if values.get('SO_HOA_DON') or values.get('NGAY_HOA_DON'):
                if record.SALE_DOCUMENT_IDS:
                    for ct in record.SALE_DOCUMENT_IDS:
                        if ct.state == 'da_ghi_so':
                            ct.action_bo_ghi_so(None)
                            ct.action_ghi_so()
        return result

    @api.multi
    def unlink(self):
        chung_tu_bh = ''
        arr_chung_tu_ban_hang = []
        for record in self:
            if record.SALE_DOCUMENT_IDS:
                for ctbh in record.SALE_DOCUMENT_IDS:
                    arr_chung_tu_ban_hang.append(ctbh.id)
                    # ctbh.write({'SO_HOA_DON': False,
                    #             'NGAY_HOA_DON': False,
                    #             'DA_LAP_HOA_DON': False,})
            chung_tu_bh = record.SALE_DOCUMENT_IDS
        result = super(SALE_EX_HOA_DON_BAN_HANG, self).unlink()
        if arr_chung_tu_ban_hang:
            for id_ctbh in arr_chung_tu_ban_hang:
                ct_bt_ids = self.env['sale.document'].search([('id', '=', id_ctbh)])
                if ct_bt_ids:
                    for ctbh in ct_bt_ids:
                        ctbh.write({'SO_HOA_DON': False,
                                    'NGAY_HOA_DON': False,
                                    'DA_LAP_HOA_DON': False,})
        if chung_tu_bh != '':
            for ct in chung_tu_bh:
                ct.action_bo_ghi_so(None)
                ct.action_ghi_so()
        return result
    
    
    # @api.onchange('SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS')
    # def _onchange_SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS(self):
    #     if self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
    #         chung_tu_ban_hang_ids = []
    #         for line in self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
    #             chung_tu_ban_hang_ids.append(line.CHUNG_TU_BAN_HANG_ID.id)
    #         self.SALE_DOCUMENT_IDS = tuple(chung_tu_ban_hang_ids)
    
    @api.onchange('SALE_DOCUMENT_IDS')
    def _onchange_SALE_DOCUMENT_IDS(self):
        doi_tuong = False
        if not self.SALE_DOCUMENT_IDS:
            self.DOI_TUONG_ID = False
            self.TEN_KHACH_HANG = ''
        self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS = []
        for sale_document in self.SALE_DOCUMENT_IDS:
            if not doi_tuong:
                doi_tuong = sale_document.DOI_TUONG_ID.id
            elif doi_tuong != sale_document.DOI_TUONG_ID.id:
                raise ValidationError('Các chứng từ bán hàng đã chọn không cùng khách hàng. Vui lòng chọn lại!')
            self.DOI_TUONG_ID = sale_document.DOI_TUONG_ID.id
            self.TEN_KHACH_HANG = sale_document.TEN_KHACH_HANG
            for ct_bh in sale_document.SALE_DOCUMENT_LINE_IDS:
                new_line = {
                    'MA_HANG_ID': ct_bh.MA_HANG_ID.id,
                    'TEN_HANG': ct_bh.TEN_HANG,
                    'DVT_ID': ct_bh.DVT_ID.id,
                    'SO_LUONG': ct_bh.SO_LUONG,
                    'DON_GIA': ct_bh.DON_GIA,
                    'THANH_TIEN': ct_bh.THANH_TIEN,
                    'THANH_TIEN_QUY_DOI': ct_bh.THANH_TIEN_QUY_DOI,
                    'TY_LE_CK': ct_bh.TY_LE_CK,
                    'TIEN_CHIET_KHAU': ct_bh.TIEN_CHIET_KHAU,
                    'TIEN_CHIET_KHAU_QUY_DOI': ct_bh.TIEN_CK_QUY_DOI,
                    'THUE_GTGT': ct_bh.THUE_GTGT_ID.id,
                    'TIEN_THUE_GTGT': ct_bh.TIEN_THUE_GTGT,
                    'TIEN_THUE_GTGT_QUY_DOI': ct_bh.TIEN_THUE_GTGT_QUY_DOI,
                    'CHUNG_TU_BAN_HANG_ID': sale_document.id
                }
                self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS += self.env['sale.ex.chi.tiet.hoa.don.ban.hang'].new(new_line)

    #Mạnh thêm hàm để lấy dữ liệu khi thay đổi chọn chứng từ bán hàng
    def lay_du_lieu_chung_tu_ban_hang(self, args):
        new_line =[]
        chung_tu_ban_hang_id = args.get('chung_tu_ban_hang_id')
        thong_tin_chung_tu_master = self.env['sale.document'].search([('id', '=', chung_tu_ban_hang_id)],limit=1)
        doi_tuong_id = thong_tin_chung_tu_master['DOI_TUONG_ID'].id
        ma_doi_tuong = thong_tin_chung_tu_master['DOI_TUONG_ID'].MA
        ten_khach_hang = thong_tin_chung_tu_master['TEN_KHACH_HANG']
        danh_sach_chung_tu_ban_hang = self.env['sale.document.line'].search([('SALE_DOCUMENT_ID', '=', chung_tu_ban_hang_id)])
        if danh_sach_chung_tu_ban_hang:
            for ct_bh in danh_sach_chung_tu_ban_hang:
                new_line += [(0,0,{
                    'MA_HANG_ID': [ct_bh['MA_HANG_ID'].id,ct_bh['MA_HANG_ID'].MA],
                    'TEN_HANG': ct_bh['TEN_HANG'],
                    'DVT_ID': [ct_bh['DVT_ID'].id,ct_bh['DVT_ID'].name],
                    'SO_LUONG': ct_bh['SO_LUONG'],
                    'DON_GIA': ct_bh['DON_GIA'],
                    'THANH_TIEN': ct_bh['THANH_TIEN'],
                    'THANH_TIEN_QUY_DOI': ct_bh['THANH_TIEN_QUY_DOI'],
                    'TY_LE_CK': ct_bh['TY_LE_CK'],
                    'TIEN_CHIET_KHAU': ct_bh['TIEN_CHIET_KHAU'],
                    'TIEN_CHIET_KHAU_QUY_DOI': ct_bh['TIEN_CK_QUY_DOI'],
                    'THUE_GTGT': [ct_bh['THUE_GTGT_ID'].id,ct_bh['THUE_GTGT_ID'].name],
                    'TIEN_THUE_GTGT': ct_bh['TIEN_THUE_GTGT'],
                    'TIEN_THUE_GTGT_QUY_DOI': ct_bh['TIEN_THUE_GTGT_QUY_DOI'],
                    'CHUNG_TU_BAN_HANG_ID': [ct_bh['SALE_DOCUMENT_ID'].id,ct_bh['THUE_GTGT_ID'].name],
                    })]
        return {'SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS': new_line,
                'DOI_TUONG_ID': [doi_tuong_id,ma_doi_tuong],
                'TEN_KHACH_HANG': ten_khach_hang,}

    
    @api.multi
    @api.depends('SOURCE_ID')
    def _compute_LAP_KEM_HOA_DON(self):
        for record in self:
            record.LAP_KEM_HOA_DON = not not record.SOURCE_ID
       

    @api.depends('HOA_DON')
    def set_loai_chung_tu_hoa_don_ban_hang(self):
        for record in self: 
            if record.HOA_DON=='BAN_HANG_HOA_DICH_VU_TRONG_NUOC':
                record.LOAI_CHUNG_TU = 3560
            elif record.HOA_DON=='BAN_HANG_XUAT_KHAU':
                record.LOAI_CHUNG_TU = 3561
            elif record.HOA_DON=='BAN_HANG_DAI_LY_BAN_DUNG_GIA':
                record.LOAI_CHUNG_TU = 3562
            else:
                record.LOAI_CHUNG_TU = 3563

    @api.onchange('DOI_TUONG_ID')
    def adnc(self):
        self.TEN_KHACH_HANG = self.DOI_TUONG_ID.HO_VA_TEN
        self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
        self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
        if self.DOI_TUONG_ID.DANH_MUC_DOI_TUONG_CHI_TIET_IDS:
            self.partner_bank_id = self.DOI_TUONG_ID.DANH_MUC_DOI_TUONG_CHI_TIET_IDS[0]
        else:
            self.partner_bank_id = False
        if self.DOI_TUONG_ID.company_type=='person':
            self.NGUOI_MUA_HANG = self.DOI_TUONG_ID.HO_VA_TEN
        else:
            self.NGUOI_MUA_HANG =''

    @api.depends('TONG_TIEN_THANH_TOAN','TY_GIA')
    def tinh_tong_tien_qd(self):
        for order in self:
            order.TONG_TIEN_THANH_TOAN_QD = order.TONG_TIEN_THANH_TOAN * order.TY_GIA

    @api.depends('SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS','SALE_DOCUMENT_LINE_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien_hang = tong_tien_thue_gtgt = tong_tien_chiet_khau = tong_tien_thanh_toan =0.0
            tong_tien_hang_qđ = tong_tien_thue_gtgt_qđ = tong_tien_chiet_khau_qđ = tong_tien_thanh_toan_qđ =0.0
            for line in order.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
                tong_tien_hang += line.THANH_TIEN
                tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
                tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt - tong_tien_chiet_khau

                tong_tien_hang_qđ += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qđ += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_chiet_khau_qđ += line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_thanh_toan_qđ = tong_tien_hang_qđ + tong_tien_thue_gtgt_qđ - tong_tien_chiet_khau_qđ
            

            for line in order.SALE_DOCUMENT_LINE_IDS:
                tong_tien_hang += line.THANH_TIEN
                tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
                tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
                tong_tien_thanh_toan = tong_tien_hang + tong_tien_thue_gtgt - tong_tien_chiet_khau

                tong_tien_hang_qđ += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_qđ += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_chiet_khau_qđ += line.TIEN_CK_QUY_DOI
                tong_tien_thanh_toan_qđ = tong_tien_hang_qđ + tong_tien_thue_gtgt_qđ - tong_tien_chiet_khau_qđ
            order.update({
                'TONG_TIEN_HANG': tong_tien_hang,
                'TIEN_THUE_GTGT': tong_tien_thue_gtgt,
                'TIEN_CHIET_KHAU': tong_tien_chiet_khau,
                'TONG_TIEN_THANH_TOAN': tong_tien_thanh_toan,

                'TONG_TIEN_HANG_QD': tong_tien_hang_qđ,
                'TIEN_THUE_GTGT_QD': tong_tien_thue_gtgt_qđ,
                'TIEN_CHIET_KHAU_QD': tong_tien_chiet_khau_qđ,
                # 'TONG_TIEN_THANH_TOAN_QD': tong_tien_thanh_toan_qđ,
            })


    @api.depends('LOAI_CHUNG_TU')
    def thay_doi_loai_text(self):
        for record in self:
            loai_text=''
            ref_type = record.env['danh.muc.reftype'].search([('REFTYPE', '=', record.LOAI_CHUNG_TU)],limit=1)
            if ref_type:
                loai_text = ref_type.REFTYPENAME
            record.LOAI_TEXT = loai_text

    @api.depends('DA_HACH_TOAN')
    def thay_doi_hach_toan_text(self):
        for record in self:
            if record.DA_HACH_TOAN:
                record.DA_HACH_TOAN_TEXT = 'Đã hạch toán'
            else:
                record.DA_HACH_TOAN_TEXT = 'Chưa hạch toán'

           
    @api.onchange('currency_id')
    def update_thaydoiIsTy_gia_tien(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False   

        
    @api.model
    def default_get(self, fields):
        rec = super(SALE_EX_HOA_DON_BAN_HANG, self).default_get(fields)
        rec['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')]).id
        return rec

    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        for line in self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
            line.tinh_tien_quy_doi()

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_thue_tu_ghi()
        self.write({'state':'da_ghi_so'})


    def ghi_so_thue(self):
        line_ids = []
        thu_tu = 0
        if self.SALE_DOCUMENT_IDS:
            if self.SOURCE_ID:
                for chung_tu_ban_hang in self.SALE_DOCUMENT_IDS:
                    chung_tu_ban_hang_chi_tiet_ids = chung_tu_ban_hang.SALE_DOCUMENT_LINE_IDS
                    if chung_tu_ban_hang_chi_tiet_ids:
                        for line in chung_tu_ban_hang_chi_tiet_ids:
                            data = helper.Obj.inject(line, self)
                            data.update({
                                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                                # 'TK_VAT_ID': line.TK_THUE_GTGT_ID.id if chung_tu_mua_hang.LOAI_CHUNG_TU_MH != 'nhap_khau_nhap_kho' else line.TK_DU_THUE_GTGT_ID.id,
                                'TK_VAT_ID': line.TK_THUE_GTGT_ID.id if self.SOURCE_ID else None,
                                'PHAN_TRAM_VAT': line.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.THUE_GTGT_ID else None,
                                'SO_TIEN_VAT': line.TIEN_THUE_GTGT_QUY_DOI,
                                'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                                'SO_TIEN_CHIU_VAT': line.THANH_TIEN_QUY_DOI - line.TIEN_CK_QUY_DOI,
                                'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                                'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                                # 'DOI_TUONG_ID' : line.DOI_TUONG_ID.id,
                                # 'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_ID.id,
                                'SO_CHUNG_TU' : chung_tu_ban_hang.SO_CHUNG_TU,
                                'DIEN_GIAI' : line.TEN_HANG,
                                'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                                'SO_HOA_DON' : self.SO_HOA_DON, 
                                'NGAY_CHUNG_TU' : self.NGAY_HOA_DON,
                                'NGAY_HACH_TOAN' : self.NGAY_HOA_DON,
                                'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                                'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                                'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE
                            })
                            line_ids += [(0,0,data)]
                            thu_tu += 1
            else:
                for chung_tu_ban_hang in self.SALE_DOCUMENT_IDS:
                    for line in self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
                        data = helper.Obj.inject(line, self)
                        data.update({
                            'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                            'THU_TU_TRONG_CHUNG_TU': thu_tu,
                            # 'TK_VAT_ID': line.TK_THUE_GTGT_ID.id if chung_tu_mua_hang.LOAI_CHUNG_TU_MH != 'nhap_khau_nhap_kho' else line.TK_DU_THUE_GTGT_ID.id,
                            # 'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                            'PHAN_TRAM_VAT': line.THUE_GTGT.PHAN_TRAM_THUE_GTGT if line.THUE_GTGT else None,
                            'SO_TIEN_VAT': line.TIEN_THUE_GTGT_QUY_DOI,
                            'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                            'SO_TIEN_CHIU_VAT': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                            'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                            # 'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                            # 'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_ID.id,
                            'SO_CHUNG_TU' : chung_tu_ban_hang.SO_CHUNG_TU,
                            'DIEN_GIAI' : line.TEN_HANG,
                            'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                            'SO_HOA_DON' : self.SO_HOA_DON, 
                            'NGAY_CHUNG_TU' : self.NGAY_HOA_DON,
                            'NGAY_HACH_TOAN' : self.NGAY_HOA_DON,
                            'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                            'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                            'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE
                        })
                        line_ids += [(0,0,data)]
                        thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_HOA_DON,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True


    def ghi_so_thue_tu_ghi(self):
        line_ids = []
        thu_tu = 0
        if self.SOURCE_ID == False:
            # if self.SALE_DOCUMENT_IDS:
            # for chung_tu_ban_hang in self.SALE_DOCUMENT_IDS:
            for line in self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
                data = helper.Obj.inject(line, self)
                data.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    # 'TK_VAT_ID': line.TK_THUE_GTGT_ID.id if chung_tu_mua_hang.LOAI_CHUNG_TU_MH != 'nhap_khau_nhap_kho' else line.TK_DU_THUE_GTGT_ID.id,
                    # 'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                    'PHAN_TRAM_VAT': line.THUE_GTGT.PHAN_TRAM_THUE_GTGT if line.THUE_GTGT else None,
                    'SO_TIEN_VAT': line.TIEN_THUE_GTGT_QUY_DOI,
                    'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'SO_TIEN_CHIU_VAT': line.THANH_TIEN_QUY_DOI - line.TIEN_CHIET_KHAU_QUY_DOI,
                    'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.THANH_TIEN - line.TIEN_CHIET_KHAU,
                    # 'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    # 'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_ID.id,
                    # 'SO_CHUNG_TU' : chung_tu_ban_hang.SO_CHUNG_TU,
                    'DIEN_GIAI' : line.TEN_HANG,
                    'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                    'SO_HOA_DON' : self.SO_HOA_DON, 
                    'NGAY_CHUNG_TU' : self.NGAY_HOA_DON,
                    'NGAY_HACH_TOAN' : self.NGAY_HOA_DON,
                    'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                    'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                    'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE
                })
                line_ids += [(0,0,data)]
                thu_tu += 1
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_HOA_DON,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True


    def ghi_so_thue_tu_tra_lai_hang_mua(self):
        line_ids = []
        thu_tu = 0
        if self.SOURCE_ID:
            tra_lai_hang_mua = self.env['purchase.ex.tra.lai.hang.mua'].search([('id', '=', self.SOURCE_ID.id)])
            if tra_lai_hang_mua:
                for line in tra_lai_hang_mua.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                    data = helper.Obj.inject(line, self)
                    data.update({
                        'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                        'THU_TU_TRONG_CHUNG_TU': thu_tu,
                        'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                        'PHAN_TRAM_VAT': line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.PHAN_TRAM_THUE_GTGT_ID else None,
                        'SO_TIEN_VAT': -1*line.TIEN_THUE_GTGT_QUY_DOI,
                        'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                        'SO_TIEN_CHIU_VAT': -1*line.THANH_TIEN_QUY_DOI,
                        'SO_TIEN_CHIU_VAT_NGUYEN_TE' : -1*line.THANH_TIEN,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'SO_CHUNG_TU' : tra_lai_hang_mua.SO_CHUNG_TU,
                        'DIEN_GIAI' : line.TEN_HANG,
                        'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                        'SO_HOA_DON' : self.SO_HOA_DON, 
                        'NGAY_CHUNG_TU' : self.NGAY_HOA_DON,
                        'NGAY_HACH_TOAN' : self.NGAY_HOA_DON,
                        'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                        'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO_ID.id,
                        'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                        'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE
                    })
                    line_ids += [(0,0,data)]
                    thu_tu += 1
            
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_HOA_DON,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True

    
    def ghi_so_thue_tu_giam_gia_hang_ban(self):
        line_ids = []
        thu_tu = 0
        if self.SOURCE_ID:
            giam_gia_hang_mua = self.env['sale.ex.giam.gia.hang.ban'].search([('id', '=', self.SOURCE_ID.id)])
            if giam_gia_hang_mua:
                for line in giam_gia_hang_mua.GIAM_GIA_HANG_BAN_CHI_TIET_IDS:
                    data = helper.Obj.inject(line, self)
                    data.update({
                        'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                        'THU_TU_TRONG_CHUNG_TU': thu_tu,
                        'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                        'PHAN_TRAM_VAT': line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT if line.PHAN_TRAM_THUE_GTGT_ID else None,
                        'SO_TIEN_VAT': -1*line.TIEN_THUE_GTGT_QUY_DOI,
                        'SO_TIEN_VAT_NGUYEN_TE' : -1*line.TIEN_THUE_GTGT,
                        'SO_TIEN_CHIU_VAT': -1*line.THANH_TIEN_QUY_DOI,
                        'SO_TIEN_CHIU_VAT_NGUYEN_TE' : -1*line.THANH_TIEN,
                        'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                        'SO_CHUNG_TU' : giam_gia_hang_mua.SO_CHUNG_TU,
                        'DIEN_GIAI' : line.TEN_HANG,
                        'NGAY_HOA_DON' : self.NGAY_HOA_DON,
                        'SO_HOA_DON' : self.SO_HOA_DON, 
                        'NGAY_CHUNG_TU' : self.NGAY_HOA_DON,
                        'NGAY_HACH_TOAN' : self.NGAY_HOA_DON,
                        'KY_HIEU_HOA_DON' : self.KY_HIEU_HD,
                        'TEN_DOI_TUONG' : self.TEN_KHACH_HANG,
                        'MA_SO_THUE_DOI_TUONG' : self.MA_SO_THUE
                    })
                    line_ids += [(0,0,data)]
                    thu_tu += 1
            
        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_HOA_DON,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True

    def phat_hanh_hoa_don(self, is_send_email, email):
        self.ensure_one()
        url = "http://demows.cyberbill.vn"
        supplierTaxCode = '0108703086'
        uri = "/api/services/hddtws/Authentication/GetToken"
        user = 'ktt'
        password = '12345678'
        # encodedBytes = base64.b64encode(':'.join([user,password]).encode("utf-8"))
        # encodedStr = str(encodedBytes, "utf-8")
        headers = {
            "Content-Type": "application/json",
            }
        params = {
            "doanhnghiep_mst": supplierTaxCode,
            "username": user,
            "password": password
        }

        _, token, _ = self._do_request(uri, params, headers, 'POST', url)
        # TH lấy thành công token
        if token:
            # Nếu lập từ chứng từ bán hàng thì phải là chi tiết chứng từ bán hàng
            stt = 1
            for chi_tiet in self.SALE_EX_CHI_TIET_HOA_DON_BAN_HANG_IDS:
                lines = [{
                    'stt': stt, #Todof
                    'hanghoa_loai': DICT_LOAI_VTHH.get(chi_tiet.MA_HANG_ID.TINH_CHAT, '2'),
                    'khuyenmai': 0, #Todof
                    'ma': chi_tiet.MA_HANG_ID.MA,
                    'ten': chi_tiet.MA_HANG_ID.TEN,
                    'donvitinh': chi_tiet.DVT_ID.DON_VI_TINH,
                    'soluong': chi_tiet.SO_LUONG,
                    'dongia': chi_tiet.DON_GIA,
                    'phantram_chietkhau': chi_tiet.TY_LE_CK,
                    'tongtien_chietkhau': chi_tiet.TIEN_CHIET_KHAU_QUY_DOI,
                    'tongtien_chuathue': chi_tiet.THANH_TIEN_QUY_DOI - chi_tiet.TIEN_CHIET_KHAU_QUY_DOI,
                    'mathue': chi_tiet.THUE_GTGT.TEN_THUE or '',
                    'tongtien_cothue ': chi_tiet.THANH_TIEN_QUY_DOI - chi_tiet.TIEN_CHIET_KHAU_QUY_DOI + chi_tiet.TIEN_THUE_GTGT_QUY_DOI,
                }]
                stt += 1
            
            data = {
                'hoadon': {
                    'doanhnghiep_mst': supplierTaxCode,
                    'loaihoadon_ma': '01GTKT', # 02GTTT
                    'mauso': self.MAU_SO_HD_ID.name,
                    'ky_hieu': self.KY_HIEU_HD,
                    'ma_hoadon': self.SO_HOA_DON,
                    'ngaylap ': self.NGAY_HOA_DON + ' 00:00:00' ,
                    'dnmua_mst': self.MA_SO_THUE or self.DOI_TUONG_ID.MA_SO_THUE or '',
                    'dnmua_tennguoimua': self.NGUOI_MUA_HANG or '',
                    'dnmua_diachi': self.DIA_CHI or '',
                    'dnmua_sdt': self.DOI_TUONG_ID.DT_DI_DONG or self.DOI_TUONG_ID.DT_CO_DINH_LIEN_HE or self.DOI_TUONG_ID.DT_DI_DONG_LIEN_HE or '',
                    'dnmua_email': email,
                    'thanhtoan_phuongthuc': DICT_HTTT.get(self.HINH_THUC_TT, 3),
                    'thanhtoan_phuongthuc_ten': dict(self._fields['HINH_THUC_TT'].selection).get(self.HINH_THUC_TT),
                    'thanhtoan_taikhoan': self.partner_bank_id.SO_TAI_KHOAN or '',
                    'thanhtoan_nganhang': self.partner_bank_id.TEN_NGAN_HANG or '',
                    'tiente_ma': self.currency_id.name,
                    'tygiangoaite': self.TY_GIA,
                    'thanhtoan_thoihan': '', #Todof
                    'tongtien_chietkhau': self.TIEN_CHIET_KHAU,
                    'ghichu': '', #Todof
                    'tongtien_chuavat': self.TONG_TIEN_HANG - self.TIEN_CHIET_KHAU,
                    'tienthue': self.TIEN_THUE_GTGT,
                    'tongtien_covat ': self.TONG_TIEN_THANH_TOAN,
                    'nguoilap': self.env.user.name,
                    'dschitiet': lines,
                }
            }
            # headers["Authorization"] = token.get('result').get('access_token')
            headers['Authorization'] = json.dumps({
                'Type': 'Bearer Token',
                'Token': token.get('result'),
                })
            uri = "/api/services/hddtws/GuiHoadon/GuiHoadonGoc"
            auth = None
            # auth= ('Bearer Token',token.get('result').get('access_token'))
            _, response, _ = self._do_request(uri, data, headers, 'POST', url, auth)
            if response:
                return True
            return False

    @api.model
    def _do_request(self, uri, params={}, headers={}, type='POST', preuri="http://demows.cyberbill.vn", auth=None):
        self.ensure_one()
        """ Execute the request to Google API. Return a tuple ('HTTP_CODE', 'HTTP_RESPONSE')
            :param uri : the url to contact
            :param params : dict or already encoded parameters for the request to make
            :param headers : headers of request
            :param type : the method to use to make the request
            :param preuri : pre url to prepend to param uri.
        """
        # _logger.debug("Uri: %s - Type : %s - Headers: %s - Params : %s !", (uri, type, headers, params))
        ask_time = fields.Datetime.now()
        try:
            res = False
            if type.upper() in ('GET', 'DELETE'):
                res = requests.request(type.lower(), preuri + uri, params=params, timeout=TIMEOUT)
            elif type.upper() in ('POST', 'PATCH', 'PUT'):
                if auth:
                    res = requests.post(preuri + uri, data=json.dumps(params), headers=headers, timeout=TIMEOUT, auth=auth)
                else:
                    res = requests.post(preuri + uri, data=json.dumps(params), headers=headers, timeout=TIMEOUT)
                # res = requests.request(type.lower(), preuri + uri, params=params, headers=headers, timeout=TIMEOUT)
            else:
                raise Exception('Method not supported [%s] not in [GET, POST, PUT, PATCH or DELETE]!' % (type))
            res.raise_for_status()
            status = res.status_code

            if int(status) in (204, 404):  # Page not found, no response
                response = False
            else:
                response = res.json()

            try:
                ask_time = datetime.strptime(res.headers.get('date'), "%a, %d %b %Y %H:%M:%S %Z")
            except:
                pass
        except requests.HTTPError as error:
            if error.response.status_code in (204, 404):
                status = error.response.status_code
                response = ""
            else:
                _logger.exception("Bad request : %s !", error.response.text)
                if error.response.status_code in (400, 401, 410):
                    raise error
                raise self.env['res.config.settings'].get_config_warning(error.response.text)
        return (status, response, ask_time)    


