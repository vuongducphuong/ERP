from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import fields, models, api, _


class KetoanBaoCaoDoanhThuTongHopParam(models.TransientModel):    
    _name = 'ketoan.bao.cao.ban.hang.tong.hop.param'    
    _description = "Báo cáo tổng hợp bán hàng"

    tu_ngay = fields.Date(string='Từ ngày',help='Từ ngày',required=True,default=fields.Datetime.now)
    den_ngay = fields.Date(string='Đến ngày ', help='Đến ngày',required=True,default=fields.Datetime.now)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)

class KetoanBaoCaoDoanhThuTongHop(models.TransientModel):    
    _name = 'ketoan.bao.cao.ban.hang.tong.hop'    

    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG_BAN = fields.Float(string='Số lượng bán ', help='Số lượng bán ', digits=0)
    DOANH_SO_BAN = fields.Float(string='Doanh số bán', help='Doanh số bán',digits= 0)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        tu_ngay = datetime.strptime(params['tu_ngay'] if 'tu_ngay' in params.keys() else 'False', '%Y-%m-%d')
        den_ngay = datetime.strptime(params['den_ngay'] if 'den_ngay' in params.keys() else 'False', '%Y-%m-%d')
        
        # Execute SQL query here
        cr = self.env.cr

        query = """
        
select name as "MA_HANG", name as "TEN_HANG", name as "DVT", 0 as "SO_LUONG_BAN", 0 as "DOANH_SO_BAN"
from res_partner
where create_date between %s and %s

        """


#         query = """
        
# select pa.name as "MA_HANG", pa.name as "TEN_HANG", pa.name as "DVT", 0 as "SO_LUONG_BAN", 0 as "DOANH_SO_BAN"
# from res_partner pa left join sale_order so on pa.id = so.partner_id
# left join sale_order_line sol on pa.id = sol.order_partner_id

#         """

        params = (tu_ngay,den_ngay)        
        cr.execute(query,params)

        for line in cr.dictfetchall():
            record.append({                
                'MA_HANG': line.get('MA_HANG', ''),
                'TEN_HANG': line.get('TEN_HANG', ''),
                'DVT': line.get('DVT', ''),
                'SO_LUONG_BAN': line.get('SO_LUONG_BAN', 0),
                'DOANH_SO_BAN': line.get('DOANH_SO_BAN', 0),
                })            
        return record
