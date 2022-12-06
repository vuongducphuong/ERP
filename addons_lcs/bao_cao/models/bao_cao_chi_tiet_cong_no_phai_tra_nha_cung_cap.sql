--TH1: THỐNG KÊ THEO = KHÔNG CHỌN

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO



--=============================================
-- Author:		VTCHI
-- Create date: 02/07/2014
-- Description:	Lấy dữ liệu cho Báo cáo Chi tiết công nợ phải trả
-- Modified By NTGIANG 24.09.2014 Viết lại store (Tham khảo Proc_GLR_GetGLAccountLedger, Proc_GetCACashBook, Proc_INR_GetINInventoryBookDetail)
-- [dbo].[Proc_PUReport_PayableDetail] '9/15/2014', '9/23/2014', '02fa2e49-bf0d-4352-8405-c860c8135e93', 1, N'331', N',891977a4-7c2f-4181-b7ce-7659ee6d4cc9,b46c1c68-106e-44a1-ab15-fb083da4abc7,', N'VND', 0, 1
-- nvtoan modify 17/01/2015: Sửa lỗi không lấy cặp định khoản chênh lệch giá
-- nvtoan modify 26/02/2015: Sửa lỗi chọn tk tất cả đang lấy cả dữ liệu tk tổng hợp, không tính đúng số dư cuối kỳ
-- VHAnh modified 11.11.2015: Bổ sung Mã, Tên nhóm KH/NCC (CR 73635) 
-- NBHIEU modified 13/05/2016 : Nếu là đánh giá lại tk ngoại tệ và quyết định 15 thì lấy tỷ giá dưới chi tiết
-- VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá khi trên báo cáo có dòng xử lý chênh lệch tỷ giá (bug 109651).
-- PTPHUONG2 MODIFY 01/04/2017 Thêm tham số cộng gộp các dòng tiền thuế có bút toán giống nhau (PBI 13154)
--PTPHUONG2 MODIFY 04/04/2017 bỏ trường DetailRefID này, vì ko cần thiết >> ảnh hưởng tới kết quả sắp xếp dữ liệu. (PBI 13154)
--PTPHUONG2 Modify 05/04/2017 bổ sung 10 trường mở rộng chi tiết (PBI 86518)
/*ntlieu 10/04/2017 - sửa bug 92352: Lỗi với khi tích chọn cộng gộp các bút toán thuế giống nhau thì số dư đầu kỳ ko tính được phần số dư nhập tại chức năng nhập số dư đầu kỳ*/
-- DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
--Comment by hoant do rollback lại sửa lỗi của khánh 26.07.2017
-- DDKhanh CR128285 17/08/2017 với chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo
--Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
/*hoant 27.09.2017 sửa theo cr 138363 Bổ sung thêm cột Đơn vị chính (ĐVC), Số lượng theo ĐVC, Đơn giá theo ĐVC*/
/*ntlieu 12/10/2017 sửa bug 150977: Với chứng từ bán trả lại đại lý bán đúng giá, nhận ủy thác xuất khẩu thì số lượng hiển thị số âm*/
/*ntlieu 11.1.2018	hỗ trợ JIRA SMESEVEN-15039: Với dữ liệu lớn ko biết vì sao select dữ liệu trả về sort ko đúng nên dữ liệu trả về luôn sort*/
/*ntquang 26.03.2018 Thi công CR195226 - khi công gộp : Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
-- =============================================

DECLARE		 @FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@BranchID UNIQUEIDENTIFIER -- Chi nhánh
DECLARE			@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(20)-- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhà cung cấp
DECLARE			@CurrencyID NVARCHAR(3) -- Loại tiền
DECLARE			@IsSimilarSum BIT  -- Có cộng gộp các bút toán giống nhau không? 
DECLARE			@IsWorkingWithManagementBook BIT  --  Có dùng sổ quản trị hay không?
DECLARE			@IsSumSameTaxAccount BIT -- có cộng gộp các dòng tiền thuế có bút toán giống nhau ko? ptphuong2 01/04/2017




SET		@FromDate = '2018-01-01 00:00:00'
SET                                 @ToDate = '2018-12-31 23:59:59'
SET                                 @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET                                 @IncludeDependentBranch = 1
SET                                 @AccountNumber = NULL
SET                                 @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
SET                                 @CurrencyID = N'VND'
SET                                 @IsSimilarSum = 0 
SET                                 @IsWorkingWithManagementBook = 0
   SET                              @IsSumSameTaxAccount = 0


    BEGIN
        DECLARE @ID UNIQUEIDENTIFIER
        SET @ID = '00000000-0000-0000-0000-000000000000'
        
        DECLARE @AccountingSystem INT
        SELECT TOP 1
                @AccountingSystem = OptionValue
        FROM    dbo.SYSDBOption
        WHERE   OptionID LIKE N'%AccountingSystem%'
        
        DECLARE @tblBrandIDList TABLE
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(20) ,
              BranchName NVARCHAR(128)
            )	
       
        INSERT  INTO @tblBrandIDList
                SELECT  FGDBBI.BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID, @IncludeDependentBranch) AS FGDBBI
               
        -- vhanh added 11/11/2015: Lấy thêm mã nhóm và tên nhóm KH/NCC       
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các khách hàng --DS_KHACH_HANG_NCC
            (
              AccountObjectID UNIQUEIDENTIFIER , 
              AccountObjectCode NVARCHAR(25) ,--
              AccountObjectName NVARCHAR(255) ,
              AccountObjectAddress NVARCHAR(255) ,
              AccountObjectTaxCode NVARCHAR(200) ,
              AccountObjectGroupListCode NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
                                                       NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
                                                       NULL -- Danh sách tên nhóm
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  AccountObjectID ,--id
                        AO.AccountObjectCode , --MA
                        AO.AccountObjectName ,--HO_VA_TEN
                        AO.Address , --DIA_CHI
                        AO.CompanyTaxCode , --MA_SO_THUE
                        AccountObjectGroupListCode , -- Danh sách mã nhóm
                        AccountObjectGroupListName -- Danh sách tên nhóm   
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID, ',') tblAccountObjectSelected
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = tblAccountObjectSelected.Value		
                        
      
                                      
		-- Bảng chứa kết quả cần lấy
        CREATE TABLE #tblResult
            (
              RowNum INT IDENTITY(1, 1)
                         PRIMARY KEY ,
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS ,   -- Mã NCC
              AccountObjectName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,	-- Tên NCC 
              AccountObjectGroupListCode NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
                                                       NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS
                                                       NULL , -- Danh sách tên nhóm              
              AccountObjectAddress NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS , -- Địa chỉ
              PostedDate DATETIME ,	-- Ngày hạch toán
              RefDate DATETIME , -- Ngày chứng từ
              RefNo NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS , -- Số chứng từ
              -- DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
              DueDate DATETIME , 
              --BTAnh bổ sung ngày 21/07/2015 (JIRA: SMEFIVE-2297)
              InvDate DATETIME ,
              InvNo NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              --
              RefType INT ,	--Loại chứng từ
              RefID UNIQUEIDENTIFIER , -- Mã chứng từ  
              --PTPHUONG2 bỏ trường này, vì ko cần thiết.                          
              --RefDetailID NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              JournalMemo NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS , -- Diễn giải
              AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS , -- Số tài khoản
              AccountCategoryKind INT , -- Tính chất tài khoản
              CorrespondingAccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS , --TK đối ứng
              ExchangeRate DECIMAL(18, 4) , --Tỷ giá
              DebitAmountOC MONEY ,	-- Phát sinh nợ
              DebitAmount MONEY , -- Phát sinh nợ quy đổi
              CreditAmountOC MONEY , -- Phát sinh có
              CreditAmount MONEY , -- Phát sinh có quy đổi
              ClosingDebitAmountOC MONEY , --Dư Nợ
              ClosingDebitAmount MONEY , --Dư Nợ Quy đổi
              ClosingCreditAmountOC MONEY ,	--Dư Có
              ClosingCreditAmount MONEY , --Dư Có quy đổi
              InventoryItemCode NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS , --Mã hàng
              InventoryItemName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS , --Tên hàng
              UnitName NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS , --DVT
              Quantity DECIMAL(22, 8) , --Số lượng
              UnitPrice DECIMAL(18, 4) , --Đơn giá    
              BranchName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              IsBold BIT , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
              OrderType INT ,
              GLJournalMemo NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
              DocumentIncluded NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              --ptphuong2 04/04/2017 BỔ sung 10 trường chi tiết mở rộng PBI 86518)
              CustomField1 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField2 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField3 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField4 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField5 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField6 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField7 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField8 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField9 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS ,
              CustomField10 NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
              /*hoant 27.09.2017 theo cr 138363*/   
               MainUnitName NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS , --DVT
              MainQuantity DECIMAL(22, 8) , --Số lượng
              MainUnitPrice DECIMAL(18, 4)  --Đơn giá   
              
            )
        
        -- Bảng chứa số tài khoản    
        DECLARE @tblAccountNumber TABLE
            (
              AccountNumber NVARCHAR(20) PRIMARY KEY ,
              AccountName NVARCHAR(255) ,
              AccountNumberPercent NVARCHAR(25) ,
              AccountCategoryKind INT
            )
        IF @AccountNumber IS NOT NULL --tai_khoan
            BEGIN
                INSERT  INTO @tblAccountNumber --TMP_TAI_KHOAN
                        SELECT  A.AccountNumber ,--SO_TAI_KHOAN
                                A.AccountName , --TEN_TAI_KHOAN
                                A.AccountNumber + '%' ,
                                A.AccountCategoryKind --TINH_CHAT
                        FROM    dbo.Account AS A --danh_muc_he_thong_tai_khoan
                        WHERE   AccountNumber = @AccountNumber  --SO_TAI_KHOAN" = tai_khoan
                        ORDER BY A.AccountNumber ,--SO_TAI_KHOAN
                                A.AccountName  --TEN_TAI_KHOAN
                
            END
        ELSE 
            BEGIN 
                INSERT  INTO @tblAccountNumber --TMP_TAI_KHOAN
                        SELECT  A.AccountNumber ,--SO_TAI_KHOAN
                                A.AccountName , --TEN_TAI_KHOAN
                                A.AccountNumber + '%' ,
                                A.AccountCategoryKind --TINH_CHAT
                        FROM    dbo.Account AS A --danh_muc_he_thong_tai_khoan
                        WHERE   DetailByAccountObject = 1  --CHI_TIET_THEO_DOI_TUONG
                                AND AccountObjectType = 0  --DOI_TUONG_SELECTION
                                AND IsParent = 0
                        ORDER BY A.AccountNumber , --SO_TAI_KHOAN
                                A.AccountName --TEN_TAI_KHOAN
            END
            
           --PTPHUONG2 01/04/2017 Tạo bảng chỉ chứa các tài khoản thuế (PBI 13154)
            
        SELECT  A.*
        INTO    #GLVoucherDetailForeignExchange
        FROM    GLVoucherDetailForeignExchange A
                INNER JOIN @tblListAccountObjectID B ON A.AccountObjectID = B.AccountObjectID
                INNER JOIN @tblAccountNumber ACC ON A.AccountNumber = ACC.AccountNumber
                
