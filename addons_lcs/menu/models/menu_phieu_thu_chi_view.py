# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import tools
from odoo import api, fields, models

class MENU_PHIEU_THU_CHI_VIEW(models.Model):
    _name = "menu.phieu.thu.chi.view"
    _description = "Phiếu thu chi"
    _auto = False
    _order = 'NGAY_CHUNG_TU desc'

    name = fields.Char(string='Số chứng từ', help='Số chứng từ', related='SO_CHUNG_TU')
    # DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    # NGUOI_NOP = fields.Char(string='Người nộp', help='Người nộp')
    # DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    LY_DO_NOP = fields.Selection([('10', 'Rút tiền gửi về nộp quỹ'), ('11', ' Thu hoàn thuế GTGT'), ('12', ' Thu hoàn ứng'), ('13', 'Thu khác'), ], string='Lý do nộp', help='Lý do nộp')
    # DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    # KEM_THEO_CHUNG_TU_GOC = fields.Char(string='Kèm theo chứng từ gốc', help='Kèm theo chứng từ gốc')
    # THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    # SO_CHUNG_TU_SO_QT = fields.Char(string='Số chứng từ (Sổ QT)', help='Số chứng từ (Sổ QT)')
    # currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    # TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    # NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên thu', help='Nhân viên thu')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    # company_id = fields.Many2one('res.company')
    # name = fields.Char(string='Name')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN_TREE = fields.Float(string='Số tiền', help='Tổng tiền')
    DIEN_GIAI_PC = fields.Text(string='Diễn giải', help='Diễn giải')
    TEN_NOI_DUNG_TT = fields.Text(string='Tên nội dung thanh toán',help='Tên nội dung thanh toán')
    NGAY_GHI_SO = fields.Date(string='Ngày ghi sổ quỹ', help='Ngày ghi sổ quỹ')
    LY_DO_THU_LIST = fields.Char(string='Loại chứng từ',help='Loại chứng từ')
    TEN_LY_DO_THU = fields.Text(string='Tên lý do thu',help='Tên lý do thu')

    # Mạnh mở coment loại chứng từ để làm view Trả lương cho nhân viên
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
   
    TYPE_NH_Q = fields.Selection([('NGAN_HANG', 'Ngân hàng'), ('QUY', 'QUY'), ], string='TYPE_NH_Q', help='TYPE_NH_Q')
    LOAI_PHIEU = fields.Selection([('PHIEU_THU','Phiếu thu'), ('PHIEU_CHI','Phiếu chi'), ('PHIEU_CHUYEN_TIEN','Phiếu chuyển tiền')])    
    ID_GOC = fields.Integer()
    MODEL_GOC = fields.Char()
    SOURCE_ID = fields.Reference(selection=[], string='Lập từ')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT
            CONCAT(a."MODEL_GOC", ',', a."ID_GOC") AS id,
            a."ID_GOC",
            a."MODEL_GOC",
            a."SOURCE_ID",
            a."LOAI_PHIEU",
            a."NGAY_CHUNG_TU",
            a."LY_DO_NOP",
            a."NGAY_HACH_TOAN",
            a."SO_CHUNG_TU",
            a."DIEN_GIAI",
            a."DIEN_GIAI"                          AS "DIEN_GIAI_PC",
            a."DIEN_GIAI"                          AS "TEN_NOI_DUNG_TT",
            a."DIEN_GIAI"                          AS "TEN_LY_DO_THU",
            a."SO_TIEN_TREE",
            a."TEN_DOI_TUONG",
            a."NGAY_GHI_SO",
            a."TYPE_NH_Q",
            a.create_date,
            a.state,
            a."LOAI_CHUNG_TU",
            a1."REFTYPENAME"                       AS "LY_DO_THU_LIST",
            a."CHI_NHANH_ID"
            FROM (SELECT
                    'account.ex.phieu.thu.chi' :: TEXT AS "MODEL_GOC",
                    pt.id                              AS "ID_GOC",
                    pt."SOURCE_ID",
                    pt."LOAI_PHIEU",
                    pt."NGAY_CHUNG_TU",
                    pt."LY_DO_NOP",
                    pt."NGAY_HACH_TOAN",
                    pt."SO_CHUNG_TU",
                    pt."DIEN_GIAI",
                    pt."SO_TIEN_TREE",
                    pt."TEN_DOI_TUONG",
                    pt."NGAY_GHI_SO",
                    pt."TYPE_NH_Q",
                    pt.create_date,
                    pt.state,
                    pt."LOAI_CHUNG_TU",
                    pt."CHI_NHANH_ID"
                FROM account_ex_phieu_thu_chi pt
                UNION ALL
                SELECT
                    'sale.document' :: TEXT      AS "MODEL_GOC",
                    ct.id                        AS "ID_GOC",
                    NULL :: VARCHAR(20)          AS "SOURCE_ID",
                    'PHIEU_THU' :: TEXT          AS "LOAI_PHIEU",
                    ct."NGAY_CHUNG_TU",
                    ct."DIEN_GIAI"               AS "LY_DO_NOP",
                    ct."NGAY_HACH_TOAN",
                    ct."SO_CHUNG_TU",
                    ct."DIEN_GIAI"               AS "LY_DO_THU_CHI",
                    ct."TONG_TIEN_THANH_TOAN_QĐ" AS "SO_TIEN_TREE",
                    ct."TEN_KHACH_HANG",
                    ct."NGAY_HACH_TOAN",
                    CASE WHEN ct."LOAI_THANH_TOAN" = 'TIEN_MAT'
                    THEN 'QUY'
                    ELSE 'NGAN_HANG'
                    END                          AS "TYPE_NH_Q",
                    ct.create_date,
                    ct.state,
                    ct."LOAI_CHUNG_TU",
                    ct."CHI_NHANH_ID"
                FROM sale_document ct
                WHERE "THU_TIEN_NGAY" = TRUE
                UNION ALL
                SELECT
                    'purchase.ex.tra.lai.hang.mua' :: TEXT AS "MODEL_GOC",
                    cttlhm.id                              AS "ID_GOC",
                    NULL :: VARCHAR(20)                    AS "SOURCE_ID",
                    'PHIEU_THU' :: TEXT                    AS "LOAI_PHIEU",
                    cttlhm."NGAY_CHUNG_TU",
                    cttlhm."LY_DO_NOP",
                    cttlhm."NGAY_HACH_TOAN",
                    cttlhm."SO_PHIEU_THU",
                    cttlhm."LY_DO_NOP",
                    cttlhm."TONG_TIEN_THANH_TOAN_QĐ"       AS "SO_TIEN_TREE",
                    cttlhm."TEN_NHA_CUNG_CAP",
                    cttlhm."NGAY_HACH_TOAN",
                    'QUY' :: TEXT                          AS "TYPE_NH_Q",
                    cttlhm.create_date,
                    cttlhm.state,
                    cttlhm."LOAI_CHUNG_TU",
                    cttlhm."CHI_NHANH_ID"
                FROM purchase_ex_tra_lai_hang_mua cttlhm
                WHERE cttlhm."selection_chung_tu_mua_hang" = 'thu_tien_mat'
                UNION ALL
                SELECT
                    'purchase.ex.giam.gia.hang.mua' :: TEXT AS "MODEL_GOC",
                    gghm.id                                 AS "ID_GOC",
                    NULL :: VARCHAR(20)                     AS "SOURCE_ID",
                    'PHIEU_THU' :: TEXT                     AS "LOAI_PHIEU",
                    gghm."NGAY_CHUNG_TU",
                    gghm."DIEN_GIAI",
                    gghm."NGAY_HACH_TOAN",
                    gghm."SO_PHIEU_THU",
                    gghm."DIEN_GIAI",
                    gghm."TONG_TIEN_THANH_TOAN_QD"          AS "SO_TIEN_TREE",
                    gghm."TEN_NHA_CUNG_CAP",
                    gghm."NGAY_HACH_TOAN",
                    'QUY' :: TEXT                           AS "TYPE_NH_Q",
                    gghm.create_date,
                    gghm.state,
                    gghm."LOAI_CHUNG_TU",
                    gghm."CHI_NHANH_ID"
                FROM purchase_ex_giam_gia_hang_mua gghm
                WHERE gghm."selection_chung_tu_giam_gia_hang_mua" = 'tra_lai_tien_mat'
                UNION ALL
                SELECT
                    'purchase.document' :: TEXT         AS "MODEL_GOC",
                    ctmh.id                             AS "ID_GOC",
                    NULL :: VARCHAR(20)                 AS "SOURCE_ID",
                    'PHIEU_CHI' :: TEXT                 AS "LOAI_PHIEU",
                    ctmh."NGAY_CHUNG_TU",
                    ctmh."DIEN_GIAI_CHUNG",
                    ctmh."NGAY_HACH_TOAN",
                    CASE WHEN ctmh."LOAI_THANH_TOAN" = 'tien_mat'
                    THEN "SO_PHIEU_CHI"
                    WHEN ctmh."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                    THEN "SO_UY_NHIEM_CHI"
                    WHEN ctmh."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                    THEN "SO_SEC_CHUYEN_KHOAN"
                    WHEN ctmh."LOAI_THANH_TOAN" = 'sec_tien_mat'
                    THEN "SO_SEC_TIEN_MAT"
                    ELSE '' END                            "SO_CHUNG_TU",
                    ctmh."DIEN_GIAI_CHUNG",
                    ctmh."TONG_TIEN_THANH_TOAN_QUY_DOI" AS "SO_TIEN_TREE",
                    ctmh."TEN_DOI_TUONG",
                    ctmh."NGAY_HACH_TOAN",
                    CASE WHEN ctmh."LOAI_THANH_TOAN" = 'tien_mat'
                    THEN 'QUY'
                    ELSE 'NGAN_HANG'
                    END                                 AS "TYPE_NH_Q",
                    ctmh.create_date,
                    ctmh.state,
                    ctmh."LOAI_CHUNG_TU",
                    ctmh."CHI_NHANH_ID"
                FROM purchase_document ctmh
                WHERE "DA_THANH_TOAN" = TRUE
                UNION ALL
                SELECT
                    'sale.ex.tra.lai.hang.ban' :: TEXT AS "MODEL_GOC",
                    tlhb.id                            AS "ID_GOC",
                    NULL :: VARCHAR(20)                AS "SOURCE_ID",
                    'PHIEU_CHI' :: TEXT                AS "LOAI_PHIEU",
                    tlhb."NGAY_CHUNG_TU",
                    tlhb."LY_DO_CHI",
                    tlhb."NGAY_HACH_TOAN",
                    tlhb."SO_CHUNG_TU_PHIEU_CHI",
                    tlhb."LY_DO_CHI",
                    tlhb."TONG_TIEN_THANH_TOAN_QĐ"     AS "SO_TIEN_TREE",
                    tlhb."TEN_KHACH_HANG",
                    tlhb."NGAY_HACH_TOAN",
                    'QUY' :: TEXT                      AS "TYPE_NH_Q",
                    tlhb.create_date,
                    tlhb.state,
                    tlhb."LOAI_CHUNG_TU",
                    tlhb."CHI_NHANH_ID"
                FROM sale_ex_tra_lai_hang_ban tlhb
                WHERE tlhb."selection_chung_tu_ban_hang" = 'tra_lai_tien_mat'
                UNION ALL
                SELECT
                    'sale.ex.giam.gia.hang.ban' :: TEXT AS "MODEL_GOC",
                    gghb.id                             AS "ID_GOC",
                    NULL :: VARCHAR(20)                 AS "SOURCE_ID",
                    'PHIEU_CHI' :: TEXT                 AS "LOAI_PHIEU",
                    gghb."NGAY_CHUNG_TU",
                    gghb."DIEN_GIAI",
                    gghb."NGAY_HACH_TOAN",
                    gghb."SO_PHIEU_CHI",
                    gghb."DIEN_GIAI",
                    gghb."TONG_TIEN_THANH_TOAN_QĐ"      AS "SO_TIEN_TREE",
                    gghb."TEN_KHACH_HANG",
                    gghb."NGAY_HACH_TOAN",
                    'QUY' :: TEXT                       AS "TYPE_NH_Q",
                    gghb.create_date,
                    gghb.state,
                    gghb."LOAI_CHUNG_TU",
                    gghb."CHI_NHANH_ID"
                FROM sale_ex_giam_gia_hang_ban gghb
                WHERE gghb."selection_chung_tu_giam_gia_hang_ban" = 'tra_lai_tien_mat'
                ) a
            LEFT JOIN danh_muc_reftype a1 ON a."LOAI_CHUNG_TU" = a1."REFTYPE"
            )""" % (self._table,))