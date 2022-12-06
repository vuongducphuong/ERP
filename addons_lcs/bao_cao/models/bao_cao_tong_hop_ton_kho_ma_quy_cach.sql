--exec Proc_INR_GetINSummaryBySerialNumber @BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@StockID='A0624CFA-D105-422F-BF20-11F246704DC3',@ListInventoryItemID=N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
/*******************************************
 * Created By:		VNTUAN
 * Created Date:	02.07.2014
 * Description:		Lay du lieu cho bao cao << Tổng hợp nhập xuất tồn theo mã quy cách >>
 * TTHOA HOÀN THIỆN 8/12/2014
 * Sửa lại ngày 17/12/2014 : lấy số lượng theo số lượng nhập (ko quy đổi nữa)
 * TTHOA Sửa lại ngày 27/2/2014 : VTCHI lưu kho theo 1 cột InwardStockID thôi, ko lưu theo OutwardStockID nữa
 * Modified by HHSon - 13.01.2016 - Fix bug 84746
 add order by  by hoant 08.12.2016 sửa lỗi 23690 Tổng hợp nhập xuất tồn theo Mã quy cách: lỗi sắp xếp sai thứ tự
  -- nmtruong 12/12/2016: sửa lỗi số lượng tồn 0 nhưng còn giá trị
  * Modify by: PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
 *******************************************/

DECLARE		@BranchID UNIQUEIDENTIFIER 
DECLARE		@IncludeDependentBranch BIT 
DECLARE		@FromDate DATETIME 
DECLARE		@ToDate DATETIME 
DECLARE		@StockID UNIQUEIDENTIFIER = NULL 
--DECLARE		--@InventoryItemCategoryID UNIQUEIDENTIFIER = NULL ,
DECLARE		@ListInventoryItemID NVARCHAR(MAX) 
DECLARE		@IsWorkingWithManagementBook BIT


SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-05 23:59:59'
SET			@StockID='A0624CFA-D105-422F-BF20-11F246704DC3'
SET			@ListInventoryItemID=N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
SET			@IsWorkingWithManagementBook=0

    BEGIN
        SET NOCOUNT ON;
	
        DECLARE @AllStockID AS UNIQUEIDENTIFIER
        SET @AllStockID = 'A0624CFA-D105-422F-BF20-11F246704DC3'

	--DECLARE @InventoryCategoryMISACodeID AS NVARCHAR(100) ,
	--		@InventoryItemCategoryName AS NVARCHAR(255)

	--SELECT  @InventoryCategoryMISACodeID = MISACodeID ,
	--		@InventoryItemCategoryName = @InventoryItemCategoryName
	--FROM    dbo.InventoryItemCategory
	--WHERE   InventoryCategoryID = @InventoryItemCategoryID
	
        DECLARE @AmountDecimalDigits AS INT
        SET @AmountDecimalDigits = 0
        SELECT  @AmountDecimalDigits = OptionValue
        FROM    dbo.SYSDBOption AS SO
        WHERE   OptionID LIKE N'%AmountDecimalDigits%'


        DECLARE @inventoryItem AS TABLE
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(50) ,
              InventoryItemName NVARCHAR(255) ,
              InventoryItemCategoryCode NVARCHAR(MAX) ,
              InventoryItemCategoryName NVARCHAR(MAX),
              --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
              InventoryItemDescription NVARCHAR(255)
              
		--UnitName NVARCHAR(20)
	        )
        INSERT  INTO @inventoryItem
                SELECT  I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        I.InventoryItemCategoryCode ,
                        I.InventoryItemCategoryName,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.Description
		   --U.UnitName
                FROM    dbo.InventoryItem I
                        INNER JOIN dbo.Func_ConvertGUIStringIntoTable(@ListInventoryItemID,
                                                              ',') F ON I.InventoryItemID = F.Value
	--LEFT JOIN dbo.Unit U ON I.UnitID = U.UnitID
	
	
        DECLARE @Result AS TABLE
            (
              StockID UNIQUEIDENTIFIER ,
              StockCode NVARCHAR(20) ,
              StockName NVARCHAR(128) ,
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(50) ,
              InventoryItemName NVARCHAR(255) ,
              SerialNumber1 NVARCHAR(50) ,
              SerialNumber2 NVARCHAR(50) ,
              SerialNumber3 NVARCHAR(50) ,
              SerialNumber4 NVARCHAR(50) ,
              SerialNumber5 NVARCHAR(50) ,
              UnitName NVARCHAR(20) ,
              OpeningQuantity DECIMAL(22, 8) ,
              InwardQuantity DECIMAL(22, 8) ,
              OutwardQuantity DECIMAL(22, 8) ,
              InventoryCategoryName NVARCHAR(MAX) ,
              RowNum INT IDENTITY(1, 1),
              --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
              InventoryItemDescription NVARCHAR(255)
            )
	
	
	--ORDER BY  StockCode, inventoryItemCode, PostedDate, RefDate, RefNo
	
        INSERT  INTO @Result
                SELECT  S.StockID ,
                        S.StockCode ,
                        S.StockName ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        INS.SerialNumber1 ,
                        INS.SerialNumber2 ,
                        INS.SerialNumber3 ,
                        INS.SerialNumber4 ,
                        INS.SerialNumber5 ,
                        U.UnitName ,
                        SUM(CASE WHEN IL.PostedDate >= @FromDate THEN 0
                                 WHEN INS.RefDetailID IS NULL
                                 THEN IL.InwardQuantity - IL.OutwardQuantity --(IL.MainInwardQuantity - IL.MainOutwardQuantity) 
                                 ELSE ( INS.InwardQuantity
                                        - INS.OutwardQuantity ) 
						--* (CASE 
						--		WHEN IL.ExchangeRateOperator = '*' THEN IL.MainConvertRate
						--		WHEN IL.MainConvertRate = 0 THEN 1
						--		ELSE 1/ISNULL(IL.MainConvertRate,1)
						--	END)						
                            END) ,
                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 WHEN INS.RefDetailID IS NULL
                                 THEN IL.InwardQuantity --IL.MainInwardQuantity
                                 ELSE INS.InwardQuantity
                                 --WHEN INS.InwardStockID = S.StockID
                                 --THEN INS.InwardQuantity
                                 --ELSE 0
						--* (CASE 
						--		WHEN IL.ExchangeRateOperator = '*' THEN IL.MainConvertRate
						--		WHEN IL.MainConvertRate = 0 THEN 1
						--		ELSE 1/ISNULL(IL.MainConvertRate,1)
						--	END)								
                            END) ,
                        SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0
                                 WHEN INS.RefDetailID IS NULL
                                 THEN IL.OutwardQuantity--IL.MainOutwardQuantity 
                                 ELSE INS.OutwardQuantity
                                 --WHEN INS.OutwardStockID = S.StockID
                                 --THEN INS.OutwardQuantity
                                 --ELSE 0
						--* (CASE 
						--		WHEN IL.ExchangeRateOperator = '*' THEN IL.MainConvertRate
						--		WHEN IL.MainConvertRate = 0 THEN 1
						--		ELSE 1/ISNULL(IL.MainConvertRate,1)
						--	END)
                            END) ,
                        I.InventoryItemCategoryName,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.InventoryItemDescription
                        --[dbo].[Func_GetInventoryCategoryListName](I.InventoryItemCategoryCode)
                FROM    dbo.InventoryLedger IL
                        INNER JOIN dbo.Stock S ON IL.StockID = S.StockID
                        INNER JOIN @inventoryItem I ON IL.InventoryItemID = I.InventoryItemID
                        INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = IL.BranchID
                        LEFT JOIN dbo.INSerialNumber INS ON IL.RefDetailID = INS.RefDetailID
                        LEFT JOIN Unit U ON IL.UnitID = U.UnitID
                WHERE   IL.PostedDate <= @ToDate
                        AND ( ( IL.StockID = @StockID
                                AND ( INS.InwardStockID IS NULL
                                      OR INS.InwardStockID = @StockID
                                    )
                              ) --Sửa lỗi jira SMEFIVE-3392: TH chứng từ có chứng từ chuyển cho chọn mã quy cách -> bị duplicate số liệu của dòng nhập/xuất
                              OR @StockID IS NULL
                              OR @StockID = @AllStockID
                            )
                        AND ( INS.InwardStockID IS NULL
                              OR INS.InwardStockID = IL.StockID
                            )
                        AND ( OU.OrganizationUnitID = @BranchID
                              OR ( OU.IsDependent = 1
                                   AND @IncludeDependentBranch = 1
                                 )
                            )
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                GROUP BY S.StockID ,
                        S.StockCode ,
                        S.StockName ,
                        I.InventoryItemID ,
                        I.InventoryItemCode ,
                        I.InventoryItemName ,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        
                        I.InventoryItemDescription,
                        INS.SerialNumber1 ,
                        INS.SerialNumber2 ,
                        INS.SerialNumber3 ,
                        INS.SerialNumber4 ,
                        INS.SerialNumber5 ,
                        U.UnitName ,
                        I.InventoryItemCategoryName
                        
                        --[dbo].[Func_GetInventoryCategoryListName](I.InventoryItemCategoryCode)
                ORDER BY S.StockName ,
                        I.InventoryItemCode ,
                        --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        I.InventoryItemDescription,
                        INS.SerialNumber1 ,
                        INS.SerialNumber2 ,
                        INS.SerialNumber3 ,
                        INS.SerialNumber4 ,
                        INS.SerialNumber5
	

        DECLARE @Master TABLE
            (
              InventoryItemID UNIQUEIDENTIFIER ,
              StockID UNIQUEIDENTIFIER ,
              RemaningAmount DECIMAL(22, 8) ,
              TotalAmount DECIMAL(22, 8) ,
              IsMaster BIT ,
              MaxRowNum INT
            )
        INSERT  @Master
                ( InventoryItemID ,
                  StockID ,
                  RemaningAmount ,
                  TotalAmount ,
                  IsMaster ,
                  MaxRowNum
                )
		
		--SELECT IL.InventoryItemID,SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0 ELSE IL.InwardAmount - IL.OutwardAmount  End),SUM(CASE WHEN IL.PostedDate < @FromDate THEN 0 ELSE IL.InwardAmount - IL.OutwardAmount  End),1,0 FROM   
                SELECT  IL.InventoryItemID ,
                        IL.StockID ,
                        SUM(IL.InwardAmount - IL.OutwardAmount) ,
                        SUM(IL.InwardAmount - IL.OutwardAmount) ,
                        1 ,
                        0
                FROM    dbo.InventoryLedger IL
                        INNER JOIN dbo.Stock S ON IL.StockID = S.StockID
                        INNER JOIN @inventoryItem I ON IL.InventoryItemID = I.InventoryItemID
                        INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = IL.BranchID
                        LEFT JOIN Unit U ON IL.UnitID = U.UnitID
                WHERE   IL.PostedDate <= @ToDate
                        AND ( ( IL.StockID = @StockID ) --AND (INS.InwardStockID IS NULL OR INS.InwardStockID = @StockID)) --Sửa lỗi jira SMEFIVE-3392: TH chứng từ có chứng từ chuyển cho chọn mã quy cách -> bị duplicate số liệu của dòng nhập/xuất
                              OR @StockID IS NULL
                              OR @StockID = @AllStockID
                            ) 
						--AND (INS.InwardStockID IS NULL OR INS.InwardStockID = IL.StockID)
                        AND ( OU.OrganizationUnitID = @BranchID
                              OR ( OU.IsDependent = 1
                                   AND @IncludeDependentBranch = 1
                                 )
                            )
                        AND IL.IsPostToManagementBook = @IsWorkingWithManagementBook
                GROUP BY IL.InventoryItemID ,
                        IL.StockID

        INSERT  @Master
                ( InventoryItemID ,
                  StockID ,
                  RemaningAmount ,
                  TotalAmount ,
                  IsMaster ,
                  MaxRowNum
		        )
                SELECT  [@Result].InventoryItemID ,
                        [@Result].StockID ,
						--nmtruong 12/12/2016: sửa lỗi 24016 bỏ round đi để cho nhân chia ở phía sau chính xác hơn
                        CASE WHEN SUM(OpeningQuantity + InwardQuantity - OutwardQuantity) = 0 THEN 0
                             ELSE (MAX(RemaningAmount) / SUM(OpeningQuantity + InwardQuantity - OutwardQuantity))
                        END ,
                        MAX(TotalAmount) ,
                        0 ,
                        MAX(RowNum)
                FROM    @Result
                        LEFT JOIN @Master AS M ON M.InventoryItemID = [@Result].InventoryItemID
                                                  AND M.StockID = [@Result].StockID
                WHERE   InwardQuantity <> 0
                        OR OutwardQuantity <> 0
                        OR OpeningQuantity <> 0
                GROUP BY [@Result].InventoryItemID ,
                        [@Result].StockID

        DECLARE @Result1 AS TABLE
            (
              StockID UNIQUEIDENTIFIER ,
              StockCode NVARCHAR(20) ,
              StockName NVARCHAR(128) ,
              InventoryItemID UNIQUEIDENTIFIER ,
              InventoryItemCode NVARCHAR(50) ,
              InventoryItemName NVARCHAR(255) ,
              SerialNumber1 NVARCHAR(50) ,
              SerialNumber2 NVARCHAR(50) ,
              SerialNumber3 NVARCHAR(50) ,
              SerialNumber4 NVARCHAR(50) ,
              SerialNumber5 NVARCHAR(50) ,
              UnitName NVARCHAR(20) ,
              OpeningQuantity DECIMAL(22, 8) ,
              InwardQuantity DECIMAL(22, 8) ,
              OutwardQuantity DECIMAL(22, 8) ,
              ExitsQuantity DECIMAL(22, 8) ,
              InventoryCategoryName NVARCHAR(MAX) ,
              RemaningAmount DECIMAL(22, 8) ,
              TotalAmount DECIMAL(22, 8) ,
              isMax BIT,
              --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
              InventoryItemDescription NVARCHAR(255)
            )

        INSERT  @Result1
                ( StockID ,
                  StockCode ,
                  StockName ,
                  InventoryItemID ,
                  InventoryItemCode ,
                  InventoryItemName ,
                  SerialNumber1 ,
                  SerialNumber2 ,
                  SerialNumber3 ,
                  SerialNumber4 ,
                  SerialNumber5 ,
                  UnitName ,
                  OpeningQuantity ,
                  InwardQuantity ,
                  OutwardQuantity ,
                  ExitsQuantity ,
                  InventoryCategoryName ,
                  RemaningAmount ,
                  TotalAmount ,
                  isMax,
                   --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                  InventoryItemDescription
		        )
                SELECT  [@Result].StockID ,
                        StockCode ,
                        StockName ,
                        [@Result].InventoryItemID ,
                        InventoryItemCode ,
                        InventoryItemName ,
                        SerialNumber1 ,
                        SerialNumber2 ,
                        SerialNumber3 ,
                        SerialNumber4 ,
                        SerialNumber5 ,
                        UnitName ,
                        OpeningQuantity ,
                        InwardQuantity ,
                        OutwardQuantity ,
                        OpeningQuantity + InwardQuantity - OutwardQuantity AS ExitsQuantity ,
                        InventoryCategoryName ,
                        ROUND(RemaningAmount * ( OpeningQuantity
                                                 + InwardQuantity
                                                 - OutwardQuantity ),
                              @AmountDecimalDigits) AS RemaningAmount ,
                        TotalAmount ,
				--ROW_NUMBER() OVER ( ORDER BY StockName, InventoryItemCode, SerialNumber1, SerialNumber2, SerialNumber3, SerialNumber4, SerialNumber5 ) AS RowNum ,
                        CASE WHEN RowNum = MaxRowNum THEN 1
                             ELSE 0
                        END,
                         --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                        InventoryItemDescription
                FROM    @Result
                        LEFT JOIN @Master AS M ON M.InventoryItemID = [@Result].InventoryItemID
                                                  AND IsMaster = 0
                                                  AND M.StockID = [@Result].StockID
                WHERE   InwardQuantity <> 0
                        OR OutwardQuantity <> 0
                        OR OpeningQuantity <> 0

		
        UPDATE  R
        SET     RemaningAmount = ROUND(TotalAmount, @AmountDecimalDigits)
                - A.RemaningAmount
        FROM    @Result1 AS R
                INNER JOIN ( SELECT ROUND(SUM(ISNULL(RemaningAmount, 0)),
                                          @AmountDecimalDigits) AS RemaningAmount ,
                                    InventoryItemID ,
                                    StockID
                             FROM   @Result1 R
                             WHERE  isMax = 0
                             GROUP BY InventoryItemID ,
                                    StockID
                           ) A ON A.InventoryItemID = R.InventoryItemID
                                  AND A.StockID = R.StockID
        WHERE   R.isMax = 1
        

        SELECT  ROW_NUMBER() OVER ( ORDER BY StockName, InventoryItemCode, SerialNumber1, SerialNumber2, SerialNumber3, SerialNumber4, SerialNumber5 ) AS RowNum ,
                StockID ,
                StockCode ,
                StockName ,
                R.InventoryItemID ,
                InventoryItemCode ,
                InventoryItemName ,
                SerialNumber1 ,
                SerialNumber2 ,
                SerialNumber3 ,
                SerialNumber4 ,
                SerialNumber5 ,
                UnitName ,
                OpeningQuantity ,
                InwardQuantity ,
                OutwardQuantity ,
                ExitsQuantity ,
                InventoryCategoryName ,
                RemaningAmount,
                TotalAmount,
                isMax,
                --PTPhuong2 17/02/2017 bổ sung mô tả (PBI 30742)
                InventoryItemDescription
        INTO #@Result2        
        FROM    @Result1 AS R
		
		-- nmtruong 12/12/2016: sửa lỗi 24016 số lượng tồn = 0 nhưng giá trị tồn là -1: bỏ cursor thay bằng đoạn update ở phía dưới

		/*dvha: bug 94495:Tổng hợp nhập xuất tồn theo mã quy cách có số lượng tồn bằng 0 nhưng giá trị tồn là -1
		Xử lý làm tròn số trong trường hợp tồn kho = 0 nhưng giá trị tồn <> 0*/
		--DECLARE @RowNum INT,@RemaningAmount DECIMAL(22,8),@TotalAmount DECIMAL(22,8),@ExitsQuantity DECIMAL(22,8)
		--DECLARE Cur CURSOR FOR SELECT RowNum,RemaningAmount,TotalAmount,ExitsQuantity FROM #@Result2 WHERE ExitsQuantity = 0 AND RemaningAmount <> 0 AND isMax = 1
		--OPEN Cur
		--FETCH NEXT FROM Cur INTO @RowNum,@RemaningAmount,@TotalAmount,@ExitsQuantity
		--WHILE @@FETCH_STATUS = 0
		--BEGIN
		--	IF ((@TotalAmount + @RemaningAmount) <> @TotalAmount) AND @ExitsQuantity = 0
		--	BEGIN
		--		UPDATE #@Result2 SET RemaningAmount = RemaningAmount + @RemaningAmount WHERE RowNum = @RowNum - 1
		--		UPDATE #@Result2 SET RemaningAmount = 0 WHERE isMax = 1 AND RowNum = @RowNum
		--	END
		--	FETCH NEXT FROM Cur INTO @RowNum,@RemaningAmount,@TotalAmount,@ExitsQuantity
		--END
		--CLOSE Cur
		--DEALLOCATE Cur
			
		--nmtruong 12/12/2016: sửa lỗi 24016 Thêm bảng tạm để cập nhật phần bù trừ giá trị thay cho cursor
		CREATE TABLE #RedueAmountToPrevLastRow
		(RowNumToReduce INT
		,Amount  DECIMAL(22, 8))
		
		INSERT #RedueAmountToPrevLastRow		
		SELECT R3.RowNumToReduce,RemaningAmount
		FROM #@Result2 R2 
		CROSS APPLY (SELECT TOP 1 RowNum AS RowNumToReduce FROM #@Result2 
						WHERE stockID =R2.StockID AND InventoryItemID = R2.InventoryItemID AND RemaningAmount<>0 AND ExitsQuantity<>0 AND RowNum<>R2.RowNum 
						ORDER BY RowNum DESC
					)R3
		WHERE ExitsQuantity = 0 AND RemaningAmount <> 0 AND isMax = 1
		
		UPDATE R2 SET  RemaningAmount = RemaningAmount + R3.Amount
		FROM
		#@Result2 R2 
		INNER JOIN #RedueAmountToPrevLastRow R3 ON R3.RowNumToReduce = R2.RowNum

		UPDATE #@Result2 SET  RemaningAmount = 0		
		WHERE ExitsQuantity = 0 AND RemaningAmount <> 0 AND isMax = 1
			
		SELECT * FROM #@Result2 ORDER BY StockName,InventoryItemName	
		
		DROP TABLE #@Result2
		DROP TABLE #RedueAmountToPrevLastRow		
    END



