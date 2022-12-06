SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO


-- =============================================
-- Author:		NVTOAN
-- Create date: 24/11/2014
-- Description:	<Bán hàng: Lấy số liệu tổng hợp bán hàng theo khách hàng>
-- nmtruong 22/10/2015: sửa bug 73674: sửa join thành union để lấy lên số giá vốn
-- lvdiep 1806/2016 : Bổ sung tham số @IsGetAllCustomer để cho phép NSD tùy chọn in cả khách hàng không phát sinh số liệu doanh thu hoặc không
-- BTAnh - 12.8.2016: Bổ sung OPTION(RECOMPILE) 
/*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
-- =============================================

		DECLARE			@FromDate DATETIME 
		DECLARE			@ToDate DATETIME 
		DECLARE			@BranchID UNIQUEIDENTIFIER  -- Chi nhánh
		DECLARE			@IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
		DECLARE			@OrganizationUnitID UNIQUEIDENTIFIER = NULL 
		DECLARE			@EmployeeID UNIQUEIDENTIFIER = NULL  -- Danh sách nhân viên
		DECLARE			@ListCustomerID NVARCHAR(MAX)  -- Danh sách nhà cung cấp,
		DECLARE			@IsWorkingWithManagementBook BIT --  Có dùng sổ quản trị hay không?
		DECLARE			@IsGetAllCustomer BIT -- có in tất cả khách hàng hay không?


			SET								@FromDate = '2016-01-01 00:00:00'
            SET                            @ToDate = '2016-12-31 23:59:59'
            SET                            @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
            SET                            @IncludeDependentBranch = 1
            SET                            @OrganizationUnitID = NULL
            SET                            @EmployeeID = NULL
            SET                            @ListCustomerID = N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,8b0ba43a-1120-4574-905d-e2abff045f13,'
            SET                            @IsWorkingWithManagementBook = 0
            SET                            @IsGetAllCustomer = 1

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

       -- nmtruong:22/10/2015 lấy lên các thông tin cần thiết để đỡ phải join khi lấy dữ liệu
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(25) ,
              AccountObjectName NVARCHAR(255) ,
              AccountObjectAddress NVARCHAR(255) ,
              CompanyTaxCode NVARCHAR(50) ,
              /*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
              Tel NVARCHAR(50) ,
              Mobile NVARCHAR(50) ,
			  Fax NVARCHAR(50) ,
			  EmailAddress NVARCHAR(100) ,
			  ContactName NVARCHAR(128) ,
			  ContactTitle NVARCHAR(128) ,
			  ContactMobile NVARCHAR(50) ,
			  ContactEmail NVARCHAR(100) ,
              AccountObjectGroupListCode NVARCHAR(MAX) ,
              AccountObjectGroupListName NVARCHAR(MAX) ,
              ProvinceOrCity NVARCHAR(100) ,
              District NVARCHAR(100) ,
              WardOrCommune NVARCHAR(100)
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  Value ,
                        AccountObjectCode , --MA_KHACH_HANG
                        AccountObjectName , --HO_VA_TEN
                        [Address] ,--DIA_CHI
                        CompanyTaxCode ,--MA_SO_THUE
                        /*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
						AOD.Tel ,	--DIEN_THOAI
						CASE WHEN AOD.AccountObjectType = 1 --LOAI_KHACH_HANG
								THEN AOD.Mobile --DT_DI_DONG
							WHEN AOD.AccountObjectType = 0  --LOAI_KHACH_HANG
								THEN NULL END  AS Mobile ,	--DT_DI_DONG
						CASE WHEN AOD.AccountObjectType = 1 --LOAI_KHACH_HANG
								THEN NULL  
							WHEN AOD.AccountObjectType = 0 --LOAI_KHACH_HANG
								THEN AOD.Fax END AS Fax , --FAX
						AOD.EmailAddress ,--EMAIL
						CASE WHEN AOD.AccountObjectType = 1 --LOAI_KHACH_HANG
								THEN NULL
							WHEN AOD.AccountObjectType = 0  --LOAI_KHACH_HANG
								THEN AOD.ContactName END AS ContactName ,--HO_VA_TEN_LIEN_HE
						CASE WHEN AOD.AccountObjectType = 1 --LOAI_KHACH_HANG
								THEN NULL  
							WHEN AOD.AccountObjectType = 0 
								THEN AOD.ContactTitle END AS ContactTitle ,--CHUC_DANH
						CASE WHEN AOD.AccountObjectType = 1 --LOAI_KHACH_HANG
								THEN NULL  
							WHEN AOD.AccountObjectType = 0 
								THEN AOD.ContactMobile END AS ContactMobile ,--DT_DI_DONG_LIEN_HE
						CASE WHEN AOD.AccountObjectType = 1 --LOAI_KHACH_HANG
								THEN NULL  
							WHEN AOD.AccountObjectType = 0 
								THEN AOD.ContactEmail END AS ContactEmail , --EMAIL_LIEN_HE
                        AccountObjectGroupListCode ,
                        AccountObjectGroupListName ,
                        AOD.ProvinceOrCity , --TINH_TP_ID
                        AOD.District , --QUAN_HUYEN_ID
                        AOD.WardOrCommune --XA_PHUONG_ID
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ListCustomerID,
                                                           ',') AS F
                        INNER JOIN dbo.AccountObject AOD ON AOD.AccountObjectID = F.Value
                                                           
         -- nmtruong: 22/10/2015 Khai báo misacode id để like cho nhanh                                   
        DECLARE @MisaCodeID AS NVARCHAR(100)
        SET @MisaCodeID = ( SELECT  MisaCodeID + '%'
                            FROM    dbo.OrganizationUnit
                            WHERE   OrganizationUnitID = @OrganizationUnitID
                          )               
        
		DROP TABLE #SalesSummaryByCustomer
        SELECT  ROW_NUMBER() OVER ( ORDER BY AO.AccountObjectCode, AO.AccountObjectName ) AS RowNum ,
                AO.AccountObjectID , --id
                AO.AccountObjectCode , --MA_KHACH_HANG
                AO.AccountObjectName , --HO_VA_TEN
                AO.AccountObjectAddress ,
                AO.CompanyTaxCode ,
                /*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
                AO.Tel  ,              
				AO.Mobile ,
				AO.Fax ,
				AO.EmailAddress ,
				AO.ContactName  ,
				AO.ContactTitle  ,
				AO.ContactMobile  ,
				AO.ContactEmail , 
                AO.AccountObjectGroupListCode ,
                AO.AccountObjectGroupListName ,
                AO.ProvinceOrCity ,--TINH_TP_ID
                AO.District , --QUAN_HUYEN_ID
                AO.WardOrCommune , --XA_PHUONG_ID
                SUM(T.SaleAmount) AS SaleAmount ,--DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount ,---SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount
                    - T.ReduceAmount) AS NetSaleAmount , --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , ---GIA_VON
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
        INTO    #SalesSummaryByCustomer
        FROM    ( SELECT    SL.AccountObjectID , --DOI_TUONG_ID
                            SUM(SL.SaleAmount) AS SaleAmount , -- Doanh số bán --DOANH_SO_BAN
                            SUM(SL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu    --SO_TIEN_CHIET_KHAU
                            SUM(SL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                            SUM(SL.ReduceAmount) AS ReduceAmount  -- Giá trị giảm giá  --GIA_TRI_GIAM_GIA
                            ,
                            0 AS CostAmount--GIA_VON
                  FROM      dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
                            INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN @tblListAccountObjectID AOL ON AOL.AccountObjectID = SL.AccountObjectID --DS_KHACH_HANG AOL ON AOL."DOI_TUONG_ID" = SL."DOI_TUONG_ID"
                            LEFT JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = SL.OrganizationUnitID --danh_muc_to_chuc OU ON OU."id" = SL."DON_VI_ID"
                  WHERE     SL.PostedDate BETWEEN @FromDate AND @ToDate --SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND ( SL.EmployeeID = @EmployeeID --SL."NHAN_VIEN_ID" = nhan_vien_id
                                  OR @EmployeeID IS NULL --nhan_vien_id = -1
                                )
                            AND ( @OrganizationUnitID IS NULL --don_vi_id = -1
                                  OR OU.MISACodeID LIKE @MisaCodeID --OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP
                                )
                  GROUP BY  SL.AccountObjectID --DOI_TUONG_ID
                  UNION ALL
                  SELECT    IL.AccountObjectID ,
                            0 ,
                            0 ,
                            0 ,
                            0 ,
                            SUM(OutwardAmount - InwardAmount) AS CostAmount --SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
                  FROM      dbo.InventoryLedger IL --so_kho_chi_tiet
                            INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                            INNER JOIN @tblListAccountObjectID AS LAO ON IL.AccountObjectID = LAO.AccountObjectID--INNER JOIN DS_KHACH_HANG AS LAO ON IL."DOI_TUONG_ID" = LAO."DOI_TUONG_ID"
                            LEFT JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = IL.OrganizationUnitID-- LEFT JOIN danh_muc_to_chuc OU ON OU."id" = IL."DON_VI_ID"
                  WHERE     IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy   --MA_TK_CO                        
                            AND ( @EmployeeID IS NULL --nhan_vien_id = -1
                                  OR IL.EmployeeID = @EmployeeID --IL."NHAN_VIEN_ID" = nhan_vien_id
                                )
                            AND ( @OrganizationUnitID IS NULL --don_vi_id = -1
                                  OR OU.MISACodeID LIKE @MisaCodeID --OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP
                                )
                            AND ( IL.RefType = 2020 --IL."LOAI_CHUNG_TU" = 2020
                                  OR IL.RefType = 2013 --IL."LOAI_CHUNG_TU" = 2013
                                ) --HHSon edited 21.05.2015: Fix bug JIRA SMEFIVE-2948 - Chỉ lấy từ xuất kho bán hàng và nhập kho hàng bán trả lại thôi
                  GROUP BY  IL.AccountObjectID --DOI_TUONG_ID
                ) T
                INNER JOIN @tblListAccountObjectID AO ON AO.AccountObjectID = T.AccountObjectID --DS_KHACH_HANG AO ON AO."DOI_TUONG_ID" = T."DOI_TUONG_ID"
        GROUP BY AO.AccountObjectID ,--DOI_TUONG_ID
                AO.AccountObjectCode ,--MA_KHACH_HANG
                AO.AccountObjectName , --HO_VA_TEN
                AO.AccountObjectAddress ,
                AO.CompanyTaxCode ,
                /*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
                AO.Tel  ,
				AO.Mobile ,
				AO.Fax ,
				AO.EmailAddress ,
				AO.ContactName  ,
				AO.ContactTitle  ,
				AO.ContactMobile  ,
				AO.ContactEmail ,
                AO.AccountObjectGroupListCode ,
                AO.AccountObjectGroupListName ,
                AO.ProvinceOrCity ,--TINH_TP_ID
                AO.District ,--QUAN_HUYEN_ID
                AO.WardOrCommune --XA_PHUONG_ID
            /*Edited by ntlieu 13/01/2016: Sửa bug 86379 - Lấy số liệu khi có bất kỳ phát sinh nào <> 0*/
        HAVING  SUM(T.SaleAmount) <> 0 --DOANH_SO_BAN
                OR SUM(T.DiscountAmount) <> 0 --SO_TIEN_CHIET_KHAU
                OR SUM(T.ReturnAmount) <> 0--GIA_TRI_TRA_LAI
                OR SUM(T.ReduceAmount) <> 0 --GIA_TRI_GIAM_GIA
                OR SUM(T.CostAmount) <> 0 --GIA_VON
        OPTION(RECOMPILE)
   --         SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) <>0 
			--OR   SUM(T.CostAmount) <>0
        
        /*Phân tách trường hợp NSD tích chọn cho phép in hiển thị cả khách hàng không phát sinh số liệu trong kỳ lên báo cáo*/
        IF @IsGetAllCustomer = 1 --chi_lay_khach_hang_co_phat_sinh
            SELECT  T.RowNum , --SO_DONG
                    T.AccountObjectID ,--DOI_TUONG_ID
                    T.AccountObjectCode , --MA_KHACH_HANG
                    T.AccountObjectName ,--HO_VA_TEN
                    T.AccountObjectAddress , 
                    T.CompanyTaxCode ,
                    /*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
                    T.Tel  ,
					T.Mobile ,
					T.Fax ,
					T.EmailAddress ,
					T.ContactName  ,
					T.ContactTitle  ,
					T.ContactMobile  ,
					T.ContactEmail ,
                    T.AccountObjectGroupListCode ,
                    T.AccountObjectGroupListName ,
                    T.ProvinceOrCity ,--TINH_TP_ID
                    T.District ,--QUAN_HUYEN_ID
                    T.WardOrCommune , --XA_PHUONG_ID
                    T.SaleAmount , --DOANH_SO_BAN
                    T.DiscountAmount ,--SO_TIEN_CHIET_KHAU
                    T.ReturnAmount ,--GIA_TRI_TRA_LAI
                    T.ReduceAmount , --GIA_TRI_GIAM_GIA
                    T.NetSaleAmount ,--DOANH_THU_THUAN
                    T.CostAmount , --GIA_VON
                    T.GrossProfitAmount ,
                    T.GrossProfitRate
            FROM    #SalesSummaryByCustomer T --
        ELSE
        SELECT  ROW_NUMBER() OVER ( ORDER BY AO.AccountObjectCode, AO.AccountObjectName ) AS RowNum , --SO_DONG
                    AO.AccountObjectID ,--DOI_TUONG_ID
                    AO.AccountObjectCode ,--MA_KHACH_HANG
                    AO.AccountObjectName , --HO_VA_TEN
                    AO.AccountObjectAddress ,
                    AO.CompanyTaxCode ,
                    /*DDKhanh 12/05/2017 CR100838 Thêm 8 trường vào mẫu báo cáo*/
                    AO.Tel  ,
					AO.Mobile ,
					AO.Fax ,
					AO.EmailAddress ,
					AO.ContactName  ,
					AO.ContactTitle  ,
					AO.ContactMobile  ,
					AO.ContactEmail ,
                    AO.AccountObjectGroupListCode ,
                    AO.AccountObjectGroupListName ,
                    AO.ProvinceOrCity ,--TINH_TP_ID
                    AO.District ,--QUAN_HUYEN_ID
                    AO.WardOrCommune , --XA_PHUONG_ID
                    T.SaleAmount ,
                    T.DiscountAmount ,
                    T.ReturnAmount ,
                    T.ReduceAmount ,
                    T.NetSaleAmount ,
                    T.CostAmount ,
                    T.GrossProfitAmount ,
                    T.GrossProfitRate
            FROM    @tblListAccountObjectID AO--DS_KHACH_HANG
                    LEFT JOIN #SalesSummaryByCustomer T ON T.AccountObjectID = AO.AccountObjectID--TMP_KET_QUA T ON T."DOI_TUONG_ID" = AO."DOI_TUONG_ID"
            OPTION(RECOMPILE)
            
    END
    



GO