--exec Proc_INR_GetINSummaryInwardOutwardOnMultiStocks @BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@InventoryItemCategoryID=NULL,@UnitType=0,@StockID=N',bcb3671e-de7b-4235-9da5-a6a2dcc4d7fb,50869ad3-9a76-4c88-b175-8ae8a50fc092,57f44512-9e57-4546-9e98-50376967c321,df81b16a-6137-4f40-8268-73f6f2b2130c,92f22538-67c7-4846-8b9e-95e316f15fc4,0572c5be-650c-40a7-ab46-cc46dfc82012,7abc3711-c6e7-4a4d-a98a-6feeaef39c10,',@DisplayOption=2,@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
/*
 * Created By:  nmtruong
 * Created Date: 27.4.2015
 * Description:  Tổng hợp nhập xuất tồn trên nhiều kho
 -- [Proc_INR_GetINSummaryInwardOutwardOnMultiStocks]'02FA2E49-BF0D-4352-8405-C860C8135E93',0 ,'4/27/2015','4/27/2015','FBACE1F2-E591-4547-8152-F1D5890C55D1',0,',209F68D7-D2DD-4B26-93E1-A0495E95BFA8,',1,0
 --BTAnh - 27/11/2015: Khai báo bảng này để thay thế cho bảng thật để đề phòng có 2 dòng đơn giá mua cùng đơn vị tính, loại tiền của 1 vật tư
 * Modify by: PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
  -- ModifiedBy nhyen - 15/6/2017 (CR111754): Lấy thêm thông tin nguồn gốc VTHH
*/
/*Hoant 16.09.2017 phục vụ drill down về sổ chi tiết VTHH cr 136884 bổ sung thêm trường IsHasInOutBalance */

DECLARE			@BranchID UNIQUEIDENTIFIER 
DECLARE			@IncludeDependentBranch BIT 
DECLARE			@FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@InventoryItemCategoryID UNIQUEIDENTIFIER 
DECLARE			@UnitType INT = 0 
DECLARE			@StockID NVARCHAR(MAX) 
DECLARE			@DisplayOption INT  -- 1: Tất cả: Lên tất cả các vật tư, kể cả VTHH không có nhập, xuất, tồn -2: Có nhập xuất tồn: Lên các vật tư có nhập hoặc xuất hoặc tồn -- 3: Phát sinh nhập xuất: Chỉ lên các vật tư có nhập hoặc xuất
DECLARE			@IsWorkingWithManagementBook BIT


SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-05 23:59:59'
SET			@InventoryItemCategoryID=NULL
SET			@UnitType=0
SET			@StockID=N',bcb3671e-de7b-4235-9da5-a6a2dcc4d7fb,50869ad3-9a76-4c88-b175-8ae8a50fc092,57f44512-9e57-4546-9e98-50376967c321,df81b16a-6137-4f40-8268-73f6f2b2130c,92f22538-67c7-4846-8b9e-95e316f15fc4,0572c5be-650c-40a7-ab46-cc46dfc82012,7abc3711-c6e7-4a4d-a98a-6feeaef39c10,'
SET			@DisplayOption=2
SET			@IsWorkingWithManagementBook=0

    BEGIN
        SET NOCOUNT ON;  
    
    --BTAnh - 27/11/2015
    --Khai báo bảng này để thay thế cho bảng thật để đề phòng có 2 dòng đơn giá mua cùng đơn vị tính, loại tiền của 1 vật tư
        SELECT DISTINCT
                InventoryItemID ,
                UnitID ,
                CurrencyID ,
                CAST(0 AS DECIMAL(18, 4)) AS UnitPrice --SMEFIVE-9126
        INTO    #InventoryItemPurchaseUnitPrice
        FROM    [dbo].[InventoryItemPurchaseUnitPrice]
	
        UPDATE  T
        SET     UnitPrice = ISNULL(R.UnitPrice, 0) -- nmtruong 14/12/2015: check isnull để sửa lỗi tiếng anh 
        FROM    #InventoryItemPurchaseUnitPrice T
                JOIN dbo.InventoryItemPurchaseUnitPrice R ON T.InventoryItemID = R.InventoryItemID
                                                             AND T.UnitID = R.UnitID
                                                             AND T.CurrencyID = R.CurrencyID


    
        DECLARE @Result AS TABLE
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              OpenQuantity DECIMAL(25, 8) ,
              OpenAmount DECIMAL(25, 8) ,
              InwardQuantity DECIMAL(25, 8) ,
              InwardAmount DECIMAL(25, 8) ,
              OutwardQuantity DECIMAL(25, 8) ,
              OutwardAmount DECIMAL(25, 8)
            )
         
    -- Bảng tạm kho
        DECLARE @Stock AS TABLE
            (
              StockID UNIQUEIDENTIFIER ,
              StockCode NVARCHAR(20) ,
              StockName NVARCHAR(255)
            )
        INSERT  INTO @Stock
                SELECT  StockID ,
                        StockCode ,
                        StockName
                FROM    dbo.Stock S
                        INNER JOIN dbo.Func_ConvertGUIStringIntoTable(@StockID,
                                                              ',') F ON S.StockID = F.Value
    
   -- Tính xem có 1 kho hay nhiều kho. nếu là 1 kho thì không xét trường hợp chuyển kho nội bộ
        DECLARE @CountStock INT
        SET @CountStock = ( SELECT  COUNT(*)
                            FROM    @Stock
                          )
   
        DECLARE @InventoryCategoryMISACodeID AS NVARCHAR(100) ,
            @QuantityDecimalDigits INT ,
            @MainCurrencyId NVARCHAR(3)
               
        SET @QuantityDecimalDigits = ( SELECT TOP 1
                                                OptionValue
                                       FROM     dbo.SYSDBOption
                                       WHERE    OptionID = 'QuantityDecimalDigits'
                                       ORDER BY IsDefault DESC
                                     )
        SET @InventoryCategoryMISACodeID = ( SELECT TOP 1
                                                    MISACodeID
                                             FROM   dbo.InventoryItemCategory
                                             WHERE  InventoryCategoryID = @InventoryItemCategoryID
                                           )
        SET @MainCurrencyId = ( SELECT TOP 1
                                        OptionValue
                                FROM    dbo.SYSDBOption
                                WHERE   OptionID = 'MainCurrency'
                                ORDER BY IsDefault DESC
                              )
   
   
   
   -- Bảng tạm đơn vị chuyển đổi
        DECLARE @UnitByType AS TABLE
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              UnitID UNIQUEIDENTIFIER ,
              ConvertRate DECIMAL(38, 24)
            )
   
        INSERT  @UnitByType
                SELECT  IIUC.InventoryItemID ,
                        UnitID ,
                        ( CASE WHEN IIUC.ExchangeRateOperator = '/'
                               THEN IIUC.ConvertRate
                               WHEN IIUC.ConvertRate = 0 THEN 1
                               ELSE 1 / IIUC.ConvertRate
                          END ) AS ConvertRate
                FROM    dbo.InventoryItemUnitConvert IIUC
                WHERE   IIUC.SortOrder = @UnitType
            
            
        INSERT  @Result
                SELECT  I.InventoryItemID ,
                -- Số lượng đầu kỳ                       
                        ROUND(SUM(CASE WHEN IL.PostedDate >= @FromDate THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                            - IL.OutwardQuantity
                                       ELSE ( IL.MainInwardQuantity
                                              - IL.MainOutwardQuantity )
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS OpenQuantity ,
    -- Giá trị đầu lỳ
                        SUM(CASE WHEN IL.PostedDate < @FromDate
                                 THEN IL.InwardAmount - IL.OutwardAmount
                                 ELSE 0
                            END) AS OpenAmount ,
                
                -- Số lượng nhập trong kỳ
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0 -- OR IL.RefType NOT IN ( 2010, 2011, 2012 )
                                       ELSE CASE WHEN U.UnitID IS NOT NULL
                                                      AND IL.UnitID = U.UnitID
                                                 THEN IL.InwardQuantity
                                                 ELSE IL.MainInwardQuantity
                                                      * ISNULL(UC.ConvertRate,
                                                              1)
                                            END
                                  END), @QuantityDecimalDigits) AS InwardQuantity , 
    -- Giá trị nhập trong kỳ  
                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 ELSE IL.InwardAmount
                            END) AS InwardAmount ,
                
    ---Số lượng xuất trong kỳ
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0  -- WHEN IL.RefType NOT IN ( 2023, 2024, 2025 ) THEN 0
                                       ELSE CASE WHEN U.UnitID IS NOT NULL
                                                      AND IL.UnitID = U.UnitID
                                                 THEN IL.OutwardQuantity
                                                 ELSE IL.MainOutwardQuantity
                                                      * ISNULL(UC.ConvertRate,
                                                              1)
                                            END
                                  END), @QuantityDecimalDigits) AS OutwardQuantity ,
    --Giá trị xuất trong kỳ
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS OutwardAmount
                FROM    dbo.InventoryLedger IL
                        INNER JOIN dbo.OrganizationUnit OU ON IL.BranchID = OU.OrganizationUnitID
                        INNER JOIN @Stock S ON IL.StockID = S.StockID
                        INNER JOIN dbo.InventoryItem I ON IL.InventoryItemID = I.InventoryItemID
                        LEFT JOIN @UnitByType UC ON I.InventoryItemID = UC.InventoryItemID
                        LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL
                                                  AND U.UnitID = I.UnitID
                                                )
                                                OR ( UC.InventoryItemID IS NOT NULL
                                                     AND UC.UnitID = U.UnitID
                                                   )
                WHERE   ( @UnitType IS NULL
                          OR @UnitType = 0
                          OR UC.InventoryItemID IS NOT NULL
                        )
                        AND IL.PostedDate <= @Todate
                        AND ( @InventoryItemCategoryID IS NULL
                              OR I.InventoryItemCategoryList LIKE '%;'
                              + @InventoryCategoryMISACodeID + '%'
                            )
                        AND ( OU.OrganizationUnitID = @BranchID
                              OR ( @IncludeDependentBranch = 1
                                   AND OU.IsDependent = 1
                                 )
                            )
                        AND I.InventoryItemType IN ( 0, 1 ) -- Là vật tư hàng hóa hoặc thành phẩm
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                        AND ( @CountStock = 1
                              OR ( @CountStock <> 1  -- Không lấy lên xuất chuyển kho nội bộ
                                   AND IL.RefType NOT IN ( 2030, 2031, 2032 )
                                 )
                            )
                GROUP BY I.InventoryItemID 
       
  -- Nếu số lượng kho chọn khác 1 thì xem xét trường hợp chuyển kho
        IF @CountStock <> 1
            BEGIN
                INSERT  @Result
                        SELECT  I.InventoryItemID ,               
                -- Số lượng đầu kỳ                       
                                ROUND(SUM(CASE WHEN IL.PostedDate >= @FromDate
                                               THEN 0
                                               WHEN U.UnitID IS NOT NULL
                                                    AND IL.UnitID = U.UnitID
                                               THEN IL.InwardQuantity
                                                    - IL.OutwardQuantity
                                               ELSE ( IL.MainInwardQuantity
                                                      - IL.MainOutwardQuantity )
                                                    * ISNULL(UC.ConvertRate, 1)
                                          END), @QuantityDecimalDigits) AS OpenQuantity ,
    -- Giá trị đầu lỳ
                                SUM(CASE WHEN IL.PostedDate < @FromDate
                                         THEN IL.InwardAmount
                                              - IL.OutwardAmount
                                         ELSE 0
                                    END) AS OpenAmount ,
                
                -- Số lượng nhập trong kỳ
                                ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate
                                               THEN 0
                                               ELSE CASE WHEN U.UnitID IS NOT NULL
                                                              AND IL.UnitID = U.UnitID
                                                         THEN IL.InwardQuantity
                                                         ELSE IL.MainInwardQuantity
                                                              * ISNULL(UC.ConvertRate,
                                                              1)
                                                    END
                                          END), @QuantityDecimalDigits) AS InwardQuantity , 
    -- Giá trị nhập trong kỳ  
                                SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                         ELSE IL.InwardAmount
                                    END) AS InwardAmount ,
                
    ---Số lượng xuất trong kỳ
                                ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate
                                               THEN 0  -- WHEN IL.RefType NOT IN ( 2023, 2024, 2025 ) THEN 0
                                               ELSE CASE WHEN U.UnitID IS NOT NULL
                                                              AND IL.UnitID = U.UnitID
                                                         THEN IL.OutwardQuantity
                                                         ELSE IL.MainOutwardQuantity
                                                              * ISNULL(UC.ConvertRate,
                                                              1)
                                                    END
                                          END), @QuantityDecimalDigits) AS OutwardQuantity ,
    --Giá trị xuất trong kỳ
                                SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                         THEN IL.OutwardAmount
                                         ELSE 0
                                    END) AS OutwardAmount
                        FROM    dbo.InventoryLedger IL
                                INNER JOIN dbo.OrganizationUnit OU ON IL.BranchID = OU.OrganizationUnitID
                                INNER JOIN @Stock S ON IL.StockID = S.StockID
                                INNER JOIN INTransferDetail TD ON IL.RefDetailID = TD.RefDetailID
                                LEFT JOIN @Stock S1 ON TD.FromStockID = S1.StockID
                                LEFT JOIN @Stock S2 ON TD.ToStockID = S2.StockID
                                INNER JOIN dbo.InventoryItem I ON IL.InventoryItemID = I.InventoryItemID
                                LEFT JOIN @UnitByType UC ON I.InventoryItemID = UC.InventoryItemID
                                LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL
                                                          AND U.UnitID = I.UnitID
                                                        )
                                                        OR ( UC.InventoryItemID IS NOT NULL
                                                             AND UC.UnitID = U.UnitID
                                                           )
                        WHERE   ( @UnitType IS NULL
                                  OR @UnitType = 0
                                  OR UC.InventoryItemID IS NOT NULL
                                )
                                AND IL.PostedDate <= @Todate
                                AND ( @InventoryItemCategoryID IS NULL
                                      OR I.InventoryItemCategoryList LIKE '%;'
                                      + @InventoryCategoryMISACodeID + '%'
                                    )
                                AND ( OU.OrganizationUnitID = @BranchID
                                      OR ( @IncludeDependentBranch = 1
                                           AND OU.IsDependent = 1
                                         )
                                    )
                                AND I.InventoryItemType IN ( 0, 1 ) -- Là vật tư hàng hóa hoặc thành phẩm
                                AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                AND IL.RefType IN ( 2030, 2031, 2032 )
                                AND ( S1.StockID IS NULL
                                      OR S2.StockID IS NULL
                                    )
                        GROUP BY I.InventoryItemID 
            END
  
        -- 1: Tất cả: Lên tất cả các vật tư, kể cả VTHH không có nhập, xuất, tồn                
        IF @DisplayOption = 1
            BEGIN
   -- Lấy lên từ danh mục vật tư hàng hóa, nếu VTHH nào không có số liệu thì để bằng 0
                SELECT  ROW_NUMBER() OVER ( ORDER BY I.InventoryItemCode ) AS RowNum ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        U.UnitName ,
                        SUM(OpenQuantity) AS OpenQuantity ,
                        SUM(OpenAmount) AS OpenAmount ,
                        SUM(InwardQuantity) AS InwardQuantity ,
                        SUM(InwardAmount) AS InwardAmount ,
                        SUM(OutwardQuantity) AS OutwardQuantity ,
                        SUM(OutwardAmount) AS OutwardAmount ,
                        SUM(OpenQuantity + InwardQuantity - OutwardQuantity) AS CloseQuantity ,
                        SUM(OpenAmount + InwardAmount - OutwardAmount) AS CloseAmount ,
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) AS MinCloseQuantity ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource ,  -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        P.UnitPrice AS PULastUnitPrice,
                    --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description AS InventoryItemDescription
                        /*Hoant 16.09.2017 phục vụ drill down về sổ chi tiết VTHH cr 136884*/
                        ,CAST(1 AS BIT)  AS IsHasInOutBalance
                FROM    dbo.InventoryItem I
                        LEFT JOIN @Result R ON I.InventoryItemID = R.InventoryItemID
                        LEFT JOIN @UnitByType UC ON I.InventoryItemID = UC.InventoryItemID
                        LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL
                                                  AND U.UnitID = I.UnitID
                                                )
                                                OR ( UC.InventoryItemID IS NOT NULL
                                                     AND UC.UnitID = U.UnitID
                                                   )
                        LEFT JOIN #InventoryItemPurchaseUnitPrice P ON ( @UnitType <> 0
                                                              AND p.inventoryItemid = uc.InventoryItemid
                                                              AND p.Unitid = UC.unitid
                                                              OR @UnitType = 0
                                                              AND p.inventoryItemid = I.InventoryItemid
                                                              AND p.Unitid = I.unitid
                                                              )
                                                              AND currencyid = @MainCurrencyId
                WHERE   I.InventoryItemType IN ( 0, 1 ) -- Là vật tư hàng hóa hoặc thành phẩm 
                        AND ( @InventoryItemCategoryID IS NULL
                              OR I.InventoryItemCategoryList LIKE '%;'
                              + @InventoryCategoryMISACodeID + '%'
                            )
                        AND ( @UnitType IS NULL
                              OR @UnitType = 0
                              OR UC.InventoryItemID IS NOT NULL
                            )
                GROUP BY I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        U.UnitName ,
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource , -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        P.UnitPrice,
      --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        
                        I.Description
      
            END
        ELSE 
    --  2: Có nhập xuất tồn: Lên các vật tư có nhập hoặc xuất hoặc tồn
            IF @DisplayOption = 2
                SELECT  ROW_NUMBER() OVER ( ORDER BY i.InventoryItemCode ) AS RowNum ,
                        i.InventoryItemID ,
                        i.InventoryItemCode ,
                        i.InventoryItemName ,
                        u.UnitName ,
                        SUM(OpenQuantity) AS OpenQuantity ,
                        SUM(OpenAmount) AS OpenAmount ,
                        SUM(InwardQuantity) AS InwardQuantity ,
                        SUM(InwardAmount) AS InwardAmount ,
                        SUM(OutwardQuantity) AS OutwardQuantity ,
                        SUM(OutwardAmount) AS OutwardAmount ,
                        SUM(OpenQuantity + InwardQuantity - OutwardQuantity) AS CloseQuantity ,
                        SUM(OpenAmount + InwardAmount - OutwardAmount) AS CloseAmount ,
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) AS MinCloseQuantity ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource ,  -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        P.UnitPrice AS PULastUnitPrice,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description AS InventoryItemDescription
                        /*Hoant 16.09.2017 phục vụ drill down về sổ chi tiết VTHH cr 136884*/
                        ,CAST(1 AS BIT)  AS IsHasInOutBalance
                FROM    dbo.InventoryItem I
                        INNER JOIN @Result R ON I.InventoryItemID = R.InventoryItemID
                        LEFT JOIN @UnitByType UC ON I.InventoryItemID = UC.InventoryItemID
                        LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL
                                                  AND U.UnitID = I.UnitID
                                                )
                                                OR ( UC.InventoryItemID IS NOT NULL
                                                     AND UC.UnitID = U.UnitID
                                                   )
                        LEFT JOIN #InventoryItemPurchaseUnitPrice P ON ( @UnitType <> 0
                                                              AND p.inventoryItemid = uc.InventoryItemid
                                                              AND p.Unitid = UC.unitid
                                                              OR @UnitType = 0
                                                              AND p.inventoryItemid = I.InventoryItemid
                                                              AND p.Unitid = I.unitid
                                                              )
                                                              AND currencyid = @MainCurrencyId
                WHERE   I.InventoryItemType IN ( 0, 1 ) -- Là vật tư hàng hóa hoặc thành phẩm    
                GROUP BY I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        U.UnitName ,
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource , -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        P.UnitPrice,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description 
                HAVING  SUM(InwardQuantity) <> 0
                        OR SUM(InwardAmount) <> 0
                        OR SUM(OutwardQuantity) <> 0
                        OR SUM(OutwardAmount) <> 0
                        OR SUM(OpenQuantity + InwardQuantity - OutwardQuantity) <> 0
                        OR SUM(OpenAmount + InwardAmount - OutwardAmount) <> 0 
         
            ELSE  
     -- 3: Phát sinh nhập xuất: Chỉ lên các vật tư có nhập hoặc xuất
                SELECT  ROW_NUMBER() OVER ( ORDER BY i.InventoryItemCode ) AS RowNum ,
                        i.InventoryItemID ,
                        i.InventoryItemCode ,
                        i.InventoryItemName ,
                        U.UnitName ,
                        SUM(OpenQuantity) AS OpenQuantity ,
                        SUM(OpenAmount) AS OpenAmount ,
                        SUM(InwardQuantity) AS InwardQuantity ,
                        SUM(InwardAmount) AS InwardAmount ,
                        SUM(OutwardQuantity) AS OutwardQuantity ,
                        SUM(OutwardAmount) AS OutwardAmount ,
                        SUM(OpenQuantity + InwardQuantity - OutwardQuantity) AS CloseQuantity ,
                        SUM(OpenAmount + InwardAmount - OutwardAmount) AS CloseAmount ,
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) AS MinCloseQuantity ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource , -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        P.UnitPrice AS PULastUnitPrice,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description AS InventoryItemDescription
                        /*Hoant 16.09.2017 phục vụ drill down về sổ chi tiết VTHH cr 136884*/
                        ,CAST(0 AS BIT)  AS IsHasInOutBalance
                FROM    dbo.InventoryItem I
                        INNER JOIN @Result R ON I.InventoryItemID = R.InventoryItemID
                        LEFT JOIN @UnitByType UC ON I.InventoryItemID = UC.InventoryItemID
                        LEFT JOIN dbo.Unit U ON ( UC.InventoryItemID IS NULL
                                                  AND U.UnitID = I.UnitID
                                                )
                                                OR ( UC.InventoryItemID IS NOT NULL
                                                     AND UC.UnitID = U.UnitID
                                                   )
                        LEFT JOIN #InventoryItemPurchaseUnitPrice P ON ( @UnitType <> 0
                                                              AND p.inventoryItemid = uc.InventoryItemid
                                                              AND p.Unitid = UC.unitid
                                                              OR @UnitType = 0
                                                              AND p.inventoryItemid = I.InventoryItemid
                                                              AND p.Unitid = I.unitid
                                                              )
                                                              AND currencyid = @MainCurrencyId
                WHERE   I.InventoryItemType IN ( 0, 1 ) -- Là vật tư hàng hóa hoặc thành phẩm    
                GROUP BY I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        U.UnitName ,
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource , -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        P.UnitPrice,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description
                HAVING  SUM(InwardQuantity) <> 0
                        OR SUM(InwardAmount) <> 0
                        OR SUM(OutwardQuantity) <> 0
                        OR SUM(OutwardAmount) <> 0   
      
                 
    END      



