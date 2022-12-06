--exec Proc_SAR_GetReceivableSummaryByProjectWork @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-05 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@ProjectWorkID=N',9b46c3a0-060f-4b8e-a5e2-4786271f51d9,c0570228-b65f-44c8-acee-3da2ae38d590,e9b86b73-2026-4fe1-9e49-9f0d0c7ee9ac,',@CurrencyID=N'VND',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		nvtoan
-- Create date: 18/11/2014
-- Description:	<Bán hàng: Lấy số liệu tổng hợp công nợ phải thu theo công trình>
-- Edited By DNMinh 29/12/2014: Sửa bug 40822, khi chọn công trình cha thì lấy lên toàn bộ các chứng từ từ công trình con
-- NVTOAN Modify 14/01/2014: Sửa lỗi không lấy định khoản xử lý chênh lệch tỷ giá
-- nvtoan modify 28/01/2015: Lấy tài khoản chi tiết theo khách hàng
-- nvtoan modify 29/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- modified by HHSon (64047): Bổ sung Loại công trình
-- VHAnh edited 11.01.2016: Sửa cách lấy số liệu khi chọn công trình, hiển thị lại theo hình cây (80389)
-- BTAnh - 12.08.2016: Tách sub query ra thành bảng #Ledger để tăng tốc độ query (JIRA: SMEFIVE-13978)
-- =============================================

DECLARE			@FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@BranchID UNIQUEIDENTIFIER -- Chi nhánh
DECLARE			@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(20) -- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhà cung cấp
DECLARE			@ProjectWorkID AS NVARCHAR(MAX)  -- Danh sách công trình
DECLARE			@CurrencyID NVARCHAR(3) -- Loại tiền
DECLARE			@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không? 


