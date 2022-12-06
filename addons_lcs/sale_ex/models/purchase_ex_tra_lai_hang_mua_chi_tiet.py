from odoo import api, models, fields

class PURCHASE_EX_TRA_LAI_MUA_HANG_CHI_TIET_DON_DAT_HANG(models.Model):
    _inherit = 'purchase.ex.tra.lai.hang.mua.chi.tiet'

    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOA_DON_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', help='Hóa đơn bán hàng', ondelete='set null')
