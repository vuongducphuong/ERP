--exec Proc_INR_GetINInventoryBalanceSummary @FromDate='2018-01-01 00:00:00',@Todate='2018-01-05 23:59:59',@StockID=N',bcb3671e-de7b-4235-9da5-a6a2dcc4d7fb,50869ad3-9a76-4c88-b175-8ae8a50fc092,57f44512-9e57-4546-9e98-50376967c321,df81b16a-6137-4f40-8268-73f6f2b2130c,92f22538-67c7-4846-8b9e-95e316f15fc4,0572c5be-650c-40a7-ab46-cc46dfc82012,7abc3711-c6e7-4a4d-a98a-6feeaef39c10,',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@UnitType=0,@InventoryItemCategoryID=NULL,@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO

-- =============================================
-- Author:		<tthoa>
-- Create date: <21/11/2014>
-- Description:	<Kho - Tổng hợp tồn kho>
-- vhanh edited 03/09/2015: Lấy thêm thông tin về đơn vị tính chính và số lượng tính theo đơn vị chính
/*modified by hoant 11.09.2015 bổ sung số lượng điều chỉnh*/
-- NBHIEU 04/01/2015 (Bug 83784): Loại bỏ các mặt hàng có tính chất là diễn giải hoặc dịch vụ
-- Modified by HHSon - 12.01.2016 - Fix bug 84746
-- vhanh edited 8.12.2016: Thêm thông tin trị xuất sản xuất (CR20079)
-- Modify by: PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
-- Modifide by NHYEN 13/4/2017 - CR 77103: Lấy thêm thông tin số lượng thành phẩm sản xuất, lắp ráp tháo rỡ của nhóm nhập, xuất 
-- ModifiedBy nhyen - 15/6/2017 (CR111754): Lấy thêm thông tin nguồn gốc VTHH 
-- Edit by nhyen - 7/9/2017 (CR 94462): Lấy thêm các cột giá trị hàng lên báo cáo
-- =============================================

DECLARE			@FromDate DATETIME 
DECLARE			@Todate DATETIME 
DECLARE			@StockID NVARCHAR(MAX) 
DECLARE			@BranchID UNIQUEIDENTIFIER 
DECLARE			@IncludeDependentBranch BIT 
DECLARE			@UnitType INT 
DECLARE			@InventoryItemCategoryID UNIQUEIDENTIFIER 
DECLARE			@IsWorkingWithManagementBook BIT


