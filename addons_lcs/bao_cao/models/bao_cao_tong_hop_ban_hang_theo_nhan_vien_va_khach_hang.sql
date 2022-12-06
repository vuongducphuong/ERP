SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		BTAnh
-- Create date: 29/05/2015
-- Description:	Lấy số liệu cho báo cáo "Tổng hợp bán hàng theo nhân viên và khách hàng"
-- nmtruong 22/10/2015: sửa bug 73674: sửa join thành union để lấy lên số giá vốn
-- Modyfy by dvha 07/07/2016: Fixbug 109959: Bán hàng\ Tổng hợp bán hàng theo nhân viên, nhân viên và khách hàng: Lỗi không hiển thị số liệu báo cáo khi trả lại toàn bộ giá trị hàng bán
-- BTAnh - 12.8.2016: Bổ sung OPTION(RECOMPILE) 
-- =============================================

 DECLARE   @FromDate DATETIME
 DECLARE   @ToDate DATETIME
 DECLARE   @BranchID UNIQUEIDENTIFIER -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @EmployeeID NVARCHAR(MAX) --Danh sách nhân viên
 DECLARE   @AccountObjectID NVARCHAR(MAX)  --Danh sách khách hàng
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?

	SET			@FromDate = '2018-01-01 00:00:00'
    SET            @ToDate = '2018-12-31 23:59:59'
    SET            @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
    SET            @IncludeDependentBranch = 1
    SET            @EmployeeID = N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,'
    SET            @AccountObjectID = N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,8b0ba43a-1120-4574-905d-e2abff045f13,'
    SET            @IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblListBrandID TABLE -- Bảng chứa danh sách chi nhánh --TMP_LIST_BRAND
            (
             BranchID UNIQUEIDENTIFIER,
             BranchCode NVARCHAR(128)
            )	
       
        INSERT  INTO @tblListBrandID
                SELECT  FGDBBI.BranchID,
                        FGDBBI.BranchCode
                FROM    dbo.Func_GetDependentByBranchID(@BranchID, @IncludeDependentBranch) AS FGDBBI           
		                          
-----------------------------------------		
		DECLARE @tbCustomerID TABLE -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER,
              AccountObjectCode NVARCHAR(25),
              AccountObjectName NVARCHAR(255),
              AccountObjectAddress NVARCHAR(255),
              AccountObjectTaxCode NVARCHAR(50),
              AccountObjectGroupListCode NVARCHAR(MAX),
              AccountObjectGroupListName NVARCHAR(MAX)
            ) 
        INSERT  INTO @tbCustomerID --DS_KHACH_HANG
                SELECT  Value,
						AccountObjectCode, --MA_KHACH_HANG
						AccountObjectName, --HO_VA_TEN
						[Address], --DIA_CHI
						CompanyTaxCode, --MA_SO_THUE
						AccountObjectGroupListCode,--LIST_MA_NHOM_KH_NCC
						AccountObjectGroupListName --LIST_TEN_NHOM_KH_NCC
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID, ',') AS F -- FROM res_partner WHERE ("id" IN(81, 79, 82, 83, 85, 84, 80, 77, 76, 78, 75))
					INNER JOIN dbo.AccountObject AOD ON AOD.AccountObjectID = F.Value
					
-----------------------------------------                
        DECLARE @tbEmployeeID TABLE -- Bảng chứa danh sách khách hàng --DS_NHAN_VIEN
            (
				EmployeeID UNIQUEIDENTIFIER,
				EmployeeCode NVARCHAR(25),
				EmployeeName NVARCHAR(128),
				OrganizationUnitName NVARCHAR(255)
            ) 
----------------------------------------
        INSERT  INTO @tbEmployeeID --DS_NHAN_VIEN
        SELECT  Value,
				AO.AccountObjectCode,
				AO.AccountObjectName,
				O.OrganizationUnitName
        FROM    dbo.Func_ConvertGUIStringIntoTable(@EmployeeID,',') AS F
			JOIN dbo.AccountObject AS AO ON F.Value = AO.AccountObjectID
			JOIN dbo.OrganizationUnit AS O ON AO.OrganizationUnitID = O.OrganizationUnitID 
-----------------------------------------                
                        
