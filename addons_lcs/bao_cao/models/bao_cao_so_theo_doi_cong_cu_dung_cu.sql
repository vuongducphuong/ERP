SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		<vttien>
-- Create date: <17/05/2014>
-- Description:	<Lấy dữ liệu sổ theo dõi CCDC>
-- lcvinh - 3/10/2014 - Sửa lại điều kiện sau khi BNDinh vứt các trường Finance và Management
--nvtoan modify 04/04/2016: Sửa lỗi chọn loại ccdc cha không lấy số liệu của ccdc con, ccdc còn số lượng trong kỳ nhưng không lên số liệu
-- nvtoan modify 13/07/2017: Lấy bổ sung nhóm CCDC theo PBI 13015
-- =============================================
-- tthoa edit 1/10/2014

DECLARE    @BranchID UNIQUEIDENTIFIER 
DECLARE    @IncludeDependentBranch BIT 
DECLARE    @FromDate DATETIME 
DECLARE    @ToDate DATETIME 
DECLARE    @SupplyCategoryID UNIQUEIDENTIFIER = NULL 
DECLARE    @IsWorkingWithManagementBook BIT
	

SET									@BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'--CHI_NHANH_ID
SET                                 @IncludeDependentBranch = 1--BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC
SET                                 @FromDate = '2018-01-01 00:00:00' --TU
SET                                 @ToDate = '2018-12-31 23:59:59'--DEN
SET                                 @SupplyCategoryID = NULL --LOAI_CCDC_ID
SET                                 @IsWorkingWithManagementBook = 0;

    BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
        SET NOCOUNT ON;
	-- Giá trị PB hàng kỳ	Phân bổ trong kỳ	Lũy kế đã PB	Giá trị còn lại	TK chờ phân bổ
	
        DECLARE @SupplyCategoryMisaCodeID NVARCHAR(20)
        SELECT  @SupplyCategoryMisaCodeID = MISACodeID --MA_PHAN_CAP
        FROM    dbo.SupplyCategory SC --danh_muc_loai_cong_cu_dung_cu
        WHERE   SupplyCategoryID = @SupplyCategoryID   --id = LOAI_CCDC_ID

        DECLARE @StartDate AS DATETIME 
        SELECT  @StartDate = CONVERT(DATETIME, OptionValue) --value
        FROM    dbo.SYSDBOption  --ir_config_parameter
        WHERE   OptionID = 'StartDate' --KEY = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
                AND IsDefault = 1	
	
        SELECT  ROW_NUMBER() OVER ( ORDER BY SUI.RefDate, SUI.SupplyCode ) AS RowNum ,
		--SL.RefID,
                SUI.SupplyID AS RefID ,--ID_CHUNG_TU
                SUI.RefType , --LOAI_CHUNG_TU
                SUI.SupplyID , --id
                SUI.SupplyCode , -- Mã CCDC --MA_CCDC
                SUI.SupplyName , -- Tên CCDC --TEN_CCDC
                SUC.SupplyCategoryName , -- Loại CCDC
                SUI.SupplyGroup,--nvtoan add 13/07/2017 
                SUI.RefDate , -- Ngày ghi tăng --NGAY_GHI_TANG
                SUI.RefNo , -- Số CT ghi tăng--SO_CT_GHI_TANG
                SUI.ReasonIncrement , -- Lý do ghi tăng --LY_DO_GHI_TANG
		--Số kỳ phân bổ trên ghi tăng hoặc khai báo CCDC đầu kỳ + Chênh lệch điều chỉnh số kỳ phân bổ còn lại trên chứng từ điều chỉnh có ngày điều chỉnh <= Đến ngày của kỳ báo cáo
                SUI.AllocationTime + SUM(CASE WHEN SL.RefType <> 454 THEN 0 --SO_KY_PHAN_BO 
                                              ELSE SL.IncrementAllocationTime -- SO_KY_PHAN_BO_GHI_TANG
                                                   - SL.DecrementAllocationTime --SO_KY_PHAN_BO_GHI_GIAM
                                         END) AS AllocationTime , -- Số kỳ phân bổ --SO_KY_PHAN_BO
		--Số kỳ PB còn lại = Số kỳ phân bổ trên khai cáo chi tiết CCDC còn lại – Số tháng đã phân bổ (căn cứ vào chứng từ phân bổ có ngày hạch toán <= đến ngày của kỳ báo cáo) + Chênh lệch điều chỉnh số kỳ phân bổ còn lại trên chứng từ điều chỉnh có ngày điều chỉnh <= Đến ngày của kỳ báo cáo
                CASE WHEN SUI.RemainingAllocationTime --SO_KY_PB_CON_LAI
                          + SUM(CASE WHEN SL.RefType = 450
                                          OR SL.RefType = 457 THEN 0
                                     ELSE SL.IncrementAllocationTime --SO_KY_PHAN_BO_GHI_TANG
                                          - SL.DecrementAllocationTime --SO_KY_PHAN_BO_GHI_GIAM
                                END) < 0 THEN 0
                     ELSE SUI.RemainingAllocationTime --SO_KY_PB_CON_LAI
                          + SUM(CASE WHEN SL.RefType = 450
                                          OR SL.RefType = 457 THEN 0
                                     ELSE SL.IncrementAllocationTime --SO_KY_PHAN_BO_GHI_TANG
                                          - SL.DecrementAllocationTime--SO_KY_PHAN_BO_GHI_GIAM
                                END)
                END AS ResidualAllocationTime , -- Số kỳ phân bổ còn lại--SO_KY_PHAN_BO_CON_LAI
                SUI.Unit ,--DON_VI_TINH
                SUI.Quantity , -- Số lượng ghi tăng --SO_LUONG
                SUM(CASE WHEN SL.PostedDate < @FromDate
                              OR SL.REftype <> 452 THEN 0
                         ELSE SL.DecrementQuantity --
                    END) AS DecrementQuantity , -- Số lượng giảm trong kỳ--SO_LUONG_GHI_GIAM
                SUM(CASE WHEN SL.REftype <> 452 THEN 0
                         ELSE SL.DecrementQuantity
                    END) AS AccumDecrementQuantity , -- Số lượng giảm lũy kế--SO_LUONG_GHI_GIAM_LUY_KE
                SUI.Quantity - SUM(CASE WHEN SL.REftype <> 452 THEN 0
                                        ELSE SL.DecrementQuantity
                                   END) AS ResidualQuantity , -- SL còn lại --SO_LUONG_CON_LAI
		-- Giá trị CCDC = Thành tiền của CCDC trên khai báo chi tiết CCDC tương ứng với từng CCDC + Chênh lệch Giá trị còn lại trên chứng từ điều chỉnh CCDC có ngày điều chỉnh <= Đến ngày của kỳ báo cáo tương ứng với từng CCDC
                SUI.Amount + SUM(CASE WHEN SL.RefType <> 454 THEN 0
                                      ELSE SL.IncrementAmount --SO_TIEN_GHI_TANG
                                           - SL.DecrementAmount --SO_TIEN_GHI_GIAM
                                 END) AS Amount ,--SO_TIEN
                ISNULL(SL2.TermlyAllocationAmount, SUI.TermlyAllocationAmount) AS TermlyAllocationAmount , -- Giá trị PB hàng kỳ (tạm)--SO_TIEN_PHAN_BO_HANG_KY
               
		-- nếu là ccdc có kỳ phân bổ nhập ban đầu bằng 1 thì phân bổ trong kỳ nếu chứa ngày ghi tăng thì sẽ bằng luôn giá trị còn lại
		-- nếu là ccdc đầu kỳ thì xét theo ngày bắt đầu dữ liệu
                SUM(CASE WHEN SUI.AllocationTime = 1 --SO_KY_PHAN_BO
                 /*=> Kiến nghị: Với CCDC đầu kỳ có số kỳ phân bổ bằng 1 thì hiểu là CCDC đã được phân bổ chi phí do đó trên sổ CCDC ký phân bổ trong kỳ luôn = 0 và Lũy kế đã phân bổ = giá trị của CCDC
*/
                              --AND ( ( SL.RefType = 450
                              --        AND SL.RefDate BETWEEN @FromDate AND @ToDate
                              --      )
                              --      OR ( SL.RefType = 457
                              --           AND @StartDate BETWEEN @FromDate AND @ToDate
                              --         )
                              --    ) 
                              THEN 0 -- SL.AllocationAmount
                         WHEN SL.PostedDate < @FromDate
                              OR SL.RefType <> 453 THEN 0
                         ELSE SL.AllocationAmount --
                    END) AS AllocationAmount , -- Phân bổ trong kỳ --SO_TIEN_PHAN_BO
                SUM(CASE WHEN SUI.AllocationTime = 1 THEN SL.AllocationAmount 
                         WHEN SL.RefType <> 453
                              AND SL.RefType <> 457
                              AND SL.RefType <> 450 THEN 0
                         ELSE SL.AllocationAmount
                    END) AS AccumAllocationAmount , -- Lũy kế phân bổ --SO_TIEN_PHAN_BO_LUY_KE
                CASE WHEN SUI.AllocationTime = 1 THEN 0
                     ELSE SUI.Amount + SUM(CASE WHEN SL.RefType <> 454 THEN 0
                                                ELSE SL.IncrementAmount
                                                     - SL.DecrementAmount
                                           END)
                          - SUM(CASE WHEN SL.RefType <> 453
                                          AND SL.RefType <> 457 THEN 0
                                     ELSE SL.AllocationAmount
                                END)
                END AS ResidualAmount , -- Giá trị còn lại  --SO_TIEN_CON_LAI
                SUI.AllocationAccount -- Tài khoản chờ phân bổ --TK."SO_TAI_KHOAN"
                ,
                OU.OrganizationUnitName BranchName
        FROM    dbo.SUIncrement SUI --supply_ghi_tang
                INNER JOIN dbo.SupplyLedger SL ON SL.SupplyID = SUI.SupplyID  --so_ccdc_chi_tiet SL ON SL."CCDC_ID" = SUI.id
                LEFT JOIN dbo.SupplyCategory SUC ON SUC.SupplyCategoryID = SUI.SupplyCategoryID  --danh_muc_loai_cong_cu_dung_cu SUC ON SUC.id = SUI."LOAI_CCDC_ID"
                INNER JOIN dbo.OrganizationUnit OU ON SUI.BranchID = OU.OrganizationUnitID  --danh_muc_to_chuc OU ON SUI."CHI_NHANH_ID" = OU.id
	-- Giá trị phân bổ hàng kỳ
                OUTER APPLY ( SELECT TOP 1
                                        SL2.TermlyAllocationAmount --SO_TIEN_PHAN_BO_HANG_KY
                              FROM      dbo.SupplyLedger SL2  --so_ccdc_chi_tiet
                              WHERE     SL2.SupplyID = SL.SupplyID
                                        AND SL2.PostedDate <= @ToDate
                                        AND SL2.RefType IN ( 450, 454, 457 )
                              ORDER BY  SL2.PostedDate DESC ,
                                        SL2.SortOrder DESC
                            ) SL2
	-- Lấy chứng từ ghi giảm cuối cùng
                OUTER APPLY ( SELECT TOP 1
                                        SL2.PostedDate
                              FROM      dbo.SupplyLedger SL2
                              WHERE     SL2.SupplyID = SL.SupplyID
                                        AND SL2.PostedDate <= @ToDate
                                        AND SL2.RefType = 452
                              ORDER BY  SL2.PostedDate DESC ,
                                        SL2.SortOrder DESC
                            ) SL3
        WHERE   SL.PostedDate <= @ToDate
				--nvtoan modify 04/04/2016: Sửa lỗi chọn loại ccdc cha không lấy số liệu của ccdc con
                --AND ( SUC.SupplyCategoryID = @SupplyCategoryID
                --      OR @SupplyCategoryID IS NULL
                --    )
                AND ( @SupplyCategoryID IS NULL --LOAI_CCDC_ID = -1
                      OR SUC.MISACodeID LIKE @SupplyCategoryMisaCodeID + '%' --"MA_PHAN_CAP" LIKE MA_PHAN_CAP_LOAI_CCDC
                    )
                AND ( OU.OrganizationUnitID = @BranchID 
                      OR ( @IncludeDependentBranch = 1 --BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC
                           AND OU.IsDependent = 1 --HACH_TOAN_SELECTION" = 'PHU_THUOC'
                         )
                    )
                AND SL.IsPostToManagementBook = @IsWorkingWithManagementBook
        GROUP BY SUI.SupplyID , 
		--RefID,
                SUI.RefType ,
                SUI.SupplyID ,
                SUI.SupplyCode ,--MA_CCDC
                SUI.SupplyName ,--TEN_CCDC
                SUI.ReasonIncrement , --LY_DO_GHI_TANG
                SUC.SupplyCategoryName ,--TEN
                SUI.SupplyGroup, --nvtoan add 13/07/2017
                SUI.RefDate , --NGAY_GHI_TANG
                SUI.RefNo , --SO_CT_GHI_TANG
                SUI.AllocationTime , --SO_KY_PHAN_BO
                SUI.RemainingAllocationTime ,--SO_KY_PB_CON_LAI
                SUI.Unit ,--DON_VI_TINH
                SUI.Quantity ,--SO_LUONG
                SUI.Amount ,--THANH_TIEN
                ISNULL(SL2.TermlyAllocationAmount, SUI.TermlyAllocationAmount) ,--SO_TIEN_PHAN_BO_HANG_KY
                SUI.AllocationAccount ,--TK."SO_TAI_KHOAN"
                SL3.PostedDate ,--NGAY_HACH_TOAN
                OU.OrganizationUnitName
        HAVING  --nvtoan modify 04/04/2016: Sửa lỗi số lượng CCDC còn trong kỳ nhưng không lên báo cáo (Error 97527)
				( SUI.Quantity - SUM(CASE WHEN SL.REftype <> 452 THEN 0
                                          ELSE CASE WHEN SL.PostedDate < @FromDate
                                                    THEN SL.DecrementQuantity
                                                    ELSE 0
                                               END
                                     END) > 0 )        
        --SUI.Quantity - SUM(CASE WHEN SL.REftype <> 452 THEN 0
        --                                ELSE SL.DecrementQuantity
        --                           END) > 0
                OR SL3.PostedDate BETWEEN @FromDate AND @ToDate 
	--ORDER BY SUI.RefDate, SUI.SupplyCode
	   
    END

GO