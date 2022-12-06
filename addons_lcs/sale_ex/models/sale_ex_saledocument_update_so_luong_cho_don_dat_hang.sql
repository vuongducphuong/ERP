SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- [dbo].[Proc_SA_Update_QuantityDelivered_By_SAVoucherID]
-- Author:		<LDNGOC>
-- Create date: <26.09.2014>
-- Description:	<Cập nhật số lượng giao trên Đơn đặt hàng khi Thêm/Sửa/Xóa chứng từ bán hàng>
-- Proc_SA_Update_QuantityDelivered_By_SAVoucherID  NULL, 0, ',d5972ca1-eea8-4732-b2f6-ce004ef607fb,'
-- 17.01.2015: cập nhật trường hợp Delete thì trên form Clone DataSet ra trước, sau delete thì mới chạy hàm cập nhật để xuống đây đỡ phải case cối phức tạp.
-- HHSon 02.06.2016 fix bug 106206: Làm tròn số lượng giao theo định dạng số của SL
/*HHSon 21.06.2016 107912: Thay đổi cách cập nhật SL giao trên DDH:
- Trường hợp CTBH và DDH cùng ĐVT thì cập nhật SL giao theo cột SL trên CT bán hàng
- Trường hợp CTBH và DDH khác ĐVT thì tính lại SL giao cần cập nhật = SL theo ĐVC (trên CTBH) *(/)Tỷ lệ CĐ (trên DDH)
*/
--vhanh edited 28.06.2017: Cập nhật số lượng đã giao trên đơn đặt hàng dựa theo cả thông tin trên hàng bán trả lại (CR 12960)
-- =============================================

DECLARE				@SAVoucherRefID UNIQUEIDENTIFIER  --ID của chứng từ bán hàng
DECLARE				@ListOrderID NVARCHAR(MAX) -- chuỗi ID các đơn đặt hàng được chọn trên CT bán hàng

