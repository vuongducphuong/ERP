from odoo import api, models, fields

class ACCOUNT_EX_DON_DAT_HANG(models.Model):
    _inherit = 'account.ex.don.dat.hang'

    BAO_GIA_ID = fields.Many2one('sale.ex.bao.gia', string='Báo giá', help='Báo giá')