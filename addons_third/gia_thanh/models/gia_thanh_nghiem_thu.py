# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import timedelta, datetime

class GIA_THANH_NGHIEM_THU(models.Model):
    _name = 'gia.thanh.nghiem.thu'
    _description = 'Giá thành nghiệm thu'
    _inherit = ['mail.thread']
    KY_TINH_GIA_THANH = fields.Char(string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',default=fields.Datetime.now)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='gia_thanh_nghiem_thu_cong_trinh_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU', oldname='NAME')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',compute='tinh_tong_tien', store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS = fields.One2many('gia.thanh.nghiem.thu.hach.toan', 'CHI_TIET_ID', string='Nghiệm thu công trình hạch toán')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    
    @api.depends('GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien = 0.0
            for line in order.GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS:
                tong_tien += line.GIA_TRI_NGHIEM_THU
            order.update({
                'SO_TIEN': tong_tien,
            })


    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
        self.write({'state':'da_ghi_so'})


    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU': self.LOAI_CHUNG_TU,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.GIA_TRI_NGHIEM_THU,
                'GHI_NO_NGUYEN_TE' : line.GIA_TRI_NGHIEM_THU,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
                'HOP_DONG_BAN_ID' : line.HOP_DONG_BAN_ID.id,
                'DON_DAT_HANG_ID' : line.SO_DON_HANG_ID.id,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.GIA_TRI_NGHIEM_THU,
                'GHI_CO_NGUYEN_TE' : line.GIA_TRI_NGHIEM_THU,
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
        thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True


            
    @api.model
    def default_get(self, fields):
        rec = super(GIA_THANH_NGHIEM_THU, self).default_get(fields)
    #     GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS_default = self.get_context('default_GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS')
    #     if GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS_default:
    #         rec['GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS'] = GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS_default

    #     ky_tinh_gia_thanh_default = self.get_context('default_KY_TINH_GIA_THANH')
    #     ky_tinh_gia_thanh_id_default = self.get_context('default_KY_TINH_GIA_THANH_ID')
    #     loai_chung_tu = self.get_context('loai_chung_tu')
    # # Nghiệm thu hợp đồng
    #     # Trường hợp chọn từ form tham số
    #     if ky_tinh_gia_thanh_default:
    #         rec['KY_TINH_GIA_THANH'] = ky_tinh_gia_thanh_default
    #     if ky_tinh_gia_thanh_id_default:
    #         id_ky_tinh_gia_thanh = int(ky_tinh_gia_thanh_id_default)
    #         rec['KY_TINH_GIA_THANH_ID'] = id_ky_tinh_gia_thanh
    #         ky_tinh_gia_thanh = self.env['gia.thanh.ky.tinh.gia.thanh'].search([('id', '=', id_ky_tinh_gia_thanh)],limit=1)
            
    #         if ky_tinh_gia_thanh:
    #             if loai_chung_tu == 4092:
    #                 rec['LOAI_CHUNG_TU'] = loai_chung_tu
    #                 rec['DIEN_GIAI'] = 'Nghiệm thu giá vốn hợp đồng kỳ tính giá thành từ ngày ' + datetime.strptime(ky_tinh_gia_thanh.TU_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y') + ' đến ngày ' + datetime.strptime(ky_tinh_gia_thanh.DEN_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y')
    #             elif loai_chung_tu == 4091:
    #                 rec['LOAI_CHUNG_TU'] = loai_chung_tu
    #                 rec['DIEN_GIAI'] = 'Nghiệm thu giá vốn đơn hàng kỳ tính giá thành từ ngày ' + datetime.strptime(ky_tinh_gia_thanh.TU_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y') + ' đến ngày ' + datetime.strptime(ky_tinh_gia_thanh.DEN_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y')
    #             elif loai_chung_tu == 4090:
    #                 rec['LOAI_CHUNG_TU'] = loai_chung_tu
    #                 rec['DIEN_GIAI'] = 'Nghiệm thu giá vốn công trình kỳ tính giá thành từ ngày ' + datetime.strptime(ky_tinh_gia_thanh.TU_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y') + ' đến ngày ' + datetime.strptime(ky_tinh_gia_thanh.DEN_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y')
    #             rec['NGAY_HACH_TOAN'] = ky_tinh_gia_thanh.DEN_NGAY
    #             rec['NGAY_CHUNG_TU'] = ky_tinh_gia_thanh.DEN_NGAY

        return rec

    def lay_du_lieu_nghiep_thu_chi_tiet(self, args):
        new_line = [[5]]
        ky_tinh_gia_thanh_id = args.get('ky_tinh_gia_thanh_id')
        arr_chi_tiet = args.get('arr_chi_tiet_id')
        chi_nhanh_id = self.get_chi_nhanh()
        du_lieu_ky_tinh_gia_thanh = self.lay_du_lieu_ky_tinh_gia_thanh(ky_tinh_gia_thanh_id,chi_nhanh_id)
        if du_lieu_ky_tinh_gia_thanh:
            for line in du_lieu_ky_tinh_gia_thanh:
                chi_tiet_id = 0
                dien_giai = ''
                if args.get('loai_nghiem_thu') == 'cong_trinh':
                    chi_tiet_id = line.get('CONG_TRINH_ID')
                    dien_giai = 'Nghiệm thu công trình ' + line.get('TEN_CONG_TRINH')
                elif args.get('loai_nghiem_thu') == 'don_hang':
                    chi_tiet_id = line.get('DON_DAT_HANG_ID')
                    dien_giai = 'Nghiệm thu công trình ' + line.get('SO_DON_HANG')
                elif args.get('loai_nghiem_thu') == 'hop_dong':
                    chi_tiet_id = line.get('HOP_DONG_ID')
                    dien_giai = 'Nghiệm thu công trình ' + line.get('SO_HOP_DONG')
                if chi_tiet_id in arr_chi_tiet:
                    loai_ct = self.env['danh.muc.loai.cong.trinh'].browse(line.get('LOAI_CONG_TRINH'))
                    tk_no = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', line.get('TK_NO'))],limit=1)
                    tk_co = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', line.get('TK_CO'))],limit=1)
                    new_line += [(0,0,{
                        'MA_CONG_TRINH_ID' : [line.get('CONG_TRINH_ID'),line.get('MA_CONG_TRINH')],
                        'TEN_CONG_TRINH' : line.get('TEN_CONG_TRINH'),
                        'LOAI_CONG_TRINH' : [line.get('LOAI_CONG_TRINH'),loai_ct.name],

                        'SO_DON_HANG_ID' : [line.get('DON_DAT_HANG_ID'),line.get('SO_DON_HANG')],
                        'NGAY_DON_HANG' : line.get('NGAY_DON_HANG'),
                        'KHACH_HANG' : [line.get('KHACH_HANG_ID'),line.get('TEN_KHACH_HANG')],
                        'HOP_DONG_BAN_ID' : [line.get('HOP_DONG_ID'),line.get('SO_HOP_DONG')],
                        'NGAY_KY' : line.get('NGAY_KY'),
                        'TRICH_YEU' : line.get('TRICH_YEU'),

                        'DIEN_GIAI' : dien_giai,
                        'TK_NO_ID' : [tk_no.id,line.get('TK_NO')],
                        'TK_CO_ID' : [tk_co.id,line.get('TK_CO')],
                        'DOANH_THU' : line.get('DOANH_THU'),
                        'SO_CHUA_NGHIEM_THU' : line.get('SO_CHUA_NGHIEM_THU'),
                        'PHAN_TRAM_NGHIEM_THU' : 100,
                        'GIA_TRI_NGHIEM_THU' : line.get('SO_CHUA_NGHIEM_THU'),
                        # 'KHOAN_MUC_CP_ID' : line.get('DOANH_THU'),
                        # 'MA_THONG_KE_ID' : line.get('SO_CHUA_NGHIEM_THU'),
                        })]
        return {'GIA_THANH_NGHIEM_THU_HACH_TOAN_IDS':new_line}





    def lay_du_lieu_ky_tinh_gia_thanh(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
        params = {
            'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
            'CHI_NHANH_ID' : chi_nhanh_id,
            }
        query = """   
                DO LANGUAGE plpgsql $$
                DECLARE

                    ky_tinh_gia_thanh_id                              INTEGER := %(KY_TINH_GIA_THANH_ID)s;


                    chi_nhanh_id                                      INTEGER := %(CHI_NHANH_ID)s;

                    CHE_DO_KE_TOAN                                    VARCHAR;

                    tu_ngay                                           TIMESTAMP;

                    den_ngay                                          TIMESTAMP;

                    LOAI_GIA_THANH                                    VARCHAR;


                    MA_PHAN_CAPMTC                                    VARCHAR(100);

                    MA_PHAN_CAPCPSX                                   VARCHAR(100);

                    TK_CO_154                                         VARCHAR(100);

                    TK_NO_632                                         VARCHAR(100);

                    LAY_DU_LIEU_CUA_DOI_TUONG_THUOC_KY_TINH_GIA_THANH BOOLEAN := FALSE ;

                    DS_DOI_TUONG                                      VARCHAR [] :=ARRAY ['danh_muc_cong_trinh,', 'account_ex_don_dat_hang,','sale_ex_hop_dong_ban,'];

                BEGIN

                    SELECT value
                    INTO CHE_DO_KE_TOAN
                    FROM ir_config_parameter
                    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                    FETCH FIRST 1 ROW ONLY
                    ;

                    SELECT "TU_NGAY"
                    INTO tu_ngay
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    SELECT "DEN_NGAY"
                    INTO den_ngay
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    SELECT "LOAI_GIA_THANH"
                    INTO LOAI_GIA_THANH
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;


                    SELECT "SO_TAI_KHOAN"
                    INTO TK_CO_154
                    FROM danh_muc_he_thong_tai_khoan
                    WHERE "SO_TAI_KHOAN" LIKE '154%%'
                        AND "LA_TK_TONG_HOP" = FALSE
                    ORDER BY "SO_TAI_KHOAN"
                    LIMIT 1
                    ;

                    SELECT "SO_TAI_KHOAN"
                    INTO TK_NO_632
                    FROM danh_muc_he_thong_tai_khoan
                    WHERE "SO_TAI_KHOAN" LIKE '632%%'
                        AND "LA_TK_TONG_HOP" = FALSE
                    ORDER BY "SO_TAI_KHOAN"
                    LIMIT 1
                    ;


                    --         LOAI_GIA_THANH = 'DON_HANG'
                    --         ;


                    --1. Lấy danh sách các ĐTTTHCP (là công trình/đơn hàng/hợp đồng) trong kỳ tính giá thành

                    DROP TABLE IF EXISTS TMP_KY_TINH_GIA_THANH_CHI_TIET
                    ;

                    CREATE TEMP TABLE TMP_KY_TINH_GIA_THANH_CHI_TIET


                    (
                        "KY_TINH_GIA_THANH_CHI_TIET_ID" INT,
                        "KY_TINH_GIA_THANH_ID"          INT,
                        "DOI_TUONG_THCP_ID"             INT,
                        "CONG_TRINH_ID"                 INT,
                        "DON_DAT_HANG_ID"               INT,
                        "HOP_DONG_ID"                   INT,

                        "DOANH_THU_THUAN"               DECIMAL(22, 4),
                        "SO_TIEN"                       DECIMAL(22, 4)
                    )
                    ;

                    /*Danh sách các đối tượng tính giá thành để lấy dữ liệu*/

                    DROP TABLE IF EXISTS TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH
                    ;

                    CREATE TEMP TABLE TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH


                    (
                        "KY_TINH_GIA_THANH_ID" INT,
                        "DOI_TUONG_THCP_ID"    INT,
                        "CONG_TRINH_ID"        INT,
                        "DON_DAT_HANG_ID"      INT,
                        "HOP_DONG_ID"          INT
                    )
                    ;

                    IF LAY_DU_LIEU_CUA_DOI_TUONG_THUOC_KY_TINH_GIA_THANH = TRUE
                    /*Khi thực hiện load theo một list các đối tượng truyền xuống thì lấy dữ liệu cho tất cả các đối tượng truyền xuống*/
                    THEN

                        IF LOAI_GIA_THANH = 'CONG_TRINH'
                        THEN

                            INSERT INTO TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH
                            ("KY_TINH_GIA_THANH_ID",
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , NULL
                                    , id
                                    , NULL
                                    , NULL
                                FROM danh_muc_cong_trinh
                                WHERE ('danh_muc_cong_trinh,' || id) = ANY (DS_DOI_TUONG)
                            ;
                        ELSE IF LOAI_GIA_THANH = 'DON_HANG'
                            THEN

                                INSERT INTO TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH
                                ("KY_TINH_GIA_THANH_ID",
                                "DOI_TUONG_THCP_ID",
                                "CONG_TRINH_ID",
                                "DON_DAT_HANG_ID",
                                "HOP_DONG_ID"
                                )
                                    SELECT
                                        ky_tinh_gia_thanh_id
                                        , NULL
                                        , NULL
                                        , id
                                        , NULL
                                    FROM account_ex_don_dat_hang
                                    WHERE ('account_ex_don_dat_hang,' || id) = ANY (DS_DOI_TUONG)
                                ;

                        ELSE IF LOAI_GIA_THANH = 'HOP_DONG'
                            THEN

                                INSERT INTO TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH
                                ("KY_TINH_GIA_THANH_ID",
                                "DOI_TUONG_THCP_ID",
                                "CONG_TRINH_ID",
                                "DON_DAT_HANG_ID",
                                "HOP_DONG_ID"
                                )
                                    SELECT
                                        ky_tinh_gia_thanh_id
                                        , NULL
                                        , NULL
                                        , NULL
                                        , id
                                    FROM sale_ex_hop_dong_ban
                                    WHERE ('sale_ex_hop_dong_ban,' || id) = ANY (DS_DOI_TUONG)
                                ;
                        END IF
                        ;
                    END IF ;
                            END IF ;








                    ELSE

                        INSERT INTO TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH
                        ("KY_TINH_GIA_THANH_ID",
                        "DOI_TUONG_THCP_ID",
                        "CONG_TRINH_ID",
                        "DON_DAT_HANG_ID",
                        "HOP_DONG_ID"
                        )
                            SELECT
                                ky_tinh_gia_thanh_id
                                , JPD."MA_DOI_TUONG_THCP_ID"
                                , JPD."MA_CONG_TRINH_ID"
                                , JPD."SO_DON_HANG_ID"
                                , JPD."SO_HOP_DONG_ID"
                            FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                            WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                        ;
                    END IF
                    ;

                    --2. Lấy số liệu trên JCOPN
                    --Để đảm bảo Rule cứ có khai báo là lấy lên thì ta sẽ lấy số đầu kỳ ở 2 tập: 1 là trong bảng số dư đầu kỳ Công trình,Hợp đồng,Đơn hàng. 2 là trong bảng JC"PHAT_SINH_TRONG_KY"Detail
                    IF LOAI_GIA_THANH = 'CONG_TRINH'
                    THEN
                        INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                        ("KY_TINH_GIA_THANH_ID",
                        "DOI_TUONG_THCP_ID",
                        "CONG_TRINH_ID",
                        "DON_DAT_HANG_ID",
                        "HOP_DONG_ID",
                        "DOANH_THU_THUAN",
                        "SO_TIEN"
                        )
                            SELECT
                                JPD."KY_TINH_GIA_THANH_ID"
                                , JPD."DOI_TUONG_THCP_ID"
                                , JPD."CONG_TRINH_ID"
                                , JPD."DON_DAT_HANG_ID"
                                , JPD."HOP_DONG_ID"
                                , 0 AS "DOANH_THU_THUAN"
                                , SUM(COALESCE(OP."SO_CHUA_NGHIEM_THU", 0))
                            FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD

                                LEFT JOIN account_ex_chi_phi_do_dang OP ON JPD."CONG_TRINH_ID" = OP."MA_CONG_TRINH_ID"
                                                                        AND OP."CHI_NHANH_ID" = chi_nhanh_id

                                                                        AND (SELECT "SO_TAI_KHOAN"
                                                                                FROM danh_muc_he_thong_tai_khoan TK
                                                                                WHERE TK.id = OP."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
                                                                            N'154%%'
                            GROUP BY
                                JPD."KY_TINH_GIA_THANH_ID",
                                JPD."DOI_TUONG_THCP_ID",
                                JPD."CONG_TRINH_ID",
                                JPD."DON_DAT_HANG_ID",
                                JPD."HOP_DONG_ID"
                        ;


                    ELSE IF LOAI_GIA_THANH = 'DON_HANG'
                    THEN
                        INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                        ("KY_TINH_GIA_THANH_ID",
                        "DOI_TUONG_THCP_ID",
                        "CONG_TRINH_ID",
                        "DON_DAT_HANG_ID",
                        "HOP_DONG_ID",
                        "DOANH_THU_THUAN",
                        "SO_TIEN"
                        )
                            SELECT
                                JPD."KY_TINH_GIA_THANH_ID"
                                , JPD."DOI_TUONG_THCP_ID"
                                , JPD."CONG_TRINH_ID"
                                , JPD."DON_DAT_HANG_ID"
                                , JPD."HOP_DONG_ID"
                                , 0 AS "DOANH_THU_THUAN"
                                , SUM(COALESCE(OP."SO_CHUA_NGHIEM_THU", 0))
                            FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                LEFT JOIN account_ex_chi_phi_do_dang OP ON JPD."DON_DAT_HANG_ID" = OP."DON_HANG_ID"
                                                                        AND OP."CHI_NHANH_ID" = chi_nhanh_id

                                                                        AND (SELECT "SO_TAI_KHOAN"
                                                                                FROM danh_muc_he_thong_tai_khoan TK
                                                                                WHERE TK.id = OP."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
                                                                            N'154%%'

                            GROUP BY
                                JPD."KY_TINH_GIA_THANH_ID",
                                JPD."DOI_TUONG_THCP_ID",
                                JPD."CONG_TRINH_ID",
                                JPD."DON_DAT_HANG_ID",
                                JPD."HOP_DONG_ID"
                        ;


                    ELSE IF LOAI_GIA_THANH = 'HOP_DONG'
                    THEN
                        INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                        ("KY_TINH_GIA_THANH_ID",
                        "DOI_TUONG_THCP_ID",
                        "CONG_TRINH_ID",
                        "DON_DAT_HANG_ID",
                        "HOP_DONG_ID",
                        "DOANH_THU_THUAN",
                        "SO_TIEN"
                        )
                            SELECT
                                JPD."KY_TINH_GIA_THANH_ID"
                                , JPD."DOI_TUONG_THCP_ID"
                                , JPD."CONG_TRINH_ID"
                                , JPD."DON_DAT_HANG_ID"
                                , JPD."HOP_DONG_ID"
                                , 0 AS "DOANH_THU_THUAN"
                                , SUM(COALESCE(OP."SO_CHUA_NGHIEM_THU", 0))
                            FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                LEFT JOIN account_ex_chi_phi_do_dang OP ON JPD."HOP_DONG_ID" = OP."HOP_DONG_ID"
                                                                        AND OP."CHI_NHANH_ID" = chi_nhanh_id

                                                                        AND (SELECT "SO_TAI_KHOAN"
                                                                                FROM danh_muc_he_thong_tai_khoan TK
                                                                                WHERE TK.id = OP."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
                                                                            N'154%%'

                            GROUP BY
                                JPD."KY_TINH_GIA_THANH_ID",
                                JPD."DOI_TUONG_THCP_ID",
                                JPD."CONG_TRINH_ID",
                                JPD."DON_DAT_HANG_ID",
                                JPD."HOP_DONG_ID"
                        ;
                    END IF
                        ;
                    END IF
                        ;
                    END IF
                    ;


                    IF (CHE_DO_KE_TOAN = '15')  --Thông tư 200
                    THEN
                        /*
                            QĐ 15 = Số chưa nghiệm thu trên form Nhập lũy kế chi phí phát sinh công trình kỳ trước
                                    + Tổng (PS Nợ -PS Có) của TK621, 622, 623, 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này (không kể PSDU Nợ TK 154/Có TK 621, 622, 623, 627 chi tiết theo từng công trình)
                                    + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của các kỳ tính giá thành có Đến ngày <= Đến ngày của kỳ tính giá thành này
                                    - PS Có TK 154 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này
                            */
                        --3. Lấy số liệu trên sổ
                        IF LOAI_GIA_THANH = 'CONG_TRINH'
                        THEN
                            INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                            ("KY_TINH_GIA_THANH_ID",
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID",
                            "DOANH_THU_THUAN",
                            "SO_TIEN"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , JPD."DOI_TUONG_THCP_ID"
                                    , JPD."CONG_TRINH_ID"
                                    , JPD."DON_DAT_HANG_ID"
                                    , JPD."HOP_DONG_ID"
                                    ,
                                    /*Doanh thu với QĐ 15: (PSC 511,711,515 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511,711,515)– PSN 511,711,515 (không bao gồm PS ĐƯ Nợ TK511,711,515/Có TK 911 và TK511/521))- PS Nợ 521+ PS Có 5211*/
                                    /*(PSC 511,711,515 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511,711,515) + PS Có 5211*/
                                    SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                            AND ((
                                        (GL."MA_TAI_KHOAN" LIKE N'511%%' OR GL."MA_TAI_KHOAN" LIKE N'515%%' OR
                                        GL."MA_TAI_KHOAN" LIKE N'711%%') AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%'
                                        OR GL."MA_TAI_KHOAN" LIKE N'5211%%'
                                    )
                                                            )
                                        THEN GL."GHI_CO"
                                                ELSE 0
                                                END
                                    , 0)
                                    )
                                    /*PSN 511,711,515 (không bao gồm PS ĐƯ Nợ TK511,711,515/Có TK 911 và TK511/521) + PS Nợ 521*/
                                    - SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                            AND ((GL."MA_TAI_KHOAN" LIKE N'511%%' AND
                                                                    GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%' AND
                                                                    GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'521%%')
                                                                    OR ((GL."MA_TAI_KHOAN" LIKE N'515%%' OR
                                                                        GL."MA_TAI_KHOAN" LIKE N'711%%') AND
                                                                        GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%')
                                                                    OR GL."MA_TAI_KHOAN" LIKE N'521%%'
                                                            )
                                        THEN GL."GHI_NO"
                                                    ELSE 0
                                                    END
                                    , 0)
                                    )              AS "DOANH_THU_THUAN"
                                    , SUM(COALESCE(
                                            (--Tổng (PS Nợ -PS Có) của TK621, 622, 623, 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này (không kể PSDU Nợ TK 154/Có TK 621, 622, 623, 627 chi tiết theo từng công trình)
                                                CASE WHEN (((GL."MA_TAI_KHOAN" LIKE '621%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '623%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '622%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '627%%')

                                                            ) AND
                                                            ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2')
                                                            OR GL."LOAI_HACH_TOAN" = '1')
                                                            OR ("MA_TAI_KHOAN" LIKE N'154%%'
                                                                AND "LOAI_HACH_TOAN" = '1'
                                                                AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%')
                                                ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                                                    THEN (Gl."GHI_NO" - GL."GHI_CO")
                                                --- PS Có TK 154 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này
                                                WHEN (GL."MA_TAI_KHOAN" LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2')
                                                    THEN -GL."GHI_CO"
                                                ELSE 0
                                                END
                                            ), 0)) AS "SO_TIEN"
                                FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                    LEFT JOIN so_cai_chi_tiet GL ON GL."CONG_TRINH_ID" = JPD."CONG_TRINH_ID" -- Công trình
                                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                    AND ("MA_TAI_KHOAN" LIKE N'511%%'
                                        OR "MA_TAI_KHOAN" LIKE N'711%%'
                                        OR "MA_TAI_KHOAN" LIKE N'515%%'
                                        OR "MA_TAI_KHOAN" LIKE N'521%%'
                                        OR "MA_TAI_KHOAN" LIKE N'62%%'
                                        OR "MA_TAI_KHOAN" LIKE N'154%%'
                                    )
                                    AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                    AND GL."CHI_NHANH_ID" = chi_nhanh_id

                                    AND GL."CONG_TRINH_ID" IS NOT NULL

                                    AND (GL."LOAI_CHUNG_TU" <> '610' OR
                                        (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))
                                GROUP BY
                                    JPD."KY_TINH_GIA_THANH_ID",
                                    JPD."DOI_TUONG_THCP_ID",
                                    JPD."CONG_TRINH_ID",
                                    JPD."DON_DAT_HANG_ID",
                                    JPD."HOP_DONG_ID"
                            ;


                        ELSE IF LOAI_GIA_THANH = 'DON_HANG'
                        THEN
                            INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                            ("KY_TINH_GIA_THANH_ID",
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID",
                            "DOANH_THU_THUAN",
                            "SO_TIEN"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , JPD."DOI_TUONG_THCP_ID"
                                    , JPD."CONG_TRINH_ID"
                                    , JPD."DON_DAT_HANG_ID"
                                    , JPD."HOP_DONG_ID"
                                    ,
                                    /*Doanh thu với QĐ 15: (PSC 511,711,515 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511,711,515)– PSN 511,711,515 (không bao gồm PS ĐƯ Nợ TK511,711,515/Có TK 911 và TK511/521))- PS Nợ 521+ PS Có 5211*/
                                    /*(PSC 511,711,515 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511,711,515) + PS Có 5211*/
                                    SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                            AND ((
                                        (GL."MA_TAI_KHOAN" LIKE N'511%%' OR GL."MA_TAI_KHOAN" LIKE N'515%%' OR
                                        GL."MA_TAI_KHOAN" LIKE N'711%%') AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%'
                                        OR GL."MA_TAI_KHOAN" LIKE N'5211%%'
                                    )
                                                            )
                                        THEN GL."GHI_CO"
                                                ELSE 0
                                                END
                                    , 0)
                                    )
                                    /*PSN 511,711,515 (không bao gồm PS ĐƯ Nợ TK511,711,515/Có TK 911 và TK511/521) + PS Nợ 521*/
                                    - SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                            AND ((GL."MA_TAI_KHOAN" LIKE N'511%%' AND
                                                                    GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%' AND
                                                                    GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'521%%')
                                                                    OR ((GL."MA_TAI_KHOAN" LIKE N'515%%' OR
                                                                        GL."MA_TAI_KHOAN" LIKE N'711%%') AND
                                                                        GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%')
                                                                    OR GL."MA_TAI_KHOAN" LIKE N'521%%'
                                                            )
                                        THEN GL."GHI_NO"
                                                    ELSE 0
                                                    END
                                    , 0)
                                    )              AS "DOANH_THU_THUAN"
                                    , SUM(COALESCE(
                                            (--Tổng (PS Nợ -PS Có) của TK621, 622, 623, 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này (không kể PSDU Nợ TK 154/Có TK 621, 622, 623, 627 chi tiết theo từng công trình)
                                                CASE WHEN (((GL."MA_TAI_KHOAN" LIKE '621%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '622%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '627%%')
                                                            ) AND
                                                            ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2')
                                                            OR GL."LOAI_HACH_TOAN" = '1'
                                                            )
                                                            OR ("MA_TAI_KHOAN" LIKE N'154%%'
                                                                AND "LOAI_HACH_TOAN" = '1'
                                                                AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%')
                                                ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                                                    THEN (Gl."GHI_NO" - GL."GHI_CO")
                                                --- PS Có TK 154 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này
                                                WHEN (GL."MA_TAI_KHOAN" LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2')
                                                    THEN -GL."GHI_CO"
                                                ELSE 0
                                                END

                                            ), 0)) AS "SO_TIEN"
                                FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                    LEFT JOIN so_cai_chi_tiet GL ON GL."DON_DAT_HANG_ID" = JPD."DON_DAT_HANG_ID"
                                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                    AND ("MA_TAI_KHOAN" LIKE N'511%%'
                                        OR "MA_TAI_KHOAN" LIKE N'711%%'
                                        OR "MA_TAI_KHOAN" LIKE N'515%%'
                                        OR "MA_TAI_KHOAN" LIKE N'521%%'
                                        OR "MA_TAI_KHOAN" LIKE N'62%%'
                                        OR "MA_TAI_KHOAN" LIKE N'154%%'
                                    )
                                    AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                    AND GL."CHI_NHANH_ID" = chi_nhanh_id

                                    AND GL."DON_DAT_HANG_ID" IS NOT NULL

                                    AND (GL."LOAI_CHUNG_TU" <> '610' OR
                                        (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))
                                GROUP BY
                                    JPD."KY_TINH_GIA_THANH_ID",
                                    JPD."DOI_TUONG_THCP_ID",
                                    JPD."CONG_TRINH_ID",
                                    JPD."DON_DAT_HANG_ID",
                                    JPD."HOP_DONG_ID"
                            ;


                        ELSE IF LOAI_GIA_THANH = 'HOP_DONG'
                        THEN
                            INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                            ("KY_TINH_GIA_THANH_ID",
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID",
                            "DOANH_THU_THUAN",
                            "SO_TIEN"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , JPD."DOI_TUONG_THCP_ID"
                                    , JPD."CONG_TRINH_ID"
                                    , JPD."DON_DAT_HANG_ID"
                                    , JPD."HOP_DONG_ID"
                                    ,
                                    /*Doanh thu với QĐ 15: (PSC 511,711,515 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511,711,515)– PSN 511,711,515 (không bao gồm PS ĐƯ Nợ TK511,711,515/Có TK 911 và TK511/521))- PS Nợ 521+ PS Có 5211*/
                                    /*(PSC 511,711,515 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511,711,515) + PS Có 5211*/
                                    SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                            AND ((
                                        (GL."MA_TAI_KHOAN" LIKE N'511%%' OR GL."MA_TAI_KHOAN" LIKE N'515%%' OR
                                        GL."MA_TAI_KHOAN" LIKE N'711%%') AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%'
                                        OR GL."MA_TAI_KHOAN" LIKE N'5211%%'
                                    )
                                                            )
                                        THEN GL."GHI_CO"
                                                ELSE 0
                                                END
                                    , 0)
                                    )
                                    /*PSN 511,711,515 (không bao gồm PS ĐƯ Nợ TK511,711,515/Có TK 911 và TK511/521) + PS Nợ 521*/
                                    - SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                            AND ((GL."MA_TAI_KHOAN" LIKE N'511%%' AND
                                                                    GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%' AND
                                                                    GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'521%%')
                                                                    OR ((GL."MA_TAI_KHOAN" LIKE N'515%%' OR
                                                                        GL."MA_TAI_KHOAN" LIKE N'711%%') AND
                                                                        GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%')
                                                                    OR GL."MA_TAI_KHOAN" LIKE N'521%%'
                                                            )
                                        THEN GL."GHI_NO"
                                                    ELSE 0
                                                    END
                                    , 0)
                                    )              AS "DOANH_THU_THUAN"
                                    , SUM(COALESCE(
                                            (--Tổng (PS Nợ -PS Có) của TK621, 622, 623, 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này (không kể PSDU Nợ TK 154/Có TK 621, 622, 623, 627 chi tiết theo từng công trình)
                                                CASE WHEN (((GL."MA_TAI_KHOAN" LIKE '621%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '622%%')
                                                            OR (GL."MA_TAI_KHOAN" LIKE '627%%')
                                                            ) AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                                    AND GL."LOAI_HACH_TOAN" = '2') OR GL."LOAI_HACH_TOAN" = '1')
                                                            OR ("MA_TAI_KHOAN" LIKE N'154%%'
                                                                AND "LOAI_HACH_TOAN" = '1'
                                                                AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%')
                                                ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                                                    THEN (Gl."GHI_NO" - GL."GHI_CO")
                                                --- PS Có TK 154 chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này
                                                WHEN (GL."MA_TAI_KHOAN" LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2')
                                                    THEN -GL."GHI_CO"
                                                ELSE 0
                                                END

                                            ), 0)) AS "SO_TIEN"
                                FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                    LEFT JOIN so_cai_chi_tiet GL ON GL."HOP_DONG_BAN_ID" = JPD."HOP_DONG_ID"
                                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                    AND ("MA_TAI_KHOAN" LIKE N'511%%'
                                        OR "MA_TAI_KHOAN" LIKE N'711%%'
                                        OR "MA_TAI_KHOAN" LIKE N'515%%'
                                        OR "MA_TAI_KHOAN" LIKE N'521%%'
                                        OR "MA_TAI_KHOAN" LIKE N'62%%'
                                        OR "MA_TAI_KHOAN" LIKE N'154%%'
                                    )
                                    AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                    AND GL."CHI_NHANH_ID" = chi_nhanh_id

                                    AND GL."HOP_DONG_BAN_ID" IS NOT NULL

                                    AND (GL."LOAI_CHUNG_TU" <> '610' OR
                                        (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))
                                GROUP BY
                                    JPD."KY_TINH_GIA_THANH_ID",
                                    JPD."DOI_TUONG_THCP_ID",
                                    JPD."CONG_TRINH_ID",
                                    JPD."DON_DAT_HANG_ID",
                                    JPD."HOP_DONG_ID"
                            ;
                        END IF
                            ;
                        END IF
                            ;
                        END IF
                        ;

                        --4. Lấy số liệu trên phân bổ (chú ý: Lấy số liệu của tất cả các lần phân bổ mà có kỳ tính giá thành có Đến ngày<= den_ngay)
                        IF LOAI_GIA_THANH = 'CONG_TRINH'
                        THEN
                            INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                            (
                                "KY_TINH_GIA_THANH_ID",
                                "DOI_TUONG_THCP_ID",
                                "CONG_TRINH_ID",
                                "DON_DAT_HANG_ID",
                                "HOP_DONG_ID",
                                "DOANH_THU_THUAN",
                                "SO_TIEN"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , JPD."DOI_TUONG_THCP_ID"
                                    , JPD."CONG_TRINH_ID"
                                    , JPD."DON_DAT_HANG_ID"
                                    , JPD."HOP_DONG_ID"
                                    , 0
                                    , SUM(COALESCE(J."SO_TIEN", 0))
                                FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                    LEFT JOIN (SELECT
                                                JA.*
                                                , JP."DEN_NGAY"
                                            FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JA
                                                INNER JOIN gia_thanh_ky_tinh_gia_thanh JP ON JA."KY_TINH_GIA_THANH_ID" = JP."id"
                                            WHERE JP."CHI_NHANH_ID" = chi_nhanh_id
                                                    AND JP."DEN_NGAY" <= den_ngay

                                            ) AS J ON J."MA_CONG_TRINH_ID" = JPD."CONG_TRINH_ID"
                                WHERE J."DEN_NGAY" <= den_ngay
                                    AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                                    AND
                                    (
                                        ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '621%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '622%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '627%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '623%%')
                                    )
                                GROUP BY
                                    JPD."KY_TINH_GIA_THANH_ID",
                                    JPD."DOI_TUONG_THCP_ID",
                                    JPD."CONG_TRINH_ID",
                                    JPD."DON_DAT_HANG_ID",
                                    JPD."HOP_DONG_ID"
                            ;


                        ELSE IF LOAI_GIA_THANH = 'DON_HANG'
                        THEN
                            INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                            (
                                "KY_TINH_GIA_THANH_ID",
                                "DOI_TUONG_THCP_ID",
                                "CONG_TRINH_ID",
                                "DON_DAT_HANG_ID",
                                "HOP_DONG_ID",
                                "DOANH_THU_THUAN",
                                "SO_TIEN"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , JPD."DOI_TUONG_THCP_ID"
                                    , JPD."CONG_TRINH_ID"
                                    , JPD."DON_DAT_HANG_ID"
                                    , JPD."HOP_DONG_ID"
                                    , 0
                                    , SUM(COALESCE(J."SO_TIEN", 0))
                                FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                    LEFT JOIN (SELECT
                                                JA.*
                                                , JP."DEN_NGAY"
                                            FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JA
                                                INNER JOIN gia_thanh_ky_tinh_gia_thanh JP ON JA."KY_TINH_GIA_THANH_ID" = JP."id"
                                            WHERE JP."CHI_NHANH_ID" = chi_nhanh_id
                                                    AND JP."DEN_NGAY" <= den_ngay

                                            ) AS J ON J."SO_DON_HANG_ID" = JPD."DON_DAT_HANG_ID"
                                WHERE J."DEN_NGAY" <= den_ngay
                                    AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                                    AND
                                    (
                                        ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '621%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '622%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '627%%')
                                    )
                                GROUP BY
                                    JPD."KY_TINH_GIA_THANH_ID",
                                    JPD."DOI_TUONG_THCP_ID",
                                    JPD."CONG_TRINH_ID",
                                    JPD."DON_DAT_HANG_ID",
                                    JPD."HOP_DONG_ID"
                            ;


                        ELSE IF LOAI_GIA_THANH = 'HOP_DONG'
                        THEN
                            INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                            (
                                "KY_TINH_GIA_THANH_ID",
                                "DOI_TUONG_THCP_ID",
                                "CONG_TRINH_ID",
                                "DON_DAT_HANG_ID",
                                "HOP_DONG_ID",
                                "DOANH_THU_THUAN",
                                "SO_TIEN"
                            )
                                SELECT
                                    ky_tinh_gia_thanh_id
                                    , JPD."DOI_TUONG_THCP_ID"
                                    , JPD."CONG_TRINH_ID"
                                    , JPD."DON_DAT_HANG_ID"
                                    , JPD."HOP_DONG_ID"
                                    , 0
                                    , SUM(COALESCE(J."SO_TIEN", 0))
                                FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                    LEFT JOIN (SELECT
                                                JA.*
                                                , JP."DEN_NGAY"
                                            FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JA
                                                INNER JOIN gia_thanh_ky_tinh_gia_thanh JP ON JA."KY_TINH_GIA_THANH_ID" = JP."id"
                                            WHERE JP."CHI_NHANH_ID" = chi_nhanh_id
                                                    AND JP."DEN_NGAY" <= den_ngay

                                            ) AS J ON J."SO_HOP_DONG_ID" = JPD."HOP_DONG_ID"
                                WHERE J."DEN_NGAY" <= den_ngay
                                    AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                                    AND
                                    (
                                        ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '621%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '622%%')
                                        OR ((SELECT "SO_TAI_KHOAN"
                                            FROM danh_muc_he_thong_tai_khoan TK
                                            WHERE TK.id = J."TAI_KHOAN_ID") LIKE '627%%')
                                    )
                                GROUP BY
                                    JPD."KY_TINH_GIA_THANH_ID",
                                    JPD."DOI_TUONG_THCP_ID",
                                    JPD."CONG_TRINH_ID",
                                    JPD."DON_DAT_HANG_ID",
                                    JPD."HOP_DONG_ID"
                            ;


                        END IF
                            ;
                        END IF
                            ;
                        END IF
                        ;

                    ELSE -- thông tư 133

                        SELECT "MA_PHAN_CAP"
                        INTO MA_PHAN_CAPCPSX
                        FROM danh_muc_khoan_muc_cp
                        WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                        ;


                        SELECT "MA_PHAN_CAP"
                        INTO MA_PHAN_CAPMTC
                        FROM danh_muc_khoan_muc_cp
                        WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                        ;

                        /*3. Lấy số liệu trên sổ
                        + Tổng (PS Nợ -PS Có) của TK 154 chi tiết theo KMCP sản xuất chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này
                        - PS Có TK 154 không chi tiết theo KMCP sản xuất có chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này
                        */
                        /*Lấy dữ liệu từ sổ của TT133*/


                        INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                        (
                            "KY_TINH_GIA_THANH_ID",
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID",
                            "DOANH_THU_THUAN",
                            "SO_TIEN"
                        )
                            SELECT
                                JPD."KY_TINH_GIA_THANH_ID"
                                , JPD."DOI_TUONG_THCP_ID"
                                , JPD."CONG_TRINH_ID"
                                , JPD."DON_DAT_HANG_ID"
                                , JPD."HOP_DONG_ID"
                                ,
                                /*[PS Có TK 511,515,711 không bao gồm PS ĐƯ Nợ TK 911/Có TK511,515,711, không kể các nghiệp vụ: Chiết khấu thương mại (bán hàng), Giảm giá hàng bán, Trả lại hàng bán  – PS Nợ TK 511,711,911 không bao gồm PS ĐƯ Nợ TK511,711,911/Có TK 911, không kể các nghiệp vụ: Chiết khấu thương mại (bán hàng), Giảm giá hàng bán, Trả lại hàng bán)] - [(PS N511 – PS Có TK 511) chi tiết các nghiệp vụ: Chiết khấu thương mại (bán hàng), Giảm giá hàng bán, Trả lại hàng bán]*/
                                SUM(COALESCE(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                    THEN
                                        (/*Doanh thu bán hàng: PS Có 511 - PS Nợ 511 (Không kể đối ứng với 911), không kể các nghiệp vụ chiết khấu*/
                                            CASE WHEN
                                                GL."MA_TAI_KHOAN" LIKE N'511%%' AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%' AND
                                                GL."LOAI_NGHIEP_VU" IS NULL
                                                THEN GL."GHI_CO" - GL."GHI_NO"
                                            /*Doanh thu khác: PS Có 515, 711 - PS Nợ 515, 711 (Không kể các phát sinh đối ứng với 911)*/
                                            WHEN (GL."MA_TAI_KHOAN" LIKE N'515%%' OR GL."MA_TAI_KHOAN" LIKE N'711%%') AND
                                                GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'911%%'
                                                THEN GL."GHI_CO" - GL."GHI_NO"
                                            /*Giảm trừ doanh thu: - (PS Nợ 511 - PS Có 511) chi tiết theo các khoản chiết khấu*/
                                            WHEN GL."MA_TAI_KHOAN" LIKE N'511%%' AND GL."LOAI_NGHIEP_VU" IS NOT NULL
                                                THEN -(GL."GHI_NO" - GL."GHI_CO")
                                            ELSE 0
                                            END
                                        )
                                            ELSE 0
                                            END
                                , 0)
                                )             AS "DOANH_THU_THUAN"
                                , SUM(
                                    COALESCE(/*|| Tổng (PS Nợ -PS Có) của TK 154 chi tiết theo KMCP sản xuất chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này */
                                        CASE WHEN GL."MA_TAI_KHOAN" LIKE '154%%' AND
                                                    (LOAI_GIA_THANH = 'CONG_TRINH' AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%'
                                                    OR
                                                    (LOAI_GIA_THANH = 'DON_HANG' AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%' AND
                                                    E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%')
                                                    OR
                                                    (LOAI_GIA_THANH = 'HOP_DONG' AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%' AND
                                                    E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%')
                                                    )
                                            THEN ("GHI_NO" - "GHI_CO")
                                        /*- PS Có TK 154 không chi tiết theo KMCP sản xuất có chi tiết theo từng công trình trên chứng từ có ngày hạch toán <= Đến ngày của kỳ tính giá thành này*/
                                        WHEN GL."MA_TAI_KHOAN" LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2' AND
                                            (GL."KHOAN_MUC_CP_ID" IS NULL OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPCPSX || '%%')
                                            THEN -GL."GHI_CO"
                                        ELSE 0
                                        END
                                        , 0)) AS "SO_TIEN"
                            FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                LEFT JOIN so_cai_chi_tiet GL
                                    ON ((LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" = JPD."CONG_TRINH_ID") -- Công trình
                                        OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" = JPD."DON_DAT_HANG_ID")-- Đơn hàng
                                        OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" = JPD."HOP_DONG_ID") -- Hợp đồng
                                    )
                                LEFT JOIN danh_muc_khoan_muc_cp E ON GL."KHOAN_MUC_CP_ID" = E."id"
                            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                AND (GL."MA_TAI_KHOAN" LIKE '154%%'
                                    OR "MA_TAI_KHOAN" LIKE N'511%%'
                                    OR "MA_TAI_KHOAN" LIKE N'711%%'
                                    OR "MA_TAI_KHOAN" LIKE N'515%%'
                                )
                                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                                AND -- Chi tiết theo ĐTTHCP
                                (
                                    (LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" IS NOT NULL)
                                    OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" IS NOT NULL)-- Đơn hàng
                                    OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" IS NOT NULL)-- Đơn hàng
                                )

                                AND
                                (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))
                            GROUP BY
                                JPD."KY_TINH_GIA_THANH_ID",
                                JPD."DOI_TUONG_THCP_ID",
                                JPD."CONG_TRINH_ID",
                                JPD."DON_DAT_HANG_ID",
                                JPD."HOP_DONG_ID"
                        ;


                        --4. Lấy số liệu trên phân bổ (chú ý: Lấy số liệu của tất cả các lần phân bổ mà có kỳ tính giá thành có Đến ngày<= den_ngay)
                        /*|| Tổng số tiền phân bổ của TK154 của các KMCP sản xuất cho từng công trình trên bảng phân bổ chi phí chung của các kỳ tính giá thành có Đến ngày <= Đến ngày của kỳ tính giá thành này*/
                        INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                        (
                            "KY_TINH_GIA_THANH_ID",
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID",
                            "DOANH_THU_THUAN",
                            "SO_TIEN"
                        )
                            SELECT

                                JPD."KY_TINH_GIA_THANH_ID"
                                , JPD."DOI_TUONG_THCP_ID"
                                , JPD."CONG_TRINH_ID"
                                , JPD."DON_DAT_HANG_ID"
                                , JPD."HOP_DONG_ID"
                                , 0
                                , SUM(COALESCE(J."SO_TIEN", 0))
                            FROM TMP_CHON_DOI_TUONG_KY_TINH_GIA_THANH JPD
                                LEFT JOIN (SELECT
                                            JA.*
                                            , JP."DEN_NGAY"
                                        FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JA
                                            INNER JOIN gia_thanh_ky_tinh_gia_thanh JP ON JA."KY_TINH_GIA_THANH_ID" = JP."id"
                                        WHERE JP."CHI_NHANH_ID" = chi_nhanh_id
                                        ) AS J ON (
                                    (LOAI_GIA_THANH = 'CONG_TRINH' AND J."MA_CONG_TRINH_ID" = JPD."CONG_TRINH_ID")
                                    OR (LOAI_GIA_THANH = 'DON_HANG' AND J."SO_DON_HANG_ID" = JPD."DON_DAT_HANG_ID")
                                    OR (LOAI_GIA_THANH = 'HOP_DONG' AND J."SO_HOP_DONG_ID" = JPD."HOP_DONG_ID")
                                    )
                            WHERE J."DEN_NGAY" <= den_ngay
                                AND JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id


                                AND J."KHOAN_MUC_CP_ID" IS NOT NULL
                                AND EXISTS(SELECT E."id"
                                            FROM danh_muc_khoan_muc_cp E
                                            WHERE (E."id" = J."KHOAN_MUC_CP_ID")
                                                AND ((LOAI_GIA_THANH = 'CONG_TRINH' AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%')
                                                        OR (LOAI_GIA_THANH = 'DON_HANG' AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%'
                                                            AND
                                                            E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%')
                                                        OR (LOAI_GIA_THANH = 'HOP_DONG' AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%'
                                                            AND
                                                            E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%')
                                                )
                                )

                            GROUP BY
                                JPD."KY_TINH_GIA_THANH_ID",
                                JPD."DOI_TUONG_THCP_ID",
                                JPD."CONG_TRINH_ID",
                                JPD."DON_DAT_HANG_ID",
                                JPD."HOP_DONG_ID"
                        ;


                    END IF
                    ;

                    --5. Lấy dữ liệu đổ ra


                    DROP TABLE IF EXISTS TMP_KET_QUA
                    ;

                    CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT

                            ROW_NUMBER()
                            OVER (
                                ORDER BY
                                    P."MA_CONG_TRINH",
                                    P."TEN_CONG_TRINH",
                                    P."LOAI_CONG_TRINH",
                                    SO."SO_DON_HANG",
                                    SO."NGAY_DON_HANG",
                                    SO."TEN_KHACH_HANG",
                                    C."SO_HOP_DONG",
                                    C."NGAY_KY",
                                    C."TEN_KHACH_HANG",
                                    C."TRICH_YEU",
                                    C."NGUOI_LIEN_HE",
                                    P."LOAI_CONG_TRINH",
                                    JC."DOI_TUONG_THCP_ID",
                                    SUM(JC."SO_TIEN"
                                    )
                                )                    AS "RowNumber"

                            , 0                        AS "KY_TINH_GIA_THANH_CHI_TIET_ID"
                            , ky_tinh_gia_thanh_id     AS "KY_TINH_GIA_THANH_ID"
                            , JC."CONG_TRINH_ID"
                            , P."MA_CONG_TRINH"
                            , P."TEN_CONG_TRINH"
                            , P."LOAI_CONG_TRINH" AS "LOAI_CONG_TRINH"
                            , JC."DON_DAT_HANG_ID"
                            , SO."SO_DON_HANG"
                            , SO."NGAY_DON_HANG"
                            , TK_NO_632                AS "TK_NO"
                            , TK_CO_154                AS "TK_CO"
                            , (
                                CASE
                                WHEN LOAI_GIA_THANH = 'DON_HANG'
                                    THEN SO."TEN_KHACH_HANG"
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN C."TEN_KHACH_HANG"
                                ELSE NULL
                                END
                            )                        AS "TEN_KHACH_HANG"
                            , (
                                CASE
                                WHEN LOAI_GIA_THANH = 'DON_HANG'
                                    THEN SO."KHACH_HANG_ID"
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN C."KHACH_HANG_ID"
                                ELSE NULL
                                END
                            )                        AS "KHACH_HANG_ID"
                            , C."id"                   AS "HOP_DONG_ID"
                            , C."SO_HOP_DONG"
                            , C."NGAY_KY"
                            , C."TRICH_YEU"

                            , C."NGUOI_LIEN_HE"

                            , (
                                ---				 0=phân xưởng;1=sản phẩm;2=quy trình sản xuất;3=công đoạn
                                CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                    THEN (SELECT "name"
                                            FROM danh_muc_loai_cong_trinh CT
                                            WHERE CT.id = P."LOAI_CONG_TRINH")
                                ELSE NULL
                                END
                            )                        AS "TEN_DANH_MUC"
                            , SUM(JC."DOANH_THU_THUAN"
                            )                        AS "DOANH_THU"
                            , SUM(JC."SO_TIEN"
                            )                        AS "SO_CHUA_NGHIEM_THU"

                        FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JC
                            LEFT JOIN (SELECT
                                        PW.*
                                        , PWC."name"
                                    FROM danh_muc_cong_trinh PW
                                        LEFT JOIN danh_muc_loai_cong_trinh PWC ON PWC."id" = PW."LOAI_CONG_TRINH"
                                    ) P
                                ON P."id" = JC."CONG_TRINH_ID" AND P."isparent" = FALSE
                            LEFT JOIN (SELECT
                                        C1."id"
                                        , C1."SO_HOP_DONG"
                                        , C1."NGAY_KY"
                                        , C1."TRICH_YEU"
                                        , C1."NGUOI_LIEN_HE"
                                        , AC."HO_VA_TEN" AS "TEN_KHACH_HANG"
                                            ,C1."KHACH_HANG_ID"
                                    FROM sale_ex_hop_dong_ban C1
                                        LEFT JOIN res_partner AC ON C1."KHACH_HANG_ID" = AC."id"
                                    ) AS C ON JC."HOP_DONG_ID" = C."id"
                            LEFT JOIN account_ex_don_dat_hang SO ON SO."id" = JC."DON_DAT_HANG_ID"
                        GROUP BY
                            JC."CONG_TRINH_ID",
                            P."MA_CONG_TRINH",
                            P."TEN_CONG_TRINH",
                            P."LOAI_CONG_TRINH",
                            JC."DON_DAT_HANG_ID",
                            SO."SO_DON_HANG",
                            SO."NGAY_DON_HANG",
                            SO."TEN_KHACH_HANG",
                            C."TEN_KHACH_HANG",
                            SO."KHACH_HANG_ID",
                            C."KHACH_HANG_ID",
                            C."id",
                            C."SO_HOP_DONG",
                            C."NGAY_KY",
                            C."TRICH_YEU",
                            C."NGUOI_LIEN_HE",

                            P."LOAI_CONG_TRINH",
                            JC."DOI_TUONG_THCP_ID"
                        ORDER BY
                            P."MA_CONG_TRINH",
                            P."TEN_CONG_TRINH",
                            P."LOAI_CONG_TRINH",
                            SO."SO_DON_HANG",
                            SO."NGAY_DON_HANG",
                            SO."TEN_KHACH_HANG",
                            C."SO_HOP_DONG",
                            C."NGAY_KY",
                            C."TEN_KHACH_HANG",
                            C."TRICH_YEU",
                            C."NGUOI_LIEN_HE",
                            P."LOAI_CONG_TRINH",
                            JC."DOI_TUONG_THCP_ID"
                            ,
                            "SO_CHUA_NGHIEM_THU" ASC
                ;


                END $$
                ;

                SELECT *
                FROM TMP_KET_QUA
                ORDER BY "RowNumber"

                ;

        """  
        return self.execute(query, params)
