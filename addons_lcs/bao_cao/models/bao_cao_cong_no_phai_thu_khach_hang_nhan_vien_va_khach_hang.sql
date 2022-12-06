--exec Proc_SAR_GetReceivableSummaryByEmployee @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@CurrencyID=N'VND',@ListEmployeeID=N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		NVTOAN
-- Create date: 19/11/2017
-- Description:	<Bán hàng: Lấy số liệu tổng hợp công nợ phải thu theo nhân viên>
-- nvtoan modify 28/01/2015: Lấy tài khoản chi tiết theo khách hàng
-- vhanh edited 25/08/2016: Sửa lại cách lấy số liệu theo CR 114658
-- =============================================

IF OBJECT_ID('tempdb..#Temp') IS NOT NULL
DROP TABLE #Temp;
IF OBJECT_ID('tempdb..#Branch') IS NOT NULL
DROP TABLE #Branch;
IF OBJECT_ID('tempdb..#EmployeeID') IS NOT NULL
DROP TABLE #EmployeeID;
IF OBJECT_ID('tempdb..#AccountObject') IS NOT NULL
DROP TABLE #AccountObject;
IF OBJECT_ID('tempdb..#AccountNumber') IS NOT NULL
DROP TABLE #AccountNumber;

DECLARE			@FromDate DATETIME
DECLARE			@ToDate DATETIME
DECLARE			@BranchID UNIQUEIDENTIFIER-- Chi nhánh
DECLARE			@IncludeDependentBranch BIT-- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(20)-- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX) -- Danh sách mã nhóm nhà cung cấp
DECLARE			@CurrencyID NVARCHAR(3)-- Loại tiền
DECLARE			@ListEmployeeID AS NVARCHAR(MAX) -- Danh sách mã nhân viên   
DECLARE			@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?

SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-05 23:59:59'
SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@AccountNumber=N'131'
SET			@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET			@CurrencyID=N'VND'
SET			@ListEmployeeID=N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,'
SET			@IsWorkingWithManagementBook=0

    BEGIN
	SET NOCOUNT ON

	/*Lấy bảng chi nhánh*/
	CREATE TABLE #Branch(
		BranchID UNIQUEIDENTIFIER PRIMARY KEY
		,BranchCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS
		,BranchName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS
	)	
	       
	INSERT  INTO #Branch
			SELECT  FGDBBI.BranchID
				   ,BranchCode
				   ,BranchName
			FROM    dbo.Func_GetDependentByBranchID(@BranchID, @IncludeDependentBranch) AS FGDBBI

	/*Lấy danh sách đối tượng*/
	CREATE TABLE #AccountObject(
		AccountObjectID UNIQUEIDENTIFIER
		,AccountObjectCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectAddress NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectTaxCode  NVARCHAR(50)
		,AccountObjectGroupListCode NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectGroupListName NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
		,Tel NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
	)

	IF @AccountObjectID = ','  OR @AccountObjectID IS NULL OR @AccountObjectID = 'SELECT_ALL' 
		INSERT INTO #AccountObject
		SELECT  AccountObjectID
			   ,AccountObjectCode
			   ,AccountObjectName
			   ,[Address]
			   ,CompanyTaxCode AS AccountObjectTaxCode
			   ,AccountObjectGroupListCode
			   ,AccountObjectGroupListName
			   ,CASE AccountObjectType WHEN 0 THEN Tel ELSE Mobile END AS Tel
		FROM    dbo.AccountObject
		WHERE   IsCustomer = 1
	ELSE 
		INSERT  INTO #AccountObject
		SELECT  AccountObjectID
			   ,AccountObjectCode
			   ,AccountObjectName
			   ,[Address]
			   ,CompanyTaxCode AS AccountObjectTaxCode
			   ,AccountObjectGroupListCode
			   ,AccountObjectGroupListName
			   ,CASE AccountObjectType WHEN 0 THEN Tel ELSE Mobile END AS Tel
		FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID, ',') FAO
				INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = FAO.Value   	
				
				
	/*Lấy danh sách nhân viên*/			
	CREATE TABLE #EmployeeID(
		EmployeeID UNIQUEIDENTIFIER, 
		EmployeeCode NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS, 
		EmployeeName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
	)

	INSERT  INTO #EmployeeID
	SELECT	AO.AccountObjectID, AO.AccountObjectCode, AO.AccountObjectName
	FROM	dbo.Func_ConvertGUIStringIntoTable(@ListEmployeeID, ',') F
			INNER JOIN dbo.AccountObject AO ON F.[Value] = AO.AccountObjectID 

	/*Lấy danh sách tài khoản*/ 
	CREATE TABLE #AccountNumber (
	  AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY ,
	  AccountName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
	  AccountNumberPercent NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS,
	  AccountCategoryKind INT
	)  
	IF @AccountNumber IS NOT NULL 
		INSERT  INTO #AccountNumber
		SELECT  A.AccountNumber ,
				A.AccountName ,
				A.AccountNumber + '%' ,
				A.AccountCategoryKind
		FROM    dbo.Account AS A
		WHERE   AccountNumber LIKE @AccountNumber + '%'
		ORDER BY A.AccountNumber, A.AccountName        
	ELSE 
	INSERT  INTO #AccountNumber
	SELECT  A.AccountNumber ,
			A.AccountName ,
			A.AccountNumber + '%' ,
			A.AccountCategoryKind
	FROM    dbo.Account AS A
	WHERE   DetailByAccountObject = 1
			AND AccountObjectType = 1
			AND IsParent = 0
	ORDER BY A.AccountNumber, A.AccountName
	    
    /*1. Tạo bảng tạm #DebtCrossEntry chứa những chứng từ công nợ đã đối trừ được lưu trong bảng liên kết đối trừ*/
	IF OBJECT_ID('tempdb..#DebtCrossEntry') IS NOT NULL DROP TABLE #DebtCrossEntry			
	CREATE TABLE #DebtCrossEntry(
		RefID UNIQUEIDENTIFIER
		,AccountObjectID UNIQUEIDENTIFIER
		,AccountNumber NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
		,CurrencyID NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS    
		,EmployeeID UNIQUEIDENTIFIER 
	) 
	INSERT  INTO #DebtCrossEntry(RefID, AccountObjectID, AccountNumber, CurrencyID, EmployeeID)
	SELECT	DISTINCT G.DebtRefID, G.AccountObjectID, G.AccountNumber, G.CurrencyID, G.DebtEmployeeID
	FROM    dbo.GLVoucherCrossEntryDetail G
			INNER JOIN #AccountNumber AC ON AC.AccountNumber = G.AccountNumber
			INNER JOIN #AccountObject AO ON AO.AccountObjectID = G.AccountObjectID
			INNER JOIN #Branch B ON B.BranchID = G.BranchID		
			/*Không lấy số dư đầu kỳ. Với số dư đầu kỳ lấy theo đúng thông tin trên tab chi tiết*/	
	WHERE	G.DebtRefType NOT IN (612,613,614)

	/*2. Tạo bảng tạm #PayCrossEntry chứa chứng từ thanh toán lấy dữ liệu từ bảng liên kết đối trừ, hàng bản trả lại, hàng bán giảm giá*/
	IF OBJECT_ID('tempdb..#PayCrossEntry') IS NOT NULL DROP TABLE #PayCrossEntry			
	CREATE TABLE #PayCrossEntry(
		CrossEntryID INT PRIMARY KEY IDENTITY(1, 1)
		,RefID UNIQUEIDENTIFIER
		,AccountObjectID UNIQUEIDENTIFIER
		,AccountNumber NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
		,CurrencyID NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS    
		,EmployeeID UNIQUEIDENTIFIER
		,PayAmountOC DECIMAL(22,8)
		,PayAmount DECIMAL(22,8)
		,DebtRefID UNIQUEIDENTIFIER
		,DebtPostedDate DATETIME
		,DebtRefNo NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
		,DebtInvNo NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
	) 
	INSERT  INTO #PayCrossEntry(RefID,AccountObjectID,AccountNumber,CurrencyID,EmployeeID,PayAmountOC,PayAmount,DebtRefID,DebtPostedDate,DebtRefNo,DebtInvNo)
    SELECT  G.PayRefID     
			,G.AccountObjectID      
           ,G.AccountNumber
           ,G.CurrencyID
           ,G.DebtEmployeeID
           ,SUM(G.PayAmountOC)
           /*Với đối trừ có chênh lệch thì tính thêm cả số tiền chênh lệch vào*/
           ,SUM(CASE WHEN G.CrossType = 0 THEN G.PayAmount - G.ExchangeDiffAmount ELSE G.PayAmount END)
           ,NULL
           ,G.DebtPostedDate
           ,G.DebtRefNo
           ,G.DebtInvNo           
	FROM    dbo.GLVoucherCrossEntryDetail G
			INNER JOIN #AccountNumber AC ON AC.AccountNumber = G.AccountNumber
			INNER JOIN #AccountObject AO ON AO.AccountObjectID = G.AccountObjectID
			INNER JOIN #Branch B ON B.BranchID = G.BranchID
	GROUP BY G.PayRefID, G.AccountObjectID, G.AccountNumber, G.CurrencyID, G.DebtRefNo , G.DebtEmployeeID,G.DebtPostedDate,G.DebtInvNo
	UNION ALL
	/*Lấy hàng bán trả lại*/
	SELECT	SARD.RefID,AL.AccountObjectID,AL.AccountNumber,AL.CurrencyID,SAV.EmployeeID,SUM(AL.CreditAmountOC) AS PayAmountOC,SUM(AL.CreditAmount) AS PayAmount, SAV.RefID, SAV.PostedDate, SAV.RefNoFinance, SAV.InvNo
	FROM	dbo.SAReturnDetail SARD
			INNER JOIN dbo.AccountObjectLedger AL ON SARD.RefDetailID = AL.RefDetailID
			INNER JOIN dbo.SAVoucher SAV ON SAV.RefID = SARD.SAVoucherRefID			
			INNER JOIN #AccountNumber AC ON AC.AccountNumber = AL.AccountNumber
			INNER JOIN #AccountObject AO ON AO.AccountObjectID = AL.AccountObjectID
			INNER JOIN #Branch B ON B.BranchID = AL.BranchID
	WHERE	SARD.SAVoucherRefID IS NOT NULL
	GROUP BY SARD.RefID,AL.AccountObjectID,AL.AccountNumber,AL.CurrencyID,SAV.EmployeeID, SAV.RefID, SAV.PostedDate, SAV.RefNoFinance, SAV.InvNo
	UNION ALL
	/*Lấy hàng bán giảm giá*/
	SELECT	SARD.RefID,AL.AccountObjectID,AL.AccountNumber,AL.CurrencyID,SAV.EmployeeID,SUM(AL.CreditAmountOC) AS PayAmountOC,SUM(AL.CreditAmount) AS PayAmount, SAV.RefID, SAV.PostedDate, SAV.RefNoFinance, SAV.InvNo
	FROM	dbo.SADiscountDetail SARD
			INNER JOIN dbo.AccountObjectLedger AL ON SARD.RefDetailID = AL.RefDetailID
			INNER JOIN dbo.SAVoucher SAV ON SAV.RefID = SARD.SAVoucherRefID			
			INNER JOIN #AccountNumber AC ON AC.AccountNumber = AL.AccountNumber
			INNER JOIN #AccountObject AO ON AO.AccountObjectID = AL.AccountObjectID
			INNER JOIN #Branch B ON B.BranchID = AL.BranchID
	WHERE	SARD.SAVoucherRefID IS NOT NULL
	GROUP BY SARD.RefID,AL.AccountObjectID,AL.AccountNumber,AL.CurrencyID,SAV.EmployeeID, SAV.RefID, SAV.PostedDate, SAV.RefNoFinance, SAV.InvNo


	/*Tạo bảng chứa kết quả*/
	CREATE	TABLE #Temp(
		EmployeeID UNIQUEIDENTIFIER
		,AccountObjectID UNIQUEIDENTIFIER		
		,AccountObjectCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectAddress NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectTaxCode  NVARCHAR(50)
		,AccountObjectGroupListCode NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
		,AccountObjectGroupListName NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
		,Tel NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
		,RefID UNIQUEIDENTIFIER
		,RefType INT
		,PostedDate DATETIME
		,RefDate DATETIME
		,RefNo NVARCHAR(22) COLLATE SQL_Latin1_General_CP1_CI_AS
		,InvDate DATETIME
		,InvNo NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
		,RefDetailID UNIQUEIDENTIFIER
		,DebtRefID UNIQUEIDENTIFIER
		,LedgerID INT				
		,AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS    
		,CurrencyID NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS    		
		,DebitAmountOC MONEY
		,DebitAmount MONEY
		,CreditAmountOC MONEY
		,CreditAmount MONEY
		,IsCrossRow BIT DEFAULT (0)							
		,CrossAmount MONEY DEFAULT (0)
		,CrossAmountOC MONEY DEFAULT (0)	
		,OrderType INT	
	)
	
	/*BTAnh - 05.08.2016: Bổ sung Index để tăng tốc độ khi sử dụng trong cursor*/
	CREATE CLUSTERED INDEX [IX_Clusted_Temp_Composite] ON #Temp
	(
		RefID ASC,
		AccountObjectID ASC,
		AccountNumber ASC,
		CurrencyID ASC
	)
	WITH (STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
	

	/*3 - 4. Lấy dữ liệu vào bảng tạm và lấy phần đối trừ*/	
	INSERT INTO #Temp(EmployeeID, AccountObjectID,AccountObjectCode,AccountObjectName,AccountObjectAddress,
					AccountObjectTaxCode,AccountObjectGroupListCode,AccountObjectGroupListName,Tel, RefID, RefType,PostedDate, RefDate, RefNo, 
					InvDate, InvNo, RefDetailID, DebtRefID, LedgerID,AccountNumber,
					CurrencyID, DebitAmountOC,DebitAmount, CreditAmountOC, CreditAmount,OrderType)
	SELECT	T.*
	FROM	(	
		SELECT ISNULL(GD.EmployeeID, AL.EmployeeID) AS EmployeeID
			   ,AL.AccountObjectID
			   ,AO.AccountObjectCode
			   ,AO.AccountObjectName
			   ,AO.AccountObjectAddress
			   ,AO.AccountObjectTaxCode
			   ,AO.AccountObjectGroupListCode
			   ,AO.AccountObjectGroupListName
			   ,AO.Tel			   
			   ,AL.RefID
			   ,AL.RefType
			   ,AL.PostedDate
			   ,AL.RefDate
			   ,AL.RefNo
			   ,AL.InvDate
			   ,AL.InvNo
			   ,AL.RefDetailID
			   ,SA.SAVoucherRefID AS DebtRefID
			   ,AL.AccountObjectLedgerID AS LedgerID			   		
			   ,AL.AccountNumber
			   ,AL.CurrencyID
			   ,AL.DebitAmountOC
			   ,AL.DebitAmount
			   ,AL.CreditAmountOC
			   ,AL.CreditAmount			   
			   ,1 AS OrderType		   			  		
		FROM    AccountObjectLedger Al
				INNER JOIN #AccountObject AO ON AO.AccountObjectID = Al.AccountObjectID
				INNER JOIN #Branch B ON B.BranchID = Al.BranchID
				INNER JOIN #AccountNumber AC ON AC.AccountNumber = Al.AccountNumber							
				LEFT JOIN #DebtCrossEntry GD ON AL.RefID = GD.RefID AND AL.AccountNumber = GD.AccountNumber AND AL.AccountObjectID = GD.AccountObjectID AND AL.CurrencyID = GD.CurrencyID
				LEFT JOIN (
					SELECT SAR.RefDetailID, SAR.SAVoucherRefID FROM dbo.SAReturnDetail SAR WHERE SAR.SAVoucherRefID IS NOT NULL
					UNION ALL
					SELECT SAD.RefDetailID, SAD.SAVoucherRefID FROM dbo.SADiscountDetail SAD WHERE SAD.SAVoucherRefID IS NOT NULL
				) SA ON AL.RefDetailID = SA.RefDetailID				
		WHERE   (AL.PostedDate BETWEEN @FromDate AND @ToDate)
				AND AL.IsPostToManagementBook = @IsWorkingWithManagementBook
				AND (AL.CurrencyID = @CurrencyID OR @CurrencyID IS NULL)
				AND (AL.DebitAmountOC <> 0 OR AL.DebitAmount <> 0 OR AL.CreditAmountOC <> 0 OR AL.CreditAmount <> 0)
		UNION ALL
		/*Số dư đầu kỳ*/      
		SELECT	ISNULL(GD.EmployeeID, AL.EmployeeID) AS EmployeeID		
				,AL.AccountObjectID		
				,AO.AccountObjectCode
			    ,AO.AccountObjectName
			    ,AO.AccountObjectAddress
				,AO.AccountObjectTaxCode
			    ,AO.AccountObjectGroupListCode
			    ,AO.AccountObjectGroupListName
			    ,AO.Tel			   			
				,AL.RefID
				,NULL AS RefType			
				,NULL AS PostedDate
				,NULL AS RefDate			
				,NULL AS RefNo
				,NULL AS InvDate
				,NULL AS InvNo
				,AL.RefDetailID
				,SA.SAVoucherRefID AS DebtRefID
				,AL.AccountObjectLedgerID AS LedgerID				
				,AL.AccountNumber
				,AL.CurrencyID				
				,AL.DebitAmountOC
				,AL.DebitAmount
				,AL.CreditAmountOC
				,AL.CreditAmount				
				,0 AS OrderType											
		FROM 	AccountObjectLedger Al
				INNER JOIN #AccountObject AO ON AO.AccountObjectID = Al.AccountObjectID
				INNER JOIN #Branch B ON B.BranchID = Al.BranchID				
				INNER JOIN #AccountNumber AC ON AC.AccountNumber = Al.AccountNumber			
				LEFT JOIN #DebtCrossEntry GD ON AL.RefID = GD.RefID AND AL.AccountNumber = GD.AccountNumber AND AL.AccountObjectID = GD.AccountObjectID AND AL.CurrencyID = GD.CurrencyID
				LEFT JOIN (
					SELECT SAR.RefDetailID, SAR.SAVoucherRefID FROM dbo.SAReturnDetail SAR WHERE SAR.SAVoucherRefID IS NOT NULL
					UNION ALL
					SELECT SAD.RefDetailID, SAD.SAVoucherRefID FROM dbo.SADiscountDetail SAD WHERE SAD.SAVoucherRefID IS NOT NULL
				) SA ON AL.RefDetailID = SA.RefDetailID					
		WHERE	AL.PostedDate < @FromDate
				AND AL.IsPostToManagementBook = @IsWorkingWithManagementBook
				AND (AL.CurrencyID = @CurrencyID OR @CurrencyID IS NULL)
				AND (AL.DebitAmountOC <> 0 OR AL.DebitAmount <> 0 OR AL.CreditAmountOC <> 0 OR AL.CreditAmount <> 0)
	) T	
	ORDER BY	T.RefID, T.AccountObjectID, T.CurrencyID, T.AccountNumber,  T.RefDetailID               

	/*5. Tính toán cộng đuổi cho chứng từ thanh toán để tính số tiền đã đối trừ và số tiền còn lại*/
	DECLARE @PayRefID UNIQUEIDENTIFIER, @PayAccountObject UNIQUEIDENTIFIER, @PayEmployee UNIQUEIDENTIFIER, @PayAccountNumber NVARCHAR(25), @PayCurrency NVARCHAR(25), @PayAmount MONEY, @PayAmountOC MONEY, @DebtRefID UNIQUEIDENTIFIER
	DECLARE cur CURSOR FAST_FORWARD READ_ONLY FOR
		SELECT	GP.RefID, GP.AccountObjectID, GP.EmployeeID, GP.AccountNumber, GP.CurrencyID, GP.PayAmount, GP.PayAmountOC, GP.DebtRefID
		FROM	#PayCrossEntry GP
		WHERE	GP.RefID IN (SELECT T.RefID FROM #Temp T WHERE T.CreditAmountOC > 0 OR T.CreditAmount > 0 )	
		ORDER BY GP.DebtPostedDate, GP.DebtRefNo, GP.DebtInvNo
	OPEN cur			
	FETCH NEXT FROM cur INTO @PayRefID, @PayAccountObject, @PayEmployee, @PayAccountNumber, @PayCurrency, @PayAmount, @PayAmountOC, @DebtRefID
	WHILE (@@FETCH_STATUS = 0) 
	BEGIN
        DECLARE @LedgerID INT
           ,@CrossAmountOC MONEY
           ,@CrossAmount MONEY
           ,@OldRemainAmountOC MONEY
           ,@OldRemainAmount MONEY
           ,@RemainAmountOC MONEY
           ,@RemainAmount MONEY
        SET @LedgerID = NULL
		SET @CrossAmountOC = 0
		SET @CrossAmount = 0
		SET @OldRemainAmountOC = 0
		SET @OldRemainAmount = 0  
		SET @RemainAmountOC = 0
		SET @RemainAmount = 0
								
		UPDATE #Temp
		SET	     @OldRemainAmount = (CASE WHEN ISNULL(@LedgerID,0) <> LedgerID THEN CreditAmount ELSE @RemainAmount END)
				,@OldRemainAmountOC = (CASE WHEN ISNULL(@LedgerID,0) <> LedgerID THEN CreditAmountOC ELSE @RemainAmountOC END)
				
				,@CrossAmount = (CASE WHEN @OldRemainAmount < @PayAmount THEN @OldRemainAmount ELSE @PayAmount END)
				,@CrossAmountOC = (CASE WHEN @OldRemainAmountOC < @PayAmountOC THEN @OldRemainAmountOC ELSE @PayAmountOC END)
				
				,@RemainAmount = @OldRemainAmount - @CrossAmount
			    ,@RemainAmountOC = @OldRemainAmountOC - @CrossAmountOC
			    
				,CrossAmount = @CrossAmount
				,CrossAmountOC = @CrossAmountOC				
				,CreditAmount =  @RemainAmount
				,CreditAmountOC =  @RemainAmountOC  
								
				,@PayAmount = @PayAmount - @CrossAmount
				,@PayAmountOC = @PayAmountOC - @CrossAmountOC
				
				,@LedgerID = LedgerID
		WHERE	RefID = @PayRefID
				AND AccountObjectID = @PayAccountObject
				AND AccountNumber = @PayAccountNumber
				AND CurrencyID = @PayCurrency
				AND ((DebtRefID IS NULL AND @DebtRefID IS NULL) OR (DebtRefID = @DebtRefID))
				AND IsCrossRow = 0		
					
		/*Nếu số tiền đối trừ > 0 và số tiền còn lại (CreditAmount = 0) thì update chuyển luôn dòng đó sang thành dòng mới*/
		UPDATE	#Temp
		SET		CreditAmount = CrossAmount
				,CreditAmountOC = CrossAmountOC
				,CrossAmount = 0
				,CrossAmountOC = 0
				,EmployeeID = ISNULL(@PayEmployee, EmployeeID)
				,IsCrossRow = 1
		WHERE	RefID = @PayRefID
				AND AccountObjectID = @PayAccountObject
				AND AccountNumber = @PayAccountNumber
				AND CurrencyID = @PayCurrency
				AND ((DebtRefID IS NULL AND @DebtRefID IS NULL) OR (DebtRefID = @DebtRefID))
				AND IsCrossRow = 0
				AND CreditAmountOC = 0 
				AND CreditAmount = 0 
				AND (CrossAmountOC <> 0 OR CrossAmount <> 0)				
		--/*Nếu số tiền đối trừ > 0 và số tiền còn lại (CreditAmount > 0) thì tách ra 1 dòng mới*/
		INSERT INTO #Temp(EmployeeID, AccountObjectID,AccountObjectCode,AccountObjectName,AccountObjectAddress			   			   
			   ,AccountObjectTaxCode,AccountObjectGroupListCode,AccountObjectGroupListName,Tel, RefID,
			   RefType, PostedDate, RefDate, RefNo, InvDate, InvNo,
		       RefDetailID, LedgerID, AccountNumber, CurrencyID,
		       DebitAmountOC, DebitAmount, CreditAmountOC, CreditAmount, IsCrossRow, OrderType)			   			   		            
        SELECT  ISNULL(@PayEmployee, EmployeeID) AS EmployeeID
               ,AccountObjectID
			   ,AccountObjectCode
			   ,AccountObjectName
			   ,AccountObjectAddress
			   ,AccountObjectTaxCode
			   ,AccountObjectGroupListCode
			   ,AccountObjectGroupListName
			   ,Tel               
               ,RefID
               ,RefType
               ,PostedDate
               ,RefDate
               ,RefNo
               ,InvDate
               ,InvNo
               ,RefDetailID
               ,LedgerID               
               ,AccountNumber
               ,CurrencyID               
               ,DebitAmountOC
               ,DebitAmount
               ,CrossAmountOC
               ,CrossAmount
               ,1 AS IsCrossRow    
			   ,OrderType                                 
        FROM    #Temp
        WHERE	RefID = @PayRefID
				AND AccountObjectID = @PayAccountObject
				AND AccountNumber = @PayAccountNumber
				AND CurrencyID = @PayCurrency
				AND ((DebtRefID IS NULL AND @DebtRefID IS NULL) OR (DebtRefID = @DebtRefID))
				AND IsCrossRow = 0
				AND (CreditAmountOC <> 0 OR CreditAmount <> 0 )
				AND (CrossAmountOC <> 0 OR CrossAmount <> 0)			
		/*Nếu số tiền đối trừ = 0 thì không làm gì. Reset số tiền đối trừ*/
		UPDATE  #Temp
		SET		CrossAmount = 0
				,CrossAmountOC = 0
		WHERE	RefID = @PayRefID
				AND AccountObjectID = @PayAccountObject
				AND AccountNumber = @PayAccountNumber
				AND CurrencyID = @PayCurrency
				AND ((DebtRefID IS NULL AND @DebtRefID IS NULL) OR (DebtRefID = @DebtRefID))
				AND IsCrossRow = 0
							                	
		FETCH NEXT FROM cur INTO @PayRefID, @PayAccountObject, @PayEmployee, @PayAccountNumber, @PayCurrency, @PayAmount, @PayAmountOC, @DebtRefID
	END
	CLOSE cur
	DEALLOCATE cur

	/*SELECT * FROM  #Temp
	WHERE OrderType = 0	
	*/

	/*6. Tính tổng lấy được số dư đầu kỳ, phát sinh và số dư cuối kỳ*/
	SELECT  ROW_NUMBER() OVER (ORDER BY EmployeeCode, AccountObjectCode) AS RowNum
			,R.EmployeeID
			,E.EmployeeCode
			,E.EmployeeName			
			,R.AccountNumber
			,R.AccountObjectID
            ,R.AccountObjectCode  
            ,R.AccountObjectName    
            ,R.AccountObjectAddress
            ,R.AccountObjectTaxCode
			,R.AccountObjectGroupListCode
			,R.AccountObjectGroupListName AS AccountObjectCategoryName
            ,R.Tel
			,AC.AccountCategoryKind	
			/*Sửa bug 114938: Lỗi số dư đầu kỳ đang hiển thị không đúng trường hợp có cả PS Nợ và Có*/		   			   			
			,(CASE WHEN (AccountCategoryKind = 0 OR (AccountCategoryKind = 2 AND SUM(CASE WHEN R.OrderType = 0 THEN (DebitAmount - CreditAmount) ELSE 0 END) >= 0)) 
						THEN SUM(CASE WHEN R.OrderType = 0 THEN (DebitAmount - CreditAmount) ELSE 0 END)
				   ELSE 0 
			 END) AS OpenningDebitAmount
			,(CASE WHEN (AccountCategoryKind = 0 OR (AccountCategoryKind = 2 AND SUM(CASE WHEN R.OrderType = 0 THEN (DebitAmountOC - CreditAmountOC) ELSE 0 END) >= 0)) 
						THEN SUM(CASE WHEN R.OrderType = 0 THEN (DebitAmountOC - CreditAmountOC) ELSE 0 END)
				   ELSE 0 
			  END)  AS OpenningDebitAmountOC
			,(CASE WHEN (AccountCategoryKind = 1 OR (AccountCategoryKind = 2 AND SUM(CASE WHEN R.OrderType = 0 THEN (CreditAmount - DebitAmount) ELSE 0 END) >= 0)) 
						THEN SUM(CASE WHEN R.OrderType = 0 THEN (CreditAmount - DebitAmount)ELSE 0 END)
				   ELSE 0 
			  END) AS OpenningCreditAmount
			,(CASE WHEN (AccountCategoryKind = 1 OR (AccountCategoryKind = 2 AND SUM(CASE WHEN R.OrderType = 0 THEN (CreditAmountOC - DebitAmountOC) ELSE 0 END) >= 0)) 
						THEN SUM(CASE WHEN R.OrderType = 0 THEN (CreditAmountOC - DebitAmountOC) ELSE 0 END)
				   ELSE 0 
			  END) AS OpenningCreditAmountOC

			,SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.DebitAmount,0) ELSE 0 END) AS DebitAmount
			,SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.DebitAmountOC,0) ELSE 0 END) AS DebitAmountOC
			,SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.CreditAmount,0) ELSE 0 END) AS CreditAmount
			,SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.CreditAmountOC,0) ELSE 0 END) AS CreditAmountOC

			,(CASE WHEN AccountCategoryKind = 0 OR (AccountCategoryKind = 2 AND SUM(DebitAmount - CreditAmount) >= 0) THEN SUM(DebitAmount - CreditAmount) ELSE 0 END) AS CloseDebitAmount
			,(CASE WHEN AccountCategoryKind = 0 OR (AccountCategoryKind = 2 AND SUM(DebitAmountOC - CreditAmountOC)>= 0) THEN SUM(DebitAmountOC - CreditAmountOC) ELSE 0 END) AS CloseDebitAmountOC
			,(CASE WHEN AccountCategoryKind = 1 OR (AccountCategoryKind = 2 AND SUM(CreditAmount - DebitAmount) >= 0) THEN SUM(CreditAmount - DebitAmount) ELSE 0 END) AS CloseCreditAmount
			,(CASE WHEN AccountCategoryKind = 1 OR (AccountCategoryKind = 2 AND SUM(CreditAmountOC - DebitAmountOC) >= 0) THEN SUM(CreditAmountOC - DebitAmountOC) ELSE 0 END) AS CloseCreditAmountOC

	FROM    #Temp R
			INNER JOIN #EmployeeID E ON E.EmployeeID = R.EmployeeID
			INNER JOIN dbo.Account AC ON AC.AccountNumber = R.AccountNumber
	GROUP BY R.EmployeeID
			,E.EmployeeCode
			,E.EmployeeName			  
			,R.AccountNumber
			,R.AccountObjectID
            ,R.AccountObjectCode  
            ,R.AccountObjectName    
            ,R.AccountObjectAddress
            ,R.AccountObjectTaxCode
			,R.AccountObjectGroupListCode
			,R.AccountObjectGroupListName
            ,R.Tel
			,AC.AccountCategoryKind				        					   			
	HAVING  SUM(CASE WHEN R.OrderType = 0 THEN (DebitAmount - CreditAmount) ELSE 0 END) <> 0
		    OR SUM(CASE WHEN R.OrderType = 0 THEN (DebitAmountOC - CreditAmountOC) ELSE 0 END) <> 0
			OR SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.DebitAmount,0) ELSE 0 END) <> 0
			OR SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.DebitAmountOC,0) ELSE 0 END) <> 0
			OR SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.CreditAmount,0) ELSE 0 END) <> 0
			OR SUM(CASE WHEN R.OrderType = 1 THEN ISNULL(R.CreditAmountOC,0) ELSE 0 END) <> 0
	ORDER BY E.EmployeeCode, R.AccountObjectCode
    END
    

