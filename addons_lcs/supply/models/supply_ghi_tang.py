# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from datetime import datetime
from odoo.exceptions import ValidationError
import json

class SUPPLY_GHI_TANG(models.Model):
    _name = 'supply.ghi.tang'
    _description = 'Công cụ dụng cụ'
    _inherit = ['mail.thread']
    _order = "NGAY_GHI_TANG desc, SO_CT_GHI_TANG desc"


    SO_CCDC_ID = fields.Many2one('so.ccdc', ondelete='set null')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái', readonly=True, default='chua_ghi_so')
    SO_CT_GHI_TANG = fields.Char(string='Số CT ghi tăng(*)', help='Số chứng từ ghi tăng', auto_num='supply_ghi_tang_SO_CT_GHI_TANG')
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng(*)', help='Ngày ghi tăng',default=fields.Datetime.now)
    MA_CCDC = fields.Char(string='Mã CCDC(*)', help='Mã công cụ dụng cụ')

    TEN_CCDC = fields.Char(string='Tên CCDC(*)', help='Tên công cụ dụng cụ')
    name = fields.Char(string='name', help='name', related='MA_CCDC',store=True)
    LOAI_CCDC_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu',string='Loại CCDC', help='Loại công cụ dụng cụ')
    NHOM_CCDC = fields.Char(string='Nhóm CCDC', help='Nhóm công cụ dụng cụ')
    LY_DO_GHI_TANG = fields.Char(string='Lý do ghi tăng', help='Lý do ghi tăng')
    DON_VI_TINH = fields.Char(string='Đơn vị tính', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng',default=1, digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA')) #Mạnh sửa bug2039 
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits= decimal_precision.get_precision('VND'))
    SO_KY_PHAN_BO = fields.Float(string='Số kỳ phân bổ(*)', help='Số kỳ phân bổ',digits= decimal_precision.get_precision('VND'),default=1)
    SO_TIEN_PHAN_BO_HANG_KY = fields.Float(string='Số tiền PB hàng kỳ', help='Số tiền phân bổ hàng kỳ',digits= decimal_precision.get_precision('VND'),default=1)
    TK_CHO_PHAN_BO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chờ phân bổ', help='Tài khoản chờ phân bổ')
    NGUNG_PHAN_BO = fields.Boolean(string='Ngừng phân bổ', help='Ngừng phân bổ')
    CHI_NHANH = fields.Many2one('res.company', string='Chi nhánh', help='Chi nhánh')
    # GHI_TANG_CCDC_HANG_LOAT_ID = fields.Many2one('supply.ghi.tang.hang.loat', string='Ghi tăng ccdc hàng loạt', help='Ghi tăng ccdc hàng loạt')
    SO_KY_PB_CON_LAI = fields.Integer(string='Số kỳ pb còn lại', help='Số kỳ pb còn lại')
    GIA_TRI_DA_PHAN_BO = fields.Float(string='Giá trị đã phân bổ', help='Giá trị đã phân bổ', digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại', digits=decimal_precision.get_precision('VND'))
    KHAI_BAO_DAU_KY = fields.Boolean(string='khai báo đầu kỳ', help='khai báo đầu kỳ', default=False)

    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu',compute='thaydoidvsd')

    SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS = fields.One2many('supply.ghi.tang.don.vi.su.dung', 'GHI_TANG_DON_VI_SU_DUNG_ID', string='Ghi tăng đơn vị sử dụng')
    SUPPLY_GHI_TANG_NGUON_GOC_HINH_THANH_IDS = fields.One2many('supply.ghi.tang.nguon.goc.hinh.thanh', 'GHI_TANG_NGUON_GOC_HINH_THANH_ID', string='Ghi tăng nguồn gốc hình thành')
    SUPPLY_GHI_TANG_MO_TA_CHI_TIET_IDS = fields.One2many('supply.ghi.tang.mo.ta.chi.tiet', 'GHI_TANG_MO_TA_CHI_TIET_ID', string='Ghi tăng mô tả chi tiết')
    SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS = fields.One2many('supply.ghi.tang.thiet.lap.phan.bo', 'GHI_TANG_THIET_LAP_PHAN_BO_ID', string='Ghi tăng thiết lập phân bổ')

    # Thêm trường Loại chứng từ
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ',default = 450)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    GIA_TRI_PHAN_BO = fields.Float(string='giá trị phân bổ', help='giá trị phân bổ', default=0)
    GIA_TRI_PHAN_BO_CON_LAI = fields.Float(string='Giá trị phân bổ còn lại', help='Giá trị phân bổ còn lại', compute='_compute_tinh_gia_tri_con_lai', store=True)
    

    CHON_CHUNG_TU_NGUON_GOC_JSON = fields.Text(store=False)


    @api.onchange('CHON_CHUNG_TU_NGUON_GOC_JSON')
    def _onchange_CHON_CHUNG_TU_NGUON_GOC_JSON(self):
        if self.CHON_CHUNG_TU_NGUON_GOC_JSON:
            chon_chung_tu = json.loads(self.CHON_CHUNG_TU_NGUON_GOC_JSON).get('ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS', [])
            self.SUPPLY_GHI_TANG_NGUON_GOC_HINH_THANH_IDS = []
            env = self.env['supply.ghi.tang.nguon.goc.hinh.thanh']
            for chung_tu in chon_chung_tu:
                new_line = env.new({
                        'NGAY_CHUNG_TU': chung_tu.get('NGAY_CHUNG_TU'),
                        'SO_CHUNG_TU': chung_tu.get('SO_CHUNG_TU'),
                        'DIEN_GIAI': chung_tu.get('DIEN_GIAI'),
                        'TK_NO_ID': chung_tu.get('TK_NO_ID'),
                        'TK_CO_ID': chung_tu.get('TK_CO_ID'),
                        'SO_TIEN': chung_tu.get('SO_TIEN'),
                        'ID_GOC': chung_tu.get('ID_GOC'),
                        'MODEL_GOC': chung_tu.get('MODEL_GOC'),
                })
                self.SUPPLY_GHI_TANG_NGUON_GOC_HINH_THANH_IDS += new_line
    
    
    @api.multi
    @api.depends('THANH_TIEN','GIA_TRI_PHAN_BO')
    def _compute_tinh_gia_tri_con_lai(self):
        for record in self:
            record.GIA_TRI_PHAN_BO_CON_LAI = record.THANH_TIEN - record.GIA_TRI_PHAN_BO
    
    
    @api.model
    def uivalidate(self, option=None):
        if not self.SO_LUONG:
            raise ValidationError('Số lượng phải lớn hơn 0.')
        if not self.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
            raise ValidationError('Bạn chưa chọn đơn vị sử dụng.')
        so_luong_con_lai = self.SO_LUONG
        for line in self.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
            so_luong_con_lai -= line.SO_LUONG
        if so_luong_con_lai:
            raise ValidationError('Số lượng phải bằng tổng số lượng ở các đơn vị sử dụng.')

    @api.model
    def default_get(self,default_fields):
        res = super(SUPPLY_GHI_TANG, self).default_get(default_fields)
        res['TK_CHO_PHAN_BO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=','242')],limit=1).id
        return res


    @api.onchange('DON_GIA')
    def thaydoidongia(self):
        self.THANH_TIEN = self.DON_GIA *self.SO_LUONG

    @api.onchange('SO_LUONG')
    def thaydoisl(self):
        self.THANH_TIEN = self.DON_GIA *self.SO_LUONG

    @api.onchange('THANH_TIEN')
    def thaydoithanhtien(self):
        if self.THANH_TIEN==0 :
            self.SO_TIEN_PHAN_BO_HANG_KY = 0
        else:
            self.SO_TIEN_PHAN_BO_HANG_KY = self.THANH_TIEN /self.SO_KY_PHAN_BO
        self.DON_GIA = self.THANH_TIEN / self.SO_LUONG

    @api.onchange('SO_KY_PHAN_BO')
    def thaydoisoky(self):
        if self.THANH_TIEN==0 :
            self.SO_TIEN_PHAN_BO_HANG_KY = 0
        else:
            self.SO_TIEN_PHAN_BO_HANG_KY = self.THANH_TIEN /self.SO_KY_PHAN_BO

        if self.KHAI_BAO_DAU_KY == False:
            self.SO_KY_PB_CON_LAI = self.SO_KY_PHAN_BO


    @api.depends('SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS')
    def thaydoidvsd(self):
        for record in self:
            env = record.env['supply.ghi.tang.thiet.lap.phan.bo']
            record.SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS = []
            # sl = self.SO_LUONG
            tl_pb = 0
            tong_ty_le = 0
            i = 0
            if record.SO_LUONG ==0:
                raise ValidationError("Số lượng phải khác 0. Xin vui lòng kiểm tra lại!")
            
            count = len(record.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS)
            for dvsd in record.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
                if dvsd.MA_DON_VI_ID:
                    doi_tuong_reference = 'danh.muc.to.chuc,' + str(dvsd.MA_DON_VI_ID.id) 
                    tong_ty_le += tl_pb                   
                    tl_pb = (dvsd.SO_LUONG / record.SO_LUONG)*100
                    i += 1
                    if count == 1:
                        tl_pb = 100
                    elif i == count:
                        tl_pb = 100 - tong_ty_le
                    
                    new_line = env.new({
                        'DOI_TUONG_PHAN_BO_ID': doi_tuong_reference,
                        'TEN_DOI_TUONG_PHAN_BO': dvsd.MA_DON_VI_ID.name,  
                        'TY_LE_PB' : tl_pb, 
                        'TK_NO_ID' : 8230,
                    })
                    record.SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS += new_line
            
    
    @api.model
    def create(self, values):
        ngay_vld = str(self.lay_ngay_dau_ky())
        if not values.get('KHAI_BAO_DAU_KY'):
            # if values.get('NGAY_GHI_TANG') < ngay_vld:
                # raise ValidationError("Chức năng Ghi tăng dùng để ghi tăng CCDC mới mua trong kỳ nên ngày ghi tăng phải lớn hơn ngày khóa sổ <" + ngay_vld+ '>. Nếu bạn muốn khai báo số dư đầu kỳ, vui lòng sử dụng chức năng Khai báo CCDC đầu kỳ')
            self.validate_unique('SO_CT_GHI_TANG', values.get('SO_CT_GHI_TANG'))
        result = super(SUPPLY_GHI_TANG, self).create(values)
        if result.KHAI_BAO_DAU_KY == True:
            result.action_ghi_so()
        return result

    @api.multi
    def write(self, values):
        self.validate_unique('SO_CT_GHI_TANG', values.get('SO_CT_GHI_TANG'), 'write')
        return super(SUPPLY_GHI_TANG, self).write(values)


    # @api.multi
    # def validate(self, vals, option=None):
        # tong_tl_pb = 0
        # tong_so_luong = 0
        # for line in vals.get('SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS'):
        #     tong_tl_pb += line[2].get('TY_LE_PB')
        # for line_dv in vals.get('SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS'):
        #     tong_so_luong += line_dv[2].get('SO_LUONG')
        # if tong_tl_pb != 100:
        #     raise ValidationError("Tổng tỷ lệ phân bổ phải bằng 100%. Xin vui lòng kiểm tra lại")
        # if tong_so_luong != vals.get('SO_LUONG'):
        #     raise ValidationError("Số lượng phải băng tổng số lượng ở các đơn vị sử dụng")
        
    
    # @api.multi
    # def write(self, values):
    #     ghi_so_dict = self.ghi_so()
    #     values.update(ghi_so_dict)
    #     return super(SUPPLY_GHI_TANG, self).write(values)

    # def ghi_so(self):
    #     ghi_so_dict = {'SO_CCDC_ID': self.ghi_so_ccdc()}
    #     return ghi_so_dict

    # def ghi_so_ccdc(self):
    #     # Bỏ ghi sổ trước
    #     if self.SO_CCDC_ID:
    #         self.SO_CCDC_ID.unlink()
    #     line_ids = []
    #     thu_tu = 0
    #     for line in self.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
    #         data = helper.Obj.inject(line, self)
    #         data.update({
    #             'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
    #             'SO_CHUNG_TU': self.SO_CT_GHI_TANG,
    #             'NGAY_CHUNG_TU': self.NGAY_GHI_TANG,
    #             'NGAY_HACH_TOAN': self.NGAY_GHI_TANG,
    #             'THU_TU_TRONG_CHUNG_TU': thu_tu,
    #             'DIEN_GIAI_CHUNG': self.LY_DO_GHI_TANG,
    #             'SO_KY_PHAN_BO_GHI_TANG': self.SO_KY_PHAN_BO,
    #             'SO_LUONG_GHI_TANG': line.SO_LUONG,
    #             'SO_TIEN_GHI_TANG': line.SO_LUONG * self.DON_GIA,
    #             'DOI_TUONG_PHAN_BO_ID': line.MA_DON_VI_ID.id,
    #             'CCDC_ID': self.id,
    #         })
    #         line_ids += [(0,0,data)]
    #         thu_tu += 1
    #     # Tạo master
    #     scc = self.env['so.ccdc'].create({
    #         'name': self.SO_CT_GHI_TANG,
    #         'line_ids': line_ids,
    #         })
    #     return scc.id

    @api.multi
    def action_ghi_so(self):
        for record in self:
            record.ghi_so_ccdc()
        self.write({'state':'da_ghi_so'})
    def ghi_so_ccdc(self):
        line_ids = []
        thu_tu = 0
        i = 0
        j = 0
        for line in self.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
            so_tien_phan_bo_dau_ky = 0
            so_ky_phan_bo_ghi_tang = 0
            so_ky_phan_bo_ghi_giam = 0
            if j == 0:
                so_ky_phan_bo_ghi_tang = self.SO_KY_PHAN_BO
            if self.KHAI_BAO_DAU_KY == True:
                if i == 0:
                    so_tien_phan_bo_dau_ky = self.GIA_TRI_DA_PHAN_BO
                    so_ky_phan_bo_ghi_giam = self.SO_KY_PHAN_BO - self.SO_KY_PB_CON_LAI
            elif self.SO_LUONG != 0:
                if self.SO_KY_PHAN_BO == 1:
                    so_tien_phan_bo_dau_ky = (line.SO_LUONG/self.SO_LUONG)*self.THANH_TIEN
            data_ghi_no = helper.Obj.inject(line, self)
            data_ghi_no.update({
                'ID_CHUNG_TU': self.id,'MODEL_CHUNG_TU' : self._name,'CHI_TIET_ID' : line.id,'CHI_TIET_MODEL' : line._name,
                'NGAY_CHUNG_TU': self.NGAY_GHI_TANG,
                'NGAY_HACH_TOAN': self.NGAY_GHI_TANG,
                'SO_KY_PHAN_BO_GHI_TANG' : so_ky_phan_bo_ghi_tang,
                'SO_LUONG_GHI_TANG' : line.SO_LUONG,
                'SO_TIEN_GHI_TANG' : line.SO_LUONG * self.DON_GIA,
                'DOI_TUONG_PHAN_BO_ID' : line.MA_DON_VI_ID.id,
                'CCDC_ID': self.id,
                'SO_CHUNG_TU' : self.SO_CT_GHI_TANG,
                'SO_TIEN_PHAN_BO' : so_tien_phan_bo_dau_ky,
                # 'SO_TIEN_PHAN_BO' : (line.SO_LUONG/self.SO_LUONG)*self.THANH_TIEN if self.SO_LUONG != 0 else 0,
                'SO_KY_PHAN_BO_GHI_GIAM' : so_ky_phan_bo_ghi_giam,
            })
            line_ids += [(0,0,data_ghi_no)]
            thu_tu += 1
            i += 1
            j += 1
        # Tạo master
        sc = self.env['so.ccdc'].create({
            # 'name': self.SO_CHUNG_TU,
            'line_ids': line_ids,
            })
        self.SO_CCDC_ID = sc.id
        return True
    # @api.multi
    # def action_bo_ghi_so(self):
        # self.SO_CCDC_ID.unlink()
        # self.write({'state':'chua_ghi_so'})


    def lay_ccdc_theo_ngay(self,ngay):
        params = {
            'NGAY':ngay, 
            'CCDC_ID':self.id, 
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
            ngay                     DATE := %(NGAY)s;
            ccdc_id INTEGER:= %(CCDC_ID)s;

            BEGIN
            DROP TABLE IF EXISTS TMP_KET_QUA;
            CREATE TEMP TABLE TMP_KET_QUA
                AS
                SELECT
                            T."CCDC_ID"
                            , T."MA_CCDC"
                            , T."TEN_CCDC"
                            , T."DOI_TUONG_PHAN_BO_ID"
                            , OU."MA_DON_VI"
                            , OU."TEN_DON_VI"
                            , OU.parent_id
                            , OU."ISPARENT"
                            , OU."active"
                            , COALESCE(T."SO_LUONG_GHI_TANG", 0) - COALESCE(T."SO_LUONG_GHI_GIAM", 0) AS "SO_LUONG"
                            FROM (

                                SELECT
                                    SL."CCDC_ID"
                                    , SL."MA_CCDC"
                                    , SL."TEN_CCDC"
                                    , SL."DOI_TUONG_PHAN_BO_ID"
                                    , SUM(SL."SO_LUONG_GHI_TANG") AS "SO_LUONG_GHI_TANG"
                                    , SUM(SL."SO_LUONG_GHI_GIAM") AS "SO_LUONG_GHI_GIAM"
                                FROM so_ccdc_chi_tiet AS SL
                                            WHERE   SL."CCDC_ID" = ccdc_id
                                            AND SL."NGAY_HACH_TOAN" <= ngay
                                GROUP BY SL."CCDC_ID",
                                    SL."MA_CCDC",
                                    SL."TEN_CCDC",
                                    SL."DOI_TUONG_PHAN_BO_ID"

                                ) AS T
                            LEFT JOIN danh_muc_to_chuc AS OU ON T."DOI_TUONG_PHAN_BO_ID" = OU.id
                            WHERE (COALESCE(T."SO_LUONG_GHI_TANG", 0) - COALESCE(T."SO_LUONG_GHI_GIAM", 0) > 0)
                            ORDER BY "MA_CCDC"
            ;

            END $$;

            SELECT *
            FROM TMP_KET_QUA;


        """  
        
        return self.execute(query, params)