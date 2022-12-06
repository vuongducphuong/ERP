SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:  nvtoan
-- Create date: 25/11/2014
-- Description: <bán hàng: Lấy số liệu tổng hợp bán hàng theo mặt hàng và khách hàng>
-- nvtoan modify 28/01/2015: Sửa lỗi lấy số lượng và số lượng trả lại của hàng khuyến mại
--nvtoan modify 04/02/2015: Sửa lỗi hóa đơn chỉ có số lượng, không có tiền không lên được (yêu cầu này khá kỳ quặc)
-- hhson modified 03/04/2015: Bổ sung lấy Mã nhóm VTHH, Tên nhóm VTHH - PBI 50464
-- vhanh edited lấy thêm thông tin về ĐVT, số lượng bán, số lượng KM, số lượng trả lại, số lượng hàng KM trả lại. Sửa lại tên ĐVC (Main + ColumnName)
-- nmtruong 22/10/2015: sửa bug 73674: sửa join thành union để lấy lên số giá vốn
-- nmtruong 17/11/2015: Sửa bug 78011: sửa having để lấy lên hàng khuyến mại
-- BTAnh - 12.8.2016: Bổ sung OPTION(RECOMPILE) 
-- nvtoan modify 24/07/2017: Thực hiện PBI 122151
-- Edit by nhyen - 7/7/2018(CR 237996): Lấy thêm thông tin số điện thoại và địa chỉ của khách hàng
-- =============================================

