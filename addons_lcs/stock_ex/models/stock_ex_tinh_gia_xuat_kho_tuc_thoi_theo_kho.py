# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_TINH_GIA_XUAT_KHO_TUC_THOI_THEO_KHO(models.Model):
    _name = 'stock.ex.tinh.gia.xuat.kho.tuc.thoi.theo.kho'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='InventoryItemID')
    MA_DON_VI_TINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Mã đơn vị tính', help='UnitID')
    MA_DON_VI_TINH_CHINH_ID = fields.Char('danh.muc.don.vi.tinh', help='MainUnitID')
    TOAN_TU_QUY_DOI = fields.Selection([('NHAN', '*'),('CHIA', '/'),],string="Toán tử quy đổi",help = 'ExchangeRateOperator')
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỷ lệ chuyển đổi', help='ConvertRate')
    MA_KHO_ID = fields.Many2one('danh.muc.kho', string='Mã kho', help='StockID')
    THOI_GIAN_HOAT_DONG = fields.Datetime(string='Thời gian hoạt động', help='DateTimeAction')
    SO_LUONG_VAT_TU = fields.Float(string='Số lượng vật tư', help='Quantity', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA_DONG = fields.Float(string='Đơn giá dòng', help='PriceRow', digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN_DONG = fields.Float(string='Thành tiền dòng', help='AmountRow')
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo dvt chính', help='QuantityMainUnit', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo dvt chính', help='PriceMainUnit')
    THANH_TIEN_DONG_DVT_CHINH = fields.Float(string='Thành tiền dòng dvt chính', help='AmountRowMainUnit')
    SO_LUONG_TON_THEO_DVT_CHINH = fields.Float(string='Số lượng tồn theo dvt chính', help='RemainQuantityMainUnit', digits=decimal_precision.get_precision('SO_LUONG'))
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh ', help='BranchID')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description')
    STT = fields.Integer(string='STT', help='SortOrder')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='RefType')
    KHONG_CAP_NHAT_GIA_XUAT = fields.Boolean(string='Không cập nhật giá xuất', help='IsUnUpdateOutwardPrice')
    LAP_RAP_THAO_DO_ID = fields.Many2one('stock.ex.lap.rap.thao.do', string='Lắp ráp tháo dỡ', help='AssemblyRefID')
    KHONG_CAN_CAP_NHAT_GIA_XUAT = fields.Boolean(string='Không cần cập nhật giá xuất', help='IsNeedUpdatePrice')
    THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT = fields.Datetime(string='Thời gian cập nhật giá xuất gần nhất', help='LastTimeUpdatePrice')
    PHAN_BIET_GIA = fields.Integer(string='Phân biệt giá', help='UnitPriceMethod')
    ID_CHUNG_TU_XUAT_KHO = fields.Integer(string='Id chứng từ xuất kho ', help='OutwardRefID')
    MODEL_CHUNG_TU_XUAT_KHO = fields.Char(string='Model chứng từ xuất kho', help='Model chứng từ xuất kho')
    ID_CHUNG_TU_XUAT_KHO_CHI_TIET = fields.Integer(string='Id chứng từ xuất kho chi tiết', help='OutwardRefDetailID')
    MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET = fields.Char(string='Model chứng từ xuất kho chi tiết', help='Model chứng từ xuất kho chi tiết')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate')
    SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH = fields.Float(string='Số lượng tồn thực tế theo dvt chính', help='AccumQuantityMainUnit', digits=decimal_precision.get_precision('SO_LUONG'))
    TONG_GIA_TRI_LUY_KE_KHO = fields.Float(string='Tổng giá trị lũy kế kho', help='AccumAmountStock')
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='RefID')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ')
    ID_CHUNG_TU_CHI_TIET = fields.Integer(string='Id chứng từ chi tiết', help='RefDetailID')
    MODEL_CHUNG_TU_TIET = fields.Char(string='Model chứng từ tiết', help='Model chứng từ tiết')
    LOAI_HOAT_DONG_NHAP_XUAT = fields.Integer(string='Loại hoạt động nhập xuất', help='TypeActionInOut')
    HOAT_DONG_CHI_TIET = fields.Integer(string='Hoạt động chi tiết', help='ActionDetail')
    GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH = fields.Float(string='Gía trị kho sau hoạt động theo dvt chính', help='AmountStockAfterActionMainUnit')
    DON_GIA_XUAT_KHO_THEO_DVT_CHINH = fields.Float(string='Đơn giá xuất kho  theo dvt chính', help='PriceOutwardStockMainUnit')
    
    HANH_DONG_TREN_VAT_TU = fields.Integer(string='Hành động trên vật tư', help='ActionRowOnMaterial')
    IsCaculateByStock = fields.Boolean(string='IsCaculateByStock', help='IsCaculateByStock')
    name = fields.Char(string='name')


    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS CAP_NHAT_ROW_ORDER_CUA_VTHH_TRONG_1_CHI_NHANH_THEO_KHO( IN

            v_chi_nhanh_id INT ) --Proc_IN_UpdatePrice_Oward_IM_UpdateOrderRowBranch
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_ROW_ORDER_CUA_VTHH_TRONG_1_CHI_NHANH_THEO_KHO(IN

            v_chi_nhanh_id                    INT)

                RETURNS INT
            AS $$
            DECLARE
                v_chi_nhanh_id                    INT;

            BEGIN

                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A
			SET "HANH_DONG_TREN_VAT_TU" = B."ROW"
			FROM
				(SELECT
					 ROW_NUMBER()
					 OVER (
						 PARTITION BY "MA_KHO_ID","MA_HANG_ID"
						 ORDER BY "THOI_GIAN_HOAT_DONG", "STT" ) AS "ROW"
					 , "id"
                    ,"MA_KHO_ID"
					 , "MA_HANG_ID"
				 FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho

				 WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

				) B
			WHERE A.id = B.id

			;

            RETURN 0
            ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;



            """)


        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS ham_kiem_tra_gia_tri_ton_kho_trong_bang_stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho( IN v_chi_nhanh_id INT,
            v_ma_vat_tu_id INT,

            v_ma_kho_id INT,

            v_thoi_gian_lay_don_gia TIMESTAMP,

            dong_truoc INT

            ) --Proc_IN_UpdatePrice_Oward_IM_GetAmountQuantityAccumBefore
            ;

            CREATE OR REPLACE FUNCTION ham_kiem_tra_gia_tri_ton_kho_trong_bang_stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho(
                IN v_chi_nhanh_id          INT,
                   v_ma_vat_tu_id          INT,

                   v_ma_kho_id             INT,
                   v_thoi_gian_lay_don_gia TIMESTAMP,

                   dong_truoc              INT

            ) --Proc_IN_UpdatePrice_Oward_IM_GetAmountQuantityAccumBefore

                RETURNS INT
            AS $$
            DECLARE

                -----------------------------------

                id_hoat_dong                         INT;

                --@ID_Action

                tong_gia_tri_ton_luy_ke_truoc        DECIMAL(18, 4);

                --@AmountAccumBefore

                so_luong_theo_dvt_chinh_luy_ke_truoc DECIMAL(18, 4);

                --@QuantityMainUnitAccumBefore

                tong_gia_tri_ton_con_lai             DECIMAL(18, 4)
                ;

                -------------- Nhap kho ------------
                tong_gia_tri_nhap_kho_binh_thuong    DECIMAL(18, 4)
                ;

                tong_gia_tri_nhap_kho_chuyen_khoan   DECIMAL(18, 4)
                ;

                tong_gia_tri_nhap_kho                DECIMAL(18, 4)
                ;

                ------------- Xuat kho-----------
                tong_gia_tri_xuat_kho_binh_thuong    DECIMAL(18, 4)
                ;

                tong_gia_tri_xuat_kho_chuyen_khoan   DECIMAL(18, 4)
                ;

                tong_gia_tri_xuat_kho                DECIMAL(18, 4)
                ;

                ------------Số lượng---------------------
                tong_so_luong_ton_con_lai            DECIMAL(18, 4)
                ;

                -------------- Nhap kho ------------
                tong_so_luong_nhap_kho_binh_thuong   DECIMAL(18, 4)
                ;

                tong_so_luong_nhap_kho_chuyen_khoan  DECIMAL(18, 4)
                ;

                tong_so_luong_nhap_kho               DECIMAL(18, 4)
                ;

                ------------- Xuat kho-----------
                tong_so_luong_xuat_kho_binh_thuong   DECIMAL(18, 4)
                ;

                tong_so_luong_xuat_kho_chuyen_khoan  DECIMAL(18, 4)
                ;

                tong_so_luong_xuat_kho               DECIMAL(18, 4)
                ;


            BEGIN


                SELECT id
                INTO id_hoat_dong

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                      AND "MA_KHO_ID" = v_ma_kho_id
                      AND "MA_HANG_ID" = v_ma_vat_tu_id
                      AND "HANH_DONG_TREN_VAT_TU" = dong_truoc
                ;

                SELECT "TONG_GIA_TRI_LUY_KE_KHO"
                INTO tong_gia_tri_ton_luy_ke_truoc
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                      AND "MA_KHO_ID" = v_ma_kho_id
                      AND "MA_HANG_ID" = v_ma_vat_tu_id
                      AND "HANH_DONG_TREN_VAT_TU" = dong_truoc
                ;

                SELECT "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"
                INTO so_luong_theo_dvt_chinh_luy_ke_truoc
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                      AND "MA_KHO_ID" = v_ma_kho_id
                      AND "MA_HANG_ID" = v_ma_vat_tu_id
                      AND "HANH_DONG_TREN_VAT_TU" = dong_truoc
                ;


                IF (tong_gia_tri_ton_luy_ke_truoc IS NULL)
                   OR (so_luong_theo_dvt_chinh_luy_ke_truoc IS NULL)
                THEN -- 1.1

                    --- A. Tính phần giá trị tồn
                    -------------------- ton ---------
                    --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                    SELECT SUM(COALESCE("SO_TIEN_NHAP", 0))
                    INTO tong_gia_tri_nhap_kho_binh_thuong
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    ---------------
                    SELECT SUM(COALESCE("SO_TIEN_NHAP",
                                        0))
                    INTO tong_gia_tri_nhap_kho_chuyen_khoan
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND "LA_NHAP_KHO" = TRUE
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;


                    tong_gia_tri_nhap_kho = COALESCE(tong_gia_tri_nhap_kho_binh_thuong,
                                                     0)
                                            + COALESCE(tong_gia_tri_nhap_kho_chuyen_khoan, 0)
                    ;

                    -- Tong gia tri nhap kho


                    --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                    SELECT SUM(COALESCE("SO_TIEN_XUAT", 0))
                    INTO tong_gia_tri_xuat_kho_binh_thuong
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    -- xuat kho thong thuong

                    SELECT SUM(COALESCE("SO_TIEN_XUAT",
                                        0))
                    INTO tong_gia_tri_xuat_kho_chuyen_khoan
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND "LA_NHAP_KHO" = FALSE
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    -- xuat kho chuyen kho
                    -- Tong gia tri xuat kho
                    tong_gia_tri_xuat_kho = COALESCE(tong_gia_tri_xuat_kho_binh_thuong,
                                                     0)
                                            + COALESCE(tong_gia_tri_xuat_kho_chuyen_khoan, 0)
                    ;


                    -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                    tong_gia_tri_ton_con_lai = tong_gia_tri_nhap_kho
                                               - tong_gia_tri_xuat_kho
                    ;


                    -- B. Tính phấn số lượng tồn

                    -------------------- ton ---------


                    --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                    SELECT SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH",
                                        0))
                    INTO tong_so_luong_nhap_kho_binh_thuong
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    ------------------
                    SELECT SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH",
                                        0))
                    INTO tong_so_luong_nhap_kho_chuyen_khoan
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND "LA_NHAP_KHO" = TRUE
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    -- Tong so luong nhap kho
                    tong_so_luong_nhap_kho = COALESCE(tong_so_luong_nhap_kho_binh_thuong,
                                                      0)
                                             + COALESCE(tong_so_luong_nhap_kho_chuyen_khoan, 0)
                    ;

                    --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                    SELECT SUM(COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
                                        0))
                    INTO tong_so_luong_xuat_kho_binh_thuong
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    -- xuat kho thong thuong

                    SELECT SUM(COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
                                        0))
                    INTO tong_gia_tri_xuat_kho_chuyen_khoan
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND "LA_NHAP_KHO" = FALSE
                          AND "STT_LOAI_CHUNG_TU" < v_thoi_gian_lay_don_gia
                    ;

                    -- xuat kho chuyen kho

                    -- Tong so luong xuat kho
                    tong_so_luong_xuat_kho = COALESCE(tong_so_luong_xuat_kho_binh_thuong,
                                                      0)
                                             + COALESCE(tong_so_luong_xuat_kho_chuyen_khoan, 0)
                    ;

                    -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                    tong_so_luong_ton_con_lai = tong_so_luong_nhap_kho
                                                - tong_so_luong_xuat_kho
                    ;


                    --- Update giá trị tồn , khối lượng tồn vào stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho cho dòng trước RowMin

                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                    SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = tong_gia_tri_ton_con_lai,
                        "TONG_GIA_TRI_LUY_KE_KHO"                  = tong_gia_tri_ton_con_lai,
                        "SO_LUONG_TON_THEO_DVT_CHINH"              = tong_so_luong_ton_con_lai,
                        "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"      = tong_so_luong_ton_con_lai
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "MA_KHO_ID" = v_ma_kho_id
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "HANH_DONG_TREN_VAT_TU" = dong_truoc

                    ;


                END IF
                ;


                RETURN 0
                ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;
            """)


        self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO( IN  ID_CHUNG_TU_XUAT_KHO       INT  ) --Proc_IN_UpdatePrice_Oward_IM_TransferStock
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO( IN  ID_CHUNG_TU_XUAT_KHO       INT  )
                RETURNS INT
            AS $$
            DECLARE

                id_chung_tu_chi_tiet INT;

            BEGIN

                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho a
                SET "DON_GIA_THEO_DVT_CHINH"               = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA_DONG"                         = b."DON_GIA_DONG",
                    "THANH_TIEN_DONG_DVT_CHINH"            = b."THANH_TIEN_DONG_DVT_CHINH",
                    "THANH_TIEN_DONG"                      = b."THANH_TIEN_DONG",
                    "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b

                WHERE (a."ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet
                       AND a."LOAI_HOAT_DONG_NHAP_XUAT" = 1 -- nhập kho
                       AND a."HOAT_DONG_CHI_TIET" = 5 --- nhap chuyen kho
            )
                       AND
                       (

                           b."ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet
                           AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 2 -- xuất kho
                           AND b."HOAT_DONG_CHI_TIET" = 5 ---  chuyen kho

                       )
                       AND (a."ID_CHUNG_TU_CHI_TIET" = b."ID_CHUNG_TU_CHI_TIET")
                ;


            RETURN 0;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;

            """)


        self.env.cr.execute(""" 
			            DROP FUNCTION IF EXISTS CAP_NHAT_GIA_TRI_CUA_ROW_TRUOC_TINH_GIA_THEO_KHO( IN

             vat_tu_hang_hoa_id INT,

            kho_id INT,

            hang_dong_tren_vat_tu INT,

            chi_nhanh_id INT,

            tu_ngay_khong_co_thoi_gian TIMESTAMP,

            den_ngay_khong_thoi_gian TIMESTAMP ) --Proc_IN_UpdatePrice_Oward_IM
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_TRI_CUA_ROW_TRUOC_TINH_GIA_THEO_KHO(IN  
             vat_tu_hang_hoa_id INT,

            kho_id INT,

            hang_dong_tren_vat_tu INT,

            chi_nhanh_id INT,

            tu_ngay_khong_co_thoi_gian TIMESTAMP,

            den_ngay_khong_thoi_gian TIMESTAMP)
                RETURNS INT
            AS $$
            DECLARE ---Proc_IN_UpdatePrice_Oward_IM

                ------------------------------------------------------


                LOAI_HOAT_DONG_NHAP_XUAT                                     INT;

                THANH_TIEN_DONG_DVT_CHINH                                    DECIMAL(22, 8);

                GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO            DECIMAL(22, 8);

                GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH                     DECIMAL(22, 8);

                SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO                         DECIMAL(18, 4);

                DON_GIA_XUAT_KHO_THEO_DVT_CHINH                              DECIMAL(18, 4);

                DON_GIA_XUAT_KHO_THEO_DVT_CHINH_TRUOC_DO                     DECIMAL(18, 4);

                LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO                            INT;

                -- Loại action của dòng trước

                HOAT_DONG_CHI_TIET                                           INT;

                SO_LUONG_THEO_DVT_CHINH                                      DECIMAL(18, 4);

                -- So luong cua Row hien tai
                KHONG_CAP_NHAT_GIA_XUAT                                      BOOLEAN;

                -- =1 : cho phep tu nhap; =0: theo tinh toan , so lieu cua row hien tai
                LAP_RAP_THAO_DO_ID_XUAT                                      INT;

                ID_CHUNG_TU_XUAT_KHO                                         INT;

                ID_CHUNG_TU_XUAT_KHO_CHI_TIET                                INT;


                LOAI_CHUNG_TU                                                INT;

                LOAI_CHUNG_TU_TRUOC_DO                                       INT;

                -- "LOAI_CHUNG_TU" cua dong truoc

                PHAN_BIET_GIA                                                INT;

                -- =0: Giá nhập kho bán hàng trả lại lấy theo giá bán ban đầu; =0: giá nhập kho nhập tay

                --=================== 1.khai bao phan lam tron------
                PHAN_THAP_PHAN_DON_GIA                                       INT;

                PHAN_THAP_PHAN_SO_LUONG                                      INT;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI                               INT;

                ------ Khai báo dùng số tồn lũy kế ( có thể âm) ----
                SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO                 DECIMAL(22, 8);

                TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO                             DECIMAL(18, 4);

                ID_HOAT_DONG                                                 INT;

                IsCaculateByStock_truoc_do                                   BOOLEAN;

                IsCaculateByStock                                            BOOLEAN;

                thoi_gian_hoat_dong_crrRow                                   TIMESTAMP;


                thoi_gian_hoat_dong_crrRow_khong_thoi_gian                   TIMESTAMP;

                id_chung_tu_chi_tiet                                         INT;

                KHONG_CAP_NHAT_GIA_XUAT_TRUOC_DO                             BOOLEAN;

                hang_dong_tren_vat_tu_truoc_do                               INT;

                CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO BOOLEAN;

                CHO_PHEP_XUAT_QUA_SO_LUONG_TON                               BOOLEAN;

                tong_gia_tri_con_lai                                         DECIMAL(18, 4);

                tong_gia_tri_nhap_kho_thong_thuong                           DECIMAL(18, 4);

                tong_gia_tri_nhap_kho_chuyen_khoan                           DECIMAL(18, 4);

                tong_gia_tri_nhap_kho                                        DECIMAL(18, 4);

                tong_gia_tri_xuat_kho_thong_thuong                           DECIMAL(18, 4);

                tong_gia_tri_xuat_kho_chuyen_khoan                           DECIMAL(18, 4);

                tong_gia_tri_xuat_kho                                        DECIMAL(18, 4);

                tem                                                          INT;


            BEGIN


                hang_dong_tren_vat_tu_truoc_do = hang_dong_tren_vat_tu - 1
                ;


                LAP_RAP_THAO_DO_ID_XUAT = NULL
                ;

                ID_CHUNG_TU_XUAT_KHO = NULL
                ;

                -- Lưu "ID_CHUNG_TU" của chứng từ xuat kho bán hàng lúc đầu trong table IN"XUAT_KHO"
                ID_CHUNG_TU_XUAT_KHO_CHI_TIET = NULL
                ;


                -- =0: Giá nhập kho bán hàng trả lại lấy theo giá bán ban đầu; =0: giá nhập kho nhập tay
                PHAN_BIET_GIA = -1
                ;


                ---=================0. Phần OPTION ================

                ---=----0.1 Option cập nhật giá nhập kho hàng bàn trả lại
                SELECT value
                INTO CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO
                FROM ir_config_parameter
                WHERE key = 'he_thong.CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO'
                FETCH FIRST 1 ROW ONLY
                ;


                IF (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO IS NULL)
                THEN
                    CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = FALSE
                    ;
                END IF
                ;

                ---=----0.2 Option cho phép xuất quá tồn

                SELECT value
                INTO CHO_PHEP_XUAT_QUA_SO_LUONG_TON
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHO_PHEP_XUAT_QUA_SO_LUONG_TON'
                FETCH FIRST 1 ROW ONLY
                ;

                --===========================================================


                -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;

                IF (PHAN_THAP_PHAN_DON_GIA IS NULL)
                THEN
                    PHAN_THAP_PHAN_DON_GIA = 0
                    ;
                END IF
                ;

                -------------- 1.2 SET gia tri  from table SYSDBOption: Số số thap phan cho "SO_LUONG_VAT_TU"  ----

                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;

                IF (PHAN_THAP_PHAN_SO_LUONG IS NULL)
                THEN
                    PHAN_THAP_PHAN_SO_LUONG = 0
                    ;
                END IF
                ;

                -------------- 1.3 SET gia tri  from table SYSDBOption: Số số thap phan cho "SO_TIEN"  ----


                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;

                IF (PHAN_THAP_PHAN_SO_TIEN_QUY_DOI IS NULL)
                THEN
                    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI = 0
                    ;

                END IF
                ;

                --- lay gia tri row truoc do : Tong gia tri kho  --
                SELECT "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH"
                INTO GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;


                SELECT "SO_LUONG_TON_THEO_DVT_CHINH"
                INTO SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                SELECT "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"
                INTO SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                SELECT "TONG_GIA_TRI_LUY_KE_KHO"
                INTO TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                SELECT "LOAI_HOAT_DONG_NHAP_XUAT"
                INTO LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                SELECT COALESCE("IsCaculateByStock", TRUE)
                INTO IsCaculateByStock_truoc_do

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                SELECT "LOAI_CHUNG_TU"
                INTO LOAI_CHUNG_TU_TRUOC_DO

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                SELECT "KHONG_CAP_NHAT_GIA_XUAT"
                INTO KHONG_CAP_NHAT_GIA_XUAT_TRUOC_DO
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                ;

                -----------------

                GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO =
                COALESCE(GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                         0)
                ;

                SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO = COALESCE(SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO,
                                                                0)
                ;

                SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO,
                                                                        0)
                ;


                TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
                ;

                ---------------------------------------------------------

                SELECT "LOAI_HOAT_DONG_NHAP_XUAT"
                INTO LOAI_HOAT_DONG_NHAP_XUAT


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "HOAT_DONG_CHI_TIET"
                INTO HOAT_DONG_CHI_TIET


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;


                SELECT "KHONG_CAP_NHAT_GIA_XUAT"
                INTO KHONG_CAP_NHAT_GIA_XUAT


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "LOAI_CHUNG_TU"
                INTO LOAI_CHUNG_TU


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT id
                INTO ID_HOAT_DONG


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT COALESCE("IsCaculateByStock", TRUE)
                INTO IsCaculateByStock


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "THOI_GIAN_HOAT_DONG"
                INTO thoi_gian_hoat_dong_crrRow


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "ID_CHUNG_TU_CHI_TIET"
                INTO id_chung_tu_chi_tiet


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "NGAY_HACH_TOAN"
                INTO thoi_gian_hoat_dong_crrRow_khong_thoi_gian


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;


                SELECT "LAP_RAP_THAO_DO_ID"
                INTO LAP_RAP_THAO_DO_ID_XUAT


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "ID_CHUNG_TU_XUAT_KHO"
                INTO ID_CHUNG_TU_XUAT_KHO


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                INTO ID_CHUNG_TU_XUAT_KHO_CHI_TIET


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;

                SELECT "PHAN_BIET_GIA"
                INTO PHAN_BIET_GIA

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                      AND "MA_KHO_ID" = kho_id
                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                ;


                KHONG_CAP_NHAT_GIA_XUAT = COALESCE(KHONG_CAP_NHAT_GIA_XUAT, FALSE)
                ;


                --========================---------2. Nhap kho ------------------------------------------


                IF (LOAI_HOAT_DONG_NHAP_XUAT = 1)
                   AND (hang_dong_tren_vat_tu > 1)
                THEN
                    -- Nhap kho


                    ---- 2.2.1 Kiểm tra nếu là nhập kho của lắp ráp thành phẩm thì tính lại giá nhập
                    IF ((LAP_RAP_THAO_DO_ID_XUAT IS NOT NULL)
                        AND (LOAI_CHUNG_TU = 2011)
                    ) -- chi áp dụng đối với nhập kho thành phẩm lắp ráp, đỗi với tháo dỡ ko áp dụng
                    THEN

                        SELECT *
                        FROM CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_KO_THEO_KHO(LAP_RAP_THAO_DO_ID_XUAT)
                        ;
                    END IF
                    ;


                    --=========2.2.2  trường hợp nhập kho bán hàng trả lại : đơn giá lấy theo giá xuất bán ban đầu ===

                    IF (HOAT_DONG_CHI_TIET = 6)
                       AND (PHAN_BIET_GIA = 0)
                       AND (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = 1)
                       AND (ID_CHUNG_TU_XUAT_KHO IS NOT NULL)
                       AND (ID_CHUNG_TU_XUAT_KHO_CHI_TIET IS NOT NULL)
                    -- HOAT_DONG_CHI_TIET=6: Nhập kho bán hàng trả lại
                    THEN
                        /* bổ sung thêm tu_ngay_khong_co_thoi_gian, den_ngay_khong_thoi_gian  ngày  11.02.2017 sửa lỗi  34819 - Bình quân tức thời: Lỗi khi tính giá xuất kho giá của chứng từ xuất kho sau chứng từ bán trả lại không đúng trường hợp sửa giá của chứng từ bán trả lại*/
                        PERFORM *
                        FROM CAP_NHAT_GIA_NHAP_VTTP_HANG_BAN_TRA_LAI_TINH_GIA_KO_THEO_KHO(ID_CHUNG_TU_XUAT_KHO,
                                                                                          ID_CHUNG_TU_XUAT_KHO_CHI_TIET,
                                                                                          tu_ngay_khong_co_thoi_gian,
                                                                                          den_ngay_khong_thoi_gian)
                        ;
                    END IF
                    ;


                    ---======== 2.2.3 trường hợp nhập kho từ chuyển kho lấy theo giá trị xuất kho
                    IF (HOAT_DONG_CHI_TIET = 5)
                       AND (LOAI_CHUNG_TU = 2030
                            OR LOAI_CHUNG_TU = 2031
                            OR LOAI_CHUNG_TU = 2032
                       )
                    THEN
                        -- chuyển kho
                        /* 2030	Xuất kho kiêm vận chuyển nội bộ
                          2031	Xuất kho gửi bán đại lý
                          2032	Xuất chuyển kho nội bộ
                          */
                        PERFORM *
                        FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)
                        ;


                    END IF
                    ;

                    --===========================================

                    SELECT COALESCE("THANH_TIEN_DONG_DVT_CHINH", 0)
                    INTO THANH_TIEN_DONG_DVT_CHINH
                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                          AND "MA_KHO_ID" = kho_id
                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                    ;

                    ------
                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                    SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(cast((THANH_TIEN_DONG_DVT_CHINH
                                                                                 +
                                                                                 GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO)
                                                                                AS NUMERIC),
                                                                           PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                        "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(cast((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                                                 + "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                                                           PHAN_THAP_PHAN_SO_LUONG),
                        "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = CASE COALESCE(SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                                                   + "SO_LUONG_THEO_DVT_CHINH",
                                                                                   0)
                                                                     WHEN 0
                                                                         THEN 0
                                                                     ELSE ROUND(cast((THANH_TIEN_DONG_DVT_CHINH +
                                                                                      GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO)
                                                                                     / COALESCE(
                                                                                         SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO +
                                                                                         "SO_LUONG_THEO_DVT_CHINH", 1) AS NUMERIC),
                                                                                PHAN_THAP_PHAN_DON_GIA)
                                                                     END,
                        "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                          AND "MA_KHO_ID" = kho_id
                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                    ;


                END IF
                ;

                ------------------2.2 Nhập kho dòng đầu tiên-------------
                IF (LOAI_HOAT_DONG_NHAP_XUAT = 1)
                   AND (hang_dong_tren_vat_tu = 1)  -- Nhap kho dòng đầu tiên
                THEN
                    ---- 2.2.1 Kiểm tra nếu là nhập kho của lắp ráp thành phẩm thì tính lại giá nhập
                    IF (LAP_RAP_THAO_DO_ID_XUAT IS NOT NULL)
                       AND (LOAI_CHUNG_TU = 2011)
                    THEN
                        PERFORM *
                        FROM CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_THEO_KHO(LAP_RAP_THAO_DO_ID_XUAT)
                        ;

                    END IF
                    ;

                    --=========2.2.2  trường hợp nhập kho bán hàng trả lại  ===

                    IF (HOAT_DONG_CHI_TIET = 6)
                       AND (PHAN_BIET_GIA = 0) --  ("DON_GIA"Method =1): Là nhập giá bằng tay
                       AND (ID_CHUNG_TU_XUAT_KHO IS NOT NULL)
                       AND (ID_CHUNG_TU_XUAT_KHO_CHI_TIET IS NOT NULL)
                       AND (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = TRUE)
                    -- HOAT_DONG_CHI_TIET=6: Nhập kho bán hàng trả lại
                    THEN
                        /* bổ sung thêm tu_ngay_khong_co_thoi_gian, den_ngay_khong_thoi_gian  ngày  11.02.2017 sửa lỗi  34819 - Bình quân tức thời: Lỗi khi tính giá xuất kho giá của chứng từ xuất kho sau chứng từ bán trả lại không đúng trường hợp sửa giá của chứng từ bán trả lại*/
                        PERFORM *
                        FROM CAP_NHAT_GIA_NHAP_VTTP_HANG_BAN_TRA_LAI(ID_CHUNG_TU_XUAT_KHO,
                                                                     ID_CHUNG_TU_XUAT_KHO_CHI_TIET,
                                                                     tu_ngay_khong_co_thoi_gian,
                                                                     den_ngay_khong_thoi_gian)
                        ;
                    END IF
                    ;

                    ---======== 2.2.3 trường hợp nhập kho từ chuyển kho lấy theo giá trị xuất kho
                    IF (HOAT_DONG_CHI_TIET = 5)
                       AND (LOAI_CHUNG_TU = 2030
                            OR LOAI_CHUNG_TU = 2031
                            OR LOAI_CHUNG_TU = 2032
                       )
                    THEN
                        -- chuyển kho
                        /* 2030	Xuất kho kiêm vận chuyển nội bộ
                          2031	Xuất kho gửi bán đại lý
                          2032	Xuất chuyển kho nội bộ
                          */
                        PERFORM *
                        FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)
                        ;

                    END IF
                    ;

                    ------
                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                    SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(CAST(("THANH_TIEN_DONG_DVT_CHINH") AS NUMERIC),
                                                                           PHAN_THAP_PHAN_SO_TIEN_QUY_DOI), --"SO_LUONG_THEO_DVT_CHINH"*"DON_GIA_THEO_DVT_CHINH",
                        "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                                                           PHAN_THAP_PHAN_SO_LUONG),
                        "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = ROUND(CAST(("DON_GIA_THEO_DVT_CHINH") AS NUMERIC),
                                                                           PHAN_THAP_PHAN_DON_GIA),
                        "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                          AND "MA_KHO_ID" = kho_id
                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu


                    ;
                END IF
                ;


                --=======================================3. XUAT KHO  ===============================


                IF (KHONG_CAP_NHAT_GIA_XUAT = FALSE)   -- 2.1 truong hop xuat kho có tính giá
                THEN
                    IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
                       AND (hang_dong_tren_vat_tu > 1)  -- Xuat kho
                    THEN
                        SELECT "SO_LUONG_THEO_DVT_CHINH"
                        INTO SO_LUONG_THEO_DVT_CHINH
                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                              AND "MA_KHO_ID" = kho_id
                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                        ;

                        SO_LUONG_THEO_DVT_CHINH = COALESCE(SO_LUONG_THEO_DVT_CHINH,
                                                           0)
                        ;

                        --- check so luong Row hien tai va so luong ton kho ------
                        --


                        IF (SO_LUONG_THEO_DVT_CHINH < SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO)
                        THEN

                            tem = 0
                            ;


                        ELSE
                            IF (SO_LUONG_THEO_DVT_CHINH = SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO) -- truong hop xuat het luong ton
                            THEN
                                --- tinh gia xuat kho de update cho Nhap kho tuong ung
                                --- new code

                                IF (IsCaculateByStock = IsCaculateByStock_truoc_do)
                                THEN

                                    /* Old code:*/

                                    DON_GIA_XUAT_KHO_THEO_DVT_CHINH = TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                      / LAY_SO_THAP_PHAN_KHAC_KHONG(
                                                                          SO_LUONG_THEO_DVT_CHINH)


                                    /* End Old code*/


                                    ;

                                ELSE /* 2 row liền nhau khác loại - theo kho và ko theo kho */

                                    IF (IsCaculateByStock = TRUE)
                                    THEN
                                        PERFORM *
                                        FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_THEO_KHO(ID_HOAT_DONG,
                                                                                            DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                        ;

                                    ELSE /* không theo kho*/
                                        PERFORM *
                                        FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_KHONG_THEO_KHO(ID_HOAT_DONG,
                                                                                                  DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                        ;


                                    END IF
                                    ;
                                END IF
                                ;


                                ------------------------------- Nếu <0 thì cho giá về 0 ----

                                IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH < 0)
                                THEN
                                    DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
                                    ;


                                    --- end new code


                                    -- tinh gia tri ton , so luong ton . Don gia xuat kho = Gia tri ton/ So luong ton
                                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                    SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                        "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                        "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                        "THANH_TIEN_DONG"                          = CASE WHEN
                                            COALESCE(GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                                                     0) < 0
                                            THEN 0
                                                                                     ELSE GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
                                                                                     END,
                                        "THANH_TIEN_DONG_DVT_CHINH"                = CASE
                                                                                     WHEN COALESCE(
                                                                                              GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                                                                                              0) < 0
                                                                                         THEN 0
                                                                                     ELSE GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
                                                                                     END,
                                        "DON_GIA_THEO_DVT_CHINH"                   = CASE
                                                                                     WHEN COALESCE(
                                                                                              GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                                                                                              0) < 0
                                                                                         THEN 0
                                                                                     ELSE ROUND(
                                                                                         CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS
                                                                                              INT),
                                                                                         PHAN_THAP_PHAN_DON_GIA)
                                                                                     END,
                                        "DON_GIA_DONG"                             =
                                        CASE
                                        WHEN COALESCE(
                                                 GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                                                 0) < 0
                                            THEN 0
                                        ELSE
                                            ROUND(
                                                LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
                                                                                   "TOAN_TU_QUY_DOI",
                                                                                   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
                                                PHAN_THAP_PHAN_DON_GIA)
                                        END,
                                        "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
                                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                          AND "MA_KHO_ID" = kho_id
                                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                    ;

                                    IF (HOAT_DONG_CHI_TIET =
                                        5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                    THEN


                                        ----------- trường hợp chuyển kho ------
                                        PERFORM *
                                        FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)

                                        ;

                                    END IF
                                    ;

                                END IF
                                ;

                                /*
                                                          Xuất vượt quá tồn làm bên dưới
                              ---===========================================

                             */


                            ELSE
                                ---=============2.2  trường hợp xuất kho bán hàng theo giá trị tự nhập : KHONG_CAP_NHAT_GIA_XUAT=1
                                ---============ hoặc trường hợp xuất kho trả lại hàng mua ----------------


                                IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
                                   AND (hang_dong_tren_vat_tu > 1)  -- Xuat kho
                                THEN
                                    ---------- Trường hợp 'Không cập nhật giá xuất' trên grid chỉ xuất hiện với Xuất kho bán hàng thôi, các trường hợp khác không có
                                    ------ không update "DON_GIA_DONG",	"SO_TIEN"Row	,"SO_LUONG_THEO_DVT_CHINH",	"DON_GIA_THEO_DVT_CHINH"	,"SO_TIEN"Row"DVT_CHINH_DVC"
                                    --------Tính : "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH", "DON_GIA_XUAT_KHO_THEO_DVT_CHINH", "SO_LUONG_TON_THEO_DVT_CHINH"
                                    ----- update gia tri Tong Kho con lai , so luong con lai -------------
                                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                    SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(CAST((
                                                                                                    GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
                                                                                                    - "THANH_TIEN_DONG_DVT_CHINH")
                                                                                                AS
                                                                                                NUMERIC),
                                                                                           PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                        "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(
                                            CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                  - "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                            PHAN_THAP_PHAN_SO_LUONG),
                                        "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          =
                                        CASE
                                        WHEN (COALESCE(GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                                                       0)
                                              - COALESCE("THANH_TIEN_DONG_DVT_CHINH",
                                                         0)) < 0
                                            THEN 0
                                        ELSE

                                            ROUND((GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO - "THANH_TIEN_DONG_DVT_CHINH")
                                                  / LAY_SO_THAP_PHAN_KHAC_KHONG(SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                                                - "SO_LUONG_THEO_DVT_CHINH"),
                                                  PHAN_THAP_PHAN_DON_GIA) END,
                                        "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
                                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                          AND "MA_KHO_ID" = kho_id
                                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                    ;


                                END IF
                                ;


                            END IF
                            ;


                        END IF
                        ;

                    END IF
                    ;
                END IF
                ;


                --===================2.3 trường hợp xuất kho dòng đầu tiên ( ko có nhập vẫn xuất) ==========

                IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
                   AND (hang_dong_tren_vat_tu = 1)
                THEN
                    IF LOAI_CHUNG_TU NOT IN (3040, 3041, 2027, 3030, 3031)  /* Xuất kho thông thường - dòng đầu tiên - ko phải chứng từ giảm giá hàng mua
                                            3030	Hàng mua trả lại - Giảm trừ công nợ
                                3031	Hàng mua trả lại - Tiền mặt
                                            */
                    THEN

                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
                            "THANH_TIEN_DONG"                          = 0,
                            "DON_GIA_DONG"                             = 0,
                            "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                            "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                            "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                              AND "MA_KHO_ID" = kho_id
                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                        ;

                        ---============= NEW ADD===

                        /*hoant sửa lôi 33209 - Bình quân tức thời: Lỗi trên sổ chi tiết VTHH không lấy được thông tin tiền vốn và đơn giá vốn trên chứng từ chuyển kho trường hợp không nhập đơn giá bán, thành tiền*/
                        /* Update lại giá nhập của chứng từ chuyển kho tương ứng*/

                        IF HOAT_DONG_CHI_TIET = 5 -- chuyển kho
                        THEN
                            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                            SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
                                "THANH_TIEN_DONG"                          = 0,
                                "DON_GIA_DONG"                             = 0,
                                "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                                "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
                            WHERE
                                "ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet
                                AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                                AND "HOAT_DONG_CHI_TIET" = 5 --- nhap chuyen kho
                            ;

                        END IF
                        ;
                    ELSE /* Xuất kho dòng đầu tiên - giảm giá hàng mua*/


                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        SET
                            "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = "THANH_TIEN_DONG",

                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                              AND "MA_KHO_ID" = kho_id
                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                        ;


                    END IF
                    ;


                END IF
                ;

                --===================================================new code========================
                --=============================2.4 Trường hợp xuất kho quá tồn có Option "Cho phép xuất quá tồn'-----


                IF (KHONG_CAP_NHAT_GIA_XUAT = FALSE) /* truong hop xuat kho có tính giá */
                   AND (LOAI_HOAT_DONG_NHAP_XUAT = 2) /* loại xuất kho */
                   AND (hang_dong_tren_vat_tu > 1)  /* Xuat kho từ dòng thứ 2 trở đi  */

                THEN
                    ---======================
                    IF (CHO_PHEP_XUAT_QUA_SO_LUONG_TON = 1)  /*Option: Check Cho phép xuất quá tồn*/
                    THEN


                        IF (SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO <=
                            0) /*Xuất khi tồn SL trước đó <=0 thì ĐG xuất lấy =0 ,  TT =0*/
                        --UPDATE1 gia=0, TT =0
                        THEN

                            IF (TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO <= 0) /* Trường hợp giá trị tồn <=0*/
                            THEN

                                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
                                    "THANH_TIEN_DONG"                          = 0,
                                    "DON_GIA_DONG"                             = 0,
                                    "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                                    "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(
                                        CAST((GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO) AS NUMERIC),
                                        PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                    "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                                                             - "SO_LUONG_THEO_DVT_CHINH") AS
                                                                                            NUMERIC),
                                                                                       PHAN_THAP_PHAN_SO_LUONG),


                                    ---
                                    "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                    "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                      AND "MA_KHO_ID" = kho_id
                                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                ;

                                ---------------------
                                IF (HOAT_DONG_CHI_TIET =
                                    5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan
                                THEN


                                    -- cap nhap gia tri nhap chuyen kho tuong ung
                                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                    SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
                                        "DON_GIA_DONG"                             = 0,
                                        "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                                        "THANH_TIEN_DONG"                          = 0,
                                        "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                        "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                        "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                        "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                    WHERE "ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet
                                          AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                                          AND "HOAT_DONG_CHI_TIET" = 5 --- nhap chuyen kho

                                    ;
                                END IF
                                ;


                            ELSE /*
                                              NQDINH. 2017.01.07. Fix ID=30248: Bình quân tức thời: Lỗi không tính lại đơn giá khi giá trị tồn lớn hơn không và số lượng tồn nhỏ hơn không ;
                                              trường hợp giá trị tồn lũy kế trước đó >0, tính giá xuất = giá trị tồn trước đó chia cho số lượng xuất*/



                                ------ update lai gia xuat ---

                                IF (SO_LUONG_THEO_DVT_CHINH > 0)
                                THEN

                                    ------ update lai gia xuat ---
                                    DON_GIA_XUAT_KHO_THEO_DVT_CHINH = ROUND(
                                        CAST(ROUND(CAST((GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH) AS NUMERIC),
                                                   PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                                             / lay_so_thap_phan_khac_khong(ROUND(CAST((SO_LUONG_THEO_DVT_CHINH) AS NUMERIC),
                                                                                 PHAN_THAP_PHAN_SO_LUONG)) AS NUMERIC),
                                        PHAN_THAP_PHAN_DON_GIA)
                                    ;


                                ELSE /* SO_LUONG_THEO_DVT_CHINH =0;TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO >0 */
                                    DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
                                    ;
                                END IF
                                ;


                                --- Nếu giá xuất âm thì cho về 0
                                IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH < 0)
                                THEN
                                    DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
                                    ;

                                    ----================================
                                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                    SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                                         PHAN_THAP_PHAN_DON_GIA),
                                        "DON_GIA_DONG"           = ROUND(
                                            LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
                                                                               "TOAN_TU_QUY_DOI",
                                                                               "TY_LE_CHUYEN_DOI") AS NUMERIC)),
                                            PHAN_THAP_PHAN_DON_GIA)
                                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                          AND "MA_KHO_ID" = kho_id
                                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                    ;


                                    ----- update gia tri Tong Kho con lai , so luong con lai -------------
                                    IF (GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO >= 0)

                                    THEN
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET --- NQDINH. Update trường hợp xuất số lượng =0; Fix ID=30248
                                            "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = (CASE
                                                                                          WHEN (DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0)
                                                                                              THEN GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO /* Trường hợp xuất SL>0
                                                                                      thì giá trị hết*/
                                                                                          ELSE 0
                                                                                          END),
                                            "THANH_TIEN_DONG_DVT_CHINH"                = (CASE
                                                                                          WHEN (DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0)
                                                                                              THEN 0
                                                                                          ELSE (ROUND(CAST((
                                                                                                               GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO)
                                                                                                           AS NUMERIC),
                                                                                                      PHAN_THAP_PHAN_SO_TIEN_QUY_DOI))
                                                                                          END),
                                            "THANH_TIEN_DONG"                          = (CASE WHEN (DON_GIA_XUAT_KHO_THEO_DVT_CHINH
                                                                                                     =
                                                                                                     0)
                                                THEN 0
                                                                                          ELSE (ROUND(CAST((
                                                                                                               GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO)
                                                                                                           AS NUMERIC),
                                                                                                      PHAN_THAP_PHAN_SO_TIEN_QUY_DOI))
                                                                                          END),


                                            ------------------------------
                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(
                                                CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                      - "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_LUONG),
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                        ;

                                    ELSE

                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET
                                            "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
                                            "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                                            "THANH_TIEN_DONG"                          = 0,


                                            ------------------------------
                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(
                                                CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                      - "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_LUONG),
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                        ;
                                    END IF
                                    ;

                                END IF
                                ;


                                IF (HOAT_DONG_CHI_TIET =
                                    5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                THEN


                                    ----------- trường hợp chuyển kho ------
                                    PERFORM *
                                    FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)
                                    ;


                                END IF
                                ;


                                /* end of */





                                /* end of: "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH"_before <= 0*/



                                --============================================================
                                IF (SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO > 0)
                                THEN
                                    IF (SO_LUONG_THEO_DVT_CHINH < SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO)
                                    THEN

                                        IF (IsCaculateByStock = IsCaculateByStock_truoc_do)
                                        THEN
                                            --- NQDINH.Fix ID=30248 . Date 2017.01.13 ; Bình quân tức thời: Lỗi không tính lại đơn giá khi giá trị tồn lớn hơn không và số lượng tồn nhỏ hơn không
                                            /* Old code:*/
                                            IF (LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO = 1)  --  Dòng trước là Nhập kho
                                               OR (LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO = 2
                                                   AND LOAI_CHUNG_TU_TRUOC_DO IN (3040,
                                                                                  3041, 2027)
                                               )
                                               /* 3040	Hàng mua giảm giá - Giảm trừ công nợ ;3041	Hàng mua giảm giá - Tiền mặt ;2027	Xuất kho từ kiểm kê (Có điều chỉnh giá trị)*/
                                               /* Fix ID=35186 . Date 2017.02.14*/
                                               OR (LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO = 2
                                                   AND KHONG_CAP_NHAT_GIA_XUAT_TRUOC_DO =
                                                       1) -- Nếu dòng trước được tích chọn Ko cập nhật thì tính lại

                                            THEN
                                                DON_GIA_XUAT_KHO_THEO_DVT_CHINH = ROUND(CAST(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                                             / LAY_SO_THAP_PHAN_KHAC_KHONG(
                                                                                                 SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO)
                                                                                             AS NUMERIC),
                                                                                        PHAN_THAP_PHAN_DON_GIA)
                                                ;

                                            ELSE --Dòng trước là  xuất kho thì lấy luôn giá xuất của dòng trước

                                                SELECT DON_GIA_XUAT_KHO_THEO_DVT_CHINH =
                                                       "DON_GIA_THEO_DVT_CHINH" --  "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"
                                                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                                      AND "MA_KHO_ID" = kho_id
                                                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
                                                ;

                                                --                                     SELECT  @Log_UpdatePriceOnRow = N'Gia xuat thang 3 .2 = @ActionRowOnMaterial_before'
                                                --                                                     + CAST (@ActionRowOnMaterial_before AS NVARCHAR(50))


                                            END IF
                                            ;


                                            /* End Old code*/

                                        END IF
                                        ;

                                    ELSE /* 2 row liền nhau khác loại - theo kho và ko theo kho */

                                        IF (IsCaculateByStock = 1)
                                        THEN

                                            SELECT *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_THEO_KHO(ID_HOAT_DONG,
                                                                                                DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                            ;

                                        ELSE /* không theo kho*/
                                            SELECT *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_KHONG_THEO_KHO(ID_HOAT_DONG,
                                                                                                      DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                            ;


                                        END IF
                                        ;


                                        ------------------------------- Nếu <0 thì cho giá về 0 ----

                                        IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH < 0)
                                        THEN
                                            DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
                                            ;
                                        END IF
                                        ;


                                        --                             SELECT  @Log_UpdatePriceOnRow = N'Gia xuat thang 3 .1 = '
                                        --                                     + CAST (DON_GIA_XUAT_KHO_THEO_DVT_CHINH AS NVARCHAR(50))


                                        ----================================
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                                             PHAN_THAP_PHAN_DON_GIA),
                                            "DON_GIA_DONG"           = ROUND(
                                                LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
                                                                                   "TOAN_TU_QUY_DOI",
                                                                                   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
                                                PHAN_THAP_PHAN_DON_GIA)
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                        ;


                                        --======================== tinh tong gia tri Row -------------------

                                        SELECT ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH"
                                                           * DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS
                                                          NUMERIC),
                                                     PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                                        INTO THANH_TIEN_DONG_DVT_CHINH
                                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;


                                        ----- update gia tri Tong Kho con lai , so luong con lai -------------
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(CAST((
                                                                                                        GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
                                                                                                        - THANH_TIEN_DONG_DVT_CHINH)
                                                                                                    AS NUMERIC),
                                                                                               PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "THANH_TIEN_DONG_DVT_CHINH"                = ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH"
                                                                                                     * "DON_GIA_THEO_DVT_CHINH") AS
                                                                                                    NUMERIC),
                                                                                               PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "THANH_TIEN_DONG"                          = ROUND(
                                                CAST(("SO_LUONG_VAT_TU" * "DON_GIA_DONG") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(
                                                CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                      - "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_LUONG),
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = ROUND(
                                                CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                PHAN_THAP_PHAN_DON_GIA),
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;


                                        IF (HOAT_DONG_CHI_TIET =
                                            5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                        THEN


                                            ----------- trường hợp chuyển kho ------
                                            PERFORM *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)

                                            ;


                                        END IF
                                        ;
                                    END IF
                                    ;


                                ELSE /*Xuất quá tồn lần đầu: SO_LUONG_THEO_DVT_CHINH >=  SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO )*/


                                    --- New code =============================================================
                                    IF (IsCaculateByStock = IsCaculateByStock_truoc_do)
                                    THEN
                                        DON_GIA_XUAT_KHO_THEO_DVT_CHINH = TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                          / LAY_SO_THAP_PHAN_KHAC_KHONG(
                                                                              SO_LUONG_THEO_DVT_CHINH)
                                        ;


                                    ELSE /* 2 row liền nhau khác loại - theo kho và ko theo kho */

                                        IF (IsCaculateByStock = 1)
                                        THEN
                                            SELECT *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_THEO_KHO(ID_HOAT_DONG,
                                                                                                DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                            ;

                                        ELSE /* không theo kho*/
                                            SELECT *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_KHONG_THEO_KHO(ID_HOAT_DONG,
                                                                                                      DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                            ;


                                        END IF
                                        ;


                                        ------------------------------- Nếu <0 thì cho giá về 0 ----

                                        IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH < 0)
                                        THEN

                                            DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
                                            ;
                                        END IF
                                        ;
                                    END IF
                                    ;

                                    --
                                    --                       SELECT  @Log_UpdatePriceOnRow = N'Gia xuat thang 3 .4 = '
                                    --                                     + CAST (DON_GIA_XUAT_KHO_THEO_DVT_CHINH AS NVARCHAR(50))
                                    ----================================
                                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                    SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                                         PHAN_THAP_PHAN_DON_GIA),
                                        "DON_GIA_DONG"           = ROUND(
                                            LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
                                                                               "TOAN_TU_QUY_DOI",
                                                                               "TY_LE_CHUYEN_DOI") AS NUMERIC)),
                                            PHAN_THAP_PHAN_DON_GIA)
                                    WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                          AND "MA_KHO_ID" = kho_id
                                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                          AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                    ;


                                    ----- update gia tri Tong Kho con lai , so luong con lai -------------

                                    IF (GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH >= 0)
                                    THEN


                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                            /*Sửa lỗi 33768*/
                                            "THANH_TIEN_DONG_DVT_CHINH"                = CASE WHEN DON_GIA_XUAT_KHO_THEO_DVT_CHINH =
                                                                                                   0
                                                THEN 0
                                                                                         ELSE ROUND(CAST((
                                                                                                             TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO)
                                                                                                         AS NUMERIC),
                                                                                                    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                                                                                         END,
                                            /* Không tính "SO_TIEN"Row"DVT_CHINH_DVC" ="DON_GIA_THEO_DVT_CHINH"x"SO_LUONG_THEO_DVT_CHINH"
                                            Vì giá trị khi làm tròn sẽ dẫn đến sai
                                             */
                                            /*  "SO_TIEN"Row"DVT_CHINH_DVC" = ROUND("DON_GIA_THEO_DVT_CHINH"
                                                                       * "SO_LUONG_THEO_DVT_CHINH",
                                                                       PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) ,*/
                                            "THANH_TIEN_DONG"                          = CASE WHEN DON_GIA_XUAT_KHO_THEO_DVT_CHINH =
                                                                                                   0
                                                THEN 0
                                                                                         ELSE ROUND(CAST((
                                                                                                             TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO)
                                                                                                         AS NUMERIC),
                                                                                                    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                                                                                         END,
                                            /* "SO_TIEN"Row = ROUND("DON_GIA_DONG" * "SO_LUONG_VAT_TU",
                                                               PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) , */
                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;
                                    ELSE
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH,

                                            "THANH_TIEN_DONG_DVT_CHINH"                = 0,

                                            "THANH_TIEN_DONG"                          = 0,

                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                                          - "SO_LUONG_THEO_DVT_CHINH") AS INT),
                                                                          PHAN_THAP_PHAN_SO_LUONG),
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                              AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;
                                    END IF
                                    ;


                                    IF (HOAT_DONG_CHI_TIET =
                                        5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                    THEN


                                        ----------- trường hợp chuyển kho ------
                                        PERFORM *
                                        FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)

                                        ;


                                    END IF
                                    ;

                                END IF
                                ;

                                /* end of */


                            END IF
                            ;

                            /* end of: CHO_PHEP_XUAT_QUA_SO_LUONG_TON = 1*/
                        ELSE

                            /*Option: Không Check Cho phép xuất quá tồn*/


                            IF (SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO <=
                                0) /*Xuất khi tồn SL trước đó <=0 thì ĐG xuất lấy =0 ,  TT =0*/
                            --UPDATE1 gia=0, TT =0
                            THEN
                                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
                                    "THANH_TIEN_DONG"                          = 0,
                                    "DON_GIA_DONG"                             = 0,
                                    "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                                    "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                    "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                    "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                    "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                     AND "MA_KHO_ID" = kho_id
                                      AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                      AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                ;

                                ---------------------
                                IF (HOAT_DONG_CHI_TIET =
                                    5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                THEN


                                    -- cap nhap gia tri nhap chuyen kho tuong ung
                                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                    SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
                                        "DON_GIA_DONG"                             = 0,
                                        "THANH_TIEN_DONG_DVT_CHINH"                = 0,
                                        "THANH_TIEN_DONG"                          = 0,
                                        "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                        "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                        "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                        "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                    WHERE "ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet
                                          AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                                          AND "HOAT_DONG_CHI_TIET" = 5
                                    ;

                                    --- nhap chuyen kho

                                    ---------------------------
                                END IF
                                ;

                            END IF
                            ;

                            /* end of: "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH"_before <= 0*/

                            IF (SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO > 0)
                            THEN
                                IF (SO_LUONG_THEO_DVT_CHINH < SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO)
                                THEN

            --                         SELECT  @Log_UpdatePriceOnRow = N'Gia xuat thang 3 .10 = '
            --                                     + CAST (DON_GIA_XUAT_KHO_THEO_DVT_CHINH AS NVARCHAR(50))
                                    IF (IsCaculateByStock = IsCaculateByStock_truoc_do)
                                    THEN
                                        /* Old code: */

                                        IF (LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO = 1)  --  Dòng trước là Nhập kho
                                           OR (LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO = 2
                                               AND LOAI_CHUNG_TU_TRUOC_DO IN (3040,
                                                                              3041, 2027)
                                           )
                                           /* 3040	Hàng mua giảm giá - Giảm trừ công nợ ;3041	Hàng mua giảm giá - Tiền mặt;2027	Xuất kho từ kiểm kê (Có điều chỉnh giá trị)
                            */
                                           /* Fix ID=35186 . Date 2017.02.14*/
                                           OR (LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO = 2
                                               AND KHONG_CAP_NHAT_GIA_XUAT_TRUOC_DO =
                                                   1) -- Nếu dòng trước được tích chọn Ko cập nhật thì tính lại

                                        THEN
                                            DON_GIA_XUAT_KHO_THEO_DVT_CHINH = ROUND(CAST(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                                         / LAY_SO_THAP_PHAN_KHAC_KHONG(
                                                                                             SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO)
                                                                                         AS NUMERIC),
                                                                                    PHAN_THAP_PHAN_DON_GIA)
                                            ;
                                        ELSE --Dòng trước là  xuất kho thì lấy luôn giá xuất của dòng trước
                                            SELECT DON_GIA_XUAT_KHO_THEO_DVT_CHINH =
                                                   "DON_GIA_THEO_DVT_CHINH" --"DON_GIA_XUAT_KHO_THEO_DVT_CHINH"
                                            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                            WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                                 AND "MA_KHO_ID" = kho_id
                                                  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                                  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do

                                            ;

                                            IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH=0 OR DON_GIA_XUAT_KHO_THEO_DVT_CHINH IS NULL	) AND TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO> 0 AND SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO>0
                                                THEN
                                                               DON_GIA_XUAT_KHO_THEO_DVT_CHINH = ROUND(CAST(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                          / lay_so_thap_phan_khac_khong(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO) AS NUMERIC),
                                                                          PHAN_THAP_PHAN_DON_GIA) ;

                                            END IF;


                                            /* End old code*/

                                        END IF
                                        ;

                                    ELSE /* 2 row liền nhau khác loại - theo kho và ko theo kho */

                                        IF (IsCaculateByStock = 1)
                                        THEN
                                            SELECT *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_THEO_KHO(ID_HOAT_DONG,
                                                                                                DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                            ;

                                        ELSE /* không theo kho*/
                                            SELECT *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_KHONG_THEO_KHO(ID_HOAT_DONG,
                                                                                                      DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                            ;


                                        END IF
                                        ;


                                        ------------------------------- Nếu <0 thì cho giá về 0 ----

                                        IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH < 0)
                                        THEN
                                            DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
                                            ;
                                        END IF
                                        ;

            --                             SELECT  @Log_UpdatePriceOnRow = N'Gia xuat thang 3 .2 = '
            --                                     + CAST (@PriceOutwardStockMainUnit AS NVARCHAR(50))

                                        ----================================
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "DON_GIA_THEO_DVT_CHINH" = ROUND(cast((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                                             PHAN_THAP_PHAN_DON_GIA),
                                            "DON_GIA_DONG"           = ROUND(
                                                LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
                                                                             "TOAN_TU_QUY_DOI",
                                                                             "TY_LE_CHUYEN_DOI"),
                                                PHAN_THAP_PHAN_DON_GIA)
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                             AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                        ;


                                        --======================== tinh tong gia tri Row -------------------

                                        SELECT ROUND(cast(("SO_LUONG_THEO_DVT_CHINH"
                                                           * DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                     PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                                        INTO THANH_TIEN_DONG_DVT_CHINH
                                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                             AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;


                                        ----- update gia tri Tong Kho con lai , so luong con lai -------------
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(cast((
                                                                                                        GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
                                                                                                        - THANH_TIEN_DONG_DVT_CHINH)
                                                                                                    AS
                                                                                                    NUMERIC),
                                                                                               PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "THANH_TIEN_DONG_DVT_CHINH"                = ROUND(cast(("SO_LUONG_THEO_DVT_CHINH"
                                                                                                     * "DON_GIA_THEO_DVT_CHINH") AS
                                                                                                    NUMERIC),
                                                                                               PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "THANH_TIEN_DONG"                          = ROUND(
                                                cast(("SO_LUONG_VAT_TU" * "DON_GIA_DONG") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(
                                                cast((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
                                                      - "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_LUONG),
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = ROUND(
                                                cast((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
                                                PHAN_THAP_PHAN_DON_GIA),
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                             AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;


                                        IF (HOAT_DONG_CHI_TIET =
                                            5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                        THEN


                                            ----------- trường hợp chuyển kho ------
                                            PERFORM *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)
                                            ;


                                        END IF
                                        ;


                                    END IF
                                    ;


                                ELSE
                                    IF (SO_LUONG_THEO_DVT_CHINH =
                                        SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO) /* Xuất hết tồn còn lại*/
                                    THEN
            --                             SELECT  @Log_UpdatePriceOnRow = N'Gia xuat thang 3 .11 = '
            --                                         + CAST (@PriceOutwardStockMainUnit AS NVARCHAR(50))

                                        DON_GIA_XUAT_KHO_THEO_DVT_CHINH = TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                          / LAY_SO_THAP_PHAN_KHAC_KHONG(SO_LUONG_THEO_DVT_CHINH)
                                        ;

                                        -- tinh gia tri ton , so luong ton . Don gia xuat kho = Gia tri ton/ So luong ton
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0
                                            , "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"        = 0
                                            , "SO_LUONG_TON_THEO_DVT_CHINH"            = 0
                                            , "THANH_TIEN_DONG"                        = CASE WHEN
                                            COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO,
                                                     0) < 0
                                            THEN 0
                                                                                         ELSE TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                                         END,
                                            "THANH_TIEN_DONG_DVT_CHINH"                = CASE
                                                                                         WHEN COALESCE(
                                                                                                  TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO,
                                                                                                  0) < 0
                                                                                             THEN 0
                                                                                         ELSE TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
                                                                                         END,
                                            "DON_GIA_THEO_DVT_CHINH"                   = CASE WHEN
                                                COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO,
                                                         0) < 0
                                                THEN 0
                                                                                         ELSE ROUND(
                                                                                             CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH)
                                                                                                  AS
                                                                                                  NUMERIC),
                                                                                             PHAN_THAP_PHAN_DON_GIA)
                                                                                         END,
                                            "DON_GIA_DONG"                             = CASE WHEN
                                                COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO,
                                                         0) < 0
                                                THEN 0
                                                                                         ELSE ROUND(
                                                                                             CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(
                                                                                                      DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
                                                                                                      "TOAN_TU_QUY_DOI",
                                                                                                      "TY_LE_CHUYEN_DOI") AS
                                                                                                  NUMERIC),
                                                                                             PHAN_THAP_PHAN_DON_GIA)
                                                                                         END,
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                               AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                                        ;

                                        IF (HOAT_DONG_CHI_TIET =
                                            5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
                                        THEN


                                            ----------- trường hợp chuyển kho ------
                                            PERFORM *
                                            FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_THEO_KHO(id_chung_tu_chi_tiet)

                                            ;

                                        END IF
                                        ;


                                    ELSE /*Xuất quá tồn lần đầu: SO_LUONG_THEO_DVT_CHINH >  "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH"_before )*/


                                        ----================================
                                        /* ko update lại giá xuất kho */


                                        ----- update gia tri Tong Kho con lai , so luong con lai -------------
                                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
                                            "THANH_TIEN_DONG_DVT_CHINH"                = ROUND(CAST(("DON_GIA_THEO_DVT_CHINH"
                                                                                                     * "SO_LUONG_THEO_DVT_CHINH") AS
                                                                                                    NUMERIC),
                                                                                               PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "THANH_TIEN_DONG"                          = ROUND(
                                                CAST(("DON_GIA_DONG" * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
                                            "SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
                                            "DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
                                            "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
                                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                               AND "MA_KHO_ID" = kho_id
                                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
                                        ;


                                        /* không thay đổi giá xuất kho điều chuyển  nên ko update giá nhập kho điều chuyển */


                                    END IF
                                    ;

                                    /* end of */


                                END IF
                                ;
                            END IF
                            ;
                        END IF
                        ;
                    END IF
                    ;
                END IF
                ;

                /* End of Option: ko Check Cho phép xuất quá tồn */


                --=========================3. Update giá trị tồn lũy kế thực tế  (có thể âm)===
                IF (IsCaculateByStock =
                    IsCaculateByStock_truoc_do) /* Trường hợp 2 row trước và row hiện tại cùng loai theo kho va ko theo kho*/
                THEN
                    IF (LOAI_HOAT_DONG_NHAP_XUAT = 1)
                    THEN
                        -- nhập kho
                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
                                                                    + "SO_LUONG_THEO_DVT_CHINH",
                            "TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
                                                                    + "THANH_TIEN_DONG_DVT_CHINH",
                            -- Update lại IsCaculateByStock ko theo kho
                            "IsCaculateByStock"                   = 0
                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                               AND "MA_KHO_ID" = kho_id
                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                        ;

                    ELSE
                        IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
                        THEN -- Xuất kho
                            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                            SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
                                                                        - "SO_LUONG_THEO_DVT_CHINH",
                                "TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
                                                                        - "THANH_TIEN_DONG_DVT_CHINH",
                                -- Update lại IsCaculateByStock ko theo kho
                                "IsCaculateByStock"                   = 0
                            WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                   AND "MA_KHO_ID" = kho_id
                                  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                            ;

                        END IF
                        ;
                    END IF
                    ;

                ELSE
                    /* Trường hợp  Row hiện tai và row trước không cùng tính theo kho hoặc cùng ko theo kho thì tính lại TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO từ ledger */

                    --- A. Tính phần giá trị tồn của dòng trước  từ "SO_CAI"
                    -------------------- ton ---------


                    --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                    SELECT SUM(COALESCE("SO_TIEN_NHAP", 0))
                    INTO tong_gia_tri_nhap_kho_thong_thuong
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id

                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                           AND "KHO_ID" = kho_id
                          AND (
                              "NGAY_HACH_TOAN" < thoi_gian_hoat_dong_crrRow_khong_thoi_gian
                              OR ("NGAY_HACH_TOAN" = thoi_gian_hoat_dong_crrRow_khong_thoi_gian AND
                                  "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow)
                          )
                    ;

                    ---------------
                    SELECT SUM(COALESCE("SO_TIEN_NHAP",
                                        0))
                    INTO tong_gia_tri_nhap_kho_chuyen_khoan
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id

                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND "LA_NHAP_KHO" = TRUE
                          AND "KHO_ID" = kho_id
                          AND (
                              "NGAY_HACH_TOAN" < thoi_gian_hoat_dong_crrRow_khong_thoi_gian
                              OR ("NGAY_HACH_TOAN" = thoi_gian_hoat_dong_crrRow_khong_thoi_gian AND
                                  "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow)
                          )
                    ;

                    tong_gia_tri_nhap_kho = COALESCE(tong_gia_tri_nhap_kho_thong_thuong,
                                                     0)
                                            + COALESCE(tong_gia_tri_nhap_kho_chuyen_khoan, 0)
                    ;

                    -- Tong gia tri nhap kho


                    --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                    SELECT SUM(COALESCE("SO_TIEN_XUAT", 0))
                    INTO tong_gia_tri_xuat_kho_thong_thuong
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id

                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                          AND "KHO_ID" = kho_id
                          AND (
                              "NGAY_HACH_TOAN" < thoi_gian_hoat_dong_crrRow_khong_thoi_gian
                              OR ("NGAY_HACH_TOAN" = thoi_gian_hoat_dong_crrRow_khong_thoi_gian AND
                                  "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow)
                          )
                    ;

                    SELECT SUM(COALESCE("SO_TIEN_XUAT",
                                        0))
                    INTO tong_gia_tri_xuat_kho_chuyen_khoan
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = chi_nhanh_id

                          AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND "LA_NHAP_KHO" = FALSE
                          AND "KHO_ID" = kho_id
                          AND (
                              "NGAY_HACH_TOAN" < thoi_gian_hoat_dong_crrRow_khong_thoi_gian
                              OR ("NGAY_HACH_TOAN" = thoi_gian_hoat_dong_crrRow_khong_thoi_gian AND
                                  "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow)
                          )
                    ;


                    -- Tong gia tri xuat kho
                    tong_gia_tri_xuat_kho = COALESCE(tong_gia_tri_xuat_kho_thong_thuong,
                                                     0)
                                            + COALESCE(tong_gia_tri_xuat_kho_chuyen_khoan, 0)
                    ;


                    -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                    tong_gia_tri_con_lai = tong_gia_tri_nhap_kho
                                           - tong_gia_tri_xuat_kho
                    ;

                    TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO = tong_gia_tri_con_lai
                    ;

                    /* Gán giá trị TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO theo giá trị tính lại từ table so_kho_chi_tiet*/

                    -- Update lai Accum
                    IF (LOAI_HOAT_DONG_NHAP_XUAT = 1)
                    THEN -- nhập kho
                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
                                                                    + "SO_LUONG_THEO_DVT_CHINH",
                            "TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0) /*change */
                                                                    + "THANH_TIEN_DONG_DVT_CHINH",
                            -- Update lại IsCaculateByStock theo kho
                            "IsCaculateByStock"                   = TRUE
                        WHERE "CHI_NHANH_ID" = chi_nhanh_id
                             AND "MA_KHO_ID" = kho_id
                              AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                              AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                        ;

                    ELSE
                        IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
                        THEN -- Xuất kho
                            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                            SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
                                                                        - "SO_LUONG_THEO_DVT_CHINH",
                                "TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
                                                                        - "THANH_TIEN_DONG_DVT_CHINH",
                                -- Update lại IsCaculateByStock theo kho
                                "IsCaculateByStock"                   = TRUE
                            WHERE "CHI_NHANH_ID" = chi_nhanh_id
                                 AND "MA_KHO_ID" = kho_id
                                  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
                                  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

                            ;


                        END IF
                        ;
                    END IF
                    ;

                END IF
                ;



                RETURN 0
                ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;

            """)


        self.env.cr.execute(""" 
		        DROP FUNCTION IF EXISTS CAP_NHAT_TINH_GIA_THEO_KHO_CHO_VAT_TU_TRONG_1_CHI_NHANH_TU_NGAY_DEN_NGAY( IN
        DS_MA_VTHH VARCHAR,

        dau_phan_cach VARCHAR,

        v_chi_nhanh_id INT,

        v_tu_ngay TIMESTAMP,

        v_den_ngay TIMESTAMP ) --Proc_IN_UpdatePrice_Oward_IM_ListMaterialFromDateToDateInBranch
        ;

        CREATE OR REPLACE FUNCTION CAP_NHAT_TINH_GIA_THEO_KHO_CHO_VAT_TU_TRONG_1_CHI_NHANH_TU_NGAY_DEN_NGAY(IN
        DS_MA_VTHH     VARCHAR,

        dau_phan_cach  VARCHAR,

        v_chi_nhanh_id INT,

        v_tu_ngay      TIMESTAMP,

        v_den_ngay     TIMESTAMP)

            RETURNS INT
        AS $$
        DECLARE

            v_den_ngay                         TIMESTAMP;

            v_tu_ngay                          TIMESTAMP;


            v_chi_nhanh_id                     INT;

            v_tu_ngay_khong_thoi_gian          TIMESTAMP;

            --@FromDate_NoTime

            v_den_ngay_khong_thoi_gian         TIMESTAMP;


            v_ToDateTime_NextNoTime            TIMESTAMP;

            DS_MA_VTHH                         VARCHAR;

            --@ListInventoryItemID


            hang_dong_toi_thieu_tren_vat_lieu  INT;

            --@MinActionRowOnMaterial

            dau_phan_cach                      VARCHAR;

            --@SeparateCharacter

            dong_toi_thieu                     INT;

            --@RowMin

            iRow                               INT;

            --iRow

            InrefOrder                         TIMESTAMP;

            --@InrefOrder

            hang_truoc                         INT;

            --@RowBefore

            rec                                RECORD;

            rec_2                              RECORD;

            cap_nhat_lan_cuoi_hang_truoc       TIMESTAMP;

            --@LastUpdate_RowBefore

            id_chung_tu_chi_tiet_id_hang_truoc INT;

            --@RefDetailID_RowBefore


        BEGIN


            v_tu_ngay_khong_thoi_gian = lay_ngay_thang(v_tu_ngay)
            ;

            v_den_ngay_khong_thoi_gian = lay_ngay_thang(v_den_ngay)
            ;


            v_ToDateTime_NextNoTime = v_den_ngay + INTERVAL '1 day'
            ;

            v_ToDateTime_NextNoTime = lay_ngay_thang(v_ToDateTime_NextNoTime)
            ;


            DROP TABLE IF EXISTS TMP_VTHH_ID
            ;

            CREATE TEMP TABLE TMP_VTHH_ID

            (
                "ValueTemp" VARCHAR
            )
            ;

            INSERT INTO TMP_VTHH_ID
                SELECT DISTINCT value
                FROM chuyen_chuoi_thanh_bang(DS_MA_VTHH,
                                             dau_phan_cach)
            ;


            FOR rec IN


            SELECT
                  A."MA_HANG_ID" AS "MA_HANG_ID_TEMP"
                , A."MA_KHO_ID"  AS "MA_KHO_ID_TEMP"
            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A
                INNER JOIN TMP_VTHH_ID B ON A."MA_HANG_ID" = CAST(B."ValueTemp" AS INT)
            WHERE "CHI_NHANH_ID" = v_chi_nhanh_id


            GROUP BY
                A."MA_HANG_ID",
                A."MA_KHO_ID"


            LOOP

                hang_dong_toi_thieu_tren_vat_lieu = NULL
            ;

                SELECT MIN("HANH_DONG_TREN_VAT_TU")
                INTO hang_dong_toi_thieu_tren_vat_lieu
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                      AND "MA_HANG_ID" = rec."MA_HANG_ID_TEMP"
                      AND "MA_KHO_ID" = rec."MA_KHO_ID_TEMP"
                      AND "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" IS NULL
            ;

                IF (hang_dong_toi_thieu_tren_vat_lieu IS NOT NULL)
                THEN
                    UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                    SET "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = NULL
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "MA_HANG_ID" = rec."MA_HANG_ID_TEMP"
                          AND "MA_KHO_ID" = rec."MA_KHO_ID_TEMP"
                          AND "HANH_DONG_TREN_VAT_TU" >= hang_dong_toi_thieu_tren_vat_lieu

                    ;


                END IF
            ;

            END LOOP
            ;

            --=================2. Create table chứa RowMinUpdatePrice bắt đầu tính giá cho vật tư trong kho ====


            DROP TABLE IF EXISTS TMP_BANG_HANG_TON_KHO_TOI_THIEU
            ;

            CREATE TEMP TABLE TMP_BANG_HANG_TON_KHO_TOI_THIEU


            (
                "MA_HANG_ID"            INT,
                "MA_KHO_ID"             INT,
                "HANH_DONG_TREN_VAT_TU" INT
            )
            ;


            INSERT INTO TMP_BANG_HANG_TON_KHO_TOI_THIEU
                SELECT
                    "MA_HANG_ID"
                    , "MA_KHO_ID"
                    , MIN("HANH_DONG_TREN_VAT_TU") AS "HANH_DONG_TREN_VAT_TU"
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A
                    INNER JOIN TMP_VTHH_ID B ON A."MA_HANG_ID" = CAST(B."ValueTemp" AS INT)
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

                      AND (("THOI_GIAN_HOAT_DONG" >= v_tu_ngay_khong_thoi_gian
                            AND "THOI_GIAN_HOAT_DONG" < v_ToDateTime_NextNoTime)
                      )
                GROUP BY
                    "MA_HANG_ID",
                    "MA_KHO_ID"
            ;


            ---===================3. Tao cursor tren danh sach ID_VatTu,  ===============


            FOR rec_2 IN
            SELECT
                  "MA_HANG_ID" AS "MA_HANG_ID_TEMP"
                , "MA_KHO_ID"  AS "MA_KHO_ID_TEMP"
                , "HANH_DONG_TREN_VAT_TU"
            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A /*hoant 10.01.2017 chuyển thành inner join thay cho in*/
                INNER JOIN TMP_VTHH_ID B ON A."MA_HANG_ID" = cast(B."ValueTemp" AS INT)
            WHERE "CHI_NHANH_ID" = v_chi_nhanh_id


                  AND (("THOI_GIAN_HOAT_DONG" >= v_tu_ngay_khong_thoi_gian
                        AND "THOI_GIAN_HOAT_DONG" < v_ToDateTime_NextNoTime)


                  )
            ORDER BY "THOI_GIAN_HOAT_DONG" ASC,
                "STT" ASC,
                "LOAI_HOAT_DONG_NHAP_XUAT" DESC


            LOOP


                ---cap nhat gia cho mot vat tu kho=======

                --============== tinh gia lai cho 1 vat tu. trong 1 kho, tren 1 row ---

                BEGIN
                    SELECT "HANH_DONG_TREN_VAT_TU"
                    INTO dong_toi_thieu
                    FROM TMP_BANG_HANG_TON_KHO_TOI_THIEU
                    WHERE "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                          AND "MA_KHO_ID" = rec_2."MA_KHO_ID_TEMP"
                    ;

                    SELECT dong_toi_thieu = COALESCE(dong_toi_thieu, 0)
                    ;

                    -------------------
                    IF (iRow = dong_toi_thieu)
                       AND (dong_toi_thieu >= 2)
                    THEN

                        /* Cập nhập giá trị tồn, Số lượng tồn cho row trước  */

                        --------------------
                        SELECT "THOI_GIAN_HOAT_DONG"
                        INTO InrefOrder
                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        WHERE "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                              AND "CHI_NHANH_ID" = v_chi_nhanh_id
                              AND "MA_KHO_ID" = rec_2."MA_KHO_ID_TEMP"
                              AND "HANH_DONG_TREN_VAT_TU" = dong_toi_thieu
                        ;


                        hang_truoc = dong_toi_thieu - 1
                        ;

                        PERFORM *
                        FROM ham_kiem_tra_gia_tri_ton_kho_trong_bang_stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho(
                            v_chi_nhanh_id, rec_2."MA_HANG_ID_TEMP", rec_2."MA_KHO_ID_TEMP", InrefOrder, hang_truoc)
                        ;


                        SELECT "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"
                        INTO cap_nhat_lan_cuoi_hang_truoc

                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        WHERE
                            "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"

                            AND "MA_KHO_ID" = rec_2."MA_KHO_ID_TEMP"
                            AND "CHI_NHANH_ID" = v_chi_nhanh_id

                            AND "HANH_DONG_TREN_VAT_TU" = hang_truoc
                        ;

                        SELECT "ID_CHUNG_TU_CHI_TIET"
                        INTO id_chung_tu_chi_tiet_id_hang_truoc
                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                        WHERE
                            "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                            AND "CHI_NHANH_ID" = v_chi_nhanh_id
                            AND "MA_KHO_ID" = rec_2."MA_KHO_ID_TEMP"
                            AND "HANH_DONG_TREN_VAT_TU" = hang_truoc
                        ;


                        IF (cap_nhat_lan_cuoi_hang_truoc IS NULL) -- Lay gia tu "SO_CAI" sang
                        THEN
                            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho B1
                            SET

                                "DON_GIA_DONG"              = A."DON_GIA", --PriceRow
                                "THANH_TIEN_DONG"           = A."SO_TIEN_XUAT", --"SO_TIEN"Row
                                "DON_GIA_THEO_DVT_CHINH"    = A."DON_GIA_THEO_DVT_CHINH", --Price"DVT_CHINH_DVC"
                                "THANH_TIEN_DONG_DVT_CHINH" = A."SO_TIEN_XUAT" --	 "SO_TIEN"Row"DVT_CHINH_DVC"


                            FROM so_kho_chi_tiet A
                                INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho B
                                    ON A."CHI_TIET_ID" = B."ID_CHUNG_TU_CHI_TIET" AND
                                       A."CHI_TIET_MODEL" = B."MODEL_CHUNG_TU_TIET"
                            WHERE B."ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet_id_hang_truoc
                                  AND B."MA_KHO_ID" = rec_2."MA_KHO_ID_TEMP"
                                  AND B."MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                                  AND B."CHI_NHANH_ID" = v_chi_nhanh_id

                                  AND B."HANH_DONG_TREN_VAT_TU" = hang_truoc

                                  AND B."LOAI_HOAT_DONG_NHAP_XUAT" = 2 -- xuat kho
                                  AND B1.id = B.id
                            ;


                        END IF
                        ;
                    END IF
                    ;


                    ---=====================================

                    PERFORM *
                    FROM CAP_NHAT_GIA_TRI_CUA_ROW_TRUOC_TINH_GIA_THEO_KHO(rec_2."MA_HANG_ID_TEMP", rec_2."MA_KHO_ID_TEMP", iRow,
                                                                          v_chi_nhanh_id,
                                                                          v_tu_ngay_khong_thoi_gian,
                                                                          v_den_ngay_khong_thoi_gian)
                    ;

                    EXCEPTION WHEN OTHERS
                    THEN

                        INSERT INTO stock_ex_tinh_gia_von_ghi_log
                        (
                            "VAT_TU_HANG_HOA_ID",
                            "KHO_ID",
                            "HANH_DONG",
                            "LOI",
                            "THOI_GIAN",
                            "PHUONG_PHAP_TINH_GIA"

                        )
                        VALUES (
                            rec_2."MA_HANG_ID_TEMP",
                            rec_2."MA_KHO_ID_TEMP",
                            iRow,
                            cast('Error' AS VARCHAR(255)),
                            LOCALTIMESTAMP,
                            'BQTT_NoStock'

                        )

                        ;
                END
            ;


            END LOOP
            ;

            RETURN 0
            ;

        END
        ;
        $$ LANGUAGE PLpgSQL
        ;

            """)


        self.env.cr.execute(""" 
			        DROP FUNCTION IF EXISTS CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY( IN
        DS_MA_VTHH VARCHAR,

        dau_phan_cach VARCHAR,

        v_tu_ngay TIMESTAMP,

        v_den_ngay TIMESTAMP,

        v_chi_nhanh_id INT
        ) --Proc_IN_UpdatePrice_Oward_IM_FromTableCaculateToInLedgerFromToDateTimeListItemIDInBranch
        ;

        CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY(IN
        DS_MA_VTHH     VARCHAR,

        dau_phan_cach  VARCHAR,

        v_tu_ngay      TIMESTAMP,

        v_den_ngay     TIMESTAMP,

        v_chi_nhanh_id INT
        )

            RETURNS INT
        AS $$

        ---Proc_IN_UpdatePrice_Oward_IM_FromTableCaculateToInLedgerFromToDateTimeListItemIDInBranch
        DECLARE

            v_chi_nhanh_id  INT;

            v_tu_ngay       TIMESTAMP;

            v_den_ngay      TIMESTAMP;

            DS_MA_VTHH      VARCHAR;

            --DS_MA_VTHH

            tat_ca_vat_lieu BOOLEAN;

            dau_phan_cach   VARCHAR;

            --@SeparateCharacter


        BEGIN


            DROP TABLE IF EXISTS TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY
            ;

            CREATE TEMP TABLE TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY

            (
                "Value" VARCHAR
            )
            ;

            INSERT INTO TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY
                SELECT DISTINCT value
                FROM chuyen_chuoi_thanh_bang(DS_MA_VTHH,
                                             dau_phan_cach)
            ;


            IF (DS_MA_VTHH IS NULL)
            THEN
                DS_MA_VTHH = ''
                ;
            END IF
            ;


            -------------------1. Update MainPrice cua cac VT xuat kho thong thuong table so_kho_chi_tiet :
            -------------------- Hieu nang : 7 s cho 112.000 bản ghi
            --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table so_kho_chi_tiet: 1. Update MainPrice cua cac VT xuat kho thong thuong'


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 2
                      AND b."HOAT_DONG_CHI_TIET" = 4
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."KHONG_CAP_NHAT_GIA_XUAT" = FALSE AND a1.id = a.id
                ;


            ELSE -- tất cả VT chi nhánh

                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 2
                      AND b."HOAT_DONG_CHI_TIET" = 4
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."KHONG_CAP_NHAT_GIA_XUAT" = FALSE AND a1.id = a.id
                ;

            END IF
            ;

            -------------  2. Update MainPrice cho cac VT xuat kho dieu chuyen table so_kho_chi_tiet

            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table so_kho_chi_tiet: 2.Update MainPrice cho cac VT xuat kho dieu chuyen'


            IF (DS_MA_VTHH <> '')
            THEN

                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND a."LA_NHAP_KHO" = FALSE
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 2
                      AND b."HOAT_DONG_CHI_TIET" = 5
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a1.id = a.id
                ;

            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND a."LA_NHAP_KHO" = FALSE
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 2
                      AND b."HOAT_DONG_CHI_TIET" = 5
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a1.id = a.id
                ;
            END IF
            ;

            --
            --
            --
            -- ------------3.=======================================================================================
            -- ----  Update MainPrice cho cac VT nhap  kho dieu chuyen  table so_kho_chi_tiet : 47926 rows  ; 1 s
            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table so_kho_chi_tiet: 3.Update MainPrice cho cac VT nhap kho dieu chuyen'
            --
            --
            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND a."LA_NHAP_KHO" = TRUE
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                      AND b."HOAT_DONG_CHI_TIET" = 5
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a1.id = a.id
                ;

            ELSE -----tất cả VT chi nhánh
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND a."LA_NHAP_KHO" = TRUE
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                      AND b."HOAT_DONG_CHI_TIET" = 5
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a1.id = a.id
                ;
            END IF
            ;


            --
            --   -------------- 3.2 Nhap kho từ thành phẩm lắp ráp -------------------------------
            --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table so_kho_chi_tiet: 3.2 Nhap kho từ thành phẩm lắp ráp'


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND a."LA_NHAP_KHO" = TRUE
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND (a."CHUNG_TU_LAP_RAP_THAO_DO_ID" IS NOT NULL)
                      AND a1.id = a.id
                ;
            ELSE ---- tất cả VT chi nhánh
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                            a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                            a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND a."LA_NHAP_KHO" = TRUE
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND (a."CHUNG_TU_LAP_RAP_THAO_DO_ID" IS NOT NULL)
                      AND a1.id = a.id
                ;
            END IF
            ;

            -- ----------------------3.3 Nhập kho hàng bán trả lại ---
            --
            --  EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table so_kho_chi_tiet: 3.3 Nhập kho hàng bán trả lại'


            IF (DS_MA_VTHH <> '')
            THEN

                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA_DONG",
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '1'  /*Nhập kho*/
                      AND a."LA_NHAP_KHO" = TRUE  /*Nhập vào*/
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1   /* Nhập kho */
                      AND b."HOAT_DONG_CHI_TIET" = 6 /* =6: Nhập kho bán hàng trả lại*/

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND (a."ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                      AND (a."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                      AND b."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IN (SELECT "ID_CHUNG_TU_CHI_TIET"
                                                                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                                                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                                                                      AND "NGAY_HACH_TOAN" >= v_tu_ngay AND
                                                                      "NGAY_HACH_TOAN" <= v_den_ngay
                                                                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2 -- xuat kho
                )

                      AND a1.id = a.id
                ;

            ELSE -- tất cả VT chi nhánh

                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH", "DON_GIA" = b."DON_GIA_DONG",
                    "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho AS b ON
                                                                                     (a."CHI_TIET_ID" =
                                                                                      b."ID_CHUNG_TU_CHI_TIET" AND
                                                                                      a."CHI_TIET_MODEL" =
                                                                                      b."MODEL_CHUNG_TU_TIET")

                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '1'  /*Nhập kho*/
                      AND a."LA_NHAP_KHO" = TRUE  /*Nhập vào*/
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1   /* Nhập kho */
                      AND b."HOAT_DONG_CHI_TIET" = 6 /* =6: Nhập kho bán hàng trả lại*/
                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay AND a."NGAY_HACH_TOAN" <= v_den_ngay

                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id AND (a."ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                      AND (a."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                      AND b."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IN (SELECT "ID_CHUNG_TU_CHI_TIET"
                                                                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                                                                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                                                                      AND "NGAY_HACH_TOAN" >= v_tu_ngay AND
                                                                      "NGAY_HACH_TOAN" <= v_den_ngay
                                                                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2 -- xuat kho
                )

                      AND a1.id = a.id
                ;
            END IF
            ;


            -- ---========================== Sau khi update xong so_kho_chi_tiet thì mới đi update "CHI_PHI_CHUNG""SO_CAI" ====
            -- ---------------------4. Update cho table "CHI_PHI_CHUNG""SO_CAI" từ table so_kho_chi_tiet------------
            -- ----------------------4.1 Update Debit : Nợ ------
            --
            -- ----------------------4.1.1 Nhập kho  ------
            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": -4.1 Update Debit : Nợ  -- 4.1.1 Nhập kho '


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_NHAP",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
                        )


                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      /*SMESEVEN-2375*/
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND a1.id = a.id
                ;

            ELSE --- tất cả VT chi nhánh
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_NHAP",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND
                      a."MA_HANG_ID" IN (SELECT "MA_HANG_ID"
                                         FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho)
                      AND a1.id = a.id
                ;
            END IF
            ;


            --  ----------------------4.1.2 Chuyển kho - xuất kho ------
            --   EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": -4.1 Update Debit : Nợ  -- 4.1.2 Chuyển kho - xuất kho '


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_DOI_UNG_ID"
                        )


                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND b."LA_NHAP_KHO" = FALSE
                      AND
                      a."MA_HANG_ID" IN (SELECT "MA_HANG_ID"
                                         FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho)
                      AND a1.id = a.id
                ;

            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_DOI_UNG_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND b."LA_NHAP_KHO" = FALSE
                      /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/
                      AND a1.id = a.id
                ;
            END IF
            ;


            --  ----------------------4.1.3 Chuyển kho - nhập kho ------
            --  EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": -4.1 Update Debit : Nợ  -- 4.1.3 Chuyển kho - nhập kho '
            --
            --
            --
            --
            --
            --   ----------------------4.1.4 Xuất  kho  ----------------------
            --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": -4.1 Update Debit : Nợ  -- 4.1.4 Xuất  kho'


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_DOI_UNG_ID"
                        )


                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3' /*"LOAI_KHU_VUC_NHAP_XUAT" =3 : Xuất kho ;*/

                      AND
                      a."MA_HANG_ID" IN (SELECT "MA_HANG_ID"
                                         FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho)
                      AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE
                      AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_DOI_UNG_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3' /*"LOAI_KHU_VUC_NHAP_XUAT" =3 : Xuất kho ;*/

                      AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE
                      AND a1.id = a.id
                ;
            END IF
            ;


            --   --========================= 4.2 Update "GHI_CO" : Có =========================
            --   ----------------------------4.2.1 - Nhập kho ---------------
            --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": - 4.2 Update "GHI_CO" : Có  -- 4.2.1 - Nhập kho : INNER  JOIN '


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_NHAP",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_DOI_UNG_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_NHAP",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_DOI_UNG_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND a1.id = a.id
                ;
            END IF
            ;

            --     ----------------------------4.2.2 - Chuyển kho : Xuất  kho ---------------
            --         EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": - 4.2 Update "GHI_CO" : Có  -- 4.2.2 - Chuyển kho : Xuất  kho '


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_XUAT",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND b."LA_NHAP_KHO" = FALSE
                      /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/

                      AND a1.id = a.id
                ;

            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_XUAT",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND b."LA_NHAP_KHO" = FALSE
                      /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/
                      AND a1.id = a.id
                ;
            END IF
            ;

            --
            --       ----------------------------4.2.3 - Chuyển kho : nhập  kho ---------------
            --        EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": - 4.2 Update "GHI_CO" : Có  -- 4.2.3 - Chuyển kho : nhập  kho '
            --
            --
            --
            --
            --  ----------------------------------4.2.4 Xuất kho --------
            --   EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": - 4.2 Update "GHI_CO" : Có  --4.2.4 Xuất kho '


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_XUAT",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3'

                      AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE
                      AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_XUAT",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"
                                                        AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3'

                      AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE
                      AND a1.id = a.id
                ;

            END IF
            ;

            -- ---========================== 5. Sau khi update xong so_kho_chi_tiet thì mới đi update so_cong_no_chi_tiet  ====
            -- ---------------------5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet------------
            -- ----------------------5.1 Update Debit : Nợ ------
            -- ----------------------5.1.1 Nhập kho  ------
            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.1 Update Debit : Nợ  --5.1.1 Nhập kho '


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_NHAP",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND a1.id = a.id
                ;

            ELSE --- tất cả VT trong chi nhánh
                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_NHAP",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND a1.id = a.id
                ;
            END IF
            ;


            -- ----------------------5.1.2 Chuyển kho - xuất kho ------
            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.1 Update Debit : Nợ  -- 5.1.2 Chuyển kho - xuất kho'


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND b."LA_NHAP_KHO" = FALSE
                      /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/
                      AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh

                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND b."LA_NHAP_KHO" = FALSE
                      /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/
                      AND a1.id = a.id
                ;
            END IF
            ;

            --  ----------------------5.1.3 Chuyển kho - nhập kho ------
            --
            --  EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.1 Update Debit : Nợ  -- 5.1.3 Chuyển kho - nhập kho'

            --   ----------------------5.1.4 Xuất  kho  ----------------------
            --
            --   EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.1 Update Debit : Nợ  -- 5.1.4 Xuất  kho'


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND b."LA_NHAP_KHO" = FALSE
                      /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/
                      AND a1.id = a.id
                ;
            ELSE


                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_XUAT",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )


                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3'

                      AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE


                      AND a1.id = a.id
                ;
            END IF
            ;

            --
            --   --========================= 5.2 Update "GHI_CO" : Có =========================
            --   ----------------------------5.2.1 - Nhập kho ---------------
            --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  -- 5.2.1 - Nhập kho'


            IF (DS_MA_VTHH <> '')
            THEN
                UPDATE so_cong_no_chi_tiet a1
                SET
                    "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_NHAP",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )

                    INNER JOIN
                    TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                        ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1' /*"LOAI_KHU_VUC_NHAP_XUAT"=1: Nhập kho */

                      AND a1.id = a.id
                ;
            ELSE


                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_NHAP",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                        AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                        )


                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                      AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1' /*"LOAI_KHU_VUC_NHAP_XUAT"=1: Nhập kho */

                      AND a1.id = a.id
                ;

        END IF ;
                --     ----------------------------5.2.2 - Chuyển kho : Xuất  kho ---------------
                --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  -- 5.2.2 - Chuyển kho : Xuất  kho'

                IF (DS_MA_VTHH <> '')
                THEN


                    UPDATE so_cong_no_chi_tiet a1
                    SET "GHI_NO"                 = 0,
                        "GHI_CO"                 = b."SO_TIEN_XUAT",
                        "GHI_NO_NGUYEN_TE"       = 0,
                        "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                        "DON_GIA"                = b."DON_GIA",
                        "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                        "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                    FROM so_cong_no_chi_tiet AS a
                        INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                            AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                            )

                        INNER JOIN
                        TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                            ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND b."LA_NHAP_KHO" = FALSE
                          /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/

                          AND a1.id = a.id
                    ;

                ELSE
                    UPDATE so_cong_no_chi_tiet a1
                    SET "GHI_NO"                 = 0,
                        "GHI_CO"                 = b."SO_TIEN_XUAT",
                        "GHI_NO_NGUYEN_TE"       = 0,
                        "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                        "DON_GIA"                = b."DON_GIA",
                        "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                        "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                    FROM so_cong_no_chi_tiet AS a
                        INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                            AND b."TK_NO_ID" = a."TK_DOI_UNG_ID"
                            )

                        INNER JOIN
                        TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                            ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND b."LA_NHAP_KHO" = FALSE

                          AND a1.id = a.id
                    ;
                END IF
                ;

                --       ----------------------------5.2.3 - Chuyển kho : nhập  kho ---------------
                --       EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  --  5.2.3 - Chuyển kho : nhập  kho'

                --  ----------------------------------5.2.4 Xuất kho --------
                --   EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  --  5.2.4 Xuất kho'


                IF (DS_MA_VTHH <> '')
                THEN

                    UPDATE so_cong_no_chi_tiet a1
                    SET "GHI_NO"                 = 0,
                        "GHI_CO"                 = b."SO_TIEN_XUAT",
                        "GHI_NO_NGUYEN_TE"       = 0,
                        "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                        "DON_GIA"                = b."DON_GIA",
                        "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                        "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                    FROM so_cong_no_chi_tiet AS a
                        INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                            AND b."TK_NO_ID" = a."TK_ID"
                            )

                        INNER JOIN
                        TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_THEO_KHO_TU_NGAY_DEN_NGAY C
                            ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'  /* Ghi có */
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3' /*"LOAI_KHU_VUC_NHAP_XUAT" =3 : Xuất kho ;*/

                          AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE

                          AND a1.id = a.id
                    ;

                ELSE

                    UPDATE so_cong_no_chi_tiet a1
                    SET "GHI_NO"                 = 0,
                        "GHI_CO"                 = b."SO_TIEN_XUAT",
                        "GHI_NO_NGUYEN_TE"       = 0,
                        "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_XUAT",
                        "DON_GIA"                = b."DON_GIA",
                        "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                        "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                    FROM so_cong_no_chi_tiet AS a
                        INNER JOIN so_kho_chi_tiet AS b ON (a."CHI_TIET_ID" = b."CHI_TIET_ID"

                                                            AND b."TK_NO_ID" = a."TK_ID"
                            )


                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'  /* Ghi có */
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3' /*"LOAI_KHU_VUC_NHAP_XUAT" =3 : Xuất kho ;*/

                          AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE

                          AND a1.id = a.id ;

                END IF

                ;

                RETURN 0
                ;

            END
            ;

        $$ LANGUAGE PLpgSQL
        ;





            """)