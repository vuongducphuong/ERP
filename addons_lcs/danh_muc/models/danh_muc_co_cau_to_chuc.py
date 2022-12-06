# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_TO_CHUC(models.Model):
    _name = 'danh.muc.to.chuc'
    _description = 'Danh mục tổ chức'
    _parent_store = True
    _inherit = ['mail.thread']
    _order = "CAP_TO_CHUC"

    name = fields.Char(string='Tên đơn vị', related='MA_DON_VI', store=True )
    MA_DON_VI = fields.Char(string='Mã đơn vị (*)', help='Mã đơn vị', required=True)
    TEN_DON_VI = fields.Char(string='Tên đơn vị (*)', help='Tên đơn vị', required=True)
    parent_id = fields.Many2one('danh.muc.to.chuc', string='Thuộc đơn vị (*)', help='Thuộc đơn vị')
    CAP_TO_CHUC = fields.Selection([('1', 'Tổng công ty/Công ty'), ('2', 'Chi nhánh'), ('3', 'Văn phòng/Trung tâm'), ('4', 'Phòng ban'), ('5', 'Phân xưởng'), ('6', 'Nhóm/Tổ/Đội') ], string='Cấp tổ chức (*)')
    TK_CHI_PHI_LUONG_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí lương', help='Tk chi phí lương')
    TEN_TK_CHI_PHI_LUONG = fields.Char(string='Tên TK chi phí lương', help='Tên tài khoản chi phí lương')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp')
    DIEN_THOAI = fields.Char(string='Điện thoại')
    FAX = fields.Char(string='Fax')

    HACH_TOAN_DOC_LAP = fields.Boolean(string='Là đơn vị hạch toán độc lập')
    KE_KHAI_THUE_GTGT_TTDB_RIENG = fields.Boolean(string='Kê khai thuế GTGT,TTĐB riêng')

    NGUOI_KY_CHUC_DANH_GIAM_DOC = fields.Char(string='Chức danh',default='Giám đốc')
    NGUOI_KY_TIEU_DE_GIAM_DOC = fields.Char(string='Tiêu đề người ký',default='Giám đốc')
    NGUOI_KY_TEN_GIAM_DOC = fields.Char(string='Tên người ký')

    NGUOI_KY_CHUC_DANH_KE_TOAN_TRUONG = fields.Char(string='Chức danh',default='Kế toán trưởng')
    NGUOI_KY_TIEU_DE_TOAN_TRUONG = fields.Char(string='Tiêu đề người ký',default='Kế toán trưởng')
    NGUOI_KY_TEN_KE_TOAN_TRUONG = fields.Char(string='Tên người ký')

    NGUOI_KY_CHUC_DANH_THU_KHO = fields.Char(string='Chức danh',default='Thủ kho')
    NGUOI_KY_TIEU_DE_KHO = fields.Char(string='Tiêu đề người ký',default='Thủ kho')
    NGUOI_KY_TEN_THU_KHO = fields.Char(string='Tên người ký')

    NGUOI_KY_CHUC_DANH_THU_QUY = fields.Char(string='Chức danh',default='Thủ quỹ')
    
    NGUOI_KY_TEN_THU_QUY = fields.Char(string='Tên người ký')
    NGUOI_KY_TIEU_DE_QUY = fields.Char(string='Tiêu đề người ký',default='Thủ quỹ')

    NGUOI_KY_CHUC_DANH_NGUOI_LAP_BIEU = fields.Char(string='Chức danh',default='Người lập biểu')
    NGUOI_KY_TIEU_DE_LAP_BIEU = fields.Char(string='Tiêu đề người ký',default='Người lập biểu')
    NGUOI_KY_TEN_NGUOI_LAP_BIEU = fields.Char(string='Tên người ký')


    BAC = fields.Integer(string='Bậc', help='Bậc')
    ISPARENT = fields.Boolean(string='Là cha mẹ', help='Là cha mẹ')

    SO_DANG_KY = fields.Char(string='Số đăng ký KD', help='Số đăng ký kinh doanh')
    NGAY_CAP = fields.Date(string='Ngày cấp')
    NOI_CAP = fields.Char(string='Nơi cấp', help='Nơi cấp')

    QUAN_HUYEN = fields.Char(string='Quận/Huyện', help='Quận/Huyện')
    TINH_TP = fields.Char(string='Tỉnh/TP', help='Tỉnh/Thành phố')
    EMAIL = fields.Char(string='Email', help='Email')
    WEBSITE = fields.Char(string='Website', help='Website')
    DV_CHU_QUAN = fields.Char(string='ĐV chủ quản', help='Đơn vị chủ quản')
    MST_DV_CHU_QUAN = fields.Char(string='MST ĐV chủ quản', help='Mã số thuế đơn vị chủ quản')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tài khoản ngân hàng')

    

    IN_TEN_NGUOI_KY = fields.Boolean(string='In tên người ký lên chứng từ, báo cáo')
    LAY_TEN_NGUOI_LAP = fields.Boolean(string='Lấy tên người lập biểu theo tên đăng nhập')
    HACH_TOAN_SELECTION = fields.Selection([('PHU_THUOC', 'Hạch toán phụ thuộc'),('DOC_LAP', 'Hạch toán độc lập'),],  default='PHU_THUOC',string="Hiển thị")
    image = fields.Binary(string="Logo", attachment=True, help="Chọn logo",)

    _sql_constraints = [
	('MA_DON_VI_uniq', 'unique ("MA_DON_VI")', 'Mã đơn vị <<>> đã tồn tại!'),
	]

    @api.onchange('TK_CHI_PHI_LUONG_ID')
    def update_laythongtintkchiphiluong(self):
        self.TEN_TK_CHI_PHI_LUONG = self.TK_CHI_PHI_LUONG_ID.TEN_TAI_KHOAN

    # @api.model
    # def default_get(self,default_fields):
    #     res = super(DANH_MUC_TO_CHUC, self).default_get(default_fields)
    #     # res['NGUOI_KY_TEN_GIAM_DOC'] = self.get_giam_doc()
    #     res['NGUOI_KY_TEN_KE_TOAN_TRUONG'] = self.get_ke_toan_truong()
    #     res['NGUOI_KY_TEN_THU_KHO'] = self.get_thu_kho()
    #     res['NGUOI_KY_TEN_THU_QUY'] = self.get_thu_quy()
    #     res['NGUOI_KY_TEN_NGUOI_LAP_BIEU'] = self.get_nguoi_lap_phieu()
    #     return res

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @return: returns a id of new record
        """
        if values.get('CAP_TO_CHUC') == "1":
            tong_cong_ty = self.lay_tong_cong_ty()
            if tong_cong_ty:
                tong_cong_ty.write(values)
                return tong_cong_ty

        res = super(DANH_MUC_TO_CHUC, self).create(values)
        # Cập nhật CHI_NHANH_ID cho các res_users chưa có chi nhánh
        if values.get('CAP_TO_CHUC') == "1":
            self.env['res.users'].search([('CHI_NHANH_ID', '=', None)]).write({'CHI_NHANH_ID': res.id})
        return res
    
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self.env.uid != 1 and not self.env.user.is_admin:
            domain = []
            for cn in self.env.user.CHI_NHANH_IDS:
                domain += [('MA_PHAN_CAP', '=ilike', cn.MA_PHAN_CAP + '%')]
                if len(domain) > 1:
                    domain = ['|'] + domain
            args = (args or []) + domain
        return super(DANH_MUC_TO_CHUC, self)._search(args, offset, limit, order, count, access_rights_uid)    
    
    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			CREATE OR REPLACE FUNCTION LAY_DANH_SACH_CHI_NHANH(IN chi_nhanh_id INTEGER, bao_gom_chi_nhanh_phu_thuoc INTEGER)
            RETURNS TABLE("CHI_NHANH_ID" INTEGER, "MA_CHI_NHANH" VARCHAR(50), "TEN_CHI_NHANH" VARCHAR(50)) AS $$
            DECLARE

            BEGIN
            RETURN QUERY (
                SELECT DISTINCT
                    OU.id   AS "CHI_NHANH_ID"
                , OU."MA_DON_VI" AS "MA_CHI_NHANH"
                , OU."TEN_DON_VI" AS "TEN_CHI_NHANH"
                FROM danh_muc_to_chuc OU

                WHERE /*1. Lấy đúng CN được truyền ID vào*/
                OU.id = chi_nhanh_id
                /*2. Nếu yêu cầu lấy CN phụ thuộc → lấy thêm các dòng cấp là Chi Nhánh có tích chọn Phụ thuộc và có ParentID = ID truyền vào (để đảm bảo là đang truyền vào TCT)*/
                OR (bao_gom_chi_nhanh_phu_thuoc = 1 AND OU."HACH_TOAN_SELECTION" = 'DOC_LAP' AND "CAP_TO_CHUC" = '2' AND parent_id = chi_nhanh_id)
                /*3. Đơn chi nhánh hoặc truyền BranchID = NULL thì lấy tất cả chi nhánh*/
                OR (chi_nhanh_id IS NULL AND "CAP_TO_CHUC" IN ('1', '2'))
            );
            END;

            $$ LANGUAGE PLpgSQL;
		""")

        self.env.cr.execute(""" 
                    -- DROP FUNCTION IF EXISTS   LAY_DS_DON_VI(IN
        --                                             DON_VI_ID_TS               INTEGER,
        --                                             LAY_CA_CHI_NHANH_PHU_THUOC INTEGER) ;
        CREATE OR REPLACE FUNCTION LAY_DS_DON_VI(IN        --Func_GetDependentByOrganizationUnitID
                                                    DON_VI_ID_TS               INTEGER,
                                                    LAY_CA_CHI_NHANH_PHU_THUOC INTEGER)
            RETURNS TABLE(
                "id"          INTEGER,
                "MA_DON_VI"   VARCHAR(500),
                "TEN_DON_VI"  VARCHAR(500),
                "MA_PHAN_CAP" VARCHAR(500),
                "CAP_TO_CHUC" VARCHAR(500),
                "parent_id"   INTEGER,
                "ISPARENT"    VARCHAR(500),
                "BAC"         VARCHAR(500)
        
            ) AS $$
        DECLARE
        
            CAP_TO_CHUC_TS             VARCHAR(500);
            MA_PHAN_CAP_TS             VARCHAR(500);
        
        BEGIN
        
            DROP TABLE IF EXISTS LAY_DS_DON_VI_TMP_KET_QUA_CUOI_CUNG
            ;
        
            CREATE TEMP TABLE LAY_DS_DON_VI_TMP_KET_QUA_CUOI_CUNG (
                "id"          INTEGER,
                "MA_DON_VI"   VARCHAR(500),
                "TEN_DON_VI"  VARCHAR(500),
                "MA_PHAN_CAP" VARCHAR(500),
                "CAP_TO_CHUC" VARCHAR(500),
                "parent_id"   INTEGER,
                "ISPARENT"    VARCHAR(500),
                "BAC"         VARCHAR(500)
            )
            ;
        
        
            SELECT OU."CAP_TO_CHUC"
            INTO
                CAP_TO_CHUC_TS
            FROM danh_muc_to_chuc OU
            WHERE OU."id" = DON_VI_ID_TS
            ;
        
            SELECT OU."MA_PHAN_CAP"
            INTO
                MA_PHAN_CAP_TS
            FROM danh_muc_to_chuc OU
            WHERE OU."id" = DON_VI_ID_TS
            ;
        
            DROP TABLE IF EXISTS LAY_DS_DON_VI_TMP_KET_QUA
            ;
        
            IF (CAP_TO_CHUC_TS = '1'
                AND LAY_CA_CHI_NHANH_PHU_THUOC = 0
            )
            THEN
                CREATE TEMP TABLE LAY_DS_DON_VI_TMP_KET_QUA
                    AS
                        SELECT DISTINCT
                            OU."id"
                            , OU."MA_DON_VI"
                            , OU."TEN_DON_VI"
                            , OU."MA_PHAN_CAP"
                            , OU."CAP_TO_CHUC"
                            , OU."parent_id"
                            , OU."ISPARENT"
                            , OU."BAC"
        
                        FROM danh_muc_to_chuc AS OU
                            INNER JOIN LATERAL ( SELECT OU."MA_PHAN_CAP"
                                                 FROM danh_muc_to_chuc AS OU_Child
                                                 WHERE (OU_Child."parent_id" = DON_VI_ID_TS
                                                        AND OU_Child."CAP_TO_CHUC" <> '2'
                                                        AND OU."MA_PHAN_CAP" LIKE OU_Child."MA_PHAN_CAP"
                                                                                  || '%%'
                                                       )
                                                       OR ou."id" = DON_VI_ID_TS
                                       ) A ON TRUE
                        ORDER BY ou."MA_PHAN_CAP"
                ;
        
            ELSE
                -- Nếu lấy tổng công ty mà lấy cả chi nhánh phụ thuộc thì lấy tất cả đơn vị của thằng này và chi nhánh phụ thuộc
                IF (CAP_TO_CHUC_TS = '1'
                    AND LAY_CA_CHI_NHANH_PHU_THUOC = 1
                )
                THEN
                    CREATE TEMP TABLE LAY_DS_DON_VI_TMP_KET_QUA
                        AS
        
                            SELECT
                                OU."id"
                                , OU."MA_DON_VI"
                                , OU."TEN_DON_VI"
                                , OU."MA_PHAN_CAP"
                                , OU."CAP_TO_CHUC"
                                , OU."parent_id"
                                , OU."ISPARENT"
                                , OU."BAC"
        
                            FROM danh_muc_to_chuc AS OU
                            WHERE OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                                  AND OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP_TS || '%%'
                            ORDER BY ou."MA_PHAN_CAP"
                    ;
        
                ELSE
                    -- Nếu là chi nhánh thì lấy tất cả phòng ban và chi nhánh
                    CREATE TEMP TABLE LAY_DS_DON_VI_TMP_KET_QUA
                        AS
                            SELECT
                                OU."id"
                                , OU."MA_DON_VI"
                                , OU."TEN_DON_VI"
                                , OU."MA_PHAN_CAP"
                                , OU."CAP_TO_CHUC"
                                , OU."parent_id"
                                , OU."ISPARENT"
                                , OU."BAC"
        
                            FROM danh_muc_to_chuc AS OU
                            WHERE OU."MA_PHAN_CAP" LIKE MA_PHAN_CAP_TS || '%%'
                            ORDER BY ou."MA_PHAN_CAP"
                    ;
        
                END IF
                ;
        
            END IF
            ;
        
        
            INSERT INTO LAY_DS_DON_VI_TMP_KET_QUA_CUOI_CUNG (
                SELECT DISTINCT
                    A."id"
                    , A."MA_DON_VI"
                    , A."TEN_DON_VI"
                    , A."MA_PHAN_CAP"
                    , A."CAP_TO_CHUC"
                    , A."parent_id"
                    , A."ISPARENT"
                    , A."BAC"
                FROM LAY_DS_DON_VI_TMP_KET_QUA A)
            ;
        
            RETURN QUERY SELECT *
                         FROM LAY_DS_DON_VI_TMP_KET_QUA_CUOI_CUNG
            ;
        
        END
        ;
        
        $$ LANGUAGE PLpgSQL
        ;
                    """)


