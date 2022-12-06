# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from datetime import datetime
from odoo.exceptions import ValidationError

class BAO_CAO_BANG_KE_SO_DU_NGAN_HANG(models.Model):
    _name = 'bao.cao.bang.ke.so.du.ngan.hang'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('res.company', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    STT = fields.Char(string='Stt', help='Stt')
    TAI_KHOAN_NGAN_HANG = fields.Char(string='Tài khoản ngân hàng', help='Tài khoản ngân hàng')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    SO_DU_DAU_KY = fields.Float(string='Số dư đầu kỳ', help='Số dư đầu kỳ')
    PHAT_SINH_NO = fields.Float(string='Phát sinh nợ', help='Phát sinh nợ')
    PHAT_SINH_CO = fields.Float(string='Phát sinh có', help='Phát sinh có')
    SO_DU_CUOI_KY = fields.Float(string='Số dư cuối kỳ', help='Số dư cuối kỳ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        tn = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        dn = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        if(tn > dn):
            raise ValidationError('Từ ngày không được lớn hơn đến ngày!')
    #FIELD_IDS = fields.One2many('model.name')

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() else 'False'
        currency_id = params['currency_id'] if 'currency_id' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr



        # Bổ sung thông tin tài khoản
        param_tk = ''
        ds_tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        # for acc in ds_tai_khoan:
        if param_tk != '':
            param_tk += '\nOR '
        param_tk = """taikhoan.code LIKE '%s'""" % ds_tai_khoan.code
        # Bổ sung thông tin chi nhánh phụ thuộc
        param_pt = ''
        if BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC == 'True':
            param_pt ="""
            OR  socaichitiet.company_id IN
                    (
                        SELECT
                            id
                        FROM
                            public.res_company congtycon
                        WHERE
                            congtycon.parent_id = %s )
            """ % CHI_NHANH_ID

        query = """
        
        
        SELECT
    result."Tài khoản ngân hàng",
    result."Tên ngân hàng",
    SUM(result."Số dư đầu kỳ")                                                    AS "Số dư đầu kỳ",
    SUM(result."Phát sinh nợ")                                                    AS "Phát sinh nợ",
    SUM(result."Phát sinh có")                                                    AS "Phát sinh có",
    SUM(result."Số dư đầu kỳ") + SUM(result."Phát sinh nợ") - SUM(result."Phát sinh có") AS
    "Số dư cuối kỳ",
    result.company_id,
    result.company_currency_id
FROM
    (
        SELECT
            'không biết' "Tài khoản ngân hàng",
            taikhoan.name                                             AS "Tên ngân hàng",
            COALESCE(SUM(socaichitiet.debit-socaichitiet.credit),0.0) AS "Số dư đầu kỳ",
            0.0                                                       AS "Phát sinh nợ",
            0.0                                                       AS "Phát sinh có",
            socaichitiet.company_id,
            socaichitiet.company_currency_id
        FROM
            public.account_move_line socaichitiet
        LEFT JOIN
            public.account_move socai
        ON
            socai.id = socaichitiet.move_id
        LEFT JOIN
            public.account_account taikhoan
        ON
            taikhoan.id = socaichitiet.account_id
        WHERE
            socai.state = 'posted' -- đã ghi sổ
        AND ("""+ param_tk +""") -- chỉ lấy thông theo bên đối ứng
        AND (
                socaichitiet.company_id = %s -- id chi nhánh,công ty
            """+ param_pt +""") -- nếu tích chọn bao gồm số liệu các chi nhánh
            -- phụ thuộc
            -- (chi nhánh con,mặc định hiểu là công ty chỉ quản lý đến 2 cấp)
        AND socai.date < %s -- Ngày đầu kỳ
        AND socaichitiet.company_currency_id = 24 -- Đơn vị tiền tệ (Lưu ý: chỗ này không chắc chắn
            -- => kiểm
            -- tra lại xem nếu là loại tiền tệ khác VNĐ thì dữ liệu lưu thế nào, điều kiện tìm kiếm
            -- ra sao)
        GROUP BY
            taikhoan.name,
            socaichitiet.company_id,
            socaichitiet.company_currency_id
        UNION
        SELECT
            'không biết' "Tài khoản ngân hàng",
            taikhoan.name                          AS "Tên ngân hàng",
            0.0                                    AS "Số dư đầu kỳ",
            COALESCE(SUM(socaichitiet.debit),0.0)  AS "Phát sinh nợ",
            COALESCE(SUM(socaichitiet.credit),0.0) AS "Phát sinh có",
            socaichitiet.company_id,
            socaichitiet.company_currency_id
        FROM
            public.account_move_line socaichitiet
        LEFT JOIN
            public.account_move socai
        ON
            socai.id = socaichitiet.move_id
        LEFT JOIN
            public.account_account taikhoan
        ON
            taikhoan.id = socaichitiet.account_id
        WHERE
            socai.state = 'posted' -- đã ghi sổ
        AND ("""+ param_tk +""") -- chỉ lấy thông theo bên đối ứng
        AND (
                socaichitiet.company_id = %s -- id chi nhánh,công ty
            """+ param_pt +""") -- nếu tích chọn bao gồm số liệu các chi nhánh
            -- phụ thuộc
            -- (chi nhánh con,mặc định hiểu là công ty chỉ quản lý đến 2 cấp)
        AND socai.date BETWEEN %s AND %s -- Trong kỳ
        AND socaichitiet.company_currency_id = %s -- Đơn vị tiền tệ (Lưu ý: chỗ này không chắc chắn
            -- => kiểm
            -- tra lại xem nếu là loại tiền tệ khác VNĐ thì dữ liệu lưu thế nào, điều kiện tìm kiếm
            -- ra sao)
        GROUP BY
            taikhoan.name,
            socaichitiet.company_id,
            socaichitiet.company_currency_id) result
GROUP BY
    result."Tài khoản ngân hàng",
    result."Tên ngân hàng",
    result.company_id,
    result.company_currency_id
        """
        params = (CHI_NHANH_ID,DEN_NGAY,CHI_NHANH_ID,TU_NGAY,DEN_NGAY,currency_id)
        cr.execute(query,params)
        # Get and show result
        stt = 1
        for line in cr.dictfetchall():
            record.append({
                'STT': str(stt),
                'TAI_KHOAN_NGAN_HANG': '',
                'TEN_NGAN_HANG': line.get('Tên ngân hàng', ''),
                'SO_DU_DAU_KY': line.get('Số dư đầu kỳ', ''),
                'PHAT_SINH_NO': line.get('Phát sinh nợ', ''),
                'PHAT_SINH_CO': line.get('Phát sinh có', ''),
                'SO_DU_CUOI_KY': line.get('Số dư đầu kỳ', ''),
                'name': '',
                })
            stt += 1
        return record

    #@api.onchange('field_name')
    #def _cap_nhat(self):
    #    for item in self:
    #        item.FIELDS_IDS = self.env['model_name'].search([])

    @api.model
    def default_get(self, fields_list):
       result = super(BAO_CAO_BANG_KE_SO_DU_NGAN_HANG, self).default_get(fields_list)
       result['CHI_NHANH_ID'] = self.env['res.company'].search([], limit=1).id
       result['TAI_KHOAN_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','112%')], limit=1).id
       result['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')], limit=1).id
       return result
    ## END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        action = self.env.ref('bao_cao.open_report__bang_ke_so_du_ngan_hang').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action