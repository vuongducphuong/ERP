SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- Lấy dữ liệu cho báo cáo Sổ tài sản cố định (Mẫu chế độ)
-- Created by: nmtruong 11/11/2014
-- tthoa thầu và sửa 
/*hoant 01.08.2017 sửa lỗi 127116- Sổ tài sản (mẫu chế độ): Không lên được tài khoản cố định đầu kỳ khi xem kỳ báo cáo chứa ngày ghi giảm*/

DECLARE    @BranchID UNIQUEIDENTIFIER 
DECLARE    @IncludeDependentBranch BIT 
DECLARE    @FromDate DATETIME 
DECLARE    @ToDate DATETIME 
DECLARE    @OrganizationUnitID UNIQUEIDENTIFIER 
DECLARE    @FixedAssetCategoryID UNIQUEIDENTIFIER 
DECLARE    @IsWorkingWithManagementBook BIT

SET						@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B' -- chi_nhanh
SET                                  @IncludeDependentBranch = 1   --BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC
SET                                  @FromDate = '2018-01-01 00:00:00' --TU_NGAY
SET                                  @ToDate = '2018-12-31 23:59:59'  --DEN_NGAY
SET                                  @OrganizationUnitID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B' --dv_sd
SET                                  @FixedAssetCategoryID = '8E8190B8-CB6B-4D25-BD61-1C124577FB42' --loai_tscd
SET                                  @IsWorkingWithManagementBook = 0





    BEGIN    
        DECLARE @tblBranch TABLE
            (
              BranchID UNIQUEIDENTIFIER PRIMARY KEY ,
              BranchCode NVARCHAR(25) ,
              BranchName NVARCHAR(128)
            )                       
        INSERT  INTO @tblBranch
                SELECT  BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.[Func_GetDependentByBranchID](@BranchID,
                                                          @IncludeDependentBranch)   
		---map từ đây--- 
        
        -- Misa code của đơn vị sử dụng        
        DECLARE @OUMisacodeID NVARCHAR(100)
        IF @OrganizationUnitID IS NOT NULL 
            SET @OUMisacodeID = ( SELECT TOP 1
                                            MisacodeID + '%' --MA_PHAN_CAP
                                  FROM      dbo.OrganizationUnit --danh_muc_to_chuc
                                  WHERE     OrganizationUnitID = @OrganizationUnitID --id = dv_sd
                                )
		
		-- Misa code của loại tài sản		
        DECLARE @FACMisacodeID NVARCHAR(100)
        IF @FixedAssetCategoryID IS NOT NULL  --loai_tscd
            SET @FACMisacodeID = ( SELECT TOP 1
                                            MisacodeID + '%' --MA_PHAN_CAP
                                   FROM     FixedAssetCategory  --danh_muc_loai_tai_san_co_dinh
                                   WHERE    FixedAssetCategoryID = @FixedAssetCategoryID  --id = loai_tscd
                                 )

	-- Bảng tạm lấy ra tài sản cố định thỏa mãn ĐK đầu vào
		DROP TABLE #tblFixedAsset
        CREATE TABLE #tblFixedAsset
            (
              RefID UNIQUEIDENTIFIER , --ID_CHUNG_TU
              RefType INT ,            --LOAI_CHUNG_TU
              FixedAssetCategoryID UNIQUEIDENTIFIER , --LOAI_TSCD_ID
              FixedAssetCategoryCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS,              --MA_LOAI_TSCD
              FixedAssetCategoryName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS,
              FixedAssetID UNIQUEIDENTIFIER PRIMARY KEY ,
              RefDate DATETIME ,	--NGAY_GHI_TANG
              RefNo NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS, 
              MadeIN NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS, --NUOC_SAN_XUAT
              SerialNumber NVARCHAR(64) COLLATE SQL_Latin1_General_CP1_CI_AS,--SO_HIEU
              UseMonthYear NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS, --NGAY_THANG_DUA_VAO_SD
              FixedAssetCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS, --MA_TAI_SAN
              FixedAssetName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS,--TEN_TSCD
              OrgPrice DECIMAL(18, 4) ,--NGUYEN_GIA
              DepreciationRateMonth DECIMAL(18, 4) ,--TY_LE_TINH_KHAU_HAO_THANG
              AccumDepreciationAmount DECIMAL(18, 4) ,--KHAU_HAO_LUY_KE
              DepreciationAmount DECIMAL(18, 4) --GIA_TRI_TINH_KHAU_HAO
            )
	
        INSERT  #tblFixedAsset
                SELECT  FA.RefID , --ID_CHUNG_TU
                        FA.RefType ,--LOAI_CHUNG_TU
                        FAC.FixedAssetCategoryID ,--LOAI_TSCD_ID
                        FAC.FixedAssetCategoryCode ,--MA_LOAI_TSCD
                        FAC.FixedAssetCategoryName ,
                        FA.FixedAssetID ,--MA_TAI_SAN
                        FA.RefDate , --NGAY_CHUNG_TU
                        FA.RefNo ,
                        FA.MadeIN ,--NUOC_SAN_XUAT
                        FA.SerialNumber ,--SO_HIEU
                        CASE WHEN MONTH(FA.DepreciationDate) < 10 THEN '0'
                             ELSE ''
                        END + CAST(MONTH(FA.DepreciationDate) AS NVARCHAR(2)) --NGAY_BAT_DAU_TINH_KH --- 
                        + '/' + CAST(YEAR(FA.DepreciationDate) AS NVARCHAR(4)) , --NGAY_BAT_DAU_TINH_KH
                        FA.FixedAssetCode ,--MA_TAI_SAN
                        FA.FixedAssetName ,--TEN_TSCD
                        FA.OrgPrice ,--NGUYEN_GIA
                        FA.DepreciationRateMonth -- Tỷ lệ khấu hao tháng --TY_LE_TINH_KHAU_HAO_THANG
                        ,
                        CASE WHEN FA.RefDate >= @FromDate       --NGAY_GHI_TANG >TU_NGAY
                             THEN FA.AccumDepreciationAmount    --HAO_MON_LUY_KE
                             ELSE 0 -- FLL.AccumDepreciationAmount			
                        END AS AccumDepreciationAmount , --KHAU_HAO_LUY_KE
                        CASE WHEN FA.RefDate >= @FromDate
                             THEN FA.DepreciationAmount
                             ELSE 0 -- FLL.DepreciationAmount --
                        END AS DepreciationAmount --GIA_TRI_TINH_KHAU_HAO
                FROM    dbo.FixedAsset FA    --asset_ghi_tang
                        LEFT JOIN dbo.FixedAssetCategory FAC ON FAC.FixedAssetCategoryID = FA.FixedAssetCategoryID   --danh_muc_loai_tai_san_co_dinh FAC ON FAC.id = FA."LOAI_TAI_SAN_ID"
                        CROSS APPLY ( SELECT TOP 1
                                                OU.MisaCodeID , --MA_PHAN_CAP
                                                FL.OrganizationunitID -- Lấy lên đơn vị sử dụng cuối cùng của tài sản DON_VI_SU_DUNG_ID
                                      FROM      dbo.FixedAssetLedger FL   --so_tscd_chi_tiet
                                                INNER JOIN @tblBranch BR ON BR.BranchID = FL.BranchID
                                                INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = FL.OrganizationUnitID
                                      WHERE     FL.FixedAssetID = FA.FixedAssetID  -- FL."TSCD_ID" = FA.id
                                                AND FL.PostedDate <= @ToDate --NGAY_HACH_TOAN
                                                AND FL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                      ORDER BY  FL.POstedDate DESC ,
                                                FL.RefOrder DESC
                                    ) FL
                WHERE   ( @FixedAssetCategoryID IS NULL --loai_tscd
                          OR ( FAC.MisaCodeID LIKE @FACMisacodeID ) --(FAC."MA_PHAN_CAP" LIKE MA_PHAN_CAP_LOAI_TAI_SAN)
                        )
                        AND ( ( @OrganizationUnitID IS NULL --dv_sd
                                AND FL.OrganizationunitID IS NOT NULL --DON_VI_SU_DUNG_ID
                              )
                              OR ( FL.MisaCodeID LIKE @OUMisaCodeID )--(FL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_DON_VI)
                            )
                        AND ( ( FA.IsPostedManagement = 1
                                AND @IsWorkingWithManagementBook = 1
                              )
                              OR ( @IsWorkingWithManagementBook = 0
                                   AND FA.IsPostedFinance = 1
                                 )
                            )
                        AND FA.FixedAssetID NOT IN (
                        SELECT  FixedAssetID --MA_TAI_SAN
                        FROM    dbo.FADecrementDetail AS FAD --asset_ghi_giam_tai_san
                                INNER JOIN dbo.FADecrement AS FD ON FAD.RefID = FD.RefID  --asset_ghi_giam --
                        WHERE   ( ( FD.IsPostedFinance = 1  --state
                                    AND @IsWorkingWithManagementBook = 0
                                  )
                                  OR ( FD.IsPostedManagement = 1
                                       AND @IsWorkingWithManagementBook = 1
                                     )
                                )
                                AND FD.BranchID = @BranchID --"CHI_NHANH_ID" = chi_nhanh
                                AND FD.PostedDate < @FromDate ) --"NGAY_HACH_TOAN" < TU_NGAY
                                
                                
                                
                                
                                
	-- UPDATE Nguyên giá, Hao mòn lũy kế và giá trị tính khấu hao cho tài sản có ngày ghi tăng trước ngày FromDate
        UPDATE  FA
        SET     FA.OrgPrice = FL.OrgPrice ,--NGUYEN_GIA
                FA.AccumDepreciationAmount = FL.AccumDepreciationAmount , --HAO_MON_LUY_KE
                FA.DepreciationAmount = FL.DepreciationAmount , --GIA_TRI_TINH_KHAU_HAO
                FA.DepreciationRateMonth = FL.DepreciationRateMonth --TY_LE_TINH_KHAU_HAO_THANG
        FROM    #tblFixedAsset FA
                CROSS APPLY ( SELECT TOP 1
                                        FL.OrgPrice ,
                                        FL.AccumDepreciationAmount
                                        + FL.SumDiffAccumDepreciationAmount AS AccumDepreciationAmount ,
                                        FL.DepreciationAmount ,
                                        FL.DepreciationRateMonth
                              FROM      dbo.FixedAssetLedger FL
                              WHERE     FL.FixedAssetID = FA.FixedAssetID
                                        AND FL.PostedDate < @FromDate
                                        AND FL.IsPostToManagementBook = @IsWorkingWithManagementBook
                              ORDER BY  FL.POstedDate DESC ,
                                        FL.RefOrder DESC
                            ) FL
        WHERE   FA.RefDate < @FromDate --"NGAY_GHI_TANG" < TU_NGAY
		--SELECT 1
		--SELECT * FROM #tblFixedAsset FA
        SELECT  FA.RefID , --ID_CHUNG_TU
                FA.RefType , --LOAI_CHUNG_TU
                FA.FixedAssetCategoryID , --LOAI_TSCD_ID
                FA.FixedAssetCategoryCode , -- MA_LOAI_TSCD
                FA.FixedAssetCategoryName ,
                FA.FixedAssetID ,
                CASE WHEN FA.RefDate < @FromDate THEN NULL
                     ELSE FA.RefDate
                END AS RefDate ,--NGAY_GHI_TANG
                CASE WHEN FA.RefDate < @FromDate THEN NULL
                     ELSE FA.RefNo
                END AS RefNo ,
                FA.MadeIN ,-- NUOC_SAN_XUAT
                FA.SerialNumber , --SO_HIEU
                RIGHT(FA.UseMonthYear, 7) AS UseMonthYear , --NGAY_THANG_DUA_VAO_SD
                FA.FixedAssetCode ,--MA_TAI_SAN
                FA.FixedAssetName ,--TEN_TSCD
                FA.OrgPrice ,--NGUYEN_GIA
                FA.DepreciationRateMonth -- Tỷ lệ khấu hao tháng --TY_LE_TINH_KHAU_HAO_THANG
                ,
                0 AS MonthlyDepreciationAmount ,--KHAU_HAO
                FA.AccumDepreciationAmount ,--HAO_MON_LUY_KE
                FA.DepreciationAmount ,--KHAU_HAO_LUY_KE
                NULL AS DecrementRefID ,
                NULL AS DecrementRefType ,
                CAST (NULL AS DATETIME) AS DecrementDate -- Ngày ghi giảm--NGAY_THANG_CHUNG_TU_GHI_GIAM
                ,
                '' AS DecrementRefNo -- Số chứng từ ghi giảm --SO_HIEU_GHI_GIAM
                ,
                '' AS DecrementReason -- Lý do ghi giảm --LY_DO_GIAM_TSCD 
                ,
                1 AS SortOrder ,--THU_TU_TRONG_CHUNG_TU
                0 AS RefOrder
        FROM    #tblFixedAsset FA --TMP_KET_QUA
	--WHERE RefDate BETWEEN @FromDate AND @ToDate
        UNION ALL
        SELECT  FAL.RefID , --ID_CHUNG_TU
                FAL.RefType , --LOAI_CHUNG_TU
                FA.FixedAssetCategoryID , --LOAI_TSCD_ID
                FA.FixedAssetCategoryCode ,--MA_LOAI_TSCD
                FA.FixedAssetCategoryName ,--
                FAL.FixedAssetID ,
                CASE WHEN FAL.RefType = 251 THEN NULL
                     ELSE ISNULL(FAL.PostedDate, FAL.RefDate)
                END AS RefDate ,--NGAY_CHUNG_TU
                CASE WHEN FAL.RefType = 251 THEN ''
                     ELSE FAL.RefNo  --SO_CHUNG_TU
                END AS RefNo ,--SO_HIEU
                '' AS MadeIN ,--NUOC_SAN_XUAT
                '' AS SerialNumber ,
                '' AS UseMonthYear ,
                FA.FixedAssetCode ,
                FA.FixedAssetName ,
                FAL.DiffOrgPriceAmount AS OrgPrice --CASE WHEN FAL.RefType = 256 THEN FAL.DiffOrgPriceAmount ELSE 0 END AS OrgPrice --"CHENH_LECH_NGUYEN_GIA" AS "NGUYEN_GIA
                ,
                CASE WHEN FAL.RefType = 251
                          OR FAL.LifeTimeInMonth + FAL.SumDiffLifeTime
                          - FAL.SumMonthly = 0 -- OR LifeTimeRemainingInMonth
                          THEN 0
                     ELSE FAL.DepreciationRateMonth
                END AS DepreciationRateMonth -- Tỷ lệ khấu hao tháng --TY_LE_TINH_KHAU_HAO_THANG
			-- Khấu hao	-- Đánh giá lại và chuyển TS thuê TC thì lấy Cột chênh lệch					
                ,
                CASE WHEN FAL.RefType = 254
                     THEN FAL.MonthlyDepreciationAmountOnDepreciation --GIA_TRI_KHAU_HAO_THANG_KHI_KH
                     WHEN FAL.Reftype IN ( 252, 256 )
                     THEN ISNULL(FAL.DiffAccumDepreciationAmount, 0)--CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE
                     ELSE 0
                END AS MonthlyDepreciationAmount -- Hao mòn tháng,--KHAU_HAO
			-- Khấu hao lũy kế
                ,
                CASE WHEN FAL.RefType = 251
                     THEN FAL.DepreciationAmount - FAL.RemainingAmount  --FAL."GIA_TRI_TINH_KHAU_HAO" - FAL."GIA_TRI_CON_LAI"
                     ELSE ISNULL(FAL.AccumDepreciationAmount, 0) --GIA_TRI_HAO_MON_LUY_KE
                          + ISNULL(FAL.SumDiffAccumDepreciationAmount, 0)--CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE
                END AS AccumDepreciationAmount , --KHAU_HAO_LUY_KE
                FAL.DiffDepreciationAmount AS DepreciationAmount --CASE WHEN FAL.RefType IN (252,256) THEN FAL.DepreciationAmount ELSE 0 END AS DepreciationAmount--GIA_TRI_KHAU_HAO_THANG
                ,
                CASE WHEN FAl.RefType = 251 THEN FAL.RefID
                     ELSE NULL
                END AS DecrementRefID ,
                CASE WHEN FAl.RefType = 251 THEN FAL.RefType
                     ELSE NULL
                END AS DecrementRefType ,
                CASE WHEN FAl.RefType = 251 THEN FAL.RefDate
                     ELSE NULL
                END AS DecrementDate ,--NGAY_THANG_CHUNG_TU_GHI_GIAM
                CASE WHEN FAL.RefType = 251 THEN FAL.RefNo
                     ELSE ''
                END AS DecrementRefNo ,--SO_HIEU_GHI_GIAM
                CASE WHEN FAL.RefType = 251 THEN FAL.JournalMemo
                     ELSE ''
                END AS DecrementReason ,--LY_DO_GIAM_TSCD
                CASE WHEN FAL.RefType = 251 THEN 3
                     ELSE 2
                END AS SortOrder ,--THU_TU_TRONG_CHUNG_TU
                FAL.RefOrder
        FROM    dbo.FixedAssetLedger FAL --so_tscd_chi_tiet
                INNER JOIN #tblFixedAsset FA ON FAL.FixedAssetID = FA.FixedAssetID
                INNER JOIN @tblBranch BR ON BR.BranchID = FAL.BranchID
        WHERE   FAL.PostedDate BETWEEN @FromDate AND @ToDate --"NGAY_HACH_TOAN" BETWEEN TU_NGAY AND DEN_NGAY
                AND FAL.RefType NOT IN ( 253, 255, 250, 615 )		-- Không lấy lên chứng từ điều chuyển và kiểm kê, ghi tăng ghi giảm --LOAI_CHUNG_TU
                AND FAL.IsPostToManagementBook = @IsWorkingWithManagementBook

				--AND FAL.RefNo ='KH00002' AND FA.FixedAssetCode ='NHAA1'

				
			
        ORDER BY FixedAssetCategoryCode ,
                FixedAssetCode ,--MA_LOAI_TSCD
                SortOrder , --THU_TU_TRONG_CHUNG_TU
                RefDate ASC ,
                RefOrder ASC

	

		
		
	
    END








GO
