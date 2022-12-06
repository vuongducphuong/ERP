# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class PURCHASE_EX_TRA_LAI_HANG_MUA(models.Model):
    _inherit = 'purchase.ex.tra.lai.hang.mua'


    HOA_DON_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', string='Hóa đơn', help='Hóa đơn')
    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            if record.selection_chung_tu_mua_hang == 'thu_tien_mat':
                record.validate_unique_thu_chi_tien(record.SO_PHIEU_THU)

    @api.multi
    def validate_nhap_xuat_kho(self):
        for record in self:
            if record.TRA_LAI_HANG_TRONG_KHO:
                record.validate_unique_thu_chi_tien(record.SO_PHIEU_XUAT)

    @api.model
    def create(self, vals):
        result = super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).create(vals)
        result.validate_unique_so_chung_tu()
        result.validate_thu_chi_tien()
        result.validate_nhap_xuat_kho()
        self.create_references(result)
        return result
    
    def create_references(self, return_doc):
        # Luôn lập kèm hóa đơn
        vals = {
            'SO_HOA_DON': return_doc.SO_HOA_DON,
            'NGAY_HOA_DON': return_doc.NGAY_HOA_DON,
            'KY_HIEU_HD': return_doc.KY_HIEU_HD,
            'MAU_SO_HD_ID': return_doc.MAU_SO_HD_ID.id,
            'DOI_TUONG_ID': return_doc.DOI_TUONG_ID.id,
            'TEN_KHACH_HANG': return_doc.TEN_NHA_CUNG_CAP,
            'LOAI_CHUNG_TU': 3564,
            'TONG_TIEN_THANH_TOAN': return_doc.TONG_TIEN_THANH_TOAN,
            'DA_HACH_TOAN': True,
            'SOURCE_ID': self._name + ',' + str(return_doc.id),
        }
        hoa_don = self.env['sale.ex.hoa.don.ban.hang'].create(vals)
        return_doc.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS.write({'HOA_DON_ID': hoa_don.id})

    @api.multi
    def write(self, values):
        result = super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).write(values)
        if values.get('selection_chung_tu_mua_hang') or values.get('SO_PHIEU_THU'):
            self.validate_thu_chi_tien()
        if values.get('TRA_LAI_HANG_TRONG_KHO') or values.get('SO_PHIEU_XUAT'):
            self.validate_nhap_xuat_kho()
        if helper.List.element_in_dict(['selection_chung_tu_mua_hang','TRA_LAI_HANG_TRONG_KHO','SO_PHIEU_XUAT','SO_PHIEU_THU'], values):
            self.validate_unique_so_chung_tu()
        self.update_references(values)
        return result
    
    def update_references(self, values):
        # Cập nhật hóa đơn gắn kèm nếu có
        if values.get('HINH_THUC_TT') == 'TM_CK':
            values['HINH_THUC_TT'] = 'TM/CK'
        vals = helper.Obj.get_sub_dict(values, ('SO_HOA_DON','NGAY_HOA_DON','KY_HIEU_HD','MAU_SO_HD_ID','DOI_TUONG_ID','LOAI_CHUNG_TU','SOURCE_ID','HINH_THUC_TT','TONG_TIEN_THANH_TOAN'))
        if 'TEN_NHA_CUNG_CAP' in values:
            vals.update({
                'TEN_KHACH_HANG': values.get('TEN_NHA_CUNG_CAP'),
            })
        for record in self: 
            record.find_reference('sale.ex.hoa.don.ban.hang').write(vals)

    @api.multi
    def unlink(self):
        for record in self:
            record.find_reference('sale.ex.hoa.don.ban.hang').unlink()
        return super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).unlink()

    @api.multi
    def action_ghi_so(self):
        for record in self:
            hoa_don = record.find_reference('sale.ex.hoa.don.ban.hang')
            if hoa_don:
                hoa_don.ghi_so_thue_tu_tra_lai_hang_mua()
        return super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).action_ghi_so()

    @api.multi
    def action_bo_ghi_so(self, args):
        # Bỏ ghi sổ các references
        for record in self:
            hoa_don = record.find_reference('sale.ex.hoa.don.ban.hang')
            if hoa_don:
                hoa_don.action_bo_ghi_so()
        return super(PURCHASE_EX_TRA_LAI_HANG_MUA, self).action_bo_ghi_so()