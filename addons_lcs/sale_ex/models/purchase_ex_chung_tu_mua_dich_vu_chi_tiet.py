from odoo import api, models, fields

class PURCHASE_EX_CHUNG_TU_MUA_HANG_DICH_VU_CHI_TIET_HOP_DONG_BAN(models.Model):
    _inherit = 'purchase.document.line'

    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')