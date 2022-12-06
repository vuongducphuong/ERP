# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_CONG_NO_NHAN_VIEN(models.Model):
    _name = 'bao.cao.tong.hop.cong.no.nhan.vien'
   
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHONG_CHON', 'Không chọn'), ('CONG_TRINH', 'Công trình'), ('HOP_DONG', 'Hợp đồng'), ], string='Thống kê theo', help='Thống kê theo' , default ='KHONG_CHON', required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc ', help='Bao gồm số liệu chi nhánh phụ thuộc ', default ='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày ',required=True ,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản' ,required=True )
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    HOP_DONG_DU_AN = fields.Char(string='Hợp đồng dự án', help='Hợp đồng dự án')
    TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')
    TK_CONG_NO = fields.Char(string='TK công nợ', help='Tài khoản công nợ')
    NO_DAU_KY = fields.Float(string='Nợ đầu kỳ', help='Nợ đầu kỳ',digits= decimal_precision.get_precision('VND'))
    CO_DAU_KY = fields.Float(string='Có đầu kỳ', help='Có đầu kỳ',digits= decimal_precision.get_precision('VND'))
    PHAT_SINH_NO = fields.Float(string='Phát sinh nợ', help='Phát sinh nợ',digits= decimal_precision.get_precision('VND'))
    PHAT_SINH_CO = fields.Float(string='Phát sinh có', help='Phát sinh có',digits= decimal_precision.get_precision('VND'))
    NO_CUOI_KY = fields.Float(string='Nợ cuối kỳ', help='Nợ cuối kỳ',digits= decimal_precision.get_precision('VND'))
    CO_CUOI_KY = fields.Float(string='Có cuối kỳ', help='Có cuối kỳ',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    HOP_DONG_DU_AN_SELECTION = fields.Selection([
        ('HOP_DONG', 'Hợp đồng'), 
        ('DU_AN', 'Dự án') 
        ],default='HOP_DONG', string='NO_SAVE')


    NHAN_VIEN_IDS = fields.One2many('res.partner')
    CHON_TAT_CA_NHAN_VIEN = fields.Boolean('Tất cả nhân viên', default=True)
    NHAN_VIEN_MANY_IDS = fields.Many2many('res.partner','tong_hop_cong_no_nv_res_partner', domain=[('LA_NHAN_VIEN', '=', True)], string='Chọn nhân viên')

    CONG_TRINH_IDS= fields.One2many('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_cong_no_nv_danh_muc_cong_trinh', string='Chọn công trình') 

    HOP_DONG_IDS= fields.One2many('sale.ex.hop.dong.ban')
    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','tong_hop_cong_no_hdbh', string='Chọn hợp đồng') 


    #vũ thêm
    HOP_DONG_MUA_IDS= fields.One2many('purchase.ex.hop.dong.mua.hang')
    CHON_TAT_CA_HOP_DONG_MUA = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MUA_MANY_IDS = fields.Many2many('purchase.ex.hop.dong.mua.hang','tong_hop_cong_no_hdmh', string='Chọn hợp đồng') 

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):

        self.CHON_TAT_CA_NHAN_VIEN = True
        self.CHON_TAT_CA_HOP_DONG = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.CHON_TAT_CA_HOP_DONG_MUA = True
        self.CONG_TRINH_MANY_IDS = []
        self.NHAN_VIEN_MANY_IDS = []
        self.HOP_DONG_MANY_IDS = []
        self.HOP_DONG_MUA_MANY_IDS = []
    
    # Nhân viên
    @api.onchange('NHAN_VIEN_IDS')
    def update_NHAN_VIEN_IDS(self):
        self.NHAN_VIEN_MANY_IDS =self.NHAN_VIEN_IDS.ids
        
    @api.onchange('NHAN_VIEN_MANY_IDS')
    def _onchange_NHAN_VIEN_MANY_IDS(self):
        self.NHAN_VIEN_IDS = self.NHAN_VIEN_MANY_IDS.ids

    # Công trình
    @api.onchange('CONG_TRINH_IDS')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.CONG_TRINH_IDS.ids
        
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.CONG_TRINH_IDS = self.CONG_TRINH_MANY_IDS.ids
    
    # Hợp đồng bán
    @api.onchange('HOP_DONG_IDS')
    def update_HOP_DONG_IDS(self):
        self.HOP_DONG_MANY_IDS =self.HOP_DONG_IDS.ids
        
    @api.onchange('HOP_DONG_MANY_IDS')
    def _onchange_HOP_DONG_MANY_IDS(self):
        self.HOP_DONG_IDS = self.HOP_DONG_MANY_IDS.ids
    
    # Hợp đồng mua
    @api.onchange('HOP_DONG_MUA_IDS')
    def update_HOP_DONG_MUA_IDS(self):
        self.HOP_DONG_MUA_MANY_IDS =self.HOP_DONG_MUA_IDS.ids
        
    @api.onchange('HOP_DONG_MUA_MANY_IDS')
    def _onchange_HOP_DONG_MUA_MANY_IDS(self):
        self.HOP_DONG_MUA_IDS = self.HOP_DONG_MUA_MANY_IDS.ids

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')
    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_TONG_HOP_CONG_NO_NHAN_VIEN, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_DOI_TUONG', '=', 'True'),('DOI_TUONG_SELECTION', '=', '2')],limit=1)
        if tai_khoan:
            result['TAI_KHOAN_ID'] = tai_khoan.id
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_NHAN_VIEN = params['CHON_TAT_CA_NHAN_VIEN'] if 'CHON_TAT_CA_NHAN_VIEN' in params.keys() else 'False'
        CHON_TAT_CA_HOP_DONG = params['CHON_TAT_CA_HOP_DONG'] if 'CHON_TAT_CA_HOP_DONG' in params.keys() else 'False'
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CHON_TAT_CA_HOP_DONG_MUA = params['CHON_TAT_CA_HOP_DONG_MUA'] if 'CHON_TAT_CA_HOP_DONG_MUA' in params.keys() else 'False'
        
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        NHAN_VIEN_MANY_IDS = params['NHAN_VIEN_MANY_IDS'] if 'NHAN_VIEN_MANY_IDS' in params.keys() else 'False'
        HOP_DONG_MANY_IDS = params['HOP_DONG_MANY_IDS'] if 'HOP_DONG_MANY_IDS' in params.keys() else 'False'
        HOP_DONG_MUA_MANY_IDS = params['HOP_DONG_MUA_MANY_IDS'] if 'HOP_DONG_MUA_MANY_IDS' in params.keys() else 'False'
        
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')


        if THONG_KE_THEO in ('KHONG_CHON','CONG_TRINH','HOP_DONG'):
            if CHON_TAT_CA_NHAN_VIEN == 'False':
                if NHAN_VIEN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Nhân viên>. Xin vui lòng chọn lại.')

        # Thống kê theo công trình
        if THONG_KE_THEO == 'CONG_TRINH':
            if CHON_TAT_CA_CONG_TRINH == 'False':
                if CONG_TRINH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')

        # Thống kê theo hợp đồng
      
        if THONG_KE_THEO == 'HOP_DONG':
            if CHON_TAT_CA_HOP_DONG == 'False':
                if HOP_DONG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hợp đồng/Dự án>. Xin vui lòng chọn lại.')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        if TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN


        TU = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
       
        if params.get('CHON_TAT_CA_NHAN_VIEN'):
            domain = [('LA_NHAN_VIEN','=', True)]
            NHAN_VIEN_IDS =  self.env['res.partner'].search(domain).ids
        else:
            NHAN_VIEN_IDS =  params.get('NHAN_VIEN_MANY_IDS')
        
        if params.get('CHON_TAT_CA_CONG_TRINH'):
            domain = []
            CONG_TRINH_IDS = self.env['danh.muc.cong.trinh'].search(domain).ids
        else:
            CONG_TRINH_IDS = params.get('CONG_TRINH_MANY_IDS')

        if params.get('CHON_TAT_CA_HOP_DONG'):
            domain = []
            HOP_DONG_IDS = self.env['sale.ex.hop.dong.ban'].search(domain).ids
        else:
            HOP_DONG_IDS = params.get('HOP_DONG_MANY_IDS')
        
        if params.get('CHON_TAT_CA_HOP_DONG_MUA'):
            domain = []
            HOP_DONG_MUA_IDS = self.env['purchase.ex.hop.dong.mua.hang'].search(domain).ids
        else:
            HOP_DONG_MUA_IDS = params.get('HOP_DONG_MUA_MANY_IDS')

        params_sql = {
               'TU_NGAY':TU_NGAY_F, 
               'DEN_NGAY':DEN_NGAY_F, 
               'NHAN_VIENIDS' : NHAN_VIEN_IDS or None,
               'CHI_NHANH_ID' : CHI_NHANH_ID,
               'HOP_DONGIDS' : HOP_DONG_IDS or None,
               'HOP_DONG_MUA_IDS' : HOP_DONG_MUA_IDS or None,
               'TAI_KHOAN_ID' : TAI_KHOAN_ID,
               'CONG_TRINHIDS' : CONG_TRINH_IDS or None,
               'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
               'limit': limit,
               'offset': offset,
               }

        # Thống kê theo không chọn
        if THONG_KE_THEO=='KHONG_CHON':
            return self._lay_bao_cao_thong_ke_theo_khong_chon(params_sql)
        # Thống kê theo công trình
        elif THONG_KE_THEO=='CONG_TRINH':
            return self._lay_bao_cao_thong_ke_theo_cong_trinh(params_sql)
        # Thống kê theo hợp đồng
        elif THONG_KE_THEO=='HOP_DONG':
            return self._lay_bao_cao_thong_ke_theo_hop_dong(params_sql)

    def _lay_bao_cao_thong_ke_theo_khong_chon(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_NHAN_VIEN --không chọn
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

    

    den_ngay                            DATE := %(DEN_NGAY)s;
   

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

   

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

   


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

   


   

    rec                                 RECORD;

    v_BalanseSide                     VARCHAR(127);

BEGIN

     SELECT  "TINH_CHAT" INTO v_BalanseSide
        FROM    danh_muc_he_thong_tai_khoan
        WHERE   "SO_TAI_KHOAN" = so_tai_khoan ;




    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT
                A."id" AS "NHAN_VIEN_ID"
                FROM    res_partner A

                WHERE   A."LA_NHAN_VIEN" = '1' AND  (id = any (%(NHAN_VIENIDS)s)

                        OR ( %(NHAN_VIENIDS)s IS NULL )) ;



    DROP TABLE IF EXISTS TMP_TAI_KHOAN
		;

		IF so_tai_khoan IS NOT NULL
		THEN
			CREATE TEMP TABLE TMP_TAI_KHOAN
				AS
					SELECT
						A."SO_TAI_KHOAN"
						, A."TEN_TAI_KHOAN"
						, A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
						, A."TINH_CHAT"
					FROM danh_muc_he_thong_tai_khoan AS A
					WHERE "SO_TAI_KHOAN" = so_tai_khoan
					ORDER BY A."SO_TAI_KHOAN",
						A."TEN_TAI_KHOAN"
			;

		ELSE
			CREATE TEMP TABLE TMP_TAI_KHOAN
				AS
					SELECT
						A."SO_TAI_KHOAN"
						, A."TEN_TAI_KHOAN"
						, A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
						, A."TINH_CHAT"
					FROM danh_muc_he_thong_tai_khoan AS A
					WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
						  AND "DOI_TUONG_SELECTION" = '2'
						  AND "LA_TK_TONG_HOP" = '0'
					ORDER BY A."SO_TAI_KHOAN",
						A."TEN_TAI_KHOAN"
			;
		END IF
		;


		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
			AS
				SELECT
				ROW_NUMBER() OVER ( ORDER BY "MA_NHAN_VIEN" ) AS RowNum ,
					"NHAN_VIEN_ID"
					,"MA_NHAN_VIEN",  -- Mã NV


					"TEN_NHAN_VIEN" , -- Tên NV
					"SO_TAI_KHOAN",
					"TEN_TAI_KHOAN",
					CASE WHEN "GHI_NO_DAU_KY" > 0 THEN "GHI_NO_DAU_KY" ELSE 0 END AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
					CASE WHEN "GHI_NO_DAU_KY" < 0 THEN -"GHI_NO_DAU_KY" ELSE 0 END As "GHI_CO_DAU_KY" , -- Dư Có Đầu kỳ quy đổi
					"GHI_NO" AS "GHI_NO" , -- Phát sinh nợ quy đổi
					"GHI_CO" AS "GHI_CO" , -- Phát sinh có quy đổi
					/* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
					Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ
					Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
					CASE WHEN "GHI_NO_DAU_KY" + "GHI_NO" - "GHI_CO" > 0
						 THEN "GHI_NO_DAU_KY" + "GHI_NO" - "GHI_CO"
						 ELSE 0
					END AS "DU_NO_CUOI_KY" ,
					CASE WHEN - "GHI_NO_DAU_KY" - "GHI_NO" + "GHI_CO" > 0
						 THEN - "GHI_NO_DAU_KY" - "GHI_NO" + "GHI_CO"
						 ELSE 0
					END AS "DU_CO_CUOI_KY"
			FROM    ( SELECT
								LEID."NHAN_VIEN_ID"
								,AO."MA_NHAN_VIEN" , -- Mã NV
								AO."HO_VA_TEN" AS "TEN_NHAN_VIEN" , -- Tên NV
								TBAN."SO_TAI_KHOAN" AS "SO_TAI_KHOAN" , -- TK công nợ
								TBAN."TEN_TAI_KHOAN" ,
								SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay  THEN AOL."GHI_NO" - AOL."GHI_CO" Else 0 end) AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
								SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_NO" END) AS "GHI_NO" , -- Phát sinh nợ quy đổi
								SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_CO" END) AS "GHI_CO"
					  FROM      so_cong_no_chi_tiet AS AOL
								INNER JOIN DS_NHAN_VIEN LEID ON AOL."DOI_TUONG_ID" = LEID."NHAN_VIEN_ID"
								INNER JOIN res_partner AO ON AO.id = LEID."NHAN_VIEN_ID"
								INNER JOIN TMP_LIST_BRAND BIDL ON AOL."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
								INNER JOIN TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE TBAN."AccountNumberPercent"
					  WHERE     AOL."NGAY_HACH_TOAN" <= den_ngay


					  GROUP BY
								LEID."NHAN_VIEN_ID"
								,AO."MA_NHAN_VIEN" , -- Mã NV
								AO."HO_VA_TEN",
								TBAN."SO_TAI_KHOAN",
								TBAN."TEN_TAI_KHOAN"
					) AS RSNS
			WHERE   RSNS."GHI_NO" <> 0
				   OR RSNS."GHI_CO" <> 0
				   OR "GHI_NO_DAU_KY" <> 0

			ORDER BY
					"MA_NHAN_VIEN",  -- Mã NV
					 "TEN_NHAN_VIEN" , -- Tên NV
					 "SO_TAI_KHOAN",
					 "TEN_TAI_KHOAN"
		;


	END $$
	;

SELECT 
    "MA_NHAN_VIEN" as "MA_NHAN_VIEN",
    "TEN_NHAN_VIEN" as "TEN_NHAN_VIEN",
    "SO_TAI_KHOAN" as "TK_CONG_NO",
    "GHI_NO_DAU_KY" as "NO_DAU_KY",
    "GHI_CO_DAU_KY" as "CO_DAU_KY",
    "GHI_NO" as "PHAT_SINH_NO",
    "GHI_CO" as "PHAT_SINH_CO",
    "DU_NO_CUOI_KY" as "NO_CUOI_KY",
    "DU_CO_CUOI_KY" as "CO_CUOI_KY"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s;

        """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_thong_ke_theo_cong_trinh(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_NHAN_VIEN 
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

   

    den_ngay                            DATE := %(DEN_NGAY)s;

    

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

   

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

  

    rec                                 RECORD;

    v_BalanseSide                       VARCHAR(127);

BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;

    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;
     CREATE TEMP TABLE TMP_TAI_KHOAN
         (
              "SO_TAI_KHOAN" VARCHAR(100) ,
              "AccountNumberPercent" VARCHAR(100)
            );


    IF so_tai_khoan IS NOT NULL
    THEN
       INSERT INTO TMP_TAI_KHOAN
                SELECT
                    so_tai_khoan
                  , so_tai_khoan || '%%' AS "AccountNumberPercent"
        ;

    ELSE
         INSERT INTO TMP_TAI_KHOAN
                SELECT
                    A."SO_TAI_KHOAN"
                    , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                FROM danh_muc_he_thong_tai_khoan AS A
                WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                      AND "DOI_TUONG_SELECTION" = '2'
                      AND "LA_TK_TONG_HOP" = '0'

        ;
    END IF
    ;

    DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT *
            FROM res_partner

            WHERE (id = any (%(NHAN_VIENIDS)s))

    ;

    DROP TABLE IF EXISTS TMP_CONG_TRINH
    ;

    CREATE TEMP TABLE TMP_CONG_TRINH
        AS
            SELECT DISTINCT
                PW."id" AS "CONG_TRINH_ID"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"
            FROM danh_muc_cong_trinh PW

            WHERE (id = any (%(CONG_TRINHIDS)s))

    ;

    DROP TABLE IF EXISTS TMP_CONG_TRINH_CHILDREN
    ;

    CREATE TEMP TABLE TMP_CONG_TRINH_CHILDREN
        AS
            SELECT DISTINCT
                PW."id" AS "CONG_TRINH_ID"
                , PW."MA_PHAN_CAP"
            FROM TMP_CONG_TRINH SPW
                INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE SPW."MA_PHAN_CAP" || '%%'

    ;

    DROP TABLE IF EXISTS DS_CONG_TRINH
    ;

    CREATE TEMP TABLE DS_CONG_TRINH
        AS
            SELECT
                T."CONG_TRINH_ID" AS "CONG_TRINH_CHILD_ID"
                , PW."CONG_TRINH_ID"
                , PW."MA_CONG_TRINH"
                , Pw."TEN_CONG_TRINH"
            FROM TMP_CONG_TRINH_CHILDREN T

                LEFT JOIN LATERAL (
                    SELECT
                        SPW."CONG_TRINH_ID",
                        SPW."MA_CONG_TRINH",
                        SPW."TEN_CONG_TRINH"
                    FROM TMP_CONG_TRINH SPW
                    WHERE T."MA_PHAN_CAP" LIKE SPW."MA_PHAN_CAP"   || '%%'
                        ORDER BY SPW."MA_PHAN_CAP" DESC
                         FETCH FIRST 1 ROW ONLY
    ) PW ON TRUE

    ;



    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS
            SELECT
                ROW_NUMBER() OVER ( ORDER BY  "MA_NHAN_VIEN","MA_CONG_TRINH","TEN_CONG_TRINH","SO_TAI_KHOAN" ) AS RowNum
				,"NHAN_VIEN_ID"   As "NHAN_VIEN_ID"
                ,"MA_NHAN_VIEN"  -- Mã NV
                ,"TEN_NHAN_VIEN"  -- Tên NV
                ,"CONG_TRINH_ID"
                ,"MA_CONG_TRINH"
                ,"TEN_CONG_TRINH"
                ,"SO_TAI_KHOAN"
                ,CASE WHEN "GHI_NO_DAU_KY" > 0 THEN "GHI_NO_DAU_KY" ELSE 0 END AS "GHI_NO_DAU_KY"  -- Dư nợ Đầu kỳ quy đổi
                ,CASE WHEN "GHI_NO_DAU_KY" < 0 THEN -"GHI_NO_DAU_KY" ELSE 0 END As "GHI_CO_DAU_KY"  -- Dư Có Đầu kỳ quy đổi
                ,"GHI_NO" AS "GHI_NO"  -- Phát sinh nợ quy đổi
                ,"GHI_CO" AS "GHI_CO"  -- Phát sinh có quy đổi
                ,CASE WHEN "GHI_NO_DAU_KY" + "GHI_NO" - "GHI_CO" > 0
                     THEN "GHI_NO_DAU_KY" + "GHI_NO" - "GHI_CO"
                     ELSE 0
                END AS "DU_NO_CUOI_KY"
                ,CASE WHEN - "GHI_NO_DAU_KY" - "GHI_NO" + "GHI_CO" > 0
                     THEN - "GHI_NO_DAU_KY" - "GHI_NO" + "GHI_CO"
                     ELSE 0
                END AS "DU_CO_CUOI_KY"
        FROM    (
					-- Lấy lên công nợ nhân viên theo hợp đồng bán
					SELECT
							A."SO_TAI_KHOAN"
							,E."id" AS "NHAN_VIEN_ID"
							,AOL."MA_DOI_TUONG" AS "MA_NHAN_VIEN"  -- Mã NV
                            ,AOL."TEN_DOI_TUONG" AS "TEN_NHAN_VIEN"  -- Tên NV
                            ,PW."CONG_TRINH_ID" AS "CONG_TRINH_ID"
                            ,PW."MA_CONG_TRINH"
							,PW."TEN_CONG_TRINH"
                            ,SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay  THEN AOL."GHI_NO" - AOL."GHI_CO" Else 0 end) AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
                            SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_NO" END) AS "GHI_NO" , -- Phát sinh nợ quy đổi
                            SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_CO" END) AS "GHI_CO"
                  FROM      so_cong_no_chi_tiet AS AOL
                            INNER JOIN DS_NHAN_VIEN E ON AOL."DOI_TUONG_ID" = E."id"
                            INNER JOIN TMP_LIST_BRAND B ON AOL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            INNER JOIN TMP_TAI_KHOAN A ON AOL."MA_TK" LIKE A."AccountNumberPercent"
                            INNER JOIN DS_CONG_TRINH PW ON AOL."CONG_TRINH_ID" = PW."CONG_TRINH_ID"
                  WHERE     AOL."NGAY_HACH_TOAN" <= den_ngay


                  GROUP BY
							A."SO_TAI_KHOAN"
							,E."id"
							,AOL."MA_DOI_TUONG"
                            ,AOL."TEN_DOI_TUONG"
                             ,PW."CONG_TRINH_ID"
                            ,PW."MA_CONG_TRINH"
							,PW."TEN_CONG_TRINH"

                ) AS RSNS
        WHERE   RSNS."GHI_NO" <> 0
               OR RSNS."GHI_CO" <> 0
               OR "GHI_NO_DAU_KY" <> 0
    ;


END $$
;

SELECT 
    "TEN_NHAN_VIEN" as "TEN_NHAN_VIEN",
    "TEN_CONG_TRINH" as "TEN_CONG_TRINH",
    "SO_TAI_KHOAN" as "TK_CONG_NO",
    "GHI_NO_DAU_KY" as "NO_DAU_KY",
    "GHI_CO_DAU_KY" as "CO_DAU_KY",
    "GHI_NO" as "PHAT_SINH_NO",
    "GHI_CO" as "PHAT_SINH_CO",
    "DU_NO_CUOI_KY" as "NO_CUOI_KY",
    "DU_CO_CUOI_KY" as "CO_CUOI_KY"
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s;

        """
        return self.execute(query,params_sql)

    def _lay_bao_cao_thong_ke_theo_hop_dong(self, params_sql):      
        record = []
        query ="""
        --BAO_CAO_TONG_HOP_CONG_NO_NHAN_VIEN --hợp đồng
DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             DATE := %(TU_NGAY)s;

   

    den_ngay                            DATE := %(DEN_NGAY)s;

    

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

   

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    


    so_tai_khoan                        VARCHAR(127) := %(TAI_KHOAN_ID)s;

    



    rec                                 RECORD;

    v_BalanseSide                       INTEGER;

BEGIN






    DROP TABLE IF EXISTS TMP_HOP_DONG_DU_AN
    ;

    CREATE TEMP TABLE TMP_HOP_DONG_DU_AN
        AS
            SELECT
                C.id AS "HOP_DONG_ID"
                , C."SO_HOP_DONG"
                , C."TRICH_YEU"
                , C."THUOC_DU_AN_ID"
                , C."HOP_DONG_DU_AN_SELECTION"
            FROM sale_ex_hop_dong_ban C

            WHERE (id = any (%(HOP_DONGIDS)s))

    ;


    DROP TABLE IF EXISTS TMP_HOP_DONG
    ;

    CREATE TEMP TABLE TMP_HOP_DONG
        AS

            SELECT DISTINCT

                 C."HOP_DONG_ID"
                , C."HOP_DONG_ID_OUT"
                , C."SO_HOP_DONG"
                , C."TRICH_YEU"
            FROM
                (
                    SELECT
                        P."HOP_DONG_ID"
                        , P."HOP_DONG_ID" AS "HOP_DONG_ID_OUT"
                        , P."SO_HOP_DONG"
                        , P."TRICH_YEU"
                    FROM TMP_HOP_DONG_DU_AN P
                          WHERE "HOP_DONG_DU_AN_SELECTION" ='DU_AN'
                          UNION ALL
                          SELECT DISTINCT
                    COALESCE ( C."id", P."HOP_DONG_ID"),
                    P."HOP_DONG_ID",
                    P."SO_HOP_DONG",
                    P."TRICH_YEU"
                     FROM TMP_HOP_DONG_DU_AN P
                     LEFT JOIN sale_ex_hop_dong_ban C ON C."THUOC_DU_AN_ID" = P."HOP_DONG_ID"
                    GROUP BY COALESCE ( C."id", P."HOP_DONG_ID"),
                    P."HOP_DONG_ID",
                    P."SO_HOP_DONG",
                    P."TRICH_YEU"
                ) C
    ;

    DROP TABLE IF EXISTS TMP_PU_HOP_DONG
    ;

    CREATE TEMP TABLE TMP_PU_HOP_DONG
        AS
            SELECT
                C."id" AS "HOP_DONG_MUA_ID" ,
				C."SO_HOP_DONG" ,
				C."TRICH_YEU"
		        FROM    purchase_ex_hop_dong_mua_hang C
                 WHERE (id = any (%(HOP_DONG_MUA_IDS)s))

;



    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

    CREATE TEMP TABLE TMP_TAI_KHOAN
    (
        "SO_TAI_KHOAN"         VARCHAR(100),
        "AccountNumberPercent" VARCHAR(100)
    )
    ;


    IF so_tai_khoan IS NOT NULL
    THEN
        INSERT INTO TMP_TAI_KHOAN
            SELECT
                so_tai_khoan
                , so_tai_khoan || '%%' AS "AccountNumberPercent"
        ;

    ELSE
        INSERT INTO TMP_TAI_KHOAN
            SELECT
                A."SO_TAI_KHOAN"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND "DOI_TUONG_SELECTION" = '2'
                  AND "LA_TK_TONG_HOP" = '0'

        ;
    END IF
    ;

     DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;

     DROP TABLE IF EXISTS DS_NHAN_VIEN
    ;

    CREATE TEMP TABLE DS_NHAN_VIEN
        AS
            SELECT

             "id" as "NHAN_VIEN_ID"
            FROM res_partner

            WHERE (id = any (%(NHAN_VIENIDS)s))

    ;






    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS
            SELECT  ROW_NUMBER() OVER ( ORDER BY "SO_TAI_KHOAN", "MA_NHAN_VIEN","SO_HOP_DONG" ) AS RowNum
				,"SO_TAI_KHOAN"
				,"NHAN_VIEN_ID"   As "NHAN_VIEN_ID"
                ,"MA_NHAN_VIEN"  -- Mã NV
                ,"TEN_NHAN_VIEN"  -- Tên NV
                ,"HOP_DONG_ID"
                ,"SO_HOP_DONG"
                ,"TRICH_YEU"
                ,CASE WHEN "GHI_NO_DAU_KY" > 0 THEN "GHI_NO_DAU_KY" ELSE 0 END AS "GHI_NO_DAU_KY"  -- Dư nợ Đầu kỳ quy đổi
                ,CASE WHEN "GHI_NO_DAU_KY" < 0 THEN -"GHI_NO_DAU_KY" ELSE 0 END As "GHI_CO_DAU_KY"  -- Dư Có Đầu kỳ quy đổi
                ,"GHI_NO" AS "GHI_NO"  -- Phát sinh nợ quy đổi
                ,"GHI_CO" AS "GHI_CO"  -- Phát sinh có quy đổi
                ,CASE WHEN "GHI_NO_DAU_KY" + "GHI_NO" - "GHI_CO" > 0
                     THEN "GHI_NO_DAU_KY" + "GHI_NO" - "GHI_CO"
                     ELSE 0
                END AS "DU_NO_CUOI_KY"
                ,CASE WHEN - "GHI_NO_DAU_KY" - "GHI_NO" + "GHI_CO" > 0
                     THEN - "GHI_NO_DAU_KY" - "GHI_NO" + "GHI_CO"
                     ELSE 0
                END AS "DU_CO_CUOI_KY"
        FROM    (
					-- Lấy lên công nợ nhân viên theo hợp đồng bán
					SELECT
							A."SO_TAI_KHOAN"
							,E."NHAN_VIEN_ID"
							,AOL."MA_DOI_TUONG" AS "MA_NHAN_VIEN"  -- Mã NV
                            ,AOL."TEN_DOI_TUONG" AS "TEN_NHAN_VIEN"  -- Tên NV
                            ,C."HOP_DONG_ID_OUT" AS "HOP_DONG_ID"
                            ,C."SO_HOP_DONG"
                            ,C."TRICH_YEU"
                            ,SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay  THEN AOL."GHI_NO" - AOL."GHI_CO" Else 0 end) AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
                            SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_NO" END) AS "GHI_NO" , -- Phát sinh nợ quy đổi
                            SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_CO" END) AS "GHI_CO"
                  FROM      so_cong_no_chi_tiet AS AOL
                            INNER JOIN DS_NHAN_VIEN E ON AOL."DOI_TUONG_ID" = E."NHAN_VIEN_ID"
                            INNER JOIN TMP_LIST_BRAND B ON AOL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            INNER JOIN TMP_TAI_KHOAN A ON AOL."MA_TK" LIKE A."AccountNumberPercent"
                            INNER JOIN TMP_HOP_DONG C ON C."HOP_DONG_ID" = AOL."HOP_DONG_BAN_ID"
                  WHERE     AOL."NGAY_HACH_TOAN" <= den_ngay


                  GROUP BY
							A."SO_TAI_KHOAN"
							,E."NHAN_VIEN_ID"
							,AOL."MA_DOI_TUONG"
                            ,AOL."TEN_DOI_TUONG"
                            ,C."HOP_DONG_ID_OUT"
                            ,C."SO_HOP_DONG"
                            ,C."TRICH_YEU"
                 UNION ALL   --Lấy lên công nợ nhân viên theo hợp đồng mua
                 SELECT
							A."SO_TAI_KHOAN"
							,E."NHAN_VIEN_ID"
							,AOL."MA_DOI_TUONG" AS "MA_NHAN_VIEN"  -- Mã NV
                            ,AOL."TEN_DOI_TUONG" AS "TEN_NHAN_VIEN"  -- Tên NV
                            ,C."HOP_DONG_MUA_ID"
                            ,C."SO_HOP_DONG"
                            ,C."TRICH_YEU"
                            ,SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay  THEN AOL."GHI_NO" - AOL."GHI_CO" Else 0 end) AS "GHI_NO_DAU_KY" , -- Dư nợ Đầu kỳ quy đổi
                            SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_NO" END) AS "GHI_NO" , -- Phát sinh nợ quy đổi
                            SUM(CASE WHEN AOL."NGAY_HACH_TOAN" < tu_ngay THEN 0 ELSE AOL."GHI_CO" END) AS "GHI_CO"
                  FROM      so_cong_no_chi_tiet AS AOL
                            INNER JOIN DS_NHAN_VIEN  E ON AOL."DOI_TUONG_ID" = E."NHAN_VIEN_ID"
                            INNER JOIN TMP_LIST_BRAND B ON AOL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            INNER JOIN TMP_TAI_KHOAN A ON AOL."MA_TK" LIKE A."AccountNumberPercent"
                            INNER JOIN TMP_PU_HOP_DONG C ON C."HOP_DONG_MUA_ID" = AOL."HOP_DONG_MUA_ID"
                  WHERE     AOL."NGAY_HACH_TOAN" <= den_ngay


                  GROUP BY
							A."SO_TAI_KHOAN"
							,E."NHAN_VIEN_ID"
							,AOL."MA_DOI_TUONG"
                            ,AOL."TEN_DOI_TUONG"
                            ,C."HOP_DONG_MUA_ID"
                            ,C."SO_HOP_DONG"
                            ,C."TRICH_YEU"
                ) AS RSNS
        WHERE   RSNS."GHI_NO" <> 0
               OR RSNS."GHI_CO" <> 0
               OR "GHI_NO_DAU_KY" <> 0
    ;


END $$
;

SELECT 
    "TEN_NHAN_VIEN" as "TEN_NHAN_VIEN" ,
    "SO_HOP_DONG" as "HOP_DONG_DU_AN" ,
    "TRICH_YEU" as "TRICH_YEU" ,
    "SO_TAI_KHOAN" as "TK_CONG_NO" ,
    "GHI_NO_DAU_KY" as "NO_DAU_KY" ,
    "GHI_CO_DAU_KY" as "CO_DAU_KY" ,
    "GHI_NO" as "PHAT_SINH_NO" ,
    "GHI_CO" as "PHAT_SINH_CO" ,
    "DU_NO_CUOI_KY" as "NO_CUOI_KY" ,
    "DU_CO_CUOI_KY" as "CO_CUOI_KY" 
FROM TMP_KET_QUA
OFFSET %(offset)s
LIMIT %(limit)s;

        """
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
        if (THONG_KE_THEO == 'KHONG_CHON'):
            action = self.env.ref('bao_cao.open_report_tong_hop_cong_no_nhan_vien_theo_khong_chon').read()[0]
        elif THONG_KE_THEO == 'CONG_TRINH':
            action = self.env.ref('bao_cao.open_report_tong_hop_cong_no_nhan_vien_theo_cong_trinh').read()[0]
        elif THONG_KE_THEO == 'HOP_DONG':
            action = self.env.ref('bao_cao.open_report_tong_hop_cong_no_nhan_vien_theo_hop_dong').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action