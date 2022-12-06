# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
import json
import ast

class ASSET_CHON_CHUNG_TU_TSCD_FORM(models.Model):
    _name = 'account.ex.chon.chung.tu.form'
    _auto = False
    _description = ''
    
    LOAI_CHUNG_TU = fields.Selection([('PHIEU_CHI', 'Phiếu chi '), ('SEC_UY_NHIEM_CHI', ' Séc/Ủy nhiệm chi '), ('XUAT_KHO_KHAC', 'Xuất kho khác'), ('CHUNG_TU_NGHIEP_VU_KHAC', 'Chứng từ nghiệp vụ khác '), ('MUA_HANG_KHONG_QUA_KHO', 'Mua hàng không qua kho'), ('MUA_DICH_VU', ' Mua dịch vụ'), ('GHI_GIAM_TAI_SAN_CO_DINH', ' Ghi giảm tài sản cố định'), ('QUYET_TOAN_TAM_UNG', ' Quyết toán tạm ứng'), ('TAT_CA', ' Tất cả  '), ], string='Loại chứng từ', help='Loại chứng từ',required=True,default='TAT_CA')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ ', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ', help='Đến ngày',default=fields.Datetime.now)
    CHUNG_TU_CHON = fields.Selection([('GHI_TANG', 'Ghi tăng'), ('DIEU_CHINH', 'Điều chỉnh'), ], string='Chứng từ chọn', help='Chứng từ chọn', default='GHI_TANG')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NGUON_GOC_HT_JSON = fields.Char()
    LAY_DU_LIEU_JSON = fields.Text()

    ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS = fields.One2many('account.ex.chon.chung.tu.chi.tiet', 'CHON_CHUNG_TU_ID', string='chọn chứng từ tscd chi tiết')
    
    @api.model
    def default_get(self, fields): 
      rec = super(ASSET_CHON_CHUNG_TU_TSCD_FORM, self).default_get(fields)
      arr_nguon_goc_ht = []
      nguon_goc_ht = self._context.get('ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS')
      # i = 0
      if nguon_goc_ht:
        for line in nguon_goc_ht:
          # i += 1
          arr_nguon_goc_ht.append({
            'ID_GOC' : line.get('ID_GOC'),
            'MODEL_GOC' : line.get('MODEL_GOC'),
          })
        rec['NGUON_GOC_HT_JSON'] = json.dumps(arr_nguon_goc_ht)
        # rec['name'] = ''
      return rec

    @api.model
    def lay_du_lieu_cac_chung_tu(self,args):
        loai_ct = []
        new_line_so_chung_tu  =[[5]]
        if 'loai_chung_tu' in args:
            if args.get('loai_chung_tu') == 'PHIEU_CHI':
                    loai_ct += ['1010','1020','1500','1510','1520','1530','1560']
            elif args.get('loai_chung_tu') == 'SEC_UY_NHIEM_CHI':
                    loai_ct += ['1510']
            elif args.get('loai_chung_tu') == 'XUAT_KHO_KHAC':
                    loai_ct += ['2022']
            elif args.get('loai_chung_tu') == 'CHUNG_TU_NGHIEP_VU_KHAC':
                    loai_ct += ['4010','4015']
            elif args.get('loai_chung_tu') == 'MUA_HANG_KHONG_QUA_KHO':
                    loai_ct += ['318']
            elif args.get('loai_chung_tu') == 'MUA_DICH_VU':
                    loai_ct += ['330','331','332','333','334']
            elif args.get('loai_chung_tu') == 'GHI_GIAM_TAI_SAN_CO_DINH':
                    loai_ct += ['251']
            elif args.get('loai_chung_tu') == 'QUYET_TOAN_TAM_UNG':
                    loai_ct += ['-1']
            elif args.get('loai_chung_tu') == 'TAT_CA':
                    loai_ct += ['1010','1020','1500','1510','1520','1530','1560','1510','2022','4010','4015','318','330','331','332','333','334','251']
        du_lieu_list = self.lay_du_lieu_chung_tu(tuple(loai_ct),args.get('tu_ngay'),args.get('den_ngay'))
        for line in du_lieu_list:
            new_line_so_chung_tu += [(0, 0, {
                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN'),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
                'SO_CHUNG_TU': line.get('SO_CHUNG_TU'),
                'DIEN_GIAI': line.get('DIEN_GIAI'),
                'TK_NO_ID': line.get('TK_NO_ID'),
                'TK_CO_ID': line.get('TK_CO_ID'),
                'SO_TIEN': line.get('SO_TIEN'),
                })]
        return new_line_so_chung_tu
        

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')

    

    def lay_du_lieu_chung_tu(self,loai_ct,tu_ngay,den_ngay):
        record = []
        params = {
            'LOAI_CT' : loai_ct,
            'TU_NGAY' : tu_ngay,
            'DEN_NGAY' : den_ngay,
            }

        query = """   

        SELECT
  row_number() OVER (PARTITION BY true::boolean) AS id,
  kq."ID_GOC",
  kq."MODEL_GOC",
  kq."NGAY_HACH_TOAN",
  kq."NGAY_CHUNG_TU",
  kq."SO_CHUNG_TU",
  kq."DIEN_GIAI_CHUNG",
  kq."TK_NO_ID",
  kq."TK_CO_ID",
  kq."SO_TIEN"
FROM (
  SELECT *FROM tien_ich_tim_kiem_chung_tu
) kq
WHERE kq."LOAI_CHUNG_TU" in %(LOAI_CT)s
      AND kq."TINH_TRANG_GHI_SO" = True
      AND kq."NGAY_HACH_TOAN" BETWEEN %(TU_NGAY)s AND %(DEN_NGAY)s

GROUP BY
          kq."ID_GOC",
          kq."MODEL_GOC",
          kq."NGAY_HACH_TOAN",
          kq."NGAY_CHUNG_TU",
          kq."SO_CHUNG_TU",
          kq."DIEN_GIAI_CHUNG",
          kq."TK_NO_ID",
          kq."TK_CO_ID",
          kq."SO_TIEN"

        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
                'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
                'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
                'TK_NO_ID': line.get('TK_NO_ID', ''),
                'TK_CO_ID': line.get('TK_CO_ID', ''),
                'SO_TIEN': line.get('SO_TIEN', ''),
                'ID_GOC': line.get('ID_GOC', ''),
                'MODEL_GOC': line.get('MODEL_GOC', ''),
            })
        
        return record