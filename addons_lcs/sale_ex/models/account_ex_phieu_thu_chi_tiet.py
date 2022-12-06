from odoo import api, models, fields

class ACCOUNT_EX_PHIEU_THU_CHI_TIET_IHERIT(models.Model):
    _inherit = 'account.ex.phieu.thu.chi.tiet'

    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')