-----------------------------------------                
        SELECT  
				ROW_NUMBER() OVER (ORDER BY E.EmployeeCode, CU.AccountObjectCode) AS RowNum, -- ROW_NUMBER() OVER (ORDER BY E."MA_NHAN_VIEN", CU."MA_KHACH_HANG") AS RowNum,
				E.EmployeeID, --NHAN_VIEN_ID
                E.EmployeeCode, -- Mã nhân viên --MA_NHAN_VIEN
                E.EmployeeName,  --    TEN_NHAN_VIEN           
                CU.AccountObjectID, -- DOI_TUONG_ID
                CU.AccountObjectCode, --MA_KHACH_HANG
                CU.AccountObjectName, --TEN_KHACH_HANG
                CU.AccountObjectAddress,		-- Địa chỉ --DIA_CHI
                CU.AccountObjectTaxCode, -- MA_SO_THUE
                 CU.AccountObjectGroupListCode, --LIST_MA_NHOM_KH_NCC
                CU.AccountObjectGroupListName,                --LIST_TEN_NHOM_KH_NCC
                E.OrganizationUnitName AS EmployeeDepartmentName, --DON_VI_KHINH_DOANH
                SUM(T.SaleAmount) AS SaleAmount , --DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount , --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , --GIA_VON
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount ,--SUM(T."DOANH_SO_BAN" - T."SO_TIEN_CHIET_KHAU" - T."GIA_TRI_TRA_LAI" - T."GIA_TRI_GIAM_GIA" -T."GIA_VON") AS "LAI_GOP"
                CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) >0 
						  AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) >0
						     OR SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) <0 
							AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) <0
				      THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount)
                                       * 100 / SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount)
                                ELSE 0
                          END AS GrossProfitRate --TY_LE_LAI_GOP
                
		FROM
			(SELECT
                SL.EmployeeID,--NHAN_VIEN_ID                
                SL.AccountObjectID,         --  DOI_TUONG_ID                       
                SUM(SL.SaleAmount) AS SaleAmount, -- Doanh số bán --DOANH_SO_BAN
                SUM(SL.DiscountAmount) AS DiscountAmount, -- Tiền chiết khấu    --SO_TIEN_CHIET_KHAU
                SUM(SL.ReturnAmount) AS ReturnAmount, -- Giá trị trả lại --GIA_TRI_TRA_LAI
                SUM(SL.ReduceAmount) AS ReduceAmount, -- Giá trị giảm giá --GIA_TRI_GIAM_GIA
                0 AS CostAmount      --         GIA_VON 
			FROM    dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
					INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
					INNER JOIN @tbCustomerID AS CU ON SL.AccountObjectID = CU.AccountObjectID --DS_KHACH_HANG AS CU ON SL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"
					INNER JOIN @tbEmployeeID AS E ON SL.EmployeeID = E.EmployeeID --    DS_NHAN_VIEN AS E ON SL."NHAN_VIEN_ID" = E."NHAN_VIEN_ID"          
			WHERE   SL.PostedDate BETWEEN @FromDate AND @ToDate   --"NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
					AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
			GROUP BY 
					SL.EmployeeID,   --NHAN_VIEN_ID              
					SL.AccountObjectID --DOI_TUONG_ID
			UNION ALL
			SELECT  IL.EmployeeID, --NHAN_VIEN_ID
					IL.AccountObjectID,--DOI_TUONG_ID
					0,0,0,0,
					SUM(OutwardAmount - InwardAmount) AS CostAmount --GIA_VON
			FROM    dbo.InventoryLedger IL --so_kho_chi_tiet
					INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
					INNER JOIN @tbCustomerID AS CU ON IL.AccountObjectID = CU.AccountObjectID   -- DS_KHACH_HANG AS CU ON IL."DOI_TUONG_ID" = CU."KHACH_HANG_ID"             
					INNER JOIN @tbEmployeeID AS E ON iL.EmployeeID = E.EmployeeID --DS_NHAN_VIEN AS E ON IL."NHAN_VIEN_ID" = E."NHAN_VIEN_ID"
			WHERE   IL.PostedDate BETWEEN @FromDate AND @ToDate -- "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
					AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
					AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy --IL."MA_TK_CO" LIKE '632%%' 
					AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
								  OR IL.RefType = 2013 --LOAI_CHUNG_TU
								) --HHSon edited 03.06.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi                          
			GROUP BY IL.EmployeeID, --NHAN_VIEN_ID
					IL.AccountObjectID --DOI_TUONG_ID
			) AS T
			INNER JOIN @tbEmployeeID E ON E.EmployeeID = T.EmployeeID --DS_NHAN_VIEN E ON E."NHAN_VIEN_ID" = T."NHAN_VIEN_ID"
			INNER JOIN @tbCustomerID CU ON CU.AccountObjectID = T.AccountObjectID -- DS_KHACH_HANG CU ON CU."KHACH_HANG_ID" = T."DOI_TUONG_ID"
			GROUP BY
				E.EmployeeID, --NHAN_VIEN_ID
                E.EmployeeCode, -- Mã nhân viên --MA_NHAN_VIEN
                E.EmployeeName,  --    TEN_NHAN_VIEN          
                CU.AccountObjectID, --KHACH_HANG_ID
                CU.AccountObjectCode, --MA_KHACH_HANG
                CU.AccountObjectName,--TEN_KHACH_HANG
                CU.AccountObjectAddress,		-- Địa chỉ --DIA_CHI
                CU.AccountObjectTaxCode, --MA_SO_THUE
                CU.AccountObjectGroupListCode, --LIST_MA_NHOM_KH_NCC
                CU.AccountObjectGroupListName,      --LIST_TEN_NHOM_KH_NCC           
                E.OrganizationUnitName --TEN_DON_VI
            /* dvha 07/07/2016: Fixbug 109959 - Nếu một trong số các cột */  
			HAVING
				SUM(T.SaleAmount) <> 0 OR SUM(T.DiscountAmount) <> 0 OR SUM(T.ReturnAmount) <> 0 OR SUM(T.ReduceAmount) <> 0 OR SUM(T.CostAmount) <>0             
			OPTION(RECOMPILE)
	
        
    END
    



GO