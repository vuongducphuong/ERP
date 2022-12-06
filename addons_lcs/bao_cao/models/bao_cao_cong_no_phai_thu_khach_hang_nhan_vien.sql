SET QUOTED_IDENTIFIER ON;
SET ANSI_NULLS ON;

/*
-- =============================================
-- Author:		vhanh
-- Create date: 15/08/2016
-- Description:	Bán hàng: Lấy số liệu tổng hợp công nợ phải thu theo nhân viên (Clone từ báo cáo Chi tiết công nợ phải thu theo nhân viên và bỏ các thông tin không  cần thiết)
-- =============================================
*/

DECLARE @FromDate DATETIME;
DECLARE @ToDate DATETIME;
DECLARE @BranchID UNIQUEIDENTIFIER; -- Chi nhánh
DECLARE @IncludeDependentBranch BIT; -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE @AccountNumber NVARCHAR(20); -- Số tài khoản   
DECLARE @CurrencyID NVARCHAR(3); -- Loại tiền
DECLARE @ListEmployeeID AS NVARCHAR(MAX); -- Danh sách mã nhân viên   
DECLARE @IsWorkingWithManagementBook BIT; --  Có dùng sổ quản trị hay không?

SET @FromDate = '2018-01-01 00:00:00';
SET @ToDate = '2018-12-31 23:59:59';
SET @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B';
SET @IncludeDependentBranch = 1;
SET @AccountNumber = NULL;
SET @CurrencyID = N'VND';
SET @ListEmployeeID
    = N',09481017-3587-4264-90c0-7af2bb9ba548,8862b15c-82ac-4c32-8567-57dea10d8e18,c884a69a-3b6b-4da3-8ed1-85d7ef56e7f4,17e67feb-d30e-42e2-ab3b-a9c902392591,a3ba20a7-fcae-4537-83f2-f9a7d003c5d7,51ccd3f8-17ae-4798-abbc-c2942527a34f,9a789a94-120c-46a4-b4f6-70d2b069bfd9,585b0efc-80c4-4f4a-8bd7-0f9afa28d6d8,316ff106-5838-4dd8-99c6-080eaf0e60fa,00ad625e-e8fc-4367-951a-39a0de4c057e,a9b7beda-67dc-49b2-bea1-003d56e0de5c,';
SET @IsWorkingWithManagementBook = 0;






