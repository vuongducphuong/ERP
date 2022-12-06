--exec Proc_SAR_GetReceivableDeptSummary @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@CurrencyID=N'VND',@IsShowInPeriodOnly=1,@IsWorkingWithManagementBook=0
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		nvtoan
-- Create date: 18/11/2014
-- Description:	Báo cáo Tổng hợp công nợ phải thu
-- nvtoan modify 16/01/2014: Sửa lỗi tính toán số liệu
-- nvtoan modify 28/01/2015: Lấy tài khoản chi tiết theo khách hàng
-- nvtoan modify 29/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- tthoa edit 6/2/2015 để phục vụ drilldown
-- NVTOAN modify 21/10/2015: Lấy bổ sung cột số nợ tối đa
-- nmtruong 6/11/2015: sửa CR 73195: Lấy lên cột phát sinh lũy kế từ đầu năm
-- =============================================

DECLARE		@FromDate DATETIME 
DECLARE		@ToDate DATETIME 
DECLARE		@BranchID UNIQUEIDENTIFIER -- Chi nhánh
DECLARE		@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE		@AccountNumber NVARCHAR(25) -- Số tài khoản
DECLARE		@AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhà cung cấp
DECLARE		@CurrencyID NVARCHAR(3) -- Loại tiền
DECLARE		@IsShowInPeriodOnly BIT -- Chỉ lấy lên KH có phát sinh trong kỳ
DECLARE		@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