/*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/ 
        IF @IsSimilarSum = 0 -- Nếu không cộng gộp --CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU
            BEGIN
            INSERT  INTO #tblResult
                        ( AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          -- DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
                          DueDate ,
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          --RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi
                          InventoryItemCode , --Mã hàng
                          InventoryItemName , --Tên hàng
                          UnitName , --DVT
                          Quantity , --Số lượng
                          UnitPrice , --Đơn giá             
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName, -- Tên chi nhánh  
                          GLJournalMemo ,                        
                          --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                          DocumentIncluded  ,
                          --PTPHUONG2 05/04/2017 bổ sung 10 trường mở rộng chi tiết (PBI 86518)
                          CustomField1 ,
                          CustomField2 ,
                          CustomField3 ,
                          CustomField4 ,
                          CustomField5 ,
                          CustomField6 ,
                          CustomField7 ,
                          CustomField8 ,
                          CustomField9 ,
                          CustomField10,
                          /*hoant 27.09.2017 theo cr 138363*/    
                          MainUnitName , --DVT chính
						  MainQuantity  , --Số lượng ĐVC
						  MainUnitPrice --Đơn giá   ĐVC
                          
                        )
                        SELECT  AccountObjectID ,
                                AccountObjectCode ,   -- Mã NCC
                                AccountObjectName ,	-- Tên NCC
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                RSNS.PostedDate ,	-- Ngày hạch toán
                                RefDate , -- Ngày chứng từ
                                RefNo , -- Số chứng từ
                                -- DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
                                DueDate , 
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ
                                RSNS.RefID , -- Mã chứng từ   
                                --RefDetailID ,
                                JournalMemo , -- Diễn giải					  
                                AccountNumber , -- Số tài khoản
                                AccountCategoryKind , -- Tính chất tài khoản
                                CorrespondingAccountNumber , --TK đối ứng				  
                                ExchangeRate , --Tỷ giá				  
                                SUM(DebitAmountOC) ,	-- Phát sinh nợ
                                SUM(DebitAmount) , -- Phát sinh nợ quy đổi
                                SUM(CreditAmountOC) , -- Phát sinh có
                                SUM(CreditAmount) , -- Phát sinh có quy đổi
                                ( CASE WHEN AccountCategoryKind = 0 THEN SUM(ClosingDebitAmountOC) - SUM(ClosingCreditAmountOC)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingDebitAmountOC) - SUM(ClosingCreditAmountOC) ) > 0 THEN ( SUM(ClosingDebitAmountOC) - SUM(ClosingCreditAmountOC) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ            
                                ( CASE WHEN AccountCategoryKind = 0 THEN ( SUM(ClosingDebitAmount) - SUM(ClosingCreditAmount) )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingDebitAmount) - SUM(ClosingCreditAmount) ) > 0 THEN SUM(ClosingDebitAmount) - SUM(ClosingCreditAmount)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi 
                                ( CASE WHEN AccountCategoryKind = 1 THEN ( SUM(ClosingCreditAmountOC) - SUM(ClosingDebitAmountOC) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmountOC) - SUM(ClosingDebitAmountOC) ) > 0 THEN ( SUM(ClosingCreditAmountOC) - SUM(ClosingDebitAmountOC) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có
                                ( CASE WHEN AccountCategoryKind = 1 THEN ( SUM(ClosingCreditAmount) - SUM(ClosingDebitAmount) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmount) - SUM(ClosingDebitAmount) ) > 0 THEN ( SUM(ClosingCreditAmount) - SUM(ClosingDebitAmount) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi 
                                  /*hoant 27.09.2017 theo cr 138363 bổ sung các refType 3552,3553,3554,3555*/                                                             
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.InventoryItemCode
                                END AS InventoryItemCode , --Mã hàng
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.InventoryItemName
                                END  AS InventoryItemName , --Tên hàng                                
                                 CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.UnitName
                                END AS   UnitName , --DVT                                
                               
                                /*hoant 27.09.2017 theo cr 138363 bổ sung các refType 3552,3553,3554,3555*/                                                             
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                      /*DDKhanh CR128285 17/08/2017 với chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo*/
                                      /*ntlieu 12/10/2017 sửa bug 150977: Với chứng từ bán trả lại đại lý bán đúng giá, nhận ủy thác xuất khẩu thì số lượng hiển thị số âm*/
                                      WHEN RSNS.Reftype IN ( 3030, 3031, 3032, 3033, 3542, 3543, 3544, 3545) --giảm giá hàng mua
											THEN RSNS.Quantity * (-1)
                                     ELSE Quantity
                                END , --Số lượng
                                /*hoant 27.09.2017 theo cr 138363 bổ sung các refType 3552,3553,3554,3555*/                                                             
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     ELSE UnitPrice
                                END , --Đơn giá                   
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName, -- Tên chi nhánh                                  
                                GLJournalMemo ,                                
                                --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                                DocumentIncluded  ,
                                --PTPHUONG2 BỔ SUNG 10 Trường mở rộng chi tiết (PBI 86518)
                                ISNULL(RSNS.CustomField1, '') AS CustomField1 ,
                                ISNULL(RSNS.CustomField2, '') AS CustomField2 ,
                                ISNULL(RSNS.CustomField3, '') AS CustomField3 ,
                                ISNULL(RSNS.CustomField4, '') AS CustomField4 ,
                                ISNULL(RSNS.CustomField5, '') AS CustomField5 ,
                                ISNULL(RSNS.CustomField6, '') AS CustomField6 ,
                                ISNULL(RSNS.CustomField7, '') AS CustomField7 ,
                                ISNULL(RSNS.CustomField8, '') AS CustomField8 ,
                                ISNULL(RSNS.CustomField9, '') AS CustomField9 ,
                                ISNULL(RSNS.CustomField10, '') AS CustomField10   
                                  /*hoant 27.09.2017 theo cr 138363*/                                                             
                                  ,
                                   CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.MainUnitName
									END AS MainUnitName                                    
                                  ,
                                    CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                      /* chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo*/
                                      /*ntlieu 12/10/2017 sửa bug 150977: Với chứng từ bán trả lại đại lý bán đúng giá, nhận ủy thác xuất khẩu thì số lượng hiển thị số âm*/
                                      WHEN RSNS.Reftype IN ( 3030, 3031, 3032, 3033, 3542, 3543, 3544, 3545 )
											THEN RSNS.MainQuantity * (-1)
                                     ELSE MainQuantity
									END AS MainQuantity                                  
                                  ,
                                   CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua
                                          THEN NULL
                                     ELSE MainUnitPrice
								  END AS MainUnitPrice
                                  
                                  
                        FROM    ( SELECT    AOL.AccountObjectID , --DOI_TUONG_ID
                                            LAOI.AccountObjectCode ,   -- Mã NCC --MA
                                            LAOI.AccountObjectName ,	-- Tên NCC lấy trên danh mục -- HO_VA_TEN
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            LAOI.AccountObjectAddress , -- Địa chỉ   --DIA_CHI
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL --NGAY_HACH_TOAN
                                                 ELSE AOL.PostedDate --
                                            END AS PostedDate , -- Ngày hạch toán    --NGAY_HACH_TOAN                             
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn --NGAY_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn   --SO_CHUNG_TU                                  
                                    --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
											CASE WHEN AOL.PostedDate < @FromDate THEN NULL
											ELSE AOL.DueDate
											END AS DueDate ,
                                    --BTAnh-21/07/2015
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID ,
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ 
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate 
												      OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												      THEN NULL
                                                 ELSE CAST(AOL.RefDetailID AS NVARCHAR(50))
                                            END AS RefDetailID ,
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = Thuế GTGT của hàng hóa dịch vụ*/
                                            CASE WHEN AOL.PostedDate < @FromDate THEN N'Số dư đầu kỳ'
												 WHEN @IsSumSameTaxAccount = 1  --CONG_GOP_CAC_BUT_TOAN_THUE_GIONG_NHAU
													  AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%') --AOL."MA_TK_DOI_UNG" LIKE '3331%' OR AOL."MA_TK_DOI_UNG" LIKE '133%'
													  THEN N'Thuế GTGT của hàng hóa, dịch vụ'
                                                 ELSE AOL.Description --DIEN_GIAI
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Detail)    --DIEN_GIAI_CHUNG  
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN 
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --
                                            END AS CorrespondingAccountNumber , --TK đối ứng   --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE ( CASE WHEN AOL.RefType = 4016 THEN ( CASE WHEN @AccountingSystem = 15 THEN ( SELECT  ISNULL(GLD.ExchangeRate, 0)
                                                                                                                                    FROM    #GLVoucherDetailForeignExchange AS GLD
                                                                                                                                    WHERE   GLD.RefID = AOL.RefID
                                                                                                                                            AND GLD.AccountNumber = AOL.AccountNumber
                                                                                                                                            AND ISNULL(GLD.AccountObjectID, @ID) = ISNULL(AOL.AccountObjectID, @ID)
                                                                                                                                    GROUP BY ISNULL(GLD.ExchangeRate, 0)
                                                                                                                                  )
                                                                                                 ELSE AOL.ExchangeRate
                                                                                            END )
                                                             ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/ CASE WHEN AOL.CashOutExchangeRateLedger IS NULL THEN AOL.ExchangeRate
                                                                                                                             ELSE AOL.CashOutExchangeRateLedger
                                                                                                                        END
                                                        END )
                                            END AS ExchangeRate , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                 ELSE AOL.DebitAmountOC --GHI_NO_NGUYEN_TE
                                            END AS DebitAmountOC , -- Phát sinh nợ                                    
                                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                 ELSE AOL.DebitAmount --GHI_NO
                                            END AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                 ELSE AOL.CreditAmountOC --GHI_CO_NGUYEN_TE
                                            END AS CreditAmountOC , -- Phát sinh có  
                                            CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                 ELSE AOL.CreditAmount -- GHI_CO
                                            END AS CreditAmount , -- Phát sinh có quy đổi
                                            CASE WHEN AOL.PostedDate < @FromDate THEN AOL.DebitAmountOC
                                                 ELSE $0
                                            END AS ClosingDebitAmountOC , --Dư Nợ            
                                            CASE WHEN AOL.PostedDate < @FromDate THEN AOL.DebitAmount
                                                 ELSE $0
                                            END AS ClosingDebitAmount , --Dư Nợ Quy đổi 
                                            CASE WHEN AOL.PostedDate < @FromDate THEN AOL.CreditAmountOC
                                                 ELSE $0
                                            END AS ClosingCreditAmountOC , --Dư Có
                                            CASE WHEN AOL.PostedDate < @FromDate THEN AOL.CreditAmount
                                                 ELSE $0
                                            END AS ClosingCreditAmount , --Dư Có quy đổi  
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL
                                                 ELSE AOL.InventoryItemCode
                                            END AS InventoryItemCode , --Mã hàng 
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate 
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL
                                                 ELSE I.InventoryItemName -- nmtruong 23/10/2015: sửa lỗi 74867 lấy mặt hàng trên danh mục
                                         --ELSE AOL.DESCRIPTION  -- nmtruong 24/8/2015 sửa theo lỗi 66972: nếu không cộng gộp thì lấy tên mặt hàng tên giao diện
                                            END AS InventoryItemName , --Tên hàng
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL
                                                 ELSE UN.UnitName
                                            END AS UnitName , -- DVT 
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL
                                                 ELSE AOL.Quantity
                                            END AS Quantity , -- Số lượng 
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                      OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL
                                                 ELSE ( CASE WHEN @CurrencyID IS NULL THEN AOL.UnitPrice
                                                             ELSE AOL.UnitPriceOC
                                                        END )
                                            END AS UnitPrice , -- Đơn giá 
                                            CASE WHEN AOL.PostedDate < @FromDate THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.JournalMemo
                                            END AS GLJournalMemo ,
                                            
                                            --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)                                            
                                              CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                 ELSE AOL.DocumentIncluded 
                                            END AS DocumentIncluded ,                                                                                         
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Khi tích chọn cộng gộp các bút toán thuế giống nhau thì gán giá trị = NULL hoặc trắng*/
                                            CASE WHEN AOL.PostedDate < @FromDate 
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField1, '') 
											END AS CustomField1 ,
											CASE WHEN AOL.PostedDate < @FromDate 
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField2, '') 
											END AS CustomField2 ,
											CASE WHEN AOL.PostedDate < @FromDate
														OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField3, '') 
											END AS CustomField3 ,
											CASE WHEN AOL.PostedDate < @FromDate 
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												THEN '' 
												ELSE ISNULL(CFL.CustomField4, '') 
											END AS CustomField4 ,
											CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField5, '') 
											END AS CustomField5 ,
											CASE WHEN AOL.PostedDate < @FromDate 
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												THEN '' 
												ELSE ISNULL(CFL.CustomField6, '') 
											END AS CustomField6 ,
											CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField7, '') 
											END AS CustomField7 ,
											CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												THEN '' 
												ELSE ISNULL(CFL.CustomField8, '') 
											END AS CustomField8 ,
											CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField9, '') 
											END AS CustomField9 ,
											CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
												THEN '' 
												ELSE ISNULL(CFL.CustomField10, '') 
											END AS CustomField10,
											
											--xử lý thêm để trường hợp số dư đầu kỳ, sẽ để giống nhau giữa cộng gộp và ko cộng gộp tiền thuế 
                                                              -->> để chỉ có 1 dòng số dư đầu kỳ duy nhất
											  CASE WHEN AOL.PostedDate < @FromDate THEN 2
												   WHEN (@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 ) 
														THEN 1
													ELSE 0
											  END AS GroupOrder ,
											  CASE WHEN AOL.PostedDate < @FromDate THEN ''
													WHEN (@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
														THEN AOL.InvNo + '_' + AOL.CorrespondingAccountNumber
													ELSE ''
											  END AS AccountNoToOrder ,
											  CASE WHEN AOL.PostedDate < @FromDate
														THEN 2
													WHEN (@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
														 THEN 0
													ELSE AOL.SortOrder
											  END AS SortOrder ,
											  CASE
											  WHEN AOL.PostedDate < @FromDate 
													THEN 2
													WHEN (@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
														 THEN 0
													ELSE AOL.DetailPostOrder
											  END AS DetailPostOrder  
											  /*hoant 27.09.2017 theo cr 138363*/
											  /*Đơn vị chính (ĐVC),SL theo đơn vị tính chính, Đơn giá theo ĐVC
												
											*/
											  ,
											  CASE WHEN AOL.PostedDate < @FromDate  THEN NULL ELSE MainUnit.UnitName end AS MainUnitName,											  											
											  CASE WHEN AOL.PostedDate < @FromDate
													  OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL  ELSE AOL.MainQuantity END AS MainQuantity , -- Số lượng  theo đơn vị tính chính                                                
                                             CASE WHEN AOL.PostedDate < @FromDate
                                                      OR (	
															@IsSumSameTaxAccount = 1 
															AND (CorrespondingAccountNumber LIKE '3331%' OR CorrespondingAccountNumber LIKE '133%')
														 )
												 THEN NULL
                                                 ELSE ( CASE WHEN @CurrencyID IS NULL THEN AOL.MainUnitPrice
                                                             ELSE AOL.MainUnitPriceOC
                                                        END )
                                            END AS MainUnitPrice
											  
                                  FROM      dbo.AccountObjectLedger AS AOL --so_cong_no_chi_tiet
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent --TMP_TAI_KHOAN AS TBAN ON AOL."MA_TK" LIKE  TBAN."AccountNumberPercent"
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber --danh_muc_he_thong_tai_khoan AS AN ON AOL."MA_TK" = AN."SO_TAI_KHOAN"
                                            INNER JOIN @tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID --DS_KHACH_HANG_NCC AS LAOI ON AOL."DOI_TUONG_ID" = LAOI.id
                                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID --
                                            LEFT JOIN dbo.InventoryItem I ON I.InventoryItemID = AOL.InventoryItemID --Lấy lên tên hàng từ danh mục --danh_muc_vat_tu_hang_hoa I ON I.id = AOL."MA_HANG_ID"                                        
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT --danh_muc_don_vi_tinh AS UN ON AOL."DVT_ID" = UN.id
                                            /*hoant 27.09.2017 theo cr 138363*/
                                            LEFT JOIN dbo.Unit AS MainUnit ON AOL.MainUnitID = MainUnit.UnitID -- Danh mục ĐVT chính -- danh_muc_don_vi_tinh AS MainUnit ON AOL."DVT_CHINH_ID" = MainUnit.id
                                            --PTPHUONG2 BỔ SUNG 10 Trường mở rộng chi tiết (PBI 86518)
                                            /*ntlieu 10/04/2017 - sửa bug 92352: Lấy thông tin trường mở rộng tại vòng trong cùng*/
                                            LEFT JOIN CustomFieldLedger CFL ON AOL.RefDetailID = CFL.RefDetailID AND CFL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                  WHERE     AOL.PostedDate <= @ToDate
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL --loai_tien_id
                                                  OR AOL.CurrencyID = @CurrencyID
                                                )
                                            AND AN.DetailByAccountObject = 1 --CHI_TIET_THEO_DOI_TUONG
                                            AND AN.AccountObjectType = 0 --DOI_TUONG_SELECTION
                                ) AS RSNS                               
                        GROUP BY RSNS.AccountObjectID , --DOI_TUONG_ID
                                RSNS.AccountObjectCode ,   -- Mã NCC -- MA
                                RSNS.AccountObjectName ,	-- Tên NCC --HO_VA_TEN
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                RSNS.AccountObjectAddress , -- Địa chỉ--DIA_CHI
                                RSNS.PostedDate ,	-- Ngày hạch toán -- NGAY_HACH_TOAN
                                RSNS.RefDate , -- Ngày chứng từ  --NGAY_CHUNG_TU
                                RSNS.RefNo , -- Số chứng từ --SO_CHUNG_TU
                                --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
								RSNS.DueDate , 
                                RSNS.InvDate ,
                                RSNS.InvNo ,
                                RSNS.RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RSNS.RefID , -- Mã chứng từ   --ID_CHUNG_TU
                                --RSNS.RefDetailID ,
                                RSNS.JournalMemo , -- Diễn giải		--DIEN_GIAI_CHUNG			  
                                RSNS.AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                RSNS.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                RSNS.CorrespondingAccountNumber , --TK đối ứng				  
                                RSNS.ExchangeRate , --Tỷ giá
                                      /*hoant 27.09.2017 theo cr 138363 bổ sung các refType 3552,3553,3554,3555*/                                                             
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.InventoryItemCode
                                END  , --Mã hàng
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.InventoryItemName
                                END   , --Tên hàng                                
                                 CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.UnitName
                                END  , --DVT                                
                               
                                /*hoant 27.09.2017 theo cr 138363 bổ sung các refType 3552,3553,3554,3555*/                                                             
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                      /*DDKhanh CR128285 17/08/2017 với chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo*/
                                      /*ntlieu 12/10/2017 sửa bug 150977: Với chứng từ bán trả lại đại lý bán đúng giá, nhận ủy thác xuất khẩu thì số lượng hiển thị số âm*/
                                      WHEN RSNS.Reftype IN ( 3030, 3031, 3032, 3033, 3542, 3543, 3544, 3545 ) --giảm giá hàng mua
											THEN RSNS.Quantity * (-1)
                                     ELSE Quantity
                                END , --Số lượng
                                /*hoant 27.09.2017 theo cr 138363 bổ sung các refType 3552,3553,3554,3555*/                                                             
                                CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     ELSE UnitPrice
                                END , --Đơn giá    
                                /*
                                RSNS.InventoryItemCode , --Mã hàng
                                RSNS.InventoryItemName , --Tên hàng
                                RSNS.UnitName , --DVT
                                RSNS.Quantity , --Số lượng
                                RSNS.UnitPrice , --Đơn giá   
                                */
                                RSNS.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                RSNS.OrderType ,
                                BranchName ,
                                GLJournalMemo ,
                                RSNS.GroupOrder , -- Trường này dùng để sắp xếp ưu tiên giữa tiền hàng và tiền thuế
                                RSNS.AccountNoToOrder , -- trường này dùng để sắp xếp ưu tiên giữa các tài khoản thuế với nhau, khi cộng gộp.
                                RSNS.SortOrder ,
                                RSNS.DetailPostOrder ,
                                RSNS.DocumentIncluded, --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                                RSNS.CustomField1 ,
                                RSNS.CustomField2 ,
                                RSNS.CustomField3 ,
                                RSNS.CustomField4 ,
                                RSNS.CustomField5 ,
                                RSNS.CustomField6 ,
                                RSNS.CustomField7 ,
                                RSNS.CustomField8 ,
                                RSNS.CustomField9 ,
                                RSNS.CustomField10
                                   /*hoant 27.09.2017 theo cr 138363*/                                                             
                                  ,
                                   CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                     
                                     ELSE RSNS.MainUnitName
									END                                    
                                  ,
                                    CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua, giảm giá hàng bán đại lý bán đúng giá, giảm giá hàng bán ủy thác xuất khẩu.
                                          THEN NULL
                                      /* chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo*/
                                      /*ntlieu 12/10/2017 sửa bug 150977: Với chứng từ bán trả lại đại lý bán đúng giá, nhận ủy thác xuất khẩu thì số lượng hiển thị số âm*/
                                      WHEN RSNS.Reftype IN ( 3030, 3031, 3032, 3033, 3542, 3543, 3544, 3545 )
											THEN RSNS.MainQuantity * (-1)
                                     ELSE MainQuantity
									END                                   
                                  ,
                                   CASE WHEN CorrespondingAccountNumber LIKE '33311%'
                                          OR CorrespondingAccountNumber LIKE '1331%'
                                          OR CorrespondingAccountNumber LIKE '1332%'
                                          OR CorrespondingAccountNumber LIKE '521%'
                                          OR Reftype IN ( 3040, 3041, 3042, 3043,3552,3553,3554,3555 ) --giảm giá hàng mua
                                          THEN NULL
                                     ELSE MainUnitPrice
								  END 
                                  
                        HAVING  SUM(DebitAmountOC) <> 0
                                OR SUM(DebitAmount) <> 0
                                OR SUM(CreditAmountOC) <> 0
                                OR SUM(CreditAmount) <> 0
                                OR SUM(ClosingDebitAmountOC - ClosingCreditAmountOC) <> 0
                                OR SUM(ClosingDebitAmount - ClosingCreditAmount) <> 0
                        ORDER BY RSNS.AccountObjectCode ,
                                RSNS.AccountNumber ,
                                RSNS.OrderType ,
                                RSNS.PostedDate ,
                                RSNS.RefDate ,
                                RSNS.RefNo ,
                                --Sắp xếp theo trường mở rộng để sắp xếp
                                RSNS.GroupOrder , -- Trường này dùng để sắp xếp ưu tiên giữa tiền hàng và tiền thuế
                                RSNS.AccountNoToOrder , -- trường này dùng để sắp xếp ưu tiên giữa các tài khoản thuế với nhau, khi cộng gộp.
                                RSNS.SortOrder ,
                                RSNS.DetailPostOrder
                OPTION  ( RECOMPILE )                
            END
        ELSE -- Cộng gộp các bút toán giống nhau
            BEGIN
                INSERT  INTO #tblResult
                        ( AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
                          DueDate , 
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          --RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi               
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName -- Tên chi nhánh     
                          ,
                          GLJournalMemo   ,
                          DocumentIncluded  --Số chứng từ gốc kèm theo   
                         
                        )
                        SELECT  AccountObjectID , --DOI_TUONG_ID
                                AccountObjectCode ,   -- Mã NCC --MA
                                AccountObjectName ,	-- Tên NCC --HO_VA_TEN
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ --DIA_CHI
                                PostedDate ,	-- Ngày hạch toán -- NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
								DueDate , 
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ    ---ID_CHUNG_TU
                                --RefDetailID ,
                                JournalMemo , -- Diễn giải	-- 		DIEN_GIAI_CHUNG		  
                                AccountNumber , -- Số tài khoản -- SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản -- TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng	 --	MA_TAI_KHOAN_DOI_UNG		  
                                ExchangeRate , --Tỷ giá				  
                                DebitAmountOC ,	-- Phát sinh nợ --  GHI_NO_NGUYEN_TE
                                DebitAmount , -- Phát sinh nợ quy đổi -- GHI_NO
                                CreditAmountOC , -- Phát sinh có --GHI_CO_NGUYEN_TE
                                CreditAmount , -- Phát sinh có quy đổi --GHI_CO
                                ( CASE WHEN AccountCategoryKind = 0 THEN ( ClosingDebitAmountOC - ClosingCreditAmountOC )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( ClosingDebitAmountOC - ClosingCreditAmountOC ) > 0 THEN ClosingDebitAmountOC - ClosingCreditAmountOC
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ     --ClosingDebitAmountOC
                                ( CASE WHEN AccountCategoryKind = 0 THEN ( ClosingDebitAmount - ClosingCreditAmount )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( ClosingDebitAmount - ClosingCreditAmount ) > 0 THEN ClosingDebitAmount - ClosingCreditAmount
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi  -- ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1 THEN ( ClosingCreditAmountOC - ClosingDebitAmountOC )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmountOC - ClosingDebitAmountOC ) > 0 THEN ( ClosingCreditAmountOC - ClosingDebitAmountOC )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có -- ClosingCreditAmountOC
                                ( CASE WHEN AccountCategoryKind = 1 THEN ( ClosingCreditAmount - ClosingDebitAmount )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmount - ClosingDebitAmount ) > 0 THEN ( ClosingCreditAmount - ClosingDebitAmount )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi   --ClosingCreditAmount
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName ,
                                GLJournalMemo,
                                DocumentIncluded --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                                
                        FROM    ( SELECT    AD.AccountObjectID , -- DOI_TUONG_ID
                                            AD.AccountObjectCode ,   -- Mã NCC --MA
                                            AD.AccountObjectName ,	-- Tên NCC lấy trên danh mục --HO_VA_TEN
                                            AD.AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AD.AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AD.AccountObjectAddress , -- Địa chỉ  --DIA_CHI
                                            AD.PostedDate , -- Ngày hạch toán    --  NGAY_HACH_TOAN                                                      
                                            AD.RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn--NGAY_CHUNG_TU
                                            AD.RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  --SO_CHUNG_TU
                                            --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
											AD.DueDate ,
                                            AD.InvDate ,
                                            AD.InvNo ,
                                            AD.RefID , --ID_CHUNG_TU
                                            AD.RefType , --Loại chứng từ  --LOAI_CHUNG_TU
                                            --MAX(AD.RefDetailID) AS RefDetailID ,
                                            AD.JournalMemo , -- Diễn giải (lấy diễn giải Master)     --DIEN_GIAI_CHUNG
                                            AD.AccountNumber , -- TK công nợ --SO_TAI_KHOAN 
                                            AD.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            AD.CorrespondingAccountNumber , --TK đối ứng   --MA_TAI_KHOAN_DOI_UNG
                                            AD.ExchangeRate , --Tỷ giá 
                                            SUM(AD.DebitAmountOC) AS DebitAmountOC , -- Phát sinh nợ           --       GHI_NO_NGUYEN_TE                  
                                            SUM(AD.DebitAmount) AS DebitAmount , -- Phát sinh nợ quy đổi        --GHI_NO                         
                                            SUM(AD.CreditAmountOC) AS CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                            SUM(AD.CreditAmount) AS CreditAmount , -- Phát sinh có quy đổi  -- GHI_CO
                                            SUM(AD.ClosingDebitAmountOC) AS ClosingDebitAmountOC , --Dư Nợ            
                                            SUM(AD.ClosingDebitAmount) AS ClosingDebitAmount , --Dư Nợ Quy đổi 
                                            SUM(AD.ClosingCreditAmountOC) AS ClosingCreditAmountOC , --Dư Có
                                            SUM(AD.ClosingCreditAmount) AS ClosingCreditAmount , --Dư Có quy đổi 
                                            AD.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            AD.OrderType ,
                                            AD.BranchName ,
                                            AD.GLJournalMemo ,
                                            AD.DetailPostOrder,
                                            AD.DocumentIncluded --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                                  FROM      ( SELECT    AOL.AccountObjectID , --DOI_TUONG_ID
                                                        LAOI.AccountObjectCode ,   -- Mã NCC --MA
                                                        LAOI.AccountObjectName ,	-- Tên NCC lấy trên danh mục --HO_VA_TEN
                                                        AccountObjectGroupListCode , -- Danh sách mã nhóm
                                                        AccountObjectGroupListName , -- Danh sách tên nhóm              
                                                        LAOI.AccountObjectAddress , -- Địa chỉ  --DIA_CHI
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.PostedDate --NGAY_HACH_TOAN
                                                        END AS PostedDate , -- Ngày hạch toán                                                            
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE RefDate --NGAY_CHUNG_TU
                                                        END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.RefNo--SO_CHUNG_TU
                                                        END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                                        --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
														CASE WHEN AOL.PostedDate < @FromDate THEN NULL
														ELSE AOL.DueDate
														END AS DueDate , -- Hạn thanh toán
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.InvDate
                                                        END AS InvDate ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.InvNo
                                                        END AS InvNo ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.RefID --ID_CHUNG_TU
                                                        END AS RefID ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.RefType --LOAI_CHUNG_TU
                                                        END AS RefType , --Loại chứng từ 
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE CAST(RefDetailID AS NVARCHAR(50))
                                                        END AS RefDetailID ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN N'Số dư đầu kỳ'
                                                              /*ntquang 26.03.2018 Thi công CR195226 - khi công gộp : Sửa lại cách lấy dữ liệu cho trường diễn giải với dòng có tài khoản đối ứng là tk thuế (133, 3331) */
                                                             ELSE CASE WHEN AOL.CorrespondingAccountNumber LIKE '133%' OR AOL.CorrespondingAccountNumber LIKE '3331%' THEN N'Thuế GTGT của hàng hóa, dịch vụ' ELSE  AOL.JournalMemo END  --DIEN_GIAI_CHUNG                                                         
                                                             --ELSE AOL.JournalMemo                        
                                                        END AS JournalMemo , -- Diễn giải (lấy diễn giải Master) --DIEN_GIAI_CHUNG
                                                        TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                                        TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.CorrespondingAccountNumber
                                                        END AS CorrespondingAccountNumber , --TK đối ứng   
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE ( CASE WHEN AOL.RefType = 4016 THEN ( CASE WHEN @AccountingSystem = 15 THEN ( SELECT  ISNULL(GLD.ExchangeRate, 0)
                                                                                                                                                FROM    #GLVoucherDetailForeignExchange AS GLD
                                                                                                                                                WHERE   GLD.RefID = AOL.RefID
                                                                                                                                                        AND GLD.AccountNumber = AOL.AccountNumber
                                                                                                                                                        AND ISNULL(GLD.AccountObjectID, @ID) = ISNULL(AOL.AccountObjectID, @ID)
                                                                                                                                                GROUP BY ISNULL(GLD.ExchangeRate, 0)
                                                                                                                                              )
                                                                                                             ELSE AOL.ExchangeRate
                                                                                                        END )
                                                                         ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/ CASE WHEN AOL.CashOutExchangeRateLedger IS NULL THEN AOL.ExchangeRate
                                                                                                                                         ELSE AOL.CashOutExchangeRateLedger
                                                                                                                                    END
                                                                    END )
                                                        END AS ExchangeRate , --Tỷ giá 
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                             ELSE AOL.DebitAmountOC --GHI_NO_NGUYEN_TE
                                                        END AS DebitAmountOC , -- Phát sinh nợ                                    
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                             ELSE AOL.DebitAmount --GHI_NO
                                                        END AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                             ELSE AOL.CreditAmountOC --GHI_CO_NGUYEN_TE
                                                        END AS CreditAmountOC , -- Phát sinh có  
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN $0
                                                             ELSE AOL.CreditAmount --GHI_CO
                                                        END AS CreditAmount , -- Phát sinh có quy đổi
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN AOL.DebitAmountOC
                                                             ELSE $0
                                                        END AS ClosingDebitAmountOC , --Dư Nợ     --   ClosingDebitAmountOC     
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN AOL.DebitAmount
                                                             ELSE $0
                                                        END AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN AOL.CreditAmountOC
                                                             ELSE $0
                                                        END AS ClosingCreditAmountOC , --Dư Có -- ClosingCreditAmountOC
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN AOL.CreditAmount
                                                             ELSE $0
                                                        END AS ClosingCreditAmount , --Dư Có quy đổi  --ClosingCreditAmount
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN 1
                                                             ELSE 0
                                                        END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN 0
                                                             ELSE 1
                                                        END AS OrderType ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE BIDL.BranchName
                                                        END BranchName ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.JournalMemo
                                                        END AS GLJournalMemo ,
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.DetailPostOrder
                                                        END AS DetailPostOrder,
                                                        --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                                                        CASE WHEN AOL.PostedDate < @FromDate THEN NULL
                                                             ELSE AOL.DocumentIncluded
                                                        END AS DocumentIncluded
                                                        
                                              FROM      dbo.AccountObjectLedger AS AOL
                                                        INNER JOIN @tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                                        INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                                                        INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                                                        INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                                        LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                              WHERE     AOL.PostedDate <= @ToDate
                                                        AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                                        AND ( @CurrencyID IS NULL
                                                              OR AOL.CurrencyID = @CurrencyID
                                                            )
                                                        AND AN.DetailByAccountObject = 1
                                                        AND AN.AccountObjectType = 0
                                            ) AS AD
                                  GROUP BY  AD.AccountObjectID , --DOI_TUONG_ID
                                            AD.AccountObjectCode ,   -- Mã NCC --MA
                                            AD.AccountObjectName ,	-- Tên NCC lấy trên danh mục --HO_VA_TEN
                                            AD.AccountObjectGroupListCode , -- Danh sách mã nhóm 
                                            AD.AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AD.AccountObjectAddress , -- Địa chỉ   --DIA_CHI
                                            AD.PostedDate , -- Ngày hạch toán   --NGAY_HACH_TOAN                                                         
                                            AD.RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn--NGAY_CHUNG_TU
                                            AD.RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn   --SO_CHUNG_TU
                                            --DDKhanh 24/04/2017(CR 27179): thêm trường hạn thanh toán
											AD.DueDate , 
                                            AD.InvDate ,
                                            AD.InvNo ,
                                            AD.RefID , --ID_CHUNG_TU
                                            AD.RefType , --Loại chứng từ  --LOAI_CHUNG_TU
                                            AD.JournalMemo , -- Diễn giải (lấy diễn giải Master)    --DIEN_GIAI_CHUNG 
                                            AD.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            AD.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            AD.CorrespondingAccountNumber , --TK đối ứng   
                                            AD.ExchangeRate , --Tỷ giá 
                                            AD.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            AD.OrderType ,
                                            AD.BranchName ,
                                            AD.GLJournalMemo ,
                                            AD.DetailPostOrder,
                                            AD.DocumentIncluded --Ntquang Modify 24/08/2017 bổ sung trường DocumentIncluded (PBI 119778)
                                ) AS RSS
                        WHERE   RSS.DebitAmountOC <> 0
                                OR RSS.CreditAmountOC <> 0
                                OR RSS.DebitAmount <> 0
                                OR RSS.CreditAmount <> 0
                                OR ClosingCreditAmountOC - ClosingDebitAmountOC <> 0
                                OR ClosingCreditAmount - ClosingDebitAmount <> 0
                        ORDER BY RSS.AccountObjectCode ,
                                RSS.AccountNumber ,
                                RSS.OrderType ,
                                RSS.PostedDate ,
                                RSS.RefDate ,
                                RSS.RefNo ,
                                RSS.DetailPostOrder
                OPTION  ( RECOMPILE )
            END

  
                        
/* Tính số tồn */
        DECLARE @CloseAmountOC AS DECIMAL(22, 8) ,
            @CloseAmount AS DECIMAL(22, 8) ,
            @AccountObjectCode_tmp NVARCHAR(100) ,
            @AccountNumber_tmp NVARCHAR(20)
        SELECT  @CloseAmountOC = 0 ,
                @CloseAmount = 0 ,
                @AccountObjectCode_tmp = N'' ,
                @AccountNumber_tmp = N''
        UPDATE  #tblResult
        SET     @CloseAmountOC = ( CASE WHEN OrderType = 0 THEN ( CASE WHEN ClosingDebitAmountOC = 0 THEN ClosingCreditAmountOC
                                                                       ELSE -1 * ClosingDebitAmountOC
                                                                  END )
                                        WHEN @AccountObjectCode_tmp <> AccountObjectCode
                                             OR @AccountNumber_tmp <> AccountNumber THEN CreditAmountOC - DebitAmountOC
                                        ELSE @CloseAmountOC + CreditAmountOC - DebitAmountOC
                                   END ) ,
                ClosingDebitAmountOC = ( CASE WHEN AccountCategoryKind = 0 THEN -1 * @CloseAmountOC
                                              WHEN AccountCategoryKind = 1 THEN $0
                                              ELSE CASE WHEN @CloseAmountOC < 0 THEN -1 * @CloseAmountOC
                                                        ELSE $0
                                                   END
                                         END ) ,
                ClosingCreditAmountOC = ( CASE WHEN AccountCategoryKind = 1 THEN @CloseAmountOC
                                               WHEN AccountCategoryKind = 0 THEN $0
                                               ELSE CASE WHEN @CloseAmountOC > 0 THEN @CloseAmountOC
                                                         ELSE $0
                                                    END
                                          END ) ,
                @CloseAmount = ( CASE WHEN OrderType = 0 THEN ( CASE WHEN ClosingDebitAmount = 0 THEN ClosingCreditAmount
                                                                     ELSE -1 * ClosingDebitAmount
                                                                END )
                                      WHEN @AccountObjectCode_tmp <> AccountObjectCode
                                           OR @AccountNumber_tmp <> AccountNumber THEN CreditAmount - DebitAmount
                                      ELSE @CloseAmount + CreditAmount - DebitAmount
                                 END ) ,
                ClosingDebitAmount = ( CASE WHEN AccountCategoryKind = 0 THEN -1 * @CloseAmount
                                            WHEN AccountCategoryKind = 1 THEN $0
                                            ELSE CASE WHEN @CloseAmount < 0 THEN -1 * @CloseAmount
                                                      ELSE $0
                                                 END
                                       END ) ,
                ClosingCreditAmount = ( CASE WHEN AccountCategoryKind = 1 THEN @CloseAmount
                                             WHEN AccountCategoryKind = 0 THEN $0
                                             ELSE CASE WHEN @CloseAmount > 0 THEN @CloseAmount
                                                       ELSE $0
                                                  END
                                        END ) ,
                @AccountObjectCode_tmp = AccountObjectCode ,
                @AccountNumber_tmp = AccountNumber
        WHERE   OrderType <> 2
        DROP TABLE #GLVoucherDetailForeignExchange
/*Lấy số liệu*/				
        SELECT  --ROW_NUMBER() OVER ( ORDER BY RS.AccountObjectCode, RS.AccountNumber, RS.OrderType, RS.PostedDate, RS.RefDate, RS.RefNo ) AS RowNum ,
                RS.*
        FROM    #tblResult RS
        ORDER BY RowNum
        /*ntlieu 11.1.2018	hỗ trợ JIRA SMESEVEN-15039: Với dữ liệu lớn ko biết vì sao select dữ liệu trả về sort ko đúng nên dữ liệu trả về luôn sort*/
        DROP TABLE #tblResult
    END				

GO

---------TH2: Thống kê theo nhân viên----------------------------

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		<HHSon>
-- Create date: <03/07/2014>
-- Description:	Lấy số liệu cho Báo cáo chi tiết công nợ phải trả theo nhân viên
-- Modified By NTGIANG 26.09.2014: Viết lại
-- Proc_PUR_GetPaymentableDetailByEmployee '9/1/2014', '9/30/2014', '02fa2e49-bf0d-4352-8405-c860c8135e93', 1, N'331', N',5937e94c-0ab9-43ca-b530-a8fa81408c32,7eb29509-07ba-4a1b-87f1-de6b987a911c,16d3eb63-5988-4a2d-b877-5625e5f5fab5,7f588dcf-d235-459b-92e7-da318dc7b608,3ef9a4e4-075b-49ef-91f2-03173fbbd037,1f66073d-e4ad-4c25-baaa-23eabccea3fd,c50aac23-b69a-4f3b-8c43-5ed6078ab05e,da880080-1665-49c7-9964-8f36d9456058,66546290-0f2a-4dee-94c5-6f1a1318669b,b810ad6d-6a73-4060-a46a-80561067629a,f4eb3e77-9fd5-4d79-9385-62c3c5f7f740,0ec5f400-436d-40cf-aaa1-2292b78fea7c,6ecf874e-4191-4d39-bf72-978407eff9fb,689776a3-88e0-4da5-9caf-280ee3268671,89b656b9-ded5-4845-9e5b-31dd4599ee53,3f414e63-949e-4b11-bd64-58d37f641cc2,3a4f45cb-a2da-4a50-8657-e6d37f983216,d24438dd-2b00-4a1b-aa54-70c99d06d817,1ee1f0b3-b4ec-4ec2-8ace-1e27f731f00e,8411435a-0beb-4301-be1a-cadf1b050c68,585c8f84-594a-49fa-99ff-2b303622036a,95d349ec-1593-4f44-bd8d-c7ebbace77d4,5d2e9665-5182-4080-a1e4-0376b695c3b0,e57e92a5-00d8-48df-97e2-59dcf924442f,a941156e-73f8-4658-8266-6f14567974d9,7473ea5b-bbe2-4de9-b491-fa457bce7466,20d4c331-60a7-44f6-9459-364114eb02cb,4735e036-3fcf-4ddd-a331-fadcbeffa9d1,25ca9b34-6ef4-4015-8133-f874ad6f2bdb,36ce7a59-66fc-46f0-aacd-9f8bb73c2d82,', NULL, N',5937e94c-0ab9-43ca-b530-a8fa81408c32,3ef9a4e4-075b-49ef-91f2-03173fbbd037,27a33254-3a0c-49c3-bdfe-9ddddf3e6672,1f66073d-e4ad-4c25-baaa-23eabccea3fd,c50aac23-b69a-4f3b-8c43-5ed6078ab05e,da880080-1665-49c7-9964-8f36d9456058,1b846248-6ab7-4d36-bbe5-b775340272a7,096e253e-367d-4bfc-ab91-b9eb1e232671,e089bdf4-3652-445e-a4e4-7ec08a57c347,4735e036-3fcf-4ddd-a331-fadcbeffa9d1,936950a8-f2f8-46cf-a936-7fc221d350de,25ca9b34-6ef4-4015-8133-f874ad6f2bdb,11347430-e739-4d0a-a707-bd50e7585575,bc3e7bb4-bc7c-4a7b-aa90-dd26d85a5ff6,e8e48fd8-dae0-4a90-9f47-b58d9c4f74c0,89e32cde-8b6b-48be-b4be-f4b1470e247e,',0, 0
-- nvtoan modify 17/01/2015: Sửa lỗi không lấy cặp định khoản chênh lệch giá
-- nvtoan modify 28/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- nvtoan modify 12/02/2015: Sửa lỗi không lấy số chứng từ, ngày chứng từ đúng theo mô tả
-- nvtoan modify 26/02/2015: Sửa lỗi không cộng trừ số dư cuối kỳ đúng khi in tất cả các tk
-- VHAnh modified 11.11.2015: Bổ sung Mã, Tên nhóm KH/NCC (CR 73635)
-- VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá khi trên báo cáo có dòng xử lý chênh lệch tỷ giá (bug 109651).
-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
-- =============================================

	DECLARE						@FromDate DATETIME 
	DECLARE						@ToDate DATETIME 
	DECLARE						@BranchID UNIQUEIDENTIFIER -- Chi nhánh
	DECLARE						@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
	DECLARE						@AccountNumber NVARCHAR(20) -- Số tài khoản
	DECLARE						@AccountObjectID AS NVARCHAR(MAX) -- Danh sách mã nhóm nhà cung cấp
	DECLARE						@CurrencyID NVARCHAR(3) -- Loại tiền
	DECLARE						@ListEmployeeID AS NVARCHAR(MAX)  -- Danh sách mã nhân viên
	DECLARE						@IsSimilarSum BIT  -- Có cộng gộp các bút toán giống nhau không? 
	DECLARE						@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?

				
SET				@FromDate = '2018-01-01 00:00:00'
SET				@ToDate = '2018-12-31 23:59:59'
SET				@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET				@IncludeDependentBranch = 1
SET				@AccountNumber = NULL
SET				@AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
SET				@CurrencyID = N'VND'
SET				@ListEmployeeID = N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,'
SET				@IsSimilarSum = 1
SET				@IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblBrandIDList TABLE
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(20) ,
              BranchName NVARCHAR(128)
            )	
       
        INSERT  INTO @tblBrandIDList
                SELECT  FGDBBI.BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI
               
        -- vhanh added 11/11/2015: Lấy thêm mã nhóm và tên nhóm KH/NCC       
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL -- Danh sách tên nhóm
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  AccountObjectID ,
                        AccountObjectGroupListCode , -- Danh sách mã nhóm
                        AccountObjectGroupListName -- Danh sách tên nhóm   
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') tblAccountObjectSelected
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = tblAccountObjectSelected.Value   
	        			
        
        DECLARE @tblListEmployeeID TABLE -- Bảng chứa danh sách mã nhân viên
            (
              EmployeeID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListEmployeeID
                SELECT  *
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ListEmployeeID,
                                                           ',')	  
                                                                                         
		-- Bảng chứa kết quả cần lấy
        CREATE TABLE #tblResult
            (
              RowNum INT IDENTITY(1, 1)
                         PRIMARY KEY ,
              EmployeeCode NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Mã NV
              EmployeeName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Tên NV
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS,   -- Mã NCC
              AccountObjectName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,	-- Tên NCC
			 -- vhanh added 11/11/2015
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách tên nhóm 
              AccountObjectAddress NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Địa chỉ
              PostedDate DATETIME ,	-- Ngày hạch toán
              RefDate DATETIME , -- Ngày chứng từ
              RefNo NVARCHAR(22) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Số chứng từ
             --BTAnh bổ sung ngày 21/07/2015 (JIRA: SMEFIVE-2297)
              InvDate DATETIME ,
              InvNo NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS, -- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
              --
              RefType INT ,	--Loại chứng từ
              RefID UNIQUEIDENTIFIER , -- Mã chứng từ                            
              RefDetailID NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
              JournalMemo NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Diễn giải
              AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS, -- Số tài khoản
              AccountCategoryKind INT , -- Tính chất tài khoản
              CorrespondingAccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS, --TK đối ứng
              ExchangeRate DECIMAL(18, 4) , --Tỷ giá
              DebitAmountOC MONEY ,	-- Phát sinh nợ
              DebitAmount MONEY , -- Phát sinh nợ quy đổi
              CreditAmountOC MONEY , -- Phát sinh có
              CreditAmount MONEY , -- Phát sinh có quy đổi
              ClosingDebitAmountOC MONEY , --Dư Nợ
              ClosingDebitAmount MONEY , --Dư Nợ Quy đổi
              ClosingCreditAmountOC MONEY ,	--Dư Có
              ClosingCreditAmount MONEY , --Dư Có quy đổi         
              IsBold BIT , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
              OrderType INT ,
              BranchName NVARCHAR(128)COLLATE SQL_Latin1_General_CP1_CI_AS -- Tên chi nhánh   
            )
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
                                AND AccountObjectType = 0
                                AND IsParent = 0
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END 
/*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/
        IF @IsSimilarSum = 0 -- Nếu không cộng gộp
            BEGIN
                INSERT  INTO #tblResult
                        ( EmployeeCode , -- Mã NV
                          EmployeeName , -- Tên NV
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi    
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName
                        
                        )
                        SELECT  EmployeeCode , -- Mã NV --MA_NHAN_VIEN
                                EmployeeName , -- Tên NV
                                AccountObjectID ,
                                AccountObjectCode ,   -- Mã NCC
                                AccountObjectName ,	-- Tên NCC
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán
                                RefDate , -- Ngày chứng từ
                                RefNo , -- Số chứng từ
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ
                                RefID , -- Mã chứng từ   
                                RefDetailID ,
                                JournalMemo , -- Diễn giải					  
                                AccountNumber , -- Số tài khoản
                                AccountCategoryKind , -- Tính chất tài khoản
                                CorrespondingAccountNumber , --TK đối ứng				  
                                ExchangeRate , --Tỷ giá				  
                                SUM(DebitAmountOC) ,	-- Phát sinh nợ
                                SUM(DebitAmount) , -- Phát sinh nợ quy đổi
                                SUM(CreditAmountOC) , -- Phát sinh có
                                SUM(CreditAmount) , -- Phát sinh có quy đổi
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ( SUM(ClosingDebitAmountOC)
                                              - SUM(ClosingCreditAmountOC) )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingDebitAmountOC)
                                                        - SUM(ClosingCreditAmountOC) ) > 0
                                                 THEN ( SUM(ClosingDebitAmountOC)
                                                        - SUM(ClosingCreditAmountOC) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ            
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ( SUM(ClosingDebitAmount)
                                              - SUM(ClosingCreditAmount) )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingDebitAmount)
                                                        - SUM(ClosingCreditAmount) ) > 0
                                                 THEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi 
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( SUM(ClosingCreditAmountOC)
                                              - SUM(ClosingDebitAmountOC) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmountOC)
                                                        - SUM(ClosingDebitAmountOC) ) > 0
                                                 THEN ( SUM(ClosingCreditAmountOC)
                                                        - SUM(ClosingDebitAmountOC) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( SUM(ClosingCreditAmount)
                                              - SUM(ClosingDebitAmount) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) ) > 0
                                                 THEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi 
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName
                        FROM    ( SELECT    AOL.EmployeeCode , -- Mã NV --MA_NHAN_VIEN
                                            AOL.EmployeeName , -- Tên NV --TEN_NHAN_VIEN
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC--TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán       ---NGAY_HACH_TOAN           
           --                             CASE 
											--WHEN AOL.PostedDate < @FromDate THEN NULL
											--WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--ELSE AOL.InvDate
           --                             END AS RefDate, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
           --                             CASE 
											--WHEN AOL.PostedDate < @FromDate THEN NULL
											--WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN AOL.RefNo
           --                                 ELSE AOL.InvNo
           --                             END AS RefNo, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo ---SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                        
                                        --BTAnh-21/07/2015
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE CAST(RefDetailID AS NVARCHAR(50))
                                            END AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.Description --DIEN_GIAI
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Detail)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng   --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate 
												 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END 
                                            END AS ExchangeRate , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE ( AOL.DebitAmountOC ) --GHI_NO_NGUYEN_TE
                                            END AS DebitAmountOC , -- Phát sinh nợ--GHI_NO_NGUYEN_TE                                    
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE ( AOL.DebitAmount )--GHI_NO
                                            END AS DebitAmount , -- Phát sinh nợ quy đổi --GHI_NO                                        
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE ( AOL.CreditAmountOC ) --
                                            END AS CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE ( AOL.CreditAmount ) --GHI_CO
                                            END AS CreditAmount , -- Phát sinh có quy đổi
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmountOC
                                                 ELSE $0
                                            END AS ClosingDebitAmountOC , --Dư Nợ  --ClosingDebitAmountOC           
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmount
                                                 ELSE $0
                                            END AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmountOC
                                                 ELSE $0
                                            END AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmount
                                                 ELSE $0
                                            END AS ClosingCreditAmount , --Dư Có quy đổi --   ClosingCreditAmount                                      
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.SortOrder
                                            END AS SortOrder ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL
                                            INNER JOIN @tblListAccountObjectID
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                            INNER JOIN @tblListEmployeeID LEID ON AOL.EmployeeID = LEID.EmployeeID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                  WHERE     AOL.PostedDate <= @ToDate
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL
                                                  OR AOL.CurrencyID = @CurrencyID
                                                )
                                            AND AN.DetailByAccountObject = 1
                                            AND AN.AccountObjectType = 0
                                ) AS RSNS
                        WHERE   ( RSNS.RefDetailID IS NOT NULL
                                  AND ( RSNS.DebitAmountOC <> 0 --GHI_NO_NGUYEN_TE
                                        OR RSNS.CreditAmountOC <> 0 --GHI_CO_NGUYEN_TE
                                        OR RSNS.DebitAmount <> 0 -- GHI_NO
                                        OR RSNS.CreditAmount <> 0 --GHI_CO
                                      )
                                )
                                OR ( RSNS.RefDetailID IS NULL
                                     AND ( ClosingCreditAmountOC <> 0
                                           OR ClosingDebitAmountOC <> 0
                                           OR ClosingCreditAmount <> 0
                                           OR ClosingDebitAmount <> 0
                                         )
                                   )
                        GROUP BY RSNS.EmployeeCode , -- Mã NV --MA_NHAN_VIEN
                                RSNS.EmployeeName , -- Tên NV  --TEN_NHAN_VIEN
                                RSNS.AccountObjectID , --DOI_TUONG_ID
                                RSNS.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                RSNS.AccountObjectName ,	-- Tên NCC -- TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                RSNS.AccountObjectAddress , -- Địa chỉ
                                RSNS.PostedDate ,	-- Ngày hạch toán--NGAY_HACH_TOAN
                                RSNS.RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RSNS.RefNo , -- Số chứng từ --SO_CHUNG_TU
                                RSNS.InvDate ,
                                RSNS.InvNo ,
                                RSNS.RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RSNS.RefID , -- Mã chứng từ   --ID_CHUNG_TU
                                RSNS.RefDetailID ,
                                RSNS.JournalMemo , -- Diễn giải		--		DIEN_GIAI_CHUNG	  
                                RSNS.AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                RSNS.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                RSNS.CorrespondingAccountNumber , --TK đối ứng--MA_TAI_KHOAN_DOI_UNG		  
                                RSNS.ExchangeRate , --Tỷ giá    
                                RSNS.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                RSNS.OrderType ,
                                BranchName ,
                                RSNS.SortOrder ,--THU_TU_TRONG_CHUNG_TU
                                RSNS.DetailPostOrder
                        HAVING  SUM(DebitAmountOC) <> 0--GHI_NO_NGUYEN_TE
                                OR SUM(DebitAmount) <> 0 --GHI_NO
                                OR SUM(CreditAmountOC) <> 0 --GHI_CO_NGUYEN_TE
                                OR SUM(CreditAmount) <> 0 --GHI_CO
                                OR SUM(ClosingDebitAmount
                                       - ClosingCreditAmount) <> 0
                                OR SUM(ClosingDebitAmountOC
                                       - ClosingCreditAmountOC) <> 0
                        ORDER BY RSNS.EmployeeCode ,
                                RSNS.AccountObjectCode ,
                                RSNS.AccountNumber ,
                                RSNS.OrderType ,
                                RSNS.PostedDate ,
                                RSNS.RefDate ,
                                RSNS.RefNo ,
                                RSNS.SortOrder ,
                                RSNS.DetailPostOrder
            END
        ELSE -- Cộng gộp các bút toán giống nhau
            BEGIN
                INSERT  INTO #tblResult
                        ( EmployeeCode , -- Mã NV
                          EmployeeName , -- Tên NV 
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi  
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName                        
                        )
                        SELECT  EmployeeCode , -- Mã NV --MA_NHAN_VIEN
                                EmployeeName , -- Tên NV  --TEN_NHAN_VIEN
                                AccountObjectID , --DOI_TUONG_ID
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ    --ID_CHUNG_TU
                                RefDetailID , 
                                JournalMemo , -- Diễn giải	--DIEN_GIAI_CHUNG				  
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng			 --	  MA_TAI_KHOAN_DOI_UNG
                                ExchangeRate , --Tỷ giá				  
                                DebitAmountOC ,	-- Phát sinh nợ --GHI_NO_NGUYEN_TE
                                DebitAmount , -- Phát sinh nợ quy đổi --GHI_NO
                                CreditAmountOC , -- Phát sinh có --GHI_CO_NGUYEN_TE
                                CreditAmount , -- Phát sinh có quy đổi --GHI_CO
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ( ClosingDebitAmountOC
                                              - ClosingCreditAmountOC )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( ClosingDebitAmountOC
                                                        - ClosingCreditAmountOC ) > 0
                                                 THEN ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ  --   ClosingDebitAmountOC       
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ( ClosingDebitAmount
                                              - ClosingCreditAmount )
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ( ClosingDebitAmount
                                                        - ClosingCreditAmount ) > 0
                                                 THEN ClosingDebitAmount
                                                      - ClosingCreditAmount
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmountOC
                                              - ClosingDebitAmountOC )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC ) > 0
                                                 THEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmount
                                              - ClosingDebitAmount )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount ) > 0
                                                 THEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi   --ClosingCreditAmount
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName
                        FROM    ( SELECT    AOL.EmployeeCode , -- Mã NV --MA_NHAN_VIEN
                                            AOL.EmployeeName , -- Tên NV	 --TEN_NHAN_VIEN
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán -- NGAY_HACH_TOAN                 
           --                             CASE 
											--WHEN AOL.PostedDate < @FromDate THEN NULL
											--WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--ELSE AOL.InvDate
           --                             END AS RefDate, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
           --                             CASE 
											--WHEN AOL.PostedDate < @FromDate THEN NULL
											--WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN AOL.RefNo
           --                                 ELSE AOL.InvNo
           --                             END AS RefNo, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn --NGAY_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo--SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  --
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID ,--ID_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ --LOAI_CHUNG_TU
                                            MAX(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN NULL
                                                     ELSE CAST(RefDetailID AS NVARCHAR(50))
                                                END) AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Master)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber
                                            END AS CorrespondingAccountNumber , --TK đối ứng   --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá 
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.DebitAmountOC )
                                                END) AS DebitAmountOC , -- Phát sinh nợ   --    GHI_NO_NGUYEN_TE                             
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.DebitAmount )
                                                END) AS DebitAmount , -- Phát sinh nợ quy đổi     --GHI_NO    --                                
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.CreditAmountOC )
                                                END) AS CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.CreditAmount )
                                                END) AS CreditAmount , -- Phát sinh có quy đổi --GHI_CO
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmountOC
                                                     ELSE $0
                                                END) AS ClosingDebitAmountOC , --Dư Nợ  --ClosingDebitAmountOC          
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmount
                                                     ELSE $0
                                                END) AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmountOC
                                                     ELSE $0
                                                END) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmount
                                                     ELSE $0
                                                END) AS ClosingCreditAmount , --Dư Có quy đổi  --ClosingCreditAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL --so_cong_no_chi_tiet
                                            INNER JOIN @tblListAccountObjectID --DS_KHACH_HANG_NCC
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID --
                                            INNER JOIN @tblListEmployeeID LEID ON AOL.EmployeeID = LEID.EmployeeID --DS_NHAN_VIEN
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent -- TMP_TAI_KHOAN
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber --danh_muc_he_thong_tai_khoan
                                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT --danh_muc_don_vi_tinh
                                  WHERE     AOL.PostedDate <= @ToDate
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL --loai_tien_id
                                                  OR AOL.CurrencyID = @CurrencyID -- "currency_id" = loai_tien_id
                                                )
                                            AND AN.DetailByAccountObject = 1 --CHI_TIET_THEO_DOI_TUONG
                                            AND AN.AccountObjectType = 0 --DOI_TUONG_SELECTION
                                  GROUP BY  AOL.EmployeeCode , -- Mã NV --MA_NHAN_VIEN
                                            AOL.EmployeeName , -- Tên NV	--TEN_NHAN_VIEN
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate --NGAY_HACH_TOAN
                                            END , -- Ngày hạch toán                  
           --                             CASE 
											--WHEN AOL.PostedDate < @FromDate THEN NULL
											--WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--ELSE AOL.InvDate
           --                             END, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
           --                             CASE 
											--WHEN AOL.PostedDate < @FromDate THEN NULL
											--WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN AOL.RefNo
           --                                 ELSE AOL.InvNo
           --                             END, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate ---NGAY_CHUNG_TU
                                            END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID---ID_CHUNG_TU
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType --LOAI_CHUNG_TU
                                            END , --Loại chứng từ                                             
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo--DIEN_GIAI_CHUNG
                                            END , -- Diễn giải (lấy diễn giải Master)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END , --TK đối ứng   
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE 
												  CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
												  END
                                            END , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END
                                ) AS RSS
                        WHERE   RSS.DebitAmountOC <> 0 --GHI_NO_NGUYEN_TE
                                OR RSS.CreditAmountOC <> 0 --GHI_NO
                                OR RSS.DebitAmount <> 0 --GHI_CO_NGUYEN_TE
                                OR RSS.CreditAmount <> 0 --GHI_CO
                                OR ClosingCreditAmountOC --ClosingCreditAmountOC
                                - ClosingDebitAmountOC <> 0 --ClosingDebitAmountOC
                                OR ClosingCreditAmount - ClosingDebitAmount <> 0 --ClosingCreditAmount -ClosingDebitAmount
                        ORDER BY RSS.EmployeeCode , --MA_NHAN_VIEN
                                RSS.AccountObjectCode , --MA_DOI_TUONG
                                RSS.AccountNumber , --SO_TAI_KHOAN
                                RSS.OrderType ,
                                RSS.PostedDate , --NGAY_HACH_TOAN
                                RSS.RefDate , --NGAY_CHUNG_TU
                                RSS.RefNo , --SO_CHUNG_TU
                                RSS.DetailPostOrder
            END 				
					
  
                        
/* Tính số tồn */
        DECLARE @CloseAmountOC AS DECIMAL(22, 8) ,
            @CloseAmount AS DECIMAL(22, 8) ,
            @EmployeeCode_tmp NVARCHAR(100) ,
            @AccountObjectCode_tmp NVARCHAR(100) ,
            @AccountNumber_tmp NVARCHAR(20)
        SELECT  @CloseAmountOC = 0 ,
                @CloseAmount = 0 ,
                @EmployeeCode_tmp = N'' ,
                @AccountObjectCode_tmp = N'' ,
                @AccountNumber_tmp = N'' 
        UPDATE  #tblResult
        SET     @CloseAmountOC = ( CASE WHEN OrderType = 0
                                        THEN ( CASE WHEN ClosingDebitAmountOC = 0
                                                    THEN ClosingCreditAmountOC
                                                    ELSE -1
                                                         * ClosingDebitAmountOC
                                               END )
                                        WHEN @EmployeeCode_tmp <> EmployeeCode
                                             OR @AccountObjectCode_tmp <> AccountObjectCode
                                             OR @AccountNumber_tmp <> AccountNumber
                                        THEN CreditAmountOC - DebitAmountOC
                                        ELSE @CloseAmountOC + CreditAmountOC
                                             - DebitAmountOC
                                   END ) ,
                ClosingDebitAmountOC = ( CASE WHEN AccountCategoryKind = 0
                                              THEN -1 * @CloseAmountOC
                                              WHEN AccountCategoryKind = 1
                                              THEN $0
                                              ELSE CASE WHEN @CloseAmountOC < 0
                                                        THEN -1
                                                             * @CloseAmountOC
                                                        ELSE $0
                                                   END
                                         END ) ,
                ClosingCreditAmountOC = ( CASE WHEN AccountCategoryKind = 1
                                               THEN @CloseAmountOC
                                               WHEN AccountCategoryKind = 0
                                               THEN $0
                                               ELSE CASE WHEN @CloseAmountOC > 0
                                                         THEN @CloseAmountOC
                                                         ELSE $0
                                                    END
                                          END ) ,
                @CloseAmount = ( CASE WHEN OrderType = 0
                                      THEN ( CASE WHEN ClosingDebitAmount = 0
                                                  THEN ClosingCreditAmount
                                                  ELSE -1 * ClosingDebitAmount
                                             END )
                                      WHEN @EmployeeCode_tmp <> EmployeeCode
                                           OR @AccountObjectCode_tmp <> AccountObjectCode
                                           OR @AccountNumber_tmp <> AccountNumber
                                      THEN CreditAmount - DebitAmount
                                      ELSE @CloseAmount + CreditAmount
                                           - DebitAmount
                                 END ) ,
                ClosingDebitAmount = ( CASE WHEN AccountCategoryKind = 0
                                            THEN -1 * @CloseAmount
                                            WHEN AccountCategoryKind = 1
                                            THEN $0
                                            ELSE CASE WHEN @CloseAmount < 0
                                                      THEN -1 * @CloseAmount
                                                      ELSE $0
                                                 END
                                       END ) ,
                ClosingCreditAmount = ( CASE WHEN AccountCategoryKind = 1
                                             THEN @CloseAmount
                                             WHEN AccountCategoryKind = 0
                                             THEN $0
                                             ELSE CASE WHEN @CloseAmount > 0
                                                       THEN @CloseAmount
                                                       ELSE $0
                                                  END
                                        END ) ,
                @EmployeeCode_tmp = EmployeeCode ,
                @AccountObjectCode_tmp = AccountObjectCode ,
                @AccountNumber_tmp = AccountNumber
        WHERE   OrderType <> 2
		
/*Lấy số liệu*/				
        SELECT  --ROW_NUMBER() OVER (ORDER BY RS.EmployeeCode, RS.AccountObjectCode, RS.AccountNumber, RS.OrderType, RS.PostedDate, RS.RefDate, RS.RefNo) AS RowNum,
                RS.*
        FROM    #tblResult RS       
        
        DROP TABLE #tblResult
    END
    



GO



--------------------------------------Thống kê theo hợp đồng mua--------------------------------------------------
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		DCQUY
-- Create date: 02/07/2014
-- Description:	<Mua hàng: Lấy số liệu chi tiết công nợ phải trả theo hợp đồng mua>
-- Modified By NTGIANG 29.09.2014: Viết lại
-- Proc_PUReport_GetPUPaymentDetailByPurchaseContract '9/1/2014', '9/30/2014', '02fa2e49-bf0d-4352-8405-c860c8135e93', 1, N'111', N',20D4C331-60A7-44F6-9459-364114EB02CB,', NULL, N',B871ED21-AB49-45E1-8F76-DAFC6D768EF6,',0, 1
-- tthoa 4/10/2014: chỉnh lại một chút đoạn nhầm credit, debit
-- nvtoan modify 17/01/2014: Sửa lỗi không lấy cặp định khoản chênh lệch tỷ giá
-- nvtoan modify 28/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- nvtoan modify 12/02/2015: Sửa lỗi không lấy số chứng từ, ngày chứng từ đúng theo mô tả
-- nmtruong 23/10/2015: sửa lỗi 74886: thêm Cột Rownum ở bảng @tblResult và sort khi insert để khi update số dư đúng thứ tự
-- VHAnh modified 11.11.2015: Bổ sung Mã, Tên nhóm KH/NCC (CR 73635)
-- VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá khi trên báo cáo có dòng xử lý chênh lệch tỷ giá (bug 109651).
/*ntlieu 22.02.2018 thi công PBI 172744 mở rộng cột số hợp đồng mua lên 50 ký tự*/
-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @AccountNumber NVARCHAR(20) -- Số tài khoản
 DECLARE   @AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhóm nhà cung cấp
 DECLARE   @CurrencyID NVARCHAR(3) -- Loại tiền
 DECLARE   @SupplierID AS NVARCHAR(MAX)  -- Danh sách mã hợp đồng
 DECLARE   @IsSimilarSum BIT  -- Có cộng gộp các bút toán giống nhau không? 
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?    



		SET					@FromDate = '2018-01-01 00:00:00'
        SET                    @ToDate = '2018-12-31 23:59:59'
        SET                    @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET                    @IncludeDependentBranch = 1
        SET                    @AccountNumber = NULL
        SET                    @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
        SET                    @CurrencyID = N'VND'
        SET                    @SupplierID = N',fa5b2fae-4ab9-496e-ae94-04c5cd6c50ff,bda81d75-e38a-4645-b1da-77a6596a9972,d2781cb6-e193-4793-8082-20f3e95273a3,'
        SET                    @IsSimilarSum = 0
        SET                    @IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblBranchIDList TABLE
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCod NVARCHAR(20) ,
              BranchName NVARCHAR(128)
            )	
       
        INSERT  INTO @tblBranchIDList
                SELECT  FGDBBI.BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI
               
        -- vhanh added 11/11/2015: Lấy thêm mã nhóm và tên nhóm KH/NCC       
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL -- Danh sách tên nhóm
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  AccountObjectID ,
                        AccountObjectGroupListCode , -- Danh sách mã nhóm
                        AccountObjectGroupListName -- Danh sách tên nhóm   
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') tblAccountObjectSelected
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = tblAccountObjectSelected.Value	        			
        
        DECLARE @tblListPUContractID TABLE -- Bảng chứa danh sách mã hợp đồng
            (
              PUContractID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListPUContractID
                SELECT  *
                FROM    dbo.Func_ConvertGUIStringIntoTable(@SupplierID, ',')	  
                                                                            
		-- Bảng chứa kết quả cần lấy
        DECLARE @tblResult TABLE
            (
              RowNum INT IDENTITY(1, 1)
                         PRIMARY KEY ,
              PUContractCode NVARCHAR(50) , /*ntlieu 22.02.2018 thi công PBI 172744 mở rộng cột số hợp đồng mua lên 50 ký tự*/
              PUSignDate DATETIME , -- Ngày ký hợp đồng mua
              PUContractName NVARCHAR(255) ,   -- Trích yếu hợp đồng mua
              BranchID UNIQUEIDENTIFIER ,
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(100) ,   -- Mã NCC
              AccountObjectName NVARCHAR(255) ,	-- Tên NCC
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách tên nhóm                
              AccountObjectAddress NVARCHAR(255) , -- Địa chỉ
              PostedDate DATETIME ,	-- Ngày hạch toán
              RefDate DATETIME , -- Ngày chứng từ
              RefNo NVARCHAR(22) , -- Số chứng từ
              --BTAnh bổ sung ngày 21/07/2015 (JIRA: SMEFIVE-2297)
              InvDate DATETIME ,
              InvNo NVARCHAR(500) ,-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
              --
              RefType INT ,	--Loại chứng từ
              RefID UNIQUEIDENTIFIER , -- Mã chứng từ                            
              RefDetailID NVARCHAR(50) ,
              JournalMemo NVARCHAR(255) , -- Diễn giải
              AccountNumber NVARCHAR(20) , -- Số tài khoản
              AccountCategoryKind INT , -- Tính chất tài khoản
              CorrespondingAccountNumber NVARCHAR(20) , --TK đối ứng
              ExchangeRate DECIMAL(18, 4) , --Tỷ giá
              DebitAmountOC MONEY ,	-- Phát sinh nợ
              DebitAmount MONEY , -- Phát sinh nợ quy đổi
              CreditAmountOC MONEY , -- Phát sinh có
              CreditAmount MONEY , -- Phát sinh có quy đổi
              ClosingDebitAmountOC MONEY , --Dư Nợ
              ClosingDebitAmount MONEY , --Dư Nợ Quy đổi
              ClosingCreditAmountOC MONEY ,	--Dư Có
              ClosingCreditAmount MONEY , --Dư Có quy đổi 
              IsBold BIT , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
              OrderType INT ,
              BranchName NVARCHAR(128)
            )
            
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
                                AND AccountObjectType = 0
                                AND IsParent = 0
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END 
/*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/
        IF @IsSimilarSum = 0 -- Nếu không cộng gộp
            BEGIN
                INSERT  INTO @tblResult
                        ( PUContractCode , -- Mã hợp đồng mua     
                          PUSignDate , -- Ngày ký hợp đồng mua
                          PUContractName ,   -- Trích yếu hợp đồng mua
                          BranchID ,
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi    
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName
                        )
                        SELECT  PUContractCode , -- Mã hợp đồng mua     
                                PUSignDate , -- Ngày ký hợp đồng mua
                                PUContractName ,   -- Trích yếu hợp đồng mua
                                BranchID ,
                                AccountObjectID ,--
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ    --ID_CHUNG_TU
                                RefDetailID ,
                                JournalMemo , -- Diễn giải				--	  DIEN_GIAI_CHUNG
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản--TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng	--	MA_TAI_KHOAN_DOI_UNG		  
                                ExchangeRate , --Tỷ giá				  
                                SUM(DebitAmountOC) ,	-- Phát sinh nợ
                                SUM(DebitAmount) , -- Phát sinh nợ quy đổi
                                SUM(CreditAmountOC) , -- Phát sinh có
                                SUM(CreditAmount) , -- Phát sinh có quy đổi
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN SUM(ClosingDebitAmountOC)
                                            - SUM(ClosingCreditAmountOC)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN SUM(ClosingDebitAmountOC)
                                                      - SUM(ClosingCreditAmountOC) > 0
                                                 THEN SUM(ClosingDebitAmountOC)
                                                      - SUM(ClosingCreditAmountOC)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ  ---ClosingDebitAmountOC           
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN SUM(ClosingDebitAmount)
                                            - SUM(ClosingCreditAmount)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount) > 0
                                                 THEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN SUM(ClosingCreditAmountOC)
                                            - SUM(ClosingDebitAmountOC)
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN SUM(ClosingCreditAmountOC)
                                                      - SUM(ClosingDebitAmountOC) > 0
                                                 THEN SUM(ClosingCreditAmountOC)
                                                      - SUM(ClosingDebitAmountOC)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( SUM(ClosingCreditAmount)
                                              - SUM(ClosingDebitAmount) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) ) > 0
                                                 THEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi -- ClosingCreditAmount                       
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng
                                OrderType ,
                                BranchName
                        FROM    ( SELECT    AOL.PUContractCode , -- Mã hợp đồng mua     
                                            AOL.PUSignDate , -- Ngày ký hợp đồng mua
                                            AOL.PUContractName ,   -- Trích yếu hợp đồng mua
                                            AOL.BranchID ,
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán    --NGAY_HACH_TOAN              
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--	ELSE AOL.InvDate
											--END AS RefDate, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefNo
											--	ELSE AOL.InvNo
											--END AS RefNo, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  ---SO_CHUNG_TU
                                            
                                            --BTAnh-21/07/2015
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE CAST(RefDetailID AS NVARCHAR(50))
                                            END AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.Description --DIEN_GIAI
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Detail)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng   --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.DebitAmountOC --GHI_NO_NGUYEN_TE
                                            END AS DebitAmountOC , -- Phát sinh nợ                                    
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.DebitAmount --GHI_NO
                                            END AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.CreditAmountOC --GHI_CO_NGUYEN_TE
                                            END AS CreditAmountOC , -- Phát sinh có  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.CreditAmount --GHI_CO
                                            END AS CreditAmount , -- Phát sinh có quy đổi
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmountOC --
                                                 ELSE $0
                                            END AS ClosingDebitAmountOC , --Dư Nợ --    ClosingDebitAmountOC       
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmount
                                                 ELSE $0
                                            END AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmountOC
                                                 ELSE $0
                                            END AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmount
                                                 ELSE $0
                                            END AS ClosingCreditAmount , --Dư Có quy đổi  --ClosingCreditAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.SortOrder
                                            END AS SortOrder , --THU_TU_TRONG_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL --so_cong_no_chi_tiet
                                            INNER JOIN @tblListAccountObjectID
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                                            INNER JOIN @tblBranchIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                         INNER JOIN @tblListPUContractID LCID ON AOL.PUContractID = LCID.PUContractID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                  WHERE     AOL.PostedDate <= @ToDate
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL
                                                  OR AOL.CurrencyID = @CurrencyID
                                                )
                                            AND AN.DetailByAccountObject = 1
                                            AND AN.AccountObjectType = 0
                                ) AS RSNS
                        WHERE   ( RSNS.RefDetailID IS NOT NULL
                                  AND ( RSNS.DebitAmountOC <> 0
                                        OR RSNS.CreditAmountOC <> 0
                                        OR RSNS.DebitAmount <> 0
                                        OR RSNS.CreditAmount <> 0
                                      )
                                )
                                OR ( RSNS.RefDetailID IS NULL
                                     AND ( ClosingCreditAmountOC <> 0
                                           OR ClosingDebitAmountOC <> 0
                                           OR ClosingCreditAmount <> 0
                                           OR ClosingDebitAmount <> 0
                                         )
                                   )
                        GROUP BY RSNS.PUContractCode , -- Mã hợp đồng mua     
                                RSNS.PUSignDate , -- Ngày ký hợp đồng mua
                                RSNS.PUContractName ,   -- Trích yếu hợp đồng mua
                                RSNS.BranchID ,
                                RSNS.AccountObjectID ,
                                RSNS.AccountObjectCode ,   -- Mã NCC
                                RSNS.AccountObjectName ,	-- Tên NCC
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                RSNS.AccountObjectAddress , -- Địa chỉ
                                RSNS.PostedDate ,	-- Ngày hạch toán
                                RSNS.RefDate , -- Ngày chứng từ
                                RSNS.RefNo , -- Số chứng từ
                                RSNS.InvDate ,
                                RSNS.InvNo ,
                                RSNS.RefType ,	--Loại chứng từ
                                RSNS.RefID , -- Mã chứng từ   
                                RSNS.RefDetailID ,
                                RSNS.JournalMemo , -- Diễn giải					  
                                RSNS.AccountNumber , -- Số tài khoản
                                RSNS.AccountCategoryKind , -- Tính chất tài khoản
                                RSNS.CorrespondingAccountNumber , --TK đối ứng				  
                                RSNS.ExchangeRate , --Tỷ giá  
                                RSNS.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng
                                RSNS.OrderType ,
                                BranchName ,
                                RSNS.SortOrder ,
                                RSNS.DetailPostOrder
                        HAVING  SUM(DebitAmountOC) <> 0
                                OR SUM(DebitAmount) <> 0
                                OR SUM(CreditAmountOC) <> 0
                                OR SUM(CreditAmount) <> 0
                                OR SUM(ClosingDebitAmount
                                       - ClosingCreditAmount) <> 0
                                OR SUM(ClosingDebitAmountOC
                                       - ClosingCreditAmountOC) <> 0
                        ORDER BY RSNS.PUContractCode ,
                                RSNS.BranchID ,
                                RSNS.AccountObjectCode ,
                                RSNS.AccountNumber ,
                                RSNS.OrderType ,
                                RSNS.PostedDate ,
                                RSNS.RefDate ,
                                RSNS.RefNo ,
                                RSNS.DetailPostOrder
            END
        ELSE -- Cộng gộp các bút toán giống nhau
            BEGIN
                INSERT  INTO @tblResult
                        ( PUContractCode , -- Mã hợp đồng mua     
                          PUSignDate , -- Ngày ký hợp đồng mua
                          PUContractName ,   -- Trích yếu hợp đồng mua
                          BranchID ,
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi  
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName
                        )
                        SELECT  PUContractCode , -- Mã hợp đồng mua     
                                PUSignDate , -- Ngày ký hợp đồng mua
                                PUContractName ,   -- Trích yếu hợp đồng mua
                                BranchID ,
                                AccountObjectID , --DOI_TUONG_ID
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ    --ID_CHUNG_TU
                                RefDetailID ,
                                JournalMemo , -- Diễn giải	--	DIEN_GIAI_CHUNG			  
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản -- TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng	 --		MA_TAI_KHOAN_DOI_UNG	  
                                ExchangeRate , --Tỷ giá				  
                                DebitAmountOC ,	-- Phát sinh nợ --GHI_NO_NGUYEN_TE
                                DebitAmount , -- Phát sinh nợ quy đổi --GHI_NO
                                CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                CreditAmount , -- Phát sinh có quy đổi  --GHI_CO
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                            - ClosingCreditAmountOC -- ClosingCreditAmountOC
                                       WHEN AccountCategoryKind = 1 THEN $0 
                                       ELSE CASE WHEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC > 0 --ClosingCreditAmountOC
                                                 THEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC --ClosingCreditAmountOC
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ   --ClosingDebitAmountOC         
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ClosingDebitAmount --ClosingDebitAmount
                                            - ClosingCreditAmount --ClosingCreditAmount
                                       WHEN AccountCategoryKind = 1 THEN $0 
                                       ELSE CASE WHEN ClosingDebitAmount --ClosingDebitAmount
                                                      - ClosingCreditAmount > 0 --ClosingCreditAmount
                                                 THEN ClosingDebitAmount  --ClosingDebitAmount
                                                      - ClosingCreditAmount --ClosingCreditAmount
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmountOC
                                              - ClosingDebitAmountOC )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC ) > 0
                                                 THEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmount
                                              - ClosingDebitAmount )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount ) > 0
                                                 THEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi  
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName
                        FROM    ( SELECT    AOL.PUContractCode , -- Mã hợp đồng mua     
                                            AOL.PUSignDate , -- Ngày ký hợp đồng mua
                                            AOL.PUContractName ,   -- Trích yếu hợp đồng mua
                                            AOL.BranchID ,
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán-- NGAY_HACH_TOAN                 
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--	ELSE AOL.InvDate
											--END AS RefDate, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefNo
											--	ELSE AOL.InvNo
											--END AS RefNo, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID , --ID_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ  --LOAI_CHUNG_TU
                                            MAX(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN NULL
                                                     ELSE CAST(RefDetailID AS NVARCHAR(50))
                                                END) AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Master)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng    --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá 
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.DebitAmountOC ) --GHI_NO_NGUYEN_TE
                                                END) AS DebitAmountOC , -- Phát sinh nợ                                    
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.DebitAmount ) --GHI_NO
                                                END) AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.CreditAmountOC ) --
                                                END) AS CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.CreditAmount )
                                                END) AS CreditAmount , -- Phát sinh có quy đổi --GHI_CO
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmountOC
                                                     ELSE $0
                                                END) AS ClosingDebitAmountOC , --Dư Nợ  --ClosingDebitAmountOC          
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmount
                                                     ELSE $0
                                                END) AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmountOC
                                                     ELSE $0
                                                END) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmount
                                                     ELSE $0
                                                END) AS ClosingCreditAmount , --Dư Có quy đổi --ClosingCreditAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL
                                            INNER JOIN @tblListAccountObjectID
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblListPUContractID LCID ON AOL.PUContractID = LCID.PUContractID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                                            INNER JOIN @tblBranchIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                  WHERE     ( AOL.PostedDate <= @ToDate )
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL
                                                  OR AOL.CurrencyID = @CurrencyID
                                                )
                                            AND AN.DetailByAccountObject = 1
                                            AND AN.AccountObjectType = 0
                                  GROUP BY  AOL.PUContractCode , -- Mã hợp đồng mua     
                                            AOL.PUSignDate , -- Ngày ký hợp đồng mua
                                            AOL.PUContractName ,   -- Trích yếu hợp đồng mua
                                            AOL.BranchID ,
                                            AOL.AccountObjectID ,--DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END , -- Ngày hạch toán                  
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--	ELSE AOL.InvDate
											--END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefNo
											--	ELSE AOL.InvNo
											--END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID --ID_CHUNG_TU
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType --LOAI_CHUNG_TU
                                            END , --Loại chứng từ                                             
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END , -- Diễn giải (lấy diễn giải Master)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END , --TK đối ứng   
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE/*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END
                                ) AS RSS
                        WHERE   RSS.DebitAmountOC <> 0 --GHI_NO_NGUYEN_TE
                                OR RSS.CreditAmountOC <> 0 --GHI_CO_NGUYEN_TE
                                OR RSS.DebitAmount <> 0 --GHI_NO
                                OR RSS.CreditAmount <> 0  --GHI_CO
                                OR ClosingCreditAmountOC
                                - ClosingDebitAmountOC <> 0
                                OR ClosingCreditAmount - ClosingDebitAmount <> 0
                        ORDER BY RSS.PUContractCode ,
                                RSS.BranchID ,
                                RSS.AccountObjectCode ,
                                RSS.AccountNumber ,
                                RSS.OrderType ,
                                RSS.PostedDate ,
                                RSS.RefDate ,
                                RSS.RefNo ,
                                RSS.DetailPostOrder
                        
            END                		
 
                        
/* Tính số tồn */
        DECLARE @CloseAmountOC AS DECIMAL(22, 8) ,
            @CloseAmount AS DECIMAL(22, 8) ,
            @PUContractCode_tmp NVARCHAR(100) ,
            @BranchID_tmp UNIQUEIDENTIFIER ,
            @AccountObjectCode_tmp NVARCHAR(100) ,
            @AccountNumber_tmp NVARCHAR(20)
        SELECT  @CloseAmountOC = 0 ,
                @CloseAmount = 0 ,
                @PUContractCode_tmp = N'' ,
                @BranchID_tmp = NULL ,
                @AccountObjectCode_tmp = N'' ,
                @AccountNumber_tmp = N''
	
        UPDATE  @tblResult
        SET     @CloseAmountOC = ( CASE WHEN OrderType = 0
                                        THEN ( CASE WHEN ClosingDebitAmountOC = 0
                                                    THEN ClosingCreditAmountOC
                                                    ELSE -1
                                                         * ClosingDebitAmountOC
                                               END )
                                        WHEN @PUContractCode_tmp <> PUContractCode
                                             OR @BranchID_tmp <> BranchID
                                             OR @AccountObjectCode_tmp <> AccountObjectCode
                                             OR @AccountNumber_tmp <> AccountNumber
                                        THEN CreditAmountOC - DebitAmountOC
                                        ELSE @CloseAmountOC + CreditAmountOC
                                             - DebitAmountOC
                                   END ) ,
                ClosingDebitAmountOC = ( CASE WHEN AccountCategoryKind = 0
                                              THEN -1 * @CloseAmountOC
                                              WHEN AccountCategoryKind = 1
                                              THEN $0
                                              ELSE CASE WHEN @CloseAmountOC < 0
                                                        THEN -1
                                                             * @CloseAmountOC
                                                        ELSE $0
                                                   END
                                         END ) ,
                ClosingCreditAmountOC = ( CASE WHEN AccountCategoryKind = 1
                                               THEN @CloseAmountOC
                                               WHEN AccountCategoryKind = 0
                                               THEN $0
                                               ELSE CASE WHEN @CloseAmountOC > 0
                                                         THEN @CloseAmountOC
                                                         ELSE $0
                                                    END
                                          END ) ,
                @CloseAmount = ( CASE WHEN OrderType = 0
                                      THEN ( CASE WHEN ClosingDebitAmount = 0
                                                  THEN ClosingCreditAmount
                                                  ELSE -1 * ClosingDebitAmount
                                             END )
                                      WHEN @PUContractCode_tmp <> PUContractCode
                                           OR @AccountObjectCode_tmp <> AccountObjectCode
                                           OR @AccountNumber_tmp <> AccountNumber
                                      THEN CreditAmount - DebitAmount
                                      ELSE @CloseAmount + CreditAmount
                                           - DebitAmount
                                 END ) ,
                ClosingDebitAmount = ( CASE WHEN AccountCategoryKind = 0
                                            THEN -1 * @CloseAmount
                                            WHEN AccountCategoryKind = 1
                                            THEN $0
                                            ELSE CASE WHEN @CloseAmount < 0
                                                      THEN -1 * @CloseAmount
                                                      ELSE $0
                                                 END
                                       END ) ,
                ClosingCreditAmount = ( CASE WHEN AccountCategoryKind = 1
                                             THEN @CloseAmount
                                             WHEN AccountCategoryKind = 0
                                             THEN $0
                                             ELSE CASE WHEN @CloseAmount > 0
                                                       THEN @CloseAmount
                                                       ELSE $0
                                                  END
                                        END ) ,
                @PUContractCode_tmp = PUContractCode ,
                @BranchID_tmp = BranchID ,
                @AccountObjectCode_tmp = AccountObjectCode ,
                @AccountNumber_tmp = AccountNumber
        WHERE   OrderType <> 2		
        
        
/*Lấy số liệu*/				
        SELECT  RS.*
        FROM    @tblResult RS   
    END

GO

------------------------------Thống kê theo công trình-----------------------------------

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO


-- =============================================
-- Author:		<HHSon>
-- Create date: <03/07/2014>
-- Description:	Lấy số liệu Báo cáo chi tiết công nợ phải trả theo công trình
-- Modified By NTGIANG 29.09.2014: Viết lại
-- Proc_PUR_GetPaymentableDetailByProjectWork '9/1/2014', '9/30/2014', '02fa2e49-bf0d-4352-8405-c860c8135e93', 1, N'111', N',20D4C331-60A7-44F6-9459-364114EB02CB,', NULL, N',B871ED21-AB49-45E1-8F76-DAFC6D768EF6,',0, 0
-- Edited By DNMinh 29/12/2014: Sửa bug 40822, khi chọn công trình cha thì lấy lên toàn bộ các chứng từ từ công trình con
-- nvtoan modify 16/01/2014: Sửa lỗi không lấy dòng định khoản chênh lệch giá
-- nvtoan modify 28/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- nvtoan modify 12/02/2015: Sửa lỗi không lấy số chứng từ, ngày chứng từ đúng theo mô tả
-- nvtoan modify 26/02/2015: Sửa lỗi khi chọn tk tất cả thì không tính đúng số dư cuối kỳ
-- modified by HHSon - 08.09.2015 (64047): Bổ sung Loại công trình
-- VHAnh bổ sung 03.11.2015: Bổ sung thêm thông tin Mã hàng, Tên hàng, ĐVT, Số lượng, Đơn giá (75892)
-- VHAnh bổ sung 09.11.2015: Bổ sung thêm thông tin Mã nhóm KH/NCC, Tên nhóm KH/NCC (75898)
-- VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá khi trên báo cáo có dòng xử lý chênh lệch tỷ giá (bug 109651).
-- DDKhanh CR128285 17/08/2017 với chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo
-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @AccountNumber NVARCHAR(20) -- Số tài khoản
 DECLARE   @AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhóm nhà cung cấp
 DECLARE   @CurrencyID NVARCHAR(3) -- Loại tiền
 DECLARE   @ProjectWorkID AS NVARCHAR(MAX)  -- Danh sách công trình
 DECLARE   @IsSimilarSum BIT  -- Có cộng gộp các bút toán giống nhau không?
 DECLARE   @IsWorkingWithManagementBook BIT --  Có dùng sổ quản trị hay không?


	SET						@FromDate = '2018-01-01 00:00:00'
	SET						@ToDate = '2018-12-31 23:59:59'
	SET						@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
	SET						@IncludeDependentBranch = 1
	SET						@AccountNumber = NULL
	SET						@AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
	SET						@CurrencyID = N'VND'
	SET						@ProjectWorkID = N',9b46c3a0-060f-4b8e-a5e2-4786271f51d9,c0570228-b65f-44c8-acee-3da2ae38d590,e9b86b73-2026-4fe1-9e49-9f0d0c7ee9ac,'
	SET						@IsSimilarSum = 1
	SET						@IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblBrandIDList TABLE
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(20) ,
              BranchName NVARCHAR(128)
            )	

        INSERT  INTO @tblBrandIDList
                SELECT  FGDBBI.BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI
		-- vhanh added 09/11/2015: Lấy thêm mã nhóm và tên nhóm KH/NCC 
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS -- Danh sách tên nhóm
            )
        INSERT  INTO @tblListAccountObjectID
                SELECT  AccountObjectID ,
                        AccountObjectGroupListCode , -- Danh sách mã nhóm
                        AccountObjectGroupListName -- Danh sách tên nhóm   
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') tblAccountObjectSelected
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = tblAccountObjectSelected.Value   					


        DECLARE @tblProjectWorkID TABLE -- Bảng các công trình được chọn--DS_CONG_TRINH
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) ,
              ProjectWorkCode NVARCHAR(20) ,
              ProjectWorkName NVARCHAR(128) ,
              ProjectWorkCategoryID UNIQUEIDENTIFIER
            )
        INSERT  INTO @tblProjectWorkID
                SELECT DISTINCT
                        PW.ProjectWorkID ,
                        PW.MISACodeID , --MA_PHAN_CAP
                        PW.ProjectWorkCode , --MA_CONG_TRINH
                        PW.ProjectWorkName , --TEN_CONG_TRINH
                        PW.ProjectWorkCategoryID --LOAI_CONG_TRINH
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ProjectWorkID, ',') tString
                        INNER JOIN dbo.ProjectWork PW ON PW.ProjectWorkID = tString.Value

        DECLARE @tblListProjectWorkID TABLE -- Bảng gồm toàn bộ các công trình con từ các công trình được chọn
            (
              ProjectWorkID UNIQUEIDENTIFIER PRIMARY KEY ,
              MISACodeID NVARCHAR(100) ,
              ProjectWorkCode NVARCHAR(20) ,
              ProjectWorkName NVARCHAR(128)
            )
        INSERT  INTO @tblListProjectWorkID
                SELECT DISTINCT
                        PW.ProjectWorkID ,
                        PW.MISACodeID ,
                        PW.ProjectWorkCode ,
                        PW.ProjectWorkName
                FROM    @tblProjectWorkID SPW
                        INNER JOIN dbo.ProjectWork PW ON PW.MisaCodeID LIKE SPW.MISACodeID
                                                         + '%'

		-- Bảng chứa kết quả cần lấy
        DECLARE @tblResult TABLE
            (
              RowNum INT IDENTITY(1, 1)
                         PRIMARY KEY ,  /*Bổ sung trường này vào để sort trong TH cộng dồn*/
              ProjectWorkCode NVARCHAR(20) , -- Mã công trình
              ProjectWorkName NVARCHAR(128) , -- Tên công trình
              ProjectWorkCategoryName NVARCHAR(128) , -- Tên loại công trình
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(100) ,   -- Mã NCC
              AccountObjectName NVARCHAR(255) ,	-- Tên NCC
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS , -- Danh sách tên nhóm  
              AccountObjectAddress NVARCHAR(255) , -- Địa chỉ
              PostedDate DATETIME ,	-- Ngày hạch toán
              RefDate DATETIME , -- Ngày chứng từ
              RefNo NVARCHAR(22) , -- Số chứng từ
              --BTAnh bổ sung ngày 21/07/2015 (JIRA: SMEFIVE-2297)
              InvDate DATETIME ,
              InvNo NVARCHAR(500) ,-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
              --
              RefType INT ,	--Loại chứng từ
              RefID UNIQUEIDENTIFIER , -- Mã chứng từ
              RefDetailID NVARCHAR(50) ,
              JournalMemo NVARCHAR(255) , -- Diễn giải
              AccountNumber NVARCHAR(20) , -- Số tài khoản
              AccountCategoryKind INT , -- Tính chất tài khoản
              CorrespondingAccountNumber NVARCHAR(20) , --TK đối ứng
              ExchangeRate DECIMAL(18, 4) , --Tỷ giá
              DebitAmountOC MONEY ,	-- Phát sinh nợ
              DebitAmount MONEY , -- Phát sinh nợ quy đổi
              CreditAmountOC MONEY , -- Phát sinh có
              CreditAmount MONEY , -- Phát sinh có quy đổi
              ClosingDebitAmountOC MONEY , --Dư Nợ
              ClosingDebitAmount MONEY , --Dư Nợ Quy đổi
              ClosingCreditAmountOC MONEY ,	--Dư Có
              ClosingCreditAmount MONEY , --Dư Có quy đổi\			  
			  --VHAnh bổ sung 03.11.2015 
              InventoryItemCode NVARCHAR(25) ,
              InventoryItemName NVARCHAR(255) ,
              UnitName NVARCHAR(20) ,
              UnitPrice DECIMAL(22, 4) ,
              Quantity DECIMAL(22, 4) ,
              IsBold BIT , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
              OrderType INT ,
              BranchName NVARCHAR(128) ,
              SortOrder INT ,
              DetailPostOrder INT
--,OrderTypeTemp INT
            )
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
                                AND AccountObjectType = 0
                                AND IsParent = 0
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END
/*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/
        IF @IsSimilarSum = 0 -- Nếu không cộng gộp
            BEGIN
                INSERT  INTO @tblResult
                        ( ProjectWorkCode , -- Mã công trình
                          ProjectWorkName , -- Tên công trình
                          ProjectWorkCategoryName , --Tên loại công trình
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm 
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán--NGAY_HACH_TOAN
                          RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                          RefNo , -- Số chứng từ --SO_CHUNG_TU
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                          RefID , -- Mã chứng từ --ID_CHUNG_TU
                          RefDetailID ,
                          JournalMemo , -- Diễn giải		 --DIEN_GIAI_CHUNG			
                          AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                          AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                          CorrespondingAccountNumber , --TK đối ứng --MA_TAI_KHOAN_DOI_UNG	
                          ExchangeRate , --Tỷ giá				
                          DebitAmountOC ,	-- Phát sinh nợ 
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi						  
                          InventoryItemCode ,
                          InventoryItemName ,
                          UnitName ,
                          UnitPrice ,
                          Quantity ,
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName ,
                          SortOrder ,
                          DetailPostOrder 
                        )
                        SELECT  ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                                ProjectWorkName , -- Tên công trình--TEN_CONG_TRINH
                                ProjectWorkCategoryName , --tên loại cT
                                AccountObjectID , --DOI_TUONG_ID
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm 
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ -- ID_CHUNG_TU
                                RefDetailID ,
                                JournalMemo , -- Diễn giải	--	DIEN_GIAI_CHUNG			
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng --	MA_TAI_KHOAN_DOI_UNG	
                                ExchangeRate , --Tỷ giá				
                                SUM(DebitAmountOC) ,	-- Phát sinh nợ --GHI_NO_NGUYEN_TE
                                SUM(DebitAmount) , -- Phát sinh nợ quy đổi --GHI_NO
                                SUM(CreditAmountOC) , -- Phát sinh có --GHI_CO_NGUYEN_TE
                                SUM(CreditAmount) , -- Phát sinh có quy đổi --GHI_CO
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN SUM(ClosingDebitAmountOC)
                                            - SUM(ClosingCreditAmountOC)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN SUM(ClosingDebitAmountOC)
                                                      - SUM(ClosingCreditAmountOC) > 0
                                                 THEN SUM(ClosingDebitAmountOC)
                                                      - SUM(ClosingCreditAmountOC)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ --ClosingDebitAmountOC
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN SUM(ClosingDebitAmount)
                                            - SUM(ClosingCreditAmount)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount) > 0
                                                 THEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( SUM(ClosingCreditAmountOC)
                                              - SUM(ClosingDebitAmountOC) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmountOC)
                                                        - SUM(ClosingDebitAmountOC) ) > 0
                                                 THEN ( SUM(ClosingCreditAmountOC)
                                                        - SUM(ClosingDebitAmountOC) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( SUM(ClosingCreditAmount)
                                              - SUM(ClosingDebitAmount) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) ) > 0
                                                 THEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi --		ClosingCreditAmount						  
                                InventoryItemCode ,
                                InventoryItemName ,
                                UnitName ,
                                UnitPrice ,
                                Quantity ,
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName ,
                                SortOrder ,
                                DetailPostOrder
                        FROM    ( SELECT    PW.ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                                            PW.ProjectWorkName , -- Tên công trình --TEN_CONG_TRINH
                                            PWC.ProjectWorkCategoryName , --Tên loại CT
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm 
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate --NGAY_HACH_TOAN
                                            END AS PostedDate , -- Ngày hạch toán
                                            --CASE WHEN AOL.PostedDate < @FromDate
                                            --     THEN NULL
                                            --     WHEN AOL.InvDate IS NULL
                                            --          OR LEN(ISNULL(AOL.InvNo,
                                            --                  '')) = 0
                                            --     THEN RefDate
                                            --     ELSE AOL.InvDate
                                            --END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            --CASE WHEN AOL.PostedDate < @FromDate
                                            --     THEN NULL
                                            --     WHEN AOL.InvDate IS NULL
                                            --          OR LEN(ISNULL(AOL.InvNo,
                                            --                  '')) = 0
                                            --     THEN AOL.RefNo
                                            --     ELSE AOL.InvNo
                                            --END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate--NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            
                                            --BTAnh-21/07/2015
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID --ID_CHUNG_TU
                                            END AS RefID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType --LOAI_CHUNG_TU
                                            END AS RefType , --Loại chứng từ
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE CAST(RefDetailID AS NVARCHAR(50))
                                            END AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.Description --DIEN_GIAI
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Detail) --DIEN_GIAI_CHUNG
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.DebitAmountOC --GHI_NO_NGUYEN_TE
                                            END AS DebitAmountOC , -- Phát sinh nợ
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.DebitAmount --GHI_NO
                                            END AS DebitAmount , -- Phát sinh nợ quy đổi
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.CreditAmountOC --GHI_CO_NGUYEN_TE
                                            END AS CreditAmountOC , -- Phát sinh có
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.CreditAmount --GHI_CO
                                            END AS CreditAmount , -- Phát sinh có quy đổi
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmountOC
                                                 ELSE $0
                                            END AS ClosingDebitAmountOC , --Dư Nợ --ClosingDebitAmountOC
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmount
                                                 ELSE $0
                                            END AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmountOC
                                                 ELSE $0
                                            END AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmount
                                                 ELSE $0
                                            END AS ClosingCreditAmount , --Dư Có quy đổi --ClosingCreditAmount
											--
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InventoryItemCode
                                            END AS InventoryItemCode , --Mã hàng
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InventoryItemName
                                            END AS InventoryItemName , --Tên hàng
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE U.UnitName
                                            END AS UnitName , --ĐVT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                      OR CorrespondingAccountNumber LIKE '33311%'
                                                      OR CorrespondingAccountNumber LIKE '1331%'
                                                      OR CorrespondingAccountNumber LIKE '1332%'
                                                      OR CorrespondingAccountNumber LIKE '521%'
                                                      OR Reftype IN ( 3040,
                                                              3041, 3042, 3043 ) --giảm giá hàng mua
                                                      THEN NULL
                                                 ELSE ( CASE WHEN @CurrencyID IS NULL
                                                             THEN AOL.UnitPrice
                                                             ELSE AOL.UnitPriceOC
                                                        END )
                                            END AS UnitPrice , --Đơn giá
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                      OR CorrespondingAccountNumber LIKE '33311%'
                                                      OR CorrespondingAccountNumber LIKE '1331%'
                                                      OR CorrespondingAccountNumber LIKE '1332%'
                                                      OR CorrespondingAccountNumber LIKE '521%'
                                                      OR Reftype IN ( 3040,
                                                              3041, 3042, 3043 ) --giảm giá hàng mua
                                                      THEN NULL
                                                      /*DDKhanh CR128285 17/08/2017 với chứng từ mua hàng trả lại thì hiển thị giá trị âm trên báo cáo*/
                                                  WHEN AOL.Reftype IN ( 3030, 3031, 3032, 3033 ) --giảm giá hàng mua
													  THEN AOL.Quantity * (-1)
                                                 ELSE Quantity
                                            END AS Quantity , --Số lượng
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN BIDL.BranchName
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.SortOrder
                                            END AS SortOrder , --THU_TU_TRONG_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL --so_cong_no_chi_tiet
                                            INNER JOIN @tblListAccountObjectID --DS_KHACH_HANG_NCC
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent --AccountNumberPercent
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber --danh_muc_he_thong_tai_khoan
                                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                            INNER JOIN @tblListProjectWorkID LPID ON AOL.ProjectWorkID = LPID.ProjectWorkID --DS_LOAI_CONG_TRINH
                                            INNER JOIN @tblProjectWorkID PW ON LPID.MISACodeID LIKE PW.MISACodeID 
                                                              + '%'
                                            LEFT JOIN dbo.ProjectWorkCategory --danh_muc_loai_cong_trinh
                                            AS PWC ON PW.ProjectWorkCategoryID = PWC.ProjectWorkCategoryID
                                            LEFT JOIN dbo.Unit AS U ON AOL.UnitID = U.UnitID --danh_muc_don_vi_tinh
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                  WHERE     AOL.PostedDate <= @ToDate --NGAY_HACH_TOAN" <= den_ngay
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL --loai_tien_id = -1
                                                  OR AOL.CurrencyID = @CurrencyID--"currency_id" = loai_tien_id
                                                )
                                            AND AN.DetailByAccountObject = 1 --CHI_TIET_THEO_DOI_TUONG
                                            AND AN.AccountObjectType = 0--DOI_TUONG_SELECTION
                                ) AS RSNS
                        GROUP BY RSNS.ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                                RSNS.ProjectWorkName , -- Tên công trình--TEN_CONG_TRINH
                                RSNS.ProjectWorkCategoryName , --Tên loại CT
                                RSNS.AccountObjectID , --DOI_TUONG_ID
                                RSNS.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                RSNS.AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm 
                                RSNS.AccountObjectAddress , -- Địa chỉ
                                RSNS.PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RSNS.RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RSNS.RefNo , -- Số chứng từ --SO_CHUNG_TU
                                RSNS.InvDate ,
                                RSNS.InvNo ,
                                RSNS.RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RSNS.RefID , -- Mã chứng từ --ID_CHUNG_TU
                                RSNS.RefDetailID ,
                                RSNS.JournalMemo , -- Diễn giải		--	DIEN_GIAI_CHUNG		
                                RSNS.AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                RSNS.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                RSNS.CorrespondingAccountNumber , --TK đối ứng		 --		MA_TAI_KHOAN_DOI_UNG
                                RSNS.ExchangeRate , --Tỷ giá
                                RSNS.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng
                                InventoryItemCode ,
                                InventoryItemName ,
                                UnitName ,
                                UnitPrice ,
                                Quantity ,
                                RSNS.OrderType ,
                                BranchName ,
                                RSNS.SortOrder ,--THU_TU_TRONG_CHUNG_TU
                                RSNS.DetailPostOrder
                        HAVING  SUM(DebitAmountOC) <> 0 --GHI_NO_NGUYEN_TE
                                OR SUM(DebitAmount) <> 0 --GHI_NO
                                OR SUM(CreditAmountOC) <> 0 --GHI_CO_NGUYEN_TE
                                OR SUM(CreditAmount) <> 0 --GHI_CO
                                OR SUM(ClosingDebitAmountOC--ClosingDebitAmountOC
                                       - ClosingCreditAmountOC) <> 0 --ClosingCreditAmountOC
                                OR SUM(ClosingDebitAmount --ClosingDebitAmount
                                       - ClosingCreditAmount) <> 0 --ClosingCreditAmount
                        ORDER BY RSNS.ProjectWorkName ,
                                RSNS.AccountObjectName ,
                                RSNS.ProjectWorkCode ,
                                RSNS.AccountNumber ,
                                RSNS.OrderType ,
                                RSNS.PostedDate ,
                                RSNS.RefDate ,
                                RSNS.RefNo ,
                                RSNS.SortOrder ,
                                RSNS.DetailPostOrder 


            END
        ELSE -- Cộng gộp các bút toán giống nhau
            BEGIN
                INSERT  INTO @tblResult
                        ( ProjectWorkCode , -- Mã công trình
                          ProjectWorkName , -- Tên công trình
                          ProjectWorkCategoryName , --Tên loại CT
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm  
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				
                          ExchangeRate , --Tỷ giá				
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName ,
                          SortOrder ,
                          DetailPostOrder 
                        )
                        SELECT  ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                                ProjectWorkName , -- Tên công trình --TEN_CONG_TRINH
                                ProjectWorkCategoryName , -- Tên loại cT
                                AccountObjectID , --DOI_TUONG_ID
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm  
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ --ID_CHUNG_TU
                                RefDetailID ,
                                JournalMemo , -- Diễn giải		 --DIEN_GIAI_CHUNG			
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng	--	MA_TAI_KHOAN_DOI_UNG		 
                                ExchangeRate , --Tỷ giá				
                                DebitAmountOC ,	-- Phát sinh nợ --GHI_NO_NGUYEN_TE
                                DebitAmount , -- Phát sinh nợ quy đổi--GHI_NO
                                CreditAmountOC , -- Phát sinh có --GHI_CO_NGUYEN_TE
                                CreditAmount , -- Phát sinh có quy đổi --GHI_CO
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                            - ClosingCreditAmountOC --ClosingCreditAmountOC
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC > 0
                                                 THEN ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ --ClosingDebitAmountOC
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ClosingDebitAmount
                                            - ClosingCreditAmount
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN ClosingDebitAmount
                                                      - ClosingCreditAmount > 0
                                                 THEN ClosingDebitAmount
                                                      - ClosingCreditAmount
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmountOC
                                              - ClosingDebitAmountOC )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC ) > 0
                                                 THEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmount
                                              - ClosingDebitAmount )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount ) > 0
                                                 THEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi --ClosingCreditAmount
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName ,
                                0 AS SortOrder ,
                                DetailPostOrder
                        FROM    ( SELECT    PW.ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                                            PW.ProjectWorkName , -- Tên công trình -- TEN_CONG_TRINH
                                            PWC.ProjectWorkCategoryName , --Tên loại công trình
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm  
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán --NGAY_HACH_TOAN
                                            --CASE WHEN AOL.PostedDate < @FromDate
                                            --     THEN NULL
                                            --     WHEN AOL.InvDate IS NULL
                                            --          OR LEN(ISNULL(AOL.InvNo,
                                            --                  '')) = 0
                                            --     THEN RefDate
                                            --     ELSE AOL.InvDate
                                            --END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            --CASE WHEN AOL.PostedDate < @FromDate
                                            --     THEN NULL
                                            --     WHEN AOL.InvDate IS NULL
                                            --          OR LEN(ISNULL(AOL.InvNo,
                                            --                  '')) = 0
                                            --     THEN AOL.RefNo
                                            --     ELSE AOL.InvNo
                                            --END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate--NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID --ID_CHUNG_TU
                                            END AS RefID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType --LOAI_CHUNG_TU
                                            END AS RefType , --Loại chứng từ
                                            MAX(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN NULL
                                                     ELSE CAST(RefDetailID AS NVARCHAR(50))
                                                END) AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Master) --DIEN_GIAI_CHUNG
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE AOL.DebitAmountOC --GHI_NO_NGUYEN_TE
                                                END) AS DebitAmountOC , -- Phát sinh nợ
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE AOL.DebitAmount --GHI_NO
                                                END) AS DebitAmount , -- Phát sinh nợ quy đổi
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE AOL.CreditAmountOC --GHI_CO_NGUYEN_TE
                                                END) AS CreditAmountOC , -- Phát sinh có
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE AOL.CreditAmount --GHI_CO
                                                END) AS CreditAmount , -- Phát sinh có quy đổi
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmountOC
                                                     ELSE $0
                                                END) AS ClosingDebitAmountOC , --Dư Nợ --ClosingDebitAmountOC
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmount
                                                     ELSE $0
                                                END) AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmountOC
                                                     ELSE $0
                                                END) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmount
                                                     ELSE $0
                                                END) AS ClosingCreditAmount , --Dư Có quy đổi --ClosingCreditAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL --so_cong_no_chi_tiet
                                            INNER JOIN @tblListAccountObjectID --DS_KHACH_HANG_NCC
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblListProjectWorkID LPID ON AOL.ProjectWorkID = LPID.ProjectWorkID --DS_LOAI_CONG_TRINH
                                            INNER JOIN @tblProjectWorkID PW ON LPID.MISACodeID LIKE PW.MISACodeID --DS_CONG_TRINH
                                                              + '%'
                                            LEFT JOIN dbo.ProjectWorkCategory --danh_muc_loai_cong_trinh
                                            AS PWC ON PW.ProjectWorkCategoryID = PWC.ProjectWorkCategoryID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent --TMP_TAI_KHOAN
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber --danh_muc_he_thong_tai_khoan
                                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT --danh_muc_don_vi_tinh
                                  WHERE     AOL.PostedDate <= @ToDate
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL --loai_tien_id = -1
                                                  OR AOL.CurrencyID = @CurrencyID --"currency_id" = loai_tien_id
                                                )
                                            AND AN.DetailByAccountObject = 1 --CHI_TIET_THEO_DOI_TUONG
                                            AND AN.AccountObjectType = 0 --DOI_TUONG_SELECTION
                                  GROUP BY  PW.ProjectWorkCode , -- Mã công trình --MA_CONG_TRINH
                                            PW.ProjectWorkName , -- Tên công trình --TEN_CONG_TRINH
                                            PWC.ProjectWorkCategoryName ,
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm  
                                            AOL.AccountObjectAddressDI , -- Địa chỉ
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate --NGAY_HACH_TOAN
                                            END , -- Ngày hạch toán
                                            --CASE WHEN AOL.PostedDate < @FromDate
                                            --     THEN NULL
                                            --     WHEN AOL.InvDate IS NULL
                                            --          OR LEN(ISNULL(AOL.InvNo,
                                            --                  '')) = 0
                                            --     THEN RefDate
                                            --     ELSE AOL.InvDate
                                            --END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            --CASE WHEN AOL.PostedDate < @FromDate
                                            --     THEN NULL
                                            --     WHEN AOL.InvDate IS NULL
                                            --          OR LEN(ISNULL(AOL.InvNo,
                                            --                  '')) = 0
                                            --     THEN AOL.RefNo
                                            --     ELSE AOL.InvNo
                                            --END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate--NGAY_CHUNG_TU
                                            END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END , --Loại chứng từ
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END , -- Diễn giải (lấy diễn giải Master)
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END , --TK đối ứng
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END , --Tỷ giá
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END
                                ) AS RSS
                        WHERE   RSS.DebitAmountOC <> 0 --GHI_NO_NGUYEN_TE
                                OR RSS.CreditAmountOC <> 0 --GHI_NO
                                OR RSS.DebitAmount <> 0 --GHI_CO_NGUYEN_TE
                                OR RSS.CreditAmount <> 0 --GHI_CO
                                OR ClosingCreditAmountOC --ClosingCreditAmountOC
                                - ClosingDebitAmountOC <> 0 --ClosingDebitAmountOC
                                OR ClosingCreditAmount - ClosingDebitAmount <> 0 --ClosingCreditAmount -ClosingDebitAmount
                        ORDER BY RSS.ProjectWorkName ,
                                RSS.AccountObjectName ,
                                RSS.ProjectWorkCode ,
                                RSS.AccountNumber ,
                                RSS.OrderType ,
                                RSS.PostedDate ,
                                RSS.RefDate ,
                                RSS.RefNo ,
                                RSS.DetailPostOrder
            END 				
					

