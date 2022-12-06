# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class STOCK_EX_LAP_RAP_THAO_DO(models.Model):
    _name = 'stock.ex.lap.rap.thao.do'
    _description = 'Lắp ráp, tháo dỡ'
    _inherit = ['mail.thread']
    _order = "NGAY desc, SO desc" 

    HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Hàng hóa', help='Hàng hóa')
    TEN_HANG_HOA = fields.Char(string='Tên hàng hóa', help='Tên hàng hóa',related='HANG_HOA_ID.TEN',store=True)
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits= decimal_precision.get_precision('VND'))
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    THAM_CHIEU = fields.Many2many('stock.ex.nhap.xuat.kho', string='Tham chiếu')
    NGAY = fields.Date(string='Ngày ', help='Ngày',default=fields.Datetime.now)
    SO = fields.Char(string='Số', help='Số', auto_num='stock_ex_lap_rap_thao_do_SO')
    LAP_RAP_THAO_DO = fields.Selection([
        ('LAP_RAP', 'Lắp ráp'), 
        ('THAO_DO', ' Tháo dỡ'), 
        ], string='Lắp ráp, tháo dỡ',default='THAO_DO' )

    name = fields.Char(string='Name', help='Name',related="SO",store=True, oldname='NAME')
    DA_XUAT_KHO = fields.Char(string='Đã xuất kho', help='Đã xuất kho')
    DA_NHAP_KHO = fields.Boolean(string='Đã nhập kho', help='Đã nhập kho')
    STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS = fields.One2many('stock.ex.lap.rap.thao.do.chi.tiet', 'LAP_RAP_THAO_DO_CHI_TIET_ID', string='Lắp ráp tháo dỡ chi tiết', copy=True)
    LOAI_CHUNG_TU=fields.Integer( string='Loại chứng từ',help='Loại chứng từ', compute='_compute_loai_chung_tu', store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    # Các field nắm trong module sale cần phải tách file và dùng theo cơ chế _inherit, vì sale đang depends vào stock
    SOURCE_ID = fields.Reference(selection=[('sale.document','Lập từ Chứng từ bán hàng')], string='Lập từ', oldname='CHON_LAP_TU_ID')

    _sql_constraints = [
	('SO_LRTD_uniq', 'unique ("SO")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
	]

    @api.depends('LAP_RAP_THAO_DO')
    def _compute_loai_chung_tu(self):
        for record in self:
            if record.LAP_RAP_THAO_DO:
                if record.LAP_RAP_THAO_DO == 'LAP_RAP':
                    record.LOAI_CHUNG_TU = 2050
                elif record.LAP_RAP_THAO_DO == 'THAO_DO':
                    record.LOAI_CHUNG_TU = 2051

    @api.onchange('HANG_HOA_ID')
    def update_TEN_HANG_HOA(self):
        self.TEN_HANG_HOA = self.HANG_HOA_ID.TEN
        self.DVT_ID = self.HANG_HOA_ID.DVT_CHINH_ID
        self.SO_LUONG = 1

    @api.onchange('HANG_HOA_ID')
    def update_lap_rap_thao_do_chi_tiet(self):
        if self.HANG_HOA_ID and self.HANG_HOA_ID.TINH_CHAT=='1':
            self.STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS= []
            for dinh_muc_nvl_hang_hoa in self.HANG_HOA_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                new_line = self.env['stock.ex.lap.rap.thao.do.chi.tiet'].new({
                    'MA_HANG_ID':dinh_muc_nvl_hang_hoa.MA_NGUYEN_VAT_LIEU_ID,
                    'DVT_ID':dinh_muc_nvl_hang_hoa.DVT_ID,
                    'TEN_HANG':dinh_muc_nvl_hang_hoa.TEN_NGUYEN_VAT_LIEU,
                    'SO_LUONG':dinh_muc_nvl_hang_hoa.SO_LUONG,
                    'KHO_ID':dinh_muc_nvl_hang_hoa.MA_NGUYEN_VAT_LIEU_ID.KHO_NGAM_DINH_ID,
                    #kho
                })

                self.STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS +=new_line

    @api.onchange('SO_LUONG')
    def _onchange_SO_LUONG(self):
        if self.STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS:
            dict_nguyen_vat_lieu = {}
            if self.HANG_HOA_ID and self.HANG_HOA_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                for nvl in self.HANG_HOA_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                    key = nvl.MA_NGUYEN_VAT_LIEU_ID.id
                    if key not in dict_nguyen_vat_lieu:
                        dict_nguyen_vat_lieu[key] = nvl.SO_LUONG
            for line in self.STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS:
                if line.MA_HANG_ID.id in dict_nguyen_vat_lieu:
                    line.SO_LUONG = self.SO_LUONG*dict_nguyen_vat_lieu[line.MA_HANG_ID.id]
                
    
    


    @api.multi
    def btn_LSX_PN(self):
        id_lap_rap_thao_do = self.id
        loai_chung_tu = False
        if self.LAP_RAP_THAO_DO == 'LAP_RAP':
            loai_chung_tu = 2011
        elif self.LAP_RAP_THAO_DO == 'THAO_DO':
            loai_chung_tu = 2012
        action = self.env.ref('stock_ex.action_open_stock_ex_nk_form').read()[0]
        context ={
            'default_ID_LAP_RAP_THAO_DO': id_lap_rap_thao_do,
            'default_LOAI_CHUNG_TU'     : loai_chung_tu ,
         }
        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['name'] =' Phiếu nhập kho thành phẩm lắp ráp' 
        return action
    
    @api.multi
    def btn_LSX_PX(self):
        id_lap_rap_thao_do = self.id
        loai_chung_tu = False
        if self.LAP_RAP_THAO_DO == 'LAP_RAP':
            loai_chung_tu = 2024
        elif self.LAP_RAP_THAO_DO == 'THAO_DO':
            loai_chung_tu = 2025
        action = self.env.ref('stock_ex.action_open_stock_ex_xk_form').read()[0]
        context ={
            'default_ID_LAP_RAP_THAO_DO': id_lap_rap_thao_do,
            'default_LOAI_CHUNG_TU_PX'  : loai_chung_tu,
         }
        action['context'] = helper.Obj.merge(context, action.get('context'))
        return action
    
    def tao_phieu_xuat_kho_nvl(self):
        self.ensure_one()
        # Tạo phiếu xuất kho nguyên vật liệu
        xuat_kho_lap_rap_chi_tiet = []
        default_2024 = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].lay_tai_khoan_ngam_dinh(2024)
        for lap_rap_thao_ro_dt_ct in self.STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET_IDS:
            xuat_kho_lap_rap_chi_tiet +=[(0,0,{
                'MA_HANG_ID':lap_rap_thao_ro_dt_ct.MA_HANG_ID.id,
                'TEN_HANG'  :lap_rap_thao_ro_dt_ct.TEN_HANG,
                'DVT_ID':lap_rap_thao_ro_dt_ct.DVT_ID.id,
                'SO_LUONG'  :lap_rap_thao_ro_dt_ct.SO_LUONG,
                'DON_GIA_VON'  :lap_rap_thao_ro_dt_ct.DON_GIA,
                'TIEN_VON'  :lap_rap_thao_ro_dt_ct.THANH_TIEN,
                'LENH_LR_TD_ID'  :self.id,
                'KHO_ID'  :lap_rap_thao_ro_dt_ct.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                'TK_NO_ID'  : default_2024.get('TK_NO_ID'),
                'TK_CO_ID':  default_2024.get('TK_CO_ID') or lap_rap_thao_ro_dt_ct.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
            })]
        so_chung_tu_xk = self.env['ir.sequence'].next_by_code('stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_XUAT_KHO')
        xuat_kho_de_lap_rap = {
            'name': so_chung_tu_xk,
            'SO_CHUNG_TU': so_chung_tu_xk,
            'LOAI_XUAT_KHO': 'SAN_XUAT',
            'LOAI_CHUNG_TU_2': 2024,
            'LOAI_CHUNG_TU': 2024,
            'type': 'XUAT_KHO',
            'LY_DO_XUAT': 'Xuất kho để lắp ráp',
            'NGAY_CHUNG_TU': self.NGAY,
            'NGAY_HACH_TOAN': self.NGAY,
            'LAP_RAP_THAO_DO_ID'  :self.id,
            'CHI_TIET_IDS': xuat_kho_lap_rap_chi_tiet,
        }
        self.env['stock.ex.nhap.xuat.kho'].create(xuat_kho_de_lap_rap)
        # self.write({'THAM_CHIEU': [(4, xuat_kho_id.id)]})
    
    def tao_phieu_nhap_kho_thanh_pham(self):
        self.ensure_one()
        # Tạo phiếu nhập kho thành phẩm
        default_2011 = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].lay_tai_khoan_ngam_dinh(2011)
        nhap_kho_lap_rap_chi_tiet = [(0,0,{
            'MA_HANG_ID':self.HANG_HOA_ID.id,
            'TEN_HANG'  :self.TEN_HANG_HOA,
            'DVT_ID':self.DVT_ID.id,
            'SO_LUONG'  :self.SO_LUONG,
            'DON_GIA_VON'  :self.DON_GIA,
            'TIEN_VON'  :self.THANH_TIEN,
            'LENH_LR_TD_ID'  :self.id,
            'KHO_ID'  :self.HANG_HOA_ID.KHO_NGAM_DINH_ID.id,
            'TK_NO_ID'  : default_2011.get('TK_NO_ID') or self.HANG_HOA_ID.TAI_KHOAN_KHO_ID.id,
            'TK_CO_ID':  default_2011.get('TK_CO_ID'),
        })]
        so_chung_tu_nk = self.env['ir.sequence'].next_by_code('stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_NHAP_KHO')
        nhap_kho_tu_lap_rap = {
            'name': so_chung_tu_nk,
            'SO_CHUNG_TU': so_chung_tu_nk,
            'LOAI_NHAP_KHO': 'THANH_PHAM',
            'LOAI_CHUNG_TU_2': 2011,
            'LOAI_CHUNG_TU': 2011,
            'type': 'NHAP_KHO',
            'DIEN_GIAI': 'Nhập kho từ lắp ráp',
            'NGAY_CHUNG_TU': self.NGAY,
            'NGAY_HACH_TOAN': self.NGAY,
            'LAP_RAP_THAO_DO_ID' :self.id,
            'CHI_TIET_IDS': nhap_kho_lap_rap_chi_tiet,
        }
        self.env['stock.ex.nhap.xuat.kho'].create(nhap_kho_tu_lap_rap)
        # self.write({'THAM_CHIEU': [(4, nhap_kho_id.id)]})

    # Cập nhật cho phiếu xuất và nhập gắn kèm
    @api.multi
    def write(self, values):
        result = super(STOCK_EX_LAP_RAP_THAO_DO, self).write(values)
        for record in self:
            if helper.List.element_in_dict(['SO_LUONG','DVT_ID'], values):
                for tc in record.THAM_CHIEU:
                    if tc.state=='da_ghi_so':
                        raise ValidationError("Lệnh lắp ráp, tháo dỡ này <<%s>> đã phát sinh. Bạn phải bỏ ghi sổ các chứng từ phát sinh trước!", self.SO)
                    if tc.type == 'NHAP_KHO':
                        tc.unlink()
                        record.tao_phieu_nhap_kho_thanh_pham()
                    elif tc.type == 'XUAT_KHO':
                        tc.unlink()
                        record.tao_phieu_xuat_kho_nvl()
            elif helper.List.element_in_dict(['NGAY'], values):
                record.THAM_CHIEU.write({
                    'NGAY_CHUNG_TU': values.get('NGAY'),
                    'NGAY_HACH_TOAN': values.get('NGAY'),
                })
                
        return result

    
    @api.multi
    def unlink(self):
        for record in self:
            msg_error = ''
            for tc in record.THAM_CHIEU:
                if tc.type == 'NHAP_KHO' and tc.state=='da_ghi_so':
                    msg_error +=  ' '.join([' Phiếu nhập số <<', tc.SO_CHUNG_TU,'>>'])
                elif tc.type == 'XUAT_KHO' and tc.state=='da_ghi_so':
                    msg_error +=  ' '.join([' Phiếu xuất số <<', tc.SO_CHUNG_TU,'>>'])
            if msg_error:
                raise ValidationError("Lệnh lắp ráp, tháo dỡ này đã phát sinh%s. Bạn phải bỏ ghi sổ các chứng từ phát sinh trước!" % msg_error)
        return super(STOCK_EX_LAP_RAP_THAO_DO, self).unlink()