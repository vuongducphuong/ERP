--exec Proc_CTR_GetReceivableSummaryBySAOrder @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-15 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@CurrencyID=N'VND',@SAOrderID=N',76b2cb33-3924-4326-8a58-2f4d4e6e73f9,7d7bfca7-4721-4815-ba97-ffb253f2081c,af61ecc0-7cf1-45bc-b1f4-97f2052c42a8,c8f2b40e-d1a7-4993-b555-ab8e383ef131,1e73cef2-4112-4976-aa3f-eb576ebdcc02,65504454-b912-4b82-a08e-fc2f57fa640a,e71e283a-fe7b-4c1f-9e41-214298e897b0,09cefbb6-f459-423d-ba04-859714a09801,',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		hoant 
-- Create date: 19/11/2014
-- Description:	Báo cáo Tổng hợp công nợ phải thu theo đơn đặt hàng
-- Nhyen - 13/4/2018 (Bug 209988):  Số dư quy đổi dư bên nào thì hiển thị số dư bên đó khi TK có tính chất là lưỡng tính 
-- =============================================

DECLARE			@FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@BranchID UNIQUEIDENTIFIER -- Chi nhánh
DECLARE			@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(25) -- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã khách hàng
DECLARE			@CurrencyID NVARCHAR(3) -- Loại tiền
DECLARE			@SAOrderID AS NVARCHAR(MAX)  -- Danh sách đơn đặt hàng 
DECLARE			@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