SET				@FromDate='2018-01-01 00:00:00'
SET				@ToDate='2018-01-05 23:59:59'
SET				@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET				@IncludeDependentBranch=1
SET				@AccountNumber=N'131'
SET				@AccountObjectID=N',410c0ed4-9d79-49d1-94e4-5f33361b1700,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,2ea65716-13d0-4aea-9506-e8ce4e0ded39,58efaebf-f074-4336-86d7-439ba11cac26,be2c2d67-d658-4245-b684-a446cd7a38f9,4176d066-cfbf-4661-bb69-37a5e88554bb,4acfc6f7-a8db-4e14-89cf-52d13b483df4,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET				@ProjectWorkID=N',9b46c3a0-060f-4b8e-a5e2-4786271f51d9,c0570228-b65f-44c8-acee-3da2ae38d590,e9b86b73-2026-4fe1-9e49-9f0d0c7ee9ac,'
SET				@CurrencyID=N'VND'
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
               
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các NCC
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              Tel NVARCHAR(50) ,
              AccountObjectName NVARCHAR(128) ,
              AccountObjectAddress NVARCHAR(255) ,
              AccountObjectGroupListCode NVARCHAR(MAX) ,
              AccountObjectCategoryName NVARCHAR(MAX)
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  TLAO.Value AS AccountObjectID ,
                        CASE ao.AccountObjectType
                          WHEN 0 THEN ao.Tel
                          ELSE AO.Mobile
                        END AS Tel ,
                        ao.AccountObjectName ,
                        Ao.Address ,
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') AS TLAO
                        INNER JOIN AccountObject AS AO ON AO.AccountObjectID = TLAO.Value                                			
        -----------------------------------------------------------------------------
		--vhanh edited 07.01.2016: CR 80389
        DECLARE @tblProjectWorkSelected TABLE  -- Bảng các công trình được chọn
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) ,
              ProjectWorkCode NVARCHAR(20),
              ProjectWorkName NVARCHAR(128),
              ProjectWorkCategoryName NVARCHAR(128),
              SortMISACodeID NVARCHAR(100),
              IsParent BIT ,
              IsParentWithChild BIT
            ) 
        INSERT  INTO @tblProjectWorkSelected
                SELECT DISTINCT
                        PW.ProjectWorkID ,
                        PW.MISACodeID ,
                        PW.ProjectWorkCode ,
                        PW.ProjectWorkName ,
                        PWC.ProjectWorkCategoryName ,
                        PW.SortMISACodeID ,
                        PW.IsParent ,
                        0
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ProjectWorkID, ',') tString
                        INNER JOIN dbo.ProjectWork PW ON PW.ProjectWorkID = tString.Value
                        LEFT JOIN dbo.ProjectWorkCategory PWC ON PW.ProjectWorkCategoryID = PWC.ProjectWorkCategoryID
        -- Update lại, tìm những thằng nào là cha và có con được chọn
        UPDATE  T
        SET     IsParentWithChild = 1
        FROM    @tblProjectWorkSelected T
                INNER JOIN @tblProjectWorkSelected T1 ON T1.MISACodeID LIKE T.MISACodeID + '%'
                                                         AND T.MISACodeID <> T1.MISACodeID
        WHERE   T.IsParent = 1			
		-- Bậc của các công trình         
        DECLARE @tblGradeListProjectwork TABLE-- Tính bậc để lùi dòng cho báo cáo hình cây
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100),
              Grade INT
            )
        INSERT  INTO @tblGradeListProjectwork
                SELECT  PWS.ProjectWorkID ,
                        PWS.MISACodeID ,
                        COUNT(PWSC.MISACodeID) Grade
                FROM    @tblProjectWorkSelected PWS
                        LEFT JOIN @tblProjectWorkSelected PWSC ON PWS.MISACodeID LIKE PWSC.MISACodeID + '%'
                                                              AND PWS.MISACodeID <> PWSC.MISACodeID
                GROUP BY PWS.ProjectWorkID ,
                        PWS.MISACodeID
				OPTION (RECOMPILE)
		-- Bảng chứa những mã công trình cha nhất từ bảng được chọn
        DECLARE @tblParentListProjectWork TABLE
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY
            )
        INSERT  INTO @tblParentListProjectWork
                SELECT DISTINCT
                        PWS.ProjectWorkID
                FROM    @tblProjectWorkSelected PWS
                        LEFT JOIN @tblProjectWorkSelected PWSC ON PWS.MISACodeID LIKE PWSC.MISACodeID
                                                              + '%'
                                                              AND PWS.MISACodeID <> PWSC.MISACodeID
                WHERE   PWSC.MISACodeID IS NULL
				OPTION (RECOMPILE)              
		-- Bảng các mã công trình là cha được chọn và có con được chọn	
        DECLARE @tblSelectedParentProjectWorkHasChild TABLE
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY
            )
        INSERT  INTO @tblSelectedParentProjectWorkHasChild
                SELECT DISTINCT
                        PWSC.ProjectWorkID
                FROM    @tblProjectWorkSelected PWS
                        LEFT JOIN @tblProjectWorkSelected PWSC ON PWS.MISACodeID LIKE PWSC.MISACodeID + '%'
                                                              AND PWS.MISACodeID <> PWSC.MISACodeID
                WHERE   PWSC.MISACodeID IS NOT NULL	
				OPTION (RECOMPILE)
		-- Bảng mã công trình gồm toàn bộ công trình được chọn và không phải là cha.
        DECLARE @tblListChildProjectWork TABLE
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100)
            ) 
			
        INSERT  INTO @tblListChildProjectWork
                SELECT    DISTINCT
                        PW.ProjectWorkID ,
                        PW.MISACodeID
                FROM    dbo.ProjectWork PW
                        INNER JOIN @tblProjectWorkSelected PWS ON PW.MISACodeID LIKE PWS.MISACodeID + '%'
                                                              AND PW.IsParent = 0
		OPTION (RECOMPILE) 
		----------------------------------------------------------------------------------------------------                                                 
           
        -- Bảng chứa số tài khoản    
        DECLARE @tblAccountNumber TABLE
            (
              AccountNumber NVARCHAR(20) PRIMARY KEY ,
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
                                AND DetailByAccountObject = 1
                                --AND IsParent = 0
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
--BTAnh-12.8.2016: Phần select này tách ra thành bảng tạm để tăng tốc độ--------------------            
		SELECT  PWS.ProjectWorkID ,
				PWS.ProjectWorkCode , -- Mã công trình
				PWS.ProjectWorkName , -- Tên công trình 
				PWS.ProjectWorkCategoryName , -- Loại công trình
				PWS.MISACodeID ,
				AOL.AccountObjectID ,
				AOL.AccountObjectCode ,   -- Mã NCC
				LAOI.tel ,
				LAOI.AccountObjectName ,	-- Tên NCC lấy trên danh mục              
				LAOI.AccountObjectAddress , -- Địa chỉ    
				AOL.AccountObjectTaxCode , -- Mã số thuế
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
				LAOI.AccountObjectCategoryName
		INTO #Ledger
		FROM      dbo.AccountObjectLedger AS AOL
				INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
				INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
				INNER JOIN @tblListChildProjectWork LCPW ON AOL.ProjectWorkID = LCPW.ProjectWorkID
				INNER JOIN @tblProjectWorkSelected PWS ON --Là cha và không có con thì lấy tất cả các con
						( PWS.IsParentWithChild = 0
						  AND LCPW.MisaCodeID LIKE PWS.MisaCodeID
						  + '%' 
						--Là cha và có con được chọn thì chỉ lấy các con được chọn
						  OR ( PWS.IsParentWithChild = 1
							   AND PWS.ProjectWorkID = LCPW.ProjectWorkID
							 )
						)
				INNER JOIN @tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
				INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
				LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
		WHERE     AOL.PostedDate <= @ToDate
				AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
				AND ( @CurrencyID IS NULL
					  OR AOL.CurrencyID = @CurrencyID
					)
		OPTION (RECOMPILE)
				--AND AN.DetailByAccountObject = 1	
		
-------------------------------------------				
                        		 		
        --SELECT * FROM dbo.Account WHERE AccountNumber = '131'
        SELECT  ROW_NUMBER() OVER ( ORDER BY AccountObjectCode, SEI.SortMISACodeID, GEI.Grade, SEI.ProjectWorkCode ) AS RowNum ,
                SEI.ProjectWorkID ,
                SPACE(GEI.Grade * 4) + SEI.ProjectWorkCode AS ProjectWorkCode ,
                SPACE(GEI.Grade * 4) + SEI.ProjectWorkName AS ProjectWorkName,
                SEI.ProjectWorkCategoryName ,				
                CASE WHEN PSEI.ProjectWorkID IS NOT NULL THEN CAST(1 AS BIT)
                     ELSE CAST(0 AS BIT)
                END IsBold ,
                GEI.Grade ,
                CAST(CASE WHEN GEI.Grade = 0 THEN 1
                          ELSE 0
                     END AS BIT) AS IsSummaryRow ,
                SEI.SortMISACodeID ,
                AccountObjectID ,
                AccountObjectCode ,   -- Mã NCC
                AccountObjectName ,	-- Tên NCC              
                AccountObjectAddress , -- Địa chỉ
                AccountObjectTaxCode ,
                tel ,
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
                ( CASE WHEN AccountCategoryKind = 0
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
                       ELSE CASE WHEN SUM(OpenningCreditAmount
                                          - OpenningDebitAmount + CreditAmount
                                          - DebitAmount) > 0 THEN $0
                                 ELSE SUM(OpenningDebitAmount
                                          - OpenningCreditAmount + DebitAmount
                                          - CreditAmount)
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
        FROM    #Ledger AS RSNS
                INNER JOIN @tblProjectWorkSelected SEI ON RSNS.MISACodeID LIKE SEI.MISACodeID + '%'                
                LEFT JOIN @tblSelectedParentProjectWorkHasChild PSEI ON PSEI.ProjectWorkID = SEI.ProjectWorkID
                INNER JOIN @tblGradeListProjectwork GEI ON GEI.ProjectWorkID = SEI.ProjectWorkID
        GROUP BY SEI.ProjectWorkID ,
                PSEI.ProjectWorkID ,
                SEI.ProjectWorkCode , -- Mã công trình
                SEI.ProjectWorkName , -- Tên công trình 
                SEI.ProjectWorkCategoryName ,
                SEI.SortMISACodeID ,
                GEI.Grade ,
                RSNS.AccountObjectID ,
                RSNS.AccountObjectCode ,   -- Mã NCC
                RSNS.AccountObjectName ,	-- Tên NCC              
                RSNS.AccountObjectAddress , -- Địa chỉ
                RSNS.AccountObjectTaxCode , -- Mã số thuế             
                RSNS.Tel ,
                RSNS.AccountNumber , -- Số tài khoản
                RSNS.AccountCategoryKind , -- Tính chất tài khoản
                RSNS.AccountObjectGroupListCode ,
                RSNS.AccountObjectCategoryName
        HAVING  SUM(DebitAmountOC) <> 0
                OR SUM(DebitAmount) <> 0
                OR SUM(CreditAmountOC) <> 0
                OR SUM(CreditAmount) <> 0
                OR SUM(OpenningDebitAmountOC - OpenningCreditAmountOC) <> 0
                OR SUM(OpenningDebitAmount - OpenningCreditAmount) <> 0 
		OPTION (RECOMPILE)       
    END

