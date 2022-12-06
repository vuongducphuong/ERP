SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		nmtruong
-- Create date: 5/10/2015
-- Description:	Báo cáo Tổng hợp bán hàng theo nhóm khách hàng
-- [Proc_SAR_GetSASaleSummaryByAOGroup] '1/1/2015','9/30/2015',NULL, 1, NULL,',0091378C-F09D-47E9-B326-151EC3712BEF,',NULL,0
-- select * from AccountObject where accountobjectCode = '!! Anh Anh'
-- BTAnh - 12.8.2016: Bổ sung OPTION(RECOMPILE) 
-- BTAnh - 08.09.2016: Tối ưu báo cáo bằng cách tạo ra bảng tạm #AccountObject để join với các bảng ledger
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?      
 DECLARE   @ListAccountObjectGroupID NVARCHAR(MAX) 
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


		SET		@FromDate = '2018-01-01 00:00:00'
        SET                                @ToDate = '2018-12-31 23:59:59'
        SET                                @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET                                @IncludeDependentBranch = 1
        SET                                @ListAccountObjectGroupID = N',12345678-2222-48b8-ae4b-5cf7fa7fb3f5,1595e9dc-6d52-4be8-bf56-e990a80b3665,463aa8db-1da0-423f-8153-d8651c33c95a,76c10d2d-bcc8-4cbb-a043-0f92d08b8d29,952b5c06-49f2-4fae-9b2c-dc9b65c8c2f2,c0e7ce4a-5025-414c-9a20-cb34793c5111,c6183f36-2359-4386-b0d8-0b799c9f5b0f,c86d8f19-28a5-45c3-a8a0-f5c6fb8031dd,'
        SET                                @IsWorkingWithManagementBook = 0


    BEGIN
        DECLARE @tblListBrandID TABLE
            (
              BranchID UNIQUEIDENTIFIER
            )	
   
        INSERT  INTO @tblListBrandID --TMP_LIST_BRAND
                SELECT  FGDBBI.BranchID
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI
    
        DECLARE @tblAccountObjectGroupID TABLE-- Bảng khoản mục CP được chọn trên form tham số
            (
              AccountObjectGroupID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS
                                       NULL ,
              AccountObjectGroupCode NVARCHAR(20)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL ,
              AccountObjectGroupName NVARCHAR(128)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL ,
              SortMISACodeID NVARCHAR(100)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL
            ) 
        INSERT  INTO @tblAccountObjectGroupID
                SELECT DISTINCT
                        EI.AccountObjectGroupID ,--NHOM_KH_NCC_ID
                        EI.MISACodeID , --MA_PHAN_CAP
                        EI.AccountObjectGroupCode , --MA
                        EI.AccountObjectGroupName , --TEN
                        EI.SortMISACodeID
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ListAccountObjectGroupID,
                                                           ',') tString
                        INNER JOIN dbo.AccountObjectGroup EI ON EI.AccountObjectGroupID = tString.Value --danh_muc_nhom_khach_hang_nha_cung_cap
                    
        DECLARE @tblAccountObjectGroupID1 TABLE-- Bảng khoản mục CP khong có node không chọn
            (
              AccountObjectGroupID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS
                                       NULL
            ) 
        INSERT  @tblAccountObjectGroupID1 --TMP_NHOM_KH_NCC_1
                SELECT  S.AccountObjectGroupID , -- NHOM_KH_NCC_ID
                        S.MISACodeID --MA_PHAN_CAP
                FROM    @tblAccountObjectGroupID S --TMP_NHOM_KH_NCC
                        LEFT  JOIN @tblAccountObjectGroupID S1 ON S1.MISACodeID LIKE S.MISACodeID --TMP_NHOM_KH_NCC S1 ON S1."MA_PHAN_CAP" LIKE concat(S."MA_PHAN_CAP", '%%') AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                                                              + '%'
                                                              AND S.MISACodeID <> S1.MISACodeID --S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE   S1.MISACodeID IS NULL  --S1."MA_PHAN_CAP" IS NULL
   
        DECLARE @tblListAccountObjectGroupID TABLE-- Bảng khoản mục CP gồm toàn bộ khoản mục CP con
            (
              AccountObjectGroupID UNIQUEIDENTIFIER ,
              MISACodeID NVARCHAR(100)
            )                     
    -- Trường hợp tích chọn KMCP khác
        DECLARE @gOtherID AS NVARCHAR(100)
        SET @gOtherID = '12345678-2222-48B8-AE4B-5CF7FA7FB3F5'
	
        DECLARE @OtherMisacodeID AS NVARCHAR(100) 
        SET @OtherMisacodeID = '/9999999/'
        DECLARE @IsIncludeOtherID BIT
        IF @ListAccountObjectGroupID LIKE '%' + @gOtherID + '%' --nhom_kh_khac_id IN (15, 16, 17, 18, 19, 20, 21, -2)
            BEGIN
                SET @IsIncludeOtherID = 1 --IsIncludeOtherID
                INSERT  INTO @tblAccountObjectGroupID --TMP_NHOM_KH_NCC
                        SELECT  @gOtherID , --nhom_kh_khac_id
                                @OtherMisacodeID , --MA_PHAN_CAP_KHAC
                                N'<<Khác>>' ,
                                N'<<Khác>>' ,
                                @OtherMisacodeID
            END
        ELSE 
            SET @IsIncludeOtherID = 0	--IsIncludeOtherID
		
		   
        INSERT  INTO @tblListAccountObjectGroupID --TMP_LIST_NHOM_KH_NCC
                SELECT DISTINCT
                        T.AccountObjectGroupID , --id
                        T.MISACodeID --MA_PHAN_CAP
                FROM    ( SELECT  DISTINCT
                                    EI.AccountObjectGroupID , --id
                                    EI.MISACodeID --MA_PHAN_CAP
                          FROM      dbo.AccountObjectGroup EI --danh_muc_nhom_khach_hang_nha_cung_cap
                                    INNER JOIN @tblAccountObjectGroupID1 SEI ON EI.MISACodeID LIKE SEI.MISACodeID --TMP_NHOM_KH_NCC_1 SEI ON EI."MA_PHAN_CAP" LIKE concat(SEI."MA_PHAN_CAP" ,'%%')
                                                              + '%'
                          UNION ALL
                          SELECT    EI.AccountObjectGroupID , --NHOM_KH_NCC_ID
                                    EI.MISACodeID --MA_PHAN_CAP
                          FROM      @tblAccountObjectGroupID EI --TMP_NHOM_KH_NCC
                        ) T
    ----        
    
        DECLARE @tblGradeAccountObjectGroupID TABLE-- Tính bậc để lùi dòng cho báo cáo hình cây
            (
              AccountObjectGroupID UNIQUEIDENTIFIER PRIMARY KEY ,
              Grade INT
            )        
        INSERT  INTO @tblGradeAccountObjectGroupID --TMP_BAC_NHOM_KH_NCC
                SELECT  P.AccountObjectGroupID , --NHOM_KH_NCC_ID
                        COUNT(PD.MISACodeID) Grade --MA_PHAN_CAP
                FROM    @tblAccountObjectGroupID P --TMP_NHOM_KH_NCC
                        LEFT JOIN @tblAccountObjectGroupID PD ON P.MISACodeID LIKE PD.MISACodeID --P."MA_PHAN_CAP" LIKE concat(PD."MA_PHAN_CAP" , '%%')
                                                              + '%'
                                                              AND P.MISACodeID <> PD.MISACodeID --P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                GROUP BY P.AccountObjectGroupID  --P."NHOM_KH_NCC_ID"                                           
    
    -- Bảng các khoản mục CP cha được chọn trong đó có chọn cả con mà là cha	
        DECLARE @tblParentAccountObjectGroupID TABLE
            (
              AccountObjectGroupID UNIQUEIDENTIFIER PRIMARY KEY
            )
    
        INSERT  INTO @tblParentAccountObjectGroupID --TMP_PARENT_NHOM_KH_NCC
                SELECT DISTINCT
                        PD.AccountObjectGroupID --NHOM_KH_NCC_ID
                FROM    @tblAccountObjectGroupID P --TMP_NHOM_KH_NCC
                        LEFT JOIN @tblAccountObjectGroupID PD ON P.MISACodeID LIKE PD.MISACodeID --TMP_NHOM_KH_NCC PD ON P."MA_PHAN_CAP" LIKE concat(PD."MA_PHAN_CAP" ,'%%')
                                                              + '%'
                                                              AND P.MISACodeID <> PD.MISACodeID --P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                WHERE   PD.MISACodeID IS NOT NULL --MA_PHAN_CAP
        
        --BTAnh - 8.9.2016: Dùng bảng này để join với các bảng ledger để không phải join vào bảng gốc --> tăng performance
        --Danh sách khách hàng 
        CREATE TABLE #AccountObject (
										AccountObjectID UNIQUEIDENTIFIER,
										MISACodeID NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
									)
		----Danh sách khách hàng thuộc nhóm đã chọn - KHÔNG PHẢI NHÓM "KHÁC"									
		INSERT INTO #AccountObject      --DS_KH_NCC
		        (AccountObjectID, MISACodeID)
		SELECT AccountObjectID,
			AOG.MISACodeID
		FROM dbo.AccountObject AS AO --res_partner
			JOIN @tblListAccountObjectGroupID AOG ON AO.AccountObjectGroupList LIKE '%;' + AOG.MISACodeID + ';%' --TMP_LIST_NHOM_KH_NCC AOG ON AO."LIST_MPC_NHOM_KH_NCC" LIKE  concat('%%;',AOG."MA_PHAN_CAP",';%%')							
		WHERE AO.AccountObjectGroupList IS NOT NULL --LIST_MPC_NHOM_KH_NCC
				AND AO.AccountObjectGroupList <> ''  --
				AND AO.IsCustomer = 1 --LA_KHACH_HANG
		
		---Nếu có chọn nhóm "KHÁC" thì insert các khách hàng thuộc nhóm KHÁC vào
		IF 	@IsIncludeOtherID = 1
			INSERT INTO #AccountObject
			        ( AccountObjectID, MISACodeID)
			SELECT AccountObjectID,
				@OtherMisacodeID
			FROM dbo.AccountObject AS AO
			WHERE (AO.AccountObjectGroupList IS NULL
					OR AO.AccountObjectGroupList = ''
				)
				AND AO.IsCustomer = 1
												
        ------------------------------------
        --Bảng chứa kết quả
        CREATE TABLE #Balance ( --TMP_KET_QUA
								MisaCodeID NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
								SaleAmount DECIMAL(18,4),
								DiscountAmount DECIMAL(18,4),
								ReturnAmount DECIMAL(18,4),
								ReduceAmount DECIMAL(18,4),
								CostAmount DECIMAL(18,4)
							)
        
        INSERT INTO #Balance
		        ( MisaCodeID ,
		          SaleAmount ,
		          DiscountAmount ,
		          ReturnAmount ,
		          ReduceAmount ,
		          CostAmount
		        )		        
		SELECT    AO.MISACodeID AS MisaCodeID , --MA_PHAN_CAP
				SUM(SL.SaleAmount) AS SaleAmount,  -- Doanh số bán --DOANH_SO_BAN
				SUM(SL.DiscountAmount) AS DiscountAmount,  -- Tiền chiết khấu   --SO_TIEN_CHIET_KHAU
				SUM(SL.ReturnAmount) AS ReturnAmount,  -- Giá trị trả lại --GIA_TRI_TRA_LAI
				SUM(SL.ReduceAmount) AS ReduceAmount,  -- Giá trị giảm giá --GIA_TRI_GIAM_GIA
				0 AS CostAmount --GIA_VON
		FROM      dbo.SaleLedger AS SL --so_ban_hang_chi_tiet
				INNER JOIN @tblListBrandID AS TLB ON SL.BranchID = TLB.BranchID--TMP_LIST_BRAND AS TLB ON SL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
				INNER JOIN #AccountObject AO ON AO.AccountObjectID = SL.AccountObjectID --DS_KH_NCC AO ON AO.id = SL."DOI_TUONG_ID"
		WHERE     SL.PostedDate BETWEEN @FromDate AND @ToDate --SL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook 
		GROUP BY  AO.MISACodeID --MA_PHAN_CAP
		HAVING    SUM(SL.SaleAmount) <> 0 -- Doanh số bán --SO_TIEN
				OR SUM(SL.DiscountAmount) <> 0-- Tiền chiết khấu   --SO_TIEN_CHIET_KHAU
				OR SUM(SL.ReturnAmount) <> 0 -- Giá trị trả lại --SO_TIEN_TRA_LAI
				OR SUM(SL.ReduceAmount) <> 0 -- Giá trị giảm giá --SO_TIEN_GIAM_TRU

		-- Lấy giá vốn  
		UNION ALL
		SELECT  AO.MISACodeID AS MisaCodeID ,
				0 ,
				0 ,
				0 ,
				0 ,
				SUM(OutwardAmount - InwardAmount) AS CostAmount --SUM("SO_TIEN_XUAT" - "SO_TIEN_NHAP") AS "GIA_VON"
		FROM      dbo.InventoryLedger IL --so_kho_chi_tiet
				INNER JOIN @tblListBrandID AS TLB ON IL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON IL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
				INNER JOIN #AccountObject AO ON AO.AccountObjectID = IL.AccountObjectID --DS_KH_NCC AO ON AO.id = IL."DOI_TUONG_ID"
		WHERE     IL.PostedDate BETWEEN @FromDate AND @ToDate --IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
				AND IL.CorrespondingAccountNumber LIKE '632%' --- cứ phát sinh 632 là lấy  -- MA_TK_CO                                             
				AND ( IL.RefType = 2020 --LOAI_CHUNG_TU
					  OR IL.RefType = 2013 --LOAI_CHUNG_TU
					)
		GROUP BY  AO.MISACodeID --MA_PHAN_CAP
	
                            
		---------------------------------------------------------                            
                
        SELECT  ROW_NUMBER() OVER ( ORDER BY P.SortMISACodeID ) AS RowNum ,
                P.AccountObjectGroupID , -- NHOM_KH_NCC_ID
                SPACE(GP.Grade * 6) + P.AccountObjectGroupCode AS AccountObjectGroupCode , --,concat(repeat(' ',cast(GP.Grade * 6 as int)),P."MA")--
                SPACE(GP.Grade * 6) + P.AccountObjectGroupName AS AccountObjectGroupName ,--concat(repeat(' ',cast(GP.Grade * 6 as int)),P."TEN")
                CAST(CASE WHEN GP.Grade = 0 THEN 1
                          ELSE 0
                     END AS BIT) AS IsSummaryRow ,
                CAST(CASE WHEN PP.AccountObjectGroupID IS NULL THEN 0
                          ELSE 1
                     END AS BIT) AS IsBold ,
                SUM(T.SaleAmount) AS SaleAmount , --DOANH_SO_BAN
                SUM(T.DiscountAmount) AS DiscountAmount , --SO_TIEN_CHIET_KHAU
                SUM(T.ReturnAmount) AS ReturnAmount , --GIA_TRI_TRA_LAI
                SUM(T.ReduceAmount) AS ReduceAmount , --GIA_TRI_GIAM_GIA
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) AS NetSaleAmount , --DOANH_THU_THUAN
                SUM(T.CostAmount) AS CostAmount , --GIA_VON
                SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) AS GrossProfitAmount , --LAI_GOP
                ( CASE WHEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) > 0 AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) >0 
							OR SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount) <0 AND SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) < 0 
                       THEN SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount - T.CostAmount) * 100 
                       / SUM(T.SaleAmount - T.DiscountAmount - T.ReturnAmount - T.ReduceAmount)
                       ELSE 0
                  END ) AS GrossProfitRate --TY_LE_LAI_GOP
        FROM    #Balance AS T --TMP_KET_QUA
                INNER JOIN @tblAccountObjectGroupID P ON T.MISACodeID LIKE P.MISACodeID + '%' --TMP_NHOM_KH_NCC P ON T."MA_PHAN_CAP" LIKE concat(P."MA_PHAN_CAP", '%%')
                LEFT JOIN @tblParentAccountObjectGroupID PP ON PP.AccountObjectGroupID = P.AccountObjectGroupID --TMP_PARENT_NHOM_KH_NCC PP ON PP."NHOM_KH_NCC_ID" = P."NHOM_KH_NCC_ID"
                LEFT JOIN @tblGradeAccountObjectGroupID GP ON GP.AccountObjectGroupID = P.AccountObjectGroupID -- TMP_BAC_NHOM_KH_NCC GP ON GP."NHOM_KH_NCC_ID" = P."NHOM_KH_NCC_ID"
        GROUP BY P.SortMISACodeID ,
                P.AccountObjectGroupID , --NHOM_KH_NCC_ID
                SPACE(GP.Grade * 6) + P.AccountObjectGroupCode ,--concat(repeat(' ',cast(GP.Grade * 6 as int)),P."MA"),
                SPACE(GP.Grade * 6) + P.AccountObjectGroupName , --concat(repeat(' ',cast(GP.Grade * 6 as int)),P."TEN")
                CAST(CASE WHEN GP.Grade = 0 THEN 1
                          ELSE 0
                     END AS BIT) ,
                CAST(CASE WHEN PP.AccountObjectGroupID IS NULL THEN 0
                          ELSE 1
                     END AS BIT)
        HAVING  SUM(T.SaleAmount) <> 0 --DOANH_SO_BAN
                OR SUM(T.DiscountAmount) <> 0 --SO_TIEN_CHIET_KHAU
                OR SUM(T.ReturnAmount) <> 0 --GIA_TRI_TRA_LAI
                OR SUM(T.ReduceAmount) <> 0 --GIA_TRI_GIAM_GIA
                OR SUM(T.CostAmount)<>0 --GIA_VON
        OPTION(RECOMPILE) 
    END


GO