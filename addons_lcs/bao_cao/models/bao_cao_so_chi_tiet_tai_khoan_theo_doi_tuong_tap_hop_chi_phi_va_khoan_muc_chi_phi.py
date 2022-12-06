# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_CHI_TIET_TK_THEO_DOI_TUONG_VA_CHI_PHI(models.Model):
    _name = 'bao.cao.so.chi.tiet.tk.theo.doi.tuong.va.chi.phi'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('DOI_TUONG_TAP_HOP_CHI_PHI', 'Đối tượng tập hợp chi phí'),('CONG_TRINH', 'Công trình'), ('DON_HANG', 'Đơn hàng'),('HOP_DONG', 'Hợp đồng'),], string='Thống kê theo', help='Thống kê theo',default='DOI_TUONG_TAP_HOP_CHI_PHI',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='true')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng THCP')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    TEN_KHOAN_MUC_CP = fields.Char(string='Tên khoản mục CP', help='Tên khoản mục CP')
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    HOP_DONG_DU_AN = fields.Char(string='Hợp đồng/Dự án', help='Hợp đồng/Dự án')
    TAI_KHOAN = fields.Char(string='Tài khoản', help='Tài khoản')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    SO_TIEN_NO = fields.Float(string='Số tiền nợ', help='Số tiền nợ',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_CO = fields.Float(string='Số tiên có', help='Số tiên có',digits=decimal_precision.get_precision('VND'))

    #hop dong#
    TAIKHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    CHIPHI_IDS=fields.One2many('danh.muc.khoan.muc.cp')
    HOP_DONG_BAN_IDS=fields.One2many('sale.ex.hop.dong.ban')
    
     #don hang#
    TAIKHOAN2_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    CHIPHI2_IDS=fields.One2many('danh.muc.khoan.muc.cp')
    DONHANG2_IDS=fields.One2many('account.ex.don.dat.hang')
     #congtrinh#
    TAIKHOAN3_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    CHIPHI3_IDS=fields.One2many('danh.muc.khoan.muc.cp')
    CONG_TRINH_IDS=fields.One2many('danh.muc.cong.trinh')
     #doi tuong#
    TAIKHOAN4_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    DOITUONG_IDS=fields.One2many('danh.muc.doi.tuong.tap.hop.chi.phi')
    CHIPHI4_IDS=fields.One2many('danh.muc.khoan.muc.cp')
  

  
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

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
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'THONG_KE_THEO': '',
                'CHI_NHANH_ID': '',
                'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC': '',
                'KY_BAO_CAO': '',
                'TU': '',
                'DEN': '',
                'NGAY_HACH_TOAN': '',
                'NGAY_CHUNG_TU': '',
                'SO_CHUNG_TU': '',
                'DIEN_GIAI': '',
                'TK_DOI_UNG': '',
                'SO_TIEN_NO': '',
                'SO_TIEN_CO': '',
                })
        return record

    #@api.onchange('field_name')
    #def _cap_nhat(self):
    #    for item in self:
    #        item.FIELDS_IDS = self.env['model_name'].search([])

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_CHI_TIET_TK_THEO_DOI_TUONG_VA_CHI_PHI, self).default_get(fields_list)
        tai_khoans = self.env['danh.muc.he.thong.tai.khoan'].search([])
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        chi_phis = self.env['danh.muc.khoan.muc.cp'].search([])
        don_hangs = self.env['account.ex.don.dat.hang'].search([])
        doi_tuong_thcps = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
        cong_trinhs = self.env['danh.muc.cong.trinh'].search([])
        hop_dong_bans = self.env['sale.ex.hop.dong.ban'].search([])
        if chi_nhanh:
             result['CHI_NHANH_ID'] = chi_nhanh.id
        if tai_khoans:
            result['TAIKHOAN_IDS'] = tai_khoans.ids
            result['TAIKHOAN2_IDS'] = tai_khoans.ids
            result['TAIKHOAN3_IDS'] = tai_khoans.ids
            result['TAIKHOAN4_IDS'] = tai_khoans.ids
        if chi_phis:
            result['CHIPHI_IDS'] = chi_phis.ids
            result['CHIPHI2_IDS'] = chi_phis.ids
            result['CHIPHI3_IDS'] = chi_phis.ids
            result['CHIPHI4_IDS'] = chi_phis.ids
        if don_hangs:
            result['DONHANG2_IDS'] = don_hangs.ids
        if doi_tuong_thcps :
            result['DOITUONG_IDS'] = doi_tuong_thcps.ids
        if cong_trinhs : 
            result['CONG_TRINH_IDS'] = cong_trinhs.ids
        if hop_dong_bans : 
            result['HOP_DONG_BAN_IDS'] = hop_dong_bans.ids

        return result
    ### END IMPLEMENTING CODE ###

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        TAIKHOAN4_IDS = params['TAIKHOAN4_IDS'] if 'TAIKHOAN4_IDS' in params.keys() else 'False'
        DOITUONG_IDS = params['DOITUONG_IDS'] if 'DOITUONG_IDS' in params.keys() else 'False'
        CHIPHI4_IDS = params['CHIPHI4_IDS'] if 'CHIPHI4_IDS' in params.keys() else 'False'
        TAIKHOAN3_IDS = params['TAIKHOAN3_IDS'] if 'TAIKHOAN3_IDS' in params.keys() else 'False'
        CHIPHI3_IDS = params['CHIPHI3_IDS'] if 'CHIPHI3_IDS' in params.keys() else 'False'
        CONG_TRINH_IDS = params['CONG_TRINH_IDS'] if 'CONG_TRINH_IDS' in params.keys() else 'False'
        TAIKHOAN2_IDS = params['TAIKHOAN2_IDS'] if 'TAIKHOAN2_IDS' in params.keys() else 'False'
        CHIPHI2_IDS = params['CHIPHI2_IDS'] if 'CHIPHI2_IDS' in params.keys() else 'False'
        DONHANG2_IDS = params['DONHANG2_IDS'] if 'DONHANG2_IDS' in params.keys() else 'False'
        TAIKHOAN_IDS = params['TAIKHOAN_IDS'] if 'TAIKHOAN_IDS' in params.keys() else 'False'
        CHIPHI_IDS = params['CHIPHI_IDS'] if 'CHIPHI_IDS' in params.keys() else 'False'
        HOP_DONG_BAN_IDS = params['HOP_DONG_BAN_IDS'] if 'HOP_DONG_BAN_IDS' in params.keys() else 'False'

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU_F > DEN_F):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')
        elif THONG_KE_THEO =='DOI_TUONG_TAP_HOP_CHI_PHI':
            if TAIKHOAN4_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Tài khoản>. Xin vui lòng chọn lại.')
            elif DOITUONG_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Đối tượng tập hợp chi phí>. Xin vui lòng chọn lại.')
            elif CHIPHI4_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Khoản mục chi phí>. Xin vui lòng chọn lại.')
        elif THONG_KE_THEO =='CONG_TRINH':
            if TAIKHOAN3_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Tài khoản>. Xin vui lòng chọn lại.')
            elif CONG_TRINH_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')
            elif CHIPHI3_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Khoản mục chi phí>. Xin vui lòng chọn lại.')
        elif THONG_KE_THEO =='DON_HANG':
            if TAIKHOAN2_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Tài khoản>. Xin vui lòng chọn lại.')
            elif DONHANG2_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Đơn hàng>. Xin vui lòng chọn lại.')
            elif CHIPHI2_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Khoản mục chi phí>. Xin vui lòng chọn lại.')
        elif THONG_KE_THEO =='HOP_DONG':
            if TAIKHOAN_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Tài khoản>. Xin vui lòng chọn lại.')
            elif HOP_DONG_BAN_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Hợp đồng/dự án>. Xin vui lòng chọn lại.')
            elif CHIPHI_IDS =='False':
                raise ValidationError('Bạn chưa chọn <Khoản mục chi phí>. Xin vui lòng chọn lại.')
       

    def _action_view_report(self):
        self._validate()
        TU_F = self.get_vntime('TU')
        DEN_F = self.get_vntime('DEN')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param =''
        tai_khoan = ''
        if THONG_KE_THEO =='DOI_TUONG_TAP_HOP_CHI_PHI':
            tai_khoans = self._context.get('TAIKHOAN4_IDS')
            doi_tuong_thcps = self._context.get('DOITUONG_IDS')
            chi_phis = self._context.get('CHIPHI4_IDS')
            if len(tai_khoans)==1 and len(doi_tuong_thcps)==1 and len(chi_phis)==1   :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                doi_tuong_thcp = doi_tuong_thcps[0].get('MA_DOI_TUONG_THCP')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Tài khoản: %s; Đối tượng tập hợp chi phí: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,doi_tuong_thcp,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(doi_tuong_thcps)==1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                doi_tuong_thcp = doi_tuong_thcps[0].get('MA_DOI_TUONG_THCP')
                param = 'Tài khoản: %s; Đối tượng tập hợp chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,doi_tuong_thcp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(doi_tuong_thcps)!=1 and len(chi_phis)==1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')                
                param = 'Tài khoản: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(doi_tuong_thcps)!=1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                param = 'Tài khoản: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,TU_F, DEN_F)
            elif len(doi_tuong_thcps)==1 and len(tai_khoans)!=1 and len(chi_phis)!=1:
                doi_tuong_thcp = doi_tuong_thcps[0].get('MA_DOI_TUONG_THCP')
                param = 'Đối tượng tập hợp chi phí: %s;Từ ngày: %s đến ngày %s' % (doi_tuong_thcp,TU_F, DEN_F)
            elif len(doi_tuong_thcps)==1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                doi_tuong_thcp = doi_tuong_thcps[0].get('MA_DOI_TUONG_THCP')
                param = 'Đối tượng tập hợp chi phí: %s;Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (doi_tuong_thcp,khoan_muc_cp,TU_F, DEN_F)
            elif len(doi_tuong_thcps)!=1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (khoan_muc_cp,TU_F, DEN_F)
            else:
                param = 'Từ ngày: %s đến ngày %s' % (TU_F, DEN_F)
            action = self.env.ref('bao_cao.open_report__so_chi_tiet_tk_theo_doi_tuong_va_chi_phi_doi_tuong').read()[0]
        elif THONG_KE_THEO =='CONG_TRINH':
            tai_khoans = self._context.get('TAIKHOAN3_IDS')
            cong_trinhs = self._context.get('CONG_TRINH_IDS')
            chi_phis = self._context.get('CHIPHI3_IDS')
            if len(tai_khoans)==1 and len(cong_trinhs)==1 and len(chi_phis)==1   :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                cong_trinh = cong_trinhs[0].get('MA_CONG_TRINH')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Tài khoản: %s; Công trình: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,cong_trinh,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(cong_trinhs)==1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                cong_trinh = cong_trinhs[0].get('MA_CONG_TRINH')
                param = 'Tài khoản: %s; Công trình: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,cong_trinh,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(cong_trinhs)!=1 and len(chi_phis)==1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')                
                param = 'Tài khoản: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(cong_trinhs)!=1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                param = 'Tài khoản: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,TU_F, DEN_F)
            elif len(cong_trinhs)==1 and len(tai_khoans)!=1 and len(chi_phis)!=1:
                cong_trinh = cong_trinhs[0].get('MA_CONG_TRINH')
                param = 'Công trình: %s;Từ ngày: %s đến ngày %s' % (cong_trinh,TU_F, DEN_F)
            elif len(cong_trinhs)==1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                cong_trinh = cong_trinhs[0].get('MA_CONG_TRINH')
                param = 'Công trình: %s;Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (cong_trinh,khoan_muc_cp,TU_F, DEN_F)
            elif len(cong_trinhs)!=1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (khoan_muc_cp,TU_F, DEN_F)
            else:
                param = 'Từ ngày: %s đến ngày %s' % (TU_F, DEN_F)
            action = self.env.ref('bao_cao.open_report__so_chi_tiet_tk_theo_doi_tuong_va_chi_phi_cong_trinh').read()[0]
        elif THONG_KE_THEO =='DON_HANG':
            tai_khoans = self._context.get('TAIKHOAN2_IDS')
            don_hangs = self._context.get('DONHANG2_IDS')
            chi_phis = self._context.get('CHIPHI2_IDS')
            if len(tai_khoans)==1 and len(don_hangs)==1 and len(chi_phis)==1   :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                don_hang = don_hangs[0].get('SO_DON_HANG')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Tài khoản: %s; Đơn hàng: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,don_hang,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(don_hangs)==1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                don_hang = don_hangs[0].get('SO_DON_HANG')
                param = 'Tài khoản: %s; Đơn hàng: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,don_hang,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(don_hangs)!=1 and len(chi_phis)==1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')                
                param = 'Tài khoản: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(don_hangs)!=1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                param = 'Tài khoản: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,TU_F, DEN_F)
            elif len(don_hangs)==1 and len(tai_khoans)!=1 and len(chi_phis)!=1:
                don_hang = don_hangs[0].get('SO_DON_HANG')
                param = 'Đơn hàng: %s;Từ ngày: %s đến ngày %s' % (don_hang,TU_F, DEN_F)
            elif len(don_hangs)==1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                don_hang = don_hangs[0].get('SO_DON_HANG')
                param = 'Đơn hàng: %s;Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (don_hang,khoan_muc_cp,TU_F, DEN_F)
            elif len(don_hangs)!=1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (khoan_muc_cp,TU_F, DEN_F)
            else:
                param = 'Từ ngày: %s đến ngày %s' % (TU_F, DEN_F)
            action = self.env.ref('bao_cao.open_report__so_chi_tiet_tk_theo_doi_tuong_va_chi_phi_don_hang').read()[0]
        elif THONG_KE_THEO =='HOP_DONG':
            tai_khoans = self._context.get('TAIKHOAN_IDS')
            hop_dongs = self._context.get('HOP_DONG_BAN_IDS')
            chi_phis = self._context.get('CHIPHI_IDS')
            if len(tai_khoans)==1 and len(hop_dongs)==1 and len(chi_phis)==1   :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                hop_dong = hop_dongs[0].get('SO_HOP_DONG')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Tài khoản: %s; Hợp đồng/dự án: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,hop_dong,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(hop_dongs)==1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                hop_dong = hop_dongs[0].get('SO_HOP_DONG')
                param = 'Tài khoản: %s; Hợp đồng/dự án: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,hop_dong,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(hop_dongs)!=1 and len(chi_phis)==1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')                
                param = 'Tài khoản: %s; Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,khoan_muc_cp,TU_F, DEN_F)
            elif len(tai_khoans)==1 and len(hop_dongs)!=1 and len(chi_phis)!=1 :
                tai_khoan = tai_khoans[0].get('SO_TAI_KHOAN')
                param = 'Tài khoản: %s;Từ ngày: %s đến ngày %s' % (tai_khoan,TU_F, DEN_F)
            elif len(hop_dongs)==1 and len(tai_khoans)!=1 and len(chi_phis)!=1:
                hop_dong = hop_dongs[0].get('SO_HOP_DONG')
                param = 'Hợp đồng/dự án: %s;Từ ngày: %s đến ngày %s' % (hop_dong,TU_F, DEN_F)
            elif len(hop_dongs)==1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                hop_dong = hop_dongs[0].get('SO_HOP_DONG')
                param = 'Hợp đồng/dự án: %s;Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (hop_dong,khoan_muc_cp,TU_F, DEN_F)
            elif len(hop_dongs)!=1 and len(tai_khoans)!=1 and len(chi_phis)==1:
                khoan_muc_cp = chi_phis[0].get('MA_KHOAN_MUC_CP')
                param = 'Khoản mục chi phí: %s;Từ ngày: %s đến ngày %s' % (khoan_muc_cp,TU_F, DEN_F)
            else:
                param = 'Từ ngày: %s đến ngày %s' % (TU_F, DEN_F)
            action = self.env.ref('bao_cao.open_report__so_chi_tiet_tk_theo_doi_tuong_va_chi_phi_hop_dong').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action