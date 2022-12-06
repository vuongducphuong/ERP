--exec Proc_CTR_GetReceivableSummaryByContract @FromDate='2018-01-01 00:00:00',@ToDate='2018-01-15 23:59:59',@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B',@IncludeDependentBranch=1,@AccountNumber=N'131',@AccountObjectID=N',271f6a73-40af-470d-8ff9-cc7cbe0a441a,4176d066-cfbf-4661-bb69-37a5e88554bb,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,58efaebf-f074-4336-86d7-439ba11cac26,410c0ed4-9d79-49d1-94e4-5f33361b1700,2ea65716-13d0-4aea-9506-e8ce4e0ded39,4acfc6f7-a8db-4e14-89cf-52d13b483df4,be2c2d67-d658-4245-b684-a446cd7a38f9,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,',@CurrencyID=N'VND',@ContractID=N',f0ef577f-2c3d-49a1-9164-a8edba07c29f,f5c3d84b-97ed-49c5-ace6-bffcbdf1022f,cb78ef91-72ba-498e-b984-90002675ddd1,3d2186e7-3033-4313-8d47-c400a7b5af9a,62c3ff3f-cded-4a16-8387-a2820165736e,6e05231b-a2f0-4004-8c7f-73fafc1d896a,79bad869-60e7-438b-bade-f67d4c9c9b67,1cf541b9-9180-42cd-98e6-6bfcd4ca7f1e,',@IsWorkingWithManagementBook=0

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
-- =============================================
-- Author:		NVTOAN
-- Create date: 19/11/2014
-- Description:	Báo cáo Tổng hợp công nợ phải thu theo hợp đồng bán
-- nvtoan modify 15/01/2014: Xử lý chênh lệch tỷ giá, lấy thông tin hợp đồng, đối tượng trong danh mục
-- nvtoan modify 22/01/2015: Sửa lỗi chọn dự án không lấy được số liệu của hợp đồng thuộc dự án đó
--exec Proc_CTR_GetReceivableSummaryByContract @FromDate='2015-01-01 00:00:00',@ToDate='2015-01-22 23:59:50',@BranchID='AFF3B6B0-FD0D-49D8-ADD8-4F5ABB45955B',@IncludeDependentBranch=0,@AccountNumber=N'131',@AccountObjectID=N',38a9873c-db14-464a-ae83-7b4c4ad92eb2,331ee88b-f64b-437d-b904-32cbc32c5b0c,1f6c4735-eae7-47a0-8922-9ee27612b162,22ccef02-c349-4ef6-9d3a-e29843b10d80,3d2a74c6-e528-467c-8bd3-9e68faa3f173,c49a4356-5584-4af2-80c5-11e8dc19b040,5937e94c-0ab9-43ca-b530-a8fa81408c32,d143944b-f42d-471e-8ee9-ff5cd59ee624,4ee3c0bc-25dd-4417-838c-4007290d1e2a,e22bda71-c91d-4e72-82fb-c08de4890b05,90943b57-0c0e-4eba-ba67-0f7325e26659,efd5d324-bdb8-4d2b-ac05-03b32727615f,7f588dcf-d235-459b-92e7-da318dc7b608,3ef9a4e4-075b-49ef-91f2-03173fbbd037,6bf84e0b-3a4a-4d4d-82ef-c16f828e9f08,2da82d44-d822-4b61-9233-87982e15064f,b5b2d0e5-1561-456d-aa01-2fa213262c56,1f66073d-e4ad-4c25-baaa-23eabccea3fd,46aecae9-f547-4555-bdc5-28f3fd9285f5,7afda240-a70d-4678-8e67-8bd9fdd07a83,c50aac23-b69a-4f3b-8c43-5ed6078ab05e,da880080-1665-49c7-9964-8f36d9456058,d3c061a4-79ab-442b-bcdf-72fe7f4f457e,66546290-0f2a-4dee-94c5-6f1a1318669b,98d66e93-55d1-4dcb-88f3-6fcc4bddad09,76477294-6785-465b-a8d9-a8f94337087d,b9c118fc-546b-426b-afbc-21ef99185d8d,2d005b33-9fd6-4261-9f39-db0268d5a079,d5f8f543-0342-4257-8c61-cc2d34c85b9f,239ab401-3a70-405a-ade8-a45832b0c67a,7caec8ca-caae-4da9-b0ef-48cea43a1a3c,09c8b7ce-aff5-45ba-9a18-65af3fcb73d3,376e2018-f4bb-49ec-89da-a0ff2f1bfa12,ccc001f0-23db-4cf2-86f6-73950915b54a,b810ad6d-6a73-4060-a46a-80561067629a,5670d00e-c734-4900-9c49-24900128ef1e,f4eb3e77-9fd5-4d79-9385-62c3c5f7f740,0ec5f400-436d-40cf-aaa1-2292b78fea7c,771519e8-6d61-4927-a498-bc28fd2086b7,6ecf874e-4191-4d39-bf72-978407eff9fb,4cf2dcb2-020c-4ee8-bf07-7f377a31d5db,93b5587a-d215-441f-8c97-4cc2d514483d,ebc6d263-abec-4bf7-ba09-e961650b0a78,46fd6a0e-f4cd-41a3-aa00-28f5e5773fa1,e26dd308-945a-406a-815a-fa9eb7cffb69,541c248a-9912-488b-aaaf-0f99b17b8ce3,9564aba5-354a-4423-9f34-c506bdeb6b87,8e0ca5ac-3ee1-4420-9196-5fd3fa5eed17,3212bb6c-ca41-4490-bd63-9471b2b6a5d1,8766cfb2-9a8f-4fe0-9fbc-ce49dc0ef74a,03248d19-7f21-4b48-b9ab-b602b25b8edf,0c88a24f-860d-4d61-a4f5-d1be6133c06a,ac6dc451-db83-48d8-8365-4852e9c04c3b,f9fe5f99-62c1-4360-aad9-aa0ab4a6492c,dbc67737-f417-4842-9474-a77fd4b63a3f,689776a3-88e0-4da5-9caf-280ee3268671,57e722a6-6647-4fcf-bb48-b2eb01ce38ac,89b656b9-ded5-4845-9e5b-31dd4599ee53,18f69984-83f8-448b-b7f1-4b2c532794dd,c651cc2d-85aa-4e77-86f9-f4eb03b3c81e,0c7892fb-c671-48b7-b6fd-1cdb887aeeed,7c3e9d26-eec6-494a-b878-c0665d7b63d8,4ee4b338-8535-44a1-9321-a43bc9cf82e5,df91a996-831e-4bd6-8893-b224ebcf93a3,ab50acc1-5381-405d-8907-5fd408446e27,3d48da1c-f794-4c66-b3ca-ba35fa5be8f8,2d91bc91-74b5-4615-bcc7-f5c88f461e91,0011125f-ef14-4690-ac6f-9488112d24b0,ee1baf3d-6411-4dce-93d3-79a0dcd745da,078a2a50-7279-4858-ba9a-5dd1724cd6d5,dd8e5d71-a30e-4d31-9fe6-c10bf3de69cd,ba98f0af-91d9-4bf2-9658-b78e04eeade2,0cea1303-9ea0-4750-9ea8-fd415f330d83,49f04b48-f4ae-422d-993d-cffb7d8ddf64,e859ea8e-d6b2-4a71-856c-e9c4abd594da,3ccb09d7-36f0-47d5-9927-929e0d7fb0ed,62f5b47e-48ff-49c4-bbf9-a7edf557d1c1,672b66a4-8974-4248-9355-0b360480187e,ed1ad56f-57e5-4edd-8281-e8dafba77461,3f414e63-949e-4b11-bd64-58d37f641cc2,3a4f45cb-a2da-4a50-8657-e6d37f983216,807b49e6-149b-4af9-9743-6fe2d19377e4,aa765751-d159-4fe9-abb4-0967e478e0d4,258f24e8-9e28-4a35-aa9a-3d67b789b2e7,73f0ea22-dbb9-45af-ae6b-23d175634341,041b530c-4e21-41b9-9a4d-34ae1e39615f,f1f7065f-45c4-4b63-92e7-0b8b522fc3db,d329f4e5-2afc-42d4-a2a4-db90ed497318,abba27f0-9a87-4f19-9f0f-7f1b6b9308bc,428d1db1-8094-4dc2-924d-986dd1583cf3,cf9d6d21-af9a-4764-87d0-f9b09745763a,1231b465-2af0-47e2-9fa9-473ecb81148c,eccf1470-5743-4c7c-a896-3d0d15040707,6c22d154-c423-4636-9ac0-fc253a58a846,732730a3-e928-461c-9a17-2b6e760e434c,d24438dd-2b00-4a1b-aa54-70c99d06d817,1ee1f0b3-b4ec-4ec2-8ace-1e27f731f00e,b6322642-082f-48f4-9a82-2fa36246b81b,94f55d3c-fde1-45d2-8ed8-749ea5da45e4,23f13486-e191-463d-8297-3ad27d53ed3d,f4cd79c4-b1cd-464d-9e44-1cc2b8d2c120,8411435a-0beb-4301-be1a-cadf1b050c68,a0e8b70d-5af3-43a0-af70-c9c43fea0a9e,41947ffe-b631-49a2-8c1f-5fd791c1d414,194eaf70-d230-48c3-917a-a2befb20af00,949a1be7-11f6-4d49-845d-97b7c1a0f290,57a2862c-aedc-41ec-9636-2ef7c37291e1,1e932097-a609-485b-ab60-308b4b3b0262,a5f2c1bb-5722-4a5e-aba7-5556a75d98f3,6c4b19cc-324c-40dc-bba8-d11133b9f50b,148926b9-7b37-4341-9992-b7d8a1ec30df,585c8f84-594a-49fa-99ff-2b303622036a,f1c74b97-80a5-4813-b937-242c91f24916,44a103f2-065c-45f2-9081-dbacfd6d9797,5617184c-bc5a-417f-a68e-67d6516f55a7,95d349ec-1593-4f44-bd8d-c7ebbace77d4,ea08a977-ff8a-45a2-abad-94093bb02e9a,ad9e50dd-4333-422f-8317-a0baedd0917d,752d7689-92fa-466b-97c0-afe45290ae58,1c0f9ec9-fe83-402c-9a23-c714a6f2168b,bff773c8-7cf2-4a36-b8a5-bcf0d67856fd,952459ab-99c5-416f-8fbd-0fb96670eae8,8be49780-0897-4c83-8e79-9900c98edb80,5d2e9665-5182-4080-a1e4-0376b695c3b0,e57e92a5-00d8-48df-97e2-59dcf924442f,7eb29509-07ba-4a1b-87f1-de6b987a911c,a941156e-73f8-4658-8266-6f14567974d9,b675b499-a4a5-4028-a90a-3dddcd2013bf,4ae88ff9-3dd1-4049-9a8a-d731694242aa,48b25bdd-dd76-4f18-b4be-ea3c1ba2e459,d1feef63-b74c-45a6-b7f1-803c77256fd5,92bdd829-6562-494f-97e0-70dd6d071f95,655c84bb-61b2-41cb-8b18-304048ec5649,d7a0b7ee-b4b2-45b2-89d9-a85cda54bddc,1c792798-6636-4583-9155-578a4da2ad62,6cf88080-812b-455e-9ed6-578db1b80079,bdb3c625-a960-4567-abd3-002278d2d618,7473ea5b-bbe2-4de9-b491-fa457bce7466,20d4c331-60a7-44f6-9459-364114eb02cb,9b97e232-1f92-49da-983b-dc611b55cb68,2de04e8f-0306-4811-a900-8d1b92651b8b,4a870e9f-1a54-4cf1-8ddb-7a81a771a287,39e5dc45-5366-4704-bf63-9240496d62dd,6f519ed9-a942-4981-b316-d505467f8662,f9f55b44-48fe-4492-9e3b-f6d4f2c945ea,0bfe100c-333b-4f30-878b-fc7c775caa9f,c4a35457-cc28-405d-8546-7c93895db3c5,b73452dc-c06e-4ee4-b7ce-ea99774539a2,0ae509c8-4201-46fe-a1ac-6252354336e0,22eb8818-7850-4961-9613-967b41cba7e1,c0945bfc-10e5-48f3-a310-c0cb11d54030,3b5904ef-505c-4af6-8dbe-9f229f8ed17c,af90070d-308c-4da9-a4b6-9d9ba7cb2932,100c7390-87c2-42a9-aa9f-df7840485d01,22079344-b22e-410a-8852-4f1f57efdeff,4735e036-3fcf-4ddd-a331-fadcbeffa9d1,25ca9b34-6ef4-4015-8133-f874ad6f2bdb,90bfa0bb-0fd4-4bde-8b3a-83267d2d5ef9,ba15f01e-0bc4-4c34-b9a7-0b23c1c6b8c7,90491aba-26c0-4020-a79d-c27ac86cd635,9a9b64a7-f5d7-4367-a8aa-05a17b00b2c1,7d09f3ce-dd43-45b2-8173-67b23a3b0588,9c6301dc-b29c-4599-9c1f-592e9ae42374,b1669f27-37ed-4823-885f-d4a904376db9,ef60430e-40b4-4549-a06c-e8e80fb1cd47,04167cb3-76c2-40b3-8d40-7dbe6cbe1467,1119aab3-87d4-4630-9d31-33bf5d1bde55,0df252d5-960a-41c5-ab26-554b3106f6eb,36ce7a59-66fc-46f0-aacd-9f8bb73c2d82,ac818551-00b0-4d97-9c12-f3d50a32d128,6b81f4b4-dd68-423f-9d65-707f343dd728,ee87e291-7c29-408b-ab66-523b425d4eac,a1569f0f-08ff-4f84-8983-cdd55e16dd57,3d5736b2-a9cc-4d77-8c8b-5d184eab41f9,e75bbb89-4fbb-4dab-b7b9-48431b45ffcb,16d23474-d345-42df-8df7-9de252916580,9055c60e-2082-4109-95c0-7894d394f61e,2186967c-014a-467f-a095-9d5c57b92af6,de33deb3-6e10-4b56-8f08-e78379ed7b1d,68836016-49a8-453b-84e7-4e92eb2aeb68,15923568-1fc2-4d0b-8e3e-1d26fecfbe58,1dbfd1fc-9fda-481c-8821-5d8cc9418d16,7a347722-6785-449a-a855-83f2b359a40f,698e26eb-cdda-4ad1-942a-08063b71c543,2a5b23f3-da78-47d4-a609-8f5e74402b44,',@CurrencyID=N'VND',@ContractID=N',da95d7c2-9236-43e5-a6bc-3dcaa1ddb60c,',@IsWorkingWithManagementBook=0
-- nvtoan modify 29/01/2014: Khi chọn tất cả tài khoản thì chỉ lấy tài khoản chi tiết nhất
-- NVTOAN MODIFY 30/01/2015: Sửa lỗi chọn dự án thì chỉ hiển thị dự án (mặc dù lấy số liệu của hợp đồng thuộc dự án)
-- =============================================

