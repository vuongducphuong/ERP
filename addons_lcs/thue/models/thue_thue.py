# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_THUE(models.Model):
    _name = 'thue.thue'
    _description = 'Thuế'
    _inherit = ['mail.thread']
    MAU_SO = fields.Char(string='Mẫu số', help='Mẫu số')
    TO_KHAI = fields.Char(string='Tờ khai', help='Tờ khai')
    LOAI_THUE = fields.Char(string='Loại thuế', help='Loại thuế')
    KY = fields.Char(string='Kỳ', help='Kỳ')
    TEN_NGUOI_NOP_THUE = fields.Char(string='Tên người nộp thuế', help='Tên người nộp thuế')
    TEN_DAI_LY_THUE = fields.Char(string='Tên đại lý thuế', help='Tên đại lý thuế')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    MA_SO_THUE_DAI_LY = fields.Char(string='Mã số thuế đại lý', help='Mã số thuế đại lý')
    TO_KHAI_LAN_DAU = fields.Boolean(string='Tờ khai lần đầu', help='Tờ khai lần đầu')
    GIA_HAN = fields.Boolean(string='Gia hạn', help='Gia hạn')
    DN_VUA_VA_NHO = fields.Boolean(string='Doanh nghiệp có quy mô vừa và nhỏ', help='Doanh nghiệp có quy mô vừa và nhỏ')
    DN_CO_CSSX_HACH_TOAN_PHU_THUOC = fields.Boolean(string='Doanh nghiệp có cơ sở sản xuất hạch toán phụ thuộc', help='Doanh nghiệp có cơ sở sản xuất hạch toán phụ thuộc')
    DN_THUOC_DOI_TUONG_KE_KHAI = fields.Boolean(string='Doanh nghiệp thuộc đối tượng kê khai thông tin giao dịch liên kết', help='Doanh nghiệp thuộc đối tượng kê khai thông tin giao dịch liên kết')

    BO_SUNG_LAN_THU = fields.Char(string='Bổ sung lần thứ', help='Bổ sung lần thứ')
    TRUONG_HOP_DUOC_GIA_HAN = fields.Char(string='Trường hợp được gia hạn', help='Trường hợp được gia hạn')
    NGHANH_NGHE_CO_TY_LE_DOANH_THU_CAO_NHAT = fields.Char(string='Nghành nghề có tỷ lệ doanh thu cao nhất', help='Nghành nghề có tỷ lệ doanh thu cao nhất')
    TY_LE_PHAN_TRAM = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ (%)', digits=decimal_precision.get_precision('VND'))
    TONG_DOANH_THU_HANG_HOA_DV_BAN_RA_CHIU_THUE_GTGT = fields.Float(string='Tổng doanh thu hàng hóa, dịch vụ bán ra chịu thuế GTGT', help='Tổng doanh thu hàng hóa, dịch vụ bán ra chịu thuế GTGT', digits=decimal_precision.get_precision('VND'))
    TONG_SO_THUE_GTGT_CUA_HANG_HOA_DV_BAN_RA = fields.Float(string='Tổng số thuế GTGT của hàng hóa, dịch vụ bán ra', help='Tổng số thuế GTGT của hàng hóa, dịch vụ bán ra', digits=decimal_precision.get_precision('VND'))
    
    SO_THUE_PHAI_NOP_CUA_NGUOI_NOP_THUE = fields.Float(string='Số thuế phải nộp của người nộp thuế', help='Số thuế phải nộp của người nộp thuế', digits=decimal_precision.get_precision('VND'))
    DOANH_THU_CHUA_CO_THUE_GTGT_CUA_SPSX_CUA_NNT = fields.Float(string='Doanh thu chưa có thuế GTGT của sản phẩm sản xuất ra của người nộp thuế', help='Doanh thu chưa có thuế GTGT của sản phẩm sản xuất ra của người nộp thuế', digits=decimal_precision.get_precision('VND'))
    SO_THUE_PHAI_NOP_CHO_DIA_PHUONG_NOI_CO_TRU_SO_CHINH = fields.Float(string='Số thuế phải nộp cho địa phương nơi có trụ sở chính', help='Số thuế phải nộp cho địa phương nơi có trụ sở chính', digits=decimal_precision.get_precision('VND'))
    SO_THUE_PHAI_NOP_CHO_DIA_PHUONG_NOI_CO_TRU_SO_CHINH_TH_0616 = fields.Float(string='Số thuế phải nộp cho địa phương nơi có trụ sở chính trong trường hợp [06] < [16]', help='Số thuế phải nộp cho địa phương nơi có trụ sở chính trong trường hợp [06] < [16]' , digits=decimal_precision.get_precision('VND'))

    DOI_TUONG_DUOC_GIA_HAN = fields.Boolean(string='Đối tượng được gia hạn', help='Đối tượng được gia hạn')
    GIA_HAN_NOP_THUE_THEO = fields.Selection([('DN_NHO_VUA', 'Doanh nghiệp có quy mô nhỏ và vừa'), ('DN_SU_DUNG_LAO_DONG', 'Doanh nghiệp sử dụng nhiều lao động'),('DN_DAU_TU_KINH_DOANH', 'Doanh nghiệp đầu tư - kinh doanh (bán, cho thuê, cho thuê mua) nhà ở'),('LY_DO_KHAC', 'Lý do khác'),], string='Trường hợp được gia hạn nộp thuế TNDN theo', help='Trường hợp được gia hạn nộp thuế TNDN theo', default='DN_NHO_VUA',required=True)
    THOI_HAN_DUOC_GIA_HAN = fields.Date(string='Thời hạn được gia hạn' , help='Thời hạn được gia hạn')
    SO_THUE_TNDN_DUOC_GIA_HAN = fields.Float(string='Số thuế TNDN được gia hạn' , help='Số thuế TNDN được gia hạn' , digits=decimal_precision.get_precision('VND'))
    SO_THUE_TNDN_KHONG_DUOC_GIA_HAN = fields.Float(string='Số thuế TNDN không được gia hạn' , help='Số thuế TNDN không được gia hạn' , digits=decimal_precision.get_precision('VND'))
    SO_NGAY_CHAM_NOP = fields.Float(string='Số ngày chậm nộp' , help='Số ngày chậm nộp' , digits=decimal_precision.get_precision('VND'))
    TU_NGAY = fields.Date(string='Từ ngày' , help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày' , help='Đến ngày')
    SO_TIEN_CHAM_NOP = fields.Float(string='Số tiền chậm nộp' , help='Số tiền chậm nộp' , digits=decimal_precision.get_precision('VND'))

    HO_VA_TEN = fields.Char(string='Họ và tên' , help='Họ và tên')
    NGUOI_KY = fields.Char(string='Người ký' , help='Người ký')
    CHUNG_CHI_HANH_NGHE_SO = fields.Char(string='Chứng chỉ hành nghề số' , help='Chứng chỉ hành nghề số')
    NGAY_KY = fields.Date(string='Ngày ký' , help='Ngày ký')


    TONG_GIA_TRI_HHDV_MUA_VAO_PV_SXKD_DUOC_KHAU_TRU_THUE_GTGT = fields.Float(string='Tổng giá trị HHDV mua vào phục vụ SXKD được khấu trừ thuế GTGT', help='Tổng giá trị HHDV mua vào phục vụ SXKD được khấu trừ thuế GTGT' , digits=decimal_precision.get_precision('VND'))
    TONG_THUE_GTGT_CUA_HHDV_MUA_VAO_DU_DK_KHAU_TRU = fields.Float(string='Tổng thuế GTGT của HHDV mua vào đủ điều kiện được khấu trừ', help='Tổng thuế GTGT của HHDV mua vào đủ điều kiện được khấu trừ' , digits=decimal_precision.get_precision('VND'))

    name = fields.Char(string='Name', help='Name', related='TO_KHAI', oldname='NAME')
    KHOAN_MUC_THUE = fields.Selection([('TT26', 'Tờ khai thuế GTGT khấu trừ (01/GTGT)'), ('TT119', 'Tờ khai thuế GTGT khấu trừ (01/GTGT)'),('THUE_GTGT_DU_AN_DAU_TU', 'Tờ khai thuế GTGT cho dự án đầu tư (02/GTGT)'),('THUE_GTGT_TRUC_TIEP_TREN_GTGT', 'Tờ khai thuế GTGT trực tiếp trên GTGT (03/GTGT)'),('QUYET_TOAN_THUE_TNDN', 'Quyết toán thuế TNDN năm (03/TNDN)'),('TIEU_THU_DAC_BIET', 'Tờ khai thuế tiêu thụ đặc biệt (01/TTĐB)'),('THUE_TAI_NGUYEN', 'Tờ khai thuế tài nguyên (01/TAIN)')  ], string='Khoản mục thuế', help='Khoản mục thuế')

    # THUE_TO_KHAI_TT26_CHI_TIET_IDS = fields.One2many('thue.to.khai.tt26.chi.tiet', 'CHI_TIET_ID', string='Tờ khai TT26 chi tiết')
    THUE_TO_KHAI_THUE_GTGT_TRUC_TIEP_TREN_GTGT_IDS = fields.One2many('thue.to.khai.thue.gtgt.truc.tiep.tren.gtgt', 'CHI_TIET_ID_1', string='Tờ khai thuế GTGT trực tiếp trên GTGT')
    THUE_TO_KHAI_QUYET_TOAN_THUE_TNDN_IDS = fields.One2many('thue.to.khai.quyet.toan.thue.tndn', 'CHI_TIET_ID_2', string='Tờ khai quyết toán thuế TNDN  ')
    # THUE_TO_KHAI_THUE_GTGT_DANH_CHO_DU_AN_DAU_TU_IDS = fields.One2many('thue.to.khai.thue.gtgt.danh.cho.du.an.dau.tu', 'CHI_TIET_ID_3', string='Tờ khai thuế GTGT dành cho dự án đầu tư')

    THUE_TAI_LIEU_KEM_THEO_IDS = fields.One2many('thue.tai.lieu.kem.theo', 'CHI_TIET_ID', string='Tài liệu kèm theo')

    THUE_PL_011_GTGT_IDS = fields.One2many('thue.pl.011.gtgt', 'CHI_TIET_ID', string='PL 011 GTGT')
    THUE_PL_012_GTGT_IDS = fields.One2many('thue.pl.012.gtgt', 'CHI_TIET_ID', string='PL 012 GTGT')
    THUE_PL_015_GTGT_IDS = fields.One2many('thue.pl.015.gtgt', 'CHI_TIET_ID', string='PL 015 GTGT')
    THUE_PL_016_GTGT_IDS = fields.One2many('thue.pl.016.gtgt', 'CHI_TIET_ID', string='PL 016 GTGT')
    THUE_PL_017_GTGT_IDS = fields.One2many('thue.pl.017.gtgt', 'CHI_TIET_ID', string='PL 017 GTGT')
    THUE_032A_TNDN_IDS = fields.One2many('thue.032a.tndn', 'CHI_TIET_ID', string='03-2A/TNDN')
    THUE_031A_TNDN_IDS = fields.One2many('thue.031a.tndn', 'CHI_TIET_ID', string='03-1A/TNDN')
    THUE_PL_BKBR_TTDB_IDS = fields.One2many('thue.pl.bkbr.ttdb', 'CHI_TIET_ID', string='PL-BKBR/TTĐB')


    # thêm các biến boolean để check trạng thái của các tab

    PL011_GTGT_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    PL012_GTGT_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    PL015_GTGT_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    PL016_GTGT_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    PL017_GTGT_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    THUE_032A_TNDN_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    THUE_031A_TNDN_BOLEAN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    THUE_PL_BKBR_TTDB = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    THUE_TO_KHAI_TRUC_TIEP_TREN_GTGT = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')
    THUE_TO_KHAI_THUE_TNDN = fields.Boolean(string='Tên nhãn', help='Tên nhãn',default='False')

    @api.model
    def default_get(self, fields):
        rec = super(THUE_THUE, self).default_get(fields)
        rec['THUE_TO_KHAI_QUYET_TOAN_THUE_TNDN_IDS'] = []
        rec['THUE_PL_011_GTGT_IDS'] = []
        rec['THUE_PL_012_GTGT_IDS'] = []
        rec['THUE_PL_015_GTGT_IDS'] = []
        rec['THUE_PL_016_GTGT_IDS'] = []
        rec['THUE_PL_017_GTGT_IDS'] = []
        rec['THUE_032A_TNDN_IDS'] = []
        rec['THUE_031A_TNDN_IDS'] = []
        rec['THUE_PL_BKBR_TTDB_IDS'] = []
        rec['THUE_TO_KHAI_THUE_GTGT_TRUC_TIEP_TREN_GTGT_IDS'] = []
        rec['THUE_TAI_LIEU_KEM_THEO_IDS'] = []
        to_khai_quyet_toan_thue_tndn_nam = []
        pl_011_gtgt = []
        pl_012_gtgt = []
        pl_015_gtgt = []
        pl_016_gtgt = []
        pl_017_gtgt = []
        thue_032a_tndn = []
        thue_031a_tndn = []
        thue_pl_bkbr_ttdb = []
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt = []
        thue_tai_lieu_kem_theo = []
        
        thue_tai_lieu_kem_theo +=[(0,0,{'STT':'1','TEN_TAI_LIEU':'',})]


        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'A','CHI_TIEU':'Kết quả kinh doanh ghi nhận theo báo cáo tài chính','MA_CHI_TIEU':'A',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1','CHI_TIEU':'Tổng lợi nhuận kế toán trước thuế thu nhập doanh nghiệp','MA_CHI_TIEU':'A1',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'B','CHI_TIEU':'Xác định thu nhập chịu thuế theo Luật thuế thu nhập doanh nghiệp','MA_CHI_TIEU':'B',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1','CHI_TIEU':'Điều chỉnh tăng tổng lợi nhuận trước thuế thu nhập doanh nghiệp (B1= B2+B3+B4+B5+B6+B7)','MA_CHI_TIEU':'B1',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1.1','CHI_TIEU':'Các khoản điều chỉnh tăng doanh thu','MA_CHI_TIEU':'B2',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1.2','CHI_TIEU':'Chi phí của phần doanh thu điều chỉnh giảm','MA_CHI_TIEU':'B3',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1.3','CHI_TIEU':'Các khoản chi không được trừ khi xác định thu nhập chịu thuế','MA_CHI_TIEU':'B4',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1.4','CHI_TIEU':'Thuế thu nhập đã nộp cho phần thu nhập nhận được ở nước ngoài','MA_CHI_TIEU':'B5',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1.5','CHI_TIEU':'Điều chỉnh tăng lợi nhuận do xác định giá thị trường đối với giao dịch liên kết','MA_CHI_TIEU':'B6',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1.6','CHI_TIEU':'Các khoản điều chỉnh làm tăng lợi nhuận trước thuế khác','MA_CHI_TIEU':'B7',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2','CHI_TIEU':'Điều chỉnh giảm tổng lợi nhuận trước thuế thu nhập doanh nghiệp (B8=B9+B10+B11) ','MA_CHI_TIEU':'B8',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2.1','CHI_TIEU':'Giảm trừ các khoản doanh thu đã tính thuế năm trước  ','MA_CHI_TIEU':'B9',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2.2','CHI_TIEU':'Chi phí của phần doanh thu điều chỉnh tăng ','MA_CHI_TIEU':'B10',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2.3','CHI_TIEU':'Các khoản điều chỉnh làm giảm lợi nhuận trước thuế khác','MA_CHI_TIEU':'B11',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3','CHI_TIEU':'Tổng thu nhập chịu thuế (B12=A1+B1-B8)','MA_CHI_TIEU':'B12',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3.1','CHI_TIEU':'Thu nhập chịu thuế từ hoạt động sản xuất kinh doanh','MA_CHI_TIEU':'B13',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3.2','CHI_TIEU':'Thu nhập chịu thuế từ hoạt động chuyển nhượng bất động sản (B14=B12-B13)','MA_CHI_TIEU':'B14',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'C','CHI_TIEU':'Xác định thuế thu nhập doanh nghiệp (TNDN) phải nộp từ hoạt động sản xuất kinh doanh','MA_CHI_TIEU':'',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1','CHI_TIEU':'Thu nhập chịu thuế (C1 = B13)','MA_CHI_TIEU':'C1',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2','CHI_TIEU':'Thu nhập miễn thuế','MA_CHI_TIEU':'C2',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3','CHI_TIEU':'Chuyển lỗ và bù trừ lãi, lỗ','MA_CHI_TIEU':'C3',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3.1','CHI_TIEU':'Lỗ từ hoạt động SXKD được chuyển trong kỳ','MA_CHI_TIEU':'C3a',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3.2','CHI_TIEU':'Lỗ từ chuyển nhượng BĐS được bù trừ với lãi của hoạt động SXKD','MA_CHI_TIEU':'C3b',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'4','CHI_TIEU':'Thu nhập tính thuế (TNTT) (C4=C1-C2-C3a-C3b)','MA_CHI_TIEU':'C4',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'5','CHI_TIEU':'Trích lập quỹ khoa học công nghệ (nếu có)','MA_CHI_TIEU':'C5',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'6','CHI_TIEU':'TNTT sau khi đã trích lập quỹ khoa học công nghệ (C6=C4-C5=C7+C8+C9)','MA_CHI_TIEU':'C6',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'6.1','CHI_TIEU':'Trong đó: + Thu nhập tính thuế tính theo thuế suất 22% (bao gồm cả thu nhập được áp dụng thuế suất ưu đãi)','MA_CHI_TIEU':'C7',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'6.2','CHI_TIEU':' + Thu nhập tính thuế tính theo thuế suất 20% (bao gồm cả thu nhập được áp dụng thuế suất ưu đãi)','MA_CHI_TIEU':'C8',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'6.3','CHI_TIEU':' + Thu nhập tính thuế tính theo thuế suất không ưu đãi khác','MA_CHI_TIEU':'C9',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'','CHI_TIEU':' + Thuế suất không ưu đãi khác','MA_CHI_TIEU':'C9a',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'7','CHI_TIEU':'Thuế TNDN từ hoạt động SXKD tính theo thuế suất không ưu đãi (C10 =(C7x22%)+(C8x20%)+(C9xC9a))','MA_CHI_TIEU':'C10',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'8','CHI_TIEU':'Thuế TNDN chênh lệch do áp dụng mức thuế suất ưu đãi','MA_CHI_TIEU':'C11',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'9','CHI_TIEU':'Thuế TNDN được miễn, giảm trong kỳ','MA_CHI_TIEU':'C12',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'9.1','CHI_TIEU':'Trong đó: + Số thuế TNDN được miễn, giảm theo Hiệp định','MA_CHI_TIEU':'C13',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'9.2','CHI_TIEU':'+ Số thuế được miễn, giảm không theo Luật Thuế TNDN','MA_CHI_TIEU':'C14',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'10','CHI_TIEU':'Số thuế thu nhập đã nộp ở nước ngoài được trừ trong kỳ tính thuế','MA_CHI_TIEU':'C15',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'11','CHI_TIEU':'Thuế TNDN của hoạt động sản xuất kinh doanh (C16=C10-C11-C12-C15)','MA_CHI_TIEU':'C16',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'D','CHI_TIEU':'Tổng số thuế TNDN phải nộp (D=D1+D2+D3)','MA_CHI_TIEU':'D',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1','CHI_TIEU':'Thuế TNDN của hoạt động sản xuất kinh doanh (D1=C16)','MA_CHI_TIEU':'D1',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2','CHI_TIEU':'Thuế TNDN từ hoạt động chuyển nhượng bất động sản','MA_CHI_TIEU':'D2',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3','CHI_TIEU':'Thuế TNDN phải nộp khác (nếu có)','MA_CHI_TIEU':'D3',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'E','CHI_TIEU':'Số thuế TNDN đã tạm nộp trong năm (E=E1+E2+E3)','MA_CHI_TIEU':'E',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1','CHI_TIEU':'Thuế TNDN của hoạt động sản xuất kinh doanh','MA_CHI_TIEU':'E1',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2','CHI_TIEU':'Thuế TNDN từ hoạt động chuyển nhượng bất động sản','MA_CHI_TIEU':'E2',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3','CHI_TIEU':'Thuế TNDN phải nộp khác (nếu có)','MA_CHI_TIEU':'E3',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'G','CHI_TIEU':'Tổng số thuế TNDN còn phải nộp (G=G1+G2+G3)','MA_CHI_TIEU':'G',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'1','CHI_TIEU':'Thuế TNDN của hoạt động sản xuất kinh doanh (G1=D1-E1)','MA_CHI_TIEU':'G1',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'2','CHI_TIEU':'Thuế TNDN từ hoạt động chuyển nhượng bất động sản (G2=D2-E2)','MA_CHI_TIEU':'G2',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'3','CHI_TIEU':'Thuế TNDN phải nộp khác (nếu có) (G3=D3-E3)','MA_CHI_TIEU':'G3',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'H','CHI_TIEU':'20% Thuế TNDN phải nộp (H=D*20%)','MA_CHI_TIEU':'H',})]
        to_khai_quyet_toan_thue_tndn_nam +=[(0,0,{'STT':'I','CHI_TIEU':'Chênh lệch giữa số thuế TNDN còn phải nộp với 20% số thuế TNDN phải nộp (I=G-H)','MA_CHI_TIEU':'I',})]

        

        pl_011_gtgt +=[(0,0,{'NHOM_HHDV':'1','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_MUA':'','MA_SO_THUE_NGUOI_MUA':'','DOANH_THU_CHUA_CO_THUE_GTGT':0,'THUE_GTGT':'','GHI_CHU':'',})]
        pl_011_gtgt +=[(0,0,{'NHOM_HHDV':'2','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_MUA':'','MA_SO_THUE_NGUOI_MUA':'','DOANH_THU_CHUA_CO_THUE_GTGT':0,'THUE_GTGT':'','GHI_CHU':'',})]
        pl_011_gtgt +=[(0,0,{'NHOM_HHDV':'3','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_MUA':'','MA_SO_THUE_NGUOI_MUA':'','DOANH_THU_CHUA_CO_THUE_GTGT':0,'THUE_GTGT':'','GHI_CHU':'',})]
        pl_011_gtgt +=[(0,0,{'NHOM_HHDV':'4','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_MUA':'','MA_SO_THUE_NGUOI_MUA':'','DOANH_THU_CHUA_CO_THUE_GTGT':0,'THUE_GTGT':'','GHI_CHU':'',})]

        pl_012_gtgt +=[(0,0,{'NHOM_HHDV':'1','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_BAN':'','MA_SO_THUE_NGUOI_BAN':'','GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE':'','THUE_GTGT':0,'GHI_CHU':'',})]
        pl_012_gtgt +=[(0,0,{'NHOM_HHDV':'2','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_BAN':'','MA_SO_THUE_NGUOI_BAN':'','GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE':'','THUE_GTGT':0,'GHI_CHU':'',})]
        pl_012_gtgt +=[(0,0,{'NHOM_HHDV':'3','STT':'1','SO_HOA_DON':'','NGAY_THANG_NAM_LAP_HOA_DON':'','TEN_NGUOI_BAN':'','MA_SO_THUE_NGUOI_BAN':'','GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE':'','THUE_GTGT':0,'GHI_CHU':'',})]
        
        
        pl_015_gtgt +=[(0,0,{'STT':'1','SO_CHUNG_TU_NOP_THUE':'','NGAY_NOP_THUE':'','NOI_NOP_THUE':'','CO_QUAN_THUE_CAP_CUC':'','CO_QUAN_THUE_QUAN_LY':'','SO_TIEN_THUE_DA_NOP':0,})]
        pl_016_gtgt +=[(0,0,{'STT':'1','TEN_CO_SO_SX_TRUC_THUOC':'','MA_SO_THUE':'','CO_QUAN_THUE_CAP_CUC':'','CO_QUAN_THUE_TRUC_TIEP_QUAN_LY':'','HANG_HOA_CHIU_THUE_5_PT':0,'HANG_HOA_CHIU_THUE_10_PT':0,'TONG':0,'SO_THUE_PHAI_NOP_CHO_DIA_PHUONG':0,'SO_THUE_PHAI_NOP_CHO_DIA_PHUONG_TH_O616':0,})]
        
        pl_017_gtgt +=[(0,0,{'STT':'1','TEN_CONG_TRINH':'','DOANH_THU':0,'CO_QUAN_THUE_CAP_CUC':'','CO_QUAN_THUE_QUAN_LY':'','TY_LE_PHAN_BO':0,'SO_THUE_GIA_TRI_GIA_TANG_PHAI_NOP':0,})]
        
        thue_032a_tndn +=[(0,0,{'STT':'1','NAM_PHAT_SINH_LO':'2014','SO_LO_PHAT_SINH':0,'SO_LO_DA_CHUYEN_TRONG_CAC_KY_TINH_THUE_TRUOC':0,'SO_LO_DUOC_CHUYEN_TRONG_KY_TINH_THUE_NAY':0,'SO_LO_CON_DUOC_CHUYEN_CHUYEN_SANG_KY_TINH_THUE_SAU':0,})]
        thue_032a_tndn +=[(0,0,{'STT':'2','NAM_PHAT_SINH_LO':'2015','SO_LO_PHAT_SINH':0,'SO_LO_DA_CHUYEN_TRONG_CAC_KY_TINH_THUE_TRUOC':0,'SO_LO_DUOC_CHUYEN_TRONG_KY_TINH_THUE_NAY':0,'SO_LO_CON_DUOC_CHUYEN_CHUYEN_SANG_KY_TINH_THUE_SAU':0,})]
        thue_032a_tndn +=[(0,0,{'STT':'3','NAM_PHAT_SINH_LO':'2016','SO_LO_PHAT_SINH':0,'SO_LO_DA_CHUYEN_TRONG_CAC_KY_TINH_THUE_TRUOC':0,'SO_LO_DUOC_CHUYEN_TRONG_KY_TINH_THUE_NAY':0,'SO_LO_CON_DUOC_CHUYEN_CHUYEN_SANG_KY_TINH_THUE_SAU':0,})]
        thue_032a_tndn +=[(0,0,{'STT':'4','NAM_PHAT_SINH_LO':'2017','SO_LO_PHAT_SINH':0,'SO_LO_DA_CHUYEN_TRONG_CAC_KY_TINH_THUE_TRUOC':0,'SO_LO_DUOC_CHUYEN_TRONG_KY_TINH_THUE_NAY':0,'SO_LO_CON_DUOC_CHUYEN_CHUYEN_SANG_KY_TINH_THUE_SAU':0,})]
        thue_032a_tndn +=[(0,0,{'STT':'5','NAM_PHAT_SINH_LO':'2018','SO_LO_PHAT_SINH':0,'SO_LO_DA_CHUYEN_TRONG_CAC_KY_TINH_THUE_TRUOC':0,'SO_LO_DUOC_CHUYEN_TRONG_KY_TINH_THUE_NAY':0,'SO_LO_CON_DUOC_CHUYEN_CHUYEN_SANG_KY_TINH_THUE_SAU':0,})]

        thue_031a_tndn +=[(0,0,{'STT':'','CHI_TIEU':'Kết  quả  kinh doanh ghi nhận theo báo cáo tài chính','MA_CHI_TIEU':'',})]
        thue_031a_tndn +=[(0,0,{'STT':'1','CHI_TIEU':'Doanh thu bán hàng và cung cấp dịch vụ','MA_CHI_TIEU':'[01]',})]
        thue_031a_tndn +=[(0,0,{'STT':'','CHI_TIEU':'Trong đó: - Doanh thu bán hàng hóa, dịch vụ xuất khẩu','MA_CHI_TIEU':'[02]',})]
        thue_031a_tndn +=[(0,0,{'STT':'2','CHI_TIEU':'Các khoản giảm trừ doanh thu ([03]=[04]+[05]+[06]+[07])','MA_CHI_TIEU':'[03]',})]
        thue_031a_tndn +=[(0,0,{'STT':'a','CHI_TIEU':'Chiết khấu thương mại','MA_CHI_TIEU':'[04]',})]
        thue_031a_tndn +=[(0,0,{'STT':'b','CHI_TIEU':'Giảm giá hàng bán','MA_CHI_TIEU':'[05]',})]
        thue_031a_tndn +=[(0,0,{'STT':'c','CHI_TIEU':'Giá trị hàng bán bị trả lại','MA_CHI_TIEU':'[06]',})]
        thue_031a_tndn +=[(0,0,{'STT':'d','CHI_TIEU':'Thuế tiêu thụ đặc biệt, thuế xuất khẩu, thuế giá trị gia tăng theo phương pháp trực tiếp phải nộp','MA_CHI_TIEU':'[07]',})]
        thue_031a_tndn +=[(0,0,{'STT':'3','CHI_TIEU':'Doanh thu hoạt động tài chính ','MA_CHI_TIEU':'[08]',})]
        thue_031a_tndn +=[(0,0,{'STT':'4','CHI_TIEU':'Chi phí sản xuất, kinh doanh hàng hóa, dịch vụ ([09]=[10]+[11]+[12])','MA_CHI_TIEU':'[09]',})]
        thue_031a_tndn +=[(0,0,{'STT':'a','CHI_TIEU':'Giá vốn hàng bán','MA_CHI_TIEU':'[10]',})]
        thue_031a_tndn +=[(0,0,{'STT':'b','CHI_TIEU':'Chi phí bán hàng','MA_CHI_TIEU':'[11]',})]
        thue_031a_tndn +=[(0,0,{'STT':'c','CHI_TIEU':'Chi phí quản lý doanh nghiệp','MA_CHI_TIEU':'[12]',})]
        thue_031a_tndn +=[(0,0,{'STT':'5','CHI_TIEU':'Chi phí tài chính','MA_CHI_TIEU':'[13]',})]
        thue_031a_tndn +=[(0,0,{'STT':'','CHI_TIEU':'Trong đó: Chi phí lãi tiền vay dùng cho sản xuất, kinh doanh','MA_CHI_TIEU':'[14]',})]
        thue_031a_tndn +=[(0,0,{'STT':'6','CHI_TIEU':'Lợi nhuận thuần từ hoạt động kinh doanh  ([15]=[01]-[03]+[08]-[09]-[13])','MA_CHI_TIEU':'[15]',})]
        thue_031a_tndn +=[(0,0,{'STT':'7','CHI_TIEU':'Thu nhập khác','MA_CHI_TIEU':'[16]',})]
        thue_031a_tndn +=[(0,0,{'STT':'8','CHI_TIEU':'Chi phí khác','MA_CHI_TIEU':'[17]',})]
        thue_031a_tndn +=[(0,0,{'STT':'9','CHI_TIEU':'Lợi nhuận khác ([18]=[16]-[17])','MA_CHI_TIEU':'[18]',})]
        thue_031a_tndn +=[(0,0,{'STT':'10','CHI_TIEU':'Tổng lợi nhuận kế toán trước thuế thu nhập doanh nghiệp ([19]=[15]+[18])','MA_CHI_TIEU':'[19]',})]

        thue_pl_bkbr_ttdb +=[(0,0,{'STT':'1','KY_HIEU_HOA_DON_BH':'','SO_HOA_DON_BAN_HANG':'','NGAY_THANG_NAM_PHAT_HANH':'','TEN_KHACH_HANG':'','TEN_HANG_HOA_DICH_VU':'','NHOM_HANG_HOA_DICH_VU':'','SO_LUONG':0,'DON_GIA':0,'DOANH_SO_BAN_CO_THUE':0,})]

        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'1','CHI_TIEU':'Giá trị gia tăng âm được kết chuyển kỳ trước','MA_CHI_TIEU':'[21]','GIA_TRI':0})]
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'2','CHI_TIEU':'Tổng doanh thu hàng hóa, dịch vụ bán ra','MA_CHI_TIEU':'[22]','GIA_TRI':0})]
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'3','CHI_TIEU':'Giá vốn của hàng hóa, dịch vụ mua vào','MA_CHI_TIEU':'[23]','GIA_TRI':301216})]
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'4','CHI_TIEU':'Điều chỉnh tăng giá trị gia tăng âm của các kỳ trước','MA_CHI_TIEU':'[24]','GIA_TRI':0})]
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'5','CHI_TIEU':'Điều chỉnh giảm giá trị gia tăng âm của các kỳ trước','MA_CHI_TIEU':'[25]','GIA_TRI':0})]
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'6','CHI_TIEU':'Giá trị gia tăng (GTGT) chịu thuế trong kỳ:[26] = [22] - [23] - [21] - [24] + [25];','MA_CHI_TIEU':'[26]','GIA_TRI':-301216})]
        thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt +=[(0,0,{'STT':'7','CHI_TIEU':'Thuế GTGT phải nộp: [27] = [26] x thuế suất thuế GTGT','MA_CHI_TIEU':'[27]','GIA_TRI':0})]


        rec['THUE_TO_KHAI_QUYET_TOAN_THUE_TNDN_IDS'] = to_khai_quyet_toan_thue_tndn_nam
        rec['THUE_PL_011_GTGT_IDS'] = pl_011_gtgt
        rec['THUE_PL_012_GTGT_IDS'] = pl_012_gtgt
        rec['THUE_PL_015_GTGT_IDS'] = pl_015_gtgt
        rec['THUE_PL_016_GTGT_IDS'] = pl_016_gtgt
        rec['THUE_PL_017_GTGT_IDS'] = pl_017_gtgt
        rec['THUE_032A_TNDN_IDS'] = thue_032a_tndn
        rec['THUE_031A_TNDN_IDS'] = thue_031a_tndn
        rec['THUE_PL_BKBR_TTDB_IDS'] = thue_pl_bkbr_ttdb
        rec['THUE_TO_KHAI_THUE_GTGT_TRUC_TIEP_TREN_GTGT_IDS'] = thue_to_khai_thue_gtgt_truc_tiep_tren_gtgt

        rec['THUE_TAI_LIEU_KEM_THEO_IDS'] = thue_tai_lieu_kem_theo

        rec['PL011_GTGT_BOLEAN'] = False
        rec['PL012_GTGT_BOLEAN'] = False
        rec['PL015_GTGT_BOLEAN'] = False
        rec['PL016_GTGT_BOLEAN'] = False
        rec['PL017_GTGT_BOLEAN'] = False
        rec['THUE_032A_TNDN_BOLEAN'] = False
        rec['THUE_031A_TNDN_BOLEAN'] = False
        rec['THUE_PL_BKBR_TTDB'] = False
        rec['THUE_TO_KHAI_TRUC_TIEP_TREN_GTGT'] = False
        rec['THUE_TO_KHAI_THUE_TNDN'] = False

        default_THUE_PHU_LUC_KE_KHAI_IDS = self.get_context('default_THUE_PHU_LUC_KE_KHAI_IDS')
        default_khoan_muc_thue = self.get_context('default_khoan_muc_thue')


        default_loai_to_khai = self.get_context('default_loai_to_khai')
        default_hang_muc_khai = self.get_context('default_hang_muc_khai')
        default_thang = self.get_context('default_thang')
        default_quy = self.get_context('default_quy')
        default_nam = self.get_context('default_nam')
        default_lan_khai_bo_sung = self.get_context('default_lan_khai_bo_sung')
        default_ngay = self.get_context('default_ngay')

        ky_tinh_thue = ''
        lan_khai = ''
        if default_loai_to_khai:
            if default_loai_to_khai=='TO_KHAI_THANG':
                ky_tinh_thue = 'Tháng ' + str(default_thang) + ' năm ' + str(default_nam)
            elif default_loai_to_khai=='TO_KHAI_QUY':
                ky_tinh_thue = 'Quý ' + str(default_quy) + ' năm ' + str(default_nam)
            elif default_loai_to_khai=='TO_KHAI_LAN_PHAT_SINH':
                ky_tinh_thue = 'Ngày ' + str(default_ngay) + ' tháng ' + str(default_thang) + ' năm ' + str(default_nam)
        if default_hang_muc_khai:
            if default_hang_muc_khai =='TO_KHAI_BO_SUNG':
                lan_khai =  str(default_lan_khai_bo_sung)
            elif default_hang_muc_khai =='TO_KHAI_LAN_DAU':
                rec['TO_KHAI_LAN_DAU'] = True
        rec['KY'] = ky_tinh_thue
        rec['BO_SUNG_LAN_THU'] = lan_khai
 
        #  lấy thông tin của context truyền sang để thực hiện ẩn hiện tờ khai
        if default_khoan_muc_thue:
            if default_khoan_muc_thue == 'THUE_GTGT_TRUC_TIEP_TREN_GTGT':
                rec['THUE_TO_KHAI_TRUC_TIEP_TREN_GTGT'] = True
                rec['MAU_SO'] = '03/GTGT'
                rec['TO_KHAI'] = 'Tờ khai thuế GTGT trực tiếp trên GTGT'
                rec['LOAI_THUE'] = 'GTGT'
            elif default_khoan_muc_thue == 'QUYET_TOAN_THUE_TNDN':
                rec['THUE_TO_KHAI_THUE_TNDN'] = True
                rec['MAU_SO'] = '03/TNDN'
                rec['TO_KHAI'] = 'Quyết toán thuế TNDN năm'
                rec['LOAI_THUE'] = 'TNDN'
            elif default_khoan_muc_thue == 'TT26':
                rec['MAU_SO'] = '01/GTGT'
                rec['TO_KHAI'] = 'TT26 - Tờ khai thuế GTGT khấu trừ (01/GTGT)'
                rec['LOAI_THUE'] = 'GTGT'
            elif default_khoan_muc_thue == 'TT119':
                rec['MAU_SO'] = '01/GTGT'
                rec['TO_KHAI'] = 'TT119 - Tờ khai thuế GTGT khấu trừ (01/GTGT)'
                rec['LOAI_THUE'] = 'GTGT'
            elif default_khoan_muc_thue == 'THUE_GTGT_DU_AN_DAU_TU':
                rec['MAU_SO'] = '02/GTGT'
                rec['TO_KHAI'] = 'Tờ khai thuế GTGT cho dự án đầu tư'
                rec['LOAI_THUE'] = 'GTGT'
            elif default_khoan_muc_thue == 'TIEU_THU_DAC_BIET':
                rec['MAU_SO'] = '01/TTĐB'
                rec['TO_KHAI'] = 'Tờ khai thuế tiêu thụ đặc biệt'
                rec['LOAI_THUE'] = 'TTĐB'
            elif default_khoan_muc_thue == 'THUE_TAI_NGUYEN':
                rec['MAU_SO'] = '01/TAIN'
                rec['TO_KHAI'] = 'Tờ khai thuế tài nguyên'
                rec['LOAI_THUE'] = 'TAIN'
        if default_THUE_PHU_LUC_KE_KHAI_IDS:
            for line in default_THUE_PHU_LUC_KE_KHAI_IDS:
                if len(line) > 1:
                    if line[2]:
                        if line[2]['MA_PHU_LUC'] == 'PL 01-1/GTGT':
                            rec['PL011_GTGT_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == 'PL 01-2/GTGT':
                            rec['PL012_GTGT_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == 'PL 01-5/GTGT':
                            rec['PL015_GTGT_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == 'PL 01-6/GTGT':
                            rec['PL016_GTGT_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == 'PL 01-7/GTGT':
                            rec['PL017_GTGT_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == '03-1A/TNDN':
                            rec['THUE_031A_TNDN_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == '03-2A/TNDN':
                            rec['THUE_032A_TNDN_BOLEAN'] = True
                        elif line[2]['MA_PHU_LUC'] == 'PL-BKBR/TTĐB':
                            rec['THUE_PL_BKBR_TTDB'] = True
        return rec