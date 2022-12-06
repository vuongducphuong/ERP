# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from operator import itemgetter
import logging

_logger = logging.getLogger(__name__)
class TIEN_ICH_BAO_TRI_DU_LIEU(models.Model):
    _name = 'tien.ich.bao.tri.du.lieu'
    _description = ''
    _auto = False

    KY = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ', help='Kỳ', default='NAM_NAY',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    GHI_SO_CAC_CHUNG_TU_CHUA_GHI_SO = fields.Boolean(string='Ghi sổ các chứng từ chưa ghi sổ', help='Ghi sổ các chứng từ chưa ghi sổ')
    TINH_LAI_GIA_XUAT_KHO = fields.Boolean(string='Tính lại giá xuất kho', help='Tính lại giá xuất kho')
    TINH_LAI_TY_GIA_XUAT_QUY = fields.Boolean(string='Tính lại tỷ giá xuất quỹ', help='Tính lại tỷ giá xuất quỹ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    @api.onchange('KY')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY, 'TU_NGAY', 'DEN_NGAY')

    def action_view_result(self):
        start_date = self.get_context('TU_NGAY')
        end_date = self.get_context('DEN_NGAY')
        post_all = self.get_context('GHI_SO_CAC_CHUNG_TU_CHUA_GHI_SO') == 'True'
        # post và unpost chỉ dành cho testing
        # post = True
        # unpost = True
        # Nếu bỏ ghi sổ
        # if unpost:
        docs = self.batch_unposted(start_date,end_date,post_all)
        # if post:
        for rec in docs:
            record = rec.get('record')
            # Khi bảo trì, chứng từ có SOURCE_ID sẽ được ghi sổ từ chứng từ cha
            # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3435/
            if not getattr(record, 'SOURCE_ID', None):
                record.with_context({'bao_tri': True}).action_ghi_so()
        
        # Nếu chỉ ghi sổ
        # elif post:
        #     self.batch_post(start_date,end_date,post_all,True)

    # post = True nếu là ghi sổ theo lô, post=False nếu là bỏ ghi sổ theo lô
    def batch_unposted(self, start_date=False, end_date=False,post_all=False):#, posted=False):
        docs = []
        date_fields = ['NGAY_HACH_TOAN','NGAY_GHI_TANG', 'NGAY', 'NGAY_CHUNG_TU','NGAY_HOA_DON']
        for model in self.env:
            all_fields = self.env[model]._fields
            if self.env[model]._auto and 'state' in all_fields:
                # if model != 'purchase.document':
                #     continue
                for date_field in date_fields:
                    if date_field in all_fields:
                        domains = []
                        if start_date:
                            domains += [(date_field,'>=',start_date)]
                        if end_date:
                            domains += [(date_field,'<=',end_date)]
                        for record in self.env[model].search(domains):
                            # if posted:
                            #     if record.state == 'chua_ghi_so':
                            #         record.action_ghi_so()
                            # else:
                            if post_all or record.state == 'da_ghi_so':
                                docs += [{'date': getattr(record, date_field), 'record': record}]
                            # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1778
                            # if record.state == 'da_ghi_so':
                            #     record.bo_ghi_so()
                        break
        # Xóa tất cả các sổ trong quãng thời gian đó
        # if not posted:
        dom = []
        if start_date:
            dom += [('NGAY_HACH_TOAN','>=',start_date)]
        if end_date:
            dom += [('NGAY_HACH_TOAN','<=',end_date)]
        # dom += [('MODEL_CHUNG_TU','=', 'purchase.document')]
        DANH_SACH = {'SO_CAI_ID':'so.cai.chi.tiet','SO_KHO_ID':'so.kho.chi.tiet','SO_BAN_HANG_ID':'so.ban.hang.chi.tiet','SO_MUA_HANG_ID':'so.mua.hang.chi.tiet','SO_CONG_NO_ID':'so.cong.no.chi.tiet','SO_THUE_ID':'so.thue.chi.tiet','SO_CCDC_ID':'so.ccdc.chi.tiet','SO_TSCD_ID':'so.tscd.chi.tiet'}
        for item in DANH_SACH:
            self.env[DANH_SACH.get(item)].search(dom).unlink()

        return sorted(docs, key=itemgetter('date'))