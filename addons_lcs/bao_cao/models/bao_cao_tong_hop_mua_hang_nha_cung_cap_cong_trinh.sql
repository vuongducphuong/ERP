SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		<VHAnh>
-- Create date: <19/11/2015>
-- Description:	Lấy số liệu Báo cáo Tổng hợp mua hàng theo công trình và nhà cung cấp
-- Modified 26.11.2015: Không lấy MisaCodeID khi select
-- =============================================

  DECLARE  @FromDate DATETIME 
  DECLARE  @ToDate DATETIME 
  DECLARE  @BranchID UNIQUEIDENTIFIER  -- Chi nhánh
  DECLARE  @IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
  DECLARE  @ProjectWorkID NVARCHAR(MAX)  -- Danh sách hàng hóa, 
  DECLARE  @AccountObjectID NVARCHAR(MAX)  -- Danh sách nhà cung cấp,
  DECLARE  @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?    

											SET		@FromDate = '2018-01-01 00:00:00'
                                            SET         @ToDate = '2018-12-31 23:59:59'
                                            SET         @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
                                            SET         @IncludeDependentBranch = 1
                                            SET         @ProjectWorkID = N',9b46c3a0-060f-4b8e-a5e2-4786271f51d9,c0570228-b65f-44c8-acee-3da2ae38d590,e9b86b73-2026-4fe1-9e49-9f0d0c7ee9ac,'
                                            SET         @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
                                            SET         @IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblListBrandID TABLE -- Bảng chứa danh sách chi nhánh --
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
		                          
        DECLARE @tblProjectWorkSelected TABLE -- Bảng các công trình được chọn --TMP_CONG_TRINH_DC_CHON
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) ,
              ProjectWorkCode NVARCHAR(20) ,
              ProjectWorkName NVARCHAR(128) ,
              ProjectWorkCategoryID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblProjectWorkSelected --TMP_CONG_TRINH_DC_CHON
                SELECT DISTINCT
                        PW.ProjectWorkID ,--CONG_TRINH_ID
                        PW.MISACodeID , --MA_PHAN_CAP
                        PW.ProjectWorkCode , --MA_CONG_TRINH
                        PW.ProjectWorkName , --TEN_CONG_TRINH
                        PW.ProjectWorkCategoryID --LOAI_CONG_TRINH
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ProjectWorkID, ',') tString
                        INNER JOIN dbo.ProjectWork PW ON PW.ProjectWorkID = tString.Value --danh_muc_cong_trinh
                       
        DECLARE @tblSelectedProjectWorkChild TABLE
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
              ProjectWorkCode NVARCHAR(20) ,
              ProjectWorkName NVARCHAR(128)              
            ) 
        INSERT  @tblSelectedProjectWorkChild --TMP_CONG_TRINH_DC_CHON_CHILD
                SELECT  S.ProjectWorkID ,--CONG_TRINH_ID
                        S.MISACodeID, --MA_PHAN_CAP
                         S.ProjectWorkCode , --MA_CONG_TRINH
                        S.ProjectWorkName  -- TEN_CONG_TRINH                       
                FROM    @tblProjectWorkSelected S --TMP_CONG_TRINH_DC_CHON
                        LEFT  JOIN @tblProjectWorkSelected S1 ON S1.MISACodeID LIKE S.MISACodeID --TMP_CONG_TRINH_DC_CHON S1 ON S1."MA_PHAN_CAP" LIKE CONCAT(S."MA_PHAN_CAP",'%%')
                                                              + '%'
                                                              AND S.MISACodeID <> S1.MISACodeID --S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE   S1.MISACodeID IS NULL --S1."MA_PHAN_CAP" IS NULL
					 

		DECLARE @tblListProjectWork TABLE --TMP_CONG_TRINH
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) ,
              ProjectWorkCode NVARCHAR(20) ,
              ProjectWorkName NVARCHAR(128)
            )
        INSERT  INTO @tblListProjectWork --TMP_CONG_TRINH
                SELECT DISTINCT
                        PW.ProjectWorkID , --CONG_TRINH_ID
                        PW.MISACodeID ,--MA_PHAN_CAP
                        PW.ProjectWorkCode , --MA_CONG_TRINH
                        PW.ProjectWorkName --TEN_CONG_TRINH
                FROM    @tblSelectedProjectWorkChild SPW --TMP_CONG_TRINH_DC_CHON_CHILD
                        INNER JOIN dbo.ProjectWork PW ON PW.MisaCodeID LIKE SPW.MISACodeID --danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE (SPW."MA_PHAN_CAP",'%%')	
                                                         + '%'		
			
        DECLARE @tblListAccountObject TABLE -- Bảng chứa danh sách các NCC
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectGroupListCode NVARCHAR(MAX) ,
              AccountObjectGroupListName NVARCHAR(MAX)
            ) 
        INSERT  INTO @tblListAccountObject
                SELECT  AccountObjectID ,--DOI_TUONG_ID
                        AccountObjectGroupListCode , --LIST_MA_NHOM_KH_NCC
                        AccountObjectGroupListName --LIST_TEN_NHOM_KH_NCC
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') tblSupplierSelected
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = tblSupplierSelected.Value --res_partner	 
													   
        SELECT  ROW_NUMBER() OVER ( ORDER BY PL.AccountObjectNameDI, PL.AccountObjectCode, JP.ProjectWorkName, JP.ProjectWorkCode, PL.InventoryItemName, PL.InventoryItemCode ) AS RowNum ,
                PL.AccountObjectID , --DOI_TUONG_ID
                PL.AccountObjectCode , -- Mã NCC --MA_DOI_TUONG
                PL.AccountObjectNameDI AS AccountObjectName, -- Tên NCC	 --	TEN_DOI_TUONG		
                JP.ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                JP.ProjectWorkName , -- Tên công trình--TEN_CONG_TRINH
                PL.InventoryItemID , --MA_HANG_ID
                PL.InventoryItemCode , -- Mã hàng --MA_HANG
                PL.InventoryItemName , -- Tên hàng --TEN_HANG			
                U.UnitName AS MainUnitName , --DON_VI_TINH_CHINH
                SUM(PL.MainQuantity) AS MainQuantity , -- Số lượng mua theo ĐVC --SO_LUONG_MUA
                SUM(PL.PurchaseAmount) AS PurchaseAmount , -- Giá trị mua --GIA_TRI_MUA
                SUM(PL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu --SO_TIEN_CHIET_KHAU
                SUM(PL.ReturnMainQuantity) AS ReturnMainQuantity , -- Số lượng trả lại theo ĐVT chính--SO_LUONG_TRA_LAI    
                SUM(PL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại--GIA_TRI_TRA_LAI
                SUM(PL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá --GIA_TRI_GIAM_GIA
                SUM(PL.MainQuantity - PL.ReturnMainQuantity) AS ToatalPurchaseQuantity ,--Tổng số lượng mua --TONG_SO_LUONG_MUA
                SUM(PL.PurchaseAmount - PL.DiscountAmount - PL.ReturnAmount
                    - PL.ReduceAmount) AS TotalPurchaseAmount , --Tổng giá trị mua  --TONG_GIA_TRI_MUA                                           
                LAO.AccountObjectGroupListCode ,
                LAO.AccountObjectGroupListName
				--LPW.MISACodeID
        FROM    dbo.PurchaseLedger AS PL --so_mua_hang_chi_tiet
                INNER JOIN @tblListBrandID AS TLB ON PL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                 INNER JOIN @tblListProjectWork AS LPW ON PL.ProjectWorkID = LPW.ProjectWorkID --TMP_CONG_TRINH AS LPW ON PL."CONG_TRINH_ID" = LPW."CONG_TRINH_ID"
                --INNER JOIN @tblProjectWorkSelected AS PWS ON LPW.MISACodeID LIKE PWS.MISACodeID
                --                                             + '%'           
                INNER JOIN @tblListAccountObject AS LAO ON PL.AccountObjectID = LAO.AccountObjectID --DS_NHA_CUNG_CAP AS LAO ON PL."DOI_TUONG_ID" = LAO."DOI_TUONG_ID"
                INNER JOIN dbo.InventoryItem AS II ON PL.InventoryItemID = II.InventoryItemID --danh_muc_vat_tu_hang_hoa AS II ON PL."MA_HANG_ID" = II."id"
                LEFT JOIN dbo.Unit AS U ON II.UnitID = U.UnitID --danh_muc_don_vi_tinh AS U ON II."DVT_CHINH_ID" = U."id"
				LEFT JOIN @tblSelectedProjectWorkChild AS JP ON LPW.MISACodeID LIKE JP.MISACodeID --TMP_CONG_TRINH_DC_CHON AS JP ON LPW."MA_PHAN_CAP" LIKE concat(JP."MA_PHAN_CAP",'%%')
                                                             + '%'
        WHERE   PL.PostedDate BETWEEN @FromDate AND @ToDate --PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND PL.IsPostToManagementBook = @IsWorkingWithManagementBook
        GROUP BY PL.AccountObjectID ,--DOI_TUONG_ID
                PL.AccountObjectCode , -- Mã NCC --MA_DOI_TUONG
                PL.AccountObjectNameDI ,  -- Tên NCC      --  TEN_DOI_TUONG                                        	                										               
                JP.ProjectWorkCode , -- Mã công trình--MA_CONG_TRINH
                JP.ProjectWorkName , -- Tên công trình --TEN_CONG_TRINH
                PL.InventoryItemID , --MA_HANG_ID
                PL.InventoryItemCode , -- Mã hàng --MA_HANG
                PL.InventoryItemName , -- Tên hàng --TEN_HANG
                U.UnitName , --DON_VI_TINH
                LAO.AccountObjectGroupListCode , --LIST_MA_NHOM_KH_NCC
                LAO.AccountObjectGroupListName --LIST_TEN_NHOM_KH_NCC
				--LPW.MISACodeID 
		HAVING 	 SUM(PL.MainQuantity) > 0 OR -- Số lượng mua theo ĐVC --SO_LUONG_THEO_DVT_CHINH
                SUM(PL.PurchaseAmount) > 0 OR  -- Giá trị mua--SO_TIEN
                SUM(PL.DiscountAmount) > 0 OR  -- Tiền chiết khấu--SO_TIEN_CHIET_KHAU
                SUM(PL.ReturnMainQuantity) > 0 OR -- Số lượng trả lại theo ĐVT chính     --SO_LUONG_TRA_LAI_THEO_DVT_CHINH
                SUM(PL.ReturnAmount) > 0 OR -- Giá trị trả lại --SO_TIEN_TRA_LAI
                SUM(PL.ReduceAmount) > 0 OR -- Giá trị giảm --SO_TIEN_GIAM_TRU
                SUM(PL.MainQuantity - PL.ReturnMainQuantity) > 0 OR--Tổng số lượng mua --(PL."SO_LUONG_THEO_DVT_CHINH" - PL."SO_LUONG_TRA_LAI_THEO_DVT_CHINH")
                SUM(PL.PurchaseAmount - PL.DiscountAmount - PL.ReturnAmount --PL."SO_TIEN" - PL."SO_TIEN_CHIET_KHAU" - PL."SO_TIEN_TRA_LAI"
                    - PL.ReduceAmount) > 0  --Tổng giá trị mua --PL."SO_TIEN_GIAM_TRU"							
    END

GO