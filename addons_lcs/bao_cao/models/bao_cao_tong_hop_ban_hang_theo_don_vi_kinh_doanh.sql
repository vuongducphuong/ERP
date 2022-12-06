SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		nvtoan
-- Create date: 26/11/2014
-- Description:	<bán hàng: Lấy số liệu tổng hợp bán hàng theo đơn vị>
-- nmtruong 22/10/2015: 73674 Dùng union để lấy lên giá vốn và sửa lỗi tỷ lệ lãi gộp bị âm
-- BTAnh - 12.8.2016: Bổ sung OPTION(RECOMPILE) 
-- =============================================

		DECLARE		@BranchID UNIQUEIDENTIFIER 
		DECLARE		@IncludeDependentBranch BIT 
		DECLARE		@FromDate DATETIME 
		DECLARE		@ToDate DATETIME 
		DECLARE		@OrganizationUnitID UNIQUEIDENTIFIER = NULL 
		DECLARE		@ListInventoryItemID NVARCHAR(MAX) 
		DECLARE		@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


				SET		@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
				SET		@IncludeDependentBranch = 1
				SET		@FromDate = '2018-01-01 00:00:00'
				SET		@ToDate = '2018-12-31 23:59:59'
				SET		@OrganizationUnitID = NULL
				SET		@ListInventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,c9386f9b-6cba-4e1a-abb6-f6391d4cc9ad,c5d407f8-0ba9-4d77-8085-d08b7eff1333,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,d304a03c-ec90-4708-9d1a-38318ba45990,e5a7407c-8933-4998-a265-3331f19845c0,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,4bb9f0d8-360e-488b-b1aa-9ff424e8f160,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,13b27260-a6cd-4957-a35f-c553043fdeb7,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
				SET		@IsWorkingWithManagementBook = 0

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
              InventoryItemID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListInventoryItemID --DS_HANG_HOA
                SELECT  f.Value
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ListInventoryItemID,
                                                           ',') AS f
		DECLARE @MisaCodeID AS NVARCHAR(100)
		SET @MisaCodeID = (SELECT MisaCodeID + '%' FROM dbo.OrganizationUnit WHERE OrganizationUnitID = @OrganizationUnitID) --concat("MA_PHAN_CAP", '%%') INTO MA_PHAN_CAP FROM danh_muc_to_chuc WHERE "id" = don_vi_id;
		

        SELECT  ROW_NUMBER() OVER ( ORDER BY T.OrganizationUnitCode, T.OrganizationUnitName ) AS RowNum ,-- ORDER BY T."MA_DON_VI", T."TEN_DON_VI" ) AS RowNum
				T.OrganizationUnitID , --DON_VI_ID
				T.OrganizationUnitCode , --MA_DON_VI
				T.OrganizationUnitName ,--TEN_DON_VI
                SUM(T.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu   --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá  --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount , --Doanh thu thuần --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , --GIA_VON
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount,
				CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) > 0 AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) >0 
							OR SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) <0 AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) < 0 
                       THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) * 100 
                       / SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount)
                       ELSE 0
                  END
                AS GrossProfitRate
        FROM        
        (SELECT
                SL.OrganizationUnitID , --DON_VI_ID
                OU.OrganizationUnitCode , --MA_DON_VI
                OU.OrganizationUnitName ,--TEN_DON_VI
                SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu   -- SO_TIEN_CHIET_KHAU
                SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                SUM(SL.ReduceAmount) AS ReduceAmount,  -- Giá trị giảm giá --GIA_TRI_GIAM_GIA
                0 AS CostAmount --GIA_VON
        FROM    dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
                INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                INNER JOIN @tblListInventoryItemID AS II ON SL.InventoryItemID = II.InventoryItemID --DS_HANG_HOA AS II ON SL."MA_HANG_ID" = II."id"
                INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = SL.OrganizationUnitID --danh_muc_to_chuc OU ON OU."id" = SL."DON_VI_ID"
                --LEFT JOIN dbo.Unit AS MU ON SL.MainUnitID = MU.UnitID -- Danh mục ĐVT -> ĐVT chính                 
        WHERE   SL.PostedDate BETWEEN @FromDate AND @ToDate  --SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
                AND ( @OrganizationUnitID IS NULL OR OU.MISACodeID LIKE @MisaCodeID) --( don_vi_id = -1 OR OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP)
        GROUP BY SL.OrganizationUnitID , --DON_VI_ID
                OU.OrganizationUnitCode , --MA_DON_VI
                OU.OrganizationUnitName  --TEN_DON_VI
        
        UNION ALL
        SELECT  IL.OrganizationUnitID ,--DON_VI_ID
                OU.OrganizationUnitCode ,--MA_DON_VI
                OU.OrganizationUnitName , --TEN_DON_VI
                0,
                0,
                0,
                0,
				SUM(OutwardAmount - InwardAmount) AS CostAmount --SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                FROM    dbo.InventoryLedger IL--so_kho_chi_tiet
                        INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN @tblListInventoryItemID AS II ON iL.InventoryItemID = II.InventoryItemID --DS_HANG_HOA AS II ON iL."MA_HANG_ID" = II."id"
                        INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = iL.OrganizationUnitID --danh_muc_to_chuc OU ON OU."id" = iL."DON_VI_ID"
                WHERE   IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                        AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy -- IL."MA_TK_CO" LIKE '632%'                        
                        AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
                              OR IL.RefType = 2013 --LOAI_CHUNG_TU
                            ) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi
                        AND ( @OrganizationUnitID IS NULL OR OU.MISACodeID LIKE @MisaCodeID) --don_vi_id = -1 OR OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP
                GROUP BY IL.OrganizationUnitID ,--DON_VI_ID
						OU.OrganizationUnitCode , --MA_DON_VI
						OU.OrganizationUnitName  --TEN_DON_VI
		) T  
		GROUP BY 
				T.OrganizationUnitID ,--DON_VI_ID
				T.OrganizationUnitCode , --MA_DON_VI
				T.OrganizationUnitName --TEN_DON_VI
		HAVING  SUM(T.SaleAmount) <> 0 --DOANH_SO_BAN
                OR SUM(T.DiscountAmount) <> 0 --SO_TIEN_CHIET_KHAU
                OR SUM(T.ReturnAmount) <> 0 --GIA_TRI_TRA_LAI
                OR SUM(T.ReduceAmount) <> 0 --GIA_TRI_TRA_LAI
                OR SUM(T.CostAmount)<>0 --GIA_VON
        OPTION(RECOMPILE)
				
    END
    



GO