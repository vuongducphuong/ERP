# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_CTGS_CHON_CHUNG_TU_FORM(models.Model):
    _name = 'tong.hop.ctgs.chon.chung.tu.form'
    _description = ''
    _auto = False
    
    LOAI_CHUNG_TU_ID = fields.Many2one('danh.muc.loai.chung.tu', string='Loại chứng từ', help='Loại chứng từ')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    LAY_DU_LIEU_JSON = fields.Text()

    TONG_HOP_CTGS_CHON_CHUNG_TU_CHI_TIET_FORM_IDS = fields.One2many('tong.hop.ctgs.chon.chung.tu.chi.tiet.form', 'CHON_CHUNG_TU_ID', string='CTGS chọn chứng từ chi tiết form')

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')

    # @api.model
    # def default_get(self, fields):
    #     rec = super(TONG_HOP_CTGS_CHON_CHUNG_TU_FORM, self).default_get(fields)
    #     rec['LOAI_CHUNG_TU_ID'] = self.env['danh.muc.loai.chung.tu'].search([('Trường', '=', ' Giá trị')])
    #     return rec


    def lay_du_lieu_chung_tu(self,args):
        new_line_chung_tu = [[5]]
        chung_tus = self.load_du_lieu_chung_tu(args.get('tu_ngay'),args.get('den_ngay'),args.get('loai_chung_tu_id'),self.get_chi_nhanh())
        if chung_tus:
            for chung_tu in chung_tus:
                chon = False
                if args.get('params'):
                    for chi_tiet in args.get('params'):
                        if chi_tiet.get('id_chung_tu') == chung_tu.get('CHUNG_TU_ID') and chi_tiet.get('model_goc') == chung_tu.get('MODEL_CHUNG_TU'):
                            chon = True
                new_line_chung_tu += [(0, 0, {
					'NGAY_HACH_TOAN': chung_tu.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': chung_tu.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': chung_tu.get('SO_CHUNG_TU'),
					'DIEN_GIAI': chung_tu.get('DIEN_GIAI_CHUNG'),
					'TK_NO_ID' : [chung_tu.get('TK_NO_ID'),chung_tu.get('MA_TK_NO')],
					'TK_CO_ID' : [chung_tu.get('TK_CO_ID'),chung_tu.get('MA_TK_CO')],
					'SO_TIEN': chung_tu.get('SO_TIEN_QUY_DOI'),
					'LOAI_CHUNG_TU': chung_tu.get('TEN_LOAI_CHUNG_TU'),
					'ID_GOC': chung_tu.get('CHUNG_TU_ID'),
					'MODEL_GOC': chung_tu.get('MODEL_CHUNG_TU'),
					'AUTO_SELECT' : chon,
					})]
        return {'TONG_HOP_CTGS_CHON_CHUNG_TU_CHI_TIET_FORM_IDS': new_line_chung_tu}


    def load_du_lieu_chung_tu(self,tu_ngay,den_ngay,loai_chung_tu_id,chi_nhanh_id):
        params = {
            'DEN_NGAY': den_ngay,
            'TU_NGAY' : tu_ngay,
            'LOAI_CHUNG_TY_ID' : loai_chung_tu_id,
            'CHI_NHANH_ID' : chi_nhanh_id,
            }

        query = """   

        DO LANGUAGE plpgsql $$
          DECLARE

            tham_so_id_chung_tu         INTEGER :=0;
            tham_so_tu_ngay             DATE := %(TU_NGAY)s;
            tham_so_den_ngay            DATE := %(DEN_NGAY)s;
            tham_so_isedit              INTEGER :=0;
            tham_so_loai_chung_tu       INTEGER := %(LOAI_CHUNG_TY_ID)s;
            tham_so_list_chi_nhanh      INTEGER := %(CHI_NHANH_ID)s;

            ma_loai_chung_tu            VARCHAR(50) :='';
            tk_no                       VARCHAR(50) :='';
            tk_co                       VARCHAR(50) :='';
            phat_sinh_theo              VARCHAR(50) :='';
            nhom_loai_chung_tu          VARCHAR(50) :='';

            cursor_chi_tiet_id          INTEGER :=0;
            cursor_loai_chung_tu        INTEGER := 0;
            cursor_chung_tu_id          INTEGER := 0;
            cursor_chung_tu_chi_tiet_id INTEGER := 0;
            cursor_doi_tuong_id         INTEGER := 0;

            m_so_chung_tu               VARCHAR(50) :='';
            m_ngay_chung_tu             DATE :='2018-01-01';
            m_nhom_loai_ct              VARCHAR(50) :='';
            m_dien_giai                 VARCHAR(50) :='';
            m_doi_tuong                 INTEGER :=0;


          BEGIN

            DROP TABLE IF EXISTS TMP_TEMP;
            DROP TABLE IF EXISTS TMP_RESULT;
            DROP TABLE IF EXISTS TMP_NHOM_LOAI_CT;
            DROP TABLE IF EXISTS TMP_KET_QUA;

            CREATE TEMP TABLE TMP_NHOM_LOAI_CT AS
              SELECT danh_muc_nhom_loai_chung_tu_id
              FROM danh_muc_loai_chung_tu_danh_muc_nhom_loai_chung_tu_rel
              WHERE danh_muc_loai_chung_tu_id = tham_so_loai_chung_tu;

            SELECT
              "MA_LOAI"
              , coalesce(tkn."SO_TAI_KHOAN", '')
              , coalesce(tkc."SO_TAI_KHOAN", '')
              , "PHAT_SINH_SELECTION"
            INTO ma_loai_chung_tu, tk_no, tk_co, phat_sinh_theo
            FROM danh_muc_loai_chung_tu l
              LEFT JOIN danh_muc_he_thong_tai_khoan tkn ON tkn.id = l."TK_NO_ID"
              LEFT JOIN danh_muc_he_thong_tai_khoan tkc ON tkc.id = l."TK_CO_ID"
            WHERE l.id = tham_so_loai_chung_tu
            LIMIT 1;

            CREATE TEMP TABLE TMP_TEMP
              AS
                SELECT
                  M.id AS "ID_CHUNG_TU"
                  , M."ID_CHUNG_TU_GOC"
                  ,
                  /*Edited by ntlieu 30/10/2015: Với chứng từ chỉ hạch toán TK Có thì khi build cần build ngược lại mới so sánh được trong Sổ cái*/
                  CONCAT(CAST(M."ID_CHUNG_TU_GOC" AS VARCHAR(50)),
                        '$'
                  , CASE WHEN coalesce(cast(D."TK_NO_ID" AS VARCHAR(50)), '') = ''
                    THEN coalesce(cast(D."TK_CO_ID" AS VARCHAR(50)), '')
                    ELSE coalesce(cast(D."TK_NO_ID" AS VARCHAR(50)), '')
                    END
                  , '$'
                  , CASE WHEN coalesce(cast(D."TK_NO_ID" AS VARCHAR(50)), '') = ''
                    THEN coalesce(cast(D."TK_NO_ID" AS VARCHAR(50)), '')
                    ELSE coalesce(cast(D."TK_CO_ID" AS VARCHAR(50)), '')
                    END
                  )    AS "CHUNG_TU_CHI_TIET_VA_TAI_KHOAN"

                FROM tong_hop_chung_tu_ghi_so_chi_tiet D
                  INNER JOIN tong_hop_chung_tu_ghi_so M ON M.id = D."CHUNG_TU_GHI_SO_ID"
                                                          AND (
                                                            (tham_so_isedit = 0)
                                                            OR (tham_so_isedit = 1
                                                                AND M.id <> tham_so_id_chung_tu)
                                                          )
                WHERE D."NGAY_HACH_TOAN" BETWEEN tham_so_tu_ngay AND tham_so_den_ngay
                      AND M."HIEN_THI_TREN_SO" = TRUE;


            CREATE TEMP TABLE TMP_RESULT
              AS
                SELECT
                    0                    "ID_CHUNG_TU"
                  , 0                    "CHI_TIET_ID"
                  , GL."ID_CHUNG_TU"     "CHUNG_TU_ID"
                  , GL."CHI_TIET_ID"  AS "CHUNG_TU_CHI_TIET_ID"
                  , GL."LOAI_CHUNG_TU"   "LOAI_CHUNG_TU"
                  , RT."REFTYPENAME"     "TEN_LOAI_CHUNG_TU"
                  , "NGAY_CHUNG_TU"      "NGAY_CHUNG_TU"
                  , "NGAY_HACH_TOAN"     "NGAY_HACH_TOAN"
                  , "SO_CHUNG_TU"        "SO_CHUNG_TU"
                  , "DIEN_GIAI_CHUNG"
                  , GL."DIEN_GIAI"
                  , /*Edited by ntlieu 26/10/2015: Lấy dòng chỉ hạch toán có TK ngoài bảng*/
                    CASE WHEN phat_sinh_theo = 'PHAT_SINH_THEO_TAI_KHOAN'
                              AND "LOAI_HACH_TOAN" = '2'
                              AND coalesce("MA_TAI_KHOAN_DOI_UNG", '') = ''
                      THEN "MA_TAI_KHOAN_DOI_UNG"
                    ELSE "MA_TAI_KHOAN"
                    END                  "MA_TK_NO"
                  , --"MA_TK" AS "MA_TK_NO" ,
                    CASE WHEN phat_sinh_theo = 'PHAT_SINH_THEO_TAI_KHOAN'
                              AND "LOAI_HACH_TOAN" = '2'
                              AND coalesce("MA_TAI_KHOAN_DOI_UNG", '') = ''
                      THEN "MA_TAI_KHOAN"
                    ELSE "MA_TAI_KHOAN_DOI_UNG"
                    END               AS "MA_TK_CO"
                  , --"MA_TAI_KHOAN_DOI_UNG" AS "MA_TK_CO" ,
                  "currency_id"
                  , CASE WHEN phat_sinh_theo = 'PHAT_SINH_THEO_TAI_KHOAN'
                              AND "LOAI_HACH_TOAN" = '2'
                              AND coalesce("MA_TAI_KHOAN_DOI_UNG", '') = ''
                  THEN "GHI_CO"
                    ELSE "GHI_NO"
                    END                  "SO_TIEN_QUY_DOI"
                  , --"GHI_NO" "SO_TIEN_QUY_DOI" ,
                    ''                   Note
                  , GL."THU_TU_TRONG_CHUNG_TU"
                  , --         GL.DetailPostOrder,
                    ma_loai_chung_tu  AS "MA_LOAI_CHUNG_TU"
                  , GL."DOI_TUONG_ID" AS "DOI_TUONG_ID"
                  ,GL."MODEL_CHUNG_TU"
                FROM so_cai_chi_tiet GL
                  INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(20)) = GL."LOAI_CHUNG_TU"
                  LEFT JOIN TMP_TEMP T ON CONCAT(CAST(GL."CHI_TIET_ID" AS VARCHAR(50)), '$', coalesce("MA_TAI_KHOAN", ''), '$',
                                                coalesce("MA_TAI_KHOAN_DOI_UNG",
                                                          '')) = T."CHUNG_TU_CHI_TIET_VA_TAI_KHOAN"
                WHERE GL."LOAI_CHUNG_TU" NOT IN ('610', '611', '612', '613', '614', '620')  -- Loại bỏ ra số dư đầu kỳ
                      AND "NGAY_HACH_TOAN" BETWEEN tham_so_tu_ngay AND tham_so_den_ngay
                      AND ((-- Trường hợp Loại chứng từ Phát sinh theo Tài khoản thì lọc theo config TK Nợ + TK Có
                            phat_sinh_theo = 'PHAT_SINH_THEO_TAI_KHOAN'
                            AND (
                              (tk_no <> ''
                                AND tk_co <> ''
                                AND GL."MA_TAI_KHOAN" LIKE concat(tk_no, '%%')
                                AND "MA_TAI_KHOAN_DOI_UNG" LIKE concat(tk_co, '%%')
                              )
                              OR (tk_no <> ''
                                  AND tk_co = ''
                                  AND GL."MA_TAI_KHOAN" LIKE concat(tk_no, '%%')
                              )
                              OR (tk_no = ''
                                  AND tk_co <> ''
                                  AND "MA_TAI_KHOAN_DOI_UNG" LIKE concat(tk_co, '%%')
                              )
                            )
                            AND "LOAI_HACH_TOAN" = '1'
                            AND "GHI_NO" <> 0
                          )
                          OR (-- Trường hợp Loại chứng từ Phát sinh theo nhóm chứng từ
                            phat_sinh_theo = 'PHAT_SINH_THEO_NHOM_CHUNG_TU'
                            AND cast(GL."LOAI_CHUNG_TU" AS INTEGER) IN (
                              SELECT DISTINCT danh_muc_reftype_id AS "LOAI_CHUNG_TU"
                              FROM danh_muc_nhom_loai_chung_tu_danh_muc_reftype_rel VT
                                INNER JOIN danh_muc_loai_chung_tu_danh_muc_nhom_loai_chung_tu_rel F
                                  ON VT.danh_muc_nhom_loai_chung_tu_id = F.danh_muc_nhom_loai_chung_tu_id)
                            AND (("LOAI_HACH_TOAN" = '1'
                                  AND "GHI_NO" <> 0
                                  )
                                  OR ("LOAI_HACH_TOAN" = '2'
                                      AND coalesce("MA_TAI_KHOAN_DOI_UNG", '') = ''
                                      AND "GHI_CO" <> 0
                                  )
                            )
                          )
                      )
                      AND T."CHUNG_TU_CHI_TIET_VA_TAI_KHOAN" IS NULL
                      AND "CHI_NHANH_ID" IN (tham_so_list_chi_nhanh)

                UNION


                SELECT
                    0                 AS "ID_CHUNG_TU"
                  , 0                 AS "CHI_TIET_ID"
                  , GL."ID_CHUNG_TU"  AS "CHUNG_TU_ID"
                  , GL."CHI_TIET_ID"  AS "CHUNG_TU_CHI_TIET_ID"
                  , GL."LOAI_CHUNG_TU"   "LOAI_CHUNG_TU"
                  , RT."REFTYPENAME"     "TEN_LOAI_CHUNG_TU"
                  , "NGAY_CHUNG_TU"      "NGAY_CHUNG_TU"
                  , "NGAY_HACH_TOAN"     "NGAY_HACH_TOAN"
                  , "SO_CHUNG_TU"        "SO_CHUNG_TU"
                  , "DIEN_GIAI_CHUNG"
                  , GL."DIEN_GIAI"
                  , NULL              AS "MA_TK_NO"
                  , "MA_TAI_KHOAN"    AS "MA_TK_CO"
                  , "currency_id"
                  , "GHI_CO"          AS "SO_TIEN_QUY_DOI"
                  , NULL              AS Note
                  , GL."THU_TU_TRONG_CHUNG_TU"
                  , --         GL.DetailPostOrder,
                    ma_loai_chung_tu  AS "MA_LOAI_CHUNG_TU"
                  , GL."DOI_TUONG_ID" AS "DOI_TUONG_ID"
                  ,GL."MODEL_CHUNG_TU"
                FROM so_cai_chi_tiet GL
                  INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(20)) = GL."LOAI_CHUNG_TU"
                  LEFT JOIN TMP_TEMP T ON concat(CAST(GL."CHI_TIET_ID" AS VARCHAR(50)), '$', coalesce("MA_TAI_KHOAN", ''), '$',
                                                coalesce("MA_TAI_KHOAN_DOI_UNG", '')) = T."CHUNG_TU_CHI_TIET_VA_TAI_KHOAN"
                WHERE Gl."NGAY_HACH_TOAN" BETWEEN tham_so_tu_ngay AND tham_so_den_ngay
                      AND GL."LOAI_CHUNG_TU" NOT IN ('610', '611', '612', '613', '614', '620')  -- Loại bỏ ra số dư đầu kỳ
                      AND GL."MA_TAI_KHOAN" LIKE N'00%%'
                      AND ('521' = ''
                          AND tk_co <> ''
                          AND GL."MA_TAI_KHOAN" LIKE concat(tk_co, '%%')
                      )
                      AND "LOAI_HACH_TOAN" = '2'
                      AND "GHI_CO" <> 0
                      AND T."CHUNG_TU_CHI_TIET_VA_TAI_KHOAN" IS NULL

                      AND "CHI_NHANH_ID" IN (tham_so_list_chi_nhanh);

            --   SELECT * FROM TMP_RESULT

            IF cursor_loai_chung_tu IN (307, 308, 309, 310, 319, 320, 321, 322, 357, 358, 359, 360, 369, 370, 371, 372, 3031)
            THEN
              -- Case các trường hợp thuộc nhóm mua hàng hóa và mua hàng trả lại
              SELECT danh_muc_nhom_loai_chung_tu_id
              INTO m_nhom_loai_ct
              FROM danh_muc_loai_chung_tu_danh_muc_nhom_loai_chung_tu_rel
              WHERE danh_muc_loai_chung_tu_id = cursor_loai_chung_tu
              LIMIT 1;

              IF m_nhom_loai_ct IN (9, 12)
              THEN
                -- kiểm tra có phát sinh theo nhóm hay không
                IF phat_sinh_theo = 'PHAT_SINH_THEO_NHOM_CHUNG_TU'
                THEN
                  -- phát sinh theo nhóm 9 thì lấy phiếu nhập
                  IF exists(SELECT *
                            FROM TMP_NHOM_LOAI_CT
                            WHERE danh_muc_nhom_loai_chung_tu_id = 9)
                  THEN
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_NHAP"
                      , "DIEN_GIAI"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_document
                    WHERE id = cursor_chung_tu_id;
                  END IF;
                  -- phát sinh theo nhóm 12 thì lấy phiếu xuất
                  IF exists(SELECT *
                            FROM TMP_NHOM_LOAI_CT
                            WHERE danh_muc_nhom_loai_chung_tu_id = 12)
                  THEN
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_XUAT"
                      , "LY_DO_XUAT"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_ex_tra_lai_hang_mua
                    WHERE id = cursor_chung_tu_id;
                  END IF;

                END IF;
              ELSE
                -- trường hợp: Mua hàng trong nước nhập kho thanh toán ngay ( ủy nhiệm chi 308, séc tiền mặt 310, séc chuyển khoản 309, tiền mặt 307)
                IF cursor_loai_chung_tu IN (307, 308, 309, 310, 357, 358, 359, 360)
                THEN
                  -- chỉ có TK Nợ hoặc TK Có
                  IF tk_no = '' OR tk_co = ''
                  THEN

                    IF concat(tk_no, tk_co) LIKE '11%%' OR concat(tk_no, tk_co) LIKE '133'
                    THEN
                      SELECT
                        "SO_CHUNG_TU"
                        , "NGAY_CHUNG_TU_PHIEU_CHI"
                        , "LY_DO_CHI"
                      INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                      FROM purchase_document
                      WHERE id = cursor_chung_tu_id;
                    END IF;
                  ELSE --ngược lại thì lấy ở phiếu nhập
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_NHAP"
                      , "DIEN_GIAI"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_document
                    WHERE id = cursor_chung_tu_id;


                  END IF;
                  IF tk_no <> '' AND tk_co <> ''-- có cả TK Nợ và TK Có
                  THEN

                    IF tk_no LIKE '11%%' OR tk_co LIKE
                                          '122%%' -- TK Có là TK 11x, 133x lấy số chứng từ ở tab phiếu chi, ủy nhiệm chi, séc tiền mặt, séc chuyển khoản
                    THEN
                      SELECT
                        "SO_CHUNG_TU"
                        , "NGAY_CHUNG_TU_PHIEU_CHI"
                        , "LY_DO_CHI"
                      INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                      FROM purchase_document
                      WHERE id = cursor_chung_tu_id;
                    END IF;
                  ELSE -- ngược lại thì tab phiếu nhập
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_NHAP"
                      , "DIEN_GIAI"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_document
                    WHERE id = cursor_chung_tu_id;
                  END IF;

                END IF;
                -- trường hợp: Mua hàng nhập khẩu nhập kho thanh toán ngay (ủy nhiệm chi 320, séc tiền mặt 322, séc chuyển khoản 321, tiền mặt 319)
                IF cursor_loai_chung_tu IN (319, 320, 321, 322, 369, 370, 371, 372)
                THEN

                  IF tk_no = '' OR tk_co = '' -- chỉ có TK Nợ hoặc TK Có
                  THEN
                    -- là (11x, 133x, 333x ) lấy số chứng từ ở tab phiếu chi
                    IF concat(tk_no, tk_co) LIKE '11%%' OR concat(tk_no, tk_co) LIKE '133%%' OR concat(tk_no, tk_co) LIKE '333'
                    THEN
                      SELECT
                        "SO_CHUNG_TU"
                        , "NGAY_CHUNG_TU_PHIEU_CHI"
                        , "LY_DO_CHI"
                      INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                      FROM purchase_document
                      WHERE id = cursor_chung_tu_id;
                    END IF;
                  ELSE -- ngược lại thì lấy ở phiếu nhập
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_NHAP"
                      , "DIEN_GIAI"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_document
                    WHERE id = cursor_chung_tu_id;

                  END IF;

                  IF tk_no <> '' AND tk_co <> '' -- có cả TK Nợ và TK Có
                  THEN

                    IF tk_co LIKE
                      '11%%' -- TK Có là TK 11x lấy số chứng từ ở tab phiếu chi, ủy nhiệm chi, séc tiền mặt, séc chuyển khoản
                    THEN
                      SELECT
                        "SO_CHUNG_TU"
                        , "NGAY_CHUNG_TU_PHIEU_CHI"
                        , "LY_DO_CHI"
                      INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                      FROM purchase_document
                      WHERE id = cursor_chung_tu_id;
                    END IF;
                  ELSE -- ngược lại thì tab phiếu nhập
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_NHAP"
                      , "DIEN_GIAI"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_document
                    WHERE id = cursor_chung_tu_id;


                  END IF;

                END IF;
                -- trường hợp: Mua trả lại thu tiền ngay 3031
                IF cursor_loai_chung_tu = 3031
                THEN
                  -- chỉ có TK Nợ hoặc TK Có
                  IF tk_no = '' OR tk_co = ''
                  THEN
                    -- là (11x, 133x ) lấy số chứng từ ở tab phiếu thu
                    IF concat(tk_no, tk_co) LIKE '11%%' OR concat(tk_no, tk_co) LIKE '133%%'
                    THEN
                      SELECT
                        "SO_CHUNG_TU"
                        , "NGAY_CHUNG_TU_PHIEU_CHI"
                        , "LY_DO_NOP"
                      INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                      FROM purchase_ex_tra_lai_hang_mua
                      WHERE id = cursor_chung_tu_id;
                    END IF;
                  ELSE --ngược lại thì lấy ở phiếu xuất
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_XUAT"
                      , "LY_DO_XUAT"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_ex_tra_lai_hang_mua
                    WHERE id = cursor_chung_tu_id;
                  END IF;
                  -- có cả TK Nợ và TK Có
                  IF tk_no <> '' AND tk_co <> ''
                  THEN
                    IF tk_no LIKE '11%%' -- TK nợ là TK 11x lấy số chứng từ ở tab phiếu thu
                    THEN
                      SELECT
                        "SO_CHUNG_TU"
                        , "NGAY_CHUNG_TU_PHIEU_CHI"
                        , "LY_DO_NOP"
                      INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                      FROM purchase_ex_tra_lai_hang_mua
                      WHERE id = cursor_chung_tu_id;
                    END IF;
                  ELSE -- ngược lại thì tab phiếu xuất
                    SELECT
                      "SO_CHUNG_TU"
                      , "NGAY_CHUNG_TU_PHIEU_XUAT"
                      , "LY_DO_XUAT"
                    INTO m_so_chung_tu, m_ngay_chung_tu, m_dien_giai
                    FROM purchase_ex_tra_lai_hang_mua
                    WHERE id = cursor_chung_tu_id;
                  END IF;
                END IF;
                -- cập nhật số chứng từ đúng vào bảng kết quả
                IF m_so_chung_tu <> ''
                THEN
                  UPDATE TMP_RESULT
                  SET "SO_CHUNG_TU" = m_so_chung_tu, "NGAY_CHUNG_TU" = m_ngay_chung_tu, "DIEN_GIAI" = m_dien_giai
                  WHERE "CHI_TIET_ID" = cursor_chi_tiet_id;
                END IF;
              END IF;
              /*Nếu đối tượng nợ không có thì lấy đối tượng có*/
              IF cursor_doi_tuong_id ISNULL
              THEN
                SELECT "DOI_TUONG_ID"
                INTO m_doi_tuong
                FROM so_cai_chi_tiet
                WHERE "CHI_TIET_ID" = cursor_chung_tu_chi_tiet_id AND "LOAI_HACH_TOAN" = '2';

                UPDATE TMP_RESULT
                SET "DOI_TUONG_ID" = m_doi_tuong
                WHERE "CHI_TIET_ID" = cursor_chi_tiet_id;
              END IF;

            END IF;

            CREATE TEMP TABLE TMP_KET_QUA
              AS
                SELECT
                  R."ID_CHUNG_TU"
                  , R."CHI_TIET_ID"
                  , R."CHUNG_TU_ID"
                  , R."CHUNG_TU_CHI_TIET_ID"
                  , R."LOAI_CHUNG_TU"
                  , R."TEN_LOAI_CHUNG_TU"
                  , R."NGAY_CHUNG_TU"
                  , R."NGAY_HACH_TOAN"
                  , R."SO_CHUNG_TU"
                  , R."DIEN_GIAI_CHUNG"
                  , R."DIEN_GIAI"
                  ,A1.id AS "TK_NO_ID"
                  ,A2.id AS "TK_CO_ID"
                  , R."MA_TK_NO"
                  , R."MA_TK_CO"
                  , R."currency_id"
                  , R."SO_TIEN_QUY_DOI"
                  , --       Note,
                  R."THU_TU_TRONG_CHUNG_TU"
                  , --DetailPostOrder,
                  R."MA_LOAI_CHUNG_TU"
                  , R."DOI_TUONG_ID"
                  ,R."MODEL_CHUNG_TU"

                FROM TMP_RESULT R
                  LEFT JOIN danh_muc_he_thong_tai_khoan A1 ON "MA_TK_NO" = A1."SO_TAI_KHOAN"
                  LEFT JOIN danh_muc_he_thong_tai_khoan A2 ON "MA_TK_CO" = A2."SO_TAI_KHOAN"
                ORDER BY "NGAY_HACH_TOAN",
                  "NGAY_CHUNG_TU",
                  "SO_CHUNG_TU";


          END $$;

          SELECT *
          FROM TMP_KET_QUA;

        """  

        return self.execute(query, params)
        
