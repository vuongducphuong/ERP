# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
import json

class ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG(models.Model):
    _name = 'account.ex.chon.chung.tu.xuat.kho.mua.hang'
    _description = ''
    
    # _auto = False

    LOAI = fields.Selection([('XUAT_KHO_KHAC', 'Xuất kho khác'), ('MUA_HANG_KHONG_QUA_KHO', 'Mua hàng không qua kho'), ], string='Loại', help='Loại',default='XUAT_KHO_KHAC', required=True)
    KY = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='THANG_NAY')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    CONG_GOP_CAC_MAT_HANG_GIONG_NHAU = fields.Boolean(string='Cộng gộp các mặt hàng giống nhau', help='Cộng gộp các mặt hàng giống nhau',default=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHON_CHUNG_TU_JSON = fields.Char()
    ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS = fields.One2many('account.ex.chon.chung.tu.xuat.kho.mua.hang.chi.tiet', 'CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_ID', string='Chọn chứng từ xuất kho mua hàng chi tiết')
    LAY_DU_LIEU_JSON = fields.Char()

    @api.onchange('LAY_DU_LIEU_JSON')
    def _onchange_LAY_DU_LIEU_JSON(self):
        if self.LAY_DU_LIEU_JSON:
                param = ast.literal_eval(self.LAY_DU_LIEU_JSON)
                if param:
                        chung_tu = self.lay_du_lieu_ct_xuat_mua_hang()
                        if chung_tu:
                                env = self.env['account.ex.chon.chung.tu.xuat.kho.mua.hang.chi.tiet']
                                self.ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS = []
                                for line in chung_tu:
                                        chon = False
                                        if self.CHON_CHUNG_TU_JSON:
                                                dict_ct_da_chon = ast.literal_eval(self.CHON_CHUNG_TU_JSON)
                                                for line_ct in dict_ct_da_chon:
                                                        if line_ct.get('ID_GOC') == line.get('ID_GOC') and line_ct.get('MODEL_GOC') == line.get('MODEL_GOC'):
                                                                chon = True
                                        new_line = env.new({
                                                'MA_HANG_ID': line.get('MA_HANG_ID'),
                                                'TEN_HANG': line.get('TEN_HANG'),
                                                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN'),
                                                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
                                                'SO_CHUNG_TU': line.get('SO_CHUNG_TU'),
                                                'TK_NO_ID': line.get('TK_NO_ID'),
                                                'TK_CO_ID': line.get('TK_CO_ID'),
                                                'DVT_ID': line.get('DVT_ID'),
                                                'SO_LUONG': line.get('SO_LUONG'),
                                                'DON_GIA': line.get('DON_GIA'),
                                                'THANH_TIEN': line.get('SO_LUONG')*line.get('DON_GIA'),
                                                'ID_GOC': line.get('ID_GOC'),
                                                'MODEL_GOC': line.get('MODEL_GOC'),
                                                'CHON' : chon,
                                        })
                                        self.ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS += new_line
                        else:
                                self.ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS = []

    @api.onchange('KY')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY, 'TU_NGAY', 'DEN_NGAY')

    @api.model
    def default_get(self, fields):
        rec = super(ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG, self).default_get(fields)
        arr_chung_tu_da_chon = []
        chung_tu_da_chon = self._context.get('ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS')
        # i = 0
        if chung_tu_da_chon:
                for line in chung_tu_da_chon:
                # i += 1
                        arr_chung_tu_da_chon.append({
                                'ID_GOC' : line.get('ID_GOC'),
                                'MODEL_GOC' : line.get('MODEL_GOC'),
                        })
                rec['JSON'] = json.dumps(arr_chung_tu_da_chon)
        return rec

