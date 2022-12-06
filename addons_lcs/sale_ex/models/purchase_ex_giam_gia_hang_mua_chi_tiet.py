from odoo import api, models, fields

class PURCHASE_EX_GIAM_GIA_HANG_MUA_CHI_TIET_DON_DAT_HANG(models.Model):
    _inherit = 'purchase.ex.giam.gia.hang.mua.chi.tiet'

    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')