# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_FORM(models.Model):
    _name = 'gia.thanh.khai.bao.dinh.muc.gttp.form'
    _description = ''
    _inherit = ['mail.thread']
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_CHI_TIET_IDS = fields.One2many('gia.thanh.khai.bao.dinh.muc.gttp.chi.tiet', 'CHI_TIET_ID', string='Khai báo định mức giá thành thành phẩm chi tiết')


    
    @api.model
    def create(self, values):
        chi_tiet_ids = self.env['gia.thanh.khai.bao.dinh.muc.gttp.chi.tiet'].search([])
        if chi_tiet_ids:
            for chi_tiet in chi_tiet_ids:
                chi_tiet.unlink()
        master = self.env['gia.thanh.khai.bao.dinh.muc.gttp.form'].search([])
        if master:
            for mt in master:
                mt.unlink()

        if values.get('GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_CHI_TIET_IDS'):
            for line in values.get('GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_CHI_TIET_IDS'):
                if line[2].get('NVL_TRUC_TIEP') > 0 or line[2].get('NVL_GIAN_TIEP') > 0 or line[2].get('NHAN_CONG_TRUC_TIEP') > 0 or line[2].get('NHAN_CONG_GIAN_TIEP') > 0 or line[2].get('KHAU_HAO') > 0 or line[2].get('CHI_PHI_MUA_NGOAI') > 0 or line[2].get('CHI_PHI_KHAC') > 0:
                    self.env['gia.thanh.khai.bao.dinh.muc.gttp.chi.tiet'].create(line[2])
        values['GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_CHI_TIET_IDS'] = {}
        result = super(GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_FORM, self).create(values)
        return result
    

    def lay_du_lieu_gia_thanh_khai_bao_dinh_muc(self, args):
        new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham = [[5]]
        chi_nhanh_id = self.get_chi_nhanh()
        du_lieu_dinh_muc_gia_thanh = self.du_lieu_gia_thanh_thanh_pham(chi_nhanh_id)
        if du_lieu_dinh_muc_gia_thanh:
            for line in du_lieu_dinh_muc_gia_thanh:
                new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham += [(0,0,{
                            'MA_THANH_PHAM_ID' : [line.get('MA_THANH_PHAM_ID'),line.get('MA_THANH_PHAM')],
                            'TEN_THANH_PHAM' : line.get('TEN_THANH_PHAM'),
                            'DON_VI_TINH_ID' : [line.get('DVT_ID'),line.get('DON_VI_TINH')],
                            'NVL_TRUC_TIEP' : line.get('NVL_TRUC_TIEP'),
                            'NVL_GIAN_TIEP' : line.get('NVL_GIAN_TIEP'),
                            'NHAN_CONG_TRUC_TIEP' : line.get('NHAN_CONG_TRUC_TIEP'),
                            'NHAN_CONG_GIAN_TIEP' : line.get('NHAN_CONG_GIAN_TIEP'),
                            'KHAU_HAO' : line.get('KHAU_HAO'),
                            'CHI_PHI_MUA_NGOAI' : line.get('CHI_PHI_MUA_NGOAI'),
                            'CHI_PHI_KHAC' : line.get('CHI_PHI_KHAC'),
                            })]

        return {'GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_CHI_TIET_IDS': new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham,}    


    def du_lieu_gia_thanh_thanh_pham(self,chi_nhanh_id):
        params = {
            'CHI_NHANH_ID' : chi_nhanh_id,
            }
        query = """   
                DO LANGUAGE plpgsql $$
                DECLARE
                
                
                    chi_nhanh_id            INTEGER := %(CHI_NHANH_ID)s;
                
                    IsUseSeperate           BOOLEAN :=FALSE;
                
                    loai_tinh_chat_san_pham INTEGER := 1;
                
                
                BEGIN
                
                
                    DROP TABLE IF EXISTS TMP_KET_QUA
                    ;
                
                    CREATE TEMP TABLE TMP_KET_QUA
                        AS
                
                
                            SELECT
                                II."id" AS "ID_THANH_PHAM"
                                , COALESCE("NVL_TRUC_TIEP", 0)                          "NVL_TRUC_TIEP"
                                , COALESCE("NVL_GIAN_TIEP", 0)                          "NVL_GIAN_TIEP"
                                , COALESCE("NHAN_CONG_TRUC_TIEP", 0) "NHAN_CONG_TRUC_TIEP"
                                , COALESCE("NHAN_CONG_GIAN_TIEP", 0)                    "NHAN_CONG_GIAN_TIEP"
                                , COALESCE("KHAU_HAO", 0)                               "KHAU_HAO"
                                , COALESCE("CHI_PHI_MUA_NGOAI", 0)                            "CHI_PHI_MUA_NGOAI"
                                , COALESCE("CHI_PHI_KHAC", 0)                          "CHI_PHI_KHAC"
                                , COALESCE("TONG_CONG", 0)                "TONG_CONG"
                                , II.id AS "MA_THANH_PHAM_ID" 
                                , II."MA" AS "MA_THANH_PHAM"
                                , II."TEN" AS "TEN_THANH_PHAM"
                                , danh_muc_don_vi_tinh."DON_VI_TINH"
                                , II."DVT_CHINH_ID" AS "DVT_ID"
                
                            FROM gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet AS PQ
                                RIGHT JOIN danh_muc_vat_tu_hang_hoa AS II ON PQ."MA_THANH_PHAM_ID" = II."id"
                                LEFT JOIN danh_muc_don_vi_tinh ON II."DVT_CHINH_ID" = danh_muc_don_vi_tinh."id"
                            WHERE "TINH_CHAT" = CAST(loai_tinh_chat_san_pham AS VARCHAR )
                    AND (IsUseSeperate = FALSE
                    OR (IsUseSeperate = TRUE
                    AND II."CHI_NHANH_ID" =  chi_nhanh_id
                    )
                    ) ;
                
                END $$
                ;
                
                
                SELECT *
                FROM TMP_KET_QUA
                
                ;
                
        """  
        return self.execute(query, params)