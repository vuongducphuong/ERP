# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime

class ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA(models.Model):
    _name = 'account.ex.ton.kho.vat.tu.hang.hoa'
    _description = 'Tồn kho vật tư hàng hóa'
    _inherit = ['mail.thread']
    
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng (*)', help='Mã hàng (*)', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    LIST_NHOM_VTHH = fields.Char(string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Mã kho (*)', help='Mã kho (*)')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_TON = fields.Float(string='Giá trị tồn', help='Giá trị tồn',digits=decimal_precision.get_precision('Product Price'))
    SO_LO = fields.Char(string='Số lô', help='Số lô')
    HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
    SO_LUONG_THEO = fields.Float(string='Số lượng theo', help='Số lượng theo', digits=decimal_precision.get_precision('SO_LUONG'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư ban đầu', help='Số dư ban đầu', ondelete='cascade')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    STT = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết', help='Thứ tự sắp xếp các dòng chi tiết')
    THU_TU_CHUNG_TU = fields.Integer(string='Thứ tự sắp xếp trong chứng từ', help='Thứ tự sắp xếp các dòng chi tiết dùng để sắp xếm khi tính giá')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', default='chua_ghi_so')
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    # SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    # SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
    DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đvt chính', help='Đvt chính')
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo đvt chính', help='Đơn giá theo đvt chính', digits=decimal_precision.get_precision('DON_GIA'))
    TY_LE_CHUYEN_DOI_THEO_DVT_CHINH = fields.Float(string='Tỷ lệ chuyển đổi theo đvt chính', help='Tỷ lệ chuyển đổi theo đvt chính')
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo (ĐVC)', help='Số lượng theo (ĐVC)', digits=decimal_precision.get_precision('SO_LUONG'))
    TOAN_TU_QUY_DOI = fields.Selection([('NHAN', '*'),('CHIA', '/'),],  default='NHAN',string="Toán tử quy đổi")
    CHI_TIET_VTHH = fields.Integer(string='Chi tiết theo vthh', help='Chi tiết theo vthh')
    NHAP_MA_QUY_CACH = fields.Char()
    TON_KHO_VAT_TU_HANG_HOA_MASTER_ID = fields.Many2one('account.ex.ton.kho.vat.tu.hang.hoa.master', string='Tồn kho vật tư hàng hóa master', help='Tồn kho vật tư hàng hóa master', ondelete='cascade')
    SO_KHO_ID = fields.Many2one('so.kho', ondelete='set null')
    # Mạnh bổ sung thêm trường theo dõi theo mã quy cách dùng để xác định sản phẩm có tích chọn mã quy cách hay chưa !
    THEO_DOI_THEO_MA_QUY_CACH = fields.Boolean(string='Theo dõi theo mã quy cách', help='Theo dõi theo mã quy cách')
    KHAI_BAO_DAU_KY = fields.Boolean(string='Khai báo đầu kỳ', help='Khai báo đầu kỳ', default=True)


    @api.onchange('MA_HANG_ID')
    def update_dong_nhap_ton_kho_vat_tu_hang_hoa(self):
        self.TEN_HANG = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', '=', self.MA_HANG_ID.id)],limit=1).TEN
        self.NHOM_VTHH_ID = self.env['danh.muc.nhom.vat.tu.hang.hoa.dich.vu'].search([('id', '=', self.MA_HANG_ID.id)],limit=1).MA
        self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
        self.NHAP_MA_QUY_CACH = 'Nhập mã quy cách'
        self.TY_LE_CHUYEN_DOI_THEO_DVT_CHINH = self.env['danh.muc.vat.tu.hang.hoa.don.vi.chuyen.doi'].search([('id', '=', self.MA_HANG_ID.id)],limit=1).TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
        self.TOAN_TU_QUY_DOI = self.env['danh.muc.vat.tu.hang.hoa.don.vi.chuyen.doi'].search([('id', '=', self.MA_HANG_ID.id)],limit=1).PHEP_TINH_CHUYEN_DOI
        self.THEO_DOI_THEO_MA_QUY_CACH =  self.MA_HANG_ID.THEO_DOI_THEO_MA_QUY_CACH

    # def kiem_tra_san_pham_ma_quy_cach(self,args):


    def action_ghi_so(self,thu_tu=0):
        self.ghi_so_kho(thu_tu)
        self.write({'state':'da_ghi_so'})


    def ghi_so_kho(self,thu_tu):
        line_ids = []
        data_ghi_no = {}
        ngay_hach_toan_str = ''
        ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
        if ngay_bat_dau_nam_tai_chinh:
            ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
            ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
            ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')
        data_ghi_no.update({
            'ID_CHUNG_TU': self.id,
            'MODEL_CHUNG_TU' : self._name,
            'LOAI_CHUNG_TU' : 611,
            'SO_CHUNG_TU' : 'OPN',
            'NGAY_HACH_TOAN': ngay_hach_toan_str,
            'NGAY_CHUNG_TU': ngay_hach_toan_str,
            'DVT_ID': self.DVT_ID.id,
            'SO_LUONG_NHAP' : self.SO_LUONG,
            'SO_LUONG_XUAT' : 0,
            'SO_TIEN_NHAP' :  self.GIA_TRI_TON,
            'SO_LUONG_NHAP_THEO_DVT_CHINH':  self.SO_LUONG,
            'SO_LUONG_XUAT_THEO_DVT_CHINH': 0,
            'DVT_CHINH_ID':  self.DVT_CHINH_ID.id,
            'KHO_ID' : self.KHO_ID.id,
            'MA_HANG_ID' :  self.MA_HANG_ID.id,
            'CHI_NHANH_ID' :  self.CHI_NHANH_ID.id,
            'DON_GIA' : self.GIA_TRI_TON/self.SO_LUONG if self.SO_LUONG != 0 else 0,
            'LOAI_KHU_VUC_NHAP_XUAT' : '1',
            'THU_TU_TRONG_CHUNG_TU' : thu_tu,
            'LA_NHAP_KHO' : True,
            # 'CHI_TIET_ID' : vals.id,
        })
        line_ids = [(0,0,data_ghi_no)]
		# Tạo master
        sc = self.env['so.kho'].create({
			# 'name': self.SO_CHUNG_TU,
			'line_ids': line_ids,
			})
        self.write({'SO_KHO_ID':sc.id})
        return True

    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()


    def import_from_excel(self, import_fields, data):
        # 1. trường hợp import thông thuwongf, gọi vào hàm load()
        if data and import_fields:
            dict_create = {}
            arr_excel = []
            dict_loi = {}
            error = []

            data_field = []
            for row in data:
                j = 0
                row_field = {}
                for field in import_fields:
                    row_field[field] = row[j]
                    j += 1
                data_field.append(row_field)

            du_lieu_trong_dtb = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([])
            i = 0
            for data in data_field:
                i += 1
                ma_hang = False
                don_vi_tinh = False
                ma_kho = False
                if data.get('MA_HANG_ID') != '':
                    vthh = self.env['danh.muc.vat.tu.hang.hoa'].search([('MA', '=', data.get('MA_HANG_ID'))])
                    if vthh:
                        ma_hang = vthh.id
                    else:
                        # thong_bao = u'cột Mã hàng dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/vật tư hàng hóa'
                        # error.append({'type':'error', 'message' : thong_bao})
                        dict_loi[i] = 'Mã hàng: '
                if data.get('DVT_ID') != '':
                    dvt = self.env['danh.muc.don.vi.tinh'].search([('DON_VI_TINH', '=', data.get('DVT_ID'))])
                    if dvt:
                        don_vi_tinh = dvt.id
                    else:
                        # thong_bao = u'cột ĐVT dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/đơn vị tính'
                        # error.append({'type':'error', 'message' : thong_bao})
                        dict_loi[i] = 'ĐVT: '
                if data.get('KHO_ID') != '':
                    kho = self.env['danh.muc.kho'].search([('MA_KHO', '=', data.get('KHO_ID'))])
                    if kho:
                        ma_kho = kho.id
                    else:
                        # thong_bao = u'cột Mã kho dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/kho'
                        # error.append({'type':'error', 'message' : thong_bao})
                        dict_loi[i] = 'Mã kho: '
                key_data_excel = str(ma_kho) +','+ str(ma_hang)
                arr_excel.append(key_data_excel)
                
                if ma_kho not in dict_create:
                    dict_create[ma_kho] = []

                line_ids = dict_create[ma_kho]
                du_lieu_1_dong = {
                    'MA_HANG_ID' : ma_hang,  #Mã hàng
                    'TEN_HANG' : data.get('TEN_HANG'), #Tên hàng
                    'LIST_NHOM_VTHH' : data.get('LIST_NHOM_VTHH'), #Nhóm VTHH
                    'DVT_ID' : don_vi_tinh, # ĐVT
                    'KHO_ID' : ma_kho, # Mã kho
                    'SO_LUONG' : float(data.get('SO_LUONG')) if data.get('SO_LUONG') != '' else False,  # Số lượng
                    'GIA_TRI_TON' : float(data.get('GIA_TRI_TON')) if data.get('GIA_TRI_TON') != '' else False,  # Giá trị tồn
                    'SO_LO' : float(data.get('SO_LO')) if data.get('SO_LO') != '' else False,  # Số lô
                    'HAN_SU_DUNG' : data.get('HAN_SU_DUNG') if data.get('HAN_SU_DUNG') !='' else False,  #Hạn sử dụng
                    'SO_LUONG_THEO_DVT_CHINH' : float(data.get('SO_LUONG_THEO_DVT_CHINH')) if data.get('SO_LUONG_THEO_DVT_CHINH') !='' else False,  # Số lượng theo (ĐVC)
                    'DON_GIA' : float(data.get('GIA_TRI_TON'))/float(data.get('SO_LUONG')) if data.get('GIA_TRI_TON') != '' and data.get('SO_LUONG') != '' and float(data.get('SO_LUONG')) != 0 else 0,
                    'DON_GIA_THEO_DVT_CHINH' : float(data.get('GIA_TRI_TON'))/float(data.get('SO_LUONG')) if data.get('GIA_TRI_TON') != '' and data.get('SO_LUONG') != '' and float(data.get('SO_LUONG')) != 0 else 0,
                    'DVT_CHINH_ID' : don_vi_tinh,
                }                    
                line_ids += [(0,0,du_lieu_1_dong)]

            if du_lieu_trong_dtb:
                for du_lieu in du_lieu_trong_dtb:
                    key_data_base = str(du_lieu.KHO_ID.id) +','+ str(du_lieu.MA_HANG_ID.id)
                    
                    # dict_database[key_data_base] = du_lieu
                    if key_data_base not in arr_excel:
                        ma_kho = du_lieu.KHO_ID.id

                        if ma_kho not in dict_create:
                            dict_create[ma_kho] = []

                        line_ids = dict_create[ma_kho]
                        du_lieu_1_dong = {
                            'MA_HANG_ID' : du_lieu.MA_HANG_ID.id,  #Mã hàng
                            'TEN_HANG' : du_lieu.TEN_HANG, #Tên hàng
                            'LIST_NHOM_VTHH' : du_lieu.LIST_NHOM_VTHH, #Nhóm VTHH
                            'DVT_ID' : du_lieu.DVT_ID.id, # ĐVT
                            'KHO_ID' : du_lieu.KHO_ID.id, # Mã kho
                            'SO_LUONG' : du_lieu.SO_LUONG,  # Số lượng
                            'GIA_TRI_TON' : du_lieu.GIA_TRI_TON,  # Giá trị tồn
                            'SO_LO' : du_lieu.SO_LO,  # Số lô
                            'HAN_SU_DUNG' : du_lieu.HAN_SU_DUNG,  #Hạn sử dụng
                            'SO_LUONG_THEO_DVT_CHINH' : du_lieu.SO_LUONG_THEO_DVT_CHINH,  # Số lượng theo (ĐVC)
                            'DON_GIA' : float(du_lieu.GIA_TRI_TON)/float(du_lieu.SO_LUONG) if du_lieu.SO_LUONG != '' and du_lieu.GIA_TRI_TON != '' and float(du_lieu.SO_LUONG) != 0 else 0,
                            'DON_GIA_THEO_DVT_CHINH' : float(du_lieu.GIA_TRI_TON)/float(du_lieu.SO_LUONG) if du_lieu.SO_LUONG != '' and du_lieu.GIA_TRI_TON != '' and float(du_lieu.SO_LUONG) != 0 else 0,
                            'DVT_CHINH_ID' : don_vi_tinh,
                        }                    
                        line_ids += [(0,0,du_lieu_1_dong)]
            
            # tạo mới dữ liệu
            for kho_create in dict_create:
                self.env['account.ex.ton.kho.vat.tu.hang.hoa.master'].create({
                    'KHO_ID': kho_create,
                    'ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS': dict_create[kho_create],
                })
            if dict_loi:
                for key in dict_loi:
                    thong_bao = u'cột ' +dict_loi[key]+ ' dòng thứ ' + str(key) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/kho'
                    error.append({'type':'error', 'message' : thong_bao})
        if error == []:
            return {}
        else:
            return {'messages' : error}
        # return self.load(import_fields, data)
        # # trường hợp tự xử lý
        # # 2. nếu không có lỗi/Warning
        # return {}
        # # 3. nếu có lỗi thì trả về theo định dạng:
        # error = []
        # error.append({'type':'error', 'message' : u"Thông báo lỗi"})
        # return {'messages' : error}