#     @api.onchange('LOAI')
#     def _onchange_LOAI(self):
#         if self.TU_NGAY != False:
#                 chung_tu = self.lay_du_lieu_ct_xuat_mua_hang()
#                 if chung_tu:
#                         env = self.env['account.ex.chon.chung.tu.xuat.kho.mua.hang.chi.tiet']
#                         self.ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS = []
#                         for line in chung_tu:
#                                 chon = False
#                                 if self.JSON:
#                                         dict_ct_da_chon = json.loads(self.JSON)
#                                         for line_ct in dict_ct_da_chon:
#                                                 if line_ct.get('ID_GOC') == line.get('ID_GOC') and line_ct.get('MODEL_GOC') == line.get('MODEL_GOC'):
#                                                         chon = True
#                                 new_line = env.new({
#                                         'MA_HANG_ID': line.get('MA_HANG_ID'),
#                                         'TEN_HANG': line.get('TEN_HANG'),
#                                         'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN'),
#                                         'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
#                                         'SO_CHUNG_TU': line.get('SO_CHUNG_TU'),
#                                         'TK_NO_ID': line.get('TK_NO_ID'),
#                                         'TK_CO_ID': line.get('TK_CO_ID'),
#                                         'DVT_ID': line.get('DVT_ID'),
#                                         'SO_LUONG': line.get('SO_LUONG'),
#                                         'DON_GIA': line.get('DON_GIA'),
#                                         'THANH_TIEN': line.get('SO_LUONG')*line.get('DON_GIA'),
#                                         'ID_GOC': line.get('ID_GOC'),
#                                         'MODEL_GOC': line.get('MODEL_GOC'),
#                                         'CHON' : chon,
#                                 })
#                                 self.ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS += new_line
#                 else:
#                         self.ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS = []
    



    def lay_du_lieu_ct_xuat_mua_hang(self):
        record = []
        loai_ct = []
        if self.LOAI == 'XUAT_KHO_KHAC':
                loai_ct.append('2022')
        elif self.LOAI == 'MUA_HANG_KHONG_QUA_KHO':
                loai_ct = ['312','324','313','314','315','316','325','326','327','328']
        params = {
            'TU_NGAY': self.TU_NGAY,
            'DEN_NGAY' : self.DEN_NGAY,
            'LOAI_CT' : tuple(loai_ct)
            }
        if self.LOAI == 'XUAT_KHO_KHAC':
        
            
            query = """   

            
SELECT  CAST(0 AS BIT) AS Selected ,
                    M."ID_CHUNG_TU" AS "ID_GOC",
                    'stock.ex.nhap.xuat.kho' AS "MODEL_GOC",
                    M."CHI_TIET_ID" ,
                    M."MA_HANG_ID" ,
                    M."TEN_HANG" ,
                    M."NGAY_HACH_TOAN" ,
                    M."NGAY_CHUNG_TU" ,
                    M."SO_CHUNG_TU" ,
                    M."DVT_ID" ,
                    coalesce(M."SO_LUONG",0) AS "SO_LUONG" ,
                    coalesce(M."DON_GIA" , 0) AS "DON_GIA" ,
                    M."GHI_NO" AS "THANH_TIEN",
                    M."GHI_CO",--dvtien-10/08/2016:sửa này để tổng giá trị=thành tiền=> không phải case trên code(trường hợp nào trên ghi tăng CCDC cũng lấy thành tiền=tổng giá trị bug 113361)
                    M."TAI_KHOAN_ID" AS "TK_NO_ID" ,
                    M."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO_ID" ,
                    M."CHI_NHANH_ID" ,
                    M."ID_CHUNG_TU" ,
                    M."LOAI_CHUNG_TU"
FROM so_cai_chi_tiet M
LEFT JOIN danh_muc_don_vi_tinh U ON M."DVT_ID" = U.id
--INNER JOIN (
----     @AccountingSystem = 15
----     @SubAccountSystem = 0
--          SELECT id,"SO_TAI_KHOAN"
--          FROM danh_muc_he_thong_tai_khoan
--          WHERE "SO_TAI_KHOAN" in ('6413','6423','6273','6233','242')
--           ) T ON M."TAI_KHOAN_ID" = T.id
					-- nmtruong 30/6/2016: Không lấy lên các dòng chi tiết đã ghi tăng
                    LEFT JOIN (
                                SELECT  SR.*
                                FROM    supply_ghi_tang_nguon_goc_hinh_thanh SR
                                        INNER JOIN supply_ghi_tang M ON M.id = SR."GHI_TANG_NGUON_GOC_HINH_THANH_ID"
--                                 WHERE   M.BranchID = @BranchID
                              ) PS ON ( ( PS.id IS NULL
                                          AND PS."GHI_TANG_NGUON_GOC_HINH_THANH_ID" = M."ID_CHUNG_TU"
                                        ) -- lấy lên phần convert từ bản trước khi có cột PS.RefdetailID
                                        OR ( PS.id IS NOT NULL
                                             AND PS.id = M."CHI_TIET_ID"
                                           )
                                      )
						-- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Chi phí trả trước
                    LEFT JOIN ( SELECT  SR.*
                                FROM    tong_hop_chi_phi_tra_truoc_tap_hop_chung_tu SR
                                        INNER JOIN tong_hop_chi_phi_tra_truoc M ON M.id = SR."CHI_PHI_TRA_TRUOC_ID"
--                                 WHERE   M.BranchID = @BranchID
                              ) SR ON ( ( SR.id IS NULL
                                          AND SR."CHI_PHI_TRA_TRUOC_ID" = M."ID_CHUNG_TU"
                                        ) -- lấy lên phần convert từ bản trước khi có cột SR.RefdetailID
                                        OR ( SR.id IS NOT NULL
                                             AND SR.id = M."CHI_TIET_ID"
                                           )
                                      )
						-- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Điều chỉnh công cụ dụng cụ
                    LEFT JOIN ( SELECT  SR.*
                                FROM    supply_dieu_chinh_tap_hop_chung_tu SR
                                        INNER JOIN supply_dieu_chinh M ON M.id = SR."TAP_HOP_CHUNG_TU_CCDC_ID_ID"
--                                 WHERE   M.BranchID = @BranchID
                              ) ADV ON ADV."TAP_HOP_CHUNG_TU_CCDC_ID_ID" = M."ID_CHUNG_TU"

WHERE   M."NGAY_CHUNG_TU" BETWEEN %(TU_NGAY)s AND %(DEN_NGAY)s
                     AND M."LOAI_CHUNG_TU" IN %(LOAI_CT)s
--                     AND M."CHI_NHANH_ID" = (chi_nhanh_id)
                    AND M."GHI_NO" <> 0
                    AND PS."GHI_TANG_NGUON_GOC_HINH_THANH_ID" IS NULL
                    AND SR."CHI_PHI_TRA_TRUOC_ID" IS NULL
                    AND ADV."TAP_HOP_CHUNG_TU_CCDC_ID_ID" IS NULL
            ORDER BY M."NGAY_HACH_TOAN" ,
                    M."NGAY_CHUNG_TU" ,
                    M."SO_CHUNG_TU"


        """  

        elif self.LOAI == 'MUA_HANG_KHONG_QUA_KHO':
            query = """   

            SELECT
    CAST(0 AS BIT) AS Selected ,
                    M.id AS "CHI_TIET_ID" ,
                    M."order_id" AS "ID_GOC",
                    'purchase.document.line' AS "MODEL_GOC",
                    M."MA_HANG_ID" ,
                    M."TEN" AS "TEN_HANG" ,
                    PV."NGAY_HACH_TOAN" ,
                    PV."NGAY_CHUNG_TU" ,
                    PV."SO_CHUNG_TU" ,
                    M."DVT_ID" ,
                    M."SO_LUONG" AS "SO_LUONG" ,
                     --dvtien 10/08/2016 sửa bug113379 Yêu cầu: Đơn giá = Thành tiền/Số lượng
                    "DON_GIA" = ( CASE WHEN M."SO_LUONG" = 0 THEN 0
                                       ELSE ( ( coalesce(M."THANH_TIEN_QUY_DOI", 0)
                                                      - coalesce(M."TIEN_CHIET_KHAU",
                                                              0)
                                                      + coalesce(M."TIEN_THUE_NK_QUY_DOI",
                                                              0)
                                                      + coalesce(M."TIEN_THUE_TTDB_QUY_DOI",
                                                              0)
                                                      + coalesce(M."TIEN_THUE_BVMT_QUY_DOI",
                                                              0)
                                                      + ( SELECT
                                                              CASE
                                                              WHEN PV."LOAI_CHUNG_TU" IN ('324', '325', '326','327', '328', '374','375', '376', '377','378' )
                                                              THEN --mua hàng nhập khẩu (Nếu TKĐUGTGT ='' thì lấy tiền thuế
                                                              CASE
                                                              WHEN ( M."TK_DU_THUE_GTGT_ID" IS NULL
                                                              OR M."TK_DU_THUE_GTGT_ID" = 0
                                                              )
                                                              THEN M."TIEN_THUE_GTGT"
                                                              ELSE 0
                                                              END
                                    --Mua hàng trong nước: Nếu k nhập TK thuế GTGT thì cộng thêm tiền thuế
                                                              WHEN PV."LOAI_CHUNG_TU" IN ('312', '313', '314','315', '316', '362','363', '364', '365','366' )
                                                              THEN CASE
                                                              WHEN ( M."TK_THUE_GTGT_ID" IS NULL
                                                              OR M."TK_THUE_GTGT_ID" = 0
                                                              )
                                                              THEN M."TK_THUE_GTGT_ID"
                                                              ELSE 0
                                                              END
                                                              ELSE 0
                                                              END
                                                        ) ) / M."SO_LUONG" )
                                  END ) ,
                                  --kt sửa bug 113379 đoạn 2
                    M."DON_GIA" ,--dvtien 10/08/2016-vì đơn giá lấy lên chứng tư ghi tăng hàng loạt là trên chứng từ còn đơn giá trên form chọn lại tính <> nên phải lấy ra thêm
                    ( coalesce(M."THANH_TIEN_QUY_DOI", 0) - coalesce(M."TIEN_CHIET_KHAU", 0)
                      + coalesce(M."TIEN_THUE_NK_QUY_DOI", 0)
                      + coalesce(M."TIEN_THUE_TTDB_QUY_DOI", 0)
                      + coalesce(M."TIEN_THUE_BVMT_QUY_DOI", 0)
                      + ( SELECT    CASE WHEN PV."LOAI_CHUNG_TU" IN ( '324', '325', '326','327', '328', '374','375', '376', '377','378' )
                                         THEN --mua hàng nhập khẩu (Nếu TKĐUGTGT ='' thì lấy tiền thuế
                                              CASE WHEN ( M."TK_DU_THUE_GTGT_ID" IS NULL
                                                          OR M."TK_DU_THUE_GTGT_ID" = 0
                                                        ) THEN M."TIEN_THUE_GTGT_QUY_DOI"
                                                   ELSE 0
                                              END
                                    --Mua hàng trong nước: Nếu k nhập TK thuế GTGT thì cộng thêm tiền thuế
                                         WHEN PV."LOAI_CHUNG_TU" IN ( '312', '313', '314','315', '316', '362','363', '364', '365','366' )
                                         THEN CASE WHEN ( M."TK_THUE_GTGT_ID" IS NULL
                                                          OR M."TK_THUE_GTGT_ID" = 0
                                                        ) THEN M."TIEN_THUE_GTGT_QUY_DOI"
                                                   ELSE 0
                                              END
                                         ELSE 0
                                    END
                        ) ) AS "SO_TIEN_QUY_DOI" ,
                         --dvtien-05/08/2016: lấy tổng chi phí của chứng từ mua hàng =chi phí trước hải quan + chi phí mua hàng
                    (coalesce(M."PHI_TRUOC_HAI_QUAN", 0)
                    + coalesce(M."SO_PHAN_BO_LAN_NAY", 0)) AS "THONG_CHI_PHI",

                      --dvtien-05/08/2016: lấy tổng giá trị
                    M."TONG_GIA_TRI" AS "TONG_GIA_TRI" ,
                    M."TK_NO_ID" ,
                    M."TK_CO_ID" ,
                    M."DON_VI_ID" ,
                    M."THANH_TIEN_QUY_DOI" ,--dvtien-luôn lấy amountOC vì trường hợp là ngoại tệ sẽ <> quy đổi cần chia lại
                    M.order_id AS "ID_CHUNG_TU" ,
                    PV."LOAI_CHUNG_TU"
            FROM    purchase_document_line M
                    LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON M."MA_HANG_ID" = II.id
                    INNER JOIN purchase_document AS PV ON M.order_id = PV.id
                    LEFT JOIN danh_muc_don_vi_tinh U ON M."DVT_ID" = U.id
--                 INNER JOIN (
--                 --     @AccountingSystem = 15
--                 --     @SubAccountSystem = 0
--                           SELECT id,"SO_TAI_KHOAN"
--                           FROM danh_muc_he_thong_tai_khoan
--                           WHERE "SO_TAI_KHOAN" in ('6413','6423','6273','6233','242')
--                            ) T ON M."TAI_KHOAN_ID" = T.id
					-- nmtruong 30/6/2016: Không lấy lên các dòng chi tiết đã ghi tăng
                    LEFT JOIN ( SELECT  SR.*
                                FROM    supply_ghi_tang_nguon_goc_hinh_thanh SR
                                        INNER JOIN asset_ghi_tang M ON M.id = SR."GHI_TANG_NGUON_GOC_HINH_THANH_ID"
--                                 WHERE   M."CHI_NHANH_ID" = (chi_nhanh_id)
                              ) PS ON ( ( PS.id IS NULL
                                          AND PS."GHI_TANG_NGUON_GOC_HINH_THANH_ID" = M.order_id
                                        ) -- lấy lên phần convert từ bản trước khi có cột PS.RefdetailID
                                        OR ( PS.id IS NOT NULL
                                             AND PS.id = M.id
                                           )
                                      )
					-- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Chi phí trả trước
                    LEFT JOIN ( SELECT  SR.*
                                FROM    tong_hop_chi_phi_tra_truoc_tap_hop_chung_tu SR
                                        INNER JOIN tong_hop_chi_phi_tra_truoc M ON M.id = SR."CHI_PHI_TRA_TRUOC_ID"
--                                 WHERE   M.BranchID = @BranchID
                              ) SR ON ( ( SR.id IS NULL
                                          AND SR."CHI_PHI_TRA_TRUOC_ID" = M.order_id
                                        ) -- lấy lên phần convert từ bản trước khi có cột SR.RefdetailID
                                        OR ( SR.id IS NOT NULL
                                             AND SR.id = M.id
                                           )
                                      )
					-- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Điều chỉnh công cụ dụng cụ
                    LEFT JOIN ( SELECT  SR.*
                                FROM    supply_dieu_chinh_tap_hop_chung_tu SR
                                        INNER JOIN supply_dieu_chinh M ON M.id = SR."TAP_HOP_CHUNG_TU_CCDC_ID_ID"
--                                 WHERE   M.BranchID = @BranchID
                              ) ADV ON ADV."TAP_HOP_CHUNG_TU_CCDC_ID_ID" = M.order_id

            WHERE   PV."NGAY_HACH_TOAN" BETWEEN %(TU_NGAY)s AND %(DEN_NGAY)s
--                     AND PV."LOAI_CHUNG_TU" IN %(LOAI_CT)s
                    AND (  PV."state" = 'da_ghi_so')
--                     AND PV."CHI_NHANH_ID" = chi_nhanh_id
                    AND PS."GHI_TANG_NGUON_GOC_HINH_THANH_ID" IS NULL
                    AND SR."CHI_PHI_TRA_TRUOC_ID" IS NULL
                    AND ADV."TAP_HOP_CHUNG_TU_CCDC_ID_ID" IS NULL
             ORDER BY PV."NGAY_HACH_TOAN" ,
                    PV."NGAY_CHUNG_TU" --dvtien-11/08/2016-Sửa bug 113584 Lỗi sắp xếp trên form Chọn chứng từ xuất kho/mua hàng


        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'MA_HANG_ID': line.get('MA_HANG_ID', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
                'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
                'TK_NO_ID': line.get('TK_NO_ID', ''),
                'TK_CO_ID': line.get('TK_CO_ID', ''),
                'DVT_ID': line.get('DVT_ID', ''),
                'SO_LUONG': line.get('SO_LUONG', 0),   
                'DON_GIA' : line.get('DON_GIA', 0),   
                'THANH_TIEN' : line.get('THANH_TIEN', 0),  
                'ID_GOC' : line.get('ID_GOC', ''),   
                'MODEL_GOC' : line.get('MODEL_GOC', ''),    
            })
        
        return record
