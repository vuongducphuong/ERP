--exec Proc_SAR_GetReceivableSummaryByDetailInvoiceDiscout @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@CurrencyID=N'VND',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		NBHIEU
-- Create date: 17/03/2017
-- Description:	Lấy dữ liệu cho Báo cáo tổng hợp công nợ phải thu (Chi tiết theo các khoản giảm trừ)
-- NBHIEU 23/03/2017 : Tối ưu lại thủ tục để đạt key hiệu năng
-- Modifide by NHYEN 24/3/2017 bug 88175: đổi tên cột số dư cuối kỳ trên dữ liệu trả về (ClosingAmountOC -> CloseAmountOC) (ClosingAmount -> CloseAmount)
-- Modifide by nhyen 24/3/2017 bug 88601: Sửa lại cách truyền dữ liệu cho cột số tài khoản
-- =============================================

DECLARE			@FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@BranchID UNIQUEIDENTIFIER -- Chi nhánh
DECLARE			@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(20) -- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhà cung cấp
DECLARE			@CurrencyID NVARCHAR(3) -- Loại tiền    
DECLARE			@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-05 23:59:59'
SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@AccountNumber=N'131'
SET			@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET			@CurrencyID=N'VND'
SET			@IsWorkingWithManagementBook=0

    BEGIN
    	IF OBJECT_ID('tempdb..#tblBrandIDList') IS NOT NULL DROP TABLE #tblBrandIDList
    	
        CREATE TABLE #tblBrandIDList
            (
              BranchID UNIQUEIDENTIFIER PRIMARY KEY ,
              BranchCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS,
              BranchName NVARCHAR(128)COLLATE SQL_Latin1_General_CP1_CI_AS
            )
       
        INSERT  INTO #tblBrandIDList
                SELECT  FGDBBI.BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID, @IncludeDependentBranch) AS FGDBBI
              
        /*Bảng chứa danh sách  đối tượng */ 
        IF OBJECT_ID('tempdb..#tblListAccountObjectID') IS NOT NULL DROP TABLE #tblListAccountObjectID 
        CREATE TABLE #tblListAccountObjectID  -- Bảng chứa danh sách các NCC
            (
               AccountObjectID UNIQUEIDENTIFIER PRIMARY KEY,
			    AccountObjectCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS,
				AccountObjectName nvarchar(128) COLLATE SQL_Latin1_General_CP1_CI_AS,
				AccountObjectAddress nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
			    AccountObjectTaxcode nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
				Mobile nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
				AccountObjectGroupListCode nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS,
				AccountObjectGroupListName	nvarchar(MAX)COLLATE SQL_Latin1_General_CP1_CI_AS		
            ) 
	         
         INSERT  INTO #tblListAccountObjectID
            SELECT  Ao.AccountObjectID,
                    AO.AccountObjectCode,
                    AO.AccountObjectName,
                    AO.[Address] AS  AccountObjectAddress,
					AO.CompanyTaxCode AS AccountObjectTaxcode,
					/* Nếu là tổ chức thì lấy trường điện thoại trên danh mục, nếu là cá nhân thì lấy di động*/
					CASE WHEN AO.AccountObjectType = 0 THEN AO.Tel
						 WHEN AO.AccountObjectType = 1 THEN AO.Mobile
					END AS Mobile,
					AO.AccountObjectGroupListCode,
					AO.AccountObjectGroupListName
            FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,',') AS F
					INNER JOIN AccountObject AS AO ON F.[Value] = AO.AccountObjectID                                                         
                                  
                                                               			
       /* Bảng chứa số tài khoản     */
       IF OBJECT_ID('tempdb..#tblAccountNumber') IS NOT NULL DROP TABLE #tblAccountNumber 
         
        CREATE TABLE #tblAccountNumber
            (
              AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              AccountNumberDetail NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY ,
              AccountCategoryKind INT ,
              DetailByAccountObject BIT
            )
            	
        IF @AccountNumber IS NOT NULL        
            BEGIN 
                INSERT  INTO #tblAccountNumber
                        SELECT  @AccountNumber ,	/*nhyen_24/3/2017_bug88601: nếu tham số tài khoản không trống thì truyển tham số này cho cột tài khoản*/
							    A.AccountNumber, --+ '%' ,
                                A.AccountCategoryKind ,
                                A.DetailByAccountObject
                        FROM    dbo.Account AS A
                        WHERE   ((AccountNumber like @AccountNumber +'%')
                                  AND DetailByAccountObject = 1
                                  AND AccountObjectType = 1
                                )
                        ORDER BY A.AccountNumber ,
                                A.AccountName 
                
            END
        ELSE 
        
            BEGIN 
                INSERT  INTO #tblAccountNumber                
                        SELECT  A.AccountNumber ,
                         A.AccountNumber,-- + '%' ,
                                A.AccountCategoryKind ,
                                A.DetailByAccountObject                                
                        FROM    dbo.Account AS A
                        WHERE   ( DetailByAccountObject = 1
                                  AND AccountObjectType = 1
                                  AND IsParent = 0
                                )
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END         
         
        /*Đồng tiền hạch toán*/         
        DECLARE @MainCurrency NVARCHAR(10)
        SELECT TOP 1
                @MainCurrency = OptionValue
        FROM    dbo.SYSDBOption
        WHERE   OptionID LIKE N'%MainCurrency%' 
        
        /*Chế độ kế toán */
        DECLARE @AccountingSystem INT
        SELECT TOP 1
                @AccountingSystem = OptionValue
        FROM    dbo.SYSDBOption
        WHERE   OptionID LIKE N'%AccountingSystem%'
        
      /*Quyết định 48 hay tt133: =0 là 48 ; =133 là 133 */
        DECLARE @SubAccountSystem INT
        SELECT TOP 1
                @SubAccountSystem = OptionValue
        FROM    dbo.SYSDBOption
        WHERE   OptionID = N'SubAccountSystem'
        
        IF OBJECT_ID('tempdb..#tblResult') IS NOT NULL DROP TABLE #tblResult              
		-- Bảng chứa kết quả cần lấy
        CREATE TABLE #tblResult
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(100)COLLATE SQL_Latin1_General_CP1_CI_AS ,   -- Mã KH
              AccountObjectName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,	-- Tên KH              
              AccountObjectAddress NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Địa chỉ     
              AccountObjectTaxcode NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Mã số thuế
              Mobile nvarchar(50)COLLATE SQL_Latin1_General_CP1_CI_AS, -- Điện thoại
              AccountNumber NVARCHAR(20)COLLATE SQL_Latin1_General_CP1_CI_AS ,  -- Tài khoản
              OpenDebitAmountOC		DECIMAL (18,4),-- Số dư đầu kỳ
			  OpenDebitAmount		DECIMAL (18,4), -- Dư đầu kỳ quy đổi			  
              ReceiptAbleAmountOC DECIMAL (18,4) ,	-- Phải thu
              ReceiptAbleAmount DECIMAL (18,4) , -- Phải thu quy đổi              
              DiscountAmountOC DECIMAL (18,4) , -- Chiết khấu
              DiscountAmount DECIMAL (18,4) , -- Chiết khấu quy đổi              
              ReturnAmountOC DECIMAL (18,4) , --Trả lại/Giảm giá
              ReturnAmount DECIMAL (18,4) , --Trả lại/giảm giá Quy đổi              
              DiscountOtherAmountOC DECIMAL (18,4) ,	--Chiết khấu TT/ giảm trừ khác
              DiscountOtherAmount DECIMAL (18,4) , --Chiết khấu TT/ giảm trừ khác quy đổi              
              ReceiptedAmountOC DECIMAL (18,4) ,	-- Số đã thu
              ReceiptedAmount DECIMAL (18,4) , -- Số đã thu quy đổi             
              ClosingAmountOC DECIMAL (18,4) ,	-- Số dư cuối kỳ
              ClosingAmount DECIMAL (18,4) , -- Số dư cuối kỳ quy đổi              
              AccountObjectGroupListCode NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS, --Mã nhóm KH
              AccountObjectGroupListName NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS, --Tên nhóm KH                        
              
            )
       
       /*Lấy dữ liệu ---------------*/
       
        INSERT  INTO #tblResult
        SELECT 
			A.AccountObjectID ,
			A.AccountObjectCode ,
			A.AccountObjectName ,
			A.AccountObjectAddress ,
			A.AccountObjectTaxcode ,
			A.Mobile,
			A.AccountNumber,
			SUM(OpenDebitAmountOC) AS OpenDebitAmountOC,
			SUM(OpenDebitAmount) AS OpenDebitAmount,
			SUM(ReceiptAbleAmountOC) AS ReceiptAbleAmountOC,
			SUM(ReceiptAbleAmount) AS ReceiptAbleAmount,
			SUM(DiscountAmountOC) AS DiscountAmountOC,
			SUM(DiscountAmount) AS DiscountAmount,
			SUM(ReturnAmountOC) AS ReturnAmountOC,
			SUM(ReturnAmount) AS ReturnAmount,
			SUM(DiscountOtherAmountOC) AS DiscountOtherAmountOC,
			SUM(DiscountOtherAmount) AS DiscountOtherAmount,
			SUM(ReceiptedAmountOC) AS ReceiptedAmountOC,
			SUM(ReceiptedAmount) AS ReceiptedAmount,
			0 AS ClosingAmountOC,
			0 AS ClosingAmount,
			
			AccountObjectGroupListCode ,
			AccountObjectGroupListName 
        FROM
          (
				/* Dư đầu kỳ - tách việc iner join có Or thành UNIOn ALL cho chạy nhanh*/
				SELECT  
						LAOI.AccountObjectID ,
						LAOI.AccountObjectCode ,
						LAOI.AccountObjectName ,
						LAOI.AccountObjectAddress,
						LAOI.AccountObjectTaxcode,
						LAOI.Mobile,
						TBAN.AccountNumber,
						
						SUM(SL.DebitAmountOC - SL.CreditAmountOC) AS OpenDebitAmountOC,
						SUM(SL.DebitAmount - SL.CreditAmount) AS OpenDebitAmount,
														
						0 AS ReceiptAbleAmountOC  ,	-- Phải thu
						0 AS ReceiptAbleAmount  , -- Phải thu quy đổi
				          
						0 AS DiscountAmountOC  , -- Chiết khấu
						0 AS DiscountAmount  , -- Chiết khấu quy đổi
				          
						0 AS ReturnAmountOC  , --Trả lại/Giảm giá
						0 AS ReturnAmount  , --Trả lại/giảm giá Quy đổi
				          
						0 AS DiscountOtherAmountOC  ,	--Chiết khấu TT/ giảm trừ khác
						0 AS DiscountOtherAmount  , --Chiết khấu TT/ giảm trừ khác quy đổi
				          
						0 AS ReceiptedAmountOC  ,	-- Số đã thu
						0 AS ReceiptedAmount  , -- Số đã thu quy đổi
				        
				        0 AS ClosingAmountOC  ,	-- Số dư cuối kỳ
						0 AS ClosingAmount  , -- Số dư cuối kỳ quy đổi
										          
						LAOI.AccountObjectGroupListCode , --Mã nhóm KH
						LAOI.AccountObjectGroupListName  --Tên nhóm KH   
				      
				 FROM    dbo.GeneralLedger AS SL
						INNER JOIN #tblListAccountObjectID AS LAOI ON SL.AccountObjectID = LAOI.AccountObjectID
						INNER JOIN #tblAccountNumber TBAN ON SL.AccountNumber = TBAN.AccountNumberDetail
						INNER JOIN #tblBrandIDList BIDL ON SL.BranchID = BIDL.BranchID
				 WHERE  SL.PostedDate < @Fromdate
						AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
						AND (@CurrencyID IS NULL OR SL.CurrencyID = @CurrencyID)
				 GROUP BY         
					LAOI.AccountObjectID ,
					LAOI.AccountObjectCode ,
					LAOI.AccountObjectName ,
					LAOI.AccountObjectAddress,
					LAOI.AccountObjectTaxcode ,
					LAOI.Mobile,
			        LAOI.AccountObjectGroupListCode , --Mã nhóm KH
				    LAOI.AccountObjectGroupListName , --Tên nhóm KH     
					TBAN.AccountNumber                                 
				UNION ALL
					/* Phát sinh trong kỳ */
				SELECT 
					LAOI.AccountObjectID ,
					LAOI.AccountObjectCode ,
					LAOI.AccountObjectName ,
					LAOI.AccountObjectAddress,
					LAOI.AccountObjectTaxcode,
					LAOI.Mobile,
					TBAN.AccountNumber,
					0 AS OpenDebitAmountOC,
					0 AS OpenDebitAmount,				            
					/*Số phải thu :Ghi tổng số tiền phát sinh Nợ nguyên tệ của TK phải thu chi tiết theo từng khách hàng trong khoảng thời gian xem báo cáo*/
					SUM(SL.DebitAmountOC) AS ReceiptAbleAmountOC ,
					SUM(SL.DebitAmount) AS ReceiptAbleAmount,
					 /*Chiết khấu
					  - Đối với QĐ 48,TT200:   = Tổng ps nợ 5211/có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					  - Đối với TT133 =  Tổng Phát sinh đối ứng nợ 511_chi tiết nghiệp vụ Chiết khấu thương mại/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					 */
					CASE WHEN @AccountingSystem = 15 OR @SubAccountSystem = 0 THEN 
							SUM(CASE 
								 WHEN SL.CorrespondingAccountNumber LIKE '5211%'
								 THEN SL.CreditAmountOC
								 ELSE 0
							END)
						ELSE
							SUM(CASE 
								 WHEN SL.CorrespondingAccountNumber LIKE '511%' AND SL.BusinessType = 0
								 THEN SL.CreditAmountOC
								 ELSE 0
							END)
					END AS DiscountAmountOC ,
						
					CASE WHEN @AccountingSystem = 15 OR @SubAccountSystem = 0 THEN 
							SUM(CASE 
								 WHEN SL.CorrespondingAccountNumber LIKE '5211%'
								 THEN SL.CreditAmount
								 ELSE 0
							END)
						ELSE
							SUM(CASE --WHEN SL.AccountNumber LIKE '5211%'
								 --THEN SL.CreditAmount
								 WHEN SL.CorrespondingAccountNumber LIKE '511%' AND SL.BusinessType = 0
								 THEN SL.CreditAmount
								 ELSE 0
							END)
					END AS DiscountAmount ,
						
					/* Giảm giá, trả lại
					- Đối với QĐ 48, TT200: = Tổng PS Nợ TK 5212, TK 5213, 33311/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					- Đối với TT 133: Tổng PS đối ứng Nợ TK 511_chi tiết nghiệp vụ Giảm giá hàng bán, trả lại hàng bán, 33311/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số nguyên tệ)
					* */
					CASE WHEN @AccountingSystem = 15 OR @SubAccountSystem = 0 THEN 
							SUM(CASE WHEN SL.CorrespondingAccountNumber LIKE '5212%'
									  OR SL.CorrespondingAccountNumber LIKE '5213%'
									  OR SL.CorrespondingAccountNumber LIKE '33311%'
								 THEN SL.CreditAmountOC
								 ELSE 0
							END)
						ELSE
							SUM(CASE WHEN (SL.CorrespondingAccountNumber LIKE '511%' AND SL.BusinessType IN (1, 2))
									  OR SL.CorrespondingAccountNumber LIKE '33311%'
								 THEN SL.CreditAmountOC
								 ELSE 0
							END)
					END AS ReturnAmountOC ,
						
					CASE WHEN @AccountingSystem = 15 OR @SubAccountSystem = 0 THEN 
							SUM(CASE WHEN SL.CorrespondingAccountNumber LIKE '5212%'
									  OR SL.CorrespondingAccountNumber LIKE '5213%'
									  OR SL.CorrespondingAccountNumber LIKE '33311%'
								 THEN SL.CreditAmount
								 ELSE 0
							END)
						ELSE
							SUM(CASE WHEN (SL.CorrespondingAccountNumber LIKE '511%' AND SL.BusinessType IN (1, 2))
									  OR SL.CorrespondingAccountNumber LIKE '33311%'
								 THEN SL.CreditAmount
								 ELSE 0
							END)
					END AS ReturnAmount ,
					/*  CK thanh toán/Giảm trừ khác quy đổi
				   - Đối với QĐ 48, TT 200:   =Tổng  PS nợ TK (không bao gồm các TK 11x, 5211,5212,5213, 33311/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số quy đổi)
					- Đối với TT 133:  = Tổng PS nợ TK (không bao gồm các TK 11x, 33311 và TK 511_chi tiết nghiệp vụ Chiết khấu thương mại, Giảm giá hàng bán, Trả lại hàng bán)/Có TK phải thu trên các chứng từ có ngày hạch toán nằm trong kỳ báo cáo của từng khách hàng (Lấy theo số quy đổi)
					* */
						CASE WHEN @AccountingSystem = 15 OR @SubAccountSystem = 0 THEN 
								( SUM(SL.CreditAmountOC)
								  - SUM(CASE 
											   WHEN SL.CorrespondingAccountNumber LIKE '5211%'
													OR SL.CorrespondingAccountNumber LIKE '5212%'
													OR SL.CorrespondingAccountNumber LIKE '5213%'
													OR SL.CorrespondingAccountNumber LIKE '33311%'
													OR SL.CorrespondingAccountNumber LIKE '11%'
											   THEN SL.CreditAmountOC
											   ELSE 0
										  END)
								  )
							ELSE
								( 
									SUM(SL.CreditAmountOC)
								  - SUM(CASE 
											   WHEN (SL.CorrespondingAccountNumber LIKE '511%' AND SL.BusinessType IN (0,1, 2))
													OR SL.CorrespondingAccountNumber LIKE '33311%'
													OR SL.CorrespondingAccountNumber LIKE '11%'
											   THEN SL.CreditAmountOC
											   ELSE 0
										  END)										  									  
								)
						END  AS DiscountOtherAmountOC,
						
					 CASE WHEN @AccountingSystem = 15 OR @SubAccountSystem = 0 THEN 
							( SUM(SL.CreditAmount)
							  - SUM(CASE 
										   WHEN SL.CorrespondingAccountNumber LIKE '5211%'
												OR SL.CorrespondingAccountNumber LIKE '5212%'
												OR SL.CorrespondingAccountNumber LIKE '5213%'
												OR SL.CorrespondingAccountNumber LIKE '33311%'
												OR SL.CorrespondingAccountNumber LIKE '11%'
										   THEN SL.CreditAmount
										   ELSE 0
									  END)
							)
						ELSE
							( 
								SUM(SL.CreditAmount)
							  - SUM(CASE 
										   WHEN (SL.CorrespondingAccountNumber LIKE '511%' AND SL.BusinessType IN (0,1, 2))
												OR SL.CorrespondingAccountNumber LIKE '33311%'
												OR SL.CorrespondingAccountNumber LIKE '11%'
										   THEN SL.CreditAmount
										   ELSE 0
										END)	
							)
						END AS DiscountOtherAmount,
						
						/*  Số đã thu
						 = Tổng PS Nợ TK 11x/Có TK phải thu tương ứng với từng khách hàng chọn xem báo cáo theo số tiền nguyên tệ trong khoảng thời gian xem báo cáo
		               
						* */
						SUM(CASE WHEN SL.CorrespondingAccountNumber LIKE '11%'
								 THEN SL.CreditAmountOC
								 ELSE 0
							END) ,
						SUM(CASE WHEN SL.CorrespondingAccountNumber LIKE '11%'
								 THEN SL.CreditAmount
								 ELSE 0
							END) ,
						0 ,
						0 ,
						LAOI.AccountObjectGroupListCode,
						LAOI.AccountObjectGroupListName
				FROM    dbo.GeneralLedger AS SL
						INNER  JOIN #tblListAccountObjectID AS LAOI ON SL.AccountObjectID = LAOI.AccountObjectID
						INNER JOIN #tblAccountNumber TBAN ON SL.AccountNumber = TBAN.AccountNumberDetail																	
						INNER JOIN #tblBrandIDList BIDL ON SL.BranchID = BIDL.BranchID
				WHERE   SL.PostedDate BETWEEN @Fromdate and @ToDate
						AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
						AND ( @CurrencyID IS NULL
							  OR SL.CurrencyID = @CurrencyID
							)
				GROUP BY 
				LAOI.AccountObjectID ,
				LAOI.AccountObjectCode ,
				LAOI.AccountObjectName ,
				LAOI.AccountObjectAddress,
				LAOI.AccountObjectTaxcode ,
			    LAOI.Mobile,
			    LAOI.AccountObjectGroupListCode , --Mã nhóm KH
		        LAOI.AccountObjectGroupListName , --Tên nhóm KH      
				TBAN.AccountNumber					 
			) AS A
			GROUP BY
				A.AccountObjectID ,
				A.AccountObjectCode ,
				A.AccountObjectName ,
				A.AccountObjectAddress ,
				A.AccountObjectTaxcode ,
				A.Mobile,
				A.AccountNumber,
				AccountObjectGroupListCode ,
				AccountObjectGroupListName 
				
			/*Tính số dư cuối kỳ*/
			
		UPDATE #tblResult
		SET ClosingAmountOC =  ISNULL(OpenDebitAmountOC,0) + ISNULL(ReceiptAbleAmountOC,0) - ISNULL(DiscountAmountOC,0) - ISNULL(ReturnAmountOC,0) - ISNULL(DiscountOtherAmountOC,0) - ISNULL(ReceiptedAmountOC,0),
			ClosingAmount = ISNULL(OpenDebitAmount,0) + ISNULL(ReceiptAbleAmount,0) - ISNULL(DiscountAmount,0)- ISNULL(ReturnAmount,0) - ISNULL(DiscountOtherAmount,0) - ISNULL(ReceiptedAmount,0)
					
	    
	