/* Tính số tồn */



        DECLARE @CloseAmountOC AS DECIMAL(22, 8) ,
            @CloseAmount AS DECIMAL(22, 8) ,
            @ProjectWorkCode_tmp NVARCHAR(100) ,
            @AccountObjectCode_tmp NVARCHAR(100) ,
            @AccountNumber_tmp NVARCHAR(20)
        SELECT  @CloseAmountOC = 0 ,
                @CloseAmount = 0 ,
                @ProjectWorkCode_tmp = N'' ,
                @AccountObjectCode_tmp = N'' ,
                @AccountNumber_tmp = N''
	
        UPDATE  @tblResult
        SET     @CloseAmountOC = ( CASE WHEN OrderType = 0
                                        THEN ( CASE WHEN ClosingDebitAmountOC = 0
                                                    THEN ClosingCreditAmountOC
                                                    ELSE -1
                                                         * ClosingDebitAmountOC
                                               END )
                                        WHEN @ProjectWorkCode_tmp <> ProjectWorkCode
                                             OR @AccountObjectCode_tmp <> AccountObjectCode
                                             OR @AccountNumber_tmp <> AccountNumber
                                        THEN CreditAmountOC - DebitAmountOC
                                        ELSE @CloseAmountOC + CreditAmountOC
                                             - DebitAmountOC
                                   END ) ,
                ClosingDebitAmountOC = ( CASE WHEN AccountCategoryKind = 0
                                              THEN -1 * @CloseAmountOC
                                              WHEN AccountCategoryKind = 1
                                              THEN $0
                                              ELSE CASE WHEN @CloseAmountOC < 0
                                                        THEN -1
                                                             * @CloseAmountOC
                                                        ELSE $0
                                                   END
                                         END ) ,
                ClosingCreditAmountOC = ( CASE WHEN AccountCategoryKind = 1
                                               THEN @CloseAmountOC
                                               WHEN AccountCategoryKind = 0
                                               THEN $0
                                               ELSE CASE WHEN @CloseAmountOC > 0
                                                         THEN @CloseAmountOC
                                                         ELSE $0
                                                    END
                                          END ) ,
                @CloseAmount = ( CASE WHEN OrderType = 0
                                      THEN ( CASE WHEN ClosingDebitAmount = 0
                                                  THEN ClosingCreditAmount
                                                  ELSE -1 * ClosingDebitAmount
                                             END )
                                      WHEN @ProjectWorkCode_tmp <> ProjectWorkCode
                                           OR @AccountObjectCode_tmp <> AccountObjectCode
                                           OR @AccountNumber_tmp <> AccountNumber
                                      THEN CreditAmount - DebitAmount
                                      ELSE @CloseAmount + CreditAmount
                                           - DebitAmount
                                 END ) ,
                ClosingDebitAmount = ( CASE WHEN AccountCategoryKind = 0
                                            THEN -1 * @CloseAmount
                                            WHEN AccountCategoryKind = 1
                                            THEN $0
                                            ELSE CASE WHEN @CloseAmount < 0
                                                      THEN -1 * @CloseAmount
                                                      ELSE $0
                                                 END
                                       END ) ,
                ClosingCreditAmount = ( CASE WHEN AccountCategoryKind = 1
                                             THEN @CloseAmount
                                             WHEN AccountCategoryKind = 0
                                             THEN $0
                                             ELSE CASE WHEN @CloseAmount > 0
                                                       THEN @CloseAmount
                                                       ELSE $0
                                                  END
                                        END ) ,
                @ProjectWorkCode_tmp = ProjectWorkCode ,
                @AccountObjectCode_tmp = AccountObjectCode ,
                @AccountNumber_tmp = AccountNumber--,
        WHERE   OrderType <> 2

		

