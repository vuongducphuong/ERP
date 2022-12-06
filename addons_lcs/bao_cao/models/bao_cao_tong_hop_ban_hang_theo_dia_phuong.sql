SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		nvtoan
-- Create date: 25/11/2014
-- Description:	<bán hàng: Lấy số liệu tổng hợp bán hàng theo địa phương>
-- Modified by HHSon - 12.10.2015 - Fix bug 73699
-- nmtruong 22/10/2015: 73674 Dùng union để lấy lên giá vốn và sửa lỗi tỷ lệ lãi gộp bị âm
-- =============================================

 DECLARE   @BranchID UNIQUEIDENTIFIER 
 DECLARE   @IncludeDependentBranch BIT 
 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @ProvinceCity NVARCHAR(255) = NULL 
 DECLARE   @District NVARCHAR(255) = NULL 
 DECLARE   @Village NVARCHAR(255) = NULL 
 DECLARE   @EmployeeID UNIQUEIDENTIFIER = NULL 
 DECLARE   @InventoryItemID UNIQUEIDENTIFIER = NULL 
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?

							SET			@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
                            SET            @IncludeDependentBranch = 1
                            SET            @FromDate = '2018-01-01 00:00:00'
                            SET            @ToDate = '2018-12-31 23:59:59'
                            SET            @ProvinceCity = NULL
                            SET            @District = NULL
                            SET            @Village = NULL
                            SET            @EmployeeID = NULL
                            SET            @InventoryItemID = NULL
                            SET            @IsWorkingWithManagementBook = 0

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
                                      
        SELECT  ROW_NUMBER() OVER ( ORDER BY T.ProvinceOrCity, T.District, T.WardOrCommune ) AS RowNum , --ORDER BY T."TINH_TP_ID", T."QUAN_HUYEN_ID", T."XA_PHUONG_ID" )  AS RowNum       		
				@InventoryItemID AS InventoryItemID , --mat_hang_id
                T.ProvinceOrCity ,--TINH_TP_ID
                T.District ,--QUAN_HUYEN_ID
                T.WardOrCommune , --XA_PHUONG_ID
                SUM(T.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu   --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá   --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount , --Doanh thu thuần --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount ,
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
					AO.ProvinceOrCity ,--TINH_TP_ID
					AO.District , --QUAN_HUYEN_ID
					AO.WardOrCommune , --XA_PHUONG_ID
					SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
					SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu  -- SO_TIEN_CHIET_KHAU
					SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
					SUM(SL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá   --GIA_TRI_GIAM_GIA
					0 AS CostAmount
			FROM    dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
					INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
					INNER JOIN dbo.InventoryItem AS II ON SL.InventoryItemID = II.InventoryItemID --danh_muc_vat_tu_hang_hoa AS II ON SL."MA_HANG_ID" = II."id"
					INNER JOIN dbo.AccountObject AS AO ON SL.AccountObjectID = AO.AccountObjectID --Join để kiểm tra theo tham số địa phương    --res_partner AS AO ON SL."DOI_TUONG_ID" = AO.id                                         
			WHERE   SL.PostedDate BETWEEN @FromDate AND @ToDate --SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
					AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
					AND ( @EmployeeID IS NULL --nhan_vien_id = -1
						  OR SL.EmployeeID = @EmployeeID --SL."NHAN_VIEN_ID" = nhan_vien_id
						)
					AND ( @InventoryItemID IS NULL -- mat_hang_id = -1
						  OR sl.InventoryItemID = @InventoryItemID --sl."MA_HANG_ID" = mat_hang_id
						)
					AND ( @ProvinceCity IS NULL --tinh_tp_id = -1
						  OR ao.ProvinceOrCity = @ProvinceCity --ao."TINH_TP_ID" = tinh_tp_id
						)
					AND ( @District IS NULL --quan_huyen_id = -1
						  OR ao.District = @District --ao."QUAN_HUYEN_ID" = quan_huyen_id
						)
					AND ( @Village IS NULL --phuong_xa_id = -1
						  OR ao.WardOrCommune = @Village --ao."XA_PHUONG_ID" = phuong_xa_id
						)
			GROUP BY AO.ProvinceOrCity , --TINH_TP_ID
					AO.District , --QUAN_HUYEN_ID
					AO.WardOrCommune --XA_PHUONG_ID
			UNION ALL
			SELECT  AO.ProvinceOrCity,--TINH_TP_ID
                    AO.District,  --QUAN_HUYEN_ID
                    AO.WardOrCommune, --XA_PHUONG_ID
                    0,0,0,0,
                    SUM(OutwardAmount - InwardAmount) AS CostAmount
            FROM    dbo.InventoryLedger IL --so_kho_chi_tiet
                    INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                    INNER JOIN dbo.AccountObject AS AO ON IL.AccountObjectID = AO.AccountObjectID --Join để kiểm tra theo tham số địa phương --res_partner AS AO ON IL."DOI_TUONG_ID" = AO.id               
            WHERE   IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                    AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                    AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy   -- MA_TK_CO                       
                    AND ( @EmployeeID IS NULL --nhan_vien_id = -1
                          OR IL.EmployeeID = @EmployeeID --IL."NHAN_VIEN_ID" = nhan_vien_id
                        )
                    AND ( @InventoryItemID IS NULL --mat_hang_id = -1
                          OR il.InventoryItemID = @InventoryItemID --il."MA_HANG_ID" = mat_hang_id
                        )
                    AND ( @ProvinceCity IS NULL --tinh_tp_id = -1
                          OR ao.ProvinceOrCity = @ProvinceCity --ao."TINH_TP_ID" = tinh_tp_id
                        )
                    AND ( @District IS NULL --quan_huyen_id = -1
                          OR ao.District = @District --ao."QUAN_HUYEN_ID" = quan_huyen_id
                        )
                    AND ( @Village IS NULL --phuong_xa_id = -1
                          OR ao.WardOrCommune = @Village --ao."XA_PHUONG_ID" = phuong_xa_id
                        )
                    AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
                          OR IL.RefType = 2013 --LOAI_CHUNG_TU
                        ) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi
            GROUP BY AO.ProvinceOrCity, --TINH_TP_ID
                    AO.District, --QUAN_HUYEN_ID
                    AO.WardOrCommune --XA_PHUONG_ID
           ) T	
           GROUP BY 
				T.ProvinceOrCity , --TINH_TP_ID
                T.District , --QUAN_HUYEN_ID
                T.WardOrCommune 		 --XA_PHUONG_ID
        
    END
    



GO