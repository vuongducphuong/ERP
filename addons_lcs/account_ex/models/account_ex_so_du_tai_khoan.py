# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class ACCOUNT_EX_SO_DU_TAI_KHOAN(models.Model):
    _name = 'account.ex.so.du.tai.khoan'

    child_id = fields.Integer(string='id của TK')
    parent_id = fields.Integer(string='id của TK Tổng hợp')
    SO_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Số tài khoản', help='Số tài khoản')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
    TINH_CHAT_TAI_KHOAN = fields.Selection([
        ('0', 'Dư Nợ'), 
		('1', 'Dư Có'), 
		('2', 'Lưỡng tính'), 
		('3', 'Không có số dư'),
    ], related='SO_TAI_KHOAN_ID.TINH_CHAT')
    DU_NO = fields.Float(string='Dư Nợ', help='Dư Nợ',digits=decimal_precision.get_precision('Product Price'))
    DU_CO = fields.Float(string='Dư Có', help='Dư Có',digits=decimal_precision.get_precision('Product Price'))
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư ban đầu', help='Số dư ban đầu', ondelete='cascade')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS = fields.One2many('account.ex.so.du.tai.khoan.chi.tiet', 'SO_DU_TAI_KHOAN_ID', string='Nhập số dư tài khoản')
    CHI_TIET_THEO_DOI_TUONG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')
    CHI_TIET_THEO_TK_NGAN_HANG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')
    LOAI_DOI_TUONG = fields.Char(string='Loại đối tượng', help='Loại đối tượng')
    # SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    # NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán')
    # NGAY_CHUNG_TU = fields.Date(string='Ngày Chứng từ', default=fields.Datetime.now)
    CO_HACH_TOAN_NGOAI_TE = fields.Boolean(string='Có hạch toán ngoại tệ', help='Có hạch toán ngoại tệ')
    # KHAI_BAO_DAU_KY = fields.Boolean(string='Khai báo đầu kỳ', default=True)

    @api.onchange('currency_id')
    def _onchange_LOAI_TIEN_ID(self):
        if self.currency_id.MA_LOAI_TIEN == 'VND':
            self.CO_HACH_TOAN_NGOAI_TE = False
        else:
            self.CO_HACH_TOAN_NGOAI_TE = True

    def lay_loai_tien(self, args):
        return self.env['res.currency'].search([('MA_LOAI_TIEN', 'like', 'VND%')],limit=1).id
    
    @api.model
    def create(self, vals):
        ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
        if ngay_bat_dau_nam_tai_chinh:
            ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
            ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
            ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')

        if vals.get('CHI_TIET_THEO_DOI_TUONG') == 1:
            chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', vals.get('SO_TAI_KHOAN_ID')),('currency_id','=',vals.get('currency_id'))])
            for ct_theo_doi_tuong in chi_tiet_server:
                if ct_theo_doi_tuong.DU_NO_NGUYEN_TE > 0 or ct_theo_doi_tuong.DU_CO_NGUYEN_TE > 0:
                    ct_theo_doi_tuong.bo_ghi_so()
                chi_tiet_theo_doi_tuongs = self.env['account.ex.sdtkct.theo.doi.tuong'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', ct_theo_doi_tuong.id)])
                chi_tiet_theo_hoa_dons = self.env['account.ex.sdtkct.theo.hoa.don'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', ct_theo_doi_tuong.id)])
                ct_theo_doi_tuong.unlink()
                if chi_tiet_theo_hoa_dons:
                    for ct_theo_hoa_don in chi_tiet_theo_hoa_dons:
                        ct_theo_hoa_don.unlink()
                if chi_tiet_theo_doi_tuongs:
                    for chi_tiet_theo_doi_tuong in chi_tiet_theo_doi_tuongs:
                        chi_tiet_theo_doi_tuong.unlink()
                        
        elif vals.get('CHI_TIET_THEO_TK_NGAN_HANG') == 1:
            for ct_khong_chi_tiet in vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):
                chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('currency_id','=',vals.get('currency_id')),('TK_ID', '=', ct_khong_chi_tiet[2].get('TK_ID'))])
                for ct_theo_tknh in chi_tiet_server:
                    if ct_theo_tknh.DU_NO_NGUYEN_TE > 0 or ct_theo_tknh.DU_CO_NGUYEN_TE > 0:
                        ct_theo_tknh.bo_ghi_so()
                    chi_tiet_theo_doi_tuongs = self.env['account.ex.sdtkct.theo.doi.tuong'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', ct_theo_tknh.id)])
                    chi_tiet_theo_hoa_dons = self.env['account.ex.sdtkct.theo.hoa.don'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', ct_theo_tknh.id)])
                    ct_theo_tknh.unlink()
                    if chi_tiet_theo_hoa_dons:
                        for ct_theo_hoa_don in chi_tiet_theo_hoa_dons:
                            ct_theo_hoa_don.unlink()
                    if chi_tiet_theo_doi_tuongs:
                        for chi_tiet_theo_doi_tuong in chi_tiet_theo_doi_tuongs:
                            chi_tiet_theo_doi_tuong.unlink()
        else:
            if vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):
                for ct_khong_chi_tiet in vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):
                    chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', ct_khong_chi_tiet[2].get('TK_ID')),('currency_id','=',vals.get('currency_id'))])
                    for khong_theo_ct in chi_tiet_server:
                        if khong_theo_ct.DU_NO_NGUYEN_TE > 0 or khong_theo_ct.DU_CO_NGUYEN_TE > 0:
                            khong_theo_ct.bo_ghi_so()
                        chi_tiet_theo_doi_tuongs = self.env['account.ex.sdtkct.theo.doi.tuong'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', khong_theo_ct.id)])
                        chi_tiet_theo_hoa_dons = self.env['account.ex.sdtkct.theo.hoa.don'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', khong_theo_ct.id)])
                        khong_theo_ct.unlink()
                        if chi_tiet_theo_hoa_dons:
                            for ct_theo_hoa_don in chi_tiet_theo_hoa_dons:
                                ct_theo_hoa_don.unlink()
                        if chi_tiet_theo_doi_tuongs:
                            for chi_tiet_theo_doi_tuong in chi_tiet_theo_doi_tuongs:
                                chi_tiet_theo_doi_tuong.unlink()
        if vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):            
            for ct in vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):
                if vals.get('CHI_TIET_THEO_DOI_TUONG') == 1:
                    ct[2]['TK_ID'] = vals.get('SO_TAI_KHOAN_ID')
                    if vals.get('LOAI_DOI_TUONG') == '0':
                        ct[2]['LOAI_CHUNG_TU'] = '613'
                    elif vals.get('LOAI_DOI_TUONG') == '1':
                        ct[2]['LOAI_CHUNG_TU'] = '612'
                    elif vals.get('LOAI_DOI_TUONG') == '2':
                        ct[2]['LOAI_CHUNG_TU'] = '614'
                elif vals.get('CHI_TIET_THEO_TK_NGAN_HANG') == 1:
                    ct[2]['LOAI_CHUNG_TU'] = '620'
                else:
                    ct[2]['LOAI_CHUNG_TU'] = '610'
                ct[2]['currency_id'] = vals.get('currency_id')
        master = self.env['account.ex.so.du.tai.khoan'].search([])
        if master:
          for mt in master:
            mt.unlink()

		# Tạo bản ghi không qua hàm supper
        if vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):
            arr_so_du_tai_khoan_ct = []
            # dữ liệu test trường hợp bị lỗi
            # dict_tam = {
            #     'DOI_TUONG_ID' : 102,
            #     'TK_ID' : 1223,
            #     'currency_id' : 24,
            # }
            # arr_so_du_tai_khoan_ct.append(dict_tam)
            for line in vals.get('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'):
                dict_so_du_tk_ct = {
                    'currency_id' : line[2].get('currency_id'),
                    'TK_ID' : line[2].get('TK_ID'),
                    'DOI_TUONG_ID' : line[2].get('DOI_TUONG_ID'),
                    'TK_NGAN_HANG_ID' : line[2].get('TK_NGAN_HANG_ID'),
                }
                if dict_so_du_tk_ct not in arr_so_du_tai_khoan_ct:
                    arr_so_du_tai_khoan_ct.append(dict_so_du_tk_ct)
                else:
                    ten_doi_tuong = ''
                    so_tai_khoan = ''
                    ten_loai_tien = ''
                    ma_tai_khoan_ngan_hang = ''
                    doi_tuong = self.env['res.partner'].search([('id', '=', line[2].get('DOI_TUONG_ID'))])
                    tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', line[2].get('TK_ID'))])
                    loai_tien = self.env['res.currency'].search([('id', '=', line[2].get('currency_id'))])
                    tai_khoan_ngan_hang = self.env['danh.muc.tai.khoan.ngan.hang'].search([('id', '=', line[2].get('currency_id'))])
                    if doi_tuong:
                        ten_doi_tuong = doi_tuong.HO_VA_TEN
                    if tai_khoan:
                        so_tai_khoan = tai_khoan.SO_TAI_KHOAN
                    if loai_tien:
                        ten_loai_tien = loai_tien.MA_LOAI_TIEN
                    if tai_khoan_ngan_hang:
                        ma_tai_khoan_ngan_hang = tai_khoan_ngan_hang.SO_TAI_KHOAN
                    thong_bao_loi = 'bị x2 dòng số dư ban đầu với thông tin số tài khoản: ' + so_tai_khoan + ' ,đối tượng: ' + ten_doi_tuong + ' ,loại tiền: ' + ten_loai_tien + ' , tài khoản ngần hàng: ' +ma_tai_khoan_ngan_hang+ '. báo cho bên kỹ thuật để xử lý ngay'
                    raise ValidationError(thong_bao_loi)
                if line[2].get('DU_NO_NGUYEN_TE') > 0 or line[2].get('DU_CO_NGUYEN_TE') > 0:
                    line[2]['NGAY_HACH_TOAN'] = ngay_hach_toan_str
                    chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].create(line[2])
                    # đã tự động ghi sổ
                    if vals.get('CHI_TIET_THEO_DOI_TUONG') == 1:
                        chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', line[2].get('TK_ID')),('DOI_TUONG_ID','=',line[2].get('DOI_TUONG_ID')),('currency_id','=',vals.get('currency_id'))], limit=1)
                        chi_tiet_server.action_ghi_so()
                    elif vals.get('CHI_TIET_THEO_TK_NGAN_HANG') == 1:
                        chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', line[2].get('TK_ID')),('TK_NGAN_HANG_ID', '=',line[2].get('TK_NGAN_HANG_ID')),('currency_id','=',vals.get('currency_id'))], limit=1)
                        chi_tiet_server.action_ghi_so()
                    else:
                        chi_tiet_server = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', line[2].get('TK_ID')),('currency_id','=',vals.get('currency_id'))], limit=1)
                        chi_tiet_server.action_ghi_so()

        vals['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS'] = {}
        result = super(ACCOUNT_EX_SO_DU_TAI_KHOAN, self).create(vals)

        return result
    
    def lay_so_du_tai_khoan(self, args):
        new_line = [[5]]
        
        
        
        tai_khoan_dto =False
        tai_khoan = -1
        so_tai_khoan = ''
        if args.get('tai_khoan_id'):
            tai_khoan_dto = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', args.get('tai_khoan_id'))],limit=1)
        else : 
            if args.get('ct_theo_dt') == 1 and args.get('loai_doi_tuong') == '0':
                tai_khoan_dto = self.env['danh.muc.he.thong.tai.khoan'].search([('DOI_TUONG_SELECTION', '=', '0')],limit=1)
            elif args.get('ct_theo_dt') == 1 and args.get('loai_doi_tuong') == '1':
                tai_khoan_dto = self.env['danh.muc.he.thong.tai.khoan'].search([('DOI_TUONG_SELECTION', '=', '1')],limit=1)	
            elif args.get('ct_theo_dt') == 1 and args.get('loai_doi_tuong') == '2':
                tai_khoan_dto = self.env['danh.muc.he.thong.tai.khoan'].search([('DOI_TUONG_SELECTION', '=', '2')],limit=1)

        if tai_khoan_dto:
            tai_khoan = tai_khoan_dto.id
            so_tai_khoan = tai_khoan_dto.SO_TAI_KHOAN
        		
        # elif args.get('ct_theo_tk') == 1:
        #     tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('TAI_KHOAN_NGAN_HANG', '=', True)],limit=1).id
        #     so_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('TAI_KHOAN_NGAN_HANG', '=', True)],limit=1).SO_TAI_KHOAN
        # elif args.get('ct_theo_tk') == 0 and args.get('ct_theo_dt') == 0:
        #     tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('TAI_KHOAN_NGAN_HANG', '=', False),('DOI_TUONG','=','')],limit=1).id
        #     so_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('TAI_KHOAN_NGAN_HANG', '=', False),('DOI_TUONG','=','')],limit=1).SO_TAI_KHOAN
        ten_loai_tien = self.env['res.currency'].search([('id', '=', args.get('loai_tien_id'))],limit=1).MA_LOAI_TIEN
        if ten_loai_tien == 'VND':
            co_hach_toan_ngoai_te = False
        else :
            co_hach_toan_ngoai_te = True

        if args.get('ct_theo_dt') == 0 and args.get('ct_theo_tk') == 0:
            loai_tien_vnd = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')]).id
            loai_tien_id = False
            if args.get('loai_tien_id') == -1:
                loai_tien_id = loai_tien_vnd
            else:
                loai_tien_id = args.get('loai_tien_id')
            du_lieu_tk = self.lay_du_lieu_so_du_tk(loai_tien_id)
            if du_lieu_tk:
                for line in du_lieu_tk:
                    new_line_chi_tiet_theo_doi_tuong_sdtk = [[5]]
                    if line.get('ID_CHUNG_TU'):
                        chi_tiet_theo_doi_tuong_sdtks = self.env['account.ex.sdtkct.theo.doi.tuong'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', line.get('ID_CHUNG_TU'))])
                        if chi_tiet_theo_doi_tuong_sdtks:
                            for ct_theo_doi_tuong_sdtk in chi_tiet_theo_doi_tuong_sdtks:
                                new_line_chi_tiet_theo_doi_tuong_sdtk += [(0,0,{
                                    'NHAN_VIEN_ID' : [ct_theo_doi_tuong_sdtk.NHAN_VIEN_ID.id,ct_theo_doi_tuong_sdtk.NHAN_VIEN_ID.HO_VA_TEN],
                                    'DON_VI_ID' : [ct_theo_doi_tuong_sdtk.DON_VI_ID.id,ct_theo_doi_tuong_sdtk.DON_VI_ID.TEN_DON_VI],
                                    'CONG_TRINH_ID' : [ct_theo_doi_tuong_sdtk.CONG_TRINH_ID.id,ct_theo_doi_tuong_sdtk.CONG_TRINH_ID.TEN_CONG_TRINH],
                                    'DON_MUA_HANG_ID' : [ct_theo_doi_tuong_sdtk.DON_MUA_HANG_ID.id,ct_theo_doi_tuong_sdtk.DON_MUA_HANG_ID.SO_DON_HANG],
                                    'HOP_DONG_MUA_ID' : [ct_theo_doi_tuong_sdtk.HOP_DONG_MUA_ID.id,ct_theo_doi_tuong_sdtk.HOP_DONG_MUA_ID.SO_HOP_DONG],
                                    'KHOAN_MUC_CP_ID' : [ct_theo_doi_tuong_sdtk.KHOAN_MUC_CP_ID.id,ct_theo_doi_tuong_sdtk.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP],
                                    'DOI_TUONG_THCP_ID' : [ct_theo_doi_tuong_sdtk.DOI_TUONG_THCP_ID.id,ct_theo_doi_tuong_sdtk.DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
                                    'DON_DAT_HANG_ID' : [ct_theo_doi_tuong_sdtk.DON_DAT_HANG_ID.id,ct_theo_doi_tuong_sdtk.DON_DAT_HANG_ID.SO_DON_HANG],
                                    'MA_THONG_KE_ID' : [ct_theo_doi_tuong_sdtk.MA_THONG_KE_ID.id,ct_theo_doi_tuong_sdtk.MA_THONG_KE_ID.MA_THONG_KE],
                                    'HOP_DONG_BAN_ID' : [ct_theo_doi_tuong_sdtk.HOP_DONG_BAN_ID.id,ct_theo_doi_tuong_sdtk.HOP_DONG_BAN_ID.SO_HOP_DONG],
                                    'DU_NO_NGUYEN_TE' : ct_theo_doi_tuong_sdtk.DU_NO_NGUYEN_TE,
                                    'DU_NO' : ct_theo_doi_tuong_sdtk.DU_NO,
                                    'DU_CO_NGUYEN_TE' : ct_theo_doi_tuong_sdtk.DU_CO_NGUYEN_TE,
                                    'DU_CO' : ct_theo_doi_tuong_sdtk.DU_CO,
                                })]
                    new_line += [(0,0,{
						'TK_ID' : [line.get('TAI_KHOAN_ID'), line.get('MA_TAI_KHOAN')],
						'SO_TAI_KHOAN' : line.get('MA_TAI_KHOAN'),
						'TEN_TAI_KHOAN' : line.get('TEN_TAI_KHOAN'),
						'DU_NO' : line.get('DU_NO'),
						'DU_CO' : line.get('DU_CO'),
						'DU_NO_NGUYEN_TE' : line.get('DU_NO_NGUYEN_TE'),
						'DU_CO_NGUYEN_TE' : line.get('DU_CO_NGUYEN_TE'),
						'NHAP_SO_DU_CHI_TIET' : 'Nhập chi tiết số dư',
						'currency_id' : [args.get('loai_tien_id'),ten_loai_tien],
						'CO_HACH_TOAN_NGOAI_TE' : co_hach_toan_ngoai_te,
                        'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS' : new_line_chi_tiet_theo_doi_tuong_sdtk,
						'TINH_CHAT_TAI_KHOAN': line.get('TINH_CHAT'),
					})]
        elif args.get('ct_theo_tk') == 1:
            du_lieu_tk_ngan_hang = self.lay_du_lieu_tk_ngan_hang(args.get('loai_tien_id'))
            
            tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG', '=', True),('CO_HACH_TOAN_NGOAI_TE', '=', False),('LA_TK_TONG_HOP', '=', False)],limit=1)
            tai_khoan_ngoai_te = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG', '=', True),('CO_HACH_TOAN_NGOAI_TE', '=', True),('LA_TK_TONG_HOP', '=', False)],limit=1)
            tien_viet = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1).id


            for tk_nh in du_lieu_tk_ngan_hang:
                if not tk_nh.get('TAI_KHOAN_ID'):
                    if args.get('loai_tien_id') == tien_viet:
                        tai_khoan_id = tai_khoan.id
                        ma_tai_khoan = tai_khoan.SO_TAI_KHOAN
                    else:
                        tai_khoan_id = tai_khoan_ngoai_te.id
                        ma_tai_khoan = tai_khoan_ngoai_te.SO_TAI_KHOAN
                else:
                    tai_khoan_id = tk_nh.get('TAI_KHOAN_ID')
                    ma_tai_khoan = tk_nh.get('MA_TAI_KHOAN')
                new_line += [(0,0,{
					'TK_NGAN_HANG_ID' : [tk_nh.get('TK_NGAN_HANG'),tk_nh.get('SO_TK_NGAN_HANG')],
					'TEN_TAI_KHOAN' : tk_nh.get('TEN_TK_NGAN_HANG'),
					'TK_ID' : [tai_khoan_id,ma_tai_khoan],
					'SO_TAI_KHOAN' : ma_tai_khoan,
					'DU_NO' : tk_nh.get('DU_NO'),
					'DU_CO' : tk_nh.get('DU_CO'),
					'DU_NO_NGUYEN_TE' : tk_nh.get('DU_NO_NGUYEN_TE'),
					'DU_CO_NGUYEN_TE' : tk_nh.get('DU_CO_NGUYEN_TE'),
					'currency_id' : [args.get('loai_tien_id'),ten_loai_tien],
					'CO_HACH_TOAN_NGOAI_TE' : co_hach_toan_ngoai_te,
					# 'TINH_CHAT_TAI_KHOAN': '',
					})]
        elif args.get('ct_theo_dt') == 1:
            du_lieu_doi_tuong = self.lay_du_lieu_doi_tuong(args.get('loai_tien_id'),args.get('loai_doi_tuong'),tai_khoan)
            if du_lieu_doi_tuong:
                for dt in du_lieu_doi_tuong:
                    new_line_chi_tiet_theo_hoa_don = [[5]]
                    new_line_chi_tiet_theo_doi_tuong = [[5]]
                    if dt.get('ID_CHUNG_TU'):
                        chi_tiet_theo_hoa_dons = self.env['account.ex.sdtkct.theo.hoa.don'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', dt.get('ID_CHUNG_TU'))])
                        if chi_tiet_theo_hoa_dons:
                            for ct_theo_hoa_don in chi_tiet_theo_hoa_dons:
                                new_line_chi_tiet_theo_hoa_don += [(0,0,{
                                    'NGAY_HOA_DON' : ct_theo_hoa_don.NGAY_HOA_DON,
                                    'SO_HOA_DON' : ct_theo_hoa_don.SO_HOA_DON,
                                    'HAN_THANH_TOAN' : ct_theo_hoa_don.HAN_THANH_TOAN,
                                    'GIA_TRI_HOA_DON_NGUYEN_TE' : ct_theo_hoa_don.GIA_TRI_HOA_DON_NGUYEN_TE,
                                    'GIA_TRI_HOA_DON' : ct_theo_hoa_don.GIA_TRI_HOA_DON,
                                    'SO_CON_PHAI_THU_NGUYEN_TE' : ct_theo_hoa_don.SO_CON_PHAI_THU_NGUYEN_TE,
                                    'SO_CON_PHAI_THU' : ct_theo_hoa_don.SO_CON_PHAI_THU,
                                    'SO_THU_TRUOC_NGUYEN_TE' : ct_theo_hoa_don.SO_THU_TRUOC_NGUYEN_TE,
                                    'SO_THU_TRUOC' : ct_theo_hoa_don.SO_THU_TRUOC,
                                    'GIA_TRI_HOA_DON' : ct_theo_hoa_don.GIA_TRI_HOA_DON,
                                    'SO_CON_PHAI_THU' : ct_theo_hoa_don.SO_CON_PHAI_THU,
                                    'SO_THU_TRUOC' : ct_theo_hoa_don.SO_THU_TRUOC,
                                    'NHAN_VIEN_ID' : [ct_theo_hoa_don.NHAN_VIEN_ID.id,ct_theo_hoa_don.NHAN_VIEN_ID.HO_VA_TEN],
                                })]
                    if dt.get('ID_CHUNG_TU'):
                        chi_tiet_theo_doi_tuongs = self.env['account.ex.sdtkct.theo.doi.tuong'].search([('SO_DU_TAI_KHOAN_CHI_TIET_ID', '=', dt.get('ID_CHUNG_TU'))])
                        if chi_tiet_theo_doi_tuongs:
                            for ct_theo_doi_tuong in chi_tiet_theo_doi_tuongs:
                                new_line_chi_tiet_theo_doi_tuong += [(0,0,{
                                    'NHAN_VIEN_ID' : [ct_theo_doi_tuong.NHAN_VIEN_ID.id,ct_theo_doi_tuong.NHAN_VIEN_ID.HO_VA_TEN],
                                    'DON_VI_ID' : [ct_theo_doi_tuong.DON_VI_ID.id,ct_theo_doi_tuong.DON_VI_ID.TEN_DON_VI],
                                    'CONG_TRINH_ID' : [ct_theo_doi_tuong.CONG_TRINH_ID.id,ct_theo_doi_tuong.CONG_TRINH_ID.TEN_CONG_TRINH],
                                    'DON_MUA_HANG_ID' : [ct_theo_doi_tuong.DON_MUA_HANG_ID.id,ct_theo_doi_tuong.DON_MUA_HANG_ID.SO_DON_HANG],
                                    'HOP_DONG_BAN_ID' : [ct_theo_doi_tuong.HOP_DONG_BAN_ID.id,ct_theo_doi_tuong.HOP_DONG_BAN_ID.SO_HOP_DONG],
                                    'HOP_DONG_MUA_ID' : [ct_theo_doi_tuong.HOP_DONG_MUA_ID.id,ct_theo_doi_tuong.HOP_DONG_MUA_ID.SO_HOP_DONG],
                                    'DON_DAT_HANG_ID' : [ct_theo_doi_tuong.DON_DAT_HANG_ID.id,ct_theo_doi_tuong.DON_DAT_HANG_ID.SO_DON_HANG],
                                    'DU_NO_NGUYEN_TE' : ct_theo_doi_tuong.DU_NO_NGUYEN_TE,
                                    'DU_NO' : ct_theo_doi_tuong.DU_NO,
                                    'DU_CO_NGUYEN_TE' : ct_theo_doi_tuong.DU_CO_NGUYEN_TE,
                                    'DU_CO' : ct_theo_doi_tuong.DU_CO,
                                })]
                    
                    new_line += [(0,0,{
						'DOI_TUONG_ID' : [dt.get('DOI_TUONG_ID'),dt.get('MA')],
						'TEN_DOI_TUONG' : dt.get('TEN_DOI_TUONG'),
						'DU_NO' : dt.get('DU_NO'),
						'DU_CO' : dt.get('DU_CO'),
						'DU_NO_NGUYEN_TE' : dt.get('DU_NO_NGUYEN_TE',0),
						'DU_CO_NGUYEN_TE' : dt.get('DU_CO_NGUYEN_TE',0),
						'NHAP_SO_DU_CHI_TIET' : 'Nhập chi tiết công nợ',
						'currency_id' : [args.get('loai_tien_id'),ten_loai_tien],
						'TK_ID' : [tai_khoan,so_tai_khoan],
						'SO_TAI_KHOAN' : so_tai_khoan,
						'CO_HACH_TOAN_NGOAI_TE' : co_hach_toan_ngoai_te,
                        'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS' : new_line_chi_tiet_theo_hoa_don,
                        'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS' : new_line_chi_tiet_theo_doi_tuong,
						# 'TINH_CHAT_TAI_KHOAN': '',
						})]
                    

        if args.get('ct_theo_dt') == 1:
            if args.get('tai_khoan_id'):
                dic_ket_qua = {'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': new_line}
            else:
                dic_ket_qua = {'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': new_line,'SO_TAI_KHOAN_ID' : [tai_khoan,so_tai_khoan]}
        else:
            dic_ket_qua = {'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': new_line}
            
        return dic_ket_qua



    def lay_du_lieu_so_du_tk(self,loai_tien):
        if self.env['res.currency'].search([('id', '=', loai_tien)], limit=1).MA_LOAI_TIEN == 'VND':
          co_hach_toan_ngoai_te = False
        else:
          co_hach_toan_ngoai_te = True

        chi_nhanh_id = self.get_chi_nhanh()
        ngay_bat_dau = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
        if ngay_bat_dau:
            ngay_bat_dau_nam_tai_chinh = ngay_bat_dau
        else:
            # ngay_bat_dau_nam_tai_chinh = '2018-01-01'
            raise ValidationError('Bạn chưa nhập năm tài tính vui lòng vào phần hệ thống, tùy chọn thiết lập năm tài chính')
        params = {
          'currency_id': loai_tien,
          'CO_HACH_TOAN_NGOAI_TE' : co_hach_toan_ngoai_te,
		  'CHI_NHANH_ID' : chi_nhanh_id,
		  'NGAY_BAT_DAU' : ngay_bat_dau_nam_tai_chinh,
          }

        query = """   

        DO LANGUAGE plpgsql $$ DECLARE
        tham_so_loai_tien_id          INTEGER := %(currency_id)s;
        tham_so_co_hach_toan_ngoai_te BOOLEAN := %(CO_HACH_TOAN_NGOAI_TE)s ;
        tham_so_hien_thi_tren_so      INTEGER :=0;
        tham_so_chi_nhanh_id          INTEGER := %(CHI_NHANH_ID)s;
        tham_so_ngay_bat_dau          DATE := %(NGAY_BAT_DAU)s;
        tham_so_goi_form_chi_tiet     INTEGER :=0;

        msc_loai_tai_khoan            VARCHAR(50) :='3';
        msc_tong_hop_loai_tien        INTEGER :=-1;
        int_grade                     INTEGER :=0;

        BEGIN

        IF tham_so_loai_tien_id = msc_tong_hop_loai_tien
        THEN
            DROP TABLE IF EXISTS TMP_OPN_DATA_2;
            CREATE TEMP TABLE TMP_OPN_DATA_2
            AS
                SELECT
                    "TK_ID"            AS "TAI_KHOAN_ID"
                , OPN.id               AS "ID_CHUNG_TU"
                , "DOI_TUONG_ID"
                , OPN."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                , "TINH_CHAT"
                , "currency_id"
                , SUM(CASE WHEN "TINH_CHAT" = '2'
                                AND ("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") > 0
                THEN ("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE")
                        WHEN "TINH_CHAT" = '2'
                            AND ("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <= 0
                        THEN 0
                        ELSE "DU_NO_NGUYEN_TE"
                        END)              "DU_NO_NGUYEN_TE"
                , SUM(CASE WHEN "TINH_CHAT" = '2'
                                AND ("DU_NO" - "DU_CO") > 0
                THEN ("DU_NO" - "DU_CO")
                        WHEN "TINH_CHAT" = '2'
                            AND ("DU_NO" - "DU_CO") <= 0
                        THEN 0
                        ELSE "DU_NO"
                        END)              "DU_NO"
                , SUM(CASE WHEN "TINH_CHAT" = '2'
                                AND ("DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE") > 0
                THEN ("DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE")
                        WHEN "TINH_CHAT" = '2'
                            AND ("DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE") <= 0
                        THEN 0
                        ELSE "DU_CO_NGUYEN_TE"
                        END)              "DU_CO_NGUYEN_TE"
                , SUM(CASE WHEN "TINH_CHAT" = '2'
                                AND ("DU_CO" - "DU_NO") > 0
                THEN ("DU_CO" - "DU_NO")
                        WHEN "TINH_CHAT" = '2'
                            AND ("DU_CO" - "DU_NO") <= 0
                        THEN 0
                        ELSE "DU_CO"
                        END)              "DU_CO"
                , "CHI_NHANH_ID"
                FROM danh_muc_he_thong_tai_khoan A
                INNER JOIN account_ex_so_du_tai_khoan_chi_tiet OPN ON OPN."TK_ID" = A.id
                WHERE (tham_so_goi_form_chi_tiet = 0
                    OR (OPN."LOAI_CHUNG_TU" = '610'
                        AND tham_so_goi_form_chi_tiet = 1
                    )
                    ) -- Số dư tài khoản
                    AND A."TINH_CHAT" <> msc_loai_tai_khoan
                    AND (OPN."currency_id" = tham_so_loai_tien_id
                        OR tham_so_loai_tien_id = msc_tong_hop_loai_tien
                    )
                    AND A."LA_TK_TONG_HOP" = FALSE
                    AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                GROUP BY "TK_ID",
                OPN.id,
                OPN."DOI_TUONG_ID",
                "currency_id",
                OPN."SO_TAI_KHOAN",
                "TINH_CHAT",
                "CHI_NHANH_ID"
                ORDER BY OPN."SO_TAI_KHOAN";


            DROP TABLE IF EXISTS TMP_OPN_DATA;
            CREATE TEMP TABLE TMP_OPN_DATA
            AS
                SELECT
                "TAI_KHOAN_ID"
                , A."ID_CHUNG_TU"                 AS "ID_CHUNG_TU"
                , "MA_TAI_KHOAN"
                , "TINH_CHAT"
                , tham_so_loai_tien_id AS "currency_id"
                , SUM("DU_NO_NGUYEN_TE")  "DU_NO_NGUYEN_TE"
                , SUM("DU_NO")            "DU_NO"
                , SUM("DU_CO_NGUYEN_TE")  "DU_CO_NGUYEN_TE"
                , SUM("DU_CO")            "DU_CO"
                , "CHI_NHANH_ID"
                FROM TMP_OPN_DATA_2 A
                GROUP BY "TAI_KHOAN_ID",
                "TINH_CHAT",
                "MA_TAI_KHOAN",
                "CHI_NHANH_ID",
                "ID_CHUNG_TU"
                ORDER BY "MA_TAI_KHOAN";

            DROP TABLE IF EXISTS TMP_TAI_KHOAN;
            CREATE TEMP TABLE TMP_TAI_KHOAN
            (
            "TAI_KHOAN_ID" INTEGER
            );
        END IF;

        IF tham_so_loai_tien_id <> msc_tong_hop_loai_tien
        THEN
            DROP TABLE IF EXISTS TMP_OPN_DATA;
            CREATE TEMP TABLE TMP_OPN_DATA
            AS
                SELECT
                    A.id                 AS    "TAI_KHOAN_ID"
                , OPN.id                 AS    "ID_CHUNG_TU"
                , OPN."SO_TAI_KHOAN"   AS    "MA_TAI_KHOAN"
                , A."TINH_CHAT"
                , tham_so_loai_tien_id AS    "currency_id"
                , SUM(OPN."DU_NO_NGUYEN_TE") "DU_NO_NGUYEN_TE"
                , SUM(OPN."DU_NO")           "DU_NO"
                , SUM(OPN."DU_CO_NGUYEN_TE") "DU_CO_NGUYEN_TE"
                , SUM(OPN."DU_CO")           "DU_CO"
                , OPN."CHI_NHANH_ID"
                FROM danh_muc_he_thong_tai_khoan A
                INNER JOIN account_ex_so_du_tai_khoan_chi_tiet OPN ON OPN."TK_ID" = A.id
                WHERE (tham_so_goi_form_chi_tiet = 0
                    OR (OPN."LOAI_CHUNG_TU" = '610'
                        AND tham_so_goi_form_chi_tiet = 1
                    )
                    )
                    AND A."TINH_CHAT" <> msc_loai_tai_khoan
                    AND (OPN."currency_id" = tham_so_loai_tien_id
                        OR tham_so_loai_tien_id = msc_tong_hop_loai_tien
                    )
                    AND A."LA_TK_TONG_HOP" = '0'    --
                    --             AND OPN.DisplayOnBook = @DisplayOnBook -- Biến truyên vào khi validate
                    AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                GROUP BY A.id,
                OPN.id,
                A."TINH_CHAT",
                OPN."SO_TAI_KHOAN",
                OPN."CHI_NHANH_ID"
                ORDER BY A."SO_TAI_KHOAN";
        END IF;

        DROP TABLE IF EXISTS TMP_TAI_KHOAN;
        CREATE TEMP TABLE TMP_TAI_KHOAN
        (
            "TAI_KHOAN_ID" INTEGER
        );

        IF tham_so_co_hach_toan_ngoai_te = TRUE
        THEN
            INSERT INTO TMP_TAI_KHOAN (
            SELECT A.id AS "TAI_KHOAN_ID"
            FROM danh_muc_he_thong_tai_khoan A
                LEFT JOIN (SELECT "SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan
                        WHERE "LA_TK_TONG_HOP" = '0'
                                AND "CO_HACH_TOAN_NGOAI_TE" = TRUE
                        ) OPN1 ON OPN1."MA_TAI_KHOAN" LIKE concat(A."SO_TAI_KHOAN", '%%')
            WHERE A."TINH_CHAT" <> msc_loai_tai_khoan
                    AND ((a."CO_HACH_TOAN_NGOAI_TE" = FALSE
            ))
                    AND A."LA_TK_TONG_HOP" = '1'
                    AND (CASE WHEN OPN1."MA_TAI_KHOAN" IS NULL
                                AND A."LA_TK_TONG_HOP" = '1'
                THEN 1
                        ELSE 0
                        END) = 0
            GROUP BY A."SO_TAI_KHOAN", A.id);
        END IF;

        DROP TABLE IF EXISTS TMP_OPN_TAI_KHOAN;
        CREATE TEMP TABLE TMP_OPN_TAI_KHOAN
            AS
            SELECT
                coalesce(OPN."ID_CHUNG_TU", 0)                    AS "ID_CHUNG_TU"
                , CASE WHEN OPN."CHI_NHANH_ID" IS NULL
                THEN 1
                ELSE 0
                END                                                   IsAddedNew
                , A.id                                               AS "TAI_KHOAN_ID"
                , A."SO_TAI_KHOAN"                                   AS "MA_TAI_KHOAN"
                , A."TEN_TAI_KHOAN"                                  AS "TEN_TAI_KHOAN"
                , A."TEN_TIENG_ANH"
                , A.parent_id                                        AS "TK_TONG_HOP"
                , A."MA_PHAN_CAP"
                , A."BAC"
                , A."LA_TK_TONG_HOP"
                , A."TINH_CHAT"
                , CASE WHEN A."CHI_TIET_THEO_DOI_TUONG" = TRUE
                THEN 1
                ELSE 0 END                                         AS "CHI_TIET_THEO_DOI_TUONG"
                , A."DOI_TUONG_SELECTION"                            AS "LOAI_DOI_TUONG"
                , CASE WHEN A."TAI_KHOAN_NGAN_HANG" = TRUE
                THEN 1
                ELSE 0 END                                         AS "CHI_TIET_THEO_TK_NGAN_HANG"
                , A."CO_HACH_TOAN_NGOAI_TE"
                , coalesce(OPN."currency_id", tham_so_loai_tien_id) AS "LOAI_TIEN"
                , coalesce(OPN."DU_NO_NGUYEN_TE", 0)                 AS "DU_NO_NGUYEN_TE"
                , coalesce(OPN."DU_NO", 0)                           AS "DU_NO"
                , coalesce(OPN."DU_CO_NGUYEN_TE", 0)                 AS "DU_CO_NGUYEN_TE"
                , coalesce(OPN."DU_CO", 0)                           AS "DU_CO"
                , tham_so_chi_nhanh_id                               AS "CHI_NHANH_ID"
                , --           coalesce(OPN.DisplayOnBook, @DisplayOnBook) AS DisplayOnBook ,
                --           coalesce(OPN.IsPostedCashBook, 0) AS IsPostedCashBook ,
                A."LA_TK_TONG_HOP"                                 AS "LA_TONG_HOP"
            FROM danh_muc_he_thong_tai_khoan A
                LEFT JOIN TMP_OPN_DATA OPN ON OPN."TAI_KHOAN_ID" = A.id
                LEFT JOIN TMP_TAI_KHOAN T ON T."TAI_KHOAN_ID" = A.id
            WHERE A."TINH_CHAT" <> msc_loai_tai_khoan
                    AND ((a."CO_HACH_TOAN_NGOAI_TE" = tham_so_co_hach_toan_ngoai_te
                        AND tham_so_co_hach_toan_ngoai_te = TRUE
                        )
                        OR (tham_so_co_hach_toan_ngoai_te = FALSE)
                        OR (A."LA_TK_TONG_HOP" = TRUE
                            AND tham_so_co_hach_toan_ngoai_te = TRUE
                            /*hoant 20.06.2018 sửa lỗi 234151*/
                            AND T."TAI_KHOAN_ID" IS NOT NULL
                        )
                    );


        SELECT MAX("BAC")
        INTO int_grade
        FROM TMP_OPN_TAI_KHOAN;

        IF tham_so_loai_tien_id = msc_tong_hop_loai_tien
        THEN

            WHILE (int_grade > 0)
            LOOP

            UPDATE TMP_OPN_TAI_KHOAN B
            SET "DU_NO"         = G."DU_NO_1",
                "DU_NO_NGUYEN_TE" = G."DU_NO_NGUYEN_TE_1",
                "DU_CO"           = G."DU_CO_1",
                "DU_CO_NGUYEN_TE" = G."DU_CO_NGUYEN_TE_1",
                "LA_TONG_HOP"     = CASE WHEN G."TK_TONG_HOP" ISNULL
                THEN FALSE
                                    ELSE TRUE END
            FROM (
                    SELECT
                    "TK_TONG_HOP"
                    , SUM("DU_NO")           AS "DU_NO_1"
                    , SUM("DU_NO_NGUYEN_TE") AS "DU_NO_NGUYEN_TE_1"
                    , SUM("DU_CO")           AS "DU_CO_1"
                    , SUM("DU_CO_NGUYEN_TE") AS "DU_CO_NGUYEN_TE_1"
                    FROM TMP_OPN_TAI_KHOAN
                    WHERE "BAC" = int_grade
                    GROUP BY "TK_TONG_HOP"

                ) G
            WHERE B."TAI_KHOAN_ID" = G."TK_TONG_HOP";
            int_grade := int_grade - 1;

            END LOOP;

        ELSE

            WHILE (int_grade > 0)
            LOOP

            UPDATE TMP_OPN_TAI_KHOAN B
            SET "DU_NO"         = G."DU_NO_1",
                "DU_NO_NGUYEN_TE" = G."DU_NO_NGUYEN_TE_1",
                "DU_CO"           = G."DU_CO_1",
                "DU_CO_NGUYEN_TE" = G."DU_CO_NGUYEN_TE_1",
                "LA_TONG_HOP"     = FALSE
            FROM (
                    SELECT
                    "TK_TONG_HOP"
                    , SUM("DU_NO")           AS "DU_NO_1"
                    , SUM("DU_NO_NGUYEN_TE") AS "DU_NO_NGUYEN_TE_1"
                    , SUM("DU_CO")           AS "DU_CO_1"
                    , SUM("DU_CO_NGUYEN_TE") AS "DU_CO_NGUYEN_TE_1"
                    FROM TMP_OPN_TAI_KHOAN
                    WHERE "BAC" = int_grade
                    GROUP BY "TK_TONG_HOP"

                ) G
            WHERE B."TAI_KHOAN_ID" = G."TK_TONG_HOP";
            int_grade := int_grade - 1;

            END LOOP;

        END IF;


        END $$;

        SELECT *
        FROM TMP_OPN_TAI_KHOAN
        WHERE "CHI_TIET_THEO_DOI_TUONG" = 0
            AND "CHI_TIET_THEO_TK_NGAN_HANG" = 0
            AND "LA_TK_TONG_HOP" = FALSE
        ORDER BY "MA_TAI_KHOAN"


        """  
        
        return self.execute(query, params)


    
    def lay_du_lieu_tk_ngan_hang(self,loai_tien):
        chi_nhanh_id = self.get_chi_nhanh()
        params = {
            'currency_id': loai_tien,
			'CHI_NHANH_ID' : chi_nhanh_id,
            }

        query = """   

        DO LANGUAGE plpgsql $$ DECLARE

        tham_so_loai_tien_id  INTEGER := %(currency_id)s;
        tham_so_chi_nhanh INTEGER := %(CHI_NHANH_ID)s ;
        tham_so_chi_tiet_theo_tk_ngan_hang INTEGER := 0 ;


        BEGIN

        DROP TABLE IF EXISTS TMP_KET_QUA;
        CREATE TEMP TABLE TMP_KET_QUA
        AS

        SELECT
                coalesce(OPN.id,row_number() OVER (PARTITION BY true::boolean)) AS "ID_CHUNG_TU" ,
                BA.id AS "TK_NGAN_HANG" ,
                BA."SO_TAI_KHOAN" AS "SO_TK_NGAN_HANG" ,
                CASE WHEN BA.name IS NULL THEN BAK."TEN_DAY_DU"
                    ELSE ( SUBSTRING(concat(BAK."TEN_DAY_DU",' - ',coalesce(BA.name,'')), 1, 128) )
                END AS "TEN_TK_NGAN_HANG" ,
                OPN."LOAI_CHUNG_TU" ,
                OPN."NGAY_HACH_TOAN" ,
                A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN",
                OPN."TK_ID" AS "TAI_KHOAN_ID",
                OPN."currency_id" ,
                coalesce(OPN."TY_GIA", 0.0) AS "TY_GIA" ,
                coalesce(OPN."DU_NO_NGUYEN_TE", 0.0) AS "DU_NO_NGUYEN_TE" ,
                coalesce(OPN."DU_NO", 0.0) AS "DU_NO" ,
                coalesce(OPN."DU_CO_NGUYEN_TE", 0.0) AS "DU_CO_NGUYEN_TE" ,
                coalesce(OPN."DU_CO", 0.0) AS "DU_CO" ,
                OPN."CHI_NHANH_ID" ,
        --         OPN.CashBook"NGAY_HACH_TOAN" ,
                OPN.state AS "TRANG_THAI_GHI_SO" ,
                OPN.id AS "ID_CHUNG_TU_DAU_KY" ,
                A."TINH_CHAT"
        FROM    danh_muc_tai_khoan_ngan_hang BA
                INNER JOIN danh_muc_ngan_hang AS BAK ON BA."NGAN_HANG_ID" = BAK.id
                LEFT JOIN account_ex_so_du_tai_khoan_chi_tiet OPN ON OPN."TK_NGAN_HANG_ID" = BA.id
                                                        AND OPN."LOAI_CHUNG_TU" = '620'
                                                        AND opn."CHI_NHANH_ID" = tham_so_chi_nhanh
--                                                         AND OPN."currency_id" = tham_so_loai_tien_id
                                                        --BTAnh25/03/2015: Thêm điều kiện này để khi lập ở sổ này rồi, sang sổ kia vẫn lập được nữa
                LEFT JOIN danh_muc_he_thong_tai_khoan A ON A.id = OPN."TK_ID"
         WHERE   ( OPN.currency_id IS NULL
              OR OPN.currency_id = tham_so_loai_tien_id
            )
            AND ( ( tham_so_chi_tiet_theo_tk_ngan_hang = 1
                    AND ( BA."CHI_NHANH_2" = tham_so_chi_nhanh
                          OR ( OPN."DU_NO_NGUYEN_TE" > 0
                               OR OPN."DU_CO_NGUYEN_TE" > 0
                             )
                        )
                  )
                  OR tham_so_chi_tiet_theo_tk_ngan_hang = 0
                )
        ORDER BY BA."SO_TAI_KHOAN" ,
                BA.name;

        END $$;

        SELECT *FROM TMP_KET_QUA


        """  
        
        return self.execute(query, params)


    def lay_du_lieu_doi_tuong(self,loai_tien,loai_doi_tuong,tai_khoan_id):
        chi_nhanh_id = self.get_chi_nhanh()
        params = {
            'currency_id': loai_tien,
			'TAI_KHOAN_ID' : tai_khoan_id,
			'CHI_NHANH_ID' : chi_nhanh_id,
            }
        
        dieu_kien = ''
        if loai_doi_tuong == '0':
            dieu_kien = """WHERE AO."LA_NHA_CUNG_CAP" = TRUE AND (OPN."CHI_NHANH_ID" = tham_so_chi_nhanh OR OPN."CHI_NHANH_ID" IS NULL)"""
        elif loai_doi_tuong == '1':
            dieu_kien = """WHERE AO."LA_KHACH_HANG" = TRUE AND (OPN."CHI_NHANH_ID" = tham_so_chi_nhanh OR OPN."CHI_NHANH_ID" IS NULL)"""
        elif loai_doi_tuong == '2':
            dieu_kien = """WHERE AO."LA_NHAN_VIEN" = TRUE AND (OPN."CHI_NHANH_ID" = tham_so_chi_nhanh OR OPN."CHI_NHANH_ID" IS NULL)"""

        query = """   

        DO LANGUAGE plpgsql $$ DECLARE

        tham_so_tai_khoan_id  INTEGER := %(TAI_KHOAN_ID)s;
        tham_so_loai_tien INTEGER := %(currency_id)s ;
        tham_so_chi_nhanh INTEGER := %(CHI_NHANH_ID)s ;


        BEGIN

        DROP TABLE IF EXISTS TMP_KET_QUA;
        CREATE TEMP TABLE TMP_KET_QUA
        AS
        SELECT
            coalesce(OPN.id, row_number() OVER (PARTITION BY true::boolean)) AS "ID_CHUNG_TU" ,
            AO.id AS "DOI_TUONG_ID" ,
            AO."MA" ,
            AO."HO_VA_TEN" AS "TEN_DOI_TUONG" ,
            AO."LA_NHA_CUNG_CAP" AS "LA_NHA_CUNG_CAP" ,
            AO."LA_KHACH_HANG" AS "LA_KHACH_HANG" ,
            AO."LA_NHAN_VIEN" AS "LA_NHAN_VIEN" ,
        --     AO."CHI_NHANH_ID" AS "CHI_NHANH_ID" ,
            OPN."LOAI_CHUNG_TU" ,
            OPN."NGAY_HACH_TOAN" ,
            OPN.state AS "TRANG_THAI_GHI_SO" ,
            OPN."SO_TAI_KHOAN" AS "MA_TAI_KHOAN" ,
            tham_so_tai_khoan_id AS "TAI_KHOAN_ID" ,
            OPN."currency_id" ,
            OPN."TY_GIA" ,
            coalesce(OPN."DU_NO_NGUYEN_TE", 0) AS "DU_NO_NGUYEN_TE" ,
            coalesce(OPN."DU_NO", 0) AS "DU_NO" ,
            coalesce(OPN."DU_CO_NGUYEN_TE", 0) AS "DU_CO_NGUYEN_TE" ,
            coalesce(OPN."DU_CO", 0) AS "DU_CO" ,
            OPN."CHI_NHANH_ID" ,
        --     (CASE WHEN OPN.id IS NULL THEN 1 ELSE OPN.[IsAutoGenerate] END) AS IsAutoGenerate ,
            N'Nhập chi tiết công nợ' AS "HIEN_THI_GHI_NO_CHI_TIET" ,
            OPN.id AS "ID_CHUNG_TU_DAU_KY"
        FROM    res_partner AO
            LEFT JOIN account_ex_so_du_tai_khoan_chi_tiet OPN ON (AO.id = OPN."DOI_TUONG_ID" 
			AND OPN."TK_ID" = tham_so_tai_khoan_id 
			AND OPN."currency_id" = tham_so_loai_tien 
			AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh)
        """+dieu_kien+"""
        ORDER BY "MA";

        END $$;

        SELECT *FROM TMP_KET_QUA;

        """  
        
        
        return self.execute(query, params)
