SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		nvtoan
-- Create date: 21/11/2014
-- Description:	<Bán hàng: Lấy số liệu tổng hợp bán hàng theo nhân viên>
-- nmtruong 22/10/2015: sửa bug 73674: sửa join thành union để lấy lên số giá vốn
-- Modyfy by dvha 07/07/2016: Fixbug 109959: Bán hàng\ Tổng hợp bán hàng theo nhân viên, nhân viên và khách hàng: Lỗi không hiển thị số liệu báo cáo khi trả lại toàn bộ giá trị hàng bán
-- BTAnh - 12.8.2016: Bổ sung OPTION(RECOMPILE) 
-- =============================================

DECLARE    @FromDate DATETIME 
DECLARE    @ToDate DATETIME 
DECLARE    @BranchID UNIQUEIDENTIFIER  -- Chi nhánh
DECLARE    @IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE    @ListEmployeeID NVARCHAR(MAX)  -- Danh sách nhân viên
DECLARE    @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


					SET					@FromDate = '2018-01-01 00:00:00'
                    SET                    @ToDate = '2018-12-31 23:59:59'
                    SET                    @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
                    SET                    @IncludeDependentBranch = 1
                    SET                    @ListEmployeeID = N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,'
                    SET                    @IsWorkingWithManagementBook = 0


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
		                          
        DECLARE @tblListEmployeeID TABLE -- Bảng chứa danh sách nhân viên--
            (
              EmployeeID UNIQUEIDENTIFIER ,
              EmployeeCode NVARCHAR(25),
              EmployeeName NVARCHAR(255) ,
              OrganizationUnitID UNIQUEIDENTIFIER ,
              OrganizationUnitName NVARCHAR(255)
            ) 
        INSERT  INTO @tblListEmployeeID --DS_NHAN_VIEN
                SELECT  F.Value ,
						AO.AccountObjectCode, --MA_NHAN_VIEN
                        AO.AccountObjectName ,--HO_VA_TEN
                        OU.OrganizationUnitID ,--DON_VI_ID
                        OU.OrganizationUnitName --TEN_DON_VI
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ListEmployeeID,
                                                           ',') F
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = F.Value
                        LEFT JOIN dbo.OrganizationUnit OU ON AO.OrganizationUnitID = OU.OrganizationUnitID --res_partner AO LEFT JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"
        
        SELECT  ROW_NUMBER() OVER ( ORDER BY LAO.EmployeeCode ) AS RowNum ,
				T.EmployeeID , --NHAN_VIEN_ID
                LAO.EmployeeCode , -- Mã NCC --MA_NHAN_VIEN
                LAO.EmployeeName ,--TEN_NHAN_VIEN
                LAO.OrganizationUnitID , --DON_VI_ID
                LAO.OrganizationUnitName, --
                SUM(T.SaleAmount) AS SaleAmount ,--DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount , --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , --GIA_VON
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount ,
                CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) >0 
						  AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) >0
						     OR SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) <0 
							AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) <0
				      THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount)
                                       * 100 / SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount)
                                ELSE 0
                          END AS GrossProfitRate
        From
           (SELECT
                SL.EmployeeID , --NHAN_VIEN_ID                      
                SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu -- SO_TIEN_CHIET_KHAU  
                SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                SUM(SL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá   --GIA_TRI_GIAM_GIA
                0 AS CostAmount  --GIA_VON              
        FROM    dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
                INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                INNER JOIN @tblListEmployeeID AS LAO ON SL.EmployeeID = LAO.EmployeeID     -- DS_NHAN_VIEN AS LAO ON SL."NHAN_VIEN_ID" = LAO."NHAN_VIEN_ID"          
        WHERE   SL.PostedDate BETWEEN @FromDate AND @ToDate --SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
        GROUP BY SL.EmployeeID , --NHAN_VIEN_ID
                SL.EmployeeCode , --MA_NHAN_VIEN
                LAO.EmployeeName , --HO_VA_TEN
                LAO.OrganizationUnitID ,--DON_VI_ID
                LAO.OrganizationUnitName--TEN_DON_VI
        UNION ALL
			SELECT  IL.EmployeeID ,--NHAN_VIEN_ID
					0,
					0,
					0,
					0,
                    SUM(OutwardAmount - InwardAmount) AS CostAmount --GIA_VON
                FROM    dbo.InventoryLedger IL --so_kho_chi_tiet
                        INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN @tblListEmployeeID AS LAO ON IL.EmployeeID = LAO.EmployeeID --DS_NHAN_VIEN AS LAO ON IL."NHAN_VIEN_ID" = LAO."NHAN_VIEN_ID"
                WHERE   IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                        AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy--AND IL."MA_TK_CO" LIKE '632%%'                        
                        AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
                              OR IL.RefType = 2013 --LOAI_CHUNG_TU
                            ) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi
                GROUP BY IL.EmployeeID --NHAN_VIEN_ID
        ) AS T
        INNER JOIN @tblListEmployeeID LAO ON LAO.EmployeeID = T.EmployeeID -- DS_NHAN_VIEN LAO ON LAO."NHAN_VIEN_ID" = T."NHAN_VIEN_ID"
        GROUP BY T.EmployeeID , --NHAN_VIEN_ID
                LAO.EmployeeCode , -- Mã NCC --MA_NHAN_VIEN
                LAO.EmployeeName , --HO_VA_TEN
                LAO.OrganizationUnitID , --DON_VI_ID
                LAO.OrganizationUnitName --TEN_DON_VI
        /* dvha 07/07/2016: Fixbug 109959*/        
        HAVING        
        SUM(T.SaleAmount) <> 0 OR SUM(T.DiscountAmount) <> 0 OR SUM(T.ReturnAmount) <> 0 OR SUM(T.ReduceAmount) <> 0 OR SUM(T.CostAmount) <>0  --SUM(T."DOANH_SO_BAN") <> 0 OR SUM(T."SO_TIEN_CHIET_KHAU") <> 0 OR SUM(T."GIA_TRI_TRA_LAI") <> 0 OR SUM(T."GIA_TRI_GIAM_GIA") <> 0 OR SUM(T."GIA_VON") <>0;
        OPTION(RECOMPILE)
     END
    




GO