SET				@FromDate='2018-01-01 00:00:00'
SET				@Todate='2018-01-05 23:59:59'
SET				@StockID=N',bcb3671e-de7b-4235-9da5-a6a2dcc4d7fb,50869ad3-9a76-4c88-b175-8ae8a50fc092,57f44512-9e57-4546-9e98-50376967c321,df81b16a-6137-4f40-8268-73f6f2b2130c,92f22538-67c7-4846-8b9e-95e316f15fc4,0572c5be-650c-40a7-ab46-cc46dfc82012,7abc3711-c6e7-4a4d-a98a-6feeaef39c10,'
SET				@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET				@IncludeDependentBranch=1
SET				@UnitType=0
SET				@InventoryItemCategoryID=NULL
SET				@IsWorkingWithManagementBook=0

    BEGIN
        SET NOCOUNT ON 
	
        DECLARE @AccountingSystem AS NVARCHAR(10) ,
            @InventoryCategoryMISACodeID AS NVARCHAR(100) ,
            @QuantityDecimalDigits INT
        SELECT  @AccountingSystem = OptionValue
        FROM    dbo.SYSDBOption
        WHERE   OptionID = 'AccountingSystem'
                AND IsDefault = 1
                
        SELECT  @QuantityDecimalDigits = CAST(OptionValue AS INT)
        FROM    dbo.SYSDBOption
        WHERE   OptionID = 'QuantityDecimalDigits'
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
                        INNER JOIN dbo.Func_ConvertGUIStringIntoTable(@StockID,
                                                              ',') F ON S.StockID = F.Value

        DECLARE @Result TABLE
            (
              StockID UNIQUEIDENTIFIER ,
              StockCode NVARCHAR(20) , -- Mã kho
              StockName NVARCHAR(255) , -- Tên kho
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(25) , --Mã hàn
              InventoryItemName NVARCHAR(255) , --Tên hàng
              UnitName NVARCHAR(20) , --ĐVT			 
			  SalePrice1 DECIMAL(22,8) ,
			  SalePrice2 DECIMAL(22,8) ,
			  SalePrice3 DECIMAL(22,8) ,
			  FixedSalePrice DECIMAL(22,8) ,
              OriginalQuantity DECIMAL(22, 8) , --SL đầu kỳ			 
              OriginalAmount MONEY , --Giá trị đầu kỳ
		---Nhập
              ProductInQuantity DECIMAL(22, 8) , -- SL nhập thành phẩm
              ProductInAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị nhập thành phẩm
              ProductCollapsingInQuantity DECIMAL(22, 8) , -- nhyen_12/4/2017_cr77103: số lượng nhập TP lắp ráp tháo rỡ		  
              ProductCollapsingInAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị lắp ráp tháo rỡ
              MaterialInQuantity DECIMAL(22, 8) , -- SL NVL nhập lại 
              MaterialInAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị NVL nhập lại
              PUVoucherQuantity DECIMAL(22, 8) , --Mua hàng
              PUVoucherAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị mua hàng
              SAReturnPromotionQuantity DECIMAL(22, 8) , --Bán trả lại KM
              SAReturnPromotionAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại KM
              SAReturnQuantity DECIMAL(22, 8) , -- Bán trả lại khác
              SAReturnAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại khác
              TransferInQuantity DECIMAL(22, 8) , --Điều chuyển
              TransferInAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển
              /*add by hoant 11.09.2015*/
              AdjustInQuantity DECIMAL(22, 8) , --Điều chỉnh
			  AdjustInAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chỉnh
			  TotalInQuantity DECIMAL(22, 8) ,
              TotalInAmount MONEY ,
		---Xuất
              ProductOutQuantity DECIMAL(22, 8) , -- Sản xuất
              ProductOutStockAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị sản xuất
              CollapsingOutQuantity DECIMAL(22, 8) , -- nhyen_12/4/2017_cr77103: số lượng xuất lắp ráp tháo rỡ			  
              CollapsingOutAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị xuất lắp ráp tháo rỡ
              PUReturnQuantity DECIMAL(22, 8) , --Mua trả lại
              PUReturnAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): nhyen - 7/9/2017 (CR 94462): Giá trị mua trả lại
              SAVoucherQuantity DECIMAL(22, 8) , -- Bán hàng
              SAVoucherAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị bán hàng
              PromotionQuantity DECIMAL(22, 8) , --Khuyến mại
              PromotionAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị khuyến mại
              TransferOutQuantity DECIMAL(22, 8) , -- Điều chuyển
              TransferOutAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển
              /*add by hoant 11.09.2015*/
              AdjustOutQuantity DECIMAL(22, 8) , -- Điều chỉnh
              AdjustOutAmount MONEY , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chỉnh
		--OtherOutQuantity DECIMAL(18,4), --Xuất khác
              TotalOutQuantity DECIMAL(22, 8) , -- Tổng SL xuất
              TotalOutAmount MONEY , --Tổng giá trị xuất
			  ProductOutAmount MONEY, /*vhanh edited 8.12.2016: Thêm thông tin trị xuất sản xuất (CR20079)*/
		--Cuối kỳ
		--ClosingQuantity DECIMAL(18,4),
		--ClosingAmount MONEY,
              MinimumStock DECIMAL(22, 8) , -- Số lượng tồn kho tối thiểu
              InventoryCategoryName NVARCHAR(MAX) ,
			  InventoryItemSource NVARCHAR(255) ,  -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
			  --vhanh added 03/09/2015: CR 61177			   
              MainUnitName NVARCHAR(20) , -- ĐVT chính
              MainOriginalQuantity DECIMAL(22, 8) , --SL đầu kỳ theo ĐVC
              MainTotalInQuantity DECIMAL(22, 8) , -- SL nhập thành phẩm theo ĐVC
              MainTotalOutQuantity DECIMAL(22, 8) , -- Số lượng xuất theo ĐVC
              MainTotalExitsQuantity DECIMAL(18, 4), -- Số lượng theo ĐVC cuối kỳ
              --* Modify by: PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
              InventoryItemDescription NVARCHAR(255)
            )
    
        INSERT  INTO @Result
                SELECT  S.StockID ,
                        S.StockCode ,
                        S.StockName ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        U.UnitName ,
						ISNULL(IIUC.SalePrice1, I.SalePrice1) ,
						ISNULL(IIUC.SalePrice2, I.SalePrice2) ,
						ISNULL(IIUC.SalePrice3, I.SalePrice3) ,
						ISNULL(IIUC.FixedSalePrice, I.FixedSalePrice) ,
                        -- Đầu kỳ                       
                        ROUND(SUM(CASE WHEN IL.PostedDate >= @FromDate THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                            - IL.OutwardQuantity
                                       ELSE ( IL.MainInwardQuantity
                                              - IL.MainOutwardQuantity )
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS OriginalQuantity ,
                        SUM(CASE WHEN IL.PostedDate < @FromDate
                                 THEN IL.InwardAmount - IL.OutwardAmount
                                 ELSE 0
                            END) AS OriginalAmount ,
               -- Nhập trong kỳ
                        -- nhyen_12/4/2017_cr77103: Nhập TP sản xuất
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate
                                            OR IL.RefType <> 2010 THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS ProductInQuantity ,
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị nhập thành phẩm
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType = 2010 
									THEN IL.InwardAmount
                                 ELSE 0
                             END) AS ProductInAmount ,
                        ----------------------------------------------------
                        -- nhyen_12/4/2017_cr77103: Nhập TP lắp ráp tháo rỡ
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate
                                            OR IL.RefType NOT IN (2011,2012 ) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS ProductCollapsingInQuantity , 
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị lắp ráp tháo rỡ
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (2011,2012 ) 
									THEN IL.InwardAmount
                                 ELSE 0
                           END) AS ProductCollapsingInAmount , 
                        --------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType <> 2014 THEN 0
                                       WHEN IL.AccountNumber NOT LIKE '152%'
                                            AND IL.AccountNumber NOT LIKE '153%'
                                       THEN 0
                                       WHEN ( @AccountingSystem = '15'
                                              AND IL.CorrespondingAccountNumber NOT LIKE '621%'
                                              AND IL.CorrespondingAccountNumber NOT LIKE '627%'
                                              AND IL.CorrespondingAccountNumber NOT LIKE '623%'
                                            )
                                            OR ( @AccountingSystem = '48'
                                                 AND IL.CorrespondingAccountNumber NOT LIKE '154%'
                                               ) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS MaterialInQuantity , -- SL NVL nhập lại
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị NVL nhập lại
                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 WHEN IL.RefType <> 2014 THEN 0
                                 WHEN IL.AccountNumber NOT LIKE '152%' AND IL.AccountNumber NOT LIKE '153%'
									THEN 0
                                 WHEN ( @AccountingSystem = '15'
                                        AND IL.CorrespondingAccountNumber NOT LIKE '621%'
                                        AND IL.CorrespondingAccountNumber NOT LIKE '627%'
                                        AND IL.CorrespondingAccountNumber NOT LIKE '623%'
                                       ) OR ( @AccountingSystem = '48'
                                              AND IL.CorrespondingAccountNumber NOT LIKE '154%' ) 
                                     THEN 0
                                 ELSE IL.InwardAmount
                            END) AS MaterialInAmount , 
                        ----------------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType NOT IN ( 302, 307, 308,
                                                              309, 310, 318,
                                                              319, 320, 321,
                                                              322,
                                                              352, -- nmtruong 7/12/2015: thêm các chứng từ nhập kho nhiều hóa đơn
																357,
																358,
																359,
																360,
																368,
																369,
																370,
																371,
																372 ) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS PUVoucherQuantity , --Mua hàng
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị mua hàng
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate)
										AND IL.RefType IN (302,307,308,309,310,318,319,320,321,322,352,357,358,359,360,368,369,370,371,372) 
									THEN IL.InwardAmount
								 ELSE 0
                            END) AS PUVoucherAmount , 
                        -----------------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType <> 2013 THEN 0
                                       WHEN IL.IsPromotion <> 1 THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS SAReturnPromotionQuantity , --Bán trả lại KM
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại KM
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) 
										AND IL.RefType = 2013
										AND IL.IsPromotion = 1 
									THEN IL.InwardAmount
								 ELSE 0
                            END) AS SAReturnPromotionAmount , --Bán trả lại KM
                        ---------------------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType <> 2013 THEN 0
                                       WHEN IL.IsPromotion <> 0 THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) , -- Bán trả lại khác
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại khác
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) 
										AND IL.RefType = 2013
										AND IL.IsPromotion = 0 
									THEN IL.InwardAmount
								 ELSE 0
                            END) AS SAReturnAmount , 
                        ---------------------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType NOT IN ( 2030, 2031,
                                                              2032 ) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS TransferInQuantity , --Điều chuyển
                         -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển
                         SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (2030,2031,2032) 
										THEN IL.InwardAmount
                                  ELSE 0
                             END) AS TransferInAmount , 
                         --------------------------------------------------------------
                         /*
                         2016	Nhập kho từ kiểm kê (Có điều chỉnh giá trị)
						 2027	Xuất kho từ kiểm kê (Có điều chỉnh giá trị)
                         */
                         ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType NOT IN ( 2015,2016)
                                                              THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS AdjustInQuantity , --Điều chỉnh
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chỉnh
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (2015,2016) 
										THEN IL.InwardAmount
                                  ELSE 0
                            END) AS AdjustInAmount , 
                        ------------------------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.InwardQuantity
                                       ELSE IL.MainInwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS TotalInQuantity ,
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN IL.InwardAmount
                                 ELSE 0
                            END) AS TotalInAmount ,
				---Xuất
                        -- nhyen_12/4/2017_cr77103: Xuất sản xuất
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType <> 2023 THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS ProductOutQuantity ,
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị sản xuất
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType = 2023 
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS ProductOutStockAmount ,        
                        -------------------------------
                        -- nhyen_12/4/2017_cr77103: Xuất lắp ráp tháo rỡ
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType NOT IN (2024,2025 ) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS CollapsingOutQuantity ,
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị xuất lắp ráp tháo rỡ
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (2024,2025) 
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS CollapsingOutAmount ,
                        --------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType NOT IN (3030,3031)
                                       THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS PUReturnQuantity , --Mua trả lại
                        -- nhyen - 7/9/2017 (CR 94462): nhyen - 7/9/2017 (CR 94462): Giá trị Mua trả lại, giảm giá
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (3030,3031,3040,3041) 
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS PUReturnAmount ,
                        -----------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.Reftype <> 2020 THEN 0
                                       WHEN IL.IsPromotion <> 0 THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS SAVoucherQuantity , -- Bán hàng
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị bán hàng
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) 
										AND IL.RefType = 2020
										AND IL.IsPromotion = 0 
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS SAVoucherAmount ,
                        ----------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.Reftype <> 2020 THEN 0
                                       WHEN IL.IsPromotion <> 1 THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS PromotionQuantity , --Khuyến mại
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị khuyến mại
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) 
										AND IL.RefType = 2020
										AND IL.IsPromotion = 1 
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS PromotionAmount , 
                        -----------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.Reftype NOT IN ( 2030, 2031,
                                                              2032 ) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS TransferOutQuantity , -- Điều chuyển
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (2030,2031,2032)
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS TransferOutAmount ,
                        -----------------------------------------
                         /*
                         2016	Nhập kho từ kiểm kê (Có điều chỉnh giá trị)
						2027	Xuất kho từ kiểm kê (Có điều chỉnh giá trị)
                         */
                           ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.Reftype NOT IN  (  2027,2026) THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS TransferOutQuantity , -- Điều chỉnh
                        -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chỉnh
                        SUM(CASE WHEN (IL.PostedDate BETWEEN @FromDate AND @ToDate) AND IL.RefType IN (2027,2026)
									THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS AdjustOutAmount ,
                        ------------------------------------------
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN U.UnitID IS NOT NULL
                                            AND IL.UnitID = U.UnitID
                                       THEN IL.OutwardQuantity
                                       ELSE IL.MainOutwardQuantity
                                            * ISNULL(UC.ConvertRate, 1)
                                  END), @QuantityDecimalDigits) AS TotalOutQuantity , -- Tổng SL xuất
                        SUM(CASE WHEN IL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN IL.OutwardAmount
                                 ELSE 0
                            END) AS TotalOutAmount , --Tổng giá trị xuất
						/*vhanh edited 8.12.2016: Thêm thông tin trị xuất sản xuất (CR20079)*/
						SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       WHEN IL.RefType NOT IN ( 2023, 2024,
                                                              2025 ) THEN 0                                      
                                       ELSE IL.OutwardAmount
                             END) AS ProductOutAmount,
                        ---------------------------------
                        ROUND(I.MinimumStock * ISNULL(UC.ConvertRate, 1),
                              @QuantityDecimalDigits) ,
                        I.InventoryItemCategoryName ,
                        I.InventoryItemSource ,  -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        --[dbo].[Func_GetInventoryCategoryListName](I.InventoryItemCategoryCode) AS InventoryItemCategoryName, --HHSon fix bug 84746
						-- vhanh added 03.09.2015
                        UI.UnitName AS MainUnitName ,
                        ROUND(SUM(CASE WHEN IL.PostedDate >= @FromDate THEN 0
                                       ELSE ( IL.MainInwardQuantity
                                              - IL.MainOutwardQuantity )                                           
                                  END), @QuantityDecimalDigits) AS MainOriginalQuantity ,
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       ELSE IL.MainInwardQuantity                                           
                                  END), @QuantityDecimalDigits) AS MainTotalInQuantity , -- Tổng SL nhập theo ĐVC
                        ROUND(SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                       ELSE IL.MainOutwardQuantity                                            
                                  END), @QuantityDecimalDigits) AS MainTotalOutQuantity , -- Tổng SL xuất theo ĐVC
                        0, --SL tồn cuối kỳ theo ĐVC
                        -- PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description AS InventoryItemDescription
                FROM    dbo.InventoryLedger IL
                        INNER JOIN dbo.OrganizationUnit OU ON IL.BranchID = OU.OrganizationUnitID
                        INNER JOIN @Stock S ON IL.StockID = S.StockID
                        INNER JOIN dbo.InventoryItem I ON IL.InventoryItemID = I.InventoryItemID
						LEFT JOIN dbo.InventoryItemUnitConvert IIUC ON I.InventoryItemID = IIUC.InventoryItemID AND IIUC.SortOrder = @UnitType
                        LEFT JOIN dbo.Unit UI ON I.UnitID=UI.UnitID
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
                        AND I.InventoryItemType IN(0,1) -- Không lấy mặt hàng có tính chất là dịch vụ hoặc diễn giải

                GROUP BY S.StockID ,
                        S.StockCode ,
                        S.StockName ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
						ISNULL(IIUC.SalePrice1, I.SalePrice1) ,
						ISNULL(IIUC.SalePrice2, I.SalePrice2) ,
						ISNULL(IIUC.SalePrice3, I.SalePrice3) ,
						ISNULL(IIUC.FixedSalePrice, I.FixedSalePrice) ,
                        U.UnitName ,
                        UI.UnitName ,
                        I.MinimumStock ,
                        ISNULL(UC.ConvertRate, 1) ,
                        I.InventoryItemCategoryName,
                        I.InventoryItemSource ,  -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                        -- PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description
                        --[dbo].[Func_GetInventoryCategoryListName](I.InventoryItemCategoryCode)       
            
        SELECT  ROW_NUMBER() OVER ( ORDER BY StockName, StockCode, InventoryItemCode ) AS RowNum ,
                StockID ,
                StockCode ,
                StockName ,
                InventoryItemID ,
                InventoryItemCode ,
                InventoryItemName ,
                UnitName ,
				SalePrice1 ,
				SalePrice2 ,
				SalePrice3 ,
				FixedSalePrice ,
                OriginalQuantity ,
                OriginalAmount ,
          -- Nhập
                ProductInQuantity ,
                ProductInAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị nhập thành phẩm
                ProductCollapsingInQuantity , -- nhyen_12/4/2017_cr77103: số lượng nhập TP lắp ráp tháo rỡ
                ProductCollapsingInAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị lắp ráp tháo rỡ
                MaterialInQuantity ,
                MaterialInAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị NVL nhập lại
                PUVoucherQuantity ,
                PUVoucherAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị mua hàng
                SAReturnPromotionQuantity ,
                SAReturnPromotionAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại KM
                SAReturnQuantity ,
                SAReturnAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại khác
                TransferInQuantity ,
                TransferInAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển
                AdjustInQuantity ,
                AdjustInAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chỉnh
                -- nhập khác |nhyen_12/4/2017_cr77103: Tổng SL nhập trong kỳ – SL trên các cột: TP Sản xuất, TP Lắp ráp/Tháo dỡ, Nhập lại NVL, Mua hàng, bán trả lại KM, Bán trả lại khác, Điều chuyển, Điều chỉnh
                TotalInQuantity - ProductInQuantity - ProductCollapsingInQuantity - MaterialInQuantity
					- PUVoucherQuantity - SAReturnPromotionQuantity
					- SAReturnQuantity - TransferInQuantity -AdjustInQuantity  AS OtherInQuantity ,
				-- nhyen - 7/9/2017 (CR 94462): Giá trị nhập khác
				TotalInAmount - ProductInAmount - ProductCollapsingInAmount - MaterialInAmount - PUVoucherAmount 
					- SAReturnPromotionAmount - SAReturnAmount- TransferInAmount -AdjustInAmount  AS OtherInAmount , 
                TotalInQuantity ,
                TotalInAmount ,
         -- Xuất
                ProductOutQuantity ,
                ProductOutStockAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị sản xuất
                CollapsingOutQuantity, -- nhyen_12/4/2017_cr77103: số lượng xuất lắp ráp tháo rỡ
                CollapsingOutAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị xuất lắp ráp tháo rỡ
                PUReturnQuantity ,
                PUReturnAmount , -- nhyen - 7/9/2017 (CR 94462): nhyen - 7/9/2017 (CR 94462): Giá trị mua trả lại
                SAVoucherQuantity ,
                SAVoucherAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị bán hàng
                PromotionQuantity ,
                PromotionAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị khuyến mại
                TransferOutQuantity ,
                TransferOutAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển
                AdjustOutQuantity ,
                AdjustOutAmount , -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chỉnh
                -- Xuất khác |nhyen_12/4/2017_cr77103: Tổng số lượng xuất – Xuất sản xuất, xuất lắp ráp/tháo dỡ, mua trả lại, bán hàng, khuyến mại, điều chuyển, điều chỉnh
                TotalOutQuantity - ProductOutQuantity - CollapsingOutQuantity - PUReturnQuantity
					- SAVoucherQuantity - PromotionQuantity - TransferOutQuantity-AdjustOutQuantity AS OtherOutQuantity ,
				-- nhyen - 7/9/2017 (CR94462): Giá trị xuất khác = Tổng GT xuất – Xuất sản xuất, xuất lắp ráp/tháo dỡ, mua trả lại, giảm  giá, bán hàng, khuyến mại, điều chuyển, điều chỉnh
				TotalOutAmount - ProductOutStockAmount - CollapsingOutAmount - PUReturnAmount
					- SAVoucherAmount - PromotionAmount - TransferOutAmount - AdjustOutAmount AS OtherOutAmount , 
                TotalOutQuantity ,
                TotalOutAmount ,
				ProductOutAmount,/*Giá trị xuất sản xuất*/
                OriginalQuantity + TotalInQuantity - TotalOutQuantity AS ExitsQuantity ,
                OriginalAmount + TotalInAmount - TotalOutAmount AS ExitsAmount ,
                MinimumStock ,
                InventoryCategoryName ,
                InventoryItemSource ,  -- nhyen_15/6/2017_Cr111754: Thông tin nguồn gốc
                MainUnitName , -- ĐVT chính
                MainOriginalQuantity , --SL đầu kỳ theo ĐVC
                MainTotalInQuantity , -- SL nhập thành phẩm theo ĐVC
                MainTotalOutQuantity , -- Số lượng xuất theo ĐVC
                (MainOriginalQuantity + MainTotalInQuantity - MainTotalOutQuantity) AS MainTotalExitsQuantity, -- Số lượng theo ĐVC cuối kỳ
                 --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                InventoryItemDescription
        FROM    @Result
        WHERE   OriginalQuantity <> 0
                OR OriginalAmount <> 0
                OR ProductInQuantity <> 0 OR ProductInAmount <> 0
                OR MaterialInQuantity <> 0 OR MaterialInAmount <> 0
                OR PUVoucherQuantity <> 0 OR PUVoucherAmount <> 0
                OR SAReturnPromotionQuantity <> 0 OR SAReturnPromotionAmount <> 0
                OR SAReturnQuantity <> 0 OR SAReturnAmount <> 0
                OR TransferInQuantity <> 0 OR TransferInAmount <> 0
                OR AdjustInQuantity <> 0 OR AdjustInAmount <> 0
                OR TotalInQuantity <> 0
                OR TotalInAmount <> 0
                OR ProductOutQuantity <> 0 OR ProductOutStockAmount <> 0
                OR PUReturnQuantity <> 0 OR PUReturnAmount <> 0
                OR SAVoucherQuantity <> 0 OR SAVoucherAmount <> 0
                OR PromotionQuantity <> 0 OR PromotionAmount <> 0
                OR TransferOutQuantity <> 0 OR TransferOutAmount <> 0
                OR AdjustOutQuantity <> 0 OR AdjustOutAmount <> 0
                OR TotalOutQuantity <> 0
                OR TotalOutAmount <> 0  
				OR MainOriginalQuantity <> 0
				OR TotalInQuantity <> 0
				OR TotalOutQuantity <> 0
				OR MainTotalExitsQuantity <> 0
        --ORDER BY StockName, StockCode, InventoryItemCode
    END

