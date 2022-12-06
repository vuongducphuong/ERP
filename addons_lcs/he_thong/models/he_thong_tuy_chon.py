# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from ast import literal_eval
import datetime

class HE_THONG_TUY_CHON(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Tùy chọn'

    # user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user.id)
    HAN_CHE_TAI_KHOAN_KHI_NHAP_CHUNG_TU = fields.Boolean(string='Hạn chế tài khoản khi nhập chứng từ')
    PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = fields.Selection(selection=[('BINH_QUAN_CUOI_KY', 'Bình quân cuối kỳ'), ('BINH_QUAN_TUC_THOI', 'Bình quân tức thời')], default='BINH_QUAN_CUOI_KY', string='Phương pháp tính tỷ giá xuất quỹ', required=True)
    TK_XU_LY_LAI_CHENH_LECH_TGXQ = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lãi')
    TK_XU_LY_LO_CHENH_LECH_TGXQ = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lỗ')
    TK_XU_LY_LAI_CHENH_LECH_TGTHKHTTNCC = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lãi')
    TK_XU_LY_LO_CHENH_LECH_TGTHKHTTNCC = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lỗ')
    PHUONG_PHAP_TINH_GIA_XUAT_KHO = fields.Selection(selection=[('BINH_QUAN_CUOI_KY', 'Bình quân cuối kỳ'), ('GIA_DICH_DANH', 'Giá đích danh'), ('BINH_QUAN_TUC_THOI', 'Bình quân tức thời'),('NHAP_TRUOC_XUAT_TRUOC', 'Nhập trước xuất trước'),], default='BINH_QUAN_CUOI_KY', string='Phương pháp tính giá xuất kho', required=True)
    CHE_DO_KE_TOAN = fields.Selection(selection=[('15', 'Chế độ kế toán doanh nghiệp ban hành theo Thông tư 200/2014/TT-BTC'), ('48', 'Chế độ kế toán doanh nghiệp nhỏ và vừa ban hành theo Thông tư 133/2016/TT-BTC')], default='0', string='Chế độ kế toán')
    CACH_LAY_SO_LIEU_THUC_THI = fields.Selection(selection=[('0', 'Khi ghi nhận chi phí'), ('1', 'Khi thực chi bằng tiền'), ('2', 'Cả hai')], default='1', string='Cách lấy số liệu Thực chi của Hợp đồng bán',required=True)
    LOAI_TIEN_CHINH = fields.Many2one('res.currency', string='Loại tiền tệ chính', help='Loại tiền tệ chính')
    NAM_TAI_CHINH_BAT_DAU = fields.Integer(string='Năm tài chính bắt đầu', help='Năm tài chính bắt đầu')
    TU_NGAY_BAT_DAU_TAI_CHINH = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY_BAT_DAU_TAI_CHINH = fields.Date(string='Đến ngày', help='Đến ngày')
    LAM_VIEC_NGAY_THU_7 = fields.Boolean(string='Làm việc ngày Thứ bảy', help='Làm việc ngày Thứ bảy')
    LAM_VIEC_NGAY_CHU_NHAT = fields.Boolean(string='Làm việc ngày Chủ nhật', help='Làm việc ngày Chủ nhật')

    # Task 3513
    CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH = fields.Boolean(string='Có vật tư số lượng theo chu vi, thể tích', help='Có vật tư số lượng theo chu vi, thể tích')


    LINH_VUC_HOAT_DONG = fields.Selection(selection=[('0', 'Thương mại dịch vụ'), ('1', 'Lắp ráp, sản xuất'), ('2', 'Thương mại dịch vụ và lắp ráp, sản xuất')], default='0', string='Lĩnh vực hoạt động',required=True)
    CHO_PHEP_XUAT_QUA_SO_LUONG_TON = fields.Boolean(string='Cho phép xuất quá số lượng tồn', help='Cho phép xuất quá số lượng tồn')
    PHAN_THAP_PHAN_SO_LUONG = fields.Integer(string='Số lượng', help='Số chữ số của phần thập phân Số lượng')
    PHAN_THAP_PHAN_DON_GIA = fields.Integer(string='Đơn giá', help='Số chữ số của phần thập phân Đơn giá')
    PHAN_THAP_PHAN_SO_CONG = fields.Integer(string='Số công', help='Số chữ số của phần thập phân Số công')
    PHAN_THAP_PHAN_KICH_THUOC = fields.Integer(string='Kích thước', help='Số chữ số của phần thập phân chiều dài/chiều rộng..')
    LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG = fields.Boolean(string='Lấy số lượng đã giao từ chứng tù bán hàng', help='Lấy số lượng đã giao từ chứng tù bán hàng')

    CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN = fields.Selection(selection=[('0', 'Phân bổ tròn tháng'), ('1', 'Phân bổ từ ngày ghi tăng')], string='Cách phân bổ CCDC, chi phí trả trước tháng đầu tiên',help='AllocateAmountFirstMonthByDate',required=True)
    CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = fields.Boolean(string='Cộng gộp số liệu theo hàng hóa, số lô', help='Cộng gộp số liệu theo hàng hóa, số lô... trên hóa đơn bán hàng, phiếu xuất khi in')
   

    CONG_GOP_DON_GIA_DVT_MA_HANG = fields.Boolean(string='Cộng gộp đơn giá, đơn vị tính, mã hàng', help='Cộng gộp theo VTHH, ĐVT, đơn giá giống nhau khi in phiếu nhập kho')
    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI = fields.Integer(string='Phần thập phân số tiền quy đổi', help='Số chữ số phần thập phân của tiền quy đổi')
    PHAN_THAP_PHAN_TY_GIA = fields.Integer(string='Phần thập phân tỷ giá', help='Số chữ số của phần thập phân của tỷ giá')

    PHUONG_PHAP_TINH_THUE = fields.Selection(selection=[('PHUONG_PHAP_KHAU_TRU', 'Tính thuế GTGT theo phương pháp khấu trừ'), ('PHUONG_PHAP_TRUC_TIEP_TREN_DOANH_THU', 'Tính thuế GTGT theo phương pháp trực tiếp trên doanh thu')], string='Phương pháp tính thuế',required=True)
    
    KIEU_HIEN_THI_TIEU_DE = fields.Selection(selection=[('CHUAN', 'Chuẩn'), ('TUY_CHINH', 'Tùy chỉnh')], default='CHUAN', string='Kiểu hiển thị', required=True)
    PHAN_THAP_PHAN_CUA_HE_SO_TY_LE = fields.Integer(string='Phần thập phân của hệ số/tỷ lệ', help='Định dạng số:Phần thập phân của hệ số/tỷ lệ')
    CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB = fields.Boolean(string='Cách lấy số lượng đã giao của VTHH trên đơn đặt hàng, hợp đồng bán', help='Tùy chọn VTHH:Cách lấy số lượng đã giao của VTHH trên đơn đặt hàng, hợp đồng bán')
    CO_PHAT_SINH_BAN_HANG_SAU_THUE = fields.Boolean(string='Có phát sinh bán hàng sau thuế', help='Tùy chọn chung: Có phát sinh bán hàng sau thuế')
    PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO = fields.Integer(string='Phần thập phân của tỷ lệ phân bổ', help='Định dạng số: Số chữ số sau dấu phẩy của tỷ lệ phân bổ')
    LUONG_CO_BAN_DUA_TREN = fields.Selection(selection=[('LUONG_THOA_THUAN', 'Lương thỏa thuận'), ('MUC_LUONG_TOI_THIEU_VA_HE_SO_LUONG', 'Mức lương tối thiểu và hệ số lương')], string='Tùy chọn Lương: Lương cơ bản dựa trên Mức lương tối thiểu và hệ số lương',required=True)
    CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN = fields.Selection(selection=[('LAY_THEO_SO_TIEN_LUONG_PHAI_TRA_TREN_BANG_LUONG', 'Lấy theo số tiền lương phải trả trên bảng lương'), ('LAY_THEO_SO_DU_CUA_TK_334', 'Lấy theo số dư của tài khoản 334')], string='Tùy chọn trả lương: Cách lấy số tiền lương phải trả cho nhân viên',required=True)
    CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = fields.Boolean(string='Cập nhật giá nhập kho hàng bán trả lại khi tính giá xuất kho', help='Tùy chọn: Cập nhật giá nhập kho hàng bán trả lại khi tính giá xuất kho')

    TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG = fields.Boolean(string='Tạo chứng từ bán hàng từ nhiều đơn đặt hàng')
    @api.model
    def get_values(self):
        res = super(HE_THONG_TUY_CHON, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        loai_tien_chinh_id = literal_eval(ICPSudo.get_param('he_thong.LOAI_TIEN_CHINH', default='False'))
        if loai_tien_chinh_id and not self.env['res.currency'].sudo().browse(loai_tien_chinh_id).exists():
            loai_tien_chinh_id = False
        # Lấy giá trị mặc định nếu người dùng chưa thiết lập
        if not loai_tien_chinh_id:
            loai_tien_chinh = self.env['res.currency'].search([('name', '=', 'VND')], limit=1)
            if loai_tien_chinh:
                loai_tien_chinh_id = loai_tien_chinh.id

        tai_khoan_xu_ly_chenh_lech_ty_gia_id = literal_eval(ICPSudo.get_param('he_thong.TK_XU_LY_LAI_CHENH_LECH_TGXQ', default='False'))
        if tai_khoan_xu_ly_chenh_lech_ty_gia_id and not self.env['danh.muc.he.thong.tai.khoan'].sudo().browse(tai_khoan_xu_ly_chenh_lech_ty_gia_id).exists():
            tai_khoan_xu_ly_chenh_lech_ty_gia_id = False

        tai_khoan_xu_ly_lo_chenh_lech_id = literal_eval(ICPSudo.get_param('he_thong.TK_XU_LY_LO_CHENH_LECH_TGXQ', default='False'))
        if tai_khoan_xu_ly_lo_chenh_lech_id and not self.env['danh.muc.he.thong.tai.khoan'].sudo().browse(tai_khoan_xu_ly_lo_chenh_lech_id).exists():
            tai_khoan_xu_ly_lo_chenh_lech_id = False

        tai_khoan_xu_ly_lai_chenh_lech_tgthkhttncc_id = literal_eval(ICPSudo.get_param('he_thong.TK_XU_LY_LAI_CHENH_LECH_TGTHKHTTNCC', default='False'))
        if tai_khoan_xu_ly_lai_chenh_lech_tgthkhttncc_id and not self.env['danh.muc.he.thong.tai.khoan'].sudo().browse(tai_khoan_xu_ly_lai_chenh_lech_tgthkhttncc_id).exists():
            tai_khoan_xu_ly_lai_chenh_lech_tgthkhttncc_id = False

        tai_khoan_xu_ly_lo_chenh_lech_tgthkhttncc_id = literal_eval(ICPSudo.get_param('he_thong.TK_XU_LY_LO_CHENH_LECH_TGTHKHTTNCC', default='False'))
        if tai_khoan_xu_ly_lo_chenh_lech_tgthkhttncc_id and not self.env['danh.muc.he.thong.tai.khoan'].sudo().browse(tai_khoan_xu_ly_lo_chenh_lech_tgthkhttncc_id).exists():
            tai_khoan_xu_ly_lo_chenh_lech_tgthkhttncc_id = False

        res.update(
            PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY=ICPSudo.get_param('he_thong.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY'),
            TK_XU_LY_LAI_CHENH_LECH_TGXQ = tai_khoan_xu_ly_chenh_lech_ty_gia_id,
            TK_XU_LY_LO_CHENH_LECH_TGXQ = tai_khoan_xu_ly_lo_chenh_lech_id,
            TK_XU_LY_LAI_CHENH_LECH_TGTHKHTTNCC=tai_khoan_xu_ly_lai_chenh_lech_tgthkhttncc_id,
            TK_XU_LY_LO_CHENH_LECH_TGTHKHTTNCC= tai_khoan_xu_ly_lo_chenh_lech_tgthkhttncc_id,
            PHUONG_PHAP_TINH_GIA_XUAT_KHO=ICPSudo.get_param('he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO'),
            CHE_DO_KE_TOAN=ICPSudo.get_param('he_thong.CHE_DO_KE_TOAN'),
            CACH_LAY_SO_LIEU_THUC_THI=ICPSudo.get_param('he_thong.CACH_LAY_SO_LIEU_THUC_THI'),
            NAM_TAI_CHINH_BAT_DAU=int(ICPSudo.get_param('he_thong.NAM_TAI_CHINH_BAT_DAU')) or 2018,
            TU_NGAY_BAT_DAU_TAI_CHINH=ICPSudo.get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'),
            DEN_NGAY_BAT_DAU_TAI_CHINH=ICPSudo.get_param('he_thong.DEN_NGAY_BAT_DAU_TAI_CHINH'),
            LAM_VIEC_NGAY_THU_7=ICPSudo.get_param('he_thong.LAM_VIEC_NGAY_THU_7'),
            LAM_VIEC_NGAY_CHU_NHAT=ICPSudo.get_param('he_thong.LAM_VIEC_NGAY_CHU_NHAT'),
            # task 3513
            CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH=ICPSudo.get_param('he_thong.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH'),
            TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG=ICPSudo.get_param('he_thong.TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG'),            

            LOAI_TIEN_CHINH=loai_tien_chinh_id,
            LINH_VUC_HOAT_DONG=ICPSudo.get_param('he_thong.LINH_VUC_HOAT_DONG'),
            PHAN_THAP_PHAN_SO_LUONG=self.env['decimal.precision'].precision_get('SO_LUONG'),
            PHAN_THAP_PHAN_DON_GIA=self.env['decimal.precision'].precision_get('DON_GIA'),
            PHAN_THAP_PHAN_SO_CONG=self.env['decimal.precision'].precision_get('SO_CONG'),
            PHAN_THAP_PHAN_KICH_THUOC=self.env['decimal.precision'].precision_get('KICH_THUOC'),
            LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG=ICPSudo.get_param('he_thong.LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG'),
            CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN=ICPSudo.get_param('he_thong.CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN'),
            CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO=ICPSudo.get_param('he_thong.CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO'),          
            CONG_GOP_DON_GIA_DVT_MA_HANG=ICPSudo.get_param('he_thong.CONG_GOP_DON_GIA_DVT_MA_HANG'),
            CHO_PHEP_XUAT_QUA_SO_LUONG_TON=ICPSudo.get_param('he_thong.CHO_PHEP_XUAT_QUA_SO_LUONG_TON'),
            PHAN_THAP_PHAN_SO_TIEN_QUY_DOI=self.env['decimal.precision'].precision_get('SO_TIEN_QUY_DOI'),
            PHAN_THAP_PHAN_TY_GIA=self.env['decimal.precision'].precision_get('TY_GIA'),
            PHUONG_PHAP_TINH_THUE=ICPSudo.get_param('he_thong.PHUONG_PHAP_TINH_THUE'),
            KIEU_HIEN_THI_TIEU_DE=ICPSudo.get_param('he_thong.KIEU_HIEN_THI_TIEU_DE'),
            PHAN_THAP_PHAN_CUA_HE_SO_TY_LE=self.env['decimal.precision'].precision_get('HE_SO_TY_LE'),
            CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB=ICPSudo.get_param('he_thong.CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB'),
            CO_PHAT_SINH_BAN_HANG_SAU_THUE=ICPSudo.get_param('he_thong.CO_PHAT_SINH_BAN_HANG_SAU_THUE'),
            PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO=self.env['decimal.precision'].precision_get('TY_LE_PHAN_BO'),
            LUONG_CO_BAN_DUA_TREN=ICPSudo.get_param('he_thong.LUONG_CO_BAN_DUA_TREN'),
            CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN=ICPSudo.get_param('he_thong.CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN'),
            CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO=ICPSudo.get_param('he_thong.CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO'),
        )
        return res

    @api.multi
    def set_values(self):
        super(HE_THONG_TUY_CHON, self).set_values()
        # Tùy chọn riêng (theo user)
        self.env.user.write({
            'HAN_CHE_TAI_KHOAN_KHI_NHAP_CHUNG_TU': self.HAN_CHE_TAI_KHOAN_KHI_NHAP_CHUNG_TU,
        })
        # Tùy chọn chung
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('he_thong.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY', self.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY)
        ICPSudo.set_param('he_thong.TK_XU_LY_LAI_CHENH_LECH_TGXQ', self.TK_XU_LY_LAI_CHENH_LECH_TGXQ.id or None)
        ICPSudo.set_param('he_thong.TK_XU_LY_LO_CHENH_LECH_TGXQ', self.TK_XU_LY_LO_CHENH_LECH_TGXQ.id or None)
        ICPSudo.set_param('he_thong.TK_XU_LY_LAI_CHENH_LECH_TGTHKHTTNCC', self.TK_XU_LY_LAI_CHENH_LECH_TGTHKHTTNCC.id or None)
        ICPSudo.set_param('he_thong.TK_XU_LY_LO_CHENH_LECH_TGTHKHTTNCC', self.TK_XU_LY_LO_CHENH_LECH_TGTHKHTTNCC.id or None)
        ICPSudo.set_param('he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO', self.PHUONG_PHAP_TINH_GIA_XUAT_KHO)
        ICPSudo.set_param('he_thong.CHE_DO_KE_TOAN', self.CHE_DO_KE_TOAN)
        ICPSudo.set_param('he_thong.CACH_LAY_SO_LIEU_THUC_THI', self.CACH_LAY_SO_LIEU_THUC_THI)
        ICPSudo.set_param('he_thong.NAM_TAI_CHINH_BAT_DAU', self.NAM_TAI_CHINH_BAT_DAU)
        ICPSudo.set_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH', self.TU_NGAY_BAT_DAU_TAI_CHINH)
        ICPSudo.set_param('he_thong.DEN_NGAY_BAT_DAU_TAI_CHINH', self.DEN_NGAY_BAT_DAU_TAI_CHINH)
        ICPSudo.set_param('he_thong.LAM_VIEC_NGAY_THU_7', self.LAM_VIEC_NGAY_THU_7)
        ICPSudo.set_param('he_thong.LAM_VIEC_NGAY_CHU_NHAT', self.LAM_VIEC_NGAY_CHU_NHAT)
        ICPSudo.set_param('he_thong.TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG', self.TAO_CHUNG_TU_BAN_HANG_TU_NHIEU_DON_DAT_HANG)# task 3513
        ICPSudo.set_param('he_thong.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH', self.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH)# task 3513
        # Cập nhật lại sale.document và purchase.document, những model có sử dụng CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH
        self.env.cr.execute("""
            UPDATE sale_document SET "CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH" = %(value)s;
            UPDATE purchase_document SET "CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH" = %(value)s;
        """, {'value': self.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH})

        ICPSudo.set_param('he_thong.LOAI_TIEN_CHINH', self.LOAI_TIEN_CHINH.id)
        ICPSudo.set_param('he_thong.LINH_VUC_HOAT_DONG', self.LINH_VUC_HOAT_DONG)

        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_SO_LUONG', self.PHAN_THAP_PHAN_SO_LUONG)
        self.env['decimal.precision'].search([('name','=','SO_LUONG')]).write({'digits': self.PHAN_THAP_PHAN_SO_LUONG})

        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_DON_GIA', self.PHAN_THAP_PHAN_DON_GIA)
        self.env['decimal.precision'].search([('name','=','DON_GIA')]).write({'digits': self.PHAN_THAP_PHAN_DON_GIA})

        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_SO_CONG', self.PHAN_THAP_PHAN_SO_CONG)
        self.env['decimal.precision'].search([('name','=','SO_CONG')]).write({'digits': self.PHAN_THAP_PHAN_SO_CONG})

        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_KICH_THUOC', self.PHAN_THAP_PHAN_KICH_THUOC)
        self.env['decimal.precision'].search([('name','=','KICH_THUOC')]).write({'digits': self.PHAN_THAP_PHAN_KICH_THUOC})

        ICPSudo.set_param('he_thong.LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG', self.LAY_SL_DA_GIAO_TU_CHUNG_TU_BAN_HANG)
        ICPSudo.set_param('he_thong.CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN', self.CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN)

        ICPSudo.set_param('he_thong.CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO', self.CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO)
        ICPSudo.set_param('he_thong.CHO_PHEP_XUAT_QUA_SO_LUONG_TON', self.CHO_PHEP_XUAT_QUA_SO_LUONG_TON)
        ICPSudo.set_param('he_thong.CONG_GOP_DON_GIA_DVT_MA_HANG', self.CONG_GOP_DON_GIA_DVT_MA_HANG)

        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI', self.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
        self.env['decimal.precision'].search([('name','=','SO_TIEN_QUY_DOI')]).write({'digits': self.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI})

        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_TY_GIA', self.PHAN_THAP_PHAN_TY_GIA)
        self.env['decimal.precision'].search([('name','=','TY_GIA')]).write({'digits': self.PHAN_THAP_PHAN_TY_GIA})
        ICPSudo.set_param('he_thong.PHUONG_PHAP_TINH_THUE', self.PHUONG_PHAP_TINH_THUE)
        ICPSudo.set_param('he_thong.KIEU_HIEN_THI_TIEU_DE', self.KIEU_HIEN_THI_TIEU_DE)
        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_CUA_HE_SO_TY_LE', self.PHAN_THAP_PHAN_CUA_HE_SO_TY_LE)
        ICPSudo.set_param('he_thong.CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB', self.CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB)
        ICPSudo.set_param('he_thong.CO_PHAT_SINH_BAN_HANG_SAU_THUE', self.CO_PHAT_SINH_BAN_HANG_SAU_THUE)
        ICPSudo.set_param('he_thong.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO', self.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO)
        self.env['decimal.precision'].search([('name','=','TY_LE_PHAN_BO')]).write({'digits': self.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO})
        ICPSudo.set_param('he_thong.LUONG_CO_BAN_DUA_TREN', self.LUONG_CO_BAN_DUA_TREN)
        ICPSudo.set_param('he_thong.CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN', self.CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN)
        ICPSudo.set_param('he_thong.CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO', self.CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO)
    
    @api.onchange('NAM_TAI_CHINH_BAT_DAU')
    def _onchange_NAM_TAI_CHINH_BAT_DAU(self):
        self.TU_NGAY_BAT_DAU_TAI_CHINH = datetime.datetime(self.NAM_TAI_CHINH_BAT_DAU, 1, 1)
        self.DEN_NGAY_BAT_DAU_TAI_CHINH = datetime.datetime(self.NAM_TAI_CHINH_BAT_DAU, 12, 31)