SET			@FromDate='2018-01-01 00:00:00'
SET			@ToDate='2018-01-05 23:59:59'
SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IncludeDependentBranch=1
SET			@AccountNumber=N'131'
SET			@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET			@CurrencyID=N'VND'
SET			@IsShowInPeriodOnly=1
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
               
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các NCC
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectGroupListCode NVARCHAR(MAX) ,
              AccountObjectCategoryName NVARCHAR(MAX)
            ) 
             
        INSERT  INTO @tblListAccountObjectID
                SELECT  AO.AccountObjectID ,
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC
                FROM    AccountObject AS AO
                        LEFT JOIN dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                              ',') AS TLAO ON AO.AccountObjectID = TLAO.Value
                WHERE   AO.IsCustomer = 1
                        AND ( @AccountObjectID IS NULL
                              OR TLAO.Value IS NOT NULL
                            )
                              			
                                                           
        -- Bảng chứa số tài khoản    
        DECLARE @tblAccountNumber TABLE
            (
              AccountNumber NVARCHAR(255) PRIMARY KEY ,
              AccountName NVARCHAR(255) ,
              AccountNumberPercent NVARCHAR(255) ,
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
            
        -- nmtruong: sửa CR 73195: Lấy lên cột phát sinh lũy kế từ đầu năm
	    DECLARE @FirstDateOfYear AS DATETIME
	    SET @FirstDateOfYear = '1/1/' + CAST(Year(@FromDate) AS NVARCHAR(4))	   
	    
        SELECT  ROW_NUMBER() OVER ( ORDER BY AccountObjectCode ) AS RowNum ,
                AccountObjectID ,
                AccountObjectCode ,   -- Mã NCC
                AccountObjectName ,	-- Tên NCC              
                AccountObjectAddress , -- Địa chỉ
                AccountObjectTaxCode ,
                Tel ,
                AccountNumber , -- Số tài khoản
                AccountCategoryKind , -- Tính chất tài khoản
                MaximizeDebtAmount ,
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
                SUM(AccumDebitAmountOC) AS AccumDebitAmountOC ,	-- Phát sinh nợ
                SUM(AccumDebitAmount) AS AccumDebitAmount , -- Phát sinh nợ quy đổi
                SUM(AccumCreditAmountOC) AS AccumCreditAmountOC , -- Phát sinh có
                SUM(AccumCreditAmount) AS AccumCreditAmount , -- Phát sinh có quy đổi
                                        
                /* Số dư cuối kỳ = Dư Có đầu kỳ - Dư Nợ đầu kỳ + Phát sinh Có – Phát sinh Nợ
				Nếu Số dư cuối kỳ >0 thì hiển bên cột Dư Có cuối kỳ 
				Nếu số dư cuối kỳ <0 thì hiển thị bên cột Dư Nợ cuối kỳ */
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
                                - DebitAmountOC + CreditAmountOC)
                       WHEN AccountCategoryKind = 0 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningCreditAmountOC
                                            - OpenningDebitAmountOC
                                            - DebitAmountOC + CreditAmountOC) ) > 0
                                 THEN SUM(OpenningCreditAmountOC
                                          - OpenningDebitAmountOC
                                          - DebitAmountOC + CreditAmountOC)
                                 ELSE $0
                            END
                  END ) AS CloseCreditAmountOC ,	-- Dư có cuối kỳ
                ( CASE WHEN AccountCategoryKind = 0
                       THEN SUM(OpenningDebitAmount - OpenningCreditAmount
                                + DebitAmount - CreditAmount)
                       WHEN AccountCategoryKind = 1 THEN $0
                       ELSE CASE WHEN SUM(OpenningDebitAmount
                                          - OpenningCreditAmount
                                          - CreditAmount + DebitAmount) > 0
                                 THEN SUM(OpenningDebitAmount
                                          - OpenningCreditAmount
                                          - CreditAmount + DebitAmount)
                                 ELSE $0
                            END
                  END ) AS CloseDebitAmount ,	-- Dư nợ cuối kỳ quy đổi
                ( CASE WHEN AccountCategoryKind = 1
                       THEN SUM(OpenningCreditAmount - OpenningDebitAmount
                                + CreditAmount - DebitAmount)
                       WHEN AccountCategoryKind = 0 THEN $0
                       ELSE CASE WHEN ( SUM(OpenningCreditAmount
                                            - OpenningDebitAmount
                                            + CreditAmount - DebitAmount) ) > 0
                                 THEN SUM(OpenningCreditAmount
                                          - OpenningDebitAmount + CreditAmount
                                          - DebitAmount)
                                 ELSE $0
                            END
                  END ) AS CloseCreditAmount ,	-- Dư có cuối kỳ quy đổi
                AccountObjectGroupListCode ,
                AccountObjectCategoryName
        FROM    ( SELECT    AOL.AccountObjectID ,
                            AOL.AccountObjectCode ,   -- Mã NCC
                            AO.AccountObjectName ,	-- Tên NCC lấy trên danh mục              
                            AO.Address AS AccountObjectAddress , -- Địa chỉ    
                            AO.CompanyTaxCode AS AccountObjectTaxCode , -- Mã số thuế
                            CASE AO.AccountObjectType
                              WHEN 0 THEN ao.Tel
                              ELSE AO.Mobile
                            END AS Tel ,
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
                            CASE WHEN AOL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN AOL.DebitAmountOC
                                 ELSE 0
                            END AS DebitAmountOC , -- Phát sinh nợ                                    
                            CASE WHEN AOL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN AOL.DebitAmount
                                 ELSE 0
                            END AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                            CASE WHEN AOL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN AOL.CreditAmountOC
                                 ELSE 0
                            END AS CreditAmountOC , -- Phát sinh có  
                            CASE WHEN AOL.PostedDate BETWEEN @FromDate AND @ToDate
                                 THEN AOL.CreditAmount
                                 ELSE 0
                            END AS CreditAmount ,
                            -- Lấy lên cột lũy kế từ đầu năm
                            CASE WHEN AOL.PostedDate BETWEEN @FirstDateOfYear AND @ToDate
                                 THEN AOL.DebitAmountOC
                                 ELSE 0
                            END AS AccumDebitAmountOC , -- Phát sinh nợ                                    
                            CASE WHEN AOL.PostedDate BETWEEN @FirstDateOfYear AND @ToDate
                                 THEN AOL.DebitAmount
                                 ELSE 0
                            END AS AccumDebitAmount , -- Phát sinh nợ quy đổi                                         
                            CASE WHEN AOL.PostedDate BETWEEN @FirstDateOfYear AND @ToDate
                                 THEN AOL.CreditAmountOC
                                 ELSE 0
                            END AS AccumCreditAmountOC , -- Phát sinh có  
                            CASE WHEN AOL.PostedDate BETWEEN @FirstDateOfYear AND @ToDate
                                 THEN AOL.CreditAmount
                                 ELSE 0
                            END AS AccumCreditAmount ,
                            LAOI.AccountObjectGroupListCode ,
                            LAOI.AccountObjectCategoryName 
                            ,AO.MaximizeDebtAmount
                  FROM      dbo.AccountObjectLedger AS AOL
                            INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = AOL.AccountObjectID
                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                            INNER JOIN @tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                  WHERE     AOL.PostedDate <= @ToDate
                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND ( @CurrencyID IS NULL
                                  OR AOL.CurrencyID = @CurrencyID
                                )
                            AND AN.DetailByAccountObject = 1
                        --AND AN.AccountObjectType = 1
                ) AS RSNS
        GROUP BY RSNS.AccountObjectID ,
                RSNS.AccountObjectCode ,   -- Mã NCC
                RSNS.AccountObjectName ,	-- Tên NCC              
                RSNS.AccountObjectAddress , -- Địa chỉ
                RSNS.AccountObjectTaxCode , -- Mã số thuế             
                RSNS.Tel ,
                RSNS.AccountNumber , -- Số tài khoản
                RSNS.AccountCategoryKind , -- Tính chất tài khoản
                RSNS.AccountObjectGroupListCode ,
                RSNS.AccountObjectCategoryName 
                ,RSNS.MaximizeDebtAmount
        HAVING  SUM(DebitAmountOC) <> 0
                OR SUM(DebitAmount) <> 0
                OR SUM(CreditAmountOC) <> 0
                OR SUM(CreditAmount) <> 0
                OR SUM(OpenningDebitAmountOC - OpenningCreditAmountOC) <> 0
                OR SUM(OpenningDebitAmount - OpenningCreditAmount) <> 0                
                OR(@IsShowInPeriodOnly = 0 AND (
                 SUM(AccumDebitAmountOC) <>0	-- Phát sinh nợ
                OR SUM(AccumDebitAmount) <>0 -- Phát sinh nợ quy đổi
                OR SUM(AccumCreditAmountOC) <>0  -- Phát sinh có
                OR SUM(AccumCreditAmount)<>0))
        ORDER BY RSNS.AccountObjectCode -- Mã NCC
        OPTION(RECOMPILE)
    END

