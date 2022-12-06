# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError
from operator import itemgetter
from datetime import timedelta, datetime
import json

class ACCOUNT_EX_PHIEU_THU_CHI(models.Model):
    _name = 'account.ex.phieu.thu.chi'
    _description = 'Phiếu thu chi'
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"


    @api.depends('ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS.SO_TIEN_QUY_DOI')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien = 0.0
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                tong_tien += line.SO_TIEN_QUY_DOI

            order.update({
                'SO_TIEN_TREE': tong_tien,
            })
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    NGUOI_NOP = fields.Char(string='Người nộp', help='Người nộp')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    LY_DO_NOP = fields.Selection([('10', 'Rút tiền gửi về nộp quỹ'), ('11', ' Thu hoàn thuế GTGT'), ('12', ' Thu hoàn ứng'), ('13', 'Thu khác'), ], string='Lý do nộp', help='Lý do nộp',default='10',required=True)
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    KEM_THEO_CHUNG_TU_GOC = fields.Char(string='Kèm theo chứng từ gốc', help='Kèm theo chứng từ gốc')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    name = fields.Char(string='Name', related="SO_CHUNG_TU", )
    TEN_TK_THU = fields.Char(string='Tên tài khoản thu',help='Tên tài khoản thu')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền', )
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    NHOM_CHUNG_TU = fields.Integer(string='Nhóm chứng từ', help='Nhóm chứng từ')

    #VŨ THÊM
    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác')
	


    #Trường dành cho mẫu in
    NOP_TIEN_MAU_IN = fields.Char(string='Nộp tiền mẫu in', help='Nộp tiền mẫu in',store=False)

    TAI_NGAN_HANG_MAU_IN = fields.Char(string='Tại ngân hàng mẫu in', help='Tại ngân hàng mẫu in',store=False)



    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN
    
    # Bổ sung hàm depend để lấy loại chứng từ 
    @api.onchange('LOAI_PHIEU','TYPE_NH_Q','LY_DO_NOP','LY_DO_CHI','ly_do_thu','PHUONG_THUC_TT','NOI_DUNG_TT','LOAI_CHUNG_TU_TEMPLE')
    def set_ma_loai_chung_tu_thu_chi(self):
        for record in self:
            if record.TYPE_NH_Q =='QUY':
                if record.LOAI_PHIEU=='PHIEU_THU':
                    record.LOAI_CHUNG_TU = 1010
                    if record.LY_DO_NOP == '10':
                        record.NHOM_CHUNG_TU = 10
                    elif record.LY_DO_NOP =='11':
                        record.NHOM_CHUNG_TU = 11
                    elif record.LY_DO_NOP =='12':
                        record.NHOM_CHUNG_TU = 12
                    elif record.LY_DO_NOP =='13':
                        record.NHOM_CHUNG_TU = 13
                elif record.LOAI_PHIEU=='PHIEU_CHI' :
                    if record.LOAI_CHUNG_TU_TEMPLE == 1026 or record.LOAI_CHUNG_TU_TEMPLE == 1025 or record.LOAI_CHUNG_TU_TEMPLE == 1022:
                        record.LOAI_CHUNG_TU = record.LOAI_CHUNG_TU_TEMPLE
                    else:
                        if record.LY_DO_CHI == 'TAM_UNG_CHO_NHAN_VIEN':
                            record.NHOM_CHUNG_TU = 21
                        elif record.LY_DO_CHI =='GUI_TIEN_VAO_NGAN_HANG':
                            record.NHOM_CHUNG_TU = 22
                        elif record.LY_DO_CHI =='CHI_KHAC':
                            record.NHOM_CHUNG_TU = 23
                        record.LOAI_CHUNG_TU = 1020                    
            elif record.TYPE_NH_Q =='NGAN_HANG':
                if record.LOAI_PHIEU=='PHIEU_THU':
                    record.LOAI_CHUNG_TU = 1500
                    if record.ly_do_thu == '30':
                        record.NHOM_CHUNG_TU = 30
                    elif record.ly_do_thu == '31':
                        record.NHOM_CHUNG_TU = 31
                    elif record.ly_do_thu == '32':
                        record.NHOM_CHUNG_TU = 32
                    elif record.ly_do_thu == '33':
                        record.NHOM_CHUNG_TU = 33
                    elif record.ly_do_thu == '34':
                        record.NHOM_CHUNG_TU = 34
                elif record.LOAI_PHIEU=='PHIEU_CHI':
                    if record.LOAI_CHUNG_TU_TEMPLE == 1523 or record.LOAI_CHUNG_TU_TEMPLE == 1522 or record.LOAI_CHUNG_TU_TEMPLE == 1512:
                        record.LOAI_CHUNG_TU = record.LOAI_CHUNG_TU_TEMPLE
                        
                    else:
                        if record.PHUONG_THUC_TT =='UY_NHIEM_CHI':
                            record.LOAI_CHUNG_TU = 1510
                            if record.NOI_DUNG_TT == '40':
                                record.NHOM_CHUNG_TU = 40
                            elif record.NOI_DUNG_TT == '42':
                                record.NHOM_CHUNG_TU = 42
                            elif record.NOI_DUNG_TT == '43':
                                record.NHOM_CHUNG_TU = 43
                        elif record.PHUONG_THUC_TT =='SEC_TIEN_MAT':
                            record.LOAI_CHUNG_TU = 1520
                            if record.NOI_DUNG_TT == '40':
                                record.NHOM_CHUNG_TU = 40
                            elif record.NOI_DUNG_TT == '42':
                                record.NHOM_CHUNG_TU = 42
                            elif record.NOI_DUNG_TT == '43':
                                record.NHOM_CHUNG_TU = 43
                        elif record.PHUONG_THUC_TT =='SEC_CHUYEN_KHOAN':
                            record.LOAI_CHUNG_TU = 1530
                            if record.NOI_DUNG_TT == '40':
                                record.NHOM_CHUNG_TU = 40
                            elif record.NOI_DUNG_TT == '42':
                                record.NHOM_CHUNG_TU = 42
                            elif record.NOI_DUNG_TT == '43':
                                record.NHOM_CHUNG_TU = 43
                elif record.LOAI_PHIEU=='PHIEU_CHUYEN_TIEN':
                    record.LOAI_CHUNG_TU = 1560

    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('account.ex.phieu.thu.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết', copy=True)
    ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS = fields.One2many('account.ex.phieu.thu.chi.thue', 'PHIEU_THU_THUE_ID', string='Phiếu thu chi thuế', copy=True)
    MO_RONG1 = fields.Char( string='Trường mở rộng 1', help='Trường mở rộng 1')
    MO_RONG2 = fields.Char( string='Trường mở rộng 2', help='Trường mở rộng 2')
    MO_RONG3 = fields.Char( string='Trường mở rộng 3', help='Trường mở rộng 3')
    SO_TIEN_TREE = fields.Float(string='Số tiền', help='Tổng tiền ',compute='tinh_tong_tien', store=True,digits= decimal_precision.get_precision('VND'))
    NGAY_GHI_SO = fields.Date(string='Ngày ghi sổ', help='Ngày ghi sổ',default=fields.Datetime.now)
    LY_DO_CHI = fields.Selection([('TAM_UNG_CHO_NHAN_VIEN', 'Tạm ứng cho nhân viên'), ('GUI_TIEN_VAO_NGAN_HANG', 'Gửi tiền vào ngân hàng'), ('CHI_KHAC', 'Chi khác'), ], string='Lý do chi', help='Lý do chi',default='CHI_KHAC')
    DIEN_GIAI_PC = fields.Text(string='Diễn giải', help='Diễn giải', related='DIEN_GIAI')

    # các trường của Ngân hàng - Phiếu chi tiền bổ sung
    PHUONG_THUC_TT = fields.Selection([('UY_NHIEM_CHI', 'Ủy nhiệm chi'),('SEC_CHUYEN_KHOAN', 'Séc chuyển khoản'),('SEC_TIEN_MAT', 'Séc tiền mặt'),], string='Phương thức thanh toán',help="Phương thức thanh toán" ,default='UY_NHIEM_CHI',required=True)
    TAI_KHOAN_CHI_GUI_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Tài khoản chi', help='Tài khoản chi')
    TEN_TK_CHI = fields.Char(string='Tên TK chi',help='Tên tài khoản chi')
    NGUOI_LINH_TIEN = fields.Char(string='Người lĩnh tiền',help='Người lĩnh tiền')
    SO_CMND = fields.Char(string='Số CMND',help='Số CMND')
    NGAY_CAP = fields.Date(string='Ngày cấp',help='Ngày cấp')
    NOI_CAP = fields.Char(string='Nơi cấp',help='Nơi cấp')
    TEN_TK_NHAN = fields.Char(string='Tên TK nhận',help='Tên tài khoản nhận')
    TAI_KHOAN_THU_NHAN_ID = fields.Many2one('danh.muc.doi.tuong.chi.tiet', string='Tài khoản đi', help='Tài khoản đi')
    NOI_DUNG_TT = fields.Selection([('40','Trả các khoản vay'),('42','Tạm ứng cho nhân viên'),('43','Chi khác')],string='Nội dung thanh toán', help='Nội dung thanh toán')
    TEN_NOI_DUNG_TT = fields.Text(string='Tên nội dung thanh toán',help='Tên nội dung thanh toán', related='DIEN_GIAI')
    TYPE_NH_Q = fields.Selection([('NGAN_HANG', 'Ngân hàng'), ('QUY', 'QUY'), ], string='TYPE_NH_Q', help='TYPE_NH_Q')
    TAI_KHOAN_DEN_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Tài khoản đến', help='Tài khoản đến')
    TAI_KHOAN_NOP_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Nộp vào TK', help='Nộp vào tài khoản')
    SOURCE_ID = fields.Reference(selection=[], string='Lập từ')
    SO_CHUNG_TU_TU_TANG_JSON = fields.Char(store=False)

    _sql_constraints = [
        ('SO_CHUNG_TU_PHIEU_THU_CHI_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
    ]

    # @api.onchange('ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS')
    # def _onchange_field(self):
    #     self.field = Giá trị

    @api.onchange('LOAI_CHUNG_TU', 'currency_id','NHOM_CHUNG_TU')
    def update_tai_khoan_ngam_dinh(self):
        # Trường hợp nộp bảo hiểm sẽ tự set tài khoản ngầm định
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3571
        if self.LOAI_CHUNG_TU not in (1522, 1025):
            tk_nd_ct = self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for line in self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                for tk in tk_nd_ct:
                    setattr(line, tk, tk_nd_ct.get(tk))
            tk_nd_thue = self.ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0), self.currency_id.name!='VND')
            for line in self.ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS:
                for tk in tk_nd_thue:
                    setattr(line, tk, tk_nd_thue.get(tk))

    @api.onchange('LOAI_PHIEU', 'TYPE_NH_Q','PHUONG_THUC_TT')
    def update_SO_CHUNG_TU(self):
        loai_chung_tu = False
        if self.TYPE_NH_Q == 'NGAN_HANG':
            if self.LOAI_PHIEU == 'PHIEU_CHI':
                if self.LOAI_CHUNG_TU == 1523 or self.LOAI_CHUNG_TU == 1522: #Mạnh thêm điều kiện để check trường hợp khi là ủy nhiệm chi Nộp bảo hiểm và unc trả lương
                    loai_chung_tu = 'UY_NHIEM_CHI'
                else:
                    loai_chung_tu = self.PHUONG_THUC_TT
            else:
                loai_chung_tu = 'THU_TIEN_GUI'
        else:
            loai_chung_tu = self.LOAI_PHIEU

        if loai_chung_tu:    
            auto_num = self.lay_so_chung_tu_tu_tang(loai_chung_tu)
            self.SO_CHUNG_TU = auto_num.get(loai_chung_tu)
            self.SO_CHUNG_TU_TU_TANG_JSON = json.dumps(auto_num)      

    def lay_so_chung_tu_tu_tang(self, loai_chung_tu):
        auto_num = json.loads(self.SO_CHUNG_TU_TU_TANG_JSON or '{}')
        if not auto_num.get(loai_chung_tu):
            code = 'account_ex_phieu_thu_chi_SO_CHUNG_TU_' + loai_chung_tu
            next_seq = self.env['ir.sequence'].next_char_by_code(code)
            auto_num[loai_chung_tu] = next_seq

        return auto_num

    def lay_so_chung_tu_tiep_theo(self):
        self.ensure_one()
        loai_chung_tu = False
        if self.TYPE_NH_Q == 'NGAN_HANG':
            if self.LOAI_PHIEU == 'PHIEU_CHI':
                loai_chung_tu = self.PHUONG_THUC_TT
            else:
                loai_chung_tu = 'THU_TIEN_GUI'
        else:
            loai_chung_tu = self.LOAI_PHIEU

        if loai_chung_tu:
            code = 'account_ex_phieu_thu_chi_SO_CHUNG_TU_' + loai_chung_tu
            return self.env['ir.sequence'].next_char_by_code(code)
        
        return super(ACCOUNT_EX_PHIEU_THU_CHI, self).lay_so_chung_tu_tiep_theo()

    # Các trường của ngân hàng: Chuyển tiền nội bộ
    TEN_TK_NHAN_CTNB = fields.Char(string='Tên tài khoản nhận',help='Tên tài khoản nhận')

    # các trường của Ngân hàng - Phiếu thu tiền bổ sung
    DIEN_GIAI_LIST = fields.Char(string='Diễn giải',help='Diễn giải')
    SO_TIEN_1 = fields.Monetary(string='Số tiền',compute='tinhtongtien', currency_field='currency_id',store =True)
    LY_DO_THU_LIST = fields.Char(string='Loại chứng từ',help='Loại chứng từ')
    ly_do_thu = fields.Selection([('30', 'Vay nợ'), ('31', 'Thu lãi đầu tư tài chính'), ('32', 'Thu hoàn ứng'),('33', 'Thu hoàn thuế GTGT'),('34', 'Thu khác') ], string='Lý do thu', help='Lý do thu',default='30',required=True)
    TEN_LY_DO_THU = fields.Text(string='Tên lý do thu',help='Tên lý do thu',related='DIEN_GIAI')
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
    SO_THUE_ID = fields.Many2one('so.thue', ondelete='set null')

    # các trường của Ủy nhiệm chi trả lương nhân viên
    TIEN_LUONG_UY_NHIEM_CHI_THONG_TIN_TRA_LUONG_NHAN_VIEN_IDS = fields.One2many('tien.luong.uy.nhiem.chi.thong.tin.tra.luong.nhan.vien', 'THONG_TIN_TRA_LUONG_CHI_TIET_ID', string='Ủy nhiệm chi thông tin trả lương nhân viên', copy=True)
    LOAI_CHUNG_TU_TEMPLE = fields.Integer(store=False)
    
    NOI_DUNG_THANH_TOAN_UNC_TRA_LUONG_NHAN_VIEN = fields.Char(string='Nội dung TT' , help='Nội dung thanh toán')

    # Bổ sung thêm trường Phiếu chi trả lương nhân viên
    LY_DO_CHI_PC_TRA_LUONG_NHAN_VIEN  = fields.Char(string='Lý do chi' , help='Lý do chi')

    # Bổ sung thêm trường Ủy nhiệm chi nộp tiền bảo hiểm 
    NOI_DUNG_THANH_TOAN_UNC_NOP_TIEN = fields.Char(string='Nội dung TT' , help='Nội dung thanh toán')
    CO_QUAN_BH_UNC_NOP_TIEN = fields.Char(string='Cơ quan BH' , help='Cơ quan bảo hiểm')
    TAI_KHOAN_NHAN_UNC_NOP_TIEN = fields.Char(string='Tài khoản nhận' , help='Tài khoản nhận')
    TEN_TAI_KHOAN_NHAN_UNC_NOP_TIEN = fields.Char(string='Tên tài khoản nhận' , help='Tên tài khoản nhận')

    # Bổ sung thêm trường Phiếu chi nộp tiền bảo hiểm
    LY_DO_CHI_PC_NOP_TIEN = fields.Char(string='Lý do chi' , help='Lý do chi')

    # Bổ sung thêm trường Ủy nhiệm chi Chi tiền gửi nộp thuế
    NOI_DUNG_THANH_TOAN_UNC_NOP_THUE = fields.Char(string='Nội dung TT' , help='Nội dung thanh toán')
    KHO_BAC = fields.Char(string='Kho bạc' , help='Kho bạc')
    TAI_KHOAN_NHAN_UNC_NOP_THUE = fields.Char(string='Tài khoản nhận' , help='Tài khoản nhận')
    TEN_TAI_KHOAN_NHAN_UNC_NOP_THUE = fields.Char(string='Tên tài khoản nhận' , help='Tên tài khoản nhận')

    # Bổ sung thêm trường Phiếu chi nộp thuế
    LY_DO_CHI_PC_NOP_THUE = fields.Char(string='Lý do chi' , help='Lý do chi')
    # NGUOI_NHAN = fields.Char(string='Người nhận' , help='Người nhận')

    #Mạnh bổ sung 2 trường là Tên tài khoản ngân hàng, và địa chỉ ngân hàng để phục vụ cho làm mẫu in ủy nhiệm chi ngân hàng
    TEN_TK_NGAN_HANG  = fields.Char(string='Tên tài khoản Ngân hàng',compute='lay_thong_tin_cua_to_chuc' ,store=False)
    DIA_CHI_NGAN_HANG  = fields.Char(string='Địa chỉ Ngân hàng',compute='lay_thong_tin_cua_to_chuc' ,store=False)

    @api.depends('CHI_NHANH_ID')
    def lay_thong_tin_cua_to_chuc(self):
        for record in self:
            record.TEN_TK_NGAN_HANG = record.CHI_NHANH_ID.TEN_DON_VI
            record.DIA_CHI_NGAN_HANG = record.CHI_NHANH_ID.DIA_CHI


    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        for line in self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
            line.tinh_tien_quy_doi()
    
    @api.depends('ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS.SO_TIEN')
    def tinhtongtien(self):
        for order in self:
            tong_so_tien = 0
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS: 
                tong_so_tien += line.SO_TIEN
            order.update({
                'SO_TIEN_1': tong_so_tien,
            })

    @api.onchange('NOI_DUNG_TT')
    def update_tenNoiDungThanhToan(self):
        if self.NOI_DUNG_TT=='43':
            self.TEN_NOI_DUNG_TT = 'Chi khác'
        elif self.NOI_DUNG_TT=='40':
            self.TEN_NOI_DUNG_TT = 'Trả các khoản vay'
        elif self.NOI_DUNG_TT == '42':
            self.TEN_NOI_DUNG_TT = 'Tạm ứng cho nhân viên'

    @api.onchange('ly_do_thu')
    def thaydoildt(self):
        if self.ly_do_thu == False:
            return
        elif self.ly_do_thu in ('30'):
            self.TEN_LY_DO_THU = "Vay tiền của..."
        elif self.ly_do_thu in ('31'):
            self.TEN_LY_DO_THU = "Thu lãi đầu tư tài chính ..."
        elif self.ly_do_thu in ('32'):
            self.TEN_LY_DO_THU = 'Thu hoàn tạm ứng của nhân viên ...'
        elif self.ly_do_thu in ('33'):
            self.TEN_LY_DO_THU = 'Thu hoàn thuế GTGT'
        else:
            self.TEN_LY_DO_THU = 'Thu từ ...'
        for order in self:
            diengiai = ['Thu hoàn thuế GTGT','Thu hoàn ứng','Thu khác','Vay nợ','Thu lãi tài chính']
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                line.DIEN_GIAI_DETAIL = str(order.TEN_LY_DO_THU) if line.DIEN_GIAI_DETAIL in diengiai else line.DIEN_GIAI_DETAIL
                self.DIEN_GIAI_LIST = line.DIEN_GIAI_DETAIL

    @api.model
    def default_get(self,default_fields):
        res = super(ACCOUNT_EX_PHIEU_THU_CHI, self).default_get(default_fields)
        res['LY_DO_THU_LIST'] = 'Thu tiền gửi'

        currency_dto = self.env['res.currency'].search([('MA_LOAI_TIEN', '=','VND')],limit=1)
        if currency_dto:
            res['currency_id'] = currency_dto.id

        if self._context.get('default_LOAI_CHUNG_TU'):
            res['LOAI_CHUNG_TU_TEMPLE'] = self._context.get('default_LOAI_CHUNG_TU')
            if self._context.get('default_LOAI_CHUNG_TU') == 1523 or self._context.get('default_LOAI_CHUNG_TU') == 1026:
                loai_chung_tu =  self._context.get('default_LOAI_CHUNG_TU')
                default = self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(loai_chung_tu, 0, currency_dto.name!='VND')
                phieu_chi_tra_luong_hach_toan_list = []
                phieu_chi_tra_luong_thong_tin_tra_luong_list = []
                thong_tin_tra_luong_list = self._context.get('default_arr_list_thong_tin_tra_luong_nhan_vien')

                ngay_tra_luong = self._context.get('default_ngay_tra_luong')
                time_thang= datetime.strptime(ngay_tra_luong,'%Y-%m-%d').date().month
                time_year= datetime.strptime(ngay_tra_luong,'%Y-%m-%d').date().year
                str_dien_giai_tra_luong = 'Trả lương nhân viên tháng '+ str(time_thang)+ ' năm '+ str(time_year)

                tong_tien = 0
                for thong_tin in thong_tin_tra_luong_list:
                    tong_tien += thong_tin[2].get('SO_TRA')
                    phieu_chi_tra_luong_thong_tin_tra_luong_list += [(0,0,{
                    'MA_NHAN_VIEN' :thong_tin[2].get('MA_NHAN_VIEN'),
                    'DON_VI' :thong_tin[2].get('DON_VI'),
                    'TEN_NHAN_VIEN' :thong_tin[2].get('TEN_NHAN_VIEN'),
                    'SO_TAI_KHOAN' :thong_tin[2].get('SO_TAI_KHOAN'),
                    'TEN_NGAN_HANG' :thong_tin[2].get('TEN_NGAN_HANG'),
                    'SO_CON_PHAI_TRA' :thong_tin[2].get('SO_CON_PHAI_TRA'),
                    'SO_TRA' :thong_tin[2].get('SO_TRA'),
                    })]

                phieu_chi_tra_luong_hach_toan_list += [(0,0,{
                'DIEN_GIAI_DETAIL': str_dien_giai_tra_luong,
                'SO_TIEN': tong_tien,
                'SO_TIEN_QUY_DOI': tong_tien,
                'TK_NO_ID' :default.get('TK_NO_ID'),
                'TK_CO_ID' :default.get('TK_CO_ID'),
                })]

                if loai_chung_tu == 1523:
                    res['NOI_DUNG_THANH_TOAN_UNC_TRA_LUONG_NHAN_VIEN'] = str_dien_giai_tra_luong
                elif loai_chung_tu == 1026:
                    res['LY_DO_CHI_PC_TRA_LUONG_NHAN_VIEN'] = str_dien_giai_tra_luong

                res['NGAY_HACH_TOAN'] = ngay_tra_luong
                res['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] = phieu_chi_tra_luong_hach_toan_list
                res['TIEN_LUONG_UY_NHIEM_CHI_THONG_TIN_TRA_LUONG_NHAN_VIEN_IDS'] = phieu_chi_tra_luong_thong_tin_tra_luong_list
                # Trường hợp nộp bảo hiểm
            if self._context.get('default_LOAI_CHUNG_TU') == 1522 or self._context.get('default_LOAI_CHUNG_TU') == 1025:
                loai_chung_tu =  self._context.get('default_LOAI_CHUNG_TU')
                default = self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS.lay_tai_khoan_ngam_dinh(loai_chung_tu, 0, currency_dto.name!='VND')
                hach_toan_nop_bao_hiem_list = []
                thong_tin_nop_bao_hiem_list = self._context.get('default_arr_list_thong_tin_nop_bao_hiem')

                ngay_nop_bao_hiem = self._context.get('default_ngay_nop_bao_hiem')
                time_thang= datetime.strptime(ngay_nop_bao_hiem,'%Y-%m-%d').date().month
                time_year= datetime.strptime(ngay_nop_bao_hiem,'%Y-%m-%d').date().year
                str_dien_giai_nop_bao_hiem = 'Nộp bảo hiểm tháng '+ str(time_thang)+ ' năm '+ str(time_year)
                
                tk_co = None
                tk_co_id = None
                
                if loai_chung_tu == 1522:
                    res['NOI_DUNG_THANH_TOAN_UNC_NOP_TIEN'] = str_dien_giai_nop_bao_hiem
                    tk_co = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=','1121')],limit=1)
                    
                elif loai_chung_tu == 1025:
                    res['LY_DO_CHI_PC_NOP_TIEN'] = str_dien_giai_nop_bao_hiem
                    tk_co = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=','1111')],limit=1)
                   
                if tk_co:
                    tk_co_id = tk_co.id
                
                for thong_tin in thong_tin_nop_bao_hiem_list:
                    hach_toan_nop_bao_hiem_list += [(0,0,{
                    'DIEN_GIAI_DETAIL' :thong_tin[2].get('DIEN_GIAI_DETAIL'),
                    'SO_TIEN' :thong_tin[2].get('SO_TIEN'),
                    'SO_TIEN_QUY_DOI' :thong_tin[2].get('SO_TIEN'),
                    'TK_NO_ID' :thong_tin[2].get('TK_NO_ID'),
                    'TK_CO_ID' :tk_co_id,
                    })]

                res['NGAY_HACH_TOAN'] = ngay_nop_bao_hiem
                res['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] = hach_toan_nop_bao_hiem_list
        return res

    LOAI_PHIEU = fields.Selection([('PHIEU_THU','Phiếu thu'), ('PHIEU_CHI','Phiếu chi'), ('PHIEU_CHUYEN_TIEN','Chuyển tiền nội bộ'),], default='PHIEU_THU')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_MUA_HANG_ID = fields.Many2one('so.mua.hang', ondelete='set null')

    @api.onchange('DOI_TUONG_ID')
    def thaydoidoituong(self):
        if self.DOI_TUONG_ID:
            self.TEN_DOI_TUONG = self.DOI_TUONG_ID.HO_VA_TEN
            self.NGUOI_NOP= self.env['res.partner'].search([('parent_id', '=',self.DOI_TUONG_ID.id)], limit=1).HO_VA_TEN
            self.DIA_CHI = self.DOI_TUONG_ID.DIA_CHI
            self.TAI_KHOAN_THU_NHAN_ID = self.env['danh.muc.doi.tuong.chi.tiet'].search([('DOI_TUONG_ID', '=',self.DOI_TUONG_ID.id)], limit=1).id

    @api.onchange('LY_DO_NOP')
    def thaydoidiengiai(self):
        str1 ='Rút tiền gửi về nộp quỹ'
        str2 ='Thu hoàn thuế GTGT'
        str3 ='Thu hoàn ứng sau khi quyết toán tạm ứng nhân viên'
        str4 ='Thu khác'
        if self.LY_DO_NOP == '10':
            self.DIEN_GIAI=str1
        elif self.LY_DO_NOP=='11':
            self.DIEN_GIAI=str2
        elif self.LY_DO_NOP=='12':
            self.DIEN_GIAI=str3
        else :
            self.DIEN_GIAI=str4

    @api.onchange('LY_DO_CHI')
    def thaydoidiengiaipc(self):
        str1 ='Tạm ứng cho nhân viên'
        str2 ='Gửi tiền vào ngân hàng'
        str3 ='Chi khác'
        
        if self.LY_DO_CHI == 'TAM_UNG_CHO_NHAN_VIEN':
            self.DIEN_GIAI_PC=str1
        elif self.LY_DO_CHI=='GUI_TIEN_VAO_NGAN_HANG':
            self.DIEN_GIAI_PC=str2
        else :
            self.DIEN_GIAI_PC=str3     

    @api.onchange('DIEN_GIAI')
    def thaydoidiengiaidetail(self):
        for order in self:
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                line.DIEN_GIAI_DETAIL = order.DIEN_GIAI

    @api.onchange('DIEN_GIAI_PC')
    def thaydoidiengiaidetailPC(self):
        for order in self:
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                line.DIEN_GIAI_DETAIL = order.DIEN_GIAI_PC 
                
    @api.onchange('DOI_TUONG_ID')
    def thaydoidoituongdetail(self):
        for order in self:
            for line in order.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                line.DOI_TUONG_ID = order.DOI_TUONG_ID 
                line.TEN_DOI_TUONG = order.TEN_DOI_TUONG 

    @api.onchange('TAI_KHOAN_NOP_ID')
    def LayTenTaiKhoanNop(self):
        self.TEN_TK_THU = self.TAI_KHOAN_NOP_ID.get_Ten_Ngan_hang(self.TAI_KHOAN_NOP_ID)

    @api.onchange('TAI_KHOAN_DEN_ID')
    def LayTenTaiKhoanDen(self):
        self.TEN_TK_NHAN_CTNB = self.TAI_KHOAN_DEN_ID.get_Ten_Ngan_hang(self.TAI_KHOAN_DEN_ID)

    @api.onchange('TAI_KHOAN_CHI_GUI_ID','TAI_KHOAN_THU_NHAN_ID')
    def thaydoittn(self):
        tenTknhan = ''
        tenTkThu = ''
        if self.TAI_KHOAN_THU_NHAN_ID:
            tenTknhan = self.TAI_KHOAN_THU_NHAN_ID.TEN_NGAN_HANG
            self.TEN_TK_NHAN = tenTknhan
            tenTkThu = self.TAI_KHOAN_THU_NHAN_ID.TEN_NGAN_HANG
            self.TEN_TK_THU = tenTkThu
        else:
            self.TEN_TK_NHAN = tenTknhan
            self.TEN_TK_THU = tenTkThu

        self.TEN_TK_CHI = self.TAI_KHOAN_CHI_GUI_ID.get_Ten_Ngan_hang(self.TAI_KHOAN_CHI_GUI_ID)
    
    
    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_cong_no()
            record.ghi_so_thue()
        self.write({'state':'da_ghi_so'})
        
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
            tien_vnd = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1).id
            tk_nh = False
            tk_nh2 = False
            # ngân hàng thì lấy tk ngân hàng bên master còn quỹ thì lấy bên detail
            if self.TYPE_NH_Q == 'NGAN_HANG':
                if self.LOAI_PHIEU == 'PHIEU_THU':
                    tk_nh = self.TAI_KHOAN_NOP_ID.id
                    tk_nh2 = tk_nh
                elif self.LOAI_PHIEU == 'PHIEU_CHI':
                    tk_nh = self.TAI_KHOAN_CHI_GUI_ID.id
                    tk_nh2 = tk_nh
                elif self.LOAI_PHIEU == 'PHIEU_CHUYEN_TIEN':
                    # ghi nợ vào tài khoản đến ghi có vào tài khoản đi
                    tk_nh = self.TAI_KHOAN_DEN_ID.id
                    tk_nh2 = self.TAI_KHOAN_CHI_GUI_ID.id
            else:
                tk_nh = line.TK_NGAN_HANG_ID.id
                tk_nh2 = tk_nh

            if self.DOI_TUONG_ID:
                doi_tuong_id = self.DOI_TUONG_ID.id
                if self.PHUONG_THUC_TT =='UY_NHIEM_CHI':
                    if line.DOI_TUONG_ID:
                        doi_tuong_id = line.DOI_TUONG_ID.id
                    else:
                        doi_tuong_id = None
            else:
                doi_tuong_id = line.DOI_TUONG_ID.id
            
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI_DETAIL,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.SO_TIEN_QUY_DOI,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN if line.TK_NO_ID.CO_HACH_TOAN_NGOAI_TE == True else line.SO_TIEN_QUY_DOI,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
                'TAI_KHOAN_NGAN_HANG_ID' : tk_nh,
                'LOAI_HACH_TOAN' : '1',
                'DOI_TUONG_ID' : doi_tuong_id,
                'NGUOI_LIEN_HE' : self.NGUOI_NOP,
                'currency_id' : self.currency_id.id if line.TK_NO_ID.CO_HACH_TOAN_NGOAI_TE == True else tien_vnd,
                'TY_GIA' : self.TY_GIA if line.TK_NO_ID.CO_HACH_TOAN_NGOAI_TE == True else 1,
            })
            if self.LOAI_PHIEU == 'PHIEU_THU':
                data_ghi_no.update({
                    'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                })
            line_ids += [(0,0,data_ghi_no)]


            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN_QUY_DOI,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN if line.TK_CO_ID.CO_HACH_TOAN_NGOAI_TE == True else line.SO_TIEN_QUY_DOI,
                'LOAI_HACH_TOAN' : '2',
                'TAI_KHOAN_NGAN_HANG_ID' : tk_nh2,
                'currency_id' : self.currency_id.id if line.TK_CO_ID.CO_HACH_TOAN_NGOAI_TE == True else tien_vnd,
                'TY_GIA' : self.TY_GIA if line.TK_CO_ID.CO_HACH_TOAN_NGOAI_TE == True else 1,
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_cong_no(self):
        line_ids = []
        thu_tu = 0
        for line in self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
            data_goc = helper.Obj.inject(line, self)
            data_goc.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'DIEN_GIAI' : line.DIEN_GIAI_DETAIL,
                'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'SO_CHUNG_TU' : self.SO_CHUNG_TU,
                'DOI_TUONG_ID' : line.DOI_TUONG_ID.id if line.DOI_TUONG_ID else self.DOI_TUONG_ID.id,
                'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
            })
            if line.TK_NO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_no = data_goc.copy()
                data_ghi_no.update({
                    'TK_ID': line.TK_NO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_CO_ID.id,
                    'GHI_NO': line.SO_TIEN_QUY_DOI,
                    'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                    'GHI_CO': 0,
                    'GHI_CO_NGUYEN_TE' : 0,
                    'LOAI_HACH_TOAN' : '1',
                })
                line_ids += [(0,0,data_ghi_no)]
            if line.TK_CO_ID.CHI_TIET_THEO_DOI_TUONG == True:
                data_ghi_co = data_goc.copy()
                data_ghi_co.update({
                    'TK_ID': line.TK_CO_ID.id,
                    'TK_DOI_UNG_ID': line.TK_NO_ID.id,
                    'GHI_NO': 0,
                    'GHI_NO_NGUYEN_TE' : 0,
                    'GHI_CO': line.SO_TIEN_QUY_DOI,
                    'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
                    'LOAI_HACH_TOAN' : '2',
                })
                line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
            
        # Tạo master
        scn = self.env['so.cong.no'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CONG_NO_ID = scn.id
        return True

    def ghi_so_thue(self):
        line_ids = []
        thu_tu = 0
        if self.LOAI_PHIEU == 'PHIEU_CHI':
            for line in self.ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS:
                data = helper.Obj.inject(line, self)
                data.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                    'TK_VAT_ID': line.TK_THUE_GTGT_ID.id,
                    'PHAN_TRAM_VAT': line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT,
                    'SO_TIEN_VAT': line.TIEN_THUE_GTGT,
                    'DIEN_GIAI_CHUNG' : self.DIEN_GIAI_PC,
                    'SO_TIEN_CHIU_VAT' : line.GIA_TRI_HHDV_CHUA_THUE,
                    'DIEN_GIAI' : line.DIEN_GIAI_THUE if self.LOAI_CHUNG_TU != 1520 else '',
                    'SO_TIEN_VAT_NGUYEN_TE' : line.TIEN_THUE_GTGT,
                    'SO_TIEN_CHIU_VAT_NGUYEN_TE' : line.GIA_TRI_HHDV_CHUA_THUE,
                    'MUC_DICH_MUA_HANG_ID' : line.NHOM_HHDV_MUA_VAO.id,
                    'MA_SO_THUE_DOI_TUONG' : line.MA_SO_THUE_NCC,
                })
                if self.TYPE_NH_Q == 'NGAN_HANG':
                    data.update({
                        'DIEN_GIAI_CHUNG' : self.TEN_NOI_DUNG_TT,
                    })
                line_ids += [(0,0,data)]
                thu_tu += 1

        # Tạo master
        st = self.env['so.thue'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_THUE_ID = st.id
        return True
    
    # @api.multi
    # # def action_bo_ghi_so(self):
        # # self.bo_ghi_so()
    
    @api.onchange('currency_id')
    def update_TY_GIA(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False

    #vu cap nhat de len mau in phieu 
    def print_cap_nhat_de_in(self):
        if self.TEN_DOI_TUONG == False:
               self.TEN_DOI_TUONG = ''
        if self.NGUOI_NOP == False:
            self.NGUOI_NOP = ''
        
        if self.TEN_DOI_TUONG  == self.NGUOI_NOP:
            self.NOP_TIEN_MAU_IN= self.TEN_DOI_TUONG
        else:
            if self.NGUOI_NOP == '':
                self.NOP_TIEN_MAU_IN=  self.TEN_DOI_TUONG
            elif self.TEN_DOI_TUONG == '':
                self.NOP_TIEN_MAU_IN= self.NGUOI_NOP 
            else:
                self.NOP_TIEN_MAU_IN= self.NGUOI_NOP + " - " + self.TEN_DOI_TUONG


    
    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        for line in self.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
            line.tinh_tien_quy_doi()

    
    @api.multi
    def get_formview_id(self, access_uid=None):
        if self.TYPE_NH_Q == 'QUY':
            if self.LOAI_PHIEU == 'PHIEU_THU':
                return self.env.ref('account_ex.view_account_ex_phieu_thu_chi_form').id
            else:
                if self.LOAI_CHUNG_TU == 1025:
                    return self.env.ref('tien_luong.view_nop_tien_bao_hiem_form').id
                elif self.LOAI_CHUNG_TU == 1026:
                    return self.env.ref('tien_luong.view_tra_luong_nhan_vien_form').id
                else:
                    return self.env.ref('account_ex.view_account_ex_phieu_chi_chi_form').id
        else:
            if self.LOAI_PHIEU == 'PHIEU_THU':
                return self.env.ref('account_ex.view_nganhang_phieuthu_form').id
            else:
                if self.LOAI_CHUNG_TU == 1522:
                    return self.env.ref('tien_luong.view_nop_tien_bao_hiem_form').id
                elif self.LOAI_CHUNG_TU == 1523:
                    return self.env.ref('tien_luong.view_tra_luong_nhan_vien_form').id
                else:
                    return self.env.ref('account_ex.view_nganhang_phieuchi_form').id

        return super(ACCOUNT_EX_PHIEU_THU_CHI, self).get_formview_id(access_uid)

    @api.multi
    def get_menu_id(self):
        if self.TYPE_NH_Q == 'QUY':
            if self.LOAI_PHIEU == 'PHIEU_THU':
                return self.env.ref('menu.menu_account_ex_phieu_thu_chi').id
            else:
                return self.env.ref('menu.menu_account_ex_phieu_chi_chi').id
        else:
            if self.LOAI_PHIEU == 'PHIEU_THU':
                return self.env.ref('menu.menu_account_thu_tien').id
            else:
                return self.env.ref('menu.menu_account_chi_tien').id

        return super(ACCOUNT_EX_PHIEU_THU_CHI, self).get_menu_id()
        