DECLARE			@FromDate DATETIME 
DECLARE			@ToDate DATETIME 
DECLARE			@BranchID UNIQUEIDENTIFIER -- Chi nhánh
DECLARE			@IncludeDependentBranch BIT -- Có bao gồm số liệu chi nhánh phụ thuộc hay không?
DECLARE			@AccountNumber NVARCHAR(25) -- Số tài khoản
DECLARE			@AccountObjectID AS NVARCHAR(MAX)  -- Danh sách mã khách hàng
DECLARE			@CurrencyID NVARCHAR(3) -- Loại tiền
DECLARE			@ContractID AS NVARCHAR(MAX)  -- Danh sách mã hợp đồng 
DECLARE			@IsWorkingWithManagementBook BIT--  Có dùng sổ quản trị hay không?


SET				@FromDate='2018-01-01 00:00:00'
SET				@ToDate='2018-01-15 23:59:59'
SET				@BranchID='9F75F5D4-5213-4432-9D30-0DA0CE72D52B'
SET				@IncludeDependentBranch=1
SET				@AccountNumber=N'131'
SET				@AccountObjectID=N',271f6a73-40af-470d-8ff9-cc7cbe0a441a,4176d066-cfbf-4661-bb69-37a5e88554bb,eb5f5dc4-a973-4e15-90c8-0b3b62fa0247,1c39f240-6a76-4d30-88cc-c1794e162dc3,0de9f8c7-560a-4b05-8e6a-3e82abcf50e2,58efaebf-f074-4336-86d7-439ba11cac26,410c0ed4-9d79-49d1-94e4-5f33361b1700,2ea65716-13d0-4aea-9506-e8ce4e0ded39,4acfc6f7-a8db-4e14-89cf-52d13b483df4,be2c2d67-d658-4245-b684-a446cd7a38f9,8cbfa0cc-26e5-48e1-bb60-f6d3c9d9965e,'
SET				@CurrencyID=N'VND'
SET				@ContractID=N',f0ef577f-2c3d-49a1-9164-a8edba07c29f,f5c3d84b-97ed-49c5-ace6-bffcbdf1022f,cb78ef91-72ba-498e-b984-90002675ddd1,3d2186e7-3033-4313-8d47-c400a7b5af9a,62c3ff3f-cded-4a16-8387-a2820165736e,6e05231b-a2f0-4004-8c7f-73fafc1d896a,79bad869-60e7-438b-bade-f67d4c9c9b67,1cf541b9-9180-42cd-98e6-6bfcd4ca7f1e,'
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
               
        DECLARE @tblListAccountObjectID TABLE -- Bảng chứa danh sách khách hàng
            (
              AccountObjectID UNIQUEIDENTIFIER ,
              AccountObjectCode NVARCHAR(25) ,
              AccountObjectName NVARCHAR(128) ,
              AccountObjectAddress NVARCHAR(255) ,
              AccountObjectTaxCode NVARCHAR(50) ,
              AccountObjectGroupListCode NVARCHAR(MAX) ,
              AccountObjectCategoryName NVARCHAR(MAX)
            ) 
        INSERT  INTO @tblListAccountObjectID
                SELECT  TLAO.Value AS AccountObjectID ,
                        ao.AccountObjectCode ,
                        ao.AccountObjectName ,
                        ao.Address ,
                        ao.CompanyTaxCode ,
                        AO.AccountObjectGroupListCode , -- Mã nhóm NCC
                        [dbo].[Func_GetAccountObjectGroupListName](AO.AccountObjectGroupListCode) AS AccountObjectCategoryName -- tên nhóm NCC
                FROM    dbo.Func_ConvertGUIStringIntoTable(@AccountObjectID,
                                                           ',') AS TLAO
                        INNER JOIN AccountObject AS AO ON AO.AccountObjectID = TLAO.Value        			
        
        DECLARE @tblListContractID TABLE -- Bảng chứa danh sách mã hợp đồng
            (
              ContractID UNIQUEIDENTIFIER ,
              ContractCode NVARCHAR(50) ,
              PUSignDate DATETIME ,
              ContractName NVARCHAR(Max)
            ) 
        INSERT  INTO @tblListContractID
                SELECT  f.Value ,
                        C.ContractCode ,
                        C.SignDate ,
                        C.ContractSubject
                FROM    dbo.Func_ConvertGUIStringIntoTable(@ContractID, ',') f
                        INNER JOIN dbo.Contract C ON f.Value = C.ContractID
        DECLARE @tblAccountNumber TABLE
            (
              AccountNumber NVARCHAR(25) PRIMARY KEY ,
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
                                AND AccountObjectType = 1
                                AND IsParent = 0
                        ORDER BY A.AccountNumber ,
                                A.AccountName
            END
            
        
        
        SELECT  ROW_NUMBER() OVER ( ORDER BY ContractCode, AccountObjectCode ) AS RowNum ,
                ContractID ,
                ContractCode , -- Mã hợp đồng bán     
                PUSignDate , -- Ngày ký hợp đồng bán
                ContractName ,   -- Trích yếu hợp đồng bán
                AccountObjectID ,
                AccountObjectCode ,   -- Mã NCC
                AccountObjectName ,	-- Tên NCC              
                AccountObjectAddress , -- Địa chỉ
                AccountObjectTaxCode ,
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
                AccountObjectCategoryName ,
                BranchName
        FROM    ( SELECT    LCID.ContractID ,
                            LCID.ContractCode ,
                            LCID.PUSignDate ,
                            LCID.ContractName ,   -- Trích yếu hợp đồng bán
                            AOL.AccountObjectID ,
                            LAOI.AccountObjectCode ,   -- Mã NCC
                            LAOI.AccountObjectName ,	-- Tên NCC lấy trên danh mục              
                            LAOI.AccountObjectAddress , -- Địa chỉ    
                            LAOI.AccountObjectTaxCode , -- Mã số thuế
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
                            LAOI.AccountObjectCategoryName ,
                            AOL.BranchID ,
                            OU.OrganizationUnitName BranchName
                  FROM      dbo.AccountObjectLedger AS AOL
                            INNER JOIN dbo.[Contract] C ON C.ContractID = AOL.ContractID
                            INNER JOIN @tblListContractID LCID ON ( C.ContractID = LCID.ContractID
                                                              OR C.ProjectID = LCID.ContractID
                                                              ) --NVTOAN modify 22/01/2015: Sử lỗi không lấy được hợp đồng con của dự án
                            INNER JOIN @tblAccountNumber TBAN ON AOL.AccountNumber LIKE TBAN.AccountNumber
                                                              + '%'
                            INNER JOIN dbo.Account AS AN ON AOL.AccountNumber = AN.AccountNumber
                            INNER JOIN @tblListAccountObjectID AS LAOI ON AOL.AccountObjectID = LAOI.AccountObjectID
                            INNER JOIN @tblBrandIDList BIDL ON AOL.BranchID = BIDL.BranchID
                            LEFT JOIN dbo.Unit AS UN ON AOL.UnitID = UN.UnitID -- Danh mục ĐVT
                            LEFT JOIN dbo.OrganizationUnit OU ON OU.OrganizationUnitID = C.BranchID
                  WHERE     AOL.PostedDate <= @ToDate
                            AND AOL.IsPostToManagementBook = @IsWorkingWithManagementBook
                            AND ( @CurrencyID IS NULL
                                  OR AOL.CurrencyID = @CurrencyID
                                )
                            AND AN.DetailByAccountObject = 1
                ) AS RSNS
       
        GROUP BY RSNS.ContractID ,
                RSNS.ContractCode , -- Mã hợp đồng bán     
                RSNS.PUSignDate , -- Ngày ký hợp đồng bán
                RSNS.ContractName ,   -- Trích yếu hợp đồng bán
                RSNS.AccountObjectID ,
                RSNS.AccountObjectCode ,   -- Mã NCC
                RSNS.AccountObjectName ,	-- Tên NCC              
                RSNS.AccountObjectAddress , -- Địa chỉ
                RSNS.AccountObjectTaxCode , -- Mã số thuế             
                RSNS.AccountNumber , -- Số tài khoản
                RSNS.AccountCategoryKind , -- Tính chất tài khoản
                RSNS.AccountObjectGroupListCode ,
                RSNS.AccountObjectCategoryName ,
                RSNS.BranchID ,
                BranchName
         HAVING
				SUM(DebitAmountOC)<>0 OR
                SUM(DebitAmount)<>0 OR
                SUM(CreditAmountOC) <>0 OR
                SUM(CreditAmount) <>0 OR
                SUM(OpenningDebitAmountOC - OpenningCreditAmountOC)<>0 OR
                SUM(OpenningDebitAmount - OpenningCreditAmount)<>0
        --ORDER BY RSNS.ContractCode, -- Mã hợp đồng bán
        --        RSNS.AccountObjectCode -- Mã NCC
    END
    
