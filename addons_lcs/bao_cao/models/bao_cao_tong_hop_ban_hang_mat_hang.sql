SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:  nvtoan
-- Create date: 24/11/2014
-- Description: <bán hàng: Lấy số liệu tổng hợp bán hàng theo mặt hàng>
-- nvtoan modify 28/01/2015: Sửa lỗi lấy số lượng và số lượng trả lại của hàng khuyến mại
--nvtoan modify 04/02/2015: Sửa lỗi hóa đơn chỉ có số lượng, không có tiền không lên được (yêu cầu này khá kỳ quặc)
-- vhanh edited lấy thêm thông tin về đơn vị, số lượng bán, số lượng KM, số lượng trả lại, số lượng hàng KM trả lại. Sửa lại tên ĐVC (Main + ColumnName)
-- nmtruong 26/8/2015: Lấy dữ liệu theo khách hàng được chọn
-- nmtruong 22/10/2015: sửa bug 73674: sửa join thành union để lấy lên số giá vốn
-- nmtruong 17/11/2015: Sửa bug 78011: sửa having để lấy lên hàng khuyến mại
-- nmtruong 9/5/2016: CR 101741 thêm cột Số lượng tiêu thụ, đơn giá bán, đơn giá vốn
-- nvtoan modify 24/07/2017: Thực hiện PBI 122151
/*ntlieu 21.11.2017 PBI 119779: Bổ sung thêm cột Doanh thu (chưa bao gồm thuế XK), Thuế xuất khẩu*/
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER  -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @InventoryItemID NVARCHAR(MAX)  -- Danh sách hàng hóa, VD: ",6c9abe42-fbaf-4157-8b2a-10a031cd48dc, 201770d3-8664-4c98-ab0f-fed9af5a89b1,"     
 DECLARE   @ListAccountObjectID NVARCHAR(MAX) 
 DECLARE   @IsWorkingWithManagementBook BIT --  Có dùng sổ quản trị hay không?
 DECLARE   @UnitType INT --Đơn vị tính


		SET			@FromDate = '2018-01-01 00:00:00'
        SET            @ToDate = '2018-12-31 23:59:59'
        SET            @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET            @IncludeDependentBranch = 1
        SET            @InventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,c9386f9b-6cba-4e1a-abb6-f6391d4cc9ad,c5d407f8-0ba9-4d77-8085-d08b7eff1333,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,d304a03c-ec90-4708-9d1a-38318ba45990,e5a7407c-8933-4998-a265-3331f19845c0,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,4bb9f0d8-360e-488b-b1aa-9ff424e8f160,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,13b27260-a6cd-4957-a35f-c553043fdeb7,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
        SET            @ListAccountObjectID = N''
        SET            @IsWorkingWithManagementBook = 0
        SET            @UnitType = 0
					
    BEGIN
        DECLARE @tblListBrandID TABLE -- Bảng chứa danh sách chi nhánh
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(128)
            ) 
       
        INSERT  INTO @tblListBrandID --TMP_LIST_BRAND
                SELECT  FGDBBI.BranchID ,
                        FGDBBI.BranchCode
                FROM    dbo.Func_GetDependentByBranchID(@BranchID, --chi_nhanh_id
                                                        @IncludeDependentBranch)--bao_gom_chi_nhanh_phu_thuoc
                        AS FGDBBI           
                            
        DECLARE @tblListInventoryItemID TABLE -- Bảng chứa danh sách hàng hóa
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemName NVARCHAR(255) ,
              InventoryItemCategoryCode NVARCHAR(MAX) ,
              InventoryItemCategoryName NVARCHAR(MAX) ,
              InventoryItemSource NVARCHAR(255) , --nvtoan add 24/07/2017
              InventoryItemType INT ,
              UnitID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListInventoryItemID --DS_HANG_HOA
                SELECT  II.InventoryItemID ,
                        II.InventoryItemName ,--TEN
                        II.InventoryItemCategoryCode ,--NHOM_VTHH
                        II.InventoryItemCategoryName , 
                        InventoryItemSource , --nvtoan add 24/07/2017 --NGUON_GOC
                        II.InventoryItemType , --TINH_CHAT
                        II.UnitID --DVT_CHINH_ID
                FROM    dbo.Func_ConvertGUIStringIntoTable(@InventoryItemID,
                                                           ',') AS LII
                        INNER JOIN dbo.InventoryItem AS II ON II.InventoryItemID = LII.Value --danh_muc_vat_tu_hang_hoa
        
        -- nmtruong 26/8/2015: Lấy dữ liệu theo khách hàng được chọn
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER
            ) 
       
        INSERT  INTO @tblListAccountObjectID
                SELECT  f.Value
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ListAccountObjectID,
                                                           ',') F                

        DECLARE @tblUnitConvert TABLE
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              UnitID UNIQUEIDENTIFIER ,
              ConvertRate DECIMAL(28, 14)
            )
        INSERT  @tblUnitConvert --TMP_DON_VI_CHUYEN_DOI
                SELECT  IIUC.InventoryItemID , --VAT_TU_HANG_HOA_ID
                        UnitID , --DVT_ID
                        ( CASE WHEN IIUC.ExchangeRateOperator = '/' --PHEP_TINH_CHUYEN_DOI
                               THEN IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                               WHEN IIUC.ConvertRate = 0 THEN 1 --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                               ELSE 1 / IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                          END ) AS ConvertRate
                FROM    dbo.InventoryItemUnitConvert IIUC --danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi
                WHERE   IIUC.SortOrder = @UnitType  --don_vi_tinh
                
        IF @ListAccountObjectID = ''
            OR @ListAccountObjectID = ','
            SET @ListAccountObjectID = NULL

		-- nmtruong 13/5/2016: sửa bug 103241: cột đơn giá bán và đơn giá vốn đang không roud theo định dạng số của đơn giá
        DECLARE @UnitPriceDecimalDigits INT
        SET @UnitPriceDecimalDigits = ( SELECT TOP 1
                                                CAST(OptionValue AS INT)
                                        FROM    dbo.SYSDBOption
                                        WHERE   OptionID = 'UnitPriceDecimalDigits'
                                        ORDER BY IsDefault DESC
                                      )
            
        SELECT  ROW_NUMBER() OVER ( ORDER BY T.InventoryItemCode, T.InventoryItemName ) AS RowNum ,
                T.InventoryItemID , --MA_HANG_ID
                T.InventoryItemCode , -- Mã hàng --MA_HANG
                T.InventoryItemName , -- Tên hàng     --  TEN_HANG                
                T.MainUnitName , --DVT_CHINH_ID
                T.UnitName , --TEN_DVT
                SUM(T.Quantity) AS Quantity , --SO_LUONG_BAN
                SUM(T.MainQuantity) AS MainQuantity , --SO_LUONG_THEO_DVT_CHINH
                SUM(T.PromotionQuantity) AS PromotionQuantity ,--SO_LUONG_KHUYEN_MAI
                SUM(T.MainPromotionQuantity) AS MainPromotionQuantity , --SO_LUONG_KHUYEN_MAI_THEO_DVT_CHINH
                SUM(T.ReturnQuantity) AS ReturnQuantity , --SO_LUONG_TRA_LAI
                SUM(T.MainReturnQuantity) AS MainReturnQuantity , --SO_LUONG_TRA_LAI_THEO_DVT_CHINH
                SUM(T.ReturnPromotionQuantity) AS ReturnPromotionQuantity , --SO_LUONG_KHUYEN_MAI_TRA_LAI
                SUM(T.MainReturnPromotionQuantity) AS MainReturnPromotionQuantity ,
                SUM(T.SaleAmount) AS SaleAmount , --SO_TIEN
                /*ntlieu 21.11.2017 PBI 119779: Bổ sung thêm cột Doanh thu (chưa bao gồm thuế XK), Thuế xuất khẩu*/
                SUM(T.SaleAmount - T.ExportTaxAmount) AS SaleAmountNotExportTax, -- Doanh thu chưa bao gồm thuế xuất khẩu = Doanh số - Thuế xuất khẩu --"SO_TIEN" - T."SO_TIEN_NHAP_KHAU"
                SUM(T.ExportTaxAmount) AS ExportTaxAmount , -- Thuế xuất khẩu --SO_TIEN_NHAP_KHAU
                SUM(T.DiscountAmount) AS DiscountAmount , --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount --SO_TIEN -SO_TIEN_CHIET_KHAU -SO_TIEN_TRA_LAI -SO_TIEN_GIAM_TRU AS DOANH_THU_THUAN
                    - T.ReduceAmount) AS NetSaleAmount ,
                SUM(T.CostAmount) AS CostAmount , --GIA_VON
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount --SO_TIEN -SO_TIEN_CHIET_KHAU -SO_TIEN_TRA_LAI -SO_TIEN_GIAM_TRU -GIA_VON
                    - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount ,
                SUM(T.Quantity + T.PromotionQuantity - T.ReturnQuantity --SO_LUONG +SO_LUONG_KHUYEN_MAI -SO_LUONG_TRA_LAI -SO_LUONG_KHUYEN_MAI_TRA_LAI
                    - T.ReturnPromotionQuantity) AS SaleQuantity , -- số lượng tiêu thụ --LOI_NHUAN_GOP
                CASE WHEN SUM(T.Quantity + T.PromotionQuantity
                              - T.ReturnQuantity - T.ReturnPromotionQuantity) <> 0
                     THEN ROUND(SUM(T.SaleAmount - T.DiscountAmount
                                    - T.ReturnAmount - T.ReduceAmount)
                                / SUM(T.Quantity + T.PromotionQuantity
                                      - T.ReturnQuantity
                                      - T.ReturnPromotionQuantity),
                                @UnitPriceDecimalDigits)
                     ELSE 0.0
                END AS SaleUnitPrice , -- đơn giá bán 
                CASE WHEN SUM(T.Quantity + T.PromotionQuantity
                              - T.ReturnQuantity - T.ReturnPromotionQuantity) <> 0
                     THEN ROUND(SUM(T.CostAmount) / SUM(T.Quantity
                                                        + T.PromotionQuantity
                                                        - T.ReturnQuantity
                                                        - T.ReturnPromotionQuantity),
                                @UnitPriceDecimalDigits)
                     ELSE 0.0
                END AS CostUnitPrice ,
                CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount
                              - T.ReduceAmount) > 0
                          AND SUM(T.SaleAmount - T.DiscountAmount
                                  - T.ReturnAmount - T.ReduceAmount
                                  - T.CostAmount) > 0
                          OR SUM(T.SaleAmount - T.DiscountAmount
                                 - T.ReturnAmount - T.ReduceAmount) < 0
                          AND SUM(T.SaleAmount - T.DiscountAmount
                                  - T.ReturnAmount - T.ReduceAmount
                                  - T.CostAmount) < 0
                     THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount
                              - T.ReduceAmount - T.CostAmount) * 100
                          / SUM(T.SaleAmount - T.DiscountAmount
                                - T.ReturnAmount - T.ReduceAmount)
                     ELSE 0
                END AS GrossProfitRate ,
                T.InventoryItemCategoryName,
                InventoryItemSource  --nvtoan add 24/07/2017
						--[dbo].[Func_GetInventoryCategoryListName](T.InventoryItemCategoryCode) AS InventoryItemCategoryName						
        FROM    ( SELECT    SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN_HANG
                            LII.InventoryItemCategoryCode , 
                            LII.InventoryItemCategoryName ,
                            InventoryItemSource,  --nvtoan add 24/07/2017
                            UI.UnitName AS MainUnitName , --DON_VI_TINH
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END AS UnitName ,
                            SUM(CASE SL.IsPromotion --LA_HANG_KHUYEN_MAI
                                  WHEN 0 THEN SL.MainQuantity --SO_LUONG_THEO_DVT_CHINH
                                  ELSE 0
                                END) AS MainQuantity , -- Số lượng bán theo ĐVC
                            SUM(CASE SL.IsPromotion --LA_HANG_KHUYEN_MAI
                                  WHEN 1 THEN SL.MainQuantity  --SO_LUONG_THEO_DVT_CHINH
                                  ELSE 0
                                END) AS MainPromotionQuantity , -- Số lượng KM  --SO_LUONG_KHUYEN_MAI_THEO_DVT_CHINH
                            SUM(CASE SL.IsPromotion --LA_HANG_KHUYEN_MAI
                                  WHEN 0 THEN SL.ReturnMainQuantity --SL_TRA_LAI_THEO_DVT_CHINH
                                  ELSE 0
                                END) AS MainReturnQuantity , -- Số lượng trả lại theo ĐVT chính    -- SO_LUONG_TRA_LAI_THEO_DVT_CHINH
                            SUM(CASE SL.IsPromotion --LA_HANG_KHUYEN_MAI
                                  WHEN 1 THEN SL.ReturnMainQuantity --SL_TRA_LAI_THEO_DVT_CHINH
                                  ELSE 0
                                END) AS MainReturnPromotionQuantity , -- Số lượng trả lại theo ĐVT chính    --SO_LUONG_KHUYEN_MAI_TRA_LAI
                            SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --SO_TIEN
                            /*ntlieu 21.11.2017 PBI 119779: Bổ sung thêm cột Doanh thu (chưa bao gồm thuế XK), Thuế xuất khẩu*/
                            SUM(SL.ExportTaxAmount) AS ExportTaxAmount , -- Thuế xuất khẩu --SO_TIEN_NHAP_KHAU
                            SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu    --SO_TIEN_CHIET_KHAU
                            SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --SO_TIEN_TRA_LAI
                            SUM(SL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá   --SO_TIEN_GIAM_TRU
                            SUM(CASE WHEN U.UnitID IS NOT NULL
                                          AND SL.UnitID = U.UnitID --"DVT_ID" = U.id
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE   SL.SaleQuantity --SO_LUONG
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.MainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                          END
                                END) AS Quantity , --SO_LUONG
                            SUM(CASE WHEN U.UnitID IS NOT NULL
                                          AND SL.UnitID = U.UnitID --"DVT_ID" = U.id
                                     THEN CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.SaleQuantity --SO_LUONG
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.MainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
                                               ELSE 0
                                          END
                                END) AS PromotionQuantity ,--SO_LUONG_KHUYEN_MAI
                            SUM(CASE WHEN U.UnitID IS NOT NULL --U."id" <> -1
                                          AND SL.UnitID = U.UnitID --DVT_ID
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.ReturnMainQuantity --SL_TRA_LAI_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                          END
                                END) AS ReturnQuantity ,--SO_LUONG_TRA_LAI
                            SUM(CASE WHEN U.UnitID IS NOT NULL --U."id" <> -1
                                          AND SL.UnitID = U.UnitID --DVT_ID
                                     THEN CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.ReturnMainQuantity --SL_TRA_LAI_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                               ELSE 0
                                          END
                                END) AS ReturnPromotionQuantity , --SO_LUONG_KHUYEN_MAI_TRA_LAI
                            0 AS CostAmount
                  FROM      dbo.SaleLedger AS SL
                            INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID
                            INNER JOIN @tblListInventoryItemID AS LII ON SL.InventoryItemID = LII.InventoryItemID
                            LEFT JOIN @tblListAccountObjectID AO ON SL.AccountObjectID = AO.AccountObjectID
                            LEFT JOIN dbo.Unit UI ON LII.UnitID = UI.UnitID
                            LEFT JOIN @tblUnitConvert UC ON LII.InventoryItemID = UC.InventoryItemID
                            LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL
                                                      AND U.UnitID = LII.UnitID
                                                    )
                                                    OR ( UC.InventoryItemID IS NOT NULL
                                                         AND UC.UnitID = U.UnitID
                                                       )
                  WHERE     ( @UnitType IS NULL --don_vi_tinh  = -1
                              OR @UnitType = 0 --don_vi_tinh
                              OR UC.InventoryItemID IS NOT NULL --"VAT_TU_HANG_HOA_ID" <> -1
                            )
                            AND SL.PostedDate BETWEEN @FromDate AND @ToDate
                            AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND ( @ListAccountObjectID IS NULL
                                  OR AO.AccountObjectID IS NOT NULL
                                )
                  GROUP BY  SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN
                            LII.InventoryItemName , -- Tên hàng
                            LII.InventoryItemCategoryCode ,
                            LII.InventoryItemCategoryName ,
                            InventoryItemSource ,
                            UI.UnitName , --DON_VI_TINH
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END
                  UNION ALL
                  SELECT    IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN
                            LII.InventoryItemCategoryCode ,
                            LII.InventoryItemCategoryName ,
                            InventoryItemSource, --nvtoan add 24/02/2017
                            UI.UnitName AS MainUnitName , --DON_VI_TINH
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END AS UnitName , --DON_VI_TINH
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
                            0 ,
                            SUM(OutwardAmount - InwardAmount) AS CostAmount
                  FROM      dbo.InventoryLedger IL --so_kho_chi_tiet
                            INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN @tblListInventoryItemID AS LII ON iL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON IL."MA_HANG_ID" = LII.id
                            LEFT JOIN @tblListAccountObjectID AO ON IL.AccountObjectID = AO.AccountObjectID
                            LEFT JOIN dbo.Unit UI ON LII.UnitID = UI.UnitID --danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI.id
                            LEFT JOIN @tblUnitConvert UC ON LII.InventoryItemID = UC.InventoryItemID --TMP_DON_VI_CHUYEN_DOI AS UC ON LII.id = UC."VAT_TU_HANG_HOA_ID"
                            LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL  -- UC."VAT_TU_HANG_HOA_ID" = -1
                                                      AND U.UnitID = LII.UnitID --U.id = LII."DVT_CHINH_ID"
                                                    )
                                                    OR ( UC.InventoryItemID IS NOT NULL --UC."VAT_TU_HANG_HOA_ID" <> -1
                                                         AND UC.UnitID = U.UnitID --UC."DVT_ID" = U.id
                                                       )
                  WHERE     IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy     --MA_TK_CO
                            AND ( IL.RefType = 2020--LOAI_CHUNG_TU
                                  OR IL.RefType = 2013 --LOAI_CHUNG_TU
                                ) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi
                            AND ( @UnitType IS NULL --don_vi_tinh
                                  OR @UnitType = 0 --don_vi_tinh
                                  OR UC.InventoryItemID IS NOT NULL --VAT_TU_HANG_HOA_ID
                                )
                            AND ( @ListAccountObjectID IS NULL
                                  OR AO.AccountObjectID IS NOT NULL
                                )
                  GROUP BY  IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN
                            LII.InventoryItemCategoryCode ,
                            LII.InventoryItemCategoryName ,
                            InventoryItemSource, --nvtoan add 24/02/2017
                            UI.UnitName , --DON_VI_TINH
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName
                            END
                ) T
				WHERE T.InventoryItemCode ='AO_SM_NAM'
        GROUP BY T.InventoryItemID , --MA_HANG_ID
                T.InventoryItemCode , -- Mã hàng --MA_HANG
                T.InventoryItemName , -- Tên hàng  --TEN                      
                T.MainUnitName , --DVT_CHINH_ID
                T.UnitName , --TEN_DVT
                T.InventoryItemCategoryName,
                InventoryItemSource --nvtoan add 24/02/2017
                        --[dbo].[Func_GetInventoryCategoryListName](T.InventoryItemCategoryCode)
        HAVING  SUM(T.Quantity) <> 0 --SO_LUONG
                OR SUM(T.PromotionQuantity) <> 0 --SO_LUONG_KHUYEN_MAI
                OR SUM(T.ReturnQuantity) <> 0 --SO_LUONG_TRA_LAI
                OR SUM(T.ReturnPromotionQuantity) <> 0 --SO_LUONG_KHUYEN_MAI_TRA_LAI
                OR SUM(T.SaleAmount) <> 0 --DOANH_SO_BAN
                OR SUM(T.DiscountAmount) <> 0 --SO_TIEN_CHIET_KHAU
                OR SUM(T.ReturnAmount) <> 0 --GIA_TRI_TRA_LAI
                OR SUM(T.ReduceAmount) <> 0 --GIA_TRI_GIAM_GIA
                OR SUM(T.CostAmount) <> 0
		
        OPTION  ( RECOMPILE )						
    END

GO