--exec Proc_INR_GetINInventoryBalanceSummaryByLotNo @BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@InventoryItemCategoryID=NULL,@UnitType=0,@ListStockID=N',bcb3671e-de7b-4235-9da5-a6a2dcc4d7fb,50869ad3-9a76-4c88-b175-8ae8a50fc092,57f44512-9e57-4546-9e98-50376967c321,df81b16a-6137-4f40-8268-73f6f2b2130c,92f22538-67c7-4846-8b9e-95e316f15fc4,0572c5be-650c-40a7-ab46-cc46dfc82012,7abc3711-c6e7-4a4d-a98a-6feeaef39c10,',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
/*******************************************
 * Created By:		VNTUAN
 * Created Date:	02.07.2014
 * Description:		Lay du lieu cho bao cao << Tổng hợp tồn kho theo lô >>
 * Modified by HHSon - 12.01.2016 - Fix bug 84746
 * Modify by: PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
 *******************************************/
 -- tthoa edit 24/11/2014

DECLARE			@BranchID UNIQUEIDENTIFIER 
DECLARE			@IncludeDependentBranch BIT 
DECLARE			@FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@InventoryItemCategoryID UNIQUEIDENTIFIER = NULL 
DECLARE			@UnitType INT = 0 
DECLARE			@ListStockID NVARCHAR(MAX) 
DECLARE			@IsWorkingWithManagementBook BIT


SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-05 23:59:59'
SET			@InventoryItemCategoryID=NULL
SET			@UnitType=0
SET			@ListStockID=N',bcb3671e-de7b-4235-9da5-a6a2dcc4d7fb,50869ad3-9a76-4c88-b175-8ae8a50fc092,57f44512-9e57-4546-9e98-50376967c321,df81b16a-6137-4f40-8268-73f6f2b2130c,92f22538-67c7-4846-8b9e-95e316f15fc4,0572c5be-650c-40a7-ab46-cc46dfc82012,7abc3711-c6e7-4a4d-a98a-6feeaef39c10,'
SET			@IsWorkingWithManagementBook=0

    BEGIN
	
        SET NOCOUNT ON;
  
        DECLARE @AccountingSystem AS NVARCHAR(10) ,
            @InventoryCategoryMISACodeID AS NVARCHAR(100)
        SELECT  @AccountingSystem = OptionValue
        FROM    dbo.SYSDBOption
        WHERE   OptionID = 'AccountingSystem'
                AND IsDefault = 1

        SELECT  @InventoryCategoryMISACodeID = MISACodeID
        FROM    dbo.InventoryItemCategory
        WHERE   InventoryCategoryID = @InventoryItemCategoryID

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
                        INNER JOIN dbo.Func_ConvertGUIStringIntoTable(@ListStockID,
                                                              ',') F ON S.StockID = F.Value

        DECLARE @Result TABLE
            (
              StockID UNIQUEIDENTIFIER ,
              StockCode NVARCHAR(20) , -- Mã kho
              StockName NVARCHAR(255) , -- Tên kho
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(25) , --Mã hàn
              InventoryItemName NVARCHAR(255) , --Tên hàng
              InventoryItemCategoryName NVARCHAR(MAX) ,
              LotNo NVARCHAR(50) ,
              ExpiryDate DATETIME ,
              UnitName NVARCHAR(20) , --ĐVT
              OpeningQuantity DECIMAL(22, 8) , --SL đầu kỳ
              OpeningAmount MONEY , --Giá trị đầu kỳ
	---Nhập
              InwardQuantity DECIMAL(22, 8) ,
              InwardAmount MONEY ,
	---Xuất
              OutwardQuantity DECIMAL(22, 8) , -- Tổng SL xuất
              OutwardAmount MONEY ,  --Tổng giá trị xuất
              --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
              InventoryItemDescription NVARCHAR(255)
	--Cuối kỳ
	--ClosingQuantity DECIMAL(18,4),
	--ClosingAmount MONEY,
    --InventoryCategoryName NVARCHAR(255)
            )

        INSERT  INTO @Result
                SELECT  S.StockID ,
                        S.StockCode ,
                        S.StockName ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        I.InventoryItemCategoryName ,
                        --[dbo].[Func_GetInventoryCategoryListName](I.InventoryItemCategoryCode) AS InventoryItemCategoryName,
                        IL.LotNo ,
                        IL.ExpiryDate ,
                        U.UnitName ,
                        SUM(CASE WHEN IL.PostedDate < @FromDate
                                 THEN ( CASE WHEN U.UnitID IS NOT NULL
                                                  AND IL.UnitID = U.UnitID --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
                                                  THEN IL.InwardQuantity
                                                  - IL.OutwardQuantity
                                             ELSE ( IL.MainInwardQuantity -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục
                                                    - IL.MainOutwardQuantity )
                                                  * ISNULL(UC.ConvertRate, 1)
                                        END )
                                 ELSE 0
                            END) AS OpeningQuantity , -- Tổng SL tồn đầu kỳ
                        SUM(CASE WHEN IL.PostedDate < @FromDate
                                 THEN IL.InwardAmount - IL.OutwardAmount
                                 ELSE 0
                            END) AS OpeningAmount ,
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN ( CASE WHEN U.UnitID IS NOT NULL
                                                  AND IL.UnitID = U.UnitID --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
                                                  THEN IL.InwardQuantity
                                             ELSE IL.MainInwardQuantity -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục											  
                                                  * ISNULL(UC.ConvertRate, 1)
                                        END )
                                 ELSE 0
                            END) AS TotalInQuantity ,   -- Tổng SL nhập 
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN IL.InwardAmount
                                 ELSE 0
                            END) AS TotalInAmount ,
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN ( CASE WHEN U.UnitID IS NOT NULL
                                                  AND IL.UnitID = U.UnitID --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
                                                  THEN IL.OutwardQuantity
                                             ELSE IL.MainOutwardQuantity -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục											  
                                                  * ISNULL(UC.ConvertRate, 1)
                                        END )
                                 ELSE 0
                            END) AS TotalOutQuantity ,    -- Tổng SL xuất
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS TotalOutAmount ,  --Tổng giá trị xuất
                            --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description AS InventoryItemDescription
                FROM    dbo.InventoryLedger IL
                        INNER JOIN dbo.OrganizationUnit OU ON IL.BranchID = OU.OrganizationUnitID
                        INNER JOIN @Stock S ON IL.StockID = S.StockID
                        INNER JOIN dbo.InventoryItem I ON IL.InventoryItemID = I.InventoryItemID
                        LEFT JOIN ( SELECT  IIUC.InventoryItemID ,
                                            UnitID ,
                                            ( CASE WHEN IIUC.ExchangeRateOperator = '/'
                                                   THEN IIUC.ConvertRate
                                                   WHEN IIUC.ConvertRate = 0
                                                   THEN 1
                                                   ELSE 1 / IIUC.ConvertRate
                                              END ) AS ConvertRate
                                    FROM    dbo.InventoryItemUnitConvert IIUC
                                    WHERE   IIUC.SortOrder = @UnitType
                                  ) UC ON I.InventoryItemID = UC.InventoryItemID
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
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                GROUP BY S.StockID ,
                        S.StockCode ,
                        S.StockName ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        I.InventoryItemCategoryName ,
                        --[dbo].[Func_GetInventoryCategoryListName](I.InventoryItemCategoryCode) ,
                        IL.LotNo ,
                        IL.ExpiryDate ,
                        U.UnitName ,
                        UC.ConvertRate ,
                          --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description 


        
        
        SELECT  ROW_NUMBER() OVER ( ORDER BY StockName , StockCode , InventoryItemCode ) AS RowNum ,
                StockID ,
                StockCode ,
                StockName ,
                InventoryItemID ,
                InventoryItemCode ,
                InventoryItemName ,
                InventoryItemCategoryName ,
                LotNo ,
                ExpiryDate ,
                UnitName ,
                OpeningQuantity ,
                OpeningAmount ,
                InwardQuantity ,
                InwardAmount ,
                OutwardQuantity ,
                OutwardAmount ,
                OpeningQuantity + InwardQuantity - OutwardQuantity AS ExitsQuantity ,
                OpeningAmount + InwardAmount - OutwardAmount AS ExitsAmount,
                --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                InventoryItemDescription
        FROM    @Result
        WHERE   OpeningQuantity <> 0
                OR OpeningAmount <> 0
                OR InwardQuantity <> 0
                OR InwardAmount <> 0
                OR OutwardQuantity <> 0
                OR OutwardAmount <> 0
        --ORDER BY StockName ,
        --        StockCode ,
        --        InventoryItemCode
    END