--'01/01/2014','12/31/2014','aff3b6b0-fd0d-49d8-add8-4f5abb45955b',1,',7f75fb4d-2f68-43fe-813e-94f15007d0e7,',',3d5736b2-a9cc-4d77-8c8b-5d184eab41f9,5e4faf7e-9a72-4b36-95ef-380eac9f1f34,',1
	DECLARE				@FromDate DATETIME 
	DECLARE				@ToDate DATETIME
	DECLARE				@BranchID UNIQUEIDENTIFIER  -- Chi nhánh
	DECLARE				@IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
	DECLARE				@InventoryItemID NVARCHAR(MAX)  -- Danh sách hàng hóa, VD: ",6c9abe42-fbaf-4157-8b2a-10a031cd48dc, 201770d3-8664-4c98-ab0f-fed9af5a89b1,"     
	DECLARE				@AccountObjectID NVARCHAR(MAX)  -- Danh sách khách hàng
	DECLARE				@IsWorkingWithManagementBook BIT --  Có dùng sổ quản trị hay không?
	DECLARE				@UnitType INT --Đơn vị tính

		SET											@FromDate = '2018-01-01 00:00:00'
        SET                                            @ToDate = '2018-12-31 23:59:59'
        SET                                            @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET                                            @IncludeDependentBranch = 1
        SET                                            @InventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,c9386f9b-6cba-4e1a-abb6-f6391d4cc9ad,c5d407f8-0ba9-4d77-8085-d08b7eff1333,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,d304a03c-ec90-4708-9d1a-38318ba45990,e5a7407c-8933-4998-a265-3331f19845c0,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,4bb9f0d8-360e-488b-b1aa-9ff424e8f160,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,13b27260-a6cd-4957-a35f-c553043fdeb7,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
        SET                                            @AccountObjectID = N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,8b0ba43a-1120-4574-905d-e2abff045f13,'
        SET                                            @IsWorkingWithManagementBook = 0
        SET                                            @UnitType = 0

    BEGIN
	DROP  TABLE #tblListBrandID
        CREATE TABLE #tblListBrandID
			(
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(128)
            ) 
        INSERT  INTO #tblListBrandID
                SELECT  FGDBBI.BranchID ,
                        FGDBBI.BranchCode
                FROM    dbo.Func_GetDependentByBranchID(@BranchID, @IncludeDependentBranch) AS FGDBBI           
         
        -- nmtruong 22/10/2015 sửa lại bảng tạm lấy lên InventoryItemCategoryName đỡ phải join khi lấy số liệu 
		DROP  TABLE #tblListInventoryItemID                  
        CREATE TABLE #tblListInventoryItemID  -- Bảng chứa danh sách hàng hóa
            (
              InventoryItemID UNIQUEIDENTIFIER PRIMARY KEY ,
              InventoryItemName NVARCHAR(255) ,
              MainUnitName NVARCHAR(20),
              UnitName NVARCHAR(20),
              InventoryItemCategoryCode NVARCHAR(MAX) ,
              InventoryItemCategoryName NVARCHAR(MAX) ,
              InventoryItemSource NVARCHAR(255) , --nvtoan add 24/07/2017
              InventoryItemType INT ,
              UnitID UNIQUEIDENTIFIER,
              UnitConvertID UNIQUEIDENTIFIER,
              ConvertRate DECIMAL(28, 14)
            ) 
          --nvtoan modify 22/11/2014: Sửa lỗi khi truyền nothing vào
        IF ISNULL(@InventoryItemID, '') <> '' --SAN_PHAMIDS IS NULL
            INSERT  INTO #tblListInventoryItemID --DS_HANG_HOA
                    SELECT  II.InventoryItemID , --MA_HANG_ID
							II.InventoryItemName , --TEN
                            ISNULL(UI.UnitName, '') AS MainUnitName, --DON_VI_TINH_CHINH
                            CASE WHEN II.UnitID IS NULL THEN ''
                                 ELSE U.UnitName
                            END AS UnitName ,--DON_VI_TINH
                            II.InventoryItemCategoryCode ,
                            II.InventoryItemCategoryName ,
                            InventoryItemSource , --nvtoan add 24/07/2017 --TINH_CHAT
                            II.InventoryItemType ,
                            II.UnitID, --DVT_CHINH_ID
                            U.UnitID AS UnitConvertID, -- U."id" AS "DON_VI_CHUYEN_DOI",
                            ( CASE WHEN IIUC.InventoryItemID IS NULL THEN 1 --IIUC."VAT_TU_HANG_HOA_ID" =-1
									WHEN IIUC.ExchangeRateOperator = '/' THEN IIUC.ConvertRate --PHEP_TINH_CHUYEN_DOI --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
									WHEN IIUC.ConvertRate = 0 THEN 1 --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
									ELSE 1 / IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
								END ) AS ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                    FROM    dbo.Func_ConvertGUIStringIntoTable(@InventoryItemID,',') AS LII
                            INNER JOIN dbo.InventoryItem AS II ON II.InventoryItemID = LII.Value --danh_muc_vat_tu_hang_hoa
                            LEFT JOIN dbo.InventoryItemUnitConvert IIUC ON IIUC.InventoryItemID = LII.Value --danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi
																			AND IIUC.SortOrder = @UnitType --STT = loai_don_vi_tinh
                            LEFT JOIN dbo.Unit UI ON II.UnitID = UI.UnitID --danh_muc_don_vi_tinh -- 
                            LEFT JOIN dbo.Unit U ON (IIUC.InventoryItemID IS NULL AND U.UnitID = II.UnitID) --(IIUC."VAT_TU_HANG_HOA_ID" = -1 AND U."id" = II."DVT_CHINH_ID")
                                                    OR (IIUC.InventoryItemID IS NOT NULL AND IIUC.UnitID = U.UnitID) --(IIUC."VAT_TU_HANG_HOA_ID" <> -1 AND IIUC."DVT_ID" = U."id")
					WHERE  ( @UnitType IS NULL OR @UnitType = 0 OR IIUC.InventoryItemID IS NOT NULL) --( loai_don_vi_tinh IS NULL OR loai_don_vi_tinh = 0 OR IIUC."VAT_TU_HANG_HOA_ID" <> -1)
                           
        ELSE
            INSERT  INTO #tblListInventoryItemID --DS_HANG_HOA
                    SELECT  II.InventoryItemID , --II."id"  as "MA_HANG_ID",
							II.InventoryItemName , --TEN
                            ISNULL(UI.UnitName, '') AS MainUnitName, --DON_VI_TINH_CHINH
                            CASE WHEN II.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END AS UnitName , --DON_VI_TINH
                            II.InventoryItemCategoryCode ,
                            II.InventoryItemCategoryName ,
                            InventoryItemSource , --nvtoan add 24/07/2017 --NGUON_GOC
                            II.InventoryItemType , --TINH_CHAT
                            II.UnitID, --DVT_CHINH_ID
                            U.UnitID AS UnitConvertID, --DON_VI_CHUYEN_DOI
                            ( CASE WHEN IIUC.InventoryItemID IS NULL THEN 1 --VAT_TU_HANG_HOA_ID
									WHEN IIUC.ExchangeRateOperator = '/' THEN IIUC.ConvertRate --IIUC."PHEP_TINH_CHUYEN_DOI" = '/' THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
									WHEN IIUC.ConvertRate = 0 THEN 1 --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
									ELSE 1 / IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
								END ) AS ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                    FROM    dbo.InventoryItem II --danh_muc_vat_tu_hang_hoa
							LEFT JOIN dbo.InventoryItemUnitConvert IIUC ON IIUC.InventoryItemID = II.InventoryItemID --danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC ON IIUC."VAT_TU_HANG_HOA_ID" = II."id"
																			AND IIUC.SortOrder = @UnitType --IIUC."STT" = loai_don_vi_tinh
                            LEFT JOIN dbo.Unit UI ON II.UnitID = UI.UnitID --danh_muc_don_vi_tinh UI ON II."DVT_CHINH_ID" = UI."id"
                            LEFT JOIN dbo.Unit U ON (IIUC.InventoryItemID IS NULL AND U.UnitID = II.UnitID) --(IIUC."VAT_TU_HANG_HOA_ID" = -1 AND U."id" = II."DVT_CHINH_ID")
                                                    OR (IIUC.InventoryItemID IS NOT NULL AND IIUC.UnitID = U.UnitID) --(IIUC."VAT_TU_HANG_HOA_ID" <> -1 AND IIUC."DVT_ID" = U."id")
                    WHERE  ( @UnitType IS NULL OR @UnitType = 0 OR IIUC.InventoryItemID IS NOT NULL)
                    
       
        -- nmtruong 22/10/2015 sửa lại bảng tạm lấy lên 1 số thông tin để đỡ phải join khi lấy số liệu
		DROP TABLE #tblListAccountObjectID 
        CREATE TABLE #tblListAccountObjectID -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER PRIMARY KEY ,
              AccountObjectCode NVARCHAR(25) ,
              AccountObjectName NVARCHAR(128) ,
              AccountObjectAddress NVARCHAR(255) ,	-- nhyen - 7/7/2018(CR 237996):địa chỉ của Khách hàng
              AccountObjectMobile NVARCHAR(50) ,	-- nhyen - 7/7/2018(CR 237996):số điện thoại của Khách hàng
              AccountObjectGroupListCode NVARCHAR(MAX) ,
              AccountObjectCategoryName NVARCHAR(MAX) ,
              ProvinceOrCity NVARCHAR(100) ,
              District NVARCHAR(100) ,
              WardOrCommune NVARCHAR(100)
            ) 
        INSERT  INTO #tblListAccountObjectID --DS_KHACH_HANG
                SELECT  AO.AccountObjectID , --id
                        AO.AccountObjectCode , --MA_DOI_TUONG
                        AO.AccountObjectName , --HO_VA_TEN
                        AO.Address,		-- nhyen - 7/7/2018(CR 237996):địa chỉ của Khách hàng --DIA_CHI
                        CASE WHEN AO.AccountObjectType = 0 THEN AO.Tel --AO."LOAI_KHACH_HANG" = 0 THEN AO."DIEN_THOAI"
							ELSE AO.Mobile --DT_DI_DONG
						END,	-- nhyen - 7/7/2018(CR 237996):số điện thoại của Khách hàng
                        AO.AccountObjectGroupListCode ,
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName ,
                        AO.ProvinceOrCity , --TINH_TP_ID
                        AO.District , --QUAN_HUYEN_ID
                        AO.WardOrCommune --XA_PHUONG_ID
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,',') F
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = F.Value --res_partner
        OPTION  ( RECOMPILE )
        
        SELECT  ROW_NUMBER() OVER ( ORDER BY T.InventoryItemCode, LII.InventoryItemName, LAO.AccountObjectCode ) AS RowNum ,
                T.InventoryItemID , --MA_HANG_ID
                T.InventoryItemCode , -- Mã hàng --MA_HANG
                LII.InventoryItemName , -- Tên hàng --TEN
                T.MainUnitName , --DON_VI_TINH_CHINH
                LII.InventoryItemCategoryCode ,
                LII.InventoryItemCategoryName , -- Mã nhóm VTHH 
                InventoryItemSource , --nvtoan add 24/07/2017
                T.UnitName , --DON_VI_TINH
                T.AccountObjectID , --MA_DOI_TUONG_ID
                LAO.AccountObjectCode ,		-- nhyen - 7/7/2018(CR 237996):địa chỉ của Khách hàng --MA_DOI_TUONG 
                LAO.AccountObjectName ,		-- nhyen - 7/7/2018(CR 237996):số điện thoại của Khách hàng --HO_VA_TEN
                LAO.AccountObjectAddress ,	-- địa chỉ của nhân viên
				LAO.AccountObjectMobile ,	-- số điện thoại của nhân viên
                LAO.ProvinceOrCity ,
                LAO.District ,
                LAO.WardOrCommune ,
                LAO.AccountObjectGroupListCode ,
                LAO.AccountObjectCategoryName ,
                SUM(T.Quantity) AS Quantity , --SO_LUONG_BAN
                SUM(T.MainQuantity) AS MainQuantity , --SO_LUONG_THEO_DVT_CHINH
                SUM(T.PromotionQuantity) AS PromotionQuantity , --SO_LUONG_KHUYEN_MAI
                SUM(T.MainPromotionQuantity) AS MainPromotionQuantity , --SO_LUONG_KHUYEN_MAI_THEO_DVT_CHINH
                SUM(T.ReturnQuantity) AS ReturnQuantity , --SO_LUONG_TRA_LAI
                SUM(T.MainReturnQuantity) AS MainReturnQuantity , --SO_LUONG_TRA_LAI_THEO_DVT_CHINH
                SUM(T.ReturnPromotionQuantity) AS ReturnPromotionQuantity , --SO_LUONG_KHUYEN_MAI_TRA_LAI
                SUM(T.MainReturnPromotionQuantity) AS MainReturnPromotionQuantity ,
                SUM(T.SaleAmount) AS SaleAmount , --DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount , --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , --SO_TIEN_CHI_PHI
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount ,
                CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) > 0
                          AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) > 0
                          OR SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) < 0
                          AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) < 0
                     THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) * 100
                          / SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount)
                     ELSE 0
                END AS GrossProfitRate
        FROM    ( SELECT    SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , -- Mã hàng  --MA_HANG              
                            LII.MainUnitName , --DON_VI_TINH_CHINH
                            LII.UnitName , --DON_VI_TINH
                            SL.AccountObjectID , --DOI_TUONG_ID
                            SUM(CASE WHEN SL.IsPromotion = 0 THEN SL.MainQuantity
                                  ELSE 0
                                END) AS MainQuantity , -- Số lượng bán theo ĐVC
                            SUM(CASE WHEN SL.IsPromotion = 1 THEN SL.MainQuantity
                                  ELSE 0
                                END) AS MainPromotionQuantity , -- Số lượng KM theo ĐVC
                            SUM(CASE WHEN SL.IsPromotion = 0 THEN SL.ReturnMainQuantity
                                  ELSE 0
                                END) AS MainReturnQuantity , -- Số lượng trả lại theo ĐVT chính    
                            SUM(CASE WHEN SL.IsPromotion = 1 THEN SL.ReturnMainQuantity
                                  ELSE 0
                                END) AS MainReturnPromotionQuantity , -- Số lượng hàng KM trả lại theo ĐVT chính    
                            SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán--DOANH_SO_BAN
                            SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu  --SO_TIEN_CHIET_KHAU
                            SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                            SUM(SL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá --GIA_TRI_GIAM_GIA
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL AND SL.UnitID = LII.UnitConvertID --LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.SaleQuantity --SO_LUONG
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.MainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(LII.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                          END
                                END) AS Quantity , --SO_LUONG_BAN --SO_LUONG_BAN
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL
                                          AND SL.UnitID = LII.UnitConvertID
                                     THEN CASE WHEN SL.IsPromotion = 1
                                               THEN SL.SaleQuantity
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1
                                               THEN SL.MainQuantity
                                                    * ISNULL(LII.ConvertRate, 1)
                                               ELSE 0
                                          END
                                END) AS PromotionQuantity ,
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL --LII."DON_VI_CHUYEN_DOI" <> -1
                                          AND SL.UnitID = LII.UnitConvertID --LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.ReturnMainQuantity--SL_TRA_LAI_THEO_DVT_CHINH
                                                    * ISNULL(LII.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                          END
                                END) AS ReturnQuantity , --SO_LUONG_TRA_LAI
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL --II."DON_VI_CHUYEN_DOI" <> -1
                                          AND SL.UnitID = LII.UnitConvertID --SL."DVT_ID" =LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.ReturnMainQuantity --SL_TRA_LAI_THEO_DVT_CHINH
                                                    * ISNULL(LII.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                               ELSE 0
                                          END
                                END) AS ReturnPromotionQuantity , --SO_LUONG_KHUYEN_MAI_TRA_LAI
                            0 AS CostAmount --SO_TIEN_CHI_PHI
                  FROM      dbo.SaleLedger AS SL --so_ban_hang_chi_tiet --
                            INNER JOIN #tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN #tblListInventoryItemID AS LII ON SL.InventoryItemID = LII.InventoryItemID-- DS_HANG_HOA  AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                            INNER JOIN #tblListAccountObjectID AS AO ON SL.AccountObjectID = ao.AccountObjectID --DS_KHACH_HANG AS AO ON SL."DOI_TUONG_ID" = AO.id
                            
                  WHERE     SL.PostedDate BETWEEN @FromDate AND @ToDate -- SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            
                  GROUP BY  SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , -- Mã hàng -- MA_HANG            
                            LII.MainUnitName , --DON_VI_TINH_CHINH
                            LII.UnitName , --DON_VI_TINH
                            SL.AccountObjectID --DOI_TUONG_ID
                  UNION ALL
                  SELECT    IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng --   MA_HANG         
                            LII.MainUnitName , --DON_VI_TINH_CHINH
                            LII.UnitName , --DON_VI_TINH
                            IL.AccountObjectID , 
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            SUM(OutwardAmount - InwardAmount) AS CostAmount
                  FROM      dbo.InventoryLedger IL --so_kho_chi_tiet
                            INNER JOIN #tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN #tblListInventoryItemID AS LII ON iL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON IL."MA_HANG_ID" = LII."MA_HANG_ID"
                            INNER JOIN #tblListAccountObjectID AS AO ON iL.AccountObjectID = ao.AccountObjectID --DS_KHACH_HANG AS AO ON SL."DOI_TUONG_ID" = AO.id
                            
                  WHERE     IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy     --IL."MA_TK_CO" LIKE '632%%'                       
                            AND ( IL.RefType = 2020 OR IL.RefType = 2013) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi --LOAI_CHUNG_TU
                  GROUP BY  IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng  --  MA_HANG             
                            LII.MainUnitName ,--DON_VI_TINH_CHINH
                            LII.UnitName , --DON_VI_TINH
                            IL.AccountObjectID --DOI_TUONG_ID
                ) T
                INNER JOIN #tblListInventoryItemID LII ON T.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON T."MA_HANG_ID" = LII."MA_HANG_ID"
                INNER JOIN #tblListAccountObjectID LAO ON T.AccountObjectID = LAO.AccountObjectID --T."DOI_TUONG_ID" = LAO.id
        GROUP BY T.InventoryItemID , --MA_HANG_ID
                T.InventoryItemCode , -- Mã hàng --MA_HANG
                LII.InventoryItemName , -- Tên hàng --TEN
                T.MainUnitName , --DON_VI_TINH_CHINH
                LII.InventoryItemCategoryCode ,
                LII.InventoryItemCategoryName , -- Mã nhóm VTHH 
                InventoryItemSource , --nvtoan add 24/07/2017
                T.UnitName , --DON_VI_TINH
                T.AccountObjectID , --DOI_TUONG_ID
                LAO.AccountObjectCode , --MA_DOI_TUONG
                LAO.AccountObjectName , --HO_VA_TEN
                LAO.AccountObjectAddress , --DIA_CHI
				LAO.AccountObjectMobile ,
                LAO.ProvinceOrCity ,
                LAO.District ,
                LAO.WardOrCommune ,
                LAO.AccountObjectGroupListCode ,
                LAO.AccountObjectCategoryName
        HAVING  SUM(T.Quantity) <> 0 --SO_LUONG_BAN
                OR SUM(T.PromotionQuantity) <> 0 --SO_LUONG_KHUYEN_MAI
                OR SUM(T.ReturnQuantity) <> 0 --SO_LUONG_TRA_LAI
                OR SUM(T.ReturnPromotionQuantity) <> 0 --SO_LUONG_KHUYEN_MAI_TRA_LAI
                OR SUM(T.SaleAmount) <> 0 --DOANH_SO_BAN
                OR SUM(T.DiscountAmount) <> 0 --SO_TIEN_CHIET_KHAU
                OR SUM(T.ReturnAmount) <> 0 --GIA_TRI_TRA_LAI
                OR SUM(T.ReduceAmount) <> 0 --GIA_TRI_GIAM_GIA
                OR SUM(T.CostAmount) <> 0 --SO_TIEN_CHI_PHI
        OPTION  ( RECOMPILE )
        
    END

GO