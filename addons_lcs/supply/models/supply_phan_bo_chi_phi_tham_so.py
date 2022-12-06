# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round

class SUPPLY_PHAN_BO_CHI_PHI_THAM_SO(models.Model):
    _name = 'supply.phan.bo.chi.phi.tham.so'
    _description = ''
    _auto = False

    THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng',required=True)
    NAM = fields.Integer(string='Năm', help='Năm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
        result = super(SUPPLY_PHAN_BO_CHI_PHI_THAM_SO, self).default_get(fields_list)
        thang = datetime.now().month
        result['NAM'] = datetime.now().year
        result['THANG'] = str(thang)
        return result

    def action_view_result(self):
        nam_tai_chinh = int(self.env['ir.config_parameter'].get_param('he_thong.NAM_TAI_CHINH_BAT_DAU'))
        nam_thuc_hien_phan_bo = self.get_context('NAM')
        if nam_thuc_hien_phan_bo < nam_tai_chinh: #Mạnh sửa bug2355 : Thêm đoạn code này để check xem nếu năm thực hiện phân bổ nhỏ hơn năm tài chính thì thông báo lỗi cho người dùng.
            raise ValidationError('Chương trình không cho phép nhập Năm nhỏ hơn năm bắt đầu hạch toán của chương trình. Bạn vui lòng kiểm tra lại.')
        else:
            thang_da_phan_bo = self.env['supply.phan.bo.chi.phi'].search([])
            for pb in thang_da_phan_bo:
                if self.get_context('NAM') == pb.NAM:
                    if self.get_context('THANG') == pb.THANG:
                        raise ValidationError('Bảng phân bổ công cụ dụng cụ tháng ' +str(self.get_context('THANG')) +' năm ' +str(self.get_context('NAM')) + ' đã tồn tại')
        action = self.env.ref('supply.action_open_supply_phan_bo_chi_phi_tham_so_form').read()[0]

        str_dien_giai = 'Phân bổ chi phí CCDC tháng ' + str(self.get_context('THANG')) + ' năm ' + str(self.get_context('NAM'))
        ngay_hach_toan = helper.Datetime.lay_ngay_cuoi_thang(self.get_context('NAM'), self.get_context('THANG'))
        gi_tang = self.lay_du_lieu_muc_cp()
        phan_bos = self.lay_du_lieu_phan_bo()

        dict_phan_bo = {}
        for phan_bo_moi in phan_bos:
            ccdc_id = phan_bo_moi.get('CCDC_ID')
            if ccdc_id not in dict_phan_bo:
                dict_phan_bo[ccdc_id] = []
            dict_phan_bo[ccdc_id] += [phan_bo_moi]
        
        for line in gi_tang:
            ccdc_id = line.get('CCDC_ID')
            if ccdc_id not in dict_phan_bo:
                #load tu bang ghi tang
                dict_phan_bo[ccdc_id] = []
                phan_bo_ghi_tang_ids = self.env['supply.ghi.tang.thiet.lap.phan.bo'].search([('GHI_TANG_THIET_LAP_PHAN_BO_ID', '=', ccdc_id)])
                if phan_bo_ghi_tang_ids:
                    for phan_bo_ghi_tang in phan_bo_ghi_tang_ids:
                        doi_tuong_phan_bo = False
                        ten_doi_tuong_phan_bo = False
                        if phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID:
                            doi_tuong_phan_bo = str(phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID._name) +','+ str(phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID.id)
                            if phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID._name == 'danh.muc.doi.tuong.tap.hop.chi.phi':
                                ten_doi_tuong_phan_bo = phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID.TEN_DOI_TUONG_THCP
                            elif phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID._name == 'danh.muc.cong.trinh':
                                ten_doi_tuong_phan_bo = phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID.TEN_CONG_TRINH
                            elif phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID._name == 'purchase.ex.hop.dong.mua.hang':
                                ten_doi_tuong_phan_bo = phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID.SO_HOP_DONG
                            elif phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID._name == 'sale.ex.hop.dong.ban':
                                ten_doi_tuong_phan_bo = phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID.SO_HOP_DONG
                            elif phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID._name == 'danh.muc.to.chuc':
                                ten_doi_tuong_phan_bo = phan_bo_ghi_tang.DOI_TUONG_PHAN_BO_ID.TEN_DON_VI

                        dict_phan_bo[ccdc_id] += [{
                            'CCDC_ID' : phan_bo_ghi_tang.GHI_TANG_THIET_LAP_PHAN_BO_ID.id,
                            'TEN_CCDC' : phan_bo_ghi_tang.GHI_TANG_THIET_LAP_PHAN_BO_ID.TEN_CCDC,
                            'DOI_TUONG_PHAN_BO_ID' : doi_tuong_phan_bo,
                            'TEN_DOI_TUONG_PBCP' : ten_doi_tuong_phan_bo,
                            'TK_NO_ID' : phan_bo_ghi_tang.TK_NO_ID.id,
                            'TY_LE' : phan_bo_ghi_tang.TY_LE_PB,
                            'LOAI_DOI_TUONG_PBCP' : phan_bo_ghi_tang.LOAI_DOI_TUONG,
                            'TK_CHO_PHAN_BO_ID' : phan_bo_ghi_tang.GHI_TANG_THIET_LAP_PHAN_BO_ID.TK_CHO_PHAN_BO_ID.id,
                            'KHOAN_MUC_CP_ID' : phan_bo_ghi_tang.KHOAN_MUC_CP_ID.id,
                        }]
                        #va add vao dic


        arr_muc_chi_phi = []
        arr_phan_bo = []
        arr_hach_toan = []
        dict_tam = {}

        for line in gi_tang:
            if line.get('SO_TIEN_PB_CCDC_DANG_DUNG') > 0:
                so_tien_phan_bo = line.get('SO_TIEN_PB_CCDC_DANG_DUNG')
                so_ky_pbccdc = 0
                so_ky_pbccdc_ghi_tang = 0
                so_pbccdc = self.env['so.ccdc.chi.tiet'].search([('CCDC_ID', '=', line.get('CCDC_ID')),('MODEL_CHUNG_TU', '=', 'supply.phan.bo.chi.phi')])
                ghi_tang_ccdc = self.env['supply.ghi.tang'].search([('id', '=', line.get('CCDC_ID'))],limit=1)
                if so_pbccdc:
                    so_ky_pbccdc = len(so_pbccdc) + 1
                if ghi_tang_ccdc:
                    so_ky_pbccdc_ghi_tang = ghi_tang_ccdc.SO_KY_PB_CON_LAI
                
                if line.get('SO_TIEN_CON_LAI') < so_tien_phan_bo or so_ky_pbccdc == so_ky_pbccdc_ghi_tang:
                    so_tien_phan_bo = line.get('SO_TIEN_CON_LAI')
                tong_so_tien_phan_bo = so_tien_phan_bo + line.get('GIA_TRI_CON_LAI_CUA_CCDC_GIAM')
                arr_muc_chi_phi += [(0, 0, {
                    'MA_CCDC' : line.get('CCDC_ID'),
                    'TEN_CCDC': line.get('TEN_CCDC'),
                    'LOAI_CCDC_ID': line.get('LOAI_CCDC_ID'),
                    'TONG_SO_TIEN_PHAN_BO': tong_so_tien_phan_bo,
                    'SO_TIEN_PB_CCDC_DAG_DUNG' : so_tien_phan_bo,
                    'GIA_TRI_CON_LAI_CUA_CCDC_GIAM' : line.get('GIA_TRI_CON_LAI_CUA_CCDC_GIAM'),
                    })]
                # for phan_bo in phan_bos:
                ccdc_id = line.get('CCDC_ID')
                if ccdc_id in dict_phan_bo:
                    phan_bo_ids = dict_phan_bo[ccdc_id]
                    if phan_bo_ids:
                        i = 0
                        so_tien_da_phan_bo = 0
                        for phan_bo in phan_bo_ids:
                            
                            if i == len(phan_bo_ids) - 1:
                                so_tien_phan_bo_lan_nay = tong_so_tien_phan_bo - so_tien_da_phan_bo
                            else:
                                so_tien_phan_bo_tab_phan_bo = float_round((tong_so_tien_phan_bo*phan_bo.get('TY_LE'))/100,0)
                                so_tien_da_phan_bo += so_tien_phan_bo_tab_phan_bo
                                so_tien_phan_bo_lan_nay = so_tien_phan_bo_tab_phan_bo
                            i+= 1
                            arr_phan_bo += [(0,0,{
                                'MA_CCDC' : phan_bo.get('CCDC_ID'),
                                'TEN_CCDC' : phan_bo.get('TEN_CCDC'),
                                'CHI_PHI_PHAN_BO': tong_so_tien_phan_bo,
                                'DOI_TUONG_PHAN_BO_ID' : phan_bo.get('DOI_TUONG_PHAN_BO_ID'),
                                'TEN_DOI_TUONG_PHAN_BO' : phan_bo.get('TEN_DOI_TUONG_PBCP'),
                                'TY_LE' : phan_bo.get('TY_LE'),
                                'SO_TIEN' : so_tien_phan_bo_lan_nay,
                                'TK_NO_ID' : phan_bo.get('TK_NO_ID'),
                                'KHOAN_MUC_CP_ID' : phan_bo.get('KHOAN_MUC_CP_ID'),
                            })]
                            khoan_muc_cp = ''
                            doi_tuong_phan_bo = ''
                            doi_tuong_thcp = None
                            cong_trinh = None
                            don_dat_hang = None
                            hop_dong_ban = None
                            don_vi = None
                            if phan_bo.get('DOI_TUONG_PHAN_BO_ID'):
                                cat_phan_bo = phan_bo.get('DOI_TUONG_PHAN_BO_ID').split(",")
                                phan_tu_cuoi = len(cat_phan_bo) - 1
                                doi_tuong = int(cat_phan_bo[phan_tu_cuoi])
                                doi_tuong_phan_bo = str(cat_phan_bo[0]) + ',' + str(cat_phan_bo[phan_tu_cuoi])
                                if cat_phan_bo[0] == 'danh.muc.doi.tuong.tap.hop.chi.phi':
                                    doi_tuong_thcp = doi_tuong
                                elif cat_phan_bo[0] == 'danh.muc.cong.trinh':
                                    cong_trinh = doi_tuong
                                elif cat_phan_bo[0] == 'account.ex.don.dat.hang':
                                    don_dat_hang = doi_tuong
                                elif cat_phan_bo[0] == 'sale.ex.hop.dong.ban':
                                    hop_dong_ban = doi_tuong
                                elif cat_phan_bo[0] == 'danh.muc.to.chuc':
                                    don_vi = doi_tuong

                            if phan_bo.get('KHOAN_MUC_CP_ID') != False and phan_bo.get('KHOAN_MUC_CP_ID') != None:
                                khoan_muc_cp = str(phan_bo.get('KHOAN_MUC_CP_ID'))
                            key = str(phan_bo.get('DOI_TUONG_PHAN_BO_ID')) +','+ str(phan_bo.get('TK_NO_ID')) + ',' + khoan_muc_cp
                            if not key in dict_tam:
                                
                                dict_tam[key] = {
                                        'DIEN_GIAI' : str_dien_giai,
                                        'TK_NO_ID' : phan_bo.get('TK_NO_ID'),
                                        'TK_CO_ID': line.get('TK_CHO_PHAN_BO_ID'),
                                        'SO_TIEN' : 0,
                                        'DOI_TUONG_THCP_ID' : doi_tuong_thcp,
                                        'CONG_TRINH_ID' : cong_trinh,
                                        'DON_DAT_HANG_ID' : don_dat_hang,
                                        'HOP_DONG_BAN_ID' : hop_dong_ban,
                                        'DON_VI_ID' : don_vi,
                                        'KHOAN_MUC_CP_ID' : phan_bo.get('KHOAN_MUC_CP_ID'),
                                    }

                            dict_tam[key]['SO_TIEN'] += so_tien_phan_bo_lan_nay
                
        for ht in dict_tam.values():
            arr_hach_toan += [(0,0,ht)]

                        
        context = {}
        context = {
            'default_NGAY_HACH_TOAN': ngay_hach_toan,
            'default_NGAY_CHUNG_TU': ngay_hach_toan,
            'default_DIEN_GIAI': str_dien_giai,
            'default_THANG': self.get_context('THANG'),
            'default_NAM': self.get_context('NAM'),
            'default_SUPPLY_PHAN_BO_CHI_PHI_MUC_CHI_PHI_IDS' : arr_muc_chi_phi,
            'default_SUPPLY_PHAN_BO_CHI_PHI_PHAN_BO_IDS' : arr_phan_bo,
            'default_SUPPLY_PHAN_BO_CHI_PHI_HACH_TOAN_IDS' : arr_hach_toan,
            }

        action['context'] = helper.Obj.merge(context, action.get('context'))


        # action['options'] = {'clear_breadcrumbs': True}
        return action





    def lay_du_lieu_muc_cp(self):

        thang = self.get_context('THANG')
        nam = self.get_context('NAM')
        ngay_dau_thang = '%s-%s-01' % (nam,thang)
        so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(nam, thang)
        ngay_cuoi_thang = '%s-%s-%s' % (nam,thang,so_ngay_trong_thang)
        params = {
            'TU_NGAY': ngay_dau_thang, 
            'DEN_NGAY': ngay_cuoi_thang, 
            'SO_NGAY_THANG_SD' : so_ngay_trong_thang,
            'CHI_NHANH' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
                v_tu_ngay                                          TIMESTAMP := %(TU_NGAY)s;

                --%%(TU_NGAY)s

                v_den_ngay                                         TIMESTAMP := %(DEN_NGAY)s;

                --%%(DEN_NGAY)s


                v_chi_nhanh_id                                     INT := %(CHI_NHANH)s;

                ref_id                                             INT := 16;


                rec                                                RECORD;

                CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN VARCHAR(50);

                SO_NGAY_CUA_THANG_GHI_TANG                         INT;


            BEGIN


                DROP TABLE IF EXISTS TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG
                ;

                CREATE TABLE TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG
                (
                    "CCDC_ID"         INT,
                    "SO_NGAY_SU_DUNG" DECIMAL(22, 8)/*số ngày sử dụng của ccdc trong tháng đầu tiên*/

                )
                ;

                SELECT value
                INTO CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN'
                FETCH FIRST 1 ROW ONLY
                ;


                /*Nếu tính chi phí tháng đầu tiên theo ngày thì thực hiện lấy ra công cụ dụng cụ*/
                IF CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN = '1'
                THEN
                    INSERT INTO TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG
                        SELECT DISTINCT
                            A."id" AS "GHI_TANG_ID"
                            , DATE_PART('day', CAST(v_den_ngay AS TIMESTAMP) - "NGAY_GHI_TANG") + 1

                        FROM supply_ghi_tang A
                        WHERE
                            A."LOAI_CHUNG_TU" <> 457/*không lấy ghi tăng đầu kỳ*/
                            AND EXTRACT(DAY FROM A."NGAY_GHI_TANG") <> 1/*không lấy ghi tăng từ đầu tháng*/
                            AND EXTRACT(MONTH FROM A."NGAY_GHI_TANG") = EXTRACT(MONTH FROM CAST(v_tu_ngay AS TIMESTAMP)) AND
                            EXTRACT(YEAR FROM A."NGAY_GHI_TANG") = EXTRACT(YEAR FROM CAST(v_tu_ngay AS TIMESTAMP))

                            AND "CHI_NHANH_ID" = v_chi_nhanh_id
                    ;

                    /*Lấy ra số ngày của tháng ghi tăng*/

                    SO_NGAY_CUA_THANG_GHI_TANG =
                    DATE_PART('day', CAST(CAST(EXTRACT(MONTH FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20))
                                        || '/01/'
                                        || CAST(EXTRACT(YEAR FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20)) AS TIMESTAMP) +
                                    INTERVAL '1 month' - CAST(CAST(EXTRACT(MONTH FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20))
                                                            || '/01/'
                                                            ||
                                                            CAST(EXTRACT(YEAR FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20))
                                                            AS TIMESTAMP))
                    ;
                END IF
                ;

                /*end by hoant 14.04.2017 lấy các thông tin phục vụ cr 12645 ccdc*/


                DROP TABLE IF EXISTS TMP_CONG_CU_DUNG_CU
                ;

                CREATE TABLE TMP_CONG_CU_DUNG_CU

                    AS
                        SELECT
                            SL."CCDC_ID"
                            , OU."TEN_DON_VI"
                        FROM so_ccdc_chi_tiet SL
                            INNER JOIN danh_muc_to_chuc OU ON SL."DOI_TUONG_PHAN_BO_ID" = OU."id"
                        GROUP BY "CCDC_ID", SL."DOI_TUONG_PHAN_BO_ID", "TEN_DON_VI"
                        HAVING SUM("SO_LUONG_GHI_TANG" - "SO_LUONG_GHI_GIAM") > 0
                        ORDER BY "TEN_DON_VI"
                ;


                DROP TABLE IF EXISTS TMP_CONG_CU_DUNG_CU_STUFF
                ;

                CREATE TABLE TMP_CONG_CU_DUNG_CU_STUFF

                    AS
                        SELECT DISTINCT
                            "CCDC_ID"
                            , OVERLAY((SELECT string_agg("TEN_DON_VI", ',')
                                    FROM TMP_CONG_CU_DUNG_CU SOU1
                                    WHERE SOU1."CCDC_ID" = SOU2."CCDC_ID"

                                    ) PLACING '' FROM 1 FOR 1) AS "TEN_DOI_TUONG_PHAN_BO"
                        FROM TMP_CONG_CU_DUNG_CU SOU2
                ;


                DROP TABLE IF EXISTS TMP_XAC_DINH_MUC_CP
                ;

                CREATE TABLE TMP_XAC_DINH_MUC_CP

                    AS

                        SELECT
                            --                 NEWID() AS RefDetailID ,
                            -- --                 @"ID_CHUNG_TU" AS "ID_CHUNG_TU" ,

                            -- 	/*Số tiền phân bổ CCDC đang dùng= (Số tiền PB hàng kỳ/SL ghi tăng của CCDC) * Số lượng đang dùng
                            -- 		Trong đó:
                            -- 		Số lượng đang dùng của mã CCDC = Số lượng ghi tăng (của mã ccdc) - Số lượng ghi giảm trên các chứng từ ghi giảm có ngày <= ngày hạch toán của chứng từ phân bổ này (kể cả chứng từ ghi giảm trong tháng này)
                            -- 	*/
                            CASE WHEN COALESCE((SELECT SUM("SO_LUONG_GHI_TANG")
                                                FROM so_ccdc_chi_tiet AS SLD
                                                WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                                        AND SLD."CCDC_ID" = SU."id"

                                                        AND "LOAI_CHUNG_TU" IN ('457', '450', '616')
                                                        AND ((SLD."NGAY_HACH_TOAN" <= v_den_ngay))
                                                ), 0) = 0
                                THEN 0
                            ELSE COALESCE((SELECT SUM("SO_LUONG_GHI_TANG")
                                                    - SUM("SO_LUONG_GHI_GIAM")
                                            FROM so_ccdc_chi_tiet AS SLD
                                            WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                                AND SLD."CCDC_ID" = SU."id"

                                                AND ((SLD."NGAY_HACH_TOAN" <= v_den_ngay)
                                                        OR (EXTRACT(MONTH FROM SLD."NGAY_HACH_TOAN") =
                                                            EXTRACT(MONTH FROM CAST(v_den_ngay AS TIMESTAMP))
                                                            AND EXTRACT(YEAR FROM SLD."NGAY_HACH_TOAN") =
                                                                EXTRACT(YEAR FROM CAST(v_den_ngay AS TIMESTAMP))
                                                        )
                                                )
                                            ), 0)
                                * (
                                    /*  Số tiền PB hàng kỳ:
                                        Nếu CCDC chưa có chứng từ điều chỉnh trước ngày hạch toán của chứng từ này thì Số tiền PB hàng kỳ = Số tiền PB hàng kỳ trên ghi tăng hoặc khai báo CCDC đầu kỳ
                                        Nếu CCDC đã có chứng từ điều chỉnh <= ngày hạch toán của chứng từ này thì số tiền Pb hàng kỳ = Số tiền PB hàng kỳ trên chứng từ điều chỉnh gần nhất với chứng từ phân bổ này
                                    */ (CASE WHEN NOT EXISTS(SELECT *
                                                                    FROM supply_dieu_chinh AS SUA
                                                                        INNER JOIN supply_dieu_chinh_chi_tiet AS SUAD
                                                                            ON SUA."id" = SUAD."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"
                                                                    WHERE SUA."CHI_NHANH_ID" = v_chi_nhanh_id
                                                                        AND SUAD."MA_CCDC" = SU."id"
                                                                        AND "NGAY_CHUNG_TU" <= v_den_ngay
                                                                        AND ((SUA."state" = 'da_ghi_so'

                                                                    )

                                                                        ))
                                    THEN

                                        /*add by hoant 14.04.2017 sửa theo cr 12645 -[CR] Kế toán mong muốn Phân bổ được công cụ dụng cụ và chi phí trả trước chính xác tính từ ngày ghi tăng để phản ánh đúng chi phí phát */
                                        (CASE WHEN A."CCDC_ID" IS NOT NULL AND SO_NGAY_CUA_THANG_GHI_TANG <> 0
                                            THEN
                                                A."SO_NGAY_SU_DUNG" / SO_NGAY_CUA_THANG_GHI_TANG
                                        ELSE 1 END)
                                        /*end by hoant 14.04.2017  sửa theo cr 12645*/
                                        * "SO_TIEN_PHAN_BO_HANG_KY"
                                            ELSE
                                                                            /*add by hoant 14.04.2017 sửa theo cr 12645 -[CR] Kế toán mong muốn Phân bổ được công cụ dụng cụ và chi phí trả trước chính xác tính từ ngày ghi tăng để phản ánh đúng chi phí phát */
                                                                            (CASE WHEN A."CCDC_ID" IS NOT NULL AND
                                                                                        SO_NGAY_CUA_THANG_GHI_TANG <> 0
                                                                                THEN
                                                                                    A."SO_NGAY_SU_DUNG" /
                                                                                    SO_NGAY_CUA_THANG_GHI_TANG
                                                                            ELSE 1 END)
                                                                            /*end by hoant 14.04.2017  sửa theo cr 12645*/
                                                                            * (SELECT SUAD."SO_TIEN_PHAN_BO_HANG_KY"
                                                                                FROM supply_dieu_chinh AS SUA
                                                                                    INNER JOIN
                                                                                    supply_dieu_chinh_chi_tiet AS SUAD
                                                                                        ON SUA."id" =
                                                                                            SUAD."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"
                                                                                WHERE SUA."CHI_NHANH_ID" = v_chi_nhanh_id
                                                                                    AND SUAD."MA_CCDC" = SU."id"
                                                                                    AND "NGAY_CHUNG_TU" <= v_den_ngay
                                                                                    AND ((SUA."state" = 'da_ghi_so'

                                                                                )

                                                                                    )

                                                                                ORDER BY "NGAY_CHUNG_TU" DESC
                                                                                LIMIT 1

                                                                            )

                                            END)

                                            / (
                                                                            --Số lượng ghi tăng
                                                                            COALESCE((SELECT SUM("SO_LUONG_GHI_TANG"
                                                                                                - "SO_LUONG_GHI_GIAM")
                                                                                    FROM so_ccdc_chi_tiet AS SLD
                                                                                    WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                                                                            AND SLD."CCDC_ID" = SU."id"

                                                                                            AND
                                                                                            "LOAI_CHUNG_TU" IN ('457', '450',
                                                                                                                '616')
                                                                                            AND ((SLD."NGAY_HACH_TOAN" <=
                                                                                                v_den_ngay))
                                                                                    ), 0)))
                            END                                  AS "SO_TIEN_PHAN_BO"
                            , /*
                                Giá trị còn lại của CCDC ghi giảm= Giá trị còn lại của CCDC ghi giảm trên các chứng từ ghi giảm phát sinh trong tháng này
                                + giá trị còn lại của CCDC ghi giảm trên các chứng từ ghi giảm phát sinh trong tháng trước nhưng chưa được lấy lên chứng từ phân bổ
                            */
                            COALESCE((SELECT SUM(SUDD."GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM")
                                        FROM supply_ghi_giam_chi_tiet AS SUDD
                                            INNER JOIN supply_ghi_giam AS SUD ON SUDD."CCDC_GHI_GIAM_ID" = SUD."id"
                                        WHERE SUD."CHI_NHANH_ID" = v_chi_nhanh_id
                                            AND SUDD."MA_CCDC_ID" = SU."id"
                                            AND ((SUD."NGAY_CHUNG_TU" <= v_den_ngay
                                                    AND SUDD."PHAN_BO_CHI_PHI_ID" IS NULL
                                                )
                                                OR (EXTRACT(MONTH FROM SUD."NGAY_CHUNG_TU") = EXTRACT(MONTH FROM v_den_ngay)
                                                    AND
                                                    EXTRACT(YEAR FROM SUD."NGAY_CHUNG_TU") = EXTRACT(YEAR FROM v_den_ngay)
                                                )
                                            )
                                            AND ((SUD."state" = 'da_ghi_so'

                                        )

                                            )
                                    ), 0)                       AS "GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM"
                            , /*
                                Trong đó, Giá trị còn lại của CCDC được tính như sau:
                                Đối với CCDC khai báo đầu kỳ: Giá trị còn lại CCDC = Giá trị còn lại của CCDC trên khai báo đầu kỳ + Chênh lệch giá trị còn lại trên các chứng từ điều chỉnh có ngày <= ngày hạch toán của chứng từ này - Tổng số tiền đã phân bổ trên các chứng từ phân bổ có ngày hạch toán <= ngày hạch toán của chứng từ này
                                Đối với CCDC ghi tăng: Giá trị còn lại CCDC = Giá trị CCDC khi ghi tăng (Thành tiền) + Chênh lệch giá trị còn lại trên các chứng từ điều chỉnh có ngày <= ngày hạch toán của chứng từ này - Tổng số tiền đã phân bổ trên các chứng từ phân bổ có ngày hạch toán <= ngày hạch toán của chứng từ này
                            */
                            --                 COALESCE(( SELECT SUM("SO_TIEN_GHI_TANG" - "SO_TIEN_GHI_GIAM"
                            --                                     - "SO_TIEN_PHAN_BO")
                            --                          FROM   so_ccdc_chi_tiet AS SL
                            --                          WHERE  SL."NGAY_HACH_TOAN" <= v_den_ngay
                            --                                 AND SL."CCDC_ID" = SU."id"
                            --                                 AND SL."CHI_NHANH_ID" = v_chi_nhanh_id
                            --
                            --                        ), 0) AS RemainingForCal"SO_TIEN" ,
                            1                                    AS "STT"
                            , SU."id"
                            , SU."MA_CCDC"
                            , SU."TEN_CCDC"
                            , SU."LOAI_CCDC_ID"
                            , SC."TEN"
                            , SU."TK_CHO_PHAN_BO_ID"
                            , "state"
                            , /*số tháng đã phân bổ*/
                            COALESCE((SELECT COUNT(PBCPMCP."MA_CCDC")
                                        FROM supply_phan_bo_chi_phi_muc_chi_phi PBCPMCP
                                            INNER JOIN supply_phan_bo_chi_phi PBCP ON PBCPMCP."PHAN_BO_CHI_PHI_ID" = PBCP."id"
                                        WHERE ((PBCP."state" = 'da_ghi_so'

                                        )

                                            )
                                            AND PBCPMCP."MA_CCDC" = su."id"
                                    ), 0)
                            /* Sửa lỗi JIRA SMEFIVE-2107 by hoant 24.01.2015 lỗi chưa tính các lần phân bổ của đầu kỳ*/
                            + COALESCE(SU."SO_KY_PHAN_BO", 0)
                            - COALESCE(SU."SO_KY_PB_CON_LAI", 0) AS "DEM_SO_KY_PHAN_BO"
                            , su."SO_KY_PHAN_BO"
                            /*Sửa bug by hoant 25.08.2015 NKH: Rà soát: Tính sai giá trị phân bổ khi CCDC có 2 chứng từ điều chỉnh, 1 chứng từ chỉ điều chỉnh giá trị*/
                            + COALESCE((SELECT SUM("CHENH_LENH_KY")
                                        FROM supply_dieu_chinh_chi_tiet
                                            INNER JOIN supply_dieu_chinh
                                                ON supply_dieu_chinh_chi_tiet."CHI_TIET_DIEU_CHINH_CCDC_ID_ID" =
                                                    supply_dieu_chinh."id"
                                        WHERE ((supply_dieu_chinh."state" = 'da_ghi_so'

                                        )

                                                )
                                                AND supply_dieu_chinh_chi_tiet."MA_CCDC" = su."id"
                                        ), 0)                     AS "SO_KY_PHAN_BO"
                            ,coalesce(( SELECT SUM("SO_TIEN_GHI_TANG" - "SO_TIEN_GHI_GIAM"
                                                - "SO_TIEN_PHAN_BO")
                                    FROM   so_ccdc_chi_tiet AS SL
                                    WHERE  SL."NGAY_HACH_TOAN" <= v_den_ngay
                                            AND SL."CCDC_ID" = SU.id
                                            AND SL."CHI_NHANH_ID" = v_chi_nhanh_id
                                ), 0) AS "SO_TIEN_CON_LAI"
                            , SU."SO_CT_GHI_TANG"
                            , SU."NGAY_GHI_TANG"
                            , SOU."TEN_DOI_TUONG_PHAN_BO"
                            , 0                                       "TONG_SO_TIEN_PHAN_BO"

                        FROM supply_ghi_tang AS SU
                            /*add by hoant 14.04.2017 sửa theo cr 12645 -[CR] Kế toán mong muốn Phân bổ được công cụ dụng cụ và chi phí trả trước chính xác tính từ ngày ghi tăng để phản ánh đúng chi phí phát sinh trong tháng*/
                            LEFT JOIN TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG A ON SU."id" = A."CCDC_ID"
                            LEFT JOIN danh_muc_loai_cong_cu_dung_cu AS SC ON SC."id" = SU."LOAI_CCDC_ID"
                            LEFT JOIN TMP_CONG_CU_DUNG_CU_STUFF SOU ON SU."id" = SOU."CCDC_ID"
                        WHERE SU."CHI_NHANH_ID" = v_chi_nhanh_id
                            AND ((SU."state" = 'da_ghi_so'

                        )

                            )
                            /*Số kỳ phân bổ>1 */
                            AND su."SO_KY_PHAN_BO" > 1
                            /*và chưa phân bổ hết cái này làm trên BL vì +-* chia*/
                            AND SU."NGUNG_PHAN_BO" = FALSE --Chỉ lấy các ccdc đang không ngừng phân bổ
                        ORDER BY SU."MA_CCDC"
                ;


                /*Lấy bảng phân bổ thiết lập trên danh mục*/

                -- nmtruong 13/7/2016: Tạo bảng tạm để loại trừ CCDC


                DROP TABLE IF EXISTS TMP_PBCP_CHI_TIET
                ;

                CREATE TABLE TMP_PBCP_CHI_TIET


                (
                    "CCDC_ID"               INT,
                    "TU_DIEU_CHUYEN"        BOOLEAN,
                    "DOI_TUONG_PHAN_BO_ID"  VARCHAR(100),
                    "TY_LE_PHAN_BO"         DECIMAL(18, 9),
                    "TK_GIA_VON"            INT,
                    "TAI_KHOAN_CHO_PHAN_BO" INT,
                    "KHOAN_MUC_CP"          INT
                    ,
                    "STT"                   INT
                    ,
                    "MA_CCDC"               VARCHAR(100)
                )
                ;


                -- Lấy lên phần CCDC có chứng từ điều chuyển về 1 đơn vị sử dụng
                INSERT INTO TMP_PBCP_CHI_TIET
                    SELECT
                        FI."id"
                        , CAST(1 AS BOOLEAN)                              AS "TU_DIEU_CHUYEN"
                        , concat('danh.muc.to.chuc,', LT."DEN_DON_VI_ID") AS "DOI_TUONG_PHAN_BO_ID"
                        , 100                                             AS "TY_LE_PHAN_BO"
                        , LT."TK_NO_ID"
                        , FI."TK_CHO_PHAN_BO_ID"
                        , LT."KHOAN_MUC_CP_ID"
                        , 0                                               AS "STT"
                        , FI."MA_CCDC"
                    FROM supply_ghi_tang AS FI
                        /*ntlieu 09.02.2018 sửa bug 190756: lỗi khi thiết lập phân bổ cho 2 đối tượng phân bổ, có điều chuyển thì số liệu đang bị gấp nhiều dòng*/
                        LEFT JOIN LATERAL
                                (
                                SELECT
                                    SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID"
                                    , SUI."DOI_TUONG_PHAN_BO_ID" AS "ObjectID"
                                    , SUI."TY_LE_PB"
                                    , SUI."LOAI_DOI_TUONG"
                                    , SUI."TK_NO_ID"
                                    , SUI."KHOAN_MUC_CP_ID"
                                FROM supply_ghi_tang_thiet_lap_phan_bo SUI
                                WHERE SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID" = FI."id"
                                FETCH FIRST 1 ROW ONLY

                                ) SIDA ON TRUE
                        -- nmtruong 12/7/2016 CR 109928 Lấy lên điều chuyển cuối cùng trong kỳ phân bổ
                        LEFT JOIN LATERAL
                                ( SELECT
                                        "MA_CCDC_ID"
                                        , "DEN_DON_VI_ID"
                                        , "KHOAN_MUC_CP_ID"
                                        , "TK_NO_ID"
                                    FROM
                                        supply_dieu_chuyen_chi_tiet D
                                        INNER JOIN supply_dieu_chuyen_cong_cu_dung_cu T
                                            ON D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = T."id"

                                    WHERE
                                        ((T."state" = 'da_ghi_so'

                                        )

                                        )
                                        AND D."MA_CCDC_ID" = FI."id"
                                        AND T."NGAY" BETWEEN v_tu_ngay AND v_den_ngay
                                    ORDER BY T."NGAY" DESC, T."STT_NHAP_CT" DESC
                                    FETCH FIRST 1 ROW ONLY
                                ) LT ON TRUE
                        -- Điều chuyển cuối cùng trong kỳ

                        -- nmtruong 12/7/2016 CR 109928 Lấy lên điều chuyển đầu tiên trong kỳ phân bổ
                        LEFT JOIN LATERAL
                                ( SELECT "TU_DON_VI_ID"
                                    FROM
                                        supply_dieu_chuyen_chi_tiet D
                                        INNER JOIN supply_dieu_chuyen_cong_cu_dung_cu T
                                            ON D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = T."id"
                                    WHERE
                                        (("state" = 'da_ghi_so'

                                        )

                                        )
                                        AND D."MA_CCDC_ID" = FI."id"
                                        AND T."NGAY" BETWEEN v_tu_ngay AND v_den_ngay
                                    ORDER BY T."NGAY" ASC, T."STT_NHAP_CT" ASC
                                    FETCH FIRST 1 ROW ONLY
                                ) FT ON TRUE
                        -- Điều chuyển đầu tiên trong kỳ phân bổ

                        -- Lấy lên phân bổ của kỳ trước đó
                        LEFT JOIN LATERAL
                                (
                                SELECT
                                    SUI."MA_CCDC"
                                    , SUI."DOI_TUONG_PHAN_BO_ID" AS "ObjectID"
                                    , SUI."TY_LE"
                                FROM supply_phan_bo_chi_phi_phan_bo SUI
                                    INNER JOIN supply_phan_bo_chi_phi A ON SUI."PHAN_BO_CHI_PHI_ID" = A."id"
                                WHERE SUI."MA_CCDC" = FI."id"
                                        AND
                                        ((A."state" = 'da_ghi_so')

                                        )
                                        AND A."NGAY_CHUNG_TU" < v_tu_ngay
                                ORDER BY A."NGAY_CHUNG_TU" DESC, A."STT_NHAP_CT" DESC
                                FETCH FIRST 1 ROW ONLY
                                ) PrevAl ON TRUE
                        -- Lấy lên số lượng ghi tăng - ghi giảm đến ngày "DEN_NGAY"
                        LEFT JOIN LATERAL
                                (
                                SELECT
                                    SLD."CCDC_ID"
                                    , SUM(SLD."SO_LUONG_GHI_TANG" - SLD."SO_LUONG_GHI_GIAM") AS "SO_LUONG_TON"
                                FROM so_ccdc_chi_tiet AS SLD
                                WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                        AND SLD."CCDC_ID" = FI."id"

                                        AND "LOAI_CHUNG_TU" IN ('452', '450', '457', '616')
                                        AND ((SLD."NGAY_HACH_TOAN" <= v_den_ngay))
                                GROUP BY SLD."CCDC_ID"
                                FETCH FIRST 1 ROW ONLY
                                ) SLD ON TRUE

                        --nmtruong 15/7/2016 Sửa lỗi 110859,110861 Lấy lên số lượng ghi tăng - ghi giảm đến ngày "DEN_NGAY" của chi nhánh điều chuyển cuối cùng
                        LEFT JOIN LATERAL
                                (
                                SELECT
                                    SL."CCDC_ID"
                                    , SL."DOI_TUONG_PHAN_BO_ID"
                                    , SUM(SL."SO_LUONG_GHI_TANG" - SL."SO_LUONG_GHI_GIAM") AS "SL_DON_VI_DIEU_CHUYEN_CUOI_CUNG"

                                FROM so_ccdc_chi_tiet AS SL
                                WHERE SL."CCDC_ID" = LT."MA_CCDC_ID"
                                        AND SL."NGAY_HACH_TOAN" <= v_den_ngay
                                        AND SL."DOI_TUONG_PHAN_BO_ID" = LT."DEN_DON_VI_ID"
                                        AND SL."CHI_NHANH_ID" = v_chi_nhanh_id

                                GROUP BY SL."CCDC_ID", SL."DOI_TUONG_PHAN_BO_ID"
                                FETCH FIRST 1 ROW ONLY

                                ) SLDO ON TRUE


                    WHERE FI."CHI_NHANH_ID" = v_chi_nhanh_id
                        AND ((FI."state" = 'da_ghi_so'

                    )

                        )
                        AND (LT."MA_CCDC_ID" IS NOT NULL
                            -- Chưa có phân bổ ở kỳ trước. Hoặc nếu có phân bổ ở kỳ trước thì phòng ban phân bổ ở kỳ trước phải là phòng ban từ của chứng từ điều chuyển đầu tiên trong kỳ và tỷ lệ phân bổ 100%%
                            AND
                            (
                                (PrevAl."ObjectID" IS NULL AND ((SIDA."ObjectID" LIKE concat('%%,', FT."TU_DON_VI_ID") AND
                                                                    (SIDA."ObjectID" LIKE 'danh.muc.to.chuc,%%')) AND
                                                                SIDA."TY_LE_PB" = 100))
                                OR (PrevAl."ObjectID" IS NOT NULL AND (
                                    (PrevAl."ObjectID" LIKE concat('%%,', FT."TU_DON_VI_ID") AND
                                        (PrevAl."ObjectID" LIKE 'danh.muc.to.chuc,%%'))

                                    AND PrevAl."TY_LE" = 100))
                            )
                            -- so sánh số lượng cuối cùng của ĐV với số lượng còn lại của CCDC (Nếu = nhau thì tại thời điểm phân bổ CCDC đang ở 1 ĐV)
                            AND SLDO."SL_DON_VI_DIEU_CHUYEN_CUOI_CUNG" = SLD."SO_LUONG_TON"
                            AND (LT."TK_NO_ID" IS NOT NULL OR LT."KHOAN_MUC_CP_ID" IS NOT NULL)
                        )
                ;

                -- ---------------------------------------------------------------------------------------------------------------------------------------------------------
                -- 	/* ntlieu 26.01.2018 thi công PBI 179096:  Kế toán muốn khi điều chuyển CCDC mà có chọn lại công trình thì chứng từ phân bổ CCDC sau đó phải tự động lấy được công trình mới chọn này để thuận tiện quản lý chi phí theo công trình
                -- 	Xử lý lấy công trình, ĐT tập hợp chi phí từ chứng từ điều chuyển gần nhất
                -- 		1. Lấy chứng từ điều chuyển CCDC cuối cùng trong kỳ phân bổ CCDC
                -- 		2. Lấy CCDC trên chứng từ điều chuyển cuối cùng mà chỉ chọn 1 Công trình
                -- 		3. Lấy CCDC trên chứng từ điều chuyển cuối cùng mà chỉ chọn 1 Đối tượng THCP
                -- 		4. Lấy chứng từ phân bổ CCDC cuối cùng trước kỳ phân bổ hiện tại
                -- 	-> Lấy số liệu các thông tin từ chứng từ điều chuyển lên đối tượng phân bổ theo điều kiện sau:
                -- 		1. Không tồn tại trong phần đối tượng phân bổ là phòng ban phía trên
                -- 		2. Tồn tại chứng từ điều chuyển
                -- 		3. Nếu chứng từ điều chuyển cuối cùng có điền thông tin công trình và chứng từ phân bổ gần nhất (nếu ko tồn tại chứng từ phân bổ thì kiểm tra tab thiết lập phân bổ trên ghi tăng) mà có đối tượng phân bổ là công trình, và tỷ lệ phân bổ của công trình là 100%%
                -- 		4. Hoặc Nếu chứng từ điều chuyển cuối cùng có điền thông tin Đối tượng THCP và chứng từ phân bổ gần nhất (nếu ko tồn tại chứng từ phân bổ thì kiểm tra tab thiết lập phân bổ trên ghi tăng) mà có đối tượng phân bổ là công trình, và tỷ lệ phân bổ của Đối tượng THCP là 100%%
                -- 	-> Thực hiện lấy số liệu đối tượng phân bổ
                -- 		1. Nếu thoản mãn các điều kiện trên thì lấy đối tượng phân bổ là Công trình, hoặc Đối tượng THCP tương ứng
                -- 	*/
                INSERT INTO TMP_PBCP_CHI_TIET
                    SELECT
                        FI."id"
                        , CAST(1 AS BOOLEAN) AS "TU_DIEU_CHUYEN"
                        , CASE WHEN (PrevAl.ObjectID IS NULL AND SIDA."LOAI_DOI_TUONG" = '1') OR
                                    (PrevAl.ObjectID IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 1)
                        THEN concat('danh.muc.cong.trinh,', LT."CONG_TRINH_ID")
                        WHEN (PrevAl.ObjectID IS NULL AND SIDA."LOAI_DOI_TUONG" = '0') OR
                            (PrevAl.ObjectID IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 0)
                            THEN
                                concat('danh.muc.doi.tuong.tap.hop.chi.phi,', LT."DOI_TUONG_TONG_HOP_CHI_PHI_ID")


                        END                AS "DOI_TUONG_PHAN_BO_ID"
                        , 100                AS "TY_LE_PHAN_BO"
                        ,
                        /*Nếu TK chi phí, và KMCP của điều chuyển để trống thì lấy từ chứng từ phân bổ gần nhất hoặc từ thiết lập phân bổ ghi tăng*/
                        COALESCE(LT."TK_GIA_VON", COALESCE(PrevAl."TK_NO_ID", SIDA."TK_NO_ID"))
                        , FI."TK_CHO_PHAN_BO_ID"
                        , COALESCE(LT."KHOAN_MUC_CP", COALESCE(PrevAl."KHOAN_MUC_CP_ID", SIDA."KHOAN_MUC_CP_ID"))
                        , 0                  AS "STT"
                        , FI."MA_CCDC"
                    FROM supply_ghi_tang AS FI
                        /*ntlieu 09.02.2018 sửa bug 190756: lỗi khi thiết lập phân bổ cho 2 đối tượng phân bổ, có điều chuyển thì số liệu đang bị gấp nhiều dòng*/
                        LEFT JOIN LATERAL
                                (
                                SELECT
                                    SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID"
                                    , SUI."DOI_TUONG_PHAN_BO_ID"
                                    , SUI."TY_LE_PB"
                                    , SUI."LOAI_DOI_TUONG"
                                    , SUI."TK_NO_ID"
                                    , SUI."KHOAN_MUC_CP_ID"
                                FROM supply_ghi_tang_thiet_lap_phan_bo SUI
                                WHERE SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID" = FI."id"
                                FETCH FIRST 1 ROW ONLY

                                ) SIDA ON TRUE
                        LEFT JOIN TMP_PBCP_CHI_TIET TempAD ON FI."id" = TempAD."CCDC_ID"
                        -- Điều chuyển cuối cùng trong kỳ
                        LEFT JOIN LATERAL (SELECT
                                            D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                                            , "MA_CCDC_ID"
                                            , "CONG_TRINH_ID"
                                            , "DOI_TUONG_TONG_HOP_CHI_PHI_ID"
                                            , "KHOAN_MUC_CP"
                                            , "TK_GIA_VON"
                                        FROM supply_dieu_chuyen_chi_tiet D
                                            INNER JOIN supply_dieu_chuyen_cong_cu_dung_cu T
                                                ON D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = T."id"
                                        WHERE (("state" = 'da_ghi_so'

                                        )

                                                )
                                                AND D."MA_CCDC_ID" = FI."id"
                                                AND T."NGAY" BETWEEN v_tu_ngay AND v_den_ngay
                                                AND (D."CONG_TRINH_ID" IS NOT NULL OR
                                                    D."DOI_TUONG_TONG_HOP_CHI_PHI_ID" IS NOT NULL)
                                        ORDER BY T."NGAY" DESC,
                                            T."STT_NHAP_CT" DESC,
                                            D."THU_TU_SAP_XEP"
                                        FETCH FIRST 1 ROW ONLY

                                ) LT ON TRUE
                        /*Số Công trình trên 1 chứng từ điều chuyển là 1*/
                        LEFT JOIN LATERAL (SELECT
                                            D."MA_CCDC_ID"
                                            , COUNT(DISTINCT D."CONG_TRINH_ID") AS "DEM_CONG_TRINH"
                                        FROM supply_dieu_chuyen_chi_tiet D
                                            INNER JOIN danh_muc_cong_trinh AS PW ON PW."id" = D."CONG_TRINH_ID"
                                        WHERE D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = LT."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                                                AND D."MA_CCDC_ID" = FI."id"
                                                AND D."CONG_TRINH_ID" IS NOT NULL
                                                AND PW."active" = TRUE
                                        GROUP BY
                                            "MA_CCDC_ID"
                                        HAVING COUNT(DISTINCT D."CONG_TRINH_ID") = 1
                                        FETCH FIRST 1 ROW ONLY

                                ) LTPW ON TRUE
                        /*Số đối tượng THCP trên 1 chứng từ điều chuyển là 1*/
                        LEFT JOIN LATERAL (SELECT
                                            "MA_CCDC_ID"
                                            , COUNT(DISTINCT D."DOI_TUONG_TONG_HOP_CHI_PHI_ID") AS "DEM_DOI_TUONG_THCP_ID"
                                        FROM supply_dieu_chuyen_chi_tiet D
                                            INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J
                                                ON J."id" = D."DOI_TUONG_TONG_HOP_CHI_PHI_ID"
                                        WHERE D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = LT."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                                                AND D."MA_CCDC_ID" = FI."id"
                                                AND D."DOI_TUONG_TONG_HOP_CHI_PHI_ID" IS NOT NULL
                                                AND J."active" = TRUE
                                        GROUP BY
                                            "MA_CCDC_ID"
                                        HAVING COUNT(DISTINCT D."DOI_TUONG_TONG_HOP_CHI_PHI_ID") = 1
                                        FETCH FIRST 1 ROW ONLY

                                ) LTJ ON TRUE
                        -- Lấy lên phân bổ của kỳ trước đó
                        LEFT JOIN LATERAL (SELECT
                                            SUI."MA_CCDC"
                                            , SUI."DOI_TUONG_PHAN_BO_ID" AS ObjectID
                                            , SUI."TY_LE"
                                            , V."LOAI_DOI_TUONG_PBCP"
                                            , SUI."TK_NO_ID"
                                            , SUI."KHOAN_MUC_CP_ID"

                                        FROM supply_phan_bo_chi_phi_phan_bo SUI
                                            INNER JOIN supply_phan_bo_chi_phi A ON SUI."PHAN_BO_CHI_PHI_ID" = A."id"
                                            LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V
                                                ON SUI."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")


                                        WHERE SUI."MA_CCDC" = FI."id"
                                                AND ((A."state" = 'da_ghi_so'

                                        )

                                                )
                                                AND A."NGAY_CHUNG_TU" < v_tu_ngay
                                        ORDER BY
                                            A."NGAY_CHUNG_TU" DESC,
                                            "STT_NHAP_CT" DESC
                                        FETCH FIRST 1 ROW ONLY

                                ) PrevAl ON TRUE

                    WHERE TempAD."CCDC_ID" IS NULL /*Đã tồn tại trên phần phòng ban thì không kiểm tra tiếp cái này nữa*/
                        AND FI."CHI_NHANH_ID" = v_chi_nhanh_id
                        AND ((FI."state" = 'da_ghi_so'

                    )

                        )
                        -- Tồn tại chứng từ điều chuyển
                        AND (LT."MA_CCDC_ID" IS NOT NULL
                            -- Chưa có phân bổ ở kỳ trước thì so sánh với bảng thiết lập phân bổ trên ghi tăng
                            -- Hoặc nếu có phân bổ ở kỳ trước thì công trình/ĐT tập hợp chi phí phân bổ ở kỳ trước tỷ lệ phân bổ 100%%
                            AND ((PrevAl.ObjectID IS NULL AND ((LTPW."MA_CCDC_ID" IS NOT NULL AND SIDA."LOAI_DOI_TUONG" = '1') OR
                                                                (LTJ."MA_CCDC_ID" IS NOT NULL AND SIDA."LOAI_DOI_TUONG" = '0'))
                                    AND
                                    SIDA."TY_LE_PB" = 100)
                                    OR (PrevAl.ObjectID IS NOT NULL AND
                                        ((LTPW."MA_CCDC_ID" IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 1) OR
                                        (LTJ."MA_CCDC_ID" IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 0)) AND
                                        PrevAl."TY_LE" = 100)
                            )
                        )
                ;


                DROP TABLE IF EXISTS TMP_PB_CHI_TIET_KQ
                ;

                CREATE TABLE TMP_PB_CHI_TIET_KQ
                    AS
                        SELECT
                            D."CCDC_ID"
                            , D."DOI_TUONG_PHAN_BO_ID"
                            , D."TK_GIA_VON"
                            , D."TY_LE_PHAN_BO"
                            , V."MA_DOI_TUONG_PBCP"
                            , V."TEN_DOI_TUONG_PBCP"
                            , V."LOAI_DOI_TUONG_PBCP"
                            , D."TAI_KHOAN_CHO_PHAN_BO"
                            , D."KHOAN_MUC_CP"
                            , "MA_CCDC"
                            , D."STT"
                        FROM TMP_PBCP_CHI_TIET D
                            LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V
                                ON
                                    D."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")

                        WHERE V."LOAI_DOI_TUONG_PBCP" IS NOT NULL/* tránh lỗi TH xóa đối tượng phân bổ*/
                        -- Lấy lên phần CCDC không ở bảng tạm trên
                        UNION ALL
                        SELECT
                            SUA."GHI_TANG_THIET_LAP_PHAN_BO_ID"
                            , SUA."DOI_TUONG_PHAN_BO_ID" AS "DOI_TUONG_PHAN_BO_ID"
                            , SUA."TK_NO_ID"
                            , SUA."TY_LE_PB"
                            , V."MA_DOI_TUONG_PBCP"
                            , V."TEN_DOI_TUONG_PBCP"
                            , V."LOAI_DOI_TUONG_PBCP"
                            , FI."TK_CHO_PHAN_BO_ID"
                            , SUA."KHOAN_MUC_CP_ID"
                            , FI."MA_CCDC"
                            , SUA."THU_TU_SAP_XEP"
                        FROM supply_ghi_tang_thiet_lap_phan_bo AS SUA
                            INNER JOIN supply_ghi_tang AS FI ON SUA."GHI_TANG_THIET_LAP_PHAN_BO_ID" = FI."id"
                            LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V ON

                                                                            SUA."DOI_TUONG_PHAN_BO_ID" LIKE
                                                                            concat('%%,', v."DOI_TUONG_PHAN_BO_ID")

                            LEFT JOIN TMP_PBCP_CHI_TIET D ON FI."id" = D."CCDC_ID"
                        WHERE FI."CHI_NHANH_ID" = v_chi_nhanh_id
                            AND ((FI."state" = 'da_ghi_so'

                        )

                            )
                            AND D."CCDC_ID" IS NULL
                        ORDER BY
                            "MA_CCDC",
                            "STT"
                ;

                DROP TABLE IF EXISTS TMP_HACH_TOAN
                ;

                CREATE TABLE TMP_HACH_TOAN
                    AS
                        -- Lấy lên chứng từ phân bổ kỳ trước
                        SELECT
                            SU1."PHAN_BO_CHI_PHI_ID"
                            , SU1."DOI_TUONG_PHAN_BO_ID"
                            , SU1."TK_NO_ID"
                            , SU1."TY_LE"
                            , V."MA_DOI_TUONG_PBCP"
                            , V."TEN_DOI_TUONG_PBCP"
                            , V."LOAI_DOI_TUONG_PBCP"
                            , SU1."TK_CHO_PHAN_BO_ID"
                            , SU1."KHOAN_MUC_CP_ID"
                        FROM (SELECT
                                SUD."id"
                                , SUD."PHAN_BO_CHI_PHI_ID"
                                , SUD."MA_CCDC"
                                , FI."TK_CHO_PHAN_BO_ID"
                                , SUD."DOI_TUONG_PHAN_BO_ID"
                                , SUD."TK_NO_ID"
                                , SUD."TY_LE"
                                , SUD."SO_TIEN"
                                , SUD."THU_TU_SAP_XEP"
                                , SUD."KHOAN_MUC_CP_ID"
                            FROM supply_phan_bo_chi_phi_phan_bo AS SUD
                                --INNER JOIN SUAllocation AS SU ON SUD."ID_CHUNG_TU" = SU."ID_CHUNG_TU"
                                INNER JOIN supply_ghi_tang AS FI ON SUD."MA_CCDC" = FI."id"
                                LEFT JOIN TMP_PBCP_CHI_TIET D ON (D."TU_DIEU_CHUYEN" = TRUE AND D."CCDC_ID" = SUD."MA_CCDC")
                            WHERE
                                SUD."PHAN_BO_CHI_PHI_ID" IN (
                                    SELECT "id"
                                    FROM supply_phan_bo_chi_phi AS SU1
                                    WHERE SU1."CHI_NHANH_ID" = v_chi_nhanh_id
                                            AND ((SU1."state" = 'da_ghi_so'

                                    )

                                            )
                                    ORDER BY SU1."NGAY_HACH_TOAN" DESC)
                                AND D."CCDC_ID" IS NULL

                            ) AS SU1
                            LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V
                                ON

                                    SU1."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")

                                    AND v.active = TRUE /*không lấy lên các đối tượng đã ngừng theo dõi sửa theo bug 42677*/
                        WHERE V."LOAI_DOI_TUONG_PBCP" IS NOT NULL/* tránh lỗi TH xóa đối tượng phân bổ*/
                        ORDER BY
                            SU1."THU_TU_SAP_XEP"
                ;


            END $$

            ;


            SELECT

                A.id AS "CCDC_ID"
                ,A."TK_CHO_PHAN_BO_ID"
                , round("SO_TIEN_PHAN_BO",0)                   AS "SO_TIEN_PB_CCDC_DANG_DUNG"
                , "GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM" AS "GIA_TRI_CON_LAI_CUA_CCDC_GIAM"
                , "SO_TIEN_CON_LAI"
                , "MA_CCDC"
                , "TEN_CCDC"
                , "LOAI_CCDC_ID"
                , "TEN"                               AS "LOAI_CCDC"
                , B."SO_TAI_KHOAN"
                , "TONG_SO_TIEN_PHAN_BO"


            FROM TMP_XAC_DINH_MUC_CP A
                LEFT JOIN danh_muc_he_thong_tai_khoan B ON A."TK_CHO_PHAN_BO_ID" = B.id
            WHERE "SO_TIEN_CON_LAI" > 0

        """  
        
        
        return self.execute(query, params)



    def lay_du_lieu_phan_bo(self):
        thang = self.get_context('THANG')
        nam = self.get_context('NAM')
        ngay_dau_thang = '%s-%s-01' % (nam,thang)
        so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(nam, thang)
        ngay_cuoi_thang = '%s-%s-%s' % (nam,thang,so_ngay_trong_thang)
        params = {
            'TU_NGAY': ngay_dau_thang, 
            'DEN_NGAY': ngay_cuoi_thang, 
            'SO_NGAY_THANG_SD' : so_ngay_trong_thang,
            'CHI_NHANH' : self.get_chi_nhanh(),
            }


        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
                v_tu_ngay                                          TIMESTAMP := %(TU_NGAY)s;

                --%%(TU_NGAY)s

                v_den_ngay                                         TIMESTAMP := %(DEN_NGAY)s;

                --%%(DEN_NGAY)s


                v_chi_nhanh_id                                     INT := %(CHI_NHANH)s;

                ref_id                                             INT := 16;


                rec                                                RECORD;

                CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN VARCHAR(50);

                SO_NGAY_CUA_THANG_GHI_TANG                         INT;


            BEGIN


            DROP TABLE IF EXISTS TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG
            ;

            CREATE TABLE TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG
            (
                "CCDC_ID"         INT,
                "SO_NGAY_SU_DUNG" DECIMAL(22, 8)/*số ngày sử dụng của ccdc trong tháng đầu tiên*/

            )
            ;

            SELECT value
            INTO CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN
            FROM ir_config_parameter
            WHERE key = 'he_thong.CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN'
            FETCH FIRST 1 ROW ONLY
            ;


            /*Nếu tính chi phí tháng đầu tiên theo ngày thì thực hiện lấy ra công cụ dụng cụ*/
            IF CACH_PHAN_BO_CCDC_CHI_PHI_TRA_TRUOC_THANG_DAU_TIEN = '1'
            THEN
                INSERT INTO TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG
                    SELECT DISTINCT
                        A."id" AS "GHI_TANG_ID"
                        , DATE_PART('day', CAST(v_den_ngay AS TIMESTAMP) - "NGAY_GHI_TANG") + 1

                    FROM supply_ghi_tang A
                    WHERE
                        A."LOAI_CHUNG_TU" <> 457/*không lấy ghi tăng đầu kỳ*/
                        AND EXTRACT(DAY FROM A."NGAY_GHI_TANG") <> 1/*không lấy ghi tăng từ đầu tháng*/
                        AND EXTRACT(MONTH FROM A."NGAY_GHI_TANG") = EXTRACT(MONTH FROM CAST(v_tu_ngay AS TIMESTAMP)) AND
                        EXTRACT(YEAR FROM A."NGAY_GHI_TANG") = EXTRACT(YEAR FROM CAST(v_tu_ngay AS TIMESTAMP))

                        AND "CHI_NHANH_ID" = v_chi_nhanh_id
                ;

                /*Lấy ra số ngày của tháng ghi tăng*/

                SO_NGAY_CUA_THANG_GHI_TANG =
                DATE_PART('day', CAST(CAST(EXTRACT(MONTH FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20))
                                    || '/01/'
                                    || CAST(EXTRACT(YEAR FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20)) AS TIMESTAMP) +
                                INTERVAL '1 month' - CAST(CAST(EXTRACT(MONTH FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20))
                                                        || '/01/'
                                                        ||
                                                        CAST(EXTRACT(YEAR FROM CAST(v_tu_ngay AS TIMESTAMP)) AS VARCHAR(20))
                                                        AS TIMESTAMP))
                ;
            END IF
            ;

            /*end by hoant 14.04.2017 lấy các thông tin phục vụ cr 12645 ccdc*/


            DROP TABLE IF EXISTS TMP_CONG_CU_DUNG_CU
            ;

            CREATE TABLE TMP_CONG_CU_DUNG_CU

                AS
                    SELECT
                        SL."CCDC_ID"
                        , OU."TEN_DON_VI"
                    FROM so_ccdc_chi_tiet SL
                        INNER JOIN danh_muc_to_chuc OU ON SL."DOI_TUONG_PHAN_BO_ID" = OU."id"
                    GROUP BY "CCDC_ID", SL."DOI_TUONG_PHAN_BO_ID", "TEN_DON_VI"
                    HAVING SUM("SO_LUONG_GHI_TANG" - "SO_LUONG_GHI_GIAM") > 0
                    ORDER BY "TEN_DON_VI"
            ;


            DROP TABLE IF EXISTS TMP_CONG_CU_DUNG_CU_STUFF
            ;

            CREATE TABLE TMP_CONG_CU_DUNG_CU_STUFF

                AS
                    SELECT DISTINCT
                        "CCDC_ID"
                        , OVERLAY((SELECT string_agg("TEN_DON_VI", ',')
                                FROM TMP_CONG_CU_DUNG_CU SOU1
                                WHERE SOU1."CCDC_ID" = SOU2."CCDC_ID"

                                ) PLACING '' FROM 1 FOR 1) AS "TEN_DOI_TUONG_PHAN_BO"
                    FROM TMP_CONG_CU_DUNG_CU SOU2
            ;


            DROP TABLE IF EXISTS TMP_XAC_DINH_MUC_CP
            ;

            CREATE TABLE TMP_XAC_DINH_MUC_CP

                AS

                    SELECT

                        CASE WHEN COALESCE((SELECT SUM("SO_LUONG_GHI_TANG")
                                            FROM so_ccdc_chi_tiet AS SLD
                                            WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                                    AND SLD."CCDC_ID" = SU."id"

                                                    AND "LOAI_CHUNG_TU" IN ('457', '450', '616')
                                                    AND ((SLD."NGAY_HACH_TOAN" <= v_den_ngay))
                                            ), 0) = 0
                            THEN 0
                        ELSE COALESCE((SELECT SUM("SO_LUONG_GHI_TANG")
                                                - SUM("SO_LUONG_GHI_GIAM")
                                        FROM so_ccdc_chi_tiet AS SLD
                                        WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                            AND SLD."CCDC_ID" = SU."id"

                                            AND ((SLD."NGAY_HACH_TOAN" <= v_den_ngay)
                                                    OR (EXTRACT(MONTH FROM SLD."NGAY_HACH_TOAN") =
                                                        EXTRACT(MONTH FROM CAST(v_den_ngay AS TIMESTAMP))
                                                        AND EXTRACT(YEAR FROM SLD."NGAY_HACH_TOAN") =
                                                            EXTRACT(YEAR FROM CAST(v_den_ngay AS TIMESTAMP))
                                                    )
                                            )
                                        ), 0)


                            * (
                                /*  Số tiền PB hàng kỳ:
                                    Nếu CCDC chưa có chứng từ điều chỉnh trước ngày hạch toán của chứng từ này thì Số tiền PB hàng kỳ = Số tiền PB hàng kỳ trên ghi tăng hoặc khai báo CCDC đầu kỳ
                                    Nếu CCDC đã có chứng từ điều chỉnh <= ngày hạch toán của chứng từ này thì số tiền Pb hàng kỳ = Số tiền PB hàng kỳ trên chứng từ điều chỉnh gần nhất với chứng từ phân bổ này
                                */ (CASE WHEN NOT EXISTS(SELECT *
                                                                    FROM supply_dieu_chinh AS SUA
                                                                        INNER JOIN supply_dieu_chinh_chi_tiet AS SUAD
                                                                            ON SUA."id" = SUAD."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"
                                                                    WHERE SUA."CHI_NHANH_ID" = v_chi_nhanh_id
                                                                        AND SUAD."MA_CCDC" = SU."id"
                                                                        AND "NGAY_CHUNG_TU" <= v_den_ngay
                                                                        AND ((SUA."state" = 'da_ghi_so'

                                                                    )

                                                                        ))
                                THEN

                                    /*add by hoant 14.04.2017 sửa theo cr 12645 -[CR] Kế toán mong muốn Phân bổ được công cụ dụng cụ và chi phí trả trước chính xác tính từ ngày ghi tăng để phản ánh đúng chi phí phát */
                                    (CASE WHEN A."CCDC_ID" IS NOT NULL AND SO_NGAY_CUA_THANG_GHI_TANG <> 0
                                        THEN
                                            A."SO_NGAY_SU_DUNG" / SO_NGAY_CUA_THANG_GHI_TANG
                                    ELSE 1 END)

                                    * "SO_TIEN_PHAN_BO_HANG_KY"
                                                ELSE
                                                                            /*add by hoant 14.04.2017 sửa theo cr 12645 -[CR] Kế toán mong muốn Phân bổ được công cụ dụng cụ và chi phí trả trước chính xác tính từ ngày ghi tăng để phản ánh đúng chi phí phát */
                                                                            (CASE WHEN A."CCDC_ID" IS NOT NULL AND
                                                                                        SO_NGAY_CUA_THANG_GHI_TANG <> 0
                                                                                THEN
                                                                                    A."SO_NGAY_SU_DUNG" /
                                                                                    SO_NGAY_CUA_THANG_GHI_TANG
                                                                                ELSE 1 END)
                                                                            /*end by hoant 14.04.2017  sửa theo cr 12645*/
                                                                            * (SELECT SUAD."SO_TIEN_PHAN_BO_HANG_KY"
                                                                                FROM supply_dieu_chinh AS SUA
                                                                                    INNER JOIN
                                                                                    supply_dieu_chinh_chi_tiet AS SUAD
                                                                                        ON SUA."id" =
                                                                                            SUAD."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"
                                                                                WHERE SUA."CHI_NHANH_ID" = v_chi_nhanh_id
                                                                                        AND SUAD."MA_CCDC" = SU."id"
                                                                                        AND "NGAY_CHUNG_TU" <= v_den_ngay
                                                                                        AND ((SUA."state" = 'da_ghi_so'

                                                                                )

                                                                                        )

                                                                                ORDER BY "NGAY_CHUNG_TU" DESC
                                                                                LIMIT 1

                                                                            )

                                                END)

                                            / (
                                                                            --Số lượng ghi tăng
                                                                            COALESCE((SELECT SUM("SO_LUONG_GHI_TANG"
                                                                                                - "SO_LUONG_GHI_GIAM")
                                                                                        FROM so_ccdc_chi_tiet AS SLD
                                                                                        WHERE
                                                                                            SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                                                                            AND SLD."CCDC_ID" = SU."id"

                                                                                            AND
                                                                                            "LOAI_CHUNG_TU" IN ('457', '450',
                                                                                                                '616')
                                                                                            AND ((SLD."NGAY_HACH_TOAN" <=
                                                                                                v_den_ngay))
                                                                                    ), 0)))
                        END
                                                            AS "SO_TIEN_PHAN_BO"
                        /*
                    Giá trị còn lại của CCDC ghi giảm= Giá trị còn lại của CCDC ghi giảm trên các chứng từ ghi giảm phát sinh trong tháng này
                    + giá trị còn lại của CCDC ghi giảm trên các chứng từ ghi giảm phát sinh trong tháng trước nhưng chưa được lấy lên chứng từ phân bổ
                */


                        , COALESCE((SELECT SUM(SUDD."GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM")
                                    FROM supply_ghi_giam_chi_tiet AS SUDD
                                        INNER JOIN supply_ghi_giam AS SUD ON SUDD."CCDC_GHI_GIAM_ID" = SUD."id"
                                    WHERE SUD."CHI_NHANH_ID" = v_chi_nhanh_id
                                        AND SUDD."MA_CCDC_ID" = SU."id"
                                        AND ((SUD."NGAY_CHUNG_TU" <= v_den_ngay
                                                AND SUDD."PHAN_BO_CHI_PHI_ID" IS NULL
                                            )
                                            OR (EXTRACT(MONTH FROM SUD."NGAY_CHUNG_TU") =
                                                EXTRACT(MONTH FROM CAST(v_den_ngay AS TIMESTAMP))
                                                AND
                                                EXTRACT(YEAR FROM SUD."NGAY_CHUNG_TU") =
                                                EXTRACT(YEAR FROM CAST(v_den_ngay AS TIMESTAMP))
                                            )
                                        )
                                        AND ((SUD."state" = 'da_ghi_so'

                                    )

                                        )
                                ), 0)                       AS "GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM"
                        , 1                                    AS "STT"
                        , SU."id"
                        , SU."MA_CCDC"
                        , SU."TEN_CCDC"
                        , SU."LOAI_CCDC_ID"
                        , SC."TEN"
                        , SU."TK_CHO_PHAN_BO_ID"
                        , "state"
                        , /*số tháng đã phân bổ*/
                        COALESCE((SELECT COUNT(PBCPMCP."MA_CCDC")
                                    FROM supply_phan_bo_chi_phi_muc_chi_phi PBCPMCP
                                        INNER JOIN supply_phan_bo_chi_phi PBCP ON PBCPMCP."PHAN_BO_CHI_PHI_ID" = PBCP."id"
                                    WHERE ((PBCP."state" = 'da_ghi_so'

                                    )

                                        )
                                        AND PBCPMCP."MA_CCDC" = su."id"
                                ), 0)
                        /* Sửa lỗi JIRA SMEFIVE-2107 by hoant 24.01.2015 lỗi chưa tính các lần phân bổ của đầu kỳ*/
                        + COALESCE(SU."SO_KY_PHAN_BO", 0)
                        - COALESCE(SU."SO_KY_PB_CON_LAI", 0) AS "DEM_SO_KY_PHAN_BO"
                        , su."SO_KY_PHAN_BO"
                        /*Sửa bug by hoant 25.08.2015 NKH: Rà soát: Tính sai giá trị phân bổ khi CCDC có 2 chứng từ điều chỉnh, 1 chứng từ chỉ điều chỉnh giá trị*/
                        + COALESCE((SELECT SUM("CHENH_LENH_KY")
                                    FROM supply_dieu_chinh_chi_tiet
                                        INNER JOIN supply_dieu_chinh
                                            ON supply_dieu_chinh_chi_tiet."CHI_TIET_DIEU_CHINH_CCDC_ID_ID" =
                                                supply_dieu_chinh."id"
                                    WHERE ((supply_dieu_chinh."state" = 'da_ghi_so'

                                    )

                                            )
                                            AND supply_dieu_chinh_chi_tiet."MA_CCDC" = su."id"
                                    ), 0)                     AS "SO_KY_PHAN_BO"
                        , SU."SO_CT_GHI_TANG"
                        , SU."NGAY_GHI_TANG"
                        , SOU."TEN_DOI_TUONG_PHAN_BO"
                        , 0                                       "TONG_SO_TIEN_PHAN_BO"

                    FROM supply_ghi_tang AS SU
                        /*add by hoant 14.04.2017 sửa theo cr 12645 -[CR] Kế toán mong muốn Phân bổ được công cụ dụng cụ và chi phí trả trước chính xác tính từ ngày ghi tăng để phản ánh đúng chi phí phát sinh trong tháng*/
                        LEFT JOIN TMP_DS_CCDC_TINH_PHAN_BO_LAN_DAU_TIEN_THEO_KHOANG_TG A ON SU."id" = A."CCDC_ID"
                        LEFT JOIN danh_muc_loai_cong_cu_dung_cu AS SC ON SC."id" = SU."LOAI_CCDC_ID"
                        LEFT JOIN TMP_CONG_CU_DUNG_CU_STUFF SOU ON SU."id" = SOU."CCDC_ID"
                    WHERE SU."CHI_NHANH_ID" = v_chi_nhanh_id
                        AND ((SU."state" = 'da_ghi_so'

                    )

                        )
                        /*Số kỳ phân bổ>1 */
                        AND su."SO_KY_PHAN_BO" > 1
                        /*và chưa phân bổ hết cái này làm trên BL vì +-* chia*/
                        AND SU."NGUNG_PHAN_BO" = FALSE --Chỉ lấy các ccdc đang không ngừng phân bổ
                    ORDER BY SU."MA_CCDC"
            ;


            /*Lấy bảng phân bổ thiết lập trên danh mục*/




            DROP TABLE IF EXISTS TMP_PBCP_CHI_TIET
            ;

            CREATE TABLE TMP_PBCP_CHI_TIET


            (
                "CCDC_ID"               INT,

                "TU_DIEU_CHUYEN"        BOOLEAN,
                "DOI_TUONG_PHAN_BO_ID"  VARCHAR(100),

                "TY_LE_PHAN_BO"         DECIMAL(18, 9),
                "TK_GIA_VON"            INT,
                "TAI_KHOAN_CHO_PHAN_BO" INT,
                "KHOAN_MUC_CP"          INT
                ,
                "STT"                   INT
                ,
                "MA_CCDC"               VARCHAR(100)
            )
            ;


            -- Lấy lên phần CCDC có chứng từ điều chuyển về 1 đơn vị sử dụng
            INSERT INTO TMP_PBCP_CHI_TIET
                SELECT
                    FI."id"
                    , CAST(1 AS BOOLEAN)                              AS "TU_DIEU_CHUYEN"
                    , concat('danh.muc.to.chuc,', LT."DEN_DON_VI_ID") AS "DOI_TUONG_PHAN_BO_ID"

                    , 100                                             AS "TY_LE_PHAN_BO"
                    , LT."TK_NO_ID"
                    , FI."TK_CHO_PHAN_BO_ID"
                    , LT."KHOAN_MUC_CP_ID"
                    , 0                                               AS "STT"
                    , FI."MA_CCDC"
                FROM supply_ghi_tang AS FI
                    /*ntlieu 09.02.2018 sửa bug 190756: lỗi khi thiết lập phân bổ cho 2 đối tượng phân bổ, có điều chuyển thì số liệu đang bị gấp nhiều dòng*/
                    LEFT JOIN LATERAL
                            (
                            SELECT
                                SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID"
                                , SUI."DOI_TUONG_PHAN_BO_ID" AS "ObjectID"
                                , SUI."TY_LE_PB"
                                , SUI."LOAI_DOI_TUONG"
                                , SUI."TK_NO_ID"
                                , SUI."KHOAN_MUC_CP_ID"
                            FROM supply_ghi_tang_thiet_lap_phan_bo SUI
                            WHERE SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID" = FI."id"
                            FETCH FIRST 1 ROW ONLY

                            ) SIDA ON TRUE
                    -- nmtruong 12/7/2016 CR 109928 Lấy lên điều chuyển cuối cùng trong kỳ phân bổ
                    LEFT JOIN LATERAL
                            ( SELECT
                                    "MA_CCDC_ID"
                                    , "DEN_DON_VI_ID"
                                    , "KHOAN_MUC_CP_ID"
                                    , "TK_NO_ID"
                                FROM
                                    supply_dieu_chuyen_chi_tiet D
                                    INNER JOIN supply_dieu_chuyen_cong_cu_dung_cu T
                                        ON D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = T."id"

                                WHERE
                                    ((T."state" = 'da_ghi_so'

                                    )

                                    )
                                    AND D."MA_CCDC_ID" = FI."id"
                                    AND T."NGAY" BETWEEN v_tu_ngay AND v_den_ngay
                                ORDER BY T."NGAY" DESC, T."STT_NHAP_CT" DESC
                                FETCH FIRST 1 ROW ONLY
                            ) LT ON TRUE
                    -- Điều chuyển cuối cùng trong kỳ

                    -- nmtruong 12/7/2016 CR 109928 Lấy lên điều chuyển đầu tiên trong kỳ phân bổ
                    LEFT JOIN LATERAL
                            ( SELECT "TU_DON_VI_ID"
                                FROM
                                    supply_dieu_chuyen_chi_tiet D
                                    INNER JOIN supply_dieu_chuyen_cong_cu_dung_cu T
                                        ON D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = T."id"
                                WHERE
                                    (("state" = 'da_ghi_so'

                                    )

                                    )
                                    AND D."MA_CCDC_ID" = FI."id"
                                    AND T."NGAY" BETWEEN v_tu_ngay AND v_den_ngay
                                ORDER BY T."NGAY" ASC, T."STT_NHAP_CT" ASC
                                FETCH FIRST 1 ROW ONLY
                            ) FT ON TRUE
                    -- Điều chuyển đầu tiên trong kỳ phân bổ

                    -- Lấy lên phân bổ của kỳ trước đó
                    LEFT JOIN LATERAL
                            (
                            SELECT
                                SUI."MA_CCDC"
                                , SUI."DOI_TUONG_PHAN_BO_ID" AS "ObjectID"
                                , SUI."TY_LE"
                            FROM supply_phan_bo_chi_phi_phan_bo SUI
                                INNER JOIN supply_phan_bo_chi_phi A ON SUI."PHAN_BO_CHI_PHI_ID" = A."id"
                            WHERE SUI."MA_CCDC" = FI."id"
                                    AND
                                    ((A."state" = 'da_ghi_so')

                                    )
                                    AND A."NGAY_CHUNG_TU" < v_tu_ngay
                            ORDER BY A."NGAY_CHUNG_TU" DESC, A."STT_NHAP_CT" DESC
                            FETCH FIRST 1 ROW ONLY
                            ) PrevAl ON TRUE
                    -- Lấy lên số lượng ghi tăng - ghi giảm đến ngày "DEN_NGAY"
                    LEFT JOIN LATERAL
                            (
                            SELECT
                                SLD."CCDC_ID"
                                , SUM(SLD."SO_LUONG_GHI_TANG" - SLD."SO_LUONG_GHI_GIAM") AS "SO_LUONG_TON"
                            FROM so_ccdc_chi_tiet AS SLD
                            WHERE SLD."CHI_NHANH_ID" = v_chi_nhanh_id
                                    AND SLD."CCDC_ID" = FI."id"

                                    AND "LOAI_CHUNG_TU" IN ('452', '450', '457', '616')
                                    AND ((SLD."NGAY_HACH_TOAN" <= v_den_ngay))
                            GROUP BY SLD."CCDC_ID"
                            FETCH FIRST 1 ROW ONLY
                            ) SLD ON TRUE

                    --nmtruong 15/7/2016 Sửa lỗi 110859,110861 Lấy lên số lượng ghi tăng - ghi giảm đến ngày "DEN_NGAY" của chi nhánh điều chuyển cuối cùng
                    LEFT JOIN LATERAL
                            (
                            SELECT
                                SL."CCDC_ID"
                                , SL."DOI_TUONG_PHAN_BO_ID"
                                , SUM(SL."SO_LUONG_GHI_TANG" - SL."SO_LUONG_GHI_GIAM") AS "SL_DON_VI_DIEU_CHUYEN_CUOI_CUNG"

                            FROM so_ccdc_chi_tiet AS SL
                            WHERE SL."CCDC_ID" = LT."MA_CCDC_ID"
                                    AND SL."NGAY_HACH_TOAN" <= v_den_ngay
                                    AND SL."DOI_TUONG_PHAN_BO_ID" = LT."DEN_DON_VI_ID"
                                    AND SL."CHI_NHANH_ID" = v_chi_nhanh_id

                            GROUP BY SL."CCDC_ID", SL."DOI_TUONG_PHAN_BO_ID"
                            FETCH FIRST 1 ROW ONLY

                            ) SLDO ON TRUE


                WHERE FI."CHI_NHANH_ID" = v_chi_nhanh_id
                    AND ((FI."state" = 'da_ghi_so'

                )

                    )
                    AND (LT."MA_CCDC_ID" IS NOT NULL
                        -- Chưa có phân bổ ở kỳ trước. Hoặc nếu có phân bổ ở kỳ trước thì phòng ban phân bổ ở kỳ trước phải là phòng ban từ của chứng từ điều chuyển đầu tiên trong kỳ và tỷ lệ phân bổ 100%%
                        AND
                        (
                            (PrevAl."ObjectID" IS NULL AND ((SIDA."ObjectID" LIKE concat('%%,', FT."TU_DON_VI_ID") AND
                                                                (SIDA."ObjectID" LIKE 'danh.muc.to.chuc,%%')) AND
                                                            SIDA."TY_LE_PB" = 100))
                            OR (PrevAl."ObjectID" IS NOT NULL AND (
                                (PrevAl."ObjectID" LIKE concat('%%,', FT."TU_DON_VI_ID") AND
                                    (PrevAl."ObjectID" LIKE 'danh.muc.to.chuc,%%'))

                                AND PrevAl."TY_LE" = 100))
                        )
                        -- so sánh số lượng cuối cùng của ĐV với số lượng còn lại của CCDC (Nếu = nhau thì tại thời điểm phân bổ CCDC đang ở 1 ĐV)
                        AND SLDO."SL_DON_VI_DIEU_CHUYEN_CUOI_CUNG" = SLD."SO_LUONG_TON"
                        AND (LT."TK_NO_ID" IS NOT NULL OR LT."KHOAN_MUC_CP_ID" IS NOT NULL)
                    )
            ;

            -- ---------------------------------------------------------------------------------------------------------------------------------------------------------
            -- 	/* ntlieu 26.01.2018 thi công PBI 179096:  Kế toán muốn khi điều chuyển CCDC mà có chọn lại công trình thì chứng từ phân bổ CCDC sau đó phải tự động lấy được công trình mới chọn này để thuận tiện quản lý chi phí theo công trình
            -- 	Xử lý lấy công trình, ĐT tập hợp chi phí từ chứng từ điều chuyển gần nhất
            -- 		1. Lấy chứng từ điều chuyển CCDC cuối cùng trong kỳ phân bổ CCDC
            -- 		2. Lấy CCDC trên chứng từ điều chuyển cuối cùng mà chỉ chọn 1 Công trình
            -- 		3. Lấy CCDC trên chứng từ điều chuyển cuối cùng mà chỉ chọn 1 Đối tượng THCP
            -- 		4. Lấy chứng từ phân bổ CCDC cuối cùng trước kỳ phân bổ hiện tại
            -- 	-> Lấy số liệu các thông tin từ chứng từ điều chuyển lên đối tượng phân bổ theo điều kiện sau:
            -- 		1. Không tồn tại trong phần đối tượng phân bổ là phòng ban phía trên
            -- 		2. Tồn tại chứng từ điều chuyển
            -- 		3. Nếu chứng từ điều chuyển cuối cùng có điền thông tin công trình và chứng từ phân bổ gần nhất (nếu ko tồn tại chứng từ phân bổ thì kiểm tra tab thiết lập phân bổ trên ghi tăng) mà có đối tượng phân bổ là công trình, và tỷ lệ phân bổ của công trình là 100%%
            -- 		4. Hoặc Nếu chứng từ điều chuyển cuối cùng có điền thông tin Đối tượng THCP và chứng từ phân bổ gần nhất (nếu ko tồn tại chứng từ phân bổ thì kiểm tra tab thiết lập phân bổ trên ghi tăng) mà có đối tượng phân bổ là công trình, và tỷ lệ phân bổ của Đối tượng THCP là 100%%
            -- 	-> Thực hiện lấy số liệu đối tượng phân bổ
            -- 		1. Nếu thoản mãn các điều kiện trên thì lấy đối tượng phân bổ là Công trình, hoặc Đối tượng THCP tương ứng
            -- 	*/
            INSERT INTO TMP_PBCP_CHI_TIET
                SELECT
                    FI."id"
                    , CAST(1 AS BOOLEAN) AS "TU_DIEU_CHUYEN"
                    , CASE WHEN (PrevAl.ObjectID IS NULL AND SIDA."LOAI_DOI_TUONG" = '1') OR
                                (PrevAl.ObjectID IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 1)
                    THEN concat('danh.muc.cong.trinh,', LT."CONG_TRINH_ID")
                    WHEN (PrevAl.ObjectID IS NULL AND SIDA."LOAI_DOI_TUONG" = '0') OR
                        (PrevAl.ObjectID IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 0)
                        THEN
                            concat('danh.muc.doi.tuong.tap.hop.chi.phi,', LT."DOI_TUONG_TONG_HOP_CHI_PHI_ID")


                    END                AS "DOI_TUONG_PHAN_BO_ID"
                    , 100                AS "TY_LE_PHAN_BO"
                    ,
                    /*Nếu TK chi phí, và KMCP của điều chuyển để trống thì lấy từ chứng từ phân bổ gần nhất hoặc từ thiết lập phân bổ ghi tăng*/
                    COALESCE(LT."TK_GIA_VON", COALESCE(PrevAl."TK_NO_ID", SIDA."TK_NO_ID"))
                    , FI."TK_CHO_PHAN_BO_ID"
                    , COALESCE(LT."KHOAN_MUC_CP", COALESCE(PrevAl."KHOAN_MUC_CP_ID", SIDA."KHOAN_MUC_CP_ID"))
                    , 0                  AS "STT"
                    , FI."MA_CCDC"
                FROM supply_ghi_tang AS FI
                    /*ntlieu 09.02.2018 sửa bug 190756: lỗi khi thiết lập phân bổ cho 2 đối tượng phân bổ, có điều chuyển thì số liệu đang bị gấp nhiều dòng*/
                    LEFT JOIN LATERAL
                            (
                            SELECT
                                SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID"
                                , SUI."DOI_TUONG_PHAN_BO_ID"
                                , SUI."TY_LE_PB"
                                , SUI."LOAI_DOI_TUONG"
                                , SUI."TK_NO_ID"
                                , SUI."KHOAN_MUC_CP_ID"
                            FROM supply_ghi_tang_thiet_lap_phan_bo SUI
                            WHERE SUI."GHI_TANG_THIET_LAP_PHAN_BO_ID" = FI."id"
                            FETCH FIRST 1 ROW ONLY

                            ) SIDA ON TRUE
                    LEFT JOIN TMP_PBCP_CHI_TIET TempAD ON FI."id" = TempAD."CCDC_ID"
                    -- Điều chuyển cuối cùng trong kỳ
                    LEFT JOIN LATERAL (SELECT
                                        D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                                        , "MA_CCDC_ID"
                                        , "CONG_TRINH_ID"
                                        , "DOI_TUONG_TONG_HOP_CHI_PHI_ID"
                                        , "KHOAN_MUC_CP"
                                        , "TK_GIA_VON"
                                    FROM supply_dieu_chuyen_chi_tiet D
                                        INNER JOIN supply_dieu_chuyen_cong_cu_dung_cu T
                                            ON D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = T."id"
                                    WHERE (("state" = 'da_ghi_so'

                                    )

                                            )
                                            AND D."MA_CCDC_ID" = FI."id"
                                            AND T."NGAY" BETWEEN v_tu_ngay AND v_den_ngay
                                            AND (D."CONG_TRINH_ID" IS NOT NULL OR
                                                D."DOI_TUONG_TONG_HOP_CHI_PHI_ID" IS NOT NULL)
                                    ORDER BY T."NGAY" DESC,
                                        T."STT_NHAP_CT" DESC,
                                        D."sequence",
                                        D.id
                                    FETCH FIRST 1 ROW ONLY

                            ) LT ON TRUE
                    /*Số Công trình trên 1 chứng từ điều chuyển là 1*/
                    LEFT JOIN LATERAL (SELECT
                                        D."MA_CCDC_ID"
                                        , COUNT(DISTINCT D."CONG_TRINH_ID") AS "DEM_CONG_TRINH"
                                    FROM supply_dieu_chuyen_chi_tiet D
                                        INNER JOIN danh_muc_cong_trinh AS PW ON PW."id" = D."CONG_TRINH_ID"
                                    WHERE D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = LT."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                                            AND D."MA_CCDC_ID" = FI."id"
                                            AND D."CONG_TRINH_ID" IS NOT NULL
                                            AND PW."active" = TRUE
                                    GROUP BY
                                        "MA_CCDC_ID"
                                    HAVING COUNT(DISTINCT D."CONG_TRINH_ID") = 1
                                    FETCH FIRST 1 ROW ONLY

                            ) LTPW ON TRUE
                    /*Số đối tượng THCP trên 1 chứng từ điều chuyển là 1*/
                    LEFT JOIN LATERAL (SELECT
                                        "MA_CCDC_ID"
                                        , COUNT(DISTINCT D."DOI_TUONG_TONG_HOP_CHI_PHI_ID") AS "DEM_DOI_TUONG_THCP_ID"
                                    FROM supply_dieu_chuyen_chi_tiet D
                                        INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J
                                            ON J."id" = D."DOI_TUONG_TONG_HOP_CHI_PHI_ID"
                                    WHERE D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID" = LT."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                                            AND D."MA_CCDC_ID" = FI."id"
                                            AND D."DOI_TUONG_TONG_HOP_CHI_PHI_ID" IS NOT NULL
                                            AND J."active" = TRUE
                                    GROUP BY
                                        "MA_CCDC_ID"
                                    HAVING COUNT(DISTINCT D."DOI_TUONG_TONG_HOP_CHI_PHI_ID") = 1
                                    FETCH FIRST 1 ROW ONLY

                            ) LTJ ON TRUE
                    -- Lấy lên phân bổ của kỳ trước đó
                    LEFT JOIN LATERAL (SELECT
                                        SUI."MA_CCDC"
                                        , SUI."DOI_TUONG_PHAN_BO_ID" AS ObjectID
                                        , SUI."TY_LE"
                                        , V."LOAI_DOI_TUONG_PBCP"
                                        , SUI."TK_NO_ID"
                                        , SUI."KHOAN_MUC_CP_ID"

                                    FROM supply_phan_bo_chi_phi_phan_bo SUI
                                        INNER JOIN supply_phan_bo_chi_phi A ON SUI."PHAN_BO_CHI_PHI_ID" = A."id"
                                        LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V
                                            ON SUI."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")
                                                AND SUI."DOI_TUONG_PHAN_BO_ID" LIKE concat(v."MODEL", ',%%')


                                    WHERE SUI."MA_CCDC" = FI."id"
                                            AND ((A."state" = 'da_ghi_so'

                                    )

                                            )
                                            AND A."NGAY_CHUNG_TU" < v_tu_ngay
                                    ORDER BY
                                        A."NGAY_CHUNG_TU" DESC,
                                        "STT_NHAP_CT" DESC
                                    FETCH FIRST 1 ROW ONLY

                            ) PrevAl ON TRUE

                WHERE TempAD."CCDC_ID" IS NULL /*Đã tồn tại trên phần phòng ban thì không kiểm tra tiếp cái này nữa*/
                    AND FI."CHI_NHANH_ID" = v_chi_nhanh_id
                    AND ((FI."state" = 'da_ghi_so'

                )

                    )
                    -- Tồn tại chứng từ điều chuyển
                    AND (LT."MA_CCDC_ID" IS NOT NULL
                        -- Chưa có phân bổ ở kỳ trước thì so sánh với bảng thiết lập phân bổ trên ghi tăng
                        -- Hoặc nếu có phân bổ ở kỳ trước thì công trình/ĐT tập hợp chi phí phân bổ ở kỳ trước tỷ lệ phân bổ 100%%
                        AND ((PrevAl.ObjectID IS NULL AND ((LTPW."MA_CCDC_ID" IS NOT NULL AND SIDA."LOAI_DOI_TUONG" = '1') OR
                                                            (LTJ."MA_CCDC_ID" IS NOT NULL AND SIDA."LOAI_DOI_TUONG" = '0'))
                                AND
                                SIDA."TY_LE_PB" = 100)
                                OR (PrevAl.ObjectID IS NOT NULL AND
                                    ((LTPW."MA_CCDC_ID" IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 1) OR
                                    (LTJ."MA_CCDC_ID" IS NOT NULL AND PrevAl."LOAI_DOI_TUONG_PBCP" = 0)) AND
                                    PrevAl."TY_LE" = 100)
                        )
                    )
            ;


            DROP TABLE IF EXISTS TMP_PB_CHI_TIET_KQ
            ;

            CREATE TABLE TMP_PB_CHI_TIET_KQ
                AS
                    SELECT
                        D."CCDC_ID"               AS "GHI_TANG_CCDC_ID"
                        , D."DOI_TUONG_PHAN_BO_ID"
                        , D."TK_GIA_VON"            AS "TK_CHI_PHI"
                        , D."TY_LE_PHAN_BO"         AS "TY_LE_PHAN_TRAM"
                        , V."MA_DOI_TUONG_PBCP"     AS "DOI_TUONG_PHAN_BO"
                        , V."TEN_DOI_TUONG_PBCP"    AS "TEN_DOI_TUONG_PHAN_BO"
                        , V."LOAI_DOI_TUONG_PBCP"
                        , D."TAI_KHOAN_CHO_PHAN_BO" AS "TK_CHO_PHAN_BO_ID"
                        , D."KHOAN_MUC_CP"          AS "KHOAN_MUC_CP_ID"
                        , "MA_CCDC"
                        , D."STT"                   AS "THU_TU_SAP_XEP"
                    FROM TMP_PBCP_CHI_TIET D
                        LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V
                            ON
                                D."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")
                                AND D."DOI_TUONG_PHAN_BO_ID" LIKE concat(v."MODEL", ',%%')

                    WHERE V."LOAI_DOI_TUONG_PBCP" IS NOT NULL/* tránh lỗi TH xóa đối tượng phân bổ*/
                    -- Lấy lên phần CCDC không ở bảng tạm trên
                    UNION ALL
                    (SELECT
                        SUA."GHI_TANG_THIET_LAP_PHAN_BO_ID" AS "GHI_TANG_CCDC_ID"
                        , SUA."DOI_TUONG_PHAN_BO_ID"          AS "DOI_TUONG_PHAN_BO_ID"
                        , SUA."TK_NO_ID"                      AS "TK_CHI_PHI"
                        , SUA."TY_LE_PB"                      AS "TY_LE_PHAN_TRAM"
                        , V."MA_DOI_TUONG_PBCP"               AS "DOI_TUONG_PHAN_BO"
                        , V."TEN_DOI_TUONG_PBCP"              AS "TEN_DOI_TUONG_PHAN_BO"
                        , V."LOAI_DOI_TUONG_PBCP"
                        , FI."TK_CHO_PHAN_BO_ID"              AS "TK_CHO_PHAN_BO_ID"
                        , SUA."KHOAN_MUC_CP_ID"
                        , FI."MA_CCDC"
                        , SUA."sequence"
                    FROM supply_ghi_tang_thiet_lap_phan_bo AS SUA
                        INNER JOIN supply_ghi_tang AS FI ON SUA."GHI_TANG_THIET_LAP_PHAN_BO_ID" = FI."id"
                        LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V
                            ON SUA."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")
                                AND SUA."DOI_TUONG_PHAN_BO_ID" LIKE concat(v."MODEL", ',%%')

                        LEFT JOIN TMP_PBCP_CHI_TIET D ON FI."id" = D."CCDC_ID"
                    WHERE FI."CHI_NHANH_ID" = v_chi_nhanh_id
                        AND ((FI."state" = 'da_ghi_so'

                    )

                        )
                        AND D."CCDC_ID" IS NULL
                    ORDER BY
                        "MA_CCDC",
                        SUA."sequence",
                        SUA.id)
            ;

            DROP TABLE IF EXISTS TMP_HACH_TOAN
            ;

            CREATE TABLE TMP_HACH_TOAN
                AS
                    -- Lấy lên chứng từ phân bổ kỳ trước
                    SELECT
                        SU1."MA_CCDC"
                        , SU1."TEN_CCDC"
                        , SU1."DOI_TUONG_PHAN_BO_ID"
                        , SU1."TK_NO_ID"
                        , SU1."TY_LE"
                        , V."MA_DOI_TUONG_PBCP"
                        , V."TEN_DOI_TUONG_PBCP"
                        , V."LOAI_DOI_TUONG_PBCP"
                        , SU1."TK_CHO_PHAN_BO_ID"
                        , SU1."KHOAN_MUC_CP_ID"
                    FROM (SELECT
                            SUD."id"
                            , FI."TEN_CCDC"
                            , SUD."PHAN_BO_CHI_PHI_ID"
                            , SUD."MA_CCDC"
                            , FI."TK_CHO_PHAN_BO_ID"
                            , SUD."DOI_TUONG_PHAN_BO_ID"
                            , SUD."TK_NO_ID"
                            , SUD."TY_LE"
                            , SUD."SO_TIEN"
                            , SUD."sequence"
                            , SUD."KHOAN_MUC_CP_ID"
                        FROM supply_phan_bo_chi_phi_phan_bo AS SUD
                            --INNER JOIN SUAllocation AS SU ON SUD."ID_CHUNG_TU" = SU."ID_CHUNG_TU"
                            INNER JOIN supply_ghi_tang AS FI ON SUD."MA_CCDC" = FI."id"
                            LEFT JOIN TMP_PBCP_CHI_TIET D ON (D."TU_DIEU_CHUYEN" = TRUE AND D."CCDC_ID" = SUD."MA_CCDC")
                        WHERE
                            SUD."PHAN_BO_CHI_PHI_ID" IN (
                                SELECT "id"
                                FROM supply_phan_bo_chi_phi AS SU1
                                WHERE SU1."CHI_NHANH_ID" = v_chi_nhanh_id
                                        AND ((SU1."state" = 'da_ghi_so'

                                            )
                                            -- thêm điều kiện này để chỉ lấy những phân bổ chi phí trước ngày hạch toán
                                            AND SU1."NGAY_HACH_TOAN" < v_tu_ngay
                                        )
                                ORDER BY SU1."NGAY_HACH_TOAN" DESC
                                LIMIT 1)
                            AND D."CCDC_ID" IS NULL

                        ) AS SU1
                        LEFT JOIN VIEW_DOI_TUONG_PHAN_BO_CHI_PHI AS V


                            ON SU1."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', v."DOI_TUONG_PHAN_BO_ID")
                            AND SU1."DOI_TUONG_PHAN_BO_ID" LIKE concat(v."MODEL", ',%%')


                            AND v.active = TRUE /*không lấy lên các đối tượng đã ngừng theo dõi sửa theo bug 42677*/
                    WHERE V."LOAI_DOI_TUONG_PBCP" IS NOT NULL/* tránh lỗi TH xóa đối tượng phân bổ*/
                    ORDER BY
                        SU1."sequence",SU1.id
            ;


        END $$

        ;





            SELECT

                HT."MA_CCDC" AS "CCDC_ID"
                ,HT."TEN_CCDC"
                , HT."DOI_TUONG_PHAN_BO_ID"
                , HT."TEN_DOI_TUONG_PBCP"
                , HT."TK_NO_ID"
                ,(select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan TK where TK.id = HT."TK_NO_ID" ) as "TK_NO"
                , HT."TY_LE"
                , HT."MA_DOI_TUONG_PBCP"
                , HT."TEN_DOI_TUONG_PBCP"
                , HT."LOAI_DOI_TUONG_PBCP"
                ,HT."TK_CHO_PHAN_BO_ID"
                ,(select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan TK where TK.id = HT."TK_CHO_PHAN_BO_ID" ) as "TK_CO"
                , HT."KHOAN_MUC_CP_ID"

            FROM  TMP_HACH_TOAN HT
            ;



        """  
        
        return self.execute(query, params)



    
    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			DROP VIEW IF EXISTS VIEW_DOI_TUONG_PHAN_BO_CHI_PHI ;
            CREATE VIEW VIEW_DOI_TUONG_PHAN_BO_CHI_PHI --View_DIViewAllocationObject
            AS
            SELECT
            "id" AS "DOI_TUONG_PHAN_BO_ID" ,
            'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL",
            "MA_DOI_TUONG_THCP" AS "MA_DOI_TUONG_PBCP" ,
            "TEN_DOI_TUONG_THCP" AS "TEN_DOI_TUONG_PBCP" ,
            CAST(0 AS INT) AS "LOAI_DOI_TUONG_PBCP" ,
            N'Đối tượng THCP' AS "TEN_LOAI_DOI_TUONG_PBCP" ,

            "active" ,
            CAST(0 AS BOOLEAN) AS "LA_TK_TONG_HOP_PBCP" ,
            CAST(0 AS VARCHAR(50)) AS "LOAI_DON_VI_ID" ,
            "MA_PHAN_CAP"
            FROM danh_muc_doi_tuong_tap_hop_chi_phi
            WHERE "id" NOT IN ( SELECT DISTINCT
            "parent_id"
            FROM danh_muc_doi_tuong_tap_hop_chi_phi
            WHERE "parent_id" IS NOT NULL )
            UNION ALL
            SELECT danh_muc_cong_trinh."id" AS "DOI_TUONG_PHAN_BO_ID" ,
            'danh.muc.cong.trinh' AS "MODEL",
            danh_muc_cong_trinh."MA_CONG_TRINH" AS "MA_DOI_TUONG_PBCP" ,
            danh_muc_cong_trinh."TEN_CONG_TRINH" AS "TEN_DOI_TUONG_PBCP" ,
            CAST(1 AS INT) AS "LOAI_DOI_TUONG_PBCP" ,
            N'Công trình' AS "TEN_LOAI_DOI_TUONG_PBCP" ,

            "active" ,
            CAST(0 AS BOOLEAN) AS "LA_TK_TONG_HOP_PBCP" ,
            CAST(0 AS VARCHAR(50)) AS "LOAI_DON_VI_ID" ,
            "MA_PHAN_CAP"
            FROM danh_muc_cong_trinh
            WHERE "id" NOT IN ( SELECT DISTINCT
            "parent_id"
            FROM danh_muc_cong_trinh
            WHERE "parent_id" IS NOT NULL )
            UNION ALL
            SELECT account_ex_don_dat_hang."id" AS "DOI_TUONG_PHAN_BO_ID" ,
            'account.ex.don.dat.hang' AS "MODEL",
            account_ex_don_dat_hang."SO_DON_HANG" AS "MA_DOI_TUONG_PBCP" ,
            account_ex_don_dat_hang."DIEN_GIAI" AS "TEN_DOI_TUONG_PBCP" ,
            CAST(2 AS INT) AS "LOAI_DOI_TUONG_PBCP" ,
            N'Đơn hàng' AS "TEN_LOAI_DOI_TUONG_PBCP" ,

            CAST(0 AS BOOLEAN) AS active ,
            CAST(0 AS BOOLEAN) AS "LA_TK_TONG_HOP_PBCP" ,
            CAST(0 AS VARCHAR(50)) AS "LOAI_DON_VI_ID" ,
            '/0' AS "MA_PHAN_CAP"
            FROM account_ex_don_dat_hang
            WHERE ( "TINH_TRANG" = '0' /* Không load đơn đặt hàng có tình trạng là Hoàn thành và Đã hủy bỏ*/
            OR "TINH_TRANG" = '1'
            )
            AND "TINH_GIA_THANH" = TRUE
            /* chỉ load các đơn đặt hàng, hợp đồng bán có tích chọn tính giá thành*/
            UNION ALL
            SELECT sale_ex_hop_dong_ban."id" AS "DOI_TUONG_PHAN_BO_ID" ,
            'sale.ex.hop.dong.ban' AS "MODEL",
            sale_ex_hop_dong_ban."SO_HOP_DONG" AS "MA_DOI_TUONG_PBCP" ,
            sale_ex_hop_dong_ban."TRICH_YEU" AS "TEN_DOI_TUONG_PBCP" ,
            CAST(3 AS INT) AS "LOAI_DOI_TUONG_PBCP" ,
            N'Hợp đồng' AS "TEN_LOAI_DOI_TUONG_PBCP" ,

            CAST(0 AS BOOLEAN) AS active ,
            CAST(0 AS BOOLEAN) AS "LA_TK_TONG_HOP_PBCP" ,
            CAST(0 AS VARCHAR(50)) AS "LOAI_DON_VI_ID" ,
            CASE WHEN "THUOC_DU_AN_ID" IS NULL THEN 'Z' ELSE CAST("THUOC_DU_AN_ID" AS VARCHAR(100)) END || '1' AS "MA_PHAN_CAP"
            FROM sale_ex_hop_dong_ban
            WHERE ( "TINH_TRANG_HOP_DONG" = '0' /* Không load các hợp đồng bán có tình trạng là Đã thanh lý và Đã hủy bỏ*/
            OR "TINH_TRANG_HOP_DONG" = '1'
            OR "TINH_TRANG_HOP_DONG" = '2'
            )
            AND "TINH_GIA_THANH" = TRUE
            AND "LA_DU_AN" = FALSE
            UNION ALL
            /*dự án cũng để là loại HĐ*/
            SELECT "id" AS "DOI_TUONG_PHAN_BO_ID" ,
            'sale.ex.hop.dong.ban' AS "MODEL",
            "SO_HOP_DONG" AS "MA_DOI_TUONG_PBCP" ,
            "SO_HOP_DONG" AS "TEN_DOI_TUONG_PBCP" ,
            CAST(3 AS INT) AS "LOAI_DOI_TUONG_PBCP" ,
            N'Hợp đồng' AS "TEN_LOAI_DOI_TUONG_PBCP" ,

            CAST(0 AS BOOLEAN) AS active ,
            CAST(1 AS BOOLEAN) AS "LA_TK_TONG_HOP_PBCP" ,
            CAST(0 AS VARCHAR(50)) AS "LOAI_DON_VI_ID" ,
            CAST("id" AS VARCHAR(100)) || '0' AS "MA_PHAN_CAP"
            FROM sale_ex_hop_dong_ban
            WHERE ( "TINH_TRANG_HOP_DONG" = '0' /* Không load các Dự án có tình trạng là Đã thanh lý và Đã hủy bỏ*/
            OR "TINH_TRANG_HOP_DONG" = '1'
            OR "TINH_TRANG_HOP_DONG" = '2'
            )
            AND "TINH_GIA_THANH" = TRUE
            AND "LA_DU_AN" = TRUE
            UNION ALL
            SELECT OU."id" AS "DOI_TUONG_PHAN_BO_ID" ,
            'danh.muc.to.chuc' AS "MODEL",
            OU."MA_DON_VI" AS "MA_DOI_TUONG_PBCP" ,
            OU."TEN_DON_VI" AS "TEN_DOI_TUONG_PBCP" ,
            CAST(4 AS INT) AS "LOAI_DOI_TUONG_PBCP" ,
            N'Đơn vị' AS "TEN_LOAI_DOI_TUONG_PBCP" ,

            OU.active ,
            OU."ISPARENT" AS "LA_TK_TONG_HOP_PBCP" ,
            OU."CAP_TO_CHUC" ,
            "MA_PHAN_CAP"
            FROM danh_muc_to_chuc OU
            WHERE "CAP_TO_CHUC" IN ( '3', '4', '5', '6' ) ;

            SELECT * FROM VIEW_DOI_TUONG_PHAN_BO_CHI_PHI ;
		""")

