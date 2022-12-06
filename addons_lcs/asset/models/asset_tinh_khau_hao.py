# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime
import logging
_logger = logging.getLogger(__name__)

class ASSET_TINH_KHAU_HAO(models.Model):
    _name = 'asset.tinh.khau.hao'
    _description = ''
    _inherit = ['mail.thread']
    _order = "NGAY_HACH_TOAN desc, NGAY_CHUNG_TU desc"

    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    THANG = fields.Integer(string='Tháng', help='Tháng')
    NAM = fields.Integer(string='Năm', help='Năm')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='asset_tinh_khau_hao_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
    SO_TSCD_ID = fields.Many2one('so.tscd', ondelete='set null')
    STT_CHUNG_TU = fields.Char(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ', auto_num='asset_STT_CHUNG_TU') 
    ASSET_TINH_KHAU_HAO_CHI_TIET_IDS = fields.One2many('asset.tinh.khau.hao.chi.tiet', 'TINH_KHAU_HAO_ID', string='Tính khấu hao chi tiết')
    ASSET_TINH_KHAU_HAO_HACH_TOAN_IDS = fields.One2many('asset.tinh.khau.hao.hach.toan', 'TINH_KHAU_HAO_ID', string='Tính khấu hao hạch toán')
    ASSET_TINH_KHAU_HAO_PHAN_BO_IDS = fields.One2many('asset.tinh.khau.hao.phan.bo', 'TINH_KHAU_HAO_ID', string='Tính khâu hao phân bổ')

    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',compute='tinh_tong_tien',store=True)

    _sql_constraints = [
	('SO_CHUNG_TU_uniq', 'unique ("SO_CHUNG_TU")', 'Số chứng từ <<>> đã tồn tại!'),
	]

    # comment đoạn này vì form này là đổ dữ liệu vào chứ không phải tạo mới
    # @api.onchange('LOAI_CHUNG_TU')
    # def update_tai_khoan_ngam_dinh(self):
    #     for line in self.ASSET_TINH_KHAU_HAO_HACH_TOAN_IDS:
    #         tk_nds = line.lay_tai_khoan_ngam_dinh(self.LOAI_CHUNG_TU, getattr(self, 'NHOM_CHUNG_TU', 0))
    #         for tk in tk_nds:
    #             setattr(line, tk, tk_nds.get(tk))

    @api.depends('ASSET_TINH_KHAU_HAO_HACH_TOAN_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien =  0
            for line in order.ASSET_TINH_KHAU_HAO_HACH_TOAN_IDS:
                tong_tien +=line.SO_TIEN

            order.update({
                'SO_TIEN':tong_tien,
            })
			
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN
    
    @api.model
    def default_get(self, fields):
        rec = super(ASSET_TINH_KHAU_HAO, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 254
        thang = rec.get('THANG')
        nam = rec.get('NAM')

        str_dien_giai = ''

        if thang and nam:
            rec['NGAY_HACH_TOAN'] = helper.Datetime.lay_ngay_cuoi_thang(nam, thang)
            rec['NGAY_CHUNG_TU'] = helper.Datetime.lay_ngay_cuoi_thang(nam, thang)
            gi_tang = self.lay_du_lieu_tinh_khau_hao(thang,nam)
            phan_bos = self.lay_du_lieu_phan_bo(thang,nam)
            str_dien_giai = 'Khấu hao TSCĐ tháng ' + str(thang) + ' năm ' + str(nam)
            arr_khau_hao = []
            arr_phan_bo = []
            arr_hach_toan = []
            dict_tam = {}

            dict_phan_bo = {}
            for phan_bo_moi in phan_bos:
                tscd_id = phan_bo_moi.get('TSCD_ID')
                if tscd_id not in dict_phan_bo:
                    dict_phan_bo[tscd_id] = []
                dict_phan_bo[tscd_id] += [phan_bo_moi]

            for line in gi_tang:
                tong_so_tien_phan_bo = float_round(line.get('GIA_TRI_TINH_KHAU_HAO_THANG'),0)
                arr_khau_hao += [(0, 0, {
                    'MA_TAI_SAN_ID' : line.get('TSCD_ID'),
                    'TEN_TAI_SAN': line.get('TEN_TSCD'),
                    'LOAI_TAI_SAN_ID': line.get('LOAI_TSCD_ID'),
                    'DON_VI_SU_DUNG_ID': line.get('DON_VI_SU_DUNG_ID'),
                    'GIA_TRI_KH_THANG': tong_so_tien_phan_bo,
                    'GIA_TRI_TINH_VAO_CP_HOP_LY' : float_round(line.get('CHI_PHI_HOP_LY'),0),
                    })]

                tscd_id = line.get('TSCD_ID')
                if tscd_id in dict_phan_bo:
                    phan_bo_ids = dict_phan_bo[tscd_id]
                    i = 0
                    so_tien_da_phan_bo = 0
                    for phan_bo in phan_bo_ids:
                        if i == len(phan_bo_ids) - 1:
                            so_tien_phan_bo_lan_nay = tong_so_tien_phan_bo - so_tien_da_phan_bo
                        else:
                            so_tien_phan_bo_tab_phan_bo = float_round((tong_so_tien_phan_bo*phan_bo.get('TY_LE_PB'))/100,0)
                            so_tien_da_phan_bo += so_tien_phan_bo_tab_phan_bo
                            so_tien_phan_bo_lan_nay = so_tien_phan_bo_tab_phan_bo
                        i+= 1
                        arr_phan_bo += [(0,0,{
                            'MA_TAI_SAN_ID' : phan_bo.get('TSCD_ID'),
                            'TEN_TAI_SAN' : phan_bo.get('TEN_TSCD'),
                            'DON_VI_SU_DUNG_ID': phan_bo.get('DON_VI_SU_DUNG_ID'),
                            'GIA_TRI_KH_THANG' : tong_so_tien_phan_bo,
                            'DOI_TUONG_PHAN_BO_ID' : phan_bo.get('DOI_TUONG_PHAN_BO_ID'),
                            'TEN_DOI_TUONG_PHAN_BO' : phan_bo.get('TEN_DOI_TUONG'),
                            'TY_LE' : phan_bo.get('TY_LE_PB'),
                            'CHI_PHI_PHAN_BO' : so_tien_phan_bo_lan_nay,
                            'TK_NO_ID' : phan_bo.get('TK_NO_ID') if phan_bo.get('TK_NO_ID') != -1 else False,
                            'KHOAN_MUC_CP_ID' : phan_bo.get('KHOAN_MUC_CP_ID'),
                            'MA_THONG_KE_ID' : phan_bo.get('MA_THONG_KE_ID'),
                        })]
                        doi_tuong_thcp = None
                        cong_trinh = None
                        don_dat_hang = None
                        hop_dong_ban = None
                        don_vi = None
                        doi_tuong_phan_bo = ''
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
                            
                        khoan_muc_cp = ''
                        if phan_bo.get('KHOAN_MUC_CP_ID') != False and phan_bo.get('KHOAN_MUC_CP_ID') != None:
                            khoan_muc_cp = str(phan_bo.get('KHOAN_MUC_CP_ID'))
                            
                        key = doi_tuong_phan_bo +','+  str(phan_bo.get('TK_NO_ID')) + ',' + khoan_muc_cp
                        if not key in dict_tam:
                            dict_tam[key] = {
                                    'DIEN_GIAI' : str_dien_giai,
                                    'TK_NO_ID' : phan_bo.get('TK_NO_ID') if phan_bo.get('TK_NO_ID') != -1 else False,
                                    'TK_CO_ID': phan_bo.get('TK_KHAU_HAO_ID'),
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

            rec['DIEN_GIAI'] = str_dien_giai
            rec['ASSET_TINH_KHAU_HAO_CHI_TIET_IDS'] = arr_khau_hao
            rec['ASSET_TINH_KHAU_HAO_HACH_TOAN_IDS'] = arr_hach_toan
            rec['ASSET_TINH_KHAU_HAO_PHAN_BO_IDS'] = arr_phan_bo
            
        return rec

    
    @api.model
    def create(self, values):
        if values.get('DIEN_GIAI'):
            values['name'] = values.get('DIEN_GIAI')
        
        result = super(ASSET_TINH_KHAU_HAO, self).create(values)
        return result

    # @api.multi
    # def validate(self, vals, option=None):
      # ngay_khoa_so = str(self.lay_ngay_khoa_so())
      # if vals.get('NGAY_CHUNG_TU') < ngay_khoa_so:
        # raise ValidationError("Ngày chứng từ không được nhỏ hơn ngày khóa sổ " +str(ngay_khoa_so)+ ". Vui lòng kiểm tra lại")
            
    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_cai()
            record.ghi_so_tscd()
        self.write({'state':'da_ghi_so'})
    def ghi_so_cai(self):
        line_ids = []
        thu_tu = 0
        for line in self.ASSET_TINH_KHAU_HAO_HACH_TOAN_IDS:
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'THU_TU_TRONG_CHUNG_TU': thu_tu,
                'DIEN_GIAI_CHUNG': self.DIEN_GIAI,
                'DON_VI_ID' : line.DON_VI_ID.id,
                'DIEN_GIAI' : line.DIEN_GIAI,
                'TAI_KHOAN_ID' : line.TK_NO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_CO_ID.id,
                'GHI_NO' : float_round(line.SO_TIEN,0),
                'GHI_NO_NGUYEN_TE' : float_round(line.SO_TIEN,0),
                'GHI_CO' : 0,
                'GHI_CO_NGUYEN_TE' : 0,
				'LOAI_HACH_TOAN' : '1',
                'TY_GIA' : 1,
            })
            line_ids += [(0,0,data_ghi_no)]

            data_ghi_co = data_ghi_no.copy()
            data_ghi_co.update({
                'TAI_KHOAN_ID' : line.TK_CO_ID.id,
                'TAI_KHOAN_DOI_UNG_ID' : line.TK_NO_ID.id,
                'GHI_NO' : 0,
                'GHI_NO_NGUYEN_TE' : 0,
                'GHI_CO' : float_round(line.SO_TIEN,0),
                'GHI_CO_NGUYEN_TE' : float_round(line.SO_TIEN,0),
				'LOAI_HACH_TOAN' : '2',
            })
            line_ids += [(0,0,data_ghi_co)]
            thu_tu += 1
        # Tạo master
        sc = self.env['so.cai'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CAI_ID = sc.id
        return True

    def ghi_so_tscd(self):
        line_ids = []
        thu_tu = 0
        for line in self.ASSET_TINH_KHAU_HAO_CHI_TIET_IDS:
            so_tscd = line.MA_TAI_SAN_ID.lay_du_lieu_tren_so(self.NGAY_HACH_TOAN)
            du_lieu_tinh_gtcl = line.MA_TAI_SAN_ID.lay_du_lieu_tren_so_de_tinh_gtcl(self.NGAY_HACH_TOAN)
            du_lieu_ngay_tren_so = line.MA_TAI_SAN_ID.lay_du_lieu_ngay_tren_so(self.NGAY_HACH_TOAN)
            if so_tscd:
                so_khau_hao = 0
                if du_lieu_tinh_gtcl:
                    # nếu là tháng tính khau hao đầu tiền thì tính khau hao từ ngay bắt đầu tính khấu hao else thì lấy theo ngày ghi tăng gần nhất trên sổ
                    if du_lieu_ngay_tren_so.MODEL_CHUNG_TU == 'asset.ghi.tang':
                        tu_ngay_de_tinh_khau_hang = line.MA_TAI_SAN_ID.NGAY_BAT_DAU_TINH_KH
                    else:
                        tu_ngay_de_tinh_khau_hang = du_lieu_ngay_tren_so.NGAY_HACH_TOAN
                    ngay_hien_tai = datetime.strptime(self.NGAY_HACH_TOAN, '%Y-%m-%d').date()
                    ngay_cuoi_cung_tren_so = datetime.strptime(tu_ngay_de_tinh_khau_hang, '%Y-%m-%d').date()
                    so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(ngay_hien_tai.year, ngay_hien_tai.month)
                    
                    if ngay_cuoi_cung_tren_so.month == ngay_hien_tai.month and ngay_cuoi_cung_tren_so.year == ngay_hien_tai.year and so_ngay_trong_thang != 0:
                        so_khau_hao = ((ngay_hien_tai.day - ngay_cuoi_cung_tren_so.day + 1)/so_ngay_trong_thang)*du_lieu_ngay_tren_so.GIA_TRI_KHAU_HAO_THANG
                    else:
                        so_khau_hao = du_lieu_tinh_gtcl.GIA_TRI_KHAU_HAO_THANG

                data_ghi_no = helper.Obj.inject(line, self)
                data_ghi_no.update({
                    'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                    'DIEN_GIAI_CHUNG' : self.DIEN_GIAI,
                    'TSCD_ID' : line.MA_TAI_SAN_ID.id,
                    'GIA_TRI_HAO_MON_LUY_KE' : so_tscd.GIA_TRI_HAO_MON_LUY_KE + line.GIA_TRI_TINH_VAO_CP_HOP_LY,
                    'THOI_GIAN_SU_DUNG' : so_tscd.THOI_GIAN_SU_DUNG,
                    'THOI_GIAN_SU_DUNG_CON_LAI' : so_tscd.THOI_GIAN_SU_DUNG_CON_LAI - 1,
                    'TY_LE_KHAU_HAO_THANG' : so_tscd.TY_LE_KHAU_HAO_THANG,
                    'GIA_TRI_KHAU_HAO_THANG' : so_tscd.GIA_TRI_KHAU_HAO_THANG,
                    'GIA_TRI_TINH_KHAU_HAO' : so_tscd.GIA_TRI_TINH_KHAU_HAO,
                    'GIA_TRI_CON_LAI' : 0 if (so_tscd.THOI_GIAN_SU_DUNG_CON_LAI - 1) < 0 else float_round(so_tscd.GIA_TRI_CON_LAI - line.GIA_TRI_TINH_VAO_CP_HOP_LY,0),
                    'NGUYEN_GIA' : so_tscd.NGUYEN_GIA,
                    'TK_NGUYEN_GIA_ID' : so_tscd.TK_NGUYEN_GIA_ID.id,
                    'TK_HAO_MON_ID' : so_tscd.TK_HAO_MON_ID.id,
                    'DON_VI_SU_DUNG_ID' : line.DON_VI_SU_DUNG_ID.id,
                    'GIA_TRI_KHAU_HAO_THANG_KHI_KH' : line.GIA_TRI_KH_THANG,
                    'THU_TU_TRONG_CHUNG_TU': thu_tu,
                })
                line_ids += [(0,0,data_ghi_no)]
                thu_tu += 1
            else:
                # raise ValidationError('Tài sản cố định này chưa được ghi sổ. Vui lòng ghi sổ lại tài sản cố định này')
                _logger.warn("Tài sản cố định này chưa được ghi sổ. Vui lòng ghi sổ lại tài sản cố định này")
        # Tạo master
        stscd = self.env['so.tscd'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_TSCD_ID = stscd.id
        return True

    # @api.multi
    # def action_bo_ghi_so(self):
        # self.bo_ghi_so()



    


    def lay_du_lieu_tinh_khau_hao(self,thang,nam):
        so_ngay = helper.Datetime.lay_so_ngay_trong_thang(nam, thang)
        ngay = str(helper.Datetime.lay_ngay_cuoi_thang(nam, thang))
        params = {
            'NGAY_HACH_TOAN' : ngay,
            'SO_NGAY_TRONG_THANG' : so_ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
            ngay_hach_toan              DATE := %(NGAY_HACH_TOAN)s;
            so_ngay_trong_thang         INTEGER := %(SO_NGAY_TRONG_THANG)s;
            chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;

            BEGIN
            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
                AS
                    SELECT
                        --SUMDiffDepreciationAmount ,
                        --                 Result.RefDetailID ,
                        --                 Result.RefID AS RefID ,
                        Result."TSCD_ID"
                        , Result."MA_TSCD"
                        , Result."TEN_TSCD"
                        , Result."DON_VI_SU_DUNG_ID"
                        , OU."MA_DON_VI"
                        , OU."TEN_DON_VI"
                        , --                 OU.OrganizationUnitName AS DepartmentName ,
                        /*Nếu là tháng cuối cùng thì dồn hết vào sửa bug 54502*/
                        CASE WHEN Result."THOI_GIAN_SU_DUNG_CON_LAI" - 1 <= 0
                                    /*HHSon 26.05.2016 - fix bug 102046: Trường hợp thời gian SD còn lại = 0 mà giá trị còn lại vẫn còn thì vẫn tính KH*/
                                    AND Result."LA_GHI_GIAM" =
                                        0 /* Sửa bug 61978 giá trị tính KH vào tháng cuối nhưng có ghi giảm tháng đó*/
                            THEN coalesce(ROUND(cast(Result."SO_TIEN_CON_LAI" AS NUMERIC), 2),
                                            0)
                        ELSE CASE WHEN Result."SO_TIEN_CON_LAI" <
                                        (CASE WHEN Result."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" =
                                                    TRUE -- khau hao theo luat dinh
                                            THEN coalesce(
                                                ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG_THEO_LUAT") AS NUMERIC), 2), 0)
                                        ELSE coalesce(ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG") AS NUMERIC), 2), 0)
                                        END)
                            THEN coalesce(ROUND(cast(Result."SO_TIEN_CON_LAI" AS NUMERIC), 2), 0)
                            ELSE (CASE WHEN Result."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = TRUE
                                THEN coalesce(ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG_THEO_LUAT") AS NUMERIC), 2), 0)
                                    ELSE coalesce(ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG") AS NUMERIC), 2), 0)
                                    END)
                            END
                        END           AS "GIA_TRI_TINH_KHAU_HAO_THANG"
                        , coalesce(ROUND(cast(Result."GIA_TRI_TINH_KHAU_HAO" AS NUMERIC), 2),
                                0)   AS "GIA_TRI_TINH_KHAU_HAO"
                        , --                 DepreciationAccount ,
                        coalesce(ROUND(CAST((Result."GIA_TRI_TINH_KH_THEO_LUAT") AS NUMERIC), 2),
                                0)   AS "GIA_TRI_TINH_KH_THEO_LUAT"
                        ,
                        --	 Nếu Giá trị tính KH còn lại theo luật của TSCĐ< Giá trị khấu hao 1 tháng theo luật của TSCĐ thì Giá trị tính vào chi phí hợp lý =Giá trị còn lại của TSCĐ
                        coalesce(
                            (CASE WHEN Result."SO_TIEN_CON_LAI" <
                                        (CASE WHEN Result."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = FALSE
                                            THEN Result."GIA_TRI_TINH_KHAU_HAO_THANG_THEO_LUAT"
                                        ELSE coalesce(
                                            ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG") AS NUMERIC),
                                                    2), 0)
                                        END)
                                THEN "SO_TIEN_CON_LAI"
                            --bug 47018
                            ELSE
                                /*Nếu là tháng cuối cùng thì dồn hết vào sửa bug 54502*/ CASE
                                                                                            WHEN
                                                                                                Result."THOI_GIAN_SU_DUNG_CON_LAI"
                                                                                                - 1 <= 0
                                                                                                /*HHSon 26.05.2016 - fix bug 102046: Trường hợp thời gian SD còn lại = 0 mà giá trị còn lại vẫn còn thì vẫn tính KH*/
                                                                                                AND Result."LA_GHI_GIAM" =
                                                                                                    0 /* Sửa bug 61978 giá trị tính KH vào tháng cuối nhưng có ghi giảm tháng đó*/
                                                                                                THEN CASE
                                                                                                    WHEN
                                                                                                        Result."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN"
                                                                                                        = TRUE
                                                                                                        THEN Result."GIA_TRI_TINH_KHAU_HAO_THANG"
                                                                                                    ELSE Result."SO_TIEN_CON_LAI"
                                                                                                    END
                                                                                            --THEN RemainingAmount
                                                                                            ELSE
                                                                                                -- CASE
                                                                                                --  WHEN MonthlyDepreciationAmount <= 0
                                                                                                --  THEN MonthlyDepreciationAmount2
                                                                                                --  ELSE MonthlyDepreciationAmount
                                                                                                --  END
                                                                                                Result."GIA_TRI_TINH_KHAU_HAO_THANG"
                                                                                            END
                            END), 0) AS "CHI_PHI_HOP_LY"
                        , 0             AS "CHI_PHI_KHONG_HOP_LY"
                        -- nmtruong 22/11/2016: CR19034: lấy lên mã loại TSCĐ và Cột có phải TSCĐ của NSNN hay không.
                        , Result."MA_LOAI_TSCD"
                        , Result."TEN_LOAI_TSCD"
                        , Result."LOAI_TSCD_ID"
                    -- 				,IsfixedAssetOfStateBudget
                    FROM (


                            SELECT
                                --         NEWID() AS RefDetailID ,
                                --         @RefID AS RefID ,
                                VF.id                                      AS "TSCD_ID"
                                , VF."MA_TAI_SAN"                            AS "MA_TSCD"
                                , VF."TEN_TAI_SAN"                           AS "TEN_TSCD"
                                , VF."GIA_TRI_TINH_KH_THEO_LUAT"
                                , VF."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN"
                                , VF."GIA_TRI_TINH_KHAU_HAO"
                                , FLED."DON_VI_SU_DUNG_ID"
                                , FLED."THOI_GIAN_SU_DUNG_CON_LAI"
                                , (CASE
                                    --Nếu tháng ghi giảm trùng với tháng tính khấu hao
                                    WHEN EXISTS(
                                        SELECT gg.id AS "CHI_TIET_ID"
                                        FROM asset_ghi_giam_tai_san ggct
                                            INNER JOIN asset_ghi_giam gg ON ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" = gg.id
                                        WHERE ggct."MA_TAI_SAN" = VF.id
                                            AND
                                            DATE_PART('month', gg."NGAY_HACH_TOAN" :: DATE) =
                                            DATE_PART('month', ngay_hach_toan :: DATE)
                                            AND
                                            DATE_PART('year', gg."NGAY_HACH_TOAN" :: DATE) =
                                            DATE_PART('year', ngay_hach_toan :: DATE)
                                    )
                                        THEN 1
                                    ELSE 0
                                    END)                                      AS "LA_GHI_GIAM"
                                , --Giá trị tính khấu hao tháng với trường hợp k giới hạn theo luật TNDN
                                (CASE
                                    --Nếu tháng ghi giảm trùng với tháng tính khấu hao
                                    --Nếu có ghi giảm trong tháng tính KH: thì tính theo công thức:

                                    WHEN EXISTS(SELECT gg.id AS "CHI_TIET_ID"
                                                FROM asset_ghi_giam_tai_san ggct
                                                    INNER JOIN asset_ghi_giam gg
                                                        ON ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" = gg.id
                                                WHERE ggct."MA_TAI_SAN" = VF.id
                                                    AND DATE_PART('month', gg."NGAY_HACH_TOAN" :: DATE) =
                                                        DATE_PART('month', ngay_hach_toan :: DATE)
                                                    AND DATE_PART('year', gg."NGAY_HACH_TOAN" :: DATE) =
                                                        DATE_PART('year', ngay_hach_toan :: DATE)
                                    )
                                        THEN
                                            ------Nếu TSCĐ không check "Giới hạn giá trị tính KH theo luật thuế TNDN
                                            (CASE WHEN VF."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = FALSE
                                                THEN (


                                                        CASE WHEN (
                                                                    SELECT gg."NGAY_HACH_TOAN"
                                                                    FROM asset_ghi_giam gg INNER JOIN
                                                                        asset_ghi_giam_tai_san ggct
                                                                            ON gg.id = ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" AND
                                                                                ggct."MA_TAI_SAN" = VF.id
                                                                ) IS NOT NULL AND
                                                                DATE_PART('month', ngay_hach_toan :: DATE) =
                                                                DATE_PART('month', (SELECT gg."NGAY_HACH_TOAN"
                                                                                    FROM asset_ghi_giam gg INNER JOIN
                                                                                        asset_ghi_giam_tai_san ggct
                                                                                            ON gg.id =
                                                                                                ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                AND
                                                                                                ggct."MA_TAI_SAN"
                                                                                                =
                                                                                                VF.id) :: DATE)
                                                                AND DATE_PART('year', ngay_hach_toan :: DATE) =
                                                                    DATE_PART('year', (SELECT gg."NGAY_HACH_TOAN"
                                                                                        FROM asset_ghi_giam gg INNER JOIN
                                                                                            asset_ghi_giam_tai_san ggct
                                                                                                ON gg.id =
                                                                                                    ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                    AND
                                                                                                    ggct."MA_TAI_SAN" =
                                                                                                    VF.id) :: DATE)

                                                            THEN (
                                                                CASE WHEN DATE_PART('month', (SELECT "NGAY_GHI_TANG"
                                                                                            FROM asset_ghi_tang gt
                                                                                            WHERE gt.id = VF.id) :: DATE) =
                                                                        DATE_PART('month', (SELECT gg."NGAY_HACH_TOAN"
                                                                                            FROM asset_ghi_giam gg INNER JOIN
                                                                                                asset_ghi_giam_tai_san ggct
                                                                                                    ON gg.id =
                                                                                                        ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                        AND
                                                                                                        ggct."MA_TAI_SAN" =
                                                                                                        VF.id) :: DATE)
                                                                        AND DATE_PART('year', (SELECT "NGAY_GHI_TANG"
                                                                                                FROM asset_ghi_tang gt
                                                                                                WHERE gt.id = VF.id) :: DATE)
                                                                            =
                                                                            DATE_PART('year', (SELECT gg."NGAY_HACH_TOAN"
                                                                                                FROM
                                                                                                    asset_ghi_giam gg INNER JOIN
                                                                                                    asset_ghi_giam_tai_san ggct
                                                                                                        ON gg.id =
                                                                                                            ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                            AND
                                                                                                            ggct."MA_TAI_SAN" =
                                                                                                            VF.id) :: DATE)
                                                                    THEN DATE_PART('day', (SELECT gg."NGAY_HACH_TOAN"
                                                                                            FROM
                                                                                                asset_ghi_giam gg INNER JOIN
                                                                                                asset_ghi_giam_tai_san ggct
                                                                                                    ON gg.id =
                                                                                                    ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                    AND
                                                                                                    ggct."MA_TAI_SAN" =
                                                                                                    VF.id) :: DATE) -
                                                                        DATE_PART('day', (SELECT "NGAY_GHI_TANG"
                                                                                            FROM asset_ghi_tang gt
                                                                                            WHERE gt.id = VF.id) :: DATE)
                                                                ELSE DATE_PART('day', (SELECT gg."NGAY_HACH_TOAN"
                                                                                        FROM asset_ghi_giam gg INNER JOIN
                                                                                            asset_ghi_giam_tai_san ggct
                                                                                                ON gg.id =
                                                                                                ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                AND
                                                                                                ggct."MA_TAI_SAN" =
                                                                                                VF.id) :: DATE) - 1
                                                                END
                                                            )
                                                        ELSE 0
                                                        END


                                                    )
                                                    --Số ngày ghi giảm/Số ngày trong tháng gi giảm* Tỷ lệ KH tháng
                                                    * coalesce(FLED."GIA_TRI_KHAU_HAO_THANG",
                                                                0)
                                                    / so_ngay_trong_thang
                                            ELSE
                                                --Nếu có tích TSCĐ không check "Giới hạn giá trị tính KH theo luật thuế TNDN
                                                (


                                                    CASE WHEN (
                                                                SELECT gg."NGAY_HACH_TOAN"
                                                                FROM asset_ghi_giam gg INNER JOIN asset_ghi_giam_tai_san ggct
                                                                        ON gg.id = ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" AND
                                                                            ggct."MA_TAI_SAN" = 36
                                                            ) IS NOT NULL AND DATE_PART('month', ngay_hach_toan :: DATE) =
                                                                                DATE_PART('month', (SELECT gg."NGAY_HACH_TOAN"
                                                                                                    FROM
                                                                                                        asset_ghi_giam gg INNER JOIN
                                                                                                        asset_ghi_giam_tai_san ggct
                                                                                                            ON gg.id =
                                                                                                                ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                                AND
                                                                                                                ggct."MA_TAI_SAN"
                                                                                                                =
                                                                                                                36) :: DATE)
                                                            AND DATE_PART('year', ngay_hach_toan :: DATE) =
                                                                DATE_PART('year', (SELECT gg."NGAY_HACH_TOAN"
                                                                                    FROM
                                                                                        asset_ghi_giam gg INNER JOIN
                                                                                        asset_ghi_giam_tai_san ggct
                                                                                            ON gg.id =
                                                                                                ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                AND
                                                                                                ggct."MA_TAI_SAN" =
                                                                                                36) :: DATE)

                                                        THEN (
                                                            CASE WHEN DATE_PART('month', (SELECT "NGAY_GHI_TANG"
                                                                                        FROM asset_ghi_tang gt
                                                                                        WHERE gt.id = 36) :: DATE) =
                                                                    DATE_PART('month', (SELECT gg."NGAY_HACH_TOAN"
                                                                                        FROM
                                                                                            asset_ghi_giam gg INNER JOIN
                                                                                            asset_ghi_giam_tai_san ggct
                                                                                                ON gg.id =
                                                                                                    ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                    AND
                                                                                                    ggct."MA_TAI_SAN" =
                                                                                                    36) :: DATE)
                                                                    AND DATE_PART('year', (SELECT "NGAY_GHI_TANG"
                                                                                            FROM asset_ghi_tang gt
                                                                                            WHERE gt.id = 36) :: DATE) =
                                                                        DATE_PART('year', (SELECT gg."NGAY_HACH_TOAN"
                                                                                            FROM asset_ghi_giam gg INNER JOIN
                                                                                                asset_ghi_giam_tai_san ggct
                                                                                                    ON gg.id =
                                                                                                        ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                        AND
                                                                                                        ggct."MA_TAI_SAN" =
                                                                                                        36) :: DATE)
                                                                THEN DATE_PART('day', (SELECT gg."NGAY_HACH_TOAN"
                                                                                        FROM asset_ghi_giam gg INNER JOIN
                                                                                            asset_ghi_giam_tai_san ggct
                                                                                                ON gg.id =
                                                                                                ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                AND
                                                                                                ggct."MA_TAI_SAN" =
                                                                                                36) :: DATE) -
                                                                    DATE_PART('day', (SELECT "NGAY_GHI_TANG"
                                                                                        FROM asset_ghi_tang gt
                                                                                        WHERE gt.id = 36) :: DATE)
                                                            ELSE DATE_PART('day', (SELECT gg."NGAY_HACH_TOAN"
                                                                                    FROM asset_ghi_giam gg INNER JOIN
                                                                                        asset_ghi_giam_tai_san ggct
                                                                                            ON gg.id =
                                                                                            ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                            AND
                                                                                            ggct."MA_TAI_SAN" = 36) :: DATE)
                                                                - 1
                                                            END
                                                        )
                                                    ELSE 0
                                                    END


                                                )
                                                * coalesce(FLED."GIA_TRI_KH_THANG_THEO_LUAT",
                                                            0)
                                                / so_ngay_trong_thang
                                            END)


                                    --Nếu ngày tính khấu hao không phải là đầu tháng
                                    -- Nếu tháng tính khấu hao trùng với tháng ghi tăng và ngày tính khấu hao không phải là đầu tháng:
                                    WHEN DATE_PART('DAY', VF."NGAY_BAT_DAU_TINH_KH" :: DATE) <> 1
                                        AND DATE_PART('month', ngay_hach_toan :: DATE) =
                                            DATE_PART('month', VF."NGAY_BAT_DAU_TINH_KH" :: DATE)
                                        AND
                                        DATE_PART('year', ngay_hach_toan :: DATE) =
                                        DATE_PART('year', VF."NGAY_BAT_DAU_TINH_KH" :: DATE)
                                        THEN DATE_PART('day', VF."NGAY_BAT_DAU_TINH_KH" :: TIMESTAMP +
                                                      CAST(-1 * EXTRACT(DAY FROM VF."NGAY_BAT_DAU_TINH_KH" :: TIMESTAMP) ||
                                                           'day' AS INTERVAL) + INTERVAL '1 day' +
                                                      INTERVAL '1 month' - VF."NGAY_BAT_DAU_TINH_KH" :: TIMESTAMP)
                                        /*nếu có chứng từ chuyển ts thành chủ sh trong tháng đầut tính KH  thì lấy trên chứng từ chuyển ts thành chủ sh*/
                                        * coalesce(CASE WHEN VF."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = FALSE
                                        THEN FLED."GIA_TRI_KHAU_HAO_THANG"
                                                    ELSE FLED."GIA_TRI_KH_THANG_THEO_LUAT" -- gia tri khau hao theo luat dinh
                                                    END, 0)
                                        / so_ngay_trong_thang

                                    --Nếu là tháng cuối cùng
                                    --Nếu là tháng khấu hao cuối cùng: kiểm tra bằng cách tính xem giá trị còn lại của TSCD có nhỏ hơn GT khấu hao tháng hay không
                                    WHEN (SELECT coalesce((SELECT *
                                                        FROM LAY_SO_TIEN_KHAU_HAO(VF.id, ngay_hach_toan)),
                                                        0) AS "SO_TIEN_KHAU_HAO")
                                        -- gia tri khau hao con lai
                                        - coalesce(CASE WHEN VF."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" =
                                                            FALSE -- neu co gioi han gia tri khau hao
                                        THEN CASE
                                            WHEN FLED."CHENH_LECH_GIA_TRI_TINH_KHAU_HAO" <> 0
                                                OR FLED."CHENH_LECH_GIA_TRI_CON_LAI" <> 0
                                                /*nhyen - 29/6/2018 (Bug 237246): nếu có chênh lệch thời gian thì cũng rơi vào trường hợp này*/
                                                OR FLED."CHENH_LECH_THOI_GIAN_SU_DUNG" <> 0
                                                THEN FLED."GIA_TRI_KHAU_HAO_THANG" -- fled - fixed asset ledger
                                            ELSE VF."GIA_TRI_TINH_KHAU_HAO_THANG" -- vf - fixed asset
                                            END
                                                    ELSE FLED."GIA_TRI_KH_THANG_THEO_LUAT"
                                                    END, 0) < 0
                                        THEN (SELECT coalesce((SELECT *
                                                            FROM LAY_SO_TIEN_KHAU_HAO(VF.id, ngay_hach_toan)),
                                                            0) AS "SO_TIEN_KHAU_HAO")


                                    ELSE (

                                        CASE WHEN EXISTS(
                                            SELECT sts.id AS "ID_SO_TSCD"
                                            FROM
                                                so_tscd_chi_tiet sts
                                            WHERE
                                                sts."TSCD_ID" = VF.id
                                                AND (sts."LOAI_CHUNG_TU" IN ('252', '256')) -- bo qua thang nay
                                                AND sts."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                AND sts."CHI_NHANH_ID" = chi_nhanh_id
                                            ORDER BY sts."NGAY_HACH_TOAN" DESC,
                                                -- nmtruong 16/9/2016: sửa lỗi 114668: sắp xếp theo reforder nếu có chứng từ đánh giá lại hoặc thuê tài chính. Chứng từ nào ghi sổ sau thì lấy lên
                                                sts.id DESC
                                            FETCH FIRST 1 ROW ONLY

                                        )
                                            THEN (SELECT (CASE
                                                        WHEN VF."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = FALSE
                                                            THEN sts."GIA_TRI_KHAU_HAO_THANG"
                                                        ELSE sts."GIA_TRI_KH_THANG_THEO_LUAT"
                                                        END)
                                                FROM so_tscd_chi_tiet sts
                                                WHERE sts."TSCD_ID" = VF.id
                                                        AND (sts."LOAI_CHUNG_TU" IN ('252', '256')) -- bo qua thang nay
                                                        AND sts."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                        AND sts."CHI_NHANH_ID" = chi_nhanh_id
                                                ORDER BY sts."NGAY_HACH_TOAN" DESC,
                                                    -- nmtruong 16/9/2016: sửa lỗi 114668: sắp xếp theo reforder nếu có chứng từ đánh giá lại hoặc thuê tài chính. Chứng từ nào ghi sổ sau thì lấy lên
                                                    sts.id DESC
                                                FETCH FIRST 1 ROW ONLY
                                            )
                                        ELSE --ngược lại lấy trên danh mục ts
                                            -- 				□ Nếu ko có thì lấy theo giá trị thông thường
                                            (CASE WHEN VF."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = FALSE
                                                THEN (coalesce(VF."GIA_TRI_TINH_KHAU_HAO_THANG",
                                                            0))
                                            ELSE (coalesce(VF."GIA_TRI_KH_THANG_THEO_LUAT",
                                                            0))
                                            END)
                                        END

                                    )
                                    END)                                      AS "GIA_TRI_TINH_KHAU_HAO_THANG"
                                , --Giá trị tính khấu hao tháng chỗ này tách riêng ra để cho TH tính KH cho ts theo luật

                                (CASE
                                    --Nếu có ghi giảm trong tháng tính KH
                                    WHEN EXISTS(
                                        SELECT gg.id
                                        FROM asset_ghi_giam_tai_san ggct
                                            INNER JOIN asset_ghi_giam gg ON ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" = gg.id
                                        WHERE ggct."MA_TAI_SAN" = VF.id
                                            AND
                                            DATE_PART('month', gg."NGAY_HACH_TOAN" :: DATE) =
                                            DATE_PART('month', ngay_hach_toan :: DATE)
                                            AND
                                            DATE_PART('year', gg."NGAY_HACH_TOAN" :: DATE) =
                                            DATE_PART('year', ngay_hach_toan :: DATE)
                                        --Số ngày từ đầu tháng đến ngày ghi giảm* Tỷ lệ KH tháng/Số ngày trong tháng ghi giảm
                                    )
                                        THEN (

                                                CASE WHEN (
                                                            SELECT gg."NGAY_HACH_TOAN"
                                                            FROM asset_ghi_giam gg INNER JOIN asset_ghi_giam_tai_san ggct
                                                                    ON gg.id = ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" AND
                                                                        ggct."MA_TAI_SAN" = VF.id
                                                        ) IS NOT NULL AND DATE_PART('month', ngay_hach_toan :: DATE) =
                                                                            DATE_PART('month', (SELECT gg."NGAY_HACH_TOAN"
                                                                                                FROM
                                                                                                    asset_ghi_giam gg INNER JOIN
                                                                                                    asset_ghi_giam_tai_san ggct
                                                                                                        ON gg.id =
                                                                                                            ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                            AND
                                                                                                            ggct."MA_TAI_SAN"
                                                                                                            =
                                                                                                            VF.id) :: DATE)
                                                        AND DATE_PART('year', ngay_hach_toan :: DATE) =
                                                            DATE_PART('year', (SELECT gg."NGAY_HACH_TOAN"
                                                                                FROM
                                                                                    asset_ghi_giam gg INNER JOIN
                                                                                    asset_ghi_giam_tai_san ggct
                                                                                        ON gg.id =
                                                                                            ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                            AND
                                                                                            ggct."MA_TAI_SAN" = VF.id) :: DATE)

                                                    THEN (
                                                        CASE WHEN DATE_PART('month', (SELECT "NGAY_GHI_TANG"
                                                                                    FROM asset_ghi_tang gt
                                                                                    WHERE gt.id = VF.id) :: DATE) =
                                                                DATE_PART('month', (SELECT gg."NGAY_HACH_TOAN"
                                                                                    FROM
                                                                                        asset_ghi_giam gg INNER JOIN
                                                                                        asset_ghi_giam_tai_san ggct
                                                                                            ON gg.id =
                                                                                                ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                AND
                                                                                                ggct."MA_TAI_SAN" =
                                                                                                VF.id) :: DATE)
                                                                AND DATE_PART('year', (SELECT "NGAY_GHI_TANG"
                                                                                        FROM asset_ghi_tang gt
                                                                                        WHERE gt.id = VF.id) :: DATE) =
                                                                    DATE_PART('year', (SELECT gg."NGAY_HACH_TOAN"
                                                                                        FROM asset_ghi_giam gg INNER JOIN
                                                                                            asset_ghi_giam_tai_san ggct
                                                                                                ON gg.id =
                                                                                                    ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                                    AND
                                                                                                    ggct."MA_TAI_SAN" =
                                                                                                    VF.id) :: DATE)
                                                            THEN DATE_PART('day', (SELECT gg."NGAY_HACH_TOAN"
                                                                                    FROM asset_ghi_giam gg INNER JOIN
                                                                                        asset_ghi_giam_tai_san ggct
                                                                                            ON gg.id =
                                                                                            ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                            AND
                                                                                            ggct."MA_TAI_SAN" =
                                                                                            VF.id) :: DATE) -
                                                                DATE_PART('day', (SELECT "NGAY_GHI_TANG"
                                                                                    FROM asset_ghi_tang gt
                                                                                    WHERE gt.id = VF.id) :: DATE)
                                                        ELSE DATE_PART('day', (SELECT gg."NGAY_HACH_TOAN"
                                                                                FROM asset_ghi_giam gg INNER JOIN
                                                                                    asset_ghi_giam_tai_san ggct
                                                                                        ON gg.id =
                                                                                        ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                                                                                        AND
                                                                                        ggct."MA_TAI_SAN" = VF.id) :: DATE) -
                                                            1
                                                        END
                                                    )
                                                ELSE 0
                                                END

                                            )
                                            * coalesce(FLED."GIA_TRI_KHAU_HAO_THANG",
                                                        0) / so_ngay_trong_thang
                                    --Nếu ngày tính khấu hao không phải là đầu tháng
                                    WHEN DATE_PART('DAY', VF."NGAY_BAT_DAU_TINH_KH" :: DATE) <> 1
                                        AND DATE_PART('month', ngay_hach_toan :: DATE) =
                                            DATE_PART('month', VF."NGAY_BAT_DAU_TINH_KH" :: DATE)
                                        AND
                                        DATE_PART('year', ngay_hach_toan :: DATE) =
                                        DATE_PART('year', VF."NGAY_BAT_DAU_TINH_KH" :: DATE)
                                        THEN (DATE_PART('DAY', ((((VF."NGAY_BAT_DAU_TINH_KH" +
                                                                (-1 * DATE_PART('DAY', VF."NGAY_BAT_DAU_TINH_KH" :: DATE)) *
                                                                INTERVAL '1 day') + INTERVAL '1 day') + INTERVAL '1 month') +
                                                                INTERVAL '1 day') :: DATE) -
                                            DATE_PART('DAY', VF."NGAY_BAT_DAU_TINH_KH" :: DATE))
                                            /*nếu có chứng từ chuyển ts thành chủ sh trong tháng đầut tính KH  thì lấy trên chứng từ chuyển ts thành chủ sh*/
                                            * coalesce(FLED."GIA_TRI_KHAU_HAO_THANG",
                                                        0) / so_ngay_trong_thang
                                    --Nếu là tháng khấu hao cuối cùng
                                    WHEN ((SELECT coalesce((SELECT *
                                                            FROM LAY_SO_TIEN_KHAU_HAO(VF.id, ngay_hach_toan)),
                                                        0) AS "SO_TIEN_KHAU_HAO")
                                        -- gia tri khau hao con lai
                                        - (CASE WHEN FLED."CHENH_LECH_GIA_TRI_TINH_KHAU_HAO" <> 0
                                                    OR FLED."CHENH_LECH_GIA_TRI_CON_LAI" <> 0
                                                    /*nhyen - 29/6/2018 (Bug 237246): nếu có chênh lệch thời gian thì cũng rơi vào trường hợp này*/
                                                    OR FLED."CHENH_LECH_THOI_GIAN_SU_DUNG" <> 0
                                        THEN coalesce(FLED."GIA_TRI_KHAU_HAO_THANG", 0)
                                            ELSE coalesce(VF."GIA_TRI_TINH_KHAU_HAO_THANG", 0)
                                            END)) < 0
                                        THEN (SELECT coalesce((SELECT *
                                                            FROM LAY_SO_TIEN_KHAU_HAO(VF.id, ngay_hach_toan)),
                                                            0) AS "SO_TIEN_KHAU_HAO")

                                    ELSE (


                                        (CASE WHEN EXISTS(
                                            SELECT sts.id AS "ID_SO_TSCD"
                                            FROM
                                                so_tscd_chi_tiet sts
                                            WHERE
                                                sts."TSCD_ID" = VF.id
                                                AND (sts."LOAI_CHUNG_TU" IN ('252', '256'))
                                                AND sts."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                AND sts."CHI_NHANH_ID" = chi_nhanh_id
                                            ORDER BY sts."NGAY_HACH_TOAN" DESC,
                                                -- nmtruong 16/9/2016: sửa lỗi 114668: sắp xếp theo reforder nếu có chứng từ đánh giá lại hoặc thuê tài chính. Chứng từ nào ghi sổ sau thì lấy lên
                                                sts.id DESC
                                            FETCH FIRST 1 ROW ONLY
                                        )
                                            THEN (
                                                SELECT sts."GIA_TRI_KH_THANG_THEO_LUAT"
                                                FROM so_tscd_chi_tiet sts
                                                WHERE sts."TSCD_ID" = VF.id
                                                    AND (sts."LOAI_CHUNG_TU" IN ('252', '256')) -- bo qua thang nay
                                                    AND sts."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                    AND sts."CHI_NHANH_ID" = chi_nhanh_id
                                                ORDER BY sts."NGAY_HACH_TOAN" DESC,
                                                    -- nmtruong 16/9/2016: sửa lỗi 114668: sắp xếp theo reforder nếu có chứng từ đánh giá lại hoặc thuê tài chính. Chứng từ nào ghi sổ sau thì lấy lên
                                                    sts.id DESC
                                                FETCH FIRST 1 ROW ONLY
                                            )
                                        ELSE --ngược lại lấy trên danh mục ts
                                            coalesce(VF."GIA_TRI_TINH_KHAU_HAO_THANG",
                                                    0)
                                        END)


                                    )
                                    END)                                      AS "GIA_TRI_TINH_KHAU_HAO_THANG_THEO_LUAT"
                                , --Giá trị tính khấu hao TSCĐ của TSCĐ:
                                --Đối với TSCĐ chưa có đánh giá lại thì lấy giá trị tính khấu hao khi khai báo TSCĐ
                                --Đối với TSCĐ đã có đánh giá lại, Giá trị tính khấu hao = giá trị tính khấu hao khi khai báo +/- chênh lệch giá trị tính khấu hao trên các chứng từ đánh giá lại

                                (CASE WHEN EXISTS(SELECT sts.id AS "ID_SO_TSCD"
                                                    FROM so_tscd_chi_tiet sts
                                                    WHERE sts."TSCD_ID" = VF.id
                                                        AND sts."LOAI_CHUNG_TU" = '252'
                                                        AND sts."LOAI_CHUNG_TU" <> '251'
                                                        AND sts."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                        AND sts."CHI_NHANH_ID" = chi_nhanh_id
                                                    ORDER BY sts."NGAY_HACH_TOAN" DESC
                                                    FETCH FIRST 1 ROW ONLY
                                )
                                    THEN coalesce(
                                                (SELECT SUM(dglct."CHENH_LECH_GTKH")
                                                FROM asset_danh_gia_lai_chi_tiet_dieu_chinh dglct
                                                    INNER JOIN asset_danh_gia_lai dgl
                                                        ON dgl.id = dglct."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID"
                                                WHERE dgl."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                    AND dgl."CHI_NHANH_ID" = chi_nhanh_id
                                                    AND dglct."MA_TAI_SAN_ID" = VF.id
                                                ), 0)
                                            + coalesce(VF."GIA_TRI_TINH_KHAU_HAO", 0)
                                    ELSE (coalesce(VF."GIA_TRI_TINH_KHAU_HAO", 0)
                                    )
                                    END)                                      AS "SO_TIEN_KHAU_HAO"
                                , (SELECT coalesce((SELECT *
                                                    FROM LAY_SO_TIEN_KHAU_HAO(VF.id, ngay_hach_toan)),
                                                    0) AS "SO_TIEN_KHAU_HAO") AS "SO_TIEN_CON_LAI"
                                , FAC."MA"                                   AS "MA_LOAI_TSCD"
                                , FAC."TEN"                                  AS "TEN_LOAI_TSCD"
                                , FAC.id                                     AS "LOAI_TSCD_ID"

                            FROM asset_ghi_tang AS VF
                                INNER JOIN danh_muc_to_chuc DV ON VF."DON_VI_SU_DUNG_ID" = DV.id
                                INNER JOIN (
                                                SELECT DISTINCT id AS "TSCD_ID"
                                                FROM asset_ghi_tang
                                                --RemTamj by hoant
                                                WHERE "NGAY_GHI_TANG" <= ngay_hach_toan
                                                    AND "LOAI_CHUNG_TU" <> '251'
                                            ) AS TEMP ON VF.id = TEMP."TSCD_ID"
                                -- Chỉ tính khấu hao cho những TSCĐ có thời gian sử dụng > 0
                                LEFT JOIN danh_muc_loai_tai_san_co_dinh FAC ON FAC.id = VF."LOAI_TAI_SAN_ID"
                                INNER JOIN LATERAL (
                                            SELECT
                                                FL."CHENH_LECH_GIA_TRI_TINH_KHAU_HAO"
                                                , FL."CHENH_LECH_GIA_TRI_CON_LAI"
                                                , FL."CHENH_LECH_THOI_GIAN_SU_DUNG"
                                                , /*nhyen - 29/6/2018 (Bug 237246):Lấy thêm thông tin thời gian chênh lệnh*/
                                                FL."GIA_TRI_KHAU_HAO_THANG"
                                                , FL."GIA_TRI_KH_THANG_THEO_LUAT"
                                                , FL."DON_VI_SU_DUNG_ID"
                                                , FL."THOI_GIAN_SU_DUNG_CON_LAI"
                                            FROM so_tscd_chi_tiet FL
                                            WHERE
                                                FL."TSCD_ID" = VF.id AND
                                                FL."NGAY_HACH_TOAN" <= ngay_hach_toan
                                                AND FL."CHI_NHANH_ID" = chi_nhanh_id
                                            ORDER BY "NGAY_HACH_TOAN" DESC
                                            FETCH FIRST 1 ROW ONLY
                                            ) FLED ON TRUE

                            WHERE VF."KHONG_TINH_KHAU_HAO" = FALSE--Không lấy các ts không tính KH
                                --Chỉ lấy các tài sản còn khấu hao
                                --hhson
                                AND (SELECT coalesce((SELECT *
                                                        FROM LAY_SO_TIEN_KHAU_HAO(VF.id, ngay_hach_toan)),
                                                        0) AS "SO_TIEN_KHAU_HAO") > 0
                                ----Không lấy ts đã ghi giảm, chỉ lấy các tài sản ghi giảm trong tháng đó
                                AND VF.id NOT IN (
                                SELECT ggct."MA_TAI_SAN"
                                FROM asset_ghi_giam_tai_san ggct
                                    INNER JOIN asset_ghi_giam gg ON ggct."TAI_SAN_CO_DINH_GHI_GIAM_ID" = gg.id
                                WHERE ((DATE_PART('month', gg."NGAY_HACH_TOAN" :: DATE) <>
                                        DATE_PART('month', ngay_hach_toan :: DATE)
                                        OR DATE_PART('year', gg."NGAY_HACH_TOAN" :: DATE) <>
                                            DATE_PART('year', ngay_hach_toan :: DATE)
                                        )
                                        AND gg."NGAY_HACH_TOAN" < ngay_hach_toan
                                    )
                                    AND (gg."CHI_NHANH_ID" = chi_nhanh_id)
                            )
                                ----                          --Ngày bắt đầu sử dụng
                                AND (VF."NGAY_BAT_DAU_TINH_KH" <= ngay_hach_toan
                                        OR VF."NGAY_BAT_DAU_TINH_KH" IS NULL
                                )
                                AND (VF."CHI_NHANH_ID" = chi_nhanh_id
                                        OR (chi_nhanh_id IS NULL
                                        )
                                )
                        ) AS Result

                        LEFT JOIN danh_muc_to_chuc AS OU ON Result."DON_VI_SU_DUNG_ID" = OU.id

                    WHERE (CASE WHEN Result."THOI_GIAN_SU_DUNG_CON_LAI" - 1 <=
                                    0 /*HHSon 26.05.2016 - fix bug 102046: Trường hợp thời gian SD còn lại = 0 mà giá trị còn lại vẫn còn thì vẫn tính KH*/
                        THEN coalesce(ROUND(cast(Result."SO_TIEN_CON_LAI" AS NUMERIC), 2),
                                    0)
                        ELSE CASE WHEN Result."SO_TIEN_CON_LAI" < (CASE
                                                                    WHEN Result."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" =
                                                                        TRUE
                                                                        THEN coalesce(ROUND(CAST(
                                                                                                (Result."GIA_TRI_TINH_KHAU_HAO_THANG_THEO_LUAT")
                                                                                                AS NUMERIC), 2), 0)
                                                                    ELSE coalesce(ROUND(
                                                                                        CAST(
                                                                                            (Result."GIA_TRI_TINH_KHAU_HAO_THANG")
                                                                                            AS
                                                                                            NUMERIC), 2), 0)
                                                                    END)
                            THEN coalesce(ROUND(cast(Result."SO_TIEN_CON_LAI" AS NUMERIC), 2), 0)
                                ELSE (CASE WHEN Result."GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN" = TRUE
                                    THEN coalesce(ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG_THEO_LUAT") AS NUMERIC), 2),
                                                0)
                                    ELSE coalesce(ROUND(CAST((Result."GIA_TRI_TINH_KHAU_HAO_THANG") AS NUMERIC), 2), 0)
                                    END)
                                END
                        END) <> 0
                    ORDER BY Result."MA_TSCD"
            ;

        END $$
        ;

            SELECT *
            FROM TMP_KET_QUA;



        """ 
        
        return self.execute(query, params)


    
    def lay_du_lieu_phan_bo(self,thang,nam):

        ngay = str(helper.Datetime.lay_ngay_cuoi_thang(nam, thang))
        params = {
            'NGAY_HACH_TOAN' : ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
            ngay_hach_toan              DATE := %(NGAY_HACH_TOAN)s;
            chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;

            BEGIN
            DROP TABLE IF EXISTS TMP_KET_QUA;
            CREATE TEMP TABLE TMP_KET_QUA
                AS
                SELECT
                    "TSCD_ID",
                    "TEN_TSCD",
                    "DON_VI_SU_DUNG_ID",
                    FA1."DOI_TUONG_PHAN_BO_ID",
                    V."TEN_DOI_TUONG",
                    "TY_LE_PB",
                    "TK_NO_ID",
                    "TK_KHAU_HAO_ID",
                    "KHOAN_MUC_CP_ID",
                    "MA_THONG_KE_ID" /*nhyen_12/7/2017_CR91640*/
                FROM (

                        SELECT
                        FAA."TAI_SAN_CO_DINH_GHI_TANG_ID" AS "TSCD_ID",
                        FI."TK_KHAU_HAO_ID",
                        FI."TEN_TAI_SAN"                           AS "TEN_TSCD",
                        FI."DON_VI_SU_DUNG_ID",
                        CASE
                        WHEN (SELECT COUNT(*)
                                FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                WHERE TMp."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id
                                ) <= 1
                                AND (SELECT COUNT(*) /*và là phòng ban */
                                    FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                    WHERE TMp."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id
                                        AND TMP."LOAI_DOI_TUONG" = '4'
                                    ) = 1
                            THEN
                            (CASE WHEN EXISTS(SELECT dcct."MA_TAI_SAN_ID"
                                                FROM
                                                asset_dieu_chuyen_chi_tiet dcct
                                                INNER JOIN asset_dieu_chuyen dc
                                                    ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                                WHERE dc."NGAY" < ngay_hach_toan AND
                                                    dcct."MA_TAI_SAN_ID" = FI.id
                                                ORDER BY dc."NGAY" DESC
                                                FETCH FIRST 1 ROW ONLY
                            )
                                THEN (SELECT concat('danh.muc.to.chuc,', cast(dcct."DEN_DON_VI_ID" AS VARCHAR(50)))
                                    FROM asset_dieu_chuyen_chi_tiet dcct
                                        INNER JOIN asset_dieu_chuyen dc ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                    WHERE dc."NGAY" < ngay_hach_toan AND
                                            dcct."MA_TAI_SAN_ID" = FI.id
                                    ORDER BY dc."NGAY" DESC
                                    FETCH FIRST 1 ROW ONLY
                                )
                                --Nếu không thì lấy trong bảng ghi tăng
                                ELSE FAA."DOI_TUONG_PHAN_BO_ID"
                                END)
                        ELSE FAA."DOI_TUONG_PHAN_BO_ID"
                        END                               AS "DOI_TUONG_PHAN_BO_ID",
                        FAA."TY_LE_PB",
                        CASE WHEN (SELECT COUNT(*)
                                    FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                    WHERE TMp."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id
                                    ) <= 1
                            THEN (
                            --Nếu có điều chỉnh thì lấy điều chỉnh
                            CASE WHEN EXISTS(SELECT dcct."MA_TAI_SAN_ID"
                                                FROM
                                                asset_dieu_chuyen_chi_tiet dcct
                                                INNER JOIN asset_dieu_chuyen dc ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                                WHERE dc."NGAY" < ngay_hach_toan AND
                                                    dcct."MA_TAI_SAN_ID" = FI.id
                                                ORDER BY dc."NGAY" DESC
                                                FETCH FIRST 1 ROW ONLY
                            )
                                THEN (SELECT coalesce(dcct."TK_NO_ID", -1)
                                    FROM asset_dieu_chuyen_chi_tiet dcct
                                        INNER JOIN asset_dieu_chuyen dc ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                    WHERE dc."NGAY" < ngay_hach_toan AND
                                            dcct."MA_TAI_SAN_ID" = FI.id
                                    ORDER BY dc."NGAY"
                                    FETCH FIRST 1 ROW ONLY
                                )
                            --Nếu không thì lấy trong bảng ghi tăng
                            ELSE coalesce(FAA."TK_NO_ID", -1)
                            END)
                        ELSE --Nếu không thì lấy trên danh mục
                            FAA."TK_NO_ID"
                        END                               AS "TK_NO_ID",
                        CASE WHEN (SELECT COUNT(*)
                                    FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                    WHERE TMp."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id
                                    ) <= 1
                                    AND (SELECT COUNT(*) /*và là phòng ban */
                                        FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                        WHERE TMp."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id
                                                AND TMP."LOAI_DOI_TUONG" = '4'
                                        ) = 1
                            THEN
                            --Nếu có điều chuyển thì lấy điều chuyển
                            (CASE WHEN EXISTS(SELECT dcct."MA_TAI_SAN_ID"
                                                FROM asset_dieu_chuyen_chi_tiet dcct
                                                INNER JOIN asset_dieu_chuyen dc
                                                    ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                                WHERE dc."NGAY" < ngay_hach_toan AND
                                                    dcct."MA_TAI_SAN_ID" = FI.id
                                                ORDER BY dc."NGAY" DESC
                                                FETCH FIRST 1 ROW ONLY
                            )
                                THEN (SELECT dcct."KHOAN_MUC_CP_ID"
                                    FROM asset_dieu_chuyen_chi_tiet dcct
                                        INNER JOIN asset_dieu_chuyen dc ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                    WHERE dc."NGAY" < ngay_hach_toan AND
                                            dcct."MA_TAI_SAN_ID" = FI.id
                                    ORDER BY dc."NGAY" DESC
                                    FETCH FIRST 1 ROW ONLY
                                )
                                --Nếu không thì lấy trong bảng ghi tăng
                                ELSE FAA."KHOAN_MUC_CP_ID"
                                END)
                        ELSE FAA."KHOAN_MUC_CP_ID"
                        END                               AS "KHOAN_MUC_CP_ID",
                        CASE WHEN (SELECT COUNT(*)
                                    FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                    WHERE TMP."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id) <= 1
                                    AND (SELECT COUNT(*)
                                        FROM asset_ghi_tang_thiet_lap_phan_bo AS TMP
                                        WHERE TMP."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id AND TMP."LOAI_DOI_TUONG" = '4') = 1
                            THEN --Nếu có điều chuyển thì lấy điều chuyển
                            (CASE WHEN EXISTS(SELECT *
                                                FROM asset_dieu_chuyen_chi_tiet dcct INNER JOIN asset_dieu_chuyen dc
                                                    ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                                WHERE dcct."MA_TAI_SAN_ID" = FI.id)
                                THEN (SELECT dcct."MA_THONG_KE_ID"
                                    FROM asset_dieu_chuyen_chi_tiet dcct
                                        INNER JOIN asset_dieu_chuyen dc ON dcct."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID" = dc.id
                                    WHERE dc."NGAY" < ngay_hach_toan AND
                                            dcct."MA_TAI_SAN_ID" = FI.id
                                    ORDER BY dc."NGAY" DESC
                                    FETCH FIRST 1 ROW ONLY
                                )
                                --Nếu không thì lấy trong bảng ghi tăng
                                ELSE FAA."MA_THONG_KE_ID"
                                END)
                        ELSE FAA."MA_THONG_KE_ID"
                        END                               AS "MA_THONG_KE_ID"


                        --Nếu thiết lập phân bổ <= 1 dòng thì kiểm tra xem điều chỉnh : lấy tài khoản chi phí
                        FROM asset_ghi_tang_thiet_lap_phan_bo AS FAA
                        INNER JOIN asset_ghi_tang AS FI ON FAA."TAI_SAN_CO_DINH_GHI_TANG_ID" = FI.id
                        WHERE
                        FI."CHI_NHANH_ID" = chi_nhanh_id

                    ) AS FA1

                    LEFT JOIN (

                                SELECT
                                id                                   AS "DOI_TUONG_ID",
                                'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL",
                                "MA_DOI_TUONG_THCP"                  AS "MA_DOI_TUONG",
                                "TEN_DOI_TUONG_THCP"                 AS "TEN_DOI_TUONG",
                                CAST(0 AS INT)                       AS "LOAI_DOI_TUONG",
                                N'Đối tượng THCP'                   AS "TEN_LOAI_DOI_TUONG",
                                --             BranchID AS BranchID ,
                                --             Inactive ,
                                CAST(FALSE AS BOOLEAN)               AS IsParent,
                                CAST('0' AS VARCHAR)                 AS "CAP_TO_CHUC",
                                "MA_PHAN_CAP"
                                FROM danh_muc_doi_tuong_tap_hop_chi_phi dtcp
                                WHERE id NOT IN (SELECT DISTINCT parent_id
                                                FROM danh_muc_doi_tuong_tap_hop_chi_phi
                                                WHERE parent_id IS NOT NULL)

                                UNION ALL
                                SELECT
                                id                     AS "DOI_TUONG_ID",
                                'danh.muc.cong.trinh'  AS "MODEL",
                                "MA_CONG_TRINH"        AS "MA_DOI_TUONG",
                                "TEN_CONG_TRINH"       AS "TEN_DOI_TUONG",
                                CAST(1 AS INT)         AS "LOAI_DOI_TUONG",
                                N'Công trình'         AS "TEN_LOAI_DOI_TUONG",
                                --             dbo.ProjectWork.BranchID AS BranchID ,
                                --             Inactive ,
                                CAST(FALSE AS BOOLEAN) AS IsParent,
                                CAST('0' AS VARCHAR)   AS "CAP_TO_CHUC",
                                "MA_PHAN_CAP"
                                FROM danh_muc_cong_trinh
                                WHERE id NOT IN (SELECT DISTINCT parent_id
                                                FROM danh_muc_cong_trinh
                                                WHERE parent_id IS NOT NULL)

                                UNION ALL
                                SELECT
                                OU.id              AS "DOI_TUONG_ID",
                                'danh.muc.to.chuc' AS "MODEL",
                                OU."MA_DON_VI"     AS "MA_DOI_TUONG",
                                OU."TEN_DON_VI"    AS "TEN_DOI_TUONG",
                                CAST(4 AS INT)     AS "LOAI_DOI_TUONG",
                                N'Đơn vị'         AS "TEN_LOAI_DOI_TUONG",
                                --             OU.BranchID AS BranchID ,
                                --             OU.Inactive ,
                                OU."ISPARENT",
                                OU."CAP_TO_CHUC",
                                "MA_PHAN_CAP"
                                FROM danh_muc_to_chuc OU
                                WHERE "CAP_TO_CHUC" IN ('3', '4', '5', '6')

                            ) AS V ON FA1."DOI_TUONG_PHAN_BO_ID" LIKE concat('%%,', V."DOI_TUONG_ID")
                                        AND FA1."DOI_TUONG_PHAN_BO_ID" LIKE concat(V."MODEL", ',%%')
                WHERE V."LOAI_DOI_TUONG" NOTNULL /* tránh lỗi TH xóa đối tượng phân bổ*/
            ;

            END $$;

            SELECT *
            FROM TMP_KET_QUA;


        """  
        
        return self.execute(query, params)


    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			CREATE OR REPLACE FUNCTION LAY_SO_TIEN_KHAU_HAO(IN tscd_id INTEGER, ngay_hach_toan DATE)
            RETURNS SETOF FLOAT AS $$
            DECLARE

            BEGIN
            DROP TABLE IF EXISTS TMP_QUERY_1;
            CREATE TEMP TABLE TMP_QUERY_1
            AS (
                SELECT (SELECT coalesce((SELECT coalesce(gt."GIA_TRI_TINH_KHAU_HAO", 0)
                                        FROM asset_ghi_tang gt
                                        WHERE gt.id = tscd_id
                                        ), 0)
                            + coalesce((SELECT SUM(dglct."CHENH_LECH_GTKH")
                                        FROM asset_danh_gia_lai_chi_tiet_dieu_chinh dglct
                                            INNER JOIN asset_danh_gia_lai dgl
                                            ON dglct."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID" = dgl.id
                                        WHERE dglct."MA_TAI_SAN_ID" = tscd_id
                                                AND dgl."NGAY_HACH_TOAN" <= ngay_hach_toan
                                        ), 0))
                    -
                    (SELECT coalesce(SUM(khct."GIA_TRI_KH_THANG"), 0)
                        FROM asset_tinh_khau_hao_chi_tiet khct
                        INNER JOIN asset_tinh_khau_hao kh ON khct."TINH_KHAU_HAO_ID" = kh.id
                        WHERE khct."MA_TAI_SAN_ID" = tscd_id
                            AND kh."NGAY_HACH_TOAN" < ngay_hach_toan)
                    -
                    (SELECT coalesce(gt."HAO_MON_LUY_KE", 0)
                        FROM asset_ghi_tang gt
                        WHERE gt.id = tscd_id)
                    -

                    coalesce((
                                SELECT coalesce(SUM(dglct."CHENH_LECH_HAO_MON_LUY_KE"), 0)
                                FROM asset_danh_gia_lai_chi_tiet_dieu_chinh dglct
                                    INNER JOIN asset_danh_gia_lai dgl ON dglct."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID" = dgl.id
                                WHERE dglct."MA_TAI_SAN_ID" = tscd_id
                                        AND dgl."NGAY_HACH_TOAN" <= ngay_hach_toan
                                ), 0) AS "SO_TIEN_KHAU_HAO"
            );

            RETURN QUERY( SELECT cast("SO_TIEN_KHAU_HAO" AS FLOAT) FROM TMP_QUERY_1);

            --   RETURN QUERY (
            --   );
            END;

            $$ LANGUAGE PLpgSQL;
		""")