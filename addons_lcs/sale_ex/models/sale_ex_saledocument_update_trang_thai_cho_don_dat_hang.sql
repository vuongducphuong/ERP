SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================  
-- Author:  <LDNGOC>  
-- Create date: <26.09.2014>  
-- Description: <Cập nhật tình trạng đơn hàng khi thêm/sửa chứng từ bán hàng/xuất kho>  
-- 0: Chưa thực hiện; 1: Đang thực hiện; 2: Hoàn thành; 3: Đã hủy bỏ  
-- [Proc_SA_Update_OrderStatus] NULL, ',51B951DB-5BCA-4907-896F-5503553EDE91,'
-- Modified by HHSon 01.016.2016 fix bug 105423: Lấy số lượng đã giao theo tùy chọn hệ thống để cập nhật tình trạng DDH
-- vhanh edited 30.06.2017: Sửa lại việc cập nhật đơn đặt hàng phải dựa theo cả Trả lại hàng bán và Nhập kho hàng bán trả lại (CR 12690)
-- =============================================

DECLARE				@RefID UNIQUEIDENTIFIER
DECLARE				@ListOrderID NVARCHAR(MAX)
DECLARE				@IsFollowSAVoucher BIT		--1: lấy từ CT bán hàng, 0: lấy từ Phiếu xuất kho

SET			@RefID=NULL
SET			@ListOrderID=N',e71e283a-fe7b-4c1f-9e41-214298e897b0,'
SET			@IsFollowSAVoucher=1

    BEGIN  


