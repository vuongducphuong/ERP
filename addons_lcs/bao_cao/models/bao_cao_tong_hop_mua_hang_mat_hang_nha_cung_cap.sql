SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		NTGIANG
-- Create date: 15.10.2014
-- Description:	<Mua hàng: Lấy số liệu tổng hợp mua hàng theo mặt hàng và nhà cung cấp>
/*hoant 27.09.2017 bổ sung Tên nhóm VTHH theo cr  143327*/
-- =============================================

 DECLARE   @FromDate DATETIME 
 DECLARE   @ToDate DATETIME 
 DECLARE   @BranchID UNIQUEIDENTIFIER  -- Chi nhánh
 DECLARE   @IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
 DECLARE   @InventoryItemID NVARCHAR(MAX)  -- Danh sách hàng hóa, 
 DECLARE   @AccountObjectID NVARCHAR(MAX)  -- Danh sách nhà cung cấp,
 DECLARE   @IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?    

									SET					 @FromDate = '2018-01-01 00:00:00'
                                    SET                     @ToDate = '2018-12-31 23:59:59'
                                    SET                     @BranchID = '9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
                                    SET                     @IncludeDependentBranch = 1
                                    SET                     @InventoryItemID = N',692b1e73-c711-4e1f-b8f6-ce0bc68f0641,2511f940-4a9a-47ed-9e4d-19774617e38c,c371f226-dcd2-46b2-b72d-6b2a38705b95,861be9cf-2e42-474f-910c-f5cc676b70df,a5e962f2-abb1-4eeb-b804-2643a431a5a1,854f8dae-d57b-4fde-a8ee-316e35bf05c1,91477af2-d05a-4578-a4f3-8f77e8d4a00c,79fb4c6b-0c4f-43cf-939d-23de9e5628fa,3a6d8b3e-0cab-4f2b-ba91-f307ba8bd461,14895c47-39eb-4827-bac1-cb1dc3f891e5,acf8a6cb-330b-4460-a8d0-316d4a09c1c1,efb8618b-ce0b-4aec-8145-f5687544fcd2,11b760c0-13ab-41f3-8d94-68513cf20bbd,c9386f9b-6cba-4e1a-abb6-f6391d4cc9ad,c5d407f8-0ba9-4d77-8085-d08b7eff1333,7ea8eda8-ab0a-4a26-9158-3b8b1303e2bc,af52ea5b-e0c2-434c-b3fc-58d811d3360c,b3768e74-4b90-4781-93dd-bfa6f6bdabfe,945550d2-3764-4b6f-b4ae-e040900d7ae0,a7163c71-e8fb-4bd5-984f-7e799bd61e4b,a2e72fd0-b25c-4aeb-9b85-9c2904ffaf93,d304a03c-ec90-4708-9d1a-38318ba45990,e5a7407c-8933-4998-a265-3331f19845c0,cca4caa5-58b6-40e1-92e3-60cf1d85cb95,113ece0c-8668-409a-b1c4-7026f0645a04,20646216-9b81-4e1b-8ab4-ec1e423db7b3,4bb9f0d8-360e-488b-b1aa-9ff424e8f160,c511bacf-bb72-4cbe-96b7-fdf930d28420,ba10e289-cbdd-4cb5-8e18-18b29905ac06,b49ea9bc-4aa2-42b4-934e-f2b64a066cdb,48eae925-541d-4959-af15-2cb14a39bfb0,25aeb054-f23d-4f80-857c-91c8c546763d,13b27260-a6cd-4957-a35f-c553043fdeb7,399b59fc-b102-42c1-8283-20940be8c762,7ab944b3-e882-4979-9ab8-78089e1ef3c6,7fa16a89-2688-4559-aeae-7c1636529d96,e215e0bd-6fa4-4bbd-b9a1-c3e438998ad4,f8041a60-334d-4799-9aac-801abb6d1220,85b71c88-d3e0-4c72-8825-bb51fed46930,32fe06c0-ded7-4a1e-bf61-50046c5a7738,0b3a4b93-c785-41ae-b75d-64fd2cb46f7e,adc99eeb-0816-4835-97d3-84885032d591,f3b724bb-5113-40b6-98d7-027f1e63153a,29ff19fb-782e-4b2a-9e29-beb1dd375bac,672f7914-5251-4a66-8fb3-2be309299a59,e630ff76-d1c2-4d80-a496-75ad280b3612,'
                                    SET                     @AccountObjectID = N',c554d748-863d-4fc1-be5e-b69597484cfd,410c0ed4-9d79-49d1-94e4-5f33361b1700,917326b1-341c-4033-a26e-9775f4d53aba,64b0bb0b-21b2-4e77-bc04-3f0cfc381919,2e836ef6-6260-4614-92e2-2504ed7e78d0,fb69f827-cbee-4d19-bd88-70c13cc11a17,5f81fa81-e2e8-4e23-899f-57ef9673f979,2b981d5a-5791-4180-a13a-9adb94e15073,4d77cdbb-d6cb-474a-8fe8-23956a7a973b,fc834cd6-5e59-4b1a-81de-9a5af2912b49,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,271f6a73-40af-470d-8ff9-cc7cbe0a441a,5da22504-5319-47f0-8a80-ccab3c0c8360,2ea65716-13d0-4aea-9506-e8ce4e0ded39,09481017-3587-4264-90c0-7af2bb9ba548,8cb2c171-c3a4-40cc-8dec-b6632fc4c16b,8b0ba43a-1120-4574-905d-e2abff045f13,'
                                    SET                     @IsWorkingWithManagementBook = 0


    BEGIN
        DECLARE @tblListBrandID TABLE -- Bảng chứa danh sách chi nhánh
            (
              BranchID UNIQUEIDENTIFIER ,
              BranchCode NVARCHAR(128)
            )	
       
        INSERT  INTO @tblListBrandID --TMP_LIST_BRAND
                SELECT  FGDBBI.BranchID ,
                        FGDBBI.BranchCode
                FROM    dbo.Func_GetDependentByBranchID(@BranchID,
                                                        @IncludeDependentBranch)
                        AS FGDBBI           
		                          
        DECLARE @tblListInventoryItemID TABLE -- Bảng chứa danh sách hàng hóa --DS_HANG_HOA
            (
              InventoryItemID UNIQUEIDENTIFIER,
			  InventoryItemType INT
            ) 
        INSERT  INTO @tblListInventoryItemID
                SELECT  II.InventoryItemID,
						II.InventoryItemType
                FROM    dbo.Func_ConvertGUIStringIntoTable(@InventoryItemID,
                                                           ',') AS LII
                        INNER JOIN dbo.InventoryItem AS II ON II.InventoryItemID = LII.Value

		
        IF @AccountObjectID = ',' -- Nếu không chọn NCC nào -> lấy hết--NHA_CUNG_CAP_IDS
            BEGIN
                SELECT  ROW_NUMBER() OVER ( ORDER BY PL.InventoryItemCode , II.InventoryItemName , PL.AccountObjectCode , PL.AccountObjectNameDI ) AS RowNum ,
                        PL.InventoryItemID , --MA_HANG_ID
                        PL.InventoryItemCode , -- Mã hàng --MA_HANG
                        II.InventoryItemName , -- Tên hàng--TEN_HANG
                        PL.AccountObjectCode , -- Mã NCC --MA_DOI_TUONG
                        PL.AccountObjectID , --DOI_TUONG_ID
                        PL.AccountObjectNameDI , -- Tên NCC --TEN_DOI_TUONG
                        (CASE LII.InventoryItemType WHEN 2 THEN U.UnitName ELSE MU.UnitName END) AS MainUnitName , -- Tên ĐVC--DON_VI_TINH_CHINH
						SUM(PL.MainQuantity) AS MainQuantity , -- Số lượng mua theo ĐVC --SO_LUONG_MUA
                        SUM(PL.PurchaseAmount) AS PurchaseAmount , -- Giá trị mua --GIA_TRI_MUA
                        SUM(PL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu --SO_TIEN_CHIET_KHAU
                        SUM(PL.ReturnMainQuantity) AS ReturnMainQuantity , -- Số lượng trả lại theo ĐVT chính--SO_LUONG_TRA_LAI    
                        SUM(PL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại --GIA_TRI_TRA_LAI
                        SUM(PL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá--  GIA_TRI_GIAM_GIA
                        SUM(PL.PurchaseAmount - PL.DiscountAmount
                            - PL.ReturnAmount - PL.ReduceAmount) AS TotalPurchaseAmount , --Tổng giá trị mua --TONG_GIA_TRI_MUA
                        II.InventoryItemCategoryCode AS InventoryItemCategoryCode ,
                        II.InventoryItemCategoryName,
                        --[dbo].[Func_GetInventoryCategoryListName](II.InventoryItemCategoryCode) AS InventoryItemCategoryName , -- tên nhóm VTHH	                 
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC	  
                        /*hoant 27.09.2017 bổ sung Tên nhóm VTHH theo cr  143327*/
                        ,II.InventoryItemCategoryName
                FROM    dbo.PurchaseLedger AS PL --so_mua_hang_chi_tiet
                        INNER JOIN @tblListBrandID AS TLB ON PL.BranchID = TLB.BranchID --TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN @tblListInventoryItemID AS LII ON PL.InventoryItemID = LII.InventoryItemID --DS_HANG_HOA AS LII ON PL."MA_HANG_ID" = LII."MA_HANG_ID"
                        INNER JOIN dbo.InventoryItem AS II ON LII.InventoryItemID = II.InventoryItemID --danh_muc_vat_tu_hang_hoa AS II ON LII."MA_HANG_ID" = II."id"
                        LEFT JOIN dbo.AccountObject AS AO ON PL.AccountObjectID = AO.AccountObjectID -- Khách hàng, NCC, NV -> NCC, KH, Cán bộ --res_partner AS AO ON PL."DOI_TUONG_ID" = AO.id        
                        LEFT JOIN dbo.Unit AS MU ON PL.MainUnitID = MU.UnitID AND LII.InventoryItemType <> 2 -- Danh mục ĐVT -> ĐVT chính --danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU."id" AND LII."TINH_CHAT" <> '2'
						LEFT JOIN dbo.Unit AS U ON PL.UnitID = U.UnitID AND LII.InventoryItemType = 2 --danh_muc_don_vi_tinh AS U ON PL."DVT_ID" = U."id" AND LII."TINH_CHAT" = '2'
                WHERE   PL.PostedDate BETWEEN @FromDate AND @ToDate -- PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                        AND PL.IsPostToManagementBook = @IsWorkingWithManagementBook
                GROUP BY PL.InventoryItemID ,--MA_HANG_ID
                        PL.AccountObjectID ,--DOI_TUONG_ID
                        PL.InventoryItemCode , -- Mã hàng--MA_HANG
                        II.InventoryItemName , -- Tên hàng --TEN
                        PL.AccountObjectCode , -- Mã NCC --MA_DOI_TUONG
                        PL.AccountObjectNameDI , -- Tên NCC --TEN_DOI_TUONG
                        CASE LII.InventoryItemType WHEN 2 THEN PL.UnitID ELSE PL.MainUnitID END , -- Nếu là dịch vụ thì nhóm theo ĐVT--LII."TINH_CHAT" WHEN '2' THEN PL."DVT_ID" ELSE PL."DVT_CHINH_ID"
						CASE LII.InventoryItemType WHEN 2 THEN U.UnitName ELSE MU.UnitName END , -- Tên ĐVT--LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH"
						II.InventoryItemCategoryCode ,
						II.InventoryItemCategoryName,
                        --[dbo].[Func_GetInventoryCategoryListName](II.InventoryItemCategoryCode) ,
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode)
                        /*hoant 27.09.2017 bổ sung Tên nhóm VTHH theo cr  143327*/
                        ,II.InventoryItemCategoryName
                --ORDER BY PL.InventoryItemCode , -- Mã hàng
                --        LII.InventoryItemName , -- Tên hàng
                --        PL.AccountObjectCode , -- Mã NCC
                --        PL.AccountObjectNameDI  -- Tên NCC
            END
        ELSE 
            BEGIN
                DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách các NCC
                    (
                      AccountObjectID UNIQUEIDENTIFIER
                    ) 
                INSERT  INTO @tblListAccountObjectID --DS_NHA_CUNG_CAP
                        SELECT  *
                        FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                              ',')
						
                SELECT  ROW_NUMBER() OVER ( ORDER BY PL.InventoryItemCode , PL.InventoryItemName , PL.AccountObjectCode , PL.AccountObjectNameDI ) AS RowNum ,
                        PL.InventoryItemID ,
                        PL.InventoryItemCode , -- Mã hàng
                        PL.InventoryItemName , -- Tên hàng
                        PL.AccountObjectID ,
                        PL.AccountObjectCode , -- Mã NCC
                        PL.AccountObjectNameDI , -- Tên NCC
                        (CASE LII.InventoryItemType WHEN 2 THEN U.UnitName ELSE MU.UnitName END) AS MainUnitName , -- Tên ĐVC
						SUM(PL.MainQuantity) AS MainQuantity , -- Số lượng mua theo ĐVC
                        SUM(PL.PurchaseAmount) AS PurchaseAmount , -- Giá trị mua
                        SUM(PL.DiscountAmount) AS DiscountAmount , -- Tiền chiết khấu
                        SUM(PL.ReturnMainQuantity) AS ReturnMainQuantity , -- Số lượng trả lại theo ĐVT chính    
                        SUM(PL.ReturnAmount) AS ReturnAmount , -- Giá trị trả lại
                        SUM(PL.ReduceAmount) AS ReduceAmount , -- Giá trị giảm giá  
                        SUM(PL.PurchaseAmount - PL.DiscountAmount
                            - PL.ReturnAmount - PL.ReduceAmount) AS TotalPurchaseAmount , --Tổng giá trị mua    
                        II.InventoryItemCategoryCode AS InventoryItemCategoryCode ,
                        II.InventoryItemCategoryName,
                        --[dbo].[Func_GetInventoryCategoryListName](II.InventoryItemCategoryCode) AS InventoryItemCategoryName , -- tên nhóm VTHH	                 
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC	                  
                        /*hoant 27.09.2017 bổ sung Tên nhóm VTHH theo cr  143327*/
                        ,II.InventoryItemCategoryName
                FROM    dbo.PurchaseLedger AS PL --so_mua_hang_chi_tiet
                        INNER JOIN @tblListBrandID AS TLB ON PL.BranchID = TLB.BranchID--TMP_LIST_BRAND AS TLB ON PL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
                        INNER JOIN @tblListInventoryItemID AS LII ON PL.InventoryItemID = LII.InventoryItemID--DS_HANG_HOA AS LII ON PL."MA_HANG_ID" = LII."MA_HANG_ID"
                        INNER JOIN dbo.InventoryItem AS II ON LII.InventoryItemID = II.InventoryItemID--danh_muc_vat_tu_hang_hoa AS II ON LII."MA_HANG_ID" = II."id"
                        INNER JOIN @tblListAccountObjectID AS LAO ON PL.AccountObjectID = LAO.AccountObjectID --DS_NHA_CUNG_CAP AS LAO ON PL."DOI_TUONG_ID" = LAO.id
                        INNER JOIN dbo.AccountObject AS AO ON LAO.AccountObjectID = AO.AccountObjectID --res_partner AS AO ON LAO."id" = AO.id
                        LEFT JOIN dbo.Unit AS MU ON PL.MainUnitID = MU.UnitID AND LII.InventoryItemType <> 2 -- Danh mục ĐVT -> ĐVT chính --danh_muc_don_vi_tinh AS MU ON PL."DVT_CHINH_ID" = MU."id" AND LII."TINH_CHAT" <> '2'
						LEFT JOIN dbo.Unit AS U ON PL.UnitID = U.UnitID AND LII.InventoryItemType = 2 --danh_muc_don_vi_tinh AS U ON PL."DVT_ID" = U."id" AND LII."TINH_CHAT" = '2'
                WHERE   PL.PostedDate BETWEEN @FromDate AND @ToDate --PL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                        AND PL.IsPostToManagementBook = @IsWorkingWithManagementBook
                GROUP BY PL.InventoryItemID , --MA_HANG_ID
                        PL.InventoryItemCode , -- Mã hàng  --MA_HANG
                        PL.InventoryItemName , -- Tên hàng--TEN
                        PL.AccountObjectID ,--DOI_TUONG_ID
                        PL.AccountObjectCode , -- Mã NCC --MA_DOI_TUONG
                        PL.AccountObjectNameDI , -- Tên NCC --TEN_DOI_TUONG
                        CASE LII.InventoryItemType WHEN 2 THEN PL.UnitID ELSE PL.MainUnitID END , -- Nếu là dịch vụ thì nhóm theo ĐVT --LII."TINH_CHAT" WHEN '2' THEN PL."DVT_ID" ELSE PL."DVT_CHINH_ID"
						CASE LII.InventoryItemType WHEN 2 THEN U.UnitName ELSE MU.UnitName END , -- Tên ĐVT --LII."TINH_CHAT" WHEN '2' THEN U."DON_VI_TINH" ELSE MU."DON_VI_TINH"
						II.InventoryItemCategoryCode ,
						II.InventoryItemCategoryName,
                        --[dbo].[Func_GetInventoryCategoryListName](II.InventoryItemCategoryCode) , -- tên nhóm VTHH	                 
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode)  -- tên nhóm NCC	 
                        /*hoant 27.09.2017 bổ sung Tên nhóm VTHH theo cr  143327*/
                        ,II.InventoryItemCategoryName
                --ORDER BY PL.InventoryItemCode , -- Mã hàng
                --        PL.InventoryItemName , -- Tên hàng
                --        PL.AccountObjectCode , -- Mã NCC
                --        PL.AccountObjectNameDI  -- Tên NCC												   
            END
    END
    


GO