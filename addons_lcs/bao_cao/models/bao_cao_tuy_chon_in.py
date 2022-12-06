# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_TUY_CHON_IN(models.Model):
    _name = 'bao.cao.tuy.chon.in'
    _description = 'Tùy chọn in'

    name = fields.Char(string='Tên báo cáo', readonly=True)

    NGUOI_KY_CHUC_DANH_GIAM_DOC = fields.Boolean(string='Giám đốc', default=True)
    NGUOI_KY_TIEU_DE_GIAM_DOC = fields.Char(string='Tiêu đề', readonly=True, default=lambda self: self.get_tieu_de_giam_doc(), store=False)
    NGUOI_KY_TEN_GIAM_DOC = fields.Char(string='Tên người ký', readonly=True, default=lambda self: self.get_giam_doc(), store=False)

    NGUOI_KY_CHUC_DANH_KE_TOAN_TRUONG = fields.Boolean(string='Kế toán trưởng', default=True)
    NGUOI_KY_TIEU_DE_TOAN_TRUONG = fields.Char(string='Tiêu đề', readonly=True, default=lambda self: self.get_tieu_de_ke_toan_truong(), store=False)
    NGUOI_KY_TEN_KE_TOAN_TRUONG = fields.Char(string='Tên người ký', readonly=True, default=lambda self: self.get_ke_toan_truong(), store=False)

    NGUOI_KY_CHUC_DANH_THU_KHO = fields.Boolean(string='Thủ kho')
    NGUOI_KY_TIEU_DE_THU_KHO = fields.Char(string='Tiêu đề', readonly=True, default=lambda self: self.get_tieu_de_thu_kho(), store=False)
    NGUOI_KY_TEN_THU_KHO = fields.Char(string='Tên người ký', readonly=True, default=lambda self: self.get_thu_kho(), store=False)

    NGUOI_KY_CHUC_DANH_THU_QUY = fields.Boolean(string='Thủ quỹ')
    NGUOI_KY_TIEU_DE_THU_QUY = fields.Char(string='Tiêu đề', readonly=True, default=lambda self: self.get_tieu_de_thu_quy(), store=False)
    NGUOI_KY_TEN_THU_QUY = fields.Char(string='Tên người ký', readonly=True, default=lambda self: self.get_thu_quy(), store=False)

    NGUOI_KY_CHUC_DANH_NGUOI_LAP_BIEU = fields.Boolean(string='Người lập biểu', default=True)
    NGUOI_KY_TIEU_DE_NGUOI_LAP_BIEU = fields.Char(string='Tiêu đề', default=lambda self: self.get_tieu_de_nguoi_lap_phieu())
    NGUOI_KY_TEN_NGUOI_LAP_BIEU = fields.Char(string='Tên người ký', default=lambda self: self.get_nguoi_lap_phieu())

    # KHONG_HIEN_THI = fields.Boolean(string='Không hiển thị giao diện này ở lần in sau')

    @api.model
    def default_get(self, fields):
        rec = super(BAO_CAO_TUY_CHON_IN, self).default_get(fields)
        saved_option = self.search([('name', '=', rec.get('name'))], limit=1)
        if saved_option:
            rec.update({
                'NGUOI_KY_CHUC_DANH_GIAM_DOC': saved_option.NGUOI_KY_CHUC_DANH_GIAM_DOC,
                'NGUOI_KY_CHUC_DANH_KE_TOAN_TRUONG': saved_option.NGUOI_KY_CHUC_DANH_KE_TOAN_TRUONG,
                'NGUOI_KY_CHUC_DANH_THU_KHO': saved_option.NGUOI_KY_CHUC_DANH_THU_KHO,
                'NGUOI_KY_CHUC_DANH_THU_QUY': saved_option.NGUOI_KY_CHUC_DANH_THU_QUY,
                'NGUOI_KY_CHUC_DANH_NGUOI_LAP_BIEU': saved_option.NGUOI_KY_CHUC_DANH_NGUOI_LAP_BIEU,
                'NGUOI_KY_TIEU_DE_NGUOI_LAP_BIEU': saved_option.NGUOI_KY_TIEU_DE_NGUOI_LAP_BIEU,
                'NGUOI_KY_TEN_NGUOI_LAP_BIEU': saved_option.NGUOI_KY_TEN_NGUOI_LAP_BIEU,
            })
        return rec

    @api.model
    def create(self, vals):
        record = self.search([('name', '=', vals.get('name'))], limit=1)
        if record:
            record.write(vals)
        else:
            record = super(BAO_CAO_TUY_CHON_IN, self).create(vals)
        return record

    def _action_view_report(self):
        return True