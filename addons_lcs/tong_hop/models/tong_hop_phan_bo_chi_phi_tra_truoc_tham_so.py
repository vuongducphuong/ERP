# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_THAM_SO(models.Model):
    _name = 'tong.hop.phan.bo.chi.phi.tra.truoc.tham.so'
    _description = ''
    _auto = False

    THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng',required=True)
    NAM = fields.Integer(string='Năm', help='Năm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ',help='Loại chứng từ')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
        result = super(TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_THAM_SO, self).default_get(fields_list)
        thang = datetime.now().month
        result['NAM'] = datetime.now().year
        result['THANG'] = str(thang)
        return result

    def action_view_result(self):
        nam_tai_chinh = int(self.env['ir.config_parameter'].get_param('he_thong.NAM_TAI_CHINH_BAT_DAU'))
        nam_thuc_hien_phan_bo = self.get_context('NAM')
        if nam_thuc_hien_phan_bo < nam_tai_chinh: #Mạnh sửa bug2355 : Thêm đoạn code này để check xem nếu năm thực hiện phân bổ nhỏ hơn năm tài chính thì thông báo lỗi cho người dùng.
            raise ValidationError('Chương trình không cho phép nhập Năm nhỏ hơn năm bắt đầu hạch toán của chương trình. Bạn vui lòng kiểm tra lại.')
        else:
            thang_da_phan_bo = self.env['account.ex.chung.tu.nghiep.vu.khac'].search([('LOAI_CHUNG_TU','=',4020)])
            for pb in thang_da_phan_bo:
                if self.get_context('NAM') == pb.NAM:
                    if self.get_context('THANG') == str(pb.THANG):
                        raise ValidationError('Đã lập chứng từ phân bổ tháng ' +str(self.get_context('THANG')) +' năm ' +str(self.get_context('NAM')))
        action = self.env.ref('tong_hop.action_open_tong_hop_phan_bo_chi_phi_tra_truoc_tham_so_form').read()[0]
        str_dien_giai = 'Phân bổ chi phí trả trước tháng ' + str(self.get_context('THANG')) + ' năm ' + str(self.get_context('NAM'))
        chi_phi_tra_troc = self.env['tong.hop.chi.phi.tra.truoc'].search([])

        arr_chi_phi = []
        arr_phan_bo = []
        arr_hach_toan = []
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')]).id
        for line in chi_phi_tra_troc:
            arr_chi_phi += [(0, 0, {
                'MA_CP_TRA_TRUOC_ID' : line.id,
                'TEN_CP_TRA_TRUOC': line['TEN_CHI_PHI_TRA_TRUOC'],
                'SO_TIEN': line['SO_TIEN'],
                'SO_TIEN_CHUA_PHAN_BO': line['SO_TIEN'],
                'SO_TIEN_PHAN_BO_TRONG_KY': line['SO_TIEN_PB_HANG_KY'],
                })]
            for phan_bo in line['TONG_HOP_CHI_PHI_TRA_TRUOC_THIET_LAP_PHAN_BO_IDS']:
                arr_phan_bo += [(0,0,{
                    'MA_CP_TRA_TRUOC_ID' : line.id,
                    'TEN_CP_TRA_TRUOC' : line['TEN_CHI_PHI_TRA_TRUOC'],
                    'CHI_PHI_PHAN_BO' : line['SO_TIEN_PB_HANG_KY'],
                    'DOI_TUONG_PHAN_BO_ID': phan_bo['DOI_TUONG_PHAN_BO_ID'].id,
                    'TEN_DOI_TUONG_PHAN_BO' : phan_bo['DOI_TUONG_PHAN_BO_ID'].TEN_DON_VI,
                    'TY_LE' : phan_bo['TY_LE_PB'],
                    'SO_TIEN' : (phan_bo['TY_LE_PB']*line['SO_TIEN_PB_HANG_KY'])/100,
                    'TK_NO_ID' : phan_bo['TK_NO_ID'].id,
                    'KHOAN_MUC_CP_ID' : phan_bo['KHOAN_MUC_CP_ID'].id,
                })]
                don_vi = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', phan_bo['DOI_TUONG_PHAN_BO_ID'].MA_DON_VI)], limit=1).id
                arr_hach_toan += [(0,0,{
                    'DIEN_GIAI' : str_dien_giai,
                    'SO_TIEN' : (phan_bo['TY_LE_PB']*line['SO_TIEN_PB_HANG_KY'])/100,
                    'SO_TIEN_QUY_DOI' : (phan_bo['TY_LE_PB']*line['SO_TIEN_PB_HANG_KY'])/100,
                    'TK_NO_ID' : phan_bo['TK_NO_ID'].id,
                    'TK_CO_ID': line['TK_CHO_PHAN_BO_ID'].id,
                    'DON_VI_ID': don_vi,
                    'KHOAN_MUC_CP_ID' : phan_bo['KHOAN_MUC_CP_ID'].id,
                })]


        context = {
            'default_DIEN_GIAI': str_dien_giai,
            'default_THANG': self.get_context('THANG'),
            'default_NAM': self.get_context('NAM'),
            'default_currency_id' : loai_tien,
            'default_TY_GIA' : 1,
            # 'default_account_payment_ids': [(0, 0, {
            #     'amount':self.get_context('SO_TIEN'),
            #     'dien_giai':tr_diengiai,
            #     'tk_no_id' : tk_no,
            #     'tk_co_id' : 9,
            #     })],
            'default_TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_XD_CHI_PHI_IDS' : arr_chi_phi,
            'default_TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_PHAN_BO_IDS' : arr_phan_bo,
            'default_ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS' : arr_hach_toan,
            'default_LOAI_CHUNG_TU'     :4020 ,

            }

        action['context'] = helper.Obj.merge(context, action.get('context'))

        # action['options'] = {'clear_breadcrumbs': True}
        return action
