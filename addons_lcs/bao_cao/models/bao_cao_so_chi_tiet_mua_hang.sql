SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		<HHSon>
-- Create date: <02/07/2014>
-- Description:	<Mua hàng: Lấy số liệu sổ chi tiết mua hàng>
-- Modified By NTGIANG 20.09.2014 Sửa lại tham số và cách lấy dữ liệu
-- [dbo].[Proc_PUR_GetPUDetailPurchaseByInventoryItem] '9/1/2014', '9/20/2014', '02fa2e49-bf0d-4352-8405-c860c8135e93', 1, ',ab832484-c2b4-4dd0-b7e6-1c7d23b07a98,ad2093ec-bd34-4ee5-94f6-32387efdeed2,', ',772434ec-2104-4fa4-82a9-aa6021b3b06c,891977a4-7c2f-4181-b7ce-7659ee6d4cc9,', NULL, 1
-- Modified by HHSON 03.04.2015: Lấy thêm mã nhóm VTHH, Tên nhóm VTHH
-- Modify by nvtoan 11/08/2015: Bổ sung thông tin diễn giải trên master
-- Modified by VHAnh 23.11.2015: Bổ sung thêm thông tin Mã công trình, Tên công trình 
/*
* Modified by LVDIEP 13/08/2016 : Bổ sung thêm các thông tin  cho báo cáo "Sổ chi tiết mua hàng" (theo CR113515)
* PL.ExchangeRate -- Tỷ giá hối đoái
* PL.UnitPriceOC -- Đơn giá nguyên tệ (Trường hợp giảm giá hàng mua thì đơn giá bằng 0
* PL.PurchaseAmountOC -- Giá trị mua nguyên tệ
* PL.DiscountAmountOC -- Chiết khấu nguyên tệ
* PL.ReturnAmountOC -- Giá trị trả lại nguyên tệ
* PL.ReduceAmountOC	-- Giá trị giảm giá nguyên tệ
* PL.VATAmountOC -- Thuế GTGT nguyên tệ (Trường hợp chứng từ mua hàng nhập khẩu giá trị thuế GTGT = 0)
Modified by: ptphuong2 24/11/2016 lấy tiền thuế Nk và tiền thuế nk NT- Chỉ lấy thuế NK với các chứng từ mua hàng nhập khẩu (PBI 18460)
Modified by:--PTPHUONG2 02/12/2016 LẤY Định dạng số: Số chữ số phần thập phân của số tiền (nguyên tệ - sửa bug 20848)
*/ 
-- Modifide by NHYEN 21/7/2017 (CR 119782 - 122146): Lấy thêm thông tin số lô, hạn sử dụng và các thông tin hạch toán
/*hoant 19.09.2017 theo cr 137225, cr 137227, cr 137224*/
/*hoant 31.10.2017 lấy tên nhóm NCC trong danh mục thay cho function tối ưu
   bổ sung cột InventoryItemSource theo cr  150433
*/
-- =============================================

		DECLARE	@FromDate DATETIME 
		DECLARE	@ToDate DATETIME 
		DECLARE	@BranchID UNIQUEIDENTIFIER  -- Chi nhánh
		DECLARE	@IncludeDependentBranch BIT  -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
		DECLARE	@InventoryItemID NVARCHAR(MAX)  -- Danh sách hàng hóa, VD: ",6c9abe42-fbaf-4157-8b2a-10a031cd48dc, 201770d3-8664-4c98-ab0f-fed9af5a89b1,"  
		DECLARE	@AccountObjectID NVARCHAR(MAX)  -- Danh sách NCC, VD: ",46bcdea7-49f5-4190-9370-2e5e70c63928, 7473ea5b-bbe2-4de9-b491-fa457bce7466,"  nếu không chọn NCC nào thì là ','
		DECLARE	@EmployeeID UNIQUEIDENTIFIER = NULL -- Nhân viên mua hàng 
		DECLARE	@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


		SET		@FromDate = '2018-01-01 00:00:00'
       SET                                         @ToDate = '2018-12-31 23:59:59'
       SET                                         @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
       SET                                         @IncludeDependentBranch = 1
       SET                                         @InventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,c9386f9b-6cba-4e1a-abb6-f6391d4cc9ad,c5d407f8-0ba9-4d77-8085-d08b7eff1333,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,d304a03c-ec90-4708-9d1a-38318ba45990,e5a7407c-8933-4998-a265-3331f19845c0,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,4bb9f0d8-360e-488b-b1aa-9ff424e8f160,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,13b27260-a6cd-4957-a35f-c553043fdeb7,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
       SET                                         @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,2ea65716-13d0-4aea-9506-e8ce4e0ded39,'
       SET                                         @EmployeeID = NULL
       SET                                         @IsWorkingWithManagementBook = 0

    BEGIN
        DECLARE @tblListBrandID TABLE -- Bảng chứa danh sách chi nhánh
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(128) ,
              BranchName NVARCHAR(128)
            )	
       
        INSERT  INTO @tblListBrandID
                SELECT  FGDBBI.BranchID ,
                        FGDBBI.BranchCode ,
                        BranchName
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI           
		                          
        DECLARE @tblListInventoryItemID TABLE -- Bảng chứa danh sách hàng hóa
            (
              InventoryItemID UNIQUEIDENTIFIER
            ) 
        IF @InventoryItemID IS NULL -- Trường hợp drilldown
            INSERT  INTO @tblListInventoryItemID
                    SELECT  InventoryItemID
                    FROM    dbo.InventoryItem
        ELSE
            INSERT  INTO @tblListInventoryItemID
                    SELECT  *
                    FROM    dbo.Func_ConvertGUIStringIntoTable(@InventoryItemID,
                                                              ',')	
        
        --PTPHUONG2 02/12/2016 LẤY Định dạng số: Số chữ số phần thập phân của số tiền (nguyên tệ - sửa bug 20848)
        
        DECLARE @amountOCDecimalDigits INTEGER
        SELECT  @amountOCDecimalDigits = CAST(OptionValue AS INTEGER)
        FROM    dbo.SYSDBOption
        WHERE   OptionID = 'AmountOCDecimalDigits'
                
		-- Chia luồng theo @AccountObjectID, lấy tất hay chỉ lấy theo những NCC đã chọn, để tăng performance                                                          
		-- tthoa add 13/11/2014 : thêm xét điều kiện @AccountObjectID NULL trong trường hợp drilldown
        IF @AccountObjectID IS NULL
            OR @AccountObjectID = ',' -- Nếu lấy tất 
            BEGIN		
            /*hoant 19.09.2017 theo cr 137227 bổ sung thêm PL.SortOrder */                                  		
                SELECT  ROW_NUMBER() OVER ( ORDER BY PL.PostedDate , PL.RefDate , PL.RefNo , PL.InvDate , PL.InvNo,PL.SortOrder ) AS RowNum ,
                        PL.RefID ,--ID_CHUNG_TU
                        PL.PurchaseLedgerID , -- PK-- 
                        PL.PostedDate ,-- Ngày hạch toán --NGAY_HACH_TOAN
                        PL.RefDate ,-- Ngày chứng từ --NGAY_CHUNG_TU
                        PL.RefNo ,-- Số chứng từ --SO_CHUNG_TU
                        PL.InvDate ,-- Ngày hóa đơn --NGAY_HOA_DON
                        PL.InvNo ,-- Số hóa đơn --SO_HOA_DON
                        PL.JournalMemo , --DIEN_GIAI_CHUNG
                        PL.Description , -- Diễn giải chi tiết --DIEN_GIAI
                        PL.AccountObjectCode , -- Mã NCC -- MA_DOI_TUONG
                        PL.AccountObjectName , -- Tên NCC --TEN_DOI_TUONG
                        PL.InventoryItemCode , -- Mã hàng --MA_HANG
                        PL.InventoryItemName , -- Tên hàng --TEN_HANG
                        UN.UnitName , -- Tên ĐVT --DON_VI_TINH
                        PL.PurchaseQuantity , -- Số lượng --SO_LUONG
                        --LVDIEP 13/08/2016: Sửa theo yêu cầu mở rộng của CR113151: Trường hợp giảm giá hàng mua thì đơn giá bằng 0
                        CASE WHEN PL.RefType IN ( 3040, 3041, 3042, 3043, 3402 )
                             THEN 0
                             ELSE PL.UnitPrice -- Đơn giá quy đổi
                        END AS UnitPrice , --DON_GIA
                        --PL.UnitPrice , -- Đơn giá quy đổi
                        MU.UnitName AS MainUnitName , --TEN_DON_VI_TINH
                        PL.MainConvertRate , -- Tỷ lệ chuyển đổi
                        PL.MainQuantity , -- Số lượng mua theo ĐVC
                        PL.MainUnitPrice , -- Đơn giá theo ĐVC
                        PL.PurchaseAmount , -- Thành tiền --SO_TIEN
                        PL.DiscountAmount , -- Tiền chiết khấu --SO_TIEN_CHIET_KHAU
						--- Trả lại
                        PL.ReturnQuantity , -- Số lượng trả lại --SO_LUONG_TRA_LAI
                        PL.ReturnMainQuantity , -- Số lượng trả lại theo ĐVT chính    
                        PL.ReturnAmount , -- Giá trị trả lại --SO_TIEN_TRA_LAI
						-- Giảm giá (Bảng PUDiscount nhưng lấy từ trường Reduce =)) )
                        PL.ReduceAmount , -- Giá trị giảm giá       --SO_TIEN_GIAM_TRU        
                           /*hoant 19.09.2017 theo cr 137224*/
						CASE WHEN PL.IncludeInvoice=1 then
							PL.VATAmount 
						ELSE
							CASE WHEN I.refID IS NOT NULL THEN PUI.VATAmount ELSE 0 end							
						END	AS VATAmount, -- Thuế GTGT (khi chứng từ là Trả lại hàng mua, Giảm giá hàng mua thì đã đẩy giá trị âm khi ghi sổ)                             
                        CASE WHEN PL.RefType IN (3030,3031,3032,3033,3040,3041,3042,3043)
								THEN PL.CreditAccount --MA_TK_CO
							ELSE PL.DebitAccount --MA_TK_NO
						END AS DebitAccount , -- TK Nợ: nhyen_21/7/2017_CR122146 --MA_TK_NO
                        CASE WHEN PL.RefType IN (3030,3031,3032,3033,3040,3041,3042,3043)
								THEN PL.DebitAccount --MA_TK_NO
							ELSE PL.CreditAccount --MA_TK_CO
						END AS CreditAccount , -- TK Có: nhyen_21/7/2017_CR122146 --MA_TK_CO
							 /*hoant 19.09.2017 theo cr 137224*/
						CASE WHEN PL.IncludeInvoice=1 then
							PL.VATAccount
						ELSE
							CASE WHEN I.refID IS NOT NULL THEN PUI.DebitAccount ELSE '' end	
						END	
                        AS VATAccount , -- TK Thuế GTGT: nhyen_21/7/2017_CR122146
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 )
                             THEN PUD.ImportTaxAccount
                             ELSE NULL
                        END AS ImportTaxAccount , -- TK thuế NK: nhyen_21/7/2017_CR122146
                        PL.LotNo , -- Số lô: nhyen_21/7/2017_CR119782
                        PL.ExpiryDate , -- Hạn sử dụng: nhyen_21/7/2017_CR119782
                        PL.EmployeeCode , -- Mã nhân viên mua hàng
                        PL.EmployeeName , -- Tên nhân viên mua hàng
                        PL.RefType , -- Mã loại chứng từ
                        PL.RefTypeName , -- Loại chứng từ
                        PO.RefNo AS OrderRefNo , -- Số đơn mua hàng
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        --[dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) 
                        /*hoant 31.10.2017 lấy tên nhóm NCC trong danh mục */
                        AO.AccountObjectGroupListName
                        AS AccountObjectCategoryName -- tên nhóm NCC	                 
                        ,
                        II.InventoryItemCategoryCode , --Mã nhóm VTHH
                        II.InventoryItemCategoryName ,
                        --[dbo].[Func_GetInventoryCategoryListName](II.InventoryItemCategoryCode) AS InventoryItemCategoryName , -- tên nhóm VTHH 
                        TLB.BranchName ,
                        LI.ListItemName ,
                        CFL.MasterCustomField1 ,
                        CFL.MasterCustomField2 ,
                        CFL.MasterCustomField3 ,
                        CFL.MasterCustomField4 ,
                        CFL.MasterCustomField5 ,
                        CFL.MasterCustomField6 ,
                        CFL.MasterCustomField7 ,
                        CFL.MasterCustomField8 ,
                        CFL.MasterCustomField9 ,
                        CFL.MasterCustomField10 ,
                        CFL.CustomField1 ,
                        CFL.CustomField2 ,
                        CFL.CustomField3 ,
                        CFL.CustomField4 ,
                        CFL.CustomField5 ,
                        CFL.CustomField6 ,
                        CFL.CustomField7 ,
                        CFL.CustomField8 ,
                        CFL.CustomField9 ,
                        CFL.CustomField10 ,
                        --DATRUONG Task 69704: Bổ sung các trường Địa chỉ NCC, số CMND, điều khoản thanh toán, mã kho, tên kho
                        AO.[Address] AS AccountObjectAddress ,
                        AO.IdentificationNumber ,
                        PL.PaymentTermCode ,
                        PL.PaymentTermName ,
                        PL.StockCode ,
                        PL.StockName   
                        -- nmtruong:10/11/2015 task 75885: Lấy lên phí trước hải quan và phí hàng về kho
                        ,
                        PL.ImportChargeAmount ,
                        PL.FreightAmount
						--vhanh added 23.11.2015
                        ,
                        PW.ProjectWorkCode ,
                        PW.ProjectWorkName ,
                        PL.CurrencyID -- Loại tiền
                        ,
                        PL.ExchangeRate -- Tỷ giá
                        ,
                        CASE WHEN PL.RefType IN ( 3040, 3041, 3042, 3043, 3402 )
                             THEN 0 -- Trường hợp giảm giá hàng mua thì đơn giá bằng 0
                             ELSE PL.UnitPriceOC -- Đơn giá nguyên tệ
                        END AS UnitPriceOC ,
                        PL.PurchaseAmountOC -- Giá trị mua nguyên tệ
                        ,
                        PL.DiscountAmountOC -- Chiết khấu nguyên tệ
                        ,
                        PL.ReturnAmountOC -- Giá trị trả lại nguyên tệ
                        ,
                        PL.ReduceAmountOC	-- Giá trị giảm giá nguyên tệ
						-- Thuế GTGT nguyên tệ (Trường hợp chứng từ mua hàng nhập khẩu (318,319,320,321,322,324,325,326,327,328,368,369,370,371,372,374,375,376,377,378) giá trị thuế GTGT = 0)
                        ,
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 ) THEN 0
                             ELSE
                               /*hoant 19.09.2017 theo cr 137224*/
								CASE WHEN PL.IncludeInvoice=1 then
									PL.VATAmountOC
								ELSE
									CASE WHEN I.refID IS NOT NULL THEN PUI.VATAmountOC ELSE 0 end									
								END	                               
                        END AS VATAmountOC ,
						  ----ptphuong2 24/11/2016 lấy tiền thuế Nk và tiền thuế nk NT chỉ lấy đối với chứng từ mua hàng nhập khẩu(PBI 18460)
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 )
                             THEN PUD.ImportTaxAmount
                             ELSE NULL
                        END AS ImportTaxAmount ,
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 )
                             THEN ROUND(PUD.ImportTaxAmountOC,
                                        @amountOCDecimalDigits) --PTPHUONG2 02/12/2016 LẤY Định dạng số: Số chữ số phần thập phân của số tiền (nguyên tệ - sửa bug 20848)
                             ELSE NULL
                        END AS ImportTaxAmountOC
                        /*hoant 19.09.2017 theo cr 137225*/
						,SAO.RefNo AS SAOrderRefNo
						/*HOANT 31.10.2017 bổ sung cột InventoryItemSource theo cr  150433*/
						,II.InventoryItemSource
                FROM    dbo.PurchaseLedger AS PL
                        INNER JOIN @tblListBrandID AS TLB ON PL.BranchID = TLB.BranchID
                        INNER JOIN @tblListInventoryItemID AS LII ON PL.InventoryItemID = LII.InventoryItemID
                        INNER JOIN dbo.InventoryItem AS II ON LII.InventoryItemID = II.InventoryItemID
                        LEFT JOIN dbo.ProjectWork AS PW ON PL.ProjectWorkID = PW.ProjectWorkID
                        LEFT JOIN dbo.AccountObject AS AO ON PL.AccountObjectID = AO.AccountObjectID -- Khách hàng, NCC, NV -> NCC, KH, Cán bộ                
                        LEFT JOIN dbo.Unit AS UN ON PL.UnitID = UN.UnitID -- Danh mục ĐVT -> ĐVT
                        LEFT JOIN dbo.Unit AS MU ON PL.MainUnitID = MU.UnitID -- Danh mục ĐVT -> ĐVT chính 
                        LEFT JOIN dbo.PUOrder AS PO ON PL.PUOrderRefID = PO.RefID -- Đơn mua hàng
                        LEFT JOIN dbo.ListItem AS LI ON PL.ListItemID = LI.ListItemID
                        LEFT JOIN dbo.CustomFieldLedger AS CFL ON PL.RefDetailID = CFL.RefDetailID
                                                              AND PL.IsPostToManagementBook = CFL.IsPostToManagementBook
                        --ptphuong2 24/11/2016 bổ sung leftjoin với bảng PUVoucherDetail để lấy tiền thuế Nk (PBI 18460) 
                        -- Chỉ lấy thuế NK với các chứng từ mua hàng nhập khẩu.
                        LEFT JOIN dbo.PUVoucherDetail PUD ON PUD.RefDetailID = PL.RefDetailID
                                                             AND PL.RefType IN (
                                                             318, 319, 320,
                                                             321, 322, 324,
                                                             325, 326, 327,
                                                             328, 368, 369,
                                                             370, 371, 372,
                                                             374, 375, 376,
                                                             377, 378 )
						/*hoant 19.09.2017 theo cr 137225*/
						LEFT JOIN dbo.SAOrder SAO ON PL.OrderID=SAO.RefID  
							/*hoant 19.09.2017 theo cr 137224*/
						LEFT JOIN PUInvoiceDetail PUI ON PUI.PUVoucherRefDetailID =PL.RefDetailID                                                                  
						LEFT JOIN dbo.PUInvoice I ON I.RefID=PUI.RefID AND ((I.IsPostedFinance=1 AND @IsWorkingWithManagementBook=0) OR (I.IsPostedManagement=1 AND @IsWorkingWithManagementBook=1))
                WHERE   PL.PostedDate BETWEEN @FromDate AND @ToDate --TU AND DEN
                        AND ( @EmployeeID IS NULL
                              OR PL.EmployeeID = @EmployeeID --NV_MUA_HANG_ID
                            )
                        AND PL.IsPostToManagementBook = @IsWorkingWithManagementBook
                OPTION  ( RECOMPILE )         
            END
        ELSE -- Nếu lấy theo những NCC đã chọn 
            BEGIN
                DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các NCC
                    (
                      AccountObjectID UNIQUEIDENTIFIER ,
                      AccountObjectGroupListCode NVARCHAR(MAX) ,
                      AccountObjectGroupListName NVARCHAR(MAX) ,
                      --DATRUONG Task 69704: Lấy số chứng minh nhân dân, địa chỉ nhà cung cấp
                      IdentificationNumber NVARCHAR(20) ,
                      AccountObjectAddress NVARCHAR(255)

                      
                    ) 
                INSERT  INTO @tblListAccountObjectID
                        SELECT  AO.AccountObjectID ,
                                AO.AccountObjectGroupListCode ,
                                ao.AccountObjectGroupListName,
                                AO.IdentificationNumber ,
                                AO.[Address] AS AccountObjectAddress
                        FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                              ',') AS LAO
                                INNER JOIN dbo.AccountObject AS AO ON LAO.Value = AO.AccountObjectID
                         /*hoant 19.09.2017 theo cr 137227 bổ sung thêm PL.SortOrder */                                  
                SELECT  ROW_NUMBER() OVER ( ORDER BY PL.PostedDate , PL.RefDate , PL.RefNo , PL.InvDate , PL.InvNo,PL.SortOrder ) AS RowNum ,
                        PL.RefID ,
                        PL.PurchaseLedgerID , -- PK
                        PL.PostedDate ,-- Ngày hạch toán
                        PL.RefDate ,-- Ngày chứng từ
                        PL.RefNo ,-- Số chứng từ 
                        PL.InvDate ,-- Ngày hóa đơn
                        PL.InvNo ,-- Số hóa đơn
                        PL.JournalMemo ,
                        PL.Description , -- Diễn giải chi tiết
                        PL.AccountObjectCode , -- Mã NCC
                        PL.AccountObjectName , -- Tên NCC
                        PL.InventoryItemCode , -- Mã hàng
                        PL.InventoryItemName , -- Tên hàng
                        UN.UnitName , -- Tên ĐVT
                        PL.PurchaseQuantity , -- Số lượng
                        --LVDIEP 13/08/2016: Sửa theo yêu cầu mở rộng của CR113151: Trường hợp giảm giá hàng mua thì đơn giá bằng 0
                        CASE WHEN PL.RefType IN ( 3040, 3041, 3042, 3043, 3402 )
                             THEN 0
                             ELSE PL.UnitPrice -- Đơn giá quy đổi
                        END AS UnitPrice ,
                        --PL.UnitPrice , -- Đơn giá quy đổi
                        MU.UnitName AS MainUnitName ,
                        PL.MainConvertRate , -- Tỷ lệ chuyển đổi
                        PL.MainQuantity , -- Số lượng mua theo ĐVC
                        PL.MainUnitPrice , -- Đơn giá theo ĐVC
                        PL.PurchaseAmount , -- Thành tiền
                        PL.DiscountAmount , -- Tiền chiết khấu
						--- Trả lại
                        PL.ReturnQuantity , -- Số lượng trả lại
                        PL.ReturnMainQuantity , -- Số lượng trả lại theo ĐVT chính    
                        PL.ReturnAmount , -- Giá trị trả lại
						 -- Giảm giá (Bảng PUDiscount nhưng lấy từ trường Reduce =)) )
                        PL.ReduceAmount , -- Giá trị giảm giá               
                          /*hoant 19.09.2017 theo cr 137224*/
						CASE WHEN PL.IncludeInvoice=1 then
							PL.VATAmount
						ELSE
							CASE WHEN I.refID IS NOT NULL THEN PUI.VATAmount ELSE 0 end									
						END	 AS VATAmount , -- Thuế GTGT (khi chứng từ là Trả lại hàng mua, Giảm giá hàng mua thì đã đẩy giá trị âm khi ghi sổ)                       
                        CASE WHEN PL.RefType IN (3030,3031,3032,3033,3040,3041,3042,3043)
								THEN PL.CreditAccount
							ELSE PL.DebitAccount
						END AS DebitAccount , -- TK Nợ: nhyen_21/7/2017_CR122146
                        CASE WHEN PL.RefType IN (3030,3031,3032,3033,3040,3041,3042,3043)
								THEN PL.DebitAccount
							ELSE PL.CreditAccount
						END AS CreditAccount , -- TK Có: nhyen_21/7/2017_CR122146
						 /*hoant 19.09.2017 theo cr 137224*/
						CASE WHEN PL.IncludeInvoice=1 then
							PL.VATAccount
						ELSE
							CASE WHEN I.refID IS NOT NULL THEN PUI.DebitAccount ELSE '' end	
						END	
                        AS VATAccount , -- TK Thuế GTGT: nhyen_21/7/2017_CR122146
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 )
                             THEN PUD.ImportTaxAccount
                             ELSE NULL
                        END AS ImportTaxAccount , -- TK thuế NK: nhyen_21/7/2017_CR122146
                        PL.LotNo , -- Số lô: nhyen_21/7/2017_CR119782
                        PL.ExpiryDate , -- Hạn sử dụng: nhyen_21/7/2017_CR119782
                        PL.EmployeeCode , -- Mã nhân viên mua hàng
                        PL.EmployeeName , -- Tên nhân viên mua hàng
                        PL.RefType , -- Mã loại chứng từ
                        PL.RefTypeName , -- Loại chứng từ
                        PO.RefNo AS OrderRefNo , -- Số đơn mua hàng
                        LAO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        --[dbo].[Func_GetAccountObjectGroupListName](LAO.AccountObjectGroupListCode)
                        /*hoant 31.10.2017 lấy tên nhóm NCC trong danh mục thay cho function*/
                         LAO.AccountObjectGroupListName AS AccountObjectCategoryName -- tên nhóm NCC	                        
                        ,
                        II.InventoryItemCategoryCode , --Mã nhóm VTHH
                        II.InventoryItemCategoryName ,
                        --[dbo].[Func_GetInventoryCategoryListName](II.InventoryItemCategoryCode) AS InventoryItemCategoryName , -- tên nhóm VTHH 
                        TLB.BranchName ,
                        LI.ListItemName ,
                        CFL.MasterCustomField1 ,
                        CFL.MasterCustomField2 ,
                        CFL.MasterCustomField3 ,
                        CFL.MasterCustomField4 ,
                        CFL.MasterCustomField5 ,
                        CFL.MasterCustomField6 ,
                        CFL.MasterCustomField7 ,
                        CFL.MasterCustomField8 ,
                        CFL.MasterCustomField9 ,
                        CFL.MasterCustomField10 ,
                        CFL.CustomField1 ,
                        CFL.CustomField2 ,
                        CFL.CustomField3 ,
                        CFL.CustomField4 ,
                        CFL.CustomField5 ,
                        CFL.CustomField6 ,
                        CFL.CustomField7 ,
                        CFL.CustomField8 ,
                        CFL.CustomField9 ,
                        CFL.CustomField10
                        --DATRUONG Task 69704: Bổ sung các trường Địa chỉ NCC, số CMND, điều khoản thanh toán, mã kho, tên kho
                        ,
                        LAO.AccountObjectAddress ,
                        LAO.IdentificationNumber ,
                        PL.PaymentTermCode ,
                        PL.PaymentTermName ,
                        PL.StockCode ,
                        PL.StockName ,
                        PL.ImportChargeAmount ,
                        PL.FreightAmount
						--vhanh added 23.11.2015
                        ,
                        PW.ProjectWorkCode ,
                        PW.ProjectWorkName ,
                        PL.CurrencyID -- Loại tiền
                        ,
                        PL.ExchangeRate -- Tỷ giá
                        ,
                        CASE WHEN PL.RefType IN ( 3040, 3041, 3042, 3043, 3402 )
                             THEN 0 -- Trường hợp giảm giá hàng mua thì đơn giá bằng 0
                             ELSE PL.UnitPriceOC -- Đơn giá nguyên tệ
                        END AS UnitPriceOC ,
                        PL.PurchaseAmountOC -- Giá trị mua nguyên tệ
                        ,
                        PL.DiscountAmountOC -- Chiết khấu nguyên tệ
                        ,
                        PL.ReturnAmountOC -- Giá trị trả lại nguyên tệ
                        ,
                        PL.ReduceAmountOC	-- Giá trị giảm giá nguyên tệ
						-- Thuế GTGT nguyên tệ (Trường hợp chứng từ mua hàng nhập khẩu (318,319,320,321,322,324,325,326,327,328,368,369,370,371,372,374,375,376,377,378) giá trị thuế GTGT = 0)
                        ,
                                                
						CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
												  325, 326, 327, 328, 368, 369,
												  370, 371, 372, 374, 375, 376,
												  377, 378 ) THEN 0
							 ELSE 
							  /*hoant 19.09.2017 theo cr 137224*/
								CASE WHEN PL.IncludeInvoice=1 then
									PL.VATAmountOC
								ELSE
									CASE WHEN I.refID IS NOT NULL THEN PUI.VATAmountOC ELSE 0 end	
								END	
						END AS VATAmountOC ,                         
							
						 ----ptphuong2 24/11/2016 lấy tiền thuế Nk và tiền thuế nk NT chỉ lấy đối với chứng từ mua hàng nhập khẩu(PBI 18460)
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 )
                             THEN PUD.ImportTaxAmount
                             ELSE NULL
                        END AS ImportTaxAmount ,
                        CASE WHEN PL.RefType IN ( 318, 319, 320, 321, 322, 324,
                                                  325, 326, 327, 328, 368, 369,
                                                  370, 371, 372, 374, 375, 376,
                                                  377, 378 )
                             THEN ROUND(PUD.ImportTaxAmountOC,
                                        @amountOCDecimalDigits) --PTPHUONG2 02/12/2016 LẤY Định dạng số: Số chữ số phần thập phân của số tiền (nguyên tệ - sửa bug 20848)
                             ELSE NULL
                        END AS ImportTaxAmountOC
						 /*hoant 19.09.2017 theo cr 137225*/
						,SAO.RefNo AS SAOrderRefNo
						/*HOANT 31.10.2017 bổ sung cột InventoryItemSource theo cr  150433*/
						,II.InventoryItemSource
                FROM    dbo.PurchaseLedger AS PL
                        INNER JOIN @tblListBrandID AS TLB ON PL.BranchID = TLB.BranchID
                        INNER JOIN @tblListAccountObjectID AS LAO ON PL.AccountObjectID = LAO.AccountObjectID
                        INNER JOIN @tblListInventoryItemID AS LII ON PL.InventoryItemID = LII.InventoryItemID
                        INNER JOIN dbo.InventoryItem AS II ON LII.InventoryItemID = II.InventoryItemID
                        LEFT JOIN dbo.ProjectWork AS PW ON PL.ProjectWorkID = PW.ProjectWorkID
                        LEFT JOIN dbo.Unit AS UN ON PL.UnitID = UN.UnitID -- Danh mục ĐVT -> ĐVT
                        LEFT JOIN dbo.Unit AS MU ON PL.MainUnitID = MU.UnitID -- Danh mục ĐVT -> ĐVT chính 
                        LEFT JOIN dbo.PUOrder AS PO ON PL.PUOrderRefID = PO.RefID -- Đơn mua hàng
                        LEFT JOIN dbo.ListItem AS LI ON PL.ListItemID = LI.ListItemID
                        LEFT JOIN dbo.CustomFieldLedger AS CFL ON PL.RefDetailID = CFL.RefDetailID
                                                              AND PL.IsPostToManagementBook = CFL.IsPostToManagementBook
                                                                 --ptphuong2 24/11/2016 bổ sung leftjoin với bảng PUVoucherDetail để lấy tiền thuế Nk (PBI 18460)
                                                                 -- Chỉ lấy thuế NK với các chứng từ mua hàng nhập khẩu.
                        LEFT JOIN dbo.PUVoucherDetail PUD ON PUD.RefDetailID = PL.RefDetailID
                                                             AND PL.RefType IN (
                                                             318, 319, 320,
                                                             321, 322, 324,
                                                             325, 326, 327,
                                                             328, 368, 369,
                                                             370, 371, 372,
                                                             374, 375, 376,
                                                             377, 378 )
						/*hoant 19.09.2017 theo cr 137225*/
						LEFT JOIN dbo.SAOrder SAO ON PL.OrderID=SAO.RefID   
						/*hoant 19.09.2017 theo cr 137224*/
						LEFT JOIN PUInvoiceDetail PUI ON PUI.PUVoucherRefDetailID =PL.RefDetailID                                                                
						LEFT JOIN dbo.PUInvoice I ON I.RefID=PUI.RefID AND ((I.IsPostedFinance=1 AND @IsWorkingWithManagementBook=0) OR (I.IsPostedManagement=1 AND @IsWorkingWithManagementBook=1))
                WHERE   PL.PostedDate BETWEEN @FromDate AND @ToDate
                        AND ( @EmployeeID IS NULL
                              OR PL.EmployeeID = @EmployeeID
                            )
                        AND PL.IsPostToManagementBook = @IsWorkingWithManagementBook
                        
                OPTION  ( RECOMPILE )
                
            END
    END
    




GO