from odoo import api, models, fields

class ACCOUNT_EX_DON_DAT_HANG(models.Model):
    _inherit = 'sale.ex.doi.tru.chi.tiet'

    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác', ondelete='cascade')