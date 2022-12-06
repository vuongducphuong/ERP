from odoo import api, models

class MUA_HANG_PHIEU_NHAP_KHO_01_VT_REPORT(models.AbstractModel):
    _name = 'report.purchase_ex.template_phieu_nhap_kho_01_vt'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['purchase.document'].browse(docids)
               
        for record in records:
            record.print_cap_nhat_de_in()
        
        return {
            'doc_ids': docids,
            'doc_model': 'purchase.document',
            'docs': records,
            'data': data,
        }
    