/*Lấy số liệu*/				
        SELECT  RS.*
        FROM    @tblResult RS        
    END


GO


-------------------------------------------------------Thống kê theo hợp đồng mua--------------------------------------------------------
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		DCQUY
-- Create date: 02/07/2014
-- Description:	<Mua hàng: Lấy số liệu chi tiết công nợ phải trả theo hợp đồng mua>
-- Modified By NTGIANG 29.09.2014: Viết lại
-- Proc_PUReport_GetPUPaymentDetailByPurchaseContract '9/1/2014', '9/30/2014', '02fa2e49-bf0d-4352-8405-c860c8135e93', 1, N'111', N',20D4C331-60A7-44F6-9459-364114EB02CB,', NULL, N',B871ED21-AB49-45E1-8F76-DAFC6D768EF6,',0, 1
-- tthoa 4/10/2014: chỉnh lại một chút đoạn nhầm credit, debit
-- nvtoan modify 17/01/2014: Sửa lỗi không lấy cặp định khoản chênh lệch tỷ giá
-- nvtoan modify 28/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- nvtoan modify 12/02/2015: Sửa lỗi không lấy số chứng từ, ngày chứng từ đúng theo mô tả
-- nmtruong 23/10/2015: sửa lỗi 74886: thêm Cột Rownum ở bảng @tblResult và sort khi insert để khi update số dư đúng thứ tự
-- VHAnh modified 11.11.2015: Bổ sung Mã, Tên nhóm KH/NCC (CR 73635)
-- VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá khi trên báo cáo có dòng xử lý chênh lệch tỷ giá (bug 109651).
/*ntlieu 22.02.2018 thi công PBI 172744 mở rộng cột số hợp đồng mua lên 50 ký tự*/
-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @AccountNumber NVARCHAR(20) -- Số tài khoản
 DECLARE   @AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã nhóm nhà cung cấp
 DECLARE   @CurrencyID NVARCHAR(3) -- Loại tiền
 DECLARE   @SupplierID AS NVARCHAR(MAX)  -- Danh sách mã hợp đồng
 DECLARE   @IsSimilarSum BIT  -- Có cộng gộp các bút toán giống nhau không? 
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?    



		SET					@FromDate = '2018-01-01 00:00:00'
        SET                    @ToDate = '2018-12-31 23:59:59'
        SET                    @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
        SET                    @IncludeDependentBranch = 1
        SET                    @AccountNumber = NULL
        SET                    @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
        SET                    @CurrencyID = N'VND'
        SET                    @SupplierID = N',fa5b2fae-4ab9-496e-ae94-04c5cd6c50ff,bda81d75-e38a-4645-b1da-77a6596a9972,d2781cb6-e193-4793-8082-20f3e95273a3,'
        SET                    @IsSimilarSum = 0
        SET                    @IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblBranchIDList TABLE
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCod NVARCHAR(20) ,
              BranchName NVARCHAR(128)
            )	
       
        INSERT  INTO @tblBranchIDList
                SELECT  FGDBBI.BranchID ,
                        BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI
               
        -- vhanh added 11/11/2015: Lấy thêm mã nhóm và tên nhóm KH/NCC       
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL -- Danh sách tên nhóm
            ) 
        INSERT  INTO @tblListAccountObjectID --DS_KHACH_HANG_NCC
                SELECT  AccountObjectID ,
                        AccountObjectGroupListCode , -- Danh sách mã nhóm
                        AccountObjectGroupListName -- Danh sách tên nhóm   
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') tblAccountObjectSelected
                        INNER JOIN dbo.AccountObject AO ON AO.AccountObjectID = tblAccountObjectSelected.Value	        			
        
        DECLARE @tblListPUContractID TABLE -- Bảng chứa danh sách mã hợp đồng
            (
              PUContractID UNIQUEIDENTIFIER
            ) 
        INSERT  INTO @tblListPUContractID --DS_HOP_DONG_MUA
                SELECT  *
                FROM    dbo.Func_ConvertGUIStringIntoTable(@SupplierID, ',')	  
                                                                            
		-- Bảng chứa kết quả cần lấy
        DECLARE @tblResult TABLE
            (
              RowNum INT IDENTITY(1, 1)
                         PRIMARY KEY ,
              PUContractCode NVARCHAR(50) , /*ntlieu 22.02.2018 thi công PBI 172744 mở rộng cột số hợp đồng mua lên 50 ký tự*/
              PUSignDate DATETIME , -- Ngày ký hợp đồng mua
              PUContractName NVARCHAR(255) ,   -- Trích yếu hợp đồng mua
              BranchID UNIQUEIDENTIFIER ,
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(100) ,   -- Mã NCC
              AccountObjectName NVARCHAR(255) ,	-- Tên NCC
              AccountObjectGroupListCode NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách mã nhóm
              AccountObjectGroupListName NVARCHAR(MAX)
                COLLATE SQL_Latin1_General_CP1_CI_AS
                NULL , -- Danh sách tên nhóm                
              AccountObjectAddress NVARCHAR(255) , -- Địa chỉ
              PostedDate DATETIME ,	-- Ngày hạch toán
              RefDate DATETIME , -- Ngày chứng từ
              RefNo NVARCHAR(22) , -- Số chứng từ
              --BTAnh bổ sung ngày 21/07/2015 (JIRA: SMEFIVE-2297)
              InvDate DATETIME ,
              InvNo NVARCHAR(500) ,-- KDCHIEN 30.08.2018:258458:SMESEVEN-26725: Dãn dộ rộng 500 theo sổ
              --
              RefType INT ,	--Loại chứng từ
              RefID UNIQUEIDENTIFIER , -- Mã chứng từ                            
              RefDetailID NVARCHAR(50) ,
              JournalMemo NVARCHAR(255) , -- Diễn giải
              AccountNumber NVARCHAR(20) , -- Số tài khoản
              AccountCategoryKind INT , -- Tính chất tài khoản
              CorrespondingAccountNumber NVARCHAR(20) , --TK đối ứng
              ExchangeRate DECIMAL(18, 4) , --Tỷ giá
              DebitAmountOC MONEY ,	-- Phát sinh nợ
              DebitAmount MONEY , -- Phát sinh nợ quy đổi
              CreditAmountOC MONEY , -- Phát sinh có
              CreditAmount MONEY , -- Phát sinh có quy đổi
              ClosingDebitAmountOC MONEY , --Dư Nợ
              ClosingDebitAmount MONEY , --Dư Nợ Quy đổi
              ClosingCreditAmountOC MONEY ,	--Dư Có
              ClosingCreditAmount MONEY , --Dư Có quy đổi 
              IsBold BIT , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
              OrderType INT ,
              BranchName NVARCHAR(128)
            )
            
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
                                AND AccountObjectType = 0
                                AND IsParent = 0
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END 
/*Lấy số dư đầu kỳ và dữ liệu phát sinh trong kỳ:*/
        IF @IsSimilarSum = 0 -- Nếu không cộng gộp
            BEGIN
                INSERT  INTO @tblResult
                        ( PUContractCode , -- Mã hợp đồng mua     
                          PUSignDate , -- Ngày ký hợp đồng mua
                          PUContractName ,   -- Trích yếu hợp đồng mua
                          BranchID ,
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi    
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName
                        )
                        SELECT  PUContractCode , -- Mã hợp đồng mua     
                                PUSignDate , -- Ngày ký hợp đồng mua
                                PUContractName ,   -- Trích yếu hợp đồng mua
                                BranchID ,
                                AccountObjectID ,--
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ    --ID_CHUNG_TU
                                RefDetailID ,
                                JournalMemo , -- Diễn giải				--	  DIEN_GIAI_CHUNG
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản--TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng	--	MA_TAI_KHOAN_DOI_UNG		  
                                ExchangeRate , --Tỷ giá				  
                                SUM(DebitAmountOC) ,	-- Phát sinh nợ
                                SUM(DebitAmount) , -- Phát sinh nợ quy đổi
                                SUM(CreditAmountOC) , -- Phát sinh có
                                SUM(CreditAmount) , -- Phát sinh có quy đổi
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN SUM(ClosingDebitAmountOC)
                                            - SUM(ClosingCreditAmountOC)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN SUM(ClosingDebitAmountOC)
                                                      - SUM(ClosingCreditAmountOC) > 0
                                                 THEN SUM(ClosingDebitAmountOC)
                                                      - SUM(ClosingCreditAmountOC)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ  ---ClosingDebitAmountOC           
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN SUM(ClosingDebitAmount)
                                            - SUM(ClosingCreditAmount)
                                       WHEN AccountCategoryKind = 1 THEN $0
                                       ELSE CASE WHEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount) > 0
                                                 THEN SUM(ClosingDebitAmount)
                                                      - SUM(ClosingCreditAmount)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN SUM(ClosingCreditAmountOC)
                                            - SUM(ClosingDebitAmountOC)
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN SUM(ClosingCreditAmountOC)
                                                      - SUM(ClosingDebitAmountOC) > 0
                                                 THEN SUM(ClosingCreditAmountOC)
                                                      - SUM(ClosingDebitAmountOC)
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( SUM(ClosingCreditAmount)
                                              - SUM(ClosingDebitAmount) )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) ) > 0
                                                 THEN ( SUM(ClosingCreditAmount)
                                                        - SUM(ClosingDebitAmount) )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi -- ClosingCreditAmount                       
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng
                                OrderType ,
                                BranchName
                        FROM    ( SELECT    AOL.PUContractCode , -- Mã hợp đồng mua     
                                            AOL.PUSignDate , -- Ngày ký hợp đồng mua
                                            AOL.PUContractName ,   -- Trích yếu hợp đồng mua
                                            AOL.BranchID ,
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán    --NGAY_HACH_TOAN              
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--	ELSE AOL.InvDate
											--END AS RefDate, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefNo
											--	ELSE AOL.InvNo
											--END AS RefNo, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  ---SO_CHUNG_TU
                                            
                                            --BTAnh-21/07/2015
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE CAST(RefDetailID AS NVARCHAR(50))
                                            END AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.Description --DIEN_GIAI
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Detail)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng   --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.DebitAmountOC --GHI_NO_NGUYEN_TE
                                            END AS DebitAmountOC , -- Phát sinh nợ                                    
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.DebitAmount --GHI_NO
                                            END AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.CreditAmountOC --GHI_CO_NGUYEN_TE
                                            END AS CreditAmountOC , -- Phát sinh có  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN $0
                                                 ELSE AOL.CreditAmount --GHI_CO
                                            END AS CreditAmount , -- Phát sinh có quy đổi
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmountOC --
                                                 ELSE $0
                                            END AS ClosingDebitAmountOC , --Dư Nợ --    ClosingDebitAmountOC       
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.DebitAmount
                                                 ELSE $0
                                            END AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmountOC
                                                 ELSE $0
                                            END AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN AOL.CreditAmount
                                                 ELSE $0
                                            END AS ClosingCreditAmount , --Dư Có quy đổi  --ClosingCreditAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.SortOrder
                                            END AS SortOrder , --THU_TU_TRONG_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL --so_cong_no_chi_tiet
                                            INNER JOIN @tblListAccountObjectID
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                                            INNER JOIN @tblBranchIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                         INNER JOIN @tblListPUContractID LCID ON AOL.PUContractID = LCID.PUContractID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                  WHERE     AOL.PostedDate <= @ToDate
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL
                                                  OR AOL.CurrencyID = @CurrencyID
                                                )
                                            AND AN.DetailByAccountObject = 1
                                            AND AN.AccountObjectType = 0
                                ) AS RSNS
                        WHERE   ( RSNS.RefDetailID IS NOT NULL
                                  AND ( RSNS.DebitAmountOC <> 0
                                        OR RSNS.CreditAmountOC <> 0
                                        OR RSNS.DebitAmount <> 0
                                        OR RSNS.CreditAmount <> 0
                                      )
                                )
                                OR ( RSNS.RefDetailID IS NULL
                                     AND ( ClosingCreditAmountOC <> 0
                                           OR ClosingDebitAmountOC <> 0
                                           OR ClosingCreditAmount <> 0
                                           OR ClosingDebitAmount <> 0
                                         )
                                   )
                        GROUP BY RSNS.PUContractCode , -- Mã hợp đồng mua     
                                RSNS.PUSignDate , -- Ngày ký hợp đồng mua
                                RSNS.PUContractName ,   -- Trích yếu hợp đồng mua
                                RSNS.BranchID ,
                                RSNS.AccountObjectID ,
                                RSNS.AccountObjectCode ,   -- Mã NCC
                                RSNS.AccountObjectName ,	-- Tên NCC
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                RSNS.AccountObjectAddress , -- Địa chỉ
                                RSNS.PostedDate ,	-- Ngày hạch toán
                                RSNS.RefDate , -- Ngày chứng từ
                                RSNS.RefNo , -- Số chứng từ
                                RSNS.InvDate ,
                                RSNS.InvNo ,
                                RSNS.RefType ,	--Loại chứng từ
                                RSNS.RefID , -- Mã chứng từ   
                                RSNS.RefDetailID ,
                                RSNS.JournalMemo , -- Diễn giải					  
                                RSNS.AccountNumber , -- Số tài khoản
                                RSNS.AccountCategoryKind , -- Tính chất tài khoản
                                RSNS.CorrespondingAccountNumber , --TK đối ứng				  
                                RSNS.ExchangeRate , --Tỷ giá  
                                RSNS.IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng
                                RSNS.OrderType ,
                                BranchName ,
                                RSNS.SortOrder ,
                                RSNS.DetailPostOrder
                        HAVING  SUM(DebitAmountOC) <> 0
                                OR SUM(DebitAmount) <> 0
                                OR SUM(CreditAmountOC) <> 0
                                OR SUM(CreditAmount) <> 0
                                OR SUM(ClosingDebitAmount
                                       - ClosingCreditAmount) <> 0
                                OR SUM(ClosingDebitAmountOC
                                       - ClosingCreditAmountOC) <> 0
                        ORDER BY RSNS.PUContractCode ,
                                RSNS.BranchID ,
                                RSNS.AccountObjectCode ,
                                RSNS.AccountNumber ,
                                RSNS.OrderType ,
                                RSNS.PostedDate ,
                                RSNS.RefDate ,
                                RSNS.RefNo ,
                                RSNS.DetailPostOrder
            END
        ELSE -- Cộng gộp các bút toán giống nhau
            BEGIN
                INSERT  INTO @tblResult
                        ( PUContractCode , -- Mã hợp đồng mua     
                          PUSignDate , -- Ngày ký hợp đồng mua
                          PUContractName ,   -- Trích yếu hợp đồng mua
                          BranchID ,
                          AccountObjectID ,
                          AccountObjectCode ,   -- Mã NCC
                          AccountObjectName ,	-- Tên NCC
                          AccountObjectGroupListCode , -- Danh sách mã nhóm
                          AccountObjectGroupListName , -- Danh sách tên nhóm              
                          AccountObjectAddress , -- Địa chỉ
                          PostedDate ,	-- Ngày hạch toán
                          RefDate , -- Ngày chứng từ
                          RefNo , -- Số chứng từ
                          InvDate ,
                          InvNo ,
                          RefType ,	--Loại chứng từ
                          RefID , -- Mã chứng từ   
                          RefDetailID ,
                          JournalMemo , -- Diễn giải					  
                          AccountNumber , -- Số tài khoản
                          AccountCategoryKind , -- Tính chất tài khoản
                          CorrespondingAccountNumber , --TK đối ứng				  
                          ExchangeRate , --Tỷ giá				  
                          DebitAmountOC ,	-- Phát sinh nợ
                          DebitAmount , -- Phát sinh nợ quy đổi
                          CreditAmountOC , -- Phát sinh có
                          CreditAmount , -- Phát sinh có quy đổi
                          ClosingDebitAmountOC , --Dư Nợ
                          ClosingDebitAmount , --Dư Nợ Quy đổi
                          ClosingCreditAmountOC ,	--Dư Có
                          ClosingCreditAmount , --Dư Có quy đổi  
                          IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                          OrderType ,
                          BranchName
                        )
                        SELECT  PUContractCode , -- Mã hợp đồng mua     
                                PUSignDate , -- Ngày ký hợp đồng mua
                                PUContractName ,   -- Trích yếu hợp đồng mua
                                BranchID ,
                                AccountObjectID , --DOI_TUONG_ID
                                AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                AccountObjectGroupListCode , -- Danh sách mã nhóm
                                AccountObjectGroupListName , -- Danh sách tên nhóm              
                                AccountObjectAddress , -- Địa chỉ
                                PostedDate ,	-- Ngày hạch toán --NGAY_HACH_TOAN
                                RefDate , -- Ngày chứng từ --NGAY_CHUNG_TU
                                RefNo , -- Số chứng từ --SO_CHUNG_TU
                                InvDate ,
                                InvNo ,
                                RefType ,	--Loại chứng từ --LOAI_CHUNG_TU
                                RefID , -- Mã chứng từ    --ID_CHUNG_TU
                                RefDetailID ,
                                JournalMemo , -- Diễn giải	--	DIEN_GIAI_CHUNG			  
                                AccountNumber , -- Số tài khoản --SO_TAI_KHOAN
                                AccountCategoryKind , -- Tính chất tài khoản -- TINH_CHAT
                                CorrespondingAccountNumber , --TK đối ứng	 --		MA_TAI_KHOAN_DOI_UNG	  
                                ExchangeRate , --Tỷ giá				  
                                DebitAmountOC ,	-- Phát sinh nợ --GHI_NO_NGUYEN_TE
                                DebitAmount , -- Phát sinh nợ quy đổi --GHI_NO
                                CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                CreditAmount , -- Phát sinh có quy đổi  --GHI_CO
                                ( CASE WHEN AccountCategoryKind = 0 --TINH_CHAT
                                       THEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                            - ClosingCreditAmountOC -- ClosingCreditAmountOC
                                       WHEN AccountCategoryKind = 1 THEN $0 
                                       ELSE CASE WHEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC > 0 --ClosingCreditAmountOC
                                                 THEN ClosingDebitAmountOC --ClosingDebitAmountOC
                                                      - ClosingCreditAmountOC --ClosingCreditAmountOC
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmountOC , --Dư Nợ   --ClosingDebitAmountOC         
                                ( CASE WHEN AccountCategoryKind = 0
                                       THEN ClosingDebitAmount --ClosingDebitAmount
                                            - ClosingCreditAmount --ClosingCreditAmount
                                       WHEN AccountCategoryKind = 1 THEN $0 
                                       ELSE CASE WHEN ClosingDebitAmount --ClosingDebitAmount
                                                      - ClosingCreditAmount > 0 --ClosingCreditAmount
                                                 THEN ClosingDebitAmount  --ClosingDebitAmount
                                                      - ClosingCreditAmount --ClosingCreditAmount
                                                 ELSE $0
                                            END
                                  END ) AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmountOC
                                              - ClosingDebitAmountOC )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC ) > 0
                                                 THEN ( ClosingCreditAmountOC
                                                        - ClosingDebitAmountOC )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmountOC , --Dư Có
                                ( CASE WHEN AccountCategoryKind = 1
                                       THEN ( ClosingCreditAmount
                                              - ClosingDebitAmount )
                                       WHEN AccountCategoryKind = 0 THEN $0
                                       ELSE CASE WHEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount ) > 0
                                                 THEN ( ClosingCreditAmount
                                                        - ClosingDebitAmount )
                                                 ELSE $0
                                            END
                                  END ) AS ClosingCreditAmount , --Dư Có quy đổi  
                                IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng	
                                OrderType ,
                                BranchName
                        FROM    ( SELECT    AOL.PUContractCode , -- Mã hợp đồng mua     
                                            AOL.PUSignDate , -- Ngày ký hợp đồng mua
                                            AOL.PUContractName ,   -- Trích yếu hợp đồng mua
                                            AOL.BranchID ,
                                            AOL.AccountObjectID , --DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI AS AccountObjectName ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI AS AccountObjectAddress , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END AS PostedDate , -- Ngày hạch toán-- NGAY_HACH_TOAN                 
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--	ELSE AOL.InvDate
											--END AS RefDate, -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefNo
											--	ELSE AOL.InvNo
											--END AS RefNo, -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END AS RefDate , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END AS RefNo , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END AS InvDate ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END AS InvNo ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID
                                            END AS RefID , --ID_CHUNG_TU
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType
                                            END AS RefType , --Loại chứng từ  --LOAI_CHUNG_TU
                                            MAX(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN NULL
                                                     ELSE CAST(RefDetailID AS NVARCHAR(50))
                                                END) AS RefDetailID ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END AS JournalMemo , -- Diễn giải (lấy diễn giải Master)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END AS CorrespondingAccountNumber , --TK đối ứng    --MA_TAI_KHOAN_DOI_UNG
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE /*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END AS ExchangeRate , --Tỷ giá 
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.DebitAmountOC ) --GHI_NO_NGUYEN_TE
                                                END) AS DebitAmountOC , -- Phát sinh nợ                                    
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.DebitAmount ) --GHI_NO
                                                END) AS DebitAmount , -- Phát sinh nợ quy đổi                                         
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.CreditAmountOC ) --
                                                END) AS CreditAmountOC , -- Phát sinh có  --GHI_CO_NGUYEN_TE
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN $0
                                                     ELSE ( AOL.CreditAmount )
                                                END) AS CreditAmount , -- Phát sinh có quy đổi --GHI_CO
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmountOC
                                                     ELSE $0
                                                END) AS ClosingDebitAmountOC , --Dư Nợ  --ClosingDebitAmountOC          
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.DebitAmount
                                                     ELSE $0
                                                END) AS ClosingDebitAmount , --Dư Nợ Quy đổi  --ClosingDebitAmount
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmountOC
                                                     ELSE $0
                                                END) AS ClosingCreditAmountOC , --Dư Có --ClosingCreditAmountOC
                                            SUM(CASE WHEN AOL.PostedDate < @FromDate
                                                     THEN AOL.CreditAmount
                                                     ELSE $0
                                                END) AS ClosingCreditAmount , --Dư Có quy đổi --ClosingCreditAmount
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END AS IsBold , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END AS OrderType ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END BranchName ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END AS DetailPostOrder
                                  FROM      dbo.AccountObjectLedger AS AOL
                                            INNER JOIN @tblListAccountObjectID
                                            AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                                            INNER JOIN @tblListPUContractID LCID ON AOL.PUContractID = LCID.PUContractID
                                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumberPercent
                                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                                            INNER JOIN @tblBranchIDList BIDL ON AOL.BranchID = BIDL.BranchID
                                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                                  WHERE     ( AOL.PostedDate <= @ToDate )
                                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                                            AND ( @CurrencyID IS NULL
                                                  OR AOL.CurrencyID = @CurrencyID
                                                )
                                            AND AN.DetailByAccountObject = 1
                                            AND AN.AccountObjectType = 0
                                  GROUP BY  AOL.PUContractCode , -- Mã hợp đồng mua     
                                            AOL.PUSignDate , -- Ngày ký hợp đồng mua
                                            AOL.PUContractName ,   -- Trích yếu hợp đồng mua
                                            AOL.BranchID ,
                                            AOL.AccountObjectID ,--DOI_TUONG_ID
                                            AOL.AccountObjectCode ,   -- Mã NCC --MA_DOI_TUONG
                                            AOL.AccountObjectNameDI ,	-- Tên NCC --TEN_DOI_TUONG
                                            AccountObjectGroupListCode , -- Danh sách mã nhóm
                                            AccountObjectGroupListName , -- Danh sách tên nhóm              
                                            AOL.AccountObjectAddressDI , -- Địa chỉ  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.PostedDate
                                            END , -- Ngày hạch toán                  
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefDate
											--	ELSE AOL.InvDate
											--END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
											--CASE 
											--	WHEN AOL.PostedDate < @FromDate THEN NULL
											--	WHEN AOL.InvDate IS NULL OR LEN(ISNULL(AOL.InvNo,'')) = 0 THEN RefNo
											--	ELSE AOL.InvNo
											--END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE RefDate --NGAY_CHUNG_TU
                                            END , -- Ngày chứng từ, ưu tiên lấy theo ngày hóa đơn nếu có cả ngày hóa đơn và số hóa đơn
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefNo --SO_CHUNG_TU
                                            END , -- Số chứng từ, ưu tiên lấy theo số hóa đơn nếu có cả ngày hóa đơn và số hóa đơn  
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvDate
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.InvNo
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefID --ID_CHUNG_TU
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.RefType --LOAI_CHUNG_TU
                                            END , --Loại chứng từ                                             
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN N'Số dư đầu kỳ'
                                                 ELSE AOL.JournalMemo --DIEN_GIAI_CHUNG
                                            END , -- Diễn giải (lấy diễn giải Master)     
                                            TBAN.AccountNumber , -- TK công nợ --SO_TAI_KHOAN
                                            TBAN.AccountCategoryKind , -- Tính chất tài khoản --TINH_CHAT
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.CorrespondingAccountNumber --MA_TK_DOI_UNG
                                            END , --TK đối ứng   
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE/*VHAnh edited 06.07.2016: Lấy lại thông tin tỷ giá*/
													CASE WHEN AOL.CashOutExchangeRateLedger IS NULL
															THEN AOL.ExchangeRate       
															ELSE AOL.CashOutExchangeRateLedger
													END
                                            END , --Tỷ giá 
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 1
                                                 ELSE 0
                                            END , -- Có bold hay không: dùng để bold dòng số dư và tổng cộng		
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN 0
                                                 ELSE 1
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE BIDL.BranchName
                                            END ,
                                            CASE WHEN AOL.PostedDate < @FromDate
                                                 THEN NULL
                                                 ELSE AOL.DetailPostOrder
                                            END
                                ) AS RSS
                        WHERE   RSS.DebitAmountOC <> 0 --GHI_NO_NGUYEN_TE
                                OR RSS.CreditAmountOC <> 0 --GHI_CO_NGUYEN_TE
                                OR RSS.DebitAmount <> 0 --GHI_NO
                                OR RSS.CreditAmount <> 0  --GHI_CO
                                OR ClosingCreditAmountOC
                                - ClosingDebitAmountOC <> 0
                                OR ClosingCreditAmount - ClosingDebitAmount <> 0
                        ORDER BY RSS.PUContractCode ,
                                RSS.BranchID ,
                                RSS.AccountObjectCode ,
                                RSS.AccountNumber ,
                                RSS.OrderType ,
                                RSS.PostedDate ,
                                RSS.RefDate ,
                                RSS.RefNo ,
                                RSS.DetailPostOrder
                        
            END                		
 
                        
