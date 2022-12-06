from odoo import api, models

class QUY_PHIEU_CHI_MAU_A5_REPORT(models.AbstractModel):
    _name = 'report.account_ex.template_account_ex_phieu_chi_a5'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['account.ex.phieu.thu.chi'].browse(docids)
               
        for record in records:
            record.print_cap_nhat_de_in()
        
        return {
            'doc_ids': docids,
            'doc_model': 'account.ex.phieu.thu.chi',
            'docs': records,
            'data': data,
        }
    