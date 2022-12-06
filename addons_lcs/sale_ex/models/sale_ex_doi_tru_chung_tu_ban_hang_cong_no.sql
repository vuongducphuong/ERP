SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
/* Created By  : VNTUAN	
 * Created Date: 14.10.2014
 * Description : Store lấy dữ liệu cho chi tiết đối trừ bán hàng (chứng từ công nợ)
 bổ sung tỷ giá sửa bug 89202 by hoant 01.02.2016
 */
--nvtoan Modify 11/04/2017: Sửa lỗi 90132 - Không phản ánh số tiền giảm giá, trả lại khi tỷ giá giữa chứng từ mua hàng và chứng từ giảm giá, trả lại khác nhau 
--NVTOAN modify 13/04/2017 thực hiện CR 34929 - Lấy bổ sung thông tin nhân viên

DECLARE				@AccountObjectID UNIQUEIDENTIFIER 
DECLARE				@AccountNumber NVARCHAR(25) 
DECLARE				@CurrencyID NVARCHAR(3) 
DECLARE				@BranchID UNIQUEIDENTIFIER 
DECLARE				@IsWorkingManagementBook BIT 
DECLARE				@ToDate DATETIME


SET				@AccountObjectID=NULL
SET				@AccountNumber=N'131'
SET				@CurrencyID=N'VND'
SET				@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET				@IsWorkingManagementBook=0
SET				@ToDate='2019-05-25 00:00:00'

    BEGIN
        DECLARE @AccountingSystem NVARCHAR(MAX)
        SELECT TOP 1
                @AccountingSystem = ISNULL(OptionValue, '')
        FROM    SYSDBOption
        WHERE   OptionID LIKE N'%AccountingSystem%' 
        DECLARE @OPNRefNo AS NVARCHAR(25)
        SET @OPNRefNo = 'OPN'
        DECLARE @Date AS DATETIME
        SET @Date = GETDATE()
        SELECT  TEM.RefID ,
                CAST(TEM.RefType AS VARCHAR(50)) AS RefType,
                TEM.RefTypeName ,
                TEM.RefDate ,
                TEM.PostedDate ,
                TEM.RefNo ,
                TEM.InvDate ,
                TEM.InvNo ,
                TEM.[Description] ,
                TEM.ExchangeRate ,
                ISNULL(GV.ExchangeRate, 0) AS RevaluationExchangeRate ,
                TEM.TotalAmountOC AS AmountOC ,
                TEM.TotalAmount AS Amount ,
                ISNULL(TEM.AmountOC, 0) - SUM(ISNULL(GL.AmountOC, 0)) AS DebtAmountOC ,
                ISNULL(TEM.Amount, 0) - SUM(ISNULL(GL.Amount, 0)) AS DebtAmount ,
                CAST(0 AS DECIMAL) AS CrossEntryAmountOC ,
                CAST(0 AS DECIMAL) AS CrossEntryAmount ,
                @AccountObjectID AS AccountObjectID ,
                TEM.DueDate ,
                TEM.EmployeeID ,
                E.AccountObjectCode AS EmployeeCode , --nvtoan Modify 22/04/2017: Sửa lỗi 96455                
                E.AccountObjectName AS EmployeeName --NVTOAN modify 13/04/2017 thực hiện CR 34929                 
        FROM    (
		 /*Begin subquery*/ SELECT  OPN.RefID ,
                                    OPN.RefType ,
                                    RT.RefTypeName ,
                                    ( CASE WHEN OPI.RefID IS NOT NULL
                                           THEN OPI.InvDate
                                           ELSE OPN.PostedDate
                                      END ) RefDate ,
                                    OPN.PostedDate ,
                                    @OPNRefNo AS RefNo ,
                                    OPI.InvDate ,
                                    ISNULL(OPI.InvNo, '') AS InvNo ,
                                    SPACE(0) AS [Description] ,
                                    ( CASE WHEN OPI.RefID IS NOT NULL
                                           THEN ISNULL(OPI.ExchangeRate, 1)
                                           ELSE ISNULL(OPN.ExchangeRate, 1)
                                      END ) AS ExchangeRate ,
                                    SUM(CASE WHEN OPI.RefID IS NOT NULL
                                             THEN ISNULL(OPI.InvoiceAmountOC,
                                                         0)
                                             ELSE ISNULL(OPN.DebitAmountOC, 0)
                                                  - ISNULL(OPN.CreditAmountOC,
                                                           0)
                                        END) AS TotalAmountOC ,
                                    SUM(CASE WHEN OPI.RefID IS NOT NULL
                                             THEN ISNULL(OPI.InvoiceAmount, 0)
                                             ELSE ISNULL(OPN.DebitAmount, 0)
                                                  - ISNULL(OPN.CreditAmount, 0)
                                        END) AS TotalAmount ,
                                    SUM(CASE WHEN OPI.RefID IS NOT NULL
                                             THEN ISNULL(OPI.AmountOC, 0)
                                             ELSE ISNULL(OPN.DebitAmountOC, 0)
                                                  - ISNULL(OPN.CreditAmountOC,
                                                           0)
                                        END) AS AmountOC ,
                                    SUM(CASE WHEN OPI.RefID IS NOT NULL
                                             THEN ISNULL(OPI.Amount, 0)
                                             ELSE ISNULL(OPN.DebitAmount, 0)
                                                  - ISNULL(OPN.CreditAmount, 0)
                                        END) AS Amount ,
                                    1 AS DetailByInvNo ,
                                    OPID.DueDate ,
                                    OPID2.EmployeeID
                            FROM    OpeningAccountEntry OPN
                                    INNER JOIN SYSRefType RT ON RT.RefType = OPN.RefType
                                    LEFT JOIN OpeningAccountEntryDetailInvoice OPI ON OPI.RefID = OPN.RefID
                                    LEFT JOIN ( SELECT  OAEDI.RefID ,
                                                        ISNULL(OAEDI.InvDate,
                                                              @Date) AS InvDate ,
                                                        ISNULL(OAEDI.InvNo, '') AS InvNo ,
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
                                    LEFT JOIN ( SELECT  OAEDI.RefID ,
                                                        ISNULL(OAEDI.InvDate,
                                                              @Date) AS InvDate ,
                                                        ISNULL(OAEDI.InvNo, '') AS InvNo ,
                                                        OAEDI.DueDate ,
                                                        ISNULL(OAEDI.ExchangeRate,
                                                              0) AS ExchangeRate ,
                                                        ROW_NUMBER() OVER ( PARTITION BY OAEDI.RefID,
                                                              ISNULL(OAEDI.InvDate,
                                                              @Date),
                                                              ISNULL(OAEDI.InvNo,
                                                              ''),
                                                              ISNULL(OAEDI.ExchangeRate,
                                                              0) ORDER BY OAEDI.SortOrder ) AS RowNumber
                                                FROM    dbo.OpeningAccountEntryDetailInvoice
                                                        AS OAEDI
                                                WHERE   OAEDI.DueDate IS NOT NULL
                                              ) AS OPID ON OPN.RefID = OPID.RefID
                                                           AND OPID.RowNumber = 1
                                                           AND ISNULL(OPI.InvNo,
                                                              '') = ISNULL(OPID.InvNo,
                                                              '')
                                                           AND ISNULL(OPI.InvDate,
                                                              @Date) = ISNULL(OPID.InvDate,
                                                              @Date)
                                                           AND ISNULL(OPI.ExchangeRate,
                                                              0) = ISNULL(OPID.ExchangeRate,
                                                              0)
                            WHERE   (OPN.AccountObjectID = @AccountObjectID OR @AccountObjectID IS NULL)
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
                            GROUP BY OPN.RefID ,
                                    OPI.RefID ,
                                    OPN.RefType ,
                                    RT.RefTypeName ,
                                    OPN.PostedDate ,
                                    OPI.InvDate ,
                                    ISNULL(OPI.InvNo, '') ,
                                    ISNULL(OPI.ExchangeRate, 1) ,
                                    ISNULL(OPN.ExchangeRate, 1) ,
                                    OPID.DueDate ,
                                    OPID2.EmployeeID
                            HAVING  SUM(CASE WHEN OPI.RefID IS NOT NULL
                                             THEN ISNULL(OPI.AmountOC, 0)
                                             ELSE ISNULL(OPN.DebitAmountOC, 0)
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
                            AL.InvDate ,
                            ISNULL(AL.InvNo, '') AS InvNo ,
                            ISNULL(AL.JournalMemo, '') AS [Description] ,
                            ISNULL(AL.ExchangeRate, 1) AS ExchangeRate ,
                            SUM(ISNULL(AL.DebitAmountOC, 0)
                                - ISNULL(AL.CreditAmountOC, 0)) AS TotalAmountOC ,
                            SUM(ISNULL(AL.DebitAmount, 0)
                                - ISNULL(AL.CreditAmount, 0)) AS TotalAmount ,
                            SUM(ISNULL(AL.DebitAmountOC, 0)
                                - ISNULL(AL.CreditAmountOC, 0)) AS AmountOC ,
                            SUM(ISNULL(AL.DebitAmount, 0)
                                - ISNULL(AL.CreditAmount, 0)) AS Amount ,
                            0 AS DetailByInvNo ,
                            AL.DueDate ,
                            /*Nếu chứng từ Nghiệp vụ khác thì sẽ lấy nhân viên đầu tiên trên form chi tiết*/
                            CASE WHEN GVDT.RefID IS NOT NULL
                                 THEN GVDT.EmployeeID
                                 ELSE AL.EmployeeID
                            END AS EmployeeID
                  FROM      AccountObjectLedger AL
                            LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/ SELECT
                                                              AOL.RefID ,
                                                              AOL.AccountObjectID ,
                                                              AOL.AccountNumber ,
                                                              AOL.EmployeeID ,
                                                              ROW_NUMBER() OVER ( PARTITION BY AOL.RefID,
                                                              AOL.AccountObjectID,
                                                              AOL.AccountNumber ORDER BY AOL.SortOrder ) AS RowNumber
                                                              FROM
                                                              dbo.AccountObjectLedger
                                                              AS AOL
                                                              WHERE
                                                              AOL.RefType IN (
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
                            LEFT JOIN (
						/* Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp*/ SELECT
                                                              RefID
                                                              FROM
                                                              SAReturnDetail
                                                              WHERE
                                                              SAVoucherRefID IS NOT NULL
                                        UNION
                                        SELECT  RefID
                                        FROM    SADiscountDetail
                                        WHERE   SAVoucherRefID IS NOT NULL
                                      ) SR ON AL.RefID = SR.RefID
                  WHERE     (AL.AccountObjectID = @AccountObjectID OR @AccountObjectID IS NULL)
                            AND AL.CurrencyID = @CurrencyID
                            AND AL.AccountNumber = @Accountnumber
                            AND AL.IsPostToManagementBook = @IsWorkingManagementBook
                            AND AL.BranchID = @BranchID
                            AND AL.PostedDate <= @ToDate
				   /* Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp,
				   *  Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi, 
				   *  Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá, 
				   *  Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ*/
                            AND AL.RefType NOT IN ( 1011, 1012, 1021, 1502,
                                                    1503, 1511, 1521, 1531,
                                                    4013, 4016, 4017 )
					/*Không lấy số dư đầu kỳ do lấy ở trên rồi*/
                            AND AL.RefType NOT IN ( 611, 612, 613, 614, 615,
                                                    616, 630 )
					/*Không lấy các chứng từ trả lại, giảm giá*/
                            AND SR.RefID IS NULL
                  GROUP BY  AL.RefID ,
                            AL.RefType ,
                            AL.RefTypeName ,
                            AL.RefDate ,
                            AL.PostedDate ,
                            AL.RefNo ,
                            AL.InvDate ,
                            ISNULL(AL.InvNo, '') ,
                            ISNULL(AL.JournalMemo, '') ,
                            ISNULL(AL.ExchangeRate, 1) ,
                            AL.DueDate ,
                            CASE WHEN GVDT.RefID IS NOT NULL
                                 THEN GVDT.EmployeeID
                                 ELSE AL.EmployeeID
                            END
                  HAVING    SUM(ISNULL(AL.DebitAmountOC, 0)
                                - ISNULL(AL.CreditAmountOC, 0)) > 0
	 /*End Subquery*/
                ) AS TEM
                LEFT JOIN dbo.Func_SA_GetPaiedAmountForDebtVoucher(@AccountNumber,
                                                              @CurrencyID,
                                                              @BranchID,
                                                              @IsWorkingManagementBook,
                                                              @AccountObjectID) GL ON GL.RefID = TEM.RefID
                                                              AND ( TEM.DetailByInvNo = 0
                                                              OR ( TEM.DetailByInvNo = 1
                                                              AND ISNULL(GL.InvNo,
                                                              '') = ISNULL(TEM.InvNo,
                                                              '')
                                                              AND ISNULL(GL.InvDate,
                                                              @Date) = ISNULL(TEM.InvDate,
                                                              @Date)
                                                              )
                                                              )
                                                              AND ( ( GL.ExchangeRate = TEM.ExchangeRate )
                                                              OR RefType NOT IN (
                                                              611, 612, 613,
                                                              614, 615, 616,
                                                              630 )--nvtoan modify 11/04/2017 Sửa lỗi 90132: Đối với chứng từ không phải số dư đầu thì không join qua ExchangeRate
                                                              )
                LEFT JOIN ( SELECT  CASE WHEN @AccountingSystem = '15'
                                         THEN ISNULL(GVD.RevalueExchangeRate,
                                                     1)
                                         ELSE ISNULL(GV.ExchangeRate, 1)
                                    END AS ExchangeRate ,/* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/
                                    GVD.VoucherRefID ,
                                    ROW_NUMBER() OVER ( PARTITION BY GVD.VoucherRefID ORDER BY GVD.VoucherRefID, GV.PostedDate DESC, GV.RefOrder DESC ) AS RowNumber
                            FROM    GLVoucher GV
                                    INNER JOIN GLVoucherDetailDebtPayment GVD ON GVD.RefID = GV.RefID
                            WHERE   GV.BranchID = @BranchID
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
                          ) AS GV ON TEM.RefID = GV.VoucherRefID
                                     AND GV.RowNumber = 1
                LEFT JOIN dbo.AccountObject E ON TEM.EmployeeID = E.AccountObjectID --NVTOAN modify 13/04/2017 thực hiện CR 34929
        GROUP BY TEM.RefID ,
                TEM.RefType ,
                TEM.RefTypeName ,
                TEM.RefDate ,
                TEM.PostedDate ,
                TEM.RefNo ,
                TEM.InvDate ,
                TEM.InvNo ,
                TEM.[Description] ,
                TEM.ExchangeRate ,
                ISNULL(GV.ExchangeRate, 0) ,
                TEM.AmountOC ,
                TEM.Amount ,
                TEM.TotalAmountOC ,
                TEM.TotalAmount ,
                TEM.DueDate ,
                TEM.EmployeeID ,
                E.AccountObjectCode , --nvtoan Modify 22/04/2017: Sửa lỗi 96455                
                E.AccountObjectName --NVTOAN modify 13/04/2017 thực hiện CR 34929
        HAVING  ISNULL(TEM.AmountOC, 0) - SUM(ISNULL(GL.AmountOC, 0)) > 0
        ORDER BY TEM.RefDate ,
                TEM.PostedDate ,
                TEM.RefNo ,
                TEM.InvDate ,
                TEM.InvNo
    END