SET				@FromDate='2018-01-01 00:00:00'
SET				@ToDate='2018-01-15 23:59:59'
SET				@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET				@IncludeDependentBranch=1
SET				@AccountNumber=N'131'
SET				@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET				@CurrencyID=N'VND'
SET				@SAOrderID=N',76b2cb33-3924-4326-8a58-2f4d4e6e73f9,7d7bfca7-4721-4815-ba97-ffb253f2081c,af61ecc0-7cf1-45bc-b1f4-97f2052c42a8,c8f2b40e-d1a7-4993-b555-ab8e383ef131,1e73cef2-4112-4976-aa3f-eb576ebdcc02,65504454-b912-4b82-a08e-fc2f57fa640a,e71e283a-fe7b-4c1f-9e41-214298e897b0,09cefbb6-f459-423d-ba04-859714a09801,'
SET				@IsWorkingWithManagementBook=0


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
               
        CREATE TABLE #tblListAccountObjectID  -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER PRIMARY KEY ,
              AccountObjectCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS,
              AccountObjectName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS,
              AccountObjectAddress NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
              AccountObjectTaxCode NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
              AccountObjectGroupListCode NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS,
              AccountObjectCategoryName NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
            ) 
        INSERT  INTO #tblListAccountObjectID
                SELECT  TLAO.Value AS AccountObjectID ,
                        ao.AccountObjectCode ,
                        ao.AccountObjectName ,
                        ao.Address ,
                        ao.CompanyTaxCode ,
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') AS TLAO
                        INNER JOIN AccountObject AS AO ON AO.AccountObjectID = TLAO.Value        			
        
        CREATE TABLE #tblListSAOrderID  -- Bảng chứa danh sách mã hợp đồng
            (
              SAOrderRefID UNIQUEIDENTIFIER PRIMARY KEY,
              SAOrderRefNo NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
              SAOrderRefDate DATETIME ,
              SAOrderStatus NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
            ) 
        INSERT  INTO #tblListSAOrderID
                SELECT  f.Value ,
                        C.RefNo ,
                        C.RefDate ,
                        (CASE C.status WHEN 0 THEN N'Chưa thực hiện'
															WHEN 1 THEN N'Đang thực hiện'
															WHEN 2 THEN N'Hoàn thành'
															WHEN 3 THEN N'Đã hủy bỏ'
											END ) AS SAOrderStatus
                FROM    dbo.Func_ConvertGUIStringIntoTable(@SAOrderID, ',') f
                        INNER JOIN dbo.SAOrder C ON f.Value = C.RefID
        DECLARE @tblAccountNumber TABLE
            (
              AccountNumber NVARCHAR(25) PRIMARY KEY ,
              AccountName NVARCHAR(255) ,
              AccountNumberPercent NVARCHAR(25) ,
              AccountCategoryKind INT
            )
           
        IF @AccountNumber IS NOT NULL
            BEGIN
                INSERT  INTO @tblAccountNumber
                        SELECT  A.AccountNumber ,
                                A.AccountName ,
                                A.AccountNumber + '%' ,
                                A.AccountCategoryKind
                        FROM    dbo.Account AS A
                        WHERE   AccountNumber = @AccountNumber
                        ORDER BY A.AccountNumber ,
                                A.AccountName 
                
            END
        ELSE
            BEGIN 
                INSERT  INTO @tblAccountNumber
                        SELECT  A.AccountNumber ,
                                A.AccountName ,
                                A.AccountNumber + '%' ,
                                A.AccountCategoryKind
                        FROM    dbo.Account AS A
                        WHERE   DetailByAccountObject = 1
                                AND AccountObjectType = 1
                                AND IsParent = 0
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END
            
        
        
        SELECT  ROW_NUMBER() OVER ( ORDER BY SAOrderRefDate,SAOrderRefNo , AccountObjectCode,AccountNumber ) AS RowNum ,
                SAOrderRefID ,
                SAOrderRefNo , 
                SAOrderRefDate , 
                SAOrderStatus,
                AccountObjectID ,
                AccountObjectCode ,   -- Mã NCC
                AccountObjectName ,	-- Tên NCC              
                AccountObjectGroupListCode ,
                AccountObjectCategoryName ,
                AccountObjectAddress , -- Địa chỉ
                AccountObjectTaxCode ,
                AccountNumber , -- Số tài khoản
                AccountCategoryKind , -- Tính chất tài khoản
                ( CASE WHEN AccountCategoryKind = 0
                       THEN SUM(OpenningDebitAmountOC)
                            - SUM(OpenningCreditAmountOC)
                       WHEN AccountCategoryKind = 1 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningDebitAmountOC
                                            - OpenningCreditAmountOC) ) > 0
                                 THEN ( SUM(OpenningDebitAmountOC
                                            - OpenningCreditAmountOC) )
                                 ELSE $0
                            END
                  END ) AS OpenningDebitAmountOC ,	-- Dư nợ Đầu kỳ           
                ( CASE WHEN AccountCategoryKind = 0
                       THEN ( SUM(OpenningDebitAmount - OpenningCreditAmount) )
                       WHEN AccountCategoryKind = 1 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningDebitAmount
                                            - OpenningCreditAmount) ) > 0
                                 THEN SUM(OpenningDebitAmount
                                          - OpenningCreditAmount)
                                 ELSE $0
                            END
                  END ) AS OpenningDebitAmount , -- Dư nợ Đầu kỳ quy đổi
                ( CASE WHEN AccountCategoryKind = 1
                       THEN ( SUM(OpenningCreditAmountOC
                                  - OpenningDebitAmountOC) )
                       WHEN AccountCategoryKind = 0 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningCreditAmountOC
                                            - OpenningDebitAmountOC) ) > 0
                                 THEN ( SUM(OpenningCreditAmountOC
                                            - OpenningDebitAmountOC) )
                                 ELSE $0
                            END
                  END ) AS OpenningCreditAmountOC , -- Dư có đầu kỳ
                ( CASE WHEN AccountCategoryKind = 1
                       THEN ( SUM(OpenningCreditAmount - OpenningDebitAmount) )
                       WHEN AccountCategoryKind = 0 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningCreditAmount
                                            - OpenningDebitAmount) ) > 0
                                 THEN ( SUM(OpenningCreditAmount
                                            - OpenningDebitAmount) )
                                 ELSE $0
                            END
                  END ) AS OpenningCreditAmount , -- Dư có đầu kỳ quy đổi 
                SUM(DebitAmountOC) AS DebitAmountOC ,	-- Phát sinh nợ
                SUM(DebitAmount) AS DebitAmount , -- Phát sinh nợ quy đổi
                SUM(CreditAmountOC) AS CreditAmountOC , -- Phát sinh có
                SUM(CreditAmount) AS CreditAmount , -- Phát sinh có quy đổi
                                        
                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ 
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
				-- Nhyen - 13/4/2018 (Bug 209988):  Số dư quy đổi dư bên nào thì hiển thị số dư bên đó khi TK có tính chất là lưỡng tính 
                ( CASE WHEN AccountCategoryKind = 0
                       THEN SUM(OpenningDebitAmountOC - OpenningCreditAmountOC
                                + DebitAmountOC - CreditAmountOC)
                       WHEN AccountCategoryKind = 1 THEN $0
                       ELSE CASE WHEN SUM(OpenningDebitAmountOC
                                          - OpenningCreditAmountOC
                                          + DebitAmountOC - CreditAmountOC) > 0
                                 THEN SUM(OpenningDebitAmountOC
                                          - OpenningCreditAmountOC
                                          + DebitAmountOC - CreditAmountOC)
                                 ELSE $0
                            END
                  END ) AS CloseDebitAmountOC ,	-- Dư nợ cuối kỳ
                ( CASE WHEN AccountCategoryKind = 1
                       THEN SUM(OpenningCreditAmountOC - OpenningDebitAmountOC
                                + CreditAmountOC - DebitAmountOC)
                       WHEN AccountCategoryKind = 0 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningCreditAmountOC
                                            - OpenningDebitAmountOC
                                            + CreditAmountOC - DebitAmountOC) ) > 0
                                 THEN SUM(OpenningCreditAmountOC
                                          - OpenningDebitAmountOC
                                          + CreditAmountOC - DebitAmountOC)
                                 ELSE $0
                            END
                  END ) AS CloseCreditAmountOC ,	-- Dư có cuối kỳ
                ( CASE WHEN AccountCategoryKind = 0
                       THEN SUM(OpenningDebitAmount - OpenningCreditAmount
                                + DebitAmount - CreditAmount)
                       WHEN AccountCategoryKind = 1 THEN $0
                       ELSE CASE WHEN SUM(OpenningDebitAmount
                                          - OpenningCreditAmount + DebitAmount
                                          - CreditAmount) > 0 
                                 THEN SUM(OpenningDebitAmount
                                          - OpenningCreditAmount + DebitAmount
                                          - CreditAmount)
                                 ELSE $0
                            END
                  END ) AS CloseDebitAmount ,	-- Dư nợ cuối kỳ quy đổi
                ( CASE WHEN AccountCategoryKind = 1
                       THEN SUM(OpenningCreditAmount - OpenningDebitAmount
                                + CreditAmount - DebitAmount)
                       WHEN AccountCategoryKind = 0 THEN $0
                       ELSE CASE WHEN SUM(OpenningCreditAmount
                                          - OpenningDebitAmount + CreditAmount
                                          - DebitAmount) > 0
                                 THEN SUM(OpenningCreditAmount
                                          - OpenningDebitAmount + CreditAmount
                                          - DebitAmount)
                                 ELSE $0
                            END
                  END ) AS CloseCreditAmount ,	-- Dư có cuối kỳ quy đổi
               
                BranchName
        FROM    ( SELECT    SA.SAOrderRefID ,
                            SA.SAOrderRefNo,
                            SA.SAOrderRefDate ,  
                            SA.SAOrderStatus     ,                     
                            AOL.AccountObjectID ,
                            LAOI.AccountObjectCode ,   -- Mã NCC
                            LAOI.AccountObjectName ,	-- Tên NCC lấy trên danh mục              
                            LAOI.AccountObjectAddress , -- Địa chỉ    
                            LAOI.AccountObjectTaxCode , -- Mã số thuế
                            TBAN.AccountNumber , -- TK công nợ
                            TBAN.AccountCategoryKind , -- Tính chất tài khoản 
                            CASE WHEN AOL.PostedDate < @FromDate
                                 THEN AOL.DebitAmountOC
                                 ELSE $0
                            END AS OpenningDebitAmountOC ,	-- Dư nợ Đầu kỳ
                            CASE WHEN AOL.PostedDate < @FromDate
                                 THEN AOL.DebitAmount
                                 ELSE $0
                            END AS OpenningDebitAmount , -- Dư nợ Đầu kỳ quy đổi
                            CASE WHEN AOL.PostedDate < @FromDate
                                 THEN AOL.CreditAmountOC
                                 ELSE $0
                            END AS OpenningCreditAmountOC , -- Dư có đầu kỳ
                            CASE WHEN AOL.PostedDate < @FromDate
                                 THEN AOL.CreditAmount
                                 ELSE $0
                            END AS OpenningCreditAmount , -- Dư có đầu kỳ quy đổi                                                  
                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                 ELSE AOL.DebitAmountOC
                            END AS DebitAmountOC , -- Phát sinh nợ                                    
                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                 ELSE AOL.DebitAmount
                            END AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                 ELSE AOL.CreditAmountOC
                            END AS CreditAmountOC , -- Phát sinh có  
                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                 ELSE AOL.CreditAmount
                            END AS CreditAmount ,
                            LAOI.AccountObjectGroupListCode ,
                            LAOI.AccountObjectCategoryName ,
                            AOL.BranchID ,
                            OU.OrganizationUnitName BranchName
                  FROM      dbo.AccountObjectLedger AS AOL                            
                            INNER JOIN #tblListSAOrderID SA ON  AOL.OrderID=SA.SAOrderRefID
                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumber
                                                              + '%'
                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                            INNER JOIN #tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID                            
                            LEFT JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = AOL.BranchID
                  WHERE     AOL.PostedDate <= @ToDate
                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND ( @CurrencyID IS NULL
                                  OR AOL.CurrencyID = @CurrencyID
                                )
                            AND AN.DetailByAccountObject = 1
                ) AS RSNS
       
        GROUP BY RSNS.SAOrderRefID ,
                RSNS.SAOrderRefNo , 
                RSNS.SAOrderRefDate , 
                RSNS.SAOrderStatus,
                RSNS.AccountObjectID ,
                RSNS.AccountObjectCode ,   -- Mã NCC
                RSNS.AccountObjectName ,	-- Tên NCC              
                RSNS.AccountObjectAddress , -- Địa chỉ
                RSNS.AccountObjectTaxCode , -- Mã số thuế             
                RSNS.AccountNumber , -- Số tài khoản
                RSNS.AccountCategoryKind , -- Tính chất tài khoản
                RSNS.AccountObjectGroupListCode ,
                RSNS.AccountObjectCategoryName ,
                RSNS.BranchID ,
                BranchName
         HAVING
				SUM(DebitAmountOC)<>0 OR
                SUM(DebitAmount)<>0 OR
                SUM(CreditAmountOC) <>0 OR
                SUM(CreditAmount) <>0 OR
                SUM(OpenningDebitAmountOC - OpenningCreditAmountOC)<>0 OR
                SUM(OpenningDebitAmount - OpenningCreditAmount)<>0
        
        DROP TABLE #tblListSAOrderID
        DROP TABLE #tblListAccountObjectID
    END
    

