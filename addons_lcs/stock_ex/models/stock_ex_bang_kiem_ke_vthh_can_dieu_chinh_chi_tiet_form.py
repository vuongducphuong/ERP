# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM(models.Model):
     _name = 'stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form'
     _description = ''
     _inherit = ['mail.thread']
     MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
     TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
     CO_MA_QUY_CACH = fields.Boolean()
     MA_KHO_ID = fields.Many2one('danh.muc.kho', string='Mã kho', help='Mã kho')
     DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đvt')
     SO_LUONG_SO_KE_TOAN = fields.Float(string='Số lượng sổ kế toán', help='Số lượng sổ kế toán', digits=decimal_precision.get_precision('SO_LUONG'))
     SO_LUONG_KIEM_KE = fields.Float(string='Số lượng kiểm kê', help='Số lượng kiểm kê', digits=decimal_precision.get_precision('SO_LUONG'))
     SO_LUONG_CHENH_LECH = fields.Float(string='Số lượng chênh lệch', help='Số lượng chênh lệch', digits=decimal_precision.get_precision('SO_LUONG'))
     GIA_TRI_SO_KE_TOAN = fields.Float(string='Giá trị sổ kế toán', help='Giá trị sổ kế toán',digits= decimal_precision.get_precision('VND'))
     GIA_TRI_KIEM_KE = fields.Float(string='Giá trị kiểm kê', help='Giá trị kiểm kê',digits= decimal_precision.get_precision('VND'))
     GIA_TRI_CHENH_LECH = fields.Float(string='Giá trị chênh lệch', help='Giá trị chênh lệch',digits= decimal_precision.get_precision('VND'))
     PHAM_CHAT_CON_TOT = fields.Float(string='Còn tốt 100%', help='Phẩm chất còn tốt')
     KEM_PHAM_CHAT = fields.Float(string='Kém phẩm chất', help='Kém phẩm chất')
     MAT_PHAM_CHAT = fields.Float(string='Mất phẩm chất', help='Mất phẩm chất')
     XU_LY = fields.Selection([('0', 'Không xử lý'), ('1', 'Nhập kho'),('2','Xuất kho')],string='Xử lý',compute='set_xu_ly',store=True)
     SO_LO = fields.Char(string='Số lô', help='Số lô')
     HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
     MA_QUY_CACH_1 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 1')
     MA_QUY_CACH_2 = fields.Char(string='Mã quy cách 2', help='Mã quy cách 2')
     MA_QUY_CACH_3 = fields.Char(string='Mã quy cách 3', help='Mã quy cách 3')
     MA_QUY_CACH_4 = fields.Char(string='Mã quy cách 4', help='Mã quy cách 4')
     MA_QUY_CACH_5 = fields.Char(string='Mã quy cách 5', help='Mã quy cách 5')
     name = fields.Char(string='Name', oldname='NAME')
     KIEM_KE_BANG_KIEM_KE_VTHH_ID = fields.Many2one('stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form', string='Kiểm kê bảng kiểm kê vthh', help='Mã hàng', ondelete='cascade')
     STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH_IDS = fields.One2many('stock.ex.chung.tu.luu.ma.quy.cach', 'KIEM_KE_KHO_CHI_TIET_ID', string='Chứng từ lưu mã quy cách')
     HIEN_THI_MA_QUY_CACH_KHONG_CON_TON = fields.Boolean(string='Hiển thị cả mã quy cách không còn tồn', help='Hiển thị cả mã quy cách không còn tồn')
     sequence = fields.Integer()

     @api.onchange('MA_HANG_ID')
     def onchange_product_id(self):
          if self.MA_HANG_ID:
               self.CO_MA_QUY_CACH = True if len(self.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_MA_QUY_CACH_IDS) > 0 else False
               vat_tu_hang_hoa = self.lay_du_lieu_khi_chon_1_dong('2019-03-01',81,94,0,self.MA_HANG_ID.id,0)
               if vat_tu_hang_hoa:
                    self.TEN_HANG = vat_tu_hang_hoa[0].get('TEM_HANG')
                    self.MA_KHO_ID = vat_tu_hang_hoa[0].get('MA_KHO_ID')
                    self.DVT_ID = vat_tu_hang_hoa[0].get('DVT_ID')
                    self.SO_LUONG_SO_KE_TOAN = vat_tu_hang_hoa[0].get('SO_LUONG_TREN_SO')
                    self.SO_LUONG_KIEM_KE = vat_tu_hang_hoa[0].get('SO_LUONG_KIEM_KE')
                    self.SO_LUONG_CHENH_LECH = vat_tu_hang_hoa[0].get('SO_LUONG_CHENH_LECH')


     @api.model
     def lay_chung_tu_luu_ma_quy_cach(self, args):
          result = None
          if len(self.STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH_IDS) == 0:
               result = {'STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH_IDS': [(0,0,{'DEN_NGAY': '2018-01-01'})]}
          return result

     @api.onchange('SO_LUONG_KIEM_KE')
     def onchange_sl_kiem_ke(self):
          for record in self:
               # if record.SO_LUONG_SO_KE_TOAN > record.SO_LUONG_KIEM_KE:
               #      raise ValidationError('Số lượng kiểm kê phải lớn hơn hoặc bằng số lượng kế toán.')
               # else:
               record.SO_LUONG_CHENH_LECH = record.SO_LUONG_KIEM_KE - record.SO_LUONG_SO_KE_TOAN
               record.PHAM_CHAT_CON_TOT = record.SO_LUONG_KIEM_KE
               if record.SO_LUONG_SO_KE_TOAN != 0:
                    record.GIA_TRI_KIEM_KE = (record.GIA_TRI_SO_KE_TOAN/record.SO_LUONG_SO_KE_TOAN)*record.SO_LUONG_KIEM_KE

     @api.onchange('GIA_TRI_KIEM_KE')
     def onchange_gia_tri_kiem_ke(self):
          for record in self:
               # if record.GIA_TRI_SO_KE_TOAN > record.GIA_TRI_KIEM_KE:
               #      raise ValidationError('Giá trị kiểm kê phải lớn hơn hoặc bằng giá trị sổ kế toán.')
               # else:
               record.GIA_TRI_CHENH_LECH = record.GIA_TRI_KIEM_KE - record.GIA_TRI_SO_KE_TOAN
     

        
     @api.depends('SO_LUONG_CHENH_LECH')
     def set_xu_ly(self):
         for record in self:
             if record.SO_LUONG_CHENH_LECH > 0:
                 record.XU_LY ='1'
             elif record.SO_LUONG_CHENH_LECH < 0:
                 record.XU_LY ='2'
             else:
                 record.XU_LY ='0'

                
     def lay_du_lieu_khi_chon_1_dong(self,den_ngay,chi_nhanh,Kho_id,dvt,ma_hang,chi_tiet_theo):
          record = []
          params = {
            'DEN_NGAY': den_ngay,
            'CHI_NHANH_ID' : chi_nhanh,
            'KHO_ID' : Kho_id,
            'STT_DVT' : dvt,
            'MA_HANG_ID' : ma_hang,
            'CHI_TIET_THEO' : chi_tiet_theo,
            }

          query = """   

        SELECT
        0 AS "ID_CHUNG_TU" ,
        0 AS "CHI_TIET_ID" ,
        I.id AS "MA_HANG_ID" ,
        I."MA" AS "MA_HANG" ,
        I."TEN" AS "TEN_HANG" ,
        ST.id AS "MA_KHO_ID" ,
        ST."MA_KHO" ,
        ST."TEN_KHO" ,
        CASE WHEN 0 = 0 THEN 0
             ELSE UC."STT"
        END AS "THU_TU_TRONG_CHUNG_TU" ,
        CASE WHEN 0 = 0 THEN I."DVT_CHINH_ID"/*Nếu loại Đơn vị tính truyền vào = 0 tức là đơn vị tính chính thì lấy ID đơn vị tính trên danh mục vật tư hàng hóa*/
             ELSE UC."DVT_ID"                  /* nếu khác 0 thì lấy ID theo đơn vị tính chuyển đổi*/
        END AS "DVT_ID" ,
        CASE WHEN 0 = 0 THEN UI.name/*Tên về mặt ý tưởng cũng tương tự như cách lấy "DVT_ID"*/
             ELSE U.name
        END AS "TEN_DVT" ,
        ROUND(cast(SUM(CASE WHEN U.id IS NOT NULL
                            AND IL."DVT_ID" = U.id
                       THEN IL."SO_LUONG_NHAP" - IL."SO_LUONG_XUAT"
                       ELSE ( IL."SO_LUONG_NHAP_THEO_DVT_CHINH"
                              - IL."SO_LUONG_XUAT_THEO_DVT_CHINH" )
                            * coalesce(UC."TI_LE_CHUYEN_DOI", 1)
                  END)AS NUMERIC), 2) AS "SO_LUONG_TREN_SO" /*Số lượng tồn trên số sách tính toán ra theo đơn vị tính truyền vào*/,
        CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_KIEM_KE" /*Số lượng kiểm kê*/,
        CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_CHENH_LECH" /*Chên lệch về số lượng giữa kiểm kê và sổ sách*/,
        coalesce(SUM(IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT"), 0) AS "SO_TIEN_QUY_DOI_TREN_SO"/*Giá trị tồn trên sổ sách*/ ,
        CAST(0 AS DECIMAL(18, 4)) AS "SO_TIEN_QUY_DOI_KIEM_KE"/*Giá trị theo kiểm kê*/ ,
        CAST(0 AS DECIMAL(18, 4)) AS "SO_TIEN_QUY_DOI_CHENH_LECH"/*Chênh lệch về giá trị giữa kiểm kê thực tế và sổ sách*/
FROM    so_kho_chi_tiet AS IL
        INNER JOIN danh_muc_kho ST ON IL."KHO_ID" = ST.id
        INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU.id
        INNER JOIN danh_muc_vat_tu_hang_hoa I ON IL."MA_HANG_ID" = I.id
        LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC ON I.id = IIUC."VAT_TU_HANG_HOA_ID"
                                                      AND IIUC."STT" = 0
        LEFT JOIN danh_muc_don_vi_tinh UI ON I."DVT_CHINH_ID" = UI.id/*lấy ra thông tin Đơn vị tính chính trên danh mục*/

        LEFT JOIN ( SELECT  IIUC."VAT_TU_HANG_HOA_ID" AS "MA_HANG_ID" ,/*Lấy ra hệ số quy đổi*/
                            "DVT_ID" ,
                            IIUC."STT" ,
                            ( CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_CHIA'
                                   THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                   WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0 THEN 1
                                   ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                              END ) AS "TI_LE_CHUYEN_DOI"
                    FROM    danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                    WHERE   IIUC."STT" = 0
                  ) UC ON I.id = UC."MA_HANG_ID"
        /*lấy ra thông tin đơn vị tính theo loại đơn vị tính truyền vào*/
        LEFT JOIN danh_muc_don_vi_tinh U ON ( UC."MA_HANG_ID" IS NULL
                                  AND U.id = I.id
                                )
                                OR ( UC."MA_HANG_ID" IS NOT NULL
                                     AND UC."DVT_ID" = U.id
                                   )
         LEFT JOIN (SELECT DISTINCT "CHI_TIET_ID" FROM stock_ex_chung_tu_luu_ma_quy_cach )AS ISN ON ISN."CHI_TIET_ID" = IL."CHI_TIET_ID"
WHERE   IL."MA_HANG_ID" = %(MA_HANG_ID)s
        AND IL."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
        AND IL."KHO_ID" = %(KHO_ID)s
        AND IL."NGAY_HACH_TOAN" <= '2019-03-01'
        AND (%(CHI_TIET_THEO)s = 0 OR (%(CHI_TIET_THEO)s = 1 AND IL."SO_LO" IS NULL AND IL."NGAY_HET_HAN" IS NULL ) OR (%(CHI_TIET_THEO)s = 2 AND  ISN."CHI_TIET_ID" IS NULL))
GROUP BY I.id ,
        I."MA" ,
        I."TEN" ,
        ST.id ,
        ST."MA_KHO" ,
        ST."TEN_KHO" ,
        UC."DVT_ID",
        CASE WHEN %(STT_DVT)s = 0 THEN 0
             ELSE UC."STT"
        END ,
        CASE WHEN %(STT_DVT)s = 0 THEN I.id
             ELSE UC."DVT_ID"
        END ,
        CASE WHEN %(STT_DVT)s = 0 THEN UI.name
             ELSE U.name
        END

        """  
          cr = self.env.cr

          cr.execute(query, params)
          for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
               record.append({
                'TEN_HANG': line.get('TEN_HANG', ''),
                'MA_KHO_ID': line.get('MA_KHO_ID', ''),
                'DVT_ID': line.get('DVT_ID', ''),
                'SO_LUONG_TREN_SO': line.get('SO_LUONG_TREN_SO', ''),
                'SO_LUONG_KIEM_KE': line.get('SO_LUONG_KIEM_KE', ''),
                'SO_LUONG_CHENH_LECH': line.get('SO_LUONG_CHENH_LECH', ''),
            })
        
          return record