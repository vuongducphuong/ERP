SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		ntquang
-- Create date: 27/07/2018
-- Description:	Lấy số liệu cho báo cáo "Tổng hợp bán hàng theo nhân viên,khách hàng và mặt hàng"
-- =============================================

				DECLARE				@FromDate DATETIME 
				DECLARE				@ToDate DATETIME 
				DECLARE				@BranchID UNIQUEIDENTIFIER  -- Chi nhánh
				DECLARE				@IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
				DECLARE				@AccountObjectID NVARCHAR(MAX)  -- Danh sách khách hàng
				DECLARE				@EmployeeID NVARCHAR(MAX)  --Danh sách nhân viên
				DECLARE				@IsWorkingWithManagementBook BIT --  Có dùng sổ quản trị hay không?
				DECLARE				@UnitType INT --Đơn vị tính

												SET				@FromDate = '2018-01-01 00:00:00'
                                                SET                   @ToDate = '2018-12-31 23:59:59'
                                                SET                   @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
                                                SET                   @IncludeDependentBranch = 1
                                                SET                   @AccountObjectID = N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,8b0ba43a-1120-4574-905d-e2abff045f13,'
                                                SET                   @EmployeeID = N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,'
                                                SET                   @IsWorkingWithManagementBook = 0
                                                SET                   @UnitType = 0

    BEGIN
    -- chi nhánh
        CREATE TABLE #tblListBrandID --TMP_LIST_BRAND
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS
            ) 
        INSERT  INTO #tblListBrandID
                SELECT  FGDBBI.BranchID ,
                        FGDBBI.BranchCode
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI 
  
  
  -----------------------------------------		
        CREATE TABLE #tbCustomerID  -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(25)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,
              AccountObjectName NVARCHAR(255)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,
              AccountObjectAddress NVARCHAR(255)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,
              AccountObjectMobile NVARCHAR(50)
                COLLATE SQL_Latin1_General_CP1_CI_AS -- tổ chức thì lấy cố định, cá nhân thì lấy di động
            ) 
        INSERT  INTO #tbCustomerID --DS_KHACH_HANG
                SELECT  Value ,
                        AccountObjectCode , --MA_KHACH_HANG
                        AccountObjectName , --TEN_KHACH_HANG
                        [Address] , --DIA_CHI
                        CASE WHEN AccountObjectType = 0 THEN Tel --CU."LOAI_KHACH_HANG" = 0 THEN CU."DIEN_THOAI"
                             ELSE Mobile --DT_DI_DONG
                        END
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') AS F
                        INNER JOIN dbo.AccountObject AOD ON AOD.AccountObjectID = F.Value
					
-----------------------------------------  
-----------------------------------------	                                               
        CREATE TABLE #tblListInventoryItemID -- Bảng chứa danh sách hàng hóa
            (
              InventoryItemID UNIQUEIDENTIFIER PRIMARY KEY ,
              InventoryItemName NVARCHAR(255)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,
              MainUnitName NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              UnitName NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              InventoryItemCategoryName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,
              InventoryItemSource NVARCHAR(255)
                COLLATE SQL_Latin1_General_CP1_CI_AS , --nvtoan add 24/07/2017
              InventoryItemType INT ,
              UnitID UNIQUEIDENTIFIER ,
              UnitConvertID UNIQUEIDENTIFIER ,
              ConvertRate DECIMAL(28, 14)
            )
            
        INSERT  INTO #tblListInventoryItemID --DS_HANG_HOA
                SELECT  II.InventoryItemID , --MA_HANG_ID
                        II.InventoryItemName , --TEN_HANG
                        ISNULL(UI.UnitName, '') AS MainUnitName , --COALESCE(UI."DON_VI_TINH", '') AS "DON_VI_TINH_CHINH"
                        CASE WHEN II.UnitID IS NULL THEN ''  --II."DVT_CHINH_ID" = -1
                             ELSE U.UnitName --DON_VI_TINH
                        END AS UnitName , --DON_VI_TINH
                        II.InventoryItemCategoryName , 
                        InventoryItemSource , --NGUON_GOC
                        II.InventoryItemType ,--TINH_CHAT
                        II.UnitID ,--DVT_CHINH_ID
                        U.UnitID AS UnitConvertID , --DON_VI_CHUYEN_DOI
                        ( CASE WHEN IIUC.InventoryItemID IS NULL THEN 1 --VAT_TU_HANG_HOA_ID
                               WHEN IIUC.ExchangeRateOperator = '/' --PHEP_TINH_CHUYEN_DOI
                               THEN IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                               WHEN IIUC.ConvertRate = 0 THEN 1 --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                               ELSE 1 / IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                          END ) AS ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                FROM    dbo.InventoryItem AS II --danh_muc_vat_tu_hang_hoa
                        LEFT JOIN dbo.InventoryItemUnitConvert IIUC ON IIUC.InventoryItemID = II.InventoryItemID --IIUC."VAT_TU_HANG_HOA_ID" = II."id"
                                                              AND IIUC.SortOrder = @UnitType --IIUC."STT" = don_vi_tinh
                        LEFT JOIN dbo.Unit UI ON II.UnitID = UI.UnitID --danh_muc_don_vi_tinh UI ON II."DVT_CHINH_ID" = UI."id"
                        LEFT JOIN dbo.Unit U ON ( IIUC.InventoryItemID IS NULL --danh_muc_don_vi_tinh U ON (IIUC."VAT_TU_HANG_HOA_ID" = -1
                                                  AND U.UnitID = II.UnitID--U."id" = II."DVT_CHINH_ID"
                                                )
                                                OR ( IIUC.InventoryItemID IS NOT NULL --IIUC."VAT_TU_HANG_HOA_ID" <> -1 
                                                     AND IIUC.UnitID = U.UnitID --IIUC."DVT_ID" = U."id"
                                                   )
                WHERE   ( @UnitType IS NULL --don_vi_tinh
                          OR @UnitType = 0 --don_vi_tinh
                          OR IIUC.InventoryItemID IS NOT NULL --IIUC."VAT_TU_HANG_HOA_ID" <> -1
                        )
  -----------------------------------------	
  
    -----------------------------------------	
        CREATE TABLE #tbEmployeeID   --Bảng chứa danh sách nhân viên được chọn
            (
              EmployeeID UNIQUEIDENTIFIER ,
              EmployeeCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              EmployeeName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              EmployeeAddress NVARCHAR(255)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,	-- địa chỉ của nhân viên
              EmployeeMobile NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS ,	-- số điện thoại của nhân viên
              OrganizationUnitID UNIQUEIDENTIFIER ,
              OrganizationUnitCode NVARCHAR(25)
                COLLATE SQL_Latin1_General_CP1_CI_AS ,
              OrganizationUnitName NVARCHAR(255)
                COLLATE SQL_Latin1_General_CP1_CI_AS
            ) 
        INSERT  INTO #tbEmployeeID --DS_NHAN_VIEN
                SELECT  F.Value ,
                        AO.AccountObjectCode ,--MA_NHAN_VIEN
                        AO.AccountObjectName , --TEN_NHAN_VIEN
                        AO.Address , --DIA_CHI_LIEN_HE
                        AO.Mobile , --DT_DI_DONG_LIEN_HE
                        Ou.OrganizationUnitID , --DON_VI_ID
                        OU.OrganizationUnitCode , --MA_DON_VI
                        OU.OrganizationUnitName --TEN_DON_VI
                FROM    dbo.Func_ConvertGUIStringIntoTable(@EmployeeID, ',') F
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = F.Value
                        LEFT JOIN dbo.OrganizationUnit OU ON AO.OrganizationUnitID = OU.OrganizationUnitID --danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"

   -----------------------------------------	
     -----------------------------------------	
     --Lấy dữ liệu                          
        OPTION  ( RECOMPILE )
        SELECT  ROW_NUMBER() OVER ( ORDER BY AO.EmployeeCode, CU.AccountObjectCode , T.InventoryItemCode ) AS RowNum ,--ROW_NUMBER() OVER ( ORDER BY AO."MA_NHAN_VIEN", CU."MA_KHACH_HANG" , T."MA_HANG" ) AS RowNum ,
                T.InventoryItemID , --MA_HANG_ID
                T.InventoryItemCode , -- Mã hàng --MA_HANG
                LII.InventoryItemName , -- Tên hàng --TEN_HANG
                T.MainUnitName , --DON_VI_TINH_CHINH
                T.UnitName , --TEN_DVT
                T.EmployeeID , --NHAN_VIEN_ID
                AO.EmployeeCode , --MA_NHAN_VIEN
                AO.EmployeeName , --TEN_NHAN_VIEN
                AO.EmployeeAddress ,	-- địa chỉ của nhân viên
                AO.EmployeeMobile ,	-- số điện thoại của nhân viên
                LII.InventoryItemCategoryName , -- tên nhóm VTHH       
                InventoryItemSource , --nvtoan add 24/07/2017
                AO.OrganizationUnitID ,
                AO.OrganizationUnitCode ,
                AO.OrganizationUnitName ,
                CU.AccountObjectID ,--KHACH_HANG_ID
                CU.AccountObjectCode , --MA_KHACH_HANG
                CU.AccountObjectName , --TEN_KHACH_HANG
                CU.AccountObjectAddress ,		-- Địa chỉ
                CU.AccountObjectMobile ,
                SUM(T.Quantity) AS Quantity , --SO_LUONG_BAN
                SUM(T.MainQuantity) AS MainQuantity , --
                SUM(T.PromotionQuantity) AS PromotionQuantity , --SO_LUONG_KHUYEN_MAI
                SUM(T.MainPromotionQuantity) AS MainPromotionQuantity ,
                SUM(T.ReturnQuantity) AS ReturnQuantity , --SO_LUONG_TRA_LAI
                SUM(T.MainReturnQuantity) AS MainReturnQuantity ,
                SUM(T.ReturnPromotionQuantity) AS ReturnPromotionQuantity ,--SO_LUONG_KHUYEN_MAI_TRA_LAI 
                SUM(T.MainReturnPromotionQuantity) AS MainReturnPromotionQuantity ,
                SUM(T.SaleAmount) AS SaleAmount , --DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount
                    - T.ReduceAmount) AS NetSaleAmount , --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , --GIA_VON
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount
                    - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount ,
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
                END AS GrossProfitRate
        FROM    ( SELECT    CU.AccountObjectID , --KHACH_HANG_ID
                            SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , --MA_HANG
                            LII.MainUnitName ,--DON_VI_TINH_CHINH
                            LII.UnitName , --TEN_DVT
                            SL.EmployeeID ,--NHAN_VIEN_ID 
                            SUM(CASE WHEN SL.IsPromotion = 0 --LA_HANG_KHUYEN_MAI
                                     THEN SL.MainQuantity
                                     ELSE 0
                                END) AS MainQuantity , -- Số lượng bán theo ĐVC --SO_LUONG_THEO_DVT_CHINH
                            SUM(CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                     THEN SL.MainQuantity
                                     ELSE 0
                                END) AS MainPromotionQuantity ,
                            SUM(CASE WHEN SL.IsPromotion = 0
                                     THEN SL.ReturnMainQuantity
                                     ELSE 0
                                END) AS MainReturnQuantity , -- Số lượng trả lại theo ĐVT chính    
                            SUM(CASE WHEN SL.IsPromotion = 1
                                     THEN SL.ReturnMainQuantity
                                     ELSE 0
                                END) AS MainReturnPromotionQuantity , -- Số lượng trả lại theo ĐVT chính    
                            SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                            SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu    --SO_TIEN_CHIET_KHAU
                            SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                            SUM(SL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá        --GIA_TRI_GIAM_TRU                        
    -- Trường không theo ĐVT chính               
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL --LII."DON_VI_CHUYEN_DOI" <> -1
                                          AND SL.UnitID = LII.UnitConvertID --SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.SaleQuantity --SO_LUONG
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.MainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(LII.ConvertRate, --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                                             1)
                                          END
                                END) AS Quantity , --SO_LUONG_BAN
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL --LII."DON_VI_CHUYEN_DOI" <> -1
                                          AND SL.UnitID = LII.UnitConvertID --SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.SaleQuantity --SO_LUONG
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1
                                               THEN SL.MainQuantity
                                                    * ISNULL(LII.ConvertRate,
                                                             1)
                                               ELSE 0
                                          END
                                END) AS PromotionQuantity , --SO_LUONG_KHUYEN_MAI
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL --LII."DON_VI_CHUYEN_DOI" <> -1
                                          AND SL.UnitID = LII.UnitConvertID --SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0
                                               ELSE SL.ReturnMainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(LII.ConvertRate, --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                                             1)
                                          END
                                END) AS ReturnQuantity , --SO_LUONG_TRA_LAI
                            SUM(CASE WHEN LII.UnitConvertID IS NOT NULL --LII."DON_VI_CHUYEN_DOI" <> -1
                                          AND SL.UnitID = LII.UnitConvertID --SL."DVT_ID" = LII."DON_VI_CHUYEN_DOI"
                                     THEN CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 --LA_HANG_KHUYEN_MAI
                                               THEN SL.ReturnMainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(LII.ConvertRate, --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                                             1)
                                               ELSE 0
                                          END
                                END) AS ReturnPromotionQuantity ,--SO_LUONG_KHUYEN_MAI_TRA_LAI
                            0 AS CostAmount  --GIA_VON
                  FROM      dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
                            INNER JOIN #tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN #tblListInventoryItemID AS LII ON SL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                            INNER JOIN #tbEmployeeID AS AO ON SL.EmployeeID = ao.EmployeeID --DS_NHAN_VIEN AS AO ON SL."NHAN_VIEN_ID" = AO."NHAN_VIEN_ID"
                            INNER JOIN #tbCustomerID AS CU ON SL.AccountObjectID = CU.AccountObjectID --DS_KHACH_HANG AS CU ON SL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
                  WHERE     SL.PostedDate BETWEEN @FromDate AND @ToDate -- SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
                  GROUP BY  SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , --MA_HANG
                            LII.MainUnitName ,--DON_VI_TINH_CHINH
                            LII.UnitName , --DON_VI_TINH
                            SL.EmployeeID , --NHAN_VIEN_ID
                            CU.AccountObjectID --KHACH_HANG_ID
                  UNION ALL
                  SELECT    CU.AccountObjectID ,--KHACH_HANG_ID
                            IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode ,--MA_HANG
                            LII.MainUnitName , --DON_VI_TINH_CHINH
                            LII.UnitName ,--DON_VI_TINH
                            IL.EmployeeID ,--NHAN_VIEN_ID
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
                            SUM(OutwardAmount - InwardAmount) AS CostAmount --GIA_VON
                  FROM      dbo.InventoryLedger IL --so_kho_chi_tiet
                            INNER JOIN #tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN #tblListInventoryItemID AS LII ON iL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON iL."MA_HANG_ID" = LII."MA_HANG_ID"
                            INNER JOIN #tbEmployeeID AS AO ON iL.EmployeeID = ao.EmployeeID --DS_NHAN_VIEN AS AO ON IL."NHAN_VIEN_ID" = AO."NHAN_VIEN_ID"
                            INNER JOIN #tbCustomerID AS CU ON IL.AccountObjectID = CU.AccountObjectID--DS_KHACH_HANG AS CU ON IL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
                  WHERE     IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy --MA_TK_CO                         
                            AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
                                  OR IL.RefType = 2013 --LOAI_CHUNG_TU
                                ) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi
                  GROUP BY  IL.InventoryItemID ,--MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng       --MA_HANG          
                            LII.MainUnitName ,--DON_VI_TINH_CHINH
                            LII.UnitName ,--DON_VI_TINH
                            IL.EmployeeID ,--NHAN_VIEN_ID
                            CU.AccountObjectID --KHACH_HANG_ID
                ) AS T
                INNER JOIN #tbEmployeeID AO ON AO.EmployeeID = T.EmployeeID --DS_NHAN_VIEN AO ON AO."NHAN_VIEN_ID" = T."NHAN_VIEN_ID"
                INNER JOIN #tblListInventoryItemID LII ON LII.InventoryItemID = T.InventoryItemID --DS_HANG_HOA LII ON LII."MA_HANG_ID" = T."MA_HANG_ID"
                INNER JOIN #tbCustomerID AS CU ON T.AccountObjectID = CU.AccountObjectID --DS_KHACH_HANG AS CU ON T."KHACH_HANG_ID" = CU."KHACH_HANG_ID"
        GROUP BY T.InventoryItemID ,--MA_HANG_ID
                T.InventoryItemCode , -- Mã hàng --MA_HANG
                LII.InventoryItemName , -- Tên hàng --TEN_HANG
                T.MainUnitName , --DON_VI_TINH_CHINH
                T.UnitName ,--DON_VI_TINH
                T.EmployeeID ,--NHAN_VIEN_ID
                AO.EmployeeCode , --MA_NHAN_VIEN
                AO.EmployeeName ,--TEN_NHAN_VIEN
                AO.EmployeeAddress ,
                AO.EmployeeMobile ,
                LII.InventoryItemCategoryName , -- tên nhóm VTHH       
                InventoryItemSource , --nvtoan add 24/07/2017
                AO.OrganizationUnitID ,
                AO.OrganizationUnitCode ,
                AO.OrganizationUnitName ,
                CU.AccountObjectID , --KHACH_HANG_ID
                CU.AccountObjectCode , --MA_KHACH_HANG
                CU.AccountObjectName , --TEN_KHACH_HANG
                CU.AccountObjectAddress ,		-- Địa chỉ
                CU.AccountObjectMobile
        HAVING  SUM(T.Quantity) <> 0 --SO_LUONG_BAN
                OR SUM(T.PromotionQuantity) <> 0--SO_LUONG_KHUYEN_MAI
                OR SUM(T.ReturnQuantity) <> 0 --SO_LUONG_TRA_LAI
                OR SUM(T.ReturnPromotionQuantity) <> 0 --SO_LUONG_KHUYEN_MAI_TRA_LAI
                OR SUM(T.SaleAmount) <> 0 --DOANH_SO_BAN
                OR SUM(T.DiscountAmount) <> 0 --SO_TIEN_CHIET_KHAU
                OR SUM(T.ReturnAmount) <> 0 --GIA_TRI_TRA_LAI
                OR SUM(T.ReduceAmount) <> 0 --GIA_TRI_GIAM_GIA
                OR SUM(T.CostAmount) <> 0 --GIA_VON
        OPTION  ( RECOMPILE )
    END

GO