/* Tính số tồn */
        DECLARE @CloseAmountOC AS DECIMAL(22, 8) ,
            @CloseAmount AS DECIMAL(22, 8) ,
            @PUContractCode_tmp NVARCHAR(100) ,
            @BranchID_tmp UNIQUEIDENTIFIER ,
            @AccountObjectCode_tmp NVARCHAR(100) ,
            @AccountNumber_tmp NVARCHAR(20)
        SELECT  @CloseAmountOC = 0 ,
                @CloseAmount = 0 ,
                @PUContractCode_tmp = N'' ,
                @BranchID_tmp = NULL ,
                @AccountObjectCode_tmp = N'' ,
                @AccountNumber_tmp = N''
	
        UPDATE  @tblResult
        SET     @CloseAmountOC = ( CASE WHEN OrderType = 0
                                        THEN ( CASE WHEN ClosingDebitAmountOC = 0
                                                    THEN ClosingCreditAmountOC
                                                    ELSE -1
                                                         * ClosingDebitAmountOC
                                               END )
                                        WHEN @PUContractCode_tmp <> PUContractCode
                                             OR @BranchID_tmp <> BranchID
                                             OR @AccountObjectCode_tmp <> AccountObjectCode
                                             OR @AccountNumber_tmp <> AccountNumber
                                        THEN CreditAmountOC - DebitAmountOC
                                        ELSE @CloseAmountOC + CreditAmountOC
                                             - DebitAmountOC
                                   END ) ,
                ClosingDebitAmountOC = ( CASE WHEN AccountCategoryKind = 0
                                              THEN -1 * @CloseAmountOC
                                              WHEN AccountCategoryKind = 1
                                              THEN $0
                                              ELSE CASE WHEN @CloseAmountOC < 0
                                                        THEN -1
                                                             * @CloseAmountOC
                                                        ELSE $0
                                                   END
                                         END ) ,
                ClosingCreditAmountOC = ( CASE WHEN AccountCategoryKind = 1
                                               THEN @CloseAmountOC
                                               WHEN AccountCategoryKind = 0
                                               THEN $0
                                               ELSE CASE WHEN @CloseAmountOC > 0
                                                         THEN @CloseAmountOC
                                                         ELSE $0
                                                    END
                                          END ) ,
                @CloseAmount = ( CASE WHEN OrderType = 0
                                      THEN ( CASE WHEN ClosingDebitAmount = 0
                                                  THEN ClosingCreditAmount
                                                  ELSE -1 * ClosingDebitAmount
                                             END )
                                      WHEN @PUContractCode_tmp <> PUContractCode
                                           OR @AccountObjectCode_tmp <> AccountObjectCode
                                           OR @AccountNumber_tmp <> AccountNumber
                                      THEN CreditAmount - DebitAmount
                                      ELSE @CloseAmount + CreditAmount
                                           - DebitAmount
                                 END ) ,
                ClosingDebitAmount = ( CASE WHEN AccountCategoryKind = 0
                                            THEN -1 * @CloseAmount
                                            WHEN AccountCategoryKind = 1
                                            THEN $0
                                            ELSE CASE WHEN @CloseAmount < 0
                                                      THEN -1 * @CloseAmount
                                                      ELSE $0
                                                 END
                                       END ) ,
                ClosingCreditAmount = ( CASE WHEN AccountCategoryKind = 1
                                             THEN @CloseAmount
                                             WHEN AccountCategoryKind = 0
                                             THEN $0
                                             ELSE CASE WHEN @CloseAmount > 0
                                                       THEN @CloseAmount
                                                       ELSE $0
                                                  END
                                        END ) ,
                @PUContractCode_tmp = PUContractCode ,
                @BranchID_tmp = BranchID ,
                @AccountObjectCode_tmp = AccountObjectCode ,
                @AccountNumber_tmp = AccountNumber
        WHERE   OrderType <> 2		
        
        
/*Lấy số liệu*/				
        SELECT  RS.*
        FROM    @tblResult RS   
    END

GO