/*============== CẬP NHẬT TÌNH TRẠNG ĐƠN HÀNG ======================================*/

 --Bảng chứa các [ĐƠN HÀNG] từ chứng từ được Thêm/Sửa/Xóa  
        DECLARE @detail TABLE
            (
              Row_ID INT IDENTITY(1, 1) ,
              RefID UNIQUEIDENTIFIER ,
              OrderID UNIQUEIDENTIFIER
            )    
        INSERT  INTO @detail
                SELECT DISTINCT
                        ID.RefID ,
                        ID.OrderID
                FROM    dbo.SAVoucherDetail ID
                WHERE   ID.RefID = @RefID						
                UNION ALL
                SELECT DISTINCT
                        OD.RefID ,
                        OD.OrderID
                FROM    dbo.INOutwardDetail OD
                WHERE   OD.RefID = @RefID 						
		
		--Lấy cả ID Đơn hàng đã Xóa dòng/Bỏ chọn
		IF @ListOrderID IS NOT NULL AND @ListOrderID <> ''
		BEGIN
			INSERT INTO @detail
				SELECT NULL, Value FROM dbo.Func_ConvertGUIStringIntoTable(@ListOrderID, ',')
		END

        DECLARE @iMax INT ,
            @i INT  
        SET @iMax = @@ROWCOUNT  
        SET @i = 1   

  
 
 --SELECT * FROM @detail

 --Cập nhật các HĐB bị ảnh hưởng từ CT bán hàng  
        WHILE @i <= @iMax 
            BEGIN  
                DECLARE @OrderID UNIQUEIDENTIFIER  
                SET @OrderID = ( SELECT OrderID
                                 FROM   @detail
                                 WHERE  Row_ID = @i
                               )    
				
				/*Nếu ĐĐH chưa Hủy bỏ thì mới cập nhật lại Tình trạng*/
				IF (SELECT TOP 1 ([Status]) FROM dbo.SAOrder WHERE RefID = @OrderID) <> 3
				BEGIN
					DECLARE @Quantity DECIMAL(22,8) , /*Tổng số lượng yêu cầu*/
							@DeliveredQuatity DECIMAL(22,8)  /*Tổng số lượng đã giao*/ 
					SELECT  @Quantity = SUM(Quantity) ,
							@DeliveredQuatity = SUM(CASE @IsFollowSAVoucher WHEN 1 THEN QuantityDeliveredSA ELSE QuantityDeliveredIN END)
					FROM    dbo.SAOrderDetail
					WHERE   RefID = @OrderID
				
					DECLARE @CountSelectedRow INT /*Tổng số dòng Detail được chọn trên CT*/
					-- Edit by HHSon 01.016.2016 fix bug 105423: Lấy số lượng đã giao theo tùy chọn hệ thống
					-- vhanh edited 30.06.2017: Sửa lại việc cập nhật đơn đặt hàng phải dựa theo cả Trả lại hàng bán và Nhập kho hàng bán trả lại (CR 12690)
					IF @IsFollowSAVoucher = 1
						SET @CountSelectedRow = (SELECT COUNT(*) FROM dbo.SAVoucherDetail WHERE OrderID = @OrderID) +
												 (SELECT COUNT(*) FROM dbo.SAReturnDetail WHERE OrderID = @OrderID )
					ELSE
						SET @CountSelectedRow = (SELECT COUNT(*) FROM dbo.INOutwardDetail WHERE OrderID = @OrderID) +
												(SELECT COUNT(*) FROM dbo.INInwardDetail WHERE OrderID = @OrderID )

					-- End of Edit by HHSon 01.016.2016 fix bug 105423: Lấy số lượng đã giao theo tùy chọn hệ thống
					DECLARE @IsChoosedZeroRow BIT /*Flag là đã chọn hết các dòng có SLYC = 0*/            
					DECLARE @CountZeroRow INT /*Số dòng có SLYC = 0*/
					SET @CountZeroRow = (SELECT COUNT(*) FROM dbo.SAOrderDetail WHERE RefID = @OrderID AND Quantity = 0)
					IF @CountZeroRow = 0
						--Không có dòng số lượng = 0 thì cũng coi như đã chọn hết
						SET @IsChoosedZeroRow = 1
					ELSE
					BEGIN             
						DECLARE @CountSelectedZeroRow INT /*Tổng số dòng có SLYC = 0 được chọn trên CT*/
						-- Edit by HHSon 01.016.2016 fix bug 105423: Lấy số lượng đã giao theo tùy chọn hệ thống
						IF @IsFollowSAVoucher = 1
							SET @CountSelectedZeroRow = (SELECT COUNT(*) FROM dbo.SAOrderDetail OD INNER JOIN dbo.SAVoucherDetail VD ON OD.RefDetailID = VD.SAOrderRefDetailID 
														 WHERE OD.RefID = @OrderID AND OD.Quantity = 0)                   
						ELSE
							SET @CountSelectedZeroRow = (SELECT COUNT(*) FROM dbo.SAOrderDetail OD INNER JOIN dbo.INOutwardDetail ID ON OD.RefDetailID = ID.SAOrderRefDetailID 
														 WHERE OD.RefID = @OrderID AND OD.Quantity = 0)
						-- End of Edit by HHSon 01.016.2016 fix bug 105423: Lấy số lượng đã giao theo tùy chọn hệ thống	
						IF @CountZeroRow = @CountSelectedZeroRow
							SET @IsChoosedZeroRow = 1
						ELSE
							SET  @IsChoosedZeroRow = 0                  
					END 
				
					--SELECT @CountSelectedRow
					--Nếu không có dòng nào được chọn thì set là "Chưa thực hiện"
					IF @CountSelectedRow = 0             
						UPDATE dbo.SAOrder SET [Status] = 0 WHERE RefID = @OrderID  
					ELSE
						BEGIN
							-- Nếu số tổng lượng yêu cầu > 0 thì đi so sánh SLYC và SL đã giao ở từng dòng VTHH
							IF @Quantity > 0 
								BEGIN
									--Biến đếm số VTHH chưa giao hết
									DECLARE @CountDiffQuantity INT
									SELECT	@CountDiffQuantity = COUNT(*) FROM	dbo.SAOrderDetail WHERE	RefID = @OrderID AND Quantity > (CASE @IsFollowSAVoucher WHEN 1 THEN QuantityDeliveredSA ELSE QuantityDeliveredIN END)
									--SELECT @OrderID
									--Nếu còn mặt hàng chưa giao thì tình trạng là "Đang thực hiện"
									IF (@CountDiffQuantity > 0 OR (@CountDiffQuantity = 0 AND @IsChoosedZeroRow = 0))
										UPDATE dbo.SAOrder SET [Status] = 1 WHERE RefID = @OrderID  
									ELSE --Ngược lại thì tình trạng là "Hoàn thành"
										UPDATE dbo.SAOrder SET [Status] = 2 WHERE RefID = @OrderID          
								END        
							ELSE -- Nếu số tổng lượng yêu cầu = 0 thì kiểm tra các dòng chi tiết ĐĐH đã được chọn hết chưa
								BEGIN  
									IF @CountZeroRow = @CountSelectedZeroRow
										UPDATE dbo.SAOrder SET [Status] = 2 WHERE RefID = @OrderID  
									ELSE
										UPDATE dbo.SAOrder SET [Status] = 1 WHERE RefID = @OrderID                                 
								END        
						END
				END

				SET @i = @i + 1  
            END    
  
    END  