SET			@SAVoucherRefID=NULL
SET			@ListOrderID=N',e71e283a-fe7b-4c1f-9e41-214298e897b0,'


    BEGIN
    DECLARE @QuantityDigits INT
    SET  @QuantityDigits = (SELECT TOP 1 CAST(OptionValue AS INT)
    FROM    dbo.SYSDBOption
    WHERE   OptionID = 'QuantityDecimalDigits') 
    
    CREATE TABLE #tblOrderID(OrderID UNIQUEIDENTIFIER)
    INSERT INTO #tblOrderID
            ( OrderID )
    SELECT VALUE FROM dbo.Func_ConvertGUIStringIntoTable(@ListOrderID, ',')
    
    /*Tạo bảng chứa số lượng đã giao trên các chứng từ bán trả lại, bán hàng*/
	CREATE TABLE #tblSAOrderDelivered
			(
				OrderID UNIQUEIDENTIFIER ,
				OrderDetailID UNIQUEIDENTIFIER,
				InventoryItemID UNIQUEIDENTIFIER ,
				QuantityDelivered DECIMAL(22,8),
				MainQuantityDelivered DECIMAL(22,8)
			)
	INSERT INTO #tblSAOrderDelivered
			( OrderID ,
			  OrderDetailID ,
			  InventoryItemID ,
			  QuantityDelivered ,
			  MainQuantityDelivered
			)
	SELECT
			T.OrderID ,
			T.RefDetailID ,
			T.InventoryItemID ,
			SUM(QuantityDelivered),
			SUM(MainQuantityDelivered)
	FROM
		(
			/*Lấy số đã giao từ chứng từ bán hàng*/
			SELECT	
					TOI.OrderID ,
					SOD.RefDetailID ,
					SOD.InventoryItemID ,
					QuantityDelivered = SUM(ROUND(CASE WHEN (( SOD.UnitID IS NULL AND SVD.UnitID IS NULL)OR ( SOD.UnitID IS NOT NULL AND SVD.UnitID IS NOT NULL AND SOD.UnitID = SVD.UnitID)) THEN SVD.Quantity
																				  ELSE (CASE WHEN ( SOD.ExchangeRateOperator = '/' ) -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
																							 THEN ROUND(SVD.MainQuantity * SOD.MainConvertRate, @QuantityDigits)
																						WHEN ( SOD.ExchangeRateOperator = '*' AND SOD.MainConvertRate != 0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
																							 THEN ROUND(SVD.MainQuantity / SOD.MainConvertRate, @QuantityDigits)
																						 ELSE SVD.MainQuantity -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
																						END )
																			  END, @QuantityDigits)),
					MainQuantityDelivered = SUM(SVD.MainQuantity)
			FROM	#tblOrderID AS TOI 
					INNER JOIN dbo.SAOrderDetail AS SOD ON SOD.RefID = TOI.OrderID 
					INNER JOIN dbo.SAVoucherDetail AS SVD ON SOD.RefDetailID = SVD.SAOrderRefDetailID AND SOD.InventoryItemID = SVD.InventoryItemID
			GROUP BY
					TOI.OrderID ,
					SOD.RefDetailID ,
					SOD.InventoryItemID
			
			/*Lấy số đã giao từ chứng từ bán trả lại*/
			UNION ALL
			SELECT	
					TOI.OrderID ,
					SOD.RefDetailID ,
					SOD.InventoryItemID ,
					QuantityDelivered = (-1) * ISNULL(SUM(ROUND(CASE WHEN (( SOD.UnitID IS NULL AND SVD.UnitID IS NULL)OR ( SOD.UnitID IS NOT NULL AND SVD.UnitID IS NOT NULL AND SOD.UnitID = SVD.UnitID)) THEN SVD.Quantity
																				  ELSE (CASE WHEN ( SOD.ExchangeRateOperator = '/' ) -- Nếu phép tính quy đổi là "/" thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng * tỷ lệ CĐ trên DDH
																							 THEN ROUND(SVD.MainQuantity * SOD.MainConvertRate, @QuantityDigits)
																						WHEN ( SOD.ExchangeRateOperator = '*' AND SOD.MainConvertRate != 0) --Nếu phép tính quy đổi là "*" và Tỷ lệ CĐ trên DDH <> 0 thì SL theo ĐVT trên DDH = SL theo ĐVC trên CT bán hàng / tỷ lệ CĐ trên DDH
																							 THEN ROUND(SVD.MainQuantity / SOD.MainConvertRate, @QuantityDigits)
																						 ELSE SVD.MainQuantity -- Các TH còn lại thì lấy luôn SL theo ĐVC trên CTBH
																						END )
																			  END, @QuantityDigits)), 0),
					MainQuantityDelivered = (-1) * ISNULL(SUM(SVD.MainQuantity), 0)
			FROM	#tblOrderID AS TOI 
					INNER JOIN dbo.SAOrderDetail AS SOD ON SOD.RefID = TOI.OrderID
					INNER JOIN dbo.SAReturnDetail AS SVD ON SOD.RefDetailID = SVD.SAOrderRefDetailID AND SOD.InventoryItemID = SVD.InventoryItemID
			GROUP BY
					TOI.OrderID ,
					SOD.RefDetailID ,
					SOD.InventoryItemID
		) AS T
	GROUP BY
			T.OrderID ,
			T.RefDetailID ,
			T.InventoryItemID
		
	SELECT * FROM #tblSAOrderDelivered		
	/*cập nhật vào đơn đặt hàng số lượng đã giao = Số lượng đã giao từ năm trước + số lượng đã giao trên các chứng từ phát sinh*/
	UPDATE	SOD
	SET		QuantityDeliveredSA = ISNULL(QuantityDeliveredSALastYear, 0) + ISNULL(TSOD.QuantityDelivered, 0),
			MainQuantityDeliveredSA = ISNULL(MainQuantityDeliveredSALastYear, 0) + ISNULL(TSOD.MainQuantityDelivered, 0)
	FROM	dbo.SAOrderDetail AS SOD
			INNER JOIN #tblOrderID AS TOI ON SOD.RefID = TOI.OrderID
			LEFT JOIN  #tblSAOrderDelivered AS TSOD ON SOD.RefDetailID = TSOD.OrderDetailID

		
	DROP TABLE #tblOrderID
	DROP TABLE #tblSAOrderDelivered
    END