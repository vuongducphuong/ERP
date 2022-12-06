# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_S37_DN_THE_TINH_GIA_THANH_SAN_PHAM_DICH_VU(models.Model):
    _name = 'bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHOAN_MUC_CHI_PHI', 'Khoản mục chi phí'), ('YEU_TO', 'Yếu tố'), ], string='Thống kê theo', help='Thống kê theo',default='KHOAN_MUC_CHI_PHI', required='True')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_TINH_GIA_THANH = fields.Many2one( 'gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    CHI_TIEU = fields.Char(string='Chi tiêu ', help='Chi tiêu ')
    TONG_SO_TIEN = fields.Float(string='Tổng số tiền', help='Tổng số tiền')
    NGUYEN_VAT_LIEU = fields.Float(string='Nguyên vật liệu', help='Nguyên vật liệu')
    NHAN_CONG = fields.Char(string='Nhân công', help='Nhân công')
    KHAU_HAO = fields.Char(string='Khấu hao', help='Khấu hao')
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài')
    CHI_PHI_KHAC = fields.Float(string='Chi phí khác', help='Chi phí khác')
    NGUYEN_VAT_LIEU_TRUC_TIEP = fields.Float(string='Nguyên vật liệu trực tiếp', help='Nguyên vật liệu trực tiếp')
    NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp')
    MAY_THI_CONG = fields.Float(string='Máy thi công', help='Máy thi công')
    CHI_PHI_SAN_XUAT_CHUNG = fields.Float(string='Chi phí sản xuất chung', help='Chi phí sản xuất chung')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    LOAI_GIA_THANH = fields.Selection([('DON_GIAN', 'Đơn giản'), ('HE_SO_TY_LE', 'Hệ số tỷ lệ'), ('CONG_TRINH', 'Công trình'), ('DON_HANG', 'Đơn hàng'), ('HOP_DONG', 'Hợp đồng'), ],string='Loại giá thành', help='Loại giá thành')

    DOI_TUONG_THCP_IDS_GIAN_DON = fields.One2many('bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet')
    DOI_TUONG_THCP_IDS_HE_SO_TY_LE = fields.One2many('bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet')
    DOI_TUONG_THCP_IDS_CONG_TRINH = fields.One2many('bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet')
    

    @api.onchange('KY_TINH_GIA_THANH')
    def _onchange_LOAI_GIA_THANH(self):
        loai_gia_thanh = ''
        id_ky_tinh_gia_thanh = 0
        self.DOI_TUONG_THCP_IDS_GIAN_DON = []
        self.DOI_TUONG_THCP_IDS_HE_SO_TY_LE = []
        self.DOI_TUONG_THCP_IDS_CONG_TRINH = []

        if self.KY_TINH_GIA_THANH:
            loai_gia_thanh = self.KY_TINH_GIA_THANH.LOAI_GIA_THANH
            id_ky_tinh_gia_thanh = self.KY_TINH_GIA_THANH.id
        if loai_gia_thanh == 'DON_GIAN':
            self.LOAI_GIA_THANH = loai_gia_thanh
            if id_ky_tinh_gia_thanh != 0:
                ky_tinh_gia_thanh_chi_tiet = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', id_ky_tinh_gia_thanh)])
                
                if ky_tinh_gia_thanh_chi_tiet:
                    for line in ky_tinh_gia_thanh_chi_tiet:
                        for thanh_pham in line.MA_DOI_TUONG_THCP_ID.DANH_MUC_CHI_TIET_DOI_TUONG_TINH_GIA_THANH_IDS:
                            detail = self.env['bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet'].new()

                            detail.MA_THANH_PHAM_ID = thanh_pham.MA_HANG_ID.id
                            detail.TEN_THANH_PHAM = thanh_pham.TEN_THANH_PHAM
                            detail.MA_DOI_TUONG_THCP_ID = line.MA_DOI_TUONG_THCP_ID.id
                            detail.TEN_DOI_TUONG_THCP = line.TEN_DOI_TUONG_THCP

                            self.DOI_TUONG_THCP_IDS_GIAN_DON += detail
        elif loai_gia_thanh == 'HE_SO_TY_LE':
            self.LOAI_GIA_THANH = loai_gia_thanh
            if id_ky_tinh_gia_thanh != 0:
                ky_tinh_gia_thanh_chi_tiet = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', id_ky_tinh_gia_thanh)])
                
                if ky_tinh_gia_thanh_chi_tiet:
                    for line in ky_tinh_gia_thanh_chi_tiet:
                        for thanh_pham in line.MA_DOI_TUONG_THCP_ID.DANH_MUC_CHI_TIET_DOI_TUONG_TINH_GIA_THANH_IDS:
                            detail = self.env['bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet'].new()

                            detail.MA_THANH_PHAM_ID = thanh_pham.MA_HANG_ID.id
                            detail.TEN_THANH_PHAM = thanh_pham.TEN_THANH_PHAM
                            detail.MA_DOI_TUONG_THCP_ID = line.MA_DOI_TUONG_THCP_ID.id
                            detail.TEN_DOI_TUONG_THCP = line.TEN_DOI_TUONG_THCP
                            
                            self.DOI_TUONG_THCP_IDS_HE_SO_TY_LE += detail
        elif loai_gia_thanh == 'CONG_TRINH':
            self.LOAI_GIA_THANH = loai_gia_thanh
            if id_ky_tinh_gia_thanh != 0:
                ky_tinh_gia_thanh_chi_tiet = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', id_ky_tinh_gia_thanh)])
                
                if ky_tinh_gia_thanh_chi_tiet:
                    for line in ky_tinh_gia_thanh_chi_tiet:
                        detail = self.env['bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet'].new()

                        bac_cong_trinh = line.MA_CONG_TRINH_ID.BAC
                        detail.MA_CONG_TRINH_ID = line.MA_CONG_TRINH_ID.id
                        detail.TEN_CONG_TRINH = line.TEN_CONG_TRINH
                        detail.LOAI_CONG_TRINH = line.LOAI_CONG_TRINH
                        detail.BAC = bac_cong_trinh
                        self.DOI_TUONG_THCP_IDS_CONG_TRINH += detail
        else:
            self.LOAI_GIA_THANH = 'DON_GIAN'


    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_S37_DN_THE_TINH_GIA_THANH_SAN_PHAM_DICH_VU, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh :
            result['CHI_NHANH_ID'] = chi_nhanh.id
        result['LOAI_GIA_THANH'] = 'DON_GIAN'
        return result
    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_TINH_GIA_THANH = params['KY_TINH_GIA_THANH'] if 'KY_TINH_GIA_THANH' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'CHI_TIEU': '',
                'TONG_SO_TIEN': '',
                'NGUYEN_VAT_LIEU': '',
                'NHAN_CONG': '',
                'KHAU_HAO': '',
                'CHI_PHI_MUA_NGOAI': '',
                'CHI_PHI_KHAC': '',
                'name': '',
                })
        return record

    def _validate(self):
        params = self._context
        LOAI_GIA_THANH = params['LOAI_GIA_THANH'] if 'LOAI_GIA_THANH' in params.keys() else 'False'
        DOI_TUONG_THCP_IDS_CONG_TRINH = params['DOI_TUONG_THCP_IDS_CONG_TRINH'] if 'DOI_TUONG_THCP_IDS_CONG_TRINH' in params.keys() else 'False'
        if LOAI_GIA_THANH == 'CONG_TRINH':
            if DOI_TUONG_THCP_IDS_CONG_TRINH == 'False':
                raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')


    def _action_view_report(self):
        self._validate()
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        LOAI_GIA_THANH = self.get_context('LOAI_GIA_THANH')
        param = ''
        if THONG_KE_THEO == 'KHOAN_MUC_CHI_PHI':
            if LOAI_GIA_THANH == 'CONG_TRINH':
                action = self.env.ref('bao_cao.open_report__s37_dn_the_tinh_gia_thanh_san_pham_dich_vu_cong_trinh_khoan_muc_cp').read()[0]
            else:
                action = self.env.ref('bao_cao.open_report__s37_dn_the_tinh_gia_thanh_san_pham_dich_vu_san_xuat_lt_khoan_muc_cp').read()[0]
        else:
            action = self.env.ref('bao_cao.open_report__s37_dn_the_tinh_gia_thanh_san_pham_dich_vu_san_xuat_lt_yeu_to').read()[0]

        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action