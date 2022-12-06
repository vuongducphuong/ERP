SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		<tthoa>
-- Create date: <11/12/2014>
-- Description:	<Sổ chi tiết vật liệu, công cụ, sản phẩm, hàng hóa>
-- Modify by DVThi: 16/08/2016 làm CR: 109986: Lấy thêm các dòng phát sinh đầu kỳ có số lượng =0
-- =============================================

DECLARE  @BranchID UNIQUEIDENTIFIER 
DECLARE  @IncludeDependentBranch BIT 
DECLARE  @FromDate DATETIME 
DECLARE  @ToDate DATETIME 
DECLARE  @UnitType INT 
DECLARE  @StockID UNIQUEIDENTIFIER 
DECLARE  @ListInventoryItemID NVARCHAR(MAX) 
DECLARE  @IsWorkingWithManagementBook BIT
		

SET		@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET                                                   @IncludeDependentBranch = 1
SET                                                   @FromDate = '2018-01-01 00:00:00'
SET                                                   @ToDate = '2018-12-31 23:59:59'
SET                                                   @UnitType = 0
SET                                                   @StockID = 'A0624CFA-D105-422F-BF20-11F246704DC3'
SET                                                   @ListInventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
SET                                                   @IsWorkingWithManagementBook = 0

    BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
        SET NOCOUNT ON;
	
        DECLARE @BranchName AS NVARCHAR(255)
        SELECT  @BranchName = OrganizationUnitName
        FROM    dbo.OrganizationUnit
        WHERE   OrganizationUnitID = @BranchID;

        DECLARE @OPNDescription AS NVARCHAR(255);
        SET @OPNDescription = N'Số dư đầu kỳ'
	
        DECLARE @AllStockID AS UNIQUEIDENTIFIER
        SET @AllStockID = 'A0624CFA-D105-422F-BF20-11F246704DC3'

        DECLARE @MainCurrencyID AS NVARCHAR(3)
        SET @MainCurrencyID = ( SELECT TOP 1
                                        OptionValue
                                FROM    sysdboption
                                WHERE   optionID = 'MainCurrency'
                                ORDER BY IsDefault DESC
                              )
	
        DECLARE @InventoryItem AS TABLE
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(50) ,
              InventoryItemName NVARCHAR(255) ,
              InventoryItemCategoryList NVARCHAR(255) ,
              InventoryItemCategoryName NVARCHAR(MAX) ,
              UnitID UNIQUEIDENTIFIER ,
              UnitName NVARCHAR(20) ,
              ConvertRate DECIMAL(22, 16)
            )
        INSERT  INTO @inventoryItem
                SELECT  I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        I.InventoryItemCategoryList ,
                        I.InventoryItemCategoryName ,
                        U.UnitID ,
                        U.UnitName ,
                        CASE WHEN @UnitType = 0
                                  OR @UnitType IS NULL THEN 1
                             WHEN IU.ConvertRate = 0 THEN 1
                             WHEN IU.ExchangeRateOperator = '*' THEN 1 / ISNULL(IU.ConvertRate, 1)
                             ELSE ISNULL(IU.ConvertRate, 1)
                        END
                FROM    dbo.InventoryItem I
                        INNER JOIN dbo.Func_ConvertGUIStringIntoTable(@ListInventoryItemID, ',') F ON I.InventoryItemID = F.Value
                        LEFT JOIN dbo.InventoryItemUnitConvert IU ON I.InventoryItemID = IU.InventoryItemID
                                                                     AND IU.SortOrder = @UnitType
                        LEFT JOIN dbo.Unit U ON ( ( @UnitType IS NULL
                                                    OR @UnitType = 0
                                                  )
                                                  AND I.UnitID = U.UnitID
                                                )
                                                OR ( @UnitType IS NOT NULL
                                                     AND @UnitType <> 0
                                                     AND IU.UnitID = U.UnitID
                                                   )
                WHERE   @UnitType IS NULL
                        OR @UnitType = 0
                        OR IU.SortOrder IS NOT NULL
	
	
	
        CREATE TABLE #Result
            (
              RowNum INT IDENTITY(1, 2) -- modify by Thidv 16/08/2015: Thiết lập bươc nhảy =2 để tùy biến nhét thêm dữ liệu số dư đầu kỳ =0
                         PRIMARY KEY ,
              RefID UNIQUEIDENTIFIER ,--ID_CHUNG_TU
              RefType INT , --LOAI_CHUNG_TU
              StockID UNIQUEIDENTIFIER ,--KHO_ID
              StockCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,--MA_KHO
              StockName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS ,--TEN_KHO
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              InventoryItemName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              PostedDate DATETIME ,
              RefDate DATETIME ,
              RefNo NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              JournalMemo NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CorrespondingAccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              UnitName NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CurrencyID NVARCHAR(3) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              UnitPrice DECIMAL(22, 8) ,
              InwardQuantity DECIMAL(22, 8) ,
              InwardAmount DECIMAL(25, 8) ,
              OutwardQuantity DECIMAL(22, 8) ,
              OutwardAmount DECIMAL(25, 8) ,
              ClosingQuantity DECIMAL(22, 8) ,
              ClosingAmount DECIMAL(25, 8) ,
              INRefOrder DATETIME ,
              IsBold BIT ,
              SortOrder INT ,
              RownumTemp INT  --Add by DVThi: Dùng để xử lý sắp xếp các dòng số dư đầu kỳ =0
            )
	
	
	--ORDER BY  StockCode, inventoryItemCode, PostedDate, RefDate, RefNo
	
        INSERT  INTO #Result
                SELECT  CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.RefID --ID_CHUNG_TU
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN 0
                             ELSE IL.RefType --LOAI_CHUNG_TU
                        END ,
                        S.StockID ,--KHO_ID
                        S.StockCode , --MA_KHO
                        S.StockName , --TEN_KHO
                        I.InventoryItemID ,--MA_HANG_ID
                        I.InventoryItemCode ,--MA_HANG
                        I.InventoryItemName ,-- TEN_HANG
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.PostedDate --NGAY_HACH_TOAN
                        END AS PostedDate , --NGAY_HACH_TOAN
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.RefDate
                        END AS RefDate ,--NGAY_CHUNG_TU
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.RefNo --SO_CHUNG_TU
                        END AS RefNo , --SO_CHUNG_TU
                        CASE WHEN IL.PostedDate < @FromDate THEN @OPNDescription -------------------dien_giai_dau_ky
                             ELSE IL.JournalMemo --DIEN_GIAI_CHUNG
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.CorrespondingAccountNumber --MA_TK_CO
                        END ,
                        I.UnitName ,
                        CASE WHEN IL.PostedDate < @FromDate THEN @MainCurrencyID -----------loai_tien_chinh
                             ELSE ISNULL(CurrencyID, @MainCurrencyID)
                        END AS CurrencyID ,
                        CASE WHEN IL.PostedDate < @FromDate THEN 0
                             WHEN I.UnitID = IL.UnitID THEN IL.UnitPrice
                             ELSE IL.MainUnitPrice / I.ConvertRate -- (TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH)
                        END AS UnitPrice ,
                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 WHEN IL.UnitID = I.UnitID THEN IL.InwardQuantity --SO_LUONG_NHAP
                                 ELSE IL.MainInwardQuantity * I.ConvertRate
                            END) ,
                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 ELSE IL.InwardAmount --SO_TIEN_NHAP -----------------------------------------------
                            END) ,


                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 WHEN IL.UnitID = I.UnitID THEN IL.OutwardQuantity --SO_LUONG_XUAT
                                 ELSE IL.MainOutwardQuantity * I.ConvertRate --TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                            END) ,



                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 ELSE IL.OutwardAmount --SO_TIEN_XUAT
                            END) ,
                        SUM(CASE WHEN IL.PostedDate >= @FromDate THEN 0
                                 WHEN IL.UnitID = I.UnitID THEN IL.InwardQuantity - IL.OutwardQuantity
                                 ELSE ( IL.MainInwardQuantity - IL.MainOutwardQuantity ) * I.ConvertRate
                            END) ,--SO_LUONG_TON_KQ
                        SUM(CASE WHEN IL.PostedDate >= @FromDate THEN 0
                                 ELSE IL.InwardAmount - IL.OutwardAmount -- (IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH")
                            END) ,--SO_TIEN_TON_KQ
                        MAX(IL.INRefOrder) AS INRefOrder ,
                        CASE WHEN IL.PostedDate < @FromDate THEN 1
                             ELSE 0
                        END ,
                        MAX(IL.SortOrder) AS SortOrder ,
                        RownumTemp = 0  --Dùng để sắp xếp các dòng số dư đầu kỳ =0
                FROM    dbo.InventoryLedger IL
                        INNER JOIN dbo.Stock S ON IL.StockID = S.StockID
                        INNER JOIN @inventoryItem I ON IL.InventoryItemID = I.InventoryItemID
                        INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = IL.BranchID
                WHERE   PostedDate <= @ToDate
                        AND ( IL.StockID = @StockID
                              OR @StockID IS NULL
                              OR @StockID = @AllStockID
                            )
                        AND ( OU.OrganizationUnitID = @BranchID
                              OR ( OU.IsDependent = 1
                                   AND @IncludeDependentBranch = 1
                                 )
                            )
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                GROUP BY CASE WHEN IL.PostedDate < @FromDate THEN NULL
                              ELSE IL.RefID
                         END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN 0
                             ELSE IL.RefType
                        END ,
                        S.StockID ,
                        S.StockCode , --MA_KHO
                        S.StockName , --TEN_KHO
                        I.InventoryItemID ,
                        I.InventoryItemCode , --MA
                        I.InventoryItemName , --TEN
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.PostedDate
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.RefDate
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
                             ELSE IL.RefNo
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN @OPNDescription
                             ELSE IL.JournalMemo
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN NULL
				--WHEN IL.InOutWardType = 3 THEN IL.AccountNumber
                             ELSE IL.CorrespondingAccountNumber
                        END ,
                        I.UnitName ,
                        CASE WHEN IL.PostedDate < @FromDate THEN @MainCurrencyID
                             ELSE ISNULL(CurrencyID, @MainCurrencyID)
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN 0
                             WHEN I.UnitID = IL.UnitID THEN IL.UnitPrice
                             ELSE IL.MainUnitPrice / I.ConvertRate
                        END ,
                        CASE WHEN IL.PostedDate < @FromDate THEN 1
                             ELSE 0
                        END
                ORDER BY S.StockCode ,
                        I.InventoryItemCode ,
                        RefDate ,
                        INRefOrder ,
                        RefNO ,
                        SortOrder	
	
	-- Tính số tồn
        DECLARE @ClosingQuantity AS DECIMAL(25, 8) ,
            @ClosingAmount AS DECIMAL(25, 8) ,
            @RowStockID UNIQUEIDENTIFIER ,
            @RowInventoryItemID UNIQUEIDENTIFIER
        SELECT  @ClosingAmount = 0 ,
                @ClosingQuantity = 0 ,
                @RowStockID = NEWID() ,
                @RowInventoryItemID = NEWID()
	
        UPDATE  #Result --TMP_KET_QUA
        SET     @ClosingAmount = ( CASE WHEN RefID IS NULL THEN ClosingAmount -- SO_TIEN_TON--ID_CHUNG_TU--SO_TIEN_TON_KQ
                                        WHEN @RowStockID <> StockID
                                             OR @RowInventoryItemID <> InventoryItemID THEN inwardAmount - OutwardAmount
                                        ELSE @ClosingAmount + inwardAmount - OutwardAmount
                                   END ) ,
                @ClosingQuantity = ( CASE WHEN RefID IS NULL THEN ClosingQuantity
                                          WHEN @RowStockID <> StockID
                                               OR @RowInventoryItemID <> InventoryItemID THEN inwardQuantity - OutwardQuantity
                                          ELSE @ClosingQuantity + inwardQuantity - OutwardQuantity
                                     END ) ,
                ClosingAmount = @ClosingAmount ,
                ClosingQuantity = @ClosingQuantity ,
                @RowStockID = StockID ,
                @RowInventoryItemID = InventoryItemID;


	   --Add by DVThi: Làm CR: 109986_Kế toán mong muốn xuất khẩu được thẻ kho hiện thị được số dư đầu kỳ 0 để phục vụ cho công tác viết hóa đơn bổ sung được nhanh chóng và chính xác.xmind
		
		--Bảng chưa các nhóm Kho và vật tư không bị lặp lại trên dữ liệu của báo cáo

        DECLARE @InventoryItemResult AS TABLE
            (
              StockID UNIQUEIDENTIFIER ,
              StockCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              StockName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              InventoryItemName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              RowNum INT
            )
	
        INSERT  INTO @InventoryItemResult
                SELECT  R.StockID ,
                        StockCode ,
                        StockName ,
                        R.InventoryItemID ,
                        InventoryItemCode ,
                        InventoryItemName ,
                        MIN(RowNum) - 1
                FROM    #Result R
                GROUP BY R.StockID ,
                        StockCode ,
                        StockName ,
                        R.InventoryItemID ,
                        InventoryItemCode ,
                        InventoryItemName
                
				 
		 --Lưu lại số thứ tự hiện thời

        UPDATE  #Result
        SET     RowNumTemp = RowNum;

		
		--Đấy dữ liệu liên quan đến số dư đầu kỳ =0 vào bảng #Result
        INSERT  INTO #Result
                ( RefID ,
                  RefType ,
                  StockID ,
                  StockCode ,
                  StockName ,
                  InventoryItemID ,
                  InventoryItemCode ,
                  InventoryItemName ,
                  PostedDate ,
                  RefDate ,
                  RefNo ,
                  JournalMemo ,
                  CorrespondingAccountNumber ,
                  UnitName ,
                  CurrencyID ,
                  UnitPrice ,
                  InwardQuantity ,
                  InwardAmount ,
                  OutwardQuantity ,
                  OutwardAmount ,
                  ClosingQuantity ,
                  ClosingAmount ,
                  INRefOrder ,
                  IsBold ,
                  SortOrder ,
                  RowNumTemp 
                )
                SELECT  RefID = NULL ,--ID_CHUNG_TU
                        RefType = 0 , --LOAI_CHUNG_TU
                        StockID , --ID_KHO
                        StockCode ,--MA_KHO
                        StockName , --TEN_KHO
                        InventoryItemID ,--MA_HANG_ID
                        InventoryItemCode ,--MA
                        InventoryItemName ,--TEN
                        PostedDate = NULL ,--NGAY_HACH_TOAN
                        RefDate = NULL ,--NGAY_CHUNG_TU
                        RefNo = NULL ,--SO_CHUNG_TU
                        JournalMemo = @OPNDescription , --
                        CorrespondingAccountNumber = NULL ,--MA_TK_CO
                        UnitName = NULL , --DON_VI_TINH
                        CurrencyID = NULL , -- currency_id
                        UnitPrice = CAST(0 AS DECIMAL(20, 6)) , --DON_GIA
                        InwardQuantity = CAST(0 AS DECIMAL(22, 8)) , --SO_LUONG_NHAP
                        InwardAmount = CAST(0 AS DECIMAL(18, 4)) ,--SO_TIEN_NHAP
                        OutwardQuantity = CAST(0 AS DECIMAL(22, 8)) ,--SO_LUONG_XUAT
                        OutwardAmount = CAST(0 AS DECIMAL(18, 4)) , --SO_TIEN_XUAT
                        ClosingQuantity = CAST(0 AS DECIMAL(22, 8)) , --SO_LUONG_TON
                        ClosingAmount = CAST(0 AS DECIMAL(18, 4)) ,--SO_TIEN_TON
                        INRefOrder = GETDATE() ,
                        IsBold = 0 ,
                        SortOrder = 0 ,
                        I.RowNum                        
                FROM    @InventoryItemResult I --TMP_KET_QUA_HANG_TON_KHO
                WHERE   NOT EXISTS ( SELECT 1
                                     FROM   #Result R
                                     WHERE  R.StockID = I.StockID
                                            AND R.InventoryItemID = I.InventoryItemID
                                            AND R.RefID IS NULL );


		 

	
        SELECT  @BranchName AS BranchName ,
                RefID , -- ID_CHUNG_TU
                RefType , --LOAI_CHUNG_TU
                R.StockID , -- ID_KHO
                StockCode , -- MA_KHO
                StockName , -- TEN_KHO
                InventoryItemID , -- MA_HANG_ID
                InventoryItemCode , -- MA
                InventoryItemName , -- TEN
                PostedDate , --NGAY_HACH_TOAN
                RefDate , -- NGAY_CHUNG_TU
                RefNo , -- SO_CHUNG_TU
                JournalMemo , --DIEN_GIAI_CHUNG
                CorrespondingAccountNumber , --MA_TK_CO
                UnitName , --DON_VI_TINH
                CASE WHEN RefID IS NULL
                          AND ClosingQuantity <> 0 THEN ClosingAmount / ClosingQuantity
                     WHEN RefID IS NOT NULL THEN CASE WHEN Reftype IN ( 3030, 3031 )
                                                           AND CurrencyID <> @MainCurrencyID THEN CASE WHEN InwardQuantity > 0 THEN InwardAmount / InwardQuantity
                                                                                                       WHEN OutwardQuantity > 0 THEN OutwardAmount / OutwardQuantity
                                                                                                       ELSE 0
                                                                                                  END
                                                      ELSE UNitPrice
                                                 END
                END AS UnitPrice ,--DON_GIA
                InwardQuantity ,--SO_LUONG_NHAP
                InwardAmount ,--SO_TIEN_NHAP
                OutwardQuantity ,--SO_LUONG_XUAT
                OutwardAmount , --SO_TIEN_XUAT
                ClosingQuantity , --SO_LUONG_TON_KQ
                ClosingAmount , --SO_TIEN_TON_KQ
                ROW_NUMBER() OVER ( ORDER BY RowNumTemp ASC ) AS RowNum ,--Modify by Thidv: Làm lại rowNum cho người dùng trên báo cáo
                INRefOrder ,
                IsBold ,
                SortOrder ,--THU_TU_TRONG_CHUNG_TU
                ( CASE WHEN RefID IS NULL
                            AND ClosingAmount = 0 --SO_TIEN_TON_KQ
                            AND ClosingQuantity = 0 THEN CAST(0 AS BIT)--SO_LUONG_TON_KQ
                       ELSE CAST(1 AS BIT)
                  END ) AS IsShowOnReport --Dùng để đánh dấu xem có hiển thị lên báo cáo hay không? DVThi: sửa lỗi 114692 Sổ chi tiết vật liệu, công cụ, hàng hóa=> Lỗi đang lấy lên dòng số dư đầu kỳ trường hợp kỳ trước có phát sinh nhập xuất
        FROM    #Result R
        WHERE   (( RefID IS NULL
                  AND (
						--Lấy lên số dư đầu kỳ <> 0  
                        ( ClosingAmount <> 0
                          OR ClosingQuantity <> 0
                        )		
						--Chỉ lấy những dòng số dư đầu kỳ =0 khi có phát sinh trong kỳ				
                        OR EXISTS ( SELECT  1
                                    FROM    #Result r1
                                    WHERE   R1.StockID = R.StockID
                                            AND R1.InventoryItemID = R.InventoryItemID
                                            AND r1.RefID IS NOT NULL )
                      ) --DVThi: sửa lỗi Active 114692: Nếu không phát sinh một vật tư nào đó trong trong kỳ thì không được xuất khẩu Excel Extend cái dòng đầu kỳ
                )
                OR ( RefID IS NOT NULL
                     AND ( InwardQuantity <> 0
                           OR InwardAmount <> 0
                           OR OutwardQuantity <> 0
                           OR OutwardAmount <> 0
                           OR ClosingQuantity <> 0
                           OR ClosingAmount <> 0
                         )
                   ))
				  AND  R.RefNo  = 'NK00006' 
				
        ORDER BY RowNumTemp;
		
        DROP TABLE #Result
    END


GO