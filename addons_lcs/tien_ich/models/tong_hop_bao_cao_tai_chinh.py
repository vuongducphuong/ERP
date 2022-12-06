# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BAO_CAO_TAI_CHINH(models.Model):
    _name = 'tong.hop.bao.cao.tai.chinh'
    _description = ''
    _inherit = ['mail.thread']

    BCTC_DA_DUOC_KIEM_TRA = fields.Boolean(string='BCTC đã được kiểm tra', help='Bctc đã được kiểm tra')
    Y_KIEN_KIEM_TOAN = fields.Selection([('Y_KIEN_TRAI_NGUOC', 'Ý kiến trái ngược'), ('Y_KIEN_TU_CHOI_DUA_Y_KIEN', ' Ý kiến từ chối đưa ý kiến'), ('Y_KIEN_NGOAI_TRU', ' Ý kiến ngoại trừ'), ('Y_KIEN_CHAP_NHAN_TOAN_PHAN', ' Ý kiến chấp nhận toàn phần'), ], string='Ý kiến kiểm toán', help='Ý kiến kiểm toán')
    CHENH_LECH_TAI_SAN_NGUON_VON = fields.Char(string='Chênh lệch tài sản-nguồn vốn', help='Chênh lệch tài sản nguồn vốn')
    DAU_KY = fields.Float(string='Đầu kỳ:', help='Đầu kỳ',digits= decimal_precision.get_precision('VND'))
    CUOI_KY = fields.Float(string='Cuối kỳ:', help='Cuối kỳ',digits= decimal_precision.get_precision('VND'))
    NGUOI_LAP_BIEU = fields.Char(string='Người lập biểu(*)', help='Người lập biểu')
    GIAM_DOC = fields.Char(string='Giám đốc(*)', help='Giám đốc')
    NGAY_LAP = fields.Date(string='Ngày lập(*)', help='Ngày lập',default=fields.Datetime.now)
    name = fields.Char(string='Name', help='Name',related='NGUOI_LAP_BIEU',store=True, oldname='NAME')


    
    TEN = fields.Char(string='Tên ', help='Tên')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')
    #FIELD_IDS = fields.One2many('model.name')
    B01_DN_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn')
    B02_DN_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn')
    B03_DN_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn')
    B03_DN_GT_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn')
    
    TONG_HOP_BAO_CAO_TAI_CHINH_CHI_TIET_B02_DN_IDS = fields.One2many('tong.hop.bao.cao.tai.chinh.chi.tiet.b02.dn', 'BAO_CAO_TAI_CHINH_ID', string='Báo cáo tài chính chi tiết B02 DN')
    TONG_HOP_BAO_CAO_TAI_CHINH_CHI_TIET_B03_DN_IDS = fields.One2many('tong.hop.bao.cao.tai.chinh.chi.tiet.b03.dn', 'BAO_CAO_TAI_CHINH_ID', string='Báo cáo tài chính chi tiết B03 DN')
    TONG_HOP_BAO_CAO_TAI_CHINH_CHI_TIET_B01_DN_IDS = fields.One2many('tong.hop.bao.cao.tai.chinh.chi.tiet.b01.dn', 'BAO_CAO_TAI_CHINH_ID', string='Báo cáo tài chính chi tiết B01 DN')
    TONG_HOP_BAO_CAO_TAI_CHINH_CHI_TIET_B03_DN_GT_IDS = fields.One2many('tong.hop.bao.cao.tai.chinh.chi.tiet.b03.dn.gt', 'BAO_CAO_TAI_CHINH_ID', string='Báo cáo tài chính chi tiết B03 DN GT')

    TONG_HOP_BCTC_THEM_PHU_LUC_CHI_TIET_FORM_IDS = fields.One2many('tong.hop.bctc.them.phu.luc.form', 'BAO_CAO_TAI_CHINH_ID', string='BCTC thêm phụ lục chi tiết form')
    DEN_NGAY_BAT_RA = fields.Date(string='Đến', help='Đến')
    DOANH_NGHIEP_SELECTION_BAT_RA = fields.Char(string='Doanh nghiệp mẫu in', help='Doanh nghiệp')
    TU_NGAY_BAT_RA = fields.Date(string='Đến', help='Đến')
    KY_BAO_CAO_LIST = fields.Char(string='KỲ báo cáo', help='KỲ')
    
    TEN_KY_BAO_CAO = fields.Char(string='KỲ mẫu in', help='KỲ')
    NAM = fields.Integer(string='Năm', help='Năm')
    AUTO_SELECT = fields.Boolean()
    CAPTION_THEO_KY_B01_MOI = fields.Char(string='caption theo kỳ B01 mới', help='caption theo kỳ B01 mới')
    CAPTION_THEO_KY_B01_CU = fields.Char(string='caption theo kỳ B01 cũ', help='caption theo kỳ B01 cũ')

    CAPTION_THEO_KY_CON_LAI_MOI = fields.Char(string='caption theo kỳ còn lại mới', help='caption theo kỳ còn lại mới')
    CAPTION_THEO_KY_CON_LAI_CU = fields.Char(string='caption theo kỳ còn lại mới', help='caption theo kỳ còn lại mới')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    HE_THONG_TAI_KHOAN = fields.Char(string='Hệ thống tài khoản', help='Hệ thống tài khoản')

    @api.model
    def default_get(self, fields_list):
      result = super(TONG_HOP_BAO_CAO_TAI_CHINH, self).default_get(fields_list)
      result['NGUOI_LAP_BIEU'] = 'ADMIN'
      result['GIAM_DOC'] = 'Vũ Ngọc Đức'
      result['TEN'] = 'Báo cáo tài chính'

      

      ky_bao_cao= self.get_context('default_KY')
      
      nam= self.get_context('default_NAM')
      if nam:
        result['NAM'] = nam
      doanh_nghiep_selection= self.get_context('default_DOANH_NGHIEP_SELECTION')
      den_ngay= self.get_context('default_DEN')
      tu_ngay= self.get_context('default_TU')
      if doanh_nghiep_selection:
        if self.get_context('default_DOANH_NGHIEP_SELECTION')=='DOANH_NGHIEP_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC':
          result['DOANH_NGHIEP_SELECTION_BAT_RA']='(Áp dụng cho doanh nghiệp đáp ứng giả định hoạt động liên tục)'
      if den_ngay:
        result['DEN_NGAY_BAT_RA']=den_ngay
      if tu_ngay:
        result['TU_NGAY_BAT_RA']=tu_ngay

      if ky_bao_cao:
        if self.get_context('default_KY')=='NAM_NAY':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối năm'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu năm'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Năm nay'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Năm trước'
          result['KY_BAO_CAO_LIST'] = 'Năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Năm ' + str(nam)
        elif self.get_context('default_KY')=='6_THANG_DAU_NAM':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = '6 tháng đầu năm  ' + str(nam)
          result['TEN_KY_BAO_CAO'] ='Từ ngày ' + tu_ngay +' đến ngày ' + den_ngay
        elif self.get_context('default_KY')=='6_THANG_CUOI_NAM':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = '6 tháng cuối năm  ' + str(nam)
          result['TEN_KY_BAO_CAO'] ='Từ ngày ' + tu_ngay +' đến ngày ' + den_ngay
        elif self.get_context('default_KY')=='QUY_1':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối quý'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu quý'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Qúy này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Qúy trước'
          result['KY_BAO_CAO_LIST'] = 'Qúy 1 năm    ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Qúy 1 năm  ' + str(nam)
        elif self.get_context('default_KY')=='QUY_2':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối quý'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu quý'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Qúy này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Qúy trước'
          result['KY_BAO_CAO_LIST'] = 'Qúy 2 năm    ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Qúy 2 năm  ' + str(nam)
        elif self.get_context('default_KY')=='QUY_3':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối quý'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu quý'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Qúy này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Qúy trước'
          result['KY_BAO_CAO_LIST'] = 'Qúy 3 năm    ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Qúy 3 năm  ' + str(nam)
        elif self.get_context('default_KY')=='QUY_4':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối quý'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu quý'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Qúy này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Qúy trước'
          result['KY_BAO_CAO_LIST'] = 'Qúy 4 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Qúy 4 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_1':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 1 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 1 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_2':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 2 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 2 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_3':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 3 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 3 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_4':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 4 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 4 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_5':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 5 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 5 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_6':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 6 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 6 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_7':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 7 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 7 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_8':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 8 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 8 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_9':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 9 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 9 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_10':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 10 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 10 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_11':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 11 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 11 năm ' + str(nam)
        elif self.get_context('default_KY')=='THANG_12':
          result['CAPTION_THEO_KY_B01_MOI'] = 'Số cuối kỳ'
          result['CAPTION_THEO_KY_B01_CU'] = 'Số đầu kỳ'
          result['CAPTION_THEO_KY_CON_LAI_MOI'] = 'Kỳ này'
          result['CAPTION_THEO_KY_CON_LAI_CU'] = 'Kỳ trước'
          result['KY_BAO_CAO_LIST'] = 'Tháng 12 năm ' + str(nam)
          result['TEN_KY_BAO_CAO'] = 'Tháng 12 năm ' + str(nam)



      lay_du_lieu_tham_so =self.get_context('default_LAY_DU_LIEU_THAM_SO')
      
      #tạo vòng lặp for trong context vừa truyền 
        #nếu mã báo cáo== B02-dn
          #B02_DN_BOLEAN ==True
        #nếu mã báo cáo ==B01-DN
          #B01_DN_BOLEAN ==True
        #nếu mã báo cáo== B03-dn
          #B03_DN_BOLEAN ==True
        #nếu mã báo cáo ==B03-DN-GT
          #B03_DN_GT_BOLEAN ==True
      if lay_du_lieu_tham_so:
        arr_them_phu_luc_chi_tiet=[]        
        result['TONG_HOP_BCTC_THEM_PHU_LUC_CHI_TIET_FORM_IDS'] = []
        for item in lay_du_lieu_tham_so:
          value=item['MA_BAO_CAO_ID']

          report = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].search([('id', '=', value)])
          arr_them_phu_luc_chi_tiet +=[(0,0,{
                'AUTO_SELECT'  :item['AUTO_SELECT'],  
                'MA_PHU_LUC_ID':report.id,
                'TEN_PHU_LUC'  :report.TEN_BAO_CAO,                
            })]
          if item['AUTO_SELECT']:
            if report.MA_BAO_CAO == 'B01-DN':
                result['B01_DN_BOLEAN'] =True
            elif report.MA_BAO_CAO == 'B02-DN':
                result['B02_DN_BOLEAN'] =True
            elif report.MA_BAO_CAO == 'B03-DN':
                result['B03_DN_BOLEAN'] =True
            elif report.MA_BAO_CAO == 'B03-DN-GT':
                result['B03_DN_GT_BOLEAN'] =True
        result['TONG_HOP_BCTC_THEM_PHU_LUC_CHI_TIET_FORM_IDS'] = arr_them_phu_luc_chi_tiet
      return result