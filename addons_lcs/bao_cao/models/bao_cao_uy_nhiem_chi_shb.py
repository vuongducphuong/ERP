# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_UNC_SHB(models.Model):
    _name = 'bao.cao.uy.nhiem.chi.shb'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    TAI_KHOAN_CHI_GUI_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Tài khoản chi', help='Tài khoản chi')
    TAI_NGAN_HANG_MAU_IN = fields.Char(string='Tại ngân hàng mẫu in', help='Tại ngân hàng mẫu in',store=False)
    TEN_TK_CHI = fields.Char(string='Tên TK chi',help='Tên tài khoản chi')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    SO_TIEN_1 = fields.Monetary(string='Số tiền',compute='tinhtongtien', currency_field='currency_id')
    TAI_KHOAN_THU_NHAN_ID = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='Tài khoản đi', help='Tài khoản đi')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TEN_NOI_DUNG_TT = fields.Text(string='Tên nội dung thanh toán',help='Tên nội dung thanh toán', related='DIEN_GIAI')
    TEN_TK_NHAN = fields.Char(string='Tên TK nhận',help='Tên tài khoản nhận')


    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.uy.nhiem.chi.shb.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

    

    @api.depends('ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS.SO_TIEN')
    def tinhtongtien(self):
        for order in self:
            tong_so_tien = 0
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS: 
                tong_so_tien += line.SO_TIEN
            order.update({
                'SO_TIEN_1': tong_so_tien,
            })

class BAO_CAO_UNC_SHB_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_shbunc'

    @api.model
    def get_report_values(self, docids, data=None):
        ############### START SQL lấy dữ liệu ###############
        query = """
            SELECT *, m.id AS master_id FROM account_ex_phieu_thu_chi m
            JOIN account_ex_phieu_thu_chi_tiet d ON d."PHIEU_THU_CHI_ID" = m.id
            WHERE m.id in %(ids)s
        """
        record_ids = []
        records = {}
        for rec in data.get('ids'):
            record_ids += [rec.split(',')[1]]
            records[rec] = self.env['bao.cao.uy.nhiem.chi.shb'].new({'ref': rec})
        
        params = {'ids': tuple(record_ids)}
        sql_result = self.execute(query, params)
        ####################### END SQL #######################

        # Tạo object để in
        for line in sql_result:
            key = 'account.ex.phieu.thu.chi,' + str(line.get('master_id'))
            master_data = {
             
                'DIEN_GIAI': line.get('DIEN_GIAI'),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
                'currency_id': line.get('currency_id'),
                'TY_GIA': line.get('TY_GIA'),
                'CHI_NHANH_ID': line.get('CHI_NHANH_ID'),
                'SO_TIEN_1': line.get('SO_TIEN_1'),
                'TEN_DOI_TUONG': line.get('TEN_DOI_TUONG'),
                'TAI_KHOAN_CHI_GUI_ID': line.get('TAI_KHOAN_CHI_GUI_ID'),
                'TAI_NGAN_HANG_MAU_IN': line.get('TAI_NGAN_HANG_MAU_IN'),
                'TEN_TK_CHI': line.get('TEN_TK_CHI'),
                'TAI_KHOAN_THU_NHAN_ID': line.get('TAI_KHOAN_THU_NHAN_ID'),
                'DOI_TUONG_ID': line.get('DOI_TUONG_ID'),
                'TEN_NOI_DUNG_TT': line.get('TEN_NOI_DUNG_TT'),
                'TEN_TK_NHAN': line.get('TEN_TK_NHAN'),
            }
            detail_data = {
                'SO_TIEN': line.get('SO_TIEN'),
           
            }
            records[key].update(master_data)
            records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.uy.nhiem.chi.shb.chi.tiet'].new(detail_data)

        return {
            'docs': [records.get(k) for k in records],
        }