/*Lấy kết quả trả về*/			
   SELECT	AccountObjectID  ,
              AccountObjectCode ,   -- Mã KH
              AccountObjectName ,	-- Tên KH              
              AccountObjectAddress , -- Địa chỉ     
              AccountObjectTaxcode , -- Mã số thuế
              Mobile, -- Điện thoại
              AccountNumber   ,  -- Tài khoản
              OpenDebitAmountOC	,-- Số dư đầu kỳ
			  OpenDebitAmount, -- Dư đầu kỳ quy đổi
			  
              ReceiptAbleAmountOC ,	-- Phải thu
              ReceiptAbleAmount , -- Phải thu quy đổi
              
              DiscountAmountOC , -- Chiết khấu
              DiscountAmount , -- Chiết khấu quy đổia
              
              ReturnAmountOC , --Trả lại/Giảm giá
              ReturnAmount , --Trả lại/giảm giá Quy đổi
              
              DiscountOtherAmountOC ,	--Chiết khấu TT/ giảm trừ khác
              DiscountOtherAmount , --Chiết khấu TT/ giảm trừ khác quy đổi
              
              ReceiptedAmountOC ,	-- Số đã thu
              ReceiptedAmount , -- Số đã thu quy đổi
             
              ClosingAmountOC AS CloseAmountOC,	-- Số dư cuối kỳ
              ClosingAmount AS CloseAmount , -- Số dư cuối kỳ quy đổi
              
              AccountObjectGroupListCode , --Mã nhóm KH
              AccountObjectGroupListName 
   FROM   #tblResult   
   WHERE 
       OpenDebitAmountOC <>0 
	  OR OpenDebitAmount <> 0		
      OR ReceiptAbleAmountOC <> 0
      OR ReceiptAbleAmount <> 0
      OR DiscountAmountOC <> 0
      OR DiscountAmount <> 0
      OR ReturnAmountOC <> 0
      OR ReturnAmount <> 0
      OR DiscountOtherAmountOC <> 0
      OR DiscountOtherAmount <> 0
      OR ReceiptedAmountOC  <> 0
      OR ReceiptedAmount <> 0
      OR ClosingAmountOC <> 0
      OR ClosingAmount <> 0
      
		   ORDER BY AccountObjectCode,AccountObjectName, AccountNumber
       
 END

