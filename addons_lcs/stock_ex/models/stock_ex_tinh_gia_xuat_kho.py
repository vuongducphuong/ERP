# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
import json
from odoo.tools.float_utils import float_round
from odoo.exceptions import ValidationError
from datetime import datetime
import numpy as np

class STOCK_EX_TINH_GIA_XUAT_KHO(models.Model):
    _name = 'stock.ex.tinh.gia.xuat.kho'
    _description = ''
    _auto = False

    VAT_TU_HANG_HOA_SELECTION = fields.Selection([
        ('TINH_TAT_CA_CAC_VAT_TU_HANG_HOA', 'Tính tất cả các vật tư hàng hóa'), 
        ('CHON_VAT_TU_HANG_HOA', ' Chọn vật tư hàng hóa') 
        ],default='TINH_TAT_CA_CAC_VAT_TU_HANG_HOA')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='NAM_NAY',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    KY_TINH_GIA = fields.Selection([('THANG', 'Tháng'), ('QUY', ' Qúy'), ('NAM', ' Năm'), ], string='Kỳ tính giá', help='Kỳ tính giá',default='THANG',required=True)
    TINH_GIA_SELECTION = fields.Selection([('TINH_THEO_KHO', 'Tính theo kho'), ('TINH_GIA_KHONG_THEO_KHO', ' Tính giá không theo kho'), ],default='TINH_THEO_KHO',required=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    LIST_VTHH = fields.Char(string='List vật tư hàng hóa', help='List vật tư hàng hóa')

    CHON_CHI_PHI_JSON = fields.Text(store=False)
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(STOCK_EX_TINH_GIA_XUAT_KHO, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result

    def action_view_result(self):
        action = self.env.ref('stock_ex.action_open_stock_ex_tinh_gia_xuat_kho_form').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')


    def _validate(self,tu_ngay,den_ngay,so_ngay_trong_thang):
        if(self.TU_NGAY == False):
            raise ValidationError('Vui lòng nhập thời gian cho Từ ngày !')
        if(self.DEN_NGAY == False):
            raise ValidationError('Vui lòng nhập thời gian cho Đến ngày !')
        if tu_ngay.day != 1:
            raise ValidationError('Từ ngày phải là ngày đầu tháng')
        if den_ngay.day != so_ngay_trong_thang:
            raise ValidationError('Đến ngày phải là ngày cuối tháng')
        if den_ngay.year != tu_ngay.year:
            raise ValidationError('Bạn chỉ có thể xem dữ liệu trong vòng 1 năm')
        if den_ngay.month < tu_ngay.month:
            raise ValidationError('Từ ngày phải nhỏ hơn đến ngày')

        ngay_cuoi_thang = '%s-%s-%s' % (den_ngay.year,den_ngay.month,so_ngay_trong_thang)
        # ngay_cuoi_thang_datetiome = datetime.strptime(ngay_cuoi_thang, '%Y-%m-%d').date()

        if self.KY_TINH_GIA == 'QUY':
            if den_ngay.month - tu_ngay.month in (2,5,8,11):
                # if (tu_ngay.month != 1 and den_ngay.month != 3) or (tu_ngay.month != 4 and den_ngay.month != 6) or (tu_ngay.month != 7 and den_ngay.month != 9) or (tu_ngay.month != 10 and den_ngay.month != 12):
                if tu_ngay.month not in (1,4,7,10):
                    raise ValidationError('Từ ngày đến ngày phải là 1 quý')
            else:
                raise ValidationError('Từ ngày đến ngày phải là 1 quý')
        if self.KY_TINH_GIA == 'NAM':
            if tu_ngay.month !=1 or den_ngay.month != 12:
                raise ValidationError('Từ ngày đến ngày phải là 1 năm')


    def btn_tinh_gia_xuat_kho(self, args):

        phuong_phap_tinh_gia = self.env['ir.config_parameter'].get_param('he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO')
        if phuong_phap_tinh_gia:
            if phuong_phap_tinh_gia != 'BINH_QUAN_CUOI_KY':
                raise ValidationError('Hiện tại phần chỉ hỗ trợ phương pháp <Bình quân cuối kỳ> bạn vui lòng chọn lại phương pháp tính giá xuất kho')
            else:
                tu_ngay = datetime.strptime(self.TU_NGAY, '%Y-%m-%d').date()
                den_ngay = datetime.strptime(self.DEN_NGAY, '%Y-%m-%d').date()

                list_vthh = None
                if self.LIST_VTHH:
                    list_vthh = self.LIST_VTHH
                
                # ngay_cuoi_thang = '%s-%s-%s' % (den_ngay.year,den_ngay.month,so_ngay_trong_thang)
                # hieu_thang = den_ngay.month - tu_ngay.month
                so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(den_ngay.year, den_ngay.month)
                self._validate(tu_ngay,den_ngay,so_ngay_trong_thang)

                if self.KY_TINH_GIA == 'THANG':
                    for i in range(tu_ngay.month,den_ngay.month + 1):
                        so_ngay_trong_thang_tinh = helper.Datetime.lay_so_ngay_trong_thang(den_ngay.year, i)
                        tu_ngay_tinh = '%s-%s-%s' % (den_ngay.year,i,1)
                        den_ngay_tinh = '%s-%s-%s' % (tu_ngay.year,i,so_ngay_trong_thang_tinh)
                        self.binh_quan_cuoi_ky(tu_ngay_tinh,den_ngay_tinh,list_vthh)
                        a = 1
                elif self.KY_TINH_GIA == 'QUY':
                    tu_ngay_theo_quy = tu_ngay
                    
                    while tu_ngay_theo_quy.month < den_ngay.month or tu_ngay_theo_quy.month > 12:
                        so_ngay_den_ngay_theo_quy = helper.Datetime.lay_so_ngay_trong_thang(tu_ngay_theo_quy.year,tu_ngay_theo_quy.month + 2)
                        den_ngay_theo_quy = '%s-%s-%s' % (tu_ngay_theo_quy.year,tu_ngay_theo_quy.month + 2,so_ngay_den_ngay_theo_quy)
                        tu_ngay_tr = '%s-%s-%s' % (tu_ngay_theo_quy.year,tu_ngay_theo_quy.month,tu_ngay_theo_quy.day)
                        self.binh_quan_cuoi_ky(tu_ngay_tr,den_ngay_theo_quy,list_vthh)
                        i = 0

                        if tu_ngay_theo_quy.month < 10:
                            so_ngay_den_ngay_theo_quy = helper.Datetime.lay_so_ngay_trong_thang(tu_ngay_theo_quy.year,tu_ngay_theo_quy.month + 3)
                            tu_ngay_theo_quy = datetime.strptime('%s-%s-%s' % (tu_ngay_theo_quy.year,tu_ngay_theo_quy.month + 3,1), '%Y-%m-%d').date()
                        else:
                            break
                else:
                    self.binh_quan_cuoi_ky(self.TU_NGAY,self.DEN_NGAY,list_vthh)
        else:
            raise ValidationError('Bạn chưa chọn phương pháp tính giá xuất kho vui lòng vào Hệ thống/ Tùy chọn để thiết lập phương pháp tính giá xuất kho')

        ket_qua = 'Tính giá xuất kho hoàn thành'
        return ket_qua


    def binh_quan_cuoi_ky(self,tu_ngay,den_ngay,list_vthh,chi_tinh_lap_rap_thao_do=False):
        phan_thap_phan_don_gia = 0
        thiet_lap_phan_thap_phan_don_gia = self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_DON_GIA')
        if thiet_lap_phan_thap_phan_don_gia:
            phan_thap_phan_don_gia = int(thiet_lap_phan_thap_phan_don_gia)
        #tinh lap rap truoc:
        if not chi_tinh_lap_rap_thao_do: #neu tinh tat ca thi moi goi vao cuoi ky
            self.binh_quan_cuoi_ky(tu_ngay,den_ngay,list_vthh,True)

        #tinh tat ca:
        dict_gia_tri = {}
        dict_so_kho_chuyen_kho = {}
        dict_hang_ban_tra_lai = {}
        dict_so_kho = {}
        dict_gia_von = {}
        dict_gia_von_tra_lai_hb = {}
        arr_ma_hang_id = []
        arr_kho_id = []
        # tạo dict lưu giá trị tính giá xuất kho
        gia_tri_update = self.function_chung(tu_ngay,den_ngay,'gia_tri_update',list_vthh)
        if gia_tri_update:
            for gia_tri in gia_tri_update:
                if gia_tri.get('MA_HANG_ID') not in arr_ma_hang_id:
                    arr_ma_hang_id.append(gia_tri.get('MA_HANG_ID'))
               
                if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
                    key_gia_tri = str(gia_tri.get('MA_HANG_ID')) + ',' + str(gia_tri.get('MA_KHO_ID'))
                else:
                    key_gia_tri = str(gia_tri.get('MA_HANG_ID'))
                if key_gia_tri not in dict_gia_tri:
                    dict_gia_tri[key_gia_tri] = []
                dict_gia_tri[key_gia_tri] += [gia_tri]

        so_kho_sql_ids = self.function_chung(tu_ngay,den_ngay,'so_kho',list_vthh)
        # dict so kho
        for so_kho_dict in so_kho_sql_ids:
            if so_kho_dict.get('MA_HANG_ID') not in arr_ma_hang_id:
                arr_ma_hang_id.append(so_kho_dict.get('MA_HANG_ID'))

            if so_kho_dict.get('KHO_ID') not in arr_kho_id:
                arr_kho_id.append(so_kho_dict.get('KHO_ID'))

            key_so_kho = str(so_kho_dict.get('CHI_TIET_ID')) + ',' + str(so_kho_dict.get('CHI_TIET_MODEL'))
            if key_so_kho not in dict_so_kho:
                dict_so_kho[key_so_kho] = []
            dict_so_kho[key_so_kho] += [so_kho_dict]
        # Tính thêm chuyển kho
        tra_lai_hang_ban_ids_tinh_them_ids = self.function_chung(tu_ngay,den_ngay,'tra_lai_hang_ban',list_vthh)    
        if tra_lai_hang_ban_ids_tinh_them_ids:
            for tra_lai_hang_ban_tinh_them in tra_lai_hang_ban_ids_tinh_them_ids:
                key_tra_lai_model = str(tra_lai_hang_ban_tinh_them.get('NHAP_XUAT_KHO_CHI_TIET_ID')) + ',' + str(tra_lai_hang_ban_tinh_them.get('MODEL_NHAP_XUAT_KHO_CHI_TIET'))
                #cvhuan bi cho dict
                key_tra_lai_hang_kho = str(tra_lai_hang_ban_tinh_them.get('MA_HANG_ID')) + ',' + str(tra_lai_hang_ban_tinh_them.get('MA_KHO_ID'))
                # if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
                #     key_tra_lai_hang_kho = str(tra_lai_hang_ban_tinh_them.get('MA_HANG_ID')) + ',' + str(tra_lai_hang_ban_tinh_them.get('MA_KHO_ID'))
                # else:
                #     key_tra_lai_hang_kho = str(tra_lai_hang_ban_tinh_them.get('MA_HANG_ID'))
                if key_tra_lai_hang_kho not in dict_hang_ban_tra_lai:
                    dict_hang_ban_tra_lai[key_tra_lai_hang_kho] = []
                #lay gia tri tu so kho
                if key_tra_lai_model in dict_so_kho:
                    dict_hang_ban_tra_lai[key_tra_lai_hang_kho] += dict_so_kho[key_tra_lai_model]
                        
        # quanhm: tinh gia xuat kho ------------------------
        
        dict_nhap_kho = {} #san pham, kho
        dict_chuyen_kho = {} #san pham, kho nhap, san pham, kho xuat
        dict_tra_lai = {} #san pham, kho
        dict_lap_rap = {} #san pham, kho nhap, san pham xuat, kho xuat

        for key_so_kho in dict_gia_tri:
            for gia_tri_so_kho in dict_gia_tri[key_so_kho]:
                don_gia = 0
                so_luong = gia_tri_so_kho.get('TONG_SL_NHAP')
                tien_von = gia_tri_so_kho.get('TONG_GIA_TRI_NHAP')
                dict_nhap_kho[key_so_kho] = {
                    "SL": gia_tri_so_kho.get('TONG_SL_NHAP'),
                    "GT": gia_tri_so_kho.get('TONG_GIA_TRI_NHAP')
                    }

        #chuyen kho tu db
        chuyen_kho_ids = self.function_chung(tu_ngay,den_ngay,'chuyen_kho',list_vthh)
        if chuyen_kho_ids:
            for chuyen_kho_dto in chuyen_kho_ids:
                key_chuyen_kho = str(chuyen_kho_dto.get('MA_HANG_ID')) + ',' + str(chuyen_kho_dto.get('NHAP_TAI_KHO_ID')) + ',' + str(chuyen_kho_dto.get('MA_HANG_ID')) + ',' + str(chuyen_kho_dto.get('XUAT_TAI_KHO_ID')) 
                #cvhuan bi cho dict
               
                #lay gia tri tu so kho
                if key_chuyen_kho not in dict_chuyen_kho:
                    dict_chuyen_kho[key_chuyen_kho] = []
                dict_chuyen_kho[key_chuyen_kho] += [{
                    "SL": chuyen_kho_dto.get('TONG_SL')
                    }]

        #chuyen kho tu db
        lap_rap_thao_do_ids = self.function_chung(tu_ngay,den_ngay,'lap_rap_thao_do',list_vthh)
        if lap_rap_thao_do_ids:
            for lap_rap_thao_do_dto in lap_rap_thao_do_ids:               

                if lap_rap_thao_do_dto.get('SO_LUONG') > 0:

                    key_so_kho_xuat_join = str(lap_rap_thao_do_dto.get('CHI_TIET_ID')) + ',' + str(lap_rap_thao_do_dto.get('CHI_TIET_MODEL'))
                    # coi ket qua cua sql tra ve la dung, luong la xuat
                    if key_so_kho_xuat_join in dict_so_kho:
                        for so_kho_xuat in dict_so_kho[key_so_kho_xuat_join]:

                            key_lap_rap_thao_do = str(lap_rap_thao_do_dto.get('MA_HANG_ID')) + ',' + str(lap_rap_thao_do_dto.get('MA_KHO_ID')) + ',' + str(so_kho_xuat.get('MA_HANG_ID')) + ',' + str(so_kho_xuat.get('KHO_ID')) 
                            #cvhuan bi cho dict
                        
                            #lay gia tri tu so kho
                            if key_lap_rap_thao_do not in dict_lap_rap:
                                dict_lap_rap[key_lap_rap_thao_do] = []
                            dict_lap_rap[key_lap_rap_thao_do] += [{
                                                                "SL": so_kho_xuat.get('SO_LUONG_XUAT_THEO_DVT_CHINH')
                                                            }]
        
        # #quanhm 25-07: code cho viec debug
        # san_phams = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', 'in', (122,122))])

        # # khos = self.env['danh.muc.kho'].search([])
        # khos = self.env['danh.muc.kho'].search([('id', 'in', (17,18,19))])

        # dict_san_pham_kho = []
        # for san_pham_dto in san_phams:
        #     for kho_dto in khos:
        #         dict_san_pham_kho += [{
        #             "MA_HANG_ID": san_pham_dto.id,
        #             "MA_KHO_ID": kho_dto.id,
        #             "TEN_KHO": kho_dto.TEN_KHO
        #             }
        #             ]

        dict_san_pham_kho = []
        for san_pham_dto in arr_ma_hang_id:
            for kho_dto in arr_kho_id:
                dict_san_pham_kho += [{
                    "MA_HANG_ID": san_pham_dto,
                    "MA_KHO_ID": kho_dto,
                    # "TEN_KHO": kho_dto.TEN_KHO
                    }
                    ]

        dic_phuong_trinh = {} #{kho nhap, [kho xuat: so luong xuat]}

        dic_gia_tri_nhap = {}
        if dict_san_pham_kho:
            for san_pham_kho_nhap_dto in dict_san_pham_kho:
                key_san_pham_kho_nhap = str(san_pham_kho_nhap_dto.get('MA_HANG_ID')) + ',' + str(san_pham_kho_nhap_dto.get('MA_KHO_ID'))

                #lay gia tri
                if key_san_pham_kho_nhap not in dic_gia_tri_nhap:
                    dic_gia_tri_nhap[key_san_pham_kho_nhap] = 0
                
                if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
                    key_gia_tri_nhap = str(san_pham_kho_nhap_dto.get('MA_HANG_ID')) + ',' + str(san_pham_kho_nhap_dto.get('MA_KHO_ID'))
                else:
                    key_gia_tri_nhap = str(san_pham_kho_nhap_dto.get('MA_HANG_ID'))
                if key_gia_tri_nhap in dict_gia_tri:
                    for dto in dict_gia_tri[key_gia_tri_nhap]:
                        dic_gia_tri_nhap[key_san_pham_kho_nhap] += dto.get('TONG_GIA_TRI_NHAP')

                tong_luong_nhap = 0

                dic_phuong_trinh[key_san_pham_kho_nhap] = {}
                #lay phuong trinh
                for san_pham_kho_xuat_dto in dict_san_pham_kho:
                    key_san_pham_kho_xuat = str(san_pham_kho_xuat_dto.get('MA_HANG_ID')) + ',' + str(san_pham_kho_xuat_dto.get('MA_KHO_ID'))

                    key_nhap_xuat = key_san_pham_kho_nhap + ',' + key_san_pham_kho_xuat

                    #so luong nhap tu ben ngoai
                    if key_san_pham_kho_xuat == key_san_pham_kho_nhap:
                        if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
                            key_gia_tri = str(san_pham_kho_xuat_dto.get('MA_HANG_ID')) + ',' + str(san_pham_kho_xuat_dto.get('MA_KHO_ID'))
                        else:
                            key_gia_tri = str(san_pham_kho_xuat_dto.get('MA_HANG_ID'))
                        if key_gia_tri in dict_gia_tri:
                            for dto in dict_gia_tri[key_gia_tri]:
                                tong_luong_nhap += dto.get('TONG_SL_NHAP')

                
                    #tinh luong nhap chuyen kho
                    so_luong_xuat_sang = 0
                    if key_nhap_xuat in dict_chuyen_kho:
                        for dto in dict_chuyen_kho[key_nhap_xuat]:
                            so_luong_xuat_sang += dto.get("SL")
                            tong_luong_nhap += dto.get("SL")
                    
                    #lap rap -> tam thoi bo
                    # if key_nhap_xuat in dict_lap_rap:
                    #     for dto in dict_lap_rap[key_nhap_xuat]:
                    #         so_luong_xuat_sang += dto.get("SL")

                   

                    dic_phuong_trinh[key_san_pham_kho_nhap][key_san_pham_kho_xuat] = -1 * so_luong_xuat_sang #lay dau am

                #dua va tong nhap                
                dic_phuong_trinh[key_san_pham_kho_nhap][key_san_pham_kho_nhap] = tong_luong_nhap
            
            # chuan bi du lieu cho vao phuong trinh
            arr_gia_tri = []
            
            for key_sp_nhap in dic_gia_tri_nhap:
                arr_gia_tri += [dic_gia_tri_nhap.get(key_sp_nhap)]
            
            arr_xuat = []
            for san_pham_kho_nhap_dto in dict_san_pham_kho:
                key_san_pham_kho_nhap = str(san_pham_kho_nhap_dto.get('MA_HANG_ID')) + ',' + str(san_pham_kho_nhap_dto.get('MA_KHO_ID'))
                temp = []
                #lay phuong trinh
                for san_pham_kho_xuat_dto in dict_san_pham_kho:
                    key_san_pham_kho_xuat = str(san_pham_kho_xuat_dto.get('MA_HANG_ID')) + ',' + str(san_pham_kho_xuat_dto.get('MA_KHO_ID'))

                    temp += [dic_phuong_trinh[key_san_pham_kho_nhap][key_san_pham_kho_xuat]]

                arr_xuat += [temp]

            # for key_sp_nhap in dic_phuong_trinh:
            #     temp = []
            #     for key_sp_xuat in dic_phuong_trinh[key_sp_nhap]:
            #         temp += [dic_phuong_trinh[key_sp_nhap][key_sp_xuat]]
            #     arr_xuat += [temp]
            
            a = np.array(arr_xuat)
            b = np.array(arr_gia_tri)
            ket_qua = np.linalg.lstsq(a,b)

            #cho vao ket qua
            dict_gia_von = {}
            i = 0
            for key_sp_nhap in dic_gia_tri_nhap:                
                dict_gia_von[key_sp_nhap] = ket_qua[0][i]
                i+=1
            
         #------------------------------------------

        

        #chuyen kho tu db
        # tra_lai_hang_ban_ids = self.function_chung(tu_ngay,den_ngay,'tra_lai_hang_ban')
        # if tra_lai_hang_ban_ids:
        #     for tra_lai_dto in tra_lai_hang_ban_ids:
        #         key_chuyen_kho = str(tra_lai_dto.get('MA_HANG_ID')) + ',' + str(tra_lai_dto.get('NHAP_TAI_KHO_ID')) + ',' + str(tra_lai_dto.get('MA_HANG_ID')) + ',' + str(tra_lai_dto.get('XUAT_TAI_KHO_ID')) 
        #         #cvhuan bi cho dict
               
        #         #lay gia tri tu so kho
        #         if key_chuyen_kho not in dict_chuyen_kho:
        #             dict_chuyen_kho[key_chuyen_kho] = []
        #         dict_chuyen_kho[key_chuyen_kho] += [chuyen_kho_dto]

        # if so_kho_sql_ids:
        #     # tạo dict chuyển kho
        #     for so_kho_chuyen_kho_sql in so_kho_sql_ids:
        #         if so_kho_chuyen_kho_sql.get('LOAI_KHU_VUC_NHAP_XUAT') == '2' and so_kho_chuyen_kho_sql.get('SO_LUONG_NHAP_THEO_DVT_CHINH') > 0 and so_kho_chuyen_kho_sql.get('KHONG_CAP_NHAT_GIA_XUAT') == False and so_kho_chuyen_kho_sql.get('LOAI_CHUNG_TU') != 2031:
        #             if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
        #                 key_chuyen_kho = str(so_kho_chuyen_kho_sql.get('MA_HANG_ID')) + ',' + str(so_kho_chuyen_kho_sql.get('KHO_ID'))
        #             else:
        #                 key_chuyen_kho = str(so_kho_chuyen_kho_sql.get('MA_HANG_ID'))
        #             if key_chuyen_kho not in dict_so_kho_chuyen_kho:
        #                 dict_so_kho_chuyen_kho[key_chuyen_kho] = []
        #             dict_so_kho_chuyen_kho[key_chuyen_kho] += [so_kho_chuyen_kho_sql]

            
        #---------------------------------Tính lắp ráp tháo dỡ để cập nhật trc---------------------------------
        if chi_tinh_lap_rap_thao_do:
            # update từ bảng lắp ráp tháo dỡ
            dict_lap_rap_thao_do_cha = {}
            lap_rap_thao_do_ids = self.function_chung(tu_ngay,den_ngay,'lap_rap_thao_do',list_vthh)
            if lap_rap_thao_do_ids:
                for lap_rap_thao_do in lap_rap_thao_do_ids:
                    if lap_rap_thao_do.get('NHAP_XUAT_KHO_CHI_TIET_ID') not in dict_lap_rap_thao_do_cha:
                        dict_lap_rap_thao_do_cha[lap_rap_thao_do.get('NHAP_XUAT_KHO_CHI_TIET_ID')] = []
                    dict_lap_rap_thao_do_cha[lap_rap_thao_do.get('NHAP_XUAT_KHO_CHI_TIET_ID')] += [lap_rap_thao_do]

            dict_gia_chi_lap_rap = {}
            
            for key_lap_rap_cha in dict_lap_rap_thao_do_cha:
                tong_luong_nhap = 0
                tong_gia_tri_xuat = 0
                for lap_rap in dict_lap_rap_thao_do_cha[key_lap_rap_cha]:
                    tong_luong_nhap = lap_rap.get('SO_LUONG')

                    #tong gia tri xuat
                    key_id_model_xuat_kho_chi_tiet = str(lap_rap.get('CHI_TIET_ID')) + ',' + str(lap_rap.get('CHI_TIET_MODEL'))
                    if key_id_model_xuat_kho_chi_tiet in dict_so_kho:
                        for nhap_xuat_kho_chi_tiet in dict_so_kho[key_id_model_xuat_kho_chi_tiet]:
                            key_xuat_kho_lap_rap_thao_do = str(nhap_xuat_kho_chi_tiet.get('MA_HANG_ID')) + ',' + str(nhap_xuat_kho_chi_tiet.get('KHO_ID'))
                            don_gia_von_xuat_kho = 0
                            if key_xuat_kho_lap_rap_thao_do in dict_gia_von:
                                if dict_gia_von[key_xuat_kho_lap_rap_thao_do] > 0:
                                    don_gia_von_xuat_kho = dict_gia_von[key_xuat_kho_lap_rap_thao_do]

                            tong_gia_tri_xuat += nhap_xuat_kho_chi_tiet.get('SO_LUONG_XUAT_THEO_DVT_CHINH')*don_gia_von_xuat_kho
                
                #gan ket qua 
                # for lap_rap in dict_lap_rap_thao_do_cha[key_lap_rap_cha]:
                #     key_nhap_kho_lap_rap_thao_do = str(lap_rap.get('MA_HANG_ID')) + ',' + str(lap_rap.get('MA_KHO_ID'))
                
                #     if key_nhap_kho_lap_rap_thao_do not in dict_gia_chi_lap_rap:
                #         dict_gia_chi_lap_rap[key_nhap_kho_lap_rap_thao_do] = tong_gia_tri_xuat / tong_luong_nhap
                don_gia_lap_rap_thao_do = tong_gia_tri_xuat / tong_luong_nhap
                # # update sổ cái
                so_cai_search_lap_rap_thao_do_ids = self.env['so.cai.chi.tiet'].search([('CHI_TIET_ID','=', key_lap_rap_cha),('CHI_TIET_MODEL','=', 'stock.ex.nhap.xuat.kho.chi.tiet')])
                if so_cai_search_lap_rap_thao_do_ids:
                    for so_cai_search_lap_rap_thao_do in so_cai_search_lap_rap_thao_do_ids:
                        if so_cai_search_lap_rap_thao_do.LOAI_HACH_TOAN == '1':
                            so_cai_search_lap_rap_thao_do.write({'GHI_NO' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                                                'GHI_NO_NGUYEN_TE' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                                                'GHI_CO' : 0,
                                                'GHI_CO_NGUYEN_TE' : 0,
                                                'DON_GIA' : don_gia_lap_rap_thao_do,
                                            })
                        else:
                            so_cai_search_lap_rap_thao_do.write({'GHI_NO' : 0,
                                                'GHI_NO_NGUYEN_TE' : 0,
                                                'GHI_CO' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                                                'GHI_CO_NGUYEN_TE' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                                                'DON_GIA' : don_gia_lap_rap_thao_do,
                                            })

                # update sổ kho
                so_kho_search_ids = self.env['so.kho.chi.tiet'].search([('CHI_TIET_ID','=', key_lap_rap_cha),('CHI_TIET_MODEL','=', 'stock.ex.nhap.xuat.kho.chi.tiet')])
                if so_kho_search_ids:
                    for so_kho_search in so_kho_search_ids:
                        if so_kho_search.LA_NHAP_KHO == True:
                            so_kho_search.write({'SO_TIEN_NHAP' : don_gia_lap_rap_thao_do*so_kho_search.SO_LUONG_NHAP,
                                                'SO_TIEN_XUAT' : 0,
                                                'DON_GIA' : don_gia_lap_rap_thao_do,
                                                'DON_GIA_THEO_DVT_CHINH' : don_gia_lap_rap_thao_do,
                                            })
                        else:
                            so_kho_search.write({'SO_TIEN_NHAP' : 0,
                                                'SO_TIEN_XUAT' : don_gia_lap_rap_thao_do*so_kho_search.SO_LUONG_XUAT,
                                                'DON_GIA' : don_gia_lap_rap_thao_do,
                                                'DON_GIA_THEO_DVT_CHINH' : don_gia_lap_rap_thao_do,
                                            })
            
            
            

                        
        #---------------------------------Kết thúc lắp ráp tháo dỡ --------------------------------------------

        if chi_tinh_lap_rap_thao_do:
            return #khong can tinh tiep luon
        
        for so_kho_sql in so_kho_sql_ids:
            # if so_kho_sql.get('KHONG_CAP_NHAT_GIA_XUAT') == False:
            # cap nhat nhung dieu kien sau:
            # + xuat kho
            # + 2013: nhap hang tra lai
            # + Có cập nhật giá xuất
            if (so_kho_sql.get('SO_LUONG_XUAT_THEO_DVT_CHINH') > 0 or so_kho_sql.get('LOAI_CHUNG_TU') == '2013')  and so_kho_sql.get('KHONG_CAP_NHAT_GIA_XUAT') == False:
                # if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
                key_so_kho = str(so_kho_sql.get('MA_HANG_ID')) + ',' + str(so_kho_sql.get('KHO_ID'))
                # else:
                #     key_so_kho = str(so_kho_sql.get('MA_HANG_ID'))
                # if key_so_kho in dict_gia_tri:
                #     for gia_tri_so_kho in dict_gia_tri[key_so_kho]:
                #         don_gia = 0
                #         so_luong = gia_tri_so_kho.get('TONG_SL_NHAP')

                if key_so_kho in dict_gia_von:
                    don_gia = 0
                    tien_von = 0
                    so_luong = 0
                    don_gia_trong_dict = float_round(dict_gia_von[key_so_kho],phan_thap_phan_don_gia)
                    # cap nhat tat
                    # if don_gia_trong_dict > 0:
                    don_gia = don_gia_trong_dict

                    # if key_so_kho in dict_gia_tri:
                    #     for gia_tri_so_kho in dict_gia_tri[key_so_kho]:
                    #         so_luong = gia_tri_so_kho.get('TONG_SL_NHAP')
                    
                    # #cap nhat them gia tri va so luong chuyen kho
                    # if key_so_kho in dict_so_kho_chuyen_kho:
                    #     for chuyen_kho in dict_so_kho_chuyen_kho[key_so_kho]:
                    #         so_luong += chuyen_kho.get('SO_LUONG_NHAP_THEO_DVT_CHINH')
                    #         tien_von += chuyen_kho.get('SO_TIEN_NHAP')

                    #  #cap nhat tra lai hang ban
                    # if key_so_kho in dict_hang_ban_tra_lai:
                    #     for tra_lai in dict_hang_ban_tra_lai[key_so_kho]:
                    #         so_luong += tra_lai.get('SO_LUONG_NHAP_THEO_DVT_CHINH')
                    #         tien_von += tra_lai.get('SO_TIEN_NHAP')
                    
                    # if so_luong > 0:
                    #     don_gia = float_round(tien_von/so_luong,0)

                    # if key_so_kho not in dict_gia_von_tra_lai_hb:
                    #     dict_gia_von_tra_lai_hb[key_so_kho] = []
                    # dict_gia_von_tra_lai_hb[key_so_kho] += [{'TIEN_VON' : tien_von, 'SO_LUONG' : so_luong,'DON_GIA_VON' : don_gia}]

                    # update sổ cái
                    so_cai_search_ids = self.env['so.cai.chi.tiet'].search([('CHI_TIET_ID','=', so_kho_sql.get('CHI_TIET_ID')),('CHI_TIET_MODEL','=', so_kho_sql.get('CHI_TIET_MODEL'))])
                    if so_cai_search_ids:
                        for so_cai_search in so_cai_search_ids:
                            if so_cai_search.LOAI_HACH_TOAN == '1':
                                so_cai_search.write({'GHI_NO' : float_round(don_gia*so_cai_search.SO_LUONG,phan_thap_phan_don_gia),
                                                    'GHI_NO_NGUYEN_TE' : float_round(don_gia*so_cai_search.SO_LUONG,phan_thap_phan_don_gia),
                                                    'GHI_CO' : 0,
                                                    'GHI_CO_NGUYEN_TE' : 0,
                                                    'DON_GIA' : don_gia,
                                                })
                            else:
                                so_cai_search.write({'GHI_NO' : 0,
                                                    'GHI_NO_NGUYEN_TE' : 0,
                                                    'GHI_CO' : float_round(don_gia*so_cai_search.SO_LUONG,phan_thap_phan_don_gia),
                                                    'GHI_CO_NGUYEN_TE' : float_round(don_gia*so_cai_search.SO_LUONG,phan_thap_phan_don_gia),
                                                    'DON_GIA' : don_gia,
                                                })

                        

                        # # update sổ công nợ
                        # so_cong_no_search_ids = self.env['so.cong.no.chi.tiet'].search([('CHI_TIET_ID','=', so_kho_sql.get('CHI_TIET_ID')),('CHI_TIET_MODEL','=', so_kho_sql.get('CHI_TIET_MODEL'))])
                        # if so_cong_no_search_ids:
                        #     for so_cong_no_search in so_cong_no_search_ids:
                        #         if so_cong_no_search.LOAI_HACH_TOAN == '1':
                        #             so_cong_no_search.write({'GHI_NO' : don_gia*so_cong_no_search.SO_LUONG,
                        #                                 'GHI_NO_NGUYEN_TE' : don_gia*so_cong_no_search.SO_LUONG,
                        #                                 'GHI_CO' : 0,
                        #                                 'GHI_CO_NGUYEN_TE' : 0,
                        #                                 'DON_GIA' : don_gia,
                        #                             })
                        #         else:
                        #             so_cong_no_search.write({'GHI_NO' : 0,
                        #                                 'GHI_NO_NGUYEN_TE' : 0,
                        #                                 'GHI_CO' : don_gia*so_cong_no_search.SO_LUONG,
                        #                                 'GHI_CO_NGUYEN_TE' : don_gia*so_cong_no_search.SO_LUONG,
                        #                                 'DON_GIA' : don_gia,
                        #                             })

                    # update sổ kho
                    so_kho_search_ids = self.env['so.kho.chi.tiet'].search([('CHI_TIET_ID','=', so_kho_sql.get('CHI_TIET_ID')),('CHI_TIET_MODEL','=', so_kho_sql.get('CHI_TIET_MODEL'))])
                    if so_kho_search_ids:
                        for so_kho_search in so_kho_search_ids:
                            if so_kho_search.LA_NHAP_KHO == True:
                                so_kho_search.write({'SO_TIEN_NHAP' : float_round(don_gia*so_kho_search.SO_LUONG_NHAP,phan_thap_phan_don_gia),
                                                    'SO_TIEN_XUAT' : 0,
                                                    'DON_GIA' : don_gia,
                                                    'DON_GIA_THEO_DVT_CHINH' : don_gia,
                                                })
                            else:
                                so_kho_search.write({'SO_TIEN_NHAP' : 0,
                                                    'SO_TIEN_XUAT' : float_round(don_gia*so_kho_search.SO_LUONG_XUAT,phan_thap_phan_don_gia),
                                                    'DON_GIA' : don_gia,
                                                    'DON_GIA_THEO_DVT_CHINH' : don_gia,
                                                })

                    # update nhập xuất kho chi tiết
                    nhap_xuat_kho_chi_tiet_ids = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].search([('id', '=', so_kho_sql.get('CHI_TIET_ID'))])
                    if nhap_xuat_kho_chi_tiet_ids:
                        for nhap_xuat in nhap_xuat_kho_chi_tiet_ids:
                            nhap_xuat.write({'TIEN_VON_QUY_DOI' : float_round(don_gia*nhap_xuat.SO_LUONG,phan_thap_phan_don_gia),'TIEN_VON' : don_gia*nhap_xuat.SO_LUONG,'DON_GIA_VON' : don_gia,'DA_TINH_GIA_XUAT_KHO' : True})

                            # update chứng từ bán hàng qua trường liên kết ở nhập xuất kho chi tiết
                            # check đúng sai qua câu sql này
                            # SELECT line."DON_GIA_VON",DT."DON_GIA_VON",* FROM sale_document_line line
                            # INNER JOIN sale_ex_document_outward_detail_ref ref ON  line.id = ref.sale_document_line_id
                            # INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet DT ON ref.stock_ex_nhap_xuat_kho_chi_tiet_id = DT.id
                            # WHERE coalesce(line."DON_GIA_VON",0) <> coalesce(DT."DON_GIA_VON",0)

                            if nhap_xuat[0].SALE_DOCUMENT_LINE_IDS:
                                for ct_ban_hang_tu_nhap_xuat_kho in nhap_xuat[0].SALE_DOCUMENT_LINE_IDS:
                                    ct_ban_hang_tu_nhap_xuat_kho.write({'TIEN_VON' : float_round(don_gia*ct_ban_hang_tu_nhap_xuat_kho.SO_LUONG,phan_thap_phan_don_gia),
                                                                                        'DON_GIA_VON' : don_gia,
                                                                                    })
                            # update chứng từ trả lại hàng bán qua trường liên kết ở nhập xuất kho chi tiết
                            if nhap_xuat[0].TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                                for ct_tra_lai_hang_ban_tu_so_kho in nhap_xuat[0].SALE_DOCUMENT_LINE_IDS:
                                    ct_tra_lai_hang_ban_tu_so_kho.write({'TIEN_VON' : float_round(don_gia*ct_tra_lai_hang_ban_tu_so_kho.SO_LUONG,phan_thap_phan_don_gia),
                                                                'DON_GIA_VON' : don_gia,
                                                            })
                    # update nhập xuất kho master
                    nhap_xuat_kho_tu_so_kho_ids = self.env['stock.ex.nhap.xuat.kho'].search([('id', '=', so_kho_sql.get('ID_CHUNG_TU'))])
                    if nhap_xuat_kho_tu_so_kho_ids:
                        for nhap_xuat_kho_tu_so_kho in nhap_xuat_kho_tu_so_kho_ids:
                            if nhap_xuat_kho_tu_so_kho.CHI_TIET_IDS:
                                tong_tien_tu_so_kho = 0
                                for chi_tiet_tinh_tong_tu_so_kho in nhap_xuat_kho_tu_so_kho.CHI_TIET_IDS:
                                    tong_tien_tu_so_kho += chi_tiet_tinh_tong_tu_so_kho.TIEN_VON
                                nhap_xuat_kho_tu_so_kho.write({'TONG_TIEN' : tong_tien_tu_so_kho})
        # # update trả lại hàng bán
        # tra_lai_hang_ban_ids = self.function_chung(tu_ngay,den_ngay,'tra_lai_hang_ban')
        # if tra_lai_hang_ban_ids:
        #     for tra_lai_hang_ban in tra_lai_hang_ban_ids:
        #         key_tra_lai_hang_ban_join = str(tra_lai_hang_ban.get('NHAP_XUAT_KHO_CHI_TIET_ID')) + ',' + str(tra_lai_hang_ban.get('MODEL_NHAP_XUAT_KHO_CHI_TIET'))
        #         if key_tra_lai_hang_ban_join in dict_so_kho:
        #             if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
        #                 key_so_tra_lai_hb = str(tra_lai_hang_ban.get('MA_HANG_ID')) + ',' + str(tra_lai_hang_ban.get('MA_KHO_ID'))
        #             else:
        #                 key_so_tra_lai_hb = str(tra_lai_hang_ban.get('MA_HANG_ID'))
                    
        #             if key_so_tra_lai_hb in dict_gia_von_tra_lai_hb:
        #                 for tra_lai_tu_kho in dict_gia_von_tra_lai_hb[key_so_tra_lai_hb]:
        #                     don_gia_tra_lai_hang_ban = tra_lai_tu_kho.get('DON_GIA_VON')
        #             # update sổ cái
        #             so_cai_search_hang_ban_tra_lai_ids = self.env['so.cai.chi.tiet'].search([('CHI_TIET_ID','=', tra_lai_hang_ban.get('NHAP_XUAT_KHO_CHI_TIET_ID')),('CHI_TIET_MODEL','=', tra_lai_hang_ban.get('MODEL_NHAP_XUAT_KHO_CHI_TIET'))])
        #             if so_cai_search_hang_ban_tra_lai_ids:
        #                 for so_cai_tu_hang_ban_tra_lai in so_cai_search_hang_ban_tra_lai_ids:
        #                     if so_cai_tu_hang_ban_tra_lai.LOAI_HACH_TOAN == '1':
        #                         so_cai_tu_hang_ban_tra_lai.write({'GHI_NO' : don_gia_tra_lai_hang_ban*so_cai_tu_hang_ban_tra_lai.SO_LUONG,
        #                                             'GHI_NO_NGUYEN_TE' : don_gia_tra_lai_hang_ban*so_cai_tu_hang_ban_tra_lai.SO_LUONG,
        #                                             'GHI_CO' : 0,
        #                                             'GHI_CO_NGUYEN_TE' : 0,
        #                                             'DON_GIA' : don_gia_tra_lai_hang_ban,
        #                                         })
        #                     else:
        #                         so_cai_tu_hang_ban_tra_lai.write({'GHI_NO' : 0,
        #                                             'GHI_NO_NGUYEN_TE' : 0,
        #                                             'GHI_CO' : don_gia_tra_lai_hang_ban*so_cai_tu_hang_ban_tra_lai.SO_LUONG,
        #                                             'GHI_CO_NGUYEN_TE' : don_gia_tra_lai_hang_ban*so_cai_tu_hang_ban_tra_lai.SO_LUONG,
        #                                             'DON_GIA' : don_gia_tra_lai_hang_ban,
        #                                         })
        #                 # update sổ công nợ
        #                 so_cong_no_search_hang_ban_tra_lai_ids = self.env['so.cong.no.chi.tiet'].search([('CHI_TIET_ID','=', tra_lai_hang_ban.get('NHAP_XUAT_KHO_CHI_TIET_ID')),('CHI_TIET_MODEL','=', tra_lai_hang_ban.get('MODEL_NHAP_XUAT_KHO_CHI_TIET'))])
        #                 if so_cong_no_search_hang_ban_tra_lai_ids:
        #                     for so_cong_no_search_hang_ban_tra_lai in so_cong_no_search_hang_ban_tra_lai_ids:
        #                         if so_cong_no_search_hang_ban_tra_lai.LOAI_HACH_TOAN == '1':
        #                             so_cong_no_search_hang_ban_tra_lai.write({'GHI_NO' : don_gia_tra_lai_hang_ban*so_cong_no_search_hang_ban_tra_lai.SO_LUONG,
        #                                                 'GHI_NO_NGUYEN_TE' : don_gia_tra_lai_hang_ban*so_cong_no_search_hang_ban_tra_lai.SO_LUONG,
        #                                                 'GHI_CO' : 0,
        #                                                 'GHI_CO_NGUYEN_TE' : 0,
        #                                                 'DON_GIA' : don_gia_tra_lai_hang_ban,
        #                                             })
        #                         else:
        #                             so_cong_no_search_hang_ban_tra_lai.write({'GHI_NO' : 0,
        #                                                 'GHI_NO_NGUYEN_TE' : 0,
        #                                                 'GHI_CO' : don_gia_tra_lai_hang_ban*so_cong_no_search_hang_ban_tra_lai.SO_LUONG,
        #                                                 'GHI_CO_NGUYEN_TE' : don_gia_tra_lai_hang_ban*so_cong_no_search_hang_ban_tra_lai.SO_LUONG,
        #                                                 'DON_GIA' : don_gia_tra_lai_hang_ban,
        #                                             })
        #                 # update sổ kho
        #                 so_kho_search_hang_ban_tra_lai_ids = self.env['so.kho.chi.tiet'].search([('CHI_TIET_ID','=', tra_lai_hang_ban.get('NHAP_XUAT_KHO_CHI_TIET_ID')),('CHI_TIET_MODEL','=', tra_lai_hang_ban.get('MODEL_NHAP_XUAT_KHO_CHI_TIET'))])
        #                 if so_kho_search_hang_ban_tra_lai_ids:
        #                     for so_kho_search_hang_ban_tra_lai in so_kho_search_hang_ban_tra_lai_ids:
        #                         if so_kho_search_hang_ban_tra_lai.LOAI_KHU_VUC_NHAP_XUAT == '1' or (so_kho_search_hang_ban_tra_lai.LOAI_KHU_VUC_NHAP_XUAT == '1' and so_kho_search_hang_ban_tra_lai.SO_LUONG_XUAT_THEO_DVT_CHINH == 0):
        #                             so_kho_search_hang_ban_tra_lai.write({'GIA_VON' : don_gia_tra_lai_hang_ban,
        #                                                 'SO_TIEN_NHAP' : don_gia_tra_lai_hang_ban*so_kho_search_hang_ban_tra_lai.SO_LUONG_XUAT,
        #                                                 'DON_GIA_THEO_DVT_CHINH' : don_gia_tra_lai_hang_ban,
        #                                             })

        #                 # câu này search theo id nên chỉ có 1 dòng
        #                 nhap_xuat_kho_hang_ban_tra_lai_ids = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].search([('id', '=', tra_lai_hang_ban.get('NHAP_XUAT_KHO_CHI_TIET_ID'))])
        #                 if nhap_xuat_kho_hang_ban_tra_lai_ids:
        #                     for nhap_xuat_kho_hang_ban_tra_lai in nhap_xuat_kho_hang_ban_tra_lai_ids:
        #                         nhap_xuat_kho_hang_ban_tra_lai.write({'TIEN_VON' : don_gia_tra_lai_hang_ban*nhap_xuat_kho_hang_ban_tra_lai.SO_LUONG,
        #                                                             'TIEN_VON_QUY_DOI' : don_gia_tra_lai_hang_ban*nhap_xuat_kho_hang_ban_tra_lai.SO_LUONG,
        #                                                             'DON_GIA_VON' : don_gia_tra_lai_hang_ban,
        #                                                             'DA_TINH_GIA_XUAT_KHO' : True,
        #                                                         })
        #                         # update chứng từ bán hàng qua trường liên kết ở nhập xuất kho chi tiết
        #                         if nhap_xuat_kho_hang_ban_tra_lai.SALE_DOCUMENT_LINE_IDS:
        #                             for ct_ban_hang_tu_nhap_xuat_kho_tra_lai_hang_ban in nhap_xuat_kho_hang_ban_tra_lai.SALE_DOCUMENT_LINE_IDS:
        #                                 ct_ban_hang_tu_nhap_xuat_kho_tra_lai_hang_ban.write({'TIEN_VON' : don_gia_tra_lai_hang_ban*ct_ban_hang_tu_nhap_xuat_kho_tra_lai_hang_ban.SO_LUONG,
        #                                                                                     'DON_GIA_VON' : don_gia_tra_lai_hang_ban,
        #                                                                                 })
        #                         # update chứng từ trả lại hàng bán qua trường liên kết ở nhập xuất kho chi tiết
        #                         if nhap_xuat_kho_hang_ban_tra_lai.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
        #                             for ct_tra_lai_hang_ban in nhap_xuat_kho_hang_ban_tra_lai.SALE_DOCUMENT_LINE_IDS:
        #                                 ct_tra_lai_hang_ban.write({'TIEN_VON' : don_gia_tra_lai_hang_ban*ct_tra_lai_hang_ban.SO_LUONG,
        #                                                             'DON_GIA_VON' : don_gia_tra_lai_hang_ban,
        #                                                         })

        #                 # update nhập xuất kho master
        #                 nhap_xuat_kho_tu_tra_lai_hang_ban_ids = self.env['stock.ex.nhap.xuat.kho'].search([('id', '=', so_kho_sql.get('ID_CHUNG_TU'))])
        #                 if nhap_xuat_kho_tu_tra_lai_hang_ban_ids:
        #                     for nhap_xuat_kho_tu_tra_lai_hang_ban in nhap_xuat_kho_tu_tra_lai_hang_ban_ids:
        #                         if nhap_xuat_kho_tu_tra_lai_hang_ban.CHI_TIET_IDS:
        #                             tong_tien_tu_tra_lai_hang_ban = 0
        #                             for chi_tiet_tinh_tong_tu_tra_lai_hang_ban in nhap_xuat_kho_tu_tra_lai_hang_ban.CHI_TIET_IDS:
        #                                 tong_tien_tu_tra_lai_hang_ban += chi_tiet_tinh_tong_tu_tra_lai_hang_ban.TIEN_VON
        #                             nhap_xuat_kho_tu_tra_lai_hang_ban.write({'TONG_TIEN' : tong_tien_tu_tra_lai_hang_ban})
                        
        # update từ bảng lắp ráp tháo dỡ
        # lap_rap_thao_do_ids = self.function_chung(tu_ngay,den_ngay,'lap_rap_thao_do')
        # if lap_rap_thao_do_ids:
        #     for lap_rap_thao_do in lap_rap_thao_do_ids:
        #         # Láy giá trị từ dict lưu giá trị tính giá xuất kho ở trên
        #         key_lap_rap_thao_do = str(lap_rap_thao_do.get('MA_HANG_ID')) + ',' + str(lap_rap_thao_do.get('MA_KHO_ID'))
        #         if key_lap_rap_thao_do in dict_gia_tri:
        #             don_gia_lap_rap_thao_do = 0
        #             so_luong_lap_rap_thao_do = dict_gia_tri[key_lap_rap_thao_do].get('TONG_SL_NHAP')
        #             tien_von_lap_rap_thao_do = dict_gia_tri[key_lap_rap_thao_do].get('TONG_GIA_TRI_NHAP')
        #             if so_luong_lap_rap_thao_do > 0:
        #                 don_gia_lap_rap_thao_do = float_round(tien_von_lap_rap_thao_do/so_luong_lap_rap_thao_do,0)

        #         # update nhập xuất kho master
        #         nhap_xuat_kho_tu_lap_rap_thao_do_ids = self.env['stock.ex.nhap.xuat.kho'].search([('id', '=', so_kho_sql.get('ID_CHUNG_TU'))])
        #         if nhap_xuat_kho_tu_lap_rap_thao_do_ids:
        #             for nhap_xuat_kho_tu_lap_rap_thao_do in nhap_xuat_kho_tu_lap_rap_thao_do_ids:
        #                 if nhap_xuat_kho_tu_lap_rap_thao_do.CHI_TIET_IDS:
        #                     tong_tien_tu_lap_rap_thao_do = 0
        #                     for chi_tiet_tinh_tong_tu_lap_rap_thao_do in nhap_xuat_kho_tu_lap_rap_thao_do.CHI_TIET_IDS:
        #                         tong_tien_tu_lap_rap_thao_do += chi_tiet_tinh_tong_tu_lap_rap_thao_do.TIEN_VON
        #                     nhap_xuat_kho_tu_lap_rap_thao_do.write({'TONG_TIEN' : tong_tien_tu_lap_rap_thao_do})
                # # update sổ cái
                # so_cai_search_lap_rap_thao_do_ids = self.env['so.cai.chi.tiet'].search([('CHI_TIET_ID','=', lap_rap_thao_do.get('CHI_TIET_ID')),('CHI_TIET_MODEL','=', lap_rap_thao_do.get('CHI_TIET_MODEL'))])
                # if so_cai_search_lap_rap_thao_do_ids:
                #     for so_cai_search_lap_rap_thao_do in so_cai_search_lap_rap_thao_do_ids:
                #         if so_cai_search_lap_rap_thao_do.LOAI_HACH_TOAN == '1':
                #             so_cai_search_lap_rap_thao_do.write({'GHI_NO' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                #                                 'GHI_NO_NGUYEN_TE' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                #                                 'GHI_CO' : 0,
                #                                 'GHI_CO_NGUYEN_TE' : 0,
                #                                 'DON_GIA' : don_gia_lap_rap_thao_do,
                #                             })
                #         else:
                #             so_cai_search_lap_rap_thao_do.write({'GHI_NO' : 0,
                #                                 'GHI_NO_NGUYEN_TE' : 0,
                #                                 'GHI_CO' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                #                                 'GHI_CO_NGUYEN_TE' : don_gia_lap_rap_thao_do*so_cai_search_lap_rap_thao_do.SO_LUONG,
                #                                 'DON_GIA' : don_gia_lap_rap_thao_do,
                #                             })

                # # update sổ công nợ
                # so_cong_no_search_lap_rap_thao_do_ids = self.env['so.cong.no.chi.tiet'].search([('CHI_TIET_ID','=', lap_rap_thao_do.get('CHI_TIET_ID')),('CHI_TIET_MODEL','=', lap_rap_thao_do.get('CHI_TIET_MODEL'))])
                # if so_cong_no_search_lap_rap_thao_do_ids:
                #     for so_cong_no_search_lap_rap_thao_do in so_cong_no_search_lap_rap_thao_do_ids:
                #         if so_cong_no_search_lap_rap_thao_do.LOAI_HACH_TOAN == '1':
                #             so_cong_no_search_lap_rap_thao_do.write({'GHI_NO' : don_gia_lap_rap_thao_do*so_cong_no_search_lap_rap_thao_do.SO_LUONG,
                #                                 'GHI_NO_NGUYEN_TE' : don_gia_lap_rap_thao_do*so_cong_no_search_lap_rap_thao_do.SO_LUONG,
                #                                 'GHI_CO' : 0,
                #                                 'GHI_CO_NGUYEN_TE' : 0,
                #                                 'DON_GIA' : don_gia_lap_rap_thao_do,
                #                             })
                #         else:
                #             so_cong_no_search_lap_rap_thao_do.write({'GHI_NO' : 0,
                #                                 'GHI_NO_NGUYEN_TE' : 0,
                #                                 'GHI_CO' : don_gia_lap_rap_thao_do*so_cong_no_search_lap_rap_thao_do.SO_LUONG,
                #                                 'GHI_CO_NGUYEN_TE' : don_gia_lap_rap_thao_do*so_cong_no_search_lap_rap_thao_do.SO_LUONG,
                #                                 'DON_GIA' : don_gia_lap_rap_thao_do,
                #                             })
                # # Cập nhật nhập xuất kho chi tiết
                # nhap_xuat_kho_lap_rap_thao_do_ids = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].search([('id', '=', lap_rap_thao_do.get('CHI_TIET_ID'))],limit=1)
                # if nhap_xuat_kho_lap_rap_thao_do_ids:
                #     for nhap_xuat_kho_lap_rap_thao_do in nhap_xuat_kho_lap_rap_thao_do_ids:
                #         nhap_xuat_kho_lap_rap_thao_do.write({'TIEN_VON' : don_gia_lap_rap_thao_do*nhap_xuat_kho_lap_rap_thao_do.SO_LUONG,
                #                                             'TIEN_VON_QUY_DOI' : don_gia_lap_rap_thao_do*nhap_xuat_kho_lap_rap_thao_do.SO_LUONG,
                #                                             'DON_GIA_VON' : don_gia_lap_rap_thao_do,
                #                                             'DA_TINH_GIA_XUAT_KHO' : True,
                #                                         })
                #         # update chứng từ bán hàng qua trường liên kết ở nhập xuất kho chi tiết
                #         if nhap_xuat_kho_lap_rap_thao_do.SALE_DOCUMENT_LINE_IDS:
                #             for ct_ban_hang_tu_lap_rap_thao_do in nhap_xuat_kho_lap_rap_thao_do.SALE_DOCUMENT_LINE_IDS:
                #                 ct_ban_hang_tu_lap_rap_thao_do.write({'TIEN_VON' : don_gia_lap_rap_thao_do*ct_ban_hang_tu_lap_rap_thao_do.SO_LUONG,
                #                                                         'DON_GIA_VON' : don_gia_lap_rap_thao_do,
                #                                                                 })
                #         # update chứng từ trả lại hàng bán qua trường liên kết ở nhập xuất kho chi tiết
                #         if nhap_xuat_kho_lap_rap_thao_do.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                #             for ct_tra_lai_hang_ban_tu_lap_rap_thao_do in nhap_xuat_kho_lap_rap_thao_do.SALE_DOCUMENT_LINE_IDS:
                #                 ct_tra_lai_hang_ban_tu_lap_rap_thao_do.write({'TIEN_VON' : don_gia_lap_rap_thao_do*ct_tra_lai_hang_ban_tu_lap_rap_thao_do.SO_LUONG,
                #                                             'DON_GIA_VON' : don_gia_lap_rap_thao_do,
                #                                     })
        

                
    def function_chung(self,tu_ngay,den_ngay,bang,list_vthh):
        # list_chi_nhanh = ';17;19;16;18;21;20;'
        list_chi_nhanh = ';'
        chi_nhanh_ids = self.env['danh.muc.to.chuc'].search([('CAP_TO_CHUC', 'in', ('1','2'))])
        if chi_nhanh_ids:
            for chi_nhanh in chi_nhanh_ids:
                list_chi_nhanh += str(chi_nhanh.id)
                list_chi_nhanh += ';'
        
        # list_vthh = None
        # if self.LIST_VTHH:
        #     list_vthh = self.LIST_VTHH

        if self.TINH_GIA_SELECTION == 'TINH_THEO_KHO':
            tinh_gia_theo_kho = 1
        else:
            tinh_gia_theo_kho = 0

        params = {
            'TU_NGAY' : tu_ngay,
            'DEN_NGAY' : den_ngay,
            'LIST_CHI_NHANH' : list_chi_nhanh,
            'TINH_GIA_THEO_KHO' : tinh_gia_theo_kho,
            'LIST_VTHH' : list_vthh,
            }
        # bảng sổ kho
        if bang == 'so_kho':
            query_dieu_kien = """    
                    SELECT
                    CASE WHEN "PHEP_TINH_CHUYEN_DOI" = 'NHAN'
                        THEN '*'
                            WHEN "PHEP_TINH_CHUYEN_DOI" ='CHIA'
                                THEN
                                '/'
                        ELSE '0'
                                    END
                        AS "PHEP_TINH_CHUYEN_DOI1"

                    ,* FROM TMP_SO_KHO_CHI_TIET_KQ
                --WHERE "MA_HANG_ID" in (113, 104, 136)
                --WHERE "MA_HANG_ID" in (122)
                --    WHERE "CHI_TIET_ID" = 1877
                """
        # bảng lấy giá trị để tính giá xuất kho
        elif bang == 'gia_tri_update':
            query_dieu_kien = """    
                     SELECT* FROM TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO_KQ 
                     --WHERE "MA_HANG_ID" in (113, 104, 136)
                     --WHERE "MA_HANG_ID" in (122)
                """
        # bảng các chứng từ trả lại hàng bán
        elif bang == 'tra_lai_hang_ban':
            query_dieu_kien = """    
                    SELECT
                    CASE WHEN "PHEP_TINH_CHUYEN_DOI" = '0'
                            THEN '*'
                            WHEN "PHEP_TINH_CHUYEN_DOI" = '1'
                                THEN '/'
                                    ELSE
                                        '0'
                                            END AS "PHEP_TINH_CHUYEN_DOI_1" ,
                    'stock.ex.nhap.xuat.kho.chi.tiet' AS "MODEL_NHAP_XUAT_KHO_CHI_TIET",
                    * FROM LAY_DU_LIEU_CHO_BANG_HANG_BAN_TRA_LAI
                   -- WHERE "NHAP_XUAT_KHO_CHI_TIET_ID" = 2228
                """
        # bảng các chứng từ lắp ráp tháo dỡ
        elif bang == 'lap_rap_thao_do':
            query_dieu_kien = """    
                     SELECT* FROM LAY_DU_LIEU_CHO_BANG_LAP_RAP
                    -- WHERE "CHI_TIET_ID" = 2271
                """
        
        # bảng các chứng từ chuyen kho
        elif bang == 'chuyen_kho':
            query_dieu_kien = """    
                     SELECT* FROM LAY_DU_LIEU_CHO_BANG_CHUYEN_KHO
                    -- WHERE "CHI_TIET_ID" = 2271
                """

        query = """   


            DO LANGUAGE plpgsql $$
            DECLARE
                v_tu_ngay                        DATE := %(TU_NGAY)s;

                --%%(TU_NGAY)s

                v_den_ngay                       DATE := %(DEN_NGAY)s;

                --%%(DEN_NGAY)s


                v_chi_nhanh_id                   VARCHAR(500) := %(LIST_CHI_NHANH)s;


                rec                              RECORD;

                rec_2                            RECORD;


                ngan_cach_giua_cac_danh_sach     VARCHAR(100) = N';';

                danh_sach_vthh_ids               VARCHAR(100) := %(LIST_VTHH)s;

                IsCaculateByStock                INTEGER := %(TINH_GIA_THEO_KHO)s;

                MA_HANG_ID_TMP                   INTEGER;

                MA_KHO_ID_TMP                    INTEGER;

                SO_LUONG_TON_DAU_KY_TMP          FLOAT;

                GIA_TRI_TON_DAU_KY_TMP           FLOAT;

                SO_LUONG_NHAP_TRONG_KY_TMP       FLOAT;

                GIA_TRI_NHAP_TRONG_KY_TMP        FLOAT;

                SL_CHUNG_TU_KO_CAP_NHAT_TMP      FLOAT;

                GIA_TRI_CHUNG_TU_KO_CAP_NHAT_TMP FLOAT;

                SO_LUONG_CHUYEN_KHO_TRONG_KY_TMP FLOAT;


            BEGIN


                DROP TABLE IF EXISTS TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO
                ;
                DROP SEQUENCE IF EXISTS TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO_seq
                ;

                CREATE TEMP SEQUENCE TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO_seq
                ;

                CREATE TEMP TABLE TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO
                (
                    RowNum             INT   DEFAULT NEXTVAL('TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO_seq')
                        PRIMARY KEY,
                    "MA_HANG_ID"        INT,
                    "MA_KHO_ID"         INT,
                    "SO_LUONG_TON"      DECIMAL(22, 8),
                    "GIA_TRI_TON"       DECIMAL(18, 4),
                    "DON_GIA_XUAT_KHO"  DECIMAL(18, 4),
                    "TONG_SL_NHAP"      DECIMAL(22, 8),
                    "TONG_GIA_TRI_NHAP" DECIMAL(18, 4),
                    "TINH_TRANG"        INT
                )
                ;

                -- Bảng danh sách các kho chuyển đi và chuyển đến theo Vật tư
                DROP TABLE IF EXISTS TMP_DS_CAC_KHO_CHUYEN_DI_VA_CHUYEN_DEN_THEO_VAT_TU
                ;

                CREATE TEMP TABLE TMP_DS_CAC_KHO_CHUYEN_DI_VA_CHUYEN_DEN_THEO_VAT_TU
                (
                    "MA_HANG_ID"      INT,
                    "XUAT_TAI_KHO_ID" INT,
                    "NHAP_TAI_KHO_ID" INT,
                    "TONG_SL"         DECIMAL(22, 8),
                    "TONG_GIA_TRI"    DECIMAL(18, 4)
                )
                ;

                INSERT INTO TMP_DS_CAC_KHO_CHUYEN_DI_VA_CHUYEN_DEN_THEO_VAT_TU
                (
                    "MA_HANG_ID",
                    "XUAT_TAI_KHO_ID",
                    "NHAP_TAI_KHO_ID",
                    "TONG_SL",
                    "TONG_GIA_TRI"
                )
                    SELECT
                        INTD."MA_HANG_ID"
                        , INTD."XUAT_TAI_KHO_ID"
                        , INTD."NHAP_TAI_KHO_ID"
                        , COALESCE(SUM(INTD."SO_LUONG_THEO_DVT_CHINH"), 0) AS "TONG_SL"
                        , 0                                           AS "TONG_GIA_TRI"
                    FROM stock_ex_nhap_xuat_kho AS INTF
                        INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS INTD ON (INTF."id" = INTD."NHAP_XUAT_ID")
                        INNER JOIN danh_muc_vat_tu_hang_hoa II ON INTD."MA_HANG_ID" = II."id" AND ii."TINH_CHAT" IN
                                                                                                ('0', '1') -- không lấy vật tư chỉ là diễn giải và dịch vụ --> chi lấy thành phẩm và thành phẩm
                    WHERE INTF."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
                        AND
                        INTF."state" = 'da_ghi_so'

                        AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                || CAST(INTF."CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach ||
                                                '%%'
                        AND (danh_sach_vthh_ids IS NULL
                            OR danh_sach_vthh_ids LIKE '%%'
                                                        || CAST(INTD."MA_HANG_ID" AS VARCHAR(50)) || '%%'
                        )
                    GROUP BY
                        INTD."MA_HANG_ID",
                        INTD."XUAT_TAI_KHO_ID",
                        INTD."NHAP_TAI_KHO_ID"
                ;

                -- Lấy ra danh sách VT || Kho có phát sinh (Chỉ lấy theo chứng từ Xuất, Với chứng từ chuyển kho thì lấy ra theo Ko đi- Tức là kho xuất)
                --====================== TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO =============================================================
                INSERT INTO TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO
                (
                    "MA_HANG_ID",
                    "MA_KHO_ID",
                    "SO_LUONG_TON",
                    "GIA_TRI_TON",
                    "DON_GIA_XUAT_KHO",
                    "TONG_SL_NHAP",
                    "TONG_GIA_TRI_NHAP",
                    "TINH_TRANG"
                )

                    SELECT
                        DISTINCT
                        IL."MA_HANG_ID"
                        , CASE WHEN IsCaculateByStock = 1
                        THEN IL."KHO_ID"
                        ELSE NULL
                        END AS "MA_KHO_ID"
                        , 0   AS "SO_LUONG_TON"
                        , 0   AS "GIA_TRI_TON"
                        , 0   AS "DON_GIA_XUAT_KHO"
                        , 0   AS "TONG_SL_NHAP"
                        , 0   AS "TONG_GIA_TRI_NHAP"
                        , 0   AS "TINH_TRANG"
                    FROM so_kho_chi_tiet IL
                        INNER JOIN danh_muc_vat_tu_hang_hoa II ON IL."MA_HANG_ID" = II."id" AND II."TINH_CHAT" IN
                                                                                                ('0', '1') -- không lấy vật tư chỉ là diễn giải và dịch vụ --> chi lấy thành phẩm và thành phẩm
                    --lấy phát sinh của xuất kho và hàng bán trả lại tùy chọn lấy đơn giá bình quân cuối kỳ
                    WHERE IL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
                        AND (IL."SO_LUONG_XUAT_THEO_DVT_CHINH" > 0
                            OR (IL."PHUONG_THUC_THANH_TOAN" = '0'
                                AND IL."LOAI_CHUNG_TU" = '2013'
                            )
                        )

                        AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                || CAST(IL."CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                        AND (danh_sach_vthh_ids IS NULL
                            OR danh_sach_vthh_ids LIKE '%%'
                                                        || CAST(IL."MA_HANG_ID" AS VARCHAR(50)) || '%%'
                        )
                ;


                FOR rec IN
                SELECT
                    "MA_HANG_ID" AS "MA_HANG_ID_TMP"
                    , "MA_KHO_ID"  AS "MA_KHO_ID_TMP"


                FROM TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO

                LOOP

                SO_LUONG_TON_DAU_KY_TMP          = 0;

                GIA_TRI_TON_DAU_KY_TMP           = 0;

                SO_LUONG_NHAP_TRONG_KY_TMP       = 0;

                GIA_TRI_NHAP_TRONG_KY_TMP        = 0;

                SL_CHUNG_TU_KO_CAP_NHAT_TMP      = 0;

                GIA_TRI_CHUNG_TU_KO_CAP_NHAT_TMP  = 0;

                SO_LUONG_CHUYEN_KHO_TRONG_KY_TMP  = 0;



                    FOR rec_2 IN
                    SELECT *
                    FROM TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO
                    WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                        AND ("MA_KHO_ID" = rec."MA_KHO_ID_TMP"
                            OR rec."MA_KHO_ID_TMP" IS NULL
                        )

                    LOOP


                        --  tồn đầu kỳ
                        SELECT COALESCE(SUM("SO_LUONG_NHAP_THEO_DVT_CHINH"), 0)
                            - COALESCE(SUM("SO_LUONG_XUAT_THEO_DVT_CHINH"), 0)
                        INTO SO_LUONG_TON_DAU_KY_TMP
                        FROM so_kho_chi_tiet
                        WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" =rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "NGAY_HACH_TOAN" < v_tu_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;


                        SELECT COALESCE(SUM("SO_TIEN_NHAP"), 0)
                            - COALESCE(SUM("SO_TIEN_XUAT"), 0)
                        INTO GIA_TRI_TON_DAU_KY_TMP
                        FROM so_kho_chi_tiet
                        WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" = rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "NGAY_HACH_TOAN" < v_tu_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;


                        -- Nhập trong kỳ không có Chuyển kho
                        SELECT COALESCE(SUM("SO_LUONG_NHAP_THEO_DVT_CHINH"), 0)
                        INTO SO_LUONG_NHAP_TRONG_KY_TMP

                        FROM so_kho_chi_tiet
                        WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" = rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                            AND ("LOAI_CHUNG_TU" <> '2013'
                                OR "PHUONG_THUC_THANH_TOAN" IS NULL
                                OR "PHUONG_THUC_THANH_TOAN" <> '0'
                            )-- Chỉ lấy chứng từ Nhập
                            AND "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;

                        SELECT COALESCE(SUM("SO_TIEN_NHAP"), 0)
                        INTO GIA_TRI_NHAP_TRONG_KY_TMP
                        FROM so_kho_chi_tiet
                        WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" = rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                            AND ("LOAI_CHUNG_TU" <> '2013'
                                OR "PHUONG_THUC_THANH_TOAN" IS NULL
                                OR "PHUONG_THUC_THANH_TOAN" <> '0'
                            )-- Chỉ lấy chứng từ Nhập
                            AND "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;

                        -- giá trị của những chứng từ xuất kho k cập nhật giá
                        SELECT COALESCE(SUM("SO_TIEN_XUAT"), 0)
                        INTO GIA_TRI_CHUNG_TU_KO_CAP_NHAT_TMP
                        FROM so_kho_chi_tiet
                        WHERE "KHONG_CAP_NHAT_GIA_XUAT" = TRUE
                            AND "LOAI_KHONG_CAP_NHAT_GIA_XUAT" IN ('1', '2')
                            AND "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" = rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;

                        --  số lượng của những chứng từ xuất kho k cập nhật giá
                        SELECT COALESCE(SUM("SO_LUONG_XUAT_THEO_DVT_CHINH"), 0)
                        INTO SL_CHUNG_TU_KO_CAP_NHAT_TMP
                        FROM so_kho_chi_tiet
                        WHERE "KHONG_CAP_NHAT_GIA_XUAT" = TRUE
                            AND "LOAI_KHONG_CAP_NHAT_GIA_XUAT" IN ('2', '3')
                            AND "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" = rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;

                        --sl chuyển kho trong kỳ
                        SELECT COALESCE(SUM("SO_LUONG_NHAP_THEO_DVT_CHINH"), 0)
                        INTO SO_LUONG_CHUYEN_KHO_TRONG_KY_TMP
                        FROM so_kho_chi_tiet
                        WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                            AND ("KHO_ID" = rec."MA_KHO_ID_TMP"
                                OR rec."MA_KHO_ID_TMP" IS NULL
                            )
                            AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'    -- Chỉ lấy chứng từ chuyển kho
                            AND "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

                            AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                                    || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                    ;


                    UPDATE TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO
                    set   "SO_LUONG_TON"      = SO_LUONG_TON_DAU_KY_TMP + SO_LUONG_NHAP_TRONG_KY_TMP
                                                                        - SL_CHUNG_TU_KO_CAP_NHAT_TMP +
                                            SO_LUONG_CHUYEN_KHO_TRONG_KY_TMP,
                        "GIA_TRI_TON"       = GIA_TRI_TON_DAU_KY_TMP + GIA_TRI_NHAP_TRONG_KY_TMP
                                                                        - GIA_TRI_CHUNG_TU_KO_CAP_NHAT_TMP,

                        "TONG_SL_NHAP"      = SO_LUONG_TON_DAU_KY_TMP + SO_LUONG_NHAP_TRONG_KY_TMP - SL_CHUNG_TU_KO_CAP_NHAT_TMP,




                        "TONG_GIA_TRI_NHAP" = GIA_TRI_TON_DAU_KY_TMP + GIA_TRI_NHAP_TRONG_KY_TMP
                                                                        - GIA_TRI_CHUNG_TU_KO_CAP_NHAT_TMP

                        WHERE "MA_HANG_ID" = rec."MA_HANG_ID_TMP"
                        AND ("MA_KHO_ID" = rec."MA_KHO_ID_TMP"
                            OR rec."MA_KHO_ID_TMP" IS NULL
                        )
                    ;


                    END LOOP
                ;






                END LOOP
                ;


                -- 	--====================== TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO =============================================================
                -- --    ------- Lấy cho so_kho_chi_tiet---------------------
                -- -- Chỉ lấy các dòng chứng từ Xuất
                --

                DROP TABLE IF  EXISTS  TMP_SO_KHO_CHI_TIET;

                    CREATE TEMP TABLE TMP_SO_KHO_CHI_TIET
                            (
                            "SO_KHO_CHI_TIET_ID" INT ,
                            "ID_CHUNG_TU" INT ,
                            "MODEL_CHUNG_TU" VARCHAR(200) ,
                            "LOAI_CHUNG_TU" VARCHAR(200) ,
                            "NGAY_HACH_TOAN" DATE ,
                            "MA_TK_NO" VARCHAR(200) ,
                            "MA_TK_CO" VARCHAR(200) ,
                            "KHO_ID" INT ,
                            "MA_HANG_ID" INT ,
                            "DON_GIA" DECIMAL(18, 4) ,
                            "DON_GIA_THEO_DVT_CHINH" DECIMAL(20, 6) NOT NULL ,
                            "TY_LE_CHUYEN_DOI" DECIMAL(18, 4) NOT NULL ,
                            "PHEP_TINH_CHUYEN_DOI" VARCHAR(200) NULL ,
                            "SO_TIEN_NHAP" DECIMAL(18, 4) ,
                            "SO_TIEN_XUAT" DECIMAL(18, 4) ,
                            "SO_LUONG_NHAP_THEO_DVT_CHINH" DECIMAL(22, 8) ,
                            "SO_LUONG_XUAT_THEO_DVT_CHINH" DECIMAL(22, 8) ,
                            "STT_LOAI_CHUNG_TU" TIMESTAMP ,
                            "CHI_TIET_ID" INT,
                            "CHI_TIET_MODEL" VARCHAR(200) ,
                            "LOAI_KHU_VUC_NHAP_XUAT" VARCHAR(200) ,
                            "KHONG_CAP_NHAT_GIA_XUAT" BOOLEAN ,
                            "LOAI_KHONG_CAP_NHAT_GIA_XUAT" VARCHAR(200) ,
                            "THU_TU_TRONG_CHUNG_TU" INT ,
                            "CHUNG_TU_LAP_RAP_THAO_DO_ID" INT ,
                            "SO_CHUNG_TU_NHAP_DOI_TRU" INT ,
                            "TEN_LOAI_TIEN" VARCHAR(200) ,
                            "TY_GIA" DECIMAL(18, 4) ,
                            "SO_CHUNG_TU" VARCHAR(200) ,
                            "NGAY_CHUNG_TU" DATE ,
                            "CHI_NHANH_ID" INT
                            ) ;
                --nnanh 25/2/2015: lấy hết thông tin trong sổ lên để tính toán chuẩn chứng từ xuất cuối cùng      (bug 41083)
                        INSERT  INTO TMP_SO_KHO_CHI_TIET
                                SELECT
                                        IL."id" ,
                                        IL."ID_CHUNG_TU" ,
                                        IL."MODEL_CHUNG_TU" ,
                                        IL."LOAI_CHUNG_TU" ,
                                        IL."NGAY_HACH_TOAN" ,
                                        IL."MA_TK_NO" ,
                                        IL."MA_TK_CO" ,
                                        IL."KHO_ID" ,
                                        IL."MA_HANG_ID" ,
                                        IL."DON_GIA" ,
                                        IL."DON_GIA_THEO_DVT_CHINH" ,
                                        IL."TY_LE_CHUYEN_DOI" ,

                                        IL."TOAN_TU_QUY_DOI" ,
                                        IL."SO_TIEN_NHAP" ,
                                        IL."SO_TIEN_XUAT" ,
                                        IL."SO_LUONG_NHAP_THEO_DVT_CHINH" ,
                                        IL."SO_LUONG_XUAT_THEO_DVT_CHINH" ,
                                        IL."STT_LOAI_CHUNG_TU" ,
                                        IL."CHI_TIET_ID" ,
                                        IL."CHI_TIET_MODEL" ,
                                        IL."LOAI_KHU_VUC_NHAP_XUAT" ,
                                        il."KHONG_CAP_NHAT_GIA_XUAT" ,
                                        il."LOAI_KHONG_CAP_NHAT_GIA_XUAT" ,
                                        IL."THU_TU_TRONG_CHUNG_TU" ,
                                        il."CHUNG_TU_LAP_RAP_THAO_DO_ID" ,
                                        il."SO_CHUNG_TU_NHAP_DOI_TRU" ,
                                        il."TEN_LOAI_TIEN" ,
                                        il."TY_GIA" ,
                                        il."SO_CHUNG_TU" ,
                                        il."NGAY_CHUNG_TU" ,
                                        IL."CHI_NHANH_ID"
                                FROM    so_kho_chi_tiet IL
                                        INNER JOIN TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO II ON ( IL."MA_HANG_ID" = II."MA_HANG_ID"
                                                                            AND ( IL."KHO_ID" = II."MA_KHO_ID"
                                                                            OR II."MA_KHO_ID" IS NULL
                                                                            )
                                                                            )
                                WHERE   "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

                                        AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                        || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%'
                                UNION --lấy thêm các chứng từ chuyển kho ở kho đến nữa
                                SELECT  IL."id" ,
                                        IL."ID_CHUNG_TU" ,
                                        IL."MODEL_CHUNG_TU" ,
                                        IL."LOAI_CHUNG_TU" ,
                                        IL."NGAY_HACH_TOAN" ,
                                        IL."MA_TK_NO" ,
                                        IL."MA_TK_CO" ,
                                        IL."KHO_ID" ,
                                        IL."MA_HANG_ID" ,
                                        IL."DON_GIA" ,
                                        IL."DON_GIA_THEO_DVT_CHINH" ,
                                        IL."TY_LE_CHUYEN_DOI" ,
                                        IL."TOAN_TU_QUY_DOI" ,
                                        IL."SO_TIEN_NHAP" ,
                                        IL."SO_TIEN_XUAT" ,
                                        IL."SO_LUONG_NHAP_THEO_DVT_CHINH" ,
                                        IL."SO_LUONG_XUAT_THEO_DVT_CHINH" ,
                                        IL."STT_LOAI_CHUNG_TU" ,
                                        IL."CHI_TIET_ID" ,
                                        IL."CHI_TIET_MODEL" ,
                                        IL."LOAI_KHU_VUC_NHAP_XUAT" ,
                                        il."KHONG_CAP_NHAT_GIA_XUAT" ,
                                        il."LOAI_KHONG_CAP_NHAT_GIA_XUAT" ,
                                        IL."THU_TU_TRONG_CHUNG_TU" ,
                                        il."CHUNG_TU_LAP_RAP_THAO_DO_ID" ,
                                        il."SO_CHUNG_TU_NHAP_DOI_TRU" ,
                                        il."TEN_LOAI_TIEN" ,
                                        il."TY_GIA" ,
                                        il."SO_CHUNG_TU" ,
                                        il."NGAY_CHUNG_TU" ,
                                        IL."CHI_NHANH_ID"
                                FROM    so_kho_chi_tiet IL
                                        INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS INTD ON INTD."id" = IL."CHI_TIET_ID"
                                        INNER JOIN TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO II ON ( INTD."MA_HANG_ID" = II."MA_HANG_ID"
                                                                            AND ( INTD."XUAT_TAI_KHO_ID" = II."MA_KHO_ID"
                                                                            OR II."MA_KHO_ID" IS NULL
                                                                            )
                                                                            )
                                WHERE   "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
                                        AND IL."LOAI_KHU_VUC_NHAP_XUAT" = '2'

                                        AND v_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_danh_sach
                                        || CAST("CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_danh_sach || '%%';





                DROP TABLE IF  EXISTS  TMP_SO_KHO_CHI_TIET_KQ;

                    CREATE TEMP TABLE TMP_SO_KHO_CHI_TIET_KQ
                        AS

                        SELECT  IL.*
                        FROM    TMP_SO_KHO_CHI_TIET IL
                                LEFT JOIN LAY_DS_THU_TU_TINH_TOAN_VAT_TU(
                                                                            v_chi_nhanh_id,
                                                                            ngan_cach_giua_cac_danh_sach) VO ON IL."MA_HANG_ID" = VO."ID_VTHH"
                                                                                                AND IL."CHI_NHANH_ID" = VO."CHI_NHANH_ID"	--BTAnh thêm vào để sửa lỗi JIRA: SMEFIVE-7645
                        ORDER BY VO."THU_TU_GHI_SO_TINH_TOAN" ,--sắp thứ tự tính giá cho vật tư để đảm bảo vật tư nào là thành phẩm lắp ráp thì phải được tính sau cùng
                                IL."MA_HANG_ID" ,
                                CASE WHEN  IsCaculateByStock = 1 THEN IL."KHO_ID"  ELSE  CAST(CAST(0 AS BOOLEAN) AS INT) END,--trường hợp tính giá k theo kho thì cập nhật chứng từ xuất cuối cùng phải cập nhật trên toàn hệ thống
                                "LOAI_KHU_VUC_NHAP_XUAT" ,--mục đích xếp chuyển kho lên tính trước để giảm thiểu lỗi trong trường hợp xuất hết phải chia lại đơn giá, trường hợp này mình sẽ chia lại đơn giá của thằng xuất kho thôi
                                "NGAY_HACH_TOAN" ,
                                "STT_LOAI_CHUNG_TU" ,
                                "THU_TU_TRONG_CHUNG_TU" ,
                                "SO_LUONG_NHAP_THEO_DVT_CHINH" ;


            DROP TABLE IF EXISTS TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO_KQ
                ;

                CREATE TEMP TABLE TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO_KQ
                    AS


                        SELECT  D."MA_HANG_ID" ,
                                COALESCE(D."MA_KHO_ID", CAST(CAST(0 AS BOOLEAN) AS INT)) AS "MA_KHO_ID" ,
                                D."SO_LUONG_TON" ,
                                D."GIA_TRI_TON" ,
                                D."DON_GIA_XUAT_KHO" ,
                                D."TONG_SL_NHAP" ,
                                D."TONG_GIA_TRI_NHAP" ,
                                D."TINH_TRANG" ,
                                I."MA" ,
                                I."TEN" ,
                                S."MA_KHO" ,
                                S."TEN_KHO"
                        FROM    TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO D
                                LEFT JOIN danh_muc_vat_tu_hang_hoa I ON D."MA_HANG_ID" = I."id"
                                LEFT JOIN danh_muc_kho S ON D."MA_KHO_ID" = S."id" ;
                -- --lấy dữ liệu cho bảng tồn theo chi nhánh ClossingAverageDictionaryByBranch
                -- --trường hợp tính k theo kho thì tính tồn trên tất cả các kho và các chi nhánh

                    DROP TABLE IF EXISTS LAY_DU_LIEU_BANG_TON_THEO_CHI_NHANH
                ;

                        IF IsCaculateByStock = 1
                            THEN

                    CREATE  TEMP TABLE  LAY_DU_LIEU_BANG_TON_THEO_CHI_NHANH
                                AS


                            SELECT  COALESCE(I."KHO_ID",
                                        CAST(CAST(0 AS BOOLEAN ) AS INT)) AS "MA_KHO_ID" ,
                                    COALESCE(I."CHI_NHANH_ID",
                                        CAST(CAST(0 AS BOOLEAN ) AS INT)) AS "CHI_NHANH_ID" ,
                                    I."MA_HANG_ID" ,
                                    COALESCE(COALESCE(SUM(I."SO_LUONG_NHAP_THEO_DVT_CHINH"), 0)
                                        - COALESCE(SUM(I."SO_LUONG_XUAT_THEO_DVT_CHINH"), 0), 0) "SO_LUONG_TON" ,
                                    COALESCE(COALESCE(SUM(I."SO_TIEN_NHAP"), 0)
                                        - COALESCE(SUM(I."SO_TIEN_XUAT"), 0), 0) "GIA_TRI_TON" ,
                                    NULL AS "CurrentOutwardInventoryLedgerID" ,
                                    NULL AS "CurrentInventoryLedgerID" ,
                                    0   AS "TINH_TRANG" ,
                                    COALESCE(COALESCE(SUM(I."SO_TIEN_NHAP"), 0)
                                        - COALESCE(SUM(I."SO_TIEN_XUAT"), 0), 0) "GIA_TRI_TON_CU"
                            FROM    TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO D
                                    INNER JOIN so_kho_chi_tiet I ON D."MA_HANG_ID" = I."MA_HANG_ID"
                                                                            AND D."MA_KHO_ID" = I."KHO_ID"
                            WHERE   I."NGAY_HACH_TOAN" < v_tu_ngay

                                    AND v_chi_nhanh_id LIKE '%%'
                                    || CAST(I."CHI_NHANH_ID" AS VARCHAR(50)) || '%%'
                                    AND ( danh_sach_vthh_ids IS NULL
                                        OR danh_sach_vthh_ids LIKE '%%'
                                        || CAST(I."MA_HANG_ID" AS VARCHAR(50)) || '%%'
                                        )
                            GROUP BY COALESCE(I."KHO_ID",
                                            CAST(CAST(0 AS BOOLEAN ) AS INT)) ,
                                    COALESCE(I."CHI_NHANH_ID",
                                        CAST(CAST(0 AS BOOLEAN ) AS INT)) ,
                                    I."MA_HANG_ID" ;
                        ELSE

                            CREATE  TEMP TABLE  LAY_DU_LIEU_BANG_TON_THEO_CHI_NHANH
                                AS

                            SELECT  CAST(CAST(0 AS BOOLEAN ) AS INT) AS "MA_KHO_ID" ,
                                    CAST(CAST(0 AS BOOLEAN ) AS INT) AS "CHI_NHANH_ID" ,
                                    I."MA_HANG_ID" ,
                                    COALESCE(COALESCE(SUM(I."SO_LUONG_NHAP_THEO_DVT_CHINH"), 0)
                                        - COALESCE(SUM(I."SO_LUONG_XUAT_THEO_DVT_CHINH"), 0), 0) "SO_LUONG_TON" ,
                                    COALESCE(COALESCE(SUM(I."SO_TIEN_NHAP"), 0)
                                        - COALESCE(SUM(I."SO_TIEN_XUAT"), 0), 0) "GIA_TRI_TON" ,
                                    NULL AS "CurrentOutwardInventoryLedgerID" ,
                                    NULL AS "CurrentInventoryLedgerID" ,
                                    0 "TINH_TRANG" ,
                                    COALESCE(COALESCE(SUM(I."SO_TIEN_NHAP"), 0)
                                        - COALESCE(SUM(I."SO_TIEN_XUAT"), 0), 0) "GIA_TRI_TON_CU"
                            FROM    TMP_TAT_CA_CAC_PHAT_SINH_TINH_CA_CHUYEN_KHO D
                                    INNER JOIN so_kho_chi_tiet I ON D."MA_HANG_ID" = I."MA_HANG_ID"
                            WHERE   I."NGAY_HACH_TOAN" < v_tu_ngay

                                    AND v_chi_nhanh_id LIKE '%%'
                                    || CAST(I."CHI_NHANH_ID" AS VARCHAR(50)) || '%%'
                                    AND ( danh_sach_vthh_ids IS NULL
                                        OR danh_sach_vthh_ids LIKE '%%'
                                        || CAST(I."MA_HANG_ID" AS VARCHAR(50)) || '%%'
                                        )
                            GROUP BY
                                    I."MA_HANG_ID" ;
                END IF;

                --lấy dữ liệu cho bảng chuyển kho
                DROP TABLE IF EXISTS LAY_DU_LIEU_CHO_BANG_CHUYEN_KHO
                ;

                CREATE TEMP TABLE LAY_DU_LIEU_CHO_BANG_CHUYEN_KHO
                    AS
                        SELECT  *
                        FROM    TMP_DS_CAC_KHO_CHUYEN_DI_VA_CHUYEN_DEN_THEO_VAT_TU
                        WHERE   "TONG_SL" <> 0
                                AND "NHAP_TAI_KHO_ID" IS NOT NULL
                                AND "XUAT_TAI_KHO_ID" IS NOT NULL ;-- NNanh Chỉ lấy những chuyển kho có tổng sl <>0
            --     -- lấy dữ liệu cho bảng "NHAP_KHO""XUAT_KHO"AssemblyRelation (lắp ráp)
            --
            --
                DROP TABLE IF EXISTS LAY_DU_LIEU_CHO_BANG_LAP_RAP
                ;

                CREATE TEMP TABLE LAY_DU_LIEU_CHO_BANG_LAP_RAP
                    AS
                        SELECT DISTINCT

                                inin."id" AS "NHAP_KHO_ID" ,
                                ININM."KHO_ID" AS "MA_KHO_ID" ,
                                ININM."MA_HANG_ID" AS "MA_HANG_ID" ,
                                INOUT."CHI_TIET_ID" ,
                                INOUT."CHI_TIET_MODEL" , -- nếu lấy thêm cột refdetail của chứng từ xuất để tìm ra dòng chứng từ nhập có liên quan đến nó
                                INOUT."ID_CHUNG_TU" ,
                                INOUT."MODEL_CHUNG_TU" ,
                                ININ."LOAI_CHUNG_TU"  ,
                                ININM."SO_LUONG" AS "SO_LUONG" ,
                                ININM."SO_LUONG_THEO_DVT_CHINH" AS "SO_LUONG_NHAP_THEO_DVT_CHINH" ,
                        --trường hợp đang ở sổ quản trị thì lấy tiền ở sổ quản trị
                                ININM."TIEN_VON_QUY_DOI" AS "SO_TIEN_NHAP_CU" ,
                                INOUT."SO_TIEN_XUAT" AS "SO_TIEN_XUAT_CU" ,
                                ININM."id" AS "NHAP_XUAT_KHO_CHI_TIET_ID",
                                --trường hợp chứng từ nhập chưa được ghi sổ thì lấy fix mặc định = -1
                                CASE	 WHEN ii."id" is NOT NULL THEN ii."id" ELSE -1 END AS "SO_KHO_CHI_TIET_ID"
                        FROM    TMP_SO_KHO_CHI_TIET AS INOUT
                                INNER JOIN stock_ex_nhap_xuat_kho AS ININ ON ( INOUT."CHUNG_TU_LAP_RAP_THAO_DO_ID" = ININ."LAP_RAP_THAO_DO_ID"
                                                                    AND inout."LOAI_KHU_VUC_NHAP_XUAT" = '3'
                                                                    AND inin."LOAI_CHUNG_TU" = '2011'
                                                                )
                                INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet ININM ON ININM."NHAP_XUAT_ID" = ININ."id"
                                INNER JOIN danh_muc_reftype RT ON RT."REFTYPE" = ININ."LOAI_CHUNG_TU"
                                LEFT JOIN so_kho_chi_tiet II ON ii."CHI_TIET_ID"=ININM."id" AND ii."CHI_TIET_MODEL"='stock.ex.nhap.xuat.kho.chi.tiet'  ;

            --     -- -- lấy dữ liệu cho bảng "NHAP_KHO""XUAT_KHO"ReturnRelation (hàng bán trả lại)
                DROP TABLE IF EXISTS LAY_DU_LIEU_CHO_BANG_HANG_BAN_TRA_LAI
                ;

                CREATE TEMP TABLE LAY_DU_LIEU_CHO_BANG_HANG_BAN_TRA_LAI
                    AS

                        SELECT DISTINCT

                                inin."id" AS "NHAP_XUAT_KHO_CHI_TIET_ID" ,
                                inin."NHAP_XUAT_ID" AS "NHAP_XUAT_KHO_ID" ,
                                ININM."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NHAP_KHO" ,
                                CASE WHEN IsCaculateByStock = 1 THEN ININ."KHO_ID"
                                    ELSE CAST(CAST(0 AS BOOLEAN ) AS INT)
                                END AS "MA_KHO_ID" ,
                                inin."MA_HANG_ID" ,
                                inin."SO_LUONG_THEO_DVT_CHINH" ,
                                COALESCE(inin."TOAN_TU_QUY_DOI", '0') "PHEP_TINH_CHUYEN_DOI" ,
                                COALESCE(inin."TY_LE_CHUYEN_DOI_RA_DVT_CHINH", 1) "TY_LE_CHUYEN_DOI"
                        FROM    stock_ex_nhap_xuat_kho_chi_tiet AS ININ
                                INNER JOIN stock_ex_nhap_xuat_kho AS ININM ON ( inin."NHAP_XUAT_ID" = ININM."id"
                                                                    AND ininm."PHUONG_THUC_TINH_DON_GIA_NHAP" = '0'
                                                                    AND ininm."LOAI_CHUNG_TU" = '2013'
                                                                    )
                                INNER JOIN danh_muc_reftype RT ON RT."REFTYPE" = ININM."LOAI_CHUNG_TU"
                        INNER JOIN danh_muc_vat_tu_hang_hoa II ON ININ."MA_HANG_ID" = II."id" AND II."TINH_CHAT" IN ('0','1')-- NNAnh 21/7/2015: không lấy vật tư chỉ là diễn giải và dịch vụ --> chi lấy thành phẩm và thành phẩm
                        WHERE   ININM."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
                                /*Edit by dvha 23/08/2016 fixbug SMEFIVE-16908( Bug 114690): Văng lỗi tiếng anh khi tính giá xuất kho*/
                                AND CASE WHEN IsCaculateByStock = 1 THEN ININ."KHO_ID" ELSE CAST(CAST(0 AS BOOLEAN ) AS INT) END IS NOT NULL

                                AND v_chi_nhanh_id LIKE '%%'
                                || CAST(ININM."CHI_NHANH_ID" AS VARCHAR(50)) || '%%'
                                AND ( danh_sach_vthh_ids IS NULL
                                    OR danh_sach_vthh_ids LIKE '%%'
                                    || CAST(ININ."MA_HANG_ID" AS VARCHAR(50)) || '%%'
                                    )
                            ;



            END $$

            ;
            """+query_dieu_kien
            
        return self.execute(query, params)


    



    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS LAY_DS_THU_TU_TINH_TOAN_VAT_TU(IN ds_chi_nhanh_id VARCHAR(500),
            ngan_cach_giua_cac_ds VARCHAR(500));

            CREATE OR REPLACE FUNCTION LAY_DS_THU_TU_TINH_TOAN_VAT_TU(IN ds_chi_nhanh_id VARCHAR(500),
            ngan_cach_giua_cac_ds VARCHAR(500))--Func_IN_InventoryItemIDSortOrder
            RETURNS TABLE(
            "ID_VTHH" INTEGER,
            "THU_TU_GHI_SO_TINH_TOAN" INTEGER,
            "CO_THE_SAP_XEP" BOOLEAN,
            "CHI_NHANH_ID" INTEGER

            ) AS $$


            DECLARE

            rec RECORD;

            rec_2 RECORD;

            TU_VAT_TU_HH_DON_HANG INT := 1;

            DEN_VAT_TU_HH_DON_HANG INT := 1;



            BEGIN

            DROP TABLE IF EXISTS LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH_CUOI_CUNG
            ;

            CREATE TEMP TABLE LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH_CUOI_CUNG
            (
            "ID_VTHH" INTEGER,
            "THU_TU_GHI_SO_TINH_TOAN" INTEGER,
            "CO_THE_SAP_XEP" BOOLEAN,
            "CHI_NHANH_ID" INTEGER

            )
            ;


            DROP TABLE IF EXISTS LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            ;

            CREATE TEMP TABLE LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            (
            "ID_VTHH" INTEGER,
            "THU_TU_GHI_SO_TINH_TOAN" INTEGER,
            "CO_THE_SAP_XEP" BOOLEAN,
            "CHI_NHANH_ID" INTEGER

            )
            ;

            INSERT INTO LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            (
            "ID_VTHH",
            "THU_TU_GHI_SO_TINH_TOAN",
            "CO_THE_SAP_XEP",
            "CHI_NHANH_ID"
            )
            SELECT DISTINCT
            B."MA_HANG_ID"
            , 1 AS "THU_TU_GHI_SO_TINH_TOAN"
            --những thằng nào có trong thành phẩm lắp ráp thì ưu tiên tính giá sau cùng (thứ tự này là chưa chuẩn, trường hợp 1 vật tư vừa là thành phẩm vừa là linh kiện thì thứ tự này chưa đảm bảo)
            , TRUE
            , --mặc định là cái nào cũng sắp xếp được
            A."CHI_NHANH_ID"
            FROM stock_ex_nhap_xuat_kho A
            JOIN stock_ex_nhap_xuat_kho_chi_tiet B
            ON A."id" = B."NHAP_XUAT_ID"
            WHERE A."LAP_RAP_THAO_DO_ID" IS NOT NULL
            AND A."LOAI_CHUNG_TU" = '2011'
            AND (A."state" = 'da_ghi_so'

            )

            AND ds_chi_nhanh_id LIKE '%%' || ngan_cach_giua_cac_ds
            || CAST(A."CHI_NHANH_ID" AS VARCHAR(50)) || ngan_cach_giua_cac_ds || '%%'
            ;

            --Duyệt trong danh sách linh kiện lắp ráp và thành phẩm, thực hiện kiểm tra và sắp lại thứ tự


            FOR rec IN


            SELECT DISTINCT
            D."MA_HANG_ID" AS "TU_VAT_TU_HH"
            , M."HANG_HOA_ID" AS "DEN_VAT_TU_HH"
            , M."CHI_NHANH_ID" AS "CHI_NHANH_ID"
            FROM stock_ex_lap_rap_thao_do M
            INNER JOIN stock_ex_lap_rap_thao_do_chi_tiet D ON M."id" = D."LAP_RAP_THAO_DO_CHI_TIET_ID"
            --chỉ duyệt những bộ có linh kiện thuộc danh sách thành phẩm thôi
            INNER JOIN LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH I ON D."MA_HANG_ID" = I."ID_VTHH"
            --chỉ duyệt những bộ có chứng từ nhập đã được ghi sổ
            INNER JOIN so_kho_chi_tiet L ON M."id" = L."CHUNG_TU_LAP_RAP_THAO_DO_ID" AND L."LOAI_KHU_VUC_NHAP_XUAT" = '1'

            WHERE M."LOAI_CHUNG_TU" = 2050

            LOOP

            FOR rec_2 IN
            SELECT *
            FROM LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH

            LOOP


            SELECT "THU_TU_GHI_SO_TINH_TOAN"
            INTO TU_VAT_TU_HH_DON_HANG
            FROM LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            WHERE "ID_VTHH" = rec."TU_VAT_TU_HH"

            ;

            SELECT "THU_TU_GHI_SO_TINH_TOAN"
            INTO DEN_VAT_TU_HH_DON_HANG
            FROM LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            WHERE "ID_VTHH" = rec."TU_VAT_TU_HH"

            ;


            IF TU_VAT_TU_HH_DON_HANG > DEN_VAT_TU_HH_DON_HANG
            THEN

            -- trường hợp đã có 1 thứ tự tính toán cho 2 kho này nhưng ngược nhau thì k thể sắp xếp được nữa
            UPDATE LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            SET "CO_THE_SAP_XEP" = FALSE
            WHERE "ID_VTHH" = rec."TU_VAT_TU_HH"
            AND "CHI_NHANH_ID" = rec."CHI_NHANH_ID"
            ;

            UPDATE LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            SET "CO_THE_SAP_XEP" = FALSE
            WHERE "ID_VTHH" = rec."DEN_VAT_TU_HH"
            AND "CHI_NHANH_ID" = rec."CHI_NHANH_ID"
            ;

            ELSE
            IF TU_VAT_TU_HH_DON_HANG = DEN_VAT_TU_HH_DON_HANG
            THEN
            --trường hợp thứ tự tính toán đang bình đẳng thì thực hiện update tất cả thứ tự tính toán cho những thằng từ sau B trở đi
            UPDATE LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH
            SET "THU_TU_GHI_SO_TINH_TOAN" = "THU_TU_GHI_SO_TINH_TOAN"
            + 1
            WHERE "THU_TU_GHI_SO_TINH_TOAN" >= DEN_VAT_TU_HH_DON_HANG
            AND "ID_VTHH" <> rec."TU_VAT_TU_HH"
            ;

            END IF
            ;

            END IF
            ;

            END LOOP
            ;

            END LOOP
            ;

            INSERT INTO LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH_CUOI_CUNG (
            SELECT DISTINCT
            A."ID_VTHH"
            , A."THU_TU_GHI_SO_TINH_TOAN"
            , A."CO_THE_SAP_XEP"
            , A."CHI_NHANH_ID"
            FROM LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH A)
            ;

            RETURN QUERY SELECT *
            FROM LAY_DS_THU_TU_TINH_TOAN_VAT_TU_TMP_VTHH_CUOI_CUNG
            ;


            END
            ;

            $$ LANGUAGE PLpgSQL
            ;

		""")