SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		NTGIANG
-- Create date: 15.10.2014
-- Description:	<Mua hàng: Lấy số liệu tổng hợp mua hàng theo nhà cung cấp>
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER  -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @AccountObjectID NVARCHAR(MAX)  -- Danh sách nhà cung cấp, VD: ",6c9abe42-fbaf-4157-8b2a-10a031cd48dc, 201770d3-8664-4c98-ab0f-fed9af5a89b1,"     
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?
			

		SET	@FromDate = '2018-01-01 00:00:00'
        SET                                     @ToDate = '2018-12-31 23:59:59'
        SET                                     @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET                                     @IncludeDependentBranch = 1
        SET                                     @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
        SET                                     @IsWorkingWithManagementBook = 0
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
		                          
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các NCC 
            (
              AccountObjectID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  *
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',')
                                                           
        SELECT  ROW_NUMBER() OVER ( ORDER BY PL.AccountObjectCode , PL.AccountObjectNameDI ) AS RowNum ,
                PL.AccountObjectID ,--DOI_TUONG_ID
                PL.AccountObjectCode , -- Mã NCC --MA_DOI_TUONG
                PL.AccountObjectNameDI , -- Tên NCC --TEN_DOI_TUONG
                SUM(PL.PurchaseAmount) AS PurchaseAmount , -- Giá trị mua--GIA_TRI_MUA
                SUM(PL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu  --  
                SUM(PL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại--GIA_TRI_TRA_LAI
                SUM(PL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá  --GIA_TRI_GIAM_GIA
                SUM(PL.PurchaseAmount - PL.DiscountAmount - PL.ReturnAmount
                    - PL.ReduceAmount) AS TotalPurchaseAmount , --Tổng giá trị mua       --TONG_GIA_TRI_MUA                                
                AO.AccountObjectGroupListCode , -- Mã nhóm NCC                       
                [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC	
        FROM    dbo.PurchaseLedger AS PL --so_mua_hang_chi_tiet
                INNER JOIN @tblListBrandID AS TLB ON PL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                INNER JOIN @tblListAccountObjectID AS LAO ON PL.AccountObjectID = LAO.AccountObjectID --DS_NHA_CUNG_CAP  AS LAO ON PL."DOI_TUONG_ID" = LAO.id
                INNER JOIN dbo.AccountObject AO ON LAO.AccountObjectID = AO.AccountObjectID
        WHERE   PL.PostedDate BETWEEN @FromDate AND @ToDate --PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND PL.IsPostToManagementBook = @IsWorkingWithManagementBook
        GROUP BY PL.AccountObjectID ,--DOI_TUONG_ID
                PL.AccountObjectCode ,--MA_DOI_TUONG
                PL.AccountObjectNameDI ,--TEN_DOI_TUONG
                AO.AccountObjectGroupListCode , -- Mã nhóm NCC                       
                [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode)-- tên nhóm NCC	 
        --ORDER BY PL.AccountObjectCode , 
        --        PL.AccountObjectNameDI 
    END
    


GO