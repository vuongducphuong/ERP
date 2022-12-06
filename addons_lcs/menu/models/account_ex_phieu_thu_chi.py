# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError
from operator import itemgetter
from datetime import timedelta, datetime
from odoo.tools.float_utils import float_round

class ACCOUNT_EX_PHIEU_THU_CHI(models.Model):
    _inherit = "account.ex.phieu.thu.chi"

    @api.multi
    def validate_thu_chi_tien(self):
        for record in self:
            record.validate_unique_thu_chi_tien(record.SO_CHUNG_TU)

    @api.model
    def create(self, vals):
        result = super(ACCOUNT_EX_PHIEU_THU_CHI, self).create(vals)
        result.validate_thu_chi_tien()
        # Update sequence
        loai_chung_tu = ''
        if result.TYPE_NH_Q == 'NGAN_HANG':
            if result.LOAI_PHIEU == 'PHIEU_CHI':
                loai_chung_tu = result.PHUONG_THUC_TT
            else:
                loai_chung_tu = 'THU_TIEN_GUI'
        else:
            loai_chung_tu = result.LOAI_PHIEU
        sequence_code = 'account_ex_phieu_thu_chi_SO_CHUNG_TU_' + loai_chung_tu
        self.update_sequence(sequence_code, result.SO_CHUNG_TU)
        return result
    
    @api.multi
    def write(self, values):
        result = super(ACCOUNT_EX_PHIEU_THU_CHI, self).write(values)
        if values.get('SO_CHUNG_TU'):
            self.validate_thu_chi_tien()
        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        fields += ['ID_GOC', 'MODEL_GOC']
        return self.env['menu.phieu.thu.chi.view'].search_read(domain, fields, offset, limit, order)

    # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1636
    @api.model
    def search_count(self, args):
        return self.env['menu.phieu.thu.chi.view'].search_count(args)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ACCOUNT_EX_PHIEU_THU_CHI, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
        if toolbar:
            bindings = self.env['ir.actions.actions'].get_bindings('menu.phieu.thu.chi.view')
            res['toolbar']['print'] += [action for action in bindings['report'] if view_type == 'tree' or not action.get('multi')]
        return res

    @api.model_cr
    def init(self):
        #quanhm 2019-04-22: de check xem co can cap nhat du lieu khong
        module = self.env['ir.module.module'].search([('name','=',self._module)],limit=1)
        self.tao_view_tim_kiem()
        if module.latest_version and module.latest_version < '11.0.0.1':
            self.update_v01()
        if module.latest_version and module.latest_version < '11.0.0.2':
            self.update_v02()
        if module.latest_version and module.latest_version < '11.0.0.3':
            self.update_v03()
        if module.latest_version and module.latest_version < '11.0.0.4':
            self.update_v04()
        if module.latest_version and module.latest_version < '11.0.0.5':
            self.update_v05()
        if module.latest_version and module.latest_version < '11.0.0.6':
            self.update_v06()
        if module.latest_version and module.latest_version < '11.0.0.7':
            self.update_v07()
        if module.latest_version and module.latest_version < '11.0.0.8':
            self.update_v08()
        if module.latest_version and module.latest_version < '11.0.0.9':
            self.update_v09()
        if module.latest_version and module.latest_version < '11.0.1.0':
            self.update_v10()
        if module.latest_version and module.latest_version < '11.0.1.1':
            self.update_v11()
        if module.latest_version and module.latest_version < '11.0.1.2':
            self.update_v12()
        if module.latest_version and module.latest_version < '11.0.1.3':
            self.update_v13()
        if module.latest_version and module.latest_version < '11.0.1.4':
            self.update_v14()
        if module.latest_version and module.latest_version < '11.0.1.5':
            self.update_v15()
        if module.latest_version and module.latest_version < '11.0.1.6':
            self.update_v16()
        if module.latest_version and module.latest_version < '11.0.1.7':
            self.update_v17()
        if module.latest_version and module.latest_version < '11.0.1.8':
            self.update_v18()
        if module.latest_version and module.latest_version < '11.0.1.9':
            self.update_v19()
        if module.latest_version and module.latest_version < '11.0.2.1':
            self.update_v21()
        if module.latest_version and module.latest_version < '11.0.2.2':
            self.update_v22()
        if module.latest_version and module.latest_version < '11.0.2.3':
            self.update_v23()
        if module.latest_version and module.latest_version < '11.0.2.4':
            self.update_v24()
        if module.latest_version and module.latest_version < '11.0.2.5':
            self.update_v25()
        if module.latest_version and module.latest_version < '11.0.2.6':
            self.update_v26()
        if module.latest_version and module.latest_version < '11.0.2.7':
            self.update_v27()
        if module.latest_version and module.latest_version < '11.0.2.8':
            self.update_v28()
        if module.latest_version and module.latest_version < '11.0.2.9':
            self.update_v29()
        if module.latest_version and module.latest_version < '11.0.3.0':
            self.update_v30()
        # if module.latest_version and module.latest_version < '11.0.3.1':
        #     self.update_v31()
        if module.latest_version and module.latest_version < '11.0.3.2':
            self.update_v32()
        if module.latest_version and module.latest_version < '11.0.3.3':
            self.update_v33()
        if module.latest_version and module.latest_version < '11.0.3.4':
            self.update_v34()
        if module.latest_version and module.latest_version < '11.0.3.5':
            self.update_v35()
        # if module.latest_version and module.latest_version < '11.0.3.6':
        #     self.update_v36()
        if module.latest_version and module.latest_version < '11.0.3.7':
            self.update_v37()
        if module.latest_version and module.latest_version < '11.0.3.8':
            self.update_v38()
        if module.latest_version and module.latest_version < '11.0.3.9':
            self.update_v39()
        if module.latest_version and module.latest_version < '11.0.4.0':
            self.update_v40()
        if module.latest_version and module.latest_version < '11.0.4.1':
            self.update_v41()
        if module.latest_version and module.latest_version < '11.0.4.2':
            self.update_v42()
        if module.latest_version and module.latest_version < '11.0.4.3':
            self.update_v43()
        if module.latest_version and module.latest_version < '11.0.4.4':
            self.update_v44()
        if module.latest_version and module.latest_version < '11.0.4.5':
            self.update_v45()
        if module.latest_version and module.latest_version < '11.0.4.6':
            self.update_v46()
        if module.latest_version and module.latest_version < '11.0.4.7':
            self.update_v47()
        if module.latest_version and module.latest_version < '11.0.4.8':
            self.update_v48()
        if module.latest_version and module.latest_version < '11.0.4.9':
            self.update_v49()
        if module.latest_version and module.latest_version < '11.0.5.0':
            self.update_v50()
        if module.latest_version and module.latest_version < '11.0.5.1':
            self.update_v51()
        if module.latest_version and module.latest_version < '11.0.5.2':
            self.update_v52()
        if module.latest_version and module.latest_version < '11.0.5.3':
            self.update_v53()
        if module.latest_version and module.latest_version < '11.0.5.4':
            self.update_v54()
        if module.latest_version and module.latest_version < '11.0.5.5':
            self.update_v55()
        if module.latest_version and module.latest_version < '11.0.5.6':
            self.update_v56()
        if module.latest_version and module.latest_version < '11.0.5.7':
            self.update_v57()
        if module.latest_version and module.latest_version < '11.0.5.8':
            self.update_v58()
        if module.latest_version and module.latest_version < '11.0.5.9':
            self.update_v59()
        if module.latest_version and module.latest_version < '11.0.6.0':
            self.update_v60()
        if module.latest_version and module.latest_version < '11.0.6.1':
            self.update_v61()
        if module.latest_version and module.latest_version < '11.0.6.2':
            self.update_v62()
        if module.latest_version and module.latest_version < '11.0.6.3':
            self.update_v63()
        if module.latest_version and module.latest_version < '11.0.6.4':
            self.update_v64()
        if module.latest_version and module.latest_version < '11.0.6.5':
            self.update_v65()
        if module.latest_version and module.latest_version < '11.0.6.6':
            self.update_v66()
        if module.latest_version and module.latest_version <= '11.0.6.7':
            self.update_v67()
        if module.latest_version and module.latest_version < '11.0.6.8':
            self.update_v68()
        if module.latest_version and module.latest_version < '11.0.6.9':
            self.update_v69()
        if module.latest_version and module.latest_version < '11.0.7.0':
            self.update_v70()
        if module.latest_version and module.latest_version < '11.0.7.1':
            self.update_v71()
        if module.latest_version and module.latest_version <= '11.0.7.2':
            self.update_v72()
        if module.latest_version and module.latest_version < '11.0.7.3':
            self.update_v73()
        if module.latest_version and module.latest_version < '11.0.7.4':
            self.update_v74()
        if module.latest_version and module.latest_version < '11.0.7.5':
            self.update_v75()


        # Tricks: Để import được, hệ thống menu phải được cập nhật trước
        if not self.env['he.thong.vai.tro.va.quyen.han'].search([],limit=1):
            self.env['base_import_ex.import'].auto_import('0. SubSystem.xml')
            self.env['base_import_ex.import'].auto_import('1. Tổng hợp vai trò quyền hạn.xml')
        #  Import danh sách mẫu in
        if 'he.thong.mau.in' in self.env and not self.env['he.thong.mau.in'].search([],limit=1):
            self.env['base_import_ex.import'].auto_import('danh_sach_mau_in.xml')
        #  Replace view theo thông tư (133)
        if self.lay_che_do_ke_toan() == '48':
            ref_view_he_so_ty_le = self.env.ref('gia_thanh.view_gia_thanh_tinh_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_tham_so_form')
            if ref_view_he_so_ty_le:
                ref_view_he_so_ty_le.arch_db = ref_view_he_so_ty_le.arch_db.replace("{'header_struct': [['Tài khoản 621', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Tài khoản 622', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Tài khoản 6271', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Tài khoản 6272', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Tài khoản 6273', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Tài khoản 6274', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Tài khoản 6277', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Tài khoản 6278', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}","{'header_struct': [['Chi phí nguyên liệu, vật liệu trực tiếp', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Chi phí nhân công trực tiếp', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Chi phí nhân viên phân xưởng', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Chi phí vật liệu', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Chi phí dụng cụ sản xuất', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Chi phí khấu hao TSCĐ', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Chi phí dịch vụ mua ngoài', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Chi phí bằng tiền khác', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}")
            
            ref_view_gian_don = self.env.ref('gia_thanh.view_gia_thanh_tinh_gia_thanh_tham_so_form')
            if ref_view_gian_don:
                ref_view_gian_don.arch_db = ref_view_gian_don.arch_db.replace("{'header_struct': [['Tài khoản 621', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Tài khoản 622', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Tài khoản 6271', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Tài khoản 6272', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Tài khoản 6273', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Tài khoản 6274', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Tài khoản 6277', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Tài khoản 6278', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}","{'header_struct': [['Chi phí nguyên liệu, vật liệu trực tiếp', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Chi phí nhân công trực tiếp', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Chi phí nhân viên phân xưởng', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Chi phí vật liệu', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Chi phí dụng cụ sản xuất', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Chi phí khấu hao TSCĐ', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Chi phí dịch vụ mua ngoài', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Chi phí bằng tiền khác', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}")

            ref_view_cong_trinh = self.env.ref('gia_thanh.view_gia_thanh_phan_bo_chi_phi_chung_cong_trinh_form')
            if ref_view_cong_trinh:
                ref_view_cong_trinh.arch_db = ref_view_cong_trinh.arch_db.replace("{'header_struct': [['Tài khoản 621', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Tài khoản 622', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Tài khoản 6271', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Tài khoản 6272', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Tài khoản 6273', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Tài khoản 6274', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Tài khoản 6277', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Tài khoản 6278', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}","{'header_struct': [['Chi phí nguyên liệu, vật liệu trực tiếp', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Chi phí nhân công trực tiếp', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Chi phí nhân viên phân xưởng', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Chi phí vật liệu', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Chi phí dụng cụ sản xuất', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Chi phí khấu hao TSCĐ', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Chi phí dịch vụ mua ngoài', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Chi phí bằng tiền khác', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}")

            ref_view_don_hang = self.env.ref('gia_thanh.view_gia_thanh_phan_bo_chi_phi_chung_don_hang_form')
            if ref_view_don_hang:
                ref_view_don_hang.arch_db = ref_view_don_hang.arch_db.replace("{'header_struct': [['Tài khoản 621', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Tài khoản 622', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Tài khoản 6271', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Tài khoản 6272', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Tài khoản 6273', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Tài khoản 6274', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Tài khoản 6277', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Tài khoản 6278', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}","{'header_struct': [['Chi phí nguyên liệu, vật liệu trực tiếp', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Chi phí nhân công trực tiếp', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Chi phí nhân viên phân xưởng', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Chi phí vật liệu', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Chi phí dụng cụ sản xuất', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Chi phí khấu hao TSCĐ', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Chi phí dịch vụ mua ngoài', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Chi phí bằng tiền khác', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}")

            ref_view_hop_dong = self.env.ref('gia_thanh.view_gia_thanh_phan_bo_chi_phi_chung_hop_dong_form')
            if ref_view_hop_dong:
                ref_view_hop_dong.arch_db = ref_view_hop_dong.arch_db.replace("{'header_struct': [['Tài khoản 621', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Tài khoản 622', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Tài khoản 6271', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Tài khoản 6272', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Tài khoản 6273', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Tài khoản 6274', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Tài khoản 6277', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Tài khoản 6278', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}","{'header_struct': [['Chi phí nguyên liệu, vật liệu trực tiếp', ['TY_LE_PHAN_TRAM_621','SO_TIEN_621']],['Chi phí nhân công trực tiếp', ['TY_LE_PHAN_TRAM_622','SO_TIEN_622']],['Chi phí nhân viên phân xưởng', ['TY_LE_PHAN_TRAM_6271','SO_TIEN_6271']],['Chi phí vật liệu', ['TY_LE_PHAN_TRAM_6272','SO_TIEN_6272']],['Chi phí dụng cụ sản xuất', ['TY_LE_PHAN_TRAM_6273','SO_TIEN_6273']],['Chi phí khấu hao TSCĐ', ['TY_LE_PHAN_TRAM_6274','SO_TIEN_6274']],['Chi phí dịch vụ mua ngoài', ['TY_LE_PHAN_TRAM_6277','SO_TIEN_6277']],['Chi phí bằng tiền khác', ['TY_LE_PHAN_TRAM_6278','SO_TIEN_6278']]]}")
    
    
    def update_v75(self):#https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3770/
        self.env['base_import_ex.import'].auto_import('Subsystem_vai_tro_quyen_han_thu_kho.xml')
        self.env['base_import_ex.import'].auto_import('Tổng hợp vai trò và quyền hạn thủ kho.xml')

    # Disable một số permission chưa hỗ trợ
    def update_v74(self):
        self.env['he.thong.permission'].search([('PermissionID', 'not in', ('Add','Delete','Edit','Use'))]).write({'active': False})

    # Import thêm file chứa report_id mẫu in phiếu xuất kho tổng hợp
    def update_v73(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_phieu_xuat_kho_tong_hop.xml')
    # Import thêm file chứa report_id đơn đặt hàng từ chứng từ bán hàng
    def update_v72(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_tu_chung_tu_ban_hang.xml')
    
    # Active thêm 1 báo cáo: Sổ nhật ký chung
    def update_v71(self): 
        list_bao_cao_con_duoc_hien_this = ['Sổ nhật ký chung','Báo cáo chi tiết lãi lỗ theo hợp đồng','Báo cáo tổng hợp lãi lỗ theo hợp đồng','Báo cáo chi tiết lãi lỗ theo đơn hàng','Báo cáo tổng hợp lãi lỗ theo đơn hàng','Chi phí dự kiến theo đơn đặt hàng','Sổ chi tiết vật tư hàng hóa','Tổng hợp bán hàng','Tổng hợp mua hàng','Bảng cân đối tài khoản','F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định','Tổng hợp chi phí sản xuất kinh doanh','Sổ chi tiết tài khoản chi phí sản xuất','Tổng hợp nhập xuất kho theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng tổng hợp chi phí theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng kê phiếu nhập, phiếu xuất theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Báo cáo tổng hợp lãi lỗ theo công trình','Báo cáo chi tiết lãi lỗ theo công trình','Bảng tính giá thành']
        list_bao_cao_cha_duoc_hien_this = ['Hợp đồng','Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định','Giá thành']        
        for line in self.env['tien.ich.bao.cao'].with_context({'active_test':False}).search([]):
            line.write({'active': line.TEN_BAO_CAO in (list_bao_cao_con_duoc_hien_this if line.parent_id else list_bao_cao_cha_duoc_hien_this)})

    def update_v70(self):
        web_layout = self.env.ref('web.layout')
        if web_layout:
            web_layout.arch_db = web_layout.arch_db.replace('<script type="text/javascript">','<script async="async" src="https://www.googletagmanager.com/gtag/js?id=UA-145792505-1"></script><script type="text/javascript">')

    # import thêm report_id mẫu in phiếu xuất kho bán hàng a5 dọc
    def update_v69(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_phieu_xuat_kho_ban_hang_a5_doc.xml')


    # Active thêm 4 báo cáo: Chi tiết lãi lỗ theo Đơn hàng, Tổng hợp lãi lỗ theo đơn hàng. Chi tiết lãi lỗ theo Hợp đồng, Tổng hợp lãi lỗ theo Hợp đồng
    def update_v68(self): 
        list_bao_cao_con_duoc_hien_this = ['Báo cáo chi tiết lãi lỗ theo hợp đồng','Báo cáo tổng hợp lãi lỗ theo hợp đồng','Báo cáo chi tiết lãi lỗ theo đơn hàng','Báo cáo tổng hợp lãi lỗ theo đơn hàng','Chi phí dự kiến theo đơn đặt hàng','Sổ chi tiết vật tư hàng hóa','Tổng hợp bán hàng','Tổng hợp mua hàng','Bảng cân đối tài khoản','F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định','Tổng hợp chi phí sản xuất kinh doanh','Sổ chi tiết tài khoản chi phí sản xuất','Tổng hợp nhập xuất kho theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng tổng hợp chi phí theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng kê phiếu nhập, phiếu xuất theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Báo cáo tổng hợp lãi lỗ theo công trình','Báo cáo chi tiết lãi lỗ theo công trình','Bảng tính giá thành']
        list_bao_cao_cha_duoc_hien_this = ['Hợp đồng','Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định','Giá thành']        
        for line in self.env['tien.ich.bao.cao'].with_context({'active_test':False}).search([]):
            line.write({'active': line.TEN_BAO_CAO in (list_bao_cao_con_duoc_hien_this if line.parent_id else list_bao_cao_cha_duoc_hien_this)})

    # Active lại các báo cáo bị inactive do v66
    def update_v67(self): 
        list_bao_cao_con_duoc_hien_this = ['Chi phí dự kiến theo đơn đặt hàng','Sổ chi tiết vật tư hàng hóa','Tổng hợp bán hàng','Tổng hợp mua hàng','Bảng cân đối tài khoản','F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định','Tổng hợp chi phí sản xuất kinh doanh','Sổ chi tiết tài khoản chi phí sản xuất','Tổng hợp nhập xuất kho theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng tổng hợp chi phí theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng kê phiếu nhập, phiếu xuất theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Báo cáo tổng hợp lãi lỗ theo công trình','Báo cáo chi tiết lãi lỗ theo công trình','Bảng tính giá thành']
        list_bao_cao_cha_duoc_hien_this = ['Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định','Giá thành']        
        for line in self.env['tien.ich.bao.cao'].with_context({'active_test':False}).search([]):
            line.write({'active': line.TEN_BAO_CAO in (list_bao_cao_con_duoc_hien_this if line.parent_id else list_bao_cao_cha_duoc_hien_this)})
    
    def update_v66(self): #Hiển thị báo cáo giá thành cho khách hàng
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Tổng hợp chi phí sản xuất kinh doanh','Sổ chi tiết tài khoản chi phí sản xuất','Tổng hợp nhập xuất kho theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng tổng hợp chi phí theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Bảng kê phiếu nhập, phiếu xuất theo đối tượng THCP, công trình, đơn hàng, hợp đồng','Báo cáo tổng hợp lãi lỗ theo công trình','Báo cáo chi tiết lãi lỗ theo công trình','Bảng tính giá thành']
        list_bao_cao_cha_duoc_hien_this = ['Giá thành']
        for line in self.env['tien.ich.bao.cao'].search([]):
            line.write({'active': line.TEN_BAO_CAO in (list_bao_cao_con_duoc_hien_this if line.parent_id else list_bao_cao_cha_duoc_hien_this)})
      
    def update_v65(self):
        for model in ('danh.muc.cong.trinh','danh.muc.doi.tuong.tap.hop.chi.phi'):
            for record in self.env[model].search([]):
                record.THU_TU_THEO_MA_PHAN_CAP = helper.String.convert_ma_phan_cap_to_thu_tu(record.MA_PHAN_CAP)
                record.BAC = len(record.MA_PHAN_CAP.split('/')) - 2
        
        #quanhm
        self.env['danh.muc.vat.tu.hang.hoa'].search([('NHOM_VTHH', '!=', None)])._compute_list()

        chung_tu_mua_hang_chi_tiet_ids = self.env['purchase.document.line'].search([])
        if chung_tu_mua_hang_chi_tiet_ids:
            for line in chung_tu_mua_hang_chi_tiet_ids:
                so_luong_theo_dvt_chinh = line.MA_HANG_ID.compute_SO_LUONG_THEO_DVT_CHINH(line.SO_LUONG,line.DVT_ID.id)
                line.write({'SO_LUONG_THEO_DVT_CHINH' : so_luong_theo_dvt_chinh})
        
        # Xóa sổ thuế thừa
        for pu in self.env['purchase.document'].search([('LOAI_HOA_DON', '!=', '1'),('state', '=', 'da_ghi_so')]):
            self.env['so.thue.chi.tiet'].search([('MODEL_CHUNG_TU', '=', 'purchase.document'), ('ID_CHUNG_TU', '=', pu.id)]).unlink()

    def update_v64(self):
        doi_tuong_tap_hop_chi_phi_ids = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
        if doi_tuong_tap_hop_chi_phi_ids:
            for line in doi_tuong_tap_hop_chi_phi_ids:
                chi_nhanh_id = self.get_chi_nhanh()
                line.write({'CHI_NHANH_ID' : chi_nhanh_id})


    def update_v62(self):
        # Tạm ẩn đi các wizard/action chưa hỗ trợ
        act_send_sms_action = self.env['ir.model.data'].search([('module','=','sms'),('name','=','send_sms_action')], limit=1)
        if act_send_sms_action:
            self.env['ir.actions.act_window'].browse(act_send_sms_action.res_id).unlink()
        # Chưa xóa được do còn liên quan đến email template
        # act_action_partner_mass_mail = self.env['ir.model.data'].search([('module','=','mail'),('name','=','action_partner_mass_mail')], limit=1)
        # if act_action_partner_mass_mail:
        #     self.env['ir.actions.act_window'].browse(act_action_partner_mass_mail.res_id).unlink()

        # Inactive menu theo thông tư 133
        if self.lay_che_do_ke_toan() == '48':
            self.env['ir.ui.menu'].search([('name','=','Kết chuyển chi phí')]).write({'groups_id': [(4, self.env.ref('base.group_no_one').id)]})
            # ref_sxltdg = self.env.ref('menu.menu_gia_thanh_ket_chuyen_chi_phi_sxltdg')
            # if ref_sxltdg:
            #     ref_sxltdg.unlink()
            # ref_sxlthstl = self.env.ref('menu.menu_gia_thanh_ket_chuyen_chi_phi_sxlthstl')
            # if ref_sxlthstl:
            #     ref_sxlthstl.unlink()
            # ref_cong_trinh = self.env.ref('menu.menu_gia_thanh_ket_chuyen_chi_phi_cong_trinh')
            # if ref_cong_trinh:
            #     ref_cong_trinh.unlink()
            # ref_don_hang = self.env.ref('menu.menu_gia_thanh_ket_chuyen_chi_phi_don_hang')
            # if ref_don_hang:
            #     ref_don_hang.unlink()
            # ref_hop_dong = self.env.ref('menu.menu_gia_thanh_ket_chuyen_chi_phi_hop_dong')
            # if ref_hop_dong:
            #     ref_hop_dong.unlink()
        
        # Remove các trường NGAY_HACH_TOAN_CK/NGAY_CHUNG_TU_CK
        for record in self.env['stock.ex.nhap.xuat.kho'].search([('type','=','CHUYEN_KHO')]):
            record.write({
                'NGAY_HACH_TOAN': record.NGAY_HACH_TOAN_CK,
                'NGAY_CHUNG_TU': record.NGAY_CHUNG_TU_CK,
            })



    def update_v63(self):
        doi_tuong_tap_hop_chi_phi_ids = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
        if doi_tuong_tap_hop_chi_phi_ids:
            for line in doi_tuong_tap_hop_chi_phi_ids:
                isparent = True if line.child_ids else False 
                line.write({'isparent' : isparent})

        cong_trinh_ids = self.env['danh.muc.cong.trinh'].search([])
        if cong_trinh_ids:
            for line in cong_trinh_ids:
                isparent = True if line.child_ids else False 
                line.write({'isparent' : isparent})

    def update_v61(self):
        nhap_xuat_kho_chi_tiet_ids = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].search([])
        if nhap_xuat_kho_chi_tiet_ids:
            for line in nhap_xuat_kho_chi_tiet_ids:
                don_vi_chuyen_doi = line.MA_HANG_ID.compute_ty_le_chuyen_doi(line.DVT_ID.id)
                toan_tu_quy_doi = line.MA_HANG_ID.compute_toan_tu_quy_doi(line.DVT_ID.id)
                line.write({'TY_LE_CHUYEN_DOI_RA_DVT_CHINH' : don_vi_chuyen_doi,'TOAN_TU_QUY_DOI' : toan_tu_quy_doi})

    def update_v60(self):
        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO', True)


    def update_v59(self):
        # Cập nhật lại sequence cho chứng từ mua hàng và danh mục vật tư hàng hóa
        # Giả định rằng sequence hiện tại được sắp xếp theo đúng thứ tự id
        for purchase in self.env['purchase.document'].search([]):
            seq = 0
            for line in purchase.CHI_TIET_IDS:
                seq += 1
                line.sequence = seq
        
        for product in self.env['danh.muc.vat.tu.hang.hoa'].search([('TINH_CHAT','=','1')]):
            seq = 0
            for line in product.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                seq += 1
                line.sequence = seq

    def update_v58(self):
        so_cai_ids = self.env['so.cai.chi.tiet'].search([])
        if so_cai_ids:
            for line in so_cai_ids:
                ten_loai_chung_tu = ''
                loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', int(line.LOAI_CHUNG_TU))],limit=1)
                if loai_chung_tu:
                    ten_loai_chung_tu = loai_chung_tu.REFTYPENAME
                line.write({'TEN_LOAI_CHUNG_TU' : ten_loai_chung_tu})


    def update_v57(self):
        ref_view = self.env.ref('web.webclient_bootstrap')
        if ref_view:
            ref_view.arch_db = ref_view.arch_db \
                .replace('(function(h,o,t,j,a,r){','') \
				.replace('h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};','') \
				.replace('h._hjSettings={hjid:1145747,hjsv:6};','') \
				.replace('h._hjSettings={hjid:1145744,hjsv:6};','') \
				.replace("a=o.getElementsByTagName('head')[0];",'') \
				.replace("r=o.createElement('script');r.async=1;",'') \
				.replace('r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;','') \
				.replace('a.appendChild(r);','') \
				.replace("})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');",'') \
    
    def update_v56(self):
        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_SO_CONG', 1)

    def update_v55(self):
        # Thêm config
       self.env['ir.config_parameter'].sudo().set_param('he_thong.CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN', 'LAY_THEO_SO_TIEN_LUONG_PHAI_TRA_TREN_BANG_LUONG')

    def update_v54(self):
        # Thêm config
       self.env['ir.config_parameter'].sudo().set_param('he_thong.LUONG_CO_BAN_DUA_TREN', 'LUONG_THOA_THUAN')

    def update_v53(self):
        ref_view = self.env.ref('web.webclient_bootstrap')
        if ref_view:
            ref_view.arch_db = ref_view.arch_db.replace("hjid:1145744","hjid:1145747")

    def update_v52(self):# https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3393/
        self.env['base_import_ex.import'].auto_import('Cấu hình lãi lỗ cho công trình, hóa đơn, đơn hàng.xml')
        self.env['base_import_ex.import'].auto_import('Cấu hình lãi lỗ cho công trình, hóa đơn, đơn hàng công thức.xml')

    def update_v51(self):
        for sa_return in self.env['sale.ex.tra.lai.hang.ban'].search([('CHUNG_TU_BAN_HANG', '!=', None)]):
            ty_gia = sa_return.TY_GIA or 1
            for line in sa_return.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                line.write({
                    'THANH_TIEN_QUY_DOI': line.THANH_TIEN * ty_gia,
                    'TIEN_CHIET_KHAU_QUY_DOI': line.TIEN_CHIET_KHAU * ty_gia,
                    'TIEN_THUE_GTGT_QUY_DOI': line.TIEN_THUE_GTGT * ty_gia,
                })
            sa_return.write({
                'TONG_TIEN_HANG_QĐ': sa_return.TONG_TIEN_HANG * ty_gia,
                'TONG_CHIET_KHAU_QĐ': sa_return.TONG_CHIET_KHAU * ty_gia,
                'TIEN_THUE_GTGT_QĐ': sa_return.TIEN_THUE_GTGT * ty_gia,
                'TONG_TIEN_THANH_TOAN_QĐ': sa_return.TONG_TIEN_THANH_TOAN * ty_gia,
            })
            if sa_return.state == 'da_ghi_so':
                sa_return.bo_ghi_so()
                sa_return.action_ghi_so()

        for pu_return in self.env['purchase.ex.tra.lai.hang.mua'].search([('CHUNG_TU_MUA_HANG', '!=', None)]):
            ty_gia = pu_return.TY_GIA or 1
            for line in pu_return.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                line.write({
                    'THANH_TIEN_QUY_DOI': line.THANH_TIEN * ty_gia,
                    'TIEN_THUE_GTGT_QUY_DOI': line.TIEN_THUE_GTGT * ty_gia,
                })
            pu_return.write({
                'TONG_TIEN_HANG_QĐ': pu_return.TONG_TIEN_HANG * ty_gia,
                'TIEN_THUE_GTGT_QĐ': pu_return.TIEN_THUE_GTGT * ty_gia,
                'TONG_TIEN_THANH_TOAN_QĐ': pu_return.TONG_TIEN_THANH_TOAN * ty_gia,
            })
            if pu_return.state == 'da_ghi_so':
                pu_return.bo_ghi_so()
                pu_return.action_ghi_so()
    
    def update_v50(self):
        khoan_muc_cp_ids = self.env['danh.muc.khoan.muc.cp'].search([])
        if khoan_muc_cp_ids:
            for line in khoan_muc_cp_ids:
                la_tong_hop = True if line.child_ids else False 
                line.write({'LA_TONG_HOP' : la_tong_hop})

    def update_v49(self):        
        kiem_ke_vat_tu_hang_hoas = self.env['stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form'].search([])
        for kiem_ke_vat_tu_hang_hoa in kiem_ke_vat_tu_hang_hoas:
            if not kiem_ke_vat_tu_hang_hoa.LOAI_CHUNG_TU :
                kiem_ke_vat_tu_hang_hoa.write({'LOAI_CHUNG_TU' : 2060})

    def update_v48(self):
        for record in self.env['stock.ex.nhap.xuat.kho'].search([('SOURCE_ID','!=',None)]):
            need_maintain = False
            for line in record.CHI_TIET_IDS:
                if line.SALE_DOCUMENT_LINE_IDS:
                    need_maintain = True
                    line.write({
                        'TK_NO_ID': line.SALE_DOCUMENT_LINE_IDS[0].TK_GIA_VON_ID.id,
                        'TK_CO_ID': line.SALE_DOCUMENT_LINE_IDS[0].TK_KHO_ID.id,
                    })
                elif line.TRA_LAI_HANG_BAN_CHI_TIET_IDS:
                    need_maintain = True
                    line.write({
                        'TK_NO_ID': line.TRA_LAI_HANG_BAN_CHI_TIET_IDS[0].TK_KHO_ID.id,
                        'TK_CO_ID': line.TRA_LAI_HANG_BAN_CHI_TIET_IDS[0].TK_GIA_VON_ID.id,
                    })
            if need_maintain and record.state=='da_ghi_so':
                line.bo_ghi_so()
                line.action_ghi_so()
    
    def update_v47(self):
        vat_tu_hang_hoas = self.env['danh.muc.vat.tu.hang.hoa'].search([])
        if vat_tu_hang_hoas:
            for vthh in vat_tu_hang_hoas:
                # cập nhật lại trường liên lưu lại list nhóm vthh
                if vthh.NHOM_VTHH:
                    ten_nhom_vthh = ''
                    arr_list_ten_nhom_vthh = []
                    for line in vthh.NHOM_VTHH:
                        arr_list_ten_nhom_vthh.append(line.TEN)
                    ten_nhom_vthh = ";".join(arr_list_ten_nhom_vthh)
                    vthh.write({'LIST_TEN_NHOM_VTHH': ten_nhom_vthh})

    def update_v46(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_hop_dong_ban.xml')
    
    def update_v45(self):
        # Thay đổi lại hệ thống kế toán
        acc_len = self.env['danh.muc.he.thong.tai.khoan'].search_count([])
        if acc_len > 200:# and self.lay_che_do_ke_toan()=='0': # Chế độ 200
            self.env['ir.config_parameter'].sudo().set_param('he_thong.CHE_DO_KE_TOAN', '15')
        else:#if acc_len < 200 and self.lay_che_do_ke_toan()=='15': # Chế độ 133
            self.env['ir.config_parameter'].sudo().set_param('he_thong.CHE_DO_KE_TOAN', '48')
        # else:
        #     raise ValidationError("Không xác định được chế độ kế toán")

    def update_v44(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_hop_dong_ban_ben_a_mua.xml')

    def update_v43(self):
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO', 2)
                      
    def update_v42(self):
        # Mạnh thêm auto_import lại do các mẫu in này bị miss trên chamnew nên import lại cho chắc
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_chi_co_so_luong.xml')
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_bao_gom_nguyen_vat_lieu.xml')
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_du_kien_chi_phi.xml')

    def update_v41(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_du_kien_chi_phi.xml')
    
    def update_v40(self):
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_chi_co_so_luong.xml')
        self.env['base_import_ex.import'].auto_import('danh_sach_mau_in_don_dat_hang_bao_gom_nguyen_vat_lieu.xml')

    def update_v39(self):
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao_chi_phi_du_kien_theo_don_dat_hang.xml')
       # Loại bỏ báo cáo thừa
        # list_bao_cao_con_duoc_hien_this = ['Chi phí dự kiến theo đơn đặt hàng','Sổ chi tiết vật tư hàng hóa','Tổng hợp bán hàng','Tổng hợp mua hàng','Bảng cân đối tài khoản','F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        # list_bao_cao_cha_duoc_hien_this = ['Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        # for line in self.env['tien.ich.bao.cao'].search([]):
        #     line.write({'active': line.TEN_BAO_CAO in (list_bao_cao_con_duoc_hien_this if line.parent_id else list_bao_cao_cha_duoc_hien_this)})

    
    def update_v38(self):
       chung_tu_ban_hang_chi_tiet_ids = self.env['sale.document.line'].search([])
       for ct_ban_hang_chi_tiet in chung_tu_ban_hang_chi_tiet_ids:
           ct_ban_hang_chi_tiet.write({'LA_HANG_KHUYEN_MAI' : False})
    def update_v37(self):
        # Thêm config
       self.env['ir.config_parameter'].sudo().set_param('he_thong.PHUONG_PHAP_TINH_THUE', 'PHUONG_PHAP_KHAU_TRU')

    #def update_v36(self):
    #    # Thêm config
    #   self.env['ir.config_parameter'].sudo().set_param('he_thong.PHUONG_PHAP_TINH_THUE', False)

    def update_v35(self):
        dict_don_dat_hang = {}
        chung_tu_ban_hang_ids = self.env['sale.document'].search([('CHON_LAP_TU_ID', '!=', None)])
        for chung_tu_ban_hang in chung_tu_ban_hang_ids:
            if chung_tu_ban_hang.CHON_LAP_TU_ID and chung_tu_ban_hang.CHON_LAP_TU_ID._name == 'account.ex.don.dat.hang':
                dict_don_dat_hang = {}
                for don_dat_hang_chi_tiet in chung_tu_ban_hang.CHON_LAP_TU_ID.ACCOUNT_EX_DON_DAT_HANG_CHI_TIET_IDS:
                    if don_dat_hang_chi_tiet.MA_HANG_ID.id not in dict_don_dat_hang:
                        dict_don_dat_hang[don_dat_hang_chi_tiet.MA_HANG_ID.id] = don_dat_hang_chi_tiet.id
                
                if chung_tu_ban_hang.SALE_DOCUMENT_LINE_IDS:
                    for ct_ban_hang_chi_tiet in chung_tu_ban_hang.SALE_DOCUMENT_LINE_IDS:
                        if ct_ban_hang_chi_tiet.MA_HANG_ID.id in dict_don_dat_hang:
                            if not ct_ban_hang_chi_tiet.DON_DAT_HANG_CHI_TIET_ID:
                                ct_ban_hang_chi_tiet.write({'DON_DAT_HANG_CHI_TIET_ID' : dict_don_dat_hang[ct_ban_hang_chi_tiet.MA_HANG_ID.id]})
                chon_lap_tu = str(chung_tu_ban_hang.CHON_LAP_TU_ID._name) + ',' + str(chung_tu_ban_hang.CHON_LAP_TU_ID.id)
                chung_tu_ban_hang.write({'CHON_LAP_TU_ID' : chon_lap_tu})

    def update_v34(self):
        self.env['ir.config_parameter'].sudo().set_param('he_thong.CO_PHAT_SINH_BAN_HANG_SAU_THUE', False)
        # Cập nhật các chứng từ chi tiết thiếu đối tượng
        for record in self.env['purchase.document'].search([]):
            record.CHI_TIET_IDS.write({'DOI_TUONG_ID': record.DOI_TUONG_ID.id})

    def update_v33(self):
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY', 'BINH_QUAN_CUOI_KY')
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO', 'BINH_QUAN_CUOI_KY')
        self.env['ir.config_parameter'].sudo().set_param('he_thong.CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB', True)
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_CUA_HE_SO_TY_LE', 2)

    def update_v32(self):
        #Cập nhật lại tổng tiền  model(account.ex.phieu.thu.chi)
        phieu_thu_chi = self.env['account.ex.phieu.thu.chi'].search([])
        if phieu_thu_chi:
            for ptc in phieu_thu_chi:
                ptc.tinhtongtien()            
                ptc.write({
                            'SO_TIEN_1':ptc.SO_TIEN_1,                          
                        })
        self.env['ir.config_parameter'].sudo().set_param('he_thong.KIEU_HIEN_THI_TIEU_DE', 'CHUAN')


    # def update_v31(self):
    #     # Thêm config
    #    self.env['ir.config_parameter'].sudo().set_param('he_thong.PHUONG_PHAP_TINH_THUE', False)

    def update_v30(self):
        # Xóa các chứng từ xuất kho chi tiết thừa tạo ra khi cập nhật chứng từ bán hàng chi tiết
        self.env.cr.execute("""DELETE FROM stock_ex_nhap_xuat_kho_chi_tiet WHERE "NHAP_XUAT_ID" ISNULL;""")

    def update_v29(self):
           # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI', 0)
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_TY_GIA', 2)


    def update_v28(self):
        so_kho_ids = self.env['so.kho.chi.tiet'].search([])
        if so_kho_ids:
            for so_kho in so_kho_ids:
                so_kho.write({'STT_LOAI_CHUNG_TU' : so_kho.NGAY_HACH_TOAN})

        # Cập nhật tài khoản chi tiết theo Đối tượng/Ngân hàng
        if not self.env['danh.muc.he.thong.tai.khoan'].search([('TAI_KHOAN_NGAN_HANG','=',True)],limit=1):
            self.update_v06()

    def update_v27(self):
        #Cập nhật lại LA_PHIEU_MUA_HANG model(chứng từ mua hàng)
        chung_tu_mua_hang = self.env['purchase.document'].search([])
        if chung_tu_mua_hang:
            for ctmh in chung_tu_mua_hang:
                if not ctmh.LA_PHIEU_MUA_HANG: 
                    ctmh.write({'LA_PHIEU_MUA_HANG':False})



    def update_v25(self):
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Sổ chi tiết vật tư hàng hóa','Tổng hợp bán hàng','Tổng hợp mua hàng','Bảng cân đối tài khoản','F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        for line in self.env['tien.ich.bao.cao'].search([]):
            line.write({'active': line.TEN_BAO_CAO in (list_bao_cao_con_duoc_hien_this if line.parent_id else list_bao_cao_cha_duoc_hien_this)})
      
      
    def update_v26(self):
        # Import lại báo cáo tài chính FRTemplate
        self.env.cr.execute("""
            DELETE FROM tien_ich_bao_cao_tai_chinh_chi_tiet;
            DELETE FROM tien_ich_bao_cao_tai_chinh_chi_tiet_mac_dinh;
            DELETE FROM ir_model_data WHERE model IN ('tien.ich.bao.cao.tai.chinh.chi.tiet','tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh');
            DELETE FROM tien_ich_xay_dung_cong_thuc_loai_chi_tieu_tong_hop;
            DELETE FROM tien_ich_xay_dung_cong_thuc_loai_chi_tieu_chi_tiet;
            DELETE FROM tien_ich_xay_dung_cong_thuc_mac_dinh;
            DELETE FROM tien_ich_xdct_loai_chi_tieu_chi_tiet_mac_dinh;
        """)
        che_do_kt = '133' if self.lay_che_do_ke_toan() == '48' else '200'
        self.env['base_import_ex.import'].auto_import('FRTemplate_%s.xml' % che_do_kt)
        self.env['base_import_ex.import'].auto_import('FRTemplateDefault_%s.xml' % che_do_kt)

    def update_v24(self):
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2620
        don_dat_hang_ids = self.env['account.ex.don.dat.hang'].search([])
        for don_dat_hang in don_dat_hang_ids:
            if don_dat_hang.currency_id.MA_LOAI_TIEN == 'VND':
                don_dat_hang.write({'TY_GIA' : 1})
        
        # Cập nhật field THUOC_HE_THONG (import từ MS)
        role_ids = self.env['ir.model.data'].search([('model', '=', 'he.thong.vai.tro.va.quyen.han')]).mapped('res_id')
        self.env['he.thong.vai.tro.va.quyen.han'].browse(role_ids).write({'THUOC_HE_THONG': True})
        # Cập nhật lại field is_admin cho res_users
        admin_role = self.env['he.thong.vai.tro.va.quyen.han'].search([('MA_VAI_TRO', '=', 'Admin')], limit=1)
        if admin_role:
            admin_role.user_ids.write({'is_admin': True})

    def update_v23(self):
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Bảng cân đối tài khoản','F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})
    def update_v22(self):
        # Cập nhật các hóa đơn thiếu thông tin tên đối tượng
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2767/
        # Hóa đơn mua hàng
        purchase_invoices = self.env['purchase.ex.hoa.don.mua.hang'].search([('TEN_NHA_CUNG_CAP','=',None),('SOURCE_ID','!=',None)])
        for invoice in purchase_invoices:
            ref_model = invoice.SOURCE_ID and invoice.SOURCE_ID._name
            if ref_model == 'purchase.document':
                invoice.write({'TEN_NHA_CUNG_CAP': invoice.SOURCE_ID.TEN_DOI_TUONG})
            elif ref_model == 'purchase.ex.giam.gia.hang.mua':
                invoice.write({'TEN_NHA_CUNG_CAP': invoice.SOURCE_ID.TEN_NHA_CUNG_CAP})
            elif ref_model == 'sale.ex.tra.lai.hang.ban':
                invoice.write({'TEN_NHA_CUNG_CAP': invoice.SOURCE_ID.TEN_KHACH_HANG})
        # Hóa đơn bán hàng
        sale_invoices = self.env['sale.ex.hoa.don.ban.hang'].search([('TEN_KHACH_HANG','=',None),('SOURCE_ID','!=',None)])
        for invoice in sale_invoices:
            ref_model = invoice.SOURCE_ID and invoice.SOURCE_ID._name
            if ref_model in ('sale.document','sale.ex.giam.gia.hang.ban'):
                invoice.write({'TEN_KHACH_HANG': invoice.SOURCE_ID.TEN_KHACH_HANG})
            elif ref_model == 'purchase.ex.tra.lai.hang.mua':
                invoice.write({'TEN_KHACH_HANG': invoice.SOURCE_ID.TEN_NHA_CUNG_CAP})
        # Chuyển đổi cột LY_DO_THU_CHI sang DIEN_GIAI
        query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='sale_document' and column_name='LY_DO_THU_CHI';
        """
        if len(self.execute(query)):
            self.env.cr.execute("""UPDATE sale_document SET "DIEN_GIAI"=sale_document."LY_DO_THU_CHI" WHERE "THU_TIEN_NGAY"=True;""")

    def update_v21(self):
        chung_tu_bhs = self.env['sale.document'].search([])
        if chung_tu_bhs:
            for ct_bh in chung_tu_bhs:
                if ct_bh.TONG_TIEN_THANH_TOAN_QĐ != ct_bh.TONG_TIEN_THANH_TOAN:
                    ct_bh.write({'TONG_TIEN_THANH_TOAN_QĐ': float_round(ct_bh.TONG_TIEN_THANH_TOAN*ct_bh.TY_GIA,0)})
                ct_bh.write({'TONG_TIEN_THANH_TOAN_QĐ': float_round(ct_bh.TONG_TIEN_THANH_TOAN_QĐ,0)})

        hoa_don_ban_hangs = self.env['sale.ex.hoa.don.ban.hang'].search([])
        if hoa_don_ban_hangs:
            for hd_bh in hoa_don_ban_hangs:
                if hd_bh.SOURCE_ID:
                    if hd_bh.SOURCE_ID.TONG_TIEN_THANH_TOAN_QĐ != hd_bh.TONG_TIEN_THANH_TOAN_QD:
                        hd_bh.write({'TONG_TIEN_THANH_TOAN_QD': float_round(hd_bh.SOURCE_ID.TONG_TIEN_THANH_TOAN_QĐ,0)})

        self.env['base_import_ex.import'].auto_import('mau_so_hoa_don_nhap_tay.xml')
        # mau_so_hds = self.env['danh.muc.mau.so.hd'].with_context(active_test=True).search([])
        # if mau_so_hds:
        #     for mau_so in mau_so_hds:
        #         if mau_so.active != True:
        #             mau_so.write({'active' : False})
        # Sửa warning loại tiền not null
        self.env.cr.execute(""" 
            UPDATE res_currency SET "TY_GIA_QUY_DOI"=0.1 WHERE "TY_GIA_QUY_DOI" ISNULL;
            UPDATE res_currency SET "TEN_LOAI_TIEN"=res_currency.currency_unit_label WHERE "TEN_LOAI_TIEN" ISNULL; 
        """)
        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO', False)
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_DON_GIA', 0)
        self.env['ir.config_parameter'].sudo().set_param('he_thong.CONG_GOP_DON_GIA_DVT_MA_HANG', False)
        # Update các chứng từ xuất kho chi tiết chưa có KHO_ID
        sd_lines = self.env['sale.document.line'].search([('KHO_ID','!=',None)])
        for sdl in sd_lines:
            for xk_line in sdl.PHIEU_XUAT_CHI_TIET_IDS:
                if not xk_line.KHO_ID:
                    xk_line.write({'KHO_ID': sdl.KHO_ID.id})

        so_du_tai_khoan_chi_tiet_ids = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([])
        if so_du_tai_khoan_chi_tiet_ids:
            for so_du_chi_tiet in so_du_tai_khoan_chi_tiet_ids:
                ty_gia = 1
                if so_du_chi_tiet.DU_NO > 0 or so_du_chi_tiet.DU_NO_NGUYEN_TE > 0:
                    if so_du_chi_tiet.DU_NO_NGUYEN_TE > 0:
                        ty_gia = so_du_chi_tiet.DU_NO/so_du_chi_tiet.DU_NO_NGUYEN_TE
                elif so_du_chi_tiet.DU_CO > 0 or so_du_chi_tiet.DU_CO_NGUYEN_TE > 0:
                    if so_du_chi_tiet.DU_CO_NGUYEN_TE > 0:
                        ty_gia = so_du_chi_tiet.DU_CO/so_du_chi_tiet.DU_CO_NGUYEN_TE
                so_du_chi_tiet.write({'TY_GIA': ty_gia})

        he_thong_tai_khoan_ids = self.env['danh.muc.he.thong.tai.khoan'].search([])
        if he_thong_tai_khoan_ids:
            for tai_khoan in he_thong_tai_khoan_ids:
                tai_khoan.write({'CHI_TIET_THEO_DOI_TUONG' : tai_khoan.DOI_TUONG,'CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG' : tai_khoan.TAI_KHOAN_NGAN_HANG})

    def update_v19(self):
        hoa_don_mua_hangs = self.env['purchase.ex.hoa.don.mua.hang'].search([])
        for hoa_don in hoa_don_mua_hangs:
            if hoa_don.SOURCE_ID:
                hoa_don.write({'NHAN_HOA_DON': True})
                if hoa_don.SOURCE_ID._name == 'sale.ex.tra.lai.hang.ban':
                    loai_chung_tu = 3403
                elif hoa_don.SOURCE_ID._name == 'purchase.ex.giam.gia.hang.mua':
                    loai_chung_tu = 3402
                else:
                    loai_chung_tu = 3400
                hoa_don.write({'LOAI_CHUNG_TU': loai_chung_tu})

            if hoa_don.HOA_DON_CHI_TIET_IDS:
                for hoa_don_chi_tiet in hoa_don.HOA_DON_CHI_TIET_IDS:
                    if hoa_don_chi_tiet.ID_CHUNG_TU_GOC:
                        hoa_don_chi_tiet.ID_CHUNG_TU_GOC.write({'HOA_DON_MUA_HANG_ID': hoa_don_chi_tiet.HOA_DON_MUA_HANG_ID.id})

        hoa_don_ban_hangs = self.env['sale.ex.hoa.don.ban.hang'].search([])
        if hoa_don_ban_hangs:
            for hoa_don_bh in hoa_don_ban_hangs:
                if hoa_don_bh.HOA_DON=='BAN_HANG_HOA_DICH_VU_TRONG_NUOC':
                    loai_chung_tu_bh = 3560
                elif hoa_don_bh.HOA_DON=='BAN_HANG_XUAT_KHAU':
                    loai_chung_tu_bh = 3561
                elif hoa_don_bh.HOA_DON=='BAN_HANG_DAI_LY_BAN_DUNG_GIA':
                    loai_chung_tu_bh = 3562
                else:
                    loai_chung_tu_bh = 3563
                if hoa_don_bh.SOURCE_ID:
                    if hoa_don_bh.SOURCE_ID._name == 'purchase.ex.tra.lai.hang.mua':
                        loai_chung_tu_bh = 3564
                    elif hoa_don_bh.SOURCE_ID._name == 'sale.ex.giam.gia.hang.ban':
                        loai_chung_tu_bh = 3565
                    elif hoa_don_bh.SOURCE_ID._name == 'sale.document':
                        if hoa_don_bh.SOURCE_ID.LOAI_NGHIEP_VU == 'TRONG_NUOC':
                            loai_chung_tu_bh = 3560
                        elif hoa_don_bh.SOURCE_ID.LOAI_NGHIEP_VU == 'XUAT_KHAU':
                            loai_chung_tu_bh = 3561
                        elif hoa_don_bh.SOURCE_ID.LOAI_NGHIEP_VU == 'DAI_LY':
                            loai_chung_tu_bh = 3562
                        elif hoa_don_bh.SOURCE_ID.LOAI_NGHIEP_VU == 'UY_THAC':
                            loai_chung_tu_bh = 3563
                hoa_don_bh.write({'LOAI_CHUNG_TU': loai_chung_tu_bh})

        so_thues = self.env['so.thue.chi.tiet'].search([])
        if so_thues:
            for st in so_thues:
                if st.CHI_TIET_MODEL in ('sale.ex.tra.lai.hang.ban.chi.tiet','sale.ex.chi.tiet.hoa.don.ban.hang','sale.document.line','sale.ex.chi.tiet.giam.gia.hang.ban'):
                    st.write({'DS_LOAI_BANG': 0})
                else:
                    st.write({'DS_LOAI_BANG': 1})
        
        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN', '0')

    def update_v18(self):
        #import báo cáo
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2538/
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')

        chung_tu_mua_hang_chi_tiet = self.env['purchase.document.line'].search([]) #Mạnh sửa bug 2529
        if chung_tu_mua_hang_chi_tiet:
            for ct in chung_tu_mua_hang_chi_tiet:
                don_gia_quy_doi = ct.DON_GIA * ct.TY_GIA
                ct.write({'DON_GIA_QUY_DOI': don_gia_quy_doi,
                })

    def update_v17(self):
        don_dat_hang_chi_tiet = self.env['account.ex.don.dat.hang.chi.tiet'].search([])
        if don_dat_hang_chi_tiet:
            for ct in don_dat_hang_chi_tiet:
                ct.write({'MA_KHO_ID': ct.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                          'DON_VI_ID' : ct.DON_DAT_HANG_CHI_TIET_ID.NV_BAN_HANG_ID.DON_VI_ID.id,
                })
        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_SO_LUONG', 2)
        self.env['base_import_ex.import'].auto_import('khoang_thoi_gian_theo_doi_no.xml')

        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2499/
        menu = self.env.ref('menu.menu_tien_ich_nhap_khau_du_lieu_ban_dau_tu_excel', False)
        if menu:
            menu.write({'groups_id': [[5]]})
    def update_v16(self):
        ton_kho_vthhs = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([])
        if ton_kho_vthhs:
            for vthh in ton_kho_vthhs:
                ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
                if ngay_bat_dau_nam_tai_chinh:
                    ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
                    ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
                    ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')

                    vthh.write({'NGAY_HACH_TOAN': ngay_hach_toan_str})
        
        doi_tuongs = self.env['res.partner'].search([])
        if doi_tuongs:
            for dt in doi_tuongs:
                # cập nhật lại trường liên lưu lại list nhóm kh ncc
                if dt.NHOM_KH_NCC_ID:
                    ma_pc_nhom_khach_hang = ''
                    for line in dt.NHOM_KH_NCC_ID:
                        ma_pc_nhom_khach_hang += ";" + line.MA_PHAN_CAP
                    ma_pc_nhom_khach_hang += ";"
                    dt.write({'LIST_MPC_NHOM_KH_NCC': ma_pc_nhom_khach_hang})
                    

        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG', True)

    def update_v15(self):
        ton_kho_vthhs = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([])
        if ton_kho_vthhs:
            for vthh in ton_kho_vthhs:
                vthh.write({'LOAI_CHUNG_TU': 611})
    def update_v14(self):
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['F01-DNN: Bảng cân đối tài khoản','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra (Mẫu quản trị)','Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ mua vào (Mẫu quản trị)','B03-DN-GT: Báo cáo lưu chuyển tiền tệ (PP gián tiếp)','B03-DN: Báo cáo lưu chuyển tiền tệ (PP trực tiếp)','B02-DN: Báo cáo kết quả hoạt động kinh doanh','B01-DN: Bảng cân đối kế toán','Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Bảng cân đối tài khoản','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Thuế','Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})
    
    def update_v13(self):
        # self.env['he.thong.vai.tro.va.quyen.han'].action_reset()
        # self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Bảng cân đối tài khoản','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})        
    def update_v12(self):
        # self.env['he.thong.vai.tro.va.quyen.han'].action_reset()
        # self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Sổ chi tiết tài khoản theo đối tượng','Sổ chi tiết các tài khoản','Tình hình thực hiện đơn đặt hàng','Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Bảng cân đối tài khoản','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})
    def update_v11(self):
        # self.env['he.thong.vai.tro.va.quyen.han'].action_reset()
        # self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Bảng cân đối tài khoản','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                # line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})

    def update_v10(self):
        self.env['he.thong.vai.tro.va.quyen.han'].action_reset()
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Phân tích công nợ phải thu theo tuổi nợ','Tổng hợp công nợ nhân viên','Tổng hợp công nợ phải trả nhà cung cấp','Chi tiết công nợ phải thu khách hàng','Tổng hợp công nợ phải thu khách hàng','Bảng cân đối tài khoản','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Tổng hợp','Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                # line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})
        
        lap_rap_thao_dos = self.env['stock.ex.lap.rap.thao.do'].search([])
        if lap_rap_thao_dos:
            for lr in lap_rap_thao_dos:
                if lr.LAP_RAP_THAO_DO == 'LAP_RAP':
                    lr.write({'LOAI_CHUNG_TU': 2050})
                elif lr.LAP_RAP_THAO_DO == 'THAO_DO':
                    lr.write({'LOAI_CHUNG_TU': 2051})
    
    def update_v09(self):
        chung_tu_mua_hang_chi_tiets = self.env['purchase.document.line'].search([])
        if chung_tu_mua_hang_chi_tiets:
            for chi_tiet in chung_tu_mua_hang_chi_tiets:
                chung_tu_ban_hang = self.env['purchase.document'].search([('id', '=', chi_tiet.order_id.id)],limit=1)
                if chung_tu_ban_hang.LOAI_CHUNG_TU_MH in ('trong_nuoc_khong_qua_kho','nhap_khau_khong_qua_kho') :
                    chi_tiet.write({'KHO_ID': False})
        
        ton_kho_vthhs = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([])
        if ton_kho_vthhs:
            for vthh in ton_kho_vthhs:
                vthh.write({'LOAI_CHUNG_TU': 610})

        chung_tu_ban_hangs = self.env['sale.document'].search([])
        if chung_tu_ban_hangs:
            for chung_tu in chung_tu_ban_hangs:
                if chung_tu.LAP_KEM_HOA_DON == False:
                    chung_tu.write({'NGAY_HOA_DON': False,'SO_HOA_DON' : False})

        bao_gias = self.env['sale.ex.bao.gia'].search([])
        if bao_gias:
            for bao_gia in bao_gias:
                bao_gia.write({'LOAI_CHUNG_TU': 3510})

    def update_v08(self):
        self.env['base_import_ex.import'].auto_import('Danh mục hành chính.xml')
        self.env['base_import_ex.import'].auto_import('tien_ich_bao_cao.xml')
        # Loại bỏ báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Bảng cân đối tài khoản','Tổng hợp tồn kho','Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Báo cáo tài chính','Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])  
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                # line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})

        doi_tru_chi_tiets = self.env['sale.ex.doi.tru.chi.tiet'].search([])
        if doi_tru_chi_tiets:
            for doi_tru in doi_tru_chi_tiets:
                if doi_tru.TAI_KHOAN_ID:
                    doi_tru.write({'MA_TAI_KHOAN': doi_tru.TAI_KHOAN_ID.SO_TAI_KHOAN})

    def update_v07(self):
        self.env['base_import_ex.import'].auto_import('Mẫu số HĐ.xml') # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2176

    def update_v06(self):
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2140
        che_do_kt = self.lay_che_do_ke_toan()
        if che_do_kt == '48': # Thông tư 133
            self.env['base_import_ex.import'].auto_import('Hệ thống tài khoản TT133.xml')
        elif che_do_kt == '15': # Thông tư 200
            self.env['base_import_ex.import'].auto_import('Hệ thống tài khoản TT200.xml')
            
        # Loại bỏ những báo cáo thừa
        list_bao_cao_con_duoc_hien_this = ['Sổ kế toán chi tiết quỹ tiền mặt','Sổ tiền gửi ngân hàng','Sổ chi tiết bán hàng','Sổ chi tiết mua hàng','Chi tiết công nợ phải trả nhà cung cấp','S10-DN: Sổ chi tiết vật liệu, công cụ (sản phẩm, hàng hóa)','Sổ theo dõi công cụ dụng cụ','S21-DN: Sổ tài sản cố định']
        list_bao_cao_cha_duoc_hien_this = ['Quỹ','Ngân hàng','Bán hàng','Mua hàng','Kho','Công cụ dụng cụ','Tài sản cố định']
        he_thong_bao_cao = self.env['tien.ich.bao.cao'].search([])
        if he_thong_bao_cao:
            for line in he_thong_bao_cao:
                # line.write({'active': True})
                if not line.parent_id:
                    check_bao_cao_cha = line.TEN_BAO_CAO not in list_bao_cao_cha_duoc_hien_this
                    if check_bao_cao_cha ==True:
                        line.write({'active': False})
                else :
                    Check_bao_cao_con = line.TEN_BAO_CAO not in list_bao_cao_con_duoc_hien_this
                    if Check_bao_cao_con == True:
                        line.write({'active': False})

        # Thêm config
        self.env['ir.config_parameter'].sudo().set_param('he_thong.PHAN_THAP_PHAN_SO_LUONG', 2)
        

    def update_v05(self):
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1979
        self._cr.execute("""UPDATE ir_sequence SET padding=5,prefix='XK' WHERE code='stock_ex_phieu_nhap_xuat_kho_SO_CHUNG_TU_XUAT_KHO' AND padding=7 AND prefix=''""")
        self.env['base_import_ex.import'].auto_import('BANK_133.xml')

        # Cập nhật trường loại chứng từ trong đơn mua hàng
        don_mua_hangs = self.env['purchase.ex.don.mua.hang'].search([])
        if don_mua_hangs:
            for dmh in don_mua_hangs:
                # if not hoa_don.LOAI_CHUNG_TU:
                dmh.write({'LOAI_CHUNG_TU': 301 })

        # Cập nhật trường loại chứng từ trong đơn đặt hàng
        don_dat_hangs = self.env['account.ex.don.dat.hang'].search([])
        if don_dat_hangs:
            for ddh in don_dat_hangs:
                # if not hoa_don.LOAI_CHUNG_TU:
                ddh.write({'LOAI_CHUNG_TU': 3520 })

        sdtkct_theo_hoa_don = self.env['account.ex.sdtkct.theo.hoa.don'].search([])
        if sdtkct_theo_hoa_don:
            for sdtk in sdtkct_theo_hoa_don:
                sdtk_chi_tiet = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('id', '=', sdtk.SO_DU_TAI_KHOAN_CHI_TIET_ID.id)],limit=1)
                if sdtk_chi_tiet:
                    if sdtk_chi_tiet.currency_id.MA_LOAI_TIEN == 'VND':
                        sdtk.write({'SO_THU_TRUOC_NGUYEN_TE': sdtk.SO_THU_TRUOC,
                                    'SO_CON_PHAI_THU_NGUYEN_TE': sdtk.SO_CON_PHAI_THU,
                                    'GIA_TRI_HOA_DON_NGUYEN_TE': sdtk.GIA_TRI_HOA_DON,
                         })

        so_du_tai_khoan_cts = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([])
        if so_du_tai_khoan_cts:
            for sdtk in so_du_tai_khoan_cts:
                if not sdtk.LOAI_CHUNG_TU:
                    sdtk.write({'LOAI_CHUNG_TU': '610' })

        doi_tuongs = self.env['res.partner'].search([])
        if doi_tuongs:
            for dt in doi_tuongs:
                # cập nhật lại trường liên lưu lại list nhóm kh ncc
                if dt.NHOM_KH_NCC_ID:
                    # ma_pc_nhom_khach_hang = ''
                    # for line in dt.NHOM_KH_NCC_ID:
                    #     ma_pc_nhom_khach_hang += "; " + line.MA_PHAN_CAP
                    # ma_pc_nhom_khach_hang += "; "
                    # dt.write({'LIST_MPC_NHOM_KH_NCC': ma_pc_nhom_khach_hang})
                    
                    ma_nhom_khach_hang = ''
                    for line in dt.NHOM_KH_NCC_ID:
                        if ma_nhom_khach_hang == '':
                            ma_nhom_khach_hang = line.MA
                        else:
                            ma_nhom_khach_hang += "; " + line.MA
                    dt.write({'LIST_MA_NHOM_KH_NCC': ma_nhom_khach_hang})
        
        hoa_dons = self.env['sale.ex.hoa.don.ban.hang'].search([])
        if hoa_dons:
            for hoa_don in hoa_dons:
                chung_tu_ban_hang_ids = []
                if hoa_don.CHUNG_TU_BAN_HANG:
                    hoa_don.CHUNG_TU_BAN_HANG.write({'SO_HOA_DON': hoa_don.SO_HOA_DON,
                                          'NGAY_HOA_DON': hoa_don.NGAY_HOA_DON,
                                          'DA_LAP_HOA_DON': True,})
                    chung_tu_ban_hang_ids.append(hoa_don.CHUNG_TU_BAN_HANG.id)
                hoa_don.SALE_DOCUMENT_IDS = tuple(chung_tu_ban_hang_ids)

        
    
    def update_v04(self):
        for partner in self.env['res.partner'].search([('MA', '=', None)]):
            partner.write({'MA': partner.name})

        #Cập nhật lại dữ liệu hệ thống tài khoản khi không tích chọn vào đối tượng và selection 1 bên đc gán là None
        he_thong_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([])
        if he_thong_tai_khoan:
            changes = {}
            for tk in he_thong_tai_khoan:
                if tk.DOI_TUONG == False:
                    changes.update({'DOI_TUONG_SELECTION':None})
                if tk.DOI_TUONG_THCP == False:
                    changes.update({'DOI_TUONG_THCP_SELECTION':None})
                if tk.CONG_TRINH == False:
                    changes.update({'CONG_TRINH_SELECTION':None})
                if tk.DON_DAT_HANG == False:
                    changes.update({'DON_DAT_HANG_SELECTION':None})
                if tk.HOP_DONG_BAN == False:
                    changes.update({'HOP_DONG_BAN_SELECTION':None})
                if tk.HOP_DONG_MUA == False:
                    changes.update({'HOP_DONG_MUA_SELECTION':None})
                if tk.KHOAN_MUC_CP == False:
                    changes.update({'KHOAN_MUC_CP_SELECTION':None})
                if tk.DON_VI == False:
                    changes.update({'DON_VI_SELECTION':None})
                if tk.MA_THONG_KE == False:
                    changes.update({'MA_THONG_KE_SELECTION':None})
                if changes:
                    tk.write(changes)

        #Cập nhật lại ảnh model(danh.muc.tai.khoan.ngan.hang)
        tai_khoan_ngan_hang = self.env['danh.muc.tai.khoan.ngan.hang'].search([])
        if tai_khoan_ngan_hang:
            for tknh in tai_khoan_ngan_hang:
                if not tknh.image:
                    tknh.write({'image': tknh.NGAN_HANG_ID.image,})

        so_kho_chi_tiet = self.env['so.kho.chi.tiet'].search([])
        if so_kho_chi_tiet:
            for sk in so_kho_chi_tiet:
                if sk.MODEL_CHUNG_TU and sk.ID_CHUNG_TU:
                    chung_tu = self.env[sk.MODEL_CHUNG_TU].search([('id', '=', sk.ID_CHUNG_TU)],limit=1)
                    if not chung_tu:
                        sk.unlink()
                else:
                    sk.unlink()

        doi_tuongs = self.env['res.partner'].search([])
        if doi_tuongs:
            for dt in doi_tuongs:
                if dt.LA_NHAN_VIEN == True:
                    ma = dt.MA_NHAN_VIEN
                elif dt.LA_KHACH_HANG == True:
                    ma = dt.MA_KHACH_HANG
                elif dt.LA_NHA_CUNG_CAP == True:
                    ma = dt.MA_NHA_CUNG_CAP
                else:
                    ma = dt.name
                if ma != dt.MA:
                    dt.write({'MA': ma})

                # cập nhật lại trường liên lưu lại list nhóm kh ncc
                if dt.NHOM_KH_NCC_ID:
                    ma_pc_nhom_khach_hang = ''
                    for line in dt.NHOM_KH_NCC_ID:
                        ma_pc_nhom_khach_hang += ";" + line.MA_PHAN_CAP
                    ma_pc_nhom_khach_hang += ";"
                    dt.write({'LIST_MPC_NHOM_KH_NCC': ma_pc_nhom_khach_hang})

                    ma_nhom_khach_hang = ''
                    for line in dt.NHOM_KH_NCC_ID:
                        if ma_nhom_khach_hang == '':
                            ma_nhom_khach_hang = line.MA
                        else:
                            ma_nhom_khach_hang += "; " + line.MA
                    dt.write({'LIST_MA_NHOM_KH_NCC': ma_nhom_khach_hang})

        vat_tu_hang_hoas = self.env['danh.muc.vat.tu.hang.hoa'].search([])
        if vat_tu_hang_hoas:
            for vthh in vat_tu_hang_hoas:
                # cập nhật lại trường liên lưu lại list nhóm vthh
                if vthh.NHOM_VTHH:
                    ma_pc_nhom_vthh = ''
                    for line in vthh.NHOM_VTHH:
                        ma_pc_nhom_vthh += ";" + line.MA_PHAN_CAP
                    ma_pc_nhom_vthh += ";"
                    vthh.write({'LIST_MPC_NHOM_VTHH': ma_pc_nhom_vthh})

        ghi_tang_ccdc = self.env['supply.ghi.tang'].search([])
        if ghi_tang_ccdc:
            for ghi_tang in ghi_tang_ccdc:
                if ghi_tang.KHAI_BAO_DAU_KY == True:
                    ghi_tang.write({'LOAI_CHUNG_TU': 457 })
        
        

    def update_v03(self):
        # cập nhật lại thời gian sử dụng ghi tăng
        assets_ghi_tang = self.env['asset.ghi.tang'].search([])
        if assets_ghi_tang:
            for ts in assets_ghi_tang:
                ts.write({'SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC':ts.SO_THOI_GIAN_SU_DUNG })
            for ts2 in assets_ghi_tang:
                thoi_gian_su_dung = 0
                if ts2.THOI_GIAN_SU_DUNG == '0':
                    thoi_gian_su_dung = ts2.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC
                elif ts2.THOI_GIAN_SU_DUNG == '1':
                    thoi_gian_su_dung = ts2.SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC*12
                ts.write({'SO_THOI_GIAN_SU_DUNG':thoi_gian_su_dung })
        
        doi_tuong_phan_bo = self.env['asset.ghi.tang.thiet.lap.phan.bo'].search([])
        if doi_tuong_phan_bo:
            for dt in doi_tuong_phan_bo:
                loai_doi_tuong = ''
                if dt.DOI_TUONG_PHAN_BO_ID:
                    if dt.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.doi.tuong.tap.hop.chi.phi':
                        loai_doi_tuong = '0'
                    elif dt.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.cong.trinh':
                        loai_doi_tuong = '1'
                    elif dt.DOI_TUONG_PHAN_BO_ID._name =='account.ex.don.dat.hang':
                        loai_doi_tuong = '2'
                    elif dt.DOI_TUONG_PHAN_BO_ID._name =='sale.ex.hop.dong.ban':
                        loai_doi_tuong = '3'
                    elif dt.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.to.chuc':
                        loai_doi_tuong = '4'
                    dt.write({'SO_THOI_GIAN_SU_DUNG':loai_doi_tuong })

        so_tscd_chi_tiet = self.env['so.tscd.chi.tiet'].search([])
        if so_tscd_chi_tiet:
            for so_tscd in so_tscd_chi_tiet:
                thu_tu_nghiep_vu = -1
                if so_tscd.LOAI_CHUNG_TU == 615:
                    thu_tu_nghiep_vu = 0
                elif so_tscd.LOAI_CHUNG_TU == 250:
                    thu_tu_nghiep_vu = 1
                elif so_tscd.LOAI_CHUNG_TU == 256:
                    thu_tu_nghiep_vu = 2
                elif so_tscd.LOAI_CHUNG_TU == 252:
                    thu_tu_nghiep_vu = 3
                elif so_tscd.LOAI_CHUNG_TU == 253:
                    thu_tu_nghiep_vu = 4
                elif so_tscd.LOAI_CHUNG_TU == 254:
                    thu_tu_nghiep_vu = 5
                elif so_tscd.LOAI_CHUNG_TU == 251:
                    thu_tu_nghiep_vu = 6
                so_tscd.write({'THU_TU_NGHIEP_VU':thu_tu_nghiep_vu })


    def update_v02(self):
        # Loại bỏ các chứng từ không tồn tại nữa sổ cái
        so_cai_chi_tiet = self.env['so.cai.chi.tiet'].search([])
        arr_so_can_xoa = []
        if so_cai_chi_tiet:
            for sc in so_cai_chi_tiet:
                if sc.MODEL_CHUNG_TU and sc.ID_CHUNG_TU:
                    chung_tu = self.env[sc.MODEL_CHUNG_TU].search([('id', '=', sc.ID_CHUNG_TU)],limit=1)
                    if not chung_tu:
                        arr_so_can_xoa.append(sc.id)
                else:
                    arr_so_can_xoa.append(sc.id)
        for so_can_xoa in arr_so_can_xoa:
            self.env['so.cai.chi.tiet'].search([('id','=',so_can_xoa)],limit=1).unlink()

        # Loại bỏ các chứng từ không tồn tại nữa sổ tscd
        so_tscd_chi_tiet = self.env['so.tscd.chi.tiet'].search([])
        if so_tscd_chi_tiet:
            for stscd in so_tscd_chi_tiet:
                if stscd.MODEL_CHUNG_TU and stscd.ID_CHUNG_TU:
                    chung_tu = self.env[stscd.MODEL_CHUNG_TU].search([('id', '=', stscd.ID_CHUNG_TU)],limit=1)
                    if not chung_tu:
                        stscd.unlink()
                else:
                    stscd.unlink()

        # Loại bỏ các chứng từ không tồn tại nữa sổ ccdc
        so_ccdc_chi_tiet = self.env['so.ccdc.chi.tiet'].search([])
        if so_ccdc_chi_tiet:
            for sccdc in so_ccdc_chi_tiet:
                if sccdc.MODEL_CHUNG_TU and sccdc.ID_CHUNG_TU:
                    chung_tu = self.env[sccdc.MODEL_CHUNG_TU].search([('id', '=', sccdc.ID_CHUNG_TU)],limit=1)
                    if not chung_tu:
                        sccdc.unlink()
                else:
                    sccdc.unlink()

        # Loại bỏ các chứng từ không tồn tại nữa sổ bán hàng
        so_ban_hang_chi_tiet = self.env['so.ban.hang.chi.tiet'].search([])
        if so_ban_hang_chi_tiet:
            for sbh in so_ban_hang_chi_tiet:
                if sbh.MODEL_CHUNG_TU and sbh.ID_CHUNG_TU:
                    chung_tu = self.env[sbh.MODEL_CHUNG_TU].search([('id', '=', sbh.ID_CHUNG_TU)],limit=1)
                    if not chung_tu:
                        sbh.unlink()
                else:
                    sbh.unlink()

        # Loại bỏ các chứng từ không tồn tại nữa sổ mua hangf
        so_mua_hang_chi_tiet = self.env['so.mua.hang.chi.tiet'].search([])
        if so_mua_hang_chi_tiet:
            for smh in so_mua_hang_chi_tiet:
                if smh.MODEL_CHUNG_TU and smh.ID_CHUNG_TU:
                    chung_tu = self.env[smh.MODEL_CHUNG_TU].search([('id', '=', smh.ID_CHUNG_TU)],limit=1)
                    if not chung_tu:
                        smh.unlink()
                else:
                    smh.unlink()

    def update_v01(self):
        #Cập nhật lại Thời gian sử dụng tháng ngoài list model(ghi tăng tscđ)
        # ghi_tang_tscd = self.env['asset.ghi.tang'].search([])
        # if ghi_tang_tscd:
            # for gttscd in ghi_tang_tscd:   
                # if gttscd.THOI_GIAN_SU_DUNG == '1':
                    # gttscd.THOI_GIAN_SU_DUNG_THANG_LIST =gttscd.SO_THOI_GIAN_SU_DUNG *12
                # else:
                    # gttscd.THOI_GIAN_SU_DUNG_THANG_LIST =gttscd.SO_THOI_GIAN_SU_DUNG         
                # gttscd.write({'THOI_GIAN_SU_DUNG_THANG_LIST':gttscd.THOI_GIAN_SU_DUNG_THANG_LIST })

        # cập nhật lại danh mục kho - trường name related tới trường Mã 
        danh_muc_kho = self.env['danh.muc.kho'].search([])
        if danh_muc_kho:
            for kho in danh_muc_kho:
                kho.write({'name': kho.MA_KHO})

        #Cập nhật lại Loại chứng từ model (Lệnh sản xuất)
        lenh_san_xuat = self.env['stock.ex.lenh.san.xuat'].search([])
        if lenh_san_xuat:
            for lsx in lenh_san_xuat:       
                lsx.write({'LOAI_CHUNG_TU': 2040})



        #Cập nhật lại LA_TIEN_CO_SO model(chứng từ bán hàng)
        chung_tu_ban_hang = self.env['sale.document'].search([])
        if chung_tu_ban_hang:
            for ctbh in chung_tu_ban_hang:   
                #cập nhật lại giá trị là tiền cơ sở: theo tỷ giá
                # nếu tỷ giá =1 thì là tiền cơ sở =true
                # ngược lại tiền cơ sở = false
                if ctbh.TY_GIA == 1.0:
                    ctbh.LA_TIEN_CO_SO =True
                else:
                    ctbh.LA_TIEN_CO_SO =False          
                ctbh.write({'LA_TIEN_CO_SO':ctbh.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(đơn đặt hàng)
        don_dat_hang = self.env['account.ex.don.dat.hang'].search([])
        if don_dat_hang:
            for ddh in don_dat_hang:   
                if ddh.TY_GIA == 1.0:
                    ddh.LA_TIEN_CO_SO =True
                else:
                    ddh.LA_TIEN_CO_SO =False          
                ddh.write({'LA_TIEN_CO_SO':ddh.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(đơn mua hang)
        don_mua_hang = self.env['purchase.ex.don.mua.hang'].search([])
        if don_mua_hang:
            for dmh in don_mua_hang:   
                if dmh.TY_GIA == 1.0:
                    dmh.LA_TIEN_CO_SO =True
                else:
                    dmh.LA_TIEN_CO_SO =False          
                dmh.write({'LA_TIEN_CO_SO':dmh.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(chứng từ mua hàng)
        chung_tu_mua_hang = self.env['purchase.document'].search([])
        if chung_tu_mua_hang:
            for ctmh in chung_tu_mua_hang:
                if ctmh.TY_GIA == 1.0:
                    ctmh.LA_TIEN_CO_SO =True
                else:
                    ctmh.LA_TIEN_CO_SO =False          
                ctmh.write({'LA_TIEN_CO_SO':ctmh.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(giảm giá hàng mua)
        giam_gia_hang_mua = self.env['purchase.ex.giam.gia.hang.mua'].search([])
        if giam_gia_hang_mua:
            for gghm in giam_gia_hang_mua:   
                if gghm.TY_GIA == 1.0:
                    gghm.LA_TIEN_CO_SO =True
                else:
                    gghm.LA_TIEN_CO_SO =False          
                gghm.write({'LA_TIEN_CO_SO':gghm.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(hóa đơn mua hàng)
        hoa_don_mua_hang = self.env['purchase.ex.hoa.don.mua.hang'].search([])
        if hoa_don_mua_hang:
            for hdmh in hoa_don_mua_hang:   
                if hdmh.TY_GIA == 1.0:
                    hdmh.LA_TIEN_CO_SO =True
                else:
                    hdmh.LA_TIEN_CO_SO =False          
                hdmh.write({'LA_TIEN_CO_SO':hdmh.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(hợp đồng mua hàng)
        hop_dong_mua_hang = self.env['purchase.ex.hop.dong.mua.hang'].search([])
        if hop_dong_mua_hang:
            for hdmh in hop_dong_mua_hang:   
                if hdmh.TY_GIA == 1.0:
                    hdmh.LA_TIEN_CO_SO =True
                else:
                    hdmh.LA_TIEN_CO_SO =False          
                hdmh.write({'LA_TIEN_CO_SO':hdmh.LA_TIEN_CO_SO,
                            'LOAI_CHUNG_TU': 9040})


        #Cập nhật lại LA_TIEN_CO_SO model(trả lại hàng mua)
        tra_lai_hang_mua = self.env['purchase.ex.tra.lai.hang.mua'].search([])
        if tra_lai_hang_mua:
            for tlhm in tra_lai_hang_mua:   
                if tlhm.TY_GIA == 1.0:
                    tlhm.LA_TIEN_CO_SO =True
                else:
                    tlhm.LA_TIEN_CO_SO =False          
                tlhm.write({'LA_TIEN_CO_SO':tlhm.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(báo giá)
        bao_gia = self.env['sale.ex.bao.gia'].search([])
        if bao_gia:
            for bg in bao_gia:   
                if bg.TY_GIA == 1.0:
                    bg.LA_TIEN_CO_SO =True
                else:
                    bg.LA_TIEN_CO_SO =False          
                bg.write({'LA_TIEN_CO_SO':bg.LA_TIEN_CO_SO })

        #Cập nhật lại LA_TIEN_CO_SO model(giảm giá hàng bán)
        giam_gia_hang_ban = self.env['sale.ex.giam.gia.hang.ban'].search([])
        if giam_gia_hang_ban:
            for gghb in giam_gia_hang_ban:   
                if gghb.TY_GIA == 1.0:
                    gghb.LA_TIEN_CO_SO =True
                else:
                    gghb.LA_TIEN_CO_SO =False          
                gghb.write({'LA_TIEN_CO_SO':gghb.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(hợp đồng bán hàng)
        hop_dong_ban_hang = self.env['sale.ex.hop.dong.ban'].search([])
        if hop_dong_ban_hang:
            for hdb in hop_dong_ban_hang:   
                if hdb.TY_GIA == 1.0:
                    hdb.LA_TIEN_CO_SO =True
                else:
                    hdb.LA_TIEN_CO_SO =False          
                hdb.write({'LA_TIEN_CO_SO':hdb.LA_TIEN_CO_SO,
                            'LOAI_CHUNG_TU':9041})
        
        #Cập nhật lại LA_TIEN_CO_SO model(trả lại hàng bán)
        tra_lai_hang_ban = self.env['sale.ex.tra.lai.hang.ban'].search([])
        if tra_lai_hang_ban:
            for tlhb in tra_lai_hang_ban:   
                if tlhb.TY_GIA == 1.0:
                    tlhb.LA_TIEN_CO_SO =True
                else:
                    tlhb.LA_TIEN_CO_SO =False          
                tlhb.write({'LA_TIEN_CO_SO':tlhb.LA_TIEN_CO_SO })
        
        #Cập nhật lại LA_TIEN_CO_SO model(chứng từ nghiệp vụ khác)
        chung_tu_nvk = self.env['account.ex.chung.tu.nghiep.vu.khac'].search([])
        if chung_tu_nvk:
            for ctnvk in chung_tu_nvk:   
                if ctnvk.TY_GIA == 1.0:
                    ctnvk.LA_TIEN_CO_SO =True
                else:
                    ctnvk.LA_TIEN_CO_SO =False          
                ctnvk.write({'LA_TIEN_CO_SO':ctnvk.LA_TIEN_CO_SO })

        

        #Cập nhật lại thành tiền quy đổi,tiền thuế gtgt quy đổi, tiền ckqđ tab hàng tiền model(sale.ex.chi.tiet.hoa.don.ban.hang)
        hoa_don_ban_hang_chi_tiet = self.env['sale.ex.chi.tiet.hoa.don.ban.hang'].search([])            
        if hoa_don_ban_hang_chi_tiet:
            for hdct in hoa_don_ban_hang_chi_tiet:
                hdct.TY_GIA = hdct.HOA_DON_ID_ID.TY_GIA
                hdct.tinh_tien_quy_doi()
                hdct.write(
                    {
                        'THANH_TIEN_QUY_DOI': hdct.THANH_TIEN_QUY_DOI,
                        'TIEN_THUE_GTGT_QUY_DOI': hdct.TIEN_THUE_GTGT_QUY_DOI, 
                        'TIEN_CHIET_KHAU_QUY_DOI': hdct.TIEN_CHIET_KHAU_QUY_DOI, 
                        'TY_GIA':hdct.HOA_DON_ID_ID.TY_GIA 
                    })


        #Cập nhật lại số tiền ngoài list model(sale.ex.hoa.don.ban.hang)
        hoa_don_ban_hang = self.env['sale.ex.hoa.don.ban.hang'].search([])
        if hoa_don_ban_hang:
            for hdbh in hoa_don_ban_hang:
                hdbh.tinh_tong_tien()
                hdbh.write({'TONG_TIEN_THANH_TOAN_QD':hdbh.TONG_TIEN_THANH_TOAN_QD })




        #Cập nhật lại số tiền quy đổi tab hạch toán model(account.ex.phieu.thu.chi.tiet)
        phieu_thu_chi_tiet = self.env['account.ex.phieu.thu.chi.tiet'].search([])            
        if phieu_thu_chi_tiet:
            for ptct in phieu_thu_chi_tiet:
                ptct.TY_GIA = ptct.PHIEU_THU_CHI_ID.TY_GIA
                ptct.tinh_tien_quy_doi()
                ptct.write({'SO_TIEN_QUY_DOI': ptct.SO_TIEN_QUY_DOI, 'TY_GIA':ptct.PHIEU_THU_CHI_ID.TY_GIA })


        #Cập nhật lại số tiền ngoài list model(account.ex.phieu.thu.chi)
        phieu_thu_chi = self.env['account.ex.phieu.thu.chi'].search([])
        if phieu_thu_chi:
            for ptc in phieu_thu_chi:
                ptc.tinh_tong_tien()
                if ptc.TY_GIA == 1.0:
                    ptc.LA_TIEN_CO_SO =True
                else:
                    ptc.LA_TIEN_CO_SO =False  
                ptc.write({
                            'SO_TIEN_TREE':ptc.SO_TIEN_TREE,
                            'LA_TIEN_CO_SO':ptc.LA_TIEN_CO_SO 
                        })





        # cập nhật lai bậc những chỗ dùng
        cong_trinh = self.env['danh.muc.cong.trinh'].search([])
        if cong_trinh:
            for ct in cong_trinh:
                ct.write({'BAC': len(ct.MA_PHAN_CAP.split('/')) - 2})

        to_chuc = self.env['danh.muc.to.chuc'].search([])
        if to_chuc:
            for tc in to_chuc:
                tc.write({'BAC': len(tc.MA_PHAN_CAP.split('/')) - 2})

        doi_tuong_tap_hop_chi_phi = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
        if doi_tuong_tap_hop_chi_phi:
            for dt in doi_tuong_tap_hop_chi_phi:
                dt.write({'BAC': len(dt.MA_PHAN_CAP.split('/')) - 2})

        he_thong_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([])
        if he_thong_tai_khoan:
            for tk in he_thong_tai_khoan:
                tk.write({'BAC': len(tk.MA_PHAN_CAP.split('/')) - 2})

        khoan_muc_cp = self.env['danh.muc.khoan.muc.cp'].search([])
        if khoan_muc_cp:
            for cp in khoan_muc_cp:
                cp.write({'BAC': len(cp.MA_PHAN_CAP.split('/')) - 2})

        nhom_kh_ncc = self.env['danh.muc.nhom.khach.hang.nha.cung.cap'].search([])
        if nhom_kh_ncc:
            for nhom in nhom_kh_ncc:
                nhom.write({'BAC': len(nhom.MA_PHAN_CAP.split('/')) - 2})
        # Update trường lưu tên và mã phân cấp của nhóm khách hàng
        doi_tuongs = self.env['res.partner'].search([])
        nhom_kh_ncc = ''
        ma_pc_nhom_kh_ncc = ''
        if doi_tuongs:
            for dt in  doi_tuongs:
                nhom_kh_ncc = dt.lay_nhom_kh_ncc()
                ma_pc_nhom_kh_ncc = dt.lay_ma_pc_nhom_kh_ncc()

                if dt.LA_NHAN_VIEN:
                    dt.KIEU_DOI_TUONG ='NHAN_VIEN'
                if dt.LA_NHA_CUNG_CAP:
                    dt.KIEU_DOI_TUONG ='NHA_CC'
                if dt.LA_KHACH_HANG:
                    dt.KIEU_DOI_TUONG ='KHACH_HANG'
                dt.write({'LIST_TEN_NHOM_KH_NCC' : nhom_kh_ncc,
                        'LIST_MPC_NHOM_KH_NCC' : ma_pc_nhom_kh_ncc,
                        'KIEU_DOI_TUONG':dt.KIEU_DOI_TUONG
                })
        # Update trường lưu tên và mã phân cấp của nhóm vật tư hàng hóa, dịch vụ
        vat_tu_hang_hoas = self.env['danh.muc.vat.tu.hang.hoa'].search([])
        nhom_vthh_dv = ''
        ma_pc_nhom_vthh_dv = ''
        if vat_tu_hang_hoas:
            for dt in  vat_tu_hang_hoas:
                nhom_vthh_dv = dt.luu_nhom_vthh()
                ma_pc_nhom_vthh_dv = dt.lay_ma_pc_nhom_vthh_dv()
                dt.write({'LIST_NHOM_VTHH' : nhom_vthh_dv,
                        'LIST_MPC_NHOM_VTHH' : ma_pc_nhom_vthh_dv,
                })

        nhap_xuat_kho_chi_tiet = self.env['stock.ex.nhap.xuat.kho.chi.tiet'].search([])
        if nhap_xuat_kho_chi_tiet:
            for chi_tiet in nhap_xuat_kho_chi_tiet:
                tien_von = 0
                if chi_tiet.TIEN_VON != 0:
                    tien_von = chi_tiet.TIEN_VON
                elif chi_tiet.TIEN_VON_QUY_DOI != 0:
                    tien_von = chi_tiet.TIEN_VON_QUY_DOI
                chi_tiet.write({'TIEN_VON' : tien_von,
                        'TIEN_VON_QUY_DOI' : tien_von,
                })

        
        cr = self.env.cr
        query = """UPDATE so_cai_chi_tiet SET currency_id = (SELECT cr.id FROM res_currency cr WHERE cr."MA_LOAI_TIEN" = 'VND') WHERE currency_id ISNULL;
                UPDATE so_cai_chi_tiet SET "TEN_LOAI_TIEN" = (SELECT cr."MA_LOAI_TIEN" FROM res_currency cr WHERE cr."MA_LOAI_TIEN" = 'VND') WHERE "TEN_LOAI_TIEN" ISNULL;
        """
        cr.execute(query)

    def tao_view_tim_kiem(self): 
        self.env.cr.execute("""DROP VIEW if EXISTS tien_ich_tim_kiem_chung_tu;
        CREATE or REPLACE VIEW tien_ich_tim_kiem_chung_tu as (
            
        SELECT
            row_number()
            OVER (
                PARTITION BY TRUE :: BOOLEAN )       AS id
            , concat(kq."ID_GOC", ',', kq."MODEL_GOC") AS "ID_AND_MODEL"
            , kq."ID_GOC"
            , kq."MODEL_GOC"
            , kq."LOAI_CHUNG_TU"
            , rt."REFTYPENAME"                         AS "TEN_LOAI_CHUNG_TU"
            , kq."NGAY_HACH_TOAN"
            , kq."NGAY_CHUNG_TU"
            , kq."SO_CHUNG_TU"
            , kq."SO_HOA_DON"
            , kq."NGAY_HOA_DON"
            , kq."TK_NO_ID"
            , kq."TK_CO_ID"
            , kq."SO_TIEN"
            , coalesce(kq."currency_id", 24)           AS "currency_id"
            , round(cast((kq."SO_TIEN_QUY_DOI") AS NUMERIC),0) AS "SO_TIEN_QUY_DOI"
            , kq."MA_HANG_ID"
            , kq."TEN_HANG"                            AS "TEN_VTHH"
            , kq."MA_KHO_NHAP_ID"
            , kq."MA_KHO_XUAT_ID"
            , kq."DVT_ID"
            , kq."SO_LUONG"
            , kq."DON_GIA"
            , kq."TY_LE_CHIET_KHAU"
            , kq."SO_TIEN_CHIET_KHAU"
            , kq."TSCD_ID"
            , kq."LOAI_TSCD_ID"
            , kq."CCDC_ID"
            , kq."DOI_TUONG_ID"
            , kq."DOI_TUONG_NO_ID"
            , kq."DOI_TUONG_CO_ID"
            , kq."DON_VI_ID"
            , kq."NHAN_VIEN_ID"
            , kq."TK_NGAN_HANG"
            , kq."KHOAN_MUC_CP_ID"
            , kq."CONG_TRINH_ID"
            , kq."DOI_TUONG_THCP_ID"
            , kq."DON_MUA_HANG_ID"
            , kq."DON_DAT_HANG_ID"
            , kq."HOP_DONG_MUA_ID"
            , kq."HOP_DONG_BAN_ID"
            , kq."MA_THONG_KE_ID"
            , kq."DIEN_GIAI_CHUNG"
            , kq."DIEN_GIAI"
            , kq."CHI_NHANH_ID"
            , kq."CHI_TIET_ID"
            , kq."TONG_TIEN_QUY_DOI"
            , kq."SOURCE_ID"
            , CASE WHEN kq."TRANG_THAI_GHI_SO" = 'da_ghi_so'
            THEN TRUE
            ELSE FALSE END                           AS "TINH_TRANG_GHI_SO"
        FROM (
                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , D."SO_TIEN"                        AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                  AS "TONG_TIEN"
                    , 0                                  AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"
                    /*(CR 12944)*/
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , D."TK_NGAN_HANG_ID"                AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_DETAIL"               AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M.id = D."PHIEU_THU_CHI_ID"
                WHERE M."TYPE_NH_Q" = 'QUY' AND M."LOAI_PHIEU" = 'PHIEU_CHI'

                UNION ALL

                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , D."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , NULL :: INT                        AS "TK_NO_ID"
                    , NULL :: INT                        AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , 0                                  AS "SO_TIEN"
                    , 0                                  AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                        AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                        AS "CONG_TRINH_ID"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                        AS "DON_DAT_HANG_ID"
                    , NULL :: INT
                    /*(CR 12944)*/
                    , NULL :: INT                        AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                        AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , NULL :: INT                        AS "MA_THONG_KE_ID"
                    , M."LY_DO_CHI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_THUE"                 AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                        AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_thue D ON M.id = D."PHIEU_THU_THUE_ID"
                WHERE M."TYPE_NH_Q" = 'QUY' AND M."LOAI_PHIEU" = 'PHIEU_CHI'


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , D."SO_TIEN"                        AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"
                    /*(CR 12944)*/
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , D."TK_NGAN_HANG_ID"                AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_DETAIL"               AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M.id = D."PHIEU_THU_CHI_ID"
                WHERE M."TYPE_NH_Q" = 'QUY' AND M."LOAI_PHIEU" = 'PHIEU_THU'


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , D."SO_TIEN"                        AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"
                    /*(CR 12944)*/
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_NOP_ID"               AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_DETAIL"               AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M.id = D."PHIEU_THU_CHI_ID"
                WHERE M."TYPE_NH_Q" = 'NGAN_HANG' AND M."LOAI_PHIEU" = 'PHIEU_THU'


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , D."SO_TIEN"                        AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 1523
                    THEN NULL :: INT
                        ELSE D."DOI_TUONG_ID"
                        END)                              AS "DOI_TUONG_NO_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 1523
                    THEN NULL :: INT
                        ELSE D."DOI_TUONG_ID"
                        END)                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"
                    /*(CR 12944)*/
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_CHI_GUI_ID"           AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_DETAIL"               AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M.id = D."PHIEU_THU_CHI_ID"
                WHERE M."TYPE_NH_Q" = 'NGAN_HANG' AND M."LOAI_PHIEU" = 'PHIEU_CHI'


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , D."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , NULL :: INT                        AS "TK_NO_ID"
                    , NULL :: INT                        AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , 0                                  AS "SO_TIEN"
                    , 0                                  AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                        AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                        AS "CONG_TRINH_ID"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                        AS "DON_DAT_HANG_ID"
                    , NULL :: INT
                    /*(CR 12944)*/
                    , NULL :: INT                        AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                        AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_CHI_GUI_ID"           AS "TK_NGAN_HANG"
                    , NULL :: INT                        AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_THUE"                 AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                        AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_thue D ON M.id = D."PHIEU_THU_THUE_ID"
                WHERE M."TYPE_NH_Q" = 'NGAN_HANG' AND M."LOAI_PHIEU" = 'PHIEU_CHI'


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , D."SO_TIEN"                        AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 1523
                    THEN NULL :: INT
                        ELSE D."DOI_TUONG_ID"
                        END)                              AS "DOI_TUONG_NO_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 1523
                    THEN NULL :: INT
                        ELSE D."DOI_TUONG_ID"
                        END)                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"
                    /*(CR 12944)*/
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_DEN_ID"               AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_DETAIL"               AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M.id = D."PHIEU_THU_CHI_ID"
                WHERE M."TYPE_NH_Q" = 'NGAN_HANG' AND M."LOAI_PHIEU" = 'PHIEU_CHUYEN_TIEN'


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , D."SO_TIEN"                        AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN"
                    , M."SO_TIEN_TREE"                   AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 1523
                    THEN NULL :: INT
                        ELSE D."DOI_TUONG_ID"
                        END)                              AS "DOI_TUONG_NO_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 1523
                    THEN NULL :: INT
                        ELSE D."DOI_TUONG_ID"
                        END)                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"
                    /*(CR 12944)*/
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_CHI_GUI_ID"           AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI_DETAIL"               AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"
                FROM account_ex_phieu_thu_chi M
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M.id = D."PHIEU_THU_CHI_ID"
                WHERE M."TYPE_NH_Q" = 'NGAN_HANG' AND M."LOAI_PHIEU" = 'PHIEU_CHUYEN_TIEN'

                UNION ALL

                SELECT
                    M.id                         AS "ID_GOC"
                    , 'asset.danh.gia.lai' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"           AS "NGAY_HACH_TOAN"
                    , NULL :: INT                  AS "currency_id"
                    , ''                           AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)           AS "NGAY_HOA_DON"
                    , NULL :: INT                  AS "MA_TK_NO"
                    , NULL :: INT                  AS "MA_TK_CO"
                    , NULL :: INT                  AS "MA_HANG_ID"
                    , ''                           AS "TEN_HANG"
                    , NULL :: INT                  AS "DVT_ID"
                    , NULL :: INT                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                  AS "MA_KHO_XUAT_ID"
                    , 0                            AS "SO_LUONG"
                    , 0                            AS "DON_GIA"
                    , 0                            AS "SO_TIEN"
                    , 0                            AS "SO_TIEN_QUY_DOI"
                    , 0                            AS "TY_LE_CHIET_KHAU"
                    , 0                            AS "SO_TIEN_CHIET_KHAU"
                    , 0                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                            AS "TONG_TIEN"
                    , 0                            AS "TONG_TIEN_QUY_DOI"
                    , D."MA_TAI_SAN_ID"            AS "TSCD_ID"
                    , GT."LOAI_TAI_SAN_ID"         AS "LOAI_TSCD_ID"
                    , NULL :: INT                  AS "CCDC_ID"
                    , NULL :: INT                  AS "DOI_TUONG_ID"
                    , NULL :: INT                  AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                  AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_SU_DUNG"           AS "DON_VI_ID"
                    , NULL :: INT                  AS "NHAN_VIEN_ID"
                    , NULL :: INT                  AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                  AS "CONG_TRINH_ID"
                    , NULL :: INT                  AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                  AS "DON_DAT_HANG_ID"
                    , NULL :: INT                  AS "DON_MUA_HANG_ID"
                    , NULL :: INT                  AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                  AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                  AS "TK_NGAN_HANG"
                    , NULL :: INT                  AS "MA_THONG_KE_ID"
                    , M."KET_LUAN"                 AS "DIEN_GIAI_CHUNG"
                    , ''                           AS "DIEN_GIAI"
                    , NULL :: INT                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                  AS "DVT_ID_CT"
                    , NULL :: INT                  AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                  AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_SU_DUNG"           AS "DON_VI_ID_CT"
                    , M."state"                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"             AS "CHI_NHANH_ID"
                    , D.id                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)          AS "SOURCE_ID"
                FROM asset_danh_gia_lai M
                    INNER JOIN asset_danh_gia_lai_chi_tiet_dieu_chinh D
                        ON M.id = D."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID"
                    LEFT JOIN asset_ghi_tang GT ON D."MA_TAI_SAN_ID" = GT.id
                --         WHERE M.id = 10

                UNION ALL


                SELECT
                    M.id                         AS "ID_GOC"
                    , 'asset.danh.gia.lai' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"           AS "NGAY_HACH_TOAN"
                    , NULL :: INT                  AS "currency_id"
                    , ''                           AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                 AS "MA_TK_NO"
                    , D."TK_CO_ID"                 AS "MA_TK_CO"
                    , NULL :: INT                  AS "MA_HANG_ID"
                    , ''                           AS "TEN_HANG"
                    , NULL :: INT                  AS "DVT_ID"
                    , NULL :: INT                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                  AS "MA_KHO_XUAT_ID"
                    , 0                            AS "SO_LUONG"
                    , 0                            AS "DON_GIA"
                    , D."SO_TIEN"                  AS "SO_TIEN"
                    , D."SO_TIEN"                  AS "SO_TIEN_QUY_DOI"
                    , 0                            AS "TY_LE_CHIET_KHAU"
                    , 0                            AS "SO_TIEN_CHIET_KHAU"
                    , 0                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                            AS "TONG_TIEN"
                    , 0                            AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                  AS "TSCD_ID"
                    , NULL :: INT                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                  AS "CCDC_ID"
                    , D."DOI_TUONG_ID"             AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_ID"             AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_ID"             AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                AS "DON_VI_ID"
                    , NULL :: INT                  AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"          AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"            AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"        AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"          AS "DON_DAT_HANG_ID"
                    , NULL :: INT                  AS "DON_MUA_HANG_ID"
                    , NULL :: INT                  AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"          AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                  AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"           AS "MA_THONG_KE_ID"
                    , M."KET_LUAN"                 AS "DIEN_GIAI_CHUNG"
                    , ''                           AS "DIEN_GIAI"
                    , NULL :: INT                  AS "MA_HANG_ID_CT"
                    , D."DON_VI_ID"                AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"        AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"          AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                AS "DON_VI_ID_CT"
                    , M."state"                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"             AS "CHI_NHANH_ID"
                    , D.id                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)          AS "SOURCE_ID"
                FROM asset_danh_gia_lai M
                    INNER JOIN asset_danh_gia_lai_hach_toan D ON M.id = D."DANH_GIA_LAI_TAI_SAN_CO_DINH_ID"


                UNION ALL


                SELECT
                    M.id                     AS "ID_GOC"
                    , 'asset.ghi.giam' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"        AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"          AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL::INT AS CABA"SO_CHUNG_TU" ,
                    --             NULL::INT AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"        AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"       AS "NGAY_HACH_TOAN"
                    ,
                    /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng NULL::INT*/
                    NULL :: INT              AS "currency_id"
                    , ''                       AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)       AS "NGAY_HOA_DON"
                    , NULL :: INT              AS "MA_TK_NO"
                    , NULL :: INT              AS "MA_TK_CO"
                    , NULL :: INT              AS "MA_HANG_ID"
                    , ''                       AS "TEN_HANG"
                    , NULL :: INT              AS "DVT_ID"
                    , NULL :: INT              AS "MA_KHO_NHAP_ID"
                    , NULL :: INT              AS "MA_KHO_XUAT_ID"
                    , 0                        AS "SO_LUONG"
                    , 0                        AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    0                        AS "SO_TIEN"
                    , --             0 AS "SO_TIEN"Management ,
                    0                        AS "SO_TIEN_QUY_DOI"
                    , --             0 AS "SO_TIEN_QUY_DOI"Management ,
                    0                        AS "TY_LE_CHIET_KHAU"
                    , 0                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                        AS "TONG_TIEN"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN"Management ,
                    0                        AS "TONG_TIEN_QUY_DOI"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN_QUY_DOI"Management ,
                    D."MA_TAI_SAN"           AS "TSCD_ID"
                    , GT."LOAI_TAI_SAN_ID"     AS "LOAI_TSCD_ID"
                    , NULL :: INT              AS "CCDC_ID"
                    , NULL :: INT              AS "DOI_TUONG_ID"
                    , NULL :: INT              AS "DOI_TUONG_NO_ID"
                    , NULL :: INT              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_SU_DUNG_ID"    AS "DON_VI_ID"
                    , NULL :: INT              AS "NHAN_VIEN_ID"
                    , NULL :: INT              AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT              AS "CONG_TRINH_ID"
                    , NULL :: INT              AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT              AS "DON_DAT_HANG_ID"
                    , NULL :: INT              AS "DON_MUA_HANG_ID"
                    , --             NULL::INT AS ContractID ,
                    NULL :: INT              AS "HOP_DONG_MUA_ID"
                    , NULL :: INT              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT              AS "TK_NGAN_HANG"
                    , NULL :: INT              AS "MA_THONG_KE_ID"
                    , --             NULL::INT AS PurchasePurposeID ,
                    M."LY_DO_GIAM"           AS "DIEN_GIAI_CHUNG"
                    , ''                       AS "DIEN_GIAI"
                    , NULL :: INT              AS "MA_HANG_ID_CT"
                    , NULL :: INT              AS "DVT_ID_CT"
                    , NULL :: INT              AS "DOI_TUONG_THCP_ID_CT"
                    , --             NULL::INT AS DetailContractID ,
                    NULL :: INT              AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_SU_DUNG_ID"    AS "DON_VI_ID_CT"
                    , M."state"                AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"         AS "CHI_NHANH_ID"
                    , D.id                        "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)      AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/
                --             CONVERT(date ,M.CreatedDate) AS CreatedDate ,
                -- 			M.CreatedBy ,
                -- 			CONVERT(date ,M.ModifiedDate) AS ModifiedDate ,
                -- 			M.ModifiedBy
                FROM asset_ghi_giam M
                    INNER JOIN asset_ghi_giam_tai_san D ON M.id = D."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                    LEFT JOIN asset_ghi_tang GT ON D."MA_TAI_SAN" = GT.id


                UNION ALL


                SELECT
                    M.id                     AS "ID_GOC"
                    , 'asset.ghi.giam' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"        AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"          AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL::INT AS CABA"SO_CHUNG_TU" ,
                    --             NULL::INT AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"        AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"       AS "NGAY_HACH_TOAN"
                    ,
                    /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng NULL::INT*/
                    NULL :: INT              AS "currency_id"
                    , ''                       AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)       AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"             AS "TK_NO_ID"
                    , D."TK_CO_ID"             AS "MA_TK_CO"
                    , NULL :: INT              AS "MA_HANG_ID"
                    , ''                       AS "TEN_HANG"
                    , NULL :: INT              AS "DVT_ID"
                    , NULL :: INT              AS "MA_KHO_NHAP_ID"
                    , NULL :: INT              AS "MA_KHO_XUAT_ID"
                    , 0                        AS "SO_LUONG"
                    , 0                        AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    D."SO_TIEN"              AS "SO_TIEN"
                    , --             D."SO_TIEN_QUY_DOI" AS "SO_TIEN"Management ,
                    D."SO_TIEN"              AS "SO_TIEN_QUY_DOI"
                    , --             D."SO_TIEN_QUY_DOI" AS "SO_TIEN_QUY_DOI"Management ,
                    0                        AS "TY_LE_CHIET_KHAU"
                    , 0                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                        AS "TONG_TIEN"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN"Management ,
                    0                        AS "TONG_TIEN_QUY_DOI"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT              AS "TSCD_ID"
                    , NULL :: INT              AS "LOAI_TSCD_ID"
                    , NULL :: INT              AS "CCDC_ID"
                    , NULL :: INT              AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_ID"         AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_ID"         AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"            AS "DON_VI_ID"
                    , NULL :: INT              AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"      AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"        AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"    AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"      AS "DON_DAT_HANG_ID"
                    , NULL :: INT              AS "DON_MUA_HANG_ID"
                    , --             D.ContractID AS ContractID ,
                    NULL :: INT              AS "HOP_DONG_MUA_ID"
                    , NULL :: INT              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"       AS "MA_THONG_KE_ID"
                    , --             NULL::INT AS PurchasePurposeID ,
                    M."LY_DO_GIAM"           AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI"            AS "DIEN_GIAI"
                    , NULL :: INT              AS "MA_HANG_ID_CT"
                    , NULL :: INT              AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"    AS "DOI_TUONG_THCP_ID_CT"
                    , --             D.ContractID AS DetailContractID ,
                    D."KHOAN_MUC_CP_ID"      AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"            AS "DON_VI_ID_CT"
                    , M."state"                AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"         AS "CHI_NHANH_ID"
                    , D.id                     AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)      AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/
                --             CONVERT(date ,M.CreatedDate) AS CreatedDate ,
                -- 			M.CreatedBy ,
                -- 			CONVERT(date ,M.ModifiedDate) AS ModifiedDate ,
                -- 			M.ModifiedBy
                FROM asset_ghi_giam M
                    INNER JOIN asset_ghi_giam_hach_toan D ON M.id = D."TAI_SAN_CO_DINH_GHI_GIAM_ID"


                UNION ALL


                SELECT
                    M.id                          AS "ID_GOC"
                    , 'asset.tinh.khau.hao' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"             AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"               AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"            AS "NGAY_HACH_TOAN"
                    , NULL :: INT                   AS "currency_id"
                    , ''                            AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)            AS "NGAY_HOA_DON"
                    , NULL :: INT                   AS "TK_NO_ID"
                    , NULL :: INT                   AS "TK_CO_ID"
                    , NULL :: INT                   AS "MA_HANG_ID"
                    , ''                            AS "TEN_HANG"
                    , NULL :: INT                   AS "DVT_ID"
                    , NULL :: INT                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                   AS "MA_KHO_XUAT_ID"
                    , 0                             AS "SO_LUONG"
                    , 0                             AS "DON_GIA"
                    , NULL :: INT                   AS "SO_TIEN"
                    , 0                             AS "SO_TIEN_QUY_DOI"
                    , 0                             AS "TY_LE_CHIET_KHAU"
                    , 0                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                             AS "TONG_TIEN"
                    , 0                             AS "TONG_TIEN_QUY_DOI"
                    , D."MA_TAI_SAN_ID"             AS "TSCD_ID"
                    , gt."LOAI_TAI_SAN_ID"          AS "LOAI_TSCD_ID"
                    , NULL :: INT                   AS "CCDC_ID"
                    , NULL :: INT                   AS "DOI_TUONG_ID"
                    , NULL :: INT                   AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_SU_DUNG_ID"         AS "DON_VI_ID"
                    , NULL :: INT                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                   AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                   AS "CONG_TRINH_ID"
                    , NULL :: INT                   AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                   AS "DON_DAT_HANG_ID"
                    , NULL :: INT                   AS "DON_MUA_HANG_ID"
                    , NULL :: INT                   AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                   AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                   AS "TK_NGAN_HANG"
                    , NULL :: INT                   AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                 AS "DIEN_GIAI_CHUNG"
                    , ''                            AS "DIEN_GIAI"
                    , NULL :: INT                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                   AS "DVT_ID_CT"
                    , NULL :: INT                   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_SU_DUNG_ID"         AS "DON_VI_ID_CT"
                    , M."state"                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"              AS "CHI_NHANH_ID"
                    , D.id                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)           AS "SOURCE_ID"
                FROM asset_tinh_khau_hao M
                    INNER JOIN asset_tinh_khau_hao_chi_tiet D ON M.id = D."TINH_KHAU_HAO_ID"
                    LEFT JOIN asset_ghi_tang gt ON D."MA_TAI_SAN_ID" = gt.id

                UNION ALL


                SELECT
                    M.id                          AS "ID_GOC"
                    , 'asset.tinh.khau.hao' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"             AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"               AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"            AS "NGAY_HACH_TOAN"
                    , NULL :: INT                   AS "currency_id"
                    , ''                            AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)            AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                  AS "TK_NO_ID"
                    , D."TK_CO_ID"                  AS "TK_CO_ID"
                    , NULL :: INT                   AS "MA_HANG_ID"
                    , ''                            AS "TEN_HANG"
                    , NULL :: INT                   AS "DVT_ID"
                    , NULL :: INT                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                   AS "MA_KHO_XUAT_ID"
                    , 0                             AS "SO_LUONG"
                    , 0                             AS "DON_GIA"
                    , D."SO_TIEN"                   AS "SO_TIEN"
                    , D."SO_TIEN"                   AS "SO_TIEN_QUY_DOI"
                    , 0                             AS "TY_LE_CHIET_KHAU"
                    , 0                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                             AS "TONG_TIEN"
                    , 0                             AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                   AS "TSCD_ID"
                    , NULL :: INT                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                   AS "CCDC_ID"
                    , NULL :: INT                   AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_NO_ID"           AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_CO_ID"           AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                 AS "DON_VI_ID"
                    , NULL :: INT                   AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"           AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"             AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"         AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"           AS "DON_DAT_HANG_ID"
                    , NULL :: INT                   AS "DON_MUA_HANG_ID"
                    , NULL :: INT                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"           AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                   AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"            AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                 AS "DIEN_GIAI_CHUNG"
                    , ''                            AS "DIEN_GIAI"
                    , NULL :: INT                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                   AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"         AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"           AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                 AS "DON_VI_ID_CT"
                    , M."state"                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"              AS "CHI_NHANH_ID"
                    , D.id                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)           AS "SOURCE_ID"
                FROM asset_tinh_khau_hao M
                    INNER JOIN asset_tinh_khau_hao_hach_toan D ON M.id = D."TINH_KHAU_HAO_ID"


                UNION ALL


                SELECT
                    M.id                        AS "ID_GOC"
                    , 'asset.dieu.chuyen' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"           AS "LOAI_CHUNG_TU"
                    , M."BIEN_BAN_GIAO_NHAN_SO"   AS "SO_CHUNG_TU"
                    , M."NGAY"                    AS "NGAY_CHUNG_TU"
                    , M."NGAY"                    AS "NGAY_HACH_TOAN"
                    , NULL :: INT                 AS "currency_id"
                    , ''                          AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)          AS "NGAY_HOA_DON"
                    , NULL :: INT                 AS "TK_NO_ID"
                    , NULL :: INT                 AS "TK_CO_ID"
                    , NULL :: INT                 AS "MA_HANG_ID"
                    , ''                          AS "TEN_HANG"
                    , NULL :: INT                 AS "DVT_ID"
                    , NULL :: INT                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                 AS "MA_KHO_XUAT_ID"
                    , 0                           AS "SO_LUONG"
                    , 0                           AS "DON_GIA"
                    , 0                           AS "SO_TIEN"
                    , 0                           AS "SO_TIEN_QUY_DOI"
                    , 0                           AS "TY_LE_CHIET_KHAU"
                    , 0                           AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                           AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                           AS "TONG_TIEN"
                    , 0                           AS "TONG_TIEN_QUY_DOI"
                    , D."MA_TAI_SAN_ID"           AS "TSCD_ID"
                    , GT."LOAI_TAI_SAN_ID"        AS "LOAI_TSCD_ID"
                    , NULL :: INT                 AS "CCDC_ID"
                    , NULL :: INT                 AS "DOI_TUONG_ID"
                    , NULL :: INT                 AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                 AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                 AS "DON_VI_ID"
                    , NULL :: INT                 AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , NULL :: INT                 AS "DON_MUA_HANG_ID"
                    , NULL :: INT                 AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                 AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                 AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."LY_DO_DIEU_CHUYEN"       AS "DIEN_GIAI_CHUNG"
                    , ''                          AS "DIEN_GIAI"
                    , NULL :: INT                 AS "MA_HANG_ID_CT"
                    , NULL :: INT                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"       AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"         AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                 AS "DON_VI_ID_CT"
                    , M."state"                   AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"            AS "CHI_NHANH_ID"
                    , D.id                        AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)         AS "SOURCE_ID"
                FROM asset_dieu_chuyen M
                    INNER JOIN asset_dieu_chuyen_chi_tiet D ON M.id = D."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID"
                    LEFT JOIN asset_ghi_tang GT ON GT.id = D."MA_TAI_SAN_ID"


                UNION ALL


                SELECT
                    M.id                     AS "ID_GOC"
                    , 'asset.ghi.tang' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"        AS "LOAI_CHUNG_TU"
                    , M."SO_CT_GHI_TANG"       AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL::INT AS CABA"SO_CHUNG_TU" ,
                    --             NULL::INT AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_GHI_TANG"        AS "NGAY_CHUNG_TU"
                    , M."NGAY_GHI_TANG"        AS "NGAY_HACH_TOAN"
                    ,
                    /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng NULL::INT*/
                    NULL :: INT              AS "currency_id"
                    , ''                       AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)       AS "NGAY_HOA_DON"
                    , NULL :: INT              AS "TK_NO_ID"
                    , NULL :: INT              AS "TK_CO_ID"
                    , NULL :: INT              AS "MA_HANG_ID"
                    , ''                       AS "TEN_HANG"
                    , NULL :: INT              AS "DVT_ID"
                    , NULL :: INT              AS "MA_KHO_NHAP_ID"
                    , NULL :: INT              AS "MA_KHO_XUAT_ID"
                    , NULL :: INT              AS "SO_LUONG"
                    , 0                        AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    M."NGUYEN_GIA"           AS "SO_TIEN"
                    , --             M.NGUYEN_GIA AS "SO_TIEN"Management ,
                    M."NGUYEN_GIA"           AS "SO_TIEN_QUY_DOI"
                    , --             M.NGUYEN_GIA AS "SO_TIEN_QUY_DOI"Management ,
                    0                        AS "TY_LE_CHIET_KHAU"
                    , 0                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."NGUYEN_GIA"           AS "TONG_TIEN"
                    , --             M.NGUYEN_GIA AS "TONG_TIEN"Management ,
                    M."NGUYEN_GIA"           AS "TONG_TIEN_QUY_DOI"
                    , --             M.NGUYEN_GIA AS "TONG_TIEN_QUY_DOI"Management ,
                    M.id                     AS "TSCD_ID"
                    , M."LOAI_TAI_SAN_ID"      AS "LOAI_TSCD_ID"
                    , NULL :: INT              AS "CCDC_ID"
                    , M."DOI_TUONG_ID"         AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"         AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"         AS "DOI_TUONG_CO_ID"
                    , M."DON_VI_SU_DUNG_ID"    AS "DON_VI_ID"
                    , NULL :: INT              AS "NHAN_VIEN_ID"
                    , NULL :: INT              AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT              AS "CONG_TRINH_ID"
                    , NULL :: INT              AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT              AS "DON_DAT_HANG_ID"
                    , NULL :: INT              AS "DON_MUA_HANG_ID"
                    , --             NULL::INT AS ContractID ,
                    NULL :: INT              AS "HOP_DONG_MUA_ID"
                    , NULL :: INT              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT              AS "TK_NGAN_HANG"
                    , NULL :: INT              AS "MA_THONG_KE_ID"
                    , --             NULL::INT AS PurchasePurposeID ,
                    ''                       AS "DIEN_GIAI_CHUNG"
                    , ''                       AS "DIEN_GIAI"
                    , NULL :: INT              AS "MA_HANG_ID_CT"
                    , NULL :: INT              AS "DVT_ID_CT"
                    , NULL :: INT              AS "DOI_TUONG_THCP_ID_CT"
                    , --             NULL::INT AS DetailContractID ,
                    NULL :: INT              AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT              AS "DON_VI_ID_CT"
                    , /* DDKhanh 04/08/2017 CR29455 chức năng không có ghi sổ thì set NULL::INT */
                    M."state"                AS "TRANG_THAI_GHI_SO"
                    , -- 			CAST(NULL::INT AS BIT) AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"         AS "CHI_NHANH_ID"
                    , NULL :: INT              AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)      AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/
                --             CONVERT(date ,M.CreatedDate) AS CreatedDate ,
                -- 			M.CreatedBy ,
                -- 			CONVERT(date ,M.ModifiedDate) AS ModifiedDate ,
                -- 			M.ModifiedBy
                FROM asset_ghi_tang M


                UNION ALL


                SELECT
                    M.id                             AS "ID_GOC"
                    , 'stock.ex.nhap.xuat.kho' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                  AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"            AS "NGAY_HACH_TOAN"
                    , NULL :: INT                      AS "currency_id"
                    , M."SO_CHUNG_TU_CK_READONLY"      AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)               AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                     AS "TK_NO_ID"
                    , D."TK_CO_ID"                     AS "TK_CO_ID"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID"
                    , D."TEN_HANG"                     AS "TEN_HANG"
                    , D."DVT_ID"                       AS "DVT_ID"
                    , D."NHAP_TAI_KHO_ID"              AS "MA_KHO_NHAP_ID"
                    , D."XUAT_TAI_KHO_ID"              AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                     AS "SO_LUONG"
                    , D."DON_GIA"                      AS "DON_GIA"
                    , D."TIEN_VON"                     AS "SO_TIEN"
                    , D."TIEN_VON_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , 0                                AS "TY_LE_CHIET_KHAU"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN"                    AS "TONG_TIEN"
                    , M."TONG_TIEN"                    AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                      AS "TSCD_ID"
                    , NULL :: INT                      AS "LOAI_TSCD_ID"
                    , NULL :: INT                      AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                    AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                 AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"              AS "DON_DAT_HANG_ID"
                    , NULL :: INT                      AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"              AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                      AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"               AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                    AS "DIEN_GIAI_CHUNG"
                    , ''                               AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                       AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                    AS "DON_VI_ID_CT"
                    , M."state"                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                 AS "CHI_NHANH_ID"
                    , D.id                             AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                    AS "SOURCE_ID"
                FROM stock_ex_nhap_xuat_kho M
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M.id = D."NHAP_XUAT_ID"
                WHERE M.type = 'CHUYEN_KHO'

                UNION ALL

                SELECT
                    M.id                             AS "ID_GOC"
                    , 'stock.ex.nhap.xuat.kho' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                  AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"               AS "NGAY_HACH_TOAN"
                    , NULL :: INT                      AS "currency_id"
                    , CASE WHEN M."LOAI_XUAT_KHO" = 'XUAT_HANG'
                    THEN M."SO_CHUNG_TU_CK_READONLY"
                    ELSE '' END                      AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)               AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                     AS "TK_NO_ID"
                    , D."TK_CO_ID"                     AS "TK_CO_ID"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID"
                    , D."TEN_HANG"                     AS "TEN_HANG"
                    , D."DVT_ID"                       AS "DVT_ID"
                    , D."NHAP_TAI_KHO_ID"              AS "MA_KHO_NHAP_ID"
                    , D."KHO_ID"                       AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                     AS "SO_LUONG"
                    , D."DON_GIA_VON"                  AS "DON_GIA"
                    , D."TIEN_VON"                     AS "SO_TIEN"
                    , D."TIEN_VON_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , 0                                AS "TY_LE_CHIET_KHAU"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN"                    AS "TONG_TIEN"
                    , M."TONG_TIEN"                    AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                      AS "TSCD_ID"
                    , NULL :: INT                      AS "LOAI_TSCD_ID"
                    , NULL :: INT                      AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                    AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                 AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"              AS "DON_DAT_HANG_ID"
                    , NULL :: INT                      AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"              AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                      AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"               AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                    AS "DIEN_GIAI_CHUNG"
                    , ''                               AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                       AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                    AS "DON_VI_ID_CT"
                    , M."state"                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                 AS "CHI_NHANH_ID"
                    , D.id                             AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                    AS "SOURCE_ID"
                FROM stock_ex_nhap_xuat_kho M
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M.id = D."NHAP_XUAT_ID"
                WHERE M.type = 'XUAT_KHO'

                UNION ALL


                SELECT
                    M.id                             AS "ID_GOC"
                    , 'stock.ex.nhap.xuat.kho' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                  AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"               AS "NGAY_HACH_TOAN"
                    , NULL :: INT                      AS "currency_id"
                    , ''                               AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)               AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                     AS "TK_NO_ID"
                    , D."TK_CO_ID"                     AS "TK_CO_ID"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID"
                    , D."TEN_HANG"                     AS "TEN_HANG"
                    , D."DVT_ID"                       AS "DVT_ID"
                    , D."KHO_ID"                       AS "MA_KHO_NHAP_ID"
                    , D."XUAT_TAI_KHO_ID"              AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                     AS "SO_LUONG"
                    , D."DON_GIA_VON"                  AS "DON_GIA"
                    , D."TIEN_VON"                     AS "SO_TIEN"
                    , D."TIEN_VON_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , 0                                AS "TY_LE_CHIET_KHAU"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN"                    AS "TONG_TIEN"
                    , M."TONG_TIEN"                    AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                      AS "TSCD_ID"
                    , NULL :: INT                      AS "LOAI_TSCD_ID"
                    , NULL :: INT                      AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                 AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                    AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                 AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"              AS "DON_DAT_HANG_ID"
                    , NULL :: INT                      AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"              AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                      AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"               AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                    AS "DIEN_GIAI_CHUNG"
                    , ''                               AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                       AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                    AS "DON_VI_ID_CT"
                    , M."state"                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                 AS "CHI_NHANH_ID"
                    , D.id                             AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                    AS "SOURCE_ID"
                FROM stock_ex_nhap_xuat_kho M
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M.id = D."NHAP_XUAT_ID"
                WHERE M.type = 'NHAP_KHO'


                UNION ALL


                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'purchase.ex.tra.lai.hang.mua' :: TEXT        AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                             AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                               AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , D1."SO_HOA_DON"                               AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                             AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                  AS "TK_NO_ID"
                    , D."TK_CO_ID"                                  AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID"
                    , D."TEN_HANG"                                  AS "TEN_HANG"
                    , D."DVT_ID"                                    AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , D."KHO_ID"                                    AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                  AS "SO_LUONG"
                    , D."DON_GIA"                                   AS "DON_GIA"
                    , (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                    THEN D."THANH_TIEN" + D."TIEN_THUE_GTGT"
                        ELSE D."THANH_TIEN"
                        END)                                         AS "SO_TIEN"
                    , (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                    THEN D."THANH_TIEN" + D."TIEN_THUE_GTGT"
                        ELSE D."THANH_TIEN"
                        END)                                         AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" + M."TIEN_THUE_GTGT"       AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ" + M."TIEN_THUE_GTGT_QĐ" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                           AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                           AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                   AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                            AS "MA_THONG_KE_ID"
                    , M."LY_DO_NOP"                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                    AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID_CT"
                    , M."state"                                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"
                FROM purchase_ex_tra_lai_hang_mua M
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet D ON M.id = D."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                    LEFT JOIN sale_ex_hoa_don_ban_hang D1
                        ON D1."SOURCE_ID" = concat('purchase.ex.tra.lai.hang.mua', ',', M.id)

                UNION ALL


                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'purchase.ex.tra.lai.hang.mua' :: TEXT        AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                             AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                               AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , M."SO_HOA_DON"                                AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                              AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                  AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"                           AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID"
                    , D."TEN_HANG"                                  AS "TEN_HANG"
                    , D."DVT_ID"                                    AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , D."KHO_ID"                                    AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                  AS "SO_LUONG"
                    , D."DON_GIA"                                   AS "DON_GIA"
                    , M."TIEN_THUE_GTGT"                            AS "SO_TIEN"
                    , "TIEN_THUE_GTGT_QUY_DOI"                      AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" + M."TIEN_THUE_GTGT"       AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ" + M."TIEN_THUE_GTGT_QĐ" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                           AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                           AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                   AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                            AS "MA_THONG_KE_ID"
                    , M."LY_DO_NOP"                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                    AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID_CT"
                    , M."state"                                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"
                FROM purchase_ex_tra_lai_hang_mua M
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet D ON M.id = D."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                    LEFT JOIN sale_ex_hoa_don_ban_hang D1
                        ON D1."SOURCE_ID" = concat('purchase.ex.tra.lai.hang.mua', ',', M.id)
                WHERE D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0
                            OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0
                    )


                UNION ALL


                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                                 AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                                      AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU" + D."TIEN_THUE_GTGT"             AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI" - D."TIEN_CHIET_KHAU_QUY_DOI" +
                    D."TIEN_THUE_GTGT_QUY_DOI"                                            AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."DIEN_GIAI_CHUNG"                                                   AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (352, 357, 358, 359, 360, 362, 363, 364, 365, 366)
                    AND (D."TK_THUE_GTGT_ID" ISNULL OR M."LOAI_HOA_DON" <> '1')

                UNION ALL

                -- 2222222222
                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                                 AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                                      AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU"                                  AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI" -
                    D."TIEN_CHIET_KHAU_QUY_DOI"                                           AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312, 352, 362, 368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (352, 357, 358, 359, 360, 362, 363, 364, 365, 366)
                    AND (D."TK_THUE_GTGT_ID" NOTNULL OR M."LOAI_HOA_DON" = '1')


                UNION ALL

                -- 333333333333333
                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                                 AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                                      AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                                                   AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                                    AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                            AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312, 352, 362, 368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (352, 357, 358, 359, 360, 362, 363, 364, 365, 366)
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                -- 44444444444444
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                      AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_CO_ID"                                               AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU"                       AS "SO_TIEN"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU_QUY_DOI"               AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (368, 369, 370, 371, 372, 374, 375, 376, 377, 378)


                UNION ALL

                -- 555555555555555555555
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                      AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_BVMT"                                           AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_BVMT"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_BVMT_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                    AND D."TK_THUE_BVMT" NOTNULL
                    AND (D."TIEN_THUE_BVMT" <> 0 OR D."TIEN_THUE_BVMT_QUY_DOI" <> 0)


                UNION ALL

                -- 6666666666666666
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                      AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_NK_ID"                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_NK"                                           AS "SO_TIEN"
                    , D."TIEN_THUE_NK_QUY_DOI"                                   AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                    AND D."TK_THUE_NK_ID" NOTNULL
                    AND (D."TIEN_THUE_NK" <> 0 OR D."TIEN_THUE_NK_QUY_DOI" <> 0)


                UNION ALL

                -- 7777777777777777
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                      AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_TTDB_ID"                                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_TTDB"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_TTDB_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                    AND D."TK_THUE_TTDB_ID" NOTNULL
                    AND (D."TIEN_THUE_TTDB" <> 0 OR D."TIEN_THUE_TTDB_QUY_DOI" <> 0)


                UNION ALL

                -- 8888888888888888888888
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                      AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                           AS "NGAY_HOA_DON"
                    , D."TK_DU_THUE_GTGT_ID"                                        AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"                                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                    AND D."TK_DU_THUE_GTGT_ID" NOTNULL
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                -- 999999999999999
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                      AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"                                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (368, 374)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                    AND D."TK_DU_THUE_GTGT_ID" NOTNULL
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                -- 10000000000000
                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D1."SO_HOA_DON"                                                       AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                                     AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU" + D."TIEN_THUE_GTGT"             AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI" - D."TIEN_CHIET_KHAU_QUY_DOI" +
                    D."TIEN_THUE_GTGT_QUY_DOI"                                            AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312, 313, 314, 315, 316)
                    AND (D."TK_THUE_GTGT_ID" ISNULL OR M."LOAI_HOA_DON" <> '1')


                UNION ALL

                -- 11-11111111111111111
                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D1."SO_HOA_DON"                                                       AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                                     AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU"                                  AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI" -
                    D."TIEN_CHIET_KHAU_QUY_DOI"                                           AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312, 313, 314, 315, 316)
                    AND (D."TK_THUE_GTGT_ID" NOTNULL OR M."LOAI_HOA_DON" = '1')

                UNION ALL

                -- 12-22222222222
                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D1."SO_HOA_DON"                                                       AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                                     AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                                                   AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                                    AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                            AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312, 313, 314, 315, 316)
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND M."LOAI_HOA_DON" = '1'
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                -- 13-3333333333
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D1."SO_HOA_DON"                                            AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                          AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_CO_ID"                                               AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."THANH_TIEN" - D."TIEN_CHIET_KHAU"                       AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI" - D."TIEN_CHIET_KHAU_QUY_DOI"       AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)


                UNION ALL

                -- 14-44444444444
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D1."SO_HOA_DON"                                            AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                          AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_BVMT"                                           AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_BVMT"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_BVMT_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)
                    AND D."TK_THUE_BVMT" NOTNULL
                    AND (D."TIEN_THUE_BVMT" <> 0 OR D."TIEN_THUE_BVMT_QUY_DOI" <> 0)


                UNION ALL

                -- 15-5555555555555
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D1."SO_HOA_DON"                                            AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                          AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_NK_ID"                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_NK"                                           AS "SO_TIEN"
                    , D."TIEN_THUE_NK_QUY_DOI"                                   AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)
                    AND D."TK_THUE_NK_ID" NOTNULL
                    AND (D."TIEN_THUE_NK" <> 0 OR D."TIEN_THUE_NK_QUY_DOI" <> 0)


                UNION ALL

                -- 16-6666666666
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D1."SO_HOA_DON"                                            AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                          AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_TTDB_ID"                                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_TTDB"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_TTDB_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)
                    AND D."TK_THUE_TTDB_ID" NOTNULL
                    AND (D."TIEN_THUE_TTDB" <> 0 OR D."TIEN_THUE_TTDB_QUY_DOI" <> 0)


                UNION ALL

                -- 17-777777777777
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D1."SO_HOA_DON"                                            AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                          AS "NGAY_HOA_DON"
                    , D."TK_DU_THUE_GTGT_ID"                                        AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"                                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                -- 18-8888888888
                SELECT
                    M.id                                                       AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                         AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                            AS "currency_id"
                    , D1."SO_HOA_DON"                                            AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                                          AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                               AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"                                        AS "TK_CO_ID"
                    , D."TK_THUE_GTGT_ID"                                        AS "MA_HANG_ID"
                    , D.name                                                     AS "TEN_HANG"
                    , D."DVT_ID"                                                 AS "DVT_ID"
                    , D."KHO_ID"                                                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                               AS "SO_LUONG"
                    , D."DON_GIA"                                                AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                         AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                AS "TSCD_ID"
                    , NULL :: INT                                                AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                           AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                        AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                              AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324)
                    THEN M."DIEN_GIAI_CHUNG"
                        ELSE M."LY_DO_CHI"
                        END)                                                      AS "DIEN_GIAI_CHUNG"
                    , ''                                                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                      AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                              AS "DON_VI_ID_CT"
                    , M.state                                                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                           AS "CHI_NHANH_ID"
                    , D.id                                                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                        AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."SOURCE_ID" = concat('purchase.document', ',', M.id)
                WHERE M.type = 'hang_hoa' AND M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)
                    AND D."TK_DU_THUE_GTGT_ID" NOTNULL
                    AND D."TK_DU_THUE_GTGT_ID" ISNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                                 AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                                      AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , (CASE WHEN D."THUE_GTGT_ID" IS NULL
                    THEN coalesce(D."THANH_TIEN", 0) - coalesce(D."TIEN_CHIET_KHAU", 0) + coalesce(D."TIEN_THUE_GTGT", 0)
                        ELSE coalesce(D."THANH_TIEN", 0) - coalesce(D."TIEN_CHIET_KHAU", 0)
                        END)                                                                 AS "SO_TIEN"
                    , (CASE WHEN D."THUE_GTGT_ID" IS NULL
                    THEN coalesce(D."THANH_TIEN_QUY_DOI", 0) - coalesce(D."TIEN_CHIET_KHAU_QUY_DOI", 0) +
                        coalesce(D."TIEN_THUE_GTGT_QUY_DOI", 0)
                        ELSE coalesce(D."THANH_TIEN_QUY_DOI", 0) - coalesce(D."TIEN_CHIET_KHAU_QUY_DOI", 0)
                        END)                                                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."LY_DO_CHI"                                                         AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'dich_vu'


                UNION ALL


                SELECT
                    M.id                                                                  AS "ID_GOC"
                    , 'purchase.document' :: TEXT                                           AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                       AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                    AS "NGAY_HACH_TOAN"
                    , M."currency_id"                                                       AS "currency_id"
                    , D."SO_HOA_DON_DETAIL"                                                 AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                                                      AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                                                   AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                          AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID"
                    , D.name                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                            AS "DVT_ID"
                    , D."KHO_ID"                                                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                          AS "SO_LUONG"
                    , D."DON_GIA"                                                           AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                                                    AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                                            AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                          AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                                                   AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" - M."SO_TIEN_CHIET_KHAU" + M."TONG_TIEN_THUE_GTGT" AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI" - M."TONG_TIEN_CK_GTGT_QUY_DOI" +
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                                           AS "TSCD_ID"
                    , NULL :: INT                                                           AS "LOAI_TSCD_ID"
                    , NULL :: INT                                                           AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                                                      AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                      AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                                                   AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_CHI_ID"                                                         AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."LY_DO_CHI"                                                         AS "DIEN_GIAI_CHUNG"
                    , ''                                                                    AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                        AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                            AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                 AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                                                   AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                         AS "DON_VI_ID_CT"
                    , M.state                                                               AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                      AS "CHI_NHANH_ID"
                    , D.id                                                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                   AS "SOURCE_ID"

                FROM purchase_document M
                    INNER JOIN purchase_document_line D ON M.id = D."order_id"
                WHERE M.type = 'dich_vu' AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)

                UNION ALL

                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'purchase.ex.giam.gia.hang.mua' :: TEXT       AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                             AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                               AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , M."SO_HOA_DON"                                AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                              AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                  AS "TK_NO_ID"
                    , D."TK_CO_ID"                                  AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID"
                    , D."TEN_HANG"                                  AS "TEN_HANG"
                    , D."DVT_ID"                                    AS "DVT_ID"
                    , D."KHO_ID"                                    AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                  AS "SO_LUONG"
                    , D."DON_GIA"                                   AS "DON_GIA"
                    , (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                    THEN D."THANH_TIEN" + D."TIEN_THUE_GTGT"
                        ELSE D."THANH_TIEN"
                        END)                                         AS "SO_TIEN"
                    , (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                    THEN D."THANH_TIEN_QUY_DOI" + D."TIEN_THUE_GTGT_QUY_DOI"
                        ELSE D."THANH_TIEN_QUY_DOI"
                        END)                                         AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" + M."TIEN_THUE_GTGT"       AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QD" + M."TIEN_THUE_GTGT_QD" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                           AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                   AS "DON_MUA_HANG_ID"
                    , NULL :: INT                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                   AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                            AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                    AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID_CT"
                    , M."state"                                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"
                FROM purchase_ex_giam_gia_hang_mua M
                    INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet D ON M.id = D."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1
                        ON concat('purchase.ex.giam.gia.hang.mua', ',', M.id) = D1."SOURCE_ID"


                UNION ALL


                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'purchase.ex.giam.gia.hang.mua' :: TEXT       AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                             AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                               AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                             AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , M."SO_HOA_DON"                                AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                              AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                  AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"                           AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID"
                    , D."TEN_HANG"                                  AS "TEN_HANG"
                    , D."DVT_ID"                                    AS "DVT_ID"
                    , D."KHO_ID"                                    AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                  AS "SO_LUONG"
                    , D."DON_GIA"                                   AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                            AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"                    AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG" + M."TIEN_THUE_GTGT"       AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QD" + M."TIEN_THUE_GTGT_QD" AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                           AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                   AS "DON_MUA_HANG_ID"
                    , NULL :: INT                                   AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                   AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                            AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                 AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                    AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID_CT"
                    , M."state"                                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"
                FROM purchase_ex_giam_gia_hang_mua M
                    INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet D ON M.id = D."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang D1
                        ON concat('purchase.ex.giam.gia.hang.mua', ',', M.id) = D1."SOURCE_ID"
                WHERE D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 AND D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL


                SELECT
                    M.id                                   AS "ID_GOC"
                    , 'purchase.ex.hoa.don.mua.hang' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                      AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                        AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU"Management AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"                      AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                     AS "NGAY_HACH_TOAN"
                    , M."currency_id"                        AS "currency_id"
                    , M."SO_HOA_DON"                         AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                       AS "NGAY_HOA_DON"
                    , D."TK_THUE_ID"                         AS "TK_NO_ID"
                    , D."TK_CO_ID"                           AS "TK_CO_ID"
                    , D."MA_HANG_ID"                         AS "MA_HANG_ID"
                    , D."TEN_HANG"                           AS "TEN_HANG"
                    , NULL                                   AS "DVT_ID"
                    , NULL                                   AS "MA_KHO_NHAP_ID"
                    , NULL                                   AS "MA_KHO_XUAT_ID"
                    , 0                                      AS "SO_LUONG"
                    , 0                                      AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                     AS "SO_TIEN"
                    , --             D."SO_TIEN_THUE_VAT"OC AS "SO_TIEN"Management ,
                    D."TIEN_THUE_GTGT_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , --             D."SO_TIEN_THUE_VAT" AS "SO_TIEN_QUY_DOI"Management ,
                    0                                      AS "TY_LE_CHIET_KHAU"
                    , 0                                      AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                      AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_THUE_GTGT"                AS "TONG_TIEN"
                    , --             M.Total"SO_TIEN_THUE_VAT"OC AS "TONG_TIEN"Management ,
                    M."TONG_TIEN_THUE_GTGT_QUY_DOI"        AS "TONG_TIEN_QUY_DOI"
                    , --             M.Total"SO_TIEN_THUE_VAT" AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL                                   AS "TSCD_ID"
                    , NULL :: INT                            AS "LOAI_TSCD_ID"
                    , NULL                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                       AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                       AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                       AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                          AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                       AS "NHAN_VIEN_ID"
                    , NULL :: INT                            AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                      AS "CONG_TRINH_ID"
                    , NULL :: INT                            AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                            AS "DON_DAT_HANG_ID"
                    , NULL :: INT                            AS "DON_MUA_HANG_ID"
                    , --HHSon 15.07.2016 fix bug 110867: (CR 81477 bổ sung đơn mua hàng trên Nhận hóa đơn)
                    --             D.ContractID AS ContractID ,
                    D."HOP_DONG_MUA_ID"                    AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                            AS "HOP_DONG_BAN_ID"
                    , NULL                                   AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                     AS "MA_THONG_KE_ID"
                    , --             D.PurchasePurposeID AS PurchasePurposeID ,
                    M."DIEN_GIAI"                          AS "DIEN_GIAI_CHUNG"
                    , ''                                     AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                         AS "MA_HANG_ID_CT"
                    , NULL                                   AS "DVT_ID_CT"
                    , NULL :: INT                            AS "DOI_TUONG_THCP_ID_CT"
                    , --             D.ContractID AS DetailContractID ,
                    NULL :: INT                            AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                            AS "DON_VI_ID_CT"
                    , M."state"                              AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"                       AS "CHI_NHANH_ID"
                    , D.id                                   AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                          AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/
                --             CONVERT(date ,M.CreatedDate) AS CreatedDate ,
                -- 			M.CreatedBy ,
                -- 			CONVERT(date ,M.ModifiedDate) AS ModifiedDate ,
                -- 			M.ModifiedBy
                FROM purchase_ex_hoa_don_mua_hang M
                    INNER JOIN purchase_ex_hoa_don_mua_hang_chi_tiet D ON M.id = D."HOA_DON_MUA_HANG_ID"


                UNION ALL


                SELECT
                    M.id                                AS "ID_GOC"
                    , 'sale.ex.giam.gia.hang.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                   AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                     AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                   AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                  AS "NGAY_HACH_TOAN"
                    , M.currency_id                       AS "currency_id"
                    , D1."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                        AS "TK_NO_ID"
                    , D."TK_CO_ID"                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                      AS "MA_HANG_ID"
                    , D."TEN_HANG"                        AS "TEN_HANG"
                    , D."DVT_ID"                          AS "DVT_ID"
                    , NULL                                AS "MA_KHO_NHAP_ID"
                    , NULL                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                        AS "SO_LUONG"
                    , D."DON_GIA"                         AS "DON_GIA"
                    , D."THANH_TIEN"                      AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI"              AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CHIET_KHAU_PHAN_TRAM"      AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                 AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"         AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                  AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"               AS "TONG_TIEN_QUY_DOI"
                    , NULL                                AS "TSCD_ID"
                    , NULL :: INT                         AS "LOAI_TSCD_ID"
                    , NULL                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                    AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN ('3550', '3551')
                    THEN M."DOI_TUONG_ID"
                        ELSE M."DON_VI_GIAO_DAI_LY_ID"
                        END)                               AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                    AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                       AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                    AS "NHAN_VIEN_ID"
                    , NULL :: INT                         AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                   AS "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                 AS "DON_DAT_HANG_ID"
                    , NULL                                AS "DON_MUA_HANG_ID"
                    , NULL                                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                 AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_NGAN_HANG_ID"
                    , D."MA_THONG_KE_ID"                  AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                       AS "DIEN_GIAI_CHUNG"
                    , ''                                  AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                      AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                          AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"               AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                         AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                       AS "DON_VI_ID_CT"
                    , M."state"                           AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                    AS "CHI_NHANH_ID"
                    , D.id                                AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                 AS "SOURCE_ID"
                FROM sale_ex_giam_gia_hang_ban M
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M.id = D."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN sale_ex_hoa_don_ban_hang D1
                        ON concat('sale.ex.giam.gia.hang.ban', ',', M.id) = D1."SOURCE_ID"


                UNION ALL


                SELECT
                    M.id                                AS "ID_GOC"
                    , 'sale.ex.giam.gia.hang.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                   AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                     AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                   AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                  AS "NGAY_HACH_TOAN"
                    , M.currency_id                       AS "currency_id"
                    , D1."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , D."TK_CO_ID"                        AS "TK_NO_ID"
                    , D."TK_CHIET_KHAU_ID"                AS "TK_CO_ID"
                    , D."MA_HANG_ID"                      AS "MA_HANG_ID"
                    , D."TEN_HANG"                        AS "TEN_HANG"
                    , D."DVT_ID"                          AS "DVT_ID"
                    , NULL                                AS "MA_KHO_NHAP_ID"
                    , NULL                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                        AS "SO_LUONG"
                    , D."DON_GIA"                         AS "DON_GIA"
                    , D."TIEN_CHIET_KHAU"                 AS "SO_TIEN"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"         AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CHIET_KHAU_PHAN_TRAM"      AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                 AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"         AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                  AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"               AS "TONG_TIEN_QUY_DOI"
                    , NULL                                AS "TSCD_ID"
                    , NULL :: INT                         AS "LOAI_TSCD_ID"
                    , NULL                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                    AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN ('3550', '3551')
                    THEN M."DOI_TUONG_ID"
                        ELSE M."DON_VI_GIAO_DAI_LY_ID"
                        END)                               AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                    AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                       AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                    AS "NHAN_VIEN_ID"
                    , NULL :: INT                         AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                   AS "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                 AS "DON_DAT_HANG_ID"
                    , NULL                                AS "DON_MUA_HANG_ID"
                    , NULL                                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                 AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_NGAN_HANG_ID"
                    , D."MA_THONG_KE_ID"                  AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                       AS "DIEN_GIAI_CHUNG"
                    , ''                                  AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                      AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                          AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"               AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                         AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                       AS "DON_VI_ID_CT"
                    , M."state"                           AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                    AS "CHI_NHANH_ID"
                    , D.id                                AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                 AS "SOURCE_ID"
                FROM sale_ex_giam_gia_hang_ban M
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M.id = D."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN sale_ex_hoa_don_ban_hang D1
                        ON concat('sale.ex.giam.gia.hang.ban', ',', M.id) = D1."SOURCE_ID"
                WHERE D."TK_CHIET_KHAU_ID" NOTNULL
                    AND (D."TIEN_CHIET_KHAU" <> 0 OR D."TIEN_CHIET_KHAU_QUY_DOI" <> 0)


                UNION ALL


                SELECT
                    M.id                                AS "ID_GOC"
                    , 'sale.ex.giam.gia.hang.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                   AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                     AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                   AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                  AS "NGAY_HACH_TOAN"
                    , M.currency_id                       AS "currency_id"
                    , D1."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , D1."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                 AS "TK_NO_ID"
                    , D."TK_CO_ID"                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                      AS "MA_HANG_ID"
                    , D."TEN_HANG"                        AS "TEN_HANG"
                    , D."DVT_ID"                          AS "DVT_ID"
                    , NULL                                AS "MA_KHO_NHAP_ID"
                    , NULL                                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                        AS "SO_LUONG"
                    , D."DON_GIA"                         AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                  AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"          AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CHIET_KHAU_PHAN_TRAM"      AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                 AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"         AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                  AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"               AS "TONG_TIEN_QUY_DOI"
                    , NULL                                AS "TSCD_ID"
                    , NULL :: INT                         AS "LOAI_TSCD_ID"
                    , NULL                                AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                    AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN ('3550', '3551')
                    THEN M."DOI_TUONG_ID"
                        ELSE M."DON_VI_GIAO_DAI_LY_ID"
                        END)                               AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                    AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                       AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                    AS "NHAN_VIEN_ID"
                    , NULL :: INT                         AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                   AS "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                 AS "DON_DAT_HANG_ID"
                    , NULL                                AS "DON_MUA_HANG_ID"
                    , NULL                                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                 AS "HOP_DONG_BAN_ID"
                    , M."TAI_KHOAN_NGAN_HANG_ID"
                    , D."MA_THONG_KE_ID"                  AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                       AS "DIEN_GIAI_CHUNG"
                    , ''                                  AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                      AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                          AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"               AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                         AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                       AS "DON_VI_ID_CT"
                    , M."state"                           AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                    AS "CHI_NHANH_ID"
                    , D.id                                AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                 AS "SOURCE_ID"
                FROM sale_ex_giam_gia_hang_ban M
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M.id = D."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN sale_ex_hoa_don_ban_hang D1
                        ON concat('sale.ex.giam.gia.hang.ban', ',', M.id) = D1."SOURCE_ID"
                WHERE D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL

                -- 1
                SELECT
                    M.id                    AS "ID_GOC"
                    , 'sale.document' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"       AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"         AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"       AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"      AS "NGAY_HACH_TOAN"
                    , M.currency_id           AS "currency_id"
                    , M."SO_HOA_DON"          AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"        AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"            AS "TK_NO_ID"
                    , D."TK_THUE_XK_ID"       AS "TK_CO_ID"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID"
                    , D."TEN_HANG"            AS "TEN_HANG"
                    , D."DVT_ID"              AS "DVT_ID"
                    , D."KHO_ID"              AS "MA_KHO_NHAP_ID"
                    , NULL                    AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"            AS "SO_LUONG"
                    , D."DON_GIA"             AS "DON_GIA"
                    , 0                       AS "SO_TIEN"
                    , D."TIEN_THUE_XUAT_KHAU" AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"            AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CK_QUY_DOI"     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"      AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"   AS "TONG_TIEN_QUY_DOI"
                    , NULL                    AS "TSCD_ID"
                    , NULL :: INT             AS "LOAI_TSCD_ID"
                    , NULL                    AS "CCDC_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"        AS "NHAN_VIEN_ID"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , NULL                    AS "DON_DAT_HANG_ID"
                    , NULL                    AS "DON_MUA_HANG_ID"
                    , NULL                    AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"     AS "HOP_DONG_BAN_ID"
                    , NULL                    AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"           AS "DIEN_GIAI_CHUNG"
                    , ''                      AS "DIEN_GIAI"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID_CT"
                    , D."DVT_ID"              AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"           AS "DON_VI_ID_CT"
                    , M.state                 AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"        AS "CHI_NHANH_ID"
                    , D.id                    AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)     AS "SOURCE_ID"
                FROM sale_document M
                    INNER JOIN sale_document_line D ON M.id = D."SALE_DOCUMENT_ID"
                WHERE M."LOAI_CHUNG_TU" = 3532
                    AND D."TK_THUE_XK_ID" NOTNULL
                    AND D."TIEN_THUE_XUAT_KHAU" <> 0
                UNION ALL

                -- 2
                SELECT
                    M.id                                                                        AS "ID_GOC"
                    , 'sale.document' :: TEXT                                                     AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                                                           AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                                                             AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                                                           AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                                                          AS "NGAY_HACH_TOAN"
                    , M.currency_id                                                               AS "currency_id"
                    , M."SO_HOA_DON"                                                              AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                                                            AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                                                AS "TK_NO_ID"
                    , D."TK_CO_ID"                                                                AS "TK_CO_ID"
                    , D."MA_HANG_ID"                                                              AS "MA_HANG_ID"
                    , D."TEN_HANG"                                                                AS "TEN_HANG"
                    , D."DVT_ID"                                                                  AS "DVT_ID"
                    , D."KHO_ID"                                                                  AS "MA_KHO_NHAP_ID"
                    , NULL                                                                        AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                                                                AS "SO_LUONG"
                    , D."DON_GIA"                                                                 AS "DON_GIA"
                    , coalesce(D."THANH_TIEN", 0) + coalesce(D."TIEN_THUE_GTGT", 0) - coalesce(D."TIEN_CHIET_KHAU",
                                                                                                0) AS "SO_TIEN"
                    , coalesce(D."THANH_TIEN_QUY_DOI", 0) + coalesce(D."TIEN_THUE_GTGT_QUY_DOI", 0) -
                    coalesce(D."TIEN_CK_QUY_DOI",
                                0)                                                                 AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                                                                AS "TY_LE_CHIET_KHAU"
                    ,
                    D."TIEN_CHIET_KHAU"                                                         AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    ,
                    D."TIEN_CK_QUY_DOI"                                                         AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                                                          AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"                                                       AS "TONG_TIEN_QUY_DOI"
                    , NULL                                                                        AS "TSCD_ID"
                    , NULL :: INT                                                                 AS "LOAI_TSCD_ID"
                    , NULL                                                                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                                                            AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                                                            AS "DOI_TUONG_NO_ID"
                    , M."DON_VI_GIAO_DAI_LY_ID"                                                   AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                                                            AS "NHAN_VIEN_ID"
                    , NULL :: INT                                                                 AS "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , NULL                                                                        AS "DON_DAT_HANG_ID"
                    , NULL                                                                        AS "DON_MUA_HANG_ID"
                    , NULL                                                                        AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                                                         AS "HOP_DONG_BAN_ID"
                    , NULL                                                                        AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                                               AS "DIEN_GIAI_CHUNG"
                    , ''                                                                          AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                                                              AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                                                                  AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                                                       AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                                                 AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                                               AS "DON_VI_ID_CT"
                    , M.state                                                                     AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                                                            AS "CHI_NHANH_ID"
                    , D.id                                                                        AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                                                         AS "SOURCE_ID"
                FROM sale_document M
                    INNER JOIN sale_document_line D ON M.id = D."SALE_DOCUMENT_ID"
                WHERE M."LOAI_CHUNG_TU" IN (3534, 3535, 3536, 3538)

                UNION ALL
                -- 3
                SELECT
                    M.id                    AS "ID_GOC"
                    , 'sale.document' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"       AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"         AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"       AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"      AS "NGAY_HACH_TOAN"
                    , M.currency_id           AS "currency_id"
                    , M."SO_HOA_DON"          AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"        AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"            AS "TK_NO_ID"
                    , D."TK_THUE_XK_ID"       AS "TK_CO_ID"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID"
                    , D."TEN_HANG"            AS "TEN_HANG"
                    , D."DVT_ID"              AS "DVT_ID"
                    , D."KHO_ID"              AS "MA_KHO_NHAP_ID"
                    , NULL                    AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"            AS "SO_LUONG"
                    , D."DON_GIA"             AS "DON_GIA"
                    , D."TIEN_THUE_XUAT_KHAU" AS "SO_TIEN"
                    , D."TIEN_THUE_XUAT_KHAU" AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"            AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"     AS "SO_TIEN_CHIET_KHAU"
                    , D."TIEN_CK_QUY_DOI"     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"      AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"   AS "TONG_TIEN_QUY_DOI"
                    , NULL                    AS "TSCD_ID"
                    , NULL :: INT             AS "LOAI_TSCD_ID"
                    , NULL                    AS "CCDC_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"        AS "NHAN_VIEN_ID"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , NULL                    AS "DON_DAT_HANG_ID"
                    , NULL                    AS "DON_MUA_HANG_ID"
                    , NULL                    AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"     AS "HOP_DONG_BAN_ID"
                    , NULL                    AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"           AS "DIEN_GIAI_CHUNG"
                    , ''                      AS "DIEN_GIAI"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID_CT"
                    , D."DVT_ID"              AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"           AS "DON_VI_ID_CT"
                    , M.state                 AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"        AS "CHI_NHANH_ID"
                    , D.id                    AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)     AS "SOURCE_ID"
                FROM sale_document M
                    INNER JOIN sale_document_line D ON M.id = D."SALE_DOCUMENT_ID"
                WHERE M."LOAI_CHUNG_TU" IN (3534, 3535, 3536, 3538)
                    AND D."TK_THUE_XK_ID" NOTNULL
                    AND D."TIEN_THUE_XUAT_KHAU" <> 0


                UNION ALL
                -- 4
                SELECT
                    M.id                    AS "ID_GOC"
                    , 'sale.document' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"       AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"         AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"       AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"      AS "NGAY_HACH_TOAN"
                    , M.currency_id           AS "currency_id"
                    , M."SO_HOA_DON"          AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"        AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"            AS "TK_NO_ID"
                    , D."TK_CO_ID"            AS "TK_CO_ID"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID"
                    , D."TEN_HANG"            AS "TEN_HANG"
                    , D."DVT_ID"              AS "DVT_ID"
                    , NULL :: INT             AS "MA_KHO_NHAP_ID"
                    , NULL :: INT             AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"            AS "SO_LUONG"
                    , D."DON_GIA"             AS "DON_GIA"
                    , D."THANH_TIEN"          AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" = 3532
                    THEN coalesce(D."THANH_TIEN_QUY_DOI", 0) - coalesce(D."TIEN_THUE_XUAT_KHAU", 0)
                    ELSE D."THANH_TIEN_QUY_DOI"
                    END                     AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"            AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"     AS "SO_TIEN_CHIET_KHAU"
                    , D."TIEN_CK_QUY_DOI"     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"      AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"   AS "TONG_TIEN_QUY_DOI"
                    , NULL                    AS "TSCD_ID"
                    , NULL :: INT             AS "LOAI_TSCD_ID"
                    , NULL                    AS "CCDC_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"        AS "NHAN_VIEN_ID"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , NULL                    AS "DON_DAT_HANG_ID"
                    , NULL                    AS "DON_MUA_HANG_ID"
                    , NULL                    AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"     AS "HOP_DONG_BAN_ID"
                    , NULL                    AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"           AS "DIEN_GIAI_CHUNG"
                    , ''                      AS "DIEN_GIAI"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID_CT"
                    , D."DVT_ID"              AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"           AS "DON_VI_ID_CT"
                    , M.state                 AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"        AS "CHI_NHANH_ID"
                    , D.id                    AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)     AS "SOURCE_ID"
                FROM sale_document M
                    INNER JOIN sale_document_line D ON M.id = D."SALE_DOCUMENT_ID"
                    INNER JOIN res_currency C ON M.currency_id = C.id
                WHERE M."LOAI_CHUNG_TU" NOT IN (3534, 3535, 3536, 3538)


                UNION ALL
                -- 5
                SELECT
                    M.id                    AS "ID_GOC"
                    , 'sale.document' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"       AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"         AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"       AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"      AS "NGAY_HACH_TOAN"
                    , M.currency_id           AS "currency_id"
                    , M."SO_HOA_DON"          AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"        AS "NGAY_HOA_DON"
                    , D."TK_CHIET_KHAU_ID"    AS "TK_NO_ID"
                    , D."TK_NO_ID"            AS "TK_CO_ID"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID"
                    , D."TEN_HANG"            AS "TEN_HANG"
                    , D."DVT_ID"              AS "DVT_ID"
                    , NULL :: INT             AS "MA_KHO_NHAP_ID"
                    , NULL                    AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"            AS "SO_LUONG"
                    , D."DON_GIA"             AS "DON_GIA"
                    , D."TIEN_CHIET_KHAU"     AS "SO_TIEN"
                    , D."TIEN_CK_QUY_DOI"     AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"            AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CK_QUY_DOI"     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"      AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"   AS "TONG_TIEN_QUY_DOI"
                    , NULL                    AS "TSCD_ID"
                    , NULL :: INT             AS "LOAI_TSCD_ID"
                    , NULL                    AS "CCDC_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"        AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"        AS "NHAN_VIEN_ID"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , NULL                    AS "DON_DAT_HANG_ID"
                    , NULL                    AS "DON_MUA_HANG_ID"
                    , NULL                    AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"     AS "HOP_DONG_BAN_ID"
                    , NULL                    AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"           AS "DIEN_GIAI_CHUNG"
                    , ''                      AS "DIEN_GIAI"
                    , D."MA_HANG_ID"          AS "MA_HANG_ID_CT"
                    , D."DVT_ID"              AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT             AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"           AS "DON_VI_ID_CT"
                    , M.state                 AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"        AS "CHI_NHANH_ID"
                    , D.id                    AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)     AS "SOURCE_ID"
                FROM sale_document M
                    INNER JOIN sale_document_line D ON M.id = D."SALE_DOCUMENT_ID"
                    INNER JOIN res_currency C ON M.currency_id = C.id
                WHERE M."LOAI_CHUNG_TU" NOT IN (3534, 3535, 3536, 3538)
                    AND D."TK_CHIET_KHAU_ID" NOTNULL
                    AND (D."TIEN_CHIET_KHAU" <> 0 OR D."TIEN_CK_QUY_DOI" <> 0)


                UNION ALL
                -- 6
                SELECT
                    M.id                       AS "ID_GOC"
                    , 'sale.document' :: TEXT    AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"          AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"          AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"         AS "NGAY_HACH_TOAN"
                    , M.currency_id              AS "currency_id"
                    , M."SO_HOA_DON"             AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"               AS "TK_NO_ID"
                    , D."TK_THUE_GTGT_ID"        AS "TK_CO_ID"
                    , D."MA_HANG_ID"             AS "MA_HANG_ID"
                    , D."TEN_HANG"               AS "TEN_HANG"
                    , D."DVT_ID"                 AS "DVT_ID"
                    , NULL :: INT                AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"               AS "SO_LUONG"
                    , D."DON_GIA"                AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"         AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI" AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CK_QUY_DOI"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"         AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"      AS "TONG_TIEN_QUY_DOI"
                    , NULL                       AS "TSCD_ID"
                    , NULL :: INT                AS "LOAI_TSCD_ID"
                    , NULL                       AS "CCDC_ID"
                    , M."DOI_TUONG_ID"           AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"           AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"           AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , M."NHAN_VIEN_ID"           AS "NHAN_VIEN_ID"
                    , NULL :: INT                AS "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , NULL                       AS "DON_DAT_HANG_ID"
                    , NULL                       AS "DON_MUA_HANG_ID"
                    , NULL                       AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"        AS "HOP_DONG_BAN_ID"
                    , NULL                       AS "TK_NGAN_HANG"
                    , "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"              AS "DIEN_GIAI_CHUNG"
                    , ''                         AS "DIEN_GIAI"
                    , D."MA_HANG_ID"             AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                 AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"      AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"              AS "DON_VI_ID_CT"
                    , M.state                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"           AS "CHI_NHANH_ID"
                    , D.id                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)        AS "SOURCE_ID"
                FROM sale_document M
                    INNER JOIN sale_document_line D ON M.id = D."SALE_DOCUMENT_ID"
                    INNER JOIN res_currency C ON M.currency_id = C.id
                WHERE M."LOAI_CHUNG_TU" NOT IN (3534, 3535, 3536, 3538)
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'sale.ex.tra.lai.hang.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , CASE WHEN M.selection_chung_tu_ban_hang = 'tra_lai_tien_mat'
                    THEN M."SO_CHUNG_TU_PHIEU_CHI"
                    ELSE M."SO_CHUNG_TU_GIAM_TRU_CONG_NO"
                    END                                AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M.currency_id                      AS "currency_id"
                    , M."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID"
                    , D."TEN_HANG"                       AS "TEN_HANG"
                    , D."DVT_ID"                         AS "DVT_ID"
                    , NULL                               AS "MA_KHO_NHAP_ID"
                    , NULL                               AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                       AS "SO_LUONG"
                    , D."DON_GIA"                        AS "DON_GIA"
                    , D."THANH_TIEN"                     AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK_PHAN_TRAM"             AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                 AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"              AS "TONG_TIEN_QUY_DOI"
                    , NULL                               AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL                               AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN ('3540', '3541')
                    THEN M."DOI_TUONG_ID"
                        ELSE M."DON_VI_GIAO_DAI_LY_ID"
                        END)                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , NULL                               AS "DON_MUA_HANG_ID"
                    , NULL                               AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE"                    AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , ''                                 AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                         AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , NULL :: INT                        AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                AS "SOURCE_ID"
                FROM sale_ex_tra_lai_hang_ban M
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M.id = D."TRA_LAI_HANG_BAN_ID"


                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'sale.ex.tra.lai.hang.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , CASE WHEN M.selection_chung_tu_ban_hang = 'tra_lai_tien_mat'
                    THEN M."SO_CHUNG_TU_PHIEU_CHI"
                    ELSE M."SO_CHUNG_TU_GIAM_TRU_CONG_NO"
                    END                                AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M.currency_id                      AS "currency_id"
                    , M."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID"
                    , D."TEN_HANG"                       AS "TEN_HANG"
                    , D."DVT_ID"                         AS "DVT_ID"
                    , NULL                               AS "MA_KHO_NHAP_ID"
                    , NULL                               AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                       AS "SO_LUONG"
                    , D."DON_GIA"                        AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                 AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI"         AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK_PHAN_TRAM"             AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                 AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"              AS "TONG_TIEN_QUY_DOI"
                    , NULL                               AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL                               AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN ('3540', '3541')
                    THEN M."DOI_TUONG_ID"
                        ELSE M."DON_VI_GIAO_DAI_LY_ID"
                        END)                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , NULL                               AS "DON_MUA_HANG_ID"
                    , NULL                               AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE"                    AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , ''                                 AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                         AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , NULL :: INT                        AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                AS "SOURCE_ID"
                FROM sale_ex_tra_lai_hang_ban M
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M.id = D."TRA_LAI_HANG_BAN_ID"
                WHERE D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)

                UNION ALL


                SELECT
                    M.id                               AS "ID_GOC"
                    , 'sale.ex.tra.lai.hang.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , CASE WHEN M.selection_chung_tu_ban_hang = 'tra_lai_tien_mat'
                    THEN M."SO_CHUNG_TU_PHIEU_CHI"
                    ELSE M."SO_CHUNG_TU_GIAM_TRU_CONG_NO"
                    END                                AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                 AS "NGAY_HACH_TOAN"
                    , M.currency_id                      AS "currency_id"
                    , M."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , D."TK_CO_ID"                       AS "TK_NO_ID"
                    , D."TK_CHIET_KHAU"                  AS "TK_CO_ID"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID"
                    , D."TEN_HANG"                       AS "TEN_HANG"
                    , D."DVT_ID"                         AS "DVT_ID"
                    , NULL                               AS "MA_KHO_NHAP_ID"
                    , NULL                               AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                       AS "SO_LUONG"
                    , D."DON_GIA"                        AS "DON_GIA"
                    , D."TIEN_CHIET_KHAU"                AS "SO_TIEN"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"        AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK_PHAN_TRAM"             AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                 AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QĐ"              AS "TONG_TIEN_QUY_DOI"
                    , NULL                               AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL                               AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN ('3540', '3541')
                    THEN M."DOI_TUONG_ID"
                        ELSE M."DON_VI_GIAO_DAI_LY_ID"
                        END)                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , NULL                               AS "DON_MUA_HANG_ID"
                    , NULL                               AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE"                    AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , ''                                 AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                         AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , M."state"                          AS "TRANG_THAI_GHI_SO"
                    , NULL :: INT                        AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                AS "SOURCE_ID"
                FROM sale_ex_tra_lai_hang_ban M
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M.id = D."TRA_LAI_HANG_BAN_ID"
                WHERE D."TK_CHIET_KHAU" NOTNULL
                    AND (D."TIEN_CHIET_KHAU" <> 0 OR D."TIEN_CHIET_KHAU_QUY_DOI" <> 0)


                UNION ALL


                SELECT
                    M.id                        AS "ID_GOC"
                    , 'supply.dieu.chinh' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"           AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"             AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"           AS "NGAY_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"           AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                 AS "currency_id"
                    , ''                          AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)          AS "NGAY_HOA_DON"
                    , NULL :: INT                 AS "TK_NO_ID"
                    , NULL :: INT                 AS "TK_CO_ID"
                    , NULL :: INT                 AS "MA_HANG_ID"
                    , ''                          AS "TEN_HANG"
                    , NULL :: INT                 AS "DVT_ID"
                    , NULL :: INT                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                 AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                AS "SO_LUONG"
                    , 0                           AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    D."CHENH_LECH_GIA_TRI"      AS "SO_TIEN"
                    , --             D."CHENH_LECH_GIA_TRI AS "SO_TIEN"Management ,
                    D."CHENH_LECH_GIA_TRI"      AS "SO_TIEN_QUY_DOI"
                    , --             D."CHENH_LECH_GIA_TRI AS "SO_TIEN_QUY_DOI"Management ,
                    0                           AS "TY_LE_CHIET_KHAU"
                    , 0                           AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                           AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                           AS "TONG_TIEN"
                    , --             0 AS "TONG_TIEN"Management ,
                    0                           AS "TONG_TIEN_QUY_DOI"
                    , --             0 AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT                 AS "TSCD_ID"
                    , NULL :: INT                 AS "LOAI_TSCD_ID"
                    , D."MA_CCDC"                 AS "CCDC_ID"
                    , NULL :: INT                 AS "DOI_TUONG_ID"
                    , NULL :: INT                 AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                 AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                 AS "DON_VI_ID"
                    , NULL :: INT                 AS "NHAN_VIEN_ID"
                    , NULL :: INT                 AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                 AS "CONG_TRINH_ID"
                    , NULL :: INT                 AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                 AS "DON_DAT_HANG_ID"
                    , NULL :: INT                 AS "DON_MUA_HANG_ID"
                    , --             NULL AS ContractID ,
                    NULL :: INT                 AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                 AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                 AS "TK_NGAN_HANG"
                    , NULL :: INT                 AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    M."LY_DO_DIEU_CHINH"        AS "DIEN_GIAI_CHUNG"
                    , ''                          AS "DIEN_GIAI"
                    , NULL :: INT                 AS "MA_HANG_ID_CT"
                    , NULL :: INT                 AS "DVT_ID_CT"
                    , NULL :: INT                 AS "DOI_TUONG_THCP_ID_CT"
                    , --             NULL AS DetailContractID ,
                    NULL :: INT                 AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                 AS "DON_VI_ID_CT"
                    , M."state"                   AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"            AS "CHI_NHANH_ID"
                    , D.id                        AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)         AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/

                FROM supply_dieu_chinh M
                    INNER JOIN supply_dieu_chinh_chi_tiet D ON M.id = D."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"


                UNION ALL


                SELECT
                    M.id                             AS "ID_GOC"
                    , 'supply.phan.bo.chi.phi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                  AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"                AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"               AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                      AS "currency_id"
                    , ''                               AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)               AS "NGAY_HOA_DON"
                    , NULL :: INT                      AS "TK_NO_ID"
                    , NULL :: INT                      AS "TK_CO_ID"
                    , NULL :: INT                      AS "MA_HANG_ID"
                    , ''                               AS "TEN_HANG"
                    , NULL :: INT                      AS "DVT_ID"
                    , NULL :: INT                      AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                      AS "MA_KHO_XUAT_ID"
                    , 0                                AS "SO_LUONG"
                    , 0                                AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    0                                AS "SO_TIEN"
                    , --             0 AS "SO_TIEN"Management ,
                    0                                AS "SO_TIEN_QUY_DOI"
                    , --             0 AS "SO_TIEN_QUY_DOI"Management ,
                    0                                AS "TY_LE_CHIET_KHAU"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                      AS "TONG_TIEN"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN"Management ,
                    NULL :: INT                      AS "TONG_TIEN_QUY_DOI"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT                      AS "TSCD_ID"
                    , NULL :: INT                      AS "LOAI_TSCD_ID"
                    , D."MA_CCDC"                      AS "CCDC_ID"
                    , NULL :: INT                      AS "DOI_TUONG_ID"
                    , NULL :: INT                      AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                      AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                      AS "DON_VI_ID"
                    , NULL :: INT                      AS "NHAN_VIEN_ID"
                    , NULL :: INT                      AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                      AS "CONG_TRINH_ID"
                    , NULL :: INT                      AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                      AS "DON_DAT_HANG_ID"
                    , NULL :: INT                      AS "DON_MUA_HANG_ID"
                    , --             NULL AS ContractID ,
                    NULL :: INT                      AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                      AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                      AS "TK_NGAN_HANG"
                    , NULL :: INT                      AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    M."DIEN_GIAI"                    AS "DIEN_GIAI_CHUNG"
                    , ''                               AS "DIEN_GIAI"
                    , NULL :: INT                      AS "MA_HANG_ID_CT"
                    , NULL :: INT                      AS "DVT_ID_CT"
                    , NULL :: INT                      AS "DOI_TUONG_THCP_ID_CT"
                    , --             NULL AS DetailContractID ,
                    NULL :: INT                      AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                      AS "DON_VI_ID_CT"
                    , M."state"                        AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"                 AS "CHI_NHANH_ID"
                    , D.id                             AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)              AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/
                FROM supply_phan_bo_chi_phi M
                    INNER JOIN supply_phan_bo_chi_phi_muc_chi_phi D ON M.id = D."PHAN_BO_CHI_PHI_ID"


                UNION ALL


                SELECT
                    M.id                             AS "ID_GOC"
                    , 'supply.phan.bo.chi.phi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                  AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"                AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"               AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                      AS "currency_id"
                    , ''                               AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)               AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                     AS "TK_NO_ID"
                    , D."TK_CO_ID"                     AS "TK_CO_ID"
                    , NULL :: INT                      AS "MA_HANG_ID"
                    , ''                               AS "TEN_HANG"
                    , NULL :: INT                      AS "DVT_ID"
                    , NULL :: INT                      AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                      AS "MA_KHO_XUAT_ID"
                    , 0                                AS "SO_LUONG"
                    , 0                                AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    D."SO_TIEN"                      AS "SO_TIEN"
                    , --             D."SO_TIEN_QUY_DOI" AS "SO_TIEN"Management ,
                    D."SO_TIEN"                      AS "SO_TIEN_QUY_DOI"
                    , --             D."SO_TIEN_QUY_DOI" AS "SO_TIEN_QUY_DOI"Management ,
                    0                                AS "TY_LE_CHIET_KHAU"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                      AS "TONG_TIEN"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN"Management ,
                    NULL :: INT                      AS "TONG_TIEN_QUY_DOI"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT                      AS "TSCD_ID"
                    , NULL :: INT                      AS "LOAI_TSCD_ID"
                    , NULL :: INT                      AS "CCDC_ID"
                    , NULL :: INT                      AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_NO_ID"              AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_CO_ID"              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                    AS "DON_VI_ID"
                    , NULL :: INT                      AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"              AS "DON_DAT_HANG_ID"
                    , NULL :: INT                      AS "DON_MUA_HANG_ID"
                    , --             D.ContractID AS ContractID ,
                    NULL :: INT                      AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                      AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                      AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"               AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    M."DIEN_GIAI"                    AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI"                    AS "DIEN_GIAI"
                    , NULL :: INT                      AS "MA_HANG_ID_CT"
                    , NULL :: INT                      AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID_CT"
                    , --             D.ContractID AS DetailContractID ,
                    D."KHOAN_MUC_CP_ID"              AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                    AS "DON_VI_ID_CT"
                    , M."state"                        AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"                 AS "CHI_NHANH_ID"
                    , D.id                             AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)              AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/

                FROM supply_phan_bo_chi_phi M
                    INNER JOIN supply_phan_bo_chi_phi_hach_toan D ON M.id = D."PHAN_BO_CHI_PHI_ID"


                UNION ALL


                SELECT
                    M.id                                  AS "ID_GOC"
                    , 'supply.ghi.giam' :: TEXT             AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                     AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                       AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_CHUNG_TU"                     AS "NGAY_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                     AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                           AS "currency_id"
                    , ''                                    AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                    AS "NGAY_HOA_DON"
                    , NULL :: INT                           AS "TK_NO_ID"
                    , NULL :: INT                           AS "TK_CO_ID"
                    , NULL :: INT                           AS "MA_HANG_ID"
                    , ''                                    AS "TEN_HANG"
                    , NULL :: INT                           AS "DVT_ID"
                    , NULL :: INT                           AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                           AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG_GHI_GIAM"                 AS "SO_LUONG"
                    , 0                                     AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    D."GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM" AS "SO_TIEN"
                    , --             D.Remaining"SO_TIEN_GHI_GIAM" AS "SO_TIEN"Management ,
                    D."GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM" AS "SO_TIEN_QUY_DOI"
                    , --             D.Remaining"SO_TIEN_GHI_GIAM" AS "SO_TIEN_QUY_DOI"Management ,
                    0                                     AS "TY_LE_CHIET_KHAU"
                    , 0                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                     AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                           AS "TONG_TIEN"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN"Management ,
                    NULL :: INT                           AS "TONG_TIEN_QUY_DOI"
                    , --             M."TONG_TIEN_QUY_DOI" AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT                           AS "TSCD_ID"
                    , NULL :: INT                           AS "LOAI_TSCD_ID"
                    , D."MA_CCDC_ID"                        AS "CCDC_ID"
                    , NULL :: INT                           AS "DOI_TUONG_ID"
                    , NULL :: INT                           AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                           AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_SU_DUNG_ID"                 AS "DON_VI_ID"
                    , NULL :: INT                           AS "NHAN_VIEN_ID"
                    , NULL :: INT                           AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                           AS "CONG_TRINH_ID"
                    , NULL :: INT                           AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                           AS "DON_DAT_HANG_ID"
                    , NULL :: INT                           AS "DON_MUA_HANG_ID"
                    , --             NULL AS ContractID ,
                    NULL :: INT                           AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                           AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                           AS "TK_NGAN_HANG"
                    , NULL :: INT                           AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    M."LY_DO_GHI_GIAM"                    AS "DIEN_GIAI_CHUNG"
                    , ''                                    AS "DIEN_GIAI"
                    , NULL :: INT                           AS "MA_HANG_ID_CT"
                    , NULL :: INT                           AS "DVT_ID_CT"
                    , NULL :: INT                           AS "DOI_TUONG_THCP_ID_CT"
                    , --             NULL AS DetailContractID ,
                    NULL                                  AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_SU_DUNG_ID"                 AS "DON_VI_ID_CT"
                    , M."state"                             AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"                      AS "CHI_NHANH_ID"
                    , D.id                                  AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                   AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/

                FROM supply_ghi_giam M
                    INNER JOIN supply_ghi_giam_chi_tiet D ON M.id = D."CCDC_GHI_GIAM_ID"


                UNION ALL


                SELECT
                    M.id                       AS "ID_GOC"
                    , 'supply.ghi.tang' :: TEXT  AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"          AS "LOAI_CHUNG_TU"
                    , M."SO_CT_GHI_TANG"         AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY_GHI_TANG"          AS "NGAY_CHUNG_TU"
                    , M."NGAY_GHI_TANG"          AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                AS "currency_id"
                    , ''                         AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)         AS "NGAY_HOA_DON"
                    , NULL :: INT                AS "TK_NO_ID"
                    , NULL :: INT                AS "TK_CO_ID"
                    , NULL :: INT                AS "MA_HANG_ID"
                    , ''                         AS "TEN_HANG"
                    , NULL :: INT                AS "DVT_ID"
                    , NULL :: INT                AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"               AS "SO_LUONG"
                    , M."DON_GIA"                AS "DON_GIA"
                    , --             D."DON_GIA" AS "DON_GIA"Management ,
                    round(cast((D."SO_LUONG" * M."DON_GIA") AS NUMERIC),0) AS "SO_TIEN"
                    , --             D."SO_TIEN_QUY_DOI" AS "SO_TIEN"Management ,
                    round(cast((D."SO_LUONG" * M."DON_GIA") AS NUMERIC),0) AS "SO_TIEN_QUY_DOI"
                    , --             D."SO_TIEN_QUY_DOI" AS "SO_TIEN_QUY_DOI"Management ,
                    0                          AS "TY_LE_CHIET_KHAU"
                    , 0                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                          AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."THANH_TIEN"             AS "TONG_TIEN"
                    , --             M."SO_TIEN_QUY_DOI" AS "TONG_TIEN"Management ,
                    M."THANH_TIEN"             AS "TONG_TIEN_QUY_DOI"
                    , --             M."SO_TIEN_QUY_DOI" AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT                AS "TSCD_ID"
                    , NULL :: INT                AS "LOAI_TSCD_ID"
                    , M.id                       AS "CCDC_ID"
                    , NULL :: INT                AS "DOI_TUONG_ID"
                    , NULL :: INT                AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                AS "DOI_TUONG_CO_ID"
                    , D."MA_DON_VI_ID"           AS "DON_VI_ID"
                    , NULL :: INT                AS "NHAN_VIEN_ID"
                    , NULL :: INT                AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                AS "CONG_TRINH_ID"
                    , NULL :: INT                AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                AS "DON_DAT_HANG_ID"
                    , NULL :: INT                AS "DON_MUA_HANG_ID"
                    , --             NULL AS ContractID ,
                    NULL :: INT                AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                AS "TK_NGAN_HANG"
                    , NULL :: INT                AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    M."LY_DO_GHI_TANG"         AS "DIEN_GIAI_CHUNG"
                    , ''                         AS "DIEN_GIAI"
                    , NULL :: INT                AS "MA_HANG_ID_CT"
                    , NULL :: INT                AS "DVT_ID_CT"
                    , NULL :: INT                AS "DOI_TUONG_THCP_ID_CT"
                    , --             NULL AS DetailContractID ,
                    NULL :: INT                AS "KHOAN_MUC_CP_ID_CT"
                    , D."MA_DON_VI_ID"           AS "DON_VI_ID_CT"
                    , /* DDKhanh 04/08/2017 CR29455 chức năng không có ghi sổ thì set null */
                    M.state                    AS "TRANG_THAI_GHI_SO"
                    , -- 			CAST(NULL AS BIT) AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"           AS "CHI_NHANH_ID"
                    , D.id                       AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)        AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/

                FROM supply_ghi_tang M
                    INNER JOIN supply_ghi_tang_don_vi_su_dung D ON M.id = D."GHI_TANG_DON_VI_SU_DUNG_ID"


                UNION ALL


                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'supply.dieu.chuyen.cong.cu.dung.cu' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , M."BIEN_BAN_GIAO_NHAN_SO"                    AS "SO_CHUNG_TU"
                    , --             M."SO_CHUNG_TU" AS "SO_CHUNG_TU"Management ,
                    --             NULL AS CABA"SO_CHUNG_TU" ,
                    --             NULL AS CABA"SO_CHUNG_TU"Management ,
                    M."NGAY"                                     AS "NGAY_CHUNG_TU"
                    , M."NGAY"                                     AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                                  AS "currency_id"
                    , ''                                           AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                           AS "NGAY_HOA_DON"
                    , NULL :: INT                                  AS "TK_NO_ID"
                    , NULL :: INT                                  AS "TK_CO_ID"
                    , NULL :: INT                                  AS "MA_HANG_ID"
                    , ''                                           AS "TEN_HANG"
                    , NULL :: INT                                  AS "DVT_ID"
                    , NULL :: INT                                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG_DIEU_CHUYEN"                     AS "SO_LUONG"
                    , 0                                            AS "DON_GIA"
                    , --             0 AS "DON_GIA"Management ,
                    0                                            AS "SO_TIEN"
                    , --             0 AS "SO_TIEN"Management ,
                    0                                            AS "SO_TIEN_QUY_DOI"
                    , --             0 AS "SO_TIEN_QUY_DOI"Management ,
                    0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "TONG_TIEN"
                    , --             0 AS "TONG_TIEN"Management ,
                    0                                            AS "TONG_TIEN_QUY_DOI"
                    , --             0 AS "TONG_TIEN_QUY_DOI"Management ,
                    NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , D."MA_CCDC_ID"                               AS "CCDC_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                                  AS "DON_VI_ID"
                    , NULL :: INT                                  AS "NHAN_VIEN_ID"
                    , NULL :: INT                                  AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                                  AS "CONG_TRINH_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                                  AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                  AS "DON_MUA_HANG_ID"
                    , --             NULL AS ContractID ,
                    NULL :: INT                                  AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                                  AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                  AS "TK_NGAN_HANG"
                    , NULL :: INT                                  AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    M."LY_DO_DIEU_CHUYEN"                        AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , D."DOI_TUONG_TONG_HOP_CHI_PHI_ID"            AS "DOI_TUONG_THCP_ID_CT"
                    , --             D.ContractID AS DetailContractID ,
                    D."KHOAN_MUC_CP_ID"                     AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                         AS "DON_VI_ID_CT"
                    , M."state"                                    AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , D.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/

                FROM supply_dieu_chuyen_cong_cu_dung_cu M
                    INNER JOIN supply_dieu_chuyen_chi_tiet D ON M.id = D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"

                UNION ALL

                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'account.ex.so.du.tai.khoan.chi.tiet' :: TEXT AS "MODEL_GOC"
                    , cast(M."LOAI_CHUNG_TU" AS INTEGER)            AS "LOAI_CHUNG_TU"
                    , (CASE WHEN M."SO_TAI_KHOAN" IS NOT NULL
                    THEN
                        concat('OPN - ', M."SO_TAI_KHOAN")
                        ELSE 'OPN'
                        END)                                         AS "SO_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , ''                                            AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                            AS "NGAY_HOA_DON"
                    , NULL :: INT                                   AS "TK_NO_ID"
                    , NULL :: INT                                   AS "TK_CO_ID"
                    , NULL :: INT                                   AS "MA_HANG_ID"
                    , ''                                            AS "TEN_HANG"
                    , NULL :: INT                                   AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                                   AS "SO_LUONG"
                    , 0                                             AS "DON_GIA"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "SO_TIEN"
                    , (CASE WHEN M."DU_NO" <> 0
                    THEN M."DU_NO"
                        ELSE M."DU_CO"
                        END)                                         AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "TONG_TIEN"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                                   AS "DON_VI_ID"
                    , NULL :: INT                                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                                   AS "CONG_TRINH_ID"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                                   AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                   AS "DON_MUA_HANG_ID"
                    , NULL :: INT                                   AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_NGAN_HANG_ID"                           AS "TK_NGAN_HANG"
                    , NULL :: INT                                   AS "MA_THONG_KE_ID"
                    , ''                                            AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , NULL :: INT                                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                                   AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                          AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                                   AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , M.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"

                FROM account_ex_so_du_tai_khoan_chi_tiet M
                WHERE M."LOAI_CHUNG_TU" NOT IN ('610', '612', '613', '614')

                UNION ALL

                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'account.ex.so.du.tai.khoan.chi.tiet' :: TEXT AS "MODEL_GOC"
                    , cast(M."LOAI_CHUNG_TU" AS INTEGER)            AS "LOAI_CHUNG_TU"
                    , (CASE WHEN M."SO_TAI_KHOAN" IS NOT NULL
                    THEN
                        concat('OPN - ', M."SO_TAI_KHOAN")
                        ELSE 'OPN'
                        END)                                         AS "SO_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , ''                                            AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                            AS "NGAY_HOA_DON"
                    , NULL :: INT                                   AS "TK_NO_ID"
                    , NULL :: INT                                   AS "TK_CO_ID"
                    , NULL :: INT                                   AS "MA_HANG_ID"
                    , ''                                            AS "TEN_HANG"
                    , NULL :: INT                                   AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                                   AS "SO_LUONG"
                    , 0                                             AS "DON_GIA"
                    , (CASE WHEN coalesce(D."DU_NO_NGUYEN_TE", M."DU_NO_NGUYEN_TE") <> 0
                    THEN coalesce(D."DU_NO_NGUYEN_TE", M."DU_NO_NGUYEN_TE")
                        ELSE coalesce(D."DU_CO_NGUYEN_TE", M."DU_CO_NGUYEN_TE")
                        END)                                         AS "SO_TIEN"
                    , (CASE WHEN coalesce(D."DU_NO", M."DU_NO") <> 0
                    THEN coalesce(D."DU_NO", M."DU_NO")
                        ELSE coalesce(D."DU_CO", M."DU_CO")
                        END)                                         AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "TONG_TIEN"
                    , (CASE WHEN M."DU_NO" <> 0
                    THEN M."DU_NO"
                        ELSE M."DU_CO"
                        END)                                         AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                           AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"                         AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                           AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                           AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                           AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , M."TK_NGAN_HANG_ID"                           AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                            AS "MA_THONG_KE_ID"
                    , ''                                            AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , NULL :: INT                                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                                   AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                          AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                                   AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"

                FROM account_ex_so_du_tai_khoan_chi_tiet M
                    LEFT JOIN account_ex_sdtkct_theo_doi_tuong D ON M.id = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                WHERE M."LOAI_CHUNG_TU" = '610'

                UNION ALL

                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'account.ex.so.du.tai.khoan.chi.tiet' :: TEXT AS "MODEL_GOC"
                    , cast(M."LOAI_CHUNG_TU" AS INTEGER)            AS "LOAI_CHUNG_TU"
                    , (CASE WHEN M."SO_TAI_KHOAN" IS NOT NULL
                    THEN
                        concat('OPN - ', M."SO_TAI_KHOAN")
                        ELSE 'OPN'
                        END)                                         AS "SO_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , ''                                            AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                            AS "NGAY_HOA_DON"
                    , NULL :: INT                                   AS "TK_NO_ID"
                    , NULL :: INT                                   AS "TK_CO_ID"
                    , NULL :: INT                                   AS "MA_HANG_ID"
                    , ''                                            AS "TEN_HANG"
                    , NULL :: INT                                   AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                                   AS "SO_LUONG"
                    , 0                                             AS "DON_GIA"
                    , (CASE WHEN coalesce(D."DU_NO_NGUYEN_TE", M."DU_NO_NGUYEN_TE") <> 0
                    THEN coalesce(D."DU_NO_NGUYEN_TE", M."DU_NO_NGUYEN_TE")
                        ELSE coalesce(D."DU_CO_NGUYEN_TE", M."DU_CO_NGUYEN_TE")
                        END)                                         AS "SO_TIEN"
                    , (CASE WHEN coalesce(D."DU_NO", M."DU_NO") <> 0
                    THEN coalesce(D."DU_NO", M."DU_NO")
                        ELSE coalesce(D."DU_CO", M."DU_CO")
                        END)                                         AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "TONG_TIEN"
                    , (CASE WHEN M."DU_NO" <> 0
                    THEN M."DU_NO"
                        ELSE M."DU_CO"
                        END)                                         AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID"
                    , CASE WHEN M."LOAI_CHUNG_TU" = '612'
                    THEN D."DON_DAT_HANG_ID"
                    ELSE NULL :: INT END                          AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                           AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                           AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , M."TK_NGAN_HANG_ID"                           AS "TK_NGAN_HANG"
                    , NULL :: INT                                   AS "MA_THONG_KE_ID"
                    , ''                                            AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , NULL :: INT                                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                                   AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                          AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                                   AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"

                FROM account_ex_so_du_tai_khoan_chi_tiet M
                    LEFT JOIN account_ex_sdtkct_theo_doi_tuong D ON M.id = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                WHERE M."LOAI_CHUNG_TU" IN ('612', '613', '614')
                    AND NOT exists(SELECT *
                                    FROM account_ex_sdtkct_theo_hoa_don OPI
                                    WHERE OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = M.id)


                UNION ALL

                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'account.ex.so.du.tai.khoan.chi.tiet' :: TEXT AS "MODEL_GOC"
                    , cast(M."LOAI_CHUNG_TU" AS INTEGER)            AS "LOAI_CHUNG_TU"
                    , (CASE WHEN M."SO_TAI_KHOAN" IS NOT NULL
                    THEN
                        concat('OPN - ', M."SO_TAI_KHOAN")
                        ELSE 'OPN'
                        END)                                         AS "SO_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , ''                                            AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                            AS "NGAY_HOA_DON"
                    , NULL :: INT                                   AS "TK_NO_ID"
                    , NULL :: INT                                   AS "TK_CO_ID"
                    , NULL :: INT                                   AS "MA_HANG_ID"
                    , ''                                            AS "TEN_HANG"
                    , NULL :: INT                                   AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                                   AS "SO_LUONG"
                    , 0                                             AS "DON_GIA"
                    , 0                                             AS "SO_TIEN"
                    , 0                                             AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "TONG_TIEN"
                    , (CASE WHEN M."DU_NO" <> 0
                    THEN M."DU_NO"
                        ELSE M."DU_CO"
                        END)                                         AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                             AS "CONG_TRINH_ID"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID"
                    , CASE WHEN M."LOAI_CHUNG_TU" = '612'
                    THEN D."DON_DAT_HANG_ID"
                    ELSE NULL :: INT END                          AS "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                           AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                           AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                           AS "HOP_DONG_BAN_ID"
                    , M."TK_NGAN_HANG_ID"                           AS "TK_NGAN_HANG"
                    , NULL :: INT                                   AS "MA_THONG_KE_ID"
                    , ''                                            AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , NULL :: INT                                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                                   AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                          AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                                   AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"

                FROM account_ex_so_du_tai_khoan_chi_tiet M
                    INNER JOIN account_ex_sdtkct_theo_doi_tuong D ON M.id = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                WHERE M."LOAI_CHUNG_TU" IN ('612', '613', '614')
                    AND exists(SELECT *
                                FROM account_ex_sdtkct_theo_hoa_don OPI
                                WHERE OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = M.id)


                UNION ALL

                SELECT
                    M.id                                          AS "ID_GOC"
                    , 'account.ex.so.du.tai.khoan.chi.tiet' :: TEXT AS "MODEL_GOC"
                    , cast(M."LOAI_CHUNG_TU" AS INTEGER)            AS "LOAI_CHUNG_TU"
                    , (CASE WHEN M."SO_TAI_KHOAN" IS NOT NULL
                    THEN
                        concat('OPN - ', M."SO_TAI_KHOAN")
                        ELSE 'OPN'
                        END)                                         AS "SO_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                            AS "NGAY_HACH_TOAN"
                    , M.currency_id                                 AS "currency_id"
                    , D."SO_HOA_DON"                                AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                              AS "NGAY_HOA_DON"
                    , NULL :: INT                                   AS "TK_NO_ID"
                    , NULL :: INT                                   AS "TK_CO_ID"
                    , NULL :: INT                                   AS "MA_HANG_ID"
                    , ''                                            AS "TEN_HANG"
                    , NULL :: INT                                   AS "DVT_ID"
                    , NULL :: INT                                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                   AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                                   AS "SO_LUONG"
                    , 0                                             AS "DON_GIA"
                    , D."SO_CON_PHAI_THU_NGUYEN_TE"                 AS "SO_TIEN"
                    , D."SO_CON_PHAI_THU"                           AS "SO_TIEN_QUY_DOI"
                    , 0                                             AS "TY_LE_CHIET_KHAU"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , (CASE WHEN M."DU_NO_NGUYEN_TE" <> 0
                    THEN M."DU_NO_NGUYEN_TE"
                        ELSE M."DU_CO_NGUYEN_TE"
                        END)                                         AS "TONG_TIEN"
                    , (CASE WHEN M."DU_NO" <> 0
                    THEN M."DU_NO"
                        ELSE M."DU_CO"
                        END)                                         AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                   AS "TSCD_ID"
                    , NULL :: INT                                   AS "LOAI_TSCD_ID"
                    , NULL :: INT                                   AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                                 AS "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                              AS "NHAN_VIEN_ID"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                                   AS "CONG_TRINH_ID"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                                   AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                   AS "DON_MUA_HANG_ID"
                    , NULL :: INT                                   AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                                   AS "HOP_DONG_BAN_ID"
                    , M."TK_NGAN_HANG_ID"                           AS "TK_NGAN_HANG"
                    , NULL :: INT                                   AS "MA_THONG_KE_ID"
                    , ''                                            AS "DIEN_GIAI_CHUNG"
                    , ''                                            AS "DIEN_GIAI"
                    , NULL :: INT                                   AS "MA_HANG_ID_CT"
                    , NULL :: INT                                   AS "DVT_ID_CT"
                    , NULL :: INT                                   AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                   AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                          AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                                   AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                              AS "CHI_NHANH_ID"
                    , D.id                                          AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                           AS "SOURCE_ID"

                FROM account_ex_so_du_tai_khoan_chi_tiet M
                    INNER JOIN account_ex_sdtkct_theo_hoa_don D ON M.id = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"


                UNION ALL

                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'account.ex.ton.kho.vat.tu.hang.hoa' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , 'OPN'                                        AS "SO_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_HACH_TOAN"
                    , /*DDKHANH 09/05/2017 (BUG100754) Với chứng từ không có hạch toán ngoại tệ thì set loại tiền bằng Null*/
                    NULL :: INT                                  AS "currency_id"
                    , ''                                           AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                           AS "NGAY_HOA_DON"
                    , NULL :: INT                                  AS "TK_NO_ID"
                    , NULL :: INT                                  AS "TK_CO_ID"
                    , M."MA_HANG_ID"                               AS "MA_HANG_ID"
                    , M."TEN_HANG"                                 AS "TEN_HANG"
                    , M."DVT_ID"                                   AS "DVT_ID"
                    , M."KHO_ID"                                   AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , M."SO_LUONG"                                 AS "SO_LUONG"
                    , M."DON_GIA"                                  AS "DON_GIA"
                    , M."GIA_TRI_TON"                              AS "SO_TIEN"
                    , M."GIA_TRI_TON"                              AS "SO_TIEN_QUY_DOI"
                    , 0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."GIA_TRI_TON"                              AS "TONG_TIEN"
                    , M."GIA_TRI_TON"                              AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                                  AS "CCDC_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                                  AS "DON_VI_ID"
                    , NULL :: INT                                  AS "NHAN_VIEN_ID"
                    , NULL :: INT                                  AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                                  AS "CONG_TRINH_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                                  AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                  AS "DON_MUA_HANG_ID"
                    , --             NULL AS ContractID ,
                    NULL :: INT                                  AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                                  AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                  AS "TK_NGAN_HANG"
                    , NULL :: INT                                  AS "MA_THONG_KE_ID"
                    , --             NULL AS PurchasePurposeID ,
                    ''                                           AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , NULL :: INT                                  AS "DOI_TUONG_THCP_ID_CT"
                    , --             D.ContractID AS DetailContractID ,
                    NULL :: INT                                  AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                         AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                                  AS "TRANG_THAI_GHI_SO"
                    , --             M.IsPostedManagement AS IsPostedManagement ,
                    --             M.DisplayOnBook AS DisplayOnBook ,
                    M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , M.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"
                /*DDKHANH 27/04/2017 (CR27148) thêm 4 trường tìm kiếm chứng từ theo người tạo*/

                FROM account_ex_ton_kho_vat_tu_hang_hoa M


                UNION ALL

                SELECT
                    M.id                           AS "ID_GOC"
                    , 'sale.ex.hop.dong.ban' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"              AS "LOAI_CHUNG_TU"
                    , M."SO_HOP_DONG"                AS "SO_CHUNG_TU"
                    , M."NGAY_KY"                    AS "NGAY_CHUNG_TU"
                    , M."NGAY_KY"                    AS "NGAY_HACH_TOAN"
                    , M.currency_id                  AS "currency_id"
                    , ''                             AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)             AS "NGAY_HOA_DON"
                    , NULL :: INT                    AS "TK_NO_ID"
                    , NULL :: INT                    AS "TK_CO_ID"
                    , NULL :: INT                    AS "MA_HANG_ID"
                    , ''                             AS "TEN_HANG"
                    , NULL :: INT                    AS "DVT_ID"
                    , NULL :: INT                    AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                    AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                    AS "SO_LUONG"
                    , 0                              AS "DON_GIA"
                    , M."GIA_TRI_HOP_DONG"           AS "SO_TIEN"
                    , M."GTHD_QUY_DOI"               AS "SO_TIEN_QUY_DOI"
                    , 0                              AS "TY_LE_CHIET_KHAU"
                    , 0                              AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                              AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."GIA_TRI_HOP_DONG"           AS "TONG_TIEN"
                    , M."GTHD_QUY_DOI"               AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                    AS "TSCD_ID"
                    , NULL :: INT                    AS "LOAI_TSCD_ID"
                    , NULL :: INT                    AS "CCDC_ID"
                    , M."KHACH_HANG_ID"              AS "DOI_TUONG_ID"
                    , M."KHACH_HANG_ID"              AS "DOI_TUONG_NO_ID"
                    , M."KHACH_HANG_ID"              AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                  AS "DON_VI_ID"
                    , M."NGUOI_THUC_HIEN_ID"         AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"            AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                    AS "CONG_TRINH_ID"
                    , NULL :: INT                    AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                    AS "DON_DAT_HANG_ID"
                    , NULL :: INT                    AS "DON_MUA_HANG_ID"
                    , NULL :: INT                    AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                    AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                    AS "TK_NGAN_HANG"
                    , NULL :: INT                    AS "MA_THONG_KE_ID"
                    , M."TRICH_YEU"                  AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI"                  AS "DIEN_GIAI"
                    , D1."MA_HANG_ID"                AS "MA_HANG_ID_CT"
                    , D1."DVT_ID"                    AS "DVT_ID_CT"
                    , NULL :: INT                    AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"            AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                           AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                    AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"               AS "CHI_NHANH_ID"
                    , M.id                           AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)            AS "SOURCE_ID"

                FROM sale_ex_hop_dong_ban M
                    LEFT JOIN sale_ex_hop_dong_ban_chi_tiet_du_kien_chi D ON M.id = D."HOP_DONG_BAN_ID"
                    LEFT JOIN sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu D1 ON M.id = D1."HOP_DONG_BAN_ID"


                UNION ALL

                SELECT
                    M.id                                 AS "ID_GOC"
                    , 'tong.hop.chi.phi.tra.truoc' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                    AS "LOAI_CHUNG_TU"
                    , M."MA_CHI_PHI_TRA_TRUOC"             AS "SO_CHUNG_TU"
                    , M."NGAY_GHI_NHAN"                    AS "NGAY_CHUNG_TU"
                    , M."NGAY_GHI_NHAN"                    AS "NGAY_HACH_TOAN"
                    , NULL :: INT                          AS "currency_id"
                    , ''                                   AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                   AS "NGAY_HOA_DON"
                    , NULL :: INT                          AS "TK_NO_ID"
                    , NULL :: INT                          AS "TK_CO_ID"
                    , NULL :: INT                          AS "MA_HANG_ID"
                    , ''                                   AS "TEN_HANG"
                    , NULL :: INT                          AS "DVT_ID"
                    , NULL :: INT                          AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                          AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                          AS "SO_LUONG"
                    , 0                                    AS "DON_GIA"
                    , M."SO_TIEN"                          AS "SO_TIEN"
                    , M."SO_TIEN"                          AS "SO_TIEN_QUY_DOI"
                    , 0                                    AS "TY_LE_CHIET_KHAU"
                    , 0                                    AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                    AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN"                          AS "TONG_TIEN"
                    , M."SO_TIEN"                          AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                          AS "TSCD_ID"
                    , NULL :: INT                          AS "LOAI_TSCD_ID"
                    , NULL :: INT                          AS "CCDC_ID"
                    , NULL :: INT                          AS "DOI_TUONG_ID"
                    , NULL :: INT                          AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                          AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                          AS "DON_VI_ID"
                    , NULL :: INT                          AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                  AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                          AS "CONG_TRINH_ID"
                    , NULL :: INT                          AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                          AS "DON_DAT_HANG_ID"
                    , NULL :: INT                          AS "DON_MUA_HANG_ID"
                    , NULL :: INT                          AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                          AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                          AS "TK_NGAN_HANG"
                    , NULL :: INT                          AS "MA_THONG_KE_ID"
                    , M."TEN_CHI_PHI_TRA_TRUOC"            AS "DIEN_GIAI_CHUNG"
                    , ''                                   AS "DIEN_GIAI"
                    , NULL :: INT                          AS "MA_HANG_ID_CT"
                    , NULL :: INT                          AS "DVT_ID_CT"
                    , NULL :: INT                          AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                  AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                 AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                          AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                     AS "CHI_NHANH_ID"
                    , M.id                                 AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                  AS "SOURCE_ID"

                FROM tong_hop_chi_phi_tra_truoc M
                    LEFT JOIN tong_hop_chi_phi_tra_truoc_thiet_lap_phan_bo D ON M.id = D."CHI_PHI_TRA_TRUOC_ID"

                UNION ALL

                SELECT
                    M.id                              AS "ID_GOC"
                    , 'account.ex.don.dat.hang' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                 AS "LOAI_CHUNG_TU"
                    , M."SO_DON_HANG"                   AS "SO_CHUNG_TU"
                    , M."NGAY_DON_HANG"                 AS "NGAY_CHUNG_TU"
                    , M."NGAY_DON_HANG"                 AS "NGAY_HACH_TOAN"
                    , M."currency_id"                   AS "currency_id"
                    , ''                                AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                AS "NGAY_HOA_DON"
                    , NULL :: INT                       AS "TK_NO_ID"
                    , NULL :: INT                       AS "TK_CO_ID"
                    , D."MA_HANG_ID"                    AS "MA_HANG_ID"
                    , D."TEN_HANG"                      AS "TEN_HANG"
                    , D."DVT_ID"                        AS "DVT_ID"
                    , D."MA_KHO_ID"                     AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                       AS "MA_KHO_NHAP_ID"
                    , D."SO_LUONG"                      AS "SO_LUONG"
                    , D."DON_GIA"                       AS "DON_GIA"
                    , D."THANH_TIEN"                    AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI"            AS "SO_TIEN_QUY_DOI"
                    , 0                                 AS "TY_LE_CHIET_KHAU"
                    , 0                                 AS "SO_TIEN_CHIET_KHAU"
                    , 0                                 AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI"        AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                       AS "TSCD_ID"
                    , NULL :: INT                       AS "LOAI_TSCD_ID"
                    , NULL :: INT                       AS "CCDC_ID"
                    , M."KHACH_HANG_ID"                 AS "DOI_TUONG_ID"
                    , M."KHACH_HANG_ID"                 AS "DOI_TUONG_NO_ID"
                    , M."KHACH_HANG_ID"                 AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                     AS "DON_VI_ID"
                    , M."NV_BAN_HANG_ID"                AS "NHAN_VIEN_ID"
                    , NULL :: INT                       AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                       AS "CONG_TRINH_ID"
                    , NULL :: INT                       AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                       AS "DON_DAT_HANG_ID"
                    , NULL :: INT                       AS "DON_MUA_HANG_ID"
                    , NULL :: INT                       AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                       AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                       AS "TK_NGAN_HANG"
                    , NULL :: INT                       AS "MA_THONG_KE_ID"
                    , M."GHI_CHU"                       AS "DIEN_GIAI_CHUNG"
                    , ''                                AS "DIEN_GIAI"
                    , NULL :: INT                       AS "MA_HANG_ID_CT"
                    , NULL :: INT                       AS "DVT_ID_CT"
                    , NULL :: INT                       AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                       AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                       AS "DON_VI_ID_CT"
                    , M."state"                         AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                  AS "CHI_NHANH_ID"
                    , D.id                              AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)               AS "SOURCE_ID"
                FROM account_ex_don_dat_hang M
                    INNER JOIN account_ex_don_dat_hang_chi_tiet D ON M.id = D."DON_DAT_HANG_CHI_TIET_ID"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa VT ON VT.id = D."MA_HANG_ID"


                UNION ALL

                SELECT
                    M.id                        AS "ID_GOC"
                    , 'sale.ex.bao.gia' :: TEXT   AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"           AS "LOAI_CHUNG_TU"
                    , M."SO_BAO_GIA"              AS "SO_CHUNG_TU"
                    , M."NGAY_BAO_GIA"            AS "NGAY_CHUNG_TU"
                    , M."NGAY_BAO_GIA"            AS "NGAY_HACH_TOAN"
                    , M.currency_id               AS "currency_id"
                    , ''                          AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)          AS "NGAY_HOA_DON"
                    , NULL :: INT                 AS "TK_NO_ID"
                    , NULL :: INT                 AS "TK_CO_ID"
                    , D."MA_HANG_ID"              AS "MA_HANG_ID"
                    , D."TEN_HANG"                AS "TEN_HANG"
                    , D."DVT_ID"                  AS "DVT_ID"
                    , NULL :: INT                 AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                 AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                AS "SO_LUONG"
                    , D."DON_GIA"                 AS "DON_GIA"
                    , D."THANH_TIEN"              AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI"      AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"         AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI" AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN"               AS "TONG_TIEN"
                    , M."TONG_TIEN_QUY_DOI"       AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                 AS "TSCD_ID"
                    , NULL :: INT                 AS "LOAI_TSCD_ID"
                    , NULL :: INT                 AS "CCDC_ID"
                    , M."KHACH_HANG_ID"           AS "DOI_TUONG_ID"
                    , M."KHACH_HANG_ID"           AS "DOI_TUONG_NO_ID"
                    , M."KHACH_HANG_ID"           AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                 AS "DON_VI_ID"
                    , M."NV_MUA_HANG_ID"          AS "NHAN_VIEN_ID"
                    , NULL :: INT                 AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                 AS "CONG_TRINH_ID"
                    , NULL :: INT                 AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                 AS "DON_DAT_HANG_ID"
                    , NULL :: INT                 AS "DON_MUA_HANG_ID"
                    , NULL :: INT                 AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                 AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                 AS "TK_NGAN_HANG"
                    , NULL :: INT                 AS "MA_THONG_KE_ID"
                    , M."GHI_CHU"                 AS "DIEN_GIAI_CHUNG"
                    , D."TEN_HANG"                AS "DIEN_GIAI"
                    , NULL :: INT                 AS "MA_HANG_ID_CT"
                    , NULL :: INT                 AS "DVT_ID_CT"
                    , NULL :: INT                 AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                 AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                        AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                 AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"            AS "CHI_NHANH_ID"
                    , M.id                        AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)         AS "SOURCE_ID"

                FROM sale_ex_bao_gia M
                    LEFT JOIN sale_ex_bao_gia_chi_tiet D ON M.id = D."BAO_GIA_CHI_TIET_ID"


                UNION ALL

                SELECT
                    M.id                               AS "ID_GOC"
                    , 'purchase.ex.don.mua.hang' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_DON_HANG"                    AS "SO_CHUNG_TU"
                    , M."NGAY_DON_HANG"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_DON_HANG"                  AS "NGAY_HACH_TOAN"
                    , M.currency_id                      AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , NULL :: INT                        AS "TK_NO_ID"
                    , NULL :: INT                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID"
                    , D."TEN_HANG"                       AS "TEN_HANG"
                    , D."DVT_ID"                         AS "DVT_ID"
                    , D."KHO_ID"                         AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                       AS "SO_LUONG"
                    , D."DON_GIA"                        AS "DON_GIA"
                    , D."THANH_TIEN"                     AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CHIET_KHAU"               AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                 AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QUY_DOI"         AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."NHA_CUNG_CAP_ID"                AS "DOI_TUONG_ID"
                    , M."NHA_CUNG_CAP_ID"                AS "DOI_TUONG_NO_ID"
                    , M."NHA_CUNG_CAP_ID"                AS "DOI_TUONG_CO_ID"
                    , D."DON_VI_ID"                      AS "DON_VI_ID"
                    , M."NV_MUA_HANG_ID"                 AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID"
                    , D."CONG_TRINH_ID"                  AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"                AS "DON_DAT_HANG_ID"
                    , NULL :: INT                        AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"                 AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."TEN_HANG"                       AS "DIEN_GIAI"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID_CT"
                    , D."DVT_ID"                         AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"              AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                      AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , M.id                               AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                AS "SOURCE_ID"

                FROM purchase_ex_don_mua_hang M
                    LEFT JOIN purchase_ex_don_mua_hang_chi_tiet D ON M.id = D."DON_MUA_HANG_CHI_TIET_ID"


                UNION ALL

                SELECT
                    M.id                                    AS "ID_GOC"
                    , 'purchase.ex.hop.dong.mua.hang' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                       AS "LOAI_CHUNG_TU"
                    , M."SO_HOP_DONG"                         AS "SO_CHUNG_TU"
                    , M."NGAY_KY"                             AS "NGAY_CHUNG_TU"
                    , M."NGAY_KY"                             AS "NGAY_HACH_TOAN"
                    , M.currency_id                           AS "currency_id"
                    , ''                                      AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                      AS "NGAY_HOA_DON"
                    , NULL :: INT                             AS "TK_NO_ID"
                    , NULL :: INT                             AS "TK_CO_ID"
                    , NULL :: INT                             AS "MA_HANG_ID"
                    , ''                                      AS "TEN_HANG"
                    , NULL :: INT                             AS "DVT_ID"
                    , NULL :: INT                             AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                             AS "MA_KHO_XUAT_ID"
                    , NULL :: INT                             AS "SO_LUONG"
                    , NULL :: INT                             AS "DON_GIA"
                    , M."GIA_TRI_HOP_DONG"                    AS "SO_TIEN"
                    , M."GT_HOP_DONG_QUY_DOI"                 AS "SO_TIEN_QUY_DOI"
                    , NULL :: INT                             AS "TY_LE_CHIET_KHAU"
                    , NULL :: INT                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                             AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."GIA_TRI_HOP_DONG"                    AS "TONG_TIEN"
                    , M."GT_HOP_DONG_QUY_DOI"                 AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                             AS "TSCD_ID"
                    , NULL :: INT                             AS "LOAI_TSCD_ID"
                    , NULL :: INT                             AS "CCDC_ID"
                    , M."NHA_CUNG_CAP_ID"                     AS "DOI_TUONG_ID"
                    , M."NHA_CUNG_CAP_ID"                     AS "DOI_TUONG_NO_ID"
                    , M."NHA_CUNG_CAP_ID"                     AS "DOI_TUONG_CO_ID"
                    , M."CHI_NHANH_ID"                        AS "DON_VI_ID"
                    , M."NV_MUA_HANG_ID"                      AS "NHAN_VIEN_ID"
                    , NULL :: INT                             AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                             AS "CONG_TRINH_ID"
                    , NULL :: INT                             AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                             AS "DON_DAT_HANG_ID"
                    , NULL :: INT                             AS "DON_MUA_HANG_ID"
                    , NULL :: INT                             AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                             AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                             AS "TK_NGAN_HANG"
                    , NULL :: INT                             AS "MA_THONG_KE_ID"
                    , M."TRICH_YEU"                           AS "DIEN_GIAI_CHUNG"
                    , ''                                      AS "DIEN_GIAI"
                    , NULL :: INT                             AS "MA_HANG_ID_CT"
                    , NULL :: INT                             AS "DVT_ID_CT"
                    , NULL :: INT                             AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                             AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                                    AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                             AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                        AS "CHI_NHANH_ID"
                    , M.id                                    AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                     AS "SOURCE_ID"

                FROM purchase_ex_hop_dong_mua_hang M


                UNION ALL

                SELECT
                    M.id                               AS "ID_GOC"
                    , 'stock.ex.lap.rap.thao.do' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO"                             AS "SO_CHUNG_TU"
                    , M."NGAY"                           AS "NGAY_CHUNG_TU"
                    , M."NGAY"                           AS "NGAY_HACH_TOAN"
                    , NULL :: INT                        AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)                 AS "NGAY_HOA_DON"
                    , NULL :: INT                        AS "TK_NO_ID"
                    , NULL :: INT                        AS "TK_CO_ID"
                    , M."HANG_HOA_ID"                    AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , M."DVT_ID"                         AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , M."SO_LUONG"                       AS "SO_LUONG"
                    , NULL :: INT                        AS "DON_GIA"
                    , NULL :: INT                        AS "SO_TIEN"
                    , NULL :: INT                        AS "SO_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TY_LE_CHIET_KHAU"
                    , NULL :: INT                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                        AS "TONG_TIEN"
                    , NULL :: INT                        AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , NULL :: INT                        AS "DOI_TUONG_ID"
                    , NULL :: INT                        AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                        AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                        AS "DON_VI_ID"
                    , NULL :: INT                        AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                        AS "CONG_TRINH_ID"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                        AS "DON_DAT_HANG_ID"
                    , NULL :: INT                        AS "DON_MUA_HANG_ID"
                    , NULL :: INT                        AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                        AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , NULL :: INT                        AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , D."TEN_HANG"                       AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                               AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , M.id                               AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                AS "SOURCE_ID"

                FROM stock_ex_lap_rap_thao_do M
                    INNER JOIN stock_ex_lap_rap_thao_do_chi_tiet D ON M.id = D."LAP_RAP_THAO_DO_CHI_TIET_ID"


                UNION ALL

                SELECT
                    M.id                             AS "ID_GOC"
                    , 'stock.ex.lenh.san.xuat' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                    , M."SO_LENH"                      AS "SO_CHUNG_TU"
                    , M."NGAY"                         AS "NGAY_CHUNG_TU"
                    , M."NGAY"                         AS "NGAY_HACH_TOAN"
                    , NULL :: INT                      AS "currency_id"
                    , ''                               AS "SO_HOA_DON"
                    , CAST(NULL AS DATE)               AS "NGAY_HOA_DON"
                    , NULL :: INT                      AS "TK_NO_ID"
                    , NULL :: INT                      AS "TK_CO_ID"
                    , D."MA_HANG_ID"                   AS "MA_HANG_ID"
                    , D."TEN_THANH_PHAM"               AS "TEN_HANG"
                    , D."DVT_ID"                       AS "DVT_ID"
                    , NULL :: INT                      AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                      AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                     AS "SO_LUONG"
                    , NULL :: INT                      AS "DON_GIA"
                    , NULL :: INT                      AS "SO_TIEN"
                    , NULL :: INT                      AS "SO_TIEN_QUY_DOI"
                    , NULL :: INT                      AS "TY_LE_CHIET_KHAU"
                    , NULL :: INT                      AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                      AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , NULL :: INT                      AS "TONG_TIEN"
                    , NULL :: INT                      AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                      AS "TSCD_ID"
                    , NULL :: INT                      AS "LOAI_TSCD_ID"
                    , NULL :: INT                      AS "CCDC_ID"
                    , NULL :: INT                      AS "DOI_TUONG_ID"
                    , NULL :: INT                      AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                      AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                      AS "DON_VI_ID"
                    , NULL :: INT                      AS "NHAN_VIEN_ID"
                    , NULL :: INT                      AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                      AS "CONG_TRINH_ID"
                    , D."DOI_TUONG_THCP_ID"            AS "DOI_TUONG_THCP_ID"
                    , D."DON_DAT_HANG_ID"              AS "DON_DAT_HANG_ID"
                    , NULL :: INT                      AS "DON_MUA_HANG_ID"
                    , NULL :: INT                      AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                      AS "TK_NGAN_HANG"
                    , NULL :: INT                      AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                    AS "DIEN_GIAI_CHUNG"
                    , D."TEN_THANH_PHAM"               AS "DIEN_GIAI"
                    , NULL :: INT                      AS "MA_HANG_ID_CT"
                    , NULL :: INT                      AS "DVT_ID_CT"
                    , NULL :: INT                      AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                      AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                             AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                      AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                 AS "CHI_NHANH_ID"
                    , M.id                             AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)              AS "SOURCE_ID"

                FROM stock_ex_lenh_san_xuat M
                    INNER JOIN stock_ex_lenh_san_xuat_chi_tiet_thanh_pham D
                        ON M.id = D."LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID"
                    INNER JOIN stock_ex_thanh_pham_chi_tiet_dinh_muc_xuat_nvl D1
                        ON D.id = D1."THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_ID"

                UNION ALL

                SELECT
                    M.id                               AS "ID_GOC"
                    , 'sale.ex.hoa.don.ban.hang' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_HOA_DON"                     AS "SO_CHUNG_TU"
                    , M."NGAY_HOA_DON"                   AS "NGAY_CHUNG_TU"
                    , M."NGAY_HOA_DON"                   AS "NGAY_HACH_TOAN"
                    , M.currency_id                      AS "currency_id"
                    , M."SO_HOA_DON"                     AS "SO_HOA_DON"
                    , M."NGAY_HOA_DON"                   AS "NGAY_HOA_DON"
                    , NULL :: INT                        AS "TK_NO_ID"
                    , NULL :: INT                        AS "TK_CO_ID"
                    , D."MA_HANG_ID"                     AS "MA_HANG_ID"
                    , D."TEN_HANG"                       AS "TEN_HANG"
                    , D."DVT_ID"                         AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , D."SO_LUONG"                       AS "SO_LUONG"
                    , D."DON_GIA"                        AS "DON_GIA"
                    , D."THANH_TIEN"                     AS "SO_TIEN"
                    , D."THANH_TIEN_QUY_DOI"             AS "SO_TIEN_QUY_DOI"
                    , D."TY_LE_CK"                       AS "TY_LE_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU"                AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"        AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN_HANG"                 AS "TONG_TIEN"
                    , M."TONG_TIEN_HANG_QD"              AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                   AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                        AS "DON_VI_ID"
                    , M."NHAN_VIEN_ID"                   AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                        AS "CONG_TRINH_ID"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                        AS "DON_DAT_HANG_ID"
                    , NULL :: INT                        AS "DON_MUA_HANG_ID"
                    , NULL :: INT                        AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                        AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TK_NGAN_HANG"
                    , NULL :: INT                        AS "MA_THONG_KE_ID"
                    , ''                                 AS "DIEN_GIAI_CHUNG"
                    , D."TEN_HANG"                       AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , NULL                               AS "DON_VI_ID_CT"
                    , 'da_ghi_so'                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , M.id                               AS "CHI_TIET_ID"
                    , M."SOURCE_ID"                      AS "SOURCE_ID"

                FROM sale_ex_hoa_don_ban_hang M
                    LEFT JOIN sale_ex_chi_tiet_hoa_don_ban_hang D ON M.id = D."HOA_DON_ID_ID"
                WHERE M."LAP_KEM_HOA_DON" = FALSE

                UNION ALL

                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'account.ex.chung.tu.nghiep.vu.khac' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_HACH_TOAN"
                    , M."currency_id"                              AS "currency_id"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."SO_HOA_DON"
                        ELSE ''
                        END)                                        AS "SO_HOA_DON"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."NGAY_HOA_DON"
                        ELSE NULL :: DATE
                        END)                                        AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                 AS "TK_NO_ID"
                    , D."TK_CO_ID"                                 AS "TK_CO_ID"
                    , NULL :: INT                                  AS "MA_HANG_ID"
                    , ''                                           AS "TEN_HANG"
                    , NULL :: INT                                  AS "DVT_ID"
                    , NULL :: INT                                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , 0                                            AS "SO_LUONG"
                    , 0                                            AS "DON_GIA"
                    , D."SO_TIEN"                                  AS "SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"                          AS "SO_TIEN_QUY_DOI"
                    , 0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                                  AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                             AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                          AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                          AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                          AS "HOP_DONG_BAN_ID"
                    , D."TK_NGAN_HANG_ID"                          AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                        AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                          AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                AS "DON_VI_ID_CT"
                    , M.state                                      AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , D.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"

                FROM account_ex_chung_tu_nghiep_vu_khac M
                    INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D ON M.id = D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                WHERE M."DOI_TUONG_ID" NOTNULL


                UNION ALL


                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'account.ex.chung.tu.nghiep.vu.khac' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_HACH_TOAN"
                    , M."currency_id"                              AS "currency_id"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."SO_HOA_DON"
                        ELSE ''
                        END)                                        AS "SO_HOA_DON"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."NGAY_HOA_DON"
                        ELSE NULL :: DATE
                        END)                                        AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                 AS "TK_CO_ID"
                    , NULL :: INT                                  AS "MA_HANG_ID"
                    , ''                                           AS "TEN_HANG"
                    , NULL :: INT                                  AS "DVT_ID"
                    , NULL :: INT                                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , 0                                            AS "SO_LUONG"
                    , 0                                            AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                           AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QD"                        AS "SO_TIEN_QUY_DOI"
                    , 0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                                  AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                             AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                          AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                          AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                          AS "HOP_DONG_BAN_ID"
                    , D."TK_NGAN_HANG_ID"                          AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                        AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                          AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                AS "DON_VI_ID_CT"
                    , M.state                                      AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , D.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"

                FROM account_ex_chung_tu_nghiep_vu_khac M
                    INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D ON M.id = D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                WHERE M."DOI_TUONG_ID" NOTNULL
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QD" <> 0)


                UNION ALL


                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'account.ex.chung.tu.nghiep.vu.khac' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_HACH_TOAN"
                    , M."currency_id"                              AS "currency_id"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."SO_HOA_DON"
                        ELSE ''
                        END)                                        AS "SO_HOA_DON"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."NGAY_HOA_DON"
                        ELSE NULL :: DATE
                        END)                                        AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                                 AS "TK_NO_ID"
                    , D."TK_CO_ID"                                 AS "TK_CO_ID"
                    , NULL :: INT                                  AS "MA_HANG_ID"
                    , ''                                           AS "TEN_HANG"
                    , NULL :: INT                                  AS "DVT_ID"
                    , NULL :: INT                                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , 0                                            AS "SO_LUONG"
                    , 0                                            AS "DON_GIA"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                                AND D."TK_THUE_GTGT_ID" ISNULL
                    THEN coalesce(D."SO_TIEN", 0) + coalesce(D."TIEN_THUE_GTGT", 0)
                        ELSE D."SO_TIEN"
                        END)                                        AS "SO_TIEN"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                                AND D."TK_THUE_GTGT_ID" ISNULL
                    THEN coalesce(D."SO_TIEN_QUY_DOI", 0) + coalesce(D."TIEN_THUE_GTGT_QD", 0)
                        ELSE D."SO_TIEN_QUY_DOI"
                        END)                                        AS "SO_TIEN_QUY_DOI"
                    , 0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                                  AS "CCDC_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN M."NHAN_VIEN_ID"
                        ELSE M."DOI_TUONG_ID"
                        END)                                        AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_NO_ID"                          AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_CO_ID"                          AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                             AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                          AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                          AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                          AS "HOP_DONG_BAN_ID"
                    , D."TK_NGAN_HANG_ID"                          AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                        AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                          AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                AS "DON_VI_ID_CT"
                    , M.state                                      AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , D.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"

                FROM account_ex_chung_tu_nghiep_vu_khac M
                    INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D ON M.id = D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                WHERE M."DOI_TUONG_ID" ISNULL


                UNION ALL


                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'account.ex.chung.tu.nghiep.vu.khac' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_HACH_TOAN"
                    , M."currency_id"                              AS "currency_id"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."SO_HOA_DON"
                        ELSE ''
                        END)                                        AS "SO_HOA_DON"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN D."NGAY_HOA_DON"
                        ELSE NULL :: DATE
                        END)                                        AS "NGAY_HOA_DON"
                    , D."TK_THUE_GTGT_ID"                          AS "TK_NO_ID"
                    , D."TK_CO_ID"                                 AS "TK_CO_ID"
                    , NULL :: INT                                  AS "MA_HANG_ID"
                    , ''                                           AS "TEN_HANG"
                    , NULL :: INT                                  AS "DVT_ID"
                    , NULL :: INT                                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , 0                                            AS "SO_LUONG"
                    , 0                                            AS "DON_GIA"
                    , D."TIEN_THUE_GTGT"                           AS "SO_TIEN"
                    , D."TIEN_THUE_GTGT_QD"                        AS "SO_TIEN_QUY_DOI"
                    , 0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                                  AS "CCDC_ID"
                    , (CASE WHEN M."LOAI_CHUNG_TU" = 4015
                    THEN M."NHAN_VIEN_ID"
                        ELSE M."DOI_TUONG_ID"
                        END)                                        AS "DOI_TUONG_ID"
                    , D."DOI_TUONG_NO_ID"                          AS "DOI_TUONG_NO_ID"
                    , D."DOI_TUONG_CO_ID"                          AS "DOI_TUONG_CO_ID"
                    , "DON_VI_ID"
                    , D."NHAN_VIEN_ID"                             AS "NHAN_VIEN_ID"
                    , "KHOAN_MUC_CP_ID"
                    , "CONG_TRINH_ID"
                    , "DOI_TUONG_THCP_ID"
                    , "DON_DAT_HANG_ID"
                    , D."DON_MUA_HANG_ID"                          AS "DON_MUA_HANG_ID"
                    , D."HOP_DONG_MUA_ID"                          AS "HOP_DONG_MUA_ID"
                    , D."HOP_DONG_BAN_ID"                          AS "HOP_DONG_BAN_ID"
                    , D."TK_NGAN_HANG_ID"                          AS "TK_NGAN_HANG"
                    , D."MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , D."DOI_TUONG_THCP_ID"                        AS "DOI_TUONG_THCP_ID_CT"
                    , D."KHOAN_MUC_CP_ID"                          AS "KHOAN_MUC_CP_ID_CT"
                    , D."DON_VI_ID"                                AS "DON_VI_ID_CT"
                    , M.state                                      AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , D.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"

                FROM account_ex_chung_tu_nghiep_vu_khac M
                    INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D ON M.id = D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                WHERE M."DOI_TUONG_ID" ISNULL
                    AND D."TK_THUE_GTGT_ID" NOTNULL
                    AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QD" <> 0)


                UNION ALL


                SELECT
                    M.id                                         AS "ID_GOC"
                    , 'account.ex.chung.tu.nghiep.vu.khac' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                            AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                              AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                            AS "NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"                           AS "NGAY_HACH_TOAN"
                    , M."currency_id"                              AS "currency_id"
                    , D."SO_HOA_DON"                               AS "SO_HOA_DON"
                    , D."NGAY_HOA_DON"                             AS "NGAY_HOA_DON"
                    , M."TK_XU_LY_LAI_ID"                          AS "TK_NO_ID"
                    , M."TK_XU_LY_LO_ID"                           AS "TK_CO_ID"
                    , NULL :: INT                                  AS "MA_HANG_ID"
                    , ''                                           AS "TEN_HANG"
                    , NULL :: INT                                  AS "DVT_ID"
                    , NULL :: INT                                  AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                                  AS "MA_KHO_XUAT_ID"
                    , 0                                            AS "SO_LUONG"
                    , 0                                            AS "DON_GIA"
                    , 0                                            AS "SO_TIEN"
                    , 0                                            AS "SO_TIEN_QUY_DOI"
                    , 0                                            AS "TY_LE_CHIET_KHAU"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                            AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN"
                    , M."TONG_CHENH_LECH"                          AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                                  AS "TSCD_ID"
                    , NULL :: INT                                  AS "LOAI_TSCD_ID"
                    , NULL :: INT                                  AS "CCDC_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_NO_ID"
                    , M."DOI_TUONG_ID"                             AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                                  AS "DON_VI_ID"
                    , NULL :: INT                                  AS "NHAN_VIEN_ID"
                    , NULL :: INT                                  AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                                  AS "CONG_TRINH_ID"
                    , NULL :: INT                                  AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                                  AS "DON_DAT_HANG_ID"
                    , NULL :: INT                                  AS "DON_MUA_HANG_ID"
                    , NULL :: INT                                  AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                                  AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                                  AS "TK_NGAN_HANG"
                    , NULL :: INT                                  AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                                AS "DIEN_GIAI_CHUNG"
                    , ''                                           AS "DIEN_GIAI"
                    , NULL :: INT                                  AS "MA_HANG_ID_CT"
                    , NULL :: INT                                  AS "DVT_ID_CT"
                    , NULL :: INT                                  AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                                  AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                                  AS "DON_VI_ID_CT"
                    , M.state                                      AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                             AS "CHI_NHANH_ID"
                    , D.id                                         AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                          AS "SOURCE_ID"

                FROM account_ex_chung_tu_nghiep_vu_khac M
                    INNER JOIN account_ex_thue D ON M.id = D."CHUNG_TU_KHAC_THUE_ID"
                UNION ALL

                SELECT
                    M.id                               AS "ID_GOC"
                    , 'tong.hop.chung.tu.ghi.so' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                  AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                    AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                  AS "NGAY_HACH_TOAN"
                    , D."currency_id"                    AS "currency_id"
                    , ''                                 AS "SO_HOA_DON"
                    , NULL :: DATE                       AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                       AS "TK_NO_ID"
                    , D."TK_CO_ID"                       AS "TK_CO_ID"
                    , NULL :: INT                        AS "MA_HANG_ID"
                    , ''                                 AS "TEN_HANG"
                    , NULL :: INT                        AS "DVT_ID"
                    , NULL :: INT                        AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                        AS "MA_KHO_XUAT_ID"
                    , 0                                  AS "SO_LUONG"
                    , 0                                  AS "DON_GIA"
                    , 0                                  AS "SO_TIEN"
                    , D."SO_TIEN"                        AS "SO_TIEN_QUY_DOI"
                    , 0                                  AS "TY_LE_CHIET_KHAU"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                  AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."TONG_TIEN"                      AS "TONG_TIEN"
                    , M."TONG_TIEN"                      AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                        AS "TSCD_ID"
                    , NULL :: INT                        AS "LOAI_TSCD_ID"
                    , NULL :: INT                        AS "CCDC_ID"
                    , NULL :: INT                        AS "DOI_TUONG_ID"
                    , NULL :: INT                        AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                        AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                        AS "DON_VI_ID"
                    , NULL :: INT                        AS "NHAN_VIEN_ID"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID"
                    , NULL :: INT                        AS "CONG_TRINH_ID"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID"
                    , NULL :: INT                        AS "DON_DAT_HANG_ID"
                    , NULL :: INT                        AS "DON_MUA_HANG_ID"
                    , NULL :: INT                        AS "HOP_DONG_MUA_ID"
                    , NULL :: INT                        AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                        AS "TAI_KHOAN_NGAN_HANG"
                    , NULL :: INT                        AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                      AS "DIEN_GIAI_CHUNG"
                    , ''                                 AS "DIEN_GIAI"
                    , NULL :: INT                        AS "MA_HANG_ID_CT"
                    , NULL :: INT                        AS "DVT_ID_CT"
                    , NULL :: INT                        AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                        AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                        AS "DON_VI_ID_CT"
                    , ''                                 AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                   AS "CHI_NHANH_ID"
                    , D.id                               AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                AS "SOURCE_ID"
                FROM tong_hop_chung_tu_ghi_so M
                    INNER JOIN tong_hop_chung_tu_ghi_so_chi_tiet D ON M.id = D."CHUNG_TU_GHI_SO_ID"

                UNION ALL

                SELECT
                    M.id                                   AS "ID_GOC"
                    , 'gia.thanh.ket.chuyen.chi.phi' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"                      AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                        AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                      AS "NGAY_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"                      AS "NGAY_HACH_TOAN"
                    , NULL :: INT                            AS "currency_id"
                    , ''                                     AS "SO_HOA_DON"
                    , NULL :: DATE                           AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                           AS "TK_NO_ID"
                    , D."TK_CO_ID"                           AS "TK_CO_ID"
                    , NULL :: INT                            AS "MA_HANG_ID"
                    , ''                                     AS "TEN_HANG"
                    , NULL :: INT                            AS "DVT_ID"
                    , NULL :: INT                            AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                            AS "MA_KHO_XUAT_ID"
                    , 0                                      AS "SO_LUONG"
                    , 0                                      AS "DON_GIA"
                    , D."SO_TIEN"                            AS "SO_TIEN"
                    , D."SO_TIEN"                            AS "SO_TIEN_QUY_DOI"
                    , 0                                      AS "TY_LE_CHIET_KHAU"
                    , 0                                      AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                      AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                                      AS "TONG_TIEN"
                    , 0                                      AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                            AS "TSCD_ID"
                    , NULL :: INT                            AS "LOAI_TSCD_ID"
                    , NULL :: INT                            AS "CCDC_ID"
                    , NULL :: INT                            AS "DOI_TUONG_ID"
                    , NULL :: INT                            AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                            AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                            AS "DON_VI_ID"
                    , NULL :: INT                            AS "NHAN_VIEN_ID"
                    , NULL :: INT                            AS "KHOAN_MUC_CP_ID"
                    , "MA_CONG_TRINH_ID"                     AS "CONG_TRINH_ID"
                    , "MA_DOI_TUONG_THCP_ID"                 AS "DOI_TUONG_THCP_ID"
                    , "SO_DON_HANG_ID"                       AS "DON_DAT_HANG_ID"
                    , NULL :: INT                            AS "DON_MUA_HANG_ID"
                    , NULL :: INT                            AS "HOP_DONG_MUA_ID"
                    , "HOP_DONG_BAN_ID"                      AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                            AS "TAI_KHOAN_NGAN_HANG"
                    , "MA_THONG_KE_ID"                       AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                          AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI"                          AS "DIEN_GIAI"
                    , NULL :: INT                            AS "MA_HANG_ID_CT"
                    , NULL :: INT                            AS "DVT_ID_CT"
                    , D."MA_DOI_TUONG_THCP_ID"               AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                            AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                            AS "DON_VI_ID_CT"
                    , M.state                                AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"                       AS "CHI_NHANH_ID"
                    , D.id                                   AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)                    AS "SOURCE_ID"
                FROM gia_thanh_ket_chuyen_chi_phi M
                    INNER JOIN gia_thanh_ket_chuyen_chi_phi_hach_toan D ON M.id = D."CHI_TIET_ID"

                UNION ALL

                SELECT
                    M.id                           AS "ID_GOC"
                    , 'gia.thanh.nghiem.thu' :: TEXT AS "MODEL_GOC"
                    , M."LOAI_CHUNG_TU"              AS "LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"                AS "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"              AS "NGAY_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"              AS "NGAY_HACH_TOAN"
                    , NULL :: INT                    AS "currency_id"
                    , ''                             AS "SO_HOA_DON"
                    , NULL :: DATE                   AS "NGAY_HOA_DON"
                    , D."TK_NO_ID"                   AS "TK_NO_ID"
                    , D."TK_CO_ID"                   AS "TK_CO_ID"
                    , NULL :: INT                    AS "MA_HANG_ID"
                    , ''                             AS "TEN_HANG"
                    , NULL :: INT                    AS "DVT_ID"
                    , NULL :: INT                    AS "MA_KHO_NHAP_ID"
                    , NULL :: INT                    AS "MA_KHO_XUAT_ID"
                    , 0                              AS "SO_LUONG"
                    , 0                              AS "DON_GIA"
                    , D."GIA_TRI_NGHIEM_THU"         AS "SO_TIEN"
                    , D."GIA_TRI_NGHIEM_THU"         AS "SO_TIEN_QUY_DOI"
                    , 0                              AS "TY_LE_CHIET_KHAU"
                    , 0                              AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , 0                              AS "SO_TIEN_CHIET_KHAU_QUY_DOI"
                    , M."SO_TIEN"                    AS "TONG_TIEN"
                    , M."SO_TIEN"                    AS "TONG_TIEN_QUY_DOI"
                    , NULL :: INT                    AS "TSCD_ID"
                    , NULL :: INT                    AS "LOAI_TSCD_ID"
                    , NULL :: INT                    AS "CCDC_ID"
                    , NULL :: INT                    AS "DOI_TUONG_ID"
                    , NULL :: INT                    AS "DOI_TUONG_NO_ID"
                    , NULL :: INT                    AS "DOI_TUONG_CO_ID"
                    , NULL :: INT                    AS "DON_VI_ID"
                    , NULL :: INT                    AS "NHAN_VIEN_ID"
                    , D."KHOAN_MUC_CP_ID"            AS "KHOAN_MUC_CP_ID"
                    , "MA_CONG_TRINH_ID"             AS "CONG_TRINH_ID"
                    , NULL :: INT                    AS "DOI_TUONG_THCP_ID"
                    , "SO_DON_HANG_ID"               AS "DON_DAT_HANG_ID"
                    , NULL :: INT                    AS "DON_MUA_HANG_ID"
                    , NULL :: INT                    AS "HOP_DONG_MUA_ID"
                    , "HOP_DONG_BAN_ID"              AS "HOP_DONG_BAN_ID"
                    , NULL :: INT                    AS "TAI_KHOAN_NGAN_HANG"
                    , "MA_THONG_KE_ID"               AS "MA_THONG_KE_ID"
                    , M."DIEN_GIAI"                  AS "DIEN_GIAI_CHUNG"
                    , D."DIEN_GIAI"                  AS "DIEN_GIAI"
                    , NULL :: INT                    AS "MA_HANG_ID_CT"
                    , NULL :: INT                    AS "DVT_ID_CT"
                    , NULL :: INT                    AS "DOI_TUONG_THCP_ID_CT"
                    , NULL :: INT                    AS "KHOAN_MUC_CP_ID_CT"
                    , NULL :: INT                    AS "DON_VI_ID_CT"
                    , M.state                        AS "TRANG_THAI_GHI_SO"
                    , M."CHI_NHANH_ID"               AS "CHI_NHANH_ID"
                    , D.id                           AS "CHI_TIET_ID"
                    , NULL :: VARCHAR(50)            AS "SOURCE_ID"
                FROM gia_thanh_nghiem_thu M
                    INNER JOIN gia_thanh_nghiem_thu_hach_toan D ON M.id = D."CHI_TIET_ID"


            ) kq
            LEFT JOIN danh_muc_reftype rt ON kq."LOAI_CHUNG_TU" = rt."REFTYPE"
        WHERE
            kq."LOAI_CHUNG_TU" NOT IN
            (6023, 6021, 6022, 256, 6030, 4100)
        GROUP BY
            kq."ID_GOC",
            kq."MODEL_GOC",
            kq."LOAI_CHUNG_TU",
            rt."REFTYPENAME",
            kq."NGAY_HACH_TOAN",
            kq."NGAY_CHUNG_TU",
            kq."SO_CHUNG_TU",
            kq."SO_HOA_DON",
            kq."NGAY_HOA_DON",
            kq."TK_NO_ID",
            kq."TK_CO_ID",
            kq."SO_TIEN",
            kq."currency_id",
            kq."SO_TIEN_QUY_DOI",
            kq."MA_HANG_ID",
            KQ."TEN_HANG",
            kq."MA_KHO_NHAP_ID",
            kq."MA_KHO_XUAT_ID",
            kq."DVT_ID",
            kq."SO_LUONG",
            kq."DON_GIA",
            kq."TY_LE_CHIET_KHAU",
            kq."SO_TIEN_CHIET_KHAU",
            kq."TSCD_ID",
            kq."LOAI_TSCD_ID",
            kq."CCDC_ID",
            kq."DOI_TUONG_ID",
            kq."DOI_TUONG_NO_ID",
            kq."DOI_TUONG_CO_ID",
            kq."DON_VI_ID",
            kq."NHAN_VIEN_ID",
            kq."TK_NGAN_HANG",
            kq."KHOAN_MUC_CP_ID",
            kq."CONG_TRINH_ID",
            kq."DOI_TUONG_THCP_ID",
            kq."DON_MUA_HANG_ID",
            kq."DON_DAT_HANG_ID",
            kq."HOP_DONG_MUA_ID",
            kq."HOP_DONG_BAN_ID",
            kq."MA_THONG_KE_ID",
            kq."DIEN_GIAI_CHUNG",
            kq."DIEN_GIAI",
            kq."CHI_NHANH_ID",
            kq."CHI_TIET_ID",
            kq."SOURCE_ID",
        kq."TRANG_THAI_GHI_SO",
        kq."TONG_TIEN_QUY_DOI"
        ORDER BY kq."NGAY_CHUNG_TU", kq."SO_CHUNG_TU", kq."LOAI_CHUNG_TU"
            )""")


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    size = fields.Char(string='Size')
    create_list = fields.Char(string='Danh sách tạo mới')
    option = fields.Char(string='Options')