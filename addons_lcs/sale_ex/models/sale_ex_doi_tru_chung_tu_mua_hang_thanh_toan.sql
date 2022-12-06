SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
-- =============================================
-- Author:		vntuan
-- Create date: 14.10.2014
-- Description:	Store lấy dữ liệu cho chi tiết đối trừ mua hàng (chứng từ thanh toán)
/*Roll back by hoant*/
--NVTOAN modify 22/04/2017 thực hiện CR 34929 - Lấy bổ sung thông tin nhân viên
-- =============================================

DECLARE				@AccountObjectID UNIQUEIDENTIFIER 
DECLARE				@AccountNumber NVARCHAR(25) 
DECLARE				@CurrencyID NVARCHAR(3) 
DECLARE				@BranchID UNIQUEIDENTIFIER 
DECLARE				@IsWorkingManagementBook BIT 
DECLARE				@ToDate DATETIME


SET			@AccountObjectID= NULL
SET			@AccountNumber=N'331'
SET			@CurrencyID=N'VND'
SET			@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET			@IsWorkingManagementBook=0
SET			@ToDate='2019-05-25 00:00:00'

    BEGIN
        DECLARE @AccountingSystem NVARCHAR(MAX)
        SELECT TOP 1
                @AccountingSystem = ISNULL(OptionValue, '')
        FROM    SYSDBOption
        WHERE   OptionID LIKE N'%AccountingSystem%' 
        DECLARE @Date AS DATETIME
        SET @Date = GETDATE()
	 
        SELECT  AL.RefID ,
                CAST(AL.RefType AS VARCHAR(50)) AS RefType,
                AL.RefTypeName ,
                AL.RefDate ,
                AL.PostedDate ,
                AL.RefNo ,
                ISNULL(AL.InvNo, '') AS InvNo ,
                AL.[Description] ,
                AL.ExchangeRate AS ExchangeRate ,
                ISNULL(GV.ExchangeRate, 0) AS RevaluationExchangeRate ,
                SUM(AL.AmountOC) AS AmountOC ,
                SUM(AL.Amount) AS Amount ,
                SUM(AL.ReceiptAmountOC) AS ReceiptAmountOC ,
                SUM(AL.ReceiptAmount) AS ReceiptAmount ,
                CAST(0 AS DECIMAL) AS CrossEntryAmountOC ,
                CAST(0 AS DECIMAL) AS CrossEntryAmount ,
                AL.AccountObjectID ,
                AL.EmployeeID , --NVTOAN modify 13/04/2017 thực hiện CR 34929
                E.AccountObjectCode AS EmployeeCode ,--NVTOAN modify 22/04/2017 thực hiện CR 34929 
                E.AccountObjectName AS EmployeeName --NVTOAN modify 13/04/2017 thực hiện CR 34929 
        FROM    ( SELECT    OPNTemp.RefID ,
                            OPNTemp.RefType ,
                            OPNTemp.RefTypeName ,
                            OPNTemp.RefDate ,
                            OPNTemp.PostedDate ,
                            OPNTemp.RefNo ,
                            OPNTemp.InvNo ,
                            OPNTemp.[Description] ,
                            OPNTemp.ExchangeRate ,
                            OPNTemp.AmountOC ,
                            OPNTemp.Amount ,
                            OPNTemp.ReceiptAmountOC - ISNULL(SUM(GL.AmountOC),
                                                             0) AS ReceiptAmountOC ,
                            OPNTemp.ReceiptAmount - ISNULL(SUM(GL.Amount), 0) AS ReceiptAmount ,
                            OPNTemp.AccountObjectID ,
                            OPNTemp.AccountNumber ,
                            OPNTemp.EmployeeID--NVTOAN modify 13/04/2017 thực hiện CR 34929 
                  FROM      ( SELECT    OPN.RefID ,
                                        OPN.RefType ,
                                        RT.RefTypeName ,
                                        ( CASE WHEN OPI.RefID IS NOT NULL
                                                    AND OPI.PayAmountOC <> 0
                                               THEN OPI.InvDate
                                               ELSE OPN.PostedDate
                                          END ) AS RefDate ,
                                        OPN.PostedDate ,
                                        ( CASE WHEN OPI.RefID IS NOT NULL
                                                    AND OPI.PayAmountOC <> 0
                                               THEN OPI.InvNo
                                               ELSE N'OPN'
                                          END ) AS RefNo ,
                                        ISNULL(OPI.InvNo, '') AS InvNo ,
                                        SPACE(0) AS [Description] ,
                                        ( CASE WHEN OPI.RefID IS NOT NULL
                                               THEN ISNULL(OPI.ExchangeRate, 1)
                                               ELSE ISNULL(OPN.ExchangeRate, 1)
                                          END ) AS ExchangeRate ,
                                        SUM(CASE WHEN OPI.RefID IS NOT NULL
                                                 THEN ISNULL(OPI.PayAmountOC,
                                                             0)
                                                 ELSE ISNULL(OPN.DebitAmountOC,
                                                             0)
                                                      - ISNULL(OPN.CreditAmountOC,
                                                              0)
                                            END) AS AmountOC ,
                                        SUM(CASE WHEN OPI.RefID IS NOT NULL
                                                 THEN ISNULL(OPI.PayAmount, 0)
                                                 ELSE ISNULL(OPN.DebitAmount,
                                                             0)
                                                      - ISNULL(OPN.CreditAmount,
                                                              0)
                                            END) AS Amount ,
                                        SUM(CASE WHEN OPI.RefID IS NOT NULL
                                                 THEN ISNULL(OPI.PayAmountOC,
                                                             0)
                                                 ELSE ISNULL(OPN.DebitAmountOC,
                                                             0)
                                                      - ISNULL(OPN.CreditAmountOC,
                                                              0)
                                            END) AS ReceiptAmountOC ,
                                        SUM(CASE WHEN OPI.RefID IS NOT NULL
                                                 THEN ISNULL(OPI.PayAmount, 0)
                                                 ELSE ISNULL(OPN.DebitAmount,
                                                             0)
                                                      - ISNULL(OPN.CreditAmount,
                                                              0)
                                            END) AS ReceiptAmount ,
                                        @AccountObjectID AS AccountObjectID ,
                                        OPN.AccountNumber ,
                                        1 AS DetailByInvNo ,
                                        OPID2.EmployeeID --NVTOAN add 13/04/2017 thực hiện CR 34929
                              FROM      OpeningAccountEntry AS OPN
                                        INNER JOIN SYSRefType RT ON RT.RefType = OPN.RefType
                                        LEFT JOIN OpeningAccountEntryDetailInvoice OPI ON OPI.RefID = OPN.RefID
                                        --NVTOAN add 13/04/2017 thực hiện CR 34929
                                        LEFT JOIN ( SELECT  OAEDI.RefID ,
                                                            ISNULL(OAEDI.InvDate,
                                                              @Date) AS InvDate ,
                                                            ISNULL(OAEDI.InvNo,
                                                              '') AS InvNo ,
                                                            ISNULL(OAEDI.ExchangeRate,
                                                              0) AS ExchangeRate ,
                                                            OAEDI.EmployeeID ,
                                                            ROW_NUMBER() OVER ( PARTITION BY OAEDI.RefID,
                                                              ISNULL(OAEDI.InvDate,
                                                              @Date),
                                                              ISNULL(OAEDI.InvNo,
                                                              ''),
                                                              ISNULL(OAEDI.ExchangeRate,
                                                              0) ORDER BY OAEDI.SortOrder ) AS RowNumber
                                                    FROM    dbo.OpeningAccountEntryDetailInvoice
                                                            AS OAEDI
                                                    WHERE   OAEDI.EmployeeID IS NOT NULL
                                                  ) AS OPID2 ON OPN.RefID = OPID2.RefID
                                                              AND OPID2.RowNumber = 1
                                                              AND ISNULL(OPI.InvNo,
                                                              '') = ISNULL(OPID2.InvNo,
                                                              '')
                                                              AND ISNULL(OPI.InvDate,
                                                              @Date) = ISNULL(OPID2.InvDate,
                                                              @Date)
                                                              AND ISNULL(OPI.ExchangeRate,
                                                              0) = ISNULL(OPID2.ExchangeRate,
                                                              0)
                              WHERE     (OPN.AccountObjectID = @AccountObjectID OR @AccountObjectID IS NULL)
                                        AND OPN.CurrencyID = @CurrencyID
                                        AND OPN.AccountNumber = @AccountNumber
                                        AND OPN.BranchID = @BranchID
                                        AND OPN.PostedDate <= @ToDate
                                        AND ( ( @IsWorkingManagementBook = 1
                                                AND OPN.IsPostedManagement = 1
                                              )
                                              OR ( @IsWorkingManagementBook = 0
                                                   AND OPN.IsPostedFinance = 1
                                                 )
                                            )
                              GROUP BY  OPN.RefID ,
                                        OPN.RefType ,
                                        RT.RefTypeName ,
                                        ( CASE WHEN OPI.RefID IS NOT NULL
                                                    AND OPI.PayAmountOC <> 0
                                               THEN OPI.InvDate
                                               ELSE OPN.PostedDate
                                          END ) ,
                                        OPN.PostedDate ,
                                        ( CASE WHEN OPI.RefID IS NOT NULL
                                                    AND OPI.PayAmountOC <> 0
                                               THEN OPI.InvNo
                                               ELSE N'OPN'
                                          END ) ,
                                        ISNULL(OPI.InvNo, '') ,
                                        ( CASE WHEN OPI.RefID IS NOT NULL
                                               THEN ISNULL(OPI.ExchangeRate, 1)
                                               ELSE ISNULL(OPN.ExchangeRate, 1)
                                          END ) ,
                                        OPN.AccountNumber ,
                                        OPID2.EmployeeID --NVTOAN add 13/04/2017 thực hiện CR 34929
                              HAVING    SUM(CASE WHEN OPI.RefID IS NOT NULL
                                                 THEN ISNULL(OPI.PayAmountOC,
                                                             0)
                                                 ELSE ISNULL(OPN.DebitAmountOC,
                                                             0)
                                                      - ISNULL(OPN.CreditAmountOC,
                                                              0)
                                            END) > 0
                              UNION ALL
                              SELECT    AL.RefID ,
                                        AL.RefType ,
                                        AL.RefTypeName ,
                                        AL.RefDate ,
                                        AL.PostedDate ,
                                        AL.RefNo ,
                                        ISNULL(AL.InvNo, '') AS InvNo ,
                                        ISNULL(AL.JournalMemo, '') AS [Description] ,
                                        ISNULL(AL.ExchangeRate, 1) AS ExchangeRate ,
                                        SUM(ISNULL(AL.DebitAmountOC, 0)
                                            - ISNULL(AL.CreditAmountOC, 0)) AS AmountOC ,
                                        SUM(ISNULL(AL.DebitAmount, 0)
                                            - ISNULL(AL.CreditAmount, 0)) AS Amount ,
                                        SUM(ISNULL(AL.DebitAmountOC, 0)
                                            - ISNULL(AL.CreditAmountOC, 0)) AS ReceiptAmountOC ,
                                        SUM(ISNULL(AL.DebitAmount, 0)
                                            - ISNULL(AL.CreditAmount, 0)) AS ReceiptAmount ,
                                        @AccountObjectID AS AccountObjectID ,
                                        AL.AccountNumber ,
                                        0 AS DetailByInvNo ,
                                        --NVTOAN add 13/04/2017 thực hiện CR 34929
                                        CASE WHEN GVDT.RefID IS NOT NULL
                                             THEN GVDT.EmployeeID
                                             ELSE AL.EmployeeID
                                        END AS EmployeeID
                              FROM      AccountObjectLedger AS AL --NVTOAN add 13/04/2017 thực hiện CR 34929
                                        LEFT JOIN (
										--/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/ 
                                                    SELECT  AOL.RefID ,
                                                            AOL.AccountObjectID ,
                                                            AOL.AccountNumber ,
                                                            AOL.EmployeeID ,
                                                            ROW_NUMBER() OVER ( PARTITION BY AOL.RefID,
                                                              AOL.AccountObjectID,
                                                              AOL.AccountNumber ORDER BY AOL.SortOrder ) AS RowNumber
                                                    FROM    dbo.AccountObjectLedger
                                                            AS AOL
                                                    WHERE   AOL.RefType IN (
                                                            4010, 4011, 4012,
                                                            4014, 4015, 4018,
                                                            4020, 4030 )
																/*Chỉ lấy theo RefType của bảng GlVoucherDetail
																Không lấy các chứng từ Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
																*/
                                                            AND AOL.EmployeeID IS NOT NULL
                                                  ) AS GVDT ON GVDT.RefID = AL.RefID
                                                              AND GVDT.AccountObjectID = AL.AccountObjectID
                                                              AND GVDT.AccountNumber = AL.AccountNumber
                                                              AND GVDT.RowNumber = 1
                              WHERE     (AL.AccountObjectID = @AccountObjectID OR @AccountObjectID IS NULL)
                                        AND AL.CurrencyID = @CurrencyID
                                        AND AL.AccountNumber = @Accountnumber
                                        AND AL.IsPostToManagementBook = @IsWorkingManagementBook
                                        AND AL.BranchID = @BranchID
						--Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp, Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi, Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá, Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
                                        AND AL.RefType NOT IN ( 1011, 1012,
                                                              1021, 1502, 1503,
                                                              1511, 1521, 1531,
                                                              4013, 4016, 4017,
                                                              611, 612, 613,
                                                              614, 615, 616,
                                                              630 )
                                        AND AL.PostedDate <= @ToDate
                              GROUP BY  AL.RefID ,
                                        AL.RefType ,
                                        AL.RefTypeName ,
                                        AL.RefDate ,
                                        AL.PostedDate ,
                                        AL.RefNo ,
                                        ISNULL(AL.InvNo, '') ,
                                        ISNULL(AL.JournalMemo, '') ,
                                        ISNULL(AL.ExchangeRate, 1) ,
                                        AL.AccountNumber ,
                                         --NVTOAN add 13/04/2017 thực hiện CR 34929
                                        CASE WHEN GVDT.RefID IS NOT NULL
                                             THEN GVDT.EmployeeID
                                             ELSE AL.EmployeeID
                                        END
                              HAVING    SUM(ISNULL(AL.DebitAmountOC, 0)
                                            - ISNULL(AL.CreditAmountOC, 0)) > 0
                            ) AS OPNTemp
                            LEFT JOIN dbo.Func_PU_GetPaiedAmountForPayVoucher(@AccountNumber,
                                                              @CurrencyID,
                                                              @BranchID,
                                                              @IsWorkingManagementBook,
                                                              @AccountObjectID) GL ON GL.RefID = OPNTemp.RefID
                                                              AND GL.AccountObjectID = OPNTemp.AccountObjectID
                                                              AND GL.AccountNumber = OPNTemp.AccountNumber
                                                              AND ( OPNTemp.DetailByInvNo = 0
                                                              OR ( OPNTemp.DetailByInvNo = 1
                                                              AND ISNULL(GL.RefNo,
                                                              '') = ISNULL(OPNTemp.RefNo,
                                                              '')
                                                              AND ISNULL(GL.RefDate,
                                                              @Date) = ISNULL(OPNTemp.RefDate,
                                                              @Date)
                                                              )
                                                              )
								--AND GL.RefNo = OPNTemp.RefNo
								--AND GL.RefDate = OPNTemp.RefDate
                  GROUP BY  OPNTemp.RefID ,
                            OPNTemp.RefType ,
                            OPNTemp.RefTypeName ,
                            OPNTemp.RefDate ,
                            OPNTemp.PostedDate ,
                            OPNTemp.RefNo ,
                            OPNTemp.InvNo ,
                            OPNTemp.[Description] ,
                            OPNTemp.ExchangeRate ,
                            OPNTemp.AmountOC ,
                            OPNTemp.Amount ,
                            OPNTemp.ReceiptAmountOC ,
                            OPNTemp.ReceiptAmount ,
                            OPNTemp.AccountObjectID ,
                            OPNTemp.AccountNumber ,
                            OPNTemp.EmployeeID--NVTOAN modify 13/04/2017 thực hiện CR 34929 
                  HAVING    OPNTemp.ReceiptAmountOC - ISNULL(SUM(GL.AmountOC),
                                                             0) > 0
                ) AL
                LEFT JOIN (
							 -- Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp
                            SELECT  RefID
                            FROM    PUReturnDetail
                            WHERE   PUVoucherRefID IS NOT NULL
                            UNION ALL
                            SELECT  RefID
                            FROM    PUDiscountDetail
                            WHERE   PUVoucherRefID IS NOT NULL
                          ) SR ON AL.RefID = SR.RefID
                LEFT JOIN (
					 /* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/ SELECT
                                                              CASE
                                                              WHEN @AccountingSystem = '15'
                                                              THEN ISNULL(GVD.RevalueExchangeRate,
                                                              1)
                                                              ELSE ISNULL(GV.ExchangeRate,
                                                              1)
                                                              END AS ExchangeRate ,
                                                              GVD.VoucherRefID ,
                                                              ROW_NUMBER() OVER ( PARTITION BY GVD.VoucherRefID ORDER BY GVD.VoucherRefID, GV.PostedDate DESC, GV.RefOrder DESC ) AS RowNumber
                                                              FROM
                                                              GLVoucher GV
                                                              INNER JOIN GLVoucherDetailDebtPayment GVD ON GVD.RefID = GV.RefID
                                                              WHERE
                                                              GV.BranchID = @BranchID
                                                              AND GV.CurrencyID = @CurrencyID
                                                              AND GVD.VoucherAccountNumber = @AccountNumber
                                                              AND GVD.VoucherAccountObjectID = @AccountObjectID
                                                              AND ( ( @IsWorkingManagementBook = 1
                                                              AND GV.IsPostedManagement = 1
                                                              )
                                                              OR ( @IsWorkingManagementBook = 0
                                                              AND GV.IsPostedFinance = 1
                                                              )
                                                              )
                          ) AS GV ON AL.RefID = GV.VoucherRefID
                                     AND GV.RowNumber = 1
                LEFT JOIN dbo.AccountObject E ON AL.EmployeeID = E.AccountObjectID --NVTOAN modify 13/04/2017 thực hiện CR 34929
        GROUP BY AL.RefID ,
                AL.RefType ,
                AL.RefTypeName ,
                AL.RefDate ,
                AL.PostedDate ,
                AL.RefNo ,
                AL.[Description] ,
                AL.ExchangeRate ,
                AL.InvNo ,
                ISNULL(GV.ExchangeRate, 0) ,
                AL.AccountObjectID ,
                AL.EmployeeID ,--NVTOAN modify 13/04/2017 thực hiện CR 34929 
                E.AccountObjectCode ,--NVTOAN modify 22/04/2017 thực hiện CR 34929 
                E.AccountObjectName
        HAVING  SUM(AL.ReceiptAmountOC) > 0
        ORDER BY AL.RefDate ,--DATRUONG 25.08.2015 Chỉnh lại sort với chế độ tăng dần ngày chứng từ
                AL.RefNo ,
                AL.InvNo
    END
