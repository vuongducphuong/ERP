# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from datetime import timedelta, datetime

class GIA_THANH_KET_CHUYEN_CHI_PHI(models.Model):
    _name = 'gia.thanh.ket.chuyen.chi.phi'
    _description = 'Kết chuyển chi phí'
    _inherit = ['mail.thread']
    KY_TINH_GIA_THANH = fields.Char(string='Kỳ tính giá thành', help='Kỳ tính giá thành',related='KY_TINH_GIA_THANH_ID.TEN',store=True, )
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',default=fields.Datetime.now)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='gia_thanh_ket_chuyen_chi_phi_SO_CHUNG_TU')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    name = fields.Char(string='Name', help='Name', related='SO_CHUNG_TU', oldname='NAME')

    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',compute='tinh_tong_tien', store=True,)

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')

    LOAI_KET_CHUYEN_CHI_PHI = fields.Selection([('GIAN_DON', 'Đơn giản'), ('HE_SO_TY_LE', 'Hệ số tỷ lệ'),], string='Loại kết chuyển chi phí', help='Loại kết chuyển chi phí')

    GIA_THANH_KET_CHUYEN_CHI_PHI_HACH_TOAN_IDS = fields.One2many('gia.thanh.ket.chuyen.chi.phi.hach.toan', 'CHI_TIET_ID', string='Kết chuyển chi phí hạch toán')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null') 

    @api.model
    def default_get(self, fields):
        rec = super(GIA_THANH_KET_CHUYEN_CHI_PHI, self).default_get(fields)
        ky_tinh_gia_thanh_default = self.get_context('default_KY_TINH_GIA_THANH')
        ky_tinh_gia_thanh_id_default = self.get_context('default_KY_TINH_GIA_THANH_ID')
    #    Sản xuất liên tục giản đơn
        #Trường hợp bật form kết chuyển từ nút kết chuyển chi phí
        loai_ket_chuyen_chi_phi = self.get_context('loai_ket_chuyen')
        ten_ky_tinh_gia_thanh = self.get_context('ten')
        loai_chung_tu = self.get_context('loai_chung_tu')
        if loai_chung_tu:
            rec['LOAI_CHUNG_TU'] = int(loai_chung_tu)
        if loai_ket_chuyen_chi_phi:
            rec['LOAI_KET_CHUYEN_CHI_PHI'] = loai_ket_chuyen_chi_phi
        if ten_ky_tinh_gia_thanh:
            rec['KY_TINH_GIA_THANH'] = ten_ky_tinh_gia_thanh
        tu_ngay = self.get_context('tu_ngay')
        den_ngay = self.get_context('den_ngay')
        if tu_ngay and den_ngay :
            rec['DIEN_GIAI'] = 'Kết chuyển chi phí sản xuất kỳ tính giá thành từ ngày ' + datetime.strptime(tu_ngay, '%Y-%m-%d').strftime('%d/%m/%Y') + ' đến ngày ' + datetime.strptime(den_ngay, '%Y-%m-%d').strftime('%d/%m/%Y')
            rec['NGAY_HACH_TOAN'] = den_ngay
            rec['NGAY_CHUNG_TU'] = den_ngay
            
        # Trường hợp chọn từ form tham số
        if ky_tinh_gia_thanh_default:
            rec['KY_TINH_GIA_THANH'] = ky_tinh_gia_thanh_default
        if ky_tinh_gia_thanh_id_default:
            id_ky_tinh_gia_thanh = int(ky_tinh_gia_thanh_id_default)
            rec['KY_TINH_GIA_THANH_ID'] = id_ky_tinh_gia_thanh
            ky_tinh_gia_thanh = self.env['gia.thanh.ky.tinh.gia.thanh'].search([('id', '=', id_ky_tinh_gia_thanh)],limit=1)
            if ky_tinh_gia_thanh:
                rec['DIEN_GIAI'] = 'Kết chuyển chi phí sản xuất kỳ tính giá thành từ ngày ' + datetime.strptime(ky_tinh_gia_thanh.TU_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y') + ' đến ngày ' + datetime.strptime(ky_tinh_gia_thanh.DEN_NGAY, '%Y-%m-%d').strftime('%d/%m/%Y')
                rec['NGAY_HACH_TOAN'] = ky_tinh_gia_thanh.DEN_NGAY
                rec['NGAY_CHUNG_TU'] = ky_tinh_gia_thanh.DEN_NGAY
    #   Sản xuất liên tục - Hệ số tỷ lệ
        id_ky_tinh_gia_thanh_sxlt_hstl =  self.get_context('id_ky_tinh_gia_thanh') # Khai báo biến để lấy id của kỳ tính giá thành khi ấn từ nút kết chuyển chi phí 
        if id_ky_tinh_gia_thanh_sxlt_hstl:
            rec['KY_TINH_GIA_THANH_ID'] = id_ky_tinh_gia_thanh_sxlt_hstl
        return rec

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
        self.write({'state':'da_ghi_so'})


    def ghi_so_cai(self): 
        line_ids = []
        thu_tu = 0
        for line in self.GIA_THANH_KET_CHUYEN_CHI_PHI_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'LOAI_CHUNG_TU': self.LOAI_CHUNG_TU,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DIEN_GIAI' : line.DIEN_GIAI,
                
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : line.SO_TIEN,
                'GHI_NO_NGUYEN_TE' : line.SO_TIEN,
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
                'HOP_DONG_BAN_ID' : line.HOP_DONG_BAN_ID.id,
                'DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
                'DON_DAT_HANG_ID' : line.SO_DON_HANG_ID.id,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : line.SO_TIEN,
                'GHI_CO_NGUYEN_TE' : line.SO_TIEN,
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
    
    @api.onchange('NGAY_HACH_TOAN')
    def update_NGAY_CHUNG_TU(self):
        self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.depends('GIA_THANH_KET_CHUYEN_CHI_PHI_HACH_TOAN_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien = 0.0
            for line in order.GIA_THANH_KET_CHUYEN_CHI_PHI_HACH_TOAN_IDS:
                tong_tien += line.SO_TIEN
            order.update({
                'SO_TIEN': tong_tien,
            })


    def lay_du_lieu_ket_chuyen_cp_he_so_ty_le(self, args):
        new_line_ket_chuyen_chi_phi_chi_tiet = [[5]]
        ky_tinh_gia_thanh_id = args.get('ky_tinh_gia_thanh_id')
        chi_nhanh_id = self.get_chi_nhanh()
        du_lieu_ket_chuyen_chi_phi = self.ket_chuyen_chi_phi_he_so_ty_le(ky_tinh_gia_thanh_id,chi_nhanh_id)
        if du_lieu_ket_chuyen_chi_phi:
            for line in du_lieu_ket_chuyen_chi_phi:
                dien_giai = 'Kết chuyển chi phí ' + str(line.get('TK_CO')) + ' của đối tượng ' + str(line.get('TEN_DOI_TUONG_THCP'))
                new_line_ket_chuyen_chi_phi_chi_tiet += [(0,0,{
							'MA_DOI_TUONG_THCP_ID' : [line.get('DOI_TUONG_THCP_ID'),line.get('MA_DOI_TUONG_THCP')],
							'TEN_DOI_TUONG_THCP' : line.get('TEN_DOI_TUONG_THCP'),
                            'LOAI_DOI_TUONG_THCP' : line.get('LOAI'),
                            
                            'MA_CONG_TRINH_ID' : [line.get('CONG_TRINH_ID'),line.get('MA_CONG_TRINH')],
							'TEN_CONG_TRINH' : line.get('TEN_CONG_TRINH'),
                            'LOAI_CONG_TRINH' : [line.get('LOAI_CONG_TRINH'),line.get('TEN_LOAI_CONG_TRINH')],

                            'SO_DON_HANG_ID' : [line.get('DON_DAT_HANG_ID'),line.get('SO_DON_HANG')],
							'NGAY_DON_HANG' : line.get('NGAY_DON_HANG'),
                            'KHACH_HANG' : [line.get('KHACH_HANG_ID'),line.get('TEN_KHACH_HANG')],

                            'HOP_DONG_BAN_ID' : [line.get('HOP_DONG_ID'),line.get('SO_HOP_DONG')],
							'NGAY_KY' : line.get('NGAY_KY'),
                            'TRICH_YEU' : line.get('TRICH_YEU'),

							'DIEN_GIAI' : dien_giai,
							'TK_NO_ID' : [line.get('TK_NO_ID'),line.get('TK_NO')],
							'TK_CO_ID' : [line.get('TK_CO_ID'),line.get('TK_CO')],
							'SO_TIEN' : line.get('SO_TIEN'),
							# 'MA_THONG_KE_ID' : ,
                            })]
        return {'GIA_THANH_KET_CHUYEN_CHI_PHI_HACH_TOAN_IDS' : new_line_ket_chuyen_chi_phi_chi_tiet}

    
    def ket_chuyen_chi_phi_he_so_ty_le(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
        params = {
            'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
            'CHI_NHANH_ID' : chi_nhanh_id,
            }
        query = """   
            DO LANGUAGE plpgsql $$
            DECLARE
            
                ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
            
            
                chi_nhanh_id         INTEGER := %(CHI_NHANH_ID)s;
            
                CHE_DO_KE_TOAN       VARCHAR;
            
                tu_ngay              TIMESTAMP;
            
                den_ngay             TIMESTAMP;
            
                LOAI_GIA_THANH       VARCHAR;
            
            
                MA_PHAN_CAPMTC       VARCHAR(100);
            
                MA_PHAN_CAPCPSX      VARCHAR(100);
            
                TK_DAU_TIEN_154      VARCHAR(100);
            
            
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
            
            
                -- Lấy chi tiết đầu tiên của TK154
            
                SELECT "SO_TAI_KHOAN"
                INTO TK_DAU_TIEN_154
                FROM danh_muc_he_thong_tai_khoan A
                WHERE "SO_TAI_KHOAN" LIKE '154%%'
                    AND "LA_TK_TONG_HOP" = FALSE
                ORDER BY A."MA_PHAN_CAP" ASC
                LIMIT 1
                ;
            
            
                -- Lấy lại các kỳ tính thỏa mãn điều kiện
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
                    "TK_NO"                         VARCHAR(20),
                    "TK_CO"                         VARCHAR(20),
                    "SO_TIEN"                       DECIMAL(18, 4)
                )
                ;
            
                -- Lấy trong bảng GL các phát sinh trực tiếp
                INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                ("KY_TINH_GIA_THANH_CHI_TIET_ID",
                "KY_TINH_GIA_THANH_ID",
                "DOI_TUONG_THCP_ID",
                "CONG_TRINH_ID",
                "DON_DAT_HANG_ID",
                "HOP_DONG_ID",
                "TK_NO",
                "TK_CO",
                "SO_TIEN"
                )
                    SELECT
                        J."id"
                        , J."KY_TINH_GIA_THANH_ID"
                        , J."MA_DOI_TUONG_THCP_ID"
                        , J."MA_CONG_TRINH_ID"
                        , J."SO_DON_HANG_ID"
                        , J."SO_HOP_DONG_ID"
                        , CASE WHEN AT."KET_CHUYEN_DEN_ID" IS NULL
                        THEN TK_DAU_TIEN_154
                        ELSE (SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = AT."KET_CHUYEN_DEN_ID")
                        END                          AS "TK_NO"
                        , G."MA_TAI_KHOAN"             AS "TK_CO"
                        , SUM(G."GHI_NO" - G."GHI_CO") AS "SO_TIEN"
                    FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet J
                        LEFT JOIN so_cai_chi_tiet G ON (LOAI_GIA_THANH IN ('DON_GIAN',
                                                                        'HE_SO_TY_LE', 'PHAN_BUOC')
                                                        AND G."DOI_TUONG_THCP_ID" = J."MA_DOI_TUONG_THCP_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'CONG_TRINH'
                                                        AND G."CONG_TRINH_ID" = J."MA_CONG_TRINH_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'DON_HANG'
                                                        AND G."DON_DAT_HANG_ID" = J."SO_DON_HANG_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'HOP_DONG'
                                                        AND G."HOP_DONG_BAN_ID" = J."SO_HOP_DONG_ID"
                                                    )
                        LEFT JOIN danh_muc_tai_khoan_ket_chuyen AT ON G."MA_TAI_KHOAN" LIKE (SELECT "SO_TAI_KHOAN"
                                                                                            FROM danh_muc_he_thong_tai_khoan TK
                                                                                            WHERE TK.id = AT."KET_CHUYEN_DEN_ID")
                                                                                            || '%%'
                                                                    AND AT."LOAI_KET_CHUYEN" = 'KET_CHUYEN_CHI_PHI_SAN_XUAT'
                    WHERE J."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                        AND G."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                        AND G."CHI_NHANH_ID" = chi_nhanh_id
            
                        AND ("MA_TAI_KHOAN" LIKE '621%%'
                            OR "MA_TAI_KHOAN" LIKE '622%%'
                            OR (LOAI_GIA_THANH = 'CONG_TRINH'
                                AND "MA_TAI_KHOAN" LIKE '623%%'
                            )
                            OR "MA_TAI_KHOAN" LIKE '627%%'
                        )
                    GROUP BY
                        J."id",
                        J."KY_TINH_GIA_THANH_ID",
                        J."MA_DOI_TUONG_THCP_ID",
                        J."MA_CONG_TRINH_ID",
                        J."SO_DON_HANG_ID",
                        J."SO_HOP_DONG_ID",
                        G."MA_TAI_KHOAN",
                        AT."KET_CHUYEN_DEN_ID"
                ;
            
                -- Lấy trong bảng phân bổ các phát sinh trực tiếp
                INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                ("KY_TINH_GIA_THANH_CHI_TIET_ID",
                "KY_TINH_GIA_THANH_ID",
                "DOI_TUONG_THCP_ID",
                "CONG_TRINH_ID",
                "DON_DAT_HANG_ID",
                "HOP_DONG_ID",
                "TK_NO",
                "TK_CO",
                "SO_TIEN"
                )
                    SELECT
                        JP."id"
                        , JP."KY_TINH_GIA_THANH_ID"
                        , JP."MA_DOI_TUONG_THCP_ID"
                        , JP."MA_CONG_TRINH_ID"
                        , JP."SO_DON_HANG_ID"
                        , JP."SO_HOP_DONG_ID"
                        , CASE WHEN AT."KET_CHUYEN_DEN_ID" IS NULL
                        THEN TK_DAU_TIEN_154
                        ELSE (SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = AT."KET_CHUYEN_DEN_ID")
                        END                                AS "TK_NO"
                        , (SELECT "SO_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan TK
                        WHERE TK.id = JCA."TAI_KHOAN_ID") AS "TK_CO"
                        , SUM(JCA."SO_TIEN")                 AS "SO_TIEN"
                    FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet JP
                        INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCA
                            ON JP."KY_TINH_GIA_THANH_ID" = JCA."KY_TINH_GIA_THANH_ID"
                            AND JP."id" = JCA."KY_TINH_GIA_THANH_CHI_TIET_ID"
                        LEFT JOIN danh_muc_tai_khoan_ket_chuyen AT ON (SELECT "SO_TAI_KHOAN"
                                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                                    WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE (SELECT "SO_TAI_KHOAN"
                                                                                                            FROM
                                                                                                                danh_muc_he_thong_tai_khoan TK
                                                                                                            WHERE TK.id =
                                                                                                                    AT."KET_CHUYEN_DEN_ID")
                                                                                                            || '%%'
                                                                    AND AT."LOAI_KET_CHUYEN" = 'KET_CHUYEN_CHI_PHI_SAN_XUAT'
                    WHERE ((SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%'
                        OR (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%'
                        OR (LOAI_GIA_THANH = 'CONG_TRINH'
                            AND (SELECT "SO_TAI_KHOAN"
                                    FROM danh_muc_he_thong_tai_khoan TK
                                    WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%'
                        )
                        OR (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%'
                        )
            
                        AND JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                    GROUP BY
                        JP."id",
                        JP."KY_TINH_GIA_THANH_ID",
                        JP."MA_DOI_TUONG_THCP_ID",
                        JP."MA_CONG_TRINH_ID",
                        JP."SO_DON_HANG_ID",
                        JP."SO_HOP_DONG_ID",
                        (SELECT "SO_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan TK
                        WHERE TK.id = JCA."TAI_KHOAN_ID"),
            
                        AT."KET_CHUYEN_DEN_ID"
                ;
            
            
                --- Lấy chi tiết các đối tượng THCP trong kỳ tính giá thành
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                            ROW_NUMBER()
                            OVER (
                                ORDER BY J."MA_DOI_TUONG_THCP",
                                    J."LOAI",
                                    JC."TK_NO",
                                    JC."TK_CO" ) AS "RowNumber"
                            , 0                    AS "KY_TINH_GIA_THANH_CHI_TIET_ID"
                            , JC."KY_TINH_GIA_THANH_ID"
                            , JC."DOI_TUONG_THCP_ID"
                            , J."MA_DOI_TUONG_THCP"
                            , J."TEN_DOI_TUONG_THCP"
                            , J."LOAI"
                            , JC."CONG_TRINH_ID"
                            , P."MA_CONG_TRINH"
                            , P."TEN_CONG_TRINH"
                            , P."LOAI_CONG_TRINH"
                            , JC."DON_DAT_HANG_ID"
                            , SO."SO_DON_HANG"
                            , SO."NGAY_DON_HANG"

                            , (CASE WHEN LOAI_GIA_THANH = 'DON_HANG'
                            THEN SO."KHACH_HANG_ID"
                            WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                THEN C."KHACH_HANG_ID"
                            ELSE NULL
                            END)                AS "KHACH_HANG_ID"
                            , (CASE WHEN LOAI_GIA_THANH = 'DON_HANG'
                            THEN SO."TEN_KHACH_HANG"
                            WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                THEN C."TEN_KHACH_HANG"
                            ELSE NULL
                            END)                AS "TEN_KHACH_HANG"
                            , C."id"               AS "HOP_DONG_ID"
                            , C."SO_HOP_DONG"
                            , C."NGAY_KY"
                            , C."TRICH_YEU"
                            , C."NGUOI_LIEN_HE"


                            , CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                            THEN (SELECT "name"
                                FROM danh_muc_loai_cong_trinh CT
                                WHERE CT.id = P."LOAI_CONG_TRINH")
                            WHEN LOAI_GIA_THANH = 'DON_GIAN'
                                THEN N'Sản phẩm'
                            WHEN LOAI_GIA_THANH = 'HE_SO_TY_LE'
                                THEN N'Phân xưởng'
                            WHEN LOAI_GIA_THANH = 'PHAN_BUOC'
                                AND J."LOAI" = '2'
                                THEN N'Quy trình sản xuất'
                            WHEN LOAI_GIA_THANH = 'PHAN_BUOC'
                                AND J."LOAI" = '3'
                                THEN N'Công đoạn'
                            ELSE NULL
                            END
                                                AS "TEN_DANH_MUC"
                            , JC."TK_NO"
                            , JC."TK_CO"
                            , SUM(JC."SO_TIEN")    AS "SO_TIEN"
                        FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JC
                            LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON JC."DOI_TUONG_THCP_ID" = J."id"
                            LEFT JOIN (SELECT
                                        PW.*
                                        , PWC."name"
                                    FROM danh_muc_cong_trinh PW
                                        LEFT JOIN danh_muc_loai_cong_trinh PWC ON PWC."id" = PW."LOAI_CONG_TRINH"
                                    ) P ON P."id" = JC."CONG_TRINH_ID"
                                            AND P."isparent" = FALSE
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
                                    ) C ON JC."HOP_DONG_ID" = C."id"
                            LEFT JOIN account_ex_don_dat_hang SO ON SO."id" = JC."DON_DAT_HANG_ID"
                        GROUP BY
                            JC."KY_TINH_GIA_THANH_ID",
                            JC."DOI_TUONG_THCP_ID",
                            J."MA_DOI_TUONG_THCP",
                            J."TEN_DOI_TUONG_THCP",
                            J."LOAI",
                            JC."CONG_TRINH_ID",
                            P."MA_CONG_TRINH",
                            P."TEN_CONG_TRINH",
                            P."LOAI_CONG_TRINH",
                            JC."DON_DAT_HANG_ID",
                            SO."SO_DON_HANG",
                            SO."NGAY_DON_HANG",
                            SO."TEN_KHACH_HANG",
                            (CASE WHEN LOAI_GIA_THANH = 'DON_HANG'
                            THEN SO."KHACH_HANG_ID"
                            WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                THEN C."KHACH_HANG_ID"
                            ELSE NULL
                            END),
                            C."TEN_KHACH_HANG",
                            C."id",
                            C."SO_HOP_DONG",
                            C."NGAY_KY",
                            C."TRICH_YEU",
                            C."NGUOI_LIEN_HE",


                            JC."TK_NO",
                            JC."TK_CO"

                        HAVING SUM(JC."SO_TIEN"
                            ) <> 0
                        ORDER BY
                            J."MA_DOI_TUONG_THCP",
                            J."LOAI",
                            JC."TK_NO",
                            JC."TK_CO"
                ;
            
            END $$
            ;
            
            
            SELECT KQ.*,tk1.id AS "TK_NO_ID",tk2.id AS "TK_CO_ID",LCT.name AS "TEN_LOAI_CONG_TRINH"
            FROM TMP_KET_QUA KQ
            LEFT JOIN danh_muc_he_thong_tai_khoan tk1 ON KQ."TK_NO" = tk1."SO_TAI_KHOAN"
            LEFT JOIN danh_muc_he_thong_tai_khoan tk2 ON KQ."TK_CO" = tk2."SO_TAI_KHOAN"
            LEFT JOIN danh_muc_loai_cong_trinh LCT ON KQ."LOAI_CONG_TRINH" = LCT.id
            ORDER BY  "RowNumber"

            ;
                
        """  
        return self.execute(query, params)