# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BANG_TINH_GIA_THANH(models.Model):
    _name = 'bao.cao.bang.tinh.gia.thanh'
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc')
    PP_TINH_GIA_THANH = fields.Selection([('PHUONG_PHAP_TINH_GIA_THANH_DON_GIAN', 'Phương pháp tính giá thành giản đơn'), ('PHUONG_PHAP_TINH_GIA_THANH_HE_SO_TY_LE', 'Phương pháp tính giá thành hệ số tỷ lệ'), ], string='PP tính giá thành', help='Pp tính giá thành', default='PHUONG_PHAP_TINH_GIA_THANH_DON_GIAN', required='True')
    KY_TINH_GIA_THANH = fields.Many2one( 'gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    MA_THANH_PHAM = fields.Char(string='Mã thành phẩm', help='Mã thành phẩm')#, auto_num='bao_cao_bang_tinh_gia_thanh_MA_THANH_PHAM')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='Nguyên vật liệu trực tiếp',digits=decimal_precision.get_precision('VND'))
    NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Nguyên vật liệu gián tiếp',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp', help='Nhân công gián tiếp',digits=decimal_precision.get_precision('VND'))
    KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='Chi phí khác', help='Chi phí khác',digits= decimal_precision.get_precision('VND'))
    TONG = fields.Float(string='Tổng', help='Tổng',digits=decimal_precision.get_precision('VND'))
    SO_LUONG_THANH_PHAM = fields.Float(string='Số lượng thành phẩm', help='Số lượng thành phẩm', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_THANH_DON_VI = fields.Float(string='Giá thành đơn vị', help='Giá thành đơn vị',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BANG_TINH_GIA_THANH, self).default_get(fields_list)
      
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1) 
        if chi_nhanh :
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result

    @api.onchange('PP_TINH_GIA_THANH')
    def _onchange_pp_tinh_gia_thanh(self):
        self.KY_TINH_GIA_THANH = False

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        PP_TINH_GIA_THANH = params['PP_TINH_GIA_THANH'] if 'PP_TINH_GIA_THANH' in params.keys() else 'False'
        KY_TINH_GIA_THANH = params['KY_TINH_GIA_THANH'] if 'KY_TINH_GIA_THANH' in params.keys() and params['KY_TINH_GIA_THANH'] != 'False' else None
        
        params_sql = {
            'CHI_NHANH_ID':CHI_NHANH_ID, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'PP_TINH_GIA_THANH':PP_TINH_GIA_THANH,
            'KY_TINH_GIA_THANH':KY_TINH_GIA_THANH,
            'limit': limit,
            'offset': offset, 
            }      
        # Execute SQL query here
        query = """
        DO LANGUAGE plpgsql $$
        DECLARE
        
            ky_tinh_gia_thanh_id       INTEGER := %(KY_TINH_GIA_THANH)s;   
        
            PP_TINH_GIA_THANH          VARCHAR:= %(PP_TINH_GIA_THANH)s;   
        
        
        BEGIN
        
        
            DROP TABLE IF EXISTS TMP_KET_QUA
            ;
        
            IF PP_TINH_GIA_THANH = 'PHUONG_PHAP_TINH_GIA_THANH_DON_GIAN'
            THEN
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                        SELECT
                    
                     ROW_NUMBER()
                          OVER (
                              ORDER BY ii."MA" )  AS "RowNumber"
        
        
                            ,ii."MA"                                                           AS "MA_THANH_PHAM"
                            , -- Mã VTHH
                            ii."TEN"                                                          AS "TEN_THANH_PHAM"
                            , -- Tên VTHH
                            j."MA_DOI_TUONG_THCP"
                            , -- Mã đối tượng THCP
                            -- Tên đối tượng THCP
                            CASE WHEN JP."LOAI_GIA_THANH" = 'DON_GIAN'
                                THEN J."TEN_DOI_TUONG_THCP"
                            ELSE (j."MA_DOI_TUONG_THCP" || ' - ' || j."TEN_DOI_TUONG_THCP") END AS "TEN_DOI_TUONG_THCP"
                            ,
        
                            JPCD."NVL_TRUC_TIEP"
                            , -- chi phí nguyên vật liệu trực tiếp
                            JPCD."NVL_GIAN_TIEP"
                            , -- chi phí nguyên vật liệu gián tiếp
                            JPCD."NHAN_CONG_TRUC_TIEP"
                            , -- Chi phí nhân công trực tiếp trong kỳ
                            JPCD."NHAN_CONG_GIAN_TIEP"
                            , -- Chi phí nhân công gián tiếp
                            JPCD."KHAU_HAO"
                            , -- Chi phí khấu hao
                            JPCD."CHI_PHI_MUA_NGOAI"
                            , -- Chi phí mua ngoài
                            JPCD."CHI_PHI_KHAC"
                            , -- Chi phí khác
                            JPCD."TONG"
                            , -- Tổng giá thành
                            JPCD."SO_LUONG_THANH_PHAM"
                            , -- Tổng số lượng
                            JPCD."GIA_THANH_DON_VI" -- Giá thành đơn vị
        
        
                        FROM gia_thanh_ky_tinh_gia_thanh AS JP INNER JOIN gia_thanh_bang_gia_thanh_chi_tiet AS JPCD
                                ON JP."id" = JPCD."KY_TINH_GIA_THANH_ID"
                            LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON JPCD."MA_THANH_PHAM_ID" = II."id"
                            LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON j."id" = JPCD."MA_DOI_TUONG_THCP_ID"
                        WHERE JPCD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
        
                        ORDER BY ii."MA"
                ;
            ELSE
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
        
                        SELECT
                            
                              ROW_NUMBER()
                          OVER (
                               ORDER BY j."MA_DOI_TUONG_THCP", ii."MA" )  AS "RowNumber"
                            ,ii."MA" AS "MA_THANH_PHAM"
                            , -- Mã VTHH
                            ii."TEN" AS "TEN_THANH_PHAM"
                            , -- Tên VTHH
                            j."MA_DOI_TUONG_THCP"
                            , -- Mã đối tượng THCP
                            -- Tên đối tượng THCP
                              CASE WHEN JP."LOAI_GIA_THANH" = 'DON_GIAN'
                                  THEN J."TEN_DOI_TUONG_THCP"
                              ELSE (j."MA_DOI_TUONG_THCP" || ' - ' || j."TEN_DOI_TUONG_THCP") END AS "TEN_DOI_TUONG_THCP"
        
                            , -- Hệ số, tỷ lệ phân bổ giá thành
                            --JPCD."STT" ,
                            JPCD."NVL_TRUC_TIEP"
                            , -- chi phí nguyên vật liệu trực tiếp
                            JPCD."NVL_GIAN_TIEP"
                            , -- chi phí nguyên vật liệu gián tiếp
                            JPCD."NHAN_CONG_TRUC_TIEP"
                            , -- Chi phí nhân công trực tiếp trong kỳ
                            JPCD."NHAN_CONG_GIAN_TIEP"
                            , -- Chi phí nhân công gián tiếp
                            JPCD."KHAU_HAO"
                            , -- Chi phí khấu hao
                            JPCD."CHI_PHI_MUA_NGOAI"
                            , -- Chi phí mua ngoài
                            JPCD."CHI_PHI_KHAC"
                            , -- Chi phí khác
                            JPCD."TONG"
                            , -- Tổng giá thành
                            JPCD."SO_LUONG_THANH_PHAM"
                            , -- Tổng số lượng
                            JPCD."GIA_THANH_DON_VI" -- Giá thành đơn vị
        
        
                        FROM gia_thanh_ky_tinh_gia_thanh AS JP INNER JOIN gia_thanh_bang_gia_thanh_chi_tiet AS JPCD
                                ON JP."id" = JPCD."KY_TINH_GIA_THANH_ID"
                            LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON JPCD."MA_THANH_PHAM_ID" = II."id"
                            LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON j."id" = JPCD."MA_DOI_TUONG_THCP_ID"
                        WHERE JPCD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
        
                        ORDER BY j."MA_DOI_TUONG_THCP", ii."MA"
                ;
            END IF
            ;
        
        END $$
        ;
        
        
        SELECT 
                "MA_THANH_PHAM" AS "MA_THANH_PHAM",
                "TEN_THANH_PHAM" AS "TEN_THANH_PHAM",
                "TEN_DOI_TUONG_THCP" AS "TEN_DOI_TUONG_THCP",
                "NVL_TRUC_TIEP" AS "NVL_TRUC_TIEP",
                "NVL_GIAN_TIEP" AS "NVL_GIAN_TIEP",
                "NHAN_CONG_TRUC_TIEP" AS "NHAN_CONG_TRUC_TIEP",
                "NHAN_CONG_GIAN_TIEP" AS "NHAN_CONG_GIAN_TIEP",
                "KHAU_HAO" AS "KHAU_HAO",
                "CHI_PHI_MUA_NGOAI" AS "CHI_PHI_MUA_NGOAI",
                "CHI_PHI_KHAC" AS "CHI_PHI_KHAC",
                "TONG" AS "TONG",
                "SO_LUONG_THANH_PHAM" AS "SO_LUONG_THANH_PHAM",
                "GIA_THANH_DON_VI" AS "GIA_THANH_DON_VI"
                           
                FROM TMP_KET_QUA
                ORDER BY  "RowNumber"
                OFFSET %(offset)s
                LIMIT %(limit)s;
        """
        return self.execute(query,params_sql)

    
    def _validate(self):
        params = self._context
        KY_TINH_GIA_THANH = params['KY_TINH_GIA_THANH'] if 'KY_TINH_GIA_THANH' in params.keys() else 'False'
        if(KY_TINH_GIA_THANH=='False'):
            raise ValidationError('<Kỳ tính giá thành> không được bỏ trống.')

    def _action_view_report(self):
        self._validate()
        PP_TINH_GIA_THANH = self.get_context('PP_TINH_GIA_THANH')
        ky_tinh_gia_thanh = self._context.get('KY_TINH_GIA_THANH')
        param =''
        if PP_TINH_GIA_THANH == 'PHUONG_PHAP_TINH_GIA_THANH_DON_GIAN':
            if ky_tinh_gia_thanh:
                ten_ky_tinh_gia_thanh = self.env['gia.thanh.ky.tinh.gia.thanh'].search([('id', '=', ky_tinh_gia_thanh)]).TEN
            param = 'Kỳ tính giá thành: %s' % (ten_ky_tinh_gia_thanh)
            action = self.env.ref('bao_cao.open_report__bang_tinh_gia_thanh_gian_don').read()[0]
        elif PP_TINH_GIA_THANH == 'PHUONG_PHAP_TINH_GIA_THANH_HE_SO_TY_LE':
            if ky_tinh_gia_thanh:
                ten_ky_tinh_gia_thanh = self.env['gia.thanh.ky.tinh.gia.thanh'].search([('id', '=', ky_tinh_gia_thanh)]).TEN
            param = 'Kỳ tính giá thành: %s' % (ten_ky_tinh_gia_thanh)
            action = self.env.ref('bao_cao.open_report__bang_tinh_gia_thanh_hstl').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action