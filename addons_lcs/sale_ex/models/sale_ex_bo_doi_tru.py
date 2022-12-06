# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
import json

class SALE_EX_BO_DOI_TRU(models.Model):
    _name = 'sale.ex.bo.doi.tru'
    _description = ''
    _auto = False
    
    TAI_KHOAN_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK phải thu', help='Tài khoản phải thu')
    TAI_KHOAN_TRA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK phải trả', help='Tài khoản phải trả')
    KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    NHA_CUNG_CAP_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    ID_DOI_TRU = fields.Text()
    LOAI_BO_DOI_TRU = fields.Selection([('BAN_HANG', 'Đối trừ chứng từ bán hàng'), ('MUA_HANG', 'Đối trừ chứng từ mua hàng')], string='Loại đối trừ chứng từ')
    BO_DOI_TRU_JSON = fields.Text(store=False)
    

    SALE_EX_BO_DOI_TRU_CHI_TIET_IDS = fields.One2many('sale.ex.bo.doi.tru.chi.tiet', 'BO_DOI_TRU_CHI_TIET_ID', string='Bỏ đối trừ chi tiết')

    # def action_view_result(self):
    #     action = self.env.ref('sale_ex.action_open_sale_ex_bo_doi_tru_form').read()[0]
    #     # action['options'] = {'clear_breadcrumbs': True}
    #     return action

    @api.model
    def default_get(self, fields):
        rec = super(SALE_EX_BO_DOI_TRU, self).default_get(fields)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1)
        tk_thu_ban_hang  = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '131')],limit=1)
        tk_thu_mua_hang = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '331')],limit=1)
        if loai_tien:
            rec['currency_id'] =loai_tien.id
        if self.get_context('LOAI_BO_DOI_TRU') == 'BAN_HANG':
            if tk_thu_ban_hang:
                rec['TAI_KHOAN_THU_ID'] =tk_thu_ban_hang.id
        elif self.get_context('LOAI_BO_DOI_TRU') == 'MUA_HANG':
            if tk_thu_mua_hang:
                rec['TAI_KHOAN_TRA_ID'] =tk_thu_mua_hang.id
       
        return rec

    @api.onchange('currency_id')
    def update_loai_tien(self):
        if self.currency_id.MA_LOAI_TIEN == 'VND':
            self.IS_TY_GIA = False
        else:
            self.IS_TY_GIA =True
    # tungdztodo:laydulieu
    # @api.onchange('KHACH_HANG_ID','NHA_CUNG_CAP_ID')
    # def _onchange_KHACH_HANG_ID(self):
    #     if self.KHACH_HANG_ID or self.NHA_CUNG_CAP_ID:
    #         self.lay_du_lieu_doi_tru()

    @api.model
    def lay_du_lieu_doi_tru(self, args):
        tt_doi_tru = []
        if self.LOAI_BO_DOI_TRU == 'BAN_HANG':
            if not self.TAI_KHOAN_THU_ID:
                raise ValidationError('<Tài khoản phải thu> không được bỏ trống')
            elif not self.KHACH_HANG_ID:
                raise ValidationError('<Khách hàng> không được bỏ trống')
            else:
                tt_doi_tru = self.reset_du_lieu_doi_tru(self.KHACH_HANG_ID.id,self.currency_id.id,self.TAI_KHOAN_THU_ID.id)
        elif self.LOAI_BO_DOI_TRU == 'MUA_HANG':
            if not self.TAI_KHOAN_TRA_ID:
                raise ValidationError('<Tài khoản phải trả> không được bỏ trống')
            elif not self.NHA_CUNG_CAP_ID:
                raise ValidationError('<Nhà cung cấp> không được bỏ trống')
            else:
                tt_doi_tru = self.reset_du_lieu_doi_tru(self.NHA_CUNG_CAP_ID.id,self.currency_id.id,self.TAI_KHOAN_TRA_ID.id)
        return tt_doi_tru

    def reset_du_lieu_doi_tru(self, doi_tuong_id, currency_id, tai_khoan_id):
        new_line = [[5]]
        for line in self.thong_tin_doi_tru(doi_tuong_id, currency_id, tai_khoan_id):
            ten_loai_chung_tu_thanh_toan = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line.get('LOAI_CHUNG_TU_THANH_TOAN'))], limit=1).REFTYPENAME
            ten_loai_chung_tu_cong_no = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line.get('LOAI_CHUNG_TU_CONG_NO'))], limit=1).REFTYPENAME
            new_line += [(0,0,{
                    'LOAI_CHUNG_TU_THANH_TOAN': ten_loai_chung_tu_thanh_toan,
                    'NGAY_CHUNG_TU_THANH_TOAN' : line.get('NGAY_CHUNG_TU_THANH_TOAN'),
                    'SO_CHUNG_TU_THANH_TOAN' : line.get('SO_CHUNG_TU_THANH_TOAN'),
                    'SO_DOI_TRU_THANH_TOAN' : line.get('SO_THANH_TOAN_LAN_NAY'),
                    'LOAI_CHUNG_TU_CONG_NO' : ten_loai_chung_tu_cong_no,
                    'NGAY_CHUNG_TU_CONG_NO' : line.get('NGAY_CHUNG_TU_CONG_NO'),
                    'SO_CHUNG_TU_CONG_NO' : line.get('SO_CHUNG_TU_CONG_NO'),
                    'SO_HOA_DON' : line.get('SO_HOA_DON_CONG_NO'),
                    'SO_DOI_TRU_CONG_NO' : line.get('SO_CONG_NO_THANH_TOAN_LAN_NAY'),
                    'CHENH_LECH_TY_GIA' : line.get('CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI'),
                    'ID_DOI_TRU' : line.get('ID_DTCT'),
                })]
        
        return new_line

    def bo_doi_tru(self, args):
        doi_tuong_id = False
        currency_id  = self.currency_id.id
        tai_khoan_id = False
        if self.LOAI_BO_DOI_TRU == 'BAN_HANG':
            if not self.TAI_KHOAN_THU_ID:
                raise ValidationError('<Tài khoản phải thu> không được bỏ trống')
            elif not self.KHACH_HANG_ID:
                raise ValidationError('<Khách hàng> không được bỏ trống')
            else:
                doi_tuong_id = self.KHACH_HANG_ID.id
                tai_khoan_id = self.TAI_KHOAN_THU_ID.id
                
        elif self.LOAI_BO_DOI_TRU == 'MUA_HANG':
            if not self.TAI_KHOAN_TRA_ID:
                raise ValidationError('<Tài khoản phải trả> không được bỏ trống')
            elif not self.NHA_CUNG_CAP_ID:
                raise ValidationError('<Nhà cung cấp> không được bỏ trống')
            else:
                doi_tuong_id = self.NHA_CUNG_CAP_ID.id
                tai_khoan_id = self.TAI_KHOAN_TRA_ID.id
            
        # Lấy dữ liệu trước rồi mới xóa, vì khi unlink xong thì self cũng bị reset giá trị ??? 
        for line in self.SALE_EX_BO_DOI_TRU_CHI_TIET_IDS:
            if line.AUTO_SELECT == True:
                self.env['sale.ex.doi.tru.chi.tiet'].browse(line.ID_DOI_TRU).unlink()

        return self.reset_du_lieu_doi_tru(doi_tuong_id, currency_id, tai_khoan_id)

    def thong_tin_doi_tru(self,doi_tuong,loai_tien,tai_khoan):
        record = []
        params = {
            'DOI_TUONG_ID': doi_tuong,
            'currency_id' : loai_tien,
            'TAI_KHOAN' : tai_khoan,
            }

        query = """   

         SELECT
                GVCED.id AS "ID_DTCT",
                GVCED."ID_CHUNG_TU" ,
                GVCED."ID_CHUNG_TU_THANH_TOAN",
                GVCED."LOAI_CHUNG_TU_THANH_TOAN" ,
--                SRT1."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU_THANH_TOAN" ,
                GVCED."NGAY_CHUNG_TU_THANH_TOAN" ,
                GVCED."NGAY_HACH_TOAN_THANH_TOAN" ,
                GVCED."SO_CHUNG_TU_THANH_TOAN" ,
                GVCED."SO_THANH_TOAN_LAN_NAY" ,
                GVCED."SO_THANH_TOAN_LAN_NAY_QUY_DOI" ,
                GVCED."ID_CHUNG_TU_CONG_NO" ,
                GVCED."LOAI_CHUNG_TU_CONG_NO" ,
--                SRT2."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU_CONG_NO" ,
                GVCED."NGAY_CHUNG_TU_CONG_NO" ,
                GVCED."NGAY_HACH_TOAN_CONG_NO" ,
                GVCED."SO_CHUNG_TU_CONG_NO" ,
                GVCED."SO_HOA_DON_CONG_NO" ,
                GVCED."SO_CONG_NO_THANH_TOAN_LAN_NAY" ,
                GVCED."SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI" ,
                GVCED."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI" ,
                coalesce(GV.id, -1) AS "ID_CHUNG_TU" ,
                coalesce(GV."LOAI_CHUNG_TU", -1) AS "LOAI_CHUNG_TU" ,
                coalesce(GV."SO_CHUNG_TU", '') AS "SO_CHUNG_TU"
      FROM      sale_ex_doi_tru_chi_tiet AS GVCED
--       INNER JOIN danh_muc_reftype AS SRT1
--                 ON GVCED."LOAI_CHUNG_TU_THANH_TOAN" = cast(SRT1."REFTYPE" AS INTEGER)
--       INNER JOIN danh_muc_reftype AS SRT2
--                 ON GVCED."LOAI_CHUNG_TU_CONG_NO" = cast(SRT2."REFTYPE" AS INTEGER)
      LEFT JOIN account_ex_chung_tu_nghiep_vu_khac AS GV
                ON GVCED."ID_CHUNG_TU" = GV.id
      WHERE     GVCED."DOI_TUONG_ID" = %(DOI_TUONG_ID)s
                AND GVCED."TAI_KHOAN_ID" = %(TAI_KHOAN)s
                AND GVCED."currency_id" = %(currency_id)s
--                 AND GVCED."CHI_NHANH_ID" = (chi_nhanh_id)
                AND GVCED."LOAI_DOI_TRU" = '1'
      ORDER BY  GVCED."SO_CHUNG_TU_THANH_TOAN"


        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                # 'TEN_LOAI_CHUNG_TU_THANH_TOAN': line.get('TEN_LOAI_CHUNG_TU_THANH_TOAN', ''),
                'NGAY_CHUNG_TU_THANH_TOAN': line.get('NGAY_CHUNG_TU_THANH_TOAN', ''),
                'SO_CHUNG_TU_THANH_TOAN': line.get('SO_CHUNG_TU_THANH_TOAN', ''),
                'SO_THANH_TOAN_LAN_NAY': line.get('SO_THANH_TOAN_LAN_NAY', ''),
                # 'TEN_LOAI_CHUNG_TU_CONG_NO': line.get('TEN_LOAI_CHUNG_TU_CONG_NO', ''),
                'NGAY_CHUNG_TU_CONG_NO': line.get('NGAY_CHUNG_TU_CONG_NO', ''),
                'SO_CHUNG_TU_CONG_NO': line.get('SO_CHUNG_TU_CONG_NO', ''),
                'SO_HOA_DON_CONG_NO': line.get('SO_HOA_DON_CONG_NO', ''),
                'SO_CONG_NO_THANH_TOAN_LAN_NAY': line.get('SO_CONG_NO_THANH_TOAN_LAN_NAY', ''),   
                'CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI' : line.get('CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI', ''),  
                'ID_DTCT': line.get('ID_DTCT', ''), 
                'LOAI_CHUNG_TU_THANH_TOAN': line.get('LOAI_CHUNG_TU_THANH_TOAN', ''), 
                'LOAI_CHUNG_TU_CONG_NO': line.get('LOAI_CHUNG_TU_CONG_NO', ''), 
            })
        
        return record