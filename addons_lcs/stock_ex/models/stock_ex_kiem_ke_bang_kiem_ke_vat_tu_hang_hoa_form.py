# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import datetime
from odoo.addons import decimal_precision

class STOCK_EX_KIEM_KE_BANG_KIEM_KE_VAT_TU_HANG_HOA_FORM(models.Model):
    _name = 'stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form'
    _description = ''
    _inherit = ['mail.thread']
    _order = "NGAY desc"

    MUC_DICH = fields.Char(string='Mục đích', help='Mục đích')
    KIEM_KE_KHO_ID = fields.Many2one('danh.muc.kho',string='Kiểm kê kho', help='Kiểm kê kho')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    SO = fields.Char(string='Số ', help='Số ', auto_num='stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form_SO')
    NGAY = fields.Date(string='Ngày', help='Ngày',default=fields.Datetime.now)
    GIO = fields.Float(string='Giờ', help='Giờ')
    KIEM_KE_GIA_TRI = fields.Boolean(string='Kiểm kê giá trị', help='Kiểm kê giá trị')
    KET_LUAN = fields.Char(string='Kết luận', help='Kết luận')
    DA_XU_LY_CHENH_LECH = fields.Boolean(string='Đã xử lý chênh lệch', help='Đã xử lý chênh lệch')
    name = fields.Char(string='Name', help='Name', related="SO", store=True, oldname='NAME')

    STOCK_EX_BANG_KIEM_KE_VTHH_THANH_VIEN_THAM_GIA_CHI_TIET_FORM_IDS = fields.One2many('stock.ex.bang.kiem.ke.vthh.tv.tham.gia.chi.tiet.form', 'BANG_KIEM_KE_VTHH_ID', string='Bảng kiểm kê VTHH thành viên tham gia chi tiết form')
    STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM_IDS = fields.One2many('stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form', 'KIEM_KE_BANG_KIEM_KE_VTHH_ID', string='Bảng kiểm kê VTHH cần điều chỉnh chi tiết form')

    KIEM_KE_KHO_BL = fields.Boolean(string='Kiểm kê kho bl', help='Kiểm kê kho bl',default=True)
    CHI_TIET_THEO_SELECTION = fields.Selection([('1', 'Số lô, hạn sử dụng'), ('2', ' Mã quy cách'), ])
    TEN_KHO = fields.Char(string='Tên kho', help='Tên kho')


    TONG_SO_LUONG_SO_KE_TOAN = fields.Float(string='Số lượng sổ kế toán', help='Số lượng sổ kế toán',compute='tinh_tong',store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    TONG_SO_LUONG_KIEM_KE = fields.Float(string='Số lượng kiểm kê', help='Số lượng kiểm kê',compute='tinh_tong',store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    TONG_SO_LUONG_CHENH_LECH = fields.Float(string='Số lượng chênh lệch', help='Số lượng chênh lệch',compute='tinh_tong',store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    TONG_GIA_TRI_SO_KE_TOAN = fields.Float(string='Giá trị sổ kế toán', help='Giá trị sổ kế toán',digits= decimal_precision.get_precision('VND'),compute='tinh_tong',store=True)
    TONG_GIA_TRI_KIEM_KE = fields.Float(string='Giá trị kiểm kê', help='Giá trị kiểm kê',digits= decimal_precision.get_precision('VND'),compute='tinh_tong',store=True)
    TONG_GIA_TRI_CHENH_LECH = fields.Float(string='Giá trị chênh lệch', help='Giá trị chênh lệch',digits= decimal_precision.get_precision('VND'),compute='tinh_tong',store=True)
    TONG_PHAM_CHAT_CON_TOT = fields.Float(string='Còn tốt 100%', help='Phẩm chất còn tốt',compute='tinh_tong',store=True)
    TONG_KEM_PHAM_CHAT = fields.Float(string='Kém phẩm chất', help='Kém phẩm chất',compute='tinh_tong',store=True)
    TONG_MAT_PHAM_CHAT = fields.Float(string='Mất phẩm chất', help='Mất phẩm chất',compute='tinh_tong',store=True)
    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)

    _sql_constraints = [
	('SO_KKKHO_uniq', 'unique ("SO")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
	]
    

    @api.model
    def default_get(self, fields):
        rec = super(STOCK_EX_KIEM_KE_BANG_KIEM_KE_VAT_TU_HANG_HOA_FORM, self).default_get(fields)
        
        rec['LOAI_CHUNG_TU'] = 2060
        current = datetime.now()
        rec['GIO'] = current.hour + 7 + current.minute/60 # GMT+7

        kiem_ke_kho = self.get_context('default_KIEM_KE_KHO_ID')
        den_ngay = self.get_context('default_DEN_NGAY')
        chi_tiet_theo = self.get_context('default_CHI_TIET_THEO')
        don_vi_tinh = self.get_context('default_DON_VI_TINH')
        lay_tat_ca_vat_tu = self.get_context('default_LAY_TAT_CA_VAT_TU')
        rec['DEN_NGAY']=den_ngay
        rec['CHI_TIET_THEO_SELECTION']=chi_tiet_theo
        ds_vat_tu = []
        if chi_tiet_theo == '2':
            ds_vat_tu = self.lay_vat_tu_hang_hoa_theo_mqc(den_ngay,kiem_ke_kho,self.get_chi_nhanh(),lay_tat_ca_vat_tu,don_vi_tinh)
        elif chi_tiet_theo == '1':
            ds_vat_tu = self.lay_vat_tu_hang_hoa_theo_sl_hsd(den_ngay,kiem_ke_kho,self.get_chi_nhanh(),lay_tat_ca_vat_tu,don_vi_tinh)
        else:
            ds_vat_tu = self.lay_vat_tu_hang_hoa(den_ngay,self.get_chi_nhanh(),lay_tat_ca_vat_tu,don_vi_tinh,kiem_ke_kho)
        if ds_vat_tu:
            arr_vat_tu = []
            rec['STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM_IDS'] = []
            for line in ds_vat_tu:
                arr_vat_tu += [(0, 0, {
                    'MA_HANG_ID' : line.get('MA_HANG_ID'),
                    'TEN_HANG': line.get('TEN_HANG'),
                    'DVT_ID': line.get('DVT_ID'),
                    'MA_KHO_ID': line.get('MA_KHO_ID'),
                    'SO_LUONG_SO_KE_TOAN': line.get('SO_LUONG_TREN_SO'),
                    'SO_LUONG_KIEM_KE' : line.get('SO_LUONG_KIEM_KE'),
                    'SO_LUONG_CHENH_LECH' : line.get('SO_LUONG_CHENH_LECH'),
                    'PHAM_CHAT_CON_TOT' : line.get('PHAM_CHAT_CON_TOT'),
                    'KEM_PHAM_CHAT' : line.get('PHAM_CHAT_KEM'),
                    'MAT_PHAM_CHAT' : line.get('PHAM_CHAT_MAT'),
                    'GIA_TRI_SO_KE_TOAN' : line.get('GIA_TRI_SO_KE_TOAN'),

                    'MA_QUY_CACH_1' : line.get('MA_QUY_CACH_1'),
                    'MA_QUY_CACH_2' : line.get('MA_QUY_CACH_2'),
                    'MA_QUY_CACH_3' : line.get('MA_QUY_CACH_3'),
                    'MA_QUY_CACH_4' : line.get('MA_QUY_CACH_4'),
                    'MA_QUY_CACH_5' : line.get('MA_QUY_CACH_5'),
                    })]

            rec['STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM_IDS'] = arr_vat_tu

        return rec


    @api.onchange('KIEM_KE_KHO_ID')
    def update_thaydoi_kiem_ke_kho_bl(self):
        if self.KIEM_KE_KHO_ID.id == -1 :
            self.KIEM_KE_KHO_BL = False
            self.TEN_KHO = '<<Tất cả>>'
        else:
            self.KIEM_KE_KHO_BL =True
            self.TEN_KHO = self.KIEM_KE_KHO_ID.TEN_KHO

    @api.depends('STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM_IDS')
    def tinh_tong(self):
        for order in self:
            tong_tien_sl_ke_toan = tong_sl_kiem_ke= tong_sl_chenh_lech= tong_gia_tri_ke_toan=tong_gia_tri_kiem_ke= tong_gia_tri_chenh_lech = tong_con_tot= tong_kem_pc=tong_mat_pc = 0.0
            for line in order.STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM_IDS:
                tong_tien_sl_ke_toan += line.SO_LUONG_SO_KE_TOAN
                tong_sl_kiem_ke += line.SO_LUONG_KIEM_KE
                tong_sl_chenh_lech += line.SO_LUONG_CHENH_LECH

                tong_gia_tri_ke_toan += line.GIA_TRI_SO_KE_TOAN
                tong_gia_tri_kiem_ke += line.GIA_TRI_KIEM_KE
                tong_gia_tri_chenh_lech += line.GIA_TRI_CHENH_LECH

                tong_con_tot += line.PHAM_CHAT_CON_TOT
                tong_kem_pc += line.KEM_PHAM_CHAT
                tong_mat_pc += line.MAT_PHAM_CHAT
               
            order.update({
                'TONG_SO_LUONG_SO_KE_TOAN': tong_tien_sl_ke_toan,
                'TONG_SO_LUONG_KIEM_KE': tong_sl_kiem_ke,
                'TONG_SO_LUONG_CHENH_LECH': tong_sl_chenh_lech,
                'TONG_GIA_TRI_SO_KE_TOAN': tong_gia_tri_ke_toan,
                'TONG_GIA_TRI_KIEM_KE': tong_gia_tri_kiem_ke,
                'TONG_GIA_TRI_CHENH_LECH': tong_gia_tri_chenh_lech,
                'TONG_PHAM_CHAT_CON_TOT': tong_con_tot,
                'TONG_KEM_PHAM_CHAT': tong_kem_pc,
                'TONG_MAT_PHAM_CHAT': tong_mat_pc,
            })


    @api.multi
    def btn_Kiem_Ke_PN(self):
        id_bang_kiem_ke = self.id
        action = self.env.ref('stock_ex.action_open_stock_ex_nk_form').read()[0]
        context ={
            'default_ID_BANG_KIEM_KE': id_bang_kiem_ke,
            'default_LOAI_CHUNG_TU_KIEM_KE_VTHH'     :2015 ,
         }
        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['name'] =' Phiếu nhập kho thành phẩm lắp ráp' 
        return action
    
    @api.multi
    def btn_Kiem_Ke_PX(self):
        id_bang_kiem_ke = self.id
        action = self.env.ref('stock_ex.action_open_stock_ex_xk_form').read()[0]
        context ={
            'default_ID_BANG_KIEM_KE': id_bang_kiem_ke,
            'default_LOAI_CHUNG_TU_KIEM_KE_VTHH_PX'     :2026 ,
         }
        action['context'] = helper.Obj.merge(context, action.get('context'))
       
        return action



    

    def lay_vat_tu_hang_hoa(self,den_ngay,chi_nhanh,lay_tat,don_vi_tinh,kho_id):
        record = []
        dvt = 2
        if don_vi_tinh == '0':
            dvt = 0
        elif don_vi_tinh == '1':
            dvt = 1

        if lay_tat == False:
            lay_tat_ca_vthh_khong_ton_kho = 0
        else:
            lay_tat_ca_vthh_khong_ton_kho = 1
        params = {
            'CHI_NHANH_ID': chi_nhanh,
            'DEN_NGAY' : den_ngay,
            'KHO_ID' : kho_id,
            'STT_DVT' : dvt,
            'LAY_TAT_CA_VTHH_KHONG_TON_KHO' : lay_tat_ca_vthh_khong_ton_kho,
            }

        query = """   

                	DO LANGUAGE plpgsql $$
                    DECLARE
                    chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s;
                    den_ngay DATE := %(DEN_NGAY)s;
                    tach_roi_theo_vthh INTEGER := 0;
                    tach_roi_theo_kho INTEGER := 0;
                    lay_tat_ca_vthh_khong_ton_kho INTEGER:= %(LAY_TAT_CA_VTHH_KHONG_TON_KHO)s;
                    kho_id INTEGER := %(KHO_ID)s;
                    stt_dvt INTEGER := %(STT_DVT)s;
                    
                    BEGIN
                    DROP TABLE IF EXISTS TMP_KET_QUA_TMP;
                    CREATE TEMP TABLE TMP_KET_QUA_TMP
                        AS
                    SELECT
                --                 '1' AS stt,
                                R."MA_HANG_ID"
                                , CAST(R."MA" AS VARCHAR(25))       AS "MA_HANG"
                                , CAST(R."TEN" AS VARCHAR(255))     AS "TEN_HANG"
                                , R."DVT_ID"
                                , CAST(R."TEN_DVT" AS VARCHAR(20))  AS "TEN_DVT"
                                , S.id                              AS "MA_KHO_ID"
                                , CAST(S."MA_KHO" AS VARCHAR(20))   AS "MA_KHO"
                                , CAST(S."TEN_KHO" AS VARCHAR(128)) AS "TEN_KHO"
                            FROM
                                (
                                SELECT
                                    II.id                    AS "MA_HANG_ID"
                                    , II."MA"
                                    , II."TEN"
                                    , (CASE WHEN stt_dvt = 0
                                    THEN II."DVT_CHINH_ID"
                                        ELSE IIUC."DVT_ID" END) AS "DVT_ID"
                                    , (CASE WHEN stt_dvt = 0
                                    THEN U.name
                                        ELSE UI.name END)       AS "TEN_DVT"
                                FROM danh_muc_vat_tu_hang_hoa AS II
                                    /*Lấy ra thông tin về loại đơn vị chuyển đổi của vật tư*/
                                    LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi AS IIUC
                                    ON IIUC."VAT_TU_HANG_HOA_ID" = II.id AND IIUC."STT" = 0
                                    /*Lấy ra thông tin về đơn vị tính của cái món đơn vị chuyển đổi*/
                                    LEFT JOIN danh_muc_don_vi_tinh AS UI ON UI.id = IIUC."DVT_ID"
                                    /*Lấy ra thông tin về đơn vị tính chính trên danh mục*/
                                    LEFT JOIN danh_muc_don_vi_tinh AS U ON U.id = II."DVT_CHINH_ID"
                                WHERE II."TINH_CHAT" NOT IN ('2', '3') AND II."DVT_CHINH_ID" IS NOT NULL
                                        AND ((tach_roi_theo_vthh = 1 AND (II."CHI_NHANH_ID" = chi_nhanh_id)) OR (tach_roi_theo_vthh = 0))

                                ) AS R, danh_muc_kho AS S
                            WHERE R."DVT_ID" IS NOT NULL AND (S.id = kho_id OR kho_id = -1)
                                    AND ((tach_roi_theo_kho = 1 AND S."CHI_NHANH_ID" = chi_nhanh_id) OR
                                        (tach_roi_theo_kho = 0))  /* nhyen_18/5/2017_cr12832: lọc dữ liệu theo tùy chọn dùng riêng dạnh mục kho*/

                            ORDER BY R."MA_HANG_ID", S."MA_KHO"
                    ;

                    IF stt_dvt = 0
                    THEN
                    INSERT INTO TMP_KET_QUA_TMP(
                    SELECT
                --                 '2' AS stt,
                                II.id    AS "MA_HANG_ID"
                                , II."MA"  AS "MA_HANG"
                                , II."TEN" AS "TEN_HANG"
                                , II."DVT_CHINH_ID"
                                , NULL
                                , S.id     AS "MA_KHO_ID"
                                , S."MA_KHO"
                                , S."TEN_KHO"
                            FROM danh_muc_vat_tu_hang_hoa AS II, danh_muc_kho AS S
                            WHERE II."TINH_CHAT" NOT IN ('2', '3')
                                    AND ((tach_roi_theo_vthh = 1 AND (II."CHI_NHANH_ID" = chi_nhanh_id)) OR (tach_roi_theo_vthh = 0))
                                    AND II."DVT_CHINH_ID" IS NULL
                                    AND (S.id = kho_id OR kho_id = -1)
                                    AND ((tach_roi_theo_kho = 1 AND S."CHI_NHANH_ID" = chi_nhanh_id) OR
                                        (tach_roi_theo_kho = 0))  /* nhyen_18/5/2017_cr12832: lọc dữ liệu theo tùy chọn dùng riêng dạnh mục kho*/
                    );
                    END IF ;

                    DROP TABLE IF EXISTS TMP_KET_QUA1;
                    CREATE TEMP TABLE TMP_KET_QUA1
                        AS
                        SELECT *,CAST(0 AS DECIMAL(22, 8)) AS "PHAM_CHAT_CON_TOT",
                        CAST(0 AS DECIMAL(22, 8)) AS "PHAM_CHAT_KEM",
                        CAST(0 AS DECIMAL(22, 8)) AS "PHAM_CHAT_MAT"
                    FROM (

                        SELECT
                --     stt,
                    0                         AS "ID_CHUNG_TU"
                , 0                        AS "CHI_TIET_ID"
                , R."MA_HANG_ID"
                , R."MA_HANG"
                , R."TEN_HANG"
                , R."DVT_ID"
                , R."TEN_DVT"
                , R."MA_KHO_ID"
                , R."MA_KHO"
                , R."TEN_KHO"
                , SUM(R."SO_LUONG_TREN_SO")        AS "SO_LUONG_TREN_SO"
                , SUM(R."SO_LUONG_KIEM_KE")         AS "SO_LUONG_KIEM_KE"
                , SUM(R."SO_LUONG_CHENH_LECH")          AS "SO_LUONG_CHENH_LECH"
                , SUM(R."SO_TIEN_QUY_DOI_TREN_SO") AS "SO_TIEN_QUY_DOI_TREN_SO"
                , SUM(R."SO_TIEN_QUY_DOI_KIEM_KE")  AS "SO_TIEN_QUY_DOI_KIEM_KE"
                --   , SUM(R."SO_TIEN_QUY_DOI_KIEM_KE")   AS "SO_TIEN_QUY_DOI_KIEM_KE"
                FROM (

                    SELECT
                --         stt,
                        "MA_HANG_ID"
                        , "MA_HANG"
                        , "TEN_HANG"
                        , "DVT_ID"
                        , "TEN_DVT"
                        , "MA_KHO_ID"
                        , "MA_KHO"
                        , "TEN_KHO"
                        , CAST(0 AS DECIMAL(18, 4)) AS "SO_LUONG_TREN_SO"
                        , CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_KIEM_KE"
                        , CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_CHENH_LECH"
                        , CAST(0 AS DECIMAL(18, 4)) AS "SO_TIEN_QUY_DOI_TREN_SO"
                        , CAST(0 AS DECIMAL(18, 4)) AS "SO_TIEN_QUY_DOI_KIEM_KE"
                        , CAST(0 AS DECIMAL(18, 4)) AS "SO_TIEN_QUY_DOI_CHENH_LECH"
                    FROM (SELECT *FROM TMP_KET_QUA_TMP) AS R1

                    UNION ALL

                    SELECT
                --          '3' AS stt,
                        I.id                                                    AS "MA_HANG_ID"
                        , I."MA"                                                  AS "MA_HANG"
                        , I."TEN"                                                 AS "TEN_HANG"
                        , CASE WHEN stt_dvt = 0
                        THEN I."DVT_CHINH_ID"
                        ELSE UC."DVT_ID"
                        END                                                     AS "DVT_ID"
                        , CASE WHEN stt_dvt = 0
                        THEN UI.name
                        ELSE U.name
                        END                                                     AS "TEN_DVT"
                        , ST.id                                                   AS "MA_KHO_ID"
                        , ST."MA_KHO"
                        , ST."TEN_KHO"
                        , ROUND(cast(SUM(CASE WHEN U.id IS NOT NULL
                                                    AND IL."DVT_ID" = U.id
                        THEN coalesce(IL."SO_LUONG_NHAP",0) - coalesce(IL."SO_LUONG_XUAT",0)
                                        ELSE (coalesce(IL."SO_LUONG_NHAP_THEO_DVT_CHINH",0)
                                                - coalesce(IL."SO_LUONG_XUAT_THEO_DVT_CHINH",0))
                                            * coalesce(UC."TI_LE_CHUYEN_DOI", 1)
                                        END) AS NUMERIC), 2)                     AS "SO_LUONG_TREN_SO"
                        , CAST(0 AS DECIMAL(22, 8))                               AS "SO_LUONG_KIEM_KE"
                        , CAST(0 AS DECIMAL(22, 8))                               AS "SO_LUONG_CHENH_LECH"
                        , coalesce(SUM(coalesce(IL."SO_TIEN_NHAP",0) - coalesce(IL."SO_TIEN_XUAT",0)), 0) AS "SO_TIEN_QUY_DOI_TREN_SO"
                        , CAST(0 AS DECIMAL(18, 4))                               AS "SO_TIEN_QUY_DOI_KIEM_KE"
                        , CAST(0 AS DECIMAL(18, 4))                               AS "SO_TIEN_QUY_DOI_CHENH_LECH"

                    FROM so_kho_chi_tiet AS IL
                        INNER JOIN danh_muc_kho ST ON IL."KHO_ID" = ST.id
                        INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU.id
                        /*Chi nhánh*/
                        INNER JOIN danh_muc_vat_tu_hang_hoa I
                        ON IL."MA_HANG_ID" = I.id AND I."TINH_CHAT" NOT IN ('2', '3')
                        /*Vật tư: Chỉ là diễn giải hoặc là HHDV*/
                        LEFT JOIN danh_muc_don_vi_tinh UI ON I."DVT_CHINH_ID" = UI.id
                        /*Đơn vị tính chính trên danh mục*/
                        /*Lấy ra hệ số quy đổi, là phép nhân thì trả ra hệ số là "TI_LE_CHUYEN_DOI", nếu là phép chia thì trả ra hệ số là 1 / IIUC."TI_LE_CHUYEN_DOI"*/
                        LEFT JOIN (SELECT
                                        IIUC."VAT_TU_HANG_HOA_ID" AS "MA_HANG_ID"
                                    , "DVT_ID"
                                    , IIUC."STT"
                                    , (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                            THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                        WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                                        THEN 1
                                        ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                        END)                     AS "TI_LE_CHUYEN_DOI"
                                    FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
                                    WHERE IIUC."STT" = 0
                                ) UC ON I.id = UC."MA_HANG_ID"
                        /*Lấy ra thông tin về đơn vị tính theo loại đơn vị tính truyền vào*/
                        LEFT JOIN danh_muc_don_vi_tinh U ON (UC."MA_HANG_ID" IS NULL
                                                            AND U.id = I."DVT_CHINH_ID"
                                                            )
                                                            OR (UC."MA_HANG_ID" IS NOT NULL
                                                                AND UC."DVT_ID" = U.id
                                                            )
                    WHERE (IL."KHO_ID" = kho_id OR kho_id = -1)
                            AND IL."CHI_NHANH_ID" = chi_nhanh_id
                            AND IL."NGAY_HACH_TOAN" <= den_ngay
                    GROUP BY I.id,
                        I."MA",
                        I."TEN",
                        ST.id,
                        ST."MA_KHO",
                        ST."TEN_KHO",
                        UC."DVT_ID",
                        CASE WHEN stt_dvt = 0
                        THEN I.id
                        ELSE UC."DVT_ID"
                        END,
                        CASE WHEN stt_dvt = 0
                        THEN UI.name
                        ELSE U.name END
                    ) AS R
                GROUP BY
                --   stt,
                R."MA_HANG_ID",
                R."MA_HANG",
                R."TEN_HANG",
                R."DVT_ID",
                R."TEN_DVT",
                R."MA_KHO_ID",
                R."MA_KHO",
                R."TEN_KHO"
                ) AS R
                -- WHERE "SO_LUONG_TREN_SO" <> 0 AND ((stt_dvt = 0 ) OR (0 <> 0 AND "DVT_ID" IS NOT NULL ))

                ORDER BY "MA_HANG","MA_KHO"
                    ;

                IF lay_tat_ca_vthh_khong_ton_kho = 0
                THEN
                    DROP TABLE IF EXISTS TMP_KET_QUA;
                    CREATE TEMP TABLE TMP_KET_QUA
                        AS
                    SELECT *
                    FROM TMP_KET_QUA1
                    WHERE "SO_LUONG_TREN_SO" <> 0 AND ((stt_dvt = 0 ) OR (stt_dvt <> 0 AND "DVT_ID" IS NOT NULL ))
                    ORDER BY "MA_HANG","MA_KHO"
                    ;
                ELSE
                    DROP TABLE IF EXISTS TMP_KET_QUA;
                    CREATE TEMP TABLE TMP_KET_QUA
                        AS
                    SELECT *
                    FROM TMP_KET_QUA1
                    WHERE ((stt_dvt = 0 ) OR (stt_dvt <> 0 AND "DVT_ID" IS NOT NULL ))
                    ORDER BY "MA_HANG","MA_KHO"
                    ;
                END IF;

                    END $$;

                    SELECT *FROM TMP_KET_QUA
                ;

        """  
        
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'MA_HANG_ID': line.get('MA_HANG_ID', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT_ID': line.get('DVT_ID', ''),
                'MA_KHO_ID': line.get('MA_KHO_ID', ''),
                'SO_LUONG_TREN_SO': line.get('SO_LUONG_TREN_SO', ''),
                'SO_LUONG_KIEM_KE': line.get('SO_LUONG_KIEM_KE', ''),
                'SO_LUONG_CHENH_LECH': line.get('SO_LUONG_CHENH_LECH', ''),
                'PHAM_CHAT_CON_TOT': line.get('PHAM_CHAT_CON_TOT', ''),   
                'PHAM_CHAT_KEM' : line.get('PHAM_CHAT_KEM', ''),   
                'PHAM_CHAT_MAT' : line.get('PHAM_CHAT_MAT', ''), 
                'GIA_TRI_SO_KE_TOAN' : line.get('SO_TIEN_QUY_DOI_TREN_SO', ''), 

                'MA_QUY_CACH_1' : '', 
                'MA_QUY_CACH_2' : '', 
                'MA_QUY_CACH_3' : '', 
                'MA_QUY_CACH_4' : '', 
                'MA_QUY_CACH_5' : '', 
            })
        
        return record


    

    def lay_vat_tu_hang_hoa_theo_mqc(self,den_ngay,kho_id,chi_nhanh,lay_tat,don_vi_tinh):
        record = []
        dvt = 2
        if don_vi_tinh == '0':
            dvt = 0
        elif don_vi_tinh == '1':
            dvt = 1
        params = {
            'DEN_NGAY': den_ngay,
            'CHI_NHANH_ID' : chi_nhanh,
            'KHO_ID' : kho_id,
            'IsUseStockSeperate' : False,
            'DVT' : dvt,
            'LAY_TAT_CA_VTHH' : lay_tat,
            }

        # tham số tach_roi_theo_vthh,tach_roi_theo_kho chưa biết lấy thế nào
        query = """   

        DO LANGUAGE plpgsql $$
        DECLARE
        chi_nhanh_id                  INTEGER := %(CHI_NHANH_ID)s;
        den_ngay                      DATE := %(DEN_NGAY)s;
        tach_roi_theo_vthh            INTEGER := 0;
        tach_roi_theo_kho             INTEGER := 0;
        lay_tat_ca_vthh_khong_ton_kho INTEGER := %(LAY_TAT_CA_VTHH)s;
        kho_id                        INTEGER := %(KHO_ID)s;
        stt_dvt                       INTEGER := %(DVT)s;

        BEGIN

        DROP TABLE IF EXISTS TMP_VTHH_TRONG_KHO;
        CREATE TEMP TABLE TMP_VTHH_TRONG_KHO
            AS
            SELECT
                I.id             AS "MA_HANG_ID",
                I."MA"           AS "MA_HANG",
                I."TEN"          AS "TEN_HANG",
                I."DVT_CHINH_ID" AS "DVT_ID",
                UI.name          AS "TEN_DVT",
                ST.id            AS "MA_KHO_ID",
                ST."MA_KHO",
                ST."TEN_KHO",
                ISN."MA_QUY_CACH_1",
                ISN."MA_QUY_CACH_2",
                ISN."MA_QUY_CACH_3",
                ISN."MA_QUY_CACH_4",
                ISN."MA_QUY_CACH_5",
                SUM(CASE WHEN ISN."CHI_TIET_ID" IS NULL
                THEN (IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH")
                    ELSE (ISN."SO_LUONG_NHAP"
                        - ISN."SO_LUONG_XUAT")
                    END)         AS "SO_LUONG_TREN_SO" /*nhyen_25/5/2017_Bug108929: Sap chép dữ liệu cho bảng tạm*/
            FROM so_kho_chi_tiet AS IL
                INNER JOIN danh_muc_vat_tu_hang_hoa I
                ON IL."MA_HANG_ID" = I.id AND I."TINH_CHAT" NOT IN ('2', '3')
                /*Vật tư: Chỉ là diễn giải hoặc là HHDV*/
                INNER JOIN danh_muc_kho ST ON IL."KHO_ID" = ST.id
                LEFT JOIN danh_muc_don_vi_tinh UI ON I."DVT_CHINH_ID" = UI.id
                /*Đơn vị tính chính trên danh mục*/
                LEFT JOIN stock_ex_chung_tu_luu_ma_quy_cach AS ISN
                ON IL."CHI_TIET_ID" = ISN."CHI_TIET_ID" AND IL."KHO_ID" = ISN."KHO_NHAP"
                    AND (ISN."LOAI_SERI" = '1' OR ISN."LOAI_SERI" = '0') /*Chỉ lấy các dòng nhập, xuất mã quy cách*/
            WHERE IL."NGAY_HACH_TOAN" <= den_ngay
                    AND (IL."KHO_ID" = kho_id OR kho_id = -1)
                    AND IL."CHI_NHANH_ID" = chi_nhanh_id
            GROUP BY I.id,
                I."MA",
                I."TEN",
                I."DVT_CHINH_ID",
                UI.name,
                ST.id,
                ST."MA_KHO",
                ST."TEN_KHO",
                ISN."MA_QUY_CACH_1",
                ISN."MA_QUY_CACH_2",
                ISN."MA_QUY_CACH_3",
                ISN."MA_QUY_CACH_4",
                ISN."MA_QUY_CACH_5";

        IF lay_tat_ca_vthh_khong_ton_kho = 0
        THEN
            DROP TABLE IF EXISTS TMP_KET_QUA;
            CREATE TEMP TABLE TMP_KET_QUA
            AS
                SELECT
                0                         AS "ID_CHUNG_TU",
                0                         AS "CHI_TIET_ID",
                R."MA_HANG_ID",
                R."MA_HANG",
                R."TEN_HANG",
                R."DVT_ID",
                R."TEN_DVT",
                R."MA_KHO_ID",
                R."MA_KHO",
                R."TEN_KHO",
                R."MA_QUY_CACH_1",
                R."MA_QUY_CACH_2",
                R."MA_QUY_CACH_3",
                R."MA_QUY_CACH_4",
                R."MA_QUY_CACH_5",
                R."SO_LUONG_TREN_SO",
                CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_KIEM_KE",
                CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_CHENH_LECH"
                FROM TMP_VTHH_TRONG_KHO AS R
                WHERE R."SO_LUONG_TREN_SO" <> 0
                ORDER BY R."MA_HANG",
                R."MA_KHO",
                R."MA_QUY_CACH_1",
                R."MA_QUY_CACH_2",
                R."MA_QUY_CACH_3",
                R."MA_QUY_CACH_4",
                R."MA_QUY_CACH_5";
        ELSE
            DROP TABLE IF EXISTS TMP_VTHH;
            CREATE TEMP TABLE TMP_VTHH
            AS
                SELECT
                R."MA_HANG_ID",
                R."MA_HANG",
                R."TEN_HANG",
                R."DVT_ID",
                R."TEN_DVT",
                S.id AS "MA_KHO_ID",
                S."MA_KHO",
                S."TEN_KHO"
                FROM
                (
                    SELECT
                    II.id             AS "MA_HANG_ID",
                    II."MA"           AS "MA_HANG",
                    II."TEN"          AS "TEN_HANG",
                    II."DVT_CHINH_ID" AS "DVT_ID",
                    U.name            AS "TEN_DVT"
                    FROM danh_muc_vat_tu_hang_hoa AS II
                    /*Lấy ra thông tin về đơn vị tính chính trên danh mục*/
                    LEFT JOIN danh_muc_don_vi_tinh AS U ON U.id = II."DVT_CHINH_ID"
                    WHERE II."TINH_CHAT" NOT IN ('2', '3')
                        AND ((tach_roi_theo_vthh = 1 AND (II."CHI_NHANH_ID" = chi_nhanh_id)) OR (tach_roi_theo_vthh = 0))
                ) AS R, danh_muc_kho AS S
                WHERE (S.id = kho_id OR kho_id = -1)
                    AND ((tach_roi_theo_kho = 1 AND S."CHI_NHANH_ID" = chi_nhanh_id) OR
                        (tach_roi_theo_kho = 0));
            /* nhyen_18/5/2017_cr12832:lọc dữ liệu theo tùy chọn dùng riêng dạnh mục kho*/
            DROP TABLE IF EXISTS TMP_KET_QUA;
            CREATE TEMP TABLE TMP_KET_QUA
            AS
                SELECT
                0                                 AS "ID_CHUNG_TU",
                0                                 AS RefDetailID,
                II."MA_HANG_ID",
                II."MA_HANG",
                II."TEN_HANG",
                II."DVT_ID",
                II."TEN_DVT",
                II."MA_KHO_ID",
                II."MA_KHO",
                II."TEN_KHO",
                R."MA_QUY_CACH_1",
                R."MA_QUY_CACH_2",
                R."MA_QUY_CACH_3",
                R."MA_QUY_CACH_4",
                R."MA_QUY_CACH_5",
                coalesce(R."SO_LUONG_TREN_SO", 0) AS "SO_LUONG_TREN_SO",
                CAST(0 AS DECIMAL(22, 8))         AS "SO_LUONG_KIEM_KE",
                CAST(0 AS DECIMAL(22, 8))         AS "SO_LUONG_CHENH_LECH"
                FROM TMP_VTHH AS II
                LEFT JOIN TMP_VTHH_TRONG_KHO AS R ON II."MA_HANG_ID" = R."MA_HANG_ID" AND II."MA_KHO_ID" = R."MA_KHO_ID"
                ORDER BY II."MA_HANG",
                II."MA_KHO",
                R."MA_QUY_CACH_1",
                R."MA_QUY_CACH_2",
                R."MA_QUY_CACH_3",
                R."MA_QUY_CACH_4",
                R."MA_QUY_CACH_5";
        END IF;

        END $$;

        SELECT *
        FROM TMP_KET_QUA
        WHERE "MA_HANG" = 'AO_SM_NAM' AND "MA_KHO" = 'KHH'
        ;


        """  
        
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'MA_HANG_ID': line.get('MA_HANG_ID', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT_ID': line.get('DVT_ID', ''),
                'MA_KHO_ID': line.get('MA_KHO_ID', ''),
                'SO_LUONG_TREN_SO': line.get('SO_LUONG_TREN_SO', ''),
                'SO_LUONG_KIEM_KE': line.get('SO_LUONG_KIEM_KE', ''),
                'SO_LUONG_CHENH_LECH': line.get('SO_LUONG_CHENH_LECH', ''),

                'MA_QUY_CACH_1': line.get('MA_QUY_CACH_1', ''),
                'MA_QUY_CACH_2': line.get('MA_QUY_CACH_2', ''),
                'MA_QUY_CACH_3': line.get('MA_QUY_CACH_3', ''),
                'MA_QUY_CACH_4': line.get('MA_QUY_CACH_4', ''),
                'MA_QUY_CACH_5': line.get('MA_QUY_CACH_5', ''),
                
            })
        
        return record



    
    def lay_vat_tu_hang_hoa_theo_sl_hsd(self,den_ngay,kho_id,chi_nhanh,lay_tat,don_vi_tinh):
        record = []
        dvt = 2
        if don_vi_tinh == '0':
            dvt = 0
        elif don_vi_tinh == '1':
            dvt = 1
        params = {
            'DEN_NGAY': den_ngay,
            'CHI_NHANH_ID' : chi_nhanh,
            'KHO_ID' : kho_id,
            'IsUseStockSeperate' : False,
            'STT_DVT' : dvt,
            }

        if lay_tat == False:
            query = """   

        SELECT
    0                   AS "ID_CHUNG_TU"
  , 0                   AS "CHI_TIET_ID"
  , R."MA_HANG_ID"
  , R."MA_HANG"
  , R."TEN_HANG"
  , R."DVT_ID"
  , R."TEN_DVT"
  , R."MA_KHO_ID"
  , R."MA_KHO"
  , R."TEN_KHO"
  , R."SO_LO"
  , R."NGAY_HET_HAN"
  , R."SO_LUONG_TREN_SO"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_KIEM_KE"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_CHENH_LECH"
  , R."SO_TIEN_QUY_DOI_TREN_SO"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_TIEN_QUY_DOI_KIEM_KE"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_TIEN_QUY_DOI_CHENH_LECH"
FROM (

       SELECT
         I."MA_HANG_ID"
         , I."MA_HANG"
         , I."TEN_HANG"
         , I."DVT_ID"
         , I."TEN_DVT"
         , I."MA_KHO_ID"
         , I."MA_KHO"
         , I."TEN_KHO"
         , IL."SO_LO"
         , IL."NGAY_HET_HAN"
         , ROUND(cast(SUM(CASE WHEN I."DVT_ID" IS NOT NULL AND IL."DVT_ID" = I."DVT_ID"
         THEN IL."SO_LUONG_NHAP" - IL."SO_LUONG_XUAT"
                          ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH") *
                               I."TI_LE_CHUYEN_DOI"
                          END) AS NUMERIC), 2)        AS "SO_LUONG_TREN_SO"
         , SUM(IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT") AS "SO_TIEN_QUY_DOI_TREN_SO"
       FROM (

              SELECT
                R."MA_HANG_ID"
                , R."MA_HANG"
                , R."TEN_HANG"
                , R."DVT_ID"
                , R."TEN_DVT"
                , S.id AS "MA_KHO_ID"
                , S."MA_KHO"
                , S."TEN_KHO"
                , R."TI_LE_CHUYEN_DOI"
              FROM
                (
                  SELECT
                      II.id    AS "MA_HANG_ID"
                    , II."MA"  AS "MA_HANG"
                    , II."TEN" AS "TEN_HANG"
                    , U.id     AS "DVT_ID"
                    , U.name   AS "TEN_DVT"
                    , CASE WHEN %(STT_DVT)s = 0 OR 0 IS NULL
                    THEN 1
                      WHEN IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                        THEN 1
                      WHEN IU."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                        THEN 1 / coalesce(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                      ELSE coalesce(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                      END      AS "TI_LE_CHUYEN_DOI"
                  FROM danh_muc_vat_tu_hang_hoa AS II
                    LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IU ON II.id = IU."VAT_TU_HANG_HOA_ID"
                                                                               AND IU."STT" = 0
                    LEFT JOIN danh_muc_don_vi_tinh U ON ((0 IS NULL
                                                          OR %(STT_DVT)s = 0
                                                         )
                                                         AND II."DVT_CHINH_ID" = U.id
                                                        )
                                                        OR (%(STT_DVT)s IS NOT NULL
                                                            AND %(STT_DVT)s <> 0
                                                            AND IU."DVT_ID" = U.id
                                                        )
                  WHERE II."TINH_CHAT" NOT IN ('1', '2')
                        AND ((%(IsUseStockSeperate)s = TRUE AND (II."CHI_NHANH_ID" = %(CHI_NHANH_ID)s)) OR (%(IsUseStockSeperate)s = FALSE))
                ) AS R, danh_muc_kho AS S
              WHERE (S.id = %(KHO_ID)s OR %(KHO_ID)s = %(KHO_ID)s)
                    AND ((%(IsUseStockSeperate)s = TRUE AND S."CHI_NHANH_ID" = 81) OR (%(IsUseStockSeperate)s = FALSE))
                    /* nhyen_18/5/2017_cr12832: lọc dữ liệu theo tùy chọn dùng riêng dạnh mục kho*/
                    AND ((%(STT_DVT)s = 0) OR (%(STT_DVT)s <> 0 AND R."DVT_ID" IS NOT NULL))

            ) AS I
         INNER JOIN so_kho_chi_tiet AS IL ON I."MA_HANG_ID" = IL."MA_HANG_ID" AND I."MA_KHO_ID" = IL."KHO_ID"
       WHERE IL."NGAY_HACH_TOAN" <= %(DEN_NGAY)s
             AND (IL."KHO_ID" = %(KHO_ID)s OR %(KHO_ID)s = %(KHO_ID)s)
             AND IL."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
       GROUP BY I."MA_HANG_ID",
         I."MA_HANG",
         I."TEN_HANG",
         I."DVT_ID",
         I."TEN_DVT",
         I."MA_KHO_ID",
         I."MA_KHO",
         I."TEN_KHO",
         IL."SO_LO",
         IL."NGAY_HET_HAN"

     ) AS R
WHERE R."SO_LUONG_TREN_SO" <> 0
AND ((%(STT_DVT)s = 0 ) OR (%(STT_DVT)s <> 0 AND R."DVT_ID" IS NOT NULL ))
ORDER BY R."MA_HANG",
R."MA_KHO",
R."SO_LO"

        """  
        else:
            query = """   

        SELECT
    0                   AS "ID_CHUNG_TU"
  , 0                   AS "CHI_TIET_ID"
  , I."MA_HANG_ID"
  , I."MA_HANG"
  , I."TEN_HANG"
  , I."DVT_ID"
  , I."TEN_DVT"
  , I."MA_KHO_ID"
  , I."MA_KHO"
  , I."TEN_KHO"
  , R."SO_LO"
  , R."NGAY_HET_HAN"
  , R."SO_LUONG_TREN_SO"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_KIEM_KE"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_LUONG_CHENH_LECH"
  , R."SO_TIEN_QUY_DOI_TREN_SO"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_TIEN_QUY_DOI_KIEM_KE"
  , CAST(0 AS DECIMAL(22, 8)) AS "SO_TIEN_QUY_DOI_CHENH_LECH"
FROM (

       SELECT
                R."MA_HANG_ID"
                , R."MA_HANG"
                , R."TEN_HANG"
                , R."DVT_ID"
                , R."TEN_DVT"
                , S.id AS "MA_KHO_ID"
                , S."MA_KHO"
                , S."TEN_KHO"
                , R."TI_LE_CHUYEN_DOI"
              FROM
                (
                  SELECT
                      II.id    AS "MA_HANG_ID"
                    , II."MA"  AS "MA_HANG"
                    , II."TEN" AS "TEN_HANG"
                    , U.id     AS "DVT_ID"
                    , U.name   AS "TEN_DVT"
                    , CASE WHEN %(STT_DVT)s = 0 OR 0 IS NULL
                    THEN 1
                      WHEN IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                        THEN 1
                      WHEN IU."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                        THEN 1 / coalesce(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                      ELSE coalesce(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                      END      AS "TI_LE_CHUYEN_DOI"
                  FROM danh_muc_vat_tu_hang_hoa AS II
                    LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IU ON II.id = IU."VAT_TU_HANG_HOA_ID"
                                                                               AND IU."STT" = 0
                    LEFT JOIN danh_muc_don_vi_tinh U ON ((0 IS NULL
                                                          OR %(STT_DVT)s = 0
                                                         )
                                                         AND II."DVT_CHINH_ID" = U.id
                                                        )
                                                        OR (%(STT_DVT)s IS NOT NULL
                                                            AND %(STT_DVT)s <> 0
                                                            AND IU."DVT_ID" = U.id
                                                        )
                  WHERE II."TINH_CHAT" NOT IN ('1', '2')
                        AND ((%(IsUseStockSeperate)s = TRUE AND (II."CHI_NHANH_ID" = %(CHI_NHANH_ID)s)) OR (%(IsUseStockSeperate)s = FALSE))
                ) AS R, danh_muc_kho AS S
              WHERE (S.id = %(KHO_ID)s OR %(KHO_ID)s = %(KHO_ID)s)
                    AND ((%(IsUseStockSeperate)s = TRUE AND S."CHI_NHANH_ID" = 81) OR (%(IsUseStockSeperate)s = FALSE))
                    /* nhyen_18/5/2017_cr12832: lọc dữ liệu theo tùy chọn dùng riêng dạnh mục kho*/
                    AND ((%(STT_DVT)s = 0) OR (%(STT_DVT)s <> 0 AND R."DVT_ID" IS NOT NULL))

     ) AS I
     LEFT JOIN (

          SELECT
         I."MA_HANG_ID"
         , I."MA_HANG"
         , I."TEN_HANG"
         , I."DVT_ID"
         , I."TEN_DVT"
         , I."MA_KHO_ID"
         , I."MA_KHO"
         , I."TEN_KHO"
         , IL."SO_LO"
         , IL."NGAY_HET_HAN"
         , ROUND(cast(SUM(CASE WHEN I."DVT_ID" IS NOT NULL AND IL."DVT_ID" = I."DVT_ID"
         THEN IL."SO_LUONG_NHAP" - IL."SO_LUONG_XUAT"
                          ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH") *
                               I."TI_LE_CHUYEN_DOI"
                          END) AS NUMERIC), 2)        AS "SO_LUONG_TREN_SO"
         , SUM(IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT") AS "SO_TIEN_QUY_DOI_TREN_SO"
       FROM (

              SELECT
                R."MA_HANG_ID"
                , R."MA_HANG"
                , R."TEN_HANG"
                , R."DVT_ID"
                , R."TEN_DVT"
                , S.id AS "MA_KHO_ID"
                , S."MA_KHO"
                , S."TEN_KHO"
                , R."TI_LE_CHUYEN_DOI"
              FROM
                (
                  SELECT
                      II.id    AS "MA_HANG_ID"
                    , II."MA"  AS "MA_HANG"
                    , II."TEN" AS "TEN_HANG"
                    , U.id     AS "DVT_ID"
                    , U.name   AS "TEN_DVT"
                    , CASE WHEN %(STT_DVT)s = 0 OR 0 IS NULL
                    THEN 1
                      WHEN IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
                        THEN 1
                      WHEN IU."PHEP_TINH_CHUYEN_DOI" = 'PHEP_NHAN'
                        THEN 1 / coalesce(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                      ELSE coalesce(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                      END      AS "TI_LE_CHUYEN_DOI"
                  FROM danh_muc_vat_tu_hang_hoa AS II
                    LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IU ON II.id = IU."VAT_TU_HANG_HOA_ID"
                                                                               AND IU."STT" = 0
                    LEFT JOIN danh_muc_don_vi_tinh U ON ((0 IS NULL
                                                          OR %(STT_DVT)s = 0
                                                         )
                                                         AND II."DVT_CHINH_ID" = U.id
                                                        )
                                                        OR (%(STT_DVT)s IS NOT NULL
                                                            AND %(STT_DVT)s <> 0
                                                            AND IU."DVT_ID" = U.id
                                                        )
                  WHERE II."TINH_CHAT" NOT IN ('1', '2')
                        AND ((%(IsUseStockSeperate)s = TRUE AND (II."CHI_NHANH_ID" = %(CHI_NHANH_ID)s)) OR (%(IsUseStockSeperate)s = FALSE))
                ) AS R, danh_muc_kho AS S
              WHERE (S.id = %(KHO_ID)s OR %(KHO_ID)s = %(KHO_ID)s)
                    AND ((%(IsUseStockSeperate)s = TRUE AND S."CHI_NHANH_ID" = 81) OR (%(IsUseStockSeperate)s = FALSE))
                    /* nhyen_18/5/2017_cr12832: lọc dữ liệu theo tùy chọn dùng riêng dạnh mục kho*/
                    AND ((%(STT_DVT)s = 0) OR (%(STT_DVT)s <> 0 AND R."DVT_ID" IS NOT NULL))

            ) AS I
         INNER JOIN so_kho_chi_tiet AS IL ON I."MA_HANG_ID" = IL."MA_HANG_ID" AND I."MA_KHO_ID" = IL."KHO_ID"
       WHERE IL."NGAY_HACH_TOAN" <= %(DEN_NGAY)s
             AND (IL."KHO_ID" = %(KHO_ID)s OR %(KHO_ID)s = %(KHO_ID)s)
             AND IL."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
       GROUP BY I."MA_HANG_ID",
         I."MA_HANG",
         I."TEN_HANG",
         I."DVT_ID",
         I."TEN_DVT",
         I."MA_KHO_ID",
         I."MA_KHO",
         I."TEN_KHO",
         IL."SO_LO",
         IL."NGAY_HET_HAN"

     ) AS R ON I."MA_HANG_ID" = R."MA_HANG_ID" AND I."MA_KHO_ID" = R."MA_KHO_ID"
WHERE ((%(STT_DVT)s = 0 ) OR (%(STT_DVT)s <> 0 AND R."DVT_ID" IS NOT NULL ))
ORDER BY R."MA_HANG",
R."MA_KHO",
R."SO_LO"

        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'MA_HANG_ID': line.get('MA_HANG_ID', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT_ID': line.get('DVT_ID', ''),
                'MA_KHO_ID': line.get('MA_KHO_ID', ''),
                'SO_LUONG_TREN_SO': line.get('SO_LUONG_TREN_SO', ''),
                'SO_LUONG_KIEM_KE': line.get('SO_LUONG_KIEM_KE', ''),
                'SO_LUONG_CHENH_LECH': line.get('SO_LUONG_CHENH_LECH', ''),

                'MA_QUY_CACH_1': '',
                'MA_QUY_CACH_2': '',
                'MA_QUY_CACH_3': '',
                'MA_QUY_CACH_4': '',
                'MA_QUY_CACH_5': '',
                
            })
        
        return record


    

    
    


    