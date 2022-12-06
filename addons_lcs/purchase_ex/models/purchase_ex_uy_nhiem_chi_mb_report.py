from odoo import api, models

class UY_NHIEM_CHI_MB_REPORT(models.AbstractModel):
    _name = 'report.purchase_ex.template_purchase_document_unc_mb'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['purchase.document'].chuyen_sang_mau_in_uy_nhiem_chi(docids)
                
        return {
            'doc_ids': docids,
            'doc_model': 'account.ex.phieu.thu.chi',
            'docs': records,
            'data': data,
        }
    