BEGIN
    SET NOCOUNT ON;
    /*Lấy quyết định*/
    DECLARE @AccountingSystem INT;
    SELECT TOP 1
           @AccountingSystem = OptionValue
    FROM dbo.SYSDBOption
    WHERE OptionID LIKE N'%AccountingSystem%';

    /*Lấy bảng chi nhánh*/
    CREATE TABLE #Branch
    (
        BranchID UNIQUEIDENTIFIER PRIMARY KEY,
        BranchCode NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS,
        BranchName NVARCHAR(128) COLLATE SQL_Latin1_General_CP1_CI_AS
    );

    INSERT INTO #Branch --TMP_LIST_BRAND
    SELECT FGDBBI.BranchID,
           BranchCode,
           BranchName
    FROM dbo.Func_GetDependentByBranchID(@BranchID, @IncludeDependentBranch) AS FGDBBI;

    /*Lấy danh sách nhân viên*/
    CREATE TABLE #EmployeeID
    (
        EmployeeID UNIQUEIDENTIFIER,
        EmployeeCode NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
        EmployeeName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS
    );

    INSERT INTO #EmployeeID
    SELECT AO.AccountObjectID,   --NHAN_VIEN_ID
           AO.AccountObjectCode, --MA_NHAN_VIEN
           AO.AccountObjectName  --HO_VA_TEN
    FROM dbo.Func_ConvertGUIStringIntoTable(@ListEmployeeID, ',') F --res_partner
        INNER JOIN dbo.AccountObject AO
            ON F.[Value] = AO.AccountObjectID;

    /*Lấy danh sách tài khoản*/
    CREATE TABLE #AccountNumber
    ( --TMP_TAI_KHOAN
        AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
        AccountName NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS,
        AccountNumberPercent NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS,
        AccountCategoryKind INT
    );
    IF @AccountNumber IS NOT NULL --tai_khoan_id
        INSERT INTO #AccountNumber --TMP_TAI_KHOAN
        SELECT A.AccountNumber,       --SO_TAI_KHOAN
               A.AccountName,         --TEN_TAI_KHOAN
               A.AccountNumber + '%', --"SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent",
               A.AccountCategoryKind  --TINH_CHAT
        FROM dbo.Account AS A --danh_muc_he_thong_tai_khoan
        WHERE AccountNumber LIKE @AccountNumber + '%' --"SO_TAI_KHOAN" LIKE tai_khoan_id || '%%' 
        ORDER BY A.AccountNumber, --SO_TAI_KHOAN
                 A.AccountName;   --  TEN_TAI_KHOAN  
    ELSE
        INSERT INTO #AccountNumber --TMP_TAI_KHOAN
        SELECT A.AccountNumber,       --SO_TAI_KHOAN
               A.AccountName,         --TEN_TAI_KHOAN
               A.AccountNumber + '%', --"SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent",
               A.AccountCategoryKind  --TINH_CHAT
        FROM dbo.Account AS A --danh_muc_he_thong_tai_khoan
        WHERE DetailByAccountObject = 1 --CHI_TIET_THEO_DOI_TUONG
              AND AccountObjectType = 1 --DOI_TUONG_SELECTION
              AND IsParent = 0 --LA_TK_TONG_HOP
        ORDER BY A.AccountNumber, --SO_TAI_KHOAN
                 A.AccountName;   --TEN_TAI_KHOAN

    /*1. Tạo bảng tạm #DebtCrossEntry chứa những chứng từ công nợ đã đối trừ được lưu trong bảng liên kết đối trừ*/
    IF OBJECT_ID('tempdb..#DebtCrossEntry') IS NOT NULL
        DROP TABLE #DebtCrossEntry; --TMP_CONG_NO_DOI_TRU
    CREATE TABLE #DebtCrossEntry --TMP_CONG_NO_DOI_TRU
    (
        RefID UNIQUEIDENTIFIER,
        AccountObjectID UNIQUEIDENTIFIER,
        AccountNumber NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
        CurrencyID NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS,
        EmployeeID UNIQUEIDENTIFIER
    );
    INSERT INTO #DebtCrossEntry
    (
        RefID, --
        AccountObjectID,
        AccountNumber,
        CurrencyID,
        EmployeeID
    )
    SELECT DISTINCT
           G.DebtRefID,       --ID_CHUNG_TU
           G.AccountObjectID, --DOI_TUONG_ID
           G.AccountNumber,   --TAI_KHOAN_ID
           G.CurrencyID,      --currency_id
           G.DebtEmployeeID   --
    FROM dbo.GLVoucherCrossEntryDetail G --sale_ex_doi_tru_chi_tiet
        INNER JOIN #AccountNumber AC --TMP_TAI_KHOAN
            ON AC.AccountNumber = G.AccountNumber --AC."SO_TAI_KHOAN" = G."TAI_KHOAN_ID"
        INNER JOIN #Branch B
            ON B.BranchID = G.BranchID
    /*Không lấy số dư đầu kỳ. Với số dư đầu kỳ lấy theo đúng thông tin trên tab chi tiết*/
    WHERE G.DebtRefType NOT IN ( 612, 613, 614 ); --LOAI_CHUNG_TU_CONG_NO

    /*2. Tạo bảng tạm #PayCrossEntry chứa chứng từ thanh toán lấy dữ liệu từ bảng liên kết đối trừ, hàng bản trả lại, hàng bán giảm giá*/
    IF OBJECT_ID('tempdb..#PayCrossEntry') IS NOT NULL
        DROP TABLE #PayCrossEntry; --TMP_CHUNG_TU_THANH_TOAN
    CREATE TABLE #PayCrossEntry --TMP_CHUNG_TU_THANH_TOAN
    (
        CrossEntryID INT PRIMARY KEY IDENTITY(1, 1),
        RefID UNIQUEIDENTIFIER,
        AccountObjectID UNIQUEIDENTIFIER,
        AccountNumber NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
        CurrencyID NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS,
        EmployeeID UNIQUEIDENTIFIER,
        PayAmountOC DECIMAL(22, 8),
        PayAmount DECIMAL(22, 8),
        DebtRefID UNIQUEIDENTIFIER,
        DebtPostedDate DATETIME,
        DebtRefNo NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS,
        DebtInvNo NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS
    );
    INSERT INTO #PayCrossEntry
    (
        RefID,
        AccountObjectID,
        AccountNumber,
        CurrencyID,
        EmployeeID,
        PayAmountOC,
        PayAmount,
        DebtRefID,
        DebtPostedDate,
        DebtRefNo,
        DebtInvNo
    )
    SELECT G.PayRefID,         --ID_CHUNG_TU
           G.AccountObjectID,  --DOI_TUONG_ID
           G.AccountNumber,    --TAI_KHOAN_ID
           G.CurrencyID,       --currency_id
           G.DebtEmployeeID,
           SUM(G.PayAmountOC), --SO_TIEN_THANH_TOAN
                               /*Với đối trừ có chênh lệch thì tính thêm cả số tiền chênh lệch vào*/
           SUM(   CASE
                      WHEN G.CrossType = 0 THEN --LOAI_DOI_TRU
                          G.PayAmount - G.ExchangeDiffAmount --G."SO_TIEN_THANH_TOAN_QUY_DOI" - G."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI" 
                      ELSE
                          G.PayAmount                        --SO_TIEN_THANH_TOAN_QUY_DOI
                  END
              ),
           NULL,
           G.DebtPostedDate,   --NGAY_HACH_TOAN_CONG_NO
           G.DebtRefNo,        --SO_CHUNG_TU_CONG_NO
           G.DebtInvNo         --SO_HOA_DON_CONG_NO
    FROM dbo.GLVoucherCrossEntryDetail G --sale_ex_doi_tru_chi_tiet
        INNER JOIN #AccountNumber AC --TMP_TAI_KHOAN
            ON AC.AccountNumber = G.AccountNumber --AC."SO_TAI_KHOAN" = G."TAI_KHOAN_ID"
        INNER JOIN #Branch B --TMP_LIST_BRAND
            ON B.BranchID = G.BranchID --B."CHI_NHANH_ID" = G."CHI_NHANH_ID"
    GROUP BY G.PayRefID,        --ID_CHUNG_TU
             G.AccountObjectID, --DOI_TUONG_ID
             G.AccountNumber,   --TAI_KHOAN_ID
             G.CurrencyID,      --currency_id
             G.DebtRefNo,       --SO_CHUNG_TU_CONG_NO
             G.DebtEmployeeID,
             G.DebtPostedDate,  --NGAY_HACH_TOAN_CONG_NO
             G.DebtInvNo        --SO_HOA_DON_CONG_NO
    UNION ALL
    /*Lấy hàng bán trả lại*/
    SELECT SARD.RefID,                            --ID_CHUNG_TU
           AL.AccountObjectID,                    --DOI_TUONG_ID
           AL.AccountNumber,                      --MA_TK
           AL.CurrencyID,                         --currency_id
           SAV.EmployeeID,                        --NHAN_VIEN_ID
           SUM(AL.CreditAmountOC) AS PayAmountOC, --SO_TIEN_THANH_TOAN
           SUM(AL.CreditAmount) AS PayAmount,     --SO_TIEN_THANH_TOAN_QUY_DOI
           SAV.RefID,                             --
           SAV.PostedDate,                        --NGAY_HACH_TOAN
           SAV.RefNoFinance,                      --SO_CHUNG_TU
           SAV.InvNo                              --SO_HOA_DON
    FROM dbo.SAReturnDetail SARD --sale_ex_tra_lai_hang_ban_chi_tiet
        INNER JOIN dbo.AccountObjectLedger AL --so_cong_no_chi_tiet
            ON SARD.RefDetailID = AL.RefDetailID --(SARD.id = AL."CHI_TIET_ID" AND AL."CHI_TIET_MODEL"='sale.ex.tra.lai.hang.ban.chi.tiet')
        INNER JOIN dbo.SAVoucher SAV --sale_document
            ON SAV.RefID = SARD.SAVoucherRefID --SAV."id" = SARD."SO_CHUNG_TU_ID"
        INNER JOIN #AccountNumber AC --TMP_TAI_KHOAN
            ON AC.AccountNumber = AL.AccountNumber -- AC ON AC."SO_TAI_KHOAN" = AL."MA_TK"
        INNER JOIN #Branch B --TMP_LIST_BRAND
            ON B.BranchID = AL.BranchID --B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
    WHERE SARD.SAVoucherRefID IS NOT NULL --SO_CHUNG_TU_ID
    GROUP BY SARD.RefID,         --TRA_LAI_HANG_BAN_ID
             AL.AccountObjectID, --DOI_TUONG_ID
             AL.AccountNumber,   --MA_TK
             AL.CurrencyID,      --currency_id
             SAV.EmployeeID,     --NHAN_VIEN_ID
             SAV.RefID,          --
             SAV.PostedDate,     --NGAY_HACH_TOAN
             SAV.RefNoFinance,   --SO_CHUNG_TU
             SAV.InvNo           --SO_HOA_DON
    UNION ALL
    /*Lấy hàng bán giảm giá*/
    SELECT SARD.RefID,                            --GIAM_GIA_HANG_BAN_ID
           AL.AccountObjectID,                    --DOI_TUONG_ID
           AL.AccountNumber,                      --MA_TK
           AL.CurrencyID,                         --currency_id
           SAV.EmployeeID,                        --NHAN_VIEN_ID
           SUM(AL.CreditAmountOC) AS PayAmountOC, --SO_TIEN_THANH_TOAN
           SUM(AL.CreditAmount) AS PayAmount,     --SO_TIEN_THANH_TOAN_QUY_DOI
           SAV.RefID,
           SAV.PostedDate,                        --NGAY_HACH_TOAN
           SAV.RefNoFinance,                      --SO_CHUNG_TU
           SAV.InvNo                              --SO_HOA_DON
    FROM dbo.SADiscountDetail SARD --sale_ex_chi_tiet_giam_gia_hang_ban
        INNER JOIN dbo.AccountObjectLedger AL --so_cong_no_chi_tiet
            ON SARD.RefDetailID = AL.RefDetailID --
        INNER JOIN dbo.SAVoucher SAV --sale_document
            ON SAV.RefID = SARD.SAVoucherRefID --SAV."id" = SARD."SO_CHUNG_TU_ID"
        INNER JOIN #AccountNumber AC --TMP_TAI_KHOAN
            ON AC.AccountNumber = AL.AccountNumber --AC."SO_TAI_KHOAN" = AL."MA_TK"
        INNER JOIN #Branch B --TMP_LIST_BRAND
            ON B.BranchID = AL.BranchID --B."CHI_NHANH_ID" = AL."CHI_NHANH_ID"
    WHERE SARD.SAVoucherRefID IS NOT NULL --CHUNG_TU_BAN_HANG_ID
    GROUP BY SARD.RefID,         --GIAM_GIA_HANG_BAN_ID
             AL.AccountObjectID, --DOI_TUONG_ID
             AL.AccountNumber,   --MA_TK
             AL.CurrencyID,      --currency_id
             SAV.EmployeeID,     --NHAN_VIEN_ID
             SAV.RefID,
             SAV.PostedDate,     --NGAY_HACH_TOAN
             SAV.RefNoFinance,   --SO_CHUNG_TU
             SAV.InvNo;          --SO_HOA_DON


    /*Tạo bảng chứa kết quả*/
    CREATE TABLE #Temp
    (
		RowNum INT IDENTITY(1, 1) ,--vũ thêm để so sánh thứ tự
        EmployeeID UNIQUEIDENTIFIER,
        AccountObjectID UNIQUEIDENTIFIER,
        RefID UNIQUEIDENTIFIER,
        RefType INT,
        PostedDate DATETIME,
        RefDate DATETIME,
        RefNo NVARCHAR(22) COLLATE SQL_Latin1_General_CP1_CI_AS,
        InvDate DATETIME,
        InvNo NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS,
        RefDetailID UNIQUEIDENTIFIER,
        DebtRefID UNIQUEIDENTIFIER,
        LedgerID INT,
        AccountNumber NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS,
        CurrencyID NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS,
        DebitAmountOC MONEY,
        DebitAmount MONEY,
        CreditAmountOC MONEY,
        CreditAmount MONEY,
        IsCrossRow BIT
            DEFAULT (0),
        CrossAmount MONEY
            DEFAULT (0),
        CrossAmountOC MONEY
            DEFAULT (0),
        OrderType INT
    );

    --BTAnh - 05.08.2016: Bổ sung Index để tăng tốc độ khi sử dụng trong cursor
    CREATE CLUSTERED INDEX [IX_Clusted_Temp_Composite]
    ON #Temp (
                 RefID ASC,
                 AccountObjectID ASC,
                 AccountNumber ASC,
                 CurrencyID ASC
             )
    WITH (STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF,
          ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON
         )
    ON [PRIMARY];


    /*3 - 4. Lấy dữ liệu vào bảng tạm và lấy phần đối trừ*/
    INSERT INTO #Temp --TMP_KET_QUA
    (
        EmployeeID,      --NHAN_VIEN_ID
        AccountObjectID, --DOI_TUONG_ID
        RefID,           --ID_CHUNG_TU
        RefType,         --LOAI_CHUNG_TU
        PostedDate,      --NGAY_HACH_TOAN
        RefDate,         --NGAY_CHUNG_TU
        RefNo,           --SO_CHUNG_TU
        InvDate,         --NGAY_HOA_DON
        InvNo,           --SO_HOA_DON
        RefDetailID,
        DebtRefID,
        LedgerID,
        AccountNumber,   --MA_TK
        CurrencyID,      --currency_id
        DebitAmountOC,   --GHI_NO_NGUYEN_TE
        DebitAmount,     --GHI_NO
        CreditAmountOC,  --GHI_CO_NGUYEN_TE
        CreditAmount,    --GHI_CO
        OrderType        --OrderType
    )
    SELECT T.*
    FROM
    (
        SELECT ISNULL(GD.EmployeeID, Al.EmployeeID) AS EmployeeID,
               Al.AccountObjectID, --DOI_TUONG_ID
               Al.RefID,           --ID_CHUNG_TU
               Al.RefType,         --LOAI_CHUNG_TU
               Al.PostedDate,      --NGAY_HACH_TOAN
               Al.RefDate,         --NGAY_CHUNG_TU
               Al.RefNo,           --SO_CHUNG_TU
               Al.InvDate,         --NGAY_HOA_DON
               Al.InvNo,           --SO_HOA_DON
               Al.RefDetailID,
               SA.SAVoucherRefID AS DebtRefID,
               Al.AccountObjectLedgerID AS LedgerID,
               Al.AccountNumber,   --MA_TK
               Al.CurrencyID,      --currency_id
               Al.DebitAmountOC,   --GHI_NO_NGUYEN_TE
               Al.DebitAmount,     --GHI_NO
               Al.CreditAmountOC,  --GHI_CO_NGUYEN_TE
               Al.CreditAmount,    --GHI_CO
               1 AS OrderType      --OrderType
        FROM AccountObjectLedger Al --so_cong_no_chi_tiet
            INNER JOIN #Branch B--TMP_LIST_BRAND
                ON B.BranchID = Al.BranchID--B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
            INNER JOIN #AccountNumber AC --TMP_TAI_KHOAN
                ON AC.AccountNumber = Al.AccountNumber --AC."SO_TAI_KHOAN" = Al."MA_TK"
            LEFT JOIN #DebtCrossEntry GD --TMP_CONG_NO_DOI_TRU
                ON Al.RefID = GD.RefID -- AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU"
                   AND Al.AccountNumber = GD.AccountNumber --AL."MA_TK" = GD."TAI_KHOAN_ID"
                   AND Al.AccountObjectID = GD.AccountObjectID --AL."DOI_TUONG_ID" = GD."DOI_TUONG_ID"
                   AND Al.CurrencyID = GD.CurrencyID --AL."currency_id" = GD."currency_id"
            LEFT JOIN
            (
                SELECT SAR.RefDetailID,--id
                       SAR.SAVoucherRefID --CHUNG_TU_BAN_HANG_ID
                FROM dbo.SAReturnDetail SAR --sale_ex_tra_lai_hang_ban_chi_tiet
                WHERE SAR.SAVoucherRefID IS NOT NULL --CHUNG_TU_BAN_HANG_ID
                UNION ALL
                SELECT SAD.RefDetailID,--
                       SAD.SAVoucherRefID--CHUNG_TU_BAN_HANG_ID
                FROM dbo.SADiscountDetail SAD --sale_ex_chi_tiet_giam_gia_hang_ban
                WHERE SAD.SAVoucherRefID IS NOT NULL--CHUNG_TU_BAN_HANG_ID
            ) SA
                ON Al.RefDetailID = SA.RefDetailID
        WHERE (Al.PostedDate --NGAY_HACH_TOAN
              BETWEEN @FromDate AND @ToDate --tu_ngay AND den_ngay
              )
              AND Al.IsPostToManagementBook = @IsWorkingWithManagementBook
              AND
              (
                  Al.CurrencyID = @CurrencyID --AL."currency_id" = loai_tien_id
                  OR @CurrencyID IS NULL--loai_tien_id
              )
              AND
              (
                  Al.DebitAmountOC <> 0--GHI_NO_NGUYEN_TE
                  OR Al.DebitAmount <> 0 --GHI_NO
                  OR Al.CreditAmountOC <> 0 --GHI_CO_NGUYEN_TE
                  OR Al.CreditAmount <> 0 --GHI_CO
              )
        UNION ALL
        /*Số dư đầu kỳ*/
        SELECT ISNULL(GD.EmployeeID, Al.EmployeeID) AS EmployeeID,--NHAN_VIEN_ID
               Al.AccountObjectID,--DOI_TUONG_ID
               Al.RefID,--ID_CHUNG_TU
               NULL AS RefType, --LOAI_CHUNG_TU
               NULL AS PostedDate,--NGAY_HACH_TOAN
               NULL AS RefDate, --NGAY_CHUNG_TU
               NULL AS RefNo, --SO_CHUNG_TU
               NULL AS InvDate, --NGAY_HOA_DON
               NULL AS InvNo, --SO_HOA_DON
               Al.RefDetailID,
               SA.SAVoucherRefID AS DebtRefID,
               Al.AccountObjectLedgerID AS LedgerID,
               Al.AccountNumber, --MA_TK
               Al.CurrencyID,--currency_id
               Al.DebitAmountOC,--GHI_NO_NGUYEN_TE
               Al.DebitAmount,--GHI_NO
               Al.CreditAmountOC, --GHI_CO_NGUYEN_TE
               Al.CreditAmount, --GHI_CO
               0 AS OrderType --OrderType
        FROM AccountObjectLedger Al --so_cong_no_chi_tiet
            INNER JOIN #Branch B --TMP_LIST_BRAND
                ON B.BranchID = Al.BranchID --B."CHI_NHANH_ID" = Al."CHI_NHANH_ID"
            INNER JOIN #AccountNumber AC --TMP_TAI_KHOAN
                ON AC.AccountNumber = Al.AccountNumber --AC."SO_TAI_KHOAN" = Al."MA_TK"
            LEFT JOIN #DebtCrossEntry GD --TMP_CONG_NO_DOI_TRU
                ON Al.RefID = GD.RefID --AL."ID_CHUNG_TU" = GD."ID_CHUNG_TU" 
                   AND Al.AccountNumber = GD.AccountNumber --AL."MA_TK" = GD."TAI_KHOAN_ID"
                   AND Al.AccountObjectID = GD.AccountObjectID --AL."DOI_TUONG_ID" = GD."DOI_TUONG_ID"
                   AND Al.CurrencyID = GD.CurrencyID --AL."currency_id" = GD."currency_id"
            LEFT JOIN
            (
                SELECT SAR.RefDetailID, --id
                       SAR.SAVoucherRefID --CHUNG_TU_BAN_HANG_ID
                FROM dbo.SAReturnDetail SAR --sale_ex_tra_lai_hang_ban_chi_tiet
                WHERE SAR.SAVoucherRefID IS NOT NULL --CHUNG_TU_BAN_HANG_ID
                UNION ALL
                SELECT SAD.RefDetailID,--id --
                       SAD.SAVoucherRefID--CHUNG_TU_BAN_HANG_ID
                FROM dbo.SADiscountDetail SAD --sale_ex_chi_tiet_giam_gia_hang_ban
                WHERE SAD.SAVoucherRefID IS NOT NULL --CHUNG_TU_BAN_HANG_ID
            ) SA
                ON Al.RefDetailID = SA.RefDetailID 
        WHERE Al.PostedDate < @FromDate--AL."NGAY_HACH_TOAN" < tu_ngay 
              AND Al.IsPostToManagementBook = @IsWorkingWithManagementBook
              AND
              (
                  Al.CurrencyID = @CurrencyID --AL."currency_id" = loai_tien_id 
                  OR @CurrencyID IS NULL --loai_tien_id
              )
              AND
              (
                  Al.DebitAmountOC <> 0 --GHI_NO_NGUYEN_TE
                  OR Al.DebitAmount <> 0 --GHI_NO
                  OR Al.CreditAmountOC <> 0--GHI_CO_NGUYEN_TE
                  OR Al.CreditAmount <> 0 --GHI_CO
              )
    ) T
    ORDER BY 
	T.PostedDate,
	T.RefNo,
	T.InvNo,
	 T.AccountNumber,--MA_TK
	  T.CreditAmount,
	  T.DebitAmount,
	 
	T.RefID, --ID_CHUNG_TU
             T.AccountObjectID, --DOI_TUONG_ID
             T.CurrencyID, --currency_id
            
             T.RefDetailID;

    /*5. Tính toán cộng đuổi cho chứng từ thanh toán để tính số tiền đã đối trừ và số tiền còn lại*/
    DECLARE @PayRefID UNIQUEIDENTIFIER,
            @PayAccountObject UNIQUEIDENTIFIER,
            @PayEmployee UNIQUEIDENTIFIER,
            @PayAccountNumber NVARCHAR(25),
            @PayCurrency NVARCHAR(25),
            @PayAmount MONEY,
            @PayAmountOC MONEY,
            @DebtRefID UNIQUEIDENTIFIER
			;

    DECLARE cur CURSOR FAST_FORWARD READ_ONLY FOR
         SELECT 			
		   GP.RefID,
           GP.AccountObjectID,
           GP.EmployeeID,
           GP.AccountNumber,
           GP.CurrencyID,
           GP.PayAmount,
           GP.PayAmountOC,
           GP.DebtRefID
		  
    FROM #PayCrossEntry GP
    WHERE GP.RefID IN
          (
              SELECT T.RefID
              FROM #Temp T
              WHERE T.CreditAmountOC > 0
                    OR T.CreditAmount > 0
          )
    ORDER BY GP.DebtPostedDate,
             GP.DebtRefNo,
             GP.DebtInvNo,
			  GP.PayAmount
			 ;
    OPEN cur;
    FETCH NEXT FROM cur
    INTO @PayRefID,
         @PayAccountObject,
         @PayEmployee,
         @PayAccountNumber,
         @PayCurrency,
         @PayAmount,
         @PayAmountOC,
         @DebtRefID
		
		 ;
    WHILE (@@FETCH_STATUS = 0)
    BEGIN
        DECLARE @LedgerID INT,
                @CrossAmountOC MONEY,
                @CrossAmount MONEY,
                @OldRemainAmountOC MONEY,
                @OldRemainAmount MONEY,
                @RemainAmountOC MONEY,
                @RemainAmount MONEY;
        SET @LedgerID = NULL;
        SET @CrossAmountOC = 0;
        SET @CrossAmount = 0;
        SET @OldRemainAmountOC = 0;
        SET @OldRemainAmount = 0;
        SET @RemainAmountOC = 0;
        SET @RemainAmount = 0;

        UPDATE #Temp
        SET @OldRemainAmount = (CASE
                                    WHEN ISNULL(@LedgerID, 0) <> LedgerID THEN
                                        CreditAmount
                                    ELSE
                                        @RemainAmount
                                END
                               ),
            @OldRemainAmountOC = (CASE
                                      WHEN ISNULL(@LedgerID, 0) <> LedgerID THEN
                                          CreditAmountOC
                                      ELSE
                                          @RemainAmountOC
                                  END
                                 ),
            @CrossAmount = (CASE
                                WHEN @OldRemainAmount < @PayAmount THEN
                                    @OldRemainAmount
                                ELSE
                                    @PayAmount
                            END
                           ),
            @CrossAmountOC = (CASE
                                  WHEN @OldRemainAmountOC < @PayAmountOC THEN
                                      @OldRemainAmountOC
                                  ELSE
                                      @PayAmountOC
                              END
                             ),
            @RemainAmount = @OldRemainAmount - @CrossAmount,
            @RemainAmountOC = @OldRemainAmountOC - @CrossAmountOC,
            CrossAmount = @CrossAmount,
            CrossAmountOC = @CrossAmountOC,
            CreditAmount = @RemainAmount,
            CreditAmountOC = @RemainAmountOC,
            @PayAmount = @PayAmount - @CrossAmount,
            @PayAmountOC = @PayAmountOC - @CrossAmountOC,
            @LedgerID = LedgerID
        WHERE RefID = @PayRefID
              AND AccountObjectID = @PayAccountObject
              AND AccountNumber = @PayAccountNumber
              AND CurrencyID = @PayCurrency
              AND
              (
                  (
                      DebtRefID IS NULL
                      AND @DebtRefID IS NULL
                  )
                  OR (DebtRefID = @DebtRefID)
              )
              AND IsCrossRow = 0;



    --    /*Nếu số tiền đối trừ > 0 và số tiền còn lại (CreditAmount = 0) thì update chuyển luôn dòng đó sang thành dòng mới*/
        UPDATE #Temp
        SET CreditAmount = CrossAmount,
            CreditAmountOC = CrossAmountOC,
            CrossAmount = 0,
            CrossAmountOC = 0,
            EmployeeID = ISNULL(@PayEmployee, EmployeeID),
            IsCrossRow = 1
        WHERE RefID = @PayRefID
              AND AccountObjectID = @PayAccountObject
              AND AccountNumber = @PayAccountNumber
              AND CurrencyID = @PayCurrency
              AND
              (
                  (
                      DebtRefID IS NULL
                      AND @DebtRefID IS NULL
                  )
                  OR (DebtRefID = @DebtRefID)
              )
              AND IsCrossRow = 0
              AND CreditAmountOC = 0
              AND CreditAmount = 0
              AND
              (
                  CrossAmountOC <> 0
                  OR CrossAmount <> 0
              );
    --    --/*Nếu số tiền đối trừ > 0 và số tiền còn lại (CreditAmount > 0) thì tách ra 1 dòng mới*/
        INSERT INTO #Temp
        (
            EmployeeID,
            AccountObjectID,
            RefID,
            RefType,
            PostedDate,
            RefDate,
            RefNo,
            InvDate,
            InvNo,
            RefDetailID,
            LedgerID,
            AccountNumber,
            CurrencyID,
            DebitAmountOC,
            DebitAmount,
            CreditAmountOC,
            CreditAmount,
            IsCrossRow,
            OrderType
        )
        SELECT ISNULL(@PayEmployee, EmployeeID) AS EmployeeID,
               AccountObjectID,
               RefID,
               RefType,
               PostedDate,
               RefDate,
               RefNo,
               InvDate,
               InvNo,
               RefDetailID,
               LedgerID,
               AccountNumber,
               CurrencyID,
               DebitAmountOC,
               DebitAmount,
               CrossAmountOC,
               CrossAmount,
               1 AS IsCrossRow,
               OrderType
        FROM #Temp
        WHERE RefID = @PayRefID
              AND AccountObjectID = @PayAccountObject
              AND AccountNumber = @PayAccountNumber
              AND CurrencyID = @PayCurrency
              AND
              (
                  (
                      DebtRefID IS NULL
                      AND @DebtRefID IS NULL
                  )
                  OR (DebtRefID = @DebtRefID)
              )
              AND IsCrossRow = 0
              AND
              (
                  CreditAmountOC <> 0
                  OR CreditAmount <> 0
              )
              AND
              (
                  CrossAmountOC <> 0
                  OR CrossAmount <> 0
              );
    --    /*Nếu số tiền đối trừ = 0 thì không làm gì. Reset số tiền đối trừ*/
        UPDATE #Temp
        SET CrossAmount = 0,
            CrossAmountOC = 0
        WHERE RefID = @PayRefID
              AND AccountObjectID = @PayAccountObject
              AND AccountNumber = @PayAccountNumber
              AND CurrencyID = @PayCurrency
              AND
              (
                  (
                      DebtRefID IS NULL
                      AND @DebtRefID IS NULL
                  )
                  OR (DebtRefID = @DebtRefID)
              )
              AND IsCrossRow = 0;

        FETCH NEXT FROM cur
        INTO @PayRefID,
             @PayAccountObject,
             @PayEmployee,
             @PayAccountNumber,
             @PayCurrency,
             @PayAmount,
             @PayAmountOC,
             @DebtRefID
			 
			 ;
    END;
    CLOSE cur;
    DEALLOCATE cur;

  
    /*6. Tính tổng lấy được số dư đầu kỳ, phát sinh và số dư cuối kỳ*/
    SELECT ROW_NUMBER() OVER (ORDER BY EmployeeCode) AS RowNum,
		
           R.EmployeeID, --NHAN_VIEN_ID
           E.EmployeeCode, --MA_NHAN_VIEN
           E.EmployeeName, --HO_VA_TEN
           R.AccountNumber,--MA_TK
           AC.AccountCategoryKind,--TINH_CHAT
           /*Sửa bug 114938: Lỗi số dư đầu kỳ đang hiển thị không đúng trường hợp có cả PS Nợ và Có*/
           (CASE
                WHEN
                (
                    AccountCategoryKind = 0--TINH_CHAT
                    OR
                    (
                        AccountCategoryKind = 2--TINH_CHAT
                        AND SUM(   CASE
                                       WHEN R.OrderType = 0 THEN--OrderType
                                   (DebitAmount - CreditAmount) --"GHI_NO" - "GHI_CO"
                                       ELSE
                                           0
                                   END
                               ) >= 0
                    )
                ) THEN
                    SUM(   CASE
                               WHEN R.OrderType = 0 THEN
                           (DebitAmount - CreditAmount)
                               ELSE
                                   0
                           END
                       )
                ELSE
                    0
            END
           ) AS OpenningDebitAmount, --GHI_NO_DAU_KY
           (CASE
                WHEN
                (
                    AccountCategoryKind = 0 --TINH_CHAT
                    OR
                    (
                        AccountCategoryKind = 2--TINH_CHAT
                        AND SUM(   CASE
                                       WHEN R.OrderType = 0 THEN --OrderType
                                   (DebitAmountOC - CreditAmountOC)  --"GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                                       ELSE
                                           0
                                   END
                               ) >= 0
                    )
                ) THEN
                    SUM(   CASE
                               WHEN R.OrderType = 0 THEN  --OrderType
                           (DebitAmountOC - CreditAmountOC)--"GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                               ELSE
                                   0
                           END
                       )
                ELSE
                    0
            END
           ) AS OpenningDebitAmountOC, --GHI_NO_NGUYEN_TE_DAU_KY
           (CASE
                WHEN
                (
                    AccountCategoryKind = 1 --TINH_CHAT
                    OR
                    (
                        AccountCategoryKind = 2 --TINH_CHAT
                        AND SUM(   CASE
                                       WHEN R.OrderType = 0 THEN
                                   (CreditAmount - DebitAmount) --"GHI_CO" - "GHI_NO"
                                       ELSE
                                           0
                                   END
                               ) >= 0
                    )
                ) THEN
                    SUM(   CASE
                               WHEN R.OrderType = 0 THEN
                           (CreditAmount - DebitAmount) --"GHI_CO" - "GHI_NO"
                               ELSE
                                   0
                           END
                       )
                ELSE
                    0
            END
           ) AS OpenningCreditAmount, --GHI_CO_DAU_KY
           (CASE
                WHEN
                (
                    AccountCategoryKind = 1 --TINH_CHAT
                    OR
                    (
                        AccountCategoryKind = 2 --TINH_CHAT
                        AND SUM(   CASE
                                       WHEN R.OrderType = 0 THEN
                                   (CreditAmountOC - DebitAmountOC) --"GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE"
                                       ELSE
                                           0
                                   END
                               ) >= 0
                    )
                ) THEN
                    SUM(   CASE
                               WHEN R.OrderType = 0 THEN --OrderType
                           (CreditAmountOC - DebitAmountOC) ----"GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE"
                               ELSE
                                   0
                           END
                       )
                ELSE
                    0
            END
           ) AS OpenningCreditAmountOC,--GHI_CO_NGUYEN_TE_DAU_KY
           SUM(   CASE
                      WHEN R.OrderType = 1 THEN --OrderType
                          ISNULL(R.DebitAmount, 0) --GHI_NO
                      ELSE
                          0
                  END
              ) AS DebitAmount, --GHI_NO
           SUM(   CASE
                      WHEN R.OrderType = 1 THEN
                          ISNULL(R.DebitAmountOC, 0) --GHI_NO_NGUYEN_TE
                      ELSE
                          0
                  END
              ) AS DebitAmountOC,--GHI_NO_NGUYEN_TE
           SUM(   CASE
                      WHEN R.OrderType = 1 THEN
                          ISNULL(R.CreditAmount, 0) --GHI_CO
                      ELSE
                          0
                  END
              ) AS CreditAmount,--GHI_CO
           SUM(   CASE
                      WHEN R.OrderType = 1 THEN
                          ISNULL(R.CreditAmountOC, 0) --GHI_CO_NGUYEN_TE
                      ELSE
                          0
                  END
              ) AS CreditAmountOC, --GHI_CO_NGUYEN_TE
           (CASE
                WHEN AccountCategoryKind = 0
                     OR
                     (
                         AccountCategoryKind = 2
                         AND SUM(DebitAmount - CreditAmount) >= 0 --"GHI_NO" - "GHI_CO"
                     ) THEN
                    SUM(DebitAmount - CreditAmount) --"GHI_NO" - "GHI_CO"
                ELSE
                    0
            END
           ) AS CloseDebitAmount,--DU_NO_CUOI_KY
           (CASE
                WHEN AccountCategoryKind = 0
                     OR
                     (
                         AccountCategoryKind = 2
                         AND SUM(DebitAmountOC - CreditAmountOC) >= 0 --"GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                     ) THEN
                    SUM(DebitAmountOC - CreditAmountOC)--"GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                ELSE
                    0
            END
           ) AS CloseDebitAmountOC, --DU_NO_NGUYEN_TE_CUOI_KY
           (CASE
                WHEN AccountCategoryKind = 1
                     OR
                     (
                         AccountCategoryKind = 2
                         AND SUM(CreditAmount - DebitAmount) >= 0 --"GHI_CO" - "GHI_NO"
                     ) THEN
                    SUM(CreditAmount - DebitAmount)--"GHI_CO" - "GHI_NO"
                ELSE
                    0
            END
           ) AS CloseCreditAmount, --DU_CO_CUOI_KY
           (CASE
                WHEN AccountCategoryKind = 1
                     OR
                     (
                         AccountCategoryKind = 2
                         AND SUM(CreditAmountOC - DebitAmountOC) >= 0--"GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE"
                     ) THEN
                    SUM(CreditAmountOC - DebitAmountOC)--"GHI_CO_NGUYEN_TE" - "GHI_NO_NGUYEN_TE"
                ELSE
                    0
            END
           ) AS CloseCreditAmountOC --DU_CO_NGUYEN_TE_CUOI_KY
    FROM #Temp R --TMP_KET_QUA
        INNER JOIN #EmployeeID E --DS_NHAN_VIEN
            ON E.EmployeeID = R.EmployeeID --E."NHAN_VIEN_ID" = R."NHAN_VIEN_ID"
        INNER JOIN dbo.Account AC --danh_muc_he_thong_tai_khoan
            ON AC.AccountNumber = R.AccountNumber--AC."id" = R."MA_TK"
			--WHERE E.EmployeeCode ='HNMAI'
    GROUP BY R.EmployeeID,--NHAN_VIEN_ID
             E.EmployeeCode,--MA_NHAN_VIEN
             E.EmployeeName,--HO_VA_TEN
             R.AccountNumber, --MA_TK
             AC.AccountCategoryKind --TINH_CHAT
		
			 
    HAVING SUM(   CASE
                      WHEN R.OrderType = 0 THEN --OrderType
                  (DebitAmount - CreditAmount)--"GHI_NO" - "GHI_CO"
                      ELSE
                          0
                  END
              ) <> 0
           OR SUM(   CASE
                         WHEN R.OrderType = 0 THEN
                     (DebitAmountOC - CreditAmountOC)--"GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE"
                         ELSE
                             0
                     END
                 ) <> 0
           OR SUM(   CASE
                         WHEN R.OrderType = 1 THEN
                             ISNULL(R.DebitAmount, 0)--GHI_NO
                         ELSE
                             0
                     END
                 ) <> 0
           OR SUM(   CASE
                         WHEN R.OrderType = 1 THEN
                             ISNULL(R.DebitAmountOC, 0)--GHI_NO_NGUYEN_TE
                         ELSE
                             0
                     END
                 ) <> 0
           OR SUM(   CASE
                         WHEN R.OrderType = 1 THEN
                             ISNULL(R.CreditAmount, 0)--GHI_CO
                         ELSE
                             0
                     END
                 ) <> 0
           OR SUM(   CASE
                         WHEN R.OrderType = 1 THEN
                             ISNULL(R.CreditAmountOC, 0)--GHI_CO_NGUYEN_TE
                         ELSE
                             0
                     END
                 ) <> 0
    ORDER BY E.EmployeeCode;

  


   --SELECT * FROM #Temp
   

	DROP TABLE #Branch
	DROP TABLE #EmployeeID
	DROP TABLE #AccountNumber
	DROP TABLE #Temp
END 



