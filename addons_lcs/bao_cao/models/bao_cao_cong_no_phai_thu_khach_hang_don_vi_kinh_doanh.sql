--exec Proc_SAR_GetReceivableSummaryByOU @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-15 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@CurrencyID=N'VND',@OrganizationUnitID=N',07957793-f914-4097-abf3-aa8251c53bdc,1b65fcd3-07e7-4fa5-b75a-c229f5d96368,9f75f5d4-5213-4432-9d30-0da0ce72d52b,b88f22a4-4cb7-4077-9414-b703cd81176f,c8b534fc-bdaf-4273-930a-33181b3e1d6f,',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		VHAnh
-- Create date: 03.10.2015
-- Description:	Tổng hợp công nợ phải thu khách hàng theo đơn vị kinh doanh
-- =============================================

DECLARE			@FromDate DATETIME
DECLARE			@ToDate DATETIME
DECLARE			@BranchID UNIQUEIDENTIFIER-- Chi nhánh
DECLARE			@IncludeDependentBranch BIT-- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(20)-- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX) -- Danh sách khách hàng
DECLARE			@CurrencyID NVARCHAR(3)-- Loại tiền
DECLARE			@OrganizationUnitID AS NVARCHAR(MAX) -- Danh sách mã đơn vị 
DECLARE			@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-15 23:59:59'
SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@AccountNumber=N'131'
SET			@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET			@CurrencyID=N'VND'
SET			@OrganizationUnitID=N',07957793-f914-4097-abf3-aa8251c53bdc,1b65fcd3-07e7-4fa5-b75a-c229f5d96368,9f75f5d4-5213-4432-9d30-0da0ce72d52b,b88f22a4-4cb7-4077-9414-b703cd81176f,c8b534fc-bdaf-4273-930a-33181b3e1d6f,'
SET			@IsWorkingWithManagementBook=0

    BEGIN
        DECLARE @tblBrandIDList TABLE
            (
             BranchID UNIQUEIDENTIFIER
            )	
       
        INSERT  INTO @tblBrandIDList
                SELECT  FGDBBI.BranchID
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI
               
               
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các khách hàng
            (
             AccountObjectID UNIQUEIDENTIFIER,
             AccountObjectGroupListCode NVARCHAR(MAX),
             AccountObjectCategoryName NVARCHAR(MAX),
             Tel NVARCHAR(50)
            ) 
            
        IF @AccountObjectID = ',' OR @AccountObjectID = NULL
        BEGIN
			INSERT @tblListAccountObjectID
			 SELECT		AO.AccountObjectID,
                        AO.AccountObjectGroupListCode, -- Mã nhóm khách hàng
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName, -- tên nhóm khách hàng
                        CASE ao.AccountObjectType
                          WHEN 0 THEN AO.Tel
                          ELSE ao.Mobile
                        END AS Tel
                FROM   dbo.AccountObject AS AO where IsCustomer = 1
        END
        ELSE
        BEGIN
        INSERT  INTO @tblListAccountObjectID
                SELECT  TLAO.Value AS AccountObjectID,
                        AO.AccountObjectGroupListCode, -- Mã nhóm khách hàng
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName, -- tên nhóm khách hàng
                        CASE ao.AccountObjectType
                          WHEN 0 THEN AO.Tel
                          ELSE ao.Mobile
                        END AS Tel
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') AS TLAO
                        INNER JOIN AccountObject AS AO ON AO.AccountObjectID = TLAO.Value  	        			
        END
        
     --  	 CREATE TABLE #tblOrganizationUnit -- Bảng đơn vị
     --       (
     --         OrganizationUnitID UNIQUEIDENTIFIER PRIMARY KEY ,
     --         OrganizationUnitCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
     --         OrganizationUnitName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
			  --MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
     --         Grade INT ,
     --         SortMISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
     --       )                       
     --   IF @OrganizationUnitID IS NOT NULL 
     --       INSERT  INTO #tblOrganizationUnit
     --               SELECT  OrganizationUnitID ,
     --                       OrganizationUnitCode ,
     --                       OrganizationUnitName,
					--		OU.MISACodeID ,
     --                       OU.Grade ,
     --                       OU.SortMISACodeID
     --                FROM    dbo.Func_ConvertGUIStringIntoTable(@OrganizationUnitID,',') F
     --                       INNER JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = F.Value             
        
		                             
     --   CREATE TABLE #tblListOrganizationUnit-- Bảng đơn vị gồm toàn bộ đơn vị con
     --       (
     --         OrganizationUnitID UNIQUEIDENTIFIER ,
			  --OrganizationUnitCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
     --         OrganizationUnitName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
     --         MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
     --       ) 
     --   INSERT  INTO #tblListOrganizationUnit
     --           SELECT    DISTINCT
     --                   OU.OrganizationUnitID ,
					--	OU.OrganizationUnitCode ,
     --                   OU.OrganizationUnitName,
     --                   OU.MISACodeID
     --           FROM    #tblOrganizationUnit tOU
     --                   LEFT JOIN dbo.OrganizationUnit OU ON OU.MISACodeID LIKE tOU.MISACodeID + '%' 	
	 
	  /*bảng chứa tham số đơn vị truyền vào ban đầu*/
        DECLARE @tblOrganizationUnitID TABLE-- 
            (
              OrganizationUnitID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS
                                       NULL ,
              OrganizationUnitCode NVARCHAR(20)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL ,
              OrganizationUnitName NVARCHAR(128)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL ,
              SortMISACodeID NVARCHAR(100)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL
              ,IsParent BIT
              ,IsParentWithChild BIT
            ) 
        INSERT  INTO @tblOrganizationUnitID /*Insert*/
                SELECT DISTINCT
                        EI.OrganizationUnitID ,
                        EI.MISACodeID ,
                        EI.OrganizationUnitCode ,
                        EI.OrganizationUnitName ,
                        EI.SortMISACodeID,
                        EI.IsParent,
                        0                        
                FROM    dbo.Func_ConvertGUIStringIntoTable(@OrganizationUnitID,
                                                           ',') tString
                        INNER JOIN dbo.OrganizationUnit EI ON EI.OrganizationUnitID = tString.Value
                        
        /*Cập nhật lại bảng đầu vào xem đơn vị truyền vào có con hay là không có con được chọn trên tham số để mục đích lấy số liệu trong TH 
        + nếu chọn con và cha thì lấy số liệu của đơn vị cha= phát sinh trực tiếp của đơn vị cha và các con được chọn, 
        + nếu  không chọn đơn vị cha thì sẽ lấy số liệu của tất cả các con cộng lên */
        UPDATE T 
        SET IsParentWithChild = 1
        FROM @tblOrganizationUnitID T
        INNER JOIN @tblOrganizationUnitID T1 ON T1.MISACodeID LIKE T.MISACodeID + '%' AND T.MISACodeID <> T1.MISACodeID
        WHERE T.IsParent = 1				
          

		  

        --SELECT * FROM   @tblOrganizationUnitID     
        DECLARE @tblOrganizationUnitID1 TABLE-- Bảng khoản mục CP khong có node không chọn
            (
              OrganizationUnitID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS
                                       NULL
            ) 
        INSERT  @tblOrganizationUnitID1
                SELECT  S.OrganizationUnitID ,
                        S.MISACodeID
                FROM    @tblOrganizationUnitID S
                        LEFT  JOIN @tblOrganizationUnitID S1 ON S1.MISACodeID LIKE S.MISACodeID
                                                              + '%'
                                                              AND S.MISACodeID <> S1.MISACodeID
                WHERE   S1.MISACodeID IS NULL 
        DECLARE @tblListOrganizationUnitID TABLE-- Bảng khoản mục CP gồm toàn bộ khoản mục CP con
            (
              OrganizationUnitID UNIQUEIDENTIFIER ,
              MISACodeID NVARCHAR(100)
            )                     
		   
        INSERT  INTO @tblListOrganizationUnitID
                SELECT DISTINCT
                        T.OrganizationUnitID ,
                        T.MISACodeID
                FROM    ( SELECT  DISTINCT
                                    EI.OrganizationUnitID ,
                                    EI.MISACodeID
                          FROM      dbo.OrganizationUnit EI
                                    INNER JOIN @tblOrganizationUnitID1 SEI ON EI.MISACodeID LIKE SEI.MISACodeID                           + '%'
                          UNION ALL
                          SELECT    EI.OrganizationUnitID ,
                                    EI.MISACodeID
                          FROM      @tblOrganizationUnitID EI
                        ) T
                           														                      
        -- Bảng chứa số tài khoản    
        DECLARE @tblAccountNumber TABLE
            (
             AccountNumber NVARCHAR(20) PRIMARY KEY,
             AccountName NVARCHAR(255),
             AccountNumberPercent NVARCHAR(25),
             AccountCategoryKind INT
            )
        IF @AccountNumber IS NOT NULL
            BEGIN
                INSERT  INTO @tblAccountNumber
                        SELECT  A.AccountNumber,
                                A.AccountName,
                                A.AccountNumber + '%',
                                A.AccountCategoryKind
                        FROM    dbo.Account AS A
                        WHERE   AccountNumber = @AccountNumber
                                AND DetailByAccountObject = 1
                        ORDER BY A.AccountNumber,
                                A.AccountName 
                
            END
        ELSE
            BEGIN 
                INSERT  INTO @tblAccountNumber
                        SELECT  A.AccountNumber,
                                A.AccountName,
                                A.AccountNumber + '%',
                                A.AccountCategoryKind
                        FROM    dbo.Account AS A
                        WHERE   DetailByAccountObject = 1
                        AND AccountObjectType = 1
                                AND IsParent = 0
                        ORDER BY  A.AccountNumber,
                                A.AccountName
            END
	    



        SELECT  ROW_NUMBER() OVER (ORDER BY P.OrganizationUnitCode, AccountObjectCode) AS RowNum,
                 P.OrganizationUnitID ,
                P.OrganizationUnitCode AS OrganizationUnitCode ,
                P.OrganizationUnitName AS OrganizationUnitName ,
				--OrganizationUnitID,
    --            OrganizationUnitCode, -- Mã đơn vị
				--OrganizationUnitName, -- Tên đơn vị
                AccountObjectID,
                AccountObjectCode,   -- Mã khách hàng
                AccountObjectName,	-- Tên khách hàng              
                AccountObjectAddress, -- Địa chỉ
                AccountObjectTaxCode,
                Tel,
                AccountNumber, -- Số tài khoản
                AccountCategoryKind, -- Tính chất tài khoản
                (CASE WHEN AccountCategoryKind = 0/*nếu dư nợ*/
                      THEN SUM(OpenningDebitAmountOC)
                           - SUM(OpenningCreditAmountOC)
                      WHEN AccountCategoryKind = 1 THEN $0/*dư có*/
                      ELSE CASE WHEN (SUM(OpenningDebitAmountOC /*lưỡng tính*/
                                          - OpenningCreditAmountOC)) > 0
                                THEN (SUM(OpenningDebitAmountOC
                                          - OpenningCreditAmountOC))
                                ELSE $0
                           END
                 END) AS OpenningDebitAmountOC,	-- Dư nợ Đầu kỳ           
                (CASE WHEN AccountCategoryKind = 0
                      THEN (SUM(OpenningDebitAmount - OpenningCreditAmount))
                      WHEN AccountCategoryKind = 1 THEN $0
                      ELSE CASE WHEN (SUM(OpenningDebitAmount
                                          - OpenningCreditAmount)) > 0
                                THEN SUM(OpenningDebitAmount
                                         - OpenningCreditAmount)
                                ELSE $0
                           END
                 END) AS OpenningDebitAmount, -- Dư nợ Đầu kỳ quy đổi
                (CASE WHEN AccountCategoryKind = 1
                      THEN (SUM(OpenningCreditAmountOC - OpenningDebitAmountOC))
                      WHEN AccountCategoryKind = 0 THEN $0
                      ELSE CASE WHEN (SUM(OpenningCreditAmountOC
                                          - OpenningDebitAmountOC)) > 0
                                THEN (SUM(OpenningCreditAmountOC
                                          - OpenningDebitAmountOC))
                                ELSE $0
                           END
                 END) AS OpenningCreditAmountOC, -- Dư có đầu kỳ
                (CASE WHEN AccountCategoryKind = 1
                      THEN (SUM(OpenningCreditAmount - OpenningDebitAmount))
                      WHEN AccountCategoryKind = 0 THEN $0
                      ELSE CASE WHEN (SUM(OpenningCreditAmount
                                          - OpenningDebitAmount)) > 0
                                THEN (SUM(OpenningCreditAmount
                                          - OpenningDebitAmount))
                                ELSE $0
                           END
                 END) AS OpenningCreditAmount, -- Dư có đầu kỳ quy đổi 
                SUM(DebitAmountOC) AS DebitAmountOC,	-- Phát sinh nợ
                SUM(DebitAmount) AS DebitAmount, -- Phát sinh nợ quy đổi
                SUM(CreditAmountOC) AS CreditAmountOC, -- Phát sinh có
                SUM(CreditAmount) AS CreditAmount, -- Phát sinh có quy đổi
                                        
                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ 
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
                (CASE WHEN AccountCategoryKind = 0/*dư cuối của tk có tính chất nợ*/
                      THEN SUM(OpenningDebitAmountOC - OpenningCreditAmountOC
                               + DebitAmountOC - CreditAmountOC)
                      WHEN AccountCategoryKind = 1 THEN $0
                      ELSE CASE WHEN SUM(OpenningCreditAmountOC
                                         - OpenningDebitAmountOC
                                         + CreditAmountOC - DebitAmountOC) > 0
                                THEN $0
                                ELSE SUM(OpenningDebitAmountOC
                                         - OpenningCreditAmountOC
                                         + DebitAmountOC - CreditAmountOC)
                           END
                 END) AS CloseDebitAmountOC,	-- Dư nợ cuối kỳ
                (CASE WHEN AccountCategoryKind = 1
                      THEN SUM(OpenningCreditAmountOC - OpenningDebitAmountOC
                               + CreditAmountOC - DebitAmountOC)
                      WHEN AccountCategoryKind = 0 THEN $0
                      ELSE CASE WHEN (SUM(OpenningCreditAmountOC
                                          - OpenningDebitAmountOC
                                          + CreditAmountOC - DebitAmountOC)) > 0
                                THEN SUM(OpenningCreditAmountOC
                                         - OpenningDebitAmountOC
                                         + CreditAmountOC - DebitAmountOC)
                                ELSE $0
                           END
                 END) AS CloseCreditAmountOC,	-- Dư có cuối kỳ
                (CASE WHEN AccountCategoryKind = 0
                      THEN SUM(OpenningDebitAmount - OpenningCreditAmount
                               + DebitAmount - CreditAmount)
                      WHEN AccountCategoryKind = 1 THEN $0
                      ELSE CASE WHEN SUM(OpenningCreditAmount
                                         - OpenningDebitAmount + CreditAmount
                                         - DebitAmount) > 0 THEN $0
                                ELSE SUM(OpenningDebitAmount
                                         - OpenningCreditAmount + DebitAmount
                                         - CreditAmount)
                           END
                 END) AS CloseDebitAmount,	-- Dư nợ cuối kỳ quy đổi
                (CASE WHEN AccountCategoryKind = 1
                      THEN SUM(OpenningCreditAmount - OpenningDebitAmount
                               + CreditAmount - DebitAmount)
                      WHEN AccountCategoryKind = 0 THEN $0
                      ELSE CASE WHEN (SUM(OpenningCreditAmount
                                          - OpenningDebitAmount + CreditAmount
                                          - DebitAmount)) > 0
                                THEN SUM(OpenningCreditAmount
                                         - OpenningDebitAmount + CreditAmount
                                         - DebitAmount)
                                ELSE $0
                           END
                 END) AS CloseCreditAmount,	-- Dư có cuối kỳ quy đổi
                AccountObjectGroupListCode,
                AccountObjectCategoryName
        FROM    (SELECT OU.OrganizationUnitID, 
						OU.MISACodeID,						                       
						--OU.OrganizationUnitCode,
						--OU.OrganizationUnitName,
                        AOL.AccountObjectID,
                        AOL.AccountObjectCode,   -- Mã khách hàng
                        AOL.AccountObjectNameDI AS AccountObjectName,	-- Tên khách hàng lấy trên danh mục              
                        AOL.AccountObjectAddressDI AS AccountObjectAddress, -- Địa chỉ    
                        AOL.AccountObjectTaxCode, -- Mã số thuế
                        LAOI.Tel,
                        TBAN.AccountNumber, -- TK công nợ
                        TBAN.AccountCategoryKind, -- Tính chất tài khoản 
                        CASE WHEN AOL.PostedDate < @FromDate
                             THEN AOL.DebitAmountOC
                             ELSE $0
                        END AS OpenningDebitAmountOC,	-- Dư nợ Đầu kỳ
                        CASE WHEN AOL.PostedDate < @FromDate
                             THEN AOL.DebitAmount
                             ELSE $0
                        END AS OpenningDebitAmount, -- Dư nợ Đầu kỳ quy đổi
                        CASE WHEN AOL.PostedDate < @FromDate
                             THEN AOL.CreditAmountOC
                             ELSE $0
                        END AS OpenningCreditAmountOC, -- Dư có đầu kỳ
                        CASE WHEN AOL.PostedDate < @FromDate
                             THEN AOL.CreditAmount
                             ELSE $0
                        END AS OpenningCreditAmount, -- Dư có đầu kỳ quy đổi                                                  
                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                             ELSE AOL.DebitAmountOC
                        END AS DebitAmountOC, -- Phát sinh nợ                                    
                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                             ELSE AOL.DebitAmount
                        END AS DebitAmount, -- Phát sinh nợ quy đổi                                         
                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                             ELSE AOL.CreditAmountOC
                        END AS CreditAmountOC, -- Phát sinh có  
                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                             ELSE AOL.CreditAmount
                        END AS CreditAmount,

                        LAOI.AccountObjectGroupListCode,
                        LAOI.AccountObjectCategoryName
                 FROM   dbo.AccountObjectLedger AS AOL
                        INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                        INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                        INNER JOIN @tblListOrganizationUnitID OU ON AOL.OrganizationUnitID = OU.OrganizationUnitID
						
                        INNER JOIN @tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                        INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                        LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                 WHERE  AOL.PostedDate <= @ToDate
                        AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                        AND (@CurrencyID IS NULL
                             OR AOL.CurrencyID = @CurrencyID
                            )
                        AND AN.DetailByAccountObject = 1
                        AND AN.AccountObjectType = 1
                ) AS RSNS
				  Inner JOIN @tblOrganizationUnitID P ON 
						((P.IsParent = 0 OR P.IsParentWithChild = 1) AND RSNS.OrganizationUnitID = P.OrganizationUnitID) 
						OR (P.IsParent = 1 AND P.IsParentWithChild = 0 AND RSNS.MisaCodeID LIKE P.MisaCodeID + '%')
       
        GROUP BY 
				--RSNS.OrganizationUnitID,
    --            RSNS.OrganizationUnitCode, -- Mã đơn vị
    --            RSNS.OrganizationUnitName, -- Tên đơn vị
	 P.OrganizationUnitID ,
                P.OrganizationUnitCode,
                P.OrganizationUnitName  ,
                RSNS.AccountObjectID,
                RSNS.AccountObjectCode,   -- Mã khách hàng
                RSNS.AccountObjectName,	-- Tên khách hàng              
                RSNS.AccountObjectAddress, -- Địa chỉ
                RSNS.AccountObjectTaxCode, -- Mã số thuế             
                RSNS.Tel,
                RSNS.AccountNumber, -- Số tài khoản
                RSNS.AccountCategoryKind, -- Tính chất tài khoản
                RSNS.AccountObjectGroupListCode,
                RSNS.AccountObjectCategoryName
        HAVING
				SUM(DebitAmountOC)<>0 OR
                SUM(DebitAmount)<>0 OR
                SUM(CreditAmountOC) <>0 OR
                SUM(CreditAmount) <>0 OR
                SUM(OpenningDebitAmountOC - OpenningCreditAmountOC)<>0 OR
                SUM(OpenningDebitAmount - OpenningCreditAmount)<>0
        ORDER BY P.OrganizationUnitCode,
                RSNS.AccountObjectCode -- Mã khách hàng							        
 
 
 
 
        
    END
 
 
    
