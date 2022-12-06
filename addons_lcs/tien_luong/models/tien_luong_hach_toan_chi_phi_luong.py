# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision



class TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG(models.Model):
    _name = 'tien.luong.hach.toan.chi.phi.luong'
    _description = ''
    _inherit = ['mail.thread']
    BANG_LUONG = fields.Char(string='Bảng lương', help='Bảng lương')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'),compute='_tong_so_tien',store=True)
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='tien_luong_hach_toan_chi_phi_luong_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU', oldname='NAME')

    BANG_LUONG_ID = fields.Many2one('tien.luong.bang.luong')


    TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_CHI_TIET_IDS = fields.One2many('tien.luong.hach.toan.chi.phi.luong.chi.tiet', 'CHI_TIET_ID', string='Hạch toán chi phí lương chi tiết')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ',help='Loại chứng từ')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.model
    def default_get(self, fields):
        rec = super(TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG, self).default_get(fields)
        rec['BANG_LUONG'] = self._context.get('default_bang_luong')

        id_bang_luong = None
        default_id_bang_luong = self._context.get('default_id_bang_luong')
        if default_id_bang_luong:
            id_bang_luong = int(default_id_bang_luong)
            rec['BANG_LUONG_ID'] = id_bang_luong
        bang_luong = self.env['tien.luong.bang.luong'].search([('id', '=', id_bang_luong)],limit=1)
        if bang_luong:
            loai_bang_luong = bang_luong.TEN_LOAI_BANG_LUONG
            thang = int(bang_luong.THANG)
            nam = int(bang_luong.NAM)
            rec['DIEN_GIAI'] = 'Hạch toán chi phí lương tháng ' + str(thang) + ' năm ' +str(nam)
            so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(nam, thang)
            ngay_cuoi_thang = '%s-%s-%s' % (nam,thang,so_ngay_trong_thang)
            rec['NGAY_HACH_TOAN'] = datetime.strptime(ngay_cuoi_thang, '%Y-%m-%d').date()
            rec['NGAY_CHUNG_TU'] = datetime.strptime(ngay_cuoi_thang, '%Y-%m-%d').date()

            # hạch toán chi phí lương
            # Lương cơ bản
            arr_list_hach_toan_chi_phi_luong = []

            bang_luong_chi_tiet = bang_luong.TIEN_LUONG_BANG_LUONG_CHI_TIET_IDS

            tk_no_nv_dong = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3341')],limit=1)
            if tk_no_nv_dong:
                tk_no_nv_dong_id = tk_no_nv_dong.id
                tk_co_luong_chinh_id = tk_no_nv_dong.id

            if loai_bang_luong == 'LUONG_CO_DINH':
                dic_luong_co_ban = {}
                for chi_tiet in bang_luong_chi_tiet:
                    id_tk_chi_phi_luong = chi_tiet.DON_VI_ID.TK_CHI_PHI_LUONG_ID.id
                    if id_tk_chi_phi_luong not in dic_luong_co_ban:
                        dic_luong_co_ban[id_tk_chi_phi_luong] = 0
                    dic_luong_co_ban[id_tk_chi_phi_luong] += chi_tiet.LUONG_CO_BAN

                for id_tk_chi_phi_luong in dic_luong_co_ban:
                    if dic_luong_co_ban.get(id_tk_chi_phi_luong) != 0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                        # tao ra dong moi
                        arr_list_hach_toan_chi_phi_luong += [(0,0,{
                            'DIEN_GIAI' : 'Lương cơ bản',
                            'TK_NO_ID' : id_tk_chi_phi_luong,
                            'TK_CO_ID': tk_co_luong_chinh_id,
                            'SO_TIEN' : dic_luong_co_ban.get(id_tk_chi_phi_luong),
                            })]
            
            elif loai_bang_luong == 'LUONG_THOI_GIAN_THEO_BUOI' or loai_bang_luong =='LUONG_THOI_GIAN_THEO_GIO':

                dic_luong_chinh = {}
                for chi_tiet in bang_luong_chi_tiet:
                    id_tk_chi_phi_luong = chi_tiet.DON_VI_ID.TK_CHI_PHI_LUONG_ID.id
                    if id_tk_chi_phi_luong not in dic_luong_chinh:
                        dic_luong_chinh[id_tk_chi_phi_luong] = 0
                    dic_luong_chinh[id_tk_chi_phi_luong] += chi_tiet.TONG_SO

                for id_tk_chi_phi_luong in dic_luong_chinh:
                    if dic_luong_chinh.get(id_tk_chi_phi_luong) != 0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                    # tao ra dong moi
                        arr_list_hach_toan_chi_phi_luong += [(0,0,{
                            'DIEN_GIAI' : 'Lương chính',
                            'TK_NO_ID' : id_tk_chi_phi_luong,
                            'TK_CO_ID': tk_co_luong_chinh_id,
                            'SO_TIEN' : dic_luong_chinh.get(id_tk_chi_phi_luong),
                            })]
            
            # BHTN công ty đóng
            dic_bhtn_cong_ty_dong = {}
            for chi_tiet in bang_luong_chi_tiet:
                id_tk_chi_phi_luong = chi_tiet.DON_VI_ID.TK_CHI_PHI_LUONG_ID.id
                if id_tk_chi_phi_luong not in dic_bhtn_cong_ty_dong:
                    dic_bhtn_cong_ty_dong[id_tk_chi_phi_luong] = 0
                dic_bhtn_cong_ty_dong[id_tk_chi_phi_luong] += chi_tiet.BHTN_CONG_TY_DONG

            tk_co_bhtn =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3386')],limit=1)
            if tk_co_bhtn:
                tk_co_bhtn_id = tk_co_bhtn.id
            
            for id_tk_chi_phi_luong in dic_bhtn_cong_ty_dong:

                if dic_bhtn_cong_ty_dong.get(id_tk_chi_phi_luong) != 0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                # tao ra dong moi
                    arr_list_hach_toan_chi_phi_luong += [(0,0,{
                        'DIEN_GIAI' : 'BHTN công ty đóng',
                        'TK_NO_ID' : id_tk_chi_phi_luong,
                        'TK_CO_ID': tk_co_bhtn_id,
                        'SO_TIEN' : dic_bhtn_cong_ty_dong.get(id_tk_chi_phi_luong),
                        })]
            
           
            tk_no_nv_dong = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3341')],limit=1)
            if tk_no_nv_dong:
                tk_no_nv_dong_id = tk_no_nv_dong.id

            so_tien_bhtn_nv_dong = 0
            so_tien_bhxh_nv_dong = 0 
            so_tien_bhyt_nv_dong = 0 
            thue_tncn_phai_nop = 0 
            for chi_tiet in bang_luong_chi_tiet:
                so_tien_bhtn_nv_dong += chi_tiet.BHTN_KHAU_TRU
                so_tien_bhxh_nv_dong += chi_tiet.BHXH_KHAU_TRU
                so_tien_bhyt_nv_dong += chi_tiet.BHYT_KHAU_TRU
                thue_tncn_phai_nop += chi_tiet.THUE_TNCN_KHAU_TRU
            
            # BHTN nhân viên đóng
            if so_tien_bhtn_nv_dong !=0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                arr_list_hach_toan_chi_phi_luong += [(0,0,{
                    'DIEN_GIAI' : 'BHTN nhân viên đóng',
                    'TK_NO_ID' : tk_no_nv_dong_id,
                    'TK_CO_ID': tk_co_bhtn_id,
                    'SO_TIEN' : so_tien_bhtn_nv_dong,
                        })]             
            
            # BHXH công ty đóng
            dic_bhxh_cong_ty_dong = {}
            for chi_tiet in bang_luong_chi_tiet:
                id_tk_chi_phi_luong = chi_tiet.DON_VI_ID.TK_CHI_PHI_LUONG_ID.id
                if id_tk_chi_phi_luong not in dic_bhxh_cong_ty_dong:
                    dic_bhxh_cong_ty_dong[id_tk_chi_phi_luong] = 0
                dic_bhxh_cong_ty_dong[id_tk_chi_phi_luong] += chi_tiet.BHXH_CONG_TY_DONG

            
            tk_co_bhxh =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3383')],limit=1)
            if tk_co_bhxh:
                tk_co_bhxh_id = tk_co_bhxh.id
            

            for id_tk_chi_phi_luong in dic_bhxh_cong_ty_dong:
                if dic_bhxh_cong_ty_dong.get(id_tk_chi_phi_luong) != 0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                # tao ra dong moi
                    arr_list_hach_toan_chi_phi_luong += [(0,0,{
                        'DIEN_GIAI' : 'BHXH công ty đóng',
                        'TK_NO_ID' : id_tk_chi_phi_luong,
                        'TK_CO_ID': tk_co_bhxh_id,
                        'SO_TIEN' : dic_bhxh_cong_ty_dong.get(id_tk_chi_phi_luong),
                        })]    

            # BHXH nhân viên đóng
            if so_tien_bhxh_nv_dong !=0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                arr_list_hach_toan_chi_phi_luong += [(0,0,{
                    'DIEN_GIAI' : 'BHXH nhân viên đóng',
                    'TK_NO_ID' : tk_no_nv_dong_id,
                    'TK_CO_ID': tk_co_bhxh_id,
                    'SO_TIEN' : so_tien_bhxh_nv_dong,
                        })]
            
            # BHYT công ty đóng
            dic_bhyt_cong_ty_dong = {}
            for chi_tiet in bang_luong_chi_tiet:
                id_tk_chi_phi_luong = chi_tiet.DON_VI_ID.TK_CHI_PHI_LUONG_ID.id
                if id_tk_chi_phi_luong not in dic_bhyt_cong_ty_dong:
                    dic_bhyt_cong_ty_dong[id_tk_chi_phi_luong] = 0
                dic_bhyt_cong_ty_dong[id_tk_chi_phi_luong] += chi_tiet.BHYT_CONG_TY_DONG

            
            tk_co_bhyt =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3384')],limit=1)
            if tk_co_bhyt:
                tk_co_bhyt_id = tk_co_bhyt.id

            for id_tk_chi_phi_luong in dic_bhyt_cong_ty_dong:
                if dic_bhyt_cong_ty_dong.get(id_tk_chi_phi_luong) != 0:#Nếu mà số tiền khác 0 mới tạo ra dòng mới
                # tao ra dong moi
                    arr_list_hach_toan_chi_phi_luong += [(0,0,{
                        'DIEN_GIAI' : 'BHYT công ty đóng',
                        'TK_NO_ID' : id_tk_chi_phi_luong,
                        'TK_CO_ID': tk_co_bhyt_id,
                        'SO_TIEN' : dic_bhyt_cong_ty_dong.get(id_tk_chi_phi_luong),
                        })]
            
            # BHYT nhân viên đóng
            if so_tien_bhyt_nv_dong !=0: #Nếu mà số tiền khác 0 mới tạo ra dòng mới
                arr_list_hach_toan_chi_phi_luong += [(0,0,{
                    'DIEN_GIAI' : 'BHYT nhân viên đóng',
                    'TK_NO_ID' : tk_no_nv_dong_id,
                    'TK_CO_ID': tk_co_bhyt_id,
                    'SO_TIEN' : so_tien_bhyt_nv_dong,
                        })]

            # KPCĐ công ty đóng
            dic_kpcd_cong_ty_dong = {}
            for chi_tiet in bang_luong_chi_tiet:
                id_tk_chi_phi_luong = chi_tiet.DON_VI_ID.TK_CHI_PHI_LUONG_ID.id
                if id_tk_chi_phi_luong not in dic_kpcd_cong_ty_dong:
                    dic_kpcd_cong_ty_dong[id_tk_chi_phi_luong] = 0
                dic_kpcd_cong_ty_dong[id_tk_chi_phi_luong] += chi_tiet.KPCD_CONG_TY_DONG

            tk_co_kpcd =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3382')],limit=1)
            if tk_co_kpcd:
                tk_co_kpcd_id = tk_co_kpcd.id

            for id_tk_chi_phi_luong in dic_kpcd_cong_ty_dong:
                if dic_kpcd_cong_ty_dong.get(id_tk_chi_phi_luong) != 0:
                # tao ra dong moi
                    arr_list_hach_toan_chi_phi_luong += [(0,0,{
                        'DIEN_GIAI' : 'KPCĐ công ty đóng',
                        'TK_NO_ID' : id_tk_chi_phi_luong,
                        'TK_CO_ID': tk_co_kpcd_id,
                        'SO_TIEN' : dic_kpcd_cong_ty_dong.get(id_tk_chi_phi_luong),
                        })]

            # Thuế TNCN cá nhân đóng
            
            tk_co_thue_tncn =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '3335')],limit=1)
            if tk_co_thue_tncn:
                tk_co_thue_tncn_id = tk_co_thue_tncn.id
            if thue_tncn_phai_nop != 0 :
                arr_list_hach_toan_chi_phi_luong += [(0,0,{
                    'DIEN_GIAI' : 'Thuế thu nhập cá nhân phải nộp',
                    'TK_NO_ID' : tk_no_nv_dong_id,
                    'TK_CO_ID': tk_co_thue_tncn_id,
                    'SO_TIEN' : thue_tncn_phai_nop,
                        })]

            rec['TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_CHI_TIET_IDS'] = arr_list_hach_toan_chi_phi_luong
        rec['LOAI_CHUNG_TU'] = 6030
        return rec
    
    @api.depends('TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_CHI_TIET_IDS.SO_TIEN')
    def _tong_so_tien(self):
        for order in self:
            tong_so_tien = 0
            for line in order.TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_CHI_TIET_IDS:
                tong_so_tien += line.SO_TIEN
            order.update({
                'SO_TIEN': tong_so_tien,
            })

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
        self.write({'state':'da_ghi_so'})

    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_CHI_TIET_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,
                'MODEL_CHUNG_TU' : self._name,
                'CHI_TIET_ID' : line.id,
                'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'DOI_TUONG_ID' : line.DOI_TUONG_NO_ID.id,
                'GHI_NO' : line.SO_TIEN,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
                'LOAI_HACH_TOAN' : '1',
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'DOI_TUONG_ID' : line.DOI_TUONG_CO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True