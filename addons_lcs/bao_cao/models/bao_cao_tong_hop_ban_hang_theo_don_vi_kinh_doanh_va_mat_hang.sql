SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		nmtruong
-- Create date: 5/10/2015
-- Description:	<bán hàng: Lấy số liệu tổng hợp bán hàng theo đơn vị và mặt hàng>
-- nmtruong 17/11/2015: Sửa bug 78011: sửa having để lấy lên hàng khuyến mại

-- =============================================

	DECLARE		@BranchID UNIQUEIDENTIFIER 
	DECLARE		@IncludeDependentBranch BIT 
	DECLARE		@FromDate DATETIME 
	DECLARE		@ToDate DATETIME 
	DECLARE		@OrganizationUnitID NVARCHAR(MAX) 
	DECLARE		@UnitType INT 
	DECLARE		@InventoryItemID NVARCHAR(MAX) 
	DECLARE		@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


		SET		@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET        @IncludeDependentBranch = 1
        SET        @FromDate = '2018-01-01 00:00:00'
        SET        @ToDate = '2018-12-31 23:59:59'
        SET        @OrganizationUnitID = N',07957793-f914-4097-abf3-aa8251c53bdc,1b65fcd3-07e7-4fa5-b75a-c229f5d96368,9f75f5d4-5213-4432-9d30-0da0ce72d52b,b4a83ce1-ed92-4be5-b8f3-1c480db0f1c4,b88f22a4-4cb7-4077-9414-b703cd81176f,c8b534fc-bdaf-4273-930a-33181b3e1d6f,'
        SET        @UnitType = 0
        SET        @InventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,c9386f9b-6cba-4e1a-abb6-f6391d4cc9ad,c5d407f8-0ba9-4d77-8085-d08b7eff1333,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,d304a03c-ec90-4708-9d1a-38318ba45990,e5a7407c-8933-4998-a265-3331f19845c0,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,4bb9f0d8-360e-488b-b1aa-9ff424e8f160,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,13b27260-a6cd-4957-a35f-c553043fdeb7,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
        SET        @IsWorkingWithManagementBook = 0
			
    BEGIN
        DECLARE @tblListBrandID TABLE -- Bảng chứa danh sách chi nhánh 
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(128)
            ) 
       
        INSERT  INTO @tblListBrandID --TMP_LIST_BRAND
                SELECT  FGDBBI.BranchID ,
                        FGDBBI.BranchCode
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI           
                            
        DECLARE @tblListInventoryItemID TABLE -- Bảng chứa danh sách hàng hóa
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemName NVARCHAR(255) ,
              InventoryItemCategoryCode NVARCHAR(MAX) ,
              InventoryItemCategoryName NVARCHAR(MAX),
              InventoryItemType INT ,
              UnitID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListInventoryItemID --DS_HANG_HOA
                SELECT  II.InventoryItemID , --MA_HANG_ID
                        II.InventoryItemName , --TEN_HANG
                        II.InventoryItemCategoryCode ,
                        II.InventoryItemCategoryName,
                        II.InventoryItemType , --TINH_CHAT
                        II.UnitID --DVT_CHINH_ID
                FROM    dbo.Func_ConvertGUIStringIntoTable(@InventoryItemID, ',') AS LII
                        INNER JOIN dbo.InventoryItem AS II ON II.InventoryItemID = LII.Value
      
       /*bảng chứa tham số đơn vị truyền vào ban đầu*/
        DECLARE @tblOrganizationUnitID TABLE-- 
            (
              OrganizationUnitID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS
                                       NULL ,
              OrganizationUnitCode NVARCHAR(20)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL ,
              OrganizationUnitName NVARCHAR(128)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL ,
              SortMISACodeID NVARCHAR(100)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL
              ,IsParent BIT
              ,IsParentWithChild BIT
            ) 
        INSERT  INTO @tblOrganizationUnitID /*Insert*/ --TMP_DON_VI
                SELECT DISTINCT
                        EI.OrganizationUnitID ,--DON_VI_ID
                        EI.MISACodeID , --MA_PHAN_CAP
                        EI.OrganizationUnitCode , --MA_DON_VI
                        EI.OrganizationUnitName , --TEN_DON_VI
                        EI.SortMISACodeID,
                        EI.IsParent, --ISPARENT
                        0                        
                FROM    dbo.Func_ConvertGUIStringIntoTable(@OrganizationUnitID,
                                                           ',') tString
                        INNER JOIN dbo.OrganizationUnit EI ON EI.OrganizationUnitID = tString.Value --danh_muc_to_chuc
                        
        /*Cập nhật lại bảng đầu vào xem đơn vị truyền vào có con hay là không có con được chọn trên tham số để mục đích lấy số liệu trong TH 
        + nếu chọn con và cha thì lấy số liệu của đơn vị cha= phát sinh trực tiếp của đơn vị cha và các con được chọn, 
        + nếu  không chọn đơn vị cha thì sẽ lấy số liệu của tất cả các con cộng lên */
        UPDATE T 
        SET IsParentWithChild = 1 ----------------------
        FROM @tblOrganizationUnitID T --TMP_DON_VI
        INNER JOIN @tblOrganizationUnitID T1 ON T1.MISACodeID LIKE T.MISACodeID + '%' AND T.MISACodeID <> T1.MISACodeID
        WHERE T.IsParent = 1				
          
        --SELECT * FROM   @tblOrganizationUnitID     
        DECLARE @tblOrganizationUnitID1 TABLE-- Bảng khoản mục CP khong có node không chọn
            (
              OrganizationUnitID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS
                                       NULL
            ) 
        INSERT  @tblOrganizationUnitID1
                SELECT  S.OrganizationUnitID ,
                        S.MISACodeID
                FROM    @tblOrganizationUnitID S
                        LEFT  JOIN @tblOrganizationUnitID S1 ON S1.MISACodeID LIKE S.MISACodeID
                                                              + '%'
                                                              AND S.MISACodeID <> S1.MISACodeID
                WHERE   S1.MISACodeID IS NULL 
        DECLARE @tblListOrganizationUnitID TABLE-- Bảng khoản mục CP gồm toàn bộ khoản mục CP con
            (
              OrganizationUnitID UNIQUEIDENTIFIER ,
              MISACodeID NVARCHAR(100)
            )                     
		   
        INSERT  INTO @tblListOrganizationUnitID
                SELECT DISTINCT
                        T.OrganizationUnitID ,
                        T.MISACodeID
                FROM    ( SELECT  DISTINCT
                                    EI.OrganizationUnitID ,
                                    EI.MISACodeID
                          FROM      dbo.OrganizationUnit EI
                                    INNER JOIN @tblOrganizationUnitID1 SEI ON EI.MISACodeID LIKE SEI.MISACodeID                           + '%'
                          UNION ALL
                          SELECT    EI.OrganizationUnitID ,
                                    EI.MISACodeID
                          FROM      @tblOrganizationUnitID EI
                        ) T
          
        DECLARE @tblUnitConvert TABLE 
        (	InventoryItemID UNIQUEIDENTIFIER
			,UnitID UNIQUEIDENTIFIER
			,ConvertRate DECIMAL(28,14)			
        )
        INSERT @tblUnitConvert --TMP_DON_VI_CHUYEN_DOI
        SELECT  IIUC.InventoryItemID , --id
                UnitID , --DVT_ID
                ( CASE WHEN IIUC.ExchangeRateOperator = '/' --PHEP_TINH_CHUYEN_DOI
                       THEN IIUC.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                       WHEN IIUC.ConvertRate = 0 --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                       THEN 1
                       ELSE 1
                            / IIUC.ConvertRate--TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                  END ) AS ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
        FROM    dbo.InventoryItemUnitConvert IIUC --danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi
        WHERE   IIUC.SortOrder = @UnitType   --IIUC."STT" = don_vi_tinh         
       	
        SELECT  ROW_NUMBER() OVER ( ORDER BY P.OrganizationUnitCode, T.InventoryItemCode ) AS RowNum ,
                P.OrganizationUnitID ,
                P.OrganizationUnitCode AS OrganizationUnitCode ,
                P.OrganizationUnitName AS OrganizationUnitName ,
                T.InventoryItemID ,
                T.InventoryItemCode  -- Mã hàng
                ,T.InventoryItemName  -- Tên hàng
                ,T.MainUnitName ,
                T.UnitName ,
                SUM(T.Quantity) AS Quantity ,
                SUM(T.MainQuantity) AS MainQuantity ,
                SUM(T.PromotionQuantity) AS PromotionQuantity ,
                SUM(T.MainPromotionQuantity) AS MainPromotionQuantity ,
                SUM(T.ReturnQuantity) AS ReturnQuantity ,
                SUM(T.MainReturnQuantity) AS MainReturnQuantity ,
                SUM(T.ReturnPromotionQuantity) AS ReturnPromotionQuantity ,
                SUM(T.MainReturnPromotionQuantity) AS MainReturnPromotionQuantity ,
                SUM(T.SaleAmount) AS SaleAmount ,
                SUM(T.DiscountAmount) AS DiscountAmount ,
                SUM(T.ReturnAmount) AS ReturnAmount ,
                SUM(T.ReduceAmount) AS ReduceAmount ,
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount ,
                SUM(T.CostAmount) AS CostAmount ,
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount ,
                CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) >0 
						  AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) >0
						     OR SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) <0 
							AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) <0
				      THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount)
                                       * 100 / SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount)
                                ELSE 0
                          END AS GrossProfitRate ,
                T.InventoryItemCategoryName
                --[dbo].[Func_GetInventoryCategoryListName](T.InventoryItemCategoryCode) AS InventoryItemCategoryName
        FROM    ( SELECT    OU.OrganizationUnitID , --DON_VI_ID
							OU.MisaCodeID, --MA_PHAN_CAP
                            SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng--TEN_HANG
                            LII.InventoryItemCategoryCode,
                            LII.InventoryItemCategoryName,
                            UI.UnitName AS MainUnitName ,
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END AS UnitName , --DON_VI_TINH
                            SUM(CASE SL.IsPromotion
                                  WHEN 0 THEN SL.MainQuantity
                                  ELSE 0
                                END) AS MainQuantity , -- Số lượng bán theo ĐVC
                            SUM(CASE SL.IsPromotion
                                  WHEN 1 THEN SL.MainQuantity
                                  ELSE 0
                                END) AS MainPromotionQuantity , -- Số lượng KM theo ĐVC
                            SUM(CASE SL.IsPromotion
                                  WHEN 0 THEN SL.ReturnMainQuantity
                                  ELSE 0
                                END) AS MainReturnQuantity , -- Số lượng trả lại theo ĐVT chính    
                            SUM(CASE SL.IsPromotion
                                  WHEN 1 THEN SL.ReturnMainQuantity
                                  ELSE 0
                                END) AS MainReturnPromotionQuantity , -- Số lượng KM trả lại theo ĐVT chính    
                            SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                            SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu --SO_TIEN_CHIET_KHAU
                            SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                            SUM(SL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá -- GIA_TRI_GIAM_GIA                                  
                            SUM(CASE WHEN U.UnitID IS NOT NULL --U."id" <> -1
                                          AND SL.UnitID = U.UnitID --SL."DVT_ID" = U."id"
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.SaleQuantity --SO_LUONG
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0 --LA_HANG_KHUYEN_MAI
                                               ELSE SL.MainQuantity  --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                          END
                                END) AS Quantity , --SO_LUONG_BAN
                            SUM(CASE WHEN U.UnitID IS NOT NULL --U."id" <> -1
                                          AND SL.UnitID = U.UnitID ----SL."DVT_ID" = U."id"
                                     THEN CASE WHEN SL.IsPromotion = 1
                                               THEN SL.SaleQuantity
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1
                                               THEN SL.MainQuantity --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                               ELSE 0
                                          END
                                END) AS PromotionQuantity , --SO_LUONG_KHUYEN_MAI
                            SUM(CASE WHEN U.UnitID IS NOT NULL
                                          AND SL.UnitID = U.UnitID
                                     THEN CASE WHEN SL.IsPromotion = 1 THEN 0
                                               ELSE SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1 THEN 0
                                               ELSE SL.ReturnMainQuantity  --SO_LUONG_THEO_DVT_CHINH
                                                    * ISNULL(UC.ConvertRate, 1) --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                          END
                                END) AS ReturnQuantity , --SO_LUONG_TRA_LAI
                            SUM(CASE WHEN U.UnitID IS NOT NULL
                                          AND SL.UnitID = U.UnitID
                                     THEN CASE WHEN SL.IsPromotion = 1
                                               THEN SL.ReturnQuantity --SO_LUONG_TRA_LAI
                                               ELSE 0
                                          END
                                     ELSE CASE WHEN SL.IsPromotion = 1
                                               THEN SL.ReturnMainQuantity
                                                    * ISNULL(UC.ConvertRate, 1)
                                               ELSE 0
                                          END
                                END) AS ReturnPromotionQuantity --SO_LUONG_KHUYEN_MAI_TRA_LAI
                            ,0 AS CostAmount --GIA_VON
                  FROM      dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
                            INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN @tblListInventoryItemID AS LII ON SL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
                            INNER JOIN @tblListOrganizationUnitID OU ON SL.OrganizationUnitID = OU.OrganizationUnitId --TMP_DON_VI OU ON SL."DON_VI_ID" = OU."DON_VI_ID"
                            LEFT JOIN dbo.Unit UI ON LII.UnitID = UI.UnitID --danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI."id"
                            LEFT JOIN @tblUnitConvert UC ON LII.InventoryItemID = UC.InventoryItemID --TMP_DON_VI_CHUYEN_DOI UC ON LII."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                            LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL --danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" = -1
                                                      AND U.UnitID = LII.UnitID --U."id" = LII."DVT_CHINH_ID"
                                                    )
                                                    OR ( UC.InventoryItemID IS NOT NULL --UC."VAT_TU_HANG_HOA_ID" <> -1
                                                         AND UC.UnitID = U.UnitID --C."DVT_ID" = U."id"
                                                       )                           
                  WHERE     ( @UnitType IS NULL --don_vi_tinh
                              OR @UnitType = 0 --don_vi_tinh
                              OR UC.InventoryItemID IS NOT NULL --VAT_TU_HANG_HOA_ID
                            )
                            AND SL.PostedDate BETWEEN @FromDate AND @ToDate --SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
                  GROUP BY  OU.OrganizationUnitID ,--DON_VI_ID
							OU.MisaCodeID,--MA_PHAN_CAP
                            SL.InventoryItemID , --MA_HANG_ID
                            SL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN_HANG
                            LII.InventoryItemName , -- Tên hàng                       
                            LII.InventoryItemCategoryCode,   
                            LII.InventoryItemCategoryName,                         
                            UI.UnitName , --DON_VI_TINH
                            CASE WHEN LII.UnitID IS NULL THEN ''
                                 ELSE U.UnitName --DON_VI_TINH
                            END                  
                  UNION ALL
                  SELECT    OU.OrganizationUnitID , --DON_VI_ID
							OU.MisaCodeID, --MA_PHAN_CAP
                            IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN_HANG
                            LII.InventoryItemCategoryCode,
                            LII.InventoryItemCategoryName,
                            UI.UnitName AS MainUnitName ,--DON_VI_TINH_CHINH
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END AS UnitName , --DON_VI_TINH
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                        SUM(IL.OutwardAmount - IL.InwardAmount) AS CostAmount --SUM(IL."SO_TIEN_XUAT" - IL."SO_TIEN_NHAP") AS "GIA_VON"
                FROM    dbo.InventoryLedger IL --so_kho_chi_tiet
                        INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN @tblListInventoryItemID AS LII ON iL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON iL."MA_HANG_ID" = LII."MA_HANG_ID"
                        INNER JOIN @tblListOrganizationUnitID OU ON IL.OrganizationUnitID = OU.OrganizationUnitId --TMP_DON_VI OU ON IL."DON_VI_ID" = OU."DON_VI_ID"
                        LEFT JOIN dbo.Unit UI ON LII.UnitID = UI.UnitID --danh_muc_don_vi_tinh UI ON LII."DVT_CHINH_ID" = UI."id"
                        LEFT JOIN @tblUnitConvert UC ON LII.InventoryItemID = UC.InventoryItemID --TMP_DON_VI_CHUYEN_DOI UC ON LII."MA_HANG_ID" = UC."VAT_TU_HANG_HOA_ID"
                        LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL --VAT_TU_HANG_HOA_ID
                                                  AND U.UnitID = LII.UnitID --U."id" = LII."DVT_CHINH_ID"
                                                )
                                                OR ( UC.InventoryItemID IS NOT NULL --VAT_TU_HANG_HOA_ID
                                                     AND UC.UnitID = U.UnitID --UC."DVT_ID" = U."id"
                                                   )                    
                WHERE   IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                        AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy --IL."MA_TK_CO" LIKE '632%%'     
                        AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
                              OR IL.RefType = 2013 --LOAI_CHUNG_TU
                            ) 
                        AND ( @UnitType IS NULL --don_vi_tinh
                              OR @UnitType = 0
                              OR UC.InventoryItemID IS NOT NULL --VAT_TU_HANG_HOA_ID
                            )
                GROUP BY 
						OU.OrganizationUnitID , --DON_VI_ID
							OU.MisaCodeID, --MA_PHAN_CAP
                            IL.InventoryItemID , --MA_HANG_ID
                            IL.InventoryItemCode , -- Mã hàng --MA_HANG
                            LII.InventoryItemName , -- Tên hàng --TEN_HANG
                            LII.InventoryItemCategoryCode,
                            LII.InventoryItemCategoryName,
                            UI.UnitName, --DON_VI_TINH
                            CASE WHEN LII.UnitID IS NULL THEN '' --DVT_CHINH_ID
                                 ELSE U.UnitName --DON_VI_TINH
                            END	
                HAVING SUM(IL.OutwardAmount - IL.InwardAmount) <>0 --SUM(IL."SO_TIEN_XUAT" - IL."SO_TIEN_NHAP") <> 0
                ) T
                INNER JOIN @tblOrganizationUnitID P ON 
						((P.IsParent = 0 OR P.IsParentWithChild = 1) AND T.OrganizationUnitID = P.OrganizationUnitID) 
						OR (P.IsParent = 1 AND P.IsParentWithChild = 0 AND T.MisaCodeID LIKE P.MisaCodeID + '%')
        GROUP BY P.OrganizationUnitID , --DON_VI_ID
                P.OrganizationUnitCode , --MA_DON_VI
                P.OrganizationUnitName , --TEN_DON_VI
                T.InventoryItemID , --MA_HANG_ID
                T.InventoryItemCode,  -- Mã hàng   --    MA_HANG          ,
                T.InventoryItemName,  -- Tên hàng          -- TEN_HANG      ,
                T.MainUnitName , --DON_VI_TINH_CHINH
                T.UnitName ,   --DON_VI_TINH
                T.InventoryItemCategoryName
                --[dbo].[Func_GetInventoryCategoryListName](T.InventoryItemCategoryCode)                
        HAVING
			SUM(T.Quantity) <>0 Or	-- SO_LUONG_BAN					
			SUM(T.PromotionQuantity)  <>0 Or		 --	SO_LUONG_KHUYEN_MAI			
			SUM(T.ReturnQuantity) <>0 Or		--SO_LUONG_TRA_LAI				
			SUM(T.ReturnPromotionQuantity) <>0 Or	 --SO_LUONG_KHUYEN_MAI_TRA_LAI					
			SUM(T.SaleAmount)  <>0 OR--DOANH_SO_BAN
			SUM(T.DiscountAmount) <>0 OR --SO_TIEN_CHIET_KHAU
			SUM(T.ReturnAmount)  <>0 OR --GIA_TRI_TRA_LAI
			SUM(T.ReduceAmount)  <>0 Or			 --GIA_TRI_GIAM_GIA			
			SUM(T.CostAmount) <>0     --GIA_VON
		OPTION (RECOMPILE)
    
    END

GO