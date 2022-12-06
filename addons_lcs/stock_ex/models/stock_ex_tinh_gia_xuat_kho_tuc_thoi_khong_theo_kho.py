# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_TINH_GIA_XUAT_KHO_TUC_THOI_KHONG_THEO_KHO(models.Model):
    _name = 'stock.ex.tinh.gia.xuat.kho.tuc.thoi.khong.theo.kho'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='InventoryItemID')
    MA_DON_VI_TINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Mã đơn vị tính', help='UnitID')
    MA_DON_VI_TINH_CHINH_ID = fields.Char('danh.muc.don.vi.tinh', help='MainUnitID')
    TOAN_TU_QUY_DOI = fields.Selection([('NHAN', '*'),('CHIA', '/'),],string="Toán tử quy đổi",help = 'ExchangeRateOperator')
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỷ lệ chuyển đổi', help='ConvertRate')
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
					DROP FUNCTION IF EXISTS LAY_NGAY_THANG( IN ngay VARCHAR(20) )
			;

			CREATE OR REPLACE FUNCTION LAY_NGAY_THANG(IN ngay TIMESTAMP)--Func_GetDateWithoutTime
				RETURNS TIMESTAMP AS $$


			DECLARE


			BEGIN

				RETURN CAST(
					CAST(EXTRACT(MONTH FROM ngay) AS VARCHAR(2)) || '/' || CAST(EXTRACT(DAY FROM ngay) AS VARCHAR(2)) || '/' ||
					CAST(EXTRACT(YEAR FROM ngay) AS VARCHAR(4)) AS TIMESTAMP)
				;


			END
			;

			$$ LANGUAGE PLpgSQL
			;

            """)

        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS LAY_SO_THAP_PHAN_KHAC_KHONG( IN GIA_TRI_DAU_VAO DECIMAL(22, 8) ) --Func_GetNumberDecimal_AvoidZero
			;

			CREATE OR REPLACE FUNCTION LAY_SO_THAP_PHAN_KHAC_KHONG(IN GIA_TRI_DAU_VAO DECIMAL(22, 8))
				RETURNS DECIMAL(22, 8)
			AS $$

			BEGIN
				IF (GIA_TRI_DAU_VAO IS NULL)
					THEN
				RETURN 1
				;
						END IF ;

				IF (GIA_TRI_DAU_VAO = 0)
					THEN
				RETURN 1
				;
						  END IF ;

				RETURN GIA_TRI_DAU_VAO
				;

			END
			;
			$$ LANGUAGE PLpgSQL
			;

            """)

        self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_DON_GIA_TU_DON_GIA_CHINH( IN DON_GIA_CHINH DECIMAL(22, 8), TOAN_TU_QUY_DOI VARCHAR(10), TY_LE_CHUYEN_DOI DECIMAL(22, 8) ) --Func_GetPriceUnit_FromPriceMainUnit
		;

		CREATE OR REPLACE FUNCTION LAY_DON_GIA_TU_DON_GIA_CHINH(IN DON_GIA_CHINH    DECIMAL(22, 8), TOAN_TU_QUY_DOI VARCHAR(10),
																   TY_LE_CHUYEN_DOI DECIMAL(22, 8))
			RETURNS DECIMAL(22, 8)
		AS $$
		DECLARE
			DON_GIA DECIMAL(22, 8);


		BEGIN
			SELECT CASE TOAN_TU_QUY_DOI
				   WHEN '*'
					   THEN DON_GIA_CHINH * TY_LE_CHUYEN_DOI
				   WHEN '/'
					   THEN DON_GIA_CHINH / lay_so_thap_phan_khac_khong(TY_LE_CHUYEN_DOI)


				   ELSE DON_GIA_CHINH END
			INTO DON_GIA
			;


			RETURN DON_GIA

		;

		END
		;
		$$ LANGUAGE PLpgSQL
		;
            """)

        self.env.cr.execute(""" 
	DROP FUNCTION IF EXISTS CHUYEN_CHUOI_THANH_BANG( IN v_ValueList VARCHAR,

		v_SeparateCharacter VARCHAR )
		;

		CREATE OR REPLACE FUNCTION CHUYEN_CHUOI_THANH_BANG(IN v_ValueList         VARCHAR,

														v_SeparateCharacter VARCHAR)--Func_ConvertStringIntoTable
		RETURNS TABLE(

		Value VARCHAR

		) AS $$



		DECLARE



		v_ValueListLength   INTEGER;

		v_StartingPosition  INTEGER;

		v_Value             VARCHAR;

		v_SecondPosition    INTEGER;


		BEGIN


		DROP TABLE IF EXISTS tt_VALUETABLE CASCADE;
		CREATE TEMPORARY TABLE tt_VALUETABLE
		(
		Value VARCHAR
		);



		--nvtoan modify 25/11/2015: Chuy?n do?n l?y leng c?a valuelist xu?ng du?i s?a l?i chu?i truy?n vào không có seperator thì không l?y du?c giá tr?
		--SET @ValueListLength = LEN(@ValueList)
		v_StartingPosition := 1;
		v_Value := REPEAT(' ',0);

		IF SUBSTR(v_ValueList,1,1) <> v_SeparateCharacter then
		v_ValueList := coalesce(v_SeparateCharacter,'') || coalesce(v_ValueList,'');
		end if;
		v_ValueListLength := LENGTH(v_ValueList);

		IF SUBSTR(v_ValueList,v_ValueListLength::INT -1,v_ValueListLength) <> v_SeparateCharacter then
		v_ValueList := coalesce(v_ValueList,'') || coalesce(v_SeparateCharacter,'');
		end if;



		-- Duy?t chu?i c?n chuy?n và b?ng
		WHILE v_StartingPosition < v_ValueListLength LOOP
			-- V? trí k? ti?p xu?t hi?n ký t? phân cách
		v_SecondPosition := CASE WHEN POSITION(v_SeparateCharacter IN SUBSTR(v_ValueList,v_StartingPosition::INT+1)) > 0 THEN POSITION(v_SeparateCharacter IN SUBSTR(v_ValueList,v_StartingPosition::INT+1))+v_StartingPosition::INT+1 -1 ELSE 0 END;
			-- Trích ra giá tr? t? chu?i
		v_Value := SUBSTR(v_ValueList,v_StartingPosition::INT+1,v_SecondPosition::INT -v_StartingPosition::INT -1);
			-- Thi?t l?p l?i giá tr? b?t d?u
		v_StartingPosition := v_SecondPosition;
		IF v_Value <> REPEAT(' ',0) then
			INSERT  INTO tt_VALUETABLE(Value)
					VALUES(LTRIM(RTRIM(v_Value)));
		end if;
		END LOOP;


		RETURN QUERY SELECT *
					FROM tt_VALUETABLE
		;

		END
		;

		$$ LANGUAGE PLpgSQL
		;


			""")



        self.env.cr.execute(""" 
	                DROP FUNCTION IF EXISTS ham_kiem_tra_gia_tri_ton_kho_trong_bang_stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho( IN v_chi_nhanh_id INT ,
                v_ma_vat_tu_id INT ,
    
                v_thoi_gian_lay_don_gia TIMESTAMP ,
    
    
                dong_truoc INT
    
                ) --Proc_IN_UpdatePriceOW_NoStock_IM_GetAmountQuantityAccumBefore
                ;
    
                CREATE OR REPLACE FUNCTION ham_kiem_tra_gia_tri_ton_kho_trong_bang_stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho( IN v_chi_nhanh_id INT ,
                v_ma_vat_tu_id INT ,
    
                v_thoi_gian_lay_don_gia TIMESTAMP ,
    
    
                dong_truoc INT
    
                ) --Proc_IN_UpdatePriceOW_NoStock_IM_GetAmountQuantityAccumBefore
    
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
    
                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
    
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "HANH_DONG_TREN_VAT_TU" = dong_truoc
                    ;
    
                    SELECT "TONG_GIA_TRI_LUY_KE_KHO"
                    INTO tong_gia_tri_ton_luy_ke_truoc
                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
    
                          AND "MA_HANG_ID" = v_ma_vat_tu_id
                          AND "HANH_DONG_TREN_VAT_TU" = dong_truoc
                    ;
    
                    SELECT "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"
                    INTO so_luong_theo_dvt_chinh_luy_ke_truoc
                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
    
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
    
    
                        --- Update giá trị tồn , khối lượng tồn vào stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho cho dòng trước RowMin
    
                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                        SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = tong_gia_tri_ton_con_lai,
                            "TONG_GIA_TRI_LUY_KE_KHO"                  = tong_gia_tri_ton_con_lai,
                            "SO_LUONG_TON_THEO_DVT_CHINH"              = tong_so_luong_ton_con_lai,
                            "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"      = tong_so_luong_ton_con_lai
                        WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
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
	      DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_KO_THEO_KHO( IN LAP_RAP_THAO_DO_ID INT ) --Proc_IN_UpdatePriceOW_NoStock_IM_Assembly
        ;
        
        CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_KO_THEO_KHO(IN LAP_RAP_THAO_DO_ID INT)
            RETURNS INT
        AS $$
        DECLARE
        
        
            PHAN_THAP_PHAN_DON_GIA           INT;
        
            PHAN_THAP_PHAN_SO_LUONG          INT;
        
            PHAN_THAP_PHAN_SO_TIEN_QUY_DOI   INT;
        
            TONG_GIA_TRI_THANH_PHAN_THEO_DVT DECIMAL(18, 4);
        
            SO_LUONG_XUAT                    DECIMAL(18, 4);
        
            DON_GIA_XUAT_THEO_DVT_CHINH      DECIMAL(18, 4);
        
        BEGIN
            -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
            SELECT value
            INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
            FETCH FIRST 1 ROW ONLY
            ;
        
            SELECT value
            INTO PHAN_THAP_PHAN_DON_GIA
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
            FETCH FIRST 1 ROW ONLY
            ;
        
            SELECT value
            INTO PHAN_THAP_PHAN_SO_LUONG
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
            FETCH FIRST 1 ROW ONLY
            ;
        
            -----------1. Tính tổng giá trị của các vật tư xuất
        
        
            SELECT SUM(COALESCE("THANH_TIEN_DONG_DVT_CHINH", 0))
            INTO TONG_GIA_TRI_THANH_PHAN_THEO_DVT
            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
            WHERE "LAP_RAP_THAO_DO_ID" = LAP_RAP_THAO_DO_ID
                  AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
            ;
        
        
            TONG_GIA_TRI_THANH_PHAN_THEO_DVT = COALESCE(TONG_GIA_TRI_THANH_PHAN_THEO_DVT, 0)
            ;
        
            --- 2. Tính số lượng thành phẩm
        
        
            SELECT COALESCE("SO_LUONG_THEO_DVT_CHINH", 0)
            INTO SO_LUONG_XUAT
            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
            WHERE "LAP_RAP_THAO_DO_ID" = LAP_RAP_THAO_DO_ID
                  AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1 -- thành phẩm nhập kho
            ;
        
            -------3. Tính giá trị của thành phẩm
        
            DON_GIA_XUAT_THEO_DVT_CHINH
            = ROUND(CAST((TONG_GIA_TRI_THANH_PHAN_THEO_DVT / COALESCE(SO_LUONG_XUAT, 1)) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
            ;
        
            ------4. Cập nhật Price cho thành phẩm
        
            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
            SET
                "DON_GIA_THEO_DVT_CHINH"    = DON_GIA_XUAT_THEO_DVT_CHINH,
                "DON_GIA_DONG"              = ROUND(CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_XUAT_THEO_DVT_CHINH :: DECIMAL,
                                                                                      "TOAN_TU_QUY_DOI",
                                                                                      "TY_LE_CHUYEN_DOI" :: DECIMAL) AS
                                                         NUMERIC), PHAN_THAP_PHAN_DON_GIA),
        
                "THANH_TIEN_DONG"           = TONG_GIA_TRI_THANH_PHAN_THEO_DVT,
        
                "THANH_TIEN_DONG_DVT_CHINH" = TONG_GIA_TRI_THANH_PHAN_THEO_DVT
            WHERE "LAP_RAP_THAO_DO_ID" = LAP_RAP_THAO_DO_ID
                  AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
            ;
        
            RETURN 0
            ;
        
        END
        ;
        $$ LANGUAGE PLpgSQL
        ;
        



			""")


        self.env.cr.execute(""" 
	               DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_HANG_BAN_TRA_LAI_TINH_GIA_KO_THEO_KHO( IN  ID_CHUNG_TU_XUAT_KHO                                       INT ,

            ID_CHUNG_TU_XUAT_KHO_CHI_TIET                                INT,

            tu_ngay_khong_thoi_gian                                      TIMESTAMP,

            den_ngay_khong_thoi_gian                                     TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM_SAreturn
        ;

        CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_HANG_BAN_TRA_LAI_TINH_GIA_KO_THEO_KHO( IN  ID_CHUNG_TU_XUAT_KHO                                       INT ,

            ID_CHUNG_TU_XUAT_KHO_CHI_TIET                                INT,

            tu_ngay_khong_thoi_gian                                      TIMESTAMP,

            den_ngay_khong_thoi_gian                                     TIMESTAMP )
            RETURNS INT
        AS $$
        DECLARE



            ----------------------------------

            PHAN_THAP_PHAN_DON_GIA                                       INT;

            PHAN_THAP_PHAN_SO_LUONG                                      INT;

            PHAN_THAP_PHAN_SO_TIEN_QUY_DOI                               INT;

            CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO BOOLEAN;

            TINH_THEO_KHO_CUA_DONG_XUAT_BAN                              BOOLEAN;

            --@IsCaculateByStock_SaleFrom

            DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU                      DECIMAL(18, 4);

            --@PriceMainUnit_SaleFrom

            DON_GIA_DONG_TEMP                                            DECIMAL(18, 4);

        BEGIN
            -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
            SELECT value
            INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
            FETCH FIRST 1 ROW ONLY
            ;

            SELECT value
            INTO PHAN_THAP_PHAN_DON_GIA
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
            FETCH FIRST 1 ROW ONLY
            ;

            SELECT value
            INTO PHAN_THAP_PHAN_SO_LUONG
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
            FETCH FIRST 1 ROW ONLY
            ;

            -----------1. Tính tổng giá trị của các vật tư xuất


            IF NOT EXISTS(SELECT *
                          FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                          WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                                AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET

                                AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2 -- xuat bán
                                AND "NGAY_HACH_TOAN" >= tu_ngay_khong_thoi_gian -- trong khoảng đã chọn
                                AND "NGAY_HACH_TOAN" <= den_ngay_khong_thoi_gian)
            THEN

                RETURN 0
                ;
            END IF
            ;

            ---=----1. Kiểm tra có cập nhật không:
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

            IF (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = FALSE)
            THEN
                RETURN 0
                ;
            END IF
            ;


            --- 3. Kiem tra xem chung từ xuất bán của chứng từ hàng bán trả lại lần cuoi cùng tình theo kho hay không theo kho
            ---- 3.1 Tinh loai theo kho hay ko theo cua dong xuat ban

            SELECT "IsCaculateByStock"
            INTO TINH_THEO_KHO_CUA_DONG_XUAT_BAN
            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
            WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                  AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET
                  AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
            ;


            ---=============================================================================
            ---------------------------------------------old code -----------------------------


            IF (TINH_THEO_KHO_CUA_DONG_XUAT_BAN = FALSE) -- Tính không theo kho của dòng xuất bán
            THEN


                SELECT "DON_GIA_THEO_DVT_CHINH"
                INTO DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                      AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET

                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                ;


            ELSE /* Dòng xuất bán tính theo kho*/

                -- Lấy giá từ dòng xuất bán từ table danh_muc_vat_tu_hang_hoaPrice"XUAT_KHO"Immediate

                -- phan nay ko can làm tròn vì giá xuất của chứng từ bán đã được làm tròn rồi

                SELECT "DON_GIA_THEO_DVT_CHINH"
                INTO DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                      AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET

                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                ;


            END IF
            ;

            --- Update lại giá của dòng nhập kho hàng bán trả lại


            DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU = ROUND(CAST(COALESCE(DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU, 0) AS NUMERIC),
                                                            PHAN_THAP_PHAN_DON_GIA)
            ;

            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
            SET
                DON_GIA_DONG_TEMP                        = ROUND(
                    CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU :: DECIMAL,
                                                      "TOAN_TU_QUY_DOI",
                                                      "TY_LE_CHUYEN_DOI" :: DECIMAL) AS
                         NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                , "DON_GIA_DONG"                         = DON_GIA_DONG_TEMP
                , "DON_GIA_THEO_DVT_CHINH"               = DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                , "THANH_TIEN_DONG"                      = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                , "THANH_TIEN_DONG_DVT_CHINH"            = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) 
                , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
           
            WHERE "ID_CHUNG_TU_XUAT_KHO" = ID_CHUNG_TU_XUAT_KHO
                  AND "ID_CHUNG_TU_XUAT_KHO_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET
                  AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                  AND "HOAT_DONG_CHI_TIET" = 6 -- "HOAT_DONG_CHI_TIET"=6: Nhập kho bán hàng trả lại

                  AND "PHAN_BIET_GIA" = 0
            ;




            UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
            SET
                DON_GIA_DONG_TEMP                        = ROUND(
                    CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU :: DECIMAL,
                                                      "TOAN_TU_QUY_DOI",
                                                      "TY_LE_CHUYEN_DOI" :: DECIMAL) AS
                         NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                , "DON_GIA_DONG"                         = DON_GIA_DONG_TEMP
                , "DON_GIA_THEO_DVT_CHINH"               = DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                , "THANH_TIEN_DONG"                      = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                , "THANH_TIEN_DONG_DVT_CHINH"            = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) 
                , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
            WHERE "ID_CHUNG_TU_XUAT_KHO" = ID_CHUNG_TU_XUAT_KHO
                  AND "ID_CHUNG_TU_XUAT_KHO_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET
                  AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                  AND "HOAT_DONG_CHI_TIET" = 6

                  AND "PHAN_BIET_GIA" = 0
            ;



           RETURN 0
            ;

        END
        ;
        $$ LANGUAGE PLpgSQL
        ;




			""")


        self.env.cr.execute(""" 
	       DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO( IN  ID_CHUNG_TU_XUAT_KHO       INT  ) --Proc_IN_UpdatePriceOW_NoStock_IM_TransferStock
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO( IN  ID_CHUNG_TU_XUAT_KHO       INT  )
                RETURNS INT
            AS $$
            DECLARE

                id_chung_tu_chi_tiet INT;

            BEGIN

                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho a
                SET "DON_GIA_THEO_DVT_CHINH"               = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA_DONG"                         = b."DON_GIA_DONG",
                    "THANH_TIEN_DONG_DVT_CHINH"            = b."THANH_TIEN_DONG_DVT_CHINH",
                    "THANH_TIEN_DONG"                      = b."THANH_TIEN_DONG",
                    "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b

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
	      DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_THEO_KHO( IN LAP_RAP_THAO_DO_ID INT ) --Proc_IN_UpdatePrice_Oward_IM_Assembly
            ;
            
            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_THEO_KHO(IN LAP_RAP_THAO_DO_ID INT)
                RETURNS INT
            AS $$
            DECLARE
            
            
                PHAN_THAP_PHAN_DON_GIA           INT;
            
                PHAN_THAP_PHAN_SO_LUONG          INT;
            
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI   INT;
            
                TONG_GIA_TRI_THANH_PHAN_THEO_DVT DECIMAL(18, 4);
            
                SO_LUONG_XUAT                    DECIMAL(18, 4);
            
                DON_GIA_XUAT_THEO_DVT_CHINH      DECIMAL(18, 4);
            
            BEGIN
                -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;
            
                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;
            
                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;
            
                -----------1. Tính tổng giá trị của các vật tư xuất
            
            
                SELECT SUM(COALESCE("THANH_TIEN_DONG_DVT_CHINH", 0))
                INTO TONG_GIA_TRI_THANH_PHAN_THEO_DVT
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "LAP_RAP_THAO_DO_ID" = LAP_RAP_THAO_DO_ID
                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                ;
            
            
                TONG_GIA_TRI_THANH_PHAN_THEO_DVT = COALESCE(TONG_GIA_TRI_THANH_PHAN_THEO_DVT, 0)
                ;
            
                --- 2. Tính số lượng thành phẩm
            
            
                SELECT COALESCE("SO_LUONG_THEO_DVT_CHINH", 0)
                INTO SO_LUONG_XUAT
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "LAP_RAP_THAO_DO_ID" = LAP_RAP_THAO_DO_ID
                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1 -- thành phẩm nhập kho
                ;
            
                -------3. Tính giá trị của thành phẩm
            
                DON_GIA_XUAT_THEO_DVT_CHINH
                = ROUND(CAST((TONG_GIA_TRI_THANH_PHAN_THEO_DVT / COALESCE(SO_LUONG_XUAT, 1)) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                ;
            
                ------4. Cập nhật Price cho thành phẩm
            
                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                SET
                    "DON_GIA_THEO_DVT_CHINH"    = DON_GIA_XUAT_THEO_DVT_CHINH,
                    "DON_GIA_DONG"              = ROUND(CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_XUAT_THEO_DVT_CHINH :: DECIMAL,
                                                                                          "TOAN_TU_QUY_DOI",
                                                                                          "TY_LE_CHUYEN_DOI" :: DECIMAL) AS
                                                             NUMERIC), PHAN_THAP_PHAN_DON_GIA),
            
                    "THANH_TIEN_DONG"           = TONG_GIA_TRI_THANH_PHAN_THEO_DVT,
            
                    "THANH_TIEN_DONG_DVT_CHINH" = TONG_GIA_TRI_THANH_PHAN_THEO_DVT
                WHERE "LAP_RAP_THAO_DO_ID" = LAP_RAP_THAO_DO_ID
                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                ;
            
                RETURN 0
                ;
            
            END
            ;
            $$ LANGUAGE PLpgSQL
            ;
            
			""")


        self.env.cr.execute(""" 
	                  DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_HANG_BAN_TRA_LAI( IN  ID_CHUNG_TU_XUAT_KHO                                       INT ,

                ID_CHUNG_TU_XUAT_KHO_CHI_TIET                                INT,

                tu_ngay_khong_thoi_gian                                      TIMESTAMP,

                den_ngay_khong_thoi_gian                                     TIMESTAMP ) --Proc_IN_UpdatePrice_Oward_IM_SAreturn
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_HANG_BAN_TRA_LAI( IN  ID_CHUNG_TU_XUAT_KHO                                       INT ,

                ID_CHUNG_TU_XUAT_KHO_CHI_TIET                                INT,

                tu_ngay_khong_thoi_gian                                      TIMESTAMP,

                den_ngay_khong_thoi_gian                                     TIMESTAMP )
                RETURNS INT
            AS $$
            DECLARE



                ----------------------------------

                PHAN_THAP_PHAN_DON_GIA                                       INT;

                PHAN_THAP_PHAN_SO_LUONG                                      INT;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI                               INT;

                CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO BOOLEAN;

                TINH_THEO_KHO_CUA_DONG_XUAT_BAN                              BOOLEAN;

                --@IsCaculateByStock_SaleFrom

                DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU                      DECIMAL(18, 4);

                --@PriceMainUnit_SaleFrom

                DON_GIA_DONG_TEMP                                            DECIMAL(18, 4);

            BEGIN
                -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;

                -----------1. Tính tổng giá trị của các vật tư xuất


                IF NOT EXISTS(SELECT *
                              FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                              WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                                    AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET

                                    AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2 -- xuat bán
                                    AND "NGAY_HACH_TOAN" >= tu_ngay_khong_thoi_gian -- trong khoảng đã chọn
                                    AND "NGAY_HACH_TOAN" <= den_ngay_khong_thoi_gian)
                THEN

                    RETURN 0
                    ;
                END IF
                ;

                ---=----1. Kiểm tra có cập nhật không:
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

                IF (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = FALSE)
                THEN
                    RETURN 0
                    ;
                END IF
                ;


                --- 3. Kiem tra xem chung từ xuất bán của chứng từ hàng bán trả lại lần cuoi cùng tình theo kho hay không theo kho
                ---- 3.1 Tinh loai theo kho hay ko theo cua dong xuat ban

                SELECT "IsCaculateByStock"
                INTO TINH_THEO_KHO_CUA_DONG_XUAT_BAN
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                      AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET
                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                ;


                ---=============================================================================
                ---------------------------------------------old code -----------------------------


                IF (TINH_THEO_KHO_CUA_DONG_XUAT_BAN = TRUE ) -- Tính không theo kho của dòng xuất bán
                THEN


                    SELECT "DON_GIA_THEO_DVT_CHINH"
                    INTO DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                    WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                          AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET

                          AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                    ;


                ELSE /* Dòng xuất bán tính theo kho*/

                    -- Lấy giá từ dòng xuất bán từ table danh_muc_vat_tu_hang_hoaPrice"XUAT_KHO"Immediate

                    -- phan nay ko can làm tròn vì giá xuất của chứng từ bán đã được làm tròn rồi

                    SELECT "DON_GIA_THEO_DVT_CHINH"
                    INTO DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                    WHERE "ID_CHUNG_TU" = ID_CHUNG_TU_XUAT_KHO
                          AND "ID_CHUNG_TU_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET

                          AND "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                    ;


                END IF
                ;

                --- Update lại giá của dòng nhập kho hàng bán trả lại


                DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU = ROUND(CAST(COALESCE(DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU, 0) AS NUMERIC),
                                                                PHAN_THAP_PHAN_DON_GIA)
                ;

                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                SET
                    DON_GIA_DONG_TEMP                        = ROUND(
                        CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU :: DECIMAL,
                                                          "TOAN_TU_QUY_DOI",
                                                          "TY_LE_CHUYEN_DOI" :: DECIMAL) AS
                             NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                    , "DON_GIA_DONG"                         = DON_GIA_DONG_TEMP
                    , "DON_GIA_THEO_DVT_CHINH"               = DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                    , "THANH_TIEN_DONG"                      = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                     PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                    , "THANH_TIEN_DONG_DVT_CHINH"            = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                     PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) 
                    , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
                WHERE "ID_CHUNG_TU_XUAT_KHO" = ID_CHUNG_TU_XUAT_KHO
                      AND "ID_CHUNG_TU_XUAT_KHO_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET
                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                      AND "HOAT_DONG_CHI_TIET" = 6 -- "HOAT_DONG_CHI_TIET"=6: Nhập kho bán hàng trả lại

                      AND "PHAN_BIET_GIA" = 0
                ;




                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                SET
                    DON_GIA_DONG_TEMP                        = ROUND(
                        CAST(LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU :: DECIMAL,
                                                          "TOAN_TU_QUY_DOI",
                                                          "TY_LE_CHUYEN_DOI" :: DECIMAL) AS
                             NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                    , "DON_GIA_DONG"                         = DON_GIA_DONG_TEMP
                    , "DON_GIA_THEO_DVT_CHINH"               = DON_GIA_TRONG_CHUNG_TU_XUAT_BAN_LUC_DAU

                    , "THANH_TIEN_DONG"                      = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                     PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                    , "THANH_TIEN_DONG_DVT_CHINH"            = ROUND(CAST((DON_GIA_DONG_TEMP * "SO_LUONG_VAT_TU") AS NUMERIC),
                                                                     PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) 
                    , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
                WHERE "ID_CHUNG_TU_XUAT_KHO" = ID_CHUNG_TU_XUAT_KHO
                      AND "ID_CHUNG_TU_XUAT_KHO_CHI_TIET" = ID_CHUNG_TU_XUAT_KHO_CHI_TIET
                      AND "LOAI_HOAT_DONG_NHAP_XUAT" = 1
                      AND "HOAT_DONG_CHI_TIET" = 6

                      AND "PHAN_BIET_GIA" = 0
                ;



               RETURN 0
                ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;


            
			""")



        self.env.cr.execute(""" 
	                   DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_THEO_KHO( IN   id_hoat_dong                        INT,

                DON_GIA_XUAT                        DECIMAL(18, 4) ) --Proc_IN_UpdatePrice_Oward_IM_CalculateOWPrice_Row_DifferType
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_THEO_KHO( IN   id_hoat_dong                        INT,

                DON_GIA_XUAT                        DECIMAL(18, 4) )
                RETURNS   DECIMAL(18, 4)
            AS $$
            DECLARE


                DON_GIA_XUAT                        DECIMAL(18, 4) ;

                ----------------------------------

                PHAN_THAP_PHAN_DON_GIA              INT;

                PHAN_THAP_PHAN_SO_LUONG             INT;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INT;

                chi_nhanh_id                        INT;

                vat_tu_id                           INT;

                kho_id                              INT;

                thoi_gian_hoat_dong                 TIMESTAMP;

                tong_gia_tri_nhap_kho_thong_thuong  DECIMAL(18, 4);

                tong_gia_tri_nhap_kho_chuyen_khoan  DECIMAL(18, 4);

                tong_gia_tri_nhap_kho               DECIMAL(18, 4);

                tong_gia_tri_xuat_kho_thong_thuong  DECIMAL(18, 4);

                tong_gia_tri_xuat_kho_chuyen_khoan  DECIMAL(18, 4);

                tong_gia_tri_xuat_kho               DECIMAL(18, 4);

                tong_gia_tri_con_lai                DECIMAL(18, 4);

                ---SO LUONG---

                tong_so_luong_nhap_kho_thong_thuong DECIMAL(18, 4);

                tong_so_luong_nhap_kho_chuyen_khoan DECIMAL(18, 4);

                tong_so_luong_nhap_kho              DECIMAL(18, 4);

                tong_so_luong_xuat_kho_thong_thuong DECIMAL(18, 4);

                tong_so_luong_xuat_kho_chuyen_khoan DECIMAL(18, 4);

                tong_so_luong_xuat_kho              DECIMAL(18, 4);

                tong_so_luong_con_lai               DECIMAL(18, 4);


            BEGIN
                -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;

                -------------------------------- -- 1. Tính Accum "SO_LUONG" + "SO_TIEN" From "SO_CAI"


                SELECT "CHI_NHANH_ID"
                INTO chi_nhanh_id


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE id = id_hoat_dong
                ;

                SELECT "MA_HANG_ID"
                INTO vat_tu_id

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE id = id_hoat_dong
                ;

                SELECT "MA_KHO_ID"
                INTO kho_id


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE id = id_hoat_dong
                ;

                SELECT "THOI_GIAN_HOAT_DONG"
                INTO thoi_gian_hoat_dong
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                WHERE id = id_hoat_dong
                ;


                --- A. Tính phần giá trị tồn


                --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                SELECT SUM(COALESCE("SO_TIEN_NHAP", 0))
                INTO tong_gia_tri_nhap_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                ---------------
                SELECT SUM(COALESCE("SO_TIEN_NHAP", 0))
                INTO tong_gia_tri_nhap_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                tong_gia_tri_nhap_kho = COALESCE(tong_gia_tri_nhap_kho_thong_thuong, 0)
                                        + COALESCE(tong_gia_tri_nhap_kho_chuyen_khoan, 0)
                ;

                -- Tong gia tri nhap kho


                --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                SELECT SUM(COALESCE("SO_TIEN_XUAT", 0))
                INTO tong_gia_tri_xuat_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho thong thuong

                SELECT SUM(COALESCE("SO_TIEN_XUAT", 0))
                INTO tong_gia_tri_xuat_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '0'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho chuyen kho
                -- Tong gia tri xuat kho
                tong_gia_tri_xuat_kho = COALESCE(tong_gia_tri_xuat_kho_thong_thuong, 0)
                                        + COALESCE(tong_gia_tri_xuat_kho_chuyen_khoan, 0)
                ;


                -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                tong_gia_tri_con_lai = tong_gia_tri_nhap_kho
                                       - tong_gia_tri_xuat_kho
                ;


                --------------- Update lại vào table danh_muc_vat_tu_hang_hoaPrice"XUAT_KHO"Immediate

                -- B. Tính phấn số lượng tồn


                --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                SELECT SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0))
                INTO tong_so_luong_nhap_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                ------------------
                SELECT SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0))
                INTO tong_so_luong_nhap_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- Tong so luong nhap kho
                tong_so_luong_nhap_kho = COALESCE(tong_so_luong_nhap_kho_thong_thuong, 0)
                                         + COALESCE(tong_gia_tri_nhap_kho_chuyen_khoan, 0)
                ;

                --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                SELECT SUM(COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH", 0))
                INTO tong_so_luong_xuat_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho thong thuong

                SELECT SUM(COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
                                    0))
                INTO tong_so_luong_xuat_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                      AND "KHO_ID" = kho_id
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '0'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho chuyen kho

                -- Tong so luong xuat kho
                tong_so_luong_xuat_kho = COALESCE(tong_so_luong_xuat_kho_thong_thuong, 0)
                                         + COALESCE(tong_so_luong_xuat_kho_chuyen_khoan, 0)
                ;


                -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                tong_so_luong_con_lai = tong_so_luong_nhap_kho
                                        - tong_so_luong_xuat_kho
                ;

                ---- Tính giá xuất base on tong_gia_tri_con_lai , tong_so_luong_con_lai
                IF (tong_gia_tri_con_lai <= 0)
                THEN
                    DON_GIA_XUAT = 0
                    ;

                    RETURN DON_GIA_XUAT
                    ;

                END IF
                ;

                ---===============================================

                IF (tong_so_luong_con_lai <= 0)
                THEN
                     DON_GIA_XUAT = 0
                    ;

                    RETURN DON_GIA_XUAT
                    ;


                ELSE

                    DON_GIA_XUAT = ROUND(cast((tong_gia_tri_con_lai
                                         / tong_so_luong_con_lai) as NUMERIC), PHAN_THAP_PHAN_DON_GIA
                    )
                    ;

                    RETURN  DON_GIA_XUAT
                    ;
                END IF
                ;


            END
            ;
            $$ LANGUAGE PLpgSQL
            ;

			""")

        self.env.cr.execute(""" 
	                   DROP FUNCTION IF EXISTS CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_KHONG_THEO_KHO( IN   id_hoat_dong                        INT,

                DON_GIA_XUAT                        DECIMAL(18, 4) ) --Proc_IN_UpdatePriceOW_NoStock_IM_CalculateOWPrice_Row_DifferType
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_NHAP_VTTP_DONG_KHAC_LOAI_KHONG_THEO_KHO( IN   id_hoat_dong                        INT,

                DON_GIA_XUAT                        DECIMAL(18, 4) )
                RETURNS   DECIMAL(18, 4)
            AS $$
            DECLARE


                DON_GIA_XUAT                        DECIMAL(18, 4) ;

                ----------------------------------

                PHAN_THAP_PHAN_DON_GIA              INT;

                PHAN_THAP_PHAN_SO_LUONG             INT;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI      INT;

                chi_nhanh_id                        INT;

                vat_tu_id                           INT;



                thoi_gian_hoat_dong                 TIMESTAMP;

                tong_gia_tri_nhap_kho_thong_thuong  DECIMAL(18, 4);

                tong_gia_tri_nhap_kho_chuyen_khoan  DECIMAL(18, 4);

                tong_gia_tri_nhap_kho               DECIMAL(18, 4);

                tong_gia_tri_xuat_kho_thong_thuong  DECIMAL(18, 4);

                tong_gia_tri_xuat_kho_chuyen_khoan  DECIMAL(18, 4);

                tong_gia_tri_xuat_kho               DECIMAL(18, 4);

                tong_gia_tri_con_lai                DECIMAL(18, 4);

                ---SO LUONG---

                tong_so_luong_nhap_kho_thong_thuong DECIMAL(18, 4);

                tong_so_luong_nhap_kho_chuyen_khoan DECIMAL(18, 4);

                tong_so_luong_nhap_kho              DECIMAL(18, 4);

                tong_so_luong_xuat_kho_thong_thuong DECIMAL(18, 4);

                tong_so_luong_xuat_kho_chuyen_khoan DECIMAL(18, 4);

                tong_so_luong_xuat_kho              DECIMAL(18, 4);

                tong_so_luong_con_lai               DECIMAL(18, 4);


            BEGIN
                -------------- 1.1 SET gia tri  from table SYSDBOption: Số số thap phan cho Price  ----
                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;

                -------------------------------- -- 1. Tính Accum "SO_LUONG" + "SO_TIEN" From "SO_CAI"


                SELECT "CHI_NHANH_ID"
                INTO chi_nhanh_id


                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                WHERE id = id_hoat_dong
                ;

                SELECT "MA_HANG_ID"
                INTO vat_tu_id

                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                WHERE id = id_hoat_dong
                ;

               

                SELECT "THOI_GIAN_HOAT_DONG"
                INTO thoi_gian_hoat_dong
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                WHERE id = id_hoat_dong
                ;


                --- A. Tính phần giá trị tồn


                --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                SELECT SUM(COALESCE("SO_TIEN_NHAP", 0))
                INTO tong_gia_tri_nhap_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                ---------------
                SELECT SUM(COALESCE("SO_TIEN_NHAP", 0))
                INTO tong_gia_tri_nhap_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                tong_gia_tri_nhap_kho = COALESCE(tong_gia_tri_nhap_kho_thong_thuong, 0)
                                        + COALESCE(tong_gia_tri_nhap_kho_chuyen_khoan, 0)
                ;

                -- Tong gia tri nhap kho


                --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                SELECT SUM(COALESCE("SO_TIEN_XUAT", 0))
                INTO tong_gia_tri_xuat_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho thong thuong

                SELECT SUM(COALESCE("SO_TIEN_XUAT", 0))
                INTO tong_gia_tri_xuat_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '0'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho chuyen kho
                -- Tong gia tri xuat kho
                tong_gia_tri_xuat_kho = COALESCE(tong_gia_tri_xuat_kho_thong_thuong, 0)
                                        + COALESCE(tong_gia_tri_xuat_kho_chuyen_khoan, 0)
                ;


                -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                tong_gia_tri_con_lai = tong_gia_tri_nhap_kho
                                       - tong_gia_tri_xuat_kho
                ;


                --------------- Update lại vào table danh_muc_vat_tu_hang_hoaPrice"XUAT_KHO"Immediate

                -- B. Tính phấn số lượng tồn


                --------------------- 1. Tính tổng giá trị nhập, số lượng nhập đến thời điểm tính giá  ---------------------
                SELECT SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0))
                INTO tong_so_luong_nhap_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                ------------------
                SELECT SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0))
                INTO tong_so_luong_nhap_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- Tong so luong nhap kho
                tong_so_luong_nhap_kho = COALESCE(tong_so_luong_nhap_kho_thong_thuong, 0)
                                         + COALESCE(tong_gia_tri_nhap_kho_chuyen_khoan, 0)
                ;

                --------------------- 2. Tính tổng giá trị,  số lượng xuất  ---------------------

                SELECT SUM(COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH", 0))
                INTO tong_so_luong_xuat_kho_thong_thuong
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho thong thuong

                SELECT SUM(COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
                                    0))
                INTO tong_so_luong_xuat_kho_chuyen_khoan
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = chi_nhanh_id

                      AND "MA_HANG_ID" = vat_tu_id
                    
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '2'
                      AND "LOAI_KHU_VUC_NHAP_XUAT" = '0'
                      AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong
                ;

                -- xuat kho chuyen kho

                -- Tong so luong xuat kho
                tong_so_luong_xuat_kho = COALESCE(tong_so_luong_xuat_kho_thong_thuong, 0)
                                         + COALESCE(tong_so_luong_xuat_kho_chuyen_khoan, 0)
                ;


                -------------------------- 3. Tính giá trị tồn, số lượng tồn suy ra giá trị xuất mới ----------------------

                tong_so_luong_con_lai = tong_so_luong_nhap_kho
                                        - tong_so_luong_xuat_kho
                ;

                ---- Tính giá xuất base on tong_gia_tri_con_lai , tong_so_luong_con_lai
                IF (tong_gia_tri_con_lai <= 0)
                THEN
                    DON_GIA_XUAT = 0
                    ;

                    RETURN DON_GIA_XUAT
                    ;

                END IF
                ;

                ---===============================================

                IF (tong_so_luong_con_lai <= 0)
                THEN
                     DON_GIA_XUAT = 0
                    ;

                    RETURN DON_GIA_XUAT
                    ;


                ELSE

                    DON_GIA_XUAT = ROUND(cast((tong_gia_tri_con_lai
                                         / tong_so_luong_con_lai) as NUMERIC), PHAN_THAP_PHAN_DON_GIA
                    )
                    ;

                    RETURN  DON_GIA_XUAT
                    ;
                END IF
                ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;



			""")

        self.env.cr.execute(""" 
					DROP FUNCTION IF EXISTS CAP_NHAT_GIA_TRI_CUA_ROW_TRUOC_TINH_GIA_KO_THEO_KHO( IN  chi_nhanh_id                                                 INT,

			vat_tu_hang_hoa_id                                           INT,

			hang_dong_tren_vat_tu                                        INT,

			tu_ngay_khong_co_thoi_gian                                   TIMESTAMP,

			den_ngay_khong_thoi_gian                                     TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM
		;

		CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_TRI_CUA_ROW_TRUOC_TINH_GIA_KO_THEO_KHO( IN  chi_nhanh_id                                                 INT,

			vat_tu_hang_hoa_id                                           INT,

			hang_dong_tren_vat_tu                                        INT,

			tu_ngay_khong_co_thoi_gian                                   TIMESTAMP,

			den_ngay_khong_thoi_gian                                     TIMESTAMP )
			RETURNS INT
		AS $$
		DECLARE ---Proc_IN_UpdatePriceOW_NoStock_IM

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
				SET PHAN_THAP_PHAN_SO_LUONG = 0
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

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;


			SELECT "SO_LUONG_TON_THEO_DVT_CHINH"
			INTO SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;

			SELECT "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"
			INTO SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;

			SELECT "TONG_GIA_TRI_LUY_KE_KHO"
			INTO TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;

			SELECT "LOAI_HOAT_DONG_NHAP_XUAT"
			INTO LOAI_HOAT_DONG_NHAP_XUAT_TRUOC_DO

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;

			SELECT COALESCE("IsCaculateByStock", FALSE)
			INTO IsCaculateByStock_truoc_do

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;

			SELECT "LOAI_CHUNG_TU"
			INTO LOAI_CHUNG_TU_TRUOC_DO

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
			;

			SELECT "KHONG_CAP_NHAT_GIA_XUAT"
			INTO KHONG_CAP_NHAT_GIA_XUAT_TRUOC_DO
			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
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


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "HOAT_DONG_CHI_TIET"
			INTO HOAT_DONG_CHI_TIET


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;


			SELECT "KHONG_CAP_NHAT_GIA_XUAT"
			INTO KHONG_CAP_NHAT_GIA_XUAT


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "LOAI_CHUNG_TU"
			INTO LOAI_CHUNG_TU


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT id
			INTO ID_HOAT_DONG


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT COALESCE("IsCaculateByStock", FALSE)
			INTO IsCaculateByStock


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "THOI_GIAN_HOAT_DONG"
			INTO thoi_gian_hoat_dong_crrRow


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "ID_CHUNG_TU_CHI_TIET"
			INTO id_chung_tu_chi_tiet


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "NGAY_HACH_TOAN"
			INTO thoi_gian_hoat_dong_crrRow_khong_thoi_gian


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;


			SELECT "LAP_RAP_THAO_DO_ID"
			INTO LAP_RAP_THAO_DO_ID_XUAT


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "ID_CHUNG_TU_XUAT_KHO"
			INTO ID_CHUNG_TU_XUAT_KHO


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
			INTO ID_CHUNG_TU_XUAT_KHO_CHI_TIET


			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
				  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
				  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
			;

			SELECT "PHAN_BIET_GIA"
			INTO PHAN_BIET_GIA

			FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			WHERE "CHI_NHANH_ID" = chi_nhanh_id
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
					SELECT *
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
					SELECT *
					FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)
					;


				END IF
				;

				--===========================================

				SELECT COALESCE("THANH_TIEN_DONG_DVT_CHINH", 0)
				INTO THANH_TIEN_DONG_DVT_CHINH
				FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
				WHERE "CHI_NHANH_ID" = chi_nhanh_id
					  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
					  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

				;

				------
				UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
					SELECT *
					FROM CAP_NHAT_GIA_NHAP_VTTP_LAP_RAP_TD_TINH_GIA_THEO_KHO(LAP_RAP_THAO_DO_ID_XUAT)
					;

				END IF
				;

				--=========2.2.2  trường hợp nhập kho bán hàng trả lại  ===

				IF (HOAT_DONG_CHI_TIET = 6)
				   AND (PHAN_BIET_GIA = 0) --  ("DON_GIA"Method =1): Là nhập giá bằng tay
				   AND (ID_CHUNG_TU_XUAT_KHO IS NOT NULL)
				   AND (ID_CHUNG_TU_XUAT_KHO_CHI_TIET IS NOT NULL)
				-- HOAT_DONG_CHI_TIET=6: Nhập kho bán hàng trả lại
				THEN
					/* bổ sung thêm tu_ngay_khong_co_thoi_gian, den_ngay_khong_thoi_gian  ngày  11.02.2017 sửa lỗi  34819 - Bình quân tức thời: Lỗi khi tính giá xuất kho giá của chứng từ xuất kho sau chứng từ bán trả lại không đúng trường hợp sửa giá của chứng từ bán trả lại*/
					SELECT *
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
					SELECT *
					FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)
					;

				END IF
				;

				------
				UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
				SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(CAST(("THANH_TIEN_DONG_DVT_CHINH") AS NUMERIC),
																	   PHAN_THAP_PHAN_SO_TIEN_QUY_DOI), --"SO_LUONG_THEO_DVT_CHINH"*"DON_GIA_THEO_DVT_CHINH",
					"SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
																	   PHAN_THAP_PHAN_SO_LUONG),
					"DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = ROUND(CAST(("DON_GIA_THEO_DVT_CHINH") AS NUMERIC),
																	   PHAN_THAP_PHAN_DON_GIA),
					"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
				WHERE "CHI_NHANH_ID" = chi_nhanh_id
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
					FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
					WHERE "CHI_NHANH_ID" = chi_nhanh_id
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

						------ update lai gia xuat ---
						SELECT "SO_LUONG_THEO_DVT_CHINH"
						INTO DON_GIA_XUAT_KHO_THEO_DVT_CHINH
						FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
						WHERE "CHI_NHANH_ID" = chi_nhanh_id
							  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
							  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
						;

						----================================
						UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
						SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
															 PHAN_THAP_PHAN_DON_GIA),
							"DON_GIA_DONG"           = ROUND(
								LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
																   "TOAN_TU_QUY_DOI",
																   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
								PHAN_THAP_PHAN_DON_GIA)
						WHERE "CHI_NHANH_ID" = chi_nhanh_id
							  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
							  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

						;

						--======================== tinh tong gia tri Row -------------------

						SELECT ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH"
										   * "DON_GIA_THEO_DVT_CHINH") AS NUMERIC),
									 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
						INTO THANH_TIEN_DONG_DVT_CHINH
						FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
						WHERE "CHI_NHANH_ID" = chi_nhanh_id
							  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
							  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
						;


						----- update gia tri Tong Kho con lai , so luong con lai -------------
						UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
						SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = ROUND(CAST((
																						GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
																						- THANH_TIEN_DONG_DVT_CHINH) AS
																					NUMERIC),
																			   PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
							"THANH_TIEN_DONG_DVT_CHINH"                = ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH"
																					 * "DON_GIA_THEO_DVT_CHINH") AS NUMERIC),
																			   PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
							"THANH_TIEN_DONG"                          = ROUND(
								CAST(("SO_LUONG_VAT_TU" * "DON_GIA_DONG") AS NUMERIC),
								PHAN_THAP_PHAN_SO_TIEN_QUY_DOI),
							"SO_LUONG_TON_THEO_DVT_CHINH"              = ROUND(CAST((SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
																					 - "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
																			   PHAN_THAP_PHAN_SO_LUONG),
							"DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = ROUND(
								CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
								PHAN_THAP_PHAN_DON_GIA),
							"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
						WHERE "CHI_NHANH_ID" = chi_nhanh_id
							  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
							  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
						;


						IF (HOAT_DONG_CHI_TIET =
							5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
						THEN


							----------- trường hợp chuyển kho ------
							SELECT *
							FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)

							;


						END IF
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
							END IF
							;


							------------------------------- Nếu <0 thì cho giá về 0 ----

							IF (DON_GIA_XUAT_KHO_THEO_DVT_CHINH < 0)
							THEN
								DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0
								;


								--- end new code


								-- tinh gia tri ton , so luong ton . Don gia xuat kho = Gia tri ton/ So luong ton
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
								SET "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
									"DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
									"SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
									"THANH_TIEN_DONG"                          = GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
									"THANH_TIEN_DONG_DVT_CHINH"                = GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO,
									"DON_GIA_THEO_DVT_CHINH"                   = ROUND(
										CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
										PHAN_THAP_PHAN_DON_GIA),
									"DON_GIA_DONG"                             = ROUND(
										LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
																		   "TOAN_TU_QUY_DOI",
																		   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
										PHAN_THAP_PHAN_DON_GIA),
									"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
								WHERE "CHI_NHANH_ID" = chi_nhanh_id
									  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
									  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

								;

								IF (HOAT_DONG_CHI_TIET =
									5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
								THEN


									----------- trường hợp chuyển kho ------
									SELECT *
									FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)

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
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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

									ROUND((GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO - "THANH_TIEN_DONG_DVT_CHINH")
										  / LAY_SO_THAP_PHAN_KHAC_KHONG(SO_LUONG_TON_THEO_DVT_CHINH_TRUOC_DO
																		- "SO_LUONG_THEO_DVT_CHINH"),
										  PHAN_THAP_PHAN_DON_GIA),
									"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
								WHERE "CHI_NHANH_ID" = chi_nhanh_id
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

					UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
					SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
						"THANH_TIEN_DONG"                          = 0,
						"DON_GIA_DONG"                             = 0,
						"THANH_TIEN_DONG_DVT_CHINH"                = 0,
						"GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
						"DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
						"SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
						"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = LOCALTIMESTAMP
					WHERE "CHI_NHANH_ID" = chi_nhanh_id
						  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
						  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

					;

					---============= NEW ADD===

					/*hoant sửa lôi 33209 - Bình quân tức thời: Lỗi trên sổ chi tiết VTHH không lấy được thông tin tiền vốn và đơn giá vốn trên chứng từ chuyển kho trường hợp không nhập đơn giá bán, thành tiền*/
					/* Update lại giá nhập của chứng từ chuyển kho tương ứng*/

					IF HOAT_DONG_CHI_TIET = 5 -- chuyển kho
					THEN
						UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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


					UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
					SET
						"GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = "THANH_TIEN_DONG",

						"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
					WHERE "CHI_NHANH_ID" = chi_nhanh_id
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

							UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
								  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
								  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

							;

							---------------------
							IF (HOAT_DONG_CHI_TIET =
								5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan
							THEN


								-- cap nhap gia tri nhap chuyen kho tuong ung
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
								DON_GIA_XUAT_KHO_THEO_DVT_CHINH = GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
																  / SO_LUONG_THEO_DVT_CHINH
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
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
								SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
																	 PHAN_THAP_PHAN_DON_GIA),
									"DON_GIA_DONG"           = ROUND(
										LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
																		   "TOAN_TU_QUY_DOI",
																		   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
										PHAN_THAP_PHAN_DON_GIA)
								WHERE "CHI_NHANH_ID" = chi_nhanh_id
									  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
									  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

								;


								----- update gia tri Tong Kho con lai , so luong con lai -------------
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
									"THANH_TIEN_DONG"                          = (CASE WHEN (DON_GIA_XUAT_KHO_THEO_DVT_CHINH =
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
									  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
									  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
								;

							END IF
							;


							IF (HOAT_DONG_CHI_TIET =
								5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
							THEN


								----------- trường hợp chuyển kho ------
								SELECT *
								FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)
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
											FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
											WHERE "CHI_NHANH_ID" = chi_nhanh_id
												  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
												  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do
											;

											/* hoant 08.05.2017 SMESEVEN-4826 sửa lỗi 100494- Bình quân tức thời: Lỗi tính giá sai khi thực hiện tính giá ngắt quãng và tháng trước có phát sinh chứng từ xuất cuối cùng*/
											IF
											(DON_GIA_XUAT_KHO_THEO_DVT_CHINH = 0 OR DON_GIA_XUAT_KHO_THEO_DVT_CHINH IS NULL) AND
											TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO > 0 AND
											SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO > 0

											THEN
												DON_GIA_XUAT_KHO_THEO_DVT_CHINH = ROUND(CAST(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
																							 / LAY_SO_THAP_PHAN_KHAC_KHONG(
																								 SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO)
																							 AS NUMERIC),
																						PHAN_THAP_PHAN_DON_GIA)
												;
											END IF
											;

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

									----================================
									UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
									SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
																		 PHAN_THAP_PHAN_DON_GIA),
										"DON_GIA_DONG"           = ROUND(
											LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
																			   "TOAN_TU_QUY_DOI",
																			   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
											PHAN_THAP_PHAN_DON_GIA)
									WHERE "CHI_NHANH_ID" = chi_nhanh_id
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

									;


									--======================== tinh tong gia tri Row -------------------

									SELECT THANH_TIEN_DONG_DVT_CHINH = ROUND(CAST(("SO_LUONG_THEO_DVT_CHINH"
																				   * DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS
																				  NUMERIC),
																			 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
									WHERE "CHI_NHANH_ID" = chi_nhanh_id
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
									;


									----- update gia tri Tong Kho con lai , so luong con lai -------------
									UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
									;


									IF (HOAT_DONG_CHI_TIET =
										5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
									THEN


										----------- trường hợp chuyển kho ------
										SELECT *
										FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)

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

								-- end new code ====================================================
								------ update lai gia xuat ---

								/* old code:
											SELECT  DON_GIA_XUAT_KHO_THEO_DVT_CHINH = GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH_TRUOC_DO
													/ SO_LUONG_THEO_DVT_CHINH
											 */


								----================================
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
								SET "DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
																	 PHAN_THAP_PHAN_DON_GIA),
									"DON_GIA_DONG"           = ROUND(
										LAY_DON_GIA_TU_DON_GIA_CHINH(CAST((DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
																		   "TOAN_TU_QUY_DOI",
																		   "TY_LE_CHUYEN_DOI") AS NUMERIC)),
										PHAN_THAP_PHAN_DON_GIA)
								WHERE "CHI_NHANH_ID" = chi_nhanh_id
									  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
									  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

								;


								----- update gia tri Tong Kho con lai , so luong con lai -------------
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
									  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
									  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
								;


								IF (HOAT_DONG_CHI_TIET =
									5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
								THEN


									----------- trường hợp chuyển kho ------
									SELECT *
									FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)

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
							UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
							SET "DON_GIA_THEO_DVT_CHINH"                   = 0,
								"THANH_TIEN_DONG"                          = 0,
								"DON_GIA_DONG"                             = 0,
								"THANH_TIEN_DONG_DVT_CHINH"                = 0,
								"GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH" = 0,
								"DON_GIA_XUAT_KHO_THEO_DVT_CHINH"          = 0,
								"SO_LUONG_TON_THEO_DVT_CHINH"              = 0,
								"THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"     = localtimestamp
							WHERE "CHI_NHANH_ID" = chi_nhanh_id
								  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
								  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

							;

							---------------------
							IF (HOAT_DONG_CHI_TIET =
								5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
							THEN


								-- cap nhap gia tri nhap chuyen kho tuong ung
								UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
										FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
										WHERE "CHI_NHANH_ID" = chi_nhanh_id
											  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
											  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu_truoc_do

										;

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


									----================================
									UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
									SET "DON_GIA_THEO_DVT_CHINH" = ROUND(cast((DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
																		 PHAN_THAP_PHAN_DON_GIA),
										"DON_GIA_DONG"           = ROUND(
											LAY_DON_GIA_TU_DON_GIA_CHINH(DON_GIA_XUAT_KHO_THEO_DVT_CHINH,
																		 "TOAN_TU_QUY_DOI",
																		 "TY_LE_CHUYEN_DOI"),
											PHAN_THAP_PHAN_DON_GIA)
									WHERE "CHI_NHANH_ID" = chi_nhanh_id
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

									;


									--======================== tinh tong gia tri Row -------------------

									SELECT ROUND(cast(("SO_LUONG_THEO_DVT_CHINH"
													   * DON_GIA_XUAT_KHO_THEO_DVT_CHINH) AS NUMERIC),
												 PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									INTO THANH_TIEN_DONG_DVT_CHINH
									FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
									WHERE "CHI_NHANH_ID" = chi_nhanh_id
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
									;


									----- update gia tri Tong Kho con lai , so luong con lai -------------
									UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu
									;


									IF (HOAT_DONG_CHI_TIET =
										5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
									THEN


										----------- trường hợp chuyển kho ------
										SELECT *
										FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)
										;


									END IF
									;


								END IF
								;


							ELSE
								IF (SO_LUONG_THEO_DVT_CHINH =
									SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO) /* Xuất hết tồn còn lại*/
								THEN
									--- tinh gia xuat kho de update cho Nhap kho tuong ung

									DON_GIA_XUAT_KHO_THEO_DVT_CHINH = TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO
																	  / LAY_SO_THAP_PHAN_KHAC_KHONG(SO_LUONG_THEO_DVT_CHINH)
									;

									-- tinh gia tri ton , so luong ton . Don gia xuat kho = Gia tri ton/ So luong ton
									UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
										  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
										  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

									;

									IF (HOAT_DONG_CHI_TIET =
										5) -- la xuat kho dieu chuyen , khi do se update lai gia tri nhap kho cua Kho nhan1
									THEN


										----------- trường hợp chuyển kho ------
										SELECT *
										FROM CAP_NHAT_GIA_NHAP_VTTP_CHUYEN_KHO_TINH_GIA_KO_THEO_KHO(id_chung_tu_chi_tiet)

										;

									END IF
									;


								ELSE /*Xuất quá tồn lần đầu: SO_LUONG_THEO_DVT_CHINH >  "GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH"_before )*/


									----================================
									/* ko update lại giá xuất kho */


									----- update gia tri Tong Kho con lai , so luong con lai -------------
									UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
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
					UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
					SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
																+ "SO_LUONG_THEO_DVT_CHINH",
						"TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
																+ "THANH_TIEN_DONG_DVT_CHINH",
						-- Update lại IsCaculateByStock ko theo kho
						"IsCaculateByStock"                   = 0
					WHERE "CHI_NHANH_ID" = chi_nhanh_id
						  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
						  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

					;

				ELSE
					IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
					THEN -- Xuất kho
						UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
						SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
																	- "SO_LUONG_THEO_DVT_CHINH",
							"TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
																	- "THANH_TIEN_DONG_DVT_CHINH",
							-- Update lại IsCaculateByStock ko theo kho
							"IsCaculateByStock"                   = 0
						WHERE "CHI_NHANH_ID" = chi_nhanh_id
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
					  --  AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow;
					  /* Fix ID= 35049. */
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
					  --    AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow;
					  /* Fix ID= 35049. */
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
					  --AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow;  -- xuat kho thong thuong
					  /* Fix ID= 35049. */
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
					  --AND "STT_LOAI_CHUNG_TU" < thoi_gian_hoat_dong_crrRow;  -- xuat kho chuyen kho
					  /* Fix ID= 35049. */
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
					UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
					SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
																+ "SO_LUONG_THEO_DVT_CHINH",
						"TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0) /*change */
																+ "THANH_TIEN_DONG_DVT_CHINH",
						-- Update lại IsCaculateByStock theo kho
						"IsCaculateByStock"                   = FALSE
					WHERE "CHI_NHANH_ID" = chi_nhanh_id
						  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
						  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

					;

				ELSE
					IF (LOAI_HOAT_DONG_NHAP_XUAT = 2)
					THEN -- Xuất kho
						UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
						SET "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = COALESCE(SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH_TRUOC_DO, 0)
																	- "SO_LUONG_THEO_DVT_CHINH",
							"TONG_GIA_TRI_LUY_KE_KHO"             = COALESCE(TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO, 0)
																	- "THANH_TIEN_DONG_DVT_CHINH",
							-- Update lại IsCaculateByStock theo kho
							"IsCaculateByStock"                   = FALSE
						WHERE "CHI_NHANH_ID" = chi_nhanh_id
							  AND "MA_HANG_ID" = vat_tu_hang_hoa_id
							  AND "HANH_DONG_TREN_VAT_TU" = hang_dong_tren_vat_tu

						;


					END IF
					;
				END IF
				;
			END IF
			;


			/* end: Trường hợp  Row hiện tai và row trước không cùng tính theo kho hoặc cùng ko theo kho thì tính lại TONG_GIA_TRI_LUY_KE_KHO_TRUOC_DO từ ledger */

			----===================== End of Procedure ==================

					   RETURN 0
						;

		END
		;
		$$ LANGUAGE PLpgSQL
		;

		

            """)


        self.env.cr.execute(""" 
	                   DROP FUNCTION IF EXISTS CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_VAT_TU_TRONG_1_CHI_NHANH_TU_NGAY_DEN_NGAY( IN
                DS_MA_VTHH                                                   VARCHAR,

                dau_phan_cach                                                VARCHAR,

                v_chi_nhanh_id                                               INT,

                v_tu_ngay                                   TIMESTAMP,

                v_den_ngay                                     TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM_ListMaterialFromDateToDateInBranch
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_VAT_TU_TRONG_1_CHI_NHANH_TU_NGAY_DEN_NGAY( IN
                DS_MA_VTHH                                                   VARCHAR,

                dau_phan_cach                                                VARCHAR,

                v_chi_nhanh_id                                               INT,

                v_tu_ngay                                   TIMESTAMP,
            
                v_den_ngay                                     TIMESTAMP )

                RETURNS INT
            AS $$
            DECLARE

                v_den_ngay                                                   TIMESTAMP ;

                 v_tu_ngay                                                   TIMESTAMP ;

               

                v_chi_nhanh_id                                               INT ;

                v_tu_ngay_khong_thoi_gian                                    TIMESTAMP;

                --@FromDate_NoTime

                v_den_ngay_khong_thoi_gian                                   TIMESTAMP;


                v_ToDateTime_NextNoTime                                      TIMESTAMP;

                DS_MA_VTHH                                                   VARCHAR ;

                --@ListInventoryItemID


                hang_dong_toi_thieu_tren_vat_lieu                            INT;

                --@MinActionRowOnMaterial

                dau_phan_cach                                                VARCHAR;

                --@SeparateCharacter

                dong_toi_thieu                                               INT;

                --@RowMin

                iRow                                                         INT;

                --iRow

                InrefOrder                                                   TIMESTAMP;

                --@InrefOrder

                hang_truoc                                                   INT;

                --@RowBefore

                rec                                                          RECORD;

                rec_2                                                        RECORD;

                cap_nhat_lan_cuoi_hang_truoc                                 TIMESTAMP;

                --@LastUpdate_RowBefore

                id_chung_tu_chi_tiet_id_hang_truoc                           INT;

                --@RefDetailID_RowBefore


            BEGIN




            v_ToDateTime_NextNoTime = v_den_ngay + INTERVAL '1 day'
                ;

                v_ToDateTime_NextNoTime = lay_ngay_thang(v_ToDateTime_NextNoTime)
                ;


                DROP TABLE IF EXISTS TMP_VTHH_ID
                ;

                CREATE TEMP TABLE TMP_VTHH_ID

                (
                    "Value" VARCHAR
                )
                ;

                INSERT INTO TMP_VTHH_ID
                    SELECT DISTINCT value
                    FROM chuyen_chuoi_thanh_bang(DS_MA_VTHH,
                                                 dau_phan_cach)
                ;


                FOR rec IN


                SELECT A."MA_HANG_ID" AS "MA_HANG_ID_TEMP"
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
                    INNER JOIN TMP_VTHH_ID B ON A."MA_HANG_ID" = CAST(B."Value" AS INT)
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id


                GROUP BY A."MA_HANG_ID"

                LOOP

                    hang_dong_toi_thieu_tren_vat_lieu = NULL
                ;

                    SELECT MIN("HANH_DONG_TREN_VAT_TU")
                    INTO hang_dong_toi_thieu_tren_vat_lieu
                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                          AND "MA_HANG_ID" = rec."MA_HANG_ID_TEMP"

                          AND "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" IS NULL
                ;

                    IF (hang_dong_toi_thieu_tren_vat_lieu IS NOT NULL)
                    THEN
                        UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                        SET "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = NULL
                        WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                              AND "MA_HANG_ID" = rec."MA_HANG_ID_TEMP"

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
                    "HANH_DONG_TREN_VAT_TU" INT
                )
                ;


                INSERT INTO TMP_BANG_HANG_TON_KHO_TOI_THIEU
                    SELECT
                        "MA_HANG_ID"
                        , MIN("HANH_DONG_TREN_VAT_TU") AS "HANH_DONG_TREN_VAT_TU"
                    FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
                        INNER JOIN TMP_VTHH_ID B ON A."MA_HANG_ID" = CAST(B."Value" AS INT)
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

                          AND (("THOI_GIAN_HOAT_DONG" >= v_tu_ngay_khong_thoi_gian
                                AND "THOI_GIAN_HOAT_DONG" < v_ToDateTime_NextNoTime)
                          )
                    GROUP BY "MA_HANG_ID"
                ;


                ---===================3. Tao cursor tren danh sach ID_VatTu,  ===============


                FOR rec_2 IN
                SELECT
                    "MA_HANG_ID" AS "MA_HANG_ID_TEMP"
                    , "HANH_DONG_TREN_VAT_TU"
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A /*hoant 10.01.2017 chuyển thành inner join thay cho in*/
                    INNER JOIN TMP_VTHH_ID B ON A."MA_HANG_ID" = cast(B."Value" AS INT)
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
                            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                            WHERE "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                                  AND "CHI_NHANH_ID" = v_chi_nhanh_id

                                  AND "HANH_DONG_TREN_VAT_TU" = dong_toi_thieu
                            ;


                            SELECT hang_truoc = dong_toi_thieu - 1
                            ;

                     select * from     ham_kiem_tra_gia_tri_ton_kho_trong_bang_stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho (v_chi_nhanh_id,rec_2."MA_HANG_ID_TEMP",InrefOrder,hang_truoc);


                            SELECT "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT"
                            INTO cap_nhat_lan_cuoi_hang_truoc

                            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                            WHERE
                                "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                                AND "CHI_NHANH_ID" = v_chi_nhanh_id

                                AND "HANH_DONG_TREN_VAT_TU" = hang_truoc
                            ;

                            SELECT "ID_CHUNG_TU_CHI_TIET"
                            INTO id_chung_tu_chi_tiet_id_hang_truoc
                            FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                            WHERE
                                "MA_HANG_ID" = rec_2."MA_HANG_ID_TEMP"
                                AND "CHI_NHANH_ID" = v_chi_nhanh_id

                                AND "HANH_DONG_TREN_VAT_TU" = hang_truoc
                            ;


                            IF (cap_nhat_lan_cuoi_hang_truoc IS NULL) -- Lay gia tu "SO_CAI" sang
                            THEN
                                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho B1
                                SET

                                    "DON_GIA_DONG"              = A."DON_GIA", --PriceRow
                                    "THANH_TIEN_DONG"           = A."SO_TIEN_XUAT", --"SO_TIEN"Row
                                    "DON_GIA_THEO_DVT_CHINH"    = A."DON_GIA_THEO_DVT_CHINH", --Price"DVT_CHINH_DVC"
                                    "THANH_TIEN_DONG_DVT_CHINH" = A."SO_TIEN_XUAT" --	 "SO_TIEN"Row"DVT_CHINH_DVC"


                                FROM so_kho_chi_tiet A
                                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho B
                                        ON A."CHI_TIET_ID" = B."ID_CHUNG_TU_CHI_TIET" AND
                                           A."CHI_TIET_MODEL" = B."MODEL_CHUNG_TU_TIET"
                                WHERE B."ID_CHUNG_TU_CHI_TIET" = id_chung_tu_chi_tiet_id_hang_truoc

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
                        
                  SELECT  * from   CAP_NHAT_GIA_TRI_CUA_ROW_TRUOC_TINH_GIA_KO_THEO_KHO (v_chi_nhanh_id,rec_2."MA_HANG_ID_TEMP",iRow,v_tu_ngay_khong_thoi_gian,v_den_ngay_khong_thoi_gian) ;

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
                                                    cast (0 as int),
                                                    iRow,
                                                    cast('Error' as VARCHAR(255)),
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
		                DROP FUNCTION IF EXISTS CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY( IN
                DS_MA_VTHH VARCHAR,

                dau_phan_cach VARCHAR,

                v_tu_ngay TIMESTAMP,

                v_den_ngay TIMESTAMP,

                v_chi_nhanh_id INT
                ) --Proc_IN_UpdatePriceOW_NoStock_IM_FromTableCaculateToInLedgerFromToDateTimeListItemIDInBranch
                ;

                CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY( IN
                DS_MA_VTHH VARCHAR,

                dau_phan_cach VARCHAR,

                v_tu_ngay TIMESTAMP,

                v_den_ngay TIMESTAMP,

                v_chi_nhanh_id INT
                )

                    RETURNS INT
                AS $$

                ---Proc_IN_UpdatePriceOW_NoStock_IM_FromTableCaculateToInLedgerFromToDateTimeListItemIDInBranch
                DECLARE

                    v_chi_nhanh_id            INT ;

                    v_tu_ngay TIMESTAMP;

                    v_den_ngay      TIMESTAMP;

                    DS_MA_VTHH                VARCHAR ;

                    --@ListInventoryItemID

                    tat_ca_vat_lieu           BOOLEAN;

                    dau_phan_cach             VARCHAR ;

                    --@SeparateCharacter


                BEGIN
                    ----------------- Step 3: Cập nhật giá sau khi tính vào table InventoryLedger, GeneralLedger, AccountObjectLedger:  ---------------


                    DROP TABLE IF EXISTS TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY
                    ;

                    CREATE TEMP TABLE TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY

                    (
                        "Value" VARCHAR
                    )
                    ;

                    INSERT INTO TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY
                        SELECT DISTINCT value
                        FROM chuyen_chuoi_thanh_bang(DS_MA_VTHH,
                                                     dau_phan_cach)
                    ;


                    IF (length(DS_MA_VTHH) > 0)
                    THEN
                        tat_ca_vat_lieu = FALSE
                        ;
                    ELSE
                        tat_ca_vat_lieu = TRUE
                        ;
                    END IF
                    ;


                    -------------------1. Update MainPrice cua cac VT xuat kho thong thuong table so_kho_chi_tiet :
                    -------------------- Hieu nang : 7 s cho 112.000 bản ghi
                    --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table so_kho_chi_tiet: 1. Update MainPrice cua cac VT xuat kho thong thuong'


                    IF (length(DS_MA_VTHH) > 0)
                    THEN
                        UPDATE so_kho_chi_tiet a1
                        SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                            "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                                    a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                                    a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                            "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                        FROM so_kho_chi_tiet AS a
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
                                ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                                )

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
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
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
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


                    IF (length(DS_MA_VTHH) > 0)
                    THEN

                        UPDATE so_kho_chi_tiet a1
                        SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                            "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                                    a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                                    a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                            "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                        FROM so_kho_chi_tiet AS a
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
                                ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                                )

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
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
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
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
                    IF (length(DS_MA_VTHH) > 0)
                    THEN
                        UPDATE so_kho_chi_tiet a1
                        SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                            "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                                    a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                                    a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                            "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                        FROM so_kho_chi_tiet AS a
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
                                ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                                )

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
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


                    IF (length(DS_MA_VTHH) > 0)
                    THEN
                        UPDATE so_kho_chi_tiet a1
                        SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                            "DON_GIA"                = LAY_DON_GIA_TU_DON_GIA_CHINH(b."DON_GIA_THEO_DVT_CHINH" :: DECIMAL,
                                                                                    a."PHEP_TINH_CHUYEN_DOI" :: VARCHAR(10),
                                                                                    a."TY_LE_CHUYEN_DOI" :: DECIMAL),
                            "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                        FROM so_kho_chi_tiet AS a
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
                                ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                                )

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
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


                    IF (length(DS_MA_VTHH) > 0)
                    THEN

                        UPDATE so_kho_chi_tiet a1
                        SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                            "DON_GIA"                = b."DON_GIA_DONG",
                            "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                        FROM so_kho_chi_tiet AS a
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
                                ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"

                                )

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                        WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '1'  /*Nhập kho*/
                              AND a."LA_NHAP_KHO" = TRUE  /*Nhập vào*/
                              AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1   /* Nhập kho */
                              AND b."HOAT_DONG_CHI_TIET" = 6 /* =6: Nhập kho bán hàng trả lại*/
                              AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                              AND a."NGAY_HACH_TOAN" <= v_den_ngay

                              AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                              AND (a."ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                              AND (a."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                              AND a1.id = a.id
                        ;

                    ELSE -- tất cả VT chi nhánh

                        UPDATE so_kho_chi_tiet a1
                        SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH", "DON_GIA" = b."DON_GIA_DONG",
                            "SO_TIEN_XUAT"           = b."THANH_TIEN_DONG"
                        FROM so_kho_chi_tiet AS a
                            INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b ON
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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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
                              AND a1.id = a.id
                        ;
                    END IF
                    ;


                    --  ----------------------4.1.2 Chuyển kho - xuất kho ------
                    --   EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update cho table "CHI_PHI_CHUNG""SO_CAI": -4.1 Update Debit : Nợ  -- 4.1.2 Chuyển kho - xuất kho '


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                        WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                              AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                              AND a."NGAY_HACH_TOAN" <= v_den_ngay
                              AND a."LOAI_HACH_TOAN" = '1'
                              AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3' /*"LOAI_KHU_VUC_NHAP_XUAT" =3 : Xuất kho ;*/

                              /*hoant 30.08.2017 sửa lỗi 135357 - Đối trừ chứng từ_Lỗi: số tiền nguyên tệ hiển thị giá trị không đúng đối với chứng từ giảm giá hàng mua*/
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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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


                    IF (length(DS_MA_VTHH) > 0)
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

                            INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

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

                        LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)

                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '1'
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3'

                          AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE

                          AND (CAST(C."Value" AS INT) IS NOT NULL OR tat_ca_vat_lieu = TRUE)
                          AND a1.id = a.id
                    ;

                    --
                    --   --========================= 5.2 Update "GHI_CO" : Có =========================
                    --   ----------------------------5.2.1 - Nhập kho ---------------
                    --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  -- 5.2.1 - Nhập kho'


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

                        LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'
                          AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1' /*"LOAI_KHU_VUC_NHAP_XUAT"=1: Nhập kho */
                          AND (CAST(C."Value" AS INT) IS NOT NULL OR tat_ca_vat_lieu = TRUE)
                          AND a1.id = a.id
                    ;


                    --     ----------------------------5.2.2 - Chuyển kho : Xuất  kho ---------------
                    --     EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  -- 5.2.2 - Chuyển kho : Xuất  kho'


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

                        LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '2'
                          AND b."LA_NHAP_KHO" = FALSE
                          /*"LOAI_KHU_VUC_NHAP_XUAT"=2 : Chuyển kho ; kết hợp với "LA_NHAP_KHO"=0: xuất kho ; "LA_NHAP_KHO"=1 : Nhập kho*/
                          AND b."LOAI_CHUNG_TU" IN ('2013', '2011')
                          AND (CAST(C."Value" AS INT) IS NOT NULL OR tat_ca_vat_lieu = TRUE)
                          AND a1.id = a.id
                    ;

                    --       ----------------------------5.2.3 - Chuyển kho : nhập  kho ---------------
                    --       EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  --  5.2.3 - Chuyển kho : nhập  kho'

                    --  ----------------------------------5.2.4 Xuất kho --------
                    --   EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'5. Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet: - 5.2 Update "GHI_CO" : Có  --  5.2.4 Xuất kho'


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

                        LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY C ON A."MA_HANG_ID" = CAST(C."Value" AS INT)
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id

                          AND a."NGAY_HACH_TOAN" >= v_tu_ngay
                          AND a."NGAY_HACH_TOAN" <= v_den_ngay
                          AND a."LOAI_HACH_TOAN" = '2'  /* Ghi có */
                          AND b."LOAI_KHU_VUC_NHAP_XUAT" = '3' /*"LOAI_KHU_VUC_NHAP_XUAT" =3 : Xuất kho ;*/

                          AND b."KHONG_CAP_NHAT_GIA_XUAT" = FALSE

                          AND (CAST(C."Value" AS INT) IS NOT NULL OR tat_ca_vat_lieu = TRUE)

                          AND a1.id = a.id
                    ;

                                  RETURN 0
                                            ;

                            END
                            ;
                            $$ LANGUAGE PLpgSQL
                            ;

                
            """)



        self.env.cr.execute(""" 
		        DROP FUNCTION IF EXISTS CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL( IN
        DS_MA_VTHH VARCHAR,
        
        dau_phan_cach VARCHAR,
        
        v_tu_ngay TIMESTAMP,
        
        v_den_ngay TIMESTAMP,
        v_chi_nhanh_id INT
        )
        --Proc_IN_UpdatePriceOW_NoStock_IM_FromTableCaculateToVchersFromToDateTimeListItemInBranch
        ;
        
        CREATE OR REPLACE FUNCTION CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL(IN
        DS_MA_VTHH     VARCHAR,
        
        dau_phan_cach  VARCHAR,
        
        v_tu_ngay      TIMESTAMP,
        
        v_den_ngay     TIMESTAMP,
        v_chi_nhanh_id INT
        )
        
            RETURNS INT
        AS $$
        DECLARE
            v_tu_ngay                  TIMESTAMP ;
        
            
        
            v_den_ngay                 TIMESTAMP ;
        
           
        
            v_chi_nhanh_id             INT;
        
            v_tu_ngay_khong_thoi_gian  TIMESTAMP;
        
          
        
            v_den_ngay_khong_thoi_gian TIMESTAMP;
        
        
            DS_MA_VTHH                 VARCHAR;
        
         
        
            tat_ca_vat_lieu            BOOLEAN;
        
        
            dau_phan_cach              VARCHAR;
        
            --@SeparateCharacter
        
        
        BEGIN
            v_tu_ngay_khong_thoi_gian = lay_ngay_thang(v_tu_ngay)
            ;
        
            v_den_ngay_khong_thoi_gian = lay_ngay_thang(v_den_ngay)
            ;
        
        
            DROP TABLE IF EXISTS TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL
            ;
        
            CREATE TEMP TABLE TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL
        
            (
                "Value" VARCHAR
            )
            ;
        
            INSERT INTO TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL
                SELECT DISTINCT value
                FROM chuyen_chuoi_thanh_bang(DS_MA_VTHH,
                                             dau_phan_cach)
            ;
        
        
            IF (length(DS_MA_VTHH) > 0)
            THEN
                tat_ca_vat_lieu = FALSE
                ;
            ELSE
                tat_ca_vat_lieu = TRUE
                ;
            END IF
            ;
        
        
            ----------------------------------Step 4: Cập nhật giá sau khi tính vào table chứng từ kho master và Detail: ----
        
        
            --======================= 1.a.1 Update Price cho Table IN"XUAT_KHO"Detail ================
            ------------------update  Table IN"XUAT_KHO"Detail
            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update Voucher xuất kho: table IN"XUAT_KHO"Detail '
        
            UPDATE stock_ex_nhap_xuat_kho_chi_tiet a1
            SET "DON_GIA_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                "DON_GIA"           = b."DON_GIA_DONG",
                "TIEN_VON"          = b."THANH_TIEN_DONG"
            FROM stock_ex_nhap_xuat_kho_chi_tiet AS a
                INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b ON (a.id = b."ID_CHUNG_TU_CHI_TIET")
                LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL c ON (b."MA_HANG_ID" = cast(c."Value" AS INT))
        
            WHERE b."LOAI_HOAT_DONG_NHAP_XUAT" = 2
                  AND b."HOAT_DONG_CHI_TIET" = 4 -- xuat kho thong thuong
                  AND (b."LOAI_CHUNG_TU" = 2022
                       OR b."LOAI_CHUNG_TU" = 2020
                       OR b."LOAI_CHUNG_TU" = 2021
                       OR b."LOAI_CHUNG_TU" = 2023  -- Xuất kho sản xuất
                       OR b."LOAI_CHUNG_TU" = 2024  -- Xuất kho lắp ráp
                       OR b."LOAI_CHUNG_TU" = 2026 -- Xuất kho từ kiểm kê
                       OR b."LOAI_CHUNG_TU" = 2025                    -- 2025	Xuất kho tháo dỡ
                  )
        
                  AND b."CHI_NHANH_ID" = v_chi_nhanh_id
                  AND b."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                  AND b."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                  AND (
        
                      cast(c."Value" AS INT) IS NOT NULL
                      OR tat_ca_vat_lieu = TRUE
                  )
                  AND a1.id = a.id
            ;
        
        
            --======================= 1.b Update "TONG_TIEN" cho Table IN"XUAT_KHO" ================ */
            --------------- 1.b.1 : update gia tri So tai chinh ------------------
            -- EXEC [Proc_IN_UpdatePrice_Oward_IM_Common_ActionLog] N'Update Voucher xuất kho: "TONG_TIEN" table IN"XUAT_KHO" '
        
            IF (length(DS_MA_VTHH) > 0)
            THEN
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."PHAT_SINH_TRONG_KY_TONG"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON") AS "PHAT_SINH_TRONG_KY_TONG"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."id" IN (
                    SELECT DISTINCT "NHAP_XUAT_ID"
                    FROM stock_ex_nhap_xuat_kho_chi_tiet
                    WHERE
        
                        "MA_HANG_ID" IN (
                            SELECT cast("Value" AS INT)
                            FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL)
                ) AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id AND a1.id = a.id
                ;
        
        
            END IF
            ;
        
        
            --   --======================= 2. Update Price cho Table INTransferDetail ================ */
        
            -- update doi voi truong hop so tai chinh
        
        
            -------------------2.a.1 : update table INTransferDetail -------------------
            UPDATE stock_ex_nhap_xuat_kho_chi_tiet a1
            SET "DON_GIA_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                "DON_GIA"           = b."DON_GIA_DONG",
                "TIEN_VON"          = b."THANH_TIEN_DONG"
            FROM stock_ex_nhap_xuat_kho_chi_tiet AS a
                INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b ON (a.id = b."ID_CHUNG_TU_CHI_TIET")
                LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL c ON (b."MA_HANG_ID" = cast(c."Value" AS INT))
        
            WHERE b."LOAI_HOAT_DONG_NHAP_XUAT" = 2
                  AND b."HOAT_DONG_CHI_TIET" = 5 -- xuat kho : chuyen kho noi bo
                  AND (b."LOAI_CHUNG_TU" = 2030  -- 2030	Xuất kho kiêm vận chuyển nội bộ
                       OR b."LOAI_CHUNG_TU" = 2031 -- 2031	Xuất kho gửi bán đại lý
                       OR b."LOAI_CHUNG_TU" = 2032  -- 2032	Xuất chuyển kho nội bộ
                  )
        
                  AND b."CHI_NHANH_ID" = v_chi_nhanh_id
                  AND b."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                  AND b."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                  AND (
                      cast(c."Value" AS INT) IS NOT NULL
        
                      OR tat_ca_vat_lieu = TRUE) AND a1.id = a.id
            ;
        
            ----- 2.b.1 Update total "SO_TIEN" Finance ------------------
        
        
            IF (length(DS_MA_VTHH) > 0)
            THEN
        
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."id" IN (
                    SELECT DISTINCT "NHAP_XUAT_ID"
                    FROM stock_ex_nhap_xuat_kho_chi_tiet
                    WHERE
        
                        "MA_HANG_ID" IN (SELECT cast("Value" AS INT)
                                         FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL)
                ) AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
        
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a1.id = a.id
                ;
        
        
            END IF
            ;
        
        
            --====================================================================================
            ----------------------3. Update Price cho table IN"NHAP_KHO"	IN"NHAP_KHO"Detail -=======================
            -------------------- 3.a Update cho table IN"NHAP_KHO"  trường hợp nhập kho thành phẩm lắp ráp ---
        
            -- update doi voi truong hop so tai chinh
        
            --======================= 3.a.1 Update Price cho Table IN"NHAP_KHO"Detail ================
            UPDATE stock_ex_nhap_xuat_kho_chi_tiet a1
            SET "DON_GIA_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                "DON_GIA"           = b."DON_GIA_DONG",
                "TIEN_VON_QUY_DOI"  = b."THANH_TIEN_DONG" /*  Sửa bug ID= 123433 ;  a."SO_LUONG" * b."DON_GIA_THEO_DVT_CHINH" ,*/,
                "TIEN_VON"          = b."THANH_TIEN_DONG" /*   a."SO_LUONG" * b."DON_GIA_THEO_DVT_CHINH" */
            FROM stock_ex_nhap_xuat_kho_chi_tiet AS a
                INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b ON (a.id = b."ID_CHUNG_TU_CHI_TIET")
                LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL c ON (b."MA_HANG_ID" = cast(c."Value" AS INT))
        
            WHERE b."LOAI_HOAT_DONG_NHAP_XUAT" = 1     -- Nhập kho lắp ráp: sử dụng nguyên tệ
                  AND (b."LOAI_CHUNG_TU" = 2011)
        
                  AND b."CHI_NHANH_ID" = v_chi_nhanh_id
                  AND b."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                  AND b."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                  AND (
                      cast(c."Value" AS INT) IS NOT NULL
        
                      OR tat_ca_vat_lieu = TRUE) AND a1.id = a.id
            ;
        
            --======================= 3.a.2 Update "TONG_TIEN" cho Table IN"NHAP_KHO" ================ */
            IF (length(DS_MA_VTHH) > 0)
            THEN
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON_QUY_DOI") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."LOAI_CHUNG_TU" = 2011
                      AND a."id" IN (
                    SELECT DISTINCT "NHAP_XUAT_ID"
                    FROM stock_ex_nhap_xuat_kho_chi_tiet
                    WHERE
        
                        "MA_HANG_ID" IN (SELECT cast("Value" AS INT)
                                         FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL)
                ) AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON_QUY_DOI") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."LOAI_CHUNG_TU" = 2011
                      AND a1.id = a.id
                ;
        
        
            END IF
            ;
        
        
            --============================4.  Nhập kho hàng bán trả lại ==============================
            -------------------- .a Update cho table IN"NHAP_KHO" , IN"NHAP_KHO"Detail trường hợp nhập kho hàng bán trả lại ---
            /* 	Nhập kho từ hàng bán trả lại:  Khi giá xuất của bán hàng thay đổi thì giá nhập hàng bán trả lại cũng thay đổi theo , trường hợp Chọn theo giá xuất */
        
            -- update doi voi truong hop so tai chinh
        
        
            --======================= 4.a.1 Update Price cho Table IN"NHAP_KHO"Detail ================
            UPDATE stock_ex_nhap_xuat_kho_chi_tiet a1
            SET "DON_GIA_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                "DON_GIA"           = b."DON_GIA_DONG",
                "TIEN_VON_QUY_DOI"  = b."THANH_TIEN_DONG", /*Sửa bug ID= 123433 : a."SO_LUONG" * b."DON_GIA_THEO_DVT_CHINH" */
                "TIEN_VON"          = b."THANH_TIEN_DONG" /* Sửa bug ID= 123433 ; a."SO_LUONG" * b."DON_GIA_THEO_DVT_CHINH" */
            FROM stock_ex_nhap_xuat_kho_chi_tiet AS a
                INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b ON (a.id = b."ID_CHUNG_TU_CHI_TIET")
                LEFT JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL c ON (b."MA_HANG_ID" = cast(c."Value" AS INT))
        
            WHERE b."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                  AND (b."LOAI_CHUNG_TU" = 2013) -- "LOAI_CHUNG_TU"=2013 : Nhập kho hàng bán trả lại , trường hợp nguyên tệ
        
                  AND b."PHAN_BIET_GIA" = 0 -- Nhập hàng bán trả lại theo giá xuất
                  AND (b."ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                  AND (b."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                  AND b."CHI_NHANH_ID" = v_chi_nhanh_id
                  AND b."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                  AND b."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                  AND (
                      cast(c."Value" AS INT) IS NOT NULL
        
                      OR tat_ca_vat_lieu = TRUE) AND a1.id = a.id
            ;
        
            --======================= 4.a.2 Update "TONG_TIEN" cho Table IN"NHAP_KHO" ================ */
            IF (length(DS_MA_VTHH) > 0)
            THEN
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON_QUY_DOI") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."LOAI_CHUNG_TU" = 2013
                      AND a."id" IN (
                    SELECT DISTINCT "NHAP_XUAT_ID"
                    FROM stock_ex_nhap_xuat_kho_chi_tiet
                    WHERE
        
                        "MA_HANG_ID" IN (SELECT cast("Value" AS INT)
                                         FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL)
        
                ) AND a1.id = a.id
                ;
            ELSE --- tất cả VT trong chi nhánh
        
                UPDATE stock_ex_nhap_xuat_kho a1
                SET "TONG_TIEN" = b."TONG_TIEN"
                FROM stock_ex_nhap_xuat_kho AS a
                    INNER JOIN (SELECT
                                    SUM("TIEN_VON_QUY_DOI") AS "TONG_TIEN"
                                    , "NHAP_XUAT_ID"
                                FROM stock_ex_nhap_xuat_kho_chi_tiet
                                GROUP BY "NHAP_XUAT_ID"
                               ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                WHERE a."NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND a."NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND a."LOAI_CHUNG_TU" = 2013 AND a1.id = a.id
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
		            DROP FUNCTION IF EXISTS CAP_NHAT_TINH_GIA_KO_THEO_KHO_HANG_BAN_TRA_LAI_ANH_HUONG( IN
              ds_id_chung_tu_chi_tiet_anh_huong                            VARCHAR ,
            
                dau_phan_cach                                                VARCHAR ,
            
                 v_chi_nhanh_id                                               INT  ) --Proc_IN_UpdatePriceOW_NoStock_IM_FromTableCaculateTo_InLedger_SAreturnAffect
            ;
            
            CREATE OR REPLACE FUNCTION CAP_NHAT_TINH_GIA_KO_THEO_KHO_HANG_BAN_TRA_LAI_ANH_HUONG(IN
             ds_id_chung_tu_chi_tiet_anh_huong                            VARCHAR ,
            
                dau_phan_cach                                                VARCHAR ,
            
                 v_chi_nhanh_id                                               INT )
            
                RETURNS INT
            AS $$
            DECLARE
            
                ds_id_chung_tu_chi_tiet_anh_huong                            VARCHAR ;
            
                dau_phan_cach                                                VARCHAR ;
            
                 v_chi_nhanh_id                                               INT ;
            
            BEGIN
            
                IF (ds_id_chung_tu_chi_tiet_anh_huong IS NULL)
                THEN
                    ds_id_chung_tu_chi_tiet_anh_huong = ''
                    ;
                END IF
                ;
            
                DROP TABLE IF EXISTS TMP_ID_CHUNG_TU_CHI_TIET
                ;
            
                CREATE TEMP TABLE TMP_ID_CHUNG_TU_CHI_TIET
            
                (
                    Value VARCHAR
            
                )
                ;
            
                INSERT INTO TMP_ID_CHUNG_TU_CHI_TIET
                    SELECT DISTINCT "value"
                    FROM CHUYEN_CHUOI_THANH_BANG(ds_id_chung_tu_chi_tiet_anh_huong,
                                                 dau_phan_cach)
                ;
            
                ----------------------1 Nhập kho hàng bán trả lại ---
            
                UPDATE so_kho_chi_tiet a1
                SET "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA_DONG",
                    "SO_TIEN_NHAP"           = b."THANH_TIEN_DONG_DVT_CHINH"
                FROM so_kho_chi_tiet AS a
                    INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b
                        ON (a."CHI_TIET_ID" = b."ID_CHUNG_TU_CHI_TIET" AND a."CHI_TIET_MODEL" = b."MODEL_CHUNG_TU_TIET"
            
                        )
            
                    INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET D ON a."CHI_TIET_MODEL" || ',' || a."CHI_TIET_ID" = D.Value
            
            
                WHERE a."LOAI_KHU_VUC_NHAP_XUAT" = '1'  /*Nhập kho*/
                      AND a."LA_NHAP_KHO" = TRUE  /*Nhập vào*/
                      AND b."LOAI_HOAT_DONG_NHAP_XUAT" = 1   /* Nhập kho */
                      AND b."HOAT_DONG_CHI_TIET" = 6 /* =6: Nhập kho bán hàng trả lại*/
            
                      AND a."CHI_NHANH_ID" = v_chi_nhanh_id
                      AND (a."ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                      AND (a."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                      AND a1.id = a.id
            
            
                ;
            
            
                ---========================== Sau khi update xong so_kho_chi_tiet thì mới đi update "CHI_PHI_CHUNG""SO_CAI" ====
                ---------------------2. Update cho table "CHI_PHI_CHUNG""SO_CAI" từ table so_kho_chi_tiet------------
                ---------------------- 2.1 Update Debit : Nợ ------
                ---------------------- Nhập kho  ------
            
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_NHAP",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b
                        ON (a."CHI_TIET_ID" = b."CHI_TIET_ID" AND a."CHI_TIET_MODEL" = b."CHI_TIET_MODEL"
                            AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
            
                        )
            
                    INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET D ON a."CHI_TIET_MODEL" || ',' || a."CHI_TIET_ID" = D.Value
            
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id
            
            
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
            
                      AND a1.id = a.id
                ;
            
            
                --   --=========================2.2 Update "GHI_CO" : Có =========================
                --   ---------------------------- Nhập kho ---------------
            
            
                UPDATE so_cai_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_NHAP",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cai_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b
                        ON (a."CHI_TIET_ID" = b."CHI_TIET_ID" AND a."CHI_TIET_MODEL" = b."CHI_TIET_MODEL"
                            AND b."TK_NO_ID" = a."TAI_KHOAN_ID"
            
                        )
            
                    INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET D ON a."CHI_TIET_MODEL" || ',' || a."CHI_TIET_ID" = D.Value
            
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id
            
            
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND a1.id = a.id
                ;
            
            
                -- ---========================== 3 Sau khi update xong so_kho_chi_tiet thì mới đi update so_cong_no_chi_tiet  ====
                -- ---------------------. 3.1 Update cho table so_cong_no_chi_tiet  từ table so_kho_chi_tiet------------
                -- ---------------------- Update Debit : Nợ ------
                -- ---------------------- Nhập kho  ------
            
                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = b."SO_TIEN_NHAP",
                    "GHI_CO"                 = 0,
                    "GHI_NO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "GHI_CO_NGUYEN_TE"       = 0,
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b
                        ON (a."CHI_TIET_ID" = b."CHI_TIET_ID" AND a."CHI_TIET_MODEL" = b."CHI_TIET_MODEL"
                            AND b."TK_NO_ID" = a."TK_ID"
                        )
            
                    INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET D ON a."CHI_TIET_MODEL" || ',' || a."CHI_TIET_ID" = D.Value
            
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id
            
            
                      AND a."LOAI_HACH_TOAN" = '1'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1'
                      AND a1.id = a.id
                ;
            
            
                --   --========================= 3.2. Update "GHI_CO" : Có =========================
                --   ---------------------------- - Nhập kho ---------------
            
                UPDATE so_cong_no_chi_tiet a1
                SET "GHI_NO"                 = 0,
                    "GHI_CO"                 = b."SO_TIEN_NHAP",
                    "GHI_NO_NGUYEN_TE"       = 0,
                    "GHI_CO_NGUYEN_TE"       = b."SO_TIEN_NHAP",
                    "DON_GIA"                = b."DON_GIA",
                    "DON_GIA_NGUYEN_TE"      = b."DON_GIA",
                    "DON_GIA_THEO_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH"
                FROM so_cong_no_chi_tiet AS a
                    INNER JOIN so_kho_chi_tiet AS b
                        ON (a."CHI_TIET_ID" = b."CHI_TIET_ID" AND a."CHI_TIET_MODEL" = b."CHI_TIET_MODEL"
                            AND b."TK_NO_ID" = a."TK_ID"
                        )
            
                    INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET D ON a."CHI_TIET_MODEL" || ',' || a."CHI_TIET_ID" = D.Value
            
                WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id
            
                      AND a."LOAI_HACH_TOAN" = '2'
                      AND b."LOAI_KHU_VUC_NHAP_XUAT" = '1' /*"LOAI_KHU_VUC_NHAP_XUAT"=1: Nhập kho */
                      AND a1.id = a.id
                ;
            
                RETURN 0
                ;
            END
            ;
            $$ LANGUAGE PLpgSQL
            ;
            

            """)


        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHUNG_TU_HANG_BAN_TRA_LAI_ANH_HUONG( IN
            ds_id_chung_tu_chi_tiet_anh_huong VARCHAR,

            dau_phan_cach VARCHAR,

            v_chi_nhanh_id INT ) --Proc_IN_UpdatePriceOW_NoStock_IM_FromTableCaculateTo_Vouchers_SAreturnAffect
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHUNG_TU_HANG_BAN_TRA_LAI_ANH_HUONG(IN
            ds_id_chung_tu_chi_tiet_anh_huong VARCHAR,

            dau_phan_cach                     VARCHAR,

            v_chi_nhanh_id                    INT)

                RETURNS INT
            AS $$
            DECLARE

                ds_id_chung_tu_chi_tiet_anh_huong VARCHAR;

                dau_phan_cach                     VARCHAR;

                v_chi_nhanh_id                    INT;
                 CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO BOOLEAN;

            BEGIN

                IF (ds_id_chung_tu_chi_tiet_anh_huong IS NULL)
                THEN
                    ds_id_chung_tu_chi_tiet_anh_huong = ''
                    ;
                END IF
                ;

                DROP TABLE IF EXISTS TMP_ID_CHUNG_TU_CHI_TIET
                ;

                CREATE TEMP TABLE TMP_ID_CHUNG_TU_CHI_TIET

                (
                    Value VARCHAR

                )
                ;

                INSERT INTO TMP_ID_CHUNG_TU_CHI_TIET
                    SELECT DISTINCT "value"
                    FROM CHUYEN_CHUOI_THANH_BANG(ds_id_chung_tu_chi_tiet_anh_huong,
                                                 dau_phan_cach)
                ;

                 SELECT value
                INTO CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO
                FROM ir_config_parameter
                WHERE key = 'he_thong.CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO'
                FETCH FIRST 1 ROW ONLY
                ;


                IF (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = TRUE)

                -- update doi voi truong hop so tai chinh
                THEN

                    --======================= 4.a.1 Update Price cho Table IN"NHAP_KHO"Detail ================

                    UPDATE stock_ex_nhap_xuat_kho_chi_tiet a1
                    SET "DON_GIA_DVT_CHINH" = b."DON_GIA_THEO_DVT_CHINH",
                        "DON_GIA"           = b."DON_GIA_DONG",
                        "TIEN_VON_QUY_DOI"  = b."THANH_TIEN_DONG_DVT_CHINH", /*Sửa bug ID= 123433 :  a."SO_LUONG" * b."DON_GIA_THEO_DVT_CHINH"t */
                        "TIEN_VON"          = b."THANH_TIEN_DONG_DVT_CHINH" /*Sửa bug ID= 123433 :  a."SO_LUONG" * b."DON_GIA_THEO_DVT_CHINH" */
                    FROM stock_ex_nhap_xuat_kho_chi_tiet AS a
                        INNER JOIN stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho AS b ON (a.id = b."ID_CHUNG_TU_CHI_TIET")

                        INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET C ON a.id = CAST(C.Value AS INT)
                    WHERE b."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                          AND (b."LOAI_CHUNG_TU" = 2013) -- "LOAI_CHUNG_TU"=2013 : Nhập kho hàng bán trả lại , trường hợp nguyên tệ

                          AND b."PHAN_BIET_GIA" = 0 -- "PHAN_BIET_GIA"=0: Nhập hàng bán trả lại theo giá xuất
                          AND (b."ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                          AND (b."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                          AND b."CHI_NHANH_ID" = v_chi_nhanh_id
                          AND a1.id = a.id

                    ;

                    --======================= 4.a.2 Update "PHAT_SINH_TRONG_KY_TONG"Finance cho Table IN"NHAP_KHO" ================ */

                    UPDATE stock_ex_nhap_xuat_kho a1
                    SET "TONG_TIEN" = b."PHAT_SINH_TRONG_KY_TONG"
                    FROM stock_ex_nhap_xuat_kho AS a
                        INNER JOIN (SELECT
                                        SUM("TIEN_VON_QUY_DOI") AS "PHAT_SINH_TRONG_KY_TONG"
                                        , "NHAP_XUAT_ID"
                                    FROM stock_ex_nhap_xuat_kho_chi_tiet
                                    GROUP BY "NHAP_XUAT_ID"
                                   ) AS b ON (a."id" = b."NHAP_XUAT_ID")
                    WHERE a."CHI_NHANH_ID" = v_chi_nhanh_id
                          AND a."LOAI_CHUNG_TU" = 2013
                          AND a."id" IN (
                        SELECT "NHAP_XUAT_ID"
                        FROM stock_ex_nhap_xuat_kho_chi_tiet A

                            INNER JOIN TMP_ID_CHUNG_TU_CHI_TIET C ON a."id" = CAST(C.Value AS INT)

                        GROUP BY "NHAP_XUAT_ID")
                          AND a1.id = a.id
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
			DROP FUNCTION IF EXISTS CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO( IN
             v_chi_nhanh_id                                               INT ,
            
            v_tu_ngay                                                    TIMESTAMP,
            
            v_den_ngay                                                   TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM_UpdateAllData_WhenSaReturnVouchersAffect
            ;
            
            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO(IN
             v_chi_nhanh_id                                               INT ,
            
            v_tu_ngay                                                    TIMESTAMP,
            
            v_den_ngay                                                   TIMESTAMP )
            
                RETURNS INT
            AS $$
            DECLARE
                v_tu_ngay                                                    TIMESTAMP ;
            
               
            
                v_den_ngay                                                   TIMESTAMP ;
            
              
            
                v_chi_nhanh_id                                               INT ;
            
                v_tu_ngay_khong_thoi_gian                                    TIMESTAMP;
            
                --@FromDate_NoTime
            
                v_den_ngay_khong_thoi_gian                                   TIMESTAMP;
            
                ToDateTime_CrrNoTime                                         TIMESTAMP;
            
                ds_id_chung_tu_chi_tiet_anh_huong                            VARCHAR;
            
                PHAN_THAP_PHAN_SO_LUONG                                      INT;
            
                PHAN_THAP_PHAN_DON_GIA                                       INT;
            
                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI                               INT;
            
                CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO BOOLEAN;
            
            
            
            BEGIN
            
                ------ Step 5: Cập nhật giá hàng bán trả lại và Số lieu sổ cái + các chứng từ
            
                v_tu_ngay_khong_thoi_gian = lay_ngay_thang(v_tu_ngay)
                ;
            
                v_den_ngay_khong_thoi_gian = lay_ngay_thang(v_den_ngay)
                ;
            
            
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
            
                IF (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = FALSE)
                THEN
                    RETURN 0
                    ;
            
                    --- ko cập nhật giá nhập kho cho chứng từ hàng bán trả lại
                END IF
                ;
            
            
                SELECT DISTINCT SUBSTR(Cast("CHI_TIET_MODEL" AS VARCHAR(255)), 1, 255) || ',' ||
                                SUBSTR(Cast("CHI_TIET_ID" AS VARCHAR(255)), 1, 255) || ';'
                INTO ds_id_chung_tu_chi_tiet_anh_huong
            
                FROM so_kho_chi_tiet
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
            
                      AND ("ID_CHUNG_TU_XUAT_KHO" IS NOT NULL)
                      AND "ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IN (
                    SELECT "CHI_TIET_ID"
                    FROM so_kho_chi_tiet
                    WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
            
                          AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                          AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
                          AND "LOAI_KHU_VUC_NHAP_XUAT" = '3')/* "LOAI_KHU_VUC_NHAP_XUAT" = 3 : là xuất kho */
                      AND "PHUONG_THUC_THANH_TOAN" = '0'
                ;
            
                /*0 = Lấy từ giá xuất bán; 1 = Nhập đơn giá bằng tay */
            
                --RAISE NOTICE '2%',ds_id_chung_tu_chi_tiet_anh_huong;
            
            
                DROP TABLE IF EXISTS TMP_CHUNG_TU_TRA_LAI_HANG_BAN
                ;
            
                CREATE TEMP TABLE TMP_CHUNG_TU_TRA_LAI_HANG_BAN
                    AS
            
            
                        SELECT
            
                            A."CHI_TIET_ID"
                            , "CHI_TIET_MODEL"
                            , "ID_CHUNG_TU_XUAT_KHO"
                            , "MODEL_CHUNG_TU_XUAT_KHO"
                            , "ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                            , "MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET"
            
                            , A."DVT_ID"
                            , A."TY_LE_CHUYEN_DOI"
                            , A."PHEP_TINH_CHUYEN_DOI" AS "PHEP_TINH_CHUYEN_DOI"
            
                        FROM so_kho_chi_tiet A
                        WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
            
                              AND ("ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                              AND "ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IN (
                            SELECT "CHI_TIET_ID"
                            FROM so_kho_chi_tiet
                            WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
            
                                  AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                                  AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
                                  AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                        )/* "LOAI_KHU_VUC_NHAP_XUAT" = 3 : là xuất kho */
                              AND "PHUONG_THUC_THANH_TOAN" = '0' /*0 = Lấy từ giá xuất bán; 1 = Nhập đơn giá bằng tay */
            
            
                        GROUP BY
                            A."CHI_TIET_ID"
                            , "CHI_TIET_MODEL"
                            , "ID_CHUNG_TU_XUAT_KHO"
                            , "MODEL_CHUNG_TU_XUAT_KHO"
                            , "ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                            , "MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET"
            
                            , A."DVT_ID"
                            , A."TY_LE_CHUYEN_DOI"
                            , A."PHEP_TINH_CHUYEN_DOI"
                ;
            
            
                ---=================== 1.khai bao phan lam tron------
            
                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;
            
                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;
            
                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;
            
            
                IF (PHAN_THAP_PHAN_SO_LUONG IS NULL)
                THEN
            
            
                    PHAN_THAP_PHAN_SO_LUONG = 0
                    ;
                END IF
                ;
            
            
                IF (PHAN_THAP_PHAN_DON_GIA IS NULL)
                THEN
            
            
                    PHAN_THAP_PHAN_DON_GIA = 0
                    ;
                END IF
                ;
            
            
                IF (PHAN_THAP_PHAN_SO_TIEN_QUY_DOI IS NULL)
                THEN
            
            
                    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI = 0
                    ;
                END IF
                ;
            
                ----------------------------- Tạo bảng tạm chứa giá trị xuất kho của phiếu kho bán hàng có hàng bán trả lại
            
                DROP TABLE IF EXISTS TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI
                ;
            
                CREATE TEMP TABLE TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI
                    AS
            
                        SELECT
            
                            B."CHI_TIET_ID"
                            , B."CHI_TIET_MODEL"
                            , ROUND(CAST(COALESCE(A."DON_GIA_THEO_DVT_CHINH", 0) AS NUMERIC),
                                    PHAN_THAP_PHAN_DON_GIA) AS "GIA_TRI_DON_GIA_THEO_DVT_CHINH"
                            , CASE
            
                              WHEN B."DVT_ID" = A."MA_DON_VI_TINH_ID" OR (B."DVT_ID" IS NULL AND A."MA_DON_VI_TINH_ID" IS NULL)
                                  THEN
                                      ROUND(CAST(COALESCE("DON_GIA_DONG", 0) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                              ELSE
                                  CASE WHEN B."TY_LE_CHUYEN_DOI" = 0
                                      THEN 0
                                  WHEN B."PHEP_TINH_CHUYEN_DOI" = '*'
                                      THEN ROUND(CAST(COALESCE(A."DON_GIA_THEO_DVT_CHINH" * B."TY_LE_CHUYEN_DOI", 0) AS NUMERIC),
                                                 PHAN_THAP_PHAN_DON_GIA)
                                  ELSE ROUND(CAST(COALESCE(A."DON_GIA_THEO_DVT_CHINH" / B."TY_LE_CHUYEN_DOI", 0) AS NUMERIC),
                                             PHAN_THAP_PHAN_DON_GIA)
                                  END
                              END
                                                            AS "GIA_TRI_DON_GIA_DONG"
                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
                            INNER JOIN TMP_CHUNG_TU_TRA_LAI_HANG_BAN B ON (A."ID_CHUNG_TU" = B."ID_CHUNG_TU_XUAT_KHO"
                                                                           AND A."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" =
                                                                               B."ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                                )
                        WHERE "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                ;
            
            
                --- 2. Update giá trị Price vào chứng từ háng bán trả lại
                --- 2.1  Update giá trị Price vào table khong theo kho
            
            
                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A1
                SET
            
                    "DON_GIA_DONG"                           = C."GIA_TRI_DON_GIA_DONG"
                    , "DON_GIA_THEO_DVT_CHINH"               = C."GIA_TRI_DON_GIA_THEO_DVT_CHINH"
                    ,
                    "THANH_TIEN_DONG"                        = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
            
                    ,
                    "THANH_TIEN_DONG_DVT_CHINH"              = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                    , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
            
                    , "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"  = NULL
                    , "TONG_GIA_TRI_LUY_KE_KHO"              = NULL
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
            
            
                    INNER JOIN TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI C
                        ON A."ID_CHUNG_TU_CHI_TIET" = C."CHI_TIET_ID" AND A."MODEL_CHUNG_TU_TIET" = C."CHI_TIET_MODEL"
            
                WHERE
                    A."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                    AND A."HOAT_DONG_CHI_TIET" = 6
                    AND A."PHAN_BIET_GIA" = 0
            
                    AND A1.id = A.id
                ;
            
            
                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A1
                SET
                    "DON_GIA_DONG"                           = C."GIA_TRI_DON_GIA_DONG"
                    , "DON_GIA_THEO_DVT_CHINH"               = C."GIA_TRI_DON_GIA_THEO_DVT_CHINH"
                    ,
                    "THANH_TIEN_DONG"                        = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
            
                    ,
                    "THANH_TIEN_DONG_DVT_CHINH"              = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                    , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP
            
                    , "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"  = NULL
                    , "TONG_GIA_TRI_LUY_KE_KHO"              = NULL
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A
            
                    INNER JOIN TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI C
                        ON A."ID_CHUNG_TU_CHI_TIET" = C."CHI_TIET_ID" AND A."MODEL_CHUNG_TU_TIET" = C."CHI_TIET_MODEL"
                WHERE
                    A."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                    AND A."HOAT_DONG_CHI_TIET" = 6
            
                    AND A."PHAN_BIET_GIA" = 0
                    AND A1.id = A.id
                ;
            
                --=========================== 2.2 : update to InventoryLedger, GeneralLedger, AccountObjectsLedger tù price của table InventoryItemPriceOutwardImmeNoStock: OK
            
                PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_HANG_BAN_TRA_LAI_ANH_HUONG(ds_id_chung_tu_chi_tiet_anh_huong, ';',
                                                                              v_chi_nhanh_id)
                ;
            
                --======================== 2.3 : Update to Vouchers: OK
            
            
               PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHUNG_TU_HANG_BAN_TRA_LAI_ANH_HUONG(ds_id_chung_tu_chi_tiet_anh_huong, ';',
                                                                                       v_chi_nhanh_id)
                ;
            
            
                RETURN 0
                ;
            
            END
            ;
            $$ LANGUAGE PLpgSQL
            ;        
            """)


        self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI( IN
		v_chi_nhanh_id INT,

		v_tu_ngay TIMESTAMP,

		v_den_ngay TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM_ReComputeUP_LedgerVchersInBranchFromDaToDateExistDataOWTable
		;

		CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI(IN
		v_chi_nhanh_id INT,

		v_tu_ngay      TIMESTAMP,

		v_den_ngay     TIMESTAMP)

			RETURNS INT
		AS $$
		DECLARE
			v_tu_ngay                  TIMESTAMP ;

			v_den_ngay                 TIMESTAMP ;	

			v_chi_nhanh_id             INT ;

			v_tu_ngay_khong_thoi_gian  TIMESTAMP;

			--@FromDate_NoTime

			v_den_ngay_khong_thoi_gian TIMESTAMP;

			ToDateTime_CrrNoTime       TIMESTAMP;

			DS_MA_VTHH                 VARCHAR ;

			--@ListInventoryItemID


		BEGIN


			v_tu_ngay_khong_thoi_gian = lay_ngay_thang(v_tu_ngay)
			;

			ToDateTime_CrrNoTime = lay_ngay_thang(v_den_ngay)
			;

			v_den_ngay_khong_thoi_gian = lay_ngay_thang(v_den_ngay)
			;

			DS_MA_VTHH = (SELECT string_agg("MA_HANG_STR", ';')
						  FROM (SELECT Cast(A."MA_HANG_ID" AS VARCHAR(255)) AS "MA_HANG_STR"
								FROM so_kho_chi_tiet AS A

								WHERE "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
									  AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
									  AND "CHI_NHANH_ID" = v_chi_nhanh_id
								GROUP BY "MA_HANG_ID") b
			)
			;


			DROP TABLE IF EXISTS TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI
			;

			CREATE TEMP TABLE TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI

			(
				"MA_VTHH_ID" INT PRIMARY KEY
			)
			;

			--------- insert danh sach vat tu vao table TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI, tat ca vat tu trong cac chứng từ---
			INSERT INTO TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI
				SELECT "MA_HANG_ID"
				FROM so_kho_chi_tiet
				WHERE "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
					  AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
					  AND "CHI_NHANH_ID" = v_chi_nhanh_id

				GROUP BY "MA_HANG_ID"
			;


			IF (NOT EXISTS(SELECT *
						   FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI
						   LIMIT 1)
			)
			THEN
				RETURN 0
				;
			END IF
			;


			UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
			SET "HANH_DONG_TREN_VAT_TU" = B."ROW"
			FROM
				(SELECT
					 ROW_NUMBER()
					 OVER (
						 PARTITION BY E."MA_HANG_ID"
						 ORDER BY "THOI_GIAN_HOAT_DONG", "STT", "LOAI_HOAT_DONG_NHAP_XUAT" DESC ) AS "ROW"
					 , "id"
					 , E."MA_HANG_ID"
				 FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho E
					 INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_TAT_CA_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI C ON C."MA_VTHH_ID" = E."MA_HANG_ID"
				 WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

				) B
			WHERE A.id = B.id

			;


			--============ Step 1.1 : Update lại IsCaculateByStock=0 - ko theo kho cho các row bị tính giá
			UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
			SET "IsCaculateByStock" = FALSE
			WHERE
				"CHI_NHANH_ID" = v_chi_nhanh_id

				AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
				AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
			;

			-- update lại theo kho , ID= 34202
			UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
			SET "IsCaculateByStock" = FALSE
			WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
				  AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
			;

			--------------- 2.2 chạy store để thực hiện tính lại giá : OK ---------

			PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_VAT_TU_TRONG_1_CHI_NHANH_TU_NGAY_DEN_NGAY(DS_MA_VTHH, ';',
																								v_chi_nhanh_id, v_tu_ngay,
																								v_den_ngay)
			;


			----------------- Step 3: Cập nhật giá sau khi tính vào table InventoryLedger, GeneralLedger, AccountObjectLedger:  ---------------

			PERFORM CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY(DS_MA_VTHH, ';',
																									v_tu_ngay, v_den_ngay,
																									v_chi_nhanh_id)
			;

			----------------- Step 4: Cập nhật giá sau khi tính vào table chứng từ kho master và Detail: ----

			PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL(DS_MA_VTHH, ';',
																						 v_tu_ngay, v_den_ngay, v_chi_nhanh_id)
			;


			------ Step 5: Cập nhật giá hàng bán trả lại và Số lieu sổ cái + các chứng từ

			PERFORM CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO(
				v_chi_nhanh_id, v_tu_ngay, v_den_ngay)
			;

             DELETE  FROM STOCK_EX_LOG_UNPOST_VAT_TU_HANG_HOA
            WHERE   "CHI_NHANH_ID" = v_chi_nhanh_id

            AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
            AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime ;


			RETURN 0
			;

		END
		;
		$$ LANGUAGE PLpgSQL
		;


            """)


        self.env.cr.execute(""" 
			            DROP FUNCTION IF EXISTS CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH( IN

            ds_vat_tu_hang_hoa_id VARCHAR,

            dau_phan_cach VARCHAR,

            v_chi_nhanh_id INT,

            v_tu_ngay TIMESTAMP,

            v_den_ngay TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM_UpdateAllData_WhenSaReturnVouchersAffect_ListItemID
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH(IN

            ds_vat_tu_hang_hoa_id VARCHAR,
            
            dau_phan_cach         VARCHAR,

            v_chi_nhanh_id        INT,

            v_tu_ngay             TIMESTAMP,

            v_den_ngay            TIMESTAMP)

                RETURNS INT
            AS $$
            DECLARE
                v_tu_ngay                                                    TIMESTAMP;


                v_den_ngay                                                   TIMESTAMP;


                v_chi_nhanh_id                                               INT;

                v_tu_ngay_khong_thoi_gian                                    TIMESTAMP;

                --@FromDate_NoTime

                v_den_ngay_khong_thoi_gian                                   TIMESTAMP;

                ToDateTime_CrrNoTime                                         TIMESTAMP;

                ds_id_chung_tu_chi_tiet_anh_huong                            VARCHAR;

                PHAN_THAP_PHAN_SO_LUONG                                      INT;

                PHAN_THAP_PHAN_DON_GIA                                       INT;

                PHAN_THAP_PHAN_SO_TIEN_QUY_DOI                               INT;

                CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO BOOLEAN;


                ds_vat_tu_hang_hoa_id                                        VARCHAR;

                dau_phan_cach                                                VARCHAR;


            BEGIN

              

                v_tu_ngay_khong_thoi_gian = lay_ngay_thang(v_tu_ngay)
                ;

                v_den_ngay_khong_thoi_gian = lay_ngay_thang(v_den_ngay)
                ;


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

                IF (CAP_NHAT_GIA_NHAP_KHO_HANG_BAN_TRA_LAI_KHI_TINH_GIA_XUAT_KHO = FALSE)
                THEN
                    RETURN 0
                    ;

                    --- ko cập nhật giá nhập kho cho chứng từ hàng bán trả lại
                END IF
                ;

                DROP TABLE IF EXISTS TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH
                ;

                CREATE TEMP TABLE TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH

                (
                    "MA_VTHH_ID" VARCHAR
                )
                ;

                --------- insert danh sach vat tu vao table TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI, tat ca vat tu trong cac chứng từ---
                INSERT INTO TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH
                    SELECT DISTINCT *
                    FROM chuyen_chuoi_thanh_bang(ds_vat_tu_hang_hoa_id, dau_phan_cach)

                ;


                SELECT DISTINCT SUBSTR(Cast(A."CHI_TIET_MODEL" AS VARCHAR(255)), 1, 255) || ',' ||
                                SUBSTR(Cast(A."CHI_TIET_ID" AS VARCHAR(255)), 1, 255) || ';'
                INTO ds_id_chung_tu_chi_tiet_anh_huong

                FROM so_kho_chi_tiet A /*hoant 09.01.2017 thay phép in bằng innner join */
                    INNER JOIN (SELECT "CHI_TIET_ID"
                                FROM so_kho_chi_tiet
                                WHERE
                                    "CHI_NHANH_ID" = v_chi_nhanh_id

                                    AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                                    AND "NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                                    AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                               ) B ON A."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" = B."CHI_TIET_ID"

                    INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH D
                        ON a."MA_HANG_ID" = CAST(D."MA_VTHH_ID" AS INT)
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

                      AND ("ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)
                      AND "PHUONG_THUC_THANH_TOAN" = '0'
                ;

                /*0 = Lấy từ giá xuất bán; 1 = Nhập đơn giá bằng tay */

                --RAISE NOTICE '2%',ds_id_chung_tu_chi_tiet_anh_huong;


                DROP TABLE IF EXISTS TMP_CHUNG_TU_TRA_LAI_HANG_BAN_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH
                ;

                CREATE TEMP TABLE TMP_CHUNG_TU_TRA_LAI_HANG_BAN_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH
                    AS


                        SELECT

                            A."CHI_TIET_ID"
                            , "CHI_TIET_MODEL"
                            , "ID_CHUNG_TU_XUAT_KHO"
                            , "MODEL_CHUNG_TU_XUAT_KHO"
                            , "ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                            , "MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET"

                            , A."DVT_ID"
                            , A."TY_LE_CHUYEN_DOI"
                            , A."PHEP_TINH_CHUYEN_DOI" AS "PHEP_TINH_CHUYEN_DOI"

                        FROM so_kho_chi_tiet A
                            INNER JOIN (SELECT "CHI_TIET_ID"
                                        FROM so_kho_chi_tiet
                                        WHERE
                                            "CHI_NHANH_ID" = v_chi_nhanh_id

                                            AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                                            AND "NGAY_HACH_TOAN" <= v_den_ngay_khong_thoi_gian
                                            AND "LOAI_KHU_VUC_NHAP_XUAT" = '3'
                                       ) B ON A."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" = B."CHI_TIET_ID"

                            INNER JOIN
                            TMP_VAT_TU_HANG_HOA_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH D
                                ON a."MA_HANG_ID" = CAST(D."MA_VTHH_ID" AS INT)

                        WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

                              AND ("ID_CHUNG_TU_XUAT_KHO_CHI_TIET" IS NOT NULL)

                              AND "PHUONG_THUC_THANH_TOAN" = '0' /*0 = Lấy từ giá xuất bán; 1 = Nhập đơn giá bằng tay */


                        GROUP BY
                            A."CHI_TIET_ID"
                            , "CHI_TIET_MODEL"
                            , "ID_CHUNG_TU_XUAT_KHO"
                            , "MODEL_CHUNG_TU_XUAT_KHO"
                            , "ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                            , "MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET"

                            , A."DVT_ID"
                            , A."TY_LE_CHUYEN_DOI"
                            , A."PHEP_TINH_CHUYEN_DOI"
                ;


                ---=================== 1.khai bao phan lam tron------

                SELECT value
                INTO PHAN_THAP_PHAN_SO_LUONG
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_DON_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
                FETCH FIRST 1 ROW ONLY
                ;


                IF (PHAN_THAP_PHAN_SO_LUONG IS NULL)
                THEN


                    PHAN_THAP_PHAN_SO_LUONG = 0
                    ;
                END IF
                ;


                IF (PHAN_THAP_PHAN_DON_GIA IS NULL)
                THEN


                    PHAN_THAP_PHAN_DON_GIA = 0
                    ;
                END IF
                ;


                IF (PHAN_THAP_PHAN_SO_TIEN_QUY_DOI IS NULL)
                THEN


                    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI = 0
                    ;
                END IF
                ;

                ----------------------------- Tạo bảng tạm chứa giá trị xuất kho của phiếu kho bán hàng có hàng bán trả lại

                DROP TABLE IF EXISTS TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI
                ;

                CREATE TEMP TABLE TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI
                    AS

                        SELECT

                            B."CHI_TIET_ID"
                            , B."CHI_TIET_MODEL"
                            , ROUND(CAST(COALESCE(A."DON_GIA_THEO_DVT_CHINH", 0) AS NUMERIC),
                                    PHAN_THAP_PHAN_DON_GIA) AS "GIA_TRI_DON_GIA_THEO_DVT_CHINH"
                            , CASE

                              WHEN B."DVT_ID" = A."MA_DON_VI_TINH_ID" OR (B."DVT_ID" IS NULL AND A."MA_DON_VI_TINH_ID" IS NULL)
                                  THEN
                                      ROUND(CAST(COALESCE("DON_GIA_DONG", 0) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
                              ELSE
                                  CASE WHEN B."TY_LE_CHUYEN_DOI" = 0
                                      THEN 0
                                  WHEN B."PHEP_TINH_CHUYEN_DOI" = '*'
                                      THEN ROUND(CAST(COALESCE(A."DON_GIA_THEO_DVT_CHINH" * B."TY_LE_CHUYEN_DOI", 0) AS NUMERIC),
                                                 PHAN_THAP_PHAN_DON_GIA)
                                  ELSE ROUND(CAST(COALESCE(A."DON_GIA_THEO_DVT_CHINH" / B."TY_LE_CHUYEN_DOI", 0) AS NUMERIC),
                                             PHAN_THAP_PHAN_DON_GIA)
                                  END
                              END
                                                            AS "GIA_TRI_DON_GIA_DONG"
                        FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
                            INNER JOIN
                            TMP_CHUNG_TU_TRA_LAI_HANG_BAN_CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH B
                                ON (A."ID_CHUNG_TU" = B."ID_CHUNG_TU_XUAT_KHO"
                                    AND A."ID_CHUNG_TU_XUAT_KHO_CHI_TIET" =
                                        B."ID_CHUNG_TU_XUAT_KHO_CHI_TIET"
                                )
                        WHERE "LOAI_HOAT_DONG_NHAP_XUAT" = 2
                ;


                --- 2. Update giá trị Price vào chứng từ háng bán trả lại
                --- 2.1  Update giá trị Price vào table khong theo kho


                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A1
                SET

                    "DON_GIA_DONG"                           = C."GIA_TRI_DON_GIA_DONG"
                    , "DON_GIA_THEO_DVT_CHINH"               = C."GIA_TRI_DON_GIA_THEO_DVT_CHINH"
                    ,
                    "THANH_TIEN_DONG"                        = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)

                    ,
                    "THANH_TIEN_DONG_DVT_CHINH"              = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                    , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP

                    , "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"  = NULL
                    , "TONG_GIA_TRI_LUY_KE_KHO"              = NULL
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A


                    INNER JOIN TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI C
                        ON A."ID_CHUNG_TU_CHI_TIET" = C."CHI_TIET_ID" AND A."MODEL_CHUNG_TU_TIET" = C."CHI_TIET_MODEL"

                WHERE
                    A."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                    AND A."HOAT_DONG_CHI_TIET" = 6
                    AND A."PHAN_BIET_GIA" = 0

                    AND A1.id = A.id
                ;


                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A1
                SET
                    "DON_GIA_DONG"                           = C."GIA_TRI_DON_GIA_DONG"
                    , "DON_GIA_THEO_DVT_CHINH"               = C."GIA_TRI_DON_GIA_THEO_DVT_CHINH"
                    ,
                    "THANH_TIEN_DONG"                        = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)

                    ,
                    "THANH_TIEN_DONG_DVT_CHINH"              = ROUND(
                        CAST((C."GIA_TRI_DON_GIA_DONG" * A."SO_LUONG_VAT_TU") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
                    , "THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT" = LOCALTIMESTAMP

                    , "SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH"  = NULL
                    , "TONG_GIA_TRI_LUY_KE_KHO"              = NULL
                FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho A

                    INNER JOIN TMP_GIA_TRI_XUAT_KHO_HANG_BAN_TRA_LAI C
                        ON A."ID_CHUNG_TU_CHI_TIET" = C."CHI_TIET_ID" AND A."MODEL_CHUNG_TU_TIET" = C."CHI_TIET_MODEL"
                WHERE
                    A."LOAI_HOAT_DONG_NHAP_XUAT" = 1
                    AND A."HOAT_DONG_CHI_TIET" = 6

                    AND A."PHAN_BIET_GIA" = 0
                    AND A1.id = A.id
                ;

                --=========================== 2.2 : update to InventoryLedger, GeneralLedger, AccountObjectsLedger tù price của table InventoryItemPriceOutwardImmeNoStock: OK

                PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_HANG_BAN_TRA_LAI_ANH_HUONG(ds_id_chung_tu_chi_tiet_anh_huong, ';',
                                                                                 v_chi_nhanh_id)
                ;

                --======================== 2.3 : Update to Vouchers: OK

                PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHUNG_TU_HANG_BAN_TRA_LAI_ANH_HUONG(ds_id_chung_tu_chi_tiet_anh_huong, ';',
                                                                                          v_chi_nhanh_id)
                ;

                RETURN 0
                ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;


    

            """)

        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI( IN

            ds_vat_tu_hang_hoa_id VARCHAR,

            dau_phan_cach VARCHAR,

            v_chi_nhanh_id INT,

            v_tu_ngay TIMESTAMP,

            v_den_ngay TIMESTAMP ) --Proc_IN_UpdatePriceOW_NoStock_IM_ReComputeUP_LedgerVouchersListInventoryItemIDs
            ;

            CREATE OR REPLACE FUNCTION CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI(IN
            ds_vat_tu_hang_hoa_id VARCHAR,

            dau_phan_cach VARCHAR,

            v_chi_nhanh_id INT,

            v_tu_ngay TIMESTAMP,

            v_den_ngay TIMESTAMP )

                RETURNS INT
            AS $$
            DECLARE
                v_tu_ngay                  TIMESTAMP ;           

                v_den_ngay                 TIMESTAMP ;
           
                v_chi_nhanh_id             INT ;

                v_tu_ngay_khong_thoi_gian  TIMESTAMP;

                --@FromDate_NoTime

                v_den_ngay_khong_thoi_gian TIMESTAMP;

                ToDateTime_CrrNoTime       TIMESTAMP;

                ds_vat_tu_hang_hoa_id      VARCHAR ;

                --@ListInventoryItemID

                dau_phan_cach              VARCHAR ;


            BEGIN


                v_tu_ngay_khong_thoi_gian = lay_ngay_thang(v_tu_ngay)
                ;

                ToDateTime_CrrNoTime = lay_ngay_thang(v_den_ngay)
                ;

                v_den_ngay_khong_thoi_gian = lay_ngay_thang(v_den_ngay)
                ;

                DROP TABLE IF EXISTS TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI
                ;

                CREATE TEMP TABLE TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI

                (
                    "MA_VTHH_ID" VARCHAR
                )
                ;

                --------- insert danh sach vat tu vao table TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI, tat ca vat tu trong cac chứng từ---
                INSERT INTO TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI
                    SELECT DISTINCT *
                    FROM chuyen_chuoi_thanh_bang(ds_vat_tu_hang_hoa_id, dau_phan_cach)

                ;


                IF (NOT EXISTS(SELECT *
                               FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI
                               LIMIT 1)
                )
                THEN
                    RETURN 0
                    ;
                END IF
                ;


                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
                SET "HANH_DONG_TREN_VAT_TU" = B."ROW"
                FROM
                    (SELECT
                         ROW_NUMBER()
                         OVER (
                             PARTITION BY A."MA_HANG_ID"
                             ORDER BY "THOI_GIAN_HOAT_DONG", "STT", "LOAI_HOAT_DONG_NHAP_XUAT" DESC ) AS "ROW"
                         , "id"
                         , A."MA_HANG_ID"
                     FROM stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho A
                         INNER JOIN TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI B
                             ON cast(B."MA_VTHH_ID" AS INT) = A."MA_HANG_ID"
                     WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

                    ) B
                WHERE A.id = B.id
                ;

                --============ Step 1.1 : Update lại IsCaculateByStock=0 - ko theo kho cho các row bị tính giá
                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
                SET "IsCaculateByStock" = FALSE
                WHERE
                    "CHI_NHANH_ID" = v_chi_nhanh_id

                    AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                    AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
                    AND "MA_HANG_ID" IN (SELECT cast("MA_VTHH_ID" AS INT)
                                         FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI)
                ;


                UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
                SET "IsCaculateByStock" = FALSE
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id
                      AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
                      AND "MA_HANG_ID" IN (SELECT cast("MA_VTHH_ID" AS INT)
                                           FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI)
                ;


                --------------- 2.2 chạy store để thực hiện tính lại giá : OK ---------

                PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_VAT_TU_TRONG_1_CHI_NHANH_TU_NGAY_DEN_NGAY(ds_vat_tu_hang_hoa_id, ';',
                                                                                                    v_chi_nhanh_id, v_tu_ngay,
                                                                                                    v_den_ngay)
                ;


                ----------------- Step 3: Cập nhật giá sau khi tính vào table InventoryLedger, GeneralLedger, AccountObjectLedger:  ---------------

                PERFORM CAP_NHAT_GIA_CHO_SO_KHO_SO_CONG_NO_SO_CAI_TINH_GIA_KO_THEO_KHO_TU_NGAY_DEN_NGAY(ds_vat_tu_hang_hoa_id, ';',
                                                                                                        v_tu_ngay, v_den_ngay,
                                                                                                        v_chi_nhanh_id)
                ;

                ----------------- Step 4: Cập nhật giá sau khi tính vào table chứng từ kho master và Detail: ----

                PERFORM CAP_NHAT_TINH_GIA_KO_THEO_KHO_CHO_BANG_CHUNG_TU_KHO_MASTER_VA_DETAIL(ds_vat_tu_hang_hoa_id, ';',
                                                                                             v_tu_ngay, v_den_ngay, v_chi_nhanh_id)
                ;


                ---- Step 5: Cập nhật giá của hàng bán trả lại nhập kho theo giá xuất

                PERFORM CAP_NHAT_GIA_CHO_CHUNG_TU_HANG_BAN_TRA_LAI_TU_PHIEU_XK_KO_THEO_KHO_CHON_VTHH(
                    ds_vat_tu_hang_hoa_id, dau_phan_cach, v_chi_nhanh_id, v_tu_ngay, v_den_ngay)
                ;


                DELETE FROM STOCK_EX_LOG_UNPOST_VAT_TU_HANG_HOA
                WHERE "CHI_NHANH_ID" = v_chi_nhanh_id

                      AND "NGAY_HACH_TOAN" >= v_tu_ngay_khong_thoi_gian
                      AND "NGAY_HACH_TOAN" <= ToDateTime_CrrNoTime
                      AND "VAT_TU_HANG_HOA_ID" IN (SELECT cast("MA_VTHH_ID" AS INT)
                                                   FROM TMP_VAT_TU_HANG_HOA_CAP_NHAT_CHON_VTHH_KHONG_THEO_KHO_PP_BINH_QUAN_TUC_THOI)
                ;

                RETURN 